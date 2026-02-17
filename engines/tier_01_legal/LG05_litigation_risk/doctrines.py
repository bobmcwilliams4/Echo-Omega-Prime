"""
LG05 LITIGATION RISK ENGINE - Doctrine Cache
Pre-compiled expert reasoning blocks for deterministic litigation risk assessment.

Engine: LG05 | Tier: 1 (LEGAL) | Mode: DET | Port: 8395 | Authority: 5.0
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any


class AuthorityLevel(str, Enum):
    STATUTE = "statute"
    REGULATION = "regulation"
    CASE_LAW = "case_law"
    RESTATEMENT = "restatement"
    TREATISE = "treatise"
    PRACTICE_GUIDE = "practice_guide"

    @property
    def weight(self) -> int:
        weights = {"statute": 100, "regulation": 80, "case_law": 60,
                   "restatement": 50, "treatise": 30, "practice_guide": 20}
        return weights.get(self.value, 10)


class ConfidenceLevel(str, Enum):
    WELL_SETTLED = "well_settled"
    GENERALLY_ACCEPTED = "generally_accepted"
    JURISDICTION_DEPENDENT = "jurisdiction_dependent"
    EVOLVING_LAW = "evolving_law"
    HIGH_RISK = "high_risk"


class RiskSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NEGLIGIBLE = "negligible"


class LitigationCategory(str, Enum):
    CIVIL_PROCEDURE = "civil_procedure"
    TORT_LIABILITY = "tort_liability"
    CONTRACT_DISPUTE = "contract_dispute"
    EMPLOYMENT = "employment"
    SECURITIES = "securities"
    ANTITRUST = "antitrust"
    IP_LITIGATION = "ip_litigation"
    ENVIRONMENTAL = "environmental"
    PRODUCTS_LIABILITY = "products_liability"
    INSURANCE = "insurance"
    REGULATORY = "regulatory"
    CLASS_ACTION = "class_action"


@dataclass
class ControllingPrecedent:
    case_name: str
    citation: str
    year: int
    court: str
    holding: str
    relevance_score: float = 0.8


@dataclass
class DoctrineInteraction:
    source_key: str
    target_key: str
    relationship: str
    strength: float
    description: str


@dataclass
class DoctrineBlock:
    key: str
    topic: str
    category: LitigationCategory
    keywords: List[str]
    conclusion_template: str
    analysis_framework: List[str]
    key_factors: List[str]
    authority: AuthorityLevel
    confidence: ConfidenceLevel
    risk_severity: RiskSeverity
    precedents: List[ControllingPrecedent]
    jurisdiction_notes: str
    risk_multipliers: Dict[str, float] = field(default_factory=dict)
    damages_guidance: str = ""
    settlement_factors: List[str] = field(default_factory=list)
    statute_of_limitations_years: Optional[float] = None
    burden_of_proof: str = "preponderance_of_evidence"


class DoctrineCoverageMap:
    def __init__(self, doctrines: Dict[str, DoctrineBlock]) -> None:
        self._doctrines = doctrines
        self._category_map: Dict[str, List[str]] = {}
        for key, block in doctrines.items():
            cat = block.category.value
            if cat not in self._category_map:
                self._category_map[cat] = []
            self._category_map[cat].append(key)

    def get_coverage_stats(self) -> Dict[str, Any]:
        return {
            "total_doctrines": len(self._doctrines),
            "categories": {k: len(v) for k, v in self._category_map.items()},
            "total_categories": len(self._category_map),
        }

    def get_uncovered_categories(self) -> List[str]:
        all_cats = {c.value for c in LitigationCategory}
        covered = set(self._category_map.keys())
        return sorted(all_cats - covered)

    def get_doctrines_for_category(self, category: str) -> List[str]:
        return self._category_map.get(category, [])


# ============================================================================
# DOCTRINE BLOCKS (50+)
# ============================================================================

DOCTRINE_CACHE: Dict[str, DoctrineBlock] = {}

# --- CIVIL PROCEDURE ---

DOCTRINE_CACHE["standing_article_iii"] = DoctrineBlock(
    key="standing_article_iii",
    topic="Article III Standing Requirements",
    category=LitigationCategory.CIVIL_PROCEDURE,
    keywords=["standing", "injury in fact", "causation", "redressability", "article iii"],
    conclusion_template="Standing analysis requires: (1) injury in fact that is concrete and particularized, (2) causal connection between injury and challenged conduct, (3) likelihood that a favorable decision will redress the injury. Failure on any prong is fatal to the claim.",
    analysis_framework=["Identify the alleged injury", "Assess concreteness and particularization", "Evaluate causal chain from defendant conduct to injury", "Determine if judicial relief can remedy the harm", "Check for organizational or associational standing"],
    key_factors=["injury_concreteness", "causal_traceability", "redressability", "procedural_injury", "informational_injury"],
    authority=AuthorityLevel.CASE_LAW,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.HIGH,
    precedents=[
        ControllingPrecedent("Lujan v. Defenders of Wildlife", "504 U.S. 555", 1992, "SCOTUS", "Established three-part standing test: injury in fact, causation, redressability"),
        ControllingPrecedent("Spokeo v. Robins", "578 U.S. 330", 2016, "SCOTUS", "Injury must be concrete even if intangible; bare procedural violation insufficient"),
        ControllingPrecedent("TransUnion v. Ramirez", "594 U.S. 413", 2021, "SCOTUS", "Only plaintiffs concretely harmed have Article III standing to seek damages"),
    ],
    jurisdiction_notes="Standing is a constitutional requirement in federal court. State courts may have broader standing rules.",
    risk_multipliers={"no_concrete_injury": 2.0, "speculative_harm": 1.5, "third_party_standing": 1.3},
    statute_of_limitations_years=None,
    burden_of_proof="preponderance_of_evidence",
)

DOCTRINE_CACHE["personal_jurisdiction"] = DoctrineBlock(
    key="personal_jurisdiction",
    topic="Personal Jurisdiction Analysis",
    category=LitigationCategory.CIVIL_PROCEDURE,
    keywords=["personal jurisdiction", "minimum contacts", "long arm", "due process", "specific jurisdiction", "general jurisdiction"],
    conclusion_template="Personal jurisdiction requires minimum contacts with the forum state such that maintenance of the suit does not offend traditional notions of fair play and substantial justice. General jurisdiction requires contacts so continuous and systematic as to render the defendant essentially at home.",
    analysis_framework=["Determine if general or specific jurisdiction applies", "Analyze minimum contacts with forum state", "Apply purposeful availment test", "Assess relatedness of contacts to claims", "Evaluate reasonableness factors"],
    key_factors=["contacts_with_forum", "purposeful_availment", "relatedness_of_claims", "reasonableness", "forum_selection_clause"],
    authority=AuthorityLevel.CASE_LAW,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.HIGH,
    precedents=[
        ControllingPrecedent("International Shoe v. Washington", "326 U.S. 310", 1945, "SCOTUS", "Established minimum contacts framework for personal jurisdiction"),
        ControllingPrecedent("Daimler AG v. Bauman", "571 U.S. 117", 2014, "SCOTUS", "Narrowed general jurisdiction to state of incorporation or principal place of business"),
        ControllingPrecedent("Bristol-Myers Squibb v. Superior Court", "582 U.S. 255", 2017, "SCOTUS", "Specific jurisdiction requires connection between forum contacts and underlying controversy"),
    ],
    jurisdiction_notes="Each state has its own long-arm statute. Some extend to constitutional limits; others are more restrictive.",
    risk_multipliers={"no_forum_contacts": 2.5, "internet_only_contacts": 1.8, "contract_forum_clause": 0.5},
    statute_of_limitations_years=None,
)

DOCTRINE_CACHE["venue_analysis"] = DoctrineBlock(
    key="venue_analysis",
    topic="Venue Selection and Transfer",
    category=LitigationCategory.CIVIL_PROCEDURE,
    keywords=["venue", "transfer", "forum non conveniens", "28 usc 1391", "forum selection"],
    conclusion_template="Venue is proper where any defendant resides (if all reside in same state), where a substantial part of events giving rise to the claim occurred, or as a fallback where any defendant is subject to personal jurisdiction. Forum selection clauses are presumptively enforceable.",
    analysis_framework=["Identify proper venue under 28 USC 1391", "Evaluate forum selection clause enforceability", "Assess convenience of parties and witnesses", "Consider transfer under 28 USC 1404(a)", "Analyze forum non conveniens factors"],
    key_factors=["defendant_residence", "events_location", "witness_convenience", "forum_clause", "public_interest_factors"],
    authority=AuthorityLevel.STATUTE,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.MEDIUM,
    precedents=[
        ControllingPrecedent("Atlantic Marine v. U.S. District Court", "571 U.S. 49", 2013, "SCOTUS", "Forum selection clauses are given controlling weight in all but exceptional cases"),
        ControllingPrecedent("Piper Aircraft v. Reyno", "454 U.S. 235", 1981, "SCOTUS", "Forum non conveniens analysis framework for federal courts"),
    ],
    jurisdiction_notes="Federal venue is governed by 28 USC 1391. State venue rules vary significantly.",
    risk_multipliers={"unfavorable_venue": 1.4, "forum_clause_present": 0.6},
    statute_of_limitations_years=None,
)

DOCTRINE_CACHE["subject_matter_jurisdiction"] = DoctrineBlock(
    key="subject_matter_jurisdiction",
    topic="Subject Matter Jurisdiction",
    category=LitigationCategory.CIVIL_PROCEDURE,
    keywords=["subject matter jurisdiction", "federal question", "diversity", "amount in controversy", "removal"],
    conclusion_template="Federal courts have limited subject matter jurisdiction: federal question (28 USC 1331) or diversity of citizenship with amount in controversy exceeding $75,000 (28 USC 1332). Subject matter jurisdiction cannot be waived and can be raised at any time.",
    analysis_framework=["Determine if federal question jurisdiction exists", "Analyze complete diversity requirement", "Calculate amount in controversy", "Consider supplemental jurisdiction for related claims", "Evaluate removal eligibility and timing"],
    key_factors=["federal_question_presence", "diversity_status", "amount_in_controversy", "supplemental_claims", "removal_deadline"],
    authority=AuthorityLevel.STATUTE,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.CRITICAL,
    precedents=[
        ControllingPrecedent("Exxon Mobil Corp. v. Allapattah Services", "545 U.S. 546", 2005, "SCOTUS", "Supplemental jurisdiction allows claims below amount in controversy when at least one named plaintiff meets threshold"),
    ],
    jurisdiction_notes="Cannot be waived. Court must dismiss if it lacks subject matter jurisdiction at any stage.",
    risk_multipliers={"no_federal_question": 1.8, "incomplete_diversity": 2.0},
    statute_of_limitations_years=None,
)

DOCTRINE_CACHE["joinder_and_consolidation"] = DoctrineBlock(
    key="joinder_and_consolidation",
    topic="Joinder of Parties and Claims",
    category=LitigationCategory.CIVIL_PROCEDURE,
    keywords=["joinder", "consolidation", "impleader", "interpleader", "intervention", "rule 19", "rule 20"],
    conclusion_template="Permissive joinder under Rule 20 allows parties to join if claims arise from same transaction or occurrence and share common questions. Required joinder under Rule 19 mandates joinder of parties needed for just adjudication. Failure to join an indispensable party may require dismissal.",
    analysis_framework=["Identify all potential parties", "Assess Rule 20 permissive joinder criteria", "Determine if any party is indispensable under Rule 19", "Evaluate third-party claims under Rule 14", "Consider intervention requests under Rule 24"],
    key_factors=["common_transaction", "common_questions", "indispensable_parties", "third_party_liability", "intervention_right"],
    authority=AuthorityLevel.STATUTE,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.MEDIUM,
    precedents=[
        ControllingPrecedent("Temple v. Synthes Corp.", "498 U.S. 5", 1990, "SCOTUS", "Joint tortfeasors are not indispensable parties under Rule 19"),
    ],
    jurisdiction_notes="Federal Rules of Civil Procedure govern joinder in federal court. State rules may differ.",
    risk_multipliers={"missing_indispensable_party": 2.0, "complex_multiparty": 1.3},
    statute_of_limitations_years=None,
)

# --- TORT LIABILITY ---

DOCTRINE_CACHE["negligence_elements"] = DoctrineBlock(
    key="negligence_elements",
    topic="Negligence Elements and Analysis",
    category=LitigationCategory.TORT_LIABILITY,
    keywords=["negligence", "duty", "breach", "causation", "damages", "reasonable care", "proximate cause"],
    conclusion_template="Negligence requires: (1) duty of care owed to plaintiff, (2) breach of that duty, (3) actual and proximate causation, (4) legally cognizable damages. The standard is what a reasonably prudent person would do under similar circumstances.",
    analysis_framework=["Identify the duty of care and its scope", "Determine whether conduct fell below standard of care", "Establish but-for causation", "Analyze proximate cause and foreseeability", "Quantify compensable damages"],
    key_factors=["duty_scope", "standard_of_care", "breach_evidence", "but_for_causation", "foreseeability", "damages_proof"],
    authority=AuthorityLevel.RESTATEMENT,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.HIGH,
    precedents=[
        ControllingPrecedent("Palsgraf v. Long Island Railroad", "248 N.Y. 339", 1928, "NY Court of Appeals", "Duty of care limited to foreseeable plaintiffs within zone of danger"),
        ControllingPrecedent("Donoghue v. Stevenson", "[1932] AC 562", 1932, "House of Lords", "Manufacturer owes duty of care to ultimate consumer (neighbor principle)"),
    ],
    jurisdiction_notes="Negligence standards are state law. Comparative vs. contributory negligence rules vary by jurisdiction.",
    risk_multipliers={"clear_duty": 0.8, "disputed_causation": 1.5, "speculative_damages": 1.4},
    damages_guidance="Compensatory damages for actual losses. No punitive damages for ordinary negligence in most jurisdictions.",
    settlement_factors=["strength_of_causation", "damages_documentation", "plaintiff_sympathy", "defense_resources"],
    statute_of_limitations_years=2.0,
    burden_of_proof="preponderance_of_evidence",
)

DOCTRINE_CACHE["strict_liability_tort"] = DoctrineBlock(
    key="strict_liability_tort",
    topic="Strict Liability in Tort",
    category=LitigationCategory.TORT_LIABILITY,
    keywords=["strict liability", "abnormally dangerous", "ultrahazardous", "defective product", "no fault"],
    conclusion_template="Strict liability imposes liability without proof of negligence for: (1) abnormally dangerous activities, (2) defective products under Restatement (Third), (3) keeping wild animals. The key is that defendant engaged in the activity or placed the product in the stream of commerce.",
    analysis_framework=["Determine if activity qualifies as abnormally dangerous", "Apply Restatement (Second) Section 520 factors", "Assess whether product was defective when it left defendant control", "Identify available defenses (assumption of risk, misuse)", "Calculate strict liability damages exposure"],
    key_factors=["activity_danger_level", "common_usage", "appropriateness_of_location", "product_defect_type", "user_misuse"],
    authority=AuthorityLevel.RESTATEMENT,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.CRITICAL,
    precedents=[
        ControllingPrecedent("Rylands v. Fletcher", "LR 3 HL 330", 1868, "House of Lords", "Strict liability for non-natural use of land causing damage to neighbors"),
        ControllingPrecedent("Greenman v. Yuba Power Products", "59 Cal.2d 57", 1963, "Cal. Supreme Court", "Manufacturer strictly liable for defective products placed in stream of commerce"),
    ],
    jurisdiction_notes="Some jurisdictions limit strict liability to manufacturing defects only. Design defect may require negligence-like analysis.",
    risk_multipliers={"clear_defect": 0.7, "abnormally_dangerous_activity": 0.6, "product_misuse": 1.5},
    damages_guidance="Full compensatory damages. Punitive damages possible if conduct was egregious.",
    statute_of_limitations_years=2.0,
)

DOCTRINE_CACHE["intentional_tort_analysis"] = DoctrineBlock(
    key="intentional_tort_analysis",
    topic="Intentional Tort Framework",
    category=LitigationCategory.TORT_LIABILITY,
    keywords=["intentional tort", "assault", "battery", "false imprisonment", "iied", "trespass", "conversion"],
    conclusion_template="Intentional torts require proof that defendant acted with intent (purpose or substantial certainty) to cause a specific type of harm. Unlike negligence, the focus is on the actor's state of mind. Transferred intent applies across certain intentional torts.",
    analysis_framework=["Identify the specific intentional tort alleged", "Determine if intent (purpose or substantial certainty) is provable", "Assess transferred intent applicability", "Evaluate available privileges and defenses", "Calculate damages including potential punitive component"],
    key_factors=["intent_evidence", "transferred_intent", "consent_defense", "self_defense", "damages_severity"],
    authority=AuthorityLevel.RESTATEMENT,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.CRITICAL,
    precedents=[
        ControllingPrecedent("Garratt v. Dailey", "46 Wash.2d 197", 1955, "Wash. Supreme Court", "Intent established by substantial certainty that harmful contact will result"),
    ],
    jurisdiction_notes="Intentional torts may have shorter statutes of limitations. Punitive damages generally available.",
    risk_multipliers={"clear_intent": 0.6, "punitive_damages_likely": 1.8, "insurance_exclusion": 1.5},
    damages_guidance="Compensatory plus punitive damages. Insurance may not cover intentional acts.",
    settlement_factors=["punitive_damages_risk", "criminal_liability_overlap", "insurance_coverage_exclusion"],
    statute_of_limitations_years=1.0,
)

DOCTRINE_CACHE["fraud_and_misrepresentation"] = DoctrineBlock(
    key="fraud_and_misrepresentation",
    topic="Fraud and Misrepresentation",
    category=LitigationCategory.TORT_LIABILITY,
    keywords=["fraud", "misrepresentation", "deceit", "scienter", "reliance", "material fact"],
    conclusion_template="Common law fraud requires: (1) material misrepresentation of fact, (2) knowledge of falsity or reckless disregard (scienter), (3) intent to induce reliance, (4) justifiable reliance, (5) resulting damages. Must be pled with particularity under Rule 9(b).",
    analysis_framework=["Identify the specific false statement of material fact", "Assess scienter evidence", "Evaluate justifiable reliance", "Calculate fraud damages (benefit of the bargain or out-of-pocket)", "Ensure Rule 9(b) particularity requirements are met"],
    key_factors=["specific_misrepresentation", "scienter_evidence", "materiality", "justifiable_reliance", "damages_calculation"],
    authority=AuthorityLevel.CASE_LAW,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.HIGH,
    precedents=[
        ControllingPrecedent("Derry v. Peek", "(1889) 14 App Cas 337", 1889, "House of Lords", "Established scienter requirement: knowledge of falsity or reckless disregard"),
    ],
    jurisdiction_notes="Fraud must be pled with particularity (who, what, when, where, how). Statute of frauds may apply.",
    risk_multipliers={"documentary_evidence": 0.7, "oral_only_representations": 1.6, "sophisticated_parties": 1.3},
    damages_guidance="Benefit of the bargain or out-of-pocket measure. Punitive damages available in egregious cases.",
    statute_of_limitations_years=3.0,
)

# --- CONTRACT DISPUTES ---

DOCTRINE_CACHE["breach_of_contract"] = DoctrineBlock(
    key="breach_of_contract",
    topic="Breach of Contract Analysis",
    category=LitigationCategory.CONTRACT_DISPUTE,
    keywords=["breach", "contract", "performance", "material breach", "substantial performance", "anticipatory"],
    conclusion_template="Breach of contract requires: (1) valid enforceable contract, (2) plaintiff's performance or excuse, (3) defendant's breach, (4) resulting damages. Material breach excuses further performance; minor breach allows damages but not termination.",
    analysis_framework=["Confirm contract formation and enforceability", "Determine if plaintiff performed or was excused", "Classify breach as material or minor", "Assess available remedies", "Consider mitigation of damages obligation"],
    key_factors=["contract_validity", "plaintiff_performance", "breach_materiality", "damages_foreseeability", "mitigation_efforts"],
    authority=AuthorityLevel.RESTATEMENT,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.HIGH,
    precedents=[
        ControllingPrecedent("Jacob & Youngs v. Kent", "230 N.Y. 239", 1921, "NY Court of Appeals", "Substantial performance doctrine: minor deviations do not excuse payment"),
        ControllingPrecedent("Hadley v. Baxendale", "9 Exch. 341", 1854, "Court of Exchequer", "Consequential damages limited to those reasonably foreseeable at contract formation"),
    ],
    jurisdiction_notes="UCC governs goods; common law governs services. Statute of limitations typically 4-6 years.",
    risk_multipliers={"clear_written_terms": 0.7, "oral_contract": 1.6, "complex_performance": 1.3},
    damages_guidance="Expectation damages (benefit of the bargain). Consequential damages if foreseeable. Specific performance for unique goods/real property.",
    settlement_factors=["contract_clarity", "breach_severity", "damages_provability", "ongoing_relationship"],
    statute_of_limitations_years=4.0,
)

DOCTRINE_CACHE["anticipatory_repudiation"] = DoctrineBlock(
    key="anticipatory_repudiation",
    topic="Anticipatory Repudiation",
    category=LitigationCategory.CONTRACT_DISPUTE,
    keywords=["anticipatory repudiation", "anticipatory breach", "demand assurances", "ucc 2-609", "retraction"],
    conclusion_template="Anticipatory repudiation occurs when a party unequivocally indicates intent not to perform before performance is due. The aggrieved party may: (1) treat as immediate breach and sue, (2) wait and urge performance, (3) demand adequate assurances under UCC 2-609.",
    analysis_framework=["Determine if the statement/conduct is unequivocal repudiation", "Assess whether performance date has passed", "Evaluate right to demand adequate assurances", "Determine if retraction is still possible", "Calculate available damages at time of repudiation"],
    key_factors=["unequivocal_repudiation", "timing_before_due", "demand_assurances", "retraction_possibility", "cover_damages"],
    authority=AuthorityLevel.STATUTE,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.MEDIUM,
    precedents=[
        ControllingPrecedent("Hochster v. De La Tour", "2 E. & B. 678", 1853, "Queen's Bench", "Established doctrine of anticipatory breach allowing immediate suit"),
    ],
    jurisdiction_notes="UCC 2-609 demand for assurances applies to goods contracts. Common law applies to services.",
    risk_multipliers={"clear_repudiation": 0.7, "ambiguous_statements": 1.5},
    damages_guidance="Market damages at time aggrieved party learned of repudiation, or cover damages.",
    statute_of_limitations_years=4.0,
)

DOCTRINE_CACHE["contract_damages_calculation"] = DoctrineBlock(
    key="contract_damages_calculation",
    topic="Contract Damages Measurement",
    category=LitigationCategory.CONTRACT_DISPUTE,
    keywords=["contract damages", "expectation", "reliance", "restitution", "consequential", "liquidated damages"],
    conclusion_template="Contract damages aim to put the non-breaching party in the position had the contract been performed. Three measures: (1) expectation (benefit of bargain), (2) reliance (expenditures in reliance), (3) restitution (unjust enrichment). Consequential damages require foreseeability at formation.",
    analysis_framework=["Calculate expectation damages", "Assess reliance expenditures as alternative", "Consider restitution interest", "Apply Hadley foreseeability limitation", "Evaluate certainty of damages", "Check for liquidated damages clause"],
    key_factors=["expectation_calculation", "foreseeability_at_formation", "certainty_of_damages", "mitigation_duty", "liquidated_damages_clause"],
    authority=AuthorityLevel.RESTATEMENT,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.HIGH,
    precedents=[
        ControllingPrecedent("Hadley v. Baxendale", "9 Exch. 341", 1854, "Court of Exchequer", "Consequential damages limited to foreseeable losses at contract formation"),
        ControllingPrecedent("Kenford Co. v. Erie County", "73 N.Y.2d 312", 1989, "NY Court of Appeals", "Lost profits must be proven with reasonable certainty"),
    ],
    jurisdiction_notes="Liquidated damages enforced if reasonable estimate; penalty clauses void. UCC allows liberal proof of lost profits.",
    risk_multipliers={"clear_damages": 0.7, "speculative_lost_profits": 1.8, "penalty_clause_risk": 1.4},
    damages_guidance="Expectation damages primary. Lost profits require reasonable certainty. Duty to mitigate applies.",
    statute_of_limitations_years=4.0,
)

# --- EMPLOYMENT ---

DOCTRINE_CACHE["wrongful_termination"] = DoctrineBlock(
    key="wrongful_termination",
    topic="Wrongful Termination Claims",
    category=LitigationCategory.EMPLOYMENT,
    keywords=["wrongful termination", "at will", "public policy", "implied contract", "retaliatory discharge"],
    conclusion_template="At-will employment can be terminated for any lawful reason. Exceptions: (1) public policy violation (firing for exercising legal right or refusing illegal act), (2) implied contract from handbooks or oral promises, (3) covenant of good faith in some jurisdictions, (4) statutory protections (whistleblower, anti-retaliation).",
    analysis_framework=["Determine employment status (at-will vs. contract)", "Identify potential public policy exceptions", "Evaluate handbook/policy language for implied contract", "Assess whistleblower or retaliation protections", "Calculate potential damages (back pay, front pay, emotional distress)"],
    key_factors=["employment_status", "termination_reason", "public_policy_violation", "handbook_promises", "documentation_trail"],
    authority=AuthorityLevel.CASE_LAW,
    confidence=ConfidenceLevel.JURISDICTION_DEPENDENT,
    risk_severity=RiskSeverity.HIGH,
    precedents=[
        ControllingPrecedent("Tameny v. Atlantic Richfield", "27 Cal.3d 167", 1980, "Cal. Supreme Court", "Firing employee for refusing to participate in price-fixing violates public policy"),
        ControllingPrecedent("Woolley v. Hoffmann-La Roche", "99 N.J. 284", 1985, "NJ Supreme Court", "Employee handbook can create implied contract of employment"),
    ],
    jurisdiction_notes="Exceptions to at-will employment vary dramatically by state. Montana is the only non-at-will state.",
    risk_multipliers={"clear_policy_violation": 0.6, "at_will_disclaimer": 1.5, "documented_cause": 0.8},
    damages_guidance="Back pay, front pay, emotional distress, punitive damages (in some jurisdictions). Mitigation required.",
    settlement_factors=["documentation_quality", "pretext_evidence", "jury_sympathy", "employer_size"],
    statute_of_limitations_years=2.0,
)

DOCTRINE_CACHE["employment_discrimination"] = DoctrineBlock(
    key="employment_discrimination",
    topic="Employment Discrimination (Title VII)",
    category=LitigationCategory.EMPLOYMENT,
    keywords=["discrimination", "title vii", "disparate treatment", "disparate impact", "hostile work environment", "eeoc"],
    conclusion_template="Title VII prohibits discrimination based on race, color, religion, sex, or national origin. Claims proceed through McDonnell Douglas burden-shifting: (1) plaintiff establishes prima facie case, (2) employer articulates legitimate nondiscriminatory reason, (3) plaintiff shows pretext. EEOC charge required before suit.",
    analysis_framework=["Confirm protected class membership", "Establish prima facie case elements", "Analyze employer's proffered reason", "Evaluate pretext evidence", "Assess damages caps by employer size", "Verify EEOC charge filing and right-to-sue"],
    key_factors=["protected_class", "adverse_action", "similarly_situated_comparators", "temporal_proximity", "pretext_evidence"],
    authority=AuthorityLevel.STATUTE,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.HIGH,
    precedents=[
        ControllingPrecedent("McDonnell Douglas v. Green", "411 U.S. 792", 1973, "SCOTUS", "Established burden-shifting framework for disparate treatment claims"),
        ControllingPrecedent("Griggs v. Duke Power Co.", "401 U.S. 424", 1971, "SCOTUS", "Established disparate impact theory of discrimination"),
        ControllingPrecedent("Meritor Savings Bank v. Vinson", "477 U.S. 57", 1986, "SCOTUS", "Sexual harassment is actionable sex discrimination under Title VII"),
    ],
    jurisdiction_notes="EEOC charge must be filed within 180/300 days. Damages caps: 15-100 employees = $50K; 500+ = $300K.",
    risk_multipliers={"strong_comparator_evidence": 0.6, "statistical_evidence": 0.7, "no_eeoc_charge": 2.5},
    damages_guidance="Back pay (no cap), compensatory + punitive (capped by employer size), attorneys' fees.",
    statute_of_limitations_years=0.82,
)

DOCTRINE_CACHE["flsa_wage_hour"] = DoctrineBlock(
    key="flsa_wage_hour",
    topic="FLSA Wage and Hour Claims",
    category=LitigationCategory.EMPLOYMENT,
    keywords=["flsa", "overtime", "minimum wage", "exempt", "misclassification", "wage hour", "collective action"],
    conclusion_template="FLSA requires minimum wage and overtime (1.5x for hours over 40/week) for non-exempt employees. Key disputes involve: (1) exempt vs. non-exempt classification, (2) off-the-clock work, (3) independent contractor misclassification. Collective actions under 29 USC 216(b) allow opt-in class treatment.",
    analysis_framework=["Determine exempt/non-exempt status under duties test", "Calculate unpaid overtime exposure", "Assess off-the-clock work claims", "Evaluate independent contractor classification", "Model collective action damages exposure", "Determine willfulness for 3-year SOL"],
    key_factors=["exemption_classification", "overtime_hours", "off_clock_work", "independent_contractor_status", "willfulness", "collective_action_size"],
    authority=AuthorityLevel.STATUTE,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.HIGH,
    precedents=[
        ControllingPrecedent("Encino Motorcars v. Navarro", "584 U.S. 79", 2018, "SCOTUS", "FLSA exemptions should not be construed narrowly; give them fair reading"),
    ],
    jurisdiction_notes="FLSA is federal. State wage laws may provide greater protections. California AB5 tightens IC classification.",
    risk_multipliers={"collective_action": 2.0, "willful_violation": 1.5, "clear_exemption": 0.5},
    damages_guidance="Unpaid wages + equal liquidated damages (doubled). Attorneys' fees mandatory for prevailing plaintiffs.",
    settlement_factors=["number_of_affected_employees", "duration_of_violations", "documentation_quality", "willfulness"],
    statute_of_limitations_years=2.0,
)

# --- SECURITIES ---

DOCTRINE_CACHE["securities_fraud_10b5"] = DoctrineBlock(
    key="securities_fraud_10b5",
    topic="Securities Fraud (Rule 10b-5)",
    category=LitigationCategory.SECURITIES,
    keywords=["10b-5", "securities fraud", "material misstatement", "scienter", "reliance", "loss causation", "pslra"],
    conclusion_template="Section 10(b) and Rule 10b-5 prohibit material misstatements or omissions in connection with purchase or sale of securities. Elements: (1) material misstatement/omission, (2) scienter, (3) connection with purchase/sale, (4) reliance, (5) economic loss, (6) loss causation. PSLRA heightens pleading standards.",
    analysis_framework=["Identify the allegedly false or misleading statement", "Assess materiality (substantial likelihood of reasonable investor significance)", "Evaluate scienter evidence (intent to deceive or severe recklessness)", "Determine reliance framework (FOTM presumption or direct)", "Establish loss causation linking fraud to economic loss", "Apply PSLRA heightened pleading requirements"],
    key_factors=["material_misstatement", "scienter_evidence", "reliance_framework", "loss_causation", "pslra_compliance", "safe_harbor_defense"],
    authority=AuthorityLevel.STATUTE,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.CRITICAL,
    precedents=[
        ControllingPrecedent("Basic v. Levinson", "485 U.S. 224", 1988, "SCOTUS", "Fraud-on-the-market presumption of reliance for publicly traded securities"),
        ControllingPrecedent("Tellabs v. Makor Issues & Rights", "551 U.S. 308", 2007, "SCOTUS", "PSLRA requires strong inference of scienter at least as compelling as any opposing inference"),
        ControllingPrecedent("Dura Pharmaceuticals v. Broudo", "544 U.S. 336", 2005, "SCOTUS", "Loss causation requires proof that the fraud actually caused the economic loss"),
    ],
    jurisdiction_notes="Exclusive federal jurisdiction. PSLRA stay of discovery during MTD. SLUSA prevents state class actions for covered securities.",
    risk_multipliers={"restatement_of_financials": 0.5, "forward_looking_statement": 1.5, "insider_trading_parallel": 0.6},
    damages_guidance="Out-of-pocket measure. 90-day lookback period for damages calculation. Joint and several liability with proportionate liability option.",
    settlement_factors=["stock_drop_magnitude", "class_size", "d_and_o_insurance", "parallel_sec_investigation"],
    statute_of_limitations_years=2.0,
)

DOCTRINE_CACHE["securities_class_certification"] = DoctrineBlock(
    key="securities_class_certification",
    topic="Securities Class Action Certification",
    category=LitigationCategory.SECURITIES,
    keywords=["class certification", "rule 23", "typicality", "commonality", "adequacy", "predominance"],
    conclusion_template="Securities class certification under Rule 23 requires: (a) numerosity, commonality, typicality, adequacy, and (b)(3) predominance and superiority. Fraud-on-the-market (FOTM) presumption provides class-wide reliance for efficient market securities. Defendants may rebut at certification.",
    analysis_framework=["Assess numerosity (generally 40+ class members)", "Confirm common questions of law or fact", "Evaluate typicality of named plaintiff claims", "Assess adequacy of representation", "Determine predominance of common issues", "Apply FOTM presumption or individual reliance"],
    key_factors=["class_size", "common_questions", "named_plaintiff_typicality", "market_efficiency", "individual_issues"],
    authority=AuthorityLevel.CASE_LAW,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.HIGH,
    precedents=[
        ControllingPrecedent("Halliburton v. Erica P. John Fund", "573 U.S. 258", 2014, "SCOTUS", "FOTM presumption rebuttable at class certification; defendants can show no price impact"),
    ],
    jurisdiction_notes="Class certification is a critical inflection point. Denial often leads to settlement or dismissal.",
    risk_multipliers={"efficient_market": 0.7, "individual_reliance_issues": 1.8, "competing_classes": 1.3},
    damages_guidance="Aggregate class damages can be massive. Event study methodology for price impact.",
    statute_of_limitations_years=2.0,
)

# --- ANTITRUST ---

DOCTRINE_CACHE["sherman_act_section1"] = DoctrineBlock(
    key="sherman_act_section1",
    topic="Sherman Act Section 1 - Agreements in Restraint of Trade",
    category=LitigationCategory.ANTITRUST,
    keywords=["sherman act", "section 1", "price fixing", "market allocation", "restraint of trade", "per se", "rule of reason"],
    conclusion_template="Section 1 of the Sherman Act prohibits agreements in unreasonable restraint of trade. Per se violations (price fixing, market allocation, bid rigging) require only proof of agreement. Rule of reason analysis requires proof of anticompetitive effects outweighing procompetitive benefits.",
    analysis_framework=["Identify the alleged agreement or conspiracy", "Classify as per se illegal or rule of reason", "For per se: prove agreement and participation", "For rule of reason: define relevant market, prove anticompetitive effects", "Assess available defenses and efficiencies"],
    key_factors=["agreement_evidence", "per_se_vs_rule_of_reason", "market_definition", "anticompetitive_effects", "procompetitive_justifications"],
    authority=AuthorityLevel.STATUTE,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.CRITICAL,
    precedents=[
        ControllingPrecedent("Leegin Creative Leather v. PSKS", "551 U.S. 877", 2007, "SCOTUS", "Resale price maintenance subject to rule of reason, not per se"),
        ControllingPrecedent("Ohio v. American Express", "585 U.S. 529", 2018, "SCOTUS", "Two-sided platforms require proof of net anticompetitive effects across both sides"),
    ],
    jurisdiction_notes="Treble damages plus attorneys fees. Criminal penalties for per se violations (up to $100M corporate/$1M individual + 10 years).",
    risk_multipliers={"per_se_violation": 0.3, "documentary_evidence_of_agreement": 0.5, "rule_of_reason": 1.5},
    damages_guidance="Treble damages (3x actual damages). Attorneys' fees mandatory for prevailing plaintiffs.",
    statute_of_limitations_years=4.0,
)

DOCTRINE_CACHE["sherman_act_section2"] = DoctrineBlock(
    key="sherman_act_section2",
    topic="Sherman Act Section 2 - Monopolization",
    category=LitigationCategory.ANTITRUST,
    keywords=["monopolization", "section 2", "market power", "exclusionary conduct", "attempted monopolization", "predatory pricing"],
    conclusion_template="Section 2 prohibits monopolization and attempted monopolization. Elements: (1) possession of monopoly power in relevant market, (2) willful acquisition or maintenance of that power through exclusionary conduct (as opposed to growth from superior product, business acumen, or historic accident).",
    analysis_framework=["Define relevant product and geographic market", "Assess market share and entry barriers", "Identify exclusionary conduct", "Distinguish from legitimate competitive behavior", "Calculate damages from monopolistic overcharge"],
    key_factors=["market_definition", "market_share", "entry_barriers", "exclusionary_conduct", "legitimate_business_justification"],
    authority=AuthorityLevel.STATUTE,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.CRITICAL,
    precedents=[
        ControllingPrecedent("Verizon v. Trinko", "540 U.S. 398", 2004, "SCOTUS", "No general duty to assist competitors; refusal to deal rarely violates Section 2"),
        ControllingPrecedent("United States v. Microsoft", "253 F.3d 34", 2001, "D.C. Circuit", "Maintenance of monopoly through anticompetitive conduct violates Section 2"),
    ],
    jurisdiction_notes="Monopoly power typically inferred from market share above 70%. Single-firm conduct is harder to prove than conspiracy.",
    risk_multipliers={"high_market_share": 0.6, "network_effects": 0.7, "legitimate_competition": 1.5},
    damages_guidance="Treble damages. Structural or behavioral remedies in government cases.",
    statute_of_limitations_years=4.0,
)

# --- IP LITIGATION ---

DOCTRINE_CACHE["patent_infringement"] = DoctrineBlock(
    key="patent_infringement",
    topic="Patent Infringement Analysis",
    category=LitigationCategory.IP_LITIGATION,
    keywords=["patent infringement", "claim construction", "literal infringement", "doctrine of equivalents", "markman", "inter partes"],
    conclusion_template="Patent infringement requires that the accused product or method practices each element of at least one patent claim, either literally or under the doctrine of equivalents. Claim construction (Markman hearing) is often dispositive. Key defenses: invalidity, non-infringement, exhaustion, laches.",
    analysis_framework=["Identify asserted patent claims", "Construe disputed claim terms (Markman)", "Compare accused product to each claim element", "Apply doctrine of equivalents if literal infringement fails", "Assess invalidity defenses (prior art, obviousness, 101 eligibility)", "Calculate reasonable royalty or lost profits damages"],
    key_factors=["claim_construction", "literal_infringement", "equivalents_analysis", "prior_art", "patent_eligibility"],
    authority=AuthorityLevel.STATUTE,
    confidence=ConfidenceLevel.JURISDICTION_DEPENDENT,
    risk_severity=RiskSeverity.HIGH,
    precedents=[
        ControllingPrecedent("Markman v. Westview Instruments", "517 U.S. 370", 1996, "SCOTUS", "Claim construction is a question of law for the court"),
        ControllingPrecedent("Alice Corp. v. CLS Bank", "573 U.S. 208", 2014, "SCOTUS", "Abstract ideas implemented on generic computers not patent-eligible under 35 USC 101"),
    ],
    jurisdiction_notes="Federal Circuit has exclusive jurisdiction over patent appeals. ITC Section 337 for imports. PTAB inter partes review.",
    risk_multipliers={"clear_literal_infringement": 0.5, "design_around_possible": 1.5, "patent_troll_plaintiff": 1.3},
    damages_guidance="Reasonable royalty (minimum). Lost profits if patentee practices patent. Enhanced damages for willful infringement (up to 3x).",
    settlement_factors=["claim_construction_outlook", "prior_art_strength", "injunction_threat", "design_around_cost"],
    statute_of_limitations_years=6.0,
)

DOCTRINE_CACHE["trade_secret_misappropriation"] = DoctrineBlock(
    key="trade_secret_misappropriation",
    topic="Trade Secret Misappropriation",
    category=LitigationCategory.IP_LITIGATION,
    keywords=["trade secret", "misappropriation", "dtsa", "defend trade secrets act", "inevitable disclosure", "non-compete"],
    conclusion_template="Trade secret misappropriation under DTSA/UTSA requires: (1) information qualifying as a trade secret, (2) reasonable measures to maintain secrecy, (3) acquisition by improper means or breach of duty. DTSA provides federal jurisdiction and ex parte seizure remedy.",
    analysis_framework=["Confirm information qualifies as trade secret", "Assess reasonable secrecy measures taken", "Identify improper means of acquisition", "Evaluate inevitable disclosure doctrine applicability", "Calculate damages (actual loss, unjust enrichment, or reasonable royalty)", "Assess injunctive relief availability"],
    key_factors=["trade_secret_identification", "secrecy_measures", "improper_means", "former_employee_involvement", "independent_development_defense"],
    authority=AuthorityLevel.STATUTE,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.HIGH,
    precedents=[
        ControllingPrecedent("PepsiCo v. Redmond", "54 F.3d 1262", 1995, "7th Circuit", "Inevitable disclosure doctrine can support injunction even without actual misappropriation"),
    ],
    jurisdiction_notes="DTSA (2016) provides federal cause of action. Most states have adopted UTSA with variations. Immunity for whistleblower disclosures.",
    risk_multipliers={"weak_secrecy_measures": 1.8, "former_employee_competitor": 0.7, "independent_development": 1.5},
    damages_guidance="Actual loss + unjust enrichment (no double counting), or reasonable royalty. Exemplary damages up to 2x for willful misappropriation.",
    statute_of_limitations_years=3.0,
)

DOCTRINE_CACHE["trademark_infringement"] = DoctrineBlock(
    key="trademark_infringement",
    topic="Trademark Infringement and Likelihood of Confusion",
    category=LitigationCategory.IP_LITIGATION,
    keywords=["trademark", "likelihood of confusion", "lanham act", "dilution", "trade dress", "unfair competition"],
    conclusion_template="Trademark infringement under the Lanham Act requires proof of likelihood of confusion between plaintiff's mark and defendant's use. Multi-factor test (varies by circuit): strength of mark, similarity, proximity of goods, evidence of actual confusion, defendant's intent, quality of goods, consumer sophistication.",
    analysis_framework=["Assess mark strength (arbitrary > suggestive > descriptive)", "Compare similarity of marks (sight, sound, meaning)", "Evaluate proximity of goods/services", "Search for evidence of actual confusion", "Assess defendant's intent in adopting mark", "Consider consumer sophistication"],
    key_factors=["mark_strength", "mark_similarity", "goods_proximity", "actual_confusion", "defendant_intent", "consumer_sophistication"],
    authority=AuthorityLevel.STATUTE,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.HIGH,
    precedents=[
        ControllingPrecedent("Polaroid Corp. v. Polarad Electronics", "287 F.2d 492", 1961, "2nd Circuit", "Established multi-factor test for likelihood of confusion"),
    ],
    jurisdiction_notes="Federal registration provides nationwide constructive notice. State common law rights exist in geographic area of actual use.",
    risk_multipliers={"famous_mark": 0.5, "parody_defense": 1.3, "actual_confusion_evidence": 0.6},
    damages_guidance="Defendant's profits, plaintiff's damages, and costs. Enhanced damages for willful infringement. Attorneys' fees in exceptional cases.",
    statute_of_limitations_years=3.0,
)

# --- ENVIRONMENTAL ---

DOCTRINE_CACHE["cercla_superfund"] = DoctrineBlock(
    key="cercla_superfund",
    topic="CERCLA Superfund Liability",
    category=LitigationCategory.ENVIRONMENTAL,
    keywords=["cercla", "superfund", "hazardous substance", "prp", "joint and several", "cost recovery", "contribution"],
    conclusion_template="CERCLA imposes strict, joint and several, retroactive liability on PRPs (current owners/operators, past owners/operators, generators, transporters) for costs of hazardous substance cleanup. Liability is without regard to fault. Innocent landowner and bona fide prospective purchaser defenses available.",
    analysis_framework=["Identify potentially responsible parties (PRPs)", "Determine PRP category (owner, operator, generator, transporter)", "Assess liability defenses (innocent landowner, BFPP, third party)", "Calculate response cost allocation", "Evaluate contribution claims against other PRPs"],
    key_factors=["prp_status", "hazardous_substance_release", "response_costs", "contribution_allocation", "innocent_landowner_defense"],
    authority=AuthorityLevel.STATUTE,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.CRITICAL,
    precedents=[
        ControllingPrecedent("Burlington Northern v. United States", "556 U.S. 599", 2009, "SCOTUS", "Divisible harm allows apportioned (not joint and several) liability if reasonable basis exists"),
    ],
    jurisdiction_notes="Federal statute with federal jurisdiction. EPA enforcement actions. State superfund laws may also apply.",
    risk_multipliers={"current_owner": 0.5, "generator_liability": 0.7, "divisible_harm": 1.3},
    damages_guidance="Response costs (past and future cleanup). No punitive damages. Treble damages for failure to comply with EPA order.",
    statute_of_limitations_years=6.0,
)

DOCTRINE_CACHE["clean_water_act_enforcement"] = DoctrineBlock(
    key="clean_water_act_enforcement",
    topic="Clean Water Act Enforcement",
    category=LitigationCategory.ENVIRONMENTAL,
    keywords=["clean water act", "npdes", "discharge", "wetlands", "citizen suit", "navigable waters"],
    conclusion_template="The Clean Water Act prohibits discharge of pollutants from a point source into navigable waters without an NPDES permit. Civil penalties up to $64,618/day/violation. Citizen suit provisions allow private enforcement. Key defense: compliance with permit terms.",
    analysis_framework=["Identify the discharge point source", "Determine if receiving water is 'navigable water'", "Check NPDES permit status and compliance", "Calculate penalty exposure (days x violations)", "Assess citizen suit standing requirements"],
    key_factors=["point_source", "navigable_waters", "permit_compliance", "discharge_volume", "environmental_harm"],
    authority=AuthorityLevel.STATUTE,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.HIGH,
    precedents=[
        ControllingPrecedent("County of Maui v. Hawaii Wildlife Fund", "590 U.S. 165", 2020, "SCOTUS", "CWA covers discharge that is functional equivalent of direct discharge to navigable waters"),
    ],
    jurisdiction_notes="Federal statute. EPA and Army Corps jurisdiction. State delegated programs in most states.",
    risk_multipliers={"ongoing_violation": 0.5, "permit_violation": 0.7, "wetland_fill": 0.8},
    damages_guidance="Civil penalties per day per violation. Injunctive relief. Supplemental environmental projects may reduce penalties.",
    statute_of_limitations_years=5.0,
)

DOCTRINE_CACHE["toxic_tort_causation"] = DoctrineBlock(
    key="toxic_tort_causation",
    topic="Toxic Tort Causation",
    category=LitigationCategory.ENVIRONMENTAL,
    keywords=["toxic tort", "exposure", "causation", "epidemiology", "daubert", "general causation", "specific causation"],
    conclusion_template="Toxic tort plaintiffs must prove both general causation (substance can cause the injury) and specific causation (substance caused this plaintiff's injury). Expert testimony must meet Daubert reliability standards. Epidemiological evidence often required for general causation.",
    analysis_framework=["Establish general causation (substance can cause injury type)", "Prove specific causation (this exposure caused this plaintiff's injury)", "Evaluate expert witness reliability under Daubert", "Assess exposure levels and duration", "Consider alternative causes"],
    key_factors=["general_causation", "specific_causation", "expert_reliability", "exposure_levels", "latency_period", "alternative_causes"],
    authority=AuthorityLevel.CASE_LAW,
    confidence=ConfidenceLevel.EVOLVING_LAW,
    risk_severity=RiskSeverity.HIGH,
    precedents=[
        ControllingPrecedent("Daubert v. Merrell Dow", "509 U.S. 579", 1993, "SCOTUS", "Trial court gatekeeping function for scientific expert testimony reliability"),
    ],
    jurisdiction_notes="Daubert applies in federal courts. Some states follow Frye general acceptance standard. Mass tort MDLs common.",
    risk_multipliers={"strong_epidemiology": 0.6, "no_dose_response": 1.8, "long_latency": 1.4},
    damages_guidance="Medical expenses, lost wages, pain and suffering. Punitive damages if defendant knew of danger. Medical monitoring in some jurisdictions.",
    statute_of_limitations_years=2.0,
)

# --- PRODUCTS LIABILITY ---

DOCTRINE_CACHE["design_defect"] = DoctrineBlock(
    key="design_defect",
    topic="Products Liability - Design Defect",
    category=LitigationCategory.PRODUCTS_LIABILITY,
    keywords=["design defect", "risk utility", "consumer expectations", "reasonable alternative design", "crashworthiness"],
    conclusion_template="Design defect claims allege the product design itself is unreasonably dangerous. Two tests: (1) consumer expectations (product more dangerous than ordinary consumer would expect), (2) risk-utility (risks outweigh benefits, reasonable alternative design exists). Restatement (Third) requires proof of reasonable alternative design.",
    analysis_framework=["Identify the alleged design defect", "Apply consumer expectations test", "Apply risk-utility balancing test", "Evaluate feasibility of reasonable alternative design", "Assess state of the art at time of manufacture", "Calculate damages exposure"],
    key_factors=["design_flaw", "consumer_expectations", "risk_utility_balance", "alternative_design", "state_of_art"],
    authority=AuthorityLevel.RESTATEMENT,
    confidence=ConfidenceLevel.JURISDICTION_DEPENDENT,
    risk_severity=RiskSeverity.CRITICAL,
    precedents=[
        ControllingPrecedent("Barker v. Lull Engineering", "20 Cal.3d 413", 1978, "Cal. Supreme Court", "Dual test for design defect: consumer expectations and risk-utility with burden shift"),
    ],
    jurisdiction_notes="Significant split on whether consumer expectations test or risk-utility test applies. Some states require RAD; others do not.",
    risk_multipliers={"mass_market_product": 0.7, "clear_alternative_design": 0.6, "state_of_art_defense": 1.3},
    damages_guidance="Compensatory damages for injury. Punitive damages if manufacturer knew of defect. Recall costs.",
    statute_of_limitations_years=2.0,
)

DOCTRINE_CACHE["manufacturing_defect"] = DoctrineBlock(
    key="manufacturing_defect",
    topic="Products Liability - Manufacturing Defect",
    category=LitigationCategory.PRODUCTS_LIABILITY,
    keywords=["manufacturing defect", "quality control", "deviation from design", "production error", "strict liability"],
    conclusion_template="Manufacturing defect exists when a specific product unit deviates from its intended design, making it more dangerous than other units of the same product. Strict liability applies regardless of manufacturer's care level. Plaintiff must show product deviated from design specifications.",
    analysis_framework=["Identify the deviation from intended design", "Compare defective unit to design specifications", "Establish defect existed when product left manufacturer", "Prove defect caused plaintiff's injury", "Assess quality control evidence"],
    key_factors=["deviation_from_design", "defect_at_departure", "causation", "quality_control_records", "batch_testing"],
    authority=AuthorityLevel.RESTATEMENT,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.CRITICAL,
    precedents=[
        ControllingPrecedent("Escola v. Coca-Cola Bottling", "24 Cal.2d 453", 1944, "Cal. Supreme Court", "Res ipsa loquitur and strict liability for manufacturing defects (Traynor concurrence)"),
    ],
    jurisdiction_notes="Strict liability universally applied to manufacturing defects. Res ipsa loquitur may create inference of defect.",
    risk_multipliers={"clear_deviation": 0.5, "destroyed_product": 1.5, "batch_recall": 0.7},
    damages_guidance="Full compensatory damages. Punitive damages if systematic QC failure. Product recall costs.",
    statute_of_limitations_years=2.0,
)

DOCTRINE_CACHE["failure_to_warn"] = DoctrineBlock(
    key="failure_to_warn",
    topic="Products Liability - Failure to Warn",
    category=LitigationCategory.PRODUCTS_LIABILITY,
    keywords=["failure to warn", "inadequate warning", "duty to warn", "learned intermediary", "post-sale warning"],
    conclusion_template="Failure to warn claims allege the product lacked adequate warnings or instructions about risks. Manufacturer must warn of reasonably foreseeable risks. Learned intermediary doctrine (prescription drugs) channels warning duty through physician. Post-sale duty to warn exists for subsequently discovered dangers.",
    analysis_framework=["Identify the undisclosed risk", "Assess adequacy of existing warnings", "Evaluate manufacturer's knowledge of risk", "Apply heeding presumption if available", "Consider learned intermediary doctrine for Rx drugs", "Assess post-sale warning duty"],
    key_factors=["risk_knowledge", "warning_adequacy", "heeding_presumption", "learned_intermediary", "post_sale_duty"],
    authority=AuthorityLevel.RESTATEMENT,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.HIGH,
    precedents=[
        ControllingPrecedent("Reyes v. Wyeth Laboratories", "498 F.2d 1264", 1974, "5th Circuit", "Mass immunization exception to learned intermediary doctrine"),
    ],
    jurisdiction_notes="Heeding presumption (plaintiff would have heeded adequate warning) exists in many but not all jurisdictions.",
    risk_multipliers={"known_risk_no_warning": 0.5, "learned_intermediary_applies": 1.4, "obvious_danger_defense": 1.3},
    damages_guidance="Compensatory damages. Punitive if manufacturer knew of danger and concealed it.",
    statute_of_limitations_years=2.0,
)

# --- INSURANCE ---

DOCTRINE_CACHE["insurance_coverage_duty_to_defend"] = DoctrineBlock(
    key="insurance_coverage_duty_to_defend",
    topic="Insurance Duty to Defend",
    category=LitigationCategory.INSURANCE,
    keywords=["duty to defend", "insurance coverage", "eight corners", "reservation of rights", "cgl", "tender"],
    conclusion_template="Insurer's duty to defend is broader than duty to indemnify. Under the 'eight corners' rule, duty to defend exists if complaint allegations potentially fall within coverage. Insurer must defend the entire action even if only one claim is potentially covered. Wrongful refusal creates estoppel.",
    analysis_framework=["Compare complaint allegations to policy terms", "Apply eight corners / four corners rule", "Identify potentially covered and excluded claims", "Assess reservation of rights implications", "Evaluate estoppel risk from wrongful denial"],
    key_factors=["complaint_allegations", "policy_terms", "exclusion_applicability", "reservation_of_rights", "estoppel_risk"],
    authority=AuthorityLevel.CASE_LAW,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.HIGH,
    precedents=[
        ControllingPrecedent("Gray v. Zurich Insurance", "65 Cal.2d 263", 1966, "Cal. Supreme Court", "Insurer has duty to defend whenever there is potential for coverage under the policy"),
    ],
    jurisdiction_notes="Eight corners vs. extrinsic evidence rule varies by state. Some states allow extrinsic evidence to establish duty to defend.",
    risk_multipliers={"clear_coverage": 0.5, "intentional_act_exclusion": 1.5, "mixed_claims": 0.8},
    damages_guidance="Defense costs, indemnity, bad faith damages if wrongful denial. Consequential damages for breach of duty to defend.",
    statute_of_limitations_years=4.0,
)

DOCTRINE_CACHE["insurance_bad_faith"] = DoctrineBlock(
    key="insurance_bad_faith",
    topic="Insurance Bad Faith Claims",
    category=LitigationCategory.INSURANCE,
    keywords=["bad faith", "insurance", "unfair claims practices", "unreasonable denial", "first party", "third party"],
    conclusion_template="Insurance bad faith arises from unreasonable denial of claims, failure to investigate, or failure to settle within policy limits. First-party bad faith (insured vs. insurer) and third-party bad faith (failure to accept reasonable settlement exposing insured to excess judgment). Punitive damages available.",
    analysis_framework=["Classify as first-party or third-party bad faith", "Evaluate reasonableness of claim denial/delay", "Assess investigation adequacy", "Determine if insurer considered insured's interests", "Calculate extra-contractual damages exposure"],
    key_factors=["denial_reasonableness", "investigation_adequacy", "settlement_opportunity", "insured_interests", "pattern_of_conduct"],
    authority=AuthorityLevel.CASE_LAW,
    confidence=ConfidenceLevel.JURISDICTION_DEPENDENT,
    risk_severity=RiskSeverity.CRITICAL,
    precedents=[
        ControllingPrecedent("Gruenberg v. Aetna Insurance", "9 Cal.3d 566", 1973, "Cal. Supreme Court", "Insurer owes implied covenant of good faith and fair dealing to its insured"),
        ControllingPrecedent("Comunale v. Traders & General Insurance", "50 Cal.2d 654", 1958, "Cal. Supreme Court", "Insurer liable for excess judgment when it unreasonably fails to settle within limits"),
    ],
    jurisdiction_notes="Bad faith standards and remedies vary significantly by state. Some states have statutory bad faith causes of action.",
    risk_multipliers={"pattern_of_denials": 0.5, "reasonable_basis_for_denial": 1.5, "excess_exposure": 0.7},
    damages_guidance="Contract damages, emotional distress, punitive damages. Excess judgment in third-party context.",
    statute_of_limitations_years=2.0,
)

DOCTRINE_CACHE["insurance_subrogation"] = DoctrineBlock(
    key="insurance_subrogation",
    topic="Insurance Subrogation Rights",
    category=LitigationCategory.INSURANCE,
    keywords=["subrogation", "equitable subrogation", "contractual subrogation", "made whole", "anti-subrogation"],
    conclusion_template="Subrogation allows an insurer that has paid a loss to step into the shoes of the insured and pursue the responsible third party. Equitable subrogation arises by operation of law; contractual subrogation arises from policy terms. The 'made whole' doctrine requires insured to be fully compensated before insurer recovers.",
    analysis_framework=["Identify basis for subrogation (equitable or contractual)", "Determine if insured has been made whole", "Assess anti-subrogation rule applicability (insured cannot subrogate against its own insured)", "Calculate subrogation recovery potential", "Evaluate waiver of subrogation provisions"],
    key_factors=["subrogation_basis", "made_whole_doctrine", "anti_subrogation_rule", "recovery_potential", "waiver_provisions"],
    authority=AuthorityLevel.CASE_LAW,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.MEDIUM,
    precedents=[
        ControllingPrecedent("US Airways v. McCutchen", "569 U.S. 88", 2013, "SCOTUS", "ERISA plan terms control subrogation; equitable principles apply in gaps"),
    ],
    jurisdiction_notes="Made whole doctrine is default in most states but can be contractually modified. ERISA plans follow plan terms.",
    risk_multipliers={"clear_third_party_fault": 0.6, "insured_not_made_whole": 1.4},
    damages_guidance="Recovery limited to amounts paid by insurer. Common fund doctrine may require contribution to recovery costs.",
    statute_of_limitations_years=4.0,
)

# --- REGULATORY ---

DOCTRINE_CACHE["regulatory_enforcement_risk"] = DoctrineBlock(
    key="regulatory_enforcement_risk",
    topic="Regulatory Enforcement Action Risk",
    category=LitigationCategory.REGULATORY,
    keywords=["enforcement", "regulatory", "administrative action", "consent decree", "civil penalty", "compliance"],
    conclusion_template="Regulatory enforcement risk depends on: (1) violation severity and duration, (2) agency enforcement priorities, (3) cooperation level, (4) compliance history, (5) remediation efforts. Consent decrees often resolve government enforcement without trial but impose ongoing obligations.",
    analysis_framework=["Identify the regulatory framework and agency", "Assess violation severity and scope", "Evaluate agency enforcement trends and priorities", "Consider voluntary disclosure and cooperation benefits", "Model penalty exposure using agency guidelines", "Assess consent decree vs. contested litigation"],
    key_factors=["violation_severity", "agency_priorities", "cooperation_level", "compliance_history", "remediation_efforts"],
    authority=AuthorityLevel.REGULATION,
    confidence=ConfidenceLevel.JURISDICTION_DEPENDENT,
    risk_severity=RiskSeverity.HIGH,
    precedents=[
        ControllingPrecedent("SEC v. Citigroup Global Markets", "752 F.3d 285", 2014, "2nd Circuit", "Courts should not reject consent decrees merely because agency did not require admission of wrongdoing"),
    ],
    jurisdiction_notes="Agency enforcement discretion varies. DOJ involvement escalates risk. Parallel criminal investigation possible.",
    risk_multipliers={"voluntary_disclosure": 1.5, "no_cooperation": 0.5, "repeat_offender": 0.6},
    damages_guidance="Civil penalties, disgorgement, injunctive relief, consent decree obligations. Criminal fines if DOJ involved.",
    settlement_factors=["agency_flexibility", "cooperation_credit", "compliance_program", "public_interest"],
    statute_of_limitations_years=5.0,
)

DOCTRINE_CACHE["qui_tam_whistleblower"] = DoctrineBlock(
    key="qui_tam_whistleblower",
    topic="Qui Tam / False Claims Act Whistleblower",
    category=LitigationCategory.REGULATORY,
    keywords=["qui tam", "false claims act", "whistleblower", "relator", "government fraud", "fca"],
    conclusion_template="The False Claims Act allows private individuals (relators) to file suit on behalf of the government against parties that defraud government programs. Treble damages plus per-claim penalties ($13,508-$27,018). If government intervenes, relator receives 15-25%; if government declines, 25-30%. Anti-retaliation protections.",
    analysis_framework=["Identify the false claim or statement to the government", "Determine scienter (knowing, deliberate ignorance, reckless disregard)", "Assess materiality of the falsehood", "Evaluate public disclosure bar and original source exception", "Calculate damages exposure (treble + per-claim penalties)", "Consider government intervention likelihood"],
    key_factors=["false_claim", "scienter", "materiality", "government_payment", "public_disclosure_bar", "original_source"],
    authority=AuthorityLevel.STATUTE,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.CRITICAL,
    precedents=[
        ControllingPrecedent("Universal Health Services v. Escobar", "579 U.S. 176", 2016, "SCOTUS", "Implied false certification theory is viable but materiality requirement is demanding"),
    ],
    jurisdiction_notes="Filed under seal initially. DOJ has 60 days (often extended) to investigate and decide on intervention.",
    risk_multipliers={"government_intervenes": 0.4, "strong_relator_evidence": 0.6, "healthcare_industry": 0.7},
    damages_guidance="Treble damages + $13,508-$27,018 per false claim. Relator share 15-30%. Anti-retaliation remedies.",
    statute_of_limitations_years=6.0,
)

# --- CLASS ACTION ---

DOCTRINE_CACHE["class_action_certification"] = DoctrineBlock(
    key="class_action_certification",
    topic="Class Action Certification Requirements",
    category=LitigationCategory.CLASS_ACTION,
    keywords=["class action", "rule 23", "numerosity", "commonality", "typicality", "adequacy", "predominance"],
    conclusion_template="Rule 23 class certification requires: (a) numerosity, commonality, typicality, adequacy of representation, and one of: (b)(1) inconsistent adjudications risk, (b)(2) declaratory/injunctive relief, or (b)(3) predominance of common questions + superiority. Certification is often the key battle.",
    analysis_framework=["Assess numerosity (typically 40+)", "Identify common questions of law or fact", "Evaluate named plaintiff typicality", "Confirm adequacy of representation and counsel", "For (b)(3): determine if common questions predominate", "Assess superiority of class treatment"],
    key_factors=["class_size", "common_questions", "typicality", "adequacy", "predominance", "manageability"],
    authority=AuthorityLevel.STATUTE,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.CRITICAL,
    precedents=[
        ControllingPrecedent("Wal-Mart v. Dukes", "564 U.S. 338", 2011, "SCOTUS", "Commonality requires common contention whose resolution will resolve an issue central to the validity of each class member's claims"),
        ControllingPrecedent("Comcast v. Behrend", "569 U.S. 27", 2013, "SCOTUS", "Damages model must be consistent with class-wide theory of liability"),
    ],
    jurisdiction_notes="CAFA (Class Action Fairness Act) provides federal jurisdiction for large interstate classes (>$5M, >100 members, minimal diversity).",
    risk_multipliers={"large_class": 0.6, "individual_issues_predominate": 1.8, "damages_model_problems": 1.5},
    damages_guidance="Aggregate class damages can be enormous. Settlement funds common. Cy pres distributions for unclaimed funds.",
    settlement_factors=["class_size", "damages_model", "certification_prospects", "opt_out_risk"],
    statute_of_limitations_years=None,
)

DOCTRINE_CACHE["class_action_settlement"] = DoctrineBlock(
    key="class_action_settlement",
    topic="Class Action Settlement Approval",
    category=LitigationCategory.CLASS_ACTION,
    keywords=["class settlement", "fairness hearing", "objectors", "cy pres", "coupon settlement", "fee award"],
    conclusion_template="Class settlements require court approval after fairness hearing. Court evaluates: (1) adequacy of recovery compared to potential, (2) reaction of class members, (3) stage of proceedings, (4) experience of counsel. CAFA requires notice to state/federal officials. Coupon settlements face heightened scrutiny.",
    analysis_framework=["Evaluate settlement amount relative to potential recovery", "Assess class notice adequacy", "Anticipate objector arguments", "Review attorneys' fee reasonableness", "Evaluate non-monetary terms", "Check CAFA notice requirements"],
    key_factors=["recovery_percentage", "class_notice", "objector_arguments", "fee_reasonableness", "claims_rate"],
    authority=AuthorityLevel.CASE_LAW,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.MEDIUM,
    precedents=[
        ControllingPrecedent("Amchem Products v. Windsor", "521 U.S. 591", 1997, "SCOTUS", "Settlement class must still satisfy Rule 23(a) and (b) requirements"),
    ],
    jurisdiction_notes="Circuit splits on fee calculation methods (lodestar vs. percentage). CAFA imposes additional requirements for coupon settlements.",
    risk_multipliers={"high_claims_rate": 0.7, "significant_objections": 1.3, "coupon_settlement": 1.5},
    damages_guidance="Settlement fund typically 2-20% of maximum damages. Fees typically 15-33% of recovery.",
    statute_of_limitations_years=None,
)

# --- ADDITIONAL TORT DOCTRINES ---

DOCTRINE_CACHE["statute_of_limitations_analysis"] = DoctrineBlock(
    key="statute_of_limitations_analysis",
    topic="Statute of Limitations Framework",
    category=LitigationCategory.CIVIL_PROCEDURE,
    keywords=["statute of limitations", "discovery rule", "tolling", "accrual", "repose", "laches"],
    conclusion_template="The statute of limitations bars claims not filed within the prescribed period. Accrual typically begins at injury, but the discovery rule delays accrual until plaintiff knew or should have known of injury and its cause. Tolling doctrines: fraudulent concealment, minority, mental incapacity, defendant absence.",
    analysis_framework=["Identify applicable limitations period", "Determine accrual date (injury vs. discovery)", "Evaluate tolling doctrines", "Distinguish limitations (procedural) from repose (substantive)", "Assess laches defense for equitable claims"],
    key_factors=["limitations_period", "accrual_date", "discovery_rule", "tolling_events", "repose_period"],
    authority=AuthorityLevel.STATUTE,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.CRITICAL,
    precedents=[
        ControllingPrecedent("TRW Inc. v. Andrews", "534 U.S. 19", 2001, "SCOTUS", "Discovery rule does not apply unless statute expressly or implicitly requires it"),
    ],
    jurisdiction_notes="Limitations periods vary dramatically by claim type and jurisdiction. Federal borrowing of state limitations for some federal claims.",
    risk_multipliers={"clearly_expired": 2.5, "discovery_rule_applies": 0.7, "fraudulent_concealment": 0.6},
    statute_of_limitations_years=None,
)

DOCTRINE_CACHE["summary_judgment_standard"] = DoctrineBlock(
    key="summary_judgment_standard",
    topic="Summary Judgment Standard",
    category=LitigationCategory.CIVIL_PROCEDURE,
    keywords=["summary judgment", "rule 56", "genuine dispute", "material fact", "no triable issue"],
    conclusion_template="Summary judgment under Rule 56 is appropriate when there is no genuine dispute as to any material fact and the movant is entitled to judgment as a matter of law. Court views evidence in light most favorable to non-movant. Non-movant must go beyond pleadings and present specific facts showing genuine dispute.",
    analysis_framework=["Identify material facts in dispute", "Determine if disputes are genuine (supported by evidence)", "View all evidence in light most favorable to non-movant", "Assess whether movant has met initial burden", "Evaluate non-movant's response evidence"],
    key_factors=["material_facts", "genuine_dispute", "evidence_sufficiency", "favorable_view", "movant_burden"],
    authority=AuthorityLevel.STATUTE,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.HIGH,
    precedents=[
        ControllingPrecedent("Celotex Corp. v. Catrett", "477 U.S. 317", 1986, "SCOTUS", "Moving party can meet burden by pointing to absence of evidence on essential element"),
        ControllingPrecedent("Anderson v. Liberty Lobby", "477 U.S. 242", 1986, "SCOTUS", "Only disputes over material facts preclude summary judgment; substantive law determines materiality"),
    ],
    jurisdiction_notes="Summary judgment practice varies by judge and jurisdiction. Some judges are more reluctant to grant in complex cases.",
    risk_multipliers={"strong_documentary_evidence": 0.6, "credibility_disputes": 1.5, "complex_facts": 1.3},
    statute_of_limitations_years=None,
)

DOCTRINE_CACHE["discovery_cost_modeling"] = DoctrineBlock(
    key="discovery_cost_modeling",
    topic="Discovery Cost Analysis",
    category=LitigationCategory.CIVIL_PROCEDURE,
    keywords=["discovery", "e-discovery", "proportionality", "deposition", "document production", "rule 26"],
    conclusion_template="Discovery costs can be the largest component of litigation expense. Rule 26(b)(1) proportionality factors: importance of issues, amount in controversy, parties' resources, importance of discovery to case, burden vs. benefit. E-discovery costs dominated by review, not collection.",
    analysis_framework=["Estimate document volume for production", "Model e-discovery costs (collection, processing, review, production)", "Estimate deposition costs (witnesses, experts, videographers)", "Factor in expert witness retention costs", "Apply proportionality limitations", "Consider cost-shifting under Rule 26(c)"],
    key_factors=["document_volume", "custodian_count", "deposition_count", "expert_witnesses", "proportionality", "e_discovery_platform"],
    authority=AuthorityLevel.STATUTE,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.HIGH,
    precedents=[
        ControllingPrecedent("Zubulake v. UBS Warburg", "217 F.R.D. 309", 2003, "S.D.N.Y.", "Landmark e-discovery cost-shifting framework based on seven-factor test"),
    ],
    jurisdiction_notes="Proportionality is now explicitly in Rule 26(b)(1). Preservation obligations trigger at reasonable anticipation of litigation.",
    risk_multipliers={"high_document_volume": 0.6, "international_discovery": 0.5, "privilege_issues": 0.7},
    damages_guidance="Discovery costs range from tens of thousands to tens of millions depending on case complexity.",
    statute_of_limitations_years=None,
)

DOCTRINE_CACHE["settlement_valuation"] = DoctrineBlock(
    key="settlement_valuation",
    topic="Settlement Valuation Framework",
    category=LitigationCategory.CIVIL_PROCEDURE,
    keywords=["settlement", "valuation", "expected value", "batna", "zopa", "negotiation"],
    conclusion_template="Settlement value = probability of liability * probable damages - litigation costs. A rational defendant settles when expected trial cost exceeds settlement. Zone of possible agreement (ZOPA) exists when plaintiff's minimum > defendant's maximum only when there is no overlap. Key: both sides must have accurate risk assessment.",
    analysis_framework=["Calculate expected value of claims (probability * damages)", "Model total litigation costs through trial", "Determine BATNA for each party", "Identify ZOPA boundaries", "Factor in non-monetary considerations (publicity, precedent, time)", "Apply discount rate for time value and risk"],
    key_factors=["liability_probability", "damages_range", "litigation_costs", "time_to_trial", "publicity_risk", "precedent_value"],
    authority=AuthorityLevel.PRACTICE_GUIDE,
    confidence=ConfidenceLevel.GENERALLY_ACCEPTED,
    risk_severity=RiskSeverity.MEDIUM,
    precedents=[],
    jurisdiction_notes="Mandatory mediation in many courts. Early neutral evaluation programs in some districts.",
    risk_multipliers={"strong_case": 0.7, "nuisance_value_only": 1.8, "bet_the_company": 0.5},
    damages_guidance="Settlement typically 10-75% of expected trial value, depending on risk factors and litigation stage.",
    statute_of_limitations_years=None,
)

DOCTRINE_CACHE["expert_witness_daubert"] = DoctrineBlock(
    key="expert_witness_daubert",
    topic="Expert Witness Admissibility (Daubert)",
    category=LitigationCategory.CIVIL_PROCEDURE,
    keywords=["daubert", "expert witness", "reliability", "methodology", "frye", "rule 702"],
    conclusion_template="Under Daubert/Rule 702, expert testimony must be based on sufficient facts, reliable principles and methods, and reliably applied to the case facts. Court acts as gatekeeper. Factors: testability, peer review, error rate, general acceptance. Daubert challenges can be dispositive.",
    analysis_framework=["Assess expert qualifications", "Evaluate methodology reliability", "Determine if methodology was properly applied to case facts", "Consider testability and error rate", "Check peer review and publication", "Evaluate general acceptance in relevant field"],
    key_factors=["expert_qualifications", "methodology_reliability", "proper_application", "testability", "error_rate", "general_acceptance"],
    authority=AuthorityLevel.CASE_LAW,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.HIGH,
    precedents=[
        ControllingPrecedent("Daubert v. Merrell Dow", "509 U.S. 579", 1993, "SCOTUS", "Trial court is gatekeeper for expert testimony reliability under FRE 702"),
        ControllingPrecedent("Kumho Tire v. Carmichael", "526 U.S. 137", 1999, "SCOTUS", "Daubert gatekeeping applies to all expert testimony, not just scientific"),
    ],
    jurisdiction_notes="Federal courts and most states follow Daubert. A few states still use Frye general acceptance standard.",
    risk_multipliers={"strong_methodology": 0.7, "novel_theory": 1.5, "ipse_dixit": 2.0},
    statute_of_limitations_years=None,
)

DOCTRINE_CACHE["punitive_damages_analysis"] = DoctrineBlock(
    key="punitive_damages_analysis",
    topic="Punitive Damages Assessment",
    category=LitigationCategory.TORT_LIABILITY,
    keywords=["punitive damages", "exemplary damages", "reprehensibility", "due process", "ratio", "constitutional limit"],
    conclusion_template="Punitive damages require proof of reprehensible conduct (malice, fraud, gross negligence). Constitutional limits: single-digit ratio to compensatory damages generally required. Three BMW guideposts: (1) degree of reprehensibility, (2) ratio to compensatory damages, (3) comparison to civil penalties for comparable conduct.",
    analysis_framework=["Assess reprehensibility of defendant's conduct", "Evaluate the ratio to compensatory damages", "Compare to statutory civil penalties", "Consider defendant's financial condition", "Assess whether conduct was isolated or repeated", "Evaluate physical vs. economic harm"],
    key_factors=["reprehensibility", "damages_ratio", "civil_penalty_comparison", "defendant_wealth", "harm_type"],
    authority=AuthorityLevel.CASE_LAW,
    confidence=ConfidenceLevel.WELL_SETTLED,
    risk_severity=RiskSeverity.CRITICAL,
    precedents=[
        ControllingPrecedent("BMW of North America v. Gore", "517 U.S. 559", 1996, "SCOTUS", "Three guideposts for evaluating punitive damages constitutionality"),
        ControllingPrecedent("State Farm v. Campbell", "538 U.S. 408", 2003, "SCOTUS", "Single-digit ratio between punitive and compensatory damages generally required"),
    ],
    jurisdiction_notes="Some states cap punitive damages by statute. Some require clear and convincing evidence. Bifurcated trials in some jurisdictions.",
    risk_multipliers={"intentional_misconduct": 0.5, "pattern_of_conduct": 0.6, "economic_harm_only": 1.3},
    damages_guidance="Typically 1:1 to 9:1 ratio. Higher ratios possible for small compensatory awards with egregious conduct.",
    statute_of_limitations_years=None,
)

DOCTRINE_CACHE["indemnification_contribution"] = DoctrineBlock(
    key="indemnification_contribution",
    topic="Indemnification and Contribution",
    category=LitigationCategory.TORT_LIABILITY,
    keywords=["indemnification", "contribution", "joint tortfeasors", "comparative fault", "cross claims"],
    conclusion_template="Indemnification shifts entire loss from one tortfeasor to another based on contract or equitable principles. Contribution allows proportionate sharing among joint tortfeasors. Many jurisdictions have abolished joint and several liability or adopted comparative fault contribution.",
    analysis_framework=["Identify contractual indemnification obligations", "Assess equitable indemnification (active/passive negligence)", "Determine contribution rights among joint tortfeasors", "Apply comparative fault allocation", "Evaluate settlement bar and credit rules"],
    key_factors=["contractual_indemnity", "equitable_indemnity", "comparative_fault", "settlement_credit", "joint_several_liability"],
    authority=AuthorityLevel.CASE_LAW,
    confidence=ConfidenceLevel.JURISDICTION_DEPENDENT,
    risk_severity=RiskSeverity.MEDIUM,
    precedents=[
        ControllingPrecedent("McDermott v. AmClyde", "511 U.S. 202", 1994, "SCOTUS", "Proportionate share settlement credit rule in admiralty (rejected pro tanto)"),
    ],
    jurisdiction_notes="Joint and several liability rules vary dramatically. Some states retain it fully; others apply only to economic damages.",
    risk_multipliers={"strong_indemnity_clause": 0.5, "multiple_tortfeasors": 0.7, "no_indemnity_agreement": 1.3},
    statute_of_limitations_years=None,
)

# ============================================================================
# DOCTRINE INTERACTIONS
# ============================================================================

DOCTRINE_INTERACTIONS: List[DoctrineInteraction] = [
    DoctrineInteraction("standing_article_iii", "subject_matter_jurisdiction", "prerequisite", 0.95, "Standing is a component of subject matter jurisdiction"),
    DoctrineInteraction("personal_jurisdiction", "venue_analysis", "related", 0.85, "Jurisdiction and venue often analyzed together"),
    DoctrineInteraction("negligence_elements", "strict_liability_tort", "alternative_theory", 0.80, "Often pled as alternative theories"),
    DoctrineInteraction("negligence_elements", "punitive_damages_analysis", "triggers", 0.70, "Gross negligence may support punitive damages"),
    DoctrineInteraction("breach_of_contract", "contract_damages_calculation", "prerequisite", 0.95, "Breach must be established before damages"),
    DoctrineInteraction("breach_of_contract", "anticipatory_repudiation", "related", 0.85, "Anticipatory repudiation is a form of breach"),
    DoctrineInteraction("employment_discrimination", "wrongful_termination", "overlapping", 0.80, "Discrimination often results in termination claims"),
    DoctrineInteraction("securities_fraud_10b5", "securities_class_certification", "sequential", 0.90, "Class cert follows substantive fraud claims"),
    DoctrineInteraction("securities_fraud_10b5", "class_action_certification", "related", 0.85, "Securities fraud often proceeds as class action"),
    DoctrineInteraction("design_defect", "manufacturing_defect", "alternative_theory", 0.75, "Often pled as alternative defect theories"),
    DoctrineInteraction("design_defect", "failure_to_warn", "complementary", 0.80, "Warning deficiency often accompanies design defect"),
    DoctrineInteraction("insurance_coverage_duty_to_defend", "insurance_bad_faith", "triggers", 0.85, "Wrongful denial of defense triggers bad faith"),
    DoctrineInteraction("cercla_superfund", "toxic_tort_causation", "related", 0.75, "CERCLA sites often generate toxic tort litigation"),
    DoctrineInteraction("regulatory_enforcement_risk", "qui_tam_whistleblower", "complementary", 0.80, "FCA actions parallel regulatory enforcement"),
    DoctrineInteraction("class_action_certification", "class_action_settlement", "sequential", 0.95, "Settlement follows certification"),
    DoctrineInteraction("statute_of_limitations_analysis", "discovery_cost_modeling", "related", 0.60, "SOL analysis affects scope of discoverable periods"),
    DoctrineInteraction("summary_judgment_standard", "expert_witness_daubert", "related", 0.75, "Daubert exclusion often precedes summary judgment"),
    DoctrineInteraction("settlement_valuation", "discovery_cost_modeling", "complementary", 0.85, "Discovery costs factor heavily into settlement math"),
    DoctrineInteraction("patent_infringement", "trade_secret_misappropriation", "alternative_theory", 0.65, "IP claims sometimes overlap"),
    DoctrineInteraction("trademark_infringement", "fraud_and_misrepresentation", "related", 0.60, "Consumer confusion can overlap with fraud theories"),
    DoctrineInteraction("indemnification_contribution", "insurance_subrogation", "related", 0.70, "Both involve shifting loss to responsible party"),
    DoctrineInteraction("sherman_act_section1", "sherman_act_section2", "complementary", 0.85, "Section 1 and 2 often alleged together"),
    DoctrineInteraction("flsa_wage_hour", "class_action_certification", "related", 0.80, "FLSA collective actions are quasi-class actions"),
]


# ============================================================================
# ACCESS FUNCTIONS
# ============================================================================

def get_all_doctrine_keys() -> List[str]:
    """Return all doctrine keys."""
    return sorted(DOCTRINE_CACHE.keys())


def get_doctrine(key: str) -> Optional[DoctrineBlock]:
    """Retrieve a specific doctrine block."""
    return DOCTRINE_CACHE.get(key)


def get_doctrines_by_category(category: LitigationCategory) -> List[DoctrineBlock]:
    """Retrieve all doctrines for a given category."""
    return [d for d in DOCTRINE_CACHE.values() if d.category == category]


def get_doctrine_count() -> int:
    """Return total doctrine count."""
    return len(DOCTRINE_CACHE)


def get_interaction_edges_for(key: str) -> List[DoctrineInteraction]:
    """Return all interaction edges involving this doctrine key."""
    return [i for i in DOCTRINE_INTERACTIONS if i.source_key == key or i.target_key == key]


def get_all_categories() -> List[str]:
    """Return all unique categories from loaded doctrines."""
    return sorted({d.category.value for d in DOCTRINE_CACHE.values()})


def search_doctrines_by_keyword(keyword: str) -> List[DoctrineBlock]:
    """Search doctrines by keyword matching."""
    keyword_lower = keyword.lower()
    results: List[DoctrineBlock] = []
    for block in DOCTRINE_CACHE.values():
        if any(keyword_lower in kw.lower() for kw in block.keywords):
            results.append(block)
        elif keyword_lower in block.topic.lower():
            results.append(block)
        elif keyword_lower in block.conclusion_template.lower():
            results.append(block)
    return results


def get_coverage_map() -> DoctrineCoverageMap:
    """Create and return a coverage map of all doctrines."""
    return DoctrineCoverageMap(DOCTRINE_CACHE)
