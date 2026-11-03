# Limitations & Threats to Validity

> **Document Type:** Methodological Disclosure & Threats to Validity  
> **Associated Project:** Explainable AI Governance Framework for Fair Student Performance Evaluation (Replication and Extension of Silva et al., IEEE RITA 2025)

---

## 1. Single-Institution Context & Generalizability

The empirical analysis in this study is based entirely on administrative records from a single public educational institution in Brazil (**Instituto Federal de Educação, Ciência e Tecnologia do Maranhão - IFMA**). 
- Institutional characteristics, regional socioeconomic disparities in northeastern Brazil, course structures, and evaluation grading policies are specific to the Brazilian Federal Institute system (*Rede Federal de Educação Profissional, Científica e Tecnológica*).
- **Threat:** Findings, risk distributions, and feature importance rankings (such as the dominance of attendance and course failures) cannot be assumed to generalize to other institutions, higher-education universities, or vocational education systems in other countries without formal multi-site recalibration and validation.

---

## 2. Cross-Sectional Data Structure & Lack of Longitudinal Records

The dataset (`dataset_evasao_MDE.xlsx`) provides a static, single-snapshot administrative extract with exactly one record per student ($N = 15,084$ in the modeled cohort).
- **Absence of Timestamps:** There are no semester-by-semester longitudinal records ($t_1, t_2, \dots, t_k$). Key predictors such as cumulative course failures (`reprovacoes`) and attendance percentage (`percentual_frequencia`) represent aggregated totals accumulated across the student’s enrollment tenure.
- **Threat:** The model is structurally a **retrospective risk-profile model**, not a dynamic early-warning system. It cannot predict whether a student will drop out at a specific future semester horizon $t$. The term "early warning" is fundamentally a misnomer for cross-sectional models trained on outcome-accumulated variables.

---

## 3. Large-Scale Cohort Exclusion & Selection Bias

From the initial institutional extract of 48,311 student records, exactly **33,227 records were excluded** to construct the 15,084 modeled cohort:
- **Active Enrollees:** 27,310 students (82.2% of excluded rows) were actively enrolled (`Matriculado`) and had not yet reached a terminal completion or dropout status.
- **Suspended Records:** 2,114 students (6.4%) had temporarily locked or voluntarily suspended enrollment (`Trancado Voluntariamente` or `Trancada`).
- **Other Exclusions:** 1,192 students graduated under the administrative code `Formado`, while others were awaiting diploma issuance or internships.
- **Threat:** Because recent cohorts (e.g., 2020–2023) primarily consist of active enrollees who have not yet had time to graduate, those who exited in recent years were predominantly fast dropouts. This right-censoring induces cohort selection bias, as evidenced by the inverse predictive signal in enrollment year (`anoingresso`).

---

## 4. Protected Attribute Representations & Intersectional Limitations

- **Binary Gender Encoding:** The administrative system records gender as a binary classification (`F` vs. `M`). Non-binary, agender, and transgender students are unrepresented in the data, preventing algorithmic equity auditing for gender-diverse populations.
- **Self-Reported Demographic Categories:** Race and ethnicity (`raca`) rely on self-declaration at enrollment. Disparities in categorization (e.g., `Não declarado` or institutional classification variances) may obscure nuanced intersectional barriers.

---

## 5. Unverified Logging of Zero-GPA Values (`ira == 0.0`)

An empirical audit of the raw dataset revealed that **10.49% of the cohort (1,583 students)** possess a recorded GPA of exactly 0.0:
- In adult education (`Subsequente`), zero GPA is 89.6% predictive of dropout, indicating administrative withdrawal or absence of grades.
- In integrated high schools (`Integrado`), **551 students with a recorded GPA of 0.0 successfully completed and graduated**, each possessing 0 course failures and an average attendance of 99.8%.
- **Threat:** Zero GPA reflects an unverified administrative logging reality (uncompiled or missing grades in the institutional ERP) rather than literal academic failure. While GPA was excluded to avoid target leakage, this underscores that administrative variables in educational ERPs often encode system artifacts.

---

## 6. Absence of Intervention Evidence

While machine learning classifiers can identify statistical correlations between student attributes and historical dropout, **the model provides no causal evidence regarding intervention efficacy**:
- Flagging a student as "at risk" does not guarantee that institutional counseling, tutoring, or financial aid will prevent attrition.
- Improperly implemented alerts risk generating counter-therapeutic effects, teacher expectancy bias (the Pygmalion effect), or student stigmatization.

---

## 7. Status of the Governance Framework

The institutional governance charter and the multi-tiered risk workflow presented in this study represent **normative institutional proposals**:
- **No Pilot Study:** The governance framework has not been evaluated in live operational deployment.
- **Untested Administrative Capacity:** The feasibility of counselor caseload limits (e.g., 50 cases/week) and the efficiency of the independent appeals body remain theoretical benchmarks that require prospective organizational evaluation.

