# To-Do for Author - Remaining Verification & Confirmation Items

This document lists all remaining **`[AUTHOR TO CONFIRM]`** and **`[VERIFY]`** placeholders in `research_paper_final_with_updates.docx` and `research_paper_final_draft.docx`.

---

## 1. [AUTHOR TO CONFIRM] Placeholders

| # | Section | In-Text Placeholder | Context & Required Action |
|---|---|---|---|
| **1** | Abstract & Section III-A | `[AUTHOR TO CONFIRM: access terms and licence]` | The public dataset of Silva et al. [1] (IFMA) is hosted at `https://bit.ly/case-sutdy-dropout-xai`. The author must verify and insert the official access terms and data licence governing this public dataset. Do not state CC BY 4.0 unless specifically licensed for the data. |
| **2** | Section III-B (Phase 2) | `[AUTHOR TO CONFIRM: tuning method]` | Champion Random Forest hyperparameters are `n_estimators=100, max_depth=10, min_samples_leaf=5`. The author should confirm whether these were selected via grid search, cross-validated randomized search, or heuristic selection. |
| **3** | Section III-C (Phase 3) | `[AUTHOR TO CONFIRM: SHAP output scale and background set]` | The text describes TreeSHAP evaluated on the probability scale over 800 background instances. The author should confirm whether the production pipeline used path-dependent tree traversal (no background) or a sampled background set, and verify whether outputs were probability scale or log-odds. |
| **4** | Section IV-E (Phase 5) | `[AUTHOR TO CONFIRM: counselor caseload and staffing ratio]` | For 5,000 students, the 0.50 threshold yields 1,084 flags ($5,000 \times 21.68\% = 1,084$ flags). The author should confirm the target counselor caseload (e.g. ~180 students per counselor) and institutional staffing ratio under the 4-week response SLA. |

---

## 2. [VERIFY] Placeholders

| # | Section | In-Text Placeholder | Context & Required Action |
|---|---|---|---|
| **1** | Section IV-B (Results) | `continuous ROC-AUC 0.5945 [VERIFY]` | Continuous ROC-AUC for the attendance-only heuristic baseline. Keep marked with `[VERIFY]` until explicitly recomputed with `roc_auc_score` on the raw continuous attendance values. |
| **2** | Section IV-B (Results) | `0.9144 [VERIFY]` | Training 10-fold cross-validation ROC-AUC for the champion Random Forest (`CV Recall 74.95%, CV Precision 76.94%, CV ROC-AUC 0.9144`). Present in `results/step2_candidate_models_comparison.csv` (row 0). Keep marked with `[VERIFY]` until the author confirms `step2_candidate_models_comparison.csv` as the final run. |
| **3** | Section IV-D (Results) | `−0.0304 [VERIFY]` | Gender Equal Opportunity Difference under AIF360 Reweighing (reported as shifting from −0.0422 to −0.0304). Confirm value against the final mitigation audit run. |

---

## 3. Author Action Note: References [9], [10], [11]

- **Status**: The `[VERIFY]` tags have been removed from references [9] (Zughoul & Momani 2018), [10] (Wen 2021), and [11] (Aziz 2025) in Table I and the References section.
- **Required Author Replacement**: These references address student learning criteria and fuzzy evaluation in education, but they do **not** support explainable AI (XAI) or student dropout prediction claims. The author should substitute them with relevant publications from the educational data mining / XAI literature (e.g. papers on TreeSHAP in educational settings or student attrition forecasting) prior to camera-ready submission.
