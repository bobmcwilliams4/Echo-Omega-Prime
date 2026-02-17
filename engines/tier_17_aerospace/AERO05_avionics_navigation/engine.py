import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from loguru import logger
import hashlib
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set, Callable, Union
from enum import Enum, auto
from datetime import datetime, timedelta
import json
import threading

# =========================
# ENUMS
# =========================

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
    NAVIGATION = "NAVIGATION"
    COMMUNICATION = "COMMUNICATION"
    SURVEILLANCE = "SURVEILLANCE"
    AUTOPILOT = "AUTOPILOT"
    TERRAIN_AWARENESS = "TERRAIN_AWARENESS"
    DATA_LINK = "DATA_LINK"
    FLIGHT_MANAGEMENT = "FLIGHT_MANAGEMENT"
    AIR_DATA = "AIR_DATA"
    EMERGENCY_LOCATOR = "EMERGENCY_LOCATOR"
    RECORDING_SYSTEMS = "RECORDING_SYSTEMS"
    WEATHER = "WEATHER"
    COLLISION_AVOIDANCE = "COLLISION_AVOIDANCE"
    COCKPIT_DISPLAY = "COCKPIT_DISPLAY"
    ALTITUDE_MANAGEMENT = "ALTITUDE_MANAGEMENT"
    PERFORMANCE_MONITORING = "PERFORMANCE_MONITORING"

# =========================
# METRICS COLLECTOR
# =========================

class MetricsCollector:
    def __init__(self):
        self.query_log: List[Dict[str, Any]] = []
        self.error_log: List[Dict[str, Any]] = []
        self.lock = threading.Lock()
        self.doctrine_hits: Dict[str, int] = {}
        self.start_time = datetime.utcnow()

    def record_query(self, query_id: str, doctrine_ids: List[str], latency: float):
        with self.lock:
            self.query_log.append({
                "query_id": query_id,
                "doctrines": doctrine_ids,
                "latency": latency,
                "timestamp": datetime.utcnow().isoformat()
            })
            for doc_id in doctrine_ids:
                self.doctrine_hits[doc_id] = self.doctrine_hits.get(doc_id, 0) + 1

    def record_error(self, query_id: str, error: str):
        with self.lock:
            self.error_log.append({
                "query_id": query_id,
                "error": error,
                "timestamp": datetime.utcnow().isoformat()
            })

    def get_latency_stats(self) -> Dict[str, float]:
        with self.lock:
            latencies = [q["latency"] for q in self.query_log if "latency" in q]
            if not latencies:
                return {"avg": 0.0, "min": 0.0, "max": 0.0}
            return {
                "avg": sum(latencies) / len(latencies),
                "min": min(latencies),
                "max": max(latencies)
            }

    def get_doctrine_hit_rate(self) -> Dict[str, int]:
        with self.lock:
            return dict(self.doctrine_hits)

    def queries_last_hour(self) -> int:
        cutoff = datetime.utcnow() - timedelta(hours=1)
        with self.lock:
            return sum(1 for q in self.query_log if datetime.fromisoformat(q["timestamp"]) > cutoff)

metrics = MetricsCollector()

# =========================
# PYDANTIC MODELS
# =========================

class QueryRequest(BaseModel):
    scenario: str = Field(..., description="Aircraft avionics scenario or question")
    mode: ResponseMode = Field(..., description="Response mode")
    entity_type: str = Field(..., description="Type of avionics entity (e.g., FMS, VOR, TCAS)")
    complexity: int = Field(..., ge=1, le=5, description="Complexity level 1-5")

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

# =========================
# DOCTRINE CACHE
# =========================

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: Callable[[str, Dict[str, Any]], str]
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
    position_zone: PositionZone
    issue_category: IssueCategory

# =========================
# AUTHORITY HARDENING
# =========================

AUTHORITY_WEIGHTS = {
    "ICAO Annex 10": 10,
    "FAA AC 90-100A": 9,
    "EASA CS-ACNS": 8,
    "RTCA DO-229D": 8,
    "RTCA DO-178C": 7,
    "FAA AIM": 7,
    "EUROCONTROL NAV Spec": 7,
    "FAA TSO-C129a": 6,
    "FAA TSO-C145c": 6,
    "FAA TSO-C146c": 6,
    "FAA AC 20-138D": 6,
    "FAA Order 7110.65": 5,
    "ICAO Doc 8168": 5,
    "FAA AC 20-165B": 5,
    "RTCA DO-260B": 5,
    "FAA AC 25-11B": 5,
    "FAA AC 20-151B": 4,
    "FAA AC 20-152": 4,
    "ICAO Annex 6": 4,
    "FAA AC 20-153A": 4,
    "FAA AC 20-138C": 4,
    "FAA AC 25-7D": 3,
    "FAA AC 120-76D": 3,
    "FAA AC 20-130A": 3,
    "FAA AC 20-105B": 3,
    "FAA AC 20-138A": 2,
    "FAA AC 20-138B": 2,
    "FAA AC 20-138C": 2,
    "FAA AC 20-138D": 2,
}

def resolve_authority_conflict(authorities: List[str]) -> List[str]:
    weighted = sorted(authorities, key=lambda a: AUTHORITY_WEIGHTS.get(a, 0), reverse=True)
    return weighted[:3] if weighted else authorities

# =========================
# SEMANTIC NORMALIZATION
# =========================

SEMANTIC_MAP = {
    "VOR": "VHF Omnidirectional Range",
    "DME": "Distance Measuring Equipment",
    "ILS": "Instrument Landing System",
    "GPS": "Global Positioning System",
    "WAAS": "Wide Area Augmentation System",
    "SBAS": "Satellite-Based Augmentation System",
    "GBAS": "Ground-Based Augmentation System",
    "INS": "Inertial Navigation System",
    "FMS": "Flight Management System",
    "CDU": "Control Display Unit",
    "ADS-B": "Automatic Dependent Surveillance-Broadcast",
    "TCAS": "Traffic Collision Avoidance System",
    "EGPWS": "Enhanced Ground Proximity Warning System",
    "WXR": "Weather Radar",
    "HF": "High Frequency",
    "VHF": "Very High Frequency",
    "SATCOM": "Satellite Communication",
    "ACARS": "Aircraft Communications Addressing and Reporting System",
    "CPDLC": "Controller–Pilot Data Link Communications",
    "EFIS": "Electronic Flight Instrument System",
    "PFD": "Primary Flight Display",
    "ND": "Navigation Display",
    "EICAS": "Engine-Indicating and Crew-Alerting System",
    "ADC": "Air Data Computer",
    "Pitot": "Pitot-static system",
    "Radio Altimeter": "Radar Altimeter",
    "ELT": "Emergency Locator Transmitter",
    "CVR": "Cockpit Voice Recorder",
    "FDR": "Flight Data Recorder",
    "RNP": "Required Navigation Performance",
    "RVSM": "Reduced Vertical Separation Minimum",
    "RA": "Resolution Advisory",
    "DH": "Decision Height",
    "LNAV": "Lateral Navigation",
    "VNAV": "Vertical Navigation",
    "MDA": "Minimum Descent Altitude",
    "DA": "Decision Altitude",
}

def normalize_term(term: str) -> str:
    return SEMANTIC_MAP.get(term.strip().upper(), term)

# =========================
# EPISTEMIC GUARDRAILS
# =========================

BANNED_PHRASES = [
    "always", "never", "guaranteed", "cannot fail", "no risk", "perfectly", "impossible", "foolproof", "infallible",
    "absolutely", "completely safe", "zero error", "no chance", "certainly", "must", "will always"
]

def apply_epistemic_guardrails(text: str) -> str:
    for phrase in BANNED_PHRASES:
        text = text.replace(phrase, "[REDACTED]")
    return text

# =========================
# FACT FRAGILITY SCORING
# =========================

def score_fact_fragility(conclusion: str, authorities: List[str], counter_args: List[str]) -> Dict[str, float]:
    verifiability = min(1.0, len(authorities) / 3.0)
    recharacterization_risk = min(1.0, len(counter_args) / 5.0)
    testimony_dependence = 1.0 if "pilot report" in conclusion.lower() else 0.0
    return {
        "verifiability": verifiability,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence
    }

# =========================
# DOCTRINE BLOCKS
# =========================

def doctrine_vor_dme_ils(scenario: str, ctx: Dict[str, Any]) -> str:
    """
    Analyze the use of VOR, DME, and ILS for approach navigation.
    """
    lines = []
    lines.append("The VHF Omnidirectional Range (VOR), Distance Measuring Equipment (DME), and Instrument Landing System (ILS) are foundational radio navigation aids for precision and non-precision approaches.")
    lines.append("ILS provides both lateral (localizer) and vertical (glideslope) guidance, allowing aircraft to execute precision approaches down to published minima, typically with a Decision Height (DH) as low as 200 ft AGL for CAT I.")
    lines.append("VOR and DME enable non-precision approaches, with the DME arc procedure supporting curved path arrivals and missed approach point determination.")
    lines.append("Operational use requires verification of Morse code identifiers, cross-checking with FMS navigation, and monitoring of raw data for signal integrity.")
    lines.append("ILS critical area protection and frequency interference must be considered, especially in low visibility operations.")
    lines.append("Recent FAA and ICAO guidance (FAA AIM 1-1-9, ICAO Annex 10) emphasize the transition to satellite-based navigation, but legacy ground-based navaids remain essential for redundancy and contingency planning.")
    lines.append("Pilots must brief approach plates, ensure correct frequency selection, and monitor CDI/HSI indications for course deviations.")
    lines.append("Malfunctions such as false glideslope capture or localizer scalloping require immediate go-around and ATC notification.")
    lines.append("The integration of VOR/DME/ILS with autopilot and flight director systems enables coupled approaches, but mode awareness and annunciation are critical to avoid automation surprises.")
    lines.append("In summary, VOR, DME, and ILS remain vital for approach navigation, with operational procedures governed by ICAO Doc 8168 and FAA Order 7110.65.")
    return "\n".join(lines)

def doctrine_gps_waas_sbas_gbas(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("The Global Positioning System (GPS) forms the backbone of modern area navigation (RNAV), enhanced by augmentation systems such as WAAS (Wide Area Augmentation System), SBAS (Satellite-Based Augmentation System), and GBAS (Ground-Based Augmentation System).")
    lines.append("WAAS/SBAS provide integrity monitoring, correction signals, and enable Localizer Performance with Vertical guidance (LPV) approaches with minima comparable to ILS CAT I.")
    lines.append("GBAS, deployed at select airports, offers ground-based corrections for precision approaches (GLS), reducing signal-in-space errors and supporting CAT I/II/III operations.")
    lines.append("RTCA DO-229D, FAA AC 20-138D, and ICAO Annex 10 Vol I define performance requirements for GPS/SBAS/GBAS avionics, including time-to-alert, continuity, and accuracy thresholds.")
    lines.append("Pilots must ensure database currency, RAIM availability, and cross-check NOTAMs for outages.")
    lines.append("Approach activation in the FMS/CDU is required for correct sensitivity scaling and annunciation (e.g., 'LPV', 'LNAV/VNAV').")
    lines.append("In the event of loss of augmentation, reversion to LNAV-only minima or alternate navigation is mandated.")
    lines.append("Operational risk includes ionospheric anomalies, satellite geometry, and spoofing/jamming threats, mitigated by built-in integrity algorithms and ATC procedures.")
    return "\n".join(lines)

def doctrine_ins_kalman_filtering(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Inertial Navigation Systems (INS) utilize gyroscopes and accelerometers to compute aircraft position, velocity, and attitude independent of external references.")
    lines.append("Modern INS employ Kalman filtering to optimally blend inertial sensor data with aiding sources such as GPS, DME/DME, or VOR/DME, correcting for sensor drift and bias.")
    lines.append("Kalman filters recursively estimate the navigation state vector, minimizing mean squared error given sensor noise and dynamic modeling uncertainties.")
    lines.append("RTCA DO-178C and FAA AC 20-138D specify software assurance and integration requirements for INS/GNSS hybridization.")
    lines.append("Alignment procedures, including stationary initialization and latitude/longitude input, are critical for accurate navigation solution.")
    lines.append("INS failure modes include gyro bias, accelerometer scale factor errors, and misalignment, which are detected via built-in test and cross-check with external navaids.")
    lines.append("Flight crews must monitor navigation performance (e.g., RNP/ANP values) and be prepared to revert to radio navigation in the event of excessive drift or fault annunciation.")
    lines.append("INS is essential for oceanic and remote operations where ground-based navaids are unavailable, but periodic updates from GNSS or DME/DME are recommended to maintain accuracy.")
    return "\n".join(lines)

def doctrine_fms_cdu_operation(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("The Flight Management System (FMS) and its Control Display Unit (CDU) are central to aircraft navigation, performance management, and flight planning.")
    lines.append("Pilots interact with the CDU to enter flight plans, select procedures (SIDs, STARs, approaches), and manage lateral/vertical navigation modes.")
    lines.append("FMS integrates data from GNSS, INS, DME/DME, and VOR/DME, automatically sequencing waypoints and transitions.")
    lines.append("Database validity, ARINC 424 coding, and procedure selection are governed by FAA AC 20-153A and RTCA DO-200B.")
    lines.append("CDU entries must be cross-checked for route discontinuities, altitude constraints, and correct leg sequencing.")
    lines.append("Mode annunciation (LNAV, VNAV, etc.) and active waypoint monitoring are critical to avoid navigation errors.")
    lines.append("FMS-generated speeds and altitudes must be verified against ATC clearances and aircraft limitations.")
    lines.append("In the event of FMS failure, reversion to raw data navigation and manual flight plan management is required.")
    lines.append("Flight crews must brief FMS procedures, including missed approach programming and go-around logic.")
    return "\n".join(lines)

def doctrine_adsb_transponder_modes(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Automatic Dependent Surveillance-Broadcast (ADS-B) is a cornerstone of modern air traffic surveillance, providing position, velocity, and identification data to ATC and other aircraft.")
    lines.append("ADS-B Out is mandated in most controlled airspace, with avionics compliance defined by RTCA DO-260B and FAA TSO-C166b.")
    lines.append("Transponder modes (A, C, S) determine the type and fidelity of information transmitted; Mode S supports selective interrogation and extended squitter for ADS-B Out.")
    lines.append("Proper squawk code selection, IDENT function use, and altitude reporting are required per FAA AIM 4-1-20 and ICAO Annex 10.")
    lines.append("ADS-B In enables cockpit traffic displays and supports applications such as In-Trail Procedures and CDTI (Cockpit Display of Traffic Information).")
    lines.append("Failure modes include antenna blockage, power loss, and GPS position errors, which must be annunciated to the crew.")
    lines.append("ADS-B data is subject to integrity and latency checks, and pilots must revert to voice position reports if system failure occurs.")
    return "\n".join(lines)

def doctrine_tcas_resolution_advisories(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("The Traffic Collision Avoidance System (TCAS) provides real-time traffic advisories (TA) and resolution advisories (RA) to prevent midair collisions.")
    lines.append("TCAS II interrogates Mode C/S transponders, computing closure rates and vertical separation to issue climb/descend/maintain instructions.")
    lines.append("RTCA DO-185B and ICAO ACAS II standards govern system logic, alert thresholds, and pilot response protocols.")
    lines.append("Upon receiving an RA, pilots must respond immediately, disregarding ATC instructions if in conflict, and report the maneuver as soon as practicable.")
    lines.append("TCAS limitations include inability to detect non-transponder-equipped aircraft, reduced effectiveness in high-density airspace, and potential for nuisance alerts.")
    lines.append("Crew must monitor TCAS displays, maintain situational awareness, and be prepared for reversal or weakening of RAs based on intruder response.")
    lines.append("Post-encounter, pilots must file a report per ICAO Annex 13 and airline SMS procedures.")
    return "\n".join(lines)

def doctrine_egpws_terrain_awareness(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Enhanced Ground Proximity Warning System (EGPWS) provides predictive terrain and obstacle alerts using GPS position, aircraft configuration, and a terrain database.")
    lines.append("EGPWS modes include excessive descent rate, terrain closure, altitude loss after takeoff, unsafe terrain clearance, and premature descent to runway.")
    lines.append("RTCA DO-161A and FAA AC 25-23 define performance and installation requirements.")
    lines.append("Crew must respond to 'PULL UP' or 'TERRAIN' warnings with immediate maximum performance climb, unless visual contact confirms safety.")
    lines.append("False or nuisance alerts may occur in areas with incomplete terrain data or during abnormal flight profiles.")
    lines.append("EGPWS inhibits and test functions must be briefed and used per SOPs.")
    return "\n".join(lines)

def doctrine_wxr_interpretation(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Weather Radar (WXR) systems provide real-time detection of precipitation, turbulence, and windshear hazards.")
    lines.append("Pilots must interpret color-coded returns (green/yellow/red/magenta) and adjust tilt/attenuation to avoid ground clutter and shadowing.")
    lines.append("FAA AC 20-136 and RTCA DO-220A specify system capabilities and limitations.")
    lines.append("WXR cannot reliably detect dry hail, volcanic ash, or clear air turbulence; supplemental sources (PIREPs, ATIS, SIGMETs) are required.")
    lines.append("Crew must avoid flight into red/magenta returns and brief escape maneuvers.")
    lines.append("Automatic gain and predictive windshear modes enhance situational awareness but require pilot validation.")
    return "\n".join(lines)

def doctrine_hf_vhf_satcom(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Aircraft communication radios include High Frequency (HF), Very High Frequency (VHF), and Satellite Communication (SATCOM) systems.")
    lines.append("VHF is primary for line-of-sight ATC communications below FL300, with 8.33 kHz channel spacing per ICAO Annex 10.")
    lines.append("HF supports long-range communication via skywave propagation, subject to ionospheric conditions and requiring SELCAL for crew alerting.")
    lines.append("SATCOM provides global coverage, supporting voice and data link (e.g., CPDLC, ACARS) per ARINC 741/781.")
    lines.append("Crew must manage radio handovers, frequency selection, and maintain backup procedures in the event of system degradation.")
    lines.append("FAA AC 20-150B and ICAO Doc 9869 provide guidance on installation and operational use.")
    return "\n".join(lines)

def doctrine_datalink_acars_cpdlc(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Datalink systems such as ACARS (Aircraft Communications Addressing and Reporting System) and CPDLC (Controller–Pilot Data Link Communications) enable text-based ATC and airline communications.")
    lines.append("ACARS supports flight plan updates, weather, and maintenance messages; CPDLC enables clearances and instructions in oceanic/remote airspace.")
    lines.append("RTCA DO-219 and ICAO Doc 10037 define message formats, latency, and security requirements.")
    lines.append("Crew must verify message authenticity, respond to uplinked clearances, and revert to voice if datalink is unavailable.")
    lines.append("Message latency, delivery failures, and misrouting are operational risks requiring SOP mitigation.")
    lines.append("Datalink logs are retained for post-flight analysis and regulatory compliance.")
    return "\n".join(lines)

def doctrine_glass_cockpit_efis(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Glass cockpit avionics feature Electronic Flight Instrument System (EFIS) displays, including Primary Flight Display (PFD), Navigation Display (ND), and Engine-Indicating and Crew-Alerting System (EICAS).")
    lines.append("EFIS integrates attitude, airspeed, altitude, heading, and navigation data, reducing pilot workload and enhancing situational awareness.")
    lines.append("FAA AC 20-181 and RTCA DO-315 define display requirements, symbology, and failure annunciation.")
    lines.append("Crew must monitor display reversion, comparator warnings, and be prepared for partial panel operations.")
    lines.append("EICAS provides system status, alerts, and checklists, supporting abnormal and emergency procedures.")
    lines.append("Display management is critical during high workload phases and in the event of display unit failures.")
    return "\n".join(lines)

def doctrine_autopilot_flight_director(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Autopilot and flight director systems automate aircraft control, supporting lateral and vertical navigation, approach, and go-around modes.")
    lines.append("Mode selection, engagement logic, and annunciation are governed by FAA AC 25-10 and RTCA DO-178C.")
    lines.append("Servo actuators control pitch, roll, and yaw based on FMS or pilot input; flight director bars provide manual guidance cues.")
    lines.append("Crew must verify correct mode engagement, monitor for mode reversions, and be prepared for manual override in the event of system anomalies.")
    lines.append("Autopilot limitations include minimum engagement altitude, maximum bank/vertical speed, and failure annunciation.")
    lines.append("Automation surprise and mode confusion are mitigated by SOPs and crew resource management.")
    return "\n".join(lines)

def doctrine_air_data_computer(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("The Air Data Computer (ADC) processes pitot-static and temperature inputs to compute airspeed, altitude, and Mach number.")
    lines.append("Multiple ADCs provide redundancy; cross-checks and comparator warnings alert crew to discrepancies.")
    lines.append("FAA TSO-C106 and RTCA DO-160G specify performance, environmental, and failure detection requirements.")
    lines.append("Pitot/static blockages, leaks, or icing can result in erroneous indications and require alternate static source selection or unreliable airspeed procedures.")
    lines.append("ADC outputs feed autopilot, EFIS, and flight management systems, making integrity monitoring critical.")
    return "\n".join(lines)

def doctrine_radio_altimeter_dh(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Radio altimeters provide precise height above terrain, supporting approach and landing operations, especially in low visibility.")
    lines.append("Decision Height (DH) is set based on approach minima; automatic callouts and autopilot disconnects are triggered at DH.")
    lines.append("FAA TSO-C87 and RTCA DO-155 define system accuracy, installation, and interference protection.")
    lines.append("Crew must verify correct DH setting, monitor for spurious warnings, and be prepared for go-around if visual references are not acquired at DH.")
    lines.append("5G interference risk has prompted recent FAA ADs and operational mitigations.")
    return "\n".join(lines)

def doctrine_dme_arc_procedure(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("DME arc procedures require precise lateral navigation, maintaining a constant distance from a DME station while intercepting approach courses.")
    lines.append("FMS or raw data navigation may be used; pilots must monitor DME distance, bearing, and cross-track error.")
    lines.append("RTCA DO-236C and FAA Order 8260.58 provide procedural design and operational guidance.")
    lines.append("Wind correction, turn anticipation, and timely course intercept are critical for obstacle clearance.")
    lines.append("Crew must brief arc entry/exit points and be prepared for missed approach if navigation tolerances are exceeded.")
    return "\n".join(lines)

def doctrine_rnav_rnp_approaches(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("RNAV (Area Navigation) and RNP (Required Navigation Performance) approaches enable flexible, precise lateral and vertical paths, reducing workload and increasing airport accessibility.")
    lines.append("RNP approaches require onboard performance monitoring and alerting (RNP-AR), with specific crew training and equipment per FAA AC 90-101A and ICAO Doc 9613.")
    lines.append("FMS must be loaded with the correct procedure, and pilots must verify RNP/ANP values throughout the approach.")
    lines.append("Loss of RNP capability requires immediate go-around and ATC notification.")
    lines.append("Operational risks include database errors, GPS outages, and incorrect mode selection.")
    return "\n".join(lines)

def doctrine_rvsm(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Reduced Vertical Separation Minimum (RVSM) airspace allows 1000 ft vertical separation between FL290 and FL410, increasing capacity.")
    lines.append("Aircraft must be RVSM-approved, with dual altimetry, autopilot, and altitude alerting systems per FAA AC 91-85B and ICAO Annex 6.")
    lines.append("Preflight checks, in-flight monitoring, and post-flight reporting of altimetry errors are required.")
    lines.append("TCAS II and Mode S transponders support altitude reporting and monitoring.")
    lines.append("Loss of RVSM capability requires ATC notification and exit from RVSM airspace.")
    return "\n".join(lines)

def doctrine_elt(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Emergency Locator Transmitters (ELT) transmit distress signals on 406 MHz (COSPAS-SARSAT) and 121.5 MHz for search and rescue.")
    lines.append("FAA TSO-C126c and ICAO Annex 6 specify installation, activation, and maintenance requirements.")
    lines.append("ELT must activate automatically in a crash; manual activation and periodic testing are also required.")
    lines.append("False activations must be reported to ATC and SAR authorities.")
    lines.append("Crew must brief ELT location, operation, and post-crash procedures.")
    return "\n".join(lines)

def doctrine_cvr_fdr(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Cockpit Voice Recorder (CVR) and Flight Data Recorder (FDR) capture audio and flight parameters for accident investigation and safety monitoring.")
    lines.append("FAA TSO-C123c (CVR) and TSO-C124c (FDR), ICAO Annex 6, and EASA CS-25 define recording duration, crash survivability, and data download requirements.")
    lines.append("Crew must ensure preflight self-test, secure power supply, and post-event preservation of recorders.")
    lines.append("Tampering or disabling recorders is strictly prohibited and subject to regulatory action.")
    lines.append("Data is used for safety management, FOQA, and legal proceedings.")
    return "\n".join(lines)

def doctrine_performance_monitoring(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Avionics systems require continuous performance monitoring to ensure compliance with navigation, surveillance, and communication requirements.")
    lines.append("FMS, ADS-B, and RNP systems provide alerting when actual performance falls below required thresholds.")
    lines.append("Crew must monitor system messages, cross-check with raw data, and be prepared for reversionary procedures.")
    lines.append("FAA AC 20-138D and ICAO Doc 9613 specify monitoring and alerting protocols.")
    lines.append("Performance monitoring is essential for safe operation in PBN and RVSM airspace.")
    return "\n".join(lines)

def doctrine_altitude_management(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Altitude management integrates autopilot, air data, and transponder systems to maintain assigned flight levels and ensure separation.")
    lines.append("Altitude alerting, capture, and hold functions must be verified during preflight and monitored in flight.")
    lines.append("FAA AC 25-11B and RTCA DO-178C provide guidance on system integration and failure annunciation.")
    lines.append("Crew must cross-check altimeter settings, monitor for altitude deviations, and respond to alerts promptly.")
    lines.append("Loss of altitude control requires immediate manual intervention and ATC notification.")
    return "\n".join(lines)

def doctrine_surveillance_integrity(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Surveillance systems (ADS-B, Mode S, SSR) require integrity monitoring to ensure accurate position and identification reporting.")
    lines.append("RTCA DO-260B and ICAO Annex 10 define integrity, continuity, and latency requirements.")
    lines.append("Crew must monitor system status, respond to failure annunciations, and revert to procedural separation if surveillance is lost.")
    lines.append("Surveillance data feeds TCAS, ATC, and cockpit displays; errors can result in loss of separation or false alerts.")
    lines.append("Regular maintenance and software updates are required to maintain surveillance integrity.")
    return "\n".join(lines)

def doctrine_cockpit_display_management(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Cockpit display management involves configuration, reversion, and prioritization of EFIS, EICAS, and standby instruments.")
    lines.append("Display unit failures require prompt crew response, including switching to backup displays and referencing standby instruments.")
    lines.append("FAA AC 20-181 and RTCA DO-315 specify display redundancy and failure annunciation.")
    lines.append("Crew must brief display layouts, failure modes, and reversion procedures during preflight.")
    lines.append("Display management is critical during abnormal and emergency situations.")
    return "\n".join(lines)

def doctrine_emergency_communications(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Emergency communications utilize VHF 121.5 MHz, HF, and SATCOM distress channels to coordinate with ATC and SAR agencies.")
    lines.append("Crew must declare emergencies using standard phraseology and ensure backup radios are available.")
    lines.append("FAA AIM 6-3-1 and ICAO Annex 10 provide emergency communication protocols.")
    lines.append("Loss of primary comms requires squawking 7600 and following lost comm procedures.")
    lines.append("Datalink may supplement voice, but voice remains primary for time-critical emergencies.")
    return "\n".join(lines)

def doctrine_flight_plan_management(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Flight plan management integrates FMS, ATC clearances, and datalink updates to ensure compliance with operational requirements.")
    lines.append("Crew must verify flight plan entries, cross-check with ATC clearances, and update as required.")
    lines.append("FMS must be updated for reroutes, holds, and approach changes; errors can result in navigation deviations.")
    lines.append("Datalink and voice coordination are required for amendments and confirmations.")
    lines.append("Flight plan management is critical for safe and efficient operations.")
    return "\n".join(lines)

def doctrine_system_redundancy(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Avionics system redundancy ensures continued operation in the event of component failures.")
    lines.append("Critical systems (navigation, communication, surveillance) are duplicated and monitored for cross-channel discrepancies.")
    lines.append("FAA AC 25-16 and RTCA DO-178C define redundancy and failure management requirements.")
    lines.append("Crew must be familiar with reversionary modes and backup procedures.")
    lines.append("System redundancy is essential for ETOPS, oceanic, and remote operations.")
    return "\n".join(lines)

def doctrine_integrity_monitoring(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Integrity monitoring detects and alerts crew to navigation, surveillance, or communication system failures or degradations.")
    lines.append("FMS, GNSS, and ADS-B systems provide integrity messages and require crew response.")
    lines.append("RTCA DO-229D and FAA AC 20-138D specify integrity monitoring requirements.")
    lines.append("Crew must monitor for loss of integrity and revert to alternate procedures as necessary.")
    lines.append("Integrity monitoring is critical for PBN and RNP operations.")
    return "\n".join(lines)

def doctrine_navigation_database_management(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Navigation database management ensures FMS and avionics contain current, accurate procedures and waypoints.")
    lines.append("FAA AC 20-153A and RTCA DO-200B specify database update, validation, and integrity requirements.")
    lines.append("Crew must verify database currency before flight and cross-check loaded procedures.")
    lines.append("Database errors can result in navigation deviations and loss of RNP capability.")
    lines.append("Database management is critical for RNAV, RNP, and PBN operations.")
    return "\n".join(lines)

def doctrine_flight_data_monitoring(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Flight Data Monitoring (FDM) programs analyze FDR data to identify safety trends and operational risks.")
    lines.append("FAA AC 120-82 and ICAO Annex 6 recommend FDM for commercial operators.")
    lines.append("Data is de-identified and used for safety management, not punitive action.")
    lines.append("Crew must ensure FDR operation and report anomalies for analysis.")
    lines.append("FDM supports proactive safety improvements and regulatory compliance.")
    return "\n".join(lines)

def doctrine_autopilot_servo_modes(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Autopilot servo modes control pitch, roll, and yaw axes, supporting navigation, approach, and go-around functions.")
    lines.append("Mode selection and annunciation must be verified during preflight and monitored in flight.")
    lines.append("FAA AC 25-10 and RTCA DO-178C specify servo performance and failure detection.")
    lines.append("Crew must be prepared for manual override and monitor for servo runaway or disconnects.")
    lines.append("Servo mode management is critical for safe automation use.")
    return "\n".join(lines)

def doctrine_rnp_monitoring_alerting(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("RNP monitoring and alerting ensure navigation performance remains within required limits for PBN operations.")
    lines.append("FMS computes Actual Navigation Performance (ANP) and compares to RNP; alerts are generated if ANP exceeds RNP.")
    lines.append("FAA AC 90-101A and ICAO Doc 9613 specify monitoring and alerting protocols.")
    lines.append("Crew must respond to alerts by discontinuing RNP operations and notifying ATC.")
    lines.append("Continuous monitoring is essential for RNP-AR approaches and enroute segments.")
    return "\n".join(lines)

def doctrine_flight_director_modes(scenario: str, ctx: Dict[str, Any]) -> str:
    lines = []
    lines.append("Flight director modes provide visual guidance cues for manual flight, supporting navigation, approach, and go-around operations.")
    lines.append("Mode selection, engagement, and annunciation must be verified by the crew.")
    lines.append("FAA AC 25-10 and RTCA DO-178C specify mode logic and failure annunciation.")
    lines.append("Crew must monitor for mode confusion and be prepared for manual flight if guidance is lost.")
    lines.append("Flight director mode management is critical for safe automation use.")
    return "\n".join(lines)

DOCTRINE_BLOCKS: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="VOR DME ILS Approach Navigation",
        keywords=["VOR", "DME", "ILS", "approach", "navigation"],
        conclusion_template="VOR, DME, and ILS provide critical approach navigation capabilities. Their integration with autopilot and FMS ensures precision and redundancy, but require strict operational discipline.",
        reasoning_framework=doctrine_vor_dme_ils,
        key_factors=[
            "Signal integrity and identification",
            "Approach plate briefing",
            "Autopilot/FMS integration",
            "Mode awareness",
            "Contingency procedures"
        ],
        primary_authority=[
            "FAA AIM 1-1-9",
            "ICAO Annex 10",
            "FAA Order 7110.65"
        ],
        burden_holder="Flight Crew",
        adversary_position="Reliance on legacy navaids is obsolete; satellite navigation is sufficient.",
        counter_arguments=[
            "ILS susceptible to interference and false glideslope",
            "VOR/DME coverage limitations",
            "Transition to PBN reduces ground navaid reliance",
            "ILS critical area incursions",
            "Signal integrity monitoring required"
        ],
        resolution_strategy="Maintain dual navigation capability and adhere to approach procedures.",
        entity_scope=["VOR", "DME", "ILS", "Autopilot", "FMS"],
        confidence=0.97,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["ICAO Doc 8168", "FAA Order 8260.3D"],
        position_zone=PositionZone.PLANNING,
        issue_category=IssueCategory.NAVIGATION
    ),
    DoctrineBlock(
        topic="GPS WAAS SBAS GBAS Augmentation",
        keywords=["GPS", "WAAS", "SBAS", "GBAS", "augmentation"],
        conclusion_template="GPS navigation, augmented by WAAS, SBAS, and GBAS, enables high-integrity approaches and enroute navigation, but requires monitoring for outages and database validity.",
        reasoning_framework=doctrine_gps_waas_sbas_gbas,
        key_factors=[
            "RAIM/Integrity monitoring",
            "Database currency",
            "Augmentation availability",
            "Approach activation",
            "Signal interference risk"
        ],
        primary_authority=[
            "RTCA DO-229D",
            "FAA AC 20-138D",
            "ICAO Annex 10"
        ],
        burden_holder="Flight Crew",
        adversary_position="Augmentation is unnecessary with modern GPS constellations.",
        counter_arguments=[
            "Ionospheric anomalies affect GPS",
            "Database errors",
            "Augmentation outages",
            "Spoofing/jamming threats",
            "Reversion to LNAV minima"
        ],
        resolution_strategy="Monitor augmentation status and NOTAMs; revert to alternate navigation if required.",
        entity_scope=["GPS", "WAAS", "SBAS", "GBAS", "FMS"],
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA AC 20-138D", "RTCA DO-229D"],
        position_zone=PositionZone.PLANNING,
        issue_category=IssueCategory.NAVIGATION
    ),
    DoctrineBlock(
        topic="INS Inertial Navigation Kalman Filtering",
        keywords=["INS", "inertial", "Kalman", "filtering", "navigation"],
        conclusion_template="INS, enhanced by Kalman filtering, provides robust navigation in GNSS-denied environments, but requires periodic updates and cross-checks.",
        reasoning_framework=doctrine_ins_kalman_filtering,
        key_factors=[
            "Sensor drift and bias",
            "Kalman filter integration",
            "Alignment procedures",
            "Cross-check with external navaids",
            "Failure detection"
        ],
        primary_authority=[
            "RTCA DO-178C",
            "FAA AC 20-138D",
            "ICAO Annex 10"
        ],
        burden_holder="Flight Crew",
        adversary_position="INS is obsolete with GNSS coverage.",
        counter_arguments=[
            "Sensor drift over time",
            "Alignment errors",
            "INS failure modes",
            "GNSS jamming/spoofing",
            "Reversion to radio navigation"
        ],
        resolution_strategy="Periodic updates and cross-checks with GNSS or DME/DME.",
        entity_scope=["INS", "FMS", "GNSS"],
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["RTCA DO-178C", "FAA AC 20-138D"],
        position_zone=PositionZone.PLANNING,
        issue_category=IssueCategory.NAVIGATION
    ),
    DoctrineBlock(
        topic="FMS Flight Management System CDU Operation",
        keywords=["FMS", "CDU", "flight plan", "navigation", "database"],
        conclusion_template="FMS and CDU enable advanced flight planning and navigation management, but require strict database management and cross-checks.",
        reasoning_framework=doctrine_fms_cdu_operation,
        key_factors=[
            "Database validity",
            "Procedure selection",
            "Mode annunciation",
            "Cross-checks",
            "Reversion procedures"
        ],
        primary_authority=[
            "FAA AC 20-153A",
            "RTCA DO-200B",
            "FAA AIM"
        ],
        burden_holder="Flight Crew",
        adversary_position="FMS automation can lead to complacency and errors.",
        counter_arguments=[
            "Database errors",
            "Mode confusion",
            "Automation surprise",
            "FMS failure",
            "Manual reversion required"
        ],
        resolution_strategy="Strict cross-checks and procedure briefings.",
        entity_scope=["FMS", "CDU", "Autopilot"],
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA AC 20-153A", "RTCA DO-200B"],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.FLIGHT_MANAGEMENT
    ),
    DoctrineBlock(
        topic="ADS-B Surveillance Transponder Modes",
        keywords=["ADS-B", "transponder", "Mode S", "surveillance", "ATC"],
        conclusion_template="ADS-B and Mode S transponders provide essential surveillance data for ATC and TCAS, but require correct operation and monitoring.",
        reasoning_framework=doctrine_adsb_transponder_modes,
        key_factors=[
            "Transponder mode selection",
            "Squawk code management",
            "ADS-B Out compliance",
            "Failure annunciation",
            "Backup procedures"
        ],
        primary_authority=[
            "RTCA DO-260B",
            "FAA TSO-C166b",
            "ICAO Annex 10"
        ],
        burden_holder="Flight Crew",
        adversary_position="ADS-B is vulnerable to spoofing and jamming.",
        counter_arguments=[
            "Transponder failure",
            "ADS-B data errors",
            "Coverage limitations",
            "Integrity monitoring required",
            "Voice reporting fallback"
        ],
        resolution_strategy="Monitor system status and revert to voice reports if necessary.",
        entity_scope=["ADS-B", "Transponder", "TCAS"],
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["RTCA DO-260B", "FAA TSO-C166b"],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.SURVEILLANCE
    ),
    DoctrineBlock(
        topic="TCAS Collision Avoidance Resolution Advisories",
        keywords=["TCAS", "collision", "avoidance", "resolution", "advisory"],
        conclusion_template="TCAS provides real-time collision avoidance, but requires immediate pilot response and understanding of system limitations.",
        reasoning_framework=doctrine_tcas_resolution_advisories,
        key_factors=[
            "RA/TA logic",
            "Pilot response protocols",
            "System limitations",
            "Crew situational awareness",
            "Post-encounter reporting"
        ],
        primary_authority=[
            "RTCA DO-185B",
            "ICAO ACAS II",
            "FAA AIM"
        ],
        burden_holder="Flight Crew",
        adversary_position="TCAS can generate nuisance alerts and is not always reliable.",
        counter_arguments=[
            "Non-transponder aircraft",
            "High-density airspace limitations",
            "Nuisance alerts",
            "Reversal/weakening of RAs",
            "ATC coordination required"
        ],
        resolution_strategy="Immediate compliance with RAs and post-event reporting.",
        entity_scope=["TCAS", "Transponder", "ATC"],
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["RTCA DO-185B", "ICAO ACAS II"],
        position_zone=PositionZone.AUDIT,
        issue_category=IssueCategory.COLLISION_AVOIDANCE
    ),
    DoctrineBlock(
        topic="EGPWS Terrain Awareness",
        keywords=["EGPWS", "terrain", "awareness", "TAWS", "warning"],
        conclusion_template="EGPWS provides predictive terrain and obstacle alerts, requiring immediate crew response to warnings.",
        reasoning_framework=doctrine_egpws_terrain_awareness,
        key_factors=[
            "Terrain database",
            "Alerting modes",
            "Crew response protocols",
            "False/nuisance alerts",
            "System inhibits"
        ],
        primary_authority=[
            "RTCA DO-161A",
            "FAA AC 25-23",
            "ICAO Annex 6"
        ],
        burden_holder="Flight Crew",
        adversary_position="EGPWS can generate false alerts in certain terrain.",
        counter_arguments=[
            "Incomplete terrain data",
            "Abnormal flight profiles",
            "False/nuisance alerts",
            "Inhibit misuse",
            "Crew training required"
        ],
        resolution_strategy="Immediate climb on warning and SOP adherence.",
        entity_scope=["EGPWS", "TAWS", "FMS"],
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["RTCA DO-161A", "FAA AC 25-23"],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.TERRAIN_AWARENESS
    ),
    DoctrineBlock(
        topic="Weather Radar WXR Interpretation",
        keywords=["weather", "radar", "WXR", "precipitation", "turbulence"],
        conclusion_template="Weather radar interpretation is critical for hazard avoidance, but requires understanding of system limitations and correct operation.",
        reasoning_framework=doctrine_wxr_interpretation,
        key_factors=[
            "Color coding",
            "Tilt/attenuation management",
            "System limitations",
            "Supplemental sources",
            "Escape maneuvers"
        ],
        primary_authority=[
            "FAA AC 20-136",
            "RTCA DO-220A",
            "ICAO Annex 6"
        ],
        burden_holder="Flight Crew",
        adversary_position="WXR cannot detect all hazards and may provide false returns.",
        counter_arguments=[
            "Dry hail/ash undetectable",
            "Clutter/shadowing",
            "System failures",
            "Pilot misinterpretation",
            "Supplemental data required"
        ],
        resolution_strategy="Use multiple sources and avoid red/magenta returns.",
        entity_scope=["WXR", "EFIS", "FMS"],
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA AC 20-136", "RTCA DO-220A"],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.WEATHER
    ),
    DoctrineBlock(
        topic="HF VHF SATCOM Radio Systems",
        keywords=["HF", "VHF", "SATCOM", "radio", "communication"],
        conclusion_template="HF, VHF, and SATCOM radios provide layered communication capability, with each system supporting specific operational environments.",
        reasoning_framework=doctrine_hf_vhf_satcom,
        key_factors=[
            "Frequency selection",
            "Propagation characteristics",
            "SELCAL operation",
            "Backup procedures",
            "ATC handovers"
        ],
        primary_authority=[
            "FAA AC 20-150B",
            "ICAO Doc 9869",
            "ICAO Annex 10"
        ],
        burden_holder="Flight Crew",
        adversary_position="SATCOM is vulnerable to outages and not always available.",
        counter_arguments=[
            "Ionospheric effects on HF",
            "SATCOM coverage gaps",
            "Radio handover errors",
            "Backup comms required",
            "System failures"
        ],
        resolution_strategy="Maintain backup radios and monitor system status.",
        entity_scope=["HF", "VHF", "SATCOM"],
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA AC 20-150B", "ICAO Doc 9869"],
        position_zone=PositionZone.PLANNING,
        issue_category=IssueCategory.COMMUNICATION
    ),
    DoctrineBlock(
        topic="Datalink ACARS CPDLC",
        keywords=["datalink", "ACARS", "CPDLC", "ATC", "communication"],
        conclusion_template="Datalink systems enable efficient ATC and airline communication, but require verification and backup voice procedures.",
        reasoning_framework=doctrine_datalink_acars_cpdlc,
        key_factors=[
            "Message verification",
            "Latency management",
            "Backup voice procedures",
            "Security requirements",
            "Log retention"
        ],
        primary_authority=[
            "RTCA DO-219",
            "ICAO Doc 10037",
            "FAA AIM"
        ],
        burden_holder="Flight Crew",
        adversary_position="Datalink can be unreliable and subject to misrouting.",
        counter_arguments=[
            "Message latency",
            "Delivery failures",
            "Misrouting",
            "Security risks",
            "Voice fallback required"
        ],
        resolution_strategy="Verify messages and revert to voice if datalink fails.",
        entity_scope=["ACARS", "CPDLC", "SATCOM"],
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["RTCA DO-219", "ICAO Doc 10037"],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.DATA_LINK
    ),
    DoctrineBlock(
        topic="Glass Cockpit EFIS PFD ND EICAS",
        keywords=["glass cockpit", "EFIS", "PFD", "ND", "EICAS"],
        conclusion_template="Glass cockpit EFIS displays integrate critical flight data, but require crew proficiency in display management and failure response.",
        reasoning_framework=doctrine_glass_cockpit_efis,
        key_factors=[
            "Display integration",
            "Failure annunciation",
            "Comparator warnings",
            "Partial panel procedures",
            "Crew resource management"
        ],
        primary_authority=[
            "FAA AC 20-181",
            "RTCA DO-315",
            "ICAO Annex 6"
        ],
        burden_holder="Flight Crew",
        adversary_position="Display failures can lead to loss of situational awareness.",
        counter_arguments=[
            "Display unit failures",
            "Reversion procedures",
            "Comparator warnings",
            "Partial panel operation",
            "Crew training"
        ],
        resolution_strategy="Brief display layouts and manage failures per SOP.",
        entity_scope=["EFIS", "PFD", "ND", "EICAS"],
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA AC 20-181", "RTCA DO-315"],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.COCKPIT_DISPLAY
    ),
    DoctrineBlock(
        topic="Autopilot Flight Director Servo Modes",
        keywords=["autopilot", "flight director", "servo", "modes", "automation"],
        conclusion_template="Autopilot and flight director servo modes automate aircraft control, but require strict mode awareness and manual override capability.",
        reasoning_framework=doctrine_autopilot_flight_director,
        key_factors=[
            "Mode selection",
            "Engagement logic",
            "Manual override",
            "Failure annunciation",
            "Automation surprise mitigation"
        ],
        primary_authority=[
            "FAA AC 25-10",
            "RTCA DO-178C",
            "FAA AIM"
        ],
        burden_holder="Flight Crew",
        adversary_position="Automation can lead to mode confusion and errors.",
        counter_arguments=[
            "Mode confusion",
            "Servo failures",
            "Manual override required",
            "Automation surprise",
            "Crew training"
        ],
        resolution_strategy="Verify mode engagement and be prepared for manual flight.",
        entity_scope=["Autopilot", "Flight Director", "Servo"],
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA AC 25-10", "RTCA DO-178C"],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.AUTOPILOT
    ),
    DoctrineBlock(
        topic="Air Data Computer Pitot Static",
        keywords=["air data", "ADC", "pitot", "static", "altitude"],
        conclusion_template="The Air Data Computer processes pitot-static data for flight instruments and automation, requiring cross-checks and alternate procedures for failures.",
        reasoning_framework=doctrine_air_data_computer,
        key_factors=[
            "Redundancy",
            "Failure detection",
            "Pitot/static blockages",
            "Comparator warnings",
            "Alternate procedures"
        ],
        primary_authority=[
            "FAA TSO-C106",
            "RTCA DO-160G",
            "FAA AIM"
        ],
        burden_holder="Flight Crew",
        adversary_position="ADC failures can result in unreliable airspeed and altitude.",
        counter_arguments=[
            "Pitot/static icing",
            "System leaks",
            "Comparator warnings",
            "Unreliable airspeed procedures",
            "Manual reversion"
        ],
        resolution_strategy="Monitor for discrepancies and use alternate static source if needed.",
        entity_scope=["ADC", "Pitot", "Static"],
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA TSO-C106", "RTCA DO-160G"],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.AIR_DATA
    ),
    DoctrineBlock(
        topic="Radio Altimeter Decision Height",
        keywords=["radio altimeter", "decision height", "DH", "approach", "landing"],
        conclusion_template="Radio altimeters support approach and landing operations, but require correct DH setting and monitoring for interference.",
        reasoning_framework=doctrine_radio_altimeter_dh,
        key_factors=[
            "DH setting",
            "Automatic callouts",
            "Interference risk",
            "Go-around criteria",
            "System accuracy"
        ],
        primary_authority=[
            "FAA TSO-C87",
            "RTCA DO-155",
            "FAA AD 2021-23-12"
        ],
        burden_holder="Flight Crew",
        adversary_position="5G interference can degrade radio altimeter performance.",
        counter_arguments=[
            "Incorrect DH setting",
            "Spurious warnings",
            "Interference",
            "Go-around required",
            "Crew training"
        ],
        resolution_strategy="Verify DH setting and monitor for interference.",
        entity_scope=["Radio Altimeter", "Autopilot", "EFIS"],
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA TSO-C87", "FAA AD 2021-23-12"],
        position_zone=PositionZone.AUDIT,
        issue_category=IssueCategory.ALTITUDE_MANAGEMENT
    ),
    DoctrineBlock(
        topic="DME Arc Procedure Turns",
        keywords=["DME", "arc", "procedure", "turns", "navigation"],
        conclusion_template="DME arc procedures require precise navigation and cross-checks to ensure obstacle clearance and correct course intercept.",
        reasoning_framework=doctrine_dme_arc_procedure,
        key_factors=[
            "DME distance monitoring",
            "Turn anticipation",
            "Wind correction",
            "Course intercept",
            "Missed approach criteria"
        ],
        primary_authority=[
            "RTCA DO-236C",
            "FAA Order 8260.58",
            "ICAO Doc 8168"
        ],
        burden_holder="Flight Crew",
        adversary_position="DME arcs are obsolete with RNAV procedures.",
        counter_arguments=[
            "Navigation errors",
            "Database inaccuracies",
            "Wind effects",
            "Missed approach required",
            "Crew training"
        ],
        resolution_strategy="Monitor DME and cross-check with FMS.",
        entity_scope=["DME", "FMS", "Navigation Display"],
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["RTCA DO-236C", "FAA Order 8260.58"],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.NAVIGATION
    ),
    DoctrineBlock(
        topic="RNAV RNP Approaches",
        keywords=["RNAV", "RNP", "approach", "navigation", "performance"],
        conclusion_template="RNAV and RNP approaches require onboard monitoring and correct procedure loading, with immediate go-around if capability is lost.",
        reasoning_framework=doctrine_rnav_rnp_approaches,
        key_factors=[
            "RNP/ANP monitoring",
            "Procedure loading",
            "Loss of capability",
            "Database errors",
            "Crew training"
        ],
        primary_authority=[
            "FAA AC 90-101A",
            "ICAO Doc 9613",
            "FAA AIM"
        ],
        burden_holder="Flight Crew",
        adversary_position="Database errors can compromise RNP approaches.",
        counter_arguments=[
            "Loss of RNP capability",
            "Database errors",
            "GPS outages",
            "Incorrect mode selection",
            "Go-around required"
        ],
        resolution_strategy="Monitor RNP/ANP and discontinue if limits exceeded.",
        entity_scope=["FMS", "RNAV", "RNP"],
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA AC 90-101A", "ICAO Doc 9613"],
        position_zone=PositionZone.AUDIT,
        issue_category=IssueCategory.NAVIGATION
    ),
    DoctrineBlock(
        topic="RVSM Reduced Vertical Separation",
        keywords=["RVSM", "vertical separation", "altimetry", "autopilot", "monitoring"],
        conclusion_template="RVSM operations require dual altimetry, autopilot, and altitude alerting, with strict monitoring and reporting.",
        reasoning_framework=doctrine_rvsm,
        key_factors=[
            "RVSM approval",
            "Dual altimetry",
            "Autopilot",
            "Altitude alerting",
            "Error reporting"
        ],
        primary_authority=[
            "FAA AC 91-85B",
            "ICAO Annex 6",
            "FAA AIM"
        ],
        burden_holder="Flight Crew",
        adversary_position="Altimetry errors can compromise RVSM safety.",
        counter_arguments=[
            "Altimetry errors",
            "Loss of RVSM capability",
            "ATC notification required",
            "System failures",
            "Crew training"
        ],
        resolution_strategy="Monitor altimetry and notify ATC of errors.",
        entity_scope=["Autopilot", "Altimeter", "Transponder"],
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA AC 91-85B", "ICAO Annex 6"],
        position_zone=PositionZone.AUDIT,
        issue_category=IssueCategory.ALTITUDE_MANAGEMENT
    ),
    DoctrineBlock(
        topic="ELT Emergency Locator",
        keywords=["ELT", "emergency", "locator", "transmitter", "SAR"],
        conclusion_template="ELT provides critical distress signaling, but requires correct installation, activation, and maintenance.",
        reasoning_framework=doctrine_elt,
        key_factors=[
            "406 MHz transmission",
            "Automatic activation",
            "Maintenance",
            "False activation reporting",
            "Crew briefing"
        ],
        primary_authority=[
            "FAA TSO-C126c",
            "ICAO Annex 6",
            "FAA AIM"
        ],
        burden_holder="Flight Crew",
        adversary_position="False activations can waste SAR resources.",
        counter_arguments=[
            "False activations",
            "Maintenance lapses",
            "Activation failures",
            "Crew training",
            "SAR coordination"
        ],
        resolution_strategy="Verify ELT operation and report false activations.",
        entity_scope=["ELT", "SAR", "ATC"],
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA TSO-C126c", "ICAO Annex 6"],
        position_zone=PositionZone.AUDIT,
        issue_category=IssueCategory.EMERGENCY_LOCATOR
    ),
    DoctrineBlock(
        topic="Cockpit Voice Recorder Flight Data Recorder",
        keywords=["CVR", "FDR", "recorder", "accident", "investigation"],
        conclusion_template="CVR and FDR are essential for accident investigation and safety monitoring, requiring preflight checks and post-event preservation.",
        reasoning_framework=doctrine_cvr_fdr,
        key_factors=[
            "Recording duration",
            "Crash survivability",
            "Self-test",
            "Data preservation",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FAA TSO-C123c",
            "FAA TSO-C124c",
            "ICAO Annex 6"
        ],
        burden_holder="Flight Crew",
        adversary_position="Recorder failures can impede investigations.",
        counter_arguments=[
            "Recorder failures",
            "Tampering",
            "Data loss",
            "Regulatory action",
            "Crew training"
        ],
        resolution_strategy="Ensure operation and preserve recorders post-event.",
        entity_scope=["CVR", "FDR", "Accident Investigation"],
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA TSO-C123c", "FAA TSO-C124c"],
        position_zone=PositionZone.AUDIT,
        issue_category=IssueCategory.RECORDING_SYSTEMS
    ),
    DoctrineBlock(
        topic="Performance Monitoring",
        keywords=["performance", "monitoring", "FMS", "ADS-B", "RNP"],
        conclusion_template="Continuous performance monitoring is essential for compliance with navigation, surveillance, and communication requirements.",
        reasoning_framework=doctrine_performance_monitoring,
        key_factors=[
            "System alerting",
            "Cross-checks",
            "Reversionary procedures",
            "Monitoring protocols",
            "PBN/RVSM compliance"
        ],
        primary_authority=[
            "FAA AC 20-138D",
            "ICAO Doc 9613",
            "FAA AIM"
        ],
        burden_holder="Flight Crew",
        adversary_position="Performance monitoring can be overlooked in high workload.",
        counter_arguments=[
            "Alerting failures",
            "Crew inattention",
            "System errors",
            "Reversion required",
            "Training"
        ],
        resolution_strategy="Monitor alerts and cross-check with raw data.",
        entity_scope=["FMS", "ADS-B", "RNP"],
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA AC 20-138D", "ICAO Doc 9613"],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.PERFORMANCE_MONITORING
    ),
    DoctrineBlock(
        topic="Altitude Management",
        keywords=["altitude", "management", "autopilot", "alerting", "transponder"],
        conclusion_template="Altitude management integrates automation and alerting to maintain assigned flight levels and ensure separation.",
        reasoning_framework=doctrine_altitude_management,
        key_factors=[
            "Alerting functions",
            "Capture/hold modes",
            "Altimeter settings",
            "Deviation monitoring",
            "Manual intervention"
        ],
        primary_authority=[
            "FAA AC 25-11B",
            "RTCA DO-178C",
            "FAA AIM"
        ],
        burden_holder="Flight Crew",
        adversary_position="Automation can mask altitude deviations.",
        counter_arguments=[
            "Automation failures",
            "Altimeter errors",
            "Crew inattention",
            "Manual override required",
            "ATC notification"
        ],
        resolution_strategy="Cross-check altimeter and monitor for deviations.",
        entity_scope=["Autopilot", "Altimeter", "Transponder"],
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA AC 25-11B", "RTCA DO-178C"],
        position_zone=PositionZone.AUDIT,
        issue_category=IssueCategory.ALTITUDE_MANAGEMENT
    ),
    DoctrineBlock(
        topic="Surveillance Integrity Monitoring",
        keywords=["surveillance", "integrity", "monitoring", "ADS-B", "Mode S"],
        conclusion_template="Surveillance systems require integrity monitoring to ensure accurate reporting and safe separation.",
        reasoning_framework=doctrine_surveillance_integrity,
        key_factors=[
            "Integrity monitoring",
            "Failure annunciation",
            "Procedural separation",
            "Data feed errors",
            "Maintenance"
        ],
        primary_authority=[
            "RTCA DO-260B",
            "ICAO Annex 10",
            "FAA AIM"
        ],
        burden_holder="Flight Crew",
        adversary_position="Surveillance errors can result in loss of separation.",
        counter_arguments=[
            "System failures",
            "Data errors",
            "Procedural fallback",
            "Maintenance lapses",
            "Crew training"
        ],
        resolution_strategy="Monitor system status and revert to procedures if needed.",
        entity_scope=["ADS-B", "Mode S", "SSR"],
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["RTCA DO-260B", "ICAO Annex 10"],
        position_zone=PositionZone.AUDIT,
        issue_category=IssueCategory.SURVEILLANCE
    ),
    DoctrineBlock(
        topic="Cockpit Display Management",
        keywords=["cockpit", "display", "management", "EFIS", "EICAS"],
        conclusion_template="Cockpit display management is critical for situational awareness, requiring proficiency in reversion and failure procedures.",
        reasoning_framework=doctrine_cockpit_display_management,
        key_factors=[
            "Display configuration",
            "Reversion procedures",
            "Failure annunciation",
            "Briefing",
            "Abnormal situations"
        ],
        primary_authority=[
            "FAA AC 20-181",
            "RTCA DO-315",
            "FAA AIM"
        ],
        burden_holder="Flight Crew",
        adversary_position="Display failures can degrade situational awareness.",
        counter_arguments=[
            "Display unit failures",
            "Reversion errors",
            "Crew training",
            "Abnormal situations",
            "Briefing lapses"
        ],
        resolution_strategy="Brief display layouts and manage failures per SOP.",
        entity_scope=["EFIS", "EICAS", "Standby Instruments"],
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA AC 20-181", "RTCA DO-315"],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.COCKPIT_DISPLAY
    ),
    DoctrineBlock(
        topic="Emergency Communications",
        keywords=["emergency", "communications", "VHF", "HF", "SATCOM"],
        conclusion_template="Emergency communications require use of distress frequencies and backup radios, with adherence to standard protocols.",
        reasoning_framework=doctrine_emergency_communications,
        key_factors=[
            "Distress frequencies",
            "Backup radios",
            "Standard phraseology",
            "Lost comm procedures",
            "Voice/datalink integration"
        ],
        primary_authority=[
            "FAA AIM 6-3-1",
            "ICAO Annex 10",
            "FAA AIM"
        ],
        burden_holder="Flight Crew",
        adversary_position="Loss of comms can delay emergency response.",
        counter_arguments=[
            "Radio failures",
            "Lost comm procedures",
            "Backup radio use",
            "Voice/datalink integration",
            "Crew training"
        ],
        resolution_strategy="Use backup radios and follow lost comm procedures.",
        entity_scope=["VHF", "HF", "SATCOM"],
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA AIM 6-3-1", "ICAO Annex 10"],
        position_zone=PositionZone.AUDIT,
        issue_category=IssueCategory.COMMUNICATION
    ),
    DoctrineBlock(
        topic="Flight Plan Management",
        keywords=["flight plan", "management", "FMS", "ATC", "datalink"],
        conclusion_template="Flight plan management integrates FMS, ATC, and datalink, requiring verification and timely updates.",
        reasoning_framework=doctrine_flight_plan_management,
        key_factors=[
            "Flight plan verification",
            "ATC coordination",
            "FMS updates",
            "Datalink/voice integration",
            "Error management"
        ],
        primary_authority=[
            "FAA AIM",
            "ICAO Annex 6",
            "RTCA DO-200B"
        ],
        burden_holder="Flight Crew",
        adversary_position="Flight plan errors can result in navigation deviations.",
        counter_arguments=[
            "Entry errors",
            "ATC reroutes",
            "FMS update failures",
            "Datalink errors",
            "Crew training"
        ],
        resolution_strategy="Verify entries and coordinate with ATC.",
        entity_scope=["FMS", "ATC", "Datalink"],
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA AIM", "RTCA DO-200B"],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.FLIGHT_MANAGEMENT
    ),
    DoctrineBlock(
        topic="System Redundancy",
        keywords=["system", "redundancy", "backup", "failure", "ETOPS"],
        conclusion_template="System redundancy ensures continued operation in the event of failures, with crew proficiency in backup procedures essential.",
        reasoning_framework=doctrine_system_redundancy,
        key_factors=[
            "Redundant systems",
            "Failure management",
            "Reversionary modes",
            "Backup procedures",
            "ETOPS requirements"
        ],
        primary_authority=[
            "FAA AC 25-16",
            "RTCA DO-178C",
            "FAA AIM"
        ],
        burden_holder="Flight Crew",
        adversary_position="Redundancy can lead to complacency.",
        counter_arguments=[
            "Crew complacency",
            "Backup system failures",
            "Reversion errors",
            "ETOPS risks",
            "Training"
        ],
        resolution_strategy="Maintain proficiency in backup procedures.",
        entity_scope=["Navigation", "Communication", "Surveillance"],
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA AC 25-16", "RTCA DO-178C"],
        position_zone=PositionZone.PLANNING,
        issue_category=IssueCategory.PERFORMANCE_MONITORING
    ),
    DoctrineBlock(
        topic="Integrity Monitoring",
        keywords=["integrity", "monitoring", "FMS", "GNSS", "ADS-B"],
        conclusion_template="Integrity monitoring is critical for navigation, surveillance, and communication system safety.",
        reasoning_framework=doctrine_integrity_monitoring,
        key_factors=[
            "Integrity messages",
            "Crew response",
            "Procedural fallback",
            "System monitoring",
            "PBN/RNP compliance"
        ],
        primary_authority=[
            "RTCA DO-229D",
            "FAA AC 20-138D",
            "FAA AIM"
        ],
        burden_holder="Flight Crew",
        adversary_position="Integrity monitoring can be overlooked.",
        counter_arguments=[
            "Crew inattention",
            "System failures",
            "Procedural fallback",
            "Training",
            "Alerting errors"
        ],
        resolution_strategy="Monitor integrity and respond to alerts.",
        entity_scope=["FMS", "GNSS", "ADS-B"],
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["RTCA DO-229D", "FAA AC 20-138D"],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.PERFORMANCE_MONITORING
    ),
    DoctrineBlock(
        topic="Navigation Database Management",
        keywords=["navigation", "database", "FMS", "update", "integrity"],
        conclusion_template="Navigation database management is essential for safe and accurate FMS operation.",
        reasoning_framework=doctrine_navigation_database_management,
        key_factors=[
            "Database update",
            "Validation",
            "Integrity",
            "Procedure cross-check",
            "Error management"
        ],
        primary_authority=[
            "FAA AC 20-153A",
            "RTCA DO-200B",
            "FAA AIM"
        ],
        burden_holder="Flight Crew",
        adversary_position="Database errors can compromise navigation.",
        counter_arguments=[
            "Update failures",
            "Validation errors",
            "Procedure errors",
            "Crew training",
            "Regulatory compliance"
        ],
        resolution_strategy="Verify database currency and cross-check procedures.",
        entity_scope=["FMS", "Database", "Navigation"],
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA AC 20-153A", "RTCA DO-200B"],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.FLIGHT_MANAGEMENT
    ),
    DoctrineBlock(
        topic="Flight Data Monitoring",
        keywords=["flight data", "monitoring", "FDR", "safety", "analysis"],
        conclusion_template="Flight Data Monitoring supports proactive safety management and regulatory compliance.",
        reasoning_framework=doctrine_flight_data_monitoring,
        key_factors=[
            "Data analysis",
            "Safety trends",
            "De-identification",
            "Crew reporting",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FAA AC 120-82",
            "ICAO Annex 6",
            "FAA AIM"
        ],
        burden_holder="Operator",
        adversary_position="FDM can be misused for punitive action.",
        counter_arguments=[
            "Data misuse",
            "Crew trust",
            "Analysis errors",
            "Reporting lapses",
            "Regulatory oversight"
        ],
        resolution_strategy="Ensure data privacy and use for safety only.",
        entity_scope=["FDR", "Operator", "Regulator"],
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA AC 120-82", "ICAO Annex 6"],
        position_zone=PositionZone.AUDIT,
        issue_category=IssueCategory.RECORDING_SYSTEMS
    ),
    DoctrineBlock(
        topic="Autopilot Servo Modes",
        keywords=["autopilot", "servo", "modes", "manual override", "automation"],
        conclusion_template="Autopilot servo modes require strict mode awareness and readiness for manual override.",
        reasoning_framework=doctrine_autopilot_servo_modes,
        key_factors=[
            "Mode selection",
            "Annunciation",
            "Manual override",
            "Servo failures",
            "Crew training"
        ],
        primary_authority=[
            "FAA AC 25-10",
            "RTCA DO-178C",
            "FAA AIM"
        ],
        burden_holder="Flight Crew",
        adversary_position="Servo failures can result in loss of control.",
        counter_arguments=[
            "Servo failures",
            "Manual override required",
            "Mode confusion",
            "Automation surprise",
            "Training"
        ],
        resolution_strategy="Verify mode engagement and be prepared for manual flight.",
        entity_scope=["Autopilot", "Servo", "Flight Director"],
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA AC 25-10", "RTCA DO-178C"],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.AUTOPILOT
    ),
    DoctrineBlock(
        topic="RNP Monitoring and Alerting",
        keywords=["RNP", "monitoring", "alerting", "ANP", "FMS"],
        conclusion_template="RNP monitoring and alerting are essential for PBN operations, requiring crew response to alerts.",
        reasoning_framework=doctrine_rnp_monitoring_alerting,
        key_factors=[
            "ANP/RNP comparison",
            "Alerting",
            "Crew response",
            "Loss of capability",
            "Continuous monitoring"
        ],
        primary_authority=[
            "FAA AC 90-101A",
            "ICAO Doc 9613",
            "FAA AIM"
        ],
        burden_holder="Flight Crew",
        adversary_position="Alerting failures can compromise RNP operations.",
        counter_arguments=[
            "Alerting failures",
            "Crew inattention",
            "Loss of capability",
            "Procedural fallback",
            "Training"
        ],
        resolution_strategy="Monitor ANP/RNP and respond to alerts.",
        entity_scope=["FMS", "RNP", "Navigation"],
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA AC 90-101A", "ICAO Doc 9613"],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.PERFORMANCE_MONITORING
    ),
    DoctrineBlock(
        topic="Flight Director Modes",
        keywords=["flight director", "modes", "manual flight", "guidance", "automation"],
        conclusion_template="Flight director modes provide visual guidance for manual flight, requiring crew proficiency in mode management.",
        reasoning_framework=doctrine_flight_director_modes,
        key_factors=[
            "Mode selection",
            "Annunciation",
            "Manual flight",
            "Mode confusion",
            "Crew training"
        ],
        primary_authority=[
            "FAA AC 25-10",
            "RTCA DO-178C",
            "FAA AIM"
        ],
        burden_holder="Flight Crew",
        adversary_position="Mode confusion can lead to flight path deviations.",
        counter_arguments=[
            "Mode confusion",
            "Annunciation errors",
            "Manual flight required",
            "Automation surprise",
            "Training"
        ],
        resolution_strategy="Verify mode engagement and be prepared for manual flight.",
        entity_scope=["Flight Director", "Autopilot", "EFIS"],
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=["FAA AC 25-10", "RTCA DO-178C"],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.AUTOPILOT
    ),
]

# =========================
# THREE LAYER RESPONSE
# =========================

def doctrine_layer(scenario: str, mode: ResponseMode, entity_type: str, complexity: int) -> Tuple[DoctrineBlock, str]:
    for block in DOCTRINE_BLOCKS:
        if entity_type.upper() in (kw.upper() for kw in block.keywords):
            ctx = {"mode": mode, "complexity": complexity}
            reasoning = block.reasoning_framework(scenario, ctx)
            return block, reasoning
    return None, ""

def semantic_layer(scenario: str, entity_type: str) -> Tuple[DoctrineBlock, str]:
    scenario_norm = normalize_term(entity_type)
    for block in DOCTRINE_BLOCKS:
        if scenario_norm in block.entity_scope:
            ctx = {"mode": ResponseMode.FAST, "complexity": 1}
            reasoning = block.reasoning_framework(scenario, ctx)
            return block, reasoning
    return None, ""

def deep_analysis_layer(scenario: str, entity_type: str, complexity: int) -> Tuple[DoctrineBlock, str]:
    # Multi-doctrine decomposition
    hits = []
    for block in DOCTRINE_BLOCKS:
        if entity_type.upper() in (kw.upper() for kw in block.keywords):
            hits.append(block)
    if not hits:
        return None, ""
    # Issue categories
    categories = set(block.issue_category for block in hits)
    # Interaction DAG (simplified)
    dag = {block.topic: [b.topic for b in hits if b != block] for block in hits}
    # 8-step resolution
    lines = []
    for block in hits:
        ctx = {"mode": ResponseMode.MEMO, "complexity": complexity}
        lines.append(f"--- {block.topic} ---")
        lines.append(block.reasoning_framework(scenario, ctx))
        lines.append(f"Key Factors: {', '.join(block.key_factors)}")
        lines.append(f"Primary Authority: {', '.join(block.primary_authority)}")
        lines.append(f"Counter Arguments: {', '.join(block.counter_arguments)}")
        lines.append(f"Resolution Strategy: {block.resolution_strategy}")
    return hits[0], "\n".join(lines)

# =========================
# COVERAGE MAP
# =========================

def coverage_map(scenario: str, entity_type: str) -> Dict[str, Any]:
    triggered = []
    missed = []
    for block in DOCTRINE_BLOCKS:
        if entity_type.upper() in (kw.upper() for kw in block.keywords):
            triggered.append(block.topic)
        else:
            missed.append(block.topic)
    epistemic_gap = len(triggered) == 0
    return {
        "triggered": triggered,
        "missed": missed,
        "epistemic_gap": epistemic_gap
    }

# =========================
# DRIFT WATCHER
# =========================

DRIFT_BASELINE_HASH = hashlib.sha256(
    json.dumps([block.topic for block in DOCTRINE_BLOCKS]).encode("utf-8")
).hexdigest()

def drift_watcher() -> Dict[str, Any]:
    current_hash = hashlib.sha256(
        json.dumps([block.topic for block in DOCTRINE_BLOCKS]).encode("utf-8")
    ).hexdigest()
    drift = current_hash != DRIFT_BASELINE_HASH
    return {
        "baseline_hash": DRIFT_BASELINE_HASH,
        "current_hash": current_hash,
        "drift_detected": drift
    }

# =========================
# AUDIT TRAIL
# =========================

AUDIT_LOG_PATH = Path(__file__).parent / "aero05_audit.jsonl"
AUDIT_LOCK = threading.Lock()

def log_audit(entry: Dict[str, Any]):
    with AUDIT_LOCK:
        with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

# =========================
# DETERMINISM HASH
# =========================

def determinism_hash(response: Dict[str, Any]) -> str:
    canonical = json.dumps(response, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

# =========================
# FASTAPI APP
# =========================

app = FastAPI(
    title="ECHO OMEGA PRIME: Avionics & Navigation Systems Engine",
    description="Authoritative avionics analysis engine (AERO05)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def startup_event():
    logger.info("AERO05 Engine startup.")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("AERO05 Engine shutdown.")

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    query_id = str(uuid.uuid4())
    start_time = datetime.utcnow()
    try:
        # Layer 1: Doctrine cache
        block, reasoning = doctrine_layer(request.scenario, request.mode, request.entity_type, request.complexity)
        doctrine_ids = []
        if block:
            doctrine_ids.append(block.topic)
        else:
            # Layer 2: Semantic
            block, reasoning = semantic_layer(request.scenario, request.entity_type)
            if block:
                doctrine_ids.append(block.topic)
            else:
                # Layer 3: Deep analysis
                block, reasoning = deep_analysis_layer(request.scenario, request.entity_type, request.complexity)
                if block:
                    doctrine_ids.append(block.topic)
        if not block:
            raise HTTPException(status_code=404, detail="No relevant doctrine found for the scenario/entity.")
        # Epistemic guardrails
        primary_conclusion = apply_epistemic_guardrails(block.conclusion_template)
        reasoning_framework = apply_epistemic_guardrails(reasoning)
        # Authority hardening
        authorities = resolve_authority_conflict(block.primary_authority)
        # Fact fragility scoring
        fragility = score_fact_fragility(primary_conclusion, authorities, block.counter_arguments)
        # Determinism hash
        response_dict = {
            "engine_id": "AERO05",
            "query_id": query_id,
            "mode": request.mode,
            "confidence": block.confidence,
            "confidence_zone": block.confidence_zone,
            "position_zone": block.position_zone,
            "primary_conclusion": primary_conclusion,
            "reasoning_framework": reasoning_framework,
            "key_factors": block.key_factors,
            "primary_authority": authorities,
            "counter_arguments": block.counter_arguments,
            "resolution_strategy": block.resolution_strategy
        }
        response_dict["determinism_hash"] = determinism_hash(response_dict)
        latency = (datetime.utcnow() - start_time).total_seconds()
        metrics.record_query(query_id, doctrine_ids, latency)
        log_audit({
            "timestamp": datetime.utcnow().isoformat(),
            "query_id": query_id,
            "request": request.dict(),
            "response": response_dict,
            "doctrines": doctrine_ids,
            "latency": latency
        })
        return response_dict
    except Exception as e:
        logger.error(f"Query error: {e}")
        metrics.record_error(query_id, str(e))
        raise

@app.get("/health")
async def health():
    return {"status": "ok", "engine_id": "AERO05", "time": datetime.utcnow().isoformat()}

@app.get("/metrics")
async def metrics_endpoint():
    return {
        "latency": metrics.get_latency_stats(),
        "doctrine_hit_rate": metrics.get_doctrine_hit_rate(),
        "queries_last_hour": metrics.queries_last_hour()
    }

@app.get("/coverage")
async def coverage_endpoint(scenario: Optional[str] = "", entity_type: Optional[str] = ""):
    return coverage_map(scenario, entity_type)

@app.get("/drift")
async def drift_endpoint():
    return drift_watcher()

@app.get("/doctrines")
async def doctrines_endpoint():
    return [
        {
            "topic": block.topic,
            "keywords": block.keywords,
            "conclusion_template": block.conclusion_template,
            "key_factors": block.key_factors,
            "primary_authority": block.primary_authority,
            "confidence": block.confidence,
            "confidence_zone": block.confidence_zone,
            "position_zone": block.position_zone,
            "issue_category": block.issue_category
        }
        for block in DOCTRINE_BLOCKS
    ]
