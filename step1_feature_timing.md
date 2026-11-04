# Step 1: Feature Timing and Data Granularity Audit

## 1. Data Provenance & Structure
- **Source File**: `dataset_evasao_MDE.xlsx`
- **Total Rows in File**: 48,311
- **Target Population (Secondary Technical Education)**: 15,084 student records matching the 4 technical modalities:
  - `Integrado`
  - `Concomitante`
  - `Subsequente`
  - `Integrado EJA`
- **Target Variable**: Terminal Status (`0 = Concluído [Completed]`, `1 = Non-completion [Dropout/Terminal Departure]`)
  - **Class 0 (Completed)**: 11,703 (77.59%) [Silva et al.: 11,703 / 77.6%]
  - **Class 1 (Non-completion)**: 3,381 (22.41%) [Silva et al.: 3,381 / 22.4%]
    - *Evasão* (Dropout): 1,760 (11.67%)
    - *Cancelado* (Voluntary cancellation): 446 (2.96%)
    - *Cancelamento Compulsório* (Compulsory administrative cancellation): 346 (2.29%)
    - *Jubilado* (Maximum tenure exceeded / dismissal): 38 (0.25%)
    - *Transferido Externo* (External transfer out): 791 (5.24%)

---

## 2. Granularity and Temporal Structure
- **Student Uniqueness**: The student identifier column `alunoid` is unique across all 15,084 rows (15,084 unique IDs). Each student record appears **exactly once**.
- **Cross-Sectional Structure**: The dataset is strictly cross-sectional. There are **no longitudinal, term-by-term tables, transcripts, or semester-indexed columns**.
- **Enrollment Cohort Window (`anoingresso`)**: Cohorts span admission years **2010 to 2022** (concentrated primarily in 2015–2019).
- **Exit Date Availability (`dataconclusao`)**:
  - Present for 11,699 students; missing for 3,385 students.
  - For Completed students (Class 0): 11,699 have completion dates recorded (4 missing).
  - For Dropout/Terminal students (Class 1): **0 have exit dates recorded** (100% missing in this column; dropout dates are omitted from the administrative export).

---

## 3. Measurement Window for Academic Predictors (`percentual_frequencia` and `reprovacoes`)
- **Cumulative Scope**: Because only a single aggregate numeric value exists per student, both `percentual_frequencia` and `reprovacoes` are calculated over the **entire institutional tenure of enrollment** up to departure, NOT over the first semester or first academic year.
- **Course Failures (`reprovacoes`)**:
  - Completed students (Class 0): Mean = 0.77 failures (75% have $\le 1$ failure, Max = 26).
  - Dropout students (Class 1): Mean = 5.99 failures (Median = 3, 75th percentile = 9, Max = 69).
  - Among dropouts, **48.8% accumulated $> 3$ failures**, and **21.3% accumulated $> 10$ failures**. Accumulating 10 to 69 failures is structurally impossible within the first year of a secondary curriculum, confirming multi-year accumulation.
- **Attendance Percentage (`percentual_frequencia`)**:
  - Completed students (Class 0): Mean = 97.52% (Std = 3.35%, Min = 59%).
  - Dropout students (Class 1): Mean = 92.34% (Std = 10.39%, Min = 37%).
- **Methodological Conclusion on Timing**:
  - The measurement window for academic friction variables is **cumulative multi-year institutional enrollment**, not an intake or first-year snapshot.
  - Consequently, claims of "early warning," "early identification," or "first-year screening" cannot be made unconditionally, as the administrative records encode academic events that unfolded across later semesters prior to formal departure.
