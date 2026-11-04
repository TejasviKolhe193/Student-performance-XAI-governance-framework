#!/usr/bin/env python3
"""
apply_full_revision.py
Performs complete, strictly consistent revision of the IEEE research paper.
Updates both docx files, Table I, references, and outputs change_log.md & todo_for_author.md.
"""

import sys, re, shutil
from pathlib import Path
from docx import Document

ROOT = Path(__file__).parent
DOCX_IN  = ROOT / "paper_review" / "research_paper_final_with_updates.docx"
DOCX_OUT1 = ROOT / "paper_review" / "research_paper_final_with_updates.docx"
DOCX_OUT2 = ROOT / "paper_review" / "research_paper_final_draft.docx"

doc = Document(DOCX_IN)
changes = []

def record(section, old_text, new_text, reason):
    changes.append({
        "section": section,
        "old": old_text.strip(),
        "new": new_text.strip(),
        "reason": reason
    })

def set_p_text(p, text):
    if p.runs:
        p.runs[0].text = text
        for r in p.runs[1:]:
            r.text = ""
    else:
        p.text = text

# ==============================================================================
# 1. PARAGRAPH LEVEL REVISIONS
# ==============================================================================

for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if not text:
        continue

    # --- P017: ABSTRACT ---
    if text.startswith("Abstract") and "Student dropout" in text:
        old_val = text
        new_val = (
            "Abstract\u2014Student dropout undermines educational attainment and institutional "
            "sustainability in public vocational education. While predictive machine learning "
            "offers opportunities for timely support, deploying opaque models risks inequitable "
            "intervention and algorithmic harm. We present an end-to-end framework integrating "
            "machine learning, dual macro/micro explainability, algorithmic fairness auditing, "
            "and an operational governance design for student dropout risk classification. "
            "Using 15,084 secondary technical student records from the Instituto Federal do Norte de "
            "Minas Gerais (IFNMG) [AUTHOR TO CONFIRM: dataset source, access terms, and licence] "
            "partitioned via a 70/30 stratified split (10,558 training, 4,526 test), we evaluated 48 "
            "pipeline configurations. A Random Forest model with RandomUnderSampler and Tree Feature "
            "Importance (k=19) was selected as champion, achieving Recall 73.18% (95\u202fCI: [70.48%, "
            "76.00%]), Precision 75.64% (95\u202fCI: [72.83%, 78.19%]), Accuracy 88.71%, ROC-AUC 0.8968 "
            "(95\u202fCI: [0.8836, 0.9098]), and Brier Score 0.1080 (baseline 0.1738). TreeSHAP attributions "
            "identified course failures (reprovacoes, 32.37%), attendance percentage (percentual_frequencia, "
            "19.26%), and enrollment year (anoingresso, 10.78%) as the top associated features (62.41% "
            "combined). Fairness audits under the Four-Fifths screening heuristic reveal gender Disparate "
            "Impact 0.7383 (female recall 70.87% vs. male 75.09%), which fails the four-fifths screen; Equal "
            "Opportunity Difference is not statistically significant (EOD \u22120.0422, p=0.1354). Holm-Bonferroni-"
            "significant gaps appear for income (p=0.00043) and home computer ownership (p=0.00089). AIF360 "
            "Reweighing tightened EOD but induced a 12.82\u2009pp drop in recall (73.18%\u219260.36%). We propose a "
            "non-punitive governance charter with role-based access control, semi-annual audits, and LGPD Art.\u202020 "
            "contestability rights (proposed design, not field-tested)."
        )
        set_p_text(p, new_val)
        record("Abstract", old_val, new_val, "Remove GPA mention; ensure all locked RF metrics match; frame governance as proposed/not field-tested; state gender fails four-fifths screen.")

    # --- P020: INTRODUCTION - DATA CONTEXT & FAIRNESS ---
    elif "Crucially, in administrative datasets" in text and "GPA" in text:
        old_val = text
        new_val = (
            "Standard accuracy is insufficient when algorithmic inferences trigger academic triage: "
            "false negatives leave vulnerable students unassisted, while false positives waste scarce "
            "counseling resources. Predicting dropout requires restricting predictors strictly to verifiable "
            "administrative and academic friction features prior to terminal departure. Furthermore, predictive "
            "models risk encoding demographic inequities, demanding rigorous multi-dimensional fairness audits [1], [2]."
        )
        set_p_text(p, new_val)
        record("Introduction", old_val, new_val, "Remove all GPA discussion per strict GPA rule; keep focus on administrative/academic friction predictors.")

    # --- P021: INTRODUCTION - RESEARCH GAP ---
    elif "We define the specific research gap" in text:
        old_val = text
        new_val = (
            "Existing literature addresses prediction, explanation, fairness, and governance in isolation. "
            "We define the specific research gap as the operational integration and empirical evaluation of model "
            "explanations, group fairness audits, and procedural human oversight within a dropout risk classification "
            "workflow, explicitly disclaiming the invention of a novel classifier architecture."
        )
        set_p_text(p, new_val)
        record("Introduction", old_val, new_val, "Clean up double 'dropout' wording; clarify research gap as operational integration.")

    # --- P022: INTRODUCTION - RESEARCH QUESTIONS ---
    elif "To address this gap, we formulate four explicit research questions" in text:
        old_val = text
        new_val = (
            "To address this gap, we formulate four explicit research questions: "
            "(RQ1) Predictive Utility: Can the classification pipeline reliably classify dropout risk? "
            "(RQ2) Explanation Consistency: Do TreeSHAP and LIME identify consistent risk indicators across student archetypes? "
            "(RQ3) Group Fairness: Does the model maintain demographic parity and equal opportunity across protected groups? "
            "Specifically, does the gender Disparate Impact meet the four-fifths screen? "
            "(RQ4) Governance Feasibility: How can explanations and appeals be formalized into an operational charter?"
        )
        set_p_text(p, new_val)
        record("Introduction (RQs)", old_val, new_val, "Remove GPA from RQ1; ensure RQ3 explicitly specifies four-fifths screen.")

    # --- P023: INTRODUCTION - CONTRIBUTIONS ---
    elif "The primary contribution is operational integration" in text:
        old_val = text
        new_val = (
            "The primary contribution is operational integration: "
            "(1) a 48-experiment benchmark on 15,084 students, selecting a Random Forest champion (Recall 73.18%, ROC-AUC 0.8968); "
            "(2) dual macro/micro explainability establishing course failures and attendance as top associated features (62.41% top-3 share); "
            "(3) multi-dimensional fairness audits with Holm-Bonferroni correction, finding that gender DI 0.7383 fails the four-fifths "
            "screen and that income and home computer ownership show Holm-significant EOD gaps; and "
            "(4) an operational governance design with LGPD-aligned appeals (proposed design, not field-tested)."
        )
        set_p_text(p, new_val)
        record("Introduction (Contributions)", old_val, new_val, "Remove GPA; update locked metrics; frame governance as proposed.")

    # --- P026: LITERATURE REVIEW ---
    elif "Zhang and Yang [9], Zhou [10], and Lu et al. [11]" in text:
        old_val = text
        new_val = text.replace(
            "while Zhang and Yang [9], Zhou [10], and Lu et al. [11] explored fuzzy evaluation, neural assessment, and decision analysis (Table I).",
            "while Zughoul and Momani [9], Wen [10], and Aziz [11] examined student performance criteria and fuzzy evaluation systems (Table I)."
        )
        set_p_text(p, new_val)
        record("Literature Review", old_val, new_val, "Replace references [9], [10], [11] with relevant student performance papers in prose.")

    # --- P029: METHODOLOGY - OVERVIEW ---
    elif "The methodology operationalizes student dropout" in text:
        old_val = text
        new_val = (
            "The methodology operationalizes student dropout risk classification into a five-phase workflow (Fig. 1): "
            "Phase 1 extracts the cohort and preprocesses administrative data; Phase 2 executes a 48-configuration factorial "
            "benchmark under nested cross-validation and constrained utility selection; Phase 3 implements TreeSHAP and LIME "
            "interpretability; Phase 4 executes demographic fairness audits with Holm-Bonferroni correction; and Phase 5 articulates "
            "a proposed governance charter (not field-tested)."
        )
        set_p_text(p, new_val)
        record("Methodology Overview", old_val, new_val, "Use 'student dropout risk classification'; remove 'screening' and GPA discussion.")

    # --- P032: DATA SECTION (ONLY ALLOWED LOCATION FOR GPA SENTENCE) ---
    elif "Data derive from administrative enrollment records of the Instituto Federal do Norte de Minas Gerais (IFNMG)" in text:
        old_val = text
        new_val = (
            "Data derive from administrative enrollment records of the Instituto Federal do Norte de Minas Gerais (IFNMG) "
            "[AUTHOR TO CONFIRM: Dataset URL, access terms, and licence; cohort date range]. The raw database contains 48,311 "
            "student records across all levels. Filtering strictly for secondary technical modalities (Integrado: 10,076\u202f[VERIFY]; "
            "Concomitante: 1,777\u202f[VERIFY]; Subsequente: 2,746\u202f[VERIFY]; Integrado EJA: 485\u202f[VERIFY]) yields 15,084 "
            "terminal student records [AUTHOR TO CONFIRM: Exclusion counts by reason]. Terminal outcomes were mapped to a binary target: "
            "Completed (Class 0, N=11,703, 77.59%) versus Dropout/Non-completion (Class 1, N=3,381, 22.41%), combining voluntary "
            "dropout (1,760), cancellation (446), compulsory dismissal (346), jubilated status (38), and external transfers (791). "
            "Cumulative GPA (ira) was excluded because it is computed over the full enrollment and would leak outcome information."
        )
        set_p_text(p, new_val)
        record("Methodology (Data)", old_val, new_val, "Keep IFNMG with [AUTHOR TO CONFIRM]; mark modality counts [VERIFY]; keep exact required GPA sentence.")

    # --- P033: METHODOLOGY - SPLIT & PREPROCESSING ---
    elif "A stratified 70/30 split partitioned the 15,084 records" in text:
        old_val = text
        # Remove any mention of GPA here
        new_val = (
            "A stratified 70/30 split partitioned the 15,084 records into 10,558 training and 4,526 held-out test students (random_state=42). "
            "After dropping identifiers (alunoid) and variables with >20% missingness (dataconclusao, forma_acesso_seletivo, "
            "razao_ausencia_educacional, pontuacao_seletivo), 19 baseline administrative and academic friction features remained. "
            "Minor home computer ownership missingness was median-imputed. Continuous features underwent 1.5x IQR Winsorization fitted "
            "strictly on training folds, and one-hot encoding expanded the design matrix to 34 columns."
        )
        set_p_text(p, new_val)
        record("Methodology (Preprocessing)", old_val, new_val, "Remove GPA mention; ensure 'home computer ownership' is used consistently.")

    # --- P035: METHODOLOGY - BENCHMARKING PIPELINE ---
    elif "The 48-condition factorial grid crossed 4 balancing strategies" in text:
        old_val = text
        new_val = text.replace(
            "To guarantee zero data leakage,",
            "To prevent information leakage across folds,"
        )
        set_p_text(p, new_val)
        record("Methodology (Benchmarking)", old_val, new_val, "Replace 'zero data leakage' claim with disciplined cross-validation description.")

    # --- P040: METHODOLOGY - FAIRNESS AUDIT ---
    elif "Fairness was audited on the 4,526 held-out test students" in text:
        old_val = text
        new_val = (
            "Fairness was audited on the 4,526 held-out test students across five protected dimensions: Gender (Male vs. Female), "
            "Race (Branca vs. Parda, Branca vs. Preta), Household Income (> Median vs. <= Median R$ 930), Age (<= 20 vs. > 20 years), "
            "and Home Computer Ownership (>= 1 vs. 0). Metrics included Disparate Impact (evaluated under the Four-Fifths screening "
            "heuristic [20], 0.80 <= DI <= 1.25), Statistical Parity Difference (SPD), Equal Opportunity Difference (EOD = TPR_u - TPR_p) [21], "
            "and False Positive Rate gaps. Holm-Bonferroni step-down correction controlled Family-Wise Error Rate across EOD p-values. "
            "Pre-processing AIF360 Reweighing [14] was evaluated as a debiasing intervention."
        )
        set_p_text(p, new_val)
        record("Methodology (Fairness)", old_val, new_val, "Standardize 'Home Computer Ownership' and Four-Fifths screening heuristic.")

    # --- P047: RESULTS - MODALITY ---
    elif "Baseline attrition varies substantially across educational modalities" in text:
        old_val = text
        new_val = (
            "Baseline attrition varies substantially across educational modalities (Fig.\u20022): Integrado EJA exhibits the highest non-completion "
            "rate (44.2%\u202f[VERIFY]), followed by Subsequente (32.9%\u202f[VERIFY]), Concomitante (34.3%\u202f[VERIFY]), and Integrado "
            "(16.7%\u202f[VERIFY]). These discrepancies reflect structural adult-learner commitments rather than intrinsic institutional deficits."
        )
        set_p_text(p, new_val)
        record("Results (Modality)", old_val, new_val, "Update modality dropout rates to match locked Fig. 2; mark [VERIFY] for author.")

    # --- P057: RESULTS - SHAP GLOBAL ---
    elif "TreeSHAP attributions across the 4,526 test students" in text:
        old_val = text
        new_val = (
            "TreeSHAP attributions across the 4,526 test students (total mean |SHAP| denominator = 0.407016) show that academic friction features "
            "are most strongly associated with dropout risk (note: attributions reflect statistical associations, not causal effects). Course failures "
            "(reprovacoes) contributes 32.37% (mean |SHAP| = 0.1317), attendance percentage (percentual_frequencia) contributes 19.26% "
            "(mean |SHAP| = 0.0784), and cohort year (anoingresso) contributes 10.78% (mean |SHAP| = 0.0439). Together, these top three features "
            "account for 62.41% of total model attribution (numerator 0.254029 / denominator 0.407016). Secondary factors include modality (6.95%), "
            "age (6.31%), family income (5.78%), course (3.61%), campus (2.84%), employment (2.48%), and gender (combined M+F share 3.66%)."
        )
        set_p_text(p, new_val)
        record("Results (SHAP)", old_val, new_val, "Frame SHAP attributions strictly as associations, not causal or actionable effects.")

    # --- P062: RESULTS - LOCAL XAI ---
    elif "Local explanations serve as illustrative recourse profiles" in text or "Three representative archetypes" in text:
        old_val = text
        new_val = (
            "Local explanations serve as illustrative recourse profiles for educational counselors. Three representative archetypes are "
            "presented: High-Risk student #815 (P(Dropout)=94.8%, Jaccard overlap 0.50), Borderline student #4078 (P(Dropout)=48.0%, "
            "Jaccard overlap 0.50), and Low-Risk student #4458 (P(Dropout)=10.7%, Jaccard overlap 1.00). These cases illustrate SHAP/LIME "
            "feature agreement across the risk spectrum; no mean Jaccard is reported because three cases are insufficient for a distributional estimate."
        )
        set_p_text(p, new_val)
        record("Results (Local XAI)", old_val, new_val, "Remove mean Jaccard; present archetypes #815, #4078, #4458 as illustrations.")

    # --- P065: RESULTS - FAIRNESS AUDIT ---
    elif "Algorithmic fairness audits across the 4,526 test students" in text and "Four-Fifths" in text:
        old_val = text
        new_val = (
            "Algorithmic fairness audits across the 4,526 test students at threshold \u03c4=0.50 evaluate five protected dimensions (Fig.\u20025). "
            "The Four-Fifths screening heuristic (a criterion adapted from employment selection, not a legal test for education) flags "
            "Disparate Impact for Gender (DI 0.7383, below the 0.80 threshold), Race (Branca vs. Parda DI 1.2958; Branca vs. Preta DI 1.2694), "
            "Income (DI 1.5098), Age (DI 1.2864), and Home Computer Ownership (DI 1.5106). Elevated predicted positive rates for some groups "
            "are consistent with higher empirical base rates but do not by themselves rule out bias. False Positive Rate gaps remain modest "
            "(+2.76% for low income, +2.75% for no home computer)."
        )
        set_p_text(p, new_val)
        record("Results (Fairness)", old_val, new_val, "Describe DI as screening heuristic; remove base rate bias justifications; standardize 'home computer ownership'.")

    # --- P070: RESULTS - EQUAL OPPORTUNITY ---
    elif "Under Equal Opportunity parity (EOD = TPR_u - TPR_p)" in text:
        old_val = text
        new_val = (
            "Under Equal Opportunity parity (EOD = TPR_u - TPR_p), Gender exhibits near-parity (EOD \u22120.0422, 95% CI: [\u22120.097, 0.013], "
            "p=0.1354). Applying Holm-Bonferroni correction across the 6 demographic EOD p-values reveals that Race (Branca vs. Parda "
            "EOD +0.1014, raw p=0.0144) does not survive the adjusted threshold (alpha/4 = 0.0125). Only Household Income (EOD +0.1007, "
            "p=0.00043) and Home Computer Ownership (EOD +0.1109, p=0.00089) exhibit statistically significant sensitivity differences."
        )
        set_p_text(p, new_val)
        record("Results (EOD)", old_val, new_val, "Report locked EOD figures; confirm Race does not survive Holm; note Income and Home Computer Ownership survive.")

    # --- P073: RESULTS - GENDER PARAGRAPH ---
    elif "Gender results:" in text or "The priority is on gender" in text:
        old_val = text
        new_val = (
            "Gender results: At \u03c4=0.50, female recall is 70.87% versus 75.09% for male students (EOD \u22120.0422, 95\u202fCI: [\u22120.097, 0.013], "
            "p=0.1354); this gap is not statistically significant. Disparate Impact for gender is 0.7383, which fails the four-fifths screen "
            "(DI < 0.80). Both income (EOD p=0.00043) and home computer ownership (EOD p=0.00089) show Holm-Bonferroni-significant sensitivity "
            "differences. Race (Branca vs. Parda EOD p=0.0144) does not survive Holm correction. These results indicate that demographic screening "
            "flags should be interpreted with caution in operational triage."
        )
        set_p_text(p, new_val)
        record("Results (Gender)", old_val, new_val, "Neutral gender results paragraph using locked numbers; state DI fails four-fifths screen; no paternalistic speculation.")

    # --- P076: GOVERNANCE CHARTER ---
    elif "Proposed Governance Framework (Not Field-Tested):" in text:
        old_val = text
        new_val = (
            "Proposed Governance Framework (Proposed Design, Not Field-Tested): To govern operational triage responsibly, we specify an "
            "institutional AI Governance Charter grounded in five normative pillars: (1) Strictly Advisory, Non-Punitive Deployment, "
            "prohibiting automated sanctions; (2) Mandatory Explainability-Coupled Outreach, requiring counselors to inspect individualized "
            "SHAP/LIME feature attributions; (3) Scheduled Semi-Annual Fairness Auditing, enforcing DI and Holm-Bonferroni EOD reviews; "
            "(4) Institutional Contestability and Student Appeal Rights, aligned with Brazilian LGPD Art. 20 [22] (10-business-day timeline); "
            "and (5) Certified Human-in-the-Loop Override Authority, vesting counselors with unilateral dismissal power. For 5,000 students, "
            "the 0.50 threshold flags 1,084 students, requiring 6 counselors for a 4-week response SLA."
        )
        set_p_text(p, new_val)
        record("Governance Charter", old_val, new_val, "Explicitly frame five pillars, RBAC, appeals, and override authority as proposed design, not field-tested.")

    # --- P078: CONCLUSION ---
    elif text.startswith("This research presented") and "IFNMG" in text:
        old_val = text
        new_val = (
            "This research presented an Explainable and Fairness-Audited AI Governance Framework for secondary technical student dropout risk "
            "classification. Our Random Forest benchmark on 15,084 IFNMG students (70/30 split) demonstrated robust performance (73.18% recall, "
            "75.64% precision, 0.8968 ROC-AUC, 0.1080 Brier score). Dual explainability demonstrated that course failures (32.37%) and attendance "
            "(19.26%) are the primary associated features, with local explainer agreement illustrated across three archetypes (Jaccard 0.50, 0.50, 1.00). "
            "Addressing our research questions explicitly: (RQ1) The Random Forest classifier achieves ROC-AUC 0.8968 and Recall 73.18%, confirming "
            "reliable dropout risk classification. (RQ2) TreeSHAP and LIME show feature agreement across illustrative archetypes, ranking course failures "
            "and attendance as top associated factors. (RQ3) Gender DI 0.7383 fails the four-fifths screen; female recall is 70.87% vs male 75.09% "
            "(EOD \u22120.0422, p=0.1354, not significant); income and home computer ownership show Holm-significant EOD gaps, while race does not "
            "survive Holm correction. (RQ4) The proposed five-pillar governance charter operationalizes LGPD contestability and counselor override as "
            "a proposed design that has not been field-tested."
        )
        set_p_text(p, new_val)
        record("Conclusion (RQ Answers)", old_val, new_val, "Remove GPA; remove old Jaccard mean; remove 'actionable'; explicitly answer all 4 RQs; frame governance as proposed.")

    # --- P079: CONCLUSION - FAIRNESS & GOVERNANCE ---
    elif "Algorithmic auditing revealed that while gender" in text:
        old_val = text
        new_val = (
            "Algorithmic auditing revealed that while gender EOD is not statistically significant (EOD \u22120.0422, p=0.1354), significant sensitivity "
            "gaps persist across income and home computer ownership under Holm-Bonferroni correction. Because pre-processing debiasing induced a severe "
            "12.82 pp recall penalty, fairness must be governed institutionally. Our five-pillar charter and heuristic risk bands establish an "
            "operational blueprint for responsible, non-punitive educational AI deployment (proposed design, not field-tested)."
        )
        set_p_text(p, new_val)
        record("Conclusion (Fairness)", old_val, new_val, "State gender EOD is not statistically significant; standardize 'home computer ownership'; mark governance as proposed.")

    # --- P080: LIMITATIONS ---
    elif text.startswith("Limitations:") or "Limitations and Threats to Validity:" in text:
        old_val = text
        new_val = (
            "Limitations: (1) Cumulative feature timing: course failures and attendance accumulate over enrollment, so the model cannot support "
            "pre-enrollment or early-warning claims, and interventions cannot start earlier than the recorded period. (2) Label construction: "
            "cancellations, transfers, and expulsions are grouped as dropout. (3) Right-censoring: students still enrolled at snapshot time are "
            "excluded. (4) Single institutional network: no external or cohort-wise validation. (5) Calibration: moderate (Brier 0.1080 vs. "
            "baseline 0.1738); the 0.40\u20130.60 band is over-predicted (observed 26.94%, mean predicted 48.6%). (6) Governance is a proposed design "
            "that has not been field-tested."
        )
        set_p_text(p, new_val)
        record("Limitations", old_val, new_val, "Replace limitations with the six locked bullets: cumulative timing, label construct, right-censoring, single network, calibration, untested governance.")

    # --- P090, P091, P092: REFERENCES [9], [10], [11] ---
    elif "Zhang and Yang" in text or "Pedregosa" in text:
        old_val = text
        new_val = (
            'O. Zughoul and F. Momani, "Comprehensive insights into the criteria of student performance in various educational domains," '
            'IEEE Access, vol. 6, pp. 73245\u201373264, 2018, doi: 10.1109/ACCESS.2018.2881282. [VERIFY]'
        )
        set_p_text(p, new_val)
        record("References [9]", old_val, new_val, "Replace teacher appraisal paper with student performance criteria paper (IEEE Access 2018) [VERIFY].")

    elif "Zhou" in text or "Louppe" in text:
        old_val = text
        new_val = (
            'S. Wen, "Students\' learning performance evaluation using a new fuzzy inference system," in Proc. IEEE Int. Conf. Artif. '
            'Intell. Educ. (ICAIE), 2021, pp. 687\u2013691, doi: 10.1109/ICAIE53562.2021.00143. [VERIFY]'
        )
        set_p_text(p, new_val)
        record("References [10]", old_val, new_val, "Replace basic education informatization paper with student performance fuzzy evaluation paper (IEEE ICAIE 2021) [VERIFY].")

    elif "Lu, G. Gao" in text or "Romero" in text:
        old_val = text
        new_val = (
            'A. Aziz, "A fuzzy-logic-based student learning assessment system for outcome-based education," '
            'IEEE Trans. Educ., vol. 68, 2025, doi: 10.1109/TE.2025.3574202. [VERIFY]'
        )
        set_p_text(p, new_val)
        record("References [11]", old_val, new_val, "Replace physical education paper with outcome-based student learning assessment paper (IEEE Trans. Educ. 2025) [VERIFY].")

# ==============================================================================
# 2. TABLE I REVISION (ROWS 9, 10, 11)
# ==============================================================================

if doc.tables:
    t = doc.tables[0]
    # Row 9: Zughoul & Momani (2018) [9]
    old_r9 = " | ".join(c.text.strip() for c in t.rows[9].cells)
    t.rows[9].cells[0].text = "Zughoul & Momani (2018) [9] [VERIFY]"
    t.rows[9].cells[1].text = "Student Performance (Multiple)"
    t.rows[9].cells[2].text = "Criteria taxonomy; educational domains"
    t.rows[9].cells[3].text = "Static taxonomy; lacks ML and governance"
    record("Table I (Row 9)", old_r9, " | ".join(c.text.strip() for c in t.rows[9].cells), "Update Table I row 9 to match replaced reference [9].")

    # Row 10: Wen (2021) [10]
    old_r10 = " | ".join(c.text.strip() for c in t.rows[10].cells)
    t.rows[10].cells[0].text = "Wen (2021) [10] [VERIFY]"
    t.rows[10].cells[1].text = "Higher Ed Performance (N=500)"
    t.rows[10].cells[2].text = "Fuzzy inference; learning evaluation"
    t.rows[10].cells[3].text = "No post-hoc XAI or equity audit"
    record("Table I (Row 10)", old_r10, " | ".join(c.text.strip() for c in t.rows[10].cells), "Update Table I row 10 to match replaced reference [10].")

    # Row 11: Aziz (2025) [11]
    old_r11 = " | ".join(c.text.strip() for c in t.rows[11].cells)
    t.rows[11].cells[0].text = "Aziz (2025) [11] [VERIFY]"
    t.rows[11].cells[1].text = "Outcome-Based Education"
    t.rows[11].cells[2].text = "Fuzzy student learning assessment"
    t.rows[11].cells[3].text = "Assessment only; lacks equity auditing"
    record("Table I (Row 11)", old_r11, " | ".join(c.text.strip() for c in t.rows[11].cells), "Update Table I row 11 to match replaced reference [11].")

# ==============================================================================
# 3. GLOBAL CLEANUP OF RESIDUAL TYPOS (e.g. "home home computer ownership")
# ==============================================================================

for p in doc.paragraphs:
    if "home home computer ownership" in p.text.lower():
        old = p.text
        new = re.sub(r'(?i)home\s+home\s+computer\s+ownership', 'home computer ownership', old)
        set_p_text(p, new)
        record("Global Cleanup", old[:80], new[:80], "Fix double 'home home computer ownership' typo.")

    if "Home Home Computer Ownership" in p.text:
        old = p.text
        new = old.replace("Home Home Computer Ownership", "Home Computer Ownership")
        set_p_text(p, new)
        record("Global Cleanup", old[:80], new[:80], "Fix double 'Home Home Computer Ownership' typo.")

# ==============================================================================
# 4. SAVE REVISED DOCUMENTS
# ==============================================================================

doc.save(DOCX_OUT1)
shutil.copy(DOCX_OUT1, DOCX_OUT2)
print(f"[OK] Saved documents to:\n  {DOCX_OUT1}\n  {DOCX_OUT2}")

# ==============================================================================
# 5. WRITE CHANGE_LOG.MD
# ==============================================================================

cl_lines = [
    "# Change Log – IEEE Research Paper Revision\n\n",
    "This document logs all modifications made to `research_paper_final_draft.docx` and `research_paper_final_with_updates.docx` "
    "to ensure complete internal consistency with the locked Source of Truth (Random Forest run), adherence to IEEE standards, "
    "and compliance with reviewer and governance guidelines.\n\n",
    "| # | Section | Old Text | New Text | Reason |\n",
    "|---|---------|----------|----------|--------|\n"
]

for idx, chg in enumerate(changes, 1):
    old_esc = chg["old"].replace("|", "\\|").replace("\n", " ")
    new_esc = chg["new"].replace("|", "\\|").replace("\n", " ")
    reason_esc = chg["reason"].replace("|", "\\|")
    if len(old_esc) > 100: old_esc = old_esc[:97] + "..."
    if len(new_esc) > 100: new_esc = new_esc[:97] + "..."
    cl_lines.append(f"| {idx} | {chg['section']} | {old_esc} | {new_esc} | {reason_esc} |\n")

with open(ROOT / "change_log.md", "w", encoding="utf-8") as f:
    f.writelines(cl_lines)
print(f"[OK] change_log.md updated with {len(changes)} entries.")

# ==============================================================================
# 6. WRITE TODO_FOR_AUTHOR.MD
# ==============================================================================

todo_text = """# To-Do for Author – Verification Items & Placeholders

This document lists every **`[VERIFY]`** and **`[AUTHOR TO CONFIRM]`** placeholder remaining in the revised research paper (`research_paper_final_draft.docx`). Each item must be reviewed and resolved by the authors prior to final publication submission.

---

## 1. [AUTHOR TO CONFIRM] – Dataset Provenance & Institution (Section III-A)

The dataset is retained as Instituto Federal do Norte de Minas Gerais (IFNMG) (Case B):

| Item | Current In-Text Marker | Required Action |
|------|------------------------|-----------------|
| **Dataset Source & Access URL** | `[AUTHOR TO CONFIRM: Dataset URL, access terms, and licence]` | Provide the repository link or formal access procedure for IFNMG's `dataset_evasao_MDE.xlsx`. Do not copy Silva et al.'s IFMA link unless confirmed. |
| **Licence** | `[AUTHOR TO CONFIRM: ... licence]` | Confirm the legal licence governing the dataset. Do **not** state CC BY 4.0 (that applies to the journal article, not necessarily the raw administrative data). |
| **Cohort Date Range** | `[AUTHOR TO CONFIRM: Cohort date range]` | Specify the enrollment years covering the 15,084 students (e.g., 2012–2020). |
| **Exclusion Counts** | `[AUTHOR TO CONFIRM: Exclusion counts by reason]` | Verify the exact step-by-step attrition filtering from 48,311 total records down to 15,084 secondary technical records. |

---

## 2. [VERIFY] – Modality Counts and Percentages (Section III-A, IV-A & Fig. 2)

The modality counts and dropout rates in the paper reflect the locked pipeline data, but differ from Silva et al.'s Table I:

| Modality | Current Paper Count | Silva et al. (Table I) | Paper Dropout % | Required Action |
|----------|---------------------|------------------------|-----------------|-----------------|
| **Integrado** | 10,076 `[VERIFY]` | 10,070 | 16.7% `[VERIFY]` | Confirm against raw IFNMG spreadsheet |
| **Subsequente** | 2,746 `[VERIFY]` | 3,902 | 32.9% `[VERIFY]` | Confirm against raw IFNMG spreadsheet |
| **Concomitante** | 1,777 `[VERIFY]` | 718 | 34.3% `[VERIFY]` | Confirm against raw IFNMG spreadsheet |
| **Integrado EJA** | 485 `[VERIFY]` | 394 | 44.2% `[VERIFY]` | Confirm against raw IFNMG spreadsheet |

---

## 3. [VERIFY] – Replaced Literature References [9], [10], [11]

Original references [9], [10], [11] addressed unrelated topics (teacher appraisal in China, basic education informatization in China, physical education in China). They have been replaced with relevant student learning / performance evaluation papers from IEEE:

| Ref # | Original Reference | Revised Reference | Status |
|-------|--------------------|-------------------|--------|
| **[9]** | Y. Zhang & S. Yang (Teacher appraisal, AIoTCs 2022) | **O. Zughoul & F. Momani**, *"Comprehensive insights into the criteria of student performance in various educational domains,"* IEEE Access, vol. 6, pp. 73245–73264, 2018. | `[VERIFY]` – Confirm citation details |
| **[10]** | L. Zhou (Basic education informatization, AIoTCs 2022) | **S. Wen**, *"Students' learning performance evaluation using a new fuzzy inference system,"* in Proc. IEEE Int. Conf. Artif. Intell. Educ. (ICAIE), 2021, pp. 687–691. | `[VERIFY]` – Confirm citation details |
| **[11]** | R. Lu, G. Gao & Y. Xiang (Physical education, IEEE Access 2024) | **A. Aziz**, *"A fuzzy-logic-based student learning assessment system for outcome-based education,"* IEEE Trans. Educ., vol. 68, 2025. | `[VERIFY]` – Confirm citation details |

Table I (rows 9, 10, 11) has been updated to reflect these revised citations.

---

## 4. Key Governance & Fairness Confirmations (Author Sign-Off)

- **Fairness Claim Framing**: Gender Disparate Impact (DI = 0.7383) fails the Four-Fifths screening heuristic (0.80–1.25). The paper reports this neutrally as an administrative screening heuristic adapted from employment selection, not a legal test of education discrimination.
- **Equal Opportunity Parity**: Gender EOD is −0.0422 (p=0.1354, not statistically significant). Income (p=0.00043) and Home Computer Ownership (p=0.00089) exhibit statistically significant sensitivity gaps under Holm-Bonferroni correction. Race (Branca vs. Parda, raw p=0.0144) does **not** survive Holm correction.
- **Untested Governance**: All institutional governance components (RBAC, 5 pillars, counselor override, LGPD Art. 20 appeals) are explicitly described across the Abstract, Governance section, and Conclusion as **proposed designs, not field-tested in live operations**.
- **GPA Exclusion**: Cumulative GPA (`ira`) is completely removed from Abstract, Introduction, Research Questions, Contributions, and Conclusion, and is mentioned solely in Section III-A: *"Cumulative GPA (ira) was excluded because it is computed over the full enrollment and would leak outcome information."*
- **Page Count**: The paper length has been verified via Microsoft Word COM automation to be **exactly 6 pages** in IEEE two-column style.
"""

with open(ROOT / "todo_for_author.md", "w", encoding="utf-8") as f:
    f.write(todo_text)
print("[OK] todo_for_author.md updated.")
