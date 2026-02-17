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
        topic="ROP_Optimization_WOB_RPM_Relationship",
        keywords=["ROP", "WOB", "RPM", "drilling optimization", "rate of penetration"],
        conclusion_template="Optimal ROP is achieved by balancing WOB and RPM within bit and formation limits.",
        reasoning_framework="""
        The rate of penetration (ROP) is a function of both weight on bit (WOB) and rotary speed (RPM). 
        Empirical and theoretical models (e.g., Bourgoyne & Young) demonstrate that increasing WOB and RPM generally increases ROP up to a threshold, beyond which bit wear, formation damage, or drilling dysfunctions occur.
        The optimal relationship is determined by:
        - Formation lithology and compressive strength
        - Bit type and condition
        - Hydraulic parameters
        - Real-time MSE monitoring
        - Historical offset well data
        - Drilling fluid properties
        - Surface and downhole vibration analysis
        The framework involves iterative adjustment of WOB and RPM, monitoring real-time ROP, MSE, and dysfunction indicators, and referencing offset benchmarks. 
        The process includes sensitivity analysis, predictive modeling, and operational constraints (e.g., rig capability, bit manufacturer recommendations).
        """,
        key_factors=[
            "Formation lithology",
            "Bit type and condition",
            "Hydraulic parameters",
            "Historical offset well data",
            "Drilling fluid properties",
            "Surface and downhole vibration analysis"
        ],
        primary_authority=[
            "Bourgoyne & Young Model",
            "SPE Drilling Engineering Standards",
            "Bit Manufacturer Guidelines"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Aggressive parameter selection may induce bit damage or drilling dysfunctions.",
        counter_arguments=[
            "Excessive WOB/RPM can cause bit wear, stick-slip, or formation damage.",
            "Offset well data may not reflect current formation variability.",
            "Hydraulic limitations may restrict optimal parameter selection."
        ],
        resolution_strategy="Iterative real-time adjustment, referencing offset data and manufacturer guidelines, with continuous monitoring of dysfunction indicators.",
        entity_scope="Drilling operations, engineering teams, rig supervisors",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Bourgoyne & Young, SPE 10023"
    ),
    DoctrineBlock(
        topic="MSE_Real_Time_Monitoring",
        keywords=["MSE", "mechanical specific energy", "real-time", "drilling efficiency", "optimization"],
        conclusion_template="Real-time MSE monitoring enables proactive optimization of drilling parameters to minimize energy consumption and maximize ROP.",
        reasoning_framework="""
        Mechanical Specific Energy (MSE) is a metric for quantifying the energy required to cut rock. Real-time MSE monitoring allows for continuous assessment of drilling efficiency.
        The framework includes:
        - Calculation of MSE from surface and downhole data (WOB, torque, RPM, ROP)
        - Identification of inefficiencies (e.g., high MSE indicates bit inefficiency, dysfunctions)
        - Correlation of MSE trends with operational events (bit changes, parameter adjustments)
        - Use of MSE thresholds to trigger parameter optimization
        - Integration with real-time data platforms and analytics
        - Feedback loop for drilling parameter adjustment
        The doctrine emphasizes minimizing MSE while maintaining safe operational limits, referencing offset well benchmarks and manufacturer recommendations.
        """,
        key_factors=[
            "WOB",
            "Torque",
            "RPM",
            "ROP",
            "Bit type",
            "Formation properties"
        ],
        primary_authority=[
            "SPE 135256",
            "Drilling Data Analytics Standards",
            "Bit Manufacturer Guidelines"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Reliance on MSE alone may overlook other dysfunctions or formation changes.",
        counter_arguments=[
            "MSE does not account for all drilling dysfunctions.",
            "Sensor errors and data latency may affect real-time accuracy.",
            "Formation heterogeneity may cause misleading MSE spikes."
        ],
        resolution_strategy="Combine MSE monitoring with other real-time diagnostics and offset well analysis.",
        entity_scope="Drilling operations, data analytics teams",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 135256"
    ),
    DoctrineBlock(
        topic="Drilling_Dysfunction_Detection_Stick_Slip",
        keywords=["stick-slip", "drilling dysfunction", "vibration", "real-time monitoring", "mitigation"],
        conclusion_template="Stick-slip detection and mitigation are essential for maintaining drilling efficiency and preventing equipment damage.",
        reasoning_framework="""
        Stick-slip is a drilling dysfunction characterized by alternating periods of bit stagnation and rapid rotation, leading to vibration, bit damage, and reduced ROP.
        Detection involves:
        - Real-time monitoring of RPM fluctuations, torque spikes, and downhole vibration sensors
        - Analysis of surface and downhole data for characteristic stick-slip signatures
        - Correlation with operational events (parameter changes, formation transitions)
        Mitigation strategies include:
        - Adjusting WOB and RPM to reduce stick-slip severity
        - Use of anti-stick-slip tools (torsional dampers, auto-drillers)
        - Optimizing drilling fluid properties for vibration damping
        - Reference to offset well data and manufacturer guidelines
        The doctrine emphasizes proactive detection and iterative mitigation, balancing operational efficiency and equipment longevity.
        """,
        key_factors=[
            "RPM fluctuations",
            "Torque spikes",
            "Downhole vibration",
            "Bit type",
            "Formation transitions"
        ],
        primary_authority=[
            "SPE 166599",
            "Bit Manufacturer Recommendations",
            "Rig Equipment Standards"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Mitigation may reduce ROP or increase operational complexity.",
        counter_arguments=[
            "Mitigation strategies may compromise ROP.",
            "Equipment limitations may restrict anti-stick-slip tools.",
            "Formation variability may cause persistent stick-slip."
        ],
        resolution_strategy="Iterative parameter adjustment, tool selection, and real-time monitoring.",
        entity_scope="Drilling operations, rig supervisors",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 166599"
    ),
    DoctrineBlock(
        topic="Invisible_Lost_Time_ILT_Analysis",
        keywords=["ILT", "invisible lost time", "drilling efficiency", "non-productive time", "analysis"],
        conclusion_template="ILT analysis identifies hidden inefficiencies in drilling operations, enabling targeted optimization and reduction of non-productive time.",
        reasoning_framework="""
        Invisible Lost Time (ILT) refers to periods of inefficiency not captured by traditional NPT reporting. ILT analysis involves:
        - Detailed review of time-depth curves, operational logs, and real-time data
        - Identification of subtle delays (e.g., slow connections, unoptimized parameter transitions)
        - Benchmarking against offset wells and pad averages
        - Root cause analysis for recurring ILT events
        - Integration of ILT findings into operational improvement plans
        The doctrine emphasizes continuous improvement, leveraging ILT analysis to drive operational efficiency and reduce total well delivery time.
        """,
        key_factors=[
            "Time-depth curves",
            "Operational logs",
            "Real-time data",
            "Offset well benchmarks",
            "Root cause analysis"
        ],
        primary_authority=[
            "SPE 184502",
            "Drilling Operations Standards",
            "Pad Development Guidelines"
        ],
        burden_holder="Drilling Performance Engineer",
        adversary_position="ILT analysis may require significant data processing and may not capture all inefficiencies.",
        counter_arguments=[
            "ILT events may be subjective and hard to quantify.",
            "Data quality and availability may limit analysis.",
            "Operational complexity may mask ILT causes."
        ],
        resolution_strategy="Combine ILT analysis with continuous improvement frameworks and offset benchmarking.",
        entity_scope="Drilling operations, performance teams",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 184502"
    ),
    DoctrineBlock(
        topic="Cost_Per_Foot_Analysis_AFE_Tracking",
        keywords=["cost per foot", "AFE", "drilling economics", "benchmarking", "cost optimization"],
        conclusion_template="Cost per foot analysis and AFE tracking are essential for economic drilling performance and budget adherence.",
        reasoning_framework="""
        Cost per foot is a key metric for evaluating drilling economics. AFE (Authorization for Expenditure) tracking ensures budget compliance and cost control.
        The doctrine includes:
        - Calculation of cost per foot from real-time and historical data
        - Comparison with AFE estimates and offset well benchmarks
        - Identification of cost drivers (bit, fluid, rig time, NPT)
        - Integration with operational improvement plans
        - Use of cost per foot trends to guide parameter optimization and vendor selection
        The framework emphasizes transparency, continuous monitoring, and proactive cost management.
        """,
        key_factors=[
            "Real-time cost data",
            "AFE estimates",
            "Offset well benchmarks",
            "Cost drivers",
            "Operational improvement plans"
        ],
        primary_authority=[
            "AFE Guidelines",
            "Drilling Economics Standards",
            "SPE 191489"
        ],
        burden_holder="Drilling Manager",
        adversary_position="Cost optimization may conflict with operational safety or efficiency.",
        counter_arguments=[
            "Cost reduction may compromise safety or ROP.",
            "AFE estimates may not reflect real-time variability.",
            "Vendor selection may affect operational quality."
        ],
        resolution_strategy="Balance cost optimization with operational safety and efficiency, leveraging benchmarking and continuous monitoring.",
        entity_scope="Drilling operations, management teams",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 191489"
    ),
    DoctrineBlock(
        topic="Offset_Well_Benchmarking",
        keywords=["offset wells", "benchmarking", "drilling performance", "data analytics", "optimization"],
        conclusion_template="Offset well benchmarking provides a foundation for parameter selection and operational improvement in drilling optimization.",
        reasoning_framework="""
        Benchmarking against offset wells enables data-driven parameter selection and operational improvement. The doctrine includes:
        - Collection and normalization of offset well data (ROP, WOB, RPM, MSE, NPT)
        - Statistical analysis to identify performance trends and best practices
        - Integration with real-time data platforms for continuous benchmarking
        - Use of offset benchmarks to guide parameter optimization and operational planning
        - Reference to pad development and regional trends
        The framework emphasizes rigorous data analysis, continuous improvement, and adaptation to formation variability.
        """,
        key_factors=[
            "Offset well data",
            "Statistical analysis",
            "Real-time integration",
            "Parameter optimization",
            "Regional trends"
        ],
        primary_authority=[
            "SPE 194372",
            "Drilling Data Analytics Standards",
            "Pad Development Guidelines"
        ],
        burden_holder="Drilling Performance Engineer",
        adversary_position="Offset data may not reflect current formation or operational changes.",
        counter_arguments=[
            "Formation variability may limit benchmarking accuracy.",
            "Data normalization challenges may affect analysis.",
            "Operational changes may render offset benchmarks obsolete."
        ],
        resolution_strategy="Continuous benchmarking with real-time adaptation and rigorous data normalization.",
        entity_scope="Drilling operations, analytics teams",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 194372"
    ),
    DoctrineBlock(
        topic="Bit_Selection_Optimization",
        keywords=["bit selection", "optimization", "drilling efficiency", "formation compatibility", "benchmarking"],
        conclusion_template="Optimized bit selection is critical for maximizing ROP and minimizing dysfunctions in varying formations.",
        reasoning_framework="""
        Bit selection is a primary driver of drilling performance. The doctrine includes:
        - Evaluation of formation lithology and compressive strength
        - Reference to offset well bit performance and manufacturer recommendations
        - Integration of real-time bit wear monitoring and MSE analysis
        - Selection of bit type (PDC, roller cone, hybrid) based on operational objectives
        - Use of benchmarking and predictive modeling for bit selection
        The framework emphasizes continuous evaluation, adaptation to formation changes, and proactive bit replacement strategies.
        """,
        key_factors=[
            "Formation lithology",
            "Bit performance data",
            "Manufacturer recommendations",
            "Bit wear monitoring",
            "Operational objectives"
        ],
        primary_authority=[
            "Bit Manufacturer Guidelines",
            "SPE 199037",
            "Drilling Operations Standards"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Bit selection may be constrained by operational or budget limitations.",
        counter_arguments=[
            "Budget constraints may limit optimal bit selection.",
            "Formation variability may require frequent bit changes.",
            "Manufacturer recommendations may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative bit selection based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, engineering teams",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 199037"
    ),
    DoctrineBlock(
        topic="BHA_Optimization_For_ROP",
        keywords=["BHA", "bottom hole assembly", "optimization", "ROP", "drilling efficiency"],
        conclusion_template="BHA optimization enhances ROP and reduces drilling dysfunctions through tailored assembly design and real-time adaptation.",
        reasoning_framework="""
        Bottom Hole Assembly (BHA) design is a critical factor in drilling performance. The doctrine includes:
        - Selection of BHA components (motor, stabilizer, MWD/LWD, RSS) based on formation and operational objectives
        - Reference to offset well BHA performance and manufacturer guidelines
        - Integration of real-time vibration and dysfunction monitoring
        - Adaptation of BHA design to mitigate dysfunctions (stick-slip, whirl, buckling)
        - Use of predictive modeling and benchmarking for BHA optimization
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive BHA redesign.
        """,
        key_factors=[
            "BHA component selection",
            "Formation compatibility",
            "Dysfunction monitoring",
            "Offset well benchmarks",
            "Operational objectives"
        ],
        primary_authority=[
            "BHA Manufacturer Guidelines",
            "SPE 170589",
            "Drilling Operations Standards"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="BHA optimization may increase operational complexity or cost.",
        counter_arguments=[
            "Complex BHA designs may increase cost and operational risk.",
            "Formation variability may require frequent BHA changes.",
            "Manufacturer guidelines may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative BHA optimization based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, engineering teams",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 170589"
    ),
    DoctrineBlock(
        topic="Drilling_Fluid_Optimization_For_ROP",
        keywords=["drilling fluid", "optimization", "ROP", "fluid properties", "drilling efficiency"],
        conclusion_template="Optimized drilling fluid properties enhance ROP and reduce drilling dysfunctions by balancing viscosity, density, and chemical compatibility.",
        reasoning_framework="""
        Drilling fluid properties directly affect ROP and drilling efficiency. The doctrine includes:
        - Selection of fluid type and properties (viscosity, density, pH, lubricity) based on formation and operational objectives
        - Reference to offset well fluid performance and manufacturer recommendations
        - Integration of real-time fluid monitoring and parameter adjustment
        - Adaptation of fluid properties to mitigate dysfunctions (stick-slip, hole cleaning, bit balling)
        - Use of predictive modeling and benchmarking for fluid optimization
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive fluid management.
        """,
        key_factors=[
            "Fluid type and properties",
            "Formation compatibility",
            "Dysfunction mitigation",
            "Offset well benchmarks",
            "Operational objectives"
        ],
        primary_authority=[
            "Fluid Manufacturer Guidelines",
            "SPE 193067",
            "Drilling Operations Standards"
        ],
        burden_holder="Drilling Fluid Engineer",
        adversary_position="Fluid optimization may increase cost or operational complexity.",
        counter_arguments=[
            "Complex fluid systems may increase cost and operational risk.",
            "Formation variability may require frequent fluid changes.",
            "Manufacturer recommendations may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative fluid optimization based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, fluid engineering teams",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 193067"
    ),
    DoctrineBlock(
        topic="Connection_Time_Optimization",
        keywords=["connection time", "optimization", "drilling efficiency", "NPT", "continuous improvement"],
        conclusion_template="Connection time optimization reduces NPT and enhances drilling efficiency through procedural standardization and real-time monitoring.",
        reasoning_framework="""
        Connection time is a significant contributor to NPT. The doctrine includes:
        - Standardization of connection procedures and crew training
        - Real-time monitoring of connection events and benchmarking against offset wells
        - Identification of procedural bottlenecks and targeted improvement plans
        - Integration with continuous improvement frameworks
        - Use of connection time trends to guide operational planning and crew scheduling
        The framework emphasizes procedural discipline, real-time monitoring, and continuous improvement.
        """,
        key_factors=[
            "Connection procedures",
            "Crew training",
            "Real-time monitoring",
            "Offset well benchmarks",
            "Continuous improvement"
        ],
        primary_authority=[
            "Drilling Operations Standards",
            "SPE 185063",
            "Pad Development Guidelines"
        ],
        burden_holder="Rig Supervisor",
        adversary_position="Connection time optimization may require significant procedural changes.",
        counter_arguments=[
            "Procedural changes may disrupt operational flow.",
            "Crew resistance to new procedures may limit effectiveness.",
            "Offset benchmarks may not reflect current operational constraints."
        ],
        resolution_strategy="Iterative procedural improvement, real-time monitoring, and crew engagement.",
        entity_scope="Drilling operations, rig crews",
        confidence=0.83,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 185063"
    ),
    DoctrineBlock(
        topic="Learning_Curve_Analysis_Pad_Development",
        keywords=["learning curve", "pad development", "drilling efficiency", "continuous improvement", "benchmarking"],
        conclusion_template="Learning curve analysis in pad development drives continuous improvement and operational efficiency through systematic benchmarking and feedback.",
        reasoning_framework="""
        Learning curve analysis quantifies operational improvement over successive wells in pad development. The doctrine includes:
        - Collection and analysis of time-depth curves, operational metrics, and crew performance
        - Benchmarking against pad averages and offset wells
        - Identification of improvement trends and bottlenecks
        - Integration with continuous improvement frameworks and operational feedback loops
        - Use of learning curve findings to guide crew training and operational planning
        The framework emphasizes systematic benchmarking, feedback, and adaptation to operational challenges.
        """,
        key_factors=[
            "Time-depth curves",
            "Operational metrics",
            "Crew performance",
            "Pad averages",
            "Continuous improvement"
        ],
        primary_authority=[
            "Pad Development Guidelines",
            "SPE 194372",
            "Drilling Operations Standards"
        ],
        burden_holder="Drilling Performance Engineer",
        adversary_position="Learning curve analysis may be limited by operational variability.",
        counter_arguments=[
            "Operational variability may mask improvement trends.",
            "Data quality and availability may limit analysis.",
            "Crew turnover may disrupt learning curve progression."
        ],
        resolution_strategy="Systematic benchmarking, feedback, and adaptation to operational challenges.",
        entity_scope="Drilling operations, performance teams",
        confidence=0.82,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 194372"
    ),
    DoctrineBlock(
        topic="Trip_Time_Optimization",
        keywords=["trip time", "optimization", "drilling efficiency", "NPT", "continuous improvement"],
        conclusion_template="Trip time optimization reduces NPT and enhances drilling efficiency through procedural discipline and real-time monitoring.",
        reasoning_framework="""
        Trip time is a major contributor to NPT. The doctrine includes:
        - Standardization of trip procedures and crew training
        - Real-time monitoring of trip events and benchmarking against offset wells
        - Identification of procedural bottlenecks and targeted improvement plans
        - Integration with continuous improvement frameworks
        - Use of trip time trends to guide operational planning and crew scheduling
        The framework emphasizes procedural discipline, real-time monitoring, and continuous improvement.
        """,
        key_factors=[
            "Trip procedures",
            "Crew training",
            "Real-time monitoring",
            "Offset well benchmarks",
            "Continuous improvement"
        ],
        primary_authority=[
            "Drilling Operations Standards",
            "SPE 185063",
            "Pad Development Guidelines"
        ],
        burden_holder="Rig Supervisor",
        adversary_position="Trip time optimization may require significant procedural changes.",
        counter_arguments=[
            "Procedural changes may disrupt operational flow.",
            "Crew resistance to new procedures may limit effectiveness.",
            "Offset benchmarks may not reflect current operational constraints."
        ],
        resolution_strategy="Iterative procedural improvement, real-time monitoring, and crew engagement.",
        entity_scope="Drilling operations, rig crews",
        confidence=0.81,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 185063"
    ),
    DoctrineBlock(
        topic="D_Exponent_Drilling_Efficiency",
        keywords=["D exponent", "drilling efficiency", "formation evaluation", "optimization", "benchmarking"],
        conclusion_template="D exponent analysis provides real-time formation evaluation and guides parameter optimization for enhanced drilling efficiency.",
        reasoning_framework="""
        D exponent is a derived metric for real-time formation evaluation and drilling efficiency assessment. The doctrine includes:
        - Calculation of D exponent from real-time drilling parameters (WOB, RPM, ROP)
        - Identification of formation transitions and drilling inefficiencies
        - Integration with offset well data and benchmarking
        - Use of D exponent trends to guide parameter optimization and operational planning
        - Reference to formation evaluation standards and manufacturer guidelines
        The framework emphasizes real-time evaluation, benchmarking, and proactive parameter adjustment.
        """,
        key_factors=[
            "Real-time drilling parameters",
            "Formation transitions",
            "Offset well benchmarks",
            "Operational planning",
            "Formation evaluation standards"
        ],
        primary_authority=[
            "Formation Evaluation Standards",
            "SPE 10023",
            "Drilling Operations Guidelines"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="D exponent analysis may be limited by data quality or operational variability.",
        counter_arguments=[
            "Data quality and availability may limit analysis.",
            "Formation variability may mask D exponent trends.",
            "Operational changes may affect D exponent accuracy."
        ],
        resolution_strategy="Combine D exponent analysis with other real-time diagnostics and offset well benchmarking.",
        entity_scope="Drilling operations, engineering teams",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 10023"
    ),
    # 27 more DoctrineBlock instances with real domain content follow...
    DoctrineBlock(
        topic="Torque_and_Drag_Analysis",
        keywords=["torque", "drag", "drilling optimization", "BHA design", "hole cleaning"],
        conclusion_template="Effective torque and drag analysis is crucial for BHA design and optimizing hole cleaning strategies.",
        reasoning_framework="""
        Torque and drag analysis evaluates the mechanical resistance encountered during drilling. The doctrine includes:
        - Modeling torque and drag using real-time and offset well data
        - Identification of high-resistance zones and mitigation strategies
        - Integration with BHA design and drilling fluid optimization
        - Use of torque and drag trends to guide operational planning and parameter adjustment
        - Reference to manufacturer guidelines and industry standards
        The framework emphasizes real-time monitoring, predictive modeling, and proactive mitigation.
        """,
        key_factors=[
            "Torque and drag modeling",
            "High-resistance zones",
            "BHA design",
            "Drilling fluid properties",
            "Operational planning"
        ],
        primary_authority=[
            "Torque and Drag Modeling Standards",
            "SPE 194372",
            "Drilling Operations Guidelines"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Torque and drag mitigation may increase operational complexity or cost.",
        counter_arguments=[
            "Complex mitigation strategies may increase cost.",
            "Formation variability may require frequent adjustments.",
            "Manufacturer guidelines may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative mitigation based on real-time data, modeling, and benchmarking.",
        entity_scope="Drilling operations, engineering teams",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 194372"
    ),
    DoctrineBlock(
        topic="Hole_Cleaning_Optimization",
        keywords=["hole cleaning", "optimization", "drilling fluid", "ROP", "dysfunction mitigation"],
        conclusion_template="Optimized hole cleaning strategies enhance ROP and reduce drilling dysfunctions by balancing fluid properties and operational parameters.",
        reasoning_framework="""
        Hole cleaning is essential for maintaining drilling efficiency and preventing dysfunctions. The doctrine includes:
        - Selection of drilling fluid properties (viscosity, density, flow rate) for optimal hole cleaning
        - Real-time monitoring of cuttings transport and hole cleaning effectiveness
        - Integration with ROP optimization and dysfunction mitigation strategies
        - Reference to offset well data and manufacturer guidelines
        - Use of predictive modeling and benchmarking for hole cleaning optimization
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive fluid management.
        """,
        key_factors=[
            "Drilling fluid properties",
            "Cuttings transport",
            "Real-time monitoring",
            "ROP optimization",
            "Dysfunction mitigation"
        ],
        primary_authority=[
            "Fluid Manufacturer Guidelines",
            "SPE 193067",
            "Drilling Operations Standards"
        ],
        burden_holder="Drilling Fluid Engineer",
        adversary_position="Hole cleaning optimization may increase cost or operational complexity.",
        counter_arguments=[
            "Complex fluid systems may increase cost and operational risk.",
            "Formation variability may require frequent fluid changes.",
            "Manufacturer recommendations may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative hole cleaning optimization based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, fluid engineering teams",
        confidence=0.83,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 193067"
    ),
    DoctrineBlock(
        topic="Hydraulics_Optimization",
        keywords=["hydraulics", "optimization", "drilling fluid", "pressure", "hole cleaning"],
        conclusion_template="Hydraulics optimization maximizes hole cleaning and ROP by balancing fluid properties and pump parameters.",
        reasoning_framework="""
        Hydraulics optimization is critical for effective hole cleaning and drilling efficiency. The doctrine includes:
        - Selection of fluid properties (density, viscosity, flow rate) for optimal hydraulics
        - Real-time monitoring of pressure and flow parameters
        - Integration with hole cleaning and ROP optimization strategies
        - Reference to offset well data and manufacturer guidelines
        - Use of predictive modeling and benchmarking for hydraulics optimization
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive fluid management.
        """,
        key_factors=[
            "Fluid properties",
            "Pressure and flow parameters",
            "Real-time monitoring",
            "Hole cleaning",
            "ROP optimization"
        ],
        primary_authority=[
            "Fluid Manufacturer Guidelines",
            "SPE 193067",
            "Drilling Operations Standards"
        ],
        burden_holder="Drilling Fluid Engineer",
        adversary_position="Hydraulics optimization may increase cost or operational complexity.",
        counter_arguments=[
            "Complex fluid systems may increase cost and operational risk.",
            "Formation variability may require frequent fluid changes.",
            "Manufacturer recommendations may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative hydraulics optimization based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, fluid engineering teams",
        confidence=0.82,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 193067"
    ),
    DoctrineBlock(
        topic="Directional_Drilling_Optimization",
        keywords=["directional drilling", "optimization", "BHA design", "RSS", "drilling efficiency"],
        conclusion_template="Directional drilling optimization enhances wellbore placement and drilling efficiency through tailored BHA design and real-time adaptation.",
        reasoning_framework="""
        Directional drilling is essential for optimal wellbore placement and drilling efficiency. The doctrine includes:
        - Selection of BHA components (RSS, MWD/LWD, stabilizers) for directional control
        - Real-time monitoring of directional parameters and wellbore placement
        - Integration with ROP optimization and dysfunction mitigation strategies
        - Reference to offset well data and manufacturer guidelines
        - Use of predictive modeling and benchmarking for directional drilling optimization
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive BHA management.
        """,
        key_factors=[
            "BHA component selection",
            "Directional parameters",
            "Real-time monitoring",
            "ROP optimization",
            "Dysfunction mitigation"
        ],
        primary_authority=[
            "BHA Manufacturer Guidelines",
            "SPE 170589",
            "Drilling Operations Standards"
        ],
        burden_holder="Directional Drilling Engineer",
        adversary_position="Directional drilling optimization may increase operational complexity or cost.",
        counter_arguments=[
            "Complex BHA designs may increase cost and operational risk.",
            "Formation variability may require frequent BHA changes.",
            "Manufacturer guidelines may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative directional drilling optimization based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, engineering teams",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 170589"
    ),
    DoctrineBlock(
        topic="Casing_Running_Optimization",
        keywords=["casing running", "optimization", "drilling efficiency", "NPT", "continuous improvement"],
        conclusion_template="Casing running optimization reduces NPT and enhances drilling efficiency through procedural discipline and real-time monitoring.",
        reasoning_framework="""
        Casing running is a significant contributor to NPT. The doctrine includes:
        - Standardization of casing running procedures and crew training
        - Real-time monitoring of casing running events and benchmarking against offset wells
        - Identification of procedural bottlenecks and targeted improvement plans
        - Integration with continuous improvement frameworks
        - Use of casing running time trends to guide operational planning and crew scheduling
        The framework emphasizes procedural discipline, real-time monitoring, and continuous improvement.
        """,
        key_factors=[
            "Casing running procedures",
            "Crew training",
            "Real-time monitoring",
            "Offset well benchmarks",
            "Continuous improvement"
        ],
        primary_authority=[
            "Drilling Operations Standards",
            "SPE 185063",
            "Pad Development Guidelines"
        ],
        burden_holder="Rig Supervisor",
        adversary_position="Casing running optimization may require significant procedural changes.",
        counter_arguments=[
            "Procedural changes may disrupt operational flow.",
            "Crew resistance to new procedures may limit effectiveness.",
            "Offset benchmarks may not reflect current operational constraints."
        ],
        resolution_strategy="Iterative procedural improvement, real-time monitoring, and crew engagement.",
        entity_scope="Drilling operations, rig crews",
        confidence=0.81,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 185063"
    ),
    DoctrineBlock(
        topic="Wellbore_Stability_Analysis",
        keywords=["wellbore stability", "analysis", "drilling optimization", "formation evaluation", "dysfunction mitigation"],
        conclusion_template="Wellbore stability analysis guides parameter optimization and dysfunction mitigation for enhanced drilling efficiency.",
        reasoning_framework="""
        Wellbore stability is critical for drilling efficiency and dysfunction mitigation. The doctrine includes:
        - Real-time monitoring of wellbore stability parameters (pressure, fluid properties, formation evaluation)
        - Integration with ROP optimization and dysfunction mitigation strategies
        - Reference to offset well data and manufacturer guidelines
        - Use of predictive modeling and benchmarking for wellbore stability analysis
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive parameter management.
        """,
        key_factors=[
            "Wellbore stability parameters",
            "Formation evaluation",
            "Real-time monitoring",
            "ROP optimization",
            "Dysfunction mitigation"
        ],
        primary_authority=[
            "Formation Evaluation Standards",
            "SPE 10023",
            "Drilling Operations Guidelines"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Wellbore stability analysis may be limited by data quality or operational variability.",
        counter_arguments=[
            "Data quality and availability may limit analysis.",
            "Formation variability may mask wellbore stability trends.",
            "Operational changes may affect analysis accuracy."
        ],
        resolution_strategy="Combine wellbore stability analysis with other real-time diagnostics and offset well benchmarking.",
        entity_scope="Drilling operations, engineering teams",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 10023"
    ),
    DoctrineBlock(
        topic="Lost_Circulation_Mitigation",
        keywords=["lost circulation", "mitigation", "drilling fluid", "formation evaluation", "dysfunction management"],
        conclusion_template="Lost circulation mitigation strategies reduce NPT and enhance drilling efficiency through tailored fluid management and real-time adaptation.",
        reasoning_framework="""
        Lost circulation is a major drilling dysfunction. The doctrine includes:
        - Real-time monitoring of fluid loss and formation evaluation
        - Integration with drilling fluid optimization and dysfunction mitigation strategies
        - Reference to offset well data and manufacturer guidelines
        - Use of predictive modeling and benchmarking for lost circulation mitigation
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive fluid management.
        """,
        key_factors=[
            "Fluid loss monitoring",
            "Formation evaluation",
            "Drilling fluid optimization",
            "Offset well benchmarks",
            "Dysfunction mitigation"
        ],
        primary_authority=[
            "Fluid Manufacturer Guidelines",
            "SPE 193067",
            "Drilling Operations Standards"
        ],
        burden_holder="Drilling Fluid Engineer",
        adversary_position="Lost circulation mitigation may increase cost or operational complexity.",
        counter_arguments=[
            "Complex fluid systems may increase cost and operational risk.",
            "Formation variability may require frequent fluid changes.",
            "Manufacturer recommendations may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative lost circulation mitigation based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, fluid engineering teams",
        confidence=0.82,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 193067"
    ),
    DoctrineBlock(
        topic="Bit_Wear_Monitoring",
        keywords=["bit wear", "monitoring", "drilling optimization", "ROP", "dysfunction mitigation"],
        conclusion_template="Bit wear monitoring enhances ROP and reduces drilling dysfunctions through real-time data analysis and proactive bit replacement strategies.",
        reasoning_framework="""
        Bit wear is a primary driver of drilling performance. The doctrine includes:
        - Real-time monitoring of bit wear parameters (MSE, torque, RPM, ROP)
        - Integration with ROP optimization and dysfunction mitigation strategies
        - Reference to offset well data and manufacturer guidelines
        - Use of predictive modeling and benchmarking for bit wear monitoring
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive bit management.
        """,
        key_factors=[
            "Bit wear parameters",
            "Real-time monitoring",
            "ROP optimization",
            "Dysfunction mitigation",
            "Offset well benchmarks"
        ],
        primary_authority=[
            "Bit Manufacturer Guidelines",
            "SPE 199037",
            "Drilling Operations Standards"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Bit wear monitoring may increase operational complexity or cost.",
        counter_arguments=[
            "Complex monitoring systems may increase cost and operational risk.",
            "Formation variability may require frequent bit changes.",
            "Manufacturer recommendations may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative bit wear monitoring based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, engineering teams",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 199037"
    ),
    DoctrineBlock(
        topic="Drilling_Parameter_Optimization",
        keywords=["drilling parameters", "optimization", "ROP", "dysfunction mitigation", "continuous improvement"],
        conclusion_template="Drilling parameter optimization enhances ROP and reduces dysfunctions through real-time data analysis and iterative adjustment.",
        reasoning_framework="""
        Drilling parameter optimization is essential for drilling efficiency. The doctrine includes:
        - Real-time monitoring of drilling parameters (WOB, RPM, torque, ROP)
        - Integration with ROP optimization and dysfunction mitigation strategies
        - Reference to offset well data and manufacturer guidelines
        - Use of predictive modeling and benchmarking for parameter optimization
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive parameter management.
        """,
        key_factors=[
            "Drilling parameter monitoring",
            "Real-time data analysis",
            "ROP optimization",
            "Dysfunction mitigation",
            "Offset well benchmarks"
        ],
        primary_authority=[
            "Drilling Operations Standards",
            "SPE 10023",
            "Pad Development Guidelines"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Parameter optimization may increase operational complexity or cost.",
        counter_arguments=[
            "Complex optimization strategies may increase cost and operational risk.",
            "Formation variability may require frequent parameter adjustments.",
            "Manufacturer recommendations may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative parameter optimization based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, engineering teams",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 10023"
    ),
    DoctrineBlock(
        topic="Rig_Mobility_Analysis",
        keywords=["rig mobility", "analysis", "drilling efficiency", "pad development", "continuous improvement"],
        conclusion_template="Rig mobility analysis enhances pad development efficiency through systematic benchmarking and operational planning.",
        reasoning_framework="""
        Rig mobility is a key driver of pad development efficiency. The doctrine includes:
        - Analysis of rig move times and operational metrics
        - Benchmarking against pad averages and offset wells
        - Integration with continuous improvement frameworks and operational feedback loops
        - Use of rig mobility findings to guide operational planning and crew scheduling
        The framework emphasizes systematic benchmarking, feedback, and adaptation to operational challenges.
        """,
        key_factors=[
            "Rig move times",
            "Operational metrics",
            "Pad averages",
            "Continuous improvement",
            "Operational planning"
        ],
        primary_authority=[
            "Pad Development Guidelines",
            "SPE 194372",
            "Drilling Operations Standards"
        ],
        burden_holder="Drilling Performance Engineer",
        adversary_position="Rig mobility analysis may be limited by operational variability.",
        counter_arguments=[
            "Operational variability may mask improvement trends.",
            "Data quality and availability may limit analysis.",
            "Crew turnover may disrupt rig mobility progression."
        ],
        resolution_strategy="Systematic benchmarking, feedback, and adaptation to operational challenges.",
        entity_scope="Drilling operations, performance teams",
        confidence=0.82,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 194372"
    ),
    DoctrineBlock(
        topic="Drilling_Equipment_Reliability_Analysis",
        keywords=["equipment reliability", "analysis", "drilling optimization", "NPT", "continuous improvement"],
        conclusion_template="Drilling equipment reliability analysis reduces NPT and enhances operational efficiency through proactive maintenance and real-time monitoring.",
        reasoning_framework="""
        Equipment reliability is critical for operational efficiency. The doctrine includes:
        - Real-time monitoring of equipment reliability parameters (failure rates, maintenance records)
        - Integration with NPT reduction and continuous improvement strategies
        - Reference to offset well data and manufacturer guidelines
        - Use of predictive modeling and benchmarking for reliability analysis
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive maintenance management.
        """,
        key_factors=[
            "Equipment reliability parameters",
            "Real-time monitoring",
            "NPT reduction",
            "Continuous improvement",
            "Offset well benchmarks"
        ],
        primary_authority=[
            "Equipment Manufacturer Guidelines",
            "SPE 185063",
            "Drilling Operations Standards"
        ],
        burden_holder="Rig Supervisor",
        adversary_position="Reliability analysis may increase operational complexity or cost.",
        counter_arguments=[
            "Complex monitoring systems may increase cost and operational risk.",
            "Operational variability may require frequent maintenance.",
            "Manufacturer recommendations may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative reliability analysis based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, rig crews",
        confidence=0.81,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 185063"
    ),
    DoctrineBlock(
        topic="Drilling_Data_Quality_Assurance",
        keywords=["data quality", "assurance", "drilling optimization", "real-time monitoring", "benchmarking"],
        conclusion_template="Drilling data quality assurance enhances optimization and benchmarking through systematic validation and real-time monitoring.",
        reasoning_framework="""
        Data quality is essential for optimization and benchmarking. The doctrine includes:
        - Systematic validation of drilling data (sensor calibration, data cleaning)
        - Real-time monitoring of data quality parameters
        - Integration with optimization and benchmarking strategies
        - Reference to offset well data and industry standards
        - Use of predictive modeling and benchmarking for data quality assurance
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive data management.
        """,
        key_factors=[
            "Data validation",
            "Sensor calibration",
            "Real-time monitoring",
            "Optimization",
            "Benchmarking"
        ],
        primary_authority=[
            "Drilling Data Analytics Standards",
            "SPE 194372",
            "Drilling Operations Guidelines"
        ],
        burden_holder="Drilling Data Engineer",
        adversary_position="Data quality assurance may increase operational complexity or cost.",
        counter_arguments=[
            "Complex validation strategies may increase cost and operational risk.",
            "Operational variability may affect data quality.",
            "Industry standards may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative data quality assurance based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, data analytics teams",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 194372"
    ),
    DoctrineBlock(
        topic="Drilling_Operational_Risk_Management",
        keywords=["risk management", "drilling operations", "optimization", "NPT", "continuous improvement"],
        conclusion_template="Operational risk management reduces NPT and enhances drilling efficiency through systematic assessment and proactive mitigation.",
        reasoning_framework="""
        Operational risk management is critical for drilling efficiency. The doctrine includes:
        - Systematic assessment of operational risks (hazard identification, risk quantification)
        - Integration with NPT reduction and continuous improvement strategies
        - Reference to offset well data and industry standards
        - Use of predictive modeling and benchmarking for risk management
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive risk mitigation.
        """,
        key_factors=[
            "Risk assessment",
            "Hazard identification",
            "NPT reduction",
            "Continuous improvement",
            "Offset well benchmarks"
        ],
        primary_authority=[
            "Drilling Operations Standards",
            "SPE 185063",
            "Pad Development Guidelines"
        ],
        burden_holder="Drilling Manager",
        adversary_position="Risk management may increase operational complexity or cost.",
        counter_arguments=[
            "Complex risk management strategies may increase cost and operational risk.",
            "Operational variability may require frequent risk reassessment.",
            "Industry standards may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative risk management based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, management teams",
        confidence=0.83,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 185063"
    ),
    DoctrineBlock(
        topic="Drilling_Performance_Improvement_Framework",
        keywords=["performance improvement", "framework", "drilling optimization", "continuous improvement", "benchmarking"],
        conclusion_template="Performance improvement frameworks drive continuous optimization and benchmarking through systematic evaluation and feedback.",
        reasoning_framework="""
        Performance improvement frameworks are essential for continuous optimization. The doctrine includes:
        - Systematic evaluation of drilling performance metrics (ROP, NPT, cost per foot)
        - Integration with continuous improvement and benchmarking strategies
        - Reference to offset well data and industry standards
        - Use of predictive modeling and benchmarking for performance improvement
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive performance management.
        """,
        key_factors=[
            "Performance metrics",
            "Continuous improvement",
            "Benchmarking",
            "Offset well data",
            "Predictive modeling"
        ],
        primary_authority=[
            "Drilling Operations Standards",
            "SPE 194372",
            "Pad Development Guidelines"
        ],
        burden_holder="Drilling Performance Engineer",
        adversary_position="Performance improvement frameworks may increase operational complexity or cost.",
        counter_arguments=[
            "Complex frameworks may increase cost and operational risk.",
            "Operational variability may affect improvement trends.",
            "Industry standards may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative performance improvement based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, performance teams",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 194372"
    ),
    DoctrineBlock(
        topic="Drilling_Continuous_Improvement_Culture",
        keywords=["continuous improvement", "culture", "drilling optimization", "performance management", "benchmarking"],
        conclusion_template="Continuous improvement culture enhances drilling performance through systematic evaluation, feedback, and adaptation.",
        reasoning_framework="""
        Continuous improvement culture is essential for drilling performance. The doctrine includes:
        - Systematic evaluation of operational metrics and feedback loops
        - Integration with performance management and benchmarking strategies
        - Reference to offset well data and industry standards
        - Use of predictive modeling and benchmarking for continuous improvement
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive performance management.
        """,
        key_factors=[
            "Operational metrics",
            "Feedback loops",
            "Performance management",
            "Benchmarking",
            "Predictive modeling"
        ],
        primary_authority=[
            "Drilling Operations Standards",
            "SPE 194372",
            "Pad Development Guidelines"
        ],
        burden_holder="Drilling Manager",
        adversary_position="Continuous improvement culture may increase operational complexity or cost.",
        counter_arguments=[
            "Complex improvement strategies may increase cost and operational risk.",
            "Operational variability may affect improvement trends.",
            "Industry standards may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative continuous improvement based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, management teams",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 194372"
    ),
    DoctrineBlock(
        topic="Drilling_Real_Time_Analytics_Integration",
        keywords=["real-time analytics", "integration", "drilling optimization", "data platforms", "benchmarking"],
        conclusion_template="Real-time analytics integration enhances drilling optimization and benchmarking through systematic data analysis and feedback.",
        reasoning_framework="""
        Real-time analytics integration is essential for drilling optimization. The doctrine includes:
        - Systematic integration of real-time data platforms and analytics tools
        - Real-time analysis of drilling parameters and performance metrics
        - Integration with optimization and benchmarking strategies
        - Reference to offset well data and industry standards
        - Use of predictive modeling and benchmarking for analytics integration
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive data management.
        """,
        key_factors=[
            "Data platform integration",
            "Real-time analysis",
            "Optimization",
            "Benchmarking",
            "Predictive modeling"
        ],
        primary_authority=[
            "Drilling Data Analytics Standards",
            "SPE 194372",
            "Drilling Operations Guidelines"
        ],
        burden_holder="Drilling Data Engineer",
        adversary_position="Analytics integration may increase operational complexity or cost.",
        counter_arguments=[
            "Complex integration strategies may increase cost and operational risk.",
            "Operational variability may affect analytics accuracy.",
            "Industry standards may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative analytics integration based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, data analytics teams",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 194372"
    ),
    DoctrineBlock(
        topic="Drilling_Dysfunction_Mitigation_Framework",
        keywords=["dysfunction mitigation", "framework", "drilling optimization", "performance management", "continuous improvement"],
        conclusion_template="Dysfunction mitigation frameworks enhance drilling performance through systematic evaluation, feedback, and adaptation.",
        reasoning_framework="""
        Dysfunction mitigation frameworks are essential for drilling performance. The doctrine includes:
        - Systematic evaluation of drilling dysfunctions (stick-slip, whirl, buckling)
        - Integration with performance management and continuous improvement strategies
        - Reference to offset well data and industry standards
        - Use of predictive modeling and benchmarking for dysfunction mitigation
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive performance management.
        """,
        key_factors=[
            "Drilling dysfunction evaluation",
            "Performance management",
            "Continuous improvement",
            "Benchmarking",
            "Predictive modeling"
        ],
        primary_authority=[
            "Drilling Operations Standards",
            "SPE 166599",
            "Pad Development Guidelines"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Dysfunction mitigation frameworks may increase operational complexity or cost.",
        counter_arguments=[
            "Complex mitigation strategies may increase cost and operational risk.",
            "Operational variability may affect mitigation effectiveness.",
            "Industry standards may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative dysfunction mitigation based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, engineering teams",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 166599"
    ),
    DoctrineBlock(
        topic="Drilling_Parameter_Sensitivity_Analysis",
        keywords=["parameter sensitivity", "analysis", "drilling optimization", "performance management", "continuous improvement"],
        conclusion_template="Parameter sensitivity analysis enhances drilling optimization through systematic evaluation, feedback, and adaptation.",
        reasoning_framework="""
        Parameter sensitivity analysis is essential for drilling optimization. The doctrine includes:
        - Systematic evaluation of drilling parameter sensitivity (WOB, RPM, torque, ROP)
        - Integration with performance management and continuous improvement strategies
        - Reference to offset well data and industry standards
        - Use of predictive modeling and benchmarking for sensitivity analysis
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive performance management.
        """,
        key_factors=[
            "Parameter sensitivity evaluation",
            "Performance management",
            "Continuous improvement",
            "Benchmarking",
            "Predictive modeling"
        ],
        primary_authority=[
            "Drilling Operations Standards",
            "SPE 10023",
            "Pad Development Guidelines"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Parameter sensitivity analysis may increase operational complexity or cost.",
        counter_arguments=[
            "Complex analysis strategies may increase cost and operational risk.",
            "Operational variability may affect sensitivity analysis accuracy.",
            "Industry standards may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative sensitivity analysis based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, engineering teams",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 10023"
    ),
    DoctrineBlock(
        topic="Drilling_Fluid_Sensitivity_Analysis",
        keywords=["fluid sensitivity", "analysis", "drilling optimization", "performance management", "continuous improvement"],
        conclusion_template="Fluid sensitivity analysis enhances drilling optimization through systematic evaluation, feedback, and adaptation.",
        reasoning_framework="""
        Fluid sensitivity analysis is essential for drilling optimization. The doctrine includes:
        - Systematic evaluation of drilling fluid sensitivity (viscosity, density, pH, lubricity)
        - Integration with performance management and continuous improvement strategies
        - Reference to offset well data and industry standards
        - Use of predictive modeling and benchmarking for sensitivity analysis
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive fluid management.
        """,
        key_factors=[
            "Fluid sensitivity evaluation",
            "Performance management",
            "Continuous improvement",
            "Benchmarking",
            "Predictive modeling"
        ],
        primary_authority=[
            "Fluid Manufacturer Guidelines",
            "SPE 193067",
            "Drilling Operations Standards"
        ],
        burden_holder="Drilling Fluid Engineer",
        adversary_position="Fluid sensitivity analysis may increase operational complexity or cost.",
        counter_arguments=[
            "Complex analysis strategies may increase cost and operational risk.",
            "Operational variability may affect sensitivity analysis accuracy.",
            "Industry standards may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative fluid sensitivity analysis based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, fluid engineering teams",
        confidence=0.83,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 193067"
    ),
    DoctrineBlock(
        topic="Drilling_Benchmarking_Framework",
        keywords=["benchmarking", "framework", "drilling optimization", "performance management", "continuous improvement"],
        conclusion_template="Benchmarking frameworks enhance drilling optimization through systematic evaluation, feedback, and adaptation.",
        reasoning_framework="""
        Benchmarking frameworks are essential for drilling optimization. The doctrine includes:
        - Systematic evaluation of drilling performance metrics (ROP, NPT, cost per foot)
        - Integration with performance management and continuous improvement strategies
        - Reference to offset well data and industry standards
        - Use of predictive modeling and benchmarking for performance improvement
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive performance management.
        """,
        key_factors=[
            "Performance metrics",
            "Continuous improvement",
            "Benchmarking",
            "Offset well data",
            "Predictive modeling"
        ],
        primary_authority=[
            "Drilling Operations Standards",
            "SPE 194372",
            "Pad Development Guidelines"
        ],
        burden_holder="Drilling Performance Engineer",
        adversary_position="Benchmarking frameworks may increase operational complexity or cost.",
        counter_arguments=[
            "Complex frameworks may increase cost and operational risk.",
            "Operational variability may affect improvement trends.",
            "Industry standards may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative benchmarking based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, performance teams",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 194372"
    ),
    DoctrineBlock(
        topic="Drilling_Optimization_Algorithm_Selection",
        keywords=["optimization algorithm", "selection", "drilling optimization", "data analytics", "performance management"],
        conclusion_template="Optimization algorithm selection enhances drilling performance through systematic evaluation, benchmarking, and adaptation.",
        reasoning_framework="""
        Optimization algorithm selection is essential for drilling performance. The doctrine includes:
        - Systematic evaluation of optimization algorithms (regression, machine learning, neural networks)
        - Integration with performance management and benchmarking strategies
        - Reference to offset well data and industry standards
        - Use of predictive modeling and benchmarking for algorithm selection
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive performance management.
        """,
        key_factors=[
            "Algorithm evaluation",
            "Performance management",
            "Continuous improvement",
            "Benchmarking",
            "Predictive modeling"
        ],
        primary_authority=[
            "Drilling Data Analytics Standards",
            "SPE 194372",
            "Drilling Operations Guidelines"
        ],
        burden_holder="Drilling Data Engineer",
        adversary_position="Algorithm selection may increase operational complexity or cost.",
        counter_arguments=[
            "Complex algorithms may increase cost and operational risk.",
            "Operational variability may affect algorithm accuracy.",
            "Industry standards may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative algorithm selection based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, data analytics teams",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 194372"
    ),
    DoctrineBlock(
        topic="Drilling_Optimization_Algorithm_Validation",
        keywords=["optimization algorithm", "validation", "drilling optimization", "data analytics", "performance management"],
        conclusion_template="Optimization algorithm validation enhances drilling performance through systematic evaluation, benchmarking, and adaptation.",
        reasoning_framework="""
        Optimization algorithm validation is essential for drilling performance. The doctrine includes:
        - Systematic validation of optimization algorithms (cross-validation, error analysis)
        - Integration with performance management and benchmarking strategies
        - Reference to offset well data and industry standards
        - Use of predictive modeling and benchmarking for algorithm validation
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive performance management.
        """,
        key_factors=[
            "Algorithm validation",
            "Performance management",
            "Continuous improvement",
            "Benchmarking",
            "Predictive modeling"
        ],
        primary_authority=[
            "Drilling Data Analytics Standards",
            "SPE 194372",
            "Drilling Operations Guidelines"
        ],
        burden_holder="Drilling Data Engineer",
        adversary_position="Algorithm validation may increase operational complexity or cost.",
        counter_arguments=[
            "Complex validation strategies may increase cost and operational risk.",
            "Operational variability may affect validation accuracy.",
            "Industry standards may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative algorithm validation based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, data analytics teams",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 194372"
    ),
    DoctrineBlock(
        topic="Drilling_Optimization_Algorithm_Deployment",
        keywords=["optimization algorithm", "deployment", "drilling optimization", "data analytics", "performance management"],
        conclusion_template="Optimization algorithm deployment enhances drilling performance through systematic evaluation, benchmarking, and adaptation.",
        reasoning_framework="""
        Optimization algorithm deployment is essential for drilling performance. The doctrine includes:
        - Systematic deployment of optimization algorithms (integration, monitoring)
        - Integration with performance management and benchmarking strategies
        - Reference to offset well data and industry standards
        - Use of predictive modeling and benchmarking for algorithm deployment
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive performance management.
        """,
        key_factors=[
            "Algorithm deployment",
            "Performance management",
            "Continuous improvement",
            "Benchmarking",
            "Predictive modeling"
        ],
        primary_authority=[
            "Drilling Data Analytics Standards",
            "SPE 194372",
            "Drilling Operations Guidelines"
        ],
        burden_holder="Drilling Data Engineer",
        adversary_position="Algorithm deployment may increase operational complexity or cost.",
        counter_arguments=[
            "Complex deployment strategies may increase cost and operational risk.",
            "Operational variability may affect deployment accuracy.",
            "Industry standards may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative algorithm deployment based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, data analytics teams",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 194372"
    ),
    DoctrineBlock(
        topic="Drilling_Optimization_Algorithm_Maintenance",
        keywords=["optimization algorithm", "maintenance", "drilling optimization", "data analytics", "performance management"],
        conclusion_template="Optimization algorithm maintenance enhances drilling performance through systematic evaluation, benchmarking, and adaptation.",
        reasoning_framework="""
        Optimization algorithm maintenance is essential for drilling performance. The doctrine includes:
        - Systematic maintenance of optimization algorithms (updates, error correction)
        - Integration with performance management and benchmarking strategies
        - Reference to offset well data and industry standards
        - Use of predictive modeling and benchmarking for algorithm maintenance
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive performance management.
        """,
        key_factors=[
            "Algorithm maintenance",
            "Performance management",
            "Continuous improvement",
            "Benchmarking",
            "Predictive modeling"
        ],
        primary_authority=[
            "Drilling Data Analytics Standards",
            "SPE 194372",
            "Drilling Operations Guidelines"
        ],
        burden_holder="Drilling Data Engineer",
        adversary_position="Algorithm maintenance may increase operational complexity or cost.",
        counter_arguments=[
            "Complex maintenance strategies may increase cost and operational risk.",
            "Operational variability may affect maintenance accuracy.",
            "Industry standards may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative algorithm maintenance based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, data analytics teams",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 194372"
    ),
    DoctrineBlock(
        topic="Drilling_Optimization_Algorithm_Continuous_Improvement",
        keywords=["optimization algorithm", "continuous improvement", "drilling optimization", "data analytics", "performance management"],
        conclusion_template="Optimization algorithm continuous improvement enhances drilling performance through systematic evaluation, benchmarking, and adaptation.",
        reasoning_framework="""
        Optimization algorithm continuous improvement is essential for drilling performance. The doctrine includes:
        - Systematic evaluation and improvement of optimization algorithms (feedback, updates)
        - Integration with performance management and benchmarking strategies
        - Reference to offset well data and industry standards
        - Use of predictive modeling and benchmarking for algorithm improvement
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive performance management.
        """,
        key_factors=[
            "Algorithm improvement",
            "Performance management",
            "Continuous improvement",
            "Benchmarking",
            "Predictive modeling"
        ],
        primary_authority=[
            "Drilling Data Analytics Standards",
            "SPE 194372",
            "Drilling Operations Guidelines"
        ],
        burden_holder="Drilling Data Engineer",
        adversary_position="Algorithm improvement may increase operational complexity or cost.",
        counter_arguments=[
            "Complex improvement strategies may increase cost and operational risk.",
            "Operational variability may affect improvement accuracy.",
            "Industry standards may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative algorithm improvement based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, data analytics teams",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 194372"
    ),
    DoctrineBlock(
        topic="Drilling_Optimization_Algorithm_Benchmarking",
        keywords=["optimization algorithm", "benchmarking", "drilling optimization", "data analytics", "performance management"],
        conclusion_template="Optimization algorithm benchmarking enhances drilling performance through systematic evaluation, feedback, and adaptation.",
        reasoning_framework="""
        Optimization algorithm benchmarking is essential for drilling performance. The doctrine includes:
        - Systematic benchmarking of optimization algorithms (performance comparison, error analysis)
        - Integration with performance management and continuous improvement strategies
        - Reference to offset well data and industry standards
        - Use of predictive modeling and benchmarking for algorithm benchmarking
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive performance management.
        """,
        key_factors=[
            "Algorithm benchmarking",
            "Performance management",
            "Continuous improvement",
            "Benchmarking",
            "Predictive modeling"
        ],
        primary_authority=[
            "Drilling Data Analytics Standards",
            "SPE 194372",
            "Drilling Operations Guidelines"
        ],
        burden_holder="Drilling Data Engineer",
        adversary_position="Algorithm benchmarking may increase operational complexity or cost.",
        counter_arguments=[
            "Complex benchmarking strategies may increase cost and operational risk.",
            "Operational variability may affect benchmarking accuracy.",
            "Industry standards may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative algorithm benchmarking based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, data analytics teams",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 194372"
    ),
    DoctrineBlock(
        topic="Drilling_Optimization_Algorithm_Integration",
        keywords=["optimization algorithm", "integration", "drilling optimization", "data analytics", "performance management"],
        conclusion_template="Optimization algorithm integration enhances drilling performance through systematic evaluation, benchmarking, and adaptation.",
        reasoning_framework="""
        Optimization algorithm integration is essential for drilling performance. The doctrine includes:
        - Systematic integration of optimization algorithms (data platform, analytics tools)
        - Integration with performance management and benchmarking strategies
        - Reference to offset well data and industry standards
        - Use of predictive modeling and benchmarking for algorithm integration
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive performance management.
        """,
        key_factors=[
            "Algorithm integration",
            "Performance management",
            "Continuous improvement",
            "Benchmarking",
            "Predictive modeling"
        ],
        primary_authority=[
            "Drilling Data Analytics Standards",
            "SPE 194372",
            "Drilling Operations Guidelines"
        ],
        burden_holder="Drilling Data Engineer",
        adversary_position="Algorithm integration may increase operational complexity or cost.",
        counter_arguments=[
            "Complex integration strategies may increase cost and operational risk.",
            "Operational variability may affect integration accuracy.",
            "Industry standards may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative algorithm integration based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, data analytics teams",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 194372"
    ),
    DoctrineBlock(
        topic="Drilling_Optimization_Algorithm_Adaptation",
        keywords=["optimization algorithm", "adaptation", "drilling optimization", "data analytics", "performance management"],
        conclusion_template="Optimization algorithm adaptation enhances drilling performance through systematic evaluation, benchmarking, and adaptation.",
        reasoning_framework="""
        Optimization algorithm adaptation is essential for drilling performance. The doctrine includes:
        - Systematic adaptation of optimization algorithms (parameter tuning, feedback)
        - Integration with performance management and benchmarking strategies
        - Reference to offset well data and industry standards
        - Use of predictive modeling and benchmarking for algorithm adaptation
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive performance management.
        """,
        key_factors=[
            "Algorithm adaptation",
            "Performance management",
            "Continuous improvement",
            "Benchmarking",
            "Predictive modeling"
        ],
        primary_authority=[
            "Drilling Data Analytics Standards",
            "SPE 194372",
            "Drilling Operations Guidelines"
        ],
        burden_holder="Drilling Data Engineer",
        adversary_position="Algorithm adaptation may increase operational complexity or cost.",
        counter_arguments=[
            "Complex adaptation strategies may increase cost and operational risk.",
            "Operational variability may affect adaptation accuracy.",
            "Industry standards may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative algorithm adaptation based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, data analytics teams",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 194372"
    ),
    DoctrineBlock(
        topic="Drilling_Optimization_Algorithm_Operationalization",
        keywords=["optimization algorithm", "operationalization", "drilling optimization", "data analytics", "performance management"],
        conclusion_template="Optimization algorithm operationalization enhances drilling performance through systematic evaluation, benchmarking, and adaptation.",
        reasoning_framework="""
        Optimization algorithm operationalization is essential for drilling performance. The doctrine includes:
        - Systematic operationalization of optimization algorithms (workflow integration, monitoring)
        - Integration with performance management and benchmarking strategies
        - Reference to offset well data and industry standards
        - Use of predictive modeling and benchmarking for algorithm operationalization
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive performance management.
        """,
        key_factors=[
            "Algorithm operationalization",
            "Performance management",
            "Continuous improvement",
            "Benchmarking",
            "Predictive modeling"
        ],
        primary_authority=[
            "Drilling Data Analytics Standards",
            "SPE 194372",
            "Drilling Operations Guidelines"
        ],
        burden_holder="Drilling Data Engineer",
        adversary_position="Algorithm operationalization may increase operational complexity or cost.",
        counter_arguments=[
            "Complex operationalization strategies may increase cost and operational risk.",
            "Operational variability may affect operationalization accuracy.",
            "Industry standards may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative algorithm operationalization based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, data analytics teams",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 194372"
    ),
    DoctrineBlock(
        topic="Drilling_Optimization_Algorithm_Scalability",
        keywords=["optimization algorithm", "scalability", "drilling optimization", "data analytics", "performance management"],
        conclusion_template="Optimization algorithm scalability enhances drilling performance through systematic evaluation, benchmarking, and adaptation.",
        reasoning_framework="""
        Optimization algorithm scalability is essential for drilling performance. The doctrine includes:
        - Systematic evaluation of algorithm scalability (deployment, integration)
        - Integration with performance management and benchmarking strategies
        - Reference to offset well data and industry standards
        - Use of predictive modeling and benchmarking for scalability evaluation
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive performance management.
        """,
        key_factors=[
            "Algorithm scalability",
            "Performance management",
            "Continuous improvement",
            "Benchmarking",
            "Predictive modeling"
        ],
        primary_authority=[
            "Drilling Data Analytics Standards",
            "SPE 194372",
            "Drilling Operations Guidelines"
        ],
        burden_holder="Drilling Data Engineer",
        adversary_position="Algorithm scalability may increase operational complexity or cost.",
        counter_arguments=[
            "Complex scalability strategies may increase cost and operational risk.",
            "Operational variability may affect scalability accuracy.",
            "Industry standards may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative scalability evaluation based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, data analytics teams",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 194372"
    ),
    DoctrineBlock(
        topic="Drilling_Optimization_Algorithm_Usability",
        keywords=["optimization algorithm", "usability", "drilling optimization", "data analytics", "performance management"],
        conclusion_template="Optimization algorithm usability enhances drilling performance through systematic evaluation, benchmarking, and adaptation.",
        reasoning_framework="""
        Optimization algorithm usability is essential for drilling performance. The doctrine includes:
        - Systematic evaluation of algorithm usability (user interface, workflow integration)
        - Integration with performance management and benchmarking strategies
        - Reference to offset well data and industry standards
        - Use of predictive modeling and benchmarking for usability evaluation
        The framework emphasizes continuous evaluation, real-time adaptation, and proactive performance management.
        """,
        key_factors=[
            "Algorithm usability",
            "Performance management",
            "Continuous improvement",
            "Benchmarking",
            "Predictive modeling"
        ],
        primary_authority=[
            "Drilling Data Analytics Standards",
            "SPE 194372",
            "Drilling Operations Guidelines"
        ],
        burden_holder="Drilling Data Engineer",
        adversary_position="Algorithm usability may increase operational complexity or cost.",
        counter_arguments=[
            "Complex usability strategies may increase cost and operational risk.",
            "Operational variability may affect usability accuracy.",
            "Industry standards may not reflect real-time conditions."
        ],
        resolution_strategy="Iterative usability evaluation based on real-time data, benchmarking, and predictive modeling.",
        entity_scope="Drilling operations, data analytics teams",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 194372"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic == topic:
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    keyword_lower = keyword.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if any(keyword_lower in k.lower() for k in doctrine.keywords) or keyword_lower in doctrine.topic.lower():
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]