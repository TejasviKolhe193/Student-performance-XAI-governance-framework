# Phase 1: Data Preparation & Bilingual Translation Guide

## Overview
This branch (`phase-1/data-prep`) isolates the foundational **Phase 1 Data Preparation and Translation Pipeline** for the **Student Dropout Prediction & Explainable AI Governance Framework**.

This phase faithfully replicates the data preprocessing methodology of the foundational IEEE research paper:
> **Silva et al., "An Investigation Into Dropout Indicators in Secondary Technical Education Using Explainable AI" (IEEE RITA, 2025).**

---

## 1. Dataset Scope
* **Data Source File**: [`dataset_evasao_MDE.xlsx`](dataset_evasao_MDE.xlsx)
* **Population**: **15,084 students** enrolled across Brazilian public federal technical institutes (*Ensino Técnico de Nível Médio*).
* **Included Course Modalities**:
  - `Integrado`: Regular integrated high school + vocational technical education.
  - `Concomitante`: Concurrent technical program taken in parallel with standard schooling.
  - `Subsequente`: Technical vocational program taken post-high school.
  - `Integrado EJA`: Technical education for adult learners returning to schooling.
  *(Higher education and Bachelor degree programs are excluded to match the research focus).*

---

## 2. Binary Target Construction
The administrative status attribute (`situacao`) is converted into a binary classification target:
* **Class 0 = "Completed" (Graduate)**: Students marked as `Concluído` (77.6% of the cohort).
* **Class 1 = "Dropped Out" (Dropout)**: Students who departed prematurely (22.4% of the cohort):
  - `Evasão` (official dropout)
  - `Cancelado` (cancelled enrollment)
  - `Cancelamento Compulsório` (dismissed for absenteeism)
  - `Jubilado` (exceeded maximum time limit)
  - `Transferido Externo` (transferred to another institution)

*(Active students or those on temporary leave are excluded because their final outcome is not yet determined).*

---

## 3. Preprocessing & Feature Engineering Steps
Executed via [`phase1_data_preparation.py`](phase1_data_preparation.py):

1. **Filtering & ID Removal**:
   - Filter down to 15,084 secondary technical records.
   - Remove non-predictive identifiers (`alunoid`, `campus`, `curso`).
2. **Missing Value Management**:
   - Dropped high-missingness columns (>20% missing): `dataconclusao`, `forma_acesso_seletivo`, `razao_ausencia_educacional`, `pontuacao_seletivo`.
   - Median-imputed low-missingness features: `quantidade_computadores` and `quantidade_notebooks`.
3. **1.5×IQR Outlier Winsorization**:
   - Capped/clipped extreme continuous values at $Q_1 - 1.5\text{IQR}$ and $Q_3 + 1.5\text{IQR}$ for: `idade`, `rendabruta`, `quantidade_computadores`, `quantidade_notebooks`, and `qtd_filhos`.
   - Preserves all 15,084 student samples and the natural 78/22 class balance.
   - Academic causal features (`ira`, `reprovacoes`, `percentual_frequencia`) are intentionally preserved without artificial distortion.
4. **Encoding**:
   - **One-Hot Encoding**: Nominal sensitive attributes (`genero`, `raca`, `estado_civil`).
   - **Ordinal Encoding**: Parental education levels (`mae_nivel_escolaridade`, `pai_nivel_escolaridade`).
   - **Label Encoding**: Modality and binary categories.
5. **Stratified Train/Test Partition**:
   - **80% Training Set**: 12,067 students (9,362 Graduates, 2,705 Dropouts).
   - **20% Test Set**: 3,017 students (2,341 Graduates, 676 Dropouts) — locked away for unbiased model evaluation.

---

## 4. Bilingual Translation Layer
Executed via [`translate_dataset.py`](translate_dataset.py):
* Maps all Portuguese column names (e.g., `ira` → `gpa`, `reprovacoes` → `num_failures`, `situacao` → `student_status`) and categorical value labels into English.
* Saves bilingual dictionary artifacts ensuring all downstream SHAP, LIME, and Governance reports can be presented seamlessly in English.

---

## 5. Execution Instructions

### Environment Setup
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run Data Preprocessing
```bash
python phase1_data_preparation.py
```
*Outputs generated in `phase1_outputs/`:*
* `phase1_data.pkl`: Processed matrices (`X_train`, `X_test`, `y_train`, `y_test`, feature names).
* `train_processed.csv`, `test_processed.csv`.

### Run Translation Pipeline
```bash
python translate_dataset.py
```
*Outputs generated in `phase1_outputs/`:*
* `dataset_english.csv`, `translation_mappings.pkl`.
