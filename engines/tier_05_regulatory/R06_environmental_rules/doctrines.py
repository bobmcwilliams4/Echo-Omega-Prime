"""
R06 ENVIRONMENTAL RULES DOCTRINE CACHE
Environmental compliance doctrines for oil & gas operations.
Topics: TCEQ, EPA, RCRA, CWA, CAA, SPCC, stormwater, produced water, NORM
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class ConfidenceStratification(str, Enum):
    MANDATORY = "mandatory"
    CLEARLY_REQUIRED = "clearly_required"
    BEST_PRACTICE = "best_practice"
    UNCERTAIN = "uncertain"

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

# TCEQ REGULATIONS

TCEQ_AIR_PERMIT = DoctrineBlock(
    topic="TCEQ Air Permits (NSR/PSD)",
    keywords=["air permit", "tceq air", "nsr", "psd", "new source review", "prevention of significant deterioration"],
    conclusion_template="Texas oil and gas facilities emitting significant air pollutants must obtain TCEQ air permits under New Source Review (NSR) or Prevention of Significant Deterioration (PSD) programs. Permit required before construction or modification.",
    reasoning_framework="30 TAC §116 requires air permits for new or modified sources exceeding emission thresholds. NSR thresholds (attainment areas): 25 tons/year VOC, 100 tons/year NOx for oil/gas production. PSD (near-attainment): 250 tons/year. Compressor engines, glycol dehydrators, storage tanks, flares trigger review. Permit application must include air dispersion modeling, BACT analysis, public notice. Processing time: 330 days standard, 18-24 months for complex PSD permits. Unauthorized construction penalties: $25,000/day, forced shutdown.",
    key_factors=["Thresholds: 25 tpy VOC, 100 tpy NOx (NSR)", "250 tpy major source (PSD)", "Required before construction/modification", "Application includes modeling and BACT", "Penalties: $25,000/day for unauthorized construction", "Processing: 330 days NSR, 18-24 months PSD"],
    primary_authority=["30 TAC §116 (TCEQ Air Permits)", "Clean Air Act §165 (PSD)", "40 CFR Part 52 (NSR)"],
    burden_holder="Facility owner/operator",
    adversary_position="TCEQ Air Permits Division, EPA",
    counter_arguments=["Unauthorized construction triggers daily penalties", "Forced shutdown until permit obtained", "Air modeling can be expensive and time-consuming"],
    resolution_strategy="Obtain air permit before construction, model emissions accurately, implement BACT, maintain emission records",
    entity_scope=["operator", "facility_owner"],
    confidence=0.93,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="30 TAC §116"
)

SPCC_PLAN = DoctrineBlock(
    topic="SPCC Plans (40 CFR 112)",
    keywords=["spcc", "spill prevention", "oil spill", "spcc plan", "secondary containment"],
    conclusion_template="Facilities with >1,320 gallons aggregate aboveground oil storage (or >42,000 gallons total) must prepare and implement Spill Prevention, Control, and Countermeasure (SPCC) plans under EPA regulations.",
    reasoning_framework="40 CFR 112 requires SPCC plans for facilities storing oil (includes crude, diesel, lube oil) above capacity thresholds. Thresholds: >1,320 gallons aggregate aboveground capacity OR >42,000 gallons total capacity (including underground). Plan must be prepared by Professional Engineer, updated every 5 years or after facility changes. Requirements: secondary containment for tanks, loading areas, piping; drainage control; inspections; personnel training; discharge response procedures. Violations: $25,000/day civil penalties, $50,000/day criminal for knowing violations, spill cleanup liability under OPA 90.",
    key_factors=["Threshold: >1,320 gal aboveground or >42,000 gal total", "PE-certified plan required", "Update every 5 years or after changes", "Secondary containment for tanks and loading areas", "Penalties: $25,000-50,000/day", "Spill cleanup liability under OPA 90"],
    primary_authority=["40 CFR Part 112 (SPCC)", "Clean Water Act §311", "Oil Pollution Act 1990"],
    burden_holder="Facility owner/operator",
    adversary_position="EPA, TCEQ",
    counter_arguments=["Inadequate secondary containment triggers violations", "Spill cleanup costs can exceed millions", "PE certification adds cost and complexity"],
    resolution_strategy="Calculate oil storage capacity, prepare PE-certified SPCC plan, install secondary containment, train personnel, inspect regularly",
    entity_scope=["operator", "facility_owner"],
    confidence=0.95,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="40 CFR Part 112"
)

PRODUCED_WATER_MANAGEMENT = DoctrineBlock(
    topic="Produced Water Management",
    keywords=["produced water", "disposal well", "injection well", "salt water disposal", "swd", "class ii well"],
    conclusion_template="Produced water from oil and gas operations must be managed through permitted disposal wells, beneficial reuse, or surface discharge under strict permit conditions. Unpermitted disposal prohibited.",
    reasoning_framework="16 TAC §3.8 and EPA UIC Class II program regulate produced water disposal. Disposal options: (1) Class II injection well (most common) requiring RRC and EPA permits, (2) beneficial reuse under 30 TAC §312 (road dust control, drilling fluids, enhanced recovery), (3) surface discharge under TPDES permit (rare, requires stringent treatment). Unpermitted disposal (surface dumping, unlined pits) is illegal - $25,000/day penalties plus remediation. Disposal well requirements: mechanical integrity tests every 5 years, monthly injection volume reporting, pressure monitoring. NORM (naturally occurring radioactive material) in produced water requires special handling under 25 TAC §289.",
    key_factors=["Three legal disposal options: injection well, beneficial reuse, TPDES discharge", "Injection wells require RRC/EPA permits", "MIT required every 5 years", "Beneficial reuse requires 30 TAC §312 authorization", "Unpermitted disposal: $25,000/day penalties", "NORM handling requirements apply"],
    primary_authority=["16 TAC §3.8 (Disposal Wells)", "30 TAC §312 (Beneficial Reuse)", "40 CFR Part 144 (UIC Class II)", "25 TAC §289 (NORM)"],
    burden_holder="Operator",
    adversary_position="Railroad Commission, TCEQ, EPA",
    counter_arguments=["Disposal well permitting takes 6-12 months", "Surface disposal extremely difficult to permit", "NORM contamination triggers expensive remediation"],
    resolution_strategy="Obtain disposal well permits, file monthly injection reports, conduct MIT every 5 years, explore beneficial reuse opportunities",
    entity_scope=["operator", "disposal_operator"],
    confidence=0.94,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="16 TAC §3.8"
)

STORMWATER_PERMIT = DoctrineBlock(
    topic="Stormwater Permits (TXR05)",
    keywords=["stormwater", "txr05", "npdes", "stormwater permit", "construction stormwater"],
    conclusion_template="Oil and gas facilities with stormwater discharges from industrial activity must obtain TCEQ Multi-Sector General Permit (MSGP) TXR05. Construction activities >1 acre require separate construction stormwater permit.",
    reasoning_framework="Clean Water Act §402 and 30 TAC §213 require stormwater permits for industrial facilities. TXR05 MSGP covers oil/gas extraction (Sector J). Requirements: Notice of Intent (NOI) filing, Stormwater Pollution Prevention Plan (SWPPP), implementation of Best Management Practices (BMPs), quarterly visual inspections, annual reporting. Construction activities disturbing >1 acre require separate TXR15 Construction General Permit with erosion/sedimentation controls. Violations: $25,000/day for unpermitted discharges, $10,000/day for reporting violations. SWPPP must address: good housekeeping, preventive maintenance, spill prevention, sediment control, vehicle tracking, waste management.",
    key_factors=["TXR05 MSGP required for industrial stormwater", "NOI filing and SWPPP required", "BMPs: good housekeeping, spill prevention, sediment control", "Quarterly visual inspections, annual reports", "Construction >1 acre needs TXR15 permit", "Penalties: $25,000/day unpermitted discharge"],
    primary_authority=["30 TAC §213 (Stormwater)", "Clean Water Act §402", "TXR05 MSGP", "TXR15 CGP"],
    burden_holder="Facility owner/operator",
    adversary_position="TCEQ, EPA",
    counter_arguments=["Unpermitted discharge triggers daily penalties", "SWPPP inadequacy can result in violations", "Inspections must be documented and retained"],
    resolution_strategy="File NOI for TXR05, prepare SWPPP, implement BMPs, conduct quarterly inspections, file annual reports",
    entity_scope=["operator", "facility_owner"],
    confidence=0.91,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="30 TAC §213"
)

PIT_CLOSURE = DoctrineBlock(
    topic="Pit Closure Requirements",
    keywords=["pit closure", "reserve pit", "drilling pit", "pit remediation", "pit closure plan"],
    conclusion_template="Oil and gas reserve pits and other earthen pits must be closed within specified timeframes using RRC-approved methods. Commercial pits require more stringent closure with financial assurance.",
    reasoning_framework="16 TAC §3.8 requires closure of pits used for drilling fluids, produced water, or other E&P wastes. Closure timeline: reserve pits (drilling fluids) within 1 year of well completion; emergency pits within 90 days. Closure methods: (1) remove fluids to permitted disposal, (2) dewater solids to <20% free liquids, (3) solidify if necessary, (4) backfill and restore surface. Soil sampling required to demonstrate no contamination above TCEQ Protective Concentration Levels (PCLs). Commercial pits: require separate permit, financial assurance, groundwater monitoring, closure plan approval. Violations: $10,000/day for failure to close timely, responsible party remains liable until closure approved.",
    key_factors=["Reserve pits: close within 1 year of completion", "Emergency pits: close within 90 days", "Closure: dewater to <20% liquids, backfill, restore", "Soil sampling to demonstrate no contamination", "Commercial pits require permit and financial assurance", "Penalties: $10,000/day for late closure"],
    primary_authority=["16 TAC §3.8 (Pit Closure)", "30 TAC §350 (Contaminated Sites)", "TCEQ PCLs"],
    burden_holder="Operator",
    adversary_position="Railroad Commission, TCEQ",
    counter_arguments=["Soil contamination requires expensive remediation", "Closure approval can take months", "Financial assurance ties up capital for commercial pits"],
    resolution_strategy="Close pits within required timelines, dewater properly, sample soil, restore surface, document closure",
    entity_scope=["operator"],
    confidence=0.90,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="16 TAC §3.8"
)

ENDANGERED_SPECIES = DoctrineBlock(
    topic="Endangered Species Compliance (ESA)",
    keywords=["endangered species", "esa", "section 7", "biological opinion", "incidental take", "habitat"],
    conclusion_template="Oil and gas operations in habitat of federally listed endangered or threatened species must comply with Endangered Species Act requirements, including consultation with U.S. Fish and Wildlife Service (USFWS) for potential 'take' of protected species.",
    reasoning_framework="Endangered Species Act §7 and §9 prohibit 'take' (harm, harass, kill) of listed species without authorization. Federal nexus (BLM permit, Corps 404 permit, FWS land) triggers formal §7 consultation. Private land operations may still violate §9 if take occurs. Protected species in Texas oil/gas areas: dunes sagebrush lizard (Permian Basin), lesser prairie chicken (Panhandle), whooping crane (coastal), Texas hornshell mussel (rivers). Compliance paths: (1) avoid habitat, (2) obtain Incidental Take Permit (ITP) under §10, (3) participate in Candidate Conservation Agreement with Assurances (CCAA), (4) obtain Biological Opinion through federal agency consultation. Violations: $50,000 civil penalty per violation, criminal penalties up to $50,000 and 1 year imprisonment, injunctive relief forcing project shutdown.",
    key_factors=["ESA prohibits 'take' of listed species", "Federal nexus triggers §7 consultation", "Protected species in TX: dunes sagebrush lizard, lesser prairie chicken, whooping crane", "Compliance: avoid habitat, obtain ITP, participate in CCAA", "Violations: $50,000 civil, criminal penalties, injunctions", "Biological Opinion process can take 135+ days"],
    primary_authority=["Endangered Species Act §7, §9, §10", "50 CFR Part 17 (Listed Species)", "USFWS Biological Opinions"],
    burden_holder="Project proponent",
    adversary_position="USFWS, environmental groups",
    counter_arguments=["Project injunctions can occur mid-construction", "ITP process is lengthy and expensive", "Habitat avoidance may be impractical in some areas"],
    resolution_strategy="Survey for listed species before operations, consult with USFWS early, participate in CCAs/CCAAs, design operations to avoid habitat",
    entity_scope=["operator", "project_proponent"],
    confidence=0.87,
    confidence_stratification=ConfidenceStratification.CLEARLY_REQUIRED,
    controlling_precedent="Endangered Species Act §7, §9"
)

NORM_HANDLING = DoctrineBlock(
    topic="NORM (Naturally Occurring Radioactive Material)",
    keywords=["norm", "radioactive", "tenorm", "radioactive scale", "radioactive waste", "naturally occurring"],
    conclusion_template="Oil and gas equipment and waste contaminated with Naturally Occurring Radioactive Material (NORM) must be handled, stored, and disposed of in accordance with Texas Department of State Health Services regulations (25 TAC §289).",
    reasoning_framework="NORM accumulates in scales, sludges, and equipment from production operations, especially high-salinity formations. Radium-226, Radium-228, Lead-210 are primary isotopes. 25 TAC §289.252 regulates NORM in oil/gas operations. Requirements: survey equipment for NORM contamination before maintenance/disposal, license required to possess/dispose of NORM >5,000 pCi/g Radium-226 or >50 pCi/g Radium-228, NORM-contaminated equipment must be decontaminated or disposed at licensed facility, worker radiation safety training and monitoring required if exposure potential, transportation under DOT radioactive materials rules. Disposal options: decontamination to below exemption levels, disposal at licensed low-level radioactive waste facility (expensive - $100-300/cubic foot), encapsulation and burial at approved site. Violations: $25,000/day for unlicensed NORM possession, improper disposal triggers CERCLA Superfund liability.",
    key_factors=["NORM thresholds: >5,000 pCi/g Ra-226 or >50 pCi/g Ra-228 requires license", "Survey equipment before maintenance/disposal", "Licensed disposal at LLRW facility ($100-300/cf)", "Worker training and monitoring if exposure potential", "DOT rules for NORM transportation", "Violations: $25,000/day, CERCLA liability"],
    primary_authority=["25 TAC §289.252 (NORM)", "DOT 49 CFR Part 173 (Radioactive Materials)", "CERCLA (Superfund)"],
    burden_holder="Operator/equipment owner",
    adversary_position="Texas DSHS, EPA, DOT",
    counter_arguments=["NORM disposal is expensive", "Unlicensed NORM possession triggers penalties", "Superfund liability can be enormous"],
    resolution_strategy="Survey equipment for NORM, obtain license if needed, decontaminate or dispose at licensed facility, train workers",
    entity_scope=["operator"],
    confidence=0.89,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="25 TAC §289.252"
)

WETLANDS_SECTION_404 = DoctrineBlock(
    topic="Wetlands Permits (CWA Section 404)",
    keywords=["wetlands", "section 404", "404 permit", "waters of the us", "wotus", "corps permit", "jurisdictional determination"],
    conclusion_template="Oil and gas operations involving dredge or fill in wetlands or other waters of the United States require permits from U.S. Army Corps of Engineers under Clean Water Act Section 404. Unauthorized impacts subject to enforcement and restoration orders.",
    reasoning_framework="Clean Water Act §404 prohibits discharge of dredged or fill material into waters of the U.S. (including wetlands) without Corps permit. Nationwide Permit 12 (NWP 12) covers oil/gas pipeline and access road construction with certain conditions (<0.5 acre impact per crossing, pre-construction notification for >300 linear feet). Individual permits required for larger impacts (months to years processing). Jurisdictional determination (JD) from Corps identifies regulated waters on site. Compensatory mitigation required for >0.1 acre permanent wetland impacts (purchase mitigation credits or permittee-responsible mitigation). Texas Coastal Management Program adds layer for coastal zone activities. Violations: cease and desist orders, $25,000-50,000/day penalties, restoration orders requiring removal of fill and wetland restoration (expensive).",
    key_factors=["Section 404 permit required for dredge/fill in wetlands/WOTUS", "NWP 12 covers pipelines/roads <0.5 acre impact", "Individual permits for larger impacts", "Compensatory mitigation >0.1 acre permanent impact", "Violations: cease/desist, $25-50K/day, restoration orders", "JD from Corps determines jurisdictional waters"],
    primary_authority=["Clean Water Act §404", "33 CFR Part 323 (Corps Permits)", "NWP 12"],
    burden_holder="Project proponent",
    adversary_position="U.S. Army Corps of Engineers, EPA",
    counter_arguments=["Restoration orders are extremely expensive", "Individual permit process takes 2+ years", "Mitigation credit costs vary widely"],
    resolution_strategy="Obtain JD early, minimize wetland impacts, use NWP 12 where possible, file PCN timely, purchase mitigation credits as needed",
    entity_scope=["operator", "pipeline_company"],
    confidence=0.92,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="Clean Water Act §404"
)

DOCTRINE_CACHE = [
    TCEQ_AIR_PERMIT,
    SPCC_PLAN,
    PRODUCED_WATER_MANAGEMENT,
    STORMWATER_PERMIT,
    PIT_CLOSURE,
    ENDANGERED_SPECIES,
    NORM_HANDLING,
    WETLANDS_SECTION_404
]

def match_doctrines(query_text: str, keywords: List[str]) -> List[DoctrineBlock]:
    query_lower = query_text.lower()
    keyword_set = set(k.lower() for k in keywords)
    matches = []
    for doctrine in DOCTRINE_CACHE:
        doctrine_keywords = set(k.lower() for k in doctrine.keywords)
        overlap = len(keyword_set & doctrine_keywords)
        text_matches = sum(1 for dk in doctrine.keywords if dk.lower() in query_lower)
        total_score = overlap + text_matches
        if total_score > 0:
            matches.append((total_score, doctrine))
    matches.sort(key=lambda x: x[0], reverse=True)
    return [doctrine for score, doctrine in matches]
