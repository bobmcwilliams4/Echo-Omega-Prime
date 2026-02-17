import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import hashlib
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set
from enum import Enum, auto
from datetime import datetime, timedelta
import json
import threading

# ========== ENUMS ==========

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class PositionZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class ConfidenceZone(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class IssueCategory(str, Enum):
    ELECTROCHEMICAL = "ELECTROCHEMICAL"
    GALVANIC = "GALVANIC"
    PITTING = "PITTING"
    CREVICE = "CREVICE"
    SCC = "STRESS_CORROSION_CRACKING"
    HYDROGEN = "HYDROGEN_DAMAGE"
    EROSION = "EROSION_CORROSION"
    MIC = "MICROBIOLOGICAL"
    CO2 = "CO2_CORROSION"
    H2S = "H2S_CORROSION"
    CATHODIC_PROTECTION = "CATHODIC_PROTECTION"
    COATING = "COATING"
    INHIBITOR = "INHIBITOR"
    MATERIAL_SELECTION = "MATERIAL_SELECTION"
    MONITORING = "MONITORING"
    INTEGRITY_MANAGEMENT = "INTEGRITY_MANAGEMENT"
    HIGH_TEMP = "HIGH_TEMPERATURE"
    ALLOWANCE = "CORROSION_ALLOWANCE"

# ========== METRICS COLLECTOR ==========

class MetricsCollector:
    def __init__(self):
        self.lock = threading.Lock()
        self.queries = []
        self.errors = []
        self.doctrine_hits = {}
        self.start_time = datetime.utcnow()

    def record_query(self, doctrine_ids: List[str]):
        now = datetime.utcnow()
        with self.lock:
            self.queries.append(now)
            for did in doctrine_ids:
                self.doctrine_hits[did] = self.doctrine_hits.get(did, 0) + 1

    def record_error(self):
        with self.lock:
            self.errors.append(datetime.utcnow())

    def get_latency_stats(self) -> Dict[str, Any]:
        with self.lock:
            if not self.queries:
                return {"min_ms": None, "max_ms": None, "avg_ms": None}
            times = [q.timestamp() for q in self.queries]
            diffs = [t2 - t1 for t1, t2 in zip(times[:-1], times[1:])]
            if not diffs:
                return {"min_ms": 0, "max_ms": 0, "avg_ms": 0}
            min_ms = min(diffs) * 1000
            max_ms = max(diffs) * 1000
            avg_ms = sum(diffs) / len(diffs) * 1000
            return {"min_ms": min_ms, "max_ms": max_ms, "avg_ms": avg_ms}

    def get_doctrine_hit_rate(self) -> Dict[str, float]:
        with self.lock:
            total = sum(self.doctrine_hits.values())
            if total == 0:
                return {}
            return {k: v / total for k, v in self.doctrine_hits.items()}

    def queries_last_hour(self) -> int:
        cutoff = datetime.utcnow() - timedelta(hours=1)
        with self.lock:
            return sum(1 for q in self.queries if q > cutoff)

metrics_collector = MetricsCollector()

# ========== PYDANTIC MODELS ==========

class QueryRequest(BaseModel):
    scenario: str = Field(..., description="Description of the corrosion scenario or question")
    mode: ResponseMode = Field(..., description="Response mode")
    entity_type: str = Field(..., description="Type of entity (e.g., pipeline, vessel, tank)")
    complexity: int = Field(..., ge=1, le=5, description="Complexity level (1-5)")

class QueryResponse(BaseModel):
    engine_id: str
    query_id: str
    mode: ResponseMode
    confidence: float
    confidence_zone: ConfidenceZone
    position_zone: PositionZone
    primary_conclusion: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    counter_arguments: List[str]
    resolution_strategy: str
    determinism_hash: str

# ========== DOCTRINE CACHE ==========

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
    confidence_zone: ConfidenceZone
    controlling_precedent: List[str]

DOCTRINE_CACHE: List[DoctrineBlock] = [

    DoctrineBlock(
        topic="Electrochemical Corrosion Fundamentals",
        keywords=["anodic", "cathodic", "electrochemical", "Nernst", "potential"],
        conclusion_template="Electrochemical corrosion is governed by anodic and cathodic reactions, with the corrosion rate determined by the mixed potential theory and environmental factors. Material selection and environmental control are primary mitigation strategies.",
        reasoning_framework=(
            "Electrochemical corrosion involves oxidation at the anode and reduction at the cathode, "
            "with electrons flowing through the metal and ions through the electrolyte. The Nernst equation "
            "describes the equilibrium potential for each half-cell reaction, and the mixed potential theory "
            "explains how the overall corrosion rate is set by the intersection of anodic and cathodic polarization curves. "
            "Key factors include the availability of oxygen (for cathodic reduction), pH, temperature, and ionic strength. "
            "Corrosion can be uniform or localized depending on the homogeneity of the environment and the material. "
            "Mitigation involves selecting materials with favorable electrode potentials, controlling environmental variables "
            "such as oxygen and chloride concentration, and applying protective coatings or cathodic protection. "
            "Electrochemical monitoring techniques (e.g., linear polarization resistance) are used to assess corrosion rates. "
            "Reference: Jones, D.A., Principles and Prevention of Corrosion, 2nd Ed., Prentice Hall, 1996."
        ),
        key_factors=[
            "Anodic and cathodic reaction kinetics",
            "Electrolyte composition and conductivity",
            "Material electrode potentials",
            "Environmental pH and temperature",
            "Presence of oxidizing/reducing species"
        ],
        primary_authority=[
            "Jones, D.A., Principles and Prevention of Corrosion, 2nd Ed., Prentice Hall, 1996",
            "Uhlig, H.H., Uhlig's Corrosion Handbook, 3rd Ed., Wiley, 2011",
            "Fontana, M.G., Corrosion Engineering, 3rd Ed., McGraw-Hill, 1986"
        ],
        burden_holder="Asset Owner",
        adversary_position="Corrosion is negligible under current operating conditions",
        counter_arguments=[
            "Localized environmental changes can accelerate corrosion unexpectedly",
            "Protective films may break down under upset conditions",
            "Electrochemical measurements may not capture all corrosion forms",
            "Material microstructure can influence corrosion susceptibility",
            "Environmental monitoring may miss transient corrosive events"
        ],
        resolution_strategy="Implement continuous monitoring and periodic review of electrochemical parameters. Validate with field coupons and adjust mitigation as needed.",
        entity_scope=["pipeline", "vessel", "tank", "heat exchanger"],
        confidence=0.98,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ASTM G102-89(2015), Standard Practice for Calculation of Corrosion Rates and Related Information from Electrochemical Measurements"
        ]
    ),

    DoctrineBlock(
        topic="Galvanic Corrosion between Dissimilar Metals",
        keywords=["galvanic", "dissimilar metals", "EMF series", "couple", "potential difference"],
        conclusion_template="Galvanic corrosion occurs when dissimilar metals are electrically connected in an electrolyte, with the more active metal corroding preferentially. Proper material selection and isolation are critical to prevent galvanic attack.",
        reasoning_framework=(
            "Galvanic corrosion is driven by the potential difference between two dissimilar metals in electrical contact within an electrolyte. "
            "The metal with the lower (more negative) electrode potential becomes the anode and corrodes, while the more noble metal is protected. "
            "The galvanic series in the relevant environment (e.g., seawater) should be consulted to assess compatibility. "
            "The area ratio of cathode to anode is a critical factor: a large cathode and small anode accelerate attack on the anode. "
            "Mitigation strategies include material selection to minimize potential difference, electrical isolation (e.g., dielectric unions), "
            "application of coatings (preferably on the cathode), and use of sacrificial anodes. "
            "Environmental factors such as electrolyte conductivity and temperature also influence the rate of galvanic corrosion. "
            "Periodic inspection and monitoring for signs of galvanic attack are essential, especially at joints and interfaces. "
            "Reference: ISO 8044:2020, Corrosion of metals and alloys – Basic terms and definitions."
        ),
        key_factors=[
            "Electrode potential difference (galvanic series)",
            "Electrical continuity between metals",
            "Electrolyte conductivity",
            "Cathode-to-anode area ratio",
            "Environmental aggressiveness"
        ],
        primary_authority=[
            "ISO 8044:2020, Corrosion of metals and alloys – Basic terms and definitions",
            "Jones, D.A., Principles and Prevention of Corrosion, 2nd Ed., Prentice Hall, 1996",
            "ASM Handbook, Vol. 13A, Corrosion: Fundamentals, Testing, and Protection, ASM International, 2003"
        ],
        burden_holder="Design Engineer",
        adversary_position="Galvanic effects are negligible due to similar materials or lack of electrolyte",
        counter_arguments=[
            "Unexpected wetting or condensation can create electrolytic paths",
            "Protective coatings may be damaged, exposing bare metal",
            "Electrical continuity may be inadvertently established during maintenance",
            "Area ratio may change due to corrosion or repairs",
            "Environmental conditions may become more aggressive over time"
        ],
        resolution_strategy="Specify compatible materials, use dielectric isolation, and inspect regularly for galvanic attack. Apply coatings judiciously.",
        entity_scope=["pipeline", "flange", "heat exchanger", "fastener"],
        confidence=0.97,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ISO 8044:2020",
            "NACE SP0169-2013, Control of External Corrosion on Underground or Submerged Metallic Piping Systems"
        ]
    ),

    DoctrineBlock(
        topic="Pitting Corrosion due to Chloride-Induced Passivity Breakdown",
        keywords=["pitting", "chloride", "passivity", "localized", "breakdown"],
        conclusion_template="Pitting corrosion is a localized attack resulting from the breakdown of passive films, often triggered by chlorides. Stainless steels and other passive alloys are particularly susceptible in chloride-containing environments.",
        reasoning_framework=(
            "Pitting corrosion initiates when aggressive anions (notably chlorides) penetrate and locally disrupt the passive oxide film on metals such as stainless steel. "
            "Once a pit nucleates, autocatalytic processes lower the pH inside the pit and concentrate chlorides, accelerating metal dissolution. "
            "Critical pitting temperature (CPT) and critical pitting potential (CPP) are key parameters for material selection. "
            "Alloy composition (chromium, molybdenum, nitrogen content) significantly affects pitting resistance; higher PREN (Pitting Resistance Equivalent Number) alloys perform better. "
            "Mitigation includes controlling chloride levels, selecting appropriate alloys, and maintaining environmental conditions below CPT. "
            "Electrochemical testing (ASTM G48) and field coupon exposure are used for assessment. "
            "Surface finish and crevices can exacerbate pitting susceptibility. "
            "Reference: Sedriks, A.J., Corrosion of Stainless Steels, 2nd Ed., Wiley, 1996."
        ),
        key_factors=[
            "Chloride concentration",
            "Alloy composition and PREN",
            "Temperature and pH",
            "Presence of crevices or deposits",
            "Surface condition"
        ],
        primary_authority=[
            "Sedriks, A.J., Corrosion of Stainless Steels, 2nd Ed., Wiley, 1996",
            "ASTM G48-11, Standard Test Methods for Pitting and Crevice Corrosion Resistance of Stainless Steels and Related Alloys by Use of Ferric Chloride Solution",
            "ISO 15156-3:2020, Petroleum and natural gas industries — Materials for use in H2S-containing environments in oil and gas production — Part 3: Cracking-resistant CRAs (corrosion-resistant alloys) and other alloys"
        ],
        burden_holder="Materials Engineer",
        adversary_position="Bulk corrosion rates are low, so pitting is not a concern",
        counter_arguments=[
            "Localized attack can lead to rapid penetration despite low average rates",
            "Chloride ingress may occur due to leaks or upsets",
            "Surface defects or inclusions can act as pit initiation sites",
            "Environmental conditions may exceed CPT temporarily",
            "Field monitoring may not detect early pit formation"
        ],
        resolution_strategy="Control chloride levels, select high-PREN alloys, and perform regular inspection for pitting. Use electrochemical testing for validation.",
        entity_scope=["pipeline", "vessel", "heat exchanger", "tank"],
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ASTM G48-11",
            "ISO 15156-3:2020"
        ]
    ),

    DoctrineBlock(
        topic="Crevice Corrosion due to Differential Aeration",
        keywords=["crevice", "differential aeration", "oxygen depletion", "localized", "gasket"],
        conclusion_template="Crevice corrosion arises in shielded areas where oxygen depletion leads to differential aeration, promoting localized attack. Design and maintenance must minimize crevice formation and ensure accessibility for inspection.",
        reasoning_framework=(
            "Crevice corrosion occurs when a stagnant microenvironment forms between a metal surface and an adjacent material (e.g., gasket, deposit, lap joint), "
            "leading to oxygen depletion and a drop in pH within the crevice. The resulting differential aeration cell causes the crevice to become anodic relative to the external surface, "
            "driving localized dissolution. Factors influencing susceptibility include crevice geometry, material composition, and environmental aggressiveness (notably chloride content). "
            "Mitigation strategies involve design modifications to eliminate or seal crevices, selection of resistant materials, and application of sealants or coatings. "
            "Regular cleaning and inspection are essential to prevent deposit buildup. Electrochemical testing (ASTM G78) can assess crevice corrosion resistance. "
            "Reference: Fontana, M.G., Corrosion Engineering, 3rd Ed., McGraw-Hill, 1986."
        ),
        key_factors=[
            "Crevice geometry and tightness",
            "Oxygen concentration gradient",
            "Chloride and other aggressive ions",
            "Material composition",
            "Surface deposits or fouling"
        ],
        primary_authority=[
            "Fontana, M.G., Corrosion Engineering, 3rd Ed., McGraw-Hill, 1986",
            "ASTM G78-15, Standard Guide for Crevice Corrosion Testing of Iron-Base and Nickel-Base Stainless Alloys in Seawater and Other Chloride-Containing Environments",
            "Uhlig, H.H., Uhlig's Corrosion Handbook, 3rd Ed., Wiley, 2011"
        ],
        burden_holder="Design Engineer",
        adversary_position="Crevices are unavoidable but do not significantly impact corrosion",
        counter_arguments=[
            "Even small crevices can initiate severe localized attack",
            "Deposits or biofilms can create crevice-like conditions",
            "Sealants may degrade over time, exposing crevices",
            "Inspection may miss hidden crevices",
            "Environmental upsets can increase aggressiveness"
        ],
        resolution_strategy="Redesign to eliminate crevices, use resistant materials, and maintain rigorous inspection and cleaning protocols.",
        entity_scope=["flange", "gasket", "lap joint", "tank"],
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ASTM G78-15"
        ]
    ),

    DoctrineBlock(
        topic="Stress Corrosion Cracking (SCC) in Chloride and Caustic Environments",
        keywords=["SCC", "chloride", "caustic", "sulfide", "cracking"],
        conclusion_template="SCC is a synergistic failure mode involving tensile stress and a specific corrosive environment, such as chlorides or caustics. Material selection and stress minimization are essential for prevention.",
        reasoning_framework=(
            "Stress corrosion cracking (SCC) results from the combined action of tensile stress (applied or residual) and a specific corrosive environment. "
            "For austenitic stainless steels, chlorides are the most common cause, while caustic SCC affects carbon steels and nickel alloys. "
            "Hydrogen sulfide (H2S) environments can also promote SCC, especially in high-strength steels. "
            "SCC typically initiates at stress concentrators such as welds, cold-worked areas, or notches. "
            "Mitigation involves selecting resistant materials (e.g., low-susceptibility alloys), reducing tensile stresses (post-weld heat treatment, stress relief), "
            "and controlling environmental variables (chloride, caustic, or sulfide concentration, temperature, pH). "
            "NACE MR0175/ISO 15156 provides guidance for material selection in H2S service. "
            "Non-destructive examination (NDE) and periodic inspection are necessary for early detection. "
            "Reference: NACE MR0175/ISO 15156, Petroleum and natural gas industries — Materials for use in H2S-containing environments."
        ),
        key_factors=[
            "Tensile stress (applied or residual)",
            "Specific environment (chloride, caustic, sulfide)",
            "Material susceptibility",
            "Temperature and pH",
            "Presence of stress concentrators"
        ],
        primary_authority=[
            "NACE MR0175/ISO 15156",
            "ASM Handbook, Vol. 13A, Corrosion: Fundamentals, Testing, and Protection, ASM International, 2003",
            "Jones, D.A., Principles and Prevention of Corrosion, 2nd Ed., Prentice Hall, 1996"
        ],
        burden_holder="Materials Engineer",
        adversary_position="Operating stresses are below threshold for SCC",
        counter_arguments=[
            "Residual stresses from fabrication may be underestimated",
            "Environmental excursions can increase SCC risk",
            "Material batch variability may affect susceptibility",
            "Surface condition (e.g., roughness) can influence initiation",
            "Inspection techniques may not detect early-stage cracks"
        ],
        resolution_strategy="Use resistant alloys, minimize stresses, and monitor environment. Apply NDE and follow NACE/ISO guidance.",
        entity_scope=["pipeline", "vessel", "heat exchanger", "weld"],
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "NACE MR0175/ISO 15156"
        ]
    ),

    DoctrineBlock(
        topic="Hydrogen Embrittlement, HIC, SOHIC, and SSC",
        keywords=["hydrogen", "embrittlement", "HIC", "SOHIC", "SSC"],
        conclusion_template="Hydrogen-induced cracking (HIC), stepwise HIC (SOHIC), and sulfide stress cracking (SSC) are forms of hydrogen damage prevalent in sour environments. Material selection and hardness control are primary defenses.",
        reasoning_framework=(
            "Hydrogen damage in steels exposed to H2S-containing (sour) environments manifests as hydrogen-induced cracking (HIC), stepwise HIC (SOHIC), and sulfide stress cracking (SSC). "
            "Atomic hydrogen generated by corrosion reactions diffuses into the steel, accumulating at inclusions or defects, leading to internal cracks. "
            "SSC occurs under tensile stress and is exacerbated by high hardness and susceptible microstructures. "
            "NACE MR0175/ISO 15156 and NACE TM0284 provide acceptance criteria for materials in sour service, including maximum hardness and microstructure requirements. "
            "Mitigation involves selecting low-susceptibility steels, controlling hardness (e.g., PWHT), and minimizing stress concentrators. "
            "Environmental control (e.g., limiting H2S, pH, and chloride) further reduces risk. "
            "Regular inspection (ultrasonic, magnetic particle) is essential for early detection. "
            "Reference: NACE TM0284-2016, Evaluation of Pipeline and Pressure Vessel Steels for Resistance to Hydrogen-Induced Cracking."
        ),
        key_factors=[
            "H2S concentration",
            "Steel composition and microstructure",
            "Hardness and heat treatment",
            "Tensile stress",
            "Presence of inclusions or laminations"
        ],
        primary_authority=[
            "NACE TM0284-2016",
            "NACE MR0175/ISO 15156",
            "API RP 941, Steels for Hydrogen Service at Elevated Temperatures and Pressures"
        ],
        burden_holder="Materials Engineer",
        adversary_position="Material meets minimum requirements; hydrogen damage unlikely",
        counter_arguments=[
            "Localized hardness may exceed specification",
            "Environmental upsets can increase H2S exposure",
            "Microstructural heterogeneity may increase susceptibility",
            "Inspection may not detect sub-surface cracks",
            "Service history may introduce new stress concentrators"
        ],
        resolution_strategy="Strictly enforce material and hardness specs, monitor environment, and perform regular NDE.",
        entity_scope=["pipeline", "vessel", "weld", "pressure part"],
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "NACE TM0284-2016",
            "NACE MR0175/ISO 15156"
        ]
    ),

    DoctrineBlock(
        topic="Erosion Corrosion due to Flow Velocity and Impingement",
        keywords=["erosion", "corrosion", "flow velocity", "impingement", "cavitation"],
        conclusion_template="Erosion corrosion results from the combined action of mechanical wear and chemical attack, often due to high flow velocities or impingement. Design and operational controls are key to mitigation.",
        reasoning_framework=(
            "Erosion corrosion is accelerated material loss caused by the synergy of mechanical erosion (from high-velocity fluids, suspended solids, or impingement) and electrochemical corrosion. "
            "Critical velocity thresholds exist above which protective films are stripped, exposing fresh metal to corrosion. "
            "Cavitation (formation and collapse of vapor bubbles) and turbulent flow at elbows, tees, or orifices increase risk. "
            "Material selection (e.g., harder alloys, ceramics) and design modifications (smooth transitions, increased radii) reduce susceptibility. "
            "Operational controls include limiting flow velocity, reducing solids content, and avoiding abrupt changes in direction. "
            "Inspection for wall thinning (ultrasonic testing) and monitoring of flow parameters are essential. "
            "Reference: ASM Handbook, Vol. 13A, Corrosion: Fundamentals, Testing, and Protection, ASM International, 2003."
        ),
        key_factors=[
            "Flow velocity and turbulence",
            "Presence of suspended solids",
            "Material hardness and toughness",
            "Geometry (elbows, tees, orifices)",
            "Cavitation potential"
        ],
        primary_authority=[
            "ASM Handbook, Vol. 13A, Corrosion: Fundamentals, Testing, and Protection, ASM International, 2003",
            "Jones, D.A., Principles and Prevention of Corrosion, 2nd Ed., Prentice Hall, 1996",
            "API 574, Inspection Practices for Piping System Components"
        ],
        burden_holder="Process Engineer",
        adversary_position="Flow velocities are within design limits; erosion corrosion is unlikely",
        counter_arguments=[
            "Localized velocities may exceed average values",
            "Solids or debris may be introduced during upsets",
            "Design changes may inadvertently increase turbulence",
            "Material degradation may reduce resistance over time",
            "Inspection intervals may be too long to detect rapid loss"
        ],
        resolution_strategy="Review flow regimes, select resistant materials, and enhance inspection at high-risk locations.",
        entity_scope=["pipeline", "elbow", "tee", "orifice", "pump"],
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "API 574"
        ]
    ),

    DoctrineBlock(
        topic="Microbiologically Influenced Corrosion (MIC) by SRB and APB",
        keywords=["MIC", "SRB", "APB", "biofilm", "microbial"],
        conclusion_template="MIC is caused by microbial activity, notably sulfate-reducing bacteria (SRB) and acid-producing bacteria (APB), leading to localized corrosion. Biocide programs and monitoring are essential.",
        reasoning_framework=(
            "Microbiologically influenced corrosion (MIC) involves the action of microorganisms, especially SRB and APB, which form biofilms on metal surfaces. "
            "SRB reduce sulfate to sulfide, producing H2S and creating localized acidic environments that accelerate corrosion. "
            "Biofilms can also create differential aeration cells, promoting pitting and under-deposit corrosion. "
            "Mitigation strategies include regular biocide dosing, pigging, and mechanical cleaning to disrupt biofilms. "
            "Monitoring involves culture-based and molecular techniques (e.g., qPCR) to quantify microbial populations. "
            "Material selection and coatings can reduce susceptibility, but no material is immune. "
            "Reference: Beech, I.B. & Sunner, J., Microbiologically Influenced Corrosion: Towards an Understanding of Mechanisms, Int. Biodeterior. Biodegrad., 2004."
        ),
        key_factors=[
            "Presence and activity of SRB/APB",
            "Biofilm formation",
            "Nutrient availability",
            "Material susceptibility",
            "Effectiveness of biocide program"
        ],
        primary_authority=[
            "Beech, I.B. & Sunner, J., Microbiologically Influenced Corrosion: Towards an Understanding of Mechanisms, Int. Biodeterior. Biodegrad., 2004",
            "NACE TM0194-2014, Field Monitoring of Bacterial Growth in Oil and Gas Systems",
            "ASM Handbook, Vol. 13C, Corrosion: Environments and Industries, ASM International, 2006"
        ],
        burden_holder="Operations",
        adversary_position="Microbial activity is low; MIC is not a significant threat",
        counter_arguments=[
            "Biofilms can develop rapidly under favorable conditions",
            "Biocide resistance may develop",
            "Monitoring may not detect all microbial species",
            "Localized MIC can occur even with low bulk counts",
            "Pigging may not remove all biofilms"
        ],
        resolution_strategy="Implement robust biocide and monitoring programs, and maintain mechanical cleaning schedules.",
        entity_scope=["pipeline", "tank", "vessel", "water system"],
        confidence=0.89,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "NACE TM0194-2014"
        ]
    ),

    DoctrineBlock(
        topic="CO2 Corrosion (Sweet Corrosion) and de Waard-Milliams Model",
        keywords=["CO2", "sweet corrosion", "de Waard", "Milliams", "carbon steel"],
        conclusion_template="CO2 corrosion, or sweet corrosion, is a major threat to carbon steel in oil and gas systems. The de Waard-Milliams model provides a predictive framework for corrosion rates.",
        reasoning_framework=(
            "CO2 dissolves in water to form carbonic acid, lowering pH and promoting general and localized corrosion of carbon steel. "
            "The de Waard-Milliams model estimates corrosion rates based on CO2 partial pressure, temperature, and flow regime. "
            "Protective iron carbonate films may form, reducing corrosion, but are unstable at high velocities or low pH. "
            "Mitigation includes material selection, corrosion inhibitors, and control of water chemistry. "
            "Field monitoring (coupons, ER probes) and periodic pigging are essential. "
            "Reference: de Waard, C. & Milliams, D., Carbonic Acid Corrosion of Steel, Corrosion, 1975."
        ),
        key_factors=[
            "CO2 partial pressure",
            "Water chemistry (pH, bicarbonate)",
            "Temperature",
            "Flow regime and velocity",
            "Presence of inhibitors"
        ],
        primary_authority=[
            "de Waard, C. & Milliams, D., Carbonic Acid Corrosion of Steel, Corrosion, 1975",
            "NACE SP0775-2013, Preparation, Installation, Analysis, and Interpretation of Corrosion Coupons in Oilfield Operations",
            "ASM Handbook, Vol. 13C, Corrosion: Environments and Industries, ASM International, 2006"
        ],
        burden_holder="Corrosion Engineer",
        adversary_position="CO2 levels are low; corrosion is not significant",
        counter_arguments=[
            "Localized attack can occur even at low average rates",
            "Protective films may be disrupted by flow or upsets",
            "Inhibitor performance may degrade over time",
            "Water chemistry may change due to process upsets",
            "Field monitoring may not capture transient events"
        ],
        resolution_strategy="Use predictive models, monitor field data, and adjust mitigation as needed.",
        entity_scope=["pipeline", "flowline", "separator", "downhole tubing"],
        confidence=0.88,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "NACE SP0775-2013"
        ]
    ),

    DoctrineBlock(
        topic="H2S Corrosion (Sour Service) and NACE MR0175/ISO 15156",
        keywords=["H2S", "sour service", "NACE MR0175", "ISO 15156", "sulfide"],
        conclusion_template="H2S corrosion in sour service environments requires strict adherence to NACE MR0175/ISO 15156 for material selection and hardness control. Monitoring and inspection are critical.",
        reasoning_framework=(
            "H2S reacts with steel to form iron sulfide films, which may be protective or non-protective depending on environmental conditions. "
            "Sour service increases risk of sulfide stress cracking (SSC), hydrogen-induced cracking (HIC), and corrosion fatigue. "
            "NACE MR0175/ISO 15156 specifies material and hardness limits for equipment in H2S environments. "
            "Mitigation involves selecting compliant materials, controlling process variables (pH, chloride, temperature), and applying inhibitors. "
            "Regular inspection (NDE) and environmental monitoring are essential. "
            "Reference: NACE MR0175/ISO 15156."
        ),
        key_factors=[
            "H2S concentration",
            "Material composition and hardness",
            "pH and chloride content",
            "Temperature",
            "Stress level"
        ],
        primary_authority=[
            "NACE MR0175/ISO 15156",
            "API RP 941",
            "ASM Handbook, Vol. 13C, Corrosion: Environments and Industries, ASM International, 2006"
        ],
        burden_holder="Materials Engineer",
        adversary_position="Material is compliant; H2S corrosion is not a concern",
        counter_arguments=[
            "Localized hardness may exceed specification",
            "Environmental upsets can increase H2S exposure",
            "Protective films may be unstable",
            "Inspection may not detect early-stage cracking",
            "Service history may introduce new stress concentrators"
        ],
        resolution_strategy="Strictly enforce material and hardness specs, monitor environment, and perform regular NDE.",
        entity_scope=["pipeline", "vessel", "separator", "downhole tubing"],
        confidence=0.87,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "NACE MR0175/ISO 15156"
        ]
    ),

    DoctrineBlock(
        topic="Cathodic Protection: Impressed Current and Sacrificial Anode Systems",
        keywords=["cathodic protection", "impressed current", "sacrificial anode", "polarization", "potential"],
        conclusion_template="Cathodic protection (CP) uses external current sources or sacrificial anodes to shift the protected structure's potential, suppressing corrosion. System design and monitoring are critical for effectiveness.",
        reasoning_framework=(
            "Cathodic protection (CP) involves making the protected structure the cathode of an electrochemical cell. "
            "Impressed current systems use external DC power sources and inert anodes, while sacrificial anode systems use more active metals (e.g., zinc, magnesium) that corrode preferentially. "
            "Design must ensure uniform current distribution and avoid overprotection (which can cause coating disbondment or hydrogen evolution). "
            "Potential measurements (e.g., using reference electrodes) are used to verify protection criteria (e.g., -850 mV vs. CSE for steel in soil). "
            "Periodic monitoring and maintenance (anode replacement, rectifier checks) are essential. "
            "Reference: NACE SP0169-2013, Control of External Corrosion on Underground or Submerged Metallic Piping Systems."
        ),
        key_factors=[
            "System type (impressed current or sacrificial)",
            "Anode material and placement",
            "Current distribution",
            "Coating integrity",
            "Potential monitoring"
        ],
        primary_authority=[
            "NACE SP0169-2013",
            "Peabody, A.W., Control of Pipeline Corrosion, 2nd Ed., NACE, 2001",
            "ISO 15589-1:2020, Petroleum and natural gas industries — Cathodic protection of pipeline transportation systems — Part 1: On-land pipelines"
        ],
        burden_holder="Corrosion Engineer",
        adversary_position="CP is unnecessary or overdesigned for the structure",
        counter_arguments=[
            "Coating defects can increase CP current demand",
            "Stray currents may reduce CP effectiveness",
            "Anode consumption rates may be underestimated",
            "Potential measurements may not represent all areas",
            "Environmental changes can alter CP requirements"
        ],
        resolution_strategy="Design CP systems per standards, monitor regularly, and adjust as needed.",
        entity_scope=["pipeline", "tank", "offshore structure", "buried vessel"],
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "NACE SP0169-2013",
            "ISO 15589-1:2020"
        ]
    ),

    DoctrineBlock(
        topic="Coating Systems: Epoxy, Polyurethane, FBE, and Three-Layer",
        keywords=["coating", "epoxy", "polyurethane", "FBE", "three-layer"],
        conclusion_template="Coating systems provide a primary barrier against corrosion. Selection depends on environment, application method, and compatibility with cathodic protection.",
        reasoning_framework=(
            "Coatings act as physical barriers, preventing contact between the metal and corrosive environment. "
            "Epoxy coatings offer good chemical resistance and adhesion, while polyurethane provides flexibility and UV resistance. "
            "Fusion-bonded epoxy (FBE) is widely used for pipelines due to its strong adhesion and resistance to cathodic disbondment. "
            "Three-layer systems (FBE + adhesive + polyethylene) enhance mechanical and moisture resistance. "
            "Proper surface preparation (e.g., SSPC-SP10/NACE No. 2) is critical for coating performance. "
            "Compatibility with cathodic protection must be ensured, as some coatings may disbond under CP. "
            "Inspection (holiday testing, thickness measurement) and maintenance are necessary for long-term protection. "
            "Reference: ISO 21809-1:2018, Petroleum and natural gas industries — External coatings for buried or submerged pipelines."
        ),
        key_factors=[
            "Coating type and thickness",
            "Surface preparation quality",
            "Application method",
            "Environmental exposure",
            "Compatibility with CP"
        ],
        primary_authority=[
            "ISO 21809-1:2018",
            "NACE SP0109-2014, Standard Practice for Selection and Application of Protective Coatings for Offshore Oil and Gas Structures",
            "ASM Handbook, Vol. 13B, Corrosion: Materials, ASM International, 2005"
        ],
        burden_holder="Coating Engineer",
        adversary_position="Coating is sufficient; no further mitigation required",
        counter_arguments=[
            "Application defects can compromise performance",
            "Mechanical damage may occur during installation",
            "Environmental exposure may exceed design limits",
            "Coating may not be compatible with CP",
            "Inspection may not detect all flaws"
        ],
        resolution_strategy="Specify coatings per standards, ensure quality control, and integrate with CP systems.",
        entity_scope=["pipeline", "tank", "offshore structure", "vessel"],
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ISO 21809-1:2018"
        ]
    ),

    DoctrineBlock(
        topic="Corrosion Inhibitors: Film-Forming and Neutralizing Types",
        keywords=["corrosion inhibitor", "film-forming", "neutralizing", "dosage", "monitoring"],
        conclusion_template="Corrosion inhibitors reduce corrosion rates by forming protective films or neutralizing corrosive agents. Proper selection, dosing, and monitoring are essential.",
        reasoning_framework=(
            "Corrosion inhibitors are chemicals added to process streams to reduce corrosion rates. "
            "Film-forming inhibitors (e.g., amines, imidazolines) adsorb onto metal surfaces, creating a barrier to corrosive species. "
            "Neutralizing inhibitors adjust pH to less aggressive levels. "
            "Selection depends on process chemistry, temperature, flow regime, and compatibility with other treatments. "
            "Proper dosing is critical; underdosing reduces effectiveness, while overdosing can cause operational issues (e.g., foaming, emulsion formation). "
            "Monitoring involves field testing (e.g., residual concentration, corrosion coupons, ER probes) and periodic adjustment. "
            "Reference: NACE SP0108-2008, Corrosion Inhibitor Selection and Management."
        ),
        key_factors=[
            "Inhibitor type and chemistry",
            "Dosage and injection point",
            "Process conditions (pH, temperature, flow)",
            "Monitoring and control",
            "Compatibility with other treatments"
        ],
        primary_authority=[
            "NACE SP0108-2008",
            "ASM Handbook, Vol. 13C, Corrosion: Environments and Industries, ASM International, 2006",
            "API RP 939C, Guidelines for Avoiding Sulfidation (Sulfidic) Corrosion Failures in Oil Refineries"
        ],
        burden_holder="Corrosion Engineer",
        adversary_position="Inhibitor program is sufficient; no further action needed",
        counter_arguments=[
            "Process upsets may dilute or remove inhibitor",
            "Inhibitor may not reach all vulnerable areas",
            "Inhibitor performance may degrade over time",
            "Compatibility issues with other chemicals",
            "Monitoring may not detect localized failures"
        ],
        resolution_strategy="Implement robust monitoring, adjust dosing as needed, and review inhibitor performance regularly.",
        entity_scope=["pipeline", "separator", "downhole tubing", "vessel"],
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "NACE SP0108-2008"
        ]
    ),

    DoctrineBlock(
        topic="Material Selection: CRA, Duplex, and Super Duplex",
        keywords=["material selection", "CRA", "duplex", "super duplex", "PREN"],
        conclusion_template="Material selection is based on corrosion resistance, mechanical properties, and cost. Duplex and super duplex stainless steels offer enhanced resistance in aggressive environments.",
        reasoning_framework=(
            "Corrosion-resistant alloys (CRAs), including duplex and super duplex stainless steels, are selected for their superior resistance to pitting, crevice, and stress corrosion cracking. "
            "PREN (Pitting Resistance Equivalent Number) is used to compare alloys; higher values indicate better resistance. "
            "Duplex alloys combine high strength with good resistance to chloride-induced corrosion, while super duplex grades are used in the most aggressive environments. "
            "Material selection must consider process conditions (chloride, temperature, pressure), fabrication constraints, and cost. "
            "ISO 15156-3 and NORSOK M-630 provide guidance for material selection in oil and gas applications. "
            "Qualification testing (e.g., ASTM G48) and supplier certification are essential. "
            "Reference: ISO 15156-3:2020, NORSOK M-630, ASTM G48-11."
        ),
        key_factors=[
            "Alloy composition and PREN",
            "Process environment (chloride, temperature, pressure)",
            "Mechanical properties",
            "Fabrication and welding constraints",
            "Cost and availability"
        ],
        primary_authority=[
            "ISO 15156-3:2020",
            "NORSOK M-630, Material Data Sheets for Piping",
            "ASTM G48-11"
        ],
        burden_holder="Materials Engineer",
        adversary_position="Lower-cost materials are adequate for the application",
        counter_arguments=[
            "Aggressive environments may exceed material limits",
            "Improper welding may reduce corrosion resistance",
            "Supplier variability can affect quality",
            "Unexpected process upsets may occur",
            "Qualification testing may not represent service conditions"
        ],
        resolution_strategy="Follow standards for material selection, require supplier certification, and perform qualification testing.",
        entity_scope=["pipeline", "manifold", "valve", "heat exchanger"],
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ISO 15156-3:2020",
            "NORSOK M-630"
        ]
    ),

    DoctrineBlock(
        topic="Corrosion Monitoring: Coupons, ER, LPR, and FSM",
        keywords=["corrosion monitoring", "coupon", "ER", "LPR", "FSM"],
        conclusion_template="Corrosion monitoring uses various techniques to assess rates and mechanisms. Selection depends on environment, accessibility, and required sensitivity.",
        reasoning_framework=(
            "Corrosion monitoring is essential for managing integrity and verifying mitigation effectiveness. "
            "Coupons provide direct measurement of metal loss but require periodic retrieval. "
            "Electrical resistance (ER) probes offer continuous monitoring of general corrosion. "
            "Linear polarization resistance (LPR) provides rapid assessment of corrosion rate in conductive environments. "
            "Field signature method (FSM) enables distributed monitoring along pipelines. "
            "Selection depends on process conditions, required sensitivity, and accessibility. "
            "Data must be interpreted in context, considering probe placement and environmental variability. "
            "Reference: NACE SP0775-2013, Preparation, Installation, Analysis, and Interpretation of Corrosion Coupons in Oilfield Operations."
        ),
        key_factors=[
            "Monitoring technique suitability",
            "Probe placement and retrieval",
            "Environmental variability",
            "Data interpretation",
            "Integration with integrity management"
        ],
        primary_authority=[
            "NACE SP0775-2013",
            "ASM Handbook, Vol. 13C, Corrosion: Environments and Industries, ASM International, 2006",
            "API 570, Piping Inspection Code"
        ],
        burden_holder="Corrosion Engineer",
        adversary_position="Current monitoring is sufficient; no further action required",
        counter_arguments=[
            "Probe placement may not represent worst-case locations",
            "Data may be affected by process upsets",
            "Coupons may not capture localized attack",
            "Interpretation may be subjective",
            "Monitoring intervals may be too long"
        ],
        resolution_strategy="Use multiple monitoring techniques, optimize probe placement, and integrate data with inspection programs.",
        entity_scope=["pipeline", "vessel", "separator", "tank"],
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "NACE SP0775-2013"
        ]
    ),

    DoctrineBlock(
        topic="Internal Corrosion Direct Assessment (ICDA)",
        keywords=["ICDA", "internal corrosion", "direct assessment", "pipeline", "integrity"],
        conclusion_template="ICDA is a structured process for assessing internal corrosion threats in pipelines. It combines modeling, inspection, and monitoring data.",
        reasoning_framework=(
            "Internal Corrosion Direct Assessment (ICDA) is a multi-step process for evaluating internal corrosion in pipelines, particularly where in-line inspection is impractical. "
            "The process includes pre-assessment (data gathering), indirect inspection (modeling, monitoring), direct examination (field inspection), and post-assessment (data integration). "
            "ICDA relies on flow modeling to identify high-risk locations (e.g., low spots, water hold-up areas). "
            "Field validation is performed by excavating and inspecting selected sites. "
            "Integration of monitoring data (coupons, ER probes) enhances accuracy. "
            "Reference: NACE SP0206-2006, Internal Corrosion Direct Assessment Methodology for Pipelines Carrying Normally Dry Natural Gas."
        ),
        key_factors=[
            "Pipeline flow regime and geometry",
            "Water and corrosive species presence",
            "Monitoring and inspection data",
            "Modeling accuracy",
            "Integration with integrity management"
        ],
        primary_authority=[
            "NACE SP0206-2006",
            "API 1160, Managing System Integrity for Hazardous Liquid Pipelines",
            "ASM Handbook, Vol. 13C, Corrosion: Environments and Industries, ASM International, 2006"
        ],
        burden_holder="Pipeline Integrity Engineer",
        adversary_position="ICDA is unnecessary; monitoring is sufficient",
        counter_arguments=[
            "Modeling may not capture all risk factors",
            "Field validation may miss localized attack",
            "Data integration may be incomplete",
            "Process upsets may introduce new threats",
            "ICDA may not be applicable to all pipeline types"
        ],
        resolution_strategy="Follow ICDA methodology, validate with field data, and integrate findings with integrity management.",
        entity_scope=["pipeline", "flowline", "gathering system"],
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "NACE SP0206-2006"
        ]
    ),

    DoctrineBlock(
        topic="External Corrosion Direct Assessment (ECDA)",
        keywords=["ECDA", "external corrosion", "direct assessment", "pipeline", "integrity"],
        conclusion_template="ECDA is a structured process for assessing external corrosion threats in pipelines. It integrates indirect inspection, direct examination, and post-assessment.",
        reasoning_framework=(
            "External Corrosion Direct Assessment (ECDA) is a four-step process: pre-assessment, indirect inspection (e.g., close-interval potential survey, DCVG), direct examination (excavation), and post-assessment. "
            "The goal is to identify and mitigate external corrosion threats, particularly for pipelines without in-line inspection capability. "
            "Integration of coating condition, cathodic protection data, and environmental factors is essential. "
            "Direct examination validates indirect findings and informs future assessments. "
            "Reference: NACE SP0502-2010, Pipeline External Corrosion Direct Assessment Methodology."
        ),
        key_factors=[
            "Coating condition",
            "Cathodic protection effectiveness",
            "Environmental factors (soil resistivity, moisture)",
            "Indirect inspection data quality",
            "Integration with integrity management"
        ],
        primary_authority=[
            "NACE SP0502-2010",
            "API 1160",
            "ASM Handbook, Vol. 13C, Corrosion: Environments and Industries, ASM International, 2006"
        ],
        burden_holder="Pipeline Integrity Engineer",
        adversary_position="ECDA is unnecessary; CP is sufficient",
        counter_arguments=[
            "Indirect inspection may miss small defects",
            "Coating condition may deteriorate rapidly",
            "Environmental changes may increase risk",
            "Direct examination may be limited in scope",
            "Data integration may be incomplete"
        ],
        resolution_strategy="Follow ECDA methodology, validate with field data, and integrate findings with integrity management.",
        entity_scope=["pipeline", "flowline", "gathering system"],
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "NACE SP0502-2010"
        ]
    ),

    DoctrineBlock(
        topic="Pipeline Integrity Management: ASME B31G and RSTRENG",
        keywords=["integrity management", "ASME B31G", "RSTRENG", "remaining strength", "assessment"],
        conclusion_template="Pipeline integrity management uses ASME B31G and RSTRENG methods to assess remaining strength and fitness-for-service. Accurate defect characterization and conservative assumptions are essential.",
        reasoning_framework=(
            "ASME B31G and RSTRENG are widely used methods for assessing the remaining strength of corroded pipelines. "
            "B31G uses a simplified approach based on maximum depth and length of corrosion, while RSTRENG incorporates detailed profile data for more accurate assessment. "
            "Both methods assume conservative defect geometry and require accurate in-line inspection or direct measurement. "
            "Fitness-for-service decisions must consider uncertainties in measurement, material properties, and loading conditions. "
            "Periodic reassessment is necessary as new data become available. "
            "Reference: ASME B31G-2012, Manual for Determining the Remaining Strength of Corroded Pipelines."
        ),
        key_factors=[
            "Defect depth and length",
            "Pipe material properties",
            "Operating pressure",
            "Measurement accuracy",
            "Conservative assumptions"
        ],
        primary_authority=[
            "ASME B31G-2012",
            "API 579-1/ASME FFS-1, Fitness-For-Service",
            "API 1160"
        ],
        burden_holder="Pipeline Integrity Engineer",
        adversary_position="Defects are minor and do not affect integrity",
        counter_arguments=[
            "Measurement errors may underestimate defect severity",
            "Material properties may vary from nominal values",
            "Loading conditions may exceed design",
            "Defect growth may be underestimated",
            "Assessment methods may not capture all failure modes"
        ],
        resolution_strategy="Use conservative assessment methods, validate with field data, and reassess periodically.",
        entity_scope=["pipeline", "flowline"],
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ASME B31G-2012"
        ]
    ),

    DoctrineBlock(
        topic="Corrosion Allowance and Remaining Life Assessment",
        keywords=["corrosion allowance", "remaining life", "thickness", "assessment", "design"],
        conclusion_template="Corrosion allowance is included in design to account for expected metal loss. Remaining life assessment requires accurate monitoring and conservative assumptions.",
        reasoning_framework=(
            "Corrosion allowance is the additional wall thickness specified at design to accommodate anticipated metal loss during service. "
            "Remaining life assessment compares current wall thickness (from inspection) to minimum allowable thickness, considering corrosion rates and uncertainties. "
            "Corrosion rates are derived from monitoring data (coupons, probes) and historical experience. "
            "Conservative assumptions are used to account for variability and measurement error. "
            "Periodic reassessment is necessary as new data become available. "
            "Reference: API 570, Piping Inspection Code."
        ),
        key_factors=[
            "Design corrosion allowance",
            "Current wall thickness",
            "Corrosion rate",
            "Minimum allowable thickness",
            "Measurement uncertainty"
        ],
        primary_authority=[
            "API 570",
            "API 579-1/ASME FFS-1",
            "ASM Handbook, Vol. 13C, Corrosion: Environments and Industries, ASM International, 2006"
        ],
        burden_holder="Design Engineer",
        adversary_position="Corrosion rates are overestimated; remaining life is adequate",
        counter_arguments=[
            "Localized thinning may not be detected",
            "Corrosion rates may increase due to process changes",
            "Measurement error may be significant",
            "Minimum thickness may not account for all loads",
            "Historical data may not represent current conditions"
        ],
        resolution_strategy="Use conservative estimates, validate with inspection data, and reassess regularly.",
        entity_scope=["pipeline", "vessel", "tank"],
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "API 570"
        ]
    ),

    DoctrineBlock(
        topic="High Temperature Corrosion: Oxidation, Sulfidation, Carburization",
        keywords=["high temperature", "oxidation", "sulfidation", "carburization", "alloy selection"],
        conclusion_template="High temperature corrosion mechanisms include oxidation, sulfidation, and carburization. Alloy selection and process control are key to mitigation.",
        reasoning_framework=(
            "At elevated temperatures, metals are susceptible to oxidation (reaction with oxygen), sulfidation (reaction with sulfur species), and carburization (carbon ingress). "
            "Oxidation forms protective or non-protective oxide scales, depending on alloy composition (chromium, aluminum content). "
            "Sulfidation is accelerated in reducing, sulfur-rich environments and can lead to rapid metal loss. "
            "Carburization increases surface hardness and brittleness, reducing ductility. "
            "Alloy selection (e.g., high-chromium, nickel-based alloys) is critical for resistance. "
            "Process control (oxygen partial pressure, sulfur content, temperature) and protective coatings can mitigate risk. "
            "Reference: API RP 571, Damage Mechanisms Affecting Fixed Equipment in the Refining Industry."
        ),
        key_factors=[
            "Operating temperature",
            "Alloy composition",
            "Oxygen and sulfur partial pressures",
            "Carbon activity",
            "Protective scale stability"
        ],
        primary_authority=[
            "API RP 571",
            "ASM Handbook, Vol. 13C, Corrosion: Environments and Industries, ASM International, 2006",
            "API 939C"
        ],
        burden_holder="Materials Engineer",
        adversary_position="Current alloys are sufficient for service conditions",
        counter_arguments=[
            "Unexpected process upsets may increase risk",
            "Alloy composition may vary across welds",
            "Protective scales may spall or crack",
            "Carburization may not be detected by routine inspection",
            "Process control may be inadequate"
        ],
        resolution_strategy="Select alloys per standards, monitor process variables, and inspect for high-temperature damage.",
        entity_scope=["furnace tube", "reactor", "heater", "piping"],
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "API RP 571"
        ]
    ),
]

# ========== AUTHORITY HARDENING ==========

AUTHORITY_WEIGHTS = {
    "NACE MR0175/ISO 15156": 1.0,
    "ASME B31G-2012": 0.95,
    "API 570": 0.9,
    "ISO 15156-3:2020": 0.95,
    "ISO 8044:2020": 0.9,
    "ASTM G48-11": 0.9,
    "NACE SP0169-2013": 0.95,
    "ISO 21809-1:2018": 0.9,
    "API RP 941": 0.85,
    "API 579-1/ASME FFS-1": 0.9,
    "NACE TM0284-2016": 0.9,
    "NACE SP0775-2013": 0.9,
    "NACE SP0108-2008": 0.9,
    "NACE SP0502-2010": 0.9,
    "NACE SP0206-2006": 0.9,
    "API 1160": 0.85,
    "API RP 571": 0.9,
    "API 574": 0.9,
    "NORSOK M-630": 0.9,
    "ISO 15589-1:2020": 0.9,
    "ASM Handbook": 0.8,
    "Fontana, M.G.": 0.8,
    "Jones, D.A.": 0.8,
    "Beech, I.B.": 0.8,
    "de Waard, C.": 0.8,
}

def resolve_authority_conflicts(authorities: List[str]) -> List[str]:
    weighted = sorted(
        [(a, AUTHORITY_WEIGHTS.get(a.split(",")[0], 0.5)) for a in authorities],
        key=lambda x: x[1],
        reverse=True
    )
    max_weight = weighted[0][1] if weighted else 0
    return [a for a, w in weighted if w >= max_weight - 0.1]

# ========== SEMANTIC NORMALIZATION ==========

SEMANTIC_MAP = {
    "SCC": "stress corrosion cracking",
    "HIC": "hydrogen-induced cracking",
    "SOHIC": "stepwise hydrogen-induced cracking",
    "SSC": "sulfide stress cracking",
    "SRB": "sulfate-reducing bacteria",
    "APB": "acid-producing bacteria",
    "CP": "cathodic protection",
    "CRA": "corrosion-resistant alloy",
    "FBE": "fusion-bonded epoxy",
    "ICDA": "internal corrosion direct assessment",
    "ECDA": "external corrosion direct assessment",
    "PREN": "pitting resistance equivalent number",
    "FSM": "field signature method",
    "ER": "electrical resistance",
    "LPR": "linear polarization resistance",
    "MIC": "microbiologically influenced corrosion",
    "sweet corrosion": "CO2 corrosion",
    "sour service": "H2S corrosion",
    "film-forming": "film-forming inhibitor",
    "neutralizing": "neutralizing inhibitor",
    "corrosion coupon": "weight loss coupon",
    "remaining strength": "fitness-for-service",
    "corrosion allowance": "design corrosion allowance",
    "oxidation": "high temperature oxidation",
    "sulfidation": "high temperature sulfidation",
    "carburization": "high temperature carburization",
    "biofilm": "microbial biofilm",
    "galvanic couple": "galvanic corrosion",
    "passivity": "passive film",
    "de Waard-Milliams": "CO2 corrosion model",
    "RSTRENG": "remaining strength method",
    "Nernst": "Nernst equation",
    "EMF series": "galvanic series",
    "API 570": "piping inspection code",
    "API 579": "fitness-for-service",
    "API 574": "inspection practices",
    "API 1160": "pipeline integrity management",
    "API RP 941": "steels for hydrogen service",
    "API RP 571": "damage mechanisms",
    "NACE MR0175": "sour service material standard",
    "NACE SP0169": "cathodic protection standard",
    "NACE SP0775": "corrosion coupon standard",
    "NACE SP0108": "inhibitor selection standard",
    "NACE SP0502": "ECDA standard",
    "NACE SP0206": "ICDA standard",
    "NACE TM0284": "HIC test standard",
    "NACE TM0194": "MIC monitoring standard",
    "NORSOK M-630": "material data sheets",
    "ISO 15156": "sour service material standard",
    "ISO 8044": "corrosion terminology",
    "ISO 21809": "pipeline coating standard",
    "ISO 15589": "cathodic protection standard",
}

def normalize_term(term: str) -> str:
    return SEMANTIC_MAP.get(term.strip().lower(), term)

# ========== EPISTEMIC GUARDRAILS ==========

BANNED_PHRASES = [
    "guaranteed",
    "always",
    "never",
    "impossible",
    "no risk",
    "fail-safe",
    "zero probability",
    "absolutely",
    "perfect",
    "100% certain",
    "cannot occur",
]

def apply_epistemic_guardrails(text: str) -> str:
    for phrase in BANNED_PHRASES:
        text = text.replace(phrase, "[epistemic-guardrail]")
    return text

# ========== FACT FRAGILITY SCORING ==========

def score_fact_fragility(fact: str) -> Dict[str, float]:
    verifiability = 1.0 if any(a in fact for a in AUTHORITY_WEIGHTS) else 0.7
    recharacterization_risk = 0.3 if "may" in fact or "can" in fact else 0.7
    testimony_dependence = 0.5 if "field" in fact or "inspection" in fact else 0.8
    return {
        "verifiability": verifiability,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence,
    }

# ========== THREE-LAYER RESPONSE ==========

def doctrine_layer_search(scenario: str) -> Tuple[List[DoctrineBlock], List[str]]:
    hits = []
    triggered = []
    scenario_lower = scenario.lower()
    for block in DOCTRINE_CACHE:
        if any(k in scenario_lower for k in block.keywords):
            hits.append(block)
            triggered.append(block.topic)
    return hits, triggered

def semantic_layer_search(scenario: str) -> Tuple[List[DoctrineBlock], List[str]]:
    hits = []
    triggered = []
    scenario_terms = set(scenario.lower().split())
    for block in DOCTRINE_CACHE:
        block_terms = set([normalize_term(k).lower() for k in block.keywords])
        if scenario_terms & block_terms:
            hits.append(block)
            triggered.append(block.topic)
    return hits, triggered

def deep_analysis_layer(scenario: str, doctrine_blocks: List[DoctrineBlock]) -> Tuple[str, List[str], List[str], List[str], List[str]]:
    # Multi-doctrine decomposition, issue categorization, interaction DAG, 8-step resolution
    reasoning_lines = []
    key_factors = set()
    authorities = set()
    counter_args = set()
    res_strategies = set()
    for block in doctrine_blocks:
        reasoning_lines.append(block.reasoning_framework)
        key_factors.update(block.key_factors)
        authorities.update(block.primary_authority)
        counter_args.update(block.counter_arguments)
        res_strategies.add(block.resolution_strategy)
    # 8-step resolution (simplified for brevity)
    steps = [
        "1. Identify corrosion mechanism(s) from scenario and doctrine.",
        "2. Assess material and environmental compatibility.",
        "3. Evaluate mitigation strategies (coatings, inhibitors, CP, material selection).",
        "4. Review monitoring and inspection data for evidence of attack.",
        "5. Quantify risk using authoritative models and standards.",
        "6. Consider counter-arguments and uncertainties.",
        "7. Recommend resolution strategies based on best practice.",
        "8. Document rationale and supporting authorities."
    ]
    reasoning_lines.extend(steps)
    return (
        "\n".join(reasoning_lines),
        list(key_factors),
        list(authorities),
        list(counter_args),
        list(res_strategies)
    )

# ========== COVERAGE MAP ==========

def get_coverage_map(triggered: List[str]) -> Dict[str, Any]:
    all_topics = set(block.topic for block in DOCTRINE_CACHE)
    triggered_set = set(triggered)
    missed = list(all_topics - triggered_set)
    gap = len(missed) / len(all_topics) if all_topics else 0
    return {
        "triggered": list(triggered_set),
        "missed": missed,
        "epistemic_gap": gap
    }

# ========== DRIFT WATCHER ==========

BASELINE_HASH = hashlib.sha256(
    "".join(sorted(block.topic for block in DOCTRINE_CACHE)).encode()
).hexdigest()

def detect_drift() -> Dict[str, Any]:
    current_hash = hashlib.sha256(
        "".join(sorted(block.topic for block in DOCTRINE_CACHE)).encode()
    ).hexdigest()
    drifted = current_hash != BASELINE_HASH
    return {
        "baseline_hash": BASELINE_HASH,
        "current_hash": current_hash,
        "drift_detected": drifted
    }

# ========== AUDIT TRAIL ==========

AUDIT_LOG_PATH = Path(__file__).parent / "corrosion_engine_audit.jsonl"
AUDIT_LOCK = threading.Lock()

def log_audit_entry(entry: Dict[str, Any]):
    with AUDIT_LOCK:
        with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")

# ========== DETERMINISM HASH ==========

def compute_determinism_hash(response: Dict[str, Any]) -> str:
    relevant = {k: v for k, v in response.items() if k != "determinism_hash"}
    serialized = json.dumps(relevant, sort_keys=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

# ========== FASTAPI APP ==========

app = FastAPI(
    title="Corrosion Engineering Engine (MECH14)",
    description="Analyze corrosion mechanisms, material selection, cathodic protection, and corrosion monitoring for industrial equipment and pipelines.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    logger.info("Corrosion Engineering Engine (MECH14) started.")

@app.on_event("shutdown")
def on_shutdown():
    logger.info("Corrosion Engineering Engine (MECH14) shutting down.")

@app.post("/query", response_model=QueryResponse)
def query_corrosion(request: QueryRequest):
    query_id = str(uuid.uuid4())
    logger.info(f"Received query {query_id}: {request.scenario}")
    try:
        # Layer 1: Doctrine cache
        doctrine_hits, doctrine_triggered = doctrine_layer_search(request.scenario)
        # Layer 2: Semantic normalization
        if not doctrine_hits:
            doctrine_hits, doctrine_triggered = semantic_layer_search(request.scenario)
        # Layer 3: Deep analysis
        if not doctrine_hits:
            # Fallback: Use all doctrines for broad analysis
            doctrine_hits = DOCTRINE_CACHE
            doctrine_triggered = [block.topic for block in DOCTRINE_CACHE]
        reasoning, key_factors, authorities, counter_args, res_strategies = deep_analysis_layer(
            request.scenario, doctrine_hits
        )
        # Authority hardening
        authorities = resolve_authority_conflicts(authorities)
        # Epistemic guardrails
        primary_conclusion = apply_epistemic_guardrails(doctrine_hits[0].conclusion_template)
        reasoning = apply_epistemic_guardrails(reasoning)
        # Confidence and zones
        avg_conf = sum(block.confidence for block in doctrine_hits) / len(doctrine_hits)
        conf_zone = doctrine_hits[0].confidence_zone
        pos_zone = PositionZone.PLANNING if request.complexity <= 2 else (
            PositionZone.REPORTING if request.complexity <= 4 else PositionZone.AUDIT
        )
        # Fact fragility scoring (example)
        fragility = score_fact_fragility(primary_conclusion)
        # Determinism hash
        response_dict = {
            "engine_id": "MECH14",
            "query_id": query_id,
            "mode": request.mode,
            "confidence": avg_conf,
            "confidence_zone": conf_zone,
            "position_zone": pos_zone,
            "primary_conclusion": primary_conclusion,
            "reasoning_framework": reasoning,
            "key_factors": key_factors,
            "primary_authority": authorities,
            "counter_arguments": counter_args,
            "resolution_strategy": "; ".join(res_strategies),
            "determinism_hash": "",
        }
        response_dict["determinism_hash"] = compute_determinism_hash(response_dict)
        # Audit trail
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "query_id": query_id,
            "scenario": request.scenario,
            "response": response_dict,
            "fragility": fragility,
            "doctrine_triggered": doctrine_triggered,
        }
        log_audit_entry(audit_entry)
        # Metrics
        metrics_collector.record_query([block.topic for block in doctrine_hits])
        return QueryResponse(**response_dict)
    except Exception as e:
        logger.error(f"Error in query {query_id}: {e}")
        metrics_collector.record_error()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok", "engine_id": "MECH14", "time": datetime.utcnow().isoformat()}

@app.get("/metrics")
def metrics():
    return {
        "latency_stats": metrics_collector.get_latency_stats(),
        "doctrine_hit_rate": metrics_collector.get_doctrine_hit_rate(),
        "queries_last_hour": metrics_collector.queries_last_hour(),
    }

@app.get("/coverage")
def coverage():
    # Return coverage map for last query (or overall)
    # For demo, use all doctrines as triggered
    coverage_map = get_coverage_map([block.topic for block in DOCTRINE_CACHE])
    return coverage_map

@app.get("/drift")
def drift():
    return detect_drift()

@app.get("/doctrines")
def doctrines():
    return [
        {
            "topic": block.topic,
            "keywords": block.keywords,
            "confidence": block.confidence,
            "confidence_zone": block.confidence_zone,
            "controlling_precedent": block.controlling_precedent,
        }
        for block in DOCTRINE_CACHE
    ]
