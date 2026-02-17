"""
LM16 Wind/Solar Lease Engine - Doctrine Definitions Module
============================================================
Pre-compiled expert reasoning blocks for wind and solar lease
negotiation, structure analysis, and landowner protection.

Engine: LM16 | Port: 8516
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from loguru import logger


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------
class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class IssueCategory(str, Enum):
    WIND_LEASE_STRUCTURE = "wind_lease_structure"
    SOLAR_LEASE_STRUCTURE = "solar_lease_structure"
    PAYMENT_STRUCTURE = "payment_structure"
    SURFACE_USE = "surface_use"
    LANDOWNER_PROTECTION = "landowner_protection"
    OIL_GAS_COEXISTENCE = "oil_gas_coexistence"
    EASEMENT_STRUCTURE = "easement_structure"
    DECOMMISSIONING = "decommissioning"
    TAX_INCENTIVE = "tax_incentive"
    TEXAS_REGULATORY = "texas_regulatory"
    ERCOT_INTERCONNECTION = "ercot_interconnection"
    ENVIRONMENTAL_COMPLIANCE = "environmental_compliance"
    TRANSMISSION = "transmission"
    BATTERY_STORAGE = "battery_storage"
    ESTATE_PLANNING = "estate_planning"
    FINANCING = "financing"
    AGRICULTURAL = "agricultural"
    ACCOMMODATION_DOCTRINE = "accommodation_doctrine"
    SHADOW_FLICKER_NOISE = "shadow_flicker_noise"
    RESOURCE_ASSESSMENT = "resource_assessment"


class EntityScope(str, Enum):
    LANDOWNER = "landowner"
    DEVELOPER = "developer"
    LENDER = "lender"
    MINERAL_OWNER = "mineral_owner"
    SURFACE_OWNER = "surface_owner"
    MUNICIPALITY = "municipality"
    UTILITY = "utility"
    ERCOT = "ercot"
    STATE_AGENCY = "state_agency"
    FEDERAL_AGENCY = "federal_agency"


class BurdenHolder(str, Enum):
    DEVELOPER = "developer"
    LANDOWNER = "landowner"
    MINERAL_OWNER = "mineral_owner"
    SHARED = "shared"
    GOVERNMENT = "government"
    LENDER = "lender"


# ---------------------------------------------------------------------------
# DoctrineBlock
# ---------------------------------------------------------------------------
@dataclass
class DoctrineBlock:
    """A single pre-compiled doctrine reasoning block."""
    topic: str
    keywords: list[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: list[str]
    primary_authority: list[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: list[str]
    resolution_strategy: str
    entity_scope: str
    confidence: str
    confidence_stratification: str
    controlling_precedent: str
    issue_category: str = ""
    interaction_edges: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Doctrine Cache Builder
# ---------------------------------------------------------------------------
def build_doctrine_cache() -> list[DoctrineBlock]:
    """Build and return the complete doctrine cache for LM16."""
    doctrines: list[DoctrineBlock] = []

    # -----------------------------------------------------------------------
    # D01: Wind Lease Option Period Structure
    # -----------------------------------------------------------------------
    doctrines.append(DoctrineBlock(
        topic="wind_lease_option_period",
        keywords=["wind", "option", "period", "development", "extension", "term"],
        conclusion_template=(
            "Wind energy option periods typically run 2-5 years with 1-3 extension "
            "periods of 1-2 years each. Landowners should negotiate automatic "
            "termination if development milestones are not met, escalating option "
            "payments for extensions, and caps on total option duration."
        ),
        reasoning_framework=(
            "The option period allows the developer to conduct feasibility studies, "
            "secure permits, arrange financing, and obtain interconnection agreements "
            "before committing to full lease obligations. The key tension is developer "
            "need for flexibility versus landowner need to avoid indefinite tie-up of "
            "their property. Best practice is milestone-based extensions rather than "
            "automatic renewals. Option payments should escalate with each extension "
            "to incentivize timely development. The option agreement should specify "
            "exactly what activities are permitted during the option period, typically "
            "limited to meteorological testing, environmental surveys, and preliminary "
            "engineering. Landowners must ensure the option does not create an implied "
            "lease that triggers property tax reassessment or affects agricultural "
            "exemption status. Texas has no statutory framework governing wind option "
            "periods, so contract terms control entirely."
        ),
        key_factors=[
            "Initial option term length (2-5 years typical)",
            "Number and duration of extension periods",
            "Option payment amounts and escalation schedule",
            "Development milestone requirements for extension",
            "Permitted activities during option period",
            "Automatic termination triggers",
            "Effect on agricultural exemption status",
            "Memorandum of option recordation requirements",
        ],
        primary_authority=[
            "Texas Property Code Ch. 5 (conveyancing requirements)",
            "Texas Tax Code Sec. 23.51 (agricultural appraisal definitions)",
            "AWEA Model Wind Lease (option period provisions)",
            "Stoel Rives LLP Wind Energy Lease Handbook (2023 ed.)",
        ],
        burden_holder=BurdenHolder.DEVELOPER.value,
        adversary_position=(
            "Developer argues for maximum flexibility with long option periods and "
            "multiple automatic extensions to accommodate uncertain permitting and "
            "interconnection timelines."
        ),
        counter_arguments=[
            "Landowner property is tied up without productive use for years",
            "Option payments rarely compensate for lost development opportunity",
            "Automatic extensions remove developer incentive to proceed diligently",
            "Extended options may cloud title and complicate estate transactions",
            "No industry standard requires more than 5 years total option period",
        ],
        resolution_strategy=(
            "Negotiate firm initial option of 3 years, with up to 2 extensions of "
            "1 year each contingent on demonstrated progress milestones. Require "
            "escalating option payments of at least 150% for each extension. Include "
            "automatic termination if interconnection agreement not secured by end "
            "of initial term."
        ),
        entity_scope=EntityScope.LANDOWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Contract law principles; no Texas wind option statute",
        issue_category=IssueCategory.WIND_LEASE_STRUCTURE.value,
        interaction_edges=["wind_lease_operations_period", "payment_escalation_structures"],
    ))

    # -----------------------------------------------------------------------
    # D02: Solar Lease Development and Construction Periods
    # -----------------------------------------------------------------------
    doctrines.append(DoctrineBlock(
        topic="solar_lease_development_construction",
        keywords=["solar", "development", "construction", "period", "timeline", "build"],
        conclusion_template=(
            "Solar lease development periods are typically 3-7 years including "
            "permitting and interconnection, with construction periods of 12-24 "
            "months. Landowners should negotiate separate payment rates for each "
            "phase and require construction commencement deadlines."
        ),
        reasoning_framework=(
            "Solar projects have distinct development, construction, and operations "
            "phases each with different land use impacts. The development phase "
            "involves site assessment, permitting, interconnection studies, and "
            "financing arrangement with minimal surface disturbance. Construction "
            "involves grading, pile driving for racking systems, inverter pad "
            "installation, trenching for underground collection, and substation "
            "construction causing significant temporary disruption. Operations "
            "involve minimal ongoing disturbance. Payment structures should reflect "
            "this progression: nominal during development, increased during "
            "construction for surface damages, and full commercial rates during "
            "operations. Key landowner protections include construction start "
            "deadlines, stormwater management requirements during construction, "
            "topsoil preservation obligations, and dust control measures."
        ),
        key_factors=[
            "Development period length and permitted activities",
            "Construction commencement deadline (drop-dead date)",
            "Construction period duration and extension triggers",
            "Separate payment rates per phase",
            "Surface restoration requirements post-construction",
            "Construction traffic and access road specifications",
            "Topsoil stockpiling and replacement obligations",
            "Stormwater pollution prevention plan requirements",
        ],
        primary_authority=[
            "SEIA Model Solar Lease Agreement (development phase provisions)",
            "Texas Commission on Environmental Quality stormwater permits",
            "IRC Sec. 48 (construction commencement for ITC)",
            "IRS Notice 2018-59 (beginning of construction safe harbors)",
        ],
        burden_holder=BurdenHolder.DEVELOPER.value,
        adversary_position=(
            "Developer seeks maximum construction timeline flexibility due to "
            "supply chain uncertainties and interconnection delays."
        ),
        counter_arguments=[
            "Extended construction periods maximize land disruption",
            "Landowner loses full agricultural use during construction",
            "Developer should bear risk of supply chain delays not landowner",
            "Interconnection delays are foreseeable developer risks",
            "Construction bonds should secure completion obligations",
        ],
        resolution_strategy=(
            "Separate payment schedules per phase with construction rate at minimum "
            "150% of development rate. Require construction commencement within 5 "
            "years of lease execution with firm 24-month construction completion "
            "deadline. Include construction bond equal to estimated restoration cost."
        ),
        entity_scope=EntityScope.LANDOWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Contract law; IRS construction commencement guidance",
        issue_category=IssueCategory.SOLAR_LEASE_STRUCTURE.value,
        interaction_edges=["decommissioning_bond_requirements", "tax_incentive_construction_timing"],
    ))

    # -----------------------------------------------------------------------
    # D03: Per-MW vs Per-Acre Payment Analysis
    # -----------------------------------------------------------------------
    doctrines.append(DoctrineBlock(
        topic="per_mw_vs_per_acre_payment",
        keywords=["payment", "per MW", "per acre", "royalty", "rent", "compensation", "rate"],
        conclusion_template=(
            "Landowner compensation in wind/solar leases is structured as per-acre "
            "annual rent ($300-$1,500/acre for solar, $30-$80/acre for wind), "
            "per-MW capacity payments ($3,000-$8,000/MW for wind), or percentage "
            "of gross revenue (2-6%). Optimal structure depends on project type, "
            "local market, and landowner risk tolerance."
        ),
        reasoning_framework=(
            "Payment structure selection involves fundamental trade-offs. Per-acre "
            "payments provide certainty regardless of project output but may undervalue "
            "highly productive sites. Per-MW payments align compensation with project "
            "scale but create risk if turbines are relocated or downsized. Gross "
            "revenue percentages capture upside from high production and escalating "
            "power prices but expose landowner to market and curtailment risk. "
            "Best practice for landowners is a hybrid structure: guaranteed minimum "
            "per-acre payment as floor, with revenue percentage kicker when actual "
            "revenue exceeds the minimum. This eliminates downside risk while "
            "preserving upside participation. For solar, per-acre payments dominate "
            "because panels cover nearly all acreage unlike wind turbines. Wind "
            "leases more commonly use per-turbine or per-MW structures because "
            "turbines occupy small footprints on large tracts. Market rates vary "
            "significantly by region, wind/solar resource quality, proximity to "
            "transmission, and local competition for leases."
        ),
        key_factors=[
            "Project type (wind vs solar vs hybrid)",
            "Local market rates and competing lease offers",
            "Wind/solar resource quality at site",
            "Proximity to transmission infrastructure",
            "Total acreage and usable project area",
            "Payment escalation mechanism (CPI, fixed %, etc.)",
            "Minimum guaranteed payment provisions",
            "Revenue definition (gross vs net, curtailment treatment)",
        ],
        primary_authority=[
            "AWEA Wind Lease Handbook (payment structure analysis)",
            "SEIA Solar Lease Best Practices Guide",
            "Windustry Land Lease Considerations for Wind Energy (2023)",
            "American Farmland Trust Solar Lease Guidance",
        ],
        burden_holder=BurdenHolder.SHARED.value,
        adversary_position=(
            "Developer prefers flat per-acre payments with modest fixed escalation "
            "to create predictable project economics for financing."
        ),
        counter_arguments=[
            "Flat per-acre undervalues high-quality wind/solar resource",
            "Fixed escalation may trail actual inflation over 30-year terms",
            "Developer captures 100% of production upside with flat rent",
            "Revenue percentage aligns landowner interest with project success",
            "Hybrid structures are increasingly standard in competitive markets",
        ],
        resolution_strategy=(
            "Negotiate hybrid structure: minimum per-acre floor ($500+/acre solar, "
            "$50+/acre wind) with 2-4% gross revenue kicker when revenue exceeds "
            "minimum. Annual CPI escalation on the minimum. Define gross revenue "
            "to exclude only transmission losses, not curtailment."
        ),
        entity_scope=EntityScope.LANDOWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Market-based; no statutory payment requirements",
        issue_category=IssueCategory.PAYMENT_STRUCTURE.value,
        interaction_edges=["payment_escalation_structures", "gross_revenue_definition"],
    ))

    # -----------------------------------------------------------------------
    # D04: Payment Escalation Structures
    # -----------------------------------------------------------------------
    doctrines.append(DoctrineBlock(
        topic="payment_escalation_structures",
        keywords=["escalation", "CPI", "inflation", "increase", "annual", "adjustment"],
        conclusion_template=(
            "Lease payment escalation provisions protect landowners against inflation "
            "over 30-50 year lease terms. CPI-based escalation with a floor of 1.5-2% "
            "and no cap is the strongest landowner position. Fixed percentage "
            "escalation of 2-3% annually is acceptable if CPI is unavailable."
        ),
        reasoning_framework=(
            "Renewable energy leases routinely span 30-50 years including extensions. "
            "Without escalation, the real value of lease payments can erode by 50-70% "
            "over a 30-year term at average inflation rates. CPI-based escalation is "
            "preferred because it tracks actual purchasing power. However developers "
            "may resist CPI linkage due to financing uncertainty. Fixed percentage "
            "escalation provides certainty to both parties but may under- or "
            "over-compensate relative to actual inflation. Key negotiation points: "
            "(1) CPI index selection (CPI-U national vs regional), (2) floor rate to "
            "prevent deflation-driven rent reduction, (3) cap on annual increase to "
            "limit developer exposure, (4) compounding vs simple escalation, (5) "
            "frequency of adjustment (annual vs every 5 years). Five-year adjustment "
            "intervals significantly disadvantage landowners in inflationary periods."
        ),
        key_factors=[
            "CPI index selection and measurement period",
            "Floor rate on annual escalation (1.5-2% minimum)",
            "Cap on annual escalation (developer will push for 3-4%)",
            "Compounding vs simple calculation method",
            "Adjustment frequency (annual strongly preferred)",
            "Base year definition",
            "Catch-up provisions if CPI exceeds cap in prior years",
            "Interaction with revenue percentage payments",
        ],
        primary_authority=[
            "Bureau of Labor Statistics CPI-U methodology",
            "AWEA Model Lease escalation provisions",
            "Windustry Fair Wind Lease Guidelines",
        ],
        burden_holder=BurdenHolder.SHARED.value,
        adversary_position=(
            "Developer prefers fixed 1.5% annual escalation with 5-year intervals "
            "to minimize financing uncertainty and lock in predictable costs."
        ),
        counter_arguments=[
            "1.5% fixed is below historical average CPI of ~2.5%",
            "5-year intervals cause landowner to absorb interim inflation",
            "Developer project revenues naturally escalate with energy prices",
            "Lenders routinely accept CPI escalation in project models",
            "Flat escalation transfers inflation risk entirely to landowner",
        ],
        resolution_strategy=(
            "Annual CPI-U escalation with 2% floor and no cap. If developer insists "
            "on cap, accept 4% cap only with catch-up provision allowing accumulated "
            "excess to be applied in subsequent below-cap years."
        ),
        entity_scope=EntityScope.LANDOWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Contract negotiation; market practice",
        issue_category=IssueCategory.PAYMENT_STRUCTURE.value,
        interaction_edges=["per_mw_vs_per_acre_payment", "gross_revenue_definition"],
    ))

    # -----------------------------------------------------------------------
    # D05: Accommodation Doctrine - Surface Use Conflicts
    # -----------------------------------------------------------------------
    doctrines.append(DoctrineBlock(
        topic="accommodation_doctrine_surface_conflicts",
        keywords=["accommodation", "doctrine", "mineral", "surface", "conflict", "dominant"],
        conclusion_template=(
            "Under the Texas accommodation doctrine (Getty Oil v. Jones, 470 S.W.2d "
            "618), the mineral owner's dominant estate right to use the surface must "
            "accommodate existing surface uses if reasonable alternatives exist. Wind "
            "and solar lessees as surface users must demonstrate their use predates "
            "the mineral activity and that the mineral lessee has reasonable "
            "alternatives available."
        ),
        reasoning_framework=(
            "The accommodation doctrine is critical for renewable energy projects in "
            "Texas where minerals are frequently severed from the surface. The mineral "
            "estate is dominant and has the implied right to use so much of the surface "
            "as is reasonably necessary to extract minerals. However, under Getty Oil "
            "Co. v. Jones (Tex. 1971), if the surface owner (or their lessee) can "
            "show: (1) an existing surface use that (2) would be substantially impaired "
            "by the mineral lessee's proposed operations, and (3) the mineral lessee "
            "has reasonable alternative methods available, then the mineral lessee must "
            "accommodate the existing surface use. For wind/solar projects, the key "
            "issue is whether renewable energy facilities constitute an 'existing use' "
            "that triggers accommodation. Post-construction, turbines and panels are "
            "existing uses. During development (pre-construction), the accommodation "
            "doctrine provides weaker protection. Wind/solar leases should include "
            "express covenants requiring the surface owner to enforce accommodation "
            "rights against mineral operators. The developer should also conduct "
            "thorough title work to identify all severed mineral interests and "
            "negotiate surface use agreements with mineral owners where possible."
        ),
        key_factors=[
            "Whether minerals are severed from surface estate",
            "Timing of wind/solar lease relative to mineral lease",
            "Whether wind/solar facilities are 'existing use' at time of conflict",
            "Availability of reasonable alternatives for mineral operations",
            "Nature and extent of surface impairment",
            "Whether surface use agreement exists with mineral owner",
            "Texas Supreme Court accommodation doctrine precedent",
            "Insurance and indemnification provisions for surface damage",
        ],
        primary_authority=[
            "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
            "Merriman v. XTO Energy, Inc., 407 S.W.3d 244 (Tex. 2013)",
            "Coyote Lake Ranch LLC v. City of Lubbock, 498 S.W.3d 53 (Tex. 2016)",
            "Texas Natural Resources Code Ch. 91 (surface damage)",
            "Lightning Oil Co. v. Anadarko E&P Onshore, LLC, 520 S.W.3d 39 (Tex. 2017)",
        ],
        burden_holder=BurdenHolder.MINERAL_OWNER.value,
        adversary_position=(
            "Mineral owner/lessee asserts dominant estate right to use surface for "
            "drilling and production operations regardless of renewable energy "
            "installations, arguing wind/solar are subordinate surface uses."
        ),
        counter_arguments=[
            "Wind/solar installations predate proposed drilling operations",
            "Directional drilling provides reasonable alternative method",
            "Horizontal pads can be located outside turbine/panel arrays",
            "Surface damage would destroy multi-million dollar infrastructure",
            "Mineral operator has duty to use surface with due regard",
        ],
        resolution_strategy=(
            "Conduct comprehensive mineral title search before lease execution. "
            "Negotiate surface use agreements with all mineral interest owners. "
            "Include lease provisions requiring developer to enforce accommodation "
            "rights. Require developer to carry insurance covering mineral "
            "operator interference. Consider purchasing surface waivers from "
            "mineral owners for critical infrastructure areas."
        ),
        entity_scope=EntityScope.SURFACE_OWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
        issue_category=IssueCategory.ACCOMMODATION_DOCTRINE.value,
        interaction_edges=["split_estate_wind_solar", "mineral_owner_surface_waiver"],
    ))

    # -----------------------------------------------------------------------
    # D06: Decommissioning Bond Requirements
    # -----------------------------------------------------------------------
    doctrines.append(DoctrineBlock(
        topic="decommissioning_bond_requirements",
        keywords=["decommissioning", "bond", "removal", "restoration", "surety", "financial"],
        conclusion_template=(
            "Landowners must require decommissioning financial assurance (surety bond, "
            "letter of credit, or escrow) equal to 100-150% of estimated removal cost, "
            "net of salvage value only if conservatively appraised. Security must be "
            "posted by commercial operation date, not deferred to end of lease term."
        ),
        reasoning_framework=(
            "Decommissioning is the single largest financial risk for landowners in "
            "renewable energy leases. Wind turbine removal costs $200,000-$500,000 per "
            "turbine; solar panel removal costs $15,000-$40,000 per MW. If a developer "
            "becomes insolvent at end of lease, the landowner is left with abandoned "
            "infrastructure. Key protective measures: (1) Independent third-party cost "
            "estimate updated every 5 years; (2) Financial assurance posted at COD, "
            "not deferred; (3) Salvage value credit limited to 50% of appraised scrap "
            "value (scrap markets fluctuate); (4) Assurance type: surety bond or "
            "irrevocable standby letter of credit from rated institution (A- minimum); "
            "(5) Restoration to original agricultural capability including topsoil "
            "replacement, foundation removal to 4 feet below grade, and road removal "
            "unless landowner elects to keep; (6) Completion deadline of 18-24 months "
            "after cessation of operations. Some Texas counties have begun adopting "
            "decommissioning ordinances (e.g., Shackelford, Callahan counties). "
            "Even absent ordinance, contractual requirements are enforceable."
        ),
        key_factors=[
            "Independent cost estimate methodology and update frequency",
            "Timing of financial assurance posting (COD preferred)",
            "Type of financial assurance (surety, LOC, escrow)",
            "Credit quality requirements for assurance issuer",
            "Salvage value credit limitations",
            "Foundation removal depth requirements",
            "Road removal vs landowner retention election",
            "Completion deadline after cessation of operations",
        ],
        primary_authority=[
            "Texas Local Government Code Ch. 232 (county regulatory authority)",
            "AWEA Decommissioning Best Practices Guide",
            "SEIA Solar Decommissioning Guidance (2023)",
            "Sample county decommissioning ordinances (Shackelford, Callahan)",
        ],
        burden_holder=BurdenHolder.DEVELOPER.value,
        adversary_position=(
            "Developer argues salvage value will cover removal costs, decommissioning "
            "security should be reduced by full salvage credit, and assurance need "
            "not be posted until year 20 of operations."
        ),
        counter_arguments=[
            "Salvage value is speculative and market-dependent",
            "Deferred posting creates insolvency risk during operations",
            "Developer may assign lease to thinly capitalized entity",
            "Actual decommissioning costs routinely exceed initial estimates",
            "Landowner has no mechanism to force developer compliance without bond",
        ],
        resolution_strategy=(
            "Require surety bond or irrevocable LOC at COD equal to 125% of "
            "third-party removal estimate. Credit salvage at no more than 50% of "
            "conservative scrap appraisal. Update estimate every 5 years with "
            "assurance amount adjusted accordingly. Require restoration to "
            "agricultural capability within 18 months of cessation."
        ),
        entity_scope=EntityScope.LANDOWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Contract law; county ordinances where adopted",
        issue_category=IssueCategory.DECOMMISSIONING.value,
        interaction_edges=["solar_lease_development_construction", "landowner_protective_provisions"],
    ))

    # -----------------------------------------------------------------------
    # D07: Production Tax Credit (PTC) Implications
    # -----------------------------------------------------------------------
    doctrines.append(DoctrineBlock(
        topic="production_tax_credit_implications",
        keywords=["PTC", "production tax credit", "section 45", "IRA", "tax", "credit"],
        conclusion_template=(
            "The Production Tax Credit (IRC Sec. 45/45Y) provides a per-kWh credit "
            "for wind energy production over 10 years. Post-IRA, PTC base rate is "
            "0.3 cents/kWh (2.75 cents/kWh with prevailing wage/apprenticeship). "
            "Lease structures must account for PTC monetization through tax equity "
            "partnerships or transferability under IRA Sec. 6418."
        ),
        reasoning_framework=(
            "The PTC is the primary federal tax incentive for wind energy. Under the "
            "Inflation Reduction Act of 2022, the PTC was extended and modified: base "
            "credit of 0.3 cents/kWh escalated to 2.75 cents/kWh (2024 value) for "
            "projects meeting prevailing wage and registered apprenticeship requirements. "
            "Additional bonus credits: 10% for domestic content, 10% for energy "
            "community siting, 10-20% for low-income community benefit. The PTC "
            "affects lease negotiations because: (1) Developer needs lease structure "
            "compatible with tax equity financing; (2) PTC value supports higher "
            "lease payments; (3) Assignment provisions must accommodate partnership "
            "flip structures; (4) IRA Sec. 6418 transferability may reduce tax equity "
            "complexity but creates new lender concerns. Landowners should understand "
            "PTC economics to negotiate fair compensation — if PTC adds $15-25/MWh in "
            "value, landowner should capture proportional benefit. Construction "
            "commencement requirements (IRS Notice 2013-29, 2013-60, 2018-59) affect "
            "development timelines in lease option periods."
        ),
        key_factors=[
            "PTC vs ITC election (wind projects may elect either post-IRA)",
            "Prevailing wage and apprenticeship compliance requirements",
            "Domestic content bonus credit eligibility",
            "Energy community bonus credit eligibility",
            "Construction commencement safe harbors",
            "Tax equity partnership structure compatibility",
            "IRA Sec. 6418 transferability election",
            "10-year credit period and production measurement",
        ],
        primary_authority=[
            "IRC Sec. 45 (Production Tax Credit)",
            "IRC Sec. 45Y (Clean Electricity Production Credit, post-2024)",
            "Inflation Reduction Act of 2022, Pub. L. 117-169",
            "IRS Notice 2013-29, 2013-60 (beginning of construction)",
            "IRS Notice 2018-59 (continuity safe harbor)",
            "IRC Sec. 6418 (transferability of clean energy credits)",
        ],
        burden_holder=BurdenHolder.DEVELOPER.value,
        adversary_position=(
            "Developer positions PTC as developer benefit only, arguing lease "
            "payments should not increase to reflect PTC value."
        ),
        counter_arguments=[
            "PTC value directly depends on landowner providing the site",
            "Without land lease, developer cannot generate PTC",
            "Fair market lease should reflect total project economics including PTC",
            "Competing developers will offer higher payments reflecting PTC value",
            "Revenue share structures automatically capture PTC benefit",
        ],
        resolution_strategy=(
            "Structure lease with revenue percentage that captures PTC-enhanced "
            "economics. Require developer to certify prevailing wage compliance "
            "to maximize credit value. Include energy community and domestic "
            "content bonus provisions in lease payment calculations."
        ),
        entity_scope=EntityScope.DEVELOPER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="IRC Sec. 45; IRA 2022; IRS Notices",
        issue_category=IssueCategory.TAX_INCENTIVE.value,
        interaction_edges=["investment_tax_credit_solar", "tax_equity_financing_structure"],
    ))

    # -----------------------------------------------------------------------
    # D08: Investment Tax Credit (ITC) for Solar
    # -----------------------------------------------------------------------
    doctrines.append(DoctrineBlock(
        topic="investment_tax_credit_solar",
        keywords=["ITC", "investment tax credit", "section 48", "solar", "tax", "credit"],
        conclusion_template=(
            "The Investment Tax Credit (IRC Sec. 48/48E) provides a percentage-of-cost "
            "credit for solar installations. Post-IRA base rate is 6% (30% with "
            "prevailing wage/apprenticeship). ITC timing is driven by 'placed in "
            "service' date, making construction period provisions in the lease "
            "critical for tax credit qualification."
        ),
        reasoning_framework=(
            "The ITC is the primary federal incentive for solar energy. Unlike the "
            "per-kWh PTC, the ITC is a percentage of eligible project cost claimed "
            "in the year property is placed in service. Post-IRA: base 6% credit "
            "escalated to 30% for projects meeting prevailing wage and apprenticeship "
            "requirements, with identical bonus adders as PTC (domestic content, "
            "energy community, low-income). Solar projects may elect PTC or ITC "
            "post-IRA, with the choice depending on project economics and financing "
            "structure. ITC election is typically preferred for solar because "
            "upfront credit provides greater present value than 10-year stream. "
            "Lease implications: (1) construction timeline must meet 'placed in "
            "service' requirements; (2) MACRS 5-year depreciation supplements ITC; "
            "(3) tax equity structures require specific lease provisions including "
            "SNDA and estoppel capabilities; (4) ITC recapture risk over 5-year "
            "period affects assignment restrictions."
        ),
        key_factors=[
            "ITC vs PTC election analysis for solar",
            "Prevailing wage and apprenticeship compliance",
            "Placed in service date determination",
            "MACRS 5-year depreciation interaction",
            "ITC recapture risk and 5-year holding period",
            "Tax equity structure requirements",
            "Eligible cost basis determination",
            "Bonus depreciation interaction with ITC basis reduction",
        ],
        primary_authority=[
            "IRC Sec. 48 (Energy Credit)",
            "IRC Sec. 48E (Clean Electricity Investment Credit, post-2024)",
            "IRC Sec. 168(e)(3)(B)(vi) (5-year MACRS for solar)",
            "IRC Sec. 50(a) (ITC recapture rules)",
            "Inflation Reduction Act of 2022, Pub. L. 117-169",
        ],
        burden_holder=BurdenHolder.DEVELOPER.value,
        adversary_position=(
            "Developer seeks lease terms protecting ITC qualification and "
            "resisting any provisions that could trigger recapture."
        ),
        counter_arguments=[
            "ITC recapture risk is developer's tax issue not landowner's",
            "Lease should not restrict landowner rights to protect developer tax position",
            "Assignment restrictions for recapture protection should be time-limited to 5 years",
            "Landowner should not guarantee ITC qualification",
            "Revenue share should reflect ITC-enhanced economics",
        ],
        resolution_strategy=(
            "Accommodate reasonable ITC-protective provisions (e.g., 5-year recapture "
            "period restrictions on early termination for landowner convenience) but "
            "do not restrict landowner rights beyond the 5-year recapture period. "
            "Revenue share should reflect total project value including ITC."
        ),
        entity_scope=EntityScope.DEVELOPER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="IRC Sec. 48; IRC Sec. 50(a); IRA 2022",
        issue_category=IssueCategory.TAX_INCENTIVE.value,
        interaction_edges=["production_tax_credit_implications", "macrs_depreciation_strategy"],
    ))

    # -----------------------------------------------------------------------
    # D09: ERCOT Interconnection Requirements
    # -----------------------------------------------------------------------
    doctrines.append(DoctrineBlock(
        topic="ercot_interconnection_requirements",
        keywords=["ERCOT", "interconnection", "grid", "POI", "queue", "transmission"],
        conclusion_template=(
            "ERCOT interconnection requires navigating a multi-year queue process "
            "including screening study, full interconnection study, and construction "
            "of network upgrades. Lease option periods must accommodate 3-5 year "
            "interconnection timelines. Landowners should require demonstrated "
            "interconnection progress as option extension conditions."
        ),
        reasoning_framework=(
            "ERCOT manages the Texas electric grid and controls interconnection of "
            "new generation resources. The interconnection process involves: (1) "
            "Screening study submission with required deposit; (2) Full "
            "interconnection study evaluating transmission system impacts; (3) "
            "Interconnection agreement execution; (4) Construction of any required "
            "network upgrades at developer cost. The process typically takes 3-5 "
            "years, creating tension with lease option periods. ERCOT queue reform "
            "in 2023-2024 introduced stricter readiness requirements including "
            "site control documentation (the lease itself), financial deposits "
            "scaling with project size, and milestone-based queue management. "
            "Lease provisions should address: (1) Developer obligation to maintain "
            "queue position; (2) Interconnection agreement as option extension "
            "condition; (3) Network upgrade cost allocation; (4) Curtailment risk "
            "and its impact on revenue-based payments; (5) Point of interconnection "
            "location and gen-tie routing across the leased property."
        ),
        key_factors=[
            "ERCOT interconnection queue position and study status",
            "Required financial deposits and security posting",
            "Timeline for screening and full interconnection studies",
            "Network upgrade cost responsibility",
            "Curtailment risk assessment for project location",
            "Gen-tie line routing and additional easement needs",
            "ERCOT site control documentation requirements",
            "Queue reform milestone requirements",
        ],
        primary_authority=[
            "ERCOT Protocols Section 5 (Resource Registration)",
            "ERCOT Planning Guide (interconnection procedures)",
            "PUCT Substantive Rule 25.198 (interconnection standards)",
            "ERCOT Generation Interconnection or Change Request procedures",
        ],
        burden_holder=BurdenHolder.DEVELOPER.value,
        adversary_position=(
            "Developer argues ERCOT delays are unforeseeable and outside developer "
            "control, justifying unlimited option extensions."
        ),
        counter_arguments=[
            "ERCOT timelines are well-established and foreseeable",
            "Developer assumed queue risk when entering market",
            "Other developers manage queue timelines within standard option periods",
            "Unlimited extensions tie up land without compensation",
            "Developer can negotiate with ERCOT for expedited processing",
        ],
        resolution_strategy=(
            "Require developer to submit interconnection application within 12 months "
            "of option execution. Condition option extensions on demonstrated queue "
            "progress (screening study complete, full study in progress). Require "
            "interconnection agreement execution as condition for lease commencement."
        ),
        entity_scope=EntityScope.DEVELOPER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="ERCOT Protocols; PUCT rules",
        issue_category=IssueCategory.ERCOT_INTERCONNECTION.value,
        interaction_edges=["wind_lease_option_period", "transmission_line_easement"],
    ))

    # -----------------------------------------------------------------------
    # D10: Agricultural Exemption Preservation
    # -----------------------------------------------------------------------
    doctrines.append(DoctrineBlock(
        topic="agricultural_exemption_preservation",
        keywords=["agricultural", "exemption", "ag", "valuation", "1-d-1", "tax", "property"],
        conclusion_template=(
            "Wind/solar leases can jeopardize Texas agricultural valuation (Tax Code "
            "Sec. 23.51) resulting in rollback taxes of up to 5 years. Lease "
            "provisions must address which party bears rollback tax liability, "
            "minimize footprint to preserve ag use on non-disturbed acreage, and "
            "include grazing/haying provisions under solar panels."
        ),
        reasoning_framework=(
            "Texas agricultural valuation under Tax Code Ch. 23 Subchapter D "
            "reduces property tax by valuing land on productive capacity rather "
            "than market value, typically reducing assessed value by 90%+. Change "
            "in use triggers rollback taxes — the difference between ag value and "
            "market value taxes for the preceding 5 years plus 7% annual interest. "
            "For wind projects, turbine pad sites and access roads clearly change "
            "use, but surrounding acreage used for grazing/farming may retain "
            "exemption. For solar projects, the entire fenced array area typically "
            "loses ag exemption unless the landowner establishes compatible "
            "agricultural use (sheep grazing under panels is increasingly accepted "
            "by county appraisal districts). Key issues: (1) Which acreage loses "
            "exemption — only disturbed footprint or entire leased tract; (2) "
            "Developer indemnification for rollback taxes; (3) Agrivoltaics and "
            "pollinator habitat as qualifying ag uses; (4) County appraisal "
            "district interpretation variability; (5) HB 3345 (2023) exempting "
            "certain renewable energy property from ad valorem tax."
        ),
        key_factors=[
            "Current agricultural valuation status and type (1-d-1 vs open space)",
            "Acreage losing agricultural use vs total tract size",
            "Rollback tax liability calculation (5 years + 7% interest)",
            "Developer indemnification for rollback taxes",
            "Compatible agricultural uses under/around solar arrays",
            "County appraisal district interpretation of 'change in use'",
            "Grazing compatibility with wind turbines",
            "Agrivoltaic or pollinator habitat programs",
        ],
        primary_authority=[
            "Texas Tax Code Sec. 23.51-23.57 (agricultural appraisal)",
            "Texas Tax Code Sec. 23.55 (change of use rollback)",
            "Texas Tax Code Sec. 312.0025 (renewable energy tax abatements)",
            "HB 3345 (88th Leg., 2023) renewable energy property",
            "Comptroller Property Tax Assistance Division guidance",
        ],
        burden_holder=BurdenHolder.SHARED.value,
        adversary_position=(
            "Developer argues rollback taxes are a landowner obligation as property "
            "owner of record and that developer compensation already accounts for "
            "this cost."
        ),
        counter_arguments=[
            "Developer's project directly causes the change in use",
            "Rollback taxes can exceed years of lease payments",
            "Developer indemnification is standard in competitive markets",
            "Developer can minimize rollback by reducing footprint",
            "Agrivoltaic provisions benefit both parties",
        ],
        resolution_strategy=(
            "Require full developer indemnification for all rollback taxes triggered "
            "by project construction. Minimize disturbed acreage through design "
            "requirements. Include mandatory agrivoltaic or grazing program for "
            "solar arrays. Require developer cooperation with appraisal district "
            "to preserve exemption on non-disturbed acreage."
        ),
        entity_scope=EntityScope.LANDOWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Texas Tax Code Ch. 23 Subchapter D",
        issue_category=IssueCategory.AGRICULTURAL.value,
        interaction_edges=["per_mw_vs_per_acre_payment", "decommissioning_bond_requirements"],
    ))

    # -----------------------------------------------------------------------
    # D11: Shadow Flicker and Noise Easements
    # -----------------------------------------------------------------------
    doctrines.append(DoctrineBlock(
        topic="shadow_flicker_noise_easements",
        keywords=["shadow", "flicker", "noise", "decibel", "setback", "nuisance"],
        conclusion_template=(
            "Shadow flicker from wind turbines should be limited to 30 hours/year "
            "at any occupied building per international best practice. Noise levels "
            "should not exceed 45 dBA at non-participating residences. Separate "
            "shadow flicker and noise easements from participating landowners are "
            "essential for project permitting."
        ),
        reasoning_framework=(
            "Shadow flicker occurs when rotating turbine blades cast moving shadows "
            "on nearby structures. International standards (German BImSchG) limit "
            "flicker to 30 hours/year actual or 8 hours/year worst-case astronomical "
            "calculation at any receptor. Texas has no statewide flicker standard, "
            "but county regulations are emerging. Noise from wind turbines is "
            "primarily aerodynamic (blade tip noise) measured as time-averaged "
            "sound pressure level (Leq). Industry standard is 45 dBA at property "
            "line of non-participating residences. Lease provisions should: (1) "
            "Include landowner consent to specified flicker and noise levels at "
            "their buildings; (2) Define measurement methodology and frequency; "
            "(3) Provide remediation requirements if limits are exceeded (curtailment, "
            "retrofit, compensation); (4) Address cumulative impact from multiple "
            "turbines; (5) Include noise easement for neighboring properties. "
            "Noise complaints are the #1 source of community opposition to wind "
            "projects. Proactive easement acquisition from neighbors reduces risk."
        ),
        key_factors=[
            "Shadow flicker hours limit (30 hrs/year actual recommended)",
            "Noise level limit at property line (45 dBA non-participating)",
            "Measurement methodology and instrumentation standards",
            "Monitoring frequency and reporting requirements",
            "Remediation triggers and required actions",
            "Neighboring property easement acquisition strategy",
            "County noise and flicker ordinance compliance",
            "Cumulative impact from multiple turbines",
        ],
        primary_authority=[
            "German Federal Immission Control Act (BImSchG) flicker limits",
            "ANSI/ASA S12.9 (sound measurement methodology)",
            "IEC 61400-11 (wind turbine noise measurement)",
            "County zoning ordinances (where adopted)",
        ],
        burden_holder=BurdenHolder.DEVELOPER.value,
        adversary_position=(
            "Developer seeks broad noise and flicker easements from participating "
            "landowners with unlimited impact levels and waiver of all claims."
        ),
        counter_arguments=[
            "Unlimited noise/flicker impairs livability of landowner residence",
            "Health impacts of chronic flicker exposure are documented",
            "Broad waivers may not be enforceable as unconscionable",
            "Developer can design layout to minimize impacts",
            "Compensation should escalate with impact levels",
        ],
        resolution_strategy=(
            "Consent to reasonable levels (45 dBA noise, 30 hours/year flicker) "
            "with annual monitoring and reporting. Include automatic curtailment "
            "obligation if limits exceeded. Require developer to acquire neighbor "
            "easements at developer cost. Provide additional compensation for "
            "residences within 1,000 feet of turbines."
        ),
        entity_scope=EntityScope.LANDOWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="No Texas statute; county ordinances; industry standards",
        issue_category=IssueCategory.SHADOW_FLICKER_NOISE.value,
        interaction_edges=["surface_use_restrictions_setbacks", "landowner_protective_provisions"],
    ))

    # -----------------------------------------------------------------------
    # D12: CREZ Transmission Lines and Eminent Domain
    # -----------------------------------------------------------------------
    doctrines.append(DoctrineBlock(
        topic="crez_transmission_eminent_domain",
        keywords=["CREZ", "transmission", "eminent domain", "condemnation", "easement", "line"],
        conclusion_template=(
            "CREZ (Competitive Renewable Energy Zone) transmission lines built under "
            "SB 20 (2005) and PUCT orders carry eminent domain authority under Texas "
            "Utilities Code Ch. 37. Landowners facing CREZ condemnation should "
            "negotiate compensation above appraised value and require construction "
            "mitigation provisions."
        ),
        reasoning_framework=(
            "Texas designated 5 CREZs in 2008 with ~3,600 miles of new 345kV "
            "transmission lines costing $6.8B to connect West Texas wind resources "
            "to population centers. Transmission utilities (LCRA TSC, AEP, Oncor, "
            "Sharyland, Cross Texas, Wind Energy Transmission Texas) were authorized "
            "to construct CREZ lines with eminent domain authority. For landowners: "
            "(1) Utilities must make good-faith purchase offer before condemnation; "
            "(2) Compensation is fair market value of easement plus damages to "
            "remainder; (3) Landowners can hire independent appraisers at utility "
            "cost; (4) Special commissioners determine compensation if parties "
            "disagree; (5) Landowners may challenge necessity and route in district "
            "court. Beyond CREZ, new transmission for renewable energy may be "
            "authorized under PUCT CCN proceedings. Developers needing transmission "
            "easements across non-participating landowner property for gen-tie lines "
            "generally do NOT have eminent domain authority unless they qualify as a "
            "utility under Texas Utilities Code."
        ),
        key_factors=[
            "Whether project is CREZ-designated or new transmission",
            "Utility CCN authority and eminent domain qualification",
            "Fair market value appraisal methodology",
            "Damage to remainder calculation",
            "Construction mitigation and restoration requirements",
            "Easement width and permitted uses within corridor",
            "Landowner right to independent appraiser at utility cost",
            "Special commissioners procedure and appeal rights",
        ],
        primary_authority=[
            "Texas Utilities Code Ch. 37 (eminent domain for utilities)",
            "Texas Property Code Ch. 21 (condemnation procedures)",
            "SB 20 (79th Leg., 2005) and PUCT Docket 33672 (CREZ designation)",
            "PUCT Substantive Rule 25.101 (CCN requirements)",
            "Texas Constitution Art. I, Sec. 17 (takings clause)",
        ],
        burden_holder=BurdenHolder.GOVERNMENT.value,
        adversary_position=(
            "Utility asserts necessity and public use, arguing that PUCT authorization "
            "conclusively establishes the right to condemn and that compensation "
            "should reflect agricultural use value only."
        ),
        counter_arguments=[
            "Landowner entitled to highest and best use valuation not just ag value",
            "Transmission line diminishes value of entire tract not just easement area",
            "Construction damage to fencing, roads, and water systems requires compensation",
            "Alternative routes that minimize landowner impact must be evaluated",
            "Landowner may challenge route selection in district court",
        ],
        resolution_strategy=(
            "Engage independent appraiser immediately upon notice of condemnation. "
            "Value easement at highest and best use including proximity to renewable "
            "energy projects. Calculate remainder damages comprehensively. Negotiate "
            "construction mitigation terms including restoration timeline, fence "
            "replacement, and access road maintenance. If necessary, challenge "
            "route through special commissioners proceeding."
        ),
        entity_scope=EntityScope.LANDOWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Texas Utilities Code Ch. 37; Texas Property Code Ch. 21",
        issue_category=IssueCategory.TRANSMISSION.value,
        interaction_edges=["ercot_interconnection_requirements", "transmission_easement_negotiation"],
    ))

    # -----------------------------------------------------------------------
    # D13: Battery Energy Storage System (BESS) Siting
    # -----------------------------------------------------------------------
    doctrines.append(DoctrineBlock(
        topic="battery_storage_siting",
        keywords=["BESS", "battery", "storage", "siting", "safety", "fire", "co-located"],
        conclusion_template=(
            "BESS siting on leased land requires specific lease provisions addressing "
            "fire risk, setback distances (minimum 200 feet from structures), "
            "hazardous materials handling, insurance requirements, and separate "
            "compensation for storage facilities beyond wind/solar payments."
        ),
        reasoning_framework=(
            "Battery storage is increasingly co-located with wind and solar projects "
            "to capture time-of-delivery premiums and provide grid services. BESS "
            "facilities present unique risks not present in wind/solar operations: "
            "thermal runaway fire risk, hazardous material (electrolyte) leakage, "
            "and electromagnetic interference. Key lease provisions: (1) Separate "
            "payment for BESS footprint (typically higher per-acre than solar due to "
            "concentrated risk); (2) Fire suppression system requirements; (3) "
            "Minimum setback from occupied structures, property lines, and water "
            "features; (4) Hazardous materials storage and spill response plan; (5) "
            "Additional insurance coverage (pollution liability, fire); (6) NFPA 855 "
            "and local fire code compliance; (7) Decommissioning provisions for "
            "battery disposal/recycling; (8) EMF exposure limits. Texas has no "
            "statewide BESS siting standards; local fire marshals have jurisdiction."
        ),
        key_factors=[
            "BESS technology type (lithium-ion, flow, etc.) and risk profile",
            "Fire suppression system design and maintenance",
            "Setback distances from structures and property lines",
            "Hazardous materials handling and spill prevention plan",
            "Insurance coverage types and limits",
            "NFPA 855 compliance requirements",
            "Separate compensation structure for BESS footprint",
            "Battery lifecycle and disposal/recycling obligations",
        ],
        primary_authority=[
            "NFPA 855 (Standard for Energy Storage Systems)",
            "IFC 2021 Ch. 12 (Energy Storage Systems)",
            "UL 9540 (Energy Storage System safety standard)",
            "Texas Fire Marshal guidance on BESS installations",
        ],
        burden_holder=BurdenHolder.DEVELOPER.value,
        adversary_position=(
            "Developer argues BESS is part of the wind/solar project and should be "
            "covered under existing lease terms without additional compensation."
        ),
        counter_arguments=[
            "BESS introduces fire and hazmat risk not present in wind/solar",
            "BESS footprint is additional surface use beyond original project scope",
            "Insurance costs increase significantly with BESS co-location",
            "Separate compensation is standard for distinct facility types",
            "Landowner liability exposure increases with hazardous materials",
        ],
        resolution_strategy=(
            "Negotiate separate BESS rider to lease with additional per-MW storage "
            "payment. Require NFPA 855 compliance, 200-foot minimum setback from "
            "occupied structures, comprehensive fire suppression, and pollution "
            "liability insurance. Include battery disposal bond separate from "
            "wind/solar decommissioning assurance."
        ),
        entity_scope=EntityScope.LANDOWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="NFPA 855; local fire codes; contract law",
        issue_category=IssueCategory.BATTERY_STORAGE.value,
        interaction_edges=["decommissioning_bond_requirements", "surface_use_restrictions_setbacks"],
    ))

    # -----------------------------------------------------------------------
    # D14: Eagle Take Permits and Environmental Compliance
    # -----------------------------------------------------------------------
    doctrines.append(DoctrineBlock(
        topic="eagle_take_permit_environmental",
        keywords=["eagle", "take", "permit", "BGEPA", "ESA", "environmental", "NEPA", "wildlife"],
        conclusion_template=(
            "Wind projects must address eagle and migratory bird mortality risk under "
            "the Bald and Golden Eagle Protection Act (BGEPA) and Migratory Bird "
            "Treaty Act. Eagle take permits from USFWS may be required, with 30-year "
            "programmatic permits available. Lease should allocate environmental "
            "compliance costs and delay risk to the developer."
        ),
        reasoning_framework=(
            "Eagle mortality at wind energy facilities is a significant regulatory "
            "and reputational risk. The BGEPA prohibits 'take' (kill, disturb) of "
            "bald and golden eagles without a permit. USFWS issues Eagle Take "
            "Permits under 50 CFR 22.80 for wind projects that cannot avoid take "
            "despite implementing Advanced Conservation Practices. Requirements: "
            "(1) Pre-construction eagle use surveys (2+ years preferred); (2) "
            "Quantitative risk assessment using USFWS Bayesian collision model; "
            "(3) Compensatory mitigation for predicted take (power line retrofitting, "
            "lead abatement); (4) Adaptive management plan with monitoring and "
            "curtailment triggers. The ESA also applies if listed species are "
            "present (lesser prairie chicken, whooping crane in Texas). For federal "
            "land or federal nexus projects, NEPA review is required. Lease "
            "implications: environmental compliance costs ($500K-$2M+) and delays "
            "(2-5 years for eagle surveys) should be allocated to developer. "
            "Landowner should not warrant absence of protected species."
        ),
        key_factors=[
            "Eagle species presence (bald eagle, golden eagle)",
            "Pre-construction survey duration and methodology",
            "USFWS collision risk model results",
            "Compensatory mitigation requirements and costs",
            "Adaptive management plan with curtailment protocols",
            "ESA listed species presence (lesser prairie chicken, etc.)",
            "NEPA requirements for federal nexus projects",
            "Environmental compliance cost allocation in lease",
        ],
        primary_authority=[
            "Bald and Golden Eagle Protection Act (16 U.S.C. 668-668d)",
            "50 CFR 22.80 (eagle take permit regulations)",
            "Migratory Bird Treaty Act (16 U.S.C. 703-712)",
            "Endangered Species Act (16 U.S.C. 1531-1544)",
            "USFWS Eagle Conservation Plan Guidance (2013)",
            "NEPA (42 U.S.C. 4321-4347)",
        ],
        burden_holder=BurdenHolder.DEVELOPER.value,
        adversary_position=(
            "Developer seeks landowner warranty that no protected species exist on "
            "the property and indemnification for environmental compliance costs."
        ),
        counter_arguments=[
            "Landowner cannot warrant wildlife presence or absence",
            "Environmental surveys are developer responsibility",
            "Developer chose this site knowing regulatory requirements",
            "Compliance costs are standard project development expenses",
            "Indemnification for regulatory compliance is unreasonable",
        ],
        resolution_strategy=(
            "Allocate all environmental compliance costs to developer. Landowner "
            "makes no wildlife warranties. Developer bears risk of environmental "
            "delay and cost. Lease option period should accommodate 2-year eagle "
            "survey timeline. Include cooperation provision requiring landowner to "
            "allow survey access during option period."
        ),
        entity_scope=EntityScope.DEVELOPER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="BGEPA; ESA; 50 CFR 22.80",
        issue_category=IssueCategory.ENVIRONMENTAL_COMPLIANCE.value,
        interaction_edges=["wind_lease_option_period", "resource_assessment_easement_terms"],
    ))

    # -----------------------------------------------------------------------
    # D15: Lease vs Easement Structure Analysis
    # -----------------------------------------------------------------------
    doctrines.append(DoctrineBlock(
        topic="lease_vs_easement_structure",
        keywords=["lease", "easement", "structure", "interest", "real property", "conveyance"],
        conclusion_template=(
            "Wind/solar agreements are structured as either leases (possessory interest "
            "with exclusive use) or easements (non-possessory right to use). Leases "
            "provide developers stronger operational control; easements allow landowners "
            "to retain more surface rights. Hybrid structures with easement for "
            "facilities and lease for footprint areas are increasingly common."
        ),
        reasoning_framework=(
            "The choice between lease and easement has significant legal consequences. "
            "A lease conveys exclusive possessory interest — the developer controls "
            "the leased premises and can exclude others. An easement grants only the "
            "right to use land for specified purposes without exclusive possession. "
            "Key differences: (1) Lease creates landlord-tenant relationship with "
            "statutory protections; easement is a property interest; (2) Lease "
            "terminates on expiration; easement may survive unless expressly limited; "
            "(3) Lease is subject to condemnation allocation rules; easement may be "
            "treated differently; (4) Lease payments are ordinary income; easement "
            "payments may have capital gain treatment; (5) Lease may trigger more "
            "extensive property tax consequences than easement. For wind projects, "
            "easements are preferred because turbines occupy small footprints and "
            "agricultural use continues on surrounding land. For solar projects, "
            "leases are more common because panels require exclusive fenced areas. "
            "Hybrid structures grant easements for collector lines, met towers, and "
            "access roads while leasing panel/turbine footprint areas."
        ),
        key_factors=[
            "Type of renewable energy project (wind vs solar)",
            "Exclusivity needs of the developer",
            "Landowner desire to maintain agricultural operations",
            "Property tax consequences of lease vs easement",
            "Income tax treatment (ordinary income vs capital gain)",
            "Condemnation allocation implications",
            "Mortgage and title insurance considerations",
            "Duration and termination provisions",
        ],
        primary_authority=[
            "Texas Property Code (lease and easement provisions)",
            "Restatement (Third) of Property: Servitudes",
            "IRS Revenue Ruling 72-85 (lease vs easement income characterization)",
            "Texas Tax Code (property tax treatment of leasehold interests)",
        ],
        burden_holder=BurdenHolder.SHARED.value,
        adversary_position=(
            "Developer prefers full lease for maximum operational control and "
            "financing flexibility, arguing lenders require possessory interest."
        ),
        counter_arguments=[
            "Easement provides adequate developer rights for wind projects",
            "Landowner retains agricultural use rights under easement",
            "Easement may provide favorable capital gain tax treatment",
            "Hybrid structure satisfies both lender and landowner concerns",
            "Exclusive use lease unnecessary where agricultural co-use is possible",
        ],
        resolution_strategy=(
            "For wind: easement structure with express developer rights for turbine "
            "pads, access roads, and collector lines. For solar: lease of fenced "
            "array area with easement for ancillary facilities. Both: include "
            "SNDA for lender protection regardless of structure choice."
        ),
        entity_scope=EntityScope.LANDOWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Texas Property Code; Restatement (Third) Servitudes",
        issue_category=IssueCategory.EASEMENT_STRUCTURE.value,
        interaction_edges=["per_mw_vs_per_acre_payment", "tax_treatment_lease_vs_easement"],
    ))

    # -----------------------------------------------------------------------
    # D16: Assignment and Financing Provisions
    # -----------------------------------------------------------------------
    doctrines.append(DoctrineBlock(
        topic="assignment_financing_provisions",
        keywords=["assignment", "financing", "lender", "SNDA", "estoppel", "transfer", "consent"],
        conclusion_template=(
            "Renewable energy lease assignment provisions must balance developer need "
            "for financing flexibility with landowner protection against financially "
            "weak assignees. Require landowner consent for assignment (not to be "
            "unreasonably withheld) with creditworthiness standards, and include "
            "SNDA provisions for project lenders."
        ),
        reasoning_framework=(
            "Renewable energy projects change hands frequently through development, "
            "construction, and operation phases. Tax equity financing requires "
            "specific assignment structures (partnership flip). Project lenders "
            "require SNDA (Subordination, Non-Disturbance, and Attornment) "
            "agreements and estoppel certificates. Key issues: (1) Whether "
            "landowner consent is required for any assignment; (2) Definition of "
            "assignment (direct transfer, change of control, merger); (3) "
            "Creditworthiness requirements for assignees; (4) Whether original "
            "developer remains liable after assignment; (5) SNDA terms — lender "
            "right to cure defaults, protection of lease on foreclosure; (6) "
            "Estoppel certificate obligations — reasonable time for response, "
            "scope of representations; (7) Tax equity partnership flip "
            "accommodation. Landowners should not provide blanket assignment "
            "consent because the developer's financial strength directly "
            "affects decommissioning and ongoing lease obligations."
        ),
        key_factors=[
            "Consent requirements for assignment (not unreasonably withheld)",
            "Creditworthiness standards for assignees",
            "Original developer continuing liability",
            "SNDA scope and lender cure rights",
            "Estoppel certificate form and response timeline",
            "Tax equity partnership structure accommodation",
            "Change of control definition and triggers",
            "Assignment to affiliates without consent threshold",
        ],
        primary_authority=[
            "UCC Article 9 (secured transactions in personal property)",
            "Texas Property Code (lease assignment provisions)",
            "Project finance documentation standards (LSTA)",
            "Tax equity partnership flip structure (Rev. Proc. 2007-65)",
        ],
        burden_holder=BurdenHolder.SHARED.value,
        adversary_position=(
            "Developer and lenders seek unrestricted assignment rights and broad "
            "SNDA protections including right to assign lease to any purchaser "
            "at foreclosure sale."
        ),
        counter_arguments=[
            "Unrestricted assignment exposes landowner to unknown parties",
            "Foreclosure purchaser may not have resources for decommissioning",
            "SNDA should not expand developer rights beyond original lease",
            "Estoppel certificates should not create new landowner obligations",
            "Landowner consent protects against financially weak assignees",
        ],
        resolution_strategy=(
            "Require consent for assignment to non-affiliates, not to be unreasonably "
            "withheld based on objective creditworthiness standards. Original developer "
            "remains liable for 2 years post-assignment. SNDA grants lender cure "
            "rights and lease protection on foreclosure but does not expand developer "
            "rights. Estoppel certificates limited to factual representations."
        ),
        entity_scope=EntityScope.LENDER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Texas Property Code; UCC Art. 9; project finance standards",
        issue_category=IssueCategory.FINANCING.value,
        interaction_edges=["decommissioning_bond_requirements", "investment_tax_credit_solar"],
    ))

    # -----------------------------------------------------------------------
    # D17: Landowner Protective Provisions
    # -----------------------------------------------------------------------
    doctrines.append(DoctrineBlock(
        topic="landowner_protective_provisions",
        keywords=["landowner", "protection", "rights", "negotiation", "provision", "clause"],
        conclusion_template=(
            "Essential landowner protective provisions include: use restrictions, "
            "access road specifications, gate and fence obligations, livestock "
            "protection, water well protection, hunting rights retention, "
            "building restriction areas, communication with tenant/operator, "
            "and right to inspect project facilities."
        ),
        reasoning_framework=(
            "Renewable energy leases are drafted by developer counsel and heavily "
            "favor developer interests. Landowners must negotiate specific "
            "protective provisions: (1) Use restrictions — limit lease to renewable "
            "energy generation, not mining, waste disposal, or unrelated uses; (2) "
            "Access roads — specify construction standards, maintenance obligation, "
            "dust control, speed limits, gate closure requirements; (3) Fencing — "
            "developer obligation to maintain perimeter fencing to livestock standard; "
            "(4) Livestock protection — gates, cattle guards, wildlife-friendly "
            "fencing; (5) Water well protection — setback from existing wells, "
            "replacement obligation if wells are damaged; (6) Hunting rights — "
            "express reservation of hunting rights outside safety zones; (7) "
            "Building restriction areas — defined zones where landowner may continue "
            "to build structures without developer consent; (8) Communication — "
            "developer obligation to notify landowner of major activities, provide "
            "24-hour emergency contact; (9) Inspection rights — landowner right to "
            "access and inspect project facilities with reasonable notice; (10) "
            "Insurance — landowner as additional insured on developer policies."
        ),
        key_factors=[
            "Use restriction scope and permitted activities",
            "Access road construction standards and maintenance",
            "Fencing and livestock protection obligations",
            "Water well protection setbacks and replacement",
            "Hunting rights reservation",
            "Building restriction area definitions",
            "Emergency contact and notification requirements",
            "Landowner inspection rights and access",
            "Insurance coverage with landowner as additional insured",
            "Indemnification scope and limitations",
        ],
        primary_authority=[
            "AWEA Model Wind Lease (landowner provisions)",
            "American Farmland Trust Solar Siting Guidance",
            "Windustry Wind Lease Considerations",
            "Farm Bureau renewable energy lease review guidelines",
        ],
        burden_holder=BurdenHolder.DEVELOPER.value,
        adversary_position=(
            "Developer seeks maximum operational flexibility with minimal landowner "
            "restrictions, arguing that specific provisions reduce project viability."
        ),
        counter_arguments=[
            "Reasonable landowner protections do not impair project viability",
            "Developer operates on landowner's property for decades",
            "Unaddressed issues create disputes that harm both parties",
            "Industry best practices include comprehensive landowner protections",
            "Failure to protect landowner invites community opposition",
        ],
        resolution_strategy=(
            "Negotiate comprehensive landowner protection package including all 10 "
            "key provisions. These are non-negotiable baseline terms. Developer "
            "acceptance of these provisions is standard in competitive markets "
            "and does not materially affect project economics."
        ),
        entity_scope=EntityScope.LANDOWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Contract law; industry best practices",
        issue_category=IssueCategory.LANDOWNER_PROTECTION.value,
        interaction_edges=["surface_use_restrictions_setbacks", "decommissioning_bond_requirements"],
    ))

    # -----------------------------------------------------------------------
    # D18: Surface Use Restrictions and Setbacks
    # -----------------------------------------------------------------------
    doctrines.append(DoctrineBlock(
        topic="surface_use_restrictions_setbacks",
        keywords=["surface", "use", "restriction", "setback", "distance", "building", "property"],
        conclusion_template=(
            "Standard wind turbine setbacks: 1.1x tip height from property lines, "
            "1,500 feet from occupied structures, 500 feet from public roads. Solar "
            "setbacks: 100-300 feet from property lines, 500 feet from residences. "
            "Texas has no statewide setback law; county regulations vary widely."
        ),
        reasoning_framework=(
            "Setback requirements define minimum distances between renewable energy "
            "facilities and protected features (property lines, residences, roads, "
            "water features). In Texas, no statewide setback law exists, leaving "
            "regulation to counties with populations under 1M (outside ETJ of "
            "municipalities). Many rural Texas counties have adopted wind energy "
            "regulations with varying setbacks. Lease provisions should establish "
            "contractual setbacks regardless of regulatory requirements: (1) "
            "Property line setback — prevents ice throw and shadow flicker on "
            "neighboring property; (2) Dwelling setback — protects residence from "
            "noise, flicker, and safety risk; (3) Road setback — prevents ice throw "
            "onto public roads; (4) Buildable area — defines where landowner can "
            "build new structures without conflicting with turbine setbacks. "
            "For solar: setbacks primarily address visual screening, stormwater, "
            "and access. Vegetative screening buffers of 25-50 feet along property "
            "lines are increasingly required."
        ),
        key_factors=[
            "Wind turbine tip height and setback multiplier",
            "Occupied structure setback distance",
            "Property line setback distance",
            "Public road setback distance",
            "County regulation requirements (if any)",
            "Solar panel setback from property lines",
            "Visual screening buffer requirements",
            "Buildable area reservation for landowner",
        ],
        primary_authority=[
            "Texas Local Government Code Ch. 232 (county regulatory authority)",
            "Various county wind energy regulations (Nolan, Taylor, Shackelford)",
            "AWEA siting guidelines",
            "International Electrotechnical Commission (IEC) turbine safety standards",
        ],
        burden_holder=BurdenHolder.DEVELOPER.value,
        adversary_position=(
            "Developer seeks minimum setbacks to maximize generation capacity and "
            "argues that Texas's lack of statewide regulation means no setbacks "
            "are legally required."
        ),
        counter_arguments=[
            "Absence of regulation does not eliminate safety and nuisance risk",
            "Inadequate setbacks invite neighbor lawsuits and project delays",
            "Lenders increasingly require reasonable setback compliance",
            "Community opposition to inadequate setbacks can block projects",
            "Contractual setbacks protect both parties regardless of regulation",
        ],
        resolution_strategy=(
            "Establish contractual setbacks meeting or exceeding strictest county "
            "standard in the area. Wind: minimum 1.1x tip height from property "
            "lines, 1,500 feet from dwellings. Solar: minimum 150 feet from "
            "property lines with vegetative screening. Reserve buildable area "
            "around landowner homestead and improvements."
        ),
        entity_scope=EntityScope.LANDOWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="County regulations where adopted; contract law",
        issue_category=IssueCategory.SURFACE_USE.value,
        interaction_edges=["shadow_flicker_noise_easements", "landowner_protective_provisions"],
    ))

    # -----------------------------------------------------------------------
    # D19: Estate Planning with Renewable Leases
    # -----------------------------------------------------------------------
    doctrines.append(DoctrineBlock(
        topic="estate_planning_renewable_leases",
        keywords=["estate", "planning", "trust", "inheritance", "death", "succession", "heir"],
        conclusion_template=(
            "Renewable energy leases spanning 30-50 years will almost certainly "
            "outlive the original landowner. Estate planning must address lease "
            "binding on heirs, trust ownership provisions, partition and sale "
            "restrictions, and estate tax valuation of encumbered land. The lease "
            "should include specific succession provisions."
        ),
        reasoning_framework=(
            "A 30-50 year lease creates multi-generational obligations. Key estate "
            "planning issues: (1) Lease should expressly bind heirs, successors, "
            "and assigns — most form leases include this but it must be confirmed; "
            "(2) If land is held in trust, trustee must have authority to execute "
            "lease (review trust document); (3) Life estate holders can lease only "
            "for their lifetime unless remaindermen consent; (4) Partition actions "
            "by co-tenants could disrupt project — lease should include partition "
            "waiver or right of first refusal; (5) Estate tax valuation — "
            "encumbered land may have lower FMV for estate tax purposes, creating "
            "potential benefit; (6) Generation-skipping transfer tax implications; "
            "(7) Step-up in basis for lease payment income does not apply (income "
            "in respect of decedent if accrued); (8) Lease payment characterization "
            "affects estate and income tax treatment; (9) Co-heirs may disagree "
            "on lease continuation — lease should address disputes among owners."
        ),
        key_factors=[
            "Lease binding on heirs and successors provision",
            "Trust ownership and trustee authority to lease",
            "Life estate vs remainder interest lease authority",
            "Partition waiver or ROFR provisions",
            "Estate tax valuation of encumbered land",
            "Income in respect of decedent (IRD) issues",
            "Co-owner dispute resolution mechanism",
            "Generation-skipping transfer tax considerations",
        ],
        primary_authority=[
            "Texas Property Code Ch. 91 (landlord obligations surviving transfer)",
            "IRC Sec. 2031-2033 (estate tax valuation)",
            "IRC Sec. 691 (income in respect of a decedent)",
            "IRC Sec. 2036 (transfers with retained life estate)",
            "Texas Estates Code (trust and estate administration)",
        ],
        burden_holder=BurdenHolder.LANDOWNER.value,
        adversary_position=(
            "Developer is primarily concerned with lease survival across ownership "
            "changes and may resist provisions that give future owners termination rights."
        ),
        counter_arguments=[
            "Heirs should not be bound by unconscionable terms",
            "Changed circumstances over 30-50 years may warrant modification",
            "Periodic review provisions protect both parties",
            "Estate planning flexibility does not threaten lease stability",
            "Developer benefits from clear succession provisions reducing disputes",
        ],
        resolution_strategy=(
            "Include express binding on heirs/successors/assigns. Require trust "
            "documentation review before execution. Obtain remainderman consent "
            "for life estate-owned land. Include co-owner dispute resolution "
            "(arbitration). Engage estate planning attorney to optimize tax "
            "treatment of lease payments and encumbered land valuation."
        ),
        entity_scope=EntityScope.LANDOWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Texas Property Code; Texas Estates Code; IRC estate provisions",
        issue_category=IssueCategory.ESTATE_PLANNING.value,
        interaction_edges=["lease_vs_easement_structure", "assignment_financing_provisions"],
    ))

    # -----------------------------------------------------------------------
    # D20: Gross Revenue Definition and Curtailment
    # -----------------------------------------------------------------------
    doctrines.append(DoctrineBlock(
        topic="gross_revenue_definition_curtailment",
        keywords=["gross revenue", "revenue", "curtailment", "definition", "net", "deduction"],
        conclusion_template=(
            "Gross revenue for royalty purposes must be defined broadly to include "
            "all project income: energy sales, capacity payments, RECs, ancillary "
            "services, and curtailment compensation. Deductions should be limited "
            "to transmission losses only. Curtailment revenue (including deemed "
            "energy payments) must be included in gross revenue."
        ),
        reasoning_framework=(
            "Revenue definition is the most contested economic term in renewable "
            "energy leases when landowner receives percentage-based compensation. "
            "Developers seek narrow definitions excluding valuable revenue streams "
            "and broad deduction allowances. Key components: (1) Energy sales — "
            "the primary revenue from power purchase agreements or merchant sales; "
            "(2) Capacity payments — payments for availability regardless of "
            "generation; (3) RECs — Renewable Energy Certificates have significant "
            "independent value ($5-$50+/MWh depending on market); (4) Ancillary "
            "services — frequency regulation, voltage support, spinning reserve; "
            "(5) Curtailment compensation — payments received when grid operator "
            "curtails output (must be included or landowner bears curtailment "
            "risk without upside); (6) Tax credit value — PTC/ITC value is not "
            "typically included in gross revenue but supports argument for higher "
            "base rate; (7) Capacity market payments in restructured markets. "
            "Allowable deductions should be limited to actual transmission "
            "line losses (typically 2-5%), not wheeling charges, scheduling "
            "fees, or administrative costs which are developer operating expenses."
        ),
        key_factors=[
            "Energy sales revenue inclusion",
            "Capacity payment inclusion",
            "REC value inclusion",
            "Ancillary services revenue inclusion",
            "Curtailment compensation treatment",
            "Allowable deductions from gross revenue",
            "Transmission loss calculation methodology",
            "Audit rights for revenue verification",
        ],
        primary_authority=[
            "PPA revenue structures (ERCOT nodal market design)",
            "ERCOT Protocols (energy settlement, congestion revenue rights)",
            "PUCT rules on renewable energy credits",
            "Contract law principles of revenue definition",
        ],
        burden_holder=BurdenHolder.SHARED.value,
        adversary_position=(
            "Developer seeks narrow revenue definition limited to net energy "
            "sales after all project costs, excluding RECs, capacity payments, "
            "and ancillary services."
        ),
        counter_arguments=[
            "Narrow definition allows developer to shift revenue to excluded categories",
            "RECs represent substantial value attributable to the land resource",
            "Capacity payments exist because of installed capacity on landowner's land",
            "Developer can restructure contracts to minimize 'gross revenue' definition",
            "Audit rights without broad definition are meaningless",
        ],
        resolution_strategy=(
            "Define gross revenue as ALL consideration received by developer from "
            "or attributable to the project, including energy sales, capacity "
            "payments, RECs (or their monetary equivalent), ancillary services, "
            "curtailment compensation, insurance proceeds for lost production, "
            "and any other project revenue. Deductions limited to metered "
            "transmission losses only. Annual audit rights at developer cost."
        ),
        entity_scope=EntityScope.LANDOWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Contract law; oil and gas royalty analogy cases",
        issue_category=IssueCategory.PAYMENT_STRUCTURE.value,
        interaction_edges=["per_mw_vs_per_acre_payment", "payment_escalation_structures"],
    ))

    # -----------------------------------------------------------------------
    # D21-D42: Additional doctrine blocks
    # -----------------------------------------------------------------------

    doctrines.append(DoctrineBlock(
        topic="split_estate_wind_solar",
        keywords=["split", "estate", "mineral", "surface", "severed", "ownership"],
        conclusion_template=(
            "In split estate situations where minerals are severed from the surface, "
            "wind/solar developers must conduct thorough mineral title examination "
            "to identify all mineral owners and negotiate surface use agreements "
            "to prevent future conflicts with the dominant mineral estate."
        ),
        reasoning_framework=(
            "Texas recognizes the mineral estate as dominant with implied right to "
            "use the surface for mineral extraction. When minerals are severed "
            "(common in West Texas after decades of oil and gas activity), the "
            "surface owner can lease for wind/solar but cannot guarantee freedom "
            "from mineral operations. Due diligence requires: (1) Full mineral "
            "title examination; (2) Identification of all current mineral owners; "
            "(3) Assessment of existing mineral leases and operations; (4) "
            "Evaluation of mineral development probability; (5) Negotiation of "
            "surface use waivers or agreements with mineral owners. Developer "
            "should obtain title insurance endorsement covering mineral estate "
            "conflicts. Lease representations should be limited — landowner "
            "cannot warrant mineral estate rights they do not own."
        ),
        key_factors=[
            "Mineral title examination depth and scope",
            "Number and identity of severed mineral owners",
            "Existing mineral leases and drilling activity",
            "Probability of future mineral development",
            "Surface use waiver negotiation with mineral owners",
            "Title insurance endorsement availability",
            "Landowner representations and limitations",
            "Indemnification for mineral estate interference",
        ],
        primary_authority=[
            "Texas Natural Resources Code Ch. 91",
            "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
            "Coyote Lake Ranch LLC v. City of Lubbock, 498 S.W.3d 53 (Tex. 2016)",
        ],
        burden_holder=BurdenHolder.DEVELOPER.value,
        adversary_position="Developer seeks landowner warranty of no mineral conflicts.",
        counter_arguments=[
            "Landowner cannot control mineral estate they do not own",
            "Mineral title risk is developer due diligence responsibility",
            "Warranty of mineral estate rights is impossible for surface owner",
        ],
        resolution_strategy=(
            "Comprehensive mineral title search by developer. Negotiate surface "
            "use agreements with key mineral owners. Limited landowner representations "
            "to actual knowledge only."
        ),
        entity_scope=EntityScope.SURFACE_OWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Texas mineral law; Getty Oil",
        issue_category=IssueCategory.OIL_GAS_COEXISTENCE.value,
    ))

    doctrines.append(DoctrineBlock(
        topic="macrs_depreciation_strategy",
        keywords=["MACRS", "depreciation", "accelerated", "bonus", "section 168", "tax"],
        conclusion_template=(
            "Wind and solar equipment qualifies for 5-year MACRS depreciation under "
            "IRC Sec. 168, with 100% bonus depreciation available through 2026 "
            "(phasing down 20% annually). Combined with ITC/PTC, MACRS significantly "
            "enhances project economics and supports higher landowner payments."
        ),
        reasoning_framework=(
            "MACRS depreciation allows wind/solar equipment to be depreciated over "
            "5 years using 200% declining balance method, generating substantial "
            "tax deductions in early project years. Bonus depreciation under IRC "
            "Sec. 168(k) allows 100% first-year deduction for property placed in "
            "service through 2026, phasing to 80% (2027), 60% (2028), etc. When "
            "ITC is elected, the depreciable basis is reduced by 50% of the ITC "
            "amount. MACRS plus ITC/PTC creates effective federal subsidies of "
            "40-60% of project cost, driving project economics. Landowners should "
            "understand these economics to negotiate fair compensation."
        ),
        key_factors=[
            "5-year MACRS recovery period for wind/solar",
            "Bonus depreciation percentage by placed-in-service year",
            "ITC basis reduction (50% of ITC amount)",
            "Tax equity investor depreciation allocation",
            "Phase-down schedule for bonus depreciation",
            "Cost segregation analysis for project components",
        ],
        primary_authority=[
            "IRC Sec. 168(e)(3)(B)(vi) (5-year MACRS for solar/wind)",
            "IRC Sec. 168(k) (bonus depreciation)",
            "IRC Sec. 50(c) (basis reduction for ITC property)",
        ],
        burden_holder=BurdenHolder.DEVELOPER.value,
        adversary_position="Developer treats MACRS as developer-only benefit in lease negotiations.",
        counter_arguments=[
            "MACRS benefit derives from investment on landowner's property",
            "Tax benefits enhance project economics that should be shared",
            "Competing developers will reflect MACRS in higher lease offers",
        ],
        resolution_strategy="Structure lease payments reflecting full project economics including MACRS.",
        entity_scope=EntityScope.DEVELOPER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="IRC Sec. 168; IRS depreciation guidance",
        issue_category=IssueCategory.TAX_INCENTIVE.value,
    ))

    doctrines.append(DoctrineBlock(
        topic="resource_assessment_easement_terms",
        keywords=["met tower", "anemometer", "resource", "assessment", "easement", "wind study"],
        conclusion_template=(
            "Resource assessment easements for meteorological towers or solar "
            "irradiance stations should be limited to 3-5 years, require annual "
            "payments, include restoration obligations, and grant no rights to "
            "future development without separate lease negotiation."
        ),
        reasoning_framework=(
            "Before committing to a full lease, developers often seek resource "
            "assessment easements to install meteorological (met) towers for wind "
            "measurement or pyranometers for solar irradiance data. Key terms: "
            "(1) Duration limited to assessment period only; (2) Annual payment "
            "for easement area; (3) No implied right to lease for development; "
            "(4) Restoration obligation upon removal; (5) Landowner right to "
            "data access (or at minimum, summary data); (6) Insurance and "
            "indemnification during assessment. Met towers are typically 60-80m "
            "with guy wires requiring larger footprint than monopole designs."
        ),
        key_factors=[
            "Easement duration and extension terms",
            "Annual payment for assessment period",
            "Equipment specifications and footprint",
            "Restoration obligations on removal",
            "Data sharing or access provisions",
            "Insurance requirements during assessment",
            "Right of first negotiation for future lease",
            "No implied development rights",
        ],
        primary_authority=[
            "General easement law principles",
            "AWEA resource assessment best practices",
            "FAA lighting requirements for met towers over 200 feet",
        ],
        burden_holder=BurdenHolder.DEVELOPER.value,
        adversary_position="Developer seeks broad assessment easement with implied development rights.",
        counter_arguments=[
            "Assessment easement should not create development entitlement",
            "Landowner retains full negotiating leverage for development lease",
            "Short duration prevents indefinite property encumbrance",
        ],
        resolution_strategy="Strict time-limited easement with no implied development rights and ROFN only.",
        entity_scope=EntityScope.LANDOWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Easement law; contract law",
        issue_category=IssueCategory.RESOURCE_ASSESSMENT.value,
    ))

    doctrines.append(DoctrineBlock(
        topic="transmission_easement_negotiation",
        keywords=["transmission", "easement", "gen-tie", "line", "corridor", "right of way"],
        conclusion_template=(
            "Transmission and gen-tie easements require separate negotiation from "
            "the generation lease. Compensation should be per-rod or per-linear-foot "
            "with separate structure payments. Easement width should be minimized "
            "and restoration obligations included."
        ),
        reasoning_framework=(
            "Transmission easements for gen-tie lines connecting renewable energy "
            "projects to substations or points of interconnection cross multiple "
            "properties and require separate negotiation. Key terms: (1) Easement "
            "width (typically 75-150 feet for 345kV); (2) Compensation per linear "
            "foot or per rod ($10-$50/linear foot depending on voltage and location); "
            "(3) Structure payments for each pole/tower ($2,000-$10,000 each); (4) "
            "Construction damage payments; (5) Vegetation management restrictions; "
            "(6) Landowner use limitations within corridor; (7) Emergency access "
            "provisions. Gen-tie developers generally lack eminent domain authority "
            "unless they qualify as a utility, making negotiation leverage stronger."
        ),
        key_factors=[
            "Easement width by voltage class",
            "Per-linear-foot or per-rod compensation",
            "Structure payments per pole/tower",
            "Construction damage and restoration",
            "Vegetation management obligations",
            "Landowner use rights within corridor",
            "Duration (perpetual vs term)",
            "Eminent domain authority assessment",
        ],
        primary_authority=[
            "Texas Utilities Code Ch. 37",
            "Texas Property Code Ch. 21",
            "Transmission easement market rate surveys",
        ],
        burden_holder=BurdenHolder.DEVELOPER.value,
        adversary_position="Developer seeks minimum-cost easement with broad rights.",
        counter_arguments=[
            "Transmission line permanently impacts land use and value",
            "Market rates for transmission easements are well-established",
            "Landowner has leverage if developer lacks eminent domain",
        ],
        resolution_strategy="Negotiate at market rates with structure payments, minimize width, require restoration.",
        entity_scope=EntityScope.LANDOWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Texas Utilities Code; Texas Property Code",
        issue_category=IssueCategory.TRANSMISSION.value,
    ))

    doctrines.append(DoctrineBlock(
        topic="tax_equity_financing_structure",
        keywords=["tax equity", "partnership flip", "financing", "investor", "structure"],
        conclusion_template=(
            "Tax equity financing using partnership flip structures is the primary "
            "mechanism for monetizing PTC/ITC. Lease provisions must accommodate "
            "the partnership structure without granting the tax equity investor "
            "rights beyond the developer's lease rights."
        ),
        reasoning_framework=(
            "Most renewable energy projects use tax equity partnerships to monetize "
            "federal tax credits. In a partnership flip, a tax equity investor "
            "contributes 35-50% of project cost in exchange for 99% of tax benefits "
            "until achieving target return, then the allocation flips. Lease "
            "implications: (1) Developer assigns lease to project company (SPV); "
            "(2) SPV is owned by developer and tax equity investor; (3) SNDA "
            "required for tax equity investor; (4) Estoppel certificates needed "
            "at financing closing; (5) Assignment provisions must accommodate "
            "change of membership interests without landowner consent; (6) "
            "Lease must be subordinated to project liens but protected by "
            "non-disturbance agreement."
        ),
        key_factors=[
            "Partnership flip structure mechanics",
            "Tax equity investor rights under lease",
            "SPV assignment and consent requirements",
            "SNDA provisions for tax equity",
            "Estoppel certificate requirements",
            "Change of membership interest treatment",
            "Subordination and non-disturbance",
            "Tax equity foreclosure protections",
        ],
        primary_authority=[
            "Rev. Proc. 2007-65 (partnership flip safe harbor)",
            "IRC Sec. 704(b) (partnership allocations)",
            "Treasury Reg. 1.704-1(b)(2) (substantial economic effect)",
        ],
        burden_holder=BurdenHolder.LENDER.value,
        adversary_position="Tax equity investor seeks maximum protections beyond standard lease rights.",
        counter_arguments=[
            "Tax equity rights should not exceed developer rights under lease",
            "Landowner should not become party to financing disputes",
            "Standard SNDA and estoppel are sufficient protection",
        ],
        resolution_strategy="Accommodate reasonable tax equity provisions within existing lease framework.",
        entity_scope=EntityScope.LENDER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Rev. Proc. 2007-65; partnership tax law",
        issue_category=IssueCategory.FINANCING.value,
    ))

    doctrines.append(DoctrineBlock(
        topic="wind_lease_operations_period",
        keywords=["operations", "term", "duration", "renewal", "extension", "wind"],
        conclusion_template=(
            "Wind lease operations periods typically run 25-35 years with 1-2 "
            "renewal options of 5-10 years each. Total lease duration should not "
            "exceed 50 years. Renewal should require affirmative landowner consent "
            "with renegotiated payment terms reflecting current market conditions."
        ),
        reasoning_framework=(
            "The operations period begins at commercial operation date (COD) and "
            "is the primary revenue-generating term. Modern wind turbines have "
            "design lifespans of 25-30 years. Key issues: (1) Initial term should "
            "match turbine design life, not exceed it; (2) Renewal options allow "
            "repowering with new turbines; (3) Renewal terms should be renegotiated "
            "not automatically at original rates; (4) Total term including all "
            "renewals should cap at 50 years; (5) Continuous operations requirement "
            "prevents developer from holding lease without generating power; (6) "
            "Cessation of operations clause provides termination right if turbines "
            "stop generating for 12-24 consecutive months."
        ),
        key_factors=[
            "Initial operations term (25-35 years)",
            "Number and duration of renewal options",
            "Total maximum lease duration cap",
            "Renewal consent and renegotiation requirements",
            "Continuous operations requirement",
            "Cessation of operations termination trigger",
            "Repowering provisions and consent",
            "Market rate reset at renewal",
        ],
        primary_authority=[
            "Wind energy lease market standards",
            "Turbine manufacturer design life specifications",
            "Contract law principles of lease duration",
        ],
        burden_holder=BurdenHolder.SHARED.value,
        adversary_position="Developer seeks automatic renewal at original terms for maximum duration.",
        counter_arguments=[
            "Automatic renewal locks in below-market rates for decades",
            "Technology changes may make original terms inappropriate",
            "Landowner should benefit from market improvements at renewal",
            "50-year cap is reasonable maximum for any land agreement",
        ],
        resolution_strategy="30-year initial term, one 10-year renewal with renegotiated terms, 50-year max.",
        entity_scope=EntityScope.LANDOWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Contract law; market practice",
        issue_category=IssueCategory.WIND_LEASE_STRUCTURE.value,
    ))

    doctrines.append(DoctrineBlock(
        topic="solar_operations_decommissioning",
        keywords=["solar", "operations", "decommissioning", "end of life", "removal", "panel"],
        conclusion_template=(
            "Solar panel end-of-life creates specific decommissioning challenges "
            "including hazardous material handling (cadmium in CdTe panels), panel "
            "recycling requirements, inverter replacement cycles, and site "
            "restoration to pre-construction agricultural capability."
        ),
        reasoning_framework=(
            "Solar panels degrade 0.5-0.8% annually, reaching 80% original capacity "
            "at 25-30 years. End-of-life decommissioning involves: (1) Panel removal "
            "and recycling (CdTe panels may contain cadmium requiring hazmat handling); "
            "(2) Racking and mounting system removal; (3) Inverter and transformer "
            "removal; (4) Underground cable removal or abandonment in place; (5) "
            "Foundation removal; (6) Access road removal unless landowner elects "
            "to retain; (7) Topsoil replacement and revegetation; (8) Stormwater "
            "management system removal. Key cost drivers: panel recycling ($15-25/panel), "
            "racking removal ($3-5/panel), civil restoration ($5,000-10,000/acre). "
            "Total decommissioning cost: $15,000-$40,000 per MW installed."
        ),
        key_factors=[
            "Panel technology and hazardous material content",
            "Panel recycling vs landfill disposal requirements",
            "Racking and mounting system removal scope",
            "Underground infrastructure abandonment vs removal",
            "Topsoil restoration and revegetation timeline",
            "Estimated decommissioning cost per MW",
            "Financial assurance amount and timing",
            "State and federal hazardous waste regulations",
        ],
        primary_authority=[
            "RCRA hazardous waste regulations (40 CFR 260-265)",
            "EPA solar panel end-of-life management guidance",
            "SEIA National Solar Panel Recycling Program",
            "State hazardous waste regulations",
        ],
        burden_holder=BurdenHolder.DEVELOPER.value,
        adversary_position="Developer seeks to credit full salvage value against decommissioning cost.",
        counter_arguments=[
            "Panel salvage value is minimal for degraded panels",
            "Recycling markets for solar panels are immature",
            "Hazardous material handling adds significant cost",
            "Salvage value estimates are speculative for 25-30 year horizon",
        ],
        resolution_strategy="Full decommissioning bond at COD, salvage credit capped at 25% of cost estimate.",
        entity_scope=EntityScope.LANDOWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="RCRA; EPA guidance; contract law",
        issue_category=IssueCategory.DECOMMISSIONING.value,
    ))

    doctrines.append(DoctrineBlock(
        topic="texas_county_regulation_wind_solar",
        keywords=["texas", "county", "regulation", "ordinance", "permitting", "zoning"],
        conclusion_template=(
            "Texas has no state-level permitting for wind or solar projects. Counties "
            "with populations under certain thresholds may regulate through local "
            "ordinances covering setbacks, noise, decommissioning, and road use "
            "agreements. Developers must comply with applicable county regulations "
            "and tax abatement agreements under Ch. 312/313."
        ),
        reasoning_framework=(
            "Texas's deregulated approach means no state agency issues permits for "
            "renewable energy projects (unlike most states). Regulatory authority "
            "resides with: (1) Counties — may adopt wind/solar regulations under "
            "Local Government Code Ch. 232; (2) Municipalities — zoning and building "
            "code authority within ETJ; (3) FAA — lighting requirements for structures "
            "over 200 feet; (4) USFWS — eagle and wildlife permits; (5) TCEQ — "
            "stormwater permits during construction; (6) TxDOT — access permits for "
            "state highways. Many counties have adopted wind energy regulations "
            "(Nolan, Taylor, Shackelford, Callahan, etc.) with varying setback, "
            "noise, and decommissioning requirements. Ch. 312 tax abatement "
            "agreements and former Ch. 313 (expired 2022, potential successor "
            "legislation) provide property tax reductions in exchange for local "
            "economic commitments."
        ),
        key_factors=[
            "Applicable county wind/solar ordinance requirements",
            "Municipal ETJ and zoning applicability",
            "FAA obstruction evaluation and lighting",
            "TCEQ stormwater permit requirements",
            "TxDOT access permit needs",
            "Ch. 312 tax abatement agreement status",
            "Former Ch. 313 value limitation status",
            "Road use and maintenance agreement requirements",
        ],
        primary_authority=[
            "Texas Local Government Code Ch. 232",
            "Texas Tax Code Ch. 312 (tax abatement)",
            "FAA Advisory Circular 70/7460-1M",
            "TCEQ stormwater general permit TXR150000",
        ],
        burden_holder=BurdenHolder.DEVELOPER.value,
        adversary_position="Developer seeks to minimize regulatory compliance costs and obligations.",
        counter_arguments=[
            "Regulatory compliance is developer responsibility",
            "County ordinances protect landowner and community interests",
            "Non-compliance creates liability for landowner as property owner",
        ],
        resolution_strategy="Require developer compliance with all applicable regulations at developer cost.",
        entity_scope=EntityScope.DEVELOPER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Texas Local Government Code; county ordinances",
        issue_category=IssueCategory.TEXAS_REGULATORY.value,
    ))

    doctrines.append(DoctrineBlock(
        topic="mineral_owner_surface_waiver",
        keywords=["mineral", "waiver", "surface", "consent", "agreement", "accommodation"],
        conclusion_template=(
            "Surface use waivers from mineral owners are the gold standard for "
            "protecting renewable energy projects from mineral estate conflicts. "
            "Waivers should restrict mineral operations in defined exclusion zones "
            "around turbines/panels in exchange for negotiated compensation."
        ),
        reasoning_framework=(
            "Rather than relying solely on the accommodation doctrine (which requires "
            "litigation to enforce), proactive surface use waivers with mineral owners "
            "provide contractual certainty. A surface waiver agreement typically: (1) "
            "Defines exclusion zones around renewable energy facilities where no "
            "surface mineral operations permitted; (2) Allows directional drilling "
            "from pads outside exclusion zones; (3) Provides compensation to mineral "
            "owner for surface restrictions ($500-$5,000/acre common); (4) Preserves "
            "mineral owner's right to develop from adjacent tracts; (5) Runs with "
            "the land binding future mineral owners. Cost of surface waivers should "
            "be developer responsibility as project development expense."
        ),
        key_factors=[
            "Exclusion zone dimensions and location",
            "Compensation to mineral owner for restrictions",
            "Directional drilling accommodation from outside zones",
            "Duration matching the renewable energy lease",
            "Binding on successors and assigns",
            "Recording requirements",
            "Developer responsibility for waiver acquisition costs",
            "Interaction with existing mineral leases",
        ],
        primary_authority=[
            "Texas Property Code (surface waiver provisions)",
            "Contract law principles",
            "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
        ],
        burden_holder=BurdenHolder.DEVELOPER.value,
        adversary_position="Mineral owner demands excessive compensation for surface restrictions.",
        counter_arguments=[
            "Directional drilling preserves mineral access from outside exclusion zones",
            "Mineral owner retains all subsurface rights",
            "Compensation reflects surface restriction only not mineral value",
        ],
        resolution_strategy="Negotiate reasonable exclusion zones with fair surface-only compensation.",
        entity_scope=EntityScope.MINERAL_OWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Contract law; Texas property law",
        issue_category=IssueCategory.OIL_GAS_COEXISTENCE.value,
    ))

    doctrines.append(DoctrineBlock(
        topic="tax_treatment_lease_vs_easement",
        keywords=["tax", "treatment", "income", "lease", "easement", "capital gain", "ordinary"],
        conclusion_template=(
            "Lease payments are taxed as ordinary income under IRC Sec. 61. Easement "
            "payments may qualify for capital gain treatment if structured as sale of "
            "a real property interest. The tax characterization depends on the legal "
            "nature of the interest conveyed, not the label used by the parties."
        ),
        reasoning_framework=(
            "The distinction between lease and easement has significant tax consequences. "
            "Lease payments: ordinary income taxed at rates up to 37%. Easement payments: "
            "if treated as sale of real property interest, taxed at long-term capital gain "
            "rates (20% max). IRS examines substance over form — calling an agreement an "
            "'easement' does not guarantee capital gain treatment if the economic substance "
            "is a lease. Key factors for capital gain treatment: (1) Easement must convey "
            "a permanent or very long-term interest; (2) Payment must be for the property "
            "interest, not periodic rent; (3) Landowner's basis in the easement area "
            "reduces gain; (4) IRC Sec. 1231 governs real property used in trade or "
            "business. Annual payments under either structure are likely ordinary income "
            "regardless of label. Lump-sum easement payments have strongest argument "
            "for capital gain treatment."
        ),
        key_factors=[
            "Legal structure (lease vs easement)",
            "Payment timing (lump sum vs periodic)",
            "Duration of interest conveyed",
            "Landowner's basis in the property",
            "IRC Sec. 1231 trade or business property status",
            "Self-employment tax implications",
            "State income tax treatment",
            "IRS examination risk factors",
        ],
        primary_authority=[
            "IRC Sec. 61 (gross income definition)",
            "IRC Sec. 1231 (property used in trade or business)",
            "IRC Sec. 1001 (gain from sale of property)",
            "IRS Revenue Ruling 72-85",
            "Dunn v. Commissioner, T.C. Memo 2013-43",
        ],
        burden_holder=BurdenHolder.LANDOWNER.value,
        adversary_position="IRS may recharacterize easement payments as ordinary lease income.",
        counter_arguments=[
            "Substance of arrangement determines tax treatment not label",
            "Periodic payments favor ordinary income characterization",
            "Easement granting exclusive possession looks like a lease",
        ],
        resolution_strategy="Consult tax advisor on optimal structure. Lump-sum easement for capital gain potential.",
        entity_scope=EntityScope.LANDOWNER.value,
        confidence=ConfidenceLevel.DISCLOSURE.value,
        confidence_stratification="DISCLOSURE",
        controlling_precedent="IRC Sec. 61; IRC Sec. 1231; Rev. Rul. 72-85",
        issue_category=IssueCategory.TAX_INCENTIVE.value,
    ))

    doctrines.append(DoctrineBlock(
        topic="repowering_provisions",
        keywords=["repowering", "repower", "upgrade", "replace", "turbine", "technology"],
        conclusion_template=(
            "Repowering provisions allowing replacement of aging turbines with newer, "
            "larger equipment require explicit landowner consent with renegotiated "
            "terms. New turbines may require different setbacks, create different "
            "noise/flicker profiles, and warrant increased compensation reflecting "
            "higher generation capacity."
        ),
        reasoning_framework=(
            "Wind turbine technology improves rapidly — modern turbines generate "
            "2-3x the power of models installed 15 years ago. Repowering (replacing "
            "old turbines with new) extends project life and increases revenue. "
            "Lease implications: (1) Repowering is essentially a new project on "
            "existing land; (2) Larger turbines may violate existing setback "
            "provisions; (3) Noise and flicker profiles change; (4) Foundation "
            "replacement may be needed; (5) Construction disruption repeats; (6) "
            "Increased capacity warrants increased payment. Developer should not "
            "have automatic repowering rights — this must be negotiated."
        ),
        key_factors=[
            "Repowering consent requirements",
            "Updated setback analysis for new turbines",
            "Revised noise and flicker assessments",
            "Payment adjustment for increased capacity",
            "Construction disruption compensation",
            "New decommissioning cost estimate",
            "Environmental permitting for new equipment",
            "Technology specification limits",
        ],
        primary_authority=[
            "Contract law; lease modification principles",
            "County ordinance compliance for new turbine specifications",
            "FAA lighting requirements for taller turbines",
        ],
        burden_holder=BurdenHolder.SHARED.value,
        adversary_position="Developer seeks automatic repowering rights without consent or increased payment.",
        counter_arguments=[
            "Repowering constitutes material change to lease terms",
            "Larger turbines create new impacts requiring new consent",
            "Increased revenue should mean increased landowner payment",
        ],
        resolution_strategy="Require affirmative consent for repowering with renegotiated terms and new impact assessment.",
        entity_scope=EntityScope.LANDOWNER.value,
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Contract law; lease modification principles",
        issue_category=IssueCategory.WIND_LEASE_STRUCTURE.value,
    ))

    logger.info(
        "Doctrine cache built: {count} blocks across {categories} categories",
        count=len(doctrines),
        categories=len(set(d.issue_category for d in doctrines)),
    )
    return doctrines


# ---------------------------------------------------------------------------
# Interaction edges between doctrines
# ---------------------------------------------------------------------------
INTERACTION_GRAPH: dict[str, list[str]] = {
    "wind_lease_option_period": ["wind_lease_operations_period", "payment_escalation_structures", "ercot_interconnection_requirements"],
    "solar_lease_development_construction": ["decommissioning_bond_requirements", "investment_tax_credit_solar", "agricultural_exemption_preservation"],
    "per_mw_vs_per_acre_payment": ["payment_escalation_structures", "gross_revenue_definition_curtailment"],
    "payment_escalation_structures": ["per_mw_vs_per_acre_payment", "gross_revenue_definition_curtailment"],
    "accommodation_doctrine_surface_conflicts": ["split_estate_wind_solar", "mineral_owner_surface_waiver"],
    "decommissioning_bond_requirements": ["solar_operations_decommissioning", "landowner_protective_provisions"],
    "production_tax_credit_implications": ["investment_tax_credit_solar", "tax_equity_financing_structure", "macrs_depreciation_strategy"],
    "investment_tax_credit_solar": ["production_tax_credit_implications", "macrs_depreciation_strategy"],
    "ercot_interconnection_requirements": ["wind_lease_option_period", "transmission_easement_negotiation", "crez_transmission_eminent_domain"],
    "agricultural_exemption_preservation": ["per_mw_vs_per_acre_payment", "solar_lease_development_construction"],
    "shadow_flicker_noise_easements": ["surface_use_restrictions_setbacks", "landowner_protective_provisions"],
    "crez_transmission_eminent_domain": ["transmission_easement_negotiation", "ercot_interconnection_requirements"],
    "battery_storage_siting": ["decommissioning_bond_requirements", "surface_use_restrictions_setbacks"],
    "eagle_take_permit_environmental": ["wind_lease_option_period", "resource_assessment_easement_terms"],
    "lease_vs_easement_structure": ["tax_treatment_lease_vs_easement", "assignment_financing_provisions"],
    "assignment_financing_provisions": ["tax_equity_financing_structure", "decommissioning_bond_requirements"],
    "estate_planning_renewable_leases": ["lease_vs_easement_structure", "assignment_financing_provisions"],
    "gross_revenue_definition_curtailment": ["per_mw_vs_per_acre_payment", "payment_escalation_structures"],
    "split_estate_wind_solar": ["accommodation_doctrine_surface_conflicts", "mineral_owner_surface_waiver"],
    "repowering_provisions": ["wind_lease_operations_period", "decommissioning_bond_requirements"],
}
