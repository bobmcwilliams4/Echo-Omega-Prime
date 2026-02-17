"""
LG18 Legislative Analysis Engine - Doctrine Cache Module
==========================================================
Pre-compiled legislative doctrine blocks for instant retrieval on common
statutory construction, congressional procedure, regulatory rulemaking,
preemption, delegation, lobbying regulation, redistricting, and Texas
legislative process queries.

Each doctrine block contains:
    - topic: Canonical topic identifier
    - summary: Executive-level overview of the doctrine
    - key_statutes: Controlling statutory references
    - elements: Legal elements or requirements
    - defenses: Common defenses or exceptions
    - remedies: Available remedies or relief
    - leading_cases: Landmark case citations

Components:
    - DOCTRINE_BLOCKS: List of pre-compiled doctrine cache entries
    - DoctrineCacheBlock: Structured doctrine entry model
    - DoctrineCacheIndex: Fast O(1) lookup by topic/category
    - build_doctrine_cache(): Build the complete cache from blocks
    - get_doctrine_block(): Retrieve a single block by topic
    - search_doctrines(): Free-text search over doctrine blocks
    - get_coverage_map(): Map of all topics with staleness data

Version: 2.0.0
Engine: LG18 Legislative Analysis
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from typing import Any, ClassVar, Dict, List, Optional, Set

from loguru import logger


# ============================================================================
# DOCTRINE CACHE BLOCK MODEL
# ============================================================================

@dataclass
class DoctrineCacheBlock:
    """A single pre-compiled legislative doctrine cache entry."""

    topic: str
    summary: str
    key_statutes: List[str]
    elements: List[str]
    defenses: List[str]
    remedies: List[str]
    leading_cases: List[str]
    category: str
    subcategory: str = ""
    jurisdiction: str = "federal"
    authority_score: float = 0.75
    confidence: float = 0.80
    last_updated: str = ""
    staleness_days: int = 0
    related_topics: List[str] = dc_field(default_factory=list)
    practice_tips: List[str] = dc_field(default_factory=list)
    risk_factors: List[str] = dc_field(default_factory=list)
    legislative_notes: str = ""

    def __post_init__(self) -> None:
        if not self.last_updated:
            self.last_updated = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "topic": self.topic,
            "summary": self.summary,
            "key_statutes": self.key_statutes,
            "elements": self.elements,
            "defenses": self.defenses,
            "remedies": self.remedies,
            "leading_cases": self.leading_cases,
            "category": self.category,
            "subcategory": self.subcategory,
            "jurisdiction": self.jurisdiction,
            "authority_score": round(self.authority_score, 4),
            "confidence": round(self.confidence, 4),
            "last_updated": self.last_updated,
            "staleness_days": self.staleness_days,
            "related_topics": self.related_topics,
            "practice_tips": self.practice_tips,
            "risk_factors": self.risk_factors,
            "legislative_notes": self.legislative_notes,
        }

    def content_for_search(self) -> str:
        """Generate searchable text content from all fields."""
        parts = [
            self.topic,
            self.summary,
            " ".join(self.key_statutes),
            " ".join(self.elements),
            " ".join(self.defenses),
            " ".join(self.remedies),
            " ".join(self.leading_cases),
            self.category,
            self.subcategory,
            self.legislative_notes,
            " ".join(self.practice_tips),
        ]
        return " ".join(parts)

    def compute_hash(self) -> str:
        """Compute SHA-256 hash of the block content."""
        content = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(content.encode("utf-8")).hexdigest()


# ============================================================================
# DOCTRINE BLOCKS - STATUTORY CONSTRUCTION CANONS
# ============================================================================

DOCTRINE_BLOCKS: List[DoctrineCacheBlock] = [
    DoctrineCacheBlock(
        topic="plain_meaning_rule",
        summary="The plain meaning rule provides that where the statutory text is unambiguous, courts must apply the statute according to its plain terms without resort to extrinsic aids such as legislative history. The text is the law, and courts enforce what Congress wrote, not what it might have intended. Under textualism, the ordinary public meaning of the statutory language at the time of enactment controls. If the text yields a clear answer, the inquiry ends there. The Supreme Court has increasingly emphasized this approach, particularly under Justice Scalia's influence and continued by the current Court.",
        key_statutes=[
            "General canon of statutory construction",
            "Restatement (Third) of Statutory Interpretation (proposed)",
            "Antonin Scalia & Bryan Garner, Reading Law (2012)",
        ],
        elements=[
            "Statutory text must be examined first in every case",
            "Words are given their ordinary, everyday meaning unless a technical term of art",
            "If the text is plain and unambiguous, analysis ends with the text",
            "Courts presume Congress means what it says and says what it means",
            "Dictionary definitions from the era of enactment guide ordinary meaning",
            "Contextual reading considers the whole statute, not isolated phrases",
        ],
        defenses=[
            "Absurdity doctrine: plain meaning yields absurd or unreasonable results",
            "Scrivener's error: obvious drafting mistake contradicted by structure",
            "Ambiguity: reasonable minds can differ on the text's meaning",
            "Technical term of art requires specialized definition",
        ],
        remedies=[
            "Apply the statute as written when text is plain",
            "If ambiguous, proceed to structural and contextual analysis",
            "Resort to legislative history only if genuine ambiguity persists",
        ],
        leading_cases=[
            "Caminetti v. United States, 242 U.S. 470 (1917) (plain meaning controls even if broader than Congress intended)",
            "BedRoc Ltd. v. United States, 541 U.S. 176 (2004) (ordinary meaning of 'valuable minerals')",
            "Bostock v. Clayton County, 590 U.S. 644 (2020) (textualism applied to Title VII 'because of sex')",
            "Tanzin v. Tanvir, 592 U.S. 43 (2020) (plain meaning of 'appropriate relief' includes money damages)",
        ],
        category="statutory_construction",
        subcategory="textualism",
        authority_score=0.95,
        confidence=0.92,
        related_topics=["textualism", "purposivism", "whole_act_rule", "bostock_textualism"],
        practice_tips=[
            "Always start with the statutory text; courts will not look past clear language",
            "Use contemporaneous dictionaries to establish ordinary meaning at time of enactment",
            "Identify all plausible readings of the text before declaring it unambiguous",
        ],
        risk_factors=[
            "Opposing counsel may argue absurdity exception to escape plain meaning",
            "Some circuits are more willing to consider legislative history even when text seems clear",
        ],
    ),
    DoctrineCacheBlock(
        topic="textualism",
        summary="Textualism is the dominant method of statutory interpretation holding that the authoritative source of law is the text enacted by Congress and signed by the President (or passed over a veto). Under textualism, courts look to the ordinary public meaning of the statutory language at the time of enactment. Legislative history, purpose statements, and committee reports are considered unreliable guides because they were not voted on by both chambers and presented to the President. The Supreme Court's decision in Bostock v. Clayton County (2020) is the landmark modern application, holding that Title VII's prohibition on discrimination 'because of sex' encompasses sexual orientation and gender identity based on textual analysis alone.",
        key_statutes=[
            "U.S. Const. Art. I, Sec. 7 (Bicameralism and Presentment)",
            "Scalia & Garner, Reading Law: The Interpretation of Legal Texts (2012)",
        ],
        elements=[
            "Text of the statute is the sole authoritative expression of law",
            "Ordinary public meaning at time of enactment controls",
            "Words interpreted in their surrounding context (noscitur a sociis)",
            "Whole-act and whole-code canons apply to harmonize provisions",
            "Legislative history is not an authoritative source of meaning",
            "Semantic canons (ejusdem generis, expressio unius) are interpretive tools",
        ],
        defenses=[
            "Purpose-driven interpretation may yield different result where text is ambiguous",
            "Stare decisis may preserve purposivist readings from prior eras",
            "Legislative history may be relevant even to textualists for resolving ambiguity (Justice Kagan, Bostock concurrence approach)",
        ],
        remedies=[
            "Apply the text as written based on ordinary public meaning",
            "If multiple plausible readings exist, use structural and contextual canons",
            "Absurdity doctrine remains a narrow safety valve",
        ],
        leading_cases=[
            "Bostock v. Clayton County, 590 U.S. 644 (2020) (textualism applied to Title VII sex discrimination)",
            "New Prime Inc. v. Oliveira, 586 U.S. 105 (2019) (ordinary meaning of 'contracts of employment' at time of FAA enactment)",
            "Wisconsin Central Ltd. v. United States, 585 U.S. 274 (2018) (ordinary meaning of 'money' excludes stock options)",
            "Encino Motorcars v. Navarro, 584 U.S. 79 (2018) (text controls over purpose in FLSA exemptions)",
        ],
        category="statutory_construction",
        subcategory="textualism",
        authority_score=0.95,
        confidence=0.93,
        related_topics=["plain_meaning_rule", "purposivism", "bostock_textualism", "noscitur_a_sociis"],
        practice_tips=[
            "Frame arguments in textual terms first; the current Court is strongly textualist",
            "Support textual arguments with corpus linguistics data where available",
            "Even textualists accept that context matters: read the whole statute",
        ],
        risk_factors=[
            "Text-based arguments may produce outcomes Congress did not foresee or intend",
            "Lower courts may still rely on purposivist reasoning in certain circuits",
        ],
    ),
    DoctrineCacheBlock(
        topic="purposivism",
        summary="Purposivism holds that statutes should be interpreted in light of the purposes Congress sought to achieve. Under this approach, courts look beyond the bare text to legislative history, committee reports, and the broader statutory scheme to determine the evil Congress intended to remedy and the remedy it chose. While less dominant on the current Supreme Court, purposivism remains influential in many lower courts and is associated with the Legal Process school of Hart and Sacks. The approach was exemplified in Church of the Holy Trinity v. United States (1892) and remains a counterweight to strict textualism.",
        key_statutes=[
            "Hart & Sacks, The Legal Process (1958 tent. ed.)",
            "General canon: statutes should be interpreted to effectuate their purpose",
        ],
        elements=[
            "Identify the mischief or evil that Congress targeted",
            "Determine the remedy Congress chose to address that evil",
            "Interpret ambiguous text in light of that remedial purpose",
            "Legislative history (committee reports, floor debate) illuminates purpose",
            "Statutory purpose may override literal text in cases of absurdity or injustice",
            "Broad remedial statutes are construed liberally to advance their purpose",
        ],
        defenses=[
            "Plain meaning rule overrides purpose where text is clear",
            "Purpose arguments are manipulable: statutes serve multiple purposes at different levels of generality",
            "Committee reports reflect the views of staff, not the voting body",
            "Bicameralism and presentment objection: only the text was enacted into law",
        ],
        remedies=[
            "Interpret text in light of identified statutory purpose",
            "Resolve ambiguity in favor of the statute's remedial goals",
            "Consider the statute's place in the broader regulatory scheme",
        ],
        leading_cases=[
            "Church of the Holy Trinity v. United States, 143 U.S. 457 (1892) (purpose overrode literal text)",
            "King v. Burwell, 576 U.S. 473 (2015) (ACA interpreted in light of broader statutory scheme and purpose)",
            "FDA v. Brown & Williamson Tobacco Corp., 529 U.S. 120 (2000) (contextual reading in light of statutory purpose)",
            "Bob Jones University v. United States, 461 U.S. 574 (1983) (IRS charitable purpose requirement)",
        ],
        category="statutory_construction",
        subcategory="purposivism",
        authority_score=0.80,
        confidence=0.78,
        related_topics=["textualism", "legislative_history", "king_v_burwell", "remedial_construction"],
        practice_tips=[
            "Use purposivist arguments as a secondary or alternative framework alongside textualism",
            "Cite committee reports sparingly and identify the specific passage relied upon",
            "Framing: textualism and purposivism often converge on the same result",
        ],
        risk_factors=[
            "The current Supreme Court majority is skeptical of purposivism standing alone",
            "Purpose arguments at high levels of generality can justify almost any reading",
        ],
    ),
    DoctrineCacheBlock(
        topic="ejusdem_generis",
        summary="Ejusdem generis ('of the same kind') is a canon of statutory construction providing that when a general word or phrase follows a list of specific items, the general word is limited to the same class or category as the specific items. For example, if a statute lists 'cars, trucks, motorcycles, and other vehicles,' the general term 'other vehicles' would be limited to motorized road vehicles and would not include aircraft or boats. This canon prevents catch-all phrases from swallowing the specific terms that precede them and ensures the specific enumeration has independent meaning.",
        key_statutes=[
            "General canon of statutory construction (common law origin)",
            "Restatement of Statutory Interpretation (proposed)",
        ],
        elements=[
            "A statutory list of specific items must precede a general catch-all term",
            "The specific items must share a common characteristic or genus",
            "The general term is limited to items sharing that common characteristic",
            "The canon reflects the presumption that Congress legislates with precision",
            "Applies most strongly when the specific terms form a coherent category",
        ],
        defenses=[
            "The specific items may not share a common genus, defeating the canon",
            "Legislative history may indicate Congress intended the catch-all to be broad",
            "The general term may be defined elsewhere in the statute",
            "Absurdity may result from artificially narrowing the catch-all",
        ],
        remedies=[
            "Limit the general term to the class defined by the preceding specific terms",
            "If the canon does not apply, the general term retains its full breadth",
        ],
        leading_cases=[
            "Circuit City Stores v. Adams, 532 U.S. 105 (2001) (ejusdem generis applied to FAA exemption for 'other class of workers')",
            "Yates v. United States, 574 U.S. 528 (2015) (plurality applied ejusdem generis to 'tangible object' in Sarbanes-Oxley)",
            "Ali v. Federal Bureau of Prisons, 552 U.S. 214 (2008) (Court declined to apply ejusdem generis where catch-all was independent)",
            "Washington State Dept. of Social & Health Services v. Guardianship Estate of Keffeler, 537 U.S. 371 (2003)",
        ],
        category="statutory_construction",
        subcategory="semantic_canons",
        authority_score=0.88,
        confidence=0.85,
        related_topics=["noscitur_a_sociis", "expressio_unius", "plain_meaning_rule", "rule_of_lenity"],
        practice_tips=[
            "Identify the common genus shared by the enumerated terms before invoking the canon",
            "If arguing against the canon, show the specific terms lack a unifying characteristic",
            "The canon is a presumption, not a rule: it yields to clear contrary evidence",
        ],
        risk_factors=[
            "Courts may disagree on what common characteristic the specific terms share",
            "Ali v. Federal Bureau of Prisons shows the canon is not automatic",
        ],
    ),
    DoctrineCacheBlock(
        topic="noscitur_a_sociis",
        summary="Noscitur a sociis ('known by its associates') is a canon of statutory construction under which the meaning of an ambiguous word or phrase is determined by reference to the words and phrases with which it is associated. Unlike ejusdem generis, which requires a general term following a specific list, noscitur a sociis applies more broadly to any grouping of terms in a statute. If a word appears in a list of terms that share a common quality, the ambiguous word is presumed to share that quality. This canon helps courts give coherent, consistent meaning to related statutory terms.",
        key_statutes=[
            "General canon of statutory construction (common law origin)",
            "Jarecki v. G.D. Searle & Co., 367 U.S. 303, 307 (1961)",
        ],
        elements=[
            "An ambiguous word appears in a statutory list or grouping of terms",
            "The surrounding words share a common quality or characteristic",
            "The ambiguous word is interpreted to share that common quality",
            "Context drives meaning: words derive meaning from their neighbors",
            "The canon applies to any grouping, not just a specific-to-general list",
        ],
        defenses=[
            "The word may have an independent meaning not limited by its companions",
            "Surrounding terms may not share a clear common quality",
            "The canon is a guide, not a rigid rule, and yields to clear text",
        ],
        remedies=[
            "Interpret the ambiguous term consistently with its statutory neighbors",
            "If the canon does not apply, give the term its ordinary standalone meaning",
        ],
        leading_cases=[
            "Jarecki v. G.D. Searle & Co., 367 U.S. 303 (1961) ('discovery' interpreted by surrounding terms)",
            "Gustafson v. Alloyd Co., 513 U.S. 561 (1995) ('prospectus' interpreted by associated terms)",
            "Yates v. United States, 574 U.S. 528 (2015) ('tangible object' limited by surrounding terms in Sarbanes-Oxley)",
            "McDonnell v. United States, 579 U.S. 550 (2016) ('official act' narrowed by associated terms)",
        ],
        category="statutory_construction",
        subcategory="semantic_canons",
        authority_score=0.87,
        confidence=0.85,
        related_topics=["ejusdem_generis", "whole_act_rule", "plain_meaning_rule"],
        practice_tips=[
            "Use noscitur a sociis to narrow overly broad terms by reference to their statutory neighbors",
            "Distinguish from ejusdem generis: noscitur does not require a general-to-specific list structure",
            "Look at the full statutory phrase, not just the immediate neighbors",
        ],
        risk_factors=[
            "Opponents may argue the term has independent force regardless of neighbors",
            "Courts have sometimes declined to apply the canon where terms are sufficiently distinct",
        ],
    ),
    DoctrineCacheBlock(
        topic="expressio_unius",
        summary="Expressio unius est exclusio alterius ('the expression of one thing is the exclusion of the other') is a canon of statutory construction under which the explicit mention of certain items in a statute implies the intentional exclusion of items not mentioned. If Congress lists specific exceptions, conditions, or covered items, the inference is that omitted items were deliberately excluded. This canon rests on the assumption that Congress acts intentionally when it includes or omits statutory language. The canon is powerful but rebuttable: it can be overcome by evidence that the list was illustrative rather than exhaustive.",
        key_statutes=[
            "General canon of statutory construction (Latin maxim, common law origin)",
            "Widely cited in federal and state statutory interpretation",
        ],
        elements=[
            "The statute explicitly mentions certain items, conditions, or exceptions",
            "The mentioned items form a discernible category or list",
            "The omission of other items from the list is assumed intentional",
            "The negative inference: what is not mentioned is excluded",
            "Strongest when the list appears to be exhaustive rather than illustrative",
        ],
        defenses=[
            "The list may be illustrative (e.g., introduced by 'including' or 'such as')",
            "Legislative history may show the omission was inadvertent, not deliberate",
            "The dog that didn't bark: silence may reflect oversight, not exclusion",
            "Other statutory provisions may cover the omitted items",
        ],
        remedies=[
            "If the canon applies, the omitted items are excluded from the statute's scope",
            "If the list is illustrative, additional items may be covered",
        ],
        leading_cases=[
            "Russello v. United States, 464 U.S. 16 (1983) (inclusion of 'interest' in one RICO provision, omission from another, was intentional)",
            "Hamdan v. Rumsfeld, 548 U.S. 557 (2006) (express grant of jurisdiction in one provision implied exclusion in another)",
            "Babb v. Wilkie, 589 U.S. 399 (2020) (statutory provision listing specific requirements implies others excluded)",
            "NLRB v. SW General Inc., 580 U.S. 288 (2017) (express exception for one category implies exclusion of others)",
        ],
        category="statutory_construction",
        subcategory="semantic_canons",
        authority_score=0.87,
        confidence=0.84,
        related_topics=["ejusdem_generis", "noscitur_a_sociis", "presumption_against_surplusage"],
        practice_tips=[
            "Look for Congress including a term in one section and omitting it from a parallel section: strongest expressio unius argument",
            "Counter the canon by showing the list is introduced by 'including but not limited to'",
            "Be prepared for the argument that silence is ambiguous, not dispositive",
        ],
        risk_factors=[
            "Courts increasingly recognize the canon can be overridden by context and purpose",
            "If the list is clearly illustrative, expressio unius does not apply",
        ],
    ),
    DoctrineCacheBlock(
        topic="rule_of_lenity",
        summary="The rule of lenity is a canon of statutory construction providing that ambiguity in criminal statutes must be resolved in favor of the defendant. The rule ensures fair notice of what conduct is criminalized and restricts the scope of criminal liability to cases clearly covered by the statute. It applies only when, after exhausting all tools of statutory construction, genuine ambiguity remains. The Supreme Court has applied the rule narrowly, requiring 'grievous ambiguity' before it controls (Muscarello v. United States). The rule also extends to civil penalty provisions and statutes that impose quasi-criminal sanctions.",
        key_statutes=[
            "General canon of statutory construction (common law origin)",
            "Due Process Clause, U.S. Const. Amend. V and XIV",
        ],
        elements=[
            "The statute imposes criminal penalties or quasi-criminal sanctions",
            "The statutory text is genuinely ambiguous after applying all interpretive tools",
            "The ambiguity goes to the scope of criminalized conduct, not peripheral matters",
            "The rule resolves the ambiguity in favor of the defendant (narrower reading)",
            "Fair notice principle: citizens must be able to understand what is prohibited",
        ],
        defenses=[
            "The statute is not genuinely ambiguous; one reading is clearly correct",
            "Legislative history resolves the ambiguity without need for the lenity rule",
            "The statute is civil or regulatory, not criminal",
            "Ambiguity is only 'grievous' enough if no other tool resolves it",
        ],
        remedies=[
            "Adopt the narrower interpretation that favors the defendant",
            "If ambiguity is resolved by other canons, the rule of lenity does not apply",
        ],
        leading_cases=[
            "Yates v. United States, 574 U.S. 528 (2015) (lenity applied to 'tangible object' in 18 USC 1519)",
            "Muscarello v. United States, 524 U.S. 125 (1998) (lenity requires 'grievous ambiguity')",
            "McNally v. United States, 483 U.S. 350 (1987) (mail fraud statute narrowly construed)",
            "Dubin v. United States, 599 U.S. 110 (2023) (aggravated identity theft narrowly construed)",
        ],
        category="statutory_construction",
        subcategory="substantive_canons",
        authority_score=0.88,
        confidence=0.85,
        related_topics=["plain_meaning_rule", "textualism", "void_for_vagueness"],
        practice_tips=[
            "Invoke lenity only after demonstrating genuine ambiguity through all other tools",
            "Pair the lenity argument with due process fair notice concerns",
            "Note that the current Court requires 'grievous' ambiguity, not merely 'some' ambiguity",
        ],
        risk_factors=[
            "Courts rarely find ambiguity grievous enough for lenity to control",
            "The rule is a tiebreaker of last resort, not a first-line argument",
        ],
    ),
    DoctrineCacheBlock(
        topic="avoidance_canon",
        summary="The constitutional avoidance canon instructs courts to adopt a statutory interpretation that avoids raising serious constitutional questions, even if another reading might be more natural. The canon comes in two forms: classical avoidance (if one reading is unconstitutional and another is constitutional, choose the constitutional reading) and modern avoidance (if one reading raises serious constitutional doubts, choose the reading that avoids those doubts). The modern version is more potent because it does not require the court to actually find a constitutional violation. Critics argue the canon distorts legislative meaning to avoid hypothetical constitutional issues.",
        key_statutes=[
            "General canon of statutory construction",
            "Ashwander v. TVA, 297 U.S. 288, 348 (1936) (Brandeis concurrence, avoidance principles)",
        ],
        elements=[
            "The statute admits of two plausible interpretations",
            "One interpretation raises serious constitutional questions",
            "The alternative interpretation is fairly possible from the text",
            "Courts adopt the interpretation that avoids constitutional doubts",
            "The canon preserves congressional enactments from invalidation",
        ],
        defenses=[
            "The clear text cannot be tortured to avoid constitutional questions",
            "The 'serious constitutional question' is speculative or remote",
            "Avoidance distorts the statute beyond fair reading",
            "Congress may have intended to test constitutional boundaries",
        ],
        remedies=[
            "Adopt the constitutionally permissible interpretation",
            "If avoidance distorts the statute, address the constitutional question directly",
        ],
        leading_cases=[
            "NLRB v. Catholic Bishop, 440 U.S. 490 (1979) (avoided First Amendment question by construing NLRA narrowly)",
            "Edward J. DeBartolo Corp. v. Florida Gulf Coast Building Trades Council, 485 U.S. 568 (1988)",
            "Zadvydas v. Davis, 533 U.S. 678 (2001) (avoided indefinite detention due process concern by implying time limit)",
            "Bond v. United States, 572 U.S. 844 (2014) (avoided federalism concerns by narrowing chemical weapons statute)",
        ],
        category="statutory_construction",
        subcategory="substantive_canons",
        authority_score=0.88,
        confidence=0.84,
        related_topics=["plain_meaning_rule", "clear_statement_rules", "delegation_doctrine"],
        practice_tips=[
            "Use the avoidance canon to argue for a narrower reading that sidesteps constitutional issues",
            "Must show the alternative reading is 'fairly possible' from the text, not forced",
            "Identify the specific constitutional provision at issue: vague references to 'constitutional doubt' are insufficient",
        ],
        risk_factors=[
            "Textualist justices are skeptical of avoidance if it distorts the plain text",
            "The canon can be used to rewrite statutes sub silentio",
        ],
    ),
    DoctrineCacheBlock(
        topic="whole_act_rule",
        summary="The whole act rule is a canon of statutory construction requiring that each provision of a statute be interpreted in the context of the entire statute, not in isolation. A word or phrase that might be ambiguous in one section may be clarified by its use elsewhere in the same act. The canon reflects the presumption that Congress drafts statutes as coherent, integrated wholes. Related principles include the presumption against surplusage (every word has meaning), the consistent-usage presumption (same term means the same thing throughout the act), and the meaningful-variation canon (different terms are used to convey different meanings).",
        key_statutes=[
            "General canon of statutory construction",
            "King v. Burwell, 576 U.S. 473, 492 (2015)",
        ],
        elements=[
            "Each provision must be read in context of the entire statute",
            "Same word used in different sections is presumed to have the same meaning",
            "Different words in parallel provisions are presumed to have different meanings",
            "No provision should be rendered superfluous or meaningless",
            "The statute's overall structure and design inform individual provisions",
        ],
        defenses=[
            "Context may require a term to have different meanings in different sections",
            "Poor drafting may produce inconsistency that cannot be harmonized",
            "The Omnibus provision may use language differently than targeted sections",
        ],
        remedies=[
            "Harmonize provisions to give effect to the entire statute",
            "If irreconcilable conflict exists, the more specific provision controls",
        ],
        leading_cases=[
            "King v. Burwell, 576 U.S. 473 (2015) ('established by the State' interpreted in context of entire ACA)",
            "FDA v. Brown & Williamson, 529 U.S. 120 (2000) (FDCA read as a whole with tobacco legislation)",
            "Utility Air Regulatory Group v. EPA, 573 U.S. 302 (2014) (Clean Air Act provisions harmonized)",
            "Yates v. United States, 574 U.S. 528 (2015) (Sarbanes-Oxley provision read in light of statutory structure)",
        ],
        category="statutory_construction",
        subcategory="structural_canons",
        authority_score=0.90,
        confidence=0.88,
        related_topics=["presumption_against_surplusage", "plain_meaning_rule", "textualism"],
        practice_tips=[
            "Map all uses of the key term throughout the statute before making your argument",
            "Cross-reference definitions sections: defined terms override ordinary meaning",
            "Show how your reading makes the statute internally consistent while the opposing reading creates conflict",
        ],
        risk_factors=[
            "Complex omnibus statutes may use terms inconsistently due to multi-committee drafting",
            "Courts may disagree on which provisions should be harmonized versus which control",
        ],
    ),
    DoctrineCacheBlock(
        topic="chevron_deference",
        summary="Chevron deference was the foundational administrative law doctrine requiring courts to defer to an agency's reasonable interpretation of an ambiguous statute it administers. Under Chevron's two-step framework: (1) courts ask whether Congress has directly spoken to the precise question at issue; (2) if the statute is ambiguous, courts defer to the agency's interpretation if it is 'permissible' or reasonable. Chevron was OVERRULED by Loper Bright Enterprises v. Ramos (2024), which held that courts must exercise independent judgment in interpreting statutes under APA Section 706 and may not defer to agency interpretations merely because the statute is ambiguous. However, Chevron-era precedents applying the framework are not automatically disturbed under principles of stare decisis.",
        key_statutes=[
            "5 USC 706 (APA scope of review)",
            "Chevron U.S.A. Inc. v. NRDC, 467 U.S. 837 (1984) (OVERRULED)",
            "Loper Bright Enterprises v. Ramos, 603 U.S. ___ (2024) (overruling Chevron)",
        ],
        elements=[
            "HISTORICAL (pre-Loper Bright): Step 1 - has Congress directly spoken to the issue?",
            "HISTORICAL: Step 2 - if ambiguous, is the agency interpretation reasonable/permissible?",
            "POST-LOPER BRIGHT: Courts exercise independent judgment on questions of statutory meaning",
            "POST-LOPER BRIGHT: Agency interpretation may be informative but is not entitled to deference",
            "Prior Chevron-based holdings are not automatically overruled (stare decisis applies)",
            "Skidmore deference survives: agency view is persuasive based on thoroughness, consistency, and expertise",
        ],
        defenses=[
            "Loper Bright does not disturb prior holdings that applied Chevron (stare decisis)",
            "Skidmore persuasive weight remains available for well-reasoned agency positions",
            "Congress can still expressly delegate interpretive authority to agencies",
            "Agency expertise remains relevant to complex technical/scientific questions of fact",
        ],
        remedies=[
            "Courts must independently interpret statutes using traditional tools of construction",
            "Agency interpretations inform but do not control judicial meaning",
            "Challenge stale agency interpretations that were upheld only under Chevron deference",
        ],
        leading_cases=[
            "Chevron U.S.A. Inc. v. NRDC, 467 U.S. 837 (1984) (established two-step deference framework) (OVERRULED)",
            "Loper Bright Enterprises v. Ramos, 603 U.S. ___ (2024) (overruled Chevron; courts exercise independent judgment under APA 706)",
            "Skidmore v. Swift & Co., 323 U.S. 134 (1944) (persuasive weight based on agency thoroughness and consistency)",
            "Kisor v. Wilkie, 588 U.S. 558 (2019) (narrowed Auer deference to agency's own regulations)",
            "West Virginia v. EPA, 597 U.S. 697 (2022) (major questions doctrine as limit on agency power)",
        ],
        category="regulatory_rulemaking",
        subcategory="judicial_deference",
        authority_score=0.95,
        confidence=0.90,
        related_topics=["loper_bright", "skidmore_deference", "major_questions_doctrine", "apa_rulemaking"],
        practice_tips=[
            "Post-Loper Bright, frame arguments around statutory text and traditional interpretive tools, not agency deference",
            "When defending agency action, emphasize Skidmore persuasive weight and agency expertise",
            "Identify whether the challenged agency interpretation was upheld solely on Chevron grounds: if so, it may be vulnerable",
            "Prior Chevron holdings are protected by stare decisis unless independently wrong",
        ],
        risk_factors=[
            "Post-Loper Bright landscape is rapidly evolving; lower courts are still working out implications",
            "Challenges to long-standing agency interpretations are now more viable",
            "Agencies relying on Chevron-era positions should prepare independent statutory justifications",
        ],
        legislative_notes="Loper Bright represents a seismic shift in administrative law. All regulatory analysis must now account for the post-Chevron framework.",
    ),
    DoctrineCacheBlock(
        topic="loper_bright",
        summary="Loper Bright Enterprises v. Ramos (2024) overruled Chevron deference, holding that the Administrative Procedure Act requires courts to exercise independent judgment in determining the meaning of federal statutes, and that courts may not defer to an agency's interpretation of law merely because a statute is ambiguous. The Court held that APA Section 706 directs courts to 'decide all relevant questions of law' and 'determine the meaning' of statutory provisions, which is incompatible with a rule requiring deference to agency legal interpretations. Chief Justice Roberts, writing for the majority, emphasized that Chevron was a judicial invention that contravened Marbury v. Madison's principle that it is 'emphatically the province and duty of the judicial department to say what the law is.'",
        key_statutes=[
            "5 USC 706 (APA scope of review)",
            "Loper Bright Enterprises v. Ramos, 603 U.S. ___ (2024)",
            "Magnuson-Stevens Fishery Conservation and Management Act, 16 USC 1801 et seq. (underlying statute in Loper Bright)",
        ],
        elements=[
            "APA Section 706 requires courts to decide all relevant questions of law",
            "Courts must determine the meaning of statutory provisions using independent judgment",
            "Deference to agency legal interpretations based solely on statutory ambiguity is impermissible",
            "Agency expertise remains relevant and may be persuasive (Skidmore weight)",
            "Prior decisions that relied on Chevron are not automatically overruled (stare decisis)",
            "Congress may still expressly delegate gap-filling authority to agencies",
        ],
        defenses=[
            "Stare decisis protects Chevron-era holdings unless independently wrong",
            "Skidmore persuasiveness standard survives for well-reasoned agency positions",
            "Express congressional delegations of interpretive authority remain valid",
            "Agency technical expertise on factual/scientific questions is still relevant",
        ],
        remedies=[
            "Challenge agency interpretations that were upheld solely on Chevron deference",
            "Seek independent judicial interpretation of ambiguous statutory provisions",
            "Argue that prior Chevron-based holdings were independently erroneous",
        ],
        leading_cases=[
            "Loper Bright Enterprises v. Ramos, 603 U.S. ___ (2024) (overruled Chevron)",
            "Marbury v. Madison, 5 U.S. (1 Cranch) 137 (1803) (judicial duty to say what the law is)",
            "Chevron U.S.A. Inc. v. NRDC, 467 U.S. 837 (1984) (OVERRULED by Loper Bright)",
            "Skidmore v. Swift & Co., 323 U.S. 134 (1944) (persuasive weight standard survives)",
        ],
        category="regulatory_rulemaking",
        subcategory="judicial_deference",
        authority_score=0.98,
        confidence=0.95,
        related_topics=["chevron_deference", "skidmore_deference", "major_questions_doctrine", "apa_rulemaking"],
        practice_tips=[
            "All new regulatory challenges should be framed under the Loper Bright independent-judgment standard",
            "Identify agency interpretations that survived only because of Chevron: those are now ripe for challenge",
            "When defending agency action, lead with the statutory text and show the agency reading is the best reading, not merely permissible",
        ],
        risk_factors=[
            "The full scope of Loper Bright's implications is still being developed in the lower courts",
            "Regulatory uncertainty has increased as agencies can no longer rely on Chevron as a shield",
            "Industries that benefited from Chevron deference to favorable agency interpretations now face litigation risk",
        ],
        legislative_notes="Loper Bright was decided June 28, 2024. It is the most significant administrative law decision since Chevron itself. All deference analysis must be updated accordingly.",
    ),
    DoctrineCacheBlock(
        topic="major_questions_doctrine",
        summary="The major questions doctrine holds that courts should not interpret ambiguous statutory provisions to authorize agency actions of vast economic and political significance unless Congress has clearly spoken to authorize such actions. The doctrine was formally articulated in West Virginia v. EPA (2022), where the Court struck down the EPA's Clean Power Plan on the ground that Congress had not clearly authorized the agency to restructure the nation's energy grid. The doctrine operates as a clear-statement rule: if the agency claims authority to make decisions of enormous economic or political import, it must point to clear statutory authorization, not merely arguable textual hooks. The doctrine survived and was strengthened by Loper Bright.",
        key_statutes=[
            "West Virginia v. EPA, 597 U.S. 697 (2022)",
            "Biden v. Nebraska, 600 U.S. 477 (2023)",
            "Clean Air Act, 42 USC 7401 et seq. (underlying statute in West Virginia)",
        ],
        elements=[
            "The agency claims authority to make a decision of vast economic and political significance",
            "The statutory basis for the claimed authority is ambiguous or involves a novel interpretation",
            "Courts require clear congressional authorization for such extraordinary assertions of power",
            "The agency is acting in an area where it has not traditionally regulated",
            "The claimed authority would fundamentally transform an industry or sector of the economy",
        ],
        defenses=[
            "Congress provided clear and specific authorization for the agency action",
            "The action falls within the agency's traditional domain and historical practice",
            "The economic or political significance does not rise to 'major questions' level",
            "The agency is implementing clear statutory directives, not asserting new authority",
        ],
        remedies=[
            "Strike down agency action lacking clear congressional authorization",
            "Require Congress to act if a major policy decision is desired",
            "Narrow the scope of agency rulemaking to clearly authorized areas",
        ],
        leading_cases=[
            "West Virginia v. EPA, 597 U.S. 697 (2022) (formally articulated the major questions doctrine)",
            "Biden v. Nebraska, 600 U.S. 477 (2023) (student loan forgiveness exceeded HEROES Act authority)",
            "King v. Burwell, 576 U.S. 473 (2015) (precursor: major question resolved by Court, not agency)",
            "FDA v. Brown & Williamson, 529 U.S. 120 (2000) (precursor: FDA lacked authority to regulate tobacco)",
            "Utility Air Regulatory Group v. EPA, 573 U.S. 302 (2014) (precursor: EPA could not expand PSD permitting to all GHG sources)",
        ],
        category="regulatory_rulemaking",
        subcategory="substantive_limits",
        authority_score=0.95,
        confidence=0.90,
        related_topics=["chevron_deference", "loper_bright", "delegation_doctrine", "nondelegation"],
        practice_tips=[
            "When challenging major agency action, lead with the major questions doctrine: it is the most powerful current tool",
            "Define 'vast economic and political significance' concretely: cite dollar figures, affected population, industry transformation",
            "When defending, show the agency has long exercised this type of authority and Congress acquiesced",
        ],
        risk_factors=[
            "The threshold for 'major question' is not precisely defined; courts may disagree",
            "The doctrine may be applied selectively to disfavored regulations",
            "Agencies face uncertainty about what actions will trigger major questions scrutiny",
        ],
    ),
    DoctrineCacheBlock(
        topic="apa_notice_and_comment",
        summary="Notice-and-comment rulemaking under APA Section 553 is the standard process by which federal agencies promulgate legislative rules. The agency must publish a Notice of Proposed Rulemaking (NPRM) in the Federal Register, provide a meaningful comment period (typically 30-60 days, often longer for complex rules), consider and respond to significant comments, and publish a final rule with a statement of basis and purpose. The final rule must be a 'logical outgrowth' of the proposed rule. Failure to follow these procedural requirements renders the rule vulnerable to challenge as 'arbitrary and capricious' or 'not in accordance with law' under APA Section 706.",
        key_statutes=[
            "5 USC 553 (APA informal rulemaking procedures)",
            "5 USC 706 (APA judicial review)",
            "44 USC 3501 et seq. (Paperwork Reduction Act)",
            "5 USC 601-612 (Regulatory Flexibility Act)",
            "2 USC 1501 et seq. (Unfunded Mandates Reform Act)",
            "Executive Order 12866 (Regulatory Planning and Review)",
        ],
        elements=[
            "Agency publishes NPRM in the Federal Register with statutory authority cited",
            "Meaningful opportunity for public comment must be provided",
            "Agency must consider and respond to significant comments received",
            "Final rule must be a logical outgrowth of the proposed rule",
            "Statement of basis and purpose must accompany the final rule",
            "Final rule published in Federal Register with effective date (generally 30 days after publication)",
            "Agency must comply with additional procedural requirements (RFA, PRA, UMRA, E.O. 12866)",
        ],
        defenses=[
            "Good cause exception: notice and comment impracticable, unnecessary, or contrary to public interest (5 USC 553(b)(B))",
            "Interpretive rules and policy statements are exempt (5 USC 553(b)(A))",
            "Rules relating to agency management, personnel, or public property are exempt",
            "Foreign affairs and military function exceptions",
        ],
        remedies=[
            "Challenge final rule as arbitrary and capricious under APA 706(2)(A)",
            "Challenge procedural deficiencies (inadequate notice, failure to respond to comments)",
            "Seek vacatur of rule that is not a logical outgrowth of the NPRM",
            "Congressional Review Act disapproval resolution (5 USC 801-808)",
        ],
        leading_cases=[
            "Motor Vehicle Mfrs. Assn. v. State Farm, 463 U.S. 29 (1983) (arbitrary and capricious review of rulemaking)",
            "Vermont Yankee Nuclear Power Corp. v. NRDC, 435 U.S. 519 (1978) (courts cannot impose procedures beyond APA minimum)",
            "Perez v. Mortgage Bankers Assn., 575 U.S. 92 (2015) (interpretive rules do not require notice-and-comment)",
            "Encino Motorcars v. Navarro, 584 U.S. 79 (2018) (unexplained regulatory reversal is arbitrary and capricious)",
            "FCC v. Fox Television Stations, 556 U.S. 502 (2009) (change in policy requires reasoned explanation)",
        ],
        category="regulatory_rulemaking",
        subcategory="procedure",
        authority_score=0.92,
        confidence=0.90,
        related_topics=["chevron_deference", "loper_bright", "arbitrary_and_capricious", "major_questions_doctrine"],
        practice_tips=[
            "Submit detailed comments during the notice-and-comment period: this preserves issues for judicial review",
            "Challenge the logical-outgrowth requirement if the final rule differs substantially from the NPRM",
            "Track the agency's response to your specific comments in the preamble to the final rule",
        ],
        risk_factors=[
            "Failure to comment during the notice-and-comment period may forfeit the right to challenge on judicial review",
            "The good cause exception is narrowly construed but agencies sometimes invoke it aggressively",
        ],
    ),
    DoctrineCacheBlock(
        topic="congressional_procedure_filibuster",
        summary="The filibuster is a Senate procedural mechanism allowing unlimited debate on most measures, effectively requiring 60 votes (three-fifths of Senators duly chosen and sworn) to invoke cloture and proceed to a final vote. The filibuster is not in the Constitution; it derives from Senate rules (Rule XXII). Cloture can be invoked by a petition signed by 16 Senators, followed by a vote requiring three-fifths (currently 60) to end debate. Exceptions include budget reconciliation (simple majority), judicial confirmations (simple majority since 2013/2017 nuclear option changes), and the Congressional Review Act (simple majority for disapproval resolutions). The filibuster has been reformed repeatedly: the 'nuclear option' eliminated the 60-vote threshold for executive branch nominees (2013) and Supreme Court nominees (2017).",
        key_statutes=[
            "Senate Rule XXII (cloture rule)",
            "U.S. Const. Art. I, Sec. 5 (each chamber sets its own rules)",
            "Congressional Budget Act of 1974, 2 USC 641 (reconciliation)",
        ],
        elements=[
            "Any Senator may speak for unlimited time on most measures unless cloture is invoked",
            "Cloture requires petition of 16 Senators followed by three-fifths vote (60)",
            "Post-cloture debate is limited to 30 hours",
            "Budget reconciliation bills require only a simple majority (51 votes)",
            "Executive and judicial nominations require only simple majority (post-nuclear option)",
            "The Byrd Rule prohibits extraneous provisions in reconciliation bills",
        ],
        defenses=[
            "Reconciliation bypass: budget-related measures can avoid the filibuster",
            "Nuclear option: Senate can change its rules by simple majority vote",
            "Unanimous consent agreements can limit debate without cloture",
            "Some statutes provide expedited procedures bypassing the filibuster (e.g., CRA, TPA)",
        ],
        remedies=[
            "File cloture petition and secure 60 votes",
            "Use budget reconciliation for measures that can be framed as budgetary",
            "Negotiate unanimous consent agreements",
            "Invoke the nuclear option to change the threshold (extreme measure)",
        ],
        leading_cases=[
            "Not primarily a judicial doctrine; governed by Senate rules and precedent",
            "Senate precedent: November 2013 (nuclear option for executive/lower court nominees)",
            "Senate precedent: April 2017 (nuclear option extended to Supreme Court nominees)",
        ],
        category="congressional_procedure",
        subcategory="senate_rules",
        authority_score=0.85,
        confidence=0.88,
        related_topics=["reconciliation", "byrd_rule", "cloture", "unanimous_consent"],
        practice_tips=[
            "For legislative strategy: assess whether the measure can survive the Byrd Rule for reconciliation",
            "Track cloture votes as a leading indicator of a bill's viability",
            "Understand that the 60-vote threshold applies to proceeding to a vote, not the vote itself",
        ],
        risk_factors=[
            "The filibuster can be modified or eliminated at any time by simple majority vote",
            "Reconciliation is limited to taxing, spending, and debt limit provisions under the Byrd Rule",
        ],
    ),
    DoctrineCacheBlock(
        topic="budget_reconciliation",
        summary="Budget reconciliation is a special legislative process under the Congressional Budget Act of 1974 that allows certain tax, spending, and debt limit legislation to pass the Senate with a simple majority vote (51), bypassing the 60-vote filibuster threshold. Reconciliation begins when the annual budget resolution includes reconciliation instructions directing specific committees to report legislation achieving specified budgetary targets. The resulting reconciliation bill is subject to the Byrd Rule (Section 313 of the Budget Act), which prohibits 'extraneous' provisions that do not change outlays or revenues, produce changes in outlays or revenues that are merely incidental to the non-budgetary components, increase the deficit beyond the budget window, or fall outside the committee's jurisdiction. The Senate Parliamentarian advises on Byrd Rule compliance. Reconciliation has been used for major legislation including the Tax Cuts and Jobs Act (2017), ACA (2010), and Inflation Reduction Act (2022).",
        key_statutes=[
            "Congressional Budget Act of 1974, 2 USC 641 (reconciliation)",
            "Byrd Rule, 2 USC 644 (extraneous provisions)",
            "Congressional Budget and Impoundment Control Act",
        ],
        elements=[
            "Budget resolution must include reconciliation instructions to committees",
            "Instructions specify committee, dollar amount, and deadline",
            "Committees report reconciliation legislation to Budget Committee",
            "Budget Committee assembles omnibus reconciliation bill",
            "Senate debate limited to 20 hours (no filibuster)",
            "Simple majority required for passage (51 votes, or 50 + VP tiebreaker)",
            "Byrd Rule prohibits extraneous provisions",
            "Senate Parliamentarian advises on Byrd Rule points of order",
        ],
        defenses=[
            "Vice President can overrule the Parliamentarian (extremely rare)",
            "60-vote waiver can overcome a Byrd Rule point of order",
            "Provisions with merely incidental budgetary effects are excluded by Byrd Rule",
        ],
        remedies=[
            "Strip extraneous provisions to comply with the Byrd Rule",
            "Seek 60-vote waiver for provisions that fail the Byrd Rule",
            "Redesign policy provisions to have direct budgetary impact",
        ],
        leading_cases=[
            "Not primarily a judicial doctrine; governed by congressional rules and precedent",
            "Notable uses: Tax Cuts and Jobs Act (2017), ACA (2010), Inflation Reduction Act (2022), ARPA (2021)",
        ],
        category="congressional_procedure",
        subcategory="budget_process",
        authority_score=0.88,
        confidence=0.87,
        related_topics=["congressional_procedure_filibuster", "byrd_rule", "appropriations", "debt_ceiling"],
        practice_tips=[
            "Assess Byrd Rule compliance early when drafting reconciliation provisions",
            "The Parliamentarian's advice is critical: engage early on borderline provisions",
            "Only one reconciliation bill per budget resolution topic (spending, revenue, debt limit) per fiscal year",
        ],
        risk_factors=[
            "The Byrd Rule can strip key policy provisions from reconciliation bills",
            "Reconciliation cannot be used for all policy objectives: only those with direct budgetary effects",
            "The budget window constraint may require sunset provisions (as in TCJA individual provisions)",
        ],
    ),
    DoctrineCacheBlock(
        topic="preemption_express",
        summary="Express preemption occurs when Congress explicitly states in a statute that federal law supersedes state law on a particular subject. The preemption clause must be interpreted according to its terms using standard tools of statutory construction. Courts begin with the presumption against preemption in areas of traditional state regulation (Rice v. Santa Fe Elevator Corp.), meaning that express preemption clauses are often construed narrowly. However, the scope of express preemption clauses varies widely: some are broad (ERISA Section 514 preempts all state laws that 'relate to' employee benefit plans) while others are narrow (specifying particular types of state laws that are preempted). Savings clauses may preserve some state law authority even within an express preemption framework.",
        key_statutes=[
            "U.S. Const. Art. VI, Cl. 2 (Supremacy Clause)",
            "ERISA Section 514, 29 USC 1144 (broad express preemption)",
            "FAAAA, 49 USC 14501(c) (airline/trucking preemption)",
            "National Bank Act, 12 USC 21 et seq. (banking preemption)",
            "Federal Arbitration Act, 9 USC 1-16 (arbitration preemption)",
        ],
        elements=[
            "Federal statute contains an explicit preemption clause",
            "The scope of the preemption clause is determined by its text",
            "Presumption against preemption applies in areas of traditional state regulation",
            "Savings clauses may carve out areas of preserved state authority",
            "Preemption clause is interpreted using standard canons of construction",
            "The breadth of preemption depends on the specific statutory language",
        ],
        defenses=[
            "The state law falls outside the scope of the preemption clause",
            "A savings clause preserves the specific state law at issue",
            "Presumption against preemption applies (traditional state regulation area)",
            "The preemption clause is ambiguous and should be construed narrowly",
        ],
        remedies=[
            "State law is preempted and unenforceable to the extent it conflicts",
            "Federal law controls in the preempted field",
            "State regulation preserved by savings clause remains enforceable",
        ],
        leading_cases=[
            "Cipollone v. Liggett Group, 505 U.S. 504 (1992) (cigarette labeling express preemption clause analyzed)",
            "Medtronic v. Lohr, 518 U.S. 470 (1996) (MDA preemption clause interpreted narrowly)",
            "Riegel v. Medtronic, 552 U.S. 312 (2008) (MDA preemption clause applied to PMA devices)",
            "Gobeille v. Liberty Mutual, 577 U.S. 312 (2016) (ERISA preemption of state health care reporting)",
        ],
        category="preemption",
        subcategory="express",
        authority_score=0.92,
        confidence=0.88,
        related_topics=["preemption_field", "preemption_conflict", "supremacy_clause", "presumption_against_preemption"],
        practice_tips=[
            "Start with the text of the preemption clause: its language controls the scope of preemption",
            "Check for savings clauses that may preserve state law authority",
            "Invoke the presumption against preemption when the state law addresses a traditional state concern",
        ],
        risk_factors=[
            "Broad preemption clauses like ERISA Section 514 can preempt a wide range of state laws",
            "The presumption against preemption may be weakened where the federal regulatory scheme is comprehensive",
        ],
    ),
    DoctrineCacheBlock(
        topic="preemption_field",
        summary="Field preemption occurs when the federal regulatory scheme is so pervasive and comprehensive that it occupies an entire field of regulation, leaving no room for state law to operate even in the absence of a direct conflict. Courts infer congressional intent to occupy the field from the pervasiveness of the federal scheme, the dominance of the federal interest, or the objective of uniformity in regulation. Field preemption is found most commonly in areas like immigration, nuclear safety, and foreign affairs where the federal interest is dominant. The presumption against preemption in areas of traditional state regulation makes field preemption difficult to establish where states have historically regulated.",
        key_statutes=[
            "U.S. Const. Art. VI, Cl. 2 (Supremacy Clause)",
            "Immigration and Nationality Act, 8 USC 1101 et seq. (immigration field preemption)",
            "Atomic Energy Act, 42 USC 2011 et seq. (nuclear safety field preemption)",
        ],
        elements=[
            "The federal regulatory scheme is so pervasive it occupies the entire field",
            "Congressional intent to preempt the field may be inferred from the scheme's comprehensiveness",
            "The federal interest in the area is dominant",
            "The nature of the regulated subject demands uniformity",
            "State regulation within the field is preempted even without direct conflict",
        ],
        defenses=[
            "The federal scheme is not comprehensive enough to occupy the entire field",
            "Congress preserved a role for state regulation through savings clauses or legislative history",
            "The area is one of traditional state regulation with a strong presumption against preemption",
            "The state law operates in a gap that federal law does not address",
        ],
        remedies=[
            "State law is preempted in the occupied field",
            "Federal regulation is the exclusive source of law in the field",
            "State laws outside the occupied field remain valid",
        ],
        leading_cases=[
            "Arizona v. United States, 567 U.S. 387 (2012) (federal immigration law occupies the field in key areas)",
            "Pacific Gas & Electric Co. v. State Energy Resources Conservation & Dev. Comm'n, 461 U.S. 190 (1983) (nuclear safety but not economics)",
            "Gade v. National Solid Wastes Mgmt Assn., 505 U.S. 88 (1992) (OSH Act field preemption of state safety standards)",
            "Buckman Co. v. Plaintiffs' Legal Committee, 531 U.S. 341 (2001) (fraud-on-the-FDA field preemption)",
        ],
        category="preemption",
        subcategory="field",
        authority_score=0.90,
        confidence=0.85,
        related_topics=["preemption_express", "preemption_conflict", "supremacy_clause"],
        practice_tips=[
            "Demonstrate the pervasiveness of the federal scheme with detailed statutory mapping",
            "Show congressional intent to occupy the field through legislative history and scheme design",
            "If defending state law, emphasize gaps in the federal scheme that show Congress did not intend to occupy the field",
        ],
        risk_factors=[
            "Field preemption is difficult to establish where the area is traditionally state-regulated",
            "Courts may find partial field preemption, preempting only certain aspects of state regulation",
        ],
    ),
    DoctrineCacheBlock(
        topic="preemption_conflict",
        summary="Conflict preemption arises when compliance with both federal and state law is impossible (impossibility preemption) or when state law stands as an obstacle to the accomplishment of the full purposes and objectives of Congress (obstacle preemption). Impossibility preemption is the narrowest form: it applies only when a regulated entity literally cannot comply with both federal and state requirements simultaneously. Obstacle preemption is broader and more contested: it requires courts to identify the purposes and objectives of the federal statute and determine whether state law impedes them. The Court in Wyeth v. Levine (2009) emphasized that impossibility must be actual, not hypothetical, and that the existence of a federal regulatory floor does not preempt state laws that provide additional protection.",
        key_statutes=[
            "U.S. Const. Art. VI, Cl. 2 (Supremacy Clause)",
            "21 USC 301 et seq. (FDCA, relevant to Wyeth v. Levine)",
        ],
        elements=[
            "IMPOSSIBILITY: Compliance with both federal and state law is physically impossible",
            "OBSTACLE: State law stands as an obstacle to the full purposes and objectives of federal law",
            "Courts examine the relationship between specific federal and state provisions",
            "The party asserting preemption bears the burden of proof",
            "Presumption against preemption applies in traditional state domains",
        ],
        defenses=[
            "Compliance with both laws is possible (no actual impossibility)",
            "State law complements rather than conflicts with federal objectives",
            "Federal law establishes a floor, not a ceiling, permitting stricter state regulation",
            "Obstacle preemption requires too much judicial speculation about congressional purpose",
        ],
        remedies=[
            "State law that actually conflicts with federal law is preempted",
            "State law that serves as an obstacle to federal purposes is preempted",
            "Complementary state law that does not conflict or obstruct is preserved",
        ],
        leading_cases=[
            "Wyeth v. Levine, 555 U.S. 555 (2009) (FDA approval did not make impossibility of state tort compliance; state failure-to-warn claims not preempted)",
            "Geier v. American Honda Motor Co., 529 U.S. 861 (2000) (state tort law conflicted with federal airbag phase-in standard; obstacle preemption)",
            "PLIVA Inc. v. Mensing, 564 U.S. 604 (2011) (impossibility preemption for generic drug manufacturers)",
            "Mutual Pharmaceutical Co. v. Bartlett, 570 U.S. 472 (2013) (impossibility preemption for generic drug design defect claims)",
        ],
        category="preemption",
        subcategory="conflict",
        authority_score=0.90,
        confidence=0.86,
        related_topics=["preemption_express", "preemption_field", "supremacy_clause"],
        practice_tips=[
            "For impossibility preemption, show that the regulated entity literally cannot comply with both laws",
            "For obstacle preemption, identify the specific federal purpose and show how state law impedes it",
            "Distinguish Wyeth (federal floor) from Geier (federal balance) to determine whether state law adds to or conflicts with federal policy",
        ],
        risk_factors=[
            "Obstacle preemption involves judicial evaluation of congressional purpose, which is inherently uncertain",
            "The impossibility standard is very high: hypothetical impossibility is not enough",
        ],
    ),
    DoctrineCacheBlock(
        topic="delegation_doctrine",
        summary="The nondelegation doctrine holds that Congress cannot delegate its legislative power to executive agencies without providing an 'intelligible principle' to guide the exercise of discretion. The doctrine derives from Article I, Section 1 of the Constitution, which vests 'all legislative Powers' in Congress. The Supreme Court has struck down statutes on nondelegation grounds only twice, both in 1935 (Schechter Poultry and Panama Refining). Since then, the Court has upheld broad delegations under the intelligible principle test. However, there is growing interest in reviving the doctrine, as reflected in Justice Gorsuch's dissent in Gundy v. United States (2019) and the major questions doctrine's role as a functional nondelegation limit. West Virginia v. EPA (2022) effectively applied nondelegation principles through the major questions framework.",
        key_statutes=[
            "U.S. Const. Art. I, Sec. 1 (vesting of legislative power)",
            "U.S. Const. Art. I, Sec. 8 (enumerated powers)",
        ],
        elements=[
            "Congress cannot delegate its legislative power without providing an intelligible principle",
            "The intelligible principle must guide the agency's exercise of delegated authority",
            "The delegation must set boundaries on the agency's discretion",
            "Adequate procedural safeguards (e.g., APA rulemaking) support delegation validity",
            "The degree of delegation must be proportional to the subject matter's complexity",
        ],
        defenses=[
            "The intelligible principle standard is highly permissive in practice",
            "Congress has provided sufficient guidance through statutory standards, definitions, and findings",
            "Procedural safeguards (notice-and-comment, judicial review) constrain agency discretion",
            "Subject matter complexity justifies broad delegation with expert agency administration",
        ],
        remedies=[
            "Strike down the statute as an unconstitutional delegation of legislative power",
            "Construe the statute narrowly to supply an intelligible principle (avoidance canon)",
            "Apply the major questions doctrine to limit the delegation's scope",
        ],
        leading_cases=[
            "A.L.A. Schechter Poultry Corp. v. United States, 295 U.S. 495 (1935) (NIRA 'fair competition' codes struck down as unconstitutional delegation)",
            "Panama Refining Co. v. Ryan, 293 U.S. 388 (1935) (NIRA petroleum provision struck down)",
            "Gundy v. United States, 588 U.S. 128 (2019) (SORNA delegation upheld; Gorsuch dissent called for reinvigorating nondelegation)",
            "West Virginia v. EPA, 597 U.S. 697 (2022) (major questions doctrine as functional nondelegation limit)",
            "Whitman v. American Trucking Assns., 531 U.S. 457 (2001) (Clean Air Act delegation upheld under intelligible principle)",
        ],
        category="delegation",
        subcategory="nondelegation",
        authority_score=0.92,
        confidence=0.82,
        related_topics=["major_questions_doctrine", "separation_of_powers", "apa_rulemaking"],
        practice_tips=[
            "The nondelegation doctrine is rarely applied directly; use the major questions doctrine as a functional substitute",
            "If challenging a broad delegation, pair nondelegation arguments with major questions and avoidance canon arguments",
            "Track Gundy plurality opinions: the doctrine may be revived if the Court takes the right case",
        ],
        risk_factors=[
            "The intelligible principle test is very permissive and rarely results in invalidation",
            "A direct nondelegation holding would have enormous consequences across the federal regulatory state",
            "The current Court may prefer the major questions doctrine over direct nondelegation invalidation",
        ],
    ),
    DoctrineCacheBlock(
        topic="enrolled_bill_doctrine",
        summary="The enrolled bill doctrine provides that a bill authenticated by the signatures of the Speaker of the House and the President of the Senate, and signed by the President, is conclusive evidence that the bill was duly enacted according to constitutional requirements. Courts will not look behind the enrolled bill to examine the journals of Congress or other evidence to determine whether the bill was actually passed by both chambers in the same form. The doctrine was established in Marshall Field & Co. v. Clark (1892) and rests on the separation of powers principle that the judiciary should not second-guess the internal proceedings of the legislature. Some states have adopted an alternative 'journal entry rule' that allows courts to examine legislative journals to determine whether proper procedures were followed.",
        key_statutes=[
            "U.S. Const. Art. I, Sec. 7 (Bicameralism and Presentment)",
            "1 USC 106a (enrolled bill process)",
        ],
        elements=[
            "The bill is enrolled (engrossed on parchment) after passage by both chambers",
            "The Speaker of the House and President of the Senate sign the enrolled bill",
            "The President signs the enrolled bill into law (or it becomes law without signature after 10 days)",
            "The enrolled bill is conclusive evidence of proper enactment",
            "Courts will not examine congressional journals or other extrinsic evidence of the legislative process",
        ],
        defenses=[
            "The enrolled bill was not properly authenticated (missing signatures)",
            "In some state courts, the journal entry rule allows examination of legislative journals",
            "The bill was not presented to the President as required by Article I, Sec. 7",
        ],
        remedies=[
            "Under the enrolled bill doctrine, the authenticated bill is treated as the law",
            "Under the journal entry rule (some states), a discrepancy may invalidate the statute",
        ],
        leading_cases=[
            "Marshall Field & Co. v. Clark, 143 U.S. 649 (1892) (established the enrolled bill doctrine)",
            "Public Citizen v. U.S. District Court, 486 F.3d 1342 (D.C. Cir. 2007) (enrolled bill doctrine applied)",
            "Oneok, Inc. v. Learjet, Inc., 575 U.S. 373 (2015) (related: Congress's word on its own process is final)",
        ],
        category="legislative_process",
        subcategory="enactment",
        authority_score=0.85,
        confidence=0.88,
        related_topics=["bicameralism_presentment", "veto_power", "congressional_procedure_filibuster"],
        practice_tips=[
            "The enrolled bill doctrine effectively forecloses challenges based on legislative procedure defects at the federal level",
            "In state practice, check whether the jurisdiction follows the enrolled bill doctrine or the journal entry rule",
            "Challenges to federal legislation should focus on substantive constitutionality, not procedural irregularities",
        ],
        risk_factors=[
            "The doctrine has been criticized as enabling legislative error without judicial correction",
            "State courts using the journal entry rule may reach different conclusions about the same type of challenge",
        ],
    ),
    DoctrineCacheBlock(
        topic="legislative_privilege_speech_debate",
        summary="The Speech or Debate Clause (Article I, Section 6, Clause 1) provides that 'for any Speech or Debate in either House, [Members of Congress] shall not be questioned in any other Place.' This grants absolute immunity from civil or criminal liability for legislative acts, including votes, speeches on the floor, committee proceedings, and activities integral to the legislative process. The privilege extends to congressional staff acting within the sphere of legitimate legislative activity. However, it does not protect political activities, press releases, newsletters, constituent services, or criminal conduct unrelated to legislation. The clause prevents use of legislative acts as evidence in any legal proceeding, not just as a basis for liability.",
        key_statutes=[
            "U.S. Const. Art. I, Sec. 6, Cl. 1 (Speech or Debate Clause)",
        ],
        elements=[
            "The challenged act must be a 'legislative act' within the sphere of legitimate legislative activity",
            "Legislative acts include voting, debating, reporting, conducting committee hearings, and investigating",
            "The immunity is absolute: no balancing test against countervailing interests",
            "Staff members share derivative immunity for acts within the legislative sphere",
            "The clause prevents compelled testimony about legislative acts and the use of such acts as evidence",
        ],
        defenses=[
            "The act is political (press releases, constituent services, campaign activity) rather than legislative",
            "The act constitutes criminal conduct outside the legislative process (bribery, corruption)",
            "The member is acting in an executive or administrative capacity, not a legislative one",
            "Publication to third parties outside Congress is not protected (Hutchinson v. Proxmire)",
        ],
        remedies=[
            "Dismissal of claims based on legislative acts",
            "Suppression of evidence derived from legislative activities",
            "Quashing of subpoenas seeking testimony about legislative acts",
        ],
        leading_cases=[
            "Gravel v. United States, 408 U.S. 606 (1972) (staff share derivative immunity; subcommittee hearing protected; private publication not protected)",
            "Eastland v. U.S. Servicemen's Fund, 421 U.S. 491 (1975) (subpoena power is legislative and protected)",
            "Kilbourn v. Thompson, 103 U.S. 168 (1881) (early articulation of Speech or Debate protection)",
            "Hutchinson v. Proxmire, 443 U.S. 111 (1979) (press releases and newsletters not protected)",
            "United States v. Brewster, 408 U.S. 501 (1972) (bribery prosecution permitted; the taking of a bribe is not a legislative act)",
        ],
        category="legislative_privilege",
        subcategory="speech_or_debate",
        authority_score=0.90,
        confidence=0.88,
        related_topics=["congressional_oversight", "separation_of_powers", "executive_privilege"],
        practice_tips=[
            "Determine at the outset whether the challenged conduct is legislative or political in character",
            "The clause protects the process (deliberation, investigation) not just the product (votes, laws)",
            "Even in criminal investigations, legislative acts cannot be used as evidence against a Member",
        ],
        risk_factors=[
            "The line between legislative and political activity is sometimes unclear",
            "Members may attempt to invoke the clause to shield non-legislative conduct",
        ],
    ),
    DoctrineCacheBlock(
        topic="texas_legislative_process",
        summary="The Texas Legislature is a bicameral body consisting of a 150-member House of Representatives and a 31-member Senate, meeting in regular biennial sessions limited to 140 calendar days in odd-numbered years. The Governor may call special sessions limited to 30 days, with the agenda set by the Governor. Bills must be introduced, referred to committee, and reported out before floor consideration. The Texas Senate historically operated under a two-thirds rule requiring a supermajority to bring a bill to the floor, but this was modified to a three-fifths rule in 2015 and has been suspended entirely during some sessions. Key procedural tools include tagging (a Senator may delay committee action on a bill for 48 hours), chubbing (extended debate on minor bills to consume the calendar), and the calendars committee system in the House. Texas also has a robust Sunset Review process under the Sunset Advisory Commission (Government Code Chapter 325), which periodically reviews state agencies for continuation or abolition on a 12-year cycle.",
        key_statutes=[
            "Texas Const. Art. III (Legislative Department)",
            "Texas Const. Art. III, Sec. 5 (biennial sessions, 140 days)",
            "Texas Const. Art. III, Sec. 40 (Governor's special session power)",
            "Tex. Gov't Code Ch. 325 (Texas Sunset Act)",
            "Texas House Rules and Senate Rules",
        ],
        elements=[
            "Biennial regular sessions limited to 140 calendar days in odd-numbered years",
            "Special sessions called by Governor, limited to 30 days, Governor sets the agenda",
            "Bills must pass both chambers in identical form",
            "Committee referral is mandatory; committee chairs have significant gatekeeping power",
            "The two-thirds/three-fifths rule in the Senate (when in effect) is a significant procedural hurdle",
            "Sunset Advisory Commission reviews agencies on a 12-year cycle",
            "Governor has line-item veto power for appropriations bills",
        ],
        defenses=[
            "The Governor's special session power is limited to the agenda the Governor sets",
            "Procedural rules can be changed by majority vote of the chamber at the start of each session",
            "Sunset review can result in agency continuation with reforms, not just abolition",
        ],
        remedies=[
            "Bills that fail in regular session may be reconsidered in special session if the Governor adds them to the call",
            "Sunset legislation must pass by end of session or the agency is abolished",
            "Vetoed bills may be reconsidered during the same session with two-thirds vote",
        ],
        leading_cases=[
            "Not primarily judicial; governed by Texas Constitution and chamber rules",
            "Notable Sunset Review: Texas Dept. of Licensing and Regulation (2019)",
            "Notable Sunset Review: Texas Railroad Commission (periodic review)",
        ],
        category="state_legislative_process",
        subcategory="texas",
        jurisdiction="texas",
        authority_score=0.85,
        confidence=0.87,
        related_topics=["congressional_procedure_filibuster", "sunset_review", "governor_veto"],
        practice_tips=[
            "The 140-day session creates intense time pressure; bills not passed by session end die",
            "For Texas advocacy: relationship with committee chairs is critical to bill movement",
            "Track the Sunset Advisory Commission schedule to identify agencies up for review",
        ],
        risk_factors=[
            "Special sessions have a narrow scope limited by the Governor's call",
            "The two-thirds/three-fifths rule (when in effect) can block legislation with majority support",
        ],
        legislative_notes="Texas is one of only four states with biennial legislative sessions. The time constraint fundamentally shapes legislative strategy.",
    ),
    DoctrineCacheBlock(
        topic="lobbying_disclosure_act",
        summary="The Lobbying Disclosure Act of 1995 (LDA), as amended by the Honest Leadership and Open Government Act of 2007 (HLOGA), requires lobbyists and lobbying firms to register with the Secretary of the Senate and the Clerk of the House and to file quarterly disclosure reports. Registration is required for any individual who makes more than one lobbying contact and spends 20% or more of their time on lobbying activities for a particular client during a quarterly period. Lobbyists must disclose the client, issues lobbied, chambers and agencies contacted, and estimated income or expenses. The LDA also imposes a ban on gifts to Members and staff (with exceptions), restrictions on former Members and senior staff revolving door activity, and requirements to disclose bundled campaign contributions. FARA (Foreign Agents Registration Act) separately requires registration for agents acting on behalf of foreign governments or political parties.",
        key_statutes=[
            "Lobbying Disclosure Act, 2 USC 1601-1614",
            "Honest Leadership and Open Government Act of 2007 (HLOGA)",
            "Foreign Agents Registration Act (FARA), 22 USC 611-621",
            "House and Senate Ethics Rules on gifts and revolving door",
        ],
        elements=[
            "Registration required for lobbyists making more than one lobbying contact per quarter",
            "20% time threshold for lobbying activities during a quarterly period",
            "Quarterly disclosure reports (LD-2) listing clients, issues, contacts, and income/expenses",
            "Semiannual political contribution reports (LD-203)",
            "Gift ban with limited exceptions (meals under $50, widely attended events, etc.)",
            "Revolving door restrictions: 1 year for House members and senior staff, 2 years for Senators",
            "FARA registration for agents of foreign principals (broader scope than LDA)",
        ],
        defenses=[
            "Activity does not constitute 'lobbying contact' under the LDA definition",
            "Lobbyist spends less than 20% of time on lobbying for the client",
            "Client is exempt (e.g., certain tax-exempt organizations for self-lobbying)",
            "Activity is grassroots lobbying (not covered by LDA, which targets direct lobbying)",
        ],
        remedies=[
            "Civil penalties for failure to register or file reports (up to $200,000)",
            "Criminal penalties for knowing and corrupt failure to comply (up to 5 years)",
            "FARA violations can result in criminal prosecution (up to 5 years and $250,000)",
            "Congressional ethics investigations for revolving door and gift violations",
        ],
        leading_cases=[
            "United States v. Harriss, 347 U.S. 612 (1954) (upheld predecessor Federal Regulation of Lobbying Act)",
            "FARA enforcement: United States v. Barrack (2022) (FARA prosecution for undisclosed foreign lobbying)",
            "United States v. Rafiekian, 991 F.3d 529 (4th Cir. 2021) (FARA prosecution standards)",
        ],
        category="lobbying_regulation",
        subcategory="disclosure",
        authority_score=0.85,
        confidence=0.85,
        related_topics=["congressional_oversight", "campaign_finance", "ethics_rules"],
        practice_tips=[
            "Track the 20% time threshold carefully: it is measured per client per quarter",
            "Maintain contemporaneous time records to demonstrate compliance",
            "FARA obligations may apply to government affairs work for foreign-owned companies",
        ],
        risk_factors=[
            "DOJ has increased FARA enforcement significantly in recent years",
            "The line between lobbying and strategic consulting can be blurry",
            "Failure to register carries both civil and criminal penalties",
        ],
    ),
    DoctrineCacheBlock(
        topic="redistricting_legal_framework",
        summary="Legislative redistricting is the process of redrawing legislative district boundaries following each decennial census to comply with the constitutional requirement of equal representation. Under the Equal Protection Clause, congressional districts must be as equal in population as practicable (Wesberry v. Sanders, Karcher v. Daggett), while state legislative districts permit slightly more deviation (Reynolds v. Sims, generally up to 10% total deviation). The Voting Rights Act Section 2 prohibits redistricting plans that dilute the voting strength of racial minorities (Allen v. Milligan, 2023). Racial gerrymandering is subject to strict scrutiny (Shaw v. Reno, Miller v. Johnson). Partisan gerrymandering claims are nonjusticiable political questions that federal courts cannot adjudicate (Rucho v. Common Cause, 2019), but some state courts have found partisan gerrymandering claims justiciable under state constitutions.",
        key_statutes=[
            "U.S. Const. Amend. XIV (Equal Protection Clause)",
            "U.S. Const. Amend. XV (right to vote not denied on account of race)",
            "Voting Rights Act Section 2, 52 USC 10301",
            "2 USC 2a(c) (apportionment of House seats)",
        ],
        elements=[
            "One person, one vote: districts must be substantially equal in population",
            "Congressional districts require near-exact mathematical equality (Karcher v. Daggett)",
            "State legislative districts permit up to approximately 10% total deviation",
            "VRA Section 2 prohibits dilution of minority voting strength",
            "Racial gerrymandering is subject to strict scrutiny and must be narrowly tailored",
            "Race cannot be the predominant factor in drawing district lines without compelling justification",
            "Traditional redistricting criteria include compactness, contiguity, and respect for political subdivisions and communities of interest",
        ],
        defenses=[
            "Partisan considerations, not race, were the predominant factor (partisan gerrymandering is nonjusticiable in federal court)",
            "VRA compliance required the use of race in drawing the district",
            "Population deviations are within the permissible range and justified by legitimate state interests",
            "The plan reflects traditional redistricting criteria, not racial or partisan manipulation",
        ],
        remedies=[
            "Court-ordered redistricting if the plan violates the Constitution or VRA",
            "Injunction against use of an unconstitutional plan",
            "State court remedies for partisan gerrymandering under state constitutions",
            "Special master-drawn plan if the legislature fails to adopt a lawful plan",
        ],
        leading_cases=[
            "Baker v. Carr, 369 U.S. 186 (1962) (redistricting is a justiciable issue under Equal Protection)",
            "Reynolds v. Sims, 377 U.S. 533 (1964) (one person, one vote for state legislatures)",
            "Wesberry v. Sanders, 376 U.S. 1 (1964) (one person, one vote for congressional districts under Art. I Sec. 2)",
            "Shaw v. Reno, 509 U.S. 630 (1993) (racial gerrymandering subject to strict scrutiny)",
            "Rucho v. Common Cause, 588 U.S. 684 (2019) (partisan gerrymandering nonjusticiable in federal court)",
            "Allen v. Milligan, 599 U.S. 1 (2023) (VRA Section 2 requires additional majority-minority districts in Alabama)",
        ],
        category="redistricting",
        subcategory="legal_framework",
        authority_score=0.93,
        confidence=0.88,
        related_topics=["voting_rights", "equal_protection", "one_person_one_vote"],
        practice_tips=[
            "After Rucho, partisan gerrymandering claims must be brought under state constitutions, not federal law",
            "Allen v. Milligan reaffirmed that VRA Section 2 requires proportional minority representation opportunity",
            "In racial gerrymandering challenges, the plaintiff must show race was the predominant factor in drawing the district",
        ],
        risk_factors=[
            "Redistricting litigation is highly political and outcomes may depend on the composition of the reviewing court",
            "The interaction between VRA compliance and racial gerrymandering doctrine creates tension",
        ],
    ),
    DoctrineCacheBlock(
        topic="constitutional_amendment_process",
        summary="Article V of the U.S. Constitution establishes two methods for proposing amendments and two methods for ratifying them. Proposal can be made by (1) two-thirds vote of both chambers of Congress, or (2) a convention called by Congress upon application of two-thirds (34) of state legislatures. Ratification requires approval by three-fourths (38) of the state legislatures or three-fourths of state conventions. All 27 amendments have been proposed by Congress; no convention has been called under Article V. Congress may set a time limit for ratification (typically 7 years). Whether a state may rescind its ratification and whether Congress can extend the ratification deadline are open constitutional questions. The political question doctrine has historically limited judicial review of the amendment process (Coleman v. Miller).",
        key_statutes=[
            "U.S. Const. Art. V (Amendment Process)",
            "1 USC 106b (amendment ratification procedures)",
        ],
        elements=[
            "Proposal by two-thirds of both chambers of Congress (most common method)",
            "OR proposal by constitutional convention called on application of 34 state legislatures (never used)",
            "Ratification by three-fourths (38) of state legislatures (most common method)",
            "OR ratification by three-fourths of state conventions (used once: 21st Amendment)",
            "Congress may specify the method of ratification and set a time limit",
            "The President has no formal role in the amendment process (Hollingsworth v. Virginia)",
        ],
        defenses=[
            "The time limit for ratification has expired",
            "The proposed amendment is not within the scope of the convention call (if convention method used)",
            "The ratification process did not comply with Article V requirements",
            "The issue is a nonjusticiable political question (Coleman v. Miller)",
        ],
        remedies=[
            "Successful ratification results in a constitutional amendment binding on all branches and states",
            "Failed ratification leaves the proposed amendment unratified and without legal effect",
            "Judicial review of the amendment process is limited by the political question doctrine",
        ],
        leading_cases=[
            "Coleman v. Miller, 307 U.S. 433 (1939) (political question doctrine limits judicial review of amendment process)",
            "National Prohibition Cases, 253 U.S. 350 (1920) (18th Amendment validly ratified; two-thirds means of members present assuming quorum)",
            "Hollingsworth v. Virginia, 3 U.S. (3 Dall.) 378 (1798) (President has no role in amendment process)",
            "Dillon v. Gloss, 256 U.S. 368 (1921) (Congress may set ratification time limit; contemporaneity required)",
        ],
        category="constitutional_process",
        subcategory="amendment",
        authority_score=0.92,
        confidence=0.88,
        related_topics=["separation_of_powers", "political_question_doctrine", "article_v_convention"],
        practice_tips=[
            "The Article V convention method has never been used; its procedures are largely unresolved",
            "Whether states can rescind ratification votes is an open question (ERA controversy)",
            "Congress's power to set ratification deadlines is established but the ability to extend them is contested",
        ],
        risk_factors=[
            "An Article V convention could potentially exceed its call and propose broader amendments",
            "Ratification deadline extensions may face constitutional challenges",
        ],
    ),
    DoctrineCacheBlock(
        topic="pocket_veto_signing_statements",
        summary="The President's veto power under Article I, Section 7 includes the regular veto (returning a bill unsigned with objections) and the pocket veto (the bill does not become law if the President fails to sign it within 10 days and Congress has adjourned, preventing return of the bill). A regular veto can be overridden by a two-thirds vote of each chamber. A pocket veto is absolute and cannot be overridden. The line-item veto was struck down as unconstitutional in Clinton v. City of New York (1998). Presidential signing statements express the President's interpretation of a law at the time of signing. They have no binding legal effect on courts but may indicate how the executive branch intends to implement the law. Signing statements have been used to raise constitutional objections to specific provisions while signing the overall bill.",
        key_statutes=[
            "U.S. Const. Art. I, Sec. 7, Cl. 2 (Presentment Clause, veto power)",
            "U.S. Const. Art. I, Sec. 7, Cl. 3 (applies presentment to all orders, resolutions, and votes)",
        ],
        elements=[
            "REGULAR VETO: President returns bill unsigned with written objections within 10 days (Sundays excepted)",
            "OVERRIDE: Each chamber may override with two-thirds vote after reconsidering the bill",
            "POCKET VETO: Bill does not become law if President does not sign within 10 days and Congress adjourns",
            "DEFAULT ENACTMENT: If President does not sign within 10 days and Congress is in session, the bill becomes law without signature",
            "SIGNING STATEMENTS: Presidential statements issued at signing have no binding legal effect",
            "LINE-ITEM VETO: Struck down as unconstitutional (Clinton v. City of New York)",
        ],
        defenses=[
            "The pocket veto is available only if Congress has adjourned, preventing return of the bill",
            "Intersession adjournments may not qualify as adjournments preventing return (Pocket Veto Case refinements)",
            "Signing statements do not alter the legal effect of the enacted statute",
        ],
        remedies=[
            "Regular vetoes can be overridden by two-thirds of each chamber",
            "Pocket vetoes cannot be overridden; Congress must pass the bill again in a new session",
            "Courts interpret statutes independently of signing statements",
        ],
        leading_cases=[
            "The Pocket Veto Case, 279 U.S. 655 (1929) (pocket veto during intersession adjournment valid)",
            "Wright v. United States, 302 U.S. 583 (1938) (bill may be returned to an agent of Congress during intrasession adjournment)",
            "Clinton v. City of New York, 524 U.S. 417 (1998) (Line Item Veto Act unconstitutional; violates Presentment Clause)",
            "INS v. Chadha, 462 U.S. 919 (1983) (legislative vetoes unconstitutional; related to separation of powers in legislative process)",
        ],
        category="legislative_process",
        subcategory="executive_action",
        authority_score=0.90,
        confidence=0.88,
        related_topics=["enrolled_bill_doctrine", "bicameralism_presentment", "separation_of_powers"],
        practice_tips=[
            "Signing statements can provide insight into executive enforcement priorities but do not change the law",
            "Track pocket veto risks when Congress plans adjournment during the 10-day presentment period",
            "After Clinton v. City of New York, any form of line-item veto requires a constitutional amendment",
        ],
        risk_factors=[
            "The scope of 'adjournment' sufficient for a pocket veto remains somewhat unsettled",
            "Presidents may use signing statements to signal nonenforcement of provisions they consider unconstitutional",
        ],
    ),
    DoctrineCacheBlock(
        topic="congressional_review_act",
        summary="The Congressional Review Act (CRA), 5 USC 801-808, provides an expedited procedure for Congress to disapprove major rules issued by federal agencies. Under the CRA, agencies must submit all final rules to both chambers of Congress and the Comptroller General before they can take effect. For major rules, there is a 60-legislative-day review period during which Congress can introduce and pass a joint resolution of disapproval. The resolution is subject to special fast-track procedures in the Senate: limited debate, no filibuster, and simple majority passage. If signed by the President (or if a veto is overridden), the rule is nullified, and the agency is prohibited from reissuing the rule in 'substantially the same form' without subsequent congressional authorization. The CRA was used extensively in early 2017 to overturn late-Obama administration rules.",
        key_statutes=[
            "Congressional Review Act, 5 USC 801-808",
            "5 USC 801(a)(1) (agency submission requirement)",
            "5 USC 802 (joint resolution of disapproval procedures)",
        ],
        elements=[
            "Agency submits final rule to both chambers and GAO before effective date",
            "Major rules have a 60-legislative-day review period before taking effect",
            "Any Member can introduce a joint resolution of disapproval within the review period",
            "Senate fast-track: 10 hours of debate, no filibuster, simple majority passage",
            "Joint resolution must pass both chambers and be signed by the President (or veto overridden)",
            "Disapproved rule is treated as though it had never taken effect",
            "Agency cannot reissue rule in substantially the same form without new statutory authority",
        ],
        defenses=[
            "The 60-legislative-day window has expired",
            "The rule is not a 'major rule' under the CRA definition (but non-major rules are also reviewable)",
            "The disapproval resolution failed to pass or was vetoed",
            "New statutory authority has been enacted authorizing the substance of the disapproved rule",
        ],
        remedies=[
            "Rule is nullified as if it never took effect",
            "Agency barred from reissuing substantially the same rule",
            "Agency must obtain new statutory authority to reimpose similar regulation",
        ],
        leading_cases=[
            "Not extensively litigated; CRA resolutions are legislative acts subject to limited judicial review",
            "Notable CRA disapprovals: 16 rules disapproved in 2017, 3 in 2021, several in 2023-2024",
        ],
        category="regulatory_rulemaking",
        subcategory="congressional_oversight",
        authority_score=0.85,
        confidence=0.85,
        related_topics=["apa_notice_and_comment", "congressional_oversight", "major_questions_doctrine"],
        practice_tips=[
            "Monitor the CRA lookback window during presidential transitions: new administrations can disapprove rules finalized in the last months of the prior administration",
            "The 'substantially the same form' prohibition is poorly defined and creates regulatory uncertainty",
            "CRA disapproval is most effective when the President and congressional majority are aligned against the agency action",
        ],
        risk_factors=[
            "The 'substantially the same form' bar may prevent future administrations from re-regulating",
            "The CRA lookback window calculation is complex and has been disputed",
        ],
    ),
    DoctrineCacheBlock(
        topic="king_v_burwell_statutory_context",
        summary="King v. Burwell (2015) addressed whether the Affordable Care Act's tax credits were available on federal exchanges ('established by the State' language in Section 36B). Chief Justice Roberts, writing for the 6-3 majority, declined to apply Chevron deference and instead interpreted the statute using the whole-act rule and purposivism. The Court held that the phrase 'established by the State' was ambiguous in context and that reading it literally would destabilize insurance markets, contradicting the ACA's structure and purpose. The decision is a key example of structural and purposive statutory interpretation, reading an unclear phrase against the backdrop of the entire statutory scheme. It also established that 'questions of deep economic and political significance' should be resolved by courts, not agencies (a precursor to the major questions doctrine).",
        key_statutes=[
            "26 USC 36B (ACA premium tax credits)",
            "42 USC 18031 (state exchange establishment)",
            "42 USC 18041 (federal fallback exchange)",
        ],
        elements=[
            "Statutory text read in context of the entire ACA, not in isolation",
            "Phrase 'established by the State' interpreted to include federal fallback exchanges",
            "Structural reading: denying credits on federal exchanges would cause a death spiral contradicting the Act's design",
            "Major question: the Court resolved the question itself rather than deferring to the IRS",
            "Purposive reasoning: the ACA's purpose was to expand coverage, not undermine it through a drafting quirk",
        ],
        defenses=[
            "The plain text says 'established by the State,' which literally excludes federal exchanges",
            "Textualist reading should control where the text is clear (Scalia dissent)",
            "Congress could fix the problem legislatively if the text produces bad results",
        ],
        remedies=[
            "Tax credits available on both state and federal exchanges",
            "The ACA's insurance market reforms function as designed",
        ],
        leading_cases=[
            "King v. Burwell, 576 U.S. 473 (2015)",
            "NFIB v. Sebelius, 567 U.S. 519 (2012) (related ACA decision)",
            "California v. Texas, 593 U.S. 659 (2021) (ACA standing; related)",
        ],
        category="statutory_construction",
        subcategory="contextual_interpretation",
        authority_score=0.93,
        confidence=0.90,
        related_topics=["whole_act_rule", "purposivism", "major_questions_doctrine", "chevron_deference"],
        practice_tips=[
            "King v. Burwell is the leading example of structural/contextual interpretation overriding a literal textual reading",
            "Use King to argue that isolated phrases must be read in the context of the statute's overall design",
            "The decision's rejection of Chevron deference for major questions foreshadowed the major questions doctrine",
        ],
        risk_factors=[
            "Textualists cite King as an example of purposivism overriding clear text",
            "The decision's approach may be limited to its unique statutory context",
        ],
    ),
    DoctrineCacheBlock(
        topic="bostock_textualism",
        summary="Bostock v. Clayton County (2020) is the landmark modern application of textualism, holding that Title VII's prohibition on discrimination 'because of sex' encompasses discrimination based on sexual orientation and gender identity. Justice Gorsuch, writing for the 6-3 majority, applied a rigorous textualist methodology: because firing someone for being homosexual or transgender necessarily involves treating them differently because of their sex (since the outcome would change if the individual's sex were different), such discrimination is discrimination 'because of sex' under the plain meaning of the statute. The decision rejected arguments based on the original expected application of Title VII in 1964, holding that the text's meaning controls regardless of whether Congress foresaw or intended the specific application. Bostock is a foundational textualist opinion demonstrating the methodology's power to produce unexpected results.",
        key_statutes=[
            "Title VII of the Civil Rights Act of 1964, 42 USC 2000e-2(a)(1)",
        ],
        elements=[
            "The statutory text prohibits discrimination 'because of sex'",
            "But-for causation: would the employer have treated the employee differently but for their sex?",
            "Discrimination based on sexual orientation or gender identity necessarily involves sex as a but-for cause",
            "The text's ordinary meaning at the time of enactment controls, not the expected application",
            "Textualism does not permit courts to narrow a statute's reach based on what Congress intended to accomplish",
        ],
        defenses=[
            "Original expected application: Congress in 1964 did not intend to cover sexual orientation or gender identity (rejected by majority)",
            "Severability of concepts: 'sex' refers to biological sex, not sexual orientation (rejected by majority)",
            "Legislative history and subsequent failed amendments show Congress did not intend this scope (rejected by majority)",
        ],
        remedies=[
            "Title VII's protections extend to sexual orientation and gender identity in employment",
            "Employers cannot discriminate in hiring, firing, compensation, or terms of employment based on these characteristics",
        ],
        leading_cases=[
            "Bostock v. Clayton County, 590 U.S. 644 (2020)",
            "Price Waterhouse v. Hopkins, 490 U.S. 228 (1989) (sex stereotyping is sex discrimination)",
            "Oncale v. Sundowner Offshore Services, 523 U.S. 75 (1998) (same-sex harassment actionable under Title VII)",
        ],
        category="statutory_construction",
        subcategory="textualism",
        authority_score=0.95,
        confidence=0.92,
        related_topics=["textualism", "plain_meaning_rule", "title_vii"],
        practice_tips=[
            "Bostock's but-for causation framework is applicable to other statutes prohibiting discrimination 'because of' a protected characteristic",
            "Use Bostock to demonstrate that textualism follows the text even to results Congress may not have foreseen",
            "The decision's reasoning has been extended to other civil rights statutes by lower courts",
        ],
        risk_factors=[
            "The scope of Bostock beyond employment (education, housing, public accommodations) is still being litigated",
            "Religious exemption defenses to Bostock-based claims are an active area of litigation",
        ],
    ),
]


# ============================================================================
# DOCTRINE CACHE INDEX - O(1) LOOKUP
# ============================================================================

class DoctrineCacheIndex:
    """Fast O(1) lookup index over doctrine blocks by topic and category."""

    def __init__(self, blocks: List[DoctrineCacheBlock]) -> None:
        self._by_topic: Dict[str, DoctrineCacheBlock] = {}
        self._by_category: Dict[str, List[DoctrineCacheBlock]] = {}
        self._by_subcategory: Dict[str, List[DoctrineCacheBlock]] = {}
        self._all_topics: Set[str] = set()
        self._all_categories: Set[str] = set()
        self._build_index(blocks)
        logger.info(
            "DoctrineCacheIndex built: {} topics, {} categories",
            len(self._by_topic),
            len(self._by_category),
        )

    def _build_index(self, blocks: List[DoctrineCacheBlock]) -> None:
        """Build the lookup indices from the raw blocks."""
        for block in blocks:
            topic_key = block.topic.lower().strip()
            self._by_topic[topic_key] = block
            self._all_topics.add(topic_key)
            cat_key = block.category.lower().strip()
            self._all_categories.add(cat_key)
            if cat_key not in self._by_category:
                self._by_category[cat_key] = []
            self._by_category[cat_key].append(block)
            if block.subcategory:
                sub_key = block.subcategory.lower().strip()
                if sub_key not in self._by_subcategory:
                    self._by_subcategory[sub_key] = []
                self._by_subcategory[sub_key].append(block)

    def get_by_topic(self, topic: str) -> Optional[DoctrineCacheBlock]:
        """Retrieve a block by exact topic match."""
        return self._by_topic.get(topic.lower().strip())

    def get_by_category(self, category: str) -> List[DoctrineCacheBlock]:
        """Retrieve all blocks in a category."""
        return self._by_category.get(category.lower().strip(), [])

    def get_by_subcategory(self, subcategory: str) -> List[DoctrineCacheBlock]:
        """Retrieve all blocks in a subcategory."""
        return self._by_subcategory.get(subcategory.lower().strip(), [])

    def all_topics(self) -> Set[str]:
        """Return all indexed topics."""
        return set(self._all_topics)

    def all_categories(self) -> Set[str]:
        """Return all indexed categories."""
        return set(self._all_categories)

    def topic_count(self) -> int:
        """Return the number of indexed topics."""
        return len(self._by_topic)

    def category_count(self) -> int:
        """Return the number of indexed categories."""
        return len(self._by_category)


# ============================================================================
# MODULE-LEVEL CACHE INSTANCES
# ============================================================================

_CACHE_INDEX: Optional[DoctrineCacheIndex] = None
_CACHE_HASH: Optional[str] = None
_CACHE_BUILT_AT: Optional[str] = None


def build_doctrine_cache() -> DoctrineCacheIndex:
    """Build or return the singleton doctrine cache index."""
    global _CACHE_INDEX, _CACHE_HASH, _CACHE_BUILT_AT
    if _CACHE_INDEX is not None:
        return _CACHE_INDEX
    start = time.perf_counter()
    _CACHE_INDEX = DoctrineCacheIndex(DOCTRINE_BLOCKS)
    content_for_hash = json.dumps(
        [b.to_dict() for b in DOCTRINE_BLOCKS], sort_keys=True
    )
    _CACHE_HASH = hashlib.sha256(content_for_hash.encode("utf-8")).hexdigest()
    _CACHE_BUILT_AT = datetime.now(timezone.utc).isoformat()
    elapsed = (time.perf_counter() - start) * 1000
    logger.info(
        "Doctrine cache built in {:.1f}ms: {} blocks, hash={}",
        elapsed,
        len(DOCTRINE_BLOCKS),
        _CACHE_HASH[:16],
    )
    return _CACHE_INDEX


def get_doctrine_cache() -> DoctrineCacheIndex:
    """Get the singleton cache index, building if necessary."""
    if _CACHE_INDEX is None:
        return build_doctrine_cache()
    return _CACHE_INDEX


def get_doctrine_block(topic: str) -> Optional[DoctrineCacheBlock]:
    """Retrieve a single doctrine block by topic."""
    cache = get_doctrine_cache()
    return cache.get_by_topic(topic)


def get_doctrine_cache_hash() -> str:
    """Return the SHA-256 hash of the entire doctrine cache."""
    if _CACHE_HASH is None:
        build_doctrine_cache()
    return _CACHE_HASH or ""


def get_doctrine_cache_stats() -> Dict[str, Any]:
    """Return statistics about the doctrine cache."""
    cache = get_doctrine_cache()
    return {
        "total_blocks": len(DOCTRINE_BLOCKS),
        "total_topics": cache.topic_count(),
        "total_categories": cache.category_count(),
        "categories": sorted(cache.all_categories()),
        "cache_hash": get_doctrine_cache_hash()[:16],
        "built_at": _CACHE_BUILT_AT,
    }


def search_doctrines(
    query: str,
    category: Optional[str] = None,
    top_k: int = 5,
) -> List[DoctrineCacheBlock]:
    """Free-text search over doctrine blocks.

    Performs keyword matching against the searchable content of each block.
    Optionally filters by category. Returns top_k results sorted by relevance score.
    """
    cache = get_doctrine_cache()
    query_lower = query.lower().strip()
    query_tokens = set(query_lower.split())
    candidates: List[DoctrineCacheBlock]
    if category:
        candidates = cache.get_by_category(category)
    else:
        candidates = list(DOCTRINE_BLOCKS)
    scored: List[tuple[float, DoctrineCacheBlock]] = []
    for block in candidates:
        content = block.content_for_search().lower()
        content_tokens = set(content.split())
        overlap = query_tokens & content_tokens
        if not overlap:
            continue
        score = len(overlap) / max(len(query_tokens), 1)
        if block.topic.lower() in query_lower or query_lower in block.topic.lower():
            score += 0.5
        for token in query_tokens:
            if token in block.summary.lower():
                score += 0.1
        score *= block.authority_score
        score *= block.confidence
        scored.append((score, block))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [block for _, block in scored[:top_k]]


def get_coverage_map() -> Dict[str, Dict[str, Any]]:
    """Return a map of all topics with metadata for coverage analysis."""
    result: Dict[str, Dict[str, Any]] = {}
    for block in DOCTRINE_BLOCKS:
        result[block.topic] = {
            "category": block.category,
            "subcategory": block.subcategory,
            "jurisdiction": block.jurisdiction,
            "authority_score": block.authority_score,
            "confidence": block.confidence,
            "last_updated": block.last_updated,
            "staleness_days": block.staleness_days,
            "num_statutes": len(block.key_statutes),
            "num_cases": len(block.leading_cases),
            "num_elements": len(block.elements),
            "related_topics": block.related_topics,
        }
    return result


def get_all_doctrine_topics() -> List[str]:
    """Return sorted list of all doctrine topics."""
    return sorted(b.topic for b in DOCTRINE_BLOCKS)


def get_all_doctrine_categories() -> List[str]:
    """Return sorted list of all doctrine categories."""
    return sorted(set(b.category for b in DOCTRINE_BLOCKS))


def get_stale_doctrines(threshold_days: int = 90) -> List[DoctrineCacheBlock]:
    """Return all doctrine blocks that exceed the staleness threshold."""
    return [b for b in DOCTRINE_BLOCKS if b.staleness_days > threshold_days]


def verify_doctrine_integrity() -> Dict[str, Any]:
    """Verify the integrity of the doctrine cache.

    Checks for duplicate topics, missing required fields, and hash consistency.
    """
    issues: List[str] = []
    seen_topics: Set[str] = set()
    for block in DOCTRINE_BLOCKS:
        if block.topic in seen_topics:
            issues.append(f"Duplicate topic: {block.topic}")
        seen_topics.add(block.topic)
        if not block.summary:
            issues.append(f"Missing summary for topic: {block.topic}")
        if not block.key_statutes:
            issues.append(f"Missing key_statutes for topic: {block.topic}")
        if not block.leading_cases:
            issues.append(f"Missing leading_cases for topic: {block.topic}")
        if not block.elements:
            issues.append(f"Missing elements for topic: {block.topic}")
        if not block.category:
            issues.append(f"Missing category for topic: {block.topic}")
        if block.authority_score < 0.0 or block.authority_score > 1.0:
            issues.append(f"Invalid authority_score for topic: {block.topic}")
        if block.confidence < 0.0 or block.confidence > 1.0:
            issues.append(f"Invalid confidence for topic: {block.topic}")
    cache_hash = get_doctrine_cache_hash()
    return {
        "valid": len(issues) == 0,
        "total_blocks": len(DOCTRINE_BLOCKS),
        "unique_topics": len(seen_topics),
        "issues": issues,
        "cache_hash": cache_hash,
        "verified_at": datetime.now(timezone.utc).isoformat(),
    }
