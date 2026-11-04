import os
import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

print("=== STEP 1: VERIFY DATA AND FEATURES ===")

DATA_PATH = "dataset_evasao_MDE.xlsx"
df_raw = pd.read_excel(DATA_PATH)
print(f"Raw shape: {df_raw.shape[0]} rows × {df_raw.shape[1]} columns")

# Check raw columns
raw_cols = df_raw.columns.tolist()
print("\nRaw Columns in dataset_evasao_MDE.xlsx:")
for i, col in enumerate(raw_cols):
    print(f"  {i+1}. {col}")

# Check secondary modalities filter
secondary_modalities = ["Integrado", "Concomitante", "Subsequente", "Integrado EJA"]
df_mod = df_raw[df_raw["modalidade"].isin(secondary_modalities)].copy()
print(f"\nStudents in secondary technical modalities: {len(df_mod)}")

# Target definition
completed_vals = ["Concluído"]
dropout_vals = ["Evasão", "Cancelado", "Cancelamento Compulsório", "Jubilado", "Transferido Externo"]

print("\nSituacao counts in secondary technical modalities:")
print(df_mod["situacao"].value_counts(dropna=False))

def map_target(val):
    if val in completed_vals:
        return 0
    elif val in dropout_vals:
        return 1
    return np.nan

df_mod["target"] = df_mod["situacao"].apply(map_target)
df_clean = df_mod.dropna(subset=["target"]).copy()
df_clean["target"] = df_clean["target"].astype(int)

total_students = len(df_clean)
c0 = (df_clean["target"] == 0).sum()
c1 = (df_clean["target"] == 1).sum()

print(f"\nFiltered Cohort Size: {total_students} (Expected: 15,084)")
print(f"  Class 0 (Completed):   {c0:>6d} ({c0/total_students*100:.2f}%) [Silva et al.: 11,703 (77.6%)]")
print(f"  Class 1 (Dropped Out): {c1:>6d} ({c1/total_students*100:.2f}%) [Silva et al.:  3,381 (22.4%)]")

# Breakdown of Class 1:
print("\nClass 1 Breakdown by situacao:")
for val in dropout_vals:
    cnt = (df_clean["situacao"] == val).sum()
    print(f"  - {val}: {cnt:>5d} ({cnt/total_students*100:.2f}%)")

# Check missing values in the 15,084 cohort
print("\nMissing values in the 15,084 cohort:")
missing_series = df_clean.isnull().sum()
missing_pct = df_clean.isnull().mean() * 100
for col in df_clean.columns:
    if missing_series[col] > 0:
        print(f"  {col}: {missing_series[col]} missing ({missing_pct[col]:.2f}%)")

# Columns with > 20% missing values
high_missing = missing_pct[missing_pct > 20].index.tolist()
print(f"\nColumns with >20% missing values (dropped as in Silva et al.): {high_missing}")

# Check the 19 features list (excluding alunoid, situacao, target, ira, and high missing)
cols_to_drop = ["alunoid", "situacao", "target", "ira"] + high_missing
feature_cols = [c for c in df_clean.columns if c not in cols_to_drop]
print(f"\nFinal feature count before one-hot encoding: {len(feature_cols)} features (Expected: 19)")
for i, col in enumerate(feature_cols):
    print(f"  {i+1}. {col} (dtype: {df_clean[col].dtype})")

# Check timing of percentual_frequencia and reprovacoes
print("\n--- TIMING & GRANULARITY ANALYSIS ---")
print("1. Rows per student: Check alunoid uniqueness")
num_unique_students = df_clean["alunoid"].nunique()
print(f"   Total rows: {len(df_clean)}, Unique alunoid: {num_unique_students}")
if num_unique_students == len(df_clean):
    print("   -> EXACTLY ONE ROW PER STUDENT. The dataset is cross-sectional, not longitudinal.")

print("\n2. Date range of enrollment (anoingresso):")
print(f"   Min anoingresso: {df_clean['anoingresso'].min()}, Max anoingresso: {df_clean['anoingresso'].max()}")
print("   anoingresso distribution:")
print(df_clean["anoingresso"].value_counts().sort_index())

print("\n3. dataconclusao (exit date):")
print(f"   Missing dataconclusao in cohort: {df_clean['dataconclusao'].isnull().sum()} / {len(df_clean)}")
print(f"   For Completed: {df_clean[df_clean['target']==0]['dataconclusao'].notnull().sum()} present, {df_clean[df_clean['target']==0]['dataconclusao'].isnull().sum()} missing")
print(f"   For Dropout:   {df_clean[df_clean['target']==1]['dataconclusao'].notnull().sum()} present, {df_clean[df_clean['target']==1]['dataconclusao'].isnull().sum()} missing")

print("\n4. Distribution of reprovacoes:")
print("   Class 0 (Completed):", df_clean[df_clean["target"]==0]["reprovacoes"].describe().to_dict())
print("   Class 1 (Dropout):  ", df_clean[df_clean["target"]==1]["reprovacoes"].describe().to_dict())
print("   reprovacoes > 3 count in Dropout:", (df_clean[df_clean["target"]==1]["reprovacoes"] > 3).sum(), f"out of {c1} ({(df_clean[df_clean['target']==1]['reprovacoes'] > 3).mean()*100:.1f}%)")
print("   reprovacoes > 10 count in Dropout:", (df_clean[df_clean["target"]==1]["reprovacoes"] > 10).sum(), f"out of {c1} ({(df_clean[df_clean['target']==1]['reprovacoes'] > 10).mean()*100:.1f}%)")
print("   Max reprovacoes in Dropout:", df_clean[df_clean["target"]==1]["reprovacoes"].max())

print("\n5. Distribution of percentual_frequencia:")
print("   Class 0 (Completed):", df_clean[df_clean["target"]==0]["percentual_frequencia"].describe().to_dict())
print("   Class 1 (Dropout):  ", df_clean[df_clean["target"]==1]["percentual_frequencia"].describe().to_dict())

