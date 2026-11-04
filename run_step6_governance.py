import os
import sys
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding='utf-8')
os.makedirs("results", exist_ok=True)

print("=" * 80)
print("EXECUTION: STEP 6 - GOVERNANCE, RISK BANDS & CALIBRATION AUDIT")
print("=" * 80)

# Load locked model bundle from Step 2/4
with open("results/chosen_model_bundle.pkl", "rb") as f:
    bundle = pickle.load(f)

y_test = bundle["y_test"]
y_prob = bundle["y_prob"]
total_test = len(y_test)

print(f"Loaded locked Random Forest test predictions (N = {total_test})")
print(f"Overall test dropout prevalence: {y_test.mean()*100:.2f}%")

# ==============================================================================
# 1. DISCRETE RISK BANDS (MUTUALLY EXCLUSIVE INTERVALS)
# ==============================================================================
# Define mutually exclusive probability intervals
intervals = [
    ("[0.80, 1.00]", 0.80, 1.0001, "Emergency Tier"),
    ("[0.60, 0.80)", 0.60, 0.80,   "High Priority Tier"),
    ("[0.40, 0.60)", 0.40, 0.60,   "Moderate Risk / Watchlist"),
    ("[0.20, 0.40)", 0.20, 0.40,   "Low Concern Tier"),
    ("[0.00, 0.20)", 0.00, 0.20,   "Minimal Risk Tier")
]

discrete_rows = []
for label, low, high, tier_name in intervals:
    mask = (y_prob >= low) & (y_prob < high)
    n_students = np.sum(mask)
    if n_students > 0:
        actual_dropouts = np.sum(y_test[mask] == 1)
        observed_rate = actual_dropouts / n_students
        mean_pred = np.mean(y_prob[mask])
    else:
        actual_dropouts = 0
        observed_rate = 0.0
        mean_pred = 0.0
        
    discrete_rows.append({
        "Probability_Interval": label,
        "Tier_Name": tier_name,
        "Student_Count": n_students,
        "Percentage_of_Cohort": round((n_students / total_test) * 100, 2),
        "Mean_Predicted_Prob": round(mean_pred, 4),
        "Actual_Dropouts": actual_dropouts,
        "Observed_Dropout_Rate": round(observed_rate, 4),
        "Calibration_Discrepancy": round(observed_rate - mean_pred, 4)
    })

df_discrete = pd.DataFrame(discrete_rows)
print("\n--- 1. MUTUALLY EXCLUSIVE RISK BANDS & OBSERVED OUTCOMES ---")
print(df_discrete.to_string(index=False))
df_discrete.to_csv("results/step6_discrete_risk_bands_audit.csv", index=False)
print("Saved results/step6_discrete_risk_bands_audit.csv")

# ==============================================================================
# 2. CUMULATIVE OPERATIONAL RISK-BAND ALLOCATION TABLE (8 TIERS)
# ==============================================================================
eval_thresholds = [
    (0.80, "Tier 1: Emergency Intervention Band", "Mandatory counselor case review & emergency retention stipend"),
    (0.70, "Tier 2: High Priority At-Risk Band", "Social worker outreach, transport assistance, peer tutoring"),
    (0.60, "Tier 3: Moderate Risk Advisory Band", "Academic advisor check-in, course failure remediation plan"),
    (0.50, "Tier 4: Baseline Standard Threshold", "General counselor notification, automated attendance monitoring"),
    (0.40, "Tier 5: Early Sensitivity Screening", "Classroom teacher notification, voluntary group tutoring"),
    (0.30, "Tier 6: Broad Precautionary Monitoring", "Departmental cohort tracking, term-start check-ins"),
    (0.20, "Tier 7: Low Concern Baseline", "Standard educational advising & institutional orientation"),
    (0.10, "Tier 8: Universal Inclusion Screening", "Universal institutional demographic tracking")
]

COHORT_SIZE = 5000
COUNSELOR_CASES_PER_WEEK = 50

cumulative_rows = []
for thresh, label, action in eval_thresholds:
    preds = (y_prob >= thresh).astype(int)
    n_flagged = np.sum(preds == 1)
    sel_rate = n_flagged / total_test
    flags_per_1000 = int(round(sel_rate * 1000))
    flags_in_5000 = int(round(sel_rate * COHORT_SIZE))
    
    tp = np.sum((preds == 1) & (y_test == 1))
    fp = np.sum((preds == 1) & (y_test == 0))
    
    prec = tp / n_flagged if n_flagged > 0 else 0.0
    rec = tp / np.sum(y_test == 1)
    
    # Workload SLA
    weeks_for_1_counselor = round(flags_in_5000 / COUNSELOR_CASES_PER_WEEK, 1)
    counselors_needed_4wks = max(1, int(np.ceil(flags_in_5000 / (COUNSELOR_CASES_PER_WEEK * 4))))
    
    cumulative_rows.append({
        "Threshold": thresh,
        "Tier_Label": label,
        "Flags_Per_1000": flags_per_1000,
        "Expected_Flags_5000_Cohort": flags_in_5000,
        "Precision_PPV": round(prec, 4),
        "Recall_Catch_Rate": round(rec, 4),
        "Observed_Dropout_Rate_In_Flags": round(prec, 4),
        "False_Alarm_Rate_In_Flags": round(1.0 - prec, 4),
        "Weeks_for_One_Counselor": weeks_for_1_counselor,
        "Counselors_Needed_4Wk_SLA": counselors_needed_4wks,
        "Recommended_Action_Protocol": action
    })

df_cumulative = pd.DataFrame(cumulative_rows)
print("\n--- 2. CUMULATIVE OPERATIONAL RISK-BAND ALLOCATION TABLE ---")
print(df_cumulative[["Threshold", "Tier_Label", "Flags_Per_1000", "Precision_PPV", "Recall_Catch_Rate", "Expected_Flags_5000_Cohort", "Counselors_Needed_4Wk_SLA"]].to_string(index=False))
df_cumulative.to_csv("results/step6_cumulative_operational_risk_bands.csv", index=False)
print("Saved results/step6_cumulative_operational_risk_bands.csv")

# ==============================================================================
# 3. GOVERNANCE POLICY CHARTER SPECIFICATION (PROPOSED DESIGN, NOT FIELD-TESTED)
# ==============================================================================
charter_text = """# Operational AI Governance Charter: Five Institutional Pillars
## Proposed Governance Framework for Educational Risk Classification (Not Field-Tested)

> **Mandatory Institutional Disclaimer**:
> This governance framework is a **proposed operational design and has not been field-tested in an active educational setting**. No pilot deployment, randomized trial, or formal user study with academic counselors was conducted. All risk bands, review protocols, and intervention thresholds are heuristic policy recommendations that require empirical validation prior to institutional adoption.

---

### Pillar 1: Strictly Advisory, Non-Punitive Deployment
Predictive model inferences are classified strictly as clinical-advisory signals designed solely to trigger supportive institutional retention mechanisms (e.g., remedial peer tutoring, transportation assistance, social worker outreach). Under no circumstances may an automated prediction be used to sanction, dismiss, track into lower academic streams, or deny institutional re-enrollment to any student.

### Pillar 2: Mandatory Explainability-Coupled Outreach
Educational counselors and faculty members are prohibited from initiating student outreach based solely on an aggregate risk probability. Prior to contacting a flagged student, staff must inspect the individualized feature attribution breakdown (top SHAP and LIME factors). Support interventions must directly address the identified friction point—such as socioeconomic aid for financial hardship or academic tutoring for course failures.

### Pillar 3: Scheduled Semi-Annual Auditing & Drift Triggers
The predictive system must undergo formal **semi-annual algorithmic audits** scheduled prior to the start of each academic semester. Audits must evaluate:
1. Disparate Impact (Four-Fifths Rule screening heuristic: 0.80–1.25) across Gender, Race/Ethnicity, Household Income, Age, and Digital Access.
2. Equal Opportunity Difference (True Positive Rate parity: |EOD| <= 0.10) with Holm-Bonferroni correction.
3. Unscheduled out-of-cycle audits are automatically triggered if: (a) curriculum requirements change, (b) student demographic composition shifts by >10%, or (c) quarterly prediction volume deviates by >15% from historical baselines. Any statistically significant degradation in fairness triggers immediate model suspension and review.

### Pillar 4: Student Notice, Explanation Access & Appeal Rights (LGPD Alignment)
In accordance with Brazilian General Data Protection Law (LGPD Art. 20) and international data ethics standards:
- Students flagged for secondary or specialized institutional interventions must receive clear, plain-language notice explaining that an algorithmic tool assisted in identifying support opportunities.
- Students maintain an unconditional right to inspect the primary factors contributing to their assessment and to request human review.
- Students possess a formal procedural avenue to challenge and correct erroneous administrative records (such as misrecorded attendance or outdated household income brackets), initiating a mandatory recalculation of their risk profile within 10 business days.

### Pillar 5: Certified Human-in-the-Loop Override Authority
Final intervention determinations rest exclusively with certified educational counselors, social workers, and multidisciplinary student support committees. Human professionals retain absolute, unilateral authority to override, downgrade, or dismiss algorithmic alerts based on qualitative context, clinical judgment, or personal student disclosures. Under no circumstances may algorithmic recommendations supersede human decision-making.
"""

with open("results/step6_governance_policy_charter.md", "w", encoding="utf-8") as f:
    f.write(charter_text)
print("Saved results/step6_governance_policy_charter.md")

# ==============================================================================
# 4. PLOT RISK BANDS VS. OBSERVED RATES (FIG 5)
# ==============================================================================
plt.figure(figsize=(9, 5))
x_labels = df_discrete["Probability_Interval"]
pred_rates = df_discrete["Mean_Predicted_Prob"] * 100
obs_rates = df_discrete["Observed_Dropout_Rate"] * 100

x = np.arange(len(x_labels))
width = 0.35

plt.bar(x - width/2, pred_rates, width, label="Mean Predicted Probability (%)", color="#1f77b4")
plt.bar(x + width/2, obs_rates, width, label="Observed Dropout Rate (%)", color="#ff7f0e")

plt.xlabel("Heuristic Probability Risk Band")
plt.ylabel("Percentage (%)")
plt.title("Heuristic Risk Bands: Predicted vs. Observed Dropout Rates (Test N = 4,526)", fontsize=12)
plt.xticks(x, x_labels)
plt.legend(loc="upper left")
plt.grid(True, linestyle=":", alpha=0.5, axis='y')

for i in range(len(x)):
    plt.text(x[i] - width/2, pred_rates.iloc[i] + 1.5, f"{pred_rates.iloc[i]:.1f}%", ha='center', fontsize=9)
    plt.text(x[i] + width/2, obs_rates.iloc[i] + 1.5, f"{obs_rates.iloc[i]:.1f}%", ha='center', fontsize=9)

plt.ylim(0, 105)
plt.tight_layout()
plt.savefig("results/fig5_risk_bands_calibration.png", dpi=300)
plt.close()
print("Saved results/fig5_risk_bands_calibration.png")

print("\n" + "=" * 80)
print("STEP 6 COMPLETE AND FULLY AUDITED!")
print("=" * 80)

