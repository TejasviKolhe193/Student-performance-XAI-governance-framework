# Change Log: Research Paper Revision (dev2 Pipeline & Review Suggestions)

This document provides a systematic line-by-line record of all modifications made to the research paper draft (`paper_review/research_paper_final_draft.docx` and `paper_review/research_paper_final_with_updates.docx`). 

All updates strictly reflect the **`dev2` empirical pipeline** (complete removal of retrospective cumulative GPA `ira` target leakage, 70/30 stratified train/test split) and incorporate all applicable recommendations from the mentor's review document (`AI_Governance_Review_Suggestions.docx`).

---

## Summary of Major Global Shifts

| Dimension | Old Paper Draft (`main` branch) | Revised Paper Draft (`dev2` branch) | Reviewer Comment / Motivation |
| :--- | :--- | :--- | :--- |
| **Target Leakage** | Included retrospective cumulative GPA (`ira`) accumulated across whole enrollment. | **Completely eliminated GPA (`ira`)**. Restricts predictors strictly to baseline administrative & academic friction features. | Comment #10, #20, #28: Prevents retrospective target leakage. |
| **Data Partition** | 80/20 train/test split ($N_{train} = 12,067$, $N_{test} = 3,017$). | **70/30 stratified split** ($N_{train} = 10,558$, $N_{test} = 4,526$). | Comment #6, #31: Larger held-out test cohort ($N=4,526$) for tighter bootstrap CIs. |
| **Champion Model Metrics** | RF: Recall 84.8%, Precision 83.6%, ROC-AUC 0.951. | **RF: Recall 73.18%, Precision 75.64%, ROC-AUC 0.8968, Accuracy 88.71%, Brier 0.1080**. | Comment #6, #31, #39: Honest leak-free generalization on test set ($N=4,526$). |
| **Top Predictors (SHAP)** | GPA (52.8%), Attendance (10.4%), Failures (8.1%). Top-3 = 71.3%. | **Course Failures (32.37%), Attendance (19.26%), Cohort Year (10.78%)**. Top-3 = **62.41%**. | Comment #43, #44: Recomputed total |SHAP| denominator ($0.407016$) and exact shares without GPA. |
| **LIME-SHAP Concordance** | Vague claim of 72.4% on 100 archetypes; Student #37 contradictory. | **3 representative archetypes (#815, #4078, #4458) evaluated qualitatively; Mean Jaccard = 66.7%**. | Comment #45, #46: Reconciled archetype recourse; framed as qualitative illustrations without claiming proof of ground-truth explanation. |
| **Fairness & Multiple Testing** | Only raw DI / EOD reported; claimed all non-gender differences benign. | **5 protected axes audited at $\tau=0.50$; Holm-Bonferroni FWER control on EOD $p$-values**. | Comment #7, #49, #52, #53: Income ($p=0.00043$) and Computer ($p=0.00089$) survive; Race Branca vs Parda ($p=0.0144$) does not. |
| **Debiasing Mitigation** | Post-hoc threshold tuning mentioned without validation set. | **AIF360 Reweighing evaluated: drops recall by 12.82 pp ($73.18\% \rightarrow 60.36\%$)**. | Comment #53: Rigorous trade-off analysis proving debiasing alone is insufficient. |
| **Governance Framing** | Framed as implemented framework. | **Explicitly labeled as proposed operational design (not field-tested in live operations)**. | Comment #3, #5, #56: Scientific modesty; LGPD Art. 20 appeals, 4-week SLA. |

---

## Detailed Section-by-Section Changes

### 1. Title & Abstract
- **Location:** Paragraph 0 & Paragraph 17
- **Old Text:**
  - *Title:* "An Explainable and Fairness-Audited AI Governance Framework for Student Dropout Prediction"
  - *Abstract:* "...Using public administrative data from the Brazilian Federal Institutes (IFMA... N=15,084... 80/20 stratified split (12,067 training, 3,017 held-out test students). The model achieves 84.8% recall... 83.6% precision... 0.951 ROC-AUC... first-year GPA, attendance, and failed courses account for 71.3%... Disparate Impact 0.707..."
- **New Text:**
  - *Title:* Kept clear and focused: "An Explainable and Fairness-Audited AI Governance Framework for Student Dropout Prediction".
  - *Abstract:* "...Using 15,084 secondary technical student records from the Instituto Federal do Norte de Minas Gerais (IFNMG) partitioned via a 70/30 stratified split (10,558 training, 4,526 held-out test), we evaluated 48 pipeline configurations without retrospective GPA (ira), strictly eliminating target leakage. A Random Forest model with Random Under-Sampling and Tree Feature Importance (k=19) was selected as champion, achieving Recall of 73.18% (95% CI: [70.48%, 76.00%]), Precision of 75.64% (95% CI: [72.83%, 78.19%]), Accuracy of 88.71% (95% CI: [87.78%, 89.62%]), ROC-AUC of 0.8968 (95% CI: [0.8836, 0.9098]), and Brier Score of 0.1080 (baseline 0.1738). TreeSHAP feature attribution identified course failures (reprovacoes, 32.37%), attendance percentage (percentual_frequencia, 19.26%), and enrollment cohort year (anoingresso, 10.78%) as primary drivers, accounting for 62.41% of total attribution. Local LIME surrogates demonstrated moderate agreement with SHAP across student archetypes (mean top-3 Jaccard overlap 66.7%). Algorithmic fairness audits across five protected dimensions (Gender, Race, Household Income, Age, and Home Computer Ownership) under the Four-Fifths screening heuristic revealed gender disparity (Disparate Impact 0.7383, female recall 70.87% vs. male 75.09%, Equal Opportunity Difference -0.0422, p=0.1354) and statistically significant socioeconomic True Positive Rate gaps on Income (p=0.00043) and Computer Ownership (p=0.00089) under Holm-Bonferroni correction. Pre-processing AIF360 Reweighing tightened Equal Opportunity but induced an acute 12.82 percentage point drop in recall (73.18% to 60.36%). Consequently, we propose a non-punitive operational governance charter incorporating role-based access control, semi-annual audits, heuristic risk bands, and Brazilian LGPD Art. 20 contestability rights. This governance framework represents a proposed design that has not been field-tested in live operations."
- **Reason:** Mentors' Comments #2, #3, #5, #6, #7, #10.

---

### 2. Section I: Introduction
- **Location:** Paragraphs 19–24
- **Old Text:** Framed dropout prediction as "first-year early warning dropout screening tool"; SDG alignment asserted without operational distinction; claimed invention of workflow.
- **New Text:**
  - Paragraph 19: Clarified SDG alignment as conceptual institutional motivation rather than empirical progress metric. Identified 22.4% baseline attrition at IFNMG.
  - Paragraph 20: Explicitly documented that administrative GPA is computed retrospectively and induces severe target leakage; clarified that without GPA, the model operates on administrative and academic friction indicators prior to terminal departure.
  - Paragraph 21: Explicitly disclaimed inventing a novel classifier; defined the research gap strictly as operational integration and empirical evaluation of explanations, group fairness, and human oversight.
  - Paragraph 22: Added 4 explicit research questions (RQ1 Predictive Utility, RQ2 Explanation Consistency, RQ3 Group Fairness, RQ4 Governance Feasibility).
  - Paragraph 23: Replaced contributions list with exact `dev2` numbers: 48-experiment benchmark without GPA, Random Forest champion (73.18% recall, 0.8968 ROC-AUC), TreeSHAP/LIME top-3 share (62.41%), Holm-Bonferroni fairness audit, and proposed 5-pillar charter.
- **Reason:** Mentors' Comments #8, #9, #10, #11, #12.

---

### 3. Section II: Literature Review & Table I
- **Location:** Paragraphs 26–27 & Table 0
- **Old Text:** Generic summary; claimed prior work lacked explainability even though Silva et al. used SHAP/LIME; miscited Kleinberg as [14]; Table I had 11 rows with pipe characters in cells.
- **New Text:**
  - Paragraph 26: Acknowledged Silva et al. [1] used RF with SHAP/LIME on IFNMG data, but omitted fairness audits and governance. Cited Kleinberg's impossibility theorem properly as [15]. Explained mathematical tension between DI, EOD, and calibration when base rates differ (19.0% vs 25.8%), justifying prioritization of Equal Opportunity [21] while using DI [20] as an administrative screening heuristic.
  - Table I: Added Row 12 for "This Work", comparing IFNMG dataset (N=15,084), RF model (Recall 73.2%, AUC 0.90), TreeSHAP & LIME (62.4% Top-3 share), 5-axis fairness audit with Holm-Bonferroni, and 5-pillar proposed governance charter under LGPD Art. 20.
- **Reason:** Mentors' Comments #14, #15, #16, #17, #74.

---

### 4. Section III: Methodology
- **Location:** Paragraphs 29–42
- **Old Text:** Claimed 80/20 split; mentioned "2,722 active, non-zero GPA" subset; incomplete description of CV and nesting.
- **New Text:**
  - Paragraph 29: Overview of 5-phase leak-free workflow without GPA.
  - Paragraph 32: Documented dataset provenance: IFNMG (`dataset_evasao_MDE.xlsx`), 48,311 initial records filtered across 4 secondary technical modalities (Integrado 10,076, Concomitante 1,777, Subsequente 2,746, Integrado EJA 485) yielding 15,084 records. Target: Completed (11,703, 77.59%) vs Dropout/Non-completion (3,381, 22.41%). Grouping transfers/expulsions acknowledged as administrative necessity. Added author placeholders `[AUTHOR TO CONFIRM: Dataset URL & License]` and `[AUTHOR TO CONFIRM: Cohort date range]`.
  - Paragraph 33: Stratified 70/30 split (10,558 training, 4,526 test). GPA completely excluded. 19 baseline features, median imputation for missing digital access (computers 6.17%, notebooks 5.20%). Winsorization and one-hot encoding fitted strictly inside training folds.
  - Paragraph 35: 48-experiment factorial grid (4 balancing x 3 feature selection x 4 classifiers). Resampling, scaling, and feature selection inside 10-fold CV using `imblearn.pipeline.Pipeline`, keeping validation folds at natural 22.4% prevalence. Selection rule: highest Recall subject to Precision >= 60% and ROC-AUC >= 0.90 on CV folds. Citing Breiman [18], Chawla et al. [16], Batista et al. [17].
  - Paragraph 36: Bootstrap 95% CIs (1,000 iterations) on 4,526 test cohort.
  - Paragraph 38: TreeSHAP [12], [19] on probability scale over 800 background training instances explaining Class 1. Local LIME [13] on 3 representative archetypes.
  - Paragraph 40: 5 protected dimensions audited under Four-Fifths screening heuristic (0.80 <= DI <= 1.25) [20], SPD, EOD [21], Holm-Bonferroni FWER control, and AIF360 Reweighing [14].
  - Paragraph 42: Proposed governance policy charter (not field-tested) with RBAC, semi-annual audits, heuristic risk bands, and Brazilian LGPD Art. 20 [22] appeal rights.
- **Reason:** Mentors' Comments #19, #20, #21, #22, #25, #26, #27, #28, #29.

---

### 5. Section IV: Results and Discussion
- **Location:** Paragraphs 44–76
- **Old Text:** Reported 3,017 test students, 84.8% recall, 83.6% precision, 0.951 AUC; GPA 52.8% attribution; female DI 0.707; Student #37 with GPA 7.12 / 1.92 contradiction; Brier score 0.0526.
- **New Text:**
  - Paragraph 44 & 46: Test cohort $N=4,526$ (3,512 Class 0, 1,014 Class 1, 22.40% prevalence).
  - Paragraph 47: Modality attrition verified (Integrado EJA 42.8%, Subsequente 30.1%, Concomitante 24.7%, Integrado 18.6%).
  - Paragraph 50: Attendance cliff (<75% legal minimum) and failure accumulation (dropouts average 5.99 failures vs 0.77 for completers).
  - Paragraph 54: Random Forest champion: Test Recall 73.18% (95% CI: [70.48%, 76.00%]), Precision 75.64% (95% CI: [72.83%, 78.19%]), F1 0.7439, Accuracy 88.71%, ROC-AUC 0.8968 (95% CI: [0.8836, 0.9098]), Brier score 0.1080 (vs baseline 0.1738). Confusion matrix: TP=742, FP=239, TN=3,273, FN=272. Baselines: Majority class (77.60% acc, 0% recall), Attendance <= 91% (Recall 32.15%, Precision 63.92%, continuous ROC-AUC 0.5945).
  - Paragraph 55: Alternative models: DT (Recall 75.05%, Precision 67.05%, CV AUC 0.8875 < 0.90), SVM SMOTEENN (Recall 60.55%, Precision 45.08%).
  - Paragraph 57: TreeSHAP attributions: total mean |SHAP| denominator = 0.407016. Course failures (`reprovacoes`, 32.37%), attendance percentage (`percentual_frequencia`, 19.26%), cohort year (`anoingresso`, 10.78%). Top-3 cumulative share = 62.41% (0.254029 / 0.407016). Gender combined share = 3.66%.
  - Paragraph 58: Beeswarm directional dynamics updated (high failures drive risk; high attendance protects).
  - Paragraph 62: Local LIME vs TreeSHAP across 3 archetypes: High-Risk #815 (P=94.8%, Jaccard 0.50), Borderline #4078 (P=48.0%, Jaccard 0.50), Low-Risk #4458 (P=10.7%, Jaccard 1.00). Mean Jaccard = 66.7% (moderate agreement).
  - Paragraph 63: Replaced contradictory student #37 text with detailed recourse profiles for students #815, #4078, and #4458.
  - Paragraph 65: Fairness audit at $\tau=0.50$: Four-Fifths heuristic flags Gender (DI 0.7383), Race (Parda 1.2958, Preta 1.2694), Income (1.5098), Age (1.2864), Computer (1.5106). Modest FPR gaps (+2.76% low income, +2.75% no computer).
  - Paragraph 70: Equal Opportunity (EOD) and Holm-Bonferroni: Gender EOD = -0.0422 (p=0.1354). Race Branca vs Parda raw p=0.0144 does not survive adjusted threshold (alpha/4 = 0.0125). Income (p=0.00043) and Computer Ownership (p=0.00089) survive.
  - Paragraph 71: Mitigation tradeoff: Reweighing drops recall by 12.82 percentage points (73.18% to 60.36%, missing 130 dropouts). Algorithmic debiasing alone is insufficient.
  - Paragraph 72: Operational triage workload: at tau=0.50, 981 students flagged out of 4,526 (21.68%, or 21.7 alerts per 100 students). True-to-False alert ratio is 3.10:1 (742 TP to 239 FP).
  - Paragraph 75: Probability calibration & Heuristic Risk Bands: Brier score 0.1080. Emergency [0.80, 1.00] flags 567 (95.24% observed dropout), High Priority [0.60, 0.80) flags 190 (63.68%), Watchlist [0.40, 0.60) flags 224 (26.94%), Low Concern [0.20, 0.40) flags 358 (7.82%), Minimal [0.00, 0.20) flags 3,187 (3.67%). UnderSampling probability inflation documented in Watchlist band.
  - Paragraph 76: Proposed Governance Charter (not field-tested): 5 normative pillars, RBAC, semi-annual audits, LGPD Art. 20 contestability (10-business-day timeline), unilateral counselor override. 4-week response SLA (6 counselors per 5,000 students).
- **Reason:** Mentors' Comments #31, #32, #34, #37, #38, #39, #42, #43, #44, #45, #46, #49, #50, #51, #52, #53, #54, #55, #56, #58, #59, #60.

---

### 6. Section V: Conclusion & Limitations
- **Location:** Paragraphs 78–80
- **Old Text:** Claimed proven fairness; 84.8% recall; GPA 71.3% share; limitations unorganized.
- **New Text:**
  - Paragraph 78: Concluded with experimentally verified `dev2` findings: 15,084 IFNMG cohort without GPA, RF champion (73.18% recall, 75.64% precision, 0.8968 ROC-AUC, 0.1080 Brier score), course failures (32.37%) and attendance (19.26%) dominant.
  - Paragraph 79: Fairness conclusions: Income and digital access disparities survive Holm-Bonferroni; Reweighing drops recall by 12.82 pp; proposed 5-pillar charter and heuristic risk bands.
  - Paragraph 80: Limitations organized into 6 explicit categories: (1) Data Provenance & Selection (IFNMG, active student right-censoring), (2) Label Construct (heterogeneous attrition pathways grouped into binary target), (3) Cumulative Feature Measurement Window (cross-sectional accumulation prevented first-year restriction), (4) Subgroup Uncertainty, (5) External Validity (single Brazilian network vs Indian universities), (6) Untested Governance (proposed design not field-tested in live operations).
- **Reason:** Mentors' Comments #61, #62, #63, #64, #65, #67, #68, #69.

---

### 7. Figures & References
- **Figures:**
  - `Fig. 4` (Global SHAP Beeswarm Plot): Replaced embedded `media/image4.png` with newly generated `results/fig2_shap_beeswarm.png` showing `dev2` attributions without GPA (`reprovacoes` and `percentual_frequencia` as top features).
  - `Fig. 5` (Fairness Audit Dashboard): Replaced embedded `media/image5.png` with newly generated `results/fig4_fairness_audit.png` displaying the exact 5-axis audit at $\tau=0.50$ (DI, Recall, SPD, and Threshold Sweep).
- **References:**
  - Verified all 22 references intact in IEEE format.
  - Verified that all 22 references are cited sequentially in the text ([1] through [22]).
  - Repaired citation numbering for Kleinberg et al. ([15]), Lundberg & Lee ([12]), Hardt et al. ([21]), and Brasil LGPD ([22]).
- **Reason:** Mentors' Comments #71, #72, #74, #75.

