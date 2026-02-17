"""
TX01 IRC Parser Engine - Doctrine Definitions
Comprehensive IRC parsing and statutory interpretation doctrines
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class IssueCategory(str, Enum):
    SECTION_STRUCTURE = "SECTION_STRUCTURE"
    STATUTORY_INTERPRETATION = "STATUTORY_INTERPRETATION"
    CROSS_REFERENCE = "CROSS_REFERENCE"
    EFFECTIVE_DATE = "EFFECTIVE_DATE"
    ANTI_ABUSE = "ANTI_ABUSE"
    SUNSET_CLAUSE = "SUNSET_CLAUSE"
    TRANSITIONAL_RULE = "TRANSITIONAL_RULE"
    REGULATORY_INTEGRATION = "REGULATORY_INTEGRATION"
    REVENUE_RULING = "REVENUE_RULING"
    DEFINITIONAL_ANALYSIS = "DEFINITIONAL_ANALYSIS"
    AMENDMENT_TRACKING = "AMENDMENT_TRACKING"
    AUTHORITY_HIERARCHY = "AUTHORITY_HIERARCHY"


@dataclass
class DoctrineBlock:
    """Represents a single doctrine with full reasoning framework"""
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: Optional[str]
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: List[str]
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: List[str]
    issue_category: IssueCategory


# Doctrine Cache - 52 blocks covering IRC parsing domain expertise
DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="IRC_Section_Hierarchical_Structure",
        keywords=["section", "subsection", "paragraph", "subparagraph", "clause", "subclause", "hierarchy"],
        conclusion_template=[
            "IRC sections follow strict hierarchical numbering: § X(a)(1)(A)(i)(I).",
            "Each level has specific semantic weight in statutory construction.",
            "Lower levels refine or limit higher-level provisions unless explicitly stated otherwise."
        ],
        reasoning_framework="""
IRC sections are structured in a nested hierarchy: Section → Subsection (lowercase letter) →
Paragraph (number) → Subparagraph (uppercase letter) → Clause (lowercase roman) →
Subclause (uppercase roman). This structure is NOT arbitrary—it reflects Congressional intent
regarding the relationship between general rules and specific exceptions or refinements.

General interpretive canon: higher-level provisions state the general rule, lower levels provide
exceptions, limitations, or special cases. However, flush language (unnumbered text within a section)
can apply to all subsections or only to the immediately preceding clause—context determines scope.

Cross-references must specify the exact hierarchical level (e.g., "§ 162(a)(1)" vs "§ 162").
Imprecise references create ambiguity in regulatory interpretation. Treasury regulations mirror
this structure with decimal notation (e.g., Treas. Reg. § 1.162-1(a)(1)).

Structural placement matters: definitions in subsection (defining terms) bind the entire section.
Effective date provisions in subsection (h) or (i) control temporal application. Anti-abuse rules
often appear as final subsections, applying broadly unless scoped narrowly by their own text.
""",
        key_factors=[
            "Hierarchical level depth (section vs subparagraph)",
            "Presence of flush language and its scope",
            "Cross-reference precision",
            "Definitional subsection placement",
            "Exception vs general rule positioning",
            "Temporal scope indicators (effective dates)",
            "Anti-abuse provision placement"
        ],
        primary_authority=["IRC § 7806", "26 USC § 1 et seq.", "Bluebook citation rules"],
        burden_holder="taxpayer claiming benefit or IRS asserting deficiency",
        adversary_position="Opposing party may argue structural placement indicates narrow or broad scope",
        counter_arguments=[
            "Flush language applies to entire section not just preceding clause",
            "Lower-level provision is independent grant of authority not limitation",
            "Cross-reference imprecision is harmless error",
            "Structural placement is coincidental not intentional",
            "Anti-abuse rule scope extends beyond its subsection"
        ],
        resolution_strategy="Apply canons of statutory construction: specific controls general, later-enacted controls earlier, express mention excludes implied inclusion",
        entity_scope=["all_entities"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: well-established interpretive framework",
        controlling_precedent=["Chevron U.S.A., Inc. v. NRDC", "King v. Burwell"],
        issue_category=IssueCategory.SECTION_STRUCTURE
    ),

    DoctrineBlock(
        topic="Plain_Meaning_Rule_IRC_Interpretation",
        keywords=["plain meaning", "statutory interpretation", "ambiguity", "legislative intent", "textualism"],
        conclusion_template=[
            "Plain meaning of IRC text governs absent clear ambiguity or absurd result.",
            "Technical tax terms have specific meanings developed through case law and regulations.",
            "Extrinsic evidence (legislative history) consulted only when text is genuinely ambiguous."
        ],
        reasoning_framework="""
The plain meaning rule is the starting point for all IRC interpretation. Courts begin with the
statutory text, giving words their ordinary meaning unless they are technical terms of art with
established tax law definitions. The IRC is highly technical—terms like "recognition," "realization,"
"basis," "amount realized," "capital asset" have meanings that differ from common usage and must be
interpreted according to their tax law definitions.

Ambiguity exists when statutory text is susceptible to multiple reasonable interpretations. Courts
will not manufacture ambiguity to consult legislative history. However, when genuine ambiguity exists,
courts examine: (1) Committee Reports (most authoritative), (2) Floor Statements (less weight),
(3) Earlier bill versions (shows rejected approaches), (4) Treasury regulatory interpretations
(Chevron deference applies if reasonable).

The "absurd result" exception allows departure from plain meaning when literal application produces
results clearly contrary to Congressional intent. But taxpayer-unfavorable outcomes are not "absurd"—
absurdity requires logical impossibility or constitutional violation. Example: literal reading would
tax the same income twice in same year, or exempt all income from tax.

Technical terms test: If IRC uses a term defined elsewhere in the Code (see § 7701 definitions),
that definition controls. If undefined, look to Treasury regulations, then case law, then ordinary
meaning as fallback.
""",
        key_factors=[
            "Presence of statutory definition in § 7701 or section-specific definitions",
            "Term of art with established tax law meaning",
            "Genuine ambiguity vs manufactured ambiguity",
            "Absurdity threshold (logical impossibility)",
            "Available legislative history quality",
            "Treasury regulation alignment with plain meaning",
            "Prior judicial interpretations"
        ],
        primary_authority=["Chevron U.S.A., Inc. v. NRDC, 467 U.S. 837", "United States v. Ron Pair Enterprises, 489 U.S. 235"],
        burden_holder="party arguing against plain meaning",
        adversary_position="Opposing party claims plain meaning is ambiguous or produces absurd result",
        counter_arguments=[
            "Legislative history shows contrary intent",
            "Plain meaning produces taxpayer windfall Congress did not intend",
            "Technical term should have ordinary meaning not tax-specific meaning",
            "Treasury regulation interpretation entitled to Chevron deference overrides plain meaning",
            "Absurdity includes unfair or inequitable results"
        ],
        resolution_strategy="Apply textualism first, invoke ambiguity only with clear evidence, absurdity requires extreme facts",
        entity_scope=["all_entities"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: Supreme Court repeatedly affirmed plain meaning primacy",
        controlling_precedent=["King v. Burwell, 576 U.S. 473", "Hardt v. Reliance Standard Life Ins. Co."],
        issue_category=IssueCategory.STATUTORY_INTERPRETATION
    ),

    DoctrineBlock(
        topic="Cross_Reference_Resolution_IRC",
        keywords=["cross-reference", "see section", "as defined in", "within the meaning of", "pursuant to"],
        conclusion_template=[
            "IRC cross-references must be resolved to their specific hierarchical level.",
            "Circular references are resolved by reading provisions harmoniously.",
            "Forward references to later-enacted sections require temporal analysis."
        ],
        reasoning_framework="""
The IRC contains thousands of cross-references. Proper resolution requires: (1) identifying the
exact provision referenced (full hierarchical path), (2) determining temporal applicability
(was referenced provision in effect for tax year?), (3) checking for circular references,
(4) applying incorporating vs referential distinction.

Incorporating cross-references bring the referenced text into the referencing provision as if
fully set forth. Example: "X applies except as provided in § Y" incorporates Y's exceptions.
Referential cross-references merely point to another provision for guidance without incorporation.
Example: "as defined in § Z" uses Z's definition but doesn't import Z's operative rules.

Circular reference problem: § A says "except as provided in § B" and § B says "subject to § A."
Resolution: read both provisions to give effect to each—typically, § B provides the exception
and § A the general rule, with § B's reference to § A merely acknowledging context.

Forward reference problem: § X enacted 2010 references § Y enacted 2015. Did Congress intend
§ X to incorporate future § Y? Depends on language: "as defined" suggests static reference to
law as it existed when X enacted; "as defined from time to time" or "as in effect" suggests
dynamic reference incorporating later amendments.

Amendment ripple effect: When § Y is amended, does that change § X which references § Y?
Yes for dynamic references, no for static references unless amendment explicitly says it applies
to all referencing provisions.
""",
        key_factors=[
            "Hierarchical precision of reference (section vs subparagraph)",
            "Temporal enactment sequence (which provision came first)",
            "Circular reference presence",
            "Incorporating vs referential language",
            "Static vs dynamic reference indicators",
            "Amendment effective date clauses",
            "Regulatory cross-reference alignment"
        ],
        primary_authority=["IRC § 7806(a)", "26 USC general cross-referencing structure"],
        burden_holder="party claiming cross-reference creates ambiguity",
        adversary_position="Opposing party argues cross-reference is clear and unambiguous",
        counter_arguments=[
            "Circular reference creates irreconcilable conflict requiring legislative history",
            "Forward reference was drafting error not intentional incorporation",
            "Cross-reference is ambiguous requiring Treasury regulation interpretation",
            "Amendment to referenced provision automatically updates all cross-references",
            "Cross-reference incorporates entire referenced section not just cited subsection"
        ],
        resolution_strategy="Map full hierarchical path, check enactment dates, read circularly referenced provisions harmoniously",
        entity_scope=["all_entities"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: well-established principles of statutory cross-referencing",
        controlling_precedent=["National Muffler Dealers Assn. v. United States"],
        issue_category=IssueCategory.CROSS_REFERENCE
    ),

    DoctrineBlock(
        topic="Effective_Date_Provisions_IRC",
        keywords=["effective date", "applies to", "taxable years beginning after", "transactions after", "sunset", "phase-in"],
        conclusion_template=[
            "IRC provisions have specific effective dates controlling temporal application.",
            "Default rule: amendments apply to taxable years ending after enactment date.",
            "Special effective date provisions override the default and must be carefully parsed."
        ],
        reasoning_framework="""
Every IRC amendment has an effective date provision, usually in the enacting legislation's
separate title (e.g., Tax Cuts and Jobs Act § 13001 amends IRC § 162, with effective date in
TCJA § 13001(c)). Three primary effective date formulations:

1. "Taxable years beginning after December 31, 20XX" - cleanest application, entire year under
new law or old law, no proration. Example: TCJA § 11001 rate changes apply to "taxable years
beginning after December 31, 2017" so calendar-year 2018 entirely under new rates.

2. "Amounts paid or incurred after December 31, 20XX" - transaction-level application, single
taxable year may have both old and new law transactions. Requires item-by-item analysis.

3. "Applies to transactions entered into after DATE" - depends on definition of "entered into"
(binding contract date, closing date, or effective date). Regulations or legislative history
usually clarify. Transitional rules may grandfather contracts in existence before enactment.

Phase-in provisions: Some amendments gradually implement changes over multiple years (e.g.,
bonus depreciation phase-down). Each year's percentage must be applied to that year's qualifying
property. Sunset provisions: Amendment expires after specific date, reverting to prior law
(e.g., 2025 TCJA individual provisions sunset December 31, 2025, reverting to pre-TCJA law for
taxable years beginning after that date).

Retroactive amendments: Congress can make IRC changes retroactive to beginning of current calendar
year (within constitutional limits). Taxpayers who filed before retroactive amendment must file
amended returns or claims for refund within statute of limitations (generally 3 years from original
filing or 2 years from tax payment, whichever is later).
""",
        key_factors=[
            "Effective date formulation (taxable year vs transaction vs amount)",
            "Taxpayer fiscal year vs calendar year",
            "Transitional rule presence",
            "Sunset clause existence and date",
            "Phase-in schedule if applicable",
            "Retroactive application scope",
            "Anti-abuse effective date rules"
        ],
        primary_authority=["IRC § 7805(b)", "Pub. L. 115-97 (TCJA) various effective date provisions"],
        burden_holder="taxpayer claiming benefit of new provision or IRS asserting new provision bars deduction",
        adversary_position="Opposing party argues different effective date interpretation",
        counter_arguments=[
            "Transitional rule does not apply to taxpayer's facts",
            "Binding contract exception does not apply (contract not truly binding)",
            "Effective date provision ambiguous, requires interpretation favoring taxpayer or government",
            "Retroactive application exceeds constitutional limits",
            "Phase-in percentage calculation disputed"
        ],
        resolution_strategy="Parse exact effective date language, identify taxpayer's fiscal year, apply transitional rules if present",
        entity_scope=["all_entities"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: effective date provisions are usually explicit",
        controlling_precedent=["United States v. Carlton, 512 U.S. 26 (retroactivity)"],
        issue_category=IssueCategory.EFFECTIVE_DATE
    ),

    DoctrineBlock(
        topic="IRC_Anti_Abuse_Provisions_General",
        keywords=["anti-abuse", "substance over form", "economic substance", "business purpose", "step transaction"],
        conclusion_template=[
            "IRC contains specific statutory anti-abuse rules and general judicial doctrines.",
            "Statutory anti-abuse rules (e.g., § 269) have specific elements and defenses.",
            "Judicial doctrines (economic substance, business purpose, step transaction) overlay the Code."
        ],
        reasoning_framework="""
IRC anti-abuse framework operates at three levels:

1. Specific statutory anti-abuse provisions: § 269 (acquisitions to evade tax), § 482 (transfer
pricing allocations), § 7701(o) (codified economic substance doctrine). These have specific elements,
burdens of proof, and defenses. Example: § 269(a) requires IRS to prove (1) acquisition of control,
(2) principal purpose of tax avoidance. Taxpayer can rebut by showing valid business purpose.

2. General anti-abuse regulations: Treasury regulations contain "anti-abuse rules" for specific
regimes (e.g., Treas. Reg. § 1.701-2 for partnerships). These regulations can recast transactions
that comply literally with statute but violate the regime's purpose. Chevron deference applies if
regulation is reasonable interpretation of statutory grant of authority.

3. Common-law judicial doctrines: Economic substance (transaction must have economic effect beyond
tax benefits), business purpose (must have non-tax business reason), step transaction (collapse
series of steps into single transaction), substance over form (disregard legal form if inconsistent
with economic reality), sham transaction (lacks economic substance entirely). Post-§ 7701(o)
codification, economic substance has two-prong conjunctive test: (1) transaction changes taxpayer's
economic position in meaningful way apart from tax effects, and (2) taxpayer has substantial purpose
for entering transaction apart from tax effects. Both prongs must be satisfied.

Application hierarchy: (1) Check for specific statutory anti-abuse rule first. (2) If none, check
for regulatory anti-abuse rule. (3) If neither, consider common-law doctrines. (4) Burden of proof:
IRS bears initial burden to assert applicability, then burden shifts to taxpayer to prove transaction
has substance/purpose.

Defense strategy: Establish pre-tax profit potential, document business purpose contemporaneously,
avoid overly complex structures that lack commercial justification, ensure transaction has meaningful
risk and real parties dealing at arm's length.
""",
        key_factors=[
            "Presence of specific statutory anti-abuse provision",
            "Regulatory anti-abuse rule applicability",
            "Economic substance prong satisfaction (profit potential)",
            "Business purpose prong satisfaction (non-tax reasons)",
            "Transaction complexity vs commercial rationale",
            "Contemporaneous documentation quality",
            "Arm's length dealing between parties",
            "Pre-tax profit potential quantification"
        ],
        primary_authority=["IRC § 7701(o)", "IRC § 269", "IRC § 482", "Treas. Reg. § 1.701-2"],
        burden_holder="IRS bears initial burden, then shifts to taxpayer",
        adversary_position="IRS argues transaction lacks economic substance or has no business purpose beyond tax avoidance",
        counter_arguments=[
            "Transaction has pre-tax profit potential satisfying economic substance",
            "Non-tax business reasons documented contemporaneously",
            "Specific anti-abuse statute does not apply to these facts",
            "Form chosen is respected under applicable caselaw",
            "Step transaction doctrine does not apply (steps are independent)",
            "Regulatory anti-abuse rule exceeds Treasury's interpretive authority"
        ],
        resolution_strategy="Apply specific statutory rule first, then general doctrines; document business purpose and profit potential",
        entity_scope=["all_entities"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="AGGRESSIVE: anti-abuse application is highly fact-specific and uncertain",
        controlling_precedent=["Gregory v. Helvering, 293 U.S. 465", "Frank Lyon Co. v. United States", "Coltec Industries v. United States"],
        issue_category=IssueCategory.ANTI_ABUSE
    ),

    DoctrineBlock(
        topic="Sunset_Clause_Analysis_IRC",
        keywords=["sunset", "termination date", "expires", "shall not apply", "ceases to be effective"],
        conclusion_template=[
            "Sunset clauses terminate IRC provisions on specified dates.",
            "Post-sunset transactions revert to prior law as it existed before temporary provision.",
            "Transitional rules may apply to transactions straddling sunset date."
        ],
        reasoning_framework="""
Sunset clauses are Congressional budget scoring tools—temporary provisions reduce 10-year revenue
loss projections. Key interpretive issues:

1. Reversion law identification: What law applies after sunset? Usually the law as it existed
immediately before temporary provision enacted, BUT if that prior law itself had sunset, reversion
may go back further. Example: TCJA § 11011 (§ 199A deduction) sunsets December 31, 2025. Post-sunset,
§ 199A ceases to exist, reverting to law as of December 31, 2017 (no § 199A).

2. Sunset date formulation: "Shall not apply to taxable years beginning after December 31, 20XX"
means provision applies for final time to taxable years beginning on or before that date. Calendar-year
taxpayer: 2025 taxable year is last year. Fiscal-year taxpayer ending June 30: fiscal year beginning
July 1, 2025 is last year (ends June 30, 2026 but *began* before December 31, 2025).

3. Straddling transactions: If transaction spans sunset date, may need to allocate between old and
new law. Example: multi-year depreciation deduction with sunset—years before sunset use temporary
provision, years after use permanent law rates.

4. Extension risk: Congress may extend sunset (has done repeatedly with bonus depreciation, R&D
credit, etc.). Extension can be retroactive (filling gap if enacted after sunset) or prospective.
Retroactive extension requires amended returns if taxpayers already filed under post-sunset law.

5. Reliance interests: Taxpayers who enter long-term transactions relying on temporary provisions
bear risk of sunset. No vested right to continuation of tax benefits. Exception: specific grandfather
clauses in sunset provision itself (rare).

Planning considerations: For transactions with long-term tax consequences, model both temporary
provision and post-sunset law to ensure economics work under either scenario. Avoid structures that
collapse catastrophically on sunset.
""",
        key_factors=[
            "Sunset date formulation (taxable year vs transaction date)",
            "Taxpayer fiscal year vs calendar year",
            "Reversion law identification",
            "Straddling transaction allocation methodology",
            "Extension likelihood based on political dynamics",
            "Grandfather clause presence",
            "Long-term transaction exposure to sunset risk"
        ],
        primary_authority=["TCJA Pub. L. 115-97 sunset provisions", "IRC § 168(k) (bonus depreciation sunset history)"],
        burden_holder="taxpayer claiming benefit of temporary provision",
        adversary_position="IRS argues sunset has occurred, temporary provision inapplicable",
        counter_arguments=[
            "Sunset date has not occurred for taxpayer's fiscal year",
            "Transitional rule extends provision beyond nominal sunset date",
            "Extension enacted retroactively covers taxpayer's tax year",
            "Grandfather clause preserves benefit for taxpayer's transaction",
            "Reversion law interpretation favors continued benefit under different provision"
        ],
        resolution_strategy="Parse sunset language precisely, identify reversion law, model both scenarios",
        entity_scope=["all_entities"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: sunset provisions are usually unambiguous as to date",
        controlling_precedent=["Boehner v. Anderson (Congressional authority to sunset provisions)"],
        issue_category=IssueCategory.SUNSET_CLAUSE
    ),

    DoctrineBlock(
        topic="Treasury_Regulation_Hierarchy_IRC",
        keywords=["Treasury regulation", "26 CFR", "legislative regulation", "interpretive regulation", "Chevron deference"],
        conclusion_template=[
            "Treasury regulations interpret IRC and have force of law when validly promulgated.",
            "Legislative regulations (explicit statutory grant) get Chevron deference if reasonable.",
            "Interpretive regulations (general grant) get Chevron deference if not arbitrary/capricious."
        ],
        reasoning_framework="""
Treasury regulations are codified in 26 CFR (Code of Federal Regulations) and come in two types:

1. Legislative (specific statutory grant): IRC explicitly authorizes Treasury to "prescribe regulations"
on specific topic. Example: IRC § 385 authorizes regulations distinguishing debt from equity. These
regulations have force and effect of law. Chevron two-step: (1) Is statute ambiguous? If yes,
(2) Is regulation reasonable interpretation? If yes, regulation controls even if court would have
interpreted differently. Example: "may prescribe regulations" in § 385 grants legislative authority.

2. Interpretive (general grant): IRC § 7805(a) grants Treasury general authority to "prescribe all
needful rules and regulations" for IRC enforcement. Regulations under this general grant interpret
existing statutory language. Post-Loper Bright (2024), Chevron deference overruled—courts independently
interpret IRC using traditional tools, giving regulations Skidmore respect weight based on thoroughness,
consistency, and persuasiveness.

Regulation citation format: Treas. Reg. § 1.162-1 means Income Tax Regulation (1.___) for IRC § 162,
first regulation (-1). Further subdivisions: § 1.162-1(a)(1). Cross-references must be precise.

Temporal rules: Regulations apply prospectively from publication unless IRC or regulation explicitly
states retroactive application. Retroactive regulations can be challenged as exceeding IRC § 7805(b)
limits (general rule: no retroactivity beyond 18 months before proposed regulation publication).

Conflict resolution: If regulation contradicts IRC plain language, statute controls. If regulation
contradicts earlier regulation, later regulation controls (must follow notice-and-comment process).
If regulation is silent on issue, statute controls.

Proposed vs final vs temporary: Proposed regulations are not binding but show Treasury's position.
Temporary regulations (§ 1.162-1T) are immediately effective but must be finalized within 3 years or
expire. Final regulations are fully effective and binding (subject to judicial review).
""",
        key_factors=[
            "Type of regulatory authority (legislative vs interpretive)",
            "Specificity of statutory grant of authority",
            "Regulation's consistency with statutory text",
            "Notice-and-comment process compliance",
            "Retroactivity scope and IRC § 7805(b) compliance",
            "Proposed vs temporary vs final status",
            "Post-Loper Bright Skidmore respect factors"
        ],
        primary_authority=["IRC § 7805", "26 CFR Part 1 (Income Tax Regulations)", "Loper Bright v. Raimondo (2024)"],
        burden_holder="party challenging regulation bears burden to prove invalidity",
        adversary_position="Opposing party argues regulation is invalid, arbitrary, or contrary to statute",
        counter_arguments=[
            "Regulation exceeds statutory grant of authority",
            "Regulation contradicts IRC plain language",
            "Retroactivity violates IRC § 7805(b)",
            "Regulation is arbitrary and capricious",
            "Notice-and-comment process defective",
            "Post-Loper Bright, court should interpret statute independently"
        ],
        resolution_strategy="Identify type of regulation, assess statutory authority scope, evaluate reasonableness",
        entity_scope=["all_entities"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: regulation hierarchy well-established (though Loper Bright shifts analysis)",
        controlling_precedent=["Loper Bright v. Raimondo, 144 S. Ct. 2244 (2024)", "Mayo Foundation v. United States, 562 U.S. 44"],
        issue_category=IssueCategory.REGULATORY_INTEGRATION
    ),

    DoctrineBlock(
        topic="Revenue_Ruling_Authority_Precedential_Value",
        keywords=["revenue ruling", "Rev. Rul.", "IRS guidance", "precedential value", "stare decisis"],
        conclusion_template=[
            "Revenue Rulings are IRS's published positions on how IRC applies to specific facts.",
            "Rev. Ruls. bind IRS but not courts or taxpayers.",
            "Taxpayers may rely on published rulings for penalty protection under IRC § 6664."
        ],
        reasoning_framework="""
Revenue Rulings (Rev. Rul. YY-XXX format, e.g., Rev. Rul. 2023-01) are IRS's official interpretation
of how tax law applies to specific fact patterns. Published in Internal Revenue Bulletin (IRB) and
cumulated in Cumulative Bulletin (C.B.). Hierarchy of IRS guidance:

1. Revenue Rulings (highest IRS authority below regulations): IRS is bound by its own published rulings
and will apply them to all taxpayers with substantially similar facts unless ruling is revoked or
modified by later ruling, regulation, or statute. Taxpayers may rely on favorable rulings for penalty
protection under IRC § 6664(d) (reasonable cause defense) but cannot be bound by unfavorable rulings
(can litigate contrary position).

2. Revenue Procedures (Rev. Proc.): Administrative procedures for dealing with IRS (filing requirements,
deadlines, etc.). Less substantive than Rev. Ruls. but equally binding on IRS for procedures.

3. Private Letter Rulings (PLR): IRS's binding determination for specific taxpayer on specific facts.
IRC § 6110(k)(3): PLRs "may not be used or cited as precedent" by other taxpayers. But can be
persuasive authority showing IRS's general approach to issue. IRS binds itself to taxpayer who
requested PLR but not to others.

4. Chief Counsel Advice (CCA), Technical Advice Memoranda (TAM), Field Service Advice (FSA): Internal
IRS guidance, less precedential than Rev. Ruls. Not citable as precedent by taxpayers but shows IRS
position.

Revenue Ruling structure: (1) Issue section (question presented), (2) Facts section (assumed facts),
(3) Law section (applicable IRC, regulations, caselaw), (4) Analysis section (application of law to
facts), (5) Holding section (conclusion). Taxpayers with identical facts to Rev. Rul. facts can rely
confidently. Different facts require analogical reasoning—more factual differences = less reliability.

Revocation/modification: IRS can revoke or modify revenue rulings prospectively or retroactively
(within IRC § 7805(b) limits). Check IRS.gov for "Actions on Decisions" and superseded ruling lists.
Obsolete rulings lose all authority.
""",
        key_factors=[
            "Revenue Ruling publication status (published vs internal memo)",
            "Factual similarity between ruling facts and taxpayer's facts",
            "Ruling age and obsolescence risk (old rulings may not reflect current law)",
            "Subsequent revocation, modification, or distinguishment",
            "Consistency with regulations and caselaw",
            "Penalty protection reliance requirements",
            "Private Letter Ruling vs Revenue Ruling distinction"
        ],
        primary_authority=["IRC § 6110", "IRC § 6664(d)", "Rev. Proc. 2024-1 (standard procedures)"],
        burden_holder="taxpayer relying on revenue ruling to prove factual similarity",
        adversary_position="IRS or opposing party argues ruling is distinguishable, obsolete, or revoked",
        counter_arguments=[
            "Ruling facts materially different from taxpayer's facts",
            "Ruling revoked or modified by later guidance",
            "Ruling inconsistent with controlling caselaw",
            "Ruling exceeds IRS's interpretive authority (contradicts statute)",
            "Ruling is internal memo not published revenue ruling (no precedential value)",
            "Taxpayer cannot cherry-pick favorable rulings (must apply IRS position consistently)"
        ],
        resolution_strategy="Verify ruling is current and published, compare facts meticulously, check for subsequent guidance",
        entity_scope=["all_entities"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: revenue ruling authority is well-settled",
        controlling_precedent=["Vons Cos. v. United States (PLRs not precedential)", "Rauenhorst v. Commissioner (reliance on rulings)"],
        issue_category=IssueCategory.REVENUE_RULING
    ),

    DoctrineBlock(
        topic="IRC_Definitional_Provisions_Section_7701",
        keywords=["§ 7701", "definition", "includes", "means", "shall be treated as", "for purposes of"],
        conclusion_template=[
            "IRC § 7701 contains definitions applicable to entire Code unless otherwise specified.",
            "'Includes' is term of enlargement, 'means' is term of limitation.",
            "Section-specific definitions override § 7701 general definitions."
        ],
        reasoning_framework="""
IRC § 7701 is the definitional provision for the entire Code. Key interpretive principles:

1. "Means" vs "includes": IRC § 7701 itself says "the term 'includes' and 'including' when used in
a definition shall not be deemed to exclude other things otherwise within the meaning of the term
defined." Translation: "includes" is illustrative not exhaustive—term may encompass more than
listed items. "Means" is limiting—term is restricted to what follows. Example: § 7701(a)(3) "The
term 'corporation' includes associations..." (enlargement—associations ARE corporations for tax
purposes, but other entities may also be corporations). Contrast: "means ABC" restricts definition
to exactly ABC.

2. Hierarchical application: Section-specific definitions override § 7701. Example: § 162 says
"ordinary and necessary business expenses"—"ordinary and necessary" defined by caselaw for § 162
purposes, not by § 7701. But § 7701(a)(1) definition of "person" (includes individuals, corporations,
partnerships, etc.) applies to § 162 unless § 162 says otherwise.

3. "For purposes of" language: Limits definitional scope. "For purposes of this section" means
definition applies only to that section. "For purposes of this subtitle" means definition applies
to entire subtitle (e.g., Subtitle A = Income Taxes). "For purposes of this title" means definition
applies to entire Title 26 (entire IRC). Check scoping language carefully.

4. "Shall be treated as" language: Creates legal fiction. Example: § 7701(a)(30) "The term 'United
States person' means... a citizen or resident of the United States." If statute says "nonresident
alien shall be treated as U.S. person for purposes of § X," that creates fiction only for § X, not
generally.

5. Cross-definitional dependencies: Some § 7701 definitions depend on other definitions. Example:
§ 7701(a)(4) "domestic" depends on § 7701(a)(3) "corporation." Must resolve entire dependency chain.

§ 7701 key definitions: (a)(1) person, (a)(3) corporation, (a)(4) domestic, (a)(9) United States,
(a)(14) taxpayer, (a)(30) United States person, (a)(31) foreign estate, (a)(36) income tax return.
These apply Code-wide unless specifically overridden.
""",
        key_factors=[
            "'Means' vs 'includes' language usage",
            "Section-specific definition presence",
            "'For purposes of' scope limitation",
            "'Shall be treated as' legal fiction scope",
            "Cross-definitional dependency resolution",
            "Regulatory elaboration in 26 CFR § 301.7701",
            "Definitional override explicit statement"
        ],
        primary_authority=["IRC § 7701", "Treas. Reg. § 301.7701-1 through -18"],
        burden_holder="party arguing for non-standard definition",
        adversary_position="Opposing party argues § 7701 definition controls or section-specific definition overrides",
        counter_arguments=[
            "Section-specific definition does not actually override § 7701 (no conflict)",
            "'Includes' language is limiting not illustrative in this context",
            "'For purposes of' scope is broader than opposing party claims",
            "Legal fiction created by 'shall be treated as' extends beyond specified scope",
            "Regulatory definition contradicts § 7701 (regulation invalid)"
        ],
        resolution_strategy="Start with § 7701, check for section-specific override, parse 'means' vs 'includes' carefully",
        entity_scope=["all_entities"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: definitional hierarchy is clear",
        controlling_precedent=["Helvering v. Morgan's Inc. (statutory definitions control)", "Commissioner v. Kowalski"],
        issue_category=IssueCategory.DEFINITIONAL_ANALYSIS
    ),

    DoctrineBlock(
        topic="IRC_Amendment_Tracking_Pub_L_Citations",
        keywords=["Pub. L.", "amendment", "enacted", "revised", "repealed", "added", "stricken"],
        conclusion_template=[
            "IRC amendments are tracked through Public Law (Pub. L.) citations.",
            "Each Pub. L. citation identifies enacting Congress, session, and law number.",
            "Amendments may add, revise, repeal, or strike IRC provisions."
        ],
        reasoning_framework="""
IRC is Title 26 of United States Code. It is amended by public laws (Pub. L. XXX-YYY format where
XXX = Congress number, YYY = law number in that Congress). Example: Pub. L. 115-97 is Tax Cuts and
Jobs Act (115th Congress, 97th law). Amendment tracking requires:

1. Pub. L. citation to amendment: Found in historical notes in USC or commercial tax services (CCH,
RIA, Bloomberg). Shows when provision was added, last amended, or repealed. Example: IRC § 199A
historical note: "Added by Pub. L. 115-97, § 11011(a), Dec. 22, 2017."

2. Amendment type identification:
   - "Added" = new provision created
   - "Amended" = existing provision modified (may change single word or entire subsection)
   - "Revised" = substantial rewrite
   - "Repealed" or "stricken" = provision deleted
   - "Redesignated" = provision renumbered (e.g., subsection (e) becomes subsection (f) when new (e) inserted)

3. Effective date determination: Pub. L. itself contains effective date provision (often in separate
section of enacting statute). Example: Pub. L. 115-97, § 11011(c) says § 199A "applies to taxable
years beginning after December 31, 2017." Must read Pub. L. to find effective date, not just IRC.

4. Prior law reconstruction: To know what law applied for prior years, must trace back through
amendments. Commercial services provide "prior law" versions. IRS.gov has historical versions.
Example: To know what § 162(m) said in 2015, must find pre-TCJA version (before Pub. L. 115-97
amended it).

5. Transitional rules: Some Pub. L.s contain transitional provisions not codified in IRC. Example:
grandfather clauses, special election procedures, one-time filing extensions. These are in Pub. L.
statutory text but not in 26 USC. Must check Pub. L. directly.

Research process: (1) Identify IRC section. (2) Check historical notes for amendment citations.
(3) Pull up Pub. L. text (Congress.gov or commercial service). (4) Find effective date section in
Pub. L. (5) Determine if transitional rules apply. (6) Confirm current law vs prior law.
""",
        key_factors=[
            "Pub. L. citation accuracy (Congress number and law number)",
            "Amendment type (added, amended, repealed, redesignated)",
            "Effective date provision location in Pub. L.",
            "Transitional rule presence",
            "Prior law version availability",
            "Multiple amendments interaction (layered amendments)",
            "Codification vs non-codified provisions"
        ],
        primary_authority=["1 USC § 112 (codification)", "Pub. L. 115-97 (TCJA example)", "Congress.gov"],
        burden_holder="party asserting specific version of law applied to tax year",
        adversary_position="Opposing party argues different version of law or different effective date",
        counter_arguments=[
            "Amendment effective date makes prior law applicable not current law",
            "Transitional rule alters effective date for this taxpayer",
            "Redesignation changed provision numbering—wrong provision cited",
            "Amendment was itself amended before taxpayer's tax year (multiple amendments)",
            "Provision was repealed and later re-enacted with different substance"
        ],
        resolution_strategy="Trace amendment history via historical notes, verify effective dates in Pub. L. text",
        entity_scope=["all_entities"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: amendment tracking is mechanical once Pub. L. citations identified",
        controlling_precedent=["District of Columbia v. Heller (statutory amendment interpretation)"],
        issue_category=IssueCategory.AMENDMENT_TRACKING
    ),

    # Additional 42 doctrine blocks follow similar pattern covering:
    # - IRC parenthetical exceptions and their scope
    # - Conjunction vs disjunction ("and" vs "or") in multi-part tests
    # - Enumeration interpretation (exhaustive vs illustrative lists)
    # - Flush language scope (applies to all subsections vs only last clause)
    # - Penalty provisions and their strict construction
    # - Double taxation prevention principles
    # - Assignment of income doctrine
    # - Constructive receipt doctrine
    # - Claim of right doctrine
    # - Tax benefit rule
    # - Substance over form
    # - Step transaction doctrine
    # - Sham transaction doctrine
    # - Business purpose requirement
    # - Economic substance doctrine (pre and post § 7701(o))
    # - Capitalization vs deduction principles
    # - Clear reflection of income standard
    # - Realization vs recognition distinction
    # - Basis determination principles
    # - Amount realized calculation
    # - Capital asset definition and exceptions
    # - Ordinary income vs capital gain characterization
    # - Timing of income inclusion (cash vs accrual)
    # - Timing of deduction (economic performance)
    # - Related party rules (§ 267, § 707(b))
    # - Attribution rules (constructive ownership)
    # - Statute of limitations (assessment and refund)
    # - Burden of proof allocation
    # - Preparer penalties
    # - Accuracy-related penalties
    # - Substantial understatement penalty
    # - Negligence penalty
    # - Fraud penalty
    # - Reasonable cause defense
    # - Tax shelter disclosure requirements
    # - Listed transaction rules
    # - Reportable transaction rules
    # - Material advisor disclosure
    # - Treaty override provisions
    # - Savings clause in treaties
    # - Tax Court jurisdiction vs District Court vs Claims Court
    # - Judicial deference to IRS (pre and post Loper Bright)

    # For brevity, including 10 more representative doctrine blocks:

    DoctrineBlock(
        topic="IRC_Parenthetical_Exceptions_Scope",
        keywords=["except", "other than", "but not including", "excluding", "parenthetical"],
        conclusion_template=[
            "Parenthetical exceptions narrow the scope of general rules.",
            "Exceptions are strictly construed—only items explicitly excepted are excluded.",
            "Multiple exceptions use 'and' vs 'or' to determine whether all or any must apply."
        ],
        reasoning_framework="""
IRC frequently uses parenthetical exceptions: "X (other than Y)..." or "X (except Z)...".
Interpretation principles:

1. Exception scope: Only what is explicitly stated in exception is excluded from general rule.
Example: § 162(a) allows "ordinary and necessary expenses (other than dividends)..." Dividends are
excluded. Are capital expenditures excluded? Not by this parenthetical—they're excluded by other
provisions (§ 263).

2. Multiple exceptions with "and": ALL conditions must be met to fall within exception. Example:
"(other than property described in § X and property used in Y)" means property must be BOTH described
in § X AND used in Y to be excepted. If only one condition met, exception doesn't apply.

3. Multiple exceptions with "or": ANY condition met triggers exception. Example: "(other than
property described in § X or property used in Y)" means property meeting EITHER condition is excepted.

4. Nested parentheticals: "(X (except Y (other than Z)))..." Work from inside out. Start with
innermost exception, apply outward. Example: "Includes all corporations (except S corporations
(other than S corporations making election under § W))..." Translation: Includes C corps and
S corps that made § W election, excludes S corps without § W election.

5. Exception placement within sentence structure: Parenthetical immediately following term modifies
that term only. Parenthetical at end of clause may modify entire clause or just last term—context
determines scope. Example: "deduction for losses from sales or exchanges of property (other than
capital assets)" suggests "other than capital assets" modifies "property" not "sales or exchanges."
""",
        key_factors=[
            "Explicit exception text (what is specifically excluded)",
            "Conjunction type in multi-part exception (and vs or)",
            "Nested parenthetical depth and sequence",
            "Exception placement (modifies specific term vs entire clause)",
            "Negative implication (expressio unius est exclusio alterius)",
            "Regulatory clarification of exception scope"
        ],
        primary_authority=["IRC general statutory construction", "Bluebook citation standards"],
        burden_holder="party claiming exception applies",
        adversary_position="Opposing party argues exception does not apply or applies more broadly/narrowly",
        counter_arguments=[
            "Exception is illustrative not exhaustive",
            "Multiple exceptions use 'and' but should be read as 'or' based on context",
            "Nested parenthetical scope is ambiguous",
            "Exception modifies entire clause not just preceding term",
            "Regulatory interpretation expands exception beyond statutory text"
        ],
        resolution_strategy="Parse exception text strictly, apply conjunction rules rigidly, resolve nested exceptions inside-out",
        entity_scope=["all_entities"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: grammatical parsing is objective",
        controlling_precedent=["Circuit City Stores v. Adams (exception interpretation)"],
        issue_category=IssueCategory.STATUTORY_INTERPRETATION
    ),

    DoctrineBlock(
        topic="Realization_vs_Recognition_Distinction",
        keywords=["realization", "recognition", "amount realized", "realized gain", "recognized gain"],
        conclusion_template=[
            "Realization occurs when taxpayer engages in transaction crystallizing gain or loss.",
            "Recognition is inclusion of realized gain/loss in gross income or allowed deduction.",
            "Realized but unrecognized gain is deferred, not eliminated (basis preservation)."
        ],
        reasoning_framework="""
Fundamental IRC concepts distinguished:

1. Realization (§ 1001): Occurs when taxpayer disposes of property in exchange for something materially
different. Eisner v. Macomber: realization requires "severance from capital" not mere appreciation.
Amount realized = cash + FMV of property received + liabilities relieved (§ 1001(b)). Realized gain =
amount realized - adjusted basis (§ 1001(a)). Realized loss = adjusted basis - amount realized.

2. Recognition (§ 1001(c) + specific nonrecognition provisions): Recognition is inclusion of realized
gain in gross income or allowance of realized loss as deduction. General rule § 1001(c): all realized
gains/losses are recognized UNLESS specific Code section provides otherwise. Nonrecognition provisions:
§ 1031 (like-kind exchanges), § 351 (corporate formations), § 721 (partnership contributions),
§ 1033 (involuntary conversions), § 121 (home sale exclusion).

3. Deferred gain vs excluded gain: Nonrecognition provisions generally defer gain (will be recognized
later when replacement property sold) by preserving basis. Example: § 1031 exchange of property with
$100K gain—gain not recognized now, but replacement property takes carryover basis ensuring gain
recognized on future sale. Contrast: § 121 home sale exclusion—up to $250K/$500K gain permanently
excluded, not deferred. Basis in new home is cost basis, not carryover.

4. Partial recognition: Some nonrecognition provisions allow partial recognition. Example: § 1031
exchange with boot (cash or non-like-kind property)—boot triggers gain recognition to extent of
boot's FMV, remainder deferred. § 351 with boot—similar rule.

5. Loss nonrecognition: Some provisions (§ 1031, § 351, § 721) also defer realized losses. Taxpayer
cannot recognize loss on like-kind exchange even if economically suffered—loss deferred via carryover
basis. Contrast: § 267 related party loss disallowance—loss is denied, not deferred (related party
buyer can offset with their future gain, but seller never gets loss deduction).
""",
        key_factors=[
            "Disposition of property occurrence (realization event)",
            "Amount realized calculation accuracy",
            "Adjusted basis determination",
            "Specific nonrecognition provision applicability",
            "Boot presence and FMV (partial recognition)",
            "Deferral vs exclusion distinction",
            "Basis preservation mechanism"
        ],
        primary_authority=["IRC § 1001", "IRC § 1031", "IRC § 351", "Eisner v. Macomber, 252 U.S. 189"],
        burden_holder="taxpayer claiming nonrecognition applies",
        adversary_position="IRS argues realization occurred and no nonrecognition provision applies",
        counter_arguments=[
            "No realization event occurred (mere appreciation)",
            "Nonrecognition provision does not apply (requirements not satisfied)",
            "Boot received triggers full recognition not partial",
            "Related party rules deny loss entirely",
            "Basis calculation incorrect (affects future recognition)"
        ],
        resolution_strategy="Identify realization event, calculate amount realized and basis, check for nonrecognition provision",
        entity_scope=["all_entities"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: realization and recognition framework is foundational and well-settled",
        controlling_precedent=["Cottage Savings Assn. v. Commissioner (realization materiality different test)"],
        issue_category=IssueCategory.STATUTORY_INTERPRETATION
    ),

    # Abbreviated additional blocks (real engine would have full 50+ blocks):
    DoctrineBlock(
        topic="Capital_Asset_Definition_IRC_1221",
        keywords=["capital asset", "§ 1221", "ordinary income", "capital gain", "exceptions"],
        conclusion_template=[
            "Capital assets are property held by taxpayer with specific statutory exceptions.",
            "§ 1221(a) lists eight categories of non-capital assets.",
            "Ordinary income characterization generally disfavored absent clear statutory basis."
        ],
        reasoning_framework="IRC § 1221 defines capital assets as property held by taxpayer OTHER THAN eight categories...",
        key_factors=["Property type", "§ 1221(a) exception applicability", "Holding purpose", "Taxpayer's business"],
        primary_authority=["IRC § 1221", "Corn Products Refining Co. v. Commissioner"],
        burden_holder="IRS claiming property is non-capital",
        adversary_position="Taxpayer claims capital asset treatment",
        counter_arguments=["Property is inventory", "Property held for sale to customers", "Hedging transaction"],
        resolution_strategy="Apply § 1221(a) exceptions strictly, presumption favors capital treatment",
        entity_scope=["all_entities"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: capital asset definition is explicit",
        controlling_precedent=["Arkansas Best Corp. v. Commissioner"],
        issue_category=IssueCategory.STATUTORY_INTERPRETATION
    ),

]


def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    """Retrieve doctrine block by exact topic match"""
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic == topic:
            return doctrine
    return None


def search_doctrines_by_keyword(keyword: str) -> List[DoctrineBlock]:
    """Search doctrine cache by keyword"""
    keyword_lower = keyword.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if any(keyword_lower in kw.lower() for kw in doctrine.keywords):
            results.append(doctrine)
    return results


def get_doctrines_by_category(category: IssueCategory) -> List[DoctrineBlock]:
    """Get all doctrines in a specific issue category"""
    return [d for d in DOCTRINE_CACHE if d.issue_category == category]
