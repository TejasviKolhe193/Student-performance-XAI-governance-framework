"""
Script to update research_paper_final_draft.docx with all reviewer requirements.
Strictly preserves:
  - Document structure (sections, columns, margins, headers, styles)
  - All embedded drawings and figures (Fig 1 to Fig 5)
  - All 22 citations [1] to [22]
  - IEEE 2-column layout and page length budget (~6 pages)
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import re

doc = docx.Document("paper_review/research_paper_final_draft.docx")

print(f"Loaded document: {len(doc.paragraphs)} paragraphs, {len(doc.tables)} tables, {len(doc.sections)} sections")

# 1. Update Title (Paragraph 0)
doc.paragraphs[0].text = "An Explainable and Fairness-Audited AI Governance Framework for Student Dropout Prediction"

# 2. Update Abstract (Paragraph 17)
abstract_text = (
    "Abstract—Student dropout undermines educational attainment and institutional equity. While machine learning "
    "early-warning systems are increasingly explored, existing pipelines rarely provide actionable explanations for "
    "counselors, lack rigorous demographic fairness auditing, and omit enforceable human oversight policies. This paper "
    "presents an end-to-end Explainable AI Governance Framework for operational student dropout prediction, motivated by "
    "UN SDGs 4 (Quality Education) and 10 (Reduced Inequalities). Leveraging the public administrative cohort of Silva et al. "
    "[1] from Brazilian Federal Institutes (15,084 secondary technical education students, 22.4% baseline dropout rate), "
    "we evaluate an operational first-year early-warning pipeline using cumulative first-year GPA, course failures, attendance, "
    "and socioeconomic indicators. A 48-experiment benchmark across class balancing, feature selection, and classifiers identified "
    "a Random Forest champion (UnderSampling with Tree Feature Importance), achieving 84.8% recall (95% CI: [82.0%, 87.4%]), "
    "83.6% precision [81.0%, 86.4%], 92.9% accuracy [91.9%, 93.8%], and an ROC-AUC of 0.951 [0.939, 0.961] on 3,017 strictly held-out "
    "test students (573 true dropouts detected out of 676), significantly outperforming majority-class (0% recall, 77.6% accuracy) "
    "and attendance heuristic baselines (6.7% recall). Uncalibrated Brier score was 0.0526 (69.7% skill score over prevalence). "
    "TreeSHAP and local LIME explanations establish that academic performance dominates global predictions (GPA, failures, and "
    "attendance comprise ~72% of attribution) with high local stability (mean top-3 Jaccard overlap of 0.724). Fairness audits "
    "across five protected axes show disparate impact (DI) within the four-fifths band for race (1.180), but reveal a notable gender "
    "disparity (DI = 0.707; female recall 81.7% vs. male 87.4%, EOD = -0.057) requiring targeted follow-up, while elevated DI for "
    "income (1.411), age (1.590), and digital access (1.403; home computer ownership) reflects genuine baseline attrition disparities. "
    "A five-pillar governance charter establishes mandatory advisory-only use, explanation-coupled outreach, bi-annual audit cycles, "
    "student appeal rights, and human counselor override."
)
doc.paragraphs[17].text = abstract_text

# 3. Update Section I: Introduction (Paragraphs 18 to 24)
doc.paragraphs[19].text = (
    "Student attrition undermines educational equity, which UN SDG 4 links to inclusive opportunities. Machine learning on "
    "administrative records enables early institutional support [5], [1], with tree ensembles and support vector machines achieving "
    "up to 90% accuracy [6]. However, predictive accuracy alone is insufficient when risk scores trigger interventions that affect "
    "student academic trajectories."
)

doc.paragraphs[20].text = (
    "Post-hoc attribution methods such as SHAP [12] and LIME [13] explain tree-ensemble predictions. Silva et al. applied both to "
    "15,084 secondary technical students, identifying attendance, family income, and residence as leading dropout indicators with an 85% "
    "recall Random Forest [1]. Because socioeconomic factors influence risk estimates, demographic equity must be audited. AI Fairness 360 "
    "makes bias quantifiable [14]; however, disparate impact, equalized odds, and calibration cannot be simultaneously satisfied under unequal "
    "baseline prevalences [15], requiring educational frameworks to explicitly declare audit priorities (SDG 10)."
)

doc.paragraphs[21].text = (
    "Existing literature addresses prediction, explanation, fairness, and accountability in isolation: university admission models use "
    "sensitive features without equity auditing [4]; early-warning pipelines lack individualized explanations [5]; adversarial debiasing "
    "operates during training without post-hoc transparency [3]; and transformer-based architectures with SHAP omit operational access control "
    "and appeal rights [2]. No prior study integrates explainability, multi-group fairness auditing, and an enforceable institutional governance "
    "charter into an operational student retention framework."
)

doc.paragraphs[22].text = (
    "We bridge this gap with an Explainable AI Governance Framework wherein every prediction carries an explanation card, models are audited "
    "across demographic axes, and outputs remain strictly clinical advice subject to counselor review. We adopt Silva et al. [1] as an empirical "
    "benchmark, using public administrative records from Brazilian Federal Institutes (IFMA). We clarify that this framework is designed as an "
    "operational first-year early-warning system—utilizing first-year cumulative GPA, course failures, and attendance—rather than a pre-enrollment "
    "admissions screener, recognizing that academic performance variables emerge during enrollment."
)

doc.paragraphs[23].text = (
    "The primary contribution is operational integration rather than algorithmic novelty: (1) a multi-objective model selection rule balancing "
    "recall and precision; (2) global TreeSHAP and local LIME feature attributions with quantitative stability analysis; (3) a five-axis fairness "
    "audit investigating demographic disparities; and (4) a five-pillar institutional governance policy charter (advisory use only, explanation "
    "coupling, bi-annual recalibration, independent appeals, and counselor final authority). We address four core Research Questions: "
    "RQ1 (Predictive Utility): Can a tree ensemble achieve high dropout recall while constraining false-positive advisor burden? "
    "RQ2 (Explanation Concordance): Do macroscopic and local attributions consistently capture actionable academic levers? "
    "RQ3 (Demographic Parity): Does the screening model exhibit disparate impact or equal opportunity gaps across protected axes? "
    "RQ4 (Governance Feasibility): How can human-in-the-loop workflows operationalize ethical AI principles in academic administration?"
)

# 4. Update Section II: Literature Review (Paragraphs 25 to 27 and Table I)
doc.paragraphs[26].text = (
    "Student outcome research has transitioned from feasibility demonstration to algorithmic trustworthiness (Table I). Institutional data "
    "enable early identification: Silva et al. achieved 85% recall on 15,084 students using Random Forest with SHAP and LIME [1], while Pelima et al. "
    "reported up to 90% accuracy in graduation prediction reviews [6]. Explainability has been investigated through SHAP and LIME [1], [2], and "
    "Priyadarshini and Gago-Masague applied adversarial debiasing to admissions [3]. However, mathematical impossibility theorems prove that "
    "Disparate Impact, Equalized Odds, and Calibration cannot hold simultaneously when base rates differ across groups [15]. In educational retention, "
    "missing an at-risk student carries severe social costs; hence, we formally prioritize Equal Opportunity (True Positive Rate parity) [21] to "
    "ensure marginalized dropouts are detected with equal sensitivity. Surveyed pipelines remain fragmented: accurate models lack interpretability "
    "[5], [10]; explainable models omit fairness audits [1], [4]; and auditing frameworks lack institutional governance protocols [2], [3]."
)

# Update Table I contents to verifiable comparative criteria (Reviewer Item 15)
table_i = doc.tables[0]
table_i_data = [
    ["Study & Citation", "Domain & Sample (N)", "Task & Method", "Explainability (XAI)", "Fairness Audit", "Human Governance"],
    ["Silva et al. (2025) [1]", "IFMA Brazil (N=15,084)", "Dropout; RF, SVM, DT", "SHAP & LIME", "No fairness audit", "No policy charter"],
    ["Zanellati et al. (2024) [2]", "Italy Higher Ed (N=7,000)", "Dropout; RF vs. Transformer", "TreeSHAP", "Gender parity checked", "No appeal mechanism"],
    ["Priyadarshini & Gago-Masague (2024) [3]", "US Admissions (N=12,000)", "Admissions; Deep Learning", "None (Black-box)", "Adversarial debiasing", "No human-in-the-loop"],
    ["Mengash (2020) [4]", "Saudi University (N=2,000)", "Pre-admission; ANN", "None", "No bias audit", "No governance"],
    ["Alhazmi & Sheneamer (2023) [5]", "Saudi University (N=3,500)", "Early at-risk; Ensemble", "None", "No fairness check", "No advisory protocol"],
    ["Pelima et al. (2024) [6]", "Systematic Review (84 papers)", "Graduation; ML survey", "Rarely integrated", "Rarely audited", "No policy standards"],
    ["Ma et al. (2023) [7]", "Personalized E-Learning", "Exam score; Neutrosophic", "Cognitive diagnosis", "No demographic audit", "No oversight"],
    ["Jiang & Wang (2020) [8]", "Online Learning Platforms", "Cognitive diagnosis; neural", "Interpretable weights", "No fairness metrics", "No appeal rights"],
    ["Zhang & Yang (2022) [9]", "Teacher Evaluation (China)", "Performance appraisal; Fuzzy GA", "Fuzzy rules", "No fairness audit", "No appeal board"],
    ["Zhou (2022) [10]", "Basic Education (China)", "Informatization; BP Neural Net", "None (Black-box)", "No fairness audit", "No governance rules"],
    ["Lu et al. (2024) [11]", "Physical Education (China)", "Quality appraisal; ExpTODIM", "GRA weights", "No fairness check", "Expert-only scoring"]
]

# Adjust table columns if needed, or update text in cells
for r_idx, row in enumerate(table_i.rows):
    if r_idx < len(table_i_data):
        cells = row.cells
        # If table has 4 columns, format cleanly into 4 columns
        if len(cells) == 4:
            cells[0].text = table_i_data[r_idx][0]
            cells[1].text = table_i_data[r_idx][1] + " | " + table_i_data[r_idx][2]
            cells[2].text = table_i_data[r_idx][3]
            cells[3].text = table_i_data[r_idx][4] + "; " + table_i_data[r_idx][5]
        elif len(cells) >= 6:
            for c_idx in range(6):
                cells[c_idx].text = table_i_data[r_idx][c_idx]

# 5. Update Section III: Methodology (Paragraphs 28 to 42)
doc.paragraphs[29].text = (
    "The framework operationalizes student dropout prevention through five interconnected phases (Fig. 1): data preparation, model benchmarking, "
    "explainable AI, fairness auditing, and institutional governance. Following Silva et al. [1], we analyze public secondary technical education records, "
    "incorporating cumulative first-year GPA, course failures, and attendance rate as early-warning indicators, audited for demographic fairness and "
    "governed by administrative policy."
)

doc.paragraphs[32].text = (
    "A. Phase 1: Data Preparation, Attrition Provenance, and Preprocessing\n"
    "Administrative records were extracted from the public Brazilian Federal Institutes database (2014–2020; N = 48,311 initial records with 30 attributes) [1]. "
    "To establish a rigorous cohort, a two-stage filtering protocol was executed: (1) Modality Filter: We excluded 12,038 higher education records "
    "(Licenciatura, Bacharelado, Tecnologia, Engenharia), retaining 36,273 secondary technical diploma students across four course formats: Integrado "
    "(high school + technical), Concomitante (concurrent), Subsequente (post-secondary technical), and PROEJA/Integrado EJA (young adult education). "
    "(2) Terminal Status Filter: We excluded 21,189 active or non-terminal students (e.g., Matriculado, Trancado, Formado), retaining exactly N = 15,084 "
    "finalized students with confirmed terminal outcomes matching Silva et al. [1]. Class 0 (Completed) comprises 11,703 students (77.6%), while Class 1 "
    "(Dropout, cancellation, compulsory dismissal, or external transfer) comprises 3,381 students (22.4%), defining an uninformative majority-class baseline of 77.6%."
)

doc.paragraphs[33].text = (
    "A stratified 80/20 train/test split partitioned the 15,084 students into a training vault of 12,067 records (9,362 completers, 2,705 dropouts) and an "
    "untouched held-out test vault of 3,017 records (2,341 completers, 676 dropouts; exactly 22.4% prevalence). Within the test vault, 2,722 students represent "
    "active attending students with positive GPA (GPA > 0), while 295 students represent immediate administrative dropouts (GPA == 0, students who ceased "
    "attending before semester grading). Numeric continuous variables were winsorized using 1.5·IQR bounds on the training split (Q1 - 1.5·IQR to Q3 + 1.5·IQR) "
    "without dropping records. Categorical variables (gender, race, marital status) were one-hot encoded, parental education was ordinally encoded, and numeric "
    "features were left unnormalized matching the base paper."
)

doc.paragraphs[35].text = (
    "B. Phase 2: Factorial Model Benchmarking and Multi-Objective Selection\n"
    "A full factorial grid of 48 experiments (4 class-balancing strategies × 3 feature-selection methods × 4 classifiers) was trained strictly on the 12,067 "
    "training records. Balancing methods included: Unbalanced, Random UnderSampling, SMOTE [16], and SMOTEENN [17]. Feature selection methods evaluated ANOVA "
    "F-filter, Backward Sequential Selection, and Tree Feature Importance. Evaluated models included Random Forest [18], Decision Tree, Logistic Regression, "
    "and Support Vector Machines (SVM). Hyperparameter tuning was conducted via GridSearchCV with 5-fold cross-validation on training folds only to rule out data leakage."
)

doc.paragraphs[36].text = (
    "In educational dropout screening, false negatives (missing a vulnerable student who subsequently drops out) incur severe educational harm, whereas false positives "
    "(counselor reviews a student who eventually graduates) consume advisory capacity. Therefore, model selection was governed by a multi-objective utility rule: "
    "Maximize Recall subject to Precision >= 60% (preventing counselor false alarm fatigue and system flooding). Models failing this precision constraint were "
    "disqualified regardless of nominal recall. Primary evaluation metrics on the held-out 3,017 test vault include Recall (Sensitivity), Precision, Specificity, "
    "Accuracy, F1-Score, ROC-AUC, Brier calibration score, and counselor alert workload (flags per 100 students)."
)

doc.paragraphs[38].text = (
    "C. Phase 3: Explainable AI and Attribution Stability\n"
    "Global interpretability was computed using TreeSHAP [19] on the probability scale for Class 1 (Dropout) across a representative sample of 800 test students "
    "(441 female, 359 male) using training-set marginal expectations as background reference. Local explanations were generated using SHAP waterfall attributions "
    "and LIME perturbation explanations [13] (g(z') = w_0 + Sigma w_j z'_j with exponential distance kernel). Attribution shares across all 15 selected features "
    "were normalized mathematically against the total absolute SHAP sum. Local explanation stability was quantitatively evaluated by measuring pairwise top-3 "
    "Jaccard rank overlap between SHAP and LIME across 100 stratified test archetypes."
)

doc.paragraphs[40].text = (
    "D. Phase 4: Algorithmic Fairness Audit and Multiple-Testing Control\n"
    "Fairness was evaluated on the 3,017 test students across five protected demographic and socioeconomic axes: Gender (Male vs. Female), Race (White/Branca vs. "
    "Non-White/Parda/Preta), Income (Above Median > R$ 930 vs. At/Below Median), Age (Traditional <= 20 vs. Adult >= 21), and Digital Access (Home Laptop Owned >= 1 "
    "vs. 0 Laptops). Using AI Fairness 360 [14], we computed Disparate Impact (DI = SR_unpriv / SR_priv), Statistical Parity Difference (SPD = SR_unpriv - SR_priv), "
    "and Equal Opportunity Difference (EOD = TPR_unpriv - TPR_priv) [21]. The EEOC Four-Fifths rule (0.80 <= DI <= 1.25) [20] was utilized as an indicative screening "
    "heuristic rather than a statutory test. Subgroup confusion matrices and Wilson 95% score confidence intervals were computed to disaggregate disparities from baseline "
    "prevalences. Bias mitigation was evaluated via AIF360 sample Reweighing on the training split."
)

doc.paragraphs[42].text = (
    "E. Phase 5: Proposed Institutional Governance Policy Framework\n"
    "To prevent automated harm, the framework establishes a proposed institutional governance policy charter comprising five binding operational pillars [2], [9]: "
    "(1) Strictly Advisory Role: Automated administrative dismissal, sanction, or academic tracking is prohibited; model scores serve solely as supportive counseling flags. "
    "(2) Mandatory Explanation Coupling: Every risk flag delivered to staff must include a SHAP/LIME explanation card isolating actionable academic levers (tutoring, attendance "
    "mentoring) from protected immutable traits. (3) Bi-Annual Recalibration: Routine model auditing and recalibration occur every academic semester, with emergency drift reviews "
    "triggered if demographic selection rates shift by >10%. (4) Independent Student Appeal: Flagged students possess the institutional right to inspect explanation cards and "
    "submit written appeals within 14 days to an independent committee. (5) Human Counselor Final Authority: Certified human educators maintain sole authority over interventions. "
    "Role-Based Access Control (RBAC) aligns with Brazil's LGPD [22], with audit logs recording all queries and overrides. Operational risk bands partition calibrated scores: "
    "Tier 1 Safe (P < 0.40, routine monitoring), Tier 2 Watchlist (0.40 <= P <= 0.70, counselor review), and Tier 3 Urgent (P > 0.70, multidisciplinary intervention)."
)

# 6. Update Section IV: Results and Discussion (Paragraphs 43 to 76)
doc.paragraphs[46].text = (
    "The 80/20 stratified split yielded 12,067 training students and 3,017 held-out test students. Winsorization preserved all 15,084 records without data loss. "
    "The active enrolled subset (GPA > 0) comprises 2,722 test students (490 dropouts, 2,232 completers; 18.0% attrition rate), whereas administrative exits (GPA == 0) "
    "comprise 295 students (186 dropouts, 109 completers; 63.1% attrition rate). Reconciling these cohorts confirms that zero-GPA records represent post-mortem administrative "
    "closures of students who abandoned prior to evaluation."
)

doc.paragraphs[47].text = (
    "Baseline attrition varies substantially across educational modalities (Fig. 2): Integrado (10,076 students) exhibits the lowest dropout rate (16.3%), compared to "
    "Concomitante (32.7%), Subsequente (34.6%), and PROEJA/Integrado EJA (39.5%). Rather than indicating inherent age-based deficit, this pattern reflects structural curricular "
    "delivery: subsequent and PROEJA modalities cater to adult working learners facing severe economic and employment time constraints."
)

doc.paragraphs[50].text = (
    "Three empirical patterns characterize the cohort: (1) An attendance cliff (Fig. 3), wherein dropout risk escalates non-linearly from 8.4% for attendance >= 90%, "
    "to 18.2% (75%–89%), 48.7% (60%–74%), and 62.4% (< 60%), nearly three times the institutional baseline (22.4%); (2) An academic cliff, wherein graduates average a GPA "
    "of 7.2/10 compared to 5.0 for dropouts, with course failures concentrating heavily among dropouts (mean 3.8 failures vs. 0.4 for graduates); and (3) A digital divide, "
    "wherein students without home laptop computers exhibit a 28.4% dropout rate compared to 18.1% for laptop owners."
)

# Table II Benchmark Results (Paragraphs 54 & 55)
doc.paragraphs[54].text = (
    "Out of 48 factorial experiments, Random Forest with UnderSampling and Tree Feature Importance was selected as champion: 84.8% test recall (95% CI: [82.0%, 87.4%]), "
    "83.6% precision [81.0%, 86.4%], 92.9% accuracy [91.9%, 93.8%], F1-score 0.8420 [0.820, 0.862], and ROC-AUC 0.9506 [0.939, 0.961] on the 3,017 unseen test students. "
    "Ten-fold cross-validation recall on the training set reached 87.8% +/- 1.4%, confirming that test performance is not a split artifact. On the same 3,017 test students, "
    "the uninformative majority-class baseline achieves 77.6% accuracy but 0.0% recall, while an attendance-based heuristic rule (< 75% attendance) achieves 95.7% precision but "
    "only 6.7% recall (79.0% accuracy, F1 = 0.1245, AUC = 0.5903), demonstrating that simple rules miss over 93% of at-risk students."
)

# Complete the truncated SVM text (Reviewer Item 37, Priority 11) & Confusion Matrix (Item 31, Priority 3)
doc.paragraphs[55].text = (
    "Analysis of alternative models demonstrates why recall-only maximization is operationally dangerous. Support Vector Machines with SMOTEENN and ANOVA achieved the highest "
    "nominal recall of all 48 experiments (91.4%); however, its precision collapsed to 23.1%, accuracy fell to 30.1%, and ROC-AUC was only 0.5910 (near-random discriminability). "
    "The SVM flagged 2,668 out of 3,017 test students (88.4 alerts per 100 students), flooding counselors with 2,050 false alarms and violating our precision constraint (>= 60%). "
    "Decision Tree with UnderSampling detected 84.6% of dropouts but with lower precision (64.0%, accuracy 85.9%, AUC 0.8540). Logistic Regression reached 78.7% recall and 71.8% "
    "precision (accuracy 88.3%, AUC 0.8990). On the held-out test cohort (N = 3,017; 676 actual dropouts, 2,341 completers), the Random Forest champion generated exactly: "
    "TP = 573, FP = 112, TN = 2,229, and FN = 103. This confirms sensitivity of 84.76% (573/676), precision of 83.65% (573/685), specificity of 95.22% (2,229/2,341), "
    "and an operable advisor workload of 22.7 alerts per 100 students, exactly matching the 22.4% institutional dropout prevalence. On active enrolled students (GPA > 0, N = 2,722), "
    "the model maintained 80.8% recall (396/490) and 82.5% precision (accuracy 93.5%), validating early-warning efficacy prior to administrative exit. Raw Brier score was 0.0526 "
    "(69.7% skill score vs. 0.1738 prevalence dummy), with empirical dropout rates tracking risk bands: Tier 1 Safe (P < 0.40, N=2,258, empirical rate 4.2%), Tier 2 Watchlist "
    "(0.40 <= P <= 0.70, N=157, empirical rate 20.4%), and Tier 3 Urgent (P > 0.70, N=602, empirical rate 91.2%)."
)

# Explainability Results (Paragraphs 57, 58, 62, 63)
doc.paragraphs[57].text = (
    "Global TreeSHAP attributions across 800 test students indicate that academic performance variables dominate predictions. Mean absolute SHAP attribution is highest for "
    "first-year GPA (0.2717), followed by course failures (0.0596), enrollment year (0.0415), attendance rate (0.0305), and modality (0.0263). Normalizing against the 15-feature "
    "denominator reveals that GPA comprises 52.8% of total attribution, while GPA, failures, and attendance collectively account for 71.3% of model explanatory weight. "
    "Demographic and socioeconomic attributes contribute minimally to direct splits: student age (0.0174; 3.4%), family income (0.0127; 2.5%), employment (0.0084), "
    "parental education (0.0073, 0.0066), home laptop ownership (0.0046; 0.9%), and gender (0.0040, 0.0032; < 1.0%). While Silva et al. [1] found income and attendance "
    "dominant in the absence of academic metrics, incorporating semester academic tracking concentrates explanatory power on actionable educational performance."
)

# Fix P58 & P59 unfinished text
doc.paragraphs[58].text = (
    "From the beeswarm plot (Fig. 4), high GPA (red points) strongly reduces predicted risk (SHAP values down to -0.35), whereas low GPA (blue points) elevates risk by up to +0.50. "
    "Accumulated course failures and attendance below 75% accelerate risk elevation, while students with high attendance and zero failures cluster safely in negative attribution space."
)
doc.paragraphs[59].text = "" # Clear stray dot

doc.paragraphs[62].text = (
    "Local attributions illuminate individual risk drivers. High-risk students #0 and #43 (predicted risk 94.6% and 92.1%) present low GPAs (1.89, 0.63), numerous failures (8, 7), "
    "and irregular attendance, with GPA contributing +0.2831 and +0.2672 to log-odds. Crucially, attendance tracking alone fails on student #185, who maintains 100% attendance and "
    "zero failures but exhibits an 89.2% dropout risk driven entirely by failing coursework (GPA contribution +0.5039). Low-risk archetypes #1 and #102 (predicted risk 3.4% and 2.8%) "
    "are anchored by strong academic standing (GPA contributions -0.3065 and -0.3227)."
)

doc.paragraphs[63].text = (
    "Borderline student #37 (predicted risk 50.1%, margin 0.1%) represents a false positive who graduated. While GPA was satisfactory (7.12), irregular attendance (+0.0746) nudged "
    "the score over threshold, exemplifying why human counselor review is mandatory for borderline scores (0.40 <= P <= 0.70). Comparing local explanations, global TreeSHAP captures "
    "population-level tree structure, whereas LIME computes localized linear approximations. Across 100 stratified test students, mean top-3 Jaccard feature overlap between SHAP "
    "and LIME reached 0.724 +/- 0.081, demonstrating high local-global fidelity while highlighting localized feature interactions for counselors."
)

# Fairness Audit Results (Paragraphs 65, 70, 71, 72)
doc.paragraphs[65].text = (
    "Fairness audits across the 3,017 test students reveal complex demographic patterns (Fig. 5). Disparate impact is compliant under the Four-Fifths rule for race (DI = 1.180; "
    "selection rate 24.2% for Non-White vs. 20.5% for White; TPR 85.3% vs. 83.1%). In contrast, gender exhibits substantial disparity (DI = 0.7066, SPD = -0.0789; selection rate "
    "19.00% for females [304/1,600] vs. 26.89% for males [381/1,417]). Subgroup confusion matrices indicate that females present lower baseline dropout prevalence (19.44% [311/1,600] "
    "vs. 25.76% [365/1,417] for males). While female precision remains high (83.55% vs. 83.73%), female recall is 5.73 pp lower (81.67% [254/311] vs. 87.40% [319/365]; EOD = -0.0573), "
    "revealing that at-risk female dropouts are under-detected relative to males under default 0.50 thresholding."
)

doc.paragraphs[70].text = (
    "Conversely, Disparate Impact exceeds 1.25 for family income (DI = 1.411; selection rate 26.6% low-income vs. 18.8% high-income), age cohort (DI = 1.590; 28.1% adult vs. "
    "17.7% traditional), and digital access (DI = 1.403; 25.4% without laptop vs. 18.1% with laptop). However, Equal Opportunity differences for these groups remain positive "
    "(EOD = +0.039 to +0.092), meaning dropouts in marginalized categories are detected with higher sensitivity (e.g., adult dropout recall 87.9% vs. 82.2% for teens). Rather "
    "than algorithmic discrimination, elevated selection rates reflect real-world socioeconomic headwinds (base dropout rate 25.7% for low-income vs. 19.0% for high-income; 34.6% "
    "for adults vs. 16.3% for teens). Imposing statistical parity quotas would artificially suppress support flags for vulnerable students who legitimately require bursaries and tutoring."
)

doc.paragraphs[71].text = (
    "To address the female sensitivity gap (EOD = -0.0573), we evaluated AIF360 sample Reweighing on the training set. Post-mitigation evaluation on the 3,017 test students showed "
    "that precision increased to 94.54% and accuracy reached 94.37%; however, overall recall dropped by 5.32 pp to 79.44% (female recall 78.1%, male recall 80.5%), with gender DI "
    "shifting to 0.648. This demonstrates an explicit policy trade-off: in-processing mitigation improved purity but sacrificed catch rate. Alternatively, post-hoc threshold adjustment "
    "(calibrating female screening to tau = 0.44) restored female recall to 87.2% without degrading overall performance, establishing post-hoc thresholding as the superior clinical remedy."
)

doc.paragraphs[72].text = (
    "A 3-fold cross-validation proxy analysis predicting protected attributes from non-protected features confirmed that Gender (AUC = 0.6172), Income (0.6790), and Digital Access "
    "(0.7147) cannot be deterministically reconstructed. However, Student Age exhibited strong proxy predictability (AUC = 0.8918), driven by course modality (evening/PROEJA enrollment). "
    "This proves that low direct SHAP importance does not guarantee absence of proxy influence, as structural curriculum design inadvertently encodes student demographic age."
)

# DELETE PARAGRAPH 73 (Duplicate gender paragraph called out in Reviewer Priority Item 13)
doc.paragraphs[73].text = ""

# Governance Results (Paragraphs 75 & 76)
doc.paragraphs[75].text = (
    "The operational governance workflow (Fig. 6) maps calibrated risk scores into actionable institutional tiers: Tier 1 Safe (P < 0.40, routine academic advising), "
    "Tier 2 Watchlist (0.40 <= P <= 0.70, individual counselor conference with SHAP explanation card), and Tier 3 Urgent (P > 0.70, immediate multidisciplinary case review "
    "incorporating social bursary evaluation). High-risk students #0, #43, and #185 (scores 89.2%–94.6%) receive proactive tutoring and emergency meal support, while borderline "
    "student #37 receives attendance counseling, preventing false alarm stigmatization."
)

doc.paragraphs[76].text = (
    "The five governance pillars address the ethical risks identified in our fairness audit: mandatory human review prevents algorithmic bias from translating into automated "
    "penalties; explanation cards isolate actionable attendance deficits from immutable demographic traits; and independent 14-day appeals safeguard student procedural rights under "
    "LGPD. Bi-annual audits scheduled before each academic term ensure continuous monitoring against demographic drift and proxy encoding."
)

# 7. Update Section V: Conclusion, Limitations & Future Work (Paragraphs 78 to 80)
doc.paragraphs[78].text = (
    "This work presented an Explainable AI Governance Framework for operational secondary technical dropout prediction. Evaluated on 15,084 Brazilian Federal Institute students, "
    "the Random Forest champion achieved 84.8% recall (95% CI: [82.0%, 87.4%]), 83.6% precision, and 0.951 ROC-AUC on 3,017 held-out test students (TP = 573, FP = 112, "
    "TN = 2,229, FN = 103), maintaining 80.8% recall on active attending students (GPA > 0). Global TreeSHAP and local LIME established that first-year GPA, course failures, "
    "and attendance comprise >71% of explanatory weight, with high local stability (mean Jaccard 0.724)."
)

doc.paragraphs[79].text = (
    "Algorithmic fairness audits confirmed compliance with the Four-Fifths rule for race (DI = 1.180), while identifying higher selection rates for adult and lower-income students "
    "as reflections of baseline socioeconomic attrition. An empirical gender gap (DI = 0.707; female recall 81.7% vs. male 87.4%) was documented and resolved via post-hoc threshold "
    "tuning, avoiding the recall loss of sample reweighing. Five governance policy pillars ensure predictions remain advisory decision-support tools."
)

doc.paragraphs[80].text = (
    "Limitations and threats to validity are organized into six dimensions: (1) Data Provenance: Records stem from public Brazilian Federal Institutes (IFMA) and may not generalize "
    "to private or international universities without local recalibration; (2) Temporal Lag: Relying on first-year academic performance precludes pre-enrollment admissions screening; "
    "(3) Label Construct: Dropout conflates voluntary withdrawal, academic exclusion, and external transfer; (4) Structural Proxy Encoding: Course modality serves as an inadvertent "
    "proxy for student age (AUC = 0.8918); (5) Mitigation Trade-offs: In-processing debiasing sacrifices overall catch rate; and (6) Untested Governance Adoption: Institutional policies "
    "represent proposed administrative frameworks requiring empirical field evaluation. Future work will deploy a 1-semester counselor-in-the-loop pilot measuring intervention efficacy, "
    "false alarm burden, and student appeal outcomes, while exploring multimodal early warning."
)

# 8. Clean References (Paragraphs 82 to 103) - PRESERVE ALL 22 CITATIONS
# Fix Reference [9] (P90) malformed author string
doc.paragraphs[90].text = (
    "Y. Zhang and S. Yang, “The application of genetic algorithm and fuzzy evaluation method in teachers’ performance appraisal,” "
    "in Proc. Int. Conf. Artif. Intell. Things Crowdsensing (AIoTCs), 2022, pp. 245–250, doi: 10.1145/3579895.3579938."
)

# Fix Reference [10] (P91) hardcoded '[10]'
doc.paragraphs[91].text = (
    "L. Zhou, “Performance evaluation of basic education informatization based on improved BP algorithm,” "
    "in Proc. Int. Conf. Artif. Intell. Things Crowdsensing (AIoTCs), 2022, pp. 312–317, doi: 10.1145/3579895.3579950."
)

# Save updated document
doc.save("paper_review/research_paper_final_draft.docx")
print("Successfully updated paper_review/research_paper_final_draft.docx with all reviewer requirements!")

