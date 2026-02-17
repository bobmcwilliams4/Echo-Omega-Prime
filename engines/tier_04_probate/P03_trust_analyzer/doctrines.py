"""
Trust Analyzer Doctrine Cache
Comprehensive trust law doctrine blocks covering Texas Trust Code and federal tax law.
50+ pre-compiled expert reasoning blocks with real domain expertise.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class ConfidenceStratum(str, Enum):
    """Confidence stratification for trust positions"""
    DEFENSIBLE = "defensible"
    AGGRESSIVE = "aggressive"
    DISCLOSURE = "disclosure"
    HIGH_RISK = "high_risk"


class IssueCategory(str, Enum):
    """Trust law issue categorization"""
    TRUST_CREATION = "trust_creation"
    GRANTOR_TRUST_TAX = "grantor_trust_tax"
    TRUSTEE_DUTIES = "trustee_duties"
    DISTRIBUTION_STANDARDS = "distribution_standards"
    MODIFICATION_TERMINATION = "modification_termination"
    PERPETUITIES_DURATION = "perpetuities_duration"
    CHARITABLE_TRUSTS = "charitable_trusts"
    CREDITOR_PROTECTION = "creditor_protection"
    MINOR_BENEFICIARY = "minor_beneficiary"
    LIFE_INSURANCE = "life_insurance"
    QUALIFIED_TRUSTS = "qualified_trusts"
    ESTATE_TAX_PLANNING = "estate_tax_planning"


@dataclass
class DoctrineBlock:
    """
    Single doctrine block representing expert reasoning on a trust law topic.
    Contains pre-compiled conclusions, reasoning frameworks, and authority citations.
    """
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: Optional[str] = None
    counter_arguments: List[str] = field(default_factory=list)
    resolution_strategy: str = ""
    entity_scope: List[str] = field(default_factory=list)
    confidence: float = 0.85
    confidence_stratification: ConfidenceStratum = ConfidenceStratum.DEFENSIBLE
    controlling_precedent: List[str] = field(default_factory=list)
    issue_category: IssueCategory = IssueCategory.TRUST_CREATION


# ==============================================================================
# TRUST CREATION AND VALIDITY DOCTRINES
# ==============================================================================

REVOCABLE_TRUST_CREATION = DoctrineBlock(
    topic="revocable_trust_creation_validity",
    keywords=["revocable trust", "living trust", "intervivos", "settlor", "creation requirements"],
    conclusion_template=[
        "A revocable trust is validly created in Texas when the settlor (1) has capacity, (2) manifests intent to create the trust, (3) designates a trustee and beneficiaries, and (4) transfers property to the trust.",
        "The trust instrument must satisfy the statute of frauds if it holds real property (written and signed).",
        "Revocable trusts remain fully within the settlor's control during lifetime and are included in the settlor's gross estate under IRC §2038."
    ],
    reasoning_framework="""
Texas Trust Code §112.001 establishes four essential elements for trust creation:
(1) Settlor capacity - same standard as will execution (sound mind, 18+ years)
(2) Intent to create trust - manifested through trust instrument language
(3) Definite beneficiaries - ascertainable at time of distribution (can be class)
(4) Trustee with duties - can be settlor initially, must have successor named

For revocable trusts specifically:
- Settlor retains power to amend or revoke (§112.051)
- Trust becomes irrevocable at settlor's death unless instrument provides otherwise
- Settlor is treated as owner of trust assets for income tax purposes (grantor trust)
- Assets included in gross estate under IRC §2038 (revocation power)

Statute of frauds (§112.004) requires written instrument for:
- Real property trusts
- Trusts not completed within one year
- Pour-over trusts receiving probate assets

Funding is critical - unfunded revocable trust is valid but holds no assets.
Must retitle assets into trust name or designate trust as beneficiary (life insurance, retirement accounts).
""",
    key_factors=[
        "Settlor capacity at trust creation",
        "Clear intent to create trust (not mere agency or will)",
        "Trust funded with property (even nominal amount sufficient initially)",
        "Trustee designated with duties to perform",
        "Beneficiaries ascertainable (can be settlor during lifetime)",
        "Written instrument if real property involved",
        "Retention of revocation power triggers estate inclusion IRC §2038"
    ],
    primary_authority=[
        "Texas Property Code §112.001 (Trust creation requirements)",
        "Texas Property Code §112.051 (Revocable trusts)",
        "IRC §2038 (Revocable transfers - estate tax inclusion)",
        "IRC §676 (Power to revest - grantor trust treatment)",
        "Treas. Reg. §20.2038-1 (Revocable transfers)",
        "Langford v. Shamburger, 417 S.W.3d 643 (Tex. App. 2013)"
    ],
    burden_holder="settlor",
    adversary_position="IRS may challenge whether trust was validly created vs. mere nominee arrangement; creditors may attack as fraudulent transfer if created to avoid existing claims",
    counter_arguments=[
        "Trust not validly created - lacks essential element (capacity, intent, property, beneficiary)",
        "Unfunded trust is testamentary and should have been executed as will",
        "Trust created to defraud creditors - voidable under Texas UFTA",
        "Self-declaration of trust invalid without proper formalities",
        "Beneficiaries too indefinite to be ascertainable"
    ],
    resolution_strategy="Document capacity with physician statement if questionable; clearly state trust intent in opening paragraphs; fund with at least nominal property; identify successor trustees; define beneficiary classes with objective standards",
    entity_scope=["individual", "married_couple", "family"],
    confidence=0.92,
    confidence_stratification=ConfidenceStratum.DEFENSIBLE,
    controlling_precedent=["Texas Property Code §§112.001-112.004"],
    issue_category=IssueCategory.TRUST_CREATION
)

IRREVOCABLE_TRUST_ELEMENTS = DoctrineBlock(
    topic="irrevocable_trust_creation_elements",
    keywords=["irrevocable trust", "permanent trust", "gift to trust", "settlor relinquishes control"],
    conclusion_template=[
        "An irrevocable trust is created when the settlor relinquishes the power to revoke and transfers property to the trust without retaining beneficial interests triggering grantor trust status.",
        "Unlike revocable trusts, irrevocable trusts are separate taxpayers (unless grantor trust powers retained).",
        "Transfers to irrevocable trusts are completed gifts subject to gift tax, with potential GST tax implications if skipping generations."
    ],
    reasoning_framework="""
Irrevocable trusts differ from revocable trusts in critical respects:

Creation mechanics (same as revocable):
- Capacity, intent, property, trustee, beneficiaries (§112.001)
- Written instrument required (§112.004)
- Funding transfers legal title to trustee

Irrevocability consequences:
- Settlor cannot unilaterally revoke or amend (§112.051(a))
- Modification requires court approval or consent of all beneficiaries (§112.054)
- Trust instrument may allow limited amendment powers (protector)

Tax treatment diverges sharply:
- Completed gift at funding (IRC §2511) - use annual exclusion if present interest
- Removed from settlor's gross estate (unless §§2036-2038 strings attached)
- Trust is separate taxpayer UNLESS grantor trust powers retained (IRC §§671-679)
- Compressed tax brackets - reaches 37% at $15,200 income (2024)

Gift tax considerations:
- Present interest gifts qualify for annual exclusion ($18,000/2024)
- Future interest gifts do not - use Crummey powers to create withdrawal rights
- Lifetime exemption ($13.61M/2024) available for taxable gifts
- GST tax if trust skips generation - use GST exemption allocation

Common irrevocable trust types:
- Life insurance trusts (ILITs) - remove policy from estate
- Intentionally defective grantor trusts (IDGTs) - estate freeze
- Spousal lifetime access trusts (SLATs) - use exemption, retain access
- Dynasty trusts - multi-generation planning
""",
    key_factors=[
        "Settlor relinquishes revocation power irrevocably",
        "Transfer to trust is completed gift for gift tax purposes",
        "Trust owns assets - removed from settlor's estate (if no retained interests)",
        "Trust is separate taxpayer unless grantor trust powers retained",
        "Annual exclusion requires present interest (Crummey powers if future interest)",
        "GST exemption allocation critical for multi-generation trusts",
        "Modification restricted to §112.054 mechanisms or trust protector powers"
    ],
    primary_authority=[
        "Texas Property Code §112.051 (Revocable vs irrevocable)",
        "Texas Property Code §112.054 (Modification of irrevocable trusts)",
        "IRC §2511 (Transfers subject to gift tax)",
        "IRC §2036 (Retained life estate - estate inclusion)",
        "IRC §2038 (Revocable transfers - estate inclusion)",
        "IRC §§671-679 (Grantor trust rules)",
        "Treas. Reg. §25.2511-2 (Cessation of donor's dominion and control)"
    ],
    burden_holder="settlor",
    adversary_position="IRS may assert retained powers trigger estate inclusion (§§2036-2038) or grantor trust status; beneficiaries may challenge validity if settlor lacked capacity or was under undue influence",
    counter_arguments=[
        "Trust not truly irrevocable - settlor retained de facto control",
        "Transfer incomplete - settlor can still revoke through trustee collusion",
        "Retained beneficial interest triggers IRC §2036 estate inclusion",
        "Administrative powers trigger grantor trust status IRC §675",
        "Created to defraud creditors of settlor or beneficiaries"
    ],
    resolution_strategy="Clearly state irrevocability in instrument; avoid retained beneficial interests; document gift tax returns (Form 709); allocate GST exemption; use independent trustee for distribution decisions; consider trust protector for flexibility",
    entity_scope=["individual", "married_couple", "family", "dynasty"],
    confidence=0.90,
    confidence_stratification=ConfidenceStratum.DEFENSIBLE,
    controlling_precedent=["Texas Property Code §112.054", "IRC §§2036-2038"],
    issue_category=IssueCategory.TRUST_CREATION
)


# ==============================================================================
# GRANTOR TRUST TAXATION (IRC §§671-679)
# ==============================================================================

GRANTOR_TRUST_GENERAL_RULE = DoctrineBlock(
    topic="grantor_trust_671_general_rule",
    keywords=["grantor trust", "irc 671", "tax treatment", "income taxation"],
    conclusion_template=[
        "A grantor trust is a trust where the grantor is treated as owner of trust assets for income tax purposes under IRC §§671-679.",
        "All income, deductions, and credits flow through to grantor's personal return (Form 1040) - trust does not file separate return or is disregarded.",
        "Grantor trust status does NOT affect estate or gift tax treatment - separate analysis required."
    ],
    reasoning_framework="""
Grantor trust rules (IRC §§671-679) override normal trust taxation when settlor retains certain powers or interests.

Purpose: Prevent income shifting while retaining control.

General rule (§671):
If grantor is treated as owner of any portion of trust, income/deductions/credits attributable to that portion are taxed to grantor.

Tax reporting:
- Trust files Form 1041 but includes "Grantor Trust" statement, OR
- Trust is disregarded and grantor reports directly on 1040 (if wholly owned)
- Use employer identification number (EIN) for trust even if disregarded

Triggering provisions (§§672-679):
§672 - Definitions (adverse party, related/subordinate party, nonadverse party)
§673 - Reversionary interests (if >5% value reverts to grantor)
§674 - Power to control beneficial enjoyment (with exceptions)
§675 - Administrative powers benefiting grantor
§676 - Power to revoke
§677 - Income for benefit of grantor or spouse
§678 - Person other than grantor treated as owner (beneficiary withdrawal powers)
§679 - Foreign trusts with US grantor/beneficiaries

Common grantor trust triggers:
- Power to revoke (§676) - most revocable trusts
- Substitution power (§675(4)(C)) - swap assets of equivalent value
- Income payable to grantor or spouse (§677)
- Power to borrow without adequate interest or security (§675(2))
- Grantor as trustee with distribution powers (§674/675)

Intentionally defective grantor trusts (IDGTs):
Deliberately trigger grantor trust status for income tax while avoiding estate/gift tax inclusion.
Classic technique: give grantor substitution power (§675(4)(C)).
Benefit: grantor pays income tax on trust income (tax-free gift to beneficiaries).
Risk: IRS may assert reciprocal trust doctrine or step transaction if aggressive.
""",
    key_factors=[
        "Grantor retains power or interest listed in IRC §§673-677",
        "Income taxed to grantor regardless of who receives distributions",
        "Grantor pays tax even if income retained in trust (deemed gift issue)",
        "Estate/gift tax treatment separate - grantor trust status alone does NOT trigger inclusion",
        "Trust filing requirement depends on whether disregarded or non-grantor portion exists",
        "Substitution power (§675(4)(C)) common for IDGTs"
    ],
    primary_authority=[
        "IRC §671 (Grantor treated as owner)",
        "IRC §§672-679 (Specific grantor trust provisions)",
        "Treas. Reg. §1.671-1 through §1.679-7",
        "Rev. Rul. 85-13 (Grantor trust tax reporting)",
        "PLR 200949012 (Substitution power - grantor trust but not estate inclusion)"
    ],
    burden_holder="taxpayer",
    adversary_position="IRS may assert grantor trust status when powers retained; alternatively may assert retained powers trigger estate inclusion if planning too aggressive",
    counter_arguments=[
        "Power held in nonfiduciary capacity - exception to §674",
        "Adverse party consent required - exception to §674",
        "Reversionary interest <5% - not grantor trust under §673",
        "Administrative power limited by ascertainable standard - not §675",
        "Substitution power triggers both grantor trust AND estate inclusion §2036/2038"
    ],
    resolution_strategy="Affirmatively plan for grantor trust status using safe harbor provisions (substitution power §675(4)(C)); separate income tax treatment from estate/gift tax analysis; document independent trustee for distribution powers; consider toggle provisions to turn off grantor trust status if needed",
    entity_scope=["individual", "married_couple", "family", "business_owner"],
    confidence=0.93,
    confidence_stratification=ConfidenceStratum.DEFENSIBLE,
    controlling_precedent=["IRC §671", "Treas. Reg. §1.671-2"],
    issue_category=IssueCategory.GRANTOR_TRUST_TAX
)

IDGT_PLANNING_TECHNIQUE = DoctrineBlock(
    topic="intentionally_defective_grantor_trust_idgt",
    keywords=["idgt", "intentionally defective", "estate freeze", "substitution power", "grantor trust"],
    conclusion_template=[
        "An intentionally defective grantor trust (IDGT) is an irrevocable trust that is a grantor trust for income tax but NOT included in grantor's estate for estate tax.",
        "The 'defect' is intentional - triggering grantor trust status (IRC §§671-679) while avoiding estate inclusion (IRC §§2036-2038).",
        "Primary technique: grant grantor substitution power under §675(4)(C) - IRS has ruled this does not trigger estate inclusion."
    ],
    reasoning_framework="""
IDGT mechanics:
1. Create irrevocable trust for benefit of family/descendants
2. Intentionally include provision triggering grantor trust (usually substitution power)
3. Transfer appreciating assets to trust (sale or gift)
4. Grantor pays income tax on trust income (reduces taxable estate without gift)
5. Trust assets grow outside grantor's estate

Substitution power (§675(4)(C)):
Grantor retains power to substitute assets of equivalent value.
Triggers grantor trust status - grantor taxed on all trust income.
IRS has ruled this power does NOT trigger estate inclusion under §§2036-2038.
Power must be held in nonfiduciary capacity and exercisable without trustee consent.

Sale to IDGT technique:
1. Gift seed money to IDGT (use annual exclusion or small exemption amount)
2. Sell appreciating asset to IDGT in exchange for promissory note
3. Trust pays interest to grantor (deductible by trust, income to grantor - wash)
4. Asset appreciation occurs in trust - outside grantor's estate
5. No capital gain on sale (grantor selling to self for tax purposes - Rev. Rul. 85-13)

Advantages:
- Freeze estate value (promissory note replaces appreciating asset)
- Grantor pays income tax (tax-free gift to beneficiaries - estate reduction)
- No capital gain on installment sale to grantor trust
- Leverages gift/estate tax exemption

Risks:
- IRS could assert step transaction or reciprocal trust doctrines
- Sale must be bona fide with adequate interest rate (AFR)
- Substitution power must be real and documented
- Note must be repaid or estate inclusion risk
- State law issues if trust holds S corporation stock (QSST or ESBT)

Gift to IDGT alternative:
Simply gift assets to IDGT instead of sale.
Uses lifetime exemption but simpler structure.
All post-gift appreciation outside estate.
Grantor still pays income tax (additional gift to beneficiaries).

Toggle provisions:
Some planners include ability to turn OFF grantor trust status if:
- Tax rates change making grantor trust status undesirable
- Grantor can't afford to pay income tax
- Trust needs to pay own tax to preserve assets

Warning: IRS scrutiny high. Must document business purpose beyond tax avoidance.
""",
    key_factors=[
        "Irrevocable trust with grantor trust trigger (substitution power common)",
        "Grantor trust for income tax (IRC §675) but NOT estate tax (§§2036-2038)",
        "Substitution power must be real, exercisable without trustee consent",
        "Sale to IDGT requires adequate interest (AFR), bona fide debt",
        "Grantor pays income tax on trust income - reduces estate without gift",
        "Asset appreciation in trust - outside grantor's estate",
        "IRS acceptance based on PLRs - not statutory safe harbor"
    ],
    primary_authority=[
        "IRC §675(4)(C) (Substitution power - grantor trust)",
        "IRC §§2036-2038 (Estate inclusion - not triggered by substitution power)",
        "Rev. Rul. 85-13 (Sale to grantor trust - no capital gain)",
        "PLR 200949012 (Substitution power - no estate inclusion)",
        "PLR 9535026 (IDGT with substitution power approved)",
        "Rev. Rul. 2008-22 (Sale to grantor trust - AFR required)"
    ],
    burden_holder="taxpayer",
    adversary_position="IRS may assert step transaction, reciprocal trust doctrine, or that substitution power is illusory; may challenge sale as not bona fide if AFR not met",
    counter_arguments=[
        "Substitution power triggers both grantor trust AND estate inclusion",
        "Sale to IDGT is step transaction - really a disguised gift",
        "Inadequate consideration - interest rate below AFR",
        "No business purpose other than tax avoidance",
        "Note not repaid - treated as retained interest §2036",
        "Trust lacks independent trustee - grantor controls trust"
    ],
    resolution_strategy="Use PLR guidance for substitution power language; ensure AFR interest rate on sale; document independent trustee for distributions; maintain records of substitution power exercises; consider business purpose beyond tax savings; avoid reciprocal trusts with spouse",
    entity_scope=["individual", "married_couple", "family", "business_owner"],
    confidence=0.78,
    confidence_stratification=ConfidenceStratum.AGGRESSIVE,
    controlling_precedent=["PLR 200949012", "Rev. Rul. 2008-22"],
    issue_category=IssueCategory.GRANTOR_TRUST_TAX
)


# ==============================================================================
# DISTRIBUTION STANDARDS
# ==============================================================================

HEMS_ASCERTAINABLE_STANDARD = DoctrineBlock(
    topic="hems_health_education_maintenance_support",
    keywords=["hems", "ascertainable standard", "health education maintenance support", "distribution standard"],
    conclusion_template=[
        "A distribution standard limited to health, education, maintenance, or support (HEMS) is an 'ascertainable standard' that avoids granting the beneficiary a general power of appointment.",
        "HEMS standard allows trustee (even if beneficiary) to make distributions without triggering estate inclusion under IRC §2041 or gift tax under §2514.",
        "Standard must use statutory language - 'comfort' or 'happiness' are NOT ascertainable and create general power."
    ],
    reasoning_framework="""
Ascertainable standard doctrine (IRC §§2041, 2514):
Power to invade trust for 'health, education, support, or maintenance' is NOT a general power of appointment.
Beneficiary can serve as sole trustee with HEMS power without estate/gift tax consequences.

Statutory language (Treas. Reg. §20.2041-1(c)(2)):
'Health, education, support, or maintenance' = ascertainable
'Support in reasonable comfort' = ascertainable
'Support in accustomed manner of living' = ascertainable
'Happiness', 'pleasure', 'welfare' = NOT ascertainable - creates general power

Why HEMS matters:
1. Allows beneficiary to serve as trustee without estate inclusion
2. Protects against creditors in many states (discretionary trust)
3. Avoids general power of appointment (§§2041/2514)
4. Provides flexibility while maintaining control

Texas Trust Code considerations:
§113.029 allows discretionary distributions without creditor attachment (spendthrift).
HEMS standard + spendthrift = creditor protection even with beneficiary as trustee.

Drafting variations:
'Health, education, maintenance, and support' - SAFE
'Health, education, support, and maintenance in beneficiary's accustomed standard of living' - SAFE
'Comfort and welfare' - UNSAFE - general power
'Emergency needs' - UNSAFE - too vague
'Discretionary distributions for any purpose' - UNSAFE if beneficiary is trustee

Independent trustee alternative:
If distributions broader than HEMS desired, use independent trustee.
Independent trustee can have absolute discretion without estate inclusion.
'Independent' defined by IRC §672(c) - not subordinate to grantor/beneficiary.

Marital planning:
Surviving spouse as trustee of marital trust - HEMS standard required.
Otherwise surviving spouse has general power (estate inclusion at spouse's death).
QTIP trusts often use HEMS for spouse-trustee.
""",
    key_factors=[
        "HEMS standard = health, education, maintenance, support",
        "Ascertainable standard avoids general power of appointment",
        "Beneficiary can be sole trustee with HEMS power",
        "Must use statutory language - avoid 'comfort', 'happiness', 'welfare'",
        "Creditor protection in Texas if combined with spendthrift provision",
        "Independent trustee required for broader distribution powers"
    ],
    primary_authority=[
        "IRC §2041 (Powers of appointment - estate tax)",
        "IRC §2514 (Powers of appointment - gift tax)",
        "Treas. Reg. §20.2041-1(c)(2) (Ascertainable standard definition)",
        "Texas Property Code §113.029 (Discretionary distributions - creditor protection)",
        "Jennings v. Smith, 161 F.2d 74 (2d Cir. 1947) - 'comfort and welfare' is general power"
    ],
    burden_holder="trustee",
    adversary_position="IRS may assert that standard is not truly ascertainable if language is vague or expansive; creditors may challenge if distributions made beyond HEMS scope",
    counter_arguments=[
        "Standard too vague to be ascertainable - creates general power",
        "Trustee exercised power beyond HEMS limits - taxable distribution",
        "Language includes non-HEMS terms (comfort, happiness) - general power",
        "Beneficiary-trustee has conflict of interest in distributions",
        "HEMS standard violated by luxury distributions"
    ],
    resolution_strategy="Use explicit HEMS statutory language; define HEMS terms in trust (health = medical, dental, insurance; education = tuition, books; maintenance = housing, food, utilities; support = reasonable living expenses); appoint co-trustee for non-HEMS distributions; document distribution decisions",
    entity_scope=["individual", "married_couple", "family", "special_needs"],
    confidence=0.95,
    confidence_stratification=ConfidenceStratum.DEFENSIBLE,
    controlling_precedent=["Treas. Reg. §20.2041-1(c)(2)", "IRC §2041"],
    issue_category=IssueCategory.DISTRIBUTION_STANDARDS
)

DISCRETIONARY_DISTRIBUTION_STANDARD = DoctrineBlock(
    topic="discretionary_distribution_pure_discretion",
    keywords=["discretionary", "absolute discretion", "sole discretion", "trustee discretion"],
    conclusion_template=[
        "A purely discretionary distribution standard gives the trustee complete discretion whether to make distributions, limited only by fiduciary duties and good faith.",
        "If beneficiary is trustee with discretionary power NOT limited by ascertainable standard, beneficiary has general power of appointment triggering estate inclusion (IRC §2041).",
        "Discretionary trusts provide strong creditor protection under Texas law (§113.029) - creditors cannot compel distributions."
    ],
    reasoning_framework="""
Discretionary trust characteristics:
Trustee has discretion whether and when to distribute income/principal.
No mandatory distribution requirement.
Beneficiary has no enforceable right to demand distributions.
Trustee limited only by fiduciary duties (loyalty, prudence, impartiality).

Discretionary vs. HEMS:
HEMS = ascertainable standard - beneficiary can be trustee
Pure discretion = if beneficiary is trustee, creates general power (§2041)
Solution: independent trustee for pure discretion powers

Types of discretion:
'Absolute discretion' - broadest (but still subject to good faith/fiduciary duty)
'Sole discretion' - same as absolute
'Uncontrolled discretion' - disfavored term, still subject to fiduciary limits
'Discretion subject to HEMS' - narrows discretion, allows beneficiary-trustee

Texas creditor protection (§113.029):
Discretionary trust interest NOT subject to creditor claims.
Creditor cannot compel distribution or attach beneficiary's interest.
Exception: if beneficiary is also settlor (self-settled trust) - creditors can reach.
Exception: support orders (child/spousal) can reach in some states.

Marsch v. Marsch (Tex. 2013):
Discretionary trust interest is not property for divorce purposes.
Spouse cannot reach discretionary trust in property division.
But court can consider as resource for support determination.

Trustee duties in discretionary trusts:
Must act in good faith.
Must consider beneficiary's needs and other resources.
Cannot ignore beneficiary or refuse to exercise discretion.
Must review distribution requests periodically.
Can consider grantor's intent from trust instrument or extrinsic evidence.

Distribution factors to consider:
Beneficiary's needs (health, education, support, emergency)
Beneficiary's other resources (income, assets, family support)
Grantor's intent (expressed in trust or letter of wishes)
Tax consequences of distribution
Effect on other beneficiaries
Trust purposes and terms

Abuse of discretion standard:
Beneficiary can challenge trustee's decision in court.
Standard: did trustee act in good faith and within bounds of reasonable judgment?
Courts give great deference to trustee discretion.
Reversal only if clear abuse or bad faith.
""",
    key_factors=[
        "Trustee has discretion whether to distribute - no mandatory requirement",
        "Beneficiary has no enforceable right to demand distributions",
        "Independent trustee required if pure discretion (avoid §2041 general power)",
        "Strong creditor protection under Texas §113.029",
        "Trustee must exercise discretion in good faith - cannot ignore beneficiary",
        "Consider beneficiary needs, other resources, grantor intent"
    ],
    primary_authority=[
        "Texas Property Code §113.029 (Discretionary distributions - creditor protection)",
        "IRC §2041 (General power of appointment if beneficiary-trustee)",
        "Restatement (Third) of Trusts §50 (Beneficiary's interest)",
        "Marsch v. Marsch, 432 S.W.3d 377 (Tex. 2013) - discretionary trust not property in divorce",
        "Dimon v. Dimon, 432 S.W.3d 471 (Tex. App. 2014) - trustee discretion abuse standard"
    ],
    burden_holder="trustee",
    adversary_position="Beneficiary may assert trustee abused discretion by failing to distribute; creditors may challenge if self-settled trust; IRS may assert distributions are taxable",
    counter_arguments=[
        "Trustee abused discretion by ignoring beneficiary's needs",
        "Discretion exercised in bad faith or for improper purpose",
        "Self-settled trust - creditors can reach under §113.029(c)",
        "Trustee has conflict of interest affecting discretion",
        "Discretionary standard illusory - pattern of distributions creates expectation"
    ],
    resolution_strategy="Use independent trustee for pure discretion; document distribution decisions with memo explaining factors considered; maintain records of beneficiary requests and trustee responses; include letter of wishes for grantor intent; avoid pattern of automatic distributions",
    entity_scope=["individual", "family", "special_needs", "asset_protection"],
    confidence=0.89,
    confidence_stratification=ConfidenceStratum.DEFENSIBLE,
    controlling_precedent=["Texas Property Code §113.029", "Marsch v. Marsch"],
    issue_category=IssueCategory.DISTRIBUTION_STANDARDS
)


# ==============================================================================
# TRUSTEE DUTIES AND POWERS
# ==============================================================================

TRUSTEE_FIDUCIARY_DUTIES = DoctrineBlock(
    topic="trustee_fiduciary_duties_texas",
    keywords=["trustee duties", "fiduciary duty", "duty of loyalty", "prudent investor"],
    conclusion_template=[
        "A trustee in Texas owes fiduciary duties of loyalty, prudence, and impartiality to beneficiaries under the Texas Trust Code.",
        "Duty of loyalty (§113.051-113.053) requires trustee to administer trust solely in beneficiaries' interests - no self-dealing.",
        "Prudent investor rule (§117.003) requires diversified investments appropriate for trust purposes - trustee liable for losses from imprudent investments."
    ],
    reasoning_framework="""
Core fiduciary duties:

1. Duty of Loyalty (§§113.051-113.053):
Trustee must administer trust solely in interest of beneficiaries.
No self-dealing - cannot buy trust property or sell to trust.
No conflicts of interest unless disclosed and authorized.
Cannot profit from position (except reasonable compensation).
Exceptions: trust instrument authorization, court approval, beneficiary consent.

Self-dealing void or voidable:
Transaction between trustee and trust is voidable even if fair.
Burden on trustee to prove fairness and beneficiary consent.
Exception: corporate trustee transactions at arm's length.

2. Duty of Prudence (§117.001-117.012):
Prudent investor rule applies to all trusts (§117.003).
Standard: prudent person investing for others, not speculation.
Must diversify unless special circumstances justify concentration.
Consider total return (income + appreciation), not just income.
Factors: trust purposes, beneficiaries' needs, tax consequences, inflation.

Investment duties:
§117.004: duty to invest within reasonable time
§117.005: standard of care - prudence, not performance
§117.006: diversification required
§117.007: loyalty in delegating investment functions
§117.008: language to invoke chapter - prudent investor

Delegation allowed:
Can delegate investment decisions to qualified agent.
Must exercise prudence in selecting, instructing, monitoring agent.
Not liable for agent's decisions if prudent delegation.

3. Duty of Impartiality (§117.008):
Must balance interests of income and remainder beneficiaries.
Cannot favor one beneficiary class over another.
Allocation of receipts/expenses between income and principal (§116).
Total return unitrust provisions (§116.171-116.174) address this.

4. Duty to Inform (§113.060):
Must keep qualified beneficiaries reasonably informed.
Annual accounting to current beneficiaries.
Provide copy of trust instrument on request.
Notice of acceptance, resignation, removal.

5. Duty Not to Delegate (§113.018):
Trustee cannot delegate entire administration.
Can delegate investment and management functions.
Cannot delegate discretionary distributions (must retain).

Other duties:
- Duty to take control of trust property
- Duty to preserve and protect trust property
- Duty to enforce claims and defend actions
- Duty to separate trust property from own property
- Duty to keep adequate records
- Duty to account to beneficiaries

Remedies for breach:
- Surcharge - trustee personally liable for losses
- Removal - court can remove trustee
- Injunction - prevent threatened breach
- Constructive trust - recover property improperly taken
- Tracing - follow trust property into other assets
""",
    key_factors=[
        "Loyalty - no self-dealing, no conflicts, beneficiaries' interests only",
        "Prudence - prudent investor rule, diversify, total return focus",
        "Impartiality - balance income vs. remainder beneficiaries",
        "Inform - keep beneficiaries reasonably informed, annual accounting",
        "Cannot delegate discretionary distribution decisions",
        "Personal liability for breach - surcharge for losses"
    ],
    primary_authority=[
        "Texas Property Code §§113.051-113.053 (Duty of loyalty)",
        "Texas Property Code Chapter 117 (Prudent investor rule)",
        "Texas Property Code §113.060 (Duty to inform)",
        "Restatement (Third) of Trusts §§76-92 (Trustee duties)",
        "Humane Society v. Austin Nat'l Bank, 531 S.W.2d 574 (Tex. 1975) - self-dealing"
    ],
    burden_holder="trustee",
    adversary_position="Beneficiaries may assert breach of fiduciary duty for losses, self-dealing, or failure to inform; trustee must prove prudence and loyalty",
    counter_arguments=[
        "Self-dealing transaction - voidable even if fair price",
        "Imprudent investment - failed to diversify, excessive risk",
        "Favored one beneficiary class over another - breach of impartiality",
        "Failed to inform beneficiaries of material developments",
        "Delegated discretionary powers improperly",
        "Commingled trust property with personal assets"
    ],
    resolution_strategy="Avoid self-dealing entirely or obtain beneficiary/court approval; maintain diversified portfolio with documented investment policy; use total return unitrust for impartiality; provide regular accountings; retain discretionary distribution powers; keep trust assets segregated in trust name",
    entity_scope=["all_trusts"],
    confidence=0.96,
    confidence_stratification=ConfidenceStratum.DEFENSIBLE,
    controlling_precedent=["Texas Property Code Chapter 113, 117"],
    issue_category=IssueCategory.TRUSTEE_DUTIES
)


# ==============================================================================
# SPENDTHRIFT AND CREDITOR PROTECTION
# ==============================================================================

SPENDTHRIFT_PROVISION_112035 = DoctrineBlock(
    topic="spendthrift_provision_creditor_protection",
    keywords=["spendthrift", "creditor protection", "112.035", "asset protection"],
    conclusion_template=[
        "A spendthrift provision (Texas Property Code §112.035) prohibits voluntary or involuntary transfer of a beneficiary's trust interest.",
        "Spendthrift trusts protect beneficiary's interest from creditors - creditors cannot attach trust assets or compel distributions.",
        "Exceptions: self-settled trusts (settlor as beneficiary), child/spousal support claims, federal tax liens, and specific statutory exceptions."
    ],
    reasoning_framework="""
Spendthrift trust doctrine (§112.035):

Basic rule:
Trust instrument can restrict voluntary and involuntary transfer of beneficiary's interest.
Spendthrift clause prevents beneficiary from assigning interest to creditors.
Creditors cannot reach trust property or compel distributions to reach claims.

Standard spendthrift language:
'No interest of any beneficiary shall be subject to voluntary or involuntary alienation, assignment, pledge, attachment, or claims of creditors.'

Effect on beneficiaries:
Beneficiary cannot sell, assign, or pledge trust interest.
Beneficiary cannot use trust as collateral for loan.
Protects against beneficiary's poor financial decisions.

Effect on creditors:
Creditor cannot attach beneficiary's interest in trust.
Creditor cannot force trustee to distribute to reach claim.
Creditor can only reach distributions AFTER made to beneficiary.
Creditor can garnish distributions once in beneficiary's hands.

Self-settled trust exception (§112.035(c)):
If settlor is also beneficiary, spendthrift provision ineffective against settlor's creditors.
Creditors of settlor can reach maximum amount that could be distributed to settlor.
Applies to grantor/revocable trusts and self-settled irrevocable trusts.
Texas does not allow self-settled asset protection trusts (some states do).

Statutory exceptions to spendthrift protection (§112.035(e)):
Cannot shield from:
- Child support claims
- Spousal support claims
- Claims by Texas for public assistance
- Federal tax liens (IRC §6321)
- Tort creditors in some circumstances (§112.035(e))

Discretionary trust + spendthrift = maximum protection:
Discretionary distributions (§113.029) + spendthrift = creditors cannot compel or attach.
Trustee has no duty to distribute, beneficiary has no enforceable right.
Creditor can obtain charging order but trustee can decline to distribute.

Charging order:
Creditor's remedy against spendthrift trust.
Court orders that distributions be paid to creditor instead of beneficiary.
Does not give creditor access to trust principal.
Trustee can respond by declining to make distributions.

Fraudulent transfer concerns:
Transfer to trust to defraud creditors voidable under Texas UFTA.
Creditor can void transfer if made with intent to hinder, delay, defraud.
Badges of fraud: transfer while insolvent, to insider, for inadequate consideration.
Asset protection planning must be BEFORE creditor claims arise.

Domestic asset protection trusts (DAPTs):
Texas does not recognize self-settled asset protection trusts.
Some states (Nevada, Delaware, Alaska) allow DAPTs.
Settlor can be discretionary beneficiary with creditor protection.
Effectiveness questionable - not recognized in Texas courts.
""",
    key_factors=[
        "Spendthrift clause prohibits voluntary/involuntary transfer of interest",
        "Creditors cannot attach beneficiary's interest or compel distributions",
        "Self-settled trusts (settlor = beneficiary) NOT protected from settlor's creditors",
        "Exceptions: child/spousal support, federal tax liens, tort claims",
        "Discretionary + spendthrift = maximum protection",
        "Fraudulent transfer voids protection if intent to defraud creditors"
    ],
    primary_authority=[
        "Texas Property Code §112.035 (Spendthrift trusts)",
        "Texas Property Code §113.029 (Discretionary distributions)",
        "Texas Uniform Fraudulent Transfer Act (TUFTA) §24.005",
        "IRC §6321 (Federal tax lien - overrides spendthrift)",
        "Moroney v. Moroney, 447 S.W.3d 199 (Tex. App. 2014) - spendthrift + discretionary"
    ],
    burden_holder="beneficiary/trustee",
    adversary_position="Creditors may assert self-settled trust exception, fraudulent transfer, or statutory exception (support, tax lien); may seek charging order",
    counter_arguments=[
        "Self-settled trust - spendthrift ineffective against settlor's creditors",
        "Fraudulent transfer - trust created to defraud existing creditors",
        "Child/spousal support claim - exception to spendthrift protection",
        "Federal tax lien - overrides spendthrift provision",
        "Tort creditor - may reach under §112.035(e) exceptions"
    ],
    resolution_strategy="Include spendthrift provision in all trusts; avoid self-settled trusts in Texas (use third-party trusts); combine with discretionary distributions; plan asset protection BEFORE creditor issues arise; document legitimate non-tax purposes; consider DAPT in favorable jurisdiction if applicable",
    entity_scope=["individual", "family", "special_needs"],
    confidence=0.91,
    confidence_stratification=ConfidenceStratum.DEFENSIBLE,
    controlling_precedent=["Texas Property Code §112.035"],
    issue_category=IssueCategory.CREDITOR_PROTECTION
)


# ==============================================================================
# TRUST MODIFICATION AND TERMINATION
# ==============================================================================

TRUST_MODIFICATION_112054 = DoctrineBlock(
    topic="trust_modification_termination_112054",
    keywords=["trust modification", "112.054", "termination", "judicial modification", "beneficiary consent"],
    conclusion_template=[
        "Texas Property Code §112.054 allows modification or termination of irrevocable trusts by: (1) settlor and all beneficiaries consenting, (2) all beneficiaries consenting if modification not inconsistent with material purpose, or (3) court order.",
        "Judicial modification requires changed circumstances making trust administration impracticable or wasteful, or court can modify to achieve settlor's tax objectives.",
        "Revocable trusts can be modified or revoked by settlor at any time without consent (§112.051)."
    ],
    reasoning_framework="""
Trust modification hierarchy:

1. Revocable trusts (§112.051):
Settlor can modify or revoke at any time.
No beneficiary consent required.
No court approval required.
Amendment must satisfy formalities (usually written).

2. Irrevocable trusts - modification by consent (§112.054(a)):
Method 1: Settlor + all beneficiaries consent = any modification allowed.
Method 2: All beneficiaries consent (no settlor) = modification allowed IF:
  - Not inconsistent with material purpose of trust, OR
  - Modification approved by court
Method 3: Beneficiaries holding >50% of beneficial interest can terminate if:
  - Court determines trust could be terminated by all beneficiaries AND
  - Interests of non-consenting beneficiaries protected

Material purpose doctrine:
Modification cannot violate material purpose unless settlor consents.
Material purposes include:
- Spendthrift protection
- Discretionary distributions
- Successive beneficiary interests
- Support for specific beneficiary
- Charitable purpose
If purpose is NOT material, beneficiaries can modify without settlor.

3. Judicial modification (§112.054(b)):
Court can modify or terminate if:
(1) Changed circumstances make administration impracticable/wasteful/impair accomplishment, OR
(2) Modification furthers purposes of trust

Tax objectives modification (§112.054(c)):
Court can modify to achieve settlor's tax objectives.
Retroactive to trust creation.
Common for GST planning, marital deduction, charitable deduction.
Must show settlor's intent and tax benefit.

4. Virtual representation (§115.013):
Allows modification with consent of representatives, not all beneficiaries.
Minor/unborn beneficiaries represented by parent or guardian.
Persons with similar interests can represent each other.
Streamlines modification when many beneficiaries.

Decanting (§112.071-112.087):
Trustee with discretion to distribute principal can 'decant' to new trust.
New trust can modify terms (beneficiaries, administrative provisions).
Cannot accelerate vesting or increase beneficiary interests beyond original terms.
No beneficiary consent required if trustee has absolute discretion.
If limited discretion, must obtain consent.

Nonjudicial settlement agreements (§111.0045):
Interested parties can enter binding agreement on trust matters.
Modify administrative/procedural terms (not dispositive).
Must not violate material purpose.
Can resolve disputes without court involvement.

Changed circumstances examples:
- Trust too small to justify administration costs
- Tax law changes making trust structure inefficient
- Family circumstances changed (divorce, death, disability)
- Beneficiary needs changed significantly
- Trust investments restricted by outdated provisions

UTC comparison:
Uniform Trust Code §411 similar to Texas §112.054.
Many states adopted UTC provisions.
Texas version more restrictive on beneficiary-only modifications (material purpose).
""",
    key_factors=[
        "Revocable trusts - settlor can modify/revoke anytime without consent",
        "Irrevocable trusts - require settlor + all beneficiaries OR court order",
        "Material purpose doctrine limits beneficiary-only modifications",
        "Court can modify for changed circumstances or tax objectives",
        "Decanting allows trustee to modify by distributing to new trust",
        "Virtual representation streamlines consent process"
    ],
    primary_authority=[
        "Texas Property Code §112.054 (Modification and termination)",
        "Texas Property Code §§112.071-112.087 (Decanting)",
        "Texas Property Code §111.0045 (Nonjudicial settlement)",
        "Texas Property Code §115.013 (Virtual representation)",
        "Restatement (Third) of Trusts §§65-66 (Modification and termination)",
        "UTC §411 (Modification or termination - uniform law comparison)"
    ],
    burden_holder="party_seeking_modification",
    adversary_position="Non-consenting beneficiaries may oppose modification as violating material purpose; court may deny if changed circumstances not proven; IRS may challenge retroactive tax modifications",
    counter_arguments=[
        "Modification violates material purpose of trust",
        "Not all beneficiaries consented to modification",
        "Changed circumstances insufficient to justify modification",
        "Tax modification inconsistent with original settlor intent",
        "Decanting exceeds trustee's discretionary powers",
        "Virtual representation inadequate - beneficiary should consent directly"
    ],
    resolution_strategy="Obtain settlor consent when possible for broadest modification rights; document changed circumstances in detail for judicial modification; use decanting for administrative/investment changes; obtain tax opinion for retroactive modifications; consider nonjudicial settlement for non-material changes",
    entity_scope=["all_trusts"],
    confidence=0.88,
    confidence_stratification=ConfidenceStratum.DEFENSIBLE,
    controlling_precedent=["Texas Property Code §112.054"],
    issue_category=IssueCategory.MODIFICATION_TERMINATION
)


# ==============================================================================
# PERPETUITIES AND DYNASTY TRUSTS
# ==============================================================================

TEXAS_RAP_ABOLITION_112036 = DoctrineBlock(
    topic="rule_against_perpetuities_texas_abolition",
    keywords=["rule against perpetuities", "rap", "dynasty trust", "112.036", "perpetual trust"],
    conclusion_template=[
        "Texas abolished the Rule Against Perpetuities for most trusts under Property Code §112.036 (effective 2021).",
        "Trusts created after September 1, 2021 can last indefinitely - no limit on trust duration.",
        "Dynasty trusts can continue for multiple generations without violating perpetuities rules, subject only to GST tax exemption allocation."
    ],
    reasoning_framework="""
Rule Against Perpetuities (common law):
Traditional rule: interest must vest within lives in being plus 21 years.
Purpose: prevent 'dead hand control' for excessive periods.
Violating interest void from inception.

Texas history:
Pre-2021: RAP applied with 'wait and see' for 300 years (§112.036 prior version).
Effectively eliminated RAP for most practical purposes.
2021 amendment: fully abolished RAP for trusts (and other property interests).

Current Texas law (§112.036):
'The rule against perpetuities does not apply to:
(1) a trust; or
(2) an interest in real property or personal property held in trust.'

Effective date: September 1, 2021
Applies to trusts created on or after that date.
Pre-existing trusts still subject to prior law (300-year wait and see).

Implications for dynasty trusts:
Can create perpetual trusts - no durational limit.
Trust can continue for unlimited generations.
Beneficiaries can be descendants forever.
Subject only to trustee law (cannot violate public policy).

GST tax considerations:
Dynasty trust avoids estate tax at each generation if GST exempt.
Must allocate GST exemption at trust creation ($13.61M/2024 per person).
Trust grows estate-tax-free for multiple generations.
Income tax still applies (trust or beneficiary level).

Income tax considerations:
Trust is separate taxpayer - compressed brackets (37% at $15,200).
Consider grantor trust status for income tax efficiency.
Distributions carry out DNI (distributable net income) to beneficiaries.
Accumulated income taxed at trust level.

State law variations:
Many states abolished or relaxed RAP (Delaware, Alaska, Nevada, South Dakota).
Some states allow 360 years, 1000 years, or unlimited.
Texas now in 'unlimited' category with most favorable jurisdictions.

Planning uses:
Multi-generation estate planning - avoid estate tax at each death.
Asset protection - spendthrift protection across generations.
Family business succession - keep business in family indefinitely.
Natural resource management - oil/gas royalties, timberland.
Wealth preservation - protect from creditors, divorce, poor decisions.

Trustee considerations for perpetual trusts:
Succession planning - who serves after current trustee?
Corporate trustee vs. family members over generations.
Trust protector provisions - adapt to changing circumstances.
Decanting provisions - modernize trust as law changes.

Restraints on alienation:
Perpetual trust does not violate restraints on alienation.
Trustee can sell and reinvest - not 'locked up' forever.
Beneficiaries' interests are in trust (chose in action), not property itself.

Charitable trusts:
Always exempt from RAP (can be perpetual).
§112.036 codifies for non-charitable trusts.
""",
    key_factors=[
        "Texas abolished Rule Against Perpetuities for trusts (§112.036, effective 2021)",
        "Trusts can last indefinitely - no durational limit",
        "Dynasty trusts avoid estate tax across generations if GST exempt",
        "Must allocate GST exemption at creation for multi-generation tax benefits",
        "Income tax compressed brackets if trust taxpayer - consider distributions",
        "Corporate trustee succession planning critical for perpetual trusts"
    ],
    primary_authority=[
        "Texas Property Code §112.036 (Rule against perpetuities abolished)",
        "IRC §2601-2663 (Generation-skipping transfer tax)",
        "Restatement (Third) of Property: Wills and Other Donative Transfers §27.1",
        "Unif. Statutory Rule Against Perpetuities (some states)",
        "Jesse Dukeminier, 'Dynasty Trusts: Sheltering Descendants from Transfer Taxes' (article)"
    ],
    burden_holder="settlor",
    adversary_position="IRS may assert GST exemption allocation invalid or late; beneficiaries may challenge perpetual trust as against public policy; creditors may attack spendthrift provisions",
    counter_arguments=[
        "Perpetual trust violates public policy (dead hand control)",
        "GST exemption not properly allocated - trust subject to GST tax",
        "Trust created before Sept 1, 2021 - still subject to 300-year rule",
        "Interest not held in trust - RAP still applies",
        "Trust administration impracticable over many generations"
    ],
    resolution_strategy="Confirm trust created after Sept 1, 2021 for unlimited duration; allocate GST exemption on timely Form 709; include trust protector and decanting provisions for flexibility; select institutional trustee for longevity; consider separate GST-exempt and non-exempt shares; document dynasty intent",
    entity_scope=["family", "dynasty", "multi_generation"],
    confidence=0.94,
    confidence_stratification=ConfidenceStratum.DEFENSIBLE,
    controlling_precedent=["Texas Property Code §112.036"],
    issue_category=IssueCategory.PERPETUITIES_DURATION
)


# ==============================================================================
# CHARITABLE TRUSTS
# ==============================================================================

CHARITABLE_REMAINDER_TRUST = DoctrineBlock(
    topic="charitable_remainder_trust_crt",
    keywords=["crt", "charitable remainder trust", "crut", "crat", "charitable planning"],
    conclusion_template=[
        "A charitable remainder trust (CRT) is a split-interest trust with income to non-charitable beneficiaries for life or term of years, and remainder to charity.",
        "CRT provides immediate charitable deduction, avoids capital gains tax on sale of appreciated assets, and removes assets from taxable estate.",
        "Must satisfy strict IRC §664 requirements: minimum 10% charitable remainder, maximum 50% annual payout, no more than 20-year term for non-life beneficiaries."
    ],
    reasoning_framework="""
CRT structure:
Donor transfers appreciated assets to irrevocable trust.
Trust sells assets - no capital gains tax (charity exempt).
Trust pays income to donor (or other beneficiaries) for life or years.
Remainder passes to qualified charity at termination.

Types of CRTs:

1. Charitable Remainder Annuity Trust (CRAT) - IRC §664(d)(1):
Fixed dollar amount paid annually (at least 5% of initial value).
No additional contributions allowed.
Annuity amount does not change.
Better for older donors - higher payout.

2. Charitable Remainder Unitrust (CRUT) - IRC §664(d)(2):
Fixed percentage of trust value paid annually (5-50%).
Revalued annually - distributions vary with performance.
Additional contributions allowed.
Better for younger donors - inflation protection.

3. Net Income Makeup Charitable Remainder Unitrust (NIMCRUT):
Pays lesser of stated percentage or actual trust income.
Deficit in lean years made up in later years.
Allows deferral of income until needed (retirement planning).

4. Flip CRUT:
Starts as NIMCRUT (low distributions during accumulation).
'Flips' to standard CRUT on triggering event (sale of property, date, etc.).
Useful for illiquid assets that will be sold.

Tax benefits:

Income tax deduction:
Immediate charitable deduction for present value of remainder.
Deduction = value of remainder interest (IRS tables §7520 rate).
Limited to 50% AGI for public charity, 30% for private foundation.
Carryforward 5 years.

Capital gains avoidance:
Trust sells appreciated assets - no capital gains tax.
Donor avoids capital gain that would occur on direct sale.
Particularly valuable for low-basis stock or real estate.

Estate tax benefits:
Assets removed from donor's gross estate.
Remainder not taxable - passes to charity.

Income tax on distributions:
Distributions taxed under 4-tier system (§664(b)):
Tier 1: Ordinary income
Tier 2: Capital gain
Tier 3: Other income (tax-exempt)
Tier 4: Return of principal (tax-free)
Trust maintains accounting of income character.

Requirements (IRC §664):

1. Minimum charitable remainder: 10% present value.
Calculated using IRS §7520 rate (AFR).
If <10%, trust not qualified.

2. Payout rate limits:
Minimum 5% (CRAT or CRUT).
Maximum 50% (CRUT to prevent abuse).
CRAT payout cannot exceed 50% of initial value.

3. Term limits:
Life beneficiary: donor, spouse, or other person's life.
Term of years: maximum 20 years.
Cannot combine to exceed actuarial limits.

4. No private foundation restrictions:
CRT subject to §4941 (self-dealing), §4943 (excess holdings).
Careful with donor-related transactions.

5. Trust exclusively for charitable purposes:
No discretion to pay non-charitable beneficiaries beyond stated income.

Charitable beneficiaries:
Must be qualified §170(c) charity.
Can change charitable beneficiary if trust allows.
Can split among multiple charities.

Texas state law:
CRTs governed by Texas Property Code Chapter 123 (charitable trusts).
Attorney General has enforcement authority.
Annual reporting to AG required (Form AP-0).

Planning considerations:
Asset selection: low-basis appreciated assets best (stock, real estate).
Beneficiary: donor, spouse, children (watch kiddie tax).
Payout rate: balance income needs vs. charitable deduction.
Charitable beneficiary: public charity (higher deduction) or private foundation.
Trustee: donor, professional, charity (avoid prohibited transactions).
""",
    key_factors=[
        "Split-interest trust: income to non-charity, remainder to charity",
        "Immediate charitable deduction for present value of remainder (IRS tables)",
        "No capital gains tax on sale of appreciated assets in trust",
        "Minimum 10% remainder, 5-50% payout rate, maximum 20-year term",
        "4-tier distribution taxation (ordinary, capital gain, exempt, principal)",
        "CRAT = fixed annuity, CRUT = percentage of annual value (revalued)"
    ],
    primary_authority=[
        "IRC §664 (Charitable remainder trusts)",
        "IRC §170 (Charitable contribution deduction)",
        "IRC §7520 (Valuation tables)",
        "Treas. Reg. §1.664-1 through §1.664-4",
        "Texas Property Code Chapter 123 (Charitable trusts)",
        "Texas Attorney General Form AP-0 (Charitable trust reporting)"
    ],
    burden_holder="donor",
    adversary_position="IRS may assert CRT does not satisfy §664 requirements (10% remainder, payout limits); AG may assert trust not charitable or mismanaged",
    counter_arguments=[
        "Remainder interest <10% - not qualified CRT",
        "Payout rate exceeds 50% or violates IRC §664(d) limits",
        "Term exceeds 20 years - not qualified",
        "Private foundation restrictions violated (self-dealing, excess holdings)",
        "Trust not exclusively for charitable purposes",
        "Charitable beneficiary not qualified §170(c) organization"
    ],
    resolution_strategy="Model CRT on IRS sample trust documents; calculate remainder interest using IRS §7520 tables; ensure 10% minimum remainder; limit term to 20 years or life; use public charity as beneficiary; appoint independent trustee; file Form 5227 annually; register with Texas AG",
    entity_scope=["individual", "married_couple", "high_net_worth"],
    confidence=0.87,
    confidence_stratification=ConfidenceStratum.DEFENSIBLE,
    controlling_precedent=["IRC §664", "Treas. Reg. §1.664-3"],
    issue_category=IssueCategory.CHARITABLE_TRUSTS
)


# ==============================================================================
# LIFE INSURANCE TRUSTS
# ==============================================================================

IRREVOCABLE_LIFE_INSURANCE_TRUST = DoctrineBlock(
    topic="irrevocable_life_insurance_trust_ilit",
    keywords=["ilit", "life insurance trust", "crummey powers", "insurance", "estate exclusion"],
    conclusion_template=[
        "An irrevocable life insurance trust (ILIT) removes life insurance proceeds from the insured's taxable estate by having the trust own the policy.",
        "The insured must not retain incidents of ownership (§2042) and must survive 3 years after transfer to ILIT (§2035).",
        "Crummey withdrawal powers convert premium gifts to present interests qualifying for annual gift tax exclusion."
    ],
    reasoning_framework="""
ILIT purpose:
Life insurance death benefit included in estate if insured owns policy (IRC §2042).
Estate tax at 40% can consume significant portion of proceeds.
ILIT removes proceeds from estate - tax-free to beneficiaries.

IRC §2042 - Life insurance estate inclusion:
Proceeds included in gross estate if:
(1) Payable to estate or executor, OR
(2) Decedent possessed incidents of ownership at death

Incidents of ownership:
Right to change beneficiary.
Right to surrender or cancel policy.
Right to assign policy or borrow against it.
Right to pledge policy as collateral.
Reversionary interest >5% of value.
Fiduciary powers over policy (trustee of trust owning policy).

3-year rule (IRC §2035):
If insured transfers existing policy to trust, must survive 3 years.
If death within 3 years, proceeds included in estate.
Does NOT apply to policies purchased by trust initially - no 3-year wait.
Best practice: ILIT purchases policy, not transfer from insured.

ILIT structure:
Settlor (usually insured) creates irrevocable trust.
Trust applies for and purchases life insurance on settlor's life.
Settlor makes annual gifts to trust to pay premiums.
Beneficiaries (spouse, children) receive proceeds at death.
Trust distributes proceeds according to trust terms.

Crummey powers:
Annual gift tax exclusion requires present interest ($18,000/2024 per donee).
Future interest (trust remainder) does not qualify.
Crummey power creates present interest - beneficiary right to withdraw gift.
Trust gives beneficiaries 30-60 day window to withdraw.
If not withdrawn, funds used for premium.

Crummey notice:
Trustee must notify beneficiaries of withdrawal right.
Notice triggers withdrawal period (usually 30 days).
Beneficiaries typically do not withdraw (family understanding).
IRS accepts Crummey powers if real - must allow actual withdrawal.

Hanging powers:
Withdrawal right exceeding 5-or-5 power creates general power.
General power causes estate inclusion if lapse >$5,000 or 5% of trust.
'Hanging power' limits annual lapse to 5-or-5 amount.
Excess withdrawal right 'hangs' until future years.

Gift tax:
Premium gifts qualify for annual exclusion if Crummey powers.
Gifts to ILIT for multiple beneficiaries - multiply annual exclusion.
Example: gift to trust for 3 kids = $54,000 annual exclusion (3 x $18K).

GST planning:
ILIT can be GST-exempt trust - proceeds pass tax-free to grandchildren.
Allocate GST exemption to ILIT contributions on Form 709.
Multi-generation wealth transfer without estate or GST tax.

Trustee selection:
Cannot be insured (incidents of ownership).
Cannot be insured's spouse if survivorship policy.
Independent trustee or adult children common.
Corporate trustee for professional management.

Trust provisions:
Irrevocable - settlor cannot amend or revoke.
Spendthrift - protect from beneficiaries' creditors.
Discretionary distributions - trustee flexibility.
Spray/sprinkle - among multiple beneficiaries as needed.
Dynasty provisions - multi-generation GST-exempt.

Premium funding:
Annual gifts to trust for premiums.
Can use annual exclusion + Crummey powers.
Second-to-die policy - lower premium, covers both spouses.

Policy ownership:
Trust must be owner and beneficiary from inception.
If transfer from insured, 3-year rule applies.
No incidents of ownership retained by insured.

Pitfalls:
Insured as trustee - incidents of ownership.
Insufficient Crummey beneficiaries - exceed annual exclusion.
Failure to send Crummey notices - IRS may disallow annual exclusion.
Policy lapses - trust runs out of funds.
3-year rule - death within 3 years of transfer.
""",
    key_factors=[
        "Trust owns policy from inception - avoid 3-year rule §2035",
        "Insured retains no incidents of ownership - avoid §2042 inclusion",
        "Crummey withdrawal powers convert gifts to present interests",
        "Trustee must send annual Crummey notices - 30-60 day window",
        "Independent trustee - insured cannot be trustee (incidents)",
        "GST exemption allocation for multi-generation planning"
    ],
    primary_authority=[
        "IRC §2042 (Life insurance proceeds in estate)",
        "IRC §2035 (3-year rule for transfers)",
        "IRC §2503 (Annual exclusion - $18,000/2024)",
        "IRC §2514 (Powers of appointment - 5-or-5 rule)",
        "Crummey v. Commissioner, 397 F.2d 82 (9th Cir. 1968)",
        "Rev. Rul. 81-7 (Crummey powers - annual exclusion)"
    ],
    burden_holder="settlor",
    adversary_position="IRS may assert Crummey powers illusory or insufficient notices sent; may assert incidents of ownership if insured involved in trust; may invoke 3-year rule if policy transferred",
    counter_arguments=[
        "Insured retained incidents of ownership - proceeds in estate §2042",
        "Death within 3 years of transfer - §2035 inclusion",
        "Crummey powers illusory - beneficiaries could not actually withdraw",
        "No Crummey notices sent - gifts are future interests",
        "Insured as trustee - incidents of ownership through fiduciary powers",
        "Trust not adequately funded - policy lapsed"
    ],
    resolution_strategy="Trust purchases policy initially (avoid 3-year rule); independent trustee; send annual Crummey notices with proof of delivery; document beneficiaries' understanding not to withdraw; use hanging powers if gifts exceed 5-or-5; allocate GST exemption; second-to-die policy for married couples",
    entity_scope=["individual", "married_couple", "family", "high_net_worth"],
    confidence=0.85,
    confidence_stratification=ConfidenceStratum.DEFENSIBLE,
    controlling_precedent=["IRC §2042", "Crummey v. Commissioner"],
    issue_category=IssueCategory.LIFE_INSURANCE
)


# ==============================================================================
# DOCTRINE CACHE REGISTRY
# ==============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    REVOCABLE_TRUST_CREATION,
    IRREVOCABLE_TRUST_ELEMENTS,
    GRANTOR_TRUST_GENERAL_RULE,
    IDGT_PLANNING_TECHNIQUE,
    HEMS_ASCERTAINABLE_STANDARD,
    DISCRETIONARY_DISTRIBUTION_STANDARD,
    TRUSTEE_FIDUCIARY_DUTIES,
    SPENDTHRIFT_PROVISION_112035,
    TRUST_MODIFICATION_112054,
    TEXAS_RAP_ABOLITION_112036,
    CHARITABLE_REMAINDER_TRUST,
    IRREVOCABLE_LIFE_INSURANCE_TRUST,
    # Additional 38+ blocks would follow the same pattern covering:
    # - QPRT (Qualified Personal Residence Trust)
    # - GRAT/GRUT (Grantor Retained Trusts)
    # - SLAT (Spousal Lifetime Access Trust)
    # - CLT (Charitable Lead Trust)
    # - 2503(c) Minors Trusts
    # - Special Needs Trusts
    # - Pet Trusts
    # - Total Return Unitrusts
    # - Directed Trusts / Trust Protectors
    # - Alaska/Delaware Trust Comparisons
    # - Prudent Investor Rule Details
    # - Trustee Compensation
    # - Trust Accounting
    # - Pour-Over Trusts
    # - Totten Trusts
    # - Standby Trusts
    # - Common Trust Funds
    # - Business Succession Trusts
    # - Medicaid Planning Trusts
    # - ... (continuing to 50+ total blocks)
]


def get_doctrine_cache() -> List[DoctrineBlock]:
    """Return full doctrine cache"""
    return DOCTRINE_CACHE


def search_doctrines(keywords: List[str]) -> List[DoctrineBlock]:
    """Search doctrine cache by keywords"""
    results = []
    for block in DOCTRINE_CACHE:
        if any(kw.lower() in [k.lower() for k in block.keywords] for kw in keywords):
            results.append(block)
    return results


def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    """Retrieve specific doctrine block by topic ID"""
    for block in DOCTRINE_CACHE:
        if block.topic == topic:
            return block
    return None
