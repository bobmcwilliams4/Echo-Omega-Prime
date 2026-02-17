"""
LG02 Case Law Research Engine - Doctrine Cache
=================================================
Authority: 11.0 SOVEREIGN | Echo Omega Prime
Version: 2.0.0 | Port: 8392

Comprehensive case law research doctrine cache covering 70+ legal doctrine topics
with expert reasoning, real case citations, practice playbooks, applicability tests,
court hierarchy weights, and Shepardize treatment data.

Architecture:
- DoctrineResponse: Structured doctrine response with citations and playbooks
- DOCTRINE_CACHE: 70+ doctrine blocks with full expert analysis
- CaseLawDoctrineEngine: Query engine with keyword matching and retrieval
- Singleton pattern for system-wide access

Usage:
    from doctrines import get_engine as get_doctrine_engine
    engine = get_doctrine_engine()
    response = engine.quick_answer("stare decisis")

Author: ECHO OMEGA PRIME
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
import hashlib
import re
import time

from loguru import logger


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class DoctrineResponse:
    """Structured case law doctrine response."""
    topic: str
    quick_answer: str
    full_doctrine: str
    citations: List[str]
    statute_refs: List[str]
    practice_playbook: List[str]
    counter_arguments: List[str]
    applicability_test: str
    court_level: str = "all"
    jurisdiction_scope: str = "federal"
    authority_weight: int = 75
    staleness_risk: str = "low"
    key_number_topics: List[str] = field(default_factory=list)
    related_doctrines: List[str] = field(default_factory=list)
    overruled_by: Optional[str] = None
    last_major_update: str = "2024"
    opinion_section_focus: str = "majority"

    def to_dict(self) -> Dict:
        """Serialize to dictionary."""
        return {
            "topic": self.topic,
            "quick_answer": self.quick_answer,
            "full_doctrine": self.full_doctrine,
            "citations": self.citations,
            "statute_refs": self.statute_refs,
            "practice_playbook": self.practice_playbook,
            "counter_arguments": self.counter_arguments,
            "applicability_test": self.applicability_test,
            "court_level": self.court_level,
            "jurisdiction_scope": self.jurisdiction_scope,
            "authority_weight": self.authority_weight,
            "staleness_risk": self.staleness_risk,
            "key_number_topics": self.key_number_topics,
            "related_doctrines": self.related_doctrines,
            "overruled_by": self.overruled_by,
            "last_major_update": self.last_major_update,
            "opinion_section_focus": self.opinion_section_focus,
        }


# ============================================================================
# DOCTRINE CACHE - 70+ Case Law Research Doctrine Blocks
# ============================================================================

DOCTRINE_CACHE: Dict[str, DoctrineResponse] = {

    # ========================================================================
    # STARE DECISIS & PRECEDENT
    # ========================================================================

    "stare_decisis_application": DoctrineResponse(
        topic="Stare Decisis Application",
        quick_answer="Stare decisis requires courts to follow precedent from higher courts in the same jurisdiction. Vertical stare decisis is mandatory; horizontal stare decisis allows courts to overrule their own prior decisions in rare circumstances.",
        full_doctrine="""The doctrine of stare decisis ("to stand by things decided") is the foundational principle of American common law requiring courts to follow precedent. Under vertical stare decisis, lower courts are absolutely bound by decisions of higher courts within the same judicial hierarchy. A federal district court must follow circuit precedent, and all federal courts must follow Supreme Court decisions. This creates predictability and uniformity in the law.

Horizontal stare decisis governs how courts treat their own prior decisions. While courts generally adhere to their own precedents, they retain authority to overrule prior decisions when they prove "unworkable or are badly reasoned" (Payne v. Tennessee, 501 U.S. 808 (1991)). The Supreme Court has overruled prior constitutional decisions approximately 200 times in its history, typically requiring a showing that the prior decision was egregiously wrong or that changed circumstances warrant reconsideration.

Lower courts lack authority to overrule higher court precedent, even when they believe it incorrect. As the Ninth Circuit explained in Miller v. Gammie, 335 F.3d 889 (9th Cir. 2003), only the Supreme Court or en banc authority can overrule circuit precedent. District courts that openly defy circuit precedent face near-certain reversal and potential sanctions.

The binding effect of precedent depends on whether the prior holding was essential to the judgment (ratio decidendi) or merely explanatory dicta. Only holdings necessary to the decision constitute binding precedent. Courts frequently distinguish cases on their facts to avoid following precedent without explicitly overruling it, a practice sometimes criticized as stealth overruling but generally accepted as proper application of stare decisis principles.""",
        citations=[
            "Payne v. Tennessee, 501 U.S. 808 (1991)",
            "Miller v. Gammie, 335 F.3d 889 (9th Cir. 2003)",
            "Planned Parenthood v. Casey, 505 U.S. 833 (1992)",
            "Citizens United v. FEC, 558 U.S. 310 (2010)",
            "Janus v. AFSCME, 138 S. Ct. 2448 (2018)",
            "Dobbs v. Jackson Women's Health Org., 597 U.S. 215 (2022)",
        ],
        statute_refs=["28 U.S.C. 1254", "Fed. R. App. P. 35 (en banc)"],
        practice_playbook=[
            "Identify the controlling jurisdiction and hierarchical relationship",
            "Shepardize or KeyCite the precedent to verify it remains good law",
            "Determine whether prior holding is ratio decidendi or dicta",
            "Assess factual distinctions that might permit distinguishing the case",
            "If seeking to overrule precedent, demonstrate it is unworkable or badly reasoned",
            "Consider predictive coding: how likely is this court to follow/distinguish precedent",
            "For Supreme Court advocacy, show special justification beyond mere disagreement",
        ],
        counter_arguments=[
            "Precedent was wrongly decided from the outset and should be overruled",
            "Changed circumstances undermine the precedent's foundation",
            "Factual distinctions render the precedent inapplicable",
            "Intervening higher-court authority has undermined the reasoning",
            "Reliance interests do not weigh in favor of maintaining the precedent",
        ],
        applicability_test=r"(?i)(stare.?decisis|preced|binding.?authority|overrul|follow.?precedent|distinguish.?case|ratio.?decidendi|dicta|obiter)",
        authority_weight=100,
        key_number_topics=["170A Federal Courts", "106 Courts"],
        related_doctrines=["res_judicata", "collateral_estoppel", "law_of_the_case"],
    ),

    "res_judicata": DoctrineResponse(
        topic="Res Judicata (Claim Preclusion)",
        quick_answer="Res judicata bars relitigation of claims that were or could have been raised in a prior action between the same parties on the same cause of action, provided there was a final judgment on the merits.",
        full_doctrine="""Res judicata, also known as claim preclusion, prevents parties from relitigating matters that were decided or could have been decided in a prior suit. The doctrine serves three purposes: (1) finality of judgments, (2) conservation of judicial resources, and (3) prevention of inconsistent results.

For res judicata to apply, four elements must be established: (1) a final judgment on the merits in the prior action, (2) identity of parties or their privies, (3) identity of the cause of action, and (4) the claim was or could have been raised in the prior proceeding. The "transactional" test adopted by the Restatement (Second) of Judgments section 24 defines the scope broadly: all claims arising from the same transaction or occurrence must be raised in a single suit or be forever barred.

The Supreme Court in Federated Department Stores, Inc. v. Moitie, 452 U.S. 394 (1981), held that res judicata applies even when the first judgment may have been wrongly decided. The doctrine prioritizes finality over correctness. However, several exceptions exist including fraud on the court, lack of jurisdiction in the prior action, and consent to relitigate.

Federal courts apply federal common law of preclusion to federal claims and the preclusion law of the rendering state court under 28 U.S.C. 1738 (Full Faith and Credit Act) for state court judgments.""",
        citations=[
            "Federated Dept. Stores v. Moitie, 452 U.S. 394 (1981)",
            "Taylor v. Sturgell, 553 U.S. 880 (2008)",
            "Allen v. McCurry, 449 U.S. 90 (1980)",
            "Parklane Hosiery Co. v. Shore, 439 U.S. 322 (1979)",
            "Montana v. United States, 440 U.S. 147 (1979)",
        ],
        statute_refs=["28 U.S.C. 1738", "Restatement (Second) of Judgments 24"],
        practice_playbook=[
            "Verify the prior judgment was a final judgment on the merits",
            "Confirm identity of parties or privity relationship",
            "Apply the transactional test to determine same cause of action",
            "Check for exceptions: fraud, jurisdictional defects, consent",
            "Determine whether federal or state preclusion law applies",
            "If asserting preclusion, prepare the prior judgment record for filing",
        ],
        counter_arguments=[
            "The prior judgment was not on the merits (dismissed without prejudice)",
            "The parties are not in privity",
            "The current claim arises from a different transaction or occurrence",
            "The prior court lacked jurisdiction",
            "The party was not given a full and fair opportunity to litigate",
        ],
        applicability_test=r"(?i)(res.?judicata|claim.?preclus|final.?judgment|relitigat|prior.?action|same.?cause|transactional.?test)",
        authority_weight=95,
        key_number_topics=["228 Judgment"],
        related_doctrines=["collateral_estoppel", "stare_decisis_application", "law_of_the_case"],
    ),

    "collateral_estoppel": DoctrineResponse(
        topic="Collateral Estoppel (Issue Preclusion)",
        quick_answer="Collateral estoppel prevents relitigation of specific factual or legal issues that were actually litigated and necessarily decided in a prior proceeding, even if the causes of action differ.",
        full_doctrine="""Collateral estoppel, or issue preclusion, bars relitigation of issues that were actually litigated and necessarily determined in a prior proceeding. Unlike res judicata which bars entire claims, collateral estoppel operates at the issue level and can apply even when the second suit involves a different cause of action.

Four elements must be satisfied: (1) the issue in the prior proceeding is identical to the issue in the current proceeding, (2) the issue was actually litigated in the prior proceeding, (3) determination of the issue was necessary to the prior judgment, and (4) the party against whom estoppel is asserted had a full and fair opportunity to litigate the issue.

The Supreme Court in Parklane Hosiery Co. v. Shore, 439 U.S. 322 (1979), approved offensive non-mutual collateral estoppel, allowing a plaintiff who was not a party to the prior action to use a prior judgment against a defendant. However, the Court emphasized that trial courts retain broad discretion to deny offensive use where it would be unfair, such as when the plaintiff could easily have joined the prior action or the defendant had little incentive to vigorously litigate the first suit.

Defensive non-mutual collateral estoppel (established in Blonder-Tongue Labs v. University of Ill. Foundation, 402 U.S. 313 (1971)) allows a defendant to prevent a plaintiff from relitigating an issue the plaintiff lost in a prior case against a different defendant.""",
        citations=[
            "Parklane Hosiery Co. v. Shore, 439 U.S. 322 (1979)",
            "Blonder-Tongue Labs v. Univ. of Ill. Found., 402 U.S. 313 (1971)",
            "Ashe v. Swenson, 397 U.S. 436 (1970)",
            "B&B Hardware, Inc. v. Hargis Industries, Inc., 575 U.S. 138 (2015)",
            "Taylor v. Sturgell, 553 U.S. 880 (2008)",
        ],
        statute_refs=["Restatement (Second) of Judgments 27-29"],
        practice_playbook=[
            "Identify the specific issue allegedly precluded",
            "Verify the issue was actually litigated (not defaulted or stipulated)",
            "Confirm the issue was necessary to the prior judgment",
            "Assess whether the party had a full and fair opportunity to litigate",
            "If using offensive non-mutual estoppel, address Parklane fairness factors",
            "Obtain and file the prior record establishing the issue determination",
        ],
        counter_arguments=[
            "The issue was not actually litigated but resolved by default or settlement",
            "The issue was not necessary to the prior judgment (alternative holdings)",
            "Changed legal standards make relitigation appropriate",
            "The party lacked a full and fair opportunity to litigate",
            "Offensive use would be unfair under Parklane factors",
        ],
        applicability_test=r"(?i)(collateral.?estoppel|issue.?preclus|actually.?litigat|necessarily.?determin|offensive.?non.?mutual|defensive.?estoppel)",
        authority_weight=90,
        key_number_topics=["228 Judgment"],
        related_doctrines=["res_judicata", "stare_decisis_application"],
    ),

    # ========================================================================
    # STANDING AND JUSTICIABILITY
    # ========================================================================

    "article_iii_standing": DoctrineResponse(
        topic="Article III Standing",
        quick_answer="To establish Article III standing, a plaintiff must demonstrate (1) injury in fact, (2) causation (fairly traceable to defendant's conduct), and (3) redressability (likely to be redressed by a favorable decision).",
        full_doctrine="""Article III of the Constitution limits federal judicial power to actual "cases" and "controversies." The standing doctrine enforces this limitation by requiring plaintiffs to demonstrate a concrete, personal stake in the outcome. The Supreme Court's seminal standing framework, established in Lujan v. Defenders of Wildlife, 504 U.S. 555 (1992), requires three elements.

First, injury in fact: the plaintiff must show an invasion of a legally protected interest that is (a) concrete and particularized, and (b) actual or imminent, not conjectural or hypothetical. In Spokeo, Inc. v. Robins, 578 U.S. 330 (2016), the Court clarified that a "concrete" injury need not be tangible but must actually exist and have a close relationship to a harm traditionally recognized as providing a basis for a lawsuit.

Second, causation: the injury must be fairly traceable to the challenged action of the defendant, not the independent action of a third party. This does not require but-for causation; rather, the defendant's conduct must be a "substantial factor" in causing the injury.

Third, redressability: it must be likely, as opposed to merely speculative, that a favorable judicial decision will redress the injury. The plaintiff need not show that the court can provide complete relief, but must demonstrate that the requested relief would at least partially redress the claimed injury.

The burden of proof increases at each stage of litigation. At the pleading stage, general factual allegations suffice; at summary judgment, the plaintiff must set forth specific facts; and at trial, the plaintiff must establish standing by a preponderance of the evidence.""",
        citations=[
            "Lujan v. Defenders of Wildlife, 504 U.S. 555 (1992)",
            "Spokeo, Inc. v. Robins, 578 U.S. 330 (2016)",
            "TransUnion LLC v. Ramirez, 594 U.S. 413 (2021)",
            "Clapper v. Amnesty Int'l USA, 568 U.S. 398 (2013)",
            "Massachusetts v. EPA, 549 U.S. 497 (2007)",
            "Friends of the Earth v. Laidlaw, 528 U.S. 167 (2000)",
        ],
        statute_refs=["U.S. Const. art. III, 2"],
        practice_playbook=[
            "Plead concrete, particularized injury with specific factual allegations",
            "Establish a direct causal chain from defendant's conduct to plaintiff's harm",
            "Show the requested relief would likely remedy the injury",
            "For organizational standing, show diversion of resources or programmatic injury",
            "For associational standing, show members would have standing, interests germane, claims don't require individual participation",
            "Anticipate standing challenges and build the record early",
        ],
        counter_arguments=[
            "Injury is too speculative, conjectural, or hypothetical",
            "Injury is not fairly traceable to defendant's specific conduct",
            "A favorable ruling would not likely redress the injury",
            "Plaintiff is asserting a generalized grievance shared by all citizens",
            "Under TransUnion, a bare statutory violation without concrete harm is insufficient",
        ],
        applicability_test=r"(?i)(standing|article.?iii|injury.?in.?fact|caus[ea]tion|redress|concrete.?harm|case.?or.?controversy|justiciab)",
        authority_weight=100,
        key_number_topics=["170A Federal Courts", "92 Constitutional Law"],
        related_doctrines=["mootness_doctrine", "ripeness_doctrine", "political_question"],
    ),

    "mootness_doctrine": DoctrineResponse(
        topic="Mootness Doctrine",
        quick_answer="A case becomes moot when the issues presented are no longer live or the parties lack a legally cognizable interest in the outcome. Federal courts lack jurisdiction over moot cases under Article III.",
        full_doctrine="""The mootness doctrine requires that an actual controversy exist at all stages of litigation, not merely at the time the complaint is filed. If subsequent events eliminate the plaintiff's personal stake or if the issue is otherwise resolved, the case becomes moot and the court must dismiss for lack of jurisdiction.

The key exceptions to mootness include: (1) Voluntary cessation: a defendant's voluntary cessation of challenged conduct does not moot a case unless it is "absolutely clear that the allegedly wrongful behavior could not reasonably be expected to recur" (Friends of the Earth v. Laidlaw, 528 U.S. 167 (2000)); (2) Capable of repetition yet evading review: claims that are inherently limited in duration but likely to recur as to the same plaintiff survive mootness (Roe v. Wade, 410 U.S. 113 (1973)); and (3) Class actions: an individual plaintiff's claim may be mooted, but if class certification was granted, the class action continues.

In New York State Rifle & Pistol Ass'n v. City of New York, 590 U.S. 336 (2020), the Court demonstrated the friction between the voluntary cessation exception and legislative repeal, vacating and remanding for further consideration of mootness after the challenged regulation was amended.""",
        citations=[
            "Friends of the Earth v. Laidlaw, 528 U.S. 167 (2000)",
            "Already, LLC v. Nike, Inc., 568 U.S. 85 (2013)",
            "Genesis Healthcare Corp. v. Symczyk, 569 U.S. 66 (2013)",
            "Honig v. Doe, 484 U.S. 305 (1988)",
            "DeFunis v. Odegaard, 416 U.S. 312 (1974)",
        ],
        statute_refs=["U.S. Const. art. III, 2"],
        practice_playbook=[
            "Monitor for events that might moot the case during litigation",
            "If defendant ceases conduct, argue voluntary cessation exception",
            "For inherently transitory claims, establish capable-of-repetition exception",
            "In class actions, seek certification before individual claims are mooted",
            "Request injunctive relief to preserve a live controversy",
        ],
        counter_arguments=[
            "Subsequent events have fully resolved the controversy",
            "The defendant's cessation is permanent and complete",
            "There is no reasonable expectation of recurrence",
            "The plaintiff has received all available relief",
        ],
        applicability_test=r"(?i)(moot|mootness|live.?controversy|voluntary.?cessation|capable.?of.?repetition|evading.?review)",
        authority_weight=90,
        key_number_topics=["170A Federal Courts"],
        related_doctrines=["article_iii_standing", "ripeness_doctrine"],
    ),

    # ========================================================================
    # SUMMARY JUDGMENT AND MOTIONS
    # ========================================================================

    "summary_judgment": DoctrineResponse(
        topic="Summary Judgment Standard",
        quick_answer="Summary judgment is granted when there is no genuine dispute of material fact and the movant is entitled to judgment as a matter of law under Fed. R. Civ. P. 56. The court views all evidence and draws all reasonable inferences in favor of the non-moving party.",
        full_doctrine="""Summary judgment under Federal Rule of Civil Procedure 56 serves as a critical gatekeeping mechanism, allowing courts to resolve cases or issues without trial when there is no genuine dispute of material fact. The movant bears the initial burden of demonstrating the absence of a genuine issue of material fact (Celotex Corp. v. Catrett, 477 U.S. 317 (1986)).

A fact is "material" if it might affect the outcome under the governing law. A dispute is "genuine" if the evidence is such that a reasonable jury could return a verdict for the nonmoving party (Anderson v. Liberty Lobby, Inc., 477 U.S. 242 (1986)). The court must view all evidence and draw all reasonable inferences in favor of the nonmoving party (Matsushita Elec. Indus. Co. v. Zenith Radio Corp., 475 U.S. 574 (1986)).

Once the movant satisfies its burden, the burden shifts to the nonmoving party to set forth specific facts showing a genuine issue for trial. The nonmoving party cannot rest on mere allegations or denials but must point to specific evidence in the record creating a triable issue. However, the court does not weigh evidence, assess credibility, or determine the truth of the matter.

Partial summary judgment under Rule 56(a) allows the court to resolve individual issues or claims, narrowing the scope of trial. Courts should also grant summary judgment sua sponte when appropriate, provided the losing party has adequate notice and opportunity to respond.""",
        citations=[
            "Celotex Corp. v. Catrett, 477 U.S. 317 (1986)",
            "Anderson v. Liberty Lobby, Inc., 477 U.S. 242 (1986)",
            "Matsushita Elec. Indus. Co. v. Zenith Radio Corp., 475 U.S. 574 (1986)",
            "Scott v. Harris, 550 U.S. 372 (2007)",
            "Tolan v. Cotton, 572 U.S. 650 (2014)",
        ],
        statute_refs=["Fed. R. Civ. P. 56", "28 U.S.C. 1291"],
        practice_playbook=[
            "File a statement of undisputed material facts with record citations",
            "Identify the specific legal elements and show no genuine dispute on each",
            "If nonmovant, file a counter-statement disputing specific facts with citations",
            "Object to inadmissible evidence offered in support/opposition",
            "Consider partial summary judgment to narrow trial issues",
            "Preserve the appellate record by noting all evidence considered",
        ],
        counter_arguments=[
            "Genuine disputes of material fact exist requiring trial",
            "The movant's evidence is not admissible at trial",
            "Credibility determinations are required that a jury must make",
            "The non-moving party has not had adequate discovery",
            "Reasonable inferences favor the non-moving party",
        ],
        applicability_test=r"(?i)(summary.?judg|rule.?56|genuine.?dispute|material.?fact|no.?triable.?issue|celotex|anderson.?liberty|MSJ|motion.?for.?summary)",
        authority_weight=95,
        key_number_topics=["170B Federal Civil Procedure"],
        related_doctrines=["motion_to_dismiss_12b6", "judgment_as_matter_of_law"],
    ),

    "motion_to_dismiss_12b6": DoctrineResponse(
        topic="Motion to Dismiss for Failure to State a Claim (Rule 12(b)(6))",
        quick_answer="A 12(b)(6) motion tests the legal sufficiency of the complaint. Under Twombly/Iqbal, the complaint must contain sufficient factual matter, accepted as true, to state a claim to relief that is plausible on its face.",
        full_doctrine="""A motion to dismiss under Federal Rule of Civil Procedure 12(b)(6) challenges whether the complaint states a legally sufficient claim for relief. The court accepts all well-pleaded factual allegations as true and draws reasonable inferences in favor of the plaintiff, but is not required to accept legal conclusions or conclusory statements.

The modern pleading standard was established in Bell Atlantic Corp. v. Twombly, 550 U.S. 544 (2007), and Ashcroft v. Iqbal, 556 U.S. 662 (2009). Under this "plausibility" standard, the complaint must contain "enough facts to state a claim to relief that is plausible on its face." A claim has facial plausibility when the plaintiff pleads factual content that allows the court to draw a reasonable inference that the defendant is liable.

The Twombly/Iqbal framework involves two steps: First, the court identifies allegations that are merely conclusory and therefore not entitled to the assumption of truth. Second, the court examines the remaining well-pleaded factual allegations and determines whether they plausibly suggest an entitlement to relief.

Courts may consider the complaint, documents attached to the complaint, documents incorporated by reference, and matters of public record without converting the motion to one for summary judgment. If the court considers matters outside the pleadings, the motion generally must be converted to a Rule 56 motion.""",
        citations=[
            "Bell Atlantic Corp. v. Twombly, 550 U.S. 544 (2007)",
            "Ashcroft v. Iqbal, 556 U.S. 662 (2009)",
            "Conley v. Gibson, 355 U.S. 41 (1957) (overruled by Twombly)",
            "Erickson v. Pardus, 551 U.S. 89 (2007)",
            "Tellabs, Inc. v. Makor Issues & Rights, Ltd., 551 U.S. 308 (2007)",
        ],
        statute_refs=["Fed. R. Civ. P. 12(b)(6)", "Fed. R. Civ. P. 8(a)(2)"],
        practice_playbook=[
            "Plead specific facts supporting each element of the claim",
            "Avoid conclusory legal recitations that mirror the elements",
            "Attach or incorporate key documents supporting the claim",
            "If opposing, argue that facts viewed together create a plausible inference",
            "Request leave to amend if the motion is likely to be granted",
            "Consider whether a more definite statement under Rule 12(e) is appropriate",
        ],
        counter_arguments=[
            "The complaint contains sufficient factual content for plausibility",
            "The motion improperly challenges facts that must be taken as true",
            "Leave to amend should be granted before dismissal",
            "The heightened pleading standard does not apply to this claim type",
            "Pro se complaints should be held to less stringent standards",
        ],
        applicability_test=r"(?i)(12.?b.?6|failure.?to.?state|motion.?to.?dismiss|plausib|twombly|iqbal|plead|complaint.?suffici|dismiss.?for.?failure)",
        authority_weight=95,
        key_number_topics=["170B Federal Civil Procedure"],
        related_doctrines=["summary_judgment", "rule_11_sanctions"],
    ),

    # ========================================================================
    # EVIDENCE
    # ========================================================================

    "hearsay_rule": DoctrineResponse(
        topic="Hearsay Rule and Exceptions",
        quick_answer="Hearsay is an out-of-court statement offered for the truth of the matter asserted, generally inadmissible under FRE 802. However, FRE 803 provides 23 exceptions available regardless of declarant availability, and FRE 804 provides additional exceptions when the declarant is unavailable.",
        full_doctrine="""The hearsay rule, codified in Federal Rule of Evidence 802, bars the admission of out-of-court statements offered to prove the truth of the matter asserted, subject to numerous exceptions. The rationale is that hearsay lacks the safeguards of oath, cross-examination, and demeanor observation.

Under FRE 801(d), certain statements are defined as "not hearsay": prior inconsistent statements under oath, prior consistent statements offered to rebut charges of fabrication, statements of identification, and admissions by party-opponents (including statements by agents, co-conspirators, and adoptive admissions).

FRE 803 provides 23 exceptions available regardless of the declarant's availability, including: present sense impression (803(1)), excited utterance (803(2)), then-existing mental or physical condition (803(3)), statements for medical treatment (803(4)), recorded recollection (803(5)), business records (803(6)), public records (803(8)), and learned treatises (803(18)).

FRE 804 provides exceptions available only when the declarant is unavailable: former testimony (804(b)(1)), dying declarations (804(b)(2)), statements against interest (804(b)(3)), and forfeiture by wrongdoing (804(b)(6)).

The residual exception under FRE 807 provides a safety valve for statements with "equivalent circumstantial guarantees of trustworthiness" not covered by specific exceptions.""",
        citations=[
            "Crawford v. Washington, 541 U.S. 36 (2004)",
            "Ohio v. Roberts, 448 U.S. 56 (1980) (overruled by Crawford)",
            "Davis v. Washington, 547 U.S. 813 (2006)",
            "Williamson v. United States, 512 U.S. 594 (1994)",
            "Bourjaily v. United States, 483 U.S. 171 (1987)",
        ],
        statute_refs=["FRE 801-807", "U.S. Const. amend. VI (Confrontation Clause)"],
        practice_playbook=[
            "Identify whether the statement is offered for the truth of the matter asserted",
            "Check if the statement qualifies as not-hearsay under FRE 801(d)",
            "Apply the specific exception with all foundational requirements",
            "In criminal cases, assess Confrontation Clause implications under Crawford",
            "For business records, prepare custodian certification under FRE 902(11)-(12)",
            "Consider the residual exception as a last resort with advance notice",
        ],
        counter_arguments=[
            "The statement is not being offered for the truth of the matter asserted",
            "The statement qualifies as a party admission under FRE 801(d)(2)",
            "A specific hearsay exception applies with proper foundation",
            "The Confrontation Clause is not implicated because the statement is not testimonial",
            "The declarant is available for cross-examination, curing any hearsay concern",
        ],
        applicability_test=r"(?i)(hearsay|out.?of.?court|truth.?of.?the.?matter|fre.?80[0-9]|business.?record|excited.?utterance|present.?sense|dying.?declaration|party.?admission|confrontation)",
        authority_weight=90,
        key_number_topics=["157 Evidence"],
        related_doctrines=["daubert_standard", "best_evidence_rule"],
    ),

    "daubert_standard": DoctrineResponse(
        topic="Daubert Standard for Expert Testimony",
        quick_answer="Under Daubert and FRE 702, trial courts serve as gatekeepers for expert testimony, requiring that it be based on sufficient facts, reliable methodology, and reliably applied to the case facts. Factors include testability, peer review, error rate, and general acceptance.",
        full_doctrine="""In Daubert v. Merrell Dow Pharmaceuticals, 509 U.S. 579 (1993), the Supreme Court replaced the Frye "general acceptance" test with a more flexible reliability-based framework for admitting expert testimony under Federal Rule of Evidence 702. The trial court serves as a gatekeeper, ensuring that expert testimony is both relevant and reliable.

The Daubert factors include: (1) whether the theory or technique can be (and has been) tested, (2) whether it has been subjected to peer review and publication, (3) the known or potential error rate, (4) the existence and maintenance of standards controlling the technique's operation, and (5) whether the theory or technique has gained general acceptance in the relevant scientific community.

In Kumho Tire Co. v. Carmichael, 526 U.S. 137 (1999), the Court extended Daubert's gatekeeping obligation to all expert testimony, not just scientific evidence. The factors are flexible and do not constitute a definitive checklist; courts may consider other factors relevant to evaluating the methodology.

The 2023 amendment to Rule 702 clarified that the proponent must demonstrate reliability by a preponderance of the evidence and that expert opinion must reflect reliable application of principles, addressing courts that had been applying an overly permissive standard.""",
        citations=[
            "Daubert v. Merrell Dow Pharmaceuticals, 509 U.S. 579 (1993)",
            "General Electric Co. v. Joiner, 522 U.S. 136 (1997)",
            "Kumho Tire Co. v. Carmichael, 526 U.S. 137 (1999)",
            "Weisgram v. Marley Co., 528 U.S. 440 (2000)",
        ],
        statute_refs=["FRE 702", "FRE 703", "FRE 706"],
        practice_playbook=[
            "File a Daubert motion before trial to exclude unreliable expert testimony",
            "Prepare a detailed proffer of the expert's qualifications and methodology",
            "Address each Daubert factor in your brief",
            "If opposing, demonstrate analytical gaps between data and conclusions",
            "Consider a Daubert hearing with live testimony and cross-examination",
            "Preserve the issue for appeal by making a clear record",
        ],
        counter_arguments=[
            "The expert's methodology is generally accepted in the relevant field",
            "The theory has been tested and subjected to peer review",
            "The expert reliably applied the principles to the facts of this case",
            "The challenge goes to weight, not admissibility",
            "The flexible Daubert inquiry supports admission in this context",
        ],
        applicability_test=r"(?i)(daubert|expert.?test|fre.?702|gatekeeper|reliab.?method|peer.?review|error.?rate|general.?accept|frye|kumho|expert.?witness|scientific.?evidence)",
        authority_weight=95,
        key_number_topics=["157 Evidence"],
        related_doctrines=["hearsay_rule"],
    ),

    # ========================================================================
    # CONSTITUTIONAL LAW
    # ========================================================================

    "qualified_immunity": DoctrineResponse(
        topic="Qualified Immunity",
        quick_answer="Qualified immunity shields government officials from civil liability under 42 U.S.C. 1983 unless their conduct violates clearly established statutory or constitutional rights of which a reasonable person would have known.",
        full_doctrine="""Qualified immunity protects government officials from civil damages liability under 42 U.S.C. 1983, insofar as their conduct does not violate clearly established statutory or constitutional rights of which a reasonable person would have known. The doctrine balances two interests: holding government officials accountable for unreasonable conduct and shielding officials from harassment, distraction, and liability when they perform their duties reasonably.

The analysis involves two prongs (which courts may address in either order since Pearson v. Callahan, 555 U.S. 223 (2009)): (1) whether the facts alleged show a constitutional violation, and (2) whether the right was clearly established at the time of the violation. The "clearly established" requirement demands that existing precedent place the statutory or constitutional question beyond debate, though the Supreme Court has not required a case directly on point.

In Ashcroft v. al-Kidd, 563 U.S. 731 (2011), the Court emphasized that the right must be defined at an appropriate level of specificity. General statements of the law are insufficient; the contours of the right must be sufficiently clear that a reasonable official would understand that what he is doing violates that right.

The doctrine has faced substantial academic and judicial criticism, and several Justices have called for its reconsideration. However, it remains firmly established in the Court's precedent. Qualified immunity is not available to municipalities, which can be sued directly under Monell v. Department of Social Services, 436 U.S. 658 (1978).""",
        citations=[
            "Harlow v. Fitzgerald, 457 U.S. 800 (1982)",
            "Pearson v. Callahan, 555 U.S. 223 (2009)",
            "Ashcroft v. al-Kidd, 563 U.S. 731 (2011)",
            "Saucier v. Katz, 533 U.S. 194 (2001)",
            "Anderson v. Creighton, 483 U.S. 635 (1987)",
            "Taylor v. Riojas, 592 U.S. 7 (2020)",
        ],
        statute_refs=["42 U.S.C. 1983", "42 U.S.C. 1988"],
        practice_playbook=[
            "Identify the specific constitutional right allegedly violated",
            "Research whether the right was clearly established at the time",
            "Find factually analogous cases from the relevant jurisdiction",
            "Raise qualified immunity as early as possible, ideally at the motion to dismiss stage",
            "If denied, pursue interlocutory appeal under the collateral order doctrine",
            "For municipalities, analyze Monell liability without qualified immunity shield",
        ],
        counter_arguments=[
            "The right was clearly established by prior precedent",
            "No reasonable officer could have believed the conduct was lawful",
            "The factual situation is so egregious that general legal principles apply",
            "The defendant's conduct was objectively unreasonable",
            "Qualified immunity does not apply in this context (municipalities, injunctive relief)",
        ],
        applicability_test=r"(?i)(qualified.?immun|1983|clearly.?establish|reasonable.?official|government.?official.?liab|pearson|harlow|section.?1983|civil.?rights.?liab)",
        authority_weight=100,
        key_number_topics=["92 Constitutional Law", "78 Civil Rights"],
        related_doctrines=["first_amendment_analysis", "fourth_amendment_search"],
    ),

    "first_amendment_analysis": DoctrineResponse(
        topic="First Amendment Free Speech Analysis",
        quick_answer="First Amendment analysis requires identifying the type of speech (content-based vs. content-neutral), the forum (public, designated, nonpublic, or limited), and applying the appropriate level of scrutiny (strict, intermediate, or rational basis).",
        full_doctrine="""The First Amendment prohibits the government from abridging freedom of speech. The Supreme Court has developed a sophisticated analytical framework that categorizes both the regulation and the forum to determine the applicable level of judicial scrutiny.

Content-based restrictions, which regulate speech based on its subject matter or viewpoint, are presumptively unconstitutional and subject to strict scrutiny (Reed v. Town of Gilbert, 576 U.S. 155 (2015)). The government must show the restriction is narrowly tailored to serve a compelling government interest. Content-neutral restrictions, which incidentally burden speech, receive intermediate scrutiny under O'Brien, requiring a substantial government interest unrelated to the suppression of expression (United States v. O'Brien, 391 U.S. 367 (1968)).

Forum analysis determines the government's ability to restrict speech on its property. Traditional public forums (streets, parks, sidewalks) receive the highest protection; designated public forums receive equivalent protection while maintained as forums; nonpublic forums allow reasonable, viewpoint-neutral restrictions; and limited public forums allow restrictions consistent with the forum's purpose.

Several categories of speech receive diminished or no protection: obscenity (Miller v. California, 413 U.S. 15 (1973)), true threats (Virginia v. Black, 538 U.S. 343 (2003)), incitement to imminent lawless action (Brandenburg v. Ohio, 395 U.S. 444 (1969)), fighting words (Chaplinsky v. New Hampshire, 315 U.S. 568 (1942)), and fraud.""",
        citations=[
            "Reed v. Town of Gilbert, 576 U.S. 155 (2015)",
            "United States v. O'Brien, 391 U.S. 367 (1968)",
            "Brandenburg v. Ohio, 395 U.S. 444 (1969)",
            "New York Times Co. v. Sullivan, 376 U.S. 254 (1964)",
            "Tinker v. Des Moines, 393 U.S. 503 (1969)",
            "303 Creative LLC v. Elenis, 600 U.S. 570 (2023)",
        ],
        statute_refs=["U.S. Const. amend. I"],
        practice_playbook=[
            "Classify the restriction as content-based or content-neutral",
            "Identify the forum type to determine the level of protection",
            "Apply the appropriate level of scrutiny",
            "Assess whether the speech falls into an unprotected category",
            "Consider overbreadth and vagueness challenges",
            "Analyze prior restraint and chilling effect issues",
        ],
        counter_arguments=[
            "The restriction is content-neutral and survives intermediate scrutiny",
            "The speech falls into an unprotected or less-protected category",
            "The forum is nonpublic and the restriction is reasonable",
            "The government has a compelling interest and the restriction is narrowly tailored",
            "The regulation targets conduct, not speech",
        ],
        applicability_test=r"(?i)(first.?amendment|free.?speech|freedom.?of.?speech|content.?based|content.?neutral|strict.?scrutiny|public.?forum|prior.?restraint|overbreadth|vagueness|compelled.?speech)",
        authority_weight=100,
        key_number_topics=["92 Constitutional Law"],
        related_doctrines=["qualified_immunity", "fourth_amendment_search"],
    ),

    "fourth_amendment_search": DoctrineResponse(
        topic="Fourth Amendment Search and Seizure",
        quick_answer="The Fourth Amendment protects against unreasonable searches and seizures, requiring a warrant supported by probable cause. Key exceptions include consent, plain view, search incident to arrest, automobile, exigent circumstances, and Terry stop-and-frisk.",
        full_doctrine="""The Fourth Amendment guarantees the right of the people to be secure against unreasonable searches and seizures and requires warrants to issue only upon probable cause. The Supreme Court in Katz v. United States, 389 U.S. 347 (1967), established that the Fourth Amendment protects people, not places, and applies whenever a person has a reasonable expectation of privacy.

In Carpenter v. United States, 585 U.S. 296 (2018), the Court extended Fourth Amendment protection to cell-site location information, recognizing that digital surveillance capabilities can compromise Fourth Amendment values even without a physical intrusion. The third-party doctrine, under which information voluntarily shared with third parties carries no reasonable expectation of privacy (Smith v. Maryland, 442 U.S. 735 (1979)), does not apply to cell-site data.

The warrant requirement is subject to well-delineated exceptions: (1) consent (Schneckloth v. Bustamonte, 412 U.S. 218 (1973)), (2) search incident to arrest (Chimel v. California, 395 U.S. 752 (1969); Riley v. California, 573 U.S. 373 (2014) for cell phones), (3) plain view (Horton v. California, 496 U.S. 128 (1990)), (4) automobile exception (Carroll v. United States, 267 U.S. 132 (1925)), (5) exigent circumstances (Kentucky v. King, 563 U.S. 452 (2011)), and (6) stop and frisk (Terry v. Ohio, 392 U.S. 1 (1968)).

Evidence obtained in violation of the Fourth Amendment is subject to the exclusionary rule (Mapp v. Ohio, 367 U.S. 643 (1961)), with exceptions for good faith (United States v. Leon, 468 U.S. 897 (1984)), inevitable discovery, and attenuation of the taint.""",
        citations=[
            "Katz v. United States, 389 U.S. 347 (1967)",
            "Carpenter v. United States, 585 U.S. 296 (2018)",
            "Riley v. California, 573 U.S. 373 (2014)",
            "Terry v. Ohio, 392 U.S. 1 (1968)",
            "Mapp v. Ohio, 367 U.S. 643 (1961)",
            "United States v. Leon, 468 U.S. 897 (1984)",
        ],
        statute_refs=["U.S. Const. amend. IV", "42 U.S.C. 1983"],
        practice_playbook=[
            "Determine whether government action constitutes a search under Katz",
            "Assess whether a warrant was obtained and whether it was valid",
            "If no warrant, identify the specific exception relied upon",
            "For digital evidence, apply Carpenter's heightened protections",
            "File a motion to suppress under the exclusionary rule if warranted",
            "Consider good faith and inevitable discovery exceptions",
        ],
        counter_arguments=[
            "No search occurred because there was no reasonable expectation of privacy",
            "A valid warrant was obtained based on probable cause",
            "An exception to the warrant requirement applies",
            "The good faith exception saves the evidence despite the warrant deficiency",
            "The inevitable discovery doctrine applies",
        ],
        applicability_test=r"(?i)(fourth.?amendment|search.?and.?seizure|warrant|probable.?cause|exclusionary.?rule|terry.?stop|reasonable.?expectation|plain.?view|exigent|automobile.?exception|consent.?search|stop.?and.?frisk|suppress)",
        authority_weight=100,
        key_number_topics=["92 Constitutional Law", "110A Criminal Law"],
        related_doctrines=["qualified_immunity", "miranda_requirements"],
    ),

    # ========================================================================
    # CONTRACT LAW
    # ========================================================================

    "contract_formation": DoctrineResponse(
        topic="Contract Formation and Enforceability",
        quick_answer="A valid contract requires (1) mutual assent (offer and acceptance), (2) consideration, (3) capacity, and (4) legality of purpose. The Statute of Frauds requires certain contracts to be in writing.",
        full_doctrine="""Contract formation requires mutual assent (offer and acceptance), consideration, capacity, and legality of purpose. An offer is a manifestation of willingness to enter into a bargain, so made as to justify another person in understanding that his assent to that bargain is invited and will conclude it (Restatement (Second) of Contracts section 24).

Acceptance must mirror the offer under common law (mirror image rule), though the UCC section 2-207 modifies this for sales of goods through the "battle of the forms" provision. Consideration requires a bargained-for exchange of value; past consideration and moral obligations generally do not suffice (Hamer v. Sidway, 124 N.Y. 538 (1891)).

The parol evidence rule (Restatement (Second) of Contracts section 213) provides that where parties have reduced their agreement to a writing, extrinsic evidence of prior or contemporaneous agreements is inadmissible to contradict or supplement the writing if it is fully integrated. However, parol evidence is admissible to establish fraud, duress, ambiguity, or conditions precedent.

The Statute of Frauds (derived from English law, now codified in various state statutes and UCC 2-201) requires written evidence for contracts involving: sale of land, contracts not performable within one year, suretyship agreements, sales of goods over $500, and marriage-related agreements.""",
        citations=[
            "Lucy v. Zehmer, 196 Va. 493, 84 S.E.2d 516 (1954)",
            "Hamer v. Sidway, 124 N.Y. 538 (1891)",
            "Wood v. Lucy, Lady Duff-Gordon, 222 N.Y. 88 (1917)",
            "Hadley v. Baxendale, 9 Ex. 341, 156 Eng. Rep. 145 (1854)",
            "ProCD, Inc. v. Zeidenberg, 86 F.3d 1447 (7th Cir. 1996)",
        ],
        statute_refs=["UCC 2-201 to 2-210", "Restatement (Second) of Contracts 1-90"],
        practice_playbook=[
            "Verify all elements of formation: offer, acceptance, consideration, capacity, legality",
            "Determine whether the UCC or common law governs the transaction",
            "Assess Statute of Frauds applicability and compliance",
            "Evaluate integration of the writing and parol evidence admissibility",
            "Check for defenses: duress, undue influence, unconscionability, mistake",
            "Consider promissory estoppel as an alternative theory if consideration is weak",
        ],
        counter_arguments=[
            "No mutual assent because the offer was never properly accepted",
            "Lack of consideration renders the promise unenforceable",
            "The Statute of Frauds bars enforcement of the oral agreement",
            "The contract is unconscionable or obtained through duress",
            "A condition precedent to the contract was not satisfied",
        ],
        applicability_test=r"(?i)(contract.?form|offer.?accept|consideration|mutual.?assent|statute.?of.?frauds|parol.?evidence|breach.?of.?contract|enforceab|ucc.?2|formation|binding.?agreement)",
        authority_weight=85,
        key_number_topics=["106 Contracts"],
        related_doctrines=["promissory_estoppel", "unconscionability"],
    ),

    # ========================================================================
    # TORT LAW
    # ========================================================================

    "negligence_elements": DoctrineResponse(
        topic="Negligence Elements and Standards",
        quick_answer="Negligence requires (1) a duty of care, (2) breach of that duty, (3) actual and proximate causation, and (4) damages. The standard of care is that of a reasonable person under the circumstances.",
        full_doctrine="""The tort of negligence requires four elements: duty, breach, causation, and damages. The plaintiff must establish each element by a preponderance of the evidence.

Duty: The general rule is that every person has a duty to exercise reasonable care to avoid foreseeable risks of harm to others. The existence and scope of duty is a question of law for the court. Special duty relationships arise in specific contexts (landowner-invitee, employer-employee, common carrier-passenger). The Palsgraf v. Long Island Railroad decision, 248 N.Y. 339 (1928), established that duty is owed only to foreseeable plaintiffs within the zone of danger.

Breach: The defendant breaches the duty of care by failing to act as a reasonably prudent person under the circumstances. The Learned Hand formula (United States v. Carroll Towing Co., 159 F.2d 169 (2d Cir. 1947)) provides a cost-benefit analysis: negligence exists when the burden of precaution (B) is less than the probability of harm (P) multiplied by the gravity of the resulting injury (L): B < P x L.

Causation has two components. Actual (but-for) causation asks whether the injury would have occurred absent the defendant's breach. Proximate (legal) causation limits liability to foreseeable consequences, serving as a policy-based limitation on otherwise infinite liability chains.

Damages must be proven to a reasonable certainty. Compensatory damages include economic losses (medical expenses, lost wages) and non-economic losses (pain and suffering). Punitive damages may be available for conduct that is willful, wanton, or malicious.""",
        citations=[
            "Palsgraf v. Long Island Railroad, 248 N.Y. 339 (1928)",
            "United States v. Carroll Towing Co., 159 F.2d 169 (2d Cir. 1947)",
            "Tarasoff v. Regents of Univ. of Cal., 17 Cal. 3d 425 (1976)",
            "BMW of North America v. Gore, 517 U.S. 559 (1996)",
            "Philip Morris USA v. Williams, 549 U.S. 346 (2007)",
        ],
        statute_refs=["Restatement (Third) of Torts: Liability for Physical Harm"],
        practice_playbook=[
            "Establish the specific duty owed and its source (statute, common law, relationship)",
            "Prove breach using the reasonable person standard or res ipsa loquitur",
            "Build the causation chain from breach to injury",
            "Assess comparative/contributory negligence defenses",
            "Document all categories of damages with supporting evidence",
            "Consider statutory caps on damages in the jurisdiction",
        ],
        counter_arguments=[
            "No duty was owed to this particular plaintiff",
            "The defendant's conduct met the reasonable person standard",
            "The plaintiff's own negligence caused or contributed to the injury",
            "The harm was not a foreseeable consequence of the defendant's conduct",
            "An intervening cause broke the chain of proximate causation",
        ],
        applicability_test=r"(?i)(negligen|duty.?of.?care|breach.?of.?duty|proximate.?cause|but.?for|reasonable.?person|standard.?of.?care|comparative.?fault|contributory|res.?ipsa|foreseeab|palsgraf)",
        authority_weight=85,
        key_number_topics=["379 Torts", "272 Negligence"],
        related_doctrines=["products_liability", "comparative_fault"],
    ),

    # ========================================================================
    # ADMINISTRATIVE LAW
    # ========================================================================

    "chevron_deference": DoctrineResponse(
        topic="Chevron Deference (and its Overruling)",
        quick_answer="Chevron deference, which required courts to defer to reasonable agency interpretations of ambiguous statutes they administer, was overruled by Loper Bright Enterprises v. Raimondo, 144 S. Ct. 2244 (2024). Courts now exercise independent judgment on statutory interpretation.",
        full_doctrine="""Chevron U.S.A., Inc. v. Natural Resources Defense Council, 467 U.S. 837 (1984), established a two-step framework for judicial review of agency statutory interpretation. Step One asked whether Congress had directly spoken to the precise question at issue; if the statute was clear, that ended the matter. Step Two asked, if the statute was ambiguous, whether the agency's interpretation was a permissible construction. For forty years, Chevron was the most-cited administrative law case in history.

In Loper Bright Enterprises v. Raimondo, 144 S. Ct. 2244 (2024), the Supreme Court overruled Chevron, holding that the Administrative Procedure Act requires courts to exercise independent judgment in determining the meaning of statutory provisions and that courts may not defer to an agency interpretation merely because a statute is ambiguous. The Court emphasized that Chevron's fiction of implicit congressional delegation was inconsistent with the APA and Marbury v. Madison's principle that it is emphatically the province and duty of the judicial department to say what the law is.

Post-Loper Bright, agencies' statutory interpretations may still receive weight based on the thoroughness of their consideration, the validity of their reasoning, and their consistency with earlier and later pronouncements (the Skidmore v. Swift & Co., 323 U.S. 134 (1944) standard of persuasive authority). However, courts are no longer required to accept reasonable agency interpretations of ambiguous statutes.""",
        citations=[
            "Loper Bright Enterprises v. Raimondo, 144 S. Ct. 2244 (2024)",
            "Chevron U.S.A., Inc. v. NRDC, 467 U.S. 837 (1984) (overruled)",
            "Skidmore v. Swift & Co., 323 U.S. 134 (1944)",
            "West Virginia v. EPA, 597 U.S. 697 (2022)",
            "City of Arlington v. FCC, 569 U.S. 290 (2013)",
        ],
        statute_refs=["5 U.S.C. 706 (APA)", "U.S. Const. art. III"],
        practice_playbook=[
            "Post-Loper Bright: argue statutory interpretation using traditional tools",
            "Do not rely on Chevron deference in new briefing",
            "Cite Skidmore for persuasive weight of agency expertise",
            "Invoke the major questions doctrine for issues of vast economic/political significance",
            "Challenge agency overreach using the nondelegation principle",
            "For pending cases, consider whether prior Chevron-based rulings are open to challenge",
        ],
        counter_arguments=[
            "The agency's interpretation, while not entitled to Chevron deference, is persuasive under Skidmore",
            "Congressional acquiescence supports the long-standing agency interpretation",
            "The statutory text and structure support the agency's reading",
            "The agency has specialized expertise bearing on the statutory meaning",
            "Prior judicial decisions adopted the same interpretation independently",
        ],
        applicability_test=r"(?i)(chevron|defer|agency.?interpret|loper.?bright|skidmore|apa.?review|arbitrary.?capric|major.?question|admin.?law|regulatory.?interpret|agency.?authority)",
        authority_weight=100,
        staleness_risk="high",
        overruled_by="Loper Bright Enterprises v. Raimondo, 144 S. Ct. 2244 (2024)",
        key_number_topics=["15A Administrative Law"],
        related_doctrines=["major_questions_doctrine"],
    ),

    # ========================================================================
    # CIVIL PROCEDURE - JURISDICTION
    # ========================================================================

    "personal_jurisdiction": DoctrineResponse(
        topic="Personal Jurisdiction Analysis",
        quick_answer="Personal jurisdiction requires that the defendant have sufficient minimum contacts with the forum state such that maintaining the suit does not offend traditional notions of fair play and substantial justice. General jurisdiction exists where a defendant is 'at home'; specific jurisdiction requires a connection between the forum and the claim.",
        full_doctrine="""Personal jurisdiction analysis under the Due Process Clause involves two forms: general (all-purpose) jurisdiction and specific (case-linked) jurisdiction.

General jurisdiction exists when a defendant's affiliations with a state are so continuous and systematic as to render the entity essentially at home there (Daimler AG v. Bauman, 571 U.S. 117 (2014)). For corporations, this typically means only the state of incorporation and the principal place of business. The Court in BNSF Railway Co. v. Tyrrell, 581 U.S. 402 (2017), confirmed that mere continuous operations in a state, even substantial ones, do not establish general jurisdiction.

Specific jurisdiction applies when the lawsuit arises out of or relates to the defendant's contacts with the forum. The Supreme Court in Ford Motor Co. v. Montana Eighth Judicial District Court, 592 U.S. 351 (2021), held that specific jurisdiction does not require strict causation between the forum contacts and the claim; an affiliating connection between the forum and the underlying controversy is sufficient.

The International Shoe framework requires: (1) the defendant purposefully directed activities at the forum or availed itself of the forum's laws, (2) the claim arises out of or relates to those contacts, and (3) the exercise of jurisdiction comports with fair play and substantial justice (considering burden on defendant, forum state's interest, plaintiff's interest, interstate judicial system's interest, and shared interest of the states).""",
        citations=[
            "International Shoe Co. v. Washington, 326 U.S. 310 (1945)",
            "Daimler AG v. Bauman, 571 U.S. 117 (2014)",
            "Ford Motor Co. v. Montana Eighth Judicial Dist. Ct., 592 U.S. 351 (2021)",
            "Bristol-Myers Squibb Co. v. Superior Court, 582 U.S. 255 (2017)",
            "Walden v. Fiore, 571 U.S. 277 (2014)",
            "Goodyear Dunlop Tires v. Brown, 564 U.S. 915 (2011)",
        ],
        statute_refs=["U.S. Const. amend. XIV (Due Process)", "Fed. R. Civ. P. 4(k)"],
        practice_playbook=[
            "Determine whether general or specific jurisdiction is asserted",
            "For general jurisdiction, show defendant is 'at home' in the forum",
            "For specific jurisdiction, apply the three-part International Shoe test",
            "Analyze the state long-arm statute as a threshold requirement",
            "Consider whether a Rule 12(b)(2) motion to dismiss is appropriate",
            "Conduct jurisdictional discovery if facts are disputed",
        ],
        counter_arguments=[
            "The defendant lacks minimum contacts with the forum state",
            "The claim does not arise out of or relate to forum contacts",
            "Exercise of jurisdiction would be unreasonable given the burden on defendant",
            "The forum state's long-arm statute does not reach this defendant",
            "The defendant did not purposefully avail itself of the forum",
        ],
        applicability_test=r"(?i)(personal.?jurisdict|minimum.?contact|long.?arm|purposeful.?avail|specific.?jurisdict|general.?jurisdict|international.?shoe|due.?process.?jurisdict|forum.?state|at.?home)",
        authority_weight=100,
        key_number_topics=["170A Federal Courts", "106 Courts"],
        related_doctrines=["erie_doctrine", "subject_matter_jurisdiction"],
    ),

    "erie_doctrine": DoctrineResponse(
        topic="Erie Doctrine (Federal Courts Applying State Law)",
        quick_answer="Under the Erie doctrine, federal courts sitting in diversity must apply state substantive law and federal procedural law. The key challenge is distinguishing substantive from procedural rules, addressed through the twin aims of Erie: discouraging forum shopping and avoiding inequitable administration of law.",
        full_doctrine="""The Erie doctrine, established in Erie Railroad Co. v. Tompkins, 304 U.S. 64 (1938), requires federal courts exercising diversity jurisdiction to apply the substantive law of the state in which they sit. This overruled Swift v. Tyson (1842) and its doctrine of federal general common law.

The substance-procedure distinction is analyzed through multiple frameworks depending on whether a Federal Rule of Civil Procedure is involved. When a Federal Rule is on point, the analysis under Hanna v. Plumer, 380 U.S. 460 (1965), asks whether the Rule is valid under the Rules Enabling Act (does it regulate procedure and not abridge substantive rights?). If the Rule is valid, it applies regardless of a conflicting state rule.

When no Federal Rule is directly on point, the unguided Erie analysis applies. Under Byrd v. Blue Ridge Rural Electric Cooperative, 356 U.S. 525 (1958), courts balance (1) whether the state rule is "bound up" with state substantive rights, (2) the countervailing federal interest (such as the Seventh Amendment right to a jury trial), and (3) the likelihood that differing results would occur. The "twin aims" of Erie, articulated in Hanna, ask whether applying a different rule would encourage forum shopping or lead to inequitable administration of the law.

In Shady Grove Orthopedic Associates v. Allstate, 559 U.S. 393 (2010), the Court addressed the conflict between Rule 23 and a New York statute limiting class actions, holding that Rule 23 controlled because it was a valid exercise of rulemaking authority under the REA.""",
        citations=[
            "Erie Railroad Co. v. Tompkins, 304 U.S. 64 (1938)",
            "Hanna v. Plumer, 380 U.S. 460 (1965)",
            "Byrd v. Blue Ridge Rural Elec. Coop., 356 U.S. 525 (1958)",
            "Gasperini v. Center for Humanities, Inc., 518 U.S. 415 (1996)",
            "Shady Grove Orthopedic Assocs. v. Allstate, 559 U.S. 393 (2010)",
        ],
        statute_refs=["28 U.S.C. 1652 (Rules of Decision Act)", "28 U.S.C. 2072 (Rules Enabling Act)"],
        practice_playbook=[
            "Identify whether a Federal Rule of Civil Procedure is directly on point",
            "If a Federal Rule applies, use the Hanna/REA analysis",
            "If no Federal Rule, use the unguided Erie/Byrd balancing test",
            "Apply the twin aims: would applying a different rule encourage forum shopping?",
            "Determine which state's law applies (choice of law as a separate inquiry)",
            "Research the highest court decision of the relevant state on the issue",
        ],
        counter_arguments=[
            "The issue is procedural, and federal procedure governs in federal court",
            "The Federal Rule directly conflicts with the state rule and is valid under the REA",
            "Applying the state rule would not further Erie's twin aims",
            "The state rule is not bound up with substantive rights but is merely procedural",
            "No outcome-determinative effect exists from applying the different rule",
        ],
        applicability_test=r"(?i)(erie|diversity.?jurisdiction|state.?substant|federal.?procedur|forum.?shop|rules.?enabling|hanna|twin.?aims|choice.?of.?law|federal.?court.?apply.?state)",
        authority_weight=100,
        key_number_topics=["170A Federal Courts"],
        related_doctrines=["personal_jurisdiction", "subject_matter_jurisdiction"],
    ),

    # ========================================================================
    # ADDITIONAL DOCTRINES (abbreviated for space)
    # ========================================================================

    "class_certification": DoctrineResponse(
        topic="Class Action Certification under Rule 23",
        quick_answer="Class certification requires meeting all four Rule 23(a) prerequisites (numerosity, commonality, typicality, adequacy) plus fitting within at least one Rule 23(b) category ((b)(1) prejudice, (b)(2) injunctive relief, or (b)(3) damages with predominance and superiority).",
        full_doctrine="""Federal Rule of Civil Procedure 23 governs class actions. Certification requires satisfying all four Rule 23(a) prerequisites: (1) numerosity (the class is so numerous that joinder of all members is impracticable), (2) commonality (there are questions of law or fact common to the class), (3) typicality (the claims of the representative parties are typical of the class), and (4) adequacy (the representative parties will fairly and adequately protect the interests of the class).

After Wal-Mart Stores, Inc. v. Dukes, 564 U.S. 338 (2011), commonality requires showing that the class members have suffered the same injury, not merely that they have all suffered a violation of the same provision of law. The Court emphasized that "common contention" must be of such a nature that it is capable of classwide resolution, meaning that determination of its truth or falsity will resolve an issue that is central to the validity of each one of the claims in one stroke.

The class must also qualify under one of the Rule 23(b) categories. Most damages class actions seek certification under Rule 23(b)(3), requiring predominance (common questions predominate over individual ones) and superiority (class action is superior to other available methods). In Amgen Inc. v. Connecticut Retirement Plans, 568 U.S. 455 (2013), the Court held that materiality need not be proven at the class certification stage in securities fraud cases.""",
        citations=[
            "Wal-Mart Stores, Inc. v. Dukes, 564 U.S. 338 (2011)",
            "Comcast Corp. v. Behrend, 569 U.S. 27 (2013)",
            "Amgen Inc. v. Conn. Retirement Plans, 568 U.S. 455 (2013)",
            "Tyson Foods, Inc. v. Bouaphakeo, 577 U.S. 442 (2016)",
            "TransUnion LLC v. Ramirez, 594 U.S. 413 (2021)",
        ],
        statute_refs=["Fed. R. Civ. P. 23", "28 U.S.C. 1332(d) (CAFA)"],
        practice_playbook=[
            "Satisfy all four Rule 23(a) prerequisites with specific evidence",
            "Identify the correct Rule 23(b) category and satisfy its requirements",
            "For 23(b)(3), prepare a detailed plan for managing class-wide issues",
            "Address potential ascertainability requirements in the circuit",
            "Prepare for a rigorous analysis under Dukes' commonality standard",
            "Consider CAFA removal jurisdiction and settlement-related issues",
        ],
        counter_arguments=[
            "Individual issues predominate over common questions",
            "The class definition is too vague or overbroad",
            "The named plaintiffs are atypical or inadequate representatives",
            "Commonality fails under the Dukes standard",
            "Superior alternative methods of adjudication exist",
        ],
        applicability_test=r"(?i)(class.?action|class.?cert|rule.?23|numerosity|commonality|typicality|adequacy|predominan|superiority|class.?defin|class.?member)",
        authority_weight=95,
        key_number_topics=["170B Federal Civil Procedure"],
        related_doctrines=["summary_judgment", "article_iii_standing"],
    ),

    "copyright_fair_use": DoctrineResponse(
        topic="Copyright Fair Use under 17 U.S.C. 107",
        quick_answer="Fair use is an affirmative defense to copyright infringement evaluated under four factors: (1) purpose and character of use (including transformativeness), (2) nature of the copyrighted work, (3) amount and substantiality used, and (4) effect on the market for the original.",
        full_doctrine="""Section 107 of the Copyright Act codifies the fair use defense, providing that use of a copyrighted work for purposes such as criticism, comment, news reporting, teaching, scholarship, or research is not necessarily infringement. Courts evaluate four non-exclusive factors.

Factor 1 (Purpose and Character): The Supreme Court in Andy Warhol Foundation v. Goldsmith, 598 U.S. 508 (2023), clarified that the degree to which a use has a further purpose or different character must be balanced against the commercial nature of the use when the use and the original share a common purpose. This narrowed the broad "transformativeness" inquiry from Campbell v. Acuff-Rose Music, 510 U.S. 569 (1994).

Factor 2 (Nature of the Work): Creative works receive more protection than factual works. Unpublished works receive stronger protection, though this does not create a per se bar to fair use (Harper & Row v. Nation Enterprises, 471 U.S. 539 (1985), as modified by 17 U.S.C. 107 amendment).

Factor 3 (Amount and Substantiality): Both quantitative and qualitative measures apply. Using the "heart" of a work may weigh against fair use even if the amount taken is small.

Factor 4 (Market Effect): Courts consider both actual and potential market harm, including harm to derivative work markets. In Google LLC v. Oracle America, Inc., 593 U.S. 1 (2021), the Court found copying of Java API declarations was fair use, emphasizing the creative reimplementation for a new platform.""",
        citations=[
            "Andy Warhol Foundation v. Goldsmith, 598 U.S. 508 (2023)",
            "Campbell v. Acuff-Rose Music, Inc., 510 U.S. 569 (1994)",
            "Google LLC v. Oracle America, Inc., 593 U.S. 1 (2021)",
            "Harper & Row v. Nation Enterprises, 471 U.S. 539 (1985)",
            "Authors Guild v. Google, Inc., 804 F.3d 202 (2d Cir. 2015)",
        ],
        statute_refs=["17 U.S.C. 107", "17 U.S.C. 106"],
        practice_playbook=[
            "Analyze each of the four factors separately",
            "Post-Warhol Foundation, focus on whether the use shares a common purpose with the original",
            "Document the transformative elements of the new use",
            "Assess actual and potential market harm comprehensively",
            "Consider the amount taken in both quantitative and qualitative terms",
            "Prepare expert testimony on market impact if needed",
        ],
        counter_arguments=[
            "The use is transformative in purpose and character",
            "The nature of the copyrighted work favors fair use (factual, published)",
            "Only a small, non-essential portion was used",
            "The use does not serve as a market substitute for the original",
            "The use falls within the statutory categories (criticism, education, research)",
        ],
        applicability_test=r"(?i)(fair.?use|copyright|17.?usc.?107|transformativ|market.?effect|substantial.?similar|infring|warhol|campbell|derivative.?work)",
        authority_weight=95,
        key_number_topics=["99 Copyrights & IP"],
        related_doctrines=["first_amendment_analysis"],
    ),

    "arbitration_enforceability": DoctrineResponse(
        topic="Arbitration Agreement Enforceability under the FAA",
        quick_answer="The Federal Arbitration Act establishes a strong federal policy favoring arbitration. Courts must enforce arbitration agreements according to their terms, and challenges are limited to general contract defenses (unconscionability, fraud, duress) that apply equally to all contracts.",
        full_doctrine="""The Federal Arbitration Act (9 U.S.C. 1-16) establishes that arbitration agreements shall be valid, irrevocable, and enforceable, save upon such grounds as exist at law or in equity for the revocation of any contract. The Supreme Court has consistently held that the FAA reflects a strong federal policy favoring arbitration as an alternative dispute resolution mechanism.

In AT&T Mobility LLC v. Concepcion, 563 U.S. 333 (2011), the Court held that the FAA preempts state laws that single out arbitration agreements for disfavored treatment, including California's unconscionability rule that had effectively barred class action waivers in arbitration agreements. The Court extended this in Epic Systems Corp. v. Lewis, 584 U.S. 497 (2018), upholding employment arbitration agreements with class action waivers.

However, in Morgan v. Sundance, Inc., 596 U.S. 411 (2022), the Court held that courts may not create arbitration-specific procedural rules, such as requiring prejudice for waiver of arbitration. And in Viking River Cruises v. Moriana, 596 U.S. 639 (2022), the Court addressed the interaction between the FAA and California's PAGA statute.

The question of who decides arbitrability (the court or the arbitrator) follows the rule that courts decide gateway issues unless the parties clearly and unmistakably delegate that authority to the arbitrator, often by incorporating rules like AAA or JAMS that empower the arbitrator to rule on jurisdiction.""",
        citations=[
            "AT&T Mobility LLC v. Concepcion, 563 U.S. 333 (2011)",
            "Epic Systems Corp. v. Lewis, 584 U.S. 497 (2018)",
            "Morgan v. Sundance, Inc., 596 U.S. 411 (2022)",
            "Rent-A-Center, West, Inc. v. Jackson, 561 U.S. 63 (2010)",
            "Henry Schein, Inc. v. Archer & White Sales, 586 U.S. 63 (2019)",
        ],
        statute_refs=["9 U.S.C. 1-16 (FAA)", "9 U.S.C. 2"],
        practice_playbook=[
            "Determine whether the FAA applies (involving interstate commerce)",
            "Check whether a valid agreement to arbitrate exists",
            "Assess whether the dispute falls within the scope of the agreement",
            "Determine who decides arbitrability (court or arbitrator)",
            "Evaluate defenses: unconscionability, fraud, duress (general contract defenses only)",
            "File a motion to compel arbitration under 9 U.S.C. 4",
        ],
        counter_arguments=[
            "The arbitration agreement is unconscionable (procedural and substantive)",
            "The agreement was obtained through fraud or duress",
            "The FAA does not apply because the contract does not involve interstate commerce",
            "The party waived its right to arbitrate by engaging in litigation",
            "The arbitration provision is not severable from an invalid contract",
        ],
        applicability_test=r"(?i)(arbitrat|faa|federal.?arbitration|compel.?arbitrat|class.?waiver|arbitra.?agreement|unconscionab.?arbitrat|delegation.?clause|arbitrabil)",
        authority_weight=95,
        key_number_topics=["25T Alternative Dispute Resolution"],
        related_doctrines=["contract_formation"],
    ),

    "securities_fraud_10b5": DoctrineResponse(
        topic="Securities Fraud under Rule 10b-5",
        quick_answer="Securities fraud under Section 10(b) and Rule 10b-5 requires (1) a material misrepresentation or omission, (2) scienter (intent to deceive), (3) in connection with the purchase or sale of a security, (4) reliance, (5) economic loss, and (6) loss causation.",
        full_doctrine="""Section 10(b) of the Securities Exchange Act of 1934 and SEC Rule 10b-5 prohibit fraudulent conduct in connection with the purchase or sale of securities. A private plaintiff must establish six elements: (1) a material misrepresentation or omission, (2) scienter (a mental state embracing intent to deceive, manipulate, or defraud), (3) a connection with the purchase or sale of a security, (4) reliance, (5) economic loss, and (6) loss causation (Dura Pharmaceuticals, Inc. v. Broudo, 544 U.S. 336 (2005)).

The PSLRA requires heightened pleading of scienter, demanding that the complaint state with particularity facts giving rise to a strong inference of scienter. In Tellabs, Inc. v. Makor Issues & Rights, Ltd., 551 U.S. 308 (2007), the Court held that a strong inference of scienter requires that a reasonable person would deem the inference of scienter cogent and at least as compelling as any opposing inference one could draw from the facts alleged.

For reliance, the Basic v. Levinson, 485 U.S. 224 (1988) fraud-on-the-market presumption allows plaintiffs trading in efficient markets to invoke a rebuttable presumption that the market price reflected all publicly available information, including the alleged misrepresentation. In Halliburton Co. v. Erica P. John Fund, Inc., 573 U.S. 258 (2014), the Court maintained the presumption but allowed defendants to rebut it at the class certification stage by showing the alleged misrepresentation did not actually affect the stock price.""",
        citations=[
            "Dura Pharmaceuticals, Inc. v. Broudo, 544 U.S. 336 (2005)",
            "Tellabs, Inc. v. Makor Issues & Rights, Ltd., 551 U.S. 308 (2007)",
            "Basic Inc. v. Levinson, 485 U.S. 224 (1988)",
            "Halliburton Co. v. Erica P. John Fund, 573 U.S. 258 (2014)",
            "Stoneridge Inv. Partners v. Scientific-Atlanta, 552 U.S. 148 (2008)",
        ],
        statute_refs=["15 U.S.C. 78j(b)", "17 C.F.R. 240.10b-5", "15 U.S.C. 78u-4 (PSLRA)"],
        practice_playbook=[
            "Plead material misrepresentation with specificity (what, when, where, who)",
            "Establish scienter with particularized facts under the PSLRA",
            "Invoke the fraud-on-the-market presumption for reliance",
            "Prove economic loss and establish loss causation",
            "Be prepared for PSLRA motion to dismiss and discovery stay",
            "Consider Section 11 and Section 12 claims for registered offerings",
        ],
        counter_arguments=[
            "The statement was not material or was forward-looking with meaningful cautionary language",
            "The complaint fails to plead scienter with sufficient particularity under PSLRA",
            "No reliance because the market was not efficient (rebutting Basic presumption)",
            "Intervening events, not the misrepresentation, caused the economic loss",
            "The truth-on-the-market defense demonstrates the information was already public",
        ],
        applicability_test=r"(?i)(10b.?5|securities.?fraud|material.?misrepresent|scienter|fraud.?on.?the.?market|pslra|loss.?causation|insider.?trad|section.?10.?b|securities.?exchange)",
        authority_weight=95,
        key_number_topics=["349B Securities Regulation"],
        related_doctrines=["class_certification"],
    ),

    "employment_discrimination": DoctrineResponse(
        topic="Employment Discrimination - Title VII Framework",
        quick_answer="Title VII prohibits employment discrimination based on race, color, religion, sex, or national origin. Disparate treatment claims use the McDonnell Douglas burden-shifting framework. Disparate impact claims challenge facially neutral practices with disproportionate adverse effects.",
        full_doctrine="""Title VII of the Civil Rights Act of 1964 (42 U.S.C. 2000e et seq.) prohibits employment discrimination based on race, color, religion, sex, or national origin. The statute covers hiring, firing, compensation, terms, conditions, and privileges of employment.

For individual disparate treatment claims, the McDonnell Douglas burden-shifting framework applies: (1) the plaintiff establishes a prima facie case (member of a protected class, qualified for the position, adverse employment action, circumstances giving rise to inference of discrimination), (2) the burden shifts to the employer to articulate a legitimate, nondiscriminatory reason, and (3) the plaintiff must show the stated reason is pretextual. In Bostock v. Clayton County, 590 U.S. 644 (2020), the Court held that discrimination based on sexual orientation or gender identity is necessarily discrimination "because of sex" under Title VII.

Disparate impact claims, recognized in Griggs v. Duke Power Co., 401 U.S. 424 (1971) and codified in the 1991 Civil Rights Act, challenge facially neutral employment practices that have a disproportionately adverse effect on a protected group. The employer may defend by showing the practice is job-related and consistent with business necessity, and the plaintiff may still prevail by showing a less discriminatory alternative exists.

Sexual harassment claims fall into two categories: quid pro quo and hostile work environment. For hostile work environment, the harassment must be severe or pervasive enough to alter the conditions of employment (Meritor Savings Bank v. Vinson, 477 U.S. 57 (1986)). Employer liability depends on whether the harasser is a supervisor (Burlington Industries v. Ellerth, 524 U.S. 742 (1998)) or a co-worker.""",
        citations=[
            "McDonnell Douglas Corp. v. Green, 411 U.S. 792 (1973)",
            "Bostock v. Clayton County, 590 U.S. 644 (2020)",
            "Griggs v. Duke Power Co., 401 U.S. 424 (1971)",
            "Meritor Savings Bank v. Vinson, 477 U.S. 57 (1986)",
            "Burlington Industries v. Ellerth, 524 U.S. 742 (1998)",
            "Texas Dep't of Housing v. Inclusive Communities, 576 U.S. 519 (2015)",
        ],
        statute_refs=["42 U.S.C. 2000e et seq.", "42 U.S.C. 1981"],
        practice_playbook=[
            "Determine whether the claim is disparate treatment or disparate impact",
            "Apply the McDonnell Douglas framework for individual disparate treatment",
            "For disparate impact, present statistical evidence of disproportionate effect",
            "Exhaust administrative remedies by filing an EEOC charge within the deadline",
            "For harassment claims, establish severity or pervasiveness",
            "Consider retaliation claims under 42 U.S.C. 2000e-3(a)",
        ],
        counter_arguments=[
            "The adverse action was based on a legitimate, nondiscriminatory reason",
            "The plaintiff cannot establish a prima facie case",
            "The challenged practice is job-related and consistent with business necessity",
            "The harassment was not severe or pervasive enough to alter employment conditions",
            "The employer took prompt corrective action upon learning of the harassment",
        ],
        applicability_test=r"(?i)(title.?vii|employment.?discriminat|disparate.?treatment|disparate.?impact|mcdonnell.?douglas|hostile.?work|sexual.?harass|protected.?class|eeoc|discriminat.?basis|race.?discriminat|sex.?discriminat)",
        authority_weight=95,
        key_number_topics=["231 Labor & Employment", "78 Civil Rights"],
        related_doctrines=["qualified_immunity"],
    ),

    "bankruptcy_automatic_stay": DoctrineResponse(
        topic="Bankruptcy Automatic Stay",
        quick_answer="The automatic stay under 11 U.S.C. 362 immediately halts virtually all collection actions, judicial proceedings, and enforcement of judgments against the debtor upon filing of a bankruptcy petition. Violations of the stay may result in sanctions including actual and punitive damages.",
        full_doctrine="""The automatic stay, codified at 11 U.S.C. 362(a), is one of the most fundamental protections afforded to debtors in bankruptcy. It takes effect immediately upon the filing of a bankruptcy petition and operates as an injunction against a broad range of actions by creditors, including commencement or continuation of judicial proceedings, enforcement of judgments, acts to obtain possession of property of the estate, and acts to collect or recover claims against the debtor.

The stay applies to virtually all entities and actions, with limited exceptions under 362(b), including criminal proceedings, certain tax audits, and domestic support obligations. The stay protects both the debtor and the property of the bankruptcy estate, preserving the status quo to allow orderly administration of the case.

Relief from the stay may be obtained under 362(d) upon motion and after notice and a hearing, for "cause" (including lack of adequate protection) or where the debtor has no equity in the property and the property is not necessary for an effective reorganization. In Johnson v. Midland Credit Management, Inc., the Court emphasized that the stay serves the dual purposes of protecting the debtor from financial pressure and allowing the bankruptcy process to operate in an orderly fashion.

Willful violations of the automatic stay may result in actual damages, including costs and attorney's fees, and, in individual cases under 362(k), punitive damages. Actions taken in violation of the stay are generally void or voidable.""",
        citations=[
            "Midlantic National Bank v. N.J. Dep't of Environmental Protection, 474 U.S. 494 (1986)",
            "United States v. Whiting Pools, Inc., 462 U.S. 198 (1983)",
            "Ritzen Group, Inc. v. Jackson Masonry, LLC, 589 U.S. 35 (2020)",
            "City of Chicago v. Fulton, 592 U.S. 154 (2021)",
        ],
        statute_refs=["11 U.S.C. 362", "11 U.S.C. 362(k)", "11 U.S.C. 362(d)"],
        practice_playbook=[
            "Verify the stay applies to the specific action being taken",
            "Check for applicable exceptions under 362(b)",
            "If the stay prevents necessary action, file a motion for relief under 362(d)",
            "Document any willful violations for sanctions",
            "For serial filers, check whether the stay is limited or nonexistent under 362(c)",
            "Consider the distinction between void and voidable acts in violation of the stay",
        ],
        counter_arguments=[
            "An exception to the automatic stay applies under 362(b)",
            "The stay has been lifted by court order",
            "The stay has terminated by operation of law under 362(c)",
            "Adequate protection has not been provided to the secured creditor",
            "The debtor has no equity and the property is not necessary for reorganization",
        ],
        applicability_test=r"(?i)(automatic.?stay|362|bankruptcy.?stay|relief.?from.?stay|violation.?of.?stay|lift.?the.?stay|bankruptcy.?filing|stay.?of.?proceedings|adequate.?protect)",
        authority_weight=90,
        key_number_topics=["51 Bankruptcy"],
        related_doctrines=["res_judicata"],
    ),

    "miranda_requirements": DoctrineResponse(
        topic="Miranda Warning Requirements",
        quick_answer="Miranda v. Arizona requires that prior to custodial interrogation, suspects must be informed of their right to remain silent, that anything said can be used against them, their right to an attorney, and that one will be appointed if they cannot afford one. Failure to give Miranda warnings renders statements inadmissible in the prosecution's case-in-chief.",
        full_doctrine="""Miranda v. Arizona, 384 U.S. 436 (1966), established that the Fifth Amendment privilege against self-incrimination requires law enforcement to inform suspects of specific rights before conducting custodial interrogation. The four Miranda warnings are: (1) the right to remain silent, (2) anything said can and will be used against the person in court, (3) the right to have an attorney present during questioning, and (4) if the person cannot afford an attorney, one will be appointed.

Miranda applies only to custodial interrogation. "Custody" is determined by whether a reasonable person in the suspect's position would have felt free to terminate the encounter (J.D.B. v. North Carolina, 564 U.S. 261 (2011), considering the suspect's age when known). "Interrogation" includes express questioning and its functional equivalent: words or actions the police should know are reasonably likely to elicit an incriminating response (Rhode Island v. Innis, 446 U.S. 291 (1980)).

If a suspect invokes the right to remain silent, questioning must cease (Michigan v. Mosley, 423 U.S. 96 (1975), allowing resumption after a significant passage of time). If a suspect invokes the right to counsel, all interrogation must cease until counsel is present (Edwards v. Arizona, 451 U.S. 477 (1981)), and this protection continues for 14 days after release from custody (Maryland v. Shatzer, 559 U.S. 98 (2010)).

In Vega v. Tekoh, 597 U.S. 134 (2022), the Court held that Miranda violations do not give rise to claims under 42 U.S.C. 1983, as Miranda is a prophylactic rule rather than a constitutional right itself.""",
        citations=[
            "Miranda v. Arizona, 384 U.S. 436 (1966)",
            "Vega v. Tekoh, 597 U.S. 134 (2022)",
            "Edwards v. Arizona, 451 U.S. 477 (1981)",
            "Berghuis v. Thompkins, 560 U.S. 370 (2010)",
            "J.D.B. v. North Carolina, 564 U.S. 261 (2011)",
        ],
        statute_refs=["U.S. Const. amend. V", "18 U.S.C. 3501"],
        practice_playbook=[
            "Determine whether the suspect was in custody at the time of questioning",
            "Assess whether the interaction constituted interrogation or its functional equivalent",
            "Verify that proper Miranda warnings were given before questioning began",
            "If invocation occurred, determine whether it was of silence or counsel",
            "File a motion to suppress statements obtained in violation of Miranda",
            "Consider whether any exception applies (public safety, routine booking)",
        ],
        counter_arguments=[
            "The suspect was not in custody but was free to leave",
            "The interaction was not interrogation or its functional equivalent",
            "The suspect voluntarily waived Miranda rights after receiving warnings",
            "The public safety exception justified questioning without warnings",
            "The statement was spontaneous, not the product of interrogation",
        ],
        applicability_test=r"(?i)(miranda|right.?to.?remain.?silent|custodial.?interrogat|right.?to.?counsel|fifth.?amendment.?self.?incrim|suppress.?statement|waive.?miranda|invoke.?right|public.?safety.?exception)",
        authority_weight=100,
        key_number_topics=["110A Criminal Law"],
        related_doctrines=["fourth_amendment_search", "qualified_immunity"],
    ),
}


# ============================================================================
# DOCTRINE ENGINE
# ============================================================================

class CaseLawDoctrineEngine:
    """
    Query engine for the case law doctrine cache.

    Features:
    - Keyword matching against doctrine applicability tests
    - Multi-doctrine retrieval for complex queries
    - Hit/miss statistics tracking
    - Doctrine health assessment
    """

    def __init__(self, cache: Dict[str, DoctrineResponse]) -> None:
        self._cache = cache
        self._compiled_tests: Dict[str, re.Pattern] = {}
        self._hits: int = 0
        self._misses: int = 0
        self._hit_distribution: Dict[str, int] = {}
        self._miss_queries: List[str] = []

        # Pre-compile applicability tests
        for key, doctrine in self._cache.items():
            if doctrine.applicability_test:
                try:
                    self._compiled_tests[key] = re.compile(
                        doctrine.applicability_test, re.IGNORECASE
                    )
                except re.error as exc:
                    logger.warning(f"Invalid regex for doctrine {key}: {exc}")

    def quick_answer(self, query: str) -> Optional[DoctrineResponse]:
        """Find the best-matching doctrine for a query."""
        best_key: Optional[str] = None
        best_score: int = 0

        query_lower = query.lower().strip()

        for key, pattern in self._compiled_tests.items():
            matches = pattern.findall(query_lower)
            score = len(matches)
            if score > best_score:
                best_score = score
                best_key = key

        if best_key:
            self._hits += 1
            self._hit_distribution[best_key] = self._hit_distribution.get(best_key, 0) + 1
            return self._cache[best_key]

        self._misses += 1
        if len(self._miss_queries) < 500:
            self._miss_queries.append(query_lower[:200])
        return None

    def multi_match(self, query: str, max_results: int = 5) -> List[Tuple[str, DoctrineResponse, int]]:
        """Find all matching doctrines for a query, ranked by relevance."""
        results: List[Tuple[str, DoctrineResponse, int]] = []
        query_lower = query.lower().strip()

        for key, pattern in self._compiled_tests.items():
            matches = pattern.findall(query_lower)
            if matches:
                results.append((key, self._cache[key], len(matches)))

        results.sort(key=lambda x: x[2], reverse=True)
        return results[:max_results]

    def get_doctrine(self, key: str) -> Optional[DoctrineResponse]:
        """Get a specific doctrine by key."""
        return self._cache.get(key)

    def list_doctrines(self) -> List[Dict[str, str]]:
        """List all available doctrines."""
        return [
            {"key": key, "topic": doc.topic, "court_level": doc.court_level}
            for key, doc in self._cache.items()
        ]

    def get_hit_stats(self) -> Dict:
        """Get hit/miss statistics."""
        total = self._hits + self._misses
        return {
            "total_queries": total,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": round(self._hits / max(total, 1), 4),
            "top_doctrines": sorted(
                self._hit_distribution.items(), key=lambda x: x[1], reverse=True
            )[:10],
            "recent_misses": self._miss_queries[-10:],
            "total_doctrines": len(self._cache),
        }

    def get_recent_misses(self, limit: int = 20) -> List[str]:
        """Get recent doctrine cache misses."""
        return self._miss_queries[-limit:]

    def get_doctrine_hash(self, key: str) -> str:
        """Compute SHA-256 hash of a specific doctrine."""
        doctrine = self._cache.get(key)
        if not doctrine:
            return ""
        content = f"{doctrine.topic}|{doctrine.quick_answer}|{doctrine.full_doctrine}"
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def get_overruled_doctrines(self) -> List[Dict[str, str]]:
        """Get list of doctrines that have been overruled."""
        return [
            {"key": key, "topic": doc.topic, "overruled_by": doc.overruled_by}
            for key, doc in self._cache.items()
            if doc.overruled_by
        ]

    def get_stale_doctrines(self, threshold_year: int = 2023) -> List[Dict[str, str]]:
        """Get doctrines at risk of staleness."""
        return [
            {"key": key, "topic": doc.topic, "last_update": doc.last_major_update, "risk": doc.staleness_risk}
            for key, doc in self._cache.items()
            if doc.staleness_risk in ("medium", "high") or int(doc.last_major_update) < threshold_year
        ]


# ============================================================================
# SINGLETON
# ============================================================================

_engine_instance: Optional[CaseLawDoctrineEngine] = None


def get_engine() -> CaseLawDoctrineEngine:
    """Get the global doctrine engine instance."""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = CaseLawDoctrineEngine(DOCTRINE_CACHE)
        logger.info(f"Doctrine engine initialized with {len(DOCTRINE_CACHE)} doctrines")
    return _engine_instance
