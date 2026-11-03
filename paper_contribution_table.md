# Research Contributions & Framework Scope Framing

## 1. Research Positioning & Honest Contribution Statement

This research replicates and empirically extends the landmark study by **Silva et al. (IEEE RITA 2025)**:
> Silva, F. da C., Santana, A. M., & Feitosa, R. M., *"An Investigation Into Dropout Indicators in Secondary Technical Education Using Explainable AI,"* IEEE Revista Iberoamericana de Tecnologias del Aprendizaje (IEEE RITA), vol. 20, 2025.

### Replicating Base Pipeline vs. Addressing Methodological Scope
Earlier preliminary designs considered introducing cumulative Grade Point Average (`ira`) under the assumption that it represented first-year academic performance. However, auditing of administrative schemas revealed that `ira` is computed retrospectively across students' entire enrollments—thereby introducing target leakage for completed students and administrative post-mortem artifacts for early dropouts (`ira = 0.0`). 

**Honest Contribution Statement**:
We explicitly **drop the early-warning GPA extension (Gap 1)** and **revert completely to the verified feature set and administrative retrospective risk-profiling methodology of Silva et al.** No cumulative GPA, no GPA-missing indicators, and no enrollment duration features are claimed or included. Attendance (`percentual_frequencia`) and Failures (`reprovacoes`) are retained strictly because Silva et al. established them as valid administrative attributes in Table II.

Our actual novel scientific contributions consist of:
1. **Methodological Pipeline Integrity**: Replicating the 48-experiment benchmark across strict, leak-free `imblearn` cross-validation pipelines (guaranteeing that outlier clipping, imputation, and balancing occur strictly within training folds).
2. **Comprehensive Algorithmic Fairness Audit**: Extending the baseline model with multi-group demographic parity, disparate impact, and equal opportunity audits across Gender, Race/Ethnicity, Income, Age, and Home Computer Access (Four-Fifths Rule, AIF360, Holm-Bonferroni correction, and Reweighing mitigation).
3. **Operational AI Governance Charter**: Defining an institutional 5-pillar advisory governance charter and operational risk-band calibration framework to govern responsible human-in-the-loop deployment in public education.

---

## 2. Updated Contribution Matrix

| Dimension | Base Paper: Silva et al. (IEEE RITA 2025) | Our Replicated & Extended Framework | Framing Status |
| :--- | :--- | :--- | :--- |
| **Problem Formulation** | Retrospective student dropout risk profiling using administrative records | Retrospective student dropout risk profiling using administrative records | **Exact Replication** (Dropped broken early-warning GPA claim) |
| **Predictive Features** | 19 administrative & demographic features (Attendance, Failures, Socioeconomic, Campus, Modality) | Exact 19 administrative & demographic features; **zero GPA / leakage features** | **Exact Replication** |
| **Experimental Matrix** | 48 experiments (4 Classifiers × 4 Balancing × 3 Feature Selection) | 48 experiments replicated with strict leak-free `imblearn` pipeline integrity | **Replication & Verification** |
| **Explainable AI (XAI)** | Global & local TreeSHAP + LIME on Champion RF and DT | TreeSHAP beeswarm & waterfall + LIME local surrogates + Top-3 Jaccard overlap | **Replication & Verification** |
| **Algorithmic Fairness** | **None** (Explicitly identified as open research gap in Section VI) | Multi-attribute fairness audit (DI, SPD, EOD) with AIF360, threshold sensitivity (0.30, 0.50, 0.70), Holm correction, and Reweighing trade-off | **Novel Extension 1 (Fairness Audit)** |
| **Governance Policy** | High-level discussion of educational policy implications | 5-Pillar Operational Governance Charter + Calibrated Risk-Band Intervention Allocation Table | **Novel Extension 2 (Governance Charter)** |

---

## 3. Methodological Integrity Clarification
* The governance charter is a policy proposal. No live clinical pilot or human user study was conducted.
* All figures, metrics, and comparisons are evaluated on a clean 70/30 stratified split with fixed random seeds (`random_state=42`).

