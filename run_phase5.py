"""
Phase 5: Operational Governance Charter and Risk-Band Calibration
- Produces calibrated risk-band table:
    Threshold, Band Label, Expected Flags per 1000 Students, Expected Precision, Expected Recall.
- Formulates the Five Institutional Governance Pillars strictly as normative policy text.
- Formulates the mandatory proposal disclaimer:
    "The governance charter is a proposal. No pilot or user study was conducted."
- Outputs phase5_governance_risk_bands.csv and summary text.
"""

import os
import sys
import io
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace", line_buffering=True)

OUTPUT_DIR = "phase5_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 80)
print("PHASE 5: OPERATIONAL GOVERNANCE CHARTER & RISK-BAND CALIBRATION")
print("=" * 80)

# Load test set probabilities from Phase 2 champion
with open("phase2_outputs/champion_model_bundle.pkl", "rb") as f:
    p2 = pickle.load(f)

rf_model = p2["champion_rf"]
rf_mask = p2["champion_mask"]
X_test_rf = p2["X_test"][:, rf_mask]
y_test = p2["y_test"]

test_probs = rf_model.predict_proba(X_test_rf)[:, 1]

# Define operational risk bands and evaluated thresholds
# We evaluate thresholds across the continuum: 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80
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

for thresh, label in eval_thresholds:
    preds = (test_probs >= thresh).astype(int)
    n_flagged = np.sum(preds == 1)
    sel_rate = n_flagged / total_test
    flags_per_1000 = int(round(sel_rate * 1000))
    
    prec = precision_score(y_test, preds, zero_division=0)
    rec = recall_score(y_test, preds, zero_division=0)
    
    risk_band_rows.append({
        "Threshold": thresh,
        "Band_Label": label,
        "Expected_Flags_Per_1000_Students": flags_per_1000,
        "Expected_Precision": round(prec, 4),
        "Expected_Recall": round(rec, 4),
        "Historical_Dropout_Catch_Rate": f"{rec*100:.1f}%",
        "False_Alarm_Rate_In_Flags": f"{(1 - prec)*100:.1f}%"
    })

df_risk_bands = pd.DataFrame(risk_band_rows)
print("\nCALIBRATED OPERATIONAL RISK-BAND INTERVENTION ALLOCATION TABLE:")
print(df_risk_bands[["Threshold", "Band_Label", "Expected_Flags_Per_1000_Students", "Expected_Precision", "Expected_Recall"]].to_string(index=False))

# Five Governance Pillars Policy Text
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

df_risk_bands.to_csv(os.path.join(OUTPUT_DIR, "phase5_governance_risk_bands.csv"), index=False)

print(f"\nSaved phase5_outputs/phase5_governance_risk_bands.csv and governance_policy_charter.md successfully!")
print("PHASE 5 COMPLETE!")

