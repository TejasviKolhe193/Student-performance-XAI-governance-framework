"""
Phase 1: Replicating Silva et al. (IEEE RITA 2025) Data Preparation Pipeline
- Filters dataset to 15,084 secondary technical education students with terminal status.
- Binary target: 0 = Concluído, 1 = Dropped Out / Cancelled / Transferred.
- Drops student ID (alunoid) and columns with >20% missing values.
- Explicitly drops GPA (ira) to eliminate target leakage and early-warning claims.
- Normalizes race categories.
- Stratified 70/30 train/test split (random_state=42).
- IQR clipping on training set only (no test leakage).
- OneHotEncoder on gender, race, marital status; LabelEncoder on other categoricals.
"""

import os
import sys
import io
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace", line_buffering=True)

DATA_PATH = "dataset_evasao_MDE.xlsx"
OUTPUT_DIR = "phase1_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 75)
print("PHASE 1: DATA PREPARATION & BASELINE REPLICATION")
print("=" * 75)

# 1. Load dataset
print("Loading raw dataset...")
df_raw = pd.read_excel(DATA_PATH)
print(f"Raw shape: {df_raw.shape[0]} rows × {df_raw.shape[1]} columns")

# 2. Filter secondary technical education modalities
secondary_modalities = ["Integrado", "Concomitante", "Subsequente", "Integrado EJA"]
df = df_raw[df_raw["modalidade"].isin(secondary_modalities)].copy()
print(f"Filtered by secondary modalities: {len(df)} rows")

# 3. Filter terminal statuses and construct binary target
completed_vals = ["Concluído"]
dropout_vals = ["Evasão", "Cancelado", "Cancelamento Compulsório", "Jubilado", "Transferido Externo"]

def map_target(val):
    if val in completed_vals:
        return 0
    elif val in dropout_vals:
        return 1
    return np.nan

df["target"] = df["situacao"].apply(map_target)
df = df.dropna(subset=["target"]).copy()
df["target"] = df["target"].astype(int)

total_students = len(df)
c0 = (df["target"] == 0).sum()
c1 = (df["target"] == 1).sum()
print(f"\nCohort Size: {total_students} students (Paper expects 15,084)")
print(f"  Class 0 (Completed):   {c0:>6d} ({c0/total_students*100:.2f}%) [Paper: 11,703 (77.6%)]")
print(f"  Class 1 (Dropped Out): {c1:>6d} ({c1/total_students*100:.2f}%) [Paper:  3,381 (22.4%)]")
assert total_students == 15084, f"Expected 15084 students, got {total_students}"
assert c0 == 11703, f"Expected 11703 Class 0, got {c0}"
assert c1 == 3381, f"Expected 3381 Class 1, got {c1}"
print(">> Exact cohort count and class distribution match Silva et al. 100%!")

# Save cached filtered dataset for fast reloading
df.to_pickle("filtered_secondary_students.pkl")
print("Saved cached filtered dataset to filtered_secondary_students.pkl")

# 4. Drop ID and >20% missing columns, and drop GPA (ira)
missing_pct = df.isnull().mean() * 100
high_missing_cols = missing_pct[missing_pct > 20].index.tolist()
print(f"\nColumns with >20% missing values dropped: {high_missing_cols}")

cols_to_drop = ["alunoid", "situacao"] + high_missing_cols

if "ira" in df.columns:
    cols_to_drop.append("ira")
    print(">> EXCLUDED 'ira' (GPA) - reverting Gap 1 extension to eliminate leakage.")

df_clean = df.drop(columns=[c for c in cols_to_drop if c in df.columns]).copy()
print(f"Remaining attributes: {df_clean.shape[1] - 1} predictive + 1 target")

# 5. Normalize race/ethnicity casing
race_map = {
    "Parda": "Parda", "PARDA": "Parda",
    "Branca": "Branca", "BRANCA": "Branca",
    "Preta": "Preta", "PRETA": "Preta",
    "Amarela": "Amarela", "AMARELA": "Amarela",
    "Indígena": "Indígena", "INDIGENA": "Indígena",
    "NAO INFORMADO": "Não declarado", "Não declarado": "Não declarado",
}
df_clean["raca"] = df_clean["raca"].map(race_map).fillna(df_clean["raca"])

# 6. Fill minor missing values in computers/laptops with median
for col in ["quantidade_computadores", "quantidade_notebooks"]:
    if col in df_clean.columns and df_clean[col].isnull().sum() > 0:
        med = df_clean[col].median()
        df_clean[col] = df_clean[col].fillna(med)

# 7. Stratified 70/30 Train/Test Split (Matching Silva et al. Table III)
train_df, test_df = train_test_split(
    df_clean, test_size=0.30, random_state=42, stratify=df_clean["target"]
)
print(f"\nStratified 70/30 Split:")
print(f"  Training set: {len(train_df)} students (Class 0: {(train_df['target']==0).sum()}, Class 1: {(train_df['target']==1).sum()})")
print(f"  Test set:     {len(test_df)} students (Class 0: {(test_df['target']==0).sum()}, Class 1: {(test_df['target']==1).sum()})")

# 8. Outlier IQR clipping on numerical continuous features - FIT ON TRAINING SET ONLY
iqr_cols = ["idade", "rendabruta", "quantidade_computadores", "quantidade_notebooks", "qtd_filhos"]
print(f"\nIQR 1.5× Outlier clipping fit on training set only: {iqr_cols}")
print("  Excluded from IQR clipping: reprovacoes (discrete count 0-5), percentual_frequencia (0-100%).")

train_df_clipped = train_df.copy()
test_df_clipped = test_df.copy()

iqr_bounds = {}
for col in iqr_cols:
    if col in train_df.columns:
        q1 = train_df[col].quantile(0.25)
        q3 = train_df[col].quantile(0.75)
        iqr = q3 - q1
        if iqr > 0:
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
        else:
            lower = train_df[col].quantile(0.01)
            upper = train_df[col].quantile(0.99)
        iqr_bounds[col] = (lower, upper)
        train_df_clipped[col] = train_df_clipped[col].clip(lower=lower, upper=upper)
        test_df_clipped[col] = test_df_clipped[col].clip(lower=lower, upper=upper)

# 9. Categorical Encoding:
# OneHotEncoder for genero, raca, estado_civil
# LabelEncoder for remaining categoricals
ohe_cols = ["genero", "raca", "estado_civil"]
ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
ohe.fit(train_df_clipped[ohe_cols])

ohe_feature_names = ohe.get_feature_names_out(ohe_cols)
train_ohe = pd.DataFrame(ohe.transform(train_df_clipped[ohe_cols]), columns=ohe_feature_names, index=train_df.index)
test_ohe = pd.DataFrame(ohe.transform(test_df_clipped[ohe_cols]), columns=ohe_feature_names, index=test_df.index)

# Remaining categoricals:
cat_cols = train_df_clipped.select_dtypes(include=["object", "string", "category"]).columns.tolist()
cat_cols = [c for c in cat_cols if c not in ohe_cols and c != "target"]

train_encoded = train_df_clipped.drop(columns=ohe_cols).copy()
test_encoded = test_df_clipped.drop(columns=ohe_cols).copy()

label_encoders = {}
for col in cat_cols:
    le = LabelEncoder()
    train_encoded[col] = le.fit_transform(train_encoded[col].astype(str))
    # Transform test with handling unseen classes
    test_vals = test_encoded[col].astype(str)
    mapping = {c: i for i, c in enumerate(le.classes_)}
    test_encoded[col] = test_vals.map(mapping).fillna(-1).astype(int)
    label_encoders[col] = le

# Combine with OHE
y_train = train_encoded.pop("target").values
y_test = test_encoded.pop("target").values

X_train_df = pd.concat([train_encoded, train_ohe], axis=1)
X_test_df = pd.concat([test_encoded, test_ohe], axis=1)

feature_names = X_train_df.columns.tolist()
X_train = X_train_df.values
X_test = X_test_df.values

print(f"\nFinal Preprocessed Feature Space: {X_train.shape[1]} features")
print(f"  X_train shape: {X_train.shape}")
print(f"  X_test shape:  {X_test.shape}")

# Save Phase 1 bundle and CSVs
phase1_bundle = {
    "X_train": X_train,
    "X_test": X_test,
    "y_train": y_train,
    "y_test": y_test,
    "feature_names": feature_names,
    "train_df_raw": train_df,
    "test_df_raw": test_df,
    "iqr_bounds": iqr_bounds,
}
with open(os.path.join(OUTPUT_DIR, "phase1_data.pkl"), "wb") as f:
    pickle.dump(phase1_bundle, f)

# Save Phase 1 Summary CSV
summary_rows = [
    {"Metric": "Total Students Filtered", "Value": total_students, "Silva_et_al_Value": 15084, "Match": "Exact"},
    {"Metric": "Class 0 (Completed)", "Value": c0, "Silva_et_al_Value": 11703, "Match": "Exact"},
    {"Metric": "Class 1 (Dropout/Terminal)", "Value": c1, "Silva_et_al_Value": 3381, "Match": "Exact"},
    {"Metric": "Class 0 Percentage", "Value": f"{c0/total_students*100:.2f}%", "Silva_et_al_Value": "77.6%", "Match": "Exact"},
    {"Metric": "Class 1 Percentage", "Value": f"{c1/total_students*100:.2f}%", "Silva_et_al_Value": "22.4%", "Match": "Exact"},
    {"Metric": "Train Set Instances (70%)", "Value": len(train_df), "Silva_et_al_Value": 10558, "Match": "Exact"},
    {"Metric": "Test Set Instances (30%)", "Value": len(test_df), "Silva_et_al_Value": 4526, "Match": "Exact"},
    {"Metric": "Train Class 0 Count", "Value": int((y_train==0).sum()), "Silva_et_al_Value": 8150, "Match": "Near (8192 vs 8150)"},
    {"Metric": "Train Class 1 Count", "Value": int((y_train==1).sum()), "Silva_et_al_Value": 2408, "Match": "Near (2366 vs 2408)"},
    {"Metric": "Test Class 0 Count", "Value": int((y_test==0).sum()), "Silva_et_al_Value": 3553, "Match": "Near (3511 vs 3553)"},
    {"Metric": "Test Class 1 Count", "Value": int((y_test==1).sum()), "Silva_et_al_Value": 973, "Match": "Near (1015 vs 973)"},
    {"Metric": "Total Engineered Features", "Value": len(feature_names), "Silva_et_al_Value": 30, "Match": "Consistent (~30)"},
    {"Metric": "GPA (ira) Included?", "Value": "NO (Excluded)", "Silva_et_al_Value": "NO", "Match": "Exact"},
]
summary_df = pd.DataFrame(summary_rows)
summary_df.to_csv(os.path.join(OUTPUT_DIR, "phase1_summary.csv"), index=False)
print("Saved phase1_outputs/phase1_summary.csv")
print("PHASE 1 COMPLETE!")

