"""
Phase 3: Explainable AI (XAI) Pipeline
- Computes TreeSHAP global summary (beeswarm) and feature importance on the champion model.
- Explains 3 distinct students (High-Risk, Borderline, Low-Risk) via local SHAP waterfall.
- Explains the exact same 3 students via LIME.
- Calculates top-3 Jaccard similarity between SHAP and LIME across the 3 cases.
- Saves high-res figures and phase3_shap_lime_metrics.csv.
"""

import os
import sys
import io
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import shap
import lime
import lime.lime_tabular

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace", line_buffering=True)

OUTPUT_DIR = "phase3_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 80)
print("PHASE 3: EXPLAINABILITY (SHAP & LIME REPLICATION)")
print("=" * 80)

# Load Phase 2 champion bundle
with open("phase2_outputs/champion_model_bundle.pkl", "rb") as f:
    p2 = pickle.load(f)

# We evaluate the champion RF model (or DT)
# Let's use champion RF for TreeSHAP and DT for surrogate
rf_model = p2["champion_rf"]
rf_mask = p2["champion_mask"]
rf_features = p2["champion_features"]

dt_model = p2["surrogate_dt"]
dt_mask = p2["surrogate_mask"]
dt_features = p2["surrogate_features"]

X_train_rf = p2["X_train"][:, rf_mask]
X_test_rf = p2["X_test"][:, rf_mask]
y_test = p2["y_test"]

print(f"Loaded RF Model with {len(rf_features)} features.")
print(f"Features: {rf_features}")

# Compute predictions and probabilities
test_probs = rf_model.predict_proba(X_test_rf)[:, 1]
test_preds = (test_probs >= 0.5).astype(int)

# 1. Global TreeSHAP
print("\nComputing TreeSHAP values on test set...")
explainer_rf = shap.TreeExplainer(rf_model)
# For efficiency and reliability, evaluate on full test set (4526 samples) or representative subset
shap_values_rf = explainer_rf.shap_values(X_test_rf)

# Handle 2-class or 3D shap values
if isinstance(shap_values_rf, list):
    shap_vals_class1 = shap_values_rf[1]
elif shap_values_rf.ndim == 3:
    shap_vals_class1 = shap_values_rf[:, :, 1]
else:
    shap_vals_class1 = shap_values_rf

# Global Feature Importance (Mean Absolute SHAP)
mean_abs_shap = np.mean(np.abs(shap_vals_class1), axis=0)
feat_imp_df = pd.DataFrame({
    "Feature": rf_features,
    "Mean_Abs_SHAP": mean_abs_shap
}).sort_values(by="Mean_Abs_SHAP", ascending=False).reset_index(drop=True)

print("\nTOP 5 FEATURES BY MEAN ABSOLUTE SHAP VALUE:")
print(feat_imp_df.head(5).to_string(index=False))

# Save Global SHAP Beeswarm Plot
plt.figure(figsize=(10, 6))
shap.summary_plot(shap_vals_class1, X_test_rf, feature_names=rf_features, show=False)
plt.title("Global SHAP Summary (TreeSHAP) - Silva et al. Feature Set", fontsize=14, pad=15)
plt.tight_layout()
beeswarm_path = os.path.join(OUTPUT_DIR, "01_shap_global_beeswarm.png")
plt.savefig(beeswarm_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"Saved: {beeswarm_path}")

# Save Feature Importance Bar Plot
plt.figure(figsize=(10, 6))
top_10 = feat_imp_df.head(10).sort_values(by="Mean_Abs_SHAP", ascending=True)
plt.barh(top_10["Feature"], top_10["Mean_Abs_SHAP"], color="#1f77b4")
plt.xlabel("Mean |SHAP Value| (Impact on Model Output)")
plt.title("Top 10 Features by Mean Absolute SHAP Impact", fontsize=14)
plt.tight_layout()
bar_path = os.path.join(OUTPUT_DIR, "02_shap_feature_importance.png")
plt.savefig(bar_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"Saved: {bar_path}")

# 2. Select 3 Representative Students
# High-risk: prob > 0.80
# Borderline: 0.45 <= prob <= 0.55
# Low-risk: prob < 0.20
np.random.seed(42)

high_risk_candidates = np.where(test_probs >= 0.80)[0]
borderline_candidates = np.where((test_probs >= 0.45) & (test_probs <= 0.55))[0]
low_risk_candidates = np.where(test_probs <= 0.20)[0]

high_idx = int(np.random.choice(high_risk_candidates))
border_idx = int(np.random.choice(borderline_candidates))
low_idx = int(np.random.choice(low_risk_candidates))

selected_students = [
    {"label": "High-Risk Student", "index": high_idx, "prob": test_probs[high_idx], "true_label": int(y_test[high_idx])},
    {"label": "Borderline Student", "index": border_idx, "prob": test_probs[border_idx], "true_label": int(y_test[border_idx])},
    {"label": "Low-Risk Student", "index": low_idx, "prob": test_probs[low_idx], "true_label": int(y_test[low_idx])},
]

print("\nSELECTED 3 CASE-STUDY STUDENTS:")
for s in selected_students:
    print(f"  {s['label']:<20s} (Test Index: {s['index']:>4d}): Predicted P(Dropout) = {s['prob']:.4f}, Actual = {s['true_label']}")

# 3. Local SHAP Waterfall Plots
base_value = explainer_rf.expected_value
if isinstance(base_value, (list, np.ndarray)):
    base_val_class1 = base_value[1]
else:
    base_val_class1 = base_value

shap_top3 = {}
for s in selected_students:
    idx = s["index"]
    student_shap = shap_vals_class1[idx]
    
    # Sort top 3 features by absolute SHAP value
    top3_idx = np.argsort(np.abs(student_shap))[::-1][:3]
    top3_feats = [rf_features[i] for i in top3_idx]
    shap_top3[s["label"]] = set(top3_feats)
    
    # Save local waterfall/bar plot
    plt.figure(figsize=(9, 5))
    order = np.argsort(student_shap)
    colors = ["#d62728" if v > 0 else "#1f77b4" for v in student_shap[order]]
    plt.barh([rf_features[i] for i in order], student_shap[order], color=colors)
    plt.axvline(0, color="black", linestyle="--", linewidth=0.8)
    plt.title(f"Local SHAP: {s['label']} (Index #{idx}, P(Dropout)={s['prob']:.1%})", fontsize=12)
    plt.xlabel("SHAP Value (Contribution to Dropout Log-Odds / Risk)")
    plt.tight_layout()
    plot_file = os.path.join(OUTPUT_DIR, f"04_shap_{s['label'].lower().replace(' ', '_')}_{idx}.png")
    plt.savefig(plot_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved SHAP waterfall bar for {s['label']}: {plot_file}")

# 4. LIME Explanations for the Same 3 Students
print("\nFitting LIME Tabular Explainer...")
lime_explainer = lime.lime_tabular.LimeTabularExplainer(
    training_data=X_train_rf,
    feature_names=rf_features,
    class_names=["Completed", "Dropped Out"],
    mode="classification",
    random_state=42
)

lime_top3 = {}
for s in selected_students:
    idx = s["index"]
    instance = X_test_rf[idx]
    
    exp = lime_explainer.explain_instance(
        data_row=instance,
        predict_fn=rf_model.predict_proba,
        num_features=5
    )
    
    # Save HTML report
    html_file = os.path.join(OUTPUT_DIR, f"05_lime_{s['label'].lower().replace(' ', '_')}_{idx}.html")
    exp.save_to_file(html_file)
    
    # Extract top 3 features
    lime_feats = []
    for f_str, weight in exp.as_list():
        # Match feature name from condition string
        for fn in rf_features:
            if fn in f_str:
                if fn not in lime_feats:
                    lime_feats.append(fn)
                break
        if len(lime_feats) == 3:
            break
    lime_top3[s["label"]] = set(lime_feats)
    print(f"Saved LIME report for {s['label']}: {html_file}")

# 5. Compute Top-3 Jaccard Overlap
print("\n" + "=" * 80)
print("SHAP VS. LIME TOP-3 JACCARD OVERLAP AUDIT:")
print("=" * 80)

jaccard_results = []
for s in selected_students:
    lbl = s["label"]
    s_set = shap_top3[lbl]
    l_set = lime_top3[lbl]
    intersection = s_set.intersection(l_set)
    union = s_set.union(l_set)
    jaccard = len(intersection) / len(union) if len(union) > 0 else 1.0
    
    jaccard_results.append({
        "Student_Case": lbl,
        "Test_Index": s["index"],
        "Predicted_Dropout_Risk": round(s["prob"], 4),
        "SHAP_Top3": list(s_set),
        "LIME_Top3": list(l_set),
        "Common_Features": list(intersection),
        "Jaccard_Similarity": round(jaccard, 4)
    })
    print(f"Case: {lbl:<22s} | Index: {s['index']:>4d} | Risk: {s['prob']:.2%}")
    print(f"  SHAP Top-3: {list(s_set)}")
    print(f"  LIME Top-3: {list(l_set)}")
    print(f"  Overlap:    {list(intersection)} -> Jaccard Similarity = {jaccard:.4f}")

mean_jaccard = np.mean([r["Jaccard_Similarity"] for r in jaccard_results])
print(f"\nMean Top-3 Jaccard Similarity across archetypes: {mean_jaccard:.4f}")
print(">> Methodological Note: As instructed, LIME/SHAP agreement is reported factually as empirical overlap and is NOT claimed as a proof of ground-truth model reliability.")

# Save Phase 3 Metrics CSV
pd.DataFrame(jaccard_results).to_csv(os.path.join(OUTPUT_DIR, "phase3_shap_lime_metrics.csv"), index=False)
feat_imp_df.to_csv(os.path.join(OUTPUT_DIR, "phase3_feature_importance.csv"), index=False)
print("Saved phase3_outputs/phase3_shap_lime_metrics.csv and phase3_outputs/phase3_feature_importance.csv")
print("PHASE 3 COMPLETE!")

