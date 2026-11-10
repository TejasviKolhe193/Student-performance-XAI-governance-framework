# Student Dropout XAI & Governance Framework

> **Institution / Dataset:** Instituto Federal do Maranhão (IFMA), Brazil — public cohort from Silva et al. (IEEE RITA 2025)  
> **Cohort:** 15,084 secondary technical students (2010–2022)  
> **Target Variable:** Binary dropout classification — `0 = Completed (77.6%)`, `1 = Dropped Out (22.4%)`  
> **Global Seed:** `42` (see `seeds.txt`)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture Overview](#2-architecture-overview)
3. [Project Structure](#3-project-structure)
4. [Technologies & Dependencies](#4-technologies--dependencies)
5. [Quick Start](#5-quick-start)
6. [Step-by-Step Pipeline Execution](#6-step-by-step-pipeline-execution)
   - [Phase 1 — Data Preparation](#phase-1--data-preparation)
   - [Phase 2 — Model Training (48-Experiment Benchmark)](#phase-2--model-training-48-experiment-benchmark)
   - [Phase 3 — Explainability (TreeSHAP + LIME)](#phase-3--explainability-treeshap--lime)
   - [Phase 4 — Fairness Audit](#phase-4--fairness-audit)
   - [Phase 5 — Governance & Risk Bands](#phase-5--governance--risk-bands)
7. [Running the Interactive Dashboard](#7-running-the-interactive-dashboard)
8. [Configuration](#8-configuration)
9. [Output Artifacts](#9-output-artifacts)
10. [Champion Model Results](#10-champion-model-results)
11. [Fairness Audit Summary](#11-fairness-audit-summary)
12. [Governance Charter](#12-governance-charter)
13. [Methodology Notes & Limitations](#13-methodology-notes--limitations)
14. [References](#14-references)

---

## 1. Project Overview

This project implements an end-to-end, explainable and fairness-audited AI framework for classifying student dropout risk in public vocational secondary education. It re-analyses the publicly released administrative cohort from Silva et al. (*IEEE RITA 2025*) covering 15,084 students at IFMA, Brazil.

The pipeline is designed around four principles:

- **No target leakage.** Cumulative GPA (`ira`) is excluded because it is computed retrospectively across a student's entire enrolment and would inflate measured performance. All preprocessing is fitted exclusively inside cross-validation training folds.
- **Transparent benchmarking.** A 48-experiment factorial grid (4 classifiers × 4 class balancers × 3 feature selectors) is run with 10-fold nested cross-validation, and the champion model is selected by a formal utility rule (maximize Recall subject to Precision ≥ 60% and CV ROC-AUC ≥ 0.90).
- **Dual explainability.** Global TreeSHAP attributions identify institution-wide feature importance; local LIME and SHAP waterfall plots provide per-student counselor-facing explanations.
- **Fairness governance.** Five demographic axes are audited with Disparate Impact screening and Holm-Bonferroni-corrected Equal Opportunity testing. A five-pillar institutional AI governance charter is generated as a proposed operational design.

---

## 2. Architecture Overview

```
Raw Dataset (N = 48,311 records)
        │
        ▼ [Phase 1] Cohort Filtering → 15,084 secondary technical terminal records
        │           Drop IDs, >20% missing columns, IQR winsorization, one-hot encoding
        │           70/30 stratified split → Train: 10,558 | Test: 4,526
        │
        ▼ [Phase 2] 48-Experiment Benchmark
        │           4 Classifiers × 4 Balancers × 3 Feature Selectors
        │           Nested 10-fold leak-free CV on training set
        │           Champion: RF + RandomUnderSampler + TreeImportance(k=19)
        │
        ▼ [Phase 3] Dual XAI
        │           Global: TreeSHAP (beeswarm, mean |SHAP| bar)
        │           Local: SHAP waterfall + LIME bar per student archetype
        │           Concordance: Jaccard overlap of top-3 features
        │
        ▼ [Phase 4] Fairness Audit (τ = 0.50)
        │           5 Protected Axes: Gender, Race, Income, Age, Computer Ownership
        │           Disparate Impact (Four-Fifths Rule), SPD, EOD, FPR gap
        │           Holm-Bonferroni FWER correction; AIF360 Reweighing trade-off
        │
        ▼ [Phase 5] Governance & Risk Calibration
                    Brier score reliability diagram (10-bin)
                    Discrete heuristic risk bands: Emergency / High Priority / Watchlist / Low Concern / Minimal
                    Five-pillar institutional AI governance charter
                    Interactive Streamlit portal (app.py)
```

---

## 3. Project Structure

```
student-performance-xai-governance-framework/
│
├── dataset_evasao_MDE.xlsx          # Raw institutional dataset (download separately — see §5)
├── config.yaml                      # Shared pipeline configuration
├── requirements.txt                 # Python dependencies
├── seeds.txt                        # Global seed log (42)
│
├── ─── PIPELINE ENTRY POINTS ───────────────────────────────────────────────
├── run_step1_step2.py               # Execute Phase 1 + Phase 2 sequentially
├── run_step3_step4.py               # Execute Phase 3 + Phase 4 sequentially
├── run_step5_fairness_audit.py      # Standalone Phase 4 fairness audit
├── run_step6_governance.py          # Phase 5: risk bands + governance charter
├── run_phase1.py                    # Phase 1 standalone runner
├── run_phase2.py                    # Phase 2 standalone runner
├── run_phase3.py                    # Phase 3 standalone runner
├── run_phase4.py                    # Phase 4 standalone runner
├── run_phase5.py                    # Phase 5 standalone runner
│
├── ─── CORE PIPELINE MODULES ───────────────────────────────────────────────
├── phase1_data_preparation.py       # Data loading, filtering, encoding, splitting
├── phase2_model_training.py         # 48-experiment factorial grid, CV, model selection
├── phase2_retrain_no_gpa.py         # GPA-excluded retrain script
├── phase3_explainability_pipeline.py # TreeSHAP global + LIME local explanations
├── phase4_fairness_audit_pipeline.py # 5-axis fairness metrics + Holm-Bonferroni correction
│
├── ─── RESULTS ─────────────────────────────────────────────────────────────
├── results/
│   ├── chosen_model_bundle.pkl              # Serialised champion RF + test predictions
│   ├── step2_full_48_experiments_marked.csv # All 48 experiment results
│   ├── step2_candidate_models_comparison.csv
│   ├── step2_model_performance_summary.csv
│   ├── step4_shap_attributions.csv          # Feature-level SHAP percentages
│   ├── step4_lime_shap_concordance.csv      # Jaccard overlap per archetype
│   ├── step5_main_fairness_audit_tau_050.csv
│   ├── step5_holm_bonferroni_eod.csv
│   ├── step5_reweighing_mitigation_tradeoff.csv
│   ├── step5_appendix_fairness_audit_tau_030_070.csv
│   ├── step6_discrete_risk_bands_audit.csv
│   ├── step6_cumulative_operational_risk_bands.csv
│   ├── step6_governance_policy_charter.md
│   └── fig1_*.png … fig5_*.png             # Publication-grade figures (300 DPI)
│
├── ─── PHASE-SPECIFIC OUTPUTS ──────────────────────────────────────────────
├── phase1_outputs/
│   └── feature_names.txt                    # 23 raw features retained after preprocessing
├── phase3_outputs/
│   ├── cohort_xai_summary.json
│   ├── phase3_xai_dashboard.html
│   └── 05_lime_*.html                       # Per-student LIME HTML reports
├── phase4_outputs/
│   ├── PHASE4_EXECUTIVE_SUMMARY.md
│   ├── phase4_dashboard.html
│   └── interactive_students_xai.json
├── phase5_outputs/
│   └── governance_policy_charter.md
│
├── ─── DASHBOARD ───────────────────────────────────────────────────────────
├── app.py                           # Streamlit interactive governance portal
├── index.html                       # Static HTML landing portal
├── dashboard.html                   # Phase 2 benchmark dashboard
├── unified_governance_portal.html   # Combined governance + fairness portal
│
├── ─── DOCUMENTATION ───────────────────────────────────────────────────────
├── README_DEV2.md                   # This file
├── DEV2_COMPLETE_MASTER_RESULTS.md  # Authoritative empirical results reference
└── docs/
    ├── governance_charter.md
    ├── limitations.md
    └── results_summary.md
```

> **Dataset:** `dataset_evasao_MDE.xlsx` is the raw institutional data file from Silva et al. (IEEE RITA 2025), available at `https://bit.ly/case-sutdy-dropout-xai`. It is not included in the repository. Download it and place it in the project root before running any step.

---

## 4. Technologies & Dependencies

### Core Language

| Tool | Version | Purpose |
|---|---|---|
| **Python** | ≥ 3.9 | All pipeline scripts |

---

### Machine Learning

| Library | Version | Purpose |
|---|---|---|
| **scikit-learn** | ≥ 1.3.0 | Random Forest, Decision Tree, Logistic Regression, Linear SVM classifiers; `StratifiedKFold` cross-validation; `SelectKBest` (ANOVA F-test) and `SequentialFeatureSelector` (backward elimination) for feature selection; classification metrics (precision, recall, F1, ROC-AUC, accuracy, Brier score) |
| **imbalanced-learn** | ≥ 0.14.0 | Class balancing strategies: `RandomUnderSampler`, `SMOTE`, `SMOTEENN`; leak-free `imblearn.pipeline.Pipeline` that wraps all preprocessing steps inside CV folds |
| **joblib** | ≥ 1.3.0 | Model serialisation and loading (`.pkl` bundles) |

---

### Explainability (XAI)

| Library | Version | Purpose |
|---|---|---|
| **shap** | ≥ 0.51.0 | `TreeExplainer` for global beeswarm and mean \|SHAP\| importance bar charts across the full test cohort (N = 4,526); local waterfall plots per student; uses path-dependent conditional expectations without background subsampling |
| **lime** | ≥ 0.2.0.1 | `LimeTabularExplainer` for local surrogate explanations per student; top-3 feature concordance with SHAP measured via Jaccard overlap |

---

### Fairness Auditing

| Library | Version | Purpose |
|---|---|---|
| **aif360** | ≥ 0.6.1 | IBM AI Fairness 360 toolkit; `BinaryLabelDataset` and `Reweighing` pre-processor for training sample weight adjustment as a gender-fairness mitigation strategy; trade-off analysis vs. recall penalty |
| **scipy** | ≥ 1.12.0 | `chi2_contingency` for per-axis Equal Opportunity Difference p-values; Holm-Bonferroni step-down family-wise error rate (FWER) correction across 4 EOD hypotheses |

---

### Data Handling

| Library | Version | Purpose |
|---|---|---|
| **pandas** | ≥ 2.0.0 | Dataset loading (`.xlsx`), preprocessing, CSV output |
| **numpy** | ≥ 1.24.0 | Array operations, IQR winsorization, probability calibration |
| **openpyxl** | ≥ 3.1.0 | Reading the raw `.xlsx` dataset file |
| **pyarrow** | ≥ 26.0.0 | Backend for Streamlit dataframe rendering |

---

### Visualization

| Library | Version | Purpose |
|---|---|---|
| **matplotlib** | ≥ 3.7.0 | 300 DPI publication-grade figures: 10-bin reliability diagram, SHAP beeswarm and importance bar, 4-panel fairness audit dashboard, risk band calibration chart, modality dropout rate chart |
| **plotly** | ≥ 5.18.0 | Interactive charts inside the Streamlit dashboard |
| **Pillow** | ≥ 10.0.0 | Image loading and processing for dashboard figure panels |

---

### Interactive Dashboard

| Library | Version | Purpose |
|---|---|---|
| **Streamlit** | ≥ 1.30.0 | `app.py` interactive governance portal — multi-tab layout covering model results, SHAP plots, fairness tables, risk band viewer, and governance charter |

---

## 5. Quick Start

### Prerequisites

- Python 3.9 or higher installed
- `dataset_evasao_MDE.xlsx` downloaded and placed in the project root (download from `https://bit.ly/case-sutdy-dropout-xai`)

### Step 1 — Clone the repository

```bash
git clone <repo-url>
cd student-performance-xai-governance-framework
```

### Step 2 — Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### Step 3 — Install all dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Place the dataset

Download `dataset_evasao_MDE.xlsx` from `https://bit.ly/case-sutdy-dropout-xai` and move it into the **project root** directory.

### Step 5 — Run the full pipeline

```bash
python run_step1_step2.py      # Phase 1: data prep + Phase 2: model training
python run_step3_step4.py      # Phase 3: explainability + Phase 4: fairness audit
python run_step6_governance.py # Phase 5: governance charter + risk bands
```

### Step 6 — Launch the interactive dashboard

```bash
streamlit run app.py
```

---

## 6. Step-by-Step Pipeline Execution

### Phase 1 — Data Preparation

**Script:** `phase1_data_preparation.py`  
**Runner:** `python run_phase1.py`

**Purpose:** Transform the raw institutional xlsx file into clean, stratified train and test arrays.

**Detailed steps:**

1. **Load** `dataset_evasao_MDE.xlsx` — 48,311 raw institutional records across all modalities and enrolment statuses.

2. **Modality filter** — Removes 12,038 higher-education records; retains 36,273 secondary technical records.

3. **Terminal status filter** — Removes 21,189 currently-enrolled (non-terminal) students; yields **15,084 terminal student records** with known outcomes.

4. **Binary target construction** from the `situacao` column:
   - `Class 0 — Completed` (N = 11,703, 77.59%)
   - `Class 1 — Dropout / Non-completion` (N = 3,381, 22.41%)  
     Comprises: voluntary evasão (1,760) + cancelado (446) + compulsório (346) + jubilado (38) + transferido externo (791)

5. **Feature dropping:**
   - Identifier columns (`alunoid`) removed.
   - Columns with > 20% missing values dropped: `dataconclusao`, `forma_acesso_seletivo`, `razao_ausencia_educacional`, `pontuacao_seletivo`.
   - Cumulative GPA (`ira`) excluded — it is computed retrospectively across full enrolment and constitutes target leakage.
   - **Remaining: 23 raw administrative features** (see `phase1_outputs/feature_names.txt`).

6. **Imputation** — Median imputation for `quantidade_computadores` (minor missingness in home computer ownership column).

7. **Winsorization** — 1.5× IQR cap applied to continuous skewed features: `idade`, `rendabruta`, `quantidade_computadores`, `quantidade_notebooks`, `qtd_filhos`. Bounds are computed on the training set only.

8. **One-hot encoding** — Categorical variables expanded to 34 total binary columns.

9. **Stratified 70/30 split** (`random_state=42`):
   - **Training set:** N = 10,558 (Class 0: 8,191 | Class 1: 2,367; dropout rate 22.42%)
   - **Held-out test vault:** N = 4,526 (Class 0: 3,512 | Class 1: 1,014; dropout rate 22.40%)

**Key outputs:** Preprocessed training and test arrays written for use in Phase 2.

---

### Phase 2 — Model Training (48-Experiment Benchmark)

**Script:** `phase2_model_training.py`  
**Runner:** `python run_phase2.py`

**Purpose:** Systematically identify the best performing model configuration under a formal operational utility rule using a fully leak-free nested cross-validation protocol.

**The 48-experiment factorial grid:**

| Dimension | Options (count) |
|---|---|
| **Classifiers** | Random Forest, Decision Tree, Logistic Regression, Linear SVM (4) |
| **Class Balancers** | Unbalanced (no resampling), `RandomUnderSampler`, `SMOTE`, `SMOTEENN` (4) |
| **Feature Selectors** | ANOVA F-test (`SelectKBest`), Backward Elimination (`SequentialFeatureSelector`), Tree Feature Importance k=19 (3) |

**Leak-free protocol:**  
Every balancer, feature selector, imputer, and encoder is wrapped inside an `imblearn.pipeline.Pipeline`. This guarantees they are fitted exclusively on each training fold and never see validation or test data.

**Cross-validation:** 10-fold stratified CV on the 10,558-student training set.

**Champion selection rule:**  
Maximize Recall (dropout catch rate), subject to:
- CV Precision ≥ 60% (counselor alert precision floor to limit false alarms)
- CV ROC-AUC ≥ 0.90 (minimum discrimination capability)

**Champion configuration:**  
Random Forest + RandomUnderSampler + Tree Feature Importance (k = 19)  
Fixed hyperparameters: `n_estimators=100`, `max_depth=10`, `min_samples_leaf=5`, `min_samples_split=10`, `random_state=42`

| Metric | CV Result (Training) | Test Result (N = 4,526) |
|---|---|---|
| Recall | 74.95% | **73.18%** (95% CI: [70.48%, 76.00%]) |
| Precision | 76.94% | **75.64%** (95% CI: [72.83%, 78.19%]) |
| F1-Score | — | **0.7439** |
| Accuracy | — | **88.71%** |
| ROC-AUC | 0.9144 | **0.8968** (95% CI: [0.8836, 0.9098]) |
| Brier Score | — | **0.1080** (baseline: 0.1738) |

**Confusion matrix (test):** TP = 742, FP = 239, TN = 3,273, FN = 272

**Key outputs:**
- `results/chosen_model_bundle.pkl` — champion model + test predictions
- `results/step2_full_48_experiments_marked.csv` — all 48 results
- `results/step2_candidate_models_comparison.csv` — top candidates side-by-side

---

### Phase 3 — Explainability (TreeSHAP + LIME)

**Script:** `phase3_explainability_pipeline.py`  
**Runner:** `python run_phase3.py`

**Purpose:** Generate both global institution-wide and local per-student explanations using TreeSHAP and LIME, then measure their concordance.

**Global Interpretability — TreeSHAP:**

Runs `shap.TreeExplainer` across all 4,526 test students using path-dependent conditional expectations (no background subsampling). Mean |SHAP| values per feature are normalized to percentage shares.

| Rank | Feature | Description | SHAP Share |
|---|---|---|---|
| 1 | `reprovacoes` | Course failures | 32.37% |
| 2 | `percentual_frequencia` | Attendance percentage | 19.26% |
| 3 | `anoingresso` | Cohort enrolment year | 10.78% |
| — | Top-3 combined | — | **62.41%** |
| — | `genero` (M + F combined) | Gender | 3.66% |

**Local Interpretability — LIME + SHAP concordance:**

Three representative student archetypes are explained using both SHAP waterfall and LIME bar charts. Concordance is measured as Jaccard overlap of their top-3 feature rankings.

| Archetype | Student ID | P(Dropout) | Top-3 Jaccard |
|---|---|---|---|
| High-Risk | #815 | 94.8% | 0.50 |
| Borderline | #4078 | 48.0% | 0.50 |
| Low-Risk | #4458 | 10.7% | 1.00 |

**Key outputs:**
- `results/step4_shap_attributions.csv`
- `results/step4_lime_shap_concordance.csv`
- `results/fig2_shap_beeswarm.png`, `results/fig3_shap_importance.png`
- `phase3_outputs/phase3_xai_dashboard.html`
- Per-student LIME HTML reports: `phase3_outputs/05_lime_*.html`

---

### Phase 4 — Fairness Audit

**Script:** `phase4_fairness_audit_pipeline.py`  
**Runner:** `python run_step5_fairness_audit.py`

**Purpose:** Audit the champion model for systematic demographic bias across five protected dimensions using established fairness metrics and multiple-testing correction.

**Protected dimensions (at τ = 0.50, N = 4,526):**

| Axis | Privileged Group | Unprivileged Group |
|---|---|---|
| Gender | Male (N = 2,135) | Female (N = 2,391) |
| Race | Branca / White (N = 641) | Parda (N = 3,182) and Preta (N = 646) |
| Household Income | Above median R$ 930 (N = 2,254) | At/below median (N = 2,272) |
| Age | ≤ 20 years (N = 2,121) | > 20 years (N = 2,405) |
| Computer Ownership | ≥ 1 device (N = 1,325) | 0 devices (N = 3,201) |

**Metrics computed per axis:**
- **Disparate Impact (DI):** Ratio of positive prediction rates between unprivileged and privileged groups. Screened against the Four-Fifths Rule (0.80 ≤ DI ≤ 1.25).
- **Statistical Parity Difference (SPD):** Absolute difference in prediction rates.
- **Equal Opportunity Difference (EOD):** TPR(unprivileged) − TPR(privileged); p-values from chi-squared test.
- **False Positive Rate (FPR) gap:** FPR(unprivileged) − FPR(privileged).
- **Holm-Bonferroni FWER correction** across 4 EOD p-values (family-wise α = 0.05/4 = 0.0125).

**AIF360 Reweighing mitigation analysis:**  
Applied at the gender axis. Reweighing tightens gender EOD from −0.0422 to −0.0304 but drops recall from 73.18% to 60.36% (−12.82 percentage points), and raises precision from 75.64% to 93.72%. This trade-off demonstrates that algorithmic-only debiasing is insufficient and must be supplemented by institutional human-in-the-loop governance.

**Key outputs:**
- `results/step5_main_fairness_audit_tau_050.csv`
- `results/step5_holm_bonferroni_eod.csv`
- `results/step5_reweighing_mitigation_tradeoff.csv`
- `results/step5_appendix_fairness_audit_tau_030_070.csv` (sensitivity at τ = 0.30, 0.70)
- `results/fig4_fairness_audit.png`

---

### Phase 5 — Governance & Risk Bands

**Script:** `run_step6_governance.py`

**Purpose:** Evaluate probability calibration, partition test students into actionable risk tiers, and generate an institutional governance charter.

**Probability calibration:**  
Brier Score = 0.1080 vs. majority-class baseline 0.1738. A 10-bin reliability diagram (`results/fig1_reliability_diagram.png`) shows the degree of calibration across the full predicted probability range.

**Discrete heuristic risk bands** (mutually exclusive, based on predicted probability):

| Band | Probability Interval | Students | % of Cohort | Observed Dropout | Mean Predicted |
|---|---|---|---|---|---|
| Emergency Tier | [0.80, 1.00] | 567 | 12.53% | 95.24% | 92.20% |
| High Priority Tier | [0.60, 0.80) | 190 | 4.20% | 63.68% | 69.41% |
| Watchlist / Moderate | [0.40, 0.60) | 553 | 12.22% | 26.94% | 48.63% |
| Low Concern | [0.20, 0.40) | 2,072 | 45.78% | 7.82% | 27.99% |
| Minimal Risk | [0.00, 0.20) | 1,144 | 25.28% | 3.67% | 15.49% |

> **Calibration note:** The Watchlist band shows probability inflation caused by `RandomUnderSampler` — the mean predicted rate (48.63%) substantially overestimates the observed dropout rate (26.94%). Raw model probabilities should not be used directly as intervention cutoffs without recalibration for this band.

**Operational projection (5,000-student campus, τ = 0.50):**  
~1,084 students flagged (21.68% selection rate), targeting a 4-week response SLA with 6 FTE academic counselors (~45 cases per counselor per week).

**Key outputs:**
- `results/step6_discrete_risk_bands_audit.csv`
- `results/step6_cumulative_operational_risk_bands.csv`
- `results/step6_governance_policy_charter.md`
- `results/fig5_risk_bands_calibration.png`

---

## 7. Running the Interactive Dashboard

The Streamlit app (`app.py`) is a full governance portal with the following sections:

| Tab / Panel | Content |
|---|---|
| **Overview** | Pipeline summary, cohort statistics, locked test metrics |
| **Phase 2: Benchmark** | 48-experiment results table, champion model card |
| **Phase 3: XAI** | Global SHAP beeswarm and importance bar; local LIME/SHAP archetype explorer |
| **Phase 4: Fairness** | 5-axis fairness audit table and dashboard; Holm-Bonferroni table; Reweighing trade-off |
| **Phase 5: Governance** | Risk band calibration chart; five-pillar charter text; operational staffing calculator |

```bash
# From the project root with the venv activated:
streamlit run app.py
```

The dashboard runs locally at `http://localhost:8501` by default. Open this URL in any browser after the command starts.

---

## 8. Configuration

All shared pipeline parameters are centrally defined in `config.yaml`:

```yaml
preprocessing:
  target_col: "situacao"           # Raw outcome column in the xlsx
  missing_threshold: 0.20          # Drop any column with >20% missing values
  winsorization:
    multiplier: 1.5                # 1.5× IQR cap for continuous features
    target_columns:
      - idade
      - rendabruta
      - quantidade_computadores
      - quantidade_notebooks
      - qtd_filhos
  split:
    test_size: 0.30                # 70/30 split
    random_state: 42               # Global reproducibility seed
    stratify: true

modeling:
  models: [RF, DT, LR, SVM]
  balancing_strategies: [Unbalanced, UnderSampling, SMOTE, SMOTEENN]
  feature_selection: [ANOVA, Backward, FeatureImportance]
  cv_folds: 10
```

---

## 9. Output Artifacts

After running all phases, the following key files are produced in `results/`:

| File | Description |
|---|---|
| `chosen_model_bundle.pkl` | Champion RF model, test features, labels, and predicted probabilities |
| `step2_full_48_experiments_marked.csv` | All 48 experiment CV + test metrics |
| `step2_candidate_models_comparison.csv` | Top 2 candidate models side-by-side |
| `step4_shap_attributions.csv` | SHAP percentage shares per feature |
| `step4_lime_shap_concordance.csv` | Jaccard overlap per student archetype |
| `step5_main_fairness_audit_tau_050.csv` | Full fairness metrics table at τ = 0.50 |
| `step5_holm_bonferroni_eod.csv` | Holm-corrected EOD p-values across all axes |
| `step5_reweighing_mitigation_tradeoff.csv` | AIF360 Reweighing recall/precision trade-off |
| `step6_discrete_risk_bands_audit.csv` | Risk band counts, observed and predicted dropout rates |
| `step6_governance_policy_charter.md` | Five-pillar institutional governance charter |
| `fig1_reliability_diagram.png` | 10-bin probability reliability diagram |
| `fig2_shap_beeswarm.png` | Global SHAP beeswarm (all 4,526 test students) |
| `fig3_shap_importance.png` | Mean \|SHAP\| percentage bar chart |
| `fig4_fairness_audit.png` | 4-panel fairness audit dashboard |
| `fig5_risk_bands_calibration.png` | Risk band calibration chart |

---

## 10. Champion Model Results

```
Random Forest — Champion Model
─────────────────────────────────────────────────────────
Configuration : RandomUnderSampler + TreeImportance(k=19)
Hyperparameters: n_estimators=100, max_depth=10,
                  min_samples_leaf=5, min_samples_split=10,
                  random_state=42
─────────────────────────────────────────────────────────
Test Cohort   : N = 4,526 students
─────────────────────────────────────────────────────────
Recall        : 73.18%  (95% CI: [70.48%, 76.00%])
Precision     : 75.64%  (95% CI: [72.83%, 78.19%])
F1-Score      : 0.7439
Accuracy      : 88.71%
ROC-AUC       : 0.8968  (95% CI: [0.8836, 0.9098])
Brier Score   : 0.1080  (majority-class baseline: 0.1738)
─────────────────────────────────────────────────────────
Confusion     : TP = 742  |  FP = 239
Matrix          TN = 3,273 |  FN = 272
─────────────────────────────────────────────────────────
```

---

## 11. Fairness Audit Summary

Audited at τ = 0.50 on N = 4,526 test students. Holm-Bonferroni family-wise α = 0.05/4 = 0.0125.

| Dimension | DI | EOD | p-value | Holm-Significant? |
|---|---|---|---|---|
| Gender (M vs F) | 0.7383 ❌ | −0.0422 | 0.1354 | No |
| Race (Branca vs Parda) | 1.2958 ❌ | +0.1014 | 0.0144 | No (p > 0.0125) |
| Race (Branca vs Preta) | 1.2694 ❌ | +0.0280 | 0.7042 | No |
| Income (High vs Low) | 1.5098 ❌ | +0.1007 | 0.00043 | **Yes** |
| Age (≤20 vs >20) | 1.2864 ❌ | +0.0126 | 0.6634 | No |
| Computer (≥1 vs 0) | 1.5106 ❌ | +0.1109 | 0.00089 | **Yes** |

All 5 dimensions fail the Four-Fifths screening heuristic (DI outside 0.80–1.25). Income and Computer Ownership show Holm-significant EOD gaps — low-income and device-deprived students have significantly higher model True Positive Rates, consistent with their higher empirical base dropout rates.

---

## 12. Governance Charter

The five-pillar charter (`results/step6_governance_policy_charter.md`) specifies how the model should be operated responsibly in an institutional setting:

| Pillar | Description |
|---|---|
| **1. Strictly Advisory** | Predictions are support-triggering signals only. No automated academic sanctions permitted. |
| **2. Explainability-Coupled Outreach** | Counselors must review per-student SHAP/LIME profiles before contacting any flagged student. |
| **3. Semi-Annual Fairness Auditing** | DI + Holm-corrected EOD reviewed each semester; unscheduled audits triggered by demographic shifts > 10% or prediction volume drift > 15%. |
| **4. LGPD Art. 20 Contestability** | Students receive plain-language notice; may inspect their contributing factors and request recalculation within 10 business days. |
| **5. Human Override Authority** | Certified counselors and social workers retain final, unilateral authority to override algorithmic alerts. |

> **This framework is a proposed operational design and has not been field-tested in any live educational environment.**

---

## 13. Methodology Notes & Limitations

1. **Feature timing constraint:** `reprovacoes` and `percentual_frequencia` are cumulative across enrolment. The model classifies dropout risk at a point-in-time snapshot. It cannot support pre-enrolment early-warning claims and cannot trigger interventions earlier than the recorded academic period.

2. **Label construction:** Voluntary dropout, administrative cancellation, compulsory dismissal, jubilado status, and external transfers are all grouped into Class 1. This conflates heterogeneous attrition pathways.

3. **Right-censoring:** Students still enrolled at the data snapshot date are excluded, creating selection bias favouring observed completers and dropouts over students with uncertain outcomes.

4. **Single institutional network:** The dataset covers one federal institute (IFMA). Results should not be generalised to other institutions without re-validation.

5. **Calibration inflation in Watchlist band:** `RandomUnderSampler` inflates predicted probabilities in the 0.40–0.60 range. The Watchlist mean predicted rate (48.63%) substantially exceeds the observed dropout rate (26.94%). Raw probabilities in this band should not be used directly as intervention thresholds.

6. **Proxy discrimination:** A low SHAP attribution for a protected attribute (e.g., gender 3.66%) does not prove the absence of proxy discrimination through correlated non-protected features such as income, modality, or digital access.

7. **Governance not field-tested:** The five-pillar charter and risk-band thresholds are proposed normative design artefacts. No pilot deployment, counselor workflow study, or randomised intervention trial was conducted.

---

## 14. References

- Silva, F. da C., Santana, A. M., and Feitosa, R. M. (2025). "An investigation into dropout indicators in secondary technical education using explainable AI." *IEEE Rev. Iberoam. Tecnol. Aprendiz.*, vol. 20. doi: 10.1109/RITA.2025.3566095.
- Lundberg, S. M. and Lee, S.-I. (2017). "A unified approach to interpreting model predictions." *NeurIPS*, vol. 30, pp. 4765–4774.
- Ribeiro, M. T., Singh, S., and Guestrin, C. (2016). "'Why should I trust you?': Explaining the predictions of any classifier." *KDD*, pp. 1135–1144.
- Bellamy, R. K. E. et al. (2019). "AI Fairness 360: An extensible toolkit for detecting and mitigating algorithmic bias." *IBM J. Res. Develop.*, vol. 63, no. 4/5, pp. 4:1–4:15.
- Hardt, M., Price, E., and Srebro, N. (2016). "Equality of opportunity in supervised learning." *NeurIPS*, vol. 29, pp. 3315–3323.
- Chawla, N. V. et al. (2002). "SMOTE: Synthetic minority over-sampling technique." *JAIR*, vol. 16, pp. 321–357.
- Kleinberg, J., Mullainathan, S., and Raghavan, M. (2017). "Inherent trade-offs in the fair determination of risk scores." *ITCS*, vol. 67, pp. 43:1–43:23.
