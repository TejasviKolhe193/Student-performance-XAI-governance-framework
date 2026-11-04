"""
Regenerate Stale Figures: Fig. 2 (Modality) and Fig. 5 (Fairness Dashboard)
==========================================================================
Recomputes and regenerates:
  1. Fig. 2: Dropout Rate by Educational Modality (from locked N=15,084 cohort)
  2. Fig. 5: Comprehensive Fairness Audit Dashboard (4 panels from locked N=4,526 test set)

Saves to:
  - phase1_outputs/02_dropout_by_modality.png
  - results/fig2_modality_dropout.png
  - phase4_outputs/01_comprehensive_fairness_audit.png
  - results/fig4_fairness_audit.png
  - paper_review/research_paper_final_with_updates.docx (replaces media/image2.png and media/image5.png)
  - paper_review/research_paper_final_draft.docx (replaces media/image2.png and media/image5.png/image4.png)
"""

import os
import sys
import pickle
import zipfile
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import recall_score, precision_score

sys.stdout.reconfigure(encoding='utf-8')

# Ensure output directories exist
os.makedirs("results", exist_ok=True)
os.makedirs("phase1_outputs", exist_ok=True)
os.makedirs("phase4_outputs", exist_ok=True)
os.makedirs("paper_review", exist_ok=True)

print("=" * 80)
print("REGENERATING STALE FIGURES: FIG. 2 (MODALITY) AND FIG. 5 (FAIRNESS)")
print("=" * 80)

# ==============================================================================
# 1. GENERATE FIG. 2: DROPOUT RATE BY EDUCATIONAL MODALITY (LOCKED RUN)
# ==============================================================================
print("\n[1/2] Generating Fig. 2: Dropout Rate by Educational Modality...")

# Load raw dataset to get exact verified counts
df_raw = pd.read_excel("dataset_evasao_MDE.xlsx")
secondary_modalities = ["Integrado", "Concomitante", "Subsequente", "Integrado EJA"]
df = df_raw[df_raw["modalidade"].isin(secondary_modalities)].copy()

completed_vals = ["Concluído"]
dropout_vals = ["Evasão", "Cancelado", "Cancelamento Compulsório", "Jubilado", "Transferido Externo"]

def map_target(val):
    if val in completed_vals:
        return 0
    elif val in dropout_vals:
        return 1
    return np.nan

df["target"] = df["situacao"].apply(map_target)
df_clean = df.dropna(subset=["target"]).copy()
df_clean["target"] = df_clean["target"].astype(int)

# Exact order matching the original figure
modality_order = [
    ("Integrado", "Integrado\n(Regular HS)", "#3b82f6"),
    ("Subsequente", "Subsequente\n(Post-Sec Adult)", "#f59e0b"),
    ("Concomitante", "Concomitante\n(Concurrent)", "#8b5cf6"),
    ("Integrado EJA", "Integrado EJA\n(Adult Evening)", "#ec4899")
]

modalities = []
labels = []
counts = []
rates = []
colors = []

for mod_code, mod_label, mod_color in modality_order:
    sub = df_clean[df_clean["modalidade"] == mod_code]
    n = len(sub)
    d = (sub["target"] == 1).sum()
    rate = (d / n) * 100
    modalities.append(mod_code)
    labels.append(mod_label)
    counts.append(n)
    rates.append(rate)
    colors.append(mod_color)
    print(f"  {mod_code}: N = {n:,}, Dropouts = {d:,}, Rate = {rate:.1f}%")

# Create Fig 2
fig, ax = plt.subplots(figsize=(6.5, 4.8), dpi=300)

bars = ax.bar(labels, rates, color=colors, width=0.55, edgecolor="#1f2937", linewidth=1.0)
ax.axhline(22.41, color="#ef4444", linestyle="--", linewidth=1.2, alpha=0.85, label="Cohort Baseline (22.4%)")

ax.set_ylim(0, 52)
ax.set_ylabel("Empirical Dropout Rate (%)", fontsize=11, fontweight="bold", color="#1e293b")
ax.set_title("Dropout Rate by Educational Modality", fontsize=13, fontweight="bold", pad=12, color="#1e293b")
ax.grid(axis="y", linestyle=":", alpha=0.6)
ax.legend(loc="upper left", fontsize=9.5, framealpha=0.9)

# Add exact text labels above bars
for bar, r, n in zip(bars, rates, counts):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 1.2,
            f"{r:.1f}%\n(N={n:,})",
            ha="center", va="bottom", fontsize=9.5, fontweight="bold", color="#1e293b")

plt.tight_layout()

# Save Fig 2 outputs
fig2_paths = [
    "results/fig2_modality_dropout.png",
    "phase1_outputs/02_dropout_by_modality.png"
]
for p in fig2_paths:
    fig.savefig(p, dpi=300, bbox_inches="tight")
    print(f"  ✓ Saved Fig 2: {p}")
plt.close(fig)


# ==============================================================================
# 2. GENERATE FIG. 5: COMPREHENSIVE FAIRNESS AUDIT DASHBOARD (LOCKED RUN)
# ==============================================================================
print("\n[2/2] Generating Fig. 5: Comprehensive Fairness Audit Dashboard...")

# Load locked Phase 2 model bundle and Phase 1 test data
with open("phase2_outputs/champion_model_bundle.pkl", "rb") as f:
    bundle = pickle.load(f)

rf = bundle["champion_rf"]
mask = bundle["champion_mask"]
X_test = bundle["X_test"][:, mask]
y_test = bundle["y_test"]

with open("phase1_outputs/phase1_data.pkl", "rb") as f:
    p1 = pickle.load(f)

test_df_raw = p1["test_df_raw"]

# Compute threshold precision-recall curve
y_probs = rf.predict_proba(X_test)[:, 1]
threshold_list = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]
curve_recalls = []
curve_precisions = []

for th in threshold_list:
    preds = (y_probs >= th).astype(int)
    curve_recalls.append(recall_score(y_test, preds) * 100)
    curve_precisions.append(precision_score(y_test, preds) * 100)

# Load locked Phase 4 fairness audit results
df_fairness_all = pd.read_csv("phase4_outputs/phase4_fairness_audit_results.csv")
df_fairness_050 = df_fairness_all[df_fairness_all["Threshold"] == 0.5].copy()

# The 5 standard dimensions displayed in Fig. 5
fairness_dims = [
    {
        "name": "Gender",
        "row": df_fairness_050[df_fairness_050["Attribute"].str.contains("Gender")].iloc[0]
    },
    {
        "name": "Race / Ethnicity",
        "row": df_fairness_050[df_fairness_050["Attribute"].str.contains("Preta")].iloc[0]  # Branca vs Preta
    },
    {
        "name": "Household Income",
        "row": df_fairness_050[df_fairness_050["Attribute"].str.contains("Income")].iloc[0]
    },
    {
        "name": "Age Cohort",
        "row": df_fairness_050[df_fairness_050["Attribute"].str.contains("Age")].iloc[0]
    },
    {
        "name": "Digital Access",
        "row": df_fairness_050[df_fairness_050["Attribute"].str.contains("Computer")].iloc[0]
    }
]

dims = [d["name"] for d in fairness_dims]
di_vals = [d["row"]["Disparate_Impact"] for d in fairness_dims]
priv_rec = [d["row"]["TPR_Priv"] * 100 for d in fairness_dims]
unpriv_rec = [d["row"]["TPR_Unpriv"] * 100 for d in fairness_dims]
spd_vals = [d["row"]["Statistical_Parity_Diff"] for d in fairness_dims]

print("  Locked Fairness Metrics (tau = 0.50):")
for d, di, spd, pr, ur in zip(dims, di_vals, spd_vals, priv_rec, unpriv_rec):
    print(f"    {d:<18}: DI = {di:.3f}, SPD = {spd:+.3f}, Priv Recall = {pr:.1f}%, Unpriv Recall = {ur:.1f}%")

# Create 4-panel figure matching exact visual structure of Image 5
fig, axes = plt.subplots(2, 2, figsize=(15, 11), dpi=300)

# ── Panel A: Disparate Impact Ratio ──
di_colors = ["#10b981" if 0.80 <= v <= 1.25 else "#f59e0b" for v in di_vals]
bars_a = axes[0, 0].bar(dims, di_vals, color=di_colors, width=0.45, edgecolor="#1f2937", linewidth=0.9)
axes[0, 0].axhline(0.80, color="#ef4444", linestyle="--", linewidth=1.5, label="80% Lower Bound (0.80)")
axes[0, 0].axhline(1.25, color="#ef4444", linestyle="--", linewidth=1.5, label="125% Upper Bound (1.25)")
axes[0, 0].axhline(1.00, color="#6b7280", linestyle=":", linewidth=1.1, label="Parity Target (1.00)")
axes[0, 0].set_ylim(0, 1.85)
axes[0, 0].set_ylabel("Disparate Impact Ratio", fontsize=11, fontweight="bold")
axes[0, 0].set_title("A. Disparate Impact Ratio vs. Four-Fifths Standard", fontsize=12, fontweight="bold", pad=8)
axes[0, 0].legend(loc="upper right", fontsize=9.5, framealpha=0.9)
axes[0, 0].grid(axis="y", linestyle=":", alpha=0.6)

for bar, val in zip(bars_a, di_vals):
    axes[0, 0].text(bar.get_x() + bar.get_width() / 2, val + 0.035,
                    f"{val:.3f}", ha="center", va="bottom", fontweight="bold", fontsize=9.5)

# ── Panel B: Equal Opportunity Parity ──
x = np.arange(len(dims))
w = 0.28
axes[0, 1].bar(x - w/2, priv_rec, w, label="Privileged Group", color="#3b82f6", edgecolor="#1f2937", linewidth=0.9)
axes[0, 1].bar(x + w/2, unpriv_rec, w, label="Protected Slice", color="#ec4899", edgecolor="#1f2937", linewidth=0.9)
axes[0, 1].set_xticks(x)
axes[0, 1].set_xticklabels(dims, fontsize=9.5, rotation=10)
axes[0, 1].set_ylim(0, 105)
axes[0, 1].set_ylabel("Recall / True Positive Rate (%)", fontsize=11, fontweight="bold")
axes[0, 1].set_title("B. Equal Opportunity: Recall Parity per Protected Slice", fontsize=12, fontweight="bold", pad=8)
axes[0, 1].legend(loc="lower right", fontsize=9.5, framealpha=0.9)
axes[0, 1].grid(axis="y", linestyle=":", alpha=0.6)

for i in range(len(dims)):
    axes[0, 1].text(x[i] - w/2, priv_rec[i] + 1.3, f"{priv_rec[i]:.1f}%", ha="center", fontsize=8.5, fontweight="bold")
    axes[0, 1].text(x[i] + w/2, unpriv_rec[i] + 1.3, f"{unpriv_rec[i]:.1f}%", ha="center", fontsize=8.5, fontweight="bold")

# ── Panel C: Statistical Parity Difference ──
spd_colors = ["#10b981" if abs(v) <= 0.10 else "#f59e0b" for v in spd_vals]
axes[1, 0].barh(dims, spd_vals, color=spd_colors, edgecolor="#1f2937", linewidth=0.9, height=0.55)
axes[1, 0].axvline(0.00, color="black", linestyle="-", linewidth=1.0)
axes[1, 0].axvline(-0.10, color="#ef4444", linestyle="--", linewidth=1.2, label="Acceptable Tolerance (±0.10)")
axes[1, 0].axvline(0.10, color="#ef4444", linestyle="--", linewidth=1.2)
axes[1, 0].set_xlim(-0.12, 0.16)
axes[1, 0].set_xlabel("Statistical Parity Difference (Unpriv - Priv)", fontsize=11, fontweight="bold")
axes[1, 0].set_title("C. Statistical Parity Difference (Selection Rate Gap)", fontsize=12, fontweight="bold", pad=8)
axes[1, 0].legend(loc="lower right", fontsize=9.5, framealpha=0.9)
axes[1, 0].grid(axis="x", linestyle=":", alpha=0.6)

for i, v in enumerate(spd_vals):
    x_pos = v + (0.005 if v >= 0 else -0.018)
    axes[1, 0].text(x_pos, i, f"{v:+.3f}", va="center", ha="left" if v >= 0 else "right",
                    fontweight="bold", fontsize=9)

# ── Panel D: Threshold Recalibration ──
axes[1, 1].plot(threshold_list, curve_recalls, marker="o", color="#2563eb", linewidth=2.2, label="Global Recall (%)")
axes[1, 1].plot(threshold_list, curve_precisions, marker="s", color="#10b981", linewidth=2.2, label="Global Precision (%)")
axes[1, 1].axvline(0.50, color="#ef4444", linestyle="--", linewidth=1.5, label="Default Threshold (0.50)")
axes[1, 1].set_xlabel("Decision Threshold", fontsize=11, fontweight="bold")
axes[1, 1].set_ylabel("Performance (%)", fontsize=11, fontweight="bold")
axes[1, 1].set_title("D. Accuracy vs. Threshold Recalibration", fontsize=12, fontweight="bold", pad=8)
axes[1, 1].set_ylim(50, 90)
axes[1, 1].legend(loc="center right", fontsize=9.5, framealpha=0.9)
axes[1, 1].grid(linestyle=":", alpha=0.6)

plt.tight_layout()

# Save Fig 5 outputs
fig5_paths = [
    "phase4_outputs/01_comprehensive_fairness_audit.png",
    "results/fig4_fairness_audit.png"
]
for p in fig5_paths:
    fig.savefig(p, dpi=300, bbox_inches="tight")
    print(f"  ✓ Saved Fig 5: {p}")
plt.close(fig)


# ==============================================================================
# 3. UPDATE EMBEDDED IMAGES INSIDE RESEARCH PAPER DOCX FILES
# ==============================================================================
print("\n[3/3] Updating embedded images inside Word docx files...")

with open("results/fig2_modality_dropout.png", "rb") as f:
    fig2_bytes = f.read()

with open("phase4_outputs/01_comprehensive_fairness_audit.png", "rb") as f:
    fig5_bytes = f.read()

target_docs = [
    "paper_review/research_paper_final_with_updates.docx",
    "paper_review/research_paper_final_draft.docx"
]

for doc_path in target_docs:
    if not os.path.exists(doc_path):
        continue
    print(f"  Updating {doc_path}...")
    tmp_path = doc_path + ".tmp.zip"
    with zipfile.ZipFile(doc_path, 'r') as zin:
        with zipfile.ZipFile(tmp_path, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == "word/media/image2.png":
                    zout.writestr(item, fig2_bytes)
                    print(f"    ✓ Replaced word/media/image2.png (Fig. 2 Modality)")
                elif item.filename in ["word/media/image5.png", "word/media/image4.png"] and "with_updates" in doc_path and item.filename == "word/media/image5.png":
                    zout.writestr(item, fig5_bytes)
                    print(f"    ✓ Replaced {item.filename} (Fig. 5 Fairness)")
                elif item.filename == "word/media/image5.png":
                    zout.writestr(item, fig5_bytes)
                    print(f"    ✓ Replaced word/media/image5.png (Fig. 5 Fairness)")
                else:
                    zout.writestr(item, zin.read(item.filename))
    os.replace(tmp_path, doc_path)
    print(f"  ✓ Finished updating {doc_path}")

print("\n" + "=" * 80)
print("SUCCESS: BOTH FIG. 2 AND FIG. 5 SUCCESSFULLY REGENERATED FROM LOCKED RUN!")
print("=" * 80)

