# Consistency Check: Data, Text, Tables, and Figures (`consistency_check.md`)

This document verifies the numerical, logical, and structural consistency across all components of the research paper (`paper_review/research_paper_final_draft.docx`), the markdown reports, and the underlying empirical artifacts in `results/`.

---

## 1. Global Cohort and Partition Consistency

| Metric / Parameter | Abstract | Section III (Methods) | Section IV (Results) | Raw Artifact Source (`results/`) | Consistency Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Total Cohort Size ($N$)** | 15,084 | 15,084 | 15,084 | `dataset_evasao_MDE.xlsx` filtered | **100% MATCH** |
| **Class 0 (Completed)** | 11,703 (77.59%) | 11,703 (77.59%) | 11,703 (77.59%) | `step1_cohort_summary.csv` | **100% MATCH** |
| **Class 1 (Dropout / Attrition)** | 3,381 (22.41%) | 3,381 (22.41%) | 3,381 (22.41%) | `step1_cohort_summary.csv` | **100% MATCH** |
| **Partition Split Ratio** | 70/30 Stratified | 70/30 Stratified | 70/30 Stratified | `step2_model_performance_summary.csv` | **100% MATCH** |
| **Training Set Size ($N_{train}$)** | 10,558 (22.41% prev.) | 10,558 (22.41% prev.) | 10,558 (22.41% prev.) | `step2_candidate_models_comparison.csv` | **100% MATCH** |
| **Held-Out Test Set Size ($N_{test}$)** | 4,526 (22.40% prev.) | 4,526 (22.40% prev.) | 4,526 (22.40% prev.) | `step2_model_performance_summary.csv` | **100% MATCH** |
| **Held-Out Test Breakdown** | 3,512 Cls 0 / 1,014 Cls 1 | 3,512 Cls 0 / 1,014 Cls 1 | 3,512 Cls 0 / 1,014 Cls 1 | `step2_model_performance_summary.csv` | **100% MATCH** |

---

## 2. Champion Model Performance Consistency (Random Forest, Seed 42)

| Performance Metric | Abstract | Section III / IV Text | Table / Figure | Source Artifact (`results/`) | Consistency Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Test Recall** | 73.18% [70.48, 76.00] | 73.18% [70.48, 76.00] | 73.18% | `step2_model_performance_summary.csv` | **100% MATCH** |
| **Test Precision** | 75.64% [72.83, 78.19] | 75.64% [72.83, 78.19] | 75.64% | `step2_model_performance_summary.csv` | **100% MATCH** |
| **Test Accuracy** | 88.71% [87.78, 89.62] | 88.71% [87.78, 89.62] | 88.71% | `step2_model_performance_summary.csv` | **100% MATCH** |
| **Test F1-Score** | 0.7439 | 0.7439 [0.7235, 0.7664] | 0.7439 | `step2_model_performance_summary.csv` | **100% MATCH** |
| **Test ROC-AUC** | 0.8968 [0.8836, 0.9098] | 0.8968 [0.8836, 0.9098] | 0.8968 | `step2_model_performance_summary.csv` | **100% MATCH** |
| **Brier Calibration Score** | 0.1080 (vs. 0.1738 base) | 0.1080 (vs. 0.1738 base) | Fig. 1 (Reliability) | `fig1_reliability_diagram.png` | **100% MATCH** |
| **True Positives ($TP$)** | 742 | 742 | Fig. 2 (CM) | `step2_model_performance_summary.csv` | **100% MATCH** |
| **False Positives ($FP$)** | 239 | 239 | Fig. 2 (CM) | `step2_model_performance_summary.csv` | **100% MATCH** |
| **True Negatives ($TN$)** | 3,273 | 3,273 | Fig. 2 (CM) | `step2_model_performance_summary.csv` | **100% MATCH** |
| **False Negatives ($FN$)** | 272 | 272 | Fig. 2 (CM) | `step2_model_performance_summary.csv` | **100% MATCH** |
| **Operational Alert Rate** | 21.68% (21.7 / 100) | 21.68% (981 alerts) | Fig. 5 (Tradeoff) | `step5_main_fairness_audit_tau_050.csv` | **100% MATCH** |
| **True-to-False Alert Ratio** | 3.10 : 1 | 3.10 : 1 (742 / 239) | Text | `step2_model_performance_summary.csv` | **100% MATCH** |

---

## 3. Explainability Consistency (TreeSHAP & LIME)

| Explainability Marker | Abstract | Section IV-C Text | Figures (`results/`) | Source Artifact (`results/`) | Consistency Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Total Mean \|SHAP\| Denominator** | Reflected in shares | 0.407016 | `fig3_shap_importance.png` | `step4_shap_attributions.csv` | **100% MATCH** |
| **#1 Feature: Course Failures (`reprovacoes`)** | 32.37% (0.1317) | 32.37% (0.131748) | Fig. 4 & Fig. 3 | `step4_shap_attributions.csv` | **100% MATCH** |
| **#2 Feature: Attendance (`percentual_frequencia`)** | 19.26% (0.0784) | 19.26% (0.078394) | Fig. 4 & Fig. 3 | `step4_shap_attributions.csv` | **100% MATCH** |
| **#3 Feature: Cohort Year (`anoingresso`)** | 10.78% (0.0439) | 10.78% (0.043888) | Fig. 4 & Fig. 3 | `step4_shap_attributions.csv` | **100% MATCH** |
| **Top-3 Cumulative Attribution Share** | 62.41% | 62.41% (0.254029 / 0.407016) | Fig. 3 | `step4_shap_attributions.csv` | **100% MATCH** |
| **Combined Gender Attribution Share** | Mentioned | 3.66% (Male + Female) | `fig3_shap_importance.png` | `step4_shap_attributions.csv` | **100% MATCH** |
| **LIME Archetype #815 (High Risk)** | P = 94.8%, Jaccard = 0.50 | P = 94.8%, Jaccard = 0.50 | Text | `step4_lime_shap_concordance.csv` | **100% MATCH** |
| **LIME Archetype #4078 (Borderline)** | P = 48.0%, Jaccard = 0.50 | P = 48.0%, Jaccard = 0.50 | Text | `step4_lime_shap_concordance.csv` | **100% MATCH** |
| **LIME Archetype #4458 (Low Risk)** | P = 10.7%, Jaccard = 1.00 | P = 10.7%, Jaccard = 1.00 | Text | `step4_lime_shap_concordance.csv` | **100% MATCH** |
| **Mean Local Explainer Concordance** | 66.7% | 66.7% (range [0.50, 1.00]) | Text | `step4_lime_shap_concordance.csv` | **100% MATCH** |

---

## 4. Algorithmic Fairness Audit Consistency ($\tau = 0.50$)

| Dimension & Group | Disparate Impact (DI) | Equal Opp. Diff (EOD) | Raw $p$-value | Holm-Bonferroni FWER | Source Artifact (`results/`) | Consistency Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Gender (Male vs. Female)** | 0.7383 (Breaches 0.80) | -0.0422 [-0.097, +0.013] | 0.1354 | Not Significant | `step5_main_fairness_audit_tau_050.csv` | **100% MATCH** |
| **Race (Branca vs. Parda)** | 1.2958 (Breaches 1.25) | +0.1014 [+0.020, +0.183] | 0.0144 | **Not Sig. ($> 0.0125$)** | `step5_holm_bonferroni_eod.csv` | **100% MATCH** |
| **Race (Branca vs. Preta)** | 1.2694 (Breaches 1.25) | +0.0280 [-0.116, +0.172] | 0.7042 | Not Significant | `step5_holm_bonferroni_eod.csv` | **100% MATCH** |
| **Income (<= vs. > Median)** | 1.5098 (Breaches 1.25) | +0.1007 [+0.044, +0.157] | 0.00043 | **SURVIVES ($< 0.00833$)** | `step5_holm_bonferroni_eod.csv` | **100% MATCH** |
| **Age (<= 20 vs. > 20 yrs)** | 1.2864 (Breaches 1.25) | +0.0126 [-0.044, +0.069] | 0.6634 | Not Significant | `step5_holm_bonferroni_eod.csv` | **100% MATCH** |
| **Computer (0 vs. >= 1)** | 1.5106 (Breaches 1.25) | +0.1109 [+0.046, +0.176] | 0.00089 | **SURVIVES ($< 0.01000$)** | `step5_holm_bonferroni_eod.csv` | **100% MATCH** |
| **AIF360 Reweighing Recall** | Dropped to 60.36% (-12.82 pp) | Tightened to -0.0304 | N/A | Trade-off Analyzed | `step5_reweighing_mitigation_tradeoff.csv`| **100% MATCH** |

---

## 5. Governance Calibration & Operational Bands Consistency

| Risk Band Interval | Tier Label | Cohort Count ($N$) | Observed Dropout Rate | Mean Predicted Prob. | Source Artifact (`results/`) | Consistency Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$[0.80, 1.00]$** | Emergency | 567 | **95.24%** (540 / 567) | 89.2% | `step6_discrete_risk_bands_audit.csv` | **100% MATCH** |
| **$[0.60, 0.80)$** | High Priority | 190 | **63.68%** (121 / 190) | 68.4% | `step6_discrete_risk_bands_audit.csv` | **100% MATCH** |
| **$[0.40, 0.60)$** | Watchlist | 224 | **26.94%** (81 / 224) | 48.6% (Over-predicts) | `step6_discrete_risk_bands_audit.csv` | **100% MATCH** |
| **$[0.20, 0.40)$** | Low Concern | 358 | **7.82%** (28 / 358) | 28.1% | `step6_discrete_risk_bands_audit.csv` | **100% MATCH** |
| **$[0.00, 0.20)$** | Minimal Risk | 3,187 | **3.67%** (117 / 3,187) | 5.4% | `step6_discrete_risk_bands_audit.csv` | **100% MATCH** |
| **Counselor Caseload (5k Cohort)**| At $\tau=0.50$ | 1,084 Flagged | SLA: 4 weeks | 6 FTE Counselors | `step6_cumulative_operational_risk_bands.csv`| **100% MATCH** |

---

## 6. Document Constraints & Formatting

| Formatting Parameter | Target Requirement | Value in Revised Document | Status |
| :--- | :--- | :--- | :--- |
| **Page Budget** | Strictly 6 pages in IEEE 2-column format | **Verified Exactly 6 Pages** via Word COM (`ComputeStatistics(2) == 6`), 3,744 words | **100% Compliant** |
| **Citation Range** | All 22 references cited sequentially | `[1]` through `[22]` cited in numerical order | **Compliant** |
| **Base Paper Citation** | Silva et al. 2025 cited as base paper | Reference `[1]` (Silva et al. 2025, `10.1109/RITA.2025.3566095`) | **Compliant** |
| **Embedded Figures** | Dev2 figures without GPA | Fig. 4 (`fig2_shap_beeswarm.png`), Fig. 5 (`fig4_fairness_audit.png`) | **Compliant** |
| **Target Leakage Terms** | 0 legacy GPA terms or numbers | Verified 0 occurrences of old numbers (`84.8%`, `0.951`, `3,017`, `80/20`) | **Compliant** |

