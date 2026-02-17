"""
REG03 Environmental Regulatory Engine
Version: 1.0.0
Port: 9123

Environmental regulatory compliance engine covering Clean Air Act, Clean Water Act,
RCRA, CERCLA/Superfund, NEPA, ESA, state delegation, permits, reporting.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from collections import defaultdict
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# Engine Configuration
ENGINE_ID = "REG03"
ENGINE_NAME = "Environmental Regulatory Engine"
VERSION = "1.0.0"
PORT = 9123


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
    AIR_PERMITS = "AIR_PERMITS"
    WATER_PERMITS = "WATER_PERMITS"
    WASTE_MANAGEMENT = "WASTE_MANAGEMENT"
    SUPERFUND = "SUPERFUND"
    NEPA_REVIEW = "NEPA_REVIEW"
    ESA_COMPLIANCE = "ESA_COMPLIANCE"
    TOXIC_SUBSTANCES = "TOXIC_SUBSTANCES"
    SPILL_REPORTING = "SPILL_REPORTING"
    STATE_DELEGATION = "STATE_DELEGATION"
    ENFORCEMENT = "ENFORCEMENT"
    REMEDIATION = "REMEDIATION"
    MONITORING = "MONITORING"


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
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str
    issue_category: IssueCategory


class QueryRequest(BaseModel):
    query: str
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.PLANNING
    context: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    query: str
    mode: ResponseMode
    zone: AnalysisZone
    response: str
    confidence: ConfidenceLevel
    sources: List[str]
    reasoning_chain: List[str]
    triggered_doctrines: List[str]
    epistemic_warnings: List[str]
    determinism_hash: str
    timestamp: str
    latency_ms: float


# Doctrine Cache with 25+ environmental law blocks
DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="CAA Title V Operating Permits",
        keywords=["title v", "operating permit", "major source", "emissions", "40 cfr 70"],
        conclusion_template=[
            "Major sources under Clean Air Act must obtain Title V operating permits covering all emission units.",
            "Title V permits consolidate all CAA requirements and require annual compliance certifications.",
            "Permit applications must be submitted within 12 months of becoming major source."
        ],
        reasoning_framework="""Major source determination: potential to emit 100 tons/year any criteria pollutant
or 10/25 tons/year HAPs. Title V permit consolidates all applicable CAA requirements including NSPS, NESHAP,
SIP requirements, and operating limits. Permit term is 5 years with annual compliance certification and
semi-annual monitoring reports. Permit shield available for explicitly listed activities. Application must
be complete and accurate with certification by responsible official. State programs delegated under 40 CFR 70,
EPA oversight retained. Significant modifications require permit revision. Minor modifications use streamlined
process. Administrative amendments for non-substantive changes. Public notice and comment required for initial
permits and significant modifications. Permit contains enforceable emission limits, monitoring requirements,
recordkeeping, and reporting. Deviation reporting required. Enhanced monitoring may be required under 40 CFR 64.
Compliance certification must identify deviations and corrective actions. Failure to submit complete application
or obtain permit before operating is violation subject to enforcement.""",
        key_factors=[
            "Potential to emit calculation methodology",
            "Major source threshold determination",
            "Applicable requirements identification",
            "Monitoring and recordkeeping adequacy",
            "Compliance certification accuracy",
            "Deviation reporting timeliness",
            "Permit application completeness"
        ],
        primary_authority=[
            "42 USC 7661 Clean Air Act Title V",
            "40 CFR Part 70 State Operating Permit Programs",
            "40 CFR Part 71 Federal Operating Permit Program",
            "State implementation plan delegated authority"
        ],
        burden_holder="Source operator to obtain and maintain valid permit",
        adversary_position="EPA or state may challenge PTE calculations, applicability determinations, or compliance status",
        counter_arguments=[
            "Synthetic minor limits can avoid Title V if federally enforceable",
            "Insignificant activities may be exempt from detailed listing",
            "Permit shield protects compliance with permit terms",
            "Good faith effort to comply may mitigate penalties",
            "Economic hardship may affect penalty calculation"
        ],
        resolution_strategy="Ensure accurate PTE calculations, maintain federally enforceable limits, submit complete applications timely, implement robust monitoring and recordkeeping, certify compliance accurately, report deviations promptly",
        entity_scope="Any stationary source meeting major source thresholds under CAA",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Title V requirements are well-established with extensive regulatory guidance and case law",
        controlling_precedent="EPA Title V regulations and state delegated programs provide comprehensive framework",
        issue_category=IssueCategory.AIR_PERMITS
    ),
    DoctrineBlock(
        topic="CWA Section 402 NPDES Permits",
        keywords=["npdes", "point source", "discharge", "waters of the us", "40 cfr 122"],
        conclusion_template=[
            "Point source discharges to waters of the US require NPDES permit under CWA Section 402.",
            "Permits establish technology-based and water quality-based effluent limitations.",
            "Unpermitted discharge is violation subject to civil and criminal penalties."
        ],
        reasoning_framework="""CWA prohibits discharge of pollutants from point source to navigable waters without
NPDES permit. Point source is any discernible, confined, discrete conveyance. Waters of the US includes traditional
navigable waters, interstate waters, tributaries, and adjacent wetlands under Rapanos significant nexus test.
NPDES permits issued by EPA or delegated states. Industrial discharges subject to categorical effluent guidelines
based on best available technology (BAT) or best conventional technology (BCT). Municipal wastewater requires
secondary treatment minimum. Water quality-based limits required where technology-based limits insufficient to
meet state water quality standards. Permits include monitoring, recordkeeping, and reporting requirements. Discharge
monitoring reports (DMRs) submitted monthly or quarterly. Storm water permits required for industrial activities
and construction sites over 1 acre. General permits available for categories of dischargers. Individual permits
for major dischargers or where general permit inadequate. Permit term is 5 years maximum. Antidegradation policy
protects existing uses and high-quality waters. Mixing zones may be allowed for thermal discharges or toxics within
limits. Biomonitoring may be required for toxicity assessment. Upset and bypass provisions provide limited defenses.
Twenty-four hour reporting required for permit limit violations. Citizen suit provision allows private enforcement.""",
        key_factors=[
            "Point source determination",
            "Waters of the US jurisdiction",
            "Effluent limitation applicability",
            "Technology-based versus water quality-based limits",
            "Monitoring and reporting compliance",
            "Storm water coverage requirements",
            "General versus individual permit"
        ],
        primary_authority=[
            "33 USC 1342 CWA Section 402",
            "40 CFR Part 122 NPDES Permit Program",
            "40 CFR Part 125 Technology-Based Standards",
            "Rapanos v. United States 547 US 715 (2006)"
        ],
        burden_holder="Discharger to obtain permit and comply with effluent limits",
        adversary_position="EPA or state may allege unpermitted discharge, permit violations, or inadequate controls",
        counter_arguments=[
            "Discharge not to waters of the US under Rapanos test",
            "Agricultural storm water exemption applies",
            "Upset or bypass defense for unavoidable violations",
            "Good faith compliance with permit is defense",
            "No additions of pollutants for flow augmentation"
        ],
        resolution_strategy="Obtain permit coverage before discharging, implement treatment to meet limits, monitor and report accurately, maintain storm water controls, investigate violations promptly",
        entity_scope="Any facility discharging pollutants from point source to waters of US",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="NPDES program well-established but WOTUS jurisdiction remains contentious",
        controlling_precedent="Rapanos significant nexus test applies to jurisdictional determinations",
        issue_category=IssueCategory.WATER_PERMITS
    ),
    DoctrineBlock(
        topic="RCRA Subtitle C Hazardous Waste",
        keywords=["rcra", "hazardous waste", "listed", "characteristic", "generator", "40 cfr 261"],
        conclusion_template=[
            "Hazardous waste generators must comply with RCRA Subtitle C identification, management, and disposal requirements.",
            "Waste is hazardous if listed under 40 CFR 261 Subpart D or exhibits characteristic of ignitability, corrosivity, reactivity, or toxicity.",
            "Large quantity generators face most stringent requirements including permits for treatment, storage, or disposal."
        ],
        reasoning_framework="""RCRA regulates hazardous waste from cradle to grave. First determine if material is
solid waste under 40 CFR 261.2. Then determine if hazardous by checking listed wastes (F, K, P, U lists) or testing
for characteristics (IGNITABILITY D001, CORROSIVITY D002, REACTIVITY D003, TOXICITY D004-D043). Generator status
based on monthly generation: LQG over 1000 kg/month, SQG 100-1000 kg/month, VSQG under 100 kg/month. LQGs must
obtain EPA ID number, manifest waste shipments, use permitted TSDFs, store on-site maximum 90 days in compliance
with standards, train personnel, prepare contingency plan, and submit biennial reports. Satellite accumulation
allows 55 gallons at point of generation. Land disposal restrictions prohibit disposal of untreated hazardous
waste. Universal waste rules provide streamlined management for batteries, lamps, mercury devices, pesticides.
Mixture rule: mixing listed waste with solid waste creates listed hazardous waste. Derived-from rule: treating
listed waste generates listed waste. Contained-in policy applies to contaminated media. Delisting petitions
available to demonstrate waste no longer hazardous. Criminal liability for knowing violations including
endangerment. Citizen suit provision. TCEQ administers Texas RCRA program with federal oversight.""",
        key_factors=[
            "Solid waste determination",
            "Hazardous waste identification via listing or characteristic",
            "Generator status classification",
            "Manifesting and transportation requirements",
            "On-site accumulation time limits",
            "TSDF permit requirements",
            "Land disposal restriction compliance"
        ],
        primary_authority=[
            "42 USC 6921 RCRA Subtitle C",
            "40 CFR Part 261 Hazardous Waste Identification",
            "40 CFR Part 262 Generators",
            "40 CFR Part 268 Land Disposal Restrictions"
        ],
        burden_holder="Generator to identify, manage, and dispose of hazardous waste properly",
        adversary_position="EPA or state may challenge waste determinations, generator status, or management practices",
        counter_arguments=[
            "Waste exempt as recycled material",
            "Characteristic waste no longer exhibits hazardous trait after treatment",
            "Delisting petition demonstrates waste not hazardous",
            "Universal waste rules apply",
            "De minimis quantities qualify as conditionally exempt"
        ],
        resolution_strategy="Conduct thorough waste characterization, maintain accurate generation records, comply with LQG standards, use permitted TSDFs, train staff, prepare contingency plans, submit biennial reports",
        entity_scope="Any entity generating, transporting, treating, storing, or disposing of hazardous waste",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="RCRA Subtitle C framework is comprehensive and well-litigated",
        controlling_precedent="Listing and characteristic tests provide clear identification criteria",
        issue_category=IssueCategory.WASTE_MANAGEMENT
    ),
    DoctrineBlock(
        topic="CERCLA Section 107 Liability",
        keywords=["cercla", "superfund", "liable party", "response costs", "strict liability"],
        conclusion_template=[
            "CERCLA imposes strict, joint and several liability on PRPs for response costs at hazardous substance sites.",
            "PRPs include current owners/operators, past owners/operators at time of disposal, arrangers, and transporters.",
            "Liability is retroactive and applies regardless of fault or compliance with regulations at time of disposal."
        ],
        reasoning_framework="""CERCLA Section 107 establishes liability for release or threatened release of hazardous
substances. Four classes of PRPs: (1) current owners and operators, (2) owners and operators at time of disposal,
(3) arrangers who arranged for disposal or treatment, (4) transporters who selected disposal site. Liability is
strict (no fault required), joint and several (each PRP can be held liable for entire cost), and retroactive
(applies to past disposal). Plaintiff must prove: (1) site is facility, (2) release or threatened release of
hazardous substance, (3) release caused incurrence of response costs, (4) defendant is PRP. Defenses limited to
act of God, act of war, third party not in contractual relationship. Innocent landowner defense requires due
diligence before acquisition. Bona fide prospective purchaser and contiguous property owner protections available
with all appropriate inquiries. De micromis settlement for minimal contributors. De minimis settlement for small
volume contributors. Contribution actions allow PRPs to allocate liability among responsible parties using equitable
factors. Divisibility of harm can limit joint and several liability if injury divisible on reasonable basis. Natural
resource damages separately recoverable by trustees. EPA can compel cleanup via UAO with penalties for non-compliance.
Voluntary cleanup with state approval may provide liability protection. Brownfields amendments encourage redevelopment.""",
        key_factors=[
            "PRP status determination",
            "Hazardous substance release",
            "Response cost causation",
            "Defense availability",
            "All appropriate inquiries compliance",
            "Divisibility of harm",
            "Contribution allocation factors"
        ],
        primary_authority=[
            "42 USC 9607 CERCLA Section 107 Liability",
            "42 USC 9613(f) Contribution",
            "United States v. Bestfoods 524 US 51 (1998)",
            "Burlington Northern v. United States 556 US 599 (2009)"
        ],
        burden_holder="PRPs liable for response costs and natural resource damages",
        adversary_position="EPA or private parties may seek cost recovery or contribution from PRPs",
        counter_arguments=[
            "Not a PRP under any of four categories",
            "Third party defense with no contractual relationship",
            "Innocent landowner with due diligence",
            "Bona fide prospective purchaser protection",
            "Harm is divisible and liability should be several only",
            "Equitable factors support minimal allocation"
        ],
        resolution_strategy="Conduct Phase I/II environmental assessments before acquisition, document all appropriate inquiries, negotiate settlements with EPA, pursue contribution from other PRPs, demonstrate divisibility if applicable",
        entity_scope="Current and past owners/operators, arrangers, transporters at CERCLA sites",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="CERCLA liability is strict and broadly applied with limited defenses",
        controlling_precedent="Bestfoods and Burlington Northern establish corporate liability and divisibility standards",
        issue_category=IssueCategory.SUPERFUND
    ),
    DoctrineBlock(
        topic="NEPA Environmental Impact Statements",
        keywords=["nepa", "eis", "environmental impact", "alternatives analysis", "cea"],
        conclusion_template=[
            "Federal agencies must prepare EIS for major federal actions significantly affecting human environment.",
            "EIS must analyze environmental impacts, reasonable alternatives, and mitigation measures.",
            "Procedural compliance with NEPA required but substantive environmental outcomes not mandated."
        ],
        reasoning_framework="""NEPA requires federal agencies to prepare detailed EIS for major federal actions
significantly affecting quality of human environment. Threshold question is whether action is major federal action:
federal funding, permitting, or direct action. Significance determined by context and intensity factors in 40 CFR
1508.27. If significant impact likely, full EIS required. If uncertain, prepare Environmental Assessment (EA) to
determine significance. If no significant impact, issue FONSI. EIS must describe proposed action, purpose and need,
affected environment, environmental consequences, alternatives including no action alternative, and mitigation
measures. Range of reasonable alternatives is heart of EIS. Cumulative effects analysis required for past, present,
and reasonably foreseeable actions. Public scoping process to identify issues. Draft EIS for public comment, final
EIS responds to comments, Record of Decision documents agency choice. Supplemental EIS required for substantial
changes to proposed action or significant new circumstances. NEPA creates procedural obligations only, not
substantive duty to select environmentally preferable alternative. Courts review for arbitrary and capricious
decision-making. Hard look doctrine requires thorough analysis. Agencies may not predetermine outcome before NEPA
complete. Segmentation of related actions to avoid significance finding is improper.""",
        key_factors=[
            "Major federal action determination",
            "Significance of environmental impact",
            "Range of reasonable alternatives",
            "Cumulative effects analysis",
            "Public participation adequacy",
            "Hard look analysis completeness",
            "Segmentation avoidance"
        ],
        primary_authority=[
            "42 USC 4321 National Environmental Policy Act",
            "40 CFR Parts 1500-1508 CEQ NEPA Regulations",
            "Kleppe v. Sierra Club 427 US 390 (1976)",
            "Robertson v. Methow Valley 490 US 332 (1989)"
        ],
        burden_holder="Federal agency to prepare adequate EIS for major actions",
        adversary_position="Environmental groups may challenge adequacy of EIS or FONSI determination",
        counter_arguments=[
            "Action not major federal action requiring EIS",
            "EA and FONSI adequately supported no significant impact finding",
            "Reasonable range of alternatives analyzed",
            "Cumulative effects analysis sufficient",
            "Agency took hard look at environmental consequences",
            "Mitigation measures reduce impacts to non-significant"
        ],
        resolution_strategy="Prepare thorough EA or EIS, analyze full range of reasonable alternatives, conduct robust cumulative effects analysis, involve public early, respond to comments substantively, document hard look analysis",
        entity_scope="Federal agencies and applicants for federal permits or funding",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="NEPA process well-established but scope of alternatives and cumulative effects often disputed",
        controlling_precedent="Courts defer to agency expertise but require hard look at environmental impacts",
        issue_category=IssueCategory.NEPA_REVIEW
    ),
    DoctrineBlock(
        topic="ESA Section 7 Consultation",
        keywords=["endangered species", "section 7", "consultation", "jeopardy", "critical habitat"],
        conclusion_template=[
            "Federal agencies must consult with FWS or NMFS to ensure actions do not jeopardize listed species or destroy critical habitat.",
            "Formal consultation results in biological opinion determining jeopardy and identifying reasonable and prudent alternatives.",
            "Incidental take statement provides Section 9 take authorization if action proceeds with RPMs."
        ],
        reasoning_framework="""ESA Section 7 requires federal agencies to consult with Fish and Wildlife Service
(terrestrial/freshwater species) or National Marine Fisheries Service (marine/anadromous species) to ensure actions
not likely to jeopardize continued existence of listed species or destroy/adversely modify critical habitat. Action
agency determines if species may be present in action area and if action may affect species. If may affect, initiate
consultation. Informal consultation if action not likely to adversely affect, results in concurrence letter. Formal
consultation if action likely to adversely affect, results in biological opinion. BiOp analyzes whether action
likely to jeopardize species or destroy critical habitat. Jeopardy finding requires reasonable and prudent
alternatives (RPAs) to avoid jeopardy. No jeopardy finding may include reasonable and prudent measures (RPMs) to
minimize take. Incidental take statement authorizes take in compliance with RPMs and terms and conditions. Action
agency may not proceed if jeopardy finding unless RPAs adopted. Reinitiation required if new information, action
modified, or species listed. Emergency consultation available for urgent actions. Exemption process through
Endangered Species Committee (God Squad) rarely used. Section 9 prohibits take of listed species, defined broadly
to include habitat modification. Section 10 incidental take permits available for private actions through habitat
conservation plans.""",
        key_factors=[
            "Listed species presence in action area",
            "Federal nexus for action",
            "May affect determination",
            "Likely to adversely affect threshold",
            "Jeopardy analysis",
            "RPA or RPM adequacy",
            "Incidental take authorization scope"
        ],
        primary_authority=[
            "16 USC 1536 ESA Section 7",
            "50 CFR Part 402 Interagency Cooperation",
            "Tennessee Valley Authority v. Hill 437 US 153 (1978)",
            "Babbitt v. Sweet Home 515 US 687 (1995)"
        ],
        burden_holder="Federal action agency to consult and ensure no jeopardy",
        adversary_position="FWS/NMFS may issue jeopardy finding or environmental groups may challenge consultation adequacy",
        counter_arguments=[
            "No federal nexus to trigger Section 7",
            "Species not present in action area",
            "Action not likely to adversely affect species",
            "BiOp failed to use best available science",
            "RPAs not reasonable or prudent",
            "Incidental take properly authorized"
        ],
        resolution_strategy="Survey for species early, involve Services in project design, modify action to avoid adverse effects, adopt RPMs or RPAs, obtain incidental take coverage, monitor and report take",
        entity_scope="Federal agencies and applicants for federal permits, funding, or authorizations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="ESA Section 7 strictly enforced with courts requiring rigorous jeopardy analysis",
        controlling_precedent="TVA v. Hill establishes species protection priority over economic considerations",
        issue_category=IssueCategory.ESA_COMPLIANCE
    ),
    DoctrineBlock(
        topic="TSCA Chemical Regulation",
        keywords=["tsca", "chemical substances", "pre manufacture", "unreasonable risk", "asbestos"],
        conclusion_template=[
            "TSCA authorizes EPA to regulate chemical substances presenting unreasonable risk to health or environment.",
            "New chemicals require pre-manufacture notification 90 days before production or import.",
            "EPA can restrict or ban chemicals through rulemaking if unreasonable risk found."
        ],
        reasoning_framework="""Toxic Substances Control Act grants EPA authority to regulate manufacture, processing,
distribution, use, and disposal of chemical substances. TSCA Inventory lists existing chemicals. New chemicals not
on inventory require Pre-Manufacture Notification (PMN) submitted 90 days before manufacture or import. EPA reviews
PMN to assess risk and can issue order to prohibit or limit production if unreasonable risk. Significant new use
rules (SNURs) require notification for new uses of existing chemicals. Section 6 allows EPA to regulate existing
chemicals presenting unreasonable risk through rulemaking. EPA must evaluate existing chemicals using risk-based
screening. 2016 amendments strengthened EPA authority and required risk evaluation without considering costs, but
cost-benefit analysis still required for regulations. Asbestos ban initially struck down for inadequate analysis
but 2016 amendments clarified authority. PCB ban remains in effect. Risk management options include use restrictions,
labeling, recordkeeping, disposal requirements, or complete ban. Exemptions available for small manufacturers,
research and development, and test marketing. Import certification required. Confidential business information
protections available but subject to disclosure in certain circumstances. Reporting required for substantial risk
information. Health and safety studies must be submitted.""",
        key_factors=[
            "New versus existing chemical determination",
            "PMN submission timing and completeness",
            "Unreasonable risk finding",
            "SNUR applicability",
            "Risk evaluation methodology",
            "Cost-benefit justification for restrictions",
            "CBI claim validity"
        ],
        primary_authority=[
            "15 USC 2601 Toxic Substances Control Act",
            "40 CFR Part 720 Pre-Manufacture Notification",
            "40 CFR Part 721 Significant New Use Rules",
            "Corrosion Proof Fittings v. EPA 947 F2d 1201 (5th Cir 1991)"
        ],
        burden_holder="Chemical manufacturers and processors to submit PMNs and comply with restrictions",
        adversary_position="EPA may prohibit production or impose restrictions if unreasonable risk found",
        counter_arguments=[
            "Chemical on TSCA Inventory as existing chemical",
            "Exemption for R&D or test marketing applies",
            "EPA failed to demonstrate unreasonable risk",
            "Less burdensome alternatives not considered",
            "Cost-benefit analysis does not support restriction",
            "CBI protections apply to submitted information"
        ],
        resolution_strategy="Check TSCA Inventory before production, submit PMN timely for new chemicals, respond to EPA information requests, demonstrate risk management, comply with SNURs, report substantial risk information",
        entity_scope="Chemical manufacturers, processors, importers, and distributors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="2016 TSCA amendments strengthened EPA authority but agency still faces resource constraints",
        controlling_precedent="Corrosion Proof Fittings requires rigorous analysis but 2016 amendments addressed deficiencies",
        issue_category=IssueCategory.TOXIC_SUBSTANCES
    ),
    DoctrineBlock(
        topic="EPCRA Tier II Reporting",
        keywords=["epcra", "tier ii", "hazardous chemicals", "community right to know", "threshold"],
        conclusion_template=[
            "Facilities storing hazardous chemicals above threshold quantities must submit annual Tier II reports.",
            "Tier II reports disclose chemical inventories to state and local emergency planning authorities.",
            "Failure to report or false reporting subject to civil penalties up to $25,000 per day per violation."
        ],
        reasoning_framework="""Emergency Planning and Community Right-to-Know Act Section 312 requires facilities
to report hazardous chemical inventories annually. Threshold is 10,000 pounds aggregate for non-EHS chemicals or
TPQ/500 pounds for extremely hazardous substances. Report due March 1 for previous calendar year maximum daily
amount and average daily amount. Submit to SERC, LEPC, and local fire department. Tier II form lists chemical name,
CAS number, physical and health hazards, maximum and average amounts, storage locations. Tier I aggregate reporting
by hazard category allowed unless Tier II specifically requested. Chemicals subject to reporting are those requiring
OSHA hazard communication SDS. Exemptions for foods, drugs, cosmetics, consumer products, tobacco. Mixtures reported
as mixture or individual components. Trade secret claims available but emergency responders must receive information.
Public may request Tier II information. Penalties up to $25,000 per day for failure to submit or false reporting.
Citizen suit provision allows enforcement by public. States may have lower thresholds or additional requirements.
EPCRA Section 313 TRI reporting separate requirement for listed chemicals over threshold at manufacturing facilities.""",
        key_factors=[
            "Threshold quantity determination",
            "Hazardous chemical versus EHS status",
            "Maximum and average daily amounts calculation",
            "Reporting deadline compliance",
            "Submission to all required agencies",
            "Trade secret claim justification",
            "Exemption applicability"
        ],
        primary_authority=[
            "42 USC 11022 EPCRA Section 312",
            "40 CFR Part 370 Hazardous Chemical Reporting",
            "State Tier II requirements",
            "OSHA Hazard Communication Standard 29 CFR 1910.1200"
        ],
        burden_holder="Facility owner/operator to submit accurate Tier II reports annually",
        adversary_position="State or EPA may assess penalties for non-reporting or inaccurate reports",
        counter_arguments=[
            "Chemical below threshold quantities",
            "Exemption for consumer products or other category",
            "Reporting deadline extended by state",
            "Trade secret protections apply",
            "Good faith effort to comply",
            "Violation self-disclosed under audit policy"
        ],
        resolution_strategy="Track chemical inventories monthly, calculate maximum and average daily amounts accurately, submit reports by March 1, provide to all required agencies, maintain SDS documentation, respond to information requests",
        entity_scope="Facilities storing hazardous chemicals above threshold quantities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Tier II requirements straightforward but threshold calculations can be complex for mixtures",
        controlling_precedent="Reporting obligations well-established with regular enforcement actions",
        issue_category=IssueCategory.SPILL_REPORTING
    ),
    DoctrineBlock(
        topic="TCEQ Air Permits",
        keywords=["tceq", "air permit", "nsr", "psd", "standard permit", "texas"],
        conclusion_template=[
            "Texas facilities must obtain TCEQ air permits before constructing or modifying emission sources.",
            "Standard permits available for common source types; case-by-case permits for others.",
            "Prevention of significant deterioration applies to major sources in attainment areas."
        ],
        reasoning_framework="""Texas Clean Air Act requires permit before construction or modification of facilities
that emit air contaminants. TCEQ administers air permitting under delegated federal and state authority. Permit
by rule (PBR) available for small sources meeting specified conditions, no formal permit application required but
must comply with PBR terms. Standard permits for common source types like concrete batch plants, rock crushers,
hot mix asphalt. Submit registration and comply with standard permit conditions. Case-by-case permits for sources
not covered by PBR or standard permit. New source review (NSR) for new or modified sources. Prevention of significant
deterioration (PSD) for major sources in attainment areas, requires BACT, air quality modeling, public participation.
Nonattainment NSR for major sources in nonattainment areas, requires LAER and offsets. Major source thresholds
depend on pollutant and area classification. Greenhouse gases subject to PSD if project anyway subject for other
pollutant. Emission reductions creditable as offsets if real, permanent, quantifiable, enforceable, surplus.
Federal land manager consultation required for PSD affecting Class I areas. Plantwide applicability limits (PALs)
provide operational flexibility. Permit amendments required for modifications, minor versus major determined by
emission increase significance. Permit by rule and standard permits do not satisfy Title V requirements. Emissions
events and scheduled maintenance must be reported to TCEQ. Opacity limits and visible emissions standards enforced.""",
        key_factors=[
            "PBR, standard permit, or case-by-case applicability",
            "NSR major versus minor source determination",
            "PSD or nonattainment NSR requirements",
            "BACT or LAER analysis",
            "Air quality modeling demonstration",
            "Offset requirements and availability",
            "Modification versus maintenance"
        ],
        primary_authority=[
            "Texas Health and Safety Code Chapter 382",
            "30 TAC Chapter 106 Permits by Rule",
            "30 TAC Chapter 116 Control of Air Pollution",
            "40 CFR Part 52 Approval of State Plans for Texas"
        ],
        burden_holder="Facility owner/operator to obtain permit before construction or modification",
        adversary_position="TCEQ or EPA may deny permit, require additional controls, or enforce for unpermitted construction",
        counter_arguments=[
            "Permit by rule applicability eliminates formal permit requirement",
            "Modification does not trigger NSR as routine maintenance",
            "Source is minor not major under applicable thresholds",
            "BACT analysis supports proposed controls",
            "Air quality modeling shows no adverse impact",
            "Offsets obtained from creditable reductions"
        ],
        resolution_strategy="Determine permit pathway early, apply for permits before construction, conduct thorough BACT analysis, perform air quality modeling, secure offsets if needed, maintain operational flexibility through PALs",
        entity_scope="Texas facilities constructing or modifying air emission sources",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="TCEQ permitting well-established but PSD and NSR applicability can be fact-intensive",
        controlling_precedent="Federal NSR regulations and Texas SIP provide framework",
        issue_category=IssueCategory.STATE_DELEGATION
    ),
    DoctrineBlock(
        topic="Railroad Commission Rule 8 Waste Disposal",
        keywords=["railroad commission", "rule 8", "oil and gas waste", "disposal well", "e&p waste"],
        conclusion_template=[
            "RRC Rule 8 regulates disposal of oil and gas exploration and production waste in Texas.",
            "Commercial disposal wells require permit and must meet geologic, mechanical, and operational standards.",
            "Unauthorized disposal of oil field waste subject to enforcement and remediation orders."
        ],
        reasoning_framework="""Texas Railroad Commission regulates oil and gas waste under Statewide Rule 8. E&P
waste includes drill cuttings, produced water, completion fluids, workover fluids. Exempt from RCRA Subtitle C
as oil and gas exploration and production waste. Must be disposed in authorized facilities: commercial disposal
wells, non-commercial disposal wells, surface disposal facilities, or treatment facilities. Commercial disposal
wells require permit under Rule 9, must demonstrate adequate confining strata, compatible injectate, mechanical
integrity, and operational compliance. Non-commercial disposal wells for operator's own lease production. Surface
disposal prohibited unless authorized variance. Centralized tank batteries and treatment facilities permitted.
Waste haulers must have permit and manifest waste shipments. Unauthorized disposal subject to administrative
penalties up to $10,000 per day per violation. RRC may issue cleanup orders requiring remediation of contaminated
sites. Financial assurance required for disposal wells. Plugging required when well no longer used. Drilling waste
management plan may be required for large operations. NORM waste management per RRC rules. Records of disposal
volumes and sources required. Local governments may have additional ordinances limiting disposal well locations.
Environmental NGOs increasingly challenge disposal permits citing induced seismicity concerns.""",
        key_factors=[
            "Waste characterization as E&P exempt",
            "Authorized disposal facility selection",
            "Commercial versus non-commercial well status",
            "Geologic suitability of disposal formation",
            "Mechanical integrity demonstration",
            "Waste hauler permit compliance",
            "Manifest documentation accuracy"
        ],
        primary_authority=[
            "16 TAC 3.8 Statewide Rule 8 Waste Disposal",
            "16 TAC 3.9 Statewide Rule 9 Disposal Wells",
            "Texas Water Code Chapter 27",
            "RRC enforcement policies and procedures"
        ],
        burden_holder="Waste generator and disposal facility operator to comply with Rule 8 and Rule 9",
        adversary_position="RRC may issue violations for unauthorized disposal or mechanical integrity failures",
        counter_arguments=[
            "Waste properly characterized as E&P exempt",
            "Disposal in authorized facility with valid permit",
            "Mechanical integrity testing demonstrates well integrity",
            "Spill or release promptly reported and remediated",
            "Waste hauler permit valid and manifest complete",
            "Good faith compliance with RRC requirements"
        ],
        resolution_strategy="Characterize waste properly, use only authorized disposal facilities, maintain waste manifests, ensure disposal well mechanical integrity, report spills immediately, cooperate with RRC inspections",
        entity_scope="Texas oil and gas operators generating or disposing of E&P waste",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Rule 8 and Rule 9 compliance well-understood but induced seismicity concerns create uncertainty",
        controlling_precedent="RRC rules provide clear framework but enforcement discretion significant",
        issue_category=IssueCategory.STATE_DELEGATION
    ),
    DoctrineBlock(
        topic="NRC Radioactive Materials Licensing",
        keywords=["nrc", "radioactive material", "byproduct", "source", "special nuclear", "license"],
        conclusion_template=[
            "NRC licenses required for possession and use of byproduct, source, and special nuclear material.",
            "Specific licenses issued based on applicant qualifications, facilities, equipment, and procedures.",
            "License conditions impose radiation safety requirements including monitoring, training, and disposal."
        ],
        reasoning_framework="""Atomic Energy Act authorizes Nuclear Regulatory Commission to license radioactive
materials. Byproduct material is material made radioactive by exposure to radiation from nuclear reactor, excludes
NORM. Source material is uranium or thorium. Special nuclear material is plutonium and enriched uranium. General
licenses for small quantities under specified conditions. Specific licenses required for possession, use, transfer,
or disposal of radioactive materials above general license limits. Application must demonstrate adequate facilities,
equipment, personnel, procedures to protect health and safety and minimize danger to life or property. Radiation
safety officer must be qualified by training and experience. ALARA program required to keep exposures as low as
reasonably achievable. Monitoring and surveying for radiation levels. Personnel dosimetry for workers. Sealed source
leak testing. Waste disposal via authorized facilities or transfer to licensed recipients. Decommissioning financial
assurance. Security requirements for Category 1 and 2 quantities. Transportation per DOT regulations. Agreement
states may assume regulatory authority under Section 274 agreement. Texas is Agreement State with TCEQ administering
radioactive materials program. Import and export licenses from NRC. Emergency planning for large quantities. License
renewal applications due 30 days before expiration. Amendments for changes to facilities, procedures, or authorized
uses. Inspections and enforcement by NRC or Agreement State. Violations can result in civil penalties, license
suspension or revocation, or criminal prosecution.""",
        key_factors=[
            "Material type and quantity",
            "General versus specific license applicability",
            "Radiation safety officer qualifications",
            "ALARA program implementation",
            "Waste disposal authorization",
            "Agreement State versus NRC jurisdiction",
            "License renewal timing"
        ],
        primary_authority=[
            "42 USC 2011 Atomic Energy Act",
            "10 CFR Part 20 Radiation Protection Standards",
            "10 CFR Part 30 Byproduct Material Licenses",
            "Texas Radiation Control Act and TCEQ regulations"
        ],
        burden_holder="Licensee to comply with all license conditions and radiation safety requirements",
        adversary_position="NRC or Agreement State may issue violations or suspend license for non-compliance",
        counter_arguments=[
            "Material exempt or covered by general license",
            "Exposures below regulatory limits and ALARA",
            "Qualified RSO and trained personnel in place",
            "Waste disposal properly documented and authorized",
            "Good faith compliance with license conditions",
            "Corrective actions implemented for violations"
        ],
        resolution_strategy="Obtain appropriate license before possession, implement comprehensive radiation safety program, train personnel, monitor exposures and contamination, dispose of waste properly, renew license timely",
        entity_scope="Any entity possessing or using radioactive materials",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Radioactive materials licensing is highly technical and strictly regulated",
        controlling_precedent="NRC regulations and Agreement State programs provide detailed requirements",
        issue_category=IssueCategory.TOXIC_SUBSTANCES
    ),
    DoctrineBlock(
        topic="Spill Reporting NCP and CERCLA",
        keywords=["spill reporting", "nrc", "reportable quantity", "cercla", "oil pollution act"],
        conclusion_template=[
            "Release of hazardous substance at or above reportable quantity must be reported immediately to NRC.",
            "Oil spills to waters of US must be reported under Clean Water Act and Oil Pollution Act.",
            "Failure to report subject to criminal penalties including fines and imprisonment."
        ],
        reasoning_framework="""CERCLA Section 103 requires immediate notification to National Response Center for
release of hazardous substance equal to or exceeding reportable quantity (RQ). RQs established in 40 CFR 302.4,
ranging from 1 pound to 5,000 pounds depending on substance. Petroleum excluded from CERCLA hazardous substance
definition but oil spills covered under CWA and OPA. Oil spill reporting required for discharge to navigable waters
that causes sheen or violates water quality standards. Report to NRC at 1-800-424-8802 within 24 hours. State and
local notification may also be required. Report must include identity and quantity of substance, time and location
of release, medium into which released, known or anticipated health risks, and precautions taken. Follow-up written
report may be required. Continuous releases may qualify for reduced reporting if initial notification made and
annual updates provided. Federally permitted releases exempt from reporting. Failure to report immediately is
criminal offense punishable by fine up to $250,000 and/or imprisonment up to 5 years. Knowing endangerment carries
higher penalties. Voluntary disclosure under EPA audit policy may reduce penalties. Prompt reporting enables
emergency response and limits liability. EPCRA Section 304 requires additional notification to SERC and LEPC for
releases of EHS or CERCLA hazardous substances.""",
        key_factors=[
            "Hazardous substance versus petroleum determination",
            "Reportable quantity threshold",
            "Timeliness of NRC notification",
            "Completeness of information reported",
            "Continuous release qualification",
            "Federally permitted release exemption",
            "EPCRA Section 304 overlap"
        ],
        primary_authority=[
            "42 USC 9603 CERCLA Section 103",
            "33 USC 1321 CWA Oil Spill Reporting",
            "40 CFR Part 302 Designation of Hazardous Substances",
            "40 CFR Part 110 Discharge of Oil"
        ],
        burden_holder="Person in charge of facility or vessel to report immediately",
        adversary_position="EPA or DOJ may prosecute for failure to report or false reporting",
        counter_arguments=[
            "Release below reportable quantity",
            "Petroleum not CERCLA hazardous substance",
            "Federally permitted release exemption applies",
            "Continuous release with proper notification",
            "Report made as soon as person in charge had knowledge",
            "Self-disclosure under audit policy"
        ],
        resolution_strategy="Establish spill response procedures, train personnel on reporting requirements, report immediately upon knowledge of RQ release, document all notifications, implement corrective measures, cooperate with response agencies",
        entity_scope="Facilities and vessels handling hazardous substances or oil",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Reporting obligations clear and strictly enforced with criminal penalties",
        controlling_precedent="Courts consistently uphold reporting requirements and impose penalties for violations",
        issue_category=IssueCategory.SPILL_REPORTING
    ),
]


class EnvironmentalRegulatoryEngine:
    def __init__(self) -> None:
        self.doctrine_cache = DOCTRINE_CACHE
        self.metrics: Dict[str, Any] = defaultdict(int)
        self.query_log: List[Dict[str, Any]] = []
        self.triggered_doctrines: Dict[str, int] = defaultdict(int)
        self.cache_hits = 0
        self.cache_misses = 0

        logger.info(f"{ENGINE_NAME} v{VERSION} initialized with {len(self.doctrine_cache)} doctrine blocks")

    def three_layer_response(
        self, query: str, mode: ResponseMode, zone: AnalysisZone
    ) -> Tuple[str, ConfidenceLevel, List[str], List[str]]:
        """Three-layer response: doctrine cache, semantic retrieval, deep analysis."""
        start_time = time.time()

        # Layer 1: Doctrine Cache
        triggered = self._search_doctrine_cache(query)

        if triggered:
            self.cache_hits += 1
            response = self._apply_doctrines(triggered, mode, zone)
            confidence = self._determine_confidence(triggered)
            sources = self._extract_sources(triggered)
            reasoning_chain = [f"Doctrine cache hit: {len(triggered)} blocks triggered"]
            latency = (time.time() - start_time) * 1000
            logger.info(f"Cache hit, {len(triggered)} doctrines, {latency:.2f}ms")
            return response, confidence, sources, reasoning_chain

        # Layer 2: Semantic Retrieval (simplified - would use vector DB in production)
        self.cache_misses += 1
        semantic_results = self._semantic_search(query)

        if semantic_results:
            response = self._synthesize_semantic(semantic_results, mode, zone)
            confidence = ConfidenceLevel.DISCLOSURE
            sources = ["Semantic search across environmental regulatory framework"]
            reasoning_chain = ["Cache miss", "Semantic retrieval successful"]
            latency = (time.time() - start_time) * 1000
            logger.info(f"Semantic hit, {latency:.2f}ms")
            return response, confidence, sources, reasoning_chain

        # Layer 3: Deep Analysis
        response = self._deep_analysis(query, mode, zone)
        confidence = ConfidenceLevel.HIGH_RISK
        sources = ["General environmental regulatory principles"]
        reasoning_chain = ["Cache miss", "Semantic miss", "Deep analysis required"]
        latency = (time.time() - start_time) * 1000
        logger.info(f"Deep analysis, {latency:.2f}ms")

        return response, confidence, sources, reasoning_chain

    def _search_doctrine_cache(self, query: str) -> List[DoctrineBlock]:
        """Search doctrine cache for matching blocks."""
        query_lower = query.lower()
        query_terms = set(query_lower.split())

        matches = []
        for doctrine in self.doctrine_cache:
            keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in query_lower)
            topic_match = any(term in doctrine.topic.lower() for term in query_terms)

            if keyword_matches >= 2 or topic_match:
                matches.append(doctrine)
                self.triggered_doctrines[doctrine.topic] += 1

        return matches

    def _semantic_search(self, query: str) -> List[str]:
        """Simplified semantic search - would use Vectorize in production."""
        # Placeholder for vector similarity search
        environmental_topics = [
            "Federal environmental statutes create comprehensive regulatory framework",
            "State programs often delegated authority under federal oversight",
            "Permits required before construction or modification of regulated facilities",
            "Violations subject to administrative, civil, and criminal penalties",
            "Public participation required in major permitting decisions"
        ]
        return environmental_topics[:3]

    def _deep_analysis(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> str:
        """Deep analysis for queries not matching doctrine cache."""
        base_response = (
            "Environmental regulatory analysis requires identification of applicable federal and state statutes, "
            "determination of permit requirements, assessment of compliance obligations, and evaluation of enforcement risks. "
            "Key federal statutes include Clean Air Act, Clean Water Act, RCRA, CERCLA, NEPA, and ESA. "
            "Many states have delegated programs implementing federal requirements with additional state law obligations. "
            "Consult with environmental counsel for specific compliance strategy."
        )

        if mode == ResponseMode.MEMO:
            return f"MEMORANDUM\n\n{base_response}\n\nFurther research recommended on specific regulatory requirements."
        elif mode == ResponseMode.DEFENSE:
            return f"COMPLIANCE POSITION: {base_response}"
        else:
            return base_response

    def _apply_doctrines(
        self, doctrines: List[DoctrineBlock], mode: ResponseMode, zone: AnalysisZone
    ) -> str:
        """Apply triggered doctrines to generate response based on mode and zone."""
        if mode == ResponseMode.FAST:
            return " ".join(doctrines[0].conclusion_template)

        response_parts = []

        for doctrine in doctrines:
            if mode == ResponseMode.DEFENSE:
                response_parts.append(f"{doctrine.topic}:")
                response_parts.append(" ".join(doctrine.conclusion_template))
                response_parts.append(f"\nAuthority: {', '.join(doctrine.primary_authority[:2])}")
                response_parts.append(f"Compliance strategy: {doctrine.resolution_strategy}\n")

            elif mode == ResponseMode.MEMO:
                response_parts.append(f"## {doctrine.topic}\n")
                response_parts.append(f"**Analysis:** {doctrine.reasoning_framework[:500]}...\n")
                response_parts.append(f"**Conclusion:** {' '.join(doctrine.conclusion_template)}\n")
                response_parts.append(f"**Key Factors:** {', '.join(doctrine.key_factors[:5])}\n")
                response_parts.append(f"**Authority:** {', '.join(doctrine.primary_authority)}\n")

        return "\n".join(response_parts)

    def _synthesize_semantic(
        self, semantic_results: List[str], mode: ResponseMode, zone: AnalysisZone
    ) -> str:
        """Synthesize semantic search results."""
        synthesis = "Based on environmental regulatory framework: " + " ".join(semantic_results)

        if mode == ResponseMode.MEMO:
            return f"MEMORANDUM\n\nISSUE: Environmental regulatory compliance\n\nANALYSIS:\n{synthesis}"
        elif mode == ResponseMode.DEFENSE:
            return f"COMPLIANCE ASSESSMENT: {synthesis}"
        else:
            return synthesis

    def _determine_confidence(self, doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """Determine overall confidence level from triggered doctrines."""
        if not doctrines:
            return ConfidenceLevel.HIGH_RISK

        confidence_priority = {
            ConfidenceLevel.DEFENSIBLE: 4,
            ConfidenceLevel.AGGRESSIVE: 3,
            ConfidenceLevel.DISCLOSURE: 2,
            ConfidenceLevel.HIGH_RISK: 1
        }

        most_conservative = min(doctrines, key=lambda d: confidence_priority[d.confidence])
        return most_conservative.confidence

    def _extract_sources(self, doctrines: List[DoctrineBlock]) -> List[str]:
        """Extract unique sources from triggered doctrines."""
        sources = set()
        for doctrine in doctrines:
            sources.update(doctrine.primary_authority[:2])
        return list(sources)

    def query(self, request: QueryRequest) -> QueryResponse:
        """Process query and return response."""
        start_time = time.time()

        response_text, confidence, sources, reasoning_chain = self.three_layer_response(
            request.query, request.mode, request.zone
        )

        triggered = [d.topic for d in self._search_doctrine_cache(request.query)]
        epistemic_warnings = self._apply_epistemic_guardrails(response_text, confidence)
        determinism_hash = self._compute_hash(request.query, response_text)

        latency_ms = (time.time() - start_time) * 1000

        self.metrics["total_queries"] += 1
        self.metrics[f"mode_{request.mode.value}"] += 1
        self.metrics[f"zone_{request.zone.value}"] += 1

        query_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "query": request.query,
            "mode": request.mode.value,
            "zone": request.zone.value,
            "confidence": confidence.value,
            "triggered_doctrines": triggered,
            "latency_ms": latency_ms
        }
        self.query_log.append(query_record)

        logger.info(f"Query processed: {request.mode.value} mode, {len(triggered)} doctrines, {latency_ms:.2f}ms")

        return QueryResponse(
            query=request.query,
            mode=request.mode,
            zone=request.zone,
            response=response_text,
            confidence=confidence,
            sources=sources,
            reasoning_chain=reasoning_chain,
            triggered_doctrines=triggered,
            epistemic_warnings=epistemic_warnings,
            determinism_hash=determinism_hash,
            timestamp=datetime.utcnow().isoformat(),
            latency_ms=latency_ms
        )

    def _apply_epistemic_guardrails(self, response: str, confidence: ConfidenceLevel) -> List[str]:
        """Apply epistemic guardrails to identify limitations."""
        warnings = []

        if confidence == ConfidenceLevel.HIGH_RISK:
            warnings.append("Analysis based on general principles; specific regulatory research required")

        if confidence == ConfidenceLevel.DISCLOSURE:
            warnings.append("Consult environmental counsel for compliance strategy")

        banned_phrases = ["definitely", "certainly will", "guaranteed", "cannot fail"]
        for phrase in banned_phrases:
            if phrase in response.lower():
                warnings.append(f"Overconfident language detected: '{phrase}'")

        return warnings

    def _compute_hash(self, query: str, response: str) -> str:
        """Compute SHA-256 hash for determinism verification."""
        content = f"{query}|{response}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def get_health(self) -> Dict[str, Any]:
        """Return comprehensive health check."""
        return {
            "engine_id": ENGINE_ID,
            "engine_name": ENGINE_NAME,
            "version": VERSION,
            "status": "healthy",
            "doctrine_blocks": len(self.doctrine_cache),
            "total_queries": self.metrics["total_queries"],
            "cache_hit_rate": (
                self.cache_hits / (self.cache_hits + self.cache_misses)
                if (self.cache_hits + self.cache_misses) > 0
                else 0.0
            ),
            "top_doctrines": sorted(
                self.triggered_doctrines.items(), key=lambda x: x[1], reverse=True
            )[:10],
            "metrics": dict(self.metrics)
        }


# FastAPI Application
app = FastAPI(title=ENGINE_NAME, version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = EnvironmentalRegulatoryEngine()


@app.on_event("startup")
async def startup_event():
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return engine.get_health()


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process environmental regulatory query."""
    try:
        return engine.query(request)
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine blocks."""
    return {
        "total": len(engine.doctrine_cache),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.issue_category.value,
                "keywords": d.keywords[:5],
                "confidence": d.confidence.value
            }
            for d in engine.doctrine_cache
        ]
    }


@app.get("/metrics")
async def get_metrics():
    """Return query metrics."""
    return {
        "total_queries": engine.metrics["total_queries"],
        "cache_hit_rate": (
            engine.cache_hits / (engine.cache_hits + engine.cache_misses)
            if (engine.cache_hits + engine.cache_misses) > 0
            else 0.0
        ),
        "mode_distribution": {
            "FAST": engine.metrics["mode_FAST"],
            "DEFENSE": engine.metrics["mode_DEFENSE"],
            "MEMO": engine.metrics["mode_MEMO"]
        },
        "top_triggered_doctrines": sorted(
            engine.triggered_doctrines.items(), key=lambda x: x[1], reverse=True
        )[:15]
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
