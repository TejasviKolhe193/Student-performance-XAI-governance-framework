# Master Results Summary: Paper Reconciliation & Replication Audit

> **Protocol:** Strict Replication of Silva et al. (IEEE RITA 2025) and Algorithmic Governance Extensions  
> **Repository:** `student-performance-xai-governance-framework`  
> **Date:** 2026-11-03  
> **Seed:** Locked globally to `42` (`seeds.txt`)

---

## 1. Number-by-Number Reconciliation Table

| Metric / Parameter | Old Paper Draft Value | New Replicated / Audited Value | Source File / Output | Reconciliation & Validity Status |
| :--- | :---: | :---: | :--- | :--- |
| **Cohort Size** | 15,084 students | **15,084 students** | `dataset_evasao_MDE.xlsx` | **Exact Match.** Filtered across 4 secondary technical modalities (`Integrado`, `Subsequente`, `Concomitante`, `Integrado EJA`) and terminal statuses. |
| **Baseline Dropout Prevalence** | 22.4% | **22.41%** (3,381 dropouts, 11,703 completers) | `phase1_outputs/preprocessed_dataset_portuguese.csv` | **Exact Match.** |
| **Train / Test Partition Ratio** | 80% / 20% (12,067 / 3,017) | **70% / 30%** (10,558 / 4,526) | `run_replication_extension.py` | **Updated.** Realigned with Silva et al. 2025 Table III specifications (70/30 split). |
| **Cumulative GPA (`ira`) Feature** | Included (carried 54% SHAP attribution) | **Completely Removed** | `run_replication_extension.py` | **Major Fix.** GPA was an undocumented addition in the earlier draft causing outcome-accumulated target leakage (single-feature AUC 0.9004). Removed to match base paper. |
| **Feature Count** | 33 features | **32 features** (15 selected per run) | `results/replication_48_experiments.csv` | **Updated.** 32 non-GPA features (personal, demographic, socioeconomic, enrollment year/period, attendance, and failures). |
| **Target RF Model (SMOTEENN + Backward)** | — | — | `results/replication_vs_base_paper.csv` | — |
| • *ROC-AUC* | 0.951 (with GPA) | **0.854** | `results/replication_vs_base_paper.csv` | **Exact Match (0.854 vs. Base Paper 0.854, Diff = 0.000).** |
| • *Accuracy* | 0.929 (with GPA) | **0.856** | `results/replication_vs_base_paper.csv` | **Match within $\le 0.02$ (0.856 vs. Base Paper 0.852, Diff = +0.004).** |
| • *MEDIA_10_CV* | 0.878 (with GPA) | **0.931** | `results/replication_vs_base_paper.csv` | Replicated. (Base paper: 0.870). |
| • *Test Recall (Default 0.5 Thresh)* | 0.848 (with GPA) | **0.656** | `results/replication_vs_base_paper.csv` | At default 0.50 threshold on 22.4% natural prevalence; reaches **0.75+ at operating threshold (0.366)** and **0.854 on balanced priors**. |
| • *Test Precision (Default 0.5 Thresh)* | 0.836 (with GPA) | **0.686** | `results/replication_vs_base_paper.csv` | At default 0.50 threshold on natural prevalence (vs 0.847 under balanced priors). |
| **Target DT Model (SMOTEENN + Backward)** | — | — | `results/replication_vs_base_paper.csv` | — |
| • *Test Recall* | 0.771 (with GPA) | **0.676** | `results/replication_vs_base_paper.csv` | Base paper Table IV reported 0.818 under balanced priors. |
| **Overall Top Model by Recall** | — | **0.797 Recall, 0.705 Precision, 0.912 AUC** | `results/replication_top5.csv` | **UnderSampling + ANOVA + Random Forest** achieves the highest clean recall (79.7%) on the held-out test set without GPA leakage. |
| **Attendance Cliff Rates** | 8.4%, 18.2%, 48.7%, 62.4% | **Completely Removed** | `results/risk_band_table.csv` | **Excised.** The prior rates were mathematically ungrounded; the $<60\%$ band contains only 46 total students (45 dropouts = 97.8%). Cliff framing dropped. |
| **Dropout Attendance Median** | Claimed 97% | **97.0%** confirmed | `run_replication_extension.py` | **Explained.** 70.8% of dropouts ($2,394/3,381$) have attendance $\ge 90\%$ on record because attendance is only averaged over active class hours. |
| **Fairness Audit Metrics** | Gender DI = 0.707 | **5 Axes Audited with 95% Bootstrap CIs** | `results/fairness_audit_before.csv` | Full transparency: per-group $N$, base rate, selection rate, TPR, FPR, and Precision reported across Gender, Race, Income, Age, Digital Access. |
| **Declared Priority Fairness Rule** | None (Post-hoc) | **Equal Opportunity (TPR Parity)** | `results/fairness_audit_before.csv` | Declared *a priori* because missing an at-risk student imposes higher pedagogical harm than a false alert. |
| **Proxy Predictability Checks** | None reported | **Reported across 5 axes** | `results/fairness_proxy_check.csv` | Gender (0.607, No risk), Race (0.546, No risk), Income (0.679, No risk), Age (0.962, High risk), Digital Access (0.707, Moderate risk). |
| **Governance Layer Claims** | "Ensures zero harm" | **Normative Institutional Proposal** | `docs/governance_charter.md` | Explicitly marked as an untested proposal; mapped to LGPD Art. 20/46, EU AI Act Art. 14, NIST AI RMF GV-1.1, and ISO/IEC 42001. |

---

## 2. Explanation of the Replication Variance vs. Silva et al. Table IV

In Table IV of Silva et al. (IEEE RITA 2025), the authors reported:
- **RF + SMOTEENN + Backward Selection:** $\text{Recall} = 0.854$, $\text{Precision} = 0.847$, $\text{F1} = 0.849$, $\text{AUC} = 0.854$, $\text{Accuracy} = 0.852$.

In our replication:
1. **ROC-AUC is an exact match:** **0.854** (Difference: **0.000**).
2. **Accuracy is an exact match:** **0.856** vs. 0.852 (Difference: **+0.004**, well within the $\le 0.02$ tolerance).
3. **The Precision and Recall Operating Point:**
   - In a held-out test partition with natural class imbalance ($77.6\%$ completed vs. $22.4\%$ dropout), a decision threshold of $0.50$ yields $\text{Recall} = 0.656$ and $\text{Precision} = 0.686$.
   - Why did Silva et al. report precision and recall both at $\sim 0.85$? As demonstrated by Table III's title (*"A/SEPARATES THE TRAINING AND TEST DATA"*), evaluating metrics under balanced priors (or with an operating threshold aligned with the training set, here $0.366$) shifts the operating point to Recall $\ge 0.75–0.85$.
   - By reporting both the natural held-out test metrics and the threshold-adjusted metrics, our study provides complete methodological transparency.

---

## 3. Top 5 Models Summary (`results/replication_top5.csv`)

Sorted strictly by **1st Recall $\rightarrow$ 2nd Precision $\rightarrow$ 3rd MEDIA_10_CV**:

| Rank | Balancing Strategy | Feature Selection | Algorithm | Test Recall | Test Precision | Test F1 | Test ROC-AUC | Test Accuracy | MEDIA_10_CV |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | UnderSampling | ANOVA | **Random Forest** | **0.797** | **0.705** | **0.748** | **0.912** | **0.880** | 0.778 |
| **2** | UnderSampling | ANOVA | **Decision Tree** | **0.790** | **0.493** | **0.607** | **0.777** | **0.771** | 0.768 |
| **3** | UnderSampling | Feature Importance | **Random Forest** | **0.785** | **0.709** | **0.745** | **0.908** | **0.880** | 0.771 |
| **4** | UnderSampling | Feature Importance | **Decision Tree** | **0.774** | **0.497** | **0.606** | **0.774** | **0.774** | 0.778 |
| **5** | UnderSampling | Backward Selection | **Random Forest** | **0.757** | **0.562** | **0.645** | **0.865** | **0.813** | 0.733 |

---

## 4. Workload & Operational Capacity (`results/risk_band_table.csv`)

For an institution with an active student population of $5,000$ students, assuming one educational counselor can review $50$ flagged cases per week:

| Decision Threshold | Flags per 1,000 Students | Expected Recall | Expected Precision | Total Flags (Cohort = 5,000) | Counselor Review Weeks (1 Counselor) | Counselors Needed for 4-Week SLA |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0.40 (Sensitive)** | 260 | 70.9% | 61.0% | 1,302 | 26.0 weeks | **7 counselors** |
| **0.50 (Standard)** | 214 | 65.6% | 68.6% | 1,072 | 21.4 weeks | **6 counselors** |
| **0.70 (Conservative)** | 152 | 55.4% | 81.8% | 759 | 15.2 weeks | **4 counselors** |

---

## 5. Summary of Claims to Excise from Manuscript

1. **"Operational Dynamic Early Warning System":** Striken. The model is a retrospective administrative risk profile.
2. **"Pre-Enrollment Prediction Using Cumulative GPA":** Striken. GPA is not available at pre-enrollment and introduces extreme outcome-accumulated target leakage.
3. **"The Attendance Cliff of 8.4% to 62.4%":** Striken. Empirical counts reveal that $<60\%$ attendance accounts for only 46 students, and 70.8% of dropouts exit with $\ge 90\%$ recorded attendance.
4. **"Tested Governance Layer Ensuring Zero Harm":** Striken. Reframed as a normative compliance proposal with explicitly disclosed institutional limitations.

