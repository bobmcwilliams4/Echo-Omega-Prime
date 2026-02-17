"""
LG16 ADR Engine - Doctrine Cache
=================================
Comprehensive ADR doctrine blocks covering arbitration (FAA, RUAA, AAA, JAMS,
FINRA, ICSID, UNCITRAL, ICC), mediation (UMA, facilitative, evaluative,
transformative), negotiation theory, ODR, hybrid processes, class action
arbitration, arbitrability, clause drafting, judicial review, enforcement,
discovery, emergency arbitrators, multi-party arbitration, Texas ADR Act,
securities arbitration, and oil & gas ADR.

Engine: LG16 | Version: 2.0.0 | Blocks: 55+
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from loguru import logger

ENGINE_ROOT = Path(__file__).parent
DOCTRINE_CACHE_DIR = ENGINE_ROOT / "doctrine_cache"
DOCTRINE_CACHE_DIR.mkdir(parents=True, exist_ok=True)

DOCTRINE_VERSION = "2.0.0"
ENGINE_ID = "LG16"


@dataclass
class DoctrineCacheBlock:
    """Single doctrine knowledge block for the ADR engine."""

    topic: str
    category: str
    authority_weight: float
    citations: list[str]
    content: str
    related_topics: list[str]
    last_verified: str
    hash_key: str = ""

    def __post_init__(self) -> None:
        if not self.hash_key:
            self.hash_key = self._compute_hash()

    def _compute_hash(self) -> str:
        payload = f"{self.topic}|{self.category}|{self.content}|{DOCTRINE_VERSION}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def matches_query(self, query: str) -> float:
        query_lower = query.lower()
        tokens = re.split(r"\W+", query_lower)
        tokens = [t for t in tokens if len(t) > 2]
        if not tokens:
            return 0.0
        content_lower = self.content.lower()
        topic_lower = self.topic.lower()
        cat_lower = self.category.lower()
        citations_text = " ".join(self.citations).lower()
        score = 0.0
        for token in tokens:
            if token in topic_lower:
                score += 3.0
            if token in cat_lower:
                score += 2.0
            if token in content_lower:
                score += 1.0
            if token in citations_text:
                score += 1.5
        score = score / (len(tokens) * 3.0)
        return min(score, 1.0)


@dataclass
class DoctrineCacheIndex:
    """Index over all doctrine blocks for fast retrieval."""

    blocks: dict[str, DoctrineCacheBlock] = field(default_factory=dict)
    category_index: dict[str, list[str]] = field(default_factory=dict)
    topic_index: dict[str, str] = field(default_factory=dict)
    built_at: str = ""

    def build(self, blocks: dict[str, DoctrineCacheBlock]) -> None:
        self.blocks = blocks
        self.category_index = {}
        self.topic_index = {}
        self.built_at = datetime.now(timezone.utc).isoformat()
        for key, block in blocks.items():
            self.topic_index[block.topic.lower()] = key
            cat = block.category.lower()
            if cat not in self.category_index:
                self.category_index[cat] = []
            self.category_index[cat].append(key)
        logger.info(
            "Doctrine index built: {} blocks, {} categories",
            len(self.blocks),
            len(self.category_index),
        )

    def search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        results: list[tuple[str, float]] = []
        for key, block in self.blocks.items():
            score = block.matches_query(query)
            if score > 0.05:
                results.append((key, score))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def get_by_category(self, category: str) -> list[DoctrineCacheBlock]:
        cat = category.lower()
        keys = self.category_index.get(cat, [])
        return [self.blocks[k] for k in keys if k in self.blocks]

    def get_by_topic(self, topic: str) -> DoctrineCacheBlock | None:
        key = self.topic_index.get(topic.lower())
        if key and key in self.blocks:
            return self.blocks[key]
        return None


# ---------------------------------------------------------------------------
# DOCTRINE BLOCKS - 55 comprehensive ADR doctrine entries
# ---------------------------------------------------------------------------

DOCTRINE_BLOCKS: dict[str, DoctrineCacheBlock] = {

    # ======================================================================
    # FEDERAL ARBITRATION ACT (FAA) - 9 USC 1-16
    # ======================================================================

    "faa_scope_applicability": DoctrineCacheBlock(
        topic="FAA Scope and Applicability",
        category="federal_arbitration",
        authority_weight=0.98,
        citations=[
            "9 USC 1-16",
            "Circuit City Stores v Adams, 532 US 105 (2001)",
            "Allied-Bruce Terminix v Dobson, 513 US 265 (1995)",
            "Citizens Bank v Alafabco, 539 US 52 (2003)",
            "New Prime Inc v Oliveira, 586 US 105 (2019)",
        ],
        content=(
            "The Federal Arbitration Act (FAA), enacted in 1925 (ch. 213, 43 Stat. 883), "
            "establishes a strong federal policy favoring arbitration agreements. Section 1 "
            "defines 'maritime transactions' and 'commerce' broadly, reaching the full extent "
            "of Congress's Commerce Clause power. The Act applies to any written arbitration "
            "agreement in a contract evidencing a transaction involving interstate or foreign "
            "commerce. Section 1 contains a residual exclusion for 'contracts of employment "
            "of seamen, railroad employees, or any other class of workers engaged in foreign "
            "or interstate commerce.' In Circuit City v Adams (2001), the Supreme Court "
            "narrowly construed this exclusion to cover only transportation workers actually "
            "engaged in interstate movement of goods, not all employment contracts. In New "
            "Prime v Oliveira (2019), the Court held that independent contractor agreements "
            "can fall within Section 1's exclusion if the worker is a transportation worker. "
            "The FAA does not itself create federal subject-matter jurisdiction; parties must "
            "have an independent basis for federal jurisdiction (diversity or federal question). "
            "However, the FAA's substantive provisions apply in both federal and state courts "
            "under the Supremacy Clause, preempting contrary state laws that single out "
            "arbitration agreements for disfavored treatment."
        ),
        related_topics=[
            "faa_preemption", "faa_section_2_savings_clause",
            "employment_arbitration", "transportation_worker_exclusion",
        ],
        last_verified="2026-02-01",
    ),

    "faa_section_2_savings_clause": DoctrineCacheBlock(
        topic="FAA Section 2 - Savings Clause",
        category="federal_arbitration",
        authority_weight=0.97,
        citations=[
            "9 USC 2",
            "AT&T Mobility v Concepcion, 563 US 333 (2011)",
            "Kindred Nursing Centers v Clark, 581 US 246 (2017)",
            "Doctor's Associates v Casarotto, 517 US 681 (1996)",
            "Perry v Thomas, 482 US 483 (1987)",
        ],
        content=(
            "FAA Section 2 provides that written arbitration agreements 'shall be valid, "
            "irrevocable, and enforceable, save upon such grounds as exist at law or in "
            "equity for the revocation of any contract.' This 'savings clause' preserves "
            "generally applicable contract defenses such as fraud, duress, and unconscionability "
            "as grounds for invalidating arbitration agreements. However, in AT&T Mobility v "
            "Concepcion (2011), the Supreme Court held that even generally applicable state "
            "contract doctrines are preempted if they have a disproportionate impact on "
            "arbitration or stand as an obstacle to the FAA's objectives. The Court struck "
            "down California's Discover Bank rule (treating class-action waivers in consumer "
            "adhesion contracts as unconscionable) because it effectively mandated class "
            "procedures in arbitration, conflicting with the FAA's preference for bilateral "
            "arbitration. In Kindred Nursing v Clark (2017), the Court invalidated Kentucky's "
            "'clear statement' rule requiring powers of attorney to specifically authorize "
            "waiver of the right to a jury trial before binding a principal to an arbitration "
            "agreement. The savings clause thus permits only defenses that apply equally to "
            "all contracts and do not derive their meaning from the fact that an agreement "
            "to arbitrate is at issue."
        ),
        related_topics=[
            "faa_scope_applicability", "unconscionability_defense",
            "class_action_arbitration", "faa_preemption",
        ],
        last_verified="2026-02-01",
    ),

    "faa_section_3_stay": DoctrineCacheBlock(
        topic="FAA Section 3 - Stay of Proceedings",
        category="federal_arbitration",
        authority_weight=0.95,
        citations=[
            "9 USC 3",
            "Smith v Spizzirri, 601 US ___ (2024)",
            "Moses H. Cone Memorial Hospital v Mercury Construction, 460 US 1 (1983)",
        ],
        content=(
            "FAA Section 3 requires a federal court to stay litigation upon application of "
            "a party if any issue in the suit is referable to arbitration under an agreement "
            "in writing. The court must be satisfied that the issue is indeed arbitrable. In "
            "Smith v Spizzirri (2024), the Supreme Court unanimously held that when a federal "
            "court finds that a dispute is subject to arbitration, Section 3 requires the "
            "court to stay the action rather than dismiss it. This resolved a circuit split "
            "where some courts had dismissed rather than stayed cases. The stay preserves "
            "the right to return to federal court to confirm, vacate, or modify the award "
            "under FAA Sections 9-11 without requiring a new action. The stay remains in "
            "effect until the arbitration has been had in accordance with the terms of the "
            "agreement. The moving party must show: (1) a valid written agreement to arbitrate, "
            "(2) the dispute falls within the scope of the agreement, (3) the opposing party "
            "has failed to comply with the agreement, and (4) the moving party has not "
            "waived its right to arbitrate."
        ),
        related_topics=[
            "faa_section_4_compel", "waiver_of_arbitration_right",
            "faa_scope_applicability",
        ],
        last_verified="2026-02-01",
    ),

    "faa_section_4_compel": DoctrineCacheBlock(
        topic="FAA Section 4 - Petition to Compel Arbitration",
        category="federal_arbitration",
        authority_weight=0.95,
        citations=[
            "9 USC 4",
            "Badgerow v Walters, 596 US 1 (2022)",
            "Vaden v Discover Bank, 556 US 49 (2009)",
            "Granite Rock Co v Teamsters, 561 US 287 (2010)",
        ],
        content=(
            "FAA Section 4 allows a party aggrieved by another party's failure to arbitrate "
            "to petition a federal court for an order directing that arbitration proceed. The "
            "petition must be filed in a district court that would have jurisdiction under "
            "title 28 (i.e., independent federal jurisdiction is required). In Badgerow v "
            "Walters (2022), the Supreme Court held that the 'look-through' approach to "
            "jurisdiction (examining the underlying substantive dispute) applies only to "
            "Section 4 petitions to compel, not to Section 9 or 10 petitions to confirm "
            "or vacate awards. The court on a Section 4 petition determines only whether "
            "a valid arbitration agreement exists and whether the dispute falls within its "
            "scope. Questions of procedural arbitrability (timeliness, prerequisites, "
            "conditions precedent) are generally for the arbitrator, not the court, under "
            "Howsam v Dean Witter Reynolds, 537 US 79 (2002). The court must order "
            "arbitration 'in accordance with the terms of the agreement' and cannot alter "
            "the agreed-upon procedures."
        ),
        related_topics=[
            "faa_section_3_stay", "arbitrability_substantive",
            "arbitrability_procedural", "delegation_clause",
        ],
        last_verified="2026-02-01",
    ),

    "faa_section_10_vacatur": DoctrineCacheBlock(
        topic="FAA Section 10 - Vacatur of Arbitration Awards",
        category="federal_arbitration",
        authority_weight=0.97,
        citations=[
            "9 USC 10",
            "Hall Street Associates v Mattel, 552 US 576 (2008)",
            "Stolt-Nielsen SA v AnimalFeeds Int'l, 559 US 662 (2010)",
            "Oxford Health Plans v Sutter, 569 US 564 (2013)",
            "Biller v Toyota Motor Corp, 668 F.3d 655 (9th Cir. 2012)",
        ],
        content=(
            "FAA Section 10 provides four exclusive statutory grounds for vacating an "
            "arbitration award: (1) the award was procured by corruption, fraud, or undue "
            "means (Section 10(a)(1)); (2) there was evident partiality or corruption in "
            "the arbitrators (Section 10(a)(2)); (3) the arbitrators were guilty of "
            "misconduct in refusing to postpone the hearing upon sufficient cause shown, "
            "refusing to hear evidence pertinent and material to the controversy, or any "
            "other misbehavior prejudicing the rights of any party (Section 10(a)(3)); or "
            "(4) the arbitrators exceeded their powers, or so imperfectly executed them "
            "that a mutual, final, and definite award upon the subject matter was not made "
            "(Section 10(a)(4)). In Hall Street v Mattel (2008), the Supreme Court held "
            "that these four grounds are exclusive and cannot be expanded by private "
            "agreement. Parties cannot contract for expanded judicial review (e.g., review "
            "for errors of law). The 'manifest disregard of the law' standard, recognized "
            "by some circuits as a non-statutory ground, was cast into doubt by Hall Street "
            "but has survived in some circuits as a judicial gloss on Section 10(a)(4). A "
            "motion to vacate must be served within three months after the award is filed "
            "or delivered (Section 12)."
        ),
        related_topics=[
            "manifest_disregard", "evident_partiality",
            "faa_section_9_confirmation", "faa_section_11_modification",
        ],
        last_verified="2026-02-01",
    ),

    "faa_section_9_confirmation": DoctrineCacheBlock(
        topic="FAA Section 9 - Confirmation of Awards",
        category="federal_arbitration",
        authority_weight=0.94,
        citations=[
            "9 USC 9",
            "Badgerow v Walters, 596 US 1 (2022)",
            "Cortez Byrd Chips v Bill Harbert Construction, 529 US 193 (2000)",
        ],
        content=(
            "FAA Section 9 provides that if the parties have agreed that a judgment of the "
            "court shall be entered upon the award, any party to the arbitration may apply "
            "to the court for an order confirming the award. The court must confirm the "
            "award unless it is vacated, modified, or corrected under Sections 10 or 11. "
            "Confirmation converts the arbitral award into an enforceable court judgment. "
            "The application must be made within one year after the award is made. In "
            "Badgerow v Walters (2022), the Supreme Court held that federal jurisdiction "
            "for confirmation actions under Section 9 cannot be established by 'looking "
            "through' to the underlying dispute; rather, an independent basis for federal "
            "jurisdiction must exist on the face of the application. This means many "
            "confirmation actions must be brought in state court. Under Cortez Byrd, the "
            "venue provisions of Section 9 are permissive, not mandatory, so parties can "
            "also confirm awards under the general venue statute 28 USC 1391."
        ),
        related_topics=[
            "faa_section_10_vacatur", "faa_section_4_compel",
            "award_enforcement_domestication",
        ],
        last_verified="2026-02-01",
    ),

    "faa_preemption": DoctrineCacheBlock(
        topic="FAA Preemption of State Law",
        category="federal_arbitration",
        authority_weight=0.97,
        citations=[
            "Southland Corp v Keating, 465 US 1 (1984)",
            "AT&T Mobility v Concepcion, 563 US 333 (2011)",
            "DIRECTV v Imburgia, 577 US 47 (2015)",
            "Viking River Cruises v Moriana, 596 US 639 (2022)",
            "Kindred Nursing Centers v Clark, 581 US 246 (2017)",
        ],
        content=(
            "The FAA creates a body of substantive federal law that preempts state laws "
            "hostile to arbitration. In Southland Corp v Keating (1984), the Court held "
            "that the FAA applies in state courts and preempts state statutes that withdraw "
            "disputes from arbitration. Preemption occurs in two situations: (1) conflict "
            "preemption, where a state law stands as an obstacle to accomplishment of the "
            "FAA's objectives; and (2) discrimination preemption, where a state law singles "
            "out arbitration agreements for disfavored treatment compared to other contracts. "
            "In Concepcion (2011), the Court found that California's unconscionability "
            "doctrine, as applied to class-action waivers in arbitration agreements, was "
            "preempted because it effectively required class procedures incompatible with "
            "bilateral arbitration. In Viking River Cruises v Moriana (2022), the Court "
            "held that the FAA preempted California's rule (from Iskanian) that barred "
            "waiver of the right to bring representative PAGA claims in any forum. The "
            "equal-treatment principle requires that any defense used to invalidate an "
            "arbitration agreement must apply equally to contracts generally. State "
            "procedural rules that discriminate against arbitration (special notice "
            "requirements, clear-statement rules, etc.) are preempted."
        ),
        related_topics=[
            "faa_section_2_savings_clause", "unconscionability_defense",
            "class_action_arbitration", "faa_scope_applicability",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # REVISED UNIFORM ARBITRATION ACT (RUAA)
    # ======================================================================

    "ruaa_overview": DoctrineCacheBlock(
        topic="Revised Uniform Arbitration Act (RUAA)",
        category="state_arbitration",
        authority_weight=0.88,
        citations=[
            "Uniform Arbitration Act (2000), 7 ULA 1",
            "RUAA Section 6 (Validity of Arbitration Agreement)",
            "RUAA Section 8 (Provisional Remedies)",
            "RUAA Section 10 (Consolidation)",
            "RUAA Section 23 (Vacatur)",
        ],
        content=(
            "The Revised Uniform Arbitration Act (RUAA), promulgated by the Uniform Law "
            "Commission in 2000, modernized the original 1955 Uniform Arbitration Act (UAA). "
            "As of 2026, 21 states and the District of Columbia have adopted the RUAA (in "
            "whole or with modifications). Key innovations include: (1) Section 6 codifies "
            "separability (the arbitration clause survives invalidity of the container "
            "contract) and permits courts to decide whether conditions precedent to "
            "arbitration have been met; (2) Section 8 expressly authorizes courts to grant "
            "provisional remedies (attachment, preliminary injunction) before or during "
            "arbitration without waiving the right to arbitrate; (3) Section 10 allows "
            "consolidation of related arbitrations if all parties agree or if the court "
            "finds consolidation appropriate; (4) Section 11 addresses arbitrator immunity "
            "from civil liability; (5) Section 14 expands arbitrator subpoena powers; "
            "(6) Section 15 codifies discovery rules for arbitration, allowing limited "
            "discovery as ordered by the arbitrator; (7) Section 17 permits arbitrators to "
            "award punitive damages and attorneys' fees to the same extent as a court; "
            "(8) Section 21 addresses remedies and confirms that arbitrators can award "
            "whatever relief would be available in court. Vacatur grounds (Section 23) "
            "largely mirror FAA Section 10 but add corruption as a separate ground."
        ),
        related_topics=[
            "faa_scope_applicability", "state_arbitration_statutes",
            "arbitrator_powers", "provisional_remedies",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # AAA RULES
    # ======================================================================

    "aaa_commercial_rules": DoctrineCacheBlock(
        topic="AAA Commercial Arbitration Rules",
        category="institutional_rules",
        authority_weight=0.90,
        citations=[
            "AAA Commercial Arbitration Rules and Mediation Procedures (2013, amended 2023)",
            "AAA Rule R-1 (Agreement of Parties)",
            "AAA Rule R-12 (Appointment of Arbitrator)",
            "AAA Rule R-21 (Exchange of Information)",
            "AAA Rule R-33 (Evidence)",
            "AAA Rule R-47 (Award)",
        ],
        content=(
            "The AAA Commercial Arbitration Rules govern arbitrations administered by the "
            "American Arbitration Association for general business disputes. Key provisions: "
            "(1) Filing and initiation: A party files a demand with the AAA office, stating "
            "the nature of the dispute, remedy sought, and the arbitration clause. Filing "
            "fees are based on a graduated schedule tied to claim amount. (2) Arbitrator "
            "selection: The AAA provides lists of potential arbitrators using its National "
            "Roster. Parties strike and rank candidates. If no mutual selection, the AAA "
            "appoints. For claims over $1M, a three-arbitrator panel is presumed unless "
            "parties agree otherwise. (3) Discovery: Rule R-21 ('Exchange of Information') "
            "permits the arbitrator to order document exchange and, in appropriate cases, "
            "depositions. Discovery is more limited than federal litigation. (4) Hearings: "
            "Conducted in person unless parties agree otherwise. Each party presents "
            "witnesses and evidence. The arbitrator controls the proceedings. Formal rules "
            "of evidence do not apply; the arbitrator determines relevance and materiality. "
            "(5) Awards: Must be rendered within 30 days of closing the hearing. Reasoned "
            "awards available upon joint request. The award is final and binding. "
            "(6) Large/Complex cases ($500K+): Special rules apply including mandatory "
            "preliminary hearing, three-arbitrator panel, and expanded discovery."
        ),
        related_topics=[
            "aaa_construction_rules", "aaa_employment_rules",
            "arbitration_discovery", "arbitrator_selection",
        ],
        last_verified="2026-02-01",
    ),

    "aaa_construction_rules": DoctrineCacheBlock(
        topic="AAA Construction Industry Arbitration Rules",
        category="institutional_rules",
        authority_weight=0.88,
        citations=[
            "AAA Construction Industry Arbitration Rules and Mediation Procedures (2015)",
            "AIA Document A201-2017 Section 15.4",
            "ConsensusDocs 200 Article 12",
        ],
        content=(
            "The AAA Construction Industry Arbitration Rules are tailored for disputes "
            "arising from construction projects. Three procedural tracks: (1) Fast Track "
            "Procedures (claims under $100,000): Streamlined process with a single "
            "arbitrator, hearing completed within 45 days, limited discovery, award within "
            "14 days of hearing close. (2) Regular Procedures ($100K-$1M): Standard "
            "arbitration with one or three arbitrators, preliminary hearing to set schedule, "
            "moderate discovery, site inspections by arbitrator permitted. (3) Procedures "
            "for Large, Complex Construction Disputes ($1M+): Three-arbitrator panel with "
            "construction expertise, comprehensive preliminary hearing, expanded discovery "
            "including depositions, multiple hearing days, site inspections, and detailed "
            "reasoned award. Special features of construction arbitration include: "
            "(a) arbitrator panels drawn from construction professionals (architects, "
            "engineers, contractors, lawyers); (b) interim measures including preservation "
            "of evidence; (c) joinder of additional parties (subcontractors, suppliers) "
            "with consent; (d) consolidation of related disputes on the same project; "
            "(e) emergency measures of protection under the AAA Optional Rules for "
            "Emergency Measures. AIA A201-2017 Section 15.4 specifies AAA construction "
            "rules as the default arbitration forum for AIA contract disputes, with "
            "mediation as a condition precedent to arbitration."
        ),
        related_topics=[
            "aaa_commercial_rules", "construction_arbitration",
            "multi_party_arbitration", "consolidation_joinder",
        ],
        last_verified="2026-02-01",
    ),

    "aaa_employment_rules": DoctrineCacheBlock(
        topic="AAA Employment Arbitration Rules",
        category="institutional_rules",
        authority_weight=0.89,
        citations=[
            "AAA Employment Arbitration Rules and Mediation Procedures (2009)",
            "AAA Employment Due Process Protocol (1995)",
            "Cole v Burns International Security Services, 105 F.3d 1465 (DC Cir. 1997)",
            "Epic Systems Corp v Lewis, 584 US 497 (2018)",
        ],
        content=(
            "The AAA Employment Arbitration Rules implement the 1995 Due Process Protocol "
            "jointly developed by the AAA, ABA, and other organizations. The Protocol "
            "establishes minimum fairness standards for employment arbitration: (1) Right "
            "to representation: Employees may be represented by counsel or other designated "
            "representative at their own expense. (2) Fee allocation: Employer pays the "
            "arbitrator's compensation and AAA administrative fees beyond an initial filing "
            "fee (currently $200 for employees) that is comparable to court filing fees. "
            "Under Cole v Burns (DC Cir. 1997), requiring employees to pay significant "
            "arbitration costs may render an agreement unenforceable. (3) Arbitrator "
            "selection: Neutral panel with no financial interest in the outcome; AAA "
            "provides vetted list; parties can strike names. (4) Discovery: Adequate but "
            "not excessive; at minimum, one deposition per side, document exchange, and "
            "access to relevant employment records. (5) Remedies: Same as available in "
            "court, including compensatory damages, front pay, back pay, injunctive relief, "
            "punitive damages (where statutory), and attorneys' fees. (6) Written, reasoned "
            "awards: Required to enable meaningful judicial review. (7) Independence: "
            "The arbitration provider cannot be beholden to the employer as a repeat player. "
            "The Ending Forced Arbitration Act (PL 117-90, 2022) amends the FAA to allow "
            "employees to void pre-dispute arbitration agreements for sexual assault and "
            "harassment claims."
        ),
        related_topics=[
            "employment_arbitration", "unconscionability_defense",
            "class_action_arbitration", "ending_forced_arbitration_act",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # JAMS RULES
    # ======================================================================

    "jams_comprehensive_rules": DoctrineCacheBlock(
        topic="JAMS Comprehensive Arbitration Rules",
        category="institutional_rules",
        authority_weight=0.88,
        citations=[
            "JAMS Comprehensive Arbitration Rules & Procedures (2024)",
            "JAMS Rule 16 (Discovery)",
            "JAMS Rule 17 (Dispositive Motions)",
            "JAMS Rule 24 (Award)",
        ],
        content=(
            "JAMS Comprehensive Arbitration Rules govern arbitrations administered by JAMS "
            "for disputes without a specific dollar threshold. Key distinguishing features "
            "versus AAA: (1) Dispositive motions: Rule 17 expressly allows summary judgment "
            "or partial summary adjudication motions, which the arbitrator can grant if there "
            "is no genuine issue of material fact and the moving party is entitled to judgment "
            "as a matter of law. Many other institutional rules are silent on dispositive "
            "motions. (2) Discovery: Rule 16 provides broader discovery than typical AAA "
            "rules; arbitrator may order depositions, interrogatories, requests for "
            "production, and requests for admission. Document exchange is the default; "
            "additional discovery upon showing good cause. (3) Arbitrator selection: JAMS "
            "Arbitration Discovery Protocol allows parties to select from the JAMS panel; "
            "a single arbitrator is default unless parties agree or the dispute involves "
            "more than $250K (three-arbitrator panel). (4) Reasoned awards: Available on "
            "request of any party. (5) Interim relief: Arbitrator may grant injunctions, "
            "appoint receivers, and order other interim measures. (6) Class arbitration: "
            "JAMS has separate Class Action Procedures. (7) Fee structure: Based on "
            "hourly arbitrator rates (typically $400-$1,200/hour) plus administrative fees "
            "that vary by claim size."
        ),
        related_topics=[
            "jams_streamlined_rules", "jams_employment_rules",
            "arbitration_discovery", "dispositive_motions_arbitration",
        ],
        last_verified="2026-02-01",
    ),

    "jams_employment_rules": DoctrineCacheBlock(
        topic="JAMS Employment Arbitration Rules",
        category="institutional_rules",
        authority_weight=0.87,
        citations=[
            "JAMS Employment Arbitration Rules & Procedures (2024)",
            "JAMS Policy on Employment Arbitration Minimum Standards (2009)",
        ],
        content=(
            "JAMS Employment Arbitration Rules parallel AAA Employment Rules with some "
            "differences. JAMS Minimum Standards of Procedural Fairness require: (1) "
            "Neutral arbitrator with no financial dependence on the employer. (2) Adequate "
            "discovery including document exchange, depositions, and interrogatories. (3) "
            "All remedies that would be available in court, including statutory damages. "
            "(4) Written, reasoned awards. (5) Employer bears all costs beyond a reasonable "
            "employee filing fee (not exceeding the fee for filing in court). (6) Location "
            "of hearing in the county where the employee worked. (7) Right to representation "
            "by counsel. JAMS will decline to administer employment arbitrations that do "
            "not comply with the Minimum Standards, providing a check on one-sided employer "
            "arbitration programs. JAMS employment arbitrators are often retired judges "
            "with employment law expertise. Hearings are typically completed within 6-12 "
            "months depending on complexity. JAMS also offers employment mediation as an "
            "alternative to arbitration."
        ),
        related_topics=[
            "aaa_employment_rules", "employment_arbitration",
            "jams_comprehensive_rules", "unconscionability_defense",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # FINRA ARBITRATION
    # ======================================================================

    "finra_customer_arbitration": DoctrineCacheBlock(
        topic="FINRA Customer Dispute Arbitration",
        category="securities_arbitration",
        authority_weight=0.92,
        citations=[
            "FINRA Rule 12000 Series (Customer Code)",
            "Shearson/American Express v McMahon, 482 US 220 (1987)",
            "Rodriguez de Quijas v Shearson/American Express, 490 US 477 (1989)",
            "FINRA Rule 12100 (Definitions)",
            "FINRA Rule 12401 (Representation by Attorneys)",
            "FINRA Rule 12800 (Simplified Arbitration)",
        ],
        content=(
            "FINRA (Financial Industry Regulatory Authority) operates the largest securities "
            "dispute resolution forum in the United States, handling approximately 3,000-4,000 "
            "arbitration cases annually. The Customer Code (Rule 12000 series) governs "
            "disputes between customers and member firms/associated persons. Key features: "
            "(1) Mandatory arbitration: FINRA member firms are required to arbitrate disputes "
            "with customers if the customer's account agreement contains an arbitration clause "
            "(virtually all do) or if the customer elects arbitration. After Shearson v McMahon "
            "(1987), virtually all securities claims (fraud, suitability, churning, unauthorized "
            "trading) are arbitrable. (2) Panel composition: For claims over $100K, a three- "
            "arbitrator panel (one industry, two public arbitrators, unless the customer opts "
            "for all-public). For claims $50K-$100K, one arbitrator. (3) Simplified arbitration "
            "(Rule 12800): Claims under $50K decided on documents only, no hearing. (4) "
            "Discovery: FINRA Discovery Guide provides a comprehensive list of presumptively "
            "discoverable documents by claim type; additional discovery by arbitrator order. "
            "(5) Eligibility: Claims must be filed within 6 years of the event giving rise to "
            "the dispute (Rule 12206). (6) Awards: Must be rendered within 30 business days of "
            "closing. Arbitrators can award compensatory damages, interest, fees, and costs. "
            "Punitive damages are available. (7) Expungement: Separate process for associated "
            "persons to remove customer complaints from CRD records (FINRA Rule 2080)."
        ),
        related_topics=[
            "finra_industry_arbitration", "securities_arbitration_finra",
            "arbitration_discovery", "expungement_finra",
        ],
        last_verified="2026-02-01",
    ),

    "finra_industry_arbitration": DoctrineCacheBlock(
        topic="FINRA Industry Dispute Arbitration",
        category="securities_arbitration",
        authority_weight=0.89,
        citations=[
            "FINRA Rule 13000 Series (Industry Code)",
            "FINRA Rule 13100 (Definitions)",
            "FINRA Rule 13200 (Arbitration Under an Arbitration Agreement)",
        ],
        content=(
            "The FINRA Industry Code (Rule 13000 series) governs disputes between or among "
            "FINRA member firms and their associated persons (intra-industry disputes). "
            "These arise from employment termination, compensation disputes, raiding claims, "
            "non-compete agreements, and trade secret misappropriation. Key features: "
            "(1) Mandatory for registered persons: Under FINRA rules, industry disputes "
            "must be arbitrated if required by a written agreement or if the claim is between "
            "members/associated persons. (2) Panel: Three arbitrators for claims over $100K, "
            "one for smaller claims. All arbitrators are public (no industry arbitrators on "
            "intra-industry panels since 2020 rule change). (3) Discovery: Same framework as "
            "the Customer Code, with additional presumptively discoverable document lists "
            "for employment disputes. (4) Promissory notes: Broker recruiting bonuses are a "
            "major category; cases turn on contractual interpretation and whether conditions "
            "for repayment were met. (5) Raiding/solicitation: Claims by firms that departing "
            "brokers violated non-solicitation agreements or the Broker Protocol (where "
            "applicable). (6) Awards: Same 30-day timeline. Attorneys' fees and costs at "
            "arbitrator discretion. (7) Statutory employment claims: Title VII, ADEA, ADA, "
            "FLSA, and state equivalents are all arbitrable in FINRA."
        ),
        related_topics=[
            "finra_customer_arbitration", "employment_arbitration",
            "securities_arbitration_finra",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # INTERNATIONAL ARBITRATION - UNCITRAL, ICC, ICSID
    # ======================================================================

    "uncitral_arbitration_rules": DoctrineCacheBlock(
        topic="UNCITRAL Arbitration Rules (2021 Revision)",
        category="international_arbitration",
        authority_weight=0.92,
        citations=[
            "UNCITRAL Arbitration Rules (2013, as revised 2021)",
            "UNCITRAL Rules on Transparency in Treaty-Based Investor-State Arbitration (2014)",
            "UNCITRAL Model Law on International Commercial Arbitration (1985, amended 2006)",
        ],
        content=(
            "The UNCITRAL Arbitration Rules are designed for ad hoc (non-institutional) "
            "international commercial arbitrations but are also used by some institutions. "
            "Originally adopted in 1976, revised in 2010 and 2013, with the 2021 Expedited "
            "Arbitration Rules added. Key features: (1) Party autonomy: Parties choose "
            "the number of arbitrators (default is three), the seat, and applicable law. "
            "(2) Appointing authority: If parties cannot agree on an arbitrator, the "
            "Secretary-General of the Permanent Court of Arbitration (PCA) serves as "
            "appointing authority. (3) Procedure: Flexible; statement of claim and defense, "
            "document production (no automatic disclosure), oral hearing unless parties "
            "agree otherwise. (4) Interim measures: Article 26 gives arbitrators power "
            "to order interim measures (security for costs, preservation of evidence, "
            "injunctions). (5) Transparency Rules (2014): Apply to investor-State "
            "arbitrations commenced under the UNCITRAL Rules after April 1, 2014, unless "
            "parties opt out. Require public access to key documents, open hearings, and "
            "third-party submissions. (6) Expedited Rules (2021): For lower-value disputes; "
            "sole arbitrator, award within 6 months, limited document production. (7) The "
            "UNCITRAL Model Law, adopted by 85+ states and 130+ jurisdictions, harmonizes "
            "national arbitration laws and strongly favors enforcement of awards."
        ),
        related_topics=[
            "icc_arbitration_rules", "icsid_convention",
            "new_york_convention_enforcement", "international_commercial_arbitration",
        ],
        last_verified="2026-02-01",
    ),

    "icc_arbitration_rules": DoctrineCacheBlock(
        topic="ICC Arbitration Rules",
        category="international_arbitration",
        authority_weight=0.92,
        citations=[
            "ICC Rules of Arbitration (2021, effective January 1, 2021)",
            "ICC Article 4 (Request for Arbitration)",
            "ICC Article 23 (Terms of Reference)",
            "ICC Article 34 (Scrutiny of the Award)",
            "ICC Article 36 (Costs)",
        ],
        content=(
            "The International Chamber of Commerce (ICC) International Court of Arbitration "
            "is the world's leading institution for international commercial arbitration. "
            "ICC Rules (2021 edition) key features: (1) Request for Arbitration (Art. 4): "
            "Claimant files a Request with the ICC Secretariat including the agreement, "
            "claim summary, and any proposals on arbitrator number, seat, and language. (2) "
            "Terms of Reference (Art. 23): Unique to ICC; the arbitral tribunal prepares a "
            "document setting out the parties, issues in dispute, claims, and procedural "
            "timetable, signed by all parties. (3) Case management: Art. 22 empowers the "
            "tribunal to adopt case management techniques including bifurcation, document "
            "production orders, and abbreviated procedures. (4) Expedited Procedure (Art. 30, "
            "Appendix VI): Mandatory for disputes under $3M (unless opt-out); sole "
            "arbitrator, reduced timeline (6 months), no Terms of Reference required, "
            "award without reasons unless requested. (5) Scrutiny of Award (Art. 34): "
            "Unique to ICC; before signing, every award is reviewed by the ICC Court for "
            "form and substance (not deciding the merits but ensuring quality). (6) Costs: "
            "ICC sets administrative costs and arbitrator fees using ad valorem scales based "
            "on the amount in dispute. (7) Multi-party: Provisions for joinder (Art. 7), "
            "consolidation (Art. 10), and multiple contracts (Art. 9). (8) Emergency "
            "Arbitrator (Art. 29): Available before tribunal constitution."
        ),
        related_topics=[
            "uncitral_arbitration_rules", "international_commercial_arbitration",
            "emergency_arbitrator", "arbitration_costs_fee_shifting",
        ],
        last_verified="2026-02-01",
    ),

    "icsid_convention": DoctrineCacheBlock(
        topic="ICSID Convention and Investment Arbitration",
        category="international_arbitration",
        authority_weight=0.93,
        citations=[
            "Convention on the Settlement of Investment Disputes (ICSID Convention, 1965)",
            "ICSID Rules of Procedure for Arbitration Proceedings (Arbitration Rules, 2022)",
            "ICSID Article 25 (Jurisdiction)",
            "ICSID Article 52 (Annulment)",
            "ICSID Article 54 (Enforcement)",
        ],
        content=(
            "The International Centre for Settlement of Investment Disputes (ICSID), "
            "established under the 1965 Washington Convention (part of the World Bank "
            "Group), provides the primary forum for investor-State dispute settlement "
            "(ISDS). Key features: (1) Jurisdiction (Art. 25): Requires consent of both "
            "the host State and the investor, a 'legal dispute' arising 'directly out of "
            "an investment,' and the investor must be a national of a Contracting State "
            "other than the host State. Consent is typically found in bilateral investment "
            "treaties (BITs), multilateral treaties (e.g., Energy Charter Treaty), or "
            "national investment laws. (2) Applicable law: Parties may choose applicable "
            "law; absent choice, the law of the host State and applicable rules of "
            "international law (Art. 42). (3) Award finality: ICSID awards are not subject "
            "to judicial review by national courts. The only recourse is ICSID annulment "
            "(Art. 52), available on five limited grounds: improper tribunal constitution, "
            "manifest excess of powers, corruption, serious departure from a fundamental "
            "rule of procedure, or failure to state reasons. (4) Enforcement (Art. 54): "
            "Each Contracting State must recognize an ICSID award as binding and enforce "
            "the pecuniary obligations as if it were a final judgment of its courts. This "
            "is more favorable than New York Convention enforcement. (5) ICSID Additional "
            "Facility: Available when one party is not an ICSID Contracting State. "
            "(6) 2022 Rule amendments: Expedited arbitration, third-party funding "
            "disclosure, security for costs."
        ),
        related_topics=[
            "investor_state_arbitration", "bilateral_investment_treaty",
            "new_york_convention_enforcement", "uncitral_arbitration_rules",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # NEW YORK CONVENTION & ENFORCEMENT
    # ======================================================================

    "new_york_convention_enforcement": DoctrineCacheBlock(
        topic="New York Convention - Recognition and Enforcement of Foreign Arbitral Awards",
        category="international_arbitration",
        authority_weight=0.96,
        citations=[
            "Convention on the Recognition and Enforcement of Foreign Arbitral Awards (1958)",
            "9 USC 201-208 (FAA Chapter 2)",
            "New York Convention Article V",
            "Scherk v Alberto-Culver Co, 417 US 506 (1974)",
        ],
        content=(
            "The 1958 New York Convention (NYC) is the cornerstone of international "
            "arbitration enforcement, ratified by 172 countries. It requires courts of "
            "Contracting States to recognize and enforce arbitral awards made in other "
            "Contracting States, subject to limited defenses. Article V provides exhaustive "
            "grounds for refusal of enforcement: (1) Article V(1)(a): Incapacity of parties "
            "or invalidity of the arbitration agreement under applicable law. (2) Article "
            "V(1)(b): Lack of proper notice of arbitrator appointment or proceedings, or "
            "inability to present one's case. (3) Article V(1)(c): Award deals with matters "
            "beyond the scope of the submission. (4) Article V(1)(d): Tribunal composition "
            "or procedure not in accordance with the agreement or the law of the seat. "
            "(5) Article V(1)(e): Award has not yet become binding, or has been set aside "
            "or suspended by a competent authority of the country in which it was made. "
            "(6) Article V(2)(a): Subject matter not arbitrable under the law of the "
            "enforcement country. (7) Article V(2)(b): Enforcement would be contrary to "
            "public policy of the enforcement country. The burden of proving a defense lies "
            "on the party resisting enforcement. Courts interpret the defenses narrowly to "
            "give effect to the Convention's pro-enforcement bias. In the US, the NYC is "
            "implemented through FAA Chapter 2 (9 USC 201-208)."
        ),
        related_topics=[
            "faa_scope_applicability", "icsid_convention",
            "award_enforcement_domestication", "panama_convention",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # MEDIATION
    # ======================================================================

    "mediation_uma": DoctrineCacheBlock(
        topic="Uniform Mediation Act (UMA)",
        category="mediation",
        authority_weight=0.87,
        citations=[
            "Uniform Mediation Act (2001, amended 2003)",
            "UMA Section 4 (Privilege Against Disclosure)",
            "UMA Section 6 (Exceptions to Privilege)",
            "UMA Section 8 (Confidentiality)",
        ],
        content=(
            "The Uniform Mediation Act (UMA), approved by the Uniform Law Commission in "
            "2001 and amended in 2003, establishes a comprehensive framework for mediation "
            "confidentiality and privilege. Adopted by 12 states and the District of "
            "Columbia. Key provisions: (1) Mediation privilege (Section 4): Mediation "
            "communications are privileged and may not be disclosed in subsequent judicial, "
            "administrative, or arbitral proceedings. The privilege belongs to the parties "
            "and the mediator. (2) Exceptions (Section 6): The privilege does not apply to "
            "signed mediated agreements, threats of bodily injury, attempts to plan or "
            "conceal a crime, communications sought in professional malpractice claims "
            "against a mediator or party's lawyer, and court orders in felony proceedings. "
            "(3) Waiver: All parties and the mediator must consent to waive the privilege; "
            "unilateral waiver is insufficient. (4) Mediator disclosure obligations: "
            "Mediators must disclose conflicts of interest before agreeing to mediate. "
            "(5) International mediation: The UMA references and is consistent with the "
            "UNCITRAL Model Law on International Commercial Mediation (2018). The UMA does "
            "not address mediator qualifications, certification, or ethical standards, "
            "leaving those to state bar rules and the Model Standards of Conduct for "
            "Mediators (jointly adopted by AAA, ABA, and ACR)."
        ),
        related_topics=[
            "mediation_confidentiality", "facilitative_mediation",
            "evaluative_mediation", "mediator_ethics_model_standards",
        ],
        last_verified="2026-02-01",
    ),

    "facilitative_mediation": DoctrineCacheBlock(
        topic="Facilitative Mediation",
        category="mediation",
        authority_weight=0.85,
        citations=[
            "Model Standards of Conduct for Mediators (AAA/ABA/ACR, 2005)",
            "Leonard Riskin, Understanding Mediators' Orientations (1996)",
            "Robert Baruch Bush & Joseph Folger, The Promise of Mediation (1994)",
        ],
        content=(
            "Facilitative mediation is the dominant mediation style in which the mediator "
            "assists the parties in reaching their own resolution without offering opinions "
            "on the merits, making recommendations, or predicting outcomes. Core principles: "
            "(1) Self-determination: The parties control the outcome; the mediator controls "
            "only the process. (2) Neutrality/impartiality: The mediator has no stake in "
            "the outcome and treats both parties equitably. (3) Process focus: The mediator "
            "uses questioning, reframing, reality testing, and active listening to help "
            "parties identify their interests (not just positions), generate options, and "
            "evaluate alternatives. (4) Caucuses: Private meetings with each party are a "
            "key tool; information shared in caucus is confidential unless the party "
            "authorizes disclosure. (5) Interest-based negotiation: The mediator guides "
            "parties from positional bargaining to interest-based problem solving, expanding "
            "the pie rather than dividing it. (6) No advisory role: Unlike evaluative "
            "mediation, the facilitative mediator does not assess the strengths and weaknesses "
            "of each side's case. (7) Agreement: If parties reach agreement, the mediator "
            "helps memorialize it in writing. The mediator does not provide legal advice. "
            "Facilitative mediation is most effective when parties have an ongoing "
            "relationship, creative solutions are possible, and parties are roughly equal "
            "in sophistication and bargaining power."
        ),
        related_topics=[
            "evaluative_mediation", "transformative_mediation",
            "mediation_uma", "negotiation_batna_watna_zopa",
        ],
        last_verified="2026-02-01",
    ),

    "evaluative_mediation": DoctrineCacheBlock(
        topic="Evaluative Mediation",
        category="mediation",
        authority_weight=0.85,
        citations=[
            "Leonard Riskin, Understanding Mediators' Orientations (1996)",
            "Lela Love, The Top Ten Reasons Why Mediators Should Not Evaluate (1997)",
            "Model Standards of Conduct for Mediators Standard VI (Quality of the Process)",
        ],
        content=(
            "Evaluative mediation involves a mediator who provides opinions on the merits, "
            "assesses the strengths and weaknesses of each party's case, predicts likely "
            "outcomes at trial, and may recommend settlement terms. Key characteristics: "
            "(1) Subject-matter expertise: Evaluative mediators are typically experienced "
            "lawyers or retired judges with expertise in the relevant area of law. (2) "
            "Case assessment: The mediator may opine on liability, damages, evidentiary "
            "issues, and procedural risks. This helps parties make informed decisions. (3) "
            "Mediator's proposal: A specific technique where the mediator proposes a "
            "settlement number after hearing both sides; each party privately accepts or "
            "rejects; if both accept, the case settles at that number; if not, neither "
            "party knows the other's response. (4) Bracketing: The mediator helps narrow "
            "the range by proposing brackets (e.g., 'Would plaintiff accept between $X-$Y? "
            "Would defendant pay between $A-$B?'). (5) Controversy: Critics argue evaluative "
            "mediation undermines party self-determination and mediator neutrality. Proponents "
            "argue it is efficient and particularly effective in litigated cases where parties "
            "need a reality check on their positions. (6) Court-annexed programs often use "
            "evaluative mediation with retired judges, especially in personal injury, "
            "commercial litigation, and employment cases."
        ),
        related_topics=[
            "facilitative_mediation", "court_annexed_adr",
            "early_neutral_evaluation", "mediation_uma",
        ],
        last_verified="2026-02-01",
    ),

    "transformative_mediation": DoctrineCacheBlock(
        topic="Transformative Mediation",
        category="mediation",
        authority_weight=0.82,
        citations=[
            "Robert Baruch Bush & Joseph Folger, The Promise of Mediation (1994, rev. 2005)",
            "USPS REDRESS Program (Transformative Mediation Model)",
        ],
        content=(
            "Transformative mediation, developed by Bush and Folger, focuses on transforming "
            "the interaction between parties rather than solving a specific problem. The two "
            "central goals are empowerment (helping each party gain clarity about their "
            "situation, options, preferences, and resources) and recognition (helping each "
            "party voluntarily choose to acknowledge and understand the other party's "
            "perspective). Key features: (1) No agenda-setting by mediator: The parties "
            "control what is discussed and in what order. (2) No directive intervention: "
            "The mediator follows the parties' conversation, reflecting and summarizing, "
            "but never steering toward agreement. (3) Conflict as opportunity: Conflict "
            "is seen as a crisis in human interaction that presents an opportunity for "
            "moral growth in both empowerment and recognition. (4) Agreement is not the "
            "goal: Settlement may or may not result; what matters is the quality of the "
            "interaction. (5) The US Postal Service's REDRESS program is the largest "
            "implementation of transformative mediation, handling thousands of EEO disputes "
            "annually with reported satisfaction rates above 90 percent. (6) Best suited for "
            "disputes with ongoing relationships (workplace, community, family) where "
            "addressing relational dynamics is as important as resolving the substantive "
            "issue. Not typically used in complex commercial or multi-party disputes."
        ),
        related_topics=[
            "facilitative_mediation", "evaluative_mediation",
            "mediation_uma", "workplace_mediation",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # COURT-ANNEXED ADR
    # ======================================================================

    "court_annexed_adr": DoctrineCacheBlock(
        topic="Court-Annexed ADR Programs",
        category="court_annexed",
        authority_weight=0.86,
        citations=[
            "Alternative Dispute Resolution Act of 1998 (28 USC 651-658)",
            "FRCP Rule 16(a)(5) (Pretrial Conference - Facilitating Settlement)",
            "Tex. Civ. Prac. & Rem. Code 154.021 (Referral of Pending Disputes)",
        ],
        content=(
            "The Alternative Dispute Resolution Act of 1998 (28 USC 651-658) requires "
            "every federal district court to authorize and implement an ADR program. Courts "
            "may mandate participation in at least one ADR process (mediation, early neutral "
            "evaluation, mini-trial, or summary jury trial). Key programs: (1) Mandatory "
            "mediation: Most common; courts order parties to mediate before trial. The "
            "parties must participate in good faith but are not required to settle. Failure "
            "to participate can result in sanctions. (2) Early Neutral Evaluation (ENE): A "
            "neutral evaluator (often a lawyer) hears abbreviated presentations from both "
            "sides early in the case and provides a non-binding assessment of the strengths "
            "and weaknesses of each party's position and the likely outcome. (3) Mini-trial: "
            "Abbreviated presentation to a panel of senior executives from each side plus a "
            "neutral advisor; executives then negotiate. (4) Summary jury trial: An "
            "abbreviated trial before an advisory jury whose non-binding verdict is used "
            "to facilitate settlement. (5) Texas: CPRC Section 154.021 allows any court to "
            "refer a pending dispute to ADR on its own motion or by agreement. Texas courts "
            "frequently order mediation in civil cases, especially family law, personal "
            "injury, and commercial disputes."
        ),
        related_topics=[
            "evaluative_mediation", "early_neutral_evaluation",
            "texas_adr_act_cprc_154", "mini_trial_summary_jury",
        ],
        last_verified="2026-02-01",
    ),

    "early_neutral_evaluation": DoctrineCacheBlock(
        topic="Early Neutral Evaluation (ENE)",
        category="court_annexed",
        authority_weight=0.82,
        citations=[
            "28 USC 652(a) (District Court ADR Programs)",
            "Northern District of California ADR Local Rule 6 (ENE Program)",
            "Wayne Brazil, Early Neutral Evaluation (1990)",
        ],
        content=(
            "Early Neutral Evaluation (ENE) is a court-annexed ADR process in which a "
            "neutral evaluator (typically a senior attorney or retired judge) meets with "
            "the parties and counsel early in the litigation to provide a non-binding "
            "assessment of the case. Process: (1) Timing: Usually within 150 days of "
            "filing, before significant discovery. (2) Session: Each side makes a brief "
            "presentation (typically 15-30 minutes). The evaluator may ask questions. (3) "
            "Assessment: The evaluator provides a confidential, oral assessment of the "
            "strengths and weaknesses of each party's claims and defenses, the probable "
            "range of damages, and the likely outcome at trial. (4) Settlement: If parties "
            "are interested, the evaluator facilitates settlement discussion. (5) Case "
            "management: If no settlement, the evaluator helps the parties develop a "
            "discovery plan and identify key issues. (6) Confidentiality: ENE sessions "
            "are confidential; the evaluator's assessment cannot be used as evidence. "
            "The Northern District of California pioneered ENE in the 1980s and continues "
            "one of the most active programs. Studies show ENE reduces discovery costs and "
            "accelerates resolution in cases where parties have realistic expectations."
        ),
        related_topics=[
            "court_annexed_adr", "evaluative_mediation",
            "mini_trial_summary_jury", "case_management_conference",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # NEGOTIATION THEORY
    # ======================================================================

    "negotiation_batna_watna_zopa": DoctrineCacheBlock(
        topic="Negotiation Theory - BATNA, WATNA, ZOPA",
        category="negotiation",
        authority_weight=0.88,
        citations=[
            "Roger Fisher & William Ury, Getting to Yes (1981, 3d ed. 2011)",
            "Howard Raiffa, The Art and Science of Negotiation (1982)",
            "Robert Mnookin et al., Beyond Winning (2000)",
        ],
        content=(
            "Core negotiation concepts essential to ADR practice: (1) BATNA (Best "
            "Alternative to a Negotiated Agreement): The most advantageous course of "
            "action a party can take if negotiations fail. In litigation context, BATNA "
            "is the expected trial outcome discounted by litigation costs, risk, and delay. "
            "A strong BATNA increases bargaining power. (2) WATNA (Worst Alternative to a "
            "Negotiated Agreement): The worst-case scenario if negotiations fail. Helps "
            "parties recognize the risks of impasse. (3) ZOPA (Zone of Possible Agreement): "
            "The range between each party's reservation point (walkaway price) where a deal "
            "is possible. If plaintiff's minimum acceptable settlement is less than "
            "defendant's maximum willingness to pay, a ZOPA exists. (4) Reservation point "
            "(bottom line): The point at which a party is indifferent between settling and "
            "pursuing the BATNA. (5) Aspiration point: The ideal outcome a party hopes to "
            "achieve. (6) Distributive negotiation: Zero-sum bargaining over a fixed pie. "
            "(7) Integrative negotiation: Expanding the pie by identifying complementary "
            "interests and creating value. (8) Principled negotiation (Fisher & Ury): "
            "Separate people from the problem, focus on interests not positions, generate "
            "options for mutual gain, insist on objective criteria. Mediators and "
            "arbitrators use these frameworks to reality-test parties' expectations."
        ),
        related_topics=[
            "facilitative_mediation", "evaluative_mediation",
            "mediation_uma", "settlement_negotiation",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # ONLINE DISPUTE RESOLUTION (ODR)
    # ======================================================================

    "online_dispute_resolution": DoctrineCacheBlock(
        topic="Online Dispute Resolution (ODR)",
        category="odr",
        authority_weight=0.83,
        citations=[
            "ICANN Uniform Domain-Name Dispute-Resolution Policy (UDRP, 1999)",
            "EU Regulation 524/2013 (Online Dispute Resolution for Consumer Disputes)",
            "UNCITRAL Technical Notes on Online Dispute Resolution (2016)",
            "Ethan Katsh & Janet Rifkin, Online Dispute Resolution (2001)",
        ],
        content=(
            "Online Dispute Resolution (ODR) encompasses ADR processes conducted partially "
            "or entirely online. Key systems and developments: (1) UDRP (Uniform Domain-Name "
            "Dispute-Resolution Policy): Administered by ICANN-approved providers (WIPO, "
            "NAF, ADR.eu). Covers cybersquatting disputes. Complainant must prove: (a) "
            "domain name is identical/confusingly similar to a trademark, (b) registrant "
            "has no rights/legitimate interests, (c) domain registered and used in bad "
            "faith. Panel decision within 14 days; remedies are transfer or cancellation. "
            "(2) EU ODR Platform: Regulation 524/2013 created a platform for cross-border "
            "consumer disputes. Online traders must link to the platform on their websites. "
            "(3) eBay Resolution Center: Processes millions of buyer-seller disputes annually "
            "using automated negotiation and human mediators. One of the largest ODR systems. "
            "(4) E-arbitration: Traditional arbitration conducted via video conference, "
            "electronic document submission, and online case management platforms. Accelerated "
            "by COVID-19. (5) AI-assisted ODR: Emerging platforms use artificial intelligence "
            "to propose settlement ranges based on case data. (6) Blockchain-based arbitration: "
            "Smart contract disputes resolved through decentralized arbitration (Kleros, "
            "Aragon Court). Still experimental. (7) Virtual hearing protocols: Major "
            "institutions (AAA, ICC, LCIA) all adopted remote hearing guidelines."
        ),
        related_topics=[
            "udrp_domain_disputes", "consumer_arbitration",
            "technology_in_arbitration", "virtual_hearing_protocols",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # HYBRID PROCESSES
    # ======================================================================

    "med_arb_hybrid": DoctrineCacheBlock(
        topic="Med-Arb and Arb-Med Hybrid Processes",
        category="hybrid_processes",
        authority_weight=0.84,
        citations=[
            "Bowden v Weickert, 903 NE 2d 628 (Ohio App. 2008)",
            "Gaskin v AIMCO/Blvd Mgmt, 173 P3d 1191 (Haw. App. 2007)",
            "Barry C. Bartel, Med-Arb as a Distinct Method of Dispute Resolution (1991)",
        ],
        content=(
            "Med-Arb and Arb-Med are hybrid ADR processes combining mediation and "
            "arbitration. (1) Med-Arb: Begins with mediation; if mediation fails to "
            "resolve all issues, the process converts to arbitration. The same neutral "
            "may serve as both mediator and arbitrator, or the roles may be split between "
            "different neutrals. Advantages: efficiency, single neutral, parties have "
            "incentive to settle knowing arbitration follows. Disadvantages: confidentiality "
            "concerns (mediator heard private caucus information that may influence arbitral "
            "decision); due process objections (party may not fully disclose in mediation "
            "knowing the neutral will decide). Some courts have upheld med-arb awards; "
            "others have vacated on due process grounds. Best practice: use separate "
            "neutrals (med-then-arb) or 'sealed envelope' technique where mediator obtains "
            "each party's bottom line in sealed envelopes, and if they overlap, settlement "
            "is announced. (2) Arb-Med: Begins with arbitration; the arbitrator makes a "
            "decision and seals it; parties then mediate; if mediation succeeds, the sealed "
            "award is destroyed; if mediation fails, the sealed award is opened. Advantages: "
            "parties negotiate in the shadow of an actual decision; eliminates caucus "
            "information contamination. Disadvantages: full arbitration costs regardless "
            "of outcome. (3) Dispute Review Boards (DRBs): Standing panels on construction "
            "projects that provide real-time advisory opinions on disputes as they arise."
        ),
        related_topics=[
            "facilitative_mediation", "aaa_commercial_rules",
            "arbitration_clause_drafting", "construction_arbitration",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # CLASS ACTION ARBITRATION
    # ======================================================================

    "class_action_arbitration": DoctrineCacheBlock(
        topic="Class and Collective Action Arbitration",
        category="class_arbitration",
        authority_weight=0.96,
        citations=[
            "Stolt-Nielsen SA v AnimalFeeds Int'l, 559 US 662 (2010)",
            "AT&T Mobility v Concepcion, 563 US 333 (2011)",
            "Epic Systems Corp v Lewis, 584 US 497 (2018)",
            "Lamps Plus v Varela, 587 US 176 (2019)",
            "Viking River Cruises v Moriana, 596 US 639 (2022)",
        ],
        content=(
            "Class action arbitration is one of the most contested areas of arbitration law. "
            "Key developments: (1) Stolt-Nielsen v AnimalFeeds (2010): An arbitral tribunal "
            "cannot impose class procedures on parties whose arbitration agreement is silent "
            "on class arbitration. Silence does not equal consent. (2) AT&T v Concepcion "
            "(2011): The FAA preempts state-law rules that condition the enforceability of "
            "arbitration agreements on the availability of class procedures. California's "
            "Discover Bank rule was preempted. (3) American Express v Italian Colors "
            "Restaurant (2013): A class waiver is enforceable even if the cost of "
            "individually arbitrating a federal statutory claim exceeds the potential "
            "recovery ('effective vindication' doctrine does not require class proceedings). "
            "(4) Epic Systems v Lewis (2018): The FAA and NLRA do not conflict; employers "
            "can enforce arbitration agreements with class/collective action waivers against "
            "employees. The NLRA's Section 7 right to 'concerted activity' does not include "
            "a right to class or collective litigation. (5) Lamps Plus v Varela (2019): "
            "Ambiguous arbitration agreements cannot be construed to authorize class "
            "arbitration. (6) Viking River Cruises v Moriana (2022): The FAA preempts "
            "California's Iskanian rule; representative PAGA claims can be split — "
            "individual PAGA claims go to arbitration, and the plaintiff may lack standing "
            "to pursue non-individual PAGA claims (though California courts have since "
            "pushed back on the standing issue in Adolph v Uber)."
        ),
        related_topics=[
            "faa_preemption", "unconscionability_defense",
            "employment_arbitration", "consumer_arbitration",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # ARBITRABILITY & DELEGATION
    # ======================================================================

    "arbitrability_substantive": DoctrineCacheBlock(
        topic="Substantive Arbitrability",
        category="arbitrability",
        authority_weight=0.93,
        citations=[
            "Rent-A-Center West v Jackson, 561 US 63 (2010)",
            "Henry Schein Inc v Archer & White Sales, 586 US 63 (2019)",
            "First Options of Chicago v Kaplan, 514 US 938 (1995)",
            "Howsam v Dean Witter Reynolds, 537 US 79 (2002)",
        ],
        content=(
            "Substantive arbitrability refers to whether a particular dispute is subject to "
            "arbitration under the parties' agreement. This is a 'gateway question' "
            "presumptively for the court unless the parties clearly and unmistakably "
            "delegate it to the arbitrator. (1) Court decides: Whether a valid arbitration "
            "agreement exists between the parties; whether the dispute falls within the "
            "scope of the agreement. (2) Delegation clauses: If the arbitration agreement "
            "clearly and unmistakably delegates arbitrability questions to the arbitrator "
            "(e.g., by incorporating institutional rules that grant the arbitrator "
            "jurisdiction to determine jurisdiction), the court defers. In Rent-A-Center "
            "v Jackson (2010), the Court held that a delegation clause is severable from "
            "the broader arbitration agreement and enforceable unless the delegation clause "
            "itself is challenged as unconscionable. (3) Henry Schein v Archer & White "
            "(2019): The Court rejected the 'wholly groundless' exception — if a valid "
            "delegation clause exists, the court must send the arbitrability question to "
            "the arbitrator even if the argument for arbitrability is wholly groundless. "
            "(4) Procedural arbitrability (e.g., timeliness, conditions precedent, "
            "satisfaction of contractual prerequisites) is presumptively for the "
            "arbitrator, not the court (Howsam v Dean Witter, 2002)."
        ),
        related_topics=[
            "delegation_clause", "separability_doctrine",
            "kompetenz_kompetenz", "faa_section_4_compel",
        ],
        last_verified="2026-02-01",
    ),

    "separability_doctrine": DoctrineCacheBlock(
        topic="Separability Doctrine (Prima Paint)",
        category="arbitrability",
        authority_weight=0.92,
        citations=[
            "Prima Paint Corp v Flood & Conklin Mfg, 388 US 395 (1967)",
            "Buckeye Check Cashing v Cardegna, 546 US 440 (2006)",
            "Rent-A-Center West v Jackson, 561 US 63 (2010)",
        ],
        content=(
            "The separability doctrine holds that an arbitration clause within a contract "
            "is a separate and independent agreement from the underlying contract. "
            "Established by Prima Paint Corp v Flood & Conklin (1967), the doctrine means: "
            "(1) A challenge to the validity of the contract as a whole (e.g., fraud in the "
            "inducement, illegality, impossibility) does not reach the arbitration clause. "
            "Such challenges must be resolved by the arbitrator. (2) Only challenges "
            "directed specifically at the making or validity of the arbitration clause "
            "itself are for the court. (3) In Buckeye Check Cashing v Cardegna (2006), the "
            "Court applied separability to hold that a challenge to a loan contract as "
            "void ab initio for usury was for the arbitrator, not the court, because the "
            "challenge was to the contract generally, not the arbitration clause. (4) In "
            "Rent-A-Center v Jackson (2010), the Court extended separability to delegation "
            "clauses within the arbitration clause itself — if a party challenges the "
            "arbitration clause as unconscionable but does not specifically challenge the "
            "delegation provision, the delegation clause is enforced. The practical effect "
            "is that most challenges to contracts containing arbitration clauses will be "
            "sent to arbitration, reinforcing the FAA's pro-arbitration policy."
        ),
        related_topics=[
            "arbitrability_substantive", "delegation_clause",
            "unconscionability_defense", "faa_section_2_savings_clause",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # ARBITRATION CLAUSE DRAFTING
    # ======================================================================

    "arbitration_clause_drafting": DoctrineCacheBlock(
        topic="Arbitration Clause Drafting",
        category="clause_drafting",
        authority_weight=0.90,
        citations=[
            "AAA Drafting Dispute Resolution Clauses: A Practical Guide",
            "ICC Arbitration Clause for Contracts",
            "Gary Born, International Commercial Arbitration, Ch. 4 (3d ed. 2021)",
        ],
        content=(
            "Effective arbitration clause drafting requires attention to multiple elements "
            "to avoid pathological clauses and ensure enforceability. Essential elements: "
            "(1) Scope: 'Any dispute, controversy, or claim arising out of or relating to "
            "this agreement, including the breach, termination, or validity thereof' — broad "
            "language is preferred. Narrow clauses (e.g., 'disputes under this agreement') "
            "may exclude tort and statutory claims. (2) Institution/rules: Designate the "
            "administering institution and applicable rules (e.g., 'shall be settled by "
            "arbitration administered by the AAA under its Commercial Arbitration Rules'). "
            "(3) Number of arbitrators: Specify one or three. For smaller disputes ($<500K), "
            "one arbitrator is efficient. For larger disputes, three provides diversity. (4) "
            "Seat/place: Critical because the seat determines the procedural law of the "
            "arbitration, the supervisory court, and the enforceability framework. (5) "
            "Governing law: Distinguish between the substantive law governing the contract, "
            "the law governing the arbitration agreement, and the procedural law of the "
            "arbitration. (6) Language: For international arbitrations, specify the language "
            "of proceedings. (7) Qualifications of arbitrators: May require industry "
            "expertise, licensing, or language ability. (8) Discovery/disclosure: Consider "
            "limiting or expanding default institutional rules. (9) Confidentiality clause: "
            "Institutional rules vary on confidentiality; an express provision is advisable. "
            "(10) Interim relief: Preserve the right to seek court-ordered interim relief "
            "without waiving arbitration. (11) Appeal mechanism: AAA Optional Appellate "
            "Arbitration Rules available since 2013."
        ),
        related_topics=[
            "pathological_clauses", "aaa_commercial_rules",
            "icc_arbitration_rules", "arbitration_costs_fee_shifting",
        ],
        last_verified="2026-02-01",
    ),

    "pathological_clauses": DoctrineCacheBlock(
        topic="Pathological Arbitration Clauses",
        category="clause_drafting",
        authority_weight=0.87,
        citations=[
            "Frédéric Eisemann, La clause d'arbitrage pathologique (1974)",
            "Lucky-Goldstar Int'l v Ng Moo Kee Engineering, [1993] 1 HKC 404",
            "Insigma Technology v Alstom Technology, [2009] SGCA 24",
        ],
        content=(
            "Pathological arbitration clauses are defectively drafted clauses that create "
            "uncertainty about the arbitration process. Common pathologies: (1) Naming a "
            "non-existent institution: 'Arbitration shall be conducted by the International "
            "Court of Arbitration in New York' (no such institution exists by that name in "
            "NYC). Courts may interpret this to refer to the ICC International Court of "
            "Arbitration or AAA. (2) Contradictory provisions: 'Disputes shall be finally "
            "resolved by arbitration... Either party may appeal to the courts.' The finality "
            "of arbitration conflicts with the appeal right. (3) Optional arbitration: 'Any "
            "dispute may be submitted to arbitration.' Courts split on whether this creates "
            "a mandatory obligation. (4) Hybrid references: 'Arbitration under ICC Rules "
            "administered by AAA.' Which institution controls? (5) Incomplete provisions: "
            "Specifying arbitration but omitting rules, institution, seat, and method of "
            "appointment. (6) Unilateral options: 'Party A may elect arbitration.' One-sided "
            "option clauses face enforceability challenges in some jurisdictions. (7) "
            "Escalation clause failure: Multi-tier clauses requiring negotiation then "
            "mediation then arbitration, but failing to specify timelines or making "
            "earlier steps 'conditions precedent' without clear triggers. Best practice: "
            "Use the recommended model clause of the chosen institution verbatim."
        ),
        related_topics=[
            "arbitration_clause_drafting", "arbitrability_substantive",
            "faa_section_4_compel", "multi_tier_dispute_resolution",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # JUDICIAL REVIEW - MANIFEST DISREGARD & EVIDENT PARTIALITY
    # ======================================================================

    "manifest_disregard": DoctrineCacheBlock(
        topic="Manifest Disregard of the Law",
        category="judicial_review",
        authority_weight=0.90,
        citations=[
            "Hall Street Associates v Mattel, 552 US 576 (2008)",
            "Wilko v Swan, 346 US 427 (1953) (overruled on other grounds)",
            "Stolt-Nielsen SA v AnimalFeeds Int'l, 559 US 662 (2010)",
            "Citigroup Global Markets v Bacon, 562 F.3d 349 (5th Cir. 2009)",
        ],
        content=(
            "Manifest disregard of the law is a judicially created ground for vacating "
            "arbitration awards that originated in dictum in Wilko v Swan (1953). After "
            "Hall Street v Mattel (2008) held that the FAA Section 10 grounds are "
            "exclusive, circuits split on whether manifest disregard survived: (1) "
            "Second Circuit: Survived as a 'judicial gloss' on Section 10(a)(4) (excess "
            "of powers). (2) Fifth Circuit: Abandoned as an independent ground after Hall "
            "Street. (3) Seventh and Eleventh Circuits: Manifest disregard may survive as "
            "a shorthand for Section 10(a)(4). (4) To establish manifest disregard, the "
            "moving party must show: (a) the law that was allegedly disregarded was clear, "
            "well-defined, and not subject to reasonable debate; (b) the arbitrator knew of "
            "the governing legal principle and refused to apply it or ignored it; and (c) "
            "the arbitrator's refusal or ignorance was conscious and deliberate. (5) The "
            "standard is extremely difficult to meet because arbitrators need not explain "
            "their reasoning (unless a reasoned award is requested), and courts are not "
            "permitted to review the merits or second-guess factual findings. (6) Practical "
            "significance has diminished post-Hall Street, but it remains relevant in "
            "circuits that recognize it, particularly for statutory claims where the "
            "applicable law is clear."
        ),
        related_topics=[
            "faa_section_10_vacatur", "evident_partiality",
            "faa_section_9_confirmation", "arbitrator_reasoned_awards",
        ],
        last_verified="2026-02-01",
    ),

    "evident_partiality": DoctrineCacheBlock(
        topic="Evident Partiality - Arbitrator Disclosure",
        category="judicial_review",
        authority_weight=0.91,
        citations=[
            "9 USC 10(a)(2)",
            "Commonwealth Coatings Corp v Continental Casualty, 393 US 145 (1968)",
            "Morelite Construction v NY City District Council, 748 F.2d 79 (2d Cir. 1984)",
            "Positive Software Solutions v New Century Mortgage, 476 F.3d 278 (5th Cir. 2007)",
            "IBA Guidelines on Conflicts of Interest in International Arbitration (2014)",
        ],
        content=(
            "Evident partiality under FAA Section 10(a)(2) is a ground for vacating an "
            "arbitration award. The standard is debated among circuits: (1) Appearance "
            "standard (broader): Some circuits hold that an award must be vacated if a "
            "reasonable person would have to conclude that an arbitrator was partial, based "
            "on the arbitrator's failure to disclose relationships that might create an "
            "impression of possible bias (Commonwealth Coatings plurality, 1968). (2) "
            "Actual bias standard (narrower): Other circuits require proof of actual bias "
            "or a concrete, direct relationship that necessarily shows partiality. (3) "
            "Fifth Circuit approach (Positive Software, 2007): Requires a showing of a "
            "significant compromising relationship between the arbitrator and a party that "
            "is 'direct, definite, and capable of demonstration.' (4) Disclosure "
            "obligations: Arbitrators have a continuing duty to disclose relationships and "
            "interests that might create an appearance of bias. AAA/ABA Code of Ethics "
            "Canon II requires disclosure. IBA Guidelines provide Red/Orange/Green lists "
            "categorizing types of relationships by severity. (5) Non-disclosure alone is "
            "insufficient; the undisclosed relationship must be significant enough to "
            "create evident partiality. (6) Repeat appointments by the same law firm or "
            "party are a common source of challenges."
        ),
        related_topics=[
            "faa_section_10_vacatur", "manifest_disregard",
            "arbitrator_disclosure", "arbitrator_selection",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # DISCOVERY IN ARBITRATION
    # ======================================================================

    "arbitration_discovery": DoctrineCacheBlock(
        topic="Discovery in Arbitration",
        category="arbitration_procedure",
        authority_weight=0.88,
        citations=[
            "9 USC 7 (FAA - Arbitrator Subpoena Power)",
            "Hay Group v E.B.S. Acquisition Corp, 360 F.3d 404 (3d Cir. 2004)",
            "Life Receivables Trust v Syndicate 102, 549 F.3d 210 (2d Cir. 2008)",
            "NBCU v Heckes, No. 22-cv-2581 (SDNY 2023)",
        ],
        content=(
            "Discovery in arbitration is more limited than in litigation, but its scope "
            "varies by institutional rules and arbitrator discretion. (1) FAA Section 7: "
            "Authorizes arbitrators to summon witnesses and documents to appear at the "
            "hearing. There is a circuit split on pre-hearing discovery: Third Circuit "
            "(Hay Group, 2004) held that Section 7 does not authorize pre-hearing document "
            "subpoenas to non-parties; subpoenas are limited to appearance at the hearing. "
            "Fourth Circuit and some others permit pre-hearing document subpoenas under "
            "Section 7. (2) Party discovery: Arbitrators have broad discretion to order "
            "discovery between the parties, including document exchange, interrogatories, "
            "and depositions. AAA Rule R-21 and JAMS Rule 16 provide frameworks. (3) "
            "Third-party discovery: More limited; depends on whether FAA Section 7 permits "
            "pre-hearing subpoenas. (4) IBA Rules on the Taking of Evidence: Widely used "
            "in international arbitration; provide a structured framework for document "
            "production (Redfern Schedule), witness statements, expert reports, and "
            "inspections. (5) E-discovery: Arbitrators increasingly address ESI issues; "
            "some apply proportionality principles from FRCP 26(b)(1). (6) Practical "
            "approach: Most arbitrators allow reasonable document exchange but limit "
            "depositions; some permit depositions for key witnesses or where a witness "
            "may be unavailable at the hearing."
        ),
        related_topics=[
            "aaa_commercial_rules", "jams_comprehensive_rules",
            "iba_evidence_rules", "arbitrator_powers",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # EMERGENCY ARBITRATOR
    # ======================================================================

    "emergency_arbitrator": DoctrineCacheBlock(
        topic="Emergency Arbitrator Provisions",
        category="arbitration_procedure",
        authority_weight=0.87,
        citations=[
            "AAA Optional Rules for Emergency Measures of Protection (2013)",
            "ICC Article 29 and Appendix V (Emergency Arbitrator)",
            "ICDR Article 6 (Emergency Measures of Protection)",
            "SCC Emergency Arbitrator Provisions",
            "Yahoo! v Microsoft Corp (ICDR Emergency Award, 2013)",
        ],
        content=(
            "Emergency arbitrator provisions allow parties to obtain urgent interim relief "
            "before the full arbitral tribunal is constituted. Most major institutions now "
            "offer emergency arbitrator procedures: (1) ICC (Art. 29): Application filed "
            "before or concurrently with the Request for Arbitration. Emergency arbitrator "
            "appointed within 2 days. Decision within 15 days. Available since 2012. (2) "
            "AAA/ICDR (Art. 6): Emergency arbitrator appointed within 1 business day. "
            "Order issued within days. (3) SIAC (Rule 30): Emergency arbitrator appointed "
            "within 1 business day. Reasoned order within 14 days. (4) Available relief: "
            "Interim injunctions, asset freezing orders, preservation of evidence, security "
            "for costs, anti-suit injunctions. (5) Standard: Generally requires: (a) "
            "urgency (relief needed before tribunal constitution); (b) irreparable harm; "
            "(c) reasonable possibility of success on the merits; (d) proportionality. "
            "(6) Enforcement: Emergency arbitrator orders are not 'awards' under the New "
            "York Convention, making cross-border enforcement uncertain. Some jurisdictions "
            "have amended their arbitration laws to provide for enforcement (Singapore, "
            "Hong Kong). In the US, enforcement depends on whether the court treats the "
            "order as a preliminary injunction or an arbitral award. (7) Parties may also "
            "seek interim relief directly from courts without waiving arbitration."
        ),
        related_topics=[
            "interim_measures_arbitration", "icc_arbitration_rules",
            "aaa_commercial_rules", "new_york_convention_enforcement",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # MULTI-PARTY ARBITRATION
    # ======================================================================

    "multi_party_arbitration": DoctrineCacheBlock(
        topic="Multi-Party Arbitration",
        category="arbitration_procedure",
        authority_weight=0.86,
        citations=[
            "ICC Article 7 (Joinder of Additional Parties)",
            "ICC Article 10 (Consolidation of Arbitrations)",
            "AAA Consolidation Procedures (R-8)",
            "Dutco Construction v BKMI/Siemens (Cour de cassation, 1992)",
        ],
        content=(
            "Multi-party arbitration arises when disputes involve more than two parties "
            "or multiple related contracts. Key issues: (1) Joinder: Adding a non-signatory "
            "or additional party to pending arbitration. ICC Art. 7 permits joinder if the "
            "additional party is bound by the arbitration agreement. Timing matters: joinder "
            "after tribunal constitution requires all parties' agreement. (2) Consolidation: "
            "Combining separate arbitrations into a single proceeding. ICC Art. 10 allows "
            "consolidation when all claims are made under the same arbitration agreement, "
            "or compatible agreements between the same parties, or the Court finds it "
            "expedient. AAA Rule R-8 allows consolidation by agreement or administrator "
            "decision. (3) Parallel proceedings: When parties are bound by different "
            "arbitration agreements (e.g., main contract and subcontract), parallel "
            "arbitrations may proceed simultaneously, risking inconsistent results. (4) "
            "Tribunal constitution in multi-party cases: The Dutco principle (French Cour "
            "de cassation, 1992) requires equal treatment — all parties must have equal "
            "participation in arbitrator selection. If multiple claimants or respondents "
            "cannot agree on a joint nomination, the institution appoints all arbitrators. "
            "(5) Construction disputes are the most common multi-party context (owner, "
            "contractor, subcontractors, architects, engineers). (6) Third-party funding: "
            "Increasingly common; disclosure of funding arrangements may be required."
        ),
        related_topics=[
            "consolidation_joinder", "construction_arbitration",
            "icc_arbitration_rules", "aaa_construction_rules",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # TEXAS ADR ACT
    # ======================================================================

    "texas_adr_act_cprc_154": DoctrineCacheBlock(
        topic="Texas ADR Act - CPRC Chapter 154",
        category="texas_adr",
        authority_weight=0.90,
        citations=[
            "Tex. Civ. Prac. & Rem. Code Ch. 154 (ADR Procedures)",
            "Tex. Civ. Prac. & Rem. Code Ch. 171 (General Arbitration Act)",
            "In re Weekley Homes, 180 SW3d 127 (Tex. 2005)",
            "Forest Oil Corp v McAllen, 268 SW3d 51 (Tex. 2008)",
        ],
        content=(
            "Texas has comprehensive ADR legislation. CPRC Chapter 154 (ADR Procedures): "
            "(1) Section 154.021: Courts may refer a pending dispute to ADR on the court's "
            "own motion or the motion of a party. (2) Section 154.023: ADR procedures "
            "include mediation, mini-trial, moderated settlement conference, summary jury "
            "trial, and arbitration (non-binding unless parties agree otherwise). (3) "
            "Section 154.053: Confidentiality — communications in ADR are confidential and "
            "may not be used as evidence. (4) Section 154.054: Impartial third parties must "
            "disclose potential conflicts. (5) Section 154.071: Settlement agreements "
            "reached through ADR are enforceable as contracts. If signed by the parties "
            "and their attorneys, the agreement is enforceable as a judgment of the court. "
            "CPRC Chapter 171 (Texas General Arbitration Act): Applies to arbitration "
            "agreements not governed by the FAA. Largely tracks the original UAA (not RUAA). "
            "Vacatur grounds (Section 171.088) mirror FAA Section 10. In re Weekley Homes "
            "(2005): Discovery in arbitration is limited; mandamus is available if an "
            "arbitrator exceeds authority in ordering discovery. Forest Oil v McAllen (2008): "
            "Non-signatories may be compelled to arbitrate under theories of incorporation "
            "by reference, agency, alter ego, or direct-benefits estoppel. Texas is generally "
            "pro-arbitration in its jurisprudence."
        ),
        related_topics=[
            "faa_scope_applicability", "court_annexed_adr",
            "mediation_confidentiality", "ruaa_overview",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # SECURITIES ARBITRATION
    # ======================================================================

    "securities_arbitration_finra": DoctrineCacheBlock(
        topic="Securities Arbitration - Mandatory FINRA",
        category="securities_arbitration",
        authority_weight=0.92,
        citations=[
            "Shearson/American Express v McMahon, 482 US 220 (1987)",
            "Rodriguez de Quijas v Shearson/American Express, 490 US 477 (1989)",
            "FINRA Regulatory Notice 16-25 (Discovery Improvements)",
            "SEC Rule 15c2-2 (Rescission of Blanket Anti-Arbitration Provisions, repealed 1999)",
        ],
        content=(
            "Securities arbitration is effectively mandatory for most customer-broker "
            "disputes. Legal framework: (1) McMahon (1987) held that claims under the "
            "Securities Exchange Act of 1934 (Section 10(b), Rule 10b-5) are arbitrable. "
            "(2) Rodriguez de Quijas (1989) overruled Wilko v Swan and held Securities Act "
            "of 1933 claims are also arbitrable. (3) FINRA Rule 12200: Customer can compel "
            "member firm to arbitrate if there is a written agreement or if the dispute "
            "arises in connection with the business activities of the member or associated "
            "person. (4) Common claims: Suitability (FINRA Rule 2111), churning (excessive "
            "trading), unauthorized trading, misrepresentation/omission (fraud), breach of "
            "fiduciary duty, elder financial exploitation, failure to supervise. (5) Damages: "
            "Compensatory damages (market-adjusted or well-managed portfolio), lost "
            "opportunity costs, interest, punitive damages (available but rare), costs "
            "and attorneys' fees. (6) Challenges: Critics argue mandatory arbitration "
            "deprives investors of jury trial rights and class action remedies (post- "
            "Concepcion, class waivers in brokerage agreements are generally enforceable). "
            "Proponents argue FINRA provides specialized, efficient, lower-cost resolution. "
            "(7) SEC oversight: FINRA rules are approved by the SEC; any changes to the "
            "arbitration program require SEC approval."
        ),
        related_topics=[
            "finra_customer_arbitration", "finra_industry_arbitration",
            "class_action_arbitration", "investor_protection",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # OIL & GAS ADR
    # ======================================================================

    "oil_gas_joa_arbitration": DoctrineCacheBlock(
        topic="Oil and Gas ADR - JOA Arbitration Clauses",
        category="oil_gas_adr",
        authority_weight=0.88,
        citations=[
            "AAPL Form 610-1989 Model Form Operating Agreement Article XVI",
            "AAPL Form 610-2015 Model Form Operating Agreement Article 17",
            "COPAS Accounting Procedures (Council of Petroleum Accountants Societies)",
            "Burlington Resources Oil & Gas v Han, 590 SW3d 524 (Tex. 2019)",
        ],
        content=(
            "Oil and gas disputes frequently use ADR, particularly arbitration under Joint "
            "Operating Agreements (JOAs). Key aspects: (1) AAPL Form 610: The standard "
            "model form operating agreement published by the American Association of "
            "Professional Landmen. The 1989 version (Article XVI) and 2015 version "
            "(Article 17) both contain optional arbitration clauses. Parties check a box "
            "to elect arbitration vs. litigation. When selected, disputes 'arising out of "
            "or relating to' the JOA are arbitrated. (2) Common JOA disputes: Accounting "
            "disputes (COPAS audits, overhead charges, AFE overruns), consent/non-consent "
            "elections, operatorship disputes, breach of operator duty (prudent operator "
            "standard), damage to wellbore, environmental remediation cost allocation, "
            "area of mutual interest (AMI) disputes. (3) COPAS arbitration: The Council "
            "of Petroleum Accountants Societies provides specialized dispute resolution "
            "for joint interest billing/accounting disputes. (4) Expert determination: "
            "Technical disputes (reserves, well productivity, facility condition) are "
            "sometimes resolved by expert determination rather than arbitration. (5) "
            "Texas context: Most Permian Basin JOAs use Texas law. Texas courts enforce "
            "JOA arbitration clauses broadly. Burlington Resources v Han (2019): The "
            "Texas Supreme Court addressed the scope of the arbitration clause in an "
            "AAPL 610 JOA. (6) Royalty disputes: Generally not arbitrable unless a "
            "specific arbitration agreement exists in the lease (most oil and gas leases "
            "do not contain arbitration clauses)."
        ),
        related_topics=[
            "texas_adr_act_cprc_154", "arbitration_clause_drafting",
            "expert_determination", "construction_arbitration",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # UNCONSCIONABILITY
    # ======================================================================

    "unconscionability_defense": DoctrineCacheBlock(
        topic="Unconscionability Defense to Arbitration",
        category="contract_defenses",
        authority_weight=0.91,
        citations=[
            "AT&T Mobility v Concepcion, 563 US 333 (2011)",
            "Rent-A-Center West v Jackson, 561 US 63 (2010)",
            "Armendariz v Foundation Health Psychcare Services, 24 Cal.4th 83 (2000)",
            "In re Halliburton Co, 80 SW3d 566 (Tex. 2002)",
        ],
        content=(
            "Unconscionability is the most frequently invoked defense to enforcement of "
            "arbitration agreements. Two elements must be present: (1) Procedural "
            "unconscionability: Defects in the bargaining process — oppression (unequal "
            "bargaining power, take-it-or-leave-it contracts, lack of meaningful choice) "
            "and surprise (terms hidden in fine print, complex language, no opportunity "
            "to review). (2) Substantive unconscionability: Unfairly one-sided terms — "
            "lopsided fee-shifting, unduly restrictive discovery, shortened limitations "
            "period, venue selection benefiting one side, waiver of statutory remedies, "
            "one-way arbitration clause (only one party must arbitrate), selection of "
            "biased arbitral forum. California applies a sliding scale: greater procedural "
            "unconscionability requires less substantive, and vice versa (Armendariz). "
            "Texas requires both procedural and substantive unconscionability; Texas courts "
            "are generally reluctant to find arbitration agreements unconscionable (In re "
            "Halliburton). Post-Concepcion, the unconscionability defense is significantly "
            "limited: state rules that have a disproportionate impact on arbitration "
            "agreements are preempted even if framed as general contract law. Post-Rent-A- "
            "Center, if a delegation clause exists, the unconscionability challenge must be "
            "directed at the delegation clause itself to be heard by the court."
        ),
        related_topics=[
            "faa_section_2_savings_clause", "faa_preemption",
            "separability_doctrine", "class_action_arbitration",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # EMPLOYMENT ARBITRATION
    # ======================================================================

    "employment_arbitration": DoctrineCacheBlock(
        topic="Employment Arbitration",
        category="employment_adr",
        authority_weight=0.93,
        citations=[
            "Epic Systems Corp v Lewis, 584 US 497 (2018)",
            "Gilmer v Interstate/Johnson Lane Corp, 500 US 20 (1991)",
            "Circuit City v Adams, 532 US 105 (2001)",
            "Ending Forced Arbitration of Sexual Assault and Sexual Harassment Act (PL 117-90, 2022)",
            "14 Penn Plaza v Pyett, 556 US 247 (2009)",
        ],
        content=(
            "Employment arbitration has expanded dramatically. Legal landscape: (1) Gilmer "
            "v Interstate (1991): Age Discrimination in Employment Act (ADEA) claims are "
            "arbitrable under a pre-dispute arbitration agreement. (2) Circuit City v Adams "
            "(2001): FAA Section 1 exclusion for 'contracts of employment' covers only "
            "transportation workers. All other employment agreements are covered by the FAA. "
            "(3) Epic Systems v Lewis (2018): Employers can enforce class/collective action "
            "waivers in employment arbitration agreements. The NLRA Section 7 does not "
            "create a non-waivable right to class or collective litigation. (4) 14 Penn "
            "Plaza v Pyett (2009): CBA arbitration clauses can waive employees' rights to "
            "a judicial forum for statutory discrimination claims if the waiver is clear "
            "and unmistakable. (5) Ending Forced Arbitration Act (2022): Employees can "
            "void pre-dispute arbitration agreements for claims of sexual assault or sexual "
            "harassment. Applies to agreements entered into before or after enactment. (6) "
            "State laws: Several states have attempted to ban mandatory employment arbitration "
            "(California AB 51, New York CPLR 7515), but these face FAA preemption challenges. "
            "(7) Fairness protocols: AAA Due Process Protocol, JAMS Minimum Standards, and "
            "various state employer-pays rules ensure baseline procedural protections. "
            "(8) Common employment claims: Title VII, ADA, ADEA, FLSA, state discrimination "
            "and wage laws, wrongful termination, non-compete enforcement."
        ),
        related_topics=[
            "aaa_employment_rules", "jams_employment_rules",
            "class_action_arbitration", "unconscionability_defense",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # CONSUMER ARBITRATION
    # ======================================================================

    "consumer_arbitration": DoctrineCacheBlock(
        topic="Consumer Arbitration",
        category="consumer_adr",
        authority_weight=0.89,
        citations=[
            "AT&T Mobility v Concepcion, 563 US 333 (2011)",
            "CompuCredit Corp v Greenwood, 565 US 95 (2012)",
            "AAA Consumer Arbitration Rules (2014)",
            "AAA Consumer Due Process Protocol (1998)",
            "CFPB Arbitration Study (2015)",
        ],
        content=(
            "Consumer arbitration governs disputes between businesses and individual "
            "consumers under pre-dispute arbitration clauses in consumer contracts (credit "
            "cards, cell phones, internet services, nursing homes, etc.). Key issues: (1) "
            "Enforceability: Post-Concepcion, consumer arbitration agreements with class "
            "waivers are generally enforceable under the FAA, even in adhesion contracts. "
            "(2) AAA Consumer Rules: Separate rules with consumer protections — filing fee "
            "capped at $200 for claims under $10K (business pays the rest), hearing location "
            "in consumer's hometown, documents-only option, and the business bears all "
            "arbitrator fees and expenses. (3) AAA Consumer Due Process Protocol (1998): "
            "Requires: reasonable cost, neutral forum, adequate discovery, same remedies "
            "as court, right to representation, reasoned written award, and independent "
            "neutral administration. (4) CFPB Arbitration Rule (2017): The Consumer Financial "
            "Protection Bureau issued a rule banning class action waivers in consumer "
            "financial contracts, but Congress repealed it under the Congressional Review "
            "Act in November 2017. (5) Effective vindication: The Supreme Court in Italian "
            "Colors (2013) held that the effective vindication doctrine does not require "
            "class arbitration, even when individual arbitration costs exceed the potential "
            "recovery. (6) State mini-CFPB laws: Some states have enacted consumer "
            "protections for arbitration (California, New York, New Jersey)."
        ),
        related_topics=[
            "class_action_arbitration", "unconscionability_defense",
            "faa_preemption", "online_dispute_resolution",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # CONSTRUCTION ARBITRATION
    # ======================================================================

    "construction_arbitration": DoctrineCacheBlock(
        topic="Construction Dispute Arbitration",
        category="construction_adr",
        authority_weight=0.87,
        citations=[
            "AIA Document A201-2017 (General Conditions) Article 15",
            "ConsensusDocs 200 Article 12",
            "AAA Construction Industry Arbitration Rules (2015)",
            "Dispute Review Board Foundation (DRBF) Practices and Procedures",
        ],
        content=(
            "Construction disputes are among the most common subjects of arbitration in "
            "the US. Key features: (1) AIA A201-2017 Article 15: Establishes a multi-tier "
            "dispute resolution process — initial decision by the Architect (Section 15.2), "
            "mediation as a condition precedent to arbitration/litigation (Section 15.3), "
            "then arbitration if elected or litigation (Section 15.4). (2) ConsensusDocs "
            "200: Alternative standard form; Article 12 requires direct discussions, then "
            "mitigation, then binding dispute resolution (parties choose arbitration or "
            "litigation). (3) Common disputes: Delay claims (excusable, compensable, "
            "concurrent), disruption/loss of productivity, differing site conditions "
            "(Type I and Type II), defective work, scope disputes (cardinal changes), "
            "payment disputes (mechanics liens, pay-if-paid vs. pay-when-paid), "
            "acceleration, warranty claims. (4) Dispute Review Boards (DRBs): Standing "
            "panels (typically three members) established at project commencement that "
            "conduct site visits and issue advisory recommendations on disputes as they "
            "arise. Used on major infrastructure projects. DRB recommendations are admissible "
            "in subsequent arbitration/litigation and carry persuasive weight. (5) Expert "
            "witness intensive: Construction arbitrations typically involve scheduling experts, "
            "cost estimators, and technical experts. (6) Multi-party complexity: Owner, CM, "
            "GC, subcontractors, suppliers, architects, engineers — joinder and consolidation "
            "are critical."
        ),
        related_topics=[
            "aaa_construction_rules", "multi_party_arbitration",
            "med_arb_hybrid", "expert_determination",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # INTERNATIONAL COMMERCIAL ARBITRATION
    # ======================================================================

    "international_commercial_arbitration": DoctrineCacheBlock(
        topic="International Commercial Arbitration",
        category="international_arbitration",
        authority_weight=0.93,
        citations=[
            "UNCITRAL Model Law on International Commercial Arbitration (1985, amended 2006)",
            "Mitsubishi Motors v Soler Chrysler-Plymouth, 473 US 614 (1985)",
            "Scherk v Alberto-Culver Co, 417 US 506 (1974)",
            "Born, International Commercial Arbitration (3d ed. 2021)",
        ],
        content=(
            "International commercial arbitration is the primary method for resolving "
            "cross-border business disputes. Foundations: (1) Party autonomy: Parties "
            "choose the seat, governing law, language, institution, and procedural rules. "
            "(2) Neutrality: Arbitration avoids the perceived bias of litigating in the "
            "other party's home courts. (3) Enforceability: Awards are enforceable in 172 "
            "countries under the New York Convention — far broader than any network for "
            "court judgment recognition. (4) Choice of seat: Determines the procedural "
            "law (lex arbitri), the supervisory court, and the availability of annulment. "
            "Popular seats include London, Paris, Singapore, Hong Kong, Geneva, Stockholm, "
            "and New York. (5) Choice of substantive law: Parties may choose any law; "
            "absent choice, the tribunal applies the law it considers appropriate (often "
            "using conflict-of-laws analysis). Some tribunals apply lex mercatoria or "
            "transnational commercial law principles. (6) Key institutions: ICC, LCIA, "
            "SIAC, HKIAC, SCC, VIAC, CIETAC. (7) Confidentiality: Not automatic in many "
            "jurisdictions; should be addressed in the arbitration agreement or procedural "
            "order. (8) Third-party funding: Increasingly prevalent; disclosure obligations "
            "expanding. (9) Treaty-based arbitration: Investor-State disputes under BITs "
            "and multilateral treaties (ICSID, UNCITRAL). (10) Mitsubishi Motors (1985): "
            "Antitrust claims are arbitrable in international disputes."
        ),
        related_topics=[
            "new_york_convention_enforcement", "icc_arbitration_rules",
            "uncitral_arbitration_rules", "icsid_convention",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # WAIVER OF ARBITRATION
    # ======================================================================

    "waiver_of_arbitration_right": DoctrineCacheBlock(
        topic="Waiver of Right to Arbitrate",
        category="arbitration_procedure",
        authority_weight=0.92,
        citations=[
            "Morgan v Sundance Inc, 596 US 411 (2022)",
            "In re Citigroup Inc, 376 F.3d 23 (1st Cir. 2004)",
            "Perry Homes v Cull, 258 SW3d 580 (Tex. 2008)",
        ],
        content=(
            "A party may waive its contractual right to arbitrate by acting inconsistently "
            "with that right, typically by litigating in court. In Morgan v Sundance (2022), "
            "the Supreme Court eliminated the requirement of showing prejudice as a condition "
            "for finding waiver. Previously, most circuits required the party opposing "
            "arbitration to show it was prejudiced by the delay. The Court held that the "
            "FAA does not authorize courts to create arbitration-specific procedural rules; "
            "waiver should be determined under the same principles applicable to any "
            "contractual right. Factors courts consider (post-Morgan, prejudice-free): "
            "(1) Whether the party seeking arbitration substantially invoked the litigation "
            "machinery (filing motions, conducting discovery, seeking rulings on the merits). "
            "(2) The length of delay before asserting the right to arbitrate. (3) Whether "
            "the party seeking arbitration participated in discovery inconsistent with "
            "arbitration. (4) Whether the party filed a dispositive motion. (5) The number "
            "of hearings and court proceedings attended. Texas (Perry Homes, 2008): Applied "
            "a totality-of-the-circumstances test requiring substantial invocation of the "
            "judicial process to the other party's detriment; post-Morgan, the prejudice "
            "requirement is gone."
        ),
        related_topics=[
            "faa_section_3_stay", "faa_section_4_compel",
            "arbitrability_substantive", "litigation_conduct",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # ARBITRATION COSTS AND FEES
    # ======================================================================

    "arbitration_costs_fee_shifting": DoctrineCacheBlock(
        topic="Arbitration Costs and Fee-Shifting",
        category="arbitration_procedure",
        authority_weight=0.86,
        citations=[
            "Green Tree Financial Corp v Randolph, 531 US 79 (2000)",
            "AAA Fee Schedule (Commercial, Employment, Consumer)",
            "ICC Cost Calculator",
            "Cole v Burns International Security Services, 105 F.3d 1465 (DC Cir. 1997)",
        ],
        content=(
            "Arbitration costs can significantly impact access to justice. Key principles: "
            "(1) Green Tree Financial v Randolph (2000): The Supreme Court held that the "
            "mere risk of prohibitive arbitration costs does not render an arbitration "
            "agreement unenforceable; the party challenging enforcement must demonstrate "
            "that the costs are actually prohibitive. (2) AAA fee schedules: Commercial — "
            "graduated filing fees ($925 for claims under $75K to $15,325 for claims over "
            "$10M). Construction and Employment have separate schedules. Consumer — employee "
            "filing fee capped at $200 (employer pays the rest). (3) ICC: Ad valorem fees "
            "based on the amount in dispute. Administrative fees and arbitrator fees "
            "calculated by schedule. Advance on costs required from both parties. (4) JAMS: "
            "Arbitrator hourly rates ($400-$1,200+/hour) plus case management fees. (5) "
            "Employment/consumer: Under Cole v Burns and subsequent cases, employers/businesses "
            "must bear the costs of arbitration beyond what the employee/consumer would pay "
            "to file in court. Excessive fee requirements can render an agreement "
            "unconscionable. (6) Fee-shifting provisions: Some arbitration agreements "
            "include loser-pays clauses. Courts scrutinize these in consumer and employment "
            "contexts for unconscionability, especially where they would deter the pursuit "
            "of statutory claims. (7) Allocation of costs: Arbitrators have discretion in "
            "allocating hearing costs, arbitrator fees, and attorneys' fees in the award."
        ),
        related_topics=[
            "unconscionability_defense", "consumer_arbitration",
            "employment_arbitration", "aaa_commercial_rules",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # CONFIDENTIALITY IN ARBITRATION
    # ======================================================================

    "confidentiality_in_arbitration": DoctrineCacheBlock(
        topic="Confidentiality in Arbitration",
        category="arbitration_procedure",
        authority_weight=0.85,
        citations=[
            "LCIA Rules Article 30 (Confidentiality)",
            "ICC Note to Parties on Conduct of Arbitration",
            "Esso Australia Resources v Plowman, (1995) 183 CLR 10 (HCA)",
            "UNCITRAL Rules on Transparency (2014)",
        ],
        content=(
            "Confidentiality in arbitration is widely assumed but not uniformly guaranteed. "
            "Key considerations: (1) Institutional rules vary: LCIA Rule 30 imposes broad "
            "confidentiality obligations on parties, arbitrators, and the LCIA. ICC Rules "
            "are largely silent on party confidentiality (Art. 22(3) merely permits "
            "appropriate measures). AAA Commercial Rules do not impose party confidentiality. "
            "(2) National law: Some jurisdictions impose arbitration confidentiality by "
            "statute (England, Singapore, Hong Kong). Others do not (Australia — Esso v "
            "Plowman held that arbitration confidentiality is not an implied term). US law "
            "does not impose blanket arbitration confidentiality. (3) Contractual "
            "confidentiality: Best practice is to include an express confidentiality clause "
            "in the arbitration agreement specifying the scope (proceedings, documents, "
            "award), exceptions (legal obligations, enforcement proceedings), and remedies "
            "for breach. (4) Exceptions to confidentiality: Regulatory requirements, court "
            "proceedings (confirmation, vacatur, enforcement), protection of legal rights, "
            "professional obligations. (5) Investment treaty arbitration: Trend toward "
            "transparency (UNCITRAL Transparency Rules, ICSID Rule amendments). (6) "
            "Award publication: ICC publishes redacted awards. Some institutions maintain "
            "searchable databases. FINRA awards are publicly available. (7) Witness "
            "confidentiality: Arbitral tribunals may issue confidentiality orders "
            "protecting witness identity and testimony."
        ),
        related_topics=[
            "mediation_uma", "icc_arbitration_rules",
            "uncitral_arbitration_rules", "arbitration_clause_drafting",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # INVESTOR-STATE ARBITRATION
    # ======================================================================

    "investor_state_arbitration": DoctrineCacheBlock(
        topic="Investor-State Dispute Settlement (ISDS)",
        category="international_arbitration",
        authority_weight=0.91,
        citations=[
            "Philip Morris v Uruguay, ICSID Case No. ARB/10/7 (2016)",
            "Metalclad Corp v Mexico, ICSID Case No. ARB(AF)/97/1 (2000)",
            "Bilateral Investment Treaties (BITs) — 2,800+ worldwide",
            "Energy Charter Treaty Article 26",
        ],
        content=(
            "Investor-State Dispute Settlement (ISDS) allows foreign investors to bring "
            "arbitration claims directly against host States for violations of investment "
            "treaty protections. Key aspects: (1) Treaty standards: Fair and equitable "
            "treatment (FET), expropriation (direct and indirect), national treatment, "
            "most-favored-nation treatment, full protection and security, umbrella clauses. "
            "(2) Consent mechanisms: BIT consent clauses, multilateral treaty provisions "
            "(Energy Charter Treaty Art. 26), national investment laws with arbitration "
            "offers. (3) Forums: ICSID (most common), UNCITRAL ad hoc, ICC, SCC, PCA. "
            "(4) Notable cases: Metalclad v Mexico (indirect expropriation through "
            "regulatory action); Philip Morris v Uruguay (upheld tobacco regulation under "
            "FET and expropriation claims, recognizing regulatory space). (5) Reform debates: "
            "Criticism of ISDS includes: lack of consistency (no binding precedent), "
            "challenges to legitimate regulation, arbitrator conflicts of interest, "
            "asymmetry (only investors can bring claims), and insufficient transparency. "
            "(6) Reform proposals: UNCITRAL Working Group III is developing reforms "
            "including a multilateral investment court, appellate mechanism, standing "
            "tribunal, and enhanced transparency. The EU has proposed a Multilateral "
            "Investment Court. (7) Several countries have terminated BITs or withdrawn "
            "from ICSID (Bolivia, Ecuador, Venezuela, India — replaced with new model BIT)."
        ),
        related_topics=[
            "icsid_convention", "bilateral_investment_treaty",
            "new_york_convention_enforcement", "uncitral_arbitration_rules",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # ARBITRATOR POWERS & INTERIM MEASURES
    # ======================================================================

    "interim_measures_arbitration": DoctrineCacheBlock(
        topic="Interim Measures in Arbitration",
        category="arbitration_procedure",
        authority_weight=0.86,
        citations=[
            "UNCITRAL Model Law Article 17 (Power of Arbitral Tribunal to Order Interim Measures)",
            "RUAA Section 8 (Provisional Remedies)",
            "ICC Article 28 (Conservatory and Interim Measures)",
            "Born, International Commercial Arbitration, Ch. 17 (3d ed. 2021)",
        ],
        content=(
            "Arbitral tribunals and emergency arbitrators have broad power to order interim "
            "measures. Types of interim measures: (1) Preservation orders: Preventing "
            "destruction, alteration, or disposal of evidence. (2) Asset freezing: "
            "Preventing dissipation of assets to protect future award enforcement. (3) "
            "Anti-suit injunctions: Restraining a party from pursuing parallel court "
            "proceedings. (4) Security for costs: Requiring a party to provide security "
            "for the other side's potential cost award. (5) Status quo preservation: "
            "Maintaining existing conditions pending final resolution. (6) Performance "
            "orders: Requiring a party to perform specific obligations pending the award. "
            "Standards for granting interim measures (UNCITRAL Model Law Art. 17A): "
            "(a) harm not adequately reparable by damages if the measure is not ordered; "
            "(b) such harm substantially outweighs the harm to the party against whom the "
            "measure is directed; and (c) reasonable possibility the requesting party will "
            "succeed on the merits. Court-ordered interim measures: Parties may seek "
            "interim measures from courts without waiving arbitration. Most arbitration "
            "agreements and institutional rules expressly preserve this right. Enforcement "
            "of tribunal-ordered interim measures typically requires court assistance, as "
            "arbitrators lack enforcement powers."
        ),
        related_topics=[
            "emergency_arbitrator", "uncitral_arbitration_rules",
            "faa_section_3_stay", "ruaa_overview",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # PUNITIVE DAMAGES IN ARBITRATION
    # ======================================================================

    "punitive_damages_arbitration": DoctrineCacheBlock(
        topic="Punitive Damages in Arbitration",
        category="arbitration_remedies",
        authority_weight=0.86,
        citations=[
            "Mastrobuono v Shearson Lehman Hutton, 514 US 52 (1995)",
            "RUAA Section 21(a) (Remedies: Punitive Damages)",
            "Garrity v Lyle Stuart Inc, 40 NY2d 354 (1976)",
        ],
        content=(
            "The availability of punitive damages in arbitration is a significant remedial "
            "issue. Key principles: (1) Mastrobuono v Shearson Lehman Hutton (1995): The "
            "Supreme Court held that arbitrators can award punitive damages under the FAA "
            "unless the parties clearly agree to exclude them. A general choice-of-law "
            "clause selecting New York law (which under Garrity prohibited arbitral "
            "punitive damages) was insufficient to waive punitive damages — an explicit "
            "exclusion is required. (2) RUAA Section 21: Expressly authorizes arbitrators "
            "to award punitive damages and other exemplary relief to the same extent "
            "available in a civil action. (3) State law variations: New York's Garrity "
            "rule (prohibiting arbitral punitive damages) was effectively overridden in "
            "FAA-governed arbitrations by Mastrobuono. Some arbitration agreements "
            "explicitly exclude punitive damages; courts generally enforce such exclusions "
            "unless they conflict with non-waivable statutory rights. (4) Statutory claims: "
            "Where statutes authorize punitive damages (e.g., Title VII, state consumer "
            "protection acts), waiver of punitive damages in the arbitration agreement may "
            "be unenforceable as it would prevent the effective vindication of statutory "
            "rights. (5) FINRA: Arbitrators may award punitive damages; Rule 12504(a) "
            "allows panels to assess any damages that a court could assess. (6) Insurance "
            "coverage: Whether liability insurance covers punitive damages awarded in "
            "arbitration varies by state."
        ),
        related_topics=[
            "arbitration_costs_fee_shifting", "finra_customer_arbitration",
            "employment_arbitration", "consumer_arbitration",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # MEDIATOR ETHICS
    # ======================================================================

    "mediator_ethics_model_standards": DoctrineCacheBlock(
        topic="Mediator Ethics - Model Standards of Conduct",
        category="mediation",
        authority_weight=0.86,
        citations=[
            "Model Standards of Conduct for Mediators (AAA/ABA/ACR, 2005)",
            "Model Standards of Practice for Family and Divorce Mediation (AFCC, 2001)",
            "Florida Rules for Certified and Court-Appointed Mediators (Ch. 10)",
        ],
        content=(
            "The Model Standards of Conduct for Mediators, jointly adopted by the AAA, "
            "ABA, and ACR (Association for Conflict Resolution) in 2005, set ethical "
            "guidelines for mediation practice. Nine standards: (1) Self-Determination: "
            "The mediator shall conduct the process based on the principle of party "
            "self-determination, the act of coming to a voluntary, uncoerced decision. "
            "(2) Impartiality: The mediator shall remain impartial throughout the process "
            "and shall not favor any party. (3) Conflicts of Interest: The mediator shall "
            "avoid conflicts of interest during and after mediation. Full disclosure of "
            "known conflicts. (4) Competence: The mediator shall mediate only when "
            "qualified by training, experience, or education. (5) Confidentiality: The "
            "mediator shall maintain confidentiality of all information obtained during "
            "the mediation. (6) Quality of the Process: The mediator shall conduct the "
            "mediation in a fair, diligent, and impartial manner, promoting mutual respect "
            "among the parties. (7) Advertising and Solicitation: Truthful and not "
            "misleading. (8) Fees and Other Charges: Must be reasonable and communicated "
            "in advance. (9) Advancement of Mediation Practice: The mediator should act "
            "to advance the practice and improve the quality of mediation. State "
            "certification: Many states certify mediators (Florida, Texas, Virginia) with "
            "training hour requirements (typically 40 hours for civil, 40 additional for "
            "family)."
        ),
        related_topics=[
            "facilitative_mediation", "evaluative_mediation",
            "mediation_uma", "court_annexed_adr",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # ENDING FORCED ARBITRATION ACT
    # ======================================================================

    "ending_forced_arbitration_act": DoctrineCacheBlock(
        topic="Ending Forced Arbitration of Sexual Assault and Harassment Act",
        category="federal_arbitration",
        authority_weight=0.94,
        citations=[
            "Pub. L. 117-90, 136 Stat. 26 (March 3, 2022)",
            "9 USC 401-402",
            "Johnson v Everyrealm Inc, 657 F.Supp.3d 535 (SDNY 2023)",
        ],
        content=(
            "The Ending Forced Arbitration of Sexual Assault and Sexual Harassment Act "
            "(EFAA), signed March 3, 2022, amends the FAA by adding a new Chapter 4 "
            "(9 USC 401-402). Key provisions: (1) Section 402(a): At the election of the "
            "person alleging sexual assault or sexual harassment, no pre-dispute arbitration "
            "agreement or pre-dispute joint-action waiver shall be valid or enforceable with "
            "respect to a case relating to the sexual assault or sexual harassment dispute. "
            "(2) Applies retroactively to pre-existing arbitration agreements. (3) The "
            "claimant makes the election: The party alleging the conduct decides whether "
            "to arbitrate or litigate. If the claimant does not elect to void the "
            "agreement, the arbitration clause remains enforceable. (4) 'Sexual harassment "
            "dispute' is defined broadly under 9 USC 401(4). (5) Section 402(b): "
            "Determination of whether the Act applies is for the court, not the arbitrator, "
            "irrespective of any delegation clause. (6) Scope questions: Courts are "
            "addressing whether the EFAA voids only the sexual harassment claims or the "
            "entire arbitration agreement (including non-sexual-harassment claims). In "
            "Johnson v Everyrealm (SDNY 2023), the court held that if a case relates to "
            "a sexual harassment dispute, all claims in that case can proceed in court. "
            "(7) The SPEAK OUT Act (PL 117-224, 2022) separately addresses NDAs and "
            "non-disparagement clauses in sexual harassment cases."
        ),
        related_topics=[
            "employment_arbitration", "faa_scope_applicability",
            "consumer_arbitration", "unconscionability_defense",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # RES JUDICATA & COLLATERAL ESTOPPEL
    # ======================================================================

    "res_judicata_collateral_estoppel": DoctrineCacheBlock(
        topic="Res Judicata and Collateral Estoppel in Arbitration",
        category="arbitration_effects",
        authority_weight=0.85,
        citations=[
            "Restatement (Second) of Judgments 84 (1982)",
            "Dean Witter Reynolds v Byrd, 470 US 213 (1985)",
            "Bear Stearns v 1109580 Ontario, 409 F.3d 87 (2d Cir. 2005)",
        ],
        content=(
            "Arbitration awards can have preclusive effect in subsequent proceedings under "
            "principles of res judicata (claim preclusion) and collateral estoppel (issue "
            "preclusion). Key principles: (1) Claim preclusion: A confirmed arbitration "
            "award on the merits bars relitigation of the same claims between the same "
            "parties. An unconfirmed award may also have preclusive effect under the "
            "Restatement (Second) of Judgments Section 84, which treats arbitration awards "
            "like court judgments for preclusion purposes, provided the arbitration "
            "proceeding afforded adequate procedural protections. (2) Issue preclusion: "
            "Specific factual or legal findings by an arbitrator can preclude relitigation "
            "of those issues in subsequent proceedings. Requirements: the issue was actually "
            "litigated and decided, the determination was essential to the award, and the "
            "party against whom preclusion is asserted had a full and fair opportunity to "
            "be heard. (3) Limitations: If the arbitration award is unreasoned, it may be "
            "impossible to determine which issues were actually decided, defeating issue "
            "preclusion. (4) Non-mutual preclusion: Some courts allow non-parties to the "
            "arbitration to invoke offensive collateral estoppel based on arbitral findings "
            "(e.g., Bear Stearns, 2d Cir. 2005). (5) Arbitration and litigation interplay: "
            "Where claims are split between arbitration and court, the first decision may "
            "have preclusive effect on overlapping issues."
        ),
        related_topics=[
            "faa_section_9_confirmation", "faa_section_10_vacatur",
            "award_enforcement_domestication", "manifest_disregard",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # REAL ESTATE ARBITRATION
    # ======================================================================

    "real_estate_arbitration": DoctrineCacheBlock(
        topic="Real Estate Dispute Arbitration",
        category="real_estate_adr",
        authority_weight=0.84,
        citations=[
            "TAR (Texas Association of Realtors) Contract Forms - Mediation Paragraph",
            "AAA Real Estate Industry Arbitration Rules",
            "NAR Code of Ethics Article 17 (Arbitration of Disputes)",
        ],
        content=(
            "Real estate disputes are increasingly resolved through ADR. Key frameworks: "
            "(1) Residential transactions: Standard form contracts (TAR, NAR affiliates) "
            "typically include mediation clauses as conditions precedent to litigation or "
            "arbitration. The TAR Residential Contract mediation paragraph requires parties "
            "to mediate before filing suit; failure to mediate can forfeit the right to "
            "recover attorneys' fees even if prevailing. (2) NAR Code of Ethics Art. 17: "
            "Requires REALTORS to submit disputes with other REALTORS to arbitration through "
            "their local association. This is a mandatory ethics obligation, not a contractual "
            "right of the consumer. Covers commission disputes, procuring cause issues, and "
            "cooperative compensation disputes. (3) Commercial real estate: Arbitration "
            "clauses are common in commercial leases, purchase agreements, partnership "
            "agreements, and development contracts. Issues include rent escalation disputes, "
            "CAM reconciliation, tenant improvement allowances, exclusivity violations, "
            "and co-tenancy provisions. (4) Title disputes: Generally not suitable for "
            "arbitration (in rem proceedings, quiet title, and recording act issues require "
            "court jurisdiction). (5) Homeowner associations: CC&R arbitration provisions; "
            "some states mandate ADR for HOA disputes (California Davis-Stirling Act). "
            "(6) Construction defect overlay: Real estate disputes often involve "
            "construction defect claims subject to separate arbitration provisions."
        ),
        related_topics=[
            "texas_adr_act_cprc_154", "construction_arbitration",
            "mediation_uma", "arbitration_clause_drafting",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # APPEAL MECHANISMS
    # ======================================================================

    "appeal_mechanisms_arbitration": DoctrineCacheBlock(
        topic="Appeal Mechanisms in Arbitration",
        category="arbitration_procedure",
        authority_weight=0.83,
        citations=[
            "AAA Optional Appellate Arbitration Rules (2013)",
            "JAMS Optional Arbitration Appeal Procedure (2003)",
            "Hall Street Associates v Mattel, 552 US 576 (2008)",
            "Rent-A-Center West v Jackson, 561 US 63 (2010)",
        ],
        content=(
            "One of arbitration's defining features is the finality of awards with very "
            "limited judicial review. However, optional appellate mechanisms are available: "
            "(1) AAA Optional Appellate Rules (2013): Parties can agree (before or after "
            "the initial arbitration) to appellate review by a three-arbitrator appeal "
            "tribunal. Standard of review: The appeal tribunal may vacate or modify the "
            "award if it is based on errors of law that are material and prejudicial, or "
            "on determinations of fact that are clearly erroneous. This is broader than "
            "FAA Section 10 but narrower than de novo. (2) JAMS Optional Appeal Procedure "
            "(2003): Similar framework; appeal to a three-arbitrator panel reviewing for "
            "material errors of law or clearly erroneous factual findings. (3) Hall Street "
            "v Mattel (2008): The Supreme Court held that the FAA's grounds for vacatur "
            "(Section 10) and modification (Section 11) are exclusive and cannot be "
            "expanded by private agreement. Thus, parties cannot contract with a court "
            "for expanded review; they can only create contractual appellate mechanisms "
            "within the arbitration system. (4) Advantages: Provides a safety net against "
            "arbitrator error while maintaining the efficiency of arbitration. (5) "
            "Disadvantages: Adds time and cost; may undermine arbitration's finality "
            "advantage. (6) Industry adoption: More common in high-stakes commercial, "
            "construction, and IP disputes."
        ),
        related_topics=[
            "faa_section_10_vacatur", "manifest_disregard",
            "aaa_commercial_rules", "jams_comprehensive_rules",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # DELEGATION CLAUSE
    # ======================================================================

    "delegation_clause": DoctrineCacheBlock(
        topic="Delegation Clauses in Arbitration Agreements",
        category="arbitrability",
        authority_weight=0.93,
        citations=[
            "Rent-A-Center West v Jackson, 561 US 63 (2010)",
            "Henry Schein Inc v Archer & White Sales, 586 US 63 (2019)",
            "Coinbase v Bielski, 599 US 736 (2023)",
        ],
        content=(
            "A delegation clause is a provision within an arbitration agreement that "
            "delegates threshold questions of arbitrability to the arbitrator rather than "
            "the court. Key principles: (1) 'Clear and unmistakable' standard: Delegation "
            "must be evidenced by clear and unmistakable intent. Incorporating institutional "
            "rules that grant the arbitrator jurisdiction over jurisdictional objections "
            "(e.g., AAA Rule R-7, JAMS Rule 11, ICC Art. 6) constitutes clear and "
            "unmistakable delegation in most circuits. (2) Rent-A-Center (2010): A "
            "delegation clause is severable from the larger arbitration agreement. If a "
            "party challenges the arbitration agreement as unconscionable but does not "
            "specifically challenge the delegation clause, the delegation clause is enforced "
            "and the arbitrator decides the unconscionability question. (3) Henry Schein "
            "(2019): There is no 'wholly groundless' exception to delegation. If a valid "
            "delegation clause exists, the court must send arbitrability questions to the "
            "arbitrator even if the argument for arbitrability is obviously without merit. "
            "(4) Coinbase v Bielski (2023): While not directly about delegation, confirmed "
            "that a district court must stay proceedings during an interlocutory appeal of "
            "an order denying a motion to compel arbitration. (5) Practical effect: "
            "Delegation clauses, combined with institutional rules, route virtually all "
            "challenges to arbitration agreements to the arbitrator rather than the court, "
            "significantly reducing judicial oversight."
        ),
        related_topics=[
            "arbitrability_substantive", "separability_doctrine",
            "kompetenz_kompetenz", "unconscionability_defense",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # BILATERAL INVESTMENT TREATIES
    # ======================================================================

    "bilateral_investment_treaty": DoctrineCacheBlock(
        topic="Bilateral Investment Treaties (BITs)",
        category="international_arbitration",
        authority_weight=0.88,
        citations=[
            "US Model BIT (2012)",
            "UNCTAD Investment Policy Hub (2,800+ BITs cataloged)",
            "Germany-Pakistan BIT (1959, first modern BIT)",
            "North American Free Trade Agreement (NAFTA) Chapter 11 / USMCA",
        ],
        content=(
            "Bilateral Investment Treaties (BITs) are agreements between two States "
            "providing protections and arbitration mechanisms for foreign investors. Over "
            "2,800 BITs are in force worldwide. Key elements: (1) Substantive protections: "
            "Fair and equitable treatment (FET), protection against expropriation (with "
            "prompt, adequate, and effective compensation), national treatment (no less "
            "favorable than domestic investors), most-favored-nation treatment (no less "
            "favorable than investors from third States), full protection and security, "
            "free transfer of capital, and umbrella clauses (elevating contractual "
            "obligations to treaty obligations). (2) Dispute resolution: Typically provides "
            "for investor-State arbitration under ICSID, UNCITRAL Rules, or other forums. "
            "Cooling-off period (typically 6 months) before commencing arbitration. "
            "Fork-in-the-road clauses requiring election between local courts and "
            "arbitration. (3) US Model BIT (2012): Reflects US policy on investor "
            "protections, environmental/labor protections, transparency, and access to "
            "ICSID and UNCITRAL. (4) NAFTA Chapter 11 (now succeeded by USMCA): Provided "
            "investor-State arbitration for US, Canada, Mexico investors. USMCA eliminates "
            "ISDS between US and Canada, retains limited ISDS for US-Mexico in certain "
            "sectors. (5) Reform trends: Newer BITs include more precise FET definitions, "
            "carve-outs for regulatory measures, and sustainability provisions."
        ),
        related_topics=[
            "investor_state_arbitration", "icsid_convention",
            "international_commercial_arbitration", "new_york_convention_enforcement",
        ],
        last_verified="2026-02-01",
    ),

    # ======================================================================
    # KOMPETENZ-KOMPETENZ
    # ======================================================================

    "kompetenz_kompetenz": DoctrineCacheBlock(
        topic="Kompetenz-Kompetenz Principle",
        category="arbitrability",
        authority_weight=0.90,
        citations=[
            "UNCITRAL Model Law Article 16 (Competence to Rule on Jurisdiction)",
            "ICC Article 6(5) (prima facie jurisdiction)",
            "First Options of Chicago v Kaplan, 514 US 938 (1995)",
            "Born, International Commercial Arbitration, Ch. 5 (3d ed. 2021)",
        ],
        content=(
            "Kompetenz-Kompetenz (competence-competence) is the principle that an arbitral "
            "tribunal has the power to rule on its own jurisdiction, including objections "
            "to the existence or validity of the arbitration agreement. Application varies: "
            "(1) International arbitration (positive effect): Under the UNCITRAL Model Law "
            "Article 16 and most institutional rules, the tribunal has the power to decide "
            "its own jurisdiction, including the validity, existence, and scope of the "
            "arbitration agreement. The tribunal's jurisdictional decision is subject to "
            "later court review (either during the arbitration or at the enforcement stage). "
            "(2) French/Swiss approach (negative effect): Courts will decline to examine "
            "jurisdictional challenges and defer to the tribunal, unless the arbitration "
            "agreement is manifestly null or inapplicable. This maximizes tribunal autonomy. "
            "(3) US approach: Under First Options v Kaplan (1995), courts independently "
            "decide whether the parties agreed to arbitrate, unless the parties clearly and "
            "unmistakably agreed to delegate that question to the arbitrator (delegation "
            "clause). The US does not apply the negative effect of kompetenz-kompetenz. "
            "(4) ICC approach (Art. 6(5)): If there is a prima facie arbitration agreement, "
            "the ICC Court allows the arbitration to proceed; the tribunal then decides "
            "jurisdiction. (5) Practical effect: In jurisdictions recognizing the negative "
            "effect, parties must arbitrate first and challenge jurisdiction afterward, "
            "which favors arbitration. In the US, judicial gatekeeping is stronger."
        ),
        related_topics=[
            "arbitrability_substantive", "delegation_clause",
            "separability_doctrine", "uncitral_arbitration_rules",
        ],
        last_verified="2026-02-01",
    ),
}


# ---------------------------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------------------------

def build_doctrine_cache() -> DoctrineCacheIndex:
    """Build the complete doctrine cache index from all blocks."""
    index = DoctrineCacheIndex()
    index.build(DOCTRINE_BLOCKS)
    logger.info(
        "LG16 ADR doctrine cache built: {} blocks across {} categories",
        len(DOCTRINE_BLOCKS),
        len(index.category_index),
    )
    _persist_cache(index)
    return index


def _persist_cache(index: DoctrineCacheIndex) -> Path:
    """Persist the doctrine cache to disk as JSON."""
    cache_file = DOCTRINE_CACHE_DIR / "lg16_adr_doctrine_cache.json"
    payload: dict[str, Any] = {
        "engine_id": ENGINE_ID,
        "version": DOCTRINE_VERSION,
        "built_at": index.built_at,
        "block_count": len(index.blocks),
        "categories": {k: len(v) for k, v in index.category_index.items()},
        "blocks": {k: v.to_dict() for k, v in index.blocks.items()},
    }
    cache_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    logger.info("Doctrine cache persisted to {}", cache_file)
    return cache_file


def search_doctrines(
    query: str,
    top_k: int = 10,
    category_filter: str | None = None,
    min_authority: float = 0.0,
) -> list[dict[str, Any]]:
    """Search doctrine blocks by query string with optional filters."""
    results: list[dict[str, Any]] = []
    for key, block in DOCTRINE_BLOCKS.items():
        if category_filter and block.category.lower() != category_filter.lower():
            continue
        if block.authority_weight < min_authority:
            continue
        score = block.matches_query(query)
        if score > 0.05:
            results.append({
                "key": key,
                "topic": block.topic,
                "category": block.category,
                "authority_weight": block.authority_weight,
                "score": round(score, 4),
                "citations_count": len(block.citations),
                "related_topics": block.related_topics,
                "content_preview": block.content[:200] + "..." if len(block.content) > 200 else block.content,
            })
    results.sort(key=lambda x: x["score"], reverse=True)
    logger.debug("Doctrine search '{}': {} results (top_k={})", query, len(results), top_k)
    return results[:top_k]


def get_doctrine_block(key: str) -> DoctrineCacheBlock | None:
    """Retrieve a single doctrine block by key."""
    block = DOCTRINE_BLOCKS.get(key)
    if block:
        logger.debug("Retrieved doctrine block: {}", key)
    else:
        logger.warning("Doctrine block not found: {}", key)
    return block


def get_doctrine_cache() -> dict[str, DoctrineCacheBlock]:
    """Return the full doctrine block dictionary."""
    return DOCTRINE_BLOCKS


def get_coverage_map() -> dict[str, Any]:
    """Generate a coverage map of all doctrine categories and their blocks."""
    category_map: dict[str, list[str]] = {}
    authority_stats: dict[str, list[float]] = {}

    for key, block in DOCTRINE_BLOCKS.items():
        cat = block.category
        if cat not in category_map:
            category_map[cat] = []
            authority_stats[cat] = []
        category_map[cat].append(key)
        authority_stats[cat].append(block.authority_weight)

    coverage: dict[str, Any] = {
        "engine_id": ENGINE_ID,
        "version": DOCTRINE_VERSION,
        "total_blocks": len(DOCTRINE_BLOCKS),
        "total_categories": len(category_map),
        "categories": {},
    }

    for cat, keys in sorted(category_map.items()):
        weights = authority_stats[cat]
        coverage["categories"][cat] = {
            "block_count": len(keys),
            "blocks": keys,
            "avg_authority": round(sum(weights) / len(weights), 3) if weights else 0.0,
            "min_authority": round(min(weights), 3) if weights else 0.0,
            "max_authority": round(max(weights), 3) if weights else 0.0,
        }

    total_citations = sum(len(b.citations) for b in DOCTRINE_BLOCKS.values())
    total_related = sum(len(b.related_topics) for b in DOCTRINE_BLOCKS.values())
    all_weights = [b.authority_weight for b in DOCTRINE_BLOCKS.values()]

    coverage["statistics"] = {
        "total_citations": total_citations,
        "avg_citations_per_block": round(total_citations / len(DOCTRINE_BLOCKS), 1) if DOCTRINE_BLOCKS else 0.0,
        "total_related_topic_links": total_related,
        "avg_authority_weight": round(sum(all_weights) / len(all_weights), 3) if all_weights else 0.0,
        "min_authority_weight": round(min(all_weights), 3) if all_weights else 0.0,
        "max_authority_weight": round(max(all_weights), 3) if all_weights else 0.0,
    }

    logger.info(
        "Coverage map: {} blocks, {} categories, {} citations",
        coverage["total_blocks"],
        coverage["total_categories"],
        total_citations,
    )
    return coverage


def verify_doctrine_integrity() -> dict[str, Any]:
    """Verify integrity of all doctrine blocks (hash check, completeness)."""
    results: dict[str, Any] = {
        "engine_id": ENGINE_ID,
        "version": DOCTRINE_VERSION,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "total_blocks": len(DOCTRINE_BLOCKS),
        "passed": 0,
        "failed": 0,
        "warnings": 0,
        "issues": [],
    }

    all_topics_referenced: set[str] = set()
    all_keys: set[str] = set(DOCTRINE_BLOCKS.keys())

    for key, block in DOCTRINE_BLOCKS.items():
        issues_for_block: list[str] = []

        # Hash verification
        expected_hash = block._compute_hash()
        if block.hash_key != expected_hash:
            issues_for_block.append(f"Hash mismatch: stored={block.hash_key}, computed={expected_hash}")

        # Content length check
        if len(block.content) < 100:
            issues_for_block.append(f"Content too short: {len(block.content)} chars (min 100)")

        # Citations check
        if len(block.citations) < 1:
            issues_for_block.append("No citations provided")

        # Related topics check
        if len(block.related_topics) < 1:
            issues_for_block.append("No related topics")

        # Authority weight range
        if not (0.0 <= block.authority_weight <= 1.0):
            issues_for_block.append(f"Authority weight out of range: {block.authority_weight}")

        # Track referenced topics
        for rt in block.related_topics:
            all_topics_referenced.add(rt)

        if issues_for_block:
            results["failed"] += 1
            results["issues"].append({"key": key, "issues": issues_for_block})
        else:
            results["passed"] += 1

    # Check for dangling references (related_topics pointing to non-existent blocks)
    dangling = all_topics_referenced - all_keys
    if dangling:
        results["warnings"] += len(dangling)
        results["issues"].append({
            "key": "_global",
            "issues": [f"Dangling related_topic references: {sorted(dangling)}"],
        })

    results["integrity_score"] = round(results["passed"] / results["total_blocks"], 3) if results["total_blocks"] else 0.0

    logger.info(
        "Doctrine integrity check: {}/{} passed, {} warnings",
        results["passed"],
        results["total_blocks"],
        results["warnings"],
    )
    return results


def get_all_doctrine_categories() -> list[str]:
    """Return sorted list of unique doctrine categories."""
    return sorted({b.category for b in DOCTRINE_BLOCKS.values()})


def get_all_doctrine_topics() -> list[str]:
    """Return sorted list of all doctrine topics."""
    return sorted(b.topic for b in DOCTRINE_BLOCKS.values())


def get_doctrine_cache_hash() -> str:
    """Compute a SHA-256 hash over the full doctrine cache for integrity checks."""
    payload = json.dumps(
        {k: v.to_dict() for k, v in sorted(DOCTRINE_BLOCKS.items())},
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def get_doctrine_cache_stats() -> dict[str, Any]:
    """Return summary statistics about the doctrine cache."""
    categories: dict[str, int] = {}
    for block in DOCTRINE_BLOCKS.values():
        categories[block.category] = categories.get(block.category, 0) + 1
    return {
        "total_blocks": len(DOCTRINE_BLOCKS),
        "total_categories": len(categories),
        "categories": categories,
        "avg_authority": round(
            sum(b.authority_weight for b in DOCTRINE_BLOCKS.values()) / max(len(DOCTRINE_BLOCKS), 1), 3
        ),
    }


def get_stale_doctrines(max_age_days: int = 90) -> list[str]:
    """Return keys of doctrine blocks whose last_verified date exceeds max_age_days."""
    stale: list[str] = []
    now = datetime.now(timezone.utc)
    for key, block in DOCTRINE_BLOCKS.items():
        try:
            verified = datetime.fromisoformat(block.last_verified).replace(tzinfo=timezone.utc)
            if (now - verified).days > max_age_days:
                stale.append(key)
        except (ValueError, TypeError):
            stale.append(key)
    return stale
