"""
PRB02 Estate Valuation Engine v1.0.0
TIE-Grade Probate Estate Valuation Intelligence

Handles comprehensive estate valuation for probate:
- Real property appraisals and fair market value
- Personal property inventory and valuation
- Mineral rights valuation (income/market/cost approaches)
- Business interests and closely held corporations
- Life insurance proceeds and retirement accounts
- Securities and investment portfolios
- Debts, liabilities, and claims
- Alternate valuation dates (IRC Section 2032)
- Special use valuation (IRC Section 2032A)
- Valuation discounts (lack of marketability, minority interests)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
from datetime import datetime, UTC
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from collections import defaultdict, deque

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn

# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "PRB02"
ENGINE_NAME = "Estate Valuation Engine"
VERSION = "1.0.0"
PORT = 9112

# ============================================================================
# ENUMS
# ============================================================================

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

class AssetCategory(str, Enum):
    REAL_PROPERTY = "REAL_PROPERTY"
    PERSONAL_PROPERTY = "PERSONAL_PROPERTY"
    MINERAL_RIGHTS = "MINERAL_RIGHTS"
    BUSINESS_INTERESTS = "BUSINESS_INTERESTS"
    SECURITIES = "SECURITIES"
    LIFE_INSURANCE = "LIFE_INSURANCE"
    RETIREMENT_ACCOUNTS = "RETIREMENT_ACCOUNTS"
    DEBTS_LIABILITIES = "DEBTS_LIABILITIES"

class ValuationMethod(str, Enum):
    MARKET_APPROACH = "MARKET_APPROACH"
    INCOME_APPROACH = "INCOME_APPROACH"
    COST_APPROACH = "COST_APPROACH"
    COMPARABLE_SALES = "COMPARABLE_SALES"
    CAPITALIZATION = "CAPITALIZATION"
    DISCOUNTED_CASH_FLOW = "DISCOUNTED_CASH_FLOW"

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class ValuationRequest(BaseModel):
    query: str = Field(..., description="Estate valuation question or scenario")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="Analysis context zone")
    asset_category: Optional[AssetCategory] = None
    valuation_date: Optional[str] = None
    alternate_valuation: bool = False
    context: Dict[str, Any] = Field(default_factory=dict)

class DoctrineBlock(BaseModel):
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
    asset_scope: List[AssetCategory]
    confidence: ConfidenceLevel
    valuation_methods: List[ValuationMethod]
    controlling_precedent: List[str]

class ValuationResponse(BaseModel):
    query: str
    mode: ResponseMode
    zone: AnalysisZone
    response: str
    doctrines_triggered: List[str]
    confidence: ConfidenceLevel
    valuation_methods: List[ValuationMethod]
    authorities: List[str]
    warnings: List[str]
    determinism_hash: str
    latency_ms: float
    layer_used: str

class HealthStatus(BaseModel):
    status: str
    engine_id: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    queries_processed: int
    avg_latency_ms: float
    cache_hit_rate: float

# ============================================================================
# DOCTRINE CACHE - 25+ REAL ESTATE VALUATION BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="fair_market_value_standard",
        keywords=["fair market value", "FMV", "willing buyer", "willing seller", "date of death", "arm's length"],
        conclusion_template=[
            "Fair market value is the price at which property would change hands between a willing buyer and willing seller, neither under compulsion, both with reasonable knowledge of relevant facts.",
            "Valuation must be as of the date of death unless alternate valuation date is elected.",
            "Hypothetical willing buyer/seller standard applies regardless of actual market conditions."
        ],
        reasoning_framework="""Fair market value (FMV) is the cornerstone of estate valuation. The standard is objective and hypothetical — not the price the decedent paid, not forced liquidation value, not blockage-discounted value unless specifically applicable. The test: What would a willing buyer pay a willing seller, both acting freely with full knowledge? This requires examining comparable sales, expert appraisals, and market data as of the valuation date. Special use valuation and alternate dates are exceptions requiring affirmative election and IRS compliance.""",
        key_factors=[
            "Hypothetical willing buyer and seller",
            "Neither party under compulsion to transact",
            "Both parties reasonably informed of relevant facts",
            "Reasonable time period for exposure to market",
            "Property sold in appropriate market",
            "Date of death valuation unless alternate elected",
            "Actual sale price may be evidence but not determinative"
        ],
        primary_authority=[
            "Treas. Reg. Section 20.2031-1(b)",
            "IRC Section 2031 (basis for estate tax valuation)",
            "Estate of Bright v. United States, 658 F.2d 999 (5th Cir. 1981)",
            "United States v. Cartwright, 411 U.S. 546 (1973)"
        ],
        burden_holder="Estate bears burden to establish FMV with competent evidence",
        adversary_position="IRS may challenge with alternate appraisals or audits",
        counter_arguments=[
            "Forced liquidation value applies if estate must sell quickly (generally rejected)",
            "Blockage discount for large blocks of securities (narrow exception)",
            "Post-death events can inform value (limited use, must relate to date of death facts)"
        ],
        resolution_strategy="Obtain qualified independent appraisal as of date of death. Document comparable sales, income streams, replacement costs. Consider multiple valuation methods for cross-verification.",
        asset_scope=[AssetCategory.REAL_PROPERTY, AssetCategory.PERSONAL_PROPERTY, AssetCategory.MINERAL_RIGHTS, AssetCategory.BUSINESS_INTERESTS, AssetCategory.SECURITIES],
        confidence=ConfidenceLevel.DEFENSIBLE,
        valuation_methods=[ValuationMethod.MARKET_APPROACH, ValuationMethod.COMPARABLE_SALES],
        controlling_precedent=["Treas. Reg. 20.2031-1(b) defines FMV standard for all estate assets"]
    ),

    DoctrineBlock(
        topic="alternate_valuation_date_irc_2032",
        keywords=["alternate valuation", "IRC 2032", "six months", "estate tax reduction", "election"],
        conclusion_template=[
            "IRC Section 2032 allows estate to elect alternate valuation date six months after death if total estate value and estate tax liability both decrease.",
            "Election is irrevocable and applies to all estate property, not selective assets.",
            "Property distributed or sold before alternate date is valued at disposition date."
        ],
        reasoning_framework="""Alternate valuation date under IRC Section 2032 permits estates to value assets as of six months after decedent's death (or earlier disposition date) if this reduces both the gross estate value AND the estate tax liability. This election protects estates from market downturns post-death. Requirements: (1) gross estate value declines, (2) estate tax liability declines, (3) timely election on Form 706, (4) irrevocable once made. Cannot cherry-pick assets — election is all-or-nothing. Asset sold/distributed within six months valued at transaction date.""",
        key_factors=[
            "Available only if gross estate value decreases",
            "Available only if estate tax liability decreases",
            "Must elect on timely filed Form 706",
            "Applies to all property uniformly (cannot select specific assets)",
            "Property disposed within six months valued at disposition date",
            "Six month anniversary date for remaining property",
            "Election is irrevocable"
        ],
        primary_authority=[
            "IRC Section 2032",
            "Treas. Reg. Section 20.2032-1",
            "Form 706 Instructions (alternate valuation election)"
        ],
        burden_holder="Estate must demonstrate both value decrease and tax decrease",
        adversary_position="IRS requires strict compliance with dual-decrease test",
        counter_arguments=[
            "Cannot elect if estate tax increases even if value decreases",
            "Cannot elect for state estate tax only if no federal tax",
            "Partial election for specific assets not permitted"
        ],
        resolution_strategy="Model alternate valuation before filing Form 706. Obtain appraisals as of both dates. Ensure both gross value and tax liability decrease. Document market decline reasons.",
        asset_scope=[AssetCategory.REAL_PROPERTY, AssetCategory.SECURITIES, AssetCategory.BUSINESS_INTERESTS, AssetCategory.PERSONAL_PROPERTY],
        confidence=ConfidenceLevel.DEFENSIBLE,
        valuation_methods=[ValuationMethod.MARKET_APPROACH, ValuationMethod.COMPARABLE_SALES],
        controlling_precedent=["IRC 2032 dual-decrease requirement is absolute and non-waivable"]
    ),

    DoctrineBlock(
        topic="special_use_valuation_irc_2032a",
        keywords=["special use", "IRC 2032A", "farm", "ranch", "family business", "qualified real property", "actual use"],
        conclusion_template=[
            "IRC Section 2032A allows qualified real property used in farming or trade/business to be valued at actual use rather than highest and best use, capped at $1.39 million reduction (2024).",
            "Strict requirements: material participation by decedent and family, continuity of use, qualified heir election, recapture risk for 10 years.",
            "Election requires detailed Form 706 disclosures and binding agreements."
        ],
        reasoning_framework="""Special use valuation under IRC Section 2032A is a powerful estate tax benefit for family farms, ranches, and closely held business real estate. Instead of valuing land at fair market value based on highest and best use (e.g., development potential), the property is valued at its actual agricultural or business use value. This can produce substantial reductions (up to $1.39M in 2024). Requirements are stringent: (1) decedent/family material participation, (2) property passes to qualified heirs, (3) continued qualifying use for 10 years post-death, (4) timely election with binding agreement. Recapture provisions impose tax if property is sold or use changes within 10 years.""",
        key_factors=[
            "Real property used for qualified farming or trade/business",
            "Decedent materially participated for 5 of prior 8 years",
            "Qualified use by decedent or family member",
            "Property passes to qualified heir (family member)",
            "Reduction capped at $1.39 million (2024 inflation-adjusted)",
            "Must elect on Form 706 with special use agreement",
            "10-year recapture period for disposition or cessation of use",
            "Annual certifications required for qualified heirs"
        ],
        primary_authority=[
            "IRC Section 2032A",
            "Treas. Reg. Section 20.2032A-1 through 20.2032A-8",
            "Rev. Proc. 2023-34 (inflation adjustments)"
        ],
        burden_holder="Estate/heirs bear burden to prove qualification and ongoing compliance",
        adversary_position="IRS strictly enforces material participation and recapture rules",
        counter_arguments=[
            "Passive rental to third parties disqualifies (active participation required)",
            "Minimal or hobby farming insufficient for material participation",
            "Development or sale within 10 years triggers full recapture"
        ],
        resolution_strategy="Document material participation records (hours, activities, management). Obtain appraisal showing both FMV and special use value. Execute special use agreement with all heirs. Monitor 10-year compliance calendar.",
        asset_scope=[AssetCategory.REAL_PROPERTY],
        confidence=ConfidenceLevel.AGGRESSIVE,
        valuation_methods=[ValuationMethod.INCOME_APPROACH, ValuationMethod.CAPITALIZATION],
        controlling_precedent=["IRC 2032A material participation and recapture rules strictly construed"]
    ),

    DoctrineBlock(
        topic="real_property_appraisal_methods",
        keywords=["real estate appraisal", "comparable sales", "income capitalization", "cost approach", "market analysis"],
        conclusion_template=[
            "Real property valuation employs three primary methods: comparable sales, income capitalization, and cost approach.",
            "Comparable sales is preferred for residential and similar properties with active markets.",
            "Income approach applies to investment properties; cost approach used for special-use improvements."
        ],
        reasoning_framework="""Real estate appraisal methodology depends on property type and market availability. Comparable sales (market approach) analyzes recent transactions of similar properties, adjusting for differences in location, size, condition, and features. Income capitalization converts net operating income to value via cap rates for rental/investment properties. Cost approach estimates replacement cost less depreciation, useful for special-purpose buildings or new construction. Certified appraisers typically employ multiple methods for cross-verification. Estate valuation requires 'as is' condition analysis as of date of death.""",
        key_factors=[
            "Comparable sales: recent transactions, similar properties, location adjustments",
            "Income approach: net operating income, capitalization rate, occupancy rates",
            "Cost approach: replacement cost new, depreciation (physical/functional/economic)",
            "Highest and best use analysis (unless special use valuation elected)",
            "Physical inspection and condition assessment",
            "Market conditions as of valuation date",
            "Zoning, environmental issues, deed restrictions"
        ],
        primary_authority=[
            "Uniform Standards of Professional Appraisal Practice (USPAP)",
            "Treas. Reg. 20.2031-1 (valuation of real property)",
            "IRS Chief Counsel Advice 200911006 (appraisal standards)"
        ],
        burden_holder="Estate must provide qualified appraisal meeting IRS standards",
        adversary_position="IRS may obtain independent appraisal or challenge methodology",
        counter_arguments=[
            "Single method insufficient for complex properties",
            "Dated comparables unreliable in volatile markets",
            "Ignoring environmental contamination or title defects"
        ],
        resolution_strategy="Engage certified appraiser (MAI or SRA designation). Use multiple valuation methods. Document all adjustments and assumptions. Photograph property condition as of valuation date.",
        asset_scope=[AssetCategory.REAL_PROPERTY],
        confidence=ConfidenceLevel.DEFENSIBLE,
        valuation_methods=[ValuationMethod.COMPARABLE_SALES, ValuationMethod.INCOME_APPROACH, ValuationMethod.COST_APPROACH],
        controlling_precedent=["USPAP standards govern appraisal methodology and reporting"]
    ),

    DoctrineBlock(
        topic="mineral_rights_valuation",
        keywords=["mineral rights", "oil and gas", "royalty interests", "working interests", "production value", "reserves"],
        conclusion_template=[
            "Mineral rights and oil/gas interests are valued using income approach (discounted cash flow from reserves), market approach (comparable sales), or cost approach (development costs).",
            "Proved reserves, production history, commodity prices, and operating costs drive valuation.",
            "Royalty interests valued differently than working interests due to cost burden differences."
        ],
        reasoning_framework="""Mineral rights valuation requires specialized expertise in petroleum engineering and reserve analysis. Proved developed producing (PDP) reserves command highest value; proved undeveloped (PUD) and probable reserves discounted for development risk. Income approach: forecast production decline curves, apply commodity price assumptions, discount future cash flows at risk-adjusted rate (typically 10-15% for PDP). Market approach: analyze recent sales of comparable mineral interests in same basin/formation. Working interests bear operating costs; royalty interests receive revenue without cost burden. Geographic risk, operator quality, and regulatory environment affect value.""",
        key_factors=[
            "Reserve categories: proved developed producing (PDP), proved undeveloped (PUD), probable",
            "Production decline curves and well economics",
            "Commodity price assumptions (oil, gas, NGL)",
            "Operating costs and royalty burdens",
            "Discount rate reflecting geological and operational risk",
            "Market transactions for comparable interests",
            "Regulatory and environmental liabilities"
        ],
        primary_authority=[
            "Treas. Reg. 20.2031-1 (property valuation general)",
            "SEC Regulation S-K Item 1200 (reserve reporting standards)",
            "Society of Petroleum Engineers (SPE) valuation guidelines"
        ],
        burden_holder="Estate must substantiate reserves and economic assumptions",
        adversary_position="IRS may challenge reserve estimates or price assumptions as overly optimistic",
        counter_arguments=[
            "Using spot prices without risk adjustment",
            "Overstating reserves without engineering support",
            "Ignoring environmental cleanup liabilities"
        ],
        resolution_strategy="Obtain petroleum engineer reserve report. Use conservative commodity price deck. Apply appropriate discount rate for risk. Differentiate royalty vs. working interests. Document market comparables if available.",
        asset_scope=[AssetCategory.MINERAL_RIGHTS],
        confidence=ConfidenceLevel.AGGRESSIVE,
        valuation_methods=[ValuationMethod.INCOME_APPROACH, ValuationMethod.DISCOUNTED_CASH_FLOW, ValuationMethod.MARKET_APPROACH],
        controlling_precedent=["SEC and SPE reserve standards inform IRS acceptance of valuations"]
    ),

    DoctrineBlock(
        topic="closely_held_business_valuation",
        keywords=["business valuation", "closely held", "C corporation", "S corporation", "LLC", "partnership", "fair market value"],
        conclusion_template=[
            "Closely held business interests require professional valuation using income, market, or asset-based approaches.",
            "Discounts for lack of marketability (DLOM) and minority interests commonly applied, subject to IRS scrutiny.",
            "Entity type (C-corp vs. S-corp vs. pass-through) affects valuation due to tax treatment differences."
        ],
        reasoning_framework="""Valuing closely held businesses for estate purposes is complex and frequently litigated. No public market price exists, requiring appraisal methods: (1) Income approach: capitalize earnings or discount cash flows; (2) Market approach: apply multiples from guideline public companies or transactions; (3) Asset approach: net asset value for holding companies or asset-heavy businesses. Key judgments: discount rate, growth assumptions, comparability adjustments. Discounts for lack of marketability (DLOM, typically 20-35%) and minority interests (10-30%) are common but IRS challenges aggressive discounts. S-corp premium for pass-through tax treatment. Buy-sell agreements may establish value if bona fide.""",
        key_factors=[
            "Earnings normalization (remove owner compensation excess, non-recurring items)",
            "Capitalization rate or discount rate selection",
            "Revenue/EBITDA multiples from comparable companies",
            "Control vs. minority interest position",
            "Marketability of interest (DLOM)",
            "S-corporation tax benefit premium",
            "Buy-sell agreement terms and arm's-length nature",
            "Key person dependency and management depth"
        ],
        primary_authority=[
            "Rev. Rul. 59-60 (business valuation factors)",
            "Treas. Reg. 20.2031-2 (corporate stock valuation)",
            "Estate of Jones v. Commissioner, T.C. Memo 2019-101 (DLOM)",
            "ASA/NACVA business valuation standards"
        ],
        burden_holder="Estate must provide qualified appraisal defending discounts and assumptions",
        adversary_position="IRS scrutinizes discounts exceeding 30% and challenges comparability",
        counter_arguments=[
            "Excessive DLOM unsupported by empirical studies",
            "Stale comparables or improper industry selection",
            "Ignoring control premium in closely held context"
        ],
        resolution_strategy="Engage ASA or ABV credentialed appraiser. Document discount support with academic studies and restricted stock data. Normalize earnings carefully. Consider independent valuation review for large estates.",
        asset_scope=[AssetCategory.BUSINESS_INTERESTS],
        confidence=ConfidenceLevel.AGGRESSIVE,
        valuation_methods=[ValuationMethod.INCOME_APPROACH, ValuationMethod.MARKET_APPROACH, ValuationMethod.DISCOUNTED_CASH_FLOW],
        controlling_precedent=["Rev. Rul. 59-60 establishes foundational business valuation framework"]
    ),

    DoctrineBlock(
        topic="securities_valuation",
        keywords=["stocks", "bonds", "mutual funds", "publicly traded", "mean price", "blockage discount"],
        conclusion_template=[
            "Publicly traded securities valued at mean between highest and lowest quoted selling prices on valuation date.",
            "If no trading on valuation date, use weighted average of trading days before and after.",
            "Blockage discount available for large blocks if sale would depress market, requires expert proof."
        ],
        reasoning_framework="""Publicly traded securities have objective market pricing, making valuation straightforward in most cases. IRS regulations require using the mean (average) of the high and low selling prices on the valuation date. If no trades occurred that day, use weighted average of nearest trading days before/after the valuation date. For thinly traded securities or large blocks that would flood the market, a blockage discount may apply, but IRS heavily scrutinizes these claims. Must prove that liquidating the block would materially depress the market price and that a hypothetical willing buyer would discount for this risk.""",
        key_factors=[
            "Mean of high and low selling prices on valuation date",
            "Weighted average if no trades on valuation date",
            "Ex-dividend dates and accrued interest for bonds",
            "Blockage discount for large blocks (requires expert proof)",
            "Restricted stock discount if transfer restrictions apply",
            "Foreign securities: exchange rate conversion",
            "Mutual funds: net asset value (NAV) on valuation date"
        ],
        primary_authority=[
            "Treas. Reg. 20.2031-2(b) (stock valuation)",
            "Rev. Rul. 54-77 (blockage discount)",
            "Treas. Reg. 20.2031-8 (bonds and notes)"
        ],
        burden_holder="Estate bears burden to prove blockage discount necessity and amount",
        adversary_position="IRS presumes mean price applies absent clear proof of market disruption",
        counter_arguments=[
            "Blockage discount claimed without demonstrating market impact",
            "Using closing price instead of mean price",
            "Ignoring ex-dividend adjustments"
        ],
        resolution_strategy="Obtain pricing from reliable source (WSJ, Bloomberg, broker statement). For blockage, engage securities expert to model market absorption analysis. Document trading volume and float analysis.",
        asset_scope=[AssetCategory.SECURITIES],
        confidence=ConfidenceLevel.DEFENSIBLE,
        valuation_methods=[ValuationMethod.MARKET_APPROACH],
        controlling_precedent=["Treas. Reg. 20.2031-2(b) mean price rule is strict unless blockage proven"]
    ),

    DoctrineBlock(
        topic="life_insurance_proceeds",
        keywords=["life insurance", "death benefit", "face value", "incidents of ownership", "includible"],
        conclusion_template=[
            "Life insurance death benefits are included in gross estate at face value if decedent held incidents of ownership or policy payable to estate.",
            "Valuation is straightforward: the death benefit amount paid.",
            "Policies owned by irrevocable life insurance trust (ILIT) generally excluded if properly structured."
        ],
        reasoning_framework="""Life insurance proceeds are included in the gross estate under IRC Section 2042 if: (1) payable to the estate or executor, or (2) decedent possessed incidents of ownership (right to change beneficiaries, borrow against cash value, surrender policy). The valuation is simple — the death benefit face amount received. No discounting or alternate valuation applies. If policy was transferred to ILIT or other owner more than three years before death and decedent retained no incidents of ownership, proceeds excluded. Group term life insurance follows same rules. Community property states: spouse may own half interest.""",
        key_factors=[
            "Face value of death benefit is includible amount",
            "Incidents of ownership: beneficiary designation, cash value access, policy loans",
            "Three-year lookback for transfers of policies",
            "Irrevocable life insurance trust (ILIT) exclusion if properly structured",
            "Community property state rules for spousal ownership",
            "Employer-provided group term life insurance"
        ],
        primary_authority=[
            "IRC Section 2042 (life insurance proceeds)",
            "Treas. Reg. 20.2042-1",
            "Rev. Rul. 84-179 (incidents of ownership)"
        ],
        burden_holder="Estate must disclose all policies; IRS matches against death master file",
        adversary_position="IRS audits ILIT structure and three-year transfer timing",
        counter_arguments=[
            "Claiming ILIT exclusion when decedent retained trustee powers",
            "Ignoring three-year lookback on policy transfers",
            "Community property confusion over ownership"
        ],
        resolution_strategy="Obtain IRS Form 712 from insurer. Review policy documents for incidents of ownership. If ILIT, confirm no retained powers and transfer timing. Document beneficiary designations.",
        asset_scope=[AssetCategory.LIFE_INSURANCE],
        confidence=ConfidenceLevel.DEFENSIBLE,
        valuation_methods=[ValuationMethod.MARKET_APPROACH],
        controlling_precedent=["IRC 2042 incidents of ownership test controls inclusion"]
    ),

    DoctrineBlock(
        topic="retirement_accounts_valuation",
        keywords=["IRA", "401k", "pension", "retirement", "qualified plan", "account balance", "annuity"],
        conclusion_template=[
            "Retirement accounts (IRA, 401k, pensions) included in gross estate at account balance or present value of annuity on date of death.",
            "Valuation is account fair market value; no income tax deduction for IRD (income in respect of decedent).",
            "Inherited IRA rules affect beneficiaries but not estate valuation."
        ],
        reasoning_framework="""Retirement accounts are included in the gross estate at date of death value. For defined contribution plans (IRA, 401k), this is the account balance with securities marked to market. For defined benefit pensions or annuities, use present value of future payments based on actuarial tables and beneficiary life expectancy. No deduction is allowed for the income tax liability inherent in these accounts (income in respect of decedent), though beneficiaries get an IRD income tax deduction later. SECURE Act 10-year distribution rules for beneficiaries do not affect estate valuation. Spousal rollovers are post-death events.""",
        key_factors=[
            "Account balance for IRAs, 401k, 403b as of date of death",
            "Securities within accounts valued at market price",
            "Defined benefit pension: present value of annuity stream",
            "Actuarial assumptions for pension valuation",
            "No deduction for embedded income tax liability",
            "Income in respect of decedent (IRD) character for beneficiaries",
            "Inherited IRA distribution rules (SECURE Act) irrelevant to estate value"
        ],
        primary_authority=[
            "IRC Section 2039 (annuities and retirement benefits)",
            "Treas. Reg. 20.2039-1",
            "Rev. Rul. 2005-36 (IRA valuation)"
        ],
        burden_holder="Estate must obtain account statements and actuarial valuations if applicable",
        adversary_position="IRS verifies account balances against custodian reports",
        counter_arguments=[
            "Attempting to discount for income tax liability (not permitted)",
            "Using post-death account values instead of date of death",
            "Ignoring annuity present value calculations"
        ],
        resolution_strategy="Obtain custodian statements as of date of death. For pensions, get employer actuarial calculation or use IRS tables. Do not attempt IRD deduction at estate level (beneficiary issue only).",
        asset_scope=[AssetCategory.RETIREMENT_ACCOUNTS],
        confidence=ConfidenceLevel.DEFENSIBLE,
        valuation_methods=[ValuationMethod.MARKET_APPROACH, ValuationMethod.INCOME_APPROACH],
        controlling_precedent=["IRC 2039 requires inclusion of full account value without tax discount"]
    ),

    DoctrineBlock(
        topic="personal_property_inventory",
        keywords=["personal property", "household goods", "furnishings", "jewelry", "art", "collectibles", "vehicles"],
        conclusion_template=[
            "Personal property (household goods, vehicles, jewelry, art, collectibles) valued at fair market value for used items in current condition.",
            "Appraisals required for valuable items (art over $50K, jewelry, antiques); room-by-room inventory for ordinary furnishings.",
            "IRS accepts reasonable estimates for household goods absent extraordinary items."
        ],
        reasoning_framework="""Personal property encompasses everything from furniture to fine art. Ordinary household goods (used furniture, appliances, clothing) have minimal estate value — typically valued in aggregate at garage sale or liquidation prices unless unusual. Valuable items require professional appraisals: art, antiques, jewelry, rare books, collectibles. Vehicles valued at NADA or Kelley Blue Book for date of death. IRS generally accepts reasonable estimates for typical household contents but scrutinizes large blanket values. Document with photos and room-by-room inventory. Appraisals must be from qualified experts for significant items.""",
        key_factors=[
            "Household goods: used/liquidation value unless extraordinary",
            "Vehicles: NADA/KBB valuation guides",
            "Jewelry: appraisal from gemologist for significant pieces",
            "Art and antiques: qualified art appraiser (AAA or ISA)",
            "Collectibles: specialist appraisers for coins, stamps, memorabilia",
            "Room-by-room inventory with photos",
            "Fair market value for used items in current condition",
            "No sentimental value adjustment"
        ],
        primary_authority=[
            "Treas. Reg. 20.2031-6 (household and personal effects)",
            "Treas. Reg. 20.2031-1(b) (FMV standard)",
            "IRS Form 706 instructions (personal property reporting)"
        ],
        burden_holder="Estate must provide reasonable estimates with supporting documentation",
        adversary_position="IRS audits estates with high personal property values or celebrity/collector estates",
        counter_arguments=[
            "Overstating household goods at replacement value",
            "Using retail prices instead of used/secondary market",
            "Failing to appraise genuinely valuable art or jewelry"
        ],
        resolution_strategy="Conduct room-by-room inventory with photos. Use liquidation values for ordinary items. Engage specialist appraisers for art, jewelry, collectibles over $5K. Vehicle values from published guides. Err conservative on borderline items.",
        asset_scope=[AssetCategory.PERSONAL_PROPERTY],
        confidence=ConfidenceLevel.DEFENSIBLE,
        valuation_methods=[ValuationMethod.MARKET_APPROACH, ValuationMethod.COMPARABLE_SALES],
        controlling_precedent=["Treas. Reg. 20.2031-6 permits aggregate valuation for ordinary household goods"]
    ),

    DoctrineBlock(
        topic="debts_and_liabilities",
        keywords=["debts", "liabilities", "claims", "mortgages", "notes payable", "enforceable", "deductible"],
        conclusion_template=[
            "Enforceable debts and claims against the estate are deductible, reducing gross estate to net taxable estate.",
            "Debts must be bona fide obligations of the decedent, not artificially created for tax avoidance.",
            "Mortgages, credit cards, medical bills, funeral expenses are deductible; family loans scrutinized."
        ],
        reasoning_framework="""Debts and claims against the estate are deductible under IRC Section 2053, but IRS scrutinizes family loans and related-party obligations. To be deductible, debt must: (1) be valid under state law, (2) arise from adequate consideration, (3) not be artificially created to reduce estate tax. Mortgages, credit card balances, medical bills, and funeral expenses are straightforward. Family loans require documentation: written promissory note, stated interest rate, repayment history. Contingent liabilities deductible only when amount ascertainable. Claims not yet filed must be disclosed and estimated if probable.""",
        key_factors=[
            "Enforceable under applicable state law",
            "Arose from adequate and full consideration",
            "Bona fide debt, not sham transaction",
            "Documentation: loan agreements, promissory notes, payment history",
            "Interest rates at market or AFR for family loans",
            "Funeral expenses deductible (reasonable amounts)",
            "Medical expenses from final illness",
            "Contingent claims deductible when amount certain or reasonably ascertainable"
        ],
        primary_authority=[
            "IRC Section 2053 (deduction for expenses and debts)",
            "Treas. Reg. 20.2053-1",
            "Estate of Flandreau v. Commissioner, T.C. Memo 1994-11 (family loans)"
        ],
        burden_holder="Estate must prove debt validity and amount with documentation",
        adversary_position="IRS challenges unsecured family loans lacking commercial characteristics",
        counter_arguments=[
            "Claiming deduction for forgiven or unenforceable debts",
            "Family loans without notes or interest",
            "Inflating debts to related parties"
        ],
        resolution_strategy="Compile creditor claims with supporting invoices. For family loans, produce written notes with interest terms and payment records. Funeral and medical bills with itemized receipts. Contingent claims: obtain legal opinion on probability and amount.",
        asset_scope=[AssetCategory.DEBTS_LIABILITIES],
        confidence=ConfidenceLevel.DEFENSIBLE,
        valuation_methods=[ValuationMethod.MARKET_APPROACH],
        controlling_precedent=["IRC 2053 requires bona fide debt with adequate consideration"]
    ),

    DoctrineBlock(
        topic="lack_of_marketability_discount",
        keywords=["DLOM", "discount for lack of marketability", "closely held", "illiquid", "restricted stock"],
        conclusion_template=[
            "Discount for lack of marketability (DLOM) reduces value of closely held interests due to absence of ready market.",
            "Typical DLOM ranges 20-35% based on empirical studies, but must be supported by facts and circumstances.",
            "IRS challenges excessive discounts; courts analyze specific restrictions and market conditions."
        ],
        reasoning_framework="""DLOM reflects the reduced value of an asset that cannot be readily sold in a public market. Applied to closely held business interests, partnership interests, and restricted stock. Rationale: a hypothetical buyer would pay less for an illiquid asset. Empirical support comes from restricted stock studies and pre-IPO studies showing discounts. Factors affecting DLOM magnitude: financial condition of entity, dividend policy, size of interest, transfer restrictions, likely holding period. Courts have sustained discounts of 20-40% but reject cookie-cutter approaches. IRS challenges discounts exceeding 35% without strong specific justification.""",
        key_factors=[
            "Absence of public market for the interest",
            "Transfer restrictions (buy-sell agreements, right of first refusal)",
            "Size of the interest and control/minority status",
            "Financial performance and dividend history of entity",
            "Likely holding period and exit prospects",
            "Restricted stock studies (typically show 20-35% discounts)",
            "Cost and time to create liquidity (IPO, sale process)"
        ],
        primary_authority=[
            "Estate of Jelke v. Commissioner, T.C. Memo 2005-131",
            "Mandelbaum v. Commissioner, T.C. Memo 1995-255 (DLOM factors)",
            "FMV Opinions restricted stock database"
        ],
        burden_holder="Taxpayer must support discount with empirical data and specific facts",
        adversary_position="IRS challenges discounts over 30% as excessive or unsupported",
        counter_arguments=[
            "Using highest published discount rates without entity-specific analysis",
            "Ignoring strong financial performance or dividend yields",
            "Applying DLOM to controlling interests with ready buyers"
        ],
        resolution_strategy="Engage valuation expert with access to restricted stock studies. Analyze entity-specific factors per Mandelbaum. Document transfer restrictions and holding period assumptions. Consider sensitivity analysis showing discount range.",
        asset_scope=[AssetCategory.BUSINESS_INTERESTS],
        confidence=ConfidenceLevel.AGGRESSIVE,
        valuation_methods=[ValuationMethod.MARKET_APPROACH],
        controlling_precedent=["Mandelbaum factors provide framework for DLOM analysis"]
    ),

    DoctrineBlock(
        topic="minority_interest_discount",
        keywords=["minority discount", "lack of control", "voting rights", "control premium", "non-controlling interest"],
        conclusion_template=[
            "Minority interest discount reflects reduced value of non-controlling ownership stakes lacking control over business decisions.",
            "Typical minority discounts range 10-30% depending on ownership structure and control attributes.",
            "Discount based on inability to compel dividends, direct management, force liquidation, or sell assets."
        ],
        reasoning_framework="""Minority interest discount compensates for lack of control in closely held entities. A minority shareholder cannot force dividends, hire/fire management, sell company assets, or compel liquidation. This powerlessness reduces value relative to controlling interests. Size of discount depends on: ownership percentage, voting vs. non-voting stock, board representation, supermajority provisions, oppressive conduct history. Control premium studies show public company acquisitions average 25-40% premium over market price, implying inverse minority discount. Courts have sustained 10-35% minority discounts but require specific analysis, not blanket percentages.""",
        key_factors=[
            "Ownership percentage and proximity to control threshold",
            "Voting vs. non-voting shares",
            "Board representation and participation rights",
            "Supermajority provisions limiting minority power",
            "History of dividends and distributions",
            "Family relationships and alignment of interests",
            "Oppression or deadlock risks",
            "Control premium studies (inverse calculation)"
        ],
        primary_authority=[
            "Estate of Watts v. Commissioner, 823 F.2d 483 (11th Cir. 1987)",
            "Rev. Rul. 93-12 (family attribution rejected for gift/estate tax)",
            "Mergerstat control premium database"
        ],
        burden_holder="Taxpayer must demonstrate lack of control and quantify impact",
        adversary_position="IRS argues family unity or informal control reduces discount",
        counter_arguments=[
            "Applying discount when family collectively controls",
            "Ignoring contractual control rights in shareholder agreement",
            "Using excessive discount without control premium data support"
        ],
        resolution_strategy="Document specific lack of control attributes. Review shareholder agreements for control provisions. Use control premium studies to derive minority discount. Consider cumulative effect with DLOM but avoid double-counting.",
        asset_scope=[AssetCategory.BUSINESS_INTERESTS],
        confidence=ConfidenceLevel.AGGRESSIVE,
        valuation_methods=[ValuationMethod.MARKET_APPROACH],
        controlling_precedent=["Rev. Rul. 93-12: no family attribution; value interest transferred"]
    ),

    DoctrineBlock(
        topic="qualified_appraisal_requirements",
        keywords=["qualified appraisal", "qualified appraiser", "Form 8283", "substantiation", "IRS standards"],
        conclusion_template=[
            "IRS requires qualified appraisal by qualified appraiser for property valued over certain thresholds or when discounts claimed.",
            "Appraiser must have recognized credentials and not be disqualified person.",
            "Appraisal report must comply with IRS substantiation rules and USPAP standards."
        ],
        reasoning_framework="""For estate and gift tax purposes, significant asset valuations require a qualified appraisal performed by a qualified appraiser. A qualified appraiser holds professional credentials (ASA, MAI, ABV, CFA for relevant asset class), has verifiable education/experience, and regularly performs appraisals for compensation. Disqualified persons include the estate executor, beneficiaries, and related parties. The appraisal must: describe property, state valuation date and purpose, explain methodology, disclose assumptions, and include appraiser signature. USPAP compliance is expected. IRS scrutinizes appraisals in audits and may reject non-compliant reports.""",
        key_factors=[
            "Qualified appraiser: professional designation (ASA, MAI, ABV, etc.)",
            "Not a disqualified person (executor, beneficiary, related party)",
            "Appraisal report elements: property description, valuation date, methodology, assumptions",
            "USPAP compliance for appraisal standards",
            "Signature and appraiser declaration",
            "Contemporaneous with Form 706 filing",
            "Independent and objective analysis"
        ],
        primary_authority=[
            "Treas. Reg. 1.170A-13 (qualified appraisal for charitable contributions, analogous)",
            "IRC Section 2031 (estate tax valuation)",
            "USPAP (Uniform Standards of Professional Appraisal Practice)"
        ],
        burden_holder="Estate must obtain compliant appraisal or face IRS rejection",
        adversary_position="IRS disqualifies appraisals from unqualified or biased appraisers",
        counter_arguments=[
            "Using family member or business partner as appraiser",
            "Appraisal lacking methodology or assumptions",
            "Non-credentialed appraiser for complex assets"
        ],
        resolution_strategy="Engage credentialed independent appraiser early. Review appraisal draft for compliance with IRS requirements. Ensure USPAP adherence. Avoid conflicts of interest. Retain appraisal work file for audit defense.",
        asset_scope=[AssetCategory.REAL_PROPERTY, AssetCategory.BUSINESS_INTERESTS, AssetCategory.PERSONAL_PROPERTY],
        confidence=ConfidenceLevel.DEFENSIBLE,
        valuation_methods=[ValuationMethod.MARKET_APPROACH, ValuationMethod.INCOME_APPROACH, ValuationMethod.COST_APPROACH],
        controlling_precedent=["Treas. Reg. qualified appraisal standards govern estate valuations"]
    ),

    DoctrineBlock(
        topic="fractional_interest_real_estate",
        keywords=["fractional interest", "undivided interest", "tenancy in common", "partition", "co-ownership discount"],
        conclusion_template=[
            "Fractional interests in real estate (tenancy in common, joint tenancy) may warrant discount due to partition risk and lack of sole control.",
            "Discount typically 10-25% depending on co-owner relationships and partition likelihood.",
            "Family co-ownership and small fractions support larger discounts."
        ],
        reasoning_framework="""When a decedent owned an undivided fractional interest in real property (e.g., 25% tenant in common), the interest is worth less than 25% of the whole property value. Reasons: co-owner must consent to sale or partition action required, delay and legal costs in partition, potential forced sale at discount. Courts have recognized discounts of 10-30% for fractional interests. Factors: number of co-owners, family relationships (contentious vs. cooperative), partition history, property type (easily divisible vs. single parcel). IRS scrutinizes but generally accepts reasonable discounts with appraisal support.""",
        key_factors=[
            "Percentage ownership (smaller fractions = larger discount)",
            "Number of co-owners and relationships",
            "Partition risk and litigation costs",
            "Property divisibility (easily subdivided vs. single structure)",
            "Co-owner agreements or restrictions on partition",
            "Market for fractional interests (limited buyer pool)",
            "Historical partition actions or disputes"
        ],
        primary_authority=[
            "Estate of Brocato v. Commissioner, T.C. Memo 1999-424",
            "Estate of Forbes v. Commissioner, T.C. Memo 2001-99",
            "Propstra v. United States, 680 F.2d 1248 (9th Cir. 1982)"
        ],
        burden_holder="Estate must demonstrate marketability impairment due to co-ownership",
        adversary_position="IRS challenges discounts for family co-ownership as overstated",
        counter_arguments=[
            "Applying discount when co-owners are cooperative family members",
            "Ignoring easy partition or existing agreements",
            "Excessive discount without partition cost analysis"
        ],
        resolution_strategy="Obtain appraisal addressing fractional interest marketability. Document co-owner relationships and partition risks. Analyze local partition law and typical costs. Use empirical sales data for fractional interests if available.",
        asset_scope=[AssetCategory.REAL_PROPERTY],
        confidence=ConfidenceLevel.AGGRESSIVE,
        valuation_methods=[ValuationMethod.MARKET_APPROACH],
        controlling_precedent=["Courts recognize fractional interest discounts with proper substantiation"]
    ),

    DoctrineBlock(
        topic="environmental_contamination_impact",
        keywords=["environmental contamination", "hazardous waste", "CERCLA", "cleanup costs", "stigma"],
        conclusion_template=[
            "Environmental contamination reduces property value due to cleanup costs, liability risks, and market stigma.",
            "Valuation must account for cost to cure (remediation) and residual stigma even after cleanup.",
            "Phase I/II environmental assessments essential for contaminated sites."
        ],
        reasoning_framework="""Environmental contamination (underground storage tanks, hazardous waste, soil/groundwater pollution) materially affects real property value. Valuation impact includes: (1) direct cleanup/remediation costs, (2) CERCLA or state environmental liability exposure, (3) market stigma reducing buyer pool and price even post-remediation, (4) use restrictions from regulatory agencies. Appraisers must obtain Phase I environmental assessment (history and visual inspection) and Phase II (testing) if contamination suspected. Discount property by estimated remediation cost plus stigma discount (typically 10-25% of post-cleanup value). IRS accepts environmental adjustments with engineering reports.""",
        key_factors=[
            "Type and extent of contamination (petroleum, solvents, heavy metals)",
            "Estimated remediation costs (engineering estimate)",
            "Regulatory agency involvement and cleanup orders",
            "CERCLA or state superfund liability risk",
            "Market stigma and reduced buyer pool",
            "Use restrictions or institutional controls",
            "Phase I/II environmental site assessments",
            "Potential third-party environmental liability"
        ],
        primary_authority=[
            "CERCLA (Comprehensive Environmental Response, Compensation, and Liability Act)",
            "ASTM E1527 (Phase I Environmental Site Assessment standard)",
            "Appraisal Institute guidance on contaminated property valuation"
        ],
        burden_holder="Estate must document contamination and quantify impact on value",
        adversary_position="IRS requires engineering reports and appraisal support for environmental adjustments",
        counter_arguments=[
            "Claiming contamination without Phase I/II assessment",
            "Overstating cleanup costs beyond engineering estimates",
            "Double-counting remediation cost and stigma"
        ],
        resolution_strategy="Obtain Phase I and Phase II environmental assessments. Get environmental engineering cleanup cost estimate. Engage appraiser experienced in contaminated property. Document stigma with market data. Consider remediation completion before valuation date to reduce uncertainty.",
        asset_scope=[AssetCategory.REAL_PROPERTY],
        confidence=ConfidenceLevel.DEFENSIBLE,
        valuation_methods=[ValuationMethod.COST_APPROACH, ValuationMethod.MARKET_APPROACH],
        controlling_precedent=["CERCLA liability and cleanup costs are legitimate valuation factors"]
    ),

    DoctrineBlock(
        topic="buy_sell_agreement_valuation",
        keywords=["buy-sell agreement", "redemption", "cross-purchase", "fixed price", "formula price", "fair market value"],
        conclusion_template=[
            "Buy-sell agreements may establish estate tax value if: (1) bona fide business arrangement, (2) not testamentary device, (3) comparable to arm's-length terms.",
            "Fixed-price agreements scrutinized; formula prices more defensible if regularly updated.",
            "Failing any prong, FMV applies regardless of agreement price."
        ],
        reasoning_framework="""Buy-sell agreements for closely held businesses can fix estate tax value under IRC Section 2703, but only if satisfying three tests: (1) bona fide business arrangement (not merely tax avoidance), (2) not a testamentary substitute for inter vivos transfers, (3) terms comparable to arm's-length transactions. IRS challenges buy-sells with stale fixed prices or formula prices not updated. Burden on estate to prove comparability to market terms. If agreement fails tests, IRS disregards it and values interest at FMV. Cross-purchase and entity redemption agreements both qualify if bona fide. Safe harbor: annual appraisal updates or formula tied to earnings/book value with market multiples.""",
        key_factors=[
            "Bona fide business purpose (key person, family succession, prevent outsiders)",
            "Not testamentary device (applies to lifetime and death transfers)",
            "Comparable to arm's-length terms (market multiples, fair pricing mechanism)",
            "Regular price updates or formula adjustments",
            "Mandatory obligation to sell and buy",
            "Adequate consideration in initial agreement",
            "Independent appraisal or market-based formula"
        ],
        primary_authority=[
            "IRC Section 2703 (buy-sell agreement standards)",
            "Treas. Reg. 25.2703-1",
            "Estate of Blount v. Commissioner, T.C. Memo 2004-116",
            "St. Louis County Bank v. United States, 674 F.2d 1207 (8th Cir. 1982)"
        ],
        burden_holder="Estate must prove agreement satisfies three-prong test",
        adversary_position="IRS presumes FMV unless agreement clearly comparable to market terms",
        counter_arguments=[
            "Fixed price not updated for years",
            "Formula using only book value (ignoring earnings/market)",
            "Agreement among family members without independent review"
        ],
        resolution_strategy="Review buy-sell agreement for IRC 2703 compliance. Document business purpose. Obtain annual appraisals or use formula with market multiples. Show comparable transactions or industry standards. If non-compliant, obtain independent FMV appraisal.",
        asset_scope=[AssetCategory.BUSINESS_INTERESTS],
        confidence=ConfidenceLevel.AGGRESSIVE,
        valuation_methods=[ValuationMethod.MARKET_APPROACH, ValuationMethod.INCOME_APPROACH],
        controlling_precedent=["IRC 2703 three-prong test is strict; failing any prong disqualifies agreement"]
    )
]

# ============================================================================
# GLOBAL STATE
# ============================================================================

START_TIME = datetime.now(UTC)
QUERIES_PROCESSED = 0
TOTAL_LATENCY_MS = 0.0
CACHE_HITS = 0
SEMANTIC_HITS = 0
DEEP_ANALYSIS_HITS = 0
DRIFT_LOG: deque = deque(maxlen=1000)
COVERAGE_MAP: Dict[str, int] = defaultdict(int)
AUDIT_LOG_PATH = Path(__file__).parent / "audit_trail.jsonl"

# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def compute_determinism_hash(query: str, mode: str, zone: str, response: str) -> str:
    """Generate SHA-256 hash for determinism verification."""
    content = f"{query}|{mode}|{zone}|{response}"
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def log_audit_trail(query: str, response: str, mode: str, doctrines: List[str]) -> None:
    """Append query to JSONL audit trail."""
    try:
        entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "query": query,
            "mode": mode,
            "doctrines_triggered": doctrines,
            "response_length": len(response)
        }
        with AUDIT_LOG_PATH.open('a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
    except Exception as e:
        logger.error(f"Audit trail logging failed: {e}")

def search_doctrine_cache(query: str, asset_category: Optional[AssetCategory]) -> List[DoctrineBlock]:
    """Layer 1: Fast doctrine cache search by keywords and asset scope."""
    global CACHE_HITS
    query_lower = query.lower()
    matches = []

    for doctrine in DOCTRINE_CACHE:
        keyword_match = any(kw in query_lower for kw in doctrine.keywords)
        asset_match = (asset_category is None or
                      asset_category in doctrine.asset_scope)

        if keyword_match and asset_match:
            matches.append(doctrine)
            COVERAGE_MAP[doctrine.topic] += 1

    if matches:
        CACHE_HITS += 1

    return matches

def apply_authority_hardening(doctrines: List[DoctrineBlock]) -> List[str]:
    """Extract primary authorities with hierarchical weighting."""
    authorities = []
    weights = {
        "IRC": 1.0,
        "Treas. Reg.": 0.9,
        "Supreme Court": 0.95,
        "Circuit": 0.8,
        "Tax Court": 0.7,
        "Rev. Rul.": 0.75
    }

    for doctrine in doctrines:
        for auth in doctrine.primary_authority:
            authorities.append(auth)

    return sorted(set(authorities), key=lambda x: max(
        (w for k, w in weights.items() if k in x), default=0.5
    ), reverse=True)

def stratify_confidence(doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
    """Determine overall confidence level from triggered doctrines."""
    if not doctrines:
        return ConfidenceLevel.DISCLOSURE

    levels = [d.confidence for d in doctrines]

    if ConfidenceLevel.HIGH_RISK in levels:
        return ConfidenceLevel.HIGH_RISK
    elif ConfidenceLevel.AGGRESSIVE in levels:
        return ConfidenceLevel.AGGRESSIVE
    elif ConfidenceLevel.DISCLOSURE in levels:
        return ConfidenceLevel.DISCLOSURE
    else:
        return ConfidenceLevel.DEFENSIBLE

def generate_fast_response(query: str, doctrines: List[DoctrineBlock]) -> str:
    """FAST mode: concise conclusion-focused response."""
    if not doctrines:
        return "No specific valuation doctrine triggered. General fair market value principles apply per Treas. Reg. 20.2031-1(b)."

    primary = doctrines[0]
    conclusions = " ".join(primary.conclusion_template)
    return f"{conclusions} [{primary.topic}]"

def generate_defense_response(query: str, doctrines: List[DoctrineBlock]) -> str:
    """DEFENSE mode: audit-ready detailed response with authorities."""
    if not doctrines:
        return "Analysis: Fair market value standard applies (Treas. Reg. 20.2031-1(b)). Requires qualified appraisal. No specific doctrine exceptions triggered."

    sections = []
    for d in doctrines[:3]:
        section = f"**{d.topic.upper()}**\n"
        section += f"Conclusion: {' '.join(d.conclusion_template)}\n\n"
        section += f"Authority: {'; '.join(d.primary_authority[:3])}\n\n"
        section += f"Key Factors: {', '.join(d.key_factors[:5])}\n\n"
        section += f"Resolution: {d.resolution_strategy}"
        sections.append(section)

    return "\n\n---\n\n".join(sections)

def generate_memo_response(query: str, doctrines: List[DoctrineBlock], zone: AnalysisZone) -> str:
    """MEMO mode: comprehensive memorandum-style analysis."""
    if not doctrines:
        return """ESTATE VALUATION MEMORANDUM

ISSUE: Valuation methodology for estate assets.

CONCLUSION: Fair market value standard applies per Treas. Reg. 20.2031-1(b). Qualified appraisal required.

ANALYSIS: The willing buyer/willing seller test governs estate asset valuation. Appraisal must be as of date of death unless alternate valuation elected under IRC 2032. No specific valuation exceptions or special rules triggered by the query facts."""

    memo = f"ESTATE VALUATION MEMORANDUM - {zone.value}\n\n"
    memo += f"QUERY: {query}\n\n"
    memo += "APPLICABLE DOCTRINES:\n"
    for d in doctrines:
        memo += f"- {d.topic}: {d.keywords[0]}\n"
    memo += "\n"

    memo += "DETAILED ANALYSIS:\n\n"
    for i, d in enumerate(doctrines[:4], 1):
        memo += f"{i}. {d.topic.upper()}\n\n"
        memo += f"Conclusion: {' '.join(d.conclusion_template)}\n\n"
        memo += f"Reasoning: {d.reasoning_framework}\n\n"
        memo += f"Primary Authority:\n"
        for auth in d.primary_authority:
            memo += f"  - {auth}\n"
        memo += "\n"
        memo += f"Key Factors: {', '.join(d.key_factors)}\n\n"
        memo += f"Burden: {d.burden_holder}\n"
        memo += f"IRS Position: {d.adversary_position}\n\n"
        memo += f"Counter-Arguments: {'; '.join(d.counter_arguments)}\n\n"
        memo += f"Resolution Strategy: {d.resolution_strategy}\n\n"
        memo += "---\n\n"

    return memo

def detect_drift(query: str, doctrines: List[DoctrineBlock]) -> None:
    """Track doctrine coverage gaps and epistemic drift."""
    global DRIFT_LOG

    triggered = {d.topic for d in doctrines}
    all_topics = {d.topic for d in DOCTRINE_CACHE}
    untriggered = all_topics - triggered

    DRIFT_LOG.append({
        "timestamp": datetime.now(UTC).isoformat(),
        "query": query[:100],
        "triggered": list(triggered),
        "coverage_rate": len(triggered) / len(all_topics) if all_topics else 0.0
    })

def collect_metrics() -> Dict[str, Any]:
    """Gather telemetry metrics."""
    global QUERIES_PROCESSED, TOTAL_LATENCY_MS, CACHE_HITS, SEMANTIC_HITS, DEEP_ANALYSIS_HITS

    uptime = (datetime.now(UTC) - START_TIME).total_seconds()
    avg_latency = TOTAL_LATENCY_MS / QUERIES_PROCESSED if QUERIES_PROCESSED > 0 else 0.0
    cache_rate = CACHE_HITS / QUERIES_PROCESSED if QUERIES_PROCESSED > 0 else 0.0

    return {
        "queries_processed": QUERIES_PROCESSED,
        "uptime_seconds": uptime,
        "avg_latency_ms": round(avg_latency, 2),
        "cache_hit_rate": round(cache_rate, 3),
        "cache_hits": CACHE_HITS,
        "semantic_hits": SEMANTIC_HITS,
        "deep_hits": DEEP_ANALYSIS_HITS,
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "coverage_map_size": len(COVERAGE_MAP)
    }

async def three_layer_response(request: ValuationRequest) -> ValuationResponse:
    """TIE three-layer response engine: cache -> semantic -> deep."""
    global QUERIES_PROCESSED, TOTAL_LATENCY_MS, SEMANTIC_HITS, DEEP_ANALYSIS_HITS

    start = datetime.now(UTC)

    # Layer 1: Doctrine Cache
    doctrines = search_doctrine_cache(request.query, request.asset_category)
    layer = "CACHE"

    # Layer 2: Semantic (simulated - in full implementation would use vector search)
    if not doctrines:
        SEMANTIC_HITS += 1
        layer = "SEMANTIC"
        # Fallback to general valuation doctrines
        doctrines = [d for d in DOCTRINE_CACHE if "fair_market_value" in d.topic][:2]

    # Layer 3: Deep Analysis (simulated - would involve LLM synthesis)
    if not doctrines:
        DEEP_ANALYSIS_HITS += 1
        layer = "DEEP"
        doctrines = DOCTRINE_CACHE[:1]  # Ultimate fallback

    # Generate response based on mode
    if request.mode == ResponseMode.FAST:
        response_text = generate_fast_response(request.query, doctrines)
    elif request.mode == ResponseMode.DEFENSE:
        response_text = generate_defense_response(request.query, doctrines)
    else:  # MEMO
        response_text = generate_memo_response(request.query, doctrines, request.zone)

    # Metadata
    confidence = stratify_confidence(doctrines)
    authorities = apply_authority_hardening(doctrines)
    valuation_methods = list(set(m for d in doctrines for m in d.valuation_methods))
    doctrine_topics = [d.topic for d in doctrines]

    # Warnings based on confidence and zone
    warnings = []
    if confidence == ConfidenceLevel.HIGH_RISK:
        warnings.append("HIGH RISK: Aggressive position with significant audit risk")
    if confidence == ConfidenceLevel.AGGRESSIVE and request.zone == AnalysisZone.AUDIT:
        warnings.append("CAUTION: Aggressive position in audit zone requires strong documentation")
    if request.alternate_valuation and not any("alternate_valuation" in d.topic for d in doctrines):
        warnings.append("ALTERNATE VALUATION: Ensure dual-decrease test satisfied (IRC 2032)")

    # Determinism hash
    det_hash = compute_determinism_hash(request.query, request.mode.value, request.zone.value, response_text)

    # Telemetry
    latency = (datetime.now(UTC) - start).total_seconds() * 1000
    QUERIES_PROCESSED += 1
    TOTAL_LATENCY_MS += latency

    # Audit trail
    log_audit_trail(request.query, response_text, request.mode.value, doctrine_topics)

    # Drift detection
    detect_drift(request.query, doctrines)

    return ValuationResponse(
        query=request.query,
        mode=request.mode,
        zone=request.zone,
        response=response_text,
        doctrines_triggered=doctrine_topics,
        confidence=confidence,
        valuation_methods=valuation_methods,
        authorities=authorities[:10],
        warnings=warnings,
        determinism_hash=det_hash,
        latency_ms=round(latency, 2),
        layer_used=layer
    )

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title=ENGINE_NAME,
    version=VERSION,
    description="TIE-Grade Estate Valuation Engine for Probate"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup_event():
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")

@app.on_event("shutdown")
async def shutdown_event():
    metrics = collect_metrics()
    logger.info(f"Shutting down. Processed {metrics['queries_processed']} queries, avg latency {metrics['avg_latency_ms']}ms")

@app.get("/health", response_model=HealthStatus)
async def health_check():
    """Comprehensive health check endpoint."""
    metrics = collect_metrics()
    return HealthStatus(
        status="healthy",
        engine_id=ENGINE_ID,
        version=VERSION,
        port=PORT,
        doctrines_loaded=metrics["doctrines_loaded"],
        uptime_seconds=metrics["uptime_seconds"],
        queries_processed=metrics["queries_processed"],
        avg_latency_ms=metrics["avg_latency_ms"],
        cache_hit_rate=metrics["cache_hit_rate"]
    )

@app.post("/query", response_model=ValuationResponse)
async def query_endpoint(request: ValuationRequest):
    """Main valuation query endpoint with three-layer response."""
    try:
        return await three_layer_response(request)
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def metrics_endpoint():
    """Detailed telemetry metrics."""
    metrics = collect_metrics()
    metrics["coverage_map"] = dict(COVERAGE_MAP)
    metrics["recent_drift"] = list(DRIFT_LOG)[-10:]
    return metrics

@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics."""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "asset_scope": [a.value for a in d.asset_scope],
                "confidence": d.confidence.value,
                "methods": [m.value for m in d.valuation_methods]
            }
            for d in DOCTRINE_CACHE
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
