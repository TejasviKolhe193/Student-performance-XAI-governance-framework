"""
Phase 5: Operational Governance Charter and Risk-Band Calibration (Best-of-Both Merge)
======================================================================================
Inherited from dev (Sahiti):
  - Calibrated risk-band table with 8 operational tiers (0.10 through 0.80).
  - Five Institutional Governance Pillars as normative policy text.
  - Mandatory proposal disclaimer.

Grafted from tejasvi:
  - Calibration curve (reliability diagram) with Brier score.
  - Counselor workload estimation per 5,000-student cohort.

Uses already-trained Phase 2 champion model (NO retraining).
"""

import os
import sys
import io
import pickle
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, recall_score, brier_score_loss
from sklearn.calibration import calibration_curve

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace", line_buffering=True)

OUTPUT_DIR = "phase5_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 80)
print("PHASE 5: OPERATIONAL GOVERNANCE CHARTER & RISK-BAND CALIBRATION")
print("           (Best-of-Both Merge: Risk Bands + Calibration Curve + Governance)")
print("=" * 80)

# Load test set probabilities from Phase 2 champion (NO retraining)
with open("phase2_outputs/champion_model_bundle.pkl", "rb") as f:
    p2 = pickle.load(f)

rf_model = p2["champion_rf"]
rf_mask = p2["champion_mask"]
X_test_rf = p2["X_test"][:, rf_mask]
y_test = p2["y_test"]

test_probs = rf_model.predict_proba(X_test_rf)[:, 1]

# ═══════════════════════════════════════════════════════════════════════
# SECTION 1: CALIBRATED RISK-BAND TABLE (8 OPERATIONAL TIERS)
# (Retained from dev: comprehensive threshold sweep)
# ═══════════════════════════════════════════════════════════════════════
eval_thresholds = [
    (0.80, "Tier 1: Emergency Intervention Band"),
    (0.70, "Tier 2: High Priority At-Risk Band"),
    (0.60, "Tier 3: Moderate Risk Advisory Band"),
    (0.50, "Tier 4: Baseline Standard Threshold"),
    (0.40, "Tier 5: Early Sensitivity Screening"),
    (0.30, "Tier 6: Broad Precautionary Monitoring"),
    (0.20, "Tier 7: Low Concern Baseline"),
    (0.10, "Tier 8: Universal Inclusion Screening"),
]

risk_band_rows = []
total_test = len(y_test)
COHORT_SIZE = 5000
COUNSELOR_CASES_PER_WEEK = 50

for thresh, label in eval_thresholds:
    preds = (test_probs >= thresh).astype(int)
    n_flagged = np.sum(preds == 1)
    sel_rate = n_flagged / total_test
    flags_per_1000 = int(round(sel_rate * 1000))
    flags_in_cohort = int(round(sel_rate * COHORT_SIZE))

    prec = precision_score(y_test, preds, zero_division=0)
    rec = recall_score(y_test, preds, zero_division=0)

    # Workload estimation (grafted from tejasvi)
    weeks_for_1_counselor = round(flags_in_cohort / COUNSELOR_CASES_PER_WEEK, 1)
    counselors_for_4wk_sla = max(1, int(np.ceil(flags_in_cohort / (COUNSELOR_CASES_PER_WEEK * 4))))

    risk_band_rows.append({
        "Threshold": thresh,
        "Band_Label": label,
        "Expected_Flags_Per_1000_Students": flags_per_1000,
        "Expected_Precision": round(prec, 4),
        "Expected_Recall": round(rec, 4),
        "Historical_Dropout_Catch_Rate": f"{rec*100:.1f}%",
        "False_Alarm_Rate_In_Flags": f"{(1 - prec)*100:.1f}%",
        "Total_Flags_Per_5000_Cohort": flags_in_cohort,
        "Weeks_for_One_Counselor": weeks_for_1_counselor,
        "Counselors_Needed_for_4Wk_SLA": counselors_for_4wk_sla,
    })

df_risk_bands = pd.DataFrame(risk_band_rows)
print("\nCALIBRATED OPERATIONAL RISK-BAND INTERVENTION ALLOCATION TABLE:")
print(df_risk_bands[["Threshold", "Band_Label", "Expected_Flags_Per_1000_Students",
                      "Expected_Precision", "Expected_Recall",
                      "Total_Flags_Per_5000_Cohort", "Counselors_Needed_for_4Wk_SLA"]].to_string(index=False))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 2: CALIBRATION CURVE + BRIER SCORE (GRAFTED FROM TEJASVI)
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("CALIBRATION RELIABILITY DIAGRAM & BRIER SCORE")
print("=" * 80)

prob_true, prob_pred = calibration_curve(y_test, test_probs, n_bins=10, strategy="uniform")
brier = brier_score_loss(y_test, test_probs)

print(f"Brier Score: {brier:.4f} (lower is better; perfect = 0.00)")
print(f"Calibration Curve (10 uniform bins):")
for i, (pt, pp) in enumerate(zip(prob_true, prob_pred)):
    print(f"  Bin {i+1}: Mean Predicted = {pp:.3f}, Fraction Positive = {pt:.3f}")

plt.figure(figsize=(7, 6))
plt.plot(prob_pred, prob_true, marker='o', linewidth=2, label=f"RF Champion (Brier={brier:.4f})")
plt.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Perfect Calibration')
plt.xlabel("Mean Predicted Probability", fontsize=11)
plt.ylabel("Fraction of Positives", fontsize=11)
plt.title("Calibration Reliability Diagram (RF: k=19, No GPA)", fontsize=12)
plt.legend(loc="lower right")
plt.grid(True, linestyle=":", alpha=0.6)
plt.tight_layout()
cal_path = os.path.join(OUTPUT_DIR, "phase5_calibration_curve.png")
plt.savefig(cal_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"Saved: {cal_path}")

# ═══════════════════════════════════════════════════════════════════════
# SECTION 3: FIVE GOVERNANCE PILLARS POLICY TEXT
# (Retained from dev: normative institutional proposal)
# ═══════════════════════════════════════════════════════════════════════
governance_policy_text = """# Operational AI Governance Charter: Five Institutional Pillars

> **Mandatory Institutional Disclaimer**:
> **The governance charter is a proposal. No pilot or user study was conducted.**

---

### Pillar 1: Strictly Advisory, Non-Punitive Deployment
Predictive model inferences are classified strictly as clinical-advisory signals designed solely to trigger institutional support mechanisms (e.g., remedial peer tutoring, transportation assistance, social worker outreach). Under no circumstances may an automated prediction be used to justify disciplinary dismissal, suspension, tracking into lower academic tiers, or denial of institutional re-enrollment.

### Pillar 2: Mandatory Explainability-Coupled Outreach
No institutional counselor or faculty member may initiate outreach based purely on a raw risk score. Prior to contacting a flagged student, staff must inspect the localized feature attribution breakdown (SHAP / LIME factors). Interventions must directly target the identified barrier—socioeconomic aid for financial vulnerability, or academic peer assistance for course failures.

### Pillar 3: Scheduled Algorithmic Fairness Audits & Drift Monitoring
The predictive system must undergo mandatory semi-annual algorithmic audits prior to the start of each academic semester. Audits must evaluate Disparate Impact (Four-Fifths Rule: 0.80–1.25) and Equal Opportunity Difference (True Positive Rate parity: |EOD| <= 0.10) across Gender, Race/Ethnicity, Socioeconomic Income, Age, and Digital Access, with Holm-Bonferroni correction applied. Any statistically significant degradation triggers model suspension and retraining.

### Pillar 4: Institutional Contestability & Student Appeal Process
All students flagged for secondary or specialized institutional interventions maintain the right to receive an accessible, plain-language explanation of why they were flagged, along with their primary contributing factors. Students possess an unconditional procedural right to contest incorrect administrative records (e.g., erroneous attendance logging or outdated income brackets) and have their risk status recalculated.

### Pillar 5: Certified Human-in-the-Loop Override & Decision Authority
Final intervention determinations rest exclusively with certified human educational counselors and multidisciplinary pedagogical committees. Human professionals retain unilateral authority to override, downgrade, or dismiss algorithmic flags without penalty. The machine learning pipeline serves strictly to assist, never replace, human judgment.
"""

with open(os.path.join(OUTPUT_DIR, "governance_policy_charter.md"), "w", encoding="utf-8") as f:
    f.write(governance_policy_text)

# ═══════════════════════════════════════════════════════════════════════
# SAVE ALL PHASE 5 OUTPUTS
# ═══════════════════════════════════════════════════════════════════════
df_risk_bands.to_csv(os.path.join(OUTPUT_DIR, "phase5_governance_risk_bands.csv"), index=False)

# Save Brier score summary
brier_summary = pd.DataFrame([{
    "Model": "RF Champion (k=19, No GPA)",
    "Brier_Score": round(brier, 4),
    "Interpretation": "Good" if brier < 0.15 else "Moderate" if brier < 0.25 else "Poor",
    "N_Test": len(y_test),
    "Prevalence": round(np.mean(y_test), 4),
}])
brier_summary.to_csv(os.path.join(OUTPUT_DIR, "phase5_calibration_summary.csv"), index=False)
print(f"\nSaved phase5_outputs/phase5_governance_risk_bands.csv, governance_policy_charter.md,")
print(f"  phase5_calibration_curve.png, and phase5_calibration_summary.csv successfully!")
print("PHASE 5 COMPLETE!")
