# Comprehensive Response to Reviewer Comments & Suggestions (dev2 Pipeline Re-Benchmarking)

**Manuscript Title:** An Explainable and Fairness-Audited AI Governance Framework for Student Dropout Prediction  
**Base Benchmark:** Silva et al., *IEEE Revista Iberoamericana de Tecnologias del Aprendizaje (RITA)* (2025), doi: [10.1109/RITA.2025.3566095](https://doi.org/10.1109/RITA.2025.3566095)  
**Evaluation Cohort:** 15,084 Secondary Technical Education Students (IFNMG Administrative Database)  
**Partition Vault:** 70/30 Stratified Split ($N_{train} = 10,558$, $N_{test} = 4,526$ Held-Out Unseen Students; 1,014 Dropouts, 3,512 Completers)  
**Methodological Evolution:** Complete architectural remediation eliminating retrospective cumulative GPA (`ira`) target leakage (`dev2` pipeline).

---

## Executive Summary of Major Architectural Remediation

In our initial submission (`main` branch), we attempted to justify the inclusion of cumulative GPA (`ira`) under the assumption that it represented a first-year intake milestone. However, following the reviewer's incisive questions regarding temporal granularity and data leakage (Comments #10, #20, #28, #63), we conducted a rigorous feature timing audit. This audit revealed that in the cross-sectional institutional database (`dataset_evasao_MDE.xlsx`), `ira` and course failures (`reprovacoes`) are cumulative totals computed across students' entire multi-year tenures, making the inclusion of `ira` a severe source of retrospective target leakage.

Rather than defending a fragile construct, we executed a complete methodological overhaul:
1. **Target Leakage Remediation:** We **completely eliminated cumulative GPA (`ira`)** from the feature set.
2. **Leak-Free Partition & 10-Fold CV:** We instituted a 70/30 stratified partition ($N_{train} = 10,558$, $N_{test} = 4,526$) and wrapped all resampling, feature selection, and transformations inside cross-validation training folds using `imblearn.pipeline.Pipeline`, preserving natural 22.4% prevalence in validation folds.
3. **Transparent Benchmark Reporting:** The leak-free Random Forest champion achieves **73.18% Recall, 75.64% Precision, 88.71% Accuracy, 0.8968 ROC-AUC, and 0.1080 Brier Score** on the held-out test cohort ($N=4,526$).
4. **Honest Explanations & Fairness:** Explainability shifts from GPA to academic friction (course failures 32.37%, attendance 19.26%). Algorithmic fairness audits evaluate 5 axes with Holm-Bonferroni FWER control, proving that socioeconomic gaps survive while demonstrating that AIF360 Reweighing induces an unviable 12.82 percentage point recall penalty ($73.18\% \rightarrow 60.36\%$).
5. **Normative Governance Charter:** Explicitly labeled as a proposed design (not field-tested in live operations), featuring heuristic risk bands and Brazilian LGPD Art. 20 appeal rights.

---

## Part 1: Quantitative Artifacts from dev2 Pipeline

All results and metrics in the revised paper and this response sheet are directly verified against empirical code executions in the `results/` directory:

| Component | Code & Output Artifact | Key Empirical Finding |
| :--- | :--- | :--- |
| **1. Feature Granularity & Timing** | `step1_feature_timing.md`, `run_step1_step2.py` | Documented multi-year cumulative nature of `reprovacoes` (max 69) and `percentual_frequencia`; justified complete removal of `ira`. |
| **2. Leak-Free Model Selection** | `step2_model_performance_summary.csv`, `step2_candidate_models_comparison.csv` | RF Champion: Recall 73.18% [0.7048, 0.7600], Precision 75.64% [0.7283, 0.7819], Accuracy 88.71%, ROC-AUC 0.8968, Brier 0.1080. |
| **3. Test Confusion Matrix** | `step2_model_performance_summary.csv` | $N=4,526$: $TP=742$, $FP=239$, $TN=3,273$, $FN=272$. Alert rate: 21.68% (21.7 / 100 students). True-to-False alert ratio: 3.10:1. |
| **4. Baselines Comparison** | `step2_model_performance_summary.csv` | Majority class: 77.60% accuracy, 0.0% recall. Attendance $\le 91\%$: Recall 32.15%, Precision 63.92%, continuous ROC-AUC 0.5945. |
| **5. TreeSHAP Attribution** | `step4_shap_attributions.csv`, `fig2_shap_beeswarm.png`, `fig3_shap_importance.png` | Total mean \|SHAP\| denominator = 0.407016. Course failures: 32.37%, Attendance: 19.26%, Cohort Year: 10.78%. Top-3 share = 62.41%. |
| **6. LIME-SHAP Concordance** | `step4_lime_shap_concordance.csv` | 3 archetypes (#815 High Risk, #4078 Borderline, #4458 Low Risk). Mean top-3 Jaccard overlap = 66.7% (moderate agreement). |
| **7. 5-Axis Fairness Audit** | `step5_main_fairness_audit_tau_050.csv`, `fig4_fairness_audit.png` | $\tau=0.50$: Gender DI 0.7383 (EOD -0.0422, $p=0.1354$). Race Branca vs Parda DI 1.2958 ($p=0.0144$). Income DI 1.5098 ($p=0.00043$). Computer DI 1.5106 ($p=0.00089$). |
| **8. Holm-Bonferroni Correction** | `step5_holm_bonferroni_eod.csv` | Income ($p=0.00043 < 0.00833$) and Computer Ownership ($p=0.00089 < 0.01000$) survive; Race Branca vs Parda ($0.0144 > 0.0125$) does not. |
| **9. Debiasing Trade-off** | `step5_reweighing_mitigation_tradeoff.csv` | AIF360 Reweighing drops recall by 12.82 percentage points ($73.18\% \rightarrow 60.36\%$, missing 130 additional dropouts). |
| **10. Risk Bands Calibration** | `step6_discrete_risk_bands_audit.csv`, `fig5_risk_bands_calibration.png` | Emergency $[0.80, 1.00]$: 95.24% observed dropout; High Priority $[0.60, 0.80)$: 63.68%; Watchlist $[0.40, 0.60)$: 26.94% (inflation noted). |
| **11. Operational SLA** | `step6_cumulative_operational_risk_bands.csv` | 5,000 student cohort flags 1,084 students at $\tau=0.50$, requiring 6 counselors for a 4-week response SLA. |

---

## Part 2: Point-by-Point Responses to Reviewer Suggestions

### Section 1: Title & Framing
* **Comment #1 & #2:** Clarify outcome is student dropout prediction; avoid implying an implemented institutional system.
  - **Response:** Revised title squarely to *"An Explainable and Fairness-Audited AI Governance Framework for Student Dropout Prediction"*. We explicitly frame the governance framework as a proposed design that has not been field-tested in live operations throughout Abstract, Intro, Results, and Limitations.

### Section 2: Abstract & Performance Reporting
* **Comment #5, #6, #7:** Distinguish empirical phases from untested governance; report exact data source, split, and metrics; state gender disparity without claiming other differences are harmless.
  - **Response:** The Abstract now explicitly reports: 15,084 secondary technical records from IFNMG, 70/30 stratified split (10,558 train, 4,526 test), complete exclusion of GPA (`ira`), Random Forest champion metrics with 95% CIs (Recall 73.18%, Precision 75.64%, Accuracy 88.71%, ROC-AUC 0.8968, Brier 0.1080), TreeSHAP attributions (failures 32.37%, attendance 19.26%, top-3 62.41%), fairness audit with Holm-Bonferroni correction (confirming Income $p=0.00043$ and Computer $p=0.00089$ sensitivity gaps), Reweighing recall penalty (12.82 pp), and explicitly disclaims field-testing of the proposed governance charter.

### Section 3: Introduction & Research Questions
* **Comment #9, #10, #11, #12:** Define research gap as operational integration; clarify prediction time without pre-enrollment claims; state explicit RQs; distinguish SDG motivation from progress.
  - **Response:** Paragraphs 19–24 now define the research gap strictly as operational integration and empirical evaluation of explanations, group fairness, and human oversight. We eliminated "pre-enrollment" claims, explicitly formulated 4 research questions (RQ1 Predictive Utility, RQ2 Explanation Consistency, RQ3 Group Fairness, RQ4 Governance Feasibility), and stated that SDG 4 and SDG 10 serve strictly as conceptual motivation.

### Section 4: Literature Review & Table I
* **Comment #14, #15, #16, #17:** Acknowledge Silva et al. [1] use of SHAP/LIME; make Table I compare verifiable evidence; explain why DI, EOD, and calibration conflict.
  - **Response:** Section II explicitly credits Silva et al. [1] for using RF with SHAP/LIME on 15,084 IFNMG records, but highlights their lack of algorithmic fairness audits and operational governance. Table I has been updated with clean columns, including a comparative row for "This Work". We cite Kleinberg's impossibility theorem ([15]) and explain why base rate differences (19.0% vs 25.8%) prevent simultaneous demographic parity and equalized odds, justifying our prioritization of Equal Opportunity ([21]) while using DI ([20]) as an administrative screening heuristic.

### Section 5: Dataset & Leakage Controls
* **Comment #19, #20, #21, #22, #23:** Document dataset access, cohort dates, exclusion counts; explain how 48,311 becomes 15,084; address grouping of transfers/expulsions; reconcile subsets.
  - **Response:** Section III-A documents IFNMG enrollment data (`dataset_evasao_MDE.xlsx`) with author confirmation placeholders (`[AUTHOR TO CONFIRM: Dataset URL & License]`, `[AUTHOR TO CONFIRM: Cohort date range]`). We detail the two-stage filter: excluding 12,038 higher-ed records and 21,189 active ongoing students to yield 15,084 terminal technical students across 4 modalities. We acknowledge grouping voluntary dropout (1,760), cancellation (446), dismissal (346), jubilated status (38), and transfers (791) into Class 1 as an administrative necessity and document it in Limitations. The arbitrary "2,722 active" subset was removed: all evaluations strictly use the held-out 4,526 test partition.

### Section 6: Methodology & Cross-Validation
* **Comment #25, #26, #27, #28, #29:** Reproducible 48-experiment grid; resolve 5-fold vs 10-fold CV ambiguity; fit all transforms inside training folds; define risk bands.
  - **Response:** Section III-B describes the 48-condition factorial grid (4 balancing x 3 feature selection x 4 classifiers). We clarify that 10-fold CV evaluated training stability using `imblearn.pipeline.Pipeline`, executing winsorization, imputation, one-hot encoding, feature selection, and resampling strictly inside each training fold, with validation folds evaluated at natural 22.4% prevalence. Selection followed the constrained utility rule: maximize Recall subject to Precision $\ge 60\%$ and ROC-AUC $\ge 0.90$. Risk bands are defined as heuristic triage intervals (<0.20, 0.20-0.40, 0.40-0.60, 0.60-0.80, >=0.80).

### Section 7: Experimental Setup & Baselines
* **Comment #31, #32, #33, #34, #35:** Report confusion matrix and positive counts on held-out test set; add majority-class and attendance baselines; assess probability calibration.
  - **Response:** Section IV-B reports exact confusion matrix on 4,526 test cases: $TP=742$, $FP=239$, $TN=3,273$, $FN=272$. Baselines confirm machine learning necessity: majority-class baseline yields 77.60% accuracy but 0.0% recall; attendance-only baseline ($\le 91\%$) captures only 32.15% of dropouts (Precision 63.92%, continuous ROC-AUC 0.5945). Probability calibration was audited via Brier score (0.1080 vs 0.1738 baseline) and a 10-bin reliability diagram.

### Section 8: Model Selection & Utility Trade-offs
* **Comment #37, #38, #39, #41:** Explain why SVM was rejected despite higher recall; define utility rule; check RF metrics against prevalence; distinguish correlation from causation.
  - **Response:** Section IV-B explains that while Linear SVM with SMOTEENN reached 60.55% recall, precision collapsed to 45.08% (generating 54.9% false alarms, saturating counseling capacity). Decision Tree reached 75.05% recall but lower precision (67.05%) and CV ROC-AUC (0.8875 < 0.90). The Random Forest uniquely satisfied the utility rule (CV Recall 74.95%, Precision 76.94%, ROC-AUC 0.9144). At $\tau=0.50$, counselor workload is 21.7 alerts per 100 students with a favorable 3.10:1 true-to-false alert ratio.

### Section 9: Explainability (TreeSHAP & LIME)
* **Comment #43, #44, #45, #46, #47:** Specify SHAP output scale (probability) and class explained; recalculate attribution shares with denominator; reconcile SHAP-LIME concordance; add stability analysis.
  - **Response:** Section IV-C specifies TreeSHAP evaluated on probability scale over 800 background training instances explaining Class 1 (dropout). Total mean |SHAP| denominator is explicitly reported as 0.407016. Attributions: course failures (32.37%), attendance (19.26%), cohort year (10.78%), summing to 62.41% top-3 share. Local LIME vs SHAP concordance was audited across 3 archetypes (#815, #4078, #4458) with mean Jaccard overlap of 66.7%, framed as qualitative illustrations without claiming proof of ground-truth explanation.

### Section 10: Fairness Audit & Mitigation
* **Comment #49, #50, #51, #52, #53, #54:** Define protected/reference groups, selection rates, and CIs; distinguish DI, SPD, EOD; investigate gender and multiple-testing; evaluate debiasing; present Four-Fifths rule as screening heuristic.
  - **Response:** Section IV-D audits 5 axes at $\tau=0.50$ under the Four-Fifths screening heuristic (0.80 $\le$ DI $\le$ 1.25) [20]. Gender exhibits DI = 0.7383 (female recall 70.87% [331/467] vs male 75.09% [410/546], EOD = -0.0422, $p=0.1354$). Applying Holm-Bonferroni FWER control across 6 demographic EOD $p$-values reveals that Race Branca vs Parda ($p=0.0144$) does not survive ($\alpha/4 = 0.0125$), while Household Income ($p=0.00043$) and Computer Ownership ($p=0.00089$) remain statistically significant. AIF360 Reweighing drops recall by 12.82 percentage points ($73.18\% \rightarrow 60.36\%$), demonstrating that debiasing alone is insufficient and justifying human-in-the-loop governance.

### Section 11: Institutional Governance Framework
* **Comment #56, #57, #58, #59, #60:** Label charter as proposed design; provide workflow; define LGPD rights, retention, and appeal timelines; explain semi-annual cadence.
  - **Response:** Section IV-E details the proposed 5-pillar charter (not field-tested): advisory non-punitive deployment, explainability-coupled outreach, semi-annual audits with drift triggers, LGPD Art. 20 [22] appeal rights (10-business-day review timeline), and unilateral counselor override authority. For a 5,000 student cohort, 1,084 flags require 6 counselors to fulfill a 4-week response SLA.

### Section 12: Limitations & Threats to Validity
* **Comment #62, #63, #64, #65:** Organize limitations by provenance, label construct, measurement window, subgroup uncertainty, external validity, and untested governance.
  - **Response:** Section V organizes limitations into 6 distinct categories: (1) Data Provenance (IFNMG, active student right-censoring), (2) Label Construct (grouping transfers/expulsions), (3) Cumulative Feature Measurement Window (cumulative multi-year features prevent first-year-only early warning), (4) Subgroup Uncertainty, (5) External Validity (single Brazilian network vs Indian institutions), and (6) Untested Governance (proposed operational blueprint).

### Section 13 & 14: IEEE Presentation & References
* **Comment #71, #72, #73, #74, #75:** Enlarge figure labels; verify percentages against source outputs; correct duplicate reference numbering and malformed refs; standardize terminology.
  - **Response:** Replaced Fig. 4 with `results/fig2_shap_beeswarm.png` and Fig. 5 with `results/fig4_fairness_audit.png`. All 22 references are cited sequentially in IEEE format, with Kleinberg cited as [15], Lundberg & Lee as [12], Hardt et al. as [21], and Brasil LGPD as [22]. Terminology standardized to "semi-annual", "disparate impact", and "Equal Opportunity Difference".
