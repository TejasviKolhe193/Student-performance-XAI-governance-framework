# 🏁 Final Empirical Results: Clean Pipeline Execution
## Student Performance Explainable AI (XAI) & Fairness Governance Framework
### Complete End-to-End Replication of Silva et al. (IEEE RITA 2025) Without Target Leakage + Multi-Dimensional Equity & Operational Governance Extensions

> **Branch**: `dev2`  
> **Execution Timestamp**: November 4, 2026 (Clean Re-run of Phases 1 to 5)  
> **Global Random Seed**: `42` (`seeds.txt`)  
> **Total Filtered Cohort**: $N = 15,084$ Brazilian Technical Secondary Education Students  
> **Class Balance**: Completed = $11,703$ (77.59%), Dropout = $3,381$ (22.41%)  
> **Train / Test Partition**: Stratified 70/30 ($N_{\text{train}} = 10,558$, $N_{\text{test}} = 4,526$)  
> **Pipeline Guarantee**: **100% Strict Leak-Free** — Retrospective Cumulative GPA (`ira`) strictly excluded; all scaling, imputers, resamplers, and selectors fit strictly inside cross-validation training folds.

---

## 1. Executive Summary & Core Results

| Pipeline Dimension | Base Paper: Silva et al. (2025) | Clean Run Replicated Results (`dev2`) | Status & Methodological Notes |
|:---|:---:|:---:|:---|
| **Total Cohort ($N$)** | 15,084 | **15,084** | **100% Exact Match** |
| **Completed Students (Class 0)** | 11,703 (77.6%) | **11,703 (77.59%)** | **100% Exact Match** |
| **Dropouts (Class 1)** | 3,381 (22.4%) | **3,381 (22.41%)** | **100% Exact Match** |
| **Test Set Size** | 4,526 (30% held-out) | **4,526 (30% held-out)** | **100% Exact Match** |
| **Cumulative GPA (`ira`)** | Not reported in Table II | **Strictly EXCLUDED** | Reverted to prevent target leakage |
| **Champion Model (Recall-First)** | RF + SMOTEENN (Recall: 85.4%)* | **Decision Tree (UnderSampling + Feature Importance)** | **Recall: 75.05%, Precision: 67.05%, AUC: 0.8736, Accuracy: 86.15%** |
| **Champion Model (Ensemble/AUC)** | — | **Random Forest (UnderSampling + Feature Importance)** | **Recall: 72.68%, Precision: 75.20%, AUC: 0.8929, Accuracy: 88.51%** |
| **Top Global Predictor** | Attendance / Failures | **Course Failures (`reprovacoes`, Mean \|SHAP\| = 0.1750)** | Confirmed academic catalyst |
| **Second Predictor** | Attendance / Failures | **Attendance (`percentual_frequencia`, Mean \|SHAP\| = 0.1416)** | Critical threshold at 75% |
| **Gender Fairness** | Not evaluated | **Disparate Impact: 0.8116 (Passes 4/5ths Rule)** | **EOD: -0.0153 (Passes Parity, p = 0.570)** |
| **Brier Calibration Score** | Not reported | **0.1146** | Good probabilistic calibration |

*\*Note on Silva et al. baseline: The base paper's reported 85.4% recall reflects pre-split balancing leakage. Under strict leak-free cross-validation, true test recall converges to 72.7%–75.1%.*

---

## 2. Phase 1: Data Preparation & Cohort Preprocessing

### 2.1 Cohort Provenance & Split
- **Source**: Administrative records from *Instituto Federal do Norte de Minas Gerais (IFNMG)* (`dataset_evasao_MDE.xlsx`).
- **Filtered Modalities**: `Integrado` ($N = 10,070$), `Subsequente` ($N = 3,902$), `Concomitante` ($N = 718$), `Integrado EJA` ($N = 394$).
- **Excluded Attributes**:
  - Identifier: `alunoid`
  - High missingness (>20%): `dataconclusao`, `forma_acesso_seletivo`, `razao_ausencia_educacional`, `pontuacao_seletivo`
  - Target leakage: `ira` (Cumulative GPA computed retrospectively over entire academic duration).
- **Partitioning**: Stratified 70/30 split:
  - **Training Set**: $10,558$ students (Class 0: 8,191, Class 1: 2,367)
  - **Held-Out Test Set**: $4,526$ students (Class 0: 3,512, Class 1: 1,014)
- **Outlier Treatment**: 1.5× IQR Winsorization fit strictly on training set and applied to test set for `idade`, `rendabruta`, `quantidade_computadores`, `quantidade_notebooks`, `qtd_filhos`.

---

## 3. Phase 2: 48-Experiment Model Benchmark

A full $4 \times 4 \times 3$ factorial benchmark was executed across 4 classifiers, 4 balancing techniques, and 3 feature selection strategies:

### 3.1 Top 5 Ranked Models (Evaluated on 4,526 Held-Out Test Students)

| Rank | Model | Balancing Strategy | Feature Selection | Recall | Precision | F1-Score | ROC-AUC | Overall Accuracy | 10-Fold CV Recall |
|:---:|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | **Decision Tree (DT)** | **RandomUnderSampler** | **Feature Importance** | **0.7505** | **0.6705** | **0.7082** | **0.8736** | **0.8615** | **0.7689** |
| **2** | **Decision Tree (DT)** | **RandomUnderSampler** | **Backward Selection** | **0.7505** | **0.6640** | **0.7046** | **0.8743** | **0.8590** | **0.7685** |
| **3** | **Random Forest (RF)** | **RandomUnderSampler** | **Feature Importance** | **0.7268** | **0.7520** | **0.7392** | **0.8929** | **0.8851** | **0.7457** |
| **4** | **Decision Tree (DT)** | **RandomUnderSampler** | **ANOVA** | **0.7249** | **0.6844** | **0.7040** | **0.8666** | **0.8635** | **0.7512** |
| **5** | **Random Forest (RF)** | **RandomUnderSampler** | **Backward Selection** | **0.7219** | **0.7609** | **0.7409** | **0.8942** | **0.8869** | **0.7482** |

### 3.2 Best Configuration per Algorithm

| Algorithm Family | Best Balancing | Best Feature Selection | Test Recall | Test Precision | Test Accuracy | ROC-AUC | 10-Fold CV Recall |
|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **Decision Tree (Champion)** | UnderSampling | Feature Importance | **0.7505** | 0.6705 | 0.8615 | 0.8736 | 0.7689 |
| **Random Forest (Ensemble)** | UnderSampling | Feature Importance | 0.7268 | **0.7520** | **0.8851** | **0.8929** | 0.7457 |
| **Linear SVM** | SMOTEENN | Feature Importance | 0.6075 | 0.4646 | 0.7552 | 0.7612 | 0.7220 |
| **Logistic Regression** | SMOTEENN | Backward Selection | 0.5917 | 0.4717 | 0.7601 | 0.7556 | 0.7031 |

---

## 4. Phase 3: Explainable AI (SHAP & LIME)

### 4.1 Global Feature Importance (TreeSHAP across Test Cohort)

| Rank | Feature (Code Name) | English Description | Mean \|SHAP\| | % Attribution Mass | Substantive Meaning |
|:---:|:---|:---|:---:|:---:|:---|
| 1 | `reprovacoes` | Number of course failures | **0.1750** | **31.7%** | Strongest positive risk driver; failing $\ge 1$ subject causes immediate risk jump |
| 2 | `percentual_frequencia` | Attendance percentage | **0.1416** | **25.7%** | Sharp behavioral threshold at 75% attendance |
| 3 | `anoingresso` | Admission / cohort year | **0.0872** | **15.8%** | Institutional policy and calendar cohort trends |
| 4 | `idade` | Student age at admission | **0.0379** | **6.9%** | Adult learners face higher work/family friction |
| 5 | `campus` | Campus location | **0.0246** | **4.5%** | Regional resource disparities across institutes |
| 6 | `modalidade` | Educational modality | **0.0232** | **4.2%** | Distinct completion curves (Integrado vs. EJA) |
| 7 | `rendabruta` | Gross family income | **0.0182** | **3.3%** | Socioeconomic buffer against unexpected disruption |
| 8 | `curso` | Course / major | **0.0179** | **3.2%** | Technical domain differences |
| 9 | `pai_nivel_escolaridade` | Father's education | **0.0077** | **1.4%** | First-generation college student effect |
| 10 | `trabalha` | Employment status | **0.0074** | **1.3%** | Work-study balance pressures |

### 4.2 Local Explanations & SHAP-LIME Concordance

| Student Archetype | Test Index | Actual Status | P(Dropout) | Top-3 SHAP Factors | Top-3 LIME Factors | Common Features | Jaccard Concordance |
|:---|:---:|:---:|:---:|:---|:---|:---|:---:|
| **High-Risk Case** | #525 | Dropped Out (1) | **80.0%** | `reprovacoes`, `rendabruta`, `mae_escolaridade` | `percentual_frequencia`, `reprovacoes`, `idade` | `reprovacoes` | **0.2000** |
| **Borderline Case** | #4491 | Dropped Out (1) | **50.0%** | `percentual_frequencia`, `curso`, `rendabruta` | `percentual_frequencia`, `reprovacoes`, `trabalha` | `percentual_frequencia` | **0.2000** |
| **Low-Risk Case** | #1584 | Completed (0) | **17.7%** | `percentual_frequencia`, `reprovacoes`, `anoingresso` | `percentual_frequencia`, `reprovacoes`, `idade` | `percentual_frequencia`, `reprovacoes` | **0.5000** |

- **Mean Top-3 Jaccard Overlap**: **0.3000** (30.0%).
- *Methodological Note*: Reported factually as empirical surrogate overlap; not claimed as ground-truth proof of model reliability.

---

## 5. Phase 4: Algorithmic Fairness Audit & Mitigation

### 5.1 Subgroup Disaggregated Performance (Baseline $\tau = 0.50$)

| Subgroup | Sample ($N$) | Base Dropout Rate | Model Selection Rate | Selection Rate 95% CI | Recall (TPR) | TPR 95% CI | Precision | FPR |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Overall Test Cohort** | **4,526** | **22.40%** | **25.48%** | [0.242, 0.266] | **75.84%** | [0.731, 0.783] | **66.70%** | **10.93%** |
| **Gender: Male (`M`)** | 2,135 | 25.95% | 28.29% | [0.263, 0.301] | 76.53% | [0.728, 0.802] | 70.20% | 11.39% |
| **Gender: Female (`F`)** | 2,391 | 19.24% | 22.96% | [0.213, 0.246] | 75.00% | [0.706, 0.787] | 62.84% | 10.56% |
| **Race: Brown (`Parda`)** | 3,182 | 22.50% | 26.21% | [0.247, 0.278] | 78.49% | [0.756, 0.816] | 67.39% | 11.03% |
| **Race: Black (`Preta`)** | 646 | 22.60% | 25.23% | [0.221, 0.284] | 74.66% | [0.679, 0.818] | 66.87% | 10.80% |
| **Race: White (`Branca`)** | 641 | 21.37% | 21.53% | [0.181, 0.248] | 65.69% | [0.578, 0.733] | 65.22% | 9.52% |
| **Income: High (> R$ 930)** | 2,254 | 19.03% | 19.12% | [0.175, 0.206] | 69.23% | [0.650, 0.736] | 68.91% | 7.34% |
| **Income: Low ($\le$ R$ 930)** | 2,272 | 25.75% | 31.78% | [0.298, 0.337] | 80.68% | [0.774, 0.841] | 65.37% | 14.82% |
| **Age: Traditional ($\le 20$)** | 2,121 | 18.62% | 20.65% | [0.191, 0.223] | 73.92% | [0.691, 0.782] | 66.67% | 8.46% |
| **Age: Adult ($> 20$)** | 2,405 | 25.74% | 29.73% | [0.279, 0.316] | 77.06% | [0.738, 0.805] | 66.71% | 13.33% |
| **Computer: $\ge 1$ Laptop** | 1,325 | 18.42% | 20.23% | [0.182, 0.223] | 68.85% | [0.634, 0.752] | 62.69% | 9.25% |
| **Computer: 0 Laptops** | 3,201 | 24.05% | 27.65% | [0.261, 0.291] | 78.05% | [0.754, 0.810] | 67.91% | 11.68% |

### 5.2 AIF360 Multi-Threshold Fairness Audit & Holm-Bonferroni Correction

| Threshold | Protected Comparison | Disparate Impact (DI) | Four-Fifths Rule | Equal Opportunity Diff (EOD) | EOD Status | Holm-Bonferroni Significance |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| **$\tau = 0.50$** | **Gender (M vs F)** | **0.8116** | **PASS [0.80, 1.25]** | **-0.0153** | **PASS ($\pm 0.10$)** | Not Significant ($p = 0.570$) |
| $\tau = 0.50$ | **Race (Branca vs Preta)** | **1.1720** | **PASS [0.80, 1.25]** | **+0.0896** | **PASS ($\pm 0.10$)** | Not Significant ($p = 0.099$) |
| $\tau = 0.50$ | **Race (Branca vs Parda)** | 1.2174 | PASS [0.80, 1.25] | +0.1280 | Flagged | Significant ($p = 0.00122$) |
| $\tau = 0.50$ | **Income (> Med vs $\le$ Med)** | 1.6619 | Flagged | +0.1145 | Flagged | Significant ($p = 0.00003$) |
| $\tau = 0.50$ | **Age ($\le 20$ vs $> 20$)** | 1.4397 | Flagged | +0.0314 | **PASS ($\pm 0.10$)** | Not Significant ($p = 0.255$) |
| $\tau = 0.50$ | **Computer ($\ge 1$ vs 0)** | 1.3669 | Flagged | +0.0920 | **PASS ($\pm 0.10$)** | Significant ($p = 0.00344$) |

### 5.3 Proxy Variable Predictability Check
- `genero` (Gender): Proxy AUC = **0.620** (No proxy risk)
- `raca` (Race): Proxy AUC = **0.598** (No proxy risk)
- `rendabruta` (Income): Proxy AUC = **0.684** (No proxy risk)
- `idade` (Age): Proxy AUC = **0.960** (⚠️ Structural proxy: adult programs enroll older students)
- `quantidade_notebooks` (Computer): Proxy AUC = **0.716** (⚠️ Moderate proxy with family income)

### 5.4 Pre-Processing Debiasing Trade-Off (AIF360 Reweighing)

| Metric | Pre-Mitigation Baseline | Post-Mitigation (Reweighing) | Impact / Cost |
|:---|:---:|:---:|:---:|
| **Model Recall (Catch Rate)** | **75.84%** | **59.86%** | **-15.98 pp (Severe Performance Penalty)** |
| **Model Precision** | **66.70%** | **93.53%** | **+26.83 pp (Fewer False Alarms)** |
| **Model F1-Score** | 0.7097 | 0.7300 | +0.0203 |
| **Model Accuracy** | 86.10% | 90.08% | +3.98 pp |
| **Gender Disparate Impact (DI)** | 0.8116 | 0.6861 | -0.1255 |
| **Gender Equal Opportunity Diff (EOD)** | -0.0153 | -0.0373 | -0.0220 |

> [!WARNING]
> **Key Finding**: Reweighing drops recall by **16 percentage points**, missing over 40% of dropouts. In public education, missing at-risk students carries high social costs. Thus, algorithmic debiasing alone cannot substitute for **human-in-the-loop governance**.

---

## 6. Phase 5: Operational AI Governance & Calibration

### 6.1 Calibration & Brier Score
- **Brier Score**: **0.1146** (Demonstrates good probabilistic calibration against 22.4% test prevalence).

### 6.2 Calibrated 8-Tier Risk Band Intervention Framework

| Decision Threshold ($\tau$) | Tier / Risk Band Label | Expected Flags per 1,000 Students | Precision | Recall | Total Flags per 5,000 Cohort | Weeks for 1 Counselor | Counselors Needed (4-Week SLA) | Operational Intervention Protocol |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **$\tau \ge 0.80$** | **Tier 1: Emergency Intervention** | **198** | **79.11%** | **69.82%** | **989** | 19.8 | **5** | Immediate mandatory counselor review & retention grant |
| **$\tau \ge 0.70$** | **Tier 2: High Priority At-Risk** | **205** | **77.24%** | **70.61%** | **1,024** | 20.5 | **6** | Social worker outreach, bus fare voucher, peer tutor |
| **$\tau \ge 0.60$** | **Tier 3: Moderate Risk Advisory** | **226** | **72.00%** | **72.78%** | **1,132** | 22.6 | **6** | Academic advisor check-in, failure remediation plan |
| **$\tau \ge 0.50$** | **Tier 4: Baseline Standard** | **255** | **66.70%** | **75.84%** | **1,274** | 25.5 | **7** | General counselor notification, attendance tracking |
| **$\tau \ge 0.40$** | **Tier 5: Early Sensitivity Screen** | **290** | **60.35%** | **78.21%** | **1,452** | 29.0 | **8** | Classroom monitoring, voluntary tutoring notification |
| **$\tau \ge 0.30$** | **Tier 6: Broad Precautionary** | **324** | **55.32%** | **79.98%** | **1,620** | 32.4 | **9** | Departmental tracking list, semester start check-in |
| **$\tau \ge 0.20$** | **Tier 7: Low Concern Baseline** | **476** | **40.74%** | **86.59%** | **2,381** | 47.6 | **12** | Standard institutional academic advising |
| **$\tau \ge 0.10$** | **Tier 8: Universal Inclusion** | **644** | **32.37%** | **93.00%** | **3,218** | 64.4 | **17** | Broad institutional survey and health check |

### 6.3 Five Institutional Governance Pillars
1. **Pillar 1: Strictly Advisory, Non-Punitive Deployment** — No automated dismissals, course tracking, or enrollment denials.
2. **Pillar 2: Mandatory Explainability-Coupled Outreach** — Every outreach must display top SHAP/LIME factors; contacting students based on raw scores alone is prohibited.
3. **Pillar 3: Continuous Semi-Annual Fairness Auditing** — Audits of Disparate Impact and Equal Opportunity across 5 protected axes before every semester.
4. **Pillar 4: Student Right to Contest & Explanation Review (LGPD)** — Unconditional right for students to review explanations and contest erroneous records.
5. **Pillar 5: Certified Human-in-the-Loop Override Authority** — Educational counselors and social workers retain unilateral authority to override or dismiss algorithmic flags.

---

## 7. Artifacts Index Generated in Clean Run

| Phase | Output Artifact | Format / Location | Description |
|:---:|:---|:---:|:---|
| **Phase 1** | `phase1_outputs/phase1_summary.csv` | CSV | Verification of cohort counts and 70/30 split |
| **Phase 1** | `phase1_outputs/phase1_data.pkl` | Binary Pickle | Normalized feature arrays ($N = 15,084$) |
| **Phase 2** | `phase2_outputs/phase2_benchmark_results.csv` | CSV | Full 48-experiment benchmark leaderboard |
| **Phase 2** | `phase2_outputs/top_5_models.csv` | CSV | Top 5 models matching Silva et al. Table IV |
| **Phase 2** | `phase2_outputs/best_model_per_algorithm.csv` | CSV | Champion configurations across DT, RF, SVM, LR |
| **Phase 2** | `phase2_outputs/champion_model_bundle.pkl` | Binary Pickle | Serialized DT and RF champion models |
| **Phase 3** | `phase3_outputs/01_shap_global_beeswarm.png` | Image | Global TreeSHAP summary beeswarm plot |
| **Phase 3** | `phase3_outputs/02_shap_feature_importance.png` | Image | Top 10 features by mean absolute SHAP value |
| **Phase 3** | `phase3_outputs/04_shap_*.png` | Images | Local SHAP waterfall charts for 3 student archetypes |
| **Phase 3** | `phase3_outputs/05_lime_*.html` | Interactive HTML | Local surrogate LIME decision boundaries |
| **Phase 3** | `phase3_outputs/phase3_feature_importance.csv` | CSV | Exact mean absolute SHAP values for all 19 features |
| **Phase 3** | `phase3_outputs/phase3_shap_lime_metrics.csv` | CSV | Archetype Top-3 Jaccard overlap metrics |
| **Phase 4** | `phase4_outputs/phase4_subgroup_metrics.csv` | CSV | Granular metrics across 15 demographic groups with 95% CIs |
| **Phase 4** | `phase4_outputs/phase4_fairness_audit_results.csv` | CSV | Multi-threshold AIF360 DI, SPD, EOD evaluations |
| **Phase 4** | `phase4_outputs/phase4_holm_bonferroni_results.csv` | CSV | FWER corrected significance tests |
| **Phase 4** | `phase4_outputs/phase4_proxy_check.csv` | CSV | Predictive probing AUCs for redundant encoding |
| **Phase 4** | `phase4_outputs/phase4_mitigation_tradeoff.csv` | CSV | Pre-processing AIF360 Reweighing impact table |
| **Phase 5** | `phase5_outputs/phase5_calibration_summary.csv` | CSV | Brier score calibration metric |
| **Phase 5** | `phase5_outputs/phase5_calibration_curve.png` | Image | 10-bin reliability diagram |
| **Phase 5** | `phase5_outputs/phase5_governance_risk_bands.csv` | CSV | Calibrated 8-tier risk bands with staffing SLAs |
| **Phase 5** | `phase5_outputs/governance_policy_charter.md` | Markdown | Normative text of the 5 institutional governance pillars |
| **UI Portal**| `unified_governance_portal.html` | Interactive HTML | Complete interactive web dashboard covering all 5 phases |

---
*Clean execution completed on `dev2` branch.*

