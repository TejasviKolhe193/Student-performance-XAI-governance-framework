import docx, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
doc = docx.Document('paper_review/research_paper_final_draft.docx')

print(f"Total sections: {len(doc.sections)}")
for i, s in enumerate(doc.sections):
    print(f"\n--- Section {i} ---")
    print(f"Start type: {s.start_type}")
    print(f"Page width: {s.page_width.inches}, Height: {s.page_height.inches}")
    print(f"Margins (in): Top={s.top_margin.inches}, Bottom={s.bottom_margin.inches}, Left={s.left_margin.inches}, Right={s.right_margin.inches}")
    cols = s._sectPr.xpath('./w:cols')
    if cols:
        num = cols[0].get(docx.oxml.ns.qn('w:num'))
        space = cols[0].get(docx.oxml.ns.qn('w:space'))
        print(f"Columns: num={num}, space={space}")
    else:
        print("Columns: default 1")

# Check which paragraphs belong to which section
print("\n--- SECTION PARAGRAPH DISTRIBUTION ---")
# In python-docx, paragraphs don't directly reference section, but sectPr occurs inside paragraph properties or document body
for i, p in enumerate(doc.paragraphs):
    sectPr = p._p.xpath('./w:pPr/w:sectPr')
    if sectPr:
        print(f"Section break after P{i}: text='{p.text[:40]}'")

