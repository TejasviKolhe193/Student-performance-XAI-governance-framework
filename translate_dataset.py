"""
English Translation Layer for the Brazilian Education Dataset
==============================================================
Creates a fully translated (columns + categorical values) English copy
of the dataset alongside the original Portuguese version.

Both versions are saved and a mapping module is produced for reuse
in SHAP/LIME labels, plots, and report generation.
"""

import sys
import io
import warnings
import pandas as pd
import os
import pickle

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
warnings.filterwarnings("ignore")

DATA_PATH = "dataset_evasao_MDE.xlsx"
OUTPUT_DIR = "phase1_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════
# 1. COLUMN NAME MAPPING (Portuguese → English)
# ═══════════════════════════════════════════════════════════════════════

COLUMN_MAP = {
    "alunoid":                      "student_id",
    "campus":                       "campus",
    "curso":                        "course",
    "anoingresso":                  "enrollment_year",
    "periodoingresso":             "enrollment_period",
    "dataconclusao":               "completion_date",
    "forma_acesso_seletivo":       "admission_type",
    "rendabruta":                  "gross_income",
    "ira":                         "gpa",
    "modalidade":                  "course_modality",
    "genero":                      "gender",
    "raca":                        "race",
    "idade":                       "age",
    "ficou_tempo_sem_estudar":     "had_study_gap",
    "razao_ausencia_educacional":  "reason_for_absence",
    "quantidade_computadores":     "num_computers",
    "exclusivo_rede_publica":      "public_school_only",
    "companhia_domiciliar":        "household_composition",
    "mae_nivel_escolaridade":      "mother_education_level",
    "pai_nivel_escolaridade":      "father_education_level",
    "quantidade_notebooks":        "num_laptops",
    "estado_civil":                "marital_status",
    "qtd_filhos":                  "num_children",
    "tipo_area_residencial":       "residential_area_type",
    "trabalha":                    "employment_status",
    "situacao":                    "student_status",
    "pontuacao_seletivo":          "admission_score",
    "percentual_frequencia":       "attendance_percentage",
    "reprovacoes":                 "num_failures",
    "idioma":                      "language",
}

# Reverse map for going back to Portuguese
COLUMN_MAP_REVERSE = {v: k for k, v in COLUMN_MAP.items()}

# ═══════════════════════════════════════════════════════════════════════
# 2. CATEGORICAL VALUE TRANSLATIONS
# ═══════════════════════════════════════════════════════════════════════

VALUE_MAPS = {
    # ── Gender ──
    "genero": {
        "F": "Female",
        "M": "Male",
    },

    # ── Race ──
    "raca": {
        "Parda":          "Mixed-race",
        "PARDA":          "Mixed-race",
        "Preta":          "Black",
        "PRETA":          "Black",
        "Branca":         "White",
        "BRANCA":         "White",
        "Amarela":        "Asian-descent",
        "AMARELA":        "Asian-descent",
        "Indígena":       "Indigenous",
        "INDIGENA":       "Indigenous",
        "NAO INFORMADO":  "Not reported",
        "Não declarado":  "Not declared",
    },

    # ── Course Modality ──
    "modalidade": {
        "Integrado":       "Integrated",
        "Subsequente":     "Subsequent",
        "Concomitante":    "Concurrent",
        "Integrado EJA":   "Integrated Adult Ed",
        "Licenciatura":    "Teaching Degree",
        "Bacharelado":     "Bachelor's Degree",
        "Tecnologia":      "Technology Degree",
        "Engenharia":      "Engineering",
    },

    # ── Student Status (target source) ──
    "situacao": {
        "Concluído":                        "Completed",
        "Evasão":                           "Dropout",
        "Cancelado":                        "Cancelled",
        "Cancelamento Compulsório":         "Compulsory Cancellation",
        "Jubilado":                         "Jubilated",
        "Transferido Externo":              "Externally Transferred",
        "Matriculado":                      "Enrolled",
        "Trancado Voluntariamente":         "Voluntarily Suspended",
        "Trancada":                         "Suspended/On Leave",
        "Formado":                          "Graduated",
        "Concludente":                      "Completing",
        "Transferido Interno":              "Internally Transferred",
        "Matrícula Vínculo Institucional":  "Institutional Enrollment",
        "Aguardando Colação de Grau":       "Awaiting Graduation Ceremony",
        "Cancelamento por Duplicidade":     "Cancelled (Duplicate)",
        "Estagiario (concludente)":         "Intern (Completing)",
        "Cancelamento por Desligamento":    "Cancelled (Dismissal)",
        "Aguardando ENADE":                 "Awaiting ENADE Exam",
        "Afastado":                         "On Leave",
        "Falecido":                         "Deceased",
    },

    # ── Marital Status ──
    "estado_civil": {
        "Solteiro(a)":    "Single",
        "Casado(a)":      "Married",
        "União Estável":  "Common-law Partner",
        "Divorciado(a)":  "Divorced",
        "Não declarado":  "Not declared",
        "Viúvo(a)":       "Widowed",
    },

    # ── Residential Area Type ──
    "tipo_area_residencial": {
        "Urbano":                "Urban",
        "Rural":                 "Rural",
        "Comunidade Quilombola": "Quilombola Community",      # Afro-Brazilian heritage community
        "Assentamento rural":    "Rural Settlement",
        "Não informado":         "Not reported",
        "Comunidade Indígena":   "Indigenous Community",
    },

    # ── Household Composition ──
    "companhia_domiciliar": {
        "Pais":          "Both Parents",
        "Mãe":           "Mother",
        "Cônjuge":       "Spouse/Partner",
        "Parentes":      "Relatives",
        "Outro":         "Other",
        "Avó":           "Grandmother",
        "Sozinho":       "Alone",
        "Pai":           "Father",
        "Amigo(s)":      "Friend(s)",
        "Tios":          "Aunt/Uncle",
        "Avô":           "Grandfather",
        "Não informado": "Not reported",
    },

    # ── Employment Status ──
    "trabalha": {
        "Nunca trabalhou":                       "Never worked",
        "Não está trabalhando":                  "Currently not working",
        "Autônomo":                              "Self-employed",
        "Serviço público":                       "Public servant",
        "Empresa privada":                       "Private company",
        "Trabalha com vínculo empregatício":     "Formally employed",
        "Trabalho informal/Bico":                "Informal work/Odd jobs",
        "Trabalhador rural/Agricultor":          "Agricultural worker",
        "Estágio ou bolsa":                      "Internship or scholarship",
        "Aposentado":                            "Retired",
        "Beneficiário ou Pensionista do INSS":   "Social security beneficiary",
        "Não informado":                         "Not reported",
        "Pescador":                              "Fisherman",
    },

    # ── Mother/Father Education Level ──
    # ⚠️ FLAGGED FOR USER REVIEW: These are the Brazilian education level names.
    # The translations below follow the standard Brazilian education system structure.
    "mae_nivel_escolaridade": {
        "Não Estudou":                      "No formal education",
        "Não conhece":                      "Unknown (to student)",        # ⚠️ Student doesn't know
        "Não sei informar":                 "Unable to report",            # ⚠️ Student can't report
        "Alfabetizado":                     "Basic literacy only",         # ⚠️ Literate but no formal diploma
        "Ensino fundamental incompleto":    "Incomplete primary school",   # Grades 1-8, not finished
        "Ensino fundamental completo":      "Complete primary school",     # Grades 1-8 finished
        "Ensino médio incompleto":          "Incomplete high school",
        "Ensino médio completo":            "Complete high school",
        "Ensino superior incompleto":       "Incomplete higher education",
        "Ensino superior completo":         "Complete higher education",
        "Pós-graduação incompleta":         "Incomplete postgraduate",
        "Pós-graduação completa":           "Complete postgraduate",
        "Pós-gradução completa":            "Complete postgraduate",       # ⚠️ Typo in dataset (missing 'a')
    },

    # ── Admission Type ──
    "forma_acesso_seletivo": {
        "CON": "General Admission",    # Concorrência ampla (open competition)
        "COT": "Quota Admission",      # Cotista (affirmative action quota)
    },

    # ── Reason for Absence ──
    # ⚠️ FLAGGED: 99% missing — included for completeness but rarely populated
    "razao_ausencia_educacional": {
        # Values are rare; translate if encountered
    },
}

# Also make pai_nivel_escolaridade use the same map as mae
VALUE_MAPS["pai_nivel_escolaridade"] = VALUE_MAPS["mae_nivel_escolaridade"]

# ═══════════════════════════════════════════════════════════════════════
# 3. FEATURE NAME MAP (for encoded features used in models/XAI)
# ═══════════════════════════════════════════════════════════════════════

# This maps the Phase 1 encoded feature names to English equivalents
ENCODED_FEATURE_MAP = {
    "anoingresso":              "enrollment_year",
    "periodoingresso":          "enrollment_period",
    "rendabruta":               "gross_income",
    "ira":                      "gpa",
    "modalidade":               "course_modality",
    "idade":                    "age",
    "ficou_tempo_sem_estudar":  "had_study_gap",
    "quantidade_computadores":  "num_computers",
    "exclusivo_rede_publica":   "public_school_only",
    "companhia_domiciliar":     "household_composition",
    "mae_nivel_escolaridade":   "mother_education_level",
    "pai_nivel_escolaridade":   "father_education_level",
    "quantidade_notebooks":     "num_laptops",
    "qtd_filhos":               "num_children",
    "tipo_area_residencial":    "residential_area_type",
    "trabalha":                 "employment_status",
    "percentual_frequencia":    "attendance_percentage",
    "reprovacoes":              "num_failures",
    "idioma":                   "language",
    # One-hot encoded features
    "genero_F":                         "gender_Female",
    "genero_M":                         "gender_Male",
    "raca_Amarela":                     "race_Asian-descent",
    "raca_Branca":                      "race_White",
    "raca_Indígena":                    "race_Indigenous",
    "raca_Não declarado":               "race_Not_declared",
    "raca_Parda":                       "race_Mixed-race",
    "raca_Preta":                       "race_Black",
    "estado_civil_Casado(a)":           "marital_Married",
    "estado_civil_Divorciado(a)":       "marital_Divorced",
    "estado_civil_Não declarado":       "marital_Not_declared",
    "estado_civil_Solteiro(a)":         "marital_Single",
    "estado_civil_União Estável":       "marital_Common-law",
    "estado_civil_Viúvo(a)":            "marital_Widowed",
}

def translate_feature_names(pt_names):
    """Translate a list of Portuguese feature names to English."""
    return [ENCODED_FEATURE_MAP.get(n, n) for n in pt_names]


# ═══════════════════════════════════════════════════════════════════════
# 4. BUILD ENGLISH DATAFRAME & SHOW SAMPLE
# ═══════════════════════════════════════════════════════════════════════

print("=" * 72)
print("BUILDING ENGLISH-TRANSLATED DATASET")
print("=" * 72)

# Load raw data
df_pt = pd.read_excel(DATA_PATH)
print(f"\n  Loaded: {df_pt.shape[0]} rows × {df_pt.shape[1]} columns")

# Create English copy
df_en = df_pt.copy()

# 4a. Rename columns
df_en = df_en.rename(columns=COLUMN_MAP)
unmapped_cols = [c for c in df_en.columns if c not in COLUMN_MAP.values()]
if unmapped_cols:
    print(f"\n  ⚠️  Unmapped columns (kept as-is): {unmapped_cols}")

print(f"\n── Column Mapping ──")
print(f"  {'Portuguese':<35s} → {'English':<35s}")
print(f"  {'-'*35}   {'-'*35}")
for pt, en in COLUMN_MAP.items():
    if pt in df_pt.columns:
        print(f"  {pt:<35s} → {en:<35s}")

# 4b. Translate categorical values
print(f"\n── Value Translations ──")
flagged_items = []
for pt_col, value_map in VALUE_MAPS.items():
    en_col = COLUMN_MAP.get(pt_col, pt_col)
    if en_col not in df_en.columns:
        continue
    if not value_map:
        continue

    # Check for any values NOT in the map
    actual_values = df_en[en_col].dropna().unique()
    unmapped_values = [v for v in actual_values if v not in value_map]
    if unmapped_values:
        flagged_items.append((en_col, unmapped_values))

    # Apply translation
    df_en[en_col] = df_en[en_col].map(value_map).fillna(df_en[en_col])
    n_translated = sum(1 for v in actual_values if v in value_map)
    print(f"  {en_col:<35s}: {n_translated}/{len(actual_values)} values translated")

# 4c. Translate boolean columns to Yes/No
bool_cols = ["had_study_gap", "public_school_only", "language"]
for col in bool_cols:
    if col in df_en.columns:
        df_en[col] = df_en[col].map({True: "Yes", False: "No", "True": "Yes", "False": "No"})

# ── Show flagged items ──
if flagged_items:
    print(f"\n── ⚠️  FLAGGED: Untranslated Values (please review) ──")
    for col, vals in flagged_items:
        print(f"  {col}:")
        for v in vals:
            count = (df_en[col] == v).sum() if not pd.isna(v) else df_en[col].isna().sum()
            print(f"    • '{v}' ({count} occurrences) — NO TRANSLATION PROVIDED")

# ═══════════════════════════════════════════════════════════════════════
# 5. DISPLAY SAMPLE & FULL COLUMN LIST
# ═══════════════════════════════════════════════════════════════════════

print(f"\n── English Column List ({len(df_en.columns)} columns) ──")
for i, col in enumerate(df_en.columns):
    pt_col = COLUMN_MAP_REVERSE.get(col, "?")
    print(f"  [{i:>2d}] {col:<35s}  (← {pt_col})")

print(f"\n── Sample: 5 translated rows ──")
# Pick 5 diverse rows — mix of completed and dropout
sample_idx = []
for status in ["Completed", "Dropout", "Enrolled", "Cancelled", "Graduated"]:
    match = df_en[df_en["student_status"] == status]
    if not match.empty:
        sample_idx.append(match.index[0])
if len(sample_idx) < 5:
    sample_idx.extend(df_en.index[:5 - len(sample_idx)])

df_sample = df_en.loc[sample_idx[:5]]

# Print each row vertically for readability
for row_num, (idx, row) in enumerate(df_sample.iterrows()):
    print(f"\n  ─── Row {row_num + 1} (index={idx}) ───")
    for col in df_en.columns:
        val = row[col]
        if pd.isna(val):
            val = "NaN"
        print(f"    {col:<35s}: {val}")

# ═══════════════════════════════════════════════════════════════════════
# 6. SAVE OUTPUTS
# ═══════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 72}")
print("SAVING OUTPUTS")
print("=" * 72)

# Save English CSV
en_csv = os.path.join(OUTPUT_DIR, "dataset_english.csv")
df_en.to_csv(en_csv, index=False, encoding="utf-8-sig")
print(f"  Saved English CSV:     {en_csv}")

# Save Portuguese CSV (for paper-matching)
pt_csv = os.path.join(OUTPUT_DIR, "dataset_portuguese.csv")
df_pt.to_csv(pt_csv, index=False, encoding="utf-8-sig")
print(f"  Saved Portuguese CSV:  {pt_csv}")

# Save the mapping dictionaries as a pickle for reuse in XAI/plots
maps = {
    "column_map": COLUMN_MAP,
    "column_map_reverse": COLUMN_MAP_REVERSE,
    "value_maps": VALUE_MAPS,
    "encoded_feature_map": ENCODED_FEATURE_MAP,
    "translate_feature_names": translate_feature_names,
}
maps_pkl = os.path.join(OUTPUT_DIR, "translation_maps.pkl")
with open(maps_pkl, "wb") as f:
    pickle.dump(maps, f)
print(f"  Saved translation maps: {maps_pkl}")

print(f"\n{'=' * 72}")
print("✅ ENGLISH TRANSLATION COMPLETE")
print("=" * 72)
