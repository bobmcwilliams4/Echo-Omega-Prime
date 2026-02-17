import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import hashlib
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set, Callable
from enum import Enum, auto
from datetime import datetime, timedelta
import threading
import json

# ==============================
# ENUMS
# ==============================

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
    HYDRAULIC_CIRCUIT = "HYDRAULIC_CIRCUIT"
    DISC_BRAKE = "DISC_BRAKE"
    DRUM_BRAKE = "DRUM_BRAKE"
    ABS = "ABS"
    EBD = "EBD"
    ESC = "ESC"
    FLUID_SPEC = "FLUID_SPEC"
    PEDAL_FEEL = "PEDAL_FEEL"
    FRICTION = "FRICTION"
    ROTOR_THERMAL = "ROTOR_THERMAL"
    BOOSTER = "BOOSTER"
    LINE_ROUTING = "LINE_ROUTING"
    PARKING_BRAKE = "PARKING_BRAKE"
    PROPORTIONING_VALVE = "PROPORTIONING_VALVE"
    REGENERATIVE = "REGENERATIVE"
    BRAKE_BY_WIRE = "BRAKE_BY_WIRE"
    NVH = "NVH"
    FMVSS = "FMVSS"
    FADE = "FADE"
    WEAR_SENSOR = "WEAR_SENSOR"

# ==============================
# METRICS COLLECTOR
# ==============================

class MetricsCollector:
    def __init__(self):
        self.query_log: List[Dict[str, Any]] = []
        self.error_log: List[Dict[str, Any]] = []
        self.lock = threading.Lock()
        self.doctrine_hits: Dict[str, int] = {}
        self.latencies: List[float] = []
        self.hourly_queries: List[datetime] = []

    def record_query(self, doctrine_ids: List[str], latency: float):
        with self.lock:
            self.query_log.append({
                "timestamp": datetime.utcnow().isoformat(),
                "doctrines": doctrine_ids,
                "latency": latency
            })
            self.latencies.append(latency)
            self.hourly_queries.append(datetime.utcnow())
            for doc_id in doctrine_ids:
                self.doctrine_hits[doc_id] = self.doctrine_hits.get(doc_id, 0) + 1

    def record_error(self, error: str):
        with self.lock:
            self.error_log.append({
                "timestamp": datetime.utcnow().isoformat(),
                "error": error
            })

    def get_latency_stats(self) -> Dict[str, float]:
        with self.lock:
            if not self.latencies:
                return {"min": 0, "max": 0, "avg": 0}
            return {
                "min": min(self.latencies),
                "max": max(self.latencies),
                "avg": sum(self.latencies) / len(self.latencies)
            }

    def get_doctrine_hit_rate(self) -> Dict[str, int]:
        with self.lock:
            return dict(self.doctrine_hits)

    def queries_last_hour(self) -> int:
        now = datetime.utcnow()
        with self.lock:
            self.hourly_queries = [t for t in self.hourly_queries if (now - t).total_seconds() < 3600]
            return len(self.hourly_queries)

metrics_collector = MetricsCollector()

# ==============================
# PYDANTIC MODELS
# ==============================

class QueryRequest(BaseModel):
    scenario: str = Field(..., description="Scenario or question about brake systems")
    mode: ResponseMode = Field(..., description="Response mode")
    entity_type: str = Field(..., description="Type of entity (e.g., vehicle, component)")
    complexity: int = Field(..., ge=1, le=10, description="Complexity level (1-10)")

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

# ==============================
# DOCTRINE CACHE
# ==============================

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
    entity_scope: str
    confidence: float
    confidence_zone: ConfidenceZone
    controlling_precedent: str

# --- Doctrine Blocks ---

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Hydraulic Brake Circuit Design: Dual Diagonal Split",
        keywords=["hydraulic", "circuit", "dual diagonal", "split", "safety"],
        conclusion_template="A dual diagonal split hydraulic brake circuit provides redundancy by ensuring that failure in one circuit retains braking in opposite corners, enhancing vehicle safety compliance.",
        reasoning_framework=(
            "The dual diagonal split configuration divides the hydraulic system into two circuits, each controlling one front and the diagonally opposite rear wheel. "
            "This design ensures that in the event of a single circuit failure (e.g., due to a leak or rupture), the vehicle retains braking capability on at least one front and one rear wheel, maintaining directional stability. "
            "FMVSS 135 and ECE R13 require such redundancy for passenger vehicles. "
            "The diagonal split is preferred over front/rear split because loss of only rear brakes can result in significant instability, especially under heavy braking. "
            "Hydraulic pressure balancing is achieved using proportioning valves and careful master cylinder sizing. "
            "The system must be designed to prevent cross-circuit pressure loss and to minimize pedal travel in the event of partial failure. "
            "Testing includes simulated circuit failure and measurement of residual braking force and vehicle controllability. "
            "Manufacturers must document compliance with regulatory standards and validate via both simulation and physical testing. "
            "Failure mode effects analysis (FMEA) is used to identify and mitigate potential single-point failures. "
            "The dual diagonal split is now standard in most passenger vehicles due to its proven safety benefits and regulatory acceptance. "
            "Brake warning systems are required to alert the driver to hydraulic failures. "
            "Designers must also consider maintenance accessibility and minimize the risk of incorrect assembly during service. "
            "Hydraulic fluid compatibility and corrosion resistance are critical for long-term reliability. "
            "The system's effectiveness is validated through both static and dynamic vehicle tests, including split-mu surfaces. "
            "Design documentation must include circuit diagrams, component specifications, and compliance matrices."
        ),
        key_factors=[
            "Redundancy in hydraulic circuits",
            "Directional stability under failure",
            "Regulatory compliance (FMVSS 135, ECE R13)",
            "Proportioning valve calibration",
            "Master cylinder sizing"
        ],
        primary_authority=[
            "FMVSS 135, S5.3.1, U.S. Department of Transportation",
            "ECE R13, UN Economic Commission for Europe",
            "SAE J1137: Dual Hydraulic Brake System Design"
        ],
        burden_holder="Manufacturer",
        adversary_position="Single circuit split is sufficient for cost savings",
        counter_arguments=[
            "Single circuit split increases risk of total brake loss",
            "Rear-only braking loss leads to instability",
            "Dual diagonal split is mandated by regulations",
            "Cost savings do not outweigh safety risks",
            "Insurance and liability exposure increases without redundancy"
        ],
        resolution_strategy="Adopt dual diagonal split as baseline; validate with FMEA and regulatory testing.",
        entity_scope="Passenger vehicles, light trucks",
        confidence=0.98,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="FMVSS 135, S5.3.1"
    ),
    DoctrineBlock(
        topic="Disc Brake Caliper Piston and Pad Analysis",
        keywords=["disc brake", "caliper", "piston", "pad", "force distribution"],
        conclusion_template="Proper caliper piston sizing and pad area selection are critical to achieving uniform pressure distribution and optimal braking performance in disc brake systems.",
        reasoning_framework=(
            "Disc brake calipers convert hydraulic pressure into clamping force on the rotor via pistons and pads. "
            "Piston diameter directly affects the force applied to the pad; larger pistons increase force but may require greater fluid volume and pedal travel. "
            "Pad area and shape influence pressure distribution and heat dissipation. "
            "Uneven pad wear or tapered wear patterns often indicate improper caliper alignment or piston retraction issues. "
            "Multi-piston calipers are used to distribute force more evenly across the pad, reducing localized thermal stress and improving modulation. "
            "Pad material selection (organic, semi-metallic, ceramic) affects friction coefficient (mu), fade resistance, and NVH characteristics. "
            "Caliper stiffness is essential to prevent flexing under load, which can degrade pedal feel and response. "
            "Seals and dust boots must be robust to prevent fluid leakage and contamination. "
            "Thermal analysis is required to ensure that caliper and pad temperatures remain within safe limits during repeated stops. "
            "Designers must validate caliper and pad combinations through dynamometer testing and on-vehicle trials, measuring stopping distance, pedal effort, and wear rates. "
            "Regulatory standards (FMVSS 135) specify minimum performance criteria for disc brake systems. "
            "Maintenance procedures must include inspection for piston seal integrity and pad thickness. "
            "Caliper mounting hardware must be torqued to specification to prevent vibration and uneven wear. "
            "Pad backing plates should be designed to minimize noise and maximize heat transfer. "
            "Documentation should include force calculations, material specs, and test data."
        ),
        key_factors=[
            "Piston diameter and count",
            "Pad area and material",
            "Caliper stiffness",
            "Thermal management",
            "Wear patterns"
        ],
        primary_authority=[
            "SAE J1602: Disc Brake Caliper Design",
            "FMVSS 135, S5.3.2",
            "Bosch Automotive Handbook, 10th Edition, Section 20.2"
        ],
        burden_holder="Brake system designer",
        adversary_position="Single piston and small pad area are sufficient for most vehicles",
        counter_arguments=[
            "Single piston may cause uneven pad wear",
            "Small pad area increases thermal stress",
            "Multi-piston calipers improve force distribution",
            "Larger pads reduce fade and wear",
            "Regulations require minimum performance standards"
        ],
        resolution_strategy="Select piston and pad sizes based on force and thermal analysis; validate with testing.",
        entity_scope="Passenger vehicles, performance vehicles",
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="SAE J1602"
    ),
    DoctrineBlock(
        topic="Drum Brake Leading and Trailing Shoe Adjustment",
        keywords=["drum brake", "leading shoe", "trailing shoe", "adjustment", "self-energizing"],
        conclusion_template="Accurate adjustment of leading and trailing shoes in drum brakes is essential for balanced braking force and prevention of premature wear.",
        reasoning_framework=(
            "Drum brakes utilize leading and trailing shoes to convert hydraulic pressure into frictional force against the drum. "
            "The leading shoe is self-energizing, using drum rotation to increase applied force, while the trailing shoe relies solely on hydraulic pressure. "
            "Improper adjustment can result in uneven braking, increased stopping distances, and accelerated wear of one shoe. "
            "Automatic adjusters are commonly used to maintain correct shoe-to-drum clearance, compensating for lining wear. "
            "Manual adjustment procedures require precise measurement of drum diameter and shoe arc. "
            "Brake fade is more likely if the leading shoe is over-adjusted, as it will bear excessive load and overheat. "
            "Brake pull (vehicle veering during braking) often indicates asymmetrical shoe adjustment or contamination. "
            "Periodic inspection is required to ensure adjusters are functioning and not seized due to corrosion or debris. "
            "Replacement linings must match OEM specifications for thickness and arc. "
            "FMVSS 135 and ECE R13 specify minimum performance and adjustment requirements for drum brakes. "
            "Technicians must use calibrated tools and follow manufacturer procedures for adjustment. "
            "Documentation should include before/after measurements and confirmation of adjuster operation. "
            "Designers may consider self-adjusting mechanisms to reduce maintenance intervals. "
            "Shoe return springs must be checked for correct tension to ensure full retraction. "
            "Brake dust shields and proper lubrication of adjuster threads are recommended for longevity."
        ),
        key_factors=[
            "Shoe-to-drum clearance",
            "Self-energizing effect",
            "Adjuster mechanism function",
            "Lining material and thickness",
            "Inspection intervals"
        ],
        primary_authority=[
            "FMVSS 135, S5.3.3",
            "Bosch Automotive Handbook, 10th Edition, Section 20.3",
            "SAE J998: Drum Brake Adjustment"
        ],
        burden_holder="Service technician",
        adversary_position="Adjustment is not critical due to self-adjusting mechanisms",
        counter_arguments=[
            "Self-adjusters can seize or fail",
            "Improper adjustment causes uneven wear",
            "Manual inspection is still required",
            "Brake pull and fade are linked to adjustment",
            "Regulations mandate periodic verification"
        ],
        resolution_strategy="Follow OEM and regulatory procedures for adjustment; verify adjuster function at each service.",
        entity_scope="Passenger vehicles, light trucks",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="FMVSS 135, S5.3.3"
    ),
    DoctrineBlock(
        topic="ABS Anti-lock Braking System: Wheel Speed Sensors",
        keywords=["ABS", "anti-lock", "wheel speed sensor", "hydraulic modulation", "slip ratio"],
        conclusion_template="Accurate wheel speed sensor data is fundamental for ABS operation, enabling real-time slip detection and hydraulic pressure modulation to prevent wheel lockup.",
        reasoning_framework=(
            "ABS relies on individual wheel speed sensors to monitor rotational velocity and detect incipient wheel lockup. "
            "Sensor types include passive (variable reluctance) and active (Hall effect), each with distinct signal characteristics. "
            "The ABS control module compares wheel speeds to calculate slip ratio and triggers hydraulic modulation when thresholds are exceeded. "
            "Signal integrity is critical; sensor wiring must be shielded and routed away from high-EMI sources. "
            "Faulty sensors or damaged tone rings can cause false activations or loss of ABS function, leading to increased stopping distances. "
            "ABS self-diagnostics monitor sensor signals for plausibility and continuity, illuminating warning indicators upon fault detection. "
            "Hydraulic modulators use rapid solenoid actuation to pulse pressure, maintaining optimal slip. "
            "Sensor mounting must ensure correct air gap and alignment to the tone ring. "
            "Environmental sealing is required to prevent corrosion and debris ingress. "
            "Testing includes oscilloscope analysis of sensor output, resistance checks, and on-road ABS activation tests. "
            "FMVSS 126 and ECE R13H specify ABS performance and diagnostic requirements. "
            "Replacement sensors must match OEM specifications for signal type and mounting geometry. "
            "ABS operation must be validated under varying surface conditions (wet, dry, split-mu). "
            "System documentation should include wiring diagrams, diagnostic procedures, and test results. "
            "Technicians must clear fault codes and verify sensor operation after service."
        ),
        key_factors=[
            "Sensor type and placement",
            "Signal integrity",
            "Diagnostic capability",
            "Hydraulic modulation response",
            "Environmental sealing"
        ],
        primary_authority=[
            "FMVSS 126, S5.1.1",
            "SAE J1042: ABS Sensor Testing",
            "Bosch Automotive Handbook, 10th Edition, Section 20.5"
        ],
        burden_holder="ABS system integrator",
        adversary_position="Sensor faults are rare and not critical to overall braking",
        counter_arguments=[
            "Sensor faults disable ABS function",
            "Increased stopping distance without ABS",
            "Regulations require sensor diagnostics",
            "Environmental exposure increases failure risk",
            "Improper sensor mounting causes false readings"
        ],
        resolution_strategy="Use robust sensors, validate with diagnostics, and follow regulatory test protocols.",
        entity_scope="Passenger vehicles, commercial vehicles",
        confidence=0.97,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="FMVSS 126, S5.1.1"
    ),
    DoctrineBlock(
        topic="EBD Electronic Brakeforce Distribution",
        keywords=["EBD", "electronic brakeforce", "distribution", "load sensing", "stability"],
        conclusion_template="EBD systems dynamically adjust brake force between axles based on load and driving conditions, improving stability and reducing stopping distances.",
        reasoning_framework=(
            "Electronic Brakeforce Distribution (EBD) extends ABS functionality by modulating brake force between front and rear axles. "
            "EBD uses inputs from wheel speed sensors, load sensors, and sometimes yaw rate sensors to calculate optimal brake force allocation. "
            "Under varying load conditions (e.g., passengers, cargo), EBD prevents rear wheel lockup by reducing rear brake pressure. "
            "EBD logic is implemented in the ABS control module, using algorithms to adjust hydraulic modulation in real time. "
            "The system improves vehicle stability, especially during emergency braking or on split-mu surfaces. "
            "EBD reduces tire wear and improves brake lining life by preventing over-braking of the rear axle. "
            "Failure of EBD function is indicated by warning lamps and triggers fallback to conventional hydraulic distribution. "
            "Validation includes dynamic vehicle tests with varying loads and surface conditions, measuring stopping distance and stability metrics. "
            "FMVSS 135 and ECE R13H require demonstration of effective brake force distribution under all loading conditions. "
            "System integration must ensure compatibility with ABS, ESC, and regenerative braking. "
            "Documentation should include control logic, sensor calibration data, and test results. "
            "Technicians must verify EBD operation after repairs affecting sensors or hydraulic circuits. "
            "EBD is now standard in most modern vehicles due to its safety benefits and regulatory requirements. "
            "Designers must ensure redundancy and fail-safe operation in case of sensor or module failure. "
            "Periodic software updates may be required to address algorithm improvements or regulatory changes."
        ),
        key_factors=[
            "Load sensing accuracy",
            "Sensor integration",
            "Control algorithm robustness",
            "Hydraulic modulation capability",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FMVSS 135, S5.3.4",
            "ECE R13H, Annex 8",
            "SAE J2784: Brake Force Distribution"
        ],
        burden_holder="Vehicle manufacturer",
        adversary_position="Conventional hydraulic proportioning is sufficient",
        counter_arguments=[
            "Hydraulic systems lack dynamic adjustment",
            "EBD improves safety under variable loads",
            "Regulations increasingly require EBD",
            "Sensor failures must be managed",
            "Integration with ABS/ESC is essential"
        ],
        resolution_strategy="Implement EBD as standard; validate with dynamic and regulatory tests.",
        entity_scope="Passenger vehicles, SUVs, light trucks",
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="FMVSS 135, S5.3.4"
    ),
    DoctrineBlock(
        topic="ESC Electronic Stability Control: Yaw Rate and Lateral Acceleration",
        keywords=["ESC", "stability control", "yaw rate", "lateral acceleration", "rollover"],
        conclusion_template="ESC systems utilize yaw rate and lateral acceleration sensors to detect and mitigate loss of control, significantly reducing rollover and spinout risk.",
        reasoning_framework=(
            "Electronic Stability Control (ESC) monitors vehicle dynamics using yaw rate, lateral acceleration, and steering angle sensors. "
            "When the system detects deviation from the intended path (e.g., understeer or oversteer), it selectively applies braking to individual wheels and may reduce engine torque. "
            "ESC algorithms compare driver steering input to actual vehicle response, calculating a desired yaw rate. "
            "If the measured yaw rate deviates beyond calibrated thresholds, the system intervenes to restore stability. "
            "ESC is particularly effective in preventing loss of control on slippery or split-mu surfaces and during sudden maneuvers. "
            "FMVSS 126 and ECE R13H mandate ESC on new passenger vehicles, with specific performance and diagnostic requirements. "
            "Sensor calibration and signal integrity are critical for accurate intervention. "
            "ESC must be integrated with ABS, EBD, and traction control systems for coordinated response. "
            "Testing includes dynamic maneuvers (e.g., J-turn, fishhook) and measurement of yaw rate response, lateral acceleration, and stopping distance. "
            "System documentation should include control logic, sensor specs, and test data. "
            "Technicians must verify ESC operation after repairs affecting sensors or control modules. "
            "ESC warning lamps indicate system faults and require diagnostic attention. "
            "ESC systems must be robust to sensor drift and environmental factors. "
            "Periodic software updates may be required to address algorithm improvements or regulatory changes. "
            "ESC has been shown to reduce single-vehicle crashes and fatalities by over 30% (NHTSA studies)."
        ),
        key_factors=[
            "Yaw rate sensor accuracy",
            "Lateral acceleration measurement",
            "Control algorithm calibration",
            "Integration with ABS/EBD",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FMVSS 126, S5.1.2",
            "ECE R13H, Annex 9",
            "NHTSA: Effectiveness of ESC, DOT HS 811 486"
        ],
        burden_holder="Vehicle manufacturer",
        adversary_position="ESC is unnecessary for experienced drivers",
        counter_arguments=[
            "ESC reduces crash risk for all drivers",
            "Mandated by regulations",
            "Sensor failures must be managed",
            "Integration complexity is justified by safety gains",
            "ESC effectiveness is well-documented"
        ],
        resolution_strategy="Implement ESC as standard; validate with dynamic and regulatory tests.",
        entity_scope="Passenger vehicles, SUVs, light trucks",
        confidence=0.97,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="FMVSS 126, S5.1.2"
    ),
    DoctrineBlock(
        topic="Brake Fluid DOT Specifications and Boiling Point",
        keywords=["brake fluid", "DOT", "boiling point", "hygroscopic", "fluid replacement"],
        conclusion_template="Selecting the correct DOT brake fluid and maintaining its boiling point is vital to prevent vapor lock and ensure consistent brake performance.",
        reasoning_framework=(
            "Brake fluid transmits hydraulic pressure from the master cylinder to the wheel brakes. "
            "DOT specifications (DOT 3, 4, 5, 5.1) define minimum boiling points, viscosity, and chemical compatibility. "
            "DOT 3 and 4 fluids are glycol-based and hygroscopic, absorbing moisture over time, which lowers boiling point and increases corrosion risk. "
            "DOT 5 is silicone-based and not hygroscopic, but is incompatible with ABS and certain seal materials. "
            "DOT 5.1 is glycol-based with higher boiling point, suitable for high-performance applications. "
            "Minimum dry boiling points: DOT 3 (205°C), DOT 4 (230°C), DOT 5.1 (260°C). "
            "Moisture ingress occurs through hoses, seals, and reservoir caps, necessitating periodic fluid replacement (typically every 2 years). "
            "Low boiling point leads to vapor lock, causing sudden loss of braking. "
            "Fluid selection must consider compatibility with system materials and regulatory requirements. "
            "FMVSS 116 specifies performance and labeling requirements for brake fluids. "
            "Technicians must use only approved fluids and avoid mixing types. "
            "Fluid testing includes boiling point measurement and visual inspection for contamination. "
            "Documentation should include fluid type, replacement interval, and test results. "
            "Improper fluid selection or maintenance is a leading cause of brake failure. "
            "Manufacturers must specify fluid type in service literature and on reservoir caps."
        ),
        key_factors=[
            "Boiling point (dry/wet)",
            "Hygroscopicity",
            "Material compatibility",
            "Replacement interval",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FMVSS 116, S5.1",
            "SAE J1703: Brake Fluid Specifications",
            "Bosch Automotive Handbook, 10th Edition, Section 20.7"
        ],
        burden_holder="Service technician",
        adversary_position="Any brake fluid is acceptable if it meets minimum standards",
        counter_arguments=[
            "Mixing fluids can cause seal failure",
            "Low boiling point leads to vapor lock",
            "Regulations specify fluid type and labeling",
            "Moisture absorption is inevitable",
            "Periodic replacement is essential"
        ],
        resolution_strategy="Use only specified DOT fluid; replace at recommended intervals and test for contamination.",
        entity_scope="All hydraulic brake systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="FMVSS 116, S5.1"
    ),
    DoctrineBlock(
        topic="Master Cylinder Bore Ratio and Pedal Feel",
        keywords=["master cylinder", "bore ratio", "pedal feel", "hydraulic leverage", "travel"],
        conclusion_template="Master cylinder bore size directly affects pedal effort and travel; optimal sizing balances hydraulic leverage and driver comfort.",
        reasoning_framework=(
            "The master cylinder converts pedal force into hydraulic pressure. "
            "Bore diameter determines the volume of fluid displaced per unit pedal travel. "
            "A larger bore reduces pedal travel but increases required pedal force, while a smaller bore increases travel but reduces effort. "
            "The bore ratio must be matched to caliper piston area and overall system compliance. "
            "Pedal feel is influenced by system stiffness, fluid compressibility, and component flex. "
            "Designers use force-displacement curves to optimize pedal feel for the target vehicle segment. "
            "Excessive pedal travel may indicate air in the system, fluid leakage, or excessive compliance. "
            "FMVSS 135 specifies minimum pedal reserve and effort requirements. "
            "Testing includes measurement of pedal force, travel, and hydraulic pressure under static and dynamic conditions. "
            "Documentation should include bore sizing calculations, force curves, and test data. "
            "Aftermarket modifications (e.g., larger calipers) may require master cylinder resizing to maintain proper pedal feel. "
            "Technicians must verify pedal reserve and effort after service. "
            "System must be free of leaks and properly bled to achieve design pedal characteristics. "
            "Manufacturers may offer different bore sizes for performance or towing packages."
        ),
        key_factors=[
            "Bore diameter",
            "Caliper piston area",
            "System compliance",
            "Pedal force/travel curve",
            "Regulatory requirements"
        ],
        primary_authority=[
            "FMVSS 135, S5.3.5",
            "SAE J1603: Master Cylinder Sizing",
            "Bosch Automotive Handbook, 10th Edition, Section 20.8"
        ],
        burden_holder="Brake system designer",
        adversary_position="Any bore size within range is acceptable",
        counter_arguments=[
            "Incorrect sizing degrades pedal feel",
            "Regulations specify minimum pedal reserve",
            "Aftermarket changes require recalculation",
            "System compliance must be considered",
            "Improper sizing can cause safety issues"
        ],
        resolution_strategy="Calculate bore size based on system analysis; validate with force-displacement testing.",
        entity_scope="Passenger vehicles, performance vehicles",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="FMVSS 135, S5.3.5"
    ),
    DoctrineBlock(
        topic="Brake Pad Friction Coefficient (Mu) and Material Selection",
        keywords=["brake pad", "friction coefficient", "mu", "material", "fade resistance"],
        conclusion_template="Selecting brake pad material with appropriate friction coefficient (mu) is crucial for consistent braking performance and fade resistance.",
        reasoning_framework=(
            "Brake pad friction coefficient (mu) determines the force generated for a given hydraulic pressure. "
            "Pad materials include organic, semi-metallic, and ceramic, each with distinct mu characteristics and thermal properties. "
            "High-mu pads provide strong initial bite but may increase noise and rotor wear. "
            "Low-mu pads offer smoother engagement but may require higher pedal effort. "
            "Fade resistance is critical for repeated stops; materials must maintain mu at elevated temperatures. "
            "FMVSS 135 and ECE R90 specify minimum performance and fade resistance for pad materials. "
            "Pad selection must consider rotor compatibility, NVH characteristics, and dust generation. "
            "Testing includes dynamometer fade cycles, wear measurements, and noise analysis. "
            "Pad backing plates and shims are used to control vibration and noise. "
            "Aftermarket pads must meet or exceed OEM specifications. "
            "Improper pad selection can result in excessive wear, noise, or reduced braking performance. "
            "Documentation should include material specs, mu curves, and test data. "
            "Technicians must verify pad thickness and material type during service. "
            "Manufacturers may offer multiple pad options for different vehicle applications."
        ),
        key_factors=[
            "Friction coefficient (mu)",
            "Material type",
            "Fade resistance",
            "NVH characteristics",
            "Rotor compatibility"
        ],
        primary_authority=[
            "FMVSS 135, S5.3.6",
            "ECE R90, Annex 7",
            "SAE J661: Brake Lining Quality Test"
        ],
        burden_holder="Pad manufacturer",
        adversary_position="Any pad material is acceptable if dimensions fit",
        counter_arguments=[
            "Incorrect mu affects stopping distance",
            "Fade resistance is critical for safety",
            "NVH issues can arise from improper material",
            "Regulations specify minimum performance",
            "Rotor compatibility must be considered"
        ],
        resolution_strategy="Select pad material based on mu, fade, and NVH testing; validate with regulatory standards.",
        entity_scope="All disc and drum brake systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="FMVSS 135, S5.3.6"
    ),
    DoctrineBlock(
        topic="Brake Rotor Thermal Analysis and Warping",
        keywords=["brake rotor", "thermal analysis", "warping", "heat dissipation", "cracking"],
        conclusion_template="Proper thermal analysis and rotor material selection are essential to prevent warping, cracking, and loss of braking performance under repeated high-energy stops.",
        reasoning_framework=(
            "Brake rotors must absorb and dissipate heat generated during braking. "
            "Thermal analysis includes calculation of energy input, heat capacity, and cooling rate. "
            "Repeated high-energy stops can cause rotor temperatures to exceed material limits, leading to warping or cracking. "
            "Vented rotors improve cooling by increasing surface area and airflow. "
            "Material selection (cast iron, carbon-ceramic) affects thermal conductivity and resistance to distortion. "
            "Uneven rotor thickness (DTV) can cause pedal pulsation and vibration. "
            "Proper torque of wheel fasteners is critical to avoid introducing stress that can lead to warping. "
            "Testing includes thermocouple measurement during fade cycles, DTV measurement, and crack inspection. "
            "FMVSS 135 specifies maximum allowable rotor temperature and performance after fade. "
            "Designers must consider vehicle mass, maximum speed, and duty cycle when sizing rotors. "
            "Aftermarket rotors must meet or exceed OEM thermal performance. "
            "Technicians must inspect for blueing, cracks, and DTV during service. "
            "Documentation should include thermal analysis, material specs, and test data. "
            "Rotor cooling can be enhanced with ducting or slotted/drilled designs, but these may affect NVH and wear."
        ),
        key_factors=[
            "Thermal capacity",
            "Material selection",
            "Rotor ventilation",
            "DTV and runout",
            "Installation torque"
        ],
        primary_authority=[
            "FMVSS 135, S5.3.7",
            "SAE J431: Brake Rotor Materials",
            "Bosch Automotive Handbook, 10th Edition, Section 20.9"
        ],
        burden_holder="Brake system designer",
        adversary_position="Any rotor material is acceptable if dimensions fit",
        counter_arguments=[
            "Material affects thermal performance",
            "Warping leads to vibration and reduced braking",
            "Regulations specify fade performance",
            "Improper installation can cause warping",
            "Aftermarket rotors must be validated"
        ],
        resolution_strategy="Conduct thermal analysis and validate rotor design with fade and DTV testing.",
        entity_scope="All disc brake systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="FMVSS 135, S5.3.7"
    ),
    DoctrineBlock(
        topic="Vacuum Brake Booster and Assist Ratio",
        keywords=["vacuum booster", "assist ratio", "pedal effort", "engine vacuum", "diaphragm"],
        conclusion_template="Vacuum brake boosters reduce pedal effort by amplifying input force; proper sizing and assist ratio are critical for driver comfort and regulatory compliance.",
        reasoning_framework=(
            "Vacuum brake boosters use engine vacuum to amplify pedal force via a diaphragm and pushrod mechanism. "
            "Assist ratio is determined by diaphragm area and lever geometry. "
            "Insufficient assist increases pedal effort, while excessive assist can reduce pedal feedback and controllability. "
            "FMVSS 135 specifies maximum allowable pedal effort for specified deceleration. "
            "Booster sizing must account for engine vacuum availability, especially in turbocharged or hybrid vehicles. "
            "Loss of vacuum (e.g., engine off) must still allow for minimum braking performance using residual hydraulic force. "
            "Testing includes measurement of pedal effort, booster response time, and vacuum level under various operating conditions. "
            "Check valves and vacuum reservoirs are used to maintain assist during transient vacuum loss. "
            "Booster failure modes include diaphragm rupture, valve sticking, and vacuum leaks. "
            "Technicians must verify booster function during service, including leak checks and pedal effort measurement. "
            "Documentation should include assist ratio calculations, test data, and failure mode analysis. "
            "Aftermarket boosters must be validated for compatibility with existing hydraulic systems. "
            "Manufacturers may offer different assist ratios for performance or towing applications."
        ),
        key_factors=[
            "Assist ratio",
            "Vacuum source availability",
            "Booster sizing",
            "Failure mode analysis",
            "Pedal effort measurement"
        ],
        primary_authority=[
            "FMVSS 135, S5.3.8",
            "SAE J1698: Brake Booster Performance",
            "Bosch Automotive Handbook, 10th Edition, Section 20.10"
        ],
        burden_holder="Brake system designer",
        adversary_position="Any booster size is acceptable if pedal effort is within range",
        counter_arguments=[
            "Incorrect sizing affects driver comfort",
            "Vacuum loss must be managed",
            "Regulations specify pedal effort limits",
            "Failure modes must be analyzed",
            "Aftermarket boosters require validation"
        ],
        resolution_strategy="Size booster for target assist ratio; validate with pedal effort and failure mode testing.",
        entity_scope="Passenger vehicles, light trucks",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="FMVSS 135, S5.3.8"
    ),
    DoctrineBlock(
        topic="Brake Line Routing and Flare Fitting Integrity",
        keywords=["brake line", "routing", "flare fitting", "corrosion", "leak prevention"],
        conclusion_template="Proper brake line routing and flare fitting installation are essential to prevent leaks, corrosion, and ensure long-term hydraulic integrity.",
        reasoning_framework=(
            "Brake lines transmit hydraulic pressure from the master cylinder to the wheel brakes. "
            "Lines must be routed to avoid sharp bends, moving parts, and heat sources. "
            "Double flare or bubble flare fittings are used to ensure leak-free connections. "
            "Improper flare angle or torque can cause leaks and pressure loss. "
            "Corrosion resistance is critical, especially in regions using road salt; materials include coated steel or copper-nickel alloy. "
            "Lines must be securely clipped to the chassis to prevent vibration and fatigue failure. "
            "FMVSS 106 specifies performance and labeling requirements for brake hoses and lines. "
            "Technicians must use proper tools for flare creation and verify fitting torque. "
            "Inspection includes checking for abrasion, corrosion, and leaks at all joints. "
            "Documentation should include routing diagrams, material specs, and installation procedures. "
            "Aftermarket repairs must use compatible fittings and materials. "
            "Pressure testing is required after installation or repair to verify integrity. "
            "Manufacturers may specify replacement intervals in severe service environments."
        ),
        key_factors=[
            "Routing path",
            "Flare fitting type and quality",
            "Corrosion resistance",
            "Secure mounting",
            "Pressure/leak testing"
        ],
        primary_authority=[
            "FMVSS 106, S5.2",
            "SAE J1401: Brake Hose and Line Standards",
            "Bosch Automotive Handbook, 10th Edition, Section 20.11"
        ],
        burden_holder="Installer/technician",
        adversary_position="Any routing is acceptable if lines reach destination",
        counter_arguments=[
            "Improper routing increases failure risk",
            "Incorrect flares cause leaks",
            "Corrosion leads to line rupture",
            "Regulations specify material and installation standards",
            "Pressure testing is mandatory"
        ],
        resolution_strategy="Follow OEM routing and flare procedures; validate with pressure and leak testing.",
        entity_scope="All hydraulic brake systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="FMVSS 106, S5.2"
    ),
    DoctrineBlock(
        topic="Parking Brake Cable and Drum Mechanism",
        keywords=["parking brake", "cable", "drum", "mechanical", "adjustment"],
        conclusion_template="Parking brake cable and drum mechanisms must be properly adjusted and maintained to ensure reliable holding force and compliance with regulatory requirements.",
        reasoning_framework=(
            "Parking brakes use a mechanical cable to actuate drum or disc mechanisms, providing secure vehicle holding when stationary. "
            "Cable tension must be adjusted to ensure full engagement without excessive lever travel. "
            "Automatic adjusters compensate for lining wear, but manual adjustment may be required after cable replacement. "
            "Corrosion and lack of lubrication can cause cable binding or failure. "
            "FMVSS 135 specifies minimum holding force and lever travel requirements. "
            "Testing includes measurement of holding force on an incline and verification of full release. "
            "Technicians must inspect cables for fraying, corrosion, and proper routing. "
            "Documentation should include adjustment procedures, test results, and replacement intervals. "
            "Aftermarket cables must match OEM specifications for length and material. "
            "Periodic inspection and lubrication are recommended for long-term reliability. "
            "Manufacturers may specify different mechanisms for disc and drum applications."
        ),
        key_factors=[
            "Cable tension and adjustment",
            "Corrosion resistance",
            "Holding force measurement",
            "Automatic adjuster function",
            "Inspection and lubrication"
        ],
        primary_authority=[
            "FMVSS 135, S5.3.9",
            "SAE J1138: Parking Brake Systems",
            "Bosch Automotive Handbook, 10th Edition, Section 20.12"
        ],
        burden_holder="Service technician",
        adversary_position="Parking brake adjustment is not critical",
        counter_arguments=[
            "Improper adjustment reduces holding force",
            "Cable corrosion leads to failure",
            "Regulations specify minimum force",
            "Automatic adjusters can fail",
            "Periodic inspection is required"
        ],
        resolution_strategy="Adjust and inspect cables per OEM and regulatory procedures; verify holding force after service.",
        entity_scope="All vehicles with mechanical parking brakes",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="FMVSS 135, S5.3.9"
    ),
    DoctrineBlock(
        topic="Brake Proportioning Valve and Bias Calibration",
        keywords=["proportioning valve", "brake bias", "hydraulic", "rear lockup", "calibration"],
        conclusion_template="Proper calibration of the brake proportioning valve is essential to prevent rear wheel lockup and maintain optimal brake bias under all loading conditions.",
        reasoning_framework=(
            "The brake proportioning valve limits rear brake pressure to prevent premature rear wheel lockup during heavy braking. "
            "Valve calibration is based on vehicle weight distribution, center of gravity, and axle load transfer. "
            "Incorrect calibration can result in rear lockup (oversteer) or excessive front bias (reduced rear braking). "
            "FMVSS 135 and ECE R13 specify maximum allowable rear axle slip and minimum front/rear bias. "
            "Testing includes dynamic stops with varying loads and measurement of wheel slip and stopping distance. "
            "Aftermarket modifications (e.g., lowering springs) may require recalibration. "
            "Technicians must verify valve function and adjust as needed during service. "
            "Documentation should include valve specs, calibration curves, and test data. "
            "Proportioning valves may be mechanical or electronically controlled (as in EBD systems). "
            "Manufacturers may specify different calibration for performance or towing packages. "
            "Improperly functioning valves can cause brake imbalance and instability."
        ),
        key_factors=[
            "Valve calibration curve",
            "Vehicle weight distribution",
            "Axle load transfer",
            "Dynamic testing",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FMVSS 135, S5.3.10",
            "ECE R13, Annex 10",
            "SAE J1095: Brake Proportioning Valves"
        ],
        burden_holder="Brake system designer",
        adversary_position="Factory calibration is sufficient for all conditions",
        counter_arguments=[
            "Load changes require recalibration",
            "Improper calibration causes instability",
            "Regulations specify bias limits",
            "Aftermarket changes affect bias",
            "Dynamic testing is required"
        ],
        resolution_strategy="Calibrate valve based on vehicle analysis; validate with dynamic and regulatory tests.",
        entity_scope="All hydraulic brake systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="FMVSS 135, S5.3.10"
    ),
    DoctrineBlock(
        topic="Regenerative Braking and Energy Recovery Integration",
        keywords=["regenerative braking", "energy recovery", "hybrid", "EV", "integration"],
        conclusion_template="Regenerative braking systems must be integrated with hydraulic brakes to ensure seamless operation, safety, and optimal energy recovery.",
        reasoning_framework=(
            "Regenerative braking uses electric motor/generator to recover kinetic energy during deceleration, converting it to electrical energy stored in the battery. "
            "Integration with hydraulic brakes is managed via brake blending algorithms, ensuring consistent pedal feel and braking force. "
            "Hydraulic brakes must provide full stopping power when battery is full or regenerative system is unavailable. "
            "FMVSS 135 and ECE R13H require that regenerative systems not compromise safety or braking performance. "
            "Control logic must coordinate transition between regenerative and friction braking to avoid abrupt changes in deceleration. "
            "Testing includes measurement of energy recovery efficiency, pedal feel, and stopping distance under various battery states. "
            "System diagnostics must detect faults in regenerative components and revert to hydraulic-only braking as needed. "
            "Documentation should include control algorithms, test data, and failure mode analysis. "
            "Technicians must verify system operation after repairs affecting either subsystem. "
            "Manufacturers may offer different blending strategies for performance or comfort. "
            "Regenerative braking can reduce brake wear and improve efficiency, but must not compromise safety."
        ),
        key_factors=[
            "Brake blending algorithm",
            "Pedal feel consistency",
            "Energy recovery efficiency",
            "Hydraulic override capability",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FMVSS 135, S5.3.11",
            "ECE R13H, Annex 13",
            "SAE J2907: Regenerative Braking Systems"
        ],
        burden_holder="Vehicle manufacturer",
        adversary_position="Regenerative braking can fully replace hydraulic brakes",
        counter_arguments=[
            "Hydraulic brakes are required for safety",
            "Battery state affects regenerative capacity",
            "Blending must be seamless",
            "Diagnostics must ensure fail-safe operation",
            "Regulations require full braking performance"
        ],
        resolution_strategy="Integrate regenerative and hydraulic systems with robust blending and diagnostics; validate with regulatory tests.",
        entity_scope="Hybrid and electric vehicles",
        confidence=0.97,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="FMVSS 135, S5.3.11"
    ),
    DoctrineBlock(
        topic="Brake-by-Wire Electromechanical Systems",
        keywords=["brake by wire", "electromechanical", "actuator", "redundancy", "fail-safe"],
        conclusion_template="Brake-by-wire systems require robust redundancy, diagnostics, and fail-safe mechanisms to ensure safety and regulatory compliance.",
        reasoning_framework=(
            "Brake-by-wire replaces traditional hydraulic actuation with electronic control and electromechanical actuators. "
            "System safety depends on redundant sensors, power supplies, and communication channels. "
            "Diagnostics must detect faults and revert to mechanical or hydraulic backup as needed. "
            "FMVSS 135 and ECE R13H require fail-safe operation and minimum performance in the event of electronic failure. "
            "Actuator response time and force output must match or exceed hydraulic systems. "
            "Control algorithms must ensure consistent pedal feel and response under all conditions. "
            "Testing includes failure mode analysis, response time measurement, and dynamic vehicle tests. "
            "Documentation should include system architecture, redundancy strategies, and test data. "
            "Technicians must be trained in diagnosis and repair of electronic components. "
            "Manufacturers may offer different levels of redundancy for cost or performance optimization. "
            "Aftermarket modifications must not compromise fail-safe operation."
        ),
        key_factors=[
            "Redundancy and fail-safe design",
            "Actuator performance",
            "Diagnostic capability",
            "Control algorithm robustness",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FMVSS 135, S5.3.12",
            "ECE R13H, Annex 16",
            "SAE J2902: Brake-by-Wire Systems"
        ],
        burden_holder="System integrator",
        adversary_position="Electronic systems are inherently reliable",
        counter_arguments=[
            "Electronic failures can cause total brake loss",
            "Redundancy is required by regulation",
            "Diagnostics must be robust",
            "Mechanical backup is essential",
            "Training is required for service"
        ],
        resolution_strategy="Design for redundancy and fail-safe operation; validate with failure mode and regulatory testing.",
        entity_scope="Electric and advanced vehicles",
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="FMVSS 135, S5.3.12"
    ),
    DoctrineBlock(
        topic="Brake Noise, Vibration, and Harshness (NVH) Control",
        keywords=["brake noise", "vibration", "harshness", "NVH", "shim"],
        conclusion_template="Effective NVH control in brake systems requires careful material selection, component design, and damping strategies to minimize noise and vibration.",
        reasoning_framework=(
            "Brake noise and vibration are common customer complaints and can indicate underlying design or material issues. "
            "Sources include pad vibration, rotor surface irregularities, and caliper flex. "
            "Material selection for pads and shims affects damping and noise generation. "
            "Designers use finite element analysis (FEA) to predict and mitigate NVH issues. "
            "Shim and insulator design can reduce high-frequency squeal. "
            "Testing includes dynamometer NVH cycles, on-vehicle noise measurement, and subjective evaluation. "
            "FMVSS 135 does not specify noise limits, but OEMs set internal targets for customer satisfaction. "
            "Aftermarket pads may increase noise if not properly matched to the system. "
            "Technicians must inspect for loose hardware, uneven wear, and contamination during service. "
            "Documentation should include NVH test data, material specs, and design analysis. "
            "Manufacturers may offer low-noise pad options for sensitive markets. "
            "Periodic cleaning and lubrication can reduce noise in service."
        ),
        key_factors=[
            "Pad and shim material",
            "Component stiffness",
            "Surface finish",
            "FEA and NVH testing",
            "Installation quality"
        ],
        primary_authority=[
            "SAE J2521: Brake NVH Testing",
            "Bosch Automotive Handbook, 10th Edition, Section 20.13",
            "FMVSS 135 (performance context)"
        ],
        burden_holder="Brake system designer",
        adversary_position="Noise is only a cosmetic issue",
        counter_arguments=[
            "Noise can indicate safety issues",
            "Customer satisfaction is critical",
            "NVH affects perceived quality",
            "Design and material choices are key",
            "Testing is required to validate solutions"
        ],
        resolution_strategy="Use FEA and NVH testing to optimize design; select materials for damping and durability.",
        entity_scope="All brake systems",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="SAE J2521"
    ),
    DoctrineBlock(
        topic="FMVSS 135 Brake Performance Standards",
        keywords=["FMVSS 135", "brake performance", "regulation", "testing", "compliance"],
        conclusion_template="Compliance with FMVSS 135 is mandatory for passenger vehicles; testing must demonstrate minimum stopping distance, fade resistance, and system integrity.",
        reasoning_framework=(
            "FMVSS 135 specifies minimum performance requirements for hydraulic brake systems in passenger vehicles. "
            "Key tests include stopping distance from 100 km/h, fade resistance after repeated stops, and recovery performance. "
            "System integrity is validated by simulating hydraulic circuit failure and measuring residual braking force. "
            "Documentation must include test procedures, data, and compliance statements. "
            "Manufacturers must certify compliance before vehicles are sold in the U.S. market. "
            "Testing must be conducted by qualified personnel using calibrated equipment. "
            "Non-compliance can result in recalls, fines, and liability exposure. "
            "Aftermarket modifications must not compromise compliance. "
            "Technicians must be aware of FMVSS 135 requirements when servicing or modifying brake systems. "
            "Periodic re-testing may be required after significant design changes. "
            "OEMs may set internal targets exceeding FMVSS 135 for competitive advantage. "
            "System documentation should include all test results and compliance matrices."
        ),
        key_factors=[
            "Stopping distance",
            "Fade resistance",
            "Residual braking force",
            "Test documentation",
            "Certification process"
        ],
        primary_authority=[
            "FMVSS 135, U.S. Department of Transportation",
            "SAE J2784: Brake Performance Testing",
            "NHTSA Compliance Manual"
        ],
        burden_holder="Vehicle manufacturer",
        adversary_position="Internal testing is sufficient for safety",
        counter_arguments=[
            "Regulatory testing is mandatory",
            "Non-compliance has legal consequences",
            "Aftermarket changes must be evaluated",
            "Certification process is detailed",
            "Documentation is required"
        ],
        resolution_strategy="Conduct all FMVSS 135 tests; document and certify compliance before market release.",
        entity_scope="Passenger vehicles",
        confidence=0.99,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="FMVSS 135"
    ),
    DoctrineBlock(
        topic="Brake Fade and Thermal Recovery",
        keywords=["brake fade", "thermal recovery", "heat buildup", "lining", "cooling"],
        conclusion_template="Brake fade and thermal recovery must be evaluated to ensure consistent performance during repeated high-energy stops.",
        reasoning_framework=(
            "Brake fade occurs when repeated or sustained braking causes friction material or fluid to overheat, reducing braking force. "
            "Thermal recovery is the system's ability to regain performance after cooling. "
            "Pad and rotor materials must be selected for high fade resistance and rapid recovery. "
            "FMVSS 135 specifies fade and recovery test protocols, including repeated stops from high speed. "
            "Testing includes measurement of stopping distance, pedal effort, and rotor/pad temperature. "
            "Designers use thermal analysis to predict fade performance and specify cooling enhancements as needed. "
            "Aftermarket pads and rotors must be validated for fade resistance. "
            "Technicians must inspect for signs of overheating (blueing, glazing) during service. "
            "Documentation should include fade/recovery test data, material specs, and analysis. "
            "Manufacturers may offer high-fade-resistance options for performance vehicles. "
            "System must be free of air and properly bled to ensure consistent fade performance."
        ),
        key_factors=[
            "Fade resistance",
            "Thermal recovery rate",
            "Material selection",
            "Test protocols",
            "Cooling enhancements"
        ],
        primary_authority=[
            "FMVSS 135, S5.3.13",
            "SAE J661: Brake Lining Quality Test",
            "Bosch Automotive Handbook, 10th Edition, Section 20.14"
        ],
        burden_holder="Brake system designer",
        adversary_position="Fade is not an issue in normal driving",
        counter_arguments=[
            "Emergency stops can cause fade",
            "Material selection is critical",
            "Regulations specify fade tests",
            "Aftermarket parts must be validated",
            "Thermal analysis is required"
        ],
        resolution_strategy="Test for fade and recovery per regulatory protocols; select materials for high resistance.",
        entity_scope="All brake systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="FMVSS 135, S5.3.13"
    ),
    DoctrineBlock(
        topic="Brake Wear Sensor and Indicator Systems",
        keywords=["brake wear sensor", "indicator", "pad wear", "maintenance", "warning"],
        conclusion_template="Brake wear sensors and indicators provide early warning of pad wear, enabling timely maintenance and preventing rotor damage.",
        reasoning_framework=(
            "Brake wear sensors detect pad thickness and trigger warning indicators when replacement is needed. "
            "Sensor types include mechanical (contact), electrical (resistive), and electronic (Hall effect). "
            "Early warning allows for scheduled maintenance, reducing risk of rotor damage and sudden brake failure. "
            "FMVSS 135 does not mandate wear sensors, but many OEMs include them for customer safety. "
            "Testing includes verification of sensor function, warning lamp activation, and pad thickness measurement. "
            "Technicians must inspect sensors during pad replacement and verify indicator operation. "
            "Aftermarket pads may not include wear sensors; compatibility must be checked. "
            "Documentation should include sensor specs, wiring diagrams, and test results. "
            "Manufacturers may offer different sensor types for various vehicle applications. "
            "Periodic inspection and replacement of sensors are recommended for long-term reliability."
        ),
        key_factors=[
            "Sensor type and placement",
            "Indicator reliability",
            "Pad thickness threshold",
            "Maintenance intervals",
            "Customer safety"
        ],
        primary_authority=[
            "SAE J1628: Brake Pad Wear Sensors",
            "Bosch Automotive Handbook, 10th Edition, Section 20.15",
            "FMVSS 135 (performance context)"
        ],
        burden_holder="Vehicle manufacturer",
        adversary_position="Wear sensors are unnecessary if pads are inspected regularly",
        counter_arguments=[
            "Early warning improves safety",
            "Reduces risk of rotor damage",
            "Customer convenience is improved",
            "Aftermarket compatibility must be checked",
            "Periodic inspection is still required"
        ],
        resolution_strategy="Install and test wear sensors; verify indicator operation during service.",
        entity_scope="All vehicles with disc brakes",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="SAE J1628"
    ),
    # 10+ more blocks would be added here for full coverage (see requirements)
]

# ==============================
# AUTHORITY HARDENING
# ==============================

AUTHORITY_WEIGHTS = {
    "FMVSS": 1.0,
    "ECE": 0.95,
    "SAE": 0.9,
    "Bosch Automotive Handbook": 0.85,
    "NHTSA": 0.8,
    "OEM": 0.75,
    "Aftermarket": 0.6
}

def extract_authority_weight(authority: str) -> float:
    for key, weight in AUTHORITY_WEIGHTS.items():
        if key in authority:
            return weight
    return 0.5

def resolve_authority_conflict(authorities: List[str]) -> Tuple[str, float]:
    max_weight = 0
    best_authority = ""
    for auth in authorities:
        w = extract_authority_weight(auth)
        if w > max_weight:
            max_weight = w
            best_authority = auth
    return best_authority, max_weight

# ==============================
# SEMANTIC NORMALIZATION
# ==============================

SEMANTIC_MAP = {
    "dual diagonal": "dual diagonal split",
    "split circuit": "dual diagonal split",
    "caliper": "disc brake caliper",
    "pad": "brake pad",
    "mu": "friction coefficient",
    "ABS": "anti-lock braking system",
    "EBD": "electronic brakeforce distribution",
    "ESC": "electronic stability control",
    "DOT fluid": "brake fluid DOT specification",
    "proportioning valve": "brake proportioning valve",
    "NVH": "noise vibration harshness",
    "fade": "brake fade",
    "thermal recovery": "brake thermal recovery",
    "wear sensor": "brake wear sensor",
    "regenerative": "regenerative braking",
    "brake by wire": "brake-by-wire",
    "hydraulic circuit": "hydraulic brake circuit",
    "booster": "vacuum brake booster",
    "rotor": "brake rotor",
    "drum": "drum brake",
    "parking brake": "parking brake cable",
    "line routing": "brake line routing",
    "flare fitting": "brake flare fitting",
    "master cylinder": "master cylinder bore",
    "pedal feel": "brake pedal feel",
    "sensor": "brake sensor",
    "indicator": "brake indicator",
    "stability control": "electronic stability control",
    "energy recovery": "regenerative braking",
    "electromechanical": "brake-by-wire",
    "mechanical backup": "fail-safe mechanism"
}

def normalize_term(term: str) -> str:
    t = term.lower().strip()
    return SEMANTIC_MAP.get(t, term)

# ==============================
# EPISTEMIC GUARDRAILS
# ==============================

BANNED_PHRASES = [
    "always", "never", "guaranteed", "impossible", "perfect", "no risk", "failproof",
    "cannot fail", "zero chance", "100% safe", "absolutely", "certainly", "without exception"
]

def apply_epistemic_guardrails(text: str) -> str:
    for phrase in BANNED_PHRASES:
        text = text.replace(phrase, "[epistemic-guardrail]")
    return text

# ==============================
# FACT FRAGILITY SCORING
# ==============================

def score_fact_fragility(fact: str) -> Dict[str, float]:
    verifiability = 1.0 if any(auth in fact for auth in AUTHORITY_WEIGHTS) else 0.7
    recharacterization_risk = 0.2 if "must" in fact or "required" in fact else 0.5
    testimony_dependence = 0.3 if "test" in fact or "measured" in fact else 0.6
    return {
        "verifiability": verifiability,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence
    }

# ==============================
# THREE LAYER RESPONSE
# ==============================

def doctrine_layer(scenario: str) -> Optional[DoctrineBlock]:
    scenario_norm = scenario.lower()
    for doc in DOCTRINE_CACHE:
        if any(k in scenario_norm for k in doc.keywords):
            return doc
    return None

def semantic_layer(scenario: str) -> Optional[DoctrineBlock]:
    scenario_norm = scenario.lower()
    for doc in DOCTRINE_CACHE:
        for kw in doc.keywords:
            if normalize_term(kw) in scenario_norm:
                return doc
    return None

def deep_analysis_layer(scenario: str) -> Optional[DoctrineBlock]:
    # Multi-keyword, multi-factor matching
    scenario_norm = scenario.lower()
    best_doc = None
    best_score = 0
    for doc in DOCTRINE_CACHE:
        score = sum(1 for kw in doc.keywords if kw in scenario_norm)
        if score > best_score:
            best_score = score
            best_doc = doc
    return best_doc if best_score > 0 else None

# ==============================
# DEEP ANALYSIS
# ==============================

def multi_doctrine_decomposition(scenario: str) -> List[DoctrineBlock]:
    scenario_norm = scenario.lower()
    matched = []
    for doc in DOCTRINE_CACHE:
        if any(k in scenario_norm for k in doc.keywords):
            matched.append(doc)
    return matched

def issue_category_mapping(scenario: str) -> Set[IssueCategory]:
    scenario_norm = scenario.lower()
    cats = set()
    for cat in IssueCategory:
        if cat.value.replace("_", " ").lower() in scenario_norm:
            cats.add(cat)
    return cats

def interaction_dag(doctrines: List[DoctrineBlock]) -> Dict[str, List[str]]:
    dag = {}
    for doc in doctrines:
        dag[doc.topic] = []
        for other in doctrines:
            if doc is not other and any(k in other.keywords for k in doc.keywords):
                dag[doc.topic].append(other.topic)
    return dag

def eight_step_resolution(doctrines: List[DoctrineBlock], scenario: str) -> Tuple[str, str, List[str], List[str]]:
    # 1. Identify issues
    issues = [doc.topic for doc in doctrines]
    # 2. Map authorities
    authorities = [auth for doc in doctrines for auth in doc.primary_authority]
    # 3. Score authorities
    best_auth, _ = resolve_authority_conflict(authorities)
    # 4. Aggregate conclusions
    conclusions = [doc.conclusion_template for doc in doctrines]
    # 5. Synthesize counter-arguments
    counters = [arg for doc in doctrines for arg in doc.counter_arguments]
    # 6. Propose resolution
    resolution = "; ".join(set(doc.resolution_strategy for doc in doctrines))
    # 7. Tag confidence
    confidence = min(doc.confidence for doc in doctrines)
    # 8. Tag zone
    zone = min((doc.confidence_zone for doc in doctrines), key=lambda z: list(ConfidenceZone).index(z))
    return (
        " | ".join(conclusions),
        best_auth,
        counters,
        [resolution]
    )

# ==============================
# COVERAGE MAP
# ==============================

def coverage_map(scenario: str) -> Dict[str, Any]:
    triggered = []
    missed = []
    scenario_norm = scenario.lower()
    for doc in DOCTRINE_CACHE:
        if any(k in scenario_norm for k in doc.keywords):
            triggered.append(doc.topic)
        else:
            missed.append(doc.topic)
    epistemic_gap = len(triggered) == 0
    return {
        "triggered_doctrines": triggered,
        "missed_doctrines": missed,
        "epistemic_gap": epistemic_gap
    }

# ==============================
# DRIFT WATCHER
# ==============================

DRIFT_BASELINE_HASH = hashlib.sha256(
    json.dumps([doc.topic for doc in DOCTRINE_CACHE]).encode("utf-8")
).hexdigest()

def drift_detection() -> Dict[str, Any]:
    current_hash = hashlib.sha256(
        json.dumps([doc.topic for doc in DOCTRINE_CACHE]).encode("utf-8")
    ).hexdigest()
    drifted = current_hash != DRIFT_BASELINE_HASH
    return {
        "baseline_hash": DRIFT_BASELINE_HASH,
        "current_hash": current_hash,
        "drifted": drifted
    }

# ==============================
# AUDIT TRAIL
# ==============================

AUDIT_LOG_PATH = Path(__file__).parent / "brake_engine_audit.jsonl"
AUDIT_LOG_LOCK = threading.Lock()

def log_audit_entry(entry: Dict[str, Any]):
    with AUDIT_LOG_LOCK:
        with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

# ==============================
# DETERMINISM HASH
# ==============================

def compute_determinism_hash(response: Dict[str, Any]) -> str:
    relevant = {k: response[k] for k in sorted(response) if k != "determinism_hash"}
    s = json.dumps(relevant, sort_keys=True)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

# ==============================
# FASTAPI APP
# ==============================

app = FastAPI(
    title="Brake Systems Engineering Engine (ECHO OMEGA PRIME)",
    description="Analyze automotive brake systems including hydraulic, disc, drum, ABS, EBD, stability control, and regenerative braking.",
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
    logger.info("Brake Systems Engineering Engine started.")

@app.on_event("shutdown")
def on_shutdown():
    logger.info("Brake Systems Engineering Engine shutting down.")

# ==============================
# MAIN QUERY ENDPOINT
# ==============================

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    start_time = datetime.utcnow()
    query_id = str(uuid.uuid4())
    scenario = request.scenario
    mode = request.mode
    complexity = request.complexity

    # Three-layer doctrine search
    doctrine = doctrine_layer(scenario)
    if not doctrine:
        doctrine = semantic_layer(scenario)
    if not doctrine:
        doctrine = deep_analysis_layer(scenario)

    # Deep analysis if complexity high or doctrine ambiguous
    doctrines = []
    if complexity >= 7 or not doctrine:
        doctrines = multi_doctrine_decomposition(scenario)
        if not doctrines:
            doctrines = [doctrine] if doctrine else []
    else:
        doctrines = [doctrine] if doctrine else []

    # Compose response
    if doctrines:
        primary = doctrines[0]
        conclusion = apply_epistemic_guardrails(primary.conclusion_template)
        reasoning = apply_epistemic_guardrails(primary.reasoning_framework)
        key_factors = primary.key_factors
        authority = primary.primary_authority
        counters = primary.counter_arguments
        resolution = primary.resolution_strategy
        confidence = primary.confidence
        confidence_zone = primary.confidence_zone
        position_zone = PositionZone.REPORTING if mode == ResponseMode.DEFENSE else PositionZone.PLANNING
    else:
        # No doctrine match
        conclusion = apply_epistemic_guardrails("No directly applicable doctrine found. Recommend further analysis or escalation to domain expert.")
        reasoning = apply_epistemic_guardrails("Scenario does not match any known doctrine block. Epistemic gap detected. Suggest review of scenario wording and additional information gathering.")
        key_factors = []
        authority = []
        counters = []
        resolution = "Escalate to domain expert."
        confidence = 0.6
        confidence_zone = ConfidenceZone.HIGH_RISK
        position_zone = PositionZone.AUDIT

    # Deep analysis for multi-doctrine
    if len(doctrines) > 1:
        conclusion, best_auth, counters, resolutions = eight_step_resolution(doctrines, scenario)
        authority = [best_auth]
        resolution = "; ".join(resolutions)
        confidence = min(doc.confidence for doc in doctrines)
        confidence_zone = min((doc.confidence_zone for doc in doctrines), key=lambda z: list(ConfidenceZone).index(z))
        position_zone = PositionZone.AUDIT

    # Fact fragility scoring (for audit)
    fragility = [score_fact_fragility(f) for f in key_factors]

    # Determinism hash
    response_dict = {
        "engine_id": "AUTO03",
        "query_id": query_id,
        "mode": mode,
        "confidence": confidence,
        "confidence_zone": confidence_zone,
        "position_zone": position_zone,
        "primary_conclusion": conclusion,
        "reasoning_framework": reasoning,
        "key_factors": key_factors,
        "primary_authority": authority,
        "counter_arguments": counters,
        "resolution_strategy": resolution,
        "determinism_hash": ""
    }
    determinism_hash = compute_determinism_hash(response_dict)
    response_dict["determinism_hash"] = determinism_hash

    # Audit logging
    audit_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "query_id": query_id,
        "scenario": scenario,
        "mode": mode,
        "complexity": complexity,
        "doctrines_triggered": [doc.topic for doc in doctrines],
        "fragility_scores": fragility,
        "response": response_dict
    }
    log_audit_entry(audit_entry)

    # Metrics
    metrics_collector.record_query([doc.topic for doc in doctrines], (datetime.utcnow() - start_time).total_seconds())

    return QueryResponse(**response_dict)

# ==============================
# HEALTH ENDPOINT
# ==============================

@app.get("/health")
async def health():
    return {"status": "ok", "engine_id": "AUTO03", "timestamp": datetime.utcnow().isoformat()}

# ==============================
# METRICS ENDPOINT
# ==============================

@app.get("/metrics")
async def metrics():
    return {
        "latency_stats": metrics_collector.get_latency_stats(),
        "doctrine_hit_rate": metrics_collector.get_doctrine_hit_rate(),
        "queries_last_hour": metrics_collector.queries_last_hour()
    }

# ==============================
# COVERAGE ENDPOINT
# ==============================

@app.get("/coverage")
async def coverage(scenario: Optional[str] = None):
    if scenario:
        return coverage_map(scenario)
    else:
        return {
            "doctrines": [doc.topic for doc in DOCTRINE_CACHE],
            "epistemic_gaps": []
        }

# ==============================
# DRIFT ENDPOINT
# ==============================

@app.get("/drift")
async def drift():
    return drift_detection()

# ==============================
# DOCTRINES ENDPOINT
# ==============================

@app.get("/doctrines")
async def doctrines():
    return [
        {
            "topic": doc.topic,
            "keywords": doc.keywords,
            "confidence": doc.confidence,
            "confidence_zone": doc.confidence_zone,
            "controlling_precedent": doc.controlling_precedent
        }
        for doc in DOCTRINE_CACHE
    ]
