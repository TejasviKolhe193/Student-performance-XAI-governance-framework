# Phase 2 Executive Summary: Model Training, Balancing & Evaluation

**Experiment Scope**: 48 Systematic Machine Learning Experiments  
**Target Variable**: Dropout Prediction (`0 = Completed`, `1 = Dropped Out`)  
**Data Partition**: 12,067 Training Samples | 3,017 Held-out Test Samples  

---

## 1. Selected Champion Models for Phase 3 (Explainable AI)

| Role | Model Architecture | Balancing Strategy | Feature Selection | Recall | Precision | F1-Score | AUC-ROC | Accuracy |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Primary Predictor** | **Random Forest** | Random UnderSampling | Feature Importance | **0.848** | **0.836** | **0.842** | **0.951** | **92.9%** |
| **Interpretable Surrogate** | **Decision Tree** | Random UnderSampling | ANOVA F-Test | **0.846** | **0.640** | **0.729** | **0.854** | **85.9%** |

---

## 2. Test Set Confusion Matrices (Out of 3,017 Real Students)

### Best Random Forest (RF)
* **Actual Dropouts Caught**: **573** out of 676 (84.8% Sensitivity)
* **Missed Dropouts (False Negatives)**: 103 students
* **False Alarms (False Positives)**: 112 students out of 2,341 completed
* **True Completers (True Negatives)**: **2,229** students

### Best Decision Tree (DT)
* **Actual Dropouts Caught**: **572** out of 676 (84.6% Sensitivity)
* **Missed Dropouts (False Negatives)**: 104 students
* **False Alarms (False Positives)**: 322 students out of 2,341 completed
* **True Completers (True Negatives)**: **2,019** students

---

## 3. Best Model for Each Evaluated Algorithm

| Algorithm | Best Configuration | Recall | Precision | F1-Score | AUC-ROC | Accuracy | 10-CV Recall |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Random Forest (RF)** | UnderSampling + FeatureImportance | **0.848** | **0.836** | **0.842** | **0.951** | **92.9%** | 0.878 |
| **Decision Tree (DT)** | UnderSampling + ANOVA | **0.846** | **0.640** | **0.729** | **0.854** | **85.9%** | 0.879 |
| **Logistic Regression (LR)** | SMOTEENN + Backward Selection | **0.787** | **0.718** | **0.751** | **0.899** | **88.3%** | 0.862 |
| **Support Vector Machine (SVM)** | SMOTEENN + ANOVA | **0.914** | **0.231** | **0.369** | **0.591** | **30.1%** | 0.873 |

---

## 4. Key Takeaways & Research Insights

1. **Random UnderSampling Was the Most Effective Strategy**:
   Balancing the training set 50/50 using Random UnderSampling produced the most well-calibrated classifiers for both Random Forest and Decision Tree. It maximized Recall without sacrificing Precision.
2. **Academic Features Dominate Prediction**:
   Academic Performance Index (`ira`), Failed Courses (`reprovacoes`), and Class Attendance (`percentual_frequencia`) account for over **65%** of the predictive weight in the champion Random Forest model.
3. **SVM Degenerate Solution**:
   While SVM ranked high in raw Recall (0.914), it exhibited pathological classification bias (flagging ~90% of students as dropouts, dropping precision to 23%). Random Forest is by far the superior institutional choice.

---

## 5. Visualizations Generated in `phase2_outputs/`
* `01_model_comparison.png` — Grouped bar chart comparing the 4 architectures.
* `02_confusion_matrices.png` — Side-by-side heatmaps of RF vs DT confusion matrices.
* `03_roc_curves.png` — Discrimination power curves (AUC).
* `04_balancing_strategy_impact.png` — Scatter analysis of Recall vs Precision across all 48 models.
* `05_top_features_importance.png` — Gini feature importance ranking in the champion model.
* `phase2_dashboard.html` — Interactive web dashboard.
