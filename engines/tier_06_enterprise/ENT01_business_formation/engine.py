"""
ENT01 Business Formation Engine v1.0.0
Port 9141 | TIE-grade business entity formation and structure analysis
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn

ENGINE_ID = "ENT01"
ENGINE_NAME = "Business Formation Engine"
VERSION = "1.0.0"
PORT = 9141

logger.add(f"logs/{ENGINE_ID}.log", rotation="100 MB", retention="30 days", level="INFO")

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class IssueCategory(str, Enum):
    ENTITY_CHOICE = "ENTITY_CHOICE"
    LLC_FORMATION = "LLC_FORMATION"
    CORP_FORMATION = "CORP_FORMATION"
    PARTNERSHIP = "PARTNERSHIP"
    SOLE_PROP = "SOLE_PROP"
    SERIES_LLC = "SERIES_LLC"
    BENEFIT_CORP = "BENEFIT_CORP"
    PROFESSIONAL_ENTITY = "PROFESSIONAL_ENTITY"
    REGISTERED_AGENT = "REGISTERED_AGENT"
    ANNUAL_COMPLIANCE = "ANNUAL_COMPLIANCE"
    TAX_ELECTION = "TAX_ELECTION"
    JOINT_VENTURE = "JOINT_VENTURE"

class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    controlling_precedent: str

class QueryRequest(BaseModel):
    query: str
    mode: ResponseMode = ResponseMode.FAST
    context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    engine_id: str
    version: str
    query: str
    mode: ResponseMode
    response: str
    confidence: ConfidenceLevel
    latency_ms: float
    triggered_doctrines: List[str]
    determinism_hash: str
    timestamp: str

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="LLC Formation Requirements Under TBOC",
        keywords=["llc", "formation", "certificate", "filing", "texas", "boc"],
        conclusion_template="LLC formation requires certificate of formation filed with Texas Secretary of State under TBOC 3.005, naming clause, registered agent/office, management structure, and member/manager names.",
        reasoning_framework="""Texas Business Organizations Code governs LLC formation. TBOC 3.005 mandates certificate of formation. TBOC 101.051 requires: (1) entity name with LLC/L.L.C., (2) registered agent name/address in Texas, (3) statement of management (member-managed or manager-managed), (4) organizer signature. TBOC 101.052 permits but does not require: operating agreement terms, member names, initial contributions, purpose clause. Filing fee $300. Certificate effective on filing unless delayed effective date specified per TBOC 4.052. Name reservation available 120 days under TBOC 5.001 for $40. Name must be distinguishable from existing entities per TBOC 5.053. Registered agent must have street address in Texas per TBOC 5.201. Failure to maintain registered agent triggers administrative penalties and potential involuntary termination under TBOC 11.252.""",
        key_factors=["Certificate filed with SOS", "Name compliance", "Registered agent in Texas", "Management structure disclosed", "Organizer signature", "Filing fee paid"],
        primary_authority=["TBOC 3.005", "TBOC 101.051", "TBOC 101.052", "TBOC 4.052", "TBOC 5.001", "TBOC 5.053", "TBOC 5.201"],
        burden_holder="Organizer/Members",
        adversary_position="SOS may reject for name conflicts, incomplete filings, or non-compliant agent",
        counter_arguments=["Operating agreement not statutorily required but strongly recommended", "Delayed effective date adds complexity", "Name reservation delays formation"],
        resolution_strategy="File complete certificate with all required fields, verify name availability via SOS search, appoint compliant registered agent, specify management structure clearly",
        entity_scope="Texas LLCs",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="TBOC statutory requirements, SOS filing guidelines"
    ),
    DoctrineBlock(
        topic="LLC Member-Managed vs Manager-Managed",
        keywords=["member managed", "manager managed", "llc", "governance", "authority"],
        conclusion_template="Member-managed LLC: all members have actual authority to bind LLC per TBOC 101.254. Manager-managed LLC: only managers have authority per TBOC 101.255; members lack binding authority absent specific grant.",
        reasoning_framework="""TBOC 101.254 governs member-managed LLCs: each member is agent of LLC with actual authority for carrying on ordinary business. TBOC 101.255 governs manager-managed LLCs: only managers are agents; members lack authority to bind LLC. Election of management structure in certificate of formation is binding on third parties with notice per TBOC 101.302. Operating agreement may limit manager/member authority internally per TBOC 101.054, but such limits do not bind third parties without actual knowledge per TBOC 101.302(b). Default is member-managed if certificate silent per TBOC 101.251. Manager appointment/removal governed by operating agreement or TBOC 101.317 (majority vote). Fiduciary duties: managers/members owe duty of loyalty and care per TBOC 101.401-402, but operating agreement may modify or eliminate except bad faith/intentional misconduct per TBOC 101.401(d). Indemnification permitted per TBOC 8.001-8.003.""",
        key_factors=["Certificate designation", "Operating agreement terms", "Third-party notice", "Actual authority scope", "Fiduciary duty analysis"],
        primary_authority=["TBOC 101.254", "TBOC 101.255", "TBOC 101.302", "TBOC 101.401", "TBOC 101.402"],
        burden_holder="LLC/Members/Managers",
        adversary_position="Third party may argue apparent authority if member in manager-managed LLC acts as agent",
        counter_arguments=["Operating agreement limits not enforceable against third parties", "Apparent authority doctrine may override structural designation"],
        resolution_strategy="Clearly designate management structure in certificate and operating agreement, notify third parties of manager-managed status, include authority limitations in contracts",
        entity_scope="Texas LLCs",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="TBOC 101.254-255, Ritchie v. Rupe 443 S.W.3d 856 (Tex. 2014)"
    ),
    DoctrineBlock(
        topic="Corporation Formation C-Corp vs S-Corp",
        keywords=["corporation", "c-corp", "s-corp", "formation", "election", "1361"],
        conclusion_template="C-corp: default tax status, unlimited shareholders, multiple share classes. S-corp: tax election under IRC 1361, max 100 shareholders, one share class, pass-through taxation.",
        reasoning_framework="""Texas corporations formed under TBOC Title 2. Certificate of formation required per TBOC 3.005, must include: name with corporation/incorporated/company/limited, registered agent/office, authorized shares, incorporator signature per TBOC 21.052. No minimum capital requirement. Filing fee $300. Bylaws not filed but required for governance per TBOC 21.054. Default tax status: C-corp taxed at entity level per IRC 11, dividends taxed to shareholders (double taxation). S-corp election under IRC 1361-1379: (1) max 100 shareholders, (2) only individuals/estates/certain trusts, (3) one class of stock, (4) no nonresident alien shareholders, (5) timely Form 2553 filed with IRS within 2.5 months of tax year start or prior year. S-corp advantages: pass-through taxation avoids double tax, losses flow to shareholders. S-corp disadvantages: shareholder restrictions limit capital raising, built-in gains tax on C-to-S conversion per IRC 1374, passive income limits per IRC 1375. Revocation of S-corp requires majority shareholder consent per IRC 1362(d)(1). Delaware formation alternative: file with Delaware Division of Corporations, $89 fee, annual franchise tax, more flexible corporate law under DGCL.""",
        key_factors=["Shareholder count", "Shareholder eligibility", "Share class structure", "Tax strategy", "Capital needs", "Growth plans"],
        primary_authority=["TBOC 21.052", "IRC 1361", "IRC 1362", "IRC 11", "IRC 1374", "IRC 1375"],
        burden_holder="Incorporator/Shareholders",
        adversary_position="IRS may challenge S-corp election if requirements not met",
        counter_arguments=["S-corp limits hinder equity compensation and VC funding", "C-corp lower rates post-TCJA (21% flat)", "S-corp less flexible for international operations"],
        resolution_strategy="Assess shareholder composition, capital needs, exit strategy; file Form 2553 timely if S-corp desired; maintain single share class and eligible shareholders",
        entity_scope="Texas and Delaware corporations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="IRC 1361-1379, TBOC Title 2, DGCL 101-398"
    ),
    DoctrineBlock(
        topic="General Partnership Formation by Operation of Law",
        keywords=["partnership", "gp", "formation", "agreement", "operation of law"],
        conclusion_template="General partnership formed automatically when two or more persons carry on business for profit as co-owners per TBOC 152.051, regardless of intent or written agreement.",
        reasoning_framework="""TBOC 152.051 defines partnership: association of two or more persons to carry on business for profit as co-owners. No filing required; partnership formed by operation of law when elements met. Key factors: (1) sharing of profits (prima facie evidence of partnership per 152.052), (2) joint control, (3) mutual agency, (4) co-ownership of business. Profit-sharing alone insufficient if received as: wages, rent, debt payment, sale proceeds per 152.052. Written partnership agreement recommended but not required. Partnership governed by TBOC Title 4 (Texas Revised Partnership Act). Partners have equal management rights per 152.101 unless agreement states otherwise. Each partner is agent with authority to bind partnership per 152.301. Partners jointly and severally liable for partnership obligations per 152.306. Partnership not separate taxpayer; income flows to partners per IRC 701-777. Partnership may elect out of subchapter K if gross receipts under $250k per IRC 761(a). Dissolution triggered by partner withdrawal, death, bankruptcy per 152.601 unless agreement provides continuation.""",
        key_factors=["Co-ownership of business", "Profit sharing", "Joint control", "Mutual agency", "Intent to associate"],
        primary_authority=["TBOC 152.051", "TBOC 152.052", "TBOC 152.301", "TBOC 152.306", "IRC 701"],
        burden_holder="Partners",
        adversary_position="Third party creditor may assert partnership liability against individual partner",
        counter_arguments=["Sharing profits as lender/employee does not create partnership", "Joint venture distinguished by single project scope", "LLC provides liability shield GP lacks"],
        resolution_strategy="Draft written partnership agreement defining roles, profit split, management, dissolution; consider LP or LLC for liability protection",
        entity_scope="Texas general partnerships",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="TBOC 152.051-052, Ingram v. Deere 288 S.W.3d 886 (Tex. 2009)"
    ),
    DoctrineBlock(
        topic="Limited Partnership Formation Requirements",
        keywords=["lp", "limited partnership", "certificate", "general partner", "limited partner"],
        conclusion_template="LP formation requires certificate of limited partnership filed with SOS per TBOC 153.101, naming LP, registered agent, general partner names/addresses, and execution by all GPs.",
        reasoning_framework="""TBOC 153.101 governs LP formation: certificate must include (1) partnership name with 'limited partnership' or 'L.P.', (2) registered agent/office, (3) name/address of each general partner, (4) general partner signature. Filing fee $750. TBOC 153.102 permits inclusion of partner contributions, business purpose, dissolution events. Limited partners have no liability beyond capital contribution per TBOC 153.102(a) unless they participate in control per TBOC 153.102(b). General partners have unlimited personal liability for LP obligations per TBOC 153.102(c). TBOC 153.003 permits partnership agreement to govern internal affairs. TBOC 153.151 allows GP to be entity (LLC as GP shields individual liability). Safe harbor: limited partner consulting, advising, guaranteeing does not constitute control per TBOC 153.102(b). Derivative standing for LP per TBOC 153.255. Tax treatment: partnership per IRC 701-777 unless check-the-box election for corporate treatment per Treas. Reg. 301.7701-3.""",
        key_factors=["Certificate filed", "GP named", "LP capital contribution", "Control participation analysis", "GP entity structure"],
        primary_authority=["TBOC 153.101", "TBOC 153.102", "TBOC 153.151", "IRC 701", "Treas. Reg. 301.7701-3"],
        burden_holder="General Partners",
        adversary_position="Creditor may pierce LP veil if limited partner exercises control",
        counter_arguments=["Limited partner safe harbor protects passive investors", "LLC-as-GP structure eliminates individual GP liability", "LP more complex than LLC for small businesses"],
        resolution_strategy="File complete certificate, use LLC as GP to shield liability, define limited partner roles to avoid control participation, draft comprehensive partnership agreement",
        entity_scope="Texas limited partnerships",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="TBOC 153.101-102, Gateway Equity Holdings v. Sikes 474 S.W.3d 766 (Tex. App. 2015)"
    ),
    DoctrineBlock(
        topic="Series LLC Structure and Liability Segregation",
        keywords=["series llc", "liability shield", "segregated assets", "tboc 101.601"],
        conclusion_template="Series LLC creates separate series with segregated assets and liabilities per TBOC 101.601, providing intra-entity liability shield if statutory requirements met.",
        reasoning_framework="""TBOC 101.601 permits LLC to establish one or more series with separate rights, powers, duties. Each series may have separate assets, members, managers, business purpose per 101.602. Certificate of formation must state LLC may establish series per 101.601(a). Series liability shield: debts of one series enforceable only against that series' assets per 101.621, not master LLC or other series, if: (1) certificate authorizes series, (2) separate records maintained for each series per 101.622, (3) notice of liability limitation in certificate per 101.621. Series may sue/be sued per 101.624. Each series files separate tax return if check-the-box election made per IRS Notice 2010-6. Series formation does not require additional SOS filing beyond initial certificate amendment per 101.601. Delaware pioneered series LLC under DGCL 18-215; Texas followed. Uncertainty exists: bankruptcy courts split on whether series is separate entity for bankruptcy purposes (In re Franchise Services of North America 891 F.3d 198 (5th Cir. 2018) held series not separate debtor). Many states do not recognize series LLC liability shield for non-Texas series.""",
        key_factors=["Certificate authorization", "Separate records per series", "Notice in certificate", "Asset segregation", "Multi-state recognition"],
        primary_authority=["TBOC 101.601", "TBOC 101.621", "TBOC 101.622", "IRS Notice 2010-6", "In re Franchise Services 891 F.3d 198"],
        burden_holder="LLC/Series",
        adversary_position="Creditor may argue veil piercing or non-recognition in foreign jurisdiction",
        counter_arguments=["Bankruptcy uncertainty undermines asset protection", "Many states do not recognize series", "Separate entities (multiple LLCs) provide clearer liability shield"],
        resolution_strategy="Include series authorization in certificate, maintain separate books/records/bank accounts for each series, include series liability disclaimer in contracts, consider separate LLCs for multi-state operations",
        entity_scope="Texas series LLCs",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="TBOC 101.601-624, In re Franchise Services 891 F.3d 198"
    ),
    DoctrineBlock(
        topic="Benefit Corporation Social Purpose Requirements",
        keywords=["benefit corporation", "social purpose", "stakeholder", "tboc 21.951"],
        conclusion_template="Benefit corporation must have general public benefit purpose per TBOC 21.951, directors must consider stakeholders beyond shareholders, and must publish annual benefit report.",
        reasoning_framework="""TBOC 21.951-21.960 govern benefit corporations (enacted 2017). Certificate must state corporation is benefit corporation per 21.952. General public benefit required: material positive impact on society and environment per 21.902(1). May specify one or more specific public benefits: charitable, environmental, artistic, economic opportunity, health, education per 21.902(7). Directors must consider: (1) shareholders, (2) employees, (3) customers, (4) community, (5) environment, (6) short/long-term interests per 21.401(a). No director liability for considering stakeholders per 21.401(c). Annual benefit report required per 21.953: assessment of overall social/environmental performance against third-party standard (B Lab, GRI, etc.). Benefit enforcement proceeding limited to shareholders (min 2% or market value per 21.955), directors, benefit corporation itself. Not available to stakeholders or public. Conversion to/from benefit corporation requires 2/3 shareholder vote per 21.952(c). Delaware alternative: public benefit corporation under DGCL 361-368. Federal B-Corp certification (B Lab) separate from legal status; certification requires performance/transparency/accountability standards.""",
        key_factors=["Certificate designation", "General public benefit purpose", "Director stakeholder consideration", "Annual benefit report", "Third-party standard"],
        primary_authority=["TBOC 21.951", "TBOC 21.952", "TBOC 21.401", "TBOC 21.953", "DGCL 361-368"],
        burden_holder="Directors/Officers",
        adversary_position="Shareholders may sue for failure to pursue public benefit or publish report",
        counter_arguments=["Benefit corporation status limits director accountability to shareholders", "Stakeholder balancing creates ambiguity", "Annual reporting adds compliance burden"],
        resolution_strategy="Clearly define public benefit in certificate, adopt third-party standard (B Impact Assessment), train directors on stakeholder balancing, publish timely annual reports",
        entity_scope="Texas benefit corporations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="TBOC 21.951-960, In re Trados Inc. Shareholder Litigation 73 A.3d 17 (Del. Ch. 2013)"
    ),
    DoctrineBlock(
        topic="Professional Entity Restrictions and Requirements",
        keywords=["professional", "pllc", "pc", "licensed", "practice", "professional service"],
        conclusion_template="Professional entities (PC/PLLC) may only perform licensed professional services, all owners must be licensed in the same profession per TBOC 301.003, and entity does not shield from malpractice liability.",
        reasoning_framework="""TBOC Title 7 (301.001-309.001) governs professional entities. Professional services defined per 301.003: services requiring license/certification (law, medicine, accounting, engineering, architecture, etc.). Professional corporation (PC) or professional LLC (PLLC) may render only one type of professional service per 301.004. All owners (shareholders/members) must be licensed to provide that service per 301.006. Certificate must state it is professional entity and identify service per 301.008. Name must include 'Professional Corporation'/'P.C.' or 'Professional Limited Liability Company'/'P.L.L.C.' per 301.010. Entity liable for errors/omissions/negligence of owners/employees per 301.015, but individual owners remain personally liable for own malpractice per 301.014. No general corporate/LLC liability shield for malpractice. Multi-disciplinary practice prohibited unless all services within same license (e.g., CPA providing tax and accounting permitted; CPA-lawyer firm prohibited) per 301.004. Foreign professional entities must register and comply with Texas licensing per 301.017. Law firms: State Bar approval required, see Texas Disciplinary Rules of Professional Conduct 1.04, 1.08.""",
        key_factors=["All owners licensed in profession", "Single professional service", "Certificate designation", "Name compliance", "Malpractice liability retained"],
        primary_authority=["TBOC 301.003", "TBOC 301.004", "TBOC 301.006", "TBOC 301.014", "Texas Disciplinary Rules 1.04"],
        burden_holder="Professional Entity/Owners",
        adversary_position="Client may assert malpractice against individual owner despite entity structure",
        counter_arguments=["Entity provides limited liability for contract/tort claims unrelated to professional services", "Ownership restrictions limit capital raising", "Single-service limitation hinders diversification"],
        resolution_strategy="Ensure all owners properly licensed, obtain errors/omissions insurance, include engagement letters disclaiming entity liability shield for malpractice, comply with profession-specific rules",
        entity_scope="Texas professional entities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="TBOC Title 7, Hooks v. Samson Lone Star 457 S.W.3d 52 (Tex. 2015)"
    ),
    DoctrineBlock(
        topic="Check-the-Box Entity Classification Election",
        keywords=["check the box", "classification", "partnership", "corporation", "8832", "disregarded"],
        conclusion_template="Eligible entities may elect tax classification as corporation, partnership, or disregarded entity per Treas. Reg. 301.7701-3 by filing Form 8832; LLC defaults to disregarded (single-member) or partnership (multi-member).",
        reasoning_framework="""Treas. Reg. 301.7701-2 defines eligible entities: business entity not per se corporation (state law LLC/LP/LLP eligible). Per se corporations: incorporated under state law, insurance companies, certain foreign entities per 301.7701-2(b). Treas. Reg. 301.7701-3 allows eligible entity to elect classification: (1) corporation (taxed under IRC subchapter C or S), (2) partnership (if 2+ members), (3) disregarded entity (if single member). Default classification: domestic LLC with one owner = disregarded, two+ owners = partnership. Election made on Form 8832 filed with IRS, effective date within 75 days prior or 12 months after filing per 301.7701-3(c)(1)(iii). Election change limited: cannot change within 60 months unless IRS permits per 301.7701-3(c)(1)(iv). Disregarded entity: income/deductions reported on owner's return (Schedule C for individual, consolidated return for corporate owner). Partnership: Form 1065 filed, K-1 to partners. Corporation: Form 1120 filed, separate taxpayer. Late election relief: IRS may grant under Rev. Proc. 2009-41 if reasonable cause.""",
        key_factors=["Entity eligibility", "Default classification", "Election timing", "60-month change limitation", "Business purpose analysis"],
        primary_authority=["Treas. Reg. 301.7701-2", "Treas. Reg. 301.7701-3", "Form 8832", "Rev. Proc. 2009-41"],
        burden_holder="Entity/Owners",
        adversary_position="IRS may challenge election if no business purpose or solely tax avoidance",
        counter_arguments=["Disregarded entity simplifies reporting but limits liability protection perception", "Corporate election triggers double taxation absent S-corp election", "Partnership requires Form 1065 complexity"],
        resolution_strategy="Evaluate tax consequences of each classification, file Form 8832 timely if non-default desired, coordinate with S-corp election if applicable, maintain separate entity formalities regardless of tax classification",
        entity_scope="Federal tax classification",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Treas. Reg. 301.7701-2/3, Rev. Proc. 2009-41"
    ),
    DoctrineBlock(
        topic="Registered Agent Requirements and Consequences of Non-Compliance",
        keywords=["registered agent", "service of process", "registered office", "tboc 5.201"],
        conclusion_template="Every Texas entity must maintain registered agent with street address in Texas per TBOC 5.201; failure to maintain agent subjects entity to administrative penalties and potential involuntary termination.",
        reasoning_framework="""TBOC 5.201 requires every filing entity to have registered agent and registered office. Registered agent must be: (1) individual resident of Texas, (2) domestic entity, or (3) foreign entity authorized to transact business in Texas, with street address in Texas per 5.201(b). P.O. Box not permitted for registered office per 5.207. Resignation of agent: agent may resign by filing notice with SOS, effective 31 days after notice to entity per 5.202. Entity must appoint new agent before resignation effective or face penalties. Service of process on entity made by serving registered agent per CPRC 17.044. If agent cannot be found, SOS is agent for service per TBOC 5.255. Non-compliance: SOS may send notice of delinquency, entity has 60 days to cure per TBOC 11.252. Failure to cure: SOS may terminate entity's existence per 11.253. Reinstatement possible within 3 years per 11.301. Commercial registered agent services widely available (CT Corporation, Incorp, etc.). Registered agent address publicly searchable via SOS database.""",
        key_factors=["Agent with Texas street address", "Agent availability for service", "Timely appointment after resignation", "Cure of delinquency within 60 days"],
        primary_authority=["TBOC 5.201", "TBOC 5.202", "TBOC 11.252", "TBOC 11.253", "CPRC 17.044"],
        burden_holder="Entity",
        adversary_position="Plaintiff may argue defective service if agent non-compliant",
        counter_arguments=["Commercial agents add recurring cost", "Involuntary termination reversible within 3 years", "SOS as fallback agent for service"],
        resolution_strategy="Appoint reliable registered agent (commercial service or principal), monitor agent resignations, update promptly if agent changes, respond to SOS delinquency notices immediately",
        entity_scope="All Texas filing entities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="TBOC 5.201-255, 11.252-253, Michiana Easy Livin' Country v. Holten 168 S.W.3d 777 (Tex. 2005)"
    ),
    DoctrineBlock(
        topic="Annual Franchise Tax and Public Information Report Requirements",
        keywords=["franchise tax", "pir", "public information report", "annual filing", "no tax due"],
        conclusion_template="Texas entities must file annual Public Information Report and pay franchise tax per Tax Code 171; LLCs/corps with revenues under $2.47M owe no tax but must file; failure to file triggers forfeiture.",
        reasoning_framework="""Texas Tax Code Chapter 171 imposes franchise tax on entities for privilege of doing business in Texas. Tax rate: 0.375% of taxable margin (retail/wholesale) or 0.75% (other) per 171.002. Taxable margin: total revenue minus greater of (1) COGS, (2) compensation, or (3) 30% of revenue, per 171.101. No tax due threshold: $2.47M total revenue (2024, indexed annually) per 171.002(d). Zero tax entities still must file No Tax Due Report annually. Public Information Report (PIR): filed with Comptroller, due May 15 each year, includes entity info, ownership, officer/director names per Tax Code 171.203. Extension available to Nov 15 if requested by May 15. Penalty for late filing: $50 per owner/officer up to $500 per 171.562. Forfeiture: entity forfeited if does not file for two consecutive years, loses right to sue in Texas courts per 171.252, may be terminated by SOS per TBOC 11.251. Reinstatement: file delinquent reports, pay taxes/penalties, SOS may reinstate per TBOC 11.302. LLCs with passive income only may qualify for reduced 0.575% rate per 171.1016. Exemptions: sole proprietorships, general partnerships (non-entity), certain non-profits per 171.063.""",
        key_factors=["Revenue threshold", "Timely PIR filing", "Tax calculation accuracy", "Forfeiture avoidance", "Passive income analysis"],
        primary_authority=["Tax Code 171.002", "Tax Code 171.101", "Tax Code 171.203", "Tax Code 171.252", "TBOC 11.251"],
        burden_holder="Entity",
        adversary_position="Comptroller may audit and assess additional tax if margin miscalculated",
        counter_arguments=["No tax due entities face compliance burden for zero revenue", "Forfeiture bars lawsuits but not defenses", "Passive entity rate reduces tax for investors"],
        resolution_strategy="Calculate revenue accurately, file PIR by May 15 or obtain extension, monitor threshold changes annually, reinstate promptly if forfeited, consider passive entity planning for investment LLCs",
        entity_scope="Texas LLCs, corporations, LPs, professional entities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Tax Code Ch. 171, Knott Partners v. Aston 734 S.W.2d 116 (Tex. 1987)"
    ),
    DoctrineBlock(
        topic="Sole Proprietorship No Filing Required",
        keywords=["sole proprietorship", "dba", "assumed name", "filing", "liability"],
        conclusion_template="Sole proprietorship requires no formation filing; business conducted in owner's name or assumed name per TBOC 71.001; owner has unlimited personal liability for business debts.",
        reasoning_framework="""Sole proprietorship is not separate legal entity; it is individual conducting business. No formation documents filed with state. TBOC 71.001-71.206 govern assumed name (DBA). If business name differs from owner's legal name, assumed name certificate must be filed with county clerk per 71.051. Assumed name certificate includes: business name, owner name/address, business address, filed in county where principal office located per 71.051-71.052. Filing fee varies by county. Certificate effective 10 years per 71.056. Renewal required. Failure to file assumed name: cannot sue on contract in assumed name per 71.201, but may still be sued. No liability shield: sole proprietor personally liable for all business debts, torts, contracts. Unlimited liability extends to all personal assets. Tax treatment: Schedule C on individual Form 1040, self-employment tax on net income per IRC 1401. No separate EIN required unless hiring employees. Advantages: simplicity, low cost, full control. Disadvantages: unlimited liability, difficulty raising capital, all income taxed at individual rates, no continuity beyond owner's life. Conversion to LLC/corp: form new entity, transfer assets, wind down sole proprietorship.""",
        key_factors=["No formation filing", "Assumed name if applicable", "Unlimited personal liability", "Tax simplicity", "Capital limitations"],
        primary_authority=["TBOC 71.001", "TBOC 71.051", "TBOC 71.201", "IRC 1401", "Schedule C instructions"],
        burden_holder="Owner",
        adversary_position="Creditor may pursue all personal assets for business debt",
        counter_arguments=["LLC costs only $300 formation and provides liability shield", "Sole proprietorship appropriate for low-risk businesses", "Conversion to entity simple if growth occurs"],
        resolution_strategy="File assumed name if using DBA, obtain general liability insurance, maintain separate bank account for business funds, consider LLC if liability risk or growth anticipated",
        entity_scope="Texas sole proprietorships",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="TBOC Ch. 71, Green v. H&R Block 735 F.2d 1039 (5th Cir. 1984)"
    ),
    DoctrineBlock(
        topic="LLP Formation and Limited Liability for Partners",
        keywords=["llp", "limited liability partnership", "professional", "liability shield", "registration"],
        conclusion_template="LLP provides partners limited liability for other partners' malpractice per TBOC 152.801; requires registration with SOS and annual renewal; commonly used by law/accounting firms.",
        reasoning_framework="""TBOC 152.801-152.806 govern registered limited liability partnerships (LLP). LLP is general partnership that has registered as LLP per 152.802. Registration requires: (1) application to SOS, (2) name ending in 'LLP' or 'L.L.P.', (3) registered agent/office, (4) all partner signatures, (5) $200 filing fee per 152.802. Annual renewal required by May 15, $50 fee per partner per 152.805. Failure to renew: LLP reverts to general partnership. Liability shield: partner not personally liable for partnership debts or obligations, including malpractice of other partners, per 152.801(a). Exception: partner remains liable for own malpractice/negligence per 152.801(b). Shield narrower than LLC: LLP protects from partner malpractice but not from ordinary partnership debts in some jurisdictions (Texas provides full shield per 152.801). Professional firms: law firms, accounting firms commonly elect LLP status per TBOC 152.807. Name may include professional designation (e.g., 'Smith & Jones LLP, Attorneys'). Tax treatment: partnership per IRC 701-777. Foreign LLP: must register in Texas if transacting business per 152.903.""",
        key_factors=["Registration with SOS", "Annual renewal", "Name with LLP designation", "Partner liability for own acts", "Professional firm suitability"],
        primary_authority=["TBOC 152.801", "TBOC 152.802", "TBOC 152.805", "TBOC 152.807", "IRC 701"],
        burden_holder="Partners",
        adversary_position="Client may still sue individual partner for that partner's malpractice",
        counter_arguments=["LLC provides broader liability shield and simpler administration", "LLP requires annual renewal (LLC does not)", "LLP historically for professionals but LLC now permitted"],
        resolution_strategy="Register as LLP if partnership desired with liability protection, file annual renewals timely, obtain errors/omissions insurance, consider PLLC as alternative",
        entity_scope="Texas LLPs",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="TBOC 152.801-903, Bohatch v. Butler & Binion 977 S.W.2d 543 (Tex. 1998)"
    ),
    DoctrineBlock(
        topic="Joint Venture Versus Partnership Distinction",
        keywords=["joint venture", "partnership", "single project", "scope", "duration"],
        conclusion_template="Joint venture is partnership limited to single project or transaction per Tex. case law; formed by operation of law like GP but with narrower scope and defined term.",
        reasoning_framework="""Joint venture is species of partnership. Essential elements same as GP per TBOC 152.051: (1) agreement (express or implied), (2) common purpose, (3) community of interest, (4) equal right to control, (5) profit sharing. Distinction: joint venture limited to single project, specific duration, or particular transaction per Schlumberger v. Haverlah 960 S.W.2d 783. Partnership implies continuing business. Joint venture terminates upon project completion. Legal consequences similar: joint venturers are agents of venture, jointly/severally liable for venture debts, fiduciary duties owed, partnership law applies per TBOC 152 unless written agreement states otherwise. No statutory definition of joint venture; common law governs. Joint venture may be formed for: real estate development project, oil/gas lease, single litigation, technology collaboration. Tax treatment: partnership unless entity election made per IRC 761. Advantages over GP: defined scope limits exposure, clear termination point. Disadvantages: same unlimited liability as GP. Alternative: LLC for single project (series LLC for multiple projects). Written agreement critical: define project scope, contributions, profit split, management, dissolution, dispute resolution.""",
        key_factors=["Single project scope", "Defined duration", "Common purpose", "Profit sharing", "Joint control"],
        primary_authority=["TBOC 152.051", "Schlumberger v. Haverlah 960 S.W.2d 783", "IRC 761"],
        burden_holder="Joint Venturers",
        adversary_position="Creditor may assert unlimited liability against any joint venturer",
        counter_arguments=["LLC provides liability shield joint venture lacks", "Joint venture/partnership distinction murky in practice", "Written agreement should specify JV to avoid GP assumption"],
        resolution_strategy="Draft written joint venture agreement specifying project scope, term, responsibilities; consider LLC instead for liability protection; include termination/dissolution provisions",
        entity_scope="Texas joint ventures",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="Schlumberger v. Haverlah 960 S.W.2d 783, TBOC 152.051"
    ),
    DoctrineBlock(
        topic="Delaware vs Texas Formation Comparison",
        keywords=["delaware", "texas", "formation", "dgcl", "tboc", "choice of state"],
        conclusion_template="Delaware offers more flexible corporate law, established Court of Chancery, and prestige for VC-backed startups; Texas offers lower cost, franchise tax parity, and simplicity for operating businesses.",
        reasoning_framework="""Delaware General Corporation Law (DGCL) widely regarded as most developed corporate law. Advantages: (1) Court of Chancery specialized business court with centuries of precedent, (2) director-friendly laws (exculpation under DGCL 102(b)(7), indemnification), (3) flexible governance (DGCL 141 board-centric), (4) no corporate income tax for out-of-state operations, (5) privacy (no officer/director names in certificate), (6) VC/IPO preference. Delaware costs: $89 formation, $300 annual franchise tax minimum (up to $200k+ for large cos), registered agent required, annual report due. Texas TBOC advantages: (1) lower formation cost ($300), (2) no separate franchise tax (Texas franchise tax applies regardless of formation state if doing business in Texas), (3) simpler for Texas-only operations, (4) no annual report to SOS. Texas costs: $300 formation, franchise tax (same threshold as DE-formed entities doing business in TX). Operational analysis: DE-formed entities doing business in TX must register as foreign entity ($750), appoint TX registered agent, file TX franchise tax, so dual compliance burden. Texas entity doing business only in TX: single compliance regime. Delaware preferred for: venture capital, national operations, eventual IPO. Texas preferred for: small businesses, Texas-only operations, lower cost. LLC considerations: fewer differences between DE and TX LLC law; TX LLC sufficient for most purposes.""",
        key_factors=["Business scope (local vs national)", "VC funding plans", "IPO potential", "Cost sensitivity", "Governance flexibility needs"],
        primary_authority=["DGCL 101-398", "TBOC Title 2", "DGCL 141", "DGCL 102(b)(7)", "Texas Tax Code 171"],
        burden_holder="Incorporators",
        adversary_position="Dual compliance if DE entity operates in TX",
        counter_arguments=["Delaware's legal advantages overstated for private companies", "Texas courts competent for business disputes", "Delaware franchise tax increases over time with equity value"],
        resolution_strategy="Choose Delaware if seeking VC funding or planning national expansion/IPO; choose Texas if local operations or cost-sensitive; always register foreign entity in states of operation",
        entity_scope="Corporations (Delaware vs Texas)",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="DGCL 101-398, TBOC Title 2, VantagePoint Venture Partners v. Examen 871 A.2d 1108 (Del. 2005)"
    ),
    DoctrineBlock(
        topic="Close Corporation Election and Shareholder Agreements",
        keywords=["close corporation", "shareholder agreement", "closely held", "restrictions"],
        conclusion_template="Close corporation election under TBOC 21.701 permits shareholder management, restriction on transfers, and elimination of board; shareholder agreement may govern all aspects of corporation.",
        reasoning_framework="""TBOC 21.701-21.712 govern close corporations. Election made in certificate of formation per 21.702: 'This corporation is a close corporation.' Requirements: (1) all shares subject to transfer restrictions per 21.704, (2) no public offering, (3) max 35 shareholders per 21.701. Close corporation may: (1) be managed by shareholders rather than board per 21.705, (2) eliminate or restrict board powers, (3) allocate voting rights disproportionate to ownership. Shareholder agreement per 21.101: may govern any aspect of corporation including management, dividends, election of directors, even if agreement 'treats the corporation as if it were a partnership' per 21.101(b)(4). Agreement enforceable among shareholders and binding on corporation. Share transfer restrictions: right of first refusal, buy-sell agreements, drag-along, tag-along provisions. Mandatory buyout on death/disability/termination common. Valuation mechanisms: book value, multiple of earnings, appraisal. Close corporation not available for public companies or those with >35 shareholders. Tax treatment: C-corp or S-corp election available. Advantages: control, flexibility, alignment of ownership/management. Disadvantages: illiquidity, valuation disputes, deadlock risk. Texas allows voting trusts per 21.201, irrevocable proxies per 21.359 as alternatives to close corporation structure.""",
        key_factors=["Transfer restrictions", "Shareholder count limit", "Management structure", "Valuation mechanism", "Deadlock resolution"],
        primary_authority=["TBOC 21.701", "TBOC 21.101", "TBOC 21.704", "TBOC 21.705"],
        burden_holder="Shareholders",
        adversary_position="Minority shareholder may claim oppression if agreements unfair",
        counter_arguments=["Shareholder agreements available without close corporation election", "Transfer restrictions hinder exit liquidity", "Deadlock requires judicial dissolution"],
        resolution_strategy="Draft comprehensive shareholder agreement with buy-sell provisions, valuation formula, deadlock resolution (arbitration, shotgun clause), consider close corp election for maximum flexibility",
        entity_scope="Texas close corporations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="TBOC 21.701-21.712, Ritchie v. Rupe 443 S.W.3d 856 (Tex. 2014)"
    ),
    DoctrineBlock(
        topic="Certificate of Formation Amendment Procedures",
        keywords=["amendment", "certificate", "restated certificate", "shareholder vote"],
        conclusion_template="Amendment to certificate of formation requires owner approval (shareholders/members) per TBOC 3.051-3.059 and filing with SOS; procedures vary by entity type and amendment type.",
        reasoning_framework="""TBOC 3.051 governs certificate amendments. General rule: amendment requires: (1) approval by owners (shareholders for corp, members for LLC, partners for LP) per 3.053, (2) filing of certificate of amendment with SOS per 3.051, (3) $150 filing fee. Shareholder vote for corporations: board adopts amendment, shareholders approve by majority unless certificate requires supermajority per 21.364. Class vote required if amendment affects class rights per 21.365. LLC amendment: requires vote of members holding majority of membership interests unless operating agreement specifies different threshold per 101.355. Name change: certificate of amendment required. Registered agent change: statement of change filed per 5.202 (not amendment). Authorized shares increase: certificate amendment with shareholder approval per 21.156. Restated certificate: consolidates all amendments into single document per 3.059, does not require shareholder vote unless making new amendments. Effective date: on filing unless delayed effective date specified per 4.052 (max 90 days). Correcting certificate: certificate of correction may fix immaterial errors without owner vote per 4.102.""",
        key_factors=["Amendment type", "Owner approval threshold", "Class vote requirements", "Filing with SOS", "Effective date"],
        primary_authority=["TBOC 3.051", "TBOC 3.053", "TBOC 21.364", "TBOC 21.365", "TBOC 101.355"],
        burden_holder="Entity/Owners",
        adversary_position="Minority owners may challenge amendment as oppressive",
        counter_arguments=["Supermajority provisions in certificate protect minority", "Restated certificate clarifies without substantive change", "Correction certificate avoids formal amendment for errors"],
        resolution_strategy="Review certificate and operating agreement for vote thresholds, obtain required owner consents, file certificate of amendment with SOS, update internal records",
        entity_scope="All Texas filing entities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="TBOC 3.051-3.059, 21.364-365"
    ),
    DoctrineBlock(
        topic="Foreign Entity Registration Requirements",
        keywords=["foreign entity", "registration", "certificate of authority", "transacting business"],
        conclusion_template="Foreign entity (formed outside Texas) must register with Texas SOS per TBOC 9.001 if transacting business in Texas; failure bars lawsuits and triggers penalties.",
        reasoning_framework="""TBOC 9.001 requires foreign filing entity to register before transacting business in Texas. Registration: file application for registration per 9.004, includes: (1) entity name, (2) jurisdiction of formation, (3) registered agent/office in Texas, (4) name/address of governing persons. Filing fee: $750. 'Transacting business' per 9.251: regular business activity, not isolated transactions. Safe harbors (not transacting business): maintaining bank accounts, holding meetings, maintaining offices without other activities, owning property, conducting isolated transactions per 9.251(b). Consequences of non-registration per 9.051: (1) foreign entity cannot maintain lawsuit in Texas, (2) $500 penalty per year, (3) $1,000 penalty if aware of duty to register. Registration cures retroactively per 9.053. Withdrawal: foreign entity may withdraw by filing application per 9.011 if no longer doing business in Texas. Name conflicts: if name unavailable, must adopt assumed name per 9.004(b). Tax obligations: registered foreign entities subject to Texas franchise tax per Tax Code 171. Secretary of State service: SOS is agent for service if foreign entity has no agent per 9.101.""",
        key_factors=["Regular business activity in Texas", "Registration filing", "Registered agent in Texas", "Penalty avoidance", "Lawsuit standing"],
        primary_authority=["TBOC 9.001", "TBOC 9.004", "TBOC 9.051", "TBOC 9.251", "Tax Code 171"],
        burden_holder="Foreign Entity",
        adversary_position="Defendant may move to dismiss if foreign entity plaintiff not registered",
        counter_arguments=["Isolated transactions do not require registration", "Registration cures retroactively for lawsuit standing", "Safe harbors protect passive investment"],
        resolution_strategy="Register before conducting regular business in Texas, appoint Texas registered agent, file franchise tax returns, withdraw if ceasing Texas operations",
        entity_scope="Foreign entities doing business in Texas",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="TBOC 9.001-9.251, DeSantis v. Wackenhut Corp. 793 S.W.2d 670 (Tex. 1990)"
    ),
    DoctrineBlock(
        topic="Operating Agreement Governance and Enforceability",
        keywords=["operating agreement", "llc", "governance", "enforceability", "oral agreement"],
        conclusion_template="LLC operating agreement governs internal affairs per TBOC 101.052, may be oral or written, enforceable among members and against LLC, and may modify default statutory rules.",
        reasoning_framework="""TBOC 101.052 permits LLC to be governed by operating agreement. Operating agreement may be oral or written per 101.052(c). Agreement may: (1) modify or eliminate fiduciary duties except for bad faith/intentional misconduct per 101.401(d), (2) establish management structure, (3) define member rights, (4) allocate profits/losses disproportionate to ownership per 101.106, (5) impose transfer restrictions, (6) provide indemnification. Operating agreement not required by statute but strongly recommended. Agreement binding on members and LLC per 101.054. Third parties not bound unless agreement terms incorporated into contracts. Default rules apply if operating agreement silent: member-managed per 101.251, profits/losses per ownership percentage per 101.106, voting per ownership per 101.352, unanimous consent for extraordinary matters per 101.355. Amendment of operating agreement: per terms of agreement or unanimous consent per 101.052(b). Enforceability: Ritchie v. Rupe 443 S.W.3d 856 held operating agreement may limit fiduciary duties and specify grounds for member removal. Oral agreements enforceable but difficult to prove; written agreement best practice.""",
        key_factors=["Written vs oral", "Fiduciary duty modifications", "Profit/loss allocations", "Amendment procedures", "Transfer restrictions"],
        primary_authority=["TBOC 101.052", "TBOC 101.054", "TBOC 101.401", "Ritchie v. Rupe 443 S.W.3d 856"],
        burden_holder="Members",
        adversary_position="Member may challenge operating agreement as unconscionable or against public policy",
        counter_arguments=["Written operating agreement prevents disputes", "Fiduciary duty elimination may enable misconduct", "Oral agreements hard to prove"],
        resolution_strategy="Draft comprehensive written operating agreement addressing management, capital, distributions, transfers, dissolution; obtain all member signatures; amend as needed per amendment provisions",
        entity_scope="Texas LLCs",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="TBOC 101.052-054, Ritchie v. Rupe 443 S.W.3d 856"
    ),
    DoctrineBlock(
        topic="Member/Shareholder Approval for Fundamental Transactions",
        keywords=["merger", "conversion", "sale of assets", "dissolution", "fundamental transaction"],
        conclusion_template="Fundamental transactions (merger, sale of assets, dissolution, conversion) require owner approval per TBOC; specific vote thresholds vary by transaction type and entity.",
        reasoning_framework="""TBOC defines fundamental transactions requiring owner approval. Merger per 10.001-10.008: requires approval of owners of each constituent entity. Corporations: board adopts, shareholders approve by majority unless certificate requires more per 21.457. LLCs: member approval per 101.355 (default unanimous for fundamental matters). Sale of all/substantially all assets per 21.458 (corp) or 101.355 (LLC): owner approval required. Dissolution: requires owner approval per 11.051-11.058, filing certificate of termination per 11.101. Conversion per 10.101-10.108: entity changes type (e.g., LLC to corporation) without dissolution; requires plan of conversion and owner approval. Domestication per 10.201-10.208: foreign entity becomes Texas entity or vice versa; owner approval required. Dissenting owners' appraisal rights: shareholders/members may demand fair value for ownership interest if they vote against merger/conversion/sale per 10.351-10.365. Appraisal triggered by: (1) merger where consideration is not shares of surviving entity, (2) conversion, (3) sale of substantially all assets. No appraisal for publicly traded shares (market out exception) per 10.354. Short-form merger per 21.459: parent owning 90%+ may merge out minority without minority vote, but appraisal rights remain.""",
        key_factors=["Transaction type", "Owner vote threshold", "Appraisal rights", "Certificate/agreement provisions", "Dissent notice requirements"],
        primary_authority=["TBOC 10.001", "TBOC 21.457", "TBOC 21.458", "TBOC 10.351", "TBOC 11.051"],
        burden_holder="Entity/Owners",
        adversary_position="Dissenting owner may demand appraisal and challenge valuation",
        counter_arguments=["Supermajority provisions protect minority", "Appraisal provides exit for dissenters", "Short-form merger disenfranchises minority but offers appraisal"],
        resolution_strategy="Obtain required owner approvals per statute and governing documents, provide appraisal notice to dissenters, comply with timelines, file required certificates with SOS",
        entity_scope="All Texas entities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="TBOC 10.001-10.365, 11.051-11.101, Weinberger v. UOP Inc. 457 A.2d 701 (Del. 1983)"
    ),
    DoctrineBlock(
        topic="Pre-Formation Contracts and Promoter Liability",
        keywords=["pre-formation", "promoter", "liability", "contracts before incorporation"],
        conclusion_template="Promoter who enters contract on behalf of entity before formation is personally liable unless: (1) contract expressly relieves promoter, (2) entity adopts contract and other party releases promoter, per Tex. case law.",
        reasoning_framework="""Entity cannot contract before formation because it does not exist. Promoter is person who takes initiative to form entity and enter contracts on its behalf before formation. General rule: promoter personally liable on pre-formation contracts per Quaker Hill v. Parr 148 S.W.3d 847. Exceptions: (1) contract states promoter not liable ('to be bound only upon formation'), (2) contract expressly novates upon formation (substitutes entity for promoter), (3) entity adopts contract after formation AND other party releases promoter (novation). Entity adoption alone does not release promoter; both entity and promoter liable unless other party agrees to release per common law novation. Entity may adopt pre-formation contract by: (1) express board/member resolution, (2) accepting benefits under contract, (3) continuing performance. Adoption makes entity liable but does not automatically discharge promoter. Best practice: include clause in pre-formation contract: 'This agreement is entered into by Promoter on behalf of Entity to be formed; Promoter shall have no personal liability upon Entity's formation and assumption of this agreement.' TBOC 2.101 permits entity to ratify acts taken in its name before formation, ratification relates back.""",
        key_factors=["Contract language re promoter liability", "Entity adoption after formation", "Other party release of promoter", "Novation analysis"],
        primary_authority=["Quaker Hill v. Parr 148 S.W.3d 847", "TBOC 2.101", "Restatement (Second) Contracts 326"],
        burden_holder="Promoter",
        adversary_position="Other party may sue promoter and entity jointly for pre-formation contract breach",
        counter_arguments=["Entity formation and adoption should relieve promoter", "Other party expects to contract with entity not individual", "Novation requires other party consent"],
        resolution_strategy="Include promoter exculpation clause in pre-formation contracts, obtain entity adoption via board/member resolution after formation, seek written release from other party upon adoption",
        entity_scope="All entities",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="Quaker Hill v. Parr 148 S.W.3d 847, TBOC 2.101"
    ),
    DoctrineBlock(
        topic="Entity Name Reservation and Availability",
        keywords=["name reservation", "name availability", "distinguishable", "tboc 5.001"],
        conclusion_template="Entity name must be distinguishable from existing names per TBOC 5.053; name reservation available for 120 days per TBOC 5.001; SOS determines distinguishability.",
        reasoning_framework="""TBOC 5.053 requires entity name to be distinguishable upon SOS records from: (1) existing entity names, (2) reserved names, (3) assumed names. Distinguishable standard: more than punctuation, capitalization, articles, conjunctions, abbreviations per 5.053(c). Example: 'ABC Company LLC' not distinguishable from 'ABC Company L.L.C.' or 'The ABC Company, LLC.' Name reservation per 5.001: file application with SOS, $40 fee, reserves name for 120 days, renewable. Reserved name cannot be used by another during reservation period. Name must include entity designation: 'corporation'/'incorporated'/'company'/'limited' or abbreviation for corporations per 5.054; 'limited liability company' or 'LLC'/'L.L.C.' for LLCs per 5.056; 'limited partnership' or 'LP'/'L.P.' for LPs per 5.057. Prohibited names: cannot imply governmental affiliation, cannot contain restricted words (bank, insurance, university) without approval per 5.053. Assumed name (DBA): if entity wishes to operate under additional name, file assumed name certificate per 71.002. Trade name vs legal name: legal name in certificate; trade name for marketing may differ. SOS online name search available but not conclusive; filing rejected if name found not distinguishable.""",
        key_factors=["Distinguishability from existing names", "Entity designation inclusion", "Prohibited words avoidance", "Reservation timing"],
        primary_authority=["TBOC 5.001", "TBOC 5.053", "TBOC 5.054", "TBOC 5.056", "TBOC 71.002"],
        burden_holder="Entity/Organizer",
        adversary_position="SOS may reject certificate if name not distinguishable",
        counter_arguments=["Name search tools imperfect", "Reservation delays formation", "Assumed name allows flexibility"],
        resolution_strategy="Conduct SOS name search before filing, reserve name if filing delayed, include proper entity designation, avoid prohibited words, file assumed name for additional trade names",
        entity_scope="All Texas filing entities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="TBOC 5.001-5.057, SOS filing guidelines"
    ),
    DoctrineBlock(
        topic="Piercing the Corporate Veil Alter Ego Doctrine",
        keywords=["veil piercing", "alter ego", "undercapitalization", "commingling", "fraud"],
        conclusion_template="Veil piercing allows creditor to hold owners personally liable if: (1) entity is alter ego of owner (unity of interest), and (2) upholding entity would sanction fraud or promote injustice, per Castleberry v. Branscum.",
        reasoning_framework="""Texas recognizes veil piercing in limited circumstances per Castleberry v. Branscum 721 S.W.2d 270. Two-prong test: (1) Alter ego: unity of interest such that separate personalities of entity and owner cease to exist. Factors: commingling of funds, failure to maintain separate books/records, undercapitalization, failure to observe formalities (no meetings/resolutions), siphoning of funds, absence of corporate assets, use of entity to perpetrate fraud. (2) Injustice: upholding entity form would sanction fraud or promote injustice. Must show actual fraud or wrong such that equity requires disregard of entity. Inadequate capitalization alone insufficient per SSP Partners v. Gladstrong Investments 275 S.W.3d 444; must show fraudulent intent. Single-member LLC: same veil piercing standard applies per Shook v. Walden 368 S.W.3d 604. Reverse piercing: creditor of owner seeks to reach entity assets; Texas courts split on permissibility. Contract creditors: veil piercing harder than tort creditors. Formalities: maintaining minutes, resolutions, separate accounts critical to avoid piercing. Parent-subsidiary: veil piercing possible if parent dominates subsidiary and uses it as mere instrumentality.""",
        key_factors=["Commingling of funds", "Undercapitalization", "Failure to observe formalities", "Fraudulent intent", "Injustice to creditor"],
        primary_authority=["Castleberry v. Branscum 721 S.W.2d 270", "SSP Partners v. Gladstrong 275 S.W.3d 444", "Shook v. Walden 368 S.W.3d 604"],
        burden_holder="Creditor seeking to pierce",
        adversary_position="Entity/owners defend by showing separate existence, proper capitalization, formalities observed",
        counter_arguments=["Veil piercing requires actual fraud not mere undercapitalization", "Single-member LLCs inherently more vulnerable", "Contract creditors agreed to deal with entity"],
        resolution_strategy="Maintain separate bank accounts, adequate capitalization, corporate formalities (meetings, minutes, resolutions), avoid commingling, document all loans/transactions with entity",
        entity_scope="All Texas entities",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="Castleberry v. Branscum 721 S.W.2d 270, SSP Partners v. Gladstrong 275 S.W.3d 444"
    ),
    DoctrineBlock(
        topic="Entity Dissolution and Winding Up Procedures",
        keywords=["dissolution", "winding up", "termination", "certificate of termination"],
        conclusion_template="Voluntary dissolution requires owner approval per TBOC 11.051, followed by winding up (paying creditors, distributing assets) per 11.053, and filing certificate of termination per 11.101.",
        reasoning_framework="""TBOC 11.051-11.101 govern voluntary dissolution. Process: (1) Owner approval: shareholders/members/partners approve dissolution per governing documents or statutory default. (2) Winding up: entity pays/provides for debts, distributes remaining assets to owners per 11.053. Entity continues for winding up purposes per 11.052. (3) Certificate of termination: filed with SOS after winding up complete per 11.101, states all debts paid/provided for. Filing fee $40. Tax clearance: Comptroller issues tax clearance letter after final franchise tax return filed per Tax Code 171.2515. Involuntary dissolution: court may order dissolution for deadlock, oppression, fraud, waste per 11.404. Judicial winding up under court supervision per 11.405. Receiver may be appointed per 11.406. Administrative termination: SOS may terminate entity for failure to file reports, maintain registered agent per 11.251-11.253. Reinstatement possible within 3 years per 11.301. Creditor claims after termination: entity liable for known claims if not paid during winding up; 3-year statute of limitations on unknown claims per 11.356. Distribution to owners: per certificate/operating agreement/partnership agreement or statutory default (pro rata to ownership).""",
        key_factors=["Owner approval", "Debt payment or provision", "Asset distribution", "Certificate of termination filed", "Tax clearance obtained"],
        primary_authority=["TBOC 11.051", "TBOC 11.053", "TBOC 11.101", "TBOC 11.251", "Tax Code 171.2515"],
        burden_holder="Entity/Owners",
        adversary_position="Creditor may sue for unpaid debts during winding up period",
        counter_arguments=["Certificate of termination shields from future claims if properly wound up", "Reinstatement possible if termination accidental", "Judicial dissolution available if voluntary dissolution disputed"],
        resolution_strategy="Obtain owner approval per governing documents, pay or escrow for all known debts, distribute remaining assets, file certificate of termination and obtain tax clearance, consider receiver if disputes exist",
        entity_scope="All Texas entities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="TBOC 11.051-11.405, Ritchie v. Rupe 443 S.W.3d 856"
    ),
    DoctrineBlock(
        topic="Single-Member LLC Liability Protection and Formalities",
        keywords=["single member llc", "smllc", "liability", "formalities", "charging order"],
        conclusion_template="Single-member LLC provides same liability shield as multi-member LLC per Tex. case law, but requires strict observance of formalities to avoid veil piercing; charging order protection applies per TBOC 101.112.",
        reasoning_framework="""Texas recognizes single-member LLC (SMLLC) per TBOC 101.101. Liability shield: SMLLC member not liable for LLC debts per 101.114, same as multi-member LLC. Veil piercing: Shook v. Walden 368 S.W.3d 604 held same alter ego standard applies to SMLLC. SMLLC more vulnerable to piercing due to: (1) no separation between owner and entity in practice, (2) commingling easier with single member, (3) less formality observed. Best practices to avoid piercing: (1) maintain separate bank account, (2) adopt written operating agreement, (3) hold annual meetings with minutes, (4) capitalize adequately, (5) avoid commingling, (6) file separate tax return (even if disregarded entity, maintain books), (7) title assets in LLC name, (8) sign contracts as 'LLC by Member' not personally. Charging order: creditor of member may obtain charging order against member's interest per 101.112, but cannot foreclose on SMLLC interest or force dissolution per 101.112(c). Charging order as exclusive remedy protects SMLLC from member's personal creditors. Operating agreement: recommended even for SMLLC to document governance, avoid default rules, demonstrate separate existence.""",
        key_factors=["Separate bank account", "Operating agreement", "Adequate capitalization", "No commingling", "Formalities observed"],
        primary_authority=["TBOC 101.101", "TBOC 101.114", "TBOC 101.112", "Shook v. Walden 368 S.W.3d 604"],
        burden_holder="Member",
        adversary_position="Creditor may pierce veil if formalities ignored or commingling shown",
        counter_arguments=["SMLLC inherently harder to separate from owner", "Charging order protection robust in Texas", "Formalities less important for SMLLC than corporations"],
        resolution_strategy="Maintain separate bank account and books, adopt operating agreement, avoid personal use of LLC assets, capitalize adequately, document all transactions, file separate tax return even if disregarded",
        entity_scope="Texas single-member LLCs",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="Shook v. Walden 368 S.W.3d 604, TBOC 101.112"
    ),
]

METRICS = {
    "total_queries": 0,
    "cache_hits": 0,
    "semantic_searches": 0,
    "deep_analyses": 0,
    "avg_latency_ms": 0.0,
    "error_count": 0
}

def normalize_query(query: str) -> str:
    q = query.lower().strip()
    replacements = {
        "limited liability company": "llc",
        "l.l.c.": "llc",
        "corporation": "corp",
        "incorporated": "corp",
        "professional limited liability company": "pllc",
        "p.l.l.c.": "pllc",
        "professional corporation": "pc",
        "limited partnership": "lp",
        "l.p.": "lp",
        "limited liability partnership": "llp",
        "l.l.p.": "llp",
        "general partnership": "gp",
        "secretary of state": "sos",
        "registered agent": "agent",
        "certificate of formation": "cof",
        "operating agreement": "oa",
        "internal revenue code": "irc",
        "texas business organizations code": "tboc"
    }
    for old, new in replacements.items():
        q = q.replace(old, new)
    return q

def search_doctrine_cache(query: str) -> List[DoctrineBlock]:
    norm = normalize_query(query)
    words = set(norm.split())
    matches = []
    for doctrine in DOCTRINE_CACHE:
        kw_set = set(k.lower() for k in doctrine.keywords)
        if words & kw_set:
            matches.append(doctrine)
    return matches

def generate_fast_response(query: str, doctrines: List[DoctrineBlock]) -> str:
    if not doctrines:
        return "No direct doctrine match. Consider: entity choice depends on liability needs, tax goals, management structure, and compliance burden. Consult TBOC Title 1-11 and IRC for specifics."
    d = doctrines[0]
    return f"{d.conclusion_template} See {', '.join(d.primary_authority[:3])}."

def generate_defense_response(query: str, doctrines: List[DoctrineBlock]) -> str:
    if not doctrines:
        return "ANALYSIS: Query implicates entity formation law under TBOC. Without specific facts, general principles apply: (1) choice of entity driven by liability exposure, tax treatment, governance needs; (2) formation requires statutory compliance (certificate filing, registered agent, fees); (3) ongoing compliance (annual reports, franchise tax) mandatory. Recommend detailed fact analysis and review of TBOC Title 1-11, Tax Code Ch. 171, IRC."
    parts = []
    for d in doctrines[:3]:
        parts.append(f"DOCTRINE: {d.topic}\nAUTHORITY: {', '.join(d.primary_authority)}\nANALYSIS: {d.reasoning_framework[:400]}...\nCONCLUSION: {d.conclusion_template}\n")
    return "\n".join(parts)

def generate_memo_response(query: str, doctrines: List[DoctrineBlock]) -> str:
    if not doctrines:
        return "MEMORANDUM\n\nISSUE: Entity formation and structure analysis.\n\nBRIEF ANSWER: Entity choice and formation governed by TBOC. Key factors: liability shield (LLC/corp vs GP/sole prop), tax treatment (pass-through vs C-corp, S-corp election), management (member/manager, board/shareholder), compliance (filing, annual reports, franchise tax). Recommend detailed analysis of specific business needs, jurisdiction (TX vs DE), and long-term strategy.\n\nDISCUSSION: See TBOC Title 1-11, Tax Code Ch. 171, IRC 1361-1379, 701-777.\n\nCONCLUSION: Consult counsel for entity selection and formation tailored to facts."
    memo = f"MEMORANDUM\n\nQUERY: {query}\n\n"
    for i, d in enumerate(doctrines[:5], 1):
        memo += f"{i}. {d.topic.upper()}\n"
        memo += f"   Authority: {', '.join(d.primary_authority)}\n"
        memo += f"   Framework: {d.reasoning_framework[:300]}...\n"
        memo += f"   Factors: {'; '.join(d.key_factors)}\n"
        memo += f"   Confidence: {d.confidence.value}\n"
        memo += f"   Conclusion: {d.conclusion_template}\n\n"
    memo += "RECOMMENDATION: Apply doctrine analysis to specific facts. Consider hybrid structures, multi-state implications, tax elections. Consult TX attorney for formation execution."
    return memo

def compute_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()[:16]

APP = FastAPI(title=ENGINE_NAME, version=VERSION)
APP.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@APP.get("/health")
def health():
    return {
        "engine_id": ENGINE_ID,
        "name": ENGINE_NAME,
        "version": VERSION,
        "status": "healthy",
        "port": PORT,
        "metrics": METRICS,
        "doctrine_count": len(DOCTRINE_CACHE)
    }

@APP.post("/query", response_model=QueryResponse)
def query_endpoint(req: QueryRequest):
    start = time.time()
    METRICS["total_queries"] += 1
    try:
        doctrines = search_doctrine_cache(req.query)
        triggered = [d.topic for d in doctrines]
        if doctrines:
            METRICS["cache_hits"] += 1
        confidence = doctrines[0].confidence if doctrines else ConfidenceLevel.DISCLOSURE
        if req.mode == ResponseMode.FAST:
            response_text = generate_fast_response(req.query, doctrines)
        elif req.mode == ResponseMode.DEFENSE:
            response_text = generate_defense_response(req.query, doctrines)
        else:
            response_text = generate_memo_response(req.query, doctrines)
        latency = (time.time() - start) * 1000
        METRICS["avg_latency_ms"] = (METRICS["avg_latency_ms"] * (METRICS["total_queries"] - 1) + latency) / METRICS["total_queries"]
        det_hash = compute_hash(req.query + req.mode.value + response_text)
        return QueryResponse(
            engine_id=ENGINE_ID,
            version=VERSION,
            query=req.query,
            mode=req.mode,
            response=response_text,
            confidence=confidence,
            latency_ms=round(latency, 2),
            triggered_doctrines=triggered,
            determinism_hash=det_hash,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    except Exception as e:
        METRICS["error_count"] += 1
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    uvicorn.run(APP, host="0.0.0.0", port=PORT)
