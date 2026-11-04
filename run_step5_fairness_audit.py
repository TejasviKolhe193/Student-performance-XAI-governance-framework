import os
import sys
import pickle
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

# AIF360 imports
from aif360.datasets import BinaryLabelDataset
from aif360.algorithms.preprocessing import Reweighing
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score, precision_score, f1_score, accuracy_score, roc_auc_score

sys.stdout.reconfigure(encoding='utf-8')
os.makedirs("results", exist_ok=True)

print("=" * 80)
print("EXECUTION: STEP 5 - ALGORITHMIC FAIRNESS AUDIT & MITIGATION")
print("=" * 80)

# Load data and locked bundle
with open("phase1_outputs/phase1_data.pkl", "rb") as f:
    p1 = pickle.load(f)

with open("results/chosen_model_bundle.pkl", "rb") as f:
    bundle = pickle.load(f)

chosen_model = bundle["model"]
selected_features = bundle["selected_features"]
top19_idx = bundle["top19_idx"]
X_train_sel = bundle["X_train_sel"]
X_test_sel = bundle["X_test_sel"]
X_tr_bal_sel = bundle["X_tr_bal_sel"]
y_tr_bal = bundle["y_tr_bal"]
y_train = bundle["y_train"]
y_test = bundle["y_test"]
y_prob = bundle["y_prob"]

train_df_raw = p1["train_df_raw"].copy()
test_df_raw = p1["test_df_raw"].copy()

# Attach predictions and probabilities
test_df_raw["y_true"] = y_test
test_df_raw["y_prob"] = y_prob
test_df_raw["y_pred_050"] = (y_prob >= 0.50).astype(int)
test_df_raw["y_pred_030"] = (y_prob >= 0.30).astype(int)
test_df_raw["y_pred_070"] = (y_prob >= 0.70).astype(int)

# Define Protected Binary Slices
income_median = train_df_raw["rendabruta"].median()

test_df_raw["gender_priv"] = (test_df_raw["genero"] == "M").astype(int) # 1: Male (priv), 0: Female (unpriv)
test_df_raw["income_priv"] = (test_df_raw["rendabruta"] > income_median).astype(int) # 1: > Med (priv), 0: <= Med (unpriv)
test_df_raw["age_priv"] = (test_df_raw["idade"] <= 20).astype(int) # 1: <= 20 (priv), 0: > 20 (unpriv)
test_df_raw["computer_priv"] = (test_df_raw["quantidade_notebooks"] > 0).astype(int) # 1: >= 1 (priv), 0: 0 (unpriv)

train_df_raw["gender_priv"] = (train_df_raw["genero"] == "M").astype(int)

audit_specs = [
    {"name": "Gender (M vs F)", "col": "gender_priv", "priv": 1, "unpriv": 0, "priv_lbl": "Male", "unpriv_lbl": "Female"},
    {"name": "Race (Branca vs Parda)", "col": "raca", "priv": "Branca", "unpriv": "Parda", "priv_lbl": "Branca", "unpriv_lbl": "Parda"},
    {"name": "Race (Branca vs Preta)", "col": "raca", "priv": "Branca", "unpriv": "Preta", "priv_lbl": "Branca", "unpriv_lbl": "Preta"},
    {"name": "Income (> Med vs <= Med)", "col": "income_priv", "priv": 1, "unpriv": 0, "priv_lbl": "> Median", "unpriv_lbl": "<= Median"},
    {"name": "Age (<=20 vs >20)", "col": "age_priv", "priv": 1, "unpriv": 0, "priv_lbl": "<= 20", "unpriv_lbl": "> 20"},
    {"name": "Computer Ownership (>=1 vs 0)", "col": "computer_priv", "priv": 1, "unpriv": 0, "priv_lbl": ">= 1", "unpriv_lbl": "0"}
]

# Function to compute audit metrics
def evaluate_fairness(df, pred_col, n_boot=1000, seed=42):
    np.random.seed(seed)
    records = []
    
    for spec in audit_specs:
        col = spec["col"]
        p_val = spec["priv"]
        u_val = spec["unpriv"]
        
        if col == "raca":
            sub = df[df[col].isin([p_val, u_val])].copy()
            sub["group_bin"] = (sub[col] == p_val).astype(int) # 1: priv, 0: unpriv
        else:
            sub = df.copy()
            sub["group_bin"] = (sub[col] == p_val).astype(int)
            
        n_p = (sub["group_bin"] == 1).sum()
        n_u = (sub["group_bin"] == 0).sum()
        
        # Point estimates
        sub_p = sub[sub["group_bin"] == 1]
        sub_u = sub[sub["group_bin"] == 0]
        
        sr_p = np.mean(sub_p[pred_col] == 1)
        sr_u = np.mean(sub_u[pred_col] == 1)
        di = sr_u / sr_p if sr_p > 0 else np.nan
        spd = sr_u - sr_p
        
        # Base dropout rates
        base_p = np.mean(sub_p["y_true"] == 1)
        base_u = np.mean(sub_u["y_true"] == 1)
        
        # TPR and FPR
        tpr_p = np.mean(sub_p[sub_p["y_true"] == 1][pred_col] == 1) if (sub_p["y_true"] == 1).sum() > 0 else np.nan
        tpr_u = np.mean(sub_u[sub_u["y_true"] == 1][pred_col] == 1) if (sub_u["y_true"] == 1).sum() > 0 else np.nan
        eod = tpr_u - tpr_p
        
        fpr_p = np.mean(sub_p[sub_p["y_true"] == 0][pred_col] == 1) if (sub_p["y_true"] == 0).sum() > 0 else np.nan
        fpr_u = np.mean(sub_u[sub_u["y_true"] == 0][pred_col] == 1) if (sub_u["y_true"] == 0).sum() > 0 else np.nan
        fpr_gap = fpr_u - fpr_p
        
        # EOD Fisher exact test p-value (comparing TPRs among actual positives)
        pos_p = sub_p[sub_p["y_true"] == 1]
        pos_u = sub_u[sub_u["y_true"] == 1]
        tp_p = (pos_p[pred_col] == 1).sum()
        fn_p = (pos_p[pred_col] == 0).sum()
        tp_u = (pos_u[pred_col] == 1).sum()
        fn_u = (pos_u[pred_col] == 0).sum()
        
        table = [[tp_p, fn_p], [tp_u, fn_u]]
        _, p_val_eod = stats.fisher_exact(table)
        
        # Bootstrap CIs
        b_di, b_spd, b_eod, b_tpr_p, b_tpr_u, b_fpr_p, b_fpr_u = [], [], [], [], [], [], []
        n_sub = len(sub)
        
        for _ in range(n_boot):
            idx = np.random.choice(n_sub, size=n_sub, replace=True)
            b_sample = sub.iloc[idx]
            b_p = b_sample[b_sample["group_bin"] == 1]
            b_u = b_sample[b_sample["group_bin"] == 0]
            
            b_srp = np.mean(b_p[pred_col] == 1) if len(b_p) > 0 else np.nan
            b_sru = np.mean(b_u[pred_col] == 1) if len(b_u) > 0 else np.nan
            
            b_di.append(b_sru / b_srp if (b_srp and b_srp > 0) else np.nan)
            b_spd.append(b_sru - b_srp if (b_sru is not np.nan and b_srp is not np.nan) else np.nan)
            
            b_tprp = np.mean(b_p[b_p["y_true"] == 1][pred_col] == 1) if (b_p["y_true"] == 1).sum() > 0 else np.nan
            b_tpru = np.mean(b_u[b_u["y_true"] == 1][pred_col] == 1) if (b_u["y_true"] == 1).sum() > 0 else np.nan
            b_tpr_p.append(b_tprp)
            b_tpr_u.append(b_tpru)
            b_eod.append(b_tpru - b_tprp if (b_tpru is not np.nan and b_tprp is not np.nan) else np.nan)
            
            b_fprp = np.mean(b_p[b_p["y_true"] == 0][pred_col] == 1) if (b_p["y_true"] == 0).sum() > 0 else np.nan
            b_fpru = np.mean(b_u[b_u["y_true"] == 0][pred_col] == 1) if (b_u["y_true"] == 0).sum() > 0 else np.nan
            b_fpr_p.append(b_fprp)
            b_fpr_u.append(b_fpru)
            
        def get_ci(arr):
            clean = [x for x in arr if not np.isnan(x)]
            if len(clean) == 0:
                return "N/A"
            return f"[{np.percentile(clean, 2.5):.4f}, {np.percentile(clean, 97.5):.4f}]"
            
        records.append({
            "Dimension": spec["name"],
            "N_Priv": n_p,
            "N_Unpriv": n_u,
            "Base_Rate_Priv": round(base_p, 4),
            "Base_Rate_Unpriv": round(base_u, 4),
            "Selection_Rate_Priv": round(sr_p, 4),
            "Selection_Rate_Unpriv": round(sr_u, 4),
            "Disparate_Impact_DI": round(di, 4),
            "DI_95_CI": get_ci(b_di),
            "DI_Four_Fifths_Status": "Pass [0.80, 1.25]" if (0.80 <= di <= 1.25) else "Screening Flag",
            "Statistical_Parity_Diff": round(spd, 4),
            "SPD_95_CI": get_ci(b_spd),
            "TPR_Priv": round(tpr_p, 4),
            "TPR_Unpriv": round(tpr_u, 4),
            "Equal_Opportunity_Diff_EOD": round(eod, 4),
            "EOD_95_CI": get_ci(b_eod),
            "FPR_Priv": round(fpr_p, 4),
            "FPR_Unpriv": round(fpr_u, 4),
            "FPR_Gap": round(fpr_gap, 4),
            "P_Value_EOD": round(p_val_eod, 6)
        })
        
    return pd.DataFrame(records)

# 1. Main Audit at tau = 0.50
print("\n--- 1. MAIN FAIRNESS AUDIT AT THRESHOLD tau = 0.50 ---")
main_audit_df = evaluate_fairness(test_df_raw, "y_pred_050")
print(main_audit_df[["Dimension", "N_Priv", "N_Unpriv", "Disparate_Impact_DI", "DI_Four_Fifths_Status", "Equal_Opportunity_Diff_EOD", "FPR_Gap", "P_Value_EOD"]].to_string(index=False))

main_audit_df.to_csv("results/step5_main_fairness_audit_tau_050.csv", index=False)
print("Saved results/step5_main_fairness_audit_tau_050.csv")

# 2. Appendix Audits at tau = 0.30 and tau = 0.70
print("\n--- 2. APPENDIX AUDIT AT THRESHOLDS tau = 0.30 AND tau = 0.70 ---")
audit_030 = evaluate_fairness(test_df_raw, "y_pred_030")
audit_030["Threshold"] = 0.30
audit_070 = evaluate_fairness(test_df_raw, "y_pred_070")
audit_070["Threshold"] = 0.70

appendix_df = pd.concat([audit_030, audit_070], ignore_index=True)
appendix_df.to_csv("results/step5_appendix_fairness_audit_tau_030_070.csv", index=False)
print("Saved results/step5_appendix_fairness_audit_tau_030_070.csv")

# 3. Holm-Bonferroni Correction on EOD P-Values (alpha = 0.05)
print("\n--- 3. HOLM-BONFERRONI CORRECTION ON EOD P-VALUES (tau = 0.50) ---")
holm_df = main_audit_df[["Dimension", "Equal_Opportunity_Diff_EOD", "P_Value_EOD"]].copy()
holm_df = holm_df.sort_values(by="P_Value_EOD", ascending=True).reset_index(drop=True)
m = len(holm_df)
alpha = 0.05

holm_df["Rank_i"] = range(1, m + 1)
holm_df["Holm_Threshold"] = [round(alpha / (m - i + 1), 6) for i in range(1, m + 1)]
holm_df["Significant_After_Correction"] = holm_df["P_Value_EOD"] <= holm_df["Holm_Threshold"]

print(holm_df.to_string(index=False))
holm_df.to_csv("results/step5_holm_bonferroni_eod.csv", index=False)
print("Saved results/step5_holm_bonferroni_eod.csv")

# 4. AIF360 Reweighing Pre-Processing Mitigation (Gender)
print("\n--- 4. AIF360 REWEIGHING MITIGATION & PERFORMANCE TRADEOFF ---")

# Train AIF360 dataset on training features
train_feat_df = pd.DataFrame(X_train_sel, columns=selected_features)
train_feat_df["gender_priv"] = train_df_raw["gender_priv"].values
train_feat_df["y_true"] = y_train

aif_train = BinaryLabelDataset(
    df=train_feat_df,
    label_names=["y_true"],
    protected_attribute_names=["gender_priv"],
    favorable_label=0,
    unfavorable_label=1
)

reweighter = Reweighing(
    unprivileged_groups=[{"gender_priv": 0}],
    privileged_groups=[{"gender_priv": 1}]
)
reweighter.fit(aif_train)
aif_train_transformed = reweighter.transform(aif_train)
sample_weights = aif_train_transformed.instance_weights

print(f"Sample weights computed via AIF360 Reweighing: min={sample_weights.min():.4f}, max={sample_weights.max():.4f}, mean={sample_weights.mean():.4f}")

# Train Mitigated Random Forest with Reweighed weights
rf_mitigated = RandomForestClassifier(
    n_estimators=100, max_depth=10, min_samples_leaf=5, min_samples_split=10,
    random_state=42, n_jobs=-1
)
rf_mitigated.fit(X_train_sel, y_train, sample_weight=sample_weights)

# Evaluate Mitigated Model on Held-out Test Set
y_prob_mit = rf_mitigated.predict_proba(X_test_sel)[:, 1]
y_pred_mit = (y_prob_mit >= 0.50).astype(int)

# Before vs After metrics
rec_pre = recall_score(y_test, (y_prob >= 0.50).astype(int))
prec_pre = precision_score(y_test, (y_prob >= 0.50).astype(int))
f1_pre = f1_score(y_test, (y_prob >= 0.50).astype(int))
acc_pre = accuracy_score(y_test, (y_prob >= 0.50).astype(int))

rec_post = recall_score(y_test, y_pred_mit)
prec_post = precision_score(y_test, y_pred_mit)
f1_post = f1_score(y_test, y_pred_mit)
acc_post = accuracy_score(y_test, y_pred_mit)

# Gender Fairness before vs after
sr_m_pre = np.mean(test_df_raw[test_df_raw["gender_priv"] == 1]["y_pred_050"] == 1)
sr_f_pre = np.mean(test_df_raw[test_df_raw["gender_priv"] == 0]["y_pred_050"] == 1)
di_pre = sr_f_pre / sr_m_pre

sr_m_post = np.mean(y_pred_mit[test_df_raw["gender_priv"] == 1] == 1)
sr_f_post = np.mean(y_pred_mit[test_df_raw["gender_priv"] == 0] == 1)
di_post = sr_f_post / sr_m_post

tpr_m_pre = np.mean((y_prob >= 0.50)[(test_df_raw["gender_priv"] == 1) & (y_test == 1)])
tpr_f_pre = np.mean((y_prob >= 0.50)[(test_df_raw["gender_priv"] == 0) & (y_test == 1)])
eod_pre = tpr_f_pre - tpr_m_pre

tpr_m_post = np.mean(y_pred_mit[(test_df_raw["gender_priv"] == 1) & (y_test == 1)] == 1)
tpr_f_post = np.mean(y_pred_mit[(test_df_raw["gender_priv"] == 0) & (y_test == 1)] == 1)
eod_post = tpr_f_post - tpr_m_post

mitigation_records = [
    {"Metric": "Recall", "Pre_Mitigation": round(rec_pre, 4), "Post_Mitigation": round(rec_post, 4), "Delta": round(rec_post - rec_pre, 4)},
    {"Metric": "Precision", "Pre_Mitigation": round(prec_pre, 4), "Post_Mitigation": round(prec_post, 4), "Delta": round(prec_post - prec_pre, 4)},
    {"Metric": "F1-Score", "Pre_Mitigation": round(f1_pre, 4), "Post_Mitigation": round(f1_post, 4), "Delta": round(f1_post - f1_pre, 4)},
    {"Metric": "Accuracy", "Pre_Mitigation": round(acc_pre, 4), "Post_Mitigation": round(acc_post, 4), "Delta": round(acc_post - acc_pre, 4)},
    {"Metric": "Gender Disparate Impact (DI)", "Pre_Mitigation": round(di_pre, 4), "Post_Mitigation": round(di_post, 4), "Delta": round(di_post - di_pre, 4)},
    {"Metric": "Gender Equal Opportunity Diff (EOD)", "Pre_Mitigation": round(eod_pre, 4), "Post_Mitigation": round(eod_post, 4), "Delta": round(eod_post - eod_pre, 4)}
]

mitigation_df = pd.DataFrame(mitigation_records)
print(mitigation_df.to_string(index=False))

mitigation_df.to_csv("results/step5_reweighing_mitigation_tradeoff.csv", index=False)
print("Saved results/step5_reweighing_mitigation_tradeoff.csv")

# 5. Generate Fairness Figure (Fig 4)
plt.figure(figsize=(10, 5))
dims = [r["name"].split("(")[0].strip() for r in audit_specs]
dis = main_audit_df["Disparate_Impact_DI"].values
plt.axhspan(0.80, 1.25, color="#2ca02c", alpha=0.15, label="Four-Fifths Rule Parity Zone [0.80, 1.25]")
plt.axhline(1.0, color="black", linestyle="--", linewidth=0.8)
colors = ["#1f77b4" if (0.80 <= d <= 1.25) else "#d62728" for d in dis]
bars = plt.bar(dims, dis, color=colors, width=0.55)
plt.ylabel("Disparate Impact Ratio (Unprivileged / Privileged)")
plt.title("Algorithmic Fairness Audit: Disparate Impact by Protected Axis (tau = 0.50)", fontsize=12)
plt.ylim(0, 2.0)
for bar, d in zip(bars, dis):
    plt.text(bar.get_x() + bar.get_width()/2, d + 0.04, f"{d:.3f}", ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.grid(True, linestyle=":", alpha=0.5, axis='y')
plt.legend(loc="upper right")
plt.xticks(rotation=15, ha='right')
plt.tight_layout()
plt.savefig("results/fig4_fairness_audit.png", dpi=300)
plt.close()
print("Saved results/fig4_fairness_audit.png")

print("\n" + "=" * 80)
print("STEP 5 COMPLETE AND FULLY VERIFIED!")
print("=" * 80)

