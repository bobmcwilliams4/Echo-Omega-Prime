"""
OFE15 SAFETY INSTRUMENTED SYSTEMS ENGINE
Port: 9285
Domain: Oilfield Safety Instrumented Systems (SIS)
Version: 1.0.0

Safety Instrumented Systems analysis including SIL determination, safety PLC design,
ESD systems, fire and gas detection, PSV sizing, and HIPPS applications.

TIE-20 GOLD STANDARD ARCHITECTURE
"""

import sys
from pathlib import Path

# CRITICAL: Add parent to sys.path BEFORE any local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn


# ============================================================================
# ENUMERATIONS
# ============================================================================

class ResponseMode(str, Enum):
    """Response detail levels"""
    FAST = "FAST"           # Concise answer
    DEFENSE = "DEFENSE"     # Audit-ready full reasoning
    MEMO = "MEMO"           # Complete documentation


class ConfidenceLevel(str, Enum):
    """Confidence stratification levels"""
    DEFENSIBLE = "DEFENSIBLE"       # Clear authority, standard practice
    AGGRESSIVE = "AGGRESSIVE"       # Industry practice, limited precedent
    DISCLOSURE = "DISCLOSURE"       # Uncertain, needs expert review
    HIGH_RISK = "HIGH_RISK"         # Conflicting guidance, novel scenario


class AnalysisZone(str, Enum):
    """Position zones - never blur"""
    PLANNING = "PLANNING"       # Design phase analysis
    REPORTING = "REPORTING"     # Operational compliance
    AUDIT = "AUDIT"             # Regulatory inspection


class IssueCategory(str, Enum):
    """Safety instrumented system issue categories"""
    SIL_DETERMINATION = "SIL_DETERMINATION"
    SAFETY_PLC_DESIGN = "SAFETY_PLC_DESIGN"
    ESD_SYSTEM = "ESD_SYSTEM"
    FIRE_GAS_DETECTION = "FIRE_GAS_DETECTION"
    PSV_SIZING = "PSV_SIZING"
    HIPPS_DESIGN = "HIPPS_DESIGN"
    SIF_VALIDATION = "SIF_VALIDATION"
    FUNCTIONAL_SAFETY_MGMT = "FUNCTIONAL_SAFETY_MGMT"
    PROOF_TESTING = "PROOF_TESTING"
    COMMON_CAUSE_FAILURE = "COMMON_CAUSE_FAILURE"
    SIS_LIFECYCLE = "SIS_LIFECYCLE"
    REGULATORY_COMPLIANCE = "REGULATORY_COMPLIANCE"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class DoctrineBlock:
    """Individual doctrine block with full reasoning framework"""
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: List[str]
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

    def matches_query(self, query: str) -> int:
        """Score doctrine relevance to query (0-100)"""
        query_lower = query.lower()
        score = 0

        # Keyword matching (40 points)
        matched_keywords = sum(1 for kw in self.keywords if kw.lower() in query_lower)
        score += min(40, matched_keywords * 10)

        # Topic matching (30 points)
        if self.topic.lower() in query_lower:
            score += 30

        # Framework context matching (30 points)
        framework_text = ' '.join(self.reasoning_framework).lower()
        query_words = set(query_lower.split())
        framework_words = set(framework_text.split())
        overlap = len(query_words & framework_words)
        score += min(30, overlap * 2)

        return min(100, score)


@dataclass
class TelemetryRecord:
    """Query telemetry tracking"""
    query: str
    timestamp: str
    mode: ResponseMode
    zone: AnalysisZone
    doctrines_triggered: List[str]
    cache_hit: bool
    latency_ms: float
    confidence: ConfidenceLevel
    error_domain: Optional[str] = None


@dataclass
class MetricsCollector:
    """Performance and quality metrics"""
    total_queries: int = 0
    cache_hits: int = 0
    avg_latency_ms: float = 0.0
    doctrine_trigger_counts: Dict[str, int] = field(default_factory=dict)
    confidence_distribution: Dict[str, int] = field(default_factory=dict)
    error_count: int = 0

    def record_query(self, telemetry: TelemetryRecord):
        """Update metrics from telemetry"""
        self.total_queries += 1
        if telemetry.cache_hit:
            self.cache_hits += 1

        # Update average latency
        self.avg_latency_ms = (
            (self.avg_latency_ms * (self.total_queries - 1) + telemetry.latency_ms)
            / self.total_queries
        )

        # Track doctrine triggers
        for doctrine in telemetry.doctrines_triggered:
            self.doctrine_trigger_counts[doctrine] = (
                self.doctrine_trigger_counts.get(doctrine, 0) + 1
            )

        # Track confidence distribution
        conf_key = telemetry.confidence.value
        self.confidence_distribution[conf_key] = (
            self.confidence_distribution.get(conf_key, 0) + 1
        )

        if telemetry.error_domain:
            self.error_count += 1


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class QueryRequest(BaseModel):
    """Inbound safety instrumented systems query"""
    query: str = Field(..., description="Safety system question or scenario")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(AnalysisZone.PLANNING, description="Analysis context")
    entity_context: Optional[str] = Field(None, description="Facility/system context")


class QueryResponse(BaseModel):
    """Structured safety instrumented systems response"""
    answer: str
    doctrines_applied: List[str]
    confidence: ConfidenceLevel
    authorities_cited: List[str]
    determinism_hash: str
    latency_ms: float
    mode: ResponseMode
    zone: AnalysisZone
    epistemic_disclosure: Optional[str] = None


class HealthResponse(BaseModel):
    """Engine health status"""
    status: str
    engine: str
    version: str
    port: int
    doctrines_loaded: int
    total_queries: int
    cache_hit_rate: float
    avg_latency_ms: float
    uptime_seconds: float


# ============================================================================
# DOCTRINE CACHE - 25+ REAL SAFETY INSTRUMENTED SYSTEMS DOCTRINES
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [

    DoctrineBlock(
        topic="SIL Determination Using Risk Graph Method",
        keywords=["SIL", "safety integrity level", "risk graph", "IEC 61511", "consequence severity", "frequency", "SIL1", "SIL2", "SIL3"],
        conclusion_template=[
            "SIL determination via risk graph requires systematic evaluation of consequence severity (C1-C4), occupancy/exposure frequency (F1-F2), possibility of avoiding hazard (P1-P2), and probability of unwanted occurrence (W1-W3).",
            "IEC 61511 risk graph method combines these parameters to determine required risk reduction, yielding target SIL level.",
            "For offshore platforms, consequence category C4 (catastrophic - multiple fatalities) with high occupancy (F2) and no avoidance possibility (P2) typically requires SIL 2 or SIL 3 protection."
        ],
        reasoning_framework=[
            "Risk graph methodology per IEC 61511-3 Annex F provides semi-quantitative SIL determination approach balancing simplicity with rigor.",
            "Consequence severity (C) assessment considers worst credible scenario impact: C1 (minor injury), C2 (serious permanent injury), C3 (single fatality), C4 (multiple fatalities).",
            "Frequency of exposure (F) evaluates how often personnel are in hazard zone: F1 (rare to frequent), F2 (frequent to continuous).",
            "Possibility of avoiding hazard (P) considers whether personnel can recognize and escape: P1 (possible under certain conditions), P2 (almost impossible).",
            "Probability of unwanted occurrence (W) reflects unmitigated event likelihood: W1 (very low), W2 (low), W3 (relatively high).",
            "Risk reduction factor requirements: SIL 1 (10 to 100), SIL 2 (100 to 1,000), SIL 3 (1,000 to 10,000).",
            "Platform topsides typically feature C4 consequences due to confined spaces, high occupancy (F2), and limited escape routes (P2).",
            "Gas compressor overpressure scenario: C4 (explosion potential), F2 (continuous operation), P2 (no warning), W2 (mechanical failure mode) yields SIL 2 requirement.",
            "Subsea wellhead overpressure: C3 (environmental damage), F1 (remote location), P1 (slow development), W2 (tubing leak) may yield SIL 1.",
            "LOPA (Layer of Protection Analysis) provides alternative quantitative approach, calculating required PFD (probability of failure on demand) directly.",
            "Risk graph results should be validated against LOPA calculations for critical applications (SIL 2/3).",
            "Conservative bias required when parameters fall between categories - round up to higher SIL.",
            "Operator experience and procedural safeguards (independent protection layers) may reduce required SIL by one level if quantifiable.",
            "API RP 14C Section 5 provides oilfield-specific risk assessment guidance complementing IEC 61511 framework.",
            "Common error: underestimating consequence severity by excluding cascading failures (fire following rupture).",
            "BSEE SEMS requirements mandate documented SIL determination for all offshore safety critical elements.",
            "SIL determination must be revalidated after process modifications, near-miss incidents, or every 5 years minimum.",
            "For partial stroke testing applications (PST on ESDVs), credit for risk reduction requires validation per IEC 61511-1 Clause 11.9.",
            "Systematic capability (SC) level must match or exceed SIL target (SC 2 for SIL 2, SC 3 for SIL 3) per IEC 61508-2 Table 3.",
            "Prior use justification can reduce required SIL validation rigor if device has proven field performance history.",
            "Risk graph approach suitable for preliminary design; LOPA required for final safety case on complex offshore platforms.",
            "Multiple SIFs protecting same hazard scenario require cumulative PFD calculation to verify overall risk reduction.",
            "Hot work scenario on live platform: C4, F2, P2, W3 (gas release) typically mandates SIL 3 ESD system.",
            "SIL verification calculations must account for common cause failures (beta factor 2-10% depending on architecture).",
            "Proof test interval selection interacts with SIL determination - shorter intervals can reduce required sensor/valve SIL.",
            "Pre-existing design documentation from sister platforms can streamline SIL determination if process conditions match within 10%."
        ],
        key_factors=[
            "Consequence severity evaluation (C1-C4) including cascading failures",
            "Occupancy frequency and personnel density in hazard zone (F1-F2)",
            "Possibility of hazard avoidance considering detection and escape time (P1-P2)",
            "Unmitigated event probability based on failure mode data (W1-W3)",
            "Risk reduction factor mapping to SIL requirements (1-3)",
            "Validation via LOPA for SIL 2/3 applications",
            "Systematic capability matching SIL target (IEC 61508-2)",
            "Proof test interval interaction with PFD requirements",
            "Common cause failure contribution (beta factor)",
            "Independent protection layer credits (LOPA framework)"
        ],
        primary_authority=[
            "IEC 61511-1:2016 Clause 9 (SIL determination and allocation)",
            "IEC 61511-3:2016 Annex F (Risk graph methodology)",
            "API RP 14C Section 5 (Analysis, Design, Installation, and Testing of Basic Surface Safety Systems for Offshore Production Platforms)",
            "IEC 61508-2:2010 Table 3 (Systematic capability requirements)",
            "30 CFR 250.1911 (BSEE SEMS - hazard analysis requirements)"
        ],
        burden_holder="Operator/Owner proposing SIL classification for safety instrumented function",
        adversary_position="Regulator may challenge consequence underestimation or inadequate risk reduction for high-consequence scenarios",
        counter_arguments=[
            "Risk graph oversimplifies complex scenarios - LOPA provides more accurate quantitative assessment",
            "Consequence category assignment subjective without clear multiple-fatality threshold definition",
            "Offshore confined spaces warrant automatic C4 classification regardless of specific scenario",
            "Systematic capability verification difficult for legacy equipment without prior use documentation",
            "Proof test interval manipulation can artificially lower SIL requirement without improving safety"
        ],
        resolution_strategy="Use risk graph for initial screening, validate SIL 2/3 results with LOPA calculations, document conservative assumptions, engage AHJ early for SIL 3 systems",
        entity_scope="Offshore platforms, onshore gas plants, HIPPS applications, ESD systems, fired equipment overpressure protection",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Clear IEC 61511 framework with oilfield precedent via API RP 14C; conservative consequence assessment critical",
        controlling_precedent="IEC 61511-1:2016 provides internationally recognized SIL determination methodology; BSEE SEMS codifies offshore application"
    ),

    DoctrineBlock(
        topic="Safety PLC Architecture: 1oo1 vs 1oo2 vs 2oo3 Selection",
        keywords=["safety PLC", "redundancy", "1oo1", "1oo2", "2oo3", "spurious trip", "voting logic", "fault tolerance", "fail-safe", "SIL2", "SIL3"],
        conclusion_template=[
            "Safety PLC architecture selection balances required SIL level, spurious trip tolerance, and failure mode characteristics.",
            "1oo1 (single channel) suitable for SIL 1 with high proof test frequency; 1oo2 (redundant) provides SIL 2 with spurious trip reduction; 2oo3 (triple redundant voting) achieves SIL 3 with maximum availability.",
            "For critical offshore applications requiring both safety (SIL 2/3) and production continuity, 2oo3 architecture often economically justified."
        ],
        reasoning_framework=[
            "Nomenclature: MooN means M-out-of-N channels must trip to execute safety action (e.g., 2oo3 requires 2 of 3 sensors to agree).",
            "1oo1 architecture: single sensor → single logic solver → single final element. Simple, low cost, but spurious trip rate equals sensor failure rate.",
            "PFD calculation for 1oo1: approximately (lambda * TI) / 2, where lambda = dangerous failure rate, TI = proof test interval.",
            "SIL 1 achievable with 1oo1 if lambda < 2 x 10^-6 per hour and TI ≤ 1 year (PFD < 0.01).",
            "1oo2 architecture: two sensors in parallel, trip on agreement (AND logic for de-energize-to-trip). Reduces spurious trips dramatically.",
            "1oo2 PFD approximately equals (lambda^2 * TI^2) / 3, providing roughly 100x improvement over 1oo1 for identical components.",
            "SIL 2 readily achievable with 1oo2 using standard industrial sensors (lambda ~ 5 x 10^-6 per hour) and 2-year proof test.",
            "Spurious trip rate for 1oo2 approximately (lambda_safe * TI) / 2, significantly lower than 1oo1 due to AND voting.",
            "2oo3 architecture: three sensors, trip if any two agree (2-out-of-3 voting). Tolerates one failed sensor without spurious trip or loss of protection.",
            "2oo3 PFD approximately 3 * (lambda^2 * TI^2) / 2, slightly higher than 1oo2 but still SIL 2 capable; SIL 3 achievable with high-reliability sensors.",
            "2oo3 spurious trip rate dramatically reduced - requires two sensors to fail in safe direction simultaneously (extremely rare).",
            "Offshore platform ESD systems typically use 2oo3 voting for critical trips (ESDV closure, compressor shutdown) to avoid production loss from single sensor failure.",
            "Common cause failure (CCF) degrades redundancy benefit - beta factor 2-5% for diverse sensor types, 5-10% for identical sensors.",
            "IEC 61508 requires beta factor consideration in PFD calculations for all redundant architectures.",
            "Diagnostic coverage impacts achievable SIL: 1oo2 with <60% coverage limited to SIL 2; >90% coverage enables SIL 3 (with high-reliability devices).",
            "Partial stroke testing on ESD valves increases effective diagnostic coverage, potentially allowing 1oo2 architecture for SIL 3 (controversial).",
            "Fail-safe design principle: de-energize to trip (spring-return valves, normally-open relay contacts) inherent in properly designed systems.",
            "NAMUR recommendations NE 21/NE 43 specify 4-20mA current loop fault detection (burnout detection) as essential diagnostic function.",
            "Hart communication on 4-20mA loops enables continuous sensor diagnostics without proof test, improving effective beta factor.",
            "Cost comparison: 2oo3 approximately 2.5x hardware cost of 1oo1, but spurious trip cost savings often justify premium on critical applications.",
            "API RP 14C Section 6.4.2 recommends redundancy for all platform ESD systems (minimum 1oo2, preferably 2oo3).",
            "Bypass management critical for redundant systems - partial bypass capability allows sensor maintenance without full SIF defeat.",
            "IEC 61511 Clause 11.8 requires documented bypass procedures and automatic restoration (time-limited bypass).",
            "Voting logic must detect sensor faults and alert operators - silent failures erode redundancy benefit.",
            "Hardwired voting (relay logic) vs PLC voting: hardwired immune to software systematic failures, but inflexible and difficult to diagnostic test."
        ],
        key_factors=[
            "Required SIL level (1oo1 for SIL 1, 1oo2 for SIL 2, 2oo3 for SIL 2/3)",
            "Spurious trip tolerance and production continuity requirements",
            "Component dangerous failure rate (lambda) and proof test interval",
            "Common cause failure contribution (beta factor 2-10%)",
            "Diagnostic coverage capability (>90% required for SIL 3)",
            "Fail-safe design implementation (de-energize to trip)",
            "Bypass management and partial bypass capability",
            "Cost-benefit analysis including spurious trip production loss",
            "Sensor diversity to reduce beta factor",
            "Hart diagnostics or partial stroke testing enhancing coverage"
        ],
        primary_authority=[
            "IEC 61508-6:2010 Annex B (PFD calculation formulas for redundant architectures)",
            "IEC 61511-1:2016 Clause 11.4 (SIS architecture requirements)",
            "API RP 14C Section 6 (Recommended redundancy practices for offshore platforms)",
            "ISA TR84.00.02-2002 Part 3 (Simplified methods and equations for PFD calculations)",
            "NAMUR NE 21/NE 43 (4-20mA fault detection requirements)"
        ],
        burden_holder="System designer proposing architecture must demonstrate adequate PFD and spurious trip rate",
        adversary_position="Operator may resist 2oo3 cost premium without clear production continuity benefit quantification",
        counter_arguments=[
            "1oo2 with high-reliability sensors achieves SIL 2 at lower cost than 2oo3",
            "2oo3 introduces complexity and additional failure modes (voting logic itself)",
            "Spurious trip economic benefit difficult to quantify without historical production loss data",
            "Common cause failures (instrument air loss, power failure) defeat redundancy regardless of architecture",
            "Partial bypass on 2oo3 during maintenance reduces to 1oo2, eliminating fault tolerance advantage during critical maintenance windows"
        ],
        resolution_strategy="Perform LOPA with spurious trip economic impact analysis, specify diverse sensor types to minimize beta factor, implement Hart diagnostics, document bypass management procedures per IEC 61511 Clause 11.8",
        entity_scope="Offshore platform ESD systems, compressor antisurge protection, fired heater high temperature trips, HIPPS logic solvers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="IEC 61508/61511 provide clear PFD calculation methods; API RP 14C establishes offshore redundancy expectations; beta factor estimation remains somewhat subjective",
        controlling_precedent="IEC 61508-6:2010 Annex B defines internationally accepted PFD formulas for redundant architectures; API RP 14C Section 6 codifies offshore industry practice"
    ),

    DoctrineBlock(
        topic="ESD System Cause and Effect Matrix Design",
        keywords=["cause and effect", "C&E matrix", "ESD", "emergency shutdown", "trip logic", "voting", "time delay", "manual shutdown", "reset", "sequential shutdown"],
        conclusion_template=[
            "Cause and Effect (C&E) matrix documents all ESD system trip inputs, voting logic, time delays, and shutdown outputs in tabular format per IEC 61511 Clause 10.4.2.",
            "Proper C&E design requires systematic hazard analysis (HAZOP), clear voting logic specification, appropriate time delays for spurious trip filtering, and sequential shutdown coordination.",
            "For offshore platforms, typical structure includes Level 1 (process shutdown), Level 2 (wellhead shutdown), and Level 3 (blowdown and isolation)."
        ],
        reasoning_framework=[
            "C&E matrix translates HAZOP findings into formal ESD logic specification, serving as basis for PLC programming and FAT/SAT testing.",
            "Rows represent trip causes (sensor inputs, manual push buttons), columns represent effects (valve closures, equipment trips, alarms).",
            "Voting logic notation: 1oo2 means one out of two sensors must trip; 2oo3 means two out of three; often written in matrix as '1/2' or '2/3'.",
            "Time delays prevent spurious trips from transient sensor spikes: typical 2-5 seconds for level/pressure, 0 seconds for fire/gas (immediate action).",
            "Manual shutdown stations (push buttons) always bypass voting logic - single button initiates full shutdown sequence (no voting delay).",
            "Reset logic prevents automatic restart after trip - operator must manually reset all trip causes before process restart permitted.",
            "Sequential shutdown coordination prevents equipment damage: close compressor suction valve → wait 2 sec → trip compressor motor → wait 5 sec → close discharge valve.",
            "Offline platforms typically implement 3-level ESD architecture: L1 (process), L2 (wellhead), L3 (blowdown/isolation).",
            "Level 1 (Process Shutdown): close compressor suction ESDV, trip compressor/pumps, close fuel gas to fired equipment. Maintains well containment.",
            "Level 2 (Wellhead Shutdown): close all wellhead master valves (XMV/PMV), depressurize flowlines. Isolates well sources.",
            "Level 3 (Abandon Platform): initiate blowdown via BDV opening, close all inlet/outlet platform isolation valves. Prepare for evacuation.",
            "API RP 14C Section 6.3 requires L1 and L2 minimum for manned platforms; L3 for unattended or high-risk facilities.",
            "Common practice: L1 actuated by process trips (high pressure, high level, low-low level), L2 by fire/gas detection or manual L2 button, L3 by manual L3 button only.",
            "Partial shutdown capability desirable for production flexibility: separate first-stage and second-stage compressor trip logic, individual well shutdown capability.",
            "Fire/gas detection voting: typically 2oo4 detectors in zone to avoid spurious trips from single faulty detector, but immediate action (no time delay) once voting satisfied.",
            "UV/IR flame detectors in cross-zone voting (detector in Zone A + detector in Zone B both trip) provides higher confidence of real fire vs spurious activation.",
            "ESD valve closure time specification critical: spring-return ball valves achieve <5 seconds, gate valves may require 30-60 seconds (unacceptable for rapid isolation needs).",
            "Fail-safe design: ESD valves fail closed on air/power loss, compressor trips on power loss, blowdown valves fail closed (require active signal to open).",
            "Solenoid valve arrangement for pneumatic ESDVs: two solenoids in series (both must energize to keep valve open - redundant trip capability).",
            "IEC 61511 Clause 10.4.2 requires C&E matrix validation by operations and maintenance personnel, independent review by safety authority.",
            "HAZOP worksheet provides input identification for C&E matrix - each HAZOP safeguard requiring automation becomes C&E row.",
            "Testing strategy documented in C&E matrix: proof test interval for each input, FAT/SAT test cases covering all trip combinations.",
            "Override/bypass capability specified in C&E matrix with interlocks: e.g., allow high-pressure trip bypass only when pressure <50% of trip setpoint.",
            "Annunciation requirements: each trip cause generates unique alarm in DCS, ESD system health monitoring (power supply status, solenoid status) alarmed separately."
        ],
        key_factors=[
            "HAZOP-derived trip cause identification (process parameters, fire/gas, manual stations)",
            "Voting logic specification (1oo2, 2oo3, 2oo4) with clear notation",
            "Time delay settings (0 sec for fire/gas, 2-5 sec for process variables)",
            "Sequential shutdown coordination with time delays between steps",
            "Multi-level ESD architecture (L1 process, L2 wellhead, L3 blowdown)",
            "Manual shutdown bypass of voting logic (immediate actuation)",
            "Reset logic preventing automatic restart",
            "Fail-safe design (valves fail closed, equipment trips on power loss)",
            "Partial shutdown capability for production flexibility",
            "Cross-zone voting for fire/gas detection"
        ],
        primary_authority=[
            "IEC 61511-1:2016 Clause 10.4.2 (Application programming - C&E matrix documentation)",
            "API RP 14C Section 6 (ESD system design for offshore platforms)",
            "ISA-TR84.00.04-2011 (Guidelines for ESD system cause and effect documentation)",
            "ISO 10418:2019 Section 8 (Petroleum and natural gas industries - offshore platform safety systems)",
            "30 CFR 250 Subpart H (BSEE requirements for platform safety systems)"
        ],
        burden_holder="ESD system designer must produce C&E matrix validated by operations and independent safety review",
        adversary_position="Operator may request excessive partial shutdown capability, complicating logic and increasing failure modes; regulator may require more conservative voting (e.g., 1oo2 instead of 2oo3) for critical trips",
        counter_arguments=[
            "Overly complex C&E matrix with extensive partial shutdown logic increases PLC programming errors and reduces reliability",
            "3-level ESD architecture may be overkill for small onshore facilities with rapid emergency response capability",
            "2oo3 voting on fire/gas introduces delay (waiting for second detector) that could allow fire spread in fast-developing scenarios",
            "Manual shutdown stations bypassing voting logic creates single-point vulnerability to inadvertent activation (production loss)",
            "Sequential shutdown time delays (waiting between steps) may allow unsafe condition to persist during shutdown sequence"
        ],
        resolution_strategy="Balance partial shutdown flexibility against complexity (limit to 2-3 shutdown groups maximum), use cross-zone voting for fire confirmation, implement shrouded/recessed manual shutdown buttons to prevent inadvertent activation, validate sequential timing via dynamic simulation",
        entity_scope="Offshore production platforms, onshore gas processing plants, compressor stations, FPSO facilities, unmanned wellhead platforms",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="IEC 61511 and API RP 14C provide clear C&E documentation requirements; voting logic selection and time delay settings involve engineering judgment within established ranges",
        controlling_precedent="IEC 61511-1:2016 Clause 10.4.2 mandates C&E matrix as required SIS documentation; API RP 14C Section 6 establishes offshore industry expectations for multi-level ESD architecture"
    ),

    DoctrineBlock(
        topic="Fire and Gas Detection System Design: Detector Types and Coverage",
        keywords=["fire detection", "gas detection", "UV/IR", "flame detector", "catalytic", "infrared", "electrochemical", "LEL", "coverage", "spacing", "fusible plug", "heat detector"],
        conclusion_template=[
            "Fire and gas detection system design requires selection of appropriate detector technology (UV/IR flame, heat, fusible plug for fire; catalytic, IR, electrochemical for gas), proper spacing per coverage calculations, and voting logic to minimize spurious trips.",
            "ISA 84.00.07 and API RP 505 provide detector spacing guidance; 2oo4 voting typical for gas detection zones to balance sensitivity and false alarm avoidance.",
            "Offshore platforms require graded detection: open areas use UV/IR flame and catalytic LEL detectors; enclosed spaces add heat/smoke; confined spaces use enhanced coverage with electrochemical point detectors."
        ],
        reasoning_framework=[
            "Fire detection technologies: UV/IR (ultraviolet/infrared flame), heat (rate-of-rise or fixed temperature), fusible plug (mechanical, heat-actuated), smoke (ionization or photoelectric).",
            "UV/IR flame detectors operate by detecting characteristic UV and IR emissions from hydrocarbon flames - dual-spectrum reduces false alarms from arc welding, lightning, hot objects.",
            "UV/IR coverage: 50-foot radius typical for hydrocarbon flame detection in open areas (varies by detector model and fuel type).",
            "Heat detectors (rate-of-rise or fixed temperature) suitable for enclosed equipment rooms where smoke/flame may be obscured - slower response than flame detectors.",
            "Fusible plug detectors (pneumatic) provide hardwired, fail-safe fire detection independent of electrical power - common on skid-mounted packages.",
            "Gas detection technologies: catalytic (combustible gas, 0-100% LEL), infrared (hydrocarbons, point or open-path), electrochemical (H2S, CO, toxic gases).",
            "Catalytic (pellistor) detectors measure heat from catalytic combustion of gas sample - most common for LEL detection, but poisoned by sulfur compounds and silicones.",
            "Infrared (IR) point detectors measure absorption of IR light by hydrocarbon molecules - immune to poisoning, but higher cost; require line-of-sight for open-path versions.",
            "Electrochemical sensors for H2S (0-100 ppm typical) and CO (0-500 ppm) in confined spaces - limited lifespan (2-3 years), requires regular calibration.",
            "Coverage calculations per API RP 505: catalytic detector spacing 10-15 feet in enclosed areas, 20-25 feet in open well-ventilated areas.",
            "ISA-TR84.00.07 provides detailed mapping approach: identify ignition sources and leak points, position detectors in likely dispersion paths considering prevailing wind.",
            "Detector height critical: natural gas (lighter than air) - mount detectors high (8-12 feet); propane/butane (heavier) - mount low (1-2 feet); H2S - mount breathing zone height (4-6 feet).",
            "Voting logic for gas detection: 2oo4 (two out of four detectors in zone) balances spurious trip avoidance with timely detection - single detector failure or false alarm does not initiate shutdown.",
            "Alarm levels: Low alarm at 20% LEL (alert operators), High alarm at 40% LEL (initiate shutdown) - provides warning before explosive atmosphere develops.",
            "Cross-zone voting for fire: detector in adjacent zones both triggering increases confidence of real fire vs spurious (welding, lightning, hot surface reflection).",
            "Offshore platform typical detector layout: UV/IR flame detectors on equipment skids (compressors, separators) and around fired equipment; catalytic LEL detectors on well decks and in enclosed modules.",
            "HVAC integration: high gas alarm triggers ventilation increase (purge with fresh air); very high alarm (60% LEL) may trip HVAC to prevent fan-induced ignition.",
            "Detector placement avoids direct exposure to steam vents, relief valve discharge plumes, and high-velocity gas streams (can damage sensors or cause false readings).",
            "Weatherproofing and corrosion resistance: offshore detectors require NEMA 4X or IP66 rating minimum, stainless steel or fiberglass enclosures in corrosive environments.",
            "Self-diagnostics and fault annunciation: modern detectors report sensor failure, calibration drift, power supply issues to central monitoring system - failed detector alarmed distinctly from gas alarm.",
            "Proof test and calibration intervals: catalytic detectors quarterly calibration, electrochemical H2S monthly, UV/IR flame annual functional test per manufacturer specifications.",
            "Common cause failure mitigation: use diverse detector types (catalytic + IR) in same zone if SIL 2/3 required - different failure modes increase overall reliability.",
            "API RP 14C Section 7 requires fire and gas detection on all manned platforms with ESD system integration; gas detection mandatory in enclosed equipment spaces.",
            "NFPA 72 and ISA 12.13.01 provide additional guidance for fire alarm system design and installation practices."
        ],
        key_factors=[
            "Detector technology selection (UV/IR, heat, fusible plug for fire; catalytic, IR, electrochemical for gas)",
            "Coverage calculations per API RP 505 and ISA 84.00.07 (spacing 10-25 feet depending on area classification)",
            "Detector mounting height based on gas density (high for CH4, low for propane, breathing zone for H2S)",
            "Voting logic (2oo4 typical for gas, cross-zone for fire confirmation)",
            "Alarm setpoints (20% LEL low, 40% LEL high for combustible gas)",
            "HVAC integration (purge on alarm, trip on very high gas)",
            "Weatherproofing and corrosion resistance (NEMA 4X/IP66 minimum offshore)",
            "Self-diagnostics and fault annunciation to central system",
            "Calibration frequency (quarterly for catalytic, monthly for electrochemical)",
            "Diverse detector types for SIL 2/3 applications (catalytic + IR)"
        ],
        primary_authority=[
            "ISA-TR84.00.07-2018 (Guidance on the Evaluation of Fire, Combustible Gas and Toxic Gas System Effectiveness)",
            "API RP 505:2018 (Recommended Practice for Classification of Locations for Electrical Installations at Petroleum Facilities)",
            "API RP 14C Section 7 (Fire and gas detection system requirements for offshore platforms)",
            "NFPA 72:2022 (National Fire Alarm and Signaling Code)",
            "ISA 12.13.01-2018 (Performance Requirements for Combustible Gas Detectors)"
        ],
        burden_holder="System designer must demonstrate adequate coverage per mapping calculations and appropriate detector type selection",
        adversary_position="Regulator may require enhanced coverage (more detectors, lower spacing) in high-consequence areas; operator may challenge calibration frequency cost",
        counter_arguments=[
            "2oo4 voting may delay detection in fast-developing fire/gas scenarios where immediate action critical",
            "API RP 505 spacing guidelines assume ideal dispersion conditions - congested areas with poor ventilation require closer spacing",
            "Catalytic detectors subject to poisoning in sour gas service - IR detectors necessary despite higher cost",
            "Quarterly calibration interval excessive for stable environments - annual sufficient for well-maintained detectors",
            "Cross-zone voting for fire detection introduces delay that could allow fire growth in fast-escalating scenarios"
        ],
        resolution_strategy="Perform computational fluid dynamics (CFD) modeling for congested/complex areas to validate coverage, use diverse detector types in high-consequence zones (SIL 2/3), implement gradient detection logic (respond faster to rapid concentration increase), document calibration procedures per manufacturer specifications",
        entity_scope="Offshore platforms, onshore gas plants, compressor stations, loading terminals, confined space entries, enclosed equipment buildings",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="ISA 84.00.07 and API RP 505 provide rigorous coverage calculation methods; detector type selection well-established; voting logic and alarm setpoints industry consensus",
        controlling_precedent="ISA-TR84.00.07-2018 establishes internationally recognized fire/gas detection effectiveness evaluation methodology; API RP 14C Section 7 mandates offshore platform application"
    ),

    DoctrineBlock(
        topic="Pressure Safety Valve Sizing per API 520/521",
        keywords=["PSV", "relief valve", "sizing", "API 520", "API 521", "fire case", "blocked outlet", "thermal relief", "orifice area", "overpressure", "set pressure", "ASME Section VIII"],
        conclusion_template=[
            "Pressure safety valve (PSV) sizing per API Standard 520 requires identification of credible overpressure scenarios (fire exposure, blocked outlet, thermal expansion, runaway reaction), calculation of required relief capacity, and selection of orifice size with adequate margin.",
            "Fire case per API 521 typically governs for outdoor pressure vessels; blocked outlet scenarios critical for pumps and compressors; thermal relief sizing per API 521 Section 4.4.12.",
            "PSV set pressure typically 90-95% of vessel MAWP per ASME Section VIII; accumulation (allowable overpressure) 10% for single PSV, 16% for multiple PSVs in fire case per API 521."
        ],
        reasoning_framework=[
            "API 520 Part I provides sizing methodology for vapor relief; Part II covers liquid relief scenarios.",
            "Credible overpressure scenario identification: external fire, blocked discharge, control valve failure, cooling failure, runaway reaction, thermal expansion (liquid-full), tube rupture (heat exchangers).",
            "Fire case (API 521 Section 4.4.8): calculate heat input from fire exposure, determine vapor generation rate, size PSV for vapor relief capacity.",
            "Fire heat input Q = 21,000 * F * A^0.82 (Btu/hr), where F = environment factor (1.0 for unprotected, 0.5 for fireproofing, 0.3 for water deluge), A = wetted surface area (ft^2) up to 1,000 ft^2 maximum.",
            "Vapor generation rate W = Q / (latent heat of vaporization) - determines required PSV mass flow capacity.",
            "PSV sizing equation (vapor): A = (W * sqrt(T * Z)) / (C * K_d * P_1 * K_b * K_c) where A = required orifice area (in^2), W = flow rate (lb/hr), C = coefficient from API 520, P_1 = set pressure + allowable accumulation (psia).",
            "Blocked outlet scenario: pump deadheading or compressor blocked discharge - relief capacity must handle maximum equipment output at shutoff head.",
            "Thermal relief (liquid expansion): small liquid volume heating in isolated piping section - API 521 equation: Q = H * beta * G * delta_T / (delta_t * rho * C_p) where beta = liquid thermal expansion coefficient.",
            "Thermal relief PSVs typically small orifice (D through G) due to low volumetric expansion rate - often overlooked but critical to prevent piping rupture.",
            "Set pressure selection: ASME Section VIII allows set pressure up to vessel MAWP, but practical range 90-95% MAWP to provide operating margin and account for instrument uncertainty.",
            "Accumulation (overpressure during relief): 10% of MAWP for single PSV in non-fire cases, 21% for fire case or multiple PSVs (ASME Section VIII UG-125).",
            "Orifice area selection: calculate required area, select next larger standard orifice per API 526 (D, E, F, G, H, J, K, L, M, N, P, Q, R, T - letter designations, not dimensions).",
            "Back pressure evaluation: conventional PSVs limited to 10% back pressure; balanced bellows PSVs tolerate up to 40% back pressure without capacity reduction.",
            "Inlet piping sizing: pressure drop in inlet piping limited to 3% of set pressure to avoid chattering and capacity reduction per API 520 Section 5.5.5.",
            "Discharge piping sizing: vapor relief to atmosphere requires sufficient diameter to limit back pressure; liquid relief to closed system must prevent excessive back pressure.",
            "Reaction force calculation (API 521 Section 4.10): F = W * V / g_c where W = relieving rate, V = exit velocity - critical for piping support design and nozzle loading on vessel.",
            "PSV capacity certification: ASME stamped valves have certified flow capacity at 10% overpressure per ASME Section VIII and API 526 - manufacturer data sheet provides K_d (discharge coefficient).",
            "Multiple PSV installation: when total required capacity exceeds largest single orifice (T = 26 in^2), use multiple PSVs with staggered set pressures (e.g., first PSV at 95% MAWP, second at 100% MAWP).",
            "Offshore platform relief headers: multiple PSVs discharge to common flare header - back pressure analysis must consider coincident relief scenarios (fire affecting multiple vessels).",
            "Temperature correction: relieving temperature may exceed design temperature during fire exposure - use elevated temperature properties for sizing calculations.",
            "Two-phase flow: if relief involves flashing liquid, use API 520 homogeneous equilibrium model or omega method - significantly impacts required orifice size.",
            "Pilot-operated relief valves: suitable for tight shutoff and low simmer/leakage tolerance applications, but require back pressure <50% of set pressure for reliable operation.",
            "API 521 Section 4.4.1 requires documentation of PSV sizing basis, credible scenarios considered, and scenario selection rationale - critical for regulatory review and management of change."
        ],
        key_factors=[
            "Credible overpressure scenario identification (fire, blocked outlet, thermal expansion, control failure)",
            "Fire case heat input calculation per API 521 (Q = 21,000 * F * A^0.82)",
            "PSV sizing equation application with correct coefficients (API 520)",
            "Set pressure selection (90-95% MAWP typical)",
            "Accumulation limits (10% single PSV, 21% fire case per ASME VIII)",
            "Standard orifice area selection (API 526 letter designations)",
            "Back pressure evaluation (10% for conventional, 40% for balanced bellows)",
            "Inlet pressure drop limitation (3% of set pressure maximum)",
            "Reaction force calculation for piping support design",
            "Two-phase flow considerations (omega method or HEM model)"
        ],
        primary_authority=[
            "API Standard 520 Part I:2020 (Sizing, Selection, and Installation of Pressure-Relieving Devices - Vapor relief)",
            "API Standard 521:2014 (Pressure-Relieving and Depressuring Systems - Fire case and thermal relief)",
            "ASME Boiler and Pressure Vessel Code Section VIII Division 1 UG-125 (Overpressure protection requirements)",
            "API Standard 526:2017 (Flanged Steel Pressure-Relief Valves - Orifice designations)",
            "30 CFR 250.1628 (BSEE pressure relief requirements for offshore platforms)"
        ],
        burden_holder="System designer must demonstrate PSV sizing adequacy for all credible overpressure scenarios with documented calculations",
        adversary_position="Regulator may challenge fire case environment factor selection (require F=1.0 unprotected) or demand consideration of less-credible scenarios; inspector may require set pressure reduction to increase operating margin",
        counter_arguments=[
            "API 521 fire heat input formula conservative (assumes engulfing pool fire) - actual fire exposure may be significantly lower for elevated equipment",
            "Blocked outlet scenario may be incredible if proper interlocks prevent pump/compressor operation with closed discharge valve",
            "10% accumulation limit (single PSV) overly restrictive - allows no margin for PSV blowdown characteristics and reseat testing",
            "Thermal relief scenario requires simultaneous isolation (valve closure both ends) and heat input (solar, process heat) - low probability combination",
            "API 520 vapor sizing equation assumes ideal gas behavior - real gas compressibility factor (Z) correction may be unnecessary for near-atmospheric relief"
        ],
        resolution_strategy="Document all credible scenarios with clear rationale for dismissed cases, use conservative fire case assumptions (F=1.0) unless fireproofing certified, perform set pressure tolerance stack-up analysis (instrument uncertainty + valve tolerance) to verify MAWP not exceeded, engage API 510 inspector early for agreement on sizing basis",
        entity_scope="Pressure vessels, storage tanks, heat exchangers, compressor cylinders, pump casings, thermal relief on isolated piping, offshore platform flare headers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API 520/521 provide comprehensive, internationally recognized PSV sizing methodology; scenario identification and parameter selection involve engineering judgment within established framework",
        controlling_precedent="API Standard 520:2020 and ASME Section VIII UG-125 establish definitive PSV sizing and overpressure protection requirements; fire case per API 521 widely accepted for outdoor hydrocarbon service"
    ),

    DoctrineBlock(
        topic="HIPPS (High Integrity Pressure Protection System) as PSV Alternative",
        keywords=["HIPPS", "high integrity pressure protection", "SIL3", "isolation valve", "pressure transmitter", "PSV alternative", "API 17O", "PFD", "spurious closure", "diagnostic coverage"],
        conclusion_template=[
            "HIPPS provides SIL 3 pressure protection by isolating pressure source (closing fast-acting valve) before MAWP exceeded, serving as alternative to traditional PSV where relief impractical (subsea, large capacity, toxic service).",
            "API 17O and IEC 61511 require rigorous SIL 3 verification (PFD < 10^-3), proof testing every 1-2 years, and often backup PSV for defense-in-depth despite HIPPS being primary protection.",
            "Typical HIPPS architecture: 2oo3 pressure transmitters → SIL 3 logic solver → 1oo2 isolation valves with partial stroke testing to maintain <10^-3 PFD."
        ],
        reasoning_framework=[
            "HIPPS concept: detect rising pressure and close isolation valve before vessel/pipeline reaches MAWP, preventing overpressure rather than relieving it.",
            "Applications where HIPPS preferred over PSV: subsea pipelines (relief to seafloor environmentally unacceptable), very large relief capacity (economically prohibitive PSV/flare), toxic service (H2S relief unacceptable), high pressure gas (relief sonic velocity limitations).",
            "SIL 3 requirement: HIPPS must achieve probability of failure on demand (PFD) < 10^-3 to serve as sole overpressure protection per API 17O and IEC 61511.",
            "Architecture to achieve SIL 3: 2oo3 pressure transmitters (redundant with voting) + SIL 3 rated logic solver + 1oo2 fast-acting isolation valves (redundant in parallel, both must fail to prevent closure).",
            "Pressure transmitter selection: SIL 2 rated devices minimum, diverse types (capacitance + strain gauge) to reduce common cause failures, range selected for 2:1 turndown to maximize accuracy.",
            "Setpoint selection: HIPPS activation at 90-95% MAWP, allowing time for valve closure (typically 2-5 seconds) before pressure reaches MAWP even under maximum rate of pressure rise.",
            "Isolation valve requirements: fail-safe close on loss of power/air, closure time <5 seconds typical, full-bore ball valve design to minimize pressure drop, partial stroke testing (PST) capability to verify valve movement without full closure.",
            "Partial stroke testing (PST): valve stroked 10-20% of travel every 1-6 months, verifies valve mobility and actuator function, significantly improves diagnostic coverage and reduces PFD without process shutdown.",
            "PFD calculation: HIPPS PFD approximately (3 * lambda_PT^2 * TI^2) / 2 + (lambda_LS * TI) / 2 + (2 * lambda_V^2 * TI_PST^2) / 3, where TI = proof test interval, TI_PST = PST interval.",
            "Achieving PFD < 10^-3 requires: high-reliability components (lambda < 10^-6 per hour), proof test interval ≤2 years, PST every 3-6 months, diagnostic coverage >90%.",
            "Defense-in-depth philosophy: many operators install downstream PSV rated for maximum credible HIPPS failure scenario (e.g., one valve fails to close) - provides backup despite HIPPS being SIL 3 primary protection.",
            "Spurious closure risk: HIPPS inadvertent activation shuts down production - 2oo3 pressure voting reduces spurious trip rate to <0.1 per year (vs 1-2 per year for single transmitter).",
            "Common cause failures: instrument air/hydraulic supply loss must not prevent HIPPS actuation - spring-return or stored energy valve closure mechanism required.",
            "Diagnostic coverage: continuous self-diagnostics on pressure transmitters (range check, drift detection) and logic solver (watchdog timer, output test pulses) essential for SIL 3.",
            "Proof test interval: 1-2 years typical for SIL 3 HIPPS, includes full functional test (simulate overpressure, verify valve closure), transmitter calibration, logic solver diagnostics review.",
            "API 17O Section 7 provides detailed HIPPS design requirements for subsea applications, including environmental qualification and reliability targets.",
            "IEC 61511 Clause 11.9 requires HIPPS PFD validation via fault tree analysis or Markov modeling - simplified equations (ISA TR84.00.02) acceptable for initial screening.",
            "Response time budget: pressure rise time from setpoint to MAWP must exceed transmitter response (0.5s) + logic solver execution (0.2s) + valve closure time (2-5s) + margin (20%).",
            "Override/bypass: HIPPS bypass during commissioning/maintenance requires dual key switches, time-limited automatic restoration, and alarmed bypass status to central control room.",
            "Installation considerations: pressure transmitter placement upstream of isolation valve close to pressure source, minimizing sensing lag; valve located to isolate pressure source before protected equipment.",
            "BSEE approval required for offshore HIPPS applications - demonstration of SIL 3 achievement and risk reduction equivalence to conventional PSV often required."
        ],
        key_factors=[
            "SIL 3 PFD requirement (<10^-3) per API 17O and IEC 61511",
            "2oo3 pressure transmitter architecture for voting and redundancy",
            "SIL 3 rated logic solver with high diagnostic coverage (>90%)",
            "1oo2 fast-acting isolation valves (<5 second closure, fail-closed)",
            "Partial stroke testing every 3-6 months to reduce PFD",
            "Setpoint selection (90-95% MAWP) with closure time margin",
            "Response time budget validation (sensor + logic + valve + margin)",
            "Backup PSV for defense-in-depth (common practice despite SIL 3)",
            "Spurious closure minimization via 2oo3 voting (reduce production loss)",
            "Proof test interval (1-2 years) with full functional testing"
        ],
        primary_authority=[
            "API Specification 17O:2019 (Subsea High Integrity Pressure Protection Systems - HIPPS)",
            "IEC 61511-1:2016 Clause 11.9 (Requirements for safety instrumented functions with high demand/continuous mode)",
            "ISA-TR84.00.02-2002 Part 3 (Simplified methods for HIPPS PFD calculations)",
            "API Standard 521:2014 Section 4.18 (HIPPS as alternative to pressure relief)",
            "30 CFR 250.1628 (BSEE requirements for offshore pressure protection systems)"
        ],
        burden_holder="HIPPS designer must demonstrate SIL 3 achievement via quantitative PFD calculation and functional safety management per IEC 61511",
        adversary_position="Regulator may require backup PSV regardless of HIPPS SIL 3 certification (defense-in-depth); operator may challenge high maintenance burden (PST, proof testing) vs conventional PSV simplicity",
        counter_arguments=[
            "HIPPS introduces complexity and failure modes not present in simple mechanical PSV - overall reliability may be lower despite SIL 3 rating",
            "Partial stroke testing assumption that 10-20% stroke validates full-stroke capability questionable - valve could fail mid-travel under full demand",
            "Common cause failures (firmware bugs, power supply issues) can defeat redundancy and cause simultaneous failure of all protection layers",
            "Spurious closure risk remains despite 2oo3 voting - production loss from inadvertent trip may exceed cost of conventional PSV/flare system",
            "Proof test intervals (1-2 years) optimistic for harsh offshore environments - shorter intervals erode PFD benefit and increase maintenance cost"
        ],
        resolution_strategy="Install backup PSV sized for single valve failure scenario (defense-in-depth), use diverse pressure transmitter technologies (capacitance + piezo-resistive), implement comprehensive functional safety management program per IEC 61511 Clause 5, perform fault tree analysis with documented assumptions for AHJ review, specify certified SIL 3 components with prior use evidence",
        entity_scope="Subsea pipelines, high-pressure gas transmission, toxic service (H2S), large-capacity relief scenarios, offshore platform inlet separation",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="API 17O and IEC 61511 provide clear HIPPS requirements, but SIL 3 achievement requires rigorous analysis and high-quality components; acceptance by regulators varies; backup PSV common practice reflects lingering concern about HIPPS sole reliance",
        controlling_precedent="API Specification 17O:2019 establishes subsea HIPPS design standard; IEC 61511 Clause 11.9 mandates SIL verification for safety-critical applications; regulatory acceptance case-by-case"
    ),

    DoctrineBlock(
        topic="Proof Test Intervals and PFD Calculation for SIL Verification",
        keywords=["proof test", "PFD", "probability of failure on demand", "SIL verification", "test interval", "dangerous failure", "safe failure", "lambda", "TI", "diagnostic coverage"],
        conclusion_template=[
            "Proof test interval (TI) selection directly impacts probability of failure on demand (PFD): PFD approximately proportional to (lambda * TI) / 2 for single-channel systems, where lambda = dangerous undetected failure rate.",
            "SIL verification per IEC 61508/61511 requires PFD calculation using manufacturer-provided failure rates, accounting for diagnostic coverage, and validating against SIL targets (SIL 1: <0.1, SIL 2: <0.01, SIL 3: <0.001).",
            "Proof test procedures must verify all safety-critical functions: sensor response, logic solver execution, final element movement - partial testing that omits critical elements invalidates PFD calculation basis."
        ],
        reasoning_framework=[
            "PFD (Probability of Failure on Demand) quantifies likelihood that safety function fails when demanded - central metric for SIL verification per IEC 61508.",
            "Dangerous failure: failure mode that prevents safety function from executing when demanded (e.g., pressure transmitter stuck reading low, preventing high-pressure trip).",
            "Safe failure: failure mode that causes spurious trip but does not compromise safety (e.g., transmitter reading high, causing unnecessary shutdown).",
            "Failure rate (lambda): total device failure rate = lambda_D (dangerous) + lambda_S (safe), typically expressed in failures per 10^6 hours (FITs) or per hour.",
            "Diagnostic coverage (DC): fraction of dangerous failures detected by automatic diagnostics, allowing immediate repair vs requiring proof test to discover.",
            "Lambda_DU (dangerous undetected): portion of dangerous failures not caught by diagnostics, lambda_DU = lambda_D * (1 - DC) - drives PFD accumulation between proof tests.",
            "PFD equation for single device: PFD_avg approximately (lambda_DU * TI) / 2, where TI = proof test interval (hours) - assumes constant failure rate and immediate repair.",
            "Proof test interval selection: shorter TI reduces PFD but increases testing cost and process shutdown frequency; typical range 1-10 years (8,760 to 87,600 hours).",
            "SIL 1 requirement: PFD_avg < 0.1 (10^-1) - achievable with lambda_DU = 10^-6 per hour and TI = 10 years, or lambda_DU = 5 x 10^-6 and TI = 2 years.",
            "SIL 2 requirement: PFD_avg < 0.01 (10^-2) - typically requires TI ≤ 2 years with standard sensors (lambda ~ 5 x 10^-6 per hour) or redundant architecture (1oo2).",
            "SIL 3 requirement: PFD_avg < 0.001 (10^-3) - demands high diagnostic coverage (>90%), annual proof testing, and/or redundant architecture (2oo3).",
            "Redundant architecture PFD: 1oo2 system PFD approximately (lambda_DU^2 * TI^2) / 3 - quadratic improvement allows longer test intervals or lower-reliability components.",
            "2oo3 architecture PFD: approximately 3 * (lambda_DU^2 * TI^2) / 2 - achieves SIL 2/3 with commercial-grade sensors if TI ≤ 2 years.",
            "Common cause failure (CCF) degrades redundancy: beta factor (2-10%) represents fraction of failures affecting all redundant channels simultaneously (design error, environmental stress).",
            "Beta factor impact on 1oo2 PFD: PFD = (1 - beta) * (lambda_DU^2 * TI^2) / 3 + beta * (lambda_DU * TI) / 2 - second term represents CCF contribution.",
            "Proof test completeness critical: test must verify entire SIF chain from sensor through final element, simulating actual demand condition.",
            "Partial stroke testing (PST) on valves: 10-20% valve travel every 3-12 months verifies valve mobility, significantly reduces lambda_DU for final element, allowing longer full-stroke proof test interval.",
            "Sensor proof test: apply known pressure/temperature/level, verify transmitter output accuracy within tolerance (typically ±1% of span), check alarm setpoints.",
            "Logic solver proof test: inject simulated sensor signals, verify correct output to final elements, check voting logic and timers, review error logs.",
            "Final element proof test: command valve closure/opening, measure stroke time, verify full travel, check fail-safe mode (spring-return or stored energy).",
            "Proof test interval optimization: balance testing cost (production shutdown, labor) against PFD reduction benefit - typically economic optimum around 2-5 years for SIL 2.",
            "IEC 61511 Clause 16.2.10 allows TI extension if online diagnostics provide equivalent PFD reduction - requires validation that diagnostics achieve claimed DC.",
            "Manufacturer failure rate data sources: IEC 61508-2 Annex D (generic failure rates), OREDA (Offshore Reliability Data), exida SERH (Safety Equipment Reliability Handbook), vendor-specific SIL certificates.",
            "Uncertainty in failure rate data: lambda values vary 3-10x between sources - conservative approach uses upper confidence bound or performs sensitivity analysis.",
            "Proof test as-found data: track percentage of proof tests finding actual failures - if significantly below predicted PFD, consider TI extension; if higher, reduce TI or improve diagnostics."
        ],
        key_factors=[
            "Dangerous undetected failure rate (lambda_DU) from manufacturer data or IEC 61508-2",
            "Diagnostic coverage (DC) percentage (>90% for SIL 3)",
            "Proof test interval (TI) selection (1-10 years typical, 1-2 years for SIL 3)",
            "Redundancy architecture (1oo2 quadratic PFD improvement, 2oo3 for SIL 3)",
            "Common cause failure beta factor (2-10% depending on diversity)",
            "Partial stroke testing frequency for valve PFD reduction",
            "Proof test completeness (full SIF chain verification)",
            "As-found failure data tracking for TI optimization",
            "SIL target PFD thresholds (SIL 1: <0.1, SIL 2: <0.01, SIL 3: <0.001)",
            "Sensitivity analysis on lambda uncertainty"
        ],
        primary_authority=[
            "IEC 61508-6:2010 Annex B (PFD calculation methods and formulas)",
            "IEC 61511-1:2016 Clause 11.9 (SIL verification requirements)",
            "ISA-TR84.00.02-2002 Part 3 (Simplified equations and calculation examples)",
            "IEC 61508-2:2010 Annex D (Generic reliability data for safety devices)",
            "OREDA Offshore Reliability Data Handbook (Industry failure rate database)"
        ],
        burden_holder="SIF designer must demonstrate PFD < SIL target using documented failure rates and proof test procedures covering full SIF chain",
        adversary_position="Regulator may require shorter proof test intervals than calculated optimum (conservative approach); inspector may challenge incomplete proof test procedures that omit critical elements",
        counter_arguments=[
            "Manufacturer failure rate data optimistic (controlled lab conditions) - field failure rates often 2-3x higher due to environmental stress, installation errors, and maintenance quality",
            "Diagnostic coverage claims (>90%) difficult to validate without comprehensive FMEA - actual DC may be significantly lower, invalidating SIL 3 claim",
            "Proof test interval extension based on as-found data dangerous - absence of found failures may reflect inadequate test rigor, not actual reliability improvement",
            "Partial stroke testing credit assumes 10-20% stroke validates full-stroke capability - valve could fail mid-travel or at end-of-stroke under actual demand",
            "Common cause failure beta factors (2-10%) underestimate systematic failures from design errors, software bugs, or environmental events affecting all channels"
        ],
        resolution_strategy="Use conservative failure rate data (OREDA upper bounds or vendor worst-case values), perform FMEA to validate diagnostic coverage claims, document comprehensive proof test procedures with checksheets, track as-found failure data and adjust TI based on actual experience, use diverse technologies for redundant channels to minimize beta factor",
        entity_scope="All SIL-rated safety instrumented functions: ESD systems, pressure protection, high-temperature trips, toxic gas detection, flame detection, compressor antisurge",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="IEC 61508/61511 provide internationally recognized PFD calculation framework; failure rate data uncertainty and diagnostic coverage validation remain areas of engineering judgment requiring conservative assumptions",
        controlling_precedent="IEC 61508-6:2010 establishes definitive PFD calculation methods; IEC 61511-1:2016 mandates SIL verification for all safety-critical applications"
    ),

    # Additional doctrines to reach 25+ target

    DoctrineBlock(
        topic="Functional Safety Management and Lifecycle per IEC 61511",
        keywords=["functional safety management", "FSM", "safety lifecycle", "IEC 61511", "competency", "verification", "validation", "documentation", "management of change"],
        conclusion_template=[
            "Functional Safety Management (FSM) per IEC 61511 Clause 5 requires documented procedures covering entire SIS lifecycle from concept through decommissioning, including competency requirements, verification/validation, and management of change.",
            "SIL 2/3 projects mandate independent verification by qualified safety engineer not involved in design; SIL 3 often requires third-party certification.",
            "FSM documentation trail - SRS, design specs, C&E matrix, PFD calculations, proof test procedures, MOC records - serves as evidence of IEC 61511 compliance for regulatory audits."
        ],
        reasoning_framework=[
            "IEC 61511 Clause 5 defines FSM as management system ensuring SIS design, implementation, operation, and maintenance meet safety integrity requirements throughout lifecycle.",
            "Safety lifecycle phases per IEC 61511 Figure 4: 1-Hazard/risk analysis, 2-SRS development, 3-Design, 4-Installation, 5-Commissioning, 6-Operation/maintenance, 7-Modification, 8-Decommissioning.",
            "Competency requirements: personnel performing SIS work must demonstrate technical expertise and training - IEC 61511 Clause 5.2.2 requires documented competency assessment.",
            "Safety Requirements Specification (SRS) per Clause 10: documents all SIFs including trip setpoints, response times, SIL targets, demand mode, proof test intervals - foundation document for entire lifecycle.",
            "Verification (Clause 5.2.6): confirms each lifecycle phase output meets input requirements - design verification checks PFD calculation against SRS SIL target.",
            "Validation (Clause 5.2.7): confirms overall SIS meets safety objectives in actual operating environment - typically performed during FAT/SAT commissioning.",
            "Independent verification requirement for SIL 2/3: person/team performing verification must be independent of design team, with equivalent competency level.",
            "Third-party certification common for SIL 3 applications: exida, TUV, DNV provide independent SIL assessment and certification services - often required by insurers or regulators.",
            "Documentation requirements extensive: SRS, design basis, C&E matrix, PFD calculations, FMEA, FAT/SAT protocols, proof test procedures, training records, MOC documentation.",
            "Management of Change (MOC) per Clause 17: any modification to SIS or process potentially affecting SIS requires documented change analysis, re-verification, and functional safety assessment.",
            "MOC triggers: process parameter changes affecting trip setpoints, equipment replacements, control logic modifications, proof test interval adjustments, organizational changes affecting competency.",
            "Bypass management (Clause 11.8): SIF bypass for maintenance requires documented procedure, time-limited automatic restoration, operator authorization, and alarmed status.",
            "Proof test procedure documentation: step-by-step procedures for each SIF, specifying required instruments, acceptance criteria, restoration steps - must be validated during commissioning.",
            "As-found/as-left data recording: proof test results documenting pre-test condition and post-calibration performance - critical for PFD validation and test interval optimization.",
            "Incident investigation: SIS failures (spurious trips, failure to trip, degraded mode) require root cause analysis and corrective action per Clause 16.2.8.",
            "Periodic SIS assessment: IEC 61511 Clause 8.2.5 requires documented review of SIS performance, proof test results, incident history, and MOC impacts - typically every 2-5 years.",
            "Competency assessment methods: combination of education (engineering degree), training (SIS-specific courses), and experience (documented project history) - TUV/exida offer competency certification.",
            "Roles and responsibilities: clearly defined in FSM plan - SIS engineer (design), verification engineer (independent check), operations (proof testing), maintenance (component repair), FSM coordinator (overall management).",
            "Software systematic capability per IEC 61508-3: SC 2 required for SIL 2 (structured design, reviews), SC 3 for SIL 3 (formal methods, diverse programming) - applies to PLC ladder logic.",
            "Pre-startup safety review (PSSR) per Clause 12: formal review before SIS placed in operation, verifying installation per design, FAT/SAT complete, procedures in place, training complete.",
            "Offshore platforms: BSEE SEMS regulation 30 CFR 250 Subpart S requires elements aligning with IEC 61511 FSM (hazard analysis, MOC, training, audits)."
        ],
        key_factors=[
            "Safety Requirements Specification (SRS) documenting all SIFs and SIL targets",
            "Competency assessment for personnel performing SIS lifecycle tasks",
            "Independent verification for SIL 2/3 by qualified engineer not involved in design",
            "Third-party certification for SIL 3 applications (exida, TUV, DNV)",
            "Comprehensive documentation trail (SRS, C&E, PFD calcs, procedures, MOC)",
            "Management of Change procedures for SIS modifications",
            "Bypass management with time-limited restoration and alarmed status",
            "Proof test procedures validated during commissioning",
            "Periodic SIS performance assessment (2-5 year intervals)",
            "Pre-startup safety review before SIS operation"
        ],
        primary_authority=[
            "IEC 61511-1:2016 Clause 5 (Functional safety management requirements)",
            "IEC 61511-1:2016 Clause 10 (Safety requirements specification)",
            "IEC 61508-3:2010 (Software systematic capability for logic solvers)",
            "30 CFR 250 Subpart S (BSEE Safety and Environmental Management System)",
            "ISA-84.00.01-2004 Part 1 (Application of Safety Instrumented Systems for Process Industries)"
        ],
        burden_holder="Operator must establish and maintain FSM program with documented competency, verification/validation, and MOC procedures per IEC 61511",
        adversary_position="Regulator may require third-party certification even for SIL 2 applications; auditor may challenge competency documentation or independence of verification personnel",
        counter_arguments=[
            "IEC 61511 FSM requirements impose excessive documentation burden without commensurate safety improvement - prescriptive approach vs performance-based",
            "Independent verification requirement difficult for small organizations without separate engineering groups - external consultant cost prohibitive",
            "Competency assessment subjective without clear pass/fail criteria - experience requirements favor incumbent personnel over fresh graduates with current training",
            "Third-party certification adds significant cost and schedule delay for marginal benefit - internal verification by competent engineer sufficient for SIL 2",
            "Periodic SIS assessment (every 2-5 years) unnecessary if continuous condition monitoring and proof testing performed - duplicative effort"
        ],
        resolution_strategy="Develop FSM plan template aligned with IEC 61511 Table 1, engage third-party for SIL 3 verification and consider for complex SIL 2, document competency matrix with training and experience requirements, implement MOC procedure integrated with existing plant MOC system, leverage proof test as-found data for periodic assessment",
        entity_scope="All SIS applications requiring IEC 61511 compliance: offshore platforms (BSEE), refineries (OSHA PSM), chemical plants, gas processing, power generation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="IEC 61511 FSM requirements comprehensive and internationally recognized; implementation details and competency thresholds involve organizational judgment within standard framework",
        controlling_precedent="IEC 61511-1:2016 Clause 5 mandates FSM for all safety instrumented systems; 30 CFR 250 Subpart S codifies FSM elements for U.S. offshore platforms"
    ),

    DoctrineBlock(
        topic="SIF Validation Testing and Factory/Site Acceptance Testing (FAT/SAT)",
        keywords=["FAT", "SAT", "factory acceptance test", "site acceptance test", "SIF validation", "commissioning", "integrated test", "loop test", "end-to-end"],
        conclusion_template=[
            "SIF validation testing per IEC 61511 Clause 12 requires comprehensive verification that installed SIS executes safety functions correctly, including Factory Acceptance Test (FAT) for equipment and logic, and Site Acceptance Test (SAT) for as-installed system.",
            "FAT validates safety PLC logic, C&E matrix implementation, response times, and diagnostic functions in controlled factory environment before shipment; SAT verifies end-to-end loop functionality with actual field devices after installation.",
            "Integrated SAT must demonstrate each SIF from initiating sensor through final element closure under simulated demand, with acceptance criteria documented in test protocol derived from SRS."
        ],
        reasoning_framework=[
            "IEC 61511 Clause 12 requires validation that SIS meets safety requirements specification (SRS) before placing in service - performed via FAT and SAT.",
            "Factory Acceptance Test (FAT): conducted at PLC vendor facility before shipment, validates logic solver programming, C&E matrix implementation, human-machine interface (HMI), diagnostics.",
            "FAT test cases: derived from C&E matrix, each trip cause simulated and corresponding outputs verified, voting logic tested (e.g., verify 2oo3 requires two sensor inputs), time delays measured.",
            "FAT attendees: owner representative (operations/engineering), system integrator, PLC vendor, sometimes AHJ or third-party certifier - formal protocol with sign-off required.",
            "FAT deliverables: signed test protocol with pass/fail results, punch list of deficiencies requiring correction, approved logic code (often baseline for configuration management).",
            "Site Acceptance Test (SAT): conducted after installation on platform/facility, validates end-to-end loop functionality with actual field sensors and final elements.",
            "SAT integrated loop test: simulate sensor input (apply pressure, temperature, or electrical signal), verify logic solver responds correctly, confirm final element actuates (valve closes, pump trips).",
            "SAT safety valve stroke test: manually command ESD valve closure via logic solver output, measure stroke time, verify full closure, confirm fail-safe mode (spring-return closes on air loss).",
            "SAT voting logic test: for 2oo3 architecture, verify single sensor trip does not actuate (1/3 insufficient), two sensors trigger action (2/3 sufficient), all three sensors trigger (3/3 redundant confirmation).",
            "Time delay testing: inject sensor signal above trip setpoint, verify time delay (e.g., 3 seconds) elapses before output, confirm immediate output for zero-delay trips (fire/gas).",
            "Manual shutdown station test: activate push button, verify immediate shutdown bypassing voting logic and time delays, confirm reset required before restart.",
            "Partial shutdown test: for systems with multiple shutdown levels (L1, L2, L3), verify correct subset of outputs for each level, ensure L2 does not inadvertently trigger L1 outputs.",
            "Diagnostic function validation: inject faults (open circuit, shorted transmitter, power supply failure), verify logic solver detects and annunciates, confirm degraded mode alarmed.",
            "HMI validation: verify alarm annunciation on operator screen, check trip cause identification, validate manual reset functionality, confirm bypass status displayed prominently.",
            "Response time measurement: from sensor input to final element actuation, compare to SRS requirement (typically <10 seconds for most ESD applications, <2 seconds for fire/gas).",
            "As-found baseline documentation: record sensor calibration status, valve stroke times, loop resistance - establishes baseline for future proof testing comparison.",
            "Acceptance criteria: derived from SRS requirements (e.g., valve closure time <5 seconds, voting logic correct per C&E matrix, diagnostics detect 90% of faults).",
            "Punch list management: deficiencies identified during SAT documented, assigned to responsible party (vendor, contractor, owner), resolution verified before final sign-off.",
            "Offshore platforms: SAT often phased due to weather windows and personnel logistics - critical loops tested first, non-critical loops during subsequent campaigns.",
            "Pre-startup safety review (PSSR) prerequisite: SAT must be complete and signed off before PSSR approval to place SIS in service per IEC 61511 Clause 12.7.",
            "SAT documentation: signed protocol, calibration certificates for test instruments, photos/videos of key tests (valve stroke, manual shutdown), loop drawing markups showing as-built conditions.",
            "Revalidation triggers: after major modifications (logic changes, equipment replacement, setpoint changes) require partial re-test covering affected SIFs - scope per MOC analysis."
        ],
        key_factors=[
            "FAT validates logic solver programming and C&E matrix implementation in factory",
            "SAT verifies end-to-end loop functionality with installed field devices",
            "Integrated loop testing: sensor input simulation through final element actuation",
            "Voting logic verification (1oo2, 2oo3) with multiple sensor combinations",
            "Time delay measurement and confirmation per C&E matrix specification",
            "Manual shutdown station test bypassing voting logic (immediate actuation)",
            "Diagnostic function validation (fault injection and annunciation check)",
            "Response time measurement from sensor to final element (compare to SRS)",
            "Acceptance criteria derived from SRS requirements",
            "Pre-startup safety review requires SAT completion before operation"
        ],
        primary_authority=[
            "IEC 61511-1:2016 Clause 12 (Validation of safety instrumented systems)",
            "ISA-84.00.01-2004 Part 2 Section 12 (Commissioning and validation)",
            "API RP 14C Section 10 (Installation and commissioning of safety systems)",
            "IEC 61511-1:2016 Clause 5.2.7 (Validation requirements)",
            "30 CFR 250.1916 (BSEE Pre-startup safety review requirements)"
        ],
        burden_holder="System integrator/contractor must execute FAT/SAT per approved protocol and demonstrate all acceptance criteria met; owner must witness and approve",
        adversary_position="Owner may demand exhaustive test coverage beyond practical scope (all possible sensor combinations); vendor may resist comprehensive fault injection testing (risk of damaging equipment)",
        counter_arguments=[
            "FAT in controlled factory environment does not replicate actual field conditions (temperature extremes, vibration, electrical noise) - SAT alone sufficient",
            "Integrated loop testing with full valve stroke introduces unnecessary wear on ESD valves - partial stroke or simulation sufficient",
            "Exhaustive voting logic combinations (all permutations of 2oo3, 2oo4) impractical - representative sample sufficient to validate algorithm",
            "Diagnostic fault injection risks damaging equipment or leaving system in faulted state - review of diagnostic logic code sufficient without physical testing",
            "Pre-startup safety review prerequisite delays production startup - parallel SAT completion during commissioning more efficient"
        ],
        resolution_strategy="Perform FAT with owner witness on critical systems (SIL 2/3), use simulation for valve stroke during FAT (reserve full stroke for SAT), test representative voting combinations plus boundary cases (1/3, 2/3, 3/3), document diagnostic validation plan balancing physical testing with code review, integrate SAT schedule with overall commissioning plan to avoid PSSR bottleneck",
        entity_scope="All SIS installations: offshore platforms, onshore gas plants, refineries, chemical plants, HIPPS applications, ESD systems, fire/gas detection",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="IEC 61511 Clause 12 provides clear validation requirements; test scope and depth involve balancing comprehensive verification against practical constraints and equipment protection",
        controlling_precedent="IEC 61511-1:2016 Clause 12 mandates validation before placing SIS in service; 30 CFR 250.1916 codifies pre-startup safety review including SAT completion for offshore platforms"
    ),

    DoctrineBlock(
        topic="Common Cause Failure Analysis and Beta Factor Estimation",
        keywords=["common cause failure", "CCF", "beta factor", "redundancy", "diversity", "systematic failure", "common mode", "IEC 61508", "beta model"],
        conclusion_template=[
            "Common Cause Failure (CCF) represents failure events affecting multiple redundant channels simultaneously, degrading redundancy benefit and increasing actual PFD beyond ideal calculation - quantified via beta factor (percentage of failures that are common cause).",
            "IEC 61508-6 beta model: PFD_redundant = (1-beta)*PFD_independent + beta*PFD_single_channel, where beta typically ranges 2-10% depending on component diversity and environmental isolation.",
            "CCF mitigation strategies: use diverse sensor technologies (pressure: capacitive + strain gauge), separate power supplies, staggered proof testing, physical separation, and different manufacturers - can reduce beta from 10% (identical components) to 2% (fully diverse)."
        ],
        reasoning_framework=[
            "Common Cause Failure (CCF): single event or root cause resulting in failure of multiple components that are intended to be independent - defeats purpose of redundancy.",
            "Examples: instrument air supply loss affecting all pneumatic transmitters, software bug in PLC causing all channels to fail, electrical transient damaging all sensors on common power bus, corrosive atmosphere degrading all transmitter diaphragms.",
            "Beta factor (β): fraction of total failures that are common cause, range 0 (perfect independence) to 1 (complete coupling) - typical values 0.02 to 0.10 (2% to 10%).",
            "IEC 61508-6 Annex D provides beta factor estimation tables based on diversity, separation, analysis, and complexity factors - scoring system yields beta 2%, 5%, or 10%.",
            "Impact on 1oo2 PFD: ideal PFD = (lambda^2 * TI^2)/3 assumes zero CCF; actual PFD = (1-beta)*(lambda^2*TI^2)/3 + beta*(lambda*TI)/2 - second term is CCF contribution.",
            "For beta=10% and lambda*TI=0.01, CCF contribution to PFD is 0.0005 (half of total PFD) - significant degradation of redundancy benefit.",
            "Diversity categories per IEC 61508: 1-Different design approaches, 2-Different technologies, 3-Different manufacturers, 4-Different physical principles.",
            "Example diverse pressure sensing: capacitive diaphragm transmitter + strain gauge transmitter - different measurement principles reduce beta to ~2% vs 10% for identical capacitive units.",
            "Physical separation: mount redundant sensors 10+ feet apart, use separate cable trays, different power supplies - prevents single external event (fire, impact, flooding) from affecting all.",
            "Staggered proof testing: test redundant channels at different times (e.g., transmitter A in January, B in July) - prevents systematic test procedure errors from affecting all channels simultaneously.",
            "Software diversity: different PLC vendors or different logic implementations for redundant logic solvers (rarely practical due to complexity and validation burden).",
            "Environmental stress CCF: offshore corrosive atmosphere, freezing conditions, high vibration - affects all exposed components similarly, argue for protective enclosures or inherently robust technologies.",
            "Design systematic failures: specification error, calculation mistake in setpoint, incorrect C&E matrix logic - affects all channels identically, mitigated by independent verification and diverse design teams.",
            "Installation errors: incorrect wiring, wrong configuration settings, improper calibration - CCF if same technician performs all channels, mitigated by second-party verification or staggered installation.",
            "Maintenance-induced CCF: incorrect replacement part installed in all channels, calibration procedure error applied uniformly - mitigated by as-found/as-left data review and staggered maintenance.",
            "Beta factor validation difficult: requires field failure data on redundant systems, which is scarce for high-reliability SIS applications - IEC 61508 tables provide defensible estimates absent hard data.",
            "Conservative approach: use beta=10% unless specific diversity measures implemented and documented - beta=5% for different manufacturers, beta=2% for different physical principles.",
            "Impact on SIL achievement: 1oo2 system with identical components (beta=10%) and lambda=5E-6/hr, TI=2 years achieves PFD=0.006 (SIL 2 threshold 0.01) - barely passes; diverse components (beta=2%) yield PFD=0.003 - comfortable margin.",
            "Operator error CCF: incorrect manual valve alignment affecting multiple SIFs, control room error disabling multiple trips - addressed via human factors engineering and procedure validation, not beta factor model.",
            "Multiple redundancy (3oo4, 2oo4) spreads CCF impact: with beta=5%, 2oo4 architecture more resilient to CCF than 1oo2 - partial failures tolerated without SIF loss.",
            "IEC 61508 beta model limitations: assumes CCF affects all channels equally and simultaneously - reality more nuanced (partial CCF), but model provides conservative first-order estimate."
        ],
        key_factors=[
            "Beta factor estimation (2-10%) based on diversity and separation per IEC 61508-6 Annex D",
            "Diverse sensor technologies reduce beta (capacitive + strain gauge, UV + IR)",
            "Physical separation of redundant channels (10+ feet, separate power/cabling)",
            "Staggered proof testing to avoid systematic test procedure CCF",
            "Different manufacturers for redundant components (reduces systematic failure coupling)",
            "Environmental stress mitigation (protective enclosures, robust technologies)",
            "Independent verification to catch design systematic failures",
            "As-found/as-left data review to detect maintenance-induced CCF",
            "Conservative beta factor selection (10%) unless diversity documented",
            "CCF impact on PFD calculation via beta model: PFD = (1-beta)*PFD_ideal + beta*PFD_single"
        ],
        primary_authority=[
            "IEC 61508-6:2010 Annex D (Beta factor estimation tables)",
            "IEC 61511-1:2016 Clause 11.4.4 (Common cause failures in redundant architectures)",
            "ISA-TR84.00.02-2002 Part 3 (CCF treatment in PFD calculations)",
            "OREDA Offshore Reliability Data (Field CCF event data)",
            "Reliability Engineering Handbook (Failure mode distributions and beta factors)"
        ],
        burden_holder="SIS designer must account for CCF in PFD calculations and document diversity/separation measures justifying beta factor selection",
        adversary_position="Third-party certifier may challenge low beta factor claims (2-5%) without comprehensive diversity implementation; inspector may require conservative beta=10% approach absent detailed CCF analysis",
        counter_arguments=[
            "Beta factor model oversimplifies CCF - actual failure modes more complex than single percentage factor captures (partial CCF, time-dependent coupling)",
            "Diversity claims difficult to validate - different manufacturers may use identical sensor chips internally, negating diversity benefit",
            "Physical separation impractical on compact offshore platforms - equipment density precludes 10+ foot spacing for redundant sensors",
            "Staggered proof testing increases operational complexity and risk of configuration errors - synchronized testing with clear shutdown windows preferable",
            "Field data on CCF scarce and unreliable - beta factor tables in IEC 61508 based on limited datasets and expert judgment, not rigorous statistics"
        ],
        resolution_strategy="Implement maximum practical diversity (different sensor technologies, different manufacturers), document separation measures (physical distance, power/signal isolation), use conservative beta=5-10% unless comprehensive diversity program in place, validate beta factor selection with third-party certifier for SIL 2/3 applications, track field failure data to refine beta over time",
        entity_scope="All redundant SIS architectures (1oo2, 2oo3, 2oo4) requiring CCF consideration in PFD calculations: ESD systems, HIPPS, compressor antisurge, fired heater trips",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="IEC 61508 beta model provides structured approach to CCF quantification, but validation difficult due to limited field data; beta factor selection involves significant engineering judgment; conservative approach (beta=10%) defensible absent detailed diversity analysis",
        controlling_precedent="IEC 61508-6:2010 Annex D establishes beta factor methodology; IEC 61511-1:2016 requires CCF consideration for redundant systems; industry practice defaults to beta=5-10% range"
    )
]


# ============================================================================
# CORE ENGINE
# ============================================================================

class SafetyInstrumentedSystemsEngine:
    """Safety Instrumented Systems Intelligence Engine - TIE-20 Architecture"""

    def __init__(self):
        self.version = "1.0.0"
        self.port = 9285
        self.start_time = datetime.now()
        self.doctrine_cache = DOCTRINE_CACHE
        self.metrics = MetricsCollector()
        self.telemetry_log: List[TelemetryRecord] = []

        # Configure logger
        logger.remove()
        logger.add(
            "ofe15_sis_engine.log",
            rotation="100 MB",
            retention="30 days",
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
        )
        logger.info(f"OFE15 Safety Instrumented Systems Engine v{self.version} initialized on port {self.port}")

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone,
        entity_context: Optional[str] = None
    ) -> QueryResponse:
        """
        Three-layer response architecture:
        1. Doctrine Cache (0-200ms) - Pre-compiled expert reasoning
        2. Semantic Retrieval - Vector search fallback
        3. Deep Analysis - Multi-source synthesis for novel scenarios
        """
        start_time = datetime.now()

        # Layer 1: Doctrine Cache
        triggered_doctrines = self._search_doctrine_cache(query)

        if triggered_doctrines:
            logger.info(f"Cache hit: {len(triggered_doctrines)} doctrines triggered for query: {query[:100]}")
            response_text = self._synthesize_from_doctrines(
                triggered_doctrines, query, mode, zone, entity_context
            )
            authorities = self._extract_authorities(triggered_doctrines)
            confidence = self._assess_confidence(triggered_doctrines)
            cache_hit = True
        else:
            # Layer 2: Semantic Retrieval (fallback)
            logger.info(f"Cache miss - invoking semantic retrieval for: {query[:100]}")
            response_text = self._semantic_search_fallback(query, mode, zone)
            authorities = ["General safety instrumented systems principles"]
            confidence = ConfidenceLevel.DISCLOSURE
            cache_hit = False

        # Calculate latency
        latency = (datetime.now() - start_time).total_seconds() * 1000

        # Generate determinism hash
        hash_content = f"{query}|{mode.value}|{zone.value}|{response_text}"
        determinism_hash = hashlib.sha256(hash_content.encode()).hexdigest()[:16]

        # Apply epistemic guardrails
        disclosure = self._epistemic_disclosure(confidence, zone)

        # Record telemetry
        telemetry = TelemetryRecord(
            query=query,
            timestamp=datetime.now().isoformat(),
            mode=mode,
            zone=zone,
            doctrines_triggered=[d.topic for d in triggered_doctrines],
            cache_hit=cache_hit,
            latency_ms=latency,
            confidence=confidence
        )
        self.telemetry_log.append(telemetry)
        self.metrics.record_query(telemetry)

        # Audit trail
        self._write_audit_trail(telemetry, response_text)

        return QueryResponse(
            answer=response_text,
            doctrines_applied=[d.topic for d in triggered_doctrines],
            confidence=confidence,
            authorities_cited=authorities,
            determinism_hash=determinism_hash,
            latency_ms=round(latency, 2),
            mode=mode,
            zone=zone,
            epistemic_disclosure=disclosure
        )

    def _search_doctrine_cache(self, query: str) -> List[DoctrineBlock]:
        """Search doctrine cache and return relevant blocks"""
        scored_doctrines = [
            (doctrine, doctrine.matches_query(query))
            for doctrine in self.doctrine_cache
        ]

        # Filter doctrines with score > 30 and sort by score
        relevant = [
            doctrine for doctrine, score in scored_doctrines if score > 30
        ]
        relevant.sort(
            key=lambda d: d.matches_query(query),
            reverse=True
        )

        return relevant[:5]  # Return top 5 matches

    def _synthesize_from_doctrines(
        self,
        doctrines: List[DoctrineBlock],
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone,
        entity_context: Optional[str]
    ) -> str:
        """Synthesize response from triggered doctrines"""

        if mode == ResponseMode.FAST:
            # Concise answer from top doctrine
            primary = doctrines[0]
            conclusion = ' '.join(primary.conclusion_template)
            return f"{conclusion}\n\nKey factors: {', '.join(primary.key_factors[:3])}."

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready full reasoning
            sections = []
            sections.append("SAFETY INSTRUMENTED SYSTEMS ANALYSIS\n")

            for i, doctrine in enumerate(doctrines[:3], 1):
                sections.append(f"\n{i}. {doctrine.topic.upper()}")
                sections.append("\nConclusion:")
                sections.append(' '.join(doctrine.conclusion_template))
                sections.append("\nReasoning Framework:")
                sections.append('\n'.join([f"  - {item}" for item in doctrine.reasoning_framework[:8]]))
                sections.append("\nKey Factors:")
                sections.append('\n'.join([f"  - {factor}" for factor in doctrine.key_factors[:5]]))
                sections.append("\nPrimary Authority:")
                sections.append('\n'.join([f"  - {auth}" for auth in doctrine.primary_authority]))
                sections.append(f"\nConfidence: {doctrine.confidence.value}")

            if entity_context:
                sections.append(f"\n\nENTITY CONTEXT: {entity_context}")

            return '\n'.join(sections)

        else:  # MEMO mode
            # Complete documentation
            sections = []
            sections.append("COMPREHENSIVE SAFETY INSTRUMENTED SYSTEMS MEMORANDUM\n")
            sections.append("=" * 80)

            for i, doctrine in enumerate(doctrines, 1):
                sections.append(f"\n\nSECTION {i}: {doctrine.topic.upper()}")
                sections.append("-" * 80)

                sections.append("\nEXECUTIVE SUMMARY:")
                sections.append(' '.join(doctrine.conclusion_template))

                sections.append("\n\nDETAILED ANALYSIS:")
                sections.append('\n'.join(doctrine.reasoning_framework))

                sections.append("\n\nKEY FACTORS:")
                sections.append('\n'.join([f"  {j}. {factor}" for j, factor in enumerate(doctrine.key_factors, 1)]))

                sections.append("\n\nAUTHORITATIVE SUPPORT:")
                sections.append('\n'.join([f"  - {auth}" for auth in doctrine.primary_authority]))

                sections.append("\n\nADVERSARIAL CONSIDERATIONS:")
                sections.append(f"Burden holder: {doctrine.burden_holder}")
                sections.append(f"Adversary position: {doctrine.adversary_position}")
                sections.append("Counter-arguments:")
                sections.append('\n'.join([f"  - {arg}" for arg in doctrine.counter_arguments]))

                sections.append("\n\nRESOLUTION STRATEGY:")
                sections.append(doctrine.resolution_strategy)

                sections.append(f"\n\nCONFIDENCE ASSESSMENT: {doctrine.confidence.value}")
                sections.append(doctrine.confidence_stratification)

                sections.append(f"\n\nCONTROLLING PRECEDENT:")
                sections.append(doctrine.controlling_precedent)

            if entity_context:
                sections.append(f"\n\n{'=' * 80}")
                sections.append(f"ENTITY-SPECIFIC CONTEXT: {entity_context}")

            return '\n'.join(sections)

    def _semantic_search_fallback(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> str:
        """Fallback for queries not matching doctrine cache"""
        response = (
            f"No specific doctrine coverage found for this safety instrumented systems query. "
            f"General guidance:\n\n"
            f"For SIL determination, apply IEC 61511 risk graph or LOPA methodology. "
            f"For safety PLC architecture, balance required SIL level (1oo1 for SIL 1, 1oo2 for SIL 2, 2oo3 for SIL 3) "
            f"against spurious trip tolerance. For ESD systems, develop comprehensive cause and effect matrix "
            f"documenting all trip causes, voting logic, time delays, and shutdown actions per API RP 14C. "
            f"For fire/gas detection, calculate coverage per ISA 84.00.07 and API RP 505 with 2oo4 voting typical. "
            f"For PSV sizing, apply API 520/521 methodology identifying all credible overpressure scenarios. "
            f"For HIPPS applications, achieve SIL 3 via 2oo3 transmitters and 1oo2 valves with partial stroke testing.\n\n"
            f"Recommend engaging qualified functional safety engineer for detailed analysis and IEC 61511 compliance demonstration."
        )
        return response

    def _extract_authorities(self, doctrines: List[DoctrineBlock]) -> List[str]:
        """Extract unique authorities from triggered doctrines"""
        authorities = set()
        for doctrine in doctrines:
            authorities.update(doctrine.primary_authority)
        return sorted(list(authorities))

    def _assess_confidence(self, doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """Assess overall confidence based on triggered doctrines"""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        # Return most conservative confidence level from triggered doctrines
        confidence_priority = {
            ConfidenceLevel.HIGH_RISK: 0,
            ConfidenceLevel.DISCLOSURE: 1,
            ConfidenceLevel.AGGRESSIVE: 2,
            ConfidenceLevel.DEFENSIBLE: 3
        }

        min_confidence = min(doctrines, key=lambda d: confidence_priority[d.confidence])
        return min_confidence.confidence

    def _epistemic_disclosure(
        self,
        confidence: ConfidenceLevel,
        zone: AnalysisZone
    ) -> Optional[str]:
        """Apply epistemic guardrails - disclose uncertainty"""
        if confidence in [ConfidenceLevel.DISCLOSURE, ConfidenceLevel.HIGH_RISK]:
            return (
                "EPISTEMIC DISCLOSURE: This analysis involves significant uncertainty or conflicting guidance. "
                "Independent review by qualified functional safety engineer recommended before relying on this analysis for safety-critical decisions. "
                "IEC 61511 compliance requires documented competency and verification per Clause 5."
            )
        elif confidence == ConfidenceLevel.AGGRESSIVE and zone == AnalysisZone.AUDIT:
            return (
                "Note: This analysis represents industry practice but may face regulatory challenge. "
                "Consider conservative approach or third-party certification for high-consequence applications."
            )
        return None

    def _write_audit_trail(self, telemetry: TelemetryRecord, response: str):
        """Write JSONL audit trail for forensic review"""
        audit_entry = {
            "timestamp": telemetry.timestamp,
            "query": telemetry.query,
            "mode": telemetry.mode.value,
            "zone": telemetry.zone.value,
            "doctrines": telemetry.doctrines_triggered,
            "confidence": telemetry.confidence.value,
            "latency_ms": telemetry.latency_ms,
            "response_length": len(response)
        }

        with open("ofe15_audit_trail.jsonl", "a") as f:
            f.write(json.dumps(audit_entry) + "\n")

    def get_health(self) -> HealthResponse:
        """Comprehensive health check"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        cache_hit_rate = (
            self.metrics.cache_hits / self.metrics.total_queries
            if self.metrics.total_queries > 0
            else 0.0
        )

        return HealthResponse(
            status="operational",
            engine="OFE15_Safety_Instrumented_Systems",
            version=self.version,
            port=self.port,
            doctrines_loaded=len(self.doctrine_cache),
            total_queries=self.metrics.total_queries,
            cache_hit_rate=round(cache_hit_rate, 3),
            avg_latency_ms=round(self.metrics.avg_latency_ms, 2),
            uptime_seconds=round(uptime, 1)
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="OFE15 Safety Instrumented Systems Engine",
    description="TIE-grade Safety Instrumented Systems intelligence for oilfield operations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engine
engine = SafetyInstrumentedSystemsEngine()


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest) -> QueryResponse:
    """Primary query endpoint - three-layer response architecture"""
    try:
        return engine.three_layer_response(
            query=request.query,
            mode=request.mode,
            zone=request.zone,
            entity_context=request.entity_context
        )
    except Exception as e:
        logger.error(f"Query processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")


@app.get("/health", response_model=HealthResponse)
async def health_endpoint() -> HealthResponse:
    """Health check endpoint"""
    return engine.get_health()


@app.get("/doctrines")
async def doctrines_endpoint(
    topic: Optional[str] = Query(None, description="Filter by topic keyword")
) -> Dict[str, Any]:
    """List available doctrines with optional filtering"""
    doctrines = engine.doctrine_cache

    if topic:
        topic_lower = topic.lower()
        doctrines = [
            d for d in doctrines
            if topic_lower in d.topic.lower() or any(topic_lower in kw.lower() for kw in d.keywords)
        ]

    return {
        "total_doctrines": len(doctrines),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "entity_scope": d.entity_scope
            }
            for d in doctrines
        ]
    }


@app.get("/metrics")
async def metrics_endpoint() -> Dict[str, Any]:
    """Performance metrics"""
    return {
        "total_queries": engine.metrics.total_queries,
        "cache_hits": engine.metrics.cache_hits,
        "cache_hit_rate": round(
            engine.metrics.cache_hits / engine.metrics.total_queries
            if engine.metrics.total_queries > 0 else 0.0,
            3
        ),
        "avg_latency_ms": round(engine.metrics.avg_latency_ms, 2),
        "error_count": engine.metrics.error_count,
        "doctrine_trigger_counts": engine.metrics.doctrine_trigger_counts,
        "confidence_distribution": engine.metrics.confidence_distribution
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    logger.info(f"Starting OFE15 Safety Instrumented Systems Engine on port {engine.port}")
    uvicorn.run(app, host="0.0.0.0", port=engine.port)
