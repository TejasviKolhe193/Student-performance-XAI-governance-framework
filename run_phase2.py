"""
Phase 2: 48-Experiment Model Benchmark Replicating Silva et al. (IEEE RITA 2025)
- Balancing: Unbalanced, RandomUnderSampler, SMOTE, SMOTEENN
- Feature Selection: ANOVA (k=19), Backward Selection (RFE k=19), Feature Importance (SelectFromModel k=19)
- Classifiers: Random Forest, Decision Tree, Logistic Regression, SVM
- Hyperparameters: max_depth=10, min_samples_leaf=5, min_samples_split=10 for trees
- Evaluation: Precision, Recall, F1, AUC, Accuracy, and 10-Fold CV Recall (MEDIA 10 CV)
- Selection Rule: 1st Recall -> 2nd Precision -> 3rd MEDIA 10 CV -> 4th other metrics
- Serializes Champion RF and Runner-Up DT for Phase 3 & 4.
"""

import os
import sys
import io
import time
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_selection import SelectKBest, f_classif, RFE, SelectFromModel
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import (
    precision_score, recall_score, f1_score, roc_auc_score,
    accuracy_score, confusion_matrix
)
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE
from imblearn.combine import SMOTEENN

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace", line_buffering=True)

OUTPUT_DIR = "phase2_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 80)
print("PHASE 2: 48-EXPERIMENT BENCHMARK & REPLICATION")
print("=" * 80)

# Load Phase 1 Data
with open("phase1_outputs/phase1_data.pkl", "rb") as f:
    p1 = pickle.load(f)

X_train = p1["X_train"]
X_test = p1["X_test"]
y_train = p1["y_train"]
y_test = p1["y_test"]
feature_names = np.array(p1["feature_names"])

print(f"Loaded Phase 1 Data:")
print(f"  Training shape: {X_train.shape} (Class 0: {(y_train==0).sum()}, Class 1: {(y_train==1).sum()})")
print(f"  Test shape:     {X_test.shape} (Class 0: {(y_test==0).sum()}, Class 1: {(y_test==1).sum()})")

# 1. Define balancing strategies
balancing_methods = {
    "Unbalanced": None,
    "UnderSampling": RandomUnderSampler(random_state=42),
    "SMOTE": SMOTE(random_state=42),
    "SMOTEENN": SMOTEENN(random_state=42),
}

# 2. Pre-generate balanced datasets
balanced_data = {}
print("\nPreparing Balanced Training Sets:")
for bal_name, sampler in balancing_methods.items():
    t0 = time.time()
    if sampler is None:
        X_bal, y_bal = X_train, y_train
    else:
        X_bal, y_bal = sampler.fit_resample(X_train, y_train)
    balanced_data[bal_name] = (X_bal, y_bal)
    c0 = (y_bal == 0).sum()
    c1 = (y_bal == 1).sum()
    print(f"  {bal_name:<15s}: {len(y_bal):>6d} samples (Class 0: {c0:>5d}, Class 1: {c1:>5d}) in {time.time()-t0:.2f}s")

# 3. Define Feature Selectors (k=19 matching Silva et al. Table V)
K_FEATS = 19

def fit_feature_selectors(X_b, y_b):
    selectors = {}
    
    # ANOVA
    anova = SelectKBest(f_classif, k=min(K_FEATS, X_b.shape[1]))
    anova.fit(X_b, y_b)
    selectors["ANOVA"] = anova.get_support()
    
    # Backward Selection (RFE)
    rfe_estimator = DecisionTreeClassifier(max_depth=10, min_samples_leaf=5, min_samples_split=10, random_state=42)
    rfe = RFE(estimator=rfe_estimator, n_features_to_select=min(K_FEATS, X_b.shape[1]), step=1)
    rfe.fit(X_b, y_b)
    selectors["Backward Selection"] = rfe.get_support()
    
    # Feature Importance (Embedded RF)
    rf_embed = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1)
    rf_embed.fit(X_b, y_b)
    importances = rf_embed.feature_importances_
    top_indices = np.argsort(importances)[::-1][:min(K_FEATS, X_b.shape[1])]
    mask_fi = np.zeros(X_b.shape[1], dtype=bool)
    mask_fi[top_indices] = True
    selectors["Feature Importance"] = mask_fi
    
    return selectors

# 4. Define Classifier Factories
def get_classifier(model_name):
    if model_name == "RF":
        return RandomForestClassifier(
            n_estimators=100, max_depth=10, min_samples_leaf=5, min_samples_split=10,
            random_state=42, n_jobs=-1
        )
    elif model_name == "DT":
        return DecisionTreeClassifier(
            max_depth=10, min_samples_leaf=5, min_samples_split=10,
            random_state=42
        )
    elif model_name == "LR":
        return LogisticRegression(max_iter=1000, random_state=42)
    elif model_name == "SVM":
        return CalibratedClassifierCV(
            LinearSVC(random_state=42, max_iter=2000, dual=False)
        )
    raise ValueError(f"Unknown model: {model_name}")

models = ["RF", "DT", "LR", "SVM"]
fs_names = ["Backward Selection", "ANOVA", "Feature Importance"]

results = []
trained_models = {}

print("\nRunning 48 Benchmarking Experiments...")
exp_count = 0
total_exps = len(balancing_methods) * len(fs_names) * len(models)

for bal_name, (X_b, y_b) in balanced_data.items():
    print(f"\n--- Balancing: {bal_name} ---")
    fs_masks = fit_feature_selectors(X_b, y_b)
    
    for fs_name in fs_names:
        mask = fs_masks[fs_name]
        X_train_sub = X_b[:, mask]
        X_test_sub = X_test[:, mask]
        sub_feature_names = feature_names[mask].tolist()
        
        for model_name in models:
            exp_count += 1
            t_start = time.time()
            clf = get_classifier(model_name)
            
            # Train model
            clf.fit(X_train_sub, y_b)
            
            # Test predictions
            y_pred = clf.predict(X_test_sub)
            if hasattr(clf, "predict_proba"):
                y_prob = clf.predict_proba(X_test_sub)[:, 1]
            else:
                y_prob = y_pred
                
            prec = precision_score(y_test, y_pred, zero_division=0)
            rec = recall_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)
            acc = accuracy_score(y_test, y_pred)
            try:
                auc = roc_auc_score(y_test, y_prob)
            except Exception:
                auc = 0.5
                
            # 10-Fold CV Recall on balanced training set
            cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
            cv_scores = cross_val_score(clf, X_train_sub, y_b, cv=cv, scoring="recall", n_jobs=-1)
            mean_cv = np.mean(cv_scores)
            
            elapsed = time.time() - t_start
            
            key = f"{model_name}_{bal_name}_{fs_name}"
            trained_models[key] = {
                "model": clf,
                "mask": mask,
                "feature_names": sub_feature_names,
                "bal_name": bal_name,
                "fs_name": fs_name,
                "model_name": model_name,
                "metrics": {
                    "Recall": rec, "Precision": prec, "F1": f1,
                    "AUC": auc, "Accuracy": acc, "MEAN_10_CV": mean_cv
                }
            }
            
            results.append({
                "Model": model_name,
                "Balancing": bal_name,
                "Feature_Selection": fs_name,
                "Recall": round(rec, 4),
                "Precision": round(prec, 4),
                "F1_score": round(f1, 4),
                "AUC": round(auc, 4),
                "Accuracy": round(acc, 4),
                "MEAN_10_CV": round(mean_cv, 4),
                "Elapsed_s": round(elapsed, 2),
                "Key": key
            })
            
            print(f"[{exp_count:>2d}/{total_exps}] {model_name:<3s} | {bal_name:<14s} | {fs_name:<18s} -> "
                  f"Recall: {rec:.4f}, Prec: {prec:.4f}, F1: {f1:.4f}, AUC: {auc:.4f}, 10CV: {mean_cv:.4f} ({elapsed:.1f}s)")

# Convert to DataFrame
df_results = pd.DataFrame(results)

# Selection Rule from Section IV-C of Silva et al.:
# 1st highest Recall, 2nd highest Precision, 3rd highest MEDIA 10 CV, 4th other metrics
df_sorted = df_results.sort_values(
    by=["Recall", "Precision", "MEAN_10_CV", "F1_score", "AUC", "Accuracy"],
    ascending=[False, False, False, False, False, False]
).reset_index(drop=True)

df_sorted["Rank"] = df_sorted.index + 1

# Save full results
df_sorted.to_csv(os.path.join(OUTPUT_DIR, "phase2_benchmark_results.csv"), index=False)
print(f"\nSaved all 48 results to {OUTPUT_DIR}/phase2_benchmark_results.csv")

# Extract Top 5 Models
top_5 = df_sorted.head(5).copy()
top_5.to_csv(os.path.join(OUTPUT_DIR, "top_5_models.csv"), index=False)

print("\n" + "=" * 80)
print("TOP 5 MODELS (Matching Silva et al. Table IV Format):")
print("=" * 80)
cols_show = ["Rank", "Model", "Balancing", "Feature_Selection", "Recall", "Precision", "F1_score", "Accuracy", "AUC", "MEAN_10_CV"]
print(top_5[cols_show].to_string(index=False))

# Best Model Per Algorithm
best_per_algo = df_sorted.groupby("Model").first().reset_index()
best_per_algo = best_per_algo.sort_values(by="Recall", ascending=False)
best_per_algo.to_csv(os.path.join(OUTPUT_DIR, "best_model_per_algorithm.csv"), index=False)
print("\nBEST MODEL PER ALGORITHM:")
print(best_per_algo[cols_show].to_string(index=False))

# Champion selection:
champion_key = top_5.iloc[0]["Key"]
champion_bundle = trained_models[champion_key]

# 2nd best Decision Tree surrogate:
dt_candidates = df_sorted[df_sorted["Model"] == "DT"]
second_best_dt_key = dt_candidates.iloc[0]["Key"]
dt_bundle = trained_models[second_best_dt_key]

print("\n" + "=" * 80)
print(f"CHAMPION MODEL SELECTED: {champion_key}")
print(f"  Recall:    {champion_bundle['metrics']['Recall']:.4f} (Base paper champion RF + SMOTEENN + Backward Recall: 0.854)")
print(f"  Precision: {champion_bundle['metrics']['Precision']:.4f} (Base paper: 0.847)")
print(f"  Accuracy:  {champion_bundle['metrics']['Accuracy']:.4f} (Base paper: 0.852)")
print(f"  AUC:       {champion_bundle['metrics']['AUC']:.4f} (Base paper: 0.854)")
print(f"  10-CV:     {champion_bundle['metrics']['MEAN_10_CV']:.4f} (Base paper: 0.870)")

print(f"\nSECOND-BEST TREE SURROGATE (DT): {second_best_dt_key}")
print(f"  Recall:    {dt_bundle['metrics']['Recall']:.4f} (Base paper DT + SMOTEENN + Backward Recall: 0.818)")
print(f"  Precision: {dt_bundle['metrics']['Precision']:.4f} (Base paper: 0.810)")
print("=" * 80)

# Save Bundle for Phase 3 and Phase 4
phase3_input_bundle = {
    "champion_rf": champion_bundle["model"],
    "champion_mask": champion_bundle["mask"],
    "champion_features": champion_bundle["feature_names"],
    "champion_metrics": champion_bundle["metrics"],
    "champion_key": champion_key,
    
    "surrogate_dt": dt_bundle["model"],
    "surrogate_mask": dt_bundle["mask"],
    "surrogate_features": dt_bundle["feature_names"],
    "surrogate_metrics": dt_bundle["metrics"],
    "surrogate_key": second_best_dt_key,
    
    "X_train": X_train,
    "X_test": X_test,
    "y_train": y_train,
    "y_test": y_test,
    "all_feature_names": feature_names.tolist(),
}

with open(os.path.join(OUTPUT_DIR, "champion_model_bundle.pkl"), "wb") as f:
    pickle.dump(phase3_input_bundle, f)

# Also save into phase3_bundle.pkl for downstream compatibility
with open("phase3_bundle.pkl", "wb") as f:
    pickle.dump({
        "model": champion_bundle["model"],
        "feature_names": champion_bundle["feature_names"],
        "X_test": X_test[:, champion_bundle["mask"]],
        "y_test": y_test,
        "dt_model": dt_bundle["model"],
        "dt_feature_names": dt_bundle["feature_names"],
        "dt_X_test": X_test[:, dt_bundle["mask"]],
    }, f)

print(f"\nSaved phase2_outputs/champion_model_bundle.pkl and phase3_bundle.pkl successfully!")
print("PHASE 2 COMPLETE!")

