# Explainable AI Governance Framework for Fair Student Performance Evaluation

## Project Overview
This project replicates and extends a methodology for predicting student dropout in secondary-level technical education in Brazil. The core goal is to build an end-to-end pipeline covering data preparation, class balancing, model training, explainability (XAI), and a fairness audit, culminating in a governance framework.

This project is built on the methodology described in the base paper: *Investigation into Dropout Indicators in Secondary Technical Education* (Silva et al., 2025).

## Architecture Phases
- [x] **Phase 1: Data Preparation & Translation** 
  - Data cleaning, IQR outlier winsorization, missing value handling, categorical encoding, stratified train/test split.
  - Creation of a Portuguese-to-English translation layer for reporting and explainability labels.
- [ ] **Phase 2: Model Training & Evaluation** (In Progress)
  - Class balancing (RandomUnderSampler, SMOTE, SMOTEENN).
  - Feature selection (ANOVA, Backward Selection, Feature Importance).
  - GridSearchCV hyperparameter tuning across RF, DT, LR, and SVM.
  - Performance ranking based on Recall, Precision, and 10-fold CV.
- [ ] **Phase 3: Explainability (XAI)**
  - Application of SHAP and LIME to the top-performing models (RF and DT).
  - Extraction of global and local feature importance.
- [ ] **Phase 4: Fairness Audit & Governance**
  - Auditing model decisions for bias across sensitive attributes (e.g., race, gender).
  - Development of the governance framework for fair student evaluation.

## Environment Setup
1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Reproducing Phase 1
1. Ensure the raw dataset `dataset_evasao_MDE.xlsx` is present in the root directory.
2. Run the data preparation script:
   ```bash
   python phase1_data_preparation.py
   ```
   This generates `phase1_data.pkl` and `feature_names.txt` in the `phase1_outputs/` directory.
3. Run the translation script to generate English/Portuguese CSVs and mapping dictionaries:
   ```bash
   python translate_dataset.py
   ```
