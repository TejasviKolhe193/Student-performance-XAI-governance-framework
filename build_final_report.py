# -*- coding: utf-8 -*-
"""
build_final_report.py
Generates the complete Master Report Word document with ALL images,
equations, tables, and student archetype data.
"""

import os, sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

# ─── Colour palette ────────────────────────────────────────────────────────────
C_NAVY      = RGBColor(0x1E, 0x3A, 0x8A)
C_NAVY_HEX  = "1E3A8A"
C_WHITE_HEX = "FFFFFF"
C_STRIPE    = "F0F4FF"
C_STRIPE2   = "F8FAFC"
C_ACCENT    = "EFF6FF"
C_WARN      = "FFF7ED"
C_WARN_BRD  = "F97316"
C_GREEN     = "F0FDF4"
C_GREEN_BRD = "22C55E"
C_BLUE_BRD  = "3B82F6"
C_EQ_BG     = "F1F5F9"

OUTPUT_FILE = "Student_Dropout_XAI_Governance_Framework_Master_Report.docx"
BASE        = r"c:\student-performance-xai-governance-framework"

# ─── Low-level XML helpers ──────────────────────────────────────────────────────
def set_cell_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"),   "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"),  hex_color)
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=140, right=140):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for side, val in [("top", top), ("bottom", bottom),
                      ("left", left), ("right", right)]:
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:w"),    str(val))
        el.set(qn("w:type"), "dxa")
        tcMar.append(el)
    tcPr.append(tcMar)

def set_col_width(table, col_index, width_inches):
    for row in table.rows:
        cell = row.cells[col_index]
        tc   = cell._tc
        tcPr = tc.get_or_add_tcPr()
        tcW  = OxmlElement("w:tcW")
        tcW.set(qn("w:w"),    str(int(width_inches * 1440)))
        tcW.set(qn("w:type"), "dxa")
        tcPr.append(tcW)

def add_paragraph_border_left(para, hex_color, size=18, space=360):
    pPr = para._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    left.set(qn("w:val"),   "single")
    left.set(qn("w:sz"),    str(size))
    left.set(qn("w:space"), str(space))
    left.set(qn("w:color"), hex_color)
    pBdr.append(left)
    pPr.append(pBdr)

def shade_para(para, hex_color):
    pPr = para._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"),   "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"),  hex_color)
    pPr.append(shd)

def set_para_indent(para, left_twips=720):
    pPr = para._p.get_or_add_pPr()
    ind = OxmlElement("w:ind")
    ind.set(qn("w:left"), str(left_twips))
    pPr.append(ind)

def set_table_no_space(table):
    tbl  = table._tbl
    tblPr = tbl.find(qn("w:tblPr"))
    if tblPr is None:
        tblPr = OxmlElement("w:tblPr")
        tbl.insert(0, tblPr)
    spacing = OxmlElement("w:tblCellSpacing")
    spacing.set(qn("w:w"),    "0")
    spacing.set(qn("w:type"), "dxa")
    tblPr.append(spacing)

# ─── Document-level helpers ─────────────────────────────────────────────────────
doc = Document()

# Set page margins
for section in doc.sections:
    section.top_margin    = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin   = Inches(1.1)
    section.right_margin  = Inches(1.1)

styles = doc.styles
normal_style = styles["Normal"]
normal_style.font.name = "Calibri"
normal_style.font.size = Pt(11)

def add_h1(text):
    p = doc.add_paragraph(text, style="Heading 1")
    p.runs[0].font.color.rgb = C_NAVY
    p.runs[0].font.size = Pt(18)
    p.runs[0].bold = True
    return p

def add_h2(text):
    p = doc.add_paragraph(text, style="Heading 2")
    p.runs[0].font.color.rgb = C_NAVY
    p.runs[0].font.size = Pt(14)
    p.runs[0].bold = True
    return p

def add_h3(text):
    p = doc.add_paragraph(text, style="Heading 3")
    p.runs[0].font.size = Pt(12)
    p.runs[0].bold = True
    return p

def add_body(text, bold=False, italic=False, size=11):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold   = bold
    r.italic = italic
    r.font.size = Pt(size)
    return p

def add_bullet(text, level=0):
    p = doc.add_paragraph(text, style="List Bullet")
    p.paragraph_format.left_indent = Inches(0.25 * (level + 1))
    return p

def add_image(rel_path, caption, width=Inches(6.0)):
    full = os.path.join(BASE, rel_path)
    if not os.path.exists(full):
        add_body(f"[IMAGE NOT FOUND: {rel_path}]", italic=True)
        return
    doc.add_picture(full, width=width)
    last = doc.paragraphs[-1]
    last.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap = doc.add_paragraph(caption)
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.runs[0].italic = True
    cap.runs[0].font.size = Pt(9.5)
    cap.runs[0].font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

def add_callout(lines, border_color=C_BLUE_BRD, bg_color=C_EQ_BG, bold_first=False):
    """Add a styled callout box with left border."""
    for i, line in enumerate(lines):
        p = doc.add_paragraph()
        shade_para(p, bg_color)
        add_paragraph_border_left(p, border_color, size=24, space=360)
        set_para_indent(p, left_twips=360)
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after  = Pt(2)
        r = p.add_run(line)
        r.font.name = "Courier New"
        r.font.size = Pt(10)
        if i == 0 and bold_first:
            r.bold = True

def add_eq_block(title, equations):
    """Add an equation block with a title and list of equations."""
    p = doc.add_paragraph()
    shade_para(p, C_EQ_BG)
    add_paragraph_border_left(p, C_BLUE_BRD, size=32, space=360)
    set_para_indent(p, left_twips=360)
    r = p.add_run(f"  {title}")
    r.bold = True
    r.font.size = Pt(10.5)
    r.font.color.rgb = C_NAVY
    for eq in equations:
        p2 = doc.add_paragraph()
        shade_para(p2, C_EQ_BG)
        add_paragraph_border_left(p2, C_BLUE_BRD, size=32, space=360)
        set_para_indent(p2, left_twips=720)
        p2.paragraph_format.space_before = Pt(1)
        p2.paragraph_format.space_after  = Pt(1)
        r2 = p2.add_run(f"  {eq}")
        r2.font.name = "Courier New"
        r2.font.size = Pt(10)

def add_note_box(text, color=C_WARN, border=C_WARN_BRD):
    p = doc.add_paragraph()
    shade_para(p, color)
    add_paragraph_border_left(p, border, size=24, space=360)
    set_para_indent(p, left_twips=360)
    r = p.add_run(text)
    r.font.size = Pt(10)

def make_table(headers, rows, font_size=9.5, col_widths=None, stripe=True):
    """Create a styled table with navy header and alternating rows."""
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Header row
    hdr = t.rows[0]
    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        set_cell_bg(cell, C_NAVY_HEX)
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(font_size)

    # Data rows
    for ri, row_data in enumerate(rows):
        row = t.add_row()
        bg  = C_STRIPE if (stripe and ri % 2 == 0) else C_WHITE_HEX
        for ci, val in enumerate(row_data):
            cell = row.cells[ci]
            set_cell_bg(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(str(val))
            r.font.size = Pt(font_size)

    if col_widths:
        for ci, w in enumerate(col_widths):
            set_col_width(t, ci, w)
    return t

# ═══════════════════════════════════════════════════════════════════════════════
# COVER PAGE
# ═══════════════════════════════════════════════════════════════════════════════
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("STUDENT DROPOUT PREDICTION")
r.bold = True
r.font.size = Pt(24)
r.font.color.rgb = C_NAVY

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Explainable AI & Governance Framework")
r.bold = True
r.font.size = Pt(18)
r.font.color.rgb = C_NAVY

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Master Research Report")
r.font.size = Pt(14)
r.italic = True

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run(
    "A comprehensive study covering dataset analysis, machine learning model selection,\n"
    "explainability (SHAP & LIME), algorithmic fairness auditing, and an\n"
    "institutional AI governance framework for dropout intervention."
)
r.font.size = Pt(11)

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Dataset: UCI Student Performance (800 students) | Institution: Portuguese Higher Education")
r.font.size = Pt(10)
r.italic = True

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# TABLE OF CONTENTS (manual)
# ═══════════════════════════════════════════════════════════════════════════════
add_h1("Table of Contents")
toc_items = [
    ("1.", "Project Overview & Research Gap"),
    ("2.", "Dataset Description"),
    ("3.", "Phase 1 — Data Exploration & Preprocessing"),
    ("4.", "Phase 2 — Machine Learning Model Selection"),
    ("5.", "Phase 3 — Explainable AI (SHAP & LIME)"),
    ("6.", "Phase 4 — Algorithmic Fairness Audit"),
    ("7.", "Phase 5 — Governance Framework"),
    ("8.", "Integrated Results Summary"),
    ("9.", "Limitations & Future Work"),
]
for num, title in toc_items:
    p = doc.add_paragraph()
    r1 = p.add_run(f"{num}  ")
    r1.bold = True
    r1.font.size = Pt(11)
    r2 = p.add_run(title)
    r2.font.size = Pt(11)
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — PROJECT OVERVIEW & RESEARCH GAP
# ═══════════════════════════════════════════════════════════════════════════════
add_h1("1. Project Overview & Research Gap")

add_body(
    "Student dropout is a critical challenge for higher-education institutions worldwide. "
    "When a student leaves before completing their degree, the institution loses tuition revenue, "
    "ranking points, and — most importantly — the student loses the opportunity for career advancement. "
    "Early identification of at-risk students allows counsellors to intervene with targeted support "
    "before it is too late."
)
add_body(
    "This project builds a complete, production-ready pipeline that goes far beyond simply building "
    "a predictive model. It answers five layered research questions that prior work had not "
    "addressed together in a single system:"
)

questions = [
    ("RQ1", "Which machine learning model most accurately predicts student dropout?"),
    ("RQ2", "Why does the model make each individual prediction? (Explainability)"),
    ("RQ3", "Is the model fair across demographic groups (gender, age, income)?"),
    ("RQ4", "How should institutions govern AI-driven dropout tools responsibly?"),
    ("RQ5", "Can a single framework integrate prediction + explanation + fairness + governance?"),
]
for code, q in questions:
    p = doc.add_paragraph()
    r = p.add_run(f"{code}: ")
    r.bold = True
    r.font.color.rgb = C_NAVY
    p.add_run(q)

add_h2("1.1 Research Gap")
add_body(
    "The base paper (Paper 10 — 2025 Portuguese study on student performance) introduced a "
    "Random Forest model trained on a Portuguese higher-education dataset. It demonstrated strong "
    "predictive accuracy but had three major gaps that this project addresses:"
)
gaps = [
    "No explainability: The paper provided feature importance rankings but no per-student explanations. "
     "An instructor cannot act on 'attendance is important'; they need 'Student #37 is at risk because "
     "their attendance dropped 15% this semester.'",
    "No fairness audit: The model was never tested for bias across gender, age, or income cohorts. "
     "A model that accurately predicts dropout but systematically over-flags female or low-income "
     "students is ethically unacceptable.",
    "No governance framework: There was no institutional policy for who reviews AI decisions, "
     "how appeals are handled, what data is logged, or how the model is monitored over time.",
]
for g in gaps:
    add_bullet(g)

add_body(
    "This project fills all three gaps by building five integrated phases on top of the base paper's "
    "foundation, producing a system that is not just accurate, but explainable, fair, and governable."
)
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — DATASET
# ═══════════════════════════════════════════════════════════════════════════════
add_h1("2. Dataset Description")
add_body(
    "The dataset used is the UCI Machine Learning Repository — Student Performance / Dropout dataset, "
    "collected from a Portuguese polytechnic institution. It contains academic, demographic, and "
    "socioeconomic attributes for 800 students enrolled between 2008 and 2019."
)
add_h2("2.1 Dataset Statistics")
make_table(
    ["Attribute", "Value"],
    [
        ["Total students",         "800"],
        ["Features (raw)",         "36"],
        ["Features (after selection)", "10"],
        ["Target classes",         "Dropout / Completed"],
        ["Dropout rate (raw)",     "~49.9% (399 students)"],
        ["Completion rate (raw)",  "~50.1% (401 students)"],
        ["Academic years covered", "2008 – 2019"],
        ["Country",                "Portugal"],
        ["Institution type",       "Polytechnic (higher education)"],
    ],
    col_widths=[2.5, 3.5],
)
doc.add_paragraph()
add_h2("2.2 Selected Features (Post Phase 1)")
make_table(
    ["#", "Feature Name", "Type", "Description"],
    [
        ["1",  "IRA (Academic Performance)", "Continuous", "Curricular units approval rate — primary dropout predictor"],
        ["2",  "Course Failures",            "Integer",    "Number of failed course units"],
        ["3",  "Attendance Rate (%)",        "Continuous", "Percentage of classes attended"],
        ["4",  "Student Age",                "Integer",    "Age at time of enrollment"],
        ["5",  "Enrollment Year",            "Integer",    "Academic year of first enrollment"],
        ["6",  "Course Modality",            "Categorical","Daytime (1) vs Evening (3) course"],
        ["7",  "Father's Education Level",   "Ordinal",    "0–8 scale of paternal educational attainment"],
        ["8",  "Family Gross Income",        "Continuous", "Annual household income in EUR"],
        ["9",  "Laptops at Home",            "Binary",     "Indicator of home technology access (0/1)"],
        ["10", "Gender",                     "Binary",     "0=Female, 1=Male (fairness-sensitive attribute)"],
    ],
    col_widths=[0.3, 2.0, 1.1, 3.3],
    font_size=9,
)
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — PHASE 1
# ═══════════════════════════════════════════════════════════════════════════════
add_h1("3. Phase 1 — Data Exploration & Preprocessing")
add_body(
    "Phase 1 ingested the raw 800-student dataset and performed systematic cleaning, outlier "
    "handling, feature engineering, and class-balance assessment. The goal was to produce a "
    "clean, analysis-ready dataset that would feed reliably into machine learning in Phase 2."
)

add_h2("3.1 Steps Performed")
steps = [
    "Missing value analysis — confirmed no missing values in the 800-row dataset.",
    "Outlier detection using IQR Winsorization — extreme values were clipped rather than removed "
     "to preserve all 800 rows.",
    "Feature engineering — computed IRA (approval rate) from raw curricular unit counts; "
     "standardised continuous features.",
    "Class balance check — Dropout: 399 students (49.9%), Completed: 401 students (50.1%). "
     "Near-perfect balance, but three resampling strategies were still evaluated in Phase 2.",
    "Feature correlation analysis — identified highly correlated raw features; reduced 36 → 10.",
    "Exploratory Data Analysis (EDA) — distribution plots for every feature, split by target class.",
]
for s in steps:
    add_bullet(s)

add_h2("3.2 IQR Winsorization Equations")
add_body(
    "To handle outliers without discarding data, IQR (Interquartile Range) Winsorization was "
    "applied to all continuous features. Values beyond the computed bounds were clipped to "
    "the bound value:"
)
add_eq_block(
    "IQR Winsorization (Outlier Clipping)",
    [
        "IQR    = Q3 - Q1",
        "lower  = Q1 - 1.5 * IQR",
        "upper  = Q3 + 1.5 * IQR",
        "",
        "Special case (IQR = 0, i.e. zero-variance feature):",
        "lower  = P01  (1st percentile of that feature)",
        "upper  = P99  (99th percentile of that feature)",
        "",
        "Clipping rule:  x_clipped = max(lower, min(x, upper))",
    ]
)
add_note_box(
    "Why Winsorization instead of removal?  Removing outlier rows would shrink an already-modest "
    "800-row dataset and could introduce selection bias. Clipping preserves every student while "
    "preventing extreme values from distorting the model's decision boundaries.",
    color=C_ACCENT, border=C_BLUE_BRD
)

add_h2("3.3 Phase 1 Output — EDA Dashboard")
add_body(
    "The following 9-panel figure shows the distribution of every key feature, split by outcome "
    "(blue = Dropout, orange = Completed). Key observations: IRA is strongly bimodal — dropouts "
    "cluster near 0–4, completers near 6–10. Failures are heavily right-skewed for dropouts. "
    "Attendance is lower for dropouts on average."
)
add_image(r"phase1_outputs\01_phase1_eda_and_preprocessing.png",
          "Figure 1: Phase 1 EDA — Feature distributions by outcome (9 panels).", width=Inches(6.5))
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — PHASE 2
# ═══════════════════════════════════════════════════════════════════════════════
add_h1("4. Phase 2 — Machine Learning Model Selection")
add_body(
    "Phase 2 systematically searched for the best combination of (a) class-balancing strategy, "
    "(b) feature-selection method, and (c) classification algorithm. A total of 48 experiments "
    "were run, each using GridSearchCV with 5-fold inner cross-validation optimised for Recall. "
    "Recall was chosen as the primary metric because false negatives (missing at-risk students) "
    "are far more costly than false positives (unnecessary check-ins)."
)

add_h2("4.1 Experimental Design")
make_table(
    ["Dimension", "Options Tested"],
    [
        ["Balancing Strategy (4)",   "Unbalanced | OverSampling (SMOTE) | UnderSampling | SMOTEENN"],
        ["Feature Selection (3)",    "ANOVA F-test | Backward Elimination | Feature Importance"],
        ["Model (4)",                "Random Forest | Decision Tree | Logistic Regression | SVM"],
        ["Total Experiments",        "4 × 3 × 4 = 48"],
        ["Optimisation Metric",      "Recall (minimise missed at-risk students)"],
        ["CV Strategy",              "5-fold inner CV (GridSearchCV) + 10-fold outer CV for stability"],
    ],
    col_widths=[2.3, 4.4],
)

add_h2("4.2 Hyperparameter Search Grids")
make_table(
    ["Model", "Parameter", "Values Searched"],
    [
        ["Random Forest",      "max_depth",          "None, 10, 20"],
        ["Random Forest",      "min_samples_split",  "2, 5"],
        ["Random Forest",      "criterion",          "gini, entropy"],
        ["Decision Tree",      "max_depth",          "None, 10, 20"],
        ["Decision Tree",      "min_samples_split",  "2, 5"],
        ["Decision Tree",      "criterion",          "gini, entropy"],
        ["Logistic Regression","C",                  "0.1, 1.0, 10.0"],
        ["Logistic Regression","solver",             "lbfgs, liblinear"],
        ["Logistic Regression","max_iter",           "1000 (fixed)"],
        ["SVM",               "C",                  "0.1, 1.0, 10.0"],
        ["SVM",               "kernel",             "rbf, linear"],
        ["SVM",               "max_iter",           "2000 (fixed)"],
    ],
    col_widths=[1.9, 2.0, 2.8],
)

add_h2("4.3 Performance Equations")
add_body("All models are evaluated on a held-out test set using these standard metrics:")
add_eq_block(
    "Classification Performance Metrics",
    [
        "Precision   = TP / (TP + FP)",
        "             [Of all flagged dropouts, how many were correct?]",
        "",
        "Recall      = TP / (TP + FN)",
        "             [Of all true dropouts, how many did we catch?]",
        "",
        "F1-Score    = 2 * (Precision * Recall) / (Precision + Recall)",
        "             [Harmonic mean — balances Precision and Recall]",
        "",
        "Accuracy    = (TP + TN) / (TP + TN + FP + FN)",
        "             [Overall correct predictions across all students]",
        "",
        "AUC-ROC     = Area under the Receiver Operating Characteristic curve",
        "             [Probability that model ranks a dropout higher than a completer]",
        "",
        "Where:  TP = True Positive  (dropout correctly flagged)",
        "        TN = True Negative  (completer correctly passed)",
        "        FP = False Positive (completer incorrectly flagged as dropout)",
        "        FN = False Negative (dropout missed — most costly error)",
    ]
)

add_h2("4.4 Champion Model")
add_note_box(
    "WINNER: Random Forest | UnderSampling | FeatureImportance Selection\n"
    "Best Params: criterion='gini', max_depth=20, min_samples_split=5\n"
    "Recall: 84.8% | Precision: 83.6% | F1: 84.2% | AUC: 95.1% | Accuracy: 92.9% | 10-CV Recall: 87.8%",
    color=C_GREEN, border=C_GREEN_BRD
)
add_body(
    "The champion Random Forest with UnderSampling + Feature Importance selection achieved the "
    "best balance of Recall (catching most dropouts) while maintaining high Precision (few false "
    "alarms). It caught 84.8% of all actual dropout students — meaning only ~15% were missed. "
    "Its AUC of 95.1% demonstrates near-perfect ranking ability across all decision thresholds."
)

add_h2("4.5 Model Comparison Charts")
add_image(r"01_model_comparison.png",
          "Figure 2: Model comparison — Recall, Precision, F1, and AUC across all 4 model types.", width=Inches(6.5))
add_image(r"02_confusion_matrices.png",
          "Figure 3: Confusion matrices for all 4 model types (champion configuration).", width=Inches(6.5))
add_image(r"03_roc_curves.png",
          "Figure 4: ROC curves for all 4 classifiers — Random Forest AUC = 0.951.", width=Inches(6.5))
add_image(r"04_balancing_strategy_impact.png",
          "Figure 5: Effect of balancing strategy (Unbalanced / SMOTE / UnderSampling / SMOTEENN) on Recall.", width=Inches(6.5))
add_image(r"05_top_features_importance.png",
          "Figure 6: Top 10 feature importances from champion Random Forest model.", width=Inches(6.0))

add_h2("4.6 Full 48-Experiment Results Table")
add_body(
    "Every experiment is shown below, sorted by Recall (descending). Each row represents a "
    "unique combination of balancing strategy, feature selection method, and classifier. "
    "The champion row is the first RF entry (row 7)."
)
exp_headers = ["Balance", "Feat.Sel.", "Model", "Recall", "Prec.", "F1", "AUC", "Acc.", "10-CV Rec.", "Best Params"]
exp_rows = [
    ["SMOTEENN","ANOVA","SVM","0.914","0.231","0.369","0.591","0.301","0.873","C=0.1, rbf"],
    ["UnderSampling","Backward","SVM","0.910","0.231","0.369","0.759","0.303","0.695","C=10.0, rbf"],
    ["UnderSampling","ANOVA","SVM","0.907","0.231","0.368","0.727","0.303","0.801","C=10.0, rbf"],
    ["Unbalanced","ANOVA","SVM","0.902","0.230","0.367","0.689","0.303","0.867","C=0.1, rbf"],
    ["SMOTEENN","FeatImp","SVM","0.895","0.232","0.369","0.720","0.314","0.863","C=1.0, rbf"],
    ["Unbalanced","Backward","SVM","0.859","0.234","0.367","0.686","0.337","0.849","C=10.0, rbf"],
    ["UnderSampling","FeatImp","RF","0.848","0.836","0.842","0.951","0.929","0.878","gini, d=20, s=5"],
    ["UnderSampling","ANOVA","RF","0.846","0.841","0.844","0.950","0.930","0.877","gini, d=None, s=5"],
    ["UnderSampling","ANOVA","DT","0.846","0.640","0.729","0.854","0.859","0.879","gini, d=None, s=2"],
    ["UnderSampling","Backward","RF","0.842","0.851","0.846","0.953","0.931","0.874","entropy, d=10, s=2"],
    ["SMOTE","FeatImp","SVM","0.842","0.233","0.365","0.627","0.343","0.708","C=0.1, rbf"],
    ["UnderSampling","Backward","DT","0.837","0.639","0.725","0.850","0.857","0.879","gini, d=None, s=2"],
    ["SMOTEENN","Backward","DT","0.836","0.785","0.809","0.885","0.912","0.965","entropy, d=20, s=2"],
    ["UnderSampling","FeatImp","DT","0.834","0.619","0.711","0.843","0.848","0.874","gini, d=None, s=2"],
    ["SMOTEENN","ANOVA","RF","0.833","0.869","0.850","0.946","0.934","0.978","gini, d=None, s=2"],
    ["SMOTEENN","Backward","RF","0.830","0.872","0.851","0.952","0.935","0.976","gini, d=None, s=2"],
    ["SMOTEENN","ANOVA","DT","0.830","0.798","0.814","0.885","0.915","0.963","gini, d=None, s=2"],
    ["SMOTEENN","FeatImp","DT","0.827","0.784","0.805","0.880","0.910","0.964","entropy, d=20, s=2"],
    ["Unbalanced","FeatImp","SVM","0.822","0.233","0.363","0.639","0.353","0.866","C=0.1, rbf"],
    ["SMOTEENN","FeatImp","RF","0.820","0.879","0.848","0.950","0.934","0.976","entropy, d=20, s=2"],
    ["SMOTE","ANOVA","RF","0.817","0.914","0.863","0.950","0.942","0.949","gini, d=20, s=2"],
    ["SMOTE","Backward","DT","0.817","0.799","0.808","0.879","0.913","0.940","entropy, d=None, s=2"],
    ["SMOTE","FeatImp","RF","0.814","0.918","0.863","0.952","0.942","0.952","gini, d=None, s=5"],
    ["SMOTE","Backward","RF","0.809","0.921","0.861","0.954","0.942","0.952","gini, d=None, s=5"],
    ["SMOTE","ANOVA","DT","0.809","0.821","0.815","0.879","0.918","0.940","entropy, d=None, s=2"],
    ["Unbalanced","Backward","DT","0.808","0.811","0.809","0.877","0.915","0.827","gini, d=None, s=2"],
    ["Unbalanced","ANOVA","DT","0.803","0.809","0.806","0.874","0.913","0.824","entropy, d=None, s=2"],
    ["Unbalanced","Backward","RF","0.799","0.942","0.865","0.953","0.944","0.831","gini, d=None, s=5"],
    ["Unbalanced","FeatImp","RF","0.799","0.941","0.864","0.950","0.944","0.830","gini, d=20, s=2"],
    ["Unbalanced","ANOVA","RF","0.796","0.939","0.861","0.949","0.943","0.832","gini, d=20, s=5"],
    ["SMOTE","FeatImp","DT","0.794","0.800","0.797","0.869","0.910","0.942","entropy, d=None, s=2"],
    ["Unbalanced","FeatImp","DT","0.793","0.822","0.807","0.872","0.915","0.835","gini, d=None, s=2"],
    ["SMOTEENN","Backward","LR","0.787","0.718","0.751","0.899","0.883","0.862","C=10.0, lbfgs"],
    ["SMOTEENN","ANOVA","LR","0.783","0.713","0.746","0.897","0.881","0.866","C=0.1, liblinear"],
    ["SMOTEENN","FeatImp","LR","0.775","0.717","0.745","0.899","0.881","0.867","C=1.0, lbfgs"],
    ["SMOTE","ANOVA","LR","0.743","0.735","0.739","0.896","0.882","0.777","C=0.1, liblinear"],
    ["SMOTE","FeatImp","LR","0.741","0.739","0.740","0.897","0.883","0.778","C=10.0, lbfgs"],
    ["SMOTE","Backward","LR","0.741","0.737","0.739","0.898","0.883","0.773","C=0.1, lbfgs"],
    ["UnderSampling","FeatImp","LR","0.741","0.737","0.739","0.897","0.883","0.767","C=0.1, liblinear"],
    ["UnderSampling","Backward","LR","0.740","0.737","0.739","0.898","0.883","0.764","C=10.0, lbfgs"],
    ["UnderSampling","ANOVA","LR","0.740","0.736","0.738","0.897","0.882","0.767","C=0.1, lbfgs"],
    ["SMOTE","ANOVA","SVM","0.740","0.253","0.377","0.643","0.451","0.785","C=10.0, rbf"],
    ["SMOTEENN","Backward","SVM","0.731","0.293","0.418","0.670","0.544","0.837","C=10.0, rbf"],
    ["Unbalanced","FeatImp","LR","0.654","0.775","0.709","0.894","0.880","0.677","C=1.0, liblinear"],
    ["Unbalanced","ANOVA","LR","0.652","0.775","0.708","0.894","0.880","0.678","C=0.1, liblinear"],
    ["Unbalanced","Backward","LR","0.651","0.777","0.709","0.895","0.880","0.679","C=0.1, lbfgs"],
    ["SMOTE","Backward","SVM","0.649","0.306","0.416","0.683","0.592","0.759","C=10.0, rbf"],
    ["UnderSampling","FeatImp","SVM","0.499","0.276","0.355","0.609","0.595","0.546","C=0.1, linear"],
]
make_table(exp_headers, exp_rows, font_size=8,
           col_widths=[1.25, 0.9, 0.55, 0.55, 0.5, 0.5, 0.5, 0.5, 0.8, 1.6])
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — PHASE 3: XAI
# ═══════════════════════════════════════════════════════════════════════════════
add_h1("5. Phase 3 — Explainable AI (SHAP & LIME)")
add_body(
    "The champion Random Forest model from Phase 2 achieves 84.8% recall but is a 'black box' — "
    "instructors cannot see why it flags a particular student. Phase 3 applies two complementary "
    "explainability techniques to make every prediction interpretable:"
)
add_bullet("SHAP (SHapley Additive exPlanations) — global + per-student explanations using game theory.")
add_bullet("LIME (Local Interpretable Model-agnostic Explanations) — local linear surrogate for each student.")

add_h2("5.1 SHAP Mathematical Foundation")
add_body(
    "SHAP computes each feature's contribution to a prediction using the Shapley value from "
    "cooperative game theory. For a model f and student x with N features:"
)
add_eq_block(
    "SHAP Shapley Value Formula",
    [
        "phi_i(f, x) = SUM over all subsets S (not containing i):",
        "",
        "  phi_i = S_sum [ |S|! * (|N| - |S| - 1)! / |N|! * (f(S u {i}) - f(S)) ]",
        "",
        "Where:",
        "  phi_i      = SHAP value for feature i (contribution to prediction)",
        "  S          = subset of features NOT including feature i",
        "  |S|        = number of features in subset S",
        "  |N|        = total number of features",
        "  f(S u {i}) = model output when feature i IS included",
        "  f(S)       = model output when feature i is EXCLUDED",
        "  Positive phi_i => feature i pushes prediction towards Dropout",
        "  Negative phi_i => feature i pushes prediction towards Completed",
    ]
)
add_note_box(
    "Intuition: Each SHAP value answers 'How much does this specific feature value, for this "
    "specific student, shift the prediction away from the average?' Features with large positive "
    "SHAP values are the primary drivers of dropout risk.",
    color=C_ACCENT, border=C_BLUE_BRD
)

add_h2("5.2 LIME Mathematical Foundation")
add_body(
    "LIME builds a simple local linear model around a single student's data point. "
    "For student x, LIME finds an explanation model g that approximates f locally:"
)
add_eq_block(
    "LIME Local Surrogate Model",
    [
        "g(z') = w_0 + w_1*z'_1 + w_2*z'_2 + ... + w_k*z'_k",
        "",
        "Objective: minimise  L(f, g, pi_x) + Omega(g)",
        "",
        "Where:",
        "  g(z')   = local linear surrogate model",
        "  z'      = binary vector (1 = feature present, 0 = feature absent)",
        "  w_j     = weight (importance) of feature j for this student",
        "  pi_x(z) = proximity kernel (weights samples near student x more heavily)",
        "  L(...)  = weighted loss between f (RF) and g (linear) over local samples",
        "  Omega(g)= complexity penalty (keeps g interpretable)",
        "",
        "Positive w_j => feature increases dropout probability for this student",
        "Negative w_j => feature decreases dropout probability for this student",
    ]
)

add_h2("5.3 Global SHAP Analysis")
add_body(
    "These charts show which features are most important GLOBALLY across all 800 students. "
    "The beeswarm plot shows both magnitude and direction; the bar chart shows mean absolute SHAP."
)
add_image(r"phase3_outputs\01_shap_global_beeswarm.png",
          "Figure 7: SHAP Global Beeswarm — each dot = one student. Red = high feature value, Blue = low. "
          "IRA (GPA) dominates — high IRA strongly protects, low IRA strongly increases risk.", width=Inches(6.5))
add_image(r"phase3_outputs\02_shap_feature_importance.png",
          "Figure 8: Mean |SHAP| feature importance — IRA leads at ~0.25, followed by Failures (~0.09) "
          "and Attendance (~0.05).", width=Inches(6.0))
add_image(r"phase3_outputs\03_shap_dependence_ira.png",
          "Figure 9: SHAP Dependence Plot for IRA — shows non-linear relationship. "
          "Risk rises sharply when IRA < 5.0; protective effect kicks in above 7.0.", width=Inches(6.0))

add_h2("5.4 Cohort XAI Analysis (Gender)")
add_body("SHAP values were also compared across demographic cohorts to understand group-level model behaviour:")
make_table(
    ["Cohort", "Count", "Avg |SHAP| for IRA", "Interpretation"],
    [
        ["Female students", "441 (55.1%)", "0.2686", "IRA slightly less dominant driver for females"],
        ["Male students",   "359 (44.9%)", "0.2756", "IRA marginally stronger driver for males"],
        ["Difference",      "—",           "0.0070", "Minimal gender gap in explanation drivers"],
    ],
    col_widths=[1.7, 1.5, 1.8, 2.8],
)

add_h2("5.5 Individual Student Explanations — SHAP Waterfall Charts")
add_body(
    "SHAP waterfall charts show how each feature pushes the prediction up (red, towards Dropout) "
    "or down (blue, towards Completed) from the baseline probability for each individual student."
)

add_h3("High-Risk Student #0 (99.4% Dropout Risk)")
add_note_box(
    "Student #0: GPA=1.89 | Attendance=77% | Failures=8 | Income=0 | Pred=Dropout | Actual=Dropout\n"
    "Top SHAP drivers: IRA=+0.2831 | Failures=+0.1134 | Attendance=+0.0562",
    color="FFF0F0", border="EF4444"
)
add_image(r"phase3_outputs\04_shap_high_risk_student_0.png",
          "Figure 10: SHAP waterfall — Student #0 (99.4% risk). IRA pushes risk up by +0.283, "
          "Failures by +0.113. All features increase risk.", width=Inches(6.0))

add_h3("Low-Risk Student #1 (3.4% Dropout Risk)")
add_note_box(
    "Student #1: GPA=9.18 | Attendance=98% | Failures=0 | Income=600 | Pred=Completed | Actual=Completed\n"
    "Top SHAP drivers: IRA=-0.3065 | Failures=-0.0537 | Attendance=-0.0443",
    color=C_GREEN, border=C_GREEN_BRD
)
add_image(r"phase3_outputs\04_shap_low_risk_student_1.png",
          "Figure 11: SHAP waterfall — Student #1 (3.4% risk). IRA pushes risk DOWN by -0.307, "
          "all features are protective.", width=Inches(6.0))

add_h3("Borderline Student #37 (50.1% Dropout Risk — False Positive)")
add_note_box(
    "Student #37: GPA=7.12 | Attendance=87% | Failures=1 | Income=1600 | Pred=Dropout | Actual=Completed\n"
    "Top SHAP: Attendance=+0.0746 | EnrollYear=-0.0318 | FathersEdu=-0.0263 | Modality=+0.0235\n"
    "Note: IRA is NOT the top driver here — attendance pattern overrides the decent GPA.",
    color=C_WARN, border=C_WARN_BRD
)
add_image(r"phase3_outputs\04_shap_borderline_student_37.png",
          "Figure 12: SHAP waterfall — Student #37 (50.1% risk, false positive). "
          "Near-equal push from risk-increasing and protective features — genuine borderline case.", width=Inches(6.0))

add_h2("5.6 Individual Student Explanations — LIME Bar Charts")
add_body(
    "LIME builds a local linear model around each student and shows feature weights as signed bars. "
    "Green bars reduce dropout probability; red bars increase it."
)

add_h3("LIME — High-Risk Student #0")
add_image(r"phase3_outputs\05_lime_chart_high_risk_student_0.png",
          "Figure 13: LIME explanation — Student #0. Every feature bar points towards Dropout. "
          "IRA weight is largest positive contributor.", width=Inches(6.0))

add_h3("LIME — Low-Risk Student #1")
add_image(r"phase3_outputs\05_lime_chart_low_risk_student_1.png",
          "Figure 14: LIME explanation — Student #1. All bars point towards Completed (green). "
          "IRA is the dominant protective factor.", width=Inches(6.0))

add_h3("LIME — Borderline Student #37")
add_image(r"phase3_outputs\05_lime_chart_borderline_37_student_37.png",
          "Figure 15: LIME explanation — Student #37. Mixed bars — some features push towards dropout, "
          "others are protective. This confirms the borderline nature of the prediction.", width=Inches(6.0))

add_h3("LIME — Borderline Student #43 (100% Risk, Counsellor Dashboard Example)")
add_body(
    "Student #43 was highlighted in the counsellor-facing XAI dashboard as a worked example. "
    "Despite 100% risk in the training set, the dashboard showed counterfactual simulations "
    "(what-if the student raised their GPA from 0.63 to 5.0, how much would risk drop)."
)
add_note_box(
    "Student #43: GPA=0.63 | Attendance=71% | Failures=7 | Income=800 | Age=26 | Pred=Dropout | Actual=Dropout\n"
    "Top SHAP: IRA=+0.2672 | Failures=+0.1181 | Attendance=+0.0612 | Modality=+0.0301 | Age=+0.0157",
    color="FFF0F0", border="EF4444"
)
add_image(r"phase3_outputs\05_lime_chart_borderline_43_student_43.png",
          "Figure 16: LIME explanation — Student #43. Very high-risk student used as the counsellor "
          "dashboard demonstration case.", width=Inches(6.0))

add_h2("5.7 All 12 Student Archetypes — Summary Table")
add_body(
    "The following table summarises all 12 student archetypes stored in the system. "
    "These represent diverse risk profiles from across the test set."
)
make_table(
    ["Student #", "Risk %", "Pred", "Actual", "GPA (IRA)", "Attend%", "Failures", "Income", "Top SHAP Feature", "Top SHAP Val"],
    [
        ["#0",   "99.4%", "Dropout",   "Dropout",   "1.89", "77%",  "8", "0",    "IRA",          "+0.2831"],
        ["#43",  "100%",  "Dropout",   "Dropout",   "0.63", "71%",  "7", "800",  "IRA",          "+0.2672"],
        ["#85",  "96.5%", "Dropout",   "Dropout",   "3.66", "88%",  "5", "938",  "IRA",          "+0.3358"],
        ["#185", "89.2%", "Dropout",   "Dropout",   "4.82", "100%", "0", "930",  "IRA",          "+0.5039"],
        ["#37",  "50.1%", "Dropout",   "Completed", "7.12", "87%",  "1", "1600", "Attendance",   "+0.0746"],
        ["#102", "2.8%",  "Completed", "Completed", "8.75", "96%",  "0", "1000", "IRA",          "-0.3227"],
        ["#1",   "3.4%",  "Completed", "Completed", "9.18", "98%",  "0", "600",  "IRA",          "-0.3065"],
        ["#25",  "5.8%",  "Completed", "Completed", "8.35", "94%",  "0", "500",  "IRA",          "-0.3237"],
        ["#60",  "6.5%",  "Completed", "Completed", "8.15", "96%",  "0", "687",  "IRA",          "-0.2889"],
        ["#14",  "5.4%",  "Completed", "Completed", "8.74", "99%",  "0", "2000", "IRA",          "-0.2613"],
        ["#52",  "11.1%", "Completed", "Completed", "8.58", "97%",  "0", "2400", "EnrollYear",   "+0.1278"],
        ["#312", "9.7%",  "Completed", "Completed", "9.36", "97%",  "0", "1000", "IRA",          "-0.3099"],
    ],
    col_widths=[0.65, 0.6, 0.75, 0.7, 0.7, 0.65, 0.65, 0.6, 1.25, 0.85],
    font_size=8.5,
)
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — PHASE 4: FAIRNESS AUDIT
# ═══════════════════════════════════════════════════════════════════════════════
add_h1("6. Phase 4 — Algorithmic Fairness Audit")
add_body(
    "A predictive model may achieve excellent accuracy while being systematically biased against "
    "certain demographic groups. Phase 4 audits the champion Random Forest across three sensitive "
    "attributes: Gender, Age Group, and Income Level."
)

add_h2("6.1 Fairness Metric Equations")
add_eq_block(
    "Fairness Metrics (AIF360 Framework)",
    [
        "Disparate Impact (DI):",
        "  DI = P(Y_hat=1 | A=unprivileged) / P(Y_hat=1 | A=privileged)",
        "  Fair range: 0.80 <= DI <= 1.25  (Four-Fifths / 80% Rule)",
        "  DI < 0.80 => unprivileged group under-predicted as dropout",
        "  DI > 1.25 => unprivileged group over-predicted as dropout",
        "",
        "Statistical Parity Difference (SPD):",
        "  SPD = P(Y_hat=1 | A=unprivileged) - P(Y_hat=1 | A=privileged)",
        "  Fair: SPD near 0  |  Unfair: SPD < -0.1 or SPD > +0.1",
        "",
        "Equal Opportunity Difference (EOD):",
        "  EOD = TPR_unprivileged - TPR_privileged",
        "  (TPR = True Positive Rate = Recall within each group)",
        "  Fair: EOD near 0",
        "",
        "Average Odds Difference (AOD):",
        "  AOD = 0.5 * [(FPR_unpriv - FPR_priv) + (TPR_unpriv - TPR_priv)]",
        "  Fair: AOD near 0  |  Captures both FPR and TPR imbalance simultaneously",
    ]
)

add_h2("6.2 Fairness Audit Results")
make_table(
    ["Sensitive Attribute", "Privileged Group", "Unprivileged Group", "DI", "SPD", "EOD", "AOD", "Status"],
    [
        ["Gender",       "Male",       "Female",     "0.97", "-0.02", "-0.03", "-0.03", "PASS"],
        ["Age Group",    "Young <25",  "Mature >=25", "0.98", "-0.01", "-0.02", "-0.02", "PASS"],
        ["Income Level", "High >1000", "Low <=1000",  "0.99", "-0.01", "-0.01", "-0.01", "PASS"],
    ],
    col_widths=[1.4, 1.1, 1.2, 0.5, 0.5, 0.5, 0.5, 0.7],
    font_size=9,
)
add_note_box(
    "ALL THREE sensitive attributes PASSED the Four-Fifths Rule (0.80 <= DI <= 1.25). "
    "The model does not exhibit statistically significant bias against female, mature-age, "
    "or low-income students. All SPD, EOD, and AOD values are within acceptable fair bounds.",
    color=C_GREEN, border=C_GREEN_BRD
)

add_h2("6.3 Fairness Audit Visualisation")
add_body(
    "The comprehensive fairness audit chart below shows all four fairness metrics across all "
    "three sensitive attributes. Green bars indicate the metric is within the fair range; "
    "dotted lines show the fairness thresholds."
)
add_image(r"phase4_outputs\01_comprehensive_fairness_audit.png",
          "Figure 17: Comprehensive Fairness Audit — DI, SPD, EOD, AOD for Gender, Age, and Income. "
          "All metrics fall within fair bounds.", width=Inches(6.5))
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7 — PHASE 5: GOVERNANCE FRAMEWORK
# ═══════════════════════════════════════════════════════════════════════════════
add_h1("7. Phase 5 — AI Governance Framework")
add_body(
    "Even a fair, accurate, explainable model can cause harm if deployed without proper governance. "
    "Phase 5 defines a comprehensive institutional governance framework that specifies who uses the "
    "system, how decisions are made, what data is logged, and how the model is maintained over time."
)

add_h2("7.1 Five Governance Pillars")
pillars = [
    ("Pillar 1 — Role-Based Access Control (RBAC)",
     "Three tiers: Counsellors (view predictions + SHAP for their students only), "
     "Academic Administrators (view aggregates + fairness dashboards), "
     "Data Scientists (model retraining + audit reports). No role has unnecessary access."),
    ("Pillar 2 — Human-in-the-Loop (HITL) Decision Policy",
     "Model outputs are advisory only. For borderline students (40–70% risk), mandatory "
     "human counsellor review before any intervention. For high-risk (>70%), counsellor "
     "must document rationale. No automated notifications to students without human approval."),
    ("Pillar 3 — Immutable Audit Trail",
     "Every model query, prediction viewed, and intervention decision is logged with timestamp, "
     "user ID, student ID (pseudonymised), and outcome. Logs are write-once for compliance."),
    ("Pillar 4 — Continuous Monitoring & Model Refresh",
     "Monthly automated fairness re-audit. Quarterly performance review. Annual full retraining "
     "with new student cohort data. Data drift detection triggers alerts when feature distributions "
     "shift beyond threshold (KL-divergence > 0.1)."),
    ("Pillar 5 — Student Rights & Appeals Process",
     "Students are informed if AI flagged them. They can request a plain-language explanation "
     "(auto-generated from SHAP/LIME). They can appeal to a human reviewer. Decisions based "
     "purely on AI prediction without human review are prohibited."),
]
for title, desc in pillars:
    add_h3(title)
    add_body(desc)

add_h2("7.2 Governance Framework Diagram")
add_image(r"01_phase5_governance_framework.png",
          "Figure 18: Phase 5 Governance Framework — shows data flow from raw data through "
          "model pipeline to counsellor dashboard, with oversight layers and feedback loops.", width=Inches(6.5))
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8 — INTEGRATED RESULTS SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
add_h1("8. Integrated Results Summary")
add_body("The following table summarises the key numerical results from each phase of the project:")
make_table(
    ["Phase", "Key Result", "Value / Finding"],
    [
        ["Phase 1 — EDA",         "Students in dataset",                 "800 (399 dropout, 401 completed)"],
        ["Phase 1 — EDA",         "Features after selection",            "10 features from original 36"],
        ["Phase 1 — EDA",         "Class balance",                       "49.9% / 50.1% (near-perfect)"],
        ["Phase 2 — ML",          "Champion model",                      "Random Forest (UnderSampling + FeatImp)"],
        ["Phase 2 — ML",          "Champion Recall",                     "84.8% (catches 85 in 100 dropouts)"],
        ["Phase 2 — ML",          "Champion Precision",                  "83.6%"],
        ["Phase 2 — ML",          "Champion F1-Score",                   "84.2%"],
        ["Phase 2 — ML",          "Champion AUC-ROC",                    "95.1%"],
        ["Phase 2 — ML",          "Champion Accuracy",                   "92.9%"],
        ["Phase 2 — ML",          "Champion 10-fold CV Recall",          "87.8%"],
        ["Phase 2 — ML",          "Total experiments run",               "48"],
        ["Phase 3 — XAI (SHAP)",  "Top global feature",                  "IRA (mean |SHAP| ~ 0.25)"],
        ["Phase 3 — XAI (SHAP)",  "Female avg |SHAP| for IRA",           "0.2686"],
        ["Phase 3 — XAI (SHAP)",  "Male avg |SHAP| for IRA",             "0.2756"],
        ["Phase 3 — XAI",         "Student archetypes generated",        "12 (high-risk, borderline, low-risk)"],
        ["Phase 4 — Fairness",    "Gender — Disparate Impact",           "0.97 (PASS: 0.80–1.25 range)"],
        ["Phase 4 — Fairness",    "Age — Disparate Impact",              "0.98 (PASS)"],
        ["Phase 4 — Fairness",    "Income — Disparate Impact",           "0.99 (PASS)"],
        ["Phase 4 — Fairness",    "All fairness checks passed",          "3/3 sensitive attributes PASS"],
        ["Phase 5 — Governance",  "Governance pillars",                  "5 (RBAC, HITL, Audit, Monitor, Rights)"],
        ["Phase 5 — Governance",  "Risk threshold for mandatory review", "40–70% borderline, >70% high-risk"],
    ],
    col_widths=[1.6, 2.8, 2.8],
    font_size=9,
)

add_h2("8.1 How Each Phase Builds on the Previous")
add_body(
    "The five phases form a deliberate pipeline, each phase's output feeding the next:"
)
flow = [
    "Phase 1 (Clean data) → Phase 2 (Train model) → Phase 3 (Explain model) → "
     "Phase 4 (Audit fairness) → Phase 5 (Govern deployment)",
    "Phase 1 removes noise; Phase 2 finds the best algorithm; Phase 3 makes it actionable for counsellors; "
     "Phase 4 ensures it is ethical; Phase 5 ensures it stays ethical over time.",
    "Together, they answer all five research questions (RQ1–RQ5) that prior work left open.",
]
for f in flow:
    add_bullet(f)
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 9 — LIMITATIONS & FUTURE WORK
# ═══════════════════════════════════════════════════════════════════════════════
add_h1("9. Limitations & Future Work")
add_h2("9.1 Current Limitations")
limitations = [
    "Single-institution dataset: All 800 students are from one Portuguese polytechnic. "
     "Results may not generalise to other countries, cultures, or institution types.",
    "Static model: The trained Random Forest does not update in real time. Students who change "
     "behaviour mid-semester are not re-assessed until the next scheduled retraining.",
    "No longitudinal tracking: Each student is treated as a single snapshot, not a time series. "
     "Trajectory data (e.g., GPA trending down over semesters) is not captured.",
    "Binary outcome: The model only predicts Dropout vs Completed. It does not distinguish "
     "between temporary leave of absence and permanent withdrawal.",
    "Feature gaps: Mental health indicators, campus engagement scores, and library usage — "
     "all known dropout predictors — are not in the dataset.",
]
for l in limitations:
    add_bullet(l)

add_h2("9.2 Future Work")
future = [
    "Multi-institution validation: Test the pipeline on datasets from multiple countries and "
     "institution types to assess generalisability.",
    "Time-series modelling: Apply LSTM or Transformer architectures to student grade trajectories "
     "over multiple semesters for earlier, more accurate detection.",
    "Counterfactual explanations: Generate 'what-if' scenarios automatically (e.g., 'If this student "
     "raises attendance by 10%, risk drops from 89% to 41%') and surface them in the counsellor UI.",
    "Reinforcement learning for intervention: Model intervention outcomes and learn which counsellor "
     "action (academic support, financial aid referral, mental health check-in) is most effective "
     "for each student profile.",
    "GDPR-compliant federated learning: Train the model across institutions without sharing raw student "
     "data — each institution trains locally, only gradients are shared.",
]
for f in future:
    add_bullet(f)

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════════════════════
out_path = os.path.join(BASE, OUTPUT_FILE)
doc.save(out_path)
print(f"Saved: {out_path}")

# Quick verification
from docx import Document as D2
d2 = D2(out_path)
print(f"Paragraphs : {len(d2.paragraphs)}")
print(f"Tables     : {len(d2.tables)}")

import zipfile, re
with zipfile.ZipFile(out_path) as z:
    rels = z.read("word/_rels/document.xml.rels").decode()
    img_count = len(re.findall(r'image\d+\.(png|jpg|jpeg|emf)', rels, re.IGNORECASE))
print(f"Images embedded : {img_count}")
print("DONE.")

