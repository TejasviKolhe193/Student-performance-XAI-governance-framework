"""
Strict 6-Page IEEE Precision Updater for research_paper_final_draft.docx
========================================================================
Implements every single reviewer suggestion with exact word-budgeting to
guarantee that the document remains STRICTLY 6 PAGES in native IEEE format.
"""

import docx

doc = docx.Document("paper_review/research_paper_final_draft_ORIGINAL_BACKUP.docx")

# 1. Title (P0)
doc.paragraphs[0].text = "An Explainable and Fairness-Audited AI Governance Framework for Student Dropout Prediction"

# 2. Abstract (P17)
doc.paragraphs[17].text = (
    "Abstract—Student dropout undermines educational attainment and institutional equity. While machine learning "
    "early-warning systems are increasingly explored, existing pipelines rarely provide actionable explanations for "
    "counselors, lack demographic fairness auditing, and omit enforceable human oversight policies. This paper "
    "presents an Explainable AI Governance Framework for operational student dropout prediction, motivated by "
    "UN SDGs 4 (Quality Education) and 10 (Reduced Inequalities). Leveraging the public administrative cohort of Silva et al. "
    "[1] from Brazilian Federal Institutes (15,084 secondary technical education students, 22.4% baseline dropout rate), "
    "we evaluate an operational first-year early-warning pipeline using cumulative first-year GPA, course failures, attendance, "
    "and socioeconomic indicators. A 48-experiment benchmark across class balancing, feature selection, and classifiers identified "
    "a Random Forest champion (UnderSampling with Tree Feature Importance), achieving 84.8% recall (95% CI: [82.0%, 87.4%]), "
    "83.6% precision [81.0%, 86.4%], 92.9% accuracy [91.9%, 93.8%], and an ROC-AUC of 0.951 [0.939, 0.961] on 3,017 held-out "
    "test students (573 true dropouts detected out of 676), significantly outperforming majority-class (0% recall, 77.6% accuracy) "
    "and attendance heuristic baselines (6.7% recall). Uncalibrated Brier score was 0.0526 (69.7% skill score over prevalence). "
    "Global TreeSHAP and local LIME establish that academic performance dominates predictions (GPA, failures, and attendance "
    "comprise 71.3% of attribution) with high local stability (mean top-3 Jaccard overlap of 0.724). Fairness audits across five "
    "protected axes show disparate impact (DI) compliant for race (1.180), but reveal a notable gender disparity (DI = 0.707; female "
    "recall 81.7% vs. male 87.4%, EOD = -0.057) requiring targeted follow-up, while elevated DI for income (1.411), age (1.590), and "
    "digital access (1.403; home laptop ownership) reflects genuine baseline attrition disparities. A proposed five-pillar governance "
    "charter establishes advisory-only use, explanation coupling, bi-annual recalibration, student appeal rights, and counselor final authority."
)

# 3. Section I: Introduction (P19 - P24)
doc.paragraphs[19].text = (
    "Student attrition undermines educational equity, which UN SDG 4 links to inclusive opportunities. Machine learning on "
    "administrative records enables early institutional support [5], [1], with tree ensembles and support vector machines achieving "
    "up to 90% accuracy [6]."
)

doc.paragraphs[20].text = (
    "Accuracy alone is insufficient when predictions trigger academic interventions. Attribution methods such as SHAP [12] and "
    "LIME [13] explain tree-ensemble predictions. Silva et al. applied both to 15,084 secondary technical students, identifying attendance, "
    "family income, and residence as leading dropout indicators with an 85% recall Random Forest [1]. Because socioeconomic factors influence "
    "risk estimates, demographic equity must be audited. AI Fairness 360 makes bias quantifiable [14]; however, disparate impact, equalized "
    "odds, and calibration cannot hold simultaneously under unequal baseline prevalences [15], requiring educational frameworks to explicitly "
    "declare audit priorities (SDG 10)."
)

doc.paragraphs[21].text = (
    "Existing literature addresses prediction, explanation, fairness, and accountability in isolation: university admission models use "
    "sensitive features without equity auditing [4]; early-warning pipelines lack individualized explanations [5]; adversarial debiasing "
    "operates during training without post-hoc transparency [3]; and transformer architectures with SHAP omit operational access control "
    "and appeal rights [2]. No prior study integrates explainability, multi-group fairness auditing, and an enforceable institutional governance charter."
)

doc.paragraphs[22].text = (
    "We bridge this gap with an Explainable AI Governance Framework wherein every prediction carries an explanation card, models are audited "
    "across demographic axes, and outputs remain strictly clinical advice subject to counselor review. We adopt Silva et al. [1] as an empirical "
    "benchmark on public Brazilian Federal Institutes (IFMA) data. Crucially, this framework is designed as an operational first-year early-warning "
    "system—utilizing first-year cumulative GPA, course failures, and attendance—rather than a pre-enrollment admissions screener, recognizing that "
    "academic performance variables emerge during enrollment."
)

doc.paragraphs[23].text = (
    "The primary contribution is operational integration: (1) a multi-objective model selection rule balancing recall and precision; (2) global "
    "TreeSHAP and local LIME attributions with quantitative stability analysis; (3) a five-axis fairness audit investigating demographic disparities; "
    "and (4) a five-pillar institutional governance policy charter. We address four explicit Research Questions: RQ1 (Predictive Utility), RQ2 "
    "(Explanation Concordance), RQ3 (Demographic Parity), and RQ4 (Governance Feasibility)."
)

doc.paragraphs[24].text = (
    "Section II reviews the literature, Section III details the methodology, Section IV presents experimental and audit results, and Section V "
    "concludes with limitations and future work."
)

# 4. Section II: Literature Review (P26)
doc.paragraphs[26].text = (
    "Student outcome research has transitioned from feasibility demonstration to algorithmic trustworthiness (Table I). Institutional datasets "
    "enable early identification: Silva et al. achieved 85% recall on 15,084 students using Random Forest with SHAP and LIME [1], while Pelima et al. "
    "reported up to 90% accuracy in graduation prediction reviews [6]. Explainability has been investigated through SHAP and LIME [1], [2], and "
    "Priyadarshini and Gago-Masague applied adversarial debiasing to admissions [3]. However, mathematical impossibility theorems prove that "
    "Disparate Impact, Equalized Odds, and Calibration cannot hold simultaneously when base rates differ across groups [15]. In educational retention, "
    "missing an at-risk student carries severe social costs; hence, we formally prioritize Equal Opportunity (True Positive Rate parity) [21] to "
    "ensure marginalized dropouts are detected with equal sensitivity. Surveyed pipelines remain fragmented: accurate models lack interpretability "
    "[5], [10]; explainable models omit fairness audits [1], [4]; and auditing frameworks lack institutional governance protocols [2], [3]."
)

# Clean and Compact Table I
t1 = doc.tables[0]
t1_rows = [
    ["Study & Citation", "Domain & Sample (N)", "Key Findings & Method", "Gaps Addressed"],
    ["Silva et al. (2025) [1]", "IFMA Brazil (N=15,084)", "85% recall; RF with SHAP & LIME", "No fairness audit or policy charter"],
    ["Zanellati et al. (2024) [2]", "Italy Higher Ed (N=7,000)", "81% recall; Transformer, TreeSHAP", "Gender checked; no appeal board"],
    ["Priyadarshini et al. (2024) [3]", "US Admissions (N=12,000)", "Adversarial debiasing in DL", "Training only; no post-hoc XAI"],
    ["Mengash (2020) [4]", "Saudi University (N=2,000)", "Pre-admission prediction; ANN", "Sensitive data; no equity audit"],
    ["Alhazmi & Sheneamer (2023) [5]", "Saudi University (N=3,500)", "Early at-risk prediction; Ensemble", "No explanations or fairness check"],
    ["Pelima et al. (2024) [6]", "Systematic Review (84 papers)", "Graduation review; RF, SVM <=90% acc", "XAI and fairness rarely integrated"],
    ["Ma et al. (2023) [7]", "Personalized E-Learning", "Exam prediction; Neutrosophic", "No demographic audit or oversight"],
    ["Jiang & Wang (2020) [8]", "Online Learning Platforms", "Cognitive diagnosis; neural weights", "Interpretable; no fairness metric"],
    ["Zhang & Yang (2022) [9]", "Teacher Evaluation (China)", "Performance appraisal; Fuzzy GA", "Fuzzy logic; no appeal rights"],
    ["Zhou (2022) [10]", "Basic Education (China)", "Informatization; BP Neural Net", "Black box; no transparency rules"],
    ["Lu et al. (2024) [11]", "Physical Education (China)", "Quality appraisal; ExpTODIM", "Expert weights; no demographic audit"]
]

for r_i, r_data in enumerate(t1_rows):
    if r_i < len(t1.rows):
        for c_i, val in enumerate(r_data):
            if c_i < len(t1.rows[r_i].cells):
                t1.rows[r_i].cells[c_i].text = val

# 5. Section III: Methodology (P29, P32, P33, P35, P36, P38, P40, P42)
doc.paragraphs[29].text = (
    "Methodology transforms the validated dropout prediction pipeline to the governed framework through five phases (Fig. 1): data preparation, "
    "model benchmarking, explainable AI, fairness auditing, and institutional governance. Following Silva et al. [1], we analyze public secondary "
    "technical education records, incorporating cumulative first-year GPA, course failures, and attendance rate as early-warning indicators, "
    "audited for demographic fairness and governed by administrative policy."
)

doc.paragraphs[32].text = (
    "Data are extracted from the public Brazilian Federal Institutes database (2014–2020; N = 48,311 initial records with 30 attributes) [1]. "
    "Two-stage filtering was executed: (1) Modality Filter: We excluded 12,038 higher education records, retaining 36,273 secondary technical students "
    "across four course formats: Integrado, Concomitante, Subsequente, and PROEJA/Integrado EJA. (2) Terminal Status Filter: We excluded 21,189 active "
    "non-terminal students (e.g., Matriculado, Trancado), yielding exactly N = 15,084 finalized students matching Silva et al. [1]. Class 0 (Completed) "
    "comprises 11,703 students (77.6%), while Class 1 (Dropout/cancellation/transfer) comprises 3,381 students (22.4%), defining an uninformative "
    "majority-class baseline of 77.6%."
)

doc.paragraphs[33].text = (
    "A stratified 80/20 train/test split partitioned the 15,084 students into 12,067 training records and an untouched held-out test vault of 3,017 "
    "records (2,341 completers, 676 dropouts; exactly 22.4% prevalence). Within the test vault, 2,722 students represent active attending students "
    "with positive GPA (GPA > 0), while 295 students represent immediate administrative dropouts (GPA == 0). Numeric continuous variables were winsorized "
    "using 1.5·IQR bounds on the training split without dropping records. Categoricals were one-hot encoded, and numeric features were left unnormalized "
    "matching the base paper."
)

doc.paragraphs[35].text = (
    "The full factorial design (4 × 3 × 4 = 48 experiments) was trained strictly on the 12,067 training records. Balancing methods included: "
    "Unbalanced, Random UnderSampling, SMOTE [16], and SMOTEENN [17]. Feature selection evaluated ANOVA F-filter, Backward Selection, and Tree Feature "
    "Importance. Models evaluated included Random Forest [18], Decision Tree, Logistic Regression, and SVM. Hyperparameter tuning was conducted via "
    "GridSearchCV with 5-fold cross-validation on training folds only to rule out test-set data leakage."
)

doc.paragraphs[36].text = (
    "In educational screening, false negatives incur severe educational harm, whereas false positives consume advisory capacity. Therefore, model "
    "selection was governed by a multi-objective utility rule: Maximize Recall subject to Precision >= 60% (preventing counselor false alarm fatigue). "
    "Primary evaluation metrics on the held-out 3,017 test vault include Recall, Precision, Specificity, Accuracy, F1-Score, ROC-AUC, Brier score, "
    "and counselor alert workload (flags per 100 students)."
)

doc.paragraphs[38].text = (
    "Global interpretability was computed using TreeSHAP [19] on the probability scale for Class 1 (Dropout) across 800 representative test students "
    "(441 female, 359 male) using training-set marginal expectations as background reference. Local explanations were generated using SHAP waterfall "
    "plots and LIME [13] (g(z') = w_0 + Sigma w_j z'_j with exponential distance kernel). Attribution shares across all 15 selected features were "
    "normalized mathematically against the total absolute SHAP sum. Local explanation stability was quantitatively evaluated by measuring pairwise "
    "top-3 Jaccard rank overlap between SHAP and LIME across 100 stratified test archetypes."
)

doc.paragraphs[40].text = (
    "Fairness was evaluated on the 3,017 test students across five protected axes: Gender (Male vs. Female), Race (White vs. Non-White), Income "
    "(Above vs. At/Below Median > R$ 930), Age (Traditional <= 20 vs. Adult >= 21), and Digital Access (Home Laptop Owned >= 1 vs. 0). Using AIF360 "
    "[14], we computed Disparate Impact (DI = SR_unpriv / SR_priv), Statistical Parity Difference (SPD = SR_unpriv - SR_priv), and Equal Opportunity "
    "Difference (EOD = TPR_unpriv - TPR_priv) [21]. The EEOC Four-Fifths rule (0.80 <= DI <= 1.25) [20] was utilized as an indicative screening heuristic. "
    "Subgroup confusion matrices and Wilson 95% score confidence intervals were computed. Bias mitigation was evaluated via AIF360 sample Reweighing on the training split."
)

doc.paragraphs[42].text = (
    "The framework establishes a proposed institutional governance policy charter comprising five operational pillars [2], [9]: (1) Strictly Advisory "
    "Role: Automated administrative dismissal or tracking is prohibited; model scores serve solely as supportive counseling flags. (2) Mandatory "
    "Explanation Coupling: Every risk flag delivered to staff must include a SHAP/LIME explanation card isolating actionable academic levers (tutoring, "
    "attendance) from protected immutable traits. (3) Bi-Annual Recalibration: Routine model auditing occurs every academic semester, with emergency "
    "drift reviews triggered if demographic selection rates shift by >10%. (4) Independent Student Appeal: Flagged students possess the institutional "
    "right to inspect explanation cards and submit written appeals within 14 days. (5) Human Counselor Final Authority: Certified human educators "
    "maintain sole intervention authority. Role-Based Access Control (RBAC) aligns with Brazil's LGPD [22], with audit logs recording all queries. "
    "Operational risk bands partition scores: Tier 1 Safe (P < 0.40, routine monitoring), Tier 2 Watchlist (0.40 <= P <= 0.70, counselor review), "
    "and Tier 3 Urgent (P > 0.70, multidisciplinary intervention)."
)

# 6. Section IV: Results and Discussion (P46, P47, P50, P54, P55, P57, P58, P59, P62, P63, P65, P70, P71, P72, P73, P75, P76)
doc.paragraphs[46].text = (
    "The 80/20 stratified split yielded 12,067 training students and 3,017 held-out test students (2,722 active with GPA > 0; 295 administrative exits "
    "with GPA == 0). Winsorization preserved all 15,084 records, exactly matching Silva et al. [1]."
)

doc.paragraphs[47].text = (
    "Baseline attrition varies across modalities (Fig. 2): Integrado (10,076 students) exhibits the lowest dropout rate (16.3%), compared to "
    "Concomitante (32.7%), Subsequente (34.6%), and PROEJA/Integrado EJA (39.5%). This pattern reflects structural delivery: adult working learners "
    "face severe employment and economic time constraints."
)

doc.paragraphs[50].text = (
    "Three empirical patterns characterize the cohort: (1) An attendance cliff (Fig. 3), wherein dropout risk escalates non-linearly from 8.4% for "
    "attendance >= 90%, to 18.2% (75%–89%), 48.7% (60%–74%), and 62.4% (< 60%), nearly three times the institutional baseline (22.4%); (2) An academic "
    "cliff, wherein graduates average a GPA of 7.2/10 compared to 5.0 for dropouts, with course failures concentrating heavily among dropouts (mean 3.8 "
    "failures vs. 0.4 for graduates); and (3) A digital divide, wherein students without home laptop computers exhibit a 28.4% dropout rate compared to "
    "18.1% for laptop owners."
)

doc.paragraphs[54].text = (
    "Out of 48 factorial experiments, Random Forest with UnderSampling and Tree Feature Importance was selected as champion: 84.8% test recall (95% CI: "
    "[82.0%, 87.4%]), 83.6% precision [81.0%, 86.4%], 92.9% accuracy [91.9%, 93.8%], F1-score 0.8420, and ROC-AUC 0.9506 on the 3,017 unseen test students. "
    "Ten-fold cross-validation recall on the training set reached 87.8% +/- 1.4%, confirming that test performance is not a split artifact. On the same 3,017 "
    "test students, the majority-class baseline achieves 77.6% accuracy but 0.0% recall, while an attendance heuristic rule (< 75% attendance) achieves "
    "95.7% precision but only 6.7% recall (79.0% accuracy, F1 = 0.1245, AUC = 0.5903), demonstrating that simple heuristics miss over 93% of at-risk students."
)

doc.paragraphs[55].text = (
    "Analysis of alternative models demonstrates why recall-only maximization is operationally dangerous. Support Vector Machines with SMOTEENN and ANOVA "
    "achieved the highest nominal recall (91.4%); however, precision collapsed to 23.1%, accuracy fell to 30.1%, and ROC-AUC was only 0.5910 (near-random "
    "discriminability). The SVM flagged 2,668 out of 3,017 test students (88.4 alerts per 100 students), flooding counselors with 2,050 false alarms and "
    "violating our precision constraint (>= 60%). Decision Tree with UnderSampling detected 84.6% of dropouts but with lower precision (64.0%, accuracy "
    "85.9%, AUC 0.8540). Logistic Regression reached 78.7% recall and 71.8% precision (accuracy 88.3%, AUC 0.8990). On the held-out test vault (N = 3,017; "
    "676 actual dropouts, 2,341 completers), the Random Forest champion generated exactly: TP = 573, FP = 112, TN = 2,229, and FN = 103 (sensitivity 84.76%, "
    "precision 83.65%, specificity 95.22%, workload 22.7 alerts/100 students). On active students (GPA > 0, N = 2,722), the model maintained 80.8% recall "
    "(396/490) and 82.5% precision (accuracy 93.5%). Raw Brier score was 0.0526 (69.7% skill score vs. 0.1738 prevalence dummy), with empirical dropout rates "
    "tracking risk bands: Tier 1 Safe (P < 0.40, empirical 4.2%), Tier 2 Watchlist (0.40 <= P <= 0.70, empirical 20.4%), and Tier 3 Urgent (P > 0.70, empirical 91.2%)."
)

doc.paragraphs[57].text = (
    "Global TreeSHAP attributions across 800 test students indicate that academic performance variables dominate predictions. Mean absolute SHAP attribution "
    "is highest for first-year GPA (0.2717), followed by course failures (0.0596), enrollment year (0.0415), attendance rate (0.0305), and modality (0.0263). "
    "Normalizing against the 15-feature denominator reveals that GPA comprises 52.8% of total attribution, while GPA, failures, and attendance collectively "
    "account for 71.3% of model explanatory weight. Demographic and socioeconomic attributes contribute minimally to direct splits: student age (0.0174; 3.4%), "
    "family income (0.0127; 2.5%), employment (0.0084), parental education (0.0073, 0.0066), home laptop ownership (0.0046; 0.9%), and gender (0.0040, 0.0032; < 1.0%). "
    "While Silva et al. [1] found income and attendance dominant in the absence of academic metrics, incorporating semester academic tracking concentrates explanatory power on actionable educational performance."
)

doc.paragraphs[58].text = (
    "From the beeswarm plot (Fig. 4), high GPA (red points) strongly reduces predicted risk (SHAP values down to -0.35), whereas low GPA (blue points) elevates "
    "risk by up to +0.50. Accumulated course failures and attendance below 75% accelerate risk elevation."
)
doc.paragraphs[59].text = ""

doc.paragraphs[62].text = (
    "Local attributions illuminate individual risk drivers. High-risk students #0 and #43 (predicted risk 94.6% and 92.1%) present low GPAs (1.89, 0.63), "
    "numerous failures (8, 7), and irregular attendance, with GPA contributing +0.2831 and +0.2672. Attendance tracking alone fails on student #185, who maintains "
    "100% attendance and zero failures but exhibits an 89.2% dropout risk driven entirely by failing coursework (GPA contribution +0.5039). Low-risk archetypes "
    "#1 and #102 (predicted risk 3.4% and 2.8%) are anchored by strong academic standing."
)

doc.paragraphs[63].text = (
    "Borderline student #37 (predicted risk 50.1%, margin 0.1%) represents a false positive who graduated. While GPA was satisfactory (7.12), irregular "
    "attendance (+0.0746) nudged the score over threshold, exemplifying why human counselor review is mandatory for borderline scores (0.40 <= P <= 0.70). "
    "Comparing local explanations, global TreeSHAP captures population-level tree structure, whereas LIME computes localized linear approximations. Across "
    "100 stratified test students, mean top-3 Jaccard feature overlap between SHAP and LIME reached 0.724 +/- 0.081, demonstrating high local-global fidelity while "
    "highlighting localized feature interactions for counselors."
)

doc.paragraphs[65].text = (
    "Fairness audits across the 3,017 test students reveal complex demographic patterns (Fig. 5). Disparate impact is compliant under the Four-Fifths rule for "
    "race (DI = 1.180; selection rate 24.2% for Non-White vs. 20.5% for White; TPR 85.3% vs. 83.1%). In contrast, gender exhibits substantial disparity (DI = 0.7066, "
    "SPD = -0.0789; selection rate 19.00% for females [304/1,600] vs. 26.89% for males [381/1,417]). Subgroup confusion matrices indicate that females present lower "
    "baseline dropout prevalence (19.44% [311/1,600] vs. 25.76% [365/1,417] for males). While female precision remains high (83.55% vs. 83.73%), female recall is "
    "5.73 pp lower (81.67% [254/311] vs. 87.40% [319/365]; EOD = -0.0573), revealing that at-risk female dropouts are under-detected relative to males under default 0.50 thresholding."
)

doc.paragraphs[70].text = (
    "Conversely, Disparate Impact exceeds 1.25 for family income (DI = 1.411; selection rate 26.6% low-income vs. 18.8% high-income), age cohort (DI = 1.590; 28.1% "
    "adult vs. 17.7% traditional), and digital access (DI = 1.403; 25.4% without laptop vs. 18.1% with laptop). However, Equal Opportunity differences for these groups "
    "remain positive (EOD = +0.039 to +0.092), meaning dropouts in marginalized categories are detected with higher sensitivity (e.g., adult dropout recall 87.9% vs. "
    "82.2% for teens). Rather than algorithmic discrimination, elevated selection rates reflect real-world socioeconomic headwinds (base dropout rate 25.7% for low-income "
    "vs. 19.0% for high-income; 34.6% for adults vs. 16.3% for teens). Imposing statistical parity quotas would artificially suppress support flags for vulnerable students "
    "who legitimately require bursaries and tutoring."
)

doc.paragraphs[71].text = (
    "To address the female sensitivity gap (EOD = -0.0573), we evaluated AIF360 sample Reweighing on the training set. Post-mitigation evaluation on the 3,017 test students "
    "showed that precision increased to 94.54% and accuracy reached 94.37%; however, overall recall dropped by 5.32 pp to 79.44% (female recall 78.1%, male recall 80.5%), "
    "with gender DI shifting to 0.648. This demonstrates an explicit policy trade-off: in-processing mitigation improved purity but sacrificed catch rate. Alternatively, "
    "post-hoc threshold adjustment (calibrating female screening to tau = 0.44) restored female recall to 87.2% without degrading overall performance, establishing post-hoc "
    "thresholding as the superior clinical remedy."
)

doc.paragraphs[72].text = (
    "A 3-fold cross-validation proxy analysis predicting protected attributes from non-protected features confirmed that Gender (AUC = 0.6172), Income (0.6790), and "
    "Digital Access (0.7147) cannot be deterministically reconstructed. However, Student Age exhibited strong proxy predictability (AUC = 0.8918), driven by course "
    "modality (evening/PROEJA enrollment). This proves that low direct SHAP importance does not guarantee absence of proxy influence, as structural curriculum design "
    "inadvertently encodes student demographic age."
)

# Delete duplicate paragraph P73
doc.paragraphs[73].text = ""

doc.paragraphs[75].text = (
    "The operational governance workflow maps calibrated risk scores into actionable institutional tiers: Tier 1 Safe (P < 0.40, routine academic advising), Tier 2 "
    "Watchlist (0.40 <= P <= 0.70, individual counselor conference with SHAP explanation card), and Tier 3 Urgent (P > 0.70, immediate multidisciplinary case review "
    "incorporating social bursary evaluation). High-risk students #0, #43, and #185 (scores 89.2%–94.6%) receive proactive tutoring and emergency meal support, while borderline "
    "student #37 receives attendance counseling, preventing false alarm stigmatization."
)

doc.paragraphs[76].text = (
    "The five governance pillars address the ethical risks identified in our fairness audit: mandatory human review prevents algorithmic bias from translating into automated "
    "penalties; explanation cards isolate actionable attendance deficits from immutable demographic traits; and independent 14-day appeals safeguard student procedural rights "
    "under LGPD. Bi-annual audits scheduled before each academic term ensure continuous monitoring against demographic drift and proxy encoding."
)

# 7. Section V: Conclusion, Limitations & Future Work (P78, P79, P80)
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
    "Limitations are structured into six dimensions: (1) Data provenance from Brazilian Federal Institutes (IFMA); (2) First-year temporal lag precluding pre-enrollment screening; "
    "(3) Composite label construct; (4) Structural proxy encoding of student age via course modality (AUC = 0.8918); (5) Mitigation trade-offs; and (6) Untested live counselor adoption. "
    "Future work will deploy a 1-semester counselor-in-the-loop pilot measuring intervention efficacy and student appeal outcomes."
)

# 8. Clean References (P90 and P91) - ALL 22 PRESERVED
doc.paragraphs[90].text = (
    "Y. Zhang and S. Yang, “The application of genetic algorithm and fuzzy evaluation method in teachers’ performance appraisal,” "
    "in Proc. Int. Conf. Artif. Intell. Things Crowdsensing (AIoTCs), 2022, pp. 245–250, doi: 10.1145/3579895.3579938."
)

doc.paragraphs[91].text = (
    "L. Zhou, “Performance evaluation of basic education informatization based on improved BP algorithm,” "
    "in Proc. Int. Conf. Artif. Intell. Things Crowdsensing (AIoTCs), 2022, pp. 312–317, doi: 10.1145/3579895.3579950."
)

doc.save("paper_review/research_paper_final_draft.docx")
print("Saved precision updated paper_review/research_paper_final_draft.docx")

