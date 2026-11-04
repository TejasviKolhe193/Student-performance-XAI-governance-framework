import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, hex_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

doc = docx.Document()

# 1 inch margins all around
for s in doc.sections:
    s.top_margin = Inches(1.0)
    s.bottom_margin = Inches(1.0)
    s.left_margin = Inches(1.0)
    s.right_margin = Inches(1.0)

# Title
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_title = p_title.add_run("Response Sheet to Reviewer Comments and Suggestions")
r_title.font.name = 'Calibri'
r_title.font.size = Pt(18)
r_title.font.bold = True
r_title.font.color.rgb = RGBColor(24, 43, 73)
p_title.paragraph_format.space_after = Pt(2)

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_sub = p_sub.add_run("Itemized Tabular Register of Exact Reviewer Suggestions and Corrections Made")
r_sub.font.name = 'Calibri'
r_sub.font.size = Pt(11)
r_sub.font.italic = True
r_sub.font.color.rgb = RGBColor(80, 95, 110)
p_sub.paragraph_format.space_after = Pt(14)

# Metadata Card
meta_t = doc.add_table(rows=3, cols=2)
meta_t.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("Manuscript Title:", "An Explainable and Fairness-Audited AI Governance Framework for Student Dropout Prediction"),
    ("Base Benchmark:", "Silva et al., IEEE Latin America Transactions / RITA (2025)"),
    ("Evaluation Cohort:", "15,084 Secondary Technical Students (IFMA Public Data; 3,017 Held-Out Test Set: TP=573, FP=112, TN=2,229, FN=103)")
]
for idx, (k, v) in enumerate(meta_data):
    r = meta_t.rows[idx]
    c0, c1 = r.cells[0], r.cells[1]
    c0.width, c1.width = Inches(1.8), Inches(4.7)
    
    p0 = c0.paragraphs[0]
    run0 = p0.add_run(k)
    run0.font.bold = True
    run0.font.name = 'Calibri'
    run0.font.size = Pt(9.5)
    run0.font.color.rgb = RGBColor(24, 43, 73)
    set_cell_background(c0, "EEF2F6")
    set_cell_margins(c0, 50, 50, 80, 80)
    
    p1 = c1.paragraphs[0]
    run1 = p1.add_run(v)
    run1.font.name = 'Calibri'
    run1.font.size = Pt(9.5)
    set_cell_background(c1, "F8FAFC")
    set_cell_margins(c1, 50, 50, 80, 80)

doc.add_paragraph().paragraph_format.space_after = Pt(12)

# Heading 1: Section-by-Section Exact Table
p_h1 = doc.add_paragraph()
r_h1 = p_h1.add_run("1. Point-by-Point Responses to Reviewer Suggestions (Sections 1–14)")
r_h1.font.name = 'Calibri'
r_h1.font.size = Pt(14)
r_h1.font.bold = True
r_h1.font.color.rgb = RGBColor(24, 43, 73)
p_h1.paragraph_format.space_after = Pt(6)

# Exact suggestions and corrections mapping
suggestions = [
    # 1. Title
    ("1. Title", 
     "Clarify that the outcome is student dropout prediction rather than general student performance evaluation.",
     "Corrected manuscript title to explicitly specify student dropout prediction: 'An Explainable and Fairness-Audited AI Governance Framework for Student Dropout Prediction'. Updated title block in research_paper_final_draft.docx."),
    ("1. Title", 
     "Consider “An Explainable and Fairness-Audited AI Governance Framework for Student Dropout Prediction”; avoid implying an implemented institutional system.",
     "Adopted the exact suggested title verbatim: 'An Explainable and Fairness-Audited AI Governance Framework for Student Dropout Prediction'. Removed all phrasing implying a previously implemented or deployed institutional system, clarifying that the governance charter is a proposed operational policy framework."),
    
    # 2. Abstract
    ("2. Abstract", 
     "Distinguish experimentally evaluated prediction, explanation and fairness from the proposed (not field-tested) governance charter.",
     "Updated Abstract to explicitly distinguish empirical phases from prospective policy: model benchmarking (84.8% recall, 83.6% precision, 0.951 AUC), TreeSHAP/LIME explanation (71.3% attribution share), and fairness audits are labeled as experimentally evaluated on the 3,017 test set, while the five-pillar institutional governance charter is explicitly defined as a proposed operational framework designed for institutional adoption."),
    ("2. Abstract", 
     "Report the exact data source, split, selected model and key test metrics consistently; avoid describing audit results as proof of fairness.",
     "Harmonized all metrics in Abstract: data source specified as Brazilian Federal Institutes (IFMA, 2014–2020; N=15,084); exact 80/20 stratified split (12,067 train, 3,017 test); selected model defined as Random Forest with SMOTE; key metrics confirmed as 84.8% recall (95% CI [82.0%, 87.4%]), 83.6% precision, 92.9% accuracy, 0.951 ROC-AUC, TP=573, FP=112, TN=2,229, FN=103. Removed claims of 'proof of fairness' and replaced with empirical disparity reporting."),
    ("2. Abstract", 
     "State gender disparity (DI 0.707 and recall gap) and the need for follow-up analysis rather than claiming all other differences are harmless.",
     "Abstract now explicitly highlights the gender disparity: Disparate Impact of 0.707 (breaching the 80% rule) and female sensitivity gap of -5.73 percentage points (female recall 81.7% vs. male recall 87.4%), noting the need for post-hoc threshold adjustment (tau=0.44) and continuous institutional oversight."),

    # 3. Introduction
    ("3. Introduction", 
     "Define the specific research gap as operational integration and evaluation of explanations, group fairness and human oversight not invention of a new classifier.",
     "Revised Section I (paragraphs 20–23) to explicitly articulate the research gap as the lack of operational integration connecting predictive algorithms, local/global explainability, demographic fairness audits, and procedural governance, explicitly disclaiming the invention of a new classifier architecture."),
    ("3. Introduction", 
     "Clarify the intended prediction time: first-year GPA, failures and attendance cannot support a pre-enrollment prediction claim.",
     "Replaced all 'pre-enrollment' statements across Section I and Section III with 'first-year early warning dropout screening', clarifying that the model operates at the conclusion of the first academic year utilizing first-year GPA, accumulated course failures, and attendance patterns."),
    ("3. Introduction", 
     "State explicit research questions for predictive performance, explanation consistency, group fairness and governance feasibility.",
     "Explicitly formulated four operational research objectives in Section I-B: (1) Predictive utility under precision-constrained triage; (2) Local/global explainability concordance; (3) Demographic fairness and proxy auditing under Brazilian LGPD; and (4) Governance policy feasibility via calibrated risk bands."),
    ("3. Introduction", 
     "Distinguish SDG alignment as motivation from measured progress toward SDG 4 or SDG 10.",
     "Re-framed SDG references in Section I to serve solely as conceptual institutional motivations rather than claiming empirically measured societal progress toward UNESCO SDG 4 or SDG 10."),

    # 4. Literature Review
    ("4. Literature Review", 
     "Recheck claims that prior papers lack explainability: the text itself identifies SHAP/LIME in Silva et al. [1]. Specify what this work actually adds.",
     "Clarified Section II: acknowledged that Silva et al. [1] utilized SHAP and LIME for feature attribution, and explicitly highlighted our incremental contributions: (1) systematic algorithmic fairness audits across five demographic axes; (2) probability calibration with Brier scoring; (3) explanation stability audits; and (4) an actionable five-pillar institutional governance policy charter."),
    ("4. Literature Review", 
     "Make Table I compare dataset, task, sample size, explanation, fairness metrics, human oversight and validation, using verifiable evidence.",
     "Revised Table I to include verifiable metadata for all 11 surveyed papers: Study & Citation, Domain & Sample Size (e.g., IFMA Brazil N=15,084, Italy Higher Ed N=7,000, US Admissions N=12,000), Key Findings & Methods, and Gaps Addressed (demographic fairness, human oversight, appeal mechanisms)."),
    ("4. Literature Review", 
     "Avoid treating results from different datasets as direct performance comparisons; verify bibliographic metadata and DOI details.",
     "Updated Section II narrative to clarify that accuracy and recall metrics across surveyed papers reflect distinct educational contexts, cohorts, and curricula, avoiding direct performance equivalence claims. Audited and corrected all bibliographic citations [1]–[11]."),
    ("4. Literature Review", 
     "Explain why disparate impact, equal opportunity and calibration may conflict, and specify the chosen audit priorities.",
     "Added explicit discussion in Section II and Section III-D on the mathematical impossibility theorem of fairness (Kleinberg et al. [14]): demographic parity (DI) and equal opportunity (EOD) naturally conflict when base dropout rates differ across demographic groups (female 19.4% vs male 25.8%), establishing equal sensitivity as our primary operational priority."),

    # 5. Dataset Description and Exploratory Analysis
    ("5. Dataset Description and Exploratory Analysis", 
     "Document dataset access, cohort dates, definitions of dropout/completion, missing-value exclusion, variables and any permissions or licensing.",
     "Documented dataset provenance in Section III-A: extracted from the Brazilian Federal Institutes public administrative database (2014–2020), defining Class 0 as Completed/Graduated and Class 1 as Dropout/Evasao (including course cancellation and institutional transfer), governed by Brazil's open data licensing."),
    ("5. Dataset Description and Exploratory Analysis", 
     "Explain how 48,311 initial records become 15,084 analyzed records; report exclusion counts by reason and potential selection bias.",
     "Audited and documented the full two-stage dataset attrition provenance in Section III-A: Initial database = 48,311 records $\rightarrow$ Modality Filter: excluded 12,038 higher education records, retaining 36,273 secondary technical students across four formats $\rightarrow$ Status Filter: excluded 21,189 active ongoing students (Matriculado/Trancado), yielding exactly N=15,084 finalized students (11,703 Completed, 3,381 Dropout; majority baseline 77.6%). Saved detailed breakdown in phase1_outputs/dataset_attrition_provenance.csv."),
    ("5. Dataset Description and Exploratory Analysis", 
     "Clarify whether transfers and expulsion are appropriately grouped with dropout, and consider sensitivity analysis with alternative outcome definitions.",
     "Clarified outcome definition in Section III-A: institutional transfers and official cancellations represent school-level attrition requiring counselor intervention, matching the ground-truth target construct established by Silva et al. [1]."),
    ("5. Dataset Description and Exploratory Analysis", 
     "Reconcile the “2,722 active, non-zero GPA” subset with the 3,017-person test set; specify which analyses use each subset.",
     "Reconciled the cohort slices in Section IV-A: the 3,017 held-out test set comprises 2,722 active enrolled students (GPA > 0; recall 80.8%, precision 82.5%) and 295 post-mortem records (GPA = 0; recall 95.2%, precision 86.3%). Confirmed all primary benchmark metrics evaluate the complete, unselected 3,017 test set. Saved in phase2_outputs/active_vs_postmortem_audit.csv."),
    ("5. Dataset Description and Exploratory Analysis", 
     "Verify subgroup sizes and denominators for modality, attendance, digital access and protected attributes; avoid causal claims about adults or economic pressure.",
     "Audited all subgroup sample sizes in Section IV-A: Integrado (N=10,076; 16.4% dropout), Concomitante (N=864; 27.8%), Subsequente (N=3,334; 31.2%), PROEJA (N=810; 36.4%). Removed speculative causal claims regarding economic stress, framing findings purely as empirical observational correlations."),

    # 6. Proposed Methodology
    ("6. Proposed Methodology", 
     "Give a reproducible 48-experiment grid (4 balancing × 3 feature selection × 4 classifiers), including every configuration and selection rule.",
     "Documented full factorial design in Section III-B: 4 classifiers (Random Forest, SVM, Decision Tree, Logistic Regression) $\times$ 3 resampling strategies (None, SMOTE, Under-sampling) $\times$ 4 preprocessing pipelines = 48 configurations, trained strictly on training folds under 5-fold cross-validation. Detailed in phase2_outputs/model_selection_utility_tradeoff.csv."),
    ("6. Proposed Methodology", 
     "Explain the statement “grid search with 5-fold CV and tested using 10-fold CV”: define nesting, model-selection stage and held-out evaluation to rule out leakage.",
     "Clarified validation architecture in Section III-B: hyperparameter tuning was conducted using nested 5-fold cross-validated grid search strictly within training folds; 10-fold cross-validation audited model stability; final reported metrics were scored once on the untouched 3,017 held-out test partition."),
    ("6. Proposed Methodology", 
     "Fit winsorization bounds, imputers, encoders, feature selection and resampling on training folds only; report handling of categorical variables for SMOTE/SMOTEENN.",
     "Documented strict data leakage controls in Section III-B: median imputers, standard scalers, one-hot encoders, and SMOTE resampling were fitted exclusively on training folds and applied transform-only to validation/test folds."),
    ("6. Proposed Methodology", 
     "Describe exact feature list, hyperparameter ranges, decision threshold, class labels, random seeds, software versions and data/code availability.",
     "Documented specifications in Section III-B: 15 features across academic, sociodemographic, and institutional modalities; Random Forest champion tuned to n_estimators=100, max_depth=12, min_samples_split=5; decision threshold tau=0.50; random seed 42; Python 3.11, scikit-learn 1.4, AIF360 0.6.1."),
    ("6. Proposed Methodology", 
     "Define whether risk bands (<0.40, 0.40–0.70, >0.70) are calibrated probabilities and how thresholds were chosen.",
     "Validated probability calibration in Section III-E and Section IV-E: Random Forest probabilities achieve a Brier score of 0.0526 (69.7% skill score over prevalence baseline 0.1738). Risk bands empirically map to: Tier 1 Safe (<0.40; empirical dropout 4.2%), Tier 2 Watchlist (0.40–0.70; empirical dropout 20.4%), and Tier 3 Urgent (>0.70; empirical dropout 91.2%)."),

    # 7. Experimental Setup and Validation
    ("7. Experimental Setup and Validation", 
     "Provide the confusion matrix and positive-class counts for 3,017 held-out students; verify precision, recall, F1 and accuracy from the same counts.",
     "Reported full 2x2 contingency matrix for the 3,017 test set in Section IV-B (paragraph 54): TP=573, FP=112, TN=2,229, FN=103. Verified all derived metrics: Recall = 573/676 = 84.76%, Precision = 573/685 = 83.65%, Specificity = 2,229/2,341 = 95.22%, Accuracy = 2,802/3,017 = 92.87%, F1 = 0.8420. Saved in phase2_outputs/rf_champion_confusion_matrix.csv."),
    ("7. Experimental Setup and Validation", 
     "Add a majority-class baseline, a simple GPA/attendance baseline and confidence intervals or bootstrap intervals for key metrics.",
     "Implemented and reported benchmark baselines in Section IV-B: (1) Majority-class baseline: 0.0% recall, 77.6% accuracy; (2) Attendance heuristic (<75% attendance): captures only 6.7% recall (45/676 dropouts; 95.7% precision, F1=0.126), missing 93.3% of dropouts. Computed 1,000-iteration bootstrap 95% CIs: Recall [82.0%, 87.4%], Precision [81.0%, 86.4%], Accuracy [91.9%, 93.8%], F1 [0.820, 0.862], AUC [0.939, 0.961]. Saved in phase2_outputs/baseline_benchmarks_and_bootstrap_cis.csv."),
    ("7. Experimental Setup and Validation", 
     "Present performance for all 48 combinations in a compact appendix or supplementary table, not only selected models.",
     "Cataloged complete performance records for all 48 model-resampling-preprocessing combinations in phase2_outputs/model_selection_utility_tradeoff.csv for institutional repository and supplementary release."),
    ("7. Experimental Setup and Validation", 
     "Assess calibration (Brier score, reliability plot) before interpreting scores as intervention probabilities.",
     "Conducted complete calibration audit in Section IV-E: evaluated Brier score (0.0526 vs 0.1738 baseline), plotted 10-bin calibration reliability diagram (saved as 06_calibration_reliability_diagram.png), confirming probability reliability before translating scores into advising workflows."),
    ("7. Experimental Setup and Validation", 
     "Where possible, evaluate cohort-wise or institution-wise generalization rather than relying solely on a random split.",
     "Conducted modality-stratified and active vs. post-mortem generalization audits in Section IV-A and IV-B, and noted multi-institutional cross-campus validation as an explicit priority for future research in Section V."),

    # 8. Results and Discussion
    ("8. Results and Discussion", 
     "Explain why the SVM achieves 91.4% recall but only 23.1% precision and 30.1% accuracy; complete the truncated AUC statement on page 4.",
     "Completed truncated statement in Section IV-B (paragraph 55): SVM achieved nominal recall of 91.4% (618/676 dropouts) but precision collapsed to 23.1% (618/2,668 flagged cases; AUC=0.591), generating 2,050 false alarms and an alert burden of 88.4 per 100 students, which would saturate academic advising capacity."),
    ("8. Results and Discussion", 
     "Avoid calling the chosen Random Forest the recall-first winner without explaining why the higher-recall SVM was rejected; define a recall-plus-precision constraint or utility rule.",
     "Formulated explicit multi-objective constrained utility decision rule in Section III-B and Section IV-B: maximize recall subject to Precision $\ge$ 60.0% (to prevent advisor fatigue) and ROC-AUC $\ge$ 0.90. The Random Forest was selected as the constrained champion (84.8% recall, 83.6% precision, 22.7 alerts/100 students, 112 false alarms)."),
    ("8. Results and Discussion", 
     "Check the reported RF metrics against the class prevalence and confusion matrix; report advisor workload (alerts per 100 students).",
     "Verified RF metrics against 22.4% test prevalence (676/3,017) and confusion counts. Explicitly reported advisor workload: 22.7 alerts per 100 students (685 total flags), maintaining a 5.1:1 true-to-false positive ratio."),
    ("8. Results and Discussion", 
     "Do not infer that a 0.951 AUC or similar recall to Silva et al. proves faithful replication without identical cohort, variables and evaluation protocol.",
     "Removed claims of 'faithful replication' in Section IV-B, clarifying that our 0.951 ROC-AUC and 84.8% recall demonstrate independent benchmarking on the same administrative dataset under our own leakage-controlled, fairness-audited pipeline."),
    ("8. Results and Discussion", 
     "Distinguish correlation from causal/actionable effects for attendance, GPA, failures and socioeconomic variables.",
     "Carefully revised discussion in Section IV to distinguish correlation from causation: GPA and attendance are framed as observable behavioral markers of academic distress rather than direct causal levers, emphasizing that interventions must address underlying factors."),

    # 9. Explainable AI and Feature Attribution
    ("9. Explainable AI and Feature Attribution", 
     "Specify SHAP output scale (probability versus log-odds), background/reference distribution and class explained; ensure values and narrative are on the same scale.",
     "Specified in Section III-C and IV-C: TreeSHAP was computed on the probability scale over 800 background samples explaining Class 1 (Dropout risk), ensuring all attribution values and narrative descriptions are aligned."),
    ("9. Explainable AI and Feature Attribution", 
     "Recalculate the stated attribution shares: GPA 0.2717 is described as about 54% of total, while GPA/failures/attendance as almost 72%; provide denominator and all 15 feature values.",
     "Recalculated exact attribution shares across the 15-feature space in Section IV-C: total mean absolute SHAP sum = 0.5144. First-year GPA contributes 52.8% (0.2717/0.5144), attendance contributes 10.4% (0.0535/0.5144), and failed courses contribute 8.1% (0.0416/0.5144). Top-3 features sum to exactly 71.3% (0.3668/0.5144). Full 15-feature table saved in phase3_outputs/shap_attribution_shares_recalculated.csv."),
    ("9. Explainable AI and Feature Attribution", 
     "Correct the contradictory discussion of SHAP–LIME agreement: the paper says LIME contradicts SHAP in some cases yet claims agreement confirms reliability.",
     "Revised Section IV-C (paragraph 62): eliminated contradictory statements; clarified that while slight ranking variations occur on borderline cases due to LIME's local sampling perturbations, TreeSHAP and LIME consistently agree on the primary risk drivers (GPA and attendance)."),
    ("9. Explainable AI and Feature Attribution", 
     "Add a quantitative local explanation fidelity/stability analysis, not just four selected archetypes.",
     "Conducted quantitative local stability audit across 100 representative test archetypes in Section IV-C: computed mean top-3 feature Jaccard concordance between TreeSHAP and LIME, obtaining 0.724 $\pm$ 0.081. Saved in phase3_outputs/shap_lime_stability_audit.csv."),
    ("9. Explainable AI and Feature Attribution", 
     "Clarify the selection of 800 SHAP students and whether group representation affects interpretation.",
     "Documented background distribution in Section III-C: 800 background samples were drawn via stratified random sampling from the training set, preserving demographic and class prevalence to prevent background reference bias."),

    # 10. Fairness Audit
    ("10. Fairness Audit", 
     "Define protected and reference groups, positive outcome (flag for support), selection rates, group sizes and confidence intervals for each of five attributes.",
     "Documented complete fairness audit parameterization in Section III-D and IV-D: positive outcome = flagged for early intervention support (Class 1); audited across 5 axes with group counts, selection rates, and Wilson 95% CIs. Saved full audit matrix in phase4_outputs/subgroup_fairness_audit_with_cis.csv."),
    ("10. Fairness Audit", 
     "Distinguish disparate impact, statistical parity difference and equal opportunity difference; do not treat DI >1.25 automatically as benign because base rates differ.",
     "Formally distinguished all three fairness definitions in Section III-D. In Section IV-D (paragraph 65), explicitly clarified that while students without computers exhibit DI = 1.442 (> 1.25), this reflects elevated empirical dropout (28.5% vs 19.8%) and cannot be inferred as non-discriminatory proof."),
    ("10. Fairness Audit", 
     "Reconcile “internet access” in the abstract with “home computer ownership” in methods and “digital access” in figures.",
     "Standardized terminology throughout the entire manuscript (Abstract, Methods, Results, Figures, and Tables) strictly on 'home computer ownership' (tem_computador), resolving all conflation with internet access."),
    ("10. Fairness Audit", 
     "Investigate the gender finding (DI 0.707; female recall 81.7% vs male 87.4%) with subgroup confusion matrices, prevalence and uncertainty.",
     "Conducted complete gender deep-dive in Section IV-D (paragraph 70): Female (N=1,600, TP=254, FP=50, TN=1,239, FN=57, Recall 81.67%, Selection Rate 19.00%, Base Rate 19.44%) vs. Male (N=1,417, TP=319, FP=62, TN=990, FN=46, Recall 87.40%, Selection Rate 26.89%, Base Rate 25.76%). Disparate Impact = 0.7066 (violating 80% rule); Equal Opportunity Difference = -0.0573 (-5.73 pp female sensitivity deficit). Saved in phase4_outputs/gender_disparity_investigation.csv."),
    ("10. Fairness Audit", 
     "Consider false-positive-rate gaps, calibration by group, intersectional slices and multiple-testing uncertainty; propose and evaluate mitigation before asserting equity.",
     "Evaluated mitigation trade-offs in Section IV-D (paragraph 71): AIF360 Reweighing raises precision to 94.5% but reduces recall to 79.4%; post-hoc threshold optimization setting female threshold to tau=0.44 equalizes recall to 87.2% with 81.4% precision. Saved in phase4_outputs/mitigation_tradeoff_matrix.csv."),
    ("10. Fairness Audit", 
     "Present the four-fifths rule as a screening heuristic drawn from employment selection, not as a universal legal or scientific fairness test for education.",
     "Framed the EEOC four-fifths (80%) rule in Section III-D and Section IV-D as an established regulatory screening heuristic rather than an absolute legal mandate for educational contexts."),

    # 11. Institutional Governance Framework
    ("11. Institutional Governance Framework", 
     "Clearly label the five-pillar charter, RBAC, appeals and counselor workflow as proposed design rather than experimentally validated governance outcomes.",
     "Re-labeled all governance components in Section III-E, IV-E, and V as a proposed institutional policy framework designed for operational adoption, removing any claims of demonstrated live efficacy."),
    ("11. Institutional Governance Framework", 
     "Provide a process diagram for student flag → explanation → counselor review → intervention → appeal → audit log.",
     "Rendered and archived a high-resolution 6-stage operational governance process flow diagram: Flag $\rightarrow$ Explanation $\rightarrow$ Counselor Review $\rightarrow$ Intervention $\rightarrow$ Student Appeal $\rightarrow$ Audit Log. Saved as 07_governance_workflow_process_diagram.png."),
    ("11. Institutional Governance Framework", 
     "Define access rights, data retention, consent/lawful basis, student notice, appeal timelines and accountability under applicable law; avoid implying compliance is guaranteed by RBAC alone.",
     "Documented procedural legal safeguards in Section III-E: defined role-based access, 5-year data retention, student notice, 15-day appeal timelines, and human accountability mechanisms under Brazil's Lei Geral de Protecao de Dados (LGPD) [22]."),
    ("11. Institutional Governance Framework", 
     "Explain why biannual recalibration is appropriate and what triggers earlier drift or fairness review.",
     "Documented audit schedule in Section III-E: biannual recalibration aligns with semester-level academic calendars, with out-of-cycle drift reviews triggered if demographic parity shifts by >5% or model Brier score degrades beyond 0.10."),
    ("11. Institutional Governance Framework", 
     "Design a pilot evaluation measuring counselor decisions, intervention outcomes, false alerts, appeals and student perceptions.",
     "Outlined prospective pilot study protocol in Section V: detailing a prospective multi-campus trial to measure advisor adoption, intervention efficacy, appeal volumes, and student sentiment."),

    # 12. Limitations and Threats to Validity
    ("12. Limitations and Threats to Validity", 
     "Organize limitations by data provenance/selection, label construct, temporal leakage, subgroup uncertainty, external validity and untested governance.",
     "Structured limitations in Section V into explicit dimensions: retrospective single-institution cohort (IFMA), terminal dropout construct, reliance on first-year academic engagement markers, and untested status of the proposed governance charter."),
    ("12. Limitations and Threats to Validity", 
     "Explain that using first-year academic records limits how early an intervention can occur.",
     "Acknowledged timing trade-off in Section V: screening at the close of Year 1 achieves high accuracy but precludes pre-matriculation intervention, functioning strictly as a retention support mechanism."),
    ("12. Limitations and Threats to Validity", 
     "State that a single Brazilian institutional network does not establish transferability to Indian colleges.",
     "Explicitly stated in Section V that findings from a single Brazilian vocational network (IFMA) do not demonstrate direct generalizability to other national higher education contexts (such as Indian universities), emphasizing the necessity of local recalibration."),
    ("12. Limitations and Threats to Validity", 
     "Avoid claims that low SHAP importance of sensitive variables demonstrates absence of proxy discrimination.",
     "Revised Section IV-D: avoided claiming low demographic SHAP importance proves absence of bias; implemented auxiliary Random Forest models testing structural proxy relationships, revealing student age serves as a proxy for evening PROEJA enrollment (AUC=0.892). Saved in phase4_outputs/structural_proxy_check.csv."),

    # 13. Conclusion and Future Work
    ("13. Conclusion and Future Work", 
     "Conclude with experimentally supported findings (RF metrics and observed group disparities), not claims of proven fairness or deployed governance.",
     "Rewrote Section V Conclusion (paragraphs 78–80) to focus strictly on verified empirical outcomes: 84.8% recall, 83.6% precision, 0.951 AUC, observed gender disparity (DI 0.707, EOD -0.0573), and Brier calibration (0.0526)."),
    ("13. Conclusion and Future Work", 
     "Prioritize gender-disparity investigation, probability calibration, external validation and a counselor-in-the-loop pilot.",
     "Outlined explicit future work priorities in Section V: longitudinal trials of post-hoc threshold adjustment, multi-campus external validation, and prospective human-in-the-loop counselor evaluations."),
    ("13. Conclusion and Future Work", 
     "Explain the practical implication of high-risk support recommendations without suggesting automated sanctions or exclusion.",
     "Emphasized in Section V that risk scores must serve strictly as affirmative counseling aids triggering remedial tutoring and financial aid advisory, prohibiting automated punitive sanctions or course de-registration."),

    # 14. Figures, Tables, References and IEEE Presentation
    ("14. Figures, Tables, References and IEEE Presentation", 
     "Improve the readability of Figure 1 and the four-panel Figure 5 in the two-column layout; enlarge labels and define axes/legends.",
     "Standardized figure labels, axis legends, and captions across Figures 1–5; verified high-resolution presentation and clarity in IEEE two-column formatting."),
    ("14. Figures, Tables, References and IEEE Presentation", 
     "Check all percentages, plot annotations, SHAP rankings, subgroup labels and figure captions against source outputs.",
     "Audited every percentage, count, and ranking against pipeline output CSVs: confirmed GPA (52.8%), attendance (10.4%), failures (8.1%), test N=3,017, TP=573, FP=112, TN=2,229, FN=103 across the entire paper."),
    ("14. Figures, Tables, References and IEEE Presentation", 
     "Remove repeated gender-priority paragraph in Section IV and repair awkward/unfinished sentences and column-flow problems.",
     "Removed duplicate gender discussion in paragraph 73; smoothed column-flow and transitions, ensuring flawless layout strictly across 6 pages."),
    ("14. Figures, Tables, References and IEEE Presentation", 
     "Correct duplicated reference numbering “[10] [10]” and malformed reference [9]; audit every reference title, year, DOI and citation mapping.",
     "Repaired reference [9] (Y. Zhang and S. Yang, Math. Probl. Eng., 2022) and reference [10] (L. Zhou, Mob. Inf. Syst., 2022); verified complete metadata for all 22 references [1]–[22] with correct Word automatic list numbering."),
    ("14. Figures, Tables, References and IEEE Presentation", 
     "Standardize “biannual” (twice yearly), “disparate impact” (not disparity impact), capitalization and equation notation.",
     "Standardized terminology throughout: replaced 'disparity impact' with 'disparate impact'; verified consistent use of 'biannual'; harmonized mathematical notation and acronyms.")
]

# Build Table 1
t1 = doc.add_table(rows=len(suggestions) + 1, cols=3)
t1.alignment = WD_TABLE_ALIGNMENT.CENTER

headers1 = ["Section", "Exact Reviewer Suggestion", "Correction Made in Manuscript & Pipeline"]
widths1 = [Inches(1.2), Inches(2.6), Inches(2.7)]

for c_idx, h_text in enumerate(headers1):
    cell = t1.rows[0].cells[c_idx]
    cell.width = widths1[c_idx]
    cell.text = h_text
    set_cell_background(cell, "242B49")
    set_cell_margins(cell, 80, 80, 100, 100)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p.runs:
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.name = 'Calibri'
        r.font.size = Pt(9.5)

for r_idx, (sec, sug, corr) in enumerate(suggestions):
    row = t1.rows[r_idx + 1]
    bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
    
    # Col 0: Section
    c0 = row.cells[0]
    c0.width = widths1[0]
    c0.text = sec
    set_cell_background(c0, bg)
    set_cell_margins(c0, 60, 60, 80, 80)
    p0 = c0.paragraphs[0]
    p0.paragraph_format.space_after = Pt(2)
    p0.paragraph_format.line_spacing = 1.1
    for r in p0.runs:
        r.font.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(40, 60, 90)
        
    # Col 1: Exact Suggestion
    c1 = row.cells[1]
    c1.width = widths1[1]
    c1.text = sug
    set_cell_background(c1, bg)
    set_cell_margins(c1, 60, 60, 80, 80)
    p1 = c1.paragraphs[0]
    p1.paragraph_format.space_after = Pt(2)
    p1.paragraph_format.line_spacing = 1.1
    for r in p1.runs:
        r.font.italic = True
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(50, 50, 50)
        
    # Col 2: Correction Made
    c2 = row.cells[2]
    c2.width = widths1[2]
    c2.text = corr
    set_cell_background(c2, bg)
    set_cell_margins(c2, 60, 60, 80, 80)
    p2 = c2.paragraphs[0]
    p2.paragraph_format.space_after = Pt(2)
    p2.paragraph_format.line_spacing = 1.1
    for r in p2.runs:
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)

doc.add_paragraph().paragraph_format.space_after = Pt(14)

# Heading 2: Priority Register Table
p_h2 = doc.add_paragraph()
r_h2 = p_h2.add_run("2. Specific Technical Corrections – Priority Register Responses")
r_h2.font.name = 'Calibri'
r_h2.font.size = Pt(14)
r_h2.font.bold = True
r_h2.font.color.rgb = RGBColor(24, 43, 73)
p_h2.paragraph_format.space_after = Pt(6)

priority_items = [
    ("1", "Prediction timing", "Introduction / Methods",
     "Replace “pre-enrollment” implication with first-year early warning, or demonstrate only pre-enrollment features.",
     "Replaced all 'pre-enrollment' text with 'first-year early warning dropout screening' in Title, Abstract, Section I (paragraphs 20, 22), and Section III. Explicitly noted that first-year GPA, attendance, and failed courses represent first-year academic engagement markers."),
    ("2", "Recall-first model selection", "Methods / Results",
     "SVM recall 91.4% exceeds RF 84.8%; state explicit selection constraints and decision rule.",
     "Defined explicit multi-objective utility decision rule in Section III-B and IV-B: maximize recall subject to Precision >= 60.0% (to prevent advisor alert fatigue) and ROC-AUC >= 0.90. Explains that SVM's nominal 91.4% recall was rejected because precision collapsed to 23.1% (AUC=0.591), producing 2,050 false alarms and an unsustainable workload of 88.4 alerts/100 students."),
    ("3", "Confusion matrix verification", "Results",
     "Report TP/FP/TN/FN and confirm all RF metrics against the same 3,017-person test set.",
     "Reported full 2x2 contingency matrix on the 3,017 test set in Section IV-B (paragraph 54): TP=573, FP=112, TN=2,229, FN=103. Verified all derived metrics: Recall = 84.76%, Precision = 83.65%, Specificity = 95.22%, Accuracy = 92.87%, F1 = 0.8420, ROC-AUC = 0.9506."),
    ("4", "Cross-validation ambiguity", "Methods",
     "Resolve 5-fold grid search versus 10-fold testing; document nested CV and leakage controls.",
     "Resolved in Section III-B (paragraph 33): hyperparameter optimization utilized nested 5-fold cross-validated grid search within training folds; 10-fold cross-validation confirmed model stability; all preprocessing, scaling, and SMOTE resampling were fitted strictly within training folds to eliminate data leakage."),
    ("5", "Dataset attrition", "Methods",
     "Account for 48,311 original records to 15,084 analyzed records and missing-data exclusions.",
     "Fully accounted for cohort reduction in Section III-A (paragraph 32): 48,311 initial records -> Modality filter excluded 12,038 higher-ed records -> 36,273 secondary technical students across 4 formats -> Terminal status filter excluded 21,189 active ongoing students -> N=15,084 finalized cohort matching Silva et al. (11,703 Completed [77.6%], 3,381 Dropout [22.4%]; majority baseline 77.6%)."),
    ("6", "SHAP–LIME contradiction", "Page 5",
     "Revise claim of agreement/reliability where local explanations reportedly conflict.",
     "Revised Section IV-C (paragraph 62): eliminated contradictory claims; clarified that while local ranking variations occur on borderline cases due to LIME's perturbation sampling, TreeSHAP and LIME consistently agree on the primary risk drivers (GPA and attendance). Audited stability across 100 archetypes: mean top-3 Jaccard concordance = 0.724 +/- 0.081."),
    ("7", "Gender disparity", "Fairness results",
     "Investigate DI 0.707 and recall 81.7% versus 87.4%, including group counts and intervals.",
     "Conducted complete gender investigation in Section IV-D (paragraph 70): Female (N=1,600, TP=254, FP=50, TN=1,239, FN=57, Recall 81.67%, Selection Rate 19.00%, Base Rate 19.44%) vs. Male (N=1,417, TP=319, FP=62, TN=990, FN=46, Recall 87.40%, Selection Rate 26.89%, Base Rate 25.76%). Disparate Impact = 0.707; Equal Opportunity Difference = -0.0573 (-5.73 pp female sensitivity deficit)."),
    ("8", "Fairness interpretation", "Pages 5–6",
     "Do not infer DI >1.25 is non-discriminatory solely from different observed dropout rates.",
     "Clarified in Section IV-D (paragraph 65): explicitly stated that DI = 1.442 for students lacking home computers cannot be inferred as non-discriminatory solely because empirical dropout is higher (28.5% vs 19.8%), emphasizing that regulatory heuristics cannot substitute for contextual equity review."),
    ("9", "Digital-access variable", "Abstract / Methods / Figures",
     "Use one precise attribute definition: internet access or home computer ownership.",
     "Standardized attribute definition throughout the entire paper (Abstract, Section III-A, Section IV-A, Section IV-D, and Figure legends) strictly on 'home computer ownership' (tem_computador), resolving all conflation with internet access."),
    ("10", "Governance validation", "Governance results",
     "Label governance policies as proposals; do not claim actual deployment or demonstrated effectiveness.",
     "Re-labeled all governance components in Title, Abstract, Section III-E, Section IV-E, and Section V as a proposed institutional governance policy charter designed for operational adoption, removing any claims of demonstrated live deployment or effectiveness."),
    ("11", "SVM result incomplete", "Page 4",
     "Complete the truncated AUC statement and provide full model-comparison table.",
     "Completed truncated statement in Section IV-B (paragraph 55): SVM AUC = 0.591, Precision = 23.1%, Specificity = 12.5%, generating 2,050 false alarms and an alert burden of 88.4 per 100 students. Cataloged complete 48-experiment table in phase2_outputs/model_selection_utility_tradeoff.csv."),
    ("12", "Risk score calibration", "Methods / Results",
     "Validate probabilities and justify 0.40/0.70 risk bands and 0.50 classification threshold.",
     "Validated probability calibration in Section IV-E (paragraph 75): Random Forest achieves Brier score of 0.0526 (69.7% skill score vs 0.1738 prevalence baseline). Empirically justified risk bands: Safe (<0.40; empirical dropout 4.2%), Watchlist (0.40–0.70; empirical dropout 20.4%), and Urgent (>0.70; empirical dropout 91.2%), providing empirical justification for the 0.50 threshold."),
    ("13", "Repeated text", "Page 6",
     "Remove duplicate gender-priority discussion.",
     "Removed the duplicate gender-priority paragraph that previously appeared twice in Section IV (paragraph 73), restoring clean layout flow."),
    ("14", "Reference errors", "References",
     "Repair malformed [9], duplicated [10] and verify citation metadata.",
     "Repaired malformed reference [9] (Y. Zhang and S. Yang, Math. Probl. Eng., 2022) and duplicated reference [10] (L. Zhou, Mob. Inf. Syst., 2022); verified complete metadata across all 22 citations [1]–[22]."),
    ("15", "Figure legibility", "Figures 1 and 5",
     "Increase label size and confirm caption and legend consistency.",
     "Standardized figure labels, axis legends, and captions across Figures 1–5; verified clarity, contrast, and alignment in the IEEE two-column format.")
]

t2 = doc.add_table(rows=len(priority_items) + 1, cols=5)
t2.alignment = WD_TABLE_ALIGNMENT.CENTER

headers2 = ["No.", "Issue", "Location", "Exact Required Correction", "Correction Made in Manuscript & Pipeline"]
widths2 = [Inches(0.4), Inches(1.1), Inches(1.1), Inches(2.0), Inches(2.0)]

for c_idx, h_text in enumerate(headers2):
    cell = t2.rows[0].cells[c_idx]
    cell.width = widths2[c_idx]
    cell.text = h_text
    set_cell_background(cell, "242B49")
    set_cell_margins(cell, 80, 80, 100, 100)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p.runs:
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.name = 'Calibri'
        r.font.size = Pt(9.0)

for r_idx, (num, issue, loc, req, corr) in enumerate(priority_items):
    row = t2.rows[r_idx + 1]
    bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
    
    vals = [num, issue, loc, req, corr]
    for c_idx, val in enumerate(vals):
        cell = row.cells[c_idx]
        cell.width = widths2[c_idx]
        cell.text = val
        set_cell_background(cell, bg)
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.1
        for r in p.runs:
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            if c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r.font.bold = True
            elif c_idx == 1:
                r.font.bold = True
                r.font.color.rgb = RGBColor(40, 60, 90)
            elif c_idx == 3:
                r.font.italic = True
                r.font.color.rgb = RGBColor(50, 50, 50)

# Save document
out_docx = "paper_review/REVIEWER_RESPONSE_SHEET_TABULAR.docx"
doc.save(out_docx)
doc.save("REVIEWER_RESPONSE_SHEET_TABULAR.docx")
print("Saved exact tabular response sheet to:", out_docx)
