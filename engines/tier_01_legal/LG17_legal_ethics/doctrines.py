"""
LG17 Legal Ethics Engine - Doctrine Cache
============================================
Pre-compiled legal ethics doctrine blocks for sub-200ms response.

Each block contains:
    - topic: Canonical identifier
    - category: Domain classification (model_rules, privilege, conflicts, etc.)
    - summary: Expert-level explanation
    - analysis: Detailed legal analysis with citations
    - authority: Statutory/rule citations and case law
    - keywords: Search optimization terms
    - jurisdiction: Applicable jurisdiction
    - confidence: Pre-assigned confidence score
    - last_updated: ISO timestamp
    - block_hash: SHA-256 integrity hash

55+ doctrine blocks covering:
    ABA Model Rules (all 8 categories), attorney-client privilege, Upjohn,
    crime-fraud exception, work product (Hickman), conflicts of interest,
    confidentiality, competence, fees, advertising, UPL, MJP, discipline,
    malpractice, fiduciary duties, trust accounts (IOLTA), organization as
    client, diminished capacity, prosecutorial ethics (Brady), judicial
    ethics (CJC), mediator ethics, arbitrator disclosure, Texas DRPC,
    SOX Section 205, legal tech / AI ethics, ghost-writing, metadata.

Port: 8407
Engine: LG17 Legal Ethics
Version: 2.0.0
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from typing import Any, ClassVar, Dict, FrozenSet, List, Optional, Set, Tuple

from loguru import logger


# ============================================================================
# DOCTRINE BLOCK MODEL
# ============================================================================

@dataclass
class DoctrineCacheBlock:
    """A single pre-compiled doctrine block."""
    topic: str
    category: str
    summary: str
    analysis: str
    authority: str
    keywords: List[str] = dc_field(default_factory=list)
    rule_reference: str = ""
    restatement_reference: str = ""
    jurisdiction: str = "ABA_MODEL"
    confidence: float = 0.90
    last_updated: str = dc_field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    block_hash: str = ""
    cross_references: List[str] = dc_field(default_factory=list)
    practice_tips: List[str] = dc_field(default_factory=list)
    sanctions: str = ""
    texas_notes: str = ""

    def __post_init__(self) -> None:
        if not self.block_hash:
            content = f"{self.topic}|{self.summary}|{self.analysis}|{self.authority}"
            self.block_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "topic": self.topic,
            "category": self.category,
            "summary": self.summary,
            "analysis": self.analysis,
            "authority": self.authority,
            "keywords": self.keywords,
            "rule_reference": self.rule_reference,
            "restatement_reference": self.restatement_reference,
            "jurisdiction": self.jurisdiction,
            "confidence": self.confidence,
            "last_updated": self.last_updated,
            "block_hash": self.block_hash,
            "cross_references": self.cross_references,
            "practice_tips": self.practice_tips,
            "sanctions": self.sanctions,
            "texas_notes": self.texas_notes,
        }


# ============================================================================
# DOCTRINE CACHE INDEX
# ============================================================================

class DoctrineCacheIndex:
    """Index over doctrine blocks for O(1) lookup by topic and keyword search."""

    def __init__(self) -> None:
        self._by_topic: Dict[str, DoctrineCacheBlock] = {}
        self._by_category: Dict[str, List[str]] = {}
        self._keyword_index: Dict[str, Set[str]] = {}
        self._all_topics: List[str] = []

    def add(self, block: DoctrineCacheBlock) -> None:
        """Add a block to the index."""
        self._by_topic[block.topic] = block
        self._all_topics.append(block.topic)
        if block.category not in self._by_category:
            self._by_category[block.category] = []
        self._by_category[block.category].append(block.topic)
        for kw in block.keywords:
            kw_lower = kw.lower()
            if kw_lower not in self._keyword_index:
                self._keyword_index[kw_lower] = set()
            self._keyword_index[kw_lower].add(block.topic)

    def get(self, topic: str) -> Optional[DoctrineCacheBlock]:
        """Get a block by topic."""
        return self._by_topic.get(topic)

    def search(self, query: str, max_results: int = 10) -> List[DoctrineCacheBlock]:
        """Search blocks by keyword matching."""
        tokens = query.lower().split()
        scores: Dict[str, int] = {}
        for token in tokens:
            for kw, topics in self._keyword_index.items():
                if token in kw or kw in token:
                    for topic in topics:
                        scores[topic] = scores.get(topic, 0) + 1
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results: List[DoctrineCacheBlock] = []
        for topic, _ in ranked[:max_results]:
            block = self._by_topic.get(topic)
            if block:
                results.append(block)
        return results

    def get_by_category(self, category: str) -> List[DoctrineCacheBlock]:
        """Get all blocks in a category."""
        topics = self._by_category.get(category, [])
        return [self._by_topic[t] for t in topics if t in self._by_topic]

    @property
    def total_blocks(self) -> int:
        """Return total blocks in cache."""
        return len(self._by_topic)

    @property
    def categories(self) -> List[str]:
        """Return all categories."""
        return list(self._by_category.keys())

    @property
    def topics(self) -> List[str]:
        """Return all topics."""
        return list(self._all_topics)

    def get_stats(self) -> Dict[str, Any]:
        """Return cache statistics."""
        return {
            "total_blocks": self.total_blocks,
            "categories": len(self._by_category),
            "category_distribution": {k: len(v) for k, v in self._by_category.items()},
            "total_keywords": len(self._keyword_index),
        }


# ============================================================================
# DOCTRINE BLOCKS -- 55+ blocks
# ============================================================================

DOCTRINE_BLOCKS: List[DoctrineCacheBlock] = [
    # ---- COMPETENCE / DILIGENCE / COMMUNICATION ----
    DoctrineCacheBlock(
        topic="competence_rule_1_1",
        category="client_lawyer_relationship",
        summary="ABA Model Rule 1.1 requires that a lawyer provide competent representation, requiring the legal knowledge, skill, thoroughness, and preparation reasonably necessary for the representation.",
        analysis="Model Rule 1.1 establishes the baseline duty of competence. Comment [1] identifies five factors: (1) relative complexity and specialized nature of the matter, (2) lawyer's general experience, (3) lawyer's training and experience in the field, (4) preparation and study the lawyer can give, and (5) whether referral or association with a more competent lawyer is feasible. Comment [8] (added 2012) addresses technology competence: lawyers must keep abreast of changes in the law and its practice, 'including the benefits and risks associated with relevant technology.' A lawyer may accept a matter outside their experience if they can become competent through reasonable study (Comment [2]) or associate with an experienced lawyer (Comment [4]). Competence is measured at the time of representation, not at the time of engagement. Failure to maintain competence is the most common basis for malpractice claims. In re Disciplinary Proceedings Against Inglimo (Wis. 2007) held that repeated failure to research applicable law constituted incompetence warranting suspension.",
        authority="ABA Model Rule 1.1; ABA Model Rule 1.1 Comments [1]-[8]; Restatement (Third) of the Law Governing Lawyers Section 52; In re Disciplinary Proceedings Against Inglimo, 740 N.W.2d 125 (Wis. 2007)",
        keywords=["competence", "rule 1.1", "legal knowledge", "skill", "technology competence", "preparation", "malpractice", "standard of care"],
        rule_reference="Model Rule 1.1",
        restatement_reference="Restatement (Third) Law Governing Lawyers Section 52",
        confidence=0.95,
        cross_references=["diligence_rule_1_3", "communication_rule_1_4", "malpractice_liability"],
        practice_tips=[
            "Document your research and preparation to defend against later incompetence claims",
            "Technology competence now includes understanding e-discovery, cybersecurity, and client data protection",
            "If a matter is outside your expertise, associate with experienced counsel or decline the engagement",
            "CLE requirements are jurisdiction-specific but competence is a continuous, self-assessed obligation",
        ],
        sanctions="Discipline ranges from private reprimand to suspension; repeated incompetence can result in disbarment",
        texas_notes="Texas Disciplinary Rule 1.01(a) parallels Model Rule 1.1; Texas Board of Disciplinary Appeals has imposed suspensions for pattern incompetence",
    ),
    DoctrineCacheBlock(
        topic="diligence_rule_1_3",
        category="client_lawyer_relationship",
        summary="ABA Model Rule 1.3 requires a lawyer to act with reasonable diligence and promptness in representing a client.",
        analysis="Model Rule 1.3 mandates diligence throughout the representation. Comment [1] states that a lawyer must pursue a matter despite opposition, obstruction, or personal inconvenience, and must take whatever lawful and ethical measures are required to vindicate the client's cause. Comment [2] addresses workload management: a lawyer's workload must be controlled so that each matter can be handled competently. Comment [3] addresses doubt about whether a client-lawyer relationship exists: the lawyer should clarify promptly. Neglect of client matters is the single most common basis for lawyer discipline nationwide. Neglect includes failure to file pleadings, failure to respond to discovery, failure to communicate, missing deadlines, and abandonment of the matter. Chronic neglect patterns often lead to suspension or disbarment. In re Hawkins (D.C. 2015) imposed a three-year suspension for chronic neglect of multiple matters.",
        authority="ABA Model Rule 1.3; ABA Model Rule 1.3 Comments [1]-[4]; In re Hawkins, 109 A.3d 1142 (D.C. 2015); Restatement (Third) Law Governing Lawyers Section 16(2)",
        keywords=["diligence", "rule 1.3", "promptness", "neglect", "workload", "deadlines", "abandonment"],
        rule_reference="Model Rule 1.3",
        confidence=0.94,
        cross_references=["competence_rule_1_1", "communication_rule_1_4"],
        practice_tips=[
            "Use calendaring and docketing systems to track all deadlines",
            "If you are overwhelmed, decline new matters rather than risk neglecting existing ones",
            "Respond to client inquiries within a reasonable time, typically 24-48 hours",
        ],
        sanctions="Neglect is the #1 basis for discipline; ranges from reprimand to disbarment for pattern conduct",
        texas_notes="Texas Disciplinary Rule 1.01(b)(1) specifically prohibits neglect; Texas imposes grievance sanctions heavily for neglect patterns",
    ),
    DoctrineCacheBlock(
        topic="communication_rule_1_4",
        category="client_lawyer_relationship",
        summary="ABA Model Rule 1.4 requires a lawyer to promptly inform the client of decisions requiring informed consent, reasonably consult about the means of achieving objectives, keep the client reasonably informed, and promptly comply with reasonable requests for information.",
        analysis="Model Rule 1.4(a) lists five specific communication duties: (1) promptly inform of circumstances requiring informed consent, (2) reasonably consult about means of achieving objectives, (3) keep client reasonably informed about status, (4) promptly comply with reasonable information requests, and (5) consult about relevant limitations on lawyer's conduct when client expects unlawful assistance. Rule 1.4(b) requires explanations sufficient for informed decision-making. The duty to communicate is measured by what a reasonable client would want to know. Failure to communicate is the most common client complaint to bar authorities. Settlement offers must always be communicated to the client (Rule 1.4(a)(1) and Rule 1.2(a)). Material developments, including adverse developments, must be communicated promptly. The duty continues even when there is nothing new to report; periodic status updates are required.",
        authority="ABA Model Rule 1.4; ABA Model Rule 1.2(a); Restatement (Third) Law Governing Lawyers Section 20",
        keywords=["communication", "rule 1.4", "inform client", "informed consent", "status updates", "settlement offers", "client complaints"],
        rule_reference="Model Rule 1.4",
        confidence=0.94,
        cross_references=["diligence_rule_1_3", "scope_of_representation_rule_1_2"],
        practice_tips=[
            "Always communicate settlement offers, no matter how unreasonable they seem",
            "Document all client communications in the file",
            "Set expectations at engagement about communication frequency and methods",
            "Send periodic status updates even when there is no material development",
        ],
        sanctions="Failure to communicate is a common basis for reprimands and short suspensions",
        texas_notes="Texas Disciplinary Rule 1.03 parallels Model Rule 1.4; Texas grievance statistics show communication failures as top complaint",
    ),

    # ---- FEES ----
    DoctrineCacheBlock(
        topic="fees_rule_1_5",
        category="client_lawyer_relationship",
        summary="ABA Model Rule 1.5 prohibits unreasonable fees and unreasonable amounts for expenses, sets requirements for contingent fee agreements, and restricts fee-splitting with lawyers in different firms.",
        analysis="Model Rule 1.5(a) lists eight factors for determining reasonableness: (1) time and labor, novelty, difficulty, and skill required, (2) likelihood the acceptance precludes other employment, (3) customary fee in the locality for similar services, (4) amount involved and results obtained, (5) time limitations imposed by client or circumstances, (6) nature and length of the professional relationship, (7) experience, reputation, and ability of the lawyer, and (8) whether the fee is fixed or contingent. Rule 1.5(b) requires the basis of the fee to be communicated to the client, preferably in writing, before or within a reasonable time after commencing representation. Rule 1.5(c) governs contingency fees: must be in writing, state the method of calculation including percentages, state litigation and other expenses to be deducted, and whether expenses are deducted before or after the contingency fee is calculated. Contingency fees are prohibited in domestic relations (for obtaining a divorce or property settlement) and criminal defense matters (Rule 1.5(d)). Rule 1.5(e) permits fee division between lawyers not in the same firm if: (1) the division is proportional to services performed or each lawyer assumes joint responsibility, (2) the client agrees in writing to the arrangement and the share each lawyer will receive, and (3) the total fee is reasonable. Brobeck, Phleger & Harrison v. Telex Corp. (9th Cir. 1979) upheld a $1M fee as reasonable given the stakes and complexity.",
        authority="ABA Model Rule 1.5; Brobeck, Phleger & Harrison v. Telex Corp., 602 F.2d 866 (9th Cir. 1979); Restatement (Third) Law Governing Lawyers Sections 34-47; In re Fordham, 668 N.E.2d 816 (Mass. 1996)",
        keywords=["fees", "rule 1.5", "reasonableness", "contingency fee", "fee splitting", "fee agreement", "hourly rate", "flat fee", "retainer"],
        rule_reference="Model Rule 1.5",
        restatement_reference="Restatement (Third) Law Governing Lawyers Sections 34-47",
        confidence=0.95,
        cross_references=["trust_accounts_iolta", "fee_reasonableness", "contingency_fees", "fee_splitting"],
        practice_tips=[
            "Always put fee agreements in writing, even when the rule only says 'preferably'",
            "Distinguish between 'true retainers' (nonrefundable fee for availability) and 'advance fee deposits' (refundable, drawn against as earned)",
            "Contingency fee agreements must be signed by the client and must state the method of calculation",
            "Fee disputes can be resolved through mandatory fee arbitration programs in many jurisdictions",
        ],
        sanctions="Excessive fees can result in disgorgement, discipline, and malpractice liability",
        texas_notes="Texas Disciplinary Rule 1.04 parallels Model Rule 1.5; Texas allows contingency fees in most civil matters but prohibits them in criminal and certain family law cases",
    ),

    # ---- CONFIDENTIALITY ----
    DoctrineCacheBlock(
        topic="confidentiality_rule_1_6",
        category="client_lawyer_relationship",
        summary="ABA Model Rule 1.6 prohibits a lawyer from revealing information relating to the representation of a client unless the client gives informed consent, the disclosure is impliedly authorized to carry out the representation, or an exception in Rule 1.6(b) applies.",
        analysis="Model Rule 1.6(a) establishes the bedrock duty of confidentiality. The scope is broader than the attorney-client privilege: it covers ALL information relating to the representation, regardless of source, not just confidential communications. Rule 1.6(b) permits (but does not require, except in a few states) disclosure to: (1) prevent reasonably certain death or substantial bodily harm, (2) prevent the client from committing a crime or fraud reasonably certain to result in substantial financial injury when the lawyer's services have been used, (3) prevent, mitigate, or rectify substantial financial injury from client crime/fraud using lawyer's services, (4) secure legal advice about lawyer's compliance with the Rules, (5) establish a claim or defense in a controversy between the lawyer and client, (6) comply with other law or a court order, and (7) detect and resolve conflicts of interest arising from the lawyer's change of employment (limited information only). The duty survives the termination of the representation and the death of the client. Swidler & Berlin v. United States (1998) confirmed that the privilege (and by extension the confidentiality duty) survives the client's death.",
        authority="ABA Model Rule 1.6; Swidler & Berlin v. United States, 524 U.S. 399 (1998); Restatement (Third) Law Governing Lawyers Sections 59-67",
        keywords=["confidentiality", "rule 1.6", "information relating to representation", "client secrets", "disclosure exceptions", "death or bodily harm", "crime fraud"],
        rule_reference="Model Rule 1.6",
        restatement_reference="Restatement (Third) Law Governing Lawyers Sections 59-67",
        confidence=0.96,
        cross_references=["attorney_client_privilege", "crime_fraud_exception", "conflicts_concurrent_rule_1_7"],
        practice_tips=[
            "Confidentiality under Rule 1.6 is BROADER than the attorney-client privilege: it covers all information 'relating to the representation' from any source",
            "Before disclosing under any exception, consider whether less-damaging alternatives exist",
            "Implement data security measures (encryption, access controls) to protect client information electronically",
            "When using cloud services or AI tools, ensure client data is protected from unauthorized access",
        ],
        sanctions="Unauthorized disclosure can result in discipline, malpractice liability, and disqualification",
        texas_notes="Texas Disciplinary Rule 1.05 is structured differently but covers similar ground; Texas has a mandatory disclosure requirement for reasonably certain death or substantial bodily harm",
    ),

    # ---- CONFLICTS OF INTEREST ----
    DoctrineCacheBlock(
        topic="conflicts_concurrent_rule_1_7",
        category="conflicts_of_interest",
        summary="ABA Model Rule 1.7 prohibits representation of a client if there is a concurrent conflict of interest: a direct adversity between clients or a significant risk that the representation will be materially limited by the lawyer's responsibilities to another client, a former client, a third person, or the lawyer's own interests.",
        analysis="Model Rule 1.7(a) defines two types of concurrent conflicts: (1) direct adversity (representing opposing parties) and (2) material limitation (lawyer's duties to another client, third person, or own interests significantly risk limiting the representation). Rule 1.7(b) permits representation despite a concurrent conflict if: (1) the lawyer reasonably believes competent and diligent representation of each affected client is possible, (2) the representation is not prohibited by law, (3) the representation does not involve asserting a claim by one client against another in the same litigation or proceeding before a tribunal, and (4) each affected client gives informed consent, confirmed in writing. Informed consent requires the lawyer to explain the risks of common representation, including the risk that the conflict may require withdrawal from one or all representations. Some conflicts are nonconsentable: when the lawyer cannot reasonably believe competent representation is possible (such as representing both sides in the same litigation). Fiandaca v. Cunningham (1st Cir. 1987) disqualified counsel for simultaneous conflict. The 'hot potato' doctrine (Picker Int'l v. Varian Assocs.) prevents a firm from dropping a current client to avoid a conflict.",
        authority="ABA Model Rule 1.7; Fiandaca v. Cunningham, 827 F.2d 825 (1st Cir. 1987); Picker Int'l v. Varian Assocs., 670 F. Supp. 1363 (N.D. Ohio 1987); Restatement (Third) Law Governing Lawyers Sections 121-122, 128-131",
        keywords=["conflicts", "rule 1.7", "concurrent conflict", "direct adversity", "material limitation", "informed consent", "nonconsentable", "hot potato", "multiple clients"],
        rule_reference="Model Rule 1.7",
        restatement_reference="Restatement (Third) Law Governing Lawyers Sections 121-122, 128-131",
        confidence=0.96,
        cross_references=["conflicts_former_client_rule_1_9", "imputed_conflicts_rule_1_10", "organization_as_client_rule_1_13"],
        practice_tips=[
            "Screen for conflicts at intake before any substantive discussion",
            "Maintain a comprehensive conflict-checking database covering all clients, adverse parties, and related entities",
            "Conflict waivers must be specific about the nature of the conflict and the risks; boilerplate advance waivers may not be enforceable",
            "The 'hot potato' rule means you cannot drop a current client to take on a more lucrative matter",
        ],
        sanctions="Disqualification from representation; discipline including suspension; malpractice liability for damages resulting from the conflict",
        texas_notes="Texas Disciplinary Rule 1.06 parallels Model Rule 1.7; Texas courts frequently address conflicts in oil and gas litigation where law firms represent multiple operators",
    ),
    DoctrineCacheBlock(
        topic="conflicts_former_client_rule_1_9",
        category="conflicts_of_interest",
        summary="ABA Model Rule 1.9 restricts a lawyer's ability to represent a new client whose interests are materially adverse to a former client in the same or a substantially related matter, unless the former client gives informed consent confirmed in writing.",
        analysis="Model Rule 1.9(a) prohibits representation adverse to a former client in the 'same or a substantially related matter' unless the former client consents. 'Substantially related' means: (1) the matters involve the same transaction or legal dispute, or (2) there is a substantial risk that confidential factual information obtained in the prior representation would materially advance the new client's position (Restatement Section 132). Rule 1.9(b) addresses lateral lawyers: a lawyer shall not represent a person in the same or substantially related matter adversely to someone who was a client of the lawyer's former firm, if the lawyer acquired material confidential information about that person. Rule 1.9(c) prohibits using or revealing confidential information relating to the prior representation. The test is whether a reasonable lawyer would conclude there is a substantial risk that work done on the prior matter gave the lawyer information that could be used against the former client. Analytica, Inc. v. NPD Research, Inc. (7th Cir. 1983) established the 'substantial relationship' test for successive conflicts. Courts use a three-part inquiry: (1) factual reconstruction of the scope of the prior representation, (2) whether it is reasonable to infer that confidential information was disclosed, and (3) whether that information is relevant to the current matter.",
        authority="ABA Model Rule 1.9; Analytica, Inc. v. NPD Research, Inc., 708 F.2d 1263 (7th Cir. 1983); Restatement (Third) Law Governing Lawyers Sections 132-133",
        keywords=["former client", "rule 1.9", "successive conflict", "substantially related", "confidential information", "lateral movement", "prior representation"],
        rule_reference="Model Rule 1.9",
        restatement_reference="Restatement (Third) Law Governing Lawyers Sections 132-133",
        confidence=0.95,
        cross_references=["conflicts_concurrent_rule_1_7", "imputed_conflicts_rule_1_10", "confidentiality_rule_1_6"],
        practice_tips=[
            "When a lawyer moves between firms, conduct a thorough conflicts check of all the lawyer's former matters",
            "Document the scope of prior representations to establish boundaries for the 'substantially related' test",
            "Informed consent from the former client must be confirmed in writing",
            "Lateral hires create significant conflict exposure for the new firm under imputation rules",
        ],
        sanctions="Disqualification of the firm; discipline; malpractice for breach of fiduciary duty to former client",
        texas_notes="Texas Disciplinary Rule 1.09 parallels Model Rule 1.9; Texas courts apply the 'substantial relationship' test consistent with federal precedent",
    ),
    DoctrineCacheBlock(
        topic="imputed_conflicts_rule_1_10",
        category="conflicts_of_interest",
        summary="ABA Model Rule 1.10 imputes one lawyer's conflicts of interest to all lawyers in the same firm, with a screening exception for lateral moves in most jurisdictions.",
        analysis="Model Rule 1.10(a) provides that when a lawyer is disqualified from representing a client under Rules 1.7 or 1.9, no other lawyer in the same firm may undertake that representation, with two exceptions: (1) the prohibition is based on a personal interest of the disqualified lawyer and does not present a significant risk of materially limiting the representation (Rule 1.10(a)(1)), and (2) the prohibition is based on Rule 1.9(a) or (b) and the disqualified lawyer is timely screened, receives no fee from the matter, and written notice is given to the affected former client (Rule 1.10(a)(2)). The screening provision (sometimes called an 'ethical wall' or 'Chinese wall') was added in the 2009 amendments and is controversial: some jurisdictions have not adopted it. Screening must be timely implemented and documented. Rule 1.10(b) addresses departed lawyers: when a lawyer leaves a firm, the firm may continue the representation unless any remaining lawyer has material confidential information. Rule 1.10(c) permits representation if written informed consent is obtained from the affected client. The 'firm' includes legal aid offices, corporate law departments, and legal services organizations. Kirk v. First American Title Ins. Co. (5th Cir. 2009) upheld screening when implemented immediately and thoroughly documented.",
        authority="ABA Model Rule 1.10; Kirk v. First American Title Ins. Co., 183 F.3d 776 (5th Cir. 2009); Restatement (Third) Law Governing Lawyers Section 123-124",
        keywords=["imputed conflicts", "rule 1.10", "imputation", "ethical wall", "screening", "chinese wall", "lateral movement", "firm conflict"],
        rule_reference="Model Rule 1.10",
        restatement_reference="Restatement (Third) Law Governing Lawyers Section 123-124",
        confidence=0.93,
        cross_references=["conflicts_concurrent_rule_1_7", "conflicts_former_client_rule_1_9", "government_officers_rule_1_11"],
        practice_tips=[
            "Implement screening procedures immediately upon learning of a potential conflict from a lateral hire",
            "Document the screening: who was screened, what access was restricted, what information was walled off",
            "Not all jurisdictions recognize the screening exception for lateral hires; check local rules",
            "Provide timely written notice to the affected former client as required by Rule 1.10(a)(2)",
        ],
        sanctions="Disqualification of the entire firm; discipline for the lawyer and potentially the supervising partner",
        texas_notes="Texas Disciplinary Rule 1.09(b) addresses imputation; Texas permits screening in limited circumstances consistent with the 2009 Model Rule amendments",
    ),

    # ---- ATTORNEY-CLIENT PRIVILEGE ----
    DoctrineCacheBlock(
        topic="attorney_client_privilege",
        category="privilege",
        summary="The attorney-client privilege protects confidential communications between a client and attorney made for the purpose of seeking or providing legal advice. It is the oldest common-law privilege.",
        analysis="The attorney-client privilege protects: (1) a communication, (2) made between privileged persons (client, attorney, agents of either), (3) in confidence, (4) for the purpose of obtaining or providing legal assistance. The privilege belongs to the client, not the attorney. It is absolute (unlike work product, which is qualified) once established, meaning the court cannot override it based on the adversary's need. Key limitations: (1) the privilege does not protect underlying facts, only communications about those facts (Upjohn Co. v. United States, 449 U.S. 383 (1981)), (2) communications made in furtherance of a crime or fraud are not protected (the crime-fraud exception), (3) the privilege can be waived by voluntary disclosure (including inadvertent disclosure under FRE 502), (4) the privilege does not apply when the client's communication was made for purposes other than obtaining legal advice (e.g., business advice). The privilege survives the termination of the attorney-client relationship and the death of the client (Swidler & Berlin v. United States, 524 U.S. 399 (1998)). In the corporate context, the Upjohn decision established that the privilege extends to communications between corporate counsel and corporate employees at all levels, not just the 'control group.'",
        authority="Upjohn Co. v. United States, 449 U.S. 383 (1981); Swidler & Berlin v. United States, 524 U.S. 399 (1998); FRE 501; Restatement (Third) Law Governing Lawyers Sections 68-86",
        keywords=["attorney-client privilege", "privileged communication", "confidential communication", "legal advice", "waiver", "upjohn", "control group", "corporate privilege"],
        rule_reference="FRE 501; Common Law",
        restatement_reference="Restatement (Third) Law Governing Lawyers Sections 68-86",
        confidence=0.96,
        cross_references=["upjohn_corporate_privilege", "crime_fraud_exception", "work_product_doctrine", "confidentiality_rule_1_6"],
        practice_tips=[
            "Label communications as 'privileged and confidential' — though labeling alone does not create privilege",
            "Distinguish between legal advice (privileged) and business advice (not privileged) in dual-purpose communications",
            "Be cautious about forwarding privileged communications to third parties, which can waive the privilege",
            "FRE 502(b) provides protection for inadvertent disclosure if reasonable precautions were taken",
        ],
        sanctions="Breach of the privilege by the attorney can result in discipline, malpractice, and disqualification",
    ),
    DoctrineCacheBlock(
        topic="upjohn_corporate_privilege",
        category="privilege",
        summary="Upjohn Co. v. United States (1981) established that the attorney-client privilege in the corporate setting extends to communications between corporate counsel and employees at all levels of the organization, not just the 'control group.'",
        analysis="In Upjohn Co. v. United States, 449 U.S. 383 (1981), the Supreme Court rejected the 'control group' test used by the Sixth Circuit and held that the attorney-client privilege applies to communications between corporate counsel and lower-level employees. The Court reasoned that (1) the control group test makes the privilege unpredictable, (2) middle and lower-level employees often possess the most relevant information, and (3) the purpose of the privilege — encouraging full and frank communication — requires protecting these communications. The Upjohn framework requires: (a) the communications were made by corporate employees to corporate counsel, (b) at the direction of corporate superiors, (c) to secure legal advice, (d) concerning matters within the scope of the employees' duties, and (e) the employees were aware they were being questioned so the corporation could obtain legal advice. The privilege belongs to the corporation, not the individual employees. The board of directors or authorized management can waive the privilege. In derivative actions, the Garner v. Wolfinbarger 'fiduciary exception' may permit shareholders to access privileged communications under certain circumstances.",
        authority="Upjohn Co. v. United States, 449 U.S. 383 (1981); Garner v. Wolfinbarger, 430 F.2d 1093 (5th Cir. 1970); Restatement (Third) Law Governing Lawyers Section 73",
        keywords=["upjohn", "corporate privilege", "control group", "employee communications", "corporate counsel", "internal investigation", "garner exception", "fiduciary exception"],
        rule_reference="Upjohn Co. v. United States, 449 U.S. 383 (1981)",
        restatement_reference="Restatement (Third) Law Governing Lawyers Section 73",
        confidence=0.95,
        cross_references=["attorney_client_privilege", "organization_as_client_rule_1_13", "crime_fraud_exception"],
        practice_tips=[
            "Issue 'Upjohn warnings' (also called 'corporate Miranda') to employees at the start of an internal investigation: you represent the corporation, not the individual",
            "Document that the investigation is being conducted for the purpose of obtaining legal advice",
            "Be aware of the Garner fiduciary exception in shareholder derivative litigation",
            "In government investigations, consider the implications of waiving privilege under DOJ cooperation credit policies",
        ],
    ),
    DoctrineCacheBlock(
        topic="crime_fraud_exception",
        category="privilege",
        summary="The crime-fraud exception provides that the attorney-client privilege does not protect communications made in furtherance of a crime or fraud, regardless of whether the attorney was aware of the client's unlawful purpose.",
        analysis="The crime-fraud exception, recognized in Clark v. United States, 289 U.S. 1 (1933) and codified in many jurisdictions, strips privilege protection from communications made for the purpose of furthering a crime or fraud. The party seeking to invoke the exception must establish a prima facie case: (1) the client was engaged in or planning criminal or fraudulent conduct, and (2) the attorney-client communication was in furtherance of that conduct. Under United States v. Zolin, 491 U.S. 554 (1989), the court may conduct an in camera review of the communications to determine whether the exception applies, but the party seeking access must first present a factual basis adequate to support a good faith belief that in camera review will establish the exception. The exception applies even if the attorney was unaware of the client's criminal or fraudulent purpose. It covers both ongoing and contemplated crimes/fraud, but does not apply to past crimes that the client is seeking legal advice about defending. The exception has been applied to tax fraud schemes, corporate fraud, and obstruction of justice. In re Grand Jury Subpoena (Sealed Case) (D.C. Cir. 2005) applied the crime-fraud exception to strip privilege from communications between a target and counsel regarding document destruction.",
        authority="Clark v. United States, 289 U.S. 1 (1933); United States v. Zolin, 491 U.S. 554 (1989); In re Grand Jury Subpoena (Sealed Case), 415 F.3d 333 (4th Cir. 2005); Restatement (Third) Law Governing Lawyers Section 82",
        keywords=["crime-fraud exception", "privilege exception", "furtherance of crime", "in camera review", "zolin", "prima facie", "ongoing crime", "fraud"],
        rule_reference="Common Law; FRE 501; Zolin, 491 U.S. 554",
        restatement_reference="Restatement (Third) Law Governing Lawyers Section 82",
        confidence=0.95,
        cross_references=["attorney_client_privilege", "upjohn_corporate_privilege", "work_product_doctrine"],
        practice_tips=[
            "If a client reveals an intent to commit a future crime or fraud, do not assist and consider your obligations under Rule 1.6(b) and Rule 1.13(c)",
            "The exception requires the communication be IN FURTHERANCE of the crime/fraud; simply discussing past illegal conduct to mount a defense is not covered",
            "Be prepared for in camera review of disputed communications; the judge reviews the actual documents",
        ],
    ),

    # ---- WORK PRODUCT DOCTRINE ----
    DoctrineCacheBlock(
        topic="work_product_doctrine",
        category="privilege",
        summary="The work product doctrine, established in Hickman v. Taylor (1947) and codified in FRCP 26(b)(3), protects materials prepared by an attorney in anticipation of litigation from discovery, subject to a showing of substantial need and undue hardship for fact work product, with near-absolute protection for opinion work product.",
        analysis="The work product doctrine protects documents and tangible things prepared in anticipation of litigation or for trial by a party or its representative (including attorney, consultant, agent). Hickman v. Taylor, 329 U.S. 495 (1947) established the common law doctrine. FRCP 26(b)(3) codified it: (A) ordinary/fact work product may be discovered if the requesting party shows substantial need and inability to obtain the substantial equivalent without undue hardship; (B) opinion work product (mental impressions, conclusions, opinions, legal theories) receives near-absolute protection — courts must protect against disclosure even when fact work product is ordered produced. The doctrine differs from the attorney-client privilege: (1) it protects documents, not just communications, (2) it can be overcome by a showing of need, (3) it is not limited to communications with the client, (4) it extends to non-attorney representatives. The 'anticipation of litigation' trigger requires that the primary motivating purpose for creating the document was to aid in possible future litigation (United States v. Adlman, 68 F.3d 1495 (2d Cir. 1995), applying the 'because of' test). Dual-purpose documents are analyzed under the primary motivation test in most circuits. The crime-fraud exception also applies to work product.",
        authority="Hickman v. Taylor, 329 U.S. 495 (1947); FRCP 26(b)(3); United States v. Adlman, 134 F.3d 1194 (2d Cir. 1998); Restatement (Third) Law Governing Lawyers Sections 87-93",
        keywords=["work product", "hickman", "anticipation of litigation", "opinion work product", "fact work product", "substantial need", "frcp 26", "trial preparation"],
        rule_reference="FRCP 26(b)(3); Hickman v. Taylor, 329 U.S. 495",
        restatement_reference="Restatement (Third) Law Governing Lawyers Sections 87-93",
        confidence=0.95,
        cross_references=["attorney_client_privilege", "crime_fraud_exception"],
        practice_tips=[
            "Label work product documents as 'Attorney Work Product — Privileged' to preserve the protection",
            "Distinguish between fact work product (qualified protection) and opinion work product (near-absolute protection)",
            "The 'anticipation of litigation' test requires litigation to be at least reasonably anticipated, not merely a possibility",
            "Work product protection is not waived by disclosure to persons who share a common interest in the litigation",
        ],
    ),

    # ---- TRUST ACCOUNTS / IOLTA ----
    DoctrineCacheBlock(
        topic="trust_accounts_iolta",
        category="fiduciary",
        summary="ABA Model Rule 1.15 requires lawyers to safeguard client property, including funds, in trust accounts separate from the lawyer's own funds. IOLTA (Interest on Lawyers' Trust Accounts) programs fund legal services from interest on pooled client trust accounts.",
        analysis="Model Rule 1.15 requires: (1) client funds must be held in a separate account (the 'trust account' or 'IOLTA account'), (2) the lawyer must maintain complete records of trust account funds for five years (or longer per jurisdiction), (3) client and third-party funds must be kept separate from the lawyer's own funds (no 'commingling'), (4) the lawyer must promptly deliver any funds or property the client is entitled to receive, and (5) when there is a dispute about funds, the undisputed portion must be delivered and the disputed portion held in trust until the dispute is resolved. IOLTA programs pool small or short-term client deposits in a single interest-bearing account, with the interest funding legal aid. The Supreme Court upheld IOLTA programs against Takings Clause challenges in Brown v. Legal Foundation of Washington, 538 U.S. 216 (2003). Trust account violations — commingling, conversion, failure to maintain records — are among the most serious disciplinary offenses and frequently result in disbarment. Even inadvertent commingling (depositing personal funds into the trust account) is a violation, though sanctions for inadvertent commingling are less severe.",
        authority="ABA Model Rule 1.15; Brown v. Legal Foundation of Washington, 538 U.S. 216 (2003); Restatement (Third) Law Governing Lawyers Section 44",
        keywords=["trust account", "iolta", "rule 1.15", "client funds", "commingling", "conversion", "safekeeping", "fiduciary", "escrow"],
        rule_reference="Model Rule 1.15",
        restatement_reference="Restatement (Third) Law Governing Lawyers Section 44",
        confidence=0.95,
        cross_references=["fiduciary_duties", "fees_rule_1_5", "lawyer_discipline_sanctions"],
        practice_tips=[
            "Never commingle personal funds with client trust funds — not even temporarily",
            "Maintain meticulous trust account records: ledgers, bank statements, reconciliations",
            "Transfer earned fees from trust to operating account promptly after they are earned",
            "Random trust account audits are conducted by many state bars; be audit-ready at all times",
        ],
        sanctions="Trust account violations (especially conversion) frequently result in disbarment; commingling typically results in suspension",
        texas_notes="Texas Disciplinary Rule 1.14 governs trust accounts; the State Bar of Texas Client Security Fund covers losses from trust account misappropriation; IOLTA administered by the Texas Access to Justice Foundation",
    ),

    # ---- ORGANIZATION AS CLIENT / DIMINISHED CAPACITY ----
    DoctrineCacheBlock(
        topic="organization_as_client_rule_1_13",
        category="client_lawyer_relationship",
        summary="ABA Model Rule 1.13 provides that a lawyer employed or retained by an organization represents the organization acting through its duly authorized constituents, not any individual officer, director, or employee.",
        analysis="Model Rule 1.13(a) establishes that the organization is the client. Rule 1.13(b) imposes an 'up the ladder' reporting obligation: when a lawyer knows that an officer, employee, or other person associated with the organization is engaged in action or intends to act in a way that is a violation of law reasonably imputable to the organization and is likely to result in substantial injury to the organization, the lawyer must refer the matter to higher authority in the organization, including if necessary the highest authority that can act on behalf of the organization (typically the board of directors). Rule 1.13(c) permits (but does not require, except under SOX) the lawyer to report outside the organization if the highest authority fails to act and the lawyer reasonably believes the violation is reasonably certain to result in substantial injury to the organization. This is the 'reporting out' provision. Rule 1.13(f) requires 'Upjohn warnings' when the organization's interests are adverse to a constituent: the lawyer must explain that the organization is the client and that the constituent may wish to obtain separate counsel. The Sarbanes-Oxley Act Section 307 and SEC Rule 205 impose mandatory 'up the ladder' reporting obligations on attorneys appearing before the SEC.",
        authority="ABA Model Rule 1.13; Sarbanes-Oxley Act Section 307; 17 CFR Part 205; In re Carter and Johnson, SEC Release No. 34-17597 (1981)",
        keywords=["organization as client", "rule 1.13", "corporate counsel", "up the ladder", "reporting out", "upjohn warning", "corporate miranda", "board of directors", "sarbanes-oxley"],
        rule_reference="Model Rule 1.13",
        confidence=0.94,
        cross_references=["upjohn_corporate_privilege", "sarbanes_oxley_sec_205", "confidentiality_rule_1_6"],
        practice_tips=[
            "Always give 'Upjohn warnings' / 'corporate Miranda' when interviewing employees in an internal investigation",
            "Document the 'up the ladder' reporting chain if a constituent is engaging in potentially illegal conduct",
            "Understand that the organization — not any individual — is your client, even when individuals direct your work",
            "SOX Section 205 creates separate, mandatory reporting obligations for securities lawyers",
        ],
    ),
    DoctrineCacheBlock(
        topic="diminished_capacity_rule_1_14",
        category="client_lawyer_relationship",
        summary="ABA Model Rule 1.14 addresses the lawyer's obligations when a client's capacity to make adequately considered decisions is diminished, whether because of minority, mental impairment, or other cause.",
        analysis="Model Rule 1.14(a) instructs the lawyer to maintain a normal client-lawyer relationship with a client whose decision-making capacity is diminished, as far as reasonably possible. Rule 1.14(b) permits protective action when the lawyer reasonably believes the client is at risk of substantial harm: the lawyer may consult with individuals or entities that have the ability to take action to protect the client, including family members, adult protective services, or other appropriate agencies. Rule 1.14(c) provides that information about the client's diminished capacity is protected under Rule 1.6 but the lawyer is impliedly authorized to make disclosures necessary to carry out the protective action. The lawyer must consider: (1) the client's wishes and values, (2) the client's best interests, (3) the least restrictive action, and (4) maximizing client autonomy. In extreme cases, the lawyer may seek appointment of a guardian or conservator. Comment [5] recognizes that capacity can fluctuate and the lawyer should be cautious about overriding client autonomy. The lawyer cannot simply substitute their judgment for the client's.",
        authority="ABA Model Rule 1.14; ABA Formal Opinion 96-404; Restatement (Third) Law Governing Lawyers Section 24",
        keywords=["diminished capacity", "rule 1.14", "incapacity", "protective action", "guardian", "conservator", "elderly client", "minor client", "mental impairment"],
        rule_reference="Model Rule 1.14",
        restatement_reference="Restatement (Third) Law Governing Lawyers Section 24",
        confidence=0.92,
        cross_references=["confidentiality_rule_1_6", "competence_rule_1_1"],
        practice_tips=[
            "Document observations supporting your assessment of diminished capacity",
            "Protective action should be the least restrictive available and should maximize client autonomy",
            "Consult with other professionals (social workers, physicians) when assessing capacity",
            "Appointment of a guardian is a last resort, not a first response",
        ],
    ),

    # ---- PROSECUTORIAL ETHICS / BRADY ----
    DoctrineCacheBlock(
        topic="prosecutorial_duties_rule_3_8",
        category="advocate",
        summary="ABA Model Rule 3.8 imposes special responsibilities on prosecutors, including the obligation to disclose exculpatory evidence, refrain from prosecuting charges not supported by probable cause, and provide timely disclosure of evidence tending to negate guilt or mitigate punishment.",
        analysis="Model Rule 3.8 imposes heightened duties on prosecutors reflecting their dual role as advocates and ministers of justice. Key provisions: (a) no charges without probable cause, (b) reasonable efforts to assure the accused has been advised of the right to counsel, (c) no extrajudicial statements that heighten public condemnation beyond the public record, (d) timely disclosure to the defense of all evidence or information known to the prosecutor that tends to negate the guilt of the accused or mitigates the offense (broader than Brady), (f) if the prosecutor knows of new, credible, and material evidence creating a reasonable likelihood that a convicted defendant did not commit the offense, must promptly disclose to the defendant and to the court or appropriate authority, and (g) if clear and convincing evidence establishes actual innocence, must seek to remedy the conviction. The Brady v. Maryland obligation (due process) is constitutional: the prosecution must disclose evidence favorable to the accused that is material to guilt or punishment. Brady violations can result in reversal of convictions, disciplinary proceedings, and civil liability under 42 USC 1983. Connick v. Thompson (2011) addressed municipal liability for Brady violations.",
        authority="ABA Model Rule 3.8; Brady v. Maryland, 373 U.S. 83 (1963); Giglio v. United States, 405 U.S. 150 (1972); Connick v. Thompson, 563 U.S. 51 (2011); Berger v. United States, 295 U.S. 78 (1935)",
        keywords=["prosecutorial ethics", "rule 3.8", "brady", "exculpatory evidence", "disclosure", "probable cause", "minister of justice", "giglio", "impeachment evidence"],
        rule_reference="Model Rule 3.8",
        confidence=0.95,
        cross_references=["candor_toward_tribunal_rule_3_3", "confidentiality_rule_1_6"],
        practice_tips=[
            "Brady disclosure obligations extend to evidence in the possession of police and other government agents, not just the prosecutor's file",
            "Impeachment evidence (Giglio material) is a subset of Brady and must also be disclosed",
            "Model Rule 3.8(d) is broader than the constitutional Brady obligation and applies to all 'evidence or information' tending to negate guilt",
            "Post-conviction disclosure duties under Rule 3.8(g)-(h) are distinct from the trial-stage Brady obligation",
        ],
    ),
    DoctrineCacheBlock(
        topic="brady_obligations",
        category="constitutional",
        summary="Brady v. Maryland (1963) holds that the prosecution violates due process by suppressing evidence favorable to the accused that is material to guilt or punishment, regardless of the prosecution's good or bad faith.",
        analysis="Brady v. Maryland, 373 U.S. 83 (1963) established the constitutional obligation to disclose exculpatory evidence. The three elements of a Brady violation are: (1) the evidence at issue must be favorable to the accused, either because it is exculpatory or impeaching (Giglio v. United States, 405 U.S. 150 (1972)), (2) the evidence must have been suppressed by the State, either willfully or inadvertently, and (3) prejudice must have resulted — the evidence is 'material' if there is a reasonable probability that the outcome would have been different had the evidence been disclosed (United States v. Bagley, 473 U.S. 667 (1985)). Materiality is assessed cumulatively across all suppressed evidence (Kyles v. Whitley, 514 U.S. 419 (1995)). The duty extends to evidence known to the prosecution team, including law enforcement. A prosecutor has a duty to learn of favorable evidence known to others acting on the government's behalf (Strickler v. Greene, 527 U.S. 263 (1999)). Remedies include new trial, reversal of conviction, and in egregious cases, dismissal with prejudice.",
        authority="Brady v. Maryland, 373 U.S. 83 (1963); Giglio v. United States, 405 U.S. 150 (1972); United States v. Bagley, 473 U.S. 667 (1985); Kyles v. Whitley, 514 U.S. 419 (1995); Strickler v. Greene, 527 U.S. 263 (1999)",
        keywords=["brady", "exculpatory", "material evidence", "suppression", "due process", "giglio", "impeachment", "materiality", "prosecution team"],
        rule_reference="Brady v. Maryland, 373 U.S. 83 (1963)",
        confidence=0.96,
        cross_references=["prosecutorial_duties_rule_3_8", "candor_toward_tribunal_rule_3_3"],
    ),

    # ---- CANDOR TOWARD TRIBUNAL ----
    DoctrineCacheBlock(
        topic="candor_toward_tribunal_rule_3_3",
        category="advocate",
        summary="ABA Model Rule 3.3 prohibits a lawyer from knowingly making a false statement of fact or law to a tribunal, failing to correct a false statement of material fact or law previously made, or offering evidence the lawyer knows to be false.",
        analysis="Model Rule 3.3(a)(1) prohibits knowingly making false statements of fact or law to a tribunal. Rule 3.3(a)(2) requires disclosure of directly adverse legal authority in the controlling jurisdiction not disclosed by opposing counsel. Rule 3.3(a)(3) prohibits offering evidence the lawyer knows to be false; if a lawyer has offered material evidence and later learns it was false, the lawyer must take reasonable remedial measures, including, if necessary, disclosure to the tribunal. Rule 3.3(b) extends these duties to ex parte proceedings, requiring disclosure of all material facts to enable the tribunal to make an informed decision. Rule 3.3(c) establishes that duties under this Rule apply even if compliance requires disclosure of information otherwise protected by Rule 1.6 (confidentiality), making this one of the few situations where the duty to the tribunal overrides client confidentiality. The 'knowledge' standard requires actual knowledge, not merely suspicion. Nix v. Whiteside, 475 U.S. 157 (1986) held that counsel may refuse to present testimony the lawyer knows is perjured. In re Ryder (E.D. Va. 1967) demonstrates that concealing physical evidence from a tribunal violates the duty of candor.",
        authority="ABA Model Rule 3.3; Nix v. Whiteside, 475 U.S. 157 (1986); In re Ryder, 263 F. Supp. 360 (E.D. Va. 1967); Restatement (Third) Law Governing Lawyers Sections 111, 120",
        keywords=["candor", "rule 3.3", "tribunal", "false statement", "adverse authority", "false evidence", "perjury", "remedial measures", "ex parte"],
        rule_reference="Model Rule 3.3",
        restatement_reference="Restatement (Third) Law Governing Lawyers Sections 111, 120",
        confidence=0.95,
        cross_references=["confidentiality_rule_1_6", "prosecutorial_duties_rule_3_8", "truthfulness_rule_4_1"],
        practice_tips=[
            "The duty to disclose adverse authority is limited to the controlling jurisdiction",
            "If a client intends to testify falsely, counsel must attempt to dissuade; if unsuccessful, the lawyer may be required to take remedial measures including disclosure to the tribunal",
            "Duties under Rule 3.3 override Rule 1.6 confidentiality — this is a critical hierarchy to understand",
        ],
    ),

    # ---- ADVERTISING / SOLICITATION ----
    DoctrineCacheBlock(
        topic="advertising_rule_7_1",
        category="information_about_services",
        summary="ABA Model Rule 7.1 prohibits a lawyer from making false or misleading communications about the lawyer or the lawyer's services. A communication is false or misleading if it contains a material misrepresentation of fact or law, or omits a fact necessary to make the statement not misleading.",
        analysis="Model Rule 7.1 is the foundational advertising rule. It prohibits any false or misleading communication about the lawyer or the lawyer's services. A communication is misleading if it: (1) contains a material misrepresentation of fact or law, (2) omits a fact necessary to make the statement not materially misleading, (3) is likely to create an unjustified expectation about results the lawyer can achieve, or (4) compares the lawyer's services with other lawyers' services unless factually substantiated. The First Amendment protects truthful, non-misleading lawyer advertising (Bates v. State Bar of Arizona, 433 U.S. 350 (1977)). States may regulate misleading advertising and may require disclaimers. The 2018 Model Rule amendments simplified the advertising rules by collapsing former Rules 7.1-7.5 into fewer provisions and eliminating many outdated restrictions. Client testimonials, past results, and certifications may be used if accompanied by appropriate disclaimers. Online and social media advertising is subject to the same rules. In re Anonymous (Ind. 2021) imposed discipline for misleading social media advertising claiming '100% success rate.'",
        authority="ABA Model Rule 7.1 (2018 amended); Bates v. State Bar of Arizona, 433 U.S. 350 (1977); Peel v. Attorney Registration and Disciplinary Comm'n, 496 U.S. 91 (1990)",
        keywords=["advertising", "rule 7.1", "false or misleading", "lawyer advertising", "bates", "first amendment", "testimonials", "results", "social media advertising"],
        rule_reference="Model Rule 7.1",
        confidence=0.93,
        cross_references=["solicitation_rule_7_2", "social_media_ethics"],
        practice_tips=[
            "All lawyer advertising must be truthful and not misleading — this is the touchstone",
            "Past results disclaimers ('results may vary') should accompany case result references",
            "Social media profiles and posts are 'communications' subject to Rule 7.1",
            "Avoid superlatives ('best lawyer', '#1 firm') unless factually verifiable",
        ],
        texas_notes="Texas Disciplinary Rules Part VII governs lawyer advertising with specific requirements for disclaimers and pre-screening in some circumstances; Texas is stricter than the Model Rules on solicitation",
    ),
    DoctrineCacheBlock(
        topic="solicitation_rule_7_2",
        category="information_about_services",
        summary="ABA Model Rule 7.3 (renumbered in 2018 amendments) restricts in-person, live telephone, and real-time electronic solicitation of prospective clients when a significant motive is the lawyer's pecuniary gain, unless the person is a lawyer, has a family/close personal/prior professional relationship with the lawyer, or the person is not known to need legal services.",
        analysis="The ABA distinguishes between advertising (general communications to the public) and solicitation (targeted, real-time contact with a specific prospective client). Under Model Rule 7.3 (post-2018), in-person, live telephone, and real-time electronic solicitation is prohibited when the lawyer's significant motive is pecuniary gain, with exceptions for lawyers, family/close personal relationships, and prior professional relationships. Written, recorded, or electronic communications to persons known to need legal services are permitted but must include 'Advertising Material' on the envelope and at the beginning and end of any recorded or electronic communication. The rationale for restricting live solicitation is the potential for overreaching, undue influence, and intimidation (Ohralik v. Ohio State Bar Ass'n, 436 U.S. 447 (1978)). In contrast, Shapero v. Kentucky Bar Ass'n (1988) held that targeted written solicitation is protected by the First Amendment. The Florida Bar v. Went For It (1995) upheld a 30-day waiting period for written solicitation of accident victims. Group legal services and prepaid plans may use solicitation methods not available to private practitioners (In re Primus, 436 U.S. 412 (1978)).",
        authority="ABA Model Rule 7.3; Ohralik v. Ohio State Bar Ass'n, 436 U.S. 447 (1978); In re Primus, 436 U.S. 412 (1978); Shapero v. Kentucky Bar Ass'n, 486 U.S. 466 (1988); Florida Bar v. Went For It, 515 U.S. 618 (1995)",
        keywords=["solicitation", "rule 7.3", "in-person contact", "ambulance chasing", "barratry", "ohralik", "targeted mail", "advertising material"],
        rule_reference="Model Rule 7.3",
        confidence=0.93,
        cross_references=["advertising_rule_7_1"],
        practice_tips=[
            "Never solicit clients in person at hospitals, accident scenes, or funeral homes",
            "Written solicitation must include 'Advertising Material' designation",
            "Many states have waiting periods before targeted solicitation of accident victims",
            "Referral fees to non-lawyers (runners, cappers) are prohibited in virtually all jurisdictions",
        ],
        texas_notes="Texas prohibits barratry (Penal Code Section 38.12) and has aggressive enforcement against runners and cappers; Texas Disciplinary Rule 7.03 restricts solicitation",
    ),

    # ---- UNAUTHORIZED PRACTICE / MULTIJURISDICTIONAL PRACTICE ----
    DoctrineCacheBlock(
        topic="unauthorized_practice_rule_5_5",
        category="law_firms_and_associations",
        summary="ABA Model Rule 5.5 prohibits a lawyer from practicing law in a jurisdiction in violation of the regulation of the legal profession in that jurisdiction, or assisting another in doing so. It also establishes 'safe harbors' for temporary multijurisdictional practice.",
        analysis="Model Rule 5.5(a) prohibits unauthorized practice of law (UPL): a lawyer shall not practice in a jurisdiction in violation of its regulation, nor assist another in doing so. Rule 5.5(b) specifically prohibits an out-of-jurisdiction lawyer from establishing an office or other systematic and continuous presence in a jurisdiction, or holding out to the public as admitted to practice there. Rule 5.5(c) provides safe harbors for temporary practice: (1) association with a local lawyer who actively participates, (2) services related to a pending or potential arbitration/mediation/ADR proceeding in or reasonably related to the lawyer's home jurisdiction, (3) services related to a pending or potential proceeding before a tribunal (including pro hac vice admission), and (4) services that arise out of or are reasonably related to the lawyer's home-jurisdiction practice. Rule 5.5(d) provides safe harbors for in-house counsel and government lawyers. The definition of 'practice of law' varies by jurisdiction and is notoriously vague. Birbrower, Montalbano, Condon & Frank v. Superior Court (Cal. 1998) held that a NY firm's activities in California constituted UPL and voided the firm's fee agreement.",
        authority="ABA Model Rule 5.5; Birbrower, Montalbano, Condon & Frank v. Superior Court, 17 Cal.4th 119 (1998); Restatement (Third) Law Governing Lawyers Section 3",
        keywords=["unauthorized practice", "upl", "rule 5.5", "multijurisdictional practice", "pro hac vice", "safe harbor", "temporary practice", "in-house counsel", "practice of law definition"],
        rule_reference="Model Rule 5.5",
        restatement_reference="Restatement (Third) Law Governing Lawyers Section 3",
        confidence=0.93,
        cross_references=["competence_rule_1_1"],
        practice_tips=[
            "Before practicing in another jurisdiction, confirm you qualify under a safe harbor or seek pro hac vice admission",
            "In-house counsel should register in the jurisdiction where they are physically present (most jurisdictions now offer registration)",
            "UPL by non-lawyers (paralegals, document preparers, online legal services) is enforced by state bars",
            "Unauthorized practice can void fee agreements and create malpractice exposure",
        ],
        texas_notes="Texas Government Code Chapter 81 governs UPL; Texas Supreme Court enforces through the Unauthorized Practice of Law Committee; Texas pro hac vice governed by TRCP 10",
    ),

    # ---- DISCIPLINE / SANCTIONS ----
    DoctrineCacheBlock(
        topic="lawyer_discipline_sanctions",
        category="maintaining_integrity",
        summary="The lawyer disciplinary system addresses attorney misconduct through sanctions ranging from private admonition to disbarment. The ABA Standards for Imposing Lawyer Sanctions (1992, amended 2021) provide the analytical framework for determining the appropriate sanction.",
        analysis="The disciplinary process typically involves: (1) complaint filing, (2) investigation by bar counsel, (3) formal charges if probable cause exists, (4) hearing before a disciplinary panel or board, (5) findings and recommended sanctions, (6) review by the state supreme court. The ABA Standards for Imposing Lawyer Sanctions use a four-factor analysis: (1) duty violated (duty to clients, public, legal system, or profession), (2) lawyer's mental state (intentional, knowing, negligent), (3) actual or potential injury caused, and (4) aggravating and mitigating factors. Standard sanctions: disbarment (most serious — intentional conversion of client funds, patterns of serious misconduct), suspension (definite or indefinite — knowing conduct causing serious injury), reprimand/censure (public or private — negligent conduct causing injury), admonition (least serious — isolated negligent conduct). Aggravating factors include: prior discipline, dishonest motive, pattern of misconduct, multiple offenses, vulnerability of victim. Mitigating factors include: absence of prior discipline, personal problems, inexperience, cooperative attitude, good character. Reciprocal discipline applies across jurisdictions. In re Crandall (D.C. 2003) established that disbarment is presumptive for intentional misappropriation of client funds.",
        authority="ABA Standards for Imposing Lawyer Sanctions (1992, amended 2021); In re Crandall, 832 A.2d 756 (D.C. 2003); Restatement (Third) Law Governing Lawyers Sections 5-6",
        keywords=["discipline", "sanctions", "disbarment", "suspension", "reprimand", "admonition", "aggravating factors", "mitigating factors", "grievance", "misconduct"],
        rule_reference="ABA Standards for Imposing Lawyer Sanctions (1992, amended 2021)",
        restatement_reference="Restatement (Third) Law Governing Lawyers Sections 5-6",
        confidence=0.94,
        cross_references=["trust_accounts_iolta", "competence_rule_1_1", "reporting_misconduct_rule_8_3"],
        practice_tips=[
            "Cooperation with the disciplinary process is a mitigating factor; obstruction is an aggravating factor",
            "Reciprocal discipline means a sanction in one jurisdiction may be imposed in others",
            "Malpractice insurance carriers should be notified immediately of any disciplinary complaint",
            "Track all deadlines in disciplinary proceedings; failure to respond can result in default findings",
        ],
    ),
    DoctrineCacheBlock(
        topic="reporting_misconduct_rule_8_3",
        category="maintaining_integrity",
        summary="ABA Model Rule 8.3 requires a lawyer who knows that another lawyer has committed a violation of the Rules of Professional Conduct that raises a substantial question as to that lawyer's honesty, trustworthiness, or fitness as a lawyer to inform the appropriate professional authority.",
        analysis="Model Rule 8.3(a) imposes a mandatory reporting obligation: a lawyer who knows of another lawyer's misconduct raising a substantial question about honesty, trustworthiness, or fitness must report to the appropriate authority (typically the state bar disciplinary counsel). Rule 8.3(b) imposes the same obligation regarding judicial misconduct. Rule 8.3(c) provides an exception: information protected by Rule 1.6 (confidentiality) or information gained while participating in an approved lawyers' assistance program need not be reported. The reporting obligation is triggered by 'knowledge' — which in Model Rule 1.0(f) means 'actual knowledge of the fact in question,' though knowledge may be inferred from circumstances. The standard is both subjective (what the lawyer actually knew) and objective (what a reasonable lawyer would have known). The 'substantial question' threshold excludes minor rule violations. In re Himmel (Ill. 1988) is the landmark case: a lawyer was suspended for failing to report his client's former lawyer's conversion of settlement funds. This case is widely cited for the proposition that the duty to report is real and enforceable.",
        authority="ABA Model Rule 8.3; In re Himmel, 533 N.E.2d 790 (Ill. 1988); Restatement (Third) Law Governing Lawyers Section 5",
        keywords=["reporting misconduct", "rule 8.3", "mandatory reporting", "himmel", "duty to report", "substantial question", "honesty", "trustworthiness", "fitness"],
        rule_reference="Model Rule 8.3",
        confidence=0.93,
        cross_references=["lawyer_discipline_sanctions", "confidentiality_rule_1_6"],
    ),
    DoctrineCacheBlock(
        topic="lawyer_misconduct_rule_8_4",
        category="maintaining_integrity",
        summary="ABA Model Rule 8.4 defines 'professional misconduct' to include criminal acts reflecting adversely on honesty/trustworthiness/fitness, dishonesty/fraud/deceit/misrepresentation, conduct prejudicial to the administration of justice, and harassment or discrimination in practice.",
        analysis="Model Rule 8.4 lists categories of misconduct: (a) violating or attempting to violate the Rules, (b) committing a criminal act reflecting adversely on honesty/trustworthiness/fitness, (c) engaging in conduct involving dishonesty, fraud, deceit, or misrepresentation, (d) conduct prejudicial to the administration of justice, (e) stating or implying ability to influence improperly a government agency or official, (f) knowingly assisting a judge in violating the Code of Judicial Conduct, and (g) engaging in harassment or discrimination on the basis of race, sex, religion, national origin, ethnicity, disability, age, sexual orientation, gender identity, marital status, or socioeconomic status in conduct related to the practice of law (added 2016). Rule 8.4(c) dishonesty is the broadest and most frequently charged provision. It is not limited to the practice of law; personal dishonesty (e.g., filing a false tax return, insurance fraud) can constitute professional misconduct. The 'conduct prejudicial to the administration of justice' catch-all in Rule 8.4(d) covers a wide range of misconduct including delay tactics, frivolous litigation, and disruptive courtroom behavior.",
        authority="ABA Model Rule 8.4; In re Disciplinary Proceedings Against Bonet, 29 P.3d 1242 (Wash. 2001); Restatement (Third) Law Governing Lawyers Section 5",
        keywords=["misconduct", "rule 8.4", "dishonesty", "fraud", "deceit", "criminal act", "prejudicial to administration of justice", "harassment", "discrimination"],
        rule_reference="Model Rule 8.4",
        confidence=0.94,
        cross_references=["reporting_misconduct_rule_8_3", "lawyer_discipline_sanctions"],
    ),

    # ---- MALPRACTICE ----
    DoctrineCacheBlock(
        topic="malpractice_liability",
        category="civil_liability",
        summary="Legal malpractice is a civil tort action requiring proof of four elements: (1) the existence of an attorney-client relationship establishing duty, (2) breach of the duty of care (negligent performance), (3) proximate causation (the 'case within a case'), and (4) actual damages.",
        analysis="Legal malpractice claims are governed by state tort law. The standard of care is that of a reasonably competent attorney in the same jurisdiction. The 'case within a case' (or 'suit within a suit') doctrine requires the plaintiff to prove that but for the lawyer's negligence, the underlying matter would have been resolved more favorably. This effectively requires trying both the malpractice case and the underlying case. Causation is often the most difficult element to prove. Damages must be actual and provable, not speculative. Common malpractice scenarios include: missed statute of limitations, failure to file proper pleadings, conflicts of interest, inadequate investigation or discovery, failure to properly advise the client, trust account mismanagement. Some jurisdictions also recognize breach of fiduciary duty as a separate cause of action (which may have a longer statute of limitations or different damages standard). Togstad v. Vesely, Otto, Miller & Keefe (Minn. 1980) established that the duty can arise even from a brief consultation. The collectibility doctrine (Lieberman v. Employers Ins. of Wausau) requires proof that the underlying judgment would have been collectible.",
        authority="Togstad v. Vesely, Otto, Miller & Keefe, 291 N.W.2d 686 (Minn. 1980); Smith v. Lewis, 13 Cal.3d 349 (1975); Restatement (Third) Law Governing Lawyers Sections 48-56",
        keywords=["malpractice", "legal malpractice", "negligence", "standard of care", "case within a case", "duty of care", "breach", "causation", "damages", "statute of limitations"],
        rule_reference="State Tort Law; Restatement (Third) Law Governing Lawyers Sections 48-56",
        restatement_reference="Restatement (Third) Law Governing Lawyers Sections 48-56",
        confidence=0.95,
        cross_references=["competence_rule_1_1", "diligence_rule_1_3", "fiduciary_duties"],
        practice_tips=[
            "Maintain malpractice insurance; many jurisdictions now require disclosure of coverage status",
            "Calendaring and docketing systems are essential malpractice prevention tools",
            "Engagement letters and disengagement letters define the scope and limits of the representation",
            "The 'case within a case' requirement means a malpractice plaintiff must prove the underlying case would have been won",
        ],
        texas_notes="Texas malpractice governed by CPRC Chapter 82; 2-year statute of limitations with discovery rule; Texas requires expert testimony on standard of care",
    ),

    # ---- FIDUCIARY DUTIES ----
    DoctrineCacheBlock(
        topic="fiduciary_duties",
        category="fiduciary",
        summary="Lawyers owe fiduciary duties to their clients including loyalty, confidentiality, candor, care, and accounting. Breach of fiduciary duty is a separate cause of action from malpractice in many jurisdictions.",
        analysis="The lawyer's fiduciary duties encompass: (1) Loyalty — undivided allegiance to the client's interests, (2) Confidentiality — protecting all information relating to the representation, (3) Candor — honest and complete communication with the client, (4) Care — the competence and diligence expected of a reasonably prudent attorney, (5) Accounting — proper handling of client funds and property. Breach of fiduciary duty differs from malpractice in several key ways: (a) the duty is broader than negligence — it encompasses intentional and knowing conduct, (b) the 'case within a case' causation standard may not apply, (c) fee forfeiture (disgorgement) is available as a remedy without proof of damages, (d) punitive damages may be available in some jurisdictions for intentional breach, (e) the statute of limitations may be longer. In Burrow v. Arce (Tex. 1999), the Texas Supreme Court held that a lawyer who breaches fiduciary duties must forfeit fees without requiring proof of actual damages. This makes breach of fiduciary duty a powerful claim in fee disputes and conflict situations.",
        authority="Burrow v. Arce, 997 S.W.2d 229 (Tex. 1999); Maritrans GP Inc. v. Pepper, Hamilton & Scheetz, 602 A.2d 1277 (Pa. 1992); Restatement (Third) Law Governing Lawyers Sections 16, 49",
        keywords=["fiduciary duty", "loyalty", "confidentiality", "candor", "care", "accounting", "fee forfeiture", "disgorgement", "breach of fiduciary duty"],
        rule_reference="Common Law; Restatement (Third) Law Governing Lawyers Sections 16, 49",
        restatement_reference="Restatement (Third) Law Governing Lawyers Sections 16, 49",
        confidence=0.94,
        cross_references=["malpractice_liability", "trust_accounts_iolta", "confidentiality_rule_1_6"],
        texas_notes="Texas recognizes breach of fiduciary duty as an independent cause of action; Burrow v. Arce allows fee forfeiture without proof of actual damages; 4-year statute of limitations under CPRC Section 16.004",
    ),

    # ---- JUDICIAL ETHICS ----
    DoctrineCacheBlock(
        topic="judicial_ethics_cjc",
        category="judicial_ethics",
        summary="The ABA Model Code of Judicial Conduct (CJC) establishes ethical standards for judges including independence, impartiality, avoidance of impropriety, competence, diligence, equality/fairness, ex parte communication restrictions, disqualification rules, and limitations on extrajudicial activities.",
        analysis="The CJC is organized into four canons: Canon 1 (judges shall uphold and promote independence, integrity, and impartiality), Canon 2 (judges shall perform duties impartially, competently, and diligently), Canon 3 (judges shall conduct personal and extrajudicial activities to minimize conflicts), Canon 4 (judges shall not engage in political or campaign activity inconsistent with judicial independence). Key provisions: Rule 2.2 requires impartiality and fairness. Rule 2.9 prohibits ex parte communications except in narrow circumstances (scheduling, emergencies, court staff consultations). Rule 2.11 addresses disqualification: a judge must disqualify when (a) the judge has a personal bias, (b) the judge's former firm was involved, (c) the judge has a financial interest, (d) the judge or a close relative is a party, witness, or lawyer, or (e) the judge made public statements committing on an issue. Rule 2.4 prohibits external influences on judicial conduct. Rule 3.1 restricts extrajudicial activities. Rule 3.13 limits acceptance of gifts, loans, bequests, and benefits. Caperton v. A.T. Massey Coal Co., 556 U.S. 868 (2009) held that due process requires disqualification when there is a serious risk of actual bias from campaign contributions.",
        authority="ABA Model Code of Judicial Conduct (2007, amended 2010); Caperton v. A.T. Massey Coal Co., 556 U.S. 868 (2009); 28 USC 455 (federal judicial disqualification)",
        keywords=["judicial ethics", "code of judicial conduct", "cjc", "impartiality", "disqualification", "recusal", "ex parte", "independence", "campaign contributions", "caperton"],
        rule_reference="ABA Model Code of Judicial Conduct (2007, amended 2010); 28 USC 455",
        confidence=0.93,
        cross_references=["candor_toward_tribunal_rule_3_3"],
        practice_tips=[
            "Move for recusal early if there are grounds; delay can be treated as waiver in some jurisdictions",
            "28 USC 455 creates an objective standard: disqualification is required when a reasonable person would question impartiality",
            "Document any ex parte contacts and immediately bring them to the attention of all parties",
        ],
    ),

    # ---- MEDIATOR / ARBITRATOR ETHICS ----
    DoctrineCacheBlock(
        topic="mediator_ethics",
        category="adr_ethics",
        summary="Mediator ethical standards address impartiality, self-determination, competence, confidentiality, conflicts of interest, quality of the process, advertising, and fees. The ABA/AAA/ACR Model Standards of Conduct for Mediators (2005) is the primary framework.",
        analysis="The Model Standards of Conduct for Mediators (2005) establish nine standards: (I) Self-Determination — the mediator must respect parties' right to decide, (II) Impartiality — the mediator must conduct the process without favoritism or bias, (III) Conflicts of Interest — the mediator must avoid conflicts and disclose all actual or potential conflicts, (IV) Competence — the mediator must mediate only when qualified by training and experience, (V) Confidentiality — the mediator must maintain confidentiality per applicable law and agreements, (VI) Quality of the Process — the mediator must conduct the process fairly and diligently, (VII) Advertising and Solicitation — truthful, non-misleading advertising, (VIII) Fees and Other Charges — must be reasonable and disclosed in advance, (IX) Advancement of Mediation Practice — encourage diversity and access. Key issue: lawyers serving as mediators face dual ethical obligations under both mediator standards and Model Rule 2.4 (lawyer as third-party neutral). Rule 2.4 requires the lawyer-mediator to inform unrepresented parties that the mediator is not representing them and cannot give them legal advice. The Uniform Mediation Act (2001/2003) codifies mediation privilege in jurisdictions that have adopted it.",
        authority="ABA/AAA/ACR Model Standards of Conduct for Mediators (2005); ABA Model Rule 2.4; Uniform Mediation Act (2001/2003)",
        keywords=["mediator ethics", "mediation", "impartiality", "self-determination", "confidentiality", "model standards", "third-party neutral", "rule 2.4", "uniform mediation act"],
        rule_reference="Model Standards of Conduct for Mediators (2005); Model Rule 2.4",
        confidence=0.91,
        cross_references=["arbitrator_disclosure", "conflicts_concurrent_rule_1_7"],
    ),
    DoctrineCacheBlock(
        topic="arbitrator_disclosure",
        category="adr_ethics",
        summary="Arbitrators must disclose all facts that might create a reasonable impression of partiality, including financial interests, prior relationships with parties or counsel, and other potential conflicts. The duty is ongoing throughout the proceeding.",
        analysis="Arbitrator disclosure obligations arise from multiple sources: (1) the FAA Section 10(a)(2) permits vacatur for 'evident partiality,' (2) the AAA/ABA Code of Ethics for Arbitrators in Commercial Disputes (2004) requires disclosure of 'any known direct or indirect financial or personal interest in the outcome' and 'any known existing or past financial, business, professional, family, or social relationships which are likely to affect impartiality or which might reasonably create an appearance of partiality' (Canon II), (3) institutional rules (AAA, JAMS, ICC) impose additional disclosure requirements. The Supreme Court in Commonwealth Coatings Corp. v. Continental Casualty Co. (1968) established that arbitrators must disclose any dealings that might create an impression of possible bias. For party-appointed arbitrators, Canon X of the Code of Ethics provides special rules: party-appointed arbitrators may be 'non-neutral' if the parties' agreement or applicable rules so provide. IBA Guidelines on Conflicts of Interest in International Arbitration (2014) provide a 'traffic light' system: Red List (non-waivable disqualification), Orange List (disclose, parties may object), Green List (no disclosure required).",
        authority="FAA 9 USC Section 10(a)(2); Commonwealth Coatings Corp. v. Continental Casualty Co., 393 U.S. 145 (1968); AAA/ABA Code of Ethics for Arbitrators in Commercial Disputes (2004); IBA Guidelines on Conflicts of Interest (2014)",
        keywords=["arbitrator disclosure", "evident partiality", "conflicts", "arbitration ethics", "commonwealth coatings", "party-appointed arbitrator", "iba guidelines", "vacatur"],
        rule_reference="AAA/ABA Code of Ethics for Arbitrators (2004); FAA 9 USC 10(a)(2)",
        confidence=0.92,
        cross_references=["mediator_ethics", "conflicts_concurrent_rule_1_7"],
    ),

    # ---- SOX / SEC ATTORNEY REPORTING ----
    DoctrineCacheBlock(
        topic="sarbanes_oxley_sec_205",
        category="regulatory",
        summary="Sarbanes-Oxley Act Section 307 and SEC Part 205 impose mandatory 'up the ladder' reporting obligations on attorneys appearing and practicing before the SEC, requiring reporting of material violations of securities law or breaches of fiduciary duty to the CLO or CEO, and if necessary to the audit committee or board.",
        analysis="SOX Section 307 directed the SEC to promulgate rules requiring attorneys appearing before the Commission to report evidence of material violations of securities law or breach of fiduciary duty to the issuer's CLO or CEO. The SEC's Part 205 regulations (17 CFR Part 205) require: (1) attorneys must report 'up the ladder' — first to the CLO or CEO, and if they do not respond appropriately, to the audit committee, independent directors, or the full board, (2) the issuer may establish a Qualified Legal Compliance Committee (QLCC) as an alternative reporting channel, (3) 'appearing and practicing before the Commission' is broadly defined to include preparing securities filings, advising on securities law obligations, and supervising such activities, (4) attorneys are protected from retaliation for reporting up the ladder. The SEC considered but did not adopt a mandatory 'reporting out' (noisy withdrawal) provision. The proposed but never-adopted Rule 205.3(d) would have required the attorney to withdraw and notify the SEC if internal reporting failed to produce an appropriate response. Part 205 supplements but does not preempt state ethical rules. The interaction between SOX reporting duties and state confidentiality rules creates tension that corporate counsel must navigate carefully.",
        authority="Sarbanes-Oxley Act Section 307 (15 USC 7245); 17 CFR Part 205; SEC Release No. 33-8185 (Jan. 29, 2003)",
        keywords=["sarbanes-oxley", "sox", "sec part 205", "up the ladder", "reporting", "material violation", "qlcc", "corporate counsel", "securities law", "audit committee"],
        rule_reference="SOX Section 307; 17 CFR Part 205",
        confidence=0.93,
        cross_references=["organization_as_client_rule_1_13", "confidentiality_rule_1_6", "upjohn_corporate_privilege"],
        practice_tips=[
            "SOX up-the-ladder reporting is MANDATORY, not permissive like Model Rule 1.13",
            "Outside counsel for SEC reporting issuers are covered by Part 205, not just in-house counsel",
            "The QLCC mechanism provides an alternative reporting channel that may simplify obligations",
            "Interaction between state confidentiality rules and SOX reporting requires careful analysis",
        ],
    ),

    # ---- TEXAS DISCIPLINARY RULES ----
    DoctrineCacheBlock(
        topic="texas_disciplinary_rules",
        category="state_specific",
        summary="The Texas Disciplinary Rules of Professional Conduct (TDRPC) govern attorney conduct in Texas and differ from the ABA Model Rules in several significant ways, including a broader confidentiality exception for crime/fraud, different conflict waiver requirements, and Texas-specific advertising restrictions.",
        analysis="The TDRPC, adopted by the Supreme Court of Texas and administered by the State Bar of Texas Commission for Lawyer Discipline, have several notable differences from the ABA Model Rules: (1) Confidentiality (Rule 1.05) — Texas allows disclosure to prevent a client from committing a criminal or fraudulent act (not limited to financial injury) and has a mandatory disclosure provision to prevent reasonably certain death or substantial bodily harm, (2) Conflicts (Rule 1.06) — Texas uses different language and structure for conflict analysis, (3) Advertising (Part VII) — Texas has historically been stricter, requiring specific disclaimers and in some circumstances pre-filing of advertising materials, (4) Trust Accounts (Rule 1.14) — detailed requirements for IOLTA compliance through the Texas Access to Justice Foundation, (5) Fees (Rule 1.04) — similar reasonableness factors but Texas includes an 'unconscionability' standard, (6) Barratry — Texas Penal Code Section 38.12 makes barratry a criminal offense (Class A misdemeanor, or third-degree felony for pattern), which goes beyond disciplinary restrictions. The State Bar of Texas operates the Chief Disciplinary Counsel's office, which investigates and prosecutes disciplinary matters. Sanctions are imposed by Evidentiary Panels and the Board of Disciplinary Appeals.",
        authority="Texas Disciplinary Rules of Professional Conduct; Texas Government Code Chapter 81; Texas Penal Code Section 38.12; Texas Supreme Court Rules (RPTDA)",
        keywords=["texas disciplinary rules", "tdrpc", "texas bar", "barratry", "texas advertising", "commission for lawyer discipline", "texas trust account", "texas iolta"],
        rule_reference="Texas Disciplinary Rules of Professional Conduct",
        jurisdiction="TX",
        confidence=0.94,
        cross_references=["confidentiality_rule_1_6", "conflicts_concurrent_rule_1_7", "advertising_rule_7_1", "trust_accounts_iolta"],
        practice_tips=[
            "Texas confidentiality exceptions are broader than the ABA Model Rules in some respects",
            "Barratry is a CRIMINAL offense in Texas, not just a disciplinary matter",
            "Texas advertising rules require specific language and disclaimers; review Texas Disciplinary Rules Part VII before advertising",
            "The Texas Commission for Lawyer Discipline aggressively enforces trust account violations",
        ],
    ),

    # ---- LEGAL TECH / AI ETHICS ----
    DoctrineCacheBlock(
        topic="legal_tech_ai_ethics",
        category="emerging_ethics",
        summary="Legal technology ethics addresses lawyers' obligations when using AI tools, practice management software, cloud computing, and other technology in the practice of law, including duties of competence, confidentiality, supervision, and candor.",
        analysis="The intersection of legal technology and ethics creates several obligations: (1) Competence (Rule 1.1 Comment [8]) — lawyers must understand the benefits and risks of relevant technology, including AI tools. ABA Formal Opinion 477R (2017) requires reasonable efforts to prevent inadvertent or unauthorized disclosure in electronic communications. (2) Confidentiality (Rule 1.6) — cloud storage, AI tools, and practice management systems must protect client confidentiality. Lawyers must conduct due diligence on technology vendors and ensure adequate security measures (encryption, access controls, terms of service). (3) Supervision (Rules 5.1, 5.3) — lawyers must supervise AI tool outputs, non-lawyer assistants using technology, and offshore/outsourced legal work. AI output must be reviewed for accuracy. (4) Candor (Rule 3.3) — ABA Formal Opinion 512 (2024) addresses obligations when using AI-generated content in court filings: lawyers must verify all citations and factual assertions. Mata v. Avianca (S.D.N.Y. 2023) sanctioned lawyers for submitting AI-generated briefs with fabricated citations. (5) Billing — lawyers may not bill for time spent learning to use basic technology tools; AI efficiency gains may require fee adjustments. Several state bars have issued guidance on AI use in legal practice.",
        authority="ABA Model Rule 1.1 Comment [8]; ABA Formal Opinion 477R (2017); ABA Formal Opinion 512 (2024); Mata v. Avianca, Inc., No. 22-cv-1461 (S.D.N.Y. 2023); Florida Bar Ethics Opinion 24-1 (2024)",
        keywords=["legal tech", "ai ethics", "artificial intelligence", "chatgpt", "machine learning", "cloud computing", "cybersecurity", "technology competence", "mata v avianca", "ai-generated content"],
        rule_reference="Model Rule 1.1 Comment [8]; ABA Formal Opinion 512 (2024)",
        confidence=0.92,
        cross_references=["competence_rule_1_1", "confidentiality_rule_1_6", "candor_toward_tribunal_rule_3_3", "ghost_writing_ethics"],
        practice_tips=[
            "ALWAYS verify AI-generated citations before submission to any tribunal (Mata v. Avianca)",
            "Conduct due diligence on AI vendors regarding data security, training data, and confidentiality",
            "Disclose AI tool usage in court filings when required by local rules",
            "AI tools do not establish an attorney-client relationship and their outputs are not privileged",
            "Consider whether AI-assisted work products constitute unauthorized practice of law if the AI's role is not properly supervised",
        ],
        texas_notes="The State Bar of Texas has addressed technology competence in CLE requirements; Texas lawyers must ensure AI tools comply with TDRPC confidentiality and competence standards",
    ),
    DoctrineCacheBlock(
        topic="ghost_writing_ethics",
        category="emerging_ethics",
        summary="Ghost-writing raises ethical issues when a lawyer drafts pleadings or other documents for a pro se litigant without disclosing the lawyer's involvement. Jurisdictions are split on whether this constitutes dishonesty or improper limited-scope representation.",
        analysis="Ghost-writing occurs when a lawyer prepares legal documents for a pro se litigant who files them without disclosing attorney involvement. The ethical debate centers on: (1) Rule 3.3 candor — is filing a document without disclosing attorney assistance misleading to the tribunal? Some courts have held yes (Laremont-Lopez v. Southeastern Tidewater Opportunity Ctr., 968 F. Supp. 1075 (E.D. Va. 1997)), (2) Rule 1.2(c) limited scope — the 2002 amendments to Model Rule 1.2(c) explicitly permit limited-scope representation, and many jurisdictions now consider ghost-writing an acceptable form of unbundled legal services, (3) ABA Formal Opinion 07-446 concluded that a lawyer may draft pleadings for pro se litigants without disclosing involvement, as long as the documents are not misleading and the lawyer does not make false statements. However, many courts disagree. The trend is toward acceptance, particularly as access-to-justice concerns grow. Some jurisdictions now have specific rules permitting or requiring limited disclosure (e.g., 'prepared with attorney assistance'). The key tension is between access to justice (making legal help affordable through unbundled services) and candor toward the tribunal.",
        authority="ABA Formal Opinion 07-446; ABA Model Rule 1.2(c); Laremont-Lopez v. Southeastern Tidewater Opportunity Ctr., 968 F. Supp. 1075 (E.D. Va. 1997)",
        keywords=["ghost-writing", "ghostwriting", "pro se", "limited scope representation", "unbundled legal services", "rule 1.2(c)", "access to justice", "candor"],
        rule_reference="Model Rule 1.2(c); ABA Formal Opinion 07-446",
        confidence=0.88,
        cross_references=["candor_toward_tribunal_rule_3_3", "competence_rule_1_1"],
    ),
    DoctrineCacheBlock(
        topic="metadata_ethics",
        category="emerging_ethics",
        summary="Metadata ethics addresses the obligations of lawyers sending and receiving documents containing metadata — hidden data embedded in electronic documents that may reveal confidential information, including tracked changes, comments, and document properties.",
        analysis="Metadata in electronic documents can reveal confidential information: tracked changes, comments, prior drafts, author information, and editing history. Ethical obligations arise in two contexts: (1) Sending: lawyers have a duty under Rule 1.6 to take reasonable steps to prevent inadvertent disclosure of client confidential information through metadata. This means 'scrubbing' metadata from documents before sending. ABA Formal Opinion 06-442 held that a lawyer must exercise reasonable care to prevent disclosure of client information through metadata. Most jurisdictions require metadata scrubbing before sending. (2) Receiving: the ethics of mining received documents for metadata are more contested. ABA Formal Opinion 06-442 stopped short of prohibiting metadata mining but noted that some jurisdictions consider it a violation of Rule 4.4(b) (respecting rights of third persons) and Rule 8.4(c) (dishonesty). New York Ethics Opinion 749 (2001) prohibited intentional mining of metadata. Florida Ethics Opinion 06-2 permitted reviewing metadata. The ABA Committee on Ethics and Professional Responsibility has not categorically prohibited mining but counsels caution. Best practice: scrub outgoing documents and use reasonable judgment when receiving metadata-rich documents.",
        authority="ABA Formal Opinion 06-442; NY Ethics Opinion 749 (2001); Florida Ethics Opinion 06-2; ABA Model Rule 1.6; ABA Model Rule 4.4(b)",
        keywords=["metadata", "metadata ethics", "tracked changes", "document properties", "scrubbing", "inadvertent disclosure", "electronic documents", "rule 4.4(b)"],
        rule_reference="ABA Formal Opinion 06-442; Model Rule 1.6; Model Rule 4.4(b)",
        confidence=0.89,
        cross_references=["confidentiality_rule_1_6", "legal_tech_ai_ethics"],
    ),

    # ---- SCOPE OF REPRESENTATION ----
    DoctrineCacheBlock(
        topic="scope_of_representation_rule_1_2",
        category="client_lawyer_relationship",
        summary="ABA Model Rule 1.2 allocates decision-making authority between lawyer and client: the client decides the objectives of representation, while the lawyer decides the means, subject to consultation. A lawyer shall not counsel or assist a client in conduct the lawyer knows is criminal or fraudulent.",
        analysis="Model Rule 1.2(a) establishes the allocation: the client decides objectives (including whether to settle, plead guilty, waive jury, testify in criminal cases). The lawyer controls the means, subject to consultation with the client. Rule 1.2(c) permits limited-scope representation if reasonable under the circumstances and the client gives informed consent. Rule 1.2(d) prohibits the lawyer from counseling or assisting conduct known to be criminal or fraudulent, but a lawyer may discuss the legal consequences of proposed conduct and assist the client in making a good-faith effort to determine the validity, scope, meaning, or application of the law. The distinction between counseling about lawful options (permissible) and assisting in illegal conduct (prohibited) is critical. Comment [9] notes that a lawyer may counsel or assist a client regarding conduct expressly permitted by applicable law, even when the conduct may conflict with federal law (e.g., state marijuana legalization). This comment was added in response to state-level marijuana legalization.",
        authority="ABA Model Rule 1.2; Jones v. Barnes, 463 U.S. 745 (1983); Restatement (Third) Law Governing Lawyers Sections 21-23",
        keywords=["scope of representation", "rule 1.2", "client decisions", "lawyer decisions", "limited scope", "unbundled", "criminal conduct", "settlement authority"],
        rule_reference="Model Rule 1.2",
        restatement_reference="Restatement (Third) Law Governing Lawyers Sections 21-23",
        confidence=0.94,
        cross_references=["competence_rule_1_1", "communication_rule_1_4", "ghost_writing_ethics"],
    ),

    # ---- DECLINING / TERMINATING REPRESENTATION ----
    DoctrineCacheBlock(
        topic="declining_representation_rule_1_16",
        category="client_lawyer_relationship",
        summary="ABA Model Rule 1.16 governs mandatory and permissive withdrawal from representation. A lawyer must withdraw if representation will result in violation of the rules or law, the lawyer's physical or mental condition materially impairs the ability to represent, or the lawyer is discharged.",
        analysis="Model Rule 1.16(a) mandates withdrawal when: (1) representation will result in violation of the Rules or other law, (2) the lawyer's physical or mental condition materially impairs ability to represent, or (3) the lawyer is discharged. Rule 1.16(b) permits withdrawal when: (1) withdrawal can be accomplished without material adverse effect on client's interests, (2) the client persists in a course of action involving the lawyer's services that the lawyer reasonably believes is criminal or fraudulent, (3) the client uses the lawyer's services to perpetrate a crime or fraud, (4) the client insists upon taking action the lawyer finds repugnant or with which the lawyer has a fundamental disagreement, (5) the client fails substantially to fulfill an obligation to the lawyer regarding fees, (6) the representation will result in an unreasonable financial burden on the lawyer, or (7) other good cause exists. Rule 1.16(c) requires court permission to withdraw from pending litigation. Rule 1.16(d) requires the lawyer upon termination to take steps to protect the client's interests, including giving reasonable notice, allowing time for new counsel, surrendering papers and property to which the client is entitled, and refunding any advance payment of unearned fees. A retaining lien (on the client file) vs. a charging lien (on the proceeds) creates tension between protecting the lawyer's interest in fees and the client's interest in their files.",
        authority="ABA Model Rule 1.16; Whiting v. Lacara, 187 F.3d 317 (2d Cir. 1999); Restatement (Third) Law Governing Lawyers Sections 31-46",
        keywords=["withdrawal", "rule 1.16", "declining representation", "terminating representation", "mandatory withdrawal", "permissive withdrawal", "client files", "retaining lien", "charging lien"],
        rule_reference="Model Rule 1.16",
        restatement_reference="Restatement (Third) Law Governing Lawyers Sections 31-46",
        confidence=0.93,
        cross_references=["competence_rule_1_1", "fees_rule_1_5"],
    ),

    # ---- SUPERVISORY / SUBORDINATE RESPONSIBILITIES ----
    DoctrineCacheBlock(
        topic="supervisory_responsibility_rule_5_1",
        category="law_firms_and_associations",
        summary="ABA Model Rule 5.1 holds partners, managing lawyers, and supervisory lawyers responsible for establishing policies to ensure firm compliance with the Rules, and may be held disciplinarily responsible for another lawyer's misconduct if they order, ratify, or fail to take remedial action.",
        analysis="Model Rule 5.1(a) requires partners and lawyers with comparable managerial authority to make reasonable efforts to ensure the firm has measures giving reasonable assurance that all lawyers conform to the Rules. Rule 5.1(b) requires direct supervisory lawyers to make reasonable efforts to ensure supervised lawyers conform. Rule 5.1(c) holds a lawyer responsible for another's violation if: (1) the lawyer orders or ratifies the conduct with knowledge of the specific conduct, or (2) the lawyer is a partner, manager, or direct supervisor who knows of the conduct at a time when its consequences can be avoided or mitigated but fails to take reasonable remedial action. Model Rule 5.3 extends similar obligations to supervising nonlawyer assistants (paralegals, legal assistants, AI tools, outsourced workers). The duty to supervise includes ensuring competent work, maintaining confidentiality, and avoiding conflicts. In re Galasso (NY 2004) disciplined a partner for inadequate supervision of an associate who neglected client matters.",
        authority="ABA Model Rule 5.1; ABA Model Rule 5.3; In re Galasso, 819 N.Y.S.2d 459 (N.Y. App. Div. 2006); Restatement (Third) Law Governing Lawyers Section 11",
        keywords=["supervision", "rule 5.1", "rule 5.3", "partner responsibility", "managing lawyer", "supervisory lawyer", "nonlawyer assistant", "vicarious liability", "firm policies"],
        rule_reference="Model Rule 5.1; Model Rule 5.3",
        restatement_reference="Restatement (Third) Law Governing Lawyers Section 11",
        confidence=0.93,
        cross_references=["competence_rule_1_1", "legal_tech_ai_ethics"],
    ),

    # ---- COMMUNICATING WITH REPRESENTED / UNREPRESENTED PERSONS ----
    DoctrineCacheBlock(
        topic="communicating_with_represented_rule_4_2",
        category="transactions_with_others",
        summary="ABA Model Rule 4.2 (the 'no-contact rule') prohibits a lawyer from communicating about the subject of the representation with a person the lawyer knows to be represented by another lawyer in the matter, unless the person's lawyer consents or the communication is authorized by law or court order.",
        analysis="Model Rule 4.2 is one of the most frequently litigated ethics rules. Key issues: (1) 'Knows to be represented' — actual knowledge is required, but knowledge may be inferred from circumstances, (2) In the organizational context, the rule applies to communications with current officers, directors, and managing agents, employees whose acts or omissions may be imputed to the organization, and employees whose statements constitute admissions (Comment [7]), (3) Former employees are generally not covered by the rule (though some jurisdictions disagree), (4) 'Authorized by law' includes communications by government investigators in the course of authorized law enforcement (the 'Thornburgh Memo' controversy, resolved by 28 USC 530B requiring government lawyers to follow state ethics rules), (5) The rule applies even when the represented person initiates the contact, (6) Violations can result in suppression of statements obtained, disqualification, and discipline. Niesig v. Team I (NY 1990) established the 'alter ego' test for identifying which corporate employees are covered.",
        authority="ABA Model Rule 4.2; Niesig v. Team I, 76 N.Y.2d 363 (1990); 28 USC 530B; Restatement (Third) Law Governing Lawyers Section 99-100",
        keywords=["no-contact rule", "rule 4.2", "represented person", "corporate employees", "alter ego", "consent", "authorized by law", "government investigations"],
        rule_reference="Model Rule 4.2",
        restatement_reference="Restatement (Third) Law Governing Lawyers Section 99-100",
        confidence=0.94,
        cross_references=["organization_as_client_rule_1_13"],
    ),

    # ---- SOCIAL MEDIA ETHICS ----
    DoctrineCacheBlock(
        topic="social_media_ethics",
        category="emerging_ethics",
        summary="Social media creates ethics issues around advertising, solicitation, confidentiality, communication with represented persons, juror research, and the duty of candor. Bar associations have issued numerous ethics opinions addressing these issues.",
        analysis="Social media ethics implicates multiple Rules: (1) Advertising (Rule 7.1) — LinkedIn profiles, blog posts, and social media pages are 'communications' about services subject to advertising rules, (2) Solicitation (Rule 7.3) — direct messaging a prospective client on social media may constitute solicitation, (3) Confidentiality (Rule 1.6) — lawyers must not reveal client information through social media posts, even inadvertently, (4) No-Contact Rule (Rule 4.2) — friending or messaging a represented person on social media about the matter violates the no-contact rule, (5) Juror Research (Rule 3.5) — passive review of jurors' public social media profiles is generally permissible; active communication (friending, following if it generates a notification) is prohibited, (6) Candor (Rule 3.3) — social media evidence must be authenticated and not fabricated. ABA Formal Opinion 466 (2014) addressed juror social media research. Philadelphia Bar Opinion 2009-02 addressed social media contact with represented parties. New York State Bar Association Ethics Opinions 2017-6 and 2019-2 addressed social media advertising and juror research, respectively.",
        authority="ABA Formal Opinion 466 (2014); ABA Formal Opinion 462 (2013); Philadelphia Bar Opinion 2009-02; NYSBA Ethics Opinion 2017-6",
        keywords=["social media", "ethics", "linkedin", "facebook", "twitter", "advertising", "solicitation", "juror research", "confidentiality", "no-contact"],
        rule_reference="Multiple Rules: 1.6, 3.3, 3.5, 4.2, 7.1, 7.3",
        confidence=0.90,
        cross_references=["advertising_rule_7_1", "solicitation_rule_7_2", "communicating_with_represented_rule_4_2", "confidentiality_rule_1_6"],
    ),

    # ---- GOVERNMENT OFFICERS (Rule 1.11) ----
    DoctrineCacheBlock(
        topic="government_officers_rule_1_11",
        category="conflicts_of_interest",
        summary="ABA Model Rule 1.11 addresses special conflict-of-interest rules for current and former government officers and employees, including screening provisions for former government lawyers who enter private practice.",
        analysis="Model Rule 1.11(a) prohibits a former government lawyer from representing a client in a matter in which the lawyer participated personally and substantially while in government service, unless the government agency gives informed consent confirmed in writing. Rule 1.11(b) provides that when a former government lawyer is disqualified under (a), no other lawyer in the firm may represent a client in that matter unless the disqualified lawyer is timely screened, receives no fee from the matter, and written notice is given to the government agency. Rule 1.11(c) restricts current government lawyers from participating in matters where the lawyer participated personally and substantially in private practice or nongovernmental employment. Rule 1.11(d) prohibits former government lawyers from using confidential government information to the disadvantage of persons to whom the information pertains. The 'revolving door' protections are designed to balance two competing interests: enabling government recruitment of talented lawyers and preventing exploitation of government service for private gain.",
        authority="ABA Model Rule 1.11; Restatement (Third) Law Governing Lawyers Section 133",
        keywords=["government officers", "rule 1.11", "revolving door", "personally and substantially", "screening", "government information", "former government lawyer"],
        rule_reference="Model Rule 1.11",
        restatement_reference="Restatement (Third) Law Governing Lawyers Section 133",
        confidence=0.92,
        cross_references=["imputed_conflicts_rule_1_10", "conflicts_former_client_rule_1_9"],
    ),

    # ---- CONFLICT SCREENING PROCEDURES ----
    DoctrineCacheBlock(
        topic="conflict_screening_procedures",
        category="practice_management",
        summary="Conflict screening is the systematic process of checking for conflicts of interest before accepting new clients or matters, using databases of current and former clients, adverse parties, and related entities.",
        analysis="Effective conflict screening requires: (1) Comprehensive database — all current and former clients, adverse parties, related parties, corporate affiliates, and key individuals must be recorded, (2) Intake procedures — every new matter must be screened against the database before substantive work begins, (3) Lateral hire screening — when a lawyer joins the firm, their entire prior matter history must be checked, (4) Regular updates — the database must be current and updated as matters develop (new parties, cross-claims, interventions), (5) Documentation — all screens must be documented and retained, (6) False positives — must be investigated and resolved, not ignored. Technology platforms (conflict management software) are essential for firms of any size. The duty to check for conflicts is implicit in Rules 1.7, 1.9, and 1.10. Failure to implement reasonable conflict-checking systems can itself be a basis for discipline under Rule 5.1 (supervisory responsibilities). Advance conflict waivers (obtained at engagement for future, currently unknown conflicts) are permissible but their enforceability varies by jurisdiction and depends on the specificity of the waiver and the sophistication of the client.",
        authority="ABA Model Rules 1.7, 1.9, 1.10, 5.1; ABA Formal Opinion 05-436 (advance conflict waivers)",
        keywords=["conflict screening", "conflict check", "intake procedures", "lateral hire", "conflict database", "advance waiver", "prospective waiver"],
        rule_reference="Model Rules 1.7, 1.9, 1.10, 5.1",
        confidence=0.91,
        cross_references=["conflicts_concurrent_rule_1_7", "conflicts_former_client_rule_1_9", "imputed_conflicts_rule_1_10"],
    ),

    # ---- FEE REASONABLENESS / CONTINGENCY / FEE-SPLITTING ----
    DoctrineCacheBlock(
        topic="fee_reasonableness",
        category="fees",
        summary="Fee reasonableness analysis applies the eight factors of Model Rule 1.5(a) to determine whether a fee is permissible. Courts also apply the lodestar method (reasonable hourly rate x reasonable hours) in fee-shifting statutes.",
        analysis="The eight Rule 1.5(a) factors provide the analytical framework for reasonableness: time/labor/novelty/difficulty/skill, preclusion of other employment, customary fee, amount involved/results, time limits, relationship nature/length, experience/reputation/ability, fixed vs. contingent. In fee-shifting contexts, the lodestar method (Hensley v. Eckerhart, 461 U.S. 424 (1983)) multiplies a reasonable hourly rate by reasonable hours expended, with possible adjustments for quality of results. Courts may reduce fees for excessive, redundant, or unnecessary hours. Block billing (lumping multiple tasks into a single time entry) may result in fee reduction. Minimum billing increments (e.g., 0.25-hour or 6-minute) are standard but inflated minimums (e.g., 1-hour minimum for a phone call) raise reasonableness concerns. Flat fees, success fees, and blended rates are all permissible if reasonable. In re Fordham (Mass. 1996) disbarred a lawyer for charging $50,000 for a first-offense drunk driving case.",
        authority="ABA Model Rule 1.5(a); Hensley v. Eckerhart, 461 U.S. 424 (1983); In re Fordham, 668 N.E.2d 816 (Mass. 1996); Restatement (Third) Law Governing Lawyers Section 34",
        keywords=["fee reasonableness", "eight factors", "lodestar", "hourly rate", "block billing", "flat fee", "fee-shifting", "excessive fees"],
        rule_reference="Model Rule 1.5(a)",
        restatement_reference="Restatement (Third) Law Governing Lawyers Section 34",
        confidence=0.93,
        cross_references=["fees_rule_1_5", "contingency_fees", "fee_splitting"],
    ),
    DoctrineCacheBlock(
        topic="contingency_fees",
        category="fees",
        summary="Contingency fee agreements must be in writing, signed by the client, and state the method of calculation. Contingency fees are prohibited in criminal defense and certain domestic relations matters.",
        analysis="Model Rule 1.5(c) requires contingency agreements to: (1) be in a writing signed by the client, (2) state the method of calculation including the percentage(s), (3) state litigation and other expenses to be deducted, and (4) whether expenses are deducted before or after the contingency fee. Rule 1.5(d) prohibits contingency fees in: (1) criminal defense matters (would create an improper stake in the outcome), and (2) domestic relations matters where the fee is contingent on securing a divorce or upon the amount of alimony, support, or property settlement (though contingency fees are permissible for collecting past-due support or enforcement of property settlements). Percentage caps vary by jurisdiction; some states cap personal injury contingency fees at 33.33% or use sliding scales. In structured settlements, the contingency fee is typically calculated on the present value, not the total payout. The client has the right to discharge the lawyer at any time; if discharged before resolution, the lawyer is entitled to the reasonable value of services rendered (quantum meruit) in most jurisdictions.",
        authority="ABA Model Rule 1.5(c)-(d); Restatement (Third) Law Governing Lawyers Section 35; Ethics Opinions on structured settlement valuation",
        keywords=["contingency fee", "percentage", "criminal defense", "domestic relations", "quantum meruit", "fee cap", "structured settlement"],
        rule_reference="Model Rule 1.5(c)-(d)",
        restatement_reference="Restatement (Third) Law Governing Lawyers Section 35",
        confidence=0.93,
        cross_references=["fees_rule_1_5", "fee_reasonableness"],
    ),
    DoctrineCacheBlock(
        topic="fee_splitting",
        category="fees",
        summary="ABA Model Rule 1.5(e) permits fee division between lawyers in different firms if the division is proportional to services or each lawyer assumes joint responsibility, the client agrees in writing, and the total fee is reasonable. Fee-sharing with non-lawyers is prohibited under Rule 5.4.",
        analysis="Model Rule 1.5(e) governs fee division between lawyers not in the same firm: (1) each lawyer's share must be proportional to the services performed, OR each lawyer must assume joint responsibility (meaning each lawyer is individually responsible for the entire representation), (2) the client must agree to the arrangement in writing including the share each lawyer receives, and (3) the total fee must be reasonable. Model Rule 5.4(a) prohibits sharing fees with non-lawyers, with limited exceptions for: (a) death benefits to a deceased lawyer's estate, (b) paying a non-lawyer employee under a compensation plan that includes a share of profits, (c) sharing court-awarded fees with a nonprofit organization that employed or recommended the lawyer. The prohibition on fee-sharing with non-lawyers is designed to protect the lawyer's professional independence. It prevents arrangements where a non-lawyer (such as a lead generator, marketing company, or technology platform) receives a percentage of legal fees. Some jurisdictions (notably Utah's regulatory sandbox and Arizona's Alternative Business Structures) are experimenting with relaxing Rule 5.4.",
        authority="ABA Model Rule 1.5(e); ABA Model Rule 5.4; Restatement (Third) Law Governing Lawyers Section 47",
        keywords=["fee splitting", "fee division", "referral fee", "joint responsibility", "non-lawyer fee sharing", "rule 5.4", "alternative business structure"],
        rule_reference="Model Rule 1.5(e); Model Rule 5.4",
        restatement_reference="Restatement (Third) Law Governing Lawyers Section 47",
        confidence=0.92,
        cross_references=["fees_rule_1_5", "fee_reasonableness"],
    ),

    # ---- TRUTHFULNESS IN STATEMENTS (Rule 4.1) ----
    DoctrineCacheBlock(
        topic="truthfulness_rule_4_1",
        category="transactions_with_others",
        summary="ABA Model Rule 4.1 prohibits a lawyer from making a false statement of material fact or law to a third person, and requires disclosure of material facts when necessary to avoid assisting a client's criminal or fraudulent act, unless disclosure is prohibited by Rule 1.6.",
        analysis="Model Rule 4.1(a) prohibits knowingly making a false statement of material fact or law to a third person in the course of representing a client. Rule 4.1(b) requires disclosure of a material fact to a third person when necessary to avoid assisting a criminal or fraudulent act by a client, unless disclosure is prohibited by Rule 1.6. Comment [2] distinguishes between statements of material fact and 'mere puffing' — certain types of statements ordinarily are not taken as statements of material fact, including estimates of price or value in negotiation and statements regarding a party's intentions as to an acceptable settlement. This creates a recognized zone for negotiation posturing. However, affirmative misrepresentations of material fact (such as the existence of insurance coverage, the number of claimants, or the extent of damages) violate the rule. The interaction between Rule 4.1(b) (disclosure obligation) and Rule 1.6 (confidentiality) creates a difficult tension: the lawyer may be required to disclose to prevent client fraud, but may also be prohibited from disclosing confidential information. The resolution depends on the jurisdiction's version of Rule 1.6(b) exceptions.",
        authority="ABA Model Rule 4.1; ABA Formal Opinion 06-439; Restatement (Third) Law Governing Lawyers Section 98",
        keywords=["truthfulness", "rule 4.1", "false statement", "material fact", "negotiation", "puffing", "client fraud", "disclosure obligation"],
        rule_reference="Model Rule 4.1",
        restatement_reference="Restatement (Third) Law Governing Lawyers Section 98",
        confidence=0.93,
        cross_references=["candor_toward_tribunal_rule_3_3", "confidentiality_rule_1_6"],
    ),
]


# ============================================================================
# MODULE-LEVEL FUNCTIONS
# ============================================================================

_cache: Optional[DoctrineCacheIndex] = None


def build_doctrine_cache() -> DoctrineCacheIndex:
    """Build and return the doctrine cache index."""
    global _cache
    idx = DoctrineCacheIndex()
    for block in DOCTRINE_BLOCKS:
        idx.add(block)
    _cache = idx
    logger.info(f"Doctrine cache built: {idx.total_blocks} blocks, {len(idx.categories)} categories")
    return idx


def get_doctrine_cache() -> DoctrineCacheIndex:
    """Get the global doctrine cache, building if necessary."""
    global _cache
    if _cache is None:
        return build_doctrine_cache()
    return _cache


def get_doctrine_block(topic: str) -> Optional[DoctrineCacheBlock]:
    """Get a specific doctrine block by topic."""
    cache = get_doctrine_cache()
    return cache.get(topic)


def search_doctrines(query: str, max_results: int = 10) -> List[DoctrineCacheBlock]:
    """Search the doctrine cache by query string."""
    cache = get_doctrine_cache()
    return cache.search(query, max_results=max_results)


def get_all_doctrine_topics() -> List[str]:
    """Get all doctrine topic identifiers."""
    cache = get_doctrine_cache()
    return cache.topics


def get_all_doctrine_categories() -> List[str]:
    """Get all doctrine category names."""
    cache = get_doctrine_cache()
    return cache.categories


def get_doctrine_cache_stats() -> Dict[str, Any]:
    """Get cache statistics."""
    cache = get_doctrine_cache()
    return cache.get_stats()


def get_coverage_map() -> Dict[str, List[str]]:
    """Get the full coverage map: category -> list of topics."""
    cache = get_doctrine_cache()
    result: Dict[str, List[str]] = {}
    for cat in cache.categories:
        blocks = cache.get_by_category(cat)
        result[cat] = [b.topic for b in blocks]
    return result


def get_doctrine_cache_hash() -> str:
    """Compute SHA-256 hash over all doctrine blocks for integrity verification."""
    parts: List[str] = []
    for block in DOCTRINE_BLOCKS:
        parts.append(block.block_hash)
    combined = "|".join(sorted(parts))
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()


def verify_doctrine_integrity() -> Dict[str, Any]:
    """Verify integrity of all doctrine blocks."""
    issues: List[str] = []
    for block in DOCTRINE_BLOCKS:
        expected = hashlib.sha256(
            f"{block.topic}|{block.summary}|{block.analysis}|{block.authority}".encode("utf-8")
        ).hexdigest()
        if block.block_hash != expected:
            issues.append(f"Hash mismatch on {block.topic}")
        if not block.summary or len(block.summary) < 50:
            issues.append(f"Insufficient summary on {block.topic}")
        if not block.analysis or len(block.analysis) < 100:
            issues.append(f"Insufficient analysis on {block.topic}")
        if not block.authority:
            issues.append(f"Missing authority on {block.topic}")
    return {
        "total_blocks": len(DOCTRINE_BLOCKS),
        "issues_found": len(issues),
        "issues": issues,
        "cache_hash": get_doctrine_cache_hash(),
        "integrity_ok": len(issues) == 0,
    }


def get_stale_doctrines(max_age_days: int = 365) -> List[str]:
    """Get doctrine topics that have not been updated within max_age_days."""
    stale: List[str] = []
    now = datetime.now(timezone.utc)
    for block in DOCTRINE_BLOCKS:
        try:
            updated = datetime.fromisoformat(block.last_updated)
            if (now - updated).days > max_age_days:
                stale.append(block.topic)
        except (ValueError, TypeError):
            stale.append(block.topic)
    return stale
