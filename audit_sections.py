import docx, sys
sys.stdout.reconfigure(encoding='utf-8')

rev_doc = docx.Document('paper_review/AI Governance Review Suggestions.docx')
paper_doc = docx.Document('paper_review/research_paper_final_draft.docx')

paper_full_text = "\n".join([f"P{i:03d}: {p.text}" for i, p in enumerate(paper_doc.paragraphs)])

print("=== AUDIT OF ALL 14 REVIEW SECTIONS ===")

# Group review points
sections = {}
curr_sec = "Intro"
sections[curr_sec] = []

for i, p in enumerate(rev_doc.paragraphs):
    t = p.text.strip()
    if not t:
        continue
    if any(t.startswith(f"{n}. ") for n in range(1, 16)):
        curr_sec = t
        sections[curr_sec] = []
    else:
        sections[curr_sec].append(t)

for sec, points in sections.items():
    print(f"\n==========================================")
    print(f"SECTION: {sec}")
    print(f"==========================================")
    for pt in points:
        print(f"• REVIEW POINT: {pt}")

