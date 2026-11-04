import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import re

def set_cell_background(cell, hex_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_header(doc, title, subtitle):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(title)
    r.font.name = 'Calibri'
    r.font.size = Pt(20)
    r.font.bold = True
    r.font.color.rgb = RGBColor(24, 43, 73) # Navy
    p.paragraph_format.space_after = Pt(4)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run(subtitle)
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(90, 105, 120)
    p_sub.paragraph_format.space_after = Pt(18)

doc = docx.Document()

# Page setup: Standard Letter, 1 inch margins
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

add_header(doc, "Author Response & Point-by-Point Revision Sheet", 
           "Accompanying the Revised Manuscript for IEEE Conference Submission")

# Meta Callout Box
meta_table = doc.add_table(rows=4, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("Manuscript Title:", "An Explainable and Fairness-Audited AI Governance Framework for Student Dropout Prediction"),
    ("Base Benchmark:", "Silva et al., IEEE Revista Iberoamericana de Tecnologias del Aprendizaje (RITA), 2025"),
    ("Evaluation Cohort:", "15,084 Secondary Technical Students (IFNMG Administrative Database, 4 Modalities)"),
    ("Held-Out Test Vault:", "4,526 Unseen Students (70/30 Stratified Split; 1,014 Dropouts, 3,512 Completers; TP=742, FP=239, TN=3,273, FN=272)")
]

for idx, (label, val) in enumerate(meta_data):
    row = meta_table.rows[idx]
    
    c0 = row.cells[0]
    c0.width = Inches(1.8)
    p0 = c0.paragraphs[0]
    r0 = p0.add_run(label)
    r0.font.bold = True
    r0.font.name = 'Calibri'
    r0.font.size = Pt(10)
    r0.font.color.rgb = RGBColor(24, 43, 73)
    p0.paragraph_format.space_after = Pt(2)
    set_cell_background(c0, "F0F4F8")
    set_cell_margins(c0, 60, 60, 100, 100)
    
    c1 = row.cells[1]
    c1.width = Inches(4.7)
    p1 = c1.paragraphs[0]
    r1 = p1.add_run(val)
    r1.font.name = 'Calibri'
    r1.font.size = Pt(10)
    p1.paragraph_format.space_after = Pt(2)
    set_cell_background(c1, "F8FAFC")
    set_cell_margins(c1, 60, 60, 100, 100)

doc.add_paragraph().paragraph_format.space_after = Pt(12)

# Parse REVIEWER_RESPONSE_SHEET.md
with open("REVIEWER_RESPONSE_SHEET.md", "r", encoding="utf-8") as f:
    md_content = f.read()

# Helper to add stylized heading
def add_custom_heading(doc, text, level):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.bold = True
    if level == 1:
        r.font.size = Pt(15)
        r.font.color.rgb = RGBColor(24, 43, 73)
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
    elif level == 2:
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(40, 80, 130)
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
    elif level == 3:
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(60, 60, 60)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)

# Helper to format markdown text with bolding
def add_formatted_paragraph(doc, text, is_quote=False, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if is_quote:
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.right_indent = Inches(0.3)
    
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            r = p.add_run(part[2:-2])
            r.font.bold = True
            r.font.name = 'Calibri'
            r.font.size = Pt(10)
            if is_quote:
                r.font.color.rgb = RGBColor(50, 50, 50)
                r.font.italic = True
        else:
            subparts = re.split(r'(\*.*?\*)', part)
            for sub in subparts:
                if sub.startswith('*') and sub.endswith('*') and len(sub) > 2:
                    r = p.add_run(sub[1:-1])
                    r.font.italic = True
                    r.font.name = 'Calibri'
                    r.font.size = Pt(10)
                else:
                    r = p.add_run(sub)
                    r.font.name = 'Calibri'
                    r.font.size = Pt(10)
                    if is_quote:
                        r.font.color.rgb = RGBColor(50, 50, 50)
                        r.font.italic = True

# Read lines from MD
lines = md_content.split('\n')
i = 0
in_table = False
table_lines = []

while i < len(lines):
    line = lines[i].strip()
    
    # Skip front matter already rendered
    if line.startswith("# ") or line.startswith("**Manuscript Title:") or line.startswith("**Base Benchmark:") or line.startswith("**Evaluation Cohort:") or line.startswith("**Held-Out Test Vault:") or line == "---":
        i += 1
        continue
    
    if line.startswith("## "):
        add_custom_heading(doc, line[3:], 1)
        i += 1
        continue
    elif line.startswith("### "):
        add_custom_heading(doc, line[4:], 2)
        i += 1
        continue
    elif line.startswith("#### "):
        add_custom_heading(doc, line[5:], 3)
        i += 1
        continue
    
    # Check for Markdown tables
    if line.startswith("|") and line.endswith("|"):
        table_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
            table_lines.append(lines[i].strip())
            i += 1
        
        # Render table
        if len(table_lines) >= 3:
            # Parse header and rows
            header_cells = [c.strip() for c in table_lines[0].split("|")[1:-1]]
            rows_data = []
            for t_line in table_lines[2:]:
                cells = [c.strip() for c in t_line.split("|")[1:-1]]
                rows_data.append(cells)
            
            t = doc.add_table(rows=len(rows_data) + 1, cols=len(header_cells))
            t.alignment = WD_TABLE_ALIGNMENT.CENTER
            
            # Format header
            hdr_row = t.rows[0]
            for col_idx, h_text in enumerate(header_cells):
                cell = hdr_row.cells[col_idx]
                cell.text = h_text
                set_cell_background(cell, "2C3E50")
                set_cell_margins(cell, 80, 80, 120, 120)
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in p.runs:
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(255, 255, 255)
                    r.font.name = 'Calibri'
                    r.font.size = Pt(9.5)
            
            # Format data rows
            for r_idx, row_vals in enumerate(rows_data):
                row = t.rows[r_idx + 1]
                bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
                for c_idx, val in enumerate(row_vals):
                    if c_idx < len(row.cells):
                        cell = row.cells[c_idx]
                        cell.text = ""
                        p = cell.paragraphs[0]
                        p.paragraph_format.space_after = Pt(2)
                        p.paragraph_format.line_spacing = 1.1
                        set_cell_background(cell, bg_color)
                        set_cell_margins(cell, 60, 60, 100, 100)
                        
                        # Add formatted text
                        subparts = re.split(r'(\*\*.*?\*\*)', val)
                        for sp in subparts:
                            if sp.startswith('**') and sp.endswith('**'):
                                r = p.add_run(sp[2:-2])
                                r.font.bold = True
                            else:
                                r = p.add_run(sp)
                            r.font.name = 'Calibri'
                            r.font.size = Pt(9)
            
            doc.add_paragraph().paragraph_format.space_after = Pt(8)
        continue
    
    if line.startswith("> "):
        add_formatted_paragraph(doc, line[2:], is_quote=True)
    elif line:
        add_formatted_paragraph(doc, line)
    
    i += 1

out_path = "paper_review/REVIEWER_RESPONSE_SHEET.docx"
doc.save(out_path)
doc.save("REVIEWER_RESPONSE_SHEET.docx")
doc.save("paper_review/REVIEWER_RESPONSE_SHEET_TABULAR.docx")
doc.save("REVIEWER_RESPONSE_SHEET_TABULAR.docx")
print(f"Successfully generated {out_path}, REVIEWER_RESPONSE_SHEET.docx, and REVIEWER_RESPONSE_SHEET_TABULAR.docx")

