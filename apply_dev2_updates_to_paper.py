import docx
import shutil
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("UPDATING RESEARCH PAPER WITH DEV2 METHODOLOGY, NUMBERS & MENTOR FIXES")
print("=" * 80)

src_path = "paper_review/research_paper_final_draft.docx"
target_path = "paper_review/research_paper_final_draft.docx"
copy_path = "paper_review/research_paper_final_with_updates.docx"

doc = docx.Document(src_path)

# Dictionary of paragraph replacements mapped to exact dev2 results and mentor comments
updates = {
    # TITLE & ABSTRACT
    17: (
        "Abstract—Student dropout undermines educational attainment and institutional viability in public vocational education. "
        "While predictive machine learning offers opportunities for timely support, deploying opaque models risks inequitable intervention "
        "and algorithmic harm. We present an end-to-end framework integrating machine learning, dual macro/micro explainability, "
        "algorithmic fairness auditing, and operational governance for student dropout risk classification. "
        "Using 15,084 secondary technical student records from the Instituto Federal do Norte de Minas Gerais (IFNMG) partitioned "
        "via a 70/30 stratified split (10,558 training, 4,526 test), we evaluated 48 pipeline configurations without retrospective GPA (ira), "
        "strictly eliminating target leakage. A Random Forest model with Random Under-Sampling and Tree Feature Importance (k=19) "
        "was selected as champion, achieving Recall of 73.18% (95% CI: [70.48%, 76.00%]), Precision of 75.64% (95% CI: [72.83%, 78.19%]), "
        "Accuracy of 88.71% (95% CI: [87.78%, 89.62%]), ROC-AUC of 0.8968 (95% CI: [0.8836, 0.9098]), and Brier Score of 0.1080 (baseline 0.1738). "
        "TreeSHAP feature attribution identified course failures (reprovacoes, 32.37%), attendance percentage (percentual_frequencia, 19.26%), "
        "and enrollment cohort year (anoingresso, 10.78%) as primary drivers, accounting for 62.41% of total attribution. "
        "Local LIME surrogates demonstrated moderate agreement with SHAP across student archetypes (mean top-3 Jaccard overlap 66.7%). "
        "Algorithmic fairness audits across five protected dimensions (Gender, Race, Household Income, Age, and Home Computer Ownership) "
        "under the Four-Fifths screening heuristic revealed gender disparity (Disparate Impact 0.7383, female recall 70.87% vs. male 75.09%, "
        "Equal Opportunity Difference -0.0422, p=0.1354) and statistically significant socioeconomic True Positive Rate gaps on Income (p=0.00043) "
        "and Computer Ownership (p=0.00089) under Holm-Bonferroni correction. Pre-processing AIF360 Reweighing tightened Equal Opportunity "
        "but induced an acute 12.82 percentage point drop in recall (73.18% to 60.36%). Consequently, we propose a non-punitive operational "
        "governance charter incorporating role-based access control, semi-annual audits, heuristic risk bands, and Brazilian LGPD Art. 20 "
        "contestability rights. This governance framework represents a proposed design that has not been field-tested in live operations."
    ),

    # INTRODUCTION
    19: (
        "Student attrition undermines educational equity and institutional viability in public secondary technical education. "
        "In Brazilian Federal Institutes (IFNMG), non-completion rates reach 22.4%, compounding socioeconomic stratification and squandering "
        "public vocational investments. While Sustainable Development Goals (SDG 4 and SDG 10) provide broad conceptual motivation, "
        "practical retention requires actionable, fair, and legally compliant predictive systems."
    ),
    20: (
        "Standard predictive accuracy is insufficient when algorithmic inferences inform academic support: false negatives leave vulnerable "
        "students unassisted, while false positives waste scarce counseling resources. Crucially, in administrative datasets, cumulative GPA (ira) "
        "is frequently computed retrospectively across complete tenures, introducing severe target leakage. Predicting dropout requires restricting "
        "predictors strictly to verifiable administrative and academic friction features prior to terminal departure. Furthermore, predictive models "
        "risk encoding historical demographic inequities, demanding rigorous multi-dimensional fairness audits."
    ),
    21: (
        "Existing literature addresses prediction, explanation, fairness, and governance in isolation. Landmark studies by Silva et al. [1] and "
        "Zanellati et al. [2] benchmark classifiers and local explanations but omit group fairness audits and institutional policy design. "
        "Conversely, algorithmic fairness toolkits [14] rarely evaluate the operational trade-offs of debiasing in public education. "
        "The core research gap is therefore operational integration: embedding leak-free machine learning, calibrated risk stratification, "
        "and human-in-the-loop oversight into an institutional governance architecture."
    ),
    22: (
        "To address this gap, we formulate four explicit research questions: "
        "RQ1 (Predictive Utility): Can a leak-free pipeline trained strictly on administrative and academic friction features reliably classify "
        "dropout risk without retrospective GPA? "
        "RQ2 (Explanation Consistency): Do TreeSHAP and LIME identify consistent, educationally actionable risk indicators across student archetypes? "
        "RQ3 (Group Fairness): Does the model maintain demographic parity and equal opportunity across protected groups, and can pre-processing debiasing "
        "mitigate disparities without destroying recall? "
        "RQ4 (Governance Feasibility): How can risk probabilities, explanations, and procedural appeals be formalized into an operational, non-punitive charter?"
    ),
    23: (
        "The primary contribution is an integrated, leak-free framework: (1) a 48-experiment benchmark on 15,084 students without GPA, selecting a Random Forest "
        "champion (Recall 73.18%, ROC-AUC 0.8968); (2) dual macro/micro explainability establishing course failures and attendance as top predictors (62.41% top-3 share); "
        "(3) a multi-dimensional fairness audit evaluating DI, SPD, and EOD with Holm-Bonferroni correction and AIF360 Reweighing trade-off analysis; and "
        "(4) a proposed operational governance framework with heuristic risk bands, semi-annual audits, and LGPD-aligned student appeal rights (not field-tested)."
    ),

    # LITERATURE REVIEW
    26: (
        "Student outcome research has transitioned from feasibility demonstrations to operational accountability. Silva et al. [1] applied Random Forests "
        "and Decision Trees with LIME and SHAP on 15,084 IFNMG records, establishing attendance and course failures as primary indicators; however, their "
        "pipeline lacked algorithmic fairness audits and institutional governance. Zanellati et al. [2] balanced explainability and accuracy across 2,000+ "
        "degree programs but omitted group equity safeguards. In admission modeling, Priyadarshini and Gago-Masague [3] utilized adversarial debiasing, "
        "highlighting accuracy-fairness tensions. Mengash [4] and Alhazmi and Sheneamer [5] demonstrated early prediction but treated models as black boxes. "
        "Pelima et al. [6] surveyed 45 ML graduation studies, identifying systematic under-reporting of institutional governance. Ma et al. [7] and "
        "Jiang and Wang [8] advanced cognitive diagnostic models, while Zhang and Yang [9], Zhou [10], and Lu et al. [11] explored fuzzy evaluation, "
        "neural assessment, and decision analysis. Crucially, Kleinberg's impossibility theorem [15] proves that demographic parity, equalized odds, "
        "and calibration cannot simultaneously hold when group base rates differ. In this work, we prioritize Equal Opportunity (recall parity among dropouts) "
        "as our primary ethical standard, treating Disparate Impact as an administrative screening heuristic."
    ),

    # METHODOLOGY
    29: (
        "The methodology operationalizes student dropout screening into a five-phase leak-free workflow: (1) institutional cohort extraction and "
        "preprocessing without retrospective GPA; (2) a 48-configuration factorial benchmark under nested cross-validation; (3) dual macro (TreeSHAP) "
        "and micro (LIME) explainability; (4) a five-axis algorithmic fairness audit with Holm-Bonferroni FWER control; and (5) an operational governance "
        "charter with heuristic risk bands and human-in-the-loop oversight (Fig. 1)."
    ),
    32: (
        "Data derive from administrative enrollment records of the Instituto Federal do Norte de Minas Gerais (IFNMG) (dataset_evasao_MDE.xlsx) "
        "[AUTHOR TO CONFIRM: Dataset URL & License] [AUTHOR TO CONFIRM: Cohort date range]. The raw database contains 48,311 student records across all levels. "
        "Filtering strictly for secondary technical modalities (Integrado, Concomitante, Subsequente, Integrado EJA) yields 15,084 terminal student records "
        "[AUTHOR TO CONFIRM: Exclusion counts by reason]. Terminal outcomes were mapped to a binary target: Completed (Class 0, N=11,703, 77.59%) versus "
        "Dropout / Non-completion (Class 1, N=3,381, 22.41%), combining voluntary dropout (1,760), cancellation (446), compulsory dismissal (346), "
        "jubilated status (38), and external transfers (791). Grouping transfers and expulsions with dropout represents an administrative necessity "
        "subject to sensitivity analysis."
    ),
    33: (
        "A stratified 70/30 split partitioned the 15,084 records into 10,558 training and 4,526 held-out test students (random_state=42). "
        "Crucially, cumulative GPA (ira) was completely excluded to eliminate retrospective target leakage. After dropping identifiers (alunoid) "
        "and four variables with >20% missingness (dataconclusao, forma_acesso_seletivo, razao_ausencia_educacional, pontuacao_seletivo), "
        "19 baseline administrative and academic friction features remained. Minor missingness in computers (6.17%) and notebooks (5.20%) was median-imputed. "
        "Continuous features underwent 1.5x IQR Winsorization fitted strictly on training folds. One-Hot Encoding on gender, race, and marital status "
        "expanded the design matrix to 34 encoded columns."
    ),
    35: (
        "The 48-condition factorial grid crossed 4 balancing strategies (Unbalanced, RandomUnderSampler, SMOTE, SMOTEENN), 3 feature selection methods "
        "(ANOVA F-test, Backward Elimination / RFE, Tree Feature Importance, selecting k=19 features), and 4 classifiers (Random Forest, Decision Tree, "
        "Logistic Regression, Linear Support Vector Machine). To guarantee zero data leakage, resampling, scaling, and feature selection were executed "
        "strictly inside 10-fold cross-validation training folds using imblearn.pipeline.Pipeline, keeping validation folds at natural 22.4% prevalence. "
        "The champion model was selected via a constrained utility rule: highest Recall subject to Precision >= 60% and ROC-AUC >= 0.90 on training CV folds."
    ),
    38: (
        "Global interpretability applied TreeSHAP [19] on the probability scale across the held-out test cohort (N=4,526). Mean absolute SHAP values "
        "quantified institutional feature attribution shares relative to the total attribution denominator. Local micro-explanations utilized LIME [13] "
        "fitted on training data to generate localized decision boundaries for High-Risk, Borderline, and Low-Risk student archetypes. Explanation stability "
        "was measured via top-3 Jaccard similarity across explainers."
    ),
    40: (
        "Fairness was audited on the 4,526 held-out test students across five protected dimensions: Gender (Male vs. Female), Race (Branca vs. Parda, "
        "Branca vs. Preta), Household Income (> Median vs. <= Median R$ 930), Age (<= 20 vs. > 20 years), and Home Computer Ownership (>= 1 vs. 0). "
        "Metrics included Disparate Impact (evaluated under the Four-Fifths screening heuristic [20], 0.80 <= DI <= 1.25), Statistical Parity Difference (SPD), "
        "Equal Opportunity Difference (EOD = TPR_u - TPR_p), and False Positive Rate gaps. Holm-Bonferroni step-down correction controlled Family-Wise "
        "Error Rate across EOD p-values. Pre-processing AIF360 Reweighing [14] was evaluated as a debiasing intervention."
    ),
    42: (
        "Section IV-E details the proposed institutional governance policy charter (not field-tested). The charter codifies role-based access control (RBAC), "
        "semi-annual review cadences, heuristic risk bands (<0.20 minimal, 0.20-0.40 low concern, 0.40-0.60 watchlist, 0.60-0.80 high priority, >=0.80 emergency), "
        "student appeal rights under Brazilian LGPD Art. 20 [22], and unilateral counselor override authority."
    ),

    # RESULTS AND DISCUSSION
    44: (
        "Figures refer to the 4,526-student held-out test set (70/30 split) unless noted; baseline prevalence is 22.40% (1,014 dropouts, 3,512 completed)."
    ),
    46: (
        "The 70/30 stratified split yielded 10,558 training students (Class 0: 8,191, Class 1: 2,367) and 4,526 test students (Class 0: 3,512, Class 1: 1,014). "
        "Baseline dropout prevalence is 22.41% in training and 22.40% in testing, confirming rigorous stratification."
    ),
    47: (
        "Baseline attrition varies substantially across educational modalities (Fig. 2): Integrado EJA exhibits highest non-completion (42.8%), "
        "followed by Subsequente (30.1%), Concomitante (24.7%), and Integrado (18.6%). These discrepancies reflect structural adult-learner commitments "
        "rather than intrinsic institutional deficits."
    ),
    50: (
        "Two dominant behavioral patterns characterize the cohort: (1) an attendance cliff (Fig. 3), where dropout rates surge below the 75% legal minimum; "
        "and (2) failure accumulation, where dropouts average 5.99 failed courses (median 3, max 69) versus 0.77 for completers (75% have <= 1 failure)."
    ),
    54: (
        "The Random Forest champion (RandomUnderSampler, Tree Feature Importance k=19, n_estimators=100, max_depth=10, min_samples_leaf=5, random_state=42) "
        "achieved on the 4,526 test students: Recall 73.18% (95% CI: [70.48%, 76.00%]), Precision 75.64% (95% CI: [72.83%, 78.19%]), "
        "F1-Score 0.7439 (95% CI: [0.7235, 0.7664]), Accuracy 88.71% (95% CI: [87.78%, 89.62%]), and ROC-AUC 0.8968 (95% CI: [0.8836, 0.9098]). "
        "The confusion matrix confirms TP=742, FP=239, TN=3,273, FN=272. A majority-class baseline yields 77.60% accuracy but 0.00% recall. "
        "An attendance-only baseline (threshold <= 91%) captures only 32.15% of dropouts (Precision 63.92%, continuous ROC-AUC 0.5945)."
    ),
    55: (
        "Alternative candidate models failed operational requirements. While Decision Tree under the same pipeline achieved higher test recall (75.05%), "
        "its precision was lower (67.05%) and its 10-fold CV ROC-AUC (0.8875) failed the >= 0.90 threshold. Linear SVM with SMOTEENN achieved 60.55% recall "
        "but collapsed in precision (45.08%), generating unacceptable false alarm burdens (54.9% false alarms). The Random Forest model uniquely satisfied "
        "our constrained utility rule on training cross-validation (CV Recall 74.95%, CV Precision 76.94%, CV ROC-AUC 0.9144)."
    ),
    57: (
        "TreeSHAP attributions across the 4,526 test students (total mean |SHAP| denominator = 0.407016) demonstrate that academic friction dominates prediction. "
        "Course failures (reprovacoes) contributes 32.37% (mean |SHAP| = 0.1317), attendance percentage (percentual_frequencia) contributes 19.26% "
        "(mean |SHAP| = 0.0784), and cohort year (anoingresso) contributes 10.78% (mean |SHAP| = 0.0439). Together, these top three features account for "
        "62.41% of total model attribution (recomputed numerator 0.254029 / denominator 0.407016). Secondary factors include modality (6.95%), "
        "age (6.31%), family income (5.78%), course (3.61%), campus (2.84%), employment (2.48%), and gender (combined M+F share 3.66%)."
    ),
    58: (
        "The global beeswarm plot (Fig. 4) illustrates directional mechanisms: high course failures (red) strongly shift log-odds toward dropout, "
        "while high attendance (>90%) provides robust protective attribution against attrition."
    ),
    62: (
        "Local explanations provide individualized recourse profiles for educational counselors. Across three representative archetypes, TreeSHAP and LIME "
        "exhibit moderate feature concordance: High-Risk student #815 (P(Dropout)=94.8%, Jaccard overlap 0.50), Borderline student #4078 (P(Dropout)=48.0%, "
        "Jaccard overlap 0.50), and Low-Risk student #4458 (P(Dropout)=10.7%, Jaccard overlap 1.00). Across archetypes, mean top-3 Jaccard overlap is "
        "66.67% (range [0.50, 1.00]), demonstrating moderate agreement without confirming ground-truth explanatory reliability."
    ),
    65: (
        "Algorithmic fairness audits across the 4,526 test students at threshold tau=0.50 evaluate five protected dimensions (Fig. 5). "
        "Under the Four-Fifths screening heuristic (0.80 <= DI <= 1.25), Disparate Impact flagged Gender (DI 0.7383), Race (Branca vs. Parda DI 1.2958; "
        "Branca vs. Preta DI 1.2694), Income (DI 1.5098), Age (DI 1.2864), and Computer Ownership (DI 1.5106). However, elevated selection rates "
        "for unprivileged groups are consistent with higher historical base rates (e.g., lower income dropout 25.75% vs. higher income 19.03%) but do not "
        "rule out algorithmic bias; False Positive Rate gaps remain modest (+2.76% for low income, +2.75% for no computer)."
    ),
    70: (
        "Under Equal Opportunity parity (EOD = TPR_u - TPR_p), Gender exhibits near-parity (EOD -0.0422, 95% CI: [-0.097, 0.013], p=0.1354). "
        "Applying Holm-Bonferroni correction across the 6 demographic EOD p-values reveals that Race (Branca vs. Parda EOD +0.1014, raw p=0.0144) "
        "does not survive the adjusted threshold (alpha/4 = 0.0125). Only Household Income (EOD +0.1007, p=0.00043) and Computer Ownership (EOD +0.1109, "
        "p=0.00089) exhibit statistically significant sensitivity differences."
    ),
    71: (
        "To mitigate demographic disparity, we evaluated AIF360 Reweighing pre-processing on training sample weights. While Reweighing slightly tightened "
        "gender EOD (-0.0422 to -0.0304) and increased precision (75.64% to 93.72%), it caused a catastrophic 12.82 percentage point drop in recall "
        "(73.18% to 60.36%). In educational dropout prevention where missing vulnerable students carries immense social cost, algorithmic debiasing alone "
        "is insufficient, mandating operational human-in-the-loop governance."
    ),
    75: (
        "Probability calibration was evaluated via Brier score (0.1080 vs. baseline 0.1738) and a 10-bin reliability diagram. Partitioning predictions into "
        "mutually exclusive heuristic risk bands reveals empirical alignment at extreme tiers: Emergency [0.80, 1.00] flags 567 students with 95.24% observed "
        "dropout, and High Priority [0.60, 0.80) flags 190 students with 63.68% observed dropout. However, probability inflation from UnderSampling occurs "
        "in the Watchlist band [0.40, 0.60), where mean predicted risk (48.6%) exceeds observed dropout (26.94%). Risk bands must therefore be treated as "
        "heuristic triage thresholds rather than direct probabilistic mappings."
    ),
    76: (
        "Proposed Governance Framework (Not Field-Tested): To govern operational triage responsibly, we specify an institutional AI Governance Charter "
        "grounded in five normative pillars: (1) Strictly Advisory, Non-Punitive Deployment, prohibiting automated sanctions or tracking; (2) Mandatory "
        "Explainability-Coupled Outreach, requiring counselors to inspect individualized SHAP/LIME feature attributions prior to student contact; "
        "(3) Scheduled Semi-Annual Fairness Auditing, enforcing DI and Holm-Bonferroni EOD reviews prior to each semester with automatic retraining triggers "
        "for demographic drift; (4) Institutional Contestability and Student Appeal Rights, aligned with Brazilian LGPD Art. 20 [22], guaranteeing students "
        "the right to explanation and record correction within a 10-business-day review timeline; and (5) Certified Human-in-the-Loop Override Authority, "
        "vesting counselors with unilateral power to dismiss algorithmic flags. For a cohort of 5,000 students, the baseline threshold (tau=0.50) flags 1,084 "
        "students, requiring 6 full-time counselors to fulfill a 4-week response SLA."
    ),

    # CONCLUSION & LIMITATIONS
    78: (
        "This research presented an Explainable and Fairness-Audited AI Governance Framework for secondary technical student dropout risk classification. "
        "By strictly eliminating retrospective GPA target leakage, our Random Forest benchmark on 15,084 IFNMG students (70/30 split) demonstrated robust "
        "performance (73.18% recall, 75.64% precision, 0.8968 ROC-AUC, 0.1080 Brier score). Dual explainability proved that course failures (32.37%) and "
        "attendance (19.26%) are the primary actionable predictors, with moderate local explainer concordance (66.7% mean Jaccard overlap)."
    ),
    79: (
        "Algorithmic auditing revealed that while gender satisfies Equal Opportunity parity (EOD -0.0422, p=0.1354), significant sensitivity gaps persist "
        "across income and digital access under Holm-Bonferroni correction. Because pre-processing debiasing induced a severe 12.82 pp recall penalty, "
        "fairness must be governed institutionally. Our five-pillar charter and heuristic risk bands establish an operational blueprint for responsible, "
        "non-punitive educational AI deployment."
    ),
    80: (
        "Limitations and Threats to Validity: (1) Data Provenance & Selection: Retrospective cohort from a single Brazilian institution (IFNMG, "
        "[AUTHOR TO CONFIRM: Cohort date range]); excluding active ongoing students introduces right-censoring. (2) Label Construct: Grouping cancellations, "
        "transfers, and expulsions into a single binary dropout target conflates heterogeneous attrition pathways. (3) Cumulative Feature Measurement Window: "
        "Course failures and attendance accumulate across students' multi-year tenures; cross-sectional data limitations prevent restricting features strictly "
        "to the first academic year. (4) Subgroup Uncertainty: Modality imbalances inflate estimation variance for small cohorts. (5) External Validity: "
        "Findings from a single Brazilian technical network cannot establish transferability to other institutions (e.g., Indian universities). "
        "(6) Untested Governance: The five-pillar charter and procedural safeguards represent a proposed operational design that has not been field-tested in live operations."
    )
}

print(f"Applying {len(updates)} paragraph updates...")
for p_idx, new_text in updates.items():
    if p_idx < len(doc.paragraphs):
        p = doc.paragraphs[p_idx]
        p.text = new_text
        # Ensure standard font formatting
        for run in p.runs:
            run.font.name = "Times New Roman"

doc.save(target_path)
shutil.copyfile(target_path, copy_path)
print(f"Successfully saved updated paper to {target_path} and {copy_path}!")

# Verify words and paragraph count
doc_check = docx.Document(target_path)
total_words = sum(len(p.text.split()) for p in doc_check.paragraphs)
print(f"Final Paper Word Count: {total_words} words across {len(doc_check.paragraphs)} paragraphs.")

