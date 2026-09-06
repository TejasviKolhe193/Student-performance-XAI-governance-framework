"""
Phase 2: Class Balancing, Feature Selection, Model Training & Evaluation
=========================================================================
Replicates the base paper's experimental setup:
  - 4 balancing strategies × 3 feature selection methods × 4 ML models = 48 experiments
  - GridSearchCV hyperparameter tuning
  - Model ranking: 1st Recall → 2nd Precision → 3rd 10-fold CV
  - Select top models for XAI (Phase 3)
"""

import sys
import io
import warnings
import numpy as np
import pandas as pd
import pickle
import os
import time
from collections import defaultdict

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.metrics import (
    precision_score, recall_score, f1_score, roc_auc_score,
    accuracy_score, classification_report, confusion_matrix
)
from sklearn.feature_selection import (
    SelectKBest, f_classif, SequentialFeatureSelector
)

from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.combine import SMOTEENN

# ── Handle encoding for Windows console ──────────────────────────────
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace", line_buffering=True)
warnings.filterwarnings("ignore")

INPUT_DIR = "phase1_outputs"
OUTPUT_DIR = "phase2_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════
# LOAD PHASE 1 DATA
# ═══════════════════════════════════════════════════════════════════════
print("=" * 72)
print("LOADING PHASE 1 DATA")
print("=" * 72)

with open(os.path.join(INPUT_DIR, "phase1_data.pkl"), "rb") as f:
    data = pickle.load(f)

X_train = data["X_train"]
X_test = data["X_test"]
y_train = data["y_train"]
y_test = data["y_test"]
feature_names = data["feature_names"]

print(f"  Train: {X_train.shape[0]} samples, {X_train.shape[1]} features")
print(f"  Test:  {X_test.shape[0]} samples")
print(f"  Train class distribution: 0={( y_train == 0).sum()}, 1={(y_train == 1).sum()}")

# ═══════════════════════════════════════════════════════════════════════
# STEP 1 — CLASS BALANCING (Training set only)
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("STEP 1: CLASS BALANCING (training set only)")
print("=" * 72)

balancing_strategies = {
    "Unbalanced": None,
    "UnderSampling": RandomUnderSampler(random_state=42),
    "OverSampling (SMOTE)": SMOTE(random_state=42),
    "SMOTEENN": SMOTEENN(random_state=42),
}

balanced_datasets = {}
for name, sampler in balancing_strategies.items():
    if sampler is None:
        X_bal, y_bal = X_train.copy(), y_train.copy()
    else:
        X_bal, y_bal = sampler.fit_resample(X_train, y_train)

    balanced_datasets[name] = (X_bal, y_bal)
    c0 = (y_bal == 0).sum()
    c1 = (y_bal == 1).sum()
    print(f"  {name:<25s}: {len(y_bal):>6d} samples  "
          f"(Class 0: {c0:>5d} [{c0/len(y_bal)*100:5.1f}%], "
          f"Class 1: {c1:>5d} [{c1/len(y_bal)*100:5.1f}%])")

# ═══════════════════════════════════════════════════════════════════════
# STEP 2 — FEATURE SELECTION METHODS
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("STEP 2: FEATURE SELECTION")
print("=" * 72)


def anova_feature_selection(X, y, feature_names, k=15):
    """Filter method: ANOVA F-test, select top-k features."""
    selector = SelectKBest(f_classif, k=min(k, X.shape[1]))
    selector.fit(X, y)
    mask = selector.get_support()
    selected = [f for f, m in zip(feature_names, mask) if m]
    scores = selector.scores_
    return mask, selected, scores


def backward_selection(X, y, feature_names):
    """Wrapper method: Backward elimination using RF as estimator."""
    estimator = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
    sfs = SequentialFeatureSelector(
        estimator, direction="backward",
        n_features_to_select="auto",  # selects half by default
        scoring="recall", cv=3, n_jobs=-1
    )
    sfs.fit(X, y)
    mask = sfs.get_support()
    selected = [f for f, m in zip(feature_names, mask) if m]
    return mask, selected


def feature_importance_selection(X, y, feature_names, threshold=0.01):
    """Embedded method: RF feature importance, keep features above threshold."""
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X, y)
    importances = rf.feature_importances_
    mask = importances >= threshold
    selected = [f for f, m in zip(feature_names, mask) if m]
    return mask, selected, importances


# Run FS on the SMOTEENN-balanced training set (most representative)
# The paper's top models used Backward Selection and ANOVA on balanced data
X_fs, y_fs = balanced_datasets["SMOTEENN"]

print("\n── 2a. ANOVA (Filter Method) ──")
anova_mask, anova_features, anova_scores = anova_feature_selection(
    X_fs, y_fs, feature_names, k=15
)
print(f"  Selected {len(anova_features)} features:")
sorted_anova = sorted(zip(feature_names, anova_scores), key=lambda x: -x[1])
for fname, score in sorted_anova[:15]:
    marker = " ✓" if fname in anova_features else ""
    print(f"    {fname:<35s} F={score:>10.2f}{marker}")

print("\n── 2b. Backward Selection (Wrapper Method) ──")
t0 = time.time()
backward_mask, backward_features = backward_selection(X_fs, y_fs, feature_names)
print(f"  Completed in {time.time() - t0:.1f}s")
print(f"  Selected {len(backward_features)} features:")
for fname in backward_features:
    print(f"    ✓ {fname}")

print("\n── 2c. Feature Importance (Embedded Method) ──")
fi_mask, fi_features, fi_importances = feature_importance_selection(
    X_fs, y_fs, feature_names
)
print(f"  Selected {len(fi_features)} features (importance ≥ 0.01):")
sorted_fi = sorted(zip(feature_names, fi_importances), key=lambda x: -x[1])
for fname, imp in sorted_fi:
    marker = " ✓" if fname in fi_features else "  "
    print(f"   {marker} {fname:<35s} importance={imp:.4f}")

fs_methods = {
    "ANOVA": anova_mask,
    "Backward": backward_mask,
    "FeatureImportance": fi_mask,
}

# ═══════════════════════════════════════════════════════════════════════
# STEP 3 — MODEL TRAINING (48 experiments)
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("STEP 3: MODEL TRAINING — 48 EXPERIMENTS")
print("=" * 72)

# ── Model definitions with hyperparameter grids ──
model_configs = {
    "RF": {
        "estimator": RandomForestClassifier(random_state=42, n_jobs=-1),
        "param_grid": {
            "max_depth": [None, 10, 20],
            "min_samples_split": [2, 5],
            "criterion": ["gini", "entropy"],
        }
    },
    "DT": {
        "estimator": DecisionTreeClassifier(random_state=42),
        "param_grid": {
            "max_depth": [None, 10, 20],
            "min_samples_split": [2, 5],
            "criterion": ["gini", "entropy"],
        }
    },
    "LR": {
        "estimator": LogisticRegression(random_state=42, max_iter=1000),
        "param_grid": {
            "C": [0.1, 1.0, 10.0],
            "solver": ["lbfgs", "liblinear"],
        }
    },
    "SVM": {
        "estimator": SVC(random_state=42, probability=True, max_iter=2000),
        "param_grid": {
            "C": [0.1, 1.0, 10.0],
            "kernel": ["rbf", "linear"],
        }
    },
}

results = []
trained_models = {}
experiment_num = 0
total_experiments = len(balancing_strategies) * len(fs_methods) * len(model_configs)

cv_inner = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

print(f"\n  Running {total_experiments} experiments "
      f"({len(balancing_strategies)} balance × {len(fs_methods)} FS × {len(model_configs)} models)")
print(f"  {'#':>3s} {'Balance':<18s} {'FS':<18s} {'Model':<5s} "
      f"{'Recall':>7s} {'Prec':>7s} {'F1':>7s} {'AUC':>7s} {'Acc':>7s} {'10-CV':>7s}")
print(f"  {'-'*3} {'-'*18} {'-'*18} {'-'*5} "
      f"{'-'*7} {'-'*7} {'-'*7} {'-'*7} {'-'*7} {'-'*7}")

for bal_name, (X_bal, y_bal) in balanced_datasets.items():
    for fs_name, fs_mask in fs_methods.items():
        # Apply feature selection mask
        X_train_fs = X_bal[:, fs_mask]
        X_test_fs = X_test[:, fs_mask]

        for model_name, config in model_configs.items():
            experiment_num += 1
            exp_key = f"{bal_name}_{fs_name}_{model_name}"

            # GridSearchCV for hyperparameter tuning
            grid = GridSearchCV(
                config["estimator"],
                config["param_grid"],
                scoring="recall",
                cv=cv_inner,
                n_jobs=-1,
                refit=True,
            )
            grid.fit(X_train_fs, y_bal)
            best_model = grid.best_estimator_

            # Predict on held-out test set
            y_pred = best_model.predict(X_test_fs)
            y_proba = best_model.predict_proba(X_test_fs)[:, 1]

            # Metrics
            recall = recall_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            auc = roc_auc_score(y_test, y_proba)
            acc = accuracy_score(y_test, y_pred)

            # 10-fold CV on the balanced training data
            cv10 = cross_val_score(
                best_model, X_train_fs, y_bal,
                cv=StratifiedKFold(n_splits=10, shuffle=True, random_state=42),
                scoring="recall", n_jobs=-1
            )
            mean_cv10 = cv10.mean()

            results.append({
                "Balance": bal_name,
                "FS": fs_name,
                "Model": model_name,
                "Recall": round(recall, 3),
                "Precision": round(precision, 3),
                "F1": round(f1, 3),
                "AUC": round(auc, 3),
                "Accuracy": round(acc, 3),
                "10-CV Recall": round(mean_cv10, 3),
                "Best Params": str(grid.best_params_),
            })

            # Store trained model
            trained_models[exp_key] = {
                "model": best_model,
                "fs_mask": fs_mask,
                "params": grid.best_params_,
            }

            print(f"  {experiment_num:>3d} {bal_name:<18s} {fs_name:<18s} {model_name:<5s} "
                  f"{recall:>7.3f} {precision:>7.3f} {f1:>7.3f} {auc:>7.3f} {acc:>7.3f} {mean_cv10:>7.3f}", flush=True)

# ═══════════════════════════════════════════════════════════════════════
# STEP 4 — MODEL RANKING & TOP-5 SELECTION
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("STEP 4: MODEL RANKING (Recall → Precision → 10-CV)")
print("=" * 72)

df_results = pd.DataFrame(results)

# Sort by paper's criteria: 1st Recall, 2nd Precision, 3rd 10-CV
df_sorted = df_results.sort_values(
    by=["Recall", "Precision", "10-CV Recall"],
    ascending=[False, False, False]
).reset_index(drop=True)

print("\n── TOP 10 MODELS ──")
print(df_sorted.head(10).to_string(index=True))

# ── Select top 2 for XAI (matching paper: RF and DT with SMOTEENN) ──
print("\n── TOP 5 MODELS (for XAI consideration) ──")
top5 = df_sorted.head(5)
for i, row in top5.iterrows():
    print(f"\n  #{i+1}: {row['Model']} | {row['Balance']} | {row['FS']}")
    print(f"      Recall={row['Recall']:.3f}  Precision={row['Precision']:.3f}  "
          f"F1={row['F1']:.3f}  AUC={row['AUC']:.3f}  10-CV={row['10-CV Recall']:.3f}")
    print(f"      Params: {row['Best Params']}")

# ── Identify the best RF and best DT for XAI (matching paper) ──
best_rf = df_sorted[df_sorted["Model"] == "RF"].head(1)
best_dt = df_sorted[df_sorted["Model"] == "DT"].head(1)

print("\n── SELECTED MODELS FOR XAI (Phase 3) ──")
for label, model_row in [("Best RF", best_rf), ("Best DT", best_dt)]:
    if not model_row.empty:
        r = model_row.iloc[0]
        key = f"{r['Balance']}_{r['FS']}_{r['Model']}"
        print(f"\n  {label}: {r['Model']} | {r['Balance']} | {r['FS']}")
        print(f"    Recall={r['Recall']:.3f}  Precision={r['Precision']:.3f}  "
              f"F1={r['F1']:.3f}  AUC={r['AUC']:.3f}")
        print(f"    Params: {r['Best Params']}")

# ── Confusion matrices for selected models ──
print("\n── CONFUSION MATRICES (Selected Models) ──")
for label, model_row in [("Best RF", best_rf), ("Best DT", best_dt)]:
    if not model_row.empty:
        r = model_row.iloc[0]
        key = f"{r['Balance']}_{r['FS']}_{r['Model']}"
        model_info = trained_models[key]
        X_test_sel = X_test[:, model_info["fs_mask"]]
        y_pred_sel = model_info["model"].predict(X_test_sel)
        cm = confusion_matrix(y_test, y_pred_sel)
        print(f"\n  {label} ({r['Model']} | {r['Balance']} | {r['FS']}):")
        print(f"                  Predicted")
        print(f"                  Comp   Drop")
        print(f"    Actual Comp  {cm[0][0]:>5d}  {cm[0][1]:>5d}")
        print(f"    Actual Drop  {cm[1][0]:>5d}  {cm[1][1]:>5d}")
        print(f"\n  {classification_report(y_test, y_pred_sel, target_names=['Completed', 'Dropped Out'])}")

# ═══════════════════════════════════════════════════════════════════════
# SAVE OUTPUTS
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("SAVING PHASE 2 OUTPUTS")
print("=" * 72)

# Save full results table
csv_path = os.path.join(OUTPUT_DIR, "experiment_results.csv")
df_sorted.to_csv(csv_path, index=False)
print(f"  Saved: {csv_path}")

# Save selected models for Phase 3
best_rf_key = f"{best_rf.iloc[0]['Balance']}_{best_rf.iloc[0]['FS']}_{best_rf.iloc[0]['Model']}" if not best_rf.empty else None
best_dt_key = f"{best_dt.iloc[0]['Balance']}_{best_dt.iloc[0]['FS']}_{best_dt.iloc[0]['Model']}" if not best_dt.empty else None

selected_for_xai = {}
if best_rf_key:
    selected_for_xai["RF"] = trained_models[best_rf_key]
    selected_for_xai["RF"]["metrics"] = best_rf.iloc[0].to_dict()
if best_dt_key:
    selected_for_xai["DT"] = trained_models[best_dt_key]
    selected_for_xai["DT"]["metrics"] = best_dt.iloc[0].to_dict()

# Also save test data needed for XAI
selected_for_xai["X_test"] = X_test
selected_for_xai["y_test"] = y_test
selected_for_xai["feature_names"] = feature_names

pkl_path = os.path.join(OUTPUT_DIR, "phase2_models.pkl")
with open(pkl_path, "wb") as f:
    pickle.dump(selected_for_xai, f)
print(f"  Saved: {pkl_path}")

# Save all trained models
all_models_path = os.path.join(OUTPUT_DIR, "all_trained_models.pkl")
with open(all_models_path, "wb") as f:
    pickle.dump(trained_models, f)
print(f"  Saved: {all_models_path}")

print("\n" + "=" * 72)
print("✅ PHASE 2 COMPLETE — Ready for Phase 3 (XAI: LIME + SHAP)")
print("=" * 72)
