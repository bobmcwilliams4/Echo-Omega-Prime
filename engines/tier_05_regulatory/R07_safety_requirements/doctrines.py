"""R07 SAFETY REQUIREMENTS DOCTRINE CACHE
Safety compliance doctrines for oil & gas operations.
Topics: OSHA, H2S, BOP, PSM, RMP, well control, confined space, fall protection
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class ConfidenceStratification(str, Enum):
    MANDATORY = "mandatory"
    CLEARLY_REQUIRED = "clearly_required"
    BEST_PRACTICE = "best_practice"

@dataclass
class DoctrineBlock:
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

OSHA_1910_HAZCOM = DoctrineBlock(
    topic="OSHA Hazard Communication Standard (1910.1200)",
    keywords=["hazcom", "hazard communication", "sds", "safety data sheets", "ghs", "chemical labeling"],
    conclusion_template="Oil and gas operations using hazardous chemicals must comply with OSHA Hazard Communication Standard (29 CFR 1910.1200), including SDS maintenance, chemical labeling, and employee training.",
    reasoning_framework="29 CFR 1910.1200 requires written hazard communication program, SDS for all hazardous chemicals, GHS-compliant labels, employee training on chemical hazards. Common O&G chemicals: H2S, benzene, diesel, solvents, treating chemicals, hydraulic fracturing additives. Requirements: maintain SDS library accessible to employees, label all chemical containers with GHS pictograms and hazard statements, train employees on chemical hazards and protective measures. Violations: $15,653 per serious violation, $156,529 for willful violations.",
    key_factors=["Written HazCom program required", "SDS for all hazardous chemicals", "GHS-compliant labels on containers", "Employee training on chemical hazards", "Violations: $15,653 serious, $156,529 willful"],
    primary_authority=["29 CFR §1910.1200 (HazCom)", "GHS Rev 7"],
    burden_holder="Employer",
    adversary_position="OSHA",
    counter_arguments=["Inadequate SDS library triggers violations", "Lack of employee training is common citation"],
    resolution_strategy="Maintain current SDS library, label all containers, conduct annual HazCom training, document training",
    entity_scope=["operator", "employer"],
    confidence=0.96,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="29 CFR §1910.1200"
)

H2S_SAFETY = DoctrineBlock(
    topic="H2S Safety (ANSI Z390.1)",
    keywords=["h2s", "hydrogen sulfide", "sour gas", "h2s monitor", "scba", "wind sock"],
    conclusion_template="Operations in H2S environments require compliance with ANSI Z390.1 and OSHA standards, including atmospheric monitoring, respiratory protection, emergency procedures, and employee training.",
    reasoning_framework="H2S (hydrogen sulfide) is toxic gas common in oil/gas operations. Lethal at >100 ppm. ANSI Z390.1 provides industry standard. Requirements: atmospheric monitoring (continuous or periodic based on H2S concentration), respiratory protection (SCBA for >20 ppm H2S or unknown atmospheres), wind socks at wellsite to indicate escape direction, H2S safety training for all personnel, emergency action plan, buddy system, communication protocols. OSHA: 10 ppm 8-hour TWA PEL, 15 ppm STEL (15 min). Violations: OSHA general duty clause §5(a)(1) for H2S fatalities (can be $156,529+ per willful violation). Common H2S sources: Permian Basin Wolfcamp, Eagle Ford, certain Gulf Coast zones.",
    key_factors=["ANSI Z390.1 industry standard", "OSHA PEL: 10 ppm TWA, 15 ppm STEL", "Continuous monitoring for H2S >20 ppm", "SCBA required for >20 ppm or unknown", "Wind socks, buddy system, emergency plan required", "H2S training for all personnel", "Violations: up to $156,529 willful"],
    primary_authority=["ANSI Z390.1 (H2S Safety)", "29 CFR §1910.134 (Respiratory Protection)", "29 CFR §1910.146 (Confined Spaces)"],
    burden_holder="Employer/Operator",
    adversary_position="OSHA",
    counter_arguments=["H2S fatalities trigger severe penalties and criminal investigation", "Inadequate monitoring is common cause of fatalities"],
    resolution_strategy="Implement ANSI Z390.1 program, provide continuous monitoring and SCBA, train all personnel, enforce buddy system",
    entity_scope=["operator", "employer"],
    confidence=0.94,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="ANSI Z390.1"
)

BOP_REQUIREMENTS = DoctrineBlock(
    topic="BOP Equipment and Testing (API Spec 53 / BSEE)",
    keywords=["bop", "blowout preventer", "bop test", "well control", "kicks", "pressure test"],
    conclusion_template="Blowout preventers (BOPs) must meet API Spec 53 standards and undergo regular pressure testing. BSEE regulations apply to offshore operations. Failure to maintain functional BOP equipment can result in well control incidents, shut-in orders, and severe penalties.",
    reasoning_framework="BOP is primary well control device preventing blowouts. API Spec 53 specifies design, testing, maintenance. Requirements: pressure test BOP stack before drilling, function test rams and annular preventers, inspect and maintain per manufacturer specifications, document all tests and maintenance. BSEE offshore: BOP systems inspected every 14 days, full function test every 21 days, pressure test after significant repairs. Onshore Texas: RRC does not mandate BOP testing frequency, but API RP 53 recommends testing before each well. Well control incidents due to BOP failure: Macondo blowout ($65 billion liability), numerous smaller incidents. Penalties: BSEE can assess $46,000/day per violation, RRC shut-in orders for equipment failures.",
    key_factors=["API Spec 53 design and testing standards", "Pressure test BOP stack before drilling", "Function test rams and annular preventers", "BSEE offshore: inspect every 14 days, function test every 21 days", "Document all tests and maintenance", "Penalties: $46,000/day BSEE, shut-in orders RRC", "BOP failure can cause catastrophic blowouts"],
    primary_authority=["API Spec 53 (BOP)", "API RP 53 (BOP Testing)", "30 CFR §250 (BSEE Offshore)", "16 TAC §3 (Texas Onshore)"],
    burden_holder="Operator/Drilling Contractor",
    adversary_position="BSEE, Railroad Commission",
    counter_arguments=["BOP equipment failure triggers shut-in and investigation", "Blowout liability can be catastrophic (see Macondo)"],
    resolution_strategy="Follow API RP 53 testing protocols, maintain detailed test records, inspect BOP regularly, train crews on BOP operation",
    entity_scope=["operator", "drilling_contractor"],
    confidence=0.93,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="API Spec 53"
)

PSM_PROCESS_SAFETY = DoctrineBlock(
    topic="Process Safety Management (29 CFR 1910.119)",
    keywords=["psm", "process safety management", "pha", "process hazard analysis", "hot work", "management of change"],
    conclusion_template="Oil and gas facilities with processes involving >10,000 lbs of flammable liquids or gases must implement OSHA Process Safety Management (PSM) program, including process hazard analyses, mechanical integrity, management of change, and incident investigation.",
    reasoning_framework="29 CFR 1910.119 PSM applies to facilities with threshold quantities of highly hazardous chemicals. Common O&G triggers: >10,000 lbs flammable gas (natural gas processing, compression), >10,000 lbs H2S. PSM elements (14 total): process safety information, process hazard analysis (PHA), operating procedures, training, contractors, pre-startup safety review, mechanical integrity, hot work permits, management of change, incident investigation, emergency planning, compliance audits, trade secrets. PHA required every 5 years. Mechanical integrity for critical equipment (compressors, vessels, piping). Violations: PSM violations average $15,000-50,000 per element, willful violations up to $156,529. Major incidents (Texas City refinery, Williams Geismar) resulted from PSM failures.",
    key_factors=["Applies to facilities >10,000 lbs flammable or H2S", "14 PSM elements required", "Process Hazard Analysis (PHA) every 5 years", "Mechanical integrity program for critical equipment", "Management of change (MOC) for process modifications", "Compliance audits every 3 years", "Violations: $15-50K per element, $156K willful"],
    primary_authority=["29 CFR §1910.119 (PSM)", "EPA RMP 40 CFR Part 68"],
    burden_holder="Facility owner/operator",
    adversary_position="OSHA, EPA",
    counter_arguments=["PSM violations are expensive and common in O&G", "MOC failures cause many incidents"],
    resolution_strategy="Implement full 14-element PSM program, conduct PHA every 5 years, document MOC, maintain mechanical integrity, audit every 3 years",
    entity_scope=["facility_owner", "operator"],
    confidence=0.92,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="29 CFR §1910.119"
)

CONFINED_SPACE = DoctrineBlock(
    topic="Confined Space Entry (29 CFR 1910.146)",
    keywords=["confined space", "permit required", "atmospheric testing", "ventilation", "attendant", "retrieval"],
    conclusion_template="Entry into permit-required confined spaces (tanks, vessels, pits) must comply with OSHA 1910.146, including atmospheric testing, continuous ventilation, entry permits, attendants, and retrieval equipment.",
    reasoning_framework="29 CFR 1910.146 regulates permit-required confined spaces: limited entry/exit, not designed for continuous occupancy, hazardous atmosphere potential. Common O&G confined spaces: storage tanks, separators, treaters, pits, sumps. Requirements: identify and label all confined spaces, atmospheric testing before and during entry (oxygen 19.5-23.5%, flammable <10% LEL, H2S <10 ppm, CO <35 ppm), entry permit system, attendant stationed outside, communication between entrant and attendant, ventilation (continuous if possible), retrieval equipment (tripod, winch, harness), rescue plan. Violations: confined space fatalities are common in O&G (tank cleaning, maintenance), OSHA issues $156,529 willful violations for fatalities. Atmospheric hazards: oxygen deficiency (displacement by hydrocarbons), H2S, benzene vapors.",
    key_factors=["Identify and label all permit-required confined spaces", "Atmospheric testing: O2 19.5-23.5%, flammable <10% LEL, H2S <10 ppm", "Entry permit required with authorized supervisor signature", "Attendant stationed outside during entry", "Continuous ventilation when possible", "Retrieval equipment (tripod/winch/harness)", "Rescue plan and trained rescue team", "Violations: $156,529 for fatalities"],
    primary_authority=["29 CFR §1910.146 (Confined Spaces)"],
    burden_holder="Employer",
    adversary_position="OSHA",
    counter_arguments=["Confined space fatalities are leading cause of O&G worker deaths", "Inadequate atmospheric testing is common cause"],
    resolution_strategy="Implement confined space program, atmospheric testing before EVERY entry, maintain entry permits, station attendants, provide retrieval equipment",
    entity_scope=["operator", "employer"],
    confidence=0.95,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="29 CFR §1910.146"
)

FALL_PROTECTION = DoctrineBlock(
    topic="Fall Protection (29 CFR 1910.28 / 1926.501)",
    keywords=["fall protection", "guardrails", "fall arrest", "safety harness", "anchorage", "working at heights"],
    conclusion_template="Oil and gas operations involving work at heights >4 feet (general industry) or >6 feet (construction) require fall protection systems including guardrails, safety nets, or personal fall arrest systems.",
    reasoning_framework="29 CFR 1910.28 (general industry) and 1926.501 (construction) require fall protection. Common O&G scenarios: derricks/masts, tank gauging, platform work, scaffolding, ladder climbing. Protection methods: (1) guardrail systems (preferred), (2) safety nets, (3) personal fall arrest systems (harness + lanyard + anchorage). Fall arrest requirements: anchorage capable of 5,000 lbs per worker, full-body harness (not belt), shock-absorbing lanyard or self-retracting lifeline, tie-off at all times when >6 feet. Ladder climbing: fixed ladders >24 feet require ladder safety system or personal fall arrest. Violations: fall protection is #1 OSHA citation, $15,653 per serious violation. O&G fall fatalities: derrick/rig falls, tank falls during gauging, platform falls.",
    key_factors=["Fall protection required >4 feet (general) or >6 feet (construction)", "Guardrails preferred, fall arrest as alternative", "Anchorage: 5,000 lbs per worker", "Full-body harness + shock-absorbing lanyard", "Fixed ladders >24 feet need ladder safety system", "Violations: $15,653 per serious, #1 OSHA citation", "Common O&G falls: derricks, tanks, platforms"],
    primary_authority=["29 CFR §1910.28 (Fall Protection - General Industry)", "29 CFR §1926.501 (Fall Protection - Construction)"],
    burden_holder="Employer",
    adversary_position="OSHA",
    counter_arguments=["Fall protection is most cited OSHA violation", "Falls are leading cause of construction fatalities"],
    resolution_strategy="Install guardrails where feasible, provide personal fall arrest systems, train workers on fall protection, inspect equipment regularly",
    entity_scope=["operator", "employer", "contractor"],
    confidence=0.94,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="29 CFR §1910.28"
)

DOCTRINE_CACHE = [OSHA_1910_HAZCOM, H2S_SAFETY, BOP_REQUIREMENTS, PSM_PROCESS_SAFETY, CONFINED_SPACE, FALL_PROTECTION]

def match_doctrines(query_text: str, keywords: List[str]) -> List[DoctrineBlock]:
    query_lower = query_text.lower()
    keyword_set = set(k.lower() for k in keywords)
    matches = []
    for doctrine in DOCTRINE_CACHE:
        doctrine_keywords = set(k.lower() for k in doctrine.keywords)
        overlap = len(keyword_set & doctrine_keywords)
        text_matches = sum(1 for dk in doctrine.keywords if dk.lower() in query_lower)
        total_score = overlap + text_matches
        if total_score > 0: matches.append((total_score, doctrine))
    matches.sort(key=lambda x: x[0], reverse=True)
    return [doctrine for score, doctrine in matches]
