import docx
import shutil
import zipfile
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("TUNING DEV2 RESEARCH PAPER TO STRICTLY 6 PAGES (IEEE TWO-COLUMN)")
print("=" * 80)

# Start fresh from the original backup to ensure section breaks, columns, and margins are 100% original
src_backup = "paper_review/research_paper_final_draft_ORIGINAL_BACKUP.docx"
target_path = "paper_review/research_paper_final_draft.docx"
copy_path = "paper_review/research_paper_final_with_updates.docx"

shutil.copyfile(src_backup, target_path)
doc = docx.Document(target_path)

# Title
title_text = "An Explainable and Fairness-Audited AI Governance Framework for Student Dropout Prediction"

# Page 1: Abstract (~240 words)
abstract_text = (
    "Abstract—Student dropout undermines educational attainment and institutional sustainability in public vocational education. "
    "While predictive machine learning offers opportunities for timely support, deploying opaque models risks inequitable intervention "
    "and algorithmic harm. We present an end-to-end framework integrating machine learning, dual macro/micro explainability, "
    "algorithmic fairness auditing, and operational governance for student dropout risk classification. "
    "Using 15,084 secondary technical student records from the Instituto Federal do Norte de Minas Gerais (IFNMG) partitioned "
    "via a 70/30 stratified split (10,558 training, 4,526 test), we evaluated 48 pipeline configurations without retrospective GPA (ira), "
    "strictly eliminating target leakage. A Random Forest model with Random Under-Sampling and Tree Feature Importance (k=19) "
    "was selected as champion, achieving Recall of 73.18% (95% CI: [70.48%, 76.00%]), Precision of 75.64% (95% CI: [72.83%, 78.19%]), "
    "Accuracy of 88.71%, ROC-AUC of 0.8968 (95% CI: [0.8836, 0.9098]), and Brier Score of 0.1080 (baseline 0.1738). "
    "TreeSHAP feature attribution identified course failures (reprovacoes, 32.37%), attendance percentage (percentual_frequencia, 19.26%), "
    "and cohort year (anoingresso, 10.78%) as primary drivers, accounting for 62.41% of total attribution. "
    "Local LIME surrogates demonstrated moderate agreement with SHAP across student archetypes (mean top-3 Jaccard overlap 66.7%). "
    "Algorithmic fairness audits across five protected dimensions under the Four-Fifths screening heuristic revealed gender disparity "
    "(Disparate Impact 0.7383, female recall 70.87% vs. male 75.09%, EOD -0.0422, p=0.1354) and statistically significant socioeconomic "
    "gaps on Income (p=0.00043) and Computer Ownership (p=0.00089) under Holm-Bonferroni correction. Pre-processing AIF360 Reweighing "
    "tightened Equal Opportunity but induced an acute 12.82 percentage point drop in recall (73.18% to 60.36%). "
    "Consequently, we propose a non-punitive operational governance charter incorporating role-based access control, semi-annual audits, "
    "heuristic risk bands, and Brazilian LGPD Art. 20 contestability rights (proposed design, not field-tested in live operations)."
)

# Page 1: Introduction P19 (~45 words)
p19_text = (
    "Student attrition undermines educational equity and institutional viability in public secondary technical education. "
    "In Brazilian Federal Institutes (IFNMG), non-completion rates reach 22.4%, compounding socioeconomic stratification. "
    "While UN Sustainable Development Goals (SDG 4 and SDG 10) motivate this work, SDG alignment serves strictly as a conceptual "
    "institutional objective rather than an empirical progress metric."
)

# Page 1: Introduction P20 (~78 words)
p20_text = (
    "Standard accuracy is insufficient when algorithmic inferences trigger academic triage: false negatives leave vulnerable students "
    "unassisted, while false positives waste scarce counseling resources. Crucially, in administrative datasets, cumulative GPA (ira) "
    "is computed retrospectively across complete tenures, introducing severe target leakage. Predicting dropout requires restricting "
    "predictors strictly to verifiable administrative and academic friction features prior to terminal departure. Furthermore, predictive "
    "models risk encoding demographic inequities, demanding rigorous multi-dimensional fairness audits [1], [2]."
)

# Page 1: Introduction P21 (~48 words)
p21_text = (
    "Existing literature addresses prediction, explanation, fairness, and governance in isolation. We define the specific research gap "
    "as the operational integration and empirical evaluation of model explanations, group fairness audits, and procedural human oversight "
    "within a dropout early warning workflow, explicitly disclaiming the invention of a novel classifier architecture."
)

# Page 1: Introduction P22 (~65 words)
p22_text = (
    "To address this gap, we formulate four explicit research questions: "
    "(RQ1) Predictive Utility: Can a leak-free pipeline reliably classify dropout risk without retrospective GPA? "
    "(RQ2) Explanation Consistency: Do TreeSHAP and LIME identify consistent risk indicators across archetypes? "
    "(RQ3) Group Fairness: Does the model maintain demographic parity and equal opportunity across protected groups? "
    "(RQ4) Governance Feasibility: How can explanations and appeals be formalized into an operational charter?"
)

# Page 1: Introduction P23 (~62 words)
p23_text = (
    "The primary contribution is operational integration: (1) a 48-experiment benchmark on 15,084 students without GPA, selecting a Random Forest "
    "champion (Recall 73.18%, ROC-AUC 0.8968); (2) dual macro/micro explainability establishing course failures and attendance as top predictors (62.41% top-3 share); "
    "(3) multi-dimensional fairness audits with Holm-Bonferroni correction; and (4) a proposed operational governance framework with LGPD-aligned appeals (not field-tested)."
)

# Page 1: Roadmap P24 (~25 words)
p24_text = (
    "Section II reviews the literature, Section III details the methodology, Section IV presents experimental and audit results, "
    "and Section V concludes with limitations and future work."
)

# Page 2: Literature Review P26 (~145 words)
p26_text = (
    "Student outcome research has transitioned from feasibility demonstration to algorithmic governance. Silva et al. [1] applied Random Forests "
    "and Decision Trees with LIME and SHAP on 15,084 IFNMG records, establishing attendance and course failures as primary indicators; however, their "
    "pipeline lacked algorithmic fairness audits and institutional governance. Zanellati et al. [2] balanced explainability and accuracy across 2,000+ "
    "degree programs but omitted group equity safeguards. In admission modeling, Priyadarshini and Gago-Masague [3] utilized adversarial debiasing, "
    "highlighting accuracy-fairness tensions. Mengash [4] and Alhazmi and Sheneamer [5] demonstrated early prediction but treated models as black boxes. "
    "Pelima et al. [6] surveyed 45 ML graduation studies, identifying systematic under-reporting of institutional governance. Ma et al. [7] and "
    "Jiang and Wang [8] advanced cognitive diagnostic models, while Zhang and Yang [9], Zhou [10], and Lu et al. [11] explored fuzzy evaluation, "
    "neural assessment, and decision analysis (Table I). Crucially, Kleinberg et al.'s impossibility theorem [15] proves that demographic parity, "
    "equalized odds, and calibration cannot simultaneously hold when group base rates differ (e.g., lower income dropout 25.8% vs. higher income 19.0%). "
    "In educational triage, we prioritize Equal Opportunity (recall parity across groups) [21] because false negatives incur severe educational harm, "
    "while treating Disparate Impact [20] as an administrative screening heuristic."
)

# Page 2: Table I updates
table_data = [
    ["Study & Citation", "Domain & Sample (N)", "Key Findings & Method", "Gaps Addressed"],
    ["Silva et al. (2025) [1]", "IFNMG Brazil (N=15,084)", "85% recall; RF with SHAP & LIME", "No fairness audit or policy charter"],
    ["Zanellati et al. (2024) [2]", "Italy Higher Ed (N=7,000)", "81% recall; Transformer, TreeSHAP", "Gender checked; no appeal board"],
    ["Priyadarshini et al. (2024) [3]", "US Admissions (N=12,000)", "Adversarial debiasing in DL", "Training only; no post-hoc XAI"],
    ["Mengash (2020) [4]", "Saudi University (N=2,000)", "Pre-admission prediction; ANN", "Sensitive data; no equity audit"],
    ["Alhazmi & Sheneamer (2023) [5]", "Saudi University (N=3,500)", "Early at-risk prediction; Ensemble", "No explanations or fairness check"],
    ["Pelima et al. (2024) [6]", "Systematic Review (84 papers)", "Graduation review; RF, SVM <=90% acc", "XAI and fairness rarely integrated"],
    ["Ma et al. (2023) [7]", "Personalized E-Learning", "Exam prediction; Neutrosophic", "No demographic audit or oversight"],
    ["Jiang & Wang (2020) [8]", "Online Learning Platforms", "Cognitive diagnosis; neural weights", "Interpretable; no fairness metric"],
    ["Zhang & Yang (2022) [9]", "Teacher Evaluation (China)", "Performance appraisal; Fuzzy GA", "Fuzzy logic; no appeal rights"],
    ["Zhou (2022) [10]", "Basic Education (China)", "Informatization; BP Neural Net", "Black box; no transparency rules"],
    ["Lu et al. (2024) [11]", "Physical Education (China)", "Quality appraisal; ExpTODIM", "Expert weights; no demographic audit"],
    ["This Work", "IFNMG Brazil (N=15,084)", "RF (Recall 73.2%, AUC 0.90) | TreeSHAP/LIME", "5-Axis Fairness, Reweighing, LGPD Governance"]
]

# Page 2: Methodology Intro P29 (~55 words)
p29_text = (
    "The methodology operationalizes student dropout screening into a five-phase leak-free workflow (Fig. 1): Phase 1 extracts the cohort and "
    "preprocesses data without retrospective GPA; Phase 2 executes a 48-configuration factorial benchmark under nested cross-validation and constrained "
    "utility selection; Phase 3 implements TreeSHAP and LIME interpretability; Phase 4 executes demographic fairness audits with Holm-Bonferroni correction; "
    "and Phase 5 articulates a proposed governance charter (not field-tested)."
)

# Page 2: Data Preparation P32 (~95 words)
p32_text = (
    "Data derive from administrative enrollment records of the Instituto Federal do Norte de Minas Gerais (IFNMG) (dataset_evasao_MDE.xlsx) "
    "[AUTHOR TO CONFIRM: Dataset URL & License]; [AUTHOR TO CONFIRM: Cohort date range]. The raw database contains 48,311 student records across all levels. "
    "Filtering strictly for secondary technical modalities (Integrado: 10,076; Concomitante: 1,777; Subsequente: 2,746; Integrado EJA: 485) yields 15,084 "
    "terminal student records [AUTHOR TO CONFIRM: Exclusion counts by reason]. Terminal outcomes were mapped to a binary target: Completed (Class 0, "
    "N=11,703, 77.59%) versus Dropout / Non-completion (Class 1, N=3,381, 22.41%), combining voluntary dropout (1,760), cancellation (446), compulsory "
    "dismissal (346), jubilated status (38), and external transfers (791)."
)

# Page 2/3: Split & Leakage P33 (~75 words)
p33_text = (
    "A stratified 70/30 split partitioned the 15,084 records into 10,558 training and 4,526 held-out test students (random_state=42). "
    "Crucially, cumulative GPA (ira) was completely excluded to eliminate retrospective target leakage. After dropping identifiers (alunoid) "
    "and variables with >20% missingness (dataconclusao, forma_acesso_seletivo, razao_ausencia_educacional, pontuacao_seletivo), "
    "19 baseline administrative and academic friction features remained. Minor digital access missingness was median-imputed. "
    "Continuous features underwent 1.5x IQR Winsorization fitted strictly on training folds, and one-hot encoding expanded the design matrix to 34 columns."
)

# Page 3: Model Benchmarking P35 (~75 words)
p35_text = (
    "The 48-condition factorial grid crossed 4 balancing strategies (Unbalanced, RandomUnderSampler, SMOTE [16], SMOTEENN [17]), 3 feature selection methods "
    "(ANOVA F-test, Backward Elimination / RFE, Tree Feature Importance, selecting k=19 features), and 4 classifiers (Random Forest [18], Decision Tree, "
    "Logistic Regression, Linear Support Vector Machine). To guarantee zero data leakage, resampling, scaling, and feature selection were executed "
    "strictly inside 10-fold cross-validation training folds using imblearn.pipeline.Pipeline, keeping validation folds at natural 22.4% prevalence. "
    "The champion model was selected via a constrained utility rule: highest Recall subject to Precision >= 60% and ROC-AUC >= 0.90 on training CV folds."
)

# Page 3: Metrics P36 (~38 words)
p36_text = (
    "Evaluation metrics include Recall = TP/(TP+FN), Precision = TP/(TP+FP), Accuracy = (TP+TN)/N, Specificity = TN/(TN+FP), and ROC-AUC. "
    "We computed 95% bootstrap confidence intervals (1,000 iterations) to quantify sampling uncertainty on the 4,526 held-out test cases."
)

# Page 3: Explainable AI P38 (~70 words)
p38_text = (
    "Global interpretability applied TreeSHAP [12], [19] on the probability scale over 800 background instances drawn via stratified random sampling from the "
    "training set, explaining Class 1 (Dropout risk) on the held-out test cohort (N=4,526). Mean absolute SHAP values quantified institutional feature "
    "attribution shares. Local micro-explanations utilized LIME [13] fitted on training data to generate localized decision boundaries for High-Risk, Borderline, "
    "and Low-Risk student archetypes, measuring explanation stability via top-3 Jaccard similarity."
)

# Page 3: Fairness Audit P40 (~85 words)
p40_text = (
    "Fairness was audited on the 4,526 held-out test students across five protected dimensions: Gender (Male vs. Female), Race (Branca vs. Parda, "
    "Branca vs. Preta), Household Income (> Median vs. <= Median R$ 930), Age (<= 20 vs. > 20 years), and Home Computer Ownership (>= 1 vs. 0). "
    "Metrics included Disparate Impact (evaluated under the Four-Fifths screening heuristic [20], 0.80 <= DI <= 1.25), Statistical Parity Difference (SPD), "
    "Equal Opportunity Difference (EOD = TPR_u - TPR_p) [21], and False Positive Rate gaps. Holm-Bonferroni step-down correction controlled Family-Wise "
    "Error Rate across EOD p-values. Pre-processing AIF360 Reweighing [14] was evaluated as a debiasing intervention."
)

# Page 3: Institutional Governance P42 (~65 words)
p42_text = (
    "Section IV-E details the proposed institutional governance policy charter (not field-tested). The charter codifies role-based access control (RBAC), "
    "semi-annual review cadences, heuristic risk bands (<0.20 minimal, 0.20-0.40 low concern, 0.40-0.60 watchlist, 0.60-0.80 high priority, >=0.80 emergency), "
    "student appeal rights under Brazilian LGPD Art. 20 [22], and unilateral counselor override authority."
)

# Page 3: Results Intro P44 (~22 words)
p44_text = (
    "Figures refer to the 4,526-student held-out test set (70/30 split) unless noted; baseline prevalence is 22.40% (1,014 dropouts, 3,512 completed)."
)

# Page 3: Phase 1 Results P46 (~35 words)
p46_text = (
    "The 70/30 stratified split yielded 10,558 training students (Class 0: 8,191, Class 1: 2,367) and 4,526 test students (Class 0: 3,512, Class 1: 1,014). "
    "Baseline dropout prevalence is 22.41% in training and 22.40% in testing, confirming rigorous stratification."
)

# Page 3: Phase 1 Modality P47 (~40 words)
p47_text = (
    "Baseline attrition varies substantially across educational modalities (Fig. 2): Integrado EJA exhibits highest non-completion (42.8%), "
    "followed by Subsequente (30.1%), Concomitante (24.7%), and Integrado (18.6%). These discrepancies reflect structural adult-learner commitments "
    "rather than intrinsic institutional deficits."
)

# Page 4: Phase 1 Patterns P50 (~55 words)
p50_text = (
    "Two dominant behavioral patterns characterize the cohort: (1) an attendance cliff (Fig. 3), where dropout rates surge below the 75% legal minimum; "
    "and (2) failure accumulation, where dropouts average 5.99 failed courses (median 3, max 69) versus 0.77 for completers (75% have <= 1 failure)."
)

# Page 4: Phase 2 Benchmarking Results P54 (~85 words)
p54_text = (
    "The Random Forest champion (RandomUnderSampler, Tree Feature Importance k=19, n_estimators=100, max_depth=10, min_samples_leaf=5, random_state=42) "
    "achieved on the 4,526 test students: Recall 73.18% (95% CI: [70.48%, 76.00%]), Precision 75.64% (95% CI: [72.83%, 78.19%]), "
    "F1-Score 0.7439, Accuracy 88.71%, and ROC-AUC 0.8968 (95% CI: [0.8836, 0.9098]). The confusion matrix confirms TP=742, FP=239, TN=3,273, FN=272. "
    "A majority-class baseline yields 77.60% accuracy but 0.00% recall. An attendance-only baseline (threshold <= 91%) captures only 32.15% of dropouts "
    "(Precision 63.92%, continuous ROC-AUC 0.5945)."
)

# Page 4: Alternative Models P55 (~78 words)
p55_text = (
    "Alternative candidate models failed operational requirements. While Decision Tree under the same pipeline achieved higher test recall (75.05%), "
    "its precision was lower (67.05%) and its 10-fold CV ROC-AUC (0.8875) failed the >= 0.90 threshold. Linear SVM with SMOTEENN achieved 60.55% recall "
    "but collapsed in precision (45.08%), generating unacceptable false alarm burdens (54.9% false alarms). The Random Forest model uniquely satisfied "
    "our constrained utility rule on training cross-validation (CV Recall 74.95%, CV Precision 76.94%, CV ROC-AUC 0.9144)."
)

# Page 4: Phase 3 Explainability P57 (~98 words)
p57_text = (
    "TreeSHAP attributions across the 4,526 test students (total mean |SHAP| denominator = 0.407016) demonstrate that academic friction dominates prediction. "
    "Course failures (reprovacoes) contributes 32.37% (mean |SHAP| = 0.1317), attendance percentage (percentual_frequencia) contributes 19.26% "
    "(mean |SHAP| = 0.0784), and cohort year (anoingresso) contributes 10.78% (mean |SHAP| = 0.0439). Together, these top three features account for "
    "62.41% of total model attribution (recomputed numerator 0.254029 / denominator 0.407016). Secondary factors include modality (6.95%), "
    "age (6.31%), family income (5.78%), course (3.61%), campus (2.84%), employment (2.48%), and gender (combined M+F share 3.66%)."
)

# Page 4: Beeswarm plot text P58 (~25 words)
p58_text = (
    "The global beeswarm plot (Fig. 4) illustrates directional mechanisms: high course failures (red) strongly shift log-odds toward dropout, "
    "while high attendance (>90%) provides robust protective attribution against attrition."
)

# Page 4: Local Explanations P62 (~55 words)
p62_text = (
    "Local explanations provide individualized recourse profiles for educational counselors. Across three representative archetypes, TreeSHAP and LIME "
    "exhibit moderate feature concordance: High-Risk student #815 (P(Dropout)=94.8%, Jaccard overlap 0.50), Borderline student #4078 (P(Dropout)=48.0%, "
    "Jaccard overlap 0.50), and Low-Risk student #4458 (P(Dropout)=10.7%, Jaccard overlap 1.00). Mean top-3 Jaccard overlap is 66.67% (moderate agreement)."
)

# Page 4: Archetype Recourse P63 (~52 words)
p63_text = (
    "For student #815 (High-Risk), TreeSHAP attributes acute risk to 12 course failures and 72.5% attendance, matched by LIME indicating reprovacoes > 4. "
    "For borderline student #4078, TreeSHAP balances risk from 2 failures against the protective buffer of 88.4% attendance. For low-risk student #4458, "
    "both explainers attribute robust retention to 0 failures and 96.2% attendance."
)

# Page 5: Fairness Audit Results P65 (~65 words)
p65_text = (
    "Algorithmic fairness audits across the 4,526 test students at threshold tau=0.50 evaluate five protected dimensions (Fig. 5). "
    "Under the Four-Fifths screening heuristic (0.80 <= DI <= 1.25), Disparate Impact flagged Gender (DI 0.7383), Race (Branca vs. Parda DI 1.2958; "
    "Branca vs. Preta DI 1.2694), Income (DI 1.5098), Age (DI 1.2864), and Computer Ownership (DI 1.5106). Elevated selection rates "
    "for unprivileged groups mirror higher historical base rates, while False Positive Rate gaps remain modest (+2.76% for low income, +2.75% for no computer)."
)

# Page 5: Gender Disparity P70 (~65 words)
p70_text = (
    "Under Equal Opportunity parity (EOD = TPR_u - TPR_p), Gender exhibits near-parity (EOD -0.0422, 95% CI: [-0.097, 0.013], p=0.1354). "
    "Applying Holm-Bonferroni correction across the 6 demographic EOD p-values reveals that Race (Branca vs. Parda EOD +0.1014, raw p=0.0144) "
    "does not survive the adjusted threshold (alpha/4 = 0.0125). Only Household Income (EOD +0.1007, p=0.00043) and Computer Ownership (EOD +0.1109, "
    "p=0.00089) exhibit statistically significant sensitivity differences."
)

# Page 5: Mitigation Trade-off P71 (~55 words)
p71_text = (
    "To mitigate demographic disparity, we evaluated AIF360 Reweighing pre-processing on training sample weights. While Reweighing slightly tightened "
    "gender EOD (-0.0422 to -0.0304) and increased precision (75.64% to 93.72%), it caused a catastrophic 12.82 percentage point drop in recall "
    "(73.18% to 60.36%). In educational dropout prevention, algorithmic debiasing alone is insufficient, mandating operational human-in-the-loop governance."
)

# Page 5: Resource Allocation P72 (~48 words)
p72_text = (
    "Figure 5(d) depicts institutional resource allocation under varying operational thresholds: lowering classification thresholds captures more dropouts "
    "but increases false alerts and counselor caseload. The proposed 0.50 threshold flags 981 students (21.68% selection rate, or 21.7 alerts per 100 students) "
    "and maintains a 3.10:1 true-to-false alert ratio (742 TP to 239 FP)."
)

# Page 5: Calibration & Risk Bands P75 (~72 words)
p75_text = (
    "Probability calibration was evaluated via Brier score (0.1080 vs. baseline 0.1738) and a 10-bin reliability diagram. Partitioning predictions into "
    "mutually exclusive heuristic risk bands reveals empirical alignment at extreme tiers: Emergency [0.80, 1.00] flags 567 students with 95.24% observed "
    "dropout, and High Priority [0.60, 0.80) flags 190 students with 63.68% observed dropout. However, probability inflation from UnderSampling occurs "
    "in the Watchlist band [0.40, 0.60) (observed dropout 26.94% vs. mean predicted 48.6%)."
)

# Page 5: Proposed Governance Charter P76 (~85 words)
p76_text = (
    "Proposed Governance Framework (Not Field-Tested): To govern operational triage responsibly, we specify an institutional AI Governance Charter "
    "grounded in five normative pillars: (1) Strictly Advisory, Non-Punitive Deployment, prohibiting automated sanctions; (2) Mandatory Explainability-Coupled "
    "Outreach, requiring counselors to inspect individualized SHAP/LIME feature attributions; (3) Scheduled Semi-Annual Fairness Auditing, enforcing DI and "
    "Holm-Bonferroni EOD reviews; (4) Institutional Contestability and Student Appeal Rights, aligned with Brazilian LGPD Art. 20 [22] (10-business-day timeline); "
    "and (5) Certified Human-in-the-Loop Override Authority, vesting counselors with unilateral dismissal power. For 5,000 students, the 0.50 threshold flags 1,084 "
    "students, requiring 6 counselors for a 4-week response SLA."
)

# Page 6: Conclusion Summary P78 (~68 words)
p78_text = (
    "This research presented an Explainable and Fairness-Audited AI Governance Framework for secondary technical student dropout risk classification. "
    "By strictly eliminating retrospective GPA target leakage, our Random Forest benchmark on 15,084 IFNMG students (70/30 split) demonstrated robust "
    "performance (73.18% recall, 75.64% precision, 0.8968 ROC-AUC, 0.1080 Brier score). Dual explainability proved that course failures (32.37%) and "
    "attendance (19.26%) are the primary actionable predictors, with moderate local explainer concordance (66.7% mean Jaccard overlap)."
)

# Page 6: Conclusion Findings P79 (~62 words)
p79_text = (
    "Algorithmic auditing revealed that while gender satisfies Equal Opportunity parity (EOD -0.0422, p=0.1354), significant sensitivity gaps persist "
    "across income and digital access under Holm-Bonferroni correction. Because pre-processing debiasing induced a severe 12.82 pp recall penalty, "
    "fairness must be governed institutionally. Our five-pillar charter and heuristic risk bands establish an operational blueprint for responsible, "
    "non-punitive educational AI deployment."
)

# Page 6: Limitations & Threats to Validity P80 (~95 words)
p80_text = (
    "Limitations and Threats to Validity: (1) Data Provenance & Selection: Retrospective cohort from a single Brazilian institution (IFNMG, "
    "[AUTHOR TO CONFIRM: Cohort date range]); excluding active ongoing students introduces right-censoring. (2) Label Construct: Grouping cancellations, "
    "transfers, and expulsions into a single binary dropout target conflates heterogeneous attrition pathways. (3) Cumulative Feature Measurement Window: "
    "Course failures and attendance accumulate across students' multi-year tenures; cross-sectional data limitations prevent restricting features strictly "
    "to the first academic year. (4) Subgroup Uncertainty: Modality imbalances inflate estimation variance for small cohorts. (5) External Validity: "
    "Findings from a single Brazilian technical network cannot establish transferability to other institutions (e.g., Indian universities). "
    "(6) Untested Governance: The five-pillar charter and procedural safeguards represent a proposed operational design that has not been field-tested in live operations."
)

# Paragraph mapping
p_map = {
    0: title_text,
    17: abstract_text,
    19: p19_text,
    20: p20_text,
    21: p21_text,
    22: p22_text,
    23: p23_text,
    24: p24_text,
    26: p26_text,
    29: p29_text,
    32: p32_text,
    33: p33_text,
    35: p35_text,
    36: p36_text,
    38: p38_text,
    40: p40_text,
    42: p42_text,
    44: p44_text,
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
    75: p75_text,
    76: p76_text,
    78: p78_text,
    79: p79_text,
    80: p80_text
}

print(f"Applying {len(p_map)} paragraph updates...")
for p_idx, text in p_map.items():
    if p_idx < len(doc.paragraphs):
        p = doc.paragraphs[p_idx]
        p.text = text
        for run in p.runs:
            run.font.name = "Times New Roman"

# Update Table 0
tbl = doc.tables[0]
# Ensure exactly 13 rows
while len(tbl.rows) < 13:
    tbl.add_row()
while len(tbl.rows) > 13:
    # remove extra rows if any
    tr = tbl.rows[-1]._tr
    tr.getparent().remove(tr)

for r_idx, row_vals in enumerate(table_data):
    for c_idx, val in enumerate(row_vals):
        tbl.rows[r_idx].cells[c_idx].text = val
        p = tbl.rows[r_idx].cells[c_idx].paragraphs[0]
        p.paragraph_format.space_before = 0
        p.paragraph_format.space_after = 0
        p.paragraph_format.line_spacing = 1.0
        for run in p.runs:
            run.font.name = "Times New Roman"
            run.font.size = docx.shared.Pt(7.5)

doc.save(target_path)
print(f"Saved text updates to {target_path}")

# Now replace the image files in the docx zip archive directly
print("Replacing embedded figures with dev2 generated figures...")
tmp_zip = "paper_review/tmp_update.zip"
with zipfile.ZipFile(target_path, 'r') as zin:
    with zipfile.ZipFile(tmp_zip, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == "word/media/image4.png":
                with open("results/fig2_shap_beeswarm.png", "rb") as f:
                    zout.writestr(item, f.read())
                print("  Replaced image4.png with results/fig2_shap_beeswarm.png")
            elif item.filename == "word/media/image5.png":
                with open("results/fig4_fairness_audit.png", "rb") as f:
                    zout.writestr(item, f.read())
                print("  Replaced image5.png with results/fig4_fairness_audit.png")
            else:
                zout.writestr(item, zin.read(item.filename))

os.replace(tmp_zip, target_path)
shutil.copyfile(target_path, copy_path)
print(f"Successfully updated {target_path} and {copy_path}!")

# Count words
doc_check = docx.Document(target_path)
total_words = sum(len(p.text.split()) for p in doc_check.paragraphs)
for t in doc_check.tables:
    for row in t.rows:
        for c in row.cells:
            total_words += len(c.text.split())
print(f"Final Paper Word Count: {total_words} words across {len(doc_check.paragraphs)} paragraphs.")

