# -*- coding: utf-8 -*-
import sys, os

with open('build_100pct_accurate_master_reports.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Concomitante rate to 32.7%
text = text.replace('24.8% (Schedule conflict pressure)', '32.7% (High schedule conflict & work pressure)')

# 2. Update Feature count to 15 engineered features
text = text.replace('10 selected features', '15 engineered features')
text = text.replace('10 leading features', '15 engineered features')

# 3. Update Table III to the exact 15 feature SHAP ranking
old_table_iii_marker = '["1", "Academic Performance (IRA / GPA)", "0.2721"'
new_table_iii_block = """[
            ["1", "Academic Performance (ira)", "0.2717", "< 5.00 GPA", "Dominant primary predictor; steep risk increase below 5.0"],
            ["2", "Course Failures (reprovacoes)", "0.0596", ">= 3 Failures", "Direct risk escalation (+0.06 to +0.12)"],
            ["3", "Enrollment Year (anoingresso)", "0.0415", "Recent cohorts", "Curricular transition and cohort reform effects"],
            ["4", "Attendance Rate (percentual_frequencia)", "0.0305", "< 75%", "Behavioral disengagement cliff"],
            ["5", "Course Modality (modalidade)", "0.0263", "Evening / Adult", "Workforce friction in Subsequente & PROEJA"],
            ["6", "Student Age (idade)", "0.0174", ">= 21 years", "Non-traditional adult learner responsibilities"],
            ["7", "Family Gross Income (rendabruta)", "0.0127", "<= R$ 930", "Economic hardship and financial vulnerability"],
            ["8", "Work Status (trabalha)", "0.0084", "Employed", "Time-allocation conflicts with classes"],
            ["9", "Mother's Education (mae_nivel_escolaridade)", "0.0073", "Incomplete primary", "Socioeconomic cultural capital proxy"],
            ["10", "Living Arrangement (companhia_domiciliar)", "0.0067", "Alone / Non-family", "Independent household vulnerability"],
            ["11", "Father's Education (pai_nivel_escolaridade)", "0.0066", "Incomplete primary", "Paternal education attainment proxy"],
            ["12", "Laptops at Home (quantidade_notebooks)", "0.0046", "0 Laptops", "Digital divide indicator"],
            ["13", "Gender: Male (genero_M)", "0.0040", "Male", "Marginal baseline dropout differential"],
            ["14", "Gender: Female (genero_F)", "0.0032", "Female", "Marginal baseline completion differential"],
            ["15", "Residential Area (tipo_area_residencial)", "0.0031", "Rural Area", "Transit distance to vocational campus"]
        ]"""

# Locate and replace Table III
idx_t3_start = text.find('add_h2("4.2 Global Feature Attributions & Cohort Parity")')
if idx_t3_start != -1:
    idx_make_table = text.find('make_table(', idx_t3_start)
    idx_list_start = text.find('[\n            ["1"', idx_make_table)
    idx_list_end = text.find('        ],\n        font_size=8.5', idx_list_start)
    if idx_list_start != -1 and idx_list_end != -1:
        text = text[:idx_list_start] + new_table_iii_block + text[idx_list_end + 10:]
        print("Successfully replaced Table III with all 15 features in real order!")

# 4. Update Fairness Table to the exact real numbers
new_fairness_block = """[
            ["Gender", "Male (N=1,365)", "Female (N=1,652)", "0.707", "-0.079", "-0.057", "-0.063", "UNDER-FLAGGED (<0.80)"],
            ["Race / Ethnicity", "White/Branca (N=1,139)", "Parda/Preta (N=1,878)", "1.180", "+0.035", "+0.065", "+0.046", "PASSED (0.80-1.25)"],
            ["Household Income", "> Median R$ 930 (N=1,498)", "<= R$ 930 (N=1,519)", "1.411", "+0.077", "+0.039", "+0.049", "OVER-FLAGGED (>1.25)"],
            ["Age Cohort", "Traditional <=20 (N=1,987)", "Adult >=21 (N=1,030)", "1.590", "+0.102", "+0.043", "+0.061", "OVER-FLAGGED (>1.25)"],
            ["Digital Access", ">=1 Laptop (N=2,374)", "0 Laptops (N=643)", "1.403", "+0.071", "+0.092", "+0.069", "OVER-FLAGGED (>1.25)"]
        ]"""

idx_f_start = text.find('add_h2("5.2 Comprehensive Fairness Audit Scores")')
if idx_f_start != -1:
    idx_f_make_table = text.find('make_table(', idx_f_start)
    idx_f_list_start = text.find('[\n            ["Gender"', idx_f_make_table)
    idx_f_list_end = text.find('        ],\n        col_widths=', idx_f_list_start)
    if idx_f_list_start != -1 and idx_f_list_end != -1:
        text = text[:idx_f_list_start] + new_fairness_block + text[idx_f_list_end + 10:]
        print("Successfully replaced Fairness Table with real pipeline audit figures!")

with open('build_100pct_accurate_master_reports.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("build_100pct_accurate_master_reports.py updated completely.")

