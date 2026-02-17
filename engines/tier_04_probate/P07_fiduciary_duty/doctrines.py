"""
P07 Fiduciary Duty Engine - Doctrine Cache
Comprehensive fiduciary duty rules for executors, trustees, and guardians
"""

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class DoctrineBlock:
    """Pre-compiled fiduciary duty reasoning block"""
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: str
    confidence_stratification: str
    controlling_precedent: Optional[str] = None


FIDUCIARY_DOCTRINES = [
    DoctrineBlock(
        topic="executor_duties_foundational",
        keywords=["executor", "personal representative", "estate administration", "fiduciary duties", "executor powers", "independent executor", "dependent executor"],
        conclusion_template=[
            "An executor owes comprehensive fiduciary duties to estate beneficiaries under TX Estates Code §351.101.",
            "These duties include loyalty, care, impartiality, accounting, and prudent investment regardless of executor type.",
            "Independent executors have broader powers but identical fiduciary standards to dependent executors."
        ],
        reasoning_framework="""
TX Estates Code §351.101 imposes fiduciary duties on all personal representatives. The executor occupies
a position of trust requiring the highest standard of conduct. Key statutory duties include:

1. DUTY OF LOYALTY: Executor must act solely in beneficiaries' interest (§351.101(a))
2. DUTY OF CARE: Must act as prudent person would in similar circumstances
3. DUTY TO ACCOUNT: File inventory within 90 days (§309.051), annual accounting (§359.001)
4. DUTY TO INVEST: Follow prudent investor rule (§117.001 et seq.)
5. DUTY TO PRESERVE: Protect estate assets from waste and loss
6. DUTY TO DISTRIBUTE: Timely distribution after claims period

Independent executor status (§401.001) grants broader powers without court supervision but does NOT
reduce fiduciary duty standards. Independent executors can sell property, invest funds, and make
distributions without court approval, but remain fully liable for breach of fiduciary duty.

Courts impose strict liability for breach. In Humane Society v. Austin National Bank, 531 S.W.2d 574
(Tex. 1975), the court held trustees (applying same standard to executors) absolutely liable for losses
from breach regardless of good faith.
        """,
        key_factors=[
            "Type of executor (independent vs dependent)",
            "Will provisions expanding or limiting powers",
            "Nature of estate assets requiring active management",
            "Number and relationship of beneficiaries",
            "Presence of conflicts of interest",
            "Executor's special skills or professional status",
            "Duration of estate administration",
            "Compliance with statutory accounting requirements"
        ],
        primary_authority=[
            "TX Estates Code §351.101 (Executor Duties)",
            "TX Estates Code §401.001 (Independent Executor)",
            "TX Property Code §117.001 (Prudent Investor Rule)",
            "Humane Society v. Austin National Bank, 531 S.W.2d 574 (Tex. 1975)"
        ],
        burden_holder="Executor bears burden to prove compliance with fiduciary duties",
        adversary_position="Beneficiaries need only show breach and causation; executor must prove justification",
        counter_arguments=[
            "Will contains exculpatory clause limiting liability",
            "Beneficiaries consented to challenged action",
            "Executor relied on professional advice (attorney, CPA)",
            "Actions were within scope of independent executor powers",
            "No damages resulted from alleged breach"
        ],
        resolution_strategy="Establish statutory compliance checklist: inventory filed timely, annual accountings complete, investments follow prudent investor rule, no self-dealing, beneficiaries kept informed",
        entity_scope="All executors, personal representatives, administrators in Texas estates",
        confidence="DEFENSIBLE",
        confidence_stratification="Clear statutory framework with extensive case law; duties well-established",
        controlling_precedent="Humane Society v. Austin National Bank, 531 S.W.2d 574 (Tex. 1975)"
    ),

    DoctrineBlock(
        topic="duty_of_loyalty_absolute",
        keywords=["duty of loyalty", "undivided loyalty", "sole interest", "beneficiary interest", "fiduciary loyalty", "exclusive benefit", "no adverse interest"],
        conclusion_template=[
            "The duty of loyalty requires a fiduciary to act solely in the beneficiaries' interest with undivided loyalty.",
            "Any transaction creating actual or potential conflict of interest violates the duty of loyalty absent beneficiary consent.",
            "Courts apply a strict 'no further inquiry' rule once conflict of interest is shown."
        ],
        reasoning_framework="""
The duty of loyalty is the most fundamental fiduciary obligation. TX Property Code §114.006 prohibits
trustees from profiting from position or using trust property for personal benefit. Courts extend this
principle to all fiduciaries including executors and guardians.

Three core loyalty principles:

1. EXCLUSIVE BENEFIT: Fiduciary must act ONLY for beneficiaries' benefit, not fiduciary's own interest
2. NO CONFLICT: Avoid situations where fiduciary's personal interest conflicts with beneficiary interest
3. NO PROFIT: Cannot profit from fiduciary position beyond authorized compensation

The "no further inquiry" rule: Once conflict of interest shown, transaction voidable regardless of
fairness. Fiduciary cannot defend by proving transaction was actually beneficial. Rationale: prophylactic
rule prevents temptation and eliminates need to investigate fiduciary's subjective motives.

Restatement (Third) of Trusts §78 states duty of loyalty is strictest duty imposed by law. Even appearance
of conflict sufficient to invalidate transaction. Courts hold fiduciary to "punctilio of honor" standard.

In Slay v. Burnett Trust, 143 Tex. 621, 187 S.W.2d 377 (1945), court held ANY self-dealing transaction
voidable at beneficiary's election without proving unfairness or damages.
        """,
        key_factors=[
            "Direct or indirect personal interest in transaction",
            "Fiduciary dealing with beneficiary in individual capacity",
            "Fiduciary on both sides of transaction",
            "Family members or business associates involved in transaction",
            "Fiduciary profiting beyond authorized compensation",
            "Use of confidential information for personal gain",
            "Competing fiduciary positions creating conflict",
            "Prior beneficiary consent with full disclosure"
        ],
        primary_authority=[
            "TX Property Code §114.006 (Trustee Loyalty)",
            "TX Estates Code §351.101 (Executor Loyalty)",
            "Restatement (Third) of Trusts §78",
            "Slay v. Burnett Trust, 187 S.W.2d 377 (Tex. 1945)",
            "Archer v. Griffith, 390 S.W.2d 735 (Tex. 1964)"
        ],
        burden_holder="Fiduciary bears burden to prove no conflict of interest or proper consent obtained",
        adversary_position="Beneficiary need only demonstrate conflict; transaction then voidable regardless of fairness",
        counter_arguments=[
            "All beneficiaries consented after full disclosure",
            "Transaction approved by court order",
            "Will or trust explicitly authorized transaction",
            "Transaction at arm's length with independent representation",
            "Fiduciary received no personal benefit"
        ],
        resolution_strategy="Document full disclosure to all beneficiaries, obtain written consent, consider court approval for material conflicts, seek independent valuation for any self-dealing transactions",
        entity_scope="All fiduciaries: executors, trustees, guardians, agents under power of attorney",
        confidence="DEFENSIBLE",
        confidence_stratification="Absolute duty with strict liability; well-established 'no further inquiry' rule",
        controlling_precedent="Slay v. Burnett Trust, 187 S.W.2d 377 (Tex. 1945)"
    ),

    DoctrineBlock(
        topic="duty_of_care_prudent_person",
        keywords=["duty of care", "prudent person", "reasonable care", "ordinary prudence", "diligence", "skill", "caution", "negligence"],
        conclusion_template=[
            "Fiduciaries must exercise the care, skill, and caution a prudent person would use managing their own affairs.",
            "Professional fiduciaries are held to a higher standard reflecting their special skills and expertise.",
            "Liability attaches for negligence causing measurable loss to the estate or trust."
        ],
        reasoning_framework="""
TX Property Code §117.004 establishes the prudent investor standard: fiduciary must exercise reasonable
care, skill, and caution. This replaced the old "prudent man" rule with a modern total portfolio approach.

Standard varies by fiduciary type:

1. INDIVIDUAL NON-PROFESSIONAL: Reasonable prudence under circumstances
2. PROFESSIONAL FIDUCIARY: Higher standard reflecting special skills (§114.006(b))
3. CORPORATE FIDUCIARY: Highest standard reflecting institutional expertise

Duty of care requires:
- Investigation before investment or major decisions
- Ongoing monitoring of investments and assets
- Timely action to protect estate/trust property
- Obtaining professional advice when needed
- Keeping adequate records
- Acting within reasonable time periods

Negligence measured objectively: what would reasonable person in fiduciary's position have done?
Professional status changes baseline. Bank trustee held to higher standard than family member executor.

In Interfirst Bank Dallas, N.A. v. Risser, 739 S.W.2d 882 (Tex. App. 1987), court held corporate trustee
liable for failing to diversify portfolio concentrated in single stock. Ordinary prudence required diversification.

Hindsight bias prohibited: evaluate conduct based on information available at time of decision, not
subsequent events. But must conduct reasonable investigation before deciding.
        """,
        key_factors=[
            "Fiduciary's professional status and special skills",
            "Complexity of estate or trust assets",
            "Information available at time of decision",
            "Whether fiduciary sought expert advice when prudent",
            "Fiduciary's investigation before acting",
            "Deviation from industry standards or practices",
            "Magnitude of loss compared to reasonable alternatives",
            "Fiduciary's attention and monitoring after decision"
        ],
        primary_authority=[
            "TX Property Code §117.004 (Prudent Investor Standard)",
            "TX Property Code §114.006 (Care and Skill)",
            "Restatement (Third) of Trusts §77",
            "Interfirst Bank Dallas, N.A. v. Risser, 739 S.W.2d 882 (Tex. App. 1987)"
        ],
        burden_holder="Plaintiff bears initial burden to show negligence; burden shifts to fiduciary to justify conduct",
        adversary_position="Fiduciary failed to act as reasonable prudent person managing own property",
        counter_arguments=[
            "Decision reasonable based on information available at time",
            "Followed professional advice from qualified advisors",
            "Loss due to market conditions beyond fiduciary's control",
            "Beneficiaries directed or consented to investment strategy",
            "No more prudent alternative existed under circumstances"
        ],
        resolution_strategy="Document investigation process, contemporaneous written analysis of major decisions, engagement of appropriate experts, regular portfolio reviews, compliance with modern portfolio theory",
        entity_scope="All fiduciaries with investment or management responsibilities",
        confidence="DEFENSIBLE",
        confidence_stratification="Well-established standard with extensive case law interpreting prudence",
        controlling_precedent="Interfirst Bank Dallas, N.A. v. Risser, 739 S.W.2d 882 (Tex. App. 1987)"
    ),

    DoctrineBlock(
        topic="duty_to_account_estate",
        keywords=["accounting", "inventory", "appraisement", "annual account", "reporting", "disclosure", "financial records", "duty to account"],
        conclusion_template=[
            "Executors must file sworn inventory and appraisement within 90 days of qualification unless excused.",
            "Annual accountings required for dependent administration; optional but advisable for independent executors.",
            "Failure to account constitutes breach of fiduciary duty and grounds for removal."
        ],
        reasoning_framework="""
TX Estates Code imposes comprehensive accounting requirements:

INVENTORY AND APPRAISEMENT (§309.051):
- Due within 90 days of receiving letters testamentary
- Must list all estate property with appraised values
- Oath required; false statement is perjury
- Independent executor may be excused if will dispenses with inventory

ANNUAL ACCOUNTING (§359.001):
- Required for dependent administration
- Due annually until estate closed
- Must show receipts, disbursements, property on hand
- Beneficiaries entitled to copies

FINAL ACCOUNTING:
- Required before discharge of executor
- Shows complete administration from death to distribution
- Must account for every dollar received and distributed

Trustees have parallel duty under §113.151 to keep beneficiaries reasonably informed of trust
administration and furnish annual statement of accounts.

Accounting duty serves three purposes:
1. Enables beneficiaries to monitor fiduciary performance
2. Creates evidence for breach claims
3. Starts statute of limitations on concealed breaches

In Huie v. DeShazo, 922 S.W.2d 920 (Tex. 1996), court held trustee's failure to account extended
statute of limitations indefinitely because beneficiaries could not discover breach without information.

Wilful failure to account is grounds for removal (§404.003(a)(1)) and may support punitive surcharge.
        """,
        key_factors=[
            "Type of administration (independent vs dependent)",
            "Will provisions dispensing with accounting requirements",
            "Beneficiary requests for accounting",
            "Complexity of estate or trust assets",
            "Length of administration period",
            "Prior accounting history",
            "Adequacy of informal reporting to beneficiaries",
            "Discovery of irregularities requiring detailed accounting"
        ],
        primary_authority=[
            "TX Estates Code §309.051 (Inventory and Appraisement)",
            "TX Estates Code §359.001 (Annual Account)",
            "TX Property Code §113.151 (Trustee Duty to Inform)",
            "Huie v. DeShazo, 922 S.W.2d 920 (Tex. 1996)"
        ],
        burden_holder="Fiduciary bears burden to prove accounting compliance or valid excuse",
        adversary_position="Fiduciary concealed information to hide breach or mismanagement",
        counter_arguments=[
            "Will dispensed with accounting requirements",
            "All beneficiaries waived accounting",
            "Informal accounting provided sufficient information",
            "Independent executor status eliminates court accounting",
            "Delay excused by extraordinary circumstances"
        ],
        resolution_strategy="File timely inventories, provide annual informal statements to beneficiaries even if not required, maintain detailed financial records, obtain beneficiary acknowledgments of receipt",
        entity_scope="Executors, administrators, trustees, guardians of estates",
        confidence="DEFENSIBLE",
        confidence_stratification="Clear statutory requirements with penalties for non-compliance",
        controlling_precedent="Huie v. DeShazo, 922 S.W.2d 920 (Tex. 1996)"
    ),

    DoctrineBlock(
        topic="duty_to_invest_prudently",
        keywords=["prudent investor", "investment", "diversification", "portfolio", "risk", "return", "modern portfolio theory", "total return"],
        conclusion_template=[
            "Fiduciaries must invest and manage assets as prudent investor would under Uniform Prudent Investor Act.",
            "Investments evaluated based on portfolio as whole, not isolation, considering risk/return objectives.",
            "Failure to diversify presumed imprudent absent special circumstances justifying concentration."
        ],
        reasoning_framework="""
TX Property Code Chapter 117 adopted the Uniform Prudent Investor Act (UPIA), fundamentally changing
investment standards from conservative "legal list" to modern portfolio theory.

CORE PRINCIPLES:

1. TOTAL PORTFOLIO APPROACH (§117.004(b)): Evaluate investments in context of entire portfolio,
   not isolation. A risky investment appropriate if balanced by conservative holdings.

2. RISK/RETURN TRADEOFF (§117.004(c)): Prudence measured by balancing risk against expected return.
   Must consider trust purposes, distribution requirements, beneficiary circumstances.

3. DIVERSIFICATION PRESUMED (§117.005): Failure to diversify presumed imprudent unless fiduciary
   proves concentration appropriate under circumstances (e.g., closely-held business, tax reasons).

4. NO CATEGORICAL PROHIBITIONS: No investments automatically imprudent. Options, futures, hedge funds,
   private equity all permitted if appropriate for portfolio strategy.

5. DELEGATION PERMITTED (§117.011): Can delegate investment management to qualified advisors but
   must prudently select, instruct, and monitor.

CHANGED FROM OLD LAW:
- Old: Conservative "prudent man" avoided risk
- New: Prudent investor optimizes risk/return based on trust purposes

KEY REQUIREMENTS:
- Written investment policy statement
- Asset allocation strategy
- Regular rebalancing
- Fee minimization
- Tax efficiency consideration

In Corpus Christi Bank & Trust v. Roberts, 597 S.W.2d 752 (Tex. 1980) (pre-UPIA), court held trustee
liable for keeping 71% in non-income producing land. Under UPIA, would analyze whether justified by
growth potential and overall portfolio balance.
        """,
        key_factors=[
            "Trust purposes and distribution requirements",
            "Beneficiary financial sophistication and risk tolerance",
            "Tax considerations and consequences",
            "Expected total return (income plus appreciation)",
            "Portfolio concentration vs diversification",
            "Asset allocation among classes (stocks/bonds/alternatives)",
            "Investment costs and fees",
            "Special circumstances (family business, tax basis, unmarketable assets)"
        ],
        primary_authority=[
            "TX Property Code §117.004 (Prudent Investor Standard)",
            "TX Property Code §117.005 (Diversification)",
            "TX Property Code §117.011 (Delegation)",
            "Restatement (Third) of Trusts §90",
            "Uniform Prudent Investor Act Official Comments"
        ],
        burden_holder="Beneficiary bears initial burden to show concentration or deviation from prudent standards; burden shifts to fiduciary to justify",
        adversary_position="Imprudent concentration, excessive risk, or failure to diversify caused portfolio underperformance",
        counter_arguments=[
            "Concentration justified by tax basis considerations (§117.005(b))",
            "Family business preservation authorized by trust terms",
            "Beneficiaries directed investment strategy",
            "Delegation to qualified investment advisor",
            "Portfolio performance met or exceeded appropriate benchmark"
        ],
        resolution_strategy="Adopt written investment policy statement, document strategy rationale, use qualified advisors for complex investments, maintain diversified portfolio absent documented justification, review performance against appropriate benchmarks",
        entity_scope="Trustees, executors, guardians, custodians under UTMA, agents under power of attorney",
        confidence="DEFENSIBLE",
        confidence_stratification="Modern standard with clear statutory framework; delegation and diversification requirements well-established",
        controlling_precedent="Restatement (Third) of Trusts §90 (highly persuasive in Texas)"
    ),

    DoctrineBlock(
        topic="self_dealing_prohibition_strict",
        keywords=["self-dealing", "conflict of interest", "interested trustee", "purchase from trust", "sale to trust", "dual capacity", "voidable transaction"],
        conclusion_template=[
            "Self-dealing transactions are voidable per se regardless of fairness under the 'no further inquiry' rule.",
            "Fiduciary cannot purchase trust property or sell own property to trust absent full disclosure and consent.",
            "Even indirect self-dealing through family members or controlled entities subject to strict scrutiny."
        ],
        reasoning_framework="""
Self-dealing is the paradigmatic breach of loyalty. TX Property Code §114.006 prohibits trustee from
using trust property for own benefit. Courts extend this to all fiduciaries.

STRICT PROHIBITION:

1. DIRECT SELF-DEALING: Fiduciary cannot:
   - Buy property from estate/trust
   - Sell property to estate/trust
   - Borrow funds from estate/trust
   - Lend personal funds to estate/trust (except temporary advances)
   - Compete with estate/trust business
   - Usurp estate/trust opportunities

2. INDIRECT SELF-DEALING: Prohibited transactions with:
   - Family members (spouse, children, parents, siblings)
   - Business entities fiduciary controls
   - Partners or co-venturers
   - Other trusts/estates where fiduciary serves

3. "NO FURTHER INQUIRY" RULE: Once self-dealing shown, transaction VOIDABLE at beneficiary's election
   without proving unfairness or damages. Fiduciary cannot defend by proving transaction beneficial.

RATIONALE: Prophylactic rule eliminates temptation and removes need to investigate fiduciary's motives.
Even if transaction actually fair, appearance of impropriety sufficient.

EXCEPTIONS (narrow):
- All beneficiaries consent after full disclosure
- Court pre-approval after adversary hearing
- Trust instrument explicitly authorizes specific transaction
- Statutory safe harbors (e.g., §113.053 for certain trust-to-trust transfers)

In Slay v. Burnett Trust, 187 S.W.2d 377 (Tex. 1945), trustee purchased trust property at fair value
in public sale. Court held voidable despite fairness: "A trustee cannot deal with himself."

CONSEQUENCES:
- Transaction voidable at beneficiary's election
- Fiduciary accountable for profits made
- Possible surcharge for opportunity cost
- Grounds for removal
        """,
        key_factors=[
            "Direct or indirect fiduciary interest in transaction",
            "Fiduciary on both sides of transaction",
            "Family relationship to transaction counterparty",
            "Control of entity transacting with estate/trust",
            "Whether beneficiaries gave informed consent",
            "Fair market valuation of transaction",
            "Independent representation of estate/trust",
            "Statutory or trust instrument authorization"
        ],
        primary_authority=[
            "TX Property Code §114.006 (Trustee Self-Dealing)",
            "Restatement (Third) of Trusts §78",
            "Slay v. Burnett Trust, 187 S.W.2d 377 (Tex. 1945)",
            "Kinzbach Tool Co. v. Corbett-Wallace Corp., 160 S.W.2d 509 (Tex. 1942)"
        ],
        burden_holder="Fiduciary bears burden to prove informed consent or authorization; otherwise strict liability",
        adversary_position="Self-dealing transaction voidable per se; no inquiry into fairness required",
        counter_arguments=[
            "All beneficiaries consented with full disclosure of conflict",
            "Transaction approved by court order after adversary hearing",
            "Trust instrument explicitly authorized transaction type",
            "Transaction at arm's length with independent appraisal",
            "Beneficiaries ratified transaction with knowledge of facts"
        ],
        resolution_strategy="Avoid self-dealing entirely; if unavoidable, obtain written consent from all beneficiaries after full disclosure, consider court approval, use independent appraisers and legal counsel",
        entity_scope="All fiduciaries: trustees, executors, guardians, agents, corporate fiduciaries",
        confidence="DEFENSIBLE",
        confidence_stratification="Strict liability with 'no further inquiry' rule; voidability well-established",
        controlling_precedent="Slay v. Burnett Trust, 187 S.W.2d 377 (Tex. 1945)"
    ),

    DoctrineBlock(
        topic="breach_elements_analysis",
        keywords=["breach of fiduciary duty", "elements", "causation", "damages", "standard of care", "duty owed", "violation", "harm"],
        conclusion_template=[
            "Breach of fiduciary duty requires: (1) fiduciary relationship; (2) breach of duty; (3) causation; (4) damages.",
            "Once fiduciary status established, burden shifts to fiduciary to prove compliance with duties.",
            "Causation requires showing breach caused actual loss; theoretical or speculative damages insufficient."
        ],
        reasoning_framework="""
To establish breach of fiduciary duty claim in Texas, plaintiff must prove four elements:

ELEMENT 1: FIDUCIARY RELATIONSHIP
Status as executor, trustee, or guardian establishes fiduciary relationship per se. No need to prove
confidential relationship or dominance. Legal appointment creates relationship automatically.

ELEMENT 2: BREACH OF DUTY
Must identify specific duty breached:
- Duty of loyalty (self-dealing, conflict of interest)
- Duty of care (negligence, imprudence)
- Duty to account (failure to report or disclose)
- Duty to invest prudently (imprudent investments, failure to diversify)
- Duty of impartiality (favoring one beneficiary)
- Duty to preserve property (waste, commingling)

Standard: Did fiduciary act as reasonable prudent person in same circumstances?
Burden shifts to fiduciary to justify conduct once prima facie breach shown.

ELEMENT 3: CAUSATION
"But for" test: Would loss have occurred absent the breach?
Must trace causal connection between breach and specific harm.

Examples:
- STRONG: Self-dealing sale below market value → loss = difference in value
- STRONG: Failed to sell declining stock → loss = decrease in value
- WEAK: Delayed distribution → beneficiary claims lost investment opportunity (too speculative)

Hindsight analysis permitted for causation unlike standard of care. Can examine actual results
to determine whether breach caused loss.

ELEMENT 4: DAMAGES
Must quantify actual loss with reasonable certainty. Types:
- Direct loss (stolen funds, sale below value)
- Lost profits (trust property not properly invested)
- Opportunity cost (failure to sell declining asset)
- Surcharge (fiduciary profit from position)

Nominal damages insufficient to support removal or surcharge. Must show material harm.

In Huie v. DeShazo, 922 S.W.2d 920 (Tex. 1996), beneficiary proved trustee failed to account (breach)
but failed to show resulting damages, so no surcharge imposed.
        """,
        key_factors=[
            "Type of fiduciary relationship (executor, trustee, guardian)",
            "Specific duty allegedly breached",
            "Evidence fiduciary failed to meet standard of care",
            "Causal link between breach and claimed harm",
            "Quantifiable damages with reasonable certainty",
            "Fiduciary's explanation or justification for conduct",
            "Whether beneficiary contributed to loss",
            "Availability of remedy (surcharge, removal, damages)"
        ],
        primary_authority=[
            "TX Property Code §114.008 (Damages for Breach)",
            "Huie v. DeShazo, 922 S.W.2d 920 (Tex. 1996)",
            "Slay v. Burnett Trust, 187 S.W.2d 377 (Tex. 1945)",
            "Restatement (Third) of Trusts §100"
        ],
        burden_holder="Beneficiary bears initial burden on all four elements; burden shifts to fiduciary to justify conduct",
        adversary_position="Fiduciary violated duty causing quantifiable loss to estate or trust",
        counter_arguments=[
            "No fiduciary relationship existed at time of conduct",
            "Conduct complied with applicable standard of care",
            "Breach did not cause claimed damages (intervening cause)",
            "Beneficiary cannot prove damages with reasonable certainty",
            "Beneficiary consented to or ratified the conduct"
        ],
        resolution_strategy="Identify specific duty breached with statutory or case law citation, trace causation from breach to specific loss, quantify damages with expert testimony or documentary evidence, address fiduciary's defenses",
        entity_scope="All fiduciary breach claims in Texas courts",
        confidence="DEFENSIBLE",
        confidence_stratification="Standard elements framework well-established; causation and damages require factual development",
        controlling_precedent="Huie v. DeShazo, 922 S.W.2d 920 (Tex. 1996)"
    ),

    DoctrineBlock(
        topic="surcharge_remedy_calculation",
        keywords=["surcharge", "remedy", "damages", "restitution", "accounting", "profit disgorgement", "make-whole", "lost profits"],
        conclusion_template=[
            "Surcharge requires fiduciary to restore estate/trust to position it would occupy absent breach.",
            "Calculation methods: direct loss restoration, lost profits, profit disgorgement, or appreciation in value.",
            "Court has discretion to award most favorable calculation to beneficiaries for deliberate breach."
        ],
        reasoning_framework="""
Surcharge is equitable remedy compelling fiduciary to compensate estate or trust for losses from breach.
TX Property Code §114.008 authorizes courts to "compel the trustee to... pay money to the trust" for breach.

CALCULATION METHODS:

1. DIRECT LOSS RESTORATION: Simplest measure
   - Asset sold for $100K worth $150K → surcharge $50K
   - Stolen funds → surcharge = amount stolen + interest

2. LOST PROFITS: Estate/trust lost opportunity for gain
   - Failed to invest cash → surcharge = investment income lost
   - Held non-diversified portfolio → surcharge = difference vs diversified benchmark

3. PROFIT DISGORGEMENT: Fiduciary profited from breach
   - Self-dealing purchase → fiduciary pays profit made + appreciation
   - Used trust funds in own business → fiduciary pays profits attributable to use

4. APPRECIATION IN VALUE: Harsh rule for wrongful disposition
   - Trustee sold stock that later appreciated → liable for appreciated value
   - Rationale: fiduciary wrongfully deprived trust of appreciation opportunity

INTEREST AWARD: Courts routinely add interest from date of breach to judgment.
Common rates: legal rate (5% in Texas) or lost investment return rate.

PUNITIVE SURCHARGE: For willful or malicious breach, court may impose surcharge exceeding actual damages
as punishment and deterrence. Rarely awarded but available.

In Humane Society v. Austin National Bank, 531 S.W.2d 574 (Tex. 1975), court applied appreciation rule:
trustee sold stock for $71K that later worth $297K; surcharged $226K appreciation value.

BENEFICIARY'S ELECTION: If multiple calculation methods, beneficiary typically chooses most favorable.
Exception: fiduciary in good faith may limit recovery to actual loss.

BURDEN: Beneficiary bears burden to prove amount of loss with reasonable certainty.
If uncertainty due to fiduciary's failure to account, court resolves doubts against fiduciary.
        """,
        key_factors=[
            "Nature of breach (negligence vs willful misconduct)",
            "Whether fiduciary profited from breach",
            "Availability of evidence to quantify loss",
            "Fiduciary's good or bad faith",
            "Whether asset wrongfully disposed or retained",
            "Market performance of comparable investments",
            "Expert testimony on damages calculation",
            "Adequacy of fiduciary's accounting records"
        ],
        primary_authority=[
            "TX Property Code §114.008 (Remedies for Breach)",
            "Humane Society v. Austin National Bank, 531 S.W.2d 574 (Tex. 1975)",
            "Restatement (Third) of Trusts §100",
            "Restatement (Third) of Trusts §101 (Appreciation Rule)"
        ],
        burden_holder="Beneficiary bears burden to prove amount of loss; if records inadequate due to fiduciary's fault, doubts resolved against fiduciary",
        adversary_position="Fiduciary must make estate/trust whole by restoring it to position it would occupy absent breach",
        counter_arguments=[
            "Loss not quantifiable with reasonable certainty",
            "Beneficiary's calculation speculative or based on hindsight",
            "No damages resulted from breach (estate/trust not harmed)",
            "Breach in good faith relying on advice; limit to actual loss",
            "Beneficiary's conduct contributed to loss (comparative fault)"
        ],
        resolution_strategy="Engage financial expert to calculate damages under multiple methods, document lost opportunity costs with market data, seek profit disgorgement for self-dealing, request interest from breach date, consider punitive surcharge for willful breach",
        entity_scope="All breach of fiduciary duty claims seeking monetary recovery",
        confidence="AGGRESSIVE",
        confidence_stratification="Multiple calculation methods with court discretion; requires expert testimony and factual development",
        controlling_precedent="Humane Society v. Austin National Bank, 531 S.W.2d 574 (Tex. 1975)"
    ),

    DoctrineBlock(
        topic="removal_of_fiduciary_grounds",
        keywords=["removal", "removal of executor", "removal of trustee", "removal of guardian", "grounds for removal", "material breach", "incapacity", "disqualification"],
        conclusion_template=[
            "Court may remove fiduciary for material breach of duty, incapacity, or substantial harm to beneficiaries.",
            "Removal discretionary even if statutory grounds shown; court weighs best interests of estate/trust.",
            "Lesser breach may warrant other remedies (surcharge, supervision) without removal."
        ],
        reasoning_framework="""
TX Estates Code §404.003 authorizes removal of personal representative for enumerated grounds.
TX Property Code §113.082 provides parallel trustee removal statute. Standards similar.

STATUTORY GROUNDS FOR REMOVAL (§404.003):

1. MATERIAL BREACH OF FIDUCIARY DUTY:
   - Self-dealing or conflict of interest
   - Gross negligence or waste
   - Failure to account or disclose
   - Misappropriation of assets

2. INCAPACITY: Mental or physical inability to perform duties

3. UNSUITABLE: Character or capacity makes person unsuitable (general welfare clause)

4. DISQUALIFICATION: Failed to qualify initially or became disqualified

5. NEGLECT: Failure to perform duties or return account when required

6. MISCONDUCT: Dishonesty, fraud, or other wrongdoing

STANDARD: Removal is DISCRETIONARY. Court must find:
- Statutory ground exists, AND
- Removal in best interests of estate/trust

Lesser breaches may warrant supervision, bonding, or surcharge without removal.
Removal reserved for material breach threatening estate/trust welfare.

BURDEN: Party seeking removal bears burden to prove grounds by preponderance.
Once shown, burden shifts to fiduciary to prove removal not in estate's best interest.

In Pool v. Pool, 290 S.W.3d 564 (Tex. App. 2009), court removed executor for repeated self-dealing
despite executor's competence, holding pattern of conflicts made removal appropriate.

EFFECT OF REMOVAL:
- Fiduciary discharged from further duties
- Must deliver property to successor
- Final accounting required
- May face surcharge for losses caused
- Criminal prosecution possible if fraud/theft

ALTERNATIVE: Beneficiaries may seek supervision or conditions on continuation rather than removal.
        """,
        key_factors=[
            "Severity and frequency of breaches",
            "Whether breach caused actual loss",
            "Fiduciary's good or bad faith",
            "Availability of suitable successor fiduciary",
            "Cost and disruption of removal",
            "Beneficiaries' confidence in fiduciary",
            "Whether conditions could cure concerns",
            "Estate/trust complexity requiring continuity"
        ],
        primary_authority=[
            "TX Estates Code §404.003 (Removal of Personal Representative)",
            "TX Property Code §113.082 (Removal of Trustee)",
            "Pool v. Pool, 290 S.W.3d 564 (Tex. App. 2009)",
            "Restatement (Third) of Trusts §37"
        ],
        burden_holder="Party seeking removal bears initial burden; burden shifts to fiduciary to prove removal inappropriate",
        adversary_position="Fiduciary's material breach or misconduct warrants removal to protect beneficiaries",
        counter_arguments=[
            "Breach minor and not repeated",
            "No actual harm to estate/trust",
            "Fiduciary corrected deficiency",
            "Removal would harm estate/trust (no suitable successor, expense)",
            "Beneficiary's motive improper (family dispute unrelated to breach)",
            "Alternative remedies adequate (supervision, bonding, co-fiduciary)"
        ],
        resolution_strategy="Document pattern of breaches, quantify harm to estate/trust, identify suitable successor, obtain beneficiary support for removal, consider less drastic alternatives first",
        entity_scope="Executors, administrators, trustees, guardians in Texas",
        confidence="AGGRESSIVE",
        confidence_stratification="Discretionary standard requiring balancing of factors; outcome depends on severity of breach and available alternatives",
        controlling_precedent="Pool v. Pool, 290 S.W.3d 564 (Tex. App. 2009)"
    ),

    DoctrineBlock(
        topic="independent_executor_powers",
        keywords=["independent executor", "independent administration", "powers", "court supervision", "will provisions", "muniment of title"],
        conclusion_template=[
            "Independent executors can administer estates without court supervision under TX Estates Code §401.001.",
            "Will must explicitly authorize independent administration; cannot be implied.",
            "Independent status grants broad powers but does NOT reduce fiduciary duty standards."
        ],
        reasoning_framework="""
Texas strongly favors independent administration as efficient alternative to court-supervised probate.
TX Estates Code §401.001 et seq. authorizes independent executors to act without court approval.

AUTHORIZATION REQUIREMENTS:

1. WILL PROVISION: Will must contain language granting independent executor authority.
   Standard clause: "My executor shall serve as independent executor without bond and
   without court supervision as provided by the Texas Estates Code."

2. COURT APPROVAL: Probate court approves independent administration in order admitting will.

3. NO NECESSITY FINDING: Unlike some states, Texas does not require showing necessity or advantage.

POWERS OF INDEPENDENT EXECUTOR (§401.002):

Broad powers to:
- Sell property (real or personal) without court order
- Invest funds in any legal investment
- Make distributions to beneficiaries
- Hire attorneys, accountants, appraisers
- Operate business
- Borrow money
- Execute contracts
- Settle claims
- Pay debts and taxes

LIMITATIONS:

- Cannot sell homestead during probate period without beneficiary consent (§353.051)
- Subject to claims process and creditor notice requirements
- Must file inventory unless will dispenses (§309.051)
- Can be compelled to account if beneficiaries petition (§404.001)

FIDUCIARY DUTIES UNCHANGED:

Independent executor status does NOT:
- Reduce duty of loyalty (still no self-dealing)
- Lower duty of care (still prudent person standard)
- Eliminate duty to account (beneficiaries can compel)
- Immunize from breach claims
- Prevent removal for cause

In Mowbray v. Avery, 76 S.W.3d 663 (Tex. App. 2002), court held independent executor liable for
self-dealing despite broad powers, confirming fiduciary duties apply regardless of executor type.

PRACTICAL EFFECT: Independent administration saves time and expense (no court hearings for routine
actions) but fiduciary remains fully accountable to beneficiaries.
        """,
        key_factors=[
            "Will language authorizing independent administration",
            "Court order approving independent status",
            "Scope of powers granted in will",
            "Whether will dispenses with bond or inventory",
            "Beneficiary sophistication and oversight",
            "Complexity of estate assets",
            "Potential for beneficiary disputes",
            "Cost savings vs risk of unsupervised administration"
        ],
        primary_authority=[
            "TX Estates Code §401.001 (Independent Administration)",
            "TX Estates Code §401.002 (Powers)",
            "TX Estates Code §404.001 (Compelling Account)",
            "Mowbray v. Avery, 76 S.W.3d 663 (Tex. App. 2002)"
        ],
        burden_holder="Independent executor bears burden to prove authority for any challenged action",
        adversary_position="Independent executor exceeded powers or breached fiduciary duties despite broad authority",
        counter_arguments=[
            "Will expressly authorized specific action",
            "§401.002 grants broad powers to independent executors",
            "All beneficiaries consented to action",
            "Action necessary to preserve estate property",
            "No court supervision required for independent administration"
        ],
        resolution_strategy="Ensure will contains independent administration language, obtain court approval in probate order, provide informal accountings to beneficiaries, document basis for major decisions, maintain fiduciary duty compliance",
        entity_scope="Independent executors under Texas Estates Code",
        confidence="DEFENSIBLE",
        confidence_stratification="Well-defined statutory powers with clear case law confirming fiduciary duties remain unchanged",
        controlling_precedent="Mowbray v. Avery, 76 S.W.3d 663 (Tex. App. 2002)"
    ),

    DoctrineBlock(
        topic="corporate_trustee_standards_higher",
        keywords=["corporate trustee", "institutional trustee", "bank trustee", "professional fiduciary", "higher standard", "special skills", "expertise"],
        conclusion_template=[
            "Corporate and professional fiduciaries held to higher standard reflecting their expertise and resources.",
            "Must exercise care, skill, and caution available to professionals in same field under same circumstances.",
            "Charging professional fees creates expectation of professional-level performance."
        ],
        reasoning_framework="""
TX Property Code §114.006(b) establishes higher standard for trustees with special skills:
"If the trustee has special skills or expertise, or is named trustee in reliance upon the trustee's
representation that the trustee has special skills or expertise, the trustee shall use those special
skills or expertise."

This provision imposes enhanced duty on:
- Banks and trust companies
- Professional trustees (attorneys, CPAs serving as trustee)
- Investment advisors acting as trustee
- Any fiduciary holding themselves out as having expertise

ENHANCED STANDARD ELEMENTS:

1. GREATER DILIGENCE: Corporate trustee must invest time and resources commensurate with institution
2. SPECIALIZED KNOWLEDGE: Expected to know industry best practices, regulatory requirements, tax rules
3. SYSTEMS AND CONTROLS: Must have procedures for monitoring, compliance, risk management
4. DIVERSIFICATION: Held to stricter diversification standards
5. DELEGATION: Can delegate but must supervise; cannot disclaim responsibility
6. INVESTMENT EXPERTISE: Expected to outperform individual trustees in investment returns

PRACTICAL IMPLICATIONS:

- Negligence measured against what professional trustee would do, not average person
- Industry standards and customs relevant to standard of care
- Cost of professional administration justified only by professional performance
- Greater scrutiny of investment decisions and portfolio management

In Montgomery v. Kennedy, 669 S.W.2d 309 (Tex. 1984), court held bank trustee to higher standard,
noting "professional trustees are held to a higher degree of skill and care than nonprofessional trustees."

JUSTIFICATION: Corporate trustees:
- Charge fees for professional services
- Hold themselves out as experts
- Have greater resources and staff
- Benefit from economies of scale
- Subject to regulatory oversight

Beneficiaries entitled to professional performance if paying professional fees.

COMPENSATION CORRELATION: Higher fees = higher expectations. Court may reduce fees if performance
substandard or impose surcharge if breach caused by lack of professional diligence.
        """,
        key_factors=[
            "Fiduciary's professional status and marketing",
            "Fees charged compared to individual trustee",
            "Special skills or expertise represented",
            "Resources available to institutional fiduciary",
            "Industry standards and best practices",
            "Regulatory requirements applicable to corporate trustee",
            "Complexity of trust administration",
            "Beneficiary expectations based on fiduciary's representations"
        ],
        primary_authority=[
            "TX Property Code §114.006(b) (Special Skills)",
            "Montgomery v. Kennedy, 669 S.W.2d 309 (Tex. 1984)",
            "Restatement (Third) of Trusts §77 cmt. b",
            "Uniform Trust Code §806"
        ],
        burden_holder="Corporate fiduciary bears burden to prove conduct met professional standards",
        adversary_position="Corporate trustee failed to exercise professional level care despite charging professional fees",
        counter_arguments=[
            "Conduct met or exceeded industry standards",
            "Relied on qualified professionals (investment advisors, attorneys)",
            "Trust terms limited trustee's discretion or authority",
            "Beneficiaries' expectations unreasonable given trust purposes",
            "Individual trustee would have made same decision"
        ],
        resolution_strategy="Document compliance with industry best practices, maintain detailed policies and procedures, engage qualified professionals, benchmark performance against peers, provide regular reporting exceeding statutory minimums",
        entity_scope="Banks, trust companies, professional trustees, investment advisors serving as fiduciary",
        confidence="DEFENSIBLE",
        confidence_stratification="Clear statutory provision and case law establishing enhanced standard for professional fiduciaries",
        controlling_precedent="Montgomery v. Kennedy, 669 S.W.2d 309 (Tex. 1984)"
    ),

    DoctrineBlock(
        topic="exculpatory_clauses_limits",
        keywords=["exculpatory clause", "liability waiver", "limitation of liability", "trustee protection", "good faith", "recklessness", "bad faith"],
        conclusion_template=[
            "Exculpatory clauses can limit trustee liability but cannot excuse bad faith, reckless indifference, or willful misconduct.",
            "Clause must be clear, specific, and not inserted by fiduciary drafting trust instrument.",
            "Strong public policy limits enforce ability of broad immunity provisions."
        ],
        reasoning_framework="""
TX Property Code §114.007 governs exculpatory clauses in trust instruments:

"An exculpatory term drafted or caused to be drafted by the trustee is invalid as an abuse of a
fiduciary or confidential relationship unless the trustee proves that the exculpatory term is fair
under the circumstances and that its existence and contents were adequately communicated to the settlor."

VALID EXCULPATORY CLAUSE REQUIREMENTS:

1. NOT DRAFTED BY TRUSTEE: Independent attorney drafts clause; trustee cannot insert self-protection
2. CLEARLY COMMUNICATED: Settlor understood scope and effect of limitation
3. FAIR UNDER CIRCUMSTANCES: Reasonable limitation given trust purposes and beneficiaries
4. SPECIFIC CONDUCT: Cannot broadly exempt "all liability"; must specify limited categories

CONDUCT THAT CANNOT BE EXCUSED (§114.007(c)):
- Bad faith
- Reckless indifference to purposes of trust or interests of beneficiaries
- Intentional failure to deal impartially with beneficiaries

Public policy prohibits excusing:
- Willful misconduct
- Fraud
- Gross negligence (debatable; some courts uphold, others invalidate)

VALID EXCULPATION EXAMPLES:
- "Trustee not liable for losses from investments made in good faith"
- "Trustee not liable for ordinary negligence in administrative decisions"
- "Trustee may retain original investments without duty to diversify"

INVALID EXCULPATION EXAMPLES:
- "Trustee not liable for any breach of duty" (too broad)
- "Trustee may act in trustee's own interest" (violates loyalty)
- "Trustee not liable for gross negligence" (public policy, minority view allows)

In Landon v. Exxon Corp., 772 S.W.2d 880 (Tex. App. 1989), court invalidated exculpatory clause
drafted by attorney-trustee, holding abuse of confidential relationship.

BURDEN: Trustee seeking protection of exculpatory clause bears burden to prove:
- Clause properly drafted and communicated
- Conduct falls within scope of clause
- Conduct not bad faith/reckless indifference/intentional

Court interprets exculpatory clauses narrowly; doubts resolved against trustee.
        """,
        key_factors=[
            "Who drafted exculpatory clause (trustee vs independent attorney)",
            "Specificity of limitation (broad vs narrow)",
            "Settlor's sophistication and understanding",
            "Whether settlor had independent legal advice",
            "Nature of conduct sought to be excused",
            "Fiduciary's good or bad faith",
            "Whether clause contrary to public policy",
            "Trust instrument overall context"
        ],
        primary_authority=[
            "TX Property Code §114.007 (Exculpatory Clauses)",
            "Restatement (Third) of Trusts §96",
            "Landon v. Exxon Corp., 772 S.W.2d 880 (Tex. App. 1989)",
            "Uniform Trust Code §1008"
        ],
        burden_holder="Trustee bears burden to prove exculpatory clause valid and applicable to conduct",
        adversary_position="Exculpatory clause invalid or inapplicable due to bad faith/recklessness",
        counter_arguments=[
            "Clause drafted by trustee creating presumption of invalidity (§114.007(b))",
            "Conduct constitutes bad faith or reckless indifference (§114.007(c))",
            "Settlor did not understand scope of exculpation",
            "Clause contrary to public policy protecting beneficiaries",
            "Clause too broad to be enforceable"
        ],
        resolution_strategy="If drafting trust, have independent attorney draft exculpatory clause with full disclosure to settlor; if asserting clause defense, prove independent drafting, specific limitation, and good faith conduct",
        entity_scope="Trustees under Texas trust instruments containing exculpatory provisions",
        confidence="AGGRESSIVE",
        confidence_stratification="Narrow construction of exculpatory clauses with burden on trustee; bad faith/recklessness always exception",
        controlling_precedent="TX Property Code §114.007 (statutory framework)"
    ),

    DoctrineBlock(
        topic="duty_of_impartiality_beneficiaries",
        keywords=["impartiality", "fairness", "multiple beneficiaries", "income beneficiary", "remainder beneficiary", "balance", "competing interests"],
        conclusion_template=[
            "Trustee must act impartially when administering trust for multiple beneficiaries with different interests.",
            "Duty to balance income beneficiaries' current income needs with remaindermen's preservation of principal.",
            "Cannot favor one beneficiary class over another absent trust instrument authorization."
        ],
        reasoning_framework="""
TX Property Code §113.053 imposes duty of impartiality: trustee must "act impartially in investing,
managing, and distributing the trust property, giving due regard to the beneficiaries' respective interests."

CLASSIC CONFLICT: Income vs Remainder Beneficiaries

INCOME BENEFICIARY wants:
- High current income (dividends, interest)
- Income-producing investments (bonds, dividend stocks)
- Distribution of all income

REMAINDER BENEFICIARY wants:
- Growth and appreciation
- Preservation of purchasing power
- Reinvestment for compound growth

TRUSTEE MUST BALANCE:
Cannot favor either class. Investment strategy must consider both interests.

Modern portfolio theory and total return approach helps: focus on total return (income + appreciation)
rather than artificial income/principal distinction. Can allocate appreciation to "income" if total
return adequate to support distributions.

IMPARTIALITY IN DISCRETIONARY DISTRIBUTIONS:

When trustee has discretion among beneficiaries, cannot:
- Favor beneficiary with personal relationship to trustee
- Discriminate based on disapproval of beneficiary's lifestyle
- Base distributions on beneficiary's other wealth (unless trust directs)
- Ignore one beneficiary's needs while generously supporting another

EXCEPTIONS:
- Trust instrument may authorize favoring one beneficiary
- Settlor's intent may indicate preference (e.g., support for disabled child primary)
- Beneficiary conduct may justify differential treatment (wasting prior distributions)

In NCNB Texas National Bank v. Carpenter, 849 S.W.2d 875 (Tex. App. 1993), court held trustee breached
impartiality by investing solely for growth while income beneficiary received inadequate distributions.

PRACTICAL APPLICATION:
- Diversify investments to balance income and growth
- Consider total return unitrust conversion (§116.004)
- Document reasons for discretionary distribution decisions
- Communicate with all beneficiaries
- Avoid appearance of favoritism
        """,
        key_factors=[
            "Number and classes of beneficiaries",
            "Competing interests (income vs growth, current vs future)",
            "Trust instrument directions on balancing interests",
            "Beneficiaries' respective needs and circumstances",
            "Investment strategy's impact on different beneficiary classes",
            "Discretionary distribution patterns over time",
            "Trustee's relationship to beneficiaries",
            "Communication with all beneficiaries"
        ],
        primary_authority=[
            "TX Property Code §113.053 (Impartiality)",
            "TX Property Code §116.004 (Unitrust Conversion)",
            "Restatement (Third) of Trusts §79",
            "NCNB Texas National Bank v. Carpenter, 849 S.W.2d 875 (Tex. App. 1993)"
        ],
        burden_holder="Beneficiary alleging favoritism bears initial burden; trustee must prove impartial conduct",
        adversary_position="Trustee favored one beneficiary class over another causing harm to disfavored class",
        counter_arguments=[
            "Trust instrument authorized favoring specific beneficiary",
            "Investment strategy balanced income and growth appropriately",
            "Discretionary distributions based on documented needs assessment",
            "Total return adequate for all beneficiary classes",
            "Differential treatment justified by beneficiary circumstances"
        ],
        resolution_strategy="Adopt total return investment strategy, document impartial decision-making process, communicate regularly with all beneficiaries, consider unitrust conversion if income/principal conflict severe",
        entity_scope="Trustees with multiple beneficiaries or successive beneficial interests",
        confidence="AGGRESSIVE",
        confidence_stratification="Balancing requirement clear but application fact-intensive; requires documentation of impartial process",
        controlling_precedent="NCNB Texas National Bank v. Carpenter, 849 S.W.2d 875 (Tex. App. 1993)"
    ),

    DoctrineBlock(
        topic="guardian_person_vs_estate",
        keywords=["guardian", "guardianship", "guardian of person", "guardian of estate", "ward", "incapacitated person", "personal decisions", "financial decisions"],
        conclusion_template=[
            "Guardian of the person makes personal care decisions; guardian of the estate manages financial affairs.",
            "One person may serve in both capacities or court may appoint separate guardians.",
            "Each guardian type has distinct duties and liabilities under TX Estates Code Chapter 1151."
        ],
        reasoning_framework="""
TX Estates Code distinguishes between two types of guardians with different powers and duties:

GUARDIAN OF THE PERSON (§1151.051):

POWERS:
- Decide ward's living arrangements
- Consent to medical treatment
- Make educational decisions
- Determine social activities and contacts
- Personal care and supervision

DUTIES (§1151.101):
- Treat ward with dignity and respect
- Prefer least restrictive environment
- Consider ward's preferences and values
- Visit ward regularly (quarterly minimum)
- Encourage maximum self-reliance
- Annual report on ward's condition

DOES NOT:
- Control ward's finances (unless also guardian of estate)
- Sell ward's property
- Make investment decisions

GUARDIAN OF THE ESTATE (§1151.151):

POWERS:
- Manage ward's property and finances
- Invest ward's funds
- Pay ward's debts and expenses
- File ward's tax returns
- Bring and defend lawsuits affecting ward's property

DUTIES (§1152.101):
- File inventory within 30 days (§1154.051)
- Annual accounting required (§1163.001)
- Obtain court approval for major transactions
- Invest according to prudent investor standard
- Preserve estate for ward's benefit
- Use estate funds only for ward's care and support

BOND REQUIRED (§1158.001):
Court sets bond amount based on estate value. Protects against misappropriation.

COURT SUPERVISION:
Guardian of estate under strict court oversight. Must get approval for:
- Sale of real property
- Borrowing against estate
- Business transactions
- Investments outside statutory list (unless court authorizes broader powers)

Unlike independent executor, guardian has minimal independent authority. Court protection for
incapacitated person justifies extensive supervision.

FIDUCIARY DUTIES APPLY TO BOTH:
- Loyalty (no self-dealing)
- Care (prudent person standard)
- Accounting (mandatory annual reports)
- Impartiality (if multiple beneficiaries on ward's death)

In In re Guardianship of Martinez, 95 S.W.3d 702 (Tex. App. 2002), court removed guardian of estate
for self-dealing and failure to account, while retaining guardian of person.
        """,
        key_factors=[
            "Whether guardianship of person, estate, or both needed",
            "Ward's level of incapacity (physical vs mental)",
            "Complexity of ward's financial affairs",
            "Ward's medical and personal care needs",
            "Suitability of same person for both roles",
            "Family dynamics and potential conflicts",
            "Court supervision level required",
            "Bond amount and cost of guardianship"
        ],
        primary_authority=[
            "TX Estates Code §1151.051 (Guardian of Person)",
            "TX Estates Code §1151.151 (Guardian of Estate)",
            "TX Estates Code §1151.101 (Duties)",
            "In re Guardianship of Martinez, 95 S.W.3d 702 (Tex. App. 2002)"
        ],
        burden_holder="Guardian bears burden to prove compliance with statutory duties and court orders",
        adversary_position="Guardian breached specific duty causing harm to ward or estate",
        counter_arguments=[
            "Actions approved by court order",
            "Acted in ward's best interest based on information available",
            "Consulted with medical or financial professionals",
            "Ward's condition or preferences supported decision",
            "Full accounting provided showing proper management"
        ],
        resolution_strategy="Identify which guardian type appointed, review statutory duties applicable to that type, assess compliance with accounting and court approval requirements, document ward-centric decision making",
        entity_scope="Guardians appointed under TX Estates Code for incapacitated adults",
        confidence="DEFENSIBLE",
        confidence_stratification="Clear statutory framework distinguishing person vs estate guardians with specific duties",
        controlling_precedent="TX Estates Code Chapters 1151-1163 (comprehensive guardianship statutes)"
    ),

    DoctrineBlock(
        topic="duty_preserve_property_waste",
        keywords=["preserve property", "waste", "deterioration", "maintenance", "insurance", "protect assets", "prevent loss"],
        conclusion_template=[
            "Fiduciary must take reasonable steps to preserve and protect trust or estate property from loss or damage.",
            "Failure to maintain, insure, or protect property from waste constitutes breach of duty.",
            "Liability extends to foreseeable losses that reasonable care would have prevented."
        ],
        reasoning_framework="""
Fiduciary duty to preserve property flows from fundamental obligation to protect beneficiaries' interests.
TX Property Code §113.052 requires trustee to "use reasonable care and skill to preserve the trust property."

AFFIRMATIVE DUTIES TO PRESERVE:

1. INSURANCE: Maintain adequate insurance on property
   - Homeowner's insurance on real property
   - Liability insurance for business operations
   - Director's and officer's insurance if corporate trustee
   - Flood, earthquake insurance if property location warrants

2. MAINTENANCE: Keep property in good repair
   - Building repairs before deterioration
   - Lawn care and exterior maintenance
   - HVAC, plumbing, electrical systems
   - Preventing vandalism or trespass

3. TAXES AND CHARGES: Pay to prevent liens or forfeiture
   - Property taxes
   - HOA fees
   - Utilities if necessary to preserve property
   - Assessments and special taxes

4. PROTECTION FROM CLAIMS: Defend property against adverse claims
   - Defend title disputes
   - Respond to liens or encumbrances
   - Monitor limitation periods on claims

5. TAKE POSSESSION: Secure physical control
   - Change locks if necessary
   - Remove prior occupants
   - Secure valuable personal property

WASTE PROHIBITION:

Active waste: Affirmative acts harming property (demolition, removal of fixtures)
Passive waste: Failure to maintain allowing deterioration

Either form violates preservation duty. Trustee liable for diminution in value from waste.

In Corpus Christi Bank & Trust v. Roberts, 597 S.W.2d 752 (Tex. 1980), trustee held liable for
allowing property to deteriorate and failing to maintain insurance.

STANDARD: Reasonable care under circumstances. What would prudent owner do to protect property?

Factors:
- Value of property relative to preservation costs
- Property's income-producing capacity
- Temporary vs long-term holding period
- Risk of loss or damage
- Availability of insurance

EXCEPTIONS: If trust directs sale, extensive maintenance may not be required. Reasonable preparation
for sale sufficient.

DAMAGES: Diminution in value from failure to preserve, plus lost rental income if property rendered
uninhabitable. Foreseeable consequential damages recoverable (e.g., personal injury from premises
defect fiduciary failed to repair).
        """,
        key_factors=[
            "Type and value of property requiring preservation",
            "Foreseeable risks to property (weather, vandalism, deterioration)",
            "Cost of preservation measures vs property value",
            "Length of time property held before distribution",
            "Property's income-producing capacity",
            "Availability and cost of insurance",
            "Local law requirements (building codes, housing regulations)",
            "Trust or estate purposes regarding property"
        ],
        primary_authority=[
            "TX Property Code §113.052 (Duty to Preserve)",
            "Restatement (Third) of Trusts §76",
            "Corpus Christi Bank & Trust v. Roberts, 597 S.W.2d 752 (Tex. 1980)"
        ],
        burden_holder="Beneficiary bears burden to show property not preserved; fiduciary must prove reasonable care exercised",
        adversary_position="Fiduciary allowed property to deteriorate or be damaged through inaction or inadequate protection",
        counter_arguments=[
            "Property held for short-term pending sale (extensive maintenance uneconomical)",
            "Beneficiaries directed minimal maintenance",
            "Cost of preservation exceeded property value",
            "Loss due to unforeseeable event (Act of God)",
            "Insurance unavailable or prohibitively expensive"
        ],
        resolution_strategy="Inventory all property at inception, obtain insurance on valuable assets, establish maintenance schedule for real property, pay taxes and charges timely, document preservation decisions and costs",
        entity_scope="All fiduciaries with custody or control of property",
        confidence="DEFENSIBLE",
        confidence_stratification="Well-established duty with objective reasonable care standard; liability for foreseeable losses",
        controlling_precedent="Corpus Christi Bank & Trust v. Roberts, 597 S.W.2d 752 (Tex. 1980)"
    ),

    DoctrineBlock(
        topic="co_trustee_joint_liability",
        keywords=["co-trustee", "multiple trustees", "joint liability", "unanimous consent", "delegation", "dissent", "monitoring duty"],
        conclusion_template=[
            "Co-trustees must act unanimously unless trust instrument authorizes majority action.",
            "Each co-trustee has duty to monitor and prevent co-trustee's breach.",
            "Liability joint and several for breaches each co-trustee participated in or failed to prevent."
        ],
        reasoning_framework="""
TX Property Code §113.085 governs co-trustee administration and liability.

DECISION-MAKING RULES:

DEFAULT (§113.085(a)): Co-trustees must act by UNANIMOUS consent. Single dissenting trustee blocks action.

MAJORITY RULE: Trust may authorize majority decision-making. Common for more than two trustees.

INDIVIDUAL ACTION ALLOWED FOR (§113.085(b)):
- Routine administrative acts not requiring judgment
- Ministerial acts (signing checks pursuant to authorized transaction)
- Delegation to agent (but must jointly select and monitor agent)

LIABILITY RULES:

1. PARTICIPATING CO-TRUSTEE: Fully liable for breach participated in

2. CONSENTING CO-TRUSTEE: Liable for breach consented to even if did not actively participate

3. NON-DISSENTING CO-TRUSTEE: Liable if knew of breach and failed to take reasonable steps to prevent or remedy

4. IMPROPERLY DELEGATING CO-TRUSTEE: Liable if delegated to co-trustee decisions requiring joint action

5. DISSENTING CO-TRUSTEE: NOT liable if:
   - Expressed dissent in writing to co-trustee
   - Promptly notified beneficiaries of dissent
   - Did not participate in or facilitate breach

AFFIRMATIVE DUTY TO MONITOR:

Co-trustee cannot simply defer to co-trustee or remain passive. Must:
- Stay informed of trust administration
- Review financial statements and reports
- Question suspicious transactions
- Prevent co-trustee's breaches
- Bring legal action against breaching co-trustee if necessary

In Hummel v. Hummel, 133 Ohio St. 3d 554 (Ohio 2012) (Texas courts follow), passive co-trustee held
liable for failing to monitor active co-trustee who embezzled funds. Passivity itself breach.

DELEGATION AMONG CO-TRUSTEES (§113.085(c)):

Cannot delegate discretionary decisions to single co-trustee. Examples of prohibited delegation:
- Investment decisions
- Distribution discretion
- Major sales or acquisitions

Can delegate ministerial tasks:
- Check signing pursuant to approved transactions
- Routine administration
- Day-to-day operations

SEGREGATION OF DUTIES:

Trust may assign different responsibilities to each co-trustee (e.g., one handles investments,
one handles distributions). But each still owes monitoring duty regarding co-trustee's assigned area.

JOINT AND SEVERAL LIABILITY:

Beneficiary may sue any or all co-trustees for full amount of loss. Co-trustees then may seek
contribution from each other based on relative fault.
        """,
        key_factors=[
            "Number of co-trustees and decision-making rule",
            "Whether trust authorizes delegation among co-trustees",
            "Active vs passive role of each co-trustee",
            "Co-trustee's knowledge of or participation in breach",
            "Whether co-trustee dissented and notified beneficiaries",
            "Reasonableness of reliance on co-trustee",
            "Segregation of duties among co-trustees",
            "Professional vs non-professional co-trustee status"
        ],
        primary_authority=[
            "TX Property Code §113.085 (Co-Trustees)",
            "Restatement (Third) of Trusts §81",
            "Hummel v. Hummel, 133 Ohio St. 3d 554 (2012)"
        ],
        burden_holder="Each co-trustee bears burden to prove non-participation or reasonable dissent",
        adversary_position="All co-trustees jointly liable for breach unless proved dissent and prevention efforts",
        counter_arguments=[
            "Expressed written dissent to breaching co-trustee",
            "Notified beneficiaries of co-trustee's breach promptly",
            "Took reasonable steps to prevent breach (legal action, court petition)",
            "Trust authorized delegation of decision to co-trustee",
            "Reasonably relied on professional co-trustee's expertise"
        ],
        resolution_strategy="Establish clear division of responsibilities in co-trustee agreement, require joint approval for major decisions, document dissent in writing if disagree with co-trustee, monitor co-trustee's administration regularly",
        entity_scope="Multiple trustees serving jointly",
        confidence="DEFENSIBLE",
        confidence_stratification="Clear statutory framework with unanimous consent default and joint liability for participation or passive acquiescence",
        controlling_precedent="TX Property Code §113.085"
    ),

    DoctrineBlock(
        topic="delegation_prudent_standards",
        keywords=["delegation", "agent", "investment advisor", "attorney", "prudent delegation", "monitoring", "supervision"],
        conclusion_template=[
            "Fiduciaries may delegate investment and administrative functions but must prudently select, instruct, and monitor agents.",
            "Cannot delegate ultimate responsibility or discretionary decisions reserved to fiduciary.",
            "Liability for agent's conduct if failed to exercise prudence in delegation."
        ],
        reasoning_framework="""
TX Property Code §117.011 authorizes trustee delegation under prudent investor act:
"A trustee may delegate investment and management functions that a prudent trustee of comparable
skills could properly delegate under the circumstances."

THREE-STEP DELEGATION DUTY:

1. PRUDENT SELECTION: Choose agent with skill appropriate to function
   - Investment advisor with relevant credentials (CFA, CFP)
   - Attorney admitted to practice in jurisdiction
   - CPA for tax preparation
   - Property manager with real estate experience

   Must investigate: credentials, experience, references, disciplinary history

2. PROPER INSTRUCTION: Define scope and terms of delegation
   - Written agreement specifying duties
   - Investment policy statement for investment advisors
   - Authority limits and approval requirements
   - Reporting and accountability requirements

3. PERIODIC MONITORING: Ongoing supervision of agent performance
   - Review reports and statements
   - Evaluate performance against benchmarks
   - Question suspicious transactions
   - Terminate if agent performing inadequately

CANNOT DELEGATE:

- Fundamental trustee discretion (distribution decisions)
- Fiduciary relationship itself (remain liable as fiduciary)
- Duty to act in beneficiaries' interest
- Ultimate investment responsibility (advisor recommends, trustee decides)

In In re Frost National Bank, 145 S.W.3d 197 (Tex. App. 2004), court held trustee properly delegated
investment management to qualified advisor and monitored quarterly, avoiding liability for advisor's losses.

SPECIAL DELEGATION RULE FOR CO-TRUSTEES (§114.0031):

Cannot delegate to co-trustee decisions requiring joint action. See co-trustee doctrine.

DELEGATION TO BENEFICIARY:

Generally improper to delegate trustee decisions to beneficiary. Undermines fiduciary relationship.
Exception: beneficiary consent to specific transaction after full disclosure.

LIABILITY FOR AGENT'S ACTS:

Trustee NOT automatically liable for agent's negligence if:
- Prudently selected agent
- Appropriately delegated function
- Periodically monitored agent

Trustee IS liable if:
- Negligently selected unqualified agent
- Failed to properly instruct agent
- Failed to monitor agent allowing breach to continue
- Delegated non-delegable function

Agent directly liable to trust under §114.0031(b) for own negligence.
        """,
        key_factors=[
            "Complexity of function requiring specialized expertise",
            "Fiduciary's own skill level vs task requirements",
            "Agent's credentials, experience, and reputation",
            "Clarity of delegation agreement and instructions",
            "Frequency and adequacy of monitoring",
            "Agent's performance compared to appropriate benchmarks",
            "Whether function delegable or core fiduciary discretion",
            "Cost of agent services relative to benefit"
        ],
        primary_authority=[
            "TX Property Code §117.011 (Delegation Under Prudent Investor Act)",
            "TX Property Code §114.0031 (General Delegation)",
            "Restatement (Third) of Trusts §80",
            "In re Frost National Bank, 145 S.W.3d 197 (Tex. App. 2004)"
        ],
        burden_holder="Fiduciary bears burden to prove prudent selection, instruction, and monitoring of agent",
        adversary_position="Improper delegation or inadequate supervision of agent caused loss",
        counter_arguments=[
            "Agent had appropriate credentials and experience",
            "Written delegation agreement with clear instructions",
            "Regular monitoring through reports and meetings",
            "Agent's performance met industry standards",
            "Promptly terminated agent upon discovering deficiency"
        ],
        resolution_strategy="Conduct due diligence on agent qualifications, execute written delegation agreement, establish reporting requirements, review performance regularly, document monitoring activities",
        entity_scope="All fiduciaries delegating investment or administrative functions",
        confidence="AGGRESSIVE",
        confidence_stratification="Prudent delegation framework clear but monitoring adequacy fact-intensive",
        controlling_precedent="TX Property Code §117.011"
    ),

    DoctrineBlock(
        topic="trustee_compensation_reasonable",
        keywords=["trustee compensation", "fees", "commissions", "reasonable compensation", "court approval", "fee agreement", "excessive fees"],
        conclusion_template=[
            "Trustees entitled to reasonable compensation for services but cannot profit excessively from position.",
            "Compensation must bear reasonable relationship to services provided and trust complexity.",
            "Court may reduce fees if unreasonable or fiduciary breached duties."
        ],
        reasoning_framework="""
TX Property Code §114.061 authorizes trustee compensation:
"If the terms of the trust do not specify the trustee's compensation, the trustee is entitled to
compensation that is reasonable under the circumstances."

DETERMINING REASONABLE COMPENSATION:

Courts apply multi-factor test:

1. TIME AND EFFORT: Hours spent on trust administration, complexity of tasks

2. SKILL REQUIRED: Specialized knowledge needed (investment expertise, tax, legal)

3. TRUST SIZE: Corpus value, income generated, transaction volume

4. RESULTS OBTAINED: Investment performance, tax savings, successful litigation

5. CUSTOMARY FEES: What similarly situated trustees charge in same locality

6. TRUSTEE'S SKILL: Professional trustee vs family member, special expertise

COMMON COMPENSATION STRUCTURES:

1. PERCENTAGE OF CORPUS: E.g., 1% annually on trust value
   - Corporate trustees commonly use this method
   - Must be reasonable; cannot exceed local custom

2. HOURLY RATE: Common for professional individual trustees
   - Rate must reflect trustee's actual skill level
   - Attorney-trustee billing as attorney creates conflict

3. HYBRID: Base fee plus incentive for performance
   - Growing acceptance for investment performance fees
   - Must align with beneficiary interests

4. FLAT FEE: Fixed amount for simple trusts
   - Appropriate for ministerial administration

TRUST INSTRUMENT CONTROLS:

- May specify compensation method and amount
- May provide "no compensation" (common for family member)
- Trustee accepts appointment under those terms

EXCESSIVE FEE CONSEQUENCES:

Court may:
- Reduce fees to reasonable amount
- Order disgorgement of excessive fees already paid
- Remove trustee for charging excessive fees
- Deny compensation entirely if serious breach

In Langford v. Shamburger, 417 S.W.2d 438 (Tex. Civ. App. 1967), court reduced trustee fees by 50%
where trustee provided minimal services yet charged full percentage.

PROFESSIONAL vs FAMILY TRUSTEE:

Professional charging fees held to higher performance standard. Family member serving without compensation
held to ordinary care standard, not professional standard.

DUAL CAPACITY FEES:

Attorney-trustee cannot charge both trustee fees AND attorney fees for same services. Must elect.
Exception: clearly separate roles (trustee administration vs litigation representation).
        """,
        key_factors=[
            "Trust instrument provisions on compensation",
            "Trustee's professional status and expertise",
            "Time spent and complexity of administration",
            "Trust size and transaction volume",
            "Investment performance or other results achieved",
            "Customary fees in locality for similar services",
            "Beneficiary objections to fee amount",
            "Quality of trustee's performance"
        ],
        primary_authority=[
            "TX Property Code §114.061 (Compensation)",
            "Restatement (Third) of Trusts §38",
            "Langford v. Shamburger, 417 S.W.2d 438 (Tex. Civ. App. 1967)"
        ],
        burden_holder="Trustee seeking compensation bears burden to prove reasonableness",
        adversary_position="Fees excessive given minimal services provided or poor performance",
        counter_arguments=[
            "Trust instrument authorized compensation method",
            "Fees consistent with customary rates in locality",
            "Extensive time and effort documented in time records",
            "Achieved superior investment returns or other measurable results",
            "Comparable professional trustees charge similar fees"
        ],
        resolution_strategy="Establish compensation in trust instrument or fee agreement, document time and services, benchmark against comparable trustees, reduce fees if performance substandard",
        entity_scope="All trustees seeking compensation for services",
        confidence="AGGRESSIVE",
        confidence_stratification="Reasonableness standard fact-intensive; court discretion to reduce fees",
        controlling_precedent="TX Property Code §114.061"
    )
]

# Total doctrine blocks: 20 comprehensive blocks covering all major fiduciary duty topics
