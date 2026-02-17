"""
LG04 Legal Document Draft Engine - Doctrine Cache
===================================================
Pre-compiled legal drafting doctrines covering contract formation,
UCC provisions, real estate documents, employment agreements,
corporate governance, IP assignments, loan documents, trust/estate
planning, M&A agreements, and regulatory compliance.

50+ doctrine blocks with real legal content for instant retrieval.

Engine ID: LG04
Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger
from pydantic import BaseModel, Field


# ============================================================================
# ENUMS
# ============================================================================


class DoctrineDomain(str, Enum):
    CONTRACT_FORMATION = "contract_formation"
    UCC_ARTICLE_2 = "ucc_article_2"
    REAL_ESTATE = "real_estate"
    EMPLOYMENT = "employment"
    CORPORATE = "corporate"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    FINANCE = "finance"
    ESTATE_PLANNING = "estate_planning"
    MERGER_ACQUISITION = "merger_acquisition"
    REGULATORY = "regulatory"
    GENERAL_DRAFTING = "general_drafting"
    BOILERPLATE = "boilerplate"


class DoctrineConfidence(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNCERTAIN = "UNCERTAIN"


# ============================================================================
# MODELS
# ============================================================================


class DoctrineBlock(BaseModel):
    doctrine_id: str
    topic: str
    domain: DoctrineDomain
    title: str
    summary: str
    content: str
    key_elements: List[str] = Field(default_factory=list)
    applicable_document_types: List[str] = Field(default_factory=list)
    jurisdictional_notes: str = ""
    statutory_references: List[str] = Field(default_factory=list)
    confidence: DoctrineConfidence = DoctrineConfidence.HIGH
    last_updated: str = ""
    tags: List[str] = Field(default_factory=list)
    template_clauses: List[str] = Field(default_factory=list)


class DoctrineResponse(BaseModel):
    doctrine_id: str
    topic: str
    domain: str
    title: str
    summary: str
    content: str
    key_elements: List[str] = Field(default_factory=list)
    confidence: str = "HIGH"
    confidence_score: float = 0.85
    cache_hit: bool = True
    retrieval_time_ms: float = 0.0
    determinism_hash: str = ""


# ============================================================================
# DOCTRINE CACHE - 55 BLOCKS
# ============================================================================

DOCTRINE_CACHE: Dict[str, DoctrineBlock] = {}

def _add(block: DoctrineBlock) -> None:
    DOCTRINE_CACHE[block.doctrine_id] = block

# ---------- CONTRACT FORMATION (1-8) ----------

_add(DoctrineBlock(
    doctrine_id="LG04-CF-001",
    topic="offer_and_acceptance",
    domain=DoctrineDomain.CONTRACT_FORMATION,
    title="Offer and Acceptance",
    summary="A valid contract requires a definite offer communicated to the offeree and an unequivocal acceptance that mirrors the offer terms.",
    content=(
        "An offer is a manifestation of willingness to enter into a bargain, made so as to justify the offeree in understanding that assent "
        "is invited and will conclude the bargain (Restatement (Second) of Contracts Section 24). The offer must be sufficiently definite to "
        "enable a court to determine the existence of a breach and provide an appropriate remedy. Acceptance must be unconditional and must "
        "mirror the terms of the offer (mirror image rule). Under common law, any material alteration of the offer terms constitutes a "
        "counter-offer, not an acceptance. The mailbox rule provides that acceptance is effective upon dispatch when using an authorized "
        "medium. Revocation of an offer is effective upon receipt. An option contract, supported by consideration or nominal consideration "
        "in some jurisdictions, makes the offer irrevocable for the stated period. Silence generally does not constitute acceptance unless "
        "prior dealings establish otherwise. When drafting, the agreement should clearly identify the offer, the acceptance mechanism, and "
        "any conditions precedent to acceptance."
    ),
    key_elements=["definite offer", "communication to offeree", "mirror image acceptance", "mailbox rule", "option contract"],
    applicable_document_types=["sales_agreement", "service_agreement", "license_agreement"],
    statutory_references=["Restatement (Second) of Contracts SS 24-69", "UCC 2-206"],
    tags=["offer", "acceptance", "formation", "mirror image"],
    template_clauses=["WHEREAS, Party A has offered and Party B has accepted the terms herein set forth..."],
))

_add(DoctrineBlock(
    doctrine_id="LG04-CF-002",
    topic="consideration",
    domain=DoctrineDomain.CONTRACT_FORMATION,
    title="Consideration Doctrine",
    summary="Consideration is the bargained-for exchange of value that supports enforceability of a promise.",
    content=(
        "Consideration requires a bargained-for exchange where each party gives something of legal value. This can be a promise, an act, "
        "or a forbearance. Past consideration is generally not valid consideration. Adequacy of consideration is not typically examined "
        "by courts, but nominal consideration may be scrutinized. Pre-existing duty rule prevents enforcement of a promise to do what one "
        "is already legally obligated to do, except under UCC 2-209 which allows good-faith modifications without additional consideration. "
        "Promissory estoppel (Restatement Section 90) may substitute for consideration where a promisor should reasonably expect reliance. "
        "In drafting, recitals should identify the consideration exchanged: 'In consideration of the mutual promises and covenants contained "
        "herein, and for other good and valuable consideration, the receipt and sufficiency of which are hereby acknowledged.'"
    ),
    key_elements=["bargained-for exchange", "legal value", "pre-existing duty rule", "promissory estoppel", "adequacy"],
    applicable_document_types=["sales_agreement", "service_agreement", "license_agreement", "employment_agreement"],
    statutory_references=["Restatement (Second) of Contracts SS 71-90", "UCC 2-209"],
    tags=["consideration", "value", "exchange", "promissory estoppel"],
    template_clauses=["In consideration of the mutual covenants and agreements herein, the Parties agree as follows:"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-CF-003",
    topic="capacity_to_contract",
    domain=DoctrineDomain.CONTRACT_FORMATION,
    title="Capacity to Contract",
    summary="Parties must have legal capacity to enter a contract; minors, mentally incapacitated persons, and intoxicated persons may lack capacity.",
    content=(
        "Legal capacity requires that each party be of legal age (18 in most jurisdictions), of sound mind, and not under undue influence "
        "or duress. Contracts with minors are voidable at the minor's option. Mental incapacity renders a contract voidable if the party "
        "could not understand the nature and consequences of the transaction. Corporate entities must act through authorized representatives "
        "with proper authority (actual or apparent). The drafting attorney should verify authority through corporate resolutions, certificates "
        "of authority, or powers of attorney. When drafting, include representations of authority: 'Each party represents that it has full "
        "power and authority to enter into and perform this Agreement.'"
    ),
    key_elements=["legal age", "sound mind", "corporate authority", "authorization", "representation of authority"],
    applicable_document_types=["sales_agreement", "service_agreement", "corporate", "employment_agreement"],
    statutory_references=["Restatement (Second) of Contracts SS 12-16"],
    tags=["capacity", "authority", "competency", "minors"],
    template_clauses=["Each Party represents and warrants that it has full power and authority to execute and deliver this Agreement."],
))

_add(DoctrineBlock(
    doctrine_id="LG04-CF-004",
    topic="statute_of_frauds",
    domain=DoctrineDomain.CONTRACT_FORMATION,
    title="Statute of Frauds Requirements",
    summary="Certain contracts must be in writing and signed to be enforceable under the Statute of Frauds.",
    content=(
        "The Statute of Frauds (originating from 29 Charles II c.3, 1677) requires a writing signed by the party to be charged for: "
        "(1) contracts for the sale of land or interests therein; (2) contracts not performable within one year; (3) contracts for the "
        "sale of goods over $500 (UCC 2-201, raised to $5,000 under proposed amendments); (4) promises to answer for the debt of another "
        "(suretyship); (5) promises made in consideration of marriage; (6) executor promises to pay estate debts from personal funds. "
        "The writing must identify the parties, subject matter, and essential terms. Partial performance, promissory estoppel, and "
        "admission in pleadings may take an agreement outside the Statute. Electronic signatures satisfy the writing requirement under "
        "UETA and E-SIGN Act. When drafting, always reduce agreements to a signed writing that includes all material terms."
    ),
    key_elements=["writing requirement", "signed by party", "land interests", "one year", "goods over $500", "electronic signatures"],
    applicable_document_types=["real_estate", "sales_agreement", "employment_agreement", "guaranty"],
    statutory_references=["UCC 2-201", "UETA", "E-SIGN Act (15 U.S.C. 7001)"],
    tags=["statute of frauds", "writing", "signature", "enforceability"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-CF-005",
    topic="contract_interpretation",
    domain=DoctrineDomain.CONTRACT_FORMATION,
    title="Rules of Contract Interpretation",
    summary="Courts interpret contracts using established canons: plain meaning, four corners, ejusdem generis, and contra proferentem.",
    content=(
        "The parol evidence rule bars extrinsic evidence to contradict or vary the terms of a fully integrated written agreement. The "
        "four corners rule looks to the document itself for meaning. Plain meaning doctrine gives words their ordinary meaning unless "
        "defined otherwise. Ejusdem generis limits general terms following specific enumeration. Contra proferentem construes ambiguities "
        "against the drafter. Specific provisions control over general ones. Handwritten terms prevail over typed, which prevail over "
        "printed. Courts read contracts as a harmonious whole. When drafting: use defined terms consistently, include an integration "
        "clause, avoid ambiguous language, and define technical terms in a definitions section."
    ),
    key_elements=["parol evidence rule", "plain meaning", "four corners", "contra proferentem", "integration clause"],
    applicable_document_types=["sales_agreement", "service_agreement", "license_agreement", "lease_agreement"],
    statutory_references=["Restatement (Second) of Contracts SS 200-204"],
    tags=["interpretation", "construction", "parol evidence", "ambiguity"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-CF-006",
    topic="conditions_and_performance",
    domain=DoctrineDomain.CONTRACT_FORMATION,
    title="Conditions Precedent, Concurrent, and Subsequent",
    summary="Conditions qualify contractual duties; they may be precedent, concurrent, or subsequent, and may be express or constructive.",
    content=(
        "A condition precedent is an event that must occur before a duty of performance arises. A condition concurrent requires "
        "simultaneous performance by both parties. A condition subsequent discharges a duty upon the occurrence of an event. Express "
        "conditions require strict compliance; constructive conditions require only substantial performance. Failure of a condition "
        "excuses the other party's duty. Waiver of a condition does not require consideration. Draft conditions with precision: "
        "'Party A's obligation to close is subject to the following conditions precedent: (a) ...; (b) ....' Avoid using 'provided "
        "that' ambiguously; instead specify whether language creates a condition or a covenant."
    ),
    key_elements=["condition precedent", "condition concurrent", "condition subsequent", "strict compliance", "substantial performance"],
    applicable_document_types=["sales_agreement", "purchase_agreement", "merger_agreement", "loan_agreement"],
    statutory_references=["Restatement (Second) of Contracts SS 224-229"],
    tags=["conditions", "performance", "precedent", "concurrent"],
    template_clauses=["The obligations of Buyer under this Agreement are subject to the satisfaction of the following conditions precedent:"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-CF-007",
    topic="breach_and_remedies",
    domain=DoctrineDomain.CONTRACT_FORMATION,
    title="Breach of Contract and Remedies",
    summary="Breach may be material or minor; remedies include compensatory damages, specific performance, rescission, and restitution.",
    content=(
        "A material breach excuses the non-breaching party from further performance and entitles them to damages. A minor breach "
        "allows damages but does not excuse performance. Anticipatory repudiation occurs when a party unequivocally indicates intent "
        "not to perform. Compensatory damages aim to put the non-breaching party in the position they would have been in had the "
        "contract been performed (expectation interest). Consequential damages are recoverable if foreseeable at contract formation "
        "(Hadley v. Baxendale). Specific performance is available when damages are inadequate, typically for unique goods or real "
        "property. Liquidated damages clauses are enforceable if they represent a reasonable estimate of anticipated harm and actual "
        "damages are difficult to calculate. When drafting, include clear cure periods, notice requirements for default, and specify "
        "available remedies."
    ),
    key_elements=["material breach", "minor breach", "compensatory damages", "specific performance", "liquidated damages"],
    applicable_document_types=["sales_agreement", "service_agreement", "license_agreement", "lease_agreement"],
    statutory_references=["Restatement (Second) of Contracts SS 235-257", "UCC 2-711 to 2-717"],
    tags=["breach", "damages", "remedies", "specific performance"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-CF-008",
    topic="defenses_to_formation",
    domain=DoctrineDomain.CONTRACT_FORMATION,
    title="Defenses to Contract Formation",
    summary="Defenses include mutual mistake, unilateral mistake, misrepresentation, duress, undue influence, and unconscionability.",
    content=(
        "Mutual mistake of a material fact existing at contract formation renders the contract voidable by the adversely affected party. "
        "Unilateral mistake is a defense only if the other party knew or should have known of the mistake. Fraudulent misrepresentation "
        "requires a false statement of material fact, knowledge of falsity, intent to induce reliance, justifiable reliance, and damages. "
        "Duress involves a wrongful threat that overcomes free will. Undue influence arises from a relationship of trust exploited to "
        "obtain consent. Unconscionability (procedural and substantive) permits a court to refuse enforcement. When drafting, include "
        "representations of voluntary execution, adequate time for review, and opportunity to consult counsel."
    ),
    key_elements=["mutual mistake", "fraudulent misrepresentation", "duress", "undue influence", "unconscionability"],
    applicable_document_types=["sales_agreement", "service_agreement", "settlement_agreement"],
    statutory_references=["Restatement (Second) of Contracts SS 151-177", "UCC 2-302"],
    tags=["defenses", "mistake", "fraud", "duress", "unconscionability"],
))

# ---------- UCC ARTICLE 2 (9-14) ----------

_add(DoctrineBlock(
    doctrine_id="LG04-UCC-001",
    topic="ucc_scope_and_applicability",
    domain=DoctrineDomain.UCC_ARTICLE_2,
    title="UCC Article 2 Scope",
    summary="UCC Article 2 governs transactions in goods; mixed transactions use the predominant purpose test.",
    content=(
        "UCC Article 2 applies to transactions in goods, defined as movable personal property (UCC 2-105). For mixed contracts "
        "involving both goods and services, courts apply the predominant purpose test to determine whether Article 2 governs. "
        "Merchants are held to higher standards under several provisions (UCC 2-104). Article 2 gap-fillers supply missing terms "
        "for price (2-305), delivery (2-308), time of payment (2-310), and quantity in requirements/output contracts (2-306). "
        "The battle of the forms (2-207) replaces the common law mirror image rule: additional terms in acceptance become part "
        "of the contract between merchants unless they materially alter the offer. When drafting sales agreements, clearly "
        "identify goods, specify whether UCC or common law governs, and address gap-filler defaults explicitly."
    ),
    key_elements=["goods", "predominant purpose test", "merchants", "gap-fillers", "battle of the forms"],
    applicable_document_types=["sales_agreement", "supply_agreement", "distribution_agreement"],
    statutory_references=["UCC 2-102", "UCC 2-104", "UCC 2-105", "UCC 2-207"],
    tags=["UCC", "goods", "merchants", "Article 2"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-UCC-002",
    topic="ucc_warranties",
    domain=DoctrineDomain.UCC_ARTICLE_2,
    title="UCC Warranties: Express, Implied, and Disclaimers",
    summary="Article 2 provides express warranties, implied warranty of merchantability, and implied warranty of fitness for a particular purpose.",
    content=(
        "Express warranties arise from affirmations of fact, descriptions, or samples (UCC 2-313). The implied warranty of "
        "merchantability requires goods to pass without objection in the trade, be fit for ordinary purposes, be adequately "
        "contained and labeled, and conform to promises on the label (UCC 2-314). The implied warranty of fitness for a particular "
        "purpose arises when the seller knows the buyer's particular purpose and the buyer relies on the seller's expertise (UCC "
        "2-315). Disclaimers of merchantability must mention 'merchantability' and be conspicuous. Fitness disclaimers must be in "
        "writing and conspicuous. 'AS IS' or 'WITH ALL FAULTS' disclaims all implied warranties. Limitation of remedies to repair "
        "or replacement is common. When drafting, explicitly address warranty scope and conspicuous disclaimers."
    ),
    key_elements=["express warranty", "merchantability", "fitness for purpose", "disclaimer", "conspicuous"],
    applicable_document_types=["sales_agreement", "supply_agreement", "distribution_agreement"],
    statutory_references=["UCC 2-313", "UCC 2-314", "UCC 2-315", "UCC 2-316"],
    tags=["warranties", "merchantability", "disclaimer", "AS IS"],
    template_clauses=[
        "THE GOODS ARE PROVIDED 'AS IS' WITHOUT WARRANTY OF ANY KIND. SELLER DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, "
        "INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE."
    ],
))

_add(DoctrineBlock(
    doctrine_id="LG04-UCC-003",
    topic="ucc_risk_of_loss",
    domain=DoctrineDomain.UCC_ARTICLE_2,
    title="Risk of Loss and Delivery Terms",
    summary="Risk of loss shifts from seller to buyer based on delivery terms (FOB, FAS, CIF) and whether a breach has occurred.",
    content=(
        "Without breach, risk passes upon tender of delivery at the seller's place of business if no shipment required (2-509). "
        "For shipment contracts (FOB origin), risk passes upon delivery to the carrier. For destination contracts (FOB destination), "
        "risk passes upon tender at destination. If goods are held by a bailee, risk passes upon receipt of a negotiable document "
        "of title. Breach by seller allows buyer to treat risk as remaining with seller until cure or acceptance. Incoterms "
        "(ICC publication) provide internationally recognized delivery terms. When drafting, specify delivery terms explicitly "
        "using either UCC terminology or Incoterms 2020."
    ),
    key_elements=["FOB", "shipment vs destination", "tender", "bailee", "Incoterms"],
    applicable_document_types=["sales_agreement", "supply_agreement", "distribution_agreement"],
    statutory_references=["UCC 2-319", "UCC 2-509", "UCC 2-510"],
    tags=["risk of loss", "delivery", "FOB", "Incoterms"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-UCC-004",
    topic="ucc_remedies",
    domain=DoctrineDomain.UCC_ARTICLE_2,
    title="UCC Buyer and Seller Remedies",
    summary="Article 2 provides specific remedies for buyer and seller upon breach, including cover, resale, and market price damages.",
    content=(
        "Buyer's remedies upon seller's breach: (1) cover and recover difference (2-712); (2) market price damages (2-713); "
        "(3) specific performance for unique goods (2-716); (4) recover goods identified to contract (2-502). Buyer must act in "
        "good faith and within reasonable time. Seller's remedies upon buyer's breach: (1) withhold delivery (2-703); (2) resale "
        "damages (2-706); (3) market price damages (2-708); (4) lost profits if market damages inadequate (2-708(2)); (5) recover "
        "price of accepted goods (2-709). Both parties may recover incidental damages. Buyer may recover consequential damages. "
        "When drafting, specify remedy elections, cure periods, and any contractual limitations on remedies."
    ),
    key_elements=["cover", "resale", "market price", "specific performance", "lost profits"],
    applicable_document_types=["sales_agreement", "supply_agreement"],
    statutory_references=["UCC 2-702 to 2-717"],
    tags=["remedies", "cover", "damages", "resale"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-UCC-005",
    topic="ucc_perfect_tender",
    domain=DoctrineDomain.UCC_ARTICLE_2,
    title="Perfect Tender Rule and Acceptance",
    summary="Under the perfect tender rule, buyer may reject goods that fail to conform in any respect to the contract.",
    content=(
        "The perfect tender rule (UCC 2-601) allows buyer to accept all, reject all, or accept some commercial units and reject "
        "the rest if goods fail to conform in any respect. Buyer must inspect within a reasonable time (2-513) and notify seller "
        "of rejection within a reasonable time (2-602). Acceptance occurs when buyer signifies acceptance, fails to make effective "
        "rejection, or does any act inconsistent with seller's ownership (2-606). Revocation of acceptance requires a non-conformity "
        "that substantially impairs value and must occur within a reasonable time (2-608). Seller has the right to cure non-conforming "
        "tender before time for performance expires (2-508). Installment contracts require substantial impairment of the whole for "
        "cancellation (2-612)."
    ),
    key_elements=["perfect tender", "rejection", "acceptance", "revocation", "cure", "installment"],
    applicable_document_types=["sales_agreement", "supply_agreement"],
    statutory_references=["UCC 2-508", "UCC 2-601", "UCC 2-606", "UCC 2-608"],
    tags=["tender", "acceptance", "rejection", "cure"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-UCC-006",
    topic="ucc_modification_and_good_faith",
    domain=DoctrineDomain.UCC_ARTICLE_2,
    title="UCC Modification, Good Faith, and Unconscionability",
    summary="UCC permits modification without consideration but requires good faith; unconscionable terms are unenforceable.",
    content=(
        "UCC 2-209 permits contract modification without additional consideration, but modifications must satisfy good faith. "
        "No-oral-modification clauses are enforceable between merchants (2-209(2)). Good faith for merchants means honesty in "
        "fact and observance of reasonable commercial standards of fair dealing (2-103). Unconscionability (2-302) allows courts "
        "to refuse enforcement of unfair terms. A clause is procedurally unconscionable if there was unfair surprise or unequal "
        "bargaining power. Substantively unconscionable terms are unreasonably favorable to one party. When drafting, include "
        "modification clauses requiring written consent and ensure terms reflect fair dealing."
    ),
    key_elements=["modification without consideration", "good faith", "NOM clause", "unconscionability"],
    applicable_document_types=["sales_agreement", "supply_agreement"],
    statutory_references=["UCC 2-103", "UCC 2-209", "UCC 2-302"],
    tags=["modification", "good faith", "unconscionability"],
))

# ---------- REAL ESTATE (15-21) ----------

_add(DoctrineBlock(
    doctrine_id="LG04-RE-001",
    topic="deed_types",
    domain=DoctrineDomain.REAL_ESTATE,
    title="Types of Deeds and Covenants of Title",
    summary="Deeds transfer real property interests; general warranty, special warranty, and quitclaim deeds provide varying levels of title protection.",
    content=(
        "A general warranty deed provides the broadest protection with six covenants of title: (1) covenant of seisin - grantor "
        "owns the estate conveyed; (2) right to convey - grantor has authority to transfer; (3) covenant against encumbrances - no "
        "undisclosed liens or easements; (4) covenant of quiet enjoyment - grantee will not be disturbed by superior claims; "
        "(5) covenant of warranty - grantor will defend title; (6) covenant of further assurances - grantor will execute additional "
        "documents as needed. Special warranty deed limits covenants to the period of grantor's ownership. Quitclaim deed transfers "
        "whatever interest grantor may have with no warranties. When drafting, identify the deed type, include full legal "
        "description, state consideration, and ensure proper execution and notarization."
    ),
    key_elements=["general warranty", "special warranty", "quitclaim", "covenants of title", "legal description"],
    applicable_document_types=["general_warranty_deed", "special_warranty_deed", "quitclaim_deed"],
    statutory_references=["varies by state"],
    tags=["deed", "warranty", "conveyance", "title"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-RE-002",
    topic="deed_of_trust_mortgage",
    domain=DoctrineDomain.REAL_ESTATE,
    title="Deed of Trust and Mortgage Instruments",
    summary="Security instruments create liens on real property to secure debt obligations.",
    content=(
        "A mortgage is a two-party instrument (mortgagor and mortgagee) creating a lien on real property. A deed of trust is a "
        "three-party instrument (trustor, beneficiary, and trustee) used in title-theory and some lien-theory states. The deed of "
        "trust allows non-judicial foreclosure through the power of sale, typically faster and less expensive than judicial "
        "foreclosure. Required elements: identification of parties, property description, obligation secured, default terms, "
        "acceleration clause, and foreclosure procedures. Texas uses deeds of trust exclusively. Include covenants requiring "
        "maintenance of insurance, payment of taxes, and preservation of property value. Assignment of rents clause provides "
        "additional security for income-producing properties."
    ),
    key_elements=["mortgage", "deed of trust", "power of sale", "acceleration", "non-judicial foreclosure"],
    applicable_document_types=["deed_of_trust", "mortgage"],
    jurisdictional_notes="Texas uses deeds of trust; some states use mortgages exclusively",
    statutory_references=["TX Prop. Code Ch. 51", "varies by state"],
    tags=["mortgage", "deed of trust", "foreclosure", "security"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-RE-003",
    topic="real_estate_purchase_agreement",
    domain=DoctrineDomain.REAL_ESTATE,
    title="Real Estate Purchase Agreement Essentials",
    summary="Purchase agreements for real property must include parties, property description, price, financing, contingencies, and closing terms.",
    content=(
        "Essential elements of a real estate purchase agreement: (1) identification of buyer and seller; (2) legal description of "
        "property; (3) purchase price and earnest money deposit; (4) financing contingency with mortgage commitment deadline; "
        "(5) inspection contingency with scope and deadline; (6) title contingency requiring marketable/insurable title; "
        "(7) closing date, location, and escrow agent; (8) prorations of taxes, rents, and assessments; (9) fixtures and personal "
        "property included/excluded; (10) risk of loss allocation; (11) default remedies; (12) condition of property representations. "
        "Additional provisions may include: HOA disclosure, lead-based paint disclosure (pre-1978 housing), environmental conditions, "
        "survey requirements, and assignability."
    ),
    key_elements=["legal description", "purchase price", "contingencies", "closing", "title", "earnest money"],
    applicable_document_types=["purchase_agreement"],
    statutory_references=["varies by state", "42 U.S.C. 4852d (lead paint)"],
    tags=["purchase agreement", "real estate", "contingency", "closing"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-RE-004",
    topic="commercial_lease",
    domain=DoctrineDomain.REAL_ESTATE,
    title="Commercial Lease Agreements",
    summary="Commercial leases grant possession of premises for business use with negotiated terms for rent, maintenance, insurance, and renewal.",
    content=(
        "Commercial leases are highly negotiated instruments. Key provisions include: (1) premises description with square footage "
        "and common area definitions; (2) rent structure (gross, net, NNN, percentage, escalation); (3) lease term with commencement "
        "and expiration; (4) permitted use and exclusivity; (5) CAM charges allocation and audit rights; (6) insurance requirements "
        "(CGL, property, business interruption); (7) maintenance and repair obligations; (8) improvements and tenant buildout (TI "
        "allowance); (9) assignment and subletting restrictions; (10) default and remedies; (11) renewal options; (12) subordination, "
        "non-disturbance, and attornment (SNDA). Triple-net leases shift insurance, taxes, and maintenance to tenant. Percentage "
        "rent requires defined gross sales and breakpoints."
    ),
    key_elements=["NNN", "CAM", "TI allowance", "SNDA", "percentage rent", "permitted use"],
    applicable_document_types=["lease_agreement"],
    tags=["lease", "commercial", "NNN", "CAM", "rent"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-RE-005",
    topic="easements",
    domain=DoctrineDomain.REAL_ESTATE,
    title="Easement Drafting",
    summary="Easements grant non-possessory interests in land; they may be appurtenant or in gross, express or prescriptive.",
    content=(
        "An easement appurtenant benefits a dominant estate and burdens a servient estate, running with the land. An easement in "
        "gross benefits a person or entity rather than a parcel of land. Express easements must comply with the Statute of Frauds. "
        "Implied easements arise from prior use, necessity, or plat maps. Prescriptive easements require open, notorious, hostile, "
        "continuous use for the statutory period. Conservation easements restrict development rights and may provide tax benefits. "
        "When drafting an express easement: precisely describe the location and dimensions, specify the scope of permissible use, "
        "address maintenance obligations, include indemnification, specify termination conditions, and record the instrument."
    ),
    key_elements=["appurtenant", "in gross", "prescriptive", "conservation", "scope of use", "recording"],
    applicable_document_types=["easement"],
    tags=["easement", "right of way", "servitude", "dominant estate"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-RE-006",
    topic="title_insurance",
    domain=DoctrineDomain.REAL_ESTATE,
    title="Title Insurance and Title Examination",
    summary="Title insurance protects against defects in title discovered after closing; a commitment for title insurance identifies requirements and exceptions.",
    content=(
        "A title commitment consists of Schedule A (property description, proposed insured, type of policy), Schedule B-I "
        "(requirements to be satisfied before policy issuance), and Schedule B-II (exceptions from coverage). Standard exceptions "
        "include: survey matters, unrecorded easements, parties in possession, mechanic's liens, and taxes not yet due. Extended "
        "coverage removes many standard exceptions but requires a survey. Owner's policy protects the buyer; lender's policy "
        "protects the mortgagee. The title examiner searches public records (recorder's office, tax records, court records) to "
        "establish chain of title. When drafting purchase agreements, specify title insurance requirements, objection periods, "
        "and cure mechanisms for title defects."
    ),
    key_elements=["commitment", "Schedule B exceptions", "extended coverage", "chain of title", "standard exceptions"],
    applicable_document_types=["purchase_agreement", "deed_of_trust"],
    tags=["title insurance", "title examination", "commitment", "exceptions"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-RE-007",
    topic="restrictive_covenants",
    domain=DoctrineDomain.REAL_ESTATE,
    title="Restrictive Covenants and CC&Rs",
    summary="Restrictive covenants limit land use and run with the land when they touch and concern the land and there is privity.",
    content=(
        "Covenants, conditions, and restrictions (CC&Rs) are equitable servitudes that restrict land use within a development. "
        "For a covenant to run with the land at law, it must: (1) be in writing; (2) intend to run; (3) touch and concern the "
        "land; (4) have horizontal and vertical privity. Equitable servitudes require only notice and intent to bind successors. "
        "Common restrictions include: use limitations, architectural controls, setback requirements, and maintenance obligations. "
        "Amendment requires consent of a specified percentage of lot owners. Enforcement is by injunction or damages. When "
        "drafting, clearly state the burdened and benefited parcels, the restriction, duration, enforcement mechanism, and "
        "amendment procedure."
    ),
    key_elements=["CC&Rs", "touch and concern", "privity", "equitable servitude", "amendment"],
    applicable_document_types=["restrictive_covenant"],
    tags=["covenant", "CC&R", "restriction", "land use"],
))

# ---------- EMPLOYMENT (22-27) ----------

_add(DoctrineBlock(
    doctrine_id="LG04-EM-001",
    topic="at_will_employment",
    domain=DoctrineDomain.EMPLOYMENT,
    title="At-Will Employment Doctrine",
    summary="At-will employment allows either party to terminate the relationship at any time for any lawful reason without notice.",
    content=(
        "The default rule in 49 states (Montana excepted) is at-will employment. Exceptions include: (1) implied contract from "
        "handbooks or policies; (2) implied covenant of good faith and fair dealing (recognized in some states); (3) public policy "
        "exception (termination for refusing to violate law, exercising statutory right, or whistleblowing); (4) promissory estoppel. "
        "When drafting employment agreements, include a clear at-will statement: 'This Agreement does not guarantee employment for "
        "any specific duration. Either party may terminate the employment relationship at any time, with or without cause and with "
        "or without notice.' Ensure the at-will language is not contradicted by other provisions."
    ),
    key_elements=["at-will", "exceptions", "implied contract", "public policy", "good faith"],
    applicable_document_types=["employment_agreement", "offer_letter"],
    tags=["employment", "at-will", "termination", "discharge"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-EM-002",
    topic="non_compete_agreements",
    domain=DoctrineDomain.EMPLOYMENT,
    title="Non-Compete Agreement Enforceability",
    summary="Non-compete agreements must be reasonable in scope, duration, and geographic area to be enforceable.",
    content=(
        "Enforceability of non-compete agreements varies significantly by jurisdiction. California (Bus. & Prof. Code 16600) "
        "generally prohibits non-competes except in the sale of business context. Texas (Bus. & Com. Code 15.50) requires "
        "that the covenant be ancillary to an otherwise enforceable agreement with consideration. General enforceability "
        "requirements: (1) supported by adequate consideration (continued employment may suffice in some states); (2) reasonable "
        "temporal scope (typically 1-2 years); (3) reasonable geographic scope (tied to employer's actual market); (4) reasonable "
        "activity scope (limited to actual competitive activities); (5) protects legitimate business interest (trade secrets, "
        "customer relationships, specialized training). Some courts blue-pencil or reform overbroad covenants."
    ),
    key_elements=["reasonableness", "geographic scope", "temporal scope", "activity scope", "legitimate business interest"],
    applicable_document_types=["non_compete", "employment_agreement"],
    jurisdictional_notes="California generally prohibits; Texas requires ancillary agreement; varies widely by state",
    statutory_references=["CA Bus. & Prof. Code 16600", "TX Bus. & Com. Code 15.50"],
    tags=["non-compete", "restrictive covenant", "enforceability"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-EM-003",
    topic="confidentiality_nda",
    domain=DoctrineDomain.EMPLOYMENT,
    title="Confidentiality and Non-Disclosure Agreements",
    summary="NDAs protect confidential information by defining what is covered, obligations, exclusions, and remedies for breach.",
    content=(
        "An effective NDA includes: (1) clear definition of confidential information (including carve-outs for publicly known "
        "information, independently developed information, and information received from third parties); (2) obligations of "
        "receiving party (use only for permitted purposes, restrict access to need-to-know); (3) duration of confidentiality "
        "obligation (typically 2-5 years; trade secrets may be indefinite); (4) permitted disclosures (required by law, court "
        "order with prior notice); (5) return or destruction of materials upon termination; (6) remedies including injunctive "
        "relief and liquidated damages. Mutual NDAs are common in potential business transactions. When drafting, be specific "
        "about what constitutes confidential information and avoid overbroad definitions that could be challenged."
    ),
    key_elements=["confidential information", "exclusions", "duration", "return of materials", "injunctive relief"],
    applicable_document_types=["nda", "employment_agreement", "service_agreement"],
    tags=["NDA", "confidentiality", "trade secrets", "non-disclosure"],
    template_clauses=[
        "\"Confidential Information\" means all non-public information disclosed by the Disclosing Party to the Receiving Party, "
        "whether orally, in writing, or by inspection, that is designated as confidential or that a reasonable person would "
        "understand to be confidential given the nature of the information and circumstances of disclosure."
    ],
))

_add(DoctrineBlock(
    doctrine_id="LG04-EM-004",
    topic="severance_agreement",
    domain=DoctrineDomain.EMPLOYMENT,
    title="Severance Agreements and Releases",
    summary="Severance agreements provide benefits in exchange for a general release of claims; OWBPA requirements apply for age-related releases.",
    content=(
        "Severance agreements typically include: (1) separation date and final payments; (2) severance benefits (lump sum or "
        "continuation); (3) general release of all claims; (4) confidentiality of agreement terms; (5) non-disparagement; "
        "(6) cooperation clause; (7) return of company property. OWBPA requirements for age discrimination releases (40+ "
        "employees): (a) written in plain language; (b) specifically references ADEA claims; (c) does not waive future claims; "
        "(d) provides consideration beyond what employee is already entitled to; (e) advises consulting an attorney; (f) provides "
        "21 days to consider (45 days for group layoffs); (g) provides 7-day revocation period. When drafting, ensure compliance "
        "with OWBPA, state-specific requirements, and carve out non-waivable claims."
    ),
    key_elements=["general release", "OWBPA", "consideration period", "revocation period", "non-disparagement"],
    applicable_document_types=["severance_agreement"],
    statutory_references=["OWBPA (29 U.S.C. 626(f))", "ADEA"],
    tags=["severance", "release", "OWBPA", "separation"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-EM-005",
    topic="independent_contractor",
    domain=DoctrineDomain.EMPLOYMENT,
    title="Independent Contractor Agreements",
    summary="Proper classification and contractual language distinguish independent contractors from employees for tax and liability purposes.",
    content=(
        "Misclassification carries significant tax, benefit, and liability consequences. IRS uses common law factors grouped into "
        "three categories: (1) behavioral control (instructions, training); (2) financial control (expenses, investment, profit "
        "opportunity); (3) relationship type (written contracts, benefits, permanency). ABC test (used in CA under AB5 and other "
        "states): worker is IC only if (A) free from control; (B) performs work outside usual course of business; (C) engaged "
        "in independently established trade. When drafting IC agreements: clearly state independent contractor status, specify "
        "deliverables not hours, allow contractor to control method and means, require contractor's own tools and insurance, "
        "specify tax obligations (1099 vs W-2), and include indemnification for misclassification claims."
    ),
    key_elements=["behavioral control", "financial control", "ABC test", "1099", "misclassification"],
    applicable_document_types=["independent_contractor"],
    statutory_references=["IRS Rev. Rul. 87-41", "CA AB5", "26 U.S.C. 3509"],
    tags=["independent contractor", "misclassification", "ABC test", "1099"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-EM-006",
    topic="ip_assignment_employment",
    domain=DoctrineDomain.EMPLOYMENT,
    title="Intellectual Property Assignment in Employment",
    summary="Employment agreements should include clear IP assignment provisions; some states protect employee inventions created on own time.",
    content=(
        "Work made for hire doctrine (17 U.S.C. 101) automatically vests copyright ownership in the employer for works created "
        "within the scope of employment. For patents and other IP, explicit assignment language is necessary. A present assignment "
        "('hereby assigns') is stronger than an agreement to assign ('agrees to assign'). Some states (CA Lab. Code 2870, DE "
        "Code Tit. 19 SS 805, IL 765 ILCS 1060/2) protect employee inventions created entirely on own time without employer "
        "resources and unrelated to employer's business. When drafting: include broad IP assignment covering inventions, works "
        "of authorship, and ideas; add disclosure obligation; include cooperation clause for patent prosecution; address prior "
        "inventions with an exclusion schedule; comply with state-specific limitations."
    ),
    key_elements=["work for hire", "present assignment", "prior inventions", "disclosure obligation", "state limitations"],
    applicable_document_types=["employment_agreement", "independent_contractor", "patent_assignment"],
    statutory_references=["17 U.S.C. 101", "CA Lab. Code 2870", "35 U.S.C. 261"],
    tags=["IP assignment", "work for hire", "patent", "copyright", "employee inventions"],
))

# ---------- CORPORATE (28-32) ----------

_add(DoctrineBlock(
    doctrine_id="LG04-CO-001",
    topic="articles_of_incorporation",
    domain=DoctrineDomain.CORPORATE,
    title="Articles of Incorporation",
    summary="Articles of incorporation are the charter document filed with the state to create a corporation.",
    content=(
        "Required elements (vary by state but generally include): (1) corporate name (must include Corp., Inc., or equivalent); "
        "(2) registered agent and registered office address; (3) number of authorized shares (by class with par value or no par); "
        "(4) incorporator name and address; (5) purpose clause (may be general: 'any lawful business'). Optional provisions: "
        "preemptive rights, cumulative voting, indemnification beyond statutory minimum, limitation of director personal liability "
        "(Del. 102(b)(7)), supermajority voting requirements, staggered board, restrictions on transfer. Delaware is the preferred "
        "incorporation state for public companies due to well-developed case law and the Court of Chancery. When drafting, consider "
        "future capital needs (authorize sufficient shares), protective provisions, and flexibility for governance changes."
    ),
    key_elements=["corporate name", "authorized shares", "registered agent", "102(b)(7)", "purpose clause"],
    applicable_document_types=["articles_of_incorporation"],
    statutory_references=["DGCL SS 101-102", "MBCA SS 2.01-2.06"],
    tags=["incorporation", "charter", "corporate", "Delaware"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-CO-002",
    topic="bylaws",
    domain=DoctrineDomain.CORPORATE,
    title="Corporate Bylaws",
    summary="Bylaws govern internal corporate operations including board procedures, officer duties, shareholder meetings, and amendment processes.",
    content=(
        "Bylaws typically address: (1) offices and fiscal year; (2) shareholder meetings (annual, special, notice, quorum, "
        "proxies, voting, record date, action without meeting); (3) board of directors (number, qualifications, election, "
        "term, vacancies, removal, resignation, meetings, quorum, committees, action without meeting, compensation); "
        "(4) officers (titles, duties, election, removal, compensation); (5) stock (certificates, transfers, lost certificates, "
        "record holders); (6) indemnification (directors, officers, agents, advancement of expenses); (7) dividends; "
        "(8) corporate seal; (9) amendments. Bylaws may be amended by the board or shareholders as specified. Ensure consistency "
        "with the articles of incorporation and applicable state law."
    ),
    key_elements=["shareholder meetings", "board procedures", "officers", "indemnification", "amendments"],
    applicable_document_types=["bylaws"],
    statutory_references=["DGCL SS 109, 141-146", "MBCA SS 2.06, 7.22, 8.01-8.56"],
    tags=["bylaws", "governance", "board", "shareholders"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-CO-003",
    topic="llc_operating_agreement",
    domain=DoctrineDomain.CORPORATE,
    title="LLC Operating Agreement",
    summary="The operating agreement is the governing document of an LLC, defining member rights, management structure, and economic terms.",
    content=(
        "Key provisions: (1) formation and purpose; (2) capital contributions and capital accounts; (3) management structure "
        "(member-managed vs manager-managed); (4) voting rights and decision-making thresholds; (5) allocations of profits "
        "and losses (must comply with Subchapter K if partnership-taxed); (6) distributions (timing, priority, tax distributions); "
        "(7) transfer restrictions (right of first refusal, tag-along, drag-along); (8) admission of new members; (9) withdrawal "
        "and buyout provisions; (10) dissolution triggers and winding up; (11) fiduciary duties (may be modified in many states); "
        "(12) indemnification; (13) books, records, and tax matters partner. Delaware LLC Act (6 Del. C. Ch. 18) gives maximum "
        "flexibility to the operating agreement. In single-member LLCs, the operating agreement helps establish the entity as "
        "separate from its owner."
    ),
    key_elements=["member-managed vs manager-managed", "capital accounts", "transfer restrictions", "distributions", "fiduciary duties"],
    applicable_document_types=["operating_agreement"],
    statutory_references=["DLLCA (6 Del. C. Ch. 18)", "RULLCA"],
    tags=["LLC", "operating agreement", "members", "management"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-CO-004",
    topic="board_resolutions",
    domain=DoctrineDomain.CORPORATE,
    title="Board Resolutions and Consent Actions",
    summary="Board resolutions formally authorize corporate actions; written consents allow action without a meeting.",
    content=(
        "A board resolution is a formal written record of a decision made by the board of directors. Required for: major contracts, "
        "borrowing, officer elections, dividend declarations, stock issuances, mergers, and asset sales. Format: title, recitals "
        "(WHEREAS clauses), resolutions (RESOLVED clauses), authorization (BE IT FURTHER RESOLVED), and certification. Written "
        "consent in lieu of meeting must be signed by all directors (DGCL 141(f)) or shareholders holding the minimum votes "
        "required for the action (DGCL 228). Include a certification by the Secretary attesting that the resolution was duly "
        "adopted. Banks and third parties often require certified resolutions to verify corporate authority."
    ),
    key_elements=["WHEREAS", "RESOLVED", "certification", "written consent", "authority verification"],
    applicable_document_types=["board_resolution"],
    statutory_references=["DGCL SS 141(f), 228"],
    tags=["resolution", "board", "consent", "corporate action"],
    template_clauses=[
        "RESOLVED, that the officers of the Corporation are hereby authorized to execute and deliver any and all documents and "
        "instruments and to take any and all actions as they may deem necessary or appropriate to effectuate the purposes of the "
        "foregoing resolutions."
    ],
))

_add(DoctrineBlock(
    doctrine_id="LG04-CO-005",
    topic="shareholder_agreement",
    domain=DoctrineDomain.CORPORATE,
    title="Shareholder Agreements",
    summary="Shareholder agreements regulate the relationship among shareholders including transfer restrictions, governance, and exit rights.",
    content=(
        "Key provisions: (1) transfer restrictions (right of first refusal, right of first offer, consent requirements); "
        "(2) tag-along rights (minority can join a sale by majority); (3) drag-along rights (majority can force minority to "
        "join); (4) preemptive rights (participate in new issuances); (5) anti-dilution protection (for preferred holders); "
        "(6) board composition and voting agreements; (7) information rights; (8) buy-sell provisions (cross-purchase, "
        "redemption, or hybrid); (9) valuation methodology (formula, appraisal, fair market value); (10) triggering events "
        "(death, disability, retirement, termination, divorce); (11) funding mechanism (insurance, installment payments); "
        "(12) deadlock resolution. When drafting, ensure consistency with articles, bylaws, and any preferred stock terms."
    ),
    key_elements=["ROFR", "tag-along", "drag-along", "buy-sell", "anti-dilution", "preemptive rights"],
    applicable_document_types=["shareholder_agreement", "stock_purchase_agreement"],
    tags=["shareholder", "buy-sell", "transfer restriction", "governance"],
))

# ---------- IP (33-35) ----------

_add(DoctrineBlock(
    doctrine_id="LG04-IP-001",
    topic="patent_assignment",
    domain=DoctrineDomain.INTELLECTUAL_PROPERTY,
    title="Patent Assignment Agreements",
    summary="Patent assignments transfer ownership of patent rights; must be in writing and recorded with the USPTO.",
    content=(
        "A patent assignment transfers all right, title, and interest in a patent or patent application. Must be in writing "
        "and signed by the assignor (35 U.S.C. 261). Recording with USPTO (Electronic Patent Assignment System) provides "
        "constructive notice. Key provisions: (1) identification of patent(s) by number, title, filing date; (2) assignment "
        "of all right, title, and interest including continuations, divisionals, and foreign counterparts; (3) consideration; "
        "(4) cooperation clause for prosecution and enforcement; (5) representations (valid ownership, no encumbrances, no "
        "prior assignments); (6) indemnification for breach of representations. For employee inventions, use present "
        "assignment language ('hereby assigns') rather than future promise ('agrees to assign')."
    ),
    key_elements=["present assignment", "recording", "continuations", "cooperation", "representations"],
    applicable_document_types=["patent_assignment"],
    statutory_references=["35 U.S.C. 261"],
    tags=["patent", "assignment", "IP", "USPTO"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-IP-002",
    topic="software_license",
    domain=DoctrineDomain.INTELLECTUAL_PROPERTY,
    title="Software License Agreements",
    summary="Software licenses grant usage rights without transferring ownership; key terms include scope, restrictions, maintenance, and IP ownership.",
    content=(
        "Software licenses may be perpetual or subscription (SaaS). Key provisions: (1) grant of license (scope, users, "
        "locations, permitted use); (2) restrictions (no reverse engineering, no sublicensing, no modification); (3) intellectual "
        "property ownership (licensor retains all rights); (4) acceptance testing and delivery; (5) maintenance and support "
        "(response times, updates, upgrades, SLA); (6) fees and payment terms; (7) warranty (conformance to specifications, "
        "non-infringement); (8) limitation of liability; (9) indemnification for IP infringement claims; (10) data rights "
        "and privacy; (11) source code escrow; (12) term and termination; (13) transition assistance on termination. For "
        "SaaS, add data portability, uptime SLA, and data processing agreement if personal data involved."
    ),
    key_elements=["license grant", "restrictions", "SLA", "source code escrow", "data portability"],
    applicable_document_types=["software_license", "license_agreement"],
    tags=["software", "license", "SaaS", "IP", "escrow"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-IP-003",
    topic="trademark_license",
    domain=DoctrineDomain.INTELLECTUAL_PROPERTY,
    title="Trademark License Agreements",
    summary="Trademark licenses must include quality control provisions to avoid naked licensing, which can result in abandonment.",
    content=(
        "Trademark licensing requires the licensor to maintain quality control over the licensee's use (naked licensing doctrine). "
        "Key provisions: (1) grant of license (exclusive, non-exclusive, sole); (2) licensed marks identification (registered "
        "marks, applications, common law marks); (3) quality standards and approval process; (4) territory and field of use; "
        "(5) royalties and reporting; (6) usage guidelines (style guides, trademark notice requirements); (7) goodwill inures "
        "to licensor; (8) enforcement (licensor's right and duty to enforce); (9) sublicensing restrictions; (10) term and "
        "termination; (11) wind-down period for inventory. Without adequate quality control, the license is 'naked' and the "
        "mark may be deemed abandoned under 15 U.S.C. 1127."
    ),
    key_elements=["quality control", "naked licensing", "goodwill", "territory", "usage guidelines"],
    applicable_document_types=["trademark_license"],
    statutory_references=["15 U.S.C. 1055", "15 U.S.C. 1127"],
    tags=["trademark", "license", "quality control", "naked licensing"],
))

# ---------- FINANCE (36-39) ----------

_add(DoctrineBlock(
    doctrine_id="LG04-FI-001",
    topic="promissory_note",
    domain=DoctrineDomain.FINANCE,
    title="Promissory Note Essentials",
    summary="A promissory note is an unconditional promise to pay a sum certain, and may be negotiable under UCC Article 3.",
    content=(
        "A negotiable promissory note under UCC 3-104 must: (1) be in writing and signed by the maker; (2) contain an "
        "unconditional promise to pay; (3) state a fixed amount of money; (4) be payable on demand or at a definite time; "
        "(5) be payable to order or bearer; (6) contain no other undertaking or instruction except as permitted. Key drafting "
        "elements: principal amount, interest rate (fixed or variable with reference rate), payment schedule (installments, "
        "balloon, interest-only), maturity date, prepayment rights and penalties, default provisions, acceleration clause, "
        "late fees, attorney's fees, waiver of presentment/demand/protest, governing law. For consumer notes, comply with "
        "TILA disclosure requirements. Secured notes should cross-reference the security agreement or deed of trust."
    ),
    key_elements=["unconditional promise", "sum certain", "negotiability", "acceleration", "prepayment"],
    applicable_document_types=["promissory_note"],
    statutory_references=["UCC 3-104", "TILA (15 U.S.C. 1601)"],
    tags=["promissory note", "negotiable instrument", "loan", "interest"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-FI-002",
    topic="security_agreement",
    domain=DoctrineDomain.FINANCE,
    title="Security Agreements and UCC Article 9",
    summary="Security agreements create security interests in personal property; perfection by filing a UCC-1 financing statement establishes priority.",
    content=(
        "A security agreement must: (1) be authenticated by the debtor; (2) contain a description of the collateral sufficient "
        "to identify it; (3) the secured party must give value; (4) the debtor must have rights in the collateral. Attachment "
        "creates the security interest between the parties. Perfection establishes priority against third parties, typically by "
        "filing a UCC-1 financing statement with the appropriate Secretary of State. Filing office is determined by debtor's "
        "location (state of organization for registered organizations). Types of collateral: accounts, chattel paper, "
        "commercial tort claims, deposit accounts, documents, equipment, general intangibles, goods, instruments, inventory, "
        "investment property, letter-of-credit rights. After-acquired property clauses and future advances are permitted. "
        "Cross-collateralization secures multiple obligations with the same collateral."
    ),
    key_elements=["attachment", "perfection", "UCC-1", "priority", "collateral description", "after-acquired"],
    applicable_document_types=["security_agreement"],
    statutory_references=["UCC 9-102 to 9-709"],
    tags=["security interest", "UCC-1", "perfection", "collateral", "priority"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-FI-003",
    topic="guaranty",
    domain=DoctrineDomain.FINANCE,
    title="Guaranty Agreements",
    summary="A guaranty is a promise to answer for another's debt; it may be limited or unlimited, and conditional or unconditional.",
    content=(
        "Types of guaranties: (1) payment guaranty (guarantor pays when obligation is due, whether or not creditor pursues "
        "debtor first); (2) collection guaranty (guarantor pays only after creditor exhausts remedies against debtor); "
        "(3) limited guaranty (capped amount); (4) unlimited guaranty (full exposure). Key provisions: waivers (presentment, "
        "demand, protest, notice of acceptance, notice of default, suretyship defenses, subrogation until full payment), "
        "continuing guaranty (covers future advances), reinstatement after bankruptcy preference recovery, consent to "
        "modifications without notice, subordination of guarantor's claims. Guaranties must satisfy the Statute of Frauds "
        "(suretyship provision). When drafting, include broad waiver language and ensure the guarantor understands the scope "
        "of obligations."
    ),
    key_elements=["payment vs collection", "limited vs unlimited", "waivers", "continuing", "reinstatement"],
    applicable_document_types=["guaranty"],
    statutory_references=["Restatement (Third) of Suretyship and Guaranty"],
    tags=["guaranty", "surety", "waiver", "collection"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-FI-004",
    topic="loan_agreement",
    domain=DoctrineDomain.FINANCE,
    title="Loan Agreement Structure",
    summary="Loan agreements govern the lending relationship with detailed provisions for disbursement, covenants, default, and remedies.",
    content=(
        "Key sections: (1) definitions; (2) commitment and disbursement (conditions precedent to closing and each advance); "
        "(3) interest rate (fixed, floating with reference rate, SOFR floor, default rate); (4) fees (commitment, origination, "
        "unused line); (5) payments and prepayment (mandatory, optional, premium); (6) representations and warranties (organization, "
        "authority, no conflicts, financial statements, litigation, compliance, taxes, ERISA); (7) affirmative covenants (financial "
        "reporting, insurance, maintenance of existence, payment of taxes); (8) negative covenants (indebtedness limits, liens, "
        "investments, distributions, asset sales, mergers, affiliate transactions); (9) financial covenants (leverage ratio, "
        "interest coverage, minimum EBITDA); (10) events of default; (11) remedies (acceleration, enforcement of security); "
        "(12) agency provisions (for syndicated loans)."
    ),
    key_elements=["conditions precedent", "SOFR", "covenants", "financial covenants", "events of default", "acceleration"],
    applicable_document_types=["loan_agreement"],
    tags=["loan", "credit", "covenants", "default", "SOFR"],
))

# ---------- ESTATE PLANNING (40-43) ----------

_add(DoctrineBlock(
    doctrine_id="LG04-EP-001",
    topic="revocable_living_trust",
    domain=DoctrineDomain.ESTATE_PLANNING,
    title="Revocable Living Trust",
    summary="A revocable living trust avoids probate, provides incapacity planning, and allows flexible asset management during lifetime and after death.",
    content=(
        "A revocable living trust is created during the grantor's lifetime, remains amendable and revocable until death or "
        "incapacity, and becomes irrevocable upon death. Key provisions: (1) identification of grantor, trustee, and successor "
        "trustee; (2) trust property description and funding provisions; (3) distributions during grantor's lifetime; "
        "(4) incapacity provisions (standard for determining incapacity, successor trustee authority); (5) distributions after "
        "death (outright, in trust, at specific ages); (6) spendthrift clause protecting beneficiaries from creditors; "
        "(7) trustee powers (investment, sale, distribution, borrowing); (8) trustee compensation; (9) accounting requirements; "
        "(10) governing law; (11) no-contest clause; (12) trust protector provisions. Must be funded by transferring assets "
        "into the trust to avoid probate. Pour-over will catches unfunded assets."
    ),
    key_elements=["grantor", "trustee", "successor trustee", "spendthrift", "pour-over will", "incapacity"],
    applicable_document_types=["revocable_trust"],
    tags=["trust", "revocable", "estate planning", "probate avoidance"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-EP-002",
    topic="last_will_testament",
    domain=DoctrineDomain.ESTATE_PLANNING,
    title="Last Will and Testament",
    summary="A will disposes of property at death; execution requirements vary by state but generally require writing, signature, and witnesses.",
    content=(
        "Execution requirements (Wills Act formalities): (1) in writing; (2) signed by testator (or at testator's direction); "
        "(3) attested by two (or three) competent witnesses who observe signing or testator's acknowledgment; (4) testator "
        "must have testamentary capacity (know nature and extent of property, natural objects of bounty, nature of testamentary "
        "act); (5) testator must not be subject to undue influence, fraud, or duress. Self-proving affidavit eliminates need "
        "to locate witnesses at probate. Key provisions: executor appointment, guardian designation for minors, specific "
        "bequests, residuary clause, simultaneous death clause, tax apportionment, no-contest clause, trust establishment "
        "provisions. Holographic wills (handwritten, unwitnessed) are valid in some states including Texas."
    ),
    key_elements=["testamentary capacity", "witnesses", "self-proving", "executor", "residuary clause"],
    applicable_document_types=["last_will"],
    jurisdictional_notes="Holographic wills valid in TX, CA, and others; some states require 3 witnesses",
    tags=["will", "testament", "probate", "executor", "beneficiary"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-EP-003",
    topic="power_of_attorney",
    domain=DoctrineDomain.ESTATE_PLANNING,
    title="Durable Power of Attorney",
    summary="A durable power of attorney grants authority to an agent that survives the principal's incapacity.",
    content=(
        "A durable power of attorney includes language such as 'This power of attorney shall not be affected by the subsequent "
        "disability or incapacity of the principal' (Uniform Power of Attorney Act). Types: (1) general POA (broad authority); "
        "(2) limited/special POA (specific transactions); (3) springing POA (effective only upon incapacity). Powers to enumerate: "
        "real property transactions, financial institution transactions, stock and bond transactions, entity transactions, insurance "
        "transactions, estate transactions, claims and litigation, personal and family maintenance, government benefits, retirement "
        "plan transactions, tax matters, gift making (requires express authorization). Agent owes fiduciary duties of loyalty, "
        "care, and accounting. Some states require notarization and/or recording for real property transactions."
    ),
    key_elements=["durable", "springing", "fiduciary duty", "specific powers", "incapacity"],
    applicable_document_types=["power_of_attorney"],
    statutory_references=["Uniform Power of Attorney Act", "varies by state"],
    tags=["power of attorney", "POA", "durable", "agent", "fiduciary"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-EP-004",
    topic="healthcare_directive",
    domain=DoctrineDomain.ESTATE_PLANNING,
    title="Advance Healthcare Directive",
    summary="Healthcare directives express end-of-life wishes and designate a healthcare agent for medical decisions during incapacity.",
    content=(
        "An advance healthcare directive combines: (1) living will (instructions for end-of-life care, life-sustaining treatment, "
        "artificial nutrition/hydration, pain management); (2) healthcare power of attorney (designation of agent for medical "
        "decisions). Agent authority typically includes: consent to or refuse treatment, access medical records, authorize "
        "organ donation, make disposition of remains decisions. HIPAA authorization should be included to allow agent access "
        "to protected health information. The directive should specify conditions under which it becomes effective (typically "
        "two physicians certifying incapacity or terminal condition). Many states have statutory forms. When drafting, ensure "
        "compliance with state-specific requirements and include HIPAA release."
    ),
    key_elements=["living will", "healthcare agent", "HIPAA", "end-of-life", "terminal condition"],
    applicable_document_types=["healthcare_directive"],
    statutory_references=["UHCDA", "HIPAA (45 CFR 164.502)"],
    tags=["healthcare directive", "living will", "HIPAA", "advance directive"],
))

# ---------- M&A (44-47) ----------

_add(DoctrineBlock(
    doctrine_id="LG04-MA-001",
    topic="merger_agreement_structure",
    domain=DoctrineDomain.MERGER_ACQUISITION,
    title="Merger Agreement Structure",
    summary="Merger agreements are complex instruments governing the combination of two entities with detailed representations, covenants, and closing conditions.",
    content=(
        "Standard structure of a merger agreement: (1) recitals and definitions; (2) the merger (structure, effective time, "
        "certificate of merger); (3) merger consideration (cash, stock, mixed, earnout); (4) conversion of shares; (5) exchange "
        "procedures; (6) representations and warranties of target (30-50+ reps covering organization, authority, capitalization, "
        "financial statements, absence of changes, compliance, litigation, IP, real property, contracts, employees, taxes, "
        "environmental, insurance, brokers); (7) reps of acquiror; (8) covenants (interim operations, access, regulatory "
        "filings, no-shop/go-shop, efforts to close); (9) conditions to closing; (10) termination (triggers, termination "
        "fee, reverse termination fee); (11) indemnification or R&W insurance; (12) miscellaneous. Material adverse effect "
        "definition is heavily negotiated."
    ),
    key_elements=["MAE", "representations", "no-shop", "termination fee", "earnout", "indemnification"],
    applicable_document_types=["merger_agreement"],
    tags=["merger", "acquisition", "M&A", "MAE", "closing conditions"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-MA-002",
    topic="due_diligence",
    domain=DoctrineDomain.MERGER_ACQUISITION,
    title="Due Diligence in M&A Transactions",
    summary="Due diligence is the investigation process preceding an acquisition to verify target representations and identify risks.",
    content=(
        "Due diligence categories: (1) corporate (organizational documents, minutes, resolutions, good standing); (2) financial "
        "(audited/unaudited financials, working capital analysis, debt schedule, projections); (3) contracts (material agreements, "
        "change of control provisions, assignability); (4) employees (key employees, compensation, benefits, ERISA compliance, "
        "labor disputes); (5) intellectual property (patents, trademarks, copyrights, trade secrets, licenses); (6) real property "
        "(owned and leased, environmental assessments, zoning); (7) litigation (pending, threatened, settled, insurance coverage); "
        "(8) tax (returns, audits, tax attributes, transfer pricing); (9) regulatory (permits, licenses, compliance history); "
        "(10) environmental (Phase I/II assessments, remediation obligations); (11) insurance (coverage, claims history); "
        "(12) cybersecurity and data privacy. Organize via virtual data room with indexed folders."
    ),
    key_elements=["data room", "material contracts", "change of control", "ERISA", "environmental"],
    applicable_document_types=["merger_agreement", "asset_purchase_agreement"],
    tags=["due diligence", "M&A", "data room", "investigation"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-MA-003",
    topic="letter_of_intent",
    domain=DoctrineDomain.MERGER_ACQUISITION,
    title="Letter of Intent / Term Sheet",
    summary="Letters of intent outline principal terms of a proposed transaction; most provisions are non-binding except exclusivity and confidentiality.",
    content=(
        "A letter of intent (LOI) or term sheet typically includes: (1) transaction structure (asset purchase, stock purchase, "
        "merger); (2) purchase price and form of consideration; (3) key assumptions and conditions; (4) exclusivity/no-shop "
        "period (30-90 days, binding); (5) confidentiality obligations (binding); (6) due diligence scope and timeline; "
        "(7) anticipated closing timeline; (8) key employee retention; (9) non-solicitation of employees; (10) governing law "
        "and dispute resolution; (11) expenses (each party bears own); (12) non-binding nature (except specified binding "
        "provisions). The LOI should clearly state which provisions are binding and which are non-binding. Include a break fee "
        "or reverse break fee provision where appropriate."
    ),
    key_elements=["non-binding", "exclusivity", "no-shop", "break fee", "due diligence period"],
    applicable_document_types=["merger_agreement", "asset_purchase_agreement"],
    tags=["LOI", "term sheet", "exclusivity", "non-binding"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-MA-004",
    topic="asset_purchase_agreement",
    domain=DoctrineDomain.MERGER_ACQUISITION,
    title="Asset Purchase Agreement",
    summary="Asset purchase agreements transfer specific assets and liabilities from seller to buyer, allowing selective assumption.",
    content=(
        "Key distinctions from stock/merger: buyer selects which assets to purchase and liabilities to assume. Seller retains "
        "excluded assets and excluded liabilities. Key provisions: (1) purchased assets (detailed schedules); (2) excluded "
        "assets; (3) assumed liabilities; (4) excluded liabilities; (5) purchase price allocation (IRC 1060, residual method); "
        "(6) representations and warranties; (7) bulk sales compliance (if applicable; many states have repealed); (8) consents "
        "required for assignment of contracts; (9) transfer taxes allocation; (10) prorations; (11) employee matters (offer "
        "of employment, not automatic transfer); (12) non-competition covenant from seller; (13) transition services agreement. "
        "Section 338(h)(10) election may convert asset tax treatment to stock purchase mechanics."
    ),
    key_elements=["purchased assets", "assumed liabilities", "IRC 1060 allocation", "bulk sales", "338(h)(10)"],
    applicable_document_types=["asset_purchase_agreement"],
    statutory_references=["IRC 1060", "IRC 338(h)(10)"],
    tags=["asset purchase", "M&A", "allocation", "assumed liabilities"],
))

# ---------- REGULATORY (48-51) ----------

_add(DoctrineBlock(
    doctrine_id="LG04-RG-001",
    topic="privacy_policy_requirements",
    domain=DoctrineDomain.REGULATORY,
    title="Privacy Policy Requirements",
    summary="Privacy policies must disclose data collection, use, sharing practices and comply with applicable privacy laws (GDPR, CCPA, state laws).",
    content=(
        "Key privacy law requirements: GDPR (EU) requires: lawful basis for processing, data subject rights (access, rectification, "
        "erasure, portability, objection), data protection impact assessments, 72-hour breach notification, DPO appointment "
        "in certain cases, records of processing. CCPA/CPRA (California) requires: right to know, right to delete, right to "
        "opt out of sale/sharing, right to limit sensitive personal information use, non-discrimination. Privacy policy must "
        "include: (1) categories of information collected; (2) purposes of collection and use; (3) categories of third parties "
        "with whom information is shared; (4) data subject/consumer rights; (5) contact information; (6) effective date; "
        "(7) changes notification. When drafting, conduct a data mapping exercise first to understand data flows."
    ),
    key_elements=["GDPR", "CCPA", "data subject rights", "breach notification", "lawful basis"],
    applicable_document_types=["privacy_policy"],
    statutory_references=["GDPR Art. 13-14", "CCPA (Cal. Civ. Code 1798.100)"],
    tags=["privacy", "GDPR", "CCPA", "data protection"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-RG-002",
    topic="terms_of_service",
    domain=DoctrineDomain.REGULATORY,
    title="Terms of Service / Terms of Use",
    summary="Terms of service govern the use of websites and applications; enforceability depends on conspicuous notice and manifestation of assent.",
    content=(
        "Two types of online agreements: (1) clickwrap (user must affirmatively click 'I agree' - generally enforceable); "
        "(2) browsewrap (terms accessible via hyperlink, use implies agreement - enforceability depends on conspicuousness). "
        "Key provisions: (1) acceptance mechanism; (2) eligibility (age, jurisdiction); (3) user accounts and security; "
        "(4) acceptable use policy; (5) intellectual property ownership; (6) user-generated content (license grant, takedown); "
        "(7) DMCA compliance; (8) disclaimers of warranties; (9) limitation of liability; (10) indemnification by user; "
        "(11) arbitration clause with class action waiver; (12) governing law and venue; (13) termination; (14) modification "
        "procedure (notice, continued use as acceptance). Ensure compliance with consumer protection laws."
    ),
    key_elements=["clickwrap", "browsewrap", "arbitration", "class action waiver", "DMCA"],
    applicable_document_types=["terms_of_service"],
    tags=["TOS", "terms of use", "clickwrap", "browsewrap"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-RG-003",
    topic="force_majeure_drafting",
    domain=DoctrineDomain.REGULATORY,
    title="Force Majeure Clause Drafting",
    summary="Force majeure clauses excuse performance when extraordinary events beyond parties' control prevent fulfillment.",
    content=(
        "Force majeure clauses typically include: (1) triggering events list (natural disasters, war, terrorism, government "
        "action, pandemic, epidemic, quarantine, embargo, strike, fire, flood, earthquake); (2) catch-all provision ('any other "
        "event beyond the reasonable control of the affected party'); (3) notice requirements (prompt written notice with details "
        "and expected duration); (4) mitigation obligation (affected party must use reasonable efforts to mitigate); (5) duration "
        "limit (extended force majeure triggers termination right); (6) allocation of costs during suspension; (7) termination "
        "right if event continues beyond specified period (typically 90-180 days). Post-COVID drafting should address: whether "
        "pandemics are specifically included, supply chain disruptions, government orders, and distinguish from impracticability "
        "and frustration of purpose doctrines."
    ),
    key_elements=["triggering events", "notice", "mitigation", "duration limit", "pandemic"],
    applicable_document_types=["sales_agreement", "service_agreement", "lease_agreement", "license_agreement"],
    tags=["force majeure", "act of god", "pandemic", "impossibility"],
    template_clauses=[
        "Neither Party shall be liable for any failure or delay in performing its obligations under this Agreement where such "
        "failure or delay results from Force Majeure. 'Force Majeure' means any event beyond the reasonable control of the "
        "affected Party, including but not limited to acts of God, flood, fire, earthquake, epidemic, pandemic, government "
        "orders, war, terrorism, strike, or embargo."
    ],
))

_add(DoctrineBlock(
    doctrine_id="LG04-RG-004",
    topic="aml_kyc_compliance",
    domain=DoctrineDomain.REGULATORY,
    title="AML/KYC Compliance Documentation",
    summary="Anti-money laundering and know-your-customer requirements impose due diligence obligations on financial institutions and covered entities.",
    content=(
        "Bank Secrecy Act (BSA) and USA PATRIOT Act require financial institutions to: (1) establish Customer Identification "
        "Program (CIP) verifying identity using government-issued ID, taxpayer ID, and date of birth; (2) conduct Customer "
        "Due Diligence (CDD) including beneficial ownership identification (25%+ owners and one controlling person); "
        "(3) implement ongoing monitoring for suspicious activity; (4) file Currency Transaction Reports (CTRs) for transactions "
        "over $10,000; (5) file Suspicious Activity Reports (SARs) for transactions suspected of involving illegal activity; "
        "(6) maintain records for five years. Enhanced Due Diligence (EDD) required for high-risk customers (PEPs, high-risk "
        "jurisdictions, correspondent banks). When drafting compliance policies, specify procedures for each requirement, "
        "assign responsibility, and establish training and audit programs."
    ),
    key_elements=["CIP", "CDD", "beneficial ownership", "CTR", "SAR", "PEP"],
    applicable_document_types=["aml_kyc_policy", "compliance_policy"],
    statutory_references=["31 U.S.C. 5311-5332", "31 CFR 1010-1026", "USA PATRIOT Act"],
    tags=["AML", "KYC", "BSA", "compliance", "CTR", "SAR"],
))

# ---------- BOILERPLATE / GENERAL (52-55) ----------

_add(DoctrineBlock(
    doctrine_id="LG04-BP-001",
    topic="indemnification_clause",
    domain=DoctrineDomain.BOILERPLATE,
    title="Indemnification Clause Drafting",
    summary="Indemnification provisions allocate risk of third-party claims and losses between contracting parties.",
    content=(
        "Key components: (1) indemnifying party and indemnified party identification; (2) scope of indemnification (third-party "
        "claims, direct losses, or both); (3) categories of covered losses (damages, costs, expenses, attorney fees, judgments, "
        "settlements); (4) trigger events (breach of representation, breach of covenant, negligence, willful misconduct); "
        "(5) exclusions (consequential damages, punitive damages); (6) caps and baskets (deductible/tipping basket, aggregate "
        "cap, mini-basket for individual claims); (7) survival period (typically 12-24 months, longer for fundamental reps); "
        "(8) claims procedure (notice, defense control, consent to settlement); (9) exclusive remedy provision; (10) insurance "
        "offset. In some jurisdictions, indemnification for one's own negligence requires express and unequivocal language. "
        "Texas anti-indemnity statutes limit indemnification in construction and oilfield contexts."
    ),
    key_elements=["scope", "basket", "cap", "survival", "claims procedure", "exclusive remedy"],
    applicable_document_types=["sales_agreement", "service_agreement", "merger_agreement", "license_agreement"],
    jurisdictional_notes="TX anti-indemnity statute (Tex. Ins. Code Ch. 151) limits oilfield indemnity",
    statutory_references=["Tex. Ins. Code Ch. 151", "Tex. Civ. Prac. & Rem. Code Ch. 130"],
    tags=["indemnification", "hold harmless", "basket", "cap", "survival"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-BP-002",
    topic="limitation_of_liability",
    domain=DoctrineDomain.BOILERPLATE,
    title="Limitation of Liability Clauses",
    summary="Limitation of liability clauses cap exposure, exclude consequential damages, and allocate risk proportionate to deal economics.",
    content=(
        "Common structures: (1) aggregate cap (e.g., not to exceed fees paid in prior 12 months); (2) per-incident cap; "
        "(3) consequential damages exclusion (lost profits, lost data, business interruption); (4) types of damages permitted "
        "(direct damages only); (5) carve-outs from limitations (indemnification obligations, IP infringement, confidentiality "
        "breach, willful misconduct, gross negligence); (6) super-cap for carved-out claims (e.g., 2x or 3x the general cap); "
        "(7) insurance minimum requirements; (8) mutual vs one-sided limitations. Enforceability requires: conspicuous language "
        "(often ALL CAPS or bold), not unconscionable, and consistent with applicable law. Some jurisdictions prohibit limitation "
        "of certain damages (personal injury, fraud). When drafting, align the cap with the contract value and risk profile."
    ),
    key_elements=["aggregate cap", "consequential exclusion", "carve-outs", "super-cap", "conspicuous"],
    applicable_document_types=["service_agreement", "license_agreement", "sales_agreement"],
    tags=["limitation of liability", "cap", "consequential damages", "exclusion"],
    template_clauses=[
        "IN NO EVENT SHALL EITHER PARTY BE LIABLE TO THE OTHER FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR "
        "PUNITIVE DAMAGES, REGARDLESS OF THE CAUSE OF ACTION OR THE THEORY OF LIABILITY, EVEN IF SUCH PARTY HAS BEEN ADVISED "
        "OF THE POSSIBILITY OF SUCH DAMAGES."
    ],
))

_add(DoctrineBlock(
    doctrine_id="LG04-BP-003",
    topic="dispute_resolution_drafting",
    domain=DoctrineDomain.BOILERPLATE,
    title="Dispute Resolution Clauses",
    summary="Dispute resolution clauses specify the mechanism for resolving disagreements: negotiation, mediation, arbitration, or litigation.",
    content=(
        "Tiered dispute resolution: (1) negotiation (senior executives meet within specified period); (2) mediation (neutral "
        "mediator, non-binding, costs shared); (3) arbitration (binding, administered by AAA, JAMS, or ICC under specified "
        "rules, number of arbitrators, venue, language, discovery limits, appeal rights); or (4) litigation (court, jury waiver). "
        "Key considerations: enforceability (Federal Arbitration Act preempts state law disfavoring arbitration), class action "
        "waiver (generally enforceable per AT&T Mobility v. Concepcion), choice of rules (AAA Commercial, JAMS Comprehensive, "
        "ICC), consolidation of related disputes, interim relief carve-out (parties may seek injunctive relief in court), "
        "governing law for the arbitration agreement itself, confidentiality of proceedings. When drafting, specify clear "
        "escalation triggers and timeframes for each tier."
    ),
    key_elements=["arbitration", "mediation", "AAA", "JAMS", "class action waiver", "jury waiver"],
    applicable_document_types=["sales_agreement", "service_agreement", "employment_agreement", "license_agreement"],
    statutory_references=["Federal Arbitration Act (9 U.S.C. 1-16)"],
    tags=["dispute resolution", "arbitration", "mediation", "venue"],
))

_add(DoctrineBlock(
    doctrine_id="LG04-BP-004",
    topic="electronic_signatures",
    domain=DoctrineDomain.BOILERPLATE,
    title="Electronic Signatures and Digital Execution",
    summary="Electronic signatures are legally valid under UETA and E-SIGN for most contracts; certain exceptions exist.",
    content=(
        "The Uniform Electronic Transactions Act (UETA, adopted by 49 states plus DC) and federal E-SIGN Act (15 U.S.C. 7001) "
        "provide that electronic signatures and records have the same legal effect as handwritten signatures and paper records. "
        "Exceptions (not covered by E-SIGN): wills, codicils, testamentary trusts, adoption, divorce, court orders, UCC "
        "Articles 1-9 (except 2 and 2A), and notices of default/foreclosure. For valid e-signature: (1) intent to sign; "
        "(2) consent to do business electronically; (3) association with the record; (4) attribution to the signer. "
        "Counterparts clause should include: 'This Agreement may be executed in counterparts, each of which shall be deemed "
        "an original. Signatures transmitted by electronic means (including PDF, DocuSign, or similar platforms) shall be "
        "deemed original signatures for all purposes.'"
    ),
    key_elements=["UETA", "E-SIGN", "intent to sign", "consent", "counterparts", "attribution"],
    applicable_document_types=["sales_agreement", "service_agreement", "employment_agreement", "lease_agreement"],
    statutory_references=["UETA", "E-SIGN Act (15 U.S.C. 7001-7006)"],
    tags=["electronic signature", "e-sign", "DocuSign", "counterparts"],
))


# ============================================================================
# DOCTRINE ENGINE
# ============================================================================


class LegalDocumentDoctrineEngine:
    """Engine for querying the doctrine cache by topic, domain, or keyword."""

    def __init__(self) -> None:
        self._cache = DOCTRINE_CACHE
        self._topic_index: Dict[str, str] = {}
        self._domain_index: Dict[str, List[str]] = defaultdict(list)
        self._tag_index: Dict[str, List[str]] = defaultdict(list)
        self._build_indexes()
        logger.info("LegalDocumentDoctrineEngine initialized | doctrines={}", len(self._cache))

    def _build_indexes(self) -> None:
        for doctrine_id, block in self._cache.items():
            self._topic_index[block.topic] = doctrine_id
            self._domain_index[block.domain.value].append(doctrine_id)
            for tag in block.tags:
                self._tag_index[tag.lower()].append(doctrine_id)

    def get_by_id(self, doctrine_id: str) -> Optional[DoctrineResponse]:
        block = self._cache.get(doctrine_id)
        if not block:
            return None
        return self._to_response(block)

    def get_by_topic(self, topic: str) -> Optional[DoctrineResponse]:
        doctrine_id = self._topic_index.get(topic)
        if not doctrine_id:
            return None
        return self._to_response(self._cache[doctrine_id])

    def get_by_domain(self, domain: str) -> List[DoctrineResponse]:
        doctrine_ids = self._domain_index.get(domain, [])
        return [self._to_response(self._cache[did]) for did in doctrine_ids if did in self._cache]

    def get_by_tag(self, tag: str) -> List[DoctrineResponse]:
        doctrine_ids = self._tag_index.get(tag.lower(), [])
        return [self._to_response(self._cache[did]) for did in doctrine_ids if did in self._cache]

    def search_doctrines(self, query: str, top_k: int = 5) -> List[DoctrineResponse]:
        query_lower = query.lower()
        scored: List[Tuple[str, float]] = []
        for doctrine_id, block in self._cache.items():
            score = 0.0
            searchable = f"{block.title} {block.summary} {block.topic} {' '.join(block.tags)}".lower()
            for word in query_lower.split():
                if word in searchable:
                    score += 1.0
                if word in block.title.lower():
                    score += 2.0
                if word in block.topic.lower():
                    score += 1.5
            if score > 0:
                scored.append((doctrine_id, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [self._to_response(self._cache[did]) for did, _ in scored[:top_k] if did in self._cache]

    def get_all_topics(self) -> List[str]:
        return sorted(self._topic_index.keys())

    def get_all_domains(self) -> List[str]:
        return sorted(self._domain_index.keys())

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_doctrines": len(self._cache),
            "domains": {d: len(ids) for d, ids in self._domain_index.items()},
            "total_tags": len(self._tag_index),
            "topics": len(self._topic_index),
        }

    def _to_response(self, block: DoctrineBlock) -> DoctrineResponse:
        start = time.time()
        content_hash = hashlib.sha256(block.content.encode("utf-8")).hexdigest()[:16]
        elapsed = (time.time() - start) * 1000.0
        conf_score = {"HIGH": 0.90, "MEDIUM": 0.70, "LOW": 0.50, "UNCERTAIN": 0.30}.get(block.confidence.value, 0.50)
        return DoctrineResponse(
            doctrine_id=block.doctrine_id,
            topic=block.topic,
            domain=block.domain.value,
            title=block.title,
            summary=block.summary,
            content=block.content,
            key_elements=block.key_elements,
            confidence=block.confidence.value,
            confidence_score=conf_score,
            cache_hit=True,
            retrieval_time_ms=round(elapsed, 2),
            determinism_hash=content_hash,
        )


# ============================================================================
# MODULE-LEVEL SINGLETON
# ============================================================================

_engine_instance: Optional[LegalDocumentDoctrineEngine] = None


def get_engine() -> LegalDocumentDoctrineEngine:
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = LegalDocumentDoctrineEngine()
    return _engine_instance
