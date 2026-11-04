#!/usr/bin/env python3
"""
verify_compliance.py
Performs automated audit of the revised docx against all user requirements.
"""

import sys, re
from pathlib import Path
from docx import Document

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).parent
doc = Document(ROOT / "paper_review" / "research_paper_final_draft.docx")

failures = []
passes = []

def check(name, condition, msg=""):
    if condition:
        passes.append(f"[PASS] {name}")
    else:
        failures.append(f"[FAIL] {name}: {msg}")

# 1. GPA check: ONLY in Data Section
gpa_paras = []
for i, p in enumerate(doc.paragraphs):
    if "gpa" in p.text.lower() or "ira" in p.text.lower():
        gpa_paras.append((i, p.text))

check(
    "GPA occurrence count",
    len(gpa_paras) == 1,
    f"Found {len(gpa_paras)} paragraphs mentioning GPA/ira: {[idx for idx, _ in gpa_paras]}"
)
if gpa_paras:
    expected_sentence = "Cumulative GPA (ira) was excluded because it is computed over the full enrollment and would leak outcome information."
    check(
        "GPA exact sentence in Data Section",
        expected_sentence in gpa_paras[0][1],
        f"Data section does not contain exact required sentence: {gpa_paras[0][1][:100]}"
    )

# 2. Banned terms check
banned = [
    "leak-free",
    "early warning",
    "early identification",
    "early intervention",
    "eliminates target leakage",
    "eliminate target leakage",
    "eliminating target leakage",
    "digital access",
    "internet access",
    "SVM 91.4",
    "91.4% recall",
    "0.9506",
    "0.951",
    "0.707",
    "The priority is on gender",
    "home home computer ownership"
]

found_banned = []
for i, p in enumerate(doc.paragraphs):
    for b in banned:
        if b.lower() in p.text.lower():
            # Allow "early warning" only if in limitations explaining that the model CANNOT support early warning
            if b.lower() == "early warning" and "cannot support" in p.text.lower():
                continue
            found_banned.append((i, b, p.text[:80]))

check(
    "No banned terms",
    len(found_banned) == 0,
    f"Found banned terms: {found_banned}"
)

# 3. Locked numbers verification
text_all = "\n".join(p.text for p in doc.paragraphs)

check("15,084 records", "15,084" in text_all, "15,084 missing")
check("70/30 split", "70/30" in text_all, "70/30 split missing")
check("10,558 training", "10,558" in text_all, "10,558 missing")
check("4,526 test", "4,526" in text_all, "4,526 missing")
check("Recall 73.18%", "73.18%" in text_all, "73.18% missing")
check("Precision 75.64%", "75.64%" in text_all, "75.64% missing")
check("Accuracy 88.71%", "88.71%" in text_all, "88.71% missing")
check("ROC-AUC 0.8968", "0.8968" in text_all, "0.8968 missing")
check("Brier 0.1080", "0.1080" in text_all, "0.1080 missing")
check("Baseline Brier 0.1738", "0.1738" in text_all, "0.1738 missing")
check("Confusion TP 742", "742" in text_all, "TP 742 missing")
check("Confusion FP 239", "239" in text_all, "FP 239 missing")
check("Confusion TN 3,273", "3,273" in text_all, "TN 3,273 missing")
check("Confusion FN 272", "272" in text_all, "FN 272 missing")
check("SHAP course failures 32.37%", "32.37%" in text_all, "32.37% missing")
check("SHAP attendance 19.26%", "19.26%" in text_all, "19.26% missing")
check("SHAP cohort year 10.78%", "10.78%" in text_all, "10.78% missing")
check("SHAP top-3 62.41%", "62.41%" in text_all, "62.41% missing")
check("Gender attribution 3.66%", "3.66%" in text_all, "3.66% missing")
check("Gender DI 0.7383", "0.7383" in text_all, "0.7383 missing")
check("Female recall 70.87%", "70.87%" in text_all, "70.87% missing")
check("Male recall 75.09%", "75.09%" in text_all, "75.09% missing")
check("EOD -0.0422", "-0.0422" in text_all or "−0.0422" in text_all, "EOD -0.0422 missing")
check("Gender p=0.1354", "0.1354" in text_all, "0.1354 missing")
check("Income p=0.00043", "0.00043" in text_all, "0.00043 missing")
check("Home computer ownership p=0.00089", "0.00089" in text_all, "0.00089 missing")
check("Race raw p=0.0144", "0.0144" in text_all, "0.0144 missing")
check("Reweighing recall 60.36%", "60.36%" in text_all, "60.36% missing")
check("Reweighing precision 93.72%", "93.72%" in text_all, "93.72% missing")
check("Local archetype #815 (0.50)", "#815" in text_all and "0.50" in text_all, "Archetype #815 missing")
check("Local archetype #4078 (0.50)", "#4078" in text_all, "Archetype #4078 missing")
check("Local archetype #4458 (1.00)", "#4458" in text_all and "1.00" in text_all, "Archetype #4458 missing")
check("Alerts per 100 students (21.7)", "21.7" in text_all, "21.7 alerts missing")
check("True-to-false alert ratio (3.10:1)", "3.10:1" in text_all, "3.10:1 ratio missing")

# 4. Table I verification
t = doc.tables[0]
check("Table I row 9 updated", "[9]" in t.rows[9].cells[0].text and "Zughoul" in t.rows[9].cells[0].text, "Table I row 9 not updated")
check("Table I row 10 updated", "[10]" in t.rows[10].cells[0].text and "Wen" in t.rows[10].cells[0].text, "Table I row 10 not updated")
check("Table I row 11 updated", "[11]" in t.rows[11].cells[0].text and "Aziz" in t.rows[11].cells[0].text, "Table I row 11 not updated")

# 5. References verification
refs_text = "\n".join(p.text for p in doc.paragraphs[81:])
check("Ref [9] Zughoul", "Zughoul" in refs_text, "Ref [9] missing Zughoul")
check("Ref [10] Wen", "Wen" in refs_text, "Ref [10] missing Wen")
check("Ref [11] Aziz", "Aziz" in refs_text, "Ref [11] missing Aziz")
check("Ref [12] Lundberg & Lee", "Lundberg" in refs_text and "Lee" in refs_text, "Ref [12] missing Lundberg & Lee")

# 6. Proposed governance framing check
check("Governance proposed in Abstract", "proposed design, not field-tested" in doc.paragraphs[17].text, "Abstract missing proposed qualifier")
check("Governance proposed in Section IV-E", "Not Field-Tested" in doc.paragraphs[76].text, "Section IV-E missing proposed qualifier")
check("Governance proposed in Conclusion", "not been field-tested" in doc.paragraphs[78].text, "Conclusion missing proposed qualifier")

# 7. Print summary
print("=" * 60)
print(f"AUDIT SUMMARY: {len(passes)} Passed, {len(failures)} Failed")
print("=" * 60)
for p in passes:
    print(p)
if failures:
    print("\nFAILURES:")
    for f in failures:
        print(f)
    sys.exit(1)
else:
    print("\nALL COMPLIANCE CHECKS PASSED PERFECTLY!")
