import docx
import shutil

# Make a fresh working copy from ORIGINAL_BACKUP
shutil.copyfile("paper_review/research_paper_final_draft_ORIGINAL_BACKUP.docx", "paper_review/research_paper_final_draft.docx")

doc = docx.Document("paper_review/research_paper_final_draft.docx")

# Define concise, high-density replacements addressing EVERY reviewer point
# Page 1: Abstract & Intro
abstract_text = (
    "Abstract-Student dropout undermines educational attainment and institutional sustainability. While machine "
    "learning identifies at-risk students, deployment without explainability, fairness audits, and procedural governance "
    "risks inequitable harm. We present an Explainable AI Governance Framework for first-year early warning dropout "
    "screening, unifying high-recall prediction, TreeSHAP and LIME interpretability, algorithmic fairness audits across "
    "five protected axes, and a five-pillar institutional governance policy charter. Benchmarking 48 model configurations "
    "on 15,084 secondary technical students from the Brazilian Federal Institutes (2014-2020) reveals that Random Forest "
    "with SMOTE and hyperparameter tuning achieves 84.8% recall (95% CI [82.0%, 87.4%]), 83.6% precision, 92.9% accuracy, "
    "and 0.951 ROC-AUC on a 3,017-student test set (TP=573, FP=112, TN=2,229, FN=103), outperforming baseline benchmarks. "
    "Global TreeSHAP confirms GPA, attendance, and failed courses account for 71.3% of feature attribution. Fairness audits "
    "reveal a critical gender sensitivity gap (disparate impact 0.707; female recall 81.7% vs. male 87.4%), while home computer "
    "ownership exhibits structural privilege. We demonstrate mitigation trade-offs via AIF360 and evaluate Brier calibration "
    "(0.0526 vs. 0.1738 baseline), establishing an actionable three-tier intervention framework with human-in-the-loop review."
)

# P20: Intro context
p20_text = (
    "Accuracy alone is insufficient when predictions trigger academic triage: false negatives allow vulnerable students to "
    "drop out without support, while false positives waste scarce institutional resources. Screening must occur during the first "
    "academic year, balancing recall with advisor workload constraints. Furthermore, black-box models prevent advisors from "
    "discovering root causes, and un-audited algorithms perpetuate demographic disparities. Algorithmic governance requires "
    "institutional safeguards, explainability, fairness guarantees, and human oversight [1], [2]."
)

# P22: Contribution proposal framing
p22_text = (
    "We bridge this gap with an Explainable AI Governance Framework for first-year dropout early warning, combining predictive "
    "modeling, dual-tier interpretability, fairness auditing, and proposed institutional governance. Validated on 15,084 Brazilian "
    "vocational students [1], the framework establishes empirical benchmarks, audits demographic fairness under Brazil's LGPD, and "
    "articulates actionable governance policies designed for institutional adoption."
)

# P23: Contributions
p23_text = (
    "The primary contribution is operational integration: (1) a multi-model benchmark with explicit utility-constrained selection; "
    "(2) concordant global and local explanations; (3) systematic fairness audits with demographic parity and equalized odds; "
    "(4) risk probability calibration; and (5) a proposed five-pillar institutional governance policy charter."
)

# P24: Roadmap
p24_text = (
    "Section II reviews the literature, Section III details the methodology, Section IV presents experimental and audit results, "
    "and Section V concludes with limitations and future work."
)

# Page 2: Table I updates
table = doc.tables[0]
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

for row_idx, data in table_updates.items():
    row = table.rows[row_idx]
    for col_idx, text in enumerate(data):
        row.cells[col_idx].text = text

# Table header
table.rows[0].cells[0].text = "Study & Citation"
table.rows[0].cells[1].text = "Domain & Sample (N)"
table.rows[0].cells[2].text = "Key Findings & Method"
table.rows[0].cells[3].text = "Gaps Addressed"

# P29: Methodology intro
p29_text = (
    "The methodology operationalizes dropout prediction into a governed, five-phase decision system (Fig. 1): "
    "data preparation, benchmarking, explainability, fairness auditing, and institutional governance."
)

# P32 (Doc P32 / P93 in COM): Dataset attrition provenance
p32_text = (
    "Data derive from the Brazilian Federal Institutes database (2014-2020; N = 48,311 initial records, 30 attributes) [1]. "
    "Provenance filtering executed in two stages: (1) Modality filter: excluded 12,038 higher education records, retaining "
    "36,273 secondary technical students across four formats (Integrado, Concomitante, Subsequente, PROEJA); (2) Terminal "
    "status filter: excluded 21,189 active ongoing students, yielding N = 15,084 finalized cohorts matching [1]. Completed "
    "students comprise 11,703 (77.6%); dropouts comprise 3,381 (22.4%), defining a 77.6% majority baseline."
)

# P33: Train/test split & nested CV
p33_text = (
    "A stratified 80/20 train/test split partitioned the 15,084 students into 12,067 training and 3,017 test cases. "
    "Data preprocessing, imputation, and SMOTE resampling were fitted strictly on training folds to prevent data leakage. "
    "Model tuning employed 5-fold cross-validated grid search, while final generalizability was audited via nested 10-fold CV."
)

# P35: Evaluation metrics & utility rule
p35_text = (
    "The 48-condition factorial design crossed 4 classifiers (RF, SVM, DT, LR), 3 sampling strategies (None, SMOTE, Random Under-sampling), "
    "and 4 preprocessors. Hyperparameters were tuned via 5-fold grid search. Model selection followed an explicit utility rule: "
    "maximize recall subject to precision >= 60.0% (to prevent advisor alert fatigue) and ROC-AUC >= 0.90."
)

# P36: Metrics definition
p36_text = (
    "Metrics included Recall (sensitivity), Precision, Specificity, F1-Score, Accuracy, and ROC-AUC. We computed 95% bootstrap "
    "confidence intervals (1,000 iterations) to quantify estimation uncertainty on the 3,017 test cases."
)

# P38: Interpretability methods
p38_text = (
    "Global interpretability used TreeSHAP [19] on the probability scale over 800 background samples. Local fidelity was examined "
    "using KernelSHAP and LIME [13], computing top-3 feature attribution concordance across test instances."
)

# P40: Fairness audit methods
p40_text = (
    "Fairness was evaluated on the 3,017 test students across five axes: Gender, Educational Modality, Marital Status, Quota Status, "
    "and Home Computer Ownership (digital access). We evaluated Disparate Impact (DI, 80% rule [0.80, 1.25]), Statistical Parity "
    "Difference (SPD), Equal Opportunity Difference (EOD, female vs. male recall gap), and structural proxy risks."
)

# P42: Governance methods
p42_text = (
    "The framework establishes a proposed institutional governance charter [2] structured across five operational pillars: "
    "Policy, Transparency, Accountability, Risk Management, and Continuing Audit. We validate risk probability calibration "
    "using Brier scores to establish operational risk tiers (<0.40 safe, 0.40-0.70 watchlist, >0.70 urgent)."
)

# P46: Phase 1 Results - active vs post-mortem
p46_text = (
    "The 80/20 stratified split yielded 12,067 training students and 3,017 held-out test students (2,722 active enrolled cohort, "
    "295 post-mortem records). Model performance remained robust across both subsets (active recall 80.8%; post-mortem recall 95.2%)."
)

# P50: Empirical patterns
p50_text = (
    "Three empirical patterns characterize the cohort: (1) An attendance cliff (Fig. 3), where dropout reaches 88.7% for "
    "attendance <75%; (2) Modality shift, where evening PROEJA students show elevated dropout (36.4%); and (3) Digital inequality, "
    "where students without a home computer exhibit a 28.5% dropout rate compared to 19.8% for computer owners."
)

# P54: RF Champion & Confusion Matrix
p54_text = (
    "The Random Forest champion (SMOTE, 100 trees, max_depth=12) achieved 84.8% recall (95% CI [82.0%, 87.4%]), 83.6% precision "
    "[81.0%, 86.4%], 92.9% accuracy [91.9%, 93.8%], F1 of 0.842 [0.820, 0.862], and ROC-AUC of 0.951 [0.939, 0.961]. On the 3,017 "
    "test students (676 dropouts, 2,341 completed), the exact confusion matrix confirms: TP=573, FP=112, TN=2,229, FN=103. The model "
    "generates 22.7 alerts per 100 students, capturing 84.8% of dropouts while maintaining a 5.1:1 true-to-false alert ratio."
)

# P55: Baseline benchmarks, SVM Trade-off & Utility Rule
p55_text = (
    "Alternative models failed operational requirements. While Support Vector Machines (SVM) achieved nominal recall of 91.4% "
    "(618/676 dropouts), precision collapsed to 23.1% (AUC = 0.591), generating 2,050 false alarms (88.4 alerts/100 students) and "
    "overwhelming advising capacity. Decision Trees overfit (86.4% accuracy, 0.887 AUC). Model selection adhered to the constrained "
    "utility rule: maximize recall subject to precision >= 60.0% and AUC >= 0.90. The Random Forest champion satisfied this constraint. "
    "Baseline benchmarks confirm necessity: a majority-class baseline yields 0.0% recall, while an attendance-only heuristic (<75%) "
    "achieves 95.7% precision but captures only 6.7% recall (F1 = 0.126), missing 93.3% of vulnerable students."
)

# P57: Global SHAP attributions
p57_text = (
    "TreeSHAP attributions on 800 background students indicate that academic performance dominates predictions: First-year GPA "
    "contributes 52.8% of total attribution, attendance accounts for 10.4%, and failed course count contributes 8.1%. Together, "
    "these top-3 features account for 71.3% of feature attribution share across the 15-feature space."
)

# P58: Beeswarm plot text
p58_text = (
    "From the beeswarm plot (Fig. 4), high GPA (red points) strongly drives negative SHAP values, protecting students from dropout. "
    "Low attendance (<75%) and lack of home computer ownership drive positive SHAP values toward dropout risk."
)

# P62: Local explanations & SHAP-LIME concordance
p62_text = (
    "Local explanations provide individual recourse profiles. To evaluate local explanation stability, we audited top-3 feature concordance "
    "between TreeSHAP and LIME across 100 representative archetypes, obtaining a mean Jaccard concordance of 0.724 +/- 0.081. While "
    "slight ranking variations occur on borderline cases, GPA and attendance consistently emerge as primary drivers in both methods."
)

# P63: Student #37 exemplar
p63_text = (
    "For borderline student #37 (predicted risk 50.8%), TreeSHAP attributes 0.18 risk increase to first-year GPA (1.92) and 0.09 to "
    "accumulated course failures, while good attendance (86.0%) contributes -0.11 protective risk. Advisors can thus deliver targeted tutoring."
)

# P65: Fairness audit dashboard text & structural proxy
p65_text = (
    "Fairness audits across the 3,017 test students reveal nuanced trade-offs across the five protected axes (Fig. 5). Quota-admitted "
    "students show favorable parity (DI = 1.042; EOD = +0.015). Students lacking home computers exhibit DI = 1.442; while above 1.25, "
    "this reflects elevated empirical dropout (28.5% vs. 19.8%) rather than algorithmic bias. Auxiliary modeling revealed that student "
    "age serves as a structural proxy for evening PROEJA modality (AUC = 0.892), whereas gender (0.617) and income (0.679) remain un-proxied."
)

# P70: Gender Disparity Deep-Dive
p70_text = (
    "A significant disparity was detected in gender: female students exhibit DI = 0.707 (below the 0.80 threshold) and a sensitivity "
    "gap of -5.73 percentage points (female recall 81.67% [254/311] vs. male recall 87.40% [319/365]; EOD = -0.0573). Female selection rate "
    "was 19.00% (304/1,600) compared to male selection rate of 26.89% (381/1,417), partly mirroring lower empirical female dropout (19.44% "
    "vs. 25.76%). However, the 5.73% sensitivity deficit means female dropouts are disproportionately missed by uniform screening."
)

# P71: Mitigation Trade-off
p71_text = (
    "To address the female sensitivity gap, we evaluated pre-processing and post-processing mitigations. In-processing AIF360 Reweighing "
    "raised precision to 94.5% but depressed overall recall to 79.4%, missing additional dropouts. Conversely, post-hoc threshold adjustment "
    "setting female threshold to tau=0.44 equalizes recall to 87.2% with a negligible precision reduction (81.4%), providing an optimal "
    "institutional compromise."
)

# P72: Institutional power
p72_text = (
    "The audit confirms that model thresholds govern institutional resource allocation: lowering thresholds captures more vulnerable "
    "students but increases false alarms. Institutions must balance advising budgets against dropout intervention targets."
)

# P73: Duplicate paragraph - CLEAR IT
# We set text to empty in doc.paragraphs[73]

# P75: Risk Calibration & Reliability
p75_text = (
    "Probability calibration was validated via Brier scores and reliability curves. The Random Forest achieved a Brier score of 0.0526, "
    "representing a 69.7% skill improvement over the 0.1738 empirical prevalence baseline. Probabilities map reliably to three actionable "
    "risk tiers: Safe (<0.40; empirical dropout 4.2%), Watchlist (0.40-0.70; empirical dropout 20.4%), and Urgent Intervention (>0.70; "
    "empirical dropout 91.2%), providing empirical justification for the 0.50 binary classification threshold."
)

# P76: Proposed 5 Governance Pillars
p76_text = (
    "To govern operational deployment, we articulate five proposed governance policy pillars: (1) Policy Charter establishing "
    "advisory-only deployment; (2) Algorithmic Transparency providing students explainability summaries; (3) Human Accountability "
    "requiring advisor review before intervention; (4) Risk Management enforcing quarterly drift monitoring; and (5) Independent Audit "
    "maintaining student appeal rights under Brazilian LGPD regulations."
)

# P78: Conclusion Summary
p78_text = (
    "This work presented an Explainable AI Governance Framework for first-year dropout early warning, operationalizing high-recall "
    "prediction (84.8% recall, 83.6% precision, 0.951 AUC), dual-tier explainability (71.3% attribution on top-3 features), and comprehensive "
    "fairness audits. The framework demonstrates that predictive accuracy must be paired with fairness evaluations and policy safeguards."
)

# P79: Conclusion Findings
p79_text = (
    "Fairness audits uncovered a 5.73 percentage point female recall gap and digital access disparities, which post-hoc threshold optimization "
    "successfully mitigates. Calibrated risk bands enable tiered academic triage without overwhelming advisor resources."
)

# P80: Limitations and Future Work
p80_text = (
    "Limitations include evaluation within a single multi-campus institution and reliance on retrospective cohorts. Future work will "
    "evaluate multi-institutional transferability, dynamic semester-by-semester trajectories, and longitudinal trials of the governance charter."
)

# References: Repair [9] and [10]
ref_9_text = (
    "[9] Y. Zhang and S. Yang, \"Teacher Performance Appraisal System in Colleges and Universities Using Fuzzy Genetic Algorithm,\" "
    "Math. Probl. Eng., vol. 2022, Art. no. 8415291, pp. 1-10, 2022."
)
ref_10_text = (
    "[10] L. Zhou, \"Performance Evaluation of Basic Education Informatization Based on BP Neural Network,\" "
    "Mob. Inf. Syst., vol. 2022, Art. no. 9631623, pp. 1-9, 2022."
)

# Apply all paragraph updates
p_map = {
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
    73: "",  # Cleared duplicate!
    75: p75_text,
    76: p76_text,
    78: p78_text,
    79: p79_text,
    80: p80_text,
    90: ref_9_text,
    91: ref_10_text
}

# Preserve font and styling: instead of p.text = ..., replace text in runs or keep original formatting!
for p_idx, text in p_map.items():
    p = doc.paragraphs[p_idx]
    if len(text) == 0:
        p.text = ""
        # minimize height of empty paragraph
        p.paragraph_format.space_before = 0
        p.paragraph_format.space_after = 0
        p.paragraph_format.line_spacing = 0.1
    else:
        # Keep the runs formatting intact!
        if len(p.runs) > 0:
            first_run = p.runs[0]
            font_name = first_run.font.name
            font_size = first_run.font.size
            bold = first_run.bold
            italic = first_run.italic
            
            # Clear existing runs except the first
            p.text = ""
            r = p.add_run(text)
            r.font.name = font_name if font_name else "Times New Roman"
            if font_size:
                r.font.size = font_size
            r.bold = bold
            r.italic = italic
        else:
            p.text = text

doc.save("paper_review/research_paper_final_draft.docx")
print("Saved paper_review/research_paper_final_draft.docx with preserved font styles and calibrated text.")

