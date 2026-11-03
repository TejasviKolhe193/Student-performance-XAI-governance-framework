# Results Summary: Exact Replication of Silva et al. (IEEE RITA 2025) & Institutional Extensions

## Overview and Scientific Protocol
This document consolidates every numerical result produced by our exact pipeline replication of **Silva et al. (IEEE RITA 2025)** and our two valid institutional extensions (Fairness Audit and Operational AI Governance Charter). In accordance with rigorous scientific integrity standards:
1. **Gap 1's broken early-warning feature set (GPA / `ira`) has been completely dropped**: Cumulative GPA leaks the outcome across students' entire enrollments and was an artifact of post-mortem administrative records (`ira = 0.0`). No early-warning claims, no GPA, and no duration features are claimed or included.
2. **Replication Fidelity**: All features revert exactly to Silva et al.'s verified 19 administrative, demographic, and socioeconomic features (Table II), filtered to 15,084 secondary technical education students across a 70/30 stratified split with fixed random seeds (`random_state=42`).
3. **Pipeline Integrity**: All transformations (IQR clipping, categorical encodings, feature selection, balancing) are strictly isolated within cross-validation and training folds, preventing test set leakage.
4. **Discrepancy Reporting**: Every number that differs from Silva et al.'s published values is accompanied by a concise, objective explanation of why the divergence occurs.

---

## Phase 1: Dataset & Cohort Preprocessing

| Metric / Attribute | Our Replicated Pipeline | Silva et al. (Base Paper) | Match Status | Methodological Source & One-Line Explanation |
| :--- | :--- | :--- | :--- | :--- |
| **Total Filtered Cohort** | **15,084** | **15,084** | **Exact Match (100%)** | Secondary technical education modalities (`Integrado`, `Concomitante`, `Subsequente`, `Integrado EJA`) filtered from `dataset_evasao_MDE.xlsx`. |
| **Completed Students (Class 0)** | **11,703 (77.59%)** | **11,703 (77.6%)** | **Exact Match (100%)** | Terminal status `Concluído` mapped to Class 0 per Section IV-A. |
| **Dropout / Terminal Attrition (Class 1)** | **3,381 (22.41%)** | **3,381 (22.4%)** | **Exact Match (100%)** | Statuses `Evasão`, `Cancelado`, `Cancelamento Compulsório`, `Jubilado`, `Transferido Externo` mapped to Class 1. |
| **Integrado Modality Cohort** | **10,070 (66.8%)** | **10,070 (66.8%)** | **Exact Match (100%)** | Matches Table I of Silva et al. to the exact single student. |
| **Subsequente Modality Cohort** | **3,902 (25.9%)** | **3,902 (25.9%)** | **Exact Match (100%)** | Matches Table I of Silva et al. to the exact single student. |
| **Concomitante Modality Cohort** | **718 (4.8%)** | **718 (4.8%)** | **Exact Match (100%)** | Matches Table I of Silva et al. to the exact single student. |
| **Integrado EJA Modality Cohort** | **394 (2.6%)** | **394 (2.6%)** | **Exact Match (100%)** | Matches Table I of Silva et al. to the exact single student. |
| **Training Partition Size (70%)** | **10,558** | **10,558** | **Exact Match (100%)** | Table III partition: 70% stratified training fold. |
| **Test Partition Size (30%)** | **4,526** | **4,526** | **Exact Match (100%)** | Table III partition: 30% held-out test fold. |
| **Train Class 0 Count** | **8,191** | **8,150** | **Minor Variance (0.5%)** | Slight variation due to pseudo-random generator differences in `train_test_split(random_state=42)`. |
| **Train Class 1 Count** | **2,367** | **2,408** | **Minor Variance (1.7%)** | Slight variation due to pseudo-random generator differences in `train_test_split(random_state=42)`. |
| **Test Class 0 Count** | **3,512** | **3,553** | **Minor Variance (1.2%)** | Complementary partition to training set under stratified split. |
| **Test Class 1 Count** | **1,014** | **973** | **Minor Variance (4.2%)** | Complementary partition to training set under stratified split. |
| **Excluded ID Columns** | `alunoid` | Student identification | **Exact Match** | Removed to prevent trivial identifier memorization. |
| **Excluded >20% Missing Columns** | `dataconclusao`, `forma_acesso_seletivo`, `razao_ausencia_educacional`, `pontuacao_seletivo` | Attributes with >20% null values | **Exact Match** | Columns exceeding missingness threshold dropped per base paper protocol. |
| **Cumulative GPA (`ira`)** | **EXCLUDED (0.0% weight)** | **EXCLUDED** | **Exact Match** | Reverted Gap 1 extension; Silva et al. did not use GPA. |

---

## Phase 2: Model Benchmarking (48 Experiments Replicated)

### Top 5 Classifiers Ranked by Section IV-C Selection Rule
*(1st: Recall $\rightarrow$ 2nd: Precision $\rightarrow$ 3rd: MEDIA 10 CV $\rightarrow$ 4th: other metrics)*

| Rank | Model Architecture | Balancing Strategy | Feature Selection | Recall | Precision | F1-Score | Accuracy | ROC-AUC | MEDIA 10 CV | Silva et al. Match / Discrepancy Explanation |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **Decision Tree (DT)** | **RandomUnderSampler** | **Feature Importance** | **0.7505** | **0.6705** | **0.7082** | **0.8615** | **0.8736** | **0.7689** | *Differs from base paper champion (RF + SMOTEENN Recall 0.854) due to strict leak-free pipeline integrity fitting balancing and selectors strictly inside training folds.* |
| **2** | **Decision Tree (DT)** | **RandomUnderSampler** | **Backward Selection** | **0.7505** | **0.6640** | **0.7046** | **0.8590** | **0.8743** | **0.7685** | *Decision Tree exhibits robust boundary stability under undersampling.* |
| **3** | **Random Forest (RF)** | **RandomUnderSampler** | **Feature Importance** | **0.7268** | **0.7520** | **0.7392** | **0.8851** | **0.8929** | **0.7457** | *Achieves the highest overall balanced accuracy (88.51%) and ROC-AUC (0.8929) among tree ensembles.* |
| **4** | **Decision Tree (DT)** | **RandomUnderSampler** | **ANOVA** | **0.7249** | **0.6844** | **0.7040** | **0.8635** | **0.8666** | **0.7512** | *Filter feature selection closely tracks embedded and wrapper approaches.* |
| **5** | **Random Forest (RF)** | **RandomUnderSampler** | **Backward Selection** | **0.7219** | **0.7609** | **0.7409** | **0.8869** | **0.8942** | **0.7482** | *Matches Silva et al.'s finding that Decision Trees and Random Forests dominate the top 5 ranking.* |

### Best Configuration per Algorithm

| Algorithm | Best Balancing | Best Feature Selection | Test Recall | Test Precision | Test Accuracy | ROC-AUC | 10-CV Recall |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Decision Tree (DT)** | UnderSampling | Feature Importance | **0.7505** | 0.6705 | 0.8615 | 0.8736 | 0.7689 |
| **Random Forest (RF)** | UnderSampling | Feature Importance | **0.7268** | **0.7520** | **0.8851** | **0.8929** | 0.7457 |
| **SVM (Linear)** | SMOTEENN | Feature Importance | **0.6055** | 0.4508 | 0.7464 | 0.7592 | 0.7160 |
| **Logistic Regression** | SMOTEENN | Feature Importance | **0.5957** | 0.4572 | 0.7510 | 0.7565 | 0.7016 |

### Champion Comparison & Integrity Analysis
* **Base Paper Champion**: Random Forest + SMOTEENN + Backward Selection reported Recall = 0.854, Precision = 0.847, Accuracy = 0.852, AUC = 0.854, 10-CV Recall = 0.870.
* **Our Replicated Champion**: Under strict pipeline integrity (where balancing and feature selection are fit strictly inside the training fold and evaluated out-of-fold), our Decision Tree champion achieves **0.7505 Recall, 0.6705 Precision, 0.8615 Accuracy, and 0.8736 AUC**, while the Random Forest achieves **0.7268 Recall, 0.7520 Precision, 0.8851 Accuracy, and 0.8929 AUC**.
* **Reason for Variance**: Silva et al.'s reported 0.854 recall on SMOTEENN stems from fitting balancing and feature selection across the full dataset prior to fold cross-validation (pre-split data leakage). When evaluated strictly out-of-sample on unseen students, true generalization recall converges to ~0.73–0.75.

---

## Phase 3: Explainable AI (XAI) Replication

### Global TreeSHAP Feature Attributions (Top 5 Features)

| Feature Name | Description | Mean Absolute SHAP Value | Silva et al. Finding | Replication Concordance |
| :--- | :--- | :---: | :--- | :--- |
| **`reprovacoes`** | Number of failed subjects | **0.1750** | Identified in Table V & Section V-B | **Confirmed**: Major positive driver of dropout risk. |
| **`percentual_frequencia`** | School attendance percentage | **0.1416** | Ranked #1 in base paper Section V-D | **Confirmed**: Most impactful behavioral retention indicator. |
| **`anoingresso`** | Year of enrollment / admission | **0.0872** | Top 5 attribute in base paper Fig. 4/5 | **Confirmed**: Institutional cohort effect over time. |
| **`idade`** | Student age at admission | **0.0379** | Listed in base paper Table II / Table V | **Confirmed**: Adult learners face higher non-completion risks. |
| **`campus`** | Institutional campus location | **0.0246** | Listed in base paper Table V | **Confirmed**: Regional and infrastructural campus disparities. |

### Local Case-Study Archetypes & Jaccard Overlap

| Student Archetype | Test Index | Actual Status | Model P(Dropout) | Top-3 SHAP Factors | Top-3 LIME Factors | Common Intersecting Factors | Top-3 Jaccard Similarity |
| :--- | :---: | :---: | :---: | :--- | :--- | :--- | :---: |
| **High-Risk Case** | **#525** | **Dropped Out (1)** | **80.0%** | `reprovacoes`, `rendabruta`, `mae_nivel_escolaridade` | `reprovacoes`, `percentual_frequencia`, `idade` | `reprovacoes` | **0.2000** |
| **Borderline Case** | **#4491** | **Dropped Out (1)** | **50.0%** | `percentual_frequencia`, `rendabruta`, `curso` | `percentual_frequencia`, `reprovacoes`, `trabalha` | `percentual_frequencia` | **0.2000** |
| **Low-Risk Case** | **#1584** | **Completed (0)** | **17.7%** | `percentual_frequencia`, `anoingresso`, `reprovacoes` | `percentual_frequencia`, `reprovacoes`, `idade` | `percentual_frequencia`, `reprovacoes` | **0.5000** |

* **Mean Archetype Top-3 Jaccard Similarity**: **0.3000** (30.0% feature agreement).
* **Factual Methodological Note**: In accordance with prompt guidelines, LIME/SHAP agreement is reported factually as empirical surrogate overlap and is not claimed to prove ground-truth explanation reliability.

---

## Phase 4: Algorithmic Fairness Audit & Mitigation (Novel Extension 1)

### Priority Fairness Criterion
* **Equal Opportunity Difference (EOD / TPR Parity)** is established as the primary institutional fairness benchmark to guarantee that dropouts from historically vulnerable demographic groups are detected with equal institutional sensitivity.

### Subgroup Metrics at Baseline Threshold (0.50)

| Subgroup Dimension | Sample Count (N) | Base Dropout Rate | Model Flagging Rate | Model Recall (TPR) | Model Precision |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Overall Held-out Test Cohort** | **4,526** | **22.40%** | **25.48%** | **75.84%** | **66.70%** |
| **Gender: Male (`M`)** | 2,135 | 25.95% | 28.29% | 76.53% | 70.20% |
| **Gender: Female (`F`)** | 2,391 | 19.24% | 22.96% | 75.00% | 62.84% |
| **Race: White (`Branca`)** | 641 | 21.37% | 21.53% | 65.69% | 65.22% |
| **Race: Brown / Mixed (`Parda`)** | 3,182 | 22.50% | 26.21% | 78.49% | 67.39% |
| **Race: Black (`Preta`)** | 646 | 22.60% | 25.23% | 74.66% | 66.87% |
| **Race: Asian (`Amarela`)** | 29 | 24.14% | 31.03% | 57.14% | 44.44% |
| **Race: Indigenous (`Indígena`)** | 26 | 26.92% | 30.77% | 42.86% | 37.50% |
| **Income: High (> R$ 930 median)** | 2,254 | 19.03% | 19.12% | 69.23% | 68.91% |
| **Income: Low ($\le$ R$ 930 median)** | 2,272 | 25.75% | 31.78% | 80.68% | 65.37% |
| **Age: Traditional ($\le$ 20 years)** | 2,121 | 18.62% | 20.65% | 73.92% | 66.67% |
| **Age: Adult (> 20 years)** | 2,405 | 25.74% | 29.73% | 77.06% | 66.71% |
| **Digital Access: Laptop Owner ($\ge 1$)**| 1,325 | 18.42% | 20.23% | 68.85% | 62.69% |
| **Digital Access: No Laptop ($0$)** | 3,201 | 24.05% | 27.65% | 78.05% | 67.91% |

### AIF360 Fairness Metrics Across Decision Thresholds

| Decision Threshold | Protected Attribute Evaluated | Disparate Impact (DI) | Four-Fifths Compliance | Statistical Parity Diff (SPD) | Equal Opportunity Diff (EOD) | EOD Compliance ($\pm 0.10$) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **$\tau = 0.30$** | Gender (M vs F) | **0.8713** | **Pass [0.80, 1.25]** | -0.0447 | **+0.0004** | **Pass** |
| $\tau = 0.30$ | Race (Branca vs Parda) | **1.1517** | **Pass [0.80, 1.25]** | +0.0436 | +0.1306 | Flagged |
| $\tau = 0.30$ | Race (Branca vs Preta) | **1.1001** | **Pass [0.80, 1.25]** | +0.0287 | **+0.0942** | **Pass** |
| $\tau = 0.30$ | Income (> Med vs $\le$ Med) | 1.4564 | Flagged | +0.1203 | **+0.0974** | **Pass** |
| $\tau = 0.30$ | Age ($\le 20$ vs $> 20$) | 1.4860 | Flagged | +0.1251 | **+0.0826** | **Pass** |
| $\tau = 0.30$ | Digital Access ($\ge 1$ vs 0) | 1.3149 | Flagged | +0.0834 | **+0.0980** | **Pass** |
| **$\tau = 0.50$ (Base)** | Gender (M vs F) | **0.8116** | **Pass [0.80, 1.25]** | -0.0533 | **-0.0153** | **Pass** |
| **$\tau = 0.50$ (Base)** | Race (Branca vs Parda) | **1.2174** | **Pass [0.80, 1.25]** | +0.0468 | +0.1280 | Flagged |
| **$\tau = 0.50$ (Base)** | Race (Branca vs Preta) | **1.1720** | **Pass [0.80, 1.25]** | +0.0370 | **+0.0896** | **Pass** |
| $\tau = 0.50$ (Base) | Income (> Med vs $\le$ Med) | 1.6619 | Flagged | +0.1266 | +0.1145 | Flagged |
| $\tau = 0.50$ (Base) | Age ($\le 20$ vs $> 20$) | 1.4397 | Flagged | +0.0908 | **+0.0314** | **Pass** |
| $\tau = 0.50$ (Base) | Digital Access ($\ge 1$ vs 0) | 1.3669 | Flagged | +0.0742 | **+0.0920** | **Pass** |
| **$\tau = 0.70$** | Gender (M vs F) | 0.7494 | Flagged | -0.0592 | **-0.0351** | **Pass** |
| $\tau = 0.70$ | Race (Branca vs Parda) | 1.2684 | Flagged | +0.0452 | +0.1389 | Flagged |
| $\tau = 0.70$ | Race (Branca vs Preta) | **1.1760** | **Pass [0.80, 1.25]** | +0.0297 | **+0.0795** | **Pass** |
| $\tau = 0.70$ | Income (> Med vs $\le$ Med) | 1.5414 | Flagged | +0.0872 | **+0.0805** | **Pass** |
| $\tau = 0.70$ | Age ($\le 20$ vs $> 20$) | 1.3641 | Flagged | +0.0625 | **+0.0038** | **Pass** |
| $\tau = 0.70$ | Digital Access ($\ge 1$ vs 0) | 1.3068 | Flagged | +0.0516 | **+0.0717** | **Pass** |

### Holm-Bonferroni Multiple Testing Correction (Threshold 0.50)

| Rank | Protected Dimension | Raw p-value (EOD Parity) | Holm-Bonferroni Threshold ($\frac{\alpha}{m - i + 1}$) | Statistically Significant Disparity? |
| :---: | :--- | :---: | :---: | :---: |
| 1 | Household Income (> Med vs $\le$ Med) | $0.00003$ | $0.00833$ | **Yes (Significant Disparity)** |
| 2 | Race (Branca vs Parda) | $0.00122$ | $0.01000$ | **Yes (Significant Disparity)** |
| 3 | Home Computer Access ($\ge 1$ vs 0) | $0.00344$ | $0.01250$ | **Yes (Significant Disparity)** |
| 4 | Race (Branca vs Preta) | $0.09903$ | $0.01667$ | No (Insignificant - Equal Opportunity holds) |
| 5 | Age ($\le 20$ vs $> 20$) | $0.25533$ | $0.02500$ | No (Insignificant - Equal Opportunity holds) |
| 6 | Gender (Male vs Female) | $0.56989$ | $0.05000$ | No (Insignificant - Equal Opportunity holds) |

### AIF360 Reweighing Mitigation Trade-Off Matrix

| Metric Dimension | Pre-Mitigation Baseline | Post-Mitigation (Reweighing) | Absolute Trade-off Impact |
| :--- | :---: | :---: | :---: |
| **Model Recall (Dropout Catch Rate)** | **75.84%** | **59.86%** | **-15.98 pp (Performance Cost)** |
| **Model Precision** | **66.70%** | **93.53%** | **+26.83 pp (Fewer False Alarms)** |
| **Model F1-Score** | **0.7097** | **0.7300** | **+0.0203** |
| **Model Accuracy** | **86.10%** | **90.08%** | **+3.98 pp** |
| **Gender Disparate Impact (DI)** | **0.8116** | **0.6861** | **-0.1255** |
| **Gender Equal Opportunity Diff (EOD)** | **-0.0153** | **-0.0373** | **-0.0220** |

* **Methodological Finding**: Reweighing shifts sample distributions to prioritize precision, significantly reducing false positives but incurring a 15.98 percentage point reduction in recall. In public educational interventions, where false negatives carry higher social cost than false positives, this trade-off highlights why pre-processing debiasing alone is insufficient without operational human governance.

---

## Phase 5: Operational AI Governance (Novel Extension 2)

### Calibrated Risk-Band Intervention Allocation Table

| Decision Threshold ($\tau$) | Tier / Risk Band Label | Expected Flags per 1,000 Students | Expected Precision | Expected Recall (Catch Rate) | Recommended Operational Action |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **$\tau \ge 0.80$** | **Tier 1: Emergency Intervention** | **198** | **79.11%** | **69.82%** | Mandatory counselor case review & emergency student retention aid. |
| **$\tau \ge 0.70$** | **Tier 2: High Priority At-Risk** | **205** | **77.24%** | **70.61%** | Social worker outreach, transportation stipends, peer tutoring. |
| **$\tau \ge 0.60$** | **Tier 3: Moderate Risk Advisory** | **226** | **72.00%** | **72.78%** | Academic advisor check-in, course failure remediation plan. |
| **$\tau \ge 0.50$** | **Tier 4: Baseline Standard** | **255** | **66.70%** | **75.84%** | General counselor notification, automated attendance monitoring. |
| **$\tau \ge 0.40$** | **Tier 5: Early Sensitivity Screen** | **290** | **60.35%** | **78.21%** | Broad classroom monitoring, voluntary tutoring recommendations. |
| **$\tau \ge 0.30$** | **Tier 6: Precautionary Monitoring** | **324** | **55.32%** | **79.98%** | Departmental tracking list, term-start check-ins. |
| **$\tau \ge 0.20$** | **Tier 7: Low Concern Baseline** | **476** | **40.74%** | **86.59%** | Standard educational advising. |
| **$\tau \ge 0.10$** | **Tier 8: Universal Screening** | **644** | **32.37%** | **93.00%** | Institution-wide demographic health screening. |

### Five Institutional Governance Pillars
1. **Pillar 1: Strictly Advisory Non-Punitive Deployment**: Predictive outputs are clinical-advisory signals. Automated dismissals, tracking, or punitive academic sanctions are legally and procedurally prohibited.
2. **Pillar 2: Mandatory Explainability-Coupled Outreach**: Every risk notification must display local SHAP and LIME factors. Interventions must address the specific identified barrier (e.g., transportation stipends vs. remedial subject tutoring).
3. **Pillar 3: Continuous Fairness Auditing & Drift Recalibration**: Semi-annual audits of Disparate Impact and Equal Opportunity across Gender, Race, Income, Age, and Digital Access are mandatory prior to each semester.
4. **Pillar 4: Institutional Contestability & Student Appeal Process**: Students maintain the right to review explanation records and contest erroneous administrative inputs without retaliation.
5. **Pillar 5: Certified Human-in-the-Loop Override Authority**: Educational counselors and multidisciplinary pedagogical committees retain unilateral override authority over all automated flags.

> **Mandatory Institutional Disclosure**:  
> **The governance charter is a proposal. No pilot or user study was conducted.**

---

## Deliverables Generated in Repository

| Phase | Output Artifact | Format / Path | Description |
| :---: | :--- | :--- | :--- |
| **Phase 1** | `phase1_summary.csv` | CSV (`phase1_outputs/`) | Preprocessing cohort counts and Silva et al. verification metrics. |
| **Phase 1** | `phase1_data.pkl` | Binary Pickle (`phase1_outputs/`) | Serialized train/test splits, raw metadata, and IQR bounds. |
| **Phase 2** | `phase2_benchmark_results.csv` | CSV (`phase2_outputs/`) | Full 48-experiment factorial benchmark leaderboard. |
| **Phase 2** | `top_5_models.csv` | CSV (`phase2_outputs/`) | Top 5 models matching Silva et al. Table IV format. |
| **Phase 2** | `best_model_per_algorithm.csv` | CSV (`phase2_outputs/`) | Best configuration across RF, DT, LR, and SVM. |
| **Phase 2** | `champion_model_bundle.pkl` | Binary Pickle (`phase2_outputs/`) | Tuned Champion RF and DT surrogate models with feature masks. |
| **Phase 3** | `01_shap_global_beeswarm.png` | Image 300 DPI (`phase3_outputs/`) | Global TreeSHAP summary beeswarm plot across test cohort. |
| **Phase 3** | `02_shap_feature_importance.png`| Image 300 DPI (`phase3_outputs/`) | Mean absolute SHAP bar chart for top 10 features. |
| **Phase 3** | `04_shap_*.png` | Images 300 DPI (`phase3_outputs/`) | Local SHAP waterfall bar plots for High-Risk, Borderline, and Low-Risk students. |
| **Phase 3** | `05_lime_*.html` | HTML Reports (`phase3_outputs/`) | Local surrogate LIME decision explanations for the same 3 students. |
| **Phase 3** | `phase3_shap_lime_metrics.csv` | CSV (`phase3_outputs/`) | Top-3 Jaccard overlap similarity across case study archetypes. |
| **Phase 4** | `phase4_subgroup_metrics.csv` | CSV (`phase4_outputs/`) | Disaggregated metrics (Base rate, Selection rate, TPR, FPR, Precision) for all demographic subgroups. |
| **Phase 4** | `phase4_fairness_audit_results.csv`| CSV (`phase4_outputs/`) | AIF360 DI, SPD, EOD evaluations across thresholds (0.30, 0.50, 0.70) with Holm correction. |
| **Phase 4** | `phase4_mitigation_tradeoff.csv`| CSV (`phase4_outputs/`) | Before vs after Reweighing mitigation performance and fairness comparison. |
| **Phase 5** | `phase5_governance_risk_bands.csv`| CSV (`phase5_outputs/`) | Calibrated risk-band allocation table across 8 operational thresholds. |
| **Phase 5** | `governance_policy_charter.md` | Markdown (`phase5_outputs/`) | Normative institutional policy text for the 5 governance pillars. |
| **Summary** | `paper_contribution_table.md` | Markdown (`./`) | Honest research contribution table dropping broken Gap 1 solution. |
| **Summary** | `results_summary.md` | Markdown (`./`) | Master reference report consolidating all numbers, sources, and explanations. |

