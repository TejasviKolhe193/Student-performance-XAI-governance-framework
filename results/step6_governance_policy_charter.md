# Operational AI Governance Charter: Five Institutional Pillars
## Proposed Governance Framework for Educational Risk Classification (Not Field-Tested)

> **Mandatory Institutional Disclaimer**:
> This governance framework is a **proposed operational design and has not been field-tested in an active educational setting**. No pilot deployment, randomized trial, or formal user study with academic counselors was conducted. All risk bands, review protocols, and intervention thresholds are heuristic policy recommendations that require empirical validation prior to institutional adoption.

---

### Pillar 1: Strictly Advisory, Non-Punitive Deployment
Predictive model inferences are classified strictly as clinical-advisory signals designed solely to trigger supportive institutional retention mechanisms (e.g., remedial peer tutoring, transportation assistance, social worker outreach). Under no circumstances may an automated prediction be used to sanction, dismiss, track into lower academic streams, or deny institutional re-enrollment to any student.

### Pillar 2: Mandatory Explainability-Coupled Outreach
Educational counselors and faculty members are prohibited from initiating student outreach based solely on an aggregate risk probability. Prior to contacting a flagged student, staff must inspect the individualized feature attribution breakdown (top SHAP and LIME factors). Support interventions must directly address the identified friction point—such as socioeconomic aid for financial hardship or academic tutoring for course failures.

### Pillar 3: Scheduled Semi-Annual Auditing & Drift Triggers
The predictive system must undergo formal **semi-annual algorithmic audits** scheduled prior to the start of each academic semester. Audits must evaluate:
1. Disparate Impact (Four-Fifths Rule screening heuristic: 0.80–1.25) across Gender, Race/Ethnicity, Household Income, Age, and Digital Access.
2. Equal Opportunity Difference (True Positive Rate parity: |EOD| <= 0.10) with Holm-Bonferroni correction.
3. Unscheduled out-of-cycle audits are automatically triggered if: (a) curriculum requirements change, (b) student demographic composition shifts by >10%, or (c) quarterly prediction volume deviates by >15% from historical baselines. Any statistically significant degradation in fairness triggers immediate model suspension and review.

### Pillar 4: Student Notice, Explanation Access & Appeal Rights (LGPD Alignment)
In accordance with Brazilian General Data Protection Law (LGPD Art. 20) and international data ethics standards:
- Students flagged for secondary or specialized institutional interventions must receive clear, plain-language notice explaining that an algorithmic tool assisted in identifying support opportunities.
- Students maintain an unconditional right to inspect the primary factors contributing to their assessment and to request human review.
- Students possess a formal procedural avenue to challenge and correct erroneous administrative records (such as misrecorded attendance or outdated household income brackets), initiating a mandatory recalculation of their risk profile within 10 business days.

### Pillar 5: Certified Human-in-the-Loop Override Authority
Final intervention determinations rest exclusively with certified educational counselors, social workers, and multidisciplinary student support committees. Human professionals retain absolute, unilateral authority to override, downgrade, or dismiss algorithmic alerts based on qualitative context, clinical judgment, or personal student disclosures. Under no circumstances may algorithmic recommendations supersede human decision-making.
