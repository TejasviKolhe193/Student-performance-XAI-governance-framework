import docx
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document('paper_review/research_paper_final_draft.docx')
full_text = '\n'.join([p.text for p in doc.paragraphs])
for t in doc.tables:
    for row in t.rows:
        for c in row.cells:
            full_text += ' ' + c.text

citations = set(re.findall(r'\[(\d+)\]', full_text))
print('Citations found in paper:', sorted([int(x) for x in citations]))

# Check for banned legacy words/numbers
banned = ['84.8%', '0.951', '3,017', '80/20', '12,067', '2,722', 'ira']
print('\nBanned legacy pattern check:')
for b in banned:
    matches = [(i, p.text) for i, p in enumerate(doc.paragraphs) if b in p.text]
    print(f'  Pattern "{b}": found {len(matches)} times')
    for idx, m in matches:
        print(f'    -> P{idx}: {m[:100]}...')

# Check presence of dev2 numbers
dev2_check = ['73.18%', '75.64%', '0.8968', '4,526', '10,558', '32.37%', '19.26%', '62.41%', '0.1080']
print('\nDev2 key metrics check:')
for d in dev2_check:
    matches = [(i, p.text) for i, p in enumerate(doc.paragraphs) if d in p.text]
    print(f'  Dev2 Metric "{d}": found {len(matches)} times')

