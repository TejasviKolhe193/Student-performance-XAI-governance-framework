# -*- coding: utf-8 -*-
"""
phase2_retrain_no_gpa.py
Retrains Phase 2 without GPA (ira) to eliminate target leakage and replicate
the pre-enrollment / non-academic paradigm of Silva et al. (2025).
Runs the full 48-experiment factorial matrix:
4 Balancing × 3 Feature Selection × 4 Algorithms.
"""

import sys, io, os, time, warnings
import numpy as np
import pandas as pd
import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.metrics import recall_score, precision_score, f1_score, roc_auc_score, accuracy_score
from sklearn.feature_selection import SelectKBest, f_classif, SequentialFeatureSelector

from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.combine import SMOTEENN

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace", line_buffering=True)
warnings.filterwarnings("ignore")

OUTPUT_DIR = "phase2_no_gpa_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════
# STEP 1: LOAD PREPROCESSED DATA & DROP 'ira' (GPA)
# ═══════════════════════════════════════════════════════════════════════
print("=" * 72)
print("STEP 1: PREPARING DATA WITHOUT GPA (ira)")
print("=" * 72)

raw_df = pd.read_csv("phase1_outputs/preprocessed_dataset_portuguese.csv")
print(f"Loaded preprocessed dataset: {raw_df.shape[0]} rows × {raw_df.shape[1]} columns")

# Drop target and 'ira'
y = raw_df["target_dropout"].values
feature_df = raw_df.drop(columns=["target_dropout", "ira"])
feature_names = feature_df.columns.tolist()

print(f"Total features after dropping 'ira': {len(feature_names)}")
print("First 10 features:", feature_names[:10])

X = feature_df.values

# Stratified 80/20 train/test split (random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print(f"\nTrain set: {X_train.shape[0]} samples (Class 0: {(y_train==0).sum()}, Class 1: {(y_train==1).sum()})")
print(f"Test set:  {X_test.shape[0]} samples (Class 0: {(y_test==0).sum()}, Class 1: {(y_test==1).sum()})")

# ═══════════════════════════════════════════════════════════════════════
# STEP 2: CLASS BALANCING STRATEGIES (ON TRAINING DATA ONLY)
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("STEP 2: CLASS BALANCING (TRAINING DATA ONLY)")
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
    print(f"  {name:<22s}: {len(y_bal):>6d} samples (Class 0: {c0:>5d}, Class 1: {c1:>5d})")

# ═══════════════════════════════════════════════════════════════════════
# STEP 3: FEATURE SELECTION ON BALANCED SMOTEENN SET
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("STEP 3: FEATURE SELECTION (WITHOUT GPA)")
print("=" * 72)

X_fs, y_fs = balanced_datasets["SMOTEENN"]

# 3a. ANOVA F-Test (Top 15)
anova_k = min(15, X_fs.shape[1])
selector_anova = SelectKBest(f_classif, k=anova_k)
selector_anova.fit(X_fs, y_fs)
anova_mask = selector_anova.get_support()
anova_features = [f for f, m in zip(feature_names, anova_mask) if m]
print(f"  ANOVA selected {len(anova_features)} features: {anova_features[:5]} ...")

# 3b. Backward Elimination using fast RF
print("  Running Backward Selection...")
t0 = time.time()
sfs = SequentialFeatureSelector(
    RandomForestClassifier(n_estimators=40, random_state=42, n_jobs=-1),
    direction="backward",
    n_features_to_select=15,
    scoring="recall", cv=3, n_jobs=-1
)
sfs.fit(X_fs, y_fs)
backward_mask = sfs.get_support()
backward_features = [f for f, m in zip(feature_names, backward_mask) if m]
print(f"  Backward Selection selected {len(backward_features)} features in {time.time()-t0:.1f}s: {backward_features[:5]} ...")

# 3c. Feature Importance Selection (threshold >= 0.01)
rf_imp = RandomForestClassifier(n_estimators=80, random_state=42, n_jobs=-1)
rf_imp.fit(X_fs, y_fs)
fi_mask = rf_imp.feature_importances_ >= 0.01
fi_features = [f for f, m in zip(feature_names, fi_mask) if m]
print(f"  Feature Importance selected {len(fi_features)} features: {fi_features[:5]} ...")

fs_methods = {
    "ANOVA": anova_mask,
    "Backward": backward_mask,
    "FeatureImportance": fi_mask,
}

# ═══════════════════════════════════════════════════════════════════════
# STEP 4: MODEL CONFIGURATIONS & 48-EXPERIMENT MATRIX
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("STEP 4: RUNNING 48 EXPERIMENTS (NO GPA)")
print("=" * 72)

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

cv_inner = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
results = []
trained_models = {}
exp_idx = 0

t_start = time.time()

for bal_name, (X_bal, y_bal) in balanced_datasets.items():
    for fs_name, fs_mask in fs_methods.items():
        X_train_fs = X_bal[:, fs_mask]
        X_test_fs = X_test[:, fs_mask]
        
        for model_name, config in model_configs.items():
            exp_idx += 1
            exp_key = f"{bal_name}_{fs_name}_{model_name}"
            
            # GridSearchCV on inner folds
            grid = GridSearchCV(
                config["estimator"],
                config["param_grid"],
                scoring="recall",
                cv=cv_inner,
                n_jobs=-1,
                refit=True
            )
            grid.fit(X_train_fs, y_bal)
            best_m = grid.best_estimator_
            
            # Held-out test evaluation
            y_pred = best_m.predict(X_test_fs)
            y_prob = best_m.predict_proba(X_test_fs)[:, 1]
            
            rec = recall_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)
            auc = roc_auc_score(y_test, y_prob)
            acc = accuracy_score(y_test, y_pred)
            
            # 10-fold CV stability on balanced train set
            cv10 = cross_val_score(
                best_m, X_train_fs, y_bal,
                cv=StratifiedKFold(n_splits=10, shuffle=True, random_state=42),
                scoring="recall", n_jobs=-1
            )
            mean_cv10 = cv10.mean()
            
            trained_models[exp_key] = {
                "model": best_m,
                "fs_mask": fs_mask,
                "best_params": grid.best_params_,
                "features": [f for f, m in zip(feature_names, fs_mask) if m]
            }
            
            rec_row = {
                "Balance": bal_name,
                "FS": fs_name,
                "Model": model_name,
                "Recall": round(rec, 3),
                "Precision": round(prec, 3),
                "F1": round(f1, 3),
                "AUC": round(auc, 3),
                "Accuracy": round(acc, 3),
                "10-CV Recall": round(mean_cv10, 3),
                "Best Params": str(grid.best_params_)
            }
            results.append(rec_row)
            print(f"[{exp_idx:02d}/48] {exp_key:<35s} | Rec: {rec:.3f} | Prec: {prec:.3f} | F1: {f1:.3f} | AUC: {auc:.3f} | Acc: {acc:.3f}")

print(f"\nAll 48 experiments completed in {time.time()-t_start:.1f}s")

# ═══════════════════════════════════════════════════════════════════════
# STEP 5: SAVE EXPERIMENT BENCHMARK RESULTS
# ═══════════════════════════════════════════════════════════════════════
df_res = pd.DataFrame(results)

# Rank with realistic constrained objective: Maximize Recall subject to Precision >= 0.50 (or 0.65)
# First sort purely by Recall descending
df_res_sorted = df_res.sort_values(by=["Recall", "Precision", "10-CV Recall"], ascending=[False, False, False])
csv_all = os.path.join(OUTPUT_DIR, "experiment_results_no_gpa.csv")
df_res_sorted.to_csv(csv_all, index=False)
print(f"\nSaved all 48 experiment results: {csv_all}")

# Find best per algorithm under constrained objective: Precision >= 0.50
best_per_algo = []
for m_name in ["RF", "DT", "LR", "SVM"]:
    sub = df_res[df_res["Model"] == m_name]
    # Filter realistic precision >= 0.50 if available, else best F1
    sub_filtered = sub[sub["Precision"] >= 0.50]
    if len(sub_filtered) > 0:
        best_row = sub_filtered.sort_values(by="Recall", ascending=False).iloc[0]
    else:
        best_row = sub.sort_values(by="F1", ascending=False).iloc[0]
    best_per_algo.append(best_row)

df_best = pd.DataFrame(best_per_algo)
csv_best = os.path.join(OUTPUT_DIR, "best_model_per_algorithm_no_gpa.csv")
df_best.to_csv(csv_best, index=False)
print(f"Saved best per algorithm: {csv_best}")

print("\n" + "=" * 72)
print("SUMMARY: BEST CONFIGURATION PER ALGORITHM (WITHOUT GPA)")
print("=" * 72)
for idx, r in df_best.iterrows():
    print(f"{r['Model']:<5s} ({r['Balance']} + {r['FS']}): Recall={r['Recall']:.3f}, Prec={r['Precision']:.3f}, F1={r['F1']:.3f}, AUC={r['AUC']:.3f}, Acc={r['Accuracy']:.3f}")

# Save bundle with champion RF
champ_row = df_best[df_best["Model"] == "RF"].iloc[0]
champ_key = f"{champ_row['Balance']}_{champ_row['FS']}_{champ_row['Model']}"
champ_data = trained_models[champ_key]

bundle_no_gpa = {
    "model": champ_data["model"],
    "feature_names": champ_data["features"],
    "fs_mask": champ_data["fs_mask"],
    "X_test": X_test[:, champ_data["fs_mask"]],
    "y_test": y_test,
    "best_params": champ_data["best_params"],
    "all_feature_names": feature_names
}

bundle_path = os.path.join(OUTPUT_DIR, "phase3_bundle_no_gpa.pkl")
with open(bundle_path, "wb") as f:
    pickle.dump(bundle_no_gpa, f)
print(f"\nSaved champion model bundle: {bundle_path}")

print("✅ PHASE 2 RETRAINING WITHOUT GPA COMPLETED!")

