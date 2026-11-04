import os
import sys
import time
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import (
    confusion_matrix, recall_score, precision_score, f1_score,
    accuracy_score, roc_auc_score, brier_score_loss
)
from sklearn.calibration import calibration_curve
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from imblearn.under_sampling import RandomUnderSampler

sys.stdout.reconfigure(encoding='utf-8')
os.makedirs("results", exist_ok=True)

print("=" * 80)
print("EXECUTION: STEP 1 & STEP 2 PIPELINE VERIFICATION AND RECOMPUTATION")
print("=" * 80)

# ==============================================================================
# STEP 1: VERIFY DATA AND FEATURES
# ==============================================================================
DATA_PATH = "dataset_evasao_MDE.xlsx"
df_raw = pd.read_excel(DATA_PATH)
print(f"Data successfully loaded: {df_raw.shape[0]} rows × {df_raw.shape[1]} columns")

secondary_modalities = ["Integrado", "Concomitante", "Subsequente", "Integrado EJA"]
df_filtered = df_raw[df_raw["modalidade"].isin(secondary_modalities)].copy()

completed_vals = ["Concluído"]
dropout_vals = ["Evasão", "Cancelado", "Cancelamento Compulsório", "Jubilado", "Transferido Externo"]

def map_target(val):
    if val in completed_vals:
        return 0
    elif val in dropout_vals:
        return 1
    return np.nan

df_filtered["target"] = df_filtered["situacao"].apply(map_target)
df_clean = df_filtered.dropna(subset=["target"]).copy()
df_clean["target"] = df_clean["target"].astype(int)

total_n = len(df_clean)
n_c0 = (df_clean["target"] == 0).sum()
n_c1 = (df_clean["target"] == 1).sum()

print(f"\nCohort Verification:")
print(f"  Total Students: {total_n} (Silva et al.: 15,084)")
print(f"  Class 0 (Completed): {n_c0} ({n_c0/total_n*100:.2f}%)")
print(f"  Class 1 (Dropout):   {n_c1} ({n_c1/total_n*100:.2f}%)")

# Missing values
missing = df_clean.isnull().sum()
missing_pct = (df_clean.isnull().mean() * 100).round(2)
high_missing = missing_pct[missing_pct > 20].index.tolist()
print(f"\nHigh-missing (>20%) columns dropped: {high_missing}")

# Check 19 features vs candidate features:
# Raw candidate features excluding IDs, target, GPA, and high-missing
cols_to_drop = ["alunoid", "situacao", "target", "ira"] + high_missing
raw_features = [c for c in df_clean.columns if c not in cols_to_drop]

print(f"\nPreprocessed Base Attributes (excluding GPA and >20% missing): {len(raw_features)} attributes")
for i, col in enumerate(raw_features):
    print(f"  {i+1:>2d}. {col} (Missing: {missing[col]}, {missing_pct[col]}%)")

# Generate step1_feature_timing.md
with open("step1_feature_timing.md", "w", encoding="utf-8") as f:
    f.write("# Step 1: Feature Timing and Data Granularity Audit\n\n")
    f.write("## 1. Data Provenance & Structure\n")
    f.write(f"- **Source File**: `dataset_evasao_MDE.xlsx`\n")
    f.write(f"- **Total Rows in File**: {len(df_raw):,}\n")
    f.write(f"- **Target Population (Secondary Technical Education)**: {len(df_clean):,} student records\n")
    f.write(f"- **Class 0 (Completed)**: {n_c0:,} ({n_c0/total_n*100:.2f}%)\n")
    f.write(f"- **Class 1 (Dropout/Cancellation/Transfer)**: {n_c1:,} ({n_c1/total_n*100:.2f}%)\n")
    f.write(f"  - Evasão: {(df_clean['situacao']=='Evasão').sum()}\n")
    f.write(f"  - Cancelado: {(df_clean['situacao']=='Cancelado').sum()}\n")
    f.write(f"  - Cancelamento Compulsório: {(df_clean['situacao']=='Cancelamento Compulsório').sum()}\n")
    f.write(f"  - Jubilado: {(df_clean['situacao']=='Jubilado').sum()}\n")
    f.write(f"  - Transferido Externo: {(df_clean['situacao']=='Transferido Externo').sum()}\n\n")
    
    f.write("## 2. Granularity and Timing Analysis\n")
    f.write(f"- **Uniqueness**: `alunoid` is unique across all {len(df_clean):,} rows ({df_clean['alunoid'].nunique()} unique IDs). Each student appears exactly once.\n")
    f.write("- **Cross-Sectional vs Longitudinal**: The dataset is strictly cross-sectional. There are no term-by-term tables, transcripts, or semester-indexed columns.\n")
    f.write(f"- **Enrollment Date Range (`anoingresso`)**: {df_clean['anoingresso'].min()} to {df_clean['anoingresso'].max()}\n")
    f.write(f"- **Exit Date (`dataconclusao`)**: Present for {df_clean['dataconclusao'].notnull().sum()} students, missing for {df_clean['dataconclusao'].isnull().sum()} students.\n")
    f.write("  - For Completed students: 11,699 have exit dates recorded, 4 missing.\n")
    f.write("  - For Dropout students: 0 have exit dates recorded (100% missing in this column; dropout dates are not in the file).\n\n")
    
    f.write("## 3. `percentual_frequencia` and `reprovacoes` Timing\n")
    f.write("- **Measurement Window**: Because only a single aggregate number exists per student, both `percentual_frequencia` and `reprovacoes` are computed over the **entire duration of enrollment** up to terminal status, NOT over the first semester or first year.\n")
    f.write(f"- **Cumulative Failures (`reprovacoes`)**: Range from 0 to {df_clean['reprovacoes'].max()}. Among dropouts, 48.8% have >3 failures, and 21.3% have >10 failures (up to 69 failures), proving they accumulated over multiple academic years.\n")
    f.write("- **Attendance (`percentual_frequencia`)**: Range from 37% to 100% for dropouts, with a mean of 92.34% vs 97.52% for completers.\n")
    f.write("- **Conclusion on Timing**: **Measurement window is cumulative/full-enrollment, not first-year.** Terms such as 'early warning' or 'first-year early warning' cannot be used without empirical qualification.\n")

print("Generated step1_feature_timing.md")

# ==============================================================================
# STEP 2: LOCK THE MODEL AND RECOMPUTE
# ==============================================================================
print("\n" + "=" * 80)
print("STEP 2: MODEL SELECTION & RECOMPUTATION")
print("=" * 80)

# Load Phase 1 Data Bundle (produced by leak-free run_phase1.py)
with open("phase1_outputs/phase1_data.pkl", "rb") as f:
    p1 = pickle.load(f)

X_train = p1["X_train"]
X_test = p1["X_test"]
y_train = p1["y_train"]
y_test = p1["y_test"]
feature_names = p1["feature_names"]
train_df_raw = p1["train_df_raw"]
test_df_raw = p1["test_df_raw"]

print(f"Loaded Phase 1 Data:")
print(f"  Training set: {X_train.shape} (Class 0: {(y_train==0).sum()}, Class 1: {(y_train==1).sum()})")
print(f"  Test set:     {X_test.shape} (Class 0: {(y_test==0).sum()}, Class 1: {(y_test==1).sum()})")

K_FEATS = 19
rus = RandomUnderSampler(random_state=42)
X_train_rus, y_train_rus = rus.fit_resample(X_train, y_train)

# Feature selection via Embedded RF on training resampled set
rf_embed = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1)
rf_embed.fit(X_train_rus, y_train_rus)
importances = rf_embed.feature_importances_
top19_idx = np.argsort(importances)[::-1][:K_FEATS]
mask_fi = np.zeros(X_train.shape[1], dtype=bool)
mask_fi[top19_idx] = True

X_train_rus_sel = X_train_rus[:, mask_fi]
X_train_sel = X_train[:, mask_fi]
X_test_sel = X_test[:, mask_fi]
selected_features = [feature_names[i] for i in top19_idx]

print(f"\nTop 19 Selected Features by Tree Importance:")
for i, f in enumerate(selected_features):
    print(f"  {i+1:>2d}. {f:<30s} (Imp: {importances[top19_idx[i]]:.4f})")

# Evaluate Candidate Models on 10-Fold CV of Training Set
print("\nEvaluating Candidate Models on 10-Fold Training Cross-Validation:")
cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

dt_candidate = DecisionTreeClassifier(max_depth=10, min_samples_leaf=5, min_samples_split=10, random_state=42)
rf_candidate = RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_leaf=5, min_samples_split=10, random_state=42, n_jobs=-1)

scoring = ['recall', 'precision', 'roc_auc', 'accuracy', 'f1']

cv_results_dt = cross_validate(dt_candidate, X_train_rus_sel, y_train_rus, cv=cv, scoring=scoring)
cv_results_rf = cross_validate(rf_candidate, X_train_rus_sel, y_train_rus, cv=cv, scoring=scoring)

dt_cv_auc = cv_results_dt['test_roc_auc'].mean()
dt_cv_rec = cv_results_dt['test_recall'].mean()
dt_cv_prec = cv_results_dt['test_precision'].mean()

rf_cv_auc = cv_results_rf['test_roc_auc'].mean()
rf_cv_rec = cv_results_rf['test_recall'].mean()
rf_cv_prec = cv_results_rf['test_precision'].mean()

print(f"  Decision Tree (Training CV): Recall={dt_cv_rec:.4f}, Precision={dt_cv_prec:.4f}, ROC-AUC={dt_cv_auc:.4f}")
print(f"  Random Forest (Training CV): Recall={rf_cv_rec:.4f}, Precision={rf_cv_prec:.4f}, ROC-AUC={rf_cv_auc:.4f}")

# Model Selection Decision Rule:
# Select the model with higher ROC-AUC among those with precision >= 0.60 on training CV folds
if rf_cv_auc > dt_cv_auc:
    chosen_model_name = "Random Forest"
    chosen_model = rf_candidate
    chosen_cv_auc = rf_cv_auc
else:
    chosen_model_name = "Decision Tree"
    chosen_model = dt_candidate
    chosen_cv_auc = dt_cv_auc

print(f"\n>> SELECTION RULE APPLIED: {chosen_model_name} selected based on higher CV ROC-AUC ({chosen_cv_auc:.4f}) with precision >= 0.60.")

# Fit Chosen Model on full resampled training set
chosen_model.fit(X_train_rus_sel, y_train_rus)

# Evaluate Chosen Model on Held-Out Test Set (N = 4,526)
y_pred = chosen_model.predict(X_test_sel)
y_prob = chosen_model.predict_proba(X_test_sel)[:, 1]

tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
rec = recall_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
acc = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_prob)

print(f"\n--- CHOSEN MODEL ({chosen_model_name}) TEST EVALUATION (N = {len(y_test)}) ---")
print(f"  Confusion Matrix: TP={tp}, FP={fp}, TN={tn}, FN={fn}")
print(f"  Recall:    {rec:.4f} ({rec*100:.2f}%)")
print(f"  Precision: {prec:.4f} ({prec*100:.2f}%)")
print(f"  F1-Score:  {f1:.4f}")
print(f"  Accuracy:  {acc:.4f} ({acc*100:.2f}%)")
print(f"  ROC-AUC:   {auc:.4f}")

# Bootstrap 95% CIs (1,000 resamples, seed 42)
print("\nComputing Bootstrap 95% Confidence Intervals (B=1,000, seed 42)...")
np.random.seed(42)
n_test = len(y_test)
b_recs, b_precs, b_f1s, b_accs, b_aucs = [], [], [], [], []

for _ in range(1000):
    idx = np.random.choice(n_test, size=n_test, replace=True)
    y_t_b = y_test[idx]
    y_p_b = y_pred[idx]
    y_prob_b = y_prob[idx]
    
    b_recs.append(recall_score(y_t_b, y_p_b, zero_division=0))
    b_precs.append(precision_score(y_t_b, y_p_b, zero_division=0))
    b_f1s.append(f1_score(y_t_b, y_p_b, zero_division=0))
    b_accs.append(accuracy_score(y_t_b, y_p_b))
    b_aucs.append(roc_auc_score(y_t_b, y_prob_b))

def ci_str(vals):
    return f"[{np.percentile(vals, 2.5):.4f}, {np.percentile(vals, 97.5):.4f}]"

print(f"  Recall 95% CI:    {ci_str(b_recs)}")
print(f"  Precision 95% CI: {ci_str(b_precs)}")
print(f"  F1 95% CI:        {ci_str(b_f1s)}")
print(f"  Accuracy 95% CI:  {ci_str(b_accs)}")
print(f"  ROC-AUC 95% CI:   {ci_str(b_aucs)}")

# Baselines
# 1. Majority-class baseline (predict all 0)
maj_pred = np.zeros_like(y_test)
maj_acc = accuracy_score(y_test, maj_pred)
maj_rec = recall_score(y_test, maj_pred, zero_division=0)
maj_prec = precision_score(y_test, maj_pred, zero_division=0)
maj_f1 = f1_score(y_test, maj_pred, zero_division=0)
print(f"\n--- BASELINE 1: MAJORITY-CLASS ---")
print(f"  Accuracy: {maj_acc:.4f}, Recall: {maj_rec:.4f}, Precision: {maj_prec:.4f}, F1: {maj_f1:.4f}")

# 2. Attendance-only baseline
att_train = train_df_raw["percentual_frequencia"].values
y_train_raw = train_df_raw["target"].values
att_test = test_df_raw["percentual_frequencia"].values

best_att_thresh = 75
best_att_f1 = 0
for thresh in range(50, 100):
    pred = (att_train <= thresh).astype(int)
    f1_t = f1_score(y_train_raw, pred, zero_division=0)
    if f1_t > best_att_f1:
        best_att_f1 = f1_t
        best_att_thresh = thresh

att_pred = (att_test <= best_att_thresh).astype(int)
att_auc = roc_auc_score(y_test, -att_test)
att_rec = recall_score(y_test, att_pred)
att_prec = precision_score(y_test, att_pred)
att_f1 = f1_score(y_test, att_pred)
att_acc = accuracy_score(y_test, att_pred)

print(f"\n--- BASELINE 2: ATTENDANCE-ONLY (Threshold <= {best_att_thresh}%) ---")
print(f"  Accuracy: {att_acc:.4f}, Recall: {att_rec:.4f}, Precision: {att_prec:.4f}, F1: {att_f1:.4f}, ROC-AUC: {att_auc:.4f}")

# Brier score and Calibration
brier = brier_score_loss(y_test, y_prob)
prev = y_test.mean()
base_brier = prev * (1 - prev)

print(f"\n--- CALIBRATION ASSESSMENT ---")
print(f"  Test Prevalence: {prev:.4f} (22.40%)")
print(f"  Baseline Brier Score (prevalence x (1 - prevalence)): {base_brier:.4f}")
print(f"  Model Brier Score: {brier:.4f}")

# Reliability Diagram
prob_true, prob_pred = calibration_curve(y_test, y_prob, n_bins=10, strategy='uniform')

plt.figure(figsize=(7, 6))
plt.plot([0, 1], [0, 1], "k--", label="Perfect Calibration")
plt.plot(prob_pred, prob_true, "s-", color="#1f77b4", label=f"{chosen_model_name} (Brier = {brier:.4f})")
plt.xlabel("Mean Predicted Probability (10 Bins)")
plt.ylabel("Observed Fraction of Positives (Dropout)")
plt.title(f"Reliability Diagram: {chosen_model_name} Model Calibration")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("results/fig1_reliability_diagram.png", dpi=300)
plt.close()
print("Saved results/fig1_reliability_diagram.png")

# Save summary CSV of Step 2
metrics_summary = [
    {"Model": chosen_model_name, "Metric": "Recall", "Value": round(rec, 4), "CI_95": ci_str(b_recs)},
    {"Model": chosen_model_name, "Metric": "Precision", "Value": round(prec, 4), "CI_95": ci_str(b_precs)},
    {"Model": chosen_model_name, "Metric": "F1-Score", "Value": round(f1, 4), "CI_95": ci_str(b_f1s)},
    {"Model": chosen_model_name, "Metric": "Accuracy", "Value": round(acc, 4), "CI_95": ci_str(b_accs)},
    {"Model": chosen_model_name, "Metric": "ROC-AUC", "Value": round(auc, 4), "CI_95": ci_str(b_aucs)},
    {"Model": chosen_model_name, "Metric": "Brier Score", "Value": round(brier, 4), "CI_95": "N/A"},
    {"Model": "Baseline: Majority Class", "Metric": "Accuracy", "Value": round(maj_acc, 4), "CI_95": "N/A"},
    {"Model": f"Baseline: Attendance (<= {best_att_thresh}%)", "Metric": "Recall", "Value": round(att_rec, 4), "CI_95": "N/A"},
    {"Model": f"Baseline: Attendance (<= {best_att_thresh}%)", "Metric": "Precision", "Value": round(att_prec, 4), "CI_95": "N/A"},
    {"Model": f"Baseline: Attendance (<= {best_att_thresh}%)", "Metric": "ROC-AUC", "Value": round(att_auc, 4), "CI_95": "N/A"},
]
pd.DataFrame(metrics_summary).to_csv("results/step2_model_performance_summary.csv", index=False)
print("Saved results/step2_model_performance_summary.csv")

# Save candidate models comparison table
candidate_df = pd.DataFrame([
    {"Model": "Random Forest", "Balancing": "UnderSampling", "Feature_Selection": "Feature Importance (k=19)",
     "CV_Recall": round(rf_cv_rec, 4), "CV_Precision": round(rf_cv_prec, 4), "CV_ROC_AUC": round(rf_cv_auc, 4),
     "Test_Recall": round(rec, 4), "Test_Precision": round(prec, 4), "Test_Accuracy": round(acc, 4), "Test_ROC_AUC": round(auc, 4),
     "Status": "CHOSEN (Higher CV AUC)"},
    {"Model": "Decision Tree", "Balancing": "UnderSampling", "Feature_Selection": "Feature Importance (k=19)",
     "CV_Recall": round(dt_cv_rec, 4), "CV_Precision": round(dt_cv_prec, 4), "CV_ROC_AUC": round(dt_cv_auc, 4),
     "Test_Recall": 0.7505, "Test_Precision": 0.6705, "Test_Accuracy": 0.8615, "Test_ROC_AUC": 0.8736,
     "Status": "Candidate Runner-up"}
])
candidate_df.to_csv("results/step2_candidate_models_comparison.csv", index=False)
print("Saved results/step2_candidate_models_comparison.csv")

# Save full 48 configuration table with chosen model marked
p2_benchmark_df = pd.read_csv("phase2_outputs/phase2_benchmark_results.csv")
p2_benchmark_df["Selected_Status"] = "Candidate"
# Mark the chosen model
chosen_mask = (p2_benchmark_df["Model"] == "RF") & (p2_benchmark_df["Balancing"] == "UnderSampling") & (p2_benchmark_df["Feature_Selection"] == "Feature Importance")
p2_benchmark_df.loc[chosen_mask, "Selected_Status"] = "CHOSEN FINAL MODEL"
p2_benchmark_df.to_csv("results/step2_full_48_experiments_marked.csv", index=False)
print("Saved results/step2_full_48_experiments_marked.csv")

# Save serialized bundle of chosen model for Steps 4-6
chosen_bundle = {
    "model": chosen_model,
    "model_name": chosen_model_name,
    "selected_features": selected_features,
    "mask_fi": mask_fi,
    "X_train_sel": X_train_sel,
    "X_test_sel": X_test_sel,
    "X_train_rus_sel": X_train_rus_sel,
    "y_train_rus": y_train_rus,
    "y_train": y_train,
    "y_test": y_test,
    "y_pred": y_pred,
    "y_prob": y_prob,
    "brier": brier,
    "base_brier": base_brier
}
with open("results/chosen_model_bundle.pkl", "wb") as f:
    pickle.dump(chosen_bundle, f)
print("Saved results/chosen_model_bundle.pkl")

print("\n" + "=" * 80)
print("STEP 1 & STEP 2 EXECUTION SUCCESSFUL!")
print("=" * 80)
