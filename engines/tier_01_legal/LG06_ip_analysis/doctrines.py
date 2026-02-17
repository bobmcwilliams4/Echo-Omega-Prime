"""
LG06 IP Analysis Engine - Doctrines Module
=============================================
Pre-compiled IP doctrine cache with structured legal knowledge
for patent law, trademark law, copyright law, trade secrets,
IP licensing, and international IP frameworks.

Each doctrine block contains:
    - topic: Canonical topic identifier
    - title: Human-readable title
    - category: IP category (patent, trademark, copyright, trade_secret, etc.)
    - content: Substantive legal analysis
    - authority: Governing statute/regulation/case
    - confidence: Base confidence score (0.0-1.0)
    - citations: Key legal citations
    - last_updated: Date of last content review
    - tags: Searchable tags

Version: 2.0.0
Engine: LG06 IP Analysis
"""

from __future__ import annotations

import hashlib
import json
import time
from collections import defaultdict
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Optional, Set, Tuple

from loguru import logger


# ============================================================================
# DOCTRINE RESPONSE
# ============================================================================

@dataclass
class DoctrineResponse:
    """A structured response from the doctrine cache."""
    topic: str
    title: str
    category: str
    content: str
    authority: str
    confidence: float
    confidence_band: str
    citations: List[str]
    tags: List[str]
    last_updated: str
    determinism_hash: str
    layer: str = "doctrine_cache"
    response_time_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "topic": self.topic,
            "title": self.title,
            "category": self.category,
            "content": self.content,
            "authority": self.authority,
            "confidence": round(self.confidence, 4),
            "confidence_band": self.confidence_band,
            "citations": self.citations,
            "tags": self.tags,
            "last_updated": self.last_updated,
            "determinism_hash": self.determinism_hash,
            "layer": self.layer,
            "response_time_ms": round(self.response_time_ms, 3),
        }


# ============================================================================
# DOCTRINE CACHE - PATENT LAW (35 USC)
# ============================================================================

PATENT_DOCTRINES: List[Dict[str, Any]] = [
    {
        "topic": "patentable_subject_matter_101",
        "title": "Patentable Subject Matter - 35 USC 101",
        "category": "patent",
        "content": (
            "Under 35 USC 101, patentable subject matter includes any new and useful "
            "process, machine, manufacture, or composition of matter, or any new and useful "
            "improvement thereof. The Supreme Court has identified three judicially-created "
            "exceptions: laws of nature, natural phenomena, and abstract ideas. "
            "The Alice/Mayo two-step framework applies: (1) determine whether the claim is "
            "directed to a judicial exception, and (2) if so, determine whether the claim "
            "recites additional elements that transform the nature of the claim into a "
            "patent-eligible application of the judicial exception (an 'inventive concept'). "
            "For software and business method patents, claims directed to abstract ideas "
            "such as fundamental economic practices, methods of organizing human activities, "
            "mathematical concepts, and mental processes require a showing of 'significantly "
            "more' than the abstract idea itself. Practical application must be demonstrated "
            "through specific technological improvement, transformation of a particular "
            "article, or meaningful limitation tied to a particular machine. The 2019 Revised "
            "Patent Eligibility Guidance (PEG) provides groupings of abstract ideas and the "
            "'practical application' integration test. Under Step 2A Prong Two, a claim that "
            "integrates the judicial exception into a practical application is patent eligible "
            "regardless of whether additional elements are well-understood, routine, or conventional."
        ),
        "authority": "35 USC 101; Alice Corp. v. CLS Bank, 573 U.S. 208 (2014); Mayo v. Prometheus, 566 U.S. 66 (2012)",
        "confidence": 0.90,
        "citations": [
            "Alice Corp. v. CLS Bank International, 573 U.S. 208 (2014)",
            "Mayo Collaborative Servs. v. Prometheus Labs., 566 U.S. 66 (2012)",
            "Bilski v. Kappos, 561 U.S. 593 (2010)",
            "Diamond v. Diehr, 450 U.S. 175 (1981)",
            "Diamond v. Chakrabarty, 447 U.S. 303 (1980)",
            "Gottschalk v. Benson, 409 U.S. 63 (1972)",
            "Berkheimer v. HP Inc., 881 F.3d 1360 (Fed. Cir. 2018)",
            "Enfish, LLC v. Microsoft Corp., 822 F.3d 1327 (Fed. Cir. 2016)",
            "MPEP 2106",
        ],
        "tags": ["101", "eligibility", "alice", "mayo", "abstract_idea", "practical_application"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "novelty_102",
        "title": "Novelty - 35 USC 102",
        "category": "patent",
        "content": (
            "Under 35 USC 102 (post-AIA), a person is entitled to a patent unless the claimed "
            "invention was (a) patented, described in a printed publication, in public use, on "
            "sale, or otherwise available to the public before the effective filing date of the "
            "claimed invention, or (b) described in a patent or published application naming "
            "another inventor with an earlier effective filing date. Anticipation under 102 "
            "requires that every element of the claimed invention be disclosed, either expressly "
            "or inherently, in a single prior art reference. The standard is strict identity: "
            "the reference must describe the claimed invention sufficiently to enable one of "
            "ordinary skill in the art (PHOSITA) to practice the invention. Inherent anticipation "
            "requires that the missing element is necessarily present in the prior art, not merely "
            "possibly present. Under the AIA first-inventor-to-file system, the critical date is "
            "the effective filing date (EFD), which may include a foreign priority date under "
            "Paris Convention or a provisional filing date. The one-year grace period under "
            "102(b)(1) protects disclosures by the inventor or those who obtained subject matter "
            "from the inventor, provided they occurred within one year before the EFD. Swearing "
            "behind references is no longer available under AIA; instead, applicants may submit "
            "a statement under 37 CFR 1.130 to disqualify references under the 102(b) exceptions."
        ),
        "authority": "35 USC 102; In re Schreiber, 128 F.3d 1473 (Fed. Cir. 1997)",
        "confidence": 0.92,
        "citations": [
            "In re Schreiber, 128 F.3d 1473 (Fed. Cir. 1997)",
            "Kennametal, Inc. v. Ingersoll Cutting Tool Co., 780 F.3d 1376 (Fed. Cir. 2015)",
            "Helsinn Healthcare S.A. v. Teva Pharm., 139 S. Ct. 628 (2019)",
            "35 USC 102(a)(1), (a)(2), (b)(1), (b)(2)",
            "MPEP 2131-2138",
        ],
        "tags": ["102", "novelty", "anticipation", "prior_art", "first_to_file", "grace_period"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "non_obviousness_103",
        "title": "Non-Obviousness - 35 USC 103",
        "category": "patent",
        "content": (
            "Under 35 USC 103, a patent may not be obtained if the differences between the "
            "claimed invention and the prior art are such that the claimed invention as a whole "
            "would have been obvious to a person having ordinary skill in the art (PHOSITA) at "
            "the time the invention was made (pre-AIA) or before the effective filing date (AIA). "
            "The Graham v. John Deere framework requires: (1) determining the scope and content "
            "of the prior art, (2) ascertaining the differences between the prior art and the "
            "claims, (3) resolving the level of ordinary skill, and (4) evaluating objective "
            "indicia of non-obviousness (secondary considerations). KSR expanded the TSM test "
            "by allowing common sense, design need, market forces, and known problem-solution "
            "approaches as motivation to combine. Obviousness requires combining references where "
            "a PHOSITA would have had reason to combine with a reasonable expectation of success. "
            "Secondary considerations include commercial success, long-felt but unsolved need, "
            "failure of others, copying, unexpected results, teaching away, praise from experts, "
            "and licensing. These must have a nexus to the claimed invention. Obvious to try is "
            "not necessarily obvious if the number of options is not finite and predictable."
        ),
        "authority": "35 USC 103; Graham v. John Deere Co., 383 U.S. 1 (1966); KSR Int'l v. Teleflex, 550 U.S. 398 (2007)",
        "confidence": 0.92,
        "citations": [
            "Graham v. John Deere Co., 383 U.S. 1 (1966)",
            "KSR Int'l Co. v. Teleflex Inc., 550 U.S. 398 (2007)",
            "In re Wands, 858 F.2d 731 (Fed. Cir. 1988)",
            "MPEP 2141-2145",
        ],
        "tags": ["103", "obviousness", "graham", "ksr", "phosita", "secondary_considerations"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "written_description_enablement_112",
        "title": "Written Description and Enablement - 35 USC 112",
        "category": "patent",
        "content": (
            "35 USC 112(a) requires three distinct requirements: (1) Written Description - the "
            "specification must demonstrate that the inventor had possession of the claimed "
            "invention at the time of filing, (2) Enablement - the specification must teach a "
            "PHOSITA how to make and use the invention without undue experimentation, evaluated "
            "under the Wands factors (breadth of claims, nature of invention, state of art, skill "
            "level, predictability, amount of direction, examples, and required experimentation), "
            "and (3) Best Mode - the inventor must disclose the best mode known for practicing "
            "the invention (though failure to disclose best mode is no longer a basis for "
            "invalidity under AIA). 35 USC 112(b) requires that claims particularly point out "
            "and distinctly claim the subject matter of the invention (definiteness). Under "
            "Nautilus v. Biosig, a claim is indefinite if it fails to inform, with reasonable "
            "certainty, those skilled in the art about the scope of the invention. 35 USC 112(f) "
            "covers means-plus-function claim elements, which are construed to cover the "
            "corresponding structure, material, or acts described in the specification and "
            "equivalents thereof. If no corresponding structure is disclosed, the claim is "
            "indefinite under 112(b)."
        ),
        "authority": "35 USC 112; Nautilus v. Biosig, 572 U.S. 898 (2014); In re Wands, 858 F.2d 731 (Fed. Cir. 1988)",
        "confidence": 0.91,
        "citations": [
            "Nautilus, Inc. v. Biosig Instruments, Inc., 572 U.S. 898 (2014)",
            "Ariad Pharm. v. Eli Lilly, 598 F.3d 1336 (Fed. Cir. 2010) (en banc)",
            "In re Wands, 858 F.2d 731 (Fed. Cir. 1988)",
            "Williamson v. Citrix Online, 792 F.3d 1339 (Fed. Cir. 2015) (en banc)",
            "MPEP 2161-2175, 2181-2186",
        ],
        "tags": ["112", "written_description", "enablement", "definiteness", "means_plus_function"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "claim_construction",
        "title": "Claim Construction - Markman Analysis",
        "category": "patent",
        "content": (
            "Claim construction is a question of law determined by the court (Markman v. Westview). "
            "Under the Phillips standard used in district court litigation, claim terms are given "
            "their ordinary and customary meaning as understood by a PHOSITA at the time of "
            "the invention, in the context of the specification and prosecution history. The "
            "intrinsic evidence hierarchy is: (1) claim language, (2) other claims, (3) specification, "
            "(4) prosecution history. Extrinsic evidence (dictionaries, expert testimony, treatises) "
            "may inform but cannot override intrinsic evidence. The specification is the single "
            "best guide to claim meaning. However, courts should not import limitations from "
            "the specification into the claims. A patentee may act as their own lexicographer "
            "by clearly defining terms in the specification. Prosecution history estoppel limits "
            "the scope of claims based on narrowing amendments and arguments made during "
            "prosecution. The PTAB uses the broadest reasonable interpretation (BRI) standard "
            "for IPR/PGR proceedings (now modified for AIA trials after Phillips claim "
            "construction rule change effective Nov. 13, 2018, applying Phillips in IPR/PGR)."
        ),
        "authority": "Markman v. Westview Instruments, 517 U.S. 370 (1996); Phillips v. AWH Corp., 415 F.3d 1303 (Fed. Cir. 2005) (en banc)",
        "confidence": 0.93,
        "citations": [
            "Markman v. Westview Instruments, Inc., 517 U.S. 370 (1996)",
            "Phillips v. AWH Corp., 415 F.3d 1303 (Fed. Cir. 2005) (en banc)",
            "Vitronics Corp. v. Conceptronic, Inc., 90 F.3d 1576 (Fed. Cir. 1996)",
            "Teva Pharm. v. Sandoz, 574 U.S. 318 (2015)",
        ],
        "tags": ["claim_construction", "markman", "phillips", "bri", "prosecution_history"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "patent_infringement_271",
        "title": "Patent Infringement - 35 USC 271",
        "category": "patent",
        "content": (
            "Direct infringement under 35 USC 271(a) occurs when a party makes, uses, offers "
            "to sell, sells, or imports the patented invention within the US without authority. "
            "Literal infringement requires that the accused product or process meets every "
            "limitation of at least one claim. Under the doctrine of equivalents, infringement "
            "occurs when an element performs substantially the same function, in substantially "
            "the same way, to achieve substantially the same result (function-way-result test) "
            "or when the differences between the claim element and the accused element are "
            "insubstantial (insubstantial differences test). Induced infringement under 271(b) "
            "requires that the accused party knowingly induced another to infringe, with "
            "knowledge of the patent and knowledge that the induced acts constitute infringement "
            "(Global-Tech/Commil). Contributory infringement under 271(c) applies to selling a "
            "component of a patented combination that has no substantial non-infringing use, "
            "with knowledge that the component is especially made for infringement. Willful "
            "infringement under Halo v. Pulse requires subjective recklessness, not merely "
            "objective recklessness. Enhanced damages (up to 3x) may be awarded for willful "
            "infringement at the court's discretion."
        ),
        "authority": "35 USC 271; Halo Elecs. v. Pulse Elecs., 579 U.S. 93 (2016)",
        "confidence": 0.92,
        "citations": [
            "35 USC 271(a), (b), (c), (f)",
            "Halo Electronics v. Pulse Electronics, 579 U.S. 93 (2016)",
            "Global-Tech v. SEB S.A., 563 U.S. 754 (2011)",
            "Commil USA v. Cisco Systems, 575 U.S. 632 (2015)",
            "Warner-Jenkinson v. Hilton Davis, 520 U.S. 17 (1997)",
            "Akamai Techs. v. Limelight Networks, 797 F.3d 1020 (Fed. Cir. 2015) (en banc)",
        ],
        "tags": ["infringement", "271", "literal", "equivalents", "induced", "contributory", "willful"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "patent_damages",
        "title": "Patent Damages - Lost Profits and Reasonable Royalty",
        "category": "patent",
        "content": (
            "Patent damages under 35 USC 284 must be adequate to compensate for infringement "
            "but in no event less than a reasonable royalty. Lost profits under Panduit require: "
            "(1) demand for the patented product, (2) absence of acceptable non-infringing "
            "substitutes, (3) manufacturing and marketing capability, and (4) the amount of "
            "profit that would have been made. The entire market value rule allows lost profits "
            "on the entire product only if the patented feature drives demand for the entire "
            "product. Reasonable royalty is determined using the Georgia-Pacific 15-factor test, "
            "including: established royalty rates, comparable licenses, nature and scope of the "
            "license, licensor's licensing policy, commercial relationship, effect of the "
            "patented invention in promoting sales of other products, duration of the patent "
            "and license, profitability, utility and advantages over old modes, the nature of "
            "the invention, extent of accused infringer's use, customary profit margin, "
            "contribution of the invention, expert testimony, and the hypothetical negotiation "
            "rate. Apportionment may be required to isolate the value attributable to the "
            "patented feature. Enhanced damages (up to treble) for willful infringement. "
            "Attorney fees may be awarded in exceptional cases under 35 USC 285 (Octane Fitness)."
        ),
        "authority": "35 USC 284-285; Georgia-Pacific Corp. v. U.S. Plywood Corp., 318 F. Supp. 1116 (S.D.N.Y. 1970)",
        "confidence": 0.89,
        "citations": [
            "Georgia-Pacific Corp. v. U.S. Plywood Corp., 318 F. Supp. 1116 (S.D.N.Y. 1970)",
            "Panduit Corp. v. Stahlin Bros., 575 F.2d 1152 (6th Cir. 1978)",
            "Rite-Hite Corp. v. Kelley, Inc., 56 F.3d 1538 (Fed. Cir. 1995) (en banc)",
            "Octane Fitness v. ICON Health, 572 U.S. 545 (2014)",
        ],
        "tags": ["damages", "lost_profits", "reasonable_royalty", "georgia_pacific", "apportionment"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "inter_partes_review",
        "title": "Inter Partes Review (IPR) - PTAB Proceedings",
        "category": "patent",
        "content": (
            "Inter partes review (IPR) under 35 USC 311-319 allows any person who is not the "
            "patent owner to challenge the validity of a patent at the PTAB on grounds of "
            "anticipation (102) or obviousness (103) based only on prior art consisting of "
            "patents and printed publications. A petition must be filed within one year of "
            "being served with an infringement complaint. The PTAB must determine within "
            "6 months whether there is a reasonable likelihood the petitioner would prevail "
            "on at least one challenged claim (institution standard). Once instituted, the PTAB "
            "must issue a final written decision within 12 months (extendable by 6 months for "
            "good cause). Claim construction uses the Phillips standard (changed from BRI "
            "effective November 13, 2018). The burden of proof is preponderance of evidence "
            "(lower than the clear and convincing standard in district court). Estoppel applies "
            "under 315(e): the petitioner may not assert in a subsequent proceeding any ground "
            "that the petitioner raised or reasonably could have raised during the IPR. "
            "SAS Institute v. Iancu requires the Board to address all claims challenged if "
            "IPR is instituted. Fintiv factors apply when parallel district court litigation "
            "exists (NHK-Fintiv discretionary denial framework)."
        ),
        "authority": "35 USC 311-319; SAS Inst. v. Iancu, 138 S. Ct. 1348 (2018)",
        "confidence": 0.91,
        "citations": [
            "35 USC 311-319",
            "SAS Institute Inc. v. Iancu, 138 S. Ct. 1348 (2018)",
            "Oil States Energy v. Greene's Energy, 138 S. Ct. 1365 (2018)",
            "Apple Inc. v. Fintiv, Inc., IPR2020-00019 (PTAB 2020)",
        ],
        "tags": ["ipr", "ptab", "inter_partes_review", "invalidity", "institution", "fintiv"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "design_patent_law",
        "title": "Design Patent Law - 35 USC 171",
        "category": "patent",
        "content": (
            "Design patents under 35 USC 171 protect new, original, and ornamental designs for "
            "articles of manufacture. The design must be primarily ornamental, not functional. "
            "The term is 15 years from grant date (for applications filed after May 13, 2015). "
            "Design patent claims consist of drawings showing the ornamental design, with solid "
            "lines showing the claimed design and broken lines showing unclaimed environment. "
            "Infringement is assessed under the 'ordinary observer' test from Egyptian Goddess: "
            "would an ordinary observer, familiar with the prior art designs, be deceived into "
            "thinking the accused design is the same as the patented design? Functional aspects "
            "are factored out. For damages, the total profit of the article of manufacture may "
            "be awarded under 35 USC 289, but the 'article of manufacture' may be a component "
            "of a multi-component product (Samsung v. Apple, 137 S. Ct. 429 (2016)). Design "
            "patent prosecution is generally faster than utility, averaging 18 months. The Hague "
            "Agreement allows international design registration in member countries."
        ),
        "authority": "35 USC 171, 289; Egyptian Goddess v. Swisa, 543 F.3d 665 (Fed. Cir. 2008) (en banc)",
        "confidence": 0.88,
        "citations": [
            "Egyptian Goddess v. Swisa, 543 F.3d 665 (Fed. Cir. 2008) (en banc)",
            "Samsung v. Apple, 137 S. Ct. 429 (2016)",
            "35 USC 171, 173, 289",
        ],
        "tags": ["design_patent", "ornamental", "ordinary_observer", "article_of_manufacture"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "patent_prosecution_strategy",
        "title": "Patent Prosecution Strategy",
        "category": "patent",
        "content": (
            "Effective patent prosecution requires strategic claim drafting, prior art analysis, "
            "and prosecution history management. Key strategies include: (1) Draft broad "
            "independent claims with narrower dependent claims as fallback positions. "
            "(2) Include multiple independent claims in different categories (method, apparatus, "
            "system, CRM) for broader coverage. (3) Use continuation strategy to maintain "
            "pending claims while pursuing different claim scope. (4) Provisional applications "
            "secure an early filing date with a 12-month window to file non-provisional. "
            "(5) Avoid prosecution history estoppel by minimizing narrowing amendments - prefer "
            "arguments over amendments when possible. (6) Consider restriction requirements "
            "carefully - elect the commercially most valuable invention and use divisionals "
            "for the rest. (7) For software/AI inventions, emphasize technical improvement and "
            "practical application in the specification to overcome 101 rejections. (8) Monitor "
            "the file wrapper for inadvertent admissions. (9) Consider PCT filing for "
            "international coverage (12-month priority, 30/31-month national phase). "
            "(10) Track continuation/divisional chains to maintain family coherence."
        ),
        "authority": "MPEP 600-800; 37 CFR 1.53, 1.78",
        "confidence": 0.87,
        "citations": [
            "MPEP 608, 714, 802, 1490",
            "37 CFR 1.53, 1.56, 1.78, 1.130",
        ],
        "tags": ["prosecution", "claim_drafting", "continuation", "provisional", "strategy"],
        "last_updated": "2026-02-10",
    },
]


# ============================================================================
# DOCTRINE CACHE - TRADEMARK LAW (Lanham Act)
# ============================================================================

TRADEMARK_DOCTRINES: List[Dict[str, Any]] = [
    {
        "topic": "trademark_distinctiveness",
        "title": "Trademark Distinctiveness Spectrum",
        "category": "trademark",
        "content": (
            "The distinctiveness spectrum, established in Abercrombie & Fitch v. Hunting World, "
            "classifies marks from strongest to weakest: (1) Fanciful - coined words with no "
            "prior meaning (Kodak, Xerox, Exxon), entitled to broadest protection. "
            "(2) Arbitrary - existing words used in unrelated context (Apple for computers, "
            "Amazon for e-commerce), strong protection. (3) Suggestive - suggest a quality or "
            "characteristic requiring imagination to connect to the goods (Coppertone, Netflix), "
            "protectable without secondary meaning. (4) Descriptive - directly describe a feature, "
            "quality, or characteristic of the goods (Sharp for TVs, Best Buy), protectable only "
            "with acquired distinctiveness (secondary meaning). (5) Generic - common name for "
            "the goods/services (computer, aspirin), never protectable. Secondary meaning is "
            "established when the primary significance of the mark to the consuming public is "
            "the producer, not the product. Evidence includes: advertising expenditures, sales "
            "volume, length and exclusivity of use, consumer surveys, unsolicited media coverage, "
            "attempts to copy the mark. The Supplemental Register accepts descriptive marks that "
            "may acquire distinctiveness over time."
        ),
        "authority": "Abercrombie & Fitch Co. v. Hunting World, Inc., 537 F.2d 4 (2d Cir. 1976)",
        "confidence": 0.93,
        "citations": [
            "Abercrombie & Fitch Co. v. Hunting World, 537 F.2d 4 (2d Cir. 1976)",
            "Two Pesos v. Taco Cabana, 505 U.S. 763 (1992)",
            "Wal-Mart v. Samara Bros., 529 U.S. 205 (2000)",
            "Qualitex Co. v. Jacobson Prods., 514 U.S. 159 (1995)",
            "TMEP 1209",
        ],
        "tags": ["distinctiveness", "fanciful", "arbitrary", "suggestive", "descriptive", "generic", "secondary_meaning"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "likelihood_of_confusion",
        "title": "Likelihood of Confusion Analysis",
        "category": "trademark",
        "content": (
            "Likelihood of confusion is the central test for trademark infringement under "
            "15 USC 1114 (registered marks) and 1125(a) (unregistered marks). The du Pont "
            "factors (In re E.I. du Pont de Nemours) provide the framework, considering: "
            "(1) similarity of marks in appearance, sound, and meaning, (2) similarity/nature "
            "of goods/services, (3) similarity of trade channels, (4) conditions under which "
            "sales are made (impulse vs. careful purchasing), (5) fame of the prior mark, "
            "(6) number and nature of similar marks on similar goods, (7) nature and extent of "
            "any actual confusion, (8) length of concurrent use without confusion, (9) variety "
            "of goods/services using the marks, (10) market interface between applicant and "
            "owner, (11) extent to which applicant has a right to exclude others, (12) extent of "
            "potential confusion, (13) any other established fact probative of the effect of use. "
            "Different circuits weigh factors differently. The Polaroid factors (2d Cir.) and "
            "Sleekcraft factors (9th Cir.) are alternative formulations. The TTAB applies du Pont. "
            "Consumer surveys (Eveready format for infringement, Teflon format for genericness) "
            "are the most probative evidence of actual confusion."
        ),
        "authority": "In re E.I. du Pont de Nemours & Co., 476 F.2d 1357 (CCPA 1973)",
        "confidence": 0.92,
        "citations": [
            "In re E.I. du Pont de Nemours & Co., 476 F.2d 1357 (CCPA 1973)",
            "Polaroid Corp. v. Polarad Elecs., 287 F.2d 492 (2d Cir. 1961)",
            "AMF Inc. v. Sleekcraft Boats, 599 F.2d 341 (9th Cir. 1979)",
            "15 USC 1114, 1125(a)",
        ],
        "tags": ["confusion", "du_pont", "polaroid", "sleekcraft", "similarity", "infringement"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "trademark_dilution",
        "title": "Trademark Dilution - TDRA",
        "category": "trademark",
        "content": (
            "The Trademark Dilution Revision Act (TDRA, 15 USC 1125(c)) protects famous marks "
            "against dilution by blurring and tarnishment, regardless of competition between "
            "the parties or likelihood of confusion. A mark is famous if it is widely recognized "
            "by the general consuming public as a designation of source (Moseley standard). "
            "Dilution by blurring is an association arising from similarity between a mark and "
            "a famous mark that impairs the distinctiveness of the famous mark. Factors include: "
            "degree of similarity, degree of inherent or acquired distinctiveness, extent of "
            "exclusive use, degree of recognition, whether the user intended to create an "
            "association, and actual association. Dilution by tarnishment is an association that "
            "harms the reputation of the famous mark, typically through unwholesome or unsavory "
            "contexts. Defenses include fair use (comparative advertising, news reporting, "
            "parody, comment, criticism), non-commercial use, and any form of news reporting "
            "and commentary. The TDRA eliminated the requirement for actual dilution, requiring "
            "only likely dilution. State dilution laws may apply with lower thresholds (niche "
            "fame sufficient in some states)."
        ),
        "authority": "15 USC 1125(c); Moseley v. V Secret Catalogue, 537 U.S. 418 (2003)",
        "confidence": 0.88,
        "citations": [
            "Moseley v. V Secret Catalogue, Inc., 537 U.S. 418 (2003)",
            "Louis Vuitton Malletier v. Haute Diggity Dog, 507 F.3d 252 (4th Cir. 2007)",
            "15 USC 1125(c)",
            "TMEP 1203.01",
        ],
        "tags": ["dilution", "blurring", "tarnishment", "famous_mark", "tdra"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "trade_dress_protection",
        "title": "Trade Dress Protection",
        "category": "trademark",
        "content": (
            "Trade dress encompasses the total commercial image or overall impression of a "
            "product, including its size, shape, color or color combinations, texture, graphics, "
            "packaging, and even certain sales techniques. To be protectable under 15 USC 1125(a), "
            "trade dress must be (1) distinctive (inherently or through secondary meaning), "
            "(2) non-functional, and (3) likely to cause confusion with the plaintiff's trade dress. "
            "Product packaging may be inherently distinctive (Two Pesos), but product configuration "
            "or design can never be inherently distinctive and always requires secondary meaning "
            "(Wal-Mart v. Samara Bros.). Functionality is determined under the Traffix test: "
            "a product feature is functional if it is essential to the use or purpose of the "
            "article or affects its cost or quality. If a feature is the subject of a utility "
            "patent, it is strong evidence of functionality. Aesthetic functionality may also "
            "bar protection if exclusive use would significantly hinder competition."
        ),
        "authority": "Two Pesos v. Taco Cabana, 505 U.S. 763 (1992); TrafFix Devices v. Marketing Displays, 532 U.S. 23 (2001)",
        "confidence": 0.87,
        "citations": [
            "Two Pesos v. Taco Cabana, 505 U.S. 763 (1992)",
            "Wal-Mart Stores v. Samara Bros., 529 U.S. 205 (2000)",
            "TrafFix Devices v. Marketing Displays, 532 U.S. 23 (2001)",
            "Qualitex Co. v. Jacobson Prods., 514 U.S. 159 (1995)",
        ],
        "tags": ["trade_dress", "packaging", "configuration", "functionality", "secondary_meaning"],
        "last_updated": "2026-02-10",
    },
]


# ============================================================================
# DOCTRINE CACHE - COPYRIGHT LAW (17 USC)
# ============================================================================

COPYRIGHT_DOCTRINES: List[Dict[str, Any]] = [
    {
        "topic": "copyright_originality_fixation",
        "title": "Copyright Originality and Fixation Requirements",
        "category": "copyright",
        "content": (
            "Copyright protection under 17 USC 102 attaches to original works of authorship "
            "fixed in a tangible medium of expression. Originality requires independent creation "
            "(not copying) plus a minimal degree of creativity (Feist). The creativity threshold "
            "is very low - almost any spark of creativity suffices. Copyright protects expression, "
            "not ideas (idea-expression dichotomy, 17 USC 102(b)). Fixation requires that the "
            "work be embodied in a copy or phonorecord by or under the authority of the author, "
            "sufficiently permanent or stable to be perceived, reproduced, or communicated for "
            "a period of more than transitory duration. Categories of works include: literary "
            "works, musical works, dramatic works, pantomimes and choreographic works, pictorial "
            "graphic and sculptural works, motion pictures and audiovisual works, sound recordings, "
            "and architectural works. Copyright does not protect facts, procedures, processes, "
            "systems, methods of operation, concepts, principles, or discoveries (Baker v. Selden). "
            "Merger doctrine: when there are only a few ways to express an idea, the expression "
            "merges with the idea and is unprotectable. Scenes a faire: stock elements that flow "
            "naturally from a genre are unprotectable."
        ),
        "authority": "17 USC 102; Feist Publications v. Rural Telephone, 499 U.S. 340 (1991)",
        "confidence": 0.93,
        "citations": [
            "Feist Publications v. Rural Telephone, 499 U.S. 340 (1991)",
            "Baker v. Selden, 101 U.S. 99 (1879)",
            "17 USC 102(a), 102(b)",
            "Mazer v. Stein, 347 U.S. 201 (1954)",
        ],
        "tags": ["originality", "fixation", "expression", "idea_expression", "merger", "scenes_a_faire"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "fair_use_defense",
        "title": "Fair Use Defense - 17 USC 107",
        "category": "copyright",
        "content": (
            "Fair use under 17 USC 107 is an affirmative defense permitting limited use of "
            "copyrighted material without permission. The four statutory factors are: "
            "(1) Purpose and character of use - commercial vs. nonprofit educational, "
            "and whether the use is transformative (Campbell v. Acuff-Rose, Andy Warhol v. "
            "Goldsmith). A transformative use adds new expression, meaning, or message beyond "
            "the original. Commercial use weighs against fair use but is not dispositive. "
            "(2) Nature of the copyrighted work - factual works receive thinner protection than "
            "creative works; published works are more susceptible to fair use than unpublished. "
            "(3) Amount and substantiality of the portion used - both quantitative and qualitative "
            "(the 'heart' of the work). Even small portions may be substantial if they are the "
            "most valuable part. (4) Effect on the potential market for the original - most "
            "important factor per Harper & Row, though Campbell de-emphasized this for "
            "transformative uses. Market harm includes both actual and potential harm, including "
            "harm to derivative markets. Google v. Oracle (2021) held that Google's copying of "
            "Java SE API declaring code was fair use, emphasizing the transformative nature of "
            "reimplementation for a new platform."
        ),
        "authority": "17 USC 107; Campbell v. Acuff-Rose Music, 510 U.S. 569 (1994); Andy Warhol Found. v. Goldsmith, 598 U.S. 508 (2023)",
        "confidence": 0.90,
        "citations": [
            "Campbell v. Acuff-Rose Music, Inc., 510 U.S. 569 (1994)",
            "Andy Warhol Foundation v. Goldsmith, 598 U.S. 508 (2023)",
            "Google LLC v. Oracle Am., Inc., 593 U.S. 1 (2021)",
            "Harper & Row v. Nation Enterprises, 471 U.S. 539 (1985)",
        ],
        "tags": ["fair_use", "transformative", "four_factors", "market_harm", "campbell"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "copyright_infringement_analysis",
        "title": "Copyright Infringement Analysis",
        "category": "copyright",
        "content": (
            "Copyright infringement requires proof of: (1) ownership of a valid copyright, and "
            "(2) copying of constituent elements of the work that are original. In the absence "
            "of direct evidence of copying, circumstantial evidence suffices: (a) access to the "
            "copyrighted work, plus (b) substantial similarity between the works. The "
            "Arnstein test (2d Cir.) uses a two-part framework: (1) probative similarity "
            "(expert-aided, dissection allowed) to show actual copying, and (2) improper "
            "appropriation based on lay observer's impression of substantial similarity "
            "(ordinary observer test). The Krofft/Cavalier test (9th Cir.) uses an "
            "extrinsic test (objective analysis of protectable elements) and intrinsic test "
            "(subjective impression of similarity). The Altai abstraction-filtration-comparison "
            "test applies to software: (1) abstract the copyrighted program into structural "
            "parts, (2) filter out unprotectable elements (ideas, merger, scenes a faire, "
            "public domain), (3) compare remaining protectable expression to the allegedly "
            "infringing program. Contributory and vicarious liability also apply. Statutory "
            "damages range from $750-$30,000 per work, up to $150,000 for willful infringement."
        ),
        "authority": "17 USC 501-504; Arnstein v. Porter, 154 F.2d 464 (2d Cir. 1946); Computer Assocs. v. Altai, 982 F.2d 693 (2d Cir. 1992)",
        "confidence": 0.90,
        "citations": [
            "Arnstein v. Porter, 154 F.2d 464 (2d Cir. 1946)",
            "Computer Associates v. Altai, 982 F.2d 693 (2d Cir. 1992)",
            "Feist Publications v. Rural Telephone, 499 U.S. 340 (1991)",
            "17 USC 501-504",
        ],
        "tags": ["infringement", "substantial_similarity", "access", "copying", "altai", "damages"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "dmca_framework",
        "title": "Digital Millennium Copyright Act (DMCA)",
        "category": "copyright",
        "content": (
            "The DMCA (Title II, 17 USC 512) provides safe harbor for online service providers "
            "(OSPs) from copyright liability if they meet certain conditions: (1) Transitory "
            "digital network communications (512(a)), (2) System caching (512(b)), (3) Storage "
            "at direction of users (512(c)), and (4) Information location tools (512(d)). "
            "For 512(c) hosting safe harbor, the OSP must: lack actual knowledge of infringing "
            "material, lack awareness of facts making infringement apparent (red flag knowledge), "
            "act expeditiously to remove material upon obtaining knowledge, not receive financial "
            "benefit directly attributable to infringement if able to control, designate a DMCA "
            "agent with the Copyright Office, and implement a repeat infringer policy. "
            "DMCA takedown/counter-notice procedure: copyright holder sends takedown notice "
            "(512(c)(3) requirements), OSP removes material, alleged infringer may submit "
            "counter-notice, OSP restores material after 10-14 business days unless suit is "
            "filed. Title I anti-circumvention (17 USC 1201) prohibits circumventing "
            "technological protection measures (TPMs) and trafficking in circumvention tools. "
            "Exemptions are granted every three years by the Librarian of Congress."
        ),
        "authority": "17 USC 512, 1201-1204",
        "confidence": 0.88,
        "citations": [
            "17 USC 512(a)-(d), 512(c)(3)",
            "17 USC 1201-1204",
            "Viacom Int'l v. YouTube, 676 F.3d 19 (2d Cir. 2012)",
            "UMG Recordings v. Shelter Capital Partners, 718 F.3d 1006 (9th Cir. 2013)",
        ],
        "tags": ["dmca", "safe_harbor", "takedown", "anti_circumvention", "512"],
        "last_updated": "2026-02-10",
    },
]


# ============================================================================
# DOCTRINE CACHE - TRADE SECRET LAW
# ============================================================================

TRADE_SECRET_DOCTRINES: List[Dict[str, Any]] = [
    {
        "topic": "trade_secret_elements",
        "title": "Trade Secret Elements and Protection",
        "category": "trade_secret",
        "content": (
            "Under both the Defend Trade Secrets Act (DTSA, 18 USC 1836) and the Uniform Trade "
            "Secrets Act (UTSA, adopted in 48 states), a trade secret must satisfy three elements: "
            "(1) The information derives independent economic value from not being generally known "
            "to or readily ascertainable by others who could obtain economic benefit from its "
            "disclosure or use. (2) The information is not generally known or readily ascertainable "
            "to the public or competitors. (3) The owner has taken reasonable measures to maintain "
            "the secrecy of the information. Types of information protectable as trade secrets: "
            "formulas, patterns, compilations, programs, devices, methods, techniques, processes, "
            "financial data, customer lists, supplier lists, pricing information, marketing "
            "strategies, source code, algorithms, and business plans. Reasonable measures include: "
            "NDAs/confidentiality agreements, limiting access on a need-to-know basis, physical "
            "and electronic security measures, employee exit procedures, marking confidential "
            "documents, compartmentalizing information, and regular audits. Trade secret protection "
            "is perpetual (unlimited duration) as long as secrecy is maintained. Unlike patents, "
            "trade secrets protect against misappropriation but not independent discovery or "
            "reverse engineering."
        ),
        "authority": "18 USC 1836 (DTSA); UTSA Section 1",
        "confidence": 0.91,
        "citations": [
            "18 USC 1831-1839 (Economic Espionage Act/DTSA)",
            "UTSA Sections 1-12",
            "Kewanee Oil Co. v. Bicron Corp., 416 U.S. 470 (1974)",
            "Restatement (Third) of Unfair Competition Sections 39-45",
        ],
        "tags": ["trade_secret", "dtsa", "utsa", "reasonable_measures", "economic_value", "secrecy"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "trade_secret_misappropriation",
        "title": "Trade Secret Misappropriation and Remedies",
        "category": "trade_secret",
        "content": (
            "Misappropriation under DTSA/UTSA occurs through: (1) acquisition by improper means "
            "(theft, bribery, misrepresentation, breach of duty, espionage, electronic intrusion), "
            "or (2) disclosure or use of a trade secret by one who acquired it through improper "
            "means, or who knew or should have known it was acquired through improper means, or "
            "who had a duty to maintain secrecy. Reverse engineering and independent discovery are "
            "lawful means of acquisition and are complete defenses. The DTSA provides: injunctive "
            "relief (including in exceptional circumstances, conditions on employment that are "
            "not greater than necessary to protect trade secrets), damages for actual loss plus "
            "unjust enrichment (or a reasonable royalty), up to 2x damages for willful and "
            "malicious misappropriation, and attorney fees for willful/malicious misappropriation "
            "or bad faith claims. The DTSA's ex parte seizure provision (18 USC 1836(b)(2)) "
            "allows courts to order seizure of property to prevent propagation of trade secrets "
            "in extraordinary circumstances. The DTSA includes an immunity provision for "
            "whistleblowers who disclose trade secrets in confidence to government officials "
            "or in court filings under seal. Statute of limitations: 3 years under DTSA, "
            "varies by state under UTSA (typically 3-5 years from discovery)."
        ),
        "authority": "18 USC 1836; UTSA Sections 2-4",
        "confidence": 0.90,
        "citations": [
            "18 USC 1836(b)(1)-(3)",
            "UTSA Sections 2-4",
            "Waymo LLC v. Uber Technologies, Inc., No. 17-cv-00939 (N.D. Cal.)",
            "E.I. du Pont de Nemours v. Christopher, 431 F.2d 1012 (5th Cir. 1970)",
        ],
        "tags": ["misappropriation", "improper_means", "remedies", "injunction", "seizure", "whistleblower"],
        "last_updated": "2026-02-10",
    },
]


# ============================================================================
# DOCTRINE CACHE - IP LICENSING AND VALUATION
# ============================================================================

LICENSING_DOCTRINES: List[Dict[str, Any]] = [
    {
        "topic": "ip_licensing_frameworks",
        "title": "IP Licensing Frameworks and Best Practices",
        "category": "licensing",
        "content": (
            "IP licensing grants permission to use intellectual property rights under specified "
            "conditions. Key license types: (1) Exclusive license - licensee is the only party "
            "authorized to practice, even excluding the licensor (must be in writing under "
            "patent/copyright law). (2) Sole license - only the licensee and licensor may "
            "practice. (3) Non-exclusive license - multiple licensees may be authorized. "
            "Critical license terms include: field of use restrictions, territorial limitations, "
            "sublicensing rights, royalty structure (running, lump-sum, milestone, minimum "
            "guarantees), improvements (grant-back vs. shop rights), term and termination, "
            "representations and warranties (validity, non-infringement, ownership), "
            "indemnification, audit rights, and dispute resolution. For patent licenses, "
            "Brulotte v. Thys (1964) held that royalties cannot extend beyond the patent term "
            "(still good law despite criticism). For FRAND-encumbered standard-essential patents "
            "(SEPs), the licensor must offer fair, reasonable, and non-discriminatory terms. "
            "Georgia-Pacific factors apply to determine reasonable royalty rates. Cross-licensing "
            "and patent pools are common in technology sectors. Open source licenses (GPL, MIT, "
            "Apache) create IP licensing obligations that must be tracked in compliance programs."
        ),
        "authority": "35 USC 261 (patent assignments); 17 USC 101, 204 (copyright licenses)",
        "confidence": 0.87,
        "citations": [
            "Brulotte v. Thys Co., 379 U.S. 29 (1964)",
            "Kimble v. Marvel Entertainment, 576 U.S. 446 (2015)",
            "35 USC 261",
            "17 USC 101, 204",
        ],
        "tags": ["licensing", "exclusive", "royalty", "frand", "sep", "cross_license", "open_source"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "ip_valuation_methods",
        "title": "IP Valuation Methodologies",
        "category": "valuation",
        "content": (
            "IP valuation employs three primary methodologies: (1) Income approach - values IP "
            "based on the present value of future economic benefits attributable to the IP asset. "
            "Methods include discounted cash flow (DCF), relief from royalty (what would be paid "
            "in a hypothetical license), and excess earnings (residual income after deducting "
            "returns on other assets). (2) Market approach - values IP based on comparable "
            "transactions involving similar IP assets. Requires arm's-length transactions with "
            "sufficient comparability adjustments. Sources include IP licensing databases "
            "(RoyaltyStat, ktMINE, SEC filings). (3) Cost approach - values IP at the cost to "
            "recreate or replace it, including R&D expenditures, prosecution costs, and "
            "opportunity costs. Generally considered a floor value. Key factors affecting IP "
            "value: remaining term, geographic scope, technology lifecycle position, competitive "
            "landscape, legal strength (claim breadth, prosecution history, prior art), "
            "revenue generated, cost savings enabled, strategic value (blocking, design-around "
            "difficulty), and enforceability record. IP valuation is required for M&A (ASC 805), "
            "financial reporting (ASC 350), tax purposes (transfer pricing, donation), "
            "licensing negotiations, litigation damages, and strategic portfolio management."
        ),
        "authority": "ASC 805, ASC 350; IVSC International Valuation Standards",
        "confidence": 0.85,
        "citations": [
            "ASC 805 Business Combinations",
            "ASC 350 Intangibles - Goodwill and Other",
            "IVSC IVS 210 Intangible Assets",
            "OECD Transfer Pricing Guidelines Chapter VI",
        ],
        "tags": ["valuation", "income_approach", "market_approach", "cost_approach", "dcf", "royalty_rate"],
        "last_updated": "2026-02-10",
    },
]


# ============================================================================
# DOCTRINE CACHE - INTERNATIONAL IP
# ============================================================================

INTERNATIONAL_DOCTRINES: List[Dict[str, Any]] = [
    {
        "topic": "pct_international_filing",
        "title": "Patent Cooperation Treaty (PCT) International Filing",
        "category": "international",
        "content": (
            "The PCT, administered by WIPO with 157 member states, provides a unified procedure "
            "for filing patent applications in multiple countries. Key phases: (1) International "
            "phase - file PCT application with a receiving office (e.g., USPTO as RO/US) within "
            "12 months of earliest priority date. Includes international search (ISR) by an "
            "International Searching Authority (ISA), written opinion on patentability, and "
            "optional international preliminary examination (Chapter II, IPEA). Publication occurs "
            "at 18 months from priority date. (2) National/regional phase - enter designated "
            "offices by month 30 (or 31 in some offices) from priority date. Each national office "
            "applies its own patentability standards. Strategic advantages: single filing secures "
            "an international filing date in all designated states, defers costs of national phase "
            "entry by 18-19 months beyond Paris Convention priority, provides early search report "
            "for prosecution strategy, and allows claim amendment before national phase entry. "
            "Cost considerations: international phase fees (search, filing, transmission), "
            "national phase entry fees (vary by country), translation costs, and local agent "
            "fees. The ISA written opinion is non-binding but influential. PPH (Patent Prosecution "
            "Highway) allows acceleration based on favorable PCT or national office reports."
        ),
        "authority": "Patent Cooperation Treaty (PCT); WIPO",
        "confidence": 0.88,
        "citations": [
            "Patent Cooperation Treaty (1970, as amended)",
            "PCT Regulations (WIPO)",
            "37 CFR 1.431-1.499 (US national phase)",
            "MPEP 1800-1899",
        ],
        "tags": ["pct", "international", "wipo", "national_phase", "isa", "pph"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "freedom_to_operate_analysis",
        "title": "Freedom to Operate (FTO) Analysis",
        "category": "fto",
        "content": (
            "A freedom-to-operate (FTO) analysis assesses whether a proposed product, process, "
            "or service can be commercialized without infringing valid and enforceable IP rights "
            "of third parties. The process involves: (1) Define the product/process features "
            "with specificity. (2) Identify relevant jurisdictions for launch/sale. (3) Search "
            "for active patents and published applications in each jurisdiction - focus on "
            "independent claims of in-force patents. (4) Analyze each identified patent: "
            "claim construction, element-by-element comparison, prosecution history review, "
            "and validity assessment. (5) Assess risk level per claim: high (literal read), "
            "medium (potential DOE), low (missing elements). (6) Develop mitigation strategies: "
            "design-around options, invalidity challenges (IPR/PGR), licensing opportunities, "
            "monitoring programs, and insurance. FTO opinions should clearly identify scope, "
            "limitations, and assumptions. Attorney-client privilege and work product doctrine "
            "protect FTO opinions, but courts may draw adverse inferences from failure to obtain "
            "or waiver of opinion counsel defense. For new market entry, FTO should cover the "
            "entire product lifecycle: manufacturing, distribution, marketing, and end-user use. "
            "Patent landscape analysis supplements FTO by identifying white space opportunities "
            "and competitive positioning."
        ),
        "authority": "Practice-based framework; 35 USC 271, 282-287",
        "confidence": 0.86,
        "citations": [
            "35 USC 271 (infringement)",
            "35 USC 282 (presumption of validity)",
            "35 USC 285 (attorney fees)",
            "Knorr-Bremse Systeme v. Dana Corp., 383 F.3d 1337 (Fed. Cir. 2004) (en banc)",
        ],
        "tags": ["fto", "freedom_to_operate", "clearance", "design_around", "risk_assessment", "landscape"],
        "last_updated": "2026-02-10",
    },
]


# ============================================================================
# DOCTRINE CACHE - IP STRATEGY AND PORTFOLIO
# ============================================================================

STRATEGY_DOCTRINES: List[Dict[str, Any]] = [
    {
        "topic": "ip_due_diligence",
        "title": "IP Due Diligence in M&A and Investment",
        "category": "portfolio",
        "content": (
            "IP due diligence is a critical component of mergers, acquisitions, investments, "
            "and licensing transactions. A comprehensive IP due diligence review covers: "
            "(1) Ownership verification - confirm clear chain of title from inventors through "
            "assignments to current owner; check for prior encumbrances, liens, or security "
            "interests; verify inventor declarations are properly executed; confirm no joint "
            "ownership issues. (2) Registration status - verify all registrations are current "
            "and properly maintained; check for pending applications and their prosecution "
            "status; review maintenance fee payment history. (3) Scope assessment - analyze "
            "claim breadth for patents; evaluate mark strength for trademarks; review copyright "
            "registration scope; assess trade secret documentation. (4) Freedom to operate - "
            "identify third-party IP that could be infringed; review existing licenses and their "
            "terms (especially change of control provisions); assess pending litigation or "
            "disputes. (5) Valuation - apply income, market, and cost approaches; consider "
            "remaining useful life; assess competitive advantage provided. (6) IP agreements - "
            "review all licenses (in and out), joint development agreements, co-existence "
            "agreements, settlement agreements, and consulting/employment agreements with IP "
            "provisions. (7) Open source audit - identify all OSS components and their licenses; "
            "assess compliance obligations and copyleft risks. (8) International coverage - "
            "review foreign filings, registrations, and enforcement actions. Common red flags: "
            "missing assignments, lapsed maintenance fees, undisclosed co-inventors, unrecorded "
            "licenses, pending IPR proceedings, broad prior art, key-person risk for trade secrets."
        ),
        "authority": "Practice-based framework; UCC Article 9 (security interests in IP)",
        "confidence": 0.86,
        "citations": [
            "UCC Article 9 (security interests in IP)",
            "35 USC 261 (patent assignments)",
            "15 USC 1060 (trademark assignments)",
            "17 USC 204 (copyright transfers require writing)",
        ],
        "tags": ["due_diligence", "m_and_a", "portfolio", "ownership", "chain_of_title", "investment"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "patent_landscape_analysis",
        "title": "Patent Landscape and Competitive Intelligence",
        "category": "portfolio",
        "content": (
            "Patent landscape analysis (also called patent mapping or patent analytics) provides "
            "strategic intelligence about the patent environment in a technology area. Key "
            "components include: (1) Technology mapping - cluster patents by technology subfields "
            "using CPC/USPC classifications, keyword analysis, and citation networks to identify "
            "technology trends, hotspots, and white spaces. (2) Competitive analysis - identify "
            "key players, their portfolio sizes, filing rates, geographic coverage, and technology "
            "focus areas; track prosecution success rates and average claim breadth. (3) Citation "
            "analysis - identify foundational patents with high forward citation counts; map "
            "citation networks to understand technology evolution; identify patent families and "
            "continuation chains. (4) White space identification - find technology areas with low "
            "patent density that represent filing opportunities; analyze convergence zones where "
            "multiple technologies meet. (5) Expiration analysis - identify patents expiring in "
            "the near term that may open competitive opportunities; plan generic/biosimilar entry "
            "strategies around patent cliffs. (6) Standard-essential patents - identify SEPs in "
            "relevant standards; assess FRAND licensing obligations and rates. Tools: PatSnap, "
            "Orbit Intelligence, Derwent Innovation, Google Patents, USPTO PAIR/PatFT. "
            "Deliverables: heat maps, filing trend charts, competitor scorecards, white space "
            "maps, technology cluster diagrams, and strategic recommendations."
        ),
        "authority": "WIPO Patent Landscape Reports methodology",
        "confidence": 0.84,
        "citations": [
            "WIPO Manual on Patent Landscape Analysis",
            "USPTO Patent Landscape Analysis resources",
        ],
        "tags": ["landscape", "analytics", "competitive_intelligence", "white_space", "patent_mapping"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "ip_strategy_framework",
        "title": "IP Strategy Development Framework",
        "category": "portfolio",
        "content": (
            "An effective IP strategy aligns intellectual property management with business "
            "objectives. The framework comprises: (1) Business alignment - map IP assets and "
            "activities to specific business goals (market protection, revenue generation, "
            "competitive defense, talent attraction). (2) Filing strategy - determine when to "
            "seek patent, trademark, copyright, or trade secret protection; define geographic "
            "filing priorities based on commercial markets, manufacturing locations, and "
            "competitor jurisdictions. (3) Prosecution management - set quality standards for "
            "applications; define continuation/divisional strategies; establish office action "
            "response protocols; manage examiner interviews. (4) Enforcement strategy - define "
            "monitoring programs; establish infringement response protocols; set litigation "
            "thresholds; maintain enforcement readiness (e.g., marked products, damage records). "
            "(5) Defense strategy - maintain freedom-to-operate awareness; build defensive "
            "portfolios; participate in defensive patent programs; monitor IPR/PGR risks. "
            "(6) Monetization - identify licensing opportunities; assess cross-licensing value; "
            "evaluate divestiture candidates; consider IP-backed financing. (7) Portfolio "
            "optimization - conduct regular portfolio audits; prune low-value assets to reduce "
            "maintenance costs; identify gaps requiring new filings. (8) Budget management - "
            "allocate resources across prosecution, maintenance, enforcement, and licensing. "
            "Review and update IP strategy annually or upon major business changes."
        ),
        "authority": "Best practices framework; IAM (Intellectual Asset Management) methodology",
        "confidence": 0.83,
        "citations": [
            "IAM Intellectual Asset Management framework",
            "AIPPI Guidelines on IP Strategy",
        ],
        "tags": ["strategy", "portfolio", "business_alignment", "filing_strategy", "optimization"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "ai_generated_ip_issues",
        "title": "AI-Generated Works and IP Issues",
        "category": "patent",
        "content": (
            "Artificial intelligence raises novel IP questions across patent, copyright, and "
            "trade secret law. Patent law: (1) Inventorship - under Thaler v. Vidal (Fed. Cir. "
            "2022), AI systems cannot be named as inventors on US patents; only natural persons "
            "can be inventors. However, a person who uses AI as a tool in the inventive process "
            "may qualify as inventor if they made a significant intellectual contribution. "
            "(2) Subject matter eligibility - AI/ML inventions face 101 challenges as potentially "
            "abstract mathematical algorithms; claims should emphasize specific technical "
            "improvements, training methodologies, and practical applications rather than the "
            "ML model itself. (3) Prior art concerns - AI-generated publications and code may "
            "constitute prior art. Copyright law: (1) Authorship - the US Copyright Office "
            "has held that works generated entirely by AI without human creative control are not "
            "copyrightable (Zarya of the Dawn guidance, 2023). (2) Human involvement threshold - "
            "works with sufficient human selection, arrangement, and creative direction may be "
            "copyrightable even if AI assisted in execution. (3) Training data - using "
            "copyrighted works to train AI models raises fair use and reproduction right issues "
            "(pending litigation: NYT v. OpenAI, Getty v. Stability AI). Trade secrets: AI "
            "models, training data, and hyperparameters may be protectable as trade secrets if "
            "reasonable measures are maintained."
        ),
        "authority": "Thaler v. Vidal, 43 F.4th 1207 (Fed. Cir. 2022); USCO Registration Guidance on AI",
        "confidence": 0.75,
        "citations": [
            "Thaler v. Vidal, 43 F.4th 1207 (Fed. Cir. 2022)",
            "Thaler v. Perlmutter, No. 1:22-cv-01564 (D.D.C. 2023)",
            "USCO Registration Guidance on AI-Generated Works (Feb 2023)",
            "Copyright Office, Zarya of the Dawn decision (Feb 2023)",
        ],
        "tags": ["ai", "artificial_intelligence", "inventorship", "authorship", "machine_learning", "training_data"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "standard_essential_patents",
        "title": "Standard-Essential Patents (SEPs) and FRAND",
        "category": "licensing",
        "content": (
            "Standard-essential patents (SEPs) are patents that claim inventions necessary to "
            "implement a technical standard (e.g., Wi-Fi, 5G, HEVC). SEP holders who participate "
            "in standard-setting organizations (SSOs) typically commit to license their SEPs on "
            "fair, reasonable, and non-discriminatory (FRAND) terms. Key issues: (1) Essentiality - "
            "not all declared SEPs are truly essential; over-declaration is common (estimates "
            "suggest 50-70% of declared SEPs may not be essential). (2) FRAND royalty determination - "
            "courts use multiple methodologies: comparable licenses (Ericsson v. D-Link), "
            "top-down approach (aggregate royalty for entire standard, allocate per patent), "
            "and Georgia-Pacific modified factors. (3) Anti-suit injunctions - increasing use of "
            "ASIs in SEP disputes (Huawei v. Samsung, InterDigital v. Xiaomi). (4) Hold-up "
            "and hold-out - SEP holders may exploit essentiality (hold-up) while implementers "
            "may delay licensing (hold-out); courts balance these concerns. (5) Licensing level - "
            "whether FRAND obligation requires licensing at component level or end-product level "
            "(Continental v. Avanci). (6) Global portfolio licensing - trend toward worldwide "
            "FRAND portfolio licenses rather than country-by-country licensing. (7) Patent pools - "
            "MPEG LA, Via Licensing, and others aggregate SEPs for simplified licensing."
        ),
        "authority": "IEEE-SA Patent Policy; ETSI IPR Policy; Ericsson v. D-Link Systems, 773 F.3d 1201 (Fed. Cir. 2014)",
        "confidence": 0.84,
        "citations": [
            "Ericsson v. D-Link Systems, 773 F.3d 1201 (Fed. Cir. 2014)",
            "TCL v. Ericsson, No. 8:14-cv-00341 (C.D. Cal. 2017)",
            "IEEE-SA Patent Policy (2015 update)",
            "ETSI IPR Policy",
        ],
        "tags": ["sep", "frand", "standard_essential", "licensing", "royalty", "patent_pool", "hold_up"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "trade_secret_vs_patent_choice",
        "title": "Strategic Choice: Trade Secret vs. Patent Protection",
        "category": "trade_secret",
        "content": (
            "The choice between patent and trade secret protection is a critical strategic "
            "decision. Patent advantages: (1) Exclusive right to exclude others for 20 years. "
            "(2) Protection against independent discovery. (3) Enforceable through injunction "
            "and damages. (4) Publicly disclosed - can be licensed, sold, or used as collateral. "
            "(5) Deterrent effect on competitors. Patent disadvantages: (1) Time-limited (20 years). "
            "(2) Expensive to obtain and maintain. (3) Public disclosure enables design-arounds. "
            "(4) Subject to invalidation (IPR, PGR). (5) 12-18 month prosecution time. "
            "Trade secret advantages: (1) Potentially unlimited duration. (2) No registration "
            "required. (3) No public disclosure. (4) Lower initial cost. (5) Immediate protection. "
            "Trade secret disadvantages: (1) No protection against independent discovery or "
            "reverse engineering. (2) Vulnerable to employee departures. (3) Requires ongoing "
            "reasonable measures. (4) Lost forever if secrecy is compromised. (5) Difficult to "
            "license without risk of disclosure. Decision framework: Choose patent when: "
            "the invention is independently discoverable, reverse-engineerable, or visible in "
            "the product; when licensing revenue is a goal; when the technology has a clear "
            "20-year commercial window. Choose trade secret when: the information is a process "
            "not visible in the final product (e.g., Coca-Cola formula); when independent "
            "discovery is unlikely; when the competitive advantage extends beyond 20 years; "
            "when secrecy can be reliably maintained."
        ),
        "authority": "Practice-based strategic framework; Kewanee Oil v. Bicron, 416 U.S. 470 (1974)",
        "confidence": 0.87,
        "citations": [
            "Kewanee Oil Co. v. Bicron Corp., 416 U.S. 470 (1974)",
            "35 USC 101-103 (patent requirements)",
            "18 USC 1836 (DTSA)",
        ],
        "tags": ["strategy", "trade_secret", "patent", "choice", "protection", "disclosure"],
        "last_updated": "2026-02-10",
    },
]


# ============================================================================
# PATENT PROSECUTION & PRACTICE DOCTRINES
# ============================================================================

PROSECUTION_DOCTRINES: List[Dict[str, Any]] = [
    {
        "topic": "plant_patent_law",
        "title": "Plant Patent Protection (35 USC 161-164)",
        "category": "patent",
        "content": (
            "Plant patents protect asexually reproduced distinct and new varieties of plants, "
            "excluding tuber-propagated plants and plants found in an uncultivated state. Under "
            "35 USC 161, whoever invents or discovers and asexually reproduces any distinct and "
            "new variety of plant, including cultivated sports, mutants, hybrids, and newly found "
            "seedlings, other than a tuber propagated plant or a plant found in an uncultivated "
            "state, may obtain a patent therefor. The term is 20 years from filing. Plant patents "
            "contain a single claim covering the plant as described and illustrated. The disclosure "
            "must describe the plant characteristics that distinguish it from related known varieties "
            "and its antecedents. Color photographs or drawings are required. The right conferred "
            "includes the right to exclude others from asexually reproducing the plant, and from "
            "using, offering for sale, or selling the plant so reproduced, or any of its parts. "
            "This is distinct from the Plant Variety Protection Act (PVPA), administered by the "
            "USDA, which covers sexually reproduced plant varieties (seeds). The PVPA certificate "
            "provides 20 years of protection (25 for trees and vines). Utility patents may also "
            "protect plants if they meet the standard patentability requirements, including enabling "
            "written description for genetically engineered plants."
        ),
        "authority": "35 USC 161-164",
        "confidence": 0.92,
        "citations": [
            "35 USC 161 (Patents for plants)",
            "35 USC 162 (Description, claim)",
            "35 USC 163 (Grant)",
            "35 USC 164 (Assistance of Department of Agriculture)",
            "J.E.M. Ag Supply v. Pioneer Hi-Bred International, 534 U.S. 124 (2001)",
            "Plant Variety Protection Act, 7 USC 2321-2582",
        ],
        "tags": ["plant_patent", "asexual_reproduction", "pvpa", "variety", "agriculture", "horticulture"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "continuation_practice",
        "title": "Continuation, CIP, and Divisional Applications",
        "category": "patent",
        "content": (
            "Continuation practice under 35 USC 120 and 37 CFR 1.53(b) allows applicants to file "
            "follow-on applications claiming the benefit of an earlier-filed parent application. "
            "Three types exist: (1) Continuation - same disclosure as parent, different claims, used "
            "to pursue claims not yet allowed or to broaden/narrow claim scope; (2) Continuation-in-Part "
            "(CIP) - adds new matter to parent disclosure, claims supported by new matter get CIP filing "
            "date while claims supported by parent get parent's date; (3) Divisional - filed in response "
            "to a restriction requirement, pursuing a different invention disclosed but not claimed in "
            "the parent. All must maintain an unbroken chain of copendency. The parent must be pending "
            "when the continuation is filed. Terminal disclaimers may be required to overcome double "
            "patenting rejections when claims overlap between family members. Strategic use of "
            "continuations allows building patent portfolios with layered protection, capturing "
            "competitor design-arounds, and maintaining patent pendency (submarine strategy is now "
            "limited since all patents expire 20 years from earliest effective filing date). CIPs are "
            "valuable when technology evolves during prosecution, but new matter claims lose the "
            "earlier priority date, which can be problematic if intervening prior art exists. "
            "Provisional applications (35 USC 111(b)) provide a 12-month priority window without "
            "formal claims or oath, serving as a cost-effective placeholder for the filing date."
        ),
        "authority": "35 USC 120; 37 CFR 1.53(b)",
        "confidence": 0.93,
        "citations": [
            "35 USC 120 (Benefit of earlier filing date)",
            "35 USC 121 (Divisional applications)",
            "35 USC 111(b) (Provisional applications)",
            "37 CFR 1.53(b) (Application filing requirements)",
            "37 CFR 1.78 (Claiming benefit of earlier applications)",
            "MPEP 201 (Types of Applications)",
        ],
        "tags": ["continuation", "cip", "divisional", "provisional", "filing", "prosecution", "portfolio"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "patent_appeals_process",
        "title": "Patent Prosecution Appeals (PTAB and Federal Circuit)",
        "category": "patent",
        "content": (
            "When a patent examiner issues a final rejection, the applicant has several options: "
            "(1) File a Request for Continued Examination (RCE) under 37 CFR 1.114, re-opening "
            "prosecution with new arguments or amendments; (2) Appeal to the Patent Trial and Appeal "
            "Board (PTAB) under 35 USC 134(a); (3) File a continuation with new claims. The PTAB "
            "appeal process involves filing a Notice of Appeal, then an Appeal Brief within two "
            "months (extendable). The brief must include a statement of the real party in interest, "
            "related appeals and interferences, summary of claimed subject matter, argument section "
            "addressing each rejected claim, and an evidence appendix. The examiner responds with an "
            "Examiner's Answer, to which the appellant may file a Reply Brief within two months. "
            "The PTAB panel (typically 3 Administrative Patent Judges) issues a written Decision. "
            "If the PTAB affirms, the applicant may seek further review via: (a) Request for Rehearing "
            "within one month; (b) Appeal to the U.S. Court of Appeals for the Federal Circuit under "
            "35 USC 141; (c) Civil action in the Eastern District of Virginia under 35 USC 145. "
            "PTAB ex parte appeals have approximately a 25-35% reversal rate. The Federal Circuit "
            "reviews PTAB decisions under the substantial evidence standard for fact findings and "
            "de novo for legal conclusions. Appeal costs include USPTO fees ($800 notice, $2,000 "
            "forwarding for large entities), attorney time for brief preparation, and potential "
            "oral hearing expenses."
        ),
        "authority": "35 USC 134(a); 37 CFR 41.31-41.54",
        "confidence": 0.91,
        "citations": [
            "35 USC 134(a) (Appeal to Patent Trial and Appeal Board)",
            "35 USC 141 (Appeal to Court of Appeals for the Federal Circuit)",
            "35 USC 145 (Civil action to obtain patent)",
            "37 CFR 41.31 (Notice of Appeal)",
            "37 CFR 41.37 (Appeal Brief)",
            "MPEP 1200 (Appeal)",
        ],
        "tags": ["appeal", "ptab", "federal_circuit", "prosecution", "rejection", "rce", "brief"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "patent_marking_and_notice",
        "title": "Patent Marking Requirements and Virtual Marking",
        "category": "patent",
        "content": (
            "Under 35 USC 287(a), a patentee who fails to mark patented articles may not recover "
            "damages for infringement prior to actual notice to the infringer. Proper marking requires "
            "affixing 'Patent' or 'Pat.' followed by the patent number on the article, or on the "
            "packaging if the article itself cannot be marked. The America Invents Act added virtual "
            "marking, allowing a web address (e.g., 'patent: www.company.com/patents') that associates "
            "the article with patent numbers, avoiding the need to re-tool when patents issue or expire. "
            "False marking under 35 USC 292 prohibits marking articles with patent numbers that do not "
            "cover the article with intent to deceive. The AIA limited standing for false marking suits "
            "to those who have suffered competitive injury. Marking must be consistent - once a patentee "
            "begins marking, they must continue on substantially all articles. Licensees must also be "
            "required to mark; failure by any licensee negates the marking benefit for all. For method "
            "patents, marking is not required since the patented invention is a process, not an article "
            "of manufacture. However, if a method patent also has apparatus claims, the apparatus should "
            "be marked. Constructive notice through marking is the most cost-effective way to establish "
            "the earliest possible damages date. Without marking, damages accrue only from the date of "
            "actual notice (typically a cease-and-desist letter or filing suit)."
        ),
        "authority": "35 USC 287(a); 35 USC 292",
        "confidence": 0.90,
        "citations": [
            "35 USC 287(a) (Limitation on damages; marking and notice)",
            "35 USC 292 (False marking)",
            "Nike, Inc. v. Wal-Mart Stores, Inc., 138 F.3d 1437 (Fed. Cir. 1998)",
            "American Medical Systems v. Medical Engineering Corp., 6 F.3d 1523 (Fed. Cir. 1993)",
        ],
        "tags": ["marking", "notice", "damages", "virtual_marking", "false_marking", "constructive_notice"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "patent_exhaustion_first_sale",
        "title": "Patent Exhaustion and First Sale Doctrine",
        "category": "patent",
        "content": (
            "The doctrine of patent exhaustion (first sale doctrine) provides that an authorized "
            "sale of a patented article exhausts the patentee's rights in that particular article. "
            "Once a patented item is sold, the purchaser may use, resell, or modify it without "
            "infringing the patent. The Supreme Court in Impression Products v. Lexmark Int'l (2017) "
            "held that patent exhaustion applies regardless of any restrictions the patentee purports "
            "to impose at the time of sale, and that it applies to both domestic and international "
            "sales. This overruled the Federal Circuit's earlier holdings that post-sale restrictions "
            "could be enforced under patent law and that international sales did not trigger exhaustion. "
            "Exhaustion applies only to authorized sales - unauthorized sales (e.g., by an infringer) "
            "do not exhaust the patent. For method claims, exhaustion applies when all apparatus needed "
            "to practice the method is sold. Self-replicating technologies (e.g., seeds) raise unique "
            "issues: in Bowman v. Monsanto (2013), the Supreme Court held that patent exhaustion does "
            "not permit a farmer to reproduce patented seeds through planting and harvesting without "
            "the patent holder's permission. The exhaustion doctrine reflects the principle that a "
            "patentee is entitled to one royalty per patented article, not an ongoing royalty stream "
            "through the article's life. Post-sale restrictions may still be enforceable under contract "
            "law (not patent law) between the original parties."
        ),
        "authority": "Common law doctrine; Impression Products v. Lexmark",
        "confidence": 0.93,
        "citations": [
            "Impression Products, Inc. v. Lexmark Int'l, Inc., 581 U.S. 360 (2017)",
            "Bowman v. Monsanto Co., 569 U.S. 278 (2013)",
            "Quanta Computer v. LG Electronics, 553 U.S. 617 (2008)",
            "United States v. Univis Lens Co., 316 U.S. 241 (1942)",
        ],
        "tags": ["exhaustion", "first_sale", "authorized_sale", "post_sale", "self_replicating", "repair"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "ptab_post_grant_proceedings",
        "title": "PTAB Post-Grant Proceedings (PGR, CBM, Derivation)",
        "category": "patent",
        "content": (
            "Beyond Inter Partes Review (IPR), the PTAB administers several other post-grant proceedings. "
            "Post-Grant Review (PGR) under 35 USC 321-329 must be filed within 9 months of patent grant "
            "and can challenge on any ground of invalidity (101, 102, 103, 112), unlike IPR which is "
            "limited to 102/103 based on patents and printed publications. PGR has a higher institution "
            "threshold ('more likely than not' vs IPR's 'reasonable likelihood'). Covered Business Method "
            "(CBM) review was a transitional program (now expired for new filings post-September 2020) "
            "targeting business method patents. Derivation proceedings under 35 USC 135 determine "
            "whether an inventor named in an earlier-filed application derived the claimed invention "
            "from an inventor named in a petition, replacing the prior interference proceedings. "
            "All PTAB proceedings share common features: institution decision within 6 months of filing, "
            "final written decision within 12 months of institution (extendable by 6 months for good "
            "cause), limited discovery, claim construction using Phillips standard (changed from BRI "
            "in 2018), and estoppel provisions. IPR/PGR estoppel under 35 USC 315(e)/325(e) bars "
            "the petitioner from asserting in subsequent proceedings any ground that was raised or "
            "reasonably could have been raised during the PTAB proceeding. Fintiv factors govern "
            "discretionary denial when parallel district court litigation is advanced. The Director's "
            "review authority allows the USPTO Director to review PTAB decisions sua sponte or on "
            "request, adding a layer of agency oversight."
        ),
        "authority": "35 USC 311-329; AIA",
        "confidence": 0.91,
        "citations": [
            "35 USC 321-329 (Post-Grant Review)",
            "35 USC 135 (Derivation proceedings)",
            "Apple Inc. v. Fintiv, Inc., IPR2020-00019 (PTAB 2020)",
            "Phillips v. AWH Corp., 415 F.3d 1303 (Fed. Cir. 2005) (en banc)",
            "SAS Institute Inc. v. Iancu, 584 U.S. 54 (2018)",
        ],
        "tags": ["ptab", "pgr", "cbm", "derivation", "post_grant", "estoppel", "fintiv", "institution"],
        "last_updated": "2026-02-10",
    },
]


# ============================================================================
# TRADEMARK REGISTRATION & CANCELLATION DOCTRINES
# ============================================================================

TRADEMARK_REGISTRATION_DOCTRINES: List[Dict[str, Any]] = [
    {
        "topic": "trademark_registration_process",
        "title": "Federal Trademark Registration (USPTO)",
        "category": "trademark",
        "content": (
            "Federal trademark registration under the Lanham Act provides significant benefits: "
            "constructive notice of ownership nationwide (15 USC 1072), prima facie evidence of "
            "validity and ownership (15 USC 1057(b)), access to federal courts, basis for obtaining "
            "registration in foreign countries, ability to record with U.S. Customs for import "
            "protection, and the path to incontestable status after 5 years of continuous use. "
            "The registration process begins with filing an application (use-based under 1(a) or "
            "intent-to-use under 1(b)) identifying the mark, owner, goods/services (classified under "
            "the Nice Classification system), and basis for filing. Examining attorneys review for "
            "compliance with formal requirements and potential bars to registration under Section 2 "
            "(including likelihood of confusion with existing registrations, mere descriptiveness, "
            "deceptiveness, geographic descriptiveness, primarily merely a surname, and functional "
            "matter). If approved, the mark is published in the Official Gazette for a 30-day "
            "opposition period. If no opposition is filed (or opposition fails), use-based marks "
            "proceed to registration. ITU marks receive a Notice of Allowance, and the applicant "
            "must file a Statement of Use within 6 months (extendable up to 3 years in 6-month "
            "increments). Maintenance requirements: Declaration of Use (Section 8) between years "
            "5-6, renewal (Section 9) every 10 years, and Declaration of Incontestability (Section "
            "15) after 5 years of continuous use. The Trademark Modernization Act of 2020 added "
            "ex parte expungement and reexamination proceedings to cancel registrations for marks "
            "never used or not used on all goods/services."
        ),
        "authority": "15 USC 1051-1072 (Lanham Act)",
        "confidence": 0.94,
        "citations": [
            "15 USC 1051 (Application for registration; verification)",
            "15 USC 1057(b) (Certificates of registration; prima facie evidence)",
            "15 USC 1058 (Duration; Section 8 affidavits)",
            "15 USC 1059 (Renewal; Section 9)",
            "15 USC 1065 (Incontestability; Section 15)",
            "15 USC 1072 (Registration as constructive notice)",
            "Trademark Modernization Act of 2020",
        ],
        "tags": ["registration", "trademark", "lanham_act", "itu", "use_based", "nice_classification",
                 "incontestability", "maintenance"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "trademark_cancellation_proceedings",
        "title": "TTAB Cancellation and Opposition Proceedings",
        "category": "trademark",
        "content": (
            "The Trademark Trial and Appeal Board (TTAB) adjudicates oppositions and cancellations. "
            "Opposition proceedings under 15 USC 1063 must be filed within 30 days of publication "
            "(extendable). Any person who believes they would be damaged may oppose. Cancellation "
            "under 15 USC 1064 may be filed anytime within 5 years of registration on most grounds, "
            "and at any time for marks that are generic, functional, abandoned, obtained by fraud, or "
            "used to misrepresent source. TTAB proceedings are quasi-judicial with discovery (including "
            "interrogatories, document requests, depositions, and admissions), testimony periods, "
            "trial briefs, and oral arguments. The TTAB applies Federal Rules of Evidence and the "
            "Federal Rules of Civil Procedure (with modifications). Standing requires a real interest "
            "in the proceeding and a reasonable belief of damage. The burden of proof is on the "
            "petitioner/opposer by a preponderance of the evidence. TTAB decisions are reviewable "
            "by the Federal Circuit or by de novo civil action in federal district court under 15 USC "
            "1071. Concurrent use proceedings under 15 USC 1052(d) establish geographically restricted "
            "registrations when multiple parties have legitimate rights in similar marks in different "
            "regions. The TTAB does not award damages or injunctions - it only determines the right "
            "to register. A TTAB cancellation does not eliminate common law trademark rights. "
            "However, TTAB findings may have preclusive effect in subsequent federal court litigation "
            "under B&B Hardware v. Hargis Industries (2015)."
        ),
        "authority": "15 USC 1063-1064; TTAB Rules of Practice",
        "confidence": 0.91,
        "citations": [
            "15 USC 1063 (Opposition to registration)",
            "15 USC 1064 (Cancellation of registration)",
            "15 USC 1071 (Appeal to courts)",
            "37 CFR 2.101-2.145 (TTAB Rules)",
            "B&B Hardware, Inc. v. Hargis Industries, Inc., 575 U.S. 138 (2015)",
        ],
        "tags": ["ttab", "cancellation", "opposition", "trademark", "proceeding", "concurrent_use", "preclusion"],
        "last_updated": "2026-02-10",
    },
]


# ============================================================================
# COPYRIGHT EXTENDED DOCTRINES
# ============================================================================

COPYRIGHT_EXTENDED_DOCTRINES: List[Dict[str, Any]] = [
    {
        "topic": "copyright_registration_benefits",
        "title": "Copyright Registration Process and Benefits",
        "category": "copyright",
        "content": (
            "While copyright protection attaches automatically upon fixation in a tangible medium, "
            "registration with the U.S. Copyright Office provides critical benefits. Under 17 USC 411, "
            "registration (or refusal) is a prerequisite to filing an infringement action for U.S. "
            "works. Registration within 3 months of publication or before infringement enables recovery "
            "of statutory damages ($750-$30,000 per work, up to $150,000 for willful infringement) and "
            "attorney's fees under 17 USC 504-505, which are often the primary deterrent and leverage "
            "in enforcement. Registration creates a public record and constitutes prima facie evidence "
            "of the validity of the copyright if made within 5 years of first publication (17 USC 410(c)). "
            "The registration process involves filing an application (Standard, Single, or Group), "
            "depositing a copy of the work, and paying the fee ($65 online for Standard as of 2024). "
            "Processing time is 1-8 months for online applications. The Copyright Office examines for "
            "copyrightable subject matter and originality, but the examination is less rigorous than "
            "patent examination. The effective date of registration is the date the Copyright Office "
            "receives all required elements, not the date the certificate issues. Preregistration under "
            "17 USC 408(f) is available for certain unpublished works (motion pictures, musical "
            "compositions, sound recordings, computer programs, literary works, advertising photographs) "
            "that have a history of pre-release infringement, allowing suit before formal registration."
        ),
        "authority": "17 USC 408-412",
        "confidence": 0.93,
        "citations": [
            "17 USC 408 (Copyright registration in general)",
            "17 USC 410(c) (Registration as prima facie evidence)",
            "17 USC 411 (Registration prerequisite to infringement suit)",
            "17 USC 412 (Registration prerequisite to statutory damages)",
            "Fourth Estate Public Benefit Corp. v. Wall-Street.com, 586 U.S. 296 (2019)",
        ],
        "tags": ["registration", "copyright", "statutory_damages", "attorney_fees", "deposit", "prima_facie"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "work_for_hire_doctrine",
        "title": "Work Made for Hire Doctrine",
        "category": "copyright",
        "content": (
            "Under 17 USC 101 and 201(b), a 'work made for hire' vests initial copyright ownership "
            "in the employer or commissioning party rather than the individual creator. Two categories "
            "exist: (1) Works prepared by an employee within the scope of employment - determined using "
            "the agency law factors from Community for Creative Non-Violence v. Reid (1989) (control, "
            "skill, tools, location, duration, hiring party's right to assign, method of payment, "
            "benefits, tax treatment, hiring party's business, employee benefits, and other factors); "
            "(2) Specially ordered or commissioned works in 9 enumerated categories (contribution to "
            "a collective work, part of a motion picture, translation, supplementary work, compilation, "
            "instructional text, test, test answer material, atlas) IF the parties expressly agree in "
            "a signed writing that the work is made for hire. The work-for-hire designation has major "
            "consequences: the employer is the author from inception (no termination right exists under "
            "17 USC 203), the copyright term is 95 years from publication or 120 years from creation "
            "(whichever is shorter) rather than life + 70 years, and the employer controls all rights "
            "without the need for an assignment. Independent contractors are generally NOT employees "
            "for work-for-hire purposes, and if the work does not fall into one of the 9 commissioned "
            "categories, a separate assignment of copyright is needed. Joint works created by employees "
            "of different companies raise complex ownership questions requiring careful contractual "
            "planning."
        ),
        "authority": "17 USC 101, 201(b)",
        "confidence": 0.93,
        "citations": [
            "17 USC 101 (Definition of work made for hire)",
            "17 USC 201(b) (Works made for hire)",
            "17 USC 203 (Termination of transfers - not applicable to WFH)",
            "Community for Creative Non-Violence v. Reid, 490 U.S. 730 (1989)",
            "Marvel Characters Inc. v. Kirby, 726 F.3d 119 (2d Cir. 2013)",
        ],
        "tags": ["work_for_hire", "copyright", "ownership", "employee", "independent_contractor",
                 "commissioned", "termination"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "joint_authorship_copyright",
        "title": "Joint Authorship and Co-Ownership in Copyright",
        "category": "copyright",
        "content": (
            "Under 17 USC 101, a 'joint work' is prepared by two or more authors with the intention "
            "that their contributions be merged into inseparable or interdependent parts of a unitary "
            "whole. Joint authors are co-owners of the entire copyright, each having an equal undivided "
            "interest regardless of the relative quantity or quality of their contributions. Each joint "
            "author may grant nonexclusive licenses without the other's consent but must account for "
            "profits to the other co-owners. Exclusive licenses require all co-owners' consent. "
            "The Childress v. Taylor (1991) test (adopted by most circuits) requires: (1) each "
            "co-author must intend the work to be joint at the time of creation, and (2) each "
            "co-author must make an independently copyrightable contribution. The Ninth Circuit in "
            "Aalmuhammed v. Lee (2000) added a 'superintendence' requirement, requiring control over "
            "the work. Intent is assessed objectively based on factors including decision-making "
            "authority, audience billing, written agreements, and how the parties describe themselves. "
            "Joint ownership creates a tenancy in common (not joint tenancy), meaning each owner's "
            "share is independently transferable and heritable. Problems arise when there is no written "
            "agreement: disputes over exploitation decisions, revenue splits, and credit attribution "
            "are common. Best practice requires written collaboration agreements specifying ownership "
            "percentages, decision-making authority, credit, exploitation rights, revenue sharing, "
            "termination procedures, and dispute resolution mechanisms."
        ),
        "authority": "17 USC 101, 201(a)",
        "confidence": 0.90,
        "citations": [
            "17 USC 101 (Definition of joint work)",
            "17 USC 201(a) (Initial ownership - joint works)",
            "Childress v. Taylor, 945 F.2d 500 (2d Cir. 1991)",
            "Aalmuhammed v. Lee, 202 F.3d 1227 (9th Cir. 2000)",
            "Thomson v. Larson, 147 F.3d 195 (2d Cir. 1998)",
        ],
        "tags": ["joint_authorship", "co_ownership", "copyright", "collaboration", "undivided_interest",
                 "tenancy_in_common", "copyrightable_contribution"],
        "last_updated": "2026-02-10",
    },
]


# ============================================================================
# INTERNATIONAL IP EXTENDED DOCTRINES
# ============================================================================

INTERNATIONAL_EXTENDED_DOCTRINES: List[Dict[str, Any]] = [
    {
        "topic": "madrid_protocol_trademarks",
        "title": "Madrid Protocol International Trademark System",
        "category": "international",
        "content": (
            "The Madrid Protocol (administered by WIPO) provides a centralized filing system for "
            "obtaining trademark protection in multiple countries through a single International "
            "Registration. The process: (1) Obtain a 'basic mark' registration or application in the "
            "home country (the 'Office of Origin'); (2) File an international application through the "
            "Office of Origin designating target countries; (3) WIPO's International Bureau examines "
            "for formalities and publishes in the WIPO Gazette; (4) Each designated Office has 12-18 "
            "months to refuse protection; silence constitutes acceptance ('deemed acceptance'). Key "
            "advantages: single application, single fee payment (in Swiss francs), single renewal "
            "every 10 years, easy subsequent designations, centralized changes of name/address. Key "
            "risks: 'central attack' dependency - if the basic mark fails (refused, cancelled, not "
            "renewed) within the first 5 years, all international designations based on it are also "
            "cancelled. However, designations can be 'transformed' into national applications retaining "
            "the international registration date. The Madrid system covers 130+ member countries. Cost "
            "savings range from 40-60% compared to filing national applications separately. Individual "
            "fee declarations vary by country. The system does not harmonize substantive law - each "
            "designated country applies its own likelihood of confusion analysis, distinctiveness "
            "requirements, and grounds for refusal. The U.S. joined the Madrid Protocol in 2003. "
            "A Section 66(a) application is the U.S. designation of an international registration."
        ),
        "authority": "Madrid Protocol; 15 USC 1141",
        "confidence": 0.91,
        "citations": [
            "Protocol Relating to the Madrid Agreement (1989)",
            "15 USC 1141-1141n (Madrid Protocol Implementation)",
            "37 CFR 7.1-7.41 (Madrid Protocol Rules)",
            "WIPO Guide to the International Registration of Marks",
        ],
        "tags": ["madrid", "international", "trademark", "wipo", "central_attack", "designation",
                 "international_registration"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "hague_agreement_industrial_designs",
        "title": "Hague Agreement for International Design Protection",
        "category": "international",
        "content": (
            "The Hague Agreement Concerning the International Registration of Industrial Designs "
            "(administered by WIPO) provides a mechanism for obtaining design protection in multiple "
            "countries through a single international application. The Geneva Act (1999), which the U.S. "
            "joined in 2015, is the primary operative text. The process: (1) File an international "
            "application directly with WIPO or through the national office; (2) Include reproductions "
            "of the design (photographs or drawings); (3) Designate member countries; (4) WIPO conducts "
            "formality examination and publishes; (5) Each designated office has 6-12 months to refuse. "
            "Key features: up to 100 designs in a single application if they belong to the same Locarno "
            "class, publication deferment up to 30 months (useful for strategic timing), single renewal. "
            "The U.S. imposes additional requirements as a designated office: designs must comply with "
            "35 USC 171 patentability standards (novelty, non-obviousness, ornamentality), claims "
            "referencing the drawings must be included, and only one design per Locarno subclass is "
            "permitted per application. The Hague system covers 90+ countries (notably excluding China "
            "until 2022 when it joined). Cost efficiency is significant for multi-country protection, "
            "particularly for consumer products, fashion, automotive, and electronics industries where "
            "design protection is commercially critical. Interaction with national design patents, "
            "registered community designs (EU), and unregistered design rights varies by jurisdiction."
        ),
        "authority": "Hague Agreement Geneva Act (1999)",
        "confidence": 0.89,
        "citations": [
            "Geneva Act of the Hague Agreement (1999)",
            "35 USC 171 (Patents for designs)",
            "37 CFR 1.1001-1.1067 (International Design Applications)",
            "Hague Agreement Common Regulations",
        ],
        "tags": ["hague", "industrial_design", "international", "wipo", "design_patent", "locarno",
                 "geneva_act"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "trips_agreement",
        "title": "TRIPS Agreement and Minimum IP Standards",
        "category": "international",
        "content": (
            "The Agreement on Trade-Related Aspects of Intellectual Property Rights (TRIPS), "
            "administered by the WTO, sets minimum standards for IP protection that all 164 WTO "
            "member states must implement in their national laws. Key provisions: Patents (Art. 27-34) "
            "- 20-year term from filing, available for inventions in all fields of technology, limited "
            "exceptions (compulsory licensing, Bolar exception, research use). Trademarks (Art. 15-21) "
            "- minimum 7-year initial term, indefinitely renewable, protection for well-known marks "
            "beyond registered goods/services. Copyright (Art. 9-14) - incorporates Berne Convention "
            "(minus moral rights), minimum term of life + 50 years (most countries now exceed this), "
            "protection for computer programs as literary works, rental rights for phonograms and "
            "computer programs. Trade Secrets (Art. 39) - protection of undisclosed information against "
            "acquisition by dishonest commercial practices. Enforcement (Art. 41-61) - requires "
            "effective enforcement procedures, civil remedies (injunctions, damages, seizure), "
            "provisional measures, border measures, and criminal procedures for willful trademark "
            "counterfeiting and copyright piracy on a commercial scale. The Doha Declaration (2001) "
            "clarified TRIPS flexibility for public health, particularly regarding compulsory licensing "
            "of pharmaceuticals. Dispute resolution is through the WTO Dispute Settlement Body. "
            "Transition periods varied: developed countries (1996), developing (2000), least-developed "
            "(extended to 2034 for general, 2033 for pharmaceuticals)."
        ),
        "authority": "WTO TRIPS Agreement (1994)",
        "confidence": 0.92,
        "citations": [
            "TRIPS Agreement (Annex 1C to WTO Agreement)",
            "Doha Declaration on TRIPS and Public Health (2001)",
            "Berne Convention for the Protection of Literary and Artistic Works",
            "Paris Convention for the Protection of Industrial Property",
        ],
        "tags": ["trips", "wto", "international", "minimum_standards", "enforcement", "compulsory_license",
                 "doha", "berne"],
        "last_updated": "2026-02-10",
    },
]


# ============================================================================
# OPEN SOURCE IP DOCTRINES
# ============================================================================

OPEN_SOURCE_DOCTRINES: List[Dict[str, Any]] = [
    {
        "topic": "open_source_licensing_fundamentals",
        "title": "Open Source Licensing and IP Implications",
        "category": "licensing",
        "content": (
            "Open source licenses are copyright licenses that grant broad permissions to use, modify, "
            "and distribute software, subject to varying conditions. The Open Source Initiative (OSI) "
            "certifies licenses meeting the Open Source Definition (10 criteria including free "
            "redistribution, source code availability, derived works permission, no discrimination "
            "against persons/groups/fields). Licenses fall on a permissive-to-copyleft spectrum: "
            "Permissive licenses (MIT, BSD-2/3-Clause, Apache-2.0) allow incorporation into "
            "proprietary products with minimal obligations (attribution, license retention). Copyleft "
            "licenses (GPL-2.0, GPL-3.0, AGPL-3.0) require derivative works to be licensed under "
            "the same terms, creating a 'viral' effect. Weak copyleft (LGPL-2.1, MPL-2.0) limits "
            "copyleft to the original component. Key patent implications: Apache-2.0 includes an "
            "express patent license and a defensive termination clause (contributing patents terminate "
            "if the licensee initiates patent litigation). GPL-3.0 includes an implicit patent "
            "license from contributors and an anti-Tivoization provision. BSD/MIT licenses have no "
            "explicit patent grant, creating potential patent risk. The Jacobsen v. Katzer (2008) "
            "decision confirmed that open source license conditions are enforceable copyright "
            "conditions (not merely covenants), enabling injunctive relief for violations. Compliance "
            "requires: tracking all open source components in a Software Bill of Materials (SBOM), "
            "honoring attribution requirements, distributing source code when required, ensuring "
            "license compatibility in combined works, and training developers on license obligations."
        ),
        "authority": "Copyright law; OSI Open Source Definition",
        "confidence": 0.90,
        "citations": [
            "Jacobsen v. Katzer, 535 F.3d 1373 (Fed. Cir. 2008)",
            "Open Source Definition v1.9 (OSI)",
            "GNU General Public License v3.0 (FSF)",
            "Apache License 2.0 (ASF)",
            "SPDX License List (Linux Foundation)",
        ],
        "tags": ["open_source", "licensing", "copyleft", "permissive", "gpl", "apache", "mit", "sbom",
                 "compliance", "derivative_work"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "open_source_patent_risk",
        "title": "Patent Risk in Open Source Software",
        "category": "licensing",
        "content": (
            "Open source software creates unique patent risk dynamics. Contributing patents: "
            "Contributors to open source projects may have patents covering contributed code. "
            "Apache-2.0 (Section 3) provides an explicit patent license from each contributor "
            "for their contributed patent claims. GPL-3.0 (Section 11) provides an implicit patent "
            "license and prohibits imposing 'further restrictions' including patent royalties on "
            "downstream users. MIT/BSD licenses contain no explicit patent terms, leaving a gap that "
            "courts have partially addressed through implied license theory. Defensive termination: "
            "Apache-2.0 terminates the patent license if a licensee files a patent infringement claim "
            "against any entity regarding the software. This discourages patent trolling against "
            "the open source community. Patent pledges: Many companies make patent pledges (e.g., "
            "Google's Open Patent Non-Assertion Pledge, Red Hat's Patent Promise, OIN's Linux "
            "System Definition cross-license). These are legally complex - some are irrevocable "
            "commitments, others are voluntary policies that may be modified. Standards and FRAND: "
            "When standards incorporate open source implementations, tension arises between FRAND "
            "licensing obligations and copyleft requirements (particularly GPL's prohibition on "
            "additional restrictions beyond the license terms). Risk mitigation strategies: "
            "(1) Maintain comprehensive SBOM; (2) Conduct IP due diligence before incorporating "
            "open source; (3) Separate open source and proprietary codebases architecturally; "
            "(4) Join defensive patent organizations (OIN, LOT Network); (5) Consider patent "
            "insurance; (6) Implement contribution license agreements (CLAs) for projects you manage."
        ),
        "authority": "Patent and copyright law intersection",
        "confidence": 0.87,
        "citations": [
            "Apache License 2.0, Section 3 (Grant of Patent License)",
            "GPL-3.0, Section 11 (Patents)",
            "Open Invention Network (OIN) License",
            "LOT Network Agreement",
            "Google Open Patent Non-Assertion Pledge",
        ],
        "tags": ["patent", "open_source", "risk", "defensive_termination", "oin", "lot_network",
                 "implied_license", "cla", "sbom"],
        "last_updated": "2026-02-10",
    },
]


# ============================================================================
# IP ENFORCEMENT & REMEDIES DOCTRINES
# ============================================================================

ENFORCEMENT_DOCTRINES: List[Dict[str, Any]] = [
    {
        "topic": "ip_injunctive_relief",
        "title": "Injunctive Relief in IP Litigation (eBay Framework)",
        "category": "enforcement",
        "content": (
            "Injunctive relief in IP cases is governed by the Supreme Court's eBay v. MercExchange "
            "(2006) four-factor test: (1) irreparable harm to the plaintiff; (2) inadequacy of money "
            "damages; (3) balance of hardships between the parties; and (4) public interest. Prior "
            "to eBay, courts in patent cases applied a near-automatic injunction rule. Post-eBay, "
            "permanent injunctions are regularly denied to non-practicing entities (NPEs/patent trolls) "
            "who do not compete in the market, as they typically cannot show irreparable harm beyond "
            "monetary damages. For practicing entities competing with the infringer, injunctions remain "
            "common. Preliminary injunctions require showing likelihood of success on the merits in "
            "addition to the eBay factors. In trademark cases, irreparable harm was traditionally "
            "presumed upon showing likelihood of confusion, but the Trademark Modernization Act of "
            "2020 reinstated a rebuttable presumption of irreparable harm, partially rolling back "
            "some post-eBay skepticism. In copyright cases, courts split on whether eBay applies with "
            "full force. Trade secret cases frequently involve inevitable disclosure injunctions "
            "preventing former employees from working for competitors, though this doctrine is "
            "controversial and not universally accepted. International Trade Commission (ITC) Section "
            "337 exclusion orders provide an alternative injunctive remedy at the border, excluding "
            "infringing imports. ITC proceedings are faster (12-18 months) and do not require eBay "
            "analysis, making them attractive for companies with domestic industry."
        ),
        "authority": "eBay v. MercExchange; Lanham Act; ITC Section 337",
        "confidence": 0.92,
        "citations": [
            "eBay Inc. v. MercExchange, L.L.C., 547 U.S. 388 (2006)",
            "Trademark Modernization Act of 2020 (rebuttable presumption)",
            "19 USC 1337 (ITC Section 337)",
            "Winter v. Natural Resources Defense Council, 555 U.S. 7 (2008)",
            "Apple Inc. v. Samsung Electronics, 809 F.3d 633 (Fed. Cir. 2015)",
        ],
        "tags": ["injunction", "ebay", "irreparable_harm", "npe", "itc", "section_337", "enforcement",
                 "preliminary_injunction"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "ip_damages_frameworks",
        "title": "IP Damages Calculation Frameworks",
        "category": "enforcement",
        "content": (
            "IP damages vary by type of IP right. Patent damages (35 USC 284): Compensatory damages "
            "measured as lost profits (Panduit test: demand, absence of acceptable non-infringing "
            "alternatives, manufacturing/marketing capability, amount of profit) or a reasonable "
            "royalty (Georgia-Pacific 15-factor hypothetical negotiation), whichever is greater. "
            "Enhanced damages up to 3x for willful infringement (Halo v. Pulse, 2016 - subjective "
            "willfulness, discretionary enhancement). Apportionment required for multi-component "
            "products (smallest salable patent-practicing unit, SSPPU, as royalty base). Entire market "
            "value rule applies only when the patented feature drives demand for the entire product. "
            "Trademark damages (15 USC 1117): (1) Defendant's profits, (2) Plaintiff's damages, "
            "(3) Costs. Trebling available. Profits require showing defendant's sales, then defendant "
            "must prove costs/deductions. Statutory damages for counterfeiting: $1,000-$200,000 per "
            "mark per type (up to $2M for willful). Copyright damages (17 USC 504): Actual damages "
            "plus defendant's profits, or statutory damages ($750-$30,000 per work, up to $150,000 "
            "for willful, minimum $200 for innocent infringement). Trade secret damages (DTSA 18 USC "
            "1836): Actual loss, unjust enrichment not duplicative of actual loss, and in lieu of "
            "damages a reasonable royalty. Exemplary damages up to 2x for willful and malicious "
            "misappropriation. Attorney's fees: Patent (exceptional cases, Octane Fitness totality "
            "of circumstances); Copyright (Kirtsaeng factors); Trademark (exceptional cases)."
        ),
        "authority": "35 USC 284; 15 USC 1117; 17 USC 504; 18 USC 1836",
        "confidence": 0.91,
        "citations": [
            "35 USC 284 (Damages for patent infringement)",
            "Panduit Corp. v. Stahlin Bros., 575 F.2d 1152 (6th Cir. 1978)",
            "Georgia-Pacific Corp. v. U.S. Plywood Corp., 318 F. Supp. 1116 (S.D.N.Y. 1970)",
            "Halo Electronics v. Pulse Electronics, 579 U.S. 93 (2016)",
            "17 USC 504 (Remedies for infringement: damages and profits)",
            "18 USC 1836 (Civil remedy under DTSA)",
        ],
        "tags": ["damages", "lost_profits", "reasonable_royalty", "statutory_damages", "willful",
                 "apportionment", "georgia_pacific", "panduit", "enforcement"],
        "last_updated": "2026-02-10",
    },
    {
        "topic": "ip_insurance_and_risk_transfer",
        "title": "IP Insurance Products and Risk Transfer",
        "category": "enforcement",
        "content": (
            "IP insurance has grown significantly as a risk management tool. Defensive IP insurance "
            "(IP abatement/defense insurance) covers the costs of defending against patent, trademark, "
            "or copyright infringement claims. Policies typically cover attorney's fees, expert witness "
            "costs, court costs, and sometimes settlement payments or judgments. Annual premiums range "
            "from $5,000-$50,000+ depending on coverage limits (typically $250K-$5M), deductibles, "
            "industry sector, and risk profile. Offensive IP insurance (IP enforcement/pursuit insurance) "
            "covers the costs of enforcing your own IP rights against infringers, enabling smaller "
            "companies to pursue litigation they could not otherwise afford. Some policies operate on "
            "a contingency model, with the insurer funding litigation in exchange for a share of any "
            "recovery. Multi-peril IP policies combine defensive and offensive coverage. Representations "
            "and warranties insurance (R&W insurance) in M&A transactions increasingly covers IP "
            "representations, protecting buyers against undisclosed IP defects, encumbrances, or "
            "infringement risks. IP valuation insurance guarantees a minimum IP portfolio value, "
            "useful for loan collateral. Open source compliance insurance covers costs arising from "
            "inadvertent open source license violations. Key underwriting factors: portfolio size, "
            "industry litigation rates, prior claims history, IP clearance procedures, and geographic "
            "scope. Notable providers include IPISC, RPX (defensive aggregation), and several Lloyd's "
            "syndicates. The IP insurance market exceeds $1B in annual premiums globally."
        ),
        "authority": "Industry practice; insurance law",
        "confidence": 0.85,
        "citations": [
            "IPISC (IP Insurance Services Corporation)",
            "RPX Corporation (Patent Risk Solutions)",
            "ABA Section of IP Law, IP Insurance Primer",
            "Lloyd's of London IP Insurance Market",
        ],
        "tags": ["insurance", "risk_transfer", "defensive", "offensive", "r_and_w", "litigation_funding",
                 "enforcement", "ip_valuation"],
        "last_updated": "2026-02-10",
    },
]


# ============================================================================
# AGGREGATE DOCTRINE CACHE
# ============================================================================

DOCTRINE_CACHE: List[Dict[str, Any]] = (
    PATENT_DOCTRINES +
    TRADEMARK_DOCTRINES +
    COPYRIGHT_DOCTRINES +
    TRADE_SECRET_DOCTRINES +
    LICENSING_DOCTRINES +
    INTERNATIONAL_DOCTRINES +
    STRATEGY_DOCTRINES +
    PROSECUTION_DOCTRINES +
    TRADEMARK_REGISTRATION_DOCTRINES +
    COPYRIGHT_EXTENDED_DOCTRINES +
    INTERNATIONAL_EXTENDED_DOCTRINES +
    OPEN_SOURCE_DOCTRINES +
    ENFORCEMENT_DOCTRINES
)


# ============================================================================
# DOCTRINE ENGINE
# ============================================================================

class IPDoctrineEngine:
    """Engine for querying the IP doctrine cache with structured responses."""

    def __init__(self, cache: Optional[List[Dict[str, Any]]] = None) -> None:
        self._cache: List[Dict[str, Any]] = cache or DOCTRINE_CACHE
        self._topic_index: Dict[str, Dict[str, Any]] = {}
        self._category_index: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._tag_index: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._build_indices()
        logger.info(
            f"IPDoctrineEngine initialized | blocks={len(self._cache)} | "
            f"topics={len(self._topic_index)} | categories={len(self._category_index)}"
        )

    def _build_indices(self) -> None:
        """Build lookup indices from doctrine cache."""
        for block in self._cache:
            topic = block["topic"]
            category = block["category"]
            self._topic_index[topic] = block
            self._category_index[category].append(block)
            for tag in block.get("tags", []):
                self._tag_index[tag].append(block)

    def lookup(self, topic: str) -> Optional[DoctrineResponse]:
        """Look up a doctrine by exact topic match."""
        block = self._topic_index.get(topic)
        if not block:
            return None
        return self._make_response(block)

    def search_by_tag(self, tag: str) -> List[DoctrineResponse]:
        """Search doctrines by tag."""
        blocks = self._tag_index.get(tag, [])
        return [self._make_response(b) for b in blocks]

    def search_by_category(self, category: str) -> List[DoctrineResponse]:
        """Search doctrines by category."""
        blocks = self._category_index.get(category, [])
        return [self._make_response(b) for b in blocks]

    def search_by_tokens(self, tokens: List[str], top_k: int = 5) -> List[DoctrineResponse]:
        """Search doctrines by matching tokens against tags and content."""
        scored: List[Tuple[float, Dict[str, Any]]] = []
        token_set = set(t.lower() for t in tokens)

        for block in self._cache:
            tag_set = set(block.get("tags", []))
            tag_overlap = len(token_set.intersection(tag_set))
            content_lower = block["content"].lower()
            content_hits = sum(1 for t in token_set if t in content_lower)
            topic_hit = 1.0 if any(t in block["topic"].lower() for t in token_set) else 0.0
            title_hit = 1.0 if any(t in block["title"].lower() for t in token_set) else 0.0

            score = (
                tag_overlap * 2.0 +
                content_hits * 0.5 +
                topic_hit * 3.0 +
                title_hit * 2.5
            )

            if score > 0:
                scored.append((score, block))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [self._make_response(b) for _, b in scored[:top_k]]

    def get_all_topics(self) -> List[str]:
        """Get all available doctrine topics."""
        return list(self._topic_index.keys())

    def get_all_categories(self) -> List[str]:
        """Get all available categories."""
        return list(self._category_index.keys())

    def get_all_tags(self) -> List[str]:
        """Get all available tags."""
        return sorted(self._tag_index.keys())

    def get_stats(self) -> Dict[str, Any]:
        """Get doctrine cache statistics."""
        return {
            "total_blocks": len(self._cache),
            "topics": len(self._topic_index),
            "categories": {k: len(v) for k, v in self._category_index.items()},
            "unique_tags": len(self._tag_index),
            "avg_content_length": (
                sum(len(b["content"]) for b in self._cache) / max(len(self._cache), 1)
            ),
            "avg_confidence": (
                sum(b["confidence"] for b in self._cache) / max(len(self._cache), 1)
            ),
        }

    def _make_response(self, block: Dict[str, Any]) -> DoctrineResponse:
        """Create a DoctrineResponse from a cache block."""
        start = time.monotonic()
        confidence = block["confidence"]
        band = self._classify_confidence(confidence)
        content = block["content"]
        hash_input = f"{block['topic']}|{content}|{block['authority']}"
        det_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()
        duration = (time.monotonic() - start) * 1000.0

        return DoctrineResponse(
            topic=block["topic"],
            title=block["title"],
            category=block["category"],
            content=content,
            authority=block["authority"],
            confidence=confidence,
            confidence_band=band,
            citations=block.get("citations", []),
            tags=block.get("tags", []),
            last_updated=block.get("last_updated", "unknown"),
            determinism_hash=det_hash,
            response_time_ms=duration,
        )

    @staticmethod
    def _classify_confidence(score: float) -> str:
        """Classify confidence score into band."""
        if score >= 0.85:
            return "DEFENSIBLE"
        if score >= 0.65:
            return "SUPPORTABLE"
        if score >= 0.50:
            return "DISCLOSURE"
        return "HIGH_RISK"


# ============================================================================
# MODULE-LEVEL SINGLETON AND CONVENIENCE FUNCTIONS
# ============================================================================

_engine: Optional[IPDoctrineEngine] = None


def get_engine() -> IPDoctrineEngine:
    """Get or create the doctrine engine singleton."""
    global _engine
    if _engine is None:
        _engine = IPDoctrineEngine()
    return _engine


def get_doctrine_cache() -> List[Dict[str, Any]]:
    """Get the raw doctrine cache."""
    return DOCTRINE_CACHE


def get_doctrine_count() -> int:
    """Get the total number of doctrine blocks."""
    return len(DOCTRINE_CACHE)


def get_doctrine_hash() -> str:
    """Get a hash of the entire doctrine cache for integrity checks."""
    content = json.dumps(DOCTRINE_CACHE, sort_keys=True)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()
