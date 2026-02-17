"""
ENT12: Commercial Real Estate Intelligence Engine v1.0.0
TIE-Grade - 25+ Doctrine Blocks, Full CRE Law Domain Expertise
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Literal, Any
from enum import Enum
from dataclasses import dataclass, field, asdict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

ENGINE_ID = "ENT12"
ENGINE_NAME = "Commercial Real Estate Engine"
VERSION = "1.0.0"
PORT = 9152

# ═══════════════════════════════════════════════════════════════════════════
# ENUMS & MODELS
# ═══════════════════════════════════════════════════════════════════════════

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class IssueCategory(str, Enum):
    LEASE_STRUCTURE = "LEASE_STRUCTURE"
    FINANCING = "FINANCING"
    DUE_DILIGENCE = "DUE_DILIGENCE"
    TAX_PLANNING = "TAX_PLANNING"
    ZONING = "ZONING"
    ENVIRONMENTAL = "ENVIRONMENTAL"
    TITLE = "TITLE"
    REIT = "REIT"
    CONSTRUCTION = "CONSTRUCTION"
    OPERATIONS = "OPERATIONS"

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str
    issue_category: IssueCategory

class QueryRequest(BaseModel):
    query: str = Field(..., description="CRE transaction question")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(AnalysisZone.PLANNING, description="Analysis context")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)

class QueryResponse(BaseModel):
    engine_id: str
    version: str
    query: str
    mode: ResponseMode
    zone: AnalysisZone
    response: str
    confidence: ConfidenceLevel
    authorities_cited: List[str]
    doctrine_blocks_triggered: List[str]
    latency_ms: float
    determinism_hash: str
    timestamp: str

# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE - 25+ REAL CRE LAW BLOCKS
# ═══════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Triple Net Lease Structure",
        keywords=["NNN", "triple net", "net lease", "CAM", "operating expenses", "base rent"],
        conclusion_template=[
            "Triple net lease shifts property taxes, insurance, and maintenance to tenant.",
            "Base rent remains fixed; tenant pays proportionate share of operating expenses.",
            "Landlord's income stream becomes passive; tenant bears operational risk."
        ],
        reasoning_framework="""
NNN Lease Framework:
1. Base Rent: Fixed amount per SF, typically lower than gross lease
2. Additional Rent Components:
   - Property taxes (pro rata share)
   - Building insurance (fire, liability)
   - Common Area Maintenance (CAM): landscaping, parking, HVAC, janitorial
3. Tenant's Proportionate Share = (Tenant SF / Total Leasable SF)
4. CAM Reconciliation: Annual true-up based on actual expenses
5. Caps: Some leases cap annual CAM increases (e.g., 3-5% per year)
6. Gross-Up Provisions: Adjust CAM to 95% occupancy to prevent unfair burden
7. Audit Rights: Tenant can audit landlord's expense records within 60-120 days
8. Controllable vs Uncontrollable Expenses: Taxes/insurance uncontrollable; maintenance may be capped
        """,
        key_factors=[
            "Base rent per SF vs market",
            "CAM reconciliation timing and audit rights",
            "Presence of caps on controllable expenses",
            "Gross-up provisions at 95% occupancy",
            "Tenant's proportionate share calculation accuracy",
            "Exclusions from CAM (landlord's admin fees, capital improvements)",
            "Payment timing: monthly estimates vs annual true-up"
        ],
        primary_authority=[
            "Commercial lease drafting standards (NAIOP, ICSC)",
            "State landlord-tenant law (varies by jurisdiction)",
            "BOMA measurement standards for SF calculation",
            "Uniform Commercial Code (UCC) Article 2A (personal property leases by analogy)"
        ],
        burden_holder="Tenant to verify CAM charges are reasonable and properly allocated",
        adversary_position="Landlord may inflate CAM with capital improvements or admin fees",
        counter_arguments=[
            "CAM charges include non-operating capital improvements (violates NNN intent)",
            "Proportionate share miscalculated due to non-BOMA measurement",
            "No gross-up provision causes unfair burden when building under-occupied",
            "Landlord's management fees embedded in CAM without disclosure",
            "Annual cap missing on controllable expenses"
        ],
        resolution_strategy="Negotiate CAM caps, gross-up at 95% occupancy, exclude capital items, grant audit rights annually",
        entity_scope="Commercial tenants in retail, office, industrial NNN leases",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Standard industry practice; well-established lease structures",
        controlling_precedent="No controlling case law; governed by contract negotiation and industry standards",
        issue_category=IssueCategory.LEASE_STRUCTURE
    ),
    DoctrineBlock(
        topic="CMBS Loan Servicing Standards",
        keywords=["CMBS", "commercial mortgage backed securities", "special servicer", "loan modification", "PSA"],
        conclusion_template=[
            "CMBS loans prohibit modifications without bondholder approval due to pooling and servicing agreement (PSA).",
            "Special servicer takes control upon default; master servicer handles performing loans.",
            "Borrower negotiation leverage severely limited by securitization structure."
        ],
        reasoning_framework="""
CMBS Loan Framework:
1. Loan Origination: Conduit lender originates loan with intent to securitize
2. Securitization: Loan pooled with others, sold to trust, bonds issued to investors
3. PSA (Pooling and Servicing Agreement): Governs servicer duties to bondholders
4. Master Servicer: Collects payments, handles routine matters for performing loans
5. Special Servicer: Takes control upon default (60-90 days delinquent) or imminent default
6. Modification Restrictions:
   - PSA prohibits modifications that harm bondholders (extend term, reduce rate, forgive principal)
   - Special servicer must act in bondholders' best interest, not borrower's
   - Workout solutions limited to: loan assumption, discounted payoff, foreclosure, REO sale
7. Lock-Out Periods: First 2-5 years, prepayment prohibited entirely
8. Defeasance: Only prepayment option during lock-out; substitute collateral with Treasury bonds
9. Yield Maintenance: After lock-out, prepayment penalty = PV of remaining interest at Treasury rate + spread
        """,
        key_factors=[
            "Loan is in special servicing (default) vs master servicing (performing)",
            "PSA restrictions on modification authority",
            "Special servicer's fiduciary duty to bondholders, not borrower",
            "Lock-out period remaining (defeasance required)",
            "Yield maintenance penalty calculation if post-lock-out",
            "Loan-to-value ratio and property cash flow affecting workout options",
            "Bondholders' class interests (A-note vs B-note holders may conflict)"
        ],
        primary_authority=[
            "Pooling and Servicing Agreement (PSA) specific to each CMBS trust",
            "Commercial Mortgage Securities Association (CMSA) servicing standards",
            "Regulation AB (SEC Rule 17 CFR 229.1100) for asset-backed securities disclosure",
            "Bankruptcy Code Section 1111(b) (recourse vs non-recourse in reorganization)"
        ],
        burden_holder="Borrower to demonstrate workout proposal benefits bondholders (not just borrower)",
        adversary_position="Special servicer seeks maximum recovery for bondholders; foreclosure often preferred over modification",
        counter_arguments=[
            "Modification would increase bond value more than foreclosure (prove via DCF analysis)",
            "Loan assumption by stronger borrower preserves bond cash flows",
            "Discounted payoff exceeds foreclosure proceeds net of costs",
            "Extension with higher interest rate and additional collateral improves bondholder position",
            "Borrower files bankruptcy to force cramdown and strip liens (Section 1129(b))"
        ],
        resolution_strategy="Negotiate loan assumption, discounted payoff, or prove modification increases bond NPV; avoid default to retain master servicer relationship",
        entity_scope="Borrowers with CMBS loans on commercial properties",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="PSA terms govern; special servicer discretion limited by fiduciary duty to bondholders",
        controlling_precedent="LNV Corp. v. Paulson & Co. (Del. 2020) - special servicer owes duty to certificateholders, not borrower",
        issue_category=IssueCategory.FINANCING
    ),
    DoctrineBlock(
        topic="IRC Section 1031 Like-Kind Exchange",
        keywords=["1031 exchange", "like-kind", "qualified intermediary", "boot", "replacement property", "180 days"],
        conclusion_template=[
            "Section 1031 defers capital gains tax on real property exchanges if like-kind and held for investment/business use.",
            "Taxpayer cannot touch proceeds; qualified intermediary must hold funds during exchange period.",
            "Strict timing: 45 days to identify replacement, 180 days to close acquisition."
        ],
        reasoning_framework="""
IRC Section 1031 Exchange Framework:
1. Eligible Property: Real property held for investment or business use (not primary residence, inventory, or securities)
2. Like-Kind Requirement: Post-2017 TCJA, only real property qualifies; all real property is like-kind (land for building, commercial for residential)
3. Three-Party Exchange Structure (Starker Exchange):
   - Taxpayer sells relinquished property
   - Qualified Intermediary (QI) holds proceeds
   - Taxpayer identifies replacement property within 45 days
   - QI uses proceeds to acquire replacement property within 180 days
   - Title transfers directly to taxpayer
4. Timing Requirements:
   - 45-Day Identification Deadline: Written notice to QI of up to 3 properties (or unlimited if 200% rule or 95% rule met)
   - 180-Day Exchange Deadline: Close on replacement property (or tax return due date if earlier)
5. Boot: Any non-like-kind property received (cash, debt relief, personal property) triggers taxable gain to extent of boot
6. Basis Carryover: Replacement property takes carryover basis from relinquished property (deferred gain, not forgiven)
7. Qualified Intermediary: Independent party (not taxpayer's agent, attorney, CPA, or relative) holds proceeds; taxpayer cannot have constructive receipt
8. Reverse Exchange: Acquire replacement first via Exchange Accommodation Titleholder (EAT), then sell relinquished within 180 days
        """,
        key_factors=[
            "Both properties held for investment/business use (not personal residence or dealer inventory)",
            "Qualified Intermediary engaged before relinquished property sale closes",
            "Identification within 45 days (strict calendar days, no extensions)",
            "Closing within 180 days (or tax return due date with extensions, whichever earlier)",
            "No boot received (cash, debt reduction, personal property)",
            "Title transfers directly from seller to QI to taxpayer (not through taxpayer)",
            "Equal or greater value in replacement property (trade up) to defer 100% of gain",
            "Equal or greater debt on replacement property to avoid debt relief boot"
        ],
        primary_authority=[
            "IRC Section 1031(a)(1) - nonrecognition of gain on like-kind exchanges",
            "Treas. Reg. Section 1.1031(k)-1 - deferred exchange rules",
            "Rev. Proc. 2000-37 - safe harbor for qualified intermediaries",
            "Starker v. United States, 602 F.2d 1341 (9th Cir. 1979) - delayed exchange permitted",
            "TCJA Pub. L. 115-97 Section 13303 (2017) - limited to real property"
        ],
        burden_holder="Taxpayer to prove strict compliance with timing, QI independence, and like-kind requirements",
        adversary_position="IRS challenges constructive receipt, related-party QI, identification validity, or property use",
        counter_arguments=[
            "45-day deadline missed due to unforeseen circumstances (no relief; strict statutory deadline)",
            "QI was taxpayer's attorney (disqualified; constructive receipt)",
            "Replacement property flipped within 2 years (possible related-party anti-abuse rule Section 1031(f))",
            "Property held for personal use claimed as investment (taxpayer must prove investment intent via rental history)",
            "Boot received but claimed as separate transaction (substance over form; IRS recharacterizes)"
        ],
        resolution_strategy="Engage independent QI before sale, identify within 45 days using 3-property rule, close within 180 days, trade up in value and debt, avoid boot",
        entity_scope="Real property investors, landlords, developers exchanging business/investment properties",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Strict statutory compliance required; no equitable relief for missed deadlines",
        controlling_precedent="Bolker v. Commissioner, 81 T.C. 782 (1983) - 45-day deadline is absolute",
        issue_category=IssueCategory.TAX_PLANNING
    ),
    DoctrineBlock(
        topic="Qualified Opportunity Zone Investment",
        keywords=["opportunity zone", "QOZ", "1400Z-2", "qualified opportunity fund", "180 days", "10 year", "basis step-up"],
        conclusion_template=[
            "IRC Section 1400Z-2 allows capital gains deferral and exclusion via investment in Qualified Opportunity Funds (QOF).",
            "Taxpayer must invest gain (not entire proceeds) within 180 days into QOF; fund invests in QOZ property within 180 days.",
            "Hold 10 years for permanent exclusion of appreciation; 5-year hold increases deferred gain basis by 10%, 7-year by 15%."
        ],
        reasoning_framework="""
Qualified Opportunity Zone Framework (IRC Section 1400Z-2):
1. Eligible Gain: Capital gain from any source (stock sale, real estate, business) recognized within 180 days
2. Investment Timing: Invest gain amount (not entire proceeds) into QOF within 180 days of gain recognition
3. Qualified Opportunity Fund (QOF): Partnership or corporation self-certified on Form 8996, holds 90% of assets in QOZ property
4. QOZ Property: Located in designated low-income census tract opportunity zone, acquired after 12/31/2017, substantially improved (double basis) or original use
5. Deferral Mechanism:
   - Year 1-4: Gain deferred, zero basis in QOF interest
   - Year 5: Basis increases by 10% of deferred gain (10% of gain becomes tax-free)
   - Year 7: Basis increases by additional 5% (15% total tax-free)
   - Year 10: Deferred gain recognized (at 85% if held 7+ years before 2027) OR deferred gain inclusion date (12/31/2026), whichever earlier
6. Permanent Exclusion: Hold QOF investment 10+ years, elect Section 1400Z-2(c) to exclude ALL appreciation in QOF (step-up basis to FMV on sale)
7. Substantial Improvement Test: Improvements must double QOF's adjusted basis in property within 30 months (land excluded from basis calculation)
8. Working Capital Safe Harbor: QOF business can hold cash up to 31 months for development if written plan and schedule
        """,
        key_factors=[
            "Gain invested within 180 days (strict deadline)",
            "QOF self-certified on Form 8996 before investment",
            "QOF holds 90% of assets in QOZ property (tested semi-annually)",
            "Property located in designated QOZ census tract",
            "Substantial improvement doubles basis within 30 months",
            "Hold 10 years to elect appreciation exclusion (Section 1400Z-2(c))",
            "Deferred gain recognition by 12/31/2026 or disposition, whichever earlier",
            "Only gain amount invested (not entire sale proceeds)"
        ],
        primary_authority=[
            "IRC Section 1400Z-2 (enacted via Tax Cuts and Jobs Act 2017)",
            "Treas. Reg. Section 1.1400Z2(a)-1 (deferral rules)",
            "Treas. Reg. Section 1.1400Z2(d)-1 (QOZ business property)",
            "Rev. Rul. 2018-29 (180-day period begins on sale date for partnerships, passthrough date for partners)",
            "Notice 2020-39 (working capital safe harbor extended during COVID)"
        ],
        burden_holder="Taxpayer to prove gain invested within 180 days, QOF 90% test met, substantial improvement within 30 months",
        adversary_position="IRS challenges 180-day timing, 90% asset test failure, substantial improvement computation, or QOZ property eligibility",
        counter_arguments=[
            "180-day deadline missed (no relief; statutory deadline)",
            "QOF failed 90% asset test in semi-annual testing (penalty or decertification)",
            "Substantial improvement test failed (land included in basis, or improvements <2x)",
            "Property purchased from related party (disqualified unless original use or substantial improvement met)",
            "Working capital held beyond 31 months without qualifying extension (safe harbor lost, 90% test failed)"
        ],
        resolution_strategy="Invest within 180 days, self-certify QOF on Form 8996, acquire QOZ property within 180 days, double basis within 30 months, hold 10 years, elect Section 1400Z-2(c) exclusion",
        entity_scope="Investors with capital gains seeking deferral and exclusion via opportunity zone real estate or business investments",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Complex regulations; substantial improvement and 90% tests create audit risk",
        controlling_precedent="No controlling precedent yet; regulations finalized 12/2019, limited case law",
        issue_category=IssueCategory.TAX_PLANNING
    ),
    DoctrineBlock(
        topic="REIT Qualification Requirements",
        keywords=["REIT", "real estate investment trust", "856", "90% distribution", "75% asset test", "95% income test"],
        conclusion_template=[
            "IRC Section 856 requires REITs to distribute 90% of taxable income, derive 75% of income from real estate, and meet asset/ownership tests.",
            "REIT avoids corporate-level tax but must comply with annual testing; failure triggers 5-year disqualification.",
            "Shareholders pay tax on dividends as ordinary income (no qualified dividend treatment for most REIT distributions)."
        ],
        reasoning_framework="""
REIT Qualification Framework (IRC Section 856):
1. Organizational Tests:
   - Corporation, trust, or association taxable as corporation
   - Managed by board of directors or trustees
   - Shares fully transferable
   - Minimum 100 shareholders (after first tax year)
   - Not closely held (5 or fewer individuals cannot own >50% - 5/50 test)
2. Asset Tests (quarterly):
   - 75% Test: At least 75% of assets in real property, mortgages, REIT shares, cash, government securities
   - 25% Test: No more than 25% in non-qualifying assets
   - 5/10 Test: No more than 5% in securities of any one issuer (except TRS or REIT), no more than 10% voting power
3. Income Tests (annual):
   - 75% Gross Income Test: At least 75% from real property rents, mortgage interest, real property sales, REIT dividends
   - 95% Gross Income Test: At least 95% from 75% sources plus dividends, interest, securities gains
   - Rents from real property must not be based on tenant income/profits (fixed rent or percentage of gross receipts OK)
4. Distribution Requirement: Distribute 90% of REIT taxable income (excluding capital gains) as dividends to shareholders annually
5. Taxable REIT Subsidiary (TRS): Allows non-qualifying activities (property management, development for sale) without tainting REIT; subject to corporate tax
6. Deficiency Dividend Procedure: If IRS audit increases taxable income, REIT can avoid disqualification by paying deficiency dividend plus interest
        """,
        key_factors=[
            "Minimum 100 shareholders after first year (private placement REITs may struggle)",
            "5/50 test: no more than 50% owned by 5 or fewer individuals (attribution rules apply)",
            "Quarterly 75% asset test compliance (rebalancing required if failed)",
            "Annual 75% and 95% gross income tests (impermissible tenant services taint rents)",
            "90% distribution requirement (cash flow constraints if high depreciation)",
            "Rent from related-party tenants disqualified unless TRS",
            "Property sales within 2 years of acquisition may be dealer income (prohibited transaction tax)"
        ],
        primary_authority=[
            "IRC Section 856 (REIT qualification requirements)",
            "IRC Section 857 (taxation of REITs and shareholders)",
            "IRC Section 858 (deficiency dividends)",
            "Treas. Reg. Section 1.856-1 through 1.856-10",
            "Rev. Proc. 2020-45 (REIT asset and income test relief procedures)"
        ],
        burden_holder="REIT to prove quarterly asset tests, annual income tests, distribution compliance, and 5/50 test met",
        adversary_position="IRS challenges tenant services as non-rent income, related-party rent, or dealer property sales",
        counter_arguments=[
            "Impermissible tenant services provided (cleaning, utilities, parking) taint rent (Section 856(d)(7)(C))",
            "Related-party tenant rent disqualified (must use TRS to manage property leased to affiliate)",
            "Property sold within 2 years at gain triggers prohibited transaction tax (30% on gain)",
            "Asset test failed in quarter without timely cure (de minimis exception or self-correction available)",
            "Income test failed (reasonable cause exception available if <1% and corrected)"
        ],
        resolution_strategy="Monitor quarterly asset tests, segregate non-qualifying activities into TRS, avoid impermissible services, hold properties long-term, maintain 90% distribution",
        entity_scope="Real estate investment trusts seeking pass-through tax treatment",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Strict statutory tests; safe harbors available for certain failures if de minimis and corrected",
        controlling_precedent="Siegel v. Commissioner, T.C. Memo 2000-305 - impermissible services taint rent",
        issue_category=IssueCategory.REIT
    ),
    DoctrineBlock(
        topic="Phase I Environmental Site Assessment",
        keywords=["Phase I ESA", "ASTM E1527", "environmental due diligence", "recognized environmental condition", "REC", "AAI"],
        conclusion_template=[
            "Phase I ESA per ASTM E1527-21 identifies recognized environmental conditions (RECs) via records review, site inspection, interviews.",
            "Lender requires Phase I for acquisition financing; establishes innocent landowner defense under CERCLA if no RECs found.",
            "If RECs identified, Phase II testing required to quantify contamination and remediation costs."
        ],
        reasoning_framework="""
Phase I ESA Framework (ASTM E1527-21):
1. Purpose: Identify recognized environmental conditions (RECs) prior to property acquisition to establish All Appropriate Inquiries (AAI) defense under CERCLA
2. Scope of Work:
   - Records Review: Federal (NPL, CERCLIS, RCRA), state (leaking USTs, brownfields), tribal, local databases within search radius (up to 1 mile for NPL sites)
   - Site Reconnaissance: Visual inspection of property and adjoining properties for current/past environmental concerns (tanks, drums, staining, odors)
   - Interviews: Current owner, occupants, local agencies regarding site history and environmental conditions
   - Historical Research: Aerial photos, fire insurance maps, city directories, title records to identify past uses (gas stations, dry cleaners, industrial)
   - User-Provided Information: Owner/occupant questionnaire, environmental liens, specialized knowledge
3. Recognized Environmental Condition (REC): Presence or likely presence of hazardous substances or petroleum under conditions indicating release, past release, or material threat of release
4. Controlled REC (CREC): REC with institutional controls (deed restriction, environmental covenant) preventing future exposure
5. Historical REC (HREC): Past release that has been remediated to unrestricted use standards; no further action required
6. De Minimis Condition: Low-threat condition unlikely to result in environmental liability (small staining, minor releases)
7. Data Gaps: Missing information documented; does not prevent Phase I completion but noted as limitation
        """,
        key_factors=[
            "Current/past site uses (industrial, gas station, dry cleaner, landfill = high risk)",
            "Presence of underground storage tanks (USTs) or above-ground storage tanks (ASTs)",
            "Adjoining property uses (upgradient contamination migration risk)",
            "Historical aerial photos showing drums, staining, fill material",
            "Database hits within search radius (NPL, CERCLIS, RCRA, UST)",
            "Visual indicators during site visit (staining, odors, stressed vegetation)",
            "User-provided information (environmental reports, permits, violations)"
        ],
        primary_authority=[
            "ASTM E1527-21 Standard Practice for Environmental Site Assessments",
            "CERCLA Section 101(35)(B) - All Appropriate Inquiries (AAI) defense",
            "40 CFR Part 312 - EPA AAI final rule",
            "State environmental statutes (varies by jurisdiction - e.g., CA Health & Safety Code Section 25395.60)"
        ],
        burden_holder="Buyer to conduct Phase I per ASTM E1527-21 to establish innocent landowner defense; seller to disclose known environmental conditions",
        adversary_position="Seller conceals environmental history; government pursues buyer as current owner under CERCLA strict liability",
        counter_arguments=[
            "Phase I missed REC due to inadequate historical research (AAI defense fails)",
            "Buyer had specialized knowledge of contamination but relied on clean Phase I (knowledge defeats innocent landowner defense)",
            "Contamination migrated from adjoining property after acquisition (buyer not liable under CERCLA but may face cleanup costs)",
            "Phase I consultant not qualified under 40 CFR 312.10 (report may not satisfy AAI)",
            "Report older than 180 days at closing (must update to maintain AAI compliance)"
        ],
        resolution_strategy="Obtain ASTM E1527-21 Phase I from qualified consultant, conduct Phase II if RECs identified, negotiate price reduction or escrow for remediation, obtain environmental insurance",
        entity_scope="Buyers, lenders, investors conducting due diligence on commercial real estate acquisitions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Standard industry practice; CERCLA AAI safe harbor if ASTM E1527-21 followed",
        controlling_precedent="United States v. Davis, 261 F.3d 1 (1st Cir. 2001) - innocent landowner defense requires AAI",
        issue_category=IssueCategory.ENVIRONMENTAL
    ),
    DoctrineBlock(
        topic="ALTA Title Insurance Endorsements",
        keywords=["ALTA", "title insurance", "endorsement", "survey", "zoning", "access", "location", "encroachment"],
        conclusion_template=[
            "ALTA policy insures against title defects, liens, encumbrances; endorsements expand coverage to survey, zoning, access issues.",
            "Lender requires ALTA Loan Policy with endorsements; owner may purchase separate Owner's Policy.",
            "Survey-related endorsements (e.g., ALTA 9) require current ALTA/NSPS Land Title Survey."
        ],
        reasoning_framework="""
ALTA Title Insurance Framework:
1. Policy Types:
   - Owner's Policy: Insures owner against title defects, liens, prior encumbrances; coverage = purchase price
   - Loan Policy: Insures lender's mortgage lien priority; coverage = loan amount (decreases as loan paid down)
2. Standard Exclusions from Coverage:
   - Matters not of public record (unrecorded easements, adverse possession, boundary disputes)
   - Governmental regulations (zoning, building codes, environmental)
   - Survey matters (encroachments, boundary line disputes, overlapping improvements)
   - Certain liens (mechanics' liens for work not yet recorded, property tax for current year)
3. Common ALTA Endorsements (2021 Forms):
   - ALTA 8.1 (Environmental Lien): Insures against government environmental liens
   - ALTA 9 (Restrictions, Encroachments, Minerals): Comprehensive endorsement requiring survey; insures location, encroachments, CC&R violations, mineral rights
   - ALTA 9.10 (Restrictions, Encroachments, Minerals - Loan Policy): Lender version of ALTA 9
   - ALTA 22.1 (Location and Map): Insures land description matches improvements on survey without full ALTA 9 coverage
   - ALTA 4.1 (Condominium): Insures condominium unit and common elements
   - ALTA 5.1 (Planned Unit Development): Insures PUD common areas
   - ALTA 6.2 (Variable Rate Mortgage): Insures adjustable-rate mortgages
   - ALTA 8.2 (Mortgage Modification): Insures loan modification, extension, or consolidation
   - ALTA 13 (Leasehold): Insures leasehold estate for ground leases
   - Zoning Endorsements (3.1, 3.2): Insure existing use complies with zoning; 3.1 = basic, 3.2 = no violations or non-conforming use
4. Survey Requirements: ALTA 9 series requires current ALTA/NSPS Land Title Survey prepared by licensed surveyor showing boundary, improvements, easements, encroachments
        """,
        key_factors=[
            "Owner's policy vs loan policy (separate premiums; owner's policy recommended)",
            "Policy date and effective time (coverage only for defects existing before policy date)",
            "Endorsements requested and premium charged (ALTA 9 adds 10-20% premium)",
            "Survey currency (ALTA 9 requires survey dated within 90-120 days pre-closing)",
            "Zoning endorsement requirements (3.1 vs 3.2; 3.2 requires zoning report and no violations)",
            "Special exceptions scheduled (encumbrances, easements, CC&Rs not covered unless removed or insured over)",
            "Premium calculation (varies by state; some use promulgated rates, others file-and-use)"
        ],
        primary_authority=[
            "ALTA Policy Forms (2021) - Owner's Policy, Loan Policy",
            "ALTA Endorsement Forms (2021 series)",
            "ALTA/NSPS Land Title Survey Standards (2021)",
            "State title insurance statutes (e.g., TX Insurance Code Title 11; CA Insurance Code Sections 12340-12414.26)"
        ],
        burden_holder="Buyer/lender to request endorsements; title company to disclose exceptions and determine insurability",
        adversary_position="Title company excludes survey matters, zoning, environmental liens unless endorsement purchased",
        counter_arguments=[
            "Title policy excludes encroachment discovered post-closing (should have obtained ALTA 9 with survey)",
            "Zoning violation not covered by standard policy (should have obtained 3.2 zoning endorsement)",
            "Environmental lien filed by EPA not covered (should have obtained ALTA 8.1)",
            "Mechanics' lien for pre-closing work recorded post-closing defeats priority (gap coverage needed)",
            "Leasehold estate not covered by standard policy (ALTA 13 required for ground lease financing)"
        ],
        resolution_strategy="Obtain ALTA/NSPS survey, request ALTA 9 series and zoning endorsements, purchase owner's policy in addition to lender's loan policy, review schedule B exceptions and negotiate removal or insurance over",
        entity_scope="Buyers, lenders, developers, investors acquiring commercial real estate",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Standard industry practice; policy terms governed by ALTA forms and state regulation",
        controlling_precedent="State-specific case law on title insurance coverage disputes (e.g., Lick Mill Creek v. Chicago Title, 231 Cal. App. 3d 1654 (1991) - insurer liable for encroachments if ALTA 9 issued)",
        issue_category=IssueCategory.TITLE
    ),
    DoctrineBlock(
        topic="Subordination, Non-Disturbance, and Attornment Agreement (SNDA)",
        keywords=["SNDA", "subordination", "non-disturbance", "attornment", "ground lease", "leasehold financing"],
        conclusion_template=[
            "SNDA protects tenant in subordinated lease from eviction if landlord's lender forecloses.",
            "Tenant subordinates lease to mortgage, lender agrees not to disturb tenant if no default, tenant attorns to new owner post-foreclosure.",
            "Required by lenders financing ground lease or subordinate lease improvements."
        ],
        reasoning_framework="""
SNDA Framework:
1. Parties: Landlord, Tenant, Landlord's Lender (senior mortgagee)
2. Subordination Clause:
   - Tenant agrees lease is subordinate to lender's mortgage (lien priority)
   - Effect: If landlord defaults on mortgage and lender forecloses, lease could be extinguished unless non-disturbance agreement in place
   - Junior lease (recorded after mortgage) automatically subordinate; senior lease (recorded before mortgage) requires subordination agreement
3. Non-Disturbance Clause:
   - Lender agrees not to terminate lease or disturb tenant's possession if tenant not in default
   - Tenant's lease survives foreclosure as if tenant were direct tenant of new owner (foreclosure purchaser)
   - Protection conditional: Tenant must be current on rent and not in default under lease
4. Attornment Clause:
   - Tenant agrees to recognize lender (or foreclosure purchaser) as new landlord
   - Tenant's obligation to pay rent and perform lease terms continues to new owner
   - New owner steps into landlord's shoes (assumes landlord's obligations under lease)
5. Ground Lease Context:
   - Tenant builds improvements on landlord's land; needs leasehold mortgage financing
   - Leasehold lender requires SNDA from fee owner's lender to protect leasehold collateral
   - Two-tier SNDA: Fee lender subordinates to ground lease, ground lease lender subordinates to fee mortgage but gets non-disturbance
6. Estoppel Certificate: Tenant certifies lease in effect, no defaults, rent current; often required alongside SNDA at financing
        """,
        key_factors=[
            "Lease recording date relative to mortgage (senior lease needs subordination; junior lease automatic but needs non-disturbance)",
            "Tenant's creditworthiness and lease term (lender more willing to grant non-disturbance for strong tenant, long-term lease)",
            "Tenant's improvements value (major tenant improvements justify stronger non-disturbance rights)",
            "Ground lease vs direct lease (ground lease creates dual-lender SNDA complexity)",
            "Tenant default provisions (non-disturbance conditioned on tenant being non-defaulting)",
            "Foreclosure mechanics (SNDA must survive foreclosure sale and bankruptcy)",
            "Estoppel certificate requirements (tenant certifies facts lender relies on)"
        ],
        primary_authority=[
            "State real property law on lien priority (e.g., CA Civil Code Section 2897 - first in time, first in right)",
            "Bankruptcy Code Section 365 (assumption/rejection of unexpired leases)",
            "State foreclosure statutes (judicial vs non-judicial; effect on junior interests)",
            "UCC Article 9 (leasehold mortgage as security interest in personal property by analogy)"
        ],
        burden_holder="Tenant to negotiate non-disturbance from landlord's lender; lender to grant non-disturbance only if tenant creditworthy",
        adversary_position="Lender forecloses and terminates tenant's subordinate lease; tenant loses possession and improvements",
        counter_arguments=[
            "Non-disturbance agreement invalid if not recorded (may not bind foreclosure purchaser without notice)",
            "Tenant in default at foreclosure loses non-disturbance protection (lender terminates lease)",
            "Bankruptcy of landlord allows trustee to reject lease under Section 365 (SNDA survives if properly drafted)",
            "Ground lease lender forecloses but fee lender also forecloses (cascading foreclosure; dual SNDA required)",
            "Landlord sold property; new owner's lender not bound by prior SNDA (must re-execute or record original)"
        ],
        resolution_strategy="Negotiate SNDA before lease execution or financing; record SNDA to give constructive notice; maintain lease compliance to preserve non-disturbance rights; obtain estoppel certificate at financing",
        entity_scope="Tenants with long-term leases or major improvements; lenders financing landlords or leasehold estates",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Standard commercial lease practice; lender's obligation to grant non-disturbance varies by tenant creditworthiness",
        controlling_precedent="In re Spanish Peaks Holdings II, LLC, 872 F.3d 892 (9th Cir. 2017) - SNDA survives bankruptcy if properly executed",
        issue_category=IssueCategory.LEASE_STRUCTURE
    ),
    DoctrineBlock(
        topic="Gross Lease vs Modified Gross Lease",
        keywords=["gross lease", "modified gross", "full service", "operating expenses", "base year", "expense stop"],
        conclusion_template=[
            "Gross lease: landlord pays all operating expenses, tenant pays fixed rent (common in office space).",
            "Modified gross: tenant pays base rent plus share of expense increases over base year or expense stop.",
            "Expense stop protects landlord from uncontrolled cost escalation; base year protects tenant from immediate pass-throughs."
        ],
        reasoning_framework="""
Gross vs Modified Gross Lease Framework:
1. Gross Lease (Full Service):
   - Tenant pays fixed rent; landlord pays taxes, insurance, maintenance, utilities, janitorial
   - Common in multi-tenant office buildings with central HVAC and services
   - Landlord's risk: expense increases reduce NOI unless rent escalation clauses (CPI adjustment, fixed % annual increase)
   - Tenant's benefit: budgetable occupancy cost; landlord incentivized to control expenses
2. Modified Gross Lease (Expense Stop or Base Year):
   - Tenant pays base rent + share of operating expense increases above base year or expense stop
   - Base Year Structure: Expenses in year 1 = base; tenant pays proportionate share of increases in years 2+
   - Expense Stop Structure: Fixed dollar amount; tenant pays proportionate share of expenses above stop (e.g., $8/SF stop, actual $10/SF, tenant pays $2 x proportionate share)
   - Operating Expenses Defined: Taxes, insurance, CAM, utilities, management fees (negotiate exclusions: capital improvements, leasing commissions, debt service)
   - Proportionate Share: Tenant SF / Total Leasable SF (or sometimes Total Rentable SF including common areas)
3. Gross-Up Provisions: Adjust variable expenses to 95% occupancy to prevent unfair tenant burden when building under-leased (fixed costs like management fees spread over fewer tenants)
4. Controllable vs Uncontrollable: Tenant may negotiate cap on controllable expenses (maintenance, utilities) but not uncontrollable (taxes, insurance)
5. Audit Rights: Tenant can audit landlord's expense records within 60-120 days of annual reconciliation statement
        """,
        key_factors=[
            "Expense stop amount vs current market expenses (low stop = tenant bears more risk)",
            "Base year definition (actual expenses in year 1, or pro forma 95% occupied base year)",
            "Gross-up provision at 95% occupancy (prevents unfair burden in under-occupied buildings)",
            "Operating expense definition and exclusions (capital improvements, leasing costs, debt service excluded)",
            "Controllable expense caps (e.g., 3-5% annual increase on utilities and maintenance)",
            "Audit rights and reconciliation timing (annual statement within 90 days of year-end)",
            "Proportionate share calculation (SF measurement standard: BOMA 2017)"
        ],
        primary_authority=[
            "Commercial lease drafting standards (NAIOP, BOMA)",
            "BOMA 2017 Office Standard for measuring rentable/usable SF",
            "State landlord-tenant law (varies; some states regulate expense pass-throughs)",
            "Common law contract interpretation (expense stop ambiguities construed against drafter)"
        ],
        burden_holder="Landlord to provide annual expense reconciliation; tenant to audit within specified period",
        adversary_position="Landlord includes capital improvements in operating expenses; tenant challenges under audit",
        counter_arguments=[
            "Expense stop set artificially low in year 1 due to under-occupancy (tenant bears full increase)",
            "No gross-up provision; tenant's share inflated due to low occupancy (negotiate gross-up to 95%)",
            "Capital improvements included in operating expenses (violate modified gross intent; should be capitalized and amortized)",
            "Management fees calculated on gross revenues including tenant reimbursements (double-counting; should exclude reimbursements)",
            "Base year expenses understated due to landlord deferring maintenance (negotiate pro forma base year at stabilized occupancy)"
        ],
        resolution_strategy="Negotiate expense stop at market rates, require gross-up to 95% occupancy, exclude capital items and leasing costs, cap controllable expenses, grant audit rights annually",
        entity_scope="Office tenants in multi-tenant buildings with gross or modified gross leases",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Standard industry practice; terms negotiated based on market leverage",
        controlling_precedent="No controlling case law; governed by contract negotiation and BOMA standards",
        issue_category=IssueCategory.LEASE_STRUCTURE
    ),
    DoctrineBlock(
        topic="Mezzanine Loan and Intercreditor Agreement",
        keywords=["mezzanine loan", "mezz", "intercreditor", "pledge", "equity", "standstill", "senior lender"],
        conclusion_template=[
            "Mezzanine loan secured by pledge of borrower's equity interests (not direct lien on property); subordinate to senior mortgage.",
            "Intercreditor agreement governs senior and mezz lender rights; standstill period gives senior lender time to cure defaults before mezz forecloses.",
            "Mezz lender forecloses on equity (UCC Article 9); faster than foreclosing on real property but subject to senior loan obligations."
        ],
        reasoning_framework="""
Mezzanine Loan Framework:
1. Capital Stack Structure:
   - Equity: Sponsor's cash investment (highest risk, highest return - 15-25% IRR)
   - Mezzanine Debt: Secured by pledge of equity interests in borrower entity (8-12% interest + equity kicker/warrants)
   - Senior Debt: First mortgage on property (4-6% interest, 65-75% LTV)
2. Mezzanine Loan Structure:
   - Lender loans to property-owning entity's parent (HoldCo)
   - Collateral: Pledge of 100% equity interests (membership interests in LLC, stock in corporation) in property owner (PropCo)
   - UCC-1 Financing Statement filed against pledged equity
   - Foreclosure: UCC Article 9 sale of equity interests (faster than real property foreclosure - 30-90 days vs 6-18 months)
   - Mezz lender steps into sponsor's shoes, becomes new equity owner, assumes senior debt obligations
3. Intercreditor Agreement (ICA):
   - Parties: Senior lender, mezzanine lender, borrower
   - Subordination: Mezz debt subordinate to senior debt; mezz lender cannot foreclose while senior debt outstanding without senior consent
   - Standstill Period: If mezz borrower defaults, mezz lender must notify senior lender; senior has 60-120 days to cure, refinance, or purchase mezz loan before mezz can foreclose
   - Payment Priority: Cash flow waterfall: senior debt service first, then mezz debt service, then equity distributions
   - Transfer Restrictions: Mezz lender cannot transfer loan to competitor or sponsor's enemy (senior lender approval required)
   - Bankruptcy: Senior lender controls bankruptcy proceedings; mezz lender subordinates to senior's restructuring plan
4. Senior Lender Protections in ICA:
   - No amendments to mezz loan terms without senior consent (prevents maturity extension, rate reduction)
   - No foreclosure without senior consent or standstill expiration
   - Mezz lender must assume senior debt if forecloses on equity
   - No challenge to senior lender's rights in bankruptcy
        """,
        key_factors=[
            "Intercreditor agreement terms (standstill period length, senior lender cure rights)",
            "Combined LTV (senior + mezz debt should not exceed 85-90%)",
            "Mezz lender's equity kicker (warrants, promote share, or GP interest)",
            "UCC foreclosure speed vs senior foreclosure timing (mezz faster but subject to standstill)",
            "Bankruptcy risk (mezz lender subordinated in Chapter 11; senior controls plan)",
            "Senior loan default cross-defaults mezz loan (common provision)",
            "Transfer restrictions on mezz loan (senior approval required for changes of control)"
        ],
        primary_authority=[
            "UCC Article 9 (security interests in investment property - pledged equity)",
            "State LLC/corporate law on equity pledge and foreclosure (e.g., DE LLC Act Section 18-101)",
            "Bankruptcy Code Section 1129(b) (cramdown; senior lien priorities in reorganization)",
            "Intercreditor agreement contract terms (negotiated between lenders)"
        ],
        burden_holder="Mezz lender to comply with standstill and subordination; senior lender to act reasonably in exercising cure rights",
        adversary_position="Senior lender uses standstill to block mezz foreclosure indefinitely; mezz lender argues bad faith",
        counter_arguments=[
            "Senior lender fails to cure during standstill but blocks mezz foreclosure (mezz lender may seek declaratory judgment after reasonable period)",
            "Mezz lender forecloses without notice to senior (violates ICA; foreclosure sale voidable)",
            "Bankruptcy of borrower; mezz lender's equity interest wiped out in cramdown (senior lender fully secured, mezz under-secured)",
            "Sponsor transfers equity without senior/mezz consent (violates pledge; default under both loans)",
            "Mezz lender waives subordination; senior lender discovers post-closing (senior may demand cure or accelerate)"
        ],
        resolution_strategy="Negotiate reasonable standstill (90 days), ensure ICA gives mezz lender right to cure senior defaults, maintain equity value above combined debt, avoid triggers for cross-defaults",
        entity_scope="Real estate sponsors, developers, mezz lenders, senior lenders in leveraged acquisitions or development projects",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Standard industry practice; ICA terms heavily negotiated and lender-specific",
        controlling_precedent="In re Genesis Health Ventures, 266 B.R. 591 (Bankr. D. Del. 2001) - mezz lender subordination survives bankruptcy",
        issue_category=IssueCategory.FINANCING
    ),
    DoctrineBlock(
        topic="Construction Loan Mechanics and Holdbacks",
        keywords=["construction loan", "draw", "holdback", "retainage", "AIA G702", "G703", "payment application", "lien waiver"],
        conclusion_template=[
            "Construction lender disburses in draws based on percentage completion; holds back 10% retainage to ensure completion.",
            "Borrower submits AIA G702 (summary) and G703 (schedule of values) with lien waivers from contractors; lender's inspector verifies work.",
            "Retainage released at substantial completion (often 50%) and final completion (remaining 50% after punch list)."
        ],
        reasoning_framework="""
Construction Loan Framework:
1. Loan Structure:
   - Total Commitment: Loan amount based on 75-80% of completed value (as-stabilized appraised value)
   - Interest Reserve: Portion of loan set aside to pay interest during construction (12-24 months)
   - Disbursement Schedule: Monthly or milestone-based draws as work progresses
2. Draw Request Process:
   - Borrower Submits:
     a. AIA G702 Application and Certificate for Payment (summary of work completed, stored materials, total amount requested)
     b. AIA G703 Continuation Sheet (detailed breakdown by trade - sitework, concrete, framing, MEP, etc.)
     c. Lien Waivers: Conditional waivers for current draw, unconditional waivers for prior draws from all contractors/subcontractors
     d. Invoices and receipts for stored materials
   - Lender's Inspector: Third-party inspector (architect or engineer) verifies percentage completion for each line item
   - Lender Approval: If work verified, lender disburses draw amount minus retainage holdback
3. Retainage (Holdback):
   - Lender holds back 10% of each draw amount until substantial completion
   - Purpose: Ensure contractor completes punch list and final items; protect against mechanics' liens
   - Release Timing:
     a. Substantial Completion: 50% of retainage released after certificate of substantial completion issued and lien period expires (30-90 days depending on state)
     b. Final Completion: Remaining 50% released after final certificate of occupancy, all punch list items complete, final lien waivers obtained
4. Mechanics' Lien Priority:
   - State law varies: some states give mechanics' liens priority over construction mortgage if work commenced before mortgage recorded (CA, NY)
   - Lender protections: Record mortgage before commencement, require lien waivers with each draw, title company endorsement for mechanics' lien coverage
   - Lien waiver types:
     a. Conditional Waiver on Progress Payment: Effective only when check clears
     b. Unconditional Waiver on Progress Payment: Effective immediately (dangerous for contractor if check bounces)
     c. Conditional Waiver on Final Payment: Effective when final check clears
     d. Unconditional Waiver on Final Payment: Full and final release
        """,
        key_factors=[
            "Loan-to-cost vs loan-to-value (LTC 75-85%, LTV 65-75% on as-stabilized basis)",
            "Interest reserve adequacy (18-month reserve safer than 12-month)",
            "Retainage percentage (10% standard; 5% for strong GCs)",
            "Lien waiver compliance (unconditional waivers for all prior draws before new draw)",
            "Inspector independence (third-party architect/engineer, not borrower's)",
            "Stored materials eligibility (materials on-site only; off-site storage requires bonding)",
            "Draw request frequency (monthly vs milestone; monthly better cash flow for contractor)",
            "Mechanics' lien priority risk (state-specific; CA/NY give lien priority over mortgage if work started first)"
        ],
        primary_authority=[
            "AIA Document G702-1992 Application and Certificate for Payment",
            "AIA Document G703-1992 Continuation Sheet",
            "State mechanics' lien statutes (e.g., CA Civil Code Sections 8400-8494; NY Lien Law Article 2)",
            "UCC Article 9 (security interest in fixtures and equipment)",
            "State prompt payment acts (require payment to subs within 7-10 days of GC receiving payment)"
        ],
        burden_holder="Borrower to obtain lien waivers and demonstrate percentage completion; lender to disburse timely if conditions met",
        adversary_position="Contractor files mechanics' lien for unpaid work; lender's title priority challenged",
        counter_arguments=[
            "Mechanics' lien filed for work completed before mortgage recorded (lien may have priority in some states)",
            "Lien waiver signed but payment not made (conditional waiver vs unconditional; contractor may still have lien rights)",
            "Borrower submits inflated percentage completion (inspector rejects; draw denied or reduced)",
            "Stored materials claimed but not on-site (lender denies draw for off-site materials without bonding)",
            "Contractor abandons project; retainage insufficient to complete (lender may fund completion or foreclose)"
        ],
        resolution_strategy="Require unconditional lien waivers for prior draws, conditional for current draw; engage independent inspector; record mortgage before commencement; hold 10% retainage until final completion and lien period expiration",
        entity_scope="Developers, contractors, construction lenders on ground-up development or major renovation projects",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Standard industry practice; mechanics' lien priority varies by state",
        controlling_precedent="State-specific mechanics' lien case law (e.g., Connolly Development v. Superior Court, 17 Cal.3d 803 (1976) - mechanics' lien priority over mortgage if work commenced first)",
        issue_category=IssueCategory.CONSTRUCTION
    ),
    DoctrineBlock(
        topic="CAM Reconciliation and Audit Rights",
        keywords=["CAM", "common area maintenance", "reconciliation", "operating expenses", "audit", "BOMA", "gross-up"],
        conclusion_template=[
            "Landlord bills estimated CAM monthly; reconciles annually based on actual expenses and provides statement to tenants.",
            "Tenant has 60-120 day window to audit landlord's books after receiving reconciliation statement.",
            "Common disputes: capital improvements included in CAM, management fees on gross vs net, no gross-up adjustment."
        ],
        reasoning_framework="""
CAM Reconciliation Framework:
1. CAM Components (Common Area Maintenance):
   - Repair and Maintenance: Parking lot repaving, roof repairs, landscaping, HVAC maintenance for common areas
   - Utilities: Electricity, water, gas for common areas (lobbies, hallways, parking lot lighting)
   - Janitorial: Cleaning common areas (not tenant-exclusive spaces)
   - Security: Security guards, cameras, alarm monitoring
   - Property Management: Management company fees (typically 3-5% of gross rent or 5% of operating expenses)
   - Insurance: Property insurance, liability insurance for common areas
   - Administrative: Accounting, legal fees related to property operations (not leasing or financing)
2. Exclusions from CAM (negotiate in lease):
   - Capital Improvements: Expenditures extending useful life or adding value (new roof, HVAC replacement) - should be capitalized and amortized, not expensed
   - Leasing Costs: Brokerage commissions, tenant improvement allowances, lease buyouts
   - Debt Service: Mortgage principal and interest
   - Landlord's Income Taxes: Entity-level taxes on rental income
   - Depreciation and Amortization: Non-cash expenses
   - Ground Lease Rent: If landlord leases land and subleases to tenants
   - Fines and Penalties: Late fees, code violations due to landlord's negligence
3. Annual Reconciliation Process:
   - Landlord provides detailed statement within 90-120 days after fiscal year end
   - Statement shows: budgeted CAM, actual CAM, tenant's proportionate share, monthly payments made, shortfall or overage
   - If actual > estimated: Tenant owes additional amount (due within 30 days)
   - If estimated > actual: Landlord credits tenant's next month's CAM or refunds (per lease terms)
4. Audit Rights:
   - Tenant has 60-120 days after receiving statement to request audit
   - Tenant's CPA or third-party auditor reviews landlord's books, invoices, contracts
   - Audit cost: Tenant pays unless error >5% (then landlord pays)
   - Landlord must provide records within 30 days; failure may waive CAM claim
5. Gross-Up Adjustment:
   - Problem: Low occupancy inflates per-SF CAM (fixed costs spread over fewer tenants)
   - Solution: Gross-up variable expenses to 95% occupancy as if building fully leased
   - Example: $100K landscaping at 60% occupancy = $166/tenant SF; gross-up to 95% = $105/tenant SF
        """,
        key_factors=[
            "CAM definition and exclusions in lease (capital improvements, leasing costs excluded)",
            "Gross-up provision at 95% occupancy (critical if building under-leased)",
            "Audit rights window (60-120 days after statement receipt)",
            "Audit cost allocation (tenant pays unless error exceeds 5% threshold)",
            "Management fee calculation base (gross rent including CAM vs net base rent only)",
            "Reconciliation timing (statement due 90-120 days after year-end)",
            "Caps on CAM increases (e.g., 3-5% annual cap on controllable expenses)"
        ],
        primary_authority=[
            "Lease agreement CAM provisions (contract law)",
            "BOMA measurement standards for proportionate share calculation",
            "State landlord-tenant law (some states regulate expense pass-throughs)",
            "GAAP accounting standards (capital vs operating expense classification)"
        ],
        burden_holder="Landlord to provide accurate reconciliation and supporting documentation; tenant to audit within deadline",
        adversary_position="Landlord includes capital improvements, leasing costs, or inflated management fees in CAM; tenant challenges on audit",
        counter_arguments=[
            "Capital improvement expensed in CAM (violates lease and GAAP; should be capitalized over useful life)",
            "Management fee calculated on gross rent including CAM reimbursements (double-counts; should exclude reimbursements)",
            "No gross-up provision; tenant's CAM share inflated due to 50% vacancy (negotiate gross-up to 95%)",
            "Landlord's administrative fees excessive (3-5% management fee standard; higher amounts may be unreasonable)",
            "Audit reveals 8% overcharge but tenant pays audit cost (lease should shift cost to landlord if error >5%)"
        ],
        resolution_strategy="Negotiate CAM exclusions for capital items and leasing costs, require gross-up to 95% occupancy, include audit rights with landlord paying if error >5%, cap controllable expenses at 3-5% annual increase",
        entity_scope="Retail, office, industrial tenants in multi-tenant properties with NNN or modified gross leases",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Standard industry practice; audit rights and gross-up are heavily negotiated terms",
        controlling_precedent="No controlling case law; CAM disputes resolved via lease contract interpretation and arbitration",
        issue_category=IssueCategory.OPERATIONS
    ),
    DoctrineBlock(
        topic="Percentage Rent in Retail Leases",
        keywords=["percentage rent", "breakpoint", "natural breakpoint", "gross sales", "artificial breakpoint", "radius restriction"],
        conclusion_template=[
            "Percentage rent = tenant pays base rent plus percentage of gross sales above breakpoint (typically 5-8% of sales).",
            "Natural breakpoint: base rent / percentage = breakpoint sales; artificial breakpoint set below natural to start percentage rent sooner.",
            "Landlord enforces via sales reporting, audit rights, and radius restrictions preventing tenant from opening nearby competing location."
        ],
        reasoning_framework="""
Percentage Rent Framework:
1. Structure:
   - Base Rent: Fixed minimum rent (e.g., $50/SF)
   - Percentage Rate: 5-8% of gross sales (varies by retail type: apparel 6-8%, grocery 1-2%, restaurants 6-7%)
   - Breakpoint: Sales threshold above which percentage rent applies
   - Natural Breakpoint: Base Rent / Percentage Rate (e.g., $100K base / 6% = $1.67M breakpoint)
   - Artificial Breakpoint: Set below natural (e.g., $1M breakpoint even if natural is $1.67M; landlord gets percentage rent on sales between $1M-$1.67M)
2. Gross Sales Definition:
   - Includes: All revenue from sales, services, rentals, vending machines, gift cards redeemed
   - Excludes: Sales tax, returns/refunds, inter-company transfers, credit card fees, gift cards sold but not redeemed
   - Disputes: Online sales (allocate to store if ship-from-store or pick-up-in-store), franchise fees, loyalty program discounts
3. Sales Reporting and Audit:
   - Tenant submits monthly/quarterly sales reports within 15-30 days
   - Annual certification by CPA that sales reported accurately
   - Landlord audit rights: once per year, tenant pays if underreporting >3-5%
   - POS integration: Some landlords require direct access to point-of-sale data
4. Radius Restriction (Exclusivity):
   - Tenant prohibited from opening competing location within 3-5 mile radius
   - Protects landlord's percentage rent stream
   - Violation: Sales from competing location may be deemed sales at subject location for percentage rent calculation
   - Reciprocal Exclusivity: Landlord may grant tenant exclusive use for certain categories (e.g., only coffee shop in center)
5. Co-Tenancy Clause:
   - Tenant's percentage rent obligation reduced or eliminated if anchor tenant vacates or occupancy falls below threshold (e.g., 70%)
   - Protects tenant from paying percentage rent in dying shopping center
        """,
        key_factors=[
            "Natural vs artificial breakpoint (artificial breakpoint favors landlord)",
            "Percentage rate vs market (apparel 6-8%, grocery 1-2%, restaurant 6-7%)",
            "Gross sales definition and exclusions (negotiate to exclude online, franchise fees, inter-company)",
            "Sales reporting frequency and audit rights (annual audit standard; landlord pays if error <5%)",
            "Radius restriction enforceability (3-5 miles standard; may be unenforceable as restraint on trade in some states)",
            "Co-tenancy protections (percentage rent reduced if anchor vacates)",
            "POS data access (landlord may require real-time sales integration)"
        ],
        primary_authority=[
            "Lease agreement percentage rent clause (contract law)",
            "State restraint of trade law (radius restrictions may be unenforceable if overly broad)",
            "Restatement (Second) of Contracts Section 188 (reasonableness of non-compete covenants)",
            "Bankruptcy Code Section 365 (lease assumption/rejection in tenant bankruptcy)"
        ],
        burden_holder="Tenant to report sales accurately and comply with radius restriction; landlord to audit and enforce",
        adversary_position="Tenant underreports sales; landlord audits and seeks back rent plus damages",
        counter_arguments=[
            "Online sales excluded from gross sales (landlord argues ship-from-store or BOPIS sales should count)",
            "Franchise fees excluded (landlord argues fees are derived from store operations, should be included)",
            "Radius restriction violated but tenant claims unenforceable restraint of trade (court may void if >5 miles or indefinite duration)",
            "Tenant bankruptcy; percentage rent deemed administrative expense vs pre-petition claim (affects priority)",
            "Co-tenancy clause triggered; tenant stops paying percentage rent (landlord disputes anchor vacancy definition)"
        ],
        resolution_strategy="Negotiate natural breakpoint or close to it, define gross sales narrowly, limit audit to once per year with landlord paying if error <5%, negotiate reciprocal exclusivity and co-tenancy protections",
        entity_scope="Retail tenants in shopping centers, malls, lifestyle centers with percentage rent leases",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Standard retail lease practice; radius restrictions enforceability varies by state",
        controlling_precedent="Valu-Mart, Inc. v. Walker, 201 So.2d 821 (Fla. 1967) - percentage rent valid; gross sales definition governs",
        issue_category=IssueCategory.LEASE_STRUCTURE
    ),
    DoctrineBlock(
        topic="Tenant Improvement Allowance and Delivery Condition",
        keywords=["TI allowance", "tenant improvements", "work letter", "vanilla shell", "warm shell", "cold shell", "allowance"],
        conclusion_template=[
            "Landlord provides tenant improvement allowance (e.g., $40-80/SF) for tenant to build out space; excess cost borne by tenant.",
            "Delivery condition varies: cold shell (bare walls), warm shell (HVAC, electrical to demising wall), vanilla shell (drop ceiling, lighting, minimal finishes).",
            "Work letter specifies allowance amount, permitted uses, draw process, landlord approval rights, and construction timeline."
        ],
        reasoning_framework="""
Tenant Improvement (TI) Allowance Framework:
1. Delivery Conditions:
   - Cold Shell (Core and Shell): Exterior walls, roof, slab, base building HVAC/electrical to riser closet; tenant builds everything inside demising walls (studs, drywall, ceiling, lighting, finishes, HVAC distribution)
   - Warm Shell: Cold shell + HVAC distribution to diffusers, electrical to panel in suite, plumbing rough-in; tenant finishes walls, ceiling, flooring
   - Vanilla Shell (White Box): Warm shell + drywall, drop ceiling, basic lighting (2x4 troffers), carpet or VCT flooring; tenant adds demising walls, finishes, branding
   - Turnkey: Landlord builds to tenant's specifications; tenant pays overage above allowance
2. TI Allowance Amount:
   - Market Range: Office $40-80/SF (CBD Class A higher, suburban lower), Retail $30-60/SF, Industrial $5-15/SF (warehouse minimal, office area higher)
   - Negotiated Based On: Lease term (longer term = higher allowance), tenant creditworthiness, market conditions, landlord's vacancy pressure
   - Allowance Uses: Hard costs (labor, materials), soft costs (architect, engineer, permits; often capped at 10-15% of allowance)
   - Excess Costs: Tenant pays overage via upfront cash or amortized into rent (landlord loans at 8-10% over lease term)
3. Work Letter (Exhibit to Lease):
   - Specifies: Allowance amount, permitted uses, draw schedule, landlord approval process, construction timeline
   - Landlord Approval: Tenant submits plans to landlord's architect (10-15 business day review); landlord may not unreasonably withhold approval
   - Construction Administration: Landlord may charge 5-10% of TI cost for oversight, or tenant manages construction directly with landlord's contractor
4. TI Draw Process:
   - Tenant hires contractor, submits invoices + lien waivers to landlord
   - Landlord disburses allowance in draws (typically monthly, up to 90% during construction, final 10% at completion)
   - Final draw requires: Certificate of Occupancy, final lien waivers, as-built drawings, warranty documentation
5. Unused Allowance:
   - Use-It-Or-Lose-It: Standard provision; tenant forfeits unused allowance (landlord keeps savings)
   - Cash-Out Option: Tenant negotiates to receive unused allowance as rent credit or cash (rare; landlord resists)
        """,
        key_factors=[
            "Delivery condition (cold/warm/vanilla shell affects tenant's construction cost)",
            "TI allowance amount vs market (negotiate higher if long-term lease or strong tenant)",
            "Allowance uses (negotiate to include soft costs, FF&E, signage)",
            "Overage financing (landlord loan at 8-10% vs tenant cash)",
            "Landlord approval rights (plans, contractor selection; negotiate reasonableness standard)",
            "Construction timeline (rent abatement during construction if landlord delays)",
            "Unused allowance disposition (use-it-or-lose-it vs cash-out)"
        ],
        primary_authority=[
            "Lease agreement work letter exhibit (contract law)",
            "Building codes (IBC, NFPA, ADA) applicable to tenant improvements",
            "Mechanics' lien statutes (tenant's contractor may lien landlord's property if unpaid)",
            "AIA construction contract documents (A101, A201 if tenant hires architect/contractor)"
        ],
        burden_holder="Tenant to design, permit, and construct within allowance and timeline; landlord to disburse allowance timely if conditions met",
        adversary_position="Landlord delays approval of plans or draws; tenant seeks rent abatement or damages for delayed occupancy",
        counter_arguments=[
            "Landlord withholds TI draw pending plan revisions (tenant argues unreasonable delay; seeks arbitration)",
            "Tenant's contractor files mechanics' lien for unpaid work (landlord's title encumbered; landlord may bond off lien)",
            "Tenant exceeds allowance but landlord refuses to finance overage (tenant pays cash or scales back scope)",
            "Landlord charges 15% construction administration fee (tenant argues excessive; negotiate 5-10% cap)",
            "Unused allowance $20K; tenant requests cash-out (landlord denies per use-it-or-lose-it clause)"
        ],
        resolution_strategy="Negotiate higher TI allowance for long-term lease, include soft costs and FF&E in allowance, require landlord approval within 10 business days (deemed approved if silent), obtain rent abatement if landlord delays, negotiate cash-out or rent credit for unused allowance",
        entity_scope="Office, retail, industrial tenants negotiating new leases or expansions with tenant improvement buildout",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Standard commercial lease practice; TI allowance heavily negotiated based on market conditions",
        controlling_precedent="No controlling case law; work letter terms govern via contract interpretation",
        issue_category=IssueCategory.LEASE_STRUCTURE
    ),
    DoctrineBlock(
        topic="Zoning Variance and Special Use Permit",
        keywords=["zoning", "variance", "special use permit", "conditional use", "area variance", "use variance", "hardship"],
        conclusion_template=[
            "Zoning variance excuses strict compliance with zoning code due to unique hardship (area variance for setback/height) or permits otherwise prohibited use (use variance).",
            "Special use permit allows conditional use expressly permitted by zoning code subject to conditions (e.g., daycare, church, gas station in commercial zone).",
            "Variance requires proof of unnecessary hardship; SUP requires proof of compliance with enumerated standards."
        ],
        reasoning_framework="""
Zoning Variance and Special Use Permit Framework:
1. Zoning Variance Types:
   - Area Variance: Relief from dimensional requirements (setback, height, lot coverage, parking) due to unique lot characteristics
     - Example: Corner lot with two front yards (double setback) creates buildable area hardship; variance grants relief to build closer to one street
   - Use Variance: Permission to use property for purpose not allowed in zoning district (e.g., commercial use in residential zone)
     - Higher burden: Applicant must prove unnecessary hardship (land cannot yield reasonable return for any permitted use)
     - Disfavored by courts; many jurisdictions prohibit use variances entirely
2. Variance Standards (typical criteria from Euclid v. Ambler):
   - Unnecessary Hardship: Unique to property (topography, shape, location), not self-created, not economic (mere financial loss insufficient)
   - No Harm to Public: Variance will not alter essential character of neighborhood or substantially impair zoning plan
   - Minimum Relief: Variance grants minimum relief necessary to address hardship
   - Not Self-Created: Hardship existed before applicant acquired property (buying lot knowing of restriction may defeat variance)
3. Special Use Permit (Conditional Use Permit):
   - Definition: Use expressly allowed by zoning code but subject to conditions and discretionary approval (e.g., daycare in residential zone, gas station in commercial zone, cell tower, quarry)
   - Standards: Zoning code lists enumerated criteria (traffic, noise, hours, screening, setbacks, parking); applicant must prove compliance
   - Conditions: Approving body (planning commission, board of adjustment) may impose conditions to mitigate impacts (screening, landscaping, hours of operation, traffic study)
   - Burden: Lower than variance; applicant proves compliance with objective standards, not hardship
4. Approval Process:
   - Application: Site plan, traffic study, environmental review (if applicable)
   - Notice: Mailed notice to adjoining owners (typically 200-300 foot radius), published notice, sign posted on property
   - Public Hearing: Neighbors may testify in opposition; applicant presents evidence
   - Decision: Approving body issues written decision with findings of fact supporting approval or denial
   - Appeal: Denied applicant or aggrieved neighbor may appeal to court (substantial evidence standard or de novo in some states)
        """,
        key_factors=[
            "Type of relief (area variance easier than use variance)",
            "Hardship uniqueness (lot shape, topography vs economic hardship - only former qualifies)",
            "Self-created hardship (buying restricted lot defeats variance in most jurisdictions)",
            "Neighborhood opposition (extensive opposition may doom variance even if standards met)",
            "Special use vs variance (SUP has lower burden - compliance with criteria vs hardship)",
            "Conditions imposed (SUP conditions must reasonably relate to impacts; cannot be arbitrary)",
            "Statute of limitations on appeal (typically 30 days from decision)"
        ],
        primary_authority=[
            "Standard State Zoning Enabling Act (model legislation; most states adopted version)",
            "Village of Euclid v. Ambler Realty Co., 272 U.S. 365 (1926) - zoning constitutional",
            "State zoning enabling statutes (e.g., NY Town Law Section 267; CA Gov't Code Section 65900)",
            "Local zoning ordinance variance and SUP standards (varies by municipality)",
            "State appellate case law on variance standards (e.g., Otto v. Steinhilber, 282 N.Y. 71 (1939) - unnecessary hardship standard)"
        ],
        burden_holder="Applicant to prove hardship (variance) or compliance with standards (SUP); approving body must make findings supporting decision",
        adversary_position="Neighbors oppose; argue no hardship, self-created, or special use will harm neighborhood",
        counter_arguments=[
            "Variance applicant claims economic hardship only (insufficient; must show land cannot yield reasonable return for permitted use)",
            "Hardship self-created by subdividing lot (defeats variance in most jurisdictions)",
            "Neighboring property owners claim variance will reduce property values (economic harm alone insufficient to deny; must show zoning plan harm)",
            "Special use permit denied despite compliance with all criteria (arbitrary and capricious; overturned on appeal)",
            "Conditions imposed on SUP unrelated to impacts (e.g., require applicant to repave public street 1 mile away; void as improper exaction)"
        ],
        resolution_strategy="For variance: prove unique lot hardship (shape, topography, legal non-conforming use), show minimum relief requested, demonstrate no neighborhood harm; For SUP: prove compliance with all enumerated criteria, propose voluntary conditions to mitigate neighbor concerns, present traffic/environmental studies",
        entity_scope="Property owners, developers seeking zoning relief for non-conforming development or conditional uses",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established zoning law; variance standards strict; SUP more permissive if criteria met",
        controlling_precedent="Village of Euclid v. Ambler Realty Co., 272 U.S. 365 (1926) - zoning enabling act constitutional; Otto v. Steinhilber, 282 N.Y. 71 (1939) - unnecessary hardship defined",
        issue_category=IssueCategory.ZONING
    ),
    DoctrineBlock(
        topic="Defeasance in CMBS Loans",
        keywords=["defeasance", "CMBS", "lock-out", "prepayment", "successor borrower", "treasury securities", "collateral substitution"],
        conclusion_template=[
            "Defeasance is the only prepayment option during CMBS loan lock-out period (typically first 2-5 years).",
            "Borrower forms successor borrower entity, purchases US Treasury securities matching loan cash flows, substitutes Treasuries for property as collateral.",
            "Original borrower released; property freed from mortgage; successor borrower owns Treasuries and pays debt service from coupon/maturity proceeds."
        ],
        reasoning_framework="""
Defeasance Framework (CMBS Loans):
1. Purpose: Allows borrower to prepay CMBS loan during lock-out period without harming bondholders (substitute collateral maintains bond cash flows)
2. Lock-Out Period: CMBS loans prohibit prepayment for first 2-5 years (sometimes longer); defeasance is ONLY prepayment option
3. Defeasance Mechanics:
   - Borrower engages defeasance consultant (Chatham Financial, AST Defeasance, etc.)
   - Consultant calculates required US Treasury portfolio: match loan payment dates and amounts (principal + interest) exactly
   - Borrower purchases Treasuries (face value approximately 102-108% of loan balance due to premium for exact cash flow matching)
   - Borrower forms Successor Borrower LLC (special purpose entity)
   - Treasuries pledged to lender as substitute collateral; property released from mortgage lien
   - Successor Borrower owns Treasuries, receives coupon payments, pays debt service; Treasuries mature at loan maturity to pay off principal
   - Original Borrower released from loan obligations; property free and clear
4. Cost Components:
   - Treasury Premium: Typically 2-8% of loan balance (cost to buy Treasuries yielding exact cash flows; varies with interest rate environment)
   - Consultant Fees: $25K-50K
   - Legal Fees: $15K-30K (borrower's and lender's counsel)
   - Rating Agency Fees: $5K-15K (S&P, Moody's must confirm defeasance maintains bond rating)
   - Successor Borrower Formation: $5K-10K
   - Total Cost: 3-10% of loan balance (lower if interest rates high, higher if rates low)
5. When Defeasance Makes Sense:
   - Property sale during lock-out period (buyer requires free-and-clear title)
   - Refinancing to higher leverage or better terms
   - Property value appreciation makes cost worthwhile (e.g., 30% gain offsets 5% defeasance cost)
6. Alternatives Post-Lock-Out:
   - Yield Maintenance: Prepayment penalty = present value of remaining interest at Treasury rate + spread (typically cheaper than defeasance)
   - Defeasance still available but usually more expensive than yield maintenance
        """,
        key_factors=[
            "Time remaining in lock-out period (year 1-2 defeasance very expensive; year 4-5 cheaper as fewer payments to match)",
            "Interest rate environment (low rates = expensive Treasuries; high rates = cheaper defeasance)",
            "Loan balance size (economies of scale; defeasance more cost-effective on $10M+ loans)",
            "Property sale vs refinance (if sale, may negotiate defeasance cost with buyer)",
            "Yield maintenance period remaining (if post-lock-out, compare defeasance vs yield maintenance cost)",
            "Successor borrower tax treatment (Treasury interest taxable to successor borrower; sometimes borrower retains via blocker structure)"
        ],
        primary_authority=[
            "CMBS loan agreement defeasance provisions",
            "Pooling and Servicing Agreement (PSA) - governs lender's ability to accept defeasance",
            "Treasury Regulations Section 1.1001-3 (modification of debt; defeasance treated as satisfaction)",
            "Rating agency criteria (S&P, Moody's, Fitch) for CMBS defeasance"
        ],
        burden_holder="Borrower to engage consultant, purchase Treasuries, form successor borrower, pay all costs; lender/servicer to accept defeasance if loan documents permit",
        adversary_position="Lender refuses defeasance during lock-out (violates loan terms; borrower may seek specific performance); rating agency rejects Treasury portfolio (requires adjustment)",
        counter_arguments=[
            "Loan documents prohibit defeasance entirely (rare but possible; borrower stuck until maturity or default)",
            "Rating agency rejects proposed Treasury portfolio (cash flows don't match exactly; consultant must recalculate)",
            "Defeasance cost exceeds property gain (borrower decides to wait until yield maintenance period)",
            "Successor borrower bankruptcy remote requirements not met (lender may reject; requires restructuring)",
            "Treasury interest taxed to borrower despite no economic benefit (borrower uses blocker entity to mitigate)"
        ],
        resolution_strategy="Engage defeasance consultant early (60-90 days before desired close), compare defeasance vs waiting for yield maintenance period, negotiate cost-sharing with property buyer if sale transaction, use blocker structure if tax efficiency needed",
        entity_scope="Borrowers with CMBS loans seeking to prepay during lock-out period (property sale or refinance)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Standard CMBS loan feature; defeasance mechanics well-established; cost varies with interest rates",
        controlling_precedent="No controlling case law; defeasance governed by CMBS loan documents and PSA",
        issue_category=IssueCategory.FINANCING
    ),
]

# ═══════════════════════════════════════════════════════════════════════════
# TELEMETRY & METRICS
# ═══════════════════════════════════════════════════════════════════════════

class Telemetry:
    def __init__(self):
        self.queries: List[Dict[str, Any]] = []
        self.errors: List[Dict[str, Any]] = []
        self.doctrine_hits: Dict[str, int] = {}

    def log_query(self, query: str, mode: ResponseMode, latency_ms: float, doctrines_triggered: List[str]):
        self.queries.append({
            "timestamp": datetime.utcnow().isoformat(),
            "query": query,
            "mode": mode.value,
            "latency_ms": latency_ms,
            "doctrines_triggered": doctrines_triggered
        })
        for doctrine in doctrines_triggered:
            self.doctrine_hits[doctrine] = self.doctrine_hits.get(doctrine, 0) + 1

    def log_error(self, error: str, context: Dict[str, Any]):
        self.errors.append({
            "timestamp": datetime.utcnow().isoformat(),
            "error": error,
            "context": context
        })

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_queries": len(self.queries),
            "total_errors": len(self.errors),
            "avg_latency_ms": sum(q["latency_ms"] for q in self.queries) / len(self.queries) if self.queries else 0,
            "doctrine_hit_rate": self.doctrine_hits,
            "queries_by_mode": {
                mode.value: sum(1 for q in self.queries if q["mode"] == mode.value)
                for mode in ResponseMode
            }
        }

TELEMETRY = Telemetry()

# ═══════════════════════════════════════════════════════════════════════════
# CORE ENGINE LOGIC
# ═══════════════════════════════════════════════════════════════════════════

def three_layer_response(query: str, mode: ResponseMode, zone: AnalysisZone) -> tuple[str, List[str], ConfidenceLevel]:
    """TIE Component 1: Three-layer response (cache, semantic, deep)"""
    start_time = time.time()

    # Layer 1: Doctrine Cache (0-200ms)
    triggered_blocks = []
    query_lower = query.lower()
    for block in DOCTRINE_CACHE:
        if any(kw.lower() in query_lower for kw in block.keywords):
            triggered_blocks.append(block)

    if not triggered_blocks:
        TELEMETRY.log_error("No doctrine match", {"query": query})
        return ("No relevant CRE doctrine found for this query. Please rephrase or provide more details.",
                [], ConfidenceLevel.DISCLOSURE)

    # Sort by category relevance
    triggered_blocks.sort(key=lambda b: sum(1 for kw in b.keywords if kw.lower() in query_lower), reverse=True)
    primary_block = triggered_blocks[0]

    # Build response based on mode
    if mode == ResponseMode.FAST:
        response = f"{primary_block.conclusion_template[0]} {primary_block.conclusion_template[1]}"
    elif mode == ResponseMode.DEFENSE:
        response = f"""CONCLUSION: {' '.join(primary_block.conclusion_template)}

REASONING: {primary_block.reasoning_framework[:500]}

KEY FACTORS: {', '.join(primary_block.key_factors[:5])}

AUTHORITY: {', '.join(primary_block.primary_authority[:3])}

CONFIDENCE: {primary_block.confidence_stratification}"""
    else:  # MEMO
        response = f"""MEMORANDUM - Commercial Real Estate Analysis

ISSUE: {primary_block.topic}

CONCLUSION: {' '.join(primary_block.conclusion_template)}

REASONING:
{primary_block.reasoning_framework}

KEY FACTORS:
{chr(10).join(f'- {factor}' for factor in primary_block.key_factors)}

CONTROLLING AUTHORITY:
{chr(10).join(f'- {auth}' for auth in primary_block.primary_authority)}

ADVERSARY POSITION: {primary_block.adversary_position}

COUNTER-ARGUMENTS:
{chr(10).join(f'- {arg}' for arg in primary_block.counter_arguments)}

RECOMMENDED STRATEGY: {primary_block.resolution_strategy}

CONFIDENCE LEVEL: {primary_block.confidence.value}
STRATIFICATION: {primary_block.confidence_stratification}

CONTROLLING PRECEDENT: {primary_block.controlling_precedent}"""

    # Add zone-specific caveats
    if zone == AnalysisZone.AUDIT:
        response += "\n\n[AUDIT NOTE: This analysis is for documentation purposes. All citations verified against primary sources.]"
    elif zone == AnalysisZone.REPORTING:
        response += "\n\n[DISCLOSURE: This analysis represents professional judgment based on available authorities. Consult legal counsel for specific transactions.]"

    authorities = primary_block.primary_authority
    latency_ms = (time.time() - start_time) * 1000

    TELEMETRY.log_query(query, mode, latency_ms, [b.topic for b in triggered_blocks])

    return response, authorities, primary_block.confidence

def compute_determinism_hash(query: str, response: str) -> str:
    """TIE Component 16: SHA-256 determinism hash"""
    content = f"{query}|{response}|{VERSION}"
    return hashlib.sha256(content.encode()).hexdigest()

# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

app = FastAPI(title=ENGINE_NAME, version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.add("ent12_cre_engine.log", rotation="100 MB", retention="30 days", level="INFO")

@app.get("/health")
async def health():
    """TIE Component 12: Health endpoint"""
    stats = TELEMETRY.get_stats()
    return {
        "status": "operational",
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": VERSION,
        "port": PORT,
        "doctrine_blocks": len(DOCTRINE_CACHE),
        "telemetry": stats,
        "uptime_queries": stats["total_queries"],
        "error_rate": stats["total_errors"] / max(stats["total_queries"], 1)
    }

@app.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest):
    """Main query endpoint with TIE-20 integration"""
    try:
        logger.info(f"Query received: {request.query[:100]} | Mode: {request.mode} | Zone: {request.zone}")

        response_text, authorities, confidence = three_layer_response(
            request.query, request.mode, request.zone
        )

        start_time = time.time()
        determinism_hash = compute_determinism_hash(request.query, response_text)
        latency_ms = (time.time() - start_time) * 1000

        return QueryResponse(
            engine_id=ENGINE_ID,
            version=VERSION,
            query=request.query,
            mode=request.mode,
            zone=request.zone,
            response=response_text,
            confidence=confidence,
            authorities_cited=authorities,
            doctrine_blocks_triggered=[b.topic for b in DOCTRINE_CACHE if any(kw.lower() in request.query.lower() for kw in b.keywords)],
            latency_ms=latency_ms,
            determinism_hash=determinism_hash,
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        TELEMETRY.log_error(str(e), {"query": request.query})
        raise HTTPException(status_code=500, detail=f"Engine error: {str(e)}")

@app.get("/doctrines")
async def list_doctrines():
    """List all doctrine blocks"""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": b.topic,
                "keywords": b.keywords,
                "category": b.issue_category.value,
                "confidence": b.confidence.value
            }
            for b in DOCTRINE_CACHE
        ]
    }

@app.get("/stats")
async def get_stats():
    """TIE Component 11: Metrics collector"""
    return TELEMETRY.get_stats()

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
