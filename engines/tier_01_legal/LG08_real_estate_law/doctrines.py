"""
LG08 Real Estate Law Engine - Doctrine Cache Module
======================================================
Pre-compiled real estate doctrine blocks for instant retrieval on common
property, title, deed, zoning, financing, landlord-tenant, eminent domain,
foreclosure, 1031 exchange, Texas-specific, and mineral rights queries.

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
Engine: LG08 Real Estate Law
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
    """A single pre-compiled real estate doctrine cache entry."""

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
    texas_notes: str = ""

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
            "texas_notes": self.texas_notes,
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
            self.texas_notes,
            " ".join(self.practice_tips),
        ]
        return " ".join(parts)

    def compute_hash(self) -> str:
        """Compute SHA-256 hash of the block content."""
        content = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(content.encode("utf-8")).hexdigest()


# ============================================================================
# DOCTRINE BLOCKS - PROPERTY TRANSACTIONS
# ============================================================================

DOCTRINE_BLOCKS: List[DoctrineCacheBlock] = [
    DoctrineCacheBlock(
        topic="real_estate_contract_formation",
        summary="Real estate purchase and sale agreements must satisfy the Statute of Frauds, requiring a signed writing that identifies the parties, property, price, and material terms. Consideration, mutual assent, legal capacity, and a lawful purpose are required. Most states enforce the mailbox rule for acceptance, but electronic signatures are valid under UETA and E-SIGN. Ambiguous contract terms are construed against the drafter. Time-of-the-essence clauses require strict compliance. Equitable conversion shifts risk of loss to the buyer upon execution in many jurisdictions.",
        key_statutes=[
            "State Statute of Frauds (varies by state)",
            "Uniform Electronic Transactions Act (UETA)",
            "15 USC 7001 (E-SIGN Act)",
            "Restatement (Second) of Contracts SS 129",
            "UCC Article 2A (lease transactions)",
            "Tex. Bus. & Com. Code SS 26.01 (Texas Statute of Frauds)",
        ],
        elements=[
            "Competent parties with legal capacity to contract",
            "Mutual assent (offer and acceptance)",
            "Adequate consideration (monetary or otherwise)",
            "Sufficiently definite terms (parties, property, price)",
            "Lawful purpose and subject matter",
            "Signed writing satisfying Statute of Frauds",
            "Property identification (legal description preferred)",
            "Compliance with any applicable disclosure requirements",
        ],
        defenses=[
            "Statute of Frauds violation (no signed writing)",
            "Mutual mistake of material fact",
            "Unilateral mistake known to the other party",
            "Fraud in the inducement or execution",
            "Duress or undue influence",
            "Lack of capacity (minor, incompetent)",
            "Unconscionability (procedural and/or substantive)",
            "Impossibility or impracticability of performance",
            "Failure of a condition precedent (financing, inspection)",
            "Part performance doctrine (may take out of Statute of Frauds)",
        ],
        remedies=[
            "Specific performance (preferred in real estate due to uniqueness)",
            "Compensatory damages (benefit of the bargain)",
            "Liquidated damages (earnest money forfeiture)",
            "Rescission and restitution",
            "Reformation of the contract",
            "Declaratory judgment on contract validity",
            "Lis pendens to protect buyer's interest during litigation",
        ],
        leading_cases=[
            "Hickey v. Green, 14 Mass. App. Ct. 671 (1982) - part performance and Statute of Frauds",
            "Centex Homes Corp. v. Boag, 128 N.J. Super. 385 (1974) - equitable conversion and risk of loss",
            "Stambovsky v. Ackley, 169 A.D.2d 254 (N.Y. 1991) - duty to disclose material facts",
            "Lempke v. Dagenais, 130 N.H. 782 (1988) - implied warranty in new home sales",
            "Johnson v. Davis, 480 So.2d 625 (Fla. 1985) - seller's duty to disclose",
        ],
        category="transaction",
        subcategory="contract_formation",
        authority_score=0.85,
        confidence=0.88,
        related_topics=["earnest_money", "closing_procedures", "statute_of_frauds", "specific_performance"],
        practice_tips=[
            "Always include a complete legal description, not just a street address",
            "Specify whether time is of the essence or waivable",
            "Include all material contingencies (financing, inspection, appraisal)",
            "Clarify what constitutes default and available remedies",
            "Include integration clause to prevent parol evidence issues",
        ],
        risk_factors=[
            "Incomplete property description may render contract unenforceable",
            "Missing financing contingency may bind buyer without funding",
            "Oral modifications may be unenforceable under Statute of Frauds",
        ],
        texas_notes="Texas uses TREC promulgated forms for most residential transactions. Tex. Bus. & Com. Code SS 26.01 requires real estate contracts be in writing. Texas follows the four-corners rule for contract interpretation.",
    ),

    DoctrineCacheBlock(
        topic="earnest_money_deposits",
        summary="Earnest money deposits demonstrate the buyer's good faith intent to complete a purchase. The deposit is typically held in escrow by a title company or broker. If the buyer defaults, the seller may retain earnest money as liquidated damages if the contract so provides. If the seller defaults, the buyer may recover earnest money plus additional damages. Disputes over earnest money often require interpleader actions. The amount is typically 1-3% of the purchase price for residential transactions and negotiable for commercial deals.",
        key_statutes=[
            "State escrow and trust account regulations",
            "State real estate commission rules on broker handling",
            "TREC SS 535.146 (Texas earnest money handling)",
            "Tex. Prop. Code SS 5.007 (contract provisions)",
        ],
        elements=[
            "Written agreement specifying earnest money amount",
            "Deposit with designated escrow holder",
            "Clear conditions for release or forfeiture",
            "Specified contingency periods and deadlines",
            "Identification of default triggers",
            "Liquidated damages clause (if applicable)",
        ],
        defenses=[
            "Buyer exercised valid contractual contingency",
            "Seller breached contract first (anticipatory repudiation)",
            "Impossibility of performance (title defect, zoning denial)",
            "Mutual agreement to release",
            "Fraud or misrepresentation by seller",
            "Unconscionable liquidated damages clause",
        ],
        remedies=[
            "Return of earnest money deposit to buyer",
            "Forfeiture of earnest money to seller as liquidated damages",
            "Interpleader action by escrow holder",
            "Actual damages in excess of earnest money",
            "Specific performance with credit for earnest money",
        ],
        leading_cases=[
            "Kuhn v. Spatial Design Inc., 245 N.J. Super. 378 (1991) - liquidated damages vs. penalty",
            "Maxton Builders v. Lo Galbo, 68 N.Y.2d 373 (1986) - 10% earnest money as reasonable liquidated damages",
            "MCA Inc. v. Universal Diversified Enterprises, 27 Cal. App. 3d 170 (1972) - equitable principles in deposit disputes",
        ],
        category="transaction",
        subcategory="earnest_money",
        authority_score=0.75,
        confidence=0.82,
        related_topics=["real_estate_contract_formation", "closing_procedures", "breach_of_contract"],
        practice_tips=[
            "Ensure the liquidated damages clause is a reasonable estimate of anticipated harm",
            "Specify that earnest money is refundable during contingency periods",
            "Clarify the escrow holder and account details in writing",
        ],
        texas_notes="In Texas, earnest money must be deposited with the escrow agent by the close of the second business day after execution. TREC requires promulgated contract forms with specific earnest money provisions.",
    ),

    DoctrineCacheBlock(
        topic="closing_procedures",
        summary="Real estate closings involve the simultaneous exchange of deed, title, funds, and ancillary documents. The closing process requires title clearance, document preparation, proration of taxes and assessments, lender document execution, deed recording, and fund disbursement. RESPA governs disclosure of settlement costs. The Closing Disclosure (CD) must be provided at least 3 business days before closing. Escrow closings (common in western states) and table closings (common in eastern states) follow different procedural formats.",
        key_statutes=[
            "12 USC 2601-2617 (RESPA)",
            "12 CFR 1024 (Regulation X - RESPA implementation)",
            "15 USC 1601 (TILA)",
            "12 CFR 1026 (Regulation Z - TILA implementation)",
            "State recording statutes",
            "State transfer tax statutes",
        ],
        elements=[
            "Title clearance and commitment update",
            "Preparation of deed, mortgage/DOT, and ancillary documents",
            "Closing Disclosure delivery (3 business days prior)",
            "Proration of taxes, insurance, HOA dues",
            "Buyer and seller document execution",
            "Lender funding authorization",
            "Recording of deed and security instrument",
            "Disbursement of funds to all parties",
            "Issuance of title insurance policy",
        ],
        defenses=[
            "Material title defect discovered before closing",
            "Failure to deliver Closing Disclosure timely",
            "RESPA violation in settlement charges",
            "Undisclosed lien or encumbrance",
            "Survey reveals encroachment or boundary issue",
        ],
        remedies=[
            "Delay closing to cure defects",
            "Price adjustment for defects",
            "Escrow holdback for unresolved items",
            "Contract termination if defect is material",
            "RESPA penalties for disclosure violations",
            "Title insurance claim for covered defects",
        ],
        leading_cases=[
            "Freeman v. Quicken Loans Inc., 566 U.S. 624 (2012) - RESPA fee-splitting liability",
            "Jesinoski v. Countrywide Home Loans Inc., 574 U.S. 259 (2015) - TILA rescission procedure",
            "PHH Corp. v. CFPB, 881 F.3d 75 (D.C. Cir. 2018) - RESPA enforcement authority",
        ],
        category="transaction",
        subcategory="closing",
        authority_score=0.82,
        confidence=0.85,
        related_topics=["real_estate_contract_formation", "title_insurance", "respa_compliance"],
        practice_tips=[
            "Review Closing Disclosure line by line against the Loan Estimate",
            "Confirm all liens will be satisfied at closing",
            "Wire fraud prevention: verify wire instructions by phone using known numbers",
        ],
        texas_notes="Texas closings are typically conducted by title companies acting as escrow agents. Texas has no transfer tax. Community property state requires both spouses to sign conveyances of homestead.",
    ),

    # ========================================================================
    # DEED TYPES
    # ========================================================================

    DoctrineCacheBlock(
        topic="general_warranty_deed",
        summary="A general warranty deed provides the highest level of protection to the grantee, containing six traditional covenants of title: seisin, right to convey, against encumbrances, quiet enjoyment, warranty, and further assurances. The grantor warrants title against all defects, whether arising before or during the grantor's ownership. This is the standard deed for residential purchase transactions. Breach of present covenants (seisin, right to convey, against encumbrances) occurs at delivery; breach of future covenants (quiet enjoyment, warranty, further assurances) occurs when grantee's title is actually disturbed.",
        key_statutes=[
            "State recording acts (race, notice, or race-notice)",
            "State deed execution requirements",
            "Restatement (Third) of Property: Servitudes",
            "Tex. Prop. Code SS 5.022 (statutory warranty deed form)",
        ],
        elements=[
            "Competent grantor with title to convey",
            "Identifiable grantee",
            "Words of conveyance (grant, convey, transfer)",
            "Adequate property description (legal description preferred)",
            "Six covenants of title present and unqualified",
            "Grantor's signature (and spouse if required)",
            "Proper acknowledgment (notarization)",
            "Delivery and acceptance",
            "Consideration recited",
        ],
        defenses=[
            "Grantee had actual knowledge of defect at time of conveyance",
            "Statute of limitations on breach of present covenant has run",
            "Defect arose after conveyance (future covenant defense)",
            "Estoppel by deed (grantor later acquires after-acquired title)",
            "Grantee contributed to the title defect",
        ],
        remedies=[
            "Damages measured by diminution in property value",
            "Cost to cure the title defect",
            "Purchase price recovery (ceiling on present covenant damages)",
            "Defense costs if grantor must defend title",
            "Specific performance of further assurances covenant",
            "Title insurance claim (if available)",
        ],
        leading_cases=[
            "Brown v. Lober, 75 Ill.2d 547 (1979) - breach of covenant against encumbrances measured by diminution in value",
            "Rockafellor v. Gray, 194 Iowa 1280 (1922) - remote grantee can enforce warranty deed covenants",
            "Frimberger v. Anzellotti, 25 Conn. App. 401 (1991) - latent violation of land use regulation",
            "Sweeney, Administratrix v. Sweeney, 126 Conn. 391 (1940) - deed delivery and acceptance",
        ],
        category="deed",
        subcategory="general_warranty",
        authority_score=0.88,
        confidence=0.90,
        related_topics=["special_warranty_deed", "quitclaim_deed", "title_insurance", "deed_covenants"],
        practice_tips=[
            "Verify grantor has authority to convey (check corporate resolutions, trust documents, or marital status)",
            "Ensure legal description matches title commitment exactly",
            "In community property states, obtain spousal joinder even if property is separate",
        ],
        texas_notes="Tex. Prop. Code SS 5.022 provides a statutory form. In Texas, the words 'grant and convey' in a deed create a statutory special warranty unless the deed expressly includes general warranty language or the phrase 'warrant generally.'",
    ),

    DoctrineCacheBlock(
        topic="special_warranty_deed",
        summary="A special warranty deed (also called a limited warranty deed or grant deed in some states) contains warranties limited to defects arising only during the grantor's period of ownership. The grantor does NOT warrant against defects created by prior owners. This deed is standard in commercial transactions, bank-owned (REO) sales, and corporate conveyances. It provides less protection than a general warranty deed but more than a quitclaim deed. Title insurance is strongly recommended when accepting a special warranty deed.",
        key_statutes=[
            "State recording acts",
            "Tex. Prop. Code SS 5.023 (statutory special warranty form)",
            "Cal. Civ. Code SS 1113 (grant deed with statutory warranties)",
        ],
        elements=[
            "Competent grantor",
            "Identifiable grantee",
            "Words of conveyance with limited warranty language",
            "Property description",
            "Grantor's signature and acknowledgment",
            "Delivery and acceptance",
            "Warranty limited to grantor's period of ownership",
        ],
        defenses=[
            "Defect arose before grantor's ownership (pre-ownership defense)",
            "Grantee had actual knowledge of the defect",
            "Statute of limitations has expired",
            "Defect is outside the scope of the limited warranty",
        ],
        remedies=[
            "Damages for defects arising during grantor's ownership only",
            "Title insurance claim for pre-ownership defects",
            "Quiet title action against prior owners",
            "Cost to cure defects attributable to grantor",
        ],
        leading_cases=[
            "Triple Net Properties LLC v. Berk Enterprises Inc., 2009 WL 1783339 (D. Ariz.) - scope of special warranty limitations",
            "Brewer v. Herbert, 30 Md. 301 (1869) - distinction between general and special warranty",
        ],
        category="deed",
        subcategory="special_warranty",
        authority_score=0.82,
        confidence=0.85,
        related_topics=["general_warranty_deed", "quitclaim_deed", "title_insurance"],
        practice_tips=[
            "Always obtain enhanced title insurance when accepting a special warranty deed",
            "Negotiate for general warranty if seller has capacity to provide it",
            "Review chain of title for pre-ownership defects that would not be covered",
        ],
        texas_notes="In Texas, the statutory form under Tex. Prop. Code SS 5.023 uses 'grant and convey' which creates a special warranty by operation of law.",
    ),

    DoctrineCacheBlock(
        topic="quitclaim_deed",
        summary="A quitclaim deed transfers whatever interest the grantor may have in the property, with NO warranties or covenants of title. The grantor does not even warrant that they have any interest to convey. Quitclaim deeds are commonly used for inter-family transfers, divorce property settlements, clearing clouds on title, transferring property into or out of trusts, and correcting errors in prior deeds. They are NOT suitable for purchase transactions. A bona fide purchaser who acquires title via quitclaim may not qualify for recording act protection in some jurisdictions.",
        key_statutes=[
            "State recording acts",
            "State deed execution requirements",
            "Tex. Prop. Code SS 13.001 (recording requirements)",
        ],
        elements=[
            "Grantor signature and acknowledgment",
            "Grantee identification",
            "Property description",
            "Words of conveyance (quitclaim, release, remise)",
            "Delivery and acceptance",
            "No covenants of title required or implied",
        ],
        defenses=[
            "Grantor had no interest to convey (no damages because no warranty)",
            "Grantee assumed all title risk by accepting quitclaim",
            "No reliance on warranty representations",
        ],
        remedies=[
            "No covenant-based remedies (no warranties to breach)",
            "Possible fraud claim if grantor misrepresented their interest",
            "Quiet title action to establish grantee's interest",
            "Title insurance claim if policy was obtained",
        ],
        leading_cases=[
            "Luthi v. Evans, 223 Kan. 622 (1978) - recording act and mother hubbard clauses in quitclaim",
            "Orr v. Byers, 198 Cal. App. 3d 666 (1988) - quitclaim grantee may not qualify as BFP in some jurisdictions",
        ],
        category="deed",
        subcategory="quitclaim",
        authority_score=0.78,
        confidence=0.85,
        related_topics=["general_warranty_deed", "special_warranty_deed", "quiet_title_action"],
        practice_tips=[
            "Never accept a quitclaim deed in a purchase transaction without title insurance",
            "Use quitclaim deeds to clear clouds on title from deceased persons or corrective conveyances",
            "Verify the quitclaim deed is properly acknowledged and recorded",
        ],
        texas_notes="Texas recognizes quitclaim deeds but they do not imply any warranties. A Texas quitclaim grantee may not qualify as a good-faith purchaser under the recording statute.",
    ),

    DoctrineCacheBlock(
        topic="deed_of_trust",
        summary="A deed of trust is a three-party security instrument where the borrower (trustor) conveys legal title to a trustee to hold as security for a loan from the lender (beneficiary). Unlike a mortgage, the deed of trust typically includes a power of sale clause allowing non-judicial foreclosure. The trustee holds bare legal title until the loan is satisfied (reconveyance) or the borrower defaults (foreclosure sale). Deeds of trust are the standard security instrument in Texas, California, and many other states.",
        key_statutes=[
            "Tex. Prop. Code SS 51.002 (Texas non-judicial foreclosure)",
            "Cal. Civ. Code SS 2924 (California foreclosure procedures)",
            "State specific deed of trust recording requirements",
            "12 USC 2601 (RESPA applicability to DOT)",
        ],
        elements=[
            "Three parties: trustor (borrower), trustee (neutral third party), beneficiary (lender)",
            "Conveyance of legal title to trustee",
            "Promissory note evidencing the debt secured",
            "Property description matching note",
            "Power of sale clause (enabling non-judicial foreclosure)",
            "Acceleration clause",
            "Due-on-sale clause (Garn-St Germain exemptions apply)",
            "Recording in county where property is located",
        ],
        defenses=[
            "Lack of valid underlying debt (note deficiency)",
            "Statute of limitations on the note or foreclosure",
            "Failure to provide required notices before foreclosure",
            "Standing challenge (broken chain of assignments)",
            "TILA rescission right (within applicable period)",
            "Bankruptcy automatic stay (11 USC 362)",
        ],
        remedies=[
            "Non-judicial foreclosure via power of sale (trustee sale)",
            "Judicial foreclosure if power of sale not available",
            "Deficiency judgment (where permitted by state law)",
            "Appointment of receiver for income-producing property",
            "Assignment of rents",
        ],
        leading_cases=[
            "Garn-St Germain Depository Institutions Act of 1982 - due on sale clause limitations",
            "Yvanova v. New Century Mortgage Corp., 62 Cal.4th 919 (2016) - borrower standing to challenge void assignment",
            "Carpenter v. Longan, 83 U.S. 271 (1872) - mortgage follows the note",
        ],
        category="deed",
        subcategory="deed_of_trust",
        authority_score=0.85,
        confidence=0.88,
        related_topics=["foreclosure_non_judicial", "mortgage", "promissory_note"],
        practice_tips=[
            "Verify the trustee is a qualified entity under state law",
            "Ensure the deed of trust is recorded after or simultaneously with the deed",
            "Confirm power of sale language complies with state requirements",
        ],
        texas_notes="Texas is a deed of trust state. Non-judicial foreclosure under Tex. Prop. Code SS 51.002 requires at least 21 days notice before the sale, which occurs on the first Tuesday of the month.",
    ),

    # ========================================================================
    # TITLE EXAMINATION AND INSURANCE
    # ========================================================================

    DoctrineCacheBlock(
        topic="title_examination",
        summary="Title examination is the process of reviewing the chain of title in public records to determine the current state of ownership and identify encumbrances, liens, easements, and other interests affecting the property. A full title search typically covers at least 40-60 years of records. Title examiners review deed records, mortgage records, judgment records, tax records, probate records, and other public filings. Title opinions are rendered by attorneys and form the basis for title insurance commitments. The three types of recording statutes (race, notice, race-notice) determine priority among competing claimants.",
        key_statutes=[
            "State recording statutes (race, notice, or race-notice)",
            "State title standards (bar association adopted)",
            "ALTA Title Insurance Forms",
            "Tex. Prop. Code Ch. 12 (Recording)",
            "Tex. Ins. Code Ch. 2501 (Title Insurance)",
        ],
        elements=[
            "Examination of grantor-grantee indices",
            "Chain of title continuity verification",
            "Encumbrance identification (liens, mortgages, judgments)",
            "Easement and covenant identification",
            "Tax lien status verification",
            "Probate and estate proceeding review",
            "Bankruptcy filing search",
            "Judgment and lis pendens search",
            "Survey review for boundary and encroachment issues",
            "Plat and subdivision compliance verification",
        ],
        defenses=[
            "Bona fide purchaser for value without notice (BFP)",
            "Recording statute priority under applicable state type",
            "Marketable title act (in applicable states)",
            "Statute of limitations on stale claims",
            "Laches barring delayed enforcement",
            "Merger doctrine (lesser estate merges into greater)",
        ],
        remedies=[
            "Quiet title action to remove clouds",
            "Title insurance claim for covered defects",
            "Damages against title examiner for negligent search",
            "Reformation of instruments with errors",
            "Declaratory judgment on priority disputes",
            "Affidavit of heirship to establish succession",
        ],
        leading_cases=[
            "Luthi v. Evans, 223 Kan. 622 (1978) - mother hubbard clause insufficient for constructive notice",
            "Guillette v. Daly Dry Wall Inc., 367 Mass. 355 (1975) - inquiry notice from visible use of property",
            "Mugaas v. Smith, 33 Wn.2d 429 (1949) - adverse possession and title examination",
            "Board of Education v. Hughes, 118 Minn. 404 (1912) - recording act protection for subsequent purchasers",
        ],
        category="title",
        subcategory="examination",
        authority_score=0.88,
        confidence=0.90,
        related_topics=["title_insurance", "encumbrances", "liens", "recording_acts"],
        practice_tips=[
            "Always perform a gap search (update) between commitment and closing",
            "Verify legal description in deed matches the title commitment Schedule A",
            "Check for unreleased liens even if they appear paid",
        ],
        texas_notes="Texas is a race-notice jurisdiction. The Texas Department of Insurance regulates title insurance rates (promulgated rates). Title companies act as both title examiner and closing agent.",
    ),

    DoctrineCacheBlock(
        topic="title_insurance",
        summary="Title insurance protects against loss from defects in title that were not discovered during the title examination. There are two primary types: owner's policies (protect the buyer) and lender's policies (protect the mortgagee). ALTA forms are the national standard. Title insurance is a one-time premium paid at closing and coverage continues as long as the insured or their heirs have an interest. Title insurance differs from other insurance in that it is retrospective (insuring against past events) rather than prospective. Standard exceptions are listed in Schedule B and can often be removed by survey, inspection, or affidavit.",
        key_statutes=[
            "State title insurance regulations",
            "ALTA Owner's Policy (2006, amended)",
            "ALTA Loan Policy (2006, amended)",
            "Tex. Ins. Code Ch. 2501-2551 (Texas Title Insurance Act)",
            "ALTA Endorsement Forms",
        ],
        elements=[
            "Written application for title insurance",
            "Title examination and commitment issuance",
            "Schedule A: insured, property description, policy amount",
            "Schedule B-I: requirements to be met before policy issuance",
            "Schedule B-II: exceptions from coverage",
            "Premium payment (one-time, at closing)",
            "Closing of the transaction",
            "Recording of insured instrument",
            "Policy issuance (typically 30-60 days post-closing)",
        ],
        defenses=[
            "Exception listed in Schedule B of the policy",
            "Known defect excluded from coverage",
            "Failure to provide timely notice of claim",
            "Post-policy defects (not covered by basic policy)",
            "Government action or eminent domain (may be excluded)",
            "Voluntary encumbrance by the insured",
        ],
        remedies=[
            "Payment of claim up to policy amount",
            "Defense of insured's title at insurer's expense",
            "Cure of the defect by the insurer",
            "Purchase of the adverse interest",
            "Endorsement adding coverage for newly discovered matters",
            "Bad faith claim against insurer for unreasonable denial",
        ],
        leading_cases=[
            "Citibank N.A. v. Chicago Title Ins. Co., 214 F.Supp.3d 1261 (S.D. Fla. 2016) - scope of lender policy coverage",
            "Stewart Title Guar. Co. v. Cheatham, 198 S.W.3d 4 (Tex. App. 2006) - duty to defend under title policy",
            "Gates v. Chicago Title Ins. Co., 813 S.W.2d 10 (Mo. App. 1991) - measure of title insurance damages",
        ],
        category="title",
        subcategory="insurance",
        authority_score=0.85,
        confidence=0.87,
        related_topics=["title_examination", "encumbrances", "closing_procedures"],
        practice_tips=[
            "Request deletion of standard exceptions by providing survey and affidavit",
            "Consider enhanced (homeowner's) policy for additional coverage",
            "Compare Schedule B exceptions to actual survey for conflicts",
        ],
        texas_notes="Texas has promulgated (fixed) title insurance rates set by the Texas Department of Insurance. The rate is the same regardless of which title company is used. Basic owner's and loan policies plus endorsements are regulated.",
    ),

    # ========================================================================
    # EASEMENTS AND COVENANTS
    # ========================================================================

    DoctrineCacheBlock(
        topic="express_easements",
        summary="An express easement is created by a written instrument, typically a deed or a separate easement agreement, and must satisfy the Statute of Frauds. It grants a non-possessory right to use another's land for a specific purpose. Express easements may be appurtenant (benefiting a dominant estate) or in gross (benefiting a person or entity). The scope is determined by the language of the grant, the circumstances at creation, and reasonable necessity. Ambiguous easement language is construed in favor of the grantee for easements created by grant, and in favor of the grantor for easements created by reservation.",
        key_statutes=[
            "State Statute of Frauds",
            "Restatement (Third) of Property: Servitudes SS 4.1",
            "State recording acts (easement must be recorded for notice)",
            "Tex. Prop. Code SS 5.021 (conveyance requirements)",
        ],
        elements=[
            "Written instrument (grant or reservation)",
            "Identification of dominant and servient estates (if appurtenant)",
            "Description of the easement location and scope",
            "Signature of the grantor (or reserving party)",
            "Proper acknowledgment and recording",
            "Consideration (though nominal consideration may suffice)",
            "Delivery and acceptance",
        ],
        defenses=[
            "Easement scope exceeded by dominant owner (overburdening)",
            "Changed conditions rendering easement unnecessary or impracticable",
            "Abandonment (intent plus nonuse over substantial period)",
            "Merger of dominant and servient estates",
            "Estoppel (acquiescence to interference)",
            "Statute of limitations on enforcement",
        ],
        remedies=[
            "Injunctive relief to prevent interference with or overburdening of easement",
            "Damages for interference with easement rights",
            "Declaratory judgment on scope and location",
            "Quiet title to establish or extinguish easement",
            "Relocation of easement by agreement or court order",
        ],
        leading_cases=[
            "Othen v. Rosier, 226 S.W.2d 484 (Tex. 1950) - easement by necessity and implied easement",
            "Cameron v. Barton, 272 S.W.2d 40 (Tex. Civ. App. 1954) - scope of express easement",
            "Restatement (Third) of Property: Servitudes SS 4.8 - relocation of easements",
        ],
        category="easement",
        subcategory="express",
        authority_score=0.82,
        confidence=0.86,
        related_topics=["prescriptive_easement", "easement_by_necessity", "conservation_easement", "restrictive_covenants"],
        practice_tips=[
            "Draft easement language with specificity regarding location, width, and permitted uses",
            "Include maintenance obligations for both dominant and servient owners",
            "Record the easement in the county where the servient estate is located",
        ],
        texas_notes="Texas recognizes all standard easement types. Express easements must satisfy the Statute of Frauds. Oil and gas surface easements are common given the split estate doctrine.",
    ),

    DoctrineCacheBlock(
        topic="prescriptive_easement",
        summary="A prescriptive easement is acquired through continuous, open, notorious, hostile, and adverse use of another's property for the statutory prescriptive period (typically 5-20 years depending on the state). Unlike adverse possession, prescriptive easement does not require payment of property taxes or exclusive possession. The claimant must prove use that would put a reasonable landowner on notice. Permissive use defeats a prescriptive claim. Government land is typically immune from prescriptive easement claims.",
        key_statutes=[
            "State prescriptive period statutes (varies: 5-20 years)",
            "Tex. Civ. Prac. & Rem. Code SS 16.026 (10-year adverse possession period used for prescriptive easement)",
            "Restatement (Third) of Property: Servitudes SS 2.16-2.17",
        ],
        elements=[
            "Open and notorious use (visible to a reasonable owner)",
            "Continuous use for the statutory prescriptive period",
            "Hostile and adverse use (without permission)",
            "Use under claim of right (some jurisdictions)",
            "Use is not merely permissive or licensed",
            "Defined and identifiable use area",
        ],
        defenses=[
            "Use was permissive (license, oral agreement, neighborly accommodation)",
            "Statutory period not satisfied (interruption resets the clock)",
            "Property is government-owned (immune in most states)",
            "Use was secret or not visible to owner",
            "Owner interrupted use or posted no-trespass signs",
            "Tacking not available (different users without privity)",
        ],
        remedies=[
            "Declaratory judgment establishing prescriptive easement",
            "Injunction against interference with established prescriptive use",
            "Quiet title incorporating prescriptive easement",
            "Damages for interference after easement established",
        ],
        leading_cases=[
            "Warsaw v. Chicago Metallic Ceilings Inc., 35 Cal.3d 564 (1984) - elements of prescriptive easement",
            "MacDonald Properties v. Volunteer Fire Co., 141 Cal.App.3d 595 (1983) - permissive use vs. prescriptive use",
            "Othen v. Rosier, 226 S.W.2d 484 (Tex. 1950) - prescriptive easement requirements in Texas",
        ],
        category="easement",
        subcategory="prescriptive",
        authority_score=0.80,
        confidence=0.82,
        related_topics=["adverse_possession", "express_easements", "easement_by_necessity"],
        practice_tips=[
            "Document all uses of your property by neighbors to establish permissive basis",
            "Post signs or send written notice denying permission to interrupt prescriptive period",
            "Survey property to identify potential prescriptive use areas before purchase",
        ],
        texas_notes="Texas courts apply the 10-year adverse possession statute by analogy. Prescriptive easements are recognized but disfavored in Texas. The Texas Supreme Court requires clear and convincing evidence.",
    ),

    DoctrineCacheBlock(
        topic="restrictive_covenants",
        summary="Restrictive covenants (also called deed restrictions or CC&Rs) are promises that limit how land may be used. They run with the land if they touch and concern the land, the original parties intended them to run, and subsequent purchasers have notice (actual, constructive, or inquiry). Equitable servitudes are enforceable in equity even if they do not technically satisfy the requirements for real covenants. Common restrictions include use limitations, architectural requirements, setback requirements, and prohibitions on certain activities. Changed conditions may render restrictions unenforceable.",
        key_statutes=[
            "Restatement (Third) of Property: Servitudes SS 3.1-3.7",
            "State covenant and restriction statutes",
            "Tex. Prop. Code Ch. 202 (Property Owners Associations)",
            "Tex. Prop. Code Ch. 209 (Texas Residential POA Act)",
            "42 USC 3604 (Fair Housing Act - unenforceable discriminatory covenants)",
        ],
        elements=[
            "Written instrument creating the restriction",
            "Intent to bind successors (running with the land)",
            "Touch and concern the land",
            "Privity of estate (horizontal and vertical for real covenants at law)",
            "Notice to subsequent purchasers (constructive via recording)",
            "Benefit and burden identifiable",
        ],
        defenses=[
            "Changed conditions rendering restriction unenforceable (neighborhood changed)",
            "Abandonment or waiver (widespread violations without enforcement)",
            "Unclean hands (enforcing party also violates restrictions)",
            "Laches (unreasonable delay in enforcement)",
            "Estoppel (party relied on non-enforcement)",
            "Restraint on alienation (unreasonable restrictions on transferability)",
            "Discriminatory covenant (unconstitutional under 14th Amendment and Fair Housing Act)",
            "Expiration of the covenant term",
            "Relative hardship (enforcement causes disproportionate harm)",
        ],
        remedies=[
            "Injunctive relief (mandatory or prohibitory)",
            "Damages for covenant violation",
            "Declaratory judgment on covenant validity and scope",
            "Modification or termination by court",
            "HOA enforcement (fines, liens, legal action)",
        ],
        leading_cases=[
            "Shelley v. Kraemer, 334 U.S. 1 (1948) - judicial enforcement of racial covenants is state action violating 14th Amendment",
            "Nahrstedt v. Lakeside Village Condo Assn., 8 Cal.4th 361 (1994) - reasonableness standard for CC&R enforcement",
            "Neponsit Property Owners Assn. v. Emigrant Bank, 278 N.Y. 248 (1938) - touch and concern requirement for running covenants",
            "Rick v. West, 228 N.Y.S.2d 195 (Sup. Ct. 1962) - single lot owner can enforce restriction against developer",
        ],
        category="easement",
        subcategory="restrictive_covenants",
        authority_score=0.85,
        confidence=0.87,
        related_topics=["hoa_governance", "zoning_regulation", "fair_housing"],
        practice_tips=[
            "Review all recorded restrictions before purchasing property",
            "Determine if there is a property owners association with enforcement authority",
            "Check for expiration dates and amendment procedures in the declaration",
        ],
        texas_notes="Texas aggressively enforces deed restrictions. Tex. Prop. Code Ch. 202 and 209 govern POA restrictions and enforcement. Texas does not require strict privity for enforcement of equitable servitudes.",
    ),

    # ========================================================================
    # ZONING AND LAND USE
    # ========================================================================

    DoctrineCacheBlock(
        topic="zoning_regulation",
        summary="Zoning is the primary tool for local governments to regulate land use, exercised under the police power. Zoning ordinances divide a municipality into districts with permitted, conditional, and prohibited uses. Euclidean (cumulative) zoning is the traditional model, while modern approaches include form-based codes, overlay districts, and incentive zoning. Zoning must be substantially related to the health, safety, morals, or general welfare. Non-conforming uses are typically grandfathered but may not be expanded. Variances and special exceptions provide flexibility but require specific findings.",
        key_statutes=[
            "State enabling statutes (based on Standard Zoning Enabling Act of 1926)",
            "State planning and zoning codes",
            "Tex. Loc. Gov. Code Ch. 211 (Municipal Zoning Authority)",
            "Tex. Loc. Gov. Code Ch. 232 (County Subdivision Regulation)",
            "U.S. Constitution, Fifth and Fourteenth Amendments (Takings and Due Process)",
        ],
        elements=[
            "Authorized by state enabling legislation",
            "Enacted by local legislative body (city council, commissioners court)",
            "Consistent with comprehensive plan (in most states)",
            "Proper notice and public hearing procedures",
            "Reasonable classification of districts and uses",
            "Substantially related to health, safety, morals, or general welfare",
            "Not arbitrary, capricious, or discriminatory",
        ],
        defenses=[
            "Vested rights (substantial reliance on prior zoning approval)",
            "Non-conforming use (lawfully established before zoning change)",
            "Regulatory taking (goes too far under Penn Central)",
            "Substantive due process violation (no rational basis)",
            "Equal protection violation (discriminatory application)",
            "Estoppel (government induced reliance)",
            "First Amendment (religious land use under RLUIPA)",
        ],
        remedies=[
            "Variance application (area or use variance)",
            "Conditional use permit application",
            "Rezoning petition to legislative body",
            "Comprehensive plan amendment request",
            "Judicial challenge (mandamus, certiorari, declaratory judgment)",
            "Inverse condemnation claim for regulatory taking",
            "RLUIPA claim for religious land use denial",
        ],
        leading_cases=[
            "Village of Euclid v. Ambler Realty Co., 272 U.S. 365 (1926) - constitutionality of zoning",
            "Penn Central Transportation Co. v. City of New York, 438 U.S. 104 (1978) - regulatory takings balancing test",
            "Nollan v. California Coastal Commission, 483 U.S. 825 (1987) - essential nexus for exactions",
            "Dolan v. City of Tigard, 512 U.S. 374 (1994) - rough proportionality for exactions",
            "Koontz v. St. Johns River Water Mgmt. Dist., 570 U.S. 595 (2013) - monetary exactions subject to Nollan/Dolan",
        ],
        category="zoning",
        subcategory="general_regulation",
        authority_score=0.90,
        confidence=0.90,
        related_topics=["variance", "conditional_use", "regulatory_taking", "eminent_domain"],
        practice_tips=[
            "Always verify current zoning classification before purchasing property",
            "Review the comprehensive plan for potential future zoning changes",
            "Obtain a zoning letter or certification from the local planning department",
        ],
        texas_notes="Texas does not have county zoning authority in unincorporated areas (except in limited ETJ circumstances). Texas cities have broad zoning power under Tex. Loc. Gov. Code Ch. 211. Houston is the only major US city without traditional zoning but uses deed restrictions and development regulations.",
    ),

    DoctrineCacheBlock(
        topic="regulatory_taking",
        summary="A regulatory taking occurs when government regulation goes 'too far' in restricting the use of private property, requiring just compensation under the Fifth Amendment. The Penn Central balancing test considers: (1) the economic impact on the owner, (2) the extent of interference with investment-backed expectations, and (3) the character of the government action. A per se taking exists under Lucas when regulation deprives the owner of ALL economically viable use. Physical invasions of any size are per se takings under Loretto. Exactions must have an essential nexus (Nollan) and rough proportionality (Dolan) to the development impact.",
        key_statutes=[
            "U.S. Constitution, Fifth Amendment ('nor shall private property be taken for public use, without just compensation')",
            "U.S. Constitution, Fourteenth Amendment (incorporation to states)",
            "42 USC 1983 (civil rights action for constitutional violation)",
            "State takings clauses (may provide broader protection)",
            "Tex. Gov. Code Ch. 2007 (Texas Private Real Property Rights Preservation Act)",
        ],
        elements=[
            "Government action (legislative, regulatory, or physical)",
            "Burden on private property rights",
            "Penn Central factors: economic impact, investment-backed expectations, character of action",
            "Lucas per se test: denial of all economically viable use",
            "Loretto per se test: permanent physical invasion",
            "Nollan/Dolan for exactions: nexus and proportionality",
            "Ripeness (final decision + state compensation remedy sought)",
        ],
        defenses=[
            "Regulation addresses nuisance or background principles of property law (Lucas exception)",
            "Property owner acquired with knowledge of the restriction",
            "No final decision on permit application (ripeness)",
            "Adequate state compensation remedy available (Williamson County, now modified by Knick)",
            "Regulation substantially advances a legitimate state interest",
            "Property retains economically viable use (Penn Central)",
            "Average reciprocity of advantage",
        ],
        remedies=[
            "Just compensation (fair market value at time of taking)",
            "Inverse condemnation judgment",
            "Injunctive relief against unconstitutional regulation",
            "Declaratory judgment",
            "42 USC 1983 damages for constitutional violation",
            "Attorney's fees under 42 USC 1988",
        ],
        leading_cases=[
            "Penn Central Transportation Co. v. City of New York, 438 U.S. 104 (1978) - balancing test for regulatory takings",
            "Lucas v. South Carolina Coastal Council, 505 U.S. 1003 (1992) - total deprivation per se taking",
            "Loretto v. Teleprompter Manhattan CATV Corp., 458 U.S. 419 (1982) - physical invasion per se taking",
            "Palazzolo v. Rhode Island, 533 U.S. 606 (2001) - notice of restriction does not bar takings claim",
            "Kelo v. City of New London, 545 U.S. 469 (2005) - economic development qualifies as public use",
            "Knick v. Township of Scott, 588 U.S. 180 (2019) - no state compensation remedy prerequisite for federal court",
            "Cedar Point Nursery v. Hassid, 594 U.S. 139 (2021) - access regulation as per se physical taking",
        ],
        category="zoning",
        subcategory="regulatory_taking",
        authority_score=0.92,
        confidence=0.88,
        related_topics=["eminent_domain", "zoning_regulation", "inverse_condemnation"],
        practice_tips=[
            "Document pre-regulation property value and permitted uses for comparison",
            "Exhaust administrative remedies before filing takings claim",
            "Consider whether a Lucas per se claim is available before relying on Penn Central",
        ],
        texas_notes="Texas has the Private Real Property Rights Preservation Act (Tex. Gov. Code Ch. 2007) which provides additional protections beyond federal takings law. Government action that reduces property value by 25% or more triggers analysis.",
    ),

    # ========================================================================
    # LANDLORD-TENANT
    # ========================================================================

    DoctrineCacheBlock(
        topic="landlord_tenant_law",
        summary="Landlord-tenant law governs the relationship between property owners (landlords) and occupants (tenants) under lease agreements. Key concepts include the implied warranty of habitability (residential), duty to mitigate damages, security deposit regulations, eviction procedures, and lease termination. Commercial leases are generally governed by freedom of contract with less statutory protection for tenants. Lease types include gross, net, triple-net (NNN), percentage, and ground leases. Assignment and subletting rights depend on lease provisions and state law.",
        key_statutes=[
            "Tex. Prop. Code Ch. 91-93 (Texas Landlord-Tenant Law)",
            "Tex. Prop. Code SS 92.101-92.109 (Security Deposits)",
            "Tex. Prop. Code SS 92.051-92.062 (Repair Obligations)",
            "Tex. Prop. Code SS 24.001-24.011 (Forcible Entry and Detainer)",
            "Uniform Residential Landlord and Tenant Act (URLTA)",
            "42 USC 3604 (Fair Housing Act)",
        ],
        elements=[
            "Valid lease agreement (written or oral, depending on term)",
            "Identification of parties, premises, and term",
            "Rent amount and payment terms",
            "Security deposit amount and conditions for refund",
            "Maintenance and repair obligations",
            "Rules regarding assignment, subletting, and modification",
            "Termination and renewal provisions",
            "Compliance with Fair Housing Act (no discrimination in protected classes)",
        ],
        defenses=[
            "Implied warranty of habitability violation (residential)",
            "Constructive eviction (landlord's breach makes premises uninhabitable)",
            "Retaliatory eviction (tenant exercised legal right)",
            "Failure to mitigate damages after tenant abandonment",
            "Improper notice for lease termination or rent increase",
            "Fair Housing Act violation in lease enforcement",
            "Waiver of landlord's right by acceptance of rent after breach",
            "Frustration of purpose or impossibility",
        ],
        remedies=[
            "Eviction (forcible entry and detainer action)",
            "Damages for unpaid rent",
            "Repair and deduct (residential, where permitted by statute)",
            "Rent withholding (where permitted by statute)",
            "Security deposit return or forfeiture",
            "Lease termination for material breach",
            "Injunctive relief against nuisance or illegal activity",
            "Statutory penalties for security deposit violations",
        ],
        leading_cases=[
            "Javins v. First National Realty Corp., 428 F.2d 1071 (D.C. Cir. 1970) - implied warranty of habitability",
            "Reste Realty Corp. v. Cooper, 53 N.J. 444 (1969) - constructive eviction and implied warranty",
            "Ernst v. Conditt, 54 Tenn. App. 328 (1964) - assignment vs. sublease distinction",
            "Sommer v. Kridel, 74 N.J. 446 (1977) - landlord's duty to mitigate damages",
        ],
        category="landlord_tenant",
        subcategory="general",
        authority_score=0.82,
        confidence=0.85,
        related_topics=["eviction", "security_deposit", "commercial_lease", "fair_housing"],
        practice_tips=[
            "Always use a written lease, even for month-to-month tenancies",
            "Document property condition at move-in and move-out with photographs",
            "Know your state's specific security deposit return deadline and procedures",
        ],
        texas_notes="Texas does NOT recognize the implied warranty of habitability by judicial decision. Instead, Tex. Prop. Code SS 92.052 imposes a statutory duty to repair conditions affecting health or safety after proper notice. Security deposits must be returned within 30 days of move-out with an itemized list of deductions.",
    ),

    DoctrineCacheBlock(
        topic="eviction_procedures",
        summary="Eviction (forcible entry and detainer) is the legal process by which a landlord recovers possession of leased premises from a tenant. The process typically requires: (1) notice to the tenant (type and duration vary by reason and jurisdiction), (2) filing a legal action if tenant does not vacate, (3) court hearing, (4) judgment, and (5) writ of possession for physical removal by a constable or sheriff. Self-help eviction (changing locks, removing property, shutting off utilities) is illegal in virtually all states. COVID-era moratoriums significantly affected eviction procedures but have largely expired.",
        key_statutes=[
            "Tex. Prop. Code SS 24.001-24.011 (Forcible Entry and Detainer)",
            "Tex. Prop. Code SS 91.001 (Notice Requirements)",
            "State eviction procedure statutes",
            "Federal CARES Act SS 4024 (expired moratorium)",
            "42 USC 3604 (Fair Housing Act - discriminatory eviction)",
        ],
        elements=[
            "Proper grounds for eviction (nonpayment, lease violation, holdover, no-fault)",
            "Written notice to vacate (type and period per state law)",
            "Filing of eviction action (justice court in Texas)",
            "Service of process on tenant",
            "Court hearing with opportunity for tenant defense",
            "Judgment for possession (and unpaid rent if applicable)",
            "Writ of possession for physical removal",
            "Compliance with Fair Housing Act throughout process",
        ],
        defenses=[
            "Improper or insufficient notice to vacate",
            "Retaliatory eviction (tenant reported code violation or exercised legal right)",
            "Discriminatory eviction (Fair Housing Act violation)",
            "Landlord failed to maintain habitable premises",
            "Rent was tendered and refused",
            "Waiver by acceptance of rent after knowledge of breach",
            "Procedural defect in eviction filing or service",
            "Bankruptcy automatic stay",
        ],
        remedies=[
            "Judgment for possession in favor of landlord",
            "Writ of possession and physical removal by peace officer",
            "Money judgment for unpaid rent and damages",
            "Tenant counterclaim for wrongful eviction",
            "Fair Housing Act damages for discriminatory eviction",
            "Statutory damages for illegal self-help eviction (lock-out)",
        ],
        leading_cases=[
            "Lindsey v. Normet, 405 U.S. 56 (1972) - due process in eviction proceedings",
            "Robinson v. Diamond Housing Corp., 463 F.2d 853 (D.C. Cir. 1972) - retaliatory eviction",
        ],
        category="landlord_tenant",
        subcategory="eviction",
        authority_score=0.80,
        confidence=0.84,
        related_topics=["landlord_tenant_law", "security_deposit", "fair_housing"],
        practice_tips=[
            "Strictly follow notice-to-vacate timing and delivery requirements",
            "Document all lease violations with dates, photos, and written warnings",
            "Never engage in self-help eviction (lock changes, utility shutoffs)",
        ],
        texas_notes="Texas evictions are heard in Justice Court (JP Court). A 3-day notice to vacate is required for nonpayment (unless the lease specifies otherwise, but cannot be less than 1 day). Appeal from JP to county court requires posting a supersedeas bond.",
    ),

    # ========================================================================
    # EMINENT DOMAIN
    # ========================================================================

    DoctrineCacheBlock(
        topic="eminent_domain",
        summary="Eminent domain is the government's power to take private property for public use upon payment of just compensation, as guaranteed by the Fifth Amendment. The condemning authority must demonstrate: (1) the taking serves a public use or public purpose, (2) the property owner receives just compensation (fair market value), (3) due process is provided, and (4) the taking is necessary. After Kelo, economic development can qualify as public use, though many states enacted anti-Kelo legislation limiting this power. Condemnation proceedings involve appraisals, negotiations, special commissioners or jury trials, and appeals.",
        key_statutes=[
            "U.S. Constitution, Fifth Amendment",
            "Tex. Gov. Code Ch. 2206 (Texas anti-Kelo statute)",
            "Tex. Prop. Code Ch. 21 (Eminent Domain procedures)",
            "State eminent domain statutes",
            "42 USC 4601 (Uniform Relocation Assistance Act)",
        ],
        elements=[
            "Condemning authority with proper statutory power",
            "Public use or public purpose for the taking",
            "Just compensation (fair market value)",
            "Due process notice and opportunity to be heard",
            "Necessity of the specific property for the public purpose",
            "Good faith negotiation before condemnation (required in most states)",
            "Compliance with state-specific procedural requirements",
        ],
        defenses=[
            "No public use or public purpose (pretextual taking)",
            "Compensation offered is not just (insufficient valuation)",
            "Condemning authority lacks statutory power",
            "Procedural defects in condemnation process",
            "Taking more property than reasonably necessary",
            "Discrimination in property selection (Equal Protection)",
            "State anti-Kelo statute prohibits economic development taking",
            "First Amendment (religious property - RLUIPA considerations)",
        ],
        remedies=[
            "Jury trial on just compensation amount",
            "Severance damages for remaining property after partial taking",
            "Relocation assistance under federal or state law",
            "Challenge to public use determination",
            "Inverse condemnation claim for de facto taking",
            "Attorney's fees (in some states when government offer is substantially below award)",
            "Precondemnation damages for government interference before formal taking",
        ],
        leading_cases=[
            "Kelo v. City of New London, 545 U.S. 469 (2005) - economic development as public use",
            "United States v. 564.54 Acres of Land, 441 U.S. 506 (1979) - substitute facilities method rejected",
            "Almota Farmers Elevator v. United States, 409 U.S. 470 (1973) - value of leasehold interest",
            "City of Monterey v. Del Monte Dunes, 526 U.S. 687 (1999) - damages for regulatory taking",
        ],
        category="eminent_domain",
        subcategory="condemnation",
        authority_score=0.90,
        confidence=0.88,
        related_topics=["regulatory_taking", "just_compensation", "inverse_condemnation"],
        practice_tips=[
            "Hire an independent appraiser immediately upon receiving notice of condemnation",
            "Document all business damages and relocation costs",
            "Challenge the necessity finding if the property is not essential to the project",
        ],
        texas_notes="Texas has strong anti-Kelo protections under Tex. Gov. Code Ch. 2206, prohibiting takings solely for economic development. Texas condemnation uses special commissioners for initial hearing, with appeal to county court at law for jury trial.",
    ),

    # ========================================================================
    # REAL ESTATE FINANCING
    # ========================================================================

    DoctrineCacheBlock(
        topic="real_estate_financing",
        summary="Real estate financing encompasses the full range of debt instruments used to acquire or improve real property, including conventional mortgages, FHA/VA/USDA government-backed loans, jumbo loans, hard money loans, seller financing, and construction loans. The primary regulatory framework includes RESPA (settlement procedures), TILA (truth in lending), ECOA (equal credit opportunity), HMDA (mortgage disclosure), and the Dodd-Frank Act. Lenders must provide a Loan Estimate within 3 business days of application and a Closing Disclosure 3 business days before closing.",
        key_statutes=[
            "12 USC 2601-2617 (RESPA)",
            "15 USC 1601 (TILA)",
            "15 USC 1691 (ECOA)",
            "12 USC 2801 (HMDA)",
            "Dodd-Frank Wall Street Reform and Consumer Protection Act",
            "12 CFR 1024 (Regulation X)",
            "12 CFR 1026 (Regulation Z)",
            "12 USC 3801 (Garn-St Germain - due-on-sale clause limitation)",
        ],
        elements=[
            "Loan application and origination",
            "Ability-to-repay (ATR) determination under Dodd-Frank",
            "Loan Estimate delivery within 3 business days of application",
            "Appraisal and property valuation",
            "Underwriting and credit analysis",
            "Closing Disclosure delivery 3 business days before closing",
            "Execution of promissory note and security instrument",
            "Recording of mortgage or deed of trust",
            "Loan servicing and payment collection",
        ],
        defenses=[
            "TILA rescission right (3 days or extended for disclosure violations)",
            "RESPA settlement charge violations",
            "ECOA discrimination in credit decision",
            "Predatory lending practices",
            "Failure to provide required disclosures",
            "Qualified mortgage (QM) safe harbor defense for lenders",
            "Statute of limitations on TILA/RESPA claims",
        ],
        remedies=[
            "TILA rescission of the loan transaction",
            "RESPA statutory and actual damages",
            "ECOA actual and punitive damages",
            "Loan modification or restructuring",
            "Borrower defense to repayment",
            "Class action for pattern of disclosure violations",
            "CFPB enforcement action",
        ],
        leading_cases=[
            "Jesinoski v. Countrywide Home Loans Inc., 574 U.S. 259 (2015) - TILA rescission by notice",
            "Freeman v. Quicken Loans Inc., 566 U.S. 624 (2012) - RESPA fee-splitting requires two or more parties",
            "PHH Corp. v. CFPB, 881 F.3d 75 (D.C. Cir. 2018) - CFPB enforcement authority",
            "Beach v. Ocwen Federal Bank, 523 U.S. 410 (1998) - RESPA escrow analysis requirements",
        ],
        category="financing",
        subcategory="general",
        authority_score=0.85,
        confidence=0.87,
        related_topics=["deed_of_trust", "respa_compliance", "tila_compliance", "foreclosure"],
        practice_tips=[
            "Compare the Loan Estimate to the Closing Disclosure for fee tolerance violations",
            "Know the difference between tolerance categories (zero, 10%, and unlimited)",
            "Verify escrow account setup complies with RESPA aggregate adjustment limits",
        ],
        texas_notes="Texas has unique home equity lending restrictions under Art. XVI, SS 50 of the Texas Constitution. Home equity loans cannot exceed 80% LTV, and there are specific requirements for closing, right of rescission, and fee limitations.",
    ),

    # ========================================================================
    # FORECLOSURE
    # ========================================================================

    DoctrineCacheBlock(
        topic="foreclosure_non_judicial",
        summary="Non-judicial foreclosure (also called power of sale foreclosure) allows the trustee or mortgagee to sell the property without court involvement, pursuant to a power of sale clause in the deed of trust or mortgage. This is faster and less expensive than judicial foreclosure. The process typically requires: default, notice of default/acceleration, notice of sale, public sale, and delivery of trustee's deed. The borrower may have a right to cure (reinstate) before sale and, in some states, a right of redemption after sale. Deficiency judgments may be available in some states. Non-judicial foreclosure is the standard method in Texas, California, and approximately 30 other states.",
        key_statutes=[
            "Tex. Prop. Code SS 51.002 (Texas non-judicial foreclosure)",
            "Tex. Prop. Code SS 51.003 (deficiency judgments)",
            "Tex. Prop. Code SS 51.0025 (notice requirements for residential)",
            "Cal. Civ. Code SS 2924 (California non-judicial foreclosure)",
            "State specific power of sale statutes",
        ],
        elements=[
            "Default under the note or deed of trust",
            "Acceleration of the debt",
            "Required notices (default notice, cure notice, sale notice)",
            "Compliance with state-specific timing requirements",
            "Public sale at designated time, place, and manner",
            "Sale to highest bidder (or credit bid by lender)",
            "Execution and recording of trustee's deed",
            "Distribution of sale proceeds (lien priority order)",
        ],
        defenses=[
            "Lack of standing (broken chain of assignments)",
            "Failure to provide required notices",
            "Failure to comply with timing requirements",
            "TILA rescission right still active",
            "Bankruptcy automatic stay (11 USC 362)",
            "Active military service (SCRA protection)",
            "Loan modification in process (dual tracking prohibited under some state laws)",
            "Tender of full amount owed before sale",
            "Fraud or procedural irregularity in sale process",
        ],
        remedies=[
            "Trustee's deed upon sale to purchaser",
            "Deficiency judgment against borrower (where permitted)",
            "Borrower right to cure before sale (reinstatement)",
            "Statutory right of redemption after sale (where available)",
            "TRO or injunction to stop wrongful foreclosure",
            "Damages for wrongful foreclosure",
            "Void sale for procedural defects",
        ],
        leading_cases=[
            "Yvanova v. New Century Mortgage Corp., 62 Cal.4th 919 (2016) - borrower standing to challenge void assignment",
            "Jasper v. Wells Fargo Bank, 2015 WL 4041240 (Tex. App.) - notice requirements for Texas foreclosure",
            "Beal Bank v. Almand & Associates, 780 So.2d 45 (Fla. 2001) - bona fide purchaser at foreclosure sale",
        ],
        category="foreclosure",
        subcategory="non_judicial",
        authority_score=0.85,
        confidence=0.87,
        related_topics=["deed_of_trust", "right_of_redemption", "deficiency_judgment", "short_sale"],
        practice_tips=[
            "Verify the complete chain of assignments from originator to current holder",
            "Confirm all notice requirements have been strictly complied with",
            "Consider bidding strategies at the sale (credit bid vs. cash bid dynamics)",
        ],
        texas_notes="Texas foreclosures occur on the first Tuesday of the month at the county courthouse. At least 21 days notice is required after a 20-day cure notice for residential properties. Texas allows deficiency judgments but applies an FMV credit under Tex. Prop. Code SS 51.003.",
    ),

    DoctrineCacheBlock(
        topic="foreclosure_alternatives",
        summary="Foreclosure alternatives allow borrowers and lenders to resolve default without a forced sale. Key alternatives include: short sale (sale for less than the debt with lender approval), deed in lieu of foreclosure (voluntary conveyance to lender), loan modification (change in loan terms), forbearance agreement (temporary pause or reduction in payments), and repayment plan (catch-up plan for arrears). Each alternative has tax implications (potential cancellation of debt income under IRC 108), credit reporting consequences, and may or may not result in a deficiency waiver. The Mortgage Forgiveness Debt Relief Act provided temporary tax relief for qualified principal residence indebtedness.",
        key_statutes=[
            "26 USC 108 (Income from discharge of indebtedness)",
            "Mortgage Forgiveness Debt Relief Act of 2007 (as extended)",
            "State deficiency judgment statutes",
            "State anti-deficiency statutes (e.g., Cal. CCP SS 580b)",
            "CFPB loss mitigation rules (12 CFR 1024.41)",
        ],
        elements=[
            "Borrower financial hardship documentation",
            "Lender approval of the specific alternative",
            "Terms of the agreement (short sale price, modification terms, forbearance period)",
            "Release or preservation of deficiency claim",
            "Tax implications analysis (IRC 108 exclusions)",
            "Credit reporting agreement",
            "Documentation and recording of instruments",
        ],
        defenses=[
            "Lender failed to consider loss mitigation before foreclosure (CFPB rules)",
            "Dual tracking (proceeding with foreclosure while loss mitigation pending)",
            "Oral promise of modification not honored (promissory estoppel)",
            "Short sale approval was unreasonably withheld",
        ],
        remedies=[
            "Approved short sale with deficiency waiver",
            "Deed in lieu with full satisfaction of debt",
            "Loan modification with reduced rate or principal",
            "Forbearance agreement with payment plan",
            "Cash for keys program",
            "IRC 108 exclusion for insolvency or principal residence debt forgiveness",
        ],
        leading_cases=[
            "Wigod v. Wells Fargo Bank, 673 F.3d 547 (7th Cir. 2012) - promissory estoppel for loan modification promises",
            "Corvello v. Wells Fargo Bank NA, 728 F.3d 878 (9th Cir. 2013) - breach of contract for HAMP trial modification",
        ],
        category="foreclosure",
        subcategory="alternatives",
        authority_score=0.78,
        confidence=0.82,
        related_topics=["foreclosure_non_judicial", "deficiency_judgment", "tax_cancellation_of_debt"],
        practice_tips=[
            "Get any short sale or modification approval in writing before proceeding",
            "Ensure deficiency waiver language is explicit and recorded",
            "Consult a tax advisor about COD income implications before accepting forgiveness",
        ],
        texas_notes="Texas does not have an anti-deficiency statute for purchase money mortgages (unlike California). Deficiency judgments are permitted but the borrower receives a credit for the greater of the sale price or FMV.",
    ),

    # ========================================================================
    # 1031 EXCHANGES
    # ========================================================================

    DoctrineCacheBlock(
        topic="section_1031_exchange",
        summary="IRC Section 1031 allows taxpayers to defer recognition of gain on the exchange of like-kind real property held for productive use in a trade or business or for investment. After the Tax Cuts and Jobs Act of 2017, only real property qualifies (personal property no longer qualifies). The exchange must be completed within a strict timeline: 45 days to identify replacement property and 180 days to close. A qualified intermediary must hold the exchange funds. Boot (non-like-kind property or cash received) is taxable. Related party exchanges have a 2-year holding requirement. Delaware Statutory Trusts (DSTs) and Tenancy-in-Common (TIC) interests can qualify as replacement property.",
        key_statutes=[
            "26 USC 1031 (Like-kind exchange)",
            "26 CFR 1.1031 (Treasury Regulations)",
            "Rev. Proc. 2000-37 (safe harbor for reverse exchanges)",
            "Rev. Proc. 2002-22 (TIC safe harbor)",
            "Tax Cuts and Jobs Act of 2017 (limited to real property)",
        ],
        elements=[
            "Like-kind real property (both relinquished and replacement)",
            "Held for productive use in trade/business or investment",
            "Qualified intermediary holding exchange funds",
            "Replacement property identified within 45 calendar days",
            "Exchange completed within 180 calendar days",
            "Same taxpayer on both sides of the exchange",
            "Three-property rule, 200% rule, or 95% rule for identification",
            "No constructive receipt of exchange funds by taxpayer",
        ],
        defenses=[
            "Personal use property does not qualify (vacation home, primary residence)",
            "Partnership interests do not qualify (even if holding real property)",
            "Related party exchange disposition within 2 years triggers gain",
            "Constructive receipt of funds by taxpayer disqualifies exchange",
            "Identification deadline missed (strict compliance required)",
            "Boot received triggers gain to the extent of boot",
        ],
        remedies=[
            "Full tax deferral on gain if all requirements met",
            "Partial deferral if boot received (gain recognized to extent of boot)",
            "Basis step-up in replacement property",
            "Depreciation recapture deferral",
            "Multiple property exchanges allowed",
            "Improvement exchange (build-to-suit) using EAT",
        ],
        leading_cases=[
            "Starker v. United States, 602 F.2d 1341 (9th Cir. 1979) - deferred exchanges qualify",
            "Crenshaw v. United States, 450 F.2d 472 (5th Cir. 1971) - like-kind standard for real property",
            "Christensen v. Commissioner, T.C. Memo 1996-254 - vacation home does not qualify",
            "Revenue Ruling 77-297, 1977-2 C.B. 304 - fee simple for leasehold 30+ years is like-kind",
        ],
        category="tax_exchange",
        subcategory="1031_exchange",
        authority_score=0.88,
        confidence=0.90,
        related_topics=["capital_gains_tax", "depreciation_recapture", "real_estate_financing", "qualified_intermediary"],
        practice_tips=[
            "Engage the qualified intermediary BEFORE closing on the relinquished property",
            "Identify replacement properties in writing, signed and delivered to QI within 45 days",
            "Do not take constructive receipt of exchange proceeds at any point",
            "Consider DST or TIC structures for passive replacement property",
        ],
        texas_notes="Texas has no state income tax, so 1031 exchanges primarily defer federal tax obligations. However, Texas property tax implications of the exchange (change in assessed value) should be analyzed.",
    ),

    # ========================================================================
    # RESPA / TILA / FAIR HOUSING
    # ========================================================================

    DoctrineCacheBlock(
        topic="respa_compliance",
        summary="The Real Estate Settlement Procedures Act (RESPA) protects consumers in residential mortgage transactions by requiring disclosures about settlement costs, prohibiting kickbacks and referral fees, limiting escrow account deposits, and requiring loan servicers to follow specific procedures for handling borrower inquiries and escrow analyses. Key RESPA requirements include the Loan Estimate (within 3 business days of application), Closing Disclosure (3 business days before closing), prohibition on fee splitting (Section 8), affiliated business disclosure requirements, and servicing transfer notices.",
        key_statutes=[
            "12 USC 2601-2617 (RESPA)",
            "12 CFR 1024 (Regulation X)",
            "TILA-RESPA Integrated Disclosure (TRID) Rules",
            "CFPB RESPA enforcement guidance",
        ],
        elements=[
            "Federally related mortgage loan on 1-4 unit residential property",
            "Loan Estimate provided within 3 business days of application",
            "Closing Disclosure provided 3 business days before consummation",
            "No kickbacks, fee-splitting, or unearned fees (Section 8 prohibition)",
            "Affiliated business arrangement disclosure where applicable",
            "Escrow account limitations (Section 10)",
            "Servicing transfer notice requirements",
            "Loss mitigation procedures for delinquent borrowers",
        ],
        defenses=[
            "Transaction not a federally related mortgage loan",
            "Commercial transaction exemption",
            "Fee paid for actual services rendered (not referral fee)",
            "Statute of limitations expired (1 year for Section 8; 3 years for Section 6)",
            "No pattern or practice (individual vs. systemic violation)",
        ],
        remedies=[
            "Actual damages suffered by borrower",
            "Statutory damages up to $2,000 per violation (individual Section 8)",
            "Class action damages: lesser of $1,000,000 or 1% of net worth (Section 8 class action)",
            "Treble damages for pattern or practice violations",
            "Attorney's fees and court costs",
            "CFPB enforcement actions and civil money penalties",
        ],
        leading_cases=[
            "Freeman v. Quicken Loans Inc., 566 U.S. 624 (2012) - Section 8 requires fee splitting between two or more persons",
            "PHH Corp. v. CFPB, 881 F.3d 75 (D.C. Cir. 2018) - CFPB enforcement authority for RESPA",
            "Mertens v. Midland Mtg. Co., 2016 WL 3369512 (N.D. Iowa) - escrow analysis requirements",
        ],
        category="compliance",
        subcategory="respa",
        authority_score=0.88,
        confidence=0.88,
        related_topics=["tila_compliance", "real_estate_financing", "closing_procedures"],
        practice_tips=[
            "Audit affiliated business arrangements for proper disclosure",
            "Review all fee arrangements for potential Section 8 kickback issues",
            "Ensure Closing Disclosure is delivered within the required timeline",
        ],
        texas_notes="RESPA applies to federally related mortgage loans in Texas. Texas title insurance rates are promulgated, which reduces but does not eliminate RESPA fee-splitting concerns.",
    ),

    DoctrineCacheBlock(
        topic="fair_housing_act",
        summary="The Fair Housing Act (Title VIII of the Civil Rights Act of 1968, as amended) prohibits discrimination in the sale, rental, and financing of housing based on race, color, religion, sex, familial status, national origin, and disability. Prohibited actions include refusing to sell or rent, discriminatory terms and conditions, discriminatory advertising, blockbusting, steering, and failure to provide reasonable accommodations for disabled persons. The Act applies to most housing with limited exemptions (Mrs. Murphy exemption for owner-occupied buildings with 4 or fewer units, and religious organizations). Disparate impact claims are cognizable under the FHA.",
        key_statutes=[
            "42 USC 3601-3619 (Fair Housing Act)",
            "42 USC 3631 (Criminal penalties for housing interference)",
            "24 CFR 100 (HUD Fair Housing regulations)",
            "Americans with Disabilities Act (ADA) for commercial properties",
            "Tex. Prop. Code Ch. 301 (Texas Fair Housing Act)",
        ],
        elements=[
            "Protected class status (race, color, religion, sex, familial status, national origin, disability)",
            "Housing transaction (sale, rental, financing, insurance, brokerage)",
            "Discriminatory conduct (intentional or disparate impact)",
            "Causal connection between protected class and adverse action",
            "Standing (aggrieved person or fair housing organization)",
        ],
        defenses=[
            "Mrs. Murphy exemption (owner-occupied, 4 or fewer units, no broker used)",
            "Religious organization or private club exemption",
            "Housing for older persons exemption (55+ or 62+)",
            "Legitimate business justification for disparate impact policy",
            "Occupancy standards based on health and safety (not pretext)",
            "Direct threat to safety of others (disability context)",
        ],
        remedies=[
            "Actual damages (economic and emotional)",
            "Punitive damages",
            "Injunctive relief (cease and desist, policy changes)",
            "Civil penalties ($21,039 first offense; $52,596 repeat; $105,194 subsequent under 42 USC 3614)",
            "Attorney's fees and court costs",
            "HUD administrative hearing and determination",
            "Pattern or practice suits by DOJ",
        ],
        leading_cases=[
            "Texas Dept. of Housing v. Inclusive Communities Project, 576 U.S. 519 (2015) - disparate impact claims cognizable under FHA",
            "Shelley v. Kraemer, 334 U.S. 1 (1948) - judicial enforcement of racial covenants violates Equal Protection",
            "Trafficante v. Metropolitan Life Ins. Co., 409 U.S. 205 (1972) - broad standing under FHA",
            "City of Edmonds v. Oxford House Inc., 514 U.S. 725 (1995) - group homes for disabled under FHA",
        ],
        category="compliance",
        subcategory="fair_housing",
        authority_score=0.90,
        confidence=0.90,
        related_topics=["landlord_tenant_law", "real_estate_financing", "respa_compliance"],
        practice_tips=[
            "Train all agents and property managers on Fair Housing compliance annually",
            "Review all advertising for potentially discriminatory language or imagery",
            "Have a written reasonable accommodation/modification policy for disabled persons",
        ],
        texas_notes="Texas Fair Housing Act (Tex. Prop. Code Ch. 301) mirrors federal protections. The Texas Workforce Commission Civil Rights Division handles state Fair Housing complaints.",
    ),

    # ========================================================================
    # TEXAS PROPERTY CODE
    # ========================================================================

    DoctrineCacheBlock(
        topic="texas_community_property",
        summary="Texas is one of nine community property states. Property acquired during marriage is presumed community property unless proven otherwise by clear and convincing evidence. Separate property includes property owned before marriage, acquired by gift or inheritance during marriage, and recovery for personal injuries (except lost wages). Inception of title determines character. Community property requires joinder of both spouses for conveyance of homestead. Management of community property follows 'sole management' (earned by one spouse) and 'joint management' categories. Upon divorce, community property is divided in a 'just and right' manner, not necessarily equally.",
        key_statutes=[
            "Tex. Fam. Code SS 3.001-3.003 (Community Property definitions)",
            "Tex. Fam. Code SS 3.102 (Management of Community Property)",
            "Tex. Const. Art. XVI, SS 15 (Separate and community property)",
            "Tex. Fam. Code SS 4.001-4.106 (Marital Property Agreements)",
            "Tex. Prop. Code SS 5.001 (Conveyances requiring spousal joinder)",
        ],
        elements=[
            "Property acquired during marriage is presumptively community",
            "Inception of title doctrine determines character at acquisition",
            "Clear and convincing evidence required to rebut community presumption",
            "Tracing required to prove separate property character",
            "Spousal joinder required for homestead conveyance",
            "Management categories: sole vs. joint management community",
            "Characterization unaffected by title-holding form",
        ],
        defenses=[
            "Property is separate by gift, devise, or descent",
            "Property owned before marriage (inception of title pre-marriage)",
            "Valid pre-marital or post-marital property agreement (partition)",
            "Tracing to separate property source",
            "Personal injury recovery (except lost earnings)",
            "Agreed transmutation by written partition agreement",
        ],
        remedies=[
            "Partition of community property",
            "Just and right division upon divorce",
            "Reimbursement for separate property contributions to community",
            "Fraud claim for unauthorized community property disposition",
            "Constructive trust on proceeds of improper disposal",
            "Void conveyance of homestead without spousal joinder",
        ],
        leading_cases=[
            "Tarver v. Tarver, 394 S.W.2d 780 (Tex. 1965) - inception of title doctrine",
            "Norris v. Vaughan, 152 Tex. 491 (1953) - community property presumption",
            "Boyd v. Boyd, 67 S.W.3d 398 (Tex. App. 2002) - tracing separate property through commingled accounts",
        ],
        category="texas",
        subcategory="community_property",
        authority_score=0.88,
        confidence=0.90,
        related_topics=["texas_homestead", "divorce_property", "title_examination"],
        practice_tips=[
            "Always verify marital status and obtain spousal joinder on homestead conveyances",
            "Check for recorded partition or prenuptial agreements affecting characterization",
            "Trace separate property contributions through maintained separate accounts",
        ],
        texas_notes="Texas community property law derives from Spanish law tradition and is constitutionally established. The inception of title doctrine is uniquely Texas and determines property character based on when the right to acquire attached.",
    ),

    DoctrineCacheBlock(
        topic="texas_homestead",
        summary="The Texas homestead exemption is among the strongest in the nation, providing constitutional protection against forced sale for most debts. An urban homestead can be up to 10 acres, and a rural homestead up to 200 acres (100 for a single person). Homestead protection is automatic (no filing required, though a homestead designation can be filed). Only specific liens can be enforced against a homestead: purchase money, property taxes, home improvement, home equity loans (with strict constitutional limitations), owelty of partition, federal tax liens, and reverse mortgages. The homestead exemption also provides a property tax exemption of at least $100,000 from school district taxes (increased from $40,000 in 2023).",
        key_statutes=[
            "Tex. Const. Art. XVI, SS 50 (Homestead protections and permissible liens)",
            "Tex. Const. Art. XVI, SS 51 (Homestead exempt from forced sale)",
            "Tex. Prop. Code Ch. 41 (Homestead exemptions)",
            "Tex. Tax Code SS 11.13 (Homestead property tax exemption)",
            "Tex. Prop. Code SS 41.001 (Homestead defined)",
        ],
        elements=[
            "Property used as the family home or single adult home",
            "Urban homestead: up to 10 acres in a city or town",
            "Rural homestead: up to 200 acres (100 for single adult) outside city",
            "Protection is automatic by use as homestead (no filing required)",
            "Both ownership and use as homestead required simultaneously",
            "Protection continues even after temporary absence if intent to return",
            "Only constitutionally enumerated liens can be enforced against homestead",
        ],
        defenses=[
            "Lien is not one of the constitutionally permitted types",
            "Creditor failed to comply with constitutional requirements for home equity",
            "Property constitutes homestead even if not designated or claimed",
            "Temporary absence does not forfeit homestead if intent to return exists",
            "Excess acreage beyond homestead limits must be separately claimed",
        ],
        remedies=[
            "Void lien that is not a permitted homestead lien",
            "Void home equity loan that fails constitutional requirements",
            "Injunction against forced sale of homestead property",
            "Property tax exemption (at least $100,000 from school district taxes)",
            "Over-65 or disabled person additional exemption and tax freeze",
            "Surviving spouse continuation of homestead protection",
        ],
        leading_cases=[
            "In re Perry, 345 F.3d 303 (5th Cir. 2003) - scope of Texas homestead protection in bankruptcy",
            "Heggen v. Pemelton, 836 S.W.2d 145 (Tex. 1992) - homestead designation not required for protection",
            "Laster v. First Huntsville Properties Co., 826 S.W.2d 125 (Tex. 1991) - intent to return preserves homestead",
        ],
        category="texas",
        subcategory="homestead",
        authority_score=0.90,
        confidence=0.92,
        related_topics=["texas_community_property", "property_tax", "foreclosure"],
        practice_tips=[
            "File a homestead designation with the county clerk even though not legally required",
            "Verify any lien against homestead is a constitutionally permitted type before honoring",
            "Apply for all available homestead property tax exemptions with the appraisal district",
        ],
        texas_notes="Texas homestead protection is enshrined in the state constitution and cannot be waived in most circumstances. The 2023 increase in the school tax homestead exemption to $100,000 provides significant property tax relief.",
    ),

    # ========================================================================
    # OIL AND GAS / MINERAL RIGHTS
    # ========================================================================

    DoctrineCacheBlock(
        topic="mineral_rights_surface_vs_subsurface",
        summary="In Texas and other mineral-producing states, the mineral estate and surface estate can be severed, creating a 'split estate.' The mineral estate is the dominant estate, meaning the mineral owner has an implied right to use as much of the surface as is reasonably necessary to explore, develop, and produce minerals. However, the accommodation doctrine (Getty Oil v. Jones) requires the mineral owner to accommodate existing surface uses if the mineral owner has reasonable alternative means to access the minerals. Key interests include royalty interests (nonparticipating and overriding), working interests (operating rights), and executive rights (right to lease). Pooling and unitization combine multiple tracts for development purposes.",
        key_statutes=[
            "Tex. Nat. Res. Code (Texas Natural Resources Code)",
            "Tex. Prop. Code SS 5.001 (Conveyances of mineral interests)",
            "Texas Railroad Commission rules (16 TAC)",
            "State mineral rights severance statutes",
            "Restatement of the Law, Property (Servitudes) - mineral rights",
        ],
        elements=[
            "Mineral estate is dominant estate (implied surface use right)",
            "Surface estate is servient to mineral operations",
            "Mineral estate includes right to explore, develop, produce, and transport",
            "Accommodation doctrine limits surface use to reasonably necessary",
            "Royalty interest: right to share in production without cost obligation",
            "Working interest: right to operate and develop, with cost obligation",
            "Executive right: right to execute oil and gas leases",
            "Pooling combines multiple tracts into a single production unit",
        ],
        defenses=[
            "Accommodation doctrine (mineral owner has reasonable alternatives)",
            "Surface damage statute (compensation required for surface destruction)",
            "Existing surface use has priority if mineral owner has alternatives",
            "Lease terms restrict surface operations",
            "Environmental regulations limiting surface disturbance",
            "Trespass claim if mineral operations exceed reasonable necessity",
        ],
        remedies=[
            "Injunction to limit unreasonable surface destruction",
            "Surface damage compensation",
            "Royalty payment enforcement",
            "Quiet title to establish mineral ownership",
            "Declaratory judgment on scope of mineral rights",
            "Accounting for production and royalties",
            "Lease termination for breach of implied covenants",
        ],
        leading_cases=[
            "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971) - accommodation doctrine",
            "Moser v. US Steel Corp., 676 S.W.2d 99 (Tex. 1984) - executive duty and self-dealing",
            "French v. Chevron U.S.A., Inc., 896 S.W.2d 795 (Tex. 1995) - royalty calculation and market value",
            "Lesley v. Veterans Land Board, 352 S.W.3d 479 (Tex. 2011) - mineral estate dominance limits",
        ],
        category="mineral_rights",
        subcategory="surface_vs_mineral",
        authority_score=0.88,
        confidence=0.88,
        related_topics=["oil_gas_lease", "pooling_unitization", "royalty_interest", "accommodation_doctrine"],
        practice_tips=[
            "Always review mineral reservations in chain of title going back to original patent",
            "Obtain a mineral title opinion before acquiring property in oil-producing regions",
            "Negotiate surface use agreements to protect existing improvements and operations",
        ],
        texas_notes="Texas is the leading oil and gas producing state with the most developed mineral rights jurisprudence. The Texas Railroad Commission regulates drilling, spacing, and production allowables. The accommodation doctrine originated in Texas in Getty Oil v. Jones.",
    ),

    DoctrineCacheBlock(
        topic="oil_gas_lease_essentials",
        summary="An oil and gas lease grants the lessee (operator) the right to explore for and produce oil, gas, and other minerals from the lessor's property. Key terms include the primary term (typically 3-5 years), bonus payment (upfront consideration), delay rental (annual payment to maintain lease without drilling during primary term), royalty rate (typically 1/8 to 1/4 of production), and shut-in royalty clause. The habendum clause defines the term ('for a period of X years and so long thereafter as oil and gas are produced'). Implied covenants include the duty to explore, develop, protect against drainage, market production, and operate as a reasonably prudent operator.",
        key_statutes=[
            "Tex. Nat. Res. Code",
            "State oil and gas conservation statutes",
            "16 TAC (Texas Railroad Commission rules)",
            "State recording acts (oil and gas leases must be recorded)",
        ],
        elements=[
            "Granting clause (minerals conveyed and rights granted)",
            "Habendum clause (primary term and secondary term conditions)",
            "Bonus payment (upfront consideration for lease execution)",
            "Delay rental clause (payment to maintain lease during primary term without drilling)",
            "Royalty clause (lessor's share of production, typically 1/8 to 1/4)",
            "Pooling clause (authority to combine tracts for drilling unit)",
            "Surface use provisions",
            "Assignment clause",
            "Force majeure clause",
            "Shut-in royalty clause (maintain lease when wells are shut-in)",
        ],
        defenses=[
            "Lease expired for failure to produce or pay delay rentals",
            "Cessation of production without resumption within reasonable time",
            "Failure to comply with implied covenant to develop",
            "Breach of implied covenant to market production",
            "Drainage of lessor's minerals without protective drilling",
            "Force majeure event preventing operations",
            "Lessor lacked authority to execute lease (title defect)",
        ],
        remedies=[
            "Lease cancellation for breach of implied covenant",
            "Damages for failure to develop or protect against drainage",
            "Royalty underpayment claim with interest",
            "Accounting for production and sales",
            "Declaratory judgment on lease status (held by production or expired)",
            "Trespass damages for operations after lease expiration",
        ],
        leading_cases=[
            "Clifton v. Koontz, 160 Tex. 82 (1959) - production in paying quantities standard",
            "Pshigoda v. Texaco Inc., 703 S.W.2d 688 (Tex. App. 1986) - implied covenant to develop",
            "Heritage Resources Inc. v. NationsBank, 939 S.W.2d 118 (Tex. 1996) - shut-in royalty clause interpretation",
            "Burlington Resources Oil & Gas Co. v. Texas Crude Energy LLC, 573 S.W.3d 198 (Tex. 2019) - top lease validity",
        ],
        category="mineral_rights",
        subcategory="oil_gas_lease",
        authority_score=0.85,
        confidence=0.87,
        related_topics=["mineral_rights_surface_vs_subsurface", "pooling_unitization", "royalty_interest"],
        practice_tips=[
            "Verify lessor's mineral ownership with a mineral title opinion before leasing",
            "Negotiate for higher royalty rates (1/4 is becoming standard in the Permian Basin)",
            "Include Pugh clause to prevent lease perpetuation on non-producing tracts",
        ],
        texas_notes="Texas oil and gas leases are real property interests that must be recorded. The Texas Railroad Commission regulates well spacing, drilling permits, and production allowables. Permian Basin lease terms are heavily negotiated.",
    ),

    # ========================================================================
    # ADDITIONAL DOCTRINE BLOCKS
    # ========================================================================

    DoctrineCacheBlock(
        topic="adverse_possession",
        summary="Adverse possession allows a person to acquire legal title to real property through continuous, open, notorious, exclusive, hostile, and adverse possession for the statutory period. The possessor must act as an owner would, making use of the property openly and without the true owner's permission. Most states require actual, visible possession (not just constructive). Color of title (an invalid deed) may reduce the required period in some states. Payment of property taxes may be required in addition to possession. Tacking of successive possessors' periods is allowed if there is privity of estate.",
        key_statutes=[
            "Tex. Civ. Prac. & Rem. Code SS 16.021-16.034 (Texas adverse possession statutes)",
            "State limitation of actions statutes (varies 5-20 years)",
            "Tex. Civ. Prac. & Rem. Code SS 16.024 (5-year peaceable possession under color of title)",
            "Tex. Civ. Prac. & Rem. Code SS 16.025 (10-year possession)",
            "Tex. Civ. Prac. & Rem. Code SS 16.026 (25-year possession)",
        ],
        elements=[
            "Actual possession (physical occupation and use of the land)",
            "Open and notorious (visible to the true owner and community)",
            "Exclusive (not shared with true owner or public)",
            "Hostile and adverse (without permission)",
            "Continuous for the statutory period (uninterrupted)",
            "Under claim of right or color of title (in some jurisdictions)",
            "Payment of taxes during possession period (required in some states)",
        ],
        defenses=[
            "Possession was permissive (license, lease, or oral agreement)",
            "Statutory period not met (interruption resets the clock)",
            "Property is government-owned (immune in most states)",
            "True owner is a minor, incompetent, or imprisoned (tolling)",
            "Possession was not exclusive or continuous",
            "Possessor acknowledged true owner's title",
        ],
        remedies=[
            "Declaratory judgment establishing title by adverse possession",
            "Quiet title action",
            "Ejectment action by true owner (before limitations expire)",
            "Damages for trespass (before adverse possession period complete)",
        ],
        leading_cases=[
            "Mugaas v. Smith, 33 Wn.2d 429 (1949) - adverse possession and boundary disputes",
            "Howard v. Kunto, 3 Wn. App. 393 (1970) - tacking of adverse possession periods",
            "Nome 2000 v. Fagerstrom, 799 P.2d 304 (Alaska 1990) - acts of possession standard",
            "Rhodes v. Cahill, 802 S.W.2d 643 (Tex. 1990) - Texas adverse possession requirements",
        ],
        category="title",
        subcategory="adverse_possession",
        authority_score=0.82,
        confidence=0.85,
        related_topics=["prescriptive_easement", "quiet_title_action", "title_examination"],
        practice_tips=[
            "Document all acts of possession with dates, photographs, and witness statements",
            "Pay property taxes during the possession period to strengthen the claim",
            "File a quiet title action promptly once the statutory period has run",
        ],
        texas_notes="Texas has three adverse possession periods: 5 years (with color of title and tax payment), 10 years (peaceable possession), and 25 years (no requirement for color of title). Government land cannot be acquired by adverse possession in Texas.",
    ),

    DoctrineCacheBlock(
        topic="property_tax_assessment",
        summary="Property taxes are ad valorem taxes levied by local governments (counties, cities, school districts, special districts) based on the assessed value of real property. Assessment methods include comparable sales, income capitalization, and cost approach. Property owners have the right to protest assessed values and receive a hearing before an appraisal review board (ARB). Exemptions include homestead, disabled veteran, over-65, agricultural (1-d-1), and charitable/religious organization exemptions. Property tax liens are typically senior to all other liens except federal tax liens in some circumstances.",
        key_statutes=[
            "Tex. Tax Code (Texas Tax Code)",
            "Tex. Tax Code SS 11.13 (Homestead exemption)",
            "Tex. Tax Code SS 23.51-23.57 (Agricultural appraisal - 1-d-1)",
            "Tex. Tax Code Ch. 41-42 (Protest and appeal procedures)",
            "State property tax codes (varies by state)",
        ],
        elements=[
            "Assessment of property value by appraisal district",
            "Notice of appraised value to property owner",
            "Right to protest value to appraisal review board (ARB)",
            "Application of applicable exemptions",
            "Tax rate set by taxing authorities",
            "Tax levy and billing",
            "Delinquent tax collection and lien enforcement",
        ],
        defenses=[
            "Overvaluation (assessed value exceeds market value)",
            "Unequal appraisal (property assessed higher than comparable properties)",
            "Incorrect property description or classification",
            "Failure to apply eligible exemptions",
            "Procedural defects in assessment notice",
            "Excessive valuation methodology",
        ],
        remedies=[
            "Protest to appraisal review board (ARB)",
            "Binding arbitration for properties under certain value thresholds",
            "Judicial appeal to district court",
            "Correction of assessment errors",
            "Retroactive application of missed exemptions (in some states)",
            "Tax lien discharge through payment",
        ],
        leading_cases=[
            "Village of Norwood v. Baker, 172 U.S. 269 (1898) - special assessments must benefit the property",
            "Allegheny Pittsburgh Coal Co. v. County Commission, 488 U.S. 336 (1989) - equal protection in assessment",
        ],
        category="tax",
        subcategory="property_tax",
        authority_score=0.80,
        confidence=0.85,
        related_topics=["texas_homestead", "property_tax_lien", "agricultural_exemption"],
        practice_tips=[
            "File protests by the May 15 deadline (or 30 days after notice) in Texas",
            "Bring comparable sales data and independent appraisals to ARB hearings",
            "Apply for all eligible exemptions before the April 30 deadline in Texas",
        ],
        texas_notes="Texas has no state income tax, making property taxes the primary revenue source for local government. Appraisal districts set values, and taxing units set rates. The 2023-2024 tax reform package provided significant compression of school tax rates and increased homestead exemptions.",
    ),
]


# ============================================================================
# DOCTRINE CACHE INDEX
# ============================================================================

class DoctrineCacheIndex:
    """Fast O(1) lookup index for doctrine cache blocks.

    Provides retrieval by topic, category, subcategory, and
    jurisdiction with search and staleness tracking.
    """

    def __init__(self) -> None:
        self._by_topic: Dict[str, DoctrineCacheBlock] = {}
        self._by_category: Dict[str, List[DoctrineCacheBlock]] = {}
        self._by_subcategory: Dict[str, List[DoctrineCacheBlock]] = {}
        self._by_jurisdiction: Dict[str, List[DoctrineCacheBlock]] = {}
        self._all_blocks: List[DoctrineCacheBlock] = []
        self._block_hashes: Dict[str, str] = {}
        self._built_at: str = ""
        self._build_time_ms: float = 0.0
        logger.info("DoctrineCacheIndex created (empty)")

    def build(self, blocks: List[DoctrineCacheBlock]) -> None:
        """Build the index from a list of doctrine blocks."""
        start = time.monotonic()
        self._by_topic.clear()
        self._by_category.clear()
        self._by_subcategory.clear()
        self._by_jurisdiction.clear()
        self._all_blocks = list(blocks)
        self._block_hashes.clear()

        for block in blocks:
            self._by_topic[block.topic] = block
            self._by_category.setdefault(block.category, []).append(block)
            if block.subcategory:
                self._by_subcategory.setdefault(block.subcategory, []).append(block)
            self._by_jurisdiction.setdefault(block.jurisdiction, []).append(block)
            self._block_hashes[block.topic] = block.compute_hash()

        self._built_at = datetime.now(timezone.utc).isoformat()
        self._build_time_ms = (time.monotonic() - start) * 1000.0
        logger.info(
            f"DoctrineCacheIndex built | blocks={len(blocks)} | "
            f"categories={len(self._by_category)} | "
            f"time={self._build_time_ms:.1f}ms"
        )

    def get_by_topic(self, topic: str) -> Optional[DoctrineCacheBlock]:
        """Get a doctrine block by topic name."""
        return self._by_topic.get(topic)

    def get_by_category(self, category: str) -> List[DoctrineCacheBlock]:
        """Get all doctrine blocks in a category."""
        return self._by_category.get(category, [])

    def get_by_subcategory(self, subcategory: str) -> List[DoctrineCacheBlock]:
        """Get all doctrine blocks in a subcategory."""
        return self._by_subcategory.get(subcategory, [])

    def get_by_jurisdiction(self, jurisdiction: str) -> List[DoctrineCacheBlock]:
        """Get all doctrine blocks for a jurisdiction."""
        return self._by_jurisdiction.get(jurisdiction, [])

    def get_all_topics(self) -> List[str]:
        """Get all indexed topic names."""
        return list(self._by_topic.keys())

    def get_all_categories(self) -> List[str]:
        """Get all indexed category names."""
        return list(self._by_category.keys())

    def search_blocks(self, query_lower: str, top_k: int = 5) -> List[DoctrineCacheBlock]:
        """Simple substring search over block content."""
        scored: List[tuple[float, DoctrineCacheBlock]] = []
        query_tokens = set(query_lower.split())

        for block in self._all_blocks:
            content_lower = block.content_for_search().lower()
            hit_count = sum(1 for token in query_tokens if token in content_lower)
            if hit_count > 0:
                score = hit_count / max(len(query_tokens), 1)
                scored.append((score, block))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [block for _, block in scored[:top_k]]

    def get_coverage_map(self) -> Dict[str, Any]:
        """Get the full doctrine coverage map with staleness data."""
        coverage: Dict[str, Any] = {
            "total_blocks": len(self._all_blocks),
            "categories": {},
            "topics": [],
            "built_at": self._built_at,
            "build_time_ms": round(self._build_time_ms, 2),
        }
        for cat, blocks in self._by_category.items():
            coverage["categories"][cat] = {
                "count": len(blocks),
                "topics": [b.topic for b in blocks],
                "avg_confidence": round(sum(b.confidence for b in blocks) / max(len(blocks), 1), 4),
                "avg_authority": round(sum(b.authority_score for b in blocks) / max(len(blocks), 1), 4),
            }
        for block in self._all_blocks:
            coverage["topics"].append({
                "topic": block.topic,
                "category": block.category,
                "subcategory": block.subcategory,
                "confidence": block.confidence,
                "authority_score": block.authority_score,
                "last_updated": block.last_updated,
                "staleness_days": block.staleness_days,
                "hash": self._block_hashes.get(block.topic, ""),
            })
        return coverage

    def get_stale_blocks(self, max_staleness_days: int = 90) -> List[DoctrineCacheBlock]:
        """Get blocks that are stale (older than max_staleness_days)."""
        return [b for b in self._all_blocks if b.staleness_days > max_staleness_days]

    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics."""
        return {
            "total_blocks": len(self._all_blocks),
            "categories": len(self._by_category),
            "subcategories": len(self._by_subcategory),
            "jurisdictions": len(self._by_jurisdiction),
            "topics": len(self._by_topic),
            "built_at": self._built_at,
            "build_time_ms": round(self._build_time_ms, 2),
            "category_counts": {cat: len(blocks) for cat, blocks in self._by_category.items()},
        }

    def compute_cache_hash(self) -> str:
        """Compute SHA-256 hash of the entire cache for integrity checks."""
        all_hashes = sorted(f"{t}:{h}" for t, h in self._block_hashes.items())
        combined = "|".join(all_hashes)
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()


# ============================================================================
# MODULE-LEVEL SINGLETONS AND CONVENIENCE FUNCTIONS
# ============================================================================

_cache_index: Optional[DoctrineCacheIndex] = None


def build_doctrine_cache(blocks: Optional[List[DoctrineCacheBlock]] = None) -> DoctrineCacheIndex:
    """Build and return the doctrine cache index.

    Uses the default DOCTRINE_BLOCKS if no custom blocks are provided.
    """
    global _cache_index
    _cache_index = DoctrineCacheIndex()
    _cache_index.build(blocks or DOCTRINE_BLOCKS)
    return _cache_index


def get_doctrine_cache() -> DoctrineCacheIndex:
    """Get the doctrine cache index, building it if necessary."""
    global _cache_index
    if _cache_index is None:
        _cache_index = build_doctrine_cache()
    return _cache_index


def get_doctrine_block(topic: str) -> Optional[DoctrineCacheBlock]:
    """Retrieve a single doctrine block by topic."""
    return get_doctrine_cache().get_by_topic(topic)


def search_doctrines(query: str, top_k: int = 5) -> List[DoctrineCacheBlock]:
    """Free-text search over doctrine blocks."""
    return get_doctrine_cache().search_blocks(query.lower(), top_k=top_k)


def get_coverage_map() -> Dict[str, Any]:
    """Get the full doctrine coverage map."""
    return get_doctrine_cache().get_coverage_map()


def get_all_doctrine_topics() -> List[str]:
    """Get all registered doctrine topics."""
    return get_doctrine_cache().get_all_topics()


def get_all_doctrine_categories() -> List[str]:
    """Get all doctrine categories."""
    return get_doctrine_cache().get_all_categories()


def get_doctrine_blocks_by_category(category: str) -> List[DoctrineCacheBlock]:
    """Get all doctrine blocks for a category."""
    return get_doctrine_cache().get_by_category(category)


def get_stale_doctrines(max_staleness_days: int = 90) -> List[DoctrineCacheBlock]:
    """Get all stale doctrine blocks."""
    return get_doctrine_cache().get_stale_blocks(max_staleness_days)


def get_doctrine_cache_stats() -> Dict[str, Any]:
    """Get doctrine cache statistics."""
    return get_doctrine_cache().get_stats()


def get_doctrine_cache_hash() -> str:
    """Get the SHA-256 hash of the entire doctrine cache."""
    return get_doctrine_cache().compute_cache_hash()


def verify_doctrine_integrity() -> Dict[str, Any]:
    """Verify doctrine cache integrity."""
    cache = get_doctrine_cache()
    stats = cache.get_stats()
    cache_hash = cache.compute_cache_hash()
    stale = cache.get_stale_blocks(90)

    return {
        "valid": stats["total_blocks"] > 0,
        "total_blocks": stats["total_blocks"],
        "categories": stats["categories"],
        "cache_hash": cache_hash,
        "stale_blocks": len(stale),
        "stale_topics": [b.topic for b in stale],
        "built_at": stats["built_at"],
    }
