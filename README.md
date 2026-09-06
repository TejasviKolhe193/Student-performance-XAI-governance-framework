. Architecture Overview
Flowchart diagram covering the multi-phase pipeline from raw data to Phase 4 governance.
2. Phase 1: Data Preparation & Preprocessing
Cohort Filtering: Filtering secondary technical modalities (Integrado, Concomitante, Subsequente, Integrado EJA) and excluding higher education.
Target Construction: Mapping terminal non-completion statuses (Evasão, Cancelado, Jubilado, etc.) to Class 1, and Concluído to Class 0 while omitting non-terminal statuses.
Missingness & Outliers: 20% column missingness threshold; IQR Winsorization clipping continuous variables while retaining 100% of rows.
Encoding & Scale Integrity: One-Hot Encoding for demographics, 12-level hierarchical ordinal encoding for parental education, and preserving unnormalized scales.
Stratified Partitioning: 80/20 train/test split ($N_{\text{train}} = 12,067$, $N_{\text{test}} = 3,017$).
3. Phase 2: Balancing, Feature Selection, Model Training & Benchmarking (In-Depth)
Experimental Matrix: Formal definition of the $4 \times 3 \times 4 = 48$ combinatorial experiments.
Step 1: Class Balancing: Detailed mechanics of Unbalanced, RandomUnderSampler, SMOTE, and SMOTEENN (with sample counts, class ratios, and ENN boundary cleaning).
Step 2: Feature Selection:
Filter: ANOVA F-test with all 15 selected features and their exact $F$-scores (e.g., ira $F = 17,093.60$, reprovacoes $F = 3,570.63$).
Wrapper: Backward Elimination via Random Forest with all 17 selected features.
Embedded: Random Forest Feature Importance with all 15 features scoring $\ge 0.01$ importance.
Step 3: Estimators & Hyperparameters: Tuned grids for RandomForestClassifier, DecisionTreeClassifier, LogisticRegression, and SVC(max_iter=2000).
Step 4: Hierarchical Ranking: The paper's 3-tier cascade ($1^{\text{st}} \text{ Recall} \rightarrow 2^{\text{nd}} \text{ Precision} \rightarrow 3^{\text{rd}} \text{ 10-Fold CV}$) and the pedagogical rationale behind prioritizing Recall.
Step 5: Benchmark Results: Full top-10 table and analysis of why tree ensembles outclassed SVM's degenerate solution.
Step 6: Selected Models for Phase 3 (XAI):
Best Random Forest (UnderSampling + FeatureImportance + RF): Recall 0.848, Precision 0.836, F1 0.842, AUC 0.951, Accuracy 92.9%, with confusion matrix and classification report.
Best Decision Tree (UnderSampling + ANOVA + DT): Recall 0.846, Precision 0.640, F1 0.729, AUC 0.854, Accuracy 85.9%, with confusion matrix and classification report.
Computational Engineering Notes: Detailed explanation of SVM scale disparity, Platt scaling overhead, iteration bounds, and streaming I/O.
Artifacts Schema: Description and schema for experiment_results.csv, phase2_models.pkl, and all_trained_models.pkl.
4. Reproducibility & Phase 3/4 Roadmap
Step-by-step terminal commands to reproduce Phase 1 and Phase 2.
Detailed blueprint for Global & Local XAI (SHAP & LIME) and Fairness Auditing across sensitive demographic groups.
