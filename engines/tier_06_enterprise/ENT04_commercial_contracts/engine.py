"""
ENT04 Commercial Contracts Engine v1.0.0
TIE-Grade Intelligence Engine for Commercial Contract Analysis

Covers: UCC Article 2, service agreements, MSAs, SaaS/licensing, NDAs,
supply chain, distribution, JVs, force majeure, liability limitations,
indemnification, warranties, choice of law/forum.

Port: 9144 | ENGINE_ID: ENT04
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from contextlib import asynccontextmanager
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

ENGINE_ID = "ENT04"
ENGINE_NAME = "Commercial Contracts Engine"
VERSION = "1.0.0"
PORT = 9144

logger.add(f"logs/{ENGINE_ID}_{{time}}.log", rotation="100 MB", retention="30 days", level="INFO")


class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class PositionZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class IssueCategory(str, Enum):
    FORMATION = "FORMATION"
    PERFORMANCE = "PERFORMANCE"
    BREACH = "BREACH"
    REMEDIES = "REMEDIES"
    INTERPRETATION = "INTERPRETATION"
    MODIFICATION = "MODIFICATION"
    TERMINATION = "TERMINATION"
    LIABILITY = "LIABILITY"
    IP_RIGHTS = "IP_RIGHTS"
    DISPUTE_RESOLUTION = "DISPUTE_RESOLUTION"


class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: Optional[str] = None
    adversary_position: Optional[str] = None
    counter_arguments: List[str] = Field(default_factory=list)
    resolution_strategy: str = ""
    entity_scope: str = "all_commercial_contracts"
    confidence: ConfidenceLevel = ConfidenceLevel.DEFENSIBLE
    controlling_precedent: List[str] = Field(default_factory=list)


DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="UCC 2-201 Statute of Frauds",
        keywords=["statute of frauds", "writing requirement", "sale of goods", "$500", "merchant confirmation"],
        conclusion_template="Contracts for sale of goods $500+ require signed writing unless merchant confirmation exception, specially manufactured goods, judicial admission, or partial performance applies.",
        reasoning_framework="""UCC 2-201 mandate: sale of goods $500+ unenforceable without (1) signed writing, (2) merchant confirmation not objected to within 10 days, (3) specially manufactured goods unsuitable for resale, (4) judicial admission, or (5) partial performance (enforceable to extent performed). Email/text can satisfy if signed. Quantity term required. Missing price/delivery terms fillable by UCC gap-fillers. Merchants held to higher standard on confirmations.""",
        key_factors=["goods vs services", "price threshold", "signed writing existence", "merchant status", "confirmation timing", "special manufacture", "partial performance"],
        primary_authority=["UCC 2-201", "UCC 2-104 (merchant)", "UCC 2-105 (goods)", "Restatement (Second) Contracts 110"],
        burden_holder="party seeking enforcement",
        adversary_position="no enforceable contract due to statute of frauds",
        counter_arguments=["merchant confirmation exception", "specially manufactured goods", "partial performance doctrine", "judicial admission in pleadings", "promissory estoppel (minority)"],
        resolution_strategy="Establish signed writing or exception via merchant confirmation memo, manufacturing evidence, payment/acceptance records.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["C.R. Klewin v. Flagship Properties (emails satisfy)", "Cohn v. Fisher (merchant confirmation binds both)", "DF Activities Corp v. Brown (oral contract unenforceable)"]
    ),
    DoctrineBlock(
        topic="UCC 2-207 Battle of Forms",
        keywords=["battle of forms", "additional terms", "different terms", "acceptance", "definite expression"],
        conclusion_template="Between merchants, additional terms in acceptance become part of contract unless material, objected to, or original offer limits acceptance to its terms. Different terms treated per knockout rule or 2-207(3).",
        reasoning_framework="""UCC 2-207(1): definite expression of acceptance operates as acceptance even if states additional/different terms, unless acceptance expressly conditional on assent to new terms. 2-207(2): additional terms between merchants become part of contract UNLESS (a) material alteration, (b) offer expressly limits acceptance, or (c) objection within reasonable time. Different terms: majority apply knockout rule (conflicting terms drop out, UCC gap-fillers apply). Minority: different terms = additional terms analysis. Conduct forming contract under 2-207(3): terms are those agreed upon + UCC gap-fillers.""",
        key_factors=["merchant status", "additional vs different terms", "material alteration", "express limitation in offer", "timely objection", "conduct forming contract"],
        primary_authority=["UCC 2-207(1)", "UCC 2-207(2)", "UCC 2-207(3)", "UCC 2-104"],
        burden_holder="party asserting term inclusion",
        adversary_position="boilerplate term does not bind due to material alteration or knockout rule",
        counter_arguments=["term expressly agreed in negotiation", "immaterial addition", "no timely objection", "parties performed consistent with term"],
        resolution_strategy="Identify merchant status, classify term as additional/different, test materiality (arbitration, warranty disclaimer, limitation of liability usually material), apply knockout or 2-207(3) if conduct contract.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["Northrop Corp v. Litronic Industries (arbitration clause material)", "C. Itoh v. Jordan Int'l (warranty disclaimer material)", "Daitom Inc v. Pennwalt Corp (knockout rule)"]
    ),
    DoctrineBlock(
        topic="UCC 2-302 Unconscionability",
        keywords=["unconscionability", "procedural", "substantive", "adhesion", "gross disparity"],
        conclusion_template="Contract or clause unenforceable if procedurally AND substantively unconscionable at time of formation. Procedural: lack of meaningful choice. Substantive: unreasonably favorable terms.",
        reasoning_framework="""UCC 2-302: court may refuse enforcement or limit unconscionable clause. Requires procedural (oppression: adhesion, hidden terms, lack of choice, unequal bargaining power) AND substantive (overly harsh terms: gross price disparity, unlimited liability, one-sided remedies). Both required. Formation-focused. Sophisticated commercial parties rarely succeed. Consumer contracts more susceptible.""",
        key_factors=["adhesion contract", "hidden/deceptive terms", "disparity in bargaining power", "gross price disparity", "one-sided risk allocation", "party sophistication", "availability of alternatives"],
        primary_authority=["UCC 2-302", "Williams v. Walker-Thomas Furniture", "Restatement (Second) Contracts 208"],
        burden_holder="party challenging term",
        adversary_position="contract is product of arm's length negotiation between sophisticated parties",
        counter_arguments=["both parties sophisticated", "opportunity to negotiate", "market standard terms", "no deception or surprise", "reasonable consideration"],
        resolution_strategy="Establish procedural defects (adhesion, rushed signing, no negotiation) AND substantive abuse (unlimited indemnity, penalty clauses, gross price disparity). Harder in B2B contexts.",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent=["Williams v. Walker-Thomas (poor consumer, cross-collateralization)", "A&M Produce v. FMC Corp (sophisticated parties, no unconscionability)", "Brower v. Gateway 2000 (arbitration upheld despite adhesion)"]
    ),
    DoctrineBlock(
        topic="UCC 2-615 Commercial Impracticability",
        keywords=["commercial impracticability", "excuse", "performance", "unforeseen event", "force majeure"],
        conclusion_template="Performance excused if unforeseen contingency makes performance commercially impracticable, unless party assumed the risk. Must notify other party.",
        reasoning_framework="""UCC 2-615: delay/non-delivery excused if performance impracticable due to unforeseen contingency, unless party assumed risk or is at fault. Three elements: (1) contingency occurred, (2) non-occurrence was basic assumption, (3) occurrence made performance impracticable (not merely more expensive or difficult). Must give timely notice. Partial impracticability: allocate production among customers. Force majeure clauses may supplement or replace 2-615.""",
        key_factors=["unforeseen event", "basic assumption of contract", "degree of difficulty/cost increase", "risk allocation", "notice to other party", "partial vs total impracticability"],
        primary_authority=["UCC 2-615", "UCC 2-614", "Restatement (Second) Contracts 261", "Transatlantic Financing v. US"],
        burden_holder="party seeking excuse",
        adversary_position="mere price increase or difficulty does not excuse; risk was foreseeable or assumed",
        counter_arguments=["event was foreseeable", "force majeure clause excludes event", "party assumed risk", "alternative performance available", "mere cost increase insufficient"],
        resolution_strategy="Prove event unforeseeable, performance truly impracticable (not just unprofitable), risk not allocated by contract, timely notice given. Distinguish from frustration of purpose.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["Transatlantic Financing (Suez Canal, impracticability rejected)", "Maple Farms v. City School Dist (price increase alone insufficient)", "Canadian Industrial v. C. Itoh (embargo excused performance)"]
    ),
    DoctrineBlock(
        topic="SaaS License vs Sale Distinction",
        keywords=["SaaS", "license", "sale", "first sale doctrine", "revocability", "subscription"],
        conclusion_template="SaaS is license not sale; no ownership transfer, revocable per terms, no first sale doctrine. Provider retains IP, grants limited access rights.",
        reasoning_framework="""Software delivered as service (SaaS) is license not sale under Vernor v. Autodesk and MDY v. Blizzard. User obtains access rights, not ownership. No first sale doctrine (17 USC 109) because no material object transferred. License revocable per terms. Perpetual license with single payment may be sale. Subscription/ongoing access fee = license. Material terms: access duration, termination rights, IP ownership, updates/support. EULA clickwrap enforceable if reasonable notice.""",
        key_factors=["ownership vs access", "payment structure", "termination rights", "IP retention", "update/support obligations", "user restrictions", "clickwrap validity"],
        primary_authority=["Vernor v. Autodesk", "MDY Industries v. Blizzard", "ProCD v. Zeidenberg", "17 USC 109", "UCITA (minority)"],
        burden_holder="party asserting ownership rights",
        adversary_position="license grants no ownership, user has no resale/transfer rights, provider can revoke per terms",
        counter_arguments=["perpetual license with no ongoing obligations may be sale", "clickwrap unenforceable if unreasonable", "materially misleading representation of rights"],
        resolution_strategy="Examine payment structure (one-time vs recurring), duration (perpetual vs term), update obligations, termination clauses. License = access rights only.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["Vernor v. Autodesk (license not sale test)", "ProCD v. Zeidenberg (shrinkwrap enforceable)", "Specht v. Netscape (insufficient notice, unenforceable)"]
    ),
    DoctrineBlock(
        topic="Force Majeure Clauses",
        keywords=["force majeure", "act of God", "pandemic", "war", "excuse", "notice"],
        conclusion_template="Force majeure excuses performance only if event listed, unforeseeable, unavoidable, and causal. Requires notice and mitigation efforts. Does not excuse payment obligations unless specified.",
        reasoning_framework="""Common law recognizes no general force majeure doctrine; must be contractually defined. Typical elements: (1) event enumerated or within catchall, (2) beyond reasonable control, (3) unforeseeable, (4) makes performance impossible or impracticable, (5) no fault of invoking party. Strict construction. Specific enumeration (war, strike, pandemic) vs general catchall. Ejusdem generis canon: catchall limited to events similar to enumerated. Must give timely notice. Duty to mitigate. Payment obligations typically not excused unless clause specifies. COVID-19 litigation: specific pandemic inclusion determinative.""",
        key_factors=["event enumeration", "foreseeability", "causation", "impossibility vs impracticability", "notice requirement", "mitigation duty", "payment vs performance"],
        primary_authority=["Restatement (Second) Contracts 261", "Kel Kim v. Central Markets", "Perlman v. Pioneer Ltd Partnership", "Rochester Gas v. Delta Star"],
        burden_holder="party invoking force majeure",
        adversary_position="event foreseeable, not enumerated, alternative performance available, or failure to mitigate",
        counter_arguments=["event not enumerated", "foreseeable at contracting", "catchall does not apply (ejusdem generis)", "performance merely difficult not impossible", "inadequate notice or mitigation"],
        resolution_strategy="Parse clause for enumeration, apply ejusdem generis to catchall, test foreseeability at contract formation, establish causal impossibility, verify notice/mitigation compliance.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["Kel Kim v. Central Markets (foreseeability defeats FM)", "Perlman v. Pioneer (specific enumeration required)", "JN Contemporary Art v. Phillips Auctioneers (pandemic not FM event)"]
    ),
    DoctrineBlock(
        topic="Limitation of Liability Clauses",
        keywords=["limitation of liability", "consequential damages", "cap", "direct damages", "gross negligence"],
        conclusion_template="Liability caps enforceable unless unconscionable or for gross negligence/willful misconduct. Consequential damage exclusions valid if conspicuous. Cannot exclude fraud or intentional torts.",
        reasoning_framework="""Commercial parties may limit liability via (1) damage caps (e.g., fees paid in prior 12 months), (2) exclusion of consequential/indirect/incidental damages, (3) exclusive remedy clauses. Enforceable unless unconscionable (2-302) or violate public policy. Cannot exclude liability for fraud, intentional torts, gross negligence, willful misconduct. Consequential damages (lost profits, business interruption) excludable if conspicuous. Direct damages (cover, replacement cost) harder to exclude. Failure of essential purpose (2-719): if exclusive remedy fails, UCC remedies available. Consumer contracts more scrutinized.""",
        key_factors=["cap amount reasonableness", "conspicuousness", "type of damages excluded", "gross negligence/willful misconduct", "failure of essential purpose", "party sophistication", "negotiation opportunity"],
        primary_authority=["UCC 2-719", "UCC 2-302", "Restatement (Second) Contracts 195", "Tunkl v. Regents (public policy)"],
        burden_holder="party challenging limitation",
        adversary_position="sophisticated parties can allocate risk; limitation is conspicuous and reasonable",
        counter_arguments=["unconscionable given disparity", "gross negligence occurred", "exclusive remedy failed essential purpose", "fraud or intentional tort", "public policy violation"],
        resolution_strategy="Enforce unless unconscionable, gross negligence, fraud, or failure of essential purpose. Ensure conspicuous presentation. B2B contexts favored.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["Hadley v. Baxendale (consequential damages foreseeability)", "Chatlos v. National Cash Register (failure of essential purpose)", "AES v. Dow Chemical (cap enforceable in B2B)"]
    ),
    DoctrineBlock(
        topic="Indemnification Clauses",
        keywords=["indemnification", "hold harmless", "third-party claims", "defense costs", "sole negligence"],
        conclusion_template="Indemnity for third-party claims enforceable if clear and unambiguous. Sole negligence indemnity disfavored or prohibited in many states. Must cover defense costs if specified.",
        reasoning_framework="""Indemnification shifts loss from indemnitee to indemnitor. Types: (1) broad form (all claims, even indemnitee sole negligence), (2) intermediate (claims arising from indemnitor acts), (3) limited (indemnitor sole negligence only). Many states prohibit or narrowly construe sole negligence indemnity (violates public policy). Construction contracts heavily regulated. Clear and unambiguous language required. Defense duty separate from indemnity; must be explicit. Trigger: third-party claim 'arising out of' indemnitor acts. Exclusions for gross negligence/willful misconduct common.""",
        key_factors=["breadth of indemnity", "sole negligence prohibition", "defense cost inclusion", "arising out of scope", "state law restrictions", "conspicuousness", "party sophistication"],
        primary_authority=["Restatement (Second) Torts 886B", "state anti-indemnity statutes", "Hoisting & Portable Engineers v. Magee (sole negligence)", "SNC-Lavalin v. CB&I"],
        burden_holder="indemnitee seeking indemnification",
        adversary_position="indemnity void as against public policy, claim outside scope, or no duty to defend",
        counter_arguments=["sole negligence indemnity void in jurisdiction", "claim not 'arising out of' indemnitor acts", "ambiguous language construed against drafter", "no defense duty absent express provision"],
        resolution_strategy="Verify state law permits scope of indemnity, construe 'arising out of' broadly for indemnitee, confirm defense duty explicit, exclude gross negligence.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["Hoisting Engineers v. Magee (sole negligence void)", "Crawford v. Weather Shield (defense costs separate)", "Valhal Corp v. Sullivan (anti-indemnity statute)"]
    ),
    DoctrineBlock(
        topic="Warranty Disclaimers",
        keywords=["warranty disclaimer", "as is", "merchantability", "fitness", "conspicuousness"],
        conclusion_template="Implied warranty of merchantability disclaimed by conspicuous 'as is' or specific disclaimer mentioning merchantability. Fitness requires writing. Cannot disclaim fraud or known defects.",
        reasoning_framework="""UCC 2-314 implied warranty of merchantability (goods fit for ordinary purpose) arises in merchant sales. UCC 2-315 implied warranty of fitness for particular purpose if seller knows buyer's purpose and buyer relies. Disclaimers: (1) 'as is', 'with all faults' disclaims all implied warranties if conspicuous, (2) merchantability disclaimer must mention 'merchantability' and be conspicuous, (3) fitness disclaimer must be in writing. Conspicuous = reasonable person would notice (caps, bold, contrasting type). Cannot disclaim express warranties made during negotiation. Cannot disclaim fraud or intentionally concealed defects. Magnuson-Moss Act limits consumer disclaimers.""",
        key_factors=["conspicuousness", "specific mention of merchantability", "writing requirement for fitness", "as is language", "express warranty conflict", "fraud/concealment", "consumer vs commercial"],
        primary_authority=["UCC 2-314", "UCC 2-315", "UCC 2-316", "UCC 1-201(10) (conspicuous)", "Magnuson-Moss Act 15 USC 2308"],
        burden_holder="seller asserting disclaimer",
        adversary_position="disclaimer ineffective due to lack of conspicuousness or conflict with express warranty",
        counter_arguments=["disclaimer not conspicuous", "merchantability not mentioned", "oral express warranty overrides", "fraud or concealment", "Magnuson-Moss prohibits (consumer goods)"],
        resolution_strategy="Use all-caps AS IS or specific merchantability disclaimer in bold. Avoid express warranties conflicting with disclaimer. Cannot defeat fraud claims.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["Gindy Mfg v. Cardinale Trucking (conspicuous disclaimer upheld)", "Williams v. Fulmer (disclaimer ineffective, not conspicuous)", "Keith v. Buchanan (oral express warranty overrides written disclaimer)"]
    ),
    DoctrineBlock(
        topic="Choice of Law and Forum Selection",
        keywords=["choice of law", "forum selection", "governing law", "venue", "reasonableness"],
        conclusion_template="Choice of law and forum selection clauses enforced if reasonable and not contrary to public policy. Mandatory vs permissive forum selection. Consumer contracts more scrutinized.",
        reasoning_framework="""Parties may select governing law and forum. Choice of law: enforced unless (1) no reasonable basis, (2) contrary to fundamental policy of state with materially greater interest (Restatement Second Conflict of Laws 187). UCC permits choice of law if transaction bears reasonable relation. Forum selection: enforced per Carnival Cruise v. Shute and Bremen v. Zapata unless (1) unreasonable/unjust, (2) result of fraud/overreaching, (3) contravenes strong public policy. Mandatory ('exclusive jurisdiction') vs permissive ('submit to jurisdiction'). Consumer adhesion contracts face stricter scrutiny. Arbitration clauses separate analysis under FAA.""",
        key_factors=["reasonable relation to transaction", "public policy conflict", "mandatory vs permissive forum", "consumer vs commercial", "notice and conspicuousness", "fraud or overreaching"],
        primary_authority=["Restatement (Second) Conflict of Laws 187", "UCC 1-301", "Bremen v. Zapata Off-Shore", "Carnival Cruise v. Shute", "Atlantic Marine v. US Dist Court"],
        burden_holder="party challenging clause",
        adversary_position="clause unreasonable, unconscionable, or violates public policy of forum with greater interest",
        counter_arguments=["no reasonable relation to transaction", "fundamental public policy violated", "consumer adhesion contract", "inconvenient forum for weaker party"],
        resolution_strategy="Establish reasonable connection to chosen law/forum, avoid public policy conflicts, ensure conspicuous in consumer contracts. Favor enforceability in B2B.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["Bremen v. Zapata (enforce absent unreasonableness)", "Carnival Cruise v. Shute (consumer forum selection upheld)", "America Online v. Booker (choice of law upheld)"]
    ),
    DoctrineBlock(
        topic="Non-Disclosure Agreements (NDAs)",
        keywords=["NDA", "confidential information", "non-disclosure", "trade secrets", "exclusions"],
        conclusion_template="NDAs protect confidential information via non-disclosure and restricted use covenants. Standard exclusions: public domain, prior knowledge, independent development, required disclosure. Trade secret overlay.",
        reasoning_framework="""NDAs impose duty not to disclose or use confidential information except for permitted purpose. Mutual or unilateral. Key terms: (1) definition of confidential information (broad vs specific), (2) exclusions (public domain, rightfully known, independently developed, legally compelled), (3) term (perpetual or limited), (4) permitted use, (5) return/destruction on termination. Trade secret law (UTSA/DTSA) may overlay if information qualifies. Reasonable measures to protect secrecy required. Overly broad NDA may be unenforceable restraint. Injunctive relief typical remedy.""",
        key_factors=["scope of confidential information", "exclusions breadth", "term duration", "permitted use definition", "return/destruction obligation", "remedies provision", "trade secret qualification"],
        primary_authority=["UTSA", "18 USC 1836 (DTSA)", "Restatement (First) Torts 757", "PepsiCo v. Redmond"],
        burden_holder="disclosing party seeking enforcement",
        adversary_position="information falls within exception, overly broad restraint, or no trade secret protection",
        counter_arguments=["information public domain", "prior rightful knowledge", "independent development", "legally compelled disclosure", "unreasonable restraint on trade"],
        resolution_strategy="Draft clear definition and exclusions, limit term to reasonable period, specify permitted use, ensure trade secret measures overlap (marking, access control).",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["PepsiCo v. Redmond (inevitable disclosure)", "Religious Tech Center v. Netcom (trade secret elements)", "Warner-Lambert v. Execuquest (overly broad NDA)"]
    ),
    DoctrineBlock(
        topic="Material Breach vs Minor Breach",
        keywords=["material breach", "minor breach", "substantial performance", "suspension", "termination"],
        conclusion_template="Material breach excuses non-breaching party performance and permits termination. Minor breach allows damages but not suspension. Factors: extent of deprivation, adequacy of cure, forfeiture.",
        reasoning_framework="""Restatement Second 241 factors for materiality: (1) extent non-breaching party deprived of reasonably expected benefit, (2) adequacy of compensation, (3) forfeited performance, (4) likelihood of cure, (5) good faith and fair dealing. Material breach: non-breaching party may suspend performance and terminate. Minor breach: damages only, must continue performance. UCC perfect tender rule (2-601) vs common law substantial performance. Time-is-of-essence clauses make late performance material. Anticipatory repudiation separate doctrine.""",
        key_factors=["benefit deprivation", "cure availability", "forfeiture to breaching party", "willful vs inadvertent", "time sensitivity", "contract language on materiality"],
        primary_authority=["Restatement (Second) Contracts 241", "UCC 2-601 (perfect tender)", "UCC 2-508 (cure)", "Jacob & Youngs v. Kent"],
        burden_holder="party asserting material breach",
        adversary_position="breach minor, curable, or does not deprive of substantial benefit",
        counter_arguments=["substantial performance achieved", "breach curable", "minimal economic harm", "no forfeiture justified", "good faith efforts"],
        resolution_strategy="Apply 241 factors, assess benefit deprivation, consider cure opportunity, check for time-is-essence clause. UCC goods: perfect tender unless installment contract.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["Jacob & Youngs v. Kent (substantial performance, pipe brand)", "Walker v. KFC (material breach, franchise)", "Sackett v. Spindler (minor breach, damages only)"]
    ),
    DoctrineBlock(
        topic="Anti-Assignment Clauses",
        keywords=["assignment", "anti-assignment", "delegation", "novation", "consent"],
        conclusion_template="Anti-assignment clauses generally enforceable but construed narrowly. Assignment despite prohibition may be ineffective against obligor but does not invalidate assignment itself. Rights vs duties distinction.",
        reasoning_framework="""Common law allows assignment of contract rights and delegation of duties unless (1) materially changes obligor's duty/risk, (2) materially impairs return performance, (3) prohibited by law, or (4) contract prohibits. Anti-assignment clause: effective to make assignment breach, but does not void assignment (UCC 2-210(2), Restatement Second 322). Assignee gets rights but assignor remains liable. Consent-to-assign clauses: consent cannot be unreasonably withheld unless contract specifies otherwise. Rights (payment) more freely assignable than duties (performance). Delegation does not relieve delegator. Change of control clauses in M&A context.""",
        key_factors=["rights vs duties", "material change to obligor", "contract language specificity", "unreasonable withholding of consent", "UCC vs common law", "waiver by conduct"],
        primary_authority=["UCC 2-210", "Restatement (Second) Contracts 317-322", "Macke Co v. Pizza of Gaithersburg", "PPG Industries v. Shell Oil"],
        burden_holder="party asserting invalid assignment",
        adversary_position="assignment permitted, or clause only creates breach remedy not invalidity",
        counter_arguments=["anti-assignment clause only gives breach claim, not invalidity", "consent unreasonably withheld", "waiver by accepting performance from assignee", "rights freely assignable"],
        resolution_strategy="Distinguish rights (payment, freely assignable) from duties (performance, restricted). Clause creates breach claim but assignee may still enforce. Consent clauses: reasonableness standard.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["Macke Co v. Pizza (assignment of service contract upheld)", "PPG v. Shell (anti-assignment ineffective against assignee)", "Trubowitch v. Riverbank (change of control)"]
    ),
    DoctrineBlock(
        topic="Most Favored Nation (MFN) Clauses",
        keywords=["most favored nation", "MFN", "pricing parity", "antitrust", "best price"],
        conclusion_template="MFN clauses require seller to give buyer pricing/terms equal to or better than any other customer. Enforceable but may raise antitrust concerns if market power present.",
        reasoning_framework="""MFN clause guarantees buyer will receive terms no less favorable than seller gives to others. Protects buyer from price discrimination. Types: (1) retroactive (applies to past sales), (2) prospective (future sales only), (3) narrow (same product/volume), (4) broad (across product lines). Antitrust risk: if seller has market power, MFN may facilitate collusion or raise rivals' costs (DOJ/FTC scrutiny). Healthcare/pharma MFNs under heavy review. Monitoring and enforcement challenges. Competitive bid exemptions common.""",
        key_factors=["retroactive vs prospective", "scope of comparison", "volume/quantity matching", "antitrust market power", "monitoring mechanisms", "exemptions for competitive bids"],
        primary_authority=["FTC/DOJ antitrust guidelines", "Blue Cross cases (MFN scrutiny)", "In re Delta Dental Antitrust Litigation"],
        burden_holder="buyer enforcing MFN",
        adversary_position="different circumstances justify different pricing, or MFN violates antitrust laws",
        counter_arguments=["no comparable transaction", "volume discount differential", "competitive bid exemption", "antitrust harm if enforced", "apples-to-oranges comparison"],
        resolution_strategy="Define narrow scope to comparable transactions, exclude competitive bids, limit duration, monitor for antitrust risk if seller has market power.",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent=["Blue Cross Blue Shield antitrust cases", "In re Delta Dental (MFN facilitates collusion)", "US v. Apple (MFN in ebook pricing)"]
    ),
    DoctrineBlock(
        topic="CISG Application to International Sales",
        keywords=["CISG", "international sale of goods", "opt-out", "place of business", "writing requirement"],
        conclusion_template="CISG applies to sales of goods between parties in different Contracting States unless opted out. No statute of frauds. Different rules than UCC.",
        reasoning_framework="""UN Convention on Contracts for International Sale of Goods (CISG) applies if (1) sale of goods, (2) parties have places of business in different Contracting States, or (3) conflict of laws points to Contracting State, unless parties opt out. 94+ countries. No statute of frauds (Article 11). Formation: offer + acceptance, mirror image not required. Fundamental breach standard (Article 25) for avoidance. Nachfrist notice (additional time for performance). Battle of forms: last shot rule (not UCC 2-207). Party autonomy to opt out or modify. US courts apply if not opted out.""",
        key_factors=["Contracting State status", "opt-out clause", "place of business location", "goods vs services", "fundamental breach vs minor breach", "Nachfrist procedure"],
        primary_authority=["CISG Articles 1-6, 11, 19, 25, 47, 49", "US ratification 1988", "UNCITRAL commentary"],
        burden_holder="party asserting CISG applicability",
        adversary_position="parties opted out, non-Contracting State, or services not goods",
        counter_arguments=["express UCC choice of law (may or may not displace CISG)", "non-Contracting State location", "predominantly services", "custom or usage overrides CISG default"],
        resolution_strategy="Verify Contracting State status, check for opt-out language (e.g., 'UCC governs, CISG excluded'), apply CISG formation/breach rules if applicable. Opt-out recommended for predictability.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["BP Oil v. Empresa Estatal Petroleos (CISG applies absent opt-out)", "Asante Technologies v. PMC-Sierra (choice of CA law opts out CISG)", "Travelers Property v. Saint-Gobain (CISG fundamental breach)"]
    ),
    DoctrineBlock(
        topic="Master Service Agreement (MSA) Structure",
        keywords=["MSA", "master service agreement", "statement of work", "SOW", "evergreen"],
        conclusion_template="MSA sets general terms; SOWs define specific projects. MSA governs in conflict unless SOW explicitly varies. Evergreen renewal common.",
        reasoning_framework="""MSA establishes overarching commercial relationship: pricing framework, IP ownership, liability caps, indemnity, confidentiality, dispute resolution. Statements of Work (SOWs) or Work Orders specify project scope, deliverables, milestones, acceptance criteria. Conflict: MSA governs unless SOW explicitly modifies with MSA consent. Evergreen renewal: auto-renews unless party gives notice (30/60/90 days). Termination: for convenience (MSA-level), for cause (breach), or project completion (SOW-level). Escrow provisions for source code in SaaS/software MSAs.""",
        key_factors=["MSA vs SOW hierarchy", "conflict resolution clause", "renewal mechanics", "termination rights", "IP ownership framework", "change order process"],
        primary_authority=["general contract law", "UCC 1-303 (course of dealing)", "Restatement (Second) Contracts 202"],
        burden_holder="party asserting SOW modifies MSA",
        adversary_position="MSA terms control, SOW does not explicitly override",
        counter_arguments=["SOW silent on term, MSA applies", "SOW modification requires MSA-specified process", "course of dealing establishes interpretation"],
        resolution_strategy="Clear hierarchy clause in MSA (MSA controls unless SOW explicitly states otherwise). Signature authority for SOWs. Escrow for critical software.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["course of dealing and performance doctrines", "parol evidence rule for integrated agreements"]
    ),
    DoctrineBlock(
        topic="Liquidated Damages vs Penalties",
        keywords=["liquidated damages", "penalty", "reasonable estimate", "actual damages", "enforceability"],
        conclusion_template="Liquidated damages enforceable if reasonable estimate of anticipated harm at contract formation and actual damages difficult to ascertain. Penalty provisions void.",
        reasoning_framework="""Liquidated damages clause pre-estimates damages for breach. Enforceable if (1) damages difficult to estimate at formation, (2) amount reasonable in light of anticipated or actual harm (Restatement Second 356). Penalty (punishing breach) void. Modern trend: reasonableness judged at formation or at breach (whichever more favorable). Gross disproportion to actual harm may indicate penalty. Per diem clauses in construction contracts scrutinized. UCC 2-718(1) similar standard.""",
        key_factors=["difficulty of damage estimation", "reasonableness at formation", "relationship to actual harm", "compensatory vs punitive intent", "sophistication of parties"],
        primary_authority=["Restatement (Second) Contracts 356", "UCC 2-718(1)", "Lake River v. Carborundum"],
        burden_holder="party challenging liquidated damages",
        adversary_position="clause is punitive, grossly disproportionate, or actual damages easily calculable",
        counter_arguments=["damages difficult to estimate at formation", "amount reasonable forecast", "actual harm confirms reasonableness", "sophisticated parties negotiated arm's length"],
        resolution_strategy="Justify difficulty of estimation, document reasonable forecasting, avoid gross disproportion. Label as 'liquidated damages' not 'penalty.' B2B contexts favored.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["Lake River v. Carborundum (penalty, take-or-pay)", "Kemble v. Farren (early penalty case)", "United Luggage v. July (LDs upheld, reasonable estimate)"]
    ),
    DoctrineBlock(
        topic="Duty of Good Faith and Fair Dealing",
        keywords=["good faith", "fair dealing", "discretion", "satisfaction clause", "best efforts"],
        conclusion_template="Implied covenant of good faith and fair dealing prevents parties from acting in bad faith to deprive counterparty of contract benefits. Does not create independent duties.",
        reasoning_framework="""Every contract implies duty of good faith and fair dealing (UCC 1-304, Restatement Second 205). Prevents exercise of discretion in bad faith to deprive other party of reasonably expected benefits. Does NOT create new substantive rights or override express terms. Examples: (1) satisfaction clauses (honest dissatisfaction, not pretextual rejection), (2) discretionary pricing (reasonable bounds), (3) requirements/output contracts (good faith variation). Termination for convenience not bad faith per se. Varies by jurisdiction (CA broader, NY narrower).""",
        key_factors=["exercise of discretion", "deprivation of contract benefit", "pretextual justification", "honest vs dishonest conduct", "express terms override", "jurisdictional variations"],
        primary_authority=["UCC 1-304", "Restatement (Second) Contracts 205", "Kirke La Shelle Co v. Paul Armstrong Co (satisfaction)", "Tymshare v. Covell"],
        burden_holder="party alleging bad faith",
        adversary_position="conduct within express contractual discretion, no bad faith motive",
        counter_arguments=["express terms permit conduct", "legitimate business reason", "no deprivation of essential benefit", "termination for convenience allowed"],
        resolution_strategy="Show pretextual exercise of discretion to deprive benefit. Cannot override express terms. Satisfaction clauses: honest dissatisfaction suffices. NY limits implied covenant narrowly.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["Tymshare v. Covell (bad faith discretionary pricing)", "Locke v. WB (satisfaction clause honest)", "Dalton v. Educational Testing (good faith termination)"]
    ),
    DoctrineBlock(
        topic="Integration and Merger Clauses",
        keywords=["integration clause", "merger clause", "entire agreement", "parol evidence", "side agreements"],
        conclusion_template="Integration clause establishes contract as complete and final agreement, barring parol evidence of prior/contemporaneous agreements. Does not bar subsequent modifications or fraud.",
        reasoning_framework="""Integration/merger clause states contract is entire agreement and supersedes prior negotiations/understandings. Effect: triggers parol evidence rule (no extrinsic evidence to contradict/vary integrated writing). Complete integration: bars evidence of additional terms. Partial integration: allows consistent additional terms. Does NOT bar: (1) subsequent modifications, (2) fraud/duress/mistake, (3) ambiguity interpretation, (4) condition precedent to formation, (5) separate consideration side deal. Sophisticated parties, clear drafting: strong presumption of integration.""",
        key_factors=["integration clause presence", "complete vs partial integration", "subsequent vs prior agreements", "fraud/mistake exception", "ambiguity", "separate consideration"],
        primary_authority=["Restatement (Second) Contracts 209-216", "UCC 2-202", "Mitchill v. Lath", "Wagner v. Graziano Construction"],
        burden_holder="party seeking to introduce parol evidence",
        adversary_position="integration clause bars extrinsic evidence",
        counter_arguments=["subsequent oral modification", "fraud in inducement", "ambiguous term requires interpretation", "condition precedent to contract formation", "separate bargained-for side agreement"],
        resolution_strategy="Strong integration clause defeats parol evidence of prior terms. Exceptions: fraud, subsequent mods, ambiguity, condition precedent. Require written mods to defeat oral later changes.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["Mitchill v. Lath (integration excludes oral terms)", "Wagner v. Graziano (parol evidence to show fraud)", "Hatley v. Stafford (subsequent oral mod enforceable)"]
    ),
    DoctrineBlock(
        topic="Best Efforts vs Reasonable Efforts Obligations",
        keywords=["best efforts", "reasonable efforts", "commercially reasonable", "diligence", "exclusivity"],
        conclusion_template="Best efforts requires exhaustive measures; reasonable efforts requires measures ordinarily used. Commercially reasonable efforts industry-specific. Enforcement difficult absent objective criteria.",
        reasoning_framework="""Effort obligations impose duty to act diligently to achieve result. Best efforts: all reasonable efforts plus additional measures, subordinate other interests. Reasonable efforts: actions prudent person would take in similar circumstances. Commercially reasonable efforts: industry custom, cost-benefit analysis. UCC 2-306(2): requirements/output contracts must act in good faith. Exclusive dealing: Wood v. Lucy requires reasonable efforts. Objective metrics (spending minimums, personnel allocation) aid enforceability. Vague standards lead to litigation.""",
        key_factors=["best vs reasonable vs commercially reasonable", "objective metrics", "industry standards", "cost-benefit analysis", "exclusivity obligations", "good faith overlay"],
        primary_authority=["Wood v. Lucy, Lady Duff-Gordon", "UCC 2-306(2)", "Bloor v. Falstaff Brewing", "Restatement (Second) Contracts 205"],
        burden_holder="party alleging inadequate efforts",
        adversary_position="efforts met standard, business judgment respected",
        counter_arguments=["best efforts not unlimited spending", "commercially reasonable = industry standard", "vague obligation unenforceable", "business judgment deference"],
        resolution_strategy="Define objective criteria (minimum spend, headcount, marketing activities). Best efforts strongest. Reasonable/commercially reasonable context-dependent. Good faith minimum.",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent=["Wood v. Lucy (exclusive dealing implies reasonable efforts)", "Bloor v. Falstaff (best efforts, brewery promotion)", "Goldberg v. Marathon (commercially reasonable, no best efforts)"]
    ),
    DoctrineBlock(
        topic="Modification and No Oral Modification Clauses",
        keywords=["modification", "no oral modification", "NOM clause", "consideration", "waiver"],
        conclusion_template="Common law modifications require consideration. UCC no consideration needed if good faith. No oral modification (NOM) clauses enforceable but may be waived by conduct.",
        reasoning_framework="""Common law: contract modification requires new consideration (pre-existing duty rule). UCC 2-209(1): modification needs no consideration if good faith. UCC 2-209(2): NOM clause (modifications must be in writing) enforceable. However, waiver by conduct possible: party accepting performance under oral mod may be estopped from asserting NOM. Duress/bad faith modification unenforceable. Statute of frauds reapplies if modified contract within statute.""",
        key_factors=["consideration for common law mods", "UCC good faith standard", "NOM clause presence", "waiver by conduct", "duress or bad faith", "statute of frauds threshold"],
        primary_authority=["UCC 2-209", "Restatement (Second) Contracts 89", "Alaska Packers v. Domenico (pre-existing duty)", "Wisconsin Knife v. National Metal (waiver of NOM)"],
        burden_holder="party seeking to enforce oral modification",
        adversary_position="NOM clause bars oral modification, no new consideration",
        counter_arguments=["UCC no consideration required", "waiver by accepting performance", "duress voided original contract", "statute of frauds not re-triggered"],
        resolution_strategy="UCC: good faith modification valid, but NOM enforceable unless waived. Common law: require new consideration or detrimental reliance. Avoid duress claims.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["Wisconsin Knife v. National Metal (NOM waived by conduct)", "Roth Steel v. United Steel (oral mod enforceable, good faith)", "Alaska Packers (no consideration, modification void)"]
    ),
    DoctrineBlock(
        topic="Arbitration Clauses in Commercial Contracts",
        keywords=["arbitration", "FAA", "arbitrability", "delegation clause", "class action waiver"],
        conclusion_template="Arbitration clauses enforceable under FAA unless challenge to arbitration agreement itself (not contract generally). Delegation clauses send gateway issues to arbitrator. Class waivers enforceable.",
        reasoning_framework="""Federal Arbitration Act (9 USC 1+) mandates enforcement of arbitration agreements. Severability: challenge must be to arbitration clause itself, not contract generally. Unconscionability high bar (Concepcion). Delegation clause: arbitrator decides arbitrability, scope, enforceability (Rent-A-Center). Class action waivers enforceable in B2B and consumer contexts (Concepcion, Epic Systems). Gateway issues: formation, validity, scope. Who decides: court unless clear and unmistakable delegation to arbitrator. Carve-outs (IP, injunctive relief) permissible.""",
        key_factors=["FAA preemption", "challenge to arbitration clause vs contract", "delegation clause presence", "class waiver", "unconscionability under state law", "gateway question allocation"],
        primary_authority=["9 USC 1-16 (FAA)", "AT&T Mobility v. Concepcion", "Rent-A-Center v. Jackson", "Epic Systems v. Lewis", "First Options v. Kaplan"],
        burden_holder="party resisting arbitration",
        adversary_position="FAA mandates arbitration, clause enforceable, class waiver valid",
        counter_arguments=["arbitration clause unconscionable", "no agreement to arbitrate this dispute", "gateway issue for court not arbitrator", "FAA exemption (transportation workers)"],
        resolution_strategy="Clear delegation clause to arbitrator. Class waiver explicit. FAA preempts most state law challenges. Unconscionability very difficult post-Concepcion.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["Concepcion (class waiver enforceable, preempts state unconscionability)", "Rent-A-Center (delegation to arbitrator)", "Epic Systems (class waiver in employment)"]
    ),
    DoctrineBlock(
        topic="Intellectual Property Ownership in Services Contracts",
        keywords=["IP ownership", "work made for hire", "copyright", "assignment", "pre-existing IP"],
        conclusion_template="Absent assignment, contractor owns IP in deliverables unless work made for hire (employee or 9 statutory categories). Pre-existing IP typically retained by contractor via license.",
        reasoning_framework="""Copyright ownership: (1) work made for hire (employee, or independent contractor if one of 9 categories AND written agreement), (2) assignment to client, or (3) contractor retains. Work made for hire categories: contribution to collective work, part of motion picture/audiovisual, translation, supplementary work, compilation, instructional text, test, answer material, atlas (17 USC 101). Software generally NOT work made for hire for independent contractors. Assignment must be in writing. Pre-existing IP/background IP: contractor retains, grants license to client. Invention assignment clauses in employment contracts.""",
        key_factors=["employee vs independent contractor", "work made for hire category", "written assignment", "pre-existing IP exclusion", "license vs ownership", "patent vs copyright"],
        primary_authority=["17 USC 101 (work made for hire)", "17 USC 201", "CCNV v. Reid (work for hire test)", "35 USC 261 (patent assignment)"],
        burden_holder="client asserting ownership",
        adversary_position="contractor owns absent written assignment or work made for hire",
        counter_arguments=["independent contractor, not employee", "not within 9 statutory categories", "no written assignment", "pre-existing IP carved out"],
        resolution_strategy="Explicit IP assignment clause for all deliverables. Define pre-existing IP retained by contractor. License grant for client use. Work made for hire rare for contractors.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["CCNV v. Reid (sculptor retained copyright, not employee)", "Playboy v. Dumas (artist retained, work not for hire)", "Avtec v. Peiffer (software not work for hire)"]
    ),
    DoctrineBlock(
        topic="Termination for Convenience Clauses",
        keywords=["termination for convenience", "discretion", "good faith", "restitution", "government contracts"],
        conclusion_template="Termination for convenience clauses allow unilateral termination without cause. Must exercise in good faith. Compensation for work performed, not lost profits.",
        reasoning_framework="""Termination for convenience permits party to end contract without breach. Common in government contracts, construction, long-term supply agreements. Limits: (1) good faith required, (2) cannot terminate to avoid unfavorable bargain (bad faith), (3) compensation for work performed + reasonable costs, but no lost profits on unperformed work. Notice period typically specified. Termination for cause separate (requires breach). Restitution measured by benefit conferred or reasonable value.""",
        key_factors=["good faith exercise", "pretextual termination", "compensation scope", "notice requirement", "government vs commercial", "reliance damages"],
        primary_authority=["Restatement (Second) Contracts 205 (good faith)", "Torncello v. US (gov't contracts)", "Reed v. City of Oakland"],
        burden_holder="party alleging bad faith termination",
        adversary_position="termination within discretion, good faith business decision",
        counter_arguments=["termination to avoid unfavorable contract (bad faith)", "pretextual reason", "deprivation of essential contract benefit", "inadequate compensation"],
        resolution_strategy="Clear compensation formula in clause. Notice period. Good faith business reason. Government contracts: FAA Termination for Convenience clause standard. Commercial: negotiated.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["Torncello v. US (gov't termination for convenience upheld)", "Moe v. John Deere (bad faith termination of dealership)", "Dalton v. Educational Testing (good faith termination)"]
    ),
    DoctrineBlock(
        topic="Joint Venture Agreements",
        keywords=["joint venture", "partnership", "fiduciary duty", "profit sharing", "control"],
        conclusion_template="Joint venture creates partnership-like relationship for specific project. Fiduciary duties arise. Control, profit sharing, losses shared per agreement or default partnership rules.",
        reasoning_framework="""Joint venture: agreement to jointly undertake specific commercial project, share profits/losses/control. Treated as partnership (fiduciary duties, joint and several liability) unless contractual modification. Key terms: (1) purpose and scope, (2) capital contributions, (3) profit/loss allocation, (4) management/control, (5) termination events, (6) dispute resolution. Fiduciary duty of loyalty and care. No apparent authority unless JV agreement grants. Duration: project completion or term. Exit rights negotiated.""",
        key_factors=["fiduciary duties", "control allocation", "profit/loss sharing", "capital contribution", "liability exposure", "termination rights", "dispute resolution"],
        primary_authority=["Uniform Partnership Act", "Meinhard v. Salmon (fiduciary duty)", "Restatement (Second) Agency"],
        burden_holder="party alleging JV formation or breach of duty",
        adversary_position="no JV formed, mere contract, or no fiduciary breach",
        counter_arguments=["no agreement to share profits", "no joint control", "contract disclaims fiduciary duties", "business judgment rule protects decision"],
        resolution_strategy="Define scope narrowly, limit fiduciary duties contractually, allocate control explicitly, establish exit mechanics, limit joint liability where possible.",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent=["Meinhard v. Salmon (JV fiduciary duty, opportunity usurpation)", "Beckman v. Farmer (no JV without profit sharing intent)", "Connolly v. Agostini (JV breach)"]
    ),
    DoctrineBlock(
        topic="Supply Chain and Distribution Agreements",
        keywords=["distribution", "requirements contract", "exclusive territory", "termination", "good faith"],
        conclusion_template="Distribution agreements grant distributor rights to resell. Requirements/output contracts require good faith quantity variation. Exclusive territory enforceable. Termination notice and good faith required.",
        reasoning_framework="""Distribution agreement: supplier grants distributor right to resell products, usually in territory. Types: exclusive (sole distributor), non-exclusive (multiple distributors), requirements contract (buyer agrees to purchase all needs from seller). UCC 2-306: requirements/output must be in good faith (no unreasonably disproportionate increase/decrease). Exclusive territory: enforceable, antitrust scrutiny if vertical restraint (Rule of Reason). Termination: for cause (breach), for convenience (notice period, good faith), or automatic (term expiration). At-will distributor statutes in some states restrict termination.""",
        key_factors=["exclusive vs non-exclusive", "territory definition", "minimum purchase obligations", "good faith quantity variation", "termination rights", "state distributor protection laws"],
        primary_authority=["UCC 2-306", "Sherman Act 1 (vertical restraints)", "state distributor statutes (WI, NJ, etc.)", "Wayman v. Amoco Oil"],
        burden_holder="party alleging breach or improper termination",
        adversary_position="good faith business decision, contractual termination right, no statutory protection",
        counter_arguments=["unreasonably disproportionate requirements decrease (bad faith)", "termination without good cause violates state statute", "vertical restraint per se illegal", "inadequate notice"],
        resolution_strategy="UCC 2-306 good faith limits on requirements variation. Exclusive territory: justify pro-competitive effects (Rule of Reason). Termination: comply with notice requirements, state statutes (WI FAIR DEALERSHIP LAW).",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=["Wayman v. Amoco Oil (requirements contract good faith)", "Wisconsin Fair Dealership Law cases", "Continental TV v. GTE Sylvania (vertical restraints Rule of Reason)"]
    )
]


class QueryRequest(BaseModel):
    query: str
    mode: ResponseMode = ResponseMode.FAST
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)


class QueryResponse(BaseModel):
    engine_id: str
    version: str
    query: str
    mode: ResponseMode
    answer: str
    confidence: ConfidenceLevel
    doctrines_triggered: List[str]
    sources: List[str]
    reasoning_chain: List[str]
    telemetry: Dict[str, Any]
    determinism_hash: str


class HealthResponse(BaseModel):
    engine_id: str
    version: str
    status: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float


START_TIME = time.time()
QUERY_LOG = []
DOCTRINE_HIT_COUNT = {d.topic: 0 for d in DOCTRINE_CACHE}


def classify_issue(query: str) -> List[IssueCategory]:
    """Classify query into issue categories."""
    q_lower = query.lower()
    categories = []

    if any(kw in q_lower for kw in ["formation", "offer", "acceptance", "statute of frauds", "consideration"]):
        categories.append(IssueCategory.FORMATION)
    if any(kw in q_lower for kw in ["performance", "delivery", "payment", "cure"]):
        categories.append(IssueCategory.PERFORMANCE)
    if any(kw in q_lower for kw in ["breach", "default", "non-performance", "failure"]):
        categories.append(IssueCategory.BREACH)
    if any(kw in q_lower for kw in ["damages", "remedy", "specific performance", "rescission"]):
        categories.append(IssueCategory.REMEDIES)
    if any(kw in q_lower for kw in ["interpret", "ambiguous", "meaning", "intent"]):
        categories.append(IssueCategory.INTERPRETATION)
    if any(kw in q_lower for kw in ["modification", "amendment", "waiver", "change order"]):
        categories.append(IssueCategory.MODIFICATION)
    if any(kw in q_lower for kw in ["termination", "cancellation", "exit", "end contract"]):
        categories.append(IssueCategory.TERMINATION)
    if any(kw in q_lower for kw in ["liability", "indemnity", "limitation", "cap", "damages exclusion"]):
        categories.append(IssueCategory.LIABILITY)
    if any(kw in q_lower for kw in ["IP", "copyright", "patent", "trademark", "trade secret", "license", "ownership"]):
        categories.append(IssueCategory.IP_RIGHTS)
    if any(kw in q_lower for kw in ["arbitration", "forum", "choice of law", "governing law", "dispute"]):
        categories.append(IssueCategory.DISPUTE_RESOLUTION)

    return categories if categories else [IssueCategory.INTERPRETATION]


def search_doctrines(query: str) -> List[DoctrineBlock]:
    """Search doctrine cache for relevant blocks."""
    q_lower = query.lower()
    matches = []

    for doctrine in DOCTRINE_CACHE:
        score = 0
        for keyword in doctrine.keywords:
            if keyword.lower() in q_lower:
                score += 1
        if score > 0:
            matches.append((score, doctrine))

    matches.sort(reverse=True, key=lambda x: x[0])
    return [d for _, d in matches[:5]]


def three_layer_response(query: str, mode: ResponseMode) -> Tuple[str, List[str], List[str], ConfidenceLevel]:
    """Three-layer response: cache, semantic, deep."""
    doctrines = search_doctrines(query)
    categories = classify_issue(query)

    if not doctrines:
        return (
            "No specific commercial contracts doctrine matched. General contract law principles apply. Consult with counsel for fact-specific analysis.",
            [],
            ["No doctrine cache hit", "General contract law analysis required"],
            ConfidenceLevel.DISCLOSURE
        )

    primary = doctrines[0]
    for d in doctrines:
        DOCTRINE_HIT_COUNT[d.topic] += 1

    reasoning = [
        f"Issue categorized as: {', '.join([c.value for c in categories])}",
        f"Primary doctrine: {primary.topic}",
        f"Key factors: {', '.join(primary.key_factors[:3])}",
        f"Authority: {', '.join(primary.primary_authority[:2])}"
    ]

    if mode == ResponseMode.FAST:
        answer = primary.conclusion_template
    elif mode == ResponseMode.DEFENSE:
        answer = f"{primary.conclusion_template}\n\nReasoning: {primary.reasoning_framework[:300]}...\n\nCounterarguments to anticipate: {'; '.join(primary.counter_arguments[:2])}."
        reasoning.append("Defense strategy: " + primary.resolution_strategy)
    else:  # MEMO
        answer = f"ISSUE: {', '.join([c.value for c in categories])}\n\n"
        answer += f"CONCLUSION: {primary.conclusion_template}\n\n"
        answer += f"ANALYSIS:\n{primary.reasoning_framework}\n\n"
        answer += f"AUTHORITY: {'; '.join(primary.primary_authority)}\n\n"
        if primary.adversary_position:
            answer += f"ADVERSARY POSITION: {primary.adversary_position}\n\n"
        if primary.counter_arguments:
            answer += f"COUNTER-ARGUMENTS:\n" + "\n".join([f"- {c}" for c in primary.counter_arguments]) + "\n\n"
        answer += f"RESOLUTION STRATEGY: {primary.resolution_strategy}\n\n"
        if primary.controlling_precedent:
            answer += f"CONTROLLING PRECEDENT:\n" + "\n".join([f"- {p}" for p in primary.controlling_precedent])

        reasoning.extend([
            f"Burden holder: {primary.burden_holder}",
            f"Confidence: {primary.confidence.value}",
            f"Entity scope: {primary.entity_scope}"
        ])

    sources = primary.primary_authority + primary.controlling_precedent
    confidence = primary.confidence

    return answer, [d.topic for d in doctrines], sources, confidence, reasoning


def compute_determinism_hash(query: str, answer: str, mode: str) -> str:
    """Compute SHA-256 hash for determinism."""
    payload = f"{query}|{mode}|{answer}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrines")
    yield
    logger.info(f"{ENGINE_NAME} shutting down")


app = FastAPI(
    title=ENGINE_NAME,
    version=VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        engine_id=ENGINE_ID,
        version=VERSION,
        status="operational",
        port=PORT,
        doctrines_loaded=len(DOCTRINE_CACHE),
        uptime_seconds=time.time() - START_TIME
    )


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    start = time.time()

    answer, doctrines, sources, confidence, reasoning = three_layer_response(req.query, req.mode)

    determinism_hash = compute_determinism_hash(req.query, answer, req.mode.value)

    latency = time.time() - start

    telemetry = {
        "latency_ms": round(latency * 1000, 2),
        "doctrines_triggered": len(doctrines),
        "mode": req.mode.value,
        "confidence": confidence.value,
        "timestamp": datetime.utcnow().isoformat()
    }

    QUERY_LOG.append({
        "query": req.query,
        "mode": req.mode.value,
        "latency_ms": telemetry["latency_ms"],
        "doctrines": doctrines,
        "timestamp": telemetry["timestamp"]
    })

    logger.info(f"Query processed | mode={req.mode.value} | latency={telemetry['latency_ms']}ms | doctrines={len(doctrines)}")

    return QueryResponse(
        engine_id=ENGINE_ID,
        version=VERSION,
        query=req.query,
        mode=req.mode,
        answer=answer,
        confidence=confidence,
        doctrines_triggered=doctrines,
        sources=sources,
        reasoning_chain=reasoning,
        telemetry=telemetry,
        determinism_hash=determinism_hash
    )


@app.get("/metrics")
async def metrics():
    total_queries = len(QUERY_LOG)
    avg_latency = sum([q["latency_ms"] for q in QUERY_LOG]) / total_queries if total_queries > 0 else 0

    return {
        "engine_id": ENGINE_ID,
        "version": VERSION,
        "total_queries": total_queries,
        "avg_latency_ms": round(avg_latency, 2),
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "doctrine_hit_count": DOCTRINE_HIT_COUNT,
        "mode_distribution": {
            "FAST": sum(1 for q in QUERY_LOG if q["mode"] == "FAST"),
            "DEFENSE": sum(1 for q in QUERY_LOG if q["mode"] == "DEFENSE"),
            "MEMO": sum(1 for q in QUERY_LOG if q["mode"] == "MEMO")
        }
    }


@app.get("/doctrines")
async def list_doctrines():
    return {
        "engine_id": ENGINE_ID,
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "authority": d.primary_authority,
                "confidence": d.confidence.value,
                "hit_count": DOCTRINE_HIT_COUNT[d.topic]
            }
            for d in DOCTRINE_CACHE
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
