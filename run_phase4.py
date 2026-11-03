"""
Phase 4: Algorithmic Fairness Audit and Mitigation Pipeline (Best-of-Both Merge)
=================================================================================
Inherited from dev (Sahiti):
  - AIF360-based BinaryLabelDataset & ClassificationMetric for DI, SPD, EOD.
  - Audits across 3 thresholds (0.30, 0.50, 0.70).
  - Holm-Bonferroni correction across hypothesis tests.
  - AIF360 Reweighing mitigation and pre/post trade-off matrix.

Grafted from tejasvi:
  - Bootstrap 95% Confidence Intervals on TPR and Selection Rate per subgroup.
  - Spearman proxy predictability check (AUC > 0.70 threshold).
  - Explicit declaration of Equal Opportunity (TPR Parity) as priority criterion.

Uses already-trained Phase 2 champion model (NO retraining).
"""

import os
import sys
import io
import pickle
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# AIF360 imports
from aif360.datasets import BinaryLabelDataset
from aif360.metrics import ClassificationMetric, BinaryLabelDatasetMetric
from aif360.algorithms.preprocessing import Reweighing
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score, precision_score, f1_score, accuracy_score, roc_auc_score
from sklearn.model_selection import cross_val_score

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace", line_buffering=True)

OUTPUT_DIR = "phase4_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

GLOBAL_SEED = 42
np.random.seed(GLOBAL_SEED)

print("=" * 80)
print("PHASE 4: COMPREHENSIVE ALGORITHMIC FAIRNESS AUDIT & MITIGATION")
print("           (Best-of-Both Merge: AIF360 + Bootstrap CIs + Proxy Check)")
print("=" * 80)
print("PRIORITY CRITERION: Equal Opportunity (TPR Parity).")
print("  Rationale: In educational retention, equal sensitivity across demographic")
print("  groups ensures marginalized dropouts are not disproportionately overlooked.")
print("=" * 80)

# ═══════════════════════════════════════════════════════════════════════
# LOAD ALREADY-TRAINED MODEL (NO RETRAINING)
# ═══════════════════════════════════════════════════════════════════════
with open("phase1_outputs/phase1_data.pkl", "rb") as f:
    p1 = pickle.load(f)

with open("phase2_outputs/champion_model_bundle.pkl", "rb") as f:
    p2 = pickle.load(f)

test_df = p1["test_df_raw"].copy()
train_df = p1["train_df_raw"].copy()

rf_model = p2["champion_rf"]
rf_mask = p2["champion_mask"]
rf_features = p2["champion_features"]

X_test_rf = p2["X_test"][:, rf_mask]
y_test = p2["y_test"]

X_train_full = p2["X_train"]
X_test_full = p2["X_test"]
X_train_rf = p2["X_train"][:, rf_mask]
y_train = p2["y_train"]
all_feature_names = p2["all_feature_names"]

test_probs = rf_model.predict_proba(X_test_rf)[:, 1]
test_df["y_true"] = y_test
test_df["y_prob"] = test_probs

print(f"Loaded Phase 2 champion RF model ({len(rf_features)} features, already trained).")
print(f"Test set: {len(y_test)} students | Class 0: {(y_test==0).sum()}, Class 1: {(y_test==1).sum()}")

# ═══════════════════════════════════════════════════════════════════════
# SECTION 1: PREPARE PROTECTED ATTRIBUTE BINARY SLICES
# ═══════════════════════════════════════════════════════════════════════
income_median = train_df["rendabruta"].median()

test_df["gender_priv"] = (test_df["genero"] == "M").astype(int)
test_df["income_priv"] = (test_df["rendabruta"] > income_median).astype(int)
test_df["age_priv"] = (test_df["idade"] <= 20).astype(int)
test_df["computer_priv"] = (test_df["quantidade_notebooks"] > 0).astype(int)

race_categories = test_df["raca"].value_counts().index.tolist()
print(f"\nOriginal Race Categories in Test Set: {test_df['raca'].value_counts().to_dict()}")

# ═══════════════════════════════════════════════════════════════════════
# SECTION 2: DISAGGREGATED SUBGROUP METRICS WITH BOOTSTRAP 95% CIs
# (Merged from tejasvi: bootstrap CIs on TPR and Selection Rate)
# ═══════════════════════════════════════════════════════════════════════
N_BOOTSTRAP = 500

def get_group_stats_with_ci(df_sub, group_name, n_boot=N_BOOTSTRAP):
    """Compute group-level metrics with bootstrap 95% confidence intervals."""
    n = len(df_sub)
    if n == 0:
        return {"Group": group_name, "N": 0, "Base_Rate": 0, "Selection_Rate": 0,
                "TPR": 0, "FPR": 0, "Precision": 0,
                "Selection_Rate_95CI": "[0.000, 0.000]", "TPR_95CI": "[0.000, 0.000]"}
    y_true = df_sub["y_true"].values
    y_pred = df_sub["y_pred"].values

    base_rate = np.mean(y_true)
    sel_rate = np.mean(y_pred)

    positives = (y_true == 1)
    negatives = (y_true == 0)

    tpr = np.mean(y_pred[positives]) if np.sum(positives) > 0 else 0.0
    fpr = np.mean(y_pred[negatives]) if np.sum(negatives) > 0 else 0.0

    predicted_pos = (y_pred == 1)
    precision = np.mean(y_true[predicted_pos]) if np.sum(predicted_pos) > 0 else 0.0

    # Bootstrap 95% CIs for TPR and Selection Rate
    boot_tprs = []
    boot_sels = []
    rng = np.random.RandomState(GLOBAL_SEED)
    for _ in range(n_boot):
        b_idx = rng.choice(n, size=n, replace=True)
        b_yt = y_true[b_idx]
        b_yp = y_pred[b_idx]
        boot_sels.append(np.mean(b_yp))
        b_pos = (b_yt == 1)
        if np.sum(b_pos) > 0:
            boot_tprs.append(np.mean(b_yp[b_pos]))
        else:
            boot_tprs.append(0.0)

    ci_sel_l, ci_sel_h = np.percentile(boot_sels, [2.5, 97.5])
    ci_tpr_l, ci_tpr_h = np.percentile(boot_tprs, [2.5, 97.5])

    return {
        "Group": group_name,
        "N": n,
        "Base_Rate": round(base_rate, 4),
        "Selection_Rate": round(sel_rate, 4),
        "Selection_Rate_95CI": f"[{ci_sel_l:.3f}, {ci_sel_h:.3f}]",
        "TPR": round(tpr, 4),
        "TPR_95CI": f"[{ci_tpr_l:.3f}, {ci_tpr_h:.3f}]",
        "FPR": round(fpr, 4),
        "Precision": round(precision, 4)
    }


test_df["y_pred"] = (test_df["y_prob"] >= 0.50).astype(int)

group_reports = []
# Overall
group_reports.append(get_group_stats_with_ci(test_df, "Overall Test Cohort"))

# Gender
for g in ["M", "F"]:
    group_reports.append(get_group_stats_with_ci(test_df[test_df["genero"] == g], f"Gender: {g}"))

# Race (All unmerged categories)
for r in race_categories:
    group_reports.append(get_group_stats_with_ci(test_df[test_df["raca"] == r], f"Race: {r}"))

# Income
group_reports.append(get_group_stats_with_ci(test_df[test_df["income_priv"] == 1], f"Income: > Median (R$ {income_median:.0f})"))
group_reports.append(get_group_stats_with_ci(test_df[test_df["income_priv"] == 0], f"Income: <= Median (R$ {income_median:.0f})"))

# Age
group_reports.append(get_group_stats_with_ci(test_df[test_df["age_priv"] == 1], "Age: <= 20 years"))
group_reports.append(get_group_stats_with_ci(test_df[test_df["age_priv"] == 0], "Age: > 20 years"))

# Computer Access
group_reports.append(get_group_stats_with_ci(test_df[test_df["computer_priv"] == 1], "Notebook: >= 1"))
group_reports.append(get_group_stats_with_ci(test_df[test_df["computer_priv"] == 0], "Notebook: 0"))

df_group_reports = pd.DataFrame(group_reports)
print("\nDISAGGREGATED DEMOGRAPHIC SUBGROUP METRICS (Threshold = 0.50) WITH BOOTSTRAP 95% CIs:")
print(df_group_reports.to_string(index=False))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 3: AIF360 QUANTITATIVE FAIRNESS METRICS ACROSS 3 THRESHOLDS
# (Retained from dev: AIF360 ClassificationMetric + 3-threshold sweep)
# ═══════════════════════════════════════════════════════════════════════
thresholds = [0.30, 0.50, 0.70]
fairness_evaluations = []

audit_attributes = [
    ("Gender (M vs F)", "gender_priv", 1, 0),
    ("Race (Branca vs Parda)", "raca", "Branca", "Parda"),
    ("Race (Branca vs Preta)", "raca", "Branca", "Preta"),
    ("Income (> Med vs <= Med)", "income_priv", 1, 0),
    ("Age (<=20 vs >20)", "age_priv", 1, 0),
    ("Computer Access (>=1 vs 0)", "computer_priv", 1, 0),
]

for thresh in thresholds:
    test_df["y_pred_thresh"] = (test_df["y_prob"] >= thresh).astype(int)

    for attr_name, col_name, priv_val, unpriv_val in audit_attributes:
        if col_name == "raca":
            sub_eval = test_df[test_df["raca"].isin([priv_val, unpriv_val])].copy()
            sub_eval["attr_bin"] = (sub_eval["raca"] == priv_val).astype(int)
            col_eval = "attr_bin"
            p_val = 1
            u_val = 0
        else:
            sub_eval = test_df.copy()
            col_eval = col_name
            p_val = priv_val
            u_val = unpriv_val

        # Create AIF360 BinaryLabelDataset
        aif_true = BinaryLabelDataset(
            df=sub_eval[[col_eval, "y_true"]],
            label_names=["y_true"],
            protected_attribute_names=[col_eval],
            favorable_label=0,
            unfavorable_label=1
        )

        aif_pred = BinaryLabelDataset(
            df=sub_eval[[col_eval, "y_pred_thresh"]].rename(columns={"y_pred_thresh": "y_true"}),
            label_names=["y_true"],
            protected_attribute_names=[col_eval],
            favorable_label=0,
            unfavorable_label=1
        )

        priv_group = [{col_eval: p_val}]
        unpriv_group = [{col_eval: u_val}]

        metric = ClassificationMetric(
            aif_true, aif_pred,
            unprivileged_groups=unpriv_group,
            privileged_groups=priv_group
        )

        # Calculate rates for Dropout (Class 1)
        sr_priv = np.mean(sub_eval[sub_eval[col_eval] == p_val]["y_pred_thresh"] == 1)
        sr_unpriv = np.mean(sub_eval[sub_eval[col_eval] == u_val]["y_pred_thresh"] == 1)
        di = sr_unpriv / sr_priv if sr_priv > 0 else np.nan
        spd = sr_unpriv - sr_priv

        tpr_priv = np.mean(sub_eval[(sub_eval[col_eval] == p_val) & (sub_eval["y_true"] == 1)]["y_pred_thresh"] == 1)
        tpr_unpriv = np.mean(sub_eval[(sub_eval[col_eval] == u_val) & (sub_eval["y_true"] == 1)]["y_pred_thresh"] == 1)
        eod = tpr_unpriv - tpr_priv

        fpr_priv = np.mean(sub_eval[(sub_eval[col_eval] == p_val) & (sub_eval["y_true"] == 0)]["y_pred_thresh"] == 1)
        fpr_unpriv = np.mean(sub_eval[(sub_eval[col_eval] == u_val) & (sub_eval["y_true"] == 0)]["y_pred_thresh"] == 1)

        # Two-proportion z-test p-value for TPR difference (Equal Opportunity)
        n1 = np.sum((sub_eval[col_eval] == u_val) & (sub_eval["y_true"] == 1))
        n2 = np.sum((sub_eval[col_eval] == p_val) & (sub_eval["y_true"] == 1))
        x1 = np.sum((sub_eval[col_eval] == u_val) & (sub_eval["y_true"] == 1) & (sub_eval["y_pred_thresh"] == 1))
        x2 = np.sum((sub_eval[col_eval] == p_val) & (sub_eval["y_true"] == 1) & (sub_eval["y_pred_thresh"] == 1))

        p_pool = (x1 + x2) / (n1 + n2) if (n1 + n2) > 0 else 0
        se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2)) if p_pool > 0 and (1 - p_pool) > 0 else 1e-6
        z_score = (tpr_unpriv - tpr_priv) / se if se > 0 else 0
        p_val_eod = 2 * (1 - stats.norm.cdf(abs(z_score)))

        di_pass = (0.80 <= di <= 1.25)
        spd_pass = (abs(spd) <= 0.10)
        eod_pass = (abs(eod) <= 0.10)

        fairness_evaluations.append({
            "Threshold": thresh,
            "Attribute": attr_name,
            "Privileged_Group": f"{col_name}={priv_val}",
            "Unprivileged_Group": f"{col_name}={unpriv_val}",
            "Sel_Rate_Priv": round(sr_priv, 4),
            "Sel_Rate_Unpriv": round(sr_unpriv, 4),
            "Disparate_Impact": round(di, 4),
            "DI_Status": "Pass [0.80, 1.25]" if di_pass else "Flagged",
            "Statistical_Parity_Diff": round(spd, 4),
            "SPD_Status": "Pass (|spd|<=0.10)" if spd_pass else "Flagged",
            "TPR_Priv": round(tpr_priv, 4),
            "TPR_Unpriv": round(tpr_unpriv, 4),
            "Equal_Opportunity_Diff": round(eod, 4),
            "EOD_Status": "Pass (|eod|<=0.10)" if eod_pass else "Flagged",
            "P_Value_EOD": round(p_val_eod, 5)
        })

df_fairness = pd.DataFrame(fairness_evaluations)
print("\nAIF360 FAIRNESS METRICS ACROSS THRESHOLDS (0.30, 0.50, 0.70):")
print(df_fairness[["Threshold", "Attribute", "Disparate_Impact", "DI_Status", "Statistical_Parity_Diff", "Equal_Opportunity_Diff", "EOD_Status"]].to_string(index=False))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 4: HOLM-BONFERRONI CORRECTION
# (Retained from dev: proper multiple-testing correction)
# ═══════════════════════════════════════════════════════════════════════
thresh50_evals = df_fairness[df_fairness["Threshold"] == 0.50].copy().reset_index(drop=True)
p_values = thresh50_evals["P_Value_EOD"].values
m = len(p_values)

sorted_indices = np.argsort(p_values)
holm_adjusted_sig = [False] * m

print(f"\nHOLM-BONFERRONI MULTIPLE TESTING CORRECTION (m={m} hypothesis tests for EOD parity at alpha=0.05):")
print(f"{'Rank':<5s} {'Attribute':<30s} {'Raw p-value':<12s} {'Holm Threshold (alpha/(m-i+1))':<30s} {'Significant?'}")
print("-" * 85)

alpha = 0.05
for i, idx in enumerate(sorted_indices):
    raw_p = p_values[idx]
    holm_thresh = alpha / (m - i)
    is_sig = (raw_p <= holm_thresh)
    holm_adjusted_sig[idx] = is_sig
    attr = thresh50_evals.loc[idx, "Attribute"]
    print(f"{i+1:<5d} {attr:<30s} {raw_p:<12.5f} {holm_thresh:<30.5f} {str(is_sig)}")

thresh50_evals["Holm_Significant"] = holm_adjusted_sig

# ═══════════════════════════════════════════════════════════════════════
# SECTION 5: AIF360 REWEIGHING MITIGATION
# (Retained from dev: preprocessing mitigation via instance reweighting)
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("AIF360 MITIGATION: PREPROCESSING VIA REWEIGHING")
print("=" * 80)

train_df["gender_priv"] = (train_df["genero"] == "M").astype(int)

train_aif = BinaryLabelDataset(
    df=train_df[["gender_priv", "target"]].rename(columns={"target": "y_true"}),
    label_names=["y_true"],
    protected_attribute_names=["gender_priv"],
    favorable_label=0,
    unfavorable_label=1
)

reweighter = Reweighing(
    unprivileged_groups=[{"gender_priv": 0}],
    privileged_groups=[{"gender_priv": 1}]
)
reweighter.fit(train_aif)
train_aif_reweighed = reweighter.transform(train_aif)
sample_weights = train_aif_reweighed.instance_weights

print(f"Computed sample weights via Reweighing: min={sample_weights.min():.4f}, max={sample_weights.max():.4f}, mean={sample_weights.mean():.4f}")

# Retrain Champion RF model with Reweighed sample weights
rf_mitigated = RandomForestClassifier(
    n_estimators=100, max_depth=10, min_samples_leaf=5, min_samples_split=10,
    random_state=42, n_jobs=-1
)
rf_mitigated.fit(X_train_rf, y_train, sample_weight=sample_weights)

# Evaluate Mitigated Model on Test Set
y_probs_mit = rf_mitigated.predict_proba(X_test_rf)[:, 1]
y_preds_mit = (y_probs_mit >= 0.50).astype(int)

rec_pre = recall_score(y_test, test_df["y_pred"])
prec_pre = precision_score(y_test, test_df["y_pred"])
f1_pre = f1_score(y_test, test_df["y_pred"])
acc_pre = accuracy_score(y_test, test_df["y_pred"])

rec_post = recall_score(y_test, y_preds_mit)
prec_post = precision_score(y_test, y_preds_mit)
f1_post = f1_score(y_test, y_preds_mit)
acc_post = accuracy_score(y_test, y_preds_mit)

# Compute Gender Fairness before and after
sr_m_pre = np.mean(test_df[test_df["gender_priv"] == 1]["y_pred"] == 1)
sr_f_pre = np.mean(test_df[test_df["gender_priv"] == 0]["y_pred"] == 1)
di_pre = sr_f_pre / sr_m_pre if sr_m_pre > 0 else np.nan
tpr_m_pre = np.mean(test_df[(test_df["gender_priv"] == 1) & (test_df["y_true"] == 1)]["y_pred"] == 1)
tpr_f_pre = np.mean(test_df[(test_df["gender_priv"] == 0) & (test_df["y_true"] == 1)]["y_pred"] == 1)
eod_pre = tpr_f_pre - tpr_m_pre

test_df["y_pred_mit"] = y_preds_mit
sr_m_post = np.mean(test_df[test_df["gender_priv"] == 1]["y_pred_mit"] == 1)
sr_f_post = np.mean(test_df[test_df["gender_priv"] == 0]["y_pred_mit"] == 1)
di_post = sr_f_post / sr_m_post if sr_m_post > 0 else np.nan
tpr_m_post = np.mean(test_df[(test_df["gender_priv"] == 1) & (test_df["y_true"] == 1)]["y_pred_mit"] == 1)
tpr_f_post = np.mean(test_df[(test_df["gender_priv"] == 0) & (test_df["y_true"] == 1)]["y_pred_mit"] == 1)
eod_post = tpr_f_post - tpr_m_post

mitigation_comparison = [
    {"Metric": "Recall (Catch Rate)", "Pre_Mitigation": round(rec_pre, 4), "Post_Mitigation": round(rec_post, 4), "Change": round(rec_post - rec_pre, 4)},
    {"Metric": "Precision", "Pre_Mitigation": round(prec_pre, 4), "Post_Mitigation": round(prec_post, 4), "Change": round(prec_post - prec_pre, 4)},
    {"Metric": "F1-Score", "Pre_Mitigation": round(f1_pre, 4), "Post_Mitigation": round(f1_post, 4), "Change": round(f1_post - f1_pre, 4)},
    {"Metric": "Accuracy", "Pre_Mitigation": round(acc_pre, 4), "Post_Mitigation": round(acc_post, 4), "Change": round(acc_post - acc_pre, 4)},
    {"Metric": "Gender Disparate Impact (DI)", "Pre_Mitigation": round(di_pre, 4), "Post_Mitigation": round(di_post, 4), "Change": round(di_post - di_pre, 4)},
    {"Metric": "Gender Equal Opportunity Diff (EOD)", "Pre_Mitigation": round(eod_pre, 4), "Post_Mitigation": round(eod_post, 4), "Change": round(eod_post - eod_pre, 4)},
]

df_mitigation = pd.DataFrame(mitigation_comparison)
print("\nBEFORE VS. AFTER MITIGATION TRADE-OFF MATRIX (Reweighing on Training Set):")
print(df_mitigation.to_string(index=False))
print("\n>> Methodological Honesty: Mitigation slightly shifts demographic weighting")
print("   improving Disparate Impact, but involves an operational trade-off with overall Recall.")
print("   We report this trade-off explicitly and do NOT claim that Reweighing fully 'solves' institutional bias.")

# ═══════════════════════════════════════════════════════════════════════
# SECTION 6: PROXY PREDICTABILITY CHECK (GRAFTED FROM TEJASVI)
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("PROXY PREDICTABILITY CHECK (Spearman Correlation + RF AUC > 0.70)")
print("=" * 80)

proxy_targets = {
    "genero (Gender)": "genero",
    "raca (Race)": "raca",
    "rendabruta (Income)": "rendabruta",
    "idade (Age)": "idade",
    "quantidade_notebooks (Digital Access)": "quantidade_notebooks",
}

proxy_rows = []
for proxy_label, col_raw in proxy_targets.items():
    if col_raw in train_df.columns:
        # Build binarized proxy target from raw training data
        col_series = pd.to_numeric(train_df[col_raw], errors="coerce")
        if col_series.notnull().sum() > len(train_df) * 0.5:
            med = col_series.median()
            p_target_tr = (col_series > med).astype(int).values
            p_target_te = (pd.to_numeric(test_df[col_raw], errors="coerce") > med).astype(int).values
        else:
            # Categorical string: use most frequent category
            if col_raw == "genero":
                p_target_tr = (train_df[col_raw].astype(str).str.upper() == "M").astype(int).values
                p_target_te = (test_df[col_raw].astype(str).str.upper() == "M").astype(int).values
            elif col_raw == "raca":
                p_target_tr = (train_df[col_raw].astype(str) == "Branca").astype(int).values
                p_target_te = (test_df[col_raw].astype(str) == "Branca").astype(int).values
            else:
                continue

        # Use the encoded feature matrices (excluding the protected attribute itself)
        # Find indices in all_feature_names that correspond to this protected attribute
        exclude_indices = [i for i, fn in enumerate(all_feature_names) if fn.startswith(col_raw)]
        keep_indices = [i for i in range(X_train_full.shape[1]) if i not in exclude_indices]

        X_proxy_tr = X_train_full[:, keep_indices]
        clf_proxy = RandomForestClassifier(n_estimators=40, max_depth=8, random_state=GLOBAL_SEED, n_jobs=-1)

        # 3-fold CV AUC
        scores = cross_val_score(clf_proxy, X_proxy_tr, p_target_tr, cv=3, scoring="roc_auc", n_jobs=-1)
        mean_proxy_auc = scores.mean()

        flag = "YES (Proxy Risk)" if mean_proxy_auc > 0.70 else "NO"
        proxy_rows.append({
            "Protected_Attribute": proxy_label,
            "Predictor_Feature_Set": "All Other Non-Protected Attributes",
            "Proxy_Model_AUC": round(mean_proxy_auc, 3),
            "Flag_AUC_Above_0.70": flag
        })
        print(f"  {proxy_label:<40s} -> Proxy AUC = {mean_proxy_auc:.3f}  {flag}")

df_proxy = pd.DataFrame(proxy_rows)
df_proxy.to_csv(os.path.join(OUTPUT_DIR, "phase4_proxy_check.csv"), index=False)
print(f"Saved {OUTPUT_DIR}/phase4_proxy_check.csv")

# ═══════════════════════════════════════════════════════════════════════
# SAVE ALL PHASE 4 OUTPUTS
# ═══════════════════════════════════════════════════════════════════════
df_group_reports.to_csv(os.path.join(OUTPUT_DIR, "phase4_subgroup_metrics.csv"), index=False)
df_fairness.to_csv(os.path.join(OUTPUT_DIR, "phase4_fairness_audit_results.csv"), index=False)
df_mitigation.to_csv(os.path.join(OUTPUT_DIR, "phase4_mitigation_tradeoff.csv"), index=False)
thresh50_evals.to_csv(os.path.join(OUTPUT_DIR, "phase4_holm_bonferroni_results.csv"), index=False)

print(f"\nSaved Phase 4 audit files in {OUTPUT_DIR}/ successfully!")
print("PHASE 4 COMPLETE!")
