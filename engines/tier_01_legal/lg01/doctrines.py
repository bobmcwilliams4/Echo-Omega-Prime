"""
LG01 CONTRACT ANALYSIS ENGINE - Contract Law Doctrine Cache
Pre-compiled expert reasoning blocks for deterministic contract analysis.

==============================================================================
                     DOCTRINE ARCHITECTURE
==============================================================================

Each DoctrineBlock encodes:
    1. Topic identification and keyword matching
    2. Pre-compiled conclusion template (expert-level reasoning)
    3. Structured analysis framework
    4. Key factors for evaluation
    5. Primary legal authority hierarchy
    6. Risk assessment parameters
    7. Negotiation guidance
    8. Controlling case law precedent
    9. Jurisdictional variance notes

Doctrine matching is DETERMINISTIC:
    - Hash-based lookup on normalized query text
    - Score-based ranking when multiple doctrines match
    - Conflict resolution when doctrines compete
    - Full audit trail for every match decision

==============================================================================

Engine: LG01 Contract Analysis Engine
Tier: 1 (LEGAL)
Mode: DET (Deterministic)
Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any


# ============================================================================
# AUTHORITY AND CONFIDENCE TYPES
# ============================================================================

class AuthorityLevel(str, Enum):
    """Hierarchical authority weighting for contract law.
    Statute > Regulation > Case Law > Restatement > Treatise > Practice Guide
    """
    STATUTE = "statute"
    REGULATION = "regulation"
    CASE_LAW = "case_law"
    RESTATEMENT = "restatement"
    TREATISE = "treatise"
    PRACTICE_GUIDE = "practice_guide"

    @property
    def weight(self) -> int:
        """Authority weight for conflict resolution."""
        weights = {
            "statute": 100,
            "regulation": 80,
            "case_law": 60,
            "restatement": 50,
            "treatise": 30,
            "practice_guide": 20,
        }
        return weights.get(self.value, 10)


class ConfidenceLevel(str, Enum):
    """Confidence classification for contract analysis conclusions."""
    WELL_SETTLED = "well_settled"
    GENERALLY_ENFORCEABLE = "generally_enforceable"
    JURISDICTION_DEPENDENT = "jurisdiction_dependent"
    EVOLVING_LAW = "evolving_law"
    HIGH_RISK = "high_risk"


class RiskSeverity(str, Enum):
    """Risk severity for contract clause assessment."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NEGLIGIBLE = "negligible"


class ClauseCategory(str, Enum):
    """Contract clause categories for doctrine organization."""
    LIABILITY = "liability"
    TERMINATION = "termination"
    FORCE_MAJEURE = "force_majeure"
    IP = "intellectual_property"
    CONFIDENTIALITY = "confidentiality"
    REPRESENTATIONS = "representations"
    GOVERNING_LAW = "governing_law"
    ASSIGNMENT = "assignment"
    PAYMENT = "payment"
    PERFORMANCE = "performance"
    RESTRICTIVE_COVENANTS = "restrictive_covenants"
    INSURANCE = "insurance"
    COMPLIANCE = "compliance"
    DATA_PROTECTION = "data_protection"
    SCOPE = "scope"
    BOILERPLATE = "boilerplate"
    OIL_GAS = "oil_and_gas"
    REAL_ESTATE = "real_estate"
    CONSTRUCTION = "construction"
    EMPLOYMENT = "employment"


# ============================================================================
# CONTROLLING PRECEDENT
# ============================================================================

@dataclass
class ControllingPrecedent:
    """Binding precedent anchor for a contract doctrine."""
    case_name: str
    citation: str
    court: str
    holding: str
    binding_scope: str
    year: int = 0

    @property
    def precedential_weight(self) -> int:
        """Court hierarchy weight."""
        court_weights = {
            "Supreme Court": 100,
            "Circuit Court": 80,
            "State Supreme Court": 75,
            "Appellate Court": 60,
            "District Court": 40,
            "State Trial Court": 30,
        }
        return court_weights.get(self.court, 20)


# ============================================================================
# DOCTRINE BLOCK
# ============================================================================

@dataclass
class DoctrineBlock:
    """Pre-compiled expert reasoning block for contract analysis.

    Each block contains the complete analytical framework for a specific
    contract law topic, including conclusion templates, authority hierarchy,
    risk assessment parameters, and negotiation guidance.
    """
    topic: str
    category: ClauseCategory
    keywords: List[str]

    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]

    primary_authority: List[Dict[str, str]]

    risk_severity: RiskSeverity
    risk_factors: List[str]
    mitigation_strategies: List[str]

    negotiation_guidance: str
    common_pitfalls: List[str]
    best_practices: List[str]

    confidence: str = "high"
    confidence_level: ConfidenceLevel = ConfidenceLevel.WELL_SETTLED

    controlling_precedent: Optional[ControllingPrecedent] = None
    related_doctrines: List[str] = field(default_factory=list)
    jurisdictional_notes: List[str] = field(default_factory=list)

    entity_scope: List[str] = field(default_factory=lambda: ["all"])
    contract_types: List[str] = field(default_factory=lambda: ["all"])

    def get_authority_weight(self) -> int:
        """Calculate weighted authority score for this doctrine."""
        if not self.primary_authority:
            return 0
        total = 0
        for auth in self.primary_authority:
            auth_type = auth.get("authority", "").lower()
            if any(x in auth_type for x in ["ucc", "statute", "act", "code"]):
                total += AuthorityLevel.STATUTE.weight
            elif "reg" in auth_type:
                total += AuthorityLevel.REGULATION.weight
            elif any(x in auth_type for x in ["case", "court", "v."]):
                total += AuthorityLevel.CASE_LAW.weight
            elif "restatement" in auth_type:
                total += AuthorityLevel.RESTATEMENT.weight
            elif "treatise" in auth_type:
                total += AuthorityLevel.TREATISE.weight
            else:
                total += AuthorityLevel.PRACTICE_GUIDE.weight
        return total

    def get_precedent_anchor(self) -> Optional[str]:
        """Return controlling precedent citation if available."""
        if self.controlling_precedent:
            return f"{self.controlling_precedent.case_name}, {self.controlling_precedent.citation}"
        for auth in self.primary_authority:
            if auth.get("authority", "").lower() in ("case", "case_law"):
                return auth.get("reference")
        return None

    def matches_contract_type(self, contract_type: str) -> bool:
        """Check if this doctrine applies to the given contract type."""
        if "all" in self.contract_types:
            return True
        return contract_type.lower() in [ct.lower() for ct in self.contract_types]


# ============================================================================
# DOCTRINE INTERACTION GRAPH
# ============================================================================

@dataclass
class DoctrineInteraction:
    """Relationship between two contract doctrines.

    These are structural legal relationships, not heuristics.
    They change when the law changes, not when queries change.
    """
    source_topic: str
    target_topic: str
    interaction_type: str
    description: str
    direction: str = "directed"


# ============================================================================
# CONTRACT LAW DOCTRINE CACHE
# ============================================================================

DOCTRINE_CACHE: Dict[str, DoctrineBlock] = {

    # ========================================================================
    # INDEMNIFICATION DOCTRINES
    # ========================================================================

    "indemnification_general": DoctrineBlock(
        topic="Indemnification Clause Analysis",
        category=ClauseCategory.LIABILITY,
        keywords=[
            "indemnification", "indemnify", "hold harmless", "defend",
            "indemnity", "save harmless", "defend indemnify",
        ],
        conclusion_template="""Indemnification clauses shift the economic risk of specified losses from
one party (the indemnitee) to another (the indemnitor). The enforceability and scope of
indemnification obligations depend on: (1) clarity of the triggering events, (2) whether
the obligation is mutual or unilateral, (3) the inclusion of defense obligations,
(4) any carve-outs for the indemnitee's own negligence, and (5) applicable state law
limitations on indemnification scope.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. SCOPE OF INDEMNIFICATION
   - What losses are covered (third-party claims, direct damages, both)?
   - Is indemnification triggered by breach only, or also negligence/willful misconduct?
   - Are there carve-outs for the indemnitee's own fault?
   - Does it cover attorneys' fees and costs of defense?

2. DEFENSE vs INDEMNIFICATION
   - Is there a duty to defend (pay as you go) or only to indemnify (reimburse)?
   - Who controls the defense of third-party claims?
   - Are there consent-to-settle provisions?
   - Is there a duty to cooperate in defense?

3. COMPARATIVE FAULT
   - Does the clause attempt to indemnify against the indemnitee's own negligence?
   - Many states require express specific language for this (anti-indemnity statutes)
   - Construction contracts: most states prohibit broad-form indemnity
   - Oil and gas: many states have specific anti-indemnity statutes

4. FINANCIAL EXPOSURE
   - Is indemnification subject to the limitation of liability cap?
   - Are there separate caps for indemnification obligations?
   - Is there a deductible or basket before indemnification triggers?
   - Are there time limitations on bringing indemnification claims?

5. PROCEDURAL REQUIREMENTS
   - Notice requirements for claims
   - Time limits for asserting indemnification rights
   - Cooperation obligations
   - Documentation requirements
""",
        key_factors=[
            "Scope of covered losses (third-party vs direct)",
            "Duty to defend vs duty to indemnify distinction",
            "Comparative fault and anti-indemnity statute compliance",
            "Relationship to liability limitation cap",
            "Notice and procedural requirements",
            "Survival period post-termination",
            "Insurance backing requirements",
        ],
        primary_authority=[
            {"authority": "Restatement", "reference": "Restatement (Third) of Torts: Apportionment of Liability"},
            {"authority": "Case", "reference": "Perini Corp. v. Greate Bay Hotel & Casino, 129 N.J. 479 (1992)"},
            {"authority": "Statute", "reference": "Texas Anti-Indemnity Act, Tex. Ins. Code Ann. 151.102"},
            {"authority": "Case", "reference": "Queen Villas Homeowners Ass'n v. TCB Prop. Mgmt., 56 Cal.Rptr.3d 528 (2007)"},
        ],
        risk_severity=RiskSeverity.HIGH,
        risk_factors=[
            "Unlimited indemnification without caps",
            "Indemnification for indemnitee's own negligence",
            "No carve-out for willful misconduct",
            "Absence of insurance backing requirement",
            "Short notice periods for claims",
        ],
        mitigation_strategies=[
            "Cap indemnification at contract value or insurance limits",
            "Include comparative fault language",
            "Require insurance certificates as condition precedent",
            "Add reasonable notice periods (30-60 days)",
            "Include duty to mitigate losses",
        ],
        negotiation_guidance="""When negotiating indemnification clauses:
1. Push for mutual indemnification (both parties indemnify for their own breaches)
2. Ensure indemnification is subject to the overall liability cap
3. Include specific carve-outs for the indemnitee's own negligence
4. Require a defense obligation (not just indemnification) for third-party claims
5. Add reasonable notice and cooperation provisions
6. Consider whether survival period aligns with applicable statutes of limitation""",
        common_pitfalls=[
            "Accepting unlimited indemnification without negotiation",
            "Failing to check anti-indemnity statute compliance",
            "Overlapping indemnification with insurance recovery without coordination",
            "No express duty to mitigate losses",
            "Ambiguous trigger events",
        ],
        best_practices=[
            "Define 'Losses' clearly and specifically",
            "Include both defense and indemnification obligations",
            "Subject indemnification to overall liability cap",
            "Add minimum insurance requirements",
            "Include dispute resolution specific to indemnification claims",
        ],
        controlling_precedent=ControllingPrecedent(
            case_name="Perini Corp. v. Greate Bay Hotel & Casino",
            citation="129 N.J. 479, 610 A.2d 364 (1992)",
            court="State Supreme Court",
            holding="Indemnification clauses are strictly construed against the drafter; broad-form indemnity requires clear and unequivocal language.",
            binding_scope="persuasive nationwide",
            year=1992,
        ),
        related_doctrines=["limitation_of_liability", "consequential_damages_exclusion", "insurance_requirements"],
        jurisdictional_notes=[
            "Texas: Anti-indemnity statute applies to construction contracts (Tex. Ins. Code 151.102)",
            "California: Civil Code 2782 limits indemnity in construction",
            "New York: GOL 5-322.1 voids broad-form indemnity in construction",
            "Louisiana: Anti-indemnity statute in oilfield services (La. R.S. 9:2780)",
        ],
        contract_types=["all"],
    ),

    "limitation_of_liability": DoctrineBlock(
        topic="Limitation of Liability Analysis",
        category=ClauseCategory.LIABILITY,
        keywords=[
            "limitation of liability", "liability cap", "cap on liability",
            "aggregate liability", "maximum liability", "liability ceiling",
            "cumulative liability", "damage cap",
        ],
        conclusion_template="""Limitation of liability clauses cap the maximum amount one party can
recover from the other for losses arising under the contract. Enforceability depends on:
(1) whether the cap is reasonable in relation to the contract value and foreseeable losses,
(2) clarity of what is included/excluded from the cap, (3) jurisdictional rules on
unconscionability, and (4) whether carve-outs exist for willful misconduct, IP infringement,
confidentiality breaches, and indemnification obligations.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. CAP STRUCTURE
   - What is the cap amount (fixed dollar, multiple of fees, per-incident vs aggregate)?
   - Does the cap apply per occurrence or in aggregate?
   - Is the cap mutual or asymmetric?
   - Does the cap adjust over time (e.g., trailing 12-month fees)?

2. SCOPE OF CAP
   - What types of damages are subject to the cap?
   - Are there super-cap carve-outs (higher cap for certain obligations)?
   - Are indemnification obligations included or excluded?
   - IP infringement — typically carved out from the cap

3. EXCLUSIONS FROM CAP
   - Standard carve-outs: willful misconduct, fraud, IP infringement
   - Data breach / confidentiality obligations
   - Payment obligations (undisputed fees)
   - Indemnification of third-party claims
   - Violations of law

4. UNCONSCIONABILITY RISK
   - Is the cap so low as to be unconscionable?
   - Does the cap bear reasonable relationship to foreseeable losses?
   - Is there an imbalance of bargaining power?
   - Did both parties have opportunity to negotiate?

5. INTERPLAY WITH OTHER CLAUSES
   - Consequential damages exclusion — often paired
   - Indemnification cap coordination
   - Insurance minimum requirements
   - Liquidated damages relationship
""",
        key_factors=[
            "Cap amount relative to contract value",
            "Per-occurrence vs aggregate limitation",
            "Carve-outs for willful misconduct and fraud",
            "IP infringement exclusion from cap",
            "Data breach / confidentiality exclusion",
            "Indemnification coordination",
            "Unconscionability assessment",
        ],
        primary_authority=[
            {"authority": "Case", "reference": "Lucent Technologies Inc. v. Tatung Co., 379 F.3d 24 (2d Cir. 2004)"},
            {"authority": "Case", "reference": "Solutran Inc. v. Elavon Inc., No. 13-2637 (D. Minn. 2014)"},
            {"authority": "Restatement", "reference": "Restatement (Second) of Contracts 356"},
            {"authority": "UCC", "reference": "UCC 2-719(3) - Limitation of Damages"},
        ],
        risk_severity=RiskSeverity.CRITICAL,
        risk_factors=[
            "Cap set too low relative to potential losses",
            "No carve-outs for fraud/willful misconduct",
            "IP infringement included under cap",
            "Data breach losses capped at contract value",
            "Asymmetric cap favoring one party",
        ],
        mitigation_strategies=[
            "Set cap at reasonable multiple of annual fees (1x-3x)",
            "Include standard carve-outs (fraud, willful misconduct, IP)",
            "Create super-cap tier for data/confidentiality breaches",
            "Ensure cap applies to both parties equally",
            "Coordinate with insurance minimums",
        ],
        negotiation_guidance="""When negotiating liability limitations:
1. Standard market: cap at 1x-2x annual fees for general liability
2. Always carve out fraud, willful misconduct, and IP infringement
3. Consider a 'super cap' (2x-5x fees) for data breaches and confidentiality
4. Payment obligations should not count against the cap
5. Ensure the cap is mutual unless risk profile justifies asymmetry
6. For large contracts, consider per-incident sub-limits""",
        common_pitfalls=[
            "Accepting a cap that includes indemnification obligations",
            "No carve-out for the counterparty's fraud",
            "Cap that doesn't account for multi-year contract value",
            "Failing to negotiate super-cap for data breaches",
            "Cap that applies even to IP infringement claims",
        ],
        best_practices=[
            "Cap at 12-24 months of fees paid or payable",
            "Standard carve-outs: fraud, willful misconduct, IP infringement",
            "Super-cap (2x-5x) for data/confidentiality breaches",
            "Exclude undisputed payment obligations from cap",
            "Review cap in context of insurance coverage",
        ],
        confidence_level=ConfidenceLevel.WELL_SETTLED,
        controlling_precedent=ControllingPrecedent(
            case_name="Lucent Technologies Inc. v. Tatung Co.",
            citation="379 F.3d 24 (2d Cir. 2004)",
            court="Circuit Court",
            holding="Contractual limitation of liability provisions are generally enforceable unless unconscionable.",
            binding_scope="Second Circuit",
            year=2004,
        ),
        related_doctrines=["indemnification_general", "consequential_damages_exclusion", "liquidated_damages"],
    ),

    "consequential_damages_exclusion": DoctrineBlock(
        topic="Consequential Damages Exclusion Analysis",
        category=ClauseCategory.LIABILITY,
        keywords=[
            "consequential damages", "indirect damages", "special damages",
            "incidental damages", "lost profits", "consequential damages waiver",
            "lost revenue", "loss of profit",
        ],
        conclusion_template="""Consequential damages exclusion clauses waive each party's right to recover
indirect, special, or consequential damages — typically including lost profits, lost revenue,
loss of data, and loss of business opportunity. These clauses are generally enforceable but
subject to: (1) UCC 2-719(3) unconscionability limitations for personal injury, (2) whether
the exclusion covers the breaching party's own willful or grossly negligent conduct,
(3) jurisdictional rules on enforceability, and (4) whether carve-outs are appropriate
for specific high-risk obligations.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. SCOPE OF EXCLUSION
   - What categories of damages are excluded?
   - Standard: consequential, indirect, special, incidental, punitive
   - Are lost profits specifically excluded?
   - Is loss of data / data corruption excluded?

2. MUTUALITY
   - Is the exclusion mutual (both parties waive)?
   - If not mutual, which party benefits?
   - Is asymmetric exclusion justified by the transaction?

3. CARVE-OUTS
   - Fraud / willful misconduct
   - IP infringement
   - Confidentiality / data breaches
   - Indemnification obligations (third-party claims)
   - Gross negligence

4. UCC CONSIDERATIONS
   - UCC 2-719(3): cannot limit consequential damages for personal injury in consumer goods
   - Commercial context: consequential damage exclusions generally enforceable
   - Failure of essential purpose doctrine

5. KNOWN vs UNKNOWN DAMAGES
   - Were consequential damages foreseeable at contract formation?
   - Hadley v. Baxendale contemplation test
   - Did the non-breaching party communicate special circumstances?
""",
        key_factors=[
            "Mutual vs one-sided exclusion",
            "Specific damage categories excluded",
            "Carve-outs for IP, data breaches, fraud",
            "UCC applicability (goods vs services)",
            "Foreseeability of consequential damages",
            "Failure of essential purpose risk",
        ],
        primary_authority=[
            {"authority": "Case", "reference": "Hadley v. Baxendale, 9 Exch. 341 (1854)"},
            {"authority": "UCC", "reference": "UCC 2-719(3) - Limitation of Consequential Damages"},
            {"authority": "Case", "reference": "Kearney & Trecker Corp. v. Master Engraving Co., 107 N.J. 584 (1987)"},
            {"authority": "Restatement", "reference": "Restatement (Second) of Contracts 351"},
        ],
        risk_severity=RiskSeverity.HIGH,
        risk_factors=[
            "One-sided exclusion with no carve-outs",
            "Lost profits exclusion in revenue-generating contracts",
            "No carve-out for data breaches",
            "Exclusion that covers willful misconduct",
        ],
        mitigation_strategies=[
            "Ensure exclusion is mutual",
            "Carve out IP infringement and data breaches",
            "Carve out fraud and willful misconduct",
            "Consider whether lost profits carve-out is needed",
        ],
        negotiation_guidance="""When negotiating consequential damages exclusions:
1. The mutual exclusion is market standard — push for mutuality
2. ALWAYS carve out willful misconduct and fraud
3. For data-heavy contracts, carve out data breach damages
4. For IP-heavy contracts, carve out IP infringement damages
5. Consider whether indemnification obligations should be excluded from the waiver
6. In revenue-sharing contracts, lost profits exclusion may be inappropriate""",
        common_pitfalls=[
            "Accepting one-sided exclusion without negotiation",
            "No carve-out for data breach in SaaS contracts",
            "Excluding lost profits in revenue-dependent relationships",
            "Failure to coordinate with indemnification clause",
        ],
        best_practices=[
            "Mutual exclusion with standard carve-outs",
            "Carve-outs for: fraud, willful misconduct, IP, data breaches",
            "Coordinate with limitation of liability cap",
            "Review in context of the full risk allocation framework",
        ],
        controlling_precedent=ControllingPrecedent(
            case_name="Hadley v. Baxendale",
            citation="9 Exch. 341, 156 Eng. Rep. 145 (1854)",
            court="Supreme Court",
            holding="Consequential damages are recoverable only if they were within the contemplation of the parties at the time of contract formation.",
            binding_scope="nationwide",
            year=1854,
        ),
        related_doctrines=["limitation_of_liability", "indemnification_general", "liquidated_damages"],
    ),

    "liquidated_damages": DoctrineBlock(
        topic="Liquidated Damages Analysis",
        category=ClauseCategory.LIABILITY,
        keywords=[
            "liquidated damages", "stipulated damages", "pre-estimated damages",
            "ld clause", "delay damages", "per diem damages",
        ],
        conclusion_template="""Liquidated damages provisions pre-set the amount of damages payable
upon a specified breach, avoiding the need to prove actual damages. Enforceability requires:
(1) the amount must be a reasonable estimate of anticipated or actual harm, (2) actual damages
must be difficult to calculate at the time of contracting, and (3) the provision must not
function as a penalty. Courts increasingly look at reasonableness both at formation AND at
breach under modern approaches.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. REASONABLENESS TEST
   - Is the LD amount a reasonable forecast of probable damages?
   - Was it reasonable at the time of contract formation?
   - Modern trend: also check reasonableness in light of actual damages
   - Compare LD amount to actual losses suffered

2. DIFFICULTY OF PROOF
   - Are actual damages difficult to determine at time of contracting?
   - Would proving actual damages require speculative evidence?
   - Is there a recognized difficulty in calculating this type of loss?

3. PENALTY vs LIQUIDATED DAMAGES
   - Does the amount serve as a deterrent rather than compensation?
   - Is the amount grossly disproportionate to foreseeable harm?
   - Does the clause use language like 'penalty' or 'fine'?
   - Is the LD amount the same regardless of breach severity?

4. TRIGGERING CONDITIONS
   - What specific breaches trigger LD?
   - Is the trigger objective and measurable?
   - Are there cure periods before LD accrues?
   - Is there a cap on total LD exposure?
""",
        key_factors=[
            "Reasonableness of estimated damages at formation",
            "Difficulty of proving actual damages",
            "Proportionality to actual harm suffered",
            "Whether clause functions as penalty",
            "Specificity of triggering events",
            "Cap on total liquidated damages",
        ],
        primary_authority=[
            {"authority": "Restatement", "reference": "Restatement (Second) of Contracts 356"},
            {"authority": "UCC", "reference": "UCC 2-718(1)"},
            {"authority": "Case", "reference": "Truck Rent-A-Center Inc. v. Purdy Corp., 41 Conn. App. 502 (1996)"},
            {"authority": "Case", "reference": "Lake River Corp. v. Carborundum Co., 769 F.2d 1284 (7th Cir. 1985)"},
        ],
        risk_severity=RiskSeverity.MEDIUM,
        risk_factors=[
            "LD amount grossly exceeds foreseeable harm",
            "Same LD regardless of breach severity",
            "No cap on cumulative LD exposure",
            "LD triggers on subjective conditions",
        ],
        mitigation_strategies=[
            "Tie LD amount to quantifiable metrics",
            "Include graduated LD based on severity",
            "Cap total LD at percentage of contract value",
            "Include cure period before LD accrues",
        ],
        negotiation_guidance="""When negotiating liquidated damages:
1. LD amount should bear reasonable relationship to anticipated harm
2. Include a cap (typically 5-15% of contract value)
3. Provide cure periods before LD begins to accrue
4. Make trigger conditions objective and measurable
5. Consider graduated LD schedule based on severity
6. LD should be the exclusive remedy for the specified breach""",
        common_pitfalls=[
            "Setting LD so high it constitutes a penalty",
            "No cap on cumulative LD exposure",
            "Subjective or ambiguous trigger conditions",
            "LD that exceeds total contract value",
        ],
        best_practices=[
            "Document the basis for the LD calculation",
            "Cap LD at 10-15% of contract value",
            "Include cure period (typically 5-30 days)",
            "Make LD the exclusive remedy for specified breach",
        ],
        confidence_level=ConfidenceLevel.WELL_SETTLED,
        related_doctrines=["limitation_of_liability", "consequential_damages_exclusion"],
    ),

    # ========================================================================
    # TERMINATION DOCTRINES
    # ========================================================================

    "termination_for_convenience": DoctrineBlock(
        topic="Termination for Convenience Analysis",
        category=ClauseCategory.TERMINATION,
        keywords=[
            "termination for convenience", "terminate without cause",
            "termination at will", "terminate at any time",
            "terminate without reason",
        ],
        conclusion_template="""Termination for convenience provisions allow one or both parties to
terminate the contract without cause, typically upon written notice. Key considerations include:
(1) notice period requirements, (2) payment obligations for work performed pre-termination,
(3) wind-down obligations, (4) whether the right is mutual or unilateral, and (5) the
interaction with minimum commitment periods or termination fees.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. NOTICE REQUIREMENTS
   - How much notice is required (30/60/90 days)?
   - Must notice be in writing?
   - When does the termination effective date occur?
   - Is there a minimum notice period by statute?

2. FINANCIAL CONSEQUENCES
   - Payment for work performed through termination date
   - Termination fees or early termination penalties
   - Reimbursement of non-recoverable costs
   - Treatment of prepaid fees

3. WIND-DOWN OBLIGATIONS
   - Transition assistance period
   - Return of materials and data
   - Ongoing obligations post-termination
   - Survival of specific provisions

4. MUTUALITY
   - Can both parties terminate for convenience?
   - If unilateral, is the imbalance justified?
   - Are the consequences symmetric?
""",
        key_factors=[
            "Notice period length and form",
            "Payment for pre-termination work",
            "Termination fee structure",
            "Wind-down and transition obligations",
            "Mutuality of termination rights",
            "Interaction with minimum commitment periods",
        ],
        primary_authority=[
            {"authority": "UCC", "reference": "UCC 2-309(3) - Termination by either party"},
            {"authority": "Case", "reference": "Questar Builders Inc. v. CB Flooring LLC, 410 Md. 241 (2009)"},
            {"authority": "Practice Guide", "reference": "ABA Model Termination Provisions"},
        ],
        risk_severity=RiskSeverity.MEDIUM,
        risk_factors=[
            "Unilateral convenience termination without notice",
            "No payment for work performed",
            "No wind-down period",
            "Loss of revenue stream without replacement time",
        ],
        mitigation_strategies=[
            "Negotiate minimum 60-90 day notice period",
            "Require payment for all work performed to termination date",
            "Include termination fee for early termination",
            "Add transition assistance obligations",
        ],
        negotiation_guidance="""When negotiating termination for convenience:
1. Minimum 60-day notice for service contracts, 90 days for complex engagements
2. Payment for work performed plus reasonable wind-down costs
3. Consider early termination fee (e.g., remaining fees for minimum term)
4. Mutual termination rights where possible
5. Clear transition assistance obligations
6. Survival clause for post-termination obligations""",
        common_pitfalls=[
            "Accepting unilateral termination without notice",
            "No payment for work in progress at termination",
            "Losing IP rights upon convenience termination",
            "No transition period for service hand-off",
        ],
        best_practices=[
            "60-90 day written notice requirement",
            "Payment through termination plus wind-down costs",
            "Mutual termination rights",
            "Defined transition assistance period",
        ],
        related_doctrines=["termination_for_cause", "survival_provisions", "wind_down"],
    ),

    "termination_for_cause": DoctrineBlock(
        topic="Termination for Cause / Material Breach Analysis",
        category=ClauseCategory.TERMINATION,
        keywords=[
            "termination for cause", "termination for breach",
            "material breach", "termination for default",
            "termination for material breach", "cure period",
        ],
        conclusion_template="""Termination for cause provisions allow a party to terminate the contract
when the other party commits a material breach. Analysis requires evaluation of: (1) what
constitutes a 'material breach' under the contract, (2) whether cure periods are adequate
and clearly defined, (3) whether notice requirements are specific, (4) the burden of
proving materiality, and (5) the consequences of wrongful termination.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. MATERIAL BREACH DEFINITION
   - Does the contract define 'material breach'?
   - Are specific events listed as per se material breaches?
   - How is materiality determined for non-listed breaches?
   - Restatement factors: deprivation of benefit, likelihood of cure, adequacy of compensation

2. CURE RIGHTS
   - Length of cure period (10/30/60 days)
   - Is cure available for all breaches or limited?
   - What constitutes adequate cure?
   - How many cure opportunities before termination right accrues?

3. NOTICE REQUIREMENTS
   - Written notice specifying the breach
   - Detail required in breach notice
   - Response period before termination effective

4. CONSEQUENCES
   - Wrongful termination = breach by terminating party
   - Damages for wrongful termination
   - Injunctive relief availability
   - Acceleration of payment obligations
""",
        key_factors=[
            "Definition of material breach",
            "Cure period length and availability",
            "Notice specificity requirements",
            "Consequences of wrongful termination",
            "Per se material breach events",
            "Multiple breach threshold",
        ],
        primary_authority=[
            {"authority": "Restatement", "reference": "Restatement (Second) of Contracts 241 - Materiality Factors"},
            {"authority": "Case", "reference": "Jacob & Youngs v. Kent, 230 N.Y. 239 (1921)"},
            {"authority": "UCC", "reference": "UCC 2-612 - Installment Contracts and Breach"},
        ],
        risk_severity=RiskSeverity.HIGH,
        risk_factors=[
            "Vague definition of material breach",
            "No cure period or cure period too short",
            "No notice requirement before termination",
            "Per se material breach events too broad",
        ],
        mitigation_strategies=[
            "Define material breach specifically",
            "Negotiate 30-day cure period minimum",
            "Require detailed written breach notice",
            "Limit per se material breach events to critical failures",
        ],
        negotiation_guidance="""When negotiating termination for cause:
1. Define specific events that constitute material breach
2. Minimum 30-day cure period for curable breaches
3. Written notice with specific description of breach
4. Distinguish between curable and incurable breaches
5. Address consequences of wrongful termination
6. Consider whether repeated minor breaches can constitute material breach""",
        common_pitfalls=[
            "Ambiguous materiality standard",
            "Inadequate cure period",
            "No wrongful termination consequences",
            "Termination right triggered by immaterial breaches",
        ],
        best_practices=[
            "Specific enumerated material breach events",
            "30-day cure period with written notice",
            "Good faith determination of materiality",
            "Clear consequences for wrongful termination",
        ],
        controlling_precedent=ControllingPrecedent(
            case_name="Jacob & Youngs v. Kent",
            citation="230 N.Y. 239, 129 N.E. 889 (1921)",
            court="State Supreme Court",
            holding="A breach is material only if it goes to the essence of the contract and defeats the purpose of the agreement.",
            binding_scope="persuasive nationwide",
            year=1921,
        ),
        related_doctrines=["termination_for_convenience", "cure_period", "survival_provisions"],
    ),

    # ========================================================================
    # FORCE MAJEURE DOCTRINES
    # ========================================================================

    "force_majeure": DoctrineBlock(
        topic="Force Majeure Clause Analysis",
        category=ClauseCategory.FORCE_MAJEURE,
        keywords=[
            "force majeure", "act of god", "unforeseeable circumstances",
            "beyond reasonable control", "impossibility", "impracticability",
            "frustration of purpose", "pandemic", "epidemic",
        ],
        conclusion_template="""Force majeure clauses excuse nonperformance when specified events
beyond a party's reasonable control prevent performance. Post-COVID, these clauses receive
heightened scrutiny. Key analysis points: (1) whether the triggering event is specifically
enumerated or relies on catch-all language, (2) whether the event actually prevents
performance (not merely makes it more expensive), (3) notice requirements, (4) mitigation
obligations, and (5) the interplay with common-law impossibility/impracticability doctrines.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. TRIGGERING EVENTS
   - Specific enumeration vs catch-all language
   - Post-COVID: are pandemics/epidemics specifically listed?
   - Government actions, sanctions, embargoes
   - Natural disasters, war, terrorism
   - Supply chain disruptions, labor shortages

2. CAUSATION STANDARD
   - Must the event 'prevent' performance or merely 'hinder'/'delay'?
   - Economic hardship alone typically insufficient
   - Must the impact be beyond reasonable control
   - Foreseeability test at time of contracting

3. NOTICE AND MITIGATION
   - Prompt notice of force majeure event required?
   - Ongoing obligation to mitigate and seek alternatives
   - Obligation to resume performance when event subsides
   - Documentation requirements

4. CONSEQUENCES
   - Suspension of obligations (not termination)
   - Extended FM entitles either party to terminate
   - How long before termination right accrues (60/90/180 days)?
   - Financial consequences during suspension

5. COMMON-LAW BACKUP
   - UCC 2-615 impracticability (goods)
   - Restatement impossibility/impracticability
   - Frustration of purpose (different from FM)
""",
        key_factors=[
            "Specificity of enumerated force majeure events",
            "Causation standard (prevent vs hinder)",
            "Notice and mitigation obligations",
            "Duration before termination right",
            "Post-pandemic language adequacy",
            "Common-law fallback availability",
        ],
        primary_authority=[
            {"authority": "UCC", "reference": "UCC 2-615 - Excuse by Failure of Presupposed Conditions"},
            {"authority": "Restatement", "reference": "Restatement (Second) of Contracts 261 - Impracticability"},
            {"authority": "Case", "reference": "Hess Corp. v. Port Authority Trans-Hudson Corp., 2013 WL 6231157 (S.D.N.Y.)"},
            {"authority": "Case", "reference": "JN Contemporary Art LLC v. Phillips Auctioneers LLC, 507 F.Supp.3d 490 (S.D.N.Y. 2020)"},
        ],
        risk_severity=RiskSeverity.HIGH,
        risk_factors=[
            "Narrow enumeration missing pandemics/cyber events",
            "Catch-all language that may be too broad or too narrow",
            "No mitigation obligation",
            "Indefinite suspension without termination right",
            "No allocation of costs during suspension",
        ],
        mitigation_strategies=[
            "Enumerate pandemics, cyber attacks, supply chain disruptions explicitly",
            "Require prompt written notice with supporting documentation",
            "Include duty to mitigate and seek alternatives",
            "Set maximum suspension period (90-180 days) before termination right",
            "Address cost allocation during force majeure period",
        ],
        negotiation_guidance="""When negotiating force majeure clauses:
1. Enumerate specific events — do not rely solely on catch-all language
2. Post-COVID: explicitly include pandemics, epidemics, quarantine orders
3. Include cyber attacks and supply chain disruptions as modern FM events
4. Require mitigation efforts and regular status updates
5. Set a maximum suspension period (90-180 days) before termination right
6. Address cost allocation during the suspension period
7. Consider partial performance obligations during FM""",
        common_pitfalls=[
            "Relying on pre-COVID boilerplate without updating",
            "No pandemic/epidemic enumeration",
            "Catch-all without 'beyond reasonable control' qualifier",
            "No termination right after extended force majeure",
            "No mitigation obligation",
        ],
        best_practices=[
            "Modern comprehensive enumeration including pandemics and cyber",
            "Clear causation standard (prevents performance, not merely hinders)",
            "Prompt notice with documentation requirements",
            "Mitigation duty with regular status updates",
            "90-180 day maximum before termination right",
        ],
        confidence_level=ConfidenceLevel.GENERALLY_ENFORCEABLE,
        related_doctrines=["termination_for_convenience", "limitation_of_liability"],
        jurisdictional_notes=[
            "NY: Force majeure construed narrowly; must be specifically listed (Kel Kim Corp. v. Central Markets)",
            "England: Frustration doctrine supplements force majeure",
            "Civil law jurisdictions: FM may be implied by law even without contractual provision",
        ],
    ),

    # ========================================================================
    # INTELLECTUAL PROPERTY DOCTRINES
    # ========================================================================

    "ip_ownership": DoctrineBlock(
        topic="Intellectual Property Ownership Analysis",
        category=ClauseCategory.IP,
        keywords=[
            "ip ownership", "intellectual property ownership", "work for hire",
            "work made for hire", "ip assignment", "assignment of inventions",
            "foreground ip", "background ip",
        ],
        conclusion_template="""IP ownership provisions determine who owns intellectual property
created during the contract. Default rules vary by jurisdiction and relationship type.
Under U.S. copyright law, the creator owns work unless: (1) it qualifies as a 'work made
for hire' under 17 U.S.C. 101 (employee scope-of-employment or commissioned work in
enumerated categories), or (2) ownership is assigned in writing. Patent rights follow
inventorship unless assigned. Analysis must address background IP, foreground IP,
jointly developed IP, and license-back rights.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. WORK FOR HIRE
   - Employee vs independent contractor (Reid factors)
   - If IC: is the work in one of the 9 enumerated categories?
   - Is there a written agreement signed before work begins?
   - Copyright vests in employer/commissioning party if WFH applies

2. ASSIGNMENT
   - Present assignment ('hereby assigns') vs promise to assign
   - Consideration for assignment
   - Breadth of assignment (all IP vs specific deliverables)
   - Assignment of future inventions — enforceability varies by state

3. BACKGROUND vs FOREGROUND IP
   - Background IP: pre-existing IP each party brings
   - Foreground IP: IP created during the engagement
   - Joint IP: created through collaborative effort
   - License-back rights for background IP used in deliverables

4. LICENSE GRANTS
   - Scope: exclusive vs non-exclusive
   - Duration: perpetual vs term-limited
   - Territory: worldwide vs limited
   - Sublicense rights
   - Revocability

5. STATE LAW LIMITS
   - California Lab. Code 2870: limits on employee invention assignment
   - Similar statutes in WA, IL, MN, NC, DE
   - Must exclude inventions made on own time with own resources
""",
        key_factors=[
            "Work for hire vs assignment distinction",
            "Background vs foreground IP delineation",
            "License-back rights for contributed IP",
            "Present assignment vs promise to assign",
            "State law limitations on invention assignment",
            "Joint development IP allocation",
        ],
        primary_authority=[
            {"authority": "Statute", "reference": "17 U.S.C. 101 - Work Made for Hire Definition"},
            {"authority": "Case", "reference": "Community for Creative Non-Violence v. Reid, 490 U.S. 730 (1989)"},
            {"authority": "Statute", "reference": "Cal. Lab. Code 2870 - Employee Invention Assignment Limits"},
            {"authority": "Case", "reference": "FilmTec Corp. v. Allied-Signal Inc., 939 F.2d 1568 (Fed. Cir. 1991)"},
        ],
        risk_severity=RiskSeverity.CRITICAL,
        risk_factors=[
            "Ambiguous ownership of deliverables",
            "No work-for-hire agreement for independent contractors",
            "Background IP not properly identified and carved out",
            "Assignment of inventions clause violates state law",
            "No license-back for contributed background IP",
        ],
        mitigation_strategies=[
            "Execute WFH agreement before work begins",
            "Clearly delineate background vs foreground IP",
            "Include present assignment language ('hereby assigns')",
            "Add license-back for background IP in deliverables",
            "Comply with state invention assignment limitations",
        ],
        negotiation_guidance="""When negotiating IP ownership:
1. Determine who should own deliverables based on business relationship
2. Use 'hereby assigns' (present tense) not 'agrees to assign' (future promise)
3. Clearly identify all background IP in a schedule
4. License-back rights for background IP incorporated in deliverables
5. Address jointly developed IP ownership explicitly
6. Include moral rights waiver where applicable
7. Comply with state invention assignment limitations (CA, WA, IL, etc.)""",
        common_pitfalls=[
            "Relying on work-for-hire without meeting statutory requirements",
            "Promise to assign vs present assignment",
            "Failing to carve out pre-existing IP",
            "No license-back for background IP in deliverables",
            "Violating state invention assignment statutes",
        ],
        best_practices=[
            "Written assignment agreement executed before work begins",
            "Background IP schedule attached to contract",
            "Present tense assignment: 'hereby assigns'",
            "License-back for all contributed background IP",
            "State law compliance carve-outs",
        ],
        controlling_precedent=ControllingPrecedent(
            case_name="Community for Creative Non-Violence v. Reid",
            citation="490 U.S. 730 (1989)",
            court="Supreme Court",
            holding="Work-for-hire status requires either an employment relationship or a written agreement for commissioned works in enumerated categories.",
            binding_scope="nationwide",
            year=1989,
        ),
        related_doctrines=["confidentiality_nda", "license_grant"],
    ),

    # ========================================================================
    # CONFIDENTIALITY DOCTRINES
    # ========================================================================

    "confidentiality_nda": DoctrineBlock(
        topic="Confidentiality / NDA Clause Analysis",
        category=ClauseCategory.CONFIDENTIALITY,
        keywords=[
            "confidentiality", "confidential information", "non-disclosure",
            "nda", "proprietary information", "trade secret",
            "confidentiality obligation",
        ],
        conclusion_template="""Confidentiality provisions protect a party's proprietary information
from unauthorized disclosure. Enforceability depends on: (1) clear definition of what
constitutes 'Confidential Information,' (2) reasonable exceptions (public domain, independent
development, prior knowledge, court order), (3) permitted disclosures (employees, advisors,
affiliates), (4) duration of the obligation, and (5) adequacy of remedies including
injunctive relief.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. DEFINITION OF CONFIDENTIAL INFORMATION
   - Is the definition broad or narrow?
   - Does it require marking or written designation?
   - Are oral disclosures covered (typically require follow-up written confirmation)?
   - Does it capture technical, financial, business, and operational information?

2. STANDARD EXCEPTIONS
   - Publicly available information (not through breach)
   - Known to receiving party prior to disclosure
   - Independently developed without use of CI
   - Received from third party without restriction
   - Required by law or court order (with notice)

3. PERMITTED DISCLOSURES
   - Employees with need to know
   - Professional advisors (attorneys, accountants)
   - Affiliates and subsidiaries
   - Subcontractors (with flow-down obligations)

4. DURATION
   - During term plus post-termination period
   - Trade secrets: indefinite (as long as secret)
   - General CI: 2-5 years is market standard
   - Perpetual confidentiality obligations — enforceability varies

5. REMEDIES
   - Injunctive relief without bond
   - Monetary damages
   - Return or destruction of CI upon termination
   - Certification of destruction
""",
        key_factors=[
            "Breadth of Confidential Information definition",
            "Completeness of standard exceptions",
            "Permitted disclosure scope",
            "Duration of confidentiality obligation",
            "Injunctive relief availability",
            "Return/destruction obligations",
        ],
        primary_authority=[
            {"authority": "Statute", "reference": "Defend Trade Secrets Act (DTSA), 18 U.S.C. 1836"},
            {"authority": "Statute", "reference": "Uniform Trade Secrets Act (UTSA)"},
            {"authority": "Case", "reference": "E.I. du Pont de Nemours & Co. v. Christopher, 431 F.2d 1012 (5th Cir. 1970)"},
        ],
        risk_severity=RiskSeverity.MEDIUM,
        risk_factors=[
            "Overly broad definition capturing non-confidential information",
            "Missing standard exceptions",
            "Perpetual confidentiality for non-trade-secret information",
            "No return/destruction obligation",
            "Inadequate permitted disclosure carve-outs",
        ],
        mitigation_strategies=[
            "Define CI specifically with marking requirements",
            "Include all five standard exceptions",
            "Limit duration to 3-5 years for general CI",
            "Require return or certified destruction",
            "Include injunctive relief provision",
        ],
        negotiation_guidance="""When negotiating confidentiality clauses:
1. Push for specific definition with marking/designation requirements
2. Ensure all five standard exceptions are included
3. Duration: 3-5 years for general CI, perpetual for trade secrets
4. Permitted disclosures: employees, advisors, affiliates (with binding obligations)
5. Return/destroy obligation upon termination with certification
6. Injunctive relief clause (money damages inadequate for CI breaches)
7. Consider residuals clause for information retained in unaided memory""",
        common_pitfalls=[
            "CI definition so broad it is unmanageable",
            "Missing the 'independently developed' exception",
            "Perpetual obligation for non-trade-secret information",
            "No carve-out for legally required disclosures",
            "No return/destruction mechanism",
        ],
        best_practices=[
            "Specific CI definition with marking requirements",
            "Five standard exceptions clearly stated",
            "3-5 year duration for general CI, perpetual for trade secrets",
            "Return or certified destruction upon termination",
            "Injunctive relief + monetary damages",
        ],
        related_doctrines=["data_protection", "ip_ownership", "restrictive_covenants"],
    ),

    # ========================================================================
    # GOVERNING LAW DOCTRINES
    # ========================================================================

    "governing_law": DoctrineBlock(
        topic="Governing Law and Jurisdiction Analysis",
        category=ClauseCategory.GOVERNING_LAW,
        keywords=[
            "governing law", "choice of law", "applicable law",
            "jurisdiction", "venue", "forum selection",
            "arbitration", "dispute resolution",
        ],
        conclusion_template="""Governing law clauses select which jurisdiction's substantive law
applies to interpret and enforce the contract. Forum selection clauses determine where
disputes will be adjudicated. Enforceability depends on: (1) whether the chosen law has
a reasonable relationship to the transaction, (2) whether the chosen forum is fundamentally
unfair or unreasonable, (3) exclusivity of the forum selection, and (4) whether the clause
was freely negotiated or imposed via adhesion.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. GOVERNING LAW SELECTION
   - Does the chosen jurisdiction have a reasonable connection to the transaction?
   - 'Without regard to conflicts of law principles' — standard inclusion
   - Federal vs state law issues (e.g., ERISA preemption)
   - International considerations (CISG opt-out for goods)

2. JURISDICTION / FORUM SELECTION
   - Exclusive vs non-exclusive jurisdiction
   - Consent to personal jurisdiction
   - Waiver of objections (inconvenient forum, improper venue)
   - Federal vs state court selection

3. DISPUTE RESOLUTION MECHANISM
   - Litigation (court) vs arbitration vs mediation
   - Mandatory pre-suit negotiation/mediation step
   - Arbitration: AAA, JAMS, ICC rules
   - Number of arbitrators, discovery scope, appeal rights

4. ENFORCEABILITY
   - Bremen v. Zapata: forum selection clauses presumptively enforceable
   - Carnival Cruise v. Shute: even in adhesion contracts
   - Exceptions: fraud, overreaching, fundamentally unfair forum
   - Consumer protection statutes may override

5. PRACTICAL CONSIDERATIONS
   - Litigation costs in chosen forum
   - Travel burden on parties
   - Quality of judiciary / arbitrators
   - Enforcement of judgments/awards across borders
""",
        key_factors=[
            "Reasonable connection to transaction",
            "Exclusive vs non-exclusive jurisdiction",
            "Arbitration vs litigation election",
            "CISG opt-out for international sales",
            "Jury trial waiver inclusion",
            "Practical fairness of chosen forum",
        ],
        primary_authority=[
            {"authority": "Case", "reference": "The Bremen v. Zapata Off-Shore Co., 407 U.S. 1 (1972)"},
            {"authority": "Case", "reference": "Carnival Cruise Lines v. Shute, 499 U.S. 585 (1991)"},
            {"authority": "Statute", "reference": "Federal Arbitration Act, 9 U.S.C. 1-16"},
            {"authority": "Restatement", "reference": "Restatement (Second) of Conflict of Laws 187"},
        ],
        risk_severity=RiskSeverity.MEDIUM,
        risk_factors=[
            "Forum with unfavorable substantive law",
            "Exclusive jurisdiction in remote location",
            "Mandatory arbitration without appeal rights",
            "No conflicts of law waiver",
            "CISG applicability not addressed",
        ],
        mitigation_strategies=[
            "Select governing law favorable to your position",
            "Include 'without regard to conflicts of law' language",
            "Opt out of CISG for international goods contracts",
            "Consider non-exclusive jurisdiction for flexibility",
            "Include jury waiver if proceeding in court",
        ],
        negotiation_guidance="""When negotiating governing law and jurisdiction:
1. Choose a jurisdiction with well-developed contract law (NY, DE, CA, TX, UK)
2. Include 'without regard to conflict of laws principles'
3. Opt out of CISG expressly for international goods contracts
4. Consider mandatory mediation before arbitration/litigation
5. If arbitration: specify rules (AAA/JAMS), number of arbitrators, seat
6. Include jury trial waiver for court proceedings
7. Consider prevailing party attorneys' fees provision""",
        common_pitfalls=[
            "Choosing governing law without considering implications",
            "Failing to opt out of CISG in international sales",
            "Mandatory arbitration without preserving injunctive relief in court",
            "No attorneys' fee shifting provision",
            "Inconsistent forum selection and governing law",
        ],
        best_practices=[
            "Clear governing law with conflicts waiver",
            "CISG opt-out for international goods",
            "Mandatory mediation step before escalation",
            "Specific arbitration rules and procedures",
            "Carve-out for injunctive relief in court",
        ],
        controlling_precedent=ControllingPrecedent(
            case_name="The Bremen v. Zapata Off-Shore Co.",
            citation="407 U.S. 1 (1972)",
            court="Supreme Court",
            holding="Forum selection clauses are presumptively valid and enforceable unless enforcement would be unreasonable or unjust.",
            binding_scope="nationwide",
            year=1972,
        ),
        related_doctrines=["dispute_resolution", "jury_waiver"],
    ),

    # ========================================================================
    # ASSIGNMENT AND CHANGE OF CONTROL
    # ========================================================================

    "assignment_change_of_control": DoctrineBlock(
        topic="Assignment and Change of Control Analysis",
        category=ClauseCategory.ASSIGNMENT,
        keywords=[
            "assignment", "change of control", "anti-assignment",
            "non-assignable", "successors and assigns", "merger",
            "acquisition", "delegation", "novation", "subcontracting",
        ],
        conclusion_template="""Assignment provisions control whether a party can transfer its rights
or delegate its obligations to a third party. Change of control provisions address whether
a merger, acquisition, or ownership change triggers consent rights or termination.
Key analysis: (1) UCC 2-210 provides default assignment rules for goods, (2) anti-assignment
clauses are narrowly construed, (3) courts distinguish between assignment of rights and
delegation of duties, and (4) change of control may or may not constitute an 'assignment'
depending on the clause's language.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. ASSIGNMENT OF RIGHTS vs DELEGATION OF DUTIES
   - Rights: generally assignable unless personal in nature
   - Duties: delegable unless performance is personal
   - Anti-assignment clauses may only bar assignment, not delegation
   - UCC 2-210: assignment of rights includes delegation of duties

2. ANTI-ASSIGNMENT CLAUSE
   - Prohibition vs consent requirement
   - Does it require consent (not to be unreasonably withheld)?
   - Remedies for unauthorized assignment (void vs voidable)
   - Exception for affiliates, successors, corporate restructuring

3. CHANGE OF CONTROL TRIGGERS
   - Is CoC defined as change in majority ownership?
   - Does a merger constitute an assignment?
   - Reverse triangular merger — may avoid assignment clause
   - Does CoC trigger consent right or termination right?

4. SUCCESSOR LIABILITY
   - 'Successors and assigns' language
   - Binding on permitted assigns
   - Successor entity inherits obligations

5. CARVE-OUTS
   - Affiliate transfers without consent
   - Restructuring within corporate family
   - Merger with entity of equal or greater creditworthiness
""",
        key_factors=[
            "Assignment prohibition vs consent requirement",
            "Change of control definition scope",
            "Affiliate transfer exception",
            "Merger / reverse merger treatment",
            "Consequences of unauthorized assignment",
            "Successor and assign binding language",
        ],
        primary_authority=[
            {"authority": "UCC", "reference": "UCC 2-210 - Delegation of Performance; Assignment of Rights"},
            {"authority": "Case", "reference": "Meso Scale Diagnostics, LLC v. Meso Scale Techs., LLC, 62 A.3d 62 (Del. Ch. 2013)"},
            {"authority": "Restatement", "reference": "Restatement (Second) of Contracts 317-322"},
        ],
        risk_severity=RiskSeverity.HIGH,
        risk_factors=[
            "Silent on change of control — creates ambiguity",
            "Overly broad anti-assignment without affiliate exception",
            "CoC triggers termination without consent opportunity",
            "No carve-out for internal restructuring",
            "Unauthorized assignment is void (not merely voidable)",
        ],
        mitigation_strategies=[
            "Include specific CoC definition and triggers",
            "Carve out affiliate transfers and internal restructuring",
            "Consent requirement with 'not unreasonably withheld' standard",
            "Address reverse merger treatment explicitly",
            "Include successor and assign binding language",
        ],
        negotiation_guidance="""When negotiating assignment and CoC provisions:
1. Distinguish between assignment, delegation, and change of control
2. Include affiliate transfer exception
3. Consent 'not to be unreasonably withheld, conditioned, or delayed'
4. Define change of control specifically (>50% ownership change)
5. Address reverse triangular mergers explicitly
6. CoC should trigger consent right, not automatic termination
7. Include deemed consent if no response within 30 days""",
        common_pitfalls=[
            "Anti-assignment clause that blocks legitimate M&A transactions",
            "Silent on reverse merger treatment",
            "No affiliate transfer exception",
            "CoC triggers termination without opportunity to address concerns",
            "Void (not voidable) unauthorized assignment",
        ],
        best_practices=[
            "Consent required, not to be unreasonably withheld",
            "Affiliate transfer exception",
            "Specific CoC definition (>50% ownership change)",
            "30-day deemed consent mechanism",
            "Address all transaction structures (merger, asset sale, stock sale)",
        ],
        related_doctrines=["termination_for_cause", "governing_law"],
    ),

    # ========================================================================
    # REPRESENTATIONS AND WARRANTIES
    # ========================================================================

    "representations_warranties": DoctrineBlock(
        topic="Representations and Warranties Analysis",
        category=ClauseCategory.REPRESENTATIONS,
        keywords=[
            "representations and warranties", "reps and warranties",
            "represents and warrants", "warranty of title",
            "warranty disclaimer", "as-is", "material adverse change",
            "mac clause", "mae clause", "bring-down condition",
        ],
        conclusion_template="""Representations and warranties are statements of fact (representations)
and promises about the present or future state (warranties) that allocate risk between the
parties. Breach of rep/warranty typically gives rise to indemnification claims and may
constitute a material breach. Key analysis: (1) distinction between representations
(reliance-based) and warranties (strict liability for breach), (2) knowledge qualifiers
and materiality qualifiers, (3) survival periods, (4) anti-sandbagging provisions, and
(5) sole remedy/exclusive remedy clauses.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. SCOPE OF R&W
   - Corporate status and authority
   - No conflicts with other agreements
   - Compliance with applicable laws
   - Financial condition accuracy
   - IP ownership and non-infringement
   - No undisclosed liabilities

2. QUALIFIERS
   - Knowledge qualifiers ('to the best of Seller's knowledge')
   - Materiality qualifiers ('in all material respects')
   - Double materiality scraping in indemnification
   - 'Material Adverse Effect' qualifier

3. SURVIVAL PERIOD
   - General R&W: 12-24 months post-closing
   - Fundamental R&W (title, authority, tax): statute of limitations
   - Tax R&W: typically full statute of limitations
   - Environmental R&W: extended survival

4. SANDBAGGING
   - Pro-sandbagging: buyer can claim even if knew of breach
   - Anti-sandbagging: no claim if buyer had knowledge
   - Silent: varies by jurisdiction (Delaware vs New York)

5. BRING-DOWN AND CLOSING CONDITIONS
   - R&W must be true at signing and at closing
   - Bring-down standard: 'true in all material respects'
   - MAC/MAE exception to bring-down
""",
        key_factors=[
            "Scope and specificity of representations",
            "Knowledge and materiality qualifiers",
            "Survival period adequacy",
            "Pro-sandbagging vs anti-sandbagging stance",
            "Indemnification trigger and exclusive remedy",
            "Bring-down conditions for closing",
        ],
        primary_authority=[
            {"authority": "Case", "reference": "CBS Inc. v. Ziff-Davis Publishing Co., 75 N.Y.2d 496 (1990)"},
            {"authority": "Case", "reference": "Akorn Inc. v. Fresenius Kabi AG, 2018 WL 4719347 (Del. Ch. 2018)"},
            {"authority": "Restatement", "reference": "Restatement (Second) of Contracts 159-169 (Misrepresentation)"},
        ],
        risk_severity=RiskSeverity.HIGH,
        risk_factors=[
            "Overly broad knowledge qualifiers that gut R&W",
            "Short survival periods for critical representations",
            "Anti-sandbagging in seller-favorable agreements",
            "Double materiality scraping eliminating claims",
            "No indemnification backing for R&W breaches",
        ],
        mitigation_strategies=[
            "Limit knowledge qualifiers to actual knowledge of named individuals",
            "Extend survival for fundamental and tax representations",
            "Address sandbagging explicitly",
            "Eliminate double materiality for indemnification claims",
            "Ensure indemnification backs all material R&W breaches",
        ],
        negotiation_guidance="""When negotiating representations and warranties:
1. Distinguish between fundamental R&W (longer survival) and general R&W
2. Knowledge qualifiers: limit to 'actual knowledge' of named individuals
3. Survival: 18-24 months general, statute of limitations for fundamental
4. Address sandbagging explicitly (do not leave silent)
5. Avoid double materiality scraping in indemnification
6. Ensure bring-down condition uses 'in all material respects' standard
7. MAC/MAE definition should be specific and exclude market-wide events""",
        common_pitfalls=[
            "Accepting broad knowledge qualifiers without inquiry obligation",
            "12-month survival for fundamental representations",
            "Silent on sandbagging in jurisdictions hostile to buyer",
            "Double materiality that eliminates most indemnification claims",
            "MAC/MAE too broad or too narrow",
        ],
        best_practices=[
            "Knowledge defined as actual knowledge with inquiry obligation",
            "Tiered survival: general (18-24 months), fundamental (statute of limitations)",
            "Express sandbagging provision",
            "Single materiality for indemnification calculation",
            "Specific MAC/MAE definition excluding market-wide events",
        ],
        controlling_precedent=ControllingPrecedent(
            case_name="Akorn Inc. v. Fresenius Kabi AG",
            citation="2018 WL 4719347 (Del. Ch. 2018)",
            court="Appellate Court",
            holding="MAE found for the first time in Delaware; systematic regulatory and compliance problems constituted a Material Adverse Effect justifying termination.",
            binding_scope="Delaware",
            year=2018,
        ),
        related_doctrines=["indemnification_general", "limitation_of_liability"],
    ),

    # ========================================================================
    # DATA PROTECTION DOCTRINES
    # ========================================================================

    "data_protection": DoctrineBlock(
        topic="Data Protection and Privacy Analysis",
        category=ClauseCategory.DATA_PROTECTION,
        keywords=[
            "data protection", "data privacy", "gdpr", "ccpa",
            "personal data", "pii", "data processing agreement",
            "dpa", "data breach notification", "cross-border data transfer",
        ],
        conclusion_template="""Data protection provisions allocate responsibility for handling personal
data in compliance with applicable privacy laws (GDPR, CCPA, etc.). Analysis requires:
(1) accurate characterization of data processing roles (controller vs processor),
(2) compliance with data processing agreement requirements, (3) cross-border transfer
mechanisms (SCCs, adequacy decisions), (4) breach notification obligations,
and (5) data subject rights facilitation.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. ROLE CLASSIFICATION
   - Controller: determines purposes and means of processing
   - Processor: processes on behalf of controller
   - Joint controllers: jointly determine purposes
   - Sub-processor management and approval

2. DPA REQUIREMENTS
   - Subject matter, duration, nature, purpose of processing
   - Types of personal data and categories of data subjects
   - Controller's instructions and obligations
   - Processor's obligations (security, confidentiality, assistance)
   - Sub-processor authorization and management
   - Audit rights

3. DATA BREACH NOTIFICATION
   - Timing: 72 hours under GDPR, varies by state law
   - Content of notification
   - Cooperation obligations
   - Remediation responsibilities
   - Cost allocation for breach response

4. CROSS-BORDER TRANSFERS
   - EU-US Data Privacy Framework
   - Standard Contractual Clauses (SCCs)
   - Transfer Impact Assessments
   - Supplementary measures

5. DATA SUBJECT RIGHTS
   - Access, rectification, erasure, portability
   - Facilitation obligations on processor
   - Response timeframes
""",
        key_factors=[
            "Accurate controller/processor classification",
            "DPA completeness per GDPR Article 28",
            "Sub-processor management requirements",
            "Breach notification timing and obligations",
            "Cross-border transfer mechanism adequacy",
            "Data subject rights facilitation",
        ],
        primary_authority=[
            {"authority": "Statute", "reference": "GDPR Articles 28, 32, 33, 44-49"},
            {"authority": "Statute", "reference": "CCPA/CPRA, Cal. Civ. Code 1798.100 et seq."},
            {"authority": "Case", "reference": "Schrems II (Case C-311/18, CJEU 2020)"},
            {"authority": "Regulation", "reference": "EU Standard Contractual Clauses (2021)"},
        ],
        risk_severity=RiskSeverity.CRITICAL,
        risk_factors=[
            "Incorrect controller/processor classification",
            "Inadequate DPA terms",
            "No cross-border transfer mechanism",
            "Breach notification > 72 hours",
            "No sub-processor management provisions",
        ],
        mitigation_strategies=[
            "Execute GDPR-compliant DPA as attachment",
            "Implement SCCs for cross-border transfers",
            "72-hour breach notification with cooperation obligations",
            "Prior written consent for sub-processors",
            "Regular data protection impact assessments",
        ],
        negotiation_guidance="""When negotiating data protection provisions:
1. Accurately classify roles (controller vs processor) based on actual data flows
2. Attach a comprehensive DPA as exhibit to the agreement
3. Require 72-hour breach notification with detailed reporting obligations
4. Address cross-border transfers with appropriate safeguards
5. Include audit rights (remote and on-site)
6. Require prior written consent for sub-processor engagement
7. Include data return/deletion obligations upon termination
8. Address CCPA/CPRA 'sale' and 'sharing' definitions""",
        common_pitfalls=[
            "Mislabeling processor as controller (or vice versa)",
            "Boilerplate DPA that does not reflect actual processing",
            "No cross-border transfer mechanism",
            "Breach notification timing inconsistent with law",
            "No sub-processor visibility or control",
        ],
        best_practices=[
            "GDPR Article 28-compliant DPA",
            "72-hour breach notification",
            "SCCs + supplementary measures for cross-border",
            "Prior written consent for sub-processors",
            "Deletion certification upon contract termination",
        ],
        confidence_level=ConfidenceLevel.EVOLVING_LAW,
        related_doctrines=["confidentiality_nda", "limitation_of_liability"],
        jurisdictional_notes=[
            "EU/EEA: GDPR applies with DPA requirements (Art. 28)",
            "UK: UK GDPR post-Brexit with separate adequacy status",
            "California: CCPA/CPRA with 'sale'/'sharing' concepts",
            "Brazil: LGPD with similar controller/processor framework",
            "China: PIPL with data localization requirements",
        ],
    ),

    # ========================================================================
    # RESTRICTIVE COVENANTS
    # ========================================================================

    "restrictive_covenants": DoctrineBlock(
        topic="Non-Compete and Restrictive Covenant Analysis",
        category=ClauseCategory.RESTRICTIVE_COVENANTS,
        keywords=[
            "non-compete", "non-solicitation", "restrictive covenant",
            "covenant not to compete", "exclusivity", "no-hire",
            "garden leave", "employee non-solicitation",
        ],
        conclusion_template="""Restrictive covenants (non-competes, non-solicitation, no-hire) limit
a party's competitive activities after contract termination. Enforceability varies dramatically
by jurisdiction and requires: (1) a legitimate protectable interest (trade secrets, customer
relationships, specialized training), (2) reasonable scope in time, geography, and activity,
(3) adequate consideration, and (4) no undue hardship on the restricted party. Several states
now ban or severely limit non-competes (California, Minnesota, Oklahoma, North Dakota).""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. LEGITIMATE PROTECTABLE INTEREST
   - Trade secrets and confidential information
   - Customer relationships and goodwill
   - Specialized training at employer's expense
   - Unique or extraordinary services

2. REASONABLENESS (Three-Factor Test)
   - Time: typically 1-2 years; longer requires strong justification
   - Geography: limited to actual business territory
   - Activity: limited to competitive activities, not all employment

3. CONSIDERATION
   - New employment: employment itself is consideration
   - Existing employment: many states require additional consideration
   - Adequate consideration varies by jurisdiction

4. STATE LAW VARIATIONS
   - California: non-competes void (Bus. & Prof. Code 16600)
   - Oklahoma, North Dakota: similar bans
   - Minnesota: banned as of July 1, 2023
   - FTC proposed rule: nationwide ban (status pending)
   - Blue pencil doctrine: court reforms overbroad covenants
   - Red pencil: court strikes entire covenant if overbroad

5. NON-SOLICITATION ALTERNATIVE
   - Customer non-solicitation: more enforceable than non-compete
   - Employee non-solicitation: generally enforceable
   - No-hire provisions: enforceability varies
""",
        key_factors=[
            "Legitimate protectable interest identified",
            "Reasonableness of time restriction",
            "Reasonableness of geographic scope",
            "Reasonableness of activity restriction",
            "Adequate consideration provided",
            "Jurisdiction-specific enforceability",
        ],
        primary_authority=[
            {"authority": "Statute", "reference": "Cal. Bus. & Prof. Code 16600"},
            {"authority": "Case", "reference": "BDO Seidman v. Hirshberg, 93 N.Y.2d 382 (1999)"},
            {"authority": "Case", "reference": "Marsh USA Inc. v. Cook, 354 S.W.3d 764 (Tex. 2011)"},
            {"authority": "Statute", "reference": "Minn. Stat. 181.988 (Non-compete Ban, eff. 7/1/2023)"},
        ],
        risk_severity=RiskSeverity.HIGH,
        risk_factors=[
            "Overbroad geographic or temporal scope",
            "No legitimate protectable interest",
            "Inadequate consideration",
            "Applicable in jurisdiction that bans non-competes",
            "Activity restriction broader than necessary",
        ],
        mitigation_strategies=[
            "Limit to 12-24 months",
            "Define geographic scope to actual business territory",
            "Narrow activity restriction to directly competitive roles",
            "Provide garden leave or additional consideration",
            "Consider non-solicitation as alternative to non-compete",
        ],
        negotiation_guidance="""When negotiating restrictive covenants:
1. Check governing law jurisdiction — California bans non-competes entirely
2. Limit time to 12 months (18-24 months maximum with strong justification)
3. Geographic scope: actual business territory or customer locations
4. Activity: only directly competitive activities, not all employment
5. Consider non-solicitation of customers/employees as less restrictive alternative
6. Ensure adequate consideration (signing bonus, severance, etc.)
7. Include garden leave provision (pay during restricted period)
8. Blue pencil clause allows court to reform rather than void""",
        common_pitfalls=[
            "Using non-compete in California (void under 16600)",
            "Geographic scope broader than actual business footprint",
            "No additional consideration for existing employees",
            "Activity restriction that prevents any employment in industry",
            "No garden leave or compensation during restricted period",
        ],
        best_practices=[
            "12-month maximum with narrow scope",
            "Non-solicitation preferred over non-compete",
            "Garden leave provision with continued compensation",
            "Blue pencil clause for judicial reformation",
            "Choice of law favorable to enforcement",
        ],
        controlling_precedent=ControllingPrecedent(
            case_name="BDO Seidman v. Hirshberg",
            citation="93 N.Y.2d 382 (1999)",
            court="State Supreme Court",
            holding="Restrictive covenants are enforceable only to the extent they are reasonable in time, geographic scope, and activity, and protect a legitimate interest.",
            binding_scope="New York",
            year=1999,
        ),
        related_doctrines=["confidentiality_nda", "ip_ownership"],
    ),

    # ========================================================================
    # PAYMENT DOCTRINES
    # ========================================================================

    "payment_terms": DoctrineBlock(
        topic="Payment Terms Analysis",
        category=ClauseCategory.PAYMENT,
        keywords=[
            "payment terms", "net 30", "net 60", "late payment",
            "interest", "milestone payment", "retainer", "setoff",
            "most favored nation", "price escalation", "audit rights",
        ],
        conclusion_template="""Payment provisions establish the economic terms of the contract including
timing, method, conditions, and consequences of non-payment. Analysis covers: (1) payment
timing and conditions precedent, (2) late payment interest rates and statutory limits,
(3) setoff and withholding rights, (4) price adjustment mechanisms, (5) audit rights,
and (6) most-favored-nation pricing commitments.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. PAYMENT TIMING AND CONDITIONS
   - Invoice submission requirements
   - Payment terms (Net 30/60/90)
   - Conditions precedent to payment
   - Milestone-based vs time-based
   - Acceptance requirements before payment

2. LATE PAYMENT CONSEQUENCES
   - Interest rate: contractual vs statutory
   - State usury laws limiting interest
   - Right to suspend services for non-payment
   - Cumulative late payment as material breach

3. PRICE ADJUSTMENTS
   - Fixed price vs variable pricing
   - CPI/COLA adjustments
   - Benchmarking provisions
   - Most-favored-nation commitments

4. SETOFF AND WITHHOLDING
   - Right to setoff against amounts owed
   - Disputed amount holdback
   - Tax withholding obligations
   - Government contract-specific rules

5. AUDIT RIGHTS
   - Right to audit books and records
   - Frequency and notice requirements
   - Cost of audit allocation
   - Overcharge remediation
""",
        key_factors=[
            "Payment timing and conditions",
            "Late payment interest rate",
            "Price adjustment mechanisms",
            "Setoff and withholding rights",
            "Audit rights scope and frequency",
            "MFN pricing commitments",
        ],
        primary_authority=[
            {"authority": "UCC", "reference": "UCC 2-310 - Open Time for Payment or Running of Credit"},
            {"authority": "Statute", "reference": "Prompt Payment Act, 31 U.S.C. 3901-3907 (federal contractors)"},
            {"authority": "Practice Guide", "reference": "ABA Model Payment Provisions"},
        ],
        risk_severity=RiskSeverity.MEDIUM,
        risk_factors=[
            "Extended payment terms without interest",
            "No remedy for late payment",
            "Unlimited setoff rights without dispute resolution",
            "MFN clause with broad benchmark scope",
            "No audit rights for complex pricing models",
        ],
        mitigation_strategies=[
            "Net 30 payment with 1.5%/month late interest",
            "Right to suspend services after 60+ days overdue",
            "Limit setoff to undisputed amounts only",
            "Narrow MFN to comparable contracts only",
            "Annual audit right with cost-shifting above 5% overcharge",
        ],
        negotiation_guidance="""When negotiating payment terms:
1. Net 30 is market standard; push back on Net 60+
2. Include late payment interest (1-1.5% per month, check usury laws)
3. Right to suspend performance after 60 days overdue
4. Setoff only against undisputed amounts
5. CPI adjustment for multi-year contracts
6. Annual audit right with cost-shifting mechanism
7. Clear invoice requirements and dispute process""",
        common_pitfalls=[
            "Accepting Net 90 without late payment interest",
            "Broad setoff rights allowing withholding of disputed amounts",
            "No escalation mechanism for payment disputes",
            "MFN clause that triggers on non-comparable contracts",
            "No suspension right for chronic late payment",
        ],
        best_practices=[
            "Net 30 with 1.5%/month late payment interest",
            "Service suspension right after 60 days",
            "Setoff limited to undisputed amounts",
            "CPI escalation for contracts > 12 months",
            "Annual audit right with 5% overcharge cost-shift",
        ],
        related_doctrines=["termination_for_cause", "limitation_of_liability"],
    ),

    # ========================================================================
    # AUTO-RENEWAL / EVERGREEN DOCTRINES
    # ========================================================================

    "auto_renewal": DoctrineBlock(
        topic="Auto-Renewal and Evergreen Clause Analysis",
        category=ClauseCategory.TERMINATION,
        keywords=[
            "auto-renewal", "auto renewal", "evergreen", "automatic renewal",
            "renewal term", "renewal option", "non-renewal notice",
        ],
        conclusion_template="""Auto-renewal (evergreen) clauses automatically extend the contract
for successive renewal terms unless a party provides timely non-renewal notice. These
clauses are generally enforceable in commercial contracts but subject to: (1) state
consumer protection statutes requiring disclosure, (2) reasonable notice periods,
(3) clear renewal terms, and (4) whether the renewal modifies material terms. Several
states have enacted auto-renewal disclosure requirements.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. RENEWAL MECHANICS
   - Length of renewal term (matching initial or shorter?)
   - Number of renewals (unlimited or capped?)
   - When does renewal trigger (end of term, anniversary?)
   - Does renewal maintain all original terms?

2. NON-RENEWAL NOTICE
   - Notice period: typically 30-90 days before renewal
   - Notice method: written, email, certified mail?
   - Consequence of late notice: locked in for renewal term
   - Calendar reminder systems

3. PRICE CHANGES ON RENEWAL
   - Price holds for renewal term?
   - Automatic price escalation on renewal?
   - Right to renegotiate on renewal?
   - Cap on price increases

4. STATE LAW REQUIREMENTS
   - Many states require conspicuous disclosure of auto-renewal
   - Some require annual reminder notices
   - B2B vs B2C different regulatory treatment
   - Penalty for non-compliance: voidable contract
""",
        key_factors=[
            "Renewal term length and frequency",
            "Non-renewal notice period and method",
            "Price change provisions on renewal",
            "State auto-renewal disclosure requirements",
            "Maximum number of renewal terms",
            "Material term changes on renewal",
        ],
        primary_authority=[
            {"authority": "Statute", "reference": "Cal. Bus. & Prof. Code 17600-17606 (Auto-Renewal Law)"},
            {"authority": "Statute", "reference": "N.Y. Gen. Oblig. Law 5-903 (Auto-Renewal Disclosure)"},
            {"authority": "Practice Guide", "reference": "National Conference of State Legislatures - Auto-Renewal Laws"},
        ],
        risk_severity=RiskSeverity.MEDIUM,
        risk_factors=[
            "Extended renewal with no non-renewal window",
            "Price increases on renewal without cap",
            "Short non-renewal notice period (e.g., 30 days)",
            "Non-compliance with state auto-renewal laws",
        ],
        mitigation_strategies=[
            "Set non-renewal notice at 60-90 days",
            "Cap price increases at CPI + 3% on renewal",
            "Calendar the non-renewal notice deadline",
            "Ensure compliance with applicable auto-renewal statutes",
        ],
        negotiation_guidance="""When negotiating auto-renewal clauses:
1. Non-renewal notice: 60-90 days minimum before renewal date
2. Cap renewal term at 1 year regardless of initial term length
3. Price increase cap on renewal (CPI or fixed percentage)
4. Right to renegotiate material terms at each renewal
5. Calendar the non-renewal deadline immediately upon signing
6. Ensure compliance with state auto-renewal disclosure laws""",
        common_pitfalls=[
            "Missing the non-renewal notice window",
            "Unlimited renewals with escalating prices",
            "Non-renewal notice too short to evaluate alternatives",
            "B2C contracts not complying with state disclosure laws",
        ],
        best_practices=[
            "60-90 day non-renewal notice period",
            "1-year maximum renewal term",
            "Price cap on renewal (CPI + reasonable percentage)",
            "Annual right to renegotiate material terms",
        ],
        related_doctrines=["termination_for_convenience", "payment_terms"],
    ),

    # ========================================================================
    # SERVICE LEVEL DOCTRINES
    # ========================================================================

    "service_level_agreement": DoctrineBlock(
        topic="Service Level Agreement (SLA) Analysis",
        category=ClauseCategory.PERFORMANCE,
        keywords=[
            "service level agreement", "sla", "uptime", "availability",
            "performance standard", "service credit", "kpi",
            "response time", "resolution time",
        ],
        conclusion_template="""Service Level Agreements define measurable performance standards and
the consequences of failing to meet them. SLA analysis requires evaluation of: (1) specificity
and measurability of performance metrics, (2) adequacy of service credits as sole remedy,
(3) exclusions from SLA calculations, (4) reporting and monitoring mechanisms, and
(5) whether SLA credits provide meaningful accountability or merely symbolic relief.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. PERFORMANCE METRICS
   - Uptime/availability percentage (99.9% vs 99.99%)
   - Response time for incident categories
   - Resolution time targets
   - Throughput and performance benchmarks

2. SERVICE CREDITS
   - Credit amount per SLA miss (% of monthly fees)
   - Cap on total credits per period
   - Are credits the sole remedy?
   - Cumulative SLA failure as material breach

3. MEASUREMENT AND REPORTING
   - How is uptime measured (provider tools vs third-party)?
   - Reporting frequency (monthly, quarterly)
   - Dispute resolution for measurement disagreements
   - Audit rights on SLA data

4. EXCLUSIONS
   - Scheduled maintenance windows
   - Force majeure events
   - Customer-caused outages
   - Third-party service failures
   - Beta/preview features

5. ESCALATION AND TERMINATION
   - Chronic SLA failure as termination trigger
   - Escalation procedures for repeated misses
   - Root cause analysis requirements
   - Improvement plan obligations
""",
        key_factors=[
            "Specificity of performance metrics",
            "Service credit adequacy",
            "Measurement methodology fairness",
            "SLA exclusion scope",
            "Chronic failure consequences",
            "Reporting and transparency",
        ],
        primary_authority=[
            {"authority": "Practice Guide", "reference": "ITIL Service Level Management Framework"},
            {"authority": "Practice Guide", "reference": "AICPA SOC Reporting Standards"},
        ],
        risk_severity=RiskSeverity.MEDIUM,
        risk_factors=[
            "Service credits as sole and exclusive remedy",
            "Credits capped at small percentage of fees",
            "Broad exclusions that render SLA meaningless",
            "Provider-measured SLA with no audit rights",
            "No chronic failure termination trigger",
        ],
        mitigation_strategies=[
            "Credits should not be sole remedy for material failures",
            "Chronic failure (3+ months) triggers termination right",
            "Third-party or mutual measurement of SLA metrics",
            "Limit exclusions to reasonable items",
            "Root cause analysis and improvement plan requirements",
        ],
        negotiation_guidance="""When negotiating SLAs:
1. Define metrics precisely with measurement methodology
2. Credits: 5-10% of monthly fees per SLA tier miss
3. Chronic failure (3+ consecutive months) = right to terminate
4. Credits as the remedy for minor misses, not for prolonged outages
5. Third-party monitoring or mutual agreement on measurement
6. Monthly reporting with quarterly review meetings
7. Root cause analysis within 5 business days of P1 incident""",
        common_pitfalls=[
            "Accepting 99.9% uptime without understanding what that means (8.77 hours downtime/year)",
            "Credits capped at 10% of monthly fee (meaningless for major outages)",
            "No chronic failure termination trigger",
            "Provider-only measurement with no verification right",
        ],
        best_practices=[
            "99.95% or higher for mission-critical services",
            "Tiered credits: 5% per 0.1% below SLA target",
            "Chronic failure = termination right after 3 consecutive months",
            "Monthly reporting with root cause for all P1/P2 incidents",
        ],
        related_doctrines=["termination_for_cause", "limitation_of_liability"],
    ),

    # ========================================================================
    # INSURANCE DOCTRINES
    # ========================================================================

    "insurance_requirements": DoctrineBlock(
        topic="Insurance Requirements Analysis",
        category=ClauseCategory.INSURANCE,
        keywords=[
            "insurance requirement", "minimum insurance", "certificate of insurance",
            "additional insured", "professional liability", "errors and omissions",
            "general liability", "cyber insurance", "workers compensation",
        ],
        conclusion_template="""Insurance provisions require one or both parties to maintain specified
types and amounts of insurance as a condition of the contract. Analysis covers: (1) adequacy
of coverage types for the engagement, (2) minimum coverage amounts relative to risk exposure,
(3) additional insured requirements, (4) waiver of subrogation, (5) certificate of insurance
requirements, and (6) consequences of lapse in coverage.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. COVERAGE TYPES
   - Commercial General Liability (CGL): bodily injury, property damage
   - Professional Liability / E&O: professional negligence
   - Cyber Liability: data breaches, cyber incidents
   - Workers Compensation: statutory requirements
   - Auto Liability: if vehicles involved
   - Umbrella/Excess: above primary limits

2. COVERAGE AMOUNTS
   - CGL: $1M per occurrence / $2M aggregate (market standard)
   - Professional Liability: $1-5M depending on engagement
   - Cyber: $1-10M depending on data volume
   - Workers Comp: statutory limits

3. ADDITIONAL INSURED STATUS
   - Named as additional insured on CGL
   - Primary and non-contributory endorsement
   - Waiver of subrogation
   - Certificate of insurance requirements

4. ONGOING OBLIGATIONS
   - Maintain coverage for contract term + tail period
   - Notice of cancellation or material change
   - Annual renewal of certificates
   - Tail coverage for claims-made policies
""",
        key_factors=[
            "Coverage types appropriate for engagement",
            "Minimum amounts adequate for risk exposure",
            "Additional insured and subrogation waiver",
            "Certificate of insurance requirements",
            "Tail coverage for claims-made policies",
            "Consequences of coverage lapse",
        ],
        primary_authority=[
            {"authority": "Practice Guide", "reference": "ACORD Certificate of Insurance Standards"},
            {"authority": "Statute", "reference": "Workers Compensation statutes (state-specific)"},
        ],
        risk_severity=RiskSeverity.MEDIUM,
        risk_factors=[
            "Insurance minimums below likely exposure",
            "No cyber insurance for data-handling contracts",
            "No additional insured requirement",
            "Claims-made policy without tail coverage requirement",
            "No consequence for insurance lapse",
        ],
        mitigation_strategies=[
            "Set minimums based on realistic risk assessment",
            "Require cyber insurance for data-handling engagements",
            "Additional insured with primary and non-contributory",
            "Require tail coverage for 3 years post-termination",
            "Insurance lapse = material breach / suspension right",
        ],
        negotiation_guidance="""When negotiating insurance requirements:
1. Match coverage types to actual engagement risks
2. CGL: $1M/$2M minimum for most contracts
3. Professional Liability: 1-2x annual contract value
4. Cyber: $2-5M for contracts involving personal data
5. Additional insured with primary/non-contributory endorsement
6. Waiver of subrogation
7. 30-day notice of cancellation or material change
8. Tail coverage for claims-made policies (3 years minimum)""",
        common_pitfalls=[
            "Cookie-cutter insurance requirements without risk assessment",
            "No cyber insurance in data-heavy contracts",
            "Forgetting tail coverage for claims-made policies",
            "No mechanism to verify ongoing coverage",
        ],
        best_practices=[
            "Risk-based insurance requirements",
            "Annual certificate verification process",
            "Tail coverage requirement (3 years minimum)",
            "Insurance lapse = right to suspend until cured",
        ],
        related_doctrines=["indemnification_general", "limitation_of_liability"],
    ),

    # ========================================================================
    # SCOPE OF WORK DOCTRINES
    # ========================================================================

    "scope_of_work": DoctrineBlock(
        topic="Scope of Work / Change Order Analysis",
        category=ClauseCategory.SCOPE,
        keywords=[
            "scope of work", "sow", "statement of work", "deliverables",
            "change order", "change request", "scope creep", "out of scope",
            "acceptance criteria", "acceptance testing",
        ],
        conclusion_template="""Scope of work provisions define the services, deliverables, and
obligations under the contract. Change order provisions manage scope modifications.
Key analysis: (1) specificity of deliverable descriptions, (2) acceptance criteria
clarity, (3) change order process rigor, (4) scope creep prevention mechanisms,
(5) dependency management, and (6) milestone/payment alignment.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. SCOPE DEFINITION
   - Specificity of deliverable descriptions
   - Functional vs technical requirements
   - Acceptance criteria for each deliverable
   - Assumptions and dependencies listed

2. CHANGE ORDER PROCESS
   - Written change request required
   - Impact assessment (timeline, cost, resources)
   - Approval authority and process
   - Pricing for change orders (T&M, fixed, rate card)

3. ACCEPTANCE TESTING
   - Testing methodology and criteria
   - Testing period duration
   - Defect classification and resolution
   - Deemed acceptance after testing period

4. SCOPE MANAGEMENT
   - Out-of-scope work identification
   - Scope freeze mechanism
   - Authority to request changes
   - Impact on timeline and milestones
""",
        key_factors=[
            "Deliverable specificity and completeness",
            "Acceptance criteria clarity",
            "Change order process rigor",
            "Scope creep prevention",
            "Milestone/payment alignment",
            "Dependency and assumption documentation",
        ],
        primary_authority=[
            {"authority": "Practice Guide", "reference": "PMI PMBOK Guide - Scope Management"},
            {"authority": "Practice Guide", "reference": "IACCM Contract Management Standards"},
        ],
        risk_severity=RiskSeverity.MEDIUM,
        risk_factors=[
            "Vague deliverable descriptions",
            "No formal change order process",
            "Ambiguous acceptance criteria",
            "No scope freeze mechanism",
            "Milestones not aligned with payments",
        ],
        mitigation_strategies=[
            "Detailed SOW with specific acceptance criteria per deliverable",
            "Written change order process with impact assessment",
            "Reasonable acceptance testing period (10-20 business days)",
            "Deemed acceptance if no rejection within testing period",
            "Milestone payments tied to deliverable acceptance",
        ],
        negotiation_guidance="""When negotiating scope of work:
1. Define deliverables with specific, measurable acceptance criteria
2. Formal written change order process with impact assessment
3. Change orders must address timeline, cost, and resource impacts
4. Acceptance testing: 10-20 business days for standard deliverables
5. Deemed acceptance if no written rejection within testing period
6. Milestone payments tied to acceptance, not delivery
7. Document assumptions and dependencies explicitly""",
        common_pitfalls=[
            "Vague deliverables without measurable criteria",
            "No change order process (leading to scope creep)",
            "Acceptance testing period too short",
            "Payment on delivery rather than acceptance",
            "Undocumented assumptions that become disputes",
        ],
        best_practices=[
            "Specific deliverables with SMART criteria",
            "Formal change order with cost/timeline impact",
            "15-day acceptance testing with defect tiers",
            "Deemed acceptance mechanism",
            "Assumption and dependency register",
        ],
        related_doctrines=["payment_terms", "termination_for_cause"],
    ),
    # ========================================================================
    # SURVIVAL PROVISIONS DOCTRINES
    # ========================================================================

    "survival_provisions": DoctrineBlock(
        topic="Survival Provisions Analysis",
        category=ClauseCategory.TERMINATION,
        keywords=[
            "survival", "surviving provisions", "survives termination",
            "survives expiration", "post-termination obligations",
        ],
        conclusion_template="""Survival provisions specify which contractual obligations continue
after the contract terminates or expires. Analysis requires: (1) identification of which
provisions are designated as surviving, (2) whether survival is indefinite or for a
specified period, (3) whether key protective provisions (indemnification, confidentiality,
IP ownership, limitation of liability) are included, and (4) alignment between survival
periods and applicable statutes of limitation.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. SURVIVING PROVISIONS INVENTORY
   - Confidentiality obligations
   - Indemnification obligations
   - Limitation of liability
   - IP ownership and license grants
   - Payment obligations for pre-termination work
   - Representations and warranties (for claims period)
   - Non-compete/non-solicitation (for restricted period)
   - Audit rights (for tail period)
   - Data return/destruction obligations
   - Dispute resolution mechanism

2. DURATION OF SURVIVAL
   - Indefinite survival for IP ownership and trade secrets
   - Time-limited survival for confidentiality (3-5 years standard)
   - Statute of limitations alignment for indemnification
   - Specific period for non-compete (matches restriction period)
   - Duration adequate for parties to assert claims

3. IMPLICIT SURVIVAL
   - Some obligations survive by their nature even without express language
   - Payment obligations for services rendered generally survive
   - Accrued rights are generally preserved
   - Express listing preferred for certainty

4. INTERACTION WITH TERMINATION TYPE
   - Termination for cause: broader survival may be appropriate
   - Termination for convenience: balanced survival
   - Expiration: standard survival
   - Mutual agreement: parties can modify survival at termination
""",
        key_factors=[
            "Identification of all surviving provisions",
            "Duration of survival for each obligation",
            "Alignment with statutes of limitation",
            "IP ownership and license survival",
            "Confidentiality post-termination duration",
            "Payment obligation survival",
        ],
        primary_authority=[
            {"authority": "Case", "reference": "GE Energy Parts Inc. v. Nuclear Fuel Servs., Inc., 2017 WL 3149350"},
            {"authority": "Restatement", "reference": "Restatement (Second) of Contracts 279"},
            {"authority": "Practice Guide", "reference": "ABA Model Survival Provisions"},
        ],
        risk_severity=RiskSeverity.MEDIUM,
        risk_factors=[
            "Key protective provisions not listed as surviving",
            "Indefinite survival without justification",
            "Survival period shorter than statute of limitations",
            "No survival of indemnification obligations",
            "Confidentiality survival too short for trade secrets",
        ],
        mitigation_strategies=[
            "Expressly list all surviving provisions",
            "Align survival periods with applicable statutes of limitation",
            "Indefinite survival for IP ownership and trade secrets",
            "3-5 year survival for general confidentiality",
            "Include payment obligations for pre-termination work",
        ],
        negotiation_guidance="""When negotiating survival provisions:
1. Expressly list every provision that should survive termination
2. Confidentiality: 3-5 years for general CI, indefinite for trade secrets
3. Indemnification: align with statute of limitations (typically 3-6 years)
4. IP ownership: indefinite — ownership should not revert on termination
5. Payment: survive for all amounts accrued pre-termination
6. Limitation of liability: must survive to protect against post-termination claims
7. Dispute resolution: must survive to resolve post-termination disputes""",
        common_pitfalls=[
            "Omitting limitation of liability from survival clause",
            "Confidentiality survival too short (1 year vs 3-5 years)",
            "No survival of indemnification (defeats purpose)",
            "Not listing dispute resolution as surviving",
            "Blanket indefinite survival (may be overbroad)",
        ],
        best_practices=[
            "Express enumeration of all surviving provisions",
            "Tiered survival: indefinite (IP), 5-year (CI), 3-year (indemnity)",
            "Always include LOL and dispute resolution",
            "Payment survival for all accrued amounts",
            "Audit rights survive for 2 years post-termination",
        ],
        related_doctrines=["termination_for_cause", "termination_for_convenience", "confidentiality_nda"],
    ),

    # ========================================================================
    # DISPUTE ESCALATION DOCTRINES
    # ========================================================================

    "dispute_resolution": DoctrineBlock(
        topic="Dispute Resolution and Escalation Analysis",
        category=ClauseCategory.GOVERNING_LAW,
        keywords=[
            "dispute resolution", "escalation", "arbitration",
            "mediation", "litigation", "alternative dispute resolution",
            "adr", "mandatory arbitration",
        ],
        conclusion_template="""Dispute resolution provisions establish the mechanism for resolving
disagreements between the parties. Best practice involves a tiered escalation process:
(1) good-faith negotiation between relationship managers, (2) escalation to senior executives,
(3) mandatory mediation, and (4) binding arbitration or litigation. Key analysis includes
the choice between arbitration and litigation, preservation of injunctive relief rights,
discovery scope, appeal rights, and cost allocation.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. ESCALATION TIERS
   - Tier 1: Direct negotiation between designated representatives (10-15 days)
   - Tier 2: Senior executive escalation (15-30 days)
   - Tier 3: Non-binding mediation (30-60 days)
   - Tier 4: Binding arbitration or litigation

2. ARBITRATION vs LITIGATION
   - Arbitration: private, generally faster, limited discovery, limited appeal
   - Litigation: public, full discovery, appellate rights
   - Hybrid: arbitration with limited discovery rights
   - Consider complexity and value of likely disputes

3. ARBITRATION MECHANICS
   - Administering body: AAA, JAMS, ICC, LCIA
   - Number of arbitrators: one (smaller disputes) or three (complex)
   - Seat of arbitration
   - Language and procedural rules
   - Discovery scope and limitations
   - Appeal rights (limited by statute)
   - Confidentiality of proceedings

4. INJUNCTIVE RELIEF CARVE-OUT
   - Critical: preserve right to seek injunctive relief in court
   - Particularly for IP infringement and confidentiality breaches
   - Should not require exhaustion of escalation tiers
   - Temporary restraining orders and preliminary injunctions

5. COST ALLOCATION
   - Each party bears own costs vs loser-pays
   - Prevailing party attorneys' fees
   - Arbitrator/mediator fee allocation
   - Administrative costs
""",
        key_factors=[
            "Tiered escalation process",
            "Arbitration vs litigation election",
            "Injunctive relief carve-out",
            "Discovery scope in arbitration",
            "Cost and fee allocation",
            "Confidentiality of proceedings",
        ],
        primary_authority=[
            {"authority": "Statute", "reference": "Federal Arbitration Act, 9 U.S.C. 1-16"},
            {"authority": "Case", "reference": "AT&T Mobility LLC v. Concepcion, 563 U.S. 333 (2011)"},
            {"authority": "Case", "reference": "Stolt-Nielsen S.A. v. AnimalFeeds Int'l Corp., 559 U.S. 662 (2010)"},
            {"authority": "Practice Guide", "reference": "AAA Commercial Arbitration Rules"},
        ],
        risk_severity=RiskSeverity.MEDIUM,
        risk_factors=[
            "Mandatory arbitration without injunctive relief carve-out",
            "No escalation tiers (direct to arbitration/litigation)",
            "Loser-pays provision that deters meritorious claims",
            "Single arbitrator for complex disputes",
            "No confidentiality protection for proceedings",
        ],
        mitigation_strategies=[
            "Include three-tier escalation before arbitration",
            "Always carve out injunctive relief for IP and CI",
            "Three arbitrators for disputes over $1M",
            "Prevailing party attorneys' fees provision",
            "Confidentiality clause for arbitration proceedings",
        ],
        negotiation_guidance="""When negotiating dispute resolution:
1. Include tiered escalation: negotiation (15 days) → exec escalation (15 days) → mediation (30 days) → binding resolution
2. Arbitration for commercial disputes (faster, private)
3. ALWAYS carve out right to seek injunctive relief in court
4. Three arbitrators for high-value disputes (>$1M)
5. Include prevailing party attorneys' fees
6. Specify AAA or JAMS rules for predictability
7. Address class action waiver if B2C or employment context
8. Ensure confidentiality of proceedings""",
        common_pitfalls=[
            "No injunctive relief carve-out for IP/confidentiality",
            "Mandatory arbitration without discovery provisions",
            "Class action waiver that may be unenforceable in some contexts",
            "No cost allocation for frivolous claims",
            "Single arbitrator for complex multi-million dollar disputes",
        ],
        best_practices=[
            "Three-tier escalation before binding resolution",
            "Injunctive relief carve-out for IP and CI",
            "Prevailing party attorneys' fees",
            "Three arbitrators for disputes >$1M",
            "Confidentiality of arbitration proceedings",
        ],
        controlling_precedent=ControllingPrecedent(
            case_name="AT&T Mobility LLC v. Concepcion",
            citation="563 U.S. 333 (2011)",
            court="Supreme Court",
            holding="FAA preempts state laws that condition enforcement of arbitration on availability of class-wide procedures.",
            binding_scope="nationwide",
            year=2011,
        ),
        related_doctrines=["governing_law"],
    ),

    # ========================================================================
    # LICENSE GRANT DOCTRINES
    # ========================================================================

    "license_grant": DoctrineBlock(
        topic="License Grant and Software License Analysis",
        category=ClauseCategory.IP,
        keywords=[
            "license grant", "software license", "license to use",
            "perpetual license", "subscription license", "seat license",
            "enterprise license", "open source", "saas",
        ],
        conclusion_template="""License grants define the scope of rights granted to use software,
IP, or other proprietary materials. Key analysis dimensions: (1) scope of grant (exclusive
vs non-exclusive, territory, field of use), (2) duration (perpetual vs subscription/term),
(3) limitations and restrictions, (4) sublicense and assignment rights, (5) audit and
compliance mechanisms, and (6) consequences of breach or termination on license rights.
SaaS agreements may involve access rights rather than traditional license grants.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. SCOPE OF GRANT
   - Exclusive vs non-exclusive
   - Territory: worldwide vs limited
   - Field of use: unrestricted vs limited
   - Internal use only vs commercial distribution
   - Number of users/seats/instances
   - Affiliates included?

2. DURATION AND RENEWAL
   - Perpetual (survives termination of services agreement)
   - Subscription/term (expires with agreement)
   - Auto-renewal terms
   - Right to continue using after termination for what was paid for

3. RESTRICTIONS
   - No reverse engineering
   - No sublicensing without consent
   - No modification or derivative works
   - Use limitations (internal only, geographic, etc.)
   - Competitor restrictions
   - Open source compliance requirements

4. SAAS vs LICENSE DISTINCTION
   - SaaS: access to service, no license per se
   - On-premise license: right to install and use software
   - Hybrid: both access and downloadable components
   - Data portability rights in SaaS context

5. TERMINATION IMPACT
   - License survives termination of services (perpetual)
   - License terminates with agreement (subscription)
   - Wind-down period for transition
   - Data export rights
   - Return/destroy obligations for licensed materials
""",
        key_factors=[
            "Exclusive vs non-exclusive grant",
            "Perpetual vs subscription duration",
            "Territory and field of use restrictions",
            "Sublicense and assignment rights",
            "Audit and compliance mechanisms",
            "Termination impact on license rights",
        ],
        primary_authority=[
            {"authority": "Statute", "reference": "17 U.S.C. 106 - Exclusive Rights in Copyrighted Works"},
            {"authority": "Case", "reference": "Vernor v. Autodesk Inc., 621 F.3d 1102 (9th Cir. 2010)"},
            {"authority": "Case", "reference": "Oracle America Inc. v. Google LLC, 593 U.S. 1 (2021)"},
            {"authority": "UCC", "reference": "UCC 2B (proposed) - Licenses"},
        ],
        risk_severity=RiskSeverity.HIGH,
        risk_factors=[
            "License scope too narrow for intended use",
            "No perpetual license for paid software",
            "Unlimited audit rights without notice",
            "True-up provisions with uncapped retroactive liability",
            "No data portability in SaaS context",
        ],
        mitigation_strategies=[
            "Define license scope to cover all intended uses",
            "Negotiate perpetual license for on-premise software",
            "Limit audit frequency (once per year) with reasonable notice",
            "Cap true-up liability at reasonable multiple",
            "Include data export rights in SaaS agreements",
        ],
        negotiation_guidance="""When negotiating license grants:
1. Define scope clearly: users, instances, territory, field of use
2. For on-premise: push for perpetual license (survives termination)
3. For SaaS: ensure data portability and export rights
4. Audit rights: annual, with 30-day notice, during business hours
5. True-up provisions: cap retroactive liability, good faith dispute process
6. Open source: require disclosure of all OSS components and licenses
7. Consider escrow for source code access if vendor fails
8. Address affiliate use explicitly""",
        common_pitfalls=[
            "License scope does not cover all intended uses",
            "No perpetual option for paid on-premise software",
            "Unlimited audit without notice or frequency limits",
            "No data export in SaaS (vendor lock-in)",
            "Open source contamination risk not addressed",
        ],
        best_practices=[
            "Clear scope covering all anticipated uses",
            "Perpetual license for on-premise, data portability for SaaS",
            "Annual audit with 30-day notice",
            "Source code escrow for critical applications",
            "Open source disclosure schedule",
        ],
        controlling_precedent=ControllingPrecedent(
            case_name="Vernor v. Autodesk Inc.",
            citation="621 F.3d 1102 (9th Cir. 2010)",
            court="Circuit Court",
            holding="A software user is a licensee (not an owner) when the copyright owner retains title, limits transfer, and imposes use restrictions.",
            binding_scope="Ninth Circuit",
            year=2010,
        ),
        related_doctrines=["ip_ownership", "confidentiality_nda"],
    ),

    # ========================================================================
    # WARRANTY AND DISCLAIMER DOCTRINES
    # ========================================================================

    "warranty_disclaimer": DoctrineBlock(
        topic="Warranty and Disclaimer Analysis",
        category=ClauseCategory.REPRESENTATIONS,
        keywords=[
            "warranty disclaimer", "as-is", "no warranty", "implied warranty",
            "merchantability", "fitness for particular purpose",
            "warranty of title", "express warranty",
        ],
        conclusion_template="""Warranty disclaimer clauses limit or eliminate the seller/provider's
exposure for defects in goods or services. Under the UCC, implied warranties of merchantability
and fitness for particular purpose arise automatically in sales of goods unless properly
disclaimed. Key analysis: (1) conspicuousness and specificity of disclaimer language,
(2) UCC 2-316 requirements for disclaiming implied warranties, (3) interaction with
express warranties, (4) Magnuson-Moss Act limitations for consumer products, and
(5) whether 'as-is' language is sufficient in the applicable jurisdiction.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. IMPLIED WARRANTY DISCLAIMERS
   - Merchantability: must use the word 'merchantability' (UCC 2-316(2))
   - Fitness for particular purpose: must be in writing and conspicuous
   - 'As is' or 'with all faults': may disclaim all implied warranties (UCC 2-316(3))
   - Conspicuousness requirement: caps, bold, larger font, or contrasting color

2. EXPRESS WARRANTY LIMITATIONS
   - Express warranties created by: affirmations of fact, descriptions, samples
   - Cannot disclaim express warranties you've made (UCC 2-316(1))
   - Consistent reading doctrine: disclaimers should not negate express warranties
   - Limitation of remedy vs disclaimer of warranty (different concepts)

3. SERVICES vs GOODS
   - UCC implied warranties apply only to goods, not services
   - Services: common law standard of care applies
   - Professional services: professional standard of care (malpractice standard)
   - Mixed transactions: look at predominant purpose

4. CONSUMER PROTECTION
   - Magnuson-Moss: cannot disclaim implied warranties if express warranty given (consumer)
   - State consumer protection statutes may override disclaimers
   - Unconscionability defense available

5. LIMITATION OF REMEDY
   - Can limit remedy to repair, replacement, or refund
   - UCC 2-719: limitation fails of its essential purpose if exclusive remedy is inadequate
   - Consequential damage exclusion (separate from warranty disclaimer)
""",
        key_factors=[
            "UCC 2-316 compliance for implied warranty disclaimers",
            "Conspicuousness of disclaimer language",
            "Express warranty consistency",
            "Consumer vs commercial context",
            "Goods vs services classification",
            "Essential purpose failure risk",
        ],
        primary_authority=[
            {"authority": "UCC", "reference": "UCC 2-316 - Exclusion or Modification of Warranties"},
            {"authority": "UCC", "reference": "UCC 2-719 - Contractual Modification or Limitation of Remedy"},
            {"authority": "Statute", "reference": "Magnuson-Moss Warranty Act, 15 U.S.C. 2301-2312"},
            {"authority": "Case", "reference": "Henningsen v. Bloomfield Motors Inc., 32 N.J. 358 (1960)"},
        ],
        risk_severity=RiskSeverity.HIGH,
        risk_factors=[
            "Implied warranty disclaimer not conspicuous",
            "Express warranty inconsistent with disclaimer",
            "Consumer product — Magnuson-Moss limitations",
            "Essential purpose failure risk for limited remedies",
            "No warranty of title or non-infringement",
        ],
        mitigation_strategies=[
            "Ensure conspicuous formatting (ALL CAPS or bold)",
            "Use specific statutory language for merchantability",
            "Separate express warranties from disclaimers",
            "Include warranty of title and non-infringement",
            "Consider consumer protection compliance",
        ],
        negotiation_guidance="""When negotiating warranty provisions:
1. Sellers: disclaim implied warranties using UCC 2-316 specific language
2. Buyers: resist broad disclaimers — negotiate express warranties instead
3. Formatting: ALL CAPS or bold is critical for enforceability
4. Express warranties: define specifically what is and is not warranted
5. Limitation of remedy: repair/replace/refund, with consequential damages carve-outs
6. Warranty period: define clearly (12-24 months is standard)
7. Non-infringement warranty: important for technology contracts
8. Professional services: negotiate a standard of care warranty""",
        common_pitfalls=[
            "Disclaimer not conspicuous (buried in fine print)",
            "Missing the word 'merchantability' for UCC compliance",
            "Disclaiming express warranties you've actually made",
            "Consumer context where Magnuson-Moss applies",
            "Exclusive remedy that fails its essential purpose",
        ],
        best_practices=[
            "Conspicuous formatting (ALL CAPS or contrasting style)",
            "Specific mention of 'merchantability' and 'fitness'",
            "Clear separation of express warranties from disclaimers",
            "Non-infringement warranty for technology",
            "Repair/replace/refund with escalation path",
        ],
        controlling_precedent=ControllingPrecedent(
            case_name="Henningsen v. Bloomfield Motors Inc.",
            citation="32 N.J. 358, 161 A.2d 69 (1960)",
            court="State Supreme Court",
            holding="Warranty disclaimers in consumer contexts must meet standards of conspicuousness and fairness; unconscionable disclaimers are unenforceable.",
            binding_scope="persuasive nationwide",
            year=1960,
        ),
        related_doctrines=["limitation_of_liability", "representations_warranties"],
    ),

    # ========================================================================
    # CONSTRUCTION CONTRACT DOCTRINES
    # ========================================================================

    "construction_contract": DoctrineBlock(
        topic="Construction Contract Analysis",
        category=ClauseCategory.CONSTRUCTION,
        keywords=[
            "construction contract", "mechanic's lien", "lien waiver",
            "retainage", "substantial completion", "punch list",
            "aia contract", "design-build", "change directive",
            "time of the essence", "delay damages",
        ],
        conclusion_template="""Construction contracts involve unique legal considerations including:
(1) mechanic's lien rights and waiver requirements, (2) retainage obligations and release
conditions, (3) substantial vs final completion standards, (4) change order pricing and
dispute mechanisms, (5) delay and acceleration claims, (6) anti-indemnity statutes
applicable in construction, and (7) insurance and bonding requirements. Many jurisdictions
have construction-specific statutes that override general contract law.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. MECHANIC'S LIEN RIGHTS
   - State-specific lien statutes (strict compliance required)
   - Preliminary notice requirements (timing varies 20-90 days)
   - Lien filing deadlines
   - Conditional vs unconditional lien waivers
   - Progress payment lien waiver exchange
   - No-lien clause enforceability (varies by state)

2. RETAINAGE
   - Standard rate: 5-10% of each progress payment
   - Release conditions: substantial completion, punch list completion
   - Prompt Payment Act requirements (public contracts)
   - Flow-down to subcontractors
   - Interest on withheld retainage (some states require)

3. COMPLETION STANDARDS
   - Substantial completion: project usable for intended purpose
   - Final completion: all work done including punch list
   - Certificate of Substantial Completion (AIA G704)
   - Impact on warranty periods, liquidated damages, and retainage

4. CHANGE ORDERS
   - Written change order requirement
   - Pricing: lump sum, time & materials, unit price
   - Constructive change doctrine (owner-directed work without formal CO)
   - Claims for extra work (notice requirements critical)
   - CCD (Construction Change Directive) — proceed while pricing disputed

5. DELAY AND TIME CLAIMS
   - Excusable delay (force majeure, owner-caused)
   - Compensable delay (owner-caused, entitles time + money)
   - Concurrent delay (both parties at fault)
   - No-damage-for-delay clauses (limited enforceability in many states)
   - Acceleration claims (constructive or directed)
   - Float ownership

6. ANTI-INDEMNITY STATUTES
   - Many states prohibit broad-form indemnity in construction
   - Limited form: indemnify only for indemnitor's negligence
   - Intermediate form: indemnify except for indemnitee's sole negligence
   - State-specific analysis required
""",
        key_factors=[
            "Mechanic's lien compliance",
            "Retainage rate and release conditions",
            "Completion standards (substantial vs final)",
            "Change order pricing mechanism",
            "Delay claims and no-damage-for-delay enforceability",
            "Anti-indemnity statute compliance",
        ],
        primary_authority=[
            {"authority": "Statute", "reference": "Miller Act, 40 U.S.C. 3131 (federal bonding)"},
            {"authority": "Practice Guide", "reference": "AIA A201-2017 General Conditions"},
            {"authority": "Case", "reference": "Seaboard Surety Co. v. Dale Constr. Co., 230 F.2d 625 (1st Cir. 1956)"},
            {"authority": "Statute", "reference": "State mechanic's lien statutes (jurisdiction-specific)"},
        ],
        risk_severity=RiskSeverity.HIGH,
        risk_factors=[
            "Non-compliance with mechanic's lien notice deadlines",
            "Retainage release conditions too stringent",
            "No-damage-for-delay clause that may be unenforceable",
            "Broad-form indemnity in anti-indemnity statute state",
            "Inadequate change order process leading to claim disputes",
            "No substantial completion definition",
        ],
        mitigation_strategies=[
            "Comply with all mechanic's lien notice requirements",
            "Cap retainage at 5% with release at substantial completion",
            "Define substantial completion specifically",
            "Formal written change order process with pricing standards",
            "Include excusable delay provisions",
            "Check anti-indemnity statute compliance",
        ],
        negotiation_guidance="""When negotiating construction contracts:
1. Mechanic's liens: calendar all preliminary notice and filing deadlines
2. Retainage: negotiate 5% (not 10%) with release at substantial completion
3. Change orders: written process with CCD mechanism for disputes
4. Delay: include excusable and compensable delay provisions
5. Liquidated damages: cap at reasonable daily amount with defined completion date
6. Indemnification: check anti-indemnity statute for applicable jurisdiction
7. Insurance: CGL, builder's risk, professional liability (if design-build)
8. Bonding: payment and performance bonds per Miller Act or state equivalent
9. Warranty: 1-year from substantial completion is standard""",
        common_pitfalls=[
            "Missing mechanic's lien preliminary notice deadlines",
            "Broad-form indemnity in anti-indemnity statute state",
            "No written change order process",
            "No-damage-for-delay clause in jurisdiction that limits enforcement",
            "Retainage not released at substantial completion",
        ],
        best_practices=[
            "Calendar all lien notice deadlines immediately",
            "5% retainage with release at substantial completion",
            "Written change order process with CCD fallback",
            "Excusable and compensable delay provisions",
            "Anti-indemnity compliance review per jurisdiction",
        ],
        confidence_level=ConfidenceLevel.JURISDICTION_DEPENDENT,
        related_doctrines=["liquidated_damages", "indemnification_general", "insurance_requirements"],
        jurisdictional_notes=[
            "Texas: anti-indemnity applies to construction (Tex. Ins. Code 151.102)",
            "California: Civil Code 2782 limits construction indemnity",
            "New York: GOL 5-322.1 voids broad-form construction indemnity",
            "Florida: s. 725.06 limits construction indemnity",
            "Mechanic's lien requirements vary dramatically by state",
        ],
    ),

    # ========================================================================
    # OIL AND GAS LEASE DOCTRINES
    # ========================================================================

    "oil_gas_lease": DoctrineBlock(
        topic="Oil and Gas Lease Analysis",
        category=ClauseCategory.OIL_GAS,
        keywords=[
            "oil and gas lease", "mineral lease", "royalty interest",
            "working interest", "overriding royalty", "farmout",
            "joint operating agreement", "joa", "pooling",
            "unitization", "pugh clause", "habendum clause",
        ],
        conclusion_template="""Oil and gas lease analysis involves specialized contract law governing
the extraction of mineral resources. Key considerations include: (1) the granting clause
(minerals covered, depth limitations), (2) habendum clause (primary term and secondary term
conditions), (3) royalty provisions (fraction, costs deductible, market value vs gross proceeds),
(4) pooling and unitization authority, (5) surface use obligations, and (6) assignment and
change of operator provisions. These leases are heavily governed by state-specific oil and
gas law, with significant variation among producing states.""",
        reasoning_framework="""
ANALYSIS FRAMEWORK:

1. GRANTING CLAUSE
   - Minerals covered: oil, gas, and other minerals
   - Depth limitations: to a specific formation or all depths
   - Surface rights vs mineral rights delineation
   - Mother Hubbard clause (after-acquired interests)
   - Subject to existing burdens and encumbrances

2. HABENDUM CLAUSE
   - Primary term: typically 3-5 years
   - Secondary term: 'so long thereafter as oil or gas is produced'
   - Held by production requirements
   - Continuous drilling obligations
   - Shut-in royalty provisions (wells capable but not producing)
   - Operations clause (drilling operations maintain lease)

3. ROYALTY PROVISIONS
   - Royalty fraction: 1/8 (traditional), 1/5 or 1/4 (modern)
   - Market value vs gross proceeds (litigation-prone)
   - Post-production cost deductions (gathering, processing, transportation)
   - Free of cost vs at the well provisions
   - Royalty on gas used in operations

4. POOLING AND UNITIZATION
   - Pooling: combining tracts for drilling unit
   - Unitization: combining leases for reservoir management
   - Voluntary vs forced pooling (varies by state)
   - Pugh clause: unpooled acreage not held by pooled production
   - Cross-unit pooling limitations

5. SURFACE USE
   - Surface damage provisions
   - Restoration obligations
   - Water source protections
   - Road and pipeline easements
   - Accommodation doctrine (balancing surface and mineral rights)

6. ASSIGNMENT AND OPERATIONS
   - Assignment without consent (typical in O&G)
   - Change of operator provisions
   - JOA requirements (AAPL Form 610)
   - Preferential right to purchase
   - Area of mutual interest (AMI) provisions
""",
        key_factors=[
            "Granting clause scope and depth limitations",
            "Habendum clause and held-by-production conditions",
            "Royalty fraction and post-production cost treatment",
            "Pooling authority and Pugh clause protection",
            "Surface use and restoration obligations",
            "Assignment and operator change provisions",
        ],
        primary_authority=[
            {"authority": "Case", "reference": "Julander Energy Co. v. Saluda Resources, 294 P.3d 1 (Utah 2012)"},
            {"authority": "Statute", "reference": "Texas Natural Resources Code, Chapters 85-92"},
            {"authority": "Practice Guide", "reference": "AAPL Form 610 - Model Joint Operating Agreement"},
            {"authority": "Case", "reference": "Heritage Resources Inc. v. NationsBank, 939 S.W.2d 118 (Tex. 1996)"},
        ],
        risk_severity=RiskSeverity.HIGH,
        risk_factors=[
            "No Pugh clause (entire lease held by partial production)",
            "Post-production cost deductions reducing royalty",
            "Indefinite primary term without drilling commitment",
            "Broad pooling authority without acreage limitations",
            "No surface damage or restoration obligations",
            "No depth limitation on granting clause",
        ],
        mitigation_strategies=[
            "Include Pugh clause (horizontal and vertical)",
            "Negotiate 'at the well' or 'free of cost' royalty",
            "Limit primary term to 3 years with drilling commitment",
            "Cap pooling unit size (640 acres for oil, section for gas)",
            "Include surface damage and restoration provisions",
            "Add depth limitation to protect deeper formations",
        ],
        negotiation_guidance="""When negotiating oil and gas leases:
1. Royalty: negotiate 1/4 (25%) minimum in today's market
2. Post-production costs: 'at the well, free of cost' protects lessor
3. Pugh clause: essential to prevent entire lease being held by one well
4. Primary term: 3 years maximum with annual delay rental
5. Continuous drilling: require commencement within 1 year
6. Pooling: limit to regulatory spacing requirements
7. Surface damage: require restoration to original condition
8. Depth: consider depth limitation to retain deeper formations
9. Force pooling: ensure lessor retains override on force-pooled tracts""",
        common_pitfalls=[
            "No Pugh clause (common in older form leases)",
            "Allowing post-production cost deductions from royalty",
            "5-year primary term without drilling obligation",
            "Unlimited pooling authority",
            "No surface damage provisions",
        ],
        best_practices=[
            "1/4 royalty free of post-production costs",
            "Pugh clause (horizontal and vertical)",
            "3-year primary term with drilling commitment",
            "Pooling limited to regulatory spacing",
            "Surface damage and restoration requirements",
        ],
        confidence_level=ConfidenceLevel.JURISDICTION_DEPENDENT,
        related_doctrines=["assignment_change_of_control"],
        jurisdictional_notes=[
            "Texas: implied covenant to develop; marketable title doctrine",
            "Oklahoma: forced pooling under OCC regulations",
            "Pennsylvania: surface owner rights under Act 13",
            "Colorado: COGCC spacing and pooling rules",
            "New Mexico: royalty valuation at the well",
            "North Dakota: forced pooling after NDIC hearing",
        ],
        contract_types=["oil_gas_lease", "operating_agreement"],
    ),
}


# ============================================================================
# DOCTRINE INTERACTION GRAPH
# ============================================================================

DOCTRINE_INTERACTIONS: List[DoctrineInteraction] = [
    DoctrineInteraction(
        source_topic="limitation_of_liability",
        target_topic="indemnification_general",
        interaction_type="limits",
        description="Liability cap should apply to indemnification obligations unless carved out.",
    ),
    DoctrineInteraction(
        source_topic="consequential_damages_exclusion",
        target_topic="indemnification_general",
        interaction_type="limits",
        description="Consequential damages exclusion may limit types of recoverable indemnification losses.",
    ),
    DoctrineInteraction(
        source_topic="limitation_of_liability",
        target_topic="consequential_damages_exclusion",
        interaction_type="enables",
        description="These clauses form the core risk allocation framework and should be read together.",
    ),
    DoctrineInteraction(
        source_topic="termination_for_cause",
        target_topic="termination_for_convenience",
        interaction_type="overrides",
        description="For-cause termination typically has different (and more urgent) notice/cure requirements.",
    ),
    DoctrineInteraction(
        source_topic="force_majeure",
        target_topic="termination_for_cause",
        interaction_type="limits",
        description="Force majeure excuses performance, preventing nonperformance from constituting breach.",
    ),
    DoctrineInteraction(
        source_topic="ip_ownership",
        target_topic="confidentiality_nda",
        interaction_type="enables",
        description="IP ownership provisions often require confidentiality to protect the IP.",
    ),
    DoctrineInteraction(
        source_topic="confidentiality_nda",
        target_topic="data_protection",
        interaction_type="enables",
        description="Confidentiality obligations support but do not replace data protection requirements.",
    ),
    DoctrineInteraction(
        source_topic="representations_warranties",
        target_topic="indemnification_general",
        interaction_type="enables",
        description="R&W breaches typically trigger indemnification obligations.",
    ),
    DoctrineInteraction(
        source_topic="assignment_change_of_control",
        target_topic="termination_for_cause",
        interaction_type="enables",
        description="Unauthorized assignment may constitute a material breach triggering termination.",
    ),
    DoctrineInteraction(
        source_topic="payment_terms",
        target_topic="termination_for_cause",
        interaction_type="enables",
        description="Non-payment is typically a per se material breach triggering termination rights.",
    ),
    DoctrineInteraction(
        source_topic="service_level_agreement",
        target_topic="termination_for_cause",
        interaction_type="enables",
        description="Chronic SLA failure may constitute material breach.",
    ),
    DoctrineInteraction(
        source_topic="insurance_requirements",
        target_topic="indemnification_general",
        interaction_type="enables",
        description="Insurance backs indemnification obligations, making them financially meaningful.",
    ),
    DoctrineInteraction(
        source_topic="scope_of_work",
        target_topic="payment_terms",
        interaction_type="enables",
        description="Payment milestones are typically tied to deliverable acceptance under the SOW.",
    ),
    DoctrineInteraction(
        source_topic="auto_renewal",
        target_topic="termination_for_convenience",
        interaction_type="limits",
        description="Auto-renewal may limit termination for convenience to the non-renewal window.",
    ),
    DoctrineInteraction(
        source_topic="restrictive_covenants",
        target_topic="confidentiality_nda",
        interaction_type="enables",
        description="Restrictive covenants supplement confidentiality by preventing competitive use of information.",
    ),
    DoctrineInteraction(
        source_topic="limitation_of_liability",
        target_topic="liquidated_damages",
        interaction_type="limits",
        description="Liquidated damages may or may not be subject to the overall liability cap.",
    ),
    DoctrineInteraction(
        source_topic="data_protection",
        target_topic="limitation_of_liability",
        interaction_type="limits",
        description="Data breach liabilities are often carved out from standard liability caps.",
    ),
]


# ============================================================================
# DOCTRINE COVERAGE MAP
# ============================================================================

class DoctrineCoverageMap:
    """Track which doctrines were triggered and which were not for a given analysis.

    Provides epistemic transparency by showing what the engine DID and
    DIDN'T analyze, allowing practitioners to identify gaps.
    """

    def __init__(self) -> None:
        self._all_doctrines = set(DOCTRINE_CACHE.keys())
        self._triggered: set = set()
        self._not_triggered: set = set()

    def mark_triggered(self, doctrine_key: str) -> None:
        """Mark a doctrine as triggered during analysis."""
        self._triggered.add(doctrine_key)

    def mark_not_triggered(self, doctrine_key: str) -> None:
        """Mark a doctrine as evaluated but not triggered."""
        self._not_triggered.add(doctrine_key)

    def get_coverage_report(self) -> Dict[str, Any]:
        """Generate coverage report showing analysis gaps."""
        not_evaluated = self._all_doctrines - self._triggered - self._not_triggered
        coverage_pct = len(self._triggered) / max(1, len(self._all_doctrines))
        return {
            "total_doctrines": len(self._all_doctrines),
            "triggered": sorted(self._triggered),
            "evaluated_not_triggered": sorted(self._not_triggered),
            "not_evaluated": sorted(not_evaluated),
            "coverage_percentage": round(coverage_pct * 100, 1),
            "gaps": sorted(not_evaluated),
        }


# ============================================================================
# DOCTRINE LOOKUP FUNCTIONS
# ============================================================================

def get_all_doctrine_keys() -> List[str]:
    """Get all doctrine keys in the cache."""
    return sorted(DOCTRINE_CACHE.keys())


def get_doctrine(key: str) -> Optional[DoctrineBlock]:
    """Get a specific doctrine by key."""
    return DOCTRINE_CACHE.get(key)


def get_doctrines_by_category(category: ClauseCategory) -> Dict[str, DoctrineBlock]:
    """Get all doctrines in a specific category."""
    return {k: v for k, v in DOCTRINE_CACHE.items() if v.category == category}


def get_doctrine_count() -> int:
    """Get total number of doctrines in the cache."""
    return len(DOCTRINE_CACHE)


def get_interaction_edges_for(doctrine_key: str) -> List[DoctrineInteraction]:
    """Get all interaction edges involving a specific doctrine."""
    return [
        edge for edge in DOCTRINE_INTERACTIONS
        if edge.source_topic == doctrine_key or edge.target_topic == doctrine_key
    ]


def get_all_categories() -> List[str]:
    """Get all unique categories in the doctrine cache."""
    return sorted(set(d.category.value for d in DOCTRINE_CACHE.values()))


def search_doctrines(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """Search doctrines by keyword matching across topics and keywords.

    Args:
        query: Search query string.
        max_results: Maximum number of results to return.

    Returns:
        List of matching doctrines with relevance scores.
    """
    query_lower = query.lower()
    query_terms = query_lower.split()
    results: List[Dict[str, Any]] = []

    for key, doctrine in DOCTRINE_CACHE.items():
        score = 0.0
        matched_terms: List[str] = []

        # Topic match (highest weight)
        topic_lower = doctrine.topic.lower()
        for term in query_terms:
            if term in topic_lower:
                score += 10.0
                matched_terms.append(f"topic:{term}")

        # Keyword match (high weight)
        keywords_lower = [k.lower() for k in doctrine.keywords]
        for term in query_terms:
            for kw in keywords_lower:
                if term in kw:
                    score += 5.0
                    matched_terms.append(f"keyword:{kw}")
                    break

        # Category match (medium weight)
        if query_lower in doctrine.category.value.lower():
            score += 3.0
            matched_terms.append(f"category:{doctrine.category.value}")

        # Key factors match (lower weight)
        for factor in doctrine.key_factors:
            factor_lower = factor.lower()
            for term in query_terms:
                if term in factor_lower:
                    score += 1.0
                    matched_terms.append(f"factor:{term}")

        # Conclusion template match
        if doctrine.conclusion_template:
            template_lower = doctrine.conclusion_template.lower()
            for term in query_terms:
                if term in template_lower:
                    score += 0.5

        if score > 0:
            results.append({
                "key": key,
                "topic": doctrine.topic,
                "category": doctrine.category.value,
                "score": round(score, 2),
                "matched_terms": matched_terms[:10],
                "risk_severity": doctrine.risk_severity,
                "keywords": doctrine.keywords[:5],
            })

    # Sort by score descending
    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:max_results]


def get_doctrine_graph() -> Dict[str, Any]:
    """Build a doctrine interaction graph for visualization.

    Returns:
        Dictionary containing nodes (doctrines) and edges (interactions)
        suitable for graph rendering.
    """
    nodes = []
    for key, doctrine in DOCTRINE_CACHE.items():
        nodes.append({
            "id": key,
            "topic": doctrine.topic,
            "category": doctrine.category.value,
            "risk_severity": doctrine.risk_severity,
            "keyword_count": len(doctrine.keywords),
            "has_precedent": bool(doctrine.controlling_precedent),
        })

    edges = []
    for interaction in DOCTRINE_INTERACTIONS:
        edges.append({
            "source": interaction.source_topic,
            "target": interaction.target_topic,
            "relationship": interaction.relationship,
            "strength": interaction.interaction_strength,
            "is_bidirectional": interaction.is_bidirectional,
        })

    return {
        "nodes": nodes,
        "edges": edges,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "categories": get_all_categories(),
        "density": (
            (2 * len(edges)) / (len(nodes) * (len(nodes) - 1))
            if len(nodes) > 1 else 0.0
        ),
    }


def get_doctrine_coverage_summary() -> Dict[str, Any]:
    """Generate summary statistics about doctrine coverage.

    Returns:
        Dictionary with coverage metrics including category distribution,
        risk distribution, interaction density, and identified gaps.
    """
    # Category distribution
    category_counts: Dict[str, int] = {}
    for doctrine in DOCTRINE_CACHE.values():
        cat = doctrine.category.value
        category_counts[cat] = category_counts.get(cat, 0) + 1

    # Risk distribution
    risk_counts: Dict[str, int] = {}
    for doctrine in DOCTRINE_CACHE.values():
        risk = doctrine.risk_severity
        risk_counts[risk] = risk_counts.get(risk, 0) + 1

    # Interaction coverage
    doctrines_with_interactions: set = set()
    for interaction in DOCTRINE_INTERACTIONS:
        doctrines_with_interactions.add(interaction.source_topic)
        doctrines_with_interactions.add(interaction.target_topic)

    orphaned = [
        key for key in DOCTRINE_CACHE.keys()
        if key not in doctrines_with_interactions
    ]

    # Authority coverage
    doctrines_with_precedent = sum(
        1 for d in DOCTRINE_CACHE.values() if d.controlling_precedent
    )

    # Pitfall coverage
    total_pitfalls = sum(len(d.common_pitfalls) for d in DOCTRINE_CACHE.values())
    total_best_practices = sum(len(d.best_practices) for d in DOCTRINE_CACHE.values())
    total_mitigations = sum(len(d.mitigation_strategies) for d in DOCTRINE_CACHE.values())

    return {
        "total_doctrines": len(DOCTRINE_CACHE),
        "total_interactions": len(DOCTRINE_INTERACTIONS),
        "category_distribution": category_counts,
        "risk_distribution": risk_counts,
        "doctrines_with_interactions": len(doctrines_with_interactions),
        "orphaned_doctrines": orphaned,
        "orphaned_count": len(orphaned),
        "doctrines_with_precedent": doctrines_with_precedent,
        "precedent_coverage_pct": round(
            (doctrines_with_precedent / len(DOCTRINE_CACHE) * 100) if DOCTRINE_CACHE else 0, 1
        ),
        "total_pitfalls_documented": total_pitfalls,
        "total_best_practices": total_best_practices,
        "total_mitigation_strategies": total_mitigations,
        "avg_pitfalls_per_doctrine": round(
            total_pitfalls / len(DOCTRINE_CACHE) if DOCTRINE_CACHE else 0, 1
        ),
        "avg_best_practices_per_doctrine": round(
            total_best_practices / len(DOCTRINE_CACHE) if DOCTRINE_CACHE else 0, 1
        ),
    }


def validate_doctrine_integrity() -> Dict[str, Any]:
    """Validate the integrity and completeness of all doctrine blocks.

    Checks for missing fields, incomplete content, and cross-reference
    consistency.

    Returns:
        Dictionary with validation results including warnings and errors.
    """
    warnings: List[str] = []
    errors: List[str] = []

    for key, doctrine in DOCTRINE_CACHE.items():
        # Check required content
        if not doctrine.topic:
            errors.append(f"{key}: Missing topic")
        if not doctrine.keywords:
            errors.append(f"{key}: No keywords defined")
        if len(doctrine.keywords) < 3:
            warnings.append(f"{key}: Only {len(doctrine.keywords)} keywords (recommend 3+)")
        if not doctrine.conclusion_template:
            warnings.append(f"{key}: No conclusion template")
        if not doctrine.reasoning_framework:
            warnings.append(f"{key}: No reasoning framework")
        if not doctrine.key_factors:
            errors.append(f"{key}: No key factors defined")
        if not doctrine.primary_authority:
            warnings.append(f"{key}: No primary authority cited")
        if not doctrine.risk_factors:
            warnings.append(f"{key}: No risk factors defined")
        if not doctrine.mitigation_strategies:
            warnings.append(f"{key}: No mitigation strategies")
        if not doctrine.negotiation_guidance:
            warnings.append(f"{key}: No negotiation guidance")
        if not doctrine.common_pitfalls:
            warnings.append(f"{key}: No common pitfalls documented")
        if not doctrine.best_practices:
            warnings.append(f"{key}: No best practices documented")

        # Check content quality (minimum word counts)
        if doctrine.reasoning_framework and len(doctrine.reasoning_framework.split()) < 10:
            warnings.append(f"{key}: Reasoning framework too brief ({len(doctrine.reasoning_framework.split())} words)")
        if doctrine.conclusion_template and len(doctrine.conclusion_template.split()) < 5:
            warnings.append(f"{key}: Conclusion template too brief")

    # Check interaction references
    all_doctrine_keys = set(DOCTRINE_CACHE.keys())
    for interaction in DOCTRINE_INTERACTIONS:
        if interaction.source_topic not in all_doctrine_keys:
            errors.append(
                f"Interaction references non-existent source: {interaction.source_topic}"
            )
        if interaction.target_topic not in all_doctrine_keys:
            errors.append(
                f"Interaction references non-existent target: {interaction.target_topic}"
            )

    return {
        "valid": len(errors) == 0,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "doctrines_checked": len(DOCTRINE_CACHE),
        "interactions_checked": len(DOCTRINE_INTERACTIONS),
    }
