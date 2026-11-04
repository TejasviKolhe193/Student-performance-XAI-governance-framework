import os
import sys
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import shap
import lime
import lime.lime_tabular

sys.stdout.reconfigure(encoding='utf-8')
os.makedirs("results", exist_ok=True)

print("=" * 80)
print("EXECUTION: STEP 3 (WINDOW NOT FEASIBLE) & STEP 4 (SHAP & LIME AUDIT)")
print("=" * 80)

# ==============================================================================
# STEP 3: MEASUREMENT WINDOW TEST AUDIT
# ==============================================================================
step3_doc = """# Step 3: Measurement-Window Feasibility Audit

## Status: Measurement Window Not Established

### Methodological Finding:
Following the reviewer's protocol, an evaluation was conducted to assess whether first-year attendance (`percentual_frequencia`) and first-year course failures (`reprovacoes`) could be reconstructed from the institutional dataset `dataset_evasao_MDE.xlsx`.

1. **Cross-Sectional Structure**: The administrative export from IFNMG contains strictly one terminal record per student (`alunoid` is 100% unique across all 15,084 records).
2. **Absence of Longitudinal Logs**: There are no term-by-term tables, semester course registration logs, or grade records in the file.
3. **Cumulative Measurement Window**: The variables `reprovacoes` (ranging up to 69 failures) and `percentual_frequencia` (ranging from 37% to 100%) represent aggregate counts calculated over the entire multi-year institutional stay of each student prior to outcome.
4. **Conclusion**: Because first-year features cannot be constructed from the administrative data without inventing or extrapolating numbers, **the measurement window cannot be restricted to the first academic year**.

### Reporting Requirement:
In accordance with Rule 4:
- The paper must state that the measurement window represents **full cumulative tenure prior to departure**, not an intake or first-year window.
- The phrases "early warning," "early identification," "early intervention," "screening," "first-year early warning," and "pre-enrollment" are withheld from the paper text.
"""

with open("step3_measurement_window.md", "w", encoding="utf-8") as f:
    f.write(step3_doc)
print("Saved step3_measurement_window.md (Measurement window not established)")

# ==============================================================================
# STEP 4: EXPLAINABILITY (SHAP & LIME ON LOCKED RF)
# ==============================================================================
print("\n" + "=" * 80)
print("STEP 4: RUNNING TREESHAP ON LOCKED RANDOM FOREST")
print("=" * 80)

# Load locked model bundle from Step 2
with open("results/chosen_model_bundle.pkl", "rb") as f:
    bundle = pickle.load(f)

rf_model = bundle["model"]
rf_features = bundle["selected_features"]
X_train_sel = bundle["X_train_rus_sel"]
X_test_sel = bundle["X_test_sel"]
y_test = bundle["y_test"]
y_prob = bundle["y_prob"]
y_pred = bundle["y_pred"]

print(f"Locked Model: {bundle['model_name']}")
print(f"Number of Selected Features: {len(rf_features)}")
print(f"Features: {rf_features}")
print(f"Test Set Size (Explained Students): N = {X_test_sel.shape[0]}")

# Run TreeSHAP
# For RandomForestClassifier, TreeExplainer computes SHAP values on probability scale or margin
explainer = shap.TreeExplainer(rf_model)
print(f"TreeSHAP Explainer initialized.")
print(f"Model output scale: probability (margin transformed via tree leaves)")

shap_values = explainer.shap_values(X_test_sel)

# Extract Dropout class (class 1)
if isinstance(shap_values, list):
    shap_vals_dropout = shap_values[1]
elif shap_values.ndim == 3:
    shap_vals_dropout = shap_values[:, :, 1]
else:
    shap_vals_dropout = shap_values

mean_abs_shap = np.mean(np.abs(shap_vals_dropout), axis=0)
total_shap = np.sum(mean_abs_shap)

shap_df = pd.DataFrame({
    "Rank": range(1, len(rf_features) + 1),
    "Feature": rf_features,
    "Mean_Abs_SHAP": mean_abs_shap,
    "Percentage_Share": (mean_abs_shap / total_shap) * 100
}).sort_values(by="Mean_Abs_SHAP", ascending=False).reset_index(drop=True)
shap_df["Rank"] = range(1, len(rf_features) + 1)

print("\n--- TREESHAP GLOBAL FEATURE ATTRIBUTIONS (ALL 19 FEATURES) ---")
print(f"Total Mean |SHAP| (Denominator): {total_shap:.6f}")
print(shap_df.to_string(index=False))

# Recompute Top-3 Share with exact formula
top3_sum = shap_df.loc[:2, "Mean_Abs_SHAP"].sum()
top3_share = (top3_sum / total_shap) * 100
top1_feat = shap_df.loc[0, "Feature"]
top1_share = shap_df.loc[0, "Percentage_Share"]
top2_feat = shap_df.loc[1, "Feature"]
top2_share = shap_df.loc[1, "Percentage_Share"]
top3_feat = shap_df.loc[2, "Feature"]
top3_share_ind = shap_df.loc[2, "Percentage_Share"]

print(f"\nTop-3 Features Attribution Calculation:")
print(f"  1. {top1_feat}: Mean |SHAP| = {shap_df.loc[0, 'Mean_Abs_SHAP']:.6f} ({top1_share:.2f}%)")
print(f"  2. {top2_feat}: Mean |SHAP| = {shap_df.loc[1, 'Mean_Abs_SHAP']:.6f} ({top2_share:.2f}%)")
print(f"  3. {top3_feat}: Mean |SHAP| = {shap_df.loc[2, 'Mean_Abs_SHAP']:.6f} ({top3_share_ind:.2f}%)")
print(f"  Numerator:   {shap_df.loc[0, 'Mean_Abs_SHAP']:.6f} + {shap_df.loc[1, 'Mean_Abs_SHAP']:.6f} + {shap_df.loc[2, 'Mean_Abs_SHAP']:.6f} = {top3_sum:.6f}")
print(f"  Denominator: {total_shap:.6f}")
print(f"  Exact Top-3 Cumulative Share: {top3_share:.2f}% (Recomputed directly from data; not 71.3% or 52%)")

shap_df.to_csv("results/step4_shap_attributions.csv", index=False)
print("Saved results/step4_shap_attributions.csv")

# Save Beeswarm and Bar Plots
plt.figure(figsize=(10, 6))
shap.summary_plot(shap_vals_dropout, X_test_sel, feature_names=rf_features, show=False)
plt.title("TreeSHAP Global Summary (Random Forest Champion, N = 4,526)", fontsize=13, pad=12)
plt.tight_layout()
plt.savefig("results/fig2_shap_beeswarm.png", dpi=300, bbox_inches="tight")
plt.close()

plt.figure(figsize=(10, 6))
top_plot = shap_df.head(10).sort_values(by="Mean_Abs_SHAP", ascending=True)
plt.barh(top_plot["Feature"], top_plot["Mean_Abs_SHAP"], color="#1f77b4")
plt.xlabel(f"Mean |SHAP Value| (Denominator Total = {total_shap:.4f})")
plt.title("Top 10 Predictors by Mean Absolute SHAP Attribution", fontsize=13)
plt.tight_layout()
plt.savefig("results/fig3_shap_importance.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved results/fig2_shap_beeswarm.png and results/fig3_shap_importance.png")

# ==============================================================================
# LIME LOCAL EXPLANATIONS & JACCARD STABILITY
# ==============================================================================
print("\n" + "=" * 80)
print("RUNNING LIME ON CASE-STUDY ARCHETYPES & COMPUTING JACCARD OVERLAP")
print("=" * 80)

# Select same 3 representative students
np.random.seed(42)
high_risk_candidates = np.where(y_prob >= 0.80)[0]
borderline_candidates = np.where((y_prob >= 0.45) & (y_prob <= 0.55))[0]
low_risk_candidates = np.where(y_prob <= 0.20)[0]

high_idx = int(np.random.choice(high_risk_candidates))
border_idx = int(np.random.choice(borderline_candidates))
low_idx = int(np.random.choice(low_risk_candidates))

archetypes = [
    {"label": "High-Risk Student", "index": high_idx, "prob": y_prob[high_idx], "true_label": int(y_test[high_idx])},
    {"label": "Borderline Student", "index": border_idx, "prob": y_prob[border_idx], "true_label": int(y_test[border_idx])},
    {"label": "Low-Risk Student", "index": low_idx, "prob": y_prob[low_idx], "true_label": int(y_test[low_idx])},
]

print("Selected Archetypes:")
for a in archetypes:
    print(f"  {a['label']:<20s} (Index {a['index']:>4d}): P(Dropout) = {a['prob']:.4f}, Actual = {a['true_label']}")

# Fit LIME Tabular Explainer
lime_explainer = lime.lime_tabular.LimeTabularExplainer(
    training_data=X_train_sel,
    feature_names=rf_features,
    class_names=["Completed", "Dropout"],
    mode="classification",
    random_state=42
)

jaccard_data = []

for a in archetypes:
    idx = a["index"]
    instance = X_test_sel[idx]
    
    # 1. Top-3 SHAP
    student_shap = shap_vals_dropout[idx]
    top3_shap_indices = np.argsort(np.abs(student_shap))[::-1][:3]
    top3_shap_names = [rf_features[i] for i in top3_shap_indices]
    
    # 2. Top-3 LIME
    exp = lime_explainer.explain_instance(
        data_row=instance,
        predict_fn=rf_model.predict_proba,
        num_features=6
    )
    
    lime_feats = []
    for f_str, weight in exp.as_list():
        for fn in rf_features:
            if fn in f_str:
                if fn not in lime_feats:
                    lime_feats.append(fn)
                break
        if len(lime_feats) == 3:
            break
            
    # Compute Jaccard
    set_s = set(top3_shap_names)
    set_l = set(lime_feats)
    inter = set_s.intersection(set_l)
    union = set_s.union(set_l)
    jaccard = len(inter) / len(union) if len(union) > 0 else 0.0
    
    jaccard_data.append({
        "Archetype": a["label"],
        "Test_Index": idx,
        "Predicted_Risk": round(a["prob"], 4),
        "Actual_Outcome": a["true_label"],
        "SHAP_Top3": top3_shap_names,
        "LIME_Top3": lime_feats,
        "Common_Features": list(inter),
        "Intersection_Count": len(inter),
        "Union_Count": len(union),
        "Jaccard_Overlap": round(jaccard, 4)
    })

jaccard_df = pd.DataFrame(jaccard_data)
mean_jaccard = jaccard_df["Jaccard_Overlap"].mean()
min_jaccard = jaccard_df["Jaccard_Overlap"].min()
max_jaccard = jaccard_df["Jaccard_Overlap"].max()

print("\n--- SHAP VS. LIME TOP-3 JACCARD OVERLAP ---")
for _, r in jaccard_df.iterrows():
    print(f"Archetype: {r['Archetype']:<20s} (Index {r['Test_Index']})")
    print(f"  SHAP Top-3: {r['SHAP_Top3']}")
    print(f"  LIME Top-3: {r['LIME_Top3']}")
    print(f"  Common:     {r['Common_Features']} -> Jaccard = {r['Jaccard_Overlap']:.4f}")

print(f"\nSummary Concordance Statistics:")
print(f"  Mean Jaccard Overlap: {mean_jaccard:.4f} ({mean_jaccard*100:.1f}%)")
print(f"  Range: [{min_jaccard:.4f}, {max_jaccard:.4f}]")

# Classify agreement
if mean_jaccard < 0.40:
    agreement_str = "weak agreement"
elif mean_jaccard < 0.70:
    agreement_str = "moderate agreement"
else:
    agreement_str = "strong agreement"

print(f"  Concordance Characterization: {agreement_str} ({mean_jaccard*100:.1f}% mean feature overlap).")
print("  Note: In accordance with Rule 5, this level of overlap is characterized as weak-to-moderate agreement and is NOT claimed to confirm explanatory reliability.")

jaccard_df.to_csv("results/step4_lime_shap_concordance.csv", index=False)
print("Saved results/step4_lime_shap_concordance.csv")

# Save step4 bundle for subsequent steps
step4_bundle = {
    "shap_df": shap_df,
    "total_shap": total_shap,
    "top3_share": top3_share,
    "jaccard_df": jaccard_df,
    "mean_jaccard": mean_jaccard,
    "min_jaccard": min_jaccard,
    "max_jaccard": max_jaccard,
    "agreement_str": agreement_str
}
with open("results/step4_bundle.pkl", "wb") as f:
    pickle.dump(step4_bundle, f)
print("Saved results/step4_bundle.pkl")

print("\n" + "=" * 80)
print("STEP 3 & STEP 4 COMPLETE!")
print("=" * 80)

