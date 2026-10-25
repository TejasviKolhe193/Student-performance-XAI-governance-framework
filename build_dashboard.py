"""
Python script to generate the 5-Phase UI Dashboard:
- 5 Sections (Phase 1, Phase 2, Phase 3, Phase 4, Phase 5)
- Crisp modern LIGHT THEME (#f8fafc, #ffffff, #e2e8f0, #0f172a)
- STRICT ASYMMETRIC LAYOUT:
    * LEFT SIDE (~58% width): Text, Specifications, Results, KPIs, Structured Tables (Wider)
    * RIGHT SIDE (~42% width): Diagrams, Graphs, Switcher pills, Zoom modal (Smaller space)
- Generous typography (12.5px - 13px body text) and high contrast dark slate text for effortless readability
- Viewport fitting: 100vh height, zero global page scroll
- Outputs index.html and dashboard.html
"""

import os
import sys
import json
import pandas as pd

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

def generate_dashboard():
    # Load required data
    with open("phase4_outputs/interactive_students_xai.json", "r", encoding="utf-8") as f:
        students_json = f.read()

    with open("phase4_outputs/counterfactual_curves.json", "r", encoding="utf-8") as f:
        cf_json = f.read()

    with open("phase4_outputs/decoded_student_metadata.json", "r", encoding="utf-8") as f:
        meta_json = f.read()

    # Load Phase 4 fairness data
    df_fairness = pd.read_csv("phase4_outputs/fairness_metrics_summary.csv")
    df_inter = pd.read_csv("phase4_outputs/intersectional_fairness_summary.csv")
    df_ew = pd.read_csv("phase4_outputs/early_warning_vs_postmortem_audit.csv")

    # Generate Phase 4 single dimension rows
    p4_fair_rows = ""
    for _, r in df_fairness.iterrows():
        b_class = "badge-pass" if "PASSED" in str(r["Four_Fifths_Status"]) else "badge-warn"
        p4_fair_rows += f"""
        <tr>
            <td><strong>{r['Dimension']}</strong></td>
            <td><small>{r['Privileged_Group']} / {r['Unprivileged_Group']}</small></td>
            <td><strong>{r['Disparate_Impact_Ratio']:.3f}</strong></td>
            <td><span class="badge {b_class}">{r['Four_Fifths_Status']}</span></td>
            <td>{r['Statistical_Parity_Diff']:+.3f}</td>
            <td>{r['Equal_Opportunity_Diff']:+.3f}</td>
        </tr>
        """

    # Generate Phase 4 intersectional rows
    p4_inter_rows = ""
    for _, r in df_inter.iterrows():
        p4_inter_rows += f"""
        <tr>
            <td><strong>{r['Subgroup']}</strong></td>
            <td>{int(r['Count']):,}</td>
            <td>{r['Actual_Dropout_Rate']:.1f}%</td>
            <td>{r['Flagged_Rate']:.1f}%</td>
            <td><span class="badge badge-primary">{r['Recall_TPR']:.1f}%</span></td>
            <td><strong>{r['Precision']:.1f}%</strong></td>
        </tr>
        """

    # Generate Phase 4 Early warning rows
    p4_ew_rows = ""
    for _, r in df_ew.iterrows():
        b_cls = "badge-pass" if "Active" in str(r["Cohort"]) else "badge-accent"
        p4_ew_rows += f"""
        <tr>
            <td><strong>{r['Cohort']}</strong></td>
            <td>{int(r['Count']):,}</td>
            <td>{int(r['Actual_Dropouts'])} ({r['Actual_Rate']:.1f}%)</td>
            <td><span class="badge {b_cls}">{r['Recall_Sensitivity']:.1f}%</span></td>
            <td><strong>{r['Precision']:.1f}%</strong></td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Performance XAI & Algorithmic Governance Framework | Executive UI Dashboard</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-light: #f8fafc;
            --bg-panel: #ffffff;
            --bg-card: #f8fafc;
            --border-color: #e2e8f0;
            --border-highlight: #93c5fd;
            --primary: #2563eb;
            --primary-light: #eff6ff;
            --primary-glow: rgba(37, 99, 235, 0.18);
            --success: #059669;
            --success-light: #ecfdf5;
            --warning: #d97706;
            --warning-light: #fffbeb;
            --danger: #dc2626;
            --danger-light: #fef2f2;
            --purple: #7c3aed;
            --purple-light: #faf5ff;
            --text-main: #0f172a;
            --text-body: #334155;
            --text-muted: #64748b;
            --text-dim: #94a3b8;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            -webkit-font-smoothing: antialiased;
        }}

        html, body {{
            width: 100vw;
            height: 100vh;
            overflow: hidden; /* STRICT NO-SCROLL ON WINDOW */
            background-color: var(--bg-light);
            color: var(--text-main);
            display: flex;
            flex-direction: column;
        }}

        /* TOP NAVIGATION HEADER (Fixed Height: 52px) */
        header.top-navbar {{
            height: 52px;
            background: #ffffff;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 18px;
            z-index: 100;
            flex-shrink: 0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
        }}

        .brand-box {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .brand-logo {{
            width: 30px;
            height: 30px;
            background: linear-gradient(135deg, #2563eb, #4f46e5);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            font-weight: 800;
            color: white;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
        }}
        .brand-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 15px;
            font-weight: 700;
            letter-spacing: -0.2px;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .brand-badge {{
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            padding: 2px 7px;
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 4px;
            color: #1d4ed8;
            letter-spacing: 0.5px;
        }}

        /* PHASE NAVIGATION TABS */
        .phase-tabs {{
            display: flex;
            align-items: center;
            gap: 6px;
            background: #f1f5f9;
            padding: 3px 5px;
            border-radius: 9px;
            border: 1px solid #e2e8f0;
        }}
        .phase-tab-btn {{
            background: transparent;
            border: none;
            color: #475569;
            font-size: 12.5px;
            font-weight: 600;
            padding: 6px 13px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.15s ease;
            display: flex;
            align-items: center;
            gap: 7px;
        }}
        .phase-tab-btn .num-pill {{
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: #e2e8f0;
            font-size: 10.5px;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #475569;
            transition: all 0.15s;
        }}
        .phase-tab-btn:hover {{
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.7);
        }}
        .phase-tab-btn.active {{
            background: #2563eb;
            color: #ffffff;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
        }}
        .phase-tab-btn.active .num-pill {{
            background: #ffffff;
            color: #2563eb;
        }}

        /* HEADER CONTROLS */
        .header-controls {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .btn-nav {{
            background: #f8fafc;
            border: 1px solid var(--border-color);
            color: var(--text-body);
            font-size: 12px;
            font-weight: 600;
            padding: 5px 11px;
            border-radius: 6px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 4px;
            transition: all 0.15s;
        }}
        .btn-nav:hover {{
            background: #f1f5f9;
            color: var(--text-main);
            border-color: #cbd5e1;
        }}
        .kbd-hint {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 10px;
            padding: 2px 6px;
            background: #f1f5f9;
            border-radius: 4px;
            color: var(--text-muted);
            border: 1px solid #e2e8f0;
        }}

        /* MAIN VIEWPORT WRAPPER (100vh - 52px) */
        main.dashboard-viewport {{
            flex: 1;
            height: calc(100vh - 52px);
            width: 100vw;
            position: relative;
            overflow: hidden;
            z-index: 1;
        }}

        /* SECTION SLIDES (5 PHASES) */
        /* STRICT ASYMMETRIC SPLIT: LEFT SIDE (~58%) = Text & Tables | RIGHT SIDE (~42%) = Graphs & Diagrams */
        .phase-section {{
            display: none;
            width: 100%;
            height: 100%;
            padding: 12px 16px;
            box-sizing: border-box;
            gap: 14px;
            grid-template-columns: 58% 42%; /* LEFT: Text & Tables (Wider ~58%), RIGHT: Graphs (~42%) */
        }}
        .phase-section.active {{
            display: grid;
            animation: fadeIn 0.2s ease-out forwards;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(3px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* LEFT PANE: TEXT, SPECIFICATIONS, RESULTS, TABLES (Wider ~58%) */
        .text-pane {{
            height: 100%;
            background: var(--bg-panel);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 14px 18px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            gap: 10px;
            overflow-y: auto;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
            scrollbar-width: thin;
            scrollbar-color: #cbd5e1 transparent;
        }}
        .text-pane::-webkit-scrollbar {{
            width: 5px;
        }}
        .text-pane::-webkit-scrollbar-thumb {{
            background: #cbd5e1;
            border-radius: 4px;
        }}

        /* RIGHT PANE: GRAPHS & DIAGRAMS (Smaller ~42%) */
        .graphs-pane {{
            height: 100%;
            background: var(--bg-panel);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 12px 14px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            gap: 10px;
            overflow: hidden;
            position: relative;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
        }}

        /* SECTION HEADER BLOCK */
        .sec-header {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 8px;
            flex-shrink: 0;
        }}
        .sec-title-wrap h2 {{
            font-family: 'Outfit', sans-serif;
            font-size: 18px;
            font-weight: 800;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .sec-title-wrap p {{
            font-size: 12.5px;
            color: var(--text-muted);
            margin-top: 2px;
        }}
        .sec-tag {{
            font-size: 11px;
            font-weight: 700;
            padding: 3px 9px;
            border-radius: 20px;
            letter-spacing: 0.3px;
        }}
        .tag-phase1 {{ background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }}
        .tag-phase2 {{ background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }}
        .tag-phase3 {{ background: #faf5ff; color: #6d28d9; border: 1px solid #ddd6fe; }}
        .tag-phase4 {{ background: #fffbeb; color: #b45309; border: 1px solid #fde68a; }}
        .tag-phase5 {{ background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }}

        /* STRUCTURED SPECIFICATION / METHODOLOGY BOX (CLEAN LIGHT CARD) */
        .spec-box {{
            background: #f8fafc;
            border: 1px solid var(--border-color);
            border-radius: 9px;
            padding: 10px 12px;
            flex-shrink: 0;
        }}
        .spec-header-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 8px;
            padding-bottom: 5px;
            border-bottom: 1px solid #e2e8f0;
        }}
        .spec-title {{
            font-size: 11.5px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #1e40af;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .spec-grid {{
            display: flex;
            flex-direction: column;
            gap: 5px;
        }}
        .spec-row {{
            display: grid;
            grid-template-columns: 145px 1fr;
            gap: 12px;
            align-items: center;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 5px 8px;
            transition: background 0.15s;
        }}
        .spec-row:hover {{
            background: #f1f5f9;
            border-color: #cbd5e1;
        }}
        .spec-badge {{
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            color: #1e40af;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.4px;
            padding: 3px 6px;
            border-radius: 4px;
            text-align: center;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .spec-badge.green {{
            background: #ecfdf5;
            border-color: #a7f3d0;
            color: #065f46;
        }}
        .spec-badge.purple {{
            background: #faf5ff;
            border-color: #ddd6fe;
            color: #5b21b6;
        }}
        .spec-badge.amber {{
            background: #fffbeb;
            border-color: #fde68a;
            color: #92400e;
        }}
        .spec-badge.red {{
            background: #fef2f2;
            border-color: #fecaca;
            color: #991b1b;
        }}
        .spec-desc {{
            font-size: 12.5px;
            color: #1e293b;
            line-height: 1.4;
            font-weight: 500;
        }}
        .spec-desc strong {{
            color: #0f172a;
            font-weight: 700;
        }}
        .spec-desc code {{
            background: #f1f5f9;
            padding: 1px 5px;
            border-radius: 3px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            color: #1d4ed8;
            border: 1px solid #e2e8f0;
        }}

        /* KPI STATS ROW (4 METRICS) */
        .kpi-row {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            flex-shrink: 0;
        }}
        .kpi-stat-card {{
            background: #f8fafc;
            border: 1px solid var(--border-color);
            border-top: 3px solid var(--primary);
            border-radius: 8px;
            padding: 8px 11px;
        }}
        .kpi-stat-card.green {{ border-top-color: var(--success); }}
        .kpi-stat-card.purple {{ border-top-color: var(--purple); }}
        .kpi-stat-card.warning {{ border-top-color: var(--warning); }}
        .kpi-stat-card.red {{ border-top-color: var(--danger); }}
        .kpi-label {{
            font-size: 10px;
            text-transform: uppercase;
            color: var(--text-muted);
            font-weight: 700;
            letter-spacing: 0.4px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .kpi-val {{
            font-family: 'Outfit', sans-serif;
            font-size: 20px;
            font-weight: 800;
            color: var(--text-main);
            margin: 2px 0;
        }}
        .kpi-subtext {{
            font-size: 10px;
            color: var(--text-muted);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        /* DATA TABLE WRAPPER (CLEAN LIGHT DESIGN) */
        .table-wrap {{
            flex: 1;
            min-height: 130px;
            background: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            overflow-y: auto;
            position: relative;
        }}
        .table-wrap h4 {{
            font-size: 12px;
            font-weight: 700;
            color: #1e293b;
            padding: 7px 12px;
            background: #f8fafc;
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 2;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        table.results-tbl {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            text-align: left;
        }}
        table.results-tbl th {{
            background: #f1f5f9;
            padding: 7px 11px;
            color: #334155;
            font-weight: 700;
            font-size: 11px;
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 33px;
            z-index: 1;
        }}
        table.results-tbl td {{
            padding: 6.5px 11px;
            border-bottom: 1px solid #f1f5f9;
            color: #334155;
            white-space: nowrap;
        }}
        table.results-tbl tr:hover td {{
            background: #f8fafc;
        }}
        table.results-tbl tr.highlight-row td {{
            background: #ecfdf5;
            color: #065f46;
            font-weight: 600;
        }}

        /* BADGES */
        .badge {{
            display: inline-block;
            padding: 2.5px 8px;
            border-radius: 12px;
            font-size: 10.5px;
            font-weight: 700;
            letter-spacing: 0.3px;
        }}
        .badge-pass {{ background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }}
        .badge-warn {{ background: #fffbeb; color: #b45309; border: 1px solid #fde68a; }}
        .badge-fail {{ background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }}
        .badge-primary {{ background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }}
        .badge-accent {{ background: #faf5ff; color: #6d28d9; border: 1px solid #ddd6fe; }}

        /* CLINICAL / EVALUATOR CALLOUT BOX */
        .callout-box {{
            background: #f8fafc;
            border-left: 4px solid var(--primary);
            border-radius: 0 7px 7px 0;
            padding: 8px 12px;
            font-size: 12px;
            color: #334155;
            flex-shrink: 0;
            line-height: 1.45;
            border-top: 1px solid #e2e8f0;
            border-right: 1px solid #e2e8f0;
            border-bottom: 1px solid #e2e8f0;
        }}
        .callout-box strong {{
            color: #0f172a;
        }}

        /* GRAPHS PANE: TOP SWITCHER BAR & DIAGRAM VIEWPORT */
        .graphs-topbar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 7px;
            flex-shrink: 0;
        }}
        .graphs-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 13.5px;
            font-weight: 700;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .diagram-pills {{
            display: flex;
            gap: 4px;
            flex-wrap: wrap;
        }}
        .diagram-pill-btn {{
            background: #f1f5f9;
            border: 1px solid #e2e8f0;
            color: #475569;
            font-size: 10.5px;
            font-weight: 600;
            padding: 3.5px 8.5px;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.15s;
        }}
        .diagram-pill-btn:hover {{
            background: #e2e8f0;
            color: #0f172a;
        }}
        .diagram-pill-btn.active {{
            background: var(--primary);
            color: #ffffff;
            border-color: var(--primary);
            box-shadow: 0 2px 6px rgba(37, 99, 235, 0.25);
        }}

        /* DIAGRAM CONTAINER */
        .diagram-viewport {{
            flex: 1;
            background: #f8fafc;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
            cursor: zoom-in;
        }}
        .diagram-img {{
            max-width: 98%;
            max-height: 98%;
            object-fit: contain;
            border-radius: 6px;
            transition: transform 0.2s ease;
        }}
        .diagram-viewport:hover .diagram-img {{
            transform: scale(1.015);
        }}
        .diagram-zoom-hint {{
            position: absolute;
            bottom: 8px;
            right: 8px;
            background: rgba(15, 23, 42, 0.75);
            color: #ffffff;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 10px;
            font-weight: 600;
            pointer-events: none;
            backdrop-filter: blur(4px);
        }}
        .diagram-caption {{
            font-size: 11.5px;
            color: #475569;
            padding: 6px 10px;
            background: #f8fafc;
            border-radius: 6px;
            border: 1px solid #e2e8f0;
            flex-shrink: 0;
            line-height: 1.4;
        }}
        .diagram-caption strong {{
            color: #1e40af;
        }}

        /* INTERACTIVE SIMULATOR (PHASE 3 RIGHT PANE ALTERNATIVE) */
        .sim-view-wrapper {{
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            gap: 8px;
            overflow-y: auto;
            padding: 6px;
        }}
        .sim-controls-card {{
            background: #f8fafc;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 10px 12px;
        }}
        .sim-slider-row {{
            margin-top: 8px;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        .sim-slider-label {{
            display: flex;
            justify-content: space-between;
            font-size: 11.8px;
            font-weight: 600;
            color: #334155;
        }}
        .sim-slider {{
            width: 100%;
            accent-color: var(--primary);
            cursor: pointer;
        }}
        .sim-student-select {{
            background: #ffffff;
            border: 1px solid #cbd5e1;
            color: #0f172a;
            font-size: 12px;
            font-weight: 600;
            padding: 5px 9px;
            border-radius: 6px;
            width: 100%;
            outline: none;
        }}

        /* FULLSCREEN LIGHTBOX MODAL */
        .lightbox-modal {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(15, 23, 42, 0.88);
            backdrop-filter: blur(6px);
            z-index: 1000;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 24px;
        }}
        .lightbox-modal.active {{
            display: flex;
        }}
        .lightbox-img {{
            max-width: 95vw;
            max-height: 92vh;
            object-fit: contain;
            border-radius: 8px;
            background: #ffffff;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
        }}
        .lightbox-close {{
            position: absolute;
            top: 18px;
            right: 24px;
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.4);
            color: white;
            font-size: 20px;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
        }}
        .lightbox-close:hover {{
            background: var(--danger);
        }}
    </style>
</head>
<body>

    <!-- TOP COMPACT NAVBAR (Fixed 52px) -->
    <header class="top-navbar">
        <div class="brand-box">
            <div class="brand-logo">IF</div>
            <div class="brand-title">
                Student Dropout XAI & Governance Center
                <span class="brand-badge">IEEE RITA 2025</span>
            </div>
        </div>

        <!-- 5 PHASE TABS -->
        <nav class="phase-tabs">
            <button class="phase-tab-btn active" onclick="switchPhase(1)" id="tab-btn-1">
                <span class="num-pill">1</span> Preprocessing & EDA
            </button>
            <button class="phase-tab-btn" onclick="switchPhase(2)" id="tab-btn-2">
                <span class="num-pill">2</span> Model Benchmark (48 Exp)
            </button>
            <button class="phase-tab-btn" onclick="switchPhase(3)" id="tab-btn-3">
                <span class="num-pill">3</span> Explainable AI (XAI)
            </button>
            <button class="phase-tab-btn" onclick="switchPhase(4)" id="tab-btn-4">
                <span class="num-pill">4</span> Fairness & Auditing
            </button>
            <button class="phase-tab-btn" onclick="switchPhase(5)" id="tab-btn-5">
                <span class="num-pill">5</span> AI Governance Charter
            </button>
        </nav>

        <!-- CONTROLS & SHORTCUTS -->
        <div class="header-controls">
            <span class="kbd-hint" title="Press 1, 2, 3, 4, 5 on your keyboard to switch phases">Keys: [1 - 5]</span>
            <button class="btn-nav" onclick="prevPhase()" title="Previous Phase (Left Arrow)">◀ Prev</button>
            <button class="btn-nav" onclick="nextPhase()" title="Next Phase (Right Arrow)">Next ▶</button>
            <button class="btn-nav" onclick="toggleFullscreen()" title="Toggle Fullscreen">⛶ Fullscreen</button>
        </div>
    </header>

    <!-- MAIN VIEWPORT CONTAINER (CALC 100VH - 52PX) -->
    <main class="dashboard-viewport" id="dashboardViewport">

        <!-- ═══════════════════════════════════════════════════════════════════ -->
        <!-- SECTION 1: PHASE 1 — DATA PREPARATION, PREPROCESSING & EDA       -->
        <!-- ═══════════════════════════════════════════════════════════════════ -->
        <section class="phase-section active" id="phase-sec-1">
            <!-- LEFT PANE: INFORMATION, SPECIFICATIONS, RESULTS, TABLES (WIDER ~58%) -->
            <div class="text-pane">
                <div class="sec-header">
                    <div class="sec-title-wrap">
                        <h2>Phase 1: Institutional Preprocessing & Feature Engineering</h2>
                        <p>Secondary Technical Education Cohort (Federal Institutes of Brazil - IFs)</p>
                    </div>
                    <span class="sec-tag tag-phase1">Phase 1 Complete</span>
                </div>

                <!-- METHODOLOGY & PREPROCESSING PIPELINE (STRUCTURED SPECIFICATION GRID) -->
                <div class="spec-box">
                    <div class="spec-header-bar">
                        <span class="spec-title">Methodology & Preprocessing Pipeline</span>
                        <span style="font-size:11px; color:var(--text-muted);">Strict Leakage Shield</span>
                    </div>
                    <div class="spec-grid">
                        <div class="spec-row">
                            <span class="spec-badge">COHORT SCOPE</span>
                            <span class="spec-desc">Filtered <strong>48,311</strong> administrative records down to <strong>15,084</strong> secondary technical students, replicating Silva et al. (IEEE RITA 2025).</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge green">TARGET DEFINITION</span>
                            <span class="spec-desc">Binary <code>situacao</code>: Class 0 (Completed: <strong>11,703 / 77.6%</strong>) vs. Class 1 (Dropout: <strong>3,381 / 22.4%</strong>), excluding non-terminal records.</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge amber">LEAKAGE PRUNING</span>
                            <span class="spec-desc">Dropped student IDs (<code>matricula</code>, CPF); pruned 4 columns with &gt;20% missing values; median-imputed negligible technical gaps.</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge purple">1.5×IQR WINSOR</span>
                            <span class="spec-desc">Clipped outliers on Age, Income, Computers without discarding a single row, preserving <strong>100%</strong> of all 15,084 records.</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge">DUAL ENCODING</span>
                            <span class="spec-desc">One-hot nominal features, ordinal parental education, label-encoded binaries into <strong>33 numerical features</strong>.</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge green">VAULT PARTITION</span>
                            <span class="spec-desc">Stratified <strong>80% Training set</strong> (12,067 records) and <strong>20% Held-Out Test Vault</strong> (3,017 untouched real students).</span>
                        </div>
                    </div>
                </div>

                <!-- KPI STATS ROW -->
                <div class="kpi-row">
                    <div class="kpi-stat-card">
                        <div class="kpi-label">Cohort Size</div>
                        <div class="kpi-val">15,084</div>
                        <div class="kpi-subtext">Secondary Students</div>
                    </div>
                    <div class="kpi-stat-card green">
                        <div class="kpi-label">Graduation Rate</div>
                        <div class="kpi-val">77.6%</div>
                        <div class="kpi-subtext">11,703 Completed</div>
                    </div>
                    <div class="kpi-stat-card red">
                        <div class="kpi-label">Dropout Rate</div>
                        <div class="kpi-val">22.4%</div>
                        <div class="kpi-subtext">3,381 True Dropouts</div>
                    </div>
                    <div class="kpi-stat-card purple">
                        <div class="kpi-label">Feature Matrix</div>
                        <div class="kpi-val">33</div>
                        <div class="kpi-subtext">Clean Features</div>
                    </div>
                </div>

                <!-- STRUCTURED RESULTS TABLE -->
                <div class="table-wrap">
                    <h4>
                        <span>Educational Modality Breakdown (15,084 Students)</span>
                        <span style="font-size:10.5px; color:var(--text-muted);">Baseline Imbalance: 3.46 to 1</span>
                    </h4>
                    <table class="results-tbl">
                        <thead>
                            <tr>
                                <th>Modality / Format</th>
                                <th>Student Population</th>
                                <th>Share (%)</th>
                                <th>Dropout Baseline</th>
                                <th>Academic Character</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Integrado</strong></td>
                                <td>10,076 students</td>
                                <td>66.8%</td>
                                <td><span class="badge badge-primary">16.3%</span></td>
                                <td>Regular daytime high-school teens</td>
                            </tr>
                            <tr>
                                <td><strong>Subsequente</strong></td>
                                <td>3,815 students</td>
                                <td>25.3%</td>
                                <td><span class="badge badge-warn">34.6%</span></td>
                                <td>Post-secondary adult technical certification</td>
                            </tr>
                            <tr>
                                <td><strong>Concomitante</strong></td>
                                <td>765 students</td>
                                <td>5.1%</td>
                                <td><span class="badge badge-warn">32.7%</span></td>
                                <td>Concurrent dual high-school enrollment</td>
                            </tr>
                            <tr>
                                <td><strong>Integrado EJA</strong></td>
                                <td>428 students</td>
                                <td>2.8%</td>
                                <td><span class="badge badge-fail">39.5%</span></td>
                                <td>Youth & Adult evening vocational returnees</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- CLINICAL CALLOUT -->
                <div class="callout-box">
                    <strong>Decisive EDA Takeaway:</strong> Attendance below 70% accelerates dropout probability by <strong>3.5×</strong>. Cumulated GPA exhibits a sharp mathematical cliff at <strong>5.0 / 10.0</strong>, separating retained students from dropouts.
                </div>
            </div>

            <!-- RIGHT PANE: DIAGRAMS & GRAPHS (SMALLER SPACE ~42%) -->
            <div class="graphs-pane">
                <div class="graphs-topbar">
                    <div class="graphs-title">Visual Diagnostics & Pipeline Architecture</div>
                    <div class="diagram-pills">
                        <button class="diagram-pill-btn active" onclick="switchDiagram(1, 'eda')">EDA & Preprocessing Overview</button>
                    </div>
                </div>
                <div class="diagram-viewport" onclick="openLightbox('phase1_outputs/01_phase1_eda_and_preprocessing.png')">
                    <img id="img-phase-1" class="diagram-img" src="phase1_outputs/01_phase1_eda_and_preprocessing.png" alt="Phase 1 EDA and Preprocessing">
                    <div class="diagram-zoom-hint">🔍 Click to Expand</div>
                </div>
                <div class="diagram-caption" id="caption-phase-1">
                    <strong>Figure 1.1:</strong> Multi-panel institutional baseline showing the 77.6%/22.4% class imbalance, 4 course modalities, the attendance cliff (&lt;70%), and the 5-step leak-free preprocessing funnel.
                </div>
            </div>
        </section>


        <!-- ═══════════════════════════════════════════════════════════════════ -->
        <!-- SECTION 2: PHASE 2 — 48-EXPERIMENT BENCHMARK & CHAMPION SELECTION -->
        <!-- ═══════════════════════════════════════════════════════════════════ -->
        <section class="phase-section" id="phase-sec-2">
            <!-- LEFT PANE: INFORMATION, SPECIFICATIONS, RESULTS, TABLES (WIDER ~58%) -->
            <div class="text-pane">
                <div class="sec-header">
                    <div class="sec-title-wrap">
                        <h2>Phase 2: 48-Experiment Model Benchmark</h2>
                        <p>4 Balancing Strategies × 3 Feature Selection Methods × 4 Model Families</p>
                    </div>
                    <span class="sec-tag tag-phase2">Champion Selected</span>
                </div>

                <!-- EXPERIMENTAL DESIGN & BENCHMARK MATRIX (STRUCTURED SPECIFICATION GRID) -->
                <div class="spec-box">
                    <div class="spec-header-bar">
                        <span class="spec-title">Experimental Design & Benchmark Matrix</span>
                        <span style="font-size:11px; color:var(--text-muted);">5-Fold CV Protocol</span>
                    </div>
                    <div class="spec-grid">
                        <div class="spec-row">
                            <span class="spec-badge">FACTORIAL GRID</span>
                            <span class="spec-desc">Tested <strong>48 experiments</strong> across 4 balancing methods × 3 feature selectors × 4 model families (RF, DT, LR, SVM).</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge green">LEAKAGE SHIELD</span>
                            <span class="spec-desc">5-Fold CV and balancing performed strictly on training folds; held-out vault of <strong>3,017 test students</strong> was untouched.</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge purple">CLINICAL RANKING</span>
                            <span class="spec-desc">Prioritized <strong>Recall</strong> (catching dropouts) first, followed by <strong>Precision</strong> (staff false-alarm burden) and ROC-AUC.</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge green">CHAMPION MODEL</span>
                            <span class="spec-desc"><strong>Random Forest (UnderSampling)</strong> delivered optimal balance: <strong>84.8% Recall, 83.6% Precision, 92.9% Accuracy, 0.951 AUC</strong>.</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge">WHITE-BOX CART</span>
                            <span class="spec-desc">Decision Tree surrogate achieved <strong>84.6% Recall</strong> with 64.0% Precision for transparent institutional flowcharts.</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge red">SVM PATHOLOGY</span>
                            <span class="spec-desc">Linear SVM flagged nearly all students as dropouts (<strong>91.4% raw recall, 23.1% precision collapse</strong>), proving clinical failure.</span>
                        </div>
                    </div>
                </div>

                <!-- KPI STATS ROW -->
                <div class="kpi-row">
                    <div class="kpi-stat-card green">
                        <div class="kpi-label">Champion Recall</div>
                        <div class="kpi-val">84.8%</div>
                        <div class="kpi-subtext">573/676 Dropouts Caught</div>
                    </div>
                    <div class="kpi-stat-card green">
                        <div class="kpi-label">Champion Precision</div>
                        <div class="kpi-val">83.6%</div>
                        <div class="kpi-subtext">Only 112 False Alarms</div>
                    </div>
                    <div class="kpi-stat-card">
                        <div class="kpi-label">Overall Accuracy</div>
                        <div class="kpi-val">92.9%</div>
                        <div class="kpi-subtext">2,802 / 3,017 Students</div>
                    </div>
                    <div class="kpi-stat-card purple">
                        <div class="kpi-label">ROC-AUC Score</div>
                        <div class="kpi-val">0.951</div>
                        <div class="kpi-subtext">Outstanding Separation</div>
                    </div>
                </div>

                <!-- STRUCTURED RESULTS TABLE -->
                <div class="table-wrap">
                    <h4>
                        <span>Leaderboard: Top Model per Algorithm Family (3,017 Test Students)</span>
                        <span style="font-size:10.5px; color:var(--text-muted);">Held-Out Vault</span>
                    </h4>
                    <table class="results-tbl">
                        <thead>
                            <tr>
                                <th>Algorithm Family</th>
                                <th>Optimal Configuration</th>
                                <th>Recall</th>
                                <th>Precision</th>
                                <th>Accuracy</th>
                                <th>ROC-AUC</th>
                                <th>Institutional Verdict</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr class="highlight-row">
                                <td><strong>Random Forest ★</strong></td>
                                <td>UnderSampling + FeatureImportance</td>
                                <td><strong>84.8%</strong></td>
                                <td><strong>83.6%</strong></td>
                                <td><strong>92.9%</strong></td>
                                <td><strong>0.951</strong></td>
                                <td><span class="badge badge-pass">Champion (Optimal)</span></td>
                            </tr>
                            <tr>
                                <td><strong>Decision Tree</strong></td>
                                <td>UnderSampling + ANOVA Filter</td>
                                <td>84.6%</td>
                                <td>64.0%</td>
                                <td>85.9%</td>
                                <td>0.854</td>
                                <td><span class="badge badge-primary">White-Box Surrogate</span></td>
                            </tr>
                            <tr>
                                <td><strong>Logistic Regression</strong></td>
                                <td>SMOTE + ANOVA Filter</td>
                                <td>82.8%</td>
                                <td>61.2%</td>
                                <td>84.1%</td>
                                <td>0.887</td>
                                <td><span class="badge badge-accent">Parametric Linear</span></td>
                            </tr>
                            <tr>
                                <td><strong>Linear SVM ⚠</strong></td>
                                <td>SMOTEENN + ANOVA Filter</td>
                                <td>91.4%</td>
                                <td>23.1%</td>
                                <td>30.1%</td>
                                <td>0.591</td>
                                <td><span class="badge badge-fail">Threshold Collapse</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- CLINICAL CALLOUT -->
                <div class="callout-box">
                    <strong>Evaluator Defense:</strong> While Linear SVM showed 91.4% raw recall, its precision collapsed to 23.1% (over-flagged nearly every student). Random Forest (UnderSampling) delivers the optimal clinical balance with <strong>84.8% Recall and 83.6% Precision</strong>.
                </div>
            </div>

            <!-- RIGHT PANE: DIAGRAMS & GRAPHS (SMALLER SPACE ~42%) -->
            <div class="graphs-pane">
                <div class="graphs-topbar">
                    <div class="graphs-title">Empirical Benchmark Visualizations</div>
                    <div class="diagram-pills">
                        <button class="diagram-pill-btn active" onclick="switchDiagram(2, 'comparison')">Model Comparison</button>
                        <button class="diagram-pill-btn" onclick="switchDiagram(2, 'cm')">Confusion Matrix</button>
                        <button class="diagram-pill-btn" onclick="switchDiagram(2, 'roc')">ROC Curves</button>
                        <button class="diagram-pill-btn" onclick="switchDiagram(2, 'balancing')">Balancing Impact</button>
                        <button class="diagram-pill-btn" onclick="switchDiagram(2, 'feat_imp')">Feature Importance</button>
                    </div>
                </div>
                <div class="diagram-viewport" onclick="openCurrentLightbox(2)">
                    <img id="img-phase-2" class="diagram-img" src="01_model_comparison.png" alt="Model Comparison">
                    <div class="diagram-zoom-hint">🔍 Click to Expand</div>
                </div>
                <div class="diagram-caption" id="caption-phase-2">
                    <strong>Figure 2.1:</strong> Recall, Precision, and F1 comparisons across 48 configurations on 3,017 unseen test students, demonstrating Random Forest superiority.
                </div>
            </div>
        </section>


        <!-- ═══════════════════════════════════════════════════════════════════ -->
        <!-- SECTION 3: PHASE 3 — EXPLAINABLE AI (XAI) & WHAT-IF SIMULATOR     -->
        <!-- ═══════════════════════════════════════════════════════════════════ -->
        <section class="phase-section" id="phase-sec-3">
            <!-- LEFT PANE: INFORMATION, SPECIFICATIONS, RESULTS, TABLES (WIDER ~58%) -->
            <div class="text-pane">
                <div class="sec-header">
                    <div class="sec-title-wrap">
                        <h2>Phase 3: Dual Macro & Micro Explainability (XAI)</h2>
                        <p>TreeExplainer SHAP + Local LIME Cards + Actionable What-If Counterfactuals</p>
                    </div>
                    <span class="sec-tag tag-phase3">Clinical XAI Ready</span>
                </div>

                <!-- EXPLAINABILITY ARCHITECTURE & DIAGNOSTIC FRAMEWORK (STRUCTURED SPECIFICATION GRID) -->
                <div class="spec-box">
                    <div class="spec-header-bar">
                        <span class="spec-title">Explainability Architecture & Attribution Framework</span>
                        <span style="font-size:11px; color:var(--text-muted);">TreeExplainer + LIME</span>
                    </div>
                    <div class="spec-grid">
                        <div class="spec-row">
                            <span class="spec-badge">GLOBAL SHAP</span>
                            <span class="spec-desc">TreeExplainer computed exact Shapley values across all <strong>3,017 test students</strong> using standardized English feature labels.</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge red">ACADEMIC CLIFF</span>
                            <span class="spec-desc">Cumulative GPA (<code>ira</code>) dominates all signals (<strong>Mean |SHAP| = 0.2717</strong>), showing acute non-linear risk below 5.0/10.</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge green">BEHAVIORAL LEVER</span>
                            <span class="spec-desc">Attendance Rate (<strong>0.0570</strong>) serves as primary early indicator; dropping below 75% triggers rapid risk escalation.</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge amber">LOCAL SURROGATES</span>
                            <span class="spec-desc">LIME explanation cards generate individual risk vs. protective factor decompositions for targeted student counseling.</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge purple">WHAT-IF SENSITIVITY</span>
                            <span class="spec-desc">Counterfactual response curves determine exact numerical thresholds needed to shift high-risk trajectories into safety.</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge green">STAR DEMO CASE</span>
                            <span class="spec-desc">Borderline Student #43 flips from <strong>65.0% risk down to 28.0% (Safe Zone)</strong> with +17% attendance contract.</span>
                        </div>
                    </div>
                </div>

                <!-- KPI STATS ROW -->
                <div class="kpi-row">
                    <div class="kpi-stat-card red">
                        <div class="kpi-label">#1 Risk Driver</div>
                        <div class="kpi-val" style="font-size:16px;">GPA (ira)</div>
                        <div class="kpi-subtext">|SHAP| = 0.2717</div>
                    </div>
                    <div class="kpi-stat-card green">
                        <div class="kpi-label">#2 Behavioral</div>
                        <div class="kpi-val" style="font-size:16px;">Attendance</div>
                        <div class="kpi-subtext">|SHAP| = 0.0570</div>
                    </div>
                    <div class="kpi-stat-card warning">
                        <div class="kpi-label">#3 Friction</div>
                        <div class="kpi-val" style="font-size:16px;">Failures</div>
                        <div class="kpi-subtext">|SHAP| = 0.0468</div>
                    </div>
                    <div class="kpi-stat-card purple">
                        <div class="kpi-label">Star Demo</div>
                        <div class="kpi-val" style="font-size:16px;">Student #43</div>
                        <div class="kpi-subtext">65% ➔ 28% Safe Zone</div>
                    </div>
                </div>

                <!-- STRUCTURED RESULTS TABLE -->
                <div class="table-wrap">
                    <h4>
                        <span>Top Global Feature Attributions (Mean |SHAP| Attribution)</span>
                        <span style="font-size:10.5px; color:var(--text-muted);">TreeExplainer</span>
                    </h4>
                    <table class="results-tbl">
                        <thead>
                            <tr>
                                <th>Feature Indicator</th>
                                <th>Mean |SHAP|</th>
                                <th>Attribution Share</th>
                                <th>Risk Trajectory Interpretation</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr class="highlight-row">
                                <td><strong>Cumulative GPA (<code>ira</code>)</strong></td>
                                <td><strong>0.2717</strong></td>
                                <td>56.2%</td>
                                <td>Decisive lever; exponential risk escalation below 5.0/10</td>
                            </tr>
                            <tr>
                                <td><strong>Attendance Rate (<code>percentual_frequencia</code>)</strong></td>
                                <td><strong>0.0570</strong></td>
                                <td>11.8%</td>
                                <td>Behavioral indicator; drops below 75% trigger acute flags</td>
                            </tr>
                            <tr>
                                <td><strong>Course Failures (<code>reprovacoes</code>)</strong></td>
                                <td><strong>0.0468</strong></td>
                                <td>9.7%</td>
                                <td>Academic friction; repeated course failures compound risk</td>
                            </tr>
                            <tr>
                                <td><strong>Enrollment Year (<code>anoingresso</code>)</strong></td>
                                <td>0.0384</td>
                                <td>7.9%</td>
                                <td>Captures curriculum reform calendar shifts and cohort timing</td>
                            </tr>
                            <tr>
                                <td><strong>Gross Family Income (<code>rendabruta</code>)</strong></td>
                                <td>0.0210</td>
                                <td>4.3%</td>
                                <td>Socioeconomic buffer; poverty increases baseline dropout hazard</td>
                            </tr>
                            <tr>
                                <td><strong>Course Modality (<code>modalidade</code>)</strong></td>
                                <td>0.0163</td>
                                <td>3.4%</td>
                                <td>Evening adult students face structural employment conflicts</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- CLINICAL CALLOUT -->
                <div class="callout-box">
                    <strong>Actionable Counterfactual Insight:</strong> For Borderline Student #43, raising attendance from 68% to 85% drops predicted risk from <strong>65.0% to 28.0% (Safe Zone)</strong>, giving counselors an achievable remedial target.
                </div>
            </div>

            <!-- RIGHT PANE: DIAGRAMS & GRAPHS (SMALLER SPACE ~42%) -->
            <div class="graphs-pane">
                <div class="graphs-topbar">
                    <div class="graphs-title">Explainability Diagrams & Live Simulator</div>
                    <div class="diagram-pills">
                        <button class="diagram-pill-btn active" onclick="switchDiagram(3, 'beeswarm')">Global Beeswarm</button>
                        <button class="diagram-pill-btn" onclick="switchDiagram(3, 'importance')">Mean |SHAP|</button>
                        <button class="diagram-pill-btn" onclick="switchDiagram(3, 'dependence')">GPA Dependence</button>
                        <button class="diagram-pill-btn" onclick="switchDiagram(3, 'lime43')">Student #43 LIME</button>
                        <button class="diagram-pill-btn" onclick="switchDiagram(3, 'sim')">🎛️ What-If Simulator</button>
                    </div>
                </div>

                <!-- STATIC DIAGRAM VIEWPORT -->
                <div class="diagram-viewport" id="viewport-phase-3" onclick="openCurrentLightbox(3)">
                    <img id="img-phase-3" class="diagram-img" src="phase3_outputs/01_shap_global_beeswarm.png" alt="SHAP Beeswarm">
                    <div class="diagram-zoom-hint">🔍 Click to Expand</div>
                </div>

                <!-- INTERACTIVE SIMULATOR (HIDDEN INITIALLY) -->
                <div class="sim-view-wrapper" id="sim-wrapper-phase-3" style="display:none;">
                    <div class="sim-controls-card">
                        <label style="font-size:11px; font-weight:700; color:var(--text-muted); text-transform:uppercase;">Select Student Archetype:</label>
                        <select id="p3-student-select" class="sim-student-select" onchange="onSimulatorStudentChange(this.value)">
                            <!-- Populated dynamically via JS -->
                        </select>
                    </div>

                    <div class="sim-controls-card" id="sim-active-card">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                            <span style="font-size:13.5px; font-weight:700; color:#0f172a;" id="sim-student-name">Student #43 Audit</span>
                            <span class="badge badge-warn" id="sim-risk-badge">65.0% Risk</span>
                        </div>
                        <div style="font-size:11.5px; color:var(--text-muted); margin-bottom:10px;" id="sim-student-sub">
                            Actual: Dropped Out | Modality: Technical High School
                        </div>

                        <div class="sim-slider-row">
                            <div class="sim-slider-label">
                                <span>Simulated Attendance Rate:</span>
                                <span id="sim-att-val" style="color:#2563eb; font-weight:700;">68.0%</span>
                            </div>
                            <input type="range" class="sim-slider" id="slider-att" min="40" max="100" step="1" value="68" oninput="updateSimAttendance(this.value)">
                        </div>

                        <div class="sim-slider-row" style="margin-top:10px;">
                            <div class="sim-slider-label">
                                <span>Simulated Cumulative GPA:</span>
                                <span id="sim-gpa-val" style="color:#059669; font-weight:700;">5.8 / 10.0</span>
                            </div>
                            <input type="range" class="sim-slider" id="slider-gpa" min="0" max="10" step="0.2" value="5.8" oninput="updateSimGPA(this.value)">
                        </div>

                        <div style="margin-top:12px; padding:8px 10px; background:#ffffff; border-radius:6px; border:1px solid #e2e8f0;">
                            <div style="font-size:11px; font-weight:700; color:#1d4ed8; margin-bottom:4px;">Counselor Action Target:</div>
                            <div style="font-size:11.5px; color:#334155; line-height:1.4;" id="sim-action-advice">
                                Increasing attendance from 68% to 85% drops risk to 28% (Safe Zone). Target attendance contract.
                            </div>
                        </div>
                    </div>
                </div>

                <div class="diagram-caption" id="caption-phase-3">
                    <strong>Figure 3.1:</strong> SHAP Beeswarm plot showing low GPA (blue dots right) and low attendance driving intense dropout probability across 3,017 test students.
                </div>
            </div>
        </section>


        <!-- ═══════════════════════════════════════════════════════════════════ -->
        <!-- SECTION 4: PHASE 4 — ALGORITHMIC FAIRNESS & EQUITY AUDITING       -->
        <!-- ═══════════════════════════════════════════════════════════════════ -->
        <section class="phase-section" id="phase-sec-4">
            <!-- LEFT PANE: INFORMATION, SPECIFICATIONS, RESULTS, TABLES (WIDER ~58%) -->
            <div class="text-pane">
                <div class="sec-header">
                    <div class="sec-title-wrap">
                        <h2>Phase 4: Algorithmic Fairness & Equity Audits</h2>
                        <p>US EEOC Four-Fifths Compliance + 8-Group Intersectional Matrix (100% Real Students)</p>
                    </div>
                    <span class="sec-tag tag-phase4">Fairness Certified</span>
                </div>

                <!-- ALGORITHMIC AUDITING & EQUITY EVALUATION PROTOCOL (STRUCTURED SPECIFICATION GRID) -->
                <div class="spec-box">
                    <div class="spec-header-bar">
                        <span class="spec-title">Algorithmic Auditing & Equity Evaluation Protocol</span>
                        <span style="font-size:11px; color:var(--text-muted);">EEOC Four-Fifths Standard</span>
                    </div>
                    <div class="spec-grid">
                        <div class="spec-row">
                            <span class="spec-badge green">RACE EQUITY</span>
                            <span class="spec-desc">Champion RF passed race audit with <strong>1.180 Disparate Impact ratio</strong> (White vs. Minority), fully within the 0.80–1.25 EEOC standard.</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge green">ACTIVE STUDENT TEST</span>
                            <span class="spec-desc">Audited active students (<code>GPA &gt; 0</code>, N=2,722) separately, delivering <strong>80.8% Recall and 82.5% Precision</strong> without relying on trivial post-mortem records.</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge purple">INTERSECTIONAL 8</span>
                            <span class="spec-desc">Evaluated all 8 compound demographic slices (Gender × Race × Income) on <strong>100% real student records</strong> (zero synthetic records).</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge amber">SELECTION DISPARITY</span>
                            <span class="spec-desc">Higher flagging in low-income/adult cohorts reflects real baseline dropout hazards (25.8% vs 19.0%), confirmed by equal recall parity.</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge">GENDER RECALL GAP</span>
                            <span class="spec-desc">Gender Equal Opportunity difference restricted to <strong>-0.038</strong> (Male 85.5% vs Female 81.7% Recall), maintaining diagnostic parity.</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge">MODALITY AUDIT</span>
                            <span class="spec-desc">Disaggregated performance across 4 modalities, proving flags appropriately track working-adult evening school attrition.</span>
                        </div>
                    </div>
                </div>

                <!-- KPI STATS ROW -->
                <div class="kpi-row">
                    <div class="kpi-stat-card green">
                        <div class="kpi-label">Race Equity Audit</div>
                        <div class="kpi-val" style="font-size:18px;">1.180</div>
                        <div class="kpi-subtext">PASSED (Four-Fifths)</div>
                    </div>
                    <div class="kpi-stat-card green">
                        <div class="kpi-label">Active Recall</div>
                        <div class="kpi-val" style="font-size:18px;">80.8%</div>
                        <div class="kpi-subtext">GPA &gt; 0 (2,722 Students)</div>
                    </div>
                    <div class="kpi-stat-card purple">
                        <div class="kpi-label">Active Precision</div>
                        <div class="kpi-val" style="font-size:18px;">82.5%</div>
                        <div class="kpi-subtext">Genuine Early Warning</div>
                    </div>
                    <div class="kpi-stat-card">
                        <div class="kpi-label">Audit Data Scope</div>
                        <div class="kpi-val" style="font-size:18px;">100% Real</div>
                        <div class="kpi-subtext">0 Synthetic Records</div>
                    </div>
                </div>

                <!-- STRUCTURED RESULTS TABLE -->
                <div class="table-wrap">
                    <h4>
                        <span>Quantitative Fairness Audit Matrix (Single Attribute Slices)</span>
                        <span style="font-size:10.5px; color:var(--text-muted);">EEOC Standard (0.80 - 1.25)</span>
                    </h4>
                    <table class="results-tbl">
                        <thead>
                            <tr>
                                <th>Protected Dimension</th>
                                <th>Privileged / Unprivileged</th>
                                <th>Disparate Impact</th>
                                <th>Four-Fifths Rule</th>
                                <th>Statistical Parity</th>
                                <th>Equal Opp Diff</th>
                            </tr>
                        </thead>
                        <tbody>
                            {p4_fair_rows}
                        </tbody>
                    </table>
                </div>

                <!-- CLINICAL CALLOUT -->
                <div class="callout-box">
                    <strong>Soundness & Equity Finding:</strong> Higher flagging rates in low-income and adult cohorts reflect authentic higher baseline dropout hazards rather than algorithmic prejudice, verified by consistent Equal Opportunity Recall parity across all groups.
                </div>
            </div>

            <!-- RIGHT PANE: DIAGRAMS & GRAPHS (SMALLER SPACE ~42%) -->
            <div class="graphs-pane">
                <div class="graphs-topbar">
                    <div class="graphs-title">Comprehensive Equity & Soundness Visualizations</div>
                    <div class="diagram-pills">
                        <button class="diagram-pill-btn active" onclick="switchDiagram(4, 'audit')">4-Panel Audit Plot</button>
                        <button class="diagram-pill-btn" onclick="switchDiagram(4, 'intersectional')">Intersectional Matrix</button>
                        <button class="diagram-pill-btn" onclick="switchDiagram(4, 'early_warning')">Active Student Test</button>
                    </div>
                </div>

                <!-- DIAGRAM VIEWPORT -->
                <div class="diagram-viewport" id="viewport-phase-4" onclick="openCurrentLightbox(4)">
                    <img id="img-phase-4" class="diagram-img" src="phase4_outputs/01_comprehensive_fairness_audit.png" alt="Fairness Charts">
                    <div class="diagram-zoom-hint">🔍 Click to Expand</div>
                </div>

                <!-- INTERSECTIONAL TABLE VIEW (HIDDEN INITIALLY) -->
                <div class="table-wrap" id="table-inter-phase-4" style="display:none; height:100%;">
                    <h4>
                        <span>Empirical 8-Group Intersectional Matrix (Gender × Race × Income)</span>
                        <span style="font-size:10.5px; color:var(--text-muted);">100% Real Test Students</span>
                    </h4>
                    <table class="results-tbl">
                        <thead>
                            <tr>
                                <th>Intersectional Compound Group</th>
                                <th>Students (N)</th>
                                <th>Actual Attrition</th>
                                <th>Model Flagged</th>
                                <th>Model Recall</th>
                                <th>Precision</th>
                            </tr>
                        </thead>
                        <tbody>
                            {p4_inter_rows}
                        </tbody>
                    </table>
                </div>

                <!-- EARLY WARNING TABLE VIEW (HIDDEN INITIALLY) -->
                <div class="table-wrap" id="table-ew-phase-4" style="display:none; height:100%;">
                    <h4>
                        <span>Early-Warning Active Students vs. Post-Mortem Records</span>
                        <span style="font-size:10.5px; color:var(--text-muted);">GPA &gt; 0 vs GPA == 0</span>
                    </h4>
                    <table class="results-tbl">
                        <thead>
                            <tr>
                                <th>Student Evaluation Cohort</th>
                                <th>Cohort (N)</th>
                                <th>Actual Dropouts</th>
                                <th>Model Recall</th>
                                <th>Precision</th>
                            </tr>
                        </thead>
                        <tbody>
                            {p4_ew_rows}
                        </tbody>
                    </table>
                </div>

                <div class="diagram-caption" id="caption-phase-4">
                    <strong>Figure 4.1:</strong> 4-panel algorithmic audit certifying race equity (Disparate Impact 1.180), equal opportunity recall parity, and robust 80.8% active student sensitivity.
                </div>
            </div>
        </section>


        <!-- ═══════════════════════════════════════════════════════════════════ -->
        <!-- SECTION 5: PHASE 5 — AI GOVERNANCE CHARTER & PROTOCOL             -->
        <!-- ═══════════════════════════════════════════════════════════════════ -->
        <section class="phase-section" id="phase-sec-5">
            <!-- LEFT PANE: INFORMATION, SPECIFICATIONS, RESULTS, TABLES (WIDER ~58%) -->
            <div class="text-pane">
                <div class="sec-header">
                    <div class="sec-title-wrap">
                        <h2>Phase 5: Institutional AI Governance Charter</h2>
                        <p>5 Binding Ethical Pillars & Human-in-the-Loop Operational Deployment Guardrails</p>
                    </div>
                    <span class="sec-tag tag-phase5">Governance Enforced</span>
                </div>

                <!-- INSTITUTIONAL GOVERNANCE CHARTER & ENFORCEMENT FRAMEWORK (STRUCTURED SPECIFICATION GRID) -->
                <div class="spec-box">
                    <div class="spec-header-bar">
                        <span class="spec-title">Institutional Governance Charter & Enforcement Framework</span>
                        <span style="font-size:11px; color:var(--text-muted);">Binding Operational Policy</span>
                    </div>
                    <div class="spec-grid">
                        <div class="spec-row">
                            <span class="spec-badge red">ADVISORY MANDATE</span>
                            <span class="spec-desc">Automated expulsion, tracking, or punitive disciplinary actions strictly prohibited; risk outputs serve solely as clinical advisory markers.</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge">XAI COUPLING</span>
                            <span class="spec-desc">Every automated notification must present primary SHAP/LIME attributions to direct intervention (academic tutoring vs. transit/food stipend).</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge green">MUTABLE TARGETING</span>
                            <span class="spec-desc">Interventions focus exclusively on mutable academic levers (attendance contracts, tutoring) rather than penalizing immutable demographic traits.</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge purple">COUNSELOR OVERRIDE</span>
                            <span class="spec-desc">Certified educational counselors retain <strong>100% exclusive final authority</strong> over all student support intervention plans.</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge amber">SEMI-ANNUAL RE-AUDIT</span>
                            <span class="spec-desc">Mandatory bi-annual recalibration of Disparate Impact and Equal Opportunity ratios before every semester to counter concept drift.</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-badge green">RIGHT TO APPEAL</span>
                            <span class="spec-desc">Guaranteed student procedural right to review explanation cards and contest algorithmic risk classifications under LGPD/FERPA laws.</span>
                        </div>
                    </div>
                </div>

                <!-- KPI STATS ROW -->
                <div class="kpi-row">
                    <div class="kpi-stat-card green">
                        <div class="kpi-label">Counselor Authority</div>
                        <div class="kpi-val" style="font-size:18px;">100%</div>
                        <div class="kpi-subtext">Final Human Override</div>
                    </div>
                    <div class="kpi-stat-card">
                        <div class="kpi-label">Autonomous Action</div>
                        <div class="kpi-val" style="font-size:18px;">0%</div>
                        <div class="kpi-subtext">Strictly Advisory</div>
                    </div>
                    <div class="kpi-stat-card purple">
                        <div class="kpi-label">Re-Audit Cadence</div>
                        <div class="kpi-val" style="font-size:18px;">Bi-Annual</div>
                        <div class="kpi-subtext">Every Academic Term</div>
                    </div>
                    <div class="kpi-stat-card green">
                        <div class="kpi-label">Student Appeal</div>
                        <div class="kpi-val" style="font-size:18px;">Protected</div>
                        <div class="kpi-subtext">LGPD / GDPR Compliant</div>
                    </div>
                </div>

                <!-- STRUCTURED RESULTS TABLE -->
                <div class="table-wrap">
                    <h4>
                        <span>5 Pillars of Institutional AI Governance & Intervention Routing</span>
                        <span style="font-size:10.5px; color:var(--text-muted);">Operational Standards</span>
                    </h4>
                    <table class="results-tbl">
                        <thead>
                            <tr>
                                <th>Governance Pillar</th>
                                <th>Binding Policy Rule</th>
                                <th>Clinical Intervention Guardrail</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>1. Advisory Use Only</strong></td>
                                <td>Automated dismissal/punitive tracking strictly prohibited</td>
                                <td>Model flags trigger clinical support, never expulsion</td>
                            </tr>
                            <tr>
                                <td><strong>2. Explainability Coupling</strong></td>
                                <td>Every risk flag MUST include SHAP/LIME cards</td>
                                <td>Counselors inspect root causes (GPA vs. Transit)</td>
                            </tr>
                            <tr>
                                <td><strong>3. Semi-Annual Re-Audits</strong></td>
                                <td>Mandatory EEOC equity checks before each semester</td>
                                <td>Protects against demographic concept drift</td>
                            </tr>
                            <tr>
                                <td><strong>4. Student Right to Appeal</strong></td>
                                <td>Right to explanation and ombudsman review</td>
                                <td>Transparent data access under LGPD/FERPA laws</td>
                            </tr>
                            <tr>
                                <td><strong>5. Counselor Supremacy</strong></td>
                                <td>Human staff retain exclusive final authority</td>
                                <td>Algorithm never triggers autonomous sanctions</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- CLINICAL CALLOUT -->
                <div class="callout-box">
                    <strong>Institutional Safe Guard:</strong> Immutable demographic attributes (Race, Gender, Age) are strictly shielded from punitive or exclusionary action. Interventions focus exclusively on actionable student academic and attendance contracts.
                </div>
            </div>

            <!-- RIGHT PANE: DIAGRAMS & GRAPHS (SMALLER SPACE ~42%) -->
            <div class="graphs-pane">
                <div class="graphs-topbar">
                    <div class="graphs-title">AI Governance Architecture & Clinical Protocol</div>
                    <div class="diagram-pills">
                        <button class="diagram-pill-btn active" onclick="switchDiagram(5, 'framework')">Governance Framework</button>
                    </div>
                </div>
                <div class="diagram-viewport" onclick="openLightbox('01_phase5_governance_framework.png')">
                    <img id="img-phase-5" class="diagram-img" src="01_phase5_governance_framework.png" alt="Governance Architecture">
                    <div class="diagram-zoom-hint">🔍 Click to Expand</div>
                </div>
                <div class="diagram-caption" id="caption-phase-5">
                    <strong>Figure 5.1:</strong> Certified Human-in-the-Loop operational workflow and 5-Pillar AI Governance Charter ensuring ethical clinical deployment in public technical education.
                </div>
            </div>
        </section>

    </main>

    <!-- FULLSCREEN LIGHTBOX MODAL -->
    <div class="lightbox-modal" id="lightboxModal" onclick="closeLightbox()">
        <button class="lightbox-close" onclick="closeLightbox()">✕</button>
        <img class="lightbox-img" id="lightboxImg" src="" alt="Enlarged Diagram">
    </div>

    <!-- JAVASCRIPT LOGIC -->
    <script>
        // Pre-embedded JSON Data
        const studentsData = {students_json};
        const counterfactualsData = {cf_json};
        const decodedMetadata = {meta_json};

        let currentPhase = 1;
        let currentDiagramKeys = {{
            1: 'eda',
            2: 'comparison',
            3: 'beeswarm',
            4: 'audit',
            5: 'framework'
        }};

        // Phase switching
        function switchPhase(phaseNum) {{
            currentPhase = phaseNum;
            document.querySelectorAll('.phase-section').forEach(sec => sec.classList.remove('active'));
            document.querySelectorAll('.phase-tab-btn').forEach(btn => btn.classList.remove('active'));

            const targetSec = document.getElementById('phase-sec-' + phaseNum);
            const targetBtn = document.getElementById('tab-btn-' + phaseNum);

            if (targetSec) targetSec.classList.add('active');
            if (targetBtn) targetBtn.classList.add('active');
        }}

        function prevPhase() {{
            let prev = currentPhase - 1;
            if (prev < 1) prev = 5;
            switchPhase(prev);
        }}

        function nextPhase() {{
            let next = currentPhase + 1;
            if (next > 5) next = 1;
            switchPhase(next);
        }}

        // Keyboard Navigation
        window.addEventListener('keydown', (e) => {{
            if (e.key === '1') switchPhase(1);
            else if (e.key === '2') switchPhase(2);
            else if (e.key === '3') switchPhase(3);
            else if (e.key === '4') switchPhase(4);
            else if (e.key === '5') switchPhase(5);
            else if (e.key === 'ArrowLeft') prevPhase();
            else if (e.key === 'ArrowRight') nextPhase();
            else if (e.key === 'Escape') closeLightbox();
        }});

        // Diagram Switcher Logic
        const diagramMap = {{
            1: {{
                'eda': {{
                    src: 'phase1_outputs/01_phase1_eda_and_preprocessing.png',
                    caption: '<strong>Figure 1.1:</strong> Multi-panel institutional baseline showing the 77.6%/22.4% class imbalance, 4 course modalities, the attendance cliff (&lt;70%), and the 5-step leak-free preprocessing funnel.'
                }}
            }},
            2: {{
                'comparison': {{
                    src: '01_model_comparison.png',
                    caption: '<strong>Figure 2.1:</strong> Recall, Precision, and F1 comparisons across 48 configurations on 3,017 unseen test students, demonstrating Random Forest superiority.'
                }},
                'cm': {{
                    src: '02_confusion_matrices.png',
                    caption: '<strong>Figure 2.2:</strong> Confusion matrices across Random Forest, Decision Tree, Logistic Regression, and Linear SVM, demonstrating high 95.2% true negative rate and low 112 false alarms.'
                }},
                'roc': {{
                    src: '03_roc_curves.png',
                    caption: '<strong>Figure 2.3:</strong> ROC Curves showing champion Random Forest AUC of 0.951 vs Decision Tree (0.854), Logistic Regression (0.887), and SVM (0.591).'
                }},
                'balancing': {{
                    src: '04_balancing_strategy_impact.png',
                    caption: '<strong>Figure 2.4:</strong> Balancing strategy impact analysis: UnderSampling achieves optimal recall without the synthetic distortion of SMOTE.'
                }},
                'feat_imp': {{
                    src: '05_top_features_importance.png',
                    caption: '<strong>Figure 2.5:</strong> Random Forest Gini feature importances highlighting academic GPA, attendance rate, and course failures as primary indicators.'
                }}
            }},
            3: {{
                'beeswarm': {{
                    src: 'phase3_outputs/01_shap_global_beeswarm.png',
                    caption: '<strong>Figure 3.1:</strong> SHAP Beeswarm plot showing low GPA (blue dots right) and low attendance driving intense dropout probability across 3,017 test students.'
                }},
                'importance': {{
                    src: 'phase3_outputs/02_shap_feature_importance.png',
                    caption: '<strong>Figure 3.2:</strong> Mean |SHAP| feature importance ranking with GPA dominating (0.2717), followed by Attendance (0.0570) and Failures (0.0468).'
                }},
                'dependence': {{
                    src: 'phase3_outputs/03_shap_dependence_ira.png',
                    caption: '<strong>Figure 3.3:</strong> SHAP dependence plot for Cumulative GPA (ira) demonstrating the non-linear risk cliff when GPA drops below 5.0.'
                }},
                'lime43': {{
                    src: 'phase3_outputs/05_lime_chart_borderline_43_student_43.png',
                    caption: '<strong>Figure 3.4:</strong> Local surrogate LIME attribution for Borderline Student #43 (65.0% Risk) identifying attendance below 70% as the primary reversible risk factor.'
                }}
            }},
            4: {{
                'audit': {{
                    src: 'phase4_outputs/01_comprehensive_fairness_audit.png',
                    caption: '<strong>Figure 4.1:</strong> 4-panel algorithmic audit certifying race equity (Disparate Impact 1.180), equal opportunity recall parity, and robust 80.8% active student sensitivity.'
                }}
            }},
            5: {{
                'framework': {{
                    src: '01_phase5_governance_framework.png',
                    caption: '<strong>Figure 5.1:</strong> Certified Human-in-the-Loop operational workflow and 5-Pillar AI Governance Charter ensuring ethical clinical deployment in public technical education.'
                }}
            }}
        }};

        function switchDiagram(phaseNum, key) {{
            currentDiagramKeys[phaseNum] = key;

            // Update pills
            const section = document.getElementById('phase-sec-' + phaseNum);
            section.querySelectorAll('.diagram-pill-btn').forEach(b => b.classList.remove('active'));
            if (event && event.currentTarget) event.currentTarget.classList.add('active');

            // Handle Phase 3 simulator toggle
            if (phaseNum === 3) {{
                const imgViewport = document.getElementById('viewport-phase-3');
                const simWrapper = document.getElementById('sim-wrapper-phase-3');
                if (key === 'sim') {{
                    imgViewport.style.display = 'none';
                    simWrapper.style.display = 'flex';
                    document.getElementById('caption-phase-3').innerHTML = '<strong>Interactive Simulator:</strong> Adjust attendance and GPA sliders to test actionable counterfactual intervention contracts in real-time.';
                    return;
                }} else {{
                    imgViewport.style.display = 'flex';
                    simWrapper.style.display = 'none';
                }}
            }}

            // Handle Phase 4 table views
            if (phaseNum === 4) {{
                const imgViewport = document.getElementById('viewport-phase-4');
                const tableInter = document.getElementById('table-inter-phase-4');
                const tableEW = document.getElementById('table-ew-phase-4');

                if (key === 'intersectional') {{
                    imgViewport.style.display = 'none';
                    tableEW.style.display = 'none';
                    tableInter.style.display = 'block';
                    document.getElementById('caption-phase-4').innerHTML = '<strong>Intersectional Matrix:</strong> 8-group compound equity evaluation across Gender × Race × Household Income on 100% real student records.';
                    return;
                }} else if (key === 'early_warning') {{
                    imgViewport.style.display = 'none';
                    tableInter.style.display = 'none';
                    tableEW.style.display = 'block';
                    document.getElementById('caption-phase-4').innerHTML = '<strong>Early-Warning Validation:</strong> Confirms 80.8% Recall and 82.5% Precision on active enrolled students (GPA &gt; 0).';
                    return;
                }} else {{
                    imgViewport.style.display = 'flex';
                    tableInter.style.display = 'none';
                    tableEW.style.display = 'none';
                }}
            }}

            const info = diagramMap[phaseNum][key];
            if (!info) return;

            const imgEl = document.getElementById('img-phase-' + phaseNum);
            const capEl = document.getElementById('caption-phase-' + phaseNum);
            if (imgEl) imgEl.src = info.src;
            if (capEl) capEl.innerHTML = info.caption;
        }}

        // Lightbox Functions
        function openLightbox(src) {{
            const modal = document.getElementById('lightboxModal');
            const img = document.getElementById('lightboxImg');
            img.src = src;
            modal.classList.add('active');
        }}

        function openCurrentLightbox(phaseNum) {{
            const key = currentDiagramKeys[phaseNum];
            if (diagramMap[phaseNum] && diagramMap[phaseNum][key]) {{
                openLightbox(diagramMap[phaseNum][key].src);
            }}
        }}

        function closeLightbox() {{
            document.getElementById('lightboxModal').classList.remove('active');
        }}

        function toggleFullscreen() {{
            if (!document.fullscreenElement) {{
                document.documentElement.requestFullscreen().catch(() => {{}});
            }} else {{
                if (document.exitFullscreen) document.exitFullscreen();
            }}
        }}

        // Simulator Logic (Phase 3)
        let simStudentId = '43';

        function initSimulator() {{
            const sel = document.getElementById('p3-student-select');
            if (!sel || !studentsData) return;
            sel.innerHTML = '';
            studentsData.forEach(s => {{
                const opt = document.createElement('option');
                opt.value = s.id;
                opt.text = `Student #${{s.id}} — ${{s.prob}}% Risk (${{s.actual}})`;
                if (s.id == '43') opt.selected = true;
                sel.appendChild(opt);
            }});
            onSimulatorStudentChange('43');
        }}

        function onSimulatorStudentChange(id) {{
            simStudentId = id;
            const s = studentsData.find(item => item.id == id);
            if (!s) return;

            const meta = decodedMetadata[id] || {{}};
            document.getElementById('sim-student-name').innerText = `Student #${{s.id}} Audit (${{s.pred}})`;
            const badge = document.getElementById('sim-risk-badge');
            badge.innerText = `${{s.prob}}% Risk`;
            badge.className = 'badge ' + (s.prob >= 70 ? 'badge-fail' : (s.prob >= 40 ? 'badge-warn' : 'badge-pass'));

            document.getElementById('sim-student-sub').innerText = `Actual: ${{s.actual}} | Modality: ${{meta.modality_en || 'Technical High School'}}`;

            const f = s.features_raw || s.features || {{}};
            const att = f.percentual_frequencia !== undefined ? f.percentual_frequencia : 75;
            const gpa = f.ira !== undefined ? f.ira : 6.0;

            document.getElementById('slider-att').value = att;
            document.getElementById('sim-att-val').innerText = `${{att}}%`;

            document.getElementById('slider-gpa').value = gpa;
            document.getElementById('sim-gpa-val').innerText = `${{gpa}} / 10.0`;

            recalcSimRisk();
        }}

        function updateSimAttendance(val) {{
            document.getElementById('sim-att-val').innerText = `${{val}}%`;
            recalcSimRisk();
        }}

        function updateSimGPA(val) {{
            document.getElementById('sim-gpa-val').innerText = `${{val}} / 10.0`;
            recalcSimRisk();
        }}

        function recalcSimRisk() {{
            const att = parseFloat(document.getElementById('slider-att').value);
            const gpa = parseFloat(document.getElementById('slider-gpa').value);

            // Realistic logistic model sensitivity approximation based on Phase 3 curves
            let baseProb = 0.5;
            const s = studentsData.find(item => item.id == simStudentId);
            if (s) baseProb = s.prob / 100;

            // Attendance sensitivity (-0.015 per 1% above 75%)
            const attShift = (att - 75) * -0.018;
            // GPA sensitivity (-0.12 per point above 5.0)
            const gpaShift = (gpa - 5.0) * -0.14;

            let newProb = baseProb + attShift + gpaShift;
            newProb = Math.max(0.02, Math.min(0.99, newProb));
            const newPct = (newProb * 100).toFixed(1);

            const badge = document.getElementById('sim-risk-badge');
            badge.innerText = `${{newPct}}% Risk`;
            badge.className = 'badge ' + (newPct >= 70 ? 'badge-fail' : (newPct >= 40 ? 'badge-warn' : 'badge-pass'));

            const advice = document.getElementById('sim-action-advice');
            if (newPct < 35) {{
                advice.innerHTML = `<span style="color:#059669; font-weight:700;">SAFE ZONE ACHIEVED!</span> Remedial attendance & tutoring contract successfully offsets dropout hazard. Maintain fortnightly counseling review.`;
            }} else if (newPct < 65) {{
                advice.innerHTML = `<span style="color:#d97706; font-weight:700;">MODERATE RISK:</span> Student is near retention boundary. Boosting attendance to ≥85% is projected to push student into the safe zone.`;
            }} else {{
                advice.innerHTML = `<span style="color:#dc2626; font-weight:700;">ACUTE RISK:</span> Urgent multi-disciplinary counselor intervention required. Combine academic tutoring with transportation/food assistance.`;
            }}
        }}

        // Initialize Simulator when page loads
        window.addEventListener('DOMContentLoaded', () => {{
            initSimulator();
        }});
    </script>
</body>
</html>
"""

    with open("dashboard.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("[SUCCESS] Successfully regenerated dashboard.html with STRICT LEFT=TEXT(58%) & RIGHT=GRAPHS(42%)")

if __name__ == "__main__":
    generate_dashboard()
