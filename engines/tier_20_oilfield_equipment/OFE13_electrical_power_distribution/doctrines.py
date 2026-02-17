from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

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
    confidence_zone: str
    controlling_precedent: str

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Primary Voltage Selection in Oilfield Power Distribution",
        keywords=["primary voltage", "oilfield", "distribution", "substation", "transmission"],
        conclusion_template="Select primary voltage based on load demand, distance, and utility availability.",
        reasoning_framework=(
            "Primary voltage selection in oilfield power distribution is governed by the anticipated load demand, "
            "distance from utility interconnection, and the voltage levels offered by the utility provider. "
            "Higher voltages are preferred for longer distances to minimize line losses and voltage drop, "
            "while lower voltages may be suitable for compact sites with moderate loads. "
            "The selection process involves evaluating the total connected load, future expansion plans, "
            "and the compatibility with downstream transformers and switchgear. "
            "NEC and IEEE standards provide guidance on minimum and maximum voltage levels, "
            "while local utility tariffs and interconnection agreements may impose constraints. "
            "Environmental factors, such as ambient temperature and altitude, may affect insulation requirements. "
            "The final selection must ensure reliable operation, safety, and compliance with regulatory requirements."
        ),
        key_factors=[
            "Load demand",
            "Distance from utility",
            "Utility voltage offerings",
            "Line losses",
            "Voltage drop",
            "Expansion plans",
            "Regulatory compliance"
        ],
        primary_authority=["NEC", "IEEE Std 141", "Local Utility Standards"],
        burden_holder="Design Engineer",
        adversary_position="Utility may restrict voltage options; cost constraints may favor lower voltages.",
        counter_arguments=[
            "Higher voltages increase equipment cost and complexity.",
            "Lower voltages may lead to excessive losses and voltage drop."
        ],
        resolution_strategy="Perform load flow and voltage drop studies; negotiate with utility; select optimal voltage.",
        entity_scope="Oilfield Power Distribution System",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 141 (Red Book)"
    ),
    DoctrineBlock(
        topic="Secondary Voltage Selection in Oilfield Power Distribution",
        keywords=["secondary voltage", "distribution", "transformer", "load", "utilization"],
        conclusion_template="Choose secondary voltage based on equipment ratings, MCC requirements, and NEC guidelines.",
        reasoning_framework=(
            "Secondary voltage selection is determined by the utilization equipment ratings, "
            "Motor Control Center (MCC) requirements, and NEC guidelines for branch circuit voltages. "
            "Standard voltages such as 480V, 600V, and 208V are commonly used in oilfield applications. "
            "The selection must ensure compatibility with motor starters, VFDs, and protective devices. "
            "Voltage drop calculations are performed to validate adequacy for the farthest load. "
            "Transformer secondary winding configuration (delta or wye) is chosen based on grounding and load balance needs. "
            "Future expansion and harmonics considerations may influence the choice. "
            "Safety and regulatory compliance are paramount."
        ),
        key_factors=[
            "Equipment ratings",
            "MCC requirements",
            "NEC voltage standards",
            "Voltage drop",
            "Transformer configuration",
            "Expansion plans"
        ],
        primary_authority=["NEC", "IEEE Std 141"],
        burden_holder="Electrical Designer",
        adversary_position="Non-standard voltages may complicate procurement and maintenance.",
        counter_arguments=[
            "Standard voltages simplify maintenance and spare parts.",
            "Non-standard voltages may offer operational advantages."
        ],
        resolution_strategy="Select standard voltage unless justified; validate with load and voltage drop studies.",
        entity_scope="Oilfield Power Distribution System",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NEC Article 210"
    ),
    DoctrineBlock(
        topic="Transformer Sizing in Oilfield Applications",
        keywords=["transformer", "sizing", "kVA", "oilfield", "load", "impedance"],
        conclusion_template="Size transformer based on connected load, future expansion, and starting currents.",
        reasoning_framework=(
            "Transformer sizing requires calculation of total connected load, consideration of future expansion, "
            "and allowance for motor starting currents. The kVA rating must accommodate peak demand and transient loads. "
            "Impedance selection affects fault current levels and voltage regulation. "
            "Tap changers may be included for voltage adjustment. "
            "NEC and IEEE standards provide minimum sizing requirements. "
            "Thermal and dielectric ratings must be validated for site conditions. "
            "Coordination with protective devices is essential to ensure safe operation."
        ),
        key_factors=[
            "Connected load",
            "Future expansion",
            "Motor starting current",
            "Impedance",
            "Tap changer",
            "Thermal rating"
        ],
        primary_authority=["NEC", "IEEE Std C57.12", "API RP 500"],
        burden_holder="Electrical Engineer",
        adversary_position="Oversized transformers increase cost and losses; undersized risk overload.",
        counter_arguments=[
            "Oversizing provides margin for expansion.",
            "Undersizing may reduce capital cost but risks reliability."
        ],
        resolution_strategy="Perform load analysis; select transformer with margin; validate with NEC and IEEE standards.",
        entity_scope="Oilfield Power Distribution System",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std C57.12"
    ),
    DoctrineBlock(
        topic="kVA Calculation in Oilfield Power Distribution",
        keywords=["kVA", "calculation", "load", "oilfield", "power factor"],
        conclusion_template="Calculate kVA using total load and power factor; validate against transformer rating.",
        reasoning_framework=(
            "kVA calculation is performed by summing the real power (kW) and dividing by the power factor. "
            "All connected and anticipated loads are included, with adjustments for diversity and utilization factors. "
            "Motor starting and transient loads are considered to ensure transformer and generator adequacy. "
            "NEC requires that the calculated kVA be used for sizing transformers, generators, and switchgear. "
            "Harmonic loads may require derating. "
            "The calculation must be documented and validated against equipment ratings."
        ),
        key_factors=[
            "Total load",
            "Power factor",
            "Diversity factor",
            "Motor starting",
            "Harmonic loads"
        ],
        primary_authority=["NEC", "IEEE Std 141"],
        burden_holder="Design Engineer",
        adversary_position="Underestimating kVA risks overload; overestimating increases cost.",
        counter_arguments=[
            "Accurate load survey ensures proper sizing.",
            "Conservative estimates provide reliability margin."
        ],
        resolution_strategy="Use detailed load survey; apply diversity; validate with NEC requirements.",
        entity_scope="Oilfield Power Distribution System",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NEC Article 220"
    ),
    DoctrineBlock(
        topic="Impedance and Tap Changing in Oilfield Transformer Applications",
        keywords=["impedance", "tap changer", "transformer", "oilfield", "voltage regulation"],
        conclusion_template="Select transformer impedance to balance fault current and voltage regulation; use tap changer for adjustment.",
        reasoning_framework=(
            "Transformer impedance is selected to limit fault current while maintaining acceptable voltage regulation. "
            "High impedance reduces fault current but may cause excessive voltage drop during load changes. "
            "Tap changers are used to adjust secondary voltage to compensate for system variations. "
            "NEC and IEEE standards specify minimum and maximum impedance values based on system voltage and kVA. "
            "Coordination with protective devices is critical to ensure safe operation. "
            "Site-specific conditions, such as distance to load and motor starting requirements, may influence impedance selection."
        ),
        key_factors=[
            "Fault current",
            "Voltage regulation",
            "Tap changer",
            "System voltage",
            "Motor starting"
        ],
        primary_authority=["IEEE Std C57.12", "NEC"],
        burden_holder="Electrical Engineer",
        adversary_position="Low impedance increases fault risk; high impedance may cause voltage issues.",
        counter_arguments=[
            "Tap changer mitigates voltage drop.",
            "Impedance selection must balance protection and performance."
        ],
        resolution_strategy="Perform fault and load flow studies; select impedance per IEEE and NEC; validate tap changer settings.",
        entity_scope="Oilfield Power Distribution System",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std C57.12"
    ),
    DoctrineBlock(
        topic="Motor Control Center (MCC) Breaker and Starter Selection",
        keywords=["MCC", "breaker", "starter", "motor", "oilfield", "selection"],
        conclusion_template="Select MCC breaker and starter based on motor rating, starting method, and NEC requirements.",
        reasoning_framework=(
            "Breaker and starter selection for MCCs is based on motor rating, starting method (across-the-line, soft start, VFD), "
            "and NEC requirements for short-circuit and overload protection. "
            "The breaker must be rated for the motor's full load current and withstand inrush during starting. "
            "Starter selection depends on motor type, application, and site conditions. "
            "Coordination with upstream protective devices is essential to prevent nuisance tripping. "
            "Hazardous area classification may require explosion-proof or intrinsically safe starters. "
            "Documentation and validation against manufacturer data is required."
        ),
        key_factors=[
            "Motor rating",
            "Starting method",
            "Breaker rating",
            "Overload protection",
            "Hazardous area classification"
        ],
        primary_authority=["NEC", "IEEE Std 1584", "API RP 500"],
        burden_holder="Electrical Designer",
        adversary_position="Improper selection risks equipment damage or safety violations.",
        counter_arguments=[
            "Manufacturer's recommendations provide guidance.",
            "NEC mandates minimum protection levels."
        ],
        resolution_strategy="Select per NEC and manufacturer data; validate with site conditions and hazardous area requirements.",
        entity_scope="Motor Control Center",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NEC Article 430"
    ),
    DoctrineBlock(
        topic="Variable Frequency Drive (VFD) Application for ESP and Rod Pump Motors",
        keywords=["VFD", "ESP", "rod pump", "motor", "oilfield", "application"],
        conclusion_template="Apply VFD for ESP and rod pump motors to optimize speed and energy efficiency.",
        reasoning_framework=(
            "VFDs are used for ESP and rod pump motors to control speed, optimize energy consumption, and improve process flexibility. "
            "Selection involves matching VFD rating to motor size and load profile. "
            "Harmonic mitigation is required to comply with IEEE 519. "
            "Environmental conditions, such as temperature and dust, may require NEMA-rated enclosures. "
            "Hazardous area requirements may necessitate explosion-proof or intrinsically safe VFDs. "
            "Integration with MCC and SCADA systems must be validated. "
            "NEC and API RP 500 provide guidance on installation and protection."
        ),
        key_factors=[
            "Motor size",
            "Load profile",
            "Harmonic mitigation",
            "Environmental conditions",
            "Hazardous area classification"
        ],
        primary_authority=["IEEE 519", "NEC", "API RP 500"],
        burden_holder="Electrical Engineer",
        adversary_position="VFDs may introduce harmonics and require additional protection.",
        counter_arguments=[
            "Harmonic filters mitigate issues.",
            "Proper selection ensures reliability."
        ],
        resolution_strategy="Select VFD per motor and site requirements; apply harmonic mitigation; validate hazardous area compliance.",
        entity_scope="ESP and Rod Pump Motor Systems",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 519"
    ),
    DoctrineBlock(
        topic="Hazardous Area Classification: NEC 500, 505 and API RP 500",
        keywords=["hazardous area", "classification", "NEC 500", "NEC 505", "API RP 500", "oilfield"],
        conclusion_template="Classify hazardous areas per NEC 500, 505 and API RP 500; document and validate.",
        reasoning_framework=(
            "Hazardous area classification is performed according to NEC 500, 505 and API RP 500. "
            "Areas are classified as Class I, Division 1 or 2, or Zone 0, 1, or 2 based on the presence and frequency of flammable gases or vapors. "
            "The process involves site survey, identification of potential sources, and documentation of boundaries. "
            "Classification affects equipment selection, wiring methods, and protection requirements. "
            "Periodic review and reclassification may be required due to process changes."
        ),
        key_factors=[
            "Presence of flammable gases",
            "Frequency of occurrence",
            "Site survey",
            "Documentation",
            "Process changes"
        ],
        primary_authority=["NEC 500", "NEC 505", "API RP 500"],
        burden_holder="Safety Engineer",
        adversary_position="Improper classification risks safety and regulatory violations.",
        counter_arguments=[
            "Conservative classification enhances safety.",
            "Over-classification increases cost."
        ],
        resolution_strategy="Perform thorough site survey; classify per standards; document and review periodically.",
        entity_scope="Oilfield Facilities",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NEC 500, API RP 500"
    ),
    DoctrineBlock(
        topic="Explosion-Proof Equipment for Class I, Division 1 and 2 Areas",
        keywords=["explosion-proof", "Class I", "Division 1", "Division 2", "equipment", "oilfield"],
        conclusion_template="Select explosion-proof equipment for Class I, Division 1 and 2 areas per NEC and API RP 500.",
        reasoning_framework=(
            "Explosion-proof equipment is required for Class I, Division 1 and 2 areas as defined by NEC and API RP 500. "
            "Equipment must be certified and labeled for the specific classification. "
            "Selection involves verification of enclosure ratings, temperature codes, and compatibility with process fluids. "
            "Installation must follow NEC wiring methods and maintain integrity of explosion-proof barriers. "
            "Periodic inspection and maintenance are required to ensure continued compliance."
        ),
        key_factors=[
            "Area classification",
            "Equipment certification",
            "Enclosure rating",
            "Temperature code",
            "Installation method"
        ],
        primary_authority=["NEC 500", "API RP 500"],
        burden_holder="Electrical Engineer",
        adversary_position="Non-compliant equipment risks explosion and regulatory action.",
        counter_arguments=[
            "Certified equipment ensures safety.",
            "Periodic inspection maintains compliance."
        ],
        resolution_strategy="Select certified equipment; install per NEC; inspect regularly.",
        entity_scope="Class I, Division 1 and 2 Areas",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NEC 500"
    ),
    DoctrineBlock(
        topic="Intrinsically Safe Barriers: Zener and Shunt Diode Application",
        keywords=["intrinsically safe", "barrier", "zener", "shunt diode", "oilfield", "hazardous area"],
        conclusion_template="Apply intrinsically safe barriers using Zener or shunt diode for hazardous area instrumentation.",
        reasoning_framework=(
            "Intrinsically safe barriers are used to limit energy in hazardous area instrumentation circuits. "
            "Zener and shunt diode barriers are selected based on voltage and current requirements. "
            "Installation must ensure proper grounding and isolation to prevent accidental energy transfer. "
            "NEC and API RP 500 provide guidance on barrier selection and wiring methods. "
            "Periodic testing and documentation are required to maintain compliance."
        ),
        key_factors=[
            "Voltage and current requirements",
            "Barrier certification",
            "Grounding",
            "Isolation",
            "Documentation"
        ],
        primary_authority=["NEC 500", "API RP 500"],
        burden_holder="Instrumentation Engineer",
        adversary_position="Improper barrier selection risks ignition.",
        counter_arguments=[
            "Certified barriers ensure safety.",
            "Proper grounding prevents failures."
        ],
        resolution_strategy="Select certified barrier; install per NEC; test and document regularly.",
        entity_scope="Hazardous Area Instrumentation",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NEC 500"
    ),
    DoctrineBlock(
        topic="Power Cable Sizing: Ampacity and Voltage Drop per NEC 310",
        keywords=["power cable", "sizing", "ampacity", "voltage drop", "NEC 310", "oilfield"],
        conclusion_template="Size power cables based on ampacity and voltage drop per NEC 310; validate for site conditions.",
        reasoning_framework=(
            "Power cable sizing is performed by calculating ampacity and voltage drop per NEC 310. "
            "Ampacity is determined by conductor material, insulation type, ambient temperature, and installation method. "
            "Voltage drop is calculated based on load current and cable length. "
            "Site-specific factors such as soil thermal resistivity and grouping may require derating. "
            "Cable selection must ensure compliance with NEC and provide margin for future expansion. "
            "Documentation and periodic review are required."
        ),
        key_factors=[
            "Ampacity",
            "Voltage drop",
            "Conductor material",
            "Ambient temperature",
            "Installation method"
        ],
        primary_authority=["NEC 310", "IEEE Std 141"],
        burden_holder="Electrical Designer",
        adversary_position="Undersized cables risk overheating; oversized increase cost.",
        counter_arguments=[
            "Proper sizing ensures reliability.",
            "Derating factors must be considered."
        ],
        resolution_strategy="Calculate ampacity and voltage drop; apply derating; select cable per NEC.",
        entity_scope="Oilfield Power Distribution",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NEC 310"
    ),
    DoctrineBlock(
        topic="Grounding System: Electrode and Grid Resistance",
        keywords=["grounding", "system", "electrode", "grid resistance", "oilfield"],
        conclusion_template="Design grounding system to achieve electrode and grid resistance per IEEE and NEC.",
        reasoning_framework=(
            "Grounding system design aims to achieve electrode and grid resistance below specified thresholds per IEEE and NEC. "
            "Soil resistivity is measured to determine electrode configuration. "
            "Grid layout is designed to minimize step and touch voltage. "
            "Periodic testing and maintenance are required to ensure continued compliance. "
            "Lightning protection integration may be necessary."
        ),
        key_factors=[
            "Soil resistivity",
            "Electrode configuration",
            "Grid layout",
            "Step and touch voltage",
            "Testing and maintenance"
        ],
        primary_authority=["IEEE Std 80", "NEC"],
        burden_holder="Electrical Engineer",
        adversary_position="High resistance risks safety; excessive cost for low resistance.",
        counter_arguments=[
            "Testing validates design.",
            "Integration with lightning protection improves safety."
        ],
        resolution_strategy="Measure soil resistivity; design per IEEE and NEC; test and maintain system.",
        entity_scope="Oilfield Facilities",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 80"
    ),
    DoctrineBlock(
        topic="Lightning Protection System: Rod, Conductor, and Ground Integration",
        keywords=["lightning protection", "rod", "conductor", "ground", "integration", "oilfield"],
        conclusion_template="Integrate lightning rods, conductors, and grounding per IEEE and NEC for oilfield protection.",
        reasoning_framework=(
            "Lightning protection system design integrates rods, conductors, and grounding to provide a safe path for lightning discharge. "
            "Rod placement is determined by site layout and risk assessment. "
            "Conductors are sized and routed to minimize impedance. "
            "Grounding is coordinated with facility grounding system. "
            "Periodic inspection and maintenance are required. "
            "Compliance with IEEE and NEC is mandatory."
        ),
        key_factors=[
            "Rod placement",
            "Conductor sizing",
            "Grounding integration",
            "Inspection",
            "Maintenance"
        ],
        primary_authority=["IEEE Std 998", "NEC"],
        burden_holder="Electrical Engineer",
        adversary_position="Improper integration risks equipment damage.",
        counter_arguments=[
            "Periodic inspection ensures reliability.",
            "Coordination with grounding improves safety."
        ],
        resolution_strategy="Design per IEEE and NEC; inspect and maintain system.",
        entity_scope="Oilfield Facilities",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 998"
    ),
    DoctrineBlock(
        topic="Switchgear: Medium Voltage, Vacuum and SF6 Breaker Application",
        keywords=["switchgear", "medium voltage", "vacuum breaker", "SF6 breaker", "oilfield"],
        conclusion_template="Select medium voltage switchgear and breaker type based on load, fault current, and site conditions.",
        reasoning_framework=(
            "Medium voltage switchgear selection involves evaluating load, fault current, and site conditions. "
            "Vacuum breakers are preferred for reliability and low maintenance. "
            "SF6 breakers offer high interrupting capacity but require environmental controls. "
            "Coordination with protective relays and downstream equipment is essential. "
            "Compliance with IEEE and NEC is required."
        ),
        key_factors=[
            "Load",
            "Fault current",
            "Breaker type",
            "Environmental controls",
            "Coordination"
        ],
        primary_authority=["IEEE Std C37", "NEC"],
        burden_holder="Electrical Engineer",
        adversary_position="Improper selection risks reliability and safety.",
        counter_arguments=[
            "Vacuum breakers reduce maintenance.",
            "SF6 breakers require environmental management."
        ],
        resolution_strategy="Select per load and site conditions; validate with IEEE and NEC.",
        entity_scope="Medium Voltage Switchgear",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std C37"
    ),
    DoctrineBlock(
        topic="Protective Relays: Overcurrent, Differential, and Ground Fault",
        keywords=["protective relay", "overcurrent", "differential", "ground fault", "oilfield"],
        conclusion_template="Apply protective relays for overcurrent, differential, and ground fault per IEEE and NEC.",
        reasoning_framework=(
            "Protective relays are applied to detect overcurrent, differential, and ground fault conditions. "
            "Relay selection is based on system configuration, fault levels, and coordination requirements. "
            "Settings are calculated to ensure selectivity and minimize nuisance tripping. "
            "Periodic testing and calibration are required. "
            "Compliance with IEEE and NEC is mandatory."
        ),
        key_factors=[
            "System configuration",
            "Fault levels",
            "Relay settings",
            "Testing",
            "Calibration"
        ],
        primary_authority=["IEEE Std C37", "NEC"],
        burden_holder="Protection Engineer",
        adversary_position="Improper settings risk equipment damage.",
        counter_arguments=[
            "Periodic testing ensures reliability.",
            "Coordination minimizes nuisance tripping."
        ],
        resolution_strategy="Select and set relays per IEEE and NEC; test and calibrate regularly.",
        entity_scope="Oilfield Power Distribution",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std C37"
    ),
    DoctrineBlock(
        topic="Power Quality: Harmonics and Total Harmonic Distortion (THD) per IEEE 519",
        keywords=["power quality", "harmonics", "THD", "IEEE 519", "oilfield"],
        conclusion_template="Monitor and mitigate harmonics and THD per IEEE 519 for oilfield power quality.",
        reasoning_framework=(
            "Power quality is assessed by monitoring harmonics and THD per IEEE 519. "
            "Sources include VFDs, nonlinear loads, and switching devices. "
            "Mitigation involves applying filters, selecting compatible equipment, and performing periodic measurements. "
            "Compliance with IEEE 519 is required to prevent equipment damage and process disruptions."
        ),
        key_factors=[
            "Harmonic sources",
            "THD measurement",
            "Mitigation methods",
            "Equipment compatibility",
            "Periodic monitoring"
        ],
        primary_authority=["IEEE 519"],
        burden_holder="Electrical Engineer",
        adversary_position="Excessive harmonics risk equipment failure.",
        counter_arguments=[
            "Filters reduce harmonics.",
            "Periodic monitoring ensures compliance."
        ],
        resolution_strategy="Monitor harmonics; apply mitigation; validate compliance with IEEE 519.",
        entity_scope="Oilfield Power Distribution",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 519"
    ),
    DoctrineBlock(
        topic="Power Factor Correction: Capacitor Bank Application",
        keywords=["power factor", "correction", "capacitor bank", "oilfield"],
        conclusion_template="Apply capacitor banks for power factor correction per IEEE and NEC.",
        reasoning_framework=(
            "Power factor correction is achieved by applying capacitor banks to offset inductive loads. "
            "Sizing is based on measured power factor and load profile. "
            "Capacitor placement is determined by system configuration and harmonic analysis. "
            "Periodic monitoring and maintenance are required. "
            "Compliance with IEEE and NEC is mandatory."
        ),
        key_factors=[
            "Measured power factor",
            "Load profile",
            "Capacitor sizing",
            "Placement",
            "Harmonic analysis"
        ],
        primary_authority=["IEEE Std 18", "NEC"],
        burden_holder="Electrical Engineer",
        adversary_position="Improper correction risks resonance and equipment damage.",
        counter_arguments=[
            "Harmonic analysis prevents resonance.",
            "Periodic monitoring ensures reliability."
        ],
        resolution_strategy="Perform harmonic analysis; size and place capacitors per IEEE and NEC.",
        entity_scope="Oilfield Power Distribution",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 18"
    ),
    DoctrineBlock(
        topic="Generator Set Sizing: Diesel and Natural Gas Applications",
        keywords=["generator", "set sizing", "diesel", "natural gas", "oilfield"],
        conclusion_template="Size generator set based on load, starting currents, and site conditions for diesel and natural gas applications.",
        reasoning_framework=(
            "Generator set sizing involves calculating total load, motor starting currents, and site-specific conditions. "
            "Diesel and natural gas generators have different transient response characteristics. "
            "Sizing must ensure adequate capacity for peak demand and transient loads. "
            "NEC and IEEE provide guidance on minimum sizing and protection. "
            "Periodic testing and maintenance are required."
        ),
        key_factors=[
            "Total load",
            "Motor starting",
            "Transient response",
            "Site conditions",
            "Testing and maintenance"
        ],
        primary_authority=["NEC", "IEEE Std 446"],
        burden_holder="Electrical Engineer",
        adversary_position="Undersized generators risk overload; oversized increase cost.",
        counter_arguments=[
            "Accurate load calculation ensures reliability.",
            "Periodic testing validates sizing."
        ],
        resolution_strategy="Calculate load and starting currents; size per NEC and IEEE; test and maintain generator.",
        entity_scope="Oilfield Power Generation",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 446"
    ),
    DoctrineBlock(
        topic="Automatic Transfer Switch (ATS) and Load Shedding",
        keywords=["automatic transfer switch", "ATS", "load shedding", "oilfield"],
        conclusion_template="Apply ATS and load shedding to ensure continuity of power during outages.",
        reasoning_framework=(
            "ATS is applied to transfer load between utility and generator during outages. "
            "Load shedding is implemented to prioritize critical loads and prevent overload. "
            "Selection involves evaluating load profile, transfer time, and site conditions. "
            "Coordination with generator and protective devices is essential. "
            "Compliance with NEC and IEEE is required."
        ),
        key_factors=[
            "Load profile",
            "Transfer time",
            "Critical loads",
            "Coordination",
            "Compliance"
        ],
        primary_authority=["NEC", "IEEE Std 446"],
        burden_holder="Electrical Engineer",
        adversary_position="Improper ATS or load shedding risks blackout.",
        counter_arguments=[
            "Coordination ensures continuity.",
            "Periodic testing validates operation."
        ],
        resolution_strategy="Select ATS and implement load shedding per NEC and IEEE; test and coordinate system.",
        entity_scope="Oilfield Power Distribution",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 446"
    ),
    DoctrineBlock(
        topic="UPS: Uninterruptible Power Supply and Battery Sizing",
        keywords=["UPS", "uninterruptible power supply", "battery sizing", "oilfield"],
        conclusion_template="Size UPS and batteries based on critical load and runtime requirements.",
        reasoning_framework=(
            "UPS and battery sizing is performed by calculating critical load and required runtime. "
            "Selection involves evaluating load profile, battery type, and environmental conditions. "
            "Periodic testing and maintenance are required. "
            "Compliance with IEEE and NEC is mandatory."
        ),
        key_factors=[
            "Critical load",
            "Runtime",
            "Battery type",
            "Environmental conditions",
            "Testing and maintenance"
        ],
        primary_authority=["IEEE Std 485", "NEC"],
        burden_holder="Electrical Engineer",
        adversary_position="Undersized UPS risks downtime; oversized increases cost.",
        counter_arguments=[
            "Accurate load calculation ensures reliability.",
            "Periodic testing validates sizing."
        ],
        resolution_strategy="Calculate critical load and runtime; size per IEEE and NEC; test and maintain UPS.",
        entity_scope="Oilfield Critical Loads",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 485"
    ),
    DoctrineBlock(
        topic="Solar Panel Application for Off-Grid Oilfield Power",
        keywords=["solar panel", "off-grid", "oilfield", "power", "renewable"],
        conclusion_template="Apply solar panels for off-grid oilfield power based on load, site conditions, and storage requirements.",
        reasoning_framework=(
            "Solar panel application involves evaluating load, site solar irradiance, and storage requirements. "
            "Sizing is based on daily energy demand and available sunlight. "
            "Battery storage is selected to ensure continuity during low sunlight periods. "
            "Periodic maintenance and monitoring are required. "
            "Compliance with NEC and IEEE is mandatory."
        ),
        key_factors=[
            "Load",
            "Solar irradiance",
            "Storage requirements",
            "Maintenance",
            "Compliance"
        ],
        primary_authority=["NEC", "IEEE Std 1562"],
        burden_holder="Electrical Engineer",
        adversary_position="Improper sizing risks downtime.",
        counter_arguments=[
            "Accurate site assessment ensures reliability.",
            "Periodic maintenance maintains performance."
        ],
        resolution_strategy="Evaluate site and load; size panels and storage per NEC and IEEE; maintain system.",
        entity_scope="Off-Grid Oilfield Power",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 1562"
    ),
    DoctrineBlock(
        topic="Electrical One-Line Diagram and Coordination Study",
        keywords=["one-line diagram", "coordination study", "oilfield", "power distribution"],
        conclusion_template="Develop electrical one-line diagram and perform coordination study for oilfield power distribution.",
        reasoning_framework=(
            "Electrical one-line diagram is developed to represent power distribution system configuration. "
            "Coordination study is performed to ensure selectivity and minimize nuisance tripping. "
            "Study involves evaluating protective device settings, fault levels, and load profile. "
            "Documentation and periodic review are required. "
            "Compliance with IEEE and NEC is mandatory."
        ),
        key_factors=[
            "System configuration",
            "Protective device settings",
            "Fault levels",
            "Documentation",
            "Review"
        ],
        primary_authority=["IEEE Std 242", "NEC"],
        burden_holder="Electrical Engineer",
        adversary_position="Improper coordination risks blackout.",
        counter_arguments=[
            "Periodic review ensures reliability.",
            "Documentation supports maintenance."
        ],
        resolution_strategy="Develop diagram and perform study per IEEE and NEC; document and review periodically.",
        entity_scope="Oilfield Power Distribution",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 242"
    ),
    DoctrineBlock(
        topic="Arc Flash Analysis and Incident Energy Calculation per NFPA 70E",
        keywords=["arc flash", "incident energy", "NFPA 70E", "oilfield"],
        conclusion_template="Perform arc flash analysis and incident energy calculation per NFPA 70E for oilfield facilities.",
        reasoning_framework=(
            "Arc flash analysis is performed to calculate incident energy and determine PPE requirements per NFPA 70E. "
            "Study involves evaluating system configuration, fault levels, and protective device settings. "
            "Documentation and periodic review are required. "
            "Compliance with NFPA 70E and OSHA is mandatory."
        ),
        key_factors=[
            "System configuration",
            "Fault levels",
            "Protective device settings",
            "Documentation",
            "Review"
        ],
        primary_authority=["NFPA 70E", "OSHA"],
        burden_holder="Safety Engineer",
        adversary_position="Improper analysis risks injury.",
        counter_arguments=[
            "Periodic review ensures safety.",
            "Documentation supports compliance."
        ],
        resolution_strategy="Perform analysis per NFPA 70E; document and review periodically.",
        entity_scope="Oilfield Facilities",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 70E"
    ),
    DoctrineBlock(
        topic="Cable Tray Selection and Installation in Oilfield Facilities",
        keywords=["cable tray", "selection", "installation", "oilfield", "NEC"],
        conclusion_template="Select and install cable trays per NEC and site requirements for oilfield facilities.",
        reasoning_framework=(
            "Cable tray selection is based on load, environmental conditions, and NEC requirements. "
            "Installation must ensure proper support, spacing, and grounding. "
            "Periodic inspection and maintenance are required. "
            "Documentation and compliance with NEC are mandatory."
        ),
        key_factors=[
            "Load",
            "Environmental conditions",
            "Support and spacing",
            "Grounding",
            "Inspection"
        ],
        primary_authority=["NEC", "IEEE Std 1202"],
        burden_holder="Electrical Engineer",
        adversary_position="Improper selection or installation risks cable damage.",
        counter_arguments=[
            "Periodic inspection ensures reliability.",
            "Proper grounding prevents failures."
        ],
        resolution_strategy="Select and install per NEC and IEEE; inspect and maintain trays.",
        entity_scope="Oilfield Facilities",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NEC Article 392"
    ),
    DoctrineBlock(
        topic="Electrical Load Forecasting for Oilfield Expansion",
        keywords=["load forecasting", "oilfield", "expansion", "power distribution"],
        conclusion_template="Forecast electrical load for oilfield expansion using historical data and anticipated growth.",
        reasoning_framework=(
            "Electrical load forecasting is performed using historical data, anticipated growth, and process changes. "
            "Forecasting models may include regression analysis, trend extrapolation, and scenario planning. "
            "Results inform transformer and generator sizing, cable selection, and expansion planning. "
            "Periodic review and adjustment are required."
        ),
        key_factors=[
            "Historical data",
            "Growth projections",
            "Process changes",
            "Forecasting models",
            "Review"
        ],
        primary_authority=["IEEE Std 141", "NEC"],
        burden_holder="Planning Engineer",
        adversary_position="Improper forecasting risks under-sizing or over-sizing.",
        counter_arguments=[
            "Periodic review ensures accuracy.",
            "Scenario planning provides flexibility."
        ],
        resolution_strategy="Use historical data and models; review and adjust periodically.",
        entity_scope="Oilfield Power Distribution",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 141"
    ),
    DoctrineBlock(
        topic="Electrical Equipment Maintenance and Reliability in Oilfield Facilities",
        keywords=["equipment maintenance", "reliability", "oilfield", "electrical"],
        conclusion_template="Implement maintenance program to ensure reliability of electrical equipment in oilfield facilities.",
        reasoning_framework=(
            "Electrical equipment maintenance is implemented to ensure reliability and prevent failures. "
            "Program includes periodic inspection, testing, and preventive maintenance. "
            "Reliability analysis informs maintenance intervals and spare parts inventory. "
            "Documentation and compliance with manufacturer recommendations and NEC are required."
        ),
        key_factors=[
            "Inspection",
            "Testing",
            "Preventive maintenance",
            "Reliability analysis",
            "Documentation"
        ],
        primary_authority=["NEC", "IEEE Std 493"],
        burden_holder="Maintenance Engineer",
        adversary_position="Improper maintenance risks failures.",
        counter_arguments=[
            "Preventive maintenance improves reliability.",
            "Documentation supports compliance."
        ],
        resolution_strategy="Implement program per manufacturer and NEC; document and review maintenance.",
        entity_scope="Oilfield Facilities",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 493"
    ),
    DoctrineBlock(
        topic="Short-Circuit Analysis in Oilfield Power Distribution",
        keywords=["short-circuit analysis", "oilfield", "power distribution", "fault current"],
        conclusion_template="Perform short-circuit analysis to determine fault current and inform equipment selection.",
        reasoning_framework=(
            "Short-circuit analysis is performed to determine fault current levels and inform equipment selection. "
            "Study involves evaluating system configuration, transformer impedance, and protective device ratings. "
            "Results are used to select switchgear, breakers, and protective relays. "
            "Periodic review and adjustment are required. "
            "Compliance with IEEE and NEC is mandatory."
        ),
        key_factors=[
            "System configuration",
            "Transformer impedance",
            "Protective device ratings",
            "Review",
            "Adjustment"
        ],
        primary_authority=["IEEE Std 399", "NEC"],
        burden_holder="Protection Engineer",
        adversary_position="Improper analysis risks equipment damage.",
        counter_arguments=[
            "Periodic review ensures reliability.",
            "Proper selection prevents failures."
        ],
        resolution_strategy="Perform analysis per IEEE and NEC; review and adjust periodically.",
        entity_scope="Oilfield Power Distribution",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 399"
    ),
    DoctrineBlock(
        topic="Load Flow Analysis in Oilfield Power Distribution",
        keywords=["load flow analysis", "oilfield", "power distribution", "voltage drop"],
        conclusion_template="Perform load flow analysis to evaluate voltage drop and optimize system configuration.",
        reasoning_framework=(
            "Load flow analysis is performed to evaluate voltage drop and optimize system configuration. "
            "Study involves modeling system components, load profile, and operating scenarios. "
            "Results inform transformer and cable sizing, and identify voltage regulation needs. "
            "Periodic review and adjustment are required. "
            "Compliance with IEEE and NEC is mandatory."
        ),
        key_factors=[
            "System modeling",
            "Load profile",
            "Operating scenarios",
            "Voltage regulation",
            "Review"
        ],
        primary_authority=["IEEE Std 399", "NEC"],
        burden_holder="Design Engineer",
        adversary_position="Improper analysis risks voltage issues.",
        counter_arguments=[
            "Periodic review ensures reliability.",
            "Optimization improves efficiency."
        ],
        resolution_strategy="Perform analysis per IEEE and NEC; review and optimize system.",
        entity_scope="Oilfield Power Distribution",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 399"
    ),
    DoctrineBlock(
        topic="Electrical Safety Program Implementation in Oilfield Facilities",
        keywords=["electrical safety", "program", "implementation", "oilfield"],
        conclusion_template="Implement electrical safety program per OSHA and NFPA 70E for oilfield facilities.",
        reasoning_framework=(
            "Electrical safety program is implemented to prevent accidents and ensure compliance. "
            "Program includes training, PPE, hazard identification, and periodic review. "
            "Documentation and compliance with OSHA and NFPA 70E are mandatory."
        ),
        key_factors=[
            "Training",
            "PPE",
            "Hazard identification",
            "Documentation",
            "Review"
        ],
        primary_authority=["OSHA", "NFPA 70E"],
        burden_holder="Safety Engineer",
        adversary_position="Improper implementation risks injury.",
        counter_arguments=[
            "Periodic review ensures safety.",
            "Documentation supports compliance."
        ],
        resolution_strategy="Implement program per OSHA and NFPA 70E; document and review periodically.",
        entity_scope="Oilfield Facilities",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 70E"
    ),
    DoctrineBlock(
        topic="Electrical Commissioning and Acceptance Testing in Oilfield Projects",
        keywords=["commissioning", "acceptance testing", "oilfield", "electrical"],
        conclusion_template="Perform commissioning and acceptance testing per IEEE and NEC for oilfield projects.",
        reasoning_framework=(
            "Commissioning and acceptance testing are performed to validate electrical system performance. "
            "Testing includes insulation resistance, continuity, functional checks, and load tests. "
            "Documentation and compliance with IEEE and NEC are mandatory."
        ),
        key_factors=[
            "Insulation resistance",
            "Continuity",
            "Functional checks",
            "Load tests",
            "Documentation"
        ],
        primary_authority=["IEEE Std 43", "NEC"],
        burden_holder="Commissioning Engineer",
        adversary_position="Improper testing risks failures.",
        counter_arguments=[
            "Proper testing ensures reliability.",
            "Documentation supports compliance."
        ],
        resolution_strategy="Perform testing per IEEE and NEC; document and review results.",
        entity_scope="Oilfield Projects",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 43"
    ),
    DoctrineBlock(
        topic="Electrical System Expansion and Upgrade Planning in Oilfield Facilities",
        keywords=["system expansion", "upgrade planning", "oilfield", "electrical"],
        conclusion_template="Plan electrical system expansion and upgrade based on load growth and site requirements.",
        reasoning_framework=(
            "Electrical system expansion and upgrade planning is performed based on load growth and site requirements. "
            "Study involves evaluating existing system capacity, anticipated growth, and process changes. "
            "Results inform transformer, generator, and cable sizing. "
            "Documentation and compliance with IEEE and NEC are mandatory."
        ),
        key_factors=[
            "Existing capacity",
            "Anticipated growth",
            "Process changes",
            "Sizing",
            "Documentation"
        ],
        primary_authority=["IEEE Std 141", "NEC"],
        burden_holder="Planning Engineer",
        adversary_position="Improper planning risks under-sizing or over-sizing.",
        counter_arguments=[
            "Periodic review ensures accuracy.",
            "Documentation supports planning."
        ],
        resolution_strategy="Evaluate capacity and growth; plan expansion per IEEE and NEC; document results.",
        entity_scope="Oilfield Facilities",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 141"
    ),
    DoctrineBlock(
        topic="Electrical System Monitoring and SCADA Integration in Oilfield Facilities",
        keywords=["system monitoring", "SCADA", "integration", "oilfield", "electrical"],
        conclusion_template="Integrate electrical system monitoring with SCADA for oilfield facilities.",
        reasoning_framework=(
            "Electrical system monitoring is integrated with SCADA to provide real-time data and control. "
            "Integration involves selecting compatible devices, communication protocols, and software. "
            "Periodic review and maintenance are required. "
            "Compliance with IEEE and NEC is mandatory."
        ),
        key_factors=[
            "Device compatibility",
            "Communication protocols",
            "Software",
            "Review",
            "Maintenance"
        ],
        primary_authority=["IEEE Std 1379", "NEC"],
        burden_holder="Automation Engineer",
        adversary_position="Improper integration risks data loss.",
        counter_arguments=[
            "Periodic review ensures reliability.",
            "Maintenance supports performance."
        ],
        resolution_strategy="Select compatible devices; integrate per IEEE and NEC; review and maintain system.",
        entity_scope="Oilfield Facilities",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 1379"
    ),
    DoctrineBlock(
        topic="Electrical System Documentation and Record Keeping in Oilfield Facilities",
        keywords=["system documentation", "record keeping", "oilfield", "electrical"],
        conclusion_template="Maintain electrical system documentation and records per NEC and IEEE for oilfield facilities.",
        reasoning_framework=(
            "Electrical system documentation and record keeping are maintained to support operation, maintenance, and compliance. "
            "Records include one-line diagrams, test results, maintenance logs, and incident reports. "
            "Periodic review and update are required. "
            "Compliance with NEC and IEEE is mandatory."
        ),
        key_factors=[
            "One-line diagrams",
            "Test results",
            "Maintenance logs",
            "Incident reports",
            "Review"
        ],
        primary_authority=["NEC", "IEEE Std 141"],
        burden_holder="Documentation Engineer",
        adversary_position="Improper documentation risks compliance issues.",
        counter_arguments=[
            "Periodic review ensures accuracy.",
            "Documentation supports maintenance."
        ],
        resolution_strategy="Maintain records per NEC and IEEE; review and update periodically.",
        entity_scope="Oilfield Facilities",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 141"
    ),
    DoctrineBlock(
        topic="Electrical System Emergency Response Planning in Oilfield Facilities",
        keywords=["emergency response", "planning", "oilfield", "electrical"],
        conclusion_template="Develop electrical system emergency response plan per OSHA and NFPA 70E for oilfield facilities.",
        reasoning_framework=(
            "Emergency response planning is performed to address electrical system failures and incidents. "
            "Plan includes hazard identification, response procedures, communication protocols, and periodic drills. "
            "Documentation and compliance with OSHA and NFPA 70E are mandatory."
        ),
        key_factors=[
            "Hazard identification",
            "Response procedures",
            "Communication protocols",
            "Drills",
            "Documentation"
        ],
        primary_authority=["OSHA", "NFPA 70E"],
        burden_holder="Safety Engineer",
        adversary_position="Improper planning risks injury.",
        counter_arguments=[
            "Periodic drills improve response.",
            "Documentation supports compliance."
        ],
        resolution_strategy="Develop plan per OSHA and NFPA 70E; document and drill periodically.",
        entity_scope="Oilfield Facilities",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 70E"
    ),
    DoctrineBlock(
        topic="Electrical System Reliability Analysis and Improvement in Oilfield Facilities",
        keywords=["reliability analysis", "improvement", "oilfield", "electrical"],
        conclusion_template="Perform reliability analysis and implement improvement measures for oilfield electrical systems.",
        reasoning_framework=(
            "Reliability analysis is performed to identify failure modes and implement improvement measures. "
            "Analysis includes FMEA, reliability block diagrams, and historical data review. "
            "Improvement measures include preventive maintenance, redundancy, and equipment upgrades. "
            "Documentation and compliance with IEEE and NEC are mandatory."
        ),
        key_factors=[
            "FMEA",
            "Reliability block diagrams",
            "Historical data",
            "Improvement measures",
            "Documentation"
        ],
        primary_authority=["IEEE Std 493", "NEC"],
        burden_holder="Reliability Engineer",
        adversary_position="Improper analysis risks failures.",
        counter_arguments=[
            "Preventive maintenance improves reliability.",
            "Redundancy reduces risk."
        ],
        resolution_strategy="Perform analysis per IEEE and NEC; implement improvement measures; document results.",
        entity_scope="Oilfield Facilities",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 493"
    ),
    DoctrineBlock(
        topic="Electrical System Risk Assessment and Mitigation in Oilfield Facilities",
        keywords=["risk assessment", "mitigation", "oilfield", "electrical"],
        conclusion_template="Perform risk assessment and implement mitigation measures for oilfield electrical systems.",
        reasoning_framework=(
            "Risk assessment is performed to identify hazards and implement mitigation measures. "
            "Assessment includes hazard identification, probability and impact analysis, and mitigation planning. "
            "Documentation and compliance with OSHA and NFPA 70E are mandatory."
        ),
        key_factors=[
            "Hazard identification",
            "Probability and impact analysis",
            "Mitigation planning",
            "Documentation",
            "Compliance"
        ],
        primary_authority=["OSHA", "NFPA 70E"],
        burden_holder="Safety Engineer",
        adversary_position="Improper assessment risks injury.",
        counter_arguments=[
            "Mitigation reduces risk.",
            "Documentation supports compliance."
        ],
        resolution_strategy="Perform assessment per OSHA and NFPA 70E; implement mitigation; document results.",
        entity_scope="Oilfield Facilities",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 70E"
    ),
    DoctrineBlock(
        topic="Electrical System Energy Efficiency Optimization in Oilfield Facilities",
        keywords=["energy efficiency", "optimization", "oilfield", "electrical"],
        conclusion_template="Optimize electrical system energy efficiency for oilfield facilities using best practices.",
        reasoning_framework=(
            "Energy efficiency optimization is performed by applying best practices such as power factor correction, load management, and equipment upgrades. "
            "Periodic monitoring and analysis are required to identify improvement opportunities. "
            "Documentation and compliance with IEEE and NEC are mandatory."
        ),
        key_factors=[
            "Power factor correction",
            "Load management",
            "Equipment upgrades",
            "Monitoring",
            "Documentation"
        ],
        primary_authority=["IEEE Std 241", "NEC"],
        burden_holder="Energy Engineer",
        adversary_position="Improper optimization risks inefficiency.",
        counter_arguments=[
            "Periodic monitoring identifies opportunities.",
            "Upgrades improve efficiency."
        ],
        resolution_strategy="Apply best practices per IEEE and NEC; monitor and document results.",
        entity_scope="Oilfield Facilities",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 241"
    ),
    DoctrineBlock(
        topic="Electrical System Environmental Compliance in Oilfield Facilities",
        keywords=["environmental compliance", "oilfield", "electrical", "EPA"],
        conclusion_template="Ensure electrical system environmental compliance per EPA and NEC for oilfield facilities.",
        reasoning_framework=(
            "Environmental compliance is ensured by adhering to EPA and NEC requirements for electrical systems. "
            "Compliance includes proper disposal of hazardous materials, spill prevention, and documentation. "
            "Periodic review and audit are required."
        ),
        key_factors=[
            "Hazardous material disposal",
            "Spill prevention",
            "Documentation",
            "Review",
            "Audit"
        ],
        primary_authority=["EPA", "NEC"],
        burden_holder="Environmental Engineer",
        adversary_position="Improper compliance risks fines.",
        counter_arguments=[
            "Periodic review ensures compliance.",
            "Documentation supports audit."
        ],
        resolution_strategy="Adhere to EPA and NEC; review and audit periodically; document results.",
        entity_scope="Oilfield Facilities",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Regulations"
    ),
    DoctrineBlock(
        topic="Electrical System Cybersecurity in Oilfield Facilities",
        keywords=["cybersecurity", "oilfield", "electrical", "SCADA"],
        conclusion_template="Implement cybersecurity measures for electrical systems and SCADA in oilfield facilities.",
        reasoning_framework=(
            "Cybersecurity measures are implemented to protect electrical systems and SCADA from cyber threats. "
            "Measures include network segmentation, access control, periodic vulnerability assessment, and incident response planning. "
            "Documentation and compliance with NIST and industry standards are required."
        ),
        key_factors=[
            "Network segmentation",
            "Access control",
            "Vulnerability assessment",
            "Incident response",
            "Documentation"
        ],
        primary_authority=["NIST", "NEC"],
        burden_holder="Cybersecurity Engineer",
        adversary_position="Improper measures risk data loss.",
        counter_arguments=[
            "Periodic assessment improves security.",
            "Incident response reduces impact."
        ],
        resolution_strategy="Implement measures per NIST and NEC; assess and document periodically.",
        entity_scope="Oilfield Facilities",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NIST SP 800-82"
    ),
    DoctrineBlock(
        topic="Electrical System Life Cycle Cost Analysis in Oilfield Facilities",
        keywords=["life cycle cost", "analysis", "oilfield", "electrical"],
        conclusion_template="Perform life cycle cost analysis for electrical systems in oilfield facilities.",
        reasoning_framework=(
            "Life cycle cost analysis is performed to evaluate total cost of ownership for electrical systems. "
            "Analysis includes initial cost, maintenance, energy consumption, and disposal. "
            "Results inform equipment selection and upgrade planning. "
            "Documentation and compliance with IEEE and NEC are mandatory."
        ),
        key_factors=[
            "Initial cost",
            "Maintenance",
            "Energy consumption",
            "Disposal",
            "Documentation"
        ],
        primary_authority=["IEEE Std 493", "NEC"],
        burden_holder="Planning Engineer",
        adversary_position="Improper analysis risks excessive cost.",
        counter_arguments=[
            "Periodic review ensures accuracy.",
            "Documentation supports planning."
        ],
        resolution_strategy="Perform analysis per IEEE and NEC; document and review results.",
        entity_scope="Oilfield Facilities",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 493"
    ),
    DoctrineBlock(
        topic="Electrical System Spare Parts Management in Oilfield Facilities",
        keywords=["spare parts", "management", "oilfield", "electrical"],
        conclusion_template="Implement spare parts management program for electrical systems in oilfield facilities.",
        reasoning_framework=(
            "Spare parts management is implemented to ensure availability and reliability of electrical systems. "
            "Program includes inventory tracking, periodic review, and criticality analysis. "
            "Documentation and compliance with manufacturer recommendations and NEC are required."
        ),
        key_factors=[
            "Inventory tracking",
            "Periodic review",
            "Criticality analysis",
            "Documentation",
            "Compliance"
        ],
        primary_authority=["NEC", "IEEE Std 493"],
        burden_holder="Maintenance Engineer",
        adversary_position="Improper management risks downtime.",
        counter_arguments=[
            "Criticality analysis prioritizes inventory.",
            "Periodic review ensures availability."
        ],
        resolution_strategy="Implement program per manufacturer and NEC; review and document inventory.",
        entity_scope="Oilfield Facilities",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 493"
    ),
    DoctrineBlock(
        topic="Electrical System Training and Competency Development in Oilfield Facilities",
        keywords=["training", "competency", "development", "oilfield", "electrical"],
        conclusion_template="Implement training and competency development program for electrical personnel in oilfield facilities.",
        reasoning_framework=(
            "Training and competency development are implemented to ensure safety and reliability. "
            "Program includes periodic training, certification, and skills assessment. "
            "Documentation and compliance with OSHA and NFPA 70E are mandatory."
        ),
        key_factors=[
            "Periodic training",
            "Certification",
            "Skills assessment",
            "Documentation",
            "Compliance"
        ],
        primary_authority=["OSHA", "NFPA 70E"],
        burden_holder="Training Coordinator",
        adversary_position="Improper training risks safety.",
        counter_arguments=[
            "Periodic training improves competency.",
            "Certification ensures compliance."
        ],
        resolution_strategy="Implement program per OSHA and NFPA 70E; document and review training.",
        entity_scope="Oilfield Facilities",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 70E"
    ),
    DoctrineBlock(
        topic="Electrical System Incident Investigation and Root Cause Analysis in Oilfield Facilities",
        keywords=["incident investigation", "root cause analysis", "oilfield", "electrical"],
        conclusion_template="Perform incident investigation and root cause analysis for electrical failures in oilfield facilities.",
        reasoning_framework=(
            "Incident investigation and root cause analysis are performed to identify causes of electrical failures. "
            "Analysis includes data collection, interviews, and failure mode analysis. "
            "Results inform corrective actions and preventive measures. "
            "Documentation and compliance with OSHA and NFPA 70E are mandatory."
        ),
        key_factors=[
            "Data collection",
            "Interviews",
            "Failure mode analysis",
            "Corrective actions",
            "Documentation"
        ],
        primary_authority=["OSHA", "NFPA 70E"],
        burden_holder="Safety Engineer",
        adversary_position="Improper analysis risks recurrence.",
        counter_arguments=[
            "Corrective actions prevent recurrence.",
            "Documentation supports compliance."
        ],
        resolution_strategy="Perform analysis per OSHA and NFPA 70E; implement corrective actions; document results.",
        entity_scope="Oilfield Facilities",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 70E"
    ),
    DoctrineBlock(
        topic="Electrical System Change Management in Oilfield Facilities",
        keywords=["change management", "oilfield", "electrical", "system"],
        conclusion_template="Implement change management program for electrical system modifications in oilfield facilities.",
        reasoning_framework=(
            "Change management is implemented to control modifications to electrical systems. "
            "Program includes change request, impact assessment, approval, and documentation. "
            "Compliance with NEC and IEEE is mandatory."
        ),
        key_factors=[
            "Change request",
            "Impact assessment",
            "Approval",
            "Documentation",
            "Compliance"
        ],
        primary_authority=["NEC", "IEEE Std 141"],
        burden_holder="Change Manager",
        adversary_position="Improper management risks failures.",
        counter_arguments=[
            "Impact assessment prevents issues.",
            "Documentation supports compliance."
        ],
        resolution_strategy="Implement program per NEC and IEEE; document and review changes.",
        entity_scope="Oilfield Facilities",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 141"
    ),
    DoctrineBlock(
        topic="Electrical System Sustainability and Green Practices in Oilfield Facilities",
        keywords=["sustainability", "green practices", "oilfield", "electrical"],
        conclusion_template="Implement sustainability and green practices for electrical systems in oilfield facilities.",
        reasoning_framework=(
            "Sustainability and green practices are implemented to reduce environmental impact. "
            "Measures include energy efficiency, renewable integration, and waste reduction. "
            "Periodic review and documentation are required. "
            "Compliance with EPA and NEC is mandatory."
        ),
        key_factors=[
            "Energy efficiency",
            "Renewable integration",
            "Waste reduction",
            "Review",
            "Documentation"
        ],
        primary_authority=["EPA", "NEC"],
        burden_holder="Sustainability Engineer",
        adversary_position="Improper practices risk environmental impact.",
        counter_arguments=[
            "Periodic review improves sustainability.",
            "Documentation supports compliance."
        ],
        resolution_strategy="Implement practices per EPA and NEC; review and document results.",
        entity_scope="Oilfield Facilities",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Regulations"
    ),
    DoctrineBlock(
        topic="Electrical System Vendor Management in Oilfield Facilities",
        keywords=["vendor management", "oilfield", "electrical", "system"],
        conclusion_template="Implement vendor management program for electrical system procurement in oilfield facilities.",
        reasoning_framework=(
            "Vendor management is implemented to ensure quality and reliability of electrical system procurement. "
            "Program includes vendor qualification, performance review, and documentation. "
            "Compliance with NEC and IEEE is mandatory."
        ),
        key_factors=[
            "Vendor qualification",
            "Performance review",
            "Documentation",
            "Compliance",
            "Procurement"
        ],
        primary_authority=["NEC", "IEEE Std 141"],
        burden_holder="Procurement Engineer",
        adversary_position="Improper management risks quality.",
        counter_arguments=[
            "Qualification ensures reliability.",
            "Performance review supports compliance."
        ],
        resolution_strategy="Implement program per NEC and IEEE; review and document vendor performance.",
        entity_scope="Oilfield Facilities",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE Std 141"
    ),
    DoctrineBlock(
        topic="Electrical System Project Management in Oilfield Facilities",
        keywords=["project management", "oilfield", "electrical", "system"],
        conclusion_template="Implement project management program for electrical system projects in oilfield facilities.",
        reasoning_framework=(
            "Project management is implemented to ensure successful completion of electrical system projects. "
            "Program includes planning, scheduling, resource allocation, and documentation. "
            "Compliance with PMI and NEC is mandatory."
        ),
        key_factors=[
            "Planning",
            "Scheduling",
            "Resource allocation",
            "Documentation",
            "Compliance"
        ],
        primary_authority=["PMI", "NEC"],
        burden_holder="Project Manager",
        adversary_position="Improper management risks delays.",
        counter_arguments=[
            "Planning ensures success.",
            "Documentation supports compliance."
        ],
        resolution_strategy="Implement program per PMI and NEC; document and review project progress.",
        entity_scope="Oilfield Facilities",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PMI PMBOK"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    keyword_lower = keyword.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in k.lower() for k in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]