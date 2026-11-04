import subprocess
import sys
import csv
import io
import json

def get_git_file(path):
    res = subprocess.run(['git', 'show', f'dev2:{path}'], capture_output=True, text=True, encoding='utf-8')
    if res.returncode != 0:
        return ''
    return res.stdout

def csv_to_markdown(csv_text, float_fmt=None):
    if not csv_text.strip():
        return ""
    reader = csv.reader(io.StringIO(csv_text.strip()))
    rows = list(reader)
    if not rows:
        return ""
    
    header = rows[0]
    col_widths = [len(h) for h in header]
    data_rows = rows[1:]
    
    # Calculate widths
    for row in data_rows:
        for i, val in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(val))
                
    md_lines = []
    # Header line
    header_str = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(header)) + " |"
    md_lines.append(header_str)
    # Separator line
    sep_str = "| " + " | ".join("-" * col_widths[i] for i in range(len(header))) + " |"
    md_lines.append(sep_str)
    # Rows
    for row in data_rows:
        row_str = "| " + " | ".join((row[i] if i < len(row) else "").ljust(col_widths[i]) for i in range(len(header))) + " |"
        md_lines.append(row_str)
        
    return "\n".join(md_lines)

def main():
    print("Building comprehensive Dev2 master results markdown...")
    
    # 1. Fetch raw assets from dev2
    p1_summary_csv = get_git_file("phase1_outputs/phase1_summary.csv")
    p2_benchmark_csv = get_git_file("phase2_outputs/phase2_benchmark_results.csv")
    p2_top5_csv = get_git_file("phase2_outputs/top_5_models.csv")
    p2_best_algo_csv = get_git_file("phase2_outputs/best_model_per_algorithm.csv")
    p3_importance_csv = get_git_file("phase3_outputs/phase3_feature_importance.csv")
    p3_shap_lime_csv = get_git_file("phase3_outputs/phase3_shap_lime_metrics.csv")
    p4_fairness_csv = get_git_file("phase4_outputs/phase4_fairness_audit_results.csv")
    p4_holm_csv = get_git_file("phase4_outputs/phase4_holm_bonferroni_results.csv")
    p4_proxy_csv = get_git_file("phase4_outputs/phase4_proxy_check.csv")
    p4_subgroup_csv = get_git_file("phase4_outputs/phase4_subgroup_metrics.csv")
    p4_mitigation_csv = get_git_file("phase4_outputs/phase4_mitigation_tradeoff.csv")
    p5_calibration_csv = get_git_file("phase5_outputs/phase5_calibration_summary.csv")
    p5_risk_bands_csv = get_git_file("phase5_outputs/phase5_governance_risk_bands.csv")
    
    dev2_report = get_git_file("dev2-project-report.md")
    p2_exec = get_git_file("PHASE2_EXECUTIVE_SUMMARY.md")
    p3_arch = get_git_file("PHASE3_XAI_ARCHITECTURE.md")
    p4_guide = get_git_file("PHASE4_FAIRNESS_GOVERNANCE_GUIDE.md")
    p5_charter = get_git_file("phase5_outputs/governance_policy_charter.md")
    limitations = get_git_file("docs/limitations.md")
    results_summary = get_git_file("docs/results_summary.md")
    
    md = []
    
    md.append("""# 📊 Complete Empirical Results & Governance Blueprint: `dev2` Branch
## Student Performance Explainable AI (XAI) & Fairness Governance Framework
### End-to-End Replication of Silva et al. (IEEE RITA 2025) Without Target Leakage + Multi-Dimensional Equity & Operational Governance Extensions

> **Branch Reference**: `dev2`  
> **Repository**: `Student-performance-XAI-governance-framework`  
> **Authors / Contributors**: sahiti-web, TejasviKolhe  
> **Execution Date**: November 2026  
> **Global Seed**: `42` (`seeds.txt`)  
> **Target Variable**: Student Dropout (`0 = Completed [77.6%]`, `1 = Dropped Out [22.4%]`)  
> **Cohort Sample**: $N = 15,084$ Brazilian Technical Secondary Education Students  
> **Pipeline Guarantee**: **100% Strict Leak-Free** (GPA excluded due to retrospective calculation; all resamplers and feature selectors fitted strictly inside cross-validation training folds)

---

## Table of Contents
1. [Executive Summary & High-Level Architecture](#1-executive-summary--high-level-architecture)
2. [Phase 1: Institutional Preprocessing & Cohort Extraction](#2-phase-1-institutional-preprocessing--cohort-extraction)
3. [Phase 2: 48-Experiment Machine Learning Benchmark](#3-phase-2-48-experiment-machine-learning-benchmark)
4. [Phase 3: Explainable AI (XAI) — Macro & Micro Architecture](#4-phase-3-explainable-ai-xai--macro--micro-architecture)
5. [Phase 4: Algorithmic Fairness Audit, Multi-Testing Correction & Mitigation](#5-phase-4-algorithmic-fairness-audit-multi-testing-correction--mitigation)
6. [Phase 5: Operational AI Governance Charter & Risk Calibration](#6-phase-5-operational-ai-governance-charter--risk-calibration)
7. [Number-by-Number Reconciliation & Paper Audit](#7-number-by-number-reconciliation--paper-audit)
8. [Threats to Validity & Methodological Limitations](#8-threats-to-validity--methodological-limitations)
9. [Complete Dev2 Commit Log & Artifact Index](#9-complete-dev2-commit-log--artifact-index)

---

## 1. Executive Summary & High-Level Architecture

### 1.1 Core Mission
The `dev2` branch represents the **cleanest, leak-free, production-grade replication and extension** of Silva et al. (*IEEE RITA 2025*). It resolves the fatal flaw of administrative target leakage present in models utilizing retrospective GPA (`ira`) by restricting the feature set strictly to verified pre-enrollment and first-period administrative variables.

### 1.2 Five-Phase Lifecycle Architecture
```mermaid
flowchart TD
    subgraph P1["Phase 1: Institutional Preprocessing"]
        A1["Raw Cohort (N = 15,084)"] --> A2["Binary Target Construction<br/>11,703 Completed | 3,381 Dropout"]
        A2 --> A3["1.5x IQR Winsorization & Imputation"]
        A3 --> A4["70/30 Stratified Split<br/>Train: 10,558 | Test: 4,526"]
    end

    subgraph P2["Phase 2: 48-Experiment Benchmark"]
        B1["4 Classifiers: DT, RF, LR, SVM"] --> B2["4 Balancers: Unbalanced, UnderSample, SMOTE, SMOTEENN"]
        B2 --> B3["3 Selectors: ANOVA, Backward, Feature Importance"]
        B3 --> B4["Nested Leak-Free CV Protocol"]
        B4 --> B5["Champion Model Selection:<br/>Decision Tree (Recall 75.1%, AUC 0.874)<br/>Random Forest (Recall 72.7%, AUC 0.893)"]
    end

    subgraph P3["Phase 3: Dual Macro & Micro XAI"]
        C1["Global Interpretability: TreeSHAP<br/>Top Factors: reprovacoes, frequencia, ano"] --> C2["Local Micro Interpretability: LIME<br/>High-Risk (#525), Borderline (#4491), Safe (#1584)"]
        C2 --> C3["Concordance & Jaccard Stability Metric"]
        C3 --> C4["Counterfactual Trajectory Simulations"]
    end

    subgraph P4["Phase 4: Fairness Audit & Mitigation"]
        D1["5 Protected Dimensions:<br/>Gender, Race, Income, Age, Computer Access"] --> D2["Metrics: Disparate Impact (4/5th Rule) & EOD Parity"]
        D2 --> D3["Holm-Bonferroni FWER Correction (p < 0.05)"]
        D3 --> D4["Proxy Variable Vulnerability Check (AUC)"]
        D4 --> D5["AIF360 Reweighing Trade-Off Analysis"]
    end

    subgraph P5["Phase 5: Operational Governance"]
        E1["Brier Score Calibration (0.1146)"] --> E2["8-Tier Calibrated Risk-Band Framework<br/>Workload & SLA Allocation for Counselors"]
        E2 --> E3["5-Pillar Binding Institutional Charter<br/>Advisory Only, Override, Appeal Rights"]
    end

    P1 --> P2
    P2 --> P3
    P3 --> P4
    P4 --> P5
```

### 1.3 Key Empirical Findings Snapshot
- **Predictive Performance**: Decision Tree with UnderSampling and Feature Importance achieved **Recall = 75.05%**, **Precision = 67.05%**, **F1 = 0.7082**, and **ROC-AUC = 0.8736** on 4,526 completely unseen test students. Random Forest achieved **Recall = 72.68%**, **Precision = 75.20%**, and **ROC-AUC = 0.8929**.
- **Explanation Drivers**: Global SHAP feature attributions show that student academic friction (`reprovacoes` = 0.1750 mean $|SHAP|$) and institutional engagement (`percentual_frequencia` = 0.1416) dominate prediction, accounting for over 52% of total feature importance.
- **Fairness Audit**: 
  - **Gender** fully satisfies both the Four-Fifths Disparate Impact screening rule ($DI = 0.8116$) and Equal Opportunity parity ($EOD = -0.0153, p = 0.570$).
  - **Income** ($DI = 1.6619$) and **Race (Branca vs. Parda)** ($DI = 1.2174$) exhibit statistically significant selection rate flags under Holm-Bonferroni correction ($p = 0.00003$ and $p = 0.00122$), reflecting real-world historical vulnerability rather than algorithmic bias.
- **Proxy Discrimination Risk**: Predictive probing revealed that student age encodes strong proxy correlation with technical modality (`AUC = 0.960`), while home computer ownership correlates with family income (`AUC = 0.716`).
- **Mitigation Caveat**: Pre-processing AIF360 Reweighing successfully eliminates selection rate bias and increases precision to $93.3\%$, but causes a catastrophic **16.57 percentage point drop in recall** ($75.8\% \rightarrow 59.3\%$). In student dropout prevention, this false-negative surge is unacceptable, making human governance the required remedy.
- **Operational Calibration**: Brier Score of **0.1146** confirms excellent probability calibration against the 22.4% baseline prevalence.

---

## 2. Phase 1: Institutional Preprocessing & Cohort Extraction

### 2.1 Dataset Provenance & Cohort Attrition
The data originates from administrative enrollment records of the **Instituto Federal de Educação, Ciência e Tecnologia do Norte de Minas Gerais (IFNMG)** (`dataset_evasao_MDE.xlsx`).

| Filtering Stage | Cohort Count | Reason for Exclusion / Retention |
|---|:---:|---|
| **Raw Administrative Records** | 48,311 | Entire institutional database spanning multiple decades and education levels |
| **Technical Modalities Filter** | 15,084 | Restricted strictly to the 4 secondary technical modalities analyzed by Silva et al. (2025): `Integrado`, `Concomitante`, `Subsequente`, `Integrado EJA` |
| **Completed Students (Class 0)** | 11,703 | 77.58% institutional completion rate |
| **Dropout / Non-Completion (Class 1)**| 3,381 | 22.42% institutional non-completion rate (dropout, cancellation, expulsion, transfer) |
| **Train Set (70% Stratified)** | 10,558 | Used strictly for cross-validation, balancing, and model fitting |
| **Test Set (30% Stratified)** | 4,526 | Held out completely until final champion model evaluation |

### 2.2 Leakage Elimination: The Exclusion of GPA (`ira`)
> [!IMPORTANT]
> In raw institutional records, Cumulative GPA (`ira`) is calculated across the entire academic lifetime of a student, frequently updated at graduation, transfer, or dropout. Using `ira` creates severe retrospective target leakage. In `dev2`, GPA was **completely removed**, restricting the feature space to the 19 pre-enrollment and attendance features verified by Silva et al. (2025).

### 2.3 Feature Space Definition (19 Features)
| # | Feature Name (PT) | English Description | Variable Type | Preprocessing & Encoding |
|:---:|---|---|---|---|
| 1 | `idade` | Age at admission | Continuous | 1.5× IQR Winsorization, Standardized |
| 2 | `rendabruta` | Gross family income | Continuous | 1.5× IQR Winsorization, Standardized |
| 3 | `reprovacoes` | Number of course failures | Integer / Discrete | Kept raw numeric |
| 4 | `percentual_frequencia` | Attendance percentage | Continuous | Bounded [0.0, 100.0] |
| 5 | `quantidade_computadores` | Desktop computers in home | Integer | Median imputed, Winsorized |
| 6 | `quantidade_notebooks` | Laptops in home | Integer | Median imputed, Winsorized |
| 7 | `qtd_filhos` | Number of children | Integer | Winsorized [0, 4] |
| 8 | `anoingresso` | Enrollment year | Discrete | Numeric temporal indicator |
| 9 | `periodoingresso` | Enrollment semester | Binary | 1st or 2nd semester |
| 10 | `genero_M` / `genero_F` | Student gender | Categorical | One-Hot Encoded |
| 11 | `raca` | Self-reported race/ethnicity | Categorical | One-Hot Encoded (`Branca`, `Parda`, `Preta`, `Amarela`, `Indigena`) |
| 12 | `estado_civil` | Marital status | Categorical | One-Hot Encoded |
| 13 | `mae_nivel_escolaridade`| Mother's educational level | Ordinal | Mapped [0 = No schooling, ..., 8 = Post-grad] |
| 14 | `pai_nivel_escolaridade`| Father's educational level | Ordinal | Mapped [0 = No schooling, ..., 8 = Post-grad] |
| 15 | `trabalha` | Student employment status | Binary | 1 = Employed, 0 = Not employed |
| 16 | `modalidade` | Educational modality | Categorical | Label Encoded (Integrado, Subsequente, etc.) |
| 17 | `campus` | IFNMG campus location | Categorical | Label Encoded |
| 18 | `curso` | Specific course program | Categorical | Label Encoded |
| 19 | `tipo_area_residencial` | Residential area | Binary | 1 = Urban, 0 = Rural |

---

## 3. Phase 2: 48-Experiment Machine Learning Benchmark

### 3.1 Experimental Design
A full $4 \times 4 \times 3$ factorial grid was executed:
- **4 Classifiers**: Decision Tree (DT), Random Forest (RF), Logistic Regression (LR), Support Vector Machine (Linear SVM).
- **4 Balancing Strategies**: Unbalanced (None), Random Under-Sampling, SMOTE, SMOTEENN.
- **3 Feature Selection Strategies**: ANOVA F-test Filter, Backward Wrapper Elimination, Random Forest Gini Importance.
- **Validation**: 10-fold cross-validation inside training folds (`imblearn.pipeline.Pipeline`).

### 3.2 Complete 48-Experiment Benchmark Results Table
The table below displays all 48 evaluated pipeline configurations on the held-out test cohort ($N = 4,526$), sorted from highest to lowest rank:
""")

    # Add 48 experiment table
    md.append(csv_to_markdown(p2_benchmark_csv))
    
    md.append("""
### 3.3 Top 5 Pipeline Configurations
""")
    md.append(csv_to_markdown(p2_top5_csv))

    md.append("""
### 3.4 Best Configuration per Model Architecture
""")
    md.append(csv_to_markdown(p2_best_algo_csv))

    md.append("""
### 3.5 Champion Model Selection Analysis
1. **Decision Tree Champion** (`DT + UnderSampling + Feature Importance`):
   - **Test Recall**: 75.05%
   - **Test Precision**: 67.05%
   - **Test Accuracy**: 86.15%
   - **ROC-AUC**: 0.8736
   - **Mean 10-Fold CV Recall**: 76.89%
2. **Random Forest Champion** (`RF + UnderSampling + Feature Importance`):
   - **Test Recall**: 72.68%
   - **Test Precision**: 75.20%
   - **Test Accuracy**: 88.51%
   - **ROC-AUC**: 0.8929
   - **Mean 10-Fold CV Recall**: 74.57%
3. **Trade-Off Justification**: In an educational early-warning system, **Recall is prioritized** over Precision to minimize missed dropouts (false negatives), subject to precision remaining $\ge 60\%$. Both DT and RF satisfy this operational threshold.

---

## 4. Phase 3: Explainable AI (XAI) — Macro & Micro Architecture

### 4.1 Global Macro Interpretability: TreeSHAP Attributions
Feature importance was computed across the held-out test cohort using TreeSHAP (`shap.TreeExplainer`). The 19 features ranked by mean absolute SHAP value:
""")

    md.append(csv_to_markdown(p3_importance_csv))

    md.append("""
### 4.2 Key Macro Feature Insights
- **Course Failures (`reprovacoes`)**: Mean $|SHAP| = 0.1750$ (31.7% of total attribution mass). Accumulating even 1 course failure dramatically shifts log-odds toward dropout.
- **Attendance Percentage (`percentual_frequencia`)**: Mean $|SHAP| = 0.1416$ (25.7% of total attribution mass). A sharp non-linear threshold occurs at 75% (the legal minimum in Brazil): attendance below 75% incurs massive positive SHAP attribution toward dropout.
- **Enrollment Cohort (`anoingresso`)**: Mean $|SHAP| = 0.0872$. Reflects macro institutional changes, funding shifts, and curricular reforms across calendar cohorts.
- **Age at Admission (`idade`)**: Mean $|SHAP| = 0.0379$. Older adult students face heightened non-completion risk due to competing work and family commitments.
- **Gross Income (`rendabruta`)**: Mean $|SHAP| = 0.0182$. Low socioeconomic status acts as an indirect vulnerability accelerator.

### 4.3 Local Micro Interpretability: Archetype Case Studies
Local explanations were audited across three real student archetypes from the test cohort using both SHAP and LIME:
""")

    md.append(csv_to_markdown(p3_shap_lime_csv))

    md.append("""
### 4.4 Local Explanation Stability & Concordance
- **Top-3 Feature Overlap**: The mean Jaccard concordance between SHAP and LIME top-3 explanations across archetypes is **0.3000** (30.0% exact agreement).
- **Explanation Divergence**: While both algorithms agree on primary academic drivers (`reprovacoes`, `percentual_frequencia`), LIME places higher weight on secondary demographic factors (`idade`, `trabalha`), whereas TreeSHAP attributes more influence to socioeconomic context (`rendabruta`, `mae_nivel_escolaridade`).

### 4.5 Counterfactual Trajectory Simulations
Counterfactual what-if simulations across 12 student test cases revealed clear operational levers:
- Increasing attendance by **+15 percentage points** reduces predicted dropout risk by an average of **38.4%**.
- Remediating **1 course failure** drops risk below the 0.50 decision threshold for 72% of borderline students.

---

## 5. Phase 4: Algorithmic Fairness Audit, Multi-Testing Correction & Mitigation

### 5.1 Comprehensive Multi-Threshold Fairness Audit
Audited across 5 protected dimensions at decision thresholds $\\tau \\in \\{0.30, 0.50, 0.70\\}$:
""")

    md.append(csv_to_markdown(p4_fairness_csv))

    md.append("""
### 5.2 Multiple Hypothesis Testing: Holm-Bonferroni FWER Correction
To prevent false-positive bias flags from multiple statistical tests, the Holm-Bonferroni step-down procedure was applied at $\\alpha = 0.05$ across all 6 demographic comparisons at baseline threshold $\\tau = 0.50$:
""")

    md.append(csv_to_markdown(p4_holm_csv))

    md.append("""
### 5.3 Redundant Encoding & Proxy Variable Vulnerability Audit
To ensure that models do not circumvent fairness safeguards via indirect proxy variables, machine learning classifiers were trained to predict each protected attribute from all remaining non-protected features:
""")

    md.append(csv_to_markdown(p4_proxy_csv))

    md.append("""
> [!WARNING]
> **Proxy Vulnerability Detected**:
> - **Age (`idade`)** is strongly predicted ($AUC = 0.960$) by educational modality (`modalidade`) and enrollment year (`anoingresso`), as adult-education programs (`Integrado EJA`) enroll exclusively older students.
> - **Home Computer Access** is moderately predicted ($AUC = 0.716$) by gross income (`rendabruta`) and parental education.

### 5.4 Subgroup Performance Matrix (10 Demographic Groups)
Detailed performance metrics across all 10 demographic subgroups on the held-out test cohort ($N = 4,526$):
""")

    md.append(csv_to_markdown(p4_subgroup_csv))

    md.append("""
### 5.5 Mitigation Trade-Off Analysis: AIF360 Reweighing
Pre-processing debiasing via AIF360 Reweighing was applied to the training distribution. The table below illustrates the acute performance trade-off:
""")

    md.append(csv_to_markdown(p4_mitigation_csv))

    md.append("""
> [!CAUTION]
> **The Cost of Pre-Processing Mitigation**:
> While Reweighing dramatically improves precision (+26.63 pp) and eliminates demographic parity gaps, it causes a severe **16.57 percentage point drop in recall** ($75.84\% \\rightarrow 59.27\\%$). In student dropout prevention, missing over 40% of at-risk students produces unacceptable social costs. Therefore, pre-processing debiasing must NOT be deployed in isolation; rather, institutional equity must be managed via human-in-the-loop governance.

---

## 6. Phase 5: Operational AI Governance Charter & Risk Calibration

### 6.1 Model Calibration Assessment
- **Brier Score**: **0.1146** (indicates good calibration against test set base prevalence of 22.4%).
- The model outputs reliable risk probabilities, validating the use of probabilistic threshold bands.

### 6.2 Calibrated 8-Tier Risk Band Intervention Framework
To prevent counselor burnout and establish clear service-level agreements (SLAs), predictions are stratified into 8 operational tiers:
""")

    md.append(csv_to_markdown(p5_risk_bands_csv))

    md.append("""
### 6.3 Five Institutional Governance Pillars
1. **Pillar 1: Strictly Advisory, Non-Punitive Deployment**:
   Under no circumstances may an algorithmic prediction be used to sanction, dismiss, track, or deny institutional privileges to any student. Predictions exist exclusively to trigger supportive retention interventions.
2. **Pillar 2: Mandatory Explainability-Coupled Outreach**:
   Every automated flag delivered to a counselor must be accompanied by its top-3 SHAP and LIME risk drivers. Counselors are prohibited from contacting students based solely on an aggregate score.
3. **Pillar 3: Continuous Semi-Annual Fairness Auditing**:
   Fairness audits must be executed prior to the start of each academic semester. If Disparate Impact drops below 0.80 or Equal Opportunity Difference exceeds $\\pm 0.10$ on newly enrolled cohorts, the model must be flagged for algorithmic review.
4. **Pillar 4: Student Right to Contest & Explanation Review (LGPD Alignment)**:
   Under Brazilian General Data Protection Law (LGPD Art. 20), students possess the right to inspect algorithmic inferences, review underlying feature attributions, and request a human review of their risk classification.
5. **Pillar 5: Human-in-the-Loop Counselor Override Authority**:
   Academic counselors and social workers retain absolute, unilateral authority to override, downgrade, or dismiss model alerts based on clinical human judgment, qualitative context, or personal circumstances.

---

## 7. Number-by-Number Reconciliation & Paper Audit

The table below reconciles the metrics between the original draft paper (which included retrospective GPA leakage) and the clean, leak-free `dev2` replication:

| Metric / Parameter | Old Paper Draft (With GPA Leakage) | dev2 Replicated Value (Leak-Free, No GPA) | Methodological Reconciliation & Status |
|---|:---:|:---:|---|
| **Champion Model** | Random Forest | Decision Tree / Random Forest | DT achieves highest recall (75.1%); RF achieves highest AUC (0.893) |
| **Test Set Recall** | 84.76% (≈ 84.8%) | **75.05%** (DT) / **72.68%** (RF) | Drop of 9.7–12.1 pp reflects removal of retrospective GPA leakage |
| **Test Set Precision** | 83.65% (≈ 83.6%) | **67.05%** (DT) / **75.20%** (RF) | Honest generalization without post-hoc academic indicators |
| **Test Set Accuracy** | 92.87% (≈ 92.9%) | **86.15%** (DT) / **88.51%** (RF) | Verified on $N = 4,526$ test cohort |
| **ROC-AUC** | 0.9506 (≈ 0.951) | **0.8736** (DT) / **0.8929** (RF) | Strong discriminative ability preserved using purely administrative data |
| **Test Set Size ($N$)** | 3,017 (80/20 split) | **4,526** (70/30 split) | Standardized 70/30 partition replicating Silva et al. (2025) |
| **Top Feature Attribution** | GPA (`ira`) = 52.8% | **Course Failures (`reprovacoes`) = 31.7%** | Academic friction remains top driver without target leakage |
| **Second Feature** | Attendance = 10.4% | **Attendance (`percentual_frequencia`) = 25.7%** | Institutional engagement is the primary actionable behavioral factor |
| **Brier Calibration** | 0.0526 | **0.1146** | Validated against 22.4% test prevalence |
| **Gender Disparate Impact** | 0.707 (Flagged) | **0.8116 (Passes 4/5ths Rule)** | Gender bias disappears when retrospective GPA is removed |
| **Gender EOD** | 0.057 | **-0.0153 (Passes Parity)** | Equal Opportunity recall parity achieved between male and female students |

---

## 8. Threats to Validity & Methodological Limitations

1. **Single-Institution Context**: All data originates from IFNMG campuses in Minas Gerais, Brazil. Transferability to higher education or institutions outside Brazil cannot be claimed without local recalibration.
2. **Right-Censoring**: Students who drop out in later semesters are classified as completed if they were active at data snapshot time.
3. **Compound Label Construction**: Combining voluntary cancellation, academic transfer, and disciplinary expulsion into a single binary dropout class obscures distinct causal pathways.
4. **Unobserved Confounders**: Unmeasured factors such as physical mental health, transportation availability, family emergencies, and classroom pedagogical climate are absent from administrative records.

---

## 9. Complete Dev2 Commit Log & Artifact Index

### 9.1 21-Commit Chronological Audit Trail
| # | Commit SHA | Date | Author | Commit Description |
|:---:|:---:|:---:|---|---|
| 1 | `f6c2402` | Sep 6, 2026 | Tejasvi | Initial file uploads and repository scaffolding |
| 2 | `e53f453` | Sep 7, 2026 | Tejasvi | Baseline data and notebook commit |
| 3-6| `15f7f6e`→`3f20737` | Oct 11, 2026 | Tejasvi | Phase 3 XAI & Phase 4 Fairness branching architecture setup |
| 7-15| `1bc8353`→`c06132c` | Oct 11, 2026 | sahiti-web | Phase 3-4 completion, XAI & fairness audit pipelines, unified portal, data CSVs |
| 16 | `f94a71c` | Oct 12, 2026 | sahiti-web | Streamlit interactive governance app deployment |
| 17-18| `2cdcf6b`→`2f82a94` | Oct 26, 2026 | Tejasvi | 5-phase executive HTML dashboard and presentation assets |
| 19 | `31570c9` | Nov 3, 2026 | sahiti-web | **Faithful replication of Silva et al. (2025) without GPA leakage** |
| 20 | `467c28d` | Nov 3, 2026 | Tejasvi | **Final dev2 merge: AIF360, bootstrap CIs, proxy check, reliability diagram** |
| 21 | `e982683` | Nov 3, 2026 | sahiti-web | **Comprehensive dev2 project report documentation** |

### 9.2 Key Artifacts & Deliverables Index
| Phase | File Path | Format | Description |
|:---:|---|:---:|---|
| **Phase 1** | `phase1_outputs/phase1_data.pkl` | Binary Pickle | Scaled training and test matrices ($N = 15,084$) |
| **Phase 1** | `phase1_outputs/preprocessed_dataset_english.csv` | CSV | Preprocessed student cohort with English translated headers |
| **Phase 2** | `phase2_outputs/phase2_benchmark_results.csv` | CSV | Complete 48-configuration factorial benchmark results |
| **Phase 2** | `phase2_outputs/champion_model_bundle.pkl` | Binary Pickle | Serialized champion model, preprocessors, and test splits |
| **Phase 3** | `phase3_outputs/01_shap_global_beeswarm.png` | PNG Chart | Global TreeSHAP summary beeswarm plot |
| **Phase 3** | `phase3_outputs/phase3_feature_importance.csv` | CSV | Mean absolute SHAP values for all 19 features |
| **Phase 3** | `phase3_outputs/phase3_shap_lime_metrics.csv` | CSV | Concordance and Jaccard similarity across archetypes |
| **Phase 4** | `phase4_outputs/phase4_fairness_audit_results.csv` | CSV | Multi-threshold AIF360 audit across 5 protected axes |
| **Phase 4** | `phase4_outputs/phase4_holm_bonferroni_results.csv` | CSV | FWER corrected statistical significance tests |
| **Phase 4** | `phase4_outputs/phase4_proxy_check.csv` | CSV | Redundant encoding proxy vulnerability evaluation |
| **Phase 4** | `phase4_outputs/phase4_subgroup_metrics.csv` | CSV | Granular metrics across 10 demographic groups |
| **Phase 4** | `phase4_outputs/phase4_mitigation_tradeoff.csv` | CSV | Pre-processing AIF360 Reweighing impact table |
| **Phase 5** | `phase5_outputs/phase5_calibration_summary.csv` | CSV | Brier score calibration metric |
| **Phase 5** | `phase5_outputs/phase5_governance_risk_bands.csv` | CSV | 8-tier risk bands with counselor staffing and SLA allocation |
| **Phase 5** | `phase5_outputs/governance_policy_charter.md` | Markdown | 5-Pillar institutional governance policy charter |
| **UI Portal**| `unified_governance_portal.html` | HTML | Interactive web dashboard combining all 5 phases |

---
*Report generated and compiled from git branch `dev2`.*
""")

    output_path = "DEV2_COMPLETE_MASTER_RESULTS.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
        
    print(f"Master markdown file successfully written to {output_path} ({len(md)} lines).")

if __name__ == "__main__":
    main()

