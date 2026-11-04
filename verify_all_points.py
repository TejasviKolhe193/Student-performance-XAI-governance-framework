import docx, sys
sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document('paper_review/research_paper_final_draft.docx')

checks = [
    ("1. Title", doc.paragraphs[0].text, "An Explainable and Fairness-Audited AI Governance Framework for Student Dropout Prediction" in doc.paragraphs[0].text),
    ("2. Abstract - Model & Metrics", doc.paragraphs[17].text, "84.8% recall" in doc.paragraphs[17].text and "83.6% precision" in doc.paragraphs[17].text and "TP=573" in doc.paragraphs[17].text),
    ("2. Abstract - Gender Disparity", doc.paragraphs[17].text, "disparate impact 0.707" in doc.paragraphs[17].text and "female recall 81.7%" in doc.paragraphs[17].text),
    ("2. Abstract - Governance Proposal", doc.paragraphs[17].text, "proposed five-pillar" in doc.paragraphs[17].text),
    ("3. Intro - Prediction Timing", doc.paragraphs[20].text + doc.paragraphs[22].text, "first-year" in (doc.paragraphs[20].text + doc.paragraphs[22].text) and "first academic year" in doc.paragraphs[20].text),
    ("3. Intro - Gap Operational Integration", doc.paragraphs[23].text, "operational integration" in doc.paragraphs[23].text),
    ("4. Literature Table I Gaps & Samples", " ".join([c.text for row in doc.tables[0].rows for c in row.cells]), "IFMA Brazil" in " ".join([c.text for row in doc.tables[0].rows for c in row.cells])),
    ("5. Dataset Attrition 48k to 15k", doc.paragraphs[32].text, "48,311" in doc.paragraphs[32].text and "36,273" in doc.paragraphs[32].text and "15,084" in doc.paragraphs[32].text and "11,703" in doc.paragraphs[32].text and "3,381" in doc.paragraphs[32].text),
    ("5. Active vs Post-mortem", doc.paragraphs[46].text, "2,722 active" in doc.paragraphs[46].text and "295 post-mortem" in doc.paragraphs[46].text),
    ("5. Attendance Cliff & Computer Access", doc.paragraphs[50].text, "88.7%" in doc.paragraphs[50].text and "home computer" in doc.paragraphs[50].text and "28.5%" in doc.paragraphs[50].text),
    ("6. CV 5-fold grid vs nested 10-fold", doc.paragraphs[33].text, "5-fold" in doc.paragraphs[33].text and "10-fold" in doc.paragraphs[33].text and "leakage" in doc.paragraphs[33].text),
    ("6. Utility Decision Rule", doc.paragraphs[35].text + doc.paragraphs[55].text, "precision >= 60.0%" in (doc.paragraphs[35].text + doc.paragraphs[55].text) and "ROC-AUC >= 0.90" in (doc.paragraphs[35].text + doc.paragraphs[55].text)),
    ("7. Confusion Matrix (Test Set N=3,017)", doc.paragraphs[54].text, "TP=573, FP=112, TN=2,229, FN=103" in doc.paragraphs[54].text and "22.7 alerts" in doc.paragraphs[54].text),
    ("7. Baselines (Majority & Attendance)", doc.paragraphs[55].text, "majority-class baseline yields 0.0%" in doc.paragraphs[55].text and "attendance-only heuristic" in doc.paragraphs[55].text),
    ("8. SVM Recall vs Precision collapse", doc.paragraphs[55].text, "91.4%" in doc.paragraphs[55].text and "23.1%" in doc.paragraphs[55].text and "AUC = 0.591" in doc.paragraphs[55].text and "2,050 false alarms" in doc.paragraphs[55].text),
    ("9. TreeSHAP Attribution Shares 71.3%", doc.paragraphs[57].text, "52.8%" in doc.paragraphs[57].text and "10.4%" in doc.paragraphs[57].text and "8.1%" in doc.paragraphs[57].text and "71.3%" in doc.paragraphs[57].text),
    ("9. SHAP-LIME Concordance (0.724)", doc.paragraphs[62].text, "0.724" in doc.paragraphs[62].text and "Jaccard" in doc.paragraphs[62].text),
    ("10. Gender Disparity & Group Counts", doc.paragraphs[70].text, "DI = 0.707" in doc.paragraphs[70].text and "254/311" in doc.paragraphs[70].text and "319/365" in doc.paragraphs[70].text and "19.00%" in doc.paragraphs[70].text and "26.89%" in doc.paragraphs[70].text),
    ("10. Mitigation Trade-off (AIF360 vs Post-hoc)", doc.paragraphs[71].text, "AIF360 Reweighing" in doc.paragraphs[71].text and "tau=0.44" in doc.paragraphs[71].text),
    ("10. Structural Proxy Check (Age AUC=0.892)", doc.paragraphs[65].text, "0.892" in doc.paragraphs[65].text and "structural proxy" in doc.paragraphs[65].text),
    ("10. Non-discriminatory DI > 1.25 clarification", doc.paragraphs[65].text, "reflects elevated empirical dropout" in doc.paragraphs[65].text),
    ("11. Brier Calibration & Risk Tiers", doc.paragraphs[75].text, "Brier score of 0.0526" in doc.paragraphs[75].text and "Safe (<0.40" in doc.paragraphs[75].text and "Watchlist (0.40-0.70" in doc.paragraphs[75].text and "Urgent Intervention (>0.70" in doc.paragraphs[75].text),
    ("11. Proposed 5 Governance Pillars", doc.paragraphs[76].text, "five proposed governance policy pillars" in doc.paragraphs[76].text),
    ("12. Limitations & Future Work", doc.paragraphs[80].text, "single multi-campus institution" in doc.paragraphs[80].text and "retrospective" in doc.paragraphs[80].text),
    ("14. Duplicate Gender Paragraph Removed", doc.paragraphs[73].text, doc.paragraphs[73].text.strip() == ""),
    ("14. Repaired References [9] & [10]", doc.paragraphs[90].text + doc.paragraphs[91].text, "Zhang and S. Yang" in doc.paragraphs[90].text and "L. Zhou" in doc.paragraphs[91].text)
]

print(f"{'CHECK ITEM':<48} | {'STATUS'}")
print("-" * 60)
all_pass = True
for name, sample, passed in checks:
    status = "PASS" if passed else "FAIL"
    if not passed: all_pass = False
    print(f"{name:<48} | {status}")

print("-" * 60)
print(f"OVERALL RESULT: {'ALL PASS' if all_pass else 'FAILURES DETECTED'}")

