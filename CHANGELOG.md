# Changelog

## Phase 1: Data Preparation & Translation (Completed)
- **Data Loading & Filtering**: Extracted subset matching secondary technical education (15,084 students).
- **Target Construction**: Created binary target variable corresponding to Completed (Class 0: 77.6%) vs. Dropped Out (Class 1: 22.4%), matching base paper exactly.
- **Missing Value Handling**: Dropped columns with >20% missing values (`dataconclusao`, `forma_acesso_seletivo`, `razao_ausencia_educacional`, `pontuacao_seletivo`). Filled minor missing values in `quantidade_computadores` and `quantidade_notebooks` with median.
- **Categorical Normalization**: Normalized case variants in `raca`.
- **IQR Outlier Winsorization**: Applied 1.5×IQR winsorization (cap/clip) specifically to `idade`, `rendabruta`, `quantidade_computadores`, `quantidade_notebooks`, and `qtd_filhos` to handle extreme values without dropping rows (preserving 15,084 records and the 78/22 class balance). Explicitly excluded causal variables like `reprovacoes`, `ira`, `percentual_frequencia`.
- **Encoding**: 
  - One-hot encoded `genero`, `raca`, `estado_civil`.
  - Ordinal encoded `mae_nivel_escolaridade`, `pai_nivel_escolaridade`.
  - Label encoded remaining categoricals.
- **Train/Test Split**: Stratified 80/20 split based on the target class.
- **Data Translation**: Created a complete Portuguese-to-English translation layer (column names and categorical values) and generated English-translated datasets, saving mapping artifacts for downstream XAI labels. Addressed typo in dataset for 'Pós-gradução completa'.

## Phase 2: Model Training & Evaluation (In Progress)
- **Status**: Actively running 48-experiment grid search (4 balancing strategies × 3 feature selection methods × 4 ML models).
- **Setup**: Configured GridSearchCV for RF, DT, LR, and SVM models using metrics prioritized by Recall, Precision, and 10-fold cross-validation.
