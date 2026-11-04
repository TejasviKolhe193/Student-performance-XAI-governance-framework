# To-Do for Author - Verification Items & Placeholders

This document lists every **`[VERIFY]`** and **`[AUTHOR TO CONFIRM]`** placeholder remaining in the revised research paper (`research_paper_final_draft.docx`). Each item must be reviewed and resolved by the authors prior to final publication submission.

---

## 1. [AUTHOR TO CONFIRM] - Dataset Provenance & Institution (Section III-A)

The dataset is retained as Instituto Federal do Norte de Minas Gerais (IFNMG) (Case B):

| Item | Current In-Text Marker | Required Action |
|------|------------------------|-----------------|
| **Dataset Source & Access URL** | `[AUTHOR TO CONFIRM: Dataset URL, access terms, and licence]` | Provide the repository link or formal access procedure for IFNMG's `dataset_evasao_MDE.xlsx`. Do not copy Silva et al.'s IFMA link unless confirmed. |
| **Licence** | `[AUTHOR TO CONFIRM: ... licence]` | Confirm the legal licence governing the dataset. Do **not** state CC BY 4.0 (that applies to the journal article, not necessarily the raw administrative data). |
| **Cohort Date Range** | `[AUTHOR TO CONFIRM: Cohort date range]` | Specify the enrollment years covering the 15,084 students (e.g., 2012-2020). |
| **Exclusion Counts** | `[AUTHOR TO CONFIRM: Exclusion counts by reason]` | Verify the exact step-by-step attrition filtering from 48,311 total records down to 15,084 secondary technical records. |

---

## 2. [VERIFY] - Modality Counts and Percentages (Section III-A, IV-A & Fig. 2)

The modality counts and dropout rates in the paper reflect the locked pipeline data, but differ from Silva et al.'s Table I:

| Modality | Current Paper Count | Silva et al. (Table I) | Paper Dropout % | Required Action |
|----------|---------------------|------------------------|-----------------|-----------------|
| **Integrado** | 10,076 `[VERIFY]` | 10,070 | 16.7% `[VERIFY]` | Confirm against raw IFNMG spreadsheet |
| **Subsequente** | 2,746 `[VERIFY]` | 3,902 | 32.9% `[VERIFY]` | Confirm against raw IFNMG spreadsheet |
| **Concomitante** | 1,777 `[VERIFY]` | 718 | 34.3% `[VERIFY]` | Confirm against raw IFNMG spreadsheet |
| **Integrado EJA** | 485 `[VERIFY]` | 394 | 44.2% `[VERIFY]` | Confirm against raw IFNMG spreadsheet |

---

## 3. [VERIFY] - Replaced Literature References [9], [10], [11]

Original references [9], [10], [11] addressed unrelated topics (teacher appraisal in China, basic education informatization in China, physical education in China). They have been replaced with relevant student learning / performance evaluation papers from IEEE:

| Ref # | Original Reference | Revised Reference | Status |
|-------|--------------------|-------------------|--------|
| **[9]** | Y. Zhang & S. Yang (Teacher appraisal, AIoTCs 2022) | **O. Zughoul & F. Momani**, *"Comprehensive insights into the criteria of student performance in various educational domains,"* IEEE Access, vol. 6, pp. 73245-73264, 2018. | `[VERIFY]` - Confirm citation details |
| **[10]** | L. Zhou (Basic education informatization, AIoTCs 2022) | **S. Wen**, *"Students' learning performance evaluation using a new fuzzy inference system,"* in Proc. IEEE Int. Conf. Artif. Intell. Educ. (ICAIE), 2021, pp. 687-691. | `[VERIFY]` - Confirm citation details |
| **[11]** | R. Lu, G. Gao & Y. Xiang (Physical education, IEEE Access 2024) | **A. Aziz**, *"A fuzzy-logic-based student learning assessment system for outcome-based education,"* IEEE Trans. Educ., vol. 68, 2025. | `[VERIFY]` - Confirm citation details |

Table I (rows 9, 10, 11) has been updated to reflect these revised citations.

---

## 4. Key Governance & Fairness Confirmations (Author Sign-Off)

- **Fairness Claim Framing**: Gender Disparate Impact (DI = 0.7383) fails the Four-Fifths screening heuristic (0.80-1.25). The paper reports this neutrally as an administrative screening heuristic adapted from employment selection, not a legal test of education discrimination.
- **Equal Opportunity Parity**: Gender EOD is −0.0422 (p=0.1354, not statistically significant). Income (p=0.00043) and Home Computer Ownership (p=0.00089) exhibit statistically significant sensitivity gaps under Holm-Bonferroni correction. Race (Branca vs. Parda, raw p=0.0144) does **not** survive Holm correction.
- **Untested Governance**: All institutional governance components (RBAC, 5 pillars, counselor override, LGPD Art. 20 appeals) are explicitly described across the Abstract, Governance section, and Conclusion as **proposed designs, not field-tested in live operations**.
- **GPA Exclusion**: Cumulative GPA (`ira`) is completely removed from Abstract, Introduction, Research Questions, Contributions, and Conclusion, and is mentioned solely in Section III-A: *"Cumulative GPA (ira) was excluded because it is computed over the full enrollment and would leak outcome information."*
- **Page Count**: The paper length has been verified via Microsoft Word COM automation to be **exactly 6 pages** in IEEE two-column style.
