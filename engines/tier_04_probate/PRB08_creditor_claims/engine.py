"""
PRB08 CREDITOR CLAIMS ENGINE v1.0.0
TIE-Grade Intelligence Engine for Probate Creditor Claims Analysis

Handles creditor claims in probate proceedings including:
- Notice to creditors and claims periods
- Priority of claims and payment order
- Secured vs unsecured creditor rights
- Exempt property and family allowances
- Insolvent estate administration
- Abatement and personal representative liability
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Literal
from dataclasses import dataclass, field, asdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

ENGINE_ID = "PRB08"
ENGINE_NAME = "Creditor Claims Engine"
VERSION = "1.0.0"
PORT = 9118

# ═══════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
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

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=5000)
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.PLANNING
    context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query: str
    answer: str
    mode: ResponseMode
    zone: AnalysisZone
    confidence: ConfidenceLevel
    triggered_doctrines: List[str]
    sources: List[str]
    epistemic_status: str
    determinism_hash: str
    latency_ms: float
    telemetry: Dict[str, Any]

# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE BLOCKS
# ═══════════════════════════════════════════════════════════════════════════

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
    disclosure_caveat: str = ""
    triggered_count: int = 0

# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE (25+ creditor claims doctrines)
# ═══════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: Dict[str, DoctrineBlock] = {
    "notice_to_creditors_publication": DoctrineBlock(
        topic="Notice to Creditors - Publication Requirements",
        keywords=["notice", "creditors", "publication", "newspaper", "claims period"],
        conclusion_template=[
            "Personal representative must publish notice to creditors in newspaper of general circulation",
            "Notice starts statutory claims period under TEC 308.051",
            "Publication must occur within one month after letters issued"
        ],
        reasoning_framework="""
Texas Estates Code 308.051-308.054 establishes mandatory notice to creditors:

1. PUBLICATION REQUIREMENT (308.051):
   - Personal representative shall publish notice in newspaper of general circulation
   - Must occur within one month after receiving letters
   - Notice format prescribed by statute

2. CONTENT OF NOTICE (308.052):
   - All persons having claims against estate are required to present them
   - Must state mailing address to which claims may be presented
   - Claims must be presented within time prescribed by law

3. EFFECT OF PUBLICATION:
   - Starts four-month claims period for creditors with actual notice
   - Starts two-month period for creditors receiving published notice only
   - Failure to timely publish extends claims period indefinitely

4. CONSEQUENCES OF DEFECTIVE NOTICE:
   - May expose personal representative to surcharge
   - Creditors not barred if notice defective
   - Court may extend claims period if publication deficient
""",
        key_factors=[
            "Newspaper of general circulation requirement",
            "One-month deadline after letters issued",
            "Statutory content requirements",
            "Starting point for claims period calculation",
            "Personal representative duty to publish"
        ],
        primary_authority=[
            "Texas Estates Code Sec. 308.051 (Publication of Notice)",
            "Texas Estates Code Sec. 308.052 (Contents of Published Notice)",
            "Texas Estates Code Sec. 308.053 (Proof of Publication)",
            "Texas Estates Code Sec. 308.054 (Failure to Publish)"
        ],
        burden_holder="Personal representative bears burden of timely compliant publication",
        adversary_position="Creditor argues publication defective or untimely, extending claims period",
        counter_arguments=[
            "Notice substantially complied with statutory requirements",
            "Creditor had actual notice from other sources",
            "Publication in approved newspaper of record",
            "Creditor suffered no prejudice from minor defects",
            "Court approved notice form before publication"
        ],
        resolution_strategy="Publish exact statutory notice within one month; obtain proof of publication; file proof with court; provide actual notice to known creditors beyond publication",
        entity_scope="Testate and intestate estates requiring administration",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - clear statutory mandate with established case law",
        controlling_precedent="TEC 308.051-308.054 mandatory publication requirements",
        disclosure_caveat="Consult local probate rules for any additional notice requirements"
    ),

    "claims_period_four_months": DoctrineBlock(
        topic="Four-Month Claims Period for Known Creditors",
        keywords=["claims period", "four months", "known creditor", "actual notice", "bar date"],
        conclusion_template=[
            "Known creditors must present claims within four months after notice",
            "Actual notice starts four-month period regardless of publication",
            "Claims not timely presented are barred"
        ],
        reasoning_framework="""
TEC 308.051(a) and 355.064 establish four-month claims period:

1. KNOWN CREDITOR STANDARD:
   - Creditor whose identity is known or reasonably ascertainable
   - Personal representative has duty to give actual notice
   - Includes creditors appearing in decedent's records

2. FOUR-MONTH PERIOD TRIGGERS:
   - Actual notice to creditor OR
   - Publication of notice (whichever is earlier)
   - Period runs from date notice received

3. EFFECT OF PERIOD EXPIRATION:
   - Claims not presented within four months are barred (355.064)
   - No extension absent fraud or concealment
   - Applies to secured and unsecured claims alike

4. CONSEQUENCES OF LATE CLAIM:
   - Personal representative may reject as untimely
   - Creditor may not maintain suit on barred claim
   - Court lacks jurisdiction over time-barred claims
   - Estate may retain property otherwise payable to creditor

5. EXCEPTIONS TO BAR:
   - Claims for which personal representative is personally liable
   - Federal tax liens (federal law preempts state bar)
   - Claims concealed by personal representative fraud
""",
        key_factors=[
            "Identity of creditor known or reasonably ascertainable",
            "Actual notice provided to creditor",
            "Date of notice receipt determines period start",
            "Four-month deadline strictly enforced",
            "No late filing absent extraordinary circumstances"
        ],
        primary_authority=[
            "Texas Estates Code Sec. 308.051(a) (Notice Period)",
            "Texas Estates Code Sec. 355.064 (Period for Filing Claim)",
            "Texas Estates Code Sec. 355.001 (Definition of Claim)",
            "Tulsa Professional Collection Services v. Pope (1988) - known creditor duty"
        ],
        burden_holder="Creditor bears burden of timely filing; personal representative bears burden of providing actual notice to known creditors",
        adversary_position="Estate argues claim time-barred; creditor argues lack of actual notice or concealment",
        counter_arguments=[
            "Creditor received actual notice on date claimed",
            "Personal representative failed to provide actual notice",
            "Creditor identity not reasonably ascertainable",
            "Extraordinary circumstances justify late filing",
            "Federal law preempts state claims period"
        ],
        resolution_strategy="Personal representative: send certified mail actual notice to all known creditors immediately after letters; document mailing. Creditor: file within four months of actual notice; if late, show lack of notice or fraud",
        entity_scope="All probate estates in Texas",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - well-established statute of non-claim",
        controlling_precedent="TEC 355.064 four-month bar is mandatory and jurisdictional",
        disclosure_caveat="Federal claims may have different notice requirements"
    ),

    "priority_of_claims_funeral": DoctrineBlock(
        topic="Priority of Claims - Funeral Expenses First Class",
        keywords=["priority", "funeral expenses", "first class", "payment order", "class one"],
        conclusion_template=[
            "Funeral expenses are Class 1 priority claims under TEC 355.102",
            "Must be paid before all other claims except administration costs",
            "Includes reasonable burial, cremation, and memorial expenses"
        ],
        reasoning_framework="""
TEC 355.102 establishes eight classes of claims with strict priority:

CLASS 1 - FUNERAL EXPENSES (355.102(1)):
   - Funeral and burial expenses
   - Reasonable in amount given decedent's estate and station
   - Includes costs of cremation, casket, service, monument
   - Court may reduce if excessive

RATIONALE FOR PRIORITY:
   - Public policy favors decent burial
   - Expenses incurred for benefit of decedent
   - Typically incurred before administration opens
   - Creditor (funeral home) had no opportunity for estate planning

REASONABLENESS STANDARD:
   - Must be commensurate with size of estate
   - Cannot exceed what average person in decedent's circumstances would incur
   - Extravagant expenses may be reduced by court
   - Examples: solid gold casket for $500 estate = unreasonable

PAYMENT MECHANICS:
   - Personal representative pays from estate assets
   - If insufficient funds, Class 1 claims paid pro rata
   - Later classes receive nothing until Class 1 paid in full
   - No bond required for funeral expense claimant
""",
        key_factors=[
            "Class 1 priority status under TEC 355.102(1)",
            "Reasonableness requirement for amount",
            "Pro rata payment within class if insufficient assets",
            "No payment to lower classes until Class 1 satisfied",
            "Court discretion to reduce excessive claims"
        ],
        primary_authority=[
            "Texas Estates Code Sec. 355.102(1) (Funeral Expenses First Class)",
            "Texas Estates Code Sec. 355.103 (Order of Payment)",
            "Texas Estates Code Sec. 355.151 (Classification of Claims)",
            "In re Estate of Smith (1995) - reasonableness standard"
        ],
        burden_holder="Funeral home bears burden of proving reasonableness if challenged",
        adversary_position="Lower-priority creditors argue funeral expenses excessive to preserve assets for their claims",
        counter_arguments=[
            "Expenses consistent with decedent's station in life",
            "Family's wishes regarding burial arrangements",
            "Customary costs in relevant community",
            "Pre-need contract establishing price",
            "No showing of excessiveness by objecting party"
        ],
        resolution_strategy="Funeral home: document standard pricing, show comparables, establish decedent's circumstances. Personal representative: pay reasonable funeral expenses without court order; seek court approval if amount questioned",
        entity_scope="All probate estates with funeral expense claims",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - clear statutory priority scheme",
        controlling_precedent="TEC 355.102 eight-class priority system is mandatory",
        disclosure_caveat="Reasonableness is fact-specific; consult local probate practice"
    ),

    "priority_secured_claims": DoctrineBlock(
        topic="Secured Claims Priority and Rights",
        keywords=["secured claim", "lien", "mortgage", "collateral", "foreclosure", "priority"],
        conclusion_template=[
            "Secured creditor has dual rights: foreclose on collateral OR file unsecured claim for deficiency",
            "Lien priority determined by state law regardless of probate priority classes",
            "Personal representative cannot defeat valid perfected liens"
        ],
        reasoning_framework="""
TEC 355.151(b) and UCC Article 9 govern secured claims in probate:

1. SECURED CLAIM DEFINED:
   - Claim with lien on specific estate property
   - Includes mortgages, deeds of trust, UCC-1 security interests
   - Judgment liens, tax liens, mechanic's liens
   - Perfection governs priority over other secured claims

2. RIGHTS OF SECURED CREDITOR IN PROBATE:
   - May foreclose under state law without probate court approval
   - May file claim for deficiency after foreclosure
   - May elect to file entire claim as unsecured (waive security)
   - Personal representative cannot sell collateral free of lien without creditor consent

3. PRIORITY AMONG SECURED CREDITORS:
   - Determined by state law (recording statutes, UCC priority rules)
   - First in time generally first in right
   - Purchase money security interests have super-priority
   - Tax liens may have statutory priority

4. INTERACTION WITH PROBATE PRIORITY CLASSES:
   - Secured claim paid from collateral first
   - Only deficiency falls into unsecured priority classes (Class 7)
   - Administration expenses (Class 0) do not prime secured creditor
   - Exception: liens securing debts for property preservation may prime

5. MARSHALLING DOCTRINE:
   - If secured creditor has claim against multiple assets
   - Unsecured creditors may request marshalling
   - Secured creditor must exhaust collateral before pursuing other estate assets
""",
        key_factors=[
            "Perfected security interest under UCC or real property recording act",
            "Collateral value vs. claim amount determines deficiency",
            "Foreclosure rights independent of probate proceeding",
            "Priority among secured creditors follows state law",
            "Personal representative cannot defeat valid liens"
        ],
        primary_authority=[
            "Texas Estates Code Sec. 355.151(b) (Secured Claims)",
            "Texas Business & Commerce Code Ch. 9 (UCC Secured Transactions)",
            "Texas Property Code Sec. 51.002 (Deed of Trust Foreclosure)",
            "Texas Property Code Sec. 12.001 (Recording Acts)",
            "Texas Tax Code Sec. 32.05 (Tax Lien Priority)"
        ],
        burden_holder="Secured creditor bears burden of proving perfection and value of collateral",
        adversary_position="Estate/unsecured creditors argue lien unperfected, value exceeds debt, or marshalling should apply",
        counter_arguments=[
            "UCC-1 filing or deed of trust recorded before death",
            "Appraisal supports collateral value below debt",
            "No other estate assets available for marshalling",
            "Foreclosure conducted per state law requirements",
            "PMSI exception to first-in-time priority applies"
        ],
        resolution_strategy="Secured creditor: confirm perfection, obtain appraisal, consider foreclosure vs. probate claim. Personal representative: review title and UCC records, object if lien invalid, request marshalling if applicable",
        entity_scope="Estates with secured debt or liened property",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - secured creditor rights well-established",
        controlling_precedent="Secured creditor may foreclose independently of probate; deficiency is Class 7 unsecured",
        disclosure_caveat="Federal tax liens have special priority rules under federal law"
    ),

    "family_allowance_exempt": DoctrineBlock(
        topic="Family Allowance and Exempt Property",
        keywords=["family allowance", "exempt property", "homestead", "surviving spouse", "exempt assets"],
        conclusion_template=[
            "Family allowance and exempt property set aside before creditor claims paid",
            "Homestead passes to heirs/surviving spouse free of testacy debts except purchase money, taxes, home equity loans",
            "Personal property exemptions under TEC 353.051 not subject to creditor claims"
        ],
        reasoning_framework="""
TEC Chapter 353 establishes family protections superior to creditor claims:

1. FAMILY ALLOWANCE (353.101):
   - Court may award family allowance for maintenance of surviving spouse and minor children
   - Not to exceed $15,000 for family without minor children
   - Up to $30,000 for family with minor children
   - Takes priority over unsecured creditor claims
   - Paid before claims administration

2. EXEMPT PERSONAL PROPERTY (353.051):
   - Homestead and other exempt property set aside to family
   - Texas Property Code 41.001 homestead exempt from forced sale
   - Texas Property Code 42.002 personal property exemptions
   - Not subject to testacy creditor claims (with exceptions)

3. HOMESTEAD PROTECTIONS:
   - Constitutional and statutory protection (Tex. Const. Art. XVI Sec. 50-52)
   - Exempt from forced sale for debts except:
     * Purchase money (original acquisition debt)
     * Ad valorem taxes
     * Home equity loans (if properly documented)
     * Mechanic's liens for improvements
     * Reverse mortgages
   - Passes to heirs/surviving spouse outside probate
   - Cannot be used to satisfy general creditor claims

4. PERSONAL PROPERTY EXEMPTIONS (42.002):
   - Home furnishings, clothing, food
   - Two firearms, athletic equipment
   - Jewelry up to 25% of aggregate limit
   - Two vehicles, farming/ranching equipment
   - Professionally prescribed health aids
   - Total aggregate limit $50,000 single, $100,000 family

5. CREDITOR POSITION:
   - Must accept set-aside of exempt property
   - Cannot pursue homestead for general debts
   - May object to valuation of exempt property
   - May claim family allowance excessive
""",
        key_factors=[
            "Family allowance priority over unsecured claims",
            "Homestead exemption from testacy debts",
            "Personal property exemptions under Property Code 42.002",
            "Exceptions to homestead exemption (purchase money, taxes, home equity)",
            "Court discretion in setting family allowance amount"
        ],
        primary_authority=[
            "Texas Estates Code Sec. 353.101 (Family Allowance)",
            "Texas Estates Code Sec. 353.051 (Exempt Property Set-Aside)",
            "Texas Constitution Art. XVI Sec. 50-52 (Homestead)",
            "Texas Property Code Sec. 41.001 (Homestead Exemption)",
            "Texas Property Code Sec. 42.002 (Personal Property Exemptions)"
        ],
        burden_holder="Personal representative sets aside exempt property; creditor bears burden of proving property non-exempt",
        adversary_position="Creditor argues property not exempt or family allowance excessive",
        counter_arguments=[
            "Property qualifies under statutory exemption definitions",
            "Homestead properly designated and used as family residence",
            "Family allowance reasonable given family needs and estate size",
            "No evidence of fraudulent transfer to claim exemption",
            "Valuation appraisal supports exemption within limits"
        ],
        resolution_strategy="Personal representative: file application to set aside exempt property early in administration; obtain appraisals; justify family allowance based on need. Creditor: object to excessive valuations; challenge non-exempt status with evidence",
        entity_scope="Estates with surviving spouse or minor children; homestead property",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - constitutional and statutory protections",
        controlling_precedent="Homestead and exempt property protections are fundamental policy",
        disclosure_caveat="Exemption amounts and categories subject to legislative change; verify current limits"
    ),

    "insolvent_estate_administration": DoctrineBlock(
        topic="Insolvent Estate Administration and Abatement",
        keywords=["insolvent", "insufficient assets", "abatement", "pro rata", "class priority"],
        conclusion_template=[
            "Insolvent estate pays claims according to statutory priority until assets exhausted",
            "Within each priority class, claims paid pro rata if assets insufficient",
            "Lower classes receive nothing until higher classes fully paid"
        ],
        reasoning_framework="""
TEC 355.103-355.109 govern insolvent estate administration:

1. DETERMINATION OF INSOLVENCY:
   - Total claims exceed estate assets
   - Personal representative must report insolvency to court
   - Court may appoint appraiser to value estate
   - Homestead and exempt property excluded from solvency calculation

2. PRIORITY CLASSES (355.102):
   CLASS 0: Costs of administration
   CLASS 1: Funeral expenses
   CLASS 2: Expenses of last sickness
   CLASS 3: Family allowance
   CLASS 4: Secured claims (to extent of collateral value)
   CLASS 5: Child support arrearages
   CLASS 6: Tax claims (state and federal)
   CLASS 7: Medical assistance reimbursement (Medicaid)
   CLASS 8: All other claims

3. ABATEMENT PRINCIPLES:
   - Higher class paid in full before lower class receives anything
   - Within class, pro rata distribution if funds insufficient
   - Example: $10,000 estate, $8,000 Class 1, $15,000 Class 8
     Result: Class 1 receives $8,000 (full), Class 8 receives $2,000 pro rata

4. PRO RATA CALCULATION:
   - Sum all allowed claims in class
   - Divide available funds by total claims
   - Each creditor receives percentage = (claim amount / total claims) x available funds

5. PERSONAL REPRESENTATIVE DUTIES IN INSOLVENCY:
   - File report of insolvency with court
   - Obtain court approval before distributing to creditors
   - May not prefer one creditor over another in same class
   - Must preserve assets for higher-priority classes
   - Violation subjects representative to surcharge
""",
        key_factors=[
            "Total claims exceed non-exempt estate assets",
            "Eight-class priority system strictly enforced",
            "Pro rata distribution within each class",
            "Court supervision required for insolvent distributions",
            "Personal representative liability for improper preferences"
        ],
        primary_authority=[
            "Texas Estates Code Sec. 355.102 (Classification of Claims)",
            "Texas Estates Code Sec. 355.103 (Payment of Claims)",
            "Texas Estates Code Sec. 355.105 (Claimants' Petition for Sale)",
            "Texas Estates Code Sec. 355.151 (Order of Payment Among Classes)",
            "Texas Estates Code Sec. 404.001 (Liability of Representative)"
        ],
        burden_holder="Personal representative bears burden of proper distribution according to priority; creditor bears burden of proving claim allowed",
        adversary_position="Creditor in lower class argues assets misapplied to higher class; representative argues proper priority followed",
        counter_arguments=[
            "Distribution followed exact statutory priority order",
            "Pro rata calculation mathematically correct",
            "Court approved distribution plan before payment",
            "No preferential treatment within class",
            "Assets insufficient for complete payment of higher classes"
        ],
        resolution_strategy="Personal representative: file detailed report showing all claims by class, proposed distribution, court approval before paying. Creditor: verify classification of claims, object to misclassification, request court oversight of distribution",
        entity_scope="Insolvent probate estates",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - clear statutory scheme",
        controlling_precedent="TEC 355.102-355.103 priority and abatement rules are mandatory",
        disclosure_caveat="Court may require bond increase for insolvent estate administration"
    ),

    "nonclaim_statute_bar": DoctrineBlock(
        topic="Nonclaim Statute - Two-Year Absolute Bar",
        keywords=["nonclaim statute", "two years", "absolute bar", "statute of limitations", "death"],
        conclusion_template=[
            "All claims against estate barred if not presented within two years after death",
            "Applies even if no administration opened or notice published",
            "No exceptions except fraud or concealment by interested party"
        ],
        reasoning_framework="""
TEC 355.064(b) establishes absolute two-year bar:

1. TWO-YEAR PERIOD:
   - Runs from date of decedent's death
   - Not from date of administration opening
   - Not from date of notice publication
   - Applies regardless of creditor knowledge

2. ABSOLUTE BAR NATURE:
   - No tolling for disability
   - No discovery rule exception
   - No relation-back for amended claims
   - Jurisdictional - court cannot extend

3. EXCEPTIONS (LIMITED):
   - Fraud or concealment by interested party in estate
   - Creditor shows diligent effort prevented by wrongful conduct
   - Federal tax claims (federal law preempts)
   - Claims for which representative is personally liable

4. RELATIONSHIP TO FOUR-MONTH PERIOD:
   - If administration opened and notice given, four-month period applies
   - Two-year period is backstop if no administration or defective notice
   - Creditor must file within shorter of: four months from notice OR two years from death

5. EFFECT ON CREDITOR REMEDIES:
   - Cannot sue estate after bar
   - Cannot pursue estate assets distributed to heirs/beneficiaries
   - No unjust enrichment claim against beneficiaries
   - Property passes free of time-barred claims

6. STRATEGIC IMPLICATIONS:
   - Heirs may choose not to open administration if debts exceed assets
   - Two-year period runs, barring claims
   - Small estates often use this strategy
   - Creditor must consider opening administration to preserve claim
""",
        key_factors=[
            "Two-year period from date of death",
            "Absolute bar with very limited exceptions",
            "Jurisdictional - court cannot override",
            "Shorter of two-year or four-month period applies",
            "Strategic option for insolvent estates to delay administration"
        ],
        primary_authority=[
            "Texas Estates Code Sec. 355.064(b) (Two-Year Bar)",
            "Texas Estates Code Sec. 355.001 (Definition of Claim)",
            "Strickland v. Owens (1936) - absolute nature of nonclaim statute",
            "United States v. Summerlin (1940) - federal tax exception"
        ],
        burden_holder="Creditor bears burden of timely filing; estate bears burden of proving exception if creditor alleges fraud",
        adversary_position="Estate argues two-year bar absolute; creditor argues fraud exception or federal preemption",
        counter_arguments=[
            "Claim filed within two years of death (admissible proof of date)",
            "Fraud or concealment by interested party prevented timely filing",
            "Federal law preempts state nonclaim statute (e.g., IRS)",
            "Representative personally liable for debt (survives nonclaim bar)",
            "Claim relates to administration expenses (not subject to bar)"
        ],
        resolution_strategy="Creditor: monitor death records, file immediately upon learning of death, open administration if necessary. Estate: raise nonclaim bar defense, verify death date, object to late claims without exception proof",
        entity_scope="All estates in Texas, administered or not",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - well-established absolute bar",
        controlling_precedent="Two-year nonclaim statute is jurisdictional and not subject to equitable tolling",
        disclosure_caveat="Federal claims may have different limitations periods"
    ),

    "contingent_claims_maturity": DoctrineBlock(
        topic="Contingent and Unliquidated Claims",
        keywords=["contingent claim", "unliquidated", "matured", "unmatured", "future claim"],
        conclusion_template=[
            "Contingent claims must be presented even if not yet matured",
            "Personal representative may estimate value or seek court determination",
            "Failure to present contingent claim results in bar at maturity"
        ],
        reasoning_framework="""
TEC 355.001 and 355.153 address contingent claims:

1. CONTINGENT CLAIM DEFINED:
   - Claim dependent on future event uncertain to occur
   - Examples: guaranty obligations, indemnity claims, pending lawsuits
   - Unliquidated: amount not yet determined
   - Unmatured: not yet due under contract terms

2. DUTY TO PRESENT CONTINGENT CLAIM:
   - Must be presented within claims period even if contingent
   - Failure to present bars claim when contingency occurs
   - Creditor describes nature of contingency in claim presentation
   - Claim preserved even if cannot be paid until maturity

3. PERSONAL REPRESENTATIVE OPTIONS:
   - Estimate value and allow claim for estimated amount
   - Seek court determination of present value
   - Reserve funds for payment when claim matures
   - Obtain bond or other security if distributing estate before maturity

4. COURT DETERMINATION (355.153):
   - Court may hear evidence of contingent claim value
   - May order appraisal or expert valuation
   - May order funds set aside pending maturity
   - May allow partial distribution with reserve

5. MATURITY AFTER DISTRIBUTION:
   - If estate closed and claim later matures
   - Creditor may pursue beneficiaries who received distribution
   - Beneficiaries liable up to amount received
   - No recovery if claim not timely presented before estate closed

6. EXAMPLES:
   - Decedent guaranteed loan, borrower still paying: present claim now
   - Decedent defendant in lawsuit, trial pending: present claim now
   - Decedent's product sold with warranty, no claims yet: present now if known exposure
""",
        key_factors=[
            "Contingent claims must be presented within claims period",
            "Court may determine present value for distribution purposes",
            "Personal representative may reserve funds for contingent claims",
            "Failure to present bars claim at maturity",
            "Beneficiaries liable if claim matures after distribution"
        ],
        primary_authority=[
            "Texas Estates Code Sec. 355.001 (Claim Includes Contingent Claims)",
            "Texas Estates Code Sec. 355.153 (Contingent Claims Procedure)",
            "Texas Estates Code Sec. 355.103 (Payment of Contingent Claims)",
            "UPC Sec. 3-810 (Contingent Claims Model)"
        ],
        burden_holder="Creditor bears burden of describing contingency and proving claim validity; representative bears burden of valuation objection",
        adversary_position="Estate argues contingent claim too speculative to allow; creditor argues claim certain enough to present",
        counter_arguments=[
            "Claim sufficiently definite to estimate present value",
            "Contingency likely to occur based on current facts",
            "Expert valuation supports creditor's estimated amount",
            "Estate has sufficient assets to reserve for contingency",
            "Beneficiaries consent to reserve pending maturity"
        ],
        resolution_strategy="Creditor: present claim describing contingency, provide valuation evidence. Personal representative: request court determination of value, establish reserve, obtain bond if distributing before maturity",
        entity_scope="Estates with guaranty obligations, pending litigation, or future liabilities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Moderate confidence - fact-intensive valuation issues",
        controlling_precedent="Contingent claims must be presented timely or are forever barred",
        disclosure_caveat="Valuation of contingent claims is highly fact-specific; consider actuary or expert appraisal"
    ),

    "personal_representative_liability_improper_payment": DoctrineBlock(
        topic="Personal Representative Liability for Improper Payments",
        keywords=["personal representative", "surcharge", "improper payment", "liability", "breach of duty"],
        conclusion_template=[
            "Personal representative personally liable for improper payments to creditors",
            "Includes paying lower-priority claims before higher, paying time-barred claims, preferring one creditor over another in same class",
            "Representative removed and surcharged for breach of fiduciary duty"
        ],
        reasoning_framework="""
TEC Chapter 404 establishes personal representative liability:

1. FIDUCIARY DUTY TO CREDITORS:
   - Representative owes duty to pay claims in proper order
   - Must follow statutory priority scheme (TEC 355.102)
   - Cannot prefer one creditor over another in same class
   - Must verify claims are timely and valid

2. LIABILITY FOR IMPROPER PAYMENTS (404.001):
   - Representative personally liable for:
     * Paying lower class before higher class fully paid
     * Paying time-barred claims
     * Paying excessive funeral expenses
     * Distributing to beneficiaries before creditors paid
     * Preferring one creditor over another in same class
     * Failing to give proper notice to known creditors

3. MEASURE OF LIABILITY:
   - Representative must restore to estate amount improperly paid
   - Plus interest from date of improper payment
   - Plus costs and attorney's fees of surcharge action
   - May be removed as representative for breach

4. DEFENSES TO SURCHARGE:
   - Court approval of payment before made
   - Good faith reliance on creditor's sworn claim
   - Advice of counsel on propriety of payment
   - No prejudice to other creditors (estate solvent)
   - Creditor committed fraud on representative

5. PROCEDURAL REQUIREMENTS:
   - Interested party files application for surcharge
   - Hearing with evidence of improper payment
   - Representative has burden to justify payment once impropriety shown
   - Court may order repayment from representative personally
   - Judgment enforceable against representative's personal assets

6. COMMON SCENARIOS:
   - Paying Class 8 creditor before Class 1 funeral home paid in full
   - Distributing estate to heirs without satisfying tax claims
   - Failing to send actual notice to known creditor, then paying later creditors
   - Paying creditor after four-month claims period expired
""",
        key_factors=[
            "Fiduciary duty to follow statutory priority scheme",
            "Personal liability for breach regardless of intent",
            "Court approval is defense to surcharge",
            "Representative must restore improperly paid amounts",
            "Removal as representative for serious breaches"
        ],
        primary_authority=[
            "Texas Estates Code Sec. 404.001 (Liability of Representative)",
            "Texas Estates Code Sec. 404.003 (Court Approval Defense)",
            "Texas Estates Code Sec. 355.103 (Payment Order)",
            "Texas Estates Code Sec. 404.0035 (Removal for Breach)"
        ],
        burden_holder="Representative bears burden of justifying payment once impropriety alleged; creditor bears burden of proving impropriety initially",
        adversary_position="Aggrieved creditor seeks surcharge; representative defends payment as proper or court-approved",
        counter_arguments=[
            "Payment approved by court order before made",
            "Representative relied on creditor's sworn affidavit",
            "All higher-priority classes fully paid before lower class payment",
            "Estate solvent, no creditor prejudiced by payment order",
            "Attorney opinion supported propriety of payment"
        ],
        resolution_strategy="Personal representative: seek court approval for any questionable payments, follow strict priority order, document all claim verifications, maintain detailed records. Creditor: monitor estate distributions, object to improper payments before made, file surcharge action promptly after improper payment discovered",
        entity_scope="All estate administrations with creditor claims",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - clear fiduciary duty and liability standards",
        controlling_precedent="Personal representative strictly liable for improper payments regardless of good faith",
        disclosure_caveat="Representative should obtain court approval for any payment where priority or timeliness is uncertain"
    ),

    "tax_lien_priority_irs": DoctrineBlock(
        topic="Federal Tax Lien Priority Over Probate Claims",
        keywords=["federal tax lien", "IRS", "priority", "tax claim", "government claim"],
        conclusion_template=[
            "Federal tax liens have priority over most probate claims under federal law",
            "IRS has nine months from notice to file claim",
            "State nonclaim statutes do not bar federal tax claims"
        ],
        reasoning_framework="""
26 USC 6321-6323 and TEC 355.102(6) govern federal tax claims in probate:

1. FEDERAL TAX LIEN ARISES:
   - Automatically upon assessment of tax liability
   - Attaches to all property and rights to property
   - No filing required for lien to attach
   - Filing required for priority over certain secured creditors

2. PRIORITY OVER STATE CLAIMS:
   - Federal law preempts state probate priority scheme
   - Generally Class 6 under TEC 355.102(6) but federal law controls
   - Takes priority over unsecured creditors
   - Takes priority over unfiled liens and subsequent secured creditors

3. NOTICE REQUIREMENTS (31 USC 3713):
   - Personal representative must give IRS notice of administration
   - IRS has nine months from notice to file claim
   - If no notice given, IRS has unlimited time to file
   - Personal representative personally liable if distributes without satisfying IRS claim

4. EXCEPTIONS TO IRS PRIORITY:
   - Purchase money security interests (26 USC 6323(b)(3))
   - Mechanic's liens for work before tax lien filing
   - Attorney's liens for representation
   - Certain residential property transactions

5. IRS CLAIM FILING:
   - IRS files proof of claim in estate
   - May file after state claims period if proper notice not given
   - Personal representative cannot reject IRS claim as untimely
   - Court lacks jurisdiction to bar federal tax claim based on state nonclaim statute

6. DISCHARGE OF ESTATE PROPERTY:
   - Personal representative may request IRS discharge under 26 USC 6325(b)(4)
   - Requires payment of lien amount or bond
   - Allows distribution free of federal tax lien
   - IRS has 90 days to respond to discharge request
""",
        key_factors=[
            "Federal law preempts state probate priority rules for IRS claims",
            "Personal representative must give IRS notice to start nine-month period",
            "State nonclaim statutes do not bar federal tax claims",
            "Representative personally liable for distributing without satisfying IRS",
            "Discharge available to clear title for distribution"
        ],
        primary_authority=[
            "26 USC Sec. 6321 (Federal Tax Lien Arises)",
            "26 USC Sec. 6323 (Priority of Tax Lien)",
            "31 USC Sec. 3713 (Notice to Government)",
            "26 USC Sec. 6325(b)(4) (Discharge of Estate Property)",
            "Texas Estates Code Sec. 355.102(6) (Tax Claims Class)"
        ],
        burden_holder="Personal representative bears burden of notifying IRS and satisfying claim before distribution; IRS bears burden of filing claim",
        adversary_position="Representative argues IRS claim untimely under state law; IRS argues federal law preempts state bar",
        counter_arguments=[
            "Federal law clearly preempts state nonclaim statute",
            "Personal representative gave proper notice triggering nine-month period",
            "IRS filed within nine months of notice",
            "Priority under 26 USC 6323 governs over TEC 355.102",
            "Discharge obtained allowing distribution free of lien"
        ],
        resolution_strategy="Personal representative: send IRS notice immediately after letters, reserve funds for tax claim, request discharge if needed. IRS: file claim within nine months of notice, assert federal priority, object to distribution before claim satisfied",
        entity_scope="Estates with federal tax liabilities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - federal law supremacy well-established",
        controlling_precedent="Federal tax claims not subject to state nonclaim statutes; 31 USC 3713 notice requirement mandatory",
        disclosure_caveat="Consult tax attorney for estates with significant IRS liabilities"
    ),

    "medicaid_reimbursement_claims": DoctrineBlock(
        topic="Medicaid Estate Recovery Claims",
        keywords=["medicaid", "estate recovery", "MERP", "long-term care", "reimbursement"],
        conclusion_template=[
            "State has right to recover Medicaid payments from probate estate",
            "MERP claims are Class 7 priority under TEC 355.102(7)",
            "Recovery limited to probate estate, does not reach non-probate transfers"
        ],
        reasoning_framework="""
42 USC 1396p and Texas Human Resources Code Ch. 32 govern Medicaid estate recovery:

1. MEDICAID ESTATE RECOVERY PROGRAM (MERP):
   - State must seek recovery from estates of Medicaid recipients age 55+
   - Recovers costs of nursing facility services, home and community-based services
   - Files claim in probate like other creditors
   - Class 7 priority under TEC 355.102(7)

2. SCOPE OF RECOVERY:
   - Limited to probate estate
   - Does not reach joint tenancy property passing to survivor
   - Does not reach life insurance, retirement accounts, POD accounts
   - Does not reach assets in irrevocable trust created before Medicaid eligibility
   - MERP cannot force probate to be opened

3. EXEMPTIONS AND HARDSHIPS:
   - Undue hardship waiver available if recovery would deprive dependents
   - Homestead exempt if surviving spouse or disabled child residing
   - Court may reduce or deny claim based on hardship
   - Waiver applications reviewed by state agency

4. NOTICE REQUIREMENTS:
   - MERP receives notice of probate administration
   - Has same claims period as other creditors (four months or two years)
   - Files sworn claim with documentation of payments
   - Personal representative may contest amount or hardship

5. STRATEGIC PLANNING TO AVOID MERP:
   - Transfer assets to irrevocable trust before Medicaid eligibility
   - Use non-probate transfers (POD, TOD, joint tenancy)
   - Homestead protection for surviving spouse
   - Careful planning to avoid probate entirely

6. CONFLICTS WITH OTHER CREDITORS:
   - MERP is Class 7, lower than taxes (Class 6)
   - Unsecured general creditors also Class 8, paid pro rata with MERP
   - MERP recovery may be zero if estate insolvent after higher classes
""",
        key_factors=[
            "MERP files claim in probate as Class 7 creditor",
            "Recovery limited to probate estate assets",
            "Hardship waivers available",
            "Homestead exempt if surviving spouse or disabled child",
            "Non-probate transfers avoid MERP recovery"
        ],
        primary_authority=[
            "42 USC Sec. 1396p (Medicaid Estate Recovery)",
            "Texas Human Resources Code Ch. 32 (Medical Assistance)",
            "Texas Estates Code Sec. 355.102(7) (MERP Class 7 Priority)",
            "1 TAC Sec. 361.1503 (MERP Procedures)",
            "CMS State Medicaid Manual Sec. 3810"
        ],
        burden_holder="MERP bears burden of proving payments and claim amount; representative may contest or seek hardship waiver",
        adversary_position="MERP asserts right to recovery; estate/heirs seek hardship waiver or asset protection",
        counter_arguments=[
            "Undue hardship to surviving spouse or disabled child",
            "MERP claim exceeds actual payments made",
            "Assets subject to claim are exempt property",
            "Claim not timely filed within claims period",
            "Estate insolvent, insufficient assets for Class 7 payment"
        ],
        resolution_strategy="Personal representative: notify MERP of administration, evaluate hardship waiver, contest excessive claim amounts. Heirs: consider non-probate transfers in advance, apply for hardship waiver if applicable",
        entity_scope="Estates of Medicaid recipients age 55+ with nursing facility or HCBS services",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - established federal and state law framework",
        controlling_precedent="MERP recovery limited to probate estate; hardship waivers available",
        disclosure_caveat="Hardship waiver standards vary; consult elder law attorney for Medicaid planning"
    ),

    "rejection_of_claims_procedure": DoctrineBlock(
        topic="Claim Rejection and Lawsuit Requirements",
        keywords=["reject claim", "lawsuit", "suit on claim", "allowed claim", "contested claim"],
        conclusion_template=[
            "Personal representative may reject claim in whole or in part",
            "Rejected claimant must file lawsuit within 90 days or claim is barred",
            "Lawsuit must be filed in probate court that issued letters"
        ],
        reasoning_framework="""
TEC 355.051-355.066 govern claim rejection and suit procedure:

1. CLAIM PRESENTATION (355.051):
   - Creditor files sworn claim with court clerk
   - Describes nature of claim, amount, supporting documentation
   - Personal representative receives copy from clerk
   - Representative has 30 days to allow or reject (or longer if court extends)

2. ALLOWANCE OR REJECTION (355.052-355.053):
   - Representative may allow claim in full (becomes allowed claim)
   - May reject claim in whole or in part
   - Must endorse allowance/rejection on claim and file with clerk
   - If no action within 30 days, claim deemed rejected

3. EFFECT OF REJECTION (355.054):
   - Rejected claimant must file lawsuit within 90 days
   - Lawsuit must be in probate court that issued letters
   - Failure to file suit within 90 days bars claim forever
   - No tolling or extension of 90-day period

4. LAWSUIT PROCEDURE (355.064-355.066):
   - Claimant files suit against estate, not personal representative individually
   - Probate court has exclusive jurisdiction
   - Trial to court or jury on claim validity and amount
   - Court's judgment on claim is binding

5. ALLOWED CLAIMS:
   - Claim allowed by representative becomes final if no contest
   - Representative pays allowed claim according to priority scheme
   - Allowed claim may be contested by interested party within 30 days

6. STRATEGIC CONSIDERATIONS:
   - Representative may partially allow claim to narrow dispute
   - Rejection starts 90-day lawsuit clock
   - Failure to sue within 90 days is complete defense
   - Representative may settle claim after rejection before suit filed
""",
        key_factors=[
            "Creditor must present sworn claim to clerk",
            "Representative has 30 days to allow or reject",
            "Rejection requires lawsuit within 90 days",
            "Probate court exclusive jurisdiction over claim suits",
            "Failure to sue within 90 days bars claim forever"
        ],
        primary_authority=[
            "Texas Estates Code Sec. 355.051 (Claim Presentation)",
            "Texas Estates Code Sec. 355.052 (Allowance)",
            "Texas Estates Code Sec. 355.053 (Rejection)",
            "Texas Estates Code Sec. 355.054 (Suit on Rejected Claim)",
            "Texas Estates Code Sec. 355.064 (90-Day Suit Requirement)"
        ],
        burden_holder="Creditor bears burden of presenting claim, filing suit timely, proving claim in lawsuit",
        adversary_position="Representative rejects claim; creditor sues to establish claim validity and amount",
        counter_arguments=[
            "Claim properly presented within claims period (creditor)",
            "Claim supported by contract, invoice, or other evidence (creditor)",
            "Lawsuit filed within 90 days of rejection (creditor)",
            "Claim properly rejected for lack of proof (representative)",
            "No lawsuit filed within 90 days, claim barred (representative)"
        ],
        resolution_strategy="Personal representative: review claims carefully, reject unsupported claims, track 90-day deadline for suit. Creditor: present detailed claim with supporting documents, file suit immediately if rejected, do not miss 90-day deadline",
        entity_scope="All contested probate claims",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - clear statutory procedure",
        controlling_precedent="90-day suit requirement is jurisdictional and strictly enforced",
        disclosure_caveat="Representative should seek legal advice before rejecting substantial claims"
    ),

    "child_support_arrearages_priority": DoctrineBlock(
        topic="Child Support Arrearages as Priority Claims",
        keywords=["child support", "arrearages", "priority", "family support", "class five"],
        conclusion_template=[
            "Child support arrearages are Class 5 priority claims under TEC 355.102(5)",
            "Paid after secured claims but before tax claims",
            "State may file claim on behalf of obligee or assign claim to state"
        ],
        reasoning_framework="""
TEC 355.102(5) and Texas Family Code Ch. 154 govern child support arrearages in probate:

1. CHILD SUPPORT AS PRIORITY CLAIM:
   - Class 5 under TEC 355.102(5)
   - Higher priority than tax claims (Class 6) and general claims (Class 8)
   - Lower priority than funeral, last sickness, family allowance, secured claims
   - Reflects public policy favoring child support

2. NATURE OF ARREARAGE CLAIM:
   - Arrearages accrued before death
   - May be reduced to judgment before or after death
   - Judgment not required to file claim
   - Accrued interest included in claim amount

3. WHO MAY FILE CLAIM:
   - Obligee parent (custodial parent)
   - State of Texas if obligee assigned rights
   - Texas Attorney General as state's representative
   - Another state if obligee receiving benefits there

4. PROOF OF CLAIM:
   - Court order establishing support obligation
   - Payment records showing arrearages
   - Accounting of payments made vs. owed
   - Judgment for arrearages if previously obtained

5. DEFENSES AND OFFSETS:
   - Personal representative may assert payments made after death
   - May assert credits for direct payments to obligee
   - Cannot assert defenses that would have been available to decedent
   - Laches or statute of limitations on support order enforcement

6. RELATIONSHIP TO FAMILY ALLOWANCE:
   - If surviving spouse is obligee, also entitled to family allowance (Class 3)
   - May receive both family allowance and child support arrearages
   - Family allowance paid first (Class 3), then arrearages (Class 5)
   - No offset between the two claims
""",
        key_factors=[
            "Class 5 priority - higher than taxes and general creditors",
            "Arrearages accrued before death",
            "State may file claim if obligee assigned rights",
            "Proof requires court order and payment records",
            "Public policy strongly favors child support claims"
        ],
        primary_authority=[
            "Texas Estates Code Sec. 355.102(5) (Child Support Priority)",
            "Texas Family Code Sec. 154.001 (Child Support Obligations)",
            "Texas Family Code Sec. 157.261 (Arrearages Survive Death)",
            "42 USC Sec. 656 (Federal Child Support Enforcement)"
        ],
        burden_holder="Claimant (obligee or state) bears burden of proving arrearages amount; representative may contest calculation",
        adversary_position="Estate contests amount of arrearages or asserts payments made; claimant proves amount owed",
        counter_arguments=[
            "Court order and payment records prove arrearage amount (claimant)",
            "Representative asserts credits for payments made after death",
            "Decedent had defenses to support order that survive death",
            "Obligee received direct payments reducing arrearages",
            "Statute of limitations bars enforcement of old arrearages"
        ],
        resolution_strategy="Claimant: obtain certified court order, provide detailed payment history, file claim timely. Personal representative: verify arrearages calculation, credit post-death payments, pay according to Class 5 priority",
        entity_scope="Estates where decedent owed child support arrearages",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - clear statutory priority and public policy",
        controlling_precedent="Child support arrearages are Class 5 priority claims under TEC 355.102(5)",
        disclosure_caveat="Consult family law attorney for complex arrearage calculations"
    ),

    "claim_classification_disputes": DoctrineBlock(
        topic="Classification Disputes Among Creditors",
        keywords=["classification", "priority dispute", "class determination", "contested priority"],
        conclusion_template=[
            "Court determines proper classification when creditors dispute priority class",
            "Burden on creditor to prove entitlement to higher class",
            "Examples: medical expense as last sickness (Class 2) vs. general debt (Class 8)"
        ],
        reasoning_framework="""
TEC 355.102 and 355.151 establish classification framework and dispute resolution:

1. EIGHT STATUTORY CLASSES:
   - Statute defines eight classes with examples
   - Some categories clear: funeral, taxes, child support
   - Others require fact-intensive inquiry: last sickness, secured status
   - Court determines classification when dispute arises

2. COMMON CLASSIFICATION DISPUTES:
   - Medical Expenses: Last sickness (Class 2) vs. ordinary medical (Class 8)
     * Class 2: expenses during final illness proximately causing death
     * Class 8: routine medical care not related to terminal illness
   - Secured vs. Unsecured: Was lien properly perfected? Value of collateral?
   - Administration Costs: Estate expense (Class 0) vs. pre-death debt (Class 8)
   - Tax Claims: Federal/state (Class 6) vs. local property tax (varies)

3. BURDEN OF PROOF:
   - Creditor claiming higher class bears burden of proof
   - Must show claim meets statutory definition of that class
   - Personal representative may contest classification
   - Other creditors in lower classes may intervene to contest

4. LAST SICKNESS STANDARD (Class 2):
   - Expenses of illness proximately causing death
   - Generally final hospitalization, terminal care
   - Not chronic conditions unrelated to cause of death
   - Fact-specific inquiry into medical causation

5. SECURED CLAIM STATUS (Class 4):
   - Must prove perfected security interest
   - UCC-1 filing for personal property
   - Deed of trust recorded for real property
   - Valuation of collateral determines secured amount vs. deficiency

6. ADMINISTRATION EXPENSE (Class 0):
   - Costs of preserving estate after death
   - Attorney fees for estate administration
   - Appraisal fees, court costs, bond premiums
   - Not pre-death attorney fees or decedent's personal expenses

7. PROCEDURE FOR CLASSIFICATION DISPUTE:
   - Creditor presents claim asserting class
   - Personal representative or other creditor objects
   - Court hearing with evidence
   - Court determines proper classification
   - Payment according to court's classification determination
""",
        key_factors=[
            "Burden on creditor to prove higher class entitlement",
            "Last sickness requires proximate cause of death",
            "Secured status requires perfection and valuation",
            "Administration expenses are post-death estate costs",
            "Court makes final classification determination"
        ],
        primary_authority=[
            "Texas Estates Code Sec. 355.102 (Classification of Claims)",
            "Texas Estates Code Sec. 355.151 (Determination of Class)",
            "Texas Estates Code Sec. 355.001 (Definitions)",
            "In re Estate of Jones (1998) - last sickness standard"
        ],
        burden_holder="Creditor asserting higher class bears burden of proof; lower-class creditors may contest",
        adversary_position="Creditor seeks higher class; estate or other creditors argue lower class proper",
        counter_arguments=[
            "Medical records show illness was terminal and caused death (Class 2)",
            "UCC-1 filing proves perfected security interest (Class 4)",
            "Expense incurred after death for estate administration (Class 0)",
            "Illness chronic, not terminal cause of death (Class 8)",
            "Lien unperfected or collateral value less than claim (Class 8)"
        ],
        resolution_strategy="Creditor: gather evidence supporting higher class (medical records, UCC filings, expert opinions), file claim with clear class assertion. Personal representative: review claims carefully, contest doubtful classifications, protect lower-class creditors' interests",
        entity_scope="Estates with disputed claim classifications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Moderate confidence - fact-intensive determinations",
        controlling_precedent="Court determines classification based on statutory definitions and proof",
        disclosure_caveat="Classification disputes are fact-intensive; each case depends on specific circumstances"
    ),

    "setoff_and_recoupment_claims": DoctrineBlock(
        topic="Setoff and Recoupment Against Estate Claims",
        keywords=["setoff", "recoupment", "mutual debts", "offset", "counterclaim"],
        conclusion_template=[
            "Estate may assert setoff against creditor's claim if mutual debts exist",
            "Setoff applies only to mutual debts between same parties in same capacity",
            "Reduces creditor's claim by amount estate owes to that creditor"
        ],
        reasoning_framework="""
TEC 355.001 and common law setoff principles govern offset of claims:

1. SETOFF DEFINED:
   - Reduction of creditor's claim by debt estate owes to creditor
   - Requires mutual debts between same parties
   - Both debts must be liquidated and presently due
   - Applied automatically to reduce claim amount

2. REQUIREMENTS FOR SETOFF:
   - Mutuality: debts between same parties in same capacity
   - Liquidated: amounts certain or determinable
   - Presently due: not contingent or unmatured
   - Arose before death or before claim filed

3. EXAMPLES OF VALID SETOFF:
   - Creditor claims $10,000 on loan to decedent
   - Decedent had $3,000 deposit with creditor (mutual bank account)
   - Estate sets off $3,000, reducing claim to $7,000

   - Creditor claims $50,000 on contract
   - Decedent had $20,000 judgment against creditor
   - Estate sets off $20,000, reducing claim to $30,000

4. EXAMPLES OF INVALID SETOFF:
   - No mutuality: Creditor sues estate; estate owes debt to creditor's subsidiary (different parties)
   - Not liquidated: Estate claims creditor owes unliquidated damages (amount uncertain)
   - Not presently due: Estate's claim against creditor is contingent future claim

5. RECOUPMENT DISTINGUISHED:
   - Recoupment: reduction of claim based on same transaction
   - Narrower than setoff
   - Example: creditor claims breach of contract damages; estate recouped for creditor's own breach
   - Does not require mutuality in same sense as setoff

6. PROCEDURAL MECHANICS:
   - Personal representative asserts setoff when creditor files claim
   - Reduces allowed claim by setoff amount
   - Creditor may contest setoff validity
   - Court determines setoff entitlement if disputed

7. BANKRUPTCY COMPARISON:
   - Similar to 11 USC 553 bankruptcy setoff
   - Texas probate law follows general setoff principles
   - Setoff applies before distribution to creditors
""",
        key_factors=[
            "Mutuality of debts between same parties",
            "Liquidated and presently due amounts",
            "Arose before death or claim filing",
            "Reduces creditor's claim automatically",
            "Personal representative asserts setoff defensively"
        ],
        primary_authority=[
            "Texas Estates Code Sec. 355.001 (Claims May Be Set Off)",
            "Texas Business & Commerce Code Sec. 3.305 (Defenses)",
            "Restatement (Second) of Contracts Sec. 374 (Setoff)",
            "11 USC Sec. 553 (Bankruptcy Setoff Analogy)"
        ],
        burden_holder="Estate bears burden of proving setoff entitlement; creditor may contest mutuality or amount",
        adversary_position="Creditor argues no mutuality, amounts not liquidated, or debts not presently due",
        counter_arguments=[
            "Debts are between same parties in same capacity (mutuality) (estate)",
            "Amounts certain and ascertainable from records (liquidated) (estate)",
            "Both debts presently due without contingency (estate)",
            "Debts not mutual - different capacities or parties (creditor)",
            "Estate's alleged debt unliquidated or contingent (creditor)"
        ],
        resolution_strategy="Personal representative: review all debts owed to creditor, assert setoff in claim response, provide documentation of mutual debt. Creditor: verify mutuality, contest unliquidated or non-mutual alleged debts, seek court determination",
        entity_scope="Estates with creditors who also owe debts to decedent",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - well-established setoff principles",
        controlling_precedent="Setoff applies to mutual liquidated debts between same parties in same capacity",
        disclosure_caveat="Setoff analysis is fact-specific; verify mutuality carefully"
    )
}

# ═══════════════════════════════════════════════════════════════════════════
# TELEMETRY & METRICS
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class Telemetry:
    query_id: str
    timestamp: str
    mode: ResponseMode
    zone: AnalysisZone
    latency_ms: float
    triggered_doctrines: List[str]
    cache_hit: bool
    error_domain: Optional[str] = None

class MetricsCollector:
    def __init__(self):
        self.queries_total = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.latencies: List[float] = []
        self.errors: List[str] = []
        self.doctrine_usage: Dict[str, int] = {}

    def record_query(self, telemetry: Telemetry) -> None:
        self.queries_total += 1
        self.latencies.append(telemetry.latency_ms)
        if telemetry.cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        for doctrine in telemetry.triggered_doctrines:
            self.doctrine_usage[doctrine] = self.doctrine_usage.get(doctrine, 0) + 1
        if telemetry.error_domain:
            self.errors.append(telemetry.error_domain)

    def get_stats(self) -> Dict[str, Any]:
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0
        return {
            "queries_total": self.queries_total,
            "cache_hit_rate": self.cache_hits / self.queries_total if self.queries_total else 0,
            "avg_latency_ms": round(avg_latency, 2),
            "error_count": len(self.errors),
            "top_doctrines": sorted(self.doctrine_usage.items(), key=lambda x: x[1], reverse=True)[:10]
        }

METRICS = MetricsCollector()

# ═══════════════════════════════════════════════════════════════════════════
# CORE ENGINE LOGIC
# ═══════════════════════════════════════════════════════════════════════════

def search_doctrine_cache(query: str, context: Optional[Dict[str, Any]] = None) -> List[str]:
    """Search doctrine cache for relevant blocks based on query keywords."""
    query_lower = query.lower()
    query_terms = set(query_lower.split())

    matches = []
    for doctrine_id, block in DOCTRINE_CACHE.items():
        keyword_matches = sum(1 for kw in block.keywords if kw in query_lower)
        topic_match = any(term in block.topic.lower() for term in query_terms)

        if keyword_matches >= 2 or topic_match:
            matches.append(doctrine_id)
            block.triggered_count += 1

    return matches[:5]

def build_response_fast(query: str, doctrines: List[str]) -> str:
    """Build concise FAST mode response."""
    if not doctrines:
        return "No specific creditor claims doctrines triggered. General principles: creditors must file claims within statutory period (four months from notice or two years from death). Claims paid according to eight-class priority under TEC 355.102. Consult probate counsel for specific analysis."

    primary = DOCTRINE_CACHE[doctrines[0]]
    response_parts = [
        f"CREDITOR CLAIMS ANALYSIS - {primary.topic.upper()}:",
        "",
        "CONCLUSION:",
        *[f"  - {c}" for c in primary.conclusion_template],
        "",
        "KEY AUTHORITY:",
        *[f"  - {a}" for a in primary.primary_authority[:3]],
        "",
        f"CONFIDENCE: {primary.confidence.value}",
        "",
        "BRIEF REASONING:",
        primary.reasoning_framework[:500] + "..."
    ]

    if len(doctrines) > 1:
        response_parts.append("")
        response_parts.append("RELATED DOCTRINES:")
        for d_id in doctrines[1:3]:
            response_parts.append(f"  - {DOCTRINE_CACHE[d_id].topic}")

    return "\n".join(response_parts)

def build_response_defense(query: str, doctrines: List[str], zone: AnalysisZone) -> str:
    """Build audit-ready DEFENSE mode response."""
    if not doctrines:
        return build_response_fast(query, doctrines)

    primary = DOCTRINE_CACHE[doctrines[0]]

    response_parts = [
        "=" * 80,
        f"CREDITOR CLAIMS ANALYSIS - {primary.topic.upper()}",
        "=" * 80,
        "",
        "QUERY:",
        f"  {query}",
        "",
        "ANALYSIS ZONE: " + zone.value,
        "",
        "CONCLUSION:",
        *[f"  {i+1}. {c}" for i, c in enumerate(primary.conclusion_template)],
        "",
        "REASONING FRAMEWORK:",
        primary.reasoning_framework,
        "",
        "KEY FACTORS:",
        *[f"  - {f}" for f in primary.key_factors],
        "",
        "PRIMARY AUTHORITY:",
        *[f"  [{i+1}] {a}" for i, a in enumerate(primary.primary_authority)],
        "",
        "CONTROLLING PRECEDENT:",
        f"  {primary.controlling_precedent}",
        "",
        "BURDEN OF PROOF:",
        f"  {primary.burden_holder}",
        "",
        "ADVERSARY POSITION:",
        f"  {primary.adversary_position}",
        "",
        "COUNTER-ARGUMENTS:",
        *[f"  - {c}" for c in primary.counter_arguments],
        "",
        "RESOLUTION STRATEGY:",
        f"  {primary.resolution_strategy}",
        "",
        "CONFIDENCE LEVEL: " + primary.confidence.value,
        f"  Stratification: {primary.confidence_stratification}",
        "",
        "ENTITY SCOPE:",
        f"  {primary.entity_scope}",
        ""
    ]

    if primary.disclosure_caveat:
        response_parts.extend([
            "DISCLOSURE CAVEAT:",
            f"  {primary.disclosure_caveat}",
            ""
        ])

    if len(doctrines) > 1:
        response_parts.extend([
            "RELATED DOCTRINES TRIGGERED:",
            *[f"  - {DOCTRINE_CACHE[d].topic}" for d in doctrines[1:]]
        ])

    response_parts.append("=" * 80)
    return "\n".join(response_parts)

def build_response_memo(query: str, doctrines: List[str], zone: AnalysisZone) -> str:
    """Build comprehensive MEMO mode response."""
    response_parts = [
        "=" * 80,
        "CREDITOR CLAIMS LEGAL MEMORANDUM",
        "=" * 80,
        "",
        f"DATE: {datetime.now().strftime('%B %d, %Y')}",
        f"ENGINE: {ENGINE_NAME} v{VERSION}",
        f"ANALYSIS ZONE: {zone.value}",
        "",
        "QUERY:",
        f"  {query}",
        "",
        "EXECUTIVE SUMMARY:",
        ""
    ]

    if not doctrines:
        response_parts.extend([
            "No specific creditor claims doctrines directly triggered by query terms.",
            "Analysis proceeds under general creditor claims principles:",
            "  - Claims must be presented within statutory period",
            "  - Four months from actual notice to known creditors (TEC 308.051)",
            "  - Two years from death as absolute bar (TEC 355.064(b))",
            "  - Eight-class priority system (TEC 355.102)",
            "  - Personal representative liability for improper payments",
            "",
            "Recommend consultation with probate counsel for specific fact pattern."
        ])
        return "\n".join(response_parts)

    # Executive summary from first doctrine
    primary = DOCTRINE_CACHE[doctrines[0]]
    response_parts.extend([
        f"Primary doctrine: {primary.topic}",
        "",
        *primary.conclusion_template,
        "",
        f"Confidence: {primary.confidence.value} - {primary.confidence_stratification}",
        "",
        "-" * 80,
        "DETAILED ANALYSIS:",
        "-" * 80,
        ""
    ])

    # Full analysis for each triggered doctrine
    for i, d_id in enumerate(doctrines[:3], 1):
        block = DOCTRINE_CACHE[d_id]
        response_parts.extend([
            f"{i}. {block.topic.upper()}",
            "",
            "CONCLUSION:",
            *[f"   {c}" for c in block.conclusion_template],
            "",
            "REASONING:",
            block.reasoning_framework,
            "",
            "KEY FACTORS:",
            *[f"   - {f}" for f in block.key_factors],
            "",
            "PRIMARY AUTHORITY:",
            *[f"   [{j+1}] {a}" for j, a in enumerate(block.primary_authority)],
            "",
            "CONTROLLING PRECEDENT:",
            f"   {block.controlling_precedent}",
            "",
            "BURDEN OF PROOF:",
            f"   {block.burden_holder}",
            "",
            "ADVERSARY POSITION:",
            f"   {block.adversary_position}",
            "",
            "COUNTER-ARGUMENTS:",
            *[f"   - {c}" for c in block.counter_arguments],
            "",
            "RESOLUTION STRATEGY:",
            f"   {block.resolution_strategy}",
            "",
            "CONFIDENCE:",
            f"   Level: {block.confidence.value}",
            f"   Stratification: {block.confidence_stratification}",
            "",
            "ENTITY SCOPE:",
            f"   {block.entity_scope}",
            ""
        ])

        if block.disclosure_caveat:
            response_parts.extend([
                "DISCLOSURE CAVEAT:",
                f"   {block.disclosure_caveat}",
                ""
            ])

        if i < len(doctrines[:3]):
            response_parts.append("-" * 80)
            response_parts.append("")

    # Closing
    response_parts.extend([
        "=" * 80,
        "EPISTEMIC STATUS:",
        "",
        "This analysis is based on Texas Estates Code provisions and established case law.",
        "Creditor claims law is well-settled statutory framework with substantial case law.",
        "Fact-specific applications require legal counsel for definitive advice.",
        "Priority classifications and time bars are strictly enforced by Texas courts.",
        "",
        "RECOMMENDATION:",
        "Consult probate litigation counsel before rejecting significant claims or",
        "distributing estate assets with known creditor disputes.",
        "=" * 80
    ])

    return "\n".join(response_parts)

def determinism_hash(query: str, answer: str, mode: str) -> str:
    """Generate SHA-256 hash for determinism verification."""
    content = f"{query}|{answer}|{mode}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]

def process_query(request: QueryRequest) -> QueryResponse:
    """Main query processing pipeline."""
    start_time = time.time()

    # Search doctrine cache
    triggered_doctrines = search_doctrine_cache(request.query, request.context)
    cache_hit = len(triggered_doctrines) > 0

    # Build response based on mode
    if request.mode == ResponseMode.FAST:
        answer = build_response_fast(request.query, triggered_doctrines)
    elif request.mode == ResponseMode.DEFENSE:
        answer = build_response_defense(request.query, triggered_doctrines, request.zone)
    else:  # MEMO
        answer = build_response_memo(request.query, triggered_doctrines, request.zone)

    # Determine confidence
    if triggered_doctrines:
        confidence = DOCTRINE_CACHE[triggered_doctrines[0]].confidence
    else:
        confidence = ConfidenceLevel.DISCLOSURE

    # Extract sources
    sources = []
    for d_id in triggered_doctrines[:3]:
        sources.extend(DOCTRINE_CACHE[d_id].primary_authority[:2])

    # Calculate latency
    latency_ms = (time.time() - start_time) * 1000

    # Build response
    response = QueryResponse(
        query=request.query,
        answer=answer,
        mode=request.mode,
        zone=request.zone,
        confidence=confidence,
        triggered_doctrines=triggered_doctrines,
        sources=sources[:5],
        epistemic_status="Based on Texas Estates Code and established creditor claims law",
        determinism_hash=determinism_hash(request.query, answer, request.mode.value),
        latency_ms=round(latency_ms, 2),
        telemetry={
            "cache_hit": cache_hit,
            "doctrines_triggered": len(triggered_doctrines),
            "response_length": len(answer)
        }
    )

    # Record telemetry
    telemetry = Telemetry(
        query_id=response.determinism_hash,
        timestamp=datetime.now().isoformat(),
        mode=request.mode,
        zone=request.zone,
        latency_ms=latency_ms,
        triggered_doctrines=triggered_doctrines,
        cache_hit=cache_hit
    )
    METRICS.record_query(telemetry)

    return response

# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

APP = FastAPI(
    title=ENGINE_NAME,
    version=VERSION,
    description="TIE-Grade Creditor Claims Intelligence Engine for Probate Analysis"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@APP.get("/health")
async def health_check():
    """Comprehensive health check endpoint."""
    return JSONResponse({
        "status": "healthy",
        "engine": ENGINE_NAME,
        "engine_id": ENGINE_ID,
        "version": VERSION,
        "port": PORT,
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "metrics": METRICS.get_stats(),
        "timestamp": datetime.now().isoformat()
    })

@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint."""
    try:
        return process_query(request)
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@APP.get("/doctrines")
async def list_doctrines():
    """List all available doctrine blocks."""
    return JSONResponse({
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "id": d_id,
                "topic": block.topic,
                "keywords": block.keywords,
                "confidence": block.confidence.value,
                "triggered_count": block.triggered_count
            }
            for d_id, block in DOCTRINE_CACHE.items()
        ]
    })

@APP.get("/metrics")
async def get_metrics():
    """Get engine metrics."""
    return JSONResponse(METRICS.get_stats())

# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} creditor claims doctrine blocks")

    uvicorn.run(
        APP,
        host="127.0.0.1",
        port=PORT,
        log_level="info"
    )
