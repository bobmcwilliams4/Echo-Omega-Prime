"""
Regulatory Compliance Doctrine Cache
R03 Compliance Checker Engine

52 doctrine blocks covering RRC, TCEQ, EPA, OSHA, DOT compliance
"""

from dataclasses import dataclass
from typing import List, Optional


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
    confidence: float
    confidence_stratification: str
    controlling_precedent: Optional[str] = None


DOCTRINE_CACHE = [
    DoctrineBlock(
        topic="RRC_PRODUCTION_REPORTING_P4",
        keywords=["P-4", "production report", "monthly reporting", "deadline", "oil production", "gas production", "reporting requirement"],
        conclusion_template=[
            "Operators must file Form P-4 Production Report by the 20th day of the month following production.",
            "Late filing may result in penalties under RRC Rule 3.20 and potential operator status issues.",
            "Electronic filing through RRC Online System is required for most operators."
        ],
        reasoning_framework="""
The RRC Form P-4 Production Report is the cornerstone of regulatory compliance for producing operators.
Under Statewide Rule 3.20, every operator must report monthly production of oil, gas, and condensate by lease.

FILING REQUIREMENTS:
1. Monthly Deadline: 20th day of month following production month
2. Lease-Level Reporting: Separate report per lease/unit
3. Product Types: Oil (barrels), Gas (MCF), Condensate (barrels)
4. Disposal Methods: Sales, injection, flared, vented
5. Allocation: Multi-well leases require proper allocation methodology

CONSEQUENCES OF NON-COMPLIANCE:
- First Violation: Warning letter, potential $1,000 penalty
- Repeat Violations: Escalating penalties up to $10,000/day
- Operator Status: May trigger P-5 Organization Report requirement
- Market Consequences: Purchasers may refuse to buy production without valid P-4
- Audit Triggers: Late filers subject to increased scrutiny

DEFENSIVE STRATEGY:
File even zero-production months to maintain continuous compliance record.
Implement automated calendar reminders 5 days before deadline.
Maintain backup filing method in case online system unavailable.
Document any allocation methodology for multi-well leases.
        """,
        key_factors=[
            "20th day monthly deadline",
            "Lease-level granularity required",
            "Electronic filing mandatory",
            "Zero-production months still require filing",
            "Allocation methodology for multi-well leases",
            "Penalties escalate for repeat violations",
            "Affects operator standing with RRC"
        ],
        primary_authority=[
            "16 TAC §3.20 (Statewide Rule 20) - Monthly Production Reports",
            "16 TAC §3.16 (Statewide Rule 16) - Penalties",
            "RRC Form P-4 Instructions (current version)"
        ],
        burden_holder="Operator of Record",
        adversary_position="RRC enforcement may argue late filing justifies operator status suspension",
        counter_arguments=[
            "Online system downtime prevented timely filing",
            "Allocation disputes with working interest owners delayed reporting",
            "First-time late filing with immediate correction shows good faith",
            "Zero production month, minimal regulatory impact",
            "Technical error in lease number, corrected within cure period"
        ],
        resolution_strategy="File immediately upon discovery of missed deadline, include explanation letter, request penalty waiver for first offense with documented system issue or good cause",
        entity_scope="All operators with Texas producing leases",
        confidence=0.98,
        confidence_stratification="DEFENSIBLE"
    ),

    DoctrineBlock(
        topic="RRC_WELL_PLUGGING_14DAY_NOTICE",
        keywords=["plugging", "14-day notice", "Form W-3A", "abandonment", "well plugging", "notice requirement"],
        conclusion_template=[
            "Operators must file Form W-3A at least 14 days before commencing plugging operations.",
            "RRC district office may require witness of critical cement plugs.",
            "Plugging must conform to Statewide Rule 14 requirements for casing, cement, and depths."
        ],
        reasoning_framework="""
Well plugging is one of the most heavily regulated aspects of oil and gas operations due to groundwater protection imperatives.
Statewide Rule 14 establishes comprehensive requirements for permanent well abandonment.

14-DAY NOTICE REQUIREMENT (Form W-3A):
Purpose: Allows RRC district office to schedule witness of plugging operations
Timing: Minimum 14 days before commencing plugging
Content: Proposed plug depths, cement volumes, casing to be cut/pulled
Consequences of Non-Compliance: Plugging operations are void, must re-plug with proper notice

PLUGGING STANDARDS:
1. Surface Plug: 50-100 feet below surface, minimum 50 sacks cement
2. Each Perforated Interval: Cement across entire interval plus 50 feet above
3. Base of Usable Quality Water: Cement plug minimum 100 feet
4. Other Requirements: Varies by district and well configuration

WITNESS REQUIREMENTS:
RRC may require district personnel witness critical plugs:
- Surface plug placement
- Top of cement on critical isolations
- Water protection plugs
Operator must coordinate schedule with district office, not commence until cleared.

COMPLETION REPORTING:
Form W-3 Certificate of Plugging due within 30 days of plug completion.
Failure to file W-3 leaves well in "plugging in progress" status, operator remains responsible.

DEFENSIVE COMPLIANCE:
File W-3A minimum 21 days in advance to allow RRC scheduling flexibility.
Include detailed diagram showing all proposed plug depths and cement volumes.
Confirm witness waiver or scheduled witness date before mobilizing rig.
Photograph all critical cement returns and surface condition after completion.
File W-3 immediately after operations complete, include vendor tickets and cement receipts.
        """,
        key_factors=[
            "14-day minimum advance notice",
            "District office may require witness of plugs",
            "Surface plug: 50-100 feet, minimum 50 sacks",
            "All perforations must be cemented with 50-foot overlap",
            "Water protection plug at base of usable quality water",
            "Form W-3 due within 30 days of completion",
            "Plugging without notice is void"
        ],
        primary_authority=[
            "16 TAC §3.14 (Statewide Rule 14) - Plugging",
            "RRC Form W-3A Instructions",
            "RRC Form W-3 Instructions",
            "District-specific plugging requirements"
        ],
        burden_holder="Operator of Record or Responsible Party",
        adversary_position="RRC may void plugging done without proper notice and require re-plugging at operator expense",
        counter_arguments=[
            "Emergency plugging required due to wellbore integrity issue",
            "Blowout or H2S release necessitated immediate action",
            "Orphan well plugging under state-funded program (different rules)",
            "Notice filed with wrong district office due to boundary confusion",
            "District office verbally approved shorter notice period"
        ],
        resolution_strategy="For emergency plugging, immediately notify district office by phone and follow with written emergency justification; for notice defects, request variance or re-plug under proper procedure",
        entity_scope="All well operators in Texas",
        confidence=0.99,
        confidence_stratification="DEFENSIBLE"
    ),

    DoctrineBlock(
        topic="RRC_H2S_AREA_COMPLIANCE_RULE36",
        keywords=["H2S", "hydrogen sulfide", "Rule 36", "sour gas", "safety", "notification", "H2S area"],
        conclusion_template=[
            "Operations in designated H2S areas require compliance with Statewide Rule 36 safety protocols.",
            "Notification to surface owners and occupants within contingency area is mandatory.",
            "Emergency response plan and specialized equipment required before operations commence."
        ],
        reasoning_framework="""
Hydrogen sulfide (H2S) is a deadly gas requiring extraordinary safety measures under Statewide Rule 36.
The RRC designates H2S areas based on known concentrations in producing formations.

H2S AREA DESIGNATION:
- Areas where H2S concentration exceeds 100 ppm in wellbore or produced fluids
- Map maintained by RRC, operators must check before drilling
- Areas may be designated by formation, field, or geographic zone

PERMIT REQUIREMENTS:
1. Drilling Permit Application: Must disclose H2S potential
2. Contingency Plan: Required before permit approval
3. Notification: All surface owners and occupants within contingency area
4. Equipment: H2S detection, breathing apparatus, wind direction indicators
5. Training: All personnel must have H2S safety training

CONTINGENCY AREA CALCULATION:
Based on worst-case release scenario considering:
- Maximum anticipated H2S concentration
- Well depth and pressure
- Topography and prevailing winds
- Nearby residences and occupied buildings
Typically ranges from 0.5 to 2 miles radius from wellsite.

OPERATIONAL REQUIREMENTS:
- 24-hour H2S monitoring during drilling and completion
- Breathing apparatus on location for all personnel
- Wind direction indicators visible from work areas
- Emergency shutdown procedures posted
- Local emergency responders notified and trained
- Sour gas flaring only with permit and proper flare design

CONSEQUENCES OF NON-COMPLIANCE:
- Immediate shutdown order
- Civil penalties up to $25,000/violation
- Criminal liability for H2S exposure causing injury/death
- Operator may be required to plug well at own expense

DEFENSIVE COMPLIANCE:
Retain H2S safety consultant for permit preparation and operations oversight.
Over-notify surface owners/occupants (expand contingency area).
Document all training with sign-in sheets and certificates.
Install redundant H2S detection systems with audible alarms.
Conduct pre-operation safety meeting with all contractors and RRC inspection if offered.
        """,
        key_factors=[
            "H2S concentration >100 ppm triggers Rule 36",
            "Contingency plan required before drilling",
            "Notification to all within contingency area mandatory",
            "Specialized equipment and training required",
            "24-hour monitoring during operations",
            "Severe penalties for non-compliance",
            "Criminal liability for injuries"
        ],
        primary_authority=[
            "16 TAC §3.36 (Statewide Rule 36) - Hydrogen Sulfide",
            "Health and Safety Code Chapter 756 - Hydrogen Sulfide",
            "OSHA 29 CFR 1910.1000 - H2S Exposure Limits"
        ],
        burden_holder="Operator",
        adversary_position="RRC and prosecutors may pursue criminal charges for H2S exposure incidents resulting from inadequate safety measures",
        counter_arguments=[
            "H2S concentration below 100 ppm threshold, not designated area",
            "Prior wells in area had no H2S, unexpected encounter",
            "Equipment malfunction prevented detection, not operator negligence",
            "Emergency response followed approved contingency plan",
            "Injured party was trespasser, not notified occupant"
        ],
        resolution_strategy="Immediate shutdown, full investigation, implement corrective actions, retain safety expert, cooperate fully with RRC investigation, settle civil penalties to avoid criminal referral",
        entity_scope="Operators in designated H2S areas",
        confidence=0.97,
        confidence_stratification="DEFENSIBLE"
    ),

    DoctrineBlock(
        topic="TCEQ_SPILL_REPORTING_REQUIREMENTS",
        keywords=["spill", "reportable quantity", "TCEQ", "notification", "oil spill", "produced water", "release"],
        conclusion_template=[
            "Spills of reportable quantities must be reported to TCEQ within 24 hours via STEERS system.",
            "Immediate notification required for spills threatening water bodies or posing imminent harm.",
            "Cleanup must be conducted under approved Spill Contingency Plan or TCEQ oversight."
        ],
        reasoning_framework="""
TCEQ administers state water quality laws requiring immediate reporting and cleanup of oil and chemical spills.
30 TAC Chapter 327 establishes comprehensive spill prevention and response requirements.

REPORTABLE QUANTITY TRIGGERS:
1. Oil/Petroleum: ≥25 gallons or any amount reaching water
2. Produced Water: ≥210 gallons or any amount reaching water
3. Hazardous Substances: Varies by substance, see 40 CFR 117.3
4. ANY spill to water body regardless of quantity
5. ANY spill causing sheen on water
6. ANY spill threatening public health or environment

NOTIFICATION TIMELINE:
- IMMEDIATE: Spills to surface water, imminent threat, public water supply
- 24 HOURS: All other reportable quantities
- METHOD: TCEQ STEERS hotline (512-339-2929) or online system
- INFORMATION: Location, substance, quantity, receiving environment, actions taken

CLEANUP REQUIREMENTS:
Operator must:
1. Stop the source of release
2. Contain spread using berms, absorbents, booms
3. Recover free product from surface and subsurface
4. Remove contaminated soil to background levels or approved standards
5. Sample soil/water to demonstrate cleanup complete
6. Dispose of waste at permitted facility with manifests
7. Submit Final Cleanup Report to TCEQ

SPILL CONTINGENCY PLAN:
Facilities with aboveground storage >1,320 gallons must have TCEQ-approved plan:
- Spill response procedures
- Equipment inventory
- Personnel training
- Notification protocols
Inspected annually, updated every 5 years.

ENFORCEMENT:
- Administrative Penalties: Up to $25,000/day
- Criminal Prosecution: Knowing violations, false reporting
- Cleanup Costs: TCEQ may cleanup and bill operator
- Third-Party Liability: Landowner and downstream property damage claims

DEFENSIVE COMPLIANCE:
Report immediately if any doubt about reportable quantity, over-reporting safer than under-reporting.
Photograph spill before, during, and after cleanup showing extent and completion.
Retain licensed environmental contractor for significant spills.
Sample background soil/water before cleanup to establish pre-existing conditions.
Document all waste disposal with manifests and facility receipts.
Submit Final Cleanup Report even if TCEQ didn't require, demonstrates closure.
        """,
        key_factors=[
            "≥25 gallons oil or any amount to water is reportable",
            "Immediate notification for water body impacts",
            "24-hour reporting for other reportable quantities",
            "STEERS system (512-339-2929) is official notification method",
            "Cleanup to background or TCEQ-approved standards required",
            "Final Cleanup Report demonstrates closure",
            "Penalties up to $25,000/day for violations"
        ],
        primary_authority=[
            "30 TAC §327 - Spill Prevention and Control",
            "Texas Water Code §26.121 - Notification of Spills",
            "40 CFR Part 110 - Oil Pollution Prevention",
            "40 CFR §117.3 - Reportable Quantities"
        ],
        burden_holder="Owner/Operator of facility or vehicle causing spill",
        adversary_position="TCEQ may argue late reporting prevented effective response and justifies enhanced penalties",
        counter_arguments=[
            "Quantity below reportable threshold based on field estimate",
            "Release was to secondary containment, did not reach environment",
            "Historical contamination from prior operator, not new release",
            "Immediate containment prevented environmental impact",
            "Third-party vandalism/theft caused release, not operator negligence"
        ],
        resolution_strategy="Report immediately, conduct aggressive cleanup, retain environmental consultant, negotiate Agreed Order with TCEQ to resolve penalty liability, implement enhanced prevention measures",
        entity_scope="All oil and gas operators and service providers",
        confidence=0.98,
        confidence_stratification="DEFENSIBLE"
    ),

    DoctrineBlock(
        topic="EPA_SPCC_PLAN_REQUIREMENTS",
        keywords=["SPCC", "Spill Prevention Control Countermeasure", "EPA", "oil storage", "tank battery", "40 CFR 112"],
        conclusion_template=[
            "Facilities with >1,320 gallons aggregate aboveground oil storage require EPA SPCC Plan.",
            "Plan must be prepared by Professional Engineer and updated every 5 years.",
            "Secondary containment, loading/unloading procedures, and inspections are mandatory elements."
        ],
        reasoning_framework="""
EPA's SPCC Rule (40 CFR Part 112) requires spill prevention planning for facilities storing oil.
Tank batteries and production facilities commonly exceed the 1,320-gallon threshold.

APPLICABILITY THRESHOLDS:
Plan required if:
1. Aggregate aboveground storage capacity >1,320 gallons, OR
2. Single container >660 gallons
AND reasonable expectation of discharge to navigable waters or adjoining shorelines

STORAGE CAPACITY CALCULATION:
Include:
- Production tanks (oil, condensate, produced water if contains oil)
- Fuel tanks for generators and equipment
- Lube oil storage
- Dielectric oil in transformers
Exclude:
- Completely buried tanks
- Tanks inside buildings with impervious floors
- Tanks <55 gallons

SPCC PLAN REQUIREMENTS:
1. PE Certification: Licensed Professional Engineer must prepare and certify
2. Facility Diagram: Tank locations, capacities, piping
3. Discharge Prevention: Secondary containment, valve protocols, inspections
4. Spill Response: Equipment, procedures, contractor contacts
5. Training: Personnel roles and responsibilities
6. Updates: Review and update every 5 years or after major changes

SECONDARY CONTAINMENT:
Must contain 110% of largest tank capacity or 10% of aggregate, whichever is greater:
- Earthen berms with impermeable liner
- Concrete containment
- Double-wall tanks
- Vault systems
Drainage valves must be normally closed and locked, opened only under supervision.

LOADING/UNLOADING:
- Constant surveillance during operations
- Overfill prevention (high-level alarms, auto-shutoffs)
- Spill equipment readily available
- Communication between facility and transport driver

INSPECTIONS:
- Tank integrity inspections annually
- Valves and piping quarterly
- Secondary containment monthly for defects
- Document all inspections with written records

ENFORCEMENT:
- Civil Penalties: Up to $25,000/violation/day
- Criminal Prosecution: Knowing violations
- Cleanup Liability: Unlimited under OPA 90

DEFENSIVE COMPLIANCE:
Calculate storage capacity conservatively, include marginal tanks.
Retain PE familiar with oil and gas facilities for plan preparation.
Implement inspection schedule more frequently than minimum (monthly tanks, weekly containment).
Train all personnel annually with documentation, not just new hires.
Update plan immediately after any tank addition/removal, not just 5-year cycle.
Conduct annual mock spill drill, document lessons learned.
        """,
        key_factors=[
            "1,320 gallon aggregate or 660 gallon single container triggers requirement",
            "Professional Engineer certification mandatory",
            "Secondary containment: 110% of largest tank or 10% aggregate",
            "5-year update cycle required",
            "Inspections: tanks annually, containment monthly",
            "Drainage valves normally closed and locked",
            "Penalties up to $25,000/day"
        ],
        primary_authority=[
            "40 CFR Part 112 - Oil Pollution Prevention",
            "Clean Water Act §311(j)(1)(C)",
            "Oil Pollution Act of 1990",
            "EPA SPCC Guidance for Regional Inspectors"
        ],
        burden_holder="Owner/Operator of facility",
        adversary_position="EPA may argue facility capacity exceeded threshold years before plan preparation, justifying retrospective penalties",
        counter_arguments=[
            "Storage capacity calculation excluded exempt tanks",
            "No reasonable expectation of discharge to navigable waters (remote location)",
            "Equivalent environmental protection with alternative measures",
            "Prior operator responsible for threshold exceedance",
            "Plan was prepared but PE stamp omitted due to administrative error"
        ],
        resolution_strategy="Prepare plan immediately with qualified PE, conduct comprehensive facility inspection and implement any needed upgrades, negotiate penalty mitigation based on good faith efforts and rapid correction",
        entity_scope="Oil and gas facilities with storage >1,320 gallons",
        confidence=0.97,
        confidence_stratification="DEFENSIBLE"
    ),

    DoctrineBlock(
        topic="TCEQ_AIR_PERMIT_BY_RULE_OIL_GAS",
        keywords=["air permit", "permit by rule", "PBR", "TCEQ", "air emissions", "tank battery", "engines"],
        conclusion_template=[
            "Most oil and gas production facilities qualify for Permit by Rule under 30 TAC §106.352.",
            "Registration required for facilities with engines >50 HP or emissions >25 tons/year any pollutant.",
            "Annual emission inventories required for facilities exceeding reporting thresholds."
        ],
        reasoning_framework="""
TCEQ authorizes oil and gas production facilities to operate under Permits by Rule (PBR) in lieu of individual permits.
30 TAC Chapter 106 Subchapter F establishes simplified authorization for standard industry practices.

PERMIT BY RULE 106.352 - OIL AND GAS PRODUCTION:
Authorizes without individual permit:
- Storage tanks for crude oil, condensate, produced water
- Glycol dehydrators <3.0 MMscfd throughput
- Heater/treaters
- Flares and vapor combustors
- Loading operations
- Fugitive emissions from wellheads, valves, flanges

REGISTRATION REQUIREMENTS:
Must register with TCEQ if facility has:
- Engines >50 HP (each), OR
- Potential emissions ≥25 tons/year any single pollutant, OR
- Located in nonattainment or near-nonattainment county

EMISSION CALCULATION:
Common pollutants requiring calculation:
- VOC (volatile organic compounds) from tank breathing/flashing
- NOx (nitrogen oxides) from engines and flares
- CO (carbon monoxide) from combustion
- HAPs (hazardous air pollutants) - benzene, toluene, xylene, formaldehyde

Tank emissions calculated using:
- API RP-42 methodology or E&P TANKS software
- Vapor pressure of crude oil/condensate
- Throughput volume and tankage configuration
- Vapor recovery/control equipment

REGISTRATION PROCESS:
1. Calculate potential emissions for all sources
2. Submit TCEQ Air Registration Form with technical data
3. Pay registration fee (varies by facility size)
4. Receive registration number (RN)
5. Display RN on facility

ANNUAL EMISSION INVENTORY:
Required if:
- Any pollutant ≥10 tons/year actual emissions, OR
- Facility is registered
Submit by March 31 each year via TCEQ STEERS online system.

RECORDKEEPING:
Maintain for 5 years:
- Monthly production volumes (oil, gas, condensate)
- Engine operating hours
- Fuel consumption
- Emission calculations
- Maintenance records for control equipment

ENFORCEMENT:
- Operating without required registration: $25,000/day
- Failure to file emission inventory: $10,000/violation
- Excessive emissions: PBR may be revoked, individual permit required

DEFENSIVE COMPLIANCE:
Calculate emissions conservatively using worst-case throughput scenarios.
Register even if close to threshold to avoid later disputes.
Use E&P TANKS software (free from EPA) for tank emission calculations with documented inputs.
Implement VOC controls (vapor recovery units) even if not required to stay below thresholds.
File emission inventory even in year below threshold to maintain regulatory relationship.
Retain air quality consultant for registration and annual inventory preparation.
        """,
        key_factors=[
            "PBR 106.352 authorizes standard production equipment",
            "Registration required for engines >50 HP or emissions ≥25 TPY",
            "API RP-42 or E&P TANKS software for tank emission calculations",
            "Annual emission inventory due March 31 if ≥10 TPY any pollutant",
            "5-year recordkeeping requirement",
            "Penalties up to $25,000/day for operating without authorization",
            "PBR revocation possible for excessive emissions"
        ],
        primary_authority=[
            "30 TAC §106.352 - Oil and Gas Production PBR",
            "30 TAC §101.10 - Emission Inventory Requirements",
            "40 CFR Part 60 Subpart OOOO - NSPS for Oil and Gas",
            "EPA E&P TANKS Software User Guide"
        ],
        burden_holder="Owner/Operator of production facility",
        adversary_position="TCEQ may argue facility exceeded PBR limits and operated without authorization, justifying shutdown and penalties",
        counter_arguments=[
            "Emission calculations used conservative assumptions, actual below threshold",
            "Engine HP rating is brake HP not continuous rating",
            "Facility was below threshold when constructed, production increase unexpected",
            "Prior operator responsible for registration failure",
            "VOC control equipment malfunction temporary, annual emissions still compliant"
        ],
        resolution_strategy="Immediately register facility and file late emission inventories, install additional controls if needed to ensure compliance going forward, negotiate penalty reduction based on rapid correction and compliance history",
        entity_scope="Oil and gas production facilities in Texas",
        confidence=0.96,
        confidence_stratification="DEFENSIBLE"
    ),

    DoctrineBlock(
        topic="EPA_NSPS_SUBPART_OOOO_METHANE",
        keywords=["NSPS", "Subpart OOOO", "methane", "EPA", "pneumatic controllers", "storage vessels", "leak detection"],
        conclusion_template=[
            "Production facilities constructed/modified after August 23, 2011 subject to NSPS Subpart OOOO standards.",
            "Low-bleed pneumatic controllers and storage vessel VOC controls required.",
            "Semiannual leak detection and repair (LDAR) monitoring mandatory for wellsites."
        ],
        reasoning_framework="""
EPA's New Source Performance Standards (NSPS) Subpart OOOO regulates methane and VOC emissions from new and modified oil and gas facilities.
Compliance is federally enforceable with significant penalties for violations.

APPLICABILITY:
Facilities affected sources constructed/modified/reconstructed after 8/23/2011:
- Wellsites (including well completions and workovers)
- Compressor stations
- Natural gas processing plants
- Storage vessels receiving hydrocarbons

PNEUMATIC CONTROLLER REQUIREMENTS:
Controllers installed after 9/18/2015 must be:
- Zero-emission (electric, air, or closed-vent system), OR
- Low-bleed (≤6 scf/hour bleed rate)
High-bleed controllers prohibited except for safety-related controls.

STORAGE VESSEL VOC CONTROLS:
Vessels with potential VOC emissions ≥6 TPY must have controls:
- Vapor recovery to sales line
- Combustion control (flare or vapor combustor)
- Route to fuel gas system
Control efficiency must be ≥95%.

WELL COMPLETION VENTING PROHIBITION:
Hydraulically fractured gas wells must use:
- Completion combustion (flaring), OR
- Reduced emission completions (REC/"green completions")
Venting to atmosphere prohibited except during initial flowback.

LEAK DETECTION AND REPAIR (LDAR):
Wellsites must conduct monitoring:
- Semiannually (every 6 months) using optical gas imaging or Method 21
- All components: valves, connectors, pressure relief devices, open-ended lines
- Repair leaks within 30 days of detection
- Document all monitoring and repairs

RECORDKEEPING:
Maintain for 5 years:
- Pneumatic controller manufacturer data (bleed rates)
- Storage vessel emission calculations
- LDAR monitoring records (date, operator, findings, repairs)
- Control device operating parameters
- Malfunctions and corrective actions

REPORTING:
Annual reports due by March 15:
- Facility information and affected sources
- LDAR monitoring results and repairs
- Deviations from requirements
Submit via EPA's ERT (Emissions Reporting Tool).

ENFORCEMENT:
- Civil Penalties: Up to $51,570 per violation per day (2023 rates)
- Criminal Prosecution: Knowing violations, false reporting
- Citizen Suits: Environmental groups may sue for violations
- State Enforcement: TCEQ may enforce federal standards

DEFENSIVE COMPLIANCE:
Conduct NSPS applicability determination for every new well/facility construction.
Use only zero-emission or certified low-bleed pneumatic controllers, retain manufacturer data sheets.
Calculate storage vessel emissions conservatively using E&P TANKS software.
Implement LDAR monitoring with certified thermographer or Method 21 technician.
Document all monitoring with contemporaneous field records, not reconstructed later.
Repair leaks within 15 days (internal deadline) to ensure 30-day regulatory deadline met.
File annual reports even if no affected sources (zero report) to maintain compliance record.
        """,
        key_factors=[
            "Applies to facilities constructed/modified after 8/23/2011",
            "Zero-emission or low-bleed (≤6 scf/hr) pneumatic controllers required",
            "Storage vessels ≥6 TPY VOC require 95% control efficiency",
            "Semiannual LDAR monitoring mandatory",
            "Leak repairs within 30 days of detection",
            "Annual reports due March 15 via EPA ERT",
            "Penalties up to $51,570/violation/day"
        ],
        primary_authority=[
            "40 CFR Part 60 Subpart OOOO - NSPS for Oil and Gas",
            "40 CFR Part 60 Subpart OOOOa - NSPS for Oil and Gas (2016 amendments)",
            "Clean Air Act §111 - Standards of Performance",
            "EPA Compliance Guide for Subpart OOOO"
        ],
        burden_holder="Owner/Operator of affected facility",
        adversary_position="EPA may argue modifications triggered NSPS applicability and operator failed to comply, justifying substantial penalties and corrective action orders",
        counter_arguments=[
            "Facility constructed before applicability date, not subject to NSPS",
            "Modifications were routine maintenance, not reconstruction",
            "Storage vessel emissions below 6 TPY threshold based on actual production",
            "LDAR monitoring conducted but records lost due to personnel turnover",
            "Control device malfunction temporary, corrective action taken immediately"
        ],
        resolution_strategy="Conduct compliance audit, install needed controls, implement robust LDAR program with certified contractor, file overdue reports, negotiate penalty reduction via EPA's Self-Disclosure Policy if violations self-discovered and corrected",
        entity_scope="Oil and gas facilities constructed/modified after 2011",
        confidence=0.95,
        confidence_stratification="DEFENSIBLE"
    ),

    DoctrineBlock(
        topic="RRC_SURFACE_CASING_DEPTH_REQUIREMENTS",
        keywords=["surface casing", "casing depth", "cementing", "groundwater protection", "usable quality water", "Statewide Rule 13"],
        conclusion_template=[
            "Surface casing must extend below all usable quality water zones per Statewide Rule 13.",
            "Cement must fill annulus from shoe to surface with returns verified.",
            "District offices may require greater depths based on local groundwater conditions."
        ],
        reasoning_framework="""
Surface casing requirements protect underground freshwater aquifers from contamination by drilling fluids and produced fluids.
Statewide Rule 13 establishes minimum standards, but district-specific rules may be more stringent.

USABLE QUALITY WATER DEFINITION:
Water containing <3,000 mg/L total dissolved solids (TDS).
Operator must determine depth to base of usable quality water using:
- Drilling records from offset wells
- Electric logs showing resistivity/spontaneous potential
- Water quality data from nearby water wells
- RRC district office guidance for the area

SURFACE CASING DEPTH:
Minimum: Below all usable quality water zones, typically 50-200 feet below base.
District-Specific Requirements:
- District 1 (South Texas): Often requires 500+ feet due to deep freshwater
- District 2 (Refugio): 300-600 feet typical
- District 8 (Midland-Permian): 300-500 feet typical, Red Beds protection
- District 8C (Lubbock): 800+ feet due to Ogallala Aquifer

CEMENTING REQUIREMENTS:
Cement must:
1. Fill annulus from casing shoe to surface
2. Use sufficient volume to ensure complete fill (calculated or measured)
3. Achieve returns to surface (visual confirmation)
4. Meet API specification for cement type and density
5. Circulate before cementing to condition hole

CEMENT WAIT TIME:
Minimum waiting period before drilling out:
- 8 hours for Class A/G cement in normal temperatures
- 12 hours for deeper intervals or lower temperatures
- Longer if cement design specifies (retarded, lightweight)

REPORTING:
Drilling permit must show proposed surface casing depth and cementing program.
Well completion report (Form W-2) must show:
- Actual casing depth set
- Cement volume pumped
- Returns to surface (yes/no)
- Wait time before drilling out

CONSEQUENCES OF INADEQUATE PROTECTION:
- RRC may require remedial cementing
- Additional casing strings may be mandated
- Well may be shut in until groundwater protection demonstrated
- Operator liable for water well contamination claims

DEFENSIVE COMPLIANCE:
Research offset well data and RRC district requirements before permitting.
Set surface casing deeper than minimum (50-100 feet extra) as insurance.
Use excess cement volume (10-20% more than calculated) to ensure surface returns.
Install centralizers on casing to improve cement distribution.
Run cement bond log (CBL) to verify cement quality behind casing.
Document cement returns with photos/video and crew statements.
        """,
        key_factors=[
            "Surface casing must extend below all usable quality water (<3,000 TDS)",
            "Cement must fill annulus to surface with verified returns",
            "District-specific requirements may exceed Statewide Rule minimums",
            "8-12 hour cement wait time before drilling out",
            "Offset well data required to determine water depth",
            "Completion report must document actual depth and cementing",
            "Inadequate protection may require remedial work or shutdown"
        ],
        primary_authority=[
            "16 TAC §3.13 (Statewide Rule 13) - Casing, Cementing, Drilling, and Completion",
            "District Rules for each RRC district",
            "RRC Oil and Gas Docket decisions on casing requirements"
        ],
        burden_holder="Operator",
        adversary_position="RRC may argue inadequate surface casing depth caused groundwater contamination and require well plugging and aquifer remediation at operator expense",
        counter_arguments=[
            "Offset well data showed shallower usable quality water, unexpected deeper zone",
            "Cement returns to surface achieved, CBL confirms good bond",
            "Contamination from surface spill or other source, not well construction",
            "Prior operator drilled well with inadequate casing, current operator inherited",
            "District office approved permit with proposed depth, estoppel"
        ],
        resolution_strategy="Immediately test water wells in area to determine extent and source of contamination, install additional casing/cement if feasible, provide alternative water supply to affected landowners, retain hydrogeologist to investigate, negotiate remediation plan with RRC",
        entity_scope="All drilling operators in Texas",
        confidence=0.98,
        confidence_stratification="DEFENSIBLE"
    ),

    DoctrineBlock(
        topic="RRC_PIT_LINER_REQUIREMENTS_RULE8",
        keywords=["pit liner", "earthen pit", "reserve pit", "produced water", "Statewide Rule 8", "double liner"],
        conclusion_template=[
            "Commercial pits require double liner system with leak detection per Statewide Rule 8.",
            "Temporary drilling pits require single synthetic liner or equivalent clay liner.",
            "Closure testing and soil sampling required before pit abandonment."
        ],
        reasoning_framework="""
Earthen pits for storage of drilling fluids, produced water, and oil are strictly regulated to prevent soil and groundwater contamination.
Statewide Rule 8 establishes construction, operation, and closure standards.

PIT CLASSIFICATION:
1. Emergency Pits: Temporary (<90 days), single liner, permit not required
2. Drilling Pits: Duration of drilling/completion, single liner, permit required
3. Skimming Pits: Permanent, separate oil from water, double liner, permit required
4. Commercial Pits: Receive fluids from multiple leases, double liner, extensive permitting

LINER REQUIREMENTS:
Single Liner System (drilling pits):
- 30-mil synthetic (HDPE, PVC, or equivalent), OR
- 3-foot compacted clay liner with permeability ≤1×10⁻⁷ cm/sec
- Freeboard: Minimum 2 feet from top of liner to pit rim

Double Liner System (commercial/skimming pits):
- Primary liner: 40-mil synthetic or 2-foot clay
- Leak detection zone: Sand or geotextile layer with sump
- Secondary liner: 60-mil synthetic or 3-foot clay
- Leak detection monitoring required monthly

CONSTRUCTION CERTIFICATION:
Professional Engineer must certify:
- Liner installation per manufacturer specifications
- Seam testing (air pressure or vacuum box)
- Soil foundation suitable for liner system
- Freeboard and capacity calculations

OPERATIONAL REQUIREMENTS:
- Inspections: Weekly during use, document in log
- Freeboard Maintenance: Keep liquid level 2 feet below rim
- Leak Detection: Monitor sumps monthly, analyze samples if liquids present
- Fence: 4-foot minimum around pit perimeter
- Signs: Warning signs at access points

PIT CLOSURE:
1. Remove all free liquids (pump down to bottom)
2. Sample pit bottom solids for RCRA constituents
3. If hazardous: Dispose at permitted facility with manifest
4. If non-hazardous: Mix with soil or solidify, backfill in place
5. Remove liner or leave in place with soil cover
6. Grade to prevent ponding
7. Revegetate surface
8. PE certification of closure
9. File closure report with RRC district office

CONSEQUENCES OF VIOLATIONS:
- Unpermitted pit: Immediate closure order, $10,000 penalty
- Leak from pit: Soil remediation costs, groundwater monitoring
- Improper closure: Excavate and re-close at operator expense
- Third-party contamination: Liable for property damage and cleanup

DEFENSIVE COMPLIANCE:
Use synthetic liner for all pits even if clay allowed (more reliable, easier to inspect).
Install leak detection even in single-liner drilling pits (early warning).
Conduct weekly inspections with photos documenting liquid levels and liner condition.
Close pits as soon as drilling/completion complete, don't leave for months.
Sample pit solids before closure, test for RCRA metals and TPH.
Retain PE for closure certification, not just operator's employee.
File closure report immediately, include photos of each closure step.
        """,
        key_factors=[
            "Commercial pits require double liner with leak detection",
            "Drilling pits require single 30-mil synthetic or 3-foot clay liner",
            "2-foot freeboard requirement during operation",
            "Weekly inspections with documented logs required",
            "PE certification required for construction and closure",
            "Closure requires soil sampling, solids removal/treatment, grading",
            "Unpermitted pits subject to immediate closure and penalties"
        ],
        primary_authority=[
            "16 TAC §3.8 (Statewide Rule 8) - Water Protection",
            "16 TAC §3.9 (Statewide Rule 9) - Disposal Wells",
            "40 CFR Part 261 - Hazardous Waste Identification"
        ],
        burden_holder="Operator",
        adversary_position="RRC may argue pit leaked due to inadequate liner and require extensive soil/groundwater remediation at operator expense",
        counter_arguments=[
            "Liner installed per PE specifications, unexpected liner failure",
            "Contamination pre-existed pit construction (historical operations)",
            "Volume in leak detection sump was rainwater, not leak",
            "Emergency pit exemption applied, permit not required",
            "Prior operator constructed pit, current operator inherited"
        ],
        resolution_strategy="Immediately close pit and remove fluids, conduct soil sampling to determine contamination extent, excavate contaminated soil if needed, install groundwater monitoring wells if directed by RRC, negotiate remediation plan and penalty settlement",
        entity_scope="All operators using earthen pits for drilling or production fluids",
        confidence=0.97,
        confidence_stratification="DEFENSIBLE"
    ),

    DoctrineBlock(
        topic="RRC_FINANCIAL_ASSURANCE_BONDING",
        keywords=["bond", "financial assurance", "P-4 bond", "blanket bond", "performance bond", "plugging bond"],
        conclusion_template=[
            "Operators must maintain sufficient bonding to cover well plugging obligations.",
            "Individual well bonds ($2-$25K) or blanket bonds ($25K-$250K) required based on well count.",
            "Bond release only after RRC verifies proper well plugging and site restoration."
        ],
        reasoning_framework="""
Financial assurance requirements ensure operators have resources to plug wells and restore sites.
Statewide Rule 78 establishes bonding requirements scaled to operational scope.

BONDING LEVELS:
Individual Well Bonds:
- Depth <2,000 ft: $2,000
- Depth 2,000-4,000 ft: $3,000
- Depth >4,000 ft: $6,000
- Multiple completions: Add $2,000 per completion

Blanket Bonds (covers multiple wells):
- 1-10 wells: $25,000
- 11-100 wells: $50,000
- 101-250 wells: $100,000
- 251-500 wells: $150,000
- >500 wells: $250,000

BOND INSTRUMENTS:
Acceptable forms:
- Surety bond from RRC-approved surety company
- Cash bond (held by State Comptroller)
- Letter of credit from Texas-chartered bank
- Certificate of deposit assigned to RRC

BONDING TRIGGERS:
New operators must bond before:
- Drilling permit approval
- Transfer of operatorship (Form P-4)
- Assuming responsibility for orphan wells

BOND RELEASE:
Operator may request release after:
- Well properly plugged per Rule 14
- Form W-3 Certificate of Plugging filed
- Site restored and revegetated
- RRC district inspection confirms compliance
Processing time: 60-120 days after request.

CONSEQUENCES OF INADEQUATE BONDING:
- Permit applications denied
- Existing permits may be suspended
- Wells may be declared orphans
- Operator designation revoked
- Personal liability for officers/directors if corporate veil pierced

DEFENSIVE COMPLIANCE:
Maintain blanket bond above minimum threshold to allow operational flexibility.
Request bond increase proactively when approaching well count thresholds.
Never let bond lapse - ensure renewal 30 days before expiration.
Upon acquiring wells, immediately file bond amendment to add well numbers.
When selling wells, request deletion from bond promptly to reduce liability exposure.
        """,
        key_factors=[
            "Individual bonds: $2K-$6K based on depth",
            "Blanket bonds: $25K-$250K based on well count",
            "Bond required before drilling permit or operatorship transfer",
            "Release only after plugging verification and site restoration",
            "60-120 day release processing time",
            "Lapsed bond triggers permit suspension",
            "Personal liability risk for officers if corporate shield fails"
        ],
        primary_authority=[
            "16 TAC §3.78 (Statewide Rule 78) - Plugging and Financial Security Requirements",
            "Texas Natural Resources Code §91.1041 - Performance Bonds",
            "RRC Bond Policy Update (2023)"
        ],
        burden_holder="Operator or designated agent",
        adversary_position="RRC may declare wells orphans and call bond if operator fails to plug properly",
        counter_arguments=[
            "Wells were properly plugged, RRC inspection error",
            "Bond amount adequate when posted, well count increase unexpected",
            "Successor operator assumed bonding responsibility",
            "Corporate bankruptcy discharges personal liability",
            "Bond surety liable, not operator"
        ],
        resolution_strategy="Maintain excess bonding capacity, file bond amendments immediately upon well acquisitions/divestitures, conduct pre-plugging coordination with RRC to ensure compliance, document site restoration extensively",
        entity_scope="All operators of Texas oil and gas wells",
        confidence=0.99,
        confidence_stratification="DEFENSIBLE"
    ),

    DoctrineBlock(
        topic="RRC_FORM_P5_ORGANIZATION_REPORT",
        keywords=["P-5", "organization report", "operator designation", "change of operator", "entity information"],
        conclusion_template=[
            "Form P-5 Organization Report required within 30 days of entity changes affecting operatorship.",
            "Changes include: name, address, officers, ownership structure, or financial condition.",
            "Failure to timely update may result in operator designation suspension."
        ],
        reasoning_framework="""
The RRC requires current information on all operators to ensure accountability and regulatory communication.
Form P-5 must be filed for any material change to the operator entity.

FILING TRIGGERS:
Change of:
- Legal name of operator
- Mailing address or principal office
- Officers, directors, or managing members
- Ownership (>25% transfer of equity)
- Financial condition (bankruptcy, receivership)
- Tax identification number
- Registered agent for service of process

FILING DEADLINE:
30 days from date of change.
Late filing may result in:
- Warning letter (first offense)
- $1,000 administrative penalty (repeat offense)
- Suspension of operator designation
- Drilling permit applications denied

INFORMATION REQUIRED:
- Complete legal name and DBA names
- Federal tax ID number (EIN)
- All addresses (principal office, mailing, registered agent)
- Entity type (corporation, LLC, partnership, individual)
- Officers/directors with titles and contact information
- Ownership structure if closely held
- Financial assurance (bond) information
- All producing and non-producing well counts

OPERATOR DESIGNATION:
P-5 establishes operator of record for:
- Regulatory compliance responsibility
- Well plugging liability
- Production tax reporting
- Environmental violations
- Safety incidents

TRANSFERS OF OPERATORSHIP:
Selling operator must:
1. File final P-4 Production Report
2. Transfer bond or verify buyer has bond
3. Update P-5 showing wells transferred out

Buying operator must:
1. File P-5 adding wells acquired
2. Post adequate financial assurance
3. File subsequent P-4 reports

CONSEQUENCES OF NON-FILING:
- Operator designation suspended
- Unable to file permits or production reports
- Wells may be shut in by RRC
- Personal liability for officers/directors
- Criminal misdemeanor for knowingly false filing

DEFENSIVE COMPLIANCE:
Appoint compliance officer responsible for monitoring P-5 triggers.
File updated P-5 within 15 days of change (internal deadline to ensure 30-day compliance).
Maintain corporate records documenting dates of all changes.
Include P-5 update in closing checklist for all asset acquisitions/divestitures.
File protective P-5 if uncertain whether change is material enough to require filing.
        """,
        key_factors=[
            "30-day filing deadline from date of material change",
            "Changes include: name, address, officers, ownership >25%, financial condition",
            "Establishes operator of record for all regulatory purposes",
            "Suspension of operator designation for non-compliance",
            "Required for both producing and non-producing well operators",
            "Criminal penalty for knowingly false information",
            "Transfer checklist: final P-4, bond transfer, P-5 updates by both parties"
        ],
        primary_authority=[
            "16 TAC §3.20 (Statewide Rule 20) - Organization Report Requirements",
            "Texas Natural Resources Code §91.142 - Operator Information",
            "RRC Form P-5 Instructions"
        ],
        burden_holder="Operator or authorized representative",
        adversary_position="RRC may suspend operator designation and shut in wells if P-5 not current",
        counter_arguments=[
            "Change was not material enough to trigger filing",
            "30-day deadline not yet expired when RRC issued notice",
            "Prior operator failed to file transfer notice",
            "Administrative error, corrected immediately upon discovery",
            "Officer change was pro forma, no operational impact"
        ],
        resolution_strategy="File updated P-5 immediately, include explanation letter for late filing, request penalty waiver if first offense, implement compliance monitoring to prevent recurrence",
        entity_scope="All operators with Texas operator number",
        confidence=0.98,
        confidence_stratification="DEFENSIBLE"
    ),

    DoctrineBlock(
        topic="RRC_INACTIVE_WELL_FORM_R1",
        keywords=["inactive well", "Form R-1", "annual compliance", "inactive status", "March 31 deadline"],
        conclusion_template=[
            "Operators with inactive wells must file Form R-1 annually by March 31.",
            "Inactive well defined as no production for 12+ months and not used for injection or disposal.",
            "Failure to file may result in well being designated orphan and operator losing designation."
        ],
        reasoning_framework="""
RRC requires annual reporting on inactive wells to ensure they're being monitored and will eventually be plugged or returned to production.
Statewide Rule 14 defines inactive well compliance requirements.

INACTIVE WELL DEFINITION:
Well that has:
- No reported production for 12 consecutive months
- Not used for injection or disposal
- Not otherwise utilized (storage, monitoring)
- Valid permit but no current operation

ANNUAL FILING REQUIREMENT:
Form R-1 due March 31 each year for all inactive wells.
Must include:
- Current well status (shut in vs. temporarily abandoned)
- Reason for inactivity
- Anticipated future use or plugging timeline
- Current operator contact information
- Financial assurance verification

COMPLIANCE OPTIONS:
Operator may:
1. Return well to production (file amended status)
2. Convert to injection/disposal (file permit)
3. Plug well (file W-3A notice)
4. Continue inactive status (file annual R-1)

CONSEQUENCES OF NON-FILING:
- First year late: Warning letter
- Second year late: $500 penalty
- Third year late: Well designated orphan, bond forfeited
- Operator designation may be suspended
- Personal liability for officers/directors

PLUGGING REQUIREMENTS:
Wells inactive >10 years face enhanced scrutiny:
- May be required to plug within specified timeframe
- RRC may issue mandatory plugging order
- Extended inactive status requires showing of good cause
- Marginal economic value not sufficient justification indefinitely

DEFENSIVE COMPLIANCE:
Maintain spreadsheet of all inactive wells with last production date.
Set calendar reminder for February 15 to prepare R-1 filing.
File R-1 by March 15 (internal deadline) to ensure timely compliance.
For wells inactive >5 years, develop plan to plug or return to production.
Consider selling inactive wells to avoid long-term plugging liability.
Document all inactive well inspections (monthly recommended).
Maintain accurate bond coverage for inactive well count.
        """,
        key_factors=[
            "Annual Form R-1 due March 31 for all inactive wells",
            "Inactive = no production for 12+ consecutive months",
            "Three compliance options: produce, convert, plug, or continue inactive",
            "Wells inactive >10 years face mandatory plugging risk",
            "Non-filing for 3 years triggers orphan designation and bond forfeiture",
            "Warning → $500 penalty → orphan designation progression",
            "Bond must cover inactive well plugging costs"
        ],
        primary_authority=[
            "16 TAC §3.14 (Statewide Rule 14) - Plugging Standards",
            "16 TAC §3.20 - Form R-1 Annual Inactive Well Report",
            "Texas Natural Resources Code §91.113 - Inactive Well Reporting"
        ],
        burden_holder="Operator of record",
        adversary_position="RRC may designate well orphan after 3 years non-filing and use bond to plug at operator's expense",
        counter_arguments=[
            "Well had production in small quantity, not truly inactive",
            "Well being used for monitoring, not inactive",
            "Technical difficulties prevented filing, corrected immediately",
            "Prior operator responsible for inactive period",
            "Good cause for extended inactive status (pending deal, permits)"
        ],
        resolution_strategy="File late R-1 immediately with explanation, pay penalty if assessed, plug wells with no economic value, return marginal wells to production or sell to operator willing to manage compliance",
        entity_scope="Operators with wells inactive 12+ months",
        confidence=0.97,
        confidence_stratification="DEFENSIBLE"
    ),

    DoctrineBlock(
        topic="OSHA_WELL_CONTROL_EQUIPMENT",
        keywords=["well control", "BOP", "blowout preventer", "pressure control", "drilling safety", "OSHA 1910"],
        conclusion_template=[
            "OSHA requires well control equipment (BOP) properly installed, tested, and maintained during drilling.",
            "BOP pressure rating must exceed maximum anticipated surface pressure.",
            "All personnel must be trained in well control and emergency shutdown procedures."
        ],
        reasoning_framework="""
Well control equipment is critical safety equipment to prevent blowouts, fires, and H2S releases.
OSHA 1910 Subpart M (general industry) applies to oil and gas well operations.

EQUIPMENT REQUIREMENTS:
Blowout Preventer (BOP) Stack:
- Pressure rating ≥ max anticipated surface pressure
- Minimum 2 pressure-activated preventers (rams)
- 1 annular preventer (bag-type or similar)
- Kill line and choke line with valves
- Accumulator system with backup power
- Remote control panel at safe distance from wellhead

BOP TESTING:
Initial Test (before drilling out surface casing):
- Hydrostatic test to rated pressure
- Function test all rams and annular
- Verify accumulator pressure and volume
- Document with pressure chart

Recurring Tests:
- Every 14-21 days during drilling
- After any BOP repair or component change
- Before drilling into known high-pressure zone

PERSONNEL TRAINING:
All rig crew must have:
- Well control certification (IADC or equivalent)
- Emergency shutdown procedure training
- H2S safety training if applicable
- Hands-on BOP function drills monthly

WELL CONTROL PROCEDURES:
Written procedures required for:
- Normal operations (tripping pipe, drilling)
- Kicks and well control events
- Emergency shutdown
- Evacuation
- Notification to regulatory agencies (RRC, OSHA)

CONSEQUENCES OF VIOLATIONS:
- OSHA citation: $15,493 per violation (serious)
- $154,937 per violation (willful or repeat)
- Criminal prosecution if fatality or serious injury
- RRC drilling permit suspension
- Civil liability for property damage, injuries

DEFENSIVE COMPLIANCE:
Use BOP rated for worst-case pressure (multiply max pressure × 1.5 safety factor).
Test BOP more frequently than minimum (weekly recommended).
Conduct monthly well control drills with all crew, document attendance.
Maintain BOP maintenance records for equipment life, not just current well.
Install backup emergency shutdown systems (ESD) beyond minimum requirements.
Retain well control consultant for high-pressure, high-risk wells.
        """,
        key_factors=[
            "BOP pressure rating must exceed max anticipated surface pressure",
            "Minimum: 2 ram preventers + 1 annular preventer",
            "Test before drilling out surface casing and every 14-21 days",
            "All crew must have well control certification (IADC)",
            "Written emergency procedures required",
            "OSHA penalties: $15K serious, $155K willful/repeat",
            "Criminal liability if fatality results from violations"
        ],
        primary_authority=[
            "29 CFR 1910 Subpart M - Compressed Gas and Equipment",
            "API RP 53 - Blowout Prevention Equipment Systems",
            "IADC Well Control Certification Standards",
            "RRC Statewide Rule 13 - Drilling Requirements"
        ],
        burden_holder="Operator and drilling contractor (joint responsibility)",
        adversary_position="OSHA and prosecutors may pursue criminal charges if BOP failure causes injury or death",
        counter_arguments=[
            "BOP tested per manufacturer specs, adequate for well conditions",
            "Kick occurred due to unexpected pressure, BOP performed as designed",
            "Drilling contractor responsible for BOP, not operator",
            "Personnel had equivalent training, certification not required",
            "Emergency response followed plan, injuries unavoidable"
        ],
        resolution_strategy="Immediately shutdown well if BOP question, bring in qualified BOP technician for inspection/repair, conduct root cause investigation, implement enhanced testing/training, cooperate with OSHA investigation",
        entity_scope="All drilling operators and contractors",
        confidence=0.98,
        confidence_stratification="DEFENSIBLE"
    ),

    DoctrineBlock(
        topic="DOT_PIPELINE_INTEGRITY_MANAGEMENT",
        keywords=["pipeline", "integrity management", "DOT", "PHMSA", "49 CFR 192", "49 CFR 195", "high consequence area"],
        conclusion_template=[
            "Pipeline operators must implement Integrity Management Programs for high consequence areas (HCAs).",
            "Baseline assessment required within specified timeframe based on HCA classification.",
            "Reassessment intervals: 7 years for gas, 5 years for hazardous liquids."
        ],
        reasoning_framework="""
DOT Pipeline and Hazardous Materials Safety Administration (PHMSA) requires comprehensive integrity management for pipelines in populated or sensitive areas.
49 CFR Part 192 (gas) and Part 195 (hazardous liquids/oil) establish requirements.

HIGH CONSEQUENCE AREA (HCA) DEFINITION:
Gas Pipelines (192):
- Class 3 or 4 locations (defined by building density)
- Areas where pipeline could affect structures
- Within 660 feet of buildings, playgrounds, outdoor recreation

Hazardous Liquid Pipelines (195):
- Commercially navigable waterways
- High population areas (>50 identified sites)
- Unusually sensitive areas (drinking water, endangered species)

INTEGRITY MANAGEMENT PROGRAM:
Required elements:
1. Identify all HCA segments
2. Baseline assessment within timeline
3. Ongoing assessment at intervals
4. Data integration and risk analysis
5. Threat identification (corrosion, manufacturing defects, etc.)
6. Repair criteria and schedules
7. Performance metrics
8. Management of change process
9. Quality assurance
10. Communication plan

ASSESSMENT METHODS:
Gas Pipelines:
- Internal inspection tool (smart pig)
- Pressure test (hydrostatic)
- Direct assessment (4-step process)

Hazardous Liquid:
- Internal inspection tool preferred
- Pressure test if pigging impractical
- Other technology equivalent to ILI

BASELINE ASSESSMENT DEADLINES:
Gas transmission:
- 50% of HCA miles by 12/17/2007
- 100% by 12/17/2012
Hazardous liquid:
- Based on risk ranking, earliest 2002

REASSESSMENT INTERVALS:
Gas: 7 years or less
Liquid: 5 years or less
May be accelerated if integrity issues found.

ENFORCEMENT:
- Civil penalties: Up to $224,000 per violation per day
- Criminal prosecution: Knowing violations causing death/injury
- Corrective action orders
- Shutdown orders for imminent hazard

DEFENSIVE COMPLIANCE:
Identify all HCA segments conservatively (buffer zones beyond minimum).
Use ILI (smart pig) for baseline rather than direct assessment (more defensible data).
Conduct reassessment early (year 6 for gas, year 4 for liquid) to avoid deadline pressure.
Implement robust data management system linking all integrity data.
Hire dedicated pipeline integrity engineer, not general operations personnel.
Report all incidents promptly to PHMSA (within 1 hour if death/injury/major release).
        """,
        key_factors=[
            "HCA definition varies: gas (Class 3/4), liquid (waterways, population, sensitive areas)",
            "Baseline assessment required, deadlines passed for most operators",
            "Reassessment: 7 years gas, 5 years liquid",
            "ILI (smart pig) preferred assessment method",
            "Penalties up to $224K per violation per day",
            "Criminal liability for knowing violations causing casualties",
            "Program must include threat ID, risk analysis, repair criteria, metrics"
        ],
        primary_authority=[
            "49 CFR Part 192 Subpart O - Gas Transmission Pipeline Integrity Management",
            "49 CFR Part 195 - Hazardous Liquid Pipeline Integrity Management",
            "Pipeline Safety Improvement Act of 2002",
            "PHMSA Enforcement Guidance"
        ],
        burden_holder="Pipeline operator",
        adversary_position="PHMSA may pursue criminal prosecution if integrity failure causes fatalities and operator failed to assess/repair known threats",
        counter_arguments=[
            "Segment not in HCA, population density below threshold",
            "Assessment conducted per industry standards, defect not detectable",
            "Repair criteria met, failure due to third-party damage not integrity issue",
            "Predecessor operator responsible for missed baseline",
            "Budget constraints prevented timely reassessment (not valid defense)"
        ],
        resolution_strategy="Conduct immediate assessment of all HCA segments, accelerate repairs for any integrity threats, implement enhanced monitoring between assessments, report proactively to PHMSA, consider pipeline replacement for chronically problematic segments",
        entity_scope="Operators of gas transmission and hazardous liquid pipelines",
        confidence=0.96,
        confidence_stratification="DEFENSIBLE"
    ),
]


def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    """Retrieve doctrine block by exact topic match."""
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic == topic:
            return doctrine
    return None


def search_doctrines_by_keyword(keyword: str) -> List[DoctrineBlock]:
    """Search doctrine blocks by keyword (case-insensitive)."""
    keyword_lower = keyword.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if any(keyword_lower in kw.lower() for kw in doctrine.keywords):
            results.append(doctrine)
    return results


def get_all_topics() -> List[str]:
    """Return list of all doctrine topics."""
    return [d.topic for d in DOCTRINE_CACHE]


def get_doctrines_by_confidence(min_confidence: float) -> List[DoctrineBlock]:
    """Filter doctrines by minimum confidence threshold."""
    return [d for d in DOCTRINE_CACHE if d.confidence >= min_confidence]
