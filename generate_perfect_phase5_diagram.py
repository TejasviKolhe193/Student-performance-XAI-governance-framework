# -*- coding: utf-8 -*-
"""
generate_perfect_phase5_diagram.py
Generates a clean, professional, non-overlapping Phase 5 Governance Framework
diagram (01_phase5_governance_framework.png) where all text fits comfortably
within each box with proper padding and text wrapping.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import textwrap

# Setup figure
fig = plt.figure(figsize=(16, 9.2), dpi=200)
ax = fig.add_subplot(111)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Background
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#ffffff')

# Outer Card Frame
outer_frame = patches.FancyBboxPatch(
    (1.5, 1.5), 97, 97,
    boxstyle="round,pad=0.0,rounding_size=1.5",
    facecolor="#ffffff",
    edgecolor="#e2e8f0",
    linewidth=1.2,
    zorder=0
)
ax.add_patch(outer_frame)

# -------------------------------------------------------------------------
# Title Block
# -------------------------------------------------------------------------
ax.text(
    50, 94.5,
    "Phase 5: Institutional AI Governance Charter & Human-in-the-Loop Protocol",
    fontsize=16.5,
    fontweight='bold',
    ha='center',
    va='center',
    color='#0f172a'
)
ax.text(
    50, 91.8,
    "Certified Operational Standards & Counselor Intervention Workflow for Secondary Technical Education",
    fontsize=10.5,
    fontweight='normal',
    ha='center',
    va='center',
    color='#64748b'
)

# -------------------------------------------------------------------------
# SECTION 1: 5 Binding Ethical Pillars of AI Governance
# -------------------------------------------------------------------------
ax.text(
    5.0, 87.5,
    "5 Binding Ethical Pillars of AI Governance",
    fontsize=12.5,
    fontweight='bold',
    ha='left',
    va='center',
    color='#1e3a8a'
)

pillars = [
    {
        "num": "1",
        "title": "Strictly Advisory Use",
        "desc": "Automated disciplinary actions, punitive sanctions, or student exclusion are strictly prohibited. Algorithmic autonomy is capped at decision support.",
        "border": "#2563eb",
        "bg": "#eff6ff",
        "header_bg": "#dbeafe"
    },
    {
        "num": "2",
        "title": "Explainability Coupling",
        "desc": "Every risk designation must be paired with an dual causal attribution card (SHAP & LIME) to reveal individual driving factors before review.",
        "border": "#0d9488",
        "bg": "#f0fdfa",
        "header_bg": "#ccfbf1"
    },
    {
        "num": "3",
        "title": "Bi-Annual Recalibration",
        "desc": "Re-train with fresh institutional cohorts bi-annually to eliminate concept drift and guarantee continuous Four-Fifths EEOC compliance.",
        "border": "#d97706",
        "bg": "#fffbeb",
        "header_bg": "#fef3c7"
    },
    {
        "num": "4",
        "title": "Independent Appeals",
        "desc": "Every student possesses the statutory right to request a plain-language explanation and contest designations with an independent ombudsman.",
        "border": "#7c3aed",
        "bg": "#faf5ff",
        "header_bg": "#f3e8ff"
    },
    {
        "num": "5",
        "title": "Counselor Authority",
        "desc": "Certified educational advisors maintain exclusive, final decision authority over every student intervention plan. Algorithmic override is binding.",
        "border": "#dc2626",
        "bg": "#fff1f2",
        "header_bg": "#ffe4e6"
    }
]

box_width = 17.5
box_gap = 1.8
x_start = 5.0
y_top = 85.0
box_height = 25.5

for i, p in enumerate(pillars):
    bx = x_start + i * (box_width + box_gap)
    by = y_top - box_height
    
    # Pillar card background
    card = patches.FancyBboxPatch(
        (bx, by), box_width, box_height,
        boxstyle="round,pad=0.0,rounding_size=1.2",
        facecolor=p["bg"],
        edgecolor=p["border"],
        linewidth=1.8,
        zorder=1
    )
    ax.add_patch(card)
    
    # Pillar Header Banner (top section of card)
    banner_height = 5.2
    banner = patches.FancyBboxPatch(
        (bx, y_top - banner_height), box_width, banner_height,
        boxstyle="round,pad=0.0,rounding_size=1.2",
        facecolor=p["header_bg"],
        edgecolor=p["border"],
        linewidth=1.0,
        zorder=2
    )
    ax.add_patch(banner)
    
    # Header Title
    header_text = f"{p['num']}. {p['title']}"
    ax.text(
        bx + box_width / 2.0,
        y_top - (banner_height / 2.0),
        header_text,
        fontsize=9.2,
        fontweight='bold',
        ha='center',
        va='center',
        color=p["border"],
        zorder=3
    )
    
    # Description Text - carefully wrapped to 24 characters
    wrapped_desc = textwrap.fill(p["desc"], width=23)
    ax.text(
        bx + 1.2,
        y_top - banner_height - 1.8,
        wrapped_desc,
        fontsize=7.8,
        ha='left',
        va='top',
        color='#334155',
        linespacing=1.45,
        zorder=3
    )

# -------------------------------------------------------------------------
# SECTION 2: Certified Human-in-the-Loop Operational Workflow
# -------------------------------------------------------------------------
ax.text(
    5.0, 54.0,
    "Certified Human-in-the-Loop Operational Workflow",
    fontsize=12.5,
    fontweight='bold',
    ha='left',
    va='center',
    color='#1e3a8a'
)

workflow_steps = [
    {
        "step": "1. Active Student Signal",
        "desc": "GPA > 0 & Attendance tracked in campus SIS.",
        "border": "#2563eb",
        "bg": "#f8fafc"
    },
    {
        "step": "2. Champion RF Inference",
        "desc": "Trained RF evaluates 15 engineered features.",
        "border": "#0d9488",
        "bg": "#f8fafc"
    },
    {
        "step": "3. Dual XAI Generation",
        "desc": "SHAP waterfall & LIME attribution cards produced.",
        "border": "#16a34a",
        "bg": "#f8fafc"
    },
    {
        "step": "4. Counselor Review",
        "desc": "Staff reviews causal drivers (Attendance vs GPA).",
        "border": "#d97706",
        "bg": "#f8fafc"
    },
    {
        "step": "5. Targeted Action Plan",
        "desc": "Tutoring contract, transit voucher, or aid grant.",
        "border": "#9333ea",
        "bg": "#f8fafc"
    }
]

wf_y_top = 51.5
wf_box_height = 16.0
wf_box_width = 16.5
wf_box_gap = 2.8
wf_x_start = 5.0

for i, step in enumerate(workflow_steps):
    bx = wf_x_start + i * (wf_box_width + wf_box_gap)
    by = wf_y_top - wf_box_height
    
    # Workflow step card
    card = patches.FancyBboxPatch(
        (bx, by), wf_box_width, wf_box_height,
        boxstyle="round,pad=0.0,rounding_size=1.0",
        facecolor=step["bg"],
        edgecolor=step["border"],
        linewidth=1.8,
        zorder=1
    )
    ax.add_patch(card)
    
    # Step Header
    banner_h = 4.2
    banner = patches.FancyBboxPatch(
        (bx, wf_y_top - banner_h), wf_box_width, banner_h,
        boxstyle="round,pad=0.0,rounding_size=1.0",
        facecolor=step["border"],
        edgecolor=step["border"],
        linewidth=1.0,
        zorder=2
    )
    ax.add_patch(banner)
    
    ax.text(
        bx + wf_box_width / 2.0,
        wf_y_top - (banner_h / 2.0),
        step["step"],
        fontsize=8.5,
        fontweight='bold',
        ha='center',
        va='center',
        color='#ffffff',
        zorder=3
    )
    
    # Step Description
    wrapped_step_desc = textwrap.fill(step["desc"], width=21)
    ax.text(
        bx + 1.2,
        wf_y_top - banner_h - 1.8,
        wrapped_step_desc,
        fontsize=7.8,
        ha='left',
        va='top',
        color='#334155',
        linespacing=1.4,
        zorder=3
    )
    
    # Draw arrow to next step
    if i < len(workflow_steps) - 1:
        arrow_x_start = bx + wf_box_width + 0.3
        arrow_x_end = arrow_x_start + wf_box_gap - 0.6
        arrow_y = wf_y_top - (wf_box_height / 2.0)
        ax.annotate(
            "",
            xy=(arrow_x_end, arrow_y),
            xytext=(arrow_x_start, arrow_y),
            arrowprops=dict(
                arrowstyle="-|>",
                color="#64748b",
                lw=2.0,
                mutation_scale=14
            ),
            zorder=4
        )

# -------------------------------------------------------------------------
# SECTION 3: Core Ethical Principles & Safeguards Box
# -------------------------------------------------------------------------
core_box_y_top = 31.0
core_box_h = 24.0
core_box_w = 90.0
core_box_x = 5.0

core_box = patches.FancyBboxPatch(
    (core_box_x, core_box_y_top - core_box_h), core_box_w, core_box_h,
    boxstyle="round,pad=0.0,rounding_size=1.2",
    facecolor="#f0f9ff",
    edgecolor="#93c5fd",
    linewidth=1.5,
    zorder=1
)
ax.add_patch(core_box)

ax.text(
    core_box_x + 2.5,
    core_box_y_top - 3.8,
    "CORE ETHICAL PRINCIPLES & GOVERNANCE SAFEGUARDS:",
    fontsize=10.8,
    fontweight='bold',
    ha='left',
    va='center',
    color='#1e3a8a',
    zorder=2
)

principles = [
    (
        "• Mutable Intervention Principle: Counseling actions focus strictly on mutable, actionable levers "
        "(attendance coaching, peer tutoring, academic recovery, and nutrition/transit aid) rather than punitive measures."
    ),
    (
        "• Non-Maleficence Shield: Immutable demographic features (Race, Gender, Age, and Family Background) are "
        "strictly shielded from punitive or exclusionary decisions. Models undergo continuous Four-Fifths bias audits."
    ),
    (
        "• Human Supremacy Mandate: No automated notification or administrative action is triggered without explicit "
        "human counselor sign-off. High-uncertainty borderline predictions (40% - 70% risk) require dual counselor consensus."
    )
]

for idx, pr in enumerate(principles):
    wrapped_pr = textwrap.fill(pr, width=128)
    ax.text(
        core_box_x + 3.0,
        core_box_y_top - 7.5 - (idx * 5.2),
        wrapped_pr,
        fontsize=8.5,
        ha='left',
        va='top',
        color='#1e293b',
        linespacing=1.35,
        zorder=2
    )

plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
output_path = "01_phase5_governance_framework.png"
plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='#ffffff')
plt.close()

print(f"Successfully generated clean diagram at: {output_path}")

