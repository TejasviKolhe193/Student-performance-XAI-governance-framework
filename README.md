Here is a complete, beginner-friendly walkthrough that covers **what we are doing**, **what we are predicting**, **the dataset**, and **everything that happened in Phase 2 from start to end**.

---

# Part 1: What Are We Doing & Why?

### The Mission
Student dropout in secondary technical education is a critical issue. When a student drops out, it affects their career prospects, wastes school resources, and exacerbates socioeconomic inequality. 

Our goal is to build an **Explainable AI & Governance System** that:
1. **Predicts early** if a student is at risk of dropping out.
2. **Explains why** the model flagged a student (using Explainable AI: SHAP & LIME) so teachers and counselors can intervene with personalized support.
3. **Audits fairness** to ensure the model doesn't discriminate against students based on race, gender, or family income.

This project replicates and extends a major research paper published in IEEE:  
*Silva et al., "An Investigation Into Dropout Indicators in Secondary Technical Education Using Explainable AI" (IEEE RITA, 2025).*

---

# Part 2: The Dataset & What We Are Predicting

### 1. Where Does the Data Come From?
The dataset (`dataset_evasao_MDE.xlsx`) contains real institutional records from public federal institutes in Brazil offering **secondary technical education** (*Ensino Técnico de Nível Médio*). 

These are 3-to-4 year programs where high school students learn a technical trade (like IT, mechanics, electronics, or chemistry) alongside their standard high school curriculum.

### 2. Who is in the Dataset?
* **15,084 total students** enrolled in secondary technical programs across four course formats:
  - `Integrado`: Regular integrated high school + technical course.
  - `Concomitante`: Concurrent technical course while attending high school elsewhere.
  - `Subsequente`: Specialized technical course taken right after high school.
  - `Integrado EJA`: Technical high school for young adults returning to education.
*(Higher education programs like Bachelor's degrees and Engineering were excluded to match the research focus).*

### 3. What Are We Predicting? (The Target Variable)
We are predicting a binary outcome: **Will this student complete their course, or will they drop out?**

From the official administrative status (`situacao`), we engineered a binary target:
* **Class 0 = "Completed" (Graduate)**: Students marked as `Concluído` (Completed their studies).
* **Class 1 = "Dropped Out" (Dropout)**: Students who left without finishing:
  - `Evasão` (official dropout)
  - `Cancelado` (cancelled enrollment)
  - `Cancelamento Compulsório` (dismissed for absenteeism)
  - `Jubilado` (exceeded the maximum allowable study duration)
  - `Transferido Externo` (transferred out to another institution)

*(Students who are still active, on a temporary leave, or haven't finished yet were excluded because their final outcome isn't known).*

### 4. What Information Do We Know About Each Student? (The 33 Features)
After Phase 1 cleaning, encoding, and preparation, each student is represented by **33 features** categorized into four groups:

1. **Academic Performance**:
   - `ira`: Cumulative Academic Performance Index (grades averaged from 0 to 10).
   - `reprovacoes`: Number of failed courses / subjects.
   - `percentual_frequencia`: Attendance rate (percentage of classes attended).
2. **Course & Educational History**:
   - `anoingresso`: Admission year (e.g., 2018, 2021).
   - `periodoingresso`: Admission semester (1st or 2nd semester).
   - `modalidade`: Type of secondary course (`Integrado`, `Subsequente`, etc.).
   - `ficou_tempo_sem_estudar`: Whether the student took a gap period before enrolling.
   - `exclusivo_rede_publica`: Whether the student went entirely to public elementary school.
   - `idioma`: Foreign language chosen (English vs. Spanish).
3. **Socioeconomic & Living Conditions**:
   - `rendabruta`: Gross monthly family income (in Brazilian Reais).
   - `quantidade_computadores`: Number of desktop computers at home.
   - `quantidade_notebooks`: Number of laptops at home.
   - `tipo_area_residencial`: Urban vs. rural home location.
   - `companhia_domiciliar`: Who the student lives with.
   - `trabalha`: Whether the student already works a job while studying.
   - `qtd_filhos`: Number of children the student has.
4. **Demographics (Protected Sensitive Attributes)**:
   - `idade`: Student age at enrollment.
   - `genero`: Gender (`genero_F`, `genero_M`).
   - `raca`: Self-declared race/ethnicity (`Branca`, `Preta`, `Parda`, `Amarela`, `Indígena`, `Não declarado`).
   - `estado_civil`: Marital status (`Solteiro(a)`, `Casado(a)`, `Divorciado(a)`, `União Estável`, `Viúvo(a)`).
   - `mae_nivel_escolaridade` & `pai_nivel_escolaridade`: Mother's and Father's education level (ranked from *No formal schooling* to *Postgraduate degree*).

### 5. The Train/Test Split
To evaluate our models honestly:
* **Training set (80%)**: **12,067 students** (9,362 Graduates, 2,705 Dropouts) — *used to teach and balance the models.*
* **Testing set (20%)**: **3,017 students** (2,341 Graduates, 676 Dropouts) — *locked away in a vault and only used to test the final models on real, untouched data.*

---

# Part 3: Phase 2 Explained from Start to End

Phase 2 is the **brain of the pipeline**. It answers: **Which machine learning model, trained with what balancing technique and which features, is the best at catching student dropouts?**

We designed a systematic matrix of **48 distinct experiments**:
$$\mathbf{4 \text{ Balancing Strategies}} \times \mathbf{3 \text{ Feature Selection Methods}} \times \mathbf{4 \text{ Machine Learning Algorithms}} = \mathbf{48 \text{ Experiments}}$$

Here is exactly what happened in each step:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: Balance Training Data (4 Strategies)                                │
│   Unbalanced (12k) │ UnderSampling (5.4k) │ SMOTE (18.7k) │ SMOTEENN (15.2k)│
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: Feature Selection (3 Methods)                                       │
│   ANOVA Filter (15 feats) │ Backward Wrapper (17 feats) │ FI Tree (15 feats)│
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: Train 4 Algorithms across all 12 combinations (48 experiments)      │
│   Random Forest (RF) │ Decision Tree (DT) │ Logistic Reg (LR) │ SVM         │
│   • Tune parameters with 5-Fold GridSearchCV                                │
│   • Test on 3,017 held-out students                                         │
│   • Validate with 10-Fold Cross-Validation                                  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: Rank Models (Recall ──► Precision ──► 10-CV) & Save for Phase 3     │
│   Best RF (Recall: 84.8%, Prec: 83.6%) + Best DT (Recall: 84.6%) Saved      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Step 1: Solving Class Imbalance

#### Why was this necessary?
In our training data:
* **77.6%** of students graduated (Class 0).
* Only **22.4%** dropped out (Class 1).

If we didn't balance the data, a machine learning model could achieve a "lazy" **77.6% accuracy** simply by predicting that *nobody ever drops out*. But that defeats our entire purpose! We need the model to be hyper-sensitive to dropouts.

We created **4 versions of the training set** (*only balancing the training data, never the test data*):

1. **Unbalanced (The Baseline)**: Left the data as-is (9,362 graduates vs. 2,705 dropouts = 12,067 rows).
2. **Random UnderSampling**: Randomly removed graduating students until both groups were exactly 50/50 (**2,705 graduates vs. 2,705 dropouts = 5,410 rows**).
   * *Advantage*: Very fast to train; forces the model to give equal weight to dropouts.
3. **OverSampling (SMOTE)**: Created synthetic dropout profiles by finding existing dropouts and mathematically generating new "in-between" students until both groups reached 50/50 (**9,362 graduates vs. 9,362 dropouts = 18,724 rows**).
   * *Advantage*: Doesn't discard any graduating student data.
4. **SMOTEENN (SMOTE + Edited Nearest Neighbors)**:
   * First generated synthetic dropouts with SMOTE.
   * Then ran a "cleaning" pass using *Edited Nearest Neighbors (ENN)*: it looked at every point's 3 closest neighbors. If a synthetic student was surrounded by the opposite class (creating confusion at the boundary), it was pruned.
   * *Result*: **15,174 clean, clearly separated students** (6,888 graduates vs. 8,286 dropouts).

---

### Step 2: Selecting the Best Features

Why not just feed all 33 features into the models?
1. **Redundancy & Noise**: Minor categories (like having a rare marital status or foreign language) confuse the algorithms.
2. **Curse of Dimensionality**: Models with fewer, stronger features generalize better to future students.
3. **Explainability**: Teachers and counselors need a focused, clear set of signals to look at.

We compared **three distinct schools of feature selection**:

#### 1. Filter Method — ANOVA F-Test (`SelectKBest(k=15)`)
* **How it works**: Pure statistics. It measures the mathematical ratio of variance between the two classes. If graduates and dropouts have drastically different values for a feature, that feature gets a high $F$-score.
* **Result (Top 15 selected)**:
  1. `ira` (Academic Performance Index) — $F = 17,093$ (by far the #1 indicator)
  2. `reprovacoes` (Course failures) — $F = 3,570$
  3. `percentual_frequencia` (Attendance rate) — $F = 1,892$
  4. `anoingresso` (Admission year) — $F = 1,606$
  5. `modalidade` (Course modality) — $F = 526$
  6. `rendabruta` (Family gross income) — $F = 416$
  7. `pai_nivel_escolaridade` (Father's education) — $F = 383$
  8. `mae_nivel_escolaridade` (Mother's education) — $F = 372$
  9. `idade` (Student age) — $F = 310$
  10. `quantidade_notebooks` (Number of laptops) — $F = 224$
  11. `qtd_filhos` (Number of children) — $F = 174$
  12. `estado_civil_Solteiro(a)` (Single) — $F = 128$
  13. `genero_F` (Female) — $F = 125$
  14. `genero_M` (Male) — $F = 125$
  15. `tipo_area_residencial` (Urban/Rural area) — $F = 122$

#### 2. Wrapper Method — Backward Elimination
* **How it works**: It started with all 33 features, trained a Random Forest model, checked its cross-validated recall, and dropped the least useful feature. It repeated this elimination cycle one-by-one until half were left.
* **Result**: Selected **17 optimal features** (including gap years `ficou_tempo_sem_estudar` and specific socioeconomic flags).

#### 3. Embedded Method — Random Forest Feature Importance
* **How it works**: Trains a 100-tree Random Forest on the data and calculates the *Gini Impurity reduction* for every feature. We kept all features with $\ge 1\%$ importance.
* **Result**: Selected **15 features** (dominated by `ira` at 49.3% and `reprovacoes` at 11.1%).

---

### Step 3: Training the Models (The 48 Experiments)

For each combination of **Balancing (4)** and **Feature Selection (3)**, we trained **4 algorithms**:

1. **Random Forest (RF)**: A committee of multiple decision trees that vote on the final prediction (very strong, resilient against overfitting).
2. **Decision Tree (DT)**: A single tree of `if/else` questions (e.g. *"If attendance < 75% and failed courses > 2 → Dropout"*). Highly interpretable!
3. **Logistic Regression (LR)**: A classic statistical model that draws a linear boundary and outputs a probability score.
4. **Support Vector Machine (SVM)**: A geometric algorithm that tries to draw a wide separating hyperplane between graduates and dropouts.

#### How Each Experiment Was Run:
* **Hyperparameter Tuning (`GridSearchCV`)**: We didn't guess settings. We tested multiple combinations (tree depths: None, 10, 20; splitting criteria: Gini vs. Entropy; regularization: C = 0.1, 1.0, 10.0; kernels: RBF vs. Linear) using **5-fold cross-validation** to find the absolute best version of that model.
* **Evaluation on Unseen Test Data**: Once tuned, the model made predictions on the **3,017 test students** who were completely untouched during training and balancing.
* **10-Fold Cross-Validation**: We also tested the best model across 10 different folds of the training data to confirm its performance was stable and reproducible.

---

### Step 4: How We Ranked the Models (Why Recall is King)

How do you decide which model is the winner?

In an educational setting, **Recall is the #1 metric**:
$$\text{Recall} = \frac{\text{Dropouts Correctly Caught}}{\text{Total Actual Dropouts}}$$

* **If Recall is low (False Negative)**: A student who is about to drop out is labeled "Fine". The school does nothing, and the student permanently drops out of high school. **The cost is catastrophic.**
* **If Precision is slightly lower (False Positive)**: A student who was going to graduate anyway gets flagged as "At-Risk". A guidance counselor calls them in for an encouraging check-in. **The cost is harmless.**

Therefore, following the research paper, all 48 models were sorted by:
$$\mathbf{1^{\text{st}} \text{ Priority: Highest Recall}} \quad \longrightarrow \quad \mathbf{2^{\text{nd}} \text{ Priority: Highest Precision}} \quad \longrightarrow \quad \mathbf{3^{\text{rd}} \text{ Priority: Highest 10-Fold CV Recall}}$$

---

### Step 5: What Were the Results?

Here is how the top models performed on the 3,017 test students:

| Rank | Balancing | Feature Selection | Model | Recall | Precision | F1 | AUC | Accuracy |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **#1** | SMOTEENN | ANOVA | **SVM** | **0.914** | 0.231 | 0.369 | 0.591 | 30.1% |
| **#2** | UnderSampling | Backward | **SVM** | **0.910** | 0.231 | 0.369 | 0.759 | 30.3% |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
| **Best RF** | **UnderSampling** | **FeatureImportance** | **Random Forest** | **0.848** | **0.836** | **0.842** | **0.951** | **92.9%** |
| **Best DT** | **UnderSampling** | **ANOVA** | **Decision Tree** | **0.846** | **0.640** | **0.729** | **0.854** | **85.9%** |

#### Why SVM Didn't Actually Win:
SVM had the highest raw recall (0.914), but its precision was only **0.231** and accuracy was only **30%**. Why? SVM panicked and predicted that almost *every single student* was going to drop out! That is useless for an institution.

#### The Real Star: Random Forest (`UnderSampling + FeatureImportance`)
* **Recall: 0.848**: Out of 676 actual dropouts, it correctly caught **573 of them**!
* **Precision: 0.836**: When it flags a student, it is right 84% of the time.
* **Accuracy: 92.9%** with an outstanding **AUC of 0.951**!
* Out of 2,341 graduating students, it only had **112 false alarms**.

#### The Interpretable Champion: Decision Tree (`UnderSampling + ANOVA`)
* **Recall: 0.846**: Caught **572 out of 676 dropouts**!
* **Precision: 0.640**, **Accuracy: 85.9%**.
* Because it's a single decision tree, we can visualize the exact flowchart of rules for school administrators!

---

### Step 6: What Outputs Were Saved?

In the folder [`phase2_outputs/`](file:///c:/Users/tejas/Downloads/research%20student%20fairness%20evaluation/code/pbl-sem5-main/pbl-sem5-main/phase2_outputs):

1. **`experiment_results.csv`**: A spreadsheet with all 48 experiments, their hyperparameters, and all metrics.
2. **`phase2_models.pkl`**: The **Best Random Forest** and **Best Decision Tree** saved alongside the test data and feature names, completely ready for Phase 3.
3. **`all_trained_models.pkl`**: An archive of all 48 trained models.

---

### 🚀 What Happens Next? (Phase 3 & Phase 4)

* **Phase 3 (Explainable AI — XAI)**:
  We take the Best Random Forest and Best Decision Tree and apply **SHAP** and **LIME**. This will generate visual plots showing *exactly* why each student was flagged (e.g. *"Student #104 has an 82% dropout risk because their IRA is 3.8 and attendance is below 70%"*).
* **Phase 4 (Fairness & Governance Audit)**:
  We check whether the models treat male vs. female students or white vs. minority students fairly, audit Disparate Impact, and build a governance policy for ethical use in schools.
