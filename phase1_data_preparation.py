"""
Phase 1: Data Preparation and Target Construction
=====================================================
Replicates the base paper's methodology:
  Silva et al., "An Investigation Into Dropout Indicators in 
  Secondary Technical Education Using Explainable AI" (IEEE RITA, 2025)

Steps:
  1. Load & explore dataset
  2. Filter to secondary-level technical education (matching the paper's 15,084 students)
  3. Build binary target from 'situacao'
  4. Preprocessing: drop IDs, drop >20% missing cols, IQR outliers, encoding
  5. Stratified train/test split
"""

import sys
import io
import warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import pickle
import os

# ── Handle encoding for Windows console ──────────────────────────────
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
warnings.filterwarnings("ignore")

DATA_PATH = "dataset_evasao_MDE.xlsx"
OUTPUT_DIR = "phase1_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════
# STEP 1 — LOAD & EXPLORE
# ═══════════════════════════════════════════════════════════════════════
print("=" * 72)
print("STEP 1: LOADING AND EXPLORING THE DATASET")
print("=" * 72)

df_raw = pd.read_excel(DATA_PATH)
print(f"\nRaw dataset shape: {df_raw.shape[0]} rows × {df_raw.shape[1]} columns")

print("\n── 1a. Full list of columns and dtypes ──")
for col in df_raw.columns:
    print(f"  {col:<35s} {str(df_raw[col].dtype)}")

print("\n── 1b. 'situacao' — unique values and counts ──")
sit_counts = df_raw["situacao"].value_counts()
for val, cnt in sit_counts.items():
    print(f"  {val:<40s} {cnt:>6d}  ({cnt / len(df_raw) * 100:5.2f}%)")

print("\n── 1c. Missing-value percentage per column ──")
missing_pct = (df_raw.isnull().sum() / len(df_raw) * 100).round(2)
for col, pct in missing_pct.items():
    flag = "  *** DROP (>20%)" if pct > 20 else ""
    print(f"  {col:<35s} {pct:6.2f}%{flag}")

print("\n── 1d. Summary statistics (numeric columns) ──")
print(df_raw.describe().T.to_string())

# ═══════════════════════════════════════════════════════════════════════
# STEP 2 — FILTER TO SECONDARY TECHNICAL EDUCATION & BUILD BINARY TARGET
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("STEP 2: FILTER TO SECONDARY TECHNICAL & BUILD BINARY TARGET")
print("=" * 72)

# 2a. The paper studies "secondary-level technical courses".
#     In Brazil, these are: Integrado, Concomitante, Subsequente, Integrado EJA.
#     Licenciatura, Bacharelado, Tecnologia, Engenharia are higher-education.
secondary_modalities = ["Integrado", "Concomitante", "Subsequente", "Integrado EJA"]
df = df_raw[df_raw["modalidade"].isin(secondary_modalities)].copy()
print(f"\nAfter filtering to secondary technical modalities:")
print(f"  Kept modalities: {secondary_modalities}")
print(f"  Rows remaining: {len(df)} (was {len(df_raw)})")

print("\n  'situacao' distribution in filtered data:")
for val, cnt in df["situacao"].value_counts().items():
    print(f"    {val:<40s} {cnt:>6d}")

# 2b. Build binary target following the paper (Section IV-A, page 108):
#     Class 0 ("Completed"): 'Concluído'
#     Class 1 ("Dropped Out"): 'Evasão', 'Cancelado', 'Cancelamento Compulsório',
#                               'Jubilado', 'Transferido Externo'
#     Everything else (Matriculado, Trancado, Formado, etc.) is EXCLUDED
#     because those students haven't reached a terminal status.

completed_vals  = ["Concluído"]
dropout_vals    = ["Evasão", "Cancelado", "Cancelamento Compulsório",
                   "Jubilado", "Transferido Externo"]

# Map and filter
def map_target(s):
    if s in completed_vals:
        return 0
    elif s in dropout_vals:
        return 1
    else:
        return np.nan  # exclude non-terminal statuses

df["target"] = df["situacao"].apply(map_target)
n_excluded = df["target"].isna().sum()
df = df.dropna(subset=["target"])
df["target"] = df["target"].astype(int)

print(f"\n  Excluded {n_excluded} rows with non-terminal status")
print(f"  (e.g., Matriculado, Trancado, Formado, Aguardando, etc.)")
print(f"\n  Final dataset for modeling: {len(df)} students")

# 2c. Show class distribution and compare with paper
class_dist = df["target"].value_counts().sort_index()
total = len(df)
c0, c1 = class_dist[0], class_dist[1]
pct0, pct1 = c0 / total * 100, c1 / total * 100

print(f"\n── TARGET CLASS DISTRIBUTION ──")
print(f"  Class 0 (Completed):   {c0:>6d}  ({pct0:.1f}%)")
print(f"  Class 1 (Dropped Out): {c1:>6d}  ({pct1:.1f}%)")
print(f"  Total:                 {total:>6d}")

# Paper expects: 11,703 (78%) / 3,381 (22%)
paper_total = 11703 + 3381
paper_pct0 = 11703 / paper_total * 100
paper_pct1 = 3381 / paper_total * 100

print(f"\n  Paper reference:   {11703} ({paper_pct0:.1f}%) / {3381} ({paper_pct1:.1f}%) = {paper_total} total")

if abs(pct0 - paper_pct0) > 3:
    print(f"\n  ⚠️  WARNING: Class distribution deviates from paper by"
          f" {abs(pct0 - paper_pct0):.1f}pp — investigate!")
else:
    print(f"\n  ✅ Class distribution matches the paper (within 3pp tolerance)")

if abs(total - paper_total) > 100:
    print(f"  ⚠️  NOTE: Total count ({total}) differs from paper ({paper_total}) by {abs(total - paper_total)}")
    print(f"        This may be due to dataset version differences or filtering criteria.")

# ═══════════════════════════════════════════════════════════════════════
# STEP 3 — PREPROCESSING
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("STEP 3: PREPROCESSING")
print("=" * 72)

# 3a. Drop the original target column and student ID / identifier columns
drop_id_cols = ["alunoid", "situacao"]
# Also drop 'curso' and 'campus' — they are identifiers/high-cardinality strings
# The paper mentions removing "student identification attributes"
# 'dataconclusao' will be caught by the >20% missing rule anyway
additional_drop = ["curso", "campus"]
cols_to_drop_ids = [c for c in drop_id_cols + additional_drop if c in df.columns]
print(f"\n── 3a. Dropping identifier columns ──")
print(f"  Dropped: {cols_to_drop_ids}")
df = df.drop(columns=cols_to_drop_ids)

# 3b. Drop columns with >20% missing values
print(f"\n── 3b. Dropping columns with >20% missing ──")
missing_pct_now = (df.isnull().sum() / len(df) * 100).round(2)
high_missing = missing_pct_now[missing_pct_now > 20]
print(f"  Columns exceeding 20% missing:")
for col, pct in high_missing.items():
    print(f"    {col:<35s} {pct:6.2f}%")
df = df.drop(columns=high_missing.index.tolist())
print(f"  Remaining columns: {df.shape[1]} (including target)")

# Show current missing values for remaining columns
print(f"\n  Remaining missing values:")
remaining_missing = (df.isnull().sum() / len(df) * 100).round(2)
remaining_missing = remaining_missing[remaining_missing > 0]
if len(remaining_missing) > 0:
    for col, pct in remaining_missing.items():
        print(f"    {col:<35s} {pct:6.2f}%")
    # Fill remaining numeric NaN with median (matching common practice)
    num_cols_with_na = [c for c in remaining_missing.index if df[c].dtype in ['float64', 'int64']]
    for col in num_cols_with_na:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        print(f"    → Filled '{col}' NaN with median ({median_val})")
else:
    print(f"    None — all clean!")

# 3c. Normalize race values (fix case inconsistencies)
print(f"\n── 3c. Normalizing categorical values ──")
race_map = {
    "Parda": "Parda", "PARDA": "Parda",
    "Branca": "Branca", "BRANCA": "Branca",
    "Preta": "Preta", "PRETA": "Preta",
    "Amarela": "Amarela", "AMARELA": "Amarela",
    "Indígena": "Indígena", "INDIGENA": "Indígena",
    "NAO INFORMADO": "Não declarado", "Não declarado": "Não declarado",
}
if "raca" in df.columns:
    df["raca"] = df["raca"].map(race_map).fillna(df["raca"])
    print(f"  Normalized 'raca' — merged case variants:")
    print(f"    {df['raca'].value_counts().to_dict()}")

# 3d. IQR Outlier Treatment (Winsorize / Cap-Clip)
print(f"\n── 3d. IQR Outlier Treatment (Winsorize) ──")

# ── Columns to apply IQR to (user-specified) ──
iqr_target_cols = ["idade", "rendabruta", "quantidade_computadores",
                   "quantidade_notebooks", "qtd_filhos"]

# ── Columns explicitly EXCLUDED from IQR ──
excluded_causal = ["reprovacoes", "ira", "percentual_frequencia"]
excluded_enrollment = ["anoingresso", "periodoingresso"]

print(f"  IQR applied to: {iqr_target_cols}")
print(f"  EXCLUDED (causally linked to target): {excluded_causal}")
print(f"     → These are legitimate at-risk signals, not noise.")
print(f"  EXCLUDED (enrollment-year fields):    {excluded_enrollment}")
print(f"     → Categorical/temporal, not continuous outlier-prone variables.")

# ── Winsorize each target column ──
print(f"\n  Strategy: CAP/CLIP (winsorize) at IQR bounds — NO rows removed.")
print(f"  {'Column':<30s} {'Method':<12s} {'Lower':>10s} {'Upper':>10s} {'Clipped':>8s}")
print(f"  {'-'*30} {'-'*12} {'-'*10} {'-'*10} {'-'*8}")

total_clipped = 0
for col in iqr_target_cols:
    if col not in df.columns:
        print(f"  {col:<30s} {'SKIPPED':<12s} (not in dataframe)")
        continue

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR_val = Q3 - Q1

    if IQR_val > 0:
        # Standard 1.5×IQR winsorization
        lower = Q1 - 1.5 * IQR_val
        upper = Q3 + 1.5 * IQR_val
        method = "1.5×IQR"
    else:
        # IQR=0 (e.g., mostly-zero columns). Use 1st/99th percentile capping.
        lower = df[col].quantile(0.01)
        upper = df[col].quantile(0.99)
        method = "P1/P99"

    # Count values that will be clipped
    n_below = (df[col] < lower).sum()
    n_above = (df[col] > upper).sum()
    n_clipped = n_below + n_above
    total_clipped += n_clipped

    # Clip in place
    df[col] = df[col].clip(lower=lower, upper=upper)

    print(f"  {col:<30s} {method:<12s} {lower:>10.2f} {upper:>10.2f} {n_clipped:>8d}")

print(f"\n  Total values clipped: {total_clipped}")
print(f"  Rows removed: 0 (all rows preserved via winsorization)")
print(f"  Dataset size after IQR: {len(df)} rows (unchanged)")


# 3e. Encode categorical variables
print(f"\n── 3e. Encoding Categorical Variables ──")

# Separate target before encoding
y = df["target"].values
df = df.drop(columns=["target"])

# ── OneHotEncoder for genero, raca, estado_civil ──
ohe_cols = [c for c in ["genero", "raca", "estado_civil"] if c in df.columns]
print(f"\n  OneHotEncoder for: {ohe_cols}")

ohe = OneHotEncoder(sparse_output=False, drop=None, handle_unknown="error")
ohe_data = ohe.fit_transform(df[ohe_cols])
ohe_feature_names = ohe.get_feature_names_out(ohe_cols)
print(f"  Generated {len(ohe_feature_names)} one-hot features:")
for fn in ohe_feature_names:
    print(f"    • {fn}")

ohe_df = pd.DataFrame(ohe_data, columns=ohe_feature_names, index=df.index)
df = df.drop(columns=ohe_cols)
df = pd.concat([df, ohe_df], axis=1)

# ── Ordinal/Label encoding for education level fields ──
edu_cols = [c for c in ["mae_nivel_escolaridade", "pai_nivel_escolaridade"] if c in df.columns]
print(f"\n  Ordinal encoding for: {edu_cols}")

# Define meaningful ordinal ordering (lowest → highest education)
edu_order = [
    "Não Estudou",
    "Não conhece",
    "Não sei informar",
    "Alfabetizado",
    "Ensino fundamental incompleto",
    "Ensino fundamental completo",
    "Ensino médio incompleto",
    "Ensino médio completo",
    "Ensino superior incompleto",
    "Ensino superior completo",
    "Pós-graduação incompleta",
    "Pós-graduação completa",
]

edu_mapping = {level: idx for idx, level in enumerate(edu_order)}
print(f"  Ordinal mapping:")
for level, idx in edu_mapping.items():
    print(f"    {idx:>2d} → {level}")

for col in edu_cols:
    # Map known values; any unmapped go to -1
    df[col] = df[col].map(edu_mapping)
    unmapped = df[col].isna().sum()
    if unmapped > 0:
        print(f"  ⚠️  {col}: {unmapped} unmapped values (set to median)")
        df[col] = df[col].fillna(df[col].median())
    df[col] = df[col].astype(int)
    print(f"  {col}: encoded to ordinal [0..{len(edu_order)-1}]")

# ── LabelEncoder for remaining categorical columns ──
remaining_cat = df.select_dtypes(include=["object", "bool", "str"]).columns.tolist()
if remaining_cat:
    print(f"\n  LabelEncoder for remaining categoricals: {remaining_cat}")
    label_encoders = {}
    for col in remaining_cat:
        le = LabelEncoder()
        df[col] = df[col].astype(str)  # handle booleans
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
        print(f"    {col}: {len(le.classes_)} classes → {list(le.classes_)}")

# 3f. Confirm no normalization (matching paper)
print(f"\n── 3f. Normalization ──")
print(f"  ✅ Numeric variables NOT normalized (matching base paper)")

# ═══════════════════════════════════════════════════════════════════════
# STEP 4 — TRAIN / TEST SPLIT (STRATIFIED)
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("STEP 4: STRATIFIED TRAIN/TEST SPLIT")
print("=" * 72)

X = df.values
feature_names = df.columns.tolist()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print(f"\n  Features: {X.shape[1]}")
print(f"  Total samples: {X.shape[0]}")
print(f"\n  Train set: {X_train.shape[0]} samples")
print(f"    Class 0: {(y_train == 0).sum()} ({(y_train == 0).mean()*100:.1f}%)")
print(f"    Class 1: {(y_train == 1).sum()} ({(y_train == 1).mean()*100:.1f}%)")
print(f"\n  Test set:  {X_test.shape[0]} samples")
print(f"    Class 0: {(y_test == 0).sum()} ({(y_test == 0).mean()*100:.1f}%)")
print(f"    Class 1: {(y_test == 1).sum()} ({(y_test == 1).mean()*100:.1f}%)")

# ═══════════════════════════════════════════════════════════════════════
# SAVE OUTPUTS
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("SAVING PHASE 1 OUTPUTS")
print("=" * 72)

output = {
    "X_train": X_train,
    "X_test": X_test,
    "y_train": y_train,
    "y_test": y_test,
    "feature_names": feature_names,
}
output_path = os.path.join(OUTPUT_DIR, "phase1_data.pkl")
with open(output_path, "wb") as f:
    pickle.dump(output, f)
print(f"  Saved: {output_path}")

# Also save the feature names list for reference
fn_path = os.path.join(OUTPUT_DIR, "feature_names.txt")
with open(fn_path, "w", encoding="utf-8") as f:
    for fn in feature_names:
        f.write(fn + "\n")
print(f"  Saved: {fn_path}")

print(f"\n  Final feature list ({len(feature_names)} features):")
for i, fn in enumerate(feature_names):
    print(f"    [{i:>2d}] {fn}")

print("\n" + "=" * 72)
print("✅ PHASE 1 COMPLETE — Ready for sanity check before Phase 2")
print("=" * 72)
