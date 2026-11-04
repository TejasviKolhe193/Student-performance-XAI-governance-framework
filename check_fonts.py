import docx, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
doc = docx.Document('paper_review/research_paper_final_draft.docx')

sample_indices = [0, 4, 17, 18, 19, 25, 26, 27, 28, 30, 43, 81, 82]
for idx in sample_indices:
    p = doc.paragraphs[idx]
    font_name = p.runs[0].font.name if p.runs and p.runs[0].font.name else 'inherit'
    font_size = p.runs[0].font.size.pt if p.runs and p.runs[0].font.size else 'inherit'
    bold = p.runs[0].font.bold if p.runs else False
    print(f"P{idx} style='{p.style.name}': font={font_name}, size={font_size}, bold={bold} | text='{p.text[:40]}'")

