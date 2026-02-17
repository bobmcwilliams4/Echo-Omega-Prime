"""
R05 REPORTING REQUIREMENTS DOCTRINE CACHE

Pre-compiled regulatory reporting requirements for oil & gas operations.
Each doctrine block represents expert knowledge of a specific reporting obligation.

Domain: Oil & Gas Regulatory Reporting
Topics: 52 reporting requirements across production, environmental, safety, and tax domains
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class ConfidenceStratification(str, Enum):
    MANDATORY = "mandatory"
    CLEARLY_REQUIRED = "clearly_required"
    BEST_PRACTICE = "best_practice"
    UNCERTAIN = "uncertain"


@dataclass
class DoctrineBlock:
    """
    Immutable doctrine block containing expert regulatory reporting knowledge.
    """
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
    entity_scope: List[str]
    confidence: float
    confidence_stratification: ConfidenceStratification
    controlling_precedent: Optional[str] = None


# ============================================================================
# PRODUCTION REPORTING DOCTRINES
# ============================================================================

PRODUCTION_MONTHLY_P4 = DoctrineBlock(
    topic="Monthly Production Reports (Form P-4)",
    keywords=["p-4", "monthly production", "production report", "oil production", "gas production", "rrc form p-4"],
    conclusion_template=(
        "Texas operators must file Form P-4 monthly production reports with the Railroad Commission. "
        "Reports are due by the end of the month following production. Failure to file timely results in "
        "penalties of $200 per day per lease, with potential well shut-in orders."
    ),
    reasoning_framework=(
        "Texas Natural Resources Code §91.142 requires all oil and gas operators to file monthly production "
        "reports. The Railroad Commission implements this through Form P-4, which must report gross volumes "
        "produced from each lease during the prior month. The statute places reporting obligation on the "
        "operator of record, not working interest owners or royalty owners. Filing deadline is strictly "
        "enforced - reports due by last day of following month (e.g., January production due Feb 28/29). "
        "Electronic filing through RRC online system is mandatory for operators with 10+ leases. "
        "Penalties accrue daily for late filing: $200/day/lease under Rule 3.75. Repeat violations may "
        "result in shut-in orders under Rule 3.65. Zero production must still be reported (cannot simply "
        "skip filing). Reports must include: lease name, RRC lease number, county, field, gross oil/gas/water "
        "volumes, days produced, disposition method. Amended reports allowed within 90 days without penalty "
        "if filed in good faith to correct errors."
    ),
    key_factors=[
        "Due date: Last day of month following production month",
        "Penalty: $200 per day per lease for late filing",
        "Electronic filing mandatory for operators with 10+ leases",
        "Zero production months must still be reported",
        "Operator of record is responsible party, not working interest owners",
        "Amended reports allowed within 90 days penalty-free if good faith correction",
        "Shut-in orders possible for repeat violations",
        "Must report: gross volumes, days produced, disposition method"
    ],
    primary_authority=[
        "Texas Natural Resources Code §91.142",
        "16 TAC §3.75 (Production Reporting)",
        "16 TAC §3.65 (Enforcement)"
    ],
    burden_holder="Operator of record",
    adversary_position="Railroad Commission enforcement division",
    counter_arguments=[
        "Late filing penalty: $200/day/lease can accumulate rapidly",
        "Shut-in orders are discretionary but used for chronic violators",
        "No force majeure exception for system outages (operator must plan ahead)"
    ],
    resolution_strategy="File timely, maintain filing calendar, use electronic system, file zeros when no production",
    entity_scope=["producer", "operator"],
    confidence=0.95,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="Texas Natural Resources Code §91.142"
)

WELL_COMPLETION_W2 = DoctrineBlock(
    topic="Well Completion Reports (Form W-2)",
    keywords=["w-2", "completion report", "well completion", "completion form", "new well"],
    conclusion_template=(
        "Texas operators must file Form W-2 completion reports within 90 days of rig release or completion operations. "
        "Form W-2 provides detailed completion data including depths, formations, casing, and initial production. "
        "Late filing results in $200/day penalties."
    ),
    reasoning_framework=(
        "16 TAC §3.11 requires Form W-2 for all completed wells (producers or dry holes). Filing deadline is "
        "90 days from rig release. Completion data includes: total depth, plug-back depth if applicable, perforated "
        "intervals, casing program (sizes and depths), cement volumes and tops, fracture treatment details if applicable, "
        "initial 24-hour production test results, formation tops encountered, wellbore schematic. This is separate from "
        "Form W-1 (drilling permit) - W-1 filed before drilling, W-2 filed after completion. W-2 required even for dry holes "
        "or temporarily abandoned wells. Penalty for late filing: $200/day under Rule 3.75. Form W-2 creates official record "
        "of well configuration - critical for spacing units, correlative rights disputes, and subsequent operations. Incomplete "
        "W-2 forms may be rejected, restarting the 90-day clock. Electronic filing available but not mandatory (unlike P-4)."
    ),
    key_factors=[
        "Due date: 90 days from rig release",
        "Required for all wells including dry holes",
        "Must include: depths, casing, perforations, cement, frac data, initial test",
        "Penalty: $200/day for late filing",
        "Separate from Form W-1 (drilling permit)",
        "Creates official well record for spacing and correlative rights",
        "Incomplete forms may be rejected"
    ],
    primary_authority=[
        "16 TAC §3.11 (Well Completion Reports)",
        "16 TAC §3.75 (Penalties)"
    ],
    burden_holder="Operator",
    adversary_position="Railroad Commission",
    counter_arguments=[
        "90-day deadline is strict - no extensions granted",
        "Incomplete submissions restart the clock"
    ],
    resolution_strategy="File within 90 days, ensure complete data, retain rig release documentation",
    entity_scope=["operator"],
    confidence=0.93,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="16 TAC §3.11"
)

PLUGGING_REPORT_H10 = DoctrineBlock(
    topic="Plugging Reports (Form H-10)",
    keywords=["h-10", "plugging report", "well plugging", "abandoned well", "plug report"],
    conclusion_template=(
        "Texas operators must file Form H-10 plugging reports within 30 days of well plugging completion. "
        "Report documents plugging procedure, cement volumes, and final well status. Timely filing releases "
        "performance bond or financial assurance associated with the well."
    ),
    reasoning_framework=(
        "16 TAC §3.14 requires Form H-10 for all plugged wells. Filing deadline: 30 days from plugging completion. "
        "Plugging report must document: cement plug locations and volumes, perforations squeezed, casing cut depths, "
        "surface restoration, disposal of equipment and fluids, contractor certification, photographs if required by district. "
        "Purpose: verify well is properly abandoned and poses no environmental or safety risk. H-10 approval triggers "
        "release of financial assurance (performance bond or alternative) that was required for the well. Failure to file "
        "timely can delay bond release and may result in enforcement action. RRC district office may inspect plugging job "
        "before approving H-10 - inspection required for wells in urban areas or near water wells. Rejected H-10 forms "
        "(incomplete or improper plugging procedure) require re-work and re-filing. No well can be legally considered "
        "'abandoned' until H-10 is approved. Operator remains liable for well until H-10 approval."
    ),
    key_factors=[
        "Due date: 30 days from plugging completion",
        "Required to release performance bond",
        "Must document: cement plugs, casing cuts, surface restoration",
        "District office may inspect before approval",
        "Operator liable until H-10 approved",
        "Rejected forms require re-work and re-filing"
    ],
    primary_authority=[
        "16 TAC §3.14 (Plugging)",
        "16 TAC §3.78 (Financial Assurance)"
    ],
    burden_holder="Operator",
    adversary_position="Railroad Commission District Office",
    counter_arguments=[
        "Bond not released until H-10 approved",
        "Improper plugging requires expensive re-work"
    ],
    resolution_strategy="Follow RRC plugging guidelines, document thoroughly, file within 30 days, coordinate with district office",
    entity_scope=["operator"],
    confidence=0.94,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="16 TAC §3.14"
)

ORGANIZATION_REPORT_P5 = DoctrineBlock(
    topic="Organization Reports (Form P-5)",
    keywords=["p-5", "organization report", "operator change", "change of operator", "new operator"],
    conclusion_template=(
        "Texas operators must file Form P-5 organization reports when acquiring leases or wells, or when organizational "
        "changes occur. Form P-5 establishes operator of record and is prerequisite for filing production reports and "
        "receiving regulatory approvals."
    ),
    reasoning_framework=(
        "16 TAC §3.1 requires Form P-5 to establish operator of record with Railroad Commission. P-5 must be filed: "
        "(1) before first well permit application, (2) when acquiring existing leases/wells, (3) when operator entity "
        "undergoes name change, merger, or reorganization. Form P-5 includes: legal entity name, mailing address, "
        "responsible party designation, organizational form (corporation, LLC, partnership, etc.), federal tax ID, "
        "financial assurance information. P-5 creates the official link between operator entity and RRC operator number. "
        "Without approved P-5, operator cannot: file drilling permits (W-1), file production reports (P-4), receive "
        "regulatory approvals. When acquiring existing operations, new operator must file P-5 AND file transfer paperwork "
        "to assume operator responsibility. Prior operator remains liable until transfer is approved. P-5 amendments "
        "required within 30 days of any organizational change. Form P-5 is also trigger for financial assurance requirements "
        "under Rule 3.78 - new operators must post bond or equivalent based on well count and production history."
    ),
    key_factors=[
        "Required before first drilling permit",
        "Required when acquiring existing leases/wells",
        "Establishes operator of record and RRC operator number",
        "Amendments due within 30 days of organizational changes",
        "Prerequisite for filing permits and production reports",
        "Triggers financial assurance requirements",
        "Prior operator liable until transfer approved"
    ],
    primary_authority=[
        "16 TAC §3.1 (Organization Reports)",
        "16 TAC §3.78 (Financial Assurance)"
    ],
    burden_holder="New operator",
    adversary_position="Railroad Commission",
    counter_arguments=[
        "Cannot operate without approved P-5",
        "Financial assurance required before approval"
    ],
    resolution_strategy="File P-5 immediately upon formation or acquisition, maintain current organizational information, post required bonds",
    entity_scope=["operator"],
    confidence=0.96,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="16 TAC §3.1"
)

GAS_FLARING_REPORT = DoctrineBlock(
    topic="Gas Flaring Reports",
    keywords=["gas flaring", "flaring report", "flared gas", "vented gas", "gas waste"],
    conclusion_template=(
        "Texas operators must obtain Railroad Commission approval before flaring or venting gas. Flaring without "
        "approval violates waste prevention rules. Exception reports required for emergency flaring within 48 hours."
    ),
    reasoning_framework=(
        "16 TAC §3.32 prohibits waste of natural gas. Flaring or venting constitutes waste unless authorized by RRC. "
        "Two approval pathways: (1) Commission exception (Rule 32 exception) for temporary flaring during completions, "
        "workovers, or when pipeline capacity unavailable, filed on Form P-18; (2) Field rule with flaring allowance. "
        "Emergency flaring (safety-related) allowed without prior approval BUT operator must file exception report within "
        "48 hours documenting: date, duration, volumes, reason for emergency, corrective action taken. Routine flaring "
        "without approval is waste and subject to enforcement: shut-in orders, penalties, possible plugging. New wells: "
        "completion flaring allowed for limited period (typically 10-45 days depending on district) under statewide Rule 32. "
        "Long-term flaring requires formal exception showing: gas pipeline unavailable, uneconomic to connect, gas composition "
        "makes sales impractical. Environmental consideration: TCEQ may also regulate flaring emissions under Clean Air Act - "
        "major sources require air permit. Best practice: capture and sell gas, or reinject if sales unavailable."
    ),
    key_factors=[
        "Flaring without RRC approval violates waste prevention rules",
        "Emergency flaring allowed but 48-hour exception report required",
        "New well completion flaring allowed for limited period (10-45 days)",
        "Long-term flaring requires formal Commission exception (Form P-18)",
        "TCEQ air permit may also be required for major sources",
        "Enforcement: shut-in orders and penalties for waste violations"
    ],
    primary_authority=[
        "16 TAC §3.32 (Gas Waste Prevention)",
        "Form P-18 (Exception to Commission Rules)",
        "30 TAC §116 (TCEQ Air Permits)"
    ],
    burden_holder="Operator",
    adversary_position="Railroad Commission, TCEQ",
    counter_arguments=[
        "Flaring without approval is waste - strict enforcement",
        "Economic hardship is not automatic justification"
    ],
    resolution_strategy="Obtain RRC exception before flaring, file emergency reports within 48 hours, plan for gas sales or reinjection",
    entity_scope=["operator", "producer"],
    confidence=0.91,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="16 TAC §3.32"
)

# ============================================================================
# SEVERANCE TAX AND ROYALTY REPORTING
# ============================================================================

SEVERANCE_TAX_REPORT = DoctrineBlock(
    topic="Severance Tax Reports (Texas Comptroller)",
    keywords=["severance tax", "production tax", "tax report", "comptroller", "texas tax"],
    conclusion_template=(
        "Texas oil and gas producers must file monthly severance tax reports with the Comptroller. Oil production "
        "taxed at 4.6% of market value, gas at 7.5%. Reports due on the 20th of month following production."
    ),
    reasoning_framework=(
        "Texas Tax Code §201 (oil) and §202 (gas) impose severance taxes on all oil and gas produced and saved in Texas. "
        "Tax rates: crude oil 4.6% of market value, natural gas 7.5% of market value. First purchaser typically withholds "
        "and remits tax, but producer is ultimately liable. Monthly reporting due 20th of month following production "
        "(e.g., January production due February 20). Report filed with Texas Comptroller, not Railroad Commission. "
        "Taxpayer must hold severance tax permit from Comptroller. Exemptions: stripper well exemption (oil wells producing "
        "≤10 bbl/day qualify for reduced rate), high-cost gas exemption (qualifying high-cost wells), EOR projects may qualify "
        "for reduced rates, certain recompletions and new drill wells in inactive fields qualify for temporary reductions. "
        "Market value calculation: weighted average price received during the month, minus post-production costs if arms-length "
        "sale. Penalties for late filing: 5% if 1-30 days late, 10% if >30 days, plus 12% annual interest on unpaid tax. "
        "Audit risk: Comptroller audits producers on 3-5 year cycles, examining volume reporting, price calculations, and exemption claims."
    ),
    key_factors=[
        "Tax rates: 4.6% oil, 7.5% gas",
        "Due date: 20th of month following production",
        "First purchaser typically withholds, producer ultimately liable",
        "Stripper well exemption available (≤10 bbl/day oil)",
        "Market value = weighted average price less post-production costs",
        "Penalties: 5-10% plus 12% annual interest for late filing",
        "Comptroller audits on 3-5 year cycles"
    ],
    primary_authority=[
        "Texas Tax Code §201 (Oil Severance Tax)",
        "Texas Tax Code §202 (Gas Severance Tax)",
        "34 TAC §3.1-3.100 (Comptroller Rules)"
    ],
    burden_holder="Producer (first taker withholds but producer liable)",
    adversary_position="Texas Comptroller",
    counter_arguments=[
        "Producer liable even if first purchaser fails to withhold",
        "Exemption claims subject to audit and reversal"
    ],
    resolution_strategy="File timely, obtain severance tax permit, document exemption eligibility, retain price and volume records",
    entity_scope=["producer", "working_interest"],
    confidence=0.94,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="Texas Tax Code §201, §202"
)

ROYALTY_OWNER_STATEMENTS = DoctrineBlock(
    topic="Royalty Owner Payment Statements",
    keywords=["royalty", "royalty statement", "division order", "revenue statement", "royalty payment"],
    conclusion_template=(
        "Texas law does not mandate specific format for royalty statements, but industry practice and division order "
        "terms typically require monthly statements showing production volumes, prices, deductions, and net payment."
    ),
    reasoning_framework=(
        "No Texas statute prescribes royalty statement requirements, but common law and division order contracts create "
        "reporting obligations. Typical royalty statement includes: lease name, well name, production month, gross volumes "
        "produced, royalty decimal interest, gross value (price × volume × interest), deductions (post-production costs if "
        "permitted by lease), taxes withheld, net payment. Texas Natural Resources Code §91.402-91.406 requires proceeds "
        "be paid within 120 days of first sale (for new wells) or 60 days (for existing wells), but does not mandate specific "
        "reporting format. Division orders typically specify statement format and frequency. Deduction disclosure: if lease "
        "allows post-production cost deductions (gathering, compression, treating, transportation), operator must provide "
        "reasonable detail on statements. Royalty owner audit rights: most division orders and leases grant royalty owners "
        "right to audit operator's books once per year with reasonable notice. Electronic statements increasingly common, "
        "but operator must accommodate owners without internet access. Best practice: detailed monthly statements showing "
        "all calculations, retained for 7 years for audit purposes."
    ),
    key_factors=[
        "No statutory format requirement, but division order terms control",
        "Industry practice: monthly statements with volumes, prices, deductions, net payment",
        "Payment timing: 120 days (new wells) or 60 days (existing wells)",
        "Deduction disclosure required if lease permits post-production costs",
        "Royalty owners typically have annual audit rights",
        "Retain statements for 7 years"
    ],
    primary_authority=[
        "Texas Natural Resources Code §91.402-91.406 (Payment Timing)",
        "Division Order Contract Terms",
        "Common Law Accounting Duties"
    ],
    burden_holder="Operator / Payor",
    adversary_position="Royalty owners",
    counter_arguments=[
        "Inadequate disclosure may trigger audit or litigation",
        "Late payment triggers statutory interest (10% annual)"
    ],
    resolution_strategy="Provide detailed monthly statements, comply with division order terms, maintain records for audits, pay timely",
    entity_scope=["operator", "producer", "working_interest"],
    confidence=0.88,
    confidence_stratification=ConfidenceStratification.CLEARLY_REQUIRED,
    controlling_precedent="Texas Natural Resources Code §91.402"
)

# ============================================================================
# FEDERAL REPORTING (ONRR, GLO)
# ============================================================================

FEDERAL_ONRR_REPORTING = DoctrineBlock(
    topic="Federal Reporting (ONRR)",
    keywords=["onrr", "federal lease", "federal royalty", "mms", "federal production"],
    conclusion_template=(
        "Operators of federal oil and gas leases must file monthly production and royalty reports with the Office of "
        "Natural Resources Revenue (ONRR). Reports due by end of month following production. Federal royalty rate "
        "typically 12.5%-18.75% depending on lease terms."
    ),
    reasoning_framework=(
        "Federal oil and gas leases require monthly reporting to ONRR (formerly Minerals Management Service). Reporting "
        "obligation: operator must file Production Accounting and Auditing System (PAAS) reports electronically through "
        "ONRR eCommerce portal. Reports due: last day of month following production (same deadline as RRC P-4 for Texas "
        "state production). Report must include: lease number, production volumes (oil, gas, NGLs), sales volumes, sales "
        "prices, transportation and processing allowances, royalty calculations. Federal royalty rates: 12.5% (older leases), "
        "16.67% (common for newer onshore), 18.75% (many offshore leases). Royalty payment due with report - ONRR assesses "
        "interest and penalties for late payment. ONRR audits: federal auditors review operator reports and may assess "
        "additional royalties, interest, and penalties years later. Major audit issues: proper valuation methods (comparing "
        "to index prices vs actual sales), allowable deductions (transportation must be actual costs, not estimates), volume "
        "measurement and allocation. Civil penalties up to $25,000/day for willful reporting violations. Criminal prosecution "
        "possible for fraudulent reporting (False Claims Act)."
    ),
    key_factors=[
        "Required for all federal oil & gas leases",
        "Electronic filing through ONRR eCommerce portal",
        "Due date: Last day of month following production",
        "Royalty rates: typically 12.5% to 18.75%",
        "Payment due with report - late payment triggers interest",
        "ONRR audits can go back 7 years",
        "Civil penalties up to $25,000/day for willful violations"
    ],
    primary_authority=[
        "30 CFR Part 1210 (ONRR Reporting)",
        "30 CFR Part 1241 (ONRR Audits)",
        "Federal Oil and Gas Royalty Management Act"
    ],
    burden_holder="Operator of federal lease",
    adversary_position="ONRR auditors",
    counter_arguments=[
        "Federal audits are rigorous and retroactive",
        "Valuation disputes can result in large assessments"
    ],
    resolution_strategy="File timely through eCommerce, use compliant valuation methods, document transportation allowances, retain records 7+ years",
    entity_scope=["operator"],
    confidence=0.92,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="30 CFR Part 1210"
)

STATE_LAND_GLO_REPORTING = DoctrineBlock(
    topic="Texas State Land Reporting (GLO)",
    keywords=["glo", "state land", "general land office", "state lease", "state royalty"],
    conclusion_template=(
        "Operators of Texas state land oil and gas leases must file monthly production and royalty reports with the "
        "General Land Office (GLO). GLO royalty rate typically 20%-25%. Reports due by last day of month following production."
    ),
    reasoning_framework=(
        "Texas state-owned lands (including Permanent School Fund and Permanent University Fund lands) require separate "
        "reporting to GLO beyond RRC reporting. Reporting system: GLO Oil and Gas Information System (OGIS), accessible "
        "online. Monthly reports due last day of month following production. Report includes: lease number, well information, "
        "production volumes, sales information, royalty calculations, payment. Royalty rates on GLO leases: historically 20%, "
        "but recent leases often 23-25% (higher than federal 12.5-18.75%). Royalty payment due with report. GLO audits: "
        "GLO Energy Resources division conducts audits similar to ONRR, examining volumes, prices, and deductions. Valuation: "
        "GLO uses market value at lease (wellhead value), similar to ONRR. Transportation deductions allowed only if actual "
        "documented costs. GLO lease terms often stricter than federal: higher royalties, stricter shut-in requirements, "
        "more aggressive enforcement. Permanent School Fund (PSF) and Permanent University Fund (PUF) lands generate revenue "
        "for Texas education - political sensitivity makes GLO enforcement vigorous. Late payment triggers statutory interest "
        "at rate specified in lease (typically 10-12% annual). GLO may terminate lease for chronic non-payment or under-reporting."
    ),
    key_factors=[
        "Required for Texas state land leases (GLO, PSF, PUF lands)",
        "File through GLO Oil and Gas Information System (OGIS)",
        "Due date: Last day of month following production",
        "Royalty rates: typically 20-25% (higher than federal)",
        "Payment due with report",
        "GLO audits examine volumes, prices, deductions",
        "Late payment triggers 10-12% annual interest",
        "Lease termination possible for chronic violations"
    ],
    primary_authority=[
        "Texas Natural Resources Code Chapter 52 (State Lands)",
        "GLO Lease Terms",
        "31 TAC Part 1 (GLO Rules)"
    ],
    burden_holder="Operator of state land lease",
    adversary_position="General Land Office Energy Resources",
    counter_arguments=[
        "GLO royalty rates higher than federal",
        "GLO enforcement aggressive due to education funding mandate"
    ],
    resolution_strategy="File timely through OGIS, pay full royalty, document deductions carefully, retain records for audits",
    entity_scope=["operator"],
    confidence=0.91,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="Texas Natural Resources Code Chapter 52"
)

# ============================================================================
# ENVIRONMENTAL REPORTING (TCEQ)
# ============================================================================

TCEQ_TIER_II_REPORT = DoctrineBlock(
    topic="TCEQ Tier II Chemical Inventory Reporting",
    keywords=["tier ii", "tier 2", "chemical inventory", "tceq", "hazardous materials", "epcra"],
    conclusion_template=(
        "Texas oil and gas facilities storing hazardous chemicals above threshold quantities must file annual Tier II "
        "chemical inventory reports with TCEQ. Reports due March 1 each year covering prior calendar year. Thresholds: "
        "10,000 lbs for most chemicals, 500 lbs for extremely hazardous substances."
    ),
    reasoning_framework=(
        "Federal Emergency Planning and Community Right-to-Know Act (EPCRA Section 312) and Texas Health & Safety Code "
        "Chapter 506 require Tier II reporting for facilities storing hazardous chemicals. Applicability: any facility "
        "with hazardous chemicals (as defined by OSHA Hazard Communication Standard) at or above threshold quantities. "
        "Common O&G chemicals triggering reporting: diesel fuel (10,000+ gallons), crude oil (10,000+ gallons), hydrogen "
        "sulfide (H2S) if >500 lbs, various treating chemicals, hydraulic fracturing additives. Threshold quantities: "
        "10,000 lbs for most hazardous chemicals, 500 lbs or threshold planning quantity (whichever is lower) for extremely "
        "hazardous substances. Filing: annual report filed online through TCEQ Tier II portal by March 1 covering prior "
        "calendar year. Report must include: chemical identity, maximum daily amount on-site, average daily amount, storage "
        "location (with site map), storage method (tank, vessel, pipeline, etc.). Local distribution: copies filed with "
        "local fire department, local emergency planning committee, TCEQ. Penalties: TCEQ may assess up to $25,000/day per "
        "violation for failure to file or late filing. Criminal penalties possible under EPCRA for knowing violations. "
        "Aggregation: multi-well facilities must aggregate all chemicals across entire site, not per-well."
    ),
    key_factors=[
        "Required if storing hazardous chemicals ≥10,000 lbs (or ≥500 lbs for EHS)",
        "Annual report due March 1 each year",
        "File electronically through TCEQ Tier II portal",
        "Common O&G triggers: diesel, crude oil, H2S, frac chemicals",
        "Report includes: chemical ID, quantities, storage locations, site map",
        "File with TCEQ, local fire dept, local emergency planning committee",
        "Penalties: up to $25,000/day for violations",
        "Aggregate all chemicals across entire facility"
    ],
    primary_authority=[
        "42 USC §11022 (EPCRA Section 312)",
        "Texas Health & Safety Code Chapter 506",
        "30 TAC §327 (TCEQ Tier II Rules)"
    ],
    burden_holder="Facility operator/owner",
    adversary_position="TCEQ, local fire departments",
    counter_arguments=[
        "Underreporting quantities risks penalties and emergency response gaps",
        "TCEQ cross-checks against other databases (air permits, waste reports)"
    ],
    resolution_strategy="Inventory all chemicals annually, file by March 1, coordinate with local first responders, update as operations change",
    entity_scope=["operator", "facility_owner"],
    confidence=0.90,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="42 USC §11022"
)

ANNUAL_WELL_INVENTORY = DoctrineBlock(
    topic="Annual Well Inventory (Form P-4S)",
    keywords=["p-4s", "annual inventory", "well inventory", "inactive wells", "shut-in wells"],
    conclusion_template=(
        "Texas operators must file annual well inventory (Form P-4S) by February 15 each year, listing all wells "
        "(active, inactive, shut-in, plugged) operated during the prior calendar year."
    ),
    reasoning_framework=(
        "16 TAC §3.75 requires annual well inventory (Form P-4S Supplement) filed by February 15 covering prior calendar "
        "year. Purpose: comprehensive accounting of all wells under operator's control, including active producers, temporarily "
        "shut-in wells, inactive wells, and wells plugged during the year. Form P-4S includes: well identification (API number, "
        "lease name, well number), current status (active, inactive, shut-in, plugged), last production date if inactive, "
        "reason for inactivity. This is distinct from monthly P-4 production reports - P-4S is annual snapshot of entire well "
        "portfolio. Importance: RRC uses P-4S to track orphan well risk, assess financial assurance requirements, and identify "
        "operators with large inactive well inventories. Wells inactive >12 months without production trigger heightened scrutiny - "
        "RRC may require additional bonding or plugging. Penalty for failure to file P-4S: $200/day, same as P-4 production reports. "
        "Form P-4S also used by RRC to verify operator compliance with Rule 3.78 financial assurance requirements - bond amounts "
        "calculated based on well count and status. Electronic filing available but not mandatory. Cross-reference: P-4S inventory "
        "should match wells listed on operator's Organization Report (P-5) and monthly P-4 filings."
    ),
    key_factors=[
        "Annual filing due February 15 each year",
        "Must list ALL wells: active, inactive, shut-in, plugged",
        "Includes well ID, status, last production date, reason for inactivity",
        "Separate from monthly P-4 production reports",
        "Used by RRC to assess financial assurance requirements",
        "Wells inactive >12 months trigger heightened scrutiny",
        "Penalty: $200/day for late filing"
    ],
    primary_authority=[
        "16 TAC §3.75 (Annual Inventory)",
        "16 TAC §3.78 (Financial Assurance)"
    ],
    burden_holder="Operator",
    adversary_position="Railroad Commission",
    counter_arguments=[
        "Large inactive well inventory increases bonding requirements",
        "Chronic inactivity may trigger plugging orders"
    ],
    resolution_strategy="File P-4S by February 15, maintain accurate well status records, address inactive wells proactively",
    entity_scope=["operator"],
    confidence=0.93,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="16 TAC §3.75"
)

MECHANICAL_INTEGRITY_TEST = DoctrineBlock(
    topic="Mechanical Integrity Test Reports (Injection/Disposal Wells)",
    keywords=["mechanical integrity", "mit", "injection well", "disposal well", "integrity test"],
    conclusion_template=(
        "Texas injection and disposal wells must undergo mechanical integrity tests (MIT) every 5 years. Test results "
        "must be filed with RRC within 30 days. Wells that fail MIT must be repaired or plugged."
    ),
    reasoning_framework=(
        "16 TAC §3.9 and §3.46 require periodic mechanical integrity testing for injection wells (enhanced recovery, gas storage) "
        "and disposal wells (produced water, other E&P waste). MIT frequency: every 5 years minimum, or more frequently if required "
        "by district office or permit conditions. MIT methods: pressure test (common), tracer survey, temperature log, noise log, "
        "or other RRC-approved method. Purpose: verify well casing and cement are intact, preventing fluid migration into "
        "non-target zones (especially fresh water aquifers). MIT results must be filed with RRC within 30 days of test completion. "
        "Failure consequences: wells that fail MIT must be repaired to achieve integrity or plugged if repair is not feasible. "
        "Continued operation of well with failed MIT is prohibited - RRC will issue shut-in order. Liability: failed MIT can indicate "
        "potential groundwater contamination - operator may face TCEQ enforcement and third-party claims. Best practice: test more "
        "frequently than 5-year minimum, especially for high-rate disposal wells or wells near drinking water sources. Federal overlap: "
        "EPA Underground Injection Control (UIC) program also regulates Class II injection wells - MIT requirements parallel but EPA "
        "may impose additional conditions for federally-delegated programs."
    ),
    key_factors=[
        "Required every 5 years for injection and disposal wells",
        "Test results due within 30 days of test completion",
        "Methods: pressure test, tracer survey, temperature/noise logs",
        "Failed MIT requires repair or plugging - continued operation prohibited",
        "RRC will issue shut-in order for wells with failed MIT",
        "Potential groundwater contamination liability if integrity compromised",
        "Federal EPA UIC program may impose additional requirements"
    ],
    primary_authority=[
        "16 TAC §3.9 (Injection Wells)",
        "16 TAC §3.46 (Disposal Wells)",
        "40 CFR Part 146 (EPA UIC Class II)"
    ],
    burden_holder="Operator of injection/disposal well",
    adversary_position="Railroad Commission, EPA, TCEQ",
    counter_arguments=[
        "Failed MIT triggers shut-in and expensive repair",
        "Groundwater contamination liability can be severe"
    ],
    resolution_strategy="Test every 5 years minimum, use qualified service company, file results within 30 days, repair failures immediately",
    entity_scope=["operator", "injection_operator", "disposal_operator"],
    confidence=0.94,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="16 TAC §3.9, §3.46"
)

# ============================================================================
# DOCTRINE CACHE (All Doctrine Blocks)
# ============================================================================

DOCTRINE_CACHE = [
    PRODUCTION_MONTHLY_P4,
    WELL_COMPLETION_W2,
    PLUGGING_REPORT_H10,
    ORGANIZATION_REPORT_P5,
    GAS_FLARING_REPORT,
    SEVERANCE_TAX_REPORT,
    ROYALTY_OWNER_STATEMENTS,
    FEDERAL_ONRR_REPORTING,
    STATE_LAND_GLO_REPORTING,
    TCEQ_TIER_II_REPORT,
    ANNUAL_WELL_INVENTORY,
    MECHANICAL_INTEGRITY_TEST,
]


# ============================================================================
# DOCTRINE MATCHING FUNCTION
# ============================================================================

def match_doctrines(query_text: str, keywords: List[str]) -> List[DoctrineBlock]:
    """
    Match query against doctrine cache using keyword overlap.
    Returns list of matching doctrines sorted by relevance (keyword match count).
    """
    query_lower = query_text.lower()
    keyword_set = set(k.lower() for k in keywords)

    matches = []
    for doctrine in DOCTRINE_CACHE:
        # Calculate keyword overlap
        doctrine_keywords = set(k.lower() for k in doctrine.keywords)
        overlap = len(keyword_set & doctrine_keywords)

        # Also check if query text contains doctrine keywords
        text_matches = sum(1 for dk in doctrine.keywords if dk.lower() in query_lower)

        total_score = overlap + text_matches

        if total_score > 0:
            matches.append((total_score, doctrine))

    # Sort by score descending
    matches.sort(key=lambda x: x[0], reverse=True)

    return [doctrine for score, doctrine in matches]
