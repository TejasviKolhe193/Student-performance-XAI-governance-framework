import docx
import shutil

target_path = "paper_review/research_paper_final_draft.docx"
shutil.copyfile("paper_review/research_paper_final_draft_ORIGINAL_BACKUP.docx", target_path)
doc = docx.Document(target_path)

# Title (Section 1 of Review Suggestions)
title_text = "An Explainable and Fairness-Audited AI Governance Framework for Student Dropout Prediction"

# Page 1: Abstract (~275 words)
abstract_text = (
    "Abstract-Student dropout undermines educational attainment and institutional sustainability. While predictive "
    "machine learning identifies vulnerable students, deploying algorithms without explainability, fairness guarantees, "
    "and procedural governance risks severe institutional harm. We present an Explainable AI Governance Framework for "
    "first-year early warning dropout screening, unifying high-recall classification, dual-tier TreeSHAP and LIME "
    "interpretability, algorithmic fairness audits across five protected demographic axes, and a proposed five-pillar "
    "institutional governance charter. Benchmarking 48 model configurations on 15,084 secondary technical students from "
    "the Brazilian Federal Institutes (2014-2020) reveals that a tuned Random Forest with SMOTE achieves 84.8% recall "
    "(95% CI [82.0%, 87.4%]), 83.6% precision [81.0%, 86.4%], 92.9% accuracy, and 0.951 ROC-AUC on a held-out test set of "
    "3,017 students (TP=573, FP=112, TN=2,229, FN=103), generating an operational workload of 22.7 alerts per 100 students. "
    "Global TreeSHAP demonstrates that first-year GPA, attendance, and failed courses account for 71.3% of total feature attribution. "
    "Audits across demographic groups reveal a critical gender sensitivity disparity (disparate impact 0.707; female recall 81.7% "
    "versus male recall 87.4%), while home computer ownership exhibits structural privilege. We evaluate fairness mitigations via "
    "AIF360 Reweighing and post-hoc threshold adjustment, audit probability calibration (Brier score 0.0526 versus 0.1738 prevalence "
    "baseline), and establish an actionable three-tier intervention workflow governed by human-in-the-loop review and student appeal "
    "mechanisms under Brazil's Lei Geral de Protecao de Dados."
)

# Page 1: Introduction P20 (~97 words)
p20_text = (
    "Accuracy alone is insufficient when predictions trigger academic triage: false negatives allow vulnerable students to "
    "drop out without support, while false positives waste scarce institutional counseling resources. Screening must occur during "
    "the first academic year, balancing recall with advisor workload constraints. Furthermore, black-box models prevent advisors from "
    "discovering root causes, and un-audited algorithms perpetuate historical demographic disparities. Operational deployment requires "
    "institutional safeguards, local and global explainability, rigorous fairness guarantees, and human oversight to prevent "
    "unintended harm [1], [2]. Without governance, early warning systems risk misallocating institutional resources."
)

# Page 1: Introduction P22 (~108 words)
p22_text = (
    "We bridge this gap with an Explainable AI Governance Framework for first-year dropout early warning, combining predictive "
    "modeling, dual-tier interpretability, fairness auditing, and proposed institutional governance. Validated on 15,084 Brazilian "
    "vocational students [1], the framework establishes empirical benchmarks, audits demographic fairness under Brazil's LGPD, and "
    "articulates actionable governance policies designed for institutional adoption. The framework moves beyond abstract principles "
    "to provide actionable mechanisms: SHAP-based local explanations translate model outputs into targeted interventions, demographic "
    "audits expose hidden disparities, and procedural governance mandates human-in-the-loop validation for high-stakes decisions."
)

# Page 1: Introduction P23 (~63 words)
p23_text = (
    "The primary contribution is operational integration: (1) a multi-model benchmark with explicit utility-constrained selection; "
    "(2) concordant global and local explanations; (3) systematic fairness audits with demographic parity and equalized odds; "
    "(4) risk probability calibration; and (5) a proposed five-pillar institutional governance policy charter designed for education."
)

# Page 1: Roadmap P24 (~25 words)
p24_text = (
    "Section II reviews the literature, Section III details the methodology, Section IV presents experimental and audit results, "
    "and Section V concludes with limitations and future work."
)

# Page 2: Table I updates
table = doc.tables[0]
table.rows[0].cells[0].text = "Study & Citation"
table.rows[0].cells[1].text = "Domain & Sample (N)"
table.rows[0].cells[2].text = "Key Findings & Method"
table.rows[0].cells[3].text = "Gaps Addressed"

table_updates = {
    1: ["Silva et al. (2025) [1]", "IFMA Brazil (N=15,084)", "85% recall; RF with SHAP & LIME", "No fairness audit or policy charter"],
    2: ["Zanellati et al. (2024) [2]", "Italy Higher Ed (N=7,000)", "81% recall; Transformer, TreeSHAP", "Gender checked; no appeal board"],
    3: ["Priyadarshini et al. (2024) [3]", "US Admissions (N=12,000)", "Adversarial debiasing in DL", "Training only; no post-hoc XAI"],
    4: ["Mengash (2020) [4]", "Saudi University (N=2,000)", "Pre-admission prediction; ANN", "Sensitive data; no equity audit"],
    5: ["Alhazmi & Sheneamer (2023) [5]", "Saudi University (N=3,500)", "Early at-risk prediction; Ensemble", "No explanations or fairness check"],
    6: ["Pelima et al. (2024) [6]", "Systematic Review (84 papers)", "Graduation review; RF, SVM <=90% acc", "XAI and fairness rarely integrated"],
    7: ["Ma et al. (2023) [7]", "Personalized E-Learning", "Exam prediction; Neutrosophic", "No demographic audit or oversight"],
    8: ["Jiang & Wang (2020) [8]", "Online Learning Platforms", "Cognitive diagnosis; neural weights", "Interpretable; no fairness metric"],
    9: ["Zhang & Yang (2022) [9]", "Teacher Evaluation (China)", "Performance appraisal; Fuzzy GA", "Fuzzy logic; no appeal rights"],
    10: ["Zhou (2022) [10]", "Basic Education (China)", "Informatization; BP Neural Net", "Black box; no transparency rules"],
    11: ["Lu et al. (2024) [11]", "Physical Education (China)", "Quality appraisal; ExpTODIM", "Expert weights; no demographic audit"]
}
for r_idx, data in table_updates.items():
    for c_idx, text in enumerate(data):
        table.rows[r_idx].cells[c_idx].text = text

# Page 2: Methodology intro P29 (~94 words)
p29_text = (
    "The methodology operationalizes student dropout screening into a governed, five-phase decision workflow (Fig. 1). "
    "Phase 1 prepares the multi-campus dataset and audits student cohort attrition. Phase 2 benchmarks 48 classifier configurations "
    "under nested cross-validation and constrained utility selection. Phase 3 implements dual-tier TreeSHAP and LIME interpretability. "
    "Phase 4 executes algorithmic fairness audits across five demographic axes. Phase 5 operationalizes risk calibration and "
    "establishes proposed institutional governance policies."
)

# Page 2: Data preparation P32 (~82 words)
p32_text = (
    "Data derive from the Brazilian Federal Institutes database (2014-2020; N = 48,311 initial records, 30 attributes) [1]. "
    "Cohort attrition followed a rigorous two-stage provenance filter: first, excluding 12,038 higher education records to retain "
    "36,273 secondary technical students; second, excluding 21,189 active non-terminal students, yielding N = 15,084 analyzed students. "
    "The analyzed cohort comprises 11,703 completed students (77.6%) and 3,381 dropouts (22.4%), establishing an uninformative "
    "majority baseline of 77.6%."
)

# Page 2/3: Split & Leakage P33 (~68 words)
p33_text = (
    "A stratified 80/20 train/test split partitioned the 15,084 students into 12,067 training and 3,017 held-out test students. "
    "All preprocessing, imputation, and SMOTE resampling were fitted strictly within training folds to prevent data leakage. "
    "Hyperparameter optimization utilized nested 5-fold cross-validated grid search within training folds, while 10-fold "
    "cross-validation confirmed stability before final evaluation on the 3,017 test set."
)

# Page 3: Model benchmarking P35 (~75 words)
p35_text = (
    "The 48-condition factorial design crossed 4 classifiers (Random Forest, SVM, Decision Tree, Logistic Regression), 3 sampling "
    "methods (None, SMOTE, Under-sampling), and 4 preprocessors. Model selection followed an explicit constrained utility rule: "
    "maximize recall subject to precision >= 60.0% (to prevent advisor alert fatigue) and ROC-AUC >= 0.90, prioritizing early warning "
    "sensitivity within operational counseling capacity."
)

# Page 3: Metrics P36 (~54 words)
p36_text = (
    "Evaluation metrics included Recall (sensitivity), Precision, Specificity, F1-Score, Accuracy, and ROC-AUC. We executed 1,000 "
    "stratified bootstrap iterations to estimate 95% confidence intervals on the 3,017-student test set, confirming statistical "
    "significance across all reported performance dimensions."
)

# Page 3: Explainable AI P38 (~104 words)
p38_text = (
    "Global interpretability applied TreeSHAP [19] on the probability scale over 800 background instances to quantify feature "
    "attribution shares across the 15-feature space. Local fidelity was examined via KernelSHAP and LIME [13], providing individual "
    "recourse profiles for academic advisors. To address potential explanation conflicts, we conducted a stability audit computing "
    "top-3 feature attribution concordance across 100 representative archetypes, ensuring that local explanations reliably reflect "
    "underlying model behavior."
)

# Page 3: Fairness Audit P40 (~119 words)
p40_text = (
    "Fairness was evaluated on the 3,017 held-out test students across five demographic axes: Gender, Educational Modality, "
    "Marital Status, Quota Admission, and Home Computer Ownership (digital access). We evaluated Disparate Impact (DI, applying the "
    "EEOC 80% rule [0.80, 1.25]), Statistical Parity Difference (SPD), and Equal Opportunity Difference (EOD, quantifying the female "
    "versus male sensitivity gap). In addition, auxiliary models audited structural proxy relationships to confirm whether unprotected "
    "academic attributes inadvertently encoded protected demographic membership."
)

# Page 3: Institutional Governance P42 (~165 words)
p42_text = (
    "The framework establishes a proposed institutional governance policy charter structured across five operational pillars: "
    "(1) Policy Charter formalizing deployment as advisory decision-support rather than autonomous tracking; (2) Algorithmic "
    "Transparency delivering plain-language explanation summaries to students and counselors; (3) Human Accountability mandating "
    "independent advisor review prior to intervention; (4) Risk Management enforcing quarterly data drift monitoring and bias audits; "
    "and (5) Independent Audit preserving student appeal rights under Brazil's Lei Geral de Protecao de Dados [22]. We evaluate "
    "probability calibration via Brier scores to validate three actionable risk tiers: Safe (<0.40), Watchlist (0.40-0.70), and "
    "Urgent Intervention (>0.70), providing empirical justification for the 0.50 operational decision boundary."
)

# Page 3: Phase 1 Results P46 (~30 words)
p46_text = (
    "The stratified split yielded 12,067 training students and 3,017 test students (2,722 active enrolled cohort, 295 post-mortem records). "
    "Model performance remained robust across active (80.8% recall) and post-mortem (95.2% recall) subsets."
)

# Page 3: Phase 1 Results P47 (~47 words)
p47_text = (
    "The largest modality, Integrado (10,076 students), exhibits the lowest dropout rate (16.4%), whereas Concomitante (27.8%), "
    "Subsequente (31.2%), and PROEJA/Integrado EJA (36.4%) show markedly higher attrition, reflecting older student populations "
    "balancing employment with technical education."
)

# Page 3: Phase 1 Patterns P50 (~114 words)
p50_text = (
    "Three empirical patterns characterize the cohort: (1) An attendance cliff (Fig. 3), where dropout reaches 88.7% for "
    "attendance <75%, dropping to 3.2% for attendance >90%; (2) Modality shift, where evening adult students (PROEJA) experience "
    "36.4% attrition compared to 16.4% in integrated programs; and (3) Digital inequality, where students lacking home computer access "
    "suffer a 28.5% dropout rate compared to 19.8% for computer owners. These findings demonstrate that early warning indicators are "
    "strongly observable during the first academic year."
)

# Page 4: Phase 2 Benchmarking Results P54 (~97 words)
p54_text = (
    "The Random Forest champion (SMOTE, 100 trees, max_depth=12) achieved 84.8% recall (95% CI [82.0%, 87.4%]), 83.6% precision "
    "[81.0%, 86.4%], 92.9% accuracy [91.9%, 93.8%], F1 of 0.842 [0.820, 0.862], and ROC-AUC of 0.951 [0.939, 0.961]. On the 3,017 "
    "test students (676 dropouts, 2,341 completed), the exact confusion matrix confirms: TP=573, FP=112, TN=2,229, FN=103. The model "
    "generates 22.7 alerts per 100 students, capturing 84.8% of dropouts while maintaining a 5.1:1 true-to-false alert ratio."
)

# Page 4: Model comparison & SVM trade-off P55 (~103 words)
p55_text = (
    "Alternative models failed operational requirements. While Support Vector Machines (SVM) achieved nominal recall of 91.4% "
    "(618/676 dropouts), precision collapsed to 23.1% (AUC = 0.591), generating 2,050 false alarms (88.4 alerts/100 students) and "
    "overwhelming advising capacity. Decision Trees overfit (86.4% accuracy, 0.887 AUC). Model selection adhered to the constrained "
    "utility rule: maximize recall subject to precision >= 60.0% and AUC >= 0.90. The Random Forest champion satisfied this constraint. "
    "Baseline benchmarks confirm necessity: a majority-class baseline yields 0.0% recall, while an attendance-only heuristic (<75%) "
    "achieves 95.7% precision but captures only 6.7% recall (F1 = 0.126), missing 93.3% of vulnerable students."
)

# Page 4: Phase 3 Explainability P57 (~173 words)
p57_text = (
    "TreeSHAP attributions on 800 background students demonstrate that academic engagement and performance dominate dropout risk: "
    "First-year GPA accounts for 52.8% of total feature attribution, attendance percentage contributes 10.4%, and failed course count "
    "accounts for 8.1%. Together, these top-3 academic features represent 71.3% of the total attribution share across the 15-feature space. "
    "In contrast, demographic attributes (gender, age, marital status, quota admission) collectively account for less than 5% of direct "
    "model attribution, confirming that the Random Forest bases its predictions primarily on observable educational behaviors rather "
    "than demographic proxies."
)

# Page 4: Beeswarm plot text P58 (~27 words)
p58_text = (
    "From the beeswarm plot (Fig. 4), high GPA (red points) strongly drives negative SHAP values, protecting students from dropout. "
    "Low attendance and computer absence drive positive risk values."
)

# Page 4: Local explanations P62 (~83 words)
p62_text = (
    "Local explanations provide individual recourse profiles for academic advisors. To evaluate local explanation stability, "
    "we audited top-3 feature concordance between TreeSHAP and LIME across 100 representative archetypes, obtaining a mean "
    "Jaccard concordance of 0.724 +/- 0.081. While slight ranking variations occur on borderline cases, GPA and attendance "
    "consistently emerge as primary risk drivers across both interpretability methods, confirming explanatory reliability."
)

# Page 4: Student exemplar P63 (~105 words)
p63_text = (
    "For borderline student #37 (predicted risk 50.8%), TreeSHAP attributes 0.18 risk increase to first-year GPA (1.92) and 0.09 to "
    "accumulated course failures, while good attendance (86.0%) contributes -0.11 protective risk. LIME produces concordant attributions, "
    "identifying the same critical risk factors. Academic advisors can thus prescribe targeted remedial tutoring in failing subjects "
    "without misinterpreting the student's regular attendance pattern as academic disengagement."
)

# Page 5: Fairness dashboard P65 (~75 words)
p65_text = (
    "Fairness audits across the 3,017 test students reveal complex demographic dynamics (Fig. 5). Quota-admitted students show "
    "favorable parity (DI = 1.042; EOD = +0.015). Students lacking home computers exhibit DI = 1.442; while exceeding 1.25, this "
    "reflects elevated empirical dropout (28.5% vs. 19.8%) rather than algorithmic bias. Auxiliary modeling revealed student age serves "
    "as a structural proxy for evening PROEJA modality (AUC = 0.892), whereas gender (0.617) and income (0.679) remain un-proxied."
)

# Page 5: Gender Disparity P70 (~81 words)
p70_text = (
    "A significant disparity was detected in gender: female students exhibit DI = 0.707 (below the 0.80 threshold) and a sensitivity "
    "gap of -5.73 percentage points (female recall 81.67% [254/311] vs. male recall 87.40% [319/365]; EOD = -0.0573). Female selection rate "
    "was 19.00% (304/1,600) compared to male selection rate of 26.89% (381/1,417), partly mirroring lower empirical female dropout "
    "(19.44% vs. 25.76%). However, the 5.73% sensitivity deficit means female dropouts are disproportionately missed by uniform screening."
)

# Page 5: Mitigation trade-offs P71 (~75 words)
p71_text = (
    "To address the female sensitivity gap, we evaluated pre-processing and post-processing mitigations. In-processing AIF360 Reweighing "
    "raised precision to 94.5% but depressed overall recall to 79.4%, missing additional dropouts. Conversely, post-hoc threshold adjustment "
    "setting female threshold to tau=0.44 equalizes recall to 87.2% with a negligible precision reduction (81.4%), providing an optimal "
    "institutional compromise."
)

# Page 5: Institutional resource trade-off P72 (~82 words)
p72_text = (
    "Figure 5(d) depicts institutional resource allocation under varying operational thresholds: lowering classification thresholds "
    "captures more vulnerable dropouts but increases false alerts and advisor caseload. The proposed 0.50 threshold maintains a 5.1:1 "
    "true-to-false alert ratio, capping counselor workload at 22.7 alerts per 100 students."
)

# Clear duplicate paragraph P73
p73_text = ""

# Page 5: Calibration P75 (~87 words)
p75_text = (
    "Probability calibration was validated via Brier scores and reliability curves. The Random Forest achieved a Brier score of 0.0526, "
    "representing a 69.7% skill improvement over the 0.1738 empirical prevalence baseline. Probabilities map reliably to three actionable "
    "risk tiers: Safe (<0.40; empirical dropout 4.2%), Watchlist (0.40-0.70; empirical dropout 20.4%), and Urgent Intervention (>0.70; "
    "empirical dropout 91.2%), providing empirical justification for the 0.50 binary classification threshold."
)

# Page 5: Proposed governance pillars P76 (~96 words)
p76_text = (
    "To govern operational deployment, we articulate five proposed governance policy pillars: (1) Policy Charter establishing "
    "advisory-only deployment; (2) Algorithmic Transparency providing students explainability summaries; (3) Human Accountability "
    "requiring advisor review before intervention; (4) Risk Management enforcing quarterly drift monitoring; and (5) Independent Audit "
    "maintaining student appeal rights under Brazilian LGPD regulations. These proposed policies ensure that predictive models serve as "
    "equitable counseling aids rather than punitive tracking systems."
)

# Page 6: Conclusion summary P78 (~90 words)
p78_text = (
    "This work presented an Explainable AI Governance Framework for first-year dropout early warning, operationalizing high-recall "
    "prediction (84.8% recall, 83.6% precision, 0.951 AUC), dual-tier explainability (71.3% attribution on top-3 features), and comprehensive "
    "fairness audits. The framework demonstrates that predictive accuracy must be paired with fairness evaluations and policy safeguards "
    "to ensure that early warning systems promote educational equity without generating unintended demographic harm."
)

# Page 6: Conclusion findings P79 (~86 words)
p79_text = (
    "Algorithmic audits revealed a 5.73 percentage point female sensitivity gap and digital access disparities, which post-hoc threshold "
    "optimization successfully mitigates. Probability calibration validates three operational risk tiers, enabling tiered academic "
    "interventions while capping advisor workload at 22.7 alerts per 100 students. The framework provides a concrete blueprint for "
    "responsible AI adoption in vocational and higher education institutions."
)

# Page 6: Conclusion limitations P80 (~67 words)
p80_text = (
    "Limitations include evaluation within a single multi-campus institution and reliance on retrospective cohort data. Future research "
    "will assess cross-institutional transferability, dynamic semester-by-semester feature trajectories, and prospective longitudinal "
    "trials of the governance policy charter to evaluate real-world intervention efficacy and counselor satisfaction."
)

# References: Repair [9] and [10]
ref_9_text = (
    "Y. Zhang and S. Yang, \"Teacher Performance Appraisal System in Colleges and Universities Using Fuzzy Genetic Algorithm,\" "
    "Math. Probl. Eng., vol. 2022, Art. no. 8415291, pp. 1-10, 2022."
)
ref_10_text = (
    "L. Zhou, \"Performance Evaluation of Basic Education Informatization Based on BP Neural Network,\" "
    "Mob. Inf. Syst., vol. 2022, Art. no. 9631623, pp. 1-9, 2022."
)

# Map all updates
p_map = {
    0: title_text,
    17: abstract_text,
    20: p20_text,
    22: p22_text,
    23: p23_text,
    24: p24_text,
    29: p29_text,
    32: p32_text,
    33: p33_text,
    35: p35_text,
    36: p36_text,
    38: p38_text,
    40: p40_text,
    42: p42_text,
    46: p46_text,
    47: p47_text,
    50: p50_text,
    54: p54_text,
    55: p55_text,
    57: p57_text,
    58: p58_text,
    62: p62_text,
    63: p63_text,
    65: p65_text,
    70: p70_text,
    71: p71_text,
    72: p72_text,
    73: p73_text,
    75: p75_text,
    76: p76_text,
    78: p78_text,
    79: p79_text,
    80: p80_text,
    90: ref_9_text,
    91: ref_10_text
}

# Apply updates preserving font styling
for p_idx, text in p_map.items():
    p = doc.paragraphs[p_idx]
    if len(text) == 0:
        p.text = ""
        p.paragraph_format.space_before = 0
        p.paragraph_format.space_after = 0
        p.paragraph_format.line_spacing = 0.1
    else:
        if len(p.runs) > 0:
            first_run = p.runs[0]
            font_name = first_run.font.name if first_run.font.name else "Times New Roman"
            font_size = first_run.font.size
            bold = first_run.bold
            italic = first_run.italic
            p.text = ""
            r = p.add_run(text)
            r.font.name = font_name
            if font_size:
                r.font.size = font_size
            r.bold = bold
            r.italic = italic
        else:
            p.text = text

doc.save(target_path)
print(f"Saved {target_path}")
