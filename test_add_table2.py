import docx
import shutil

shutil.copyfile("paper_review/research_paper_final_draft.docx", "paper_review/test_table2.docx")
doc = docx.Document("paper_review/test_table2.docx")

# Insert table after P54
p54 = doc.paragraphs[54]
# Add paragraph for Table II caption
caption_p = p54.insert_paragraph_before()
# Wait, insert_paragraph_before inserts before P54.
# In python-docx, to insert a table after a paragraph:
# we can use XML manipulation or insert before P55!
p55 = doc.paragraphs[55]
caption = p55.insert_paragraph_before("TABLE II. CONFUSION MATRIX (RF CHAMPION, N = 3,017)")
caption.style = doc.paragraphs[27].style # Table title style

table = doc.add_table(rows=3, cols=4)
table.style = doc.tables[0].style
# Move table before p55 in XML
p55._p.addprevious(table._tbl)

# Fill table
data = [
    ["", "Pred. Graduated", "Pred. Dropout", "Total"],
    ["Actual Graduated", "TN = 2,229", "FP = 112", "2,341"],
    ["Actual Dropout", "FN = 103", "TP = 573", "676"]
]
for r_idx, row in enumerate(data):
    for c_idx, val in enumerate(row):
        table.rows[r_idx].cells[c_idx].text = val
        # set small font
        for p in table.rows[r_idx].cells[c_idx].paragraphs:
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = docx.shared.Pt(8)

doc.save("paper_review/test_table2.docx")
print("Saved test_table2.docx")
