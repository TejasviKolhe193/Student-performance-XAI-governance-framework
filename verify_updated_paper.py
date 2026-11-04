import docx, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
doc = docx.Document("paper_review/research_paper_final_draft.docx")

print(f"Total paragraphs: {len(doc.paragraphs)}")
print(f"Total tables: {len(doc.tables)}")
print(f"Total sections: {len(doc.sections)}")

words_p = sum(len(p.text.split()) for p in doc.paragraphs)
words_t = sum(len(c.text.split()) for t in doc.tables for row in t.rows for c in row.cells)
print(f"Total word count: {words_p + words_t} words (Body + Tables)")

# Check specific priority register fixes
print("\n--- PRIORITY REGISTER VERIFICATION ---")
print("1. Title:", doc.paragraphs[0].text[:70])
print("2. Prediction timing in Abstract:", "operational first-year early-warning" in doc.paragraphs[17].text)
print("3. Multi-objective rule in Methods:", "Maximize Recall subject to Precision" in doc.paragraphs[36].text)
print("4. Confusion matrix in Results:", "TP = 573, FP = 112, TN = 2,229, and FN = 103" in doc.paragraphs[55].text)
print("5. Nested CV in Methods:", "5-fold cross-validation on training folds only" in doc.paragraphs[35].text)
print("6. Dataset attrition in Methods:", "48,311" in doc.paragraphs[32].text and "15,084" in doc.paragraphs[32].text)
print("7. SHAP-LIME agreement corrected:", "0.724" in doc.paragraphs[63].text)
print("8. Gender disparity investigated:", "DI = 0.7066" in doc.paragraphs[65].text and "EOD = -0.0573" in doc.paragraphs[65].text)
print("9. Fairness interpretation updated:", "reflect real-world socioeconomic headwinds" in doc.paragraphs[70].text)
print("10. Digital access standardized:", "home laptop" in doc.paragraphs[40].text or "laptop" in doc.paragraphs[40].text)
print("11. Governance labeled as proposal:", "Proposed Institutional Governance Policy Framework" in doc.paragraphs[42].text)
print("12. SVM AUC completed:", "0.5910" in doc.paragraphs[55].text)
print("13. Risk score calibration reported:", "Brier score was 0.0526" in doc.paragraphs[55].text)
print("14. Repeated text removed:", doc.paragraphs[73].text.strip() == "")
print("15. Reference [9] cleaned:", "2022Y" not in doc.paragraphs[90].text)
print("16. Reference [10] cleaned:", "[10] L. Zhou" not in doc.paragraphs[91].text and "L. Zhou" in doc.paragraphs[91].text)
print("17. Total citations preserved:", len([p for p in doc.paragraphs[82:] if p.text.strip()]))

