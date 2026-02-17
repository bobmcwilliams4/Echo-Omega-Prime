"""
OFE06 - SCADA Monitoring & Control Engine
TIE Gold Standard - Oilfield Equipment Intelligence

SCADA/Automation expertise for oilfield operations:
- RTU/PLC programming and configuration
- Flow computers (ROC800, FloBoss, Omni)
- Modbus/DNP3/OPC protocols
- Radio/cellular/satellite telemetry
- Tank level and flow measurement
- EFM and API 21.1 compliance
- Alarm management and trending
- OT network cybersecurity

Port: 9006
Version: 1.0.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any, Literal
from enum import Enum
from dataclasses import dataclass, asdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn


# ============================================================================
# CONFIGURATION
# ============================================================================

APP = FastAPI(
    title="OFE06 SCADA Monitoring & Control Engine",
    version="1.0.0",
    description="TIE Gold Standard - Oilfield SCADA/Automation Intelligence"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.add(
    Path(__file__).parent / "logs" / "ofe06_{time:YYYY-MM-DD}.log",
    rotation="100 MB",
    retention="90 days",
    level="INFO"
)


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


class IssueCategory(str, Enum):
    RTU_CONFIGURATION = "RTU_CONFIGURATION"
    PLC_PROGRAMMING = "PLC_PROGRAMMING"
    FLOW_COMPUTER = "FLOW_COMPUTER"
    PROTOCOL_INTEGRATION = "PROTOCOL_INTEGRATION"
    TELEMETRY_SYSTEM = "TELEMETRY_SYSTEM"
    MEASUREMENT_SETUP = "MEASUREMENT_SETUP"
    ALARM_MANAGEMENT = "ALARM_MANAGEMENT"
    DATA_HISTORIAN = "DATA_HISTORIAN"
    CYBERSECURITY = "CYBERSECURITY"
    COMPLIANCE = "COMPLIANCE"
    TROUBLESHOOTING = "TROUBLESHOOTING"
    SYSTEM_DESIGN = "SYSTEM_DESIGN"


class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class DoctrineBlock:
    """Pre-compiled SCADA expertise block"""
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
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str

    def matches(self, query: str) -> float:
        """Calculate match score 0.0-1.0"""
        query_lower = query.lower()
        score = 0.0

        if self.topic.lower() in query_lower:
            score += 0.4

        keyword_matches = sum(1 for kw in self.keywords if kw.lower() in query_lower)
        score += (keyword_matches / len(self.keywords)) * 0.6

        return min(score, 1.0)


class QueryRequest(BaseModel):
    query: str = Field(..., description="SCADA/automation question")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(AnalysisZone.REPORTING, description="Analysis context")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")


class QueryResponse(BaseModel):
    query: str
    answer: str
    mode: ResponseMode
    zone: AnalysisZone
    confidence: ConfidenceLevel
    doctrines_triggered: List[str]
    reasoning_chain: Optional[List[str]] = None
    key_factors: Optional[List[str]] = None
    recommendations: Optional[List[str]] = None
    determinism_hash: str
    timestamp: str
    processing_time_ms: float


class HealthResponse(BaseModel):
    status: str
    version: str
    port: int
    doctrines_loaded: int
    categories: List[str]
    uptime_seconds: float


# ============================================================================
# DOCTRINE CACHE - REAL SCADA EXPERTISE
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [

    # RTU CONFIGURATION
    DoctrineBlock(
        topic="RTU Polling Interval Optimization",
        keywords=["RTU", "polling", "scan rate", "update interval", "optimization", "bandwidth"],
        conclusion_template="RTU polling intervals must balance data freshness against communication bandwidth and radio duty cycle. Critical parameters (alarms, safety shutdowns) require 1-5 second scans. Production data (flow, pressure, temperature) typically scans every 15-60 seconds. Cumulative values (daily volumes) can update hourly. Poll faster than needed and you waste bandwidth; poll too slow and you miss critical events or violate custody transfer requirements.",
        reasoning_framework="""
1. CRITICALITY ASSESSMENT: Categorize each point by operational importance
   - Safety/ESD points: 1-5 second scan (immediate alarm response)
   - Process control: 5-15 seconds (PID loop stability)
   - Production monitoring: 15-60 seconds (operator visibility)
   - Custody transfer: Per API/AGA standards (typically 1-minute)
   - Diagnostic data: 5-15 minutes (trend analysis)
   - Configuration/status: On change or hourly (minimal bandwidth)

2. COMMUNICATION CONSTRAINTS: Factor radio/cellular limits
   - Licensed radio (900 MHz): 9600-19200 baud typical
   - Unlicensed (Freewave): 115 kbps max, shared channel
   - Cellular 3G/4G: Good bandwidth but latency varies (200-800 ms)
   - Satellite (VSAT): 500 ms+ latency, expensive per-byte
   - Calculate: (points × bytes/point × scans/hour) must fit bandwidth budget

3. PROTOCOL EFFICIENCY: Modbus vs DNP3 message overhead
   - Modbus RTU: Compact but no timestamps, poll everything each scan
   - DNP3: Report-by-exception reduces traffic 60-90%
   - Use DNP3 Class 0 (static) for slow data, Class 1 (event) for alarms
   - Enable unsolicited responses for critical alarms (no polling delay)

4. POWER BUDGET: Solar/battery sites need conservative scans
   - Transmit power dominates RTU energy use
   - Polling every 60s vs 15s can double battery life
   - Use store-and-forward for non-critical data (hourly batches)

5. REGULATORY COMPLIANCE: API 21.1/AGA require specific intervals
   - Flow computer data: Minimum 1-minute averages for EFM
   - Alarm logs: Must capture event timestamp within 1 second
   - Daily volumes: Must snapshot at midnight local time (not UTC)
        """,
        key_factors=[
            "Point criticality (safety > control > monitoring)",
            "Radio bandwidth and duty cycle limits",
            "Protocol overhead (Modbus vs DNP3)",
            "Power budget for remote solar sites",
            "Custody transfer interval requirements (API 21.1)",
            "Network latency (satellite 500ms+, cellular 200-800ms)",
            "Report-by-exception vs polling efficiency"
        ],
        primary_authority=[
            "API 21.1 Flow Measurement Using EFM (1-minute minimum intervals)",
            "DNP3 IEEE 1815-2012 (report-by-exception and event classes)",
            "ISA-100.11a Wireless Systems for Industrial Automation",
            "Manufacturer specs: ROC800 supports 1-second to 1-hour scan groups"
        ],
        burden_holder="SCADA system designer",
        adversary_position="Faster polling is always better for data visibility",
        counter_arguments=[
            "Excessive polling wastes 70%+ of radio bandwidth on unchanged data",
            "Battery sites can't sustain 5-second polling (3x power vs 60-second)",
            "Cellular data costs scale with message count (overage charges)",
            "Modbus polls must read entire register block even if 1 point changed",
            "Network congestion from over-polling causes packet loss and retries"
        ],
        resolution_strategy="Use tiered scan groups: alarms at 1-5s (DNP3 unsolicited), control at 15s, monitoring at 60s, diagnostics at 5-15 minutes. Enable DNP3 report-by-exception for non-critical points to reduce traffic 80%. For satellite links, use store-and-forward with 15-minute batches except for critical alarms. Document scan rates in SCADA database and validate bandwidth usage with communication load analysis.",
        entity_scope="RTU configuration for all oilfield SCADA systems (well pads, tank batteries, compressor stations)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Industry standard practice with clear technical justification",
        controlling_precedent="API 21.1 custody transfer requirements plus bandwidth engineering fundamentals"
    ),

    DoctrineBlock(
        topic="Modbus Register Mapping Best Practices",
        keywords=["Modbus", "register map", "holding register", "input register", "coil", "addressing"],
        conclusion_template="Modbus register maps must follow logical address grouping, reserve expansion space, and document data types explicitly. Use 40001-49999 holding registers for read/write values (setpoints, configs), 30001-39999 input registers for read-only measurements. Group related points in contiguous blocks to enable efficient multi-register reads (FC03/FC04). Reserve 20% address space for future expansion. Document scale factors, units, and bit packing explicitly to avoid misinterpretation.",
        reasoning_framework="""
1. ADDRESS ALLOCATION STRATEGY: Logical grouping reduces polling overhead
   - Block 1 (40001-40100): Critical alarms and status (poll every 5s)
   - Block 2 (40101-40300): Process values (flow, pressure, temp) (poll every 60s)
   - Block 3 (40301-40400): Daily totalizers and counters (poll hourly)
   - Block 4 (40401-40500): Configuration registers (read on startup only)
   - Block 5 (40501-40999): RESERVED for future expansion (don't allocate)

   Single FC03 read of 100 registers is 10x faster than 100 individual FC03 reads.

2. DATA TYPE DOCUMENTATION: Avoid catastrophic misinterpretation
   - Specify byte order: Big-endian (Modicon) vs little-endian (rare)
   - Float representation: IEEE-754 32-bit in 2 registers (AB CD or CD AB order?)
   - Scaling: Is 40150 value "1234" actually 12.34 PSI (scale 0.01)?
   - Units: PSI vs kPa, °F vs °C, MCF vs cubic meters
   - Signed vs unsigned: Is 65535 actually -1 or max scale?

   Example disaster: Flow computer sends totalizer as UINT32 = 4,294,967,295 cubic feet.
   SCADA interprets as two INT16s = [65535, 65535] = invalid, logs zero flow.

3. FUNCTION CODE USAGE: Read-only vs read-write separation
   - FC01 (Read Coils): Discrete outputs (valve open/close commands)
   - FC02 (Read Discrete Inputs): Alarm states, limit switches (read-only)
   - FC03 (Read Holding Registers): Setpoints, configs, totals (read-write)
   - FC04 (Read Input Registers): Analog measurements (read-only)
   - FC06/FC16 (Write Single/Multiple Registers): Setpoint changes

   Never map same physical point to both holding and input registers (creates confusion).

4. EXPANSION PLANNING: Leave 20% gaps for future points
   - New flowmeter? No space in 40101-40300 block = must remap everything.
   - Pre-allocate blocks by equipment type (Tank 1 = 40200-40299, Tank 2 = 40300-40399).
   - Document "RESERVED" ranges in register map spreadsheet.

5. DIAGNOSTIC REGISTERS: Include health monitoring
   - RTU uptime counter (helps detect reboot loops)
   - Communication error count (diagnose radio link issues)
   - Analog input health bits (sensor failure detection)
   - Battery voltage and solar charge current (solar RTU sites)
        """,
        key_factors=[
            "Logical address grouping by scan rate and function",
            "Explicit data type and scaling documentation",
            "Byte order (big-endian vs little-endian) clarity",
            "Read-only (input registers) vs read-write (holding registers) separation",
            "20% reserved address space for expansion",
            "Multi-register read optimization (contiguous blocks)",
            "Diagnostic register inclusion (uptime, errors, health)"
        ],
        primary_authority=[
            "Modbus Application Protocol V1.1b3 (Modbus Organization)",
            "IEEE-754 floating-point standard for 32-bit floats",
            "ISA-5.1 Instrumentation Symbols and Identification",
            "Manufacturer documentation: ROC800 register map conventions"
        ],
        burden_holder="RTU programmer and SCADA integrator",
        adversary_position="Just map registers sequentially as needed, document later",
        counter_arguments=[
            "Sequential mapping without gaps requires complete remap when adding points",
            "Undocumented scaling causes operators to misread values by 10x-100x",
            "Mixed byte order between devices creates float parsing errors",
            "Poor grouping forces 50+ small Modbus reads instead of 5 large reads (10x slower)",
            "No diagnostic registers means remote sites fail silently until field visit"
        ],
        resolution_strategy="Create register map spreadsheet with columns: Address, Tag Name, Description, Data Type, Byte Order, Scale Factor, Units, Read/Write, Scan Group. Use Excel conditional formatting to highlight reserved ranges. Publish map in SCADA database and as PDF in RTU panel. Review and update map during commissioning and after any field changes.",
        entity_scope="All Modbus RTU/TCP devices in oilfield SCADA systems",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Engineering best practice with documented technical justification",
        controlling_precedent="Modbus specification plus decades of field experience"
    ),

    DoctrineBlock(
        topic="DNP3 Configuration for Oilfield SCADA",
        keywords=["DNP3", "outstation", "master", "event class", "unsolicited", "integrity poll"],
        conclusion_template="DNP3 offers significant advantages over Modbus for oilfield SCADA: report-by-exception reduces traffic 70-90%, timestamps provide event sequencing, and unsolicited responses enable sub-second alarm delivery. Configure outstations with Class 1 (high priority alarms), Class 2 (medium priority events), Class 3 (low priority data). Enable unsolicited responses for critical alarms. Set integrity poll interval to 5-15 minutes to catch any missed events. Use DNP3 Secure Authentication (SA) for cybersecurity.",
        reasoning_framework="""
1. EVENT CLASS ASSIGNMENT: Prioritize data delivery by importance
   - Class 0 (Static): Current values, read on integrity poll only (every 5-15 min)
   - Class 1 (High Priority): ESD alarms, safety shutdowns, critical equipment failures
     → Master polls Class 1 every 1-5 seconds OR uses unsolicited response
   - Class 2 (Medium Priority): Process alarms (high pressure, low flow, deviation)
     → Master polls every 15-30 seconds
   - Class 3 (Low Priority): Status changes (valve position, mode changes)
     → Master polls every 1-5 minutes

   Example: Tank high-level alarm = Class 1 (immediate response needed)
            Tank level value = Class 0 (static data, poll on integrity scan)

2. UNSOLICITED RESPONSE CONFIGURATION: Eliminate polling delay for alarms
   - Enable unsolicited for Class 1 events (alarm conditions)
   - Outstation sends event to master immediately when alarm occurs (1-2 second delivery)
   - Master sends confirmation (DNP3 ACK), outstation retries if no ACK (robust delivery)
   - Vs Modbus: Must wait for next poll cycle (15-60 second delay typical)

   Critical for safety: Unsolicited response delivers ESD alarm in <2 seconds vs 60 seconds with polling.

3. INTEGRITY POLL STRATEGY: Catch missed events without excessive traffic
   - Integrity poll (Class 0/1/2/3 all) every 5-15 minutes
   - Resynchronizes SCADA with RTU state if event was lost
   - Much lower bandwidth than Modbus constant polling (90% reduction typical)
   - Example: 200-point RTU with 10% change rate:
     * Modbus: 200 registers × 60 polls/hour = 12,000 reads/hour
     * DNP3: 20 events × 60/hour + 200 registers × 12 integrity/hour = 1,200+2,400 = 3,600 reads/hour (70% reduction)

4. TIMESTAMP UTILIZATION: Event sequencing and alarm analysis
   - DNP3 embeds timestamp in each event (resolution to 1 millisecond)
   - SCADA historian stores event time, not poll time (accurate trending)
   - Alarm sequence analysis: Which alarm occurred first? DNP3 knows, Modbus guesses.
   - Critical for post-incident investigation (safety events, equipment failures)

5. SECURE AUTHENTICATION (DNP3-SA): Prevent unauthorized control
   - DNP3-SA adds HMAC authentication to prevent command spoofing
   - Required for critical infrastructure (NERC-CIP, TSA pipeline security)
   - Configure symmetric keys (AES-256) in both master and outstation
   - Enable challenge-response for control commands (valve open/close, setpoint changes)
        """,
        key_factors=[
            "Event class assignment by priority (Class 1=alarms, Class 2=warnings, Class 3=status)",
            "Unsolicited response for critical alarms (sub-second delivery)",
            "Integrity poll interval (5-15 min to catch missed events)",
            "Timestamp accuracy for event sequencing",
            "70-90% bandwidth reduction vs Modbus polling",
            "DNP3 Secure Authentication for command verification",
            "Report-by-exception efficiency"
        ],
        primary_authority=[
            "IEEE 1815-2012 DNP3 specification",
            "DNP3 Secure Authentication v5 (DNP.org)",
            "NERC-CIP-005/007 cybersecurity requirements for critical infrastructure",
            "ISA-99/IEC 62443 industrial control system security"
        ],
        burden_holder="SCADA system designer and RTU programmer",
        adversary_position="Modbus is simpler and good enough for oilfield",
        counter_arguments=[
            "Modbus has no timestamps, can't determine alarm sequence in multi-alarm events",
            "Modbus polling delay = 15-60 seconds typical, DNP3 unsolicited = <2 seconds",
            "Modbus wastes 70-90% bandwidth reading unchanged values every poll",
            "Modbus has no authentication, vulnerable to command injection attacks",
            "DNP3 event classes enable tiered data delivery (critical data faster)"
        ],
        resolution_strategy="Migrate oilfield SCADA to DNP3 for all new RTU deployments. Configure Class 1 for all safety/alarm points with unsolicited enabled. Set integrity poll to 10 minutes. Use DNP3-SA for control commands on critical sites (production platforms, compressor stations). Maintain Modbus support for legacy flowmeters and PLCs until replacement. Document class assignments in SCADA database.",
        entity_scope="All RTU-based SCADA systems in oil and gas production and midstream",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Industry standard for modern SCADA with regulatory support",
        controlling_precedent="DNP3 IEEE standard plus NERC-CIP cybersecurity mandates"
    ),

    # FLOW COMPUTER CONFIGURATION
    DoctrineBlock(
        topic="ROC800 Flow Computer Setup for Custody Transfer",
        keywords=["ROC800", "flow computer", "EFM", "API 21.1", "AGA", "custody transfer", "orifice"],
        conclusion_template="ROC800 flow computers must comply with API 21.1 for custody transfer accuracy. Configure orifice flow per AGA-3 (natural gas) or API 14.3 (liquids). Set 1-minute flow average periods per API 21.1 requirement. Enable EFM archiving with 35-day minimum retention. Validate differential pressure transmitter calibration (0.5% accuracy required). Configure temperature and pressure compensation per AGA-8 (gas density) or API 11.1 (liquid density). Lock configuration with password protection and audit logging.",
        reasoning_framework="""
1. API 21.1 COMPLIANCE CHECKLIST: Custody transfer requirements
   - Flow averaging: 1-minute minimum period (can use shorter for control, but report 1-min for custody)
   - Data archiving: 35-day minimum retention of flow history
   - Audit trail: Log all configuration changes with timestamp and user
   - Security: Password-protect configuration access (prevent tampering)
   - Accuracy: Total uncertainty ≤2% for fiscal measurement (sensor + calculation)
   - Clock sync: ±2 seconds accuracy (use NTP or GPS time source)

2. AGA-3 ORIFICE FLOW CALCULATION: Natural gas measurement
   - Inputs required: Differential pressure (dP), static pressure (P), temperature (T), orifice diameter (d), pipe diameter (D)
   - Calculation: Flow = C × Y × (π/4) × d² × √(2 × ρ × dP)
     where C = discharge coefficient (function of Reynolds number, β = d/D)
           Y = expansion factor (compressibility correction)
           ρ = gas density (from AGA-8 equation of state using P, T, composition)

   - Critical: Gas composition (methane %, CO2, N2, H2S) affects density calculation
   - Update composition monthly or when gas source changes
   - ROC800 has AGA-3 1985 and 1992 calculation modes (use 1992 for accuracy)

3. TRANSMITTER CALIBRATION VALIDATION: Accuracy starts at sensor
   - Differential pressure: 0-100 inH2O typical, ±0.5% accuracy required
     * Zero check: Close block valves, verify 0.0 inH2O reading
     * Span check: Apply known pressure (test gauge), verify within 0.5%
     * Calibrate annually minimum (quarterly for critical custody transfer)

   - Static pressure: 0-1500 PSIG typical, ±0.2% accuracy
   - Temperature: RTD or thermocouple, ±1°F accuracy
     * Use 4-wire RTD for best accuracy (eliminates lead resistance error)

4. FLOW COMPUTER CONFIGURATION PARAMETERS: ROC800 setup
   - Meter run ID: Physical location and tag number
   - Orifice plate: Diameter (inches), material, tap type (flange, pipe, or radius)
   - Pipe: Diameter (inches), material (affects roughness)
   - Fluid: Gas or liquid, composition (for density calculation)
   - Flowing conditions: P and T ranges (configure alarms for out-of-range)
   - Calculation method: AGA-3 (gas), API 14.3 (liquid)
   - Averaging period: 1-minute for custody transfer
   - Alarm limits: Low flow, high flow, low dP (plugged orifice), high dP (damaged plate)

5. EFM DATA ARCHIVING AND RETRIEVAL: Historical flow records
   - ROC800 stores hourly and daily totals in flash memory (35 days minimum)
   - SCADA polls EFM data daily and archives to historian database
   - Monthly reporting: Generate custody transfer report from EFM archive
   - Audit trail: Configuration change log with timestamp, user, old/new values
   - Data export: Modbus, DNP3, or ROC protocol (proprietary) to SCADA
        """,
        key_factors=[
            "API 21.1 compliance (1-min averaging, 35-day retention, audit logging)",
            "AGA-3 orifice calculation with gas composition updates",
            "Transmitter calibration validation (dP ±0.5%, P ±0.2%, T ±1°F)",
            "Configuration lock with password protection",
            "EFM archiving and daily SCADA polling",
            "Clock synchronization (NTP or GPS, ±2 sec accuracy)",
            "Total uncertainty ≤2% for fiscal measurement"
        ],
        primary_authority=[
            "API 21.1 Flow Measurement Using Electronic Metering Systems",
            "AGA Report No. 3 Orifice Metering of Natural Gas (1992 edition)",
            "AGA Report No. 8 Compressibility and Supercompressibility of Natural Gas",
            "API 14.3 Orifice Metering of Liquids",
            "Emerson ROC800-Series Flow Computer User Manual"
        ],
        burden_holder="Measurement technician and custody transfer operator",
        adversary_position="Flow computer factory defaults are good enough",
        counter_arguments=[
            "Factory defaults use placeholder gas composition (100% methane), errors up to 5% with real gas",
            "1-hour averaging instead of 1-minute violates API 21.1 for custody transfer",
            "No transmitter calibration validation = sensor drift causes revenue loss",
            "No audit logging = configuration tampering undetectable",
            "35-day EFM retention not configured = lost data if SCADA polling fails"
        ],
        resolution_strategy="Commission ROC800 per manufacturer checklist and API 21.1 requirements. Validate all sensor calibrations before startup. Configure gas composition from laboratory analysis (update monthly). Enable 1-minute averaging and 35-day EFM retention. Set up SCADA polling for daily EFM retrieval. Lock configuration with password and enable audit trail. Document configuration in meter book with photos of orifice plate and transmitter nameplates.",
        entity_scope="All custody transfer flow measurement in oil and gas production and midstream",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Regulatory requirement with clear technical standards",
        controlling_precedent="API 21.1 industry standard plus contract custody transfer agreements"
    ),

    DoctrineBlock(
        topic="Flow Computer vs PLC for Custody Transfer",
        keywords=["flow computer", "PLC", "custody transfer", "EFM", "ROC", "FloBoss", "ControlLogix"],
        conclusion_template="Use dedicated flow computers (ROC800, FloBoss, Omni) for custody transfer, not general-purpose PLCs. Flow computers provide API 21.1 compliant EFM archiving, built-in AGA/API calculation libraries, and audit trails. PLCs lack these features and require extensive custom programming to achieve compliance. Flow computers have proven accuracy and reliability for fiscal measurement. PLCs are better suited for process control (pumps, valves, logic) while flow computers handle custody transfer measurement.",
        reasoning_framework="""
1. API 21.1 COMPLIANCE FEATURES: Flow computer vs PLC capability

   FLOW COMPUTER (ROC800, FloBoss 107, Omni 6000):
   - Built-in EFM archiving (35+ days, hourly/daily totals)
   - Pre-certified AGA-3, AGA-7, AGA-8 calculation libraries (no custom code needed)
   - Audit trail (configuration changes logged with timestamp and user)
   - Clock sync (NTP client, GPS receiver interface)
   - Security (password levels, lockout after failed attempts)
   - Data export (ROC protocol, Modbus, DNP3 with EFM structures)

   PLC (Allen-Bradley ControlLogix, Siemens S7):
   - No built-in EFM archiving (must program custom historian)
   - No pre-certified AGA/API libraries (must implement from scratch = months of work)
   - Limited audit trail (may log program changes but not config parameter changes)
   - Clock sync possible (NTP module) but not standard
   - Security varies (password protection available but not custody-transfer focused)
   - Data export requires custom Modbus/Ethernet-IP mapping

2. CALCULATION LIBRARY CERTIFICATION: Proven accuracy vs custom code risk
   - ROC800 AGA-3 library: Certified by manufacturer, field-proven in 100,000+ installations
   - PLC custom AGA-3 code: Requires independent verification, prone to implementation errors
   - Example error: Incorrect Reynolds number iteration in AGA-3 causes 1-3% flow error
   - Litigation risk: Custom PLC code has no audit trail of calculation verification

3. COST AND SCHEDULE ANALYSIS: Total cost of ownership
   - Flow computer: $3,000-$8,000 hardware + 2-4 days commissioning = $5,000-$12,000
   - PLC custody transfer: $2,000 hardware + 40-80 hours custom programming + verification testing = $15,000-$30,000
   - Ongoing: Flow computer firmware updates include calculation library updates (free)
              PLC custom code requires re-validation after any change ($5,000-$10,000 per update)

4. SEGREGATION OF DUTIES: Process control vs custody transfer
   - Flow computer: Dedicated to measurement, isolated from process control logic
     * If process PLC fails, flow measurement continues uninterrupted
     * Configuration changes to custody transfer require separate authorization

   - PLC combined: Process control and custody transfer in same processor
     * Process logic change (pump sequencing) could inadvertently affect flow calculation
     * No segregation for audit purposes (operator can modify both control and custody)

5. FIELD SUPPORT AND VENDOR ECOSYSTEM: Troubleshooting and parts availability
   - Flow computers: Specialist vendors (Emerson, Schneider Electric, ABB) with oilfield expertise
     * Field service techs familiar with AGA/API standards
     * Replacement parts stocked at oilfield supply houses

   - PLCs: Industrial automation vendors (Rockwell, Siemens) with limited oilfield custody transfer expertise
     * Field service techs unfamiliar with API 21.1 compliance requirements
     * Must train internal staff on custom custody transfer code
        """,
        key_factors=[
            "Built-in EFM archiving and audit trail (flow computer standard, PLC custom)",
            "Pre-certified AGA/API calculation libraries (flow computer yes, PLC no)",
            "Total cost of ownership (flow computer lower due to no custom programming)",
            "Segregation of custody transfer from process control",
            "Vendor support for oilfield measurement standards",
            "API 21.1 compliance out-of-box (flow computer) vs extensive customization (PLC)",
            "Litigation risk of unverified custom calculation code"
        ],
        primary_authority=[
            "API 21.1 Section 5.2 (recommends dedicated EFM devices for custody transfer)",
            "AGA Report No. 3 (specifies calculation methods, doesn't endorse PLC implementation)",
            "GPA Midstream 2145 (measurement equipment specifications for custody transfer)",
            "Industry practice: 95%+ of custody transfer uses dedicated flow computers"
        ],
        burden_holder="Facility owner and measurement technician",
        adversary_position="Modern PLCs can do anything a flow computer does",
        counter_arguments=[
            "PLCs require 40-80 hours custom programming vs 2-4 days flow computer commissioning",
            "Custom PLC code has no manufacturer certification (litigation exposure)",
            "No segregation of process control and custody transfer in PLC (audit risk)",
            "PLC lacks built-in EFM structures (must design custom database)",
            "Vendor support: PLC vendors don't specialize in oilfield measurement"
        ],
        resolution_strategy="Use dedicated flow computers (ROC800, FloBoss 107) for all custody transfer applications per API 21.1 recommendation. Reserve PLCs for process control (pump/compressor sequencing, vessel level control, safety shutdowns). Interface flow computer to PLC via Modbus for totalizer display on HMI, but keep custody transfer calculation in flow computer. Document segregation of duties in SCADA system architecture. Budget $5,000-$12,000 per flow computer installation vs $15,000-$30,000 for custom PLC solution.",
        entity_scope="All custody transfer measurement in oil and gas production, gathering, and pipelines",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Industry best practice with regulatory and contractual support",
        controlling_precedent="API 21.1 recommendations plus 30+ years field experience"
    ),

    # TELEMETRY SYSTEMS
    DoctrineBlock(
        topic="Radio Telemetry Frequency Selection for Oilfield SCADA",
        keywords=["radio", "telemetry", "frequency", "900 MHz", "licensed", "unlicensed", "FCC", "Freewave"],
        conclusion_template="Oilfield SCADA radio telemetry uses licensed (900 MHz, 450 MHz) or unlicensed (900 MHz ISM, 2.4 GHz) frequencies. Licensed frequencies provide interference protection and longer range (20-30 miles) but require FCC coordination ($2,000-$5,000 per site). Unlicensed ISM band is free but shared (interference risk) and limited to 1W transmit power (5-10 mile range). Use licensed for critical backhaul links and dense oilfield areas. Use unlicensed for short-hop well pad to tank battery links in remote areas.",
        reasoning_framework="""
1. LICENSED VS UNLICENSED FREQUENCY COMPARISON:

   LICENSED (900 MHz Industrial/Business Pool, 450 MHz):
   - FCC coordination required (frequency search, interference study, license fee)
   - Cost: $2,000-$5,000 per site (one-time), $500-$1,000 annual renewal
   - Interference protection: FCC prevents other users from operating on your frequency
   - Transmit power: Up to 100W (long range, 20-30 miles line-of-sight)
   - Bandwidth: 12.5 kHz or 25 kHz channel (sufficient for SCADA data rates)
   - Antenna height: Can use tall towers (200+ feet) without interference concerns
   - Best for: Critical backhaul, dense oilfield areas, long-distance point-to-point

   UNLICENSED (900 MHz ISM Band 902-928 MHz):
   - No FCC license needed (free to use)
   - Cost: $0 (included in radio hardware purchase)
   - Interference: Shared with other users (oilfield neighbors, industrial equipment, amateur radio)
   - Transmit power: Limited to 1W (5-10 miles range typical)
   - Bandwidth: Frequency hopping spread spectrum (FHSS) or direct sequence (DSSS)
   - Antenna height: No restrictions, but interference risk increases in populated areas
   - Best for: Short-hop links, remote areas with low user density, non-critical backup paths

2. PROPAGATION AND RANGE CALCULATION: Path loss analysis
   - Free space path loss: FSPL (dB) = 32.45 + 20×log(freq MHz) + 20×log(dist km)
   - Example: 900 MHz, 10 miles (16 km)
     FSPL = 32.45 + 20×log(900) + 20×log(16) = 32.45 + 59.08 + 24.08 = 115.6 dB

   - Link budget: TX power + TX antenna gain - path loss + RX antenna gain > receiver sensitivity
   - Licensed 100W (50 dBm) + 6 dBi Yagi - 115.6 dB + 6 dBi = -53.6 dBm at receiver
     vs. receiver sensitivity -110 dBm = 56.4 dB fade margin (excellent)

   - Unlicensed 1W (30 dBm) + 6 dBi - 115.6 dB + 6 dBi = -73.6 dBm at receiver
     vs. receiver sensitivity -110 dBm = 36.4 dB fade margin (marginal, will fail in rain/fog)

3. FCC COORDINATION PROCESS: Licensed frequency acquisition
   - Step 1: Frequency search ($500-$1,000) - Find available channels in your area
   - Step 2: Interference study - Calculate path loss to existing license holders
   - Step 3: FCC application (Form 601) - Submit technical details and coordination data
   - Step 4: License grant (30-90 days) - FCC issues 10-year renewable license
   - Cost: $2,000-$5,000 per site including frequency coordination consultant
   - Benefit: Legal protection from interference, can request FCC enforcement against violators

4. INTERFERENCE MITIGATION: Unlicensed band coexistence
   - Frequency hopping (FHSS): Radio switches channels 50-100 times/second
     * Reduces impact of narrowband interference (other radios, industrial noise)
     * Example: Freewave FGR2 uses 50-hop pattern across 902-928 MHz band

   - Directional antennas: Yagi or panel antennas (6-15 dBi gain)
     * Reduces received interference from off-axis sources
     * Focuses transmit power toward desired receiver (increases range)

   - Site survey: Use spectrum analyzer to identify interference sources before installation
     * Measure noise floor at 900 MHz (should be <-100 dBm)
     * Identify strong interferers (other radios, microwave ovens, motors)

5. HYBRID NETWORK ARCHITECTURE: Licensed backbone + unlicensed edge
   - Central site to repeater: Licensed 900 MHz (30 mile backhaul)
   - Repeater to well pads: Unlicensed 900 MHz (5-10 mile short hops)
   - Benefit: Licensed backhaul provides reliable core, unlicensed edge keeps cost down
   - Redundancy: Dual-path routing (if unlicensed link fails, data routes via alternate repeater)
        """,
        key_factors=[
            "Licensed frequency: FCC protection, 20-30 mile range, $2K-$5K per site cost",
            "Unlicensed ISM: Free, 5-10 mile range, interference risk",
            "Link budget calculation (path loss vs fade margin)",
            "FCC coordination process (30-90 days, frequency search + interference study)",
            "Frequency hopping spread spectrum for interference mitigation",
            "Hybrid architecture (licensed backbone, unlicensed edge)",
            "Spectrum analyzer site survey before deployment"
        ],
        primary_authority=[
            "FCC Part 90 Industrial/Business Pool Rules (licensed 900/450 MHz)",
            "FCC Part 15.247 Unlicensed ISM Band Rules (902-928 MHz)",
            "Telecommunications Industry Association (TIA) radio propagation models",
            "Manufacturer specs: Freewave FGR2, GE MDS 9710, Motorola Canopy"
        ],
        burden_holder="SCADA system designer and radio engineer",
        adversary_position="Unlicensed is free and works fine, no need for licensed",
        counter_arguments=[
            "Unlicensed 1W range fails in dense oilfield areas (interference from neighbors)",
            "Licensed provides FCC enforcement against interferers (legal protection)",
            "Unlicensed fails in rain/fog due to low fade margin (link outages)",
            "Licensed allows tall tower antennas (200+ feet) for 30+ mile range",
            "Unlicensed interference increases as oilfield activity grows (spectrum congestion)"
        ],
        resolution_strategy="Use licensed 900 MHz for critical backhaul links (central site to repeaters, long-distance point-to-point) and dense oilfield areas. Use unlicensed 900 MHz ISM for short-hop links (well pad to tank battery) in remote areas with low user density. Budget $2,000-$5,000 per licensed site for FCC coordination. Perform spectrum analyzer site survey before deployment to measure interference. Use frequency-hopping radios (Freewave FGR2) and directional antennas (6+ dBi) for unlicensed links. Document frequency assignments and link budgets in SCADA network design.",
        entity_scope="All radio-based oilfield SCADA telemetry systems",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Engineering best practice with regulatory framework",
        controlling_precedent="FCC Part 90 and Part 15 rules plus radio propagation fundamentals"
    ),

    DoctrineBlock(
        topic="Cellular SCADA vs Radio Telemetry",
        keywords=["cellular", "SCADA", "LTE", "4G", "5G", "radio", "cost comparison", "coverage"],
        conclusion_template="Cellular SCADA (4G/5G) offers easier deployment and no FCC licensing vs radio telemetry, but has higher recurring costs ($30-$80/month per site) and coverage gaps in remote oilfields. Use cellular for low-density sites (<20 RTUs) or areas with good coverage. Use radio telemetry for high-density oilfields (>50 RTUs) where 2-year payback justifies licensed frequency investment. Hybrid networks use cellular as backup for critical radio paths.",
        reasoning_framework="""
1. COST COMPARISON: Total cost of ownership over 5 years

   CELLULAR (4G/5G):
   - Hardware: $300-$800 per RTU (cellular modem + antenna)
   - Monthly service: $30-$80 per month per site (data plan)
   - 5-year cost per site: $800 + ($50/mo × 60 mo) = $3,800
   - 100-site network: $380,000 over 5 years
   - No FCC licensing or frequency coordination
   - No repeater infrastructure needed

   RADIO TELEMETRY (Licensed 900 MHz):
   - Hardware: $1,500-$3,000 per RTU (radio + antenna)
   - FCC license: $2,000-$5,000 per site (one-time, 10-year renewable)
   - Monthly service: $0 (no recurring charges)
   - Repeater sites: $10,000-$20,000 each (tower, radio, solar power)
   - 5-year cost per site: $3,000 + $3,000 (FCC) = $6,000 (amortized)
   - 100-site network: $600,000 (year 1) + $50,000 (3 repeaters) = $650,000 initial, then $0/year
   - Breakeven: 2-3 years vs cellular ($650K / $76K per year = 8.6 years... but)

   Correction: Radio amortized over 10+ years, cellular compounds.
   Year 5: Cellular = $380K total, Radio = $650K initial (no additional)
   Year 10: Cellular = $760K total, Radio = $650K + $50K (license renewals) = $700K
   Radio wins after year 8-9 for high-density networks.

2. COVERAGE ANALYSIS: Cellular gaps in remote oilfields
   - Urban/suburban: 95%+ 4G/5G coverage (cellular excellent)
   - Rural oilfield: 60-80% coverage (coverage gaps common)
   - Remote desert/mountain: 20-40% coverage (cellular unusable)

   - Radio telemetry: You control coverage (build repeaters where needed)
   - Cellular: Coverage depends on carrier infrastructure (AT&T, Verizon, T-Mobile)

   - Example: West Texas Permian Basin
     * Highway corridors: Good cellular (4G LTE, 10+ Mbps)
     * Remote lease roads: Spotty cellular (edge/3G, <1 Mbps, frequent outages)
     * Radio telemetry: 100% coverage with 3-4 repeater sites on hills

3. LATENCY AND RELIABILITY: Real-time control vs delayed polling
   - Cellular latency: 200-800 ms typical (4G), 20-50 ms (5G)
     * Acceptable for monitoring (hourly polling, data logging)
     * Marginal for real-time control (valve open/close, ESD shutdown)

   - Radio latency: 50-200 ms typical (direct link), 100-400 ms (via repeater)
     * Good for real-time control and alarm response

   - Reliability: Cellular can disconnect during tower handoff, network congestion
                 Radio provides consistent link once tuned (no handoffs)

4. DATA USAGE AND THROTTLING: Cellular plan limitations
   - Typical SCADA data: 1-10 MB per site per month (polling + alarms)
   - Cellular plans: Unlimited (throttled at 5-50 GB) or metered ($10 per GB overage)
   - Risk: Software bug or misconfiguration causes excessive polling
     * Example: RTU polls 1000 registers every 1 second instead of 60 seconds
     * Data usage: 100 KB/poll × 86,400 polls/day × 30 days = 259 GB/month
     * Overage charges: 259 GB × $10/GB = $2,590 vs $50 normal bill (52x overage)

5. CYBERSECURITY: Cellular vs radio attack surface
   - Cellular: Exposed to internet (requires VPN, firewall rules, device management)
     * SCADA traffic routed through carrier network (potential eavesdropping)
     * Must secure: VPN tunnel (IPsec or SSL), strong authentication, firmware updates

   - Radio: Private RF network (not internet-connected until central site)
     * Eavesdropping requires physical proximity (RF receiver tuned to your frequency)
     * Licensed frequency provides legal protection against unauthorized monitoring
     * Can add RF encryption (AES-256) for defense-in-depth
        """,
        key_factors=[
            "Cellular cost: $30-$80/month per site ($380K for 100 sites over 5 years)",
            "Radio cost: $6K per site initial, then $0/month ($650K for 100 sites, amortized over 10 years)",
            "Cellular coverage gaps in remote oilfields (20-40% in desert/mountain)",
            "Radio coverage: 100% with repeater infrastructure (you control deployment)",
            "Cellular latency 200-800 ms (marginal for real-time control)",
            "Radio latency 50-200 ms (good for control and alarms)",
            "Cellular data overage risk ($2,500+ per site if misconfigured)",
            "Cybersecurity: Cellular requires VPN, radio is private RF network"
        ],
        primary_authority=[
            "Cellular coverage maps: AT&T, Verizon, T-Mobile (verify before deployment)",
            "Radio propagation: ITU-R P.1546 (path loss models for rural areas)",
            "ISA-99/IEC 62443 cybersecurity for industrial control systems",
            "Industry practice: Large oilfield operators use radio for core SCADA, cellular for remote/backup"
        ],
        burden_holder="SCADA system designer and operations manager",
        adversary_position="Cellular is easier and cheaper than radio infrastructure",
        counter_arguments=[
            "Cellular monthly fees compound to exceed radio infrastructure cost after 5-8 years",
            "Cellular coverage gaps cause RTU outages in remote oilfields (40%+ of sites)",
            "Cellular data overages can spike to $2,500+ per site if misconfigured",
            "Cellular latency (200-800 ms) too slow for real-time ESD and control applications",
            "Cellular requires VPN and firewall management (adds IT complexity and cost)"
        ],
        resolution_strategy="Use cellular for low-density sites (<20 RTUs), areas with verified good coverage, and non-critical monitoring applications. Use radio telemetry for high-density oilfields (>50 RTUs), remote areas with poor cellular coverage, and real-time control applications. Consider hybrid: radio for core SCADA network, cellular as backup path for critical sites. Validate cellular coverage with field testing before deployment (don't rely on carrier maps). Budget $50/month per cellular site for data plan. Document coverage analysis and cost comparison in SCADA network design.",
        entity_scope="All oilfield SCADA telemetry system planning",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Engineering cost-benefit analysis with operational considerations",
        controlling_precedent="Total cost of ownership comparison plus coverage validation"
    ),

    # MEASUREMENT AND INSTRUMENTATION
    DoctrineBlock(
        topic="Tank Level Measurement Technology Selection",
        keywords=["tank level", "radar", "ultrasonic", "pressure", "float", "measurement", "accuracy"],
        conclusion_template="Select tank level measurement technology based on accuracy requirements, tank size, and fluid properties. Radar (26 GHz FMCW) provides ±1mm accuracy for custody transfer but costs $3,000-$8,000. Ultrasonic (±0.25% FS) works for most production tanks at $800-$2,000 but fails with foam or heavy vapors. Pressure transmitters (±0.1% FS) are cheapest ($300-$800) but require specific gravity compensation for accuracy. Float/tape gauges (±1/8 inch) are reliable but don't integrate to SCADA easily.",
        reasoning_framework="""
1. ACCURACY AND APPLICATION REQUIREMENTS:

   CUSTODY TRANSFER (API 3.1B Manual Gauging accuracy ±1/8 inch):
   - Radar 26 GHz FMCW: ±1 mm (0.04 inch) accuracy
     * Emerson Rosemount 5900S, Endress+Hauser Micropilot FMR67
     * Cost: $5,000-$8,000 per tank
     * Best for: Crude oil, condensate, refined products storage

   PRODUCTION MONITORING (±1% tank volume acceptable):
   - Ultrasonic: ±0.25% of full scale (e.g., ±3 inches on 100 foot tank)
     * Magnetrol Echotel 961, Siemens Sitrans LU
     * Cost: $800-$2,000 per tank
     * Best for: Produced water, oil storage, chemical tanks

   LEVEL SWITCHING (overfill/low-level alarms, ±6 inch accuracy acceptable):
   - Pressure transmitter: ±0.1% FS (e.g., ±1.2 inches on 100 foot tank)
     * Rosemount 3051, Yokogawa EJA
     * Cost: $300-$800 per tank
     * Best for: Well pad gun barrels, frac tanks, process vessels

2. TECHNOLOGY COMPARISON: Strengths and weaknesses

   RADAR (26 GHz Frequency-Modulated Continuous Wave):
   ✓ Highest accuracy (±1 mm)
   ✓ Unaffected by temperature, pressure, vapor, foam
   ✓ Non-contact (no moving parts, no tank entry for maintenance)
   ✓ Works with corrosive/toxic fluids (antenna isolated from process)
   ✗ Expensive ($5,000-$8,000)
   ✗ Requires tank nozzle (6 inch minimum for antenna)
   ✗ Calibration requires empty tank (measure tank bottom reference)

   ULTRASONIC (20-50 kHz sound waves):
   ✓ Good accuracy (±0.25% FS) for most applications
   ✓ Non-contact, no moving parts
   ✓ Moderate cost ($800-$2,000)
   ✓ Easy installation (threaded or flanged mounting)
   ✗ Fails with foam (sound absorbed, no echo)
   ✗ Fails with heavy vapors (hydrocarbon vapors attenuate sound)
   ✗ Temperature-sensitive (speed of sound changes with temp)
   ✗ Requires compensation for fluid density (vapor space)

   PRESSURE TRANSMITTER (Hydrostatic head measurement):
   ✓ Lowest cost ($300-$800)
   ✓ Proven reliability (no moving parts)
   ✓ Works in any fluid (oil, water, foam, vapor)
   ✓ Fast response (1-2 second update)
   ✗ Requires specific gravity compensation (SG varies with temperature and composition)
   ✗ Tank bottom must be sealed (no drain valve leakage)
   ✗ Requires tank height configuration (convert pressure to level)
   ✗ Affected by fluid density changes (emulsion, sediment, water cut)

   FLOAT/TAPE GAUGE (Mechanical float on perforated tape):
   ✓ Very accurate (±1/8 inch per API 3.1B)
   ✓ No power required (mechanical readout)
   ✓ Reliable (proven design, 50+ year life)
   ✗ No SCADA integration (manual reading or expensive encoder add-on)
   ✗ Moving parts (tape, float) require periodic maintenance
   ✗ Float can stick (sludge, wax, emulsion buildup)
   ✗ Requires tank entry for tape replacement (confined space hazard)

3. FLUID PROPERTY CONSIDERATIONS: Match technology to application

   CRUDE OIL / CONDENSATE (clean hydrocarbon liquid):
   - Best: Radar (custody transfer) or ultrasonic (production monitoring)
   - Avoid: Pressure (SG varies with temperature and water cut)

   PRODUCED WATER (water with oil emulsion, sediment):
   - Best: Radar (unaffected by emulsion) or pressure (if SG stable)
   - Avoid: Ultrasonic (foam from gas breakout absorbs sound)

   FOAM-PRONE FLUIDS (gas breakout, surfactant injection):
   - Best: Radar (penetrates foam) or pressure (measures total head)
   - Avoid: Ultrasonic (foam absorbs sound, no echo)

   CORROSIVE/TOXIC FLUIDS (H2S, acids, caustic):
   - Best: Radar (non-contact, antenna isolated) or ultrasonic (non-contact)
   - Avoid: Pressure (wetted transmitter requires special materials, $$)

4. INSTALLATION AND CALIBRATION: Practical considerations

   RADAR:
   - Mount on top of tank, nozzle centered (avoid interference from fill pipe, mixer)
   - Calibrate: Empty tank, measure distance to bottom, configure as reference
   - Validation: Fill tank to known level (manual tape gauge), verify radar reading
   - Maintenance: Clean antenna every 6-12 months (remove coating/buildup)

   ULTRASONIC:
   - Mount on top, minimum 12 inches above high-level (avoid splashing)
   - Configure: Tank height, fluid type (affects speed of sound correction)
   - Compensation: Temperature sensor for vapor space (correct speed of sound)
   - Troubleshooting: Foam = no echo, heavy vapors = weak echo (increase gain)

   PRESSURE:
   - Mount at tank bottom, flush-mount diaphragm preferred (avoid sludge buildup)
   - Calibrate: Zero with tank empty, span with tank full (measure actual height)
   - SG compensation: Measure fluid specific gravity, configure in transmitter
     Level (feet) = Pressure (PSI) / (SG × 0.433 PSI/foot)
   - Validate: Compare to manual tape gauge monthly
        """,
        key_factors=[
            "Radar: ±1mm accuracy, $5K-$8K, best for custody transfer",
            "Ultrasonic: ±0.25% FS accuracy, $800-$2K, fails with foam/vapors",
            "Pressure: ±0.1% FS accuracy, $300-$800, requires SG compensation",
            "Float/tape: ±1/8 inch accuracy, mechanical, no SCADA integration",
            "Fluid properties: foam, vapor, emulsion affect technology selection",
            "Installation: radar/ultrasonic top-mount, pressure bottom-mount",
            "Calibration: empty tank reference for radar, SG compensation for pressure"
        ],
        primary_authority=[
            "API 3.1B Manual Gauging of Petroleum and Petroleum Products",
            "API 2550 Measurement and Calibration of Upright Cylindrical Tanks",
            "ISA-5.1 Instrumentation Symbols and Identification",
            "Manufacturer specs: Rosemount 5900S radar, Magnetrol Echotel 961 ultrasonic"
        ],
        burden_holder="Instrumentation engineer and measurement technician",
        adversary_position="Pressure transmitters are cheapest and good enough for everything",
        counter_arguments=[
            "Pressure requires SG compensation (errors if SG changes with temperature or water cut)",
            "Pressure fails if tank bottom drain valve leaks (false low reading)",
            "Ultrasonic fails with foam (common in produced water tanks)",
            "Float/tape has no SCADA integration (manual reading or expensive encoder)",
            "Only radar provides custody transfer accuracy (±1mm per API 3.1B)"
        ],
        resolution_strategy="Use radar for custody transfer tanks (crude oil sales, condensate). Use ultrasonic for production monitoring (clean fluids, no foam). Use pressure transmitters for level switching and low-cost monitoring (validate SG monthly). Use float/tape as backup/reference gauge on critical tanks. Document technology selection rationale in P&ID and instrument data sheets. Budget $5K-$8K per radar, $800-$2K per ultrasonic, $300-$800 per pressure. Calibrate per manufacturer procedures and validate monthly against manual tape gauge.",
        entity_scope="All tank level measurement in oil and gas production, storage, and terminals",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Engineering best practice with technology-specific applications",
        controlling_precedent="API standards for custody transfer plus instrumentation fundamentals"
    ),

    # CYBERSECURITY
    DoctrineBlock(
        topic="OT Network Segmentation for SCADA Cybersecurity",
        keywords=["cybersecurity", "network segmentation", "OT", "IT", "firewall", "SCADA", "ICS"],
        conclusion_template="Segment SCADA/OT networks from corporate IT networks with defense-in-depth: DMZ with unidirectional gateways or data diodes for historian access, firewall rules limiting IT-to-OT traffic to read-only HMI/SCADA polling, and air-gap critical control networks (ESD, turbine control). Never allow direct internet access from SCADA RTUs or control systems. Use VPN with multi-factor authentication for remote access, and monitor all OT network traffic with IDS/IPS tuned for industrial protocols.",
        reasoning_framework="""
1. PURDUE MODEL NETWORK ARCHITECTURE: ISA-99/IEC 62443 standard

   LEVEL 0-1 (FIELD DEVICES - NO IT ACCESS):
   - RTUs, PLCs, flow computers, transmitters, valve actuators
   - Network: Isolated serial (Modbus RTU) or industrial Ethernet (EtherNet/IP, Profinet)
   - Security: Physical access control, no remote access, no internet

   LEVEL 2 (CONTROL SYSTEMS - RESTRICTED ACCESS):
   - SCADA servers, HMI workstations, OPC servers, historians
   - Network: Industrial control system (ICS) LAN, isolated from IT
   - Firewall: Between Level 2 and Level 3 (allow only specific HMI/SCADA traffic)
   - Security: Read-only access from Level 3 (IT), no write commands from IT

   LEVEL 3 (OPERATIONS MANAGEMENT - DMZ):
   - Historian mirror (read-only copy), reporting servers, engineering workstations
   - Network: DMZ between ICS and corporate IT
   - Data flow: Unidirectional gateway (data diode) from Level 2 historian to Level 3 mirror
     * Data flows ICS → IT (production data, alarms, trends)
     * No traffic flows IT → ICS (prevents malware/ransomware propagation)

   LEVEL 4-5 (ENTERPRISE IT - NO DIRECT OT ACCESS):
   - Corporate network, business applications (SAP, email, internet)
   - Network: Corporate LAN with internet access
   - Access to OT: Only via DMZ (read-only historian data), no direct ICS access

2. FIREWALL RULE DESIGN: Deny-by-default, allow specific traffic

   IT → OT FIREWALL (between Level 3 DMZ and Level 2 ICS):
   - DENY ALL by default (zero trust)
   - ALLOW TCP 102 from HMI workstation to SCADA server (Siemens S7 protocol, read-only)
   - ALLOW TCP 502 from OPC client to RTU (Modbus TCP polling, read-only registers)
   - ALLOW TCP 20000 from historian to OPC server (read-only data collection)
   - LOG ALL denied traffic (detect unauthorized access attempts)

   OT → IT FIREWALL (between Level 2 ICS and Level 3 DMZ):
   - ALLOW TCP 20000 from historian to DMZ mirror (data replication)
   - ALLOW UDP 123 from SCADA server to NTP server (time synchronization)
   - DENY all other traffic (no internet browsing from ICS workstations)

   REMOTE ACCESS VPN:
   - REQUIRE multi-factor authentication (MFA) - password + token/app
   - TERMINATE VPN in DMZ, not directly in ICS (inspect traffic before allowing into OT)
   - ALLOW only specific source IPs (vendor support, authorized engineers)
   - LOG all VPN sessions with timestamp, user, source IP, commands executed
   - DISABLE split tunneling (force all traffic through VPN, prevent malware sideload)

3. UNIDIRECTIONAL GATEWAY / DATA DIODE: Hardware-enforced one-way data flow

   TECHNOLOGY:
   - Physical layer isolation: TX fiber from ICS, RX fiber to IT (no physical path for IT→ICS traffic)
   - Replication: Historian in ICS publishes data, mirror in DMZ receives (application-layer replication)
   - Use cases: Historian data to IT reporting, alarm logs to SIEM, process data to analytics

   PRODUCTS:
   - Waterfall Unidirectional Gateway, Owl Cyber Defense Data Diode, Fend Foresight
   - Cost: $15,000-$50,000 per link

   BENEFIT:
   - Absolute protection: Ransomware/malware in IT network cannot traverse data diode to ICS
   - Compliance: Meets NERC-CIP, TSA pipeline security, and other regulations
   - Read-only: IT can view production data but cannot send commands to OT

4. INTRUSION DETECTION FOR INDUSTRIAL PROTOCOLS: Detect SCADA attacks

   IDS/IPS DEPLOYMENT:
   - Passive tap on ICS network (monitor Modbus, DNP3, OPC traffic)
   - Products: Nozomi Networks, Claroty, Dragos Platform, Cisco Cyber Vision
   - Signatures: Detect unauthorized Modbus writes, DNP3 control commands, OPC exploits

   ALERT EXAMPLES:
   - Modbus FC16 (write registers) from unknown IP → Unauthorized setpoint change attempt
   - DNP3 direct operate command outside maintenance window → Unexpected valve control
   - OPC DA connection from non-HMI workstation → Rogue client scanning ICS
   - Excessive Modbus polling (100+ requests/second) → Denial-of-service or network scan

5. PATCH MANAGEMENT AND VULNERABILITY REMEDIATION: Balance security and uptime

   CHALLENGE: SCADA systems can't reboot for patches (24/7 operations, downtime = lost production)

   STRATEGY:
   - Virtual patching: IPS rules block exploit traffic without patching vulnerable system
     * Example: OPC exploit CVE-2021-1234 → IPS drops packets matching exploit signature
   - Compensating controls: Network segmentation + firewall rules reduce attack surface
     * Example: Unpatched Windows XP HMI isolated from internet, only SCADA server can connect
   - Scheduled maintenance: Patch during planned outage (annual turnaround, quarterly maintenance)
   - Testing: Validate patches in lab environment before production deployment
        """,
        key_factors=[
            "Purdue Model: Levels 0-2 (OT) isolated from Levels 3-5 (IT)",
            "Firewall deny-by-default, allow only specific HMI/SCADA traffic",
            "Unidirectional gateway (data diode) for historian replication to IT",
            "VPN remote access with MFA, terminate in DMZ not ICS",
            "IDS/IPS for industrial protocols (Modbus, DNP3, OPC)",
            "Virtual patching and compensating controls for legacy systems",
            "Air-gap critical control networks (no IT access to ESD systems)"
        ],
        primary_authority=[
            "ISA-99/IEC 62443 Industrial Control System Security",
            "NERC-CIP Critical Infrastructure Protection (power grid)",
            "TSA Pipeline Security Directive (oil and gas pipelines)",
            "NIST SP 800-82 Guide to ICS Security",
            "Purdue Model for Industrial Control Systems"
        ],
        burden_holder="OT cybersecurity engineer and SCADA administrator",
        adversary_position="Flat network is simpler, firewall blocks productivity",
        counter_arguments=[
            "Colonial Pipeline ransomware (2021): IT network breach spread to OT, shut down pipeline for 6 days",
            "Triton/Trisis malware (2017): Targeted safety systems, could have caused catastrophic explosion",
            "Stuxnet (2010): Crossed air-gap via USB, destroyed centrifuges",
            "Flat network allows ransomware to encrypt SCADA servers (production shutdown)",
            "Direct internet access from RTU enables remote takeover (valve control, setpoint changes)"
        ],
        resolution_strategy="Implement Purdue Model network segmentation with Level 2 ICS isolated from Level 3-5 IT. Deploy firewall with deny-by-default rules between ICS and DMZ. Use unidirectional gateway for historian data replication to IT ($15K-$50K investment). Require VPN with MFA for remote access, terminate in DMZ. Deploy IDS/IPS for industrial protocols (Nozomi, Claroty, Dragos). Document network architecture in ICS security plan. Train operators on USB policy (no personal USB drives in ICS network). Perform annual penetration testing and vulnerability assessment.",
        entity_scope="All SCADA/ICS networks in oil and gas production, midstream, and downstream",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Cybersecurity best practice with regulatory requirements",
        controlling_precedent="ISA-99/IEC 62443 plus NERC-CIP and TSA mandates for critical infrastructure"
    ),

    # Additional doctrines covering remaining topics...

    DoctrineBlock(
        topic="SCADA Alarm Management - ISA-18.2 Principles",
        keywords=["alarm", "management", "ISA-18.2", "nuisance", "alarm flood", "rationalization"],
        conclusion_template="Effective SCADA alarm management follows ISA-18.2: alarms must be relevant (operator action required), unique (one cause = one alarm), timely (actionable within response time), and prioritized (critical > high > medium > low). Alarm flood (>10 alarms/10 minutes) overwhelms operators and masks critical alarms. Rationalize alarms during design: eliminate nuisance alarms (fleeting, chattering), set deadbands to prevent chatter, and use alarm shelving for maintenance. Target <6 alarms per operator per day for sustainable operations.",
        reasoning_framework="""
1. ISA-18.2 ALARM PHILOSOPHY: Alarm vs information

   ALARM (requires operator action):
   - Tank high-level alarm at 90% → Operator must stop fill or divert flow
   - Compressor high vibration → Operator must investigate and potentially shut down
   - ESD low pressure → Operator must diagnose cause and restore pressure

   INFORMATION (no action required):
   - Tank level 50% → Normal operation, no action needed
   - Compressor running status → Informational, not actionable
   - Daily totalizer value → Data logging, not alarm

   RULE: If no operator action is required, it's not an alarm (use HMI display instead).

2. ALARM PRIORITY CLASSIFICATION: ISA-18.2 severity levels

   CRITICAL (emergency, safety impact):
   - ESD system activation, fire/gas detection, catastrophic equipment failure
   - Operator response required: <1 minute
   - Audible: Distinct tone (horn), visual: Flashing red
   - Example: Tank overfill spill risk, H2S gas detection, compressor overspeed trip

   HIGH (abnormal, production impact):
   - Process deviation requiring intervention to prevent shutdown
   - Operator response required: <10 minutes
   - Audible: Chime, visual: Solid red
   - Example: High separator pressure, low flow rate, pump failure

   MEDIUM (off-normal, requires monitoring):
   - Process deviation that may escalate if not addressed
   - Operator response required: <1 hour
   - Audible: Optional, visual: Yellow
   - Example: Tank 80% level (trending toward 90% alarm), minor instrument failure

   LOW (advisory, no immediate action):
   - Notification of abnormal condition, no immediate consequence
   - Operator response required: <8 hours (next shift)
   - Audible: None, visual: Cyan or white
   - Example: Scheduled maintenance due, calibration reminder

3. ALARM RATIONALIZATION: Reduce nuisance alarms by 80%+

   NUISANCE ALARM TYPES:
   - Fleeting: Alarm activates for <10 seconds then clears (noise, transient)
     * Example: Pressure alarm triggers during pump startup (normal transient)
     * Fix: Add 10-30 second time delay (alarm only if condition persists)

   - Chattering: Alarm activates/clears repeatedly (oscillation around setpoint)
     * Example: Tank level alarm at 90.0 feet, level oscillates 89.8-90.2 feet
     * Fix: Add deadband (alarm at 90.0, clear at 89.5 feet = 0.5 foot hysteresis)

   - Standing: Alarm remains active for hours/days (operator ignores, normalizes)
     * Example: Instrument failure alarm for out-of-service equipment
     * Fix: Shelve alarm during maintenance, unshelve when back in service

   - Consequential: Single root cause triggers 10+ related alarms (alarm flood)
     * Example: Power failure → 50 alarms (pumps off, pressures low, levels high)
     * Fix: Suppress child alarms when parent alarm active (power fail = one alarm)

4. ALARM RATE BENCHMARKING: ISA-18.2 performance targets

   ACCEPTABLE ALARM RATE:
   - Average: <6 alarms per operator per 10-hour shift
   - Peak: <10 alarms per 10 minutes (alarm flood threshold)
   - Standing alarms: <5% of total alarm activations

   EXAMPLE CALCULATION:
   - 100-point SCADA system, 2 operators
   - Current: 50 alarms per day per operator = 500 total alarms/day
     * ISA-18.2: 50 alarms/day is 8.3x target (6 alarms/day)
     * Rationalization goal: Reduce to <60 total alarms/day

   - After rationalization:
     * Eliminated 60% of nuisance alarms (fleeting, chattering)
     * Reduced to 200 alarms/day total = 100 per operator = 16.7 per 10-hour shift
     * Still above target, need further reduction

5. ALARM SHELVING AND SUPPRESSION: Temporary alarm disable during maintenance

   SHELVING:
   - Operator temporarily disables alarm during planned maintenance
   - Example: Tank being cleaned → disable high/low level alarms
   - Automatic unshelve: After 8 hours or when operator logs out (prevent forgotten shelved alarms)
   - Audit trail: Log who shelved, when, and reason

   SUPPRESSION:
   - Logic-based alarm disable (not manual shelving)
   - Example: If pump is off, suppress pump discharge pressure alarm
   - Conditional suppression: If Mode=Maintenance, suppress all alarms for Unit 1
        """,
        key_factors=[
            "ISA-18.2 alarm philosophy: alarms require operator action",
            "Priority levels: Critical <1 min, High <10 min, Medium <1 hour, Low <8 hours",
            "Alarm rationalization: eliminate fleeting, chattering, standing, consequential alarms",
            "Target <6 alarms per operator per day (ISA-18.2 sustainable rate)",
            "Alarm flood threshold: >10 alarms per 10 minutes overwhelms operator",
            "Time delays and deadbands to reduce nuisance alarms 80%+",
            "Alarm shelving with audit trail and auto-unshelve"
        ],
        primary_authority=[
            "ISA-18.2 Management of Alarm Systems for the Process Industries",
            "EEMUA 191 Alarm Systems: A Guide to Design, Management and Procurement",
            "API RP 1167 Pipeline SCADA Alarm Management",
            "ASM Consortium alarm management benchmarking studies"
        ],
        burden_holder="SCADA system designer and operations supervisor",
        adversary_position="More alarms are better, operator can sort it out",
        counter_arguments=[
            "Alarm flood (>10 alarms/10 min) causes operator to miss critical alarm (BP Texas City 2005)",
            "Standing alarms cause alarm desensitization (operator ignores all alarms)",
            "Nuisance alarms account for 80% of total alarms but provide zero value",
            "Chattering alarms distract operator from real process deviations",
            "Unrationalized alarms lead to 50+ alarms/day per operator (ISA-18.2 target is <6)"
        ],
        resolution_strategy="Perform alarm rationalization per ISA-18.2: classify all alarms by priority, eliminate nuisance alarms (fleeting, chattering, standing), add time delays (10-30 sec) and deadbands (5-10% of range) to reduce chatter. Implement alarm shelving with audit trail for maintenance. Monitor alarm rate and target <6 alarms per operator per day. Review alarm performance quarterly and adjust setpoints/logic as needed. Document alarm philosophy and rationalization decisions in alarm management plan.",
        entity_scope="All SCADA alarm systems in oil and gas operations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Industry best practice with safety and operational benefits",
        controlling_precedent="ISA-18.2 standard plus incident investigation findings (BP Texas City, etc.)"
    ),

]


# ============================================================================
# TELEMETRY AND METRICS
# ============================================================================

class TelemetryCollector:
    """Track query performance and doctrine usage"""

    def __init__(self):
        self.queries_processed = 0
        self.total_processing_time_ms = 0.0
        self.doctrine_hit_counts: Dict[str, int] = {}
        self.errors: List[Dict[str, Any]] = []
        self.start_time = datetime.now()

    def record_query(self, processing_time_ms: float, doctrines_used: List[str], error: Optional[str] = None):
        """Record query metrics"""
        self.queries_processed += 1
        self.total_processing_time_ms += processing_time_ms

        for doctrine in doctrines_used:
            self.doctrine_hit_counts[doctrine] = self.doctrine_hit_counts.get(doctrine, 0) + 1

        if error:
            self.errors.append({
                "timestamp": datetime.now().isoformat(),
                "error": error,
                "doctrines_attempted": doctrines_used
            })

    def get_stats(self) -> Dict[str, Any]:
        """Get telemetry statistics"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        avg_time = self.total_processing_time_ms / self.queries_processed if self.queries_processed > 0 else 0

        return {
            "queries_processed": self.queries_processed,
            "average_processing_time_ms": round(avg_time, 2),
            "uptime_seconds": round(uptime, 2),
            "error_count": len(self.errors),
            "doctrines_triggered": len(self.doctrine_hit_counts),
            "top_doctrines": sorted(self.doctrine_hit_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        }


TELEMETRY = TelemetryCollector()


# ============================================================================
# CORE ENGINE LOGIC
# ============================================================================

def three_layer_response(query: str, mode: ResponseMode, zone: AnalysisZone) -> QueryResponse:
    """
    TIE-20 Component: Three-layer response strategy
    Layer 1: Doctrine cache (0-50ms)
    Layer 2: Semantic search (50-200ms) - not implemented yet
    Layer 3: Deep analysis (200ms+)
    """
    start_time = datetime.now()

    # Layer 1: Doctrine cache lookup
    matched_doctrines = []
    for doctrine in DOCTRINE_CACHE:
        score = doctrine.matches(query)
        if score > 0.3:  # Threshold for relevance
            matched_doctrines.append((score, doctrine))

    # Sort by match score
    matched_doctrines.sort(key=lambda x: x[0], reverse=True)

    if not matched_doctrines:
        # No doctrine match - generate generic response
        answer = generate_generic_response(query, mode, zone)
        confidence = ConfidenceLevel.DISCLOSURE
        doctrines_triggered = []
        reasoning_chain = ["No specific doctrine matched - providing general SCADA guidance"]
        key_factors = []
        recommendations = ["Consult manufacturer documentation", "Engage SCADA system integrator for detailed design"]
    else:
        # Use top-matching doctrines
        top_doctrines = [d for _, d in matched_doctrines[:3]]  # Top 3 matches
        answer = synthesize_answer(query, top_doctrines, mode, zone)
        confidence = top_doctrines[0].confidence
        doctrines_triggered = [d.topic for d in top_doctrines]
        reasoning_chain = [d.reasoning_framework[:200] + "..." for d in top_doctrines] if mode != ResponseMode.FAST else None
        key_factors = top_doctrines[0].key_factors if mode != ResponseMode.FAST else None
        recommendations = extract_recommendations(top_doctrines)

    processing_time = (datetime.now() - start_time).total_seconds() * 1000

    # Determinism hash
    hash_input = f"{query}|{mode}|{zone}|{','.join(doctrines_triggered)}"
    determinism_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

    response = QueryResponse(
        query=query,
        answer=answer,
        mode=mode,
        zone=zone,
        confidence=confidence,
        doctrines_triggered=doctrines_triggered,
        reasoning_chain=reasoning_chain,
        key_factors=key_factors,
        recommendations=recommendations,
        determinism_hash=determinism_hash,
        timestamp=datetime.now().isoformat(),
        processing_time_ms=round(processing_time, 2)
    )

    TELEMETRY.record_query(processing_time, doctrines_triggered)

    return response


def generate_generic_response(query: str, mode: ResponseMode, zone: AnalysisZone) -> str:
    """Generate response when no doctrine matches"""
    return f"Your SCADA question about '{query}' doesn't match specific pre-compiled expertise blocks. For detailed guidance on SCADA systems, RTU configuration, flow computers, telemetry, or cybersecurity, please consult manufacturer documentation or engage a SCADA system integrator. General best practices include following ISA/API standards, validating sensor calibrations, implementing defense-in-depth cybersecurity, and documenting all configuration changes with audit trails."


def synthesize_answer(query: str, doctrines: List[DoctrineBlock], mode: ResponseMode, zone: AnalysisZone) -> str:
    """Synthesize answer from matched doctrines"""
    primary = doctrines[0]

    if mode == ResponseMode.FAST:
        # Concise response
        return primary.conclusion_template

    elif mode == ResponseMode.DEFENSE:
        # Audit-ready detailed response
        answer_parts = [
            f"SCADA Analysis: {primary.topic}",
            "",
            "CONCLUSION:",
            primary.conclusion_template,
            "",
            "KEY TECHNICAL FACTORS:",
        ]
        answer_parts.extend(f"  • {factor}" for factor in primary.key_factors)
        answer_parts.extend([
            "",
            "AUTHORITATIVE STANDARDS:",
        ])
        answer_parts.extend(f"  • {auth}" for auth in primary.primary_authority)
        answer_parts.extend([
            "",
            "CONFIDENCE ASSESSMENT:",
            f"  {primary.confidence_stratification}",
            "",
            "RECOMMENDED ACTION:",
            f"  {primary.resolution_strategy}"
        ])

        return "\n".join(answer_parts)

    else:  # MEMO mode
        # Full documentation with reasoning
        answer_parts = [
            f"SCADA ENGINEERING MEMORANDUM",
            f"Topic: {primary.topic}",
            f"Zone: {zone.value}",
            "",
            "EXECUTIVE SUMMARY:",
            primary.conclusion_template,
            "",
            "TECHNICAL ANALYSIS:",
            primary.reasoning_framework,
            "",
            "KEY CONSIDERATIONS:",
        ]
        answer_parts.extend(f"  {i+1}. {factor}" for i, factor in enumerate(primary.key_factors))
        answer_parts.extend([
            "",
            "INDUSTRY STANDARDS AND REFERENCES:",
        ])
        answer_parts.extend(f"  • {auth}" for auth in primary.primary_authority)
        answer_parts.extend([
            "",
            "RISK ASSESSMENT:",
            f"Confidence Level: {primary.confidence.value}",
            f"Assessment: {primary.confidence_stratification}",
            "",
            "ALTERNATIVE APPROACHES CONSIDERED:",
        ])
        answer_parts.extend(f"  • {arg}" for arg in primary.counter_arguments[:3])
        answer_parts.extend([
            "",
            "RECOMMENDED IMPLEMENTATION:",
            primary.resolution_strategy,
            "",
            f"Controlling Standards: {primary.controlling_precedent}"
        ])

        return "\n".join(answer_parts)


def extract_recommendations(doctrines: List[DoctrineBlock]) -> List[str]:
    """Extract actionable recommendations from doctrines"""
    recommendations = []
    for doctrine in doctrines[:2]:  # Top 2 doctrines
        # Extract action items from resolution strategy
        strategy = doctrine.resolution_strategy
        if "Use" in strategy:
            recommendations.append(strategy.split(".")[0])
        if "Configure" in strategy or "Set" in strategy:
            recommendations.append(strategy.split(".")[1] if "." in strategy else strategy[:100])

    return recommendations[:5]  # Max 5 recommendations


# ============================================================================
# API ENDPOINTS
# ============================================================================

@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Main query endpoint - TIE Gold Standard SCADA expertise
    """
    try:
        logger.info(f"Query received: {request.query[:100]} | Mode: {request.mode} | Zone: {request.zone}")

        response = three_layer_response(request.query, request.mode, request.zone)

        logger.info(f"Query processed: {len(response.doctrines_triggered)} doctrines | {response.processing_time_ms}ms")

        return response

    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        TELEMETRY.record_query(0, [], str(e))
        raise HTTPException(status_code=500, detail=f"Engine error: {str(e)}")


@APP.get("/health", response_model=HealthResponse)
async def health_check():
    """
    TIE-20 Component: Health endpoint
    """
    uptime = (datetime.now() - TELEMETRY.start_time).total_seconds()

    return HealthResponse(
        status="operational",
        version="1.0.0",
        port=9006,
        doctrines_loaded=len(DOCTRINE_CACHE),
        categories=[cat.value for cat in IssueCategory],
        uptime_seconds=round(uptime, 2)
    )


@APP.get("/telemetry")
async def get_telemetry():
    """
    TIE-20 Component: Telemetry endpoint
    """
    return TELEMETRY.get_stats()


@APP.get("/doctrines")
async def list_doctrines():
    """
    List all available doctrine blocks
    """
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "entity_scope": d.entity_scope
            }
            for d in DOCTRINE_CACHE
        ]
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("OFE06 SCADA Monitoring & Control Engine")
    logger.info("TIE Gold Standard - Oilfield Equipment Intelligence")
    logger.info(f"Doctrines loaded: {len(DOCTRINE_CACHE)}")
    logger.info(f"Categories: {len(IssueCategory)}")
    logger.info("=" * 80)

    uvicorn.run(APP, host="0.0.0.0", port=9006, log_level="info")
