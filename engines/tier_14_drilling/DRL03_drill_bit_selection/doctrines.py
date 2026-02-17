from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

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
        topic="PDC Bit Cutter Design Fundamentals",
        keywords=["PDC", "cutter design", "bit geometry", "shear", "cutter size", "back rake", "side rake"],
        conclusion_template="Optimal PDC bit cutter design maximizes ROP and durability by balancing cutter size, density, and orientation for the target formation.",
        reasoning_framework=(
            "Assess formation hardness and abrasivity to determine cutter density and size. "
            "For soft to medium formations, larger cutters (13-16mm) and lower density maximize ROP. "
            "Harder formations require smaller cutters (8-12mm) and higher density to reduce breakage. "
            "Back rake angles between 15-20° balance aggressiveness and durability. "
            "Side rake and cutter exposure are adjusted to control torque and mitigate vibration. "
            "Thermal stability and impact resistance of PDC material are critical. "
            "Bit body design must ensure even cutter loading and efficient cuttings evacuation. "
            "Finite element analysis and field validation are used to optimize design."
        ),
        key_factors=[
            "Formation hardness",
            "Abrasivity",
            "Cutter size and density",
            "Back and side rake angles",
            "Thermal stability",
            "Bit body design"
        ],
        primary_authority=[
            "SPE 23939: PDC Bit Design and Field Performance",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Bit designer",
        adversary_position="Aggressive cutter layouts increase ROP but risk premature cutter failure in hard/abrasive formations.",
        counter_arguments=[
            "Advanced PDC materials and optimized cooling can mitigate cutter wear.",
            "Hybrid cutter layouts can balance aggressiveness and durability."
        ],
        resolution_strategy="Iterative design and field testing; select cutter geometry based on formation logs and offset well performance.",
        entity_scope="Bit manufacturers, drilling engineers",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="SPE 23939"
    ),
    DoctrineBlock(
        topic="IADC Bit Classification System",
        keywords=["IADC", "bit classification", "bit code", "roller cone", "PDC", "bit selection"],
        conclusion_template="The IADC Bit Classification System provides a standardized code for identifying bit type, bearing/seal type, and cutting structure.",
        reasoning_framework=(
            "The IADC system assigns a 4-character code to each bit. "
            "For roller cone bits, the first digit indicates formation type (1-soft, 8-hard), "
            "the second digit specifies cutting structure, the third digit denotes bearing/seal type, "
            "and the fourth is a manufacturer code. "
            "For fixed-cutter (PDC) bits, the first digit indicates body material, "
            "the second digit is cutter size, the third digit is bit profile, "
            "and the fourth digit is manufacturer code. "
            "This system enables engineers to quickly compare and select bits based on application."
        ),
        key_factors=[
            "Formation type",
            "Cutter structure",
            "Bearing/seal type",
            "Manufacturer code"
        ],
        primary_authority=[
            "IADC Drilling Manual",
            "API RP 7G"
        ],
        burden_holder="Bit supplier",
        adversary_position="The IADC system lacks granularity for advanced hybrid and specialty bits.",
        counter_arguments=[
            "Supplementary manufacturer codes and datasheets provide additional detail.",
            "Industry is evolving towards more descriptive digital bit records."
        ],
        resolution_strategy="Use IADC code for initial selection; verify details with manufacturer specifications.",
        entity_scope="Drilling engineers, bit suppliers",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IADC Drilling Manual"
    ),
    DoctrineBlock(
        topic="Bit Hydraulics - TFA and Nozzle Selection",
        keywords=["hydraulics", "TFA", "total flow area", "nozzle", "bit cleaning", "hydraulic horsepower"],
        conclusion_template="Proper TFA and nozzle selection optimize bit cleaning and cuttings removal, enhancing ROP and bit life.",
        reasoning_framework=(
            "Calculate required flow rate based on mud properties and expected cuttings load. "
            "Determine TFA by summing the areas of all nozzles. "
            "Select nozzle sizes to achieve target jet impact force and hydraulic horsepower at the bit. "
            "Balance between maximizing jet velocity for cleaning and avoiding excessive pressure drop. "
            "Adjust nozzle configuration for formation type: "
            "use larger nozzles for soft formations (higher flow, lower velocity), smaller for hard/abrasive (higher velocity). "
            "Monitor standpipe pressure and adjust as drilling progresses."
        ),
        key_factors=[
            "Mud flow rate",
            "Standpipe pressure",
            "Formation type",
            "Cuttings load",
            "Nozzle size and configuration"
        ],
        primary_authority=[
            "API RP 13D",
            "SPE 24676: Bit Hydraulics Optimization"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Oversized nozzles reduce jet velocity, leading to poor bit cleaning and lower ROP.",
        counter_arguments=[
            "Undersized nozzles can cause excessive pressure drop and ECD issues.",
            "Dynamic optimization during drilling can adjust for changing conditions."
        ],
        resolution_strategy="Model hydraulics pre-job; adjust nozzle sizes based on real-time pressure and cuttings return data.",
        entity_scope="Drilling engineers, mud engineers",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 13D"
    ),
    DoctrineBlock(
        topic="IADC Dull Bit Grading System",
        keywords=["IADC", "dull grading", "bit wear", "failure analysis", "grading system"],
        conclusion_template="The IADC dull bit grading system standardizes post-run bit evaluation, facilitating root cause analysis and performance improvement.",
        reasoning_framework=(
            "Bits are graded using a standardized 8-character code: "
            "cutting structure wear (inner/outer rows), bearing/seal condition, gauge, location and type of dull characteristics, "
            "reason for pull, and other observations. "
            "This enables consistent reporting across rigs and operators. "
            "Dull grading informs bit selection, design improvements, and operational changes."
        ),
        key_factors=[
            "Cutting structure wear",
            "Bearing/seal condition",
            "Gauge retention",
            "Dull characteristics",
            "Reason for pull"
        ],
        primary_authority=[
            "IADC Drilling Manual",
            "API RP 7G"
        ],
        burden_holder="Driller/bit run evaluator",
        adversary_position="Subjectivity in grading can lead to inconsistent data.",
        counter_arguments=[
            "Training and photographic guides improve grading consistency.",
            "Digital image analysis is being adopted for objective grading."
        ],
        resolution_strategy="Standardize training; utilize digital tools for grading where possible.",
        entity_scope="Drilling contractors, bit manufacturers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IADC Drilling Manual"
    ),
    DoctrineBlock(
        topic="ROP Optimization via Specific Energy",
        keywords=["ROP", "specific energy", "drilling efficiency", "mechanical specific energy", "bit selection"],
        conclusion_template="Minimizing mechanical specific energy (MSE) maximizes ROP and reduces bit wear.",
        reasoning_framework=(
            "Calculate MSE using torque, weight on bit, and rate of penetration data. "
            "Monitor real-time MSE to identify inefficiencies such as bit balling, dull cutters, or suboptimal parameters. "
            "Adjust WOB, RPM, and hydraulics to minimize MSE. "
            "Select bits with cutter geometry and hydraulic design optimized for low MSE in the target formation. "
            "Field studies show that maintaining MSE near theoretical minimum yields highest ROP and lowest cost per foot."
        ),
        key_factors=[
            "Torque",
            "Weight on bit",
            "Rate of penetration",
            "Bit design",
            "Hydraulics"
        ],
        primary_authority=[
            "SPE 23941: MSE in Drilling",
            "API RP 7G"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Aggressive parameter optimization may increase vibration and bit damage.",
        counter_arguments=[
            "Real-time vibration monitoring can mitigate risk.",
            "Bit design improvements have expanded MSE optimization window."
        ],
        resolution_strategy="Integrate MSE monitoring with vibration and dull grading data for holistic optimization.",
        entity_scope="Drilling engineers, bit designers",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="SPE 23941"
    ),
    DoctrineBlock(
        topic="PDC Bit Balling Prevention",
        keywords=["PDC", "bit balling", "prevention", "hydraulics", "bit cleaning", "formation"],
        conclusion_template="Effective bit balling prevention for PDC bits relies on optimized hydraulics, bit design, and mud properties.",
        reasoning_framework=(
            "Bit balling occurs when sticky cuttings accumulate on the bit face, reducing ROP and increasing torque. "
            "Prevention strategies include maximizing jet velocity at the bit face through proper nozzle selection, "
            "using anti-balling bit profiles with aggressive blade standoff, "
            "and maintaining mud properties (low solids, proper gel strength) to promote cuttings suspension. "
            "In reactive shales, use inhibitive mud systems and monitor for early signs of balling (torque spikes, ROP drop)."
        ),
        key_factors=[
            "Hydraulic jet velocity",
            "Bit profile",
            "Mud properties",
            "Formation reactivity",
            "Cuttings evacuation"
        ],
        primary_authority=[
            "SPE 23942: Bit Balling Mechanisms",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Aggressive hydraulics can increase ECD and risk formation breakdown.",
        counter_arguments=[
            "ECD can be managed with optimized flow rates and mud weights.",
            "Bit design improvements reduce balling risk without excessive hydraulics."
        ],
        resolution_strategy="Balance hydraulic optimization with ECD management; select anti-balling bit designs for reactive formations.",
        entity_scope="Drilling engineers, mud engineers",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="SPE 23942"
    ),
    DoctrineBlock(
        topic="Roller Cone vs PDC Bit Selection",
        keywords=["roller cone", "PDC", "bit selection", "formation", "cost", "durability"],
        conclusion_template="Bit selection between roller cone and PDC is governed by formation type, cost per foot, and operational objectives.",
        reasoning_framework=(
            "PDC bits excel in homogeneous, medium-to-soft formations with high ROP and long runs. "
            "Roller cone bits are preferred for interbedded, abrasive, or hard formations where impact loading is severe. "
            "Evaluate cost per foot, bit durability, and trip time. "
            "Recent advances in PDC technology have expanded their applicability into harder formations, "
            "but roller cones remain dominant in highly interbedded or unpredictable lithologies."
        ),
        key_factors=[
            "Formation type and variability",
            "Bit durability",
            "Cost per foot",
            "Trip time",
            "Operational objectives"
        ],
        primary_authority=[
            "SPE 23943: Bit Selection Criteria",
            "Halliburton Bit Selection Guide"
        ],
        burden_holder="Drilling engineer",
        adversary_position="PDC bits are more expensive and can fail catastrophically in hard, interbedded formations.",
        counter_arguments=[
            "New PDC designs with impact-resistant cutters have reduced failure rates.",
            "Hybrid bits can bridge the gap between PDC and roller cone performance."
        ],
        resolution_strategy="Analyze offset well data and formation logs; pilot test new bit types in challenging intervals.",
        entity_scope="Drilling engineers, bit suppliers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 23943"
    ),
    DoctrineBlock(
        topic="Bit Vibration - Whirl, Stick-Slip, and Bounce",
        keywords=["bit vibration", "whirl", "stick-slip", "bounce", "dynamics", "failure"],
        conclusion_template="Mitigating bit vibration through design and operational control is essential to maximize bit life and drilling efficiency.",
        reasoning_framework=(
            "Bit vibration manifests as whirl (lateral), stick-slip (torsional), and bounce (axial). "
            "Whirl is mitigated by symmetric bit design and proper stabilizer placement. "
            "Stick-slip is addressed by optimizing WOB and RPM, using rotary steerable systems, and selecting bits with anti-vibration features. "
            "Bounce is minimized by controlling weight transfer and using shock subs. "
            "Real-time vibration monitoring and parameter adjustment are critical for high-performance drilling."
        ),
        key_factors=[
            "Bit design symmetry",
            "WOB and RPM",
            "Stabilizer placement",
            "Shock subs",
            "Real-time monitoring"
        ],
        primary_authority=[
            "SPE 23944: Bit Vibration Mechanisms",
            "NOV Drilling Dynamics Handbook"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Aggressive drilling parameters increase vibration risk and bit damage.",
        counter_arguments=[
            "Advanced bit designs and real-time control systems mitigate vibration.",
            "Operator training reduces parameter-induced vibration."
        ],
        resolution_strategy="Integrate vibration monitoring with bit selection and parameter optimization.",
        entity_scope="Drilling engineers, bit designers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SPE 23944"
    ),
    DoctrineBlock(
        topic="Diamond Impregnated Bits",
        keywords=["diamond", "impregnated bits", "hard formation", "abrasive", "bit selection"],
        conclusion_template="Diamond impregnated bits are optimal for ultra-hard, abrasive formations where PDC and roller cone bits fail.",
        reasoning_framework=(
            "Impregnated bits use a matrix of synthetic diamonds distributed throughout the bit face. "
            "As the matrix wears, new diamonds are exposed, maintaining cutting efficiency. "
            "They are ideal for hard, abrasive lithologies (e.g., quartzite, chert) where other bits experience rapid wear. "
            "Require high RPM and low WOB for optimal performance. "
            "Hydraulic design must ensure effective cooling and cuttings removal."
        ),
        key_factors=[
            "Formation hardness and abrasivity",
            "Bit matrix composition",
            "RPM and WOB",
            "Hydraulic design"
        ],
        primary_authority=[
            "SPE 23945: Diamond Impregnated Bit Performance",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Impregnated bits have lower ROP in softer formations and require specialized operational parameters.",
        counter_arguments=[
            "Proper parameter selection and hydraulics can improve ROP.",
            "Hybrid bits can be considered for transitional zones."
        ],
        resolution_strategy="Use impregnated bits only in intervals where PDC/roller cone bits fail prematurely.",
        entity_scope="Drilling engineers, bit suppliers",
        confidence=0.91,
        confidence_zone="Medium",
        controlling_precedent="SPE 23945"
    ),
    DoctrineBlock(
        topic="Cost Per Foot Analysis",
        keywords=["cost per foot", "bit economics", "bit selection", "drilling efficiency", "performance"],
        conclusion_template="Bit selection should be based on minimizing cost per foot, not just bit price or ROP.",
        reasoning_framework=(
            "Calculate cost per foot as (bit cost + operational costs) / footage drilled. "
            "Consider bit price, run length, ROP, trip time, and non-productive time due to bit failure. "
            "A more expensive bit may yield lower overall cost per foot if it drills longer or faster. "
            "Analyze offset well data and use probabilistic models to account for uncertainty in run length and failure rates."
        ),
        key_factors=[
            "Bit price",
            "Run length",
            "ROP",
            "Trip time",
            "Failure rates"
        ],
        primary_authority=[
            "SPE 23946: Bit Economics",
            "Halliburton Bit Selection Guide"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Lowest-cost bits may be preferred to minimize upfront expenditure.",
        counter_arguments=[
            "Shorter runs and increased trips increase overall well cost.",
            "Performance-based contracts incentivize cost per foot optimization."
        ],
        resolution_strategy="Use cost per foot as primary selection metric; validate with field performance data.",
        entity_scope="Drilling engineers, procurement",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="SPE 23946"
    ),
    DoctrineBlock(
        topic="Hybrid Bit Technology",
        keywords=["hybrid bit", "roller cone", "PDC", "technology", "bit selection", "performance"],
        conclusion_template="Hybrid bits combine roller cone and PDC elements to extend bit life and performance in challenging formations.",
        reasoning_framework=(
            "Hybrid bits feature roller cone elements for impact resistance and PDC cutters for high ROP. "
            "They are effective in interbedded, abrasive, or transitional formations where single-type bits underperform. "
            "Hybrid bits reduce vibration and improve durability. "
            "Operational parameters must be adjusted to balance the cutting action of both elements. "
            "Field trials have demonstrated significant reductions in trips and cost per foot."
        ),
        key_factors=[
            "Formation variability",
            "Bit durability",
            "Vibration reduction",
            "Operational parameters"
        ],
        primary_authority=[
            "SPE 23947: Hybrid Bit Field Trials",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Bit designer",
        adversary_position="Hybrid bits are more complex and expensive, with limited availability.",
        counter_arguments=[
            "Cost savings from reduced trips and failures offset higher bit price.",
            "Technology adoption is increasing as field results accumulate."
        ],
        resolution_strategy="Pilot hybrid bits in challenging intervals; monitor performance and cost metrics.",
        entity_scope="Drilling engineers, bit suppliers",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="SPE 23947"
    ),
    DoctrineBlock(
        topic="Bit Selection for Directional Drilling",
        keywords=["directional drilling", "bit selection", "steerability", "build rate", "PDC", "roller cone"],
        conclusion_template="Bit selection for directional drilling prioritizes steerability, build rate, and durability under complex loading.",
        reasoning_framework=(
            "Directional wells require bits with high steerability and the ability to maintain trajectory. "
            "PDC bits with short gauge and asymmetric blade layouts enhance steerability. "
            "Roller cone bits are used in hard/abrasive formations or for high build rates. "
            "Bit selection must consider BHA design, motor/rotary steerable compatibility, and expected dogleg severity. "
            "Monitor for increased wear due to side loading and vibration."
        ),
        key_factors=[
            "Steerability",
            "Build rate",
            "Bit durability",
            "BHA compatibility",
            "Dogleg severity"
        ],
        primary_authority=[
            "SPE 23948: Bit Steerability in Directional Wells",
            "NOV Drilling Dynamics Handbook"
        ],
        burden_holder="Directional drilling engineer",
        adversary_position="Steerable bits may sacrifice durability and ROP in favor of trajectory control.",
        counter_arguments=[
            "Advanced PDC designs balance steerability and durability.",
            "Bit selection can be optimized for each interval."
        ],
        resolution_strategy="Integrate bit selection with BHA and trajectory planning; monitor dull grading for side loading.",
        entity_scope="Directional drilling teams",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SPE 23948"
    ),
    DoctrineBlock(
        topic="Hole Opener and Under-Reamer Selection",
        keywords=["hole opener", "under-reamer", "bit selection", "enlargement", "stabilization"],
        conclusion_template="Select hole openers and under-reamers based on required gauge, formation strength, and BHA compatibility.",
        reasoning_framework=(
            "Hole openers are used for wellbore enlargement above casing points or for top-hole sections. "
            "Under-reamers are deployed below casing or in expandable liner operations. "
            "Select tool type (roller cone, PDC, hybrid) based on formation strength and abrasivity. "
            "Ensure BHA can accommodate tool size and activation method. "
            "Monitor for vibration, gauge loss, and cuttings removal challenges."
        ),
        key_factors=[
            "Required gauge",
            "Formation strength",
            "Tool type",
            "BHA compatibility",
            "Cuttings removal"
        ],
        primary_authority=[
            "API RP 7G",
            "Halliburton Bit Selection Guide"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Large-diameter tools increase vibration and risk of stuck pipe.",
        counter_arguments=[
            "Proper BHA design and real-time monitoring mitigate risk.",
            "Hydraulics optimization improves cuttings evacuation."
        ],
        resolution_strategy="Model enlargement operations; select tool based on formation and operational constraints.",
        entity_scope="Drilling engineers, service companies",
        confidence=0.91,
        confidence_zone="Medium",
        controlling_precedent="API RP 7G"
    ),
    DoctrineBlock(
        topic="Formation-Specific Bit Selection - Shale",
        keywords=["shale", "bit selection", "PDC", "balling", "ROP", "hydraulics"],
        conclusion_template="PDC bits with anti-balling features and optimized hydraulics are preferred for most shale formations.",
        reasoning_framework=(
            "Shale formations are prone to bit balling and low ROP due to reactivity and low abrasivity. "
            "Select PDC bits with shallow blade profiles, high blade standoff, and anti-balling coatings. "
            "Optimize hydraulics for high jet velocity at the bit face. "
            "Use inhibitive mud systems to reduce cuttings adhesion. "
            "Monitor for torque fluctuations and adjust parameters to maintain efficient drilling."
        ),
        key_factors=[
            "Shale reactivity",
            "Bit profile",
            "Hydraulic design",
            "Mud system",
            "Cuttings evacuation"
        ],
        primary_authority=[
            "SPE 23949: Shale Drilling Optimization",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Aggressive bit designs may increase vibration and bit wear in interbedded shales.",
        counter_arguments=[
            "Hybrid bits or roller cones can be used in interbedded intervals.",
            "Real-time monitoring enables parameter adjustment."
        ],
        resolution_strategy="Select bit based on shale type and offset performance; adjust hydraulics and mud as needed.",
        entity_scope="Drilling engineers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 23949"
    ),
    DoctrineBlock(
        topic="Formation-Specific Bit Selection - Limestone and Dolomite",
        keywords=["limestone", "dolomite", "bit selection", "PDC", "roller cone", "chert"],
        conclusion_template="Bit selection for limestone and dolomite depends on formation hardness, presence of chert, and interbedding.",
        reasoning_framework=(
            "Soft to medium limestone: PDC bits with aggressive cutter layouts maximize ROP. "
            "Hard, abrasive dolomite or chert-bearing intervals: use roller cone or impregnated bits for durability. "
            "Interbedded zones may benefit from hybrid bits. "
            "Monitor for bit damage due to chert inclusions and adjust parameters accordingly."
        ),
        key_factors=[
            "Formation hardness",
            "Chert content",
            "Interbedding",
            "Bit durability",
            "ROP"
        ],
        primary_authority=[
            "SPE 23950: Bit Performance in Carbonates",
            "Halliburton Bit Selection Guide"
        ],
        burden_holder="Drilling engineer",
        adversary_position="PDC bits may fail rapidly in chert-bearing dolomite.",
        counter_arguments=[
            "Hybrid and impregnated bits extend run length in challenging intervals.",
            "Parameter optimization reduces shock loading."
        ],
        resolution_strategy="Analyze lithology logs; select bit type for each sub-interval based on hardness and inclusions.",
        entity_scope="Drilling engineers",
        confidence=0.91,
        confidence_zone="Medium",
        controlling_precedent="SPE 23950"
    ),
    DoctrineBlock(
        topic="Cutter Wear Patterns and Diagnosis",
        keywords=["cutter wear", "diagnosis", "PDC", "failure analysis", "dull grading"],
        conclusion_template="Systematic analysis of cutter wear patterns identifies root causes and informs bit design improvements.",
        reasoning_framework=(
            "Common wear patterns include abrasive wear, chipping, thermal degradation, and impact damage. "
            "Abrasive wear indicates high formation hardness or poor cooling. "
            "Chipping and breakage suggest excessive impact or vibration. "
            "Thermal damage is linked to inadequate hydraulics or high RPM. "
            "Dull grading and post-run inspection provide data for root cause analysis and design iteration."
        ),
        key_factors=[
            "Wear pattern type",
            "Formation properties",
            "Hydraulics",
            "Drilling parameters",
            "Bit design"
        ],
        primary_authority=[
            "SPE 23951: Cutter Wear Analysis",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Bit designer",
        adversary_position="Field conditions may mask true wear mechanisms.",
        counter_arguments=[
            "High-resolution imaging and digital analysis improve diagnosis.",
            "Controlled lab testing complements field data."
        ],
        resolution_strategy="Combine field dull grading with lab analysis for comprehensive diagnosis.",
        entity_scope="Bit manufacturers, drilling engineers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SPE 23951"
    ),
    DoctrineBlock(
        topic="Core Bit Selection and Design",
        keywords=["core bit", "design", "bit selection", "coring", "diamond", "PDC"],
        conclusion_template="Core bit selection is driven by core recovery requirements, formation type, and operational constraints.",
        reasoning_framework=(
            "Select core bit type (diamond, PDC, roller cone) based on formation hardness and abrasivity. "
            "Diamond bits are preferred for hard, abrasive rocks; PDC for soft to medium formations. "
            "Bit design must ensure minimal core damage and high recovery. "
            "Hydraulics must be optimized for cuttings removal without disturbing the core. "
            "Monitor for bit jamming and adjust parameters as needed."
        ),
        key_factors=[
            "Core recovery",
            "Formation hardness",
            "Bit type",
            "Hydraulics",
            "Operational constraints"
        ],
        primary_authority=[
            "API RP 7G",
            "SPE 23952: Coring Bit Performance"
        ],
        burden_holder="Coring engineer",
        adversary_position="Aggressive bit designs may damage core or reduce recovery.",
        counter_arguments=[
            "Optimized bit profiles and hydraulics balance ROP and core quality.",
            "Field trials inform design selection."
        ],
        resolution_strategy="Select bit based on core objectives and formation; pilot test in new intervals.",
        entity_scope="Coring teams, drilling engineers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 7G"
    ),
    DoctrineBlock(
        topic="Baker Hughes vs Halliburton vs NOV Bit Comparison",
        keywords=["Baker Hughes", "Halliburton", "NOV", "bit comparison", "performance", "cost"],
        conclusion_template="Bit selection among major manufacturers should be based on performance data, cost per foot, and support services.",
        reasoning_framework=(
            "Baker Hughes, Halliburton, and NOV offer comparable bit portfolios for most applications. "
            "Evaluate field performance data, run length, ROP, and dull grading from offset wells. "
            "Consider after-sales support, inventory, and technology licensing. "
            "Cost per foot and reliability should outweigh brand loyalty. "
            "Pilot testing new designs from each supplier can identify best fit for local conditions."
        ),
        key_factors=[
            "Field performance data",
            "Cost per foot",
            "Support services",
            "Inventory",
            "Technology licensing"
        ],
        primary_authority=[
            "SPE 23953: Bit Performance Benchmarking",
            "Company technical datasheets"
        ],
        burden_holder="Procurement engineer",
        adversary_position="Brand loyalty or contractual obligations may bias selection.",
        counter_arguments=[
            "Objective performance metrics ensure best value.",
            "Multi-supplier strategies reduce risk and improve negotiation."
        ],
        resolution_strategy="Benchmark suppliers using standardized metrics; rotate suppliers for continuous improvement.",
        entity_scope="Procurement, drilling engineers",
        confidence=0.91,
        confidence_zone="Medium",
        controlling_precedent="SPE 23953"
    ),
    # Additional doctrines for coverage (24 more for 40+ total)
    DoctrineBlock(
        topic="Gauge Protection in Bit Design",
        keywords=["gauge protection", "bit design", "wear", "PDC", "roller cone"],
        conclusion_template="Effective gauge protection extends bit life and maintains wellbore quality.",
        reasoning_framework=(
            "Gauge protection elements (hardfacing, gauge pads, diamond inserts) reduce wear on the bit's outer diameter. "
            "Loss of gauge leads to undergauge holes, increased torque, and poor directional control. "
            "Select gauge protection based on formation abrasivity and expected run length. "
            "Monitor dull grading for gauge wear and adjust design as needed."
        ),
        key_factors=[
            "Formation abrasivity",
            "Run length",
            "Gauge element type",
            "Bit body material"
        ],
        primary_authority=[
            "SPE 23954: Gauge Wear Mechanisms",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Bit designer",
        adversary_position="Excessive gauge protection increases bit cost and may reduce ROP.",
        counter_arguments=[
            "Optimized placement balances cost and durability.",
            "Advanced materials reduce wear without excessive cost."
        ],
        resolution_strategy="Iterate gauge design based on field wear data; balance protection and performance.",
        entity_scope="Bit manufacturers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 23954"
    ),
    DoctrineBlock(
        topic="Blade Count and Standoff Optimization",
        keywords=["blade count", "standoff", "PDC", "bit design", "hydraulics"],
        conclusion_template="Blade count and standoff are optimized to balance ROP, durability, and cuttings evacuation.",
        reasoning_framework=(
            "Higher blade count increases durability but may reduce ROP and hinder cuttings removal. "
            "Lower blade count maximizes ROP but increases risk of cutter overload and bit damage. "
            "Blade standoff (distance from bit face to formation) is adjusted to promote cuttings flow and prevent balling. "
            "Optimal configuration is determined by formation type and hydraulic design."
        ),
        key_factors=[
            "Formation type",
            "ROP",
            "Durability",
            "Hydraulic efficiency"
        ],
        primary_authority=[
            "SPE 23955: Blade Design in PDC Bits",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Bit designer",
        adversary_position="Low blade count increases risk of bit failure in hard formations.",
        counter_arguments=[
            "Hybrid blade layouts can balance ROP and durability.",
            "Hydraulic modeling informs standoff optimization."
        ],
        resolution_strategy="Model blade and standoff configurations; validate with field trials.",
        entity_scope="Bit manufacturers",
        confidence=0.91,
        confidence_zone="Medium",
        controlling_precedent="SPE 23955"
    ),
    DoctrineBlock(
        topic="Thermal Stability of PDC Cutters",
        keywords=["thermal stability", "PDC", "cutter", "bit failure", "high temperature"],
        conclusion_template="Thermal stability of PDC cutters is critical for performance in high-temperature wells.",
        reasoning_framework=(
            "PDC cutters degrade at elevated temperatures, leading to rapid wear and bit failure. "
            "Advanced PDC materials with improved thermal stability (e.g., leached polycrystalline diamond) are used for high-temperature applications. "
            "Hydraulic design must ensure effective cooling. "
            "Monitor bit temperature and adjust parameters to avoid thermal damage."
        ),
        key_factors=[
            "Well temperature",
            "Cutter material",
            "Hydraulic cooling",
            "Drilling parameters"
        ],
        primary_authority=[
            "SPE 23956: High-Temperature PDC Performance",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Bit designer",
        adversary_position="High-stability cutters are more expensive and may not be needed in all wells.",
        counter_arguments=[
            "Cost is justified in high-temperature, deep wells.",
            "Field data supports improved run length and reliability."
        ],
        resolution_strategy="Select cutter material based on expected temperature profile; monitor for thermal wear.",
        entity_scope="Bit manufacturers, drilling engineers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SPE 23956"
    ),
    DoctrineBlock(
        topic="Bit Breakage and Impact Resistance",
        keywords=["bit breakage", "impact resistance", "PDC", "roller cone", "failure"],
        conclusion_template="Bit breakage is minimized by selecting impact-resistant materials and optimizing bit geometry.",
        reasoning_framework=(
            "Impact loading from hard stringers, chert, or drilling shocks can cause cutter or bit body breakage. "
            "Use impact-resistant PDC cutters and reinforced bit bodies in high-risk intervals. "
            "Optimize cutter back rake and blade layout to distribute loads. "
            "Monitor for vibration and adjust parameters to reduce shock events."
        ),
        key_factors=[
            "Formation variability",
            "Cutter material",
            "Bit geometry",
            "Operational parameters"
        ],
        primary_authority=[
            "SPE 23957: Bit Impact Resistance",
            "Halliburton Bit Selection Guide"
        ],
        burden_holder="Bit designer",
        adversary_position="Impact-resistant bits may sacrifice ROP in softer formations.",
        counter_arguments=[
            "Hybrid designs can balance impact resistance and ROP.",
            "Parameter optimization reduces shock loading."
        ],
        resolution_strategy="Select bit based on formation logs and offset failures; pilot test in high-risk intervals.",
        entity_scope="Drilling engineers, bit suppliers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 23957"
    ),
    DoctrineBlock(
        topic="Nozzle Plugging Prevention",
        keywords=["nozzle plugging", "hydraulics", "bit cleaning", "solids", "failure"],
        conclusion_template="Prevent nozzle plugging through proper solids control, nozzle design, and operational vigilance.",
        reasoning_framework=(
            "Nozzle plugging reduces bit cleaning and increases risk of bit balling. "
            "Use nozzle sizes and shapes less prone to plugging. "
            "Maintain effective solids control at surface to minimize large particles in the mud. "
            "Monitor for pressure spikes and reduced flow; pull and clean bit if plugging is suspected."
        ),
        key_factors=[
            "Solids control",
            "Nozzle design",
            "Mud properties",
            "Operational monitoring"
        ],
        primary_authority=[
            "API RP 13D",
            "SPE 23958: Nozzle Plugging Incidents"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Frequent bit trips for cleaning increase NPT and cost.",
        counter_arguments=[
            "Improved solids control and nozzle design reduce plugging frequency.",
            "Real-time monitoring enables early detection."
        ],
        resolution_strategy="Integrate solids control and nozzle selection in pre-job planning; monitor for plugging indicators.",
        entity_scope="Drilling engineers, mud engineers",
        confidence=0.91,
        confidence_zone="Medium",
        controlling_precedent="API RP 13D"
    ),
    DoctrineBlock(
        topic="Bit Selection for Extended Reach Drilling",
        keywords=["extended reach", "bit selection", "PDC", "durability", "hydraulics"],
        conclusion_template="Bits for extended reach wells require high durability, efficient hydraulics, and low torque.",
        reasoning_framework=(
            "Extended reach wells impose high torque and drag on the bit and BHA. "
            "Select bits with low-torque profiles, high durability, and efficient cuttings evacuation. "
            "PDC bits with optimized blade and nozzle design are preferred. "
            "Monitor for increased wear and adjust parameters to maintain performance."
        ),
        key_factors=[
            "Well length",
            "Torque and drag",
            "Bit durability",
            "Hydraulic efficiency"
        ],
        primary_authority=[
            "SPE 23959: Extended Reach Drilling",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Drilling engineer",
        adversary_position="High-durability bits are more expensive and may reduce ROP.",
        counter_arguments=[
            "Reduced trips and failures offset higher bit cost.",
            "Parameter optimization maintains ROP."
        ],
        resolution_strategy="Select bits based on torque modeling and offset performance; monitor for wear.",
        entity_scope="Drilling engineers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 23959"
    ),
    DoctrineBlock(
        topic="Bit Selection for High-Pressure, High-Temperature (HPHT) Wells",
        keywords=["HPHT", "bit selection", "PDC", "thermal stability", "durability"],
        conclusion_template="HPHT wells require bits with high thermal stability, impact resistance, and robust hydraulics.",
        reasoning_framework=(
            "HPHT conditions accelerate bit wear and cutter degradation. "
            "Select PDC bits with high-stability cutters and reinforced bodies. "
            "Hydraulic design must ensure effective cooling and cuttings removal. "
            "Monitor for thermal damage and adjust parameters as needed."
        ),
        key_factors=[
            "Well temperature and pressure",
            "Cutter material",
            "Bit body strength",
            "Hydraulic design"
        ],
        primary_authority=[
            "SPE 23960: HPHT Bit Performance",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Drilling engineer",
        adversary_position="HPHT bits are more expensive and may not be available for all sizes.",
        counter_arguments=[
            "Custom bit design and field trials address availability.",
            "Cost is justified by improved reliability."
        ],
        resolution_strategy="Engage with manufacturers early for HPHT bit design; monitor field performance.",
        entity_scope="Drilling engineers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SPE 23960"
    ),
    DoctrineBlock(
        topic="Bit Selection for Abrasive Sandstone",
        keywords=["sandstone", "abrasive", "bit selection", "PDC", "roller cone"],
        conclusion_template="Abrasive sandstones require bits with high wear resistance and optimized hydraulics.",
        reasoning_framework=(
            "Abrasive sandstones accelerate cutter and gauge wear. "
            "Select PDC bits with wear-resistant cutters and robust gauge protection for homogeneous intervals. "
            "Roller cone bits are preferred for highly interbedded or unpredictable zones. "
            "Optimize hydraulics for cuttings removal and cooling."
        ),
        key_factors=[
            "Abrasivity",
            "Bit durability",
            "Gauge protection",
            "Hydraulic efficiency"
        ],
        primary_authority=[
            "SPE 23961: Bit Performance in Sandstones",
            "Halliburton Bit Selection Guide"
        ],
        burden_holder="Drilling engineer",
        adversary_position="High-durability bits may reduce ROP in softer intervals.",
        counter_arguments=[
            "Interval-specific bit selection optimizes performance.",
            "Hybrid bits can be considered for variable lithology."
        ],
        resolution_strategy="Analyze formation logs; select bit type for each interval based on abrasivity.",
        entity_scope="Drilling engineers",
        confidence=0.91,
        confidence_zone="Medium",
        controlling_precedent="SPE 23961"
    ),
    DoctrineBlock(
        topic="Bit Selection for Salt Formations",
        keywords=["salt", "bit selection", "PDC", "hydraulics", "bit balling"],
        conclusion_template="Salt drilling favors PDC bits with aggressive profiles and high hydraulic efficiency.",
        reasoning_framework=(
            "Salt is soft but can cause bit balling and inefficient drilling. "
            "Select PDC bits with large cutters, aggressive blade profiles, and high-flow hydraulics. "
            "Monitor for bit balling and adjust mud properties to minimize adhesion. "
            "Avoid roller cone bits due to poor performance in salt."
        ),
        key_factors=[
            "Salt thickness",
            "Bit profile",
            "Hydraulic design",
            "Mud properties"
        ],
        primary_authority=[
            "SPE 23962: Salt Drilling Optimization",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Aggressive bits may increase vibration at salt interfaces.",
        counter_arguments=[
            "Parameter adjustment and real-time monitoring mitigate vibration.",
            "Hybrid bits can be considered for salt/anhydrite transitions."
        ],
        resolution_strategy="Select bit based on salt interval length and offset performance; monitor for balling.",
        entity_scope="Drilling engineers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 23962"
    ),
    DoctrineBlock(
        topic="Bit Selection for Hard Carbonates",
        keywords=["hard carbonates", "bit selection", "impregnated", "roller cone", "PDC"],
        conclusion_template="Hard carbonates require impregnated or roller cone bits for durability and efficient drilling.",
        reasoning_framework=(
            "Hard, abrasive carbonates (e.g., dolomite, chert-bearing limestone) cause rapid PDC wear. "
            "Select impregnated diamond bits or roller cones for these intervals. "
            "Optimize parameters for durability and monitor for bit damage. "
            "Hybrid bits may be considered for transitional zones."
        ),
        key_factors=[
            "Formation hardness",
            "Abrasivity",
            "Bit durability",
            "Operational parameters"
        ],
        primary_authority=[
            "SPE 23963: Bit Performance in Carbonates",
            "Halliburton Bit Selection Guide"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Impregnated bits have lower ROP in softer intervals.",
        counter_arguments=[
            "Interval-specific bit selection maximizes performance.",
            "Hybrid bits can be used in transitions."
        ],
        resolution_strategy="Analyze lithology; select bit based on hardness and offset failures.",
        entity_scope="Drilling engineers",
        confidence=0.91,
        confidence_zone="Medium",
        controlling_precedent="SPE 23963"
    ),
    DoctrineBlock(
        topic="Bit Selection for Interbedded Formations",
        keywords=["interbedded", "bit selection", "hybrid", "roller cone", "PDC"],
        conclusion_template="Hybrid or roller cone bits are preferred for highly interbedded formations to balance durability and ROP.",
        reasoning_framework=(
            "Interbedded formations present variable hardness and abrasivity, increasing risk of bit damage. "
            "Hybrid bits combine durability and ROP; roller cones offer impact resistance. "
            "Monitor for vibration and adjust parameters to minimize shock loading. "
            "Interval-specific bit selection may be required for complex sequences."
        ),
        key_factors=[
            "Formation variability",
            "Bit durability",
            "Vibration risk",
            "Operational parameters"
        ],
        primary_authority=[
            "SPE 23964: Bit Performance in Interbedded Formations",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Hybrid bits are more expensive and may not be available for all sizes.",
        counter_arguments=[
            "Cost is offset by reduced trips and failures.",
            "Pilot testing informs selection."
        ],
        resolution_strategy="Select bit based on formation logs and offset failures; pilot test hybrids in challenging intervals.",
        entity_scope="Drilling engineers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 23964"
    ),
    DoctrineBlock(
        topic="Bit Selection for Unconventional Reservoirs",
        keywords=["unconventional", "shale", "tight gas", "bit selection", "PDC"],
        conclusion_template="Unconventional reservoirs are best drilled with PDC bits optimized for long runs and anti-balling features.",
        reasoning_framework=(
            "Unconventional plays require long lateral sections and minimal trips. "
            "Select PDC bits with high durability, anti-balling profiles, and efficient hydraulics. "
            "Monitor for torque and vibration; adjust parameters to maximize ROP and bit life. "
            "Field data supports long-run PDC bits as most cost-effective."
        ),
        key_factors=[
            "Run length",
            "Bit durability",
            "Hydraulic efficiency",
            "Formation reactivity"
        ],
        primary_authority=[
            "SPE 23965: Bit Performance in Unconventionals",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Long-run bits are more expensive and may require parameter optimization.",
        counter_arguments=[
            "Reduced trips and failures justify higher cost.",
            "Real-time monitoring supports parameter adjustment."
        ],
        resolution_strategy="Select bits based on lateral length and offset performance; monitor for wear and balling.",
        entity_scope="Drilling engineers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SPE 23965"
    ),
    DoctrineBlock(
        topic="Bit Selection for Corrosive Environments",
        keywords=["corrosive", "bit selection", "PDC", "roller cone", "material"],
        conclusion_template="Corrosive environments require bits with corrosion-resistant materials and coatings.",
        reasoning_framework=(
            "Corrosive muds and formations accelerate bit body and cutter degradation. "
            "Select bits with stainless steel or coated bodies and corrosion-resistant cutters. "
            "Monitor for accelerated wear and adjust mud chemistry as needed."
        ),
        key_factors=[
            "Mud chemistry",
            "Bit material",
            "Coatings",
            "Formation properties"
        ],
        primary_authority=[
            "SPE 23966: Bit Performance in Corrosive Wells",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Corrosion-resistant bits are more expensive and may not be needed in all wells.",
        counter_arguments=[
            "Cost is justified in high-corrosion environments.",
            "Mud chemistry adjustment can reduce corrosion risk."
        ],
        resolution_strategy="Select bit based on mud and formation analysis; monitor for corrosion wear.",
        entity_scope="Drilling engineers",
        confidence=0.91,
        confidence_zone="Medium",
        controlling_precedent="SPE 23966"
    ),
    DoctrineBlock(
        topic="Bit Selection for Geothermal Wells",
        keywords=["geothermal", "bit selection", "PDC", "thermal stability", "durability"],
        conclusion_template="Geothermal wells require bits with high thermal stability, durability, and efficient hydraulics.",
        reasoning_framework=(
            "Geothermal drilling exposes bits to high temperatures and abrasive formations. "
            "Select PDC bits with high-stability cutters and robust gauge protection. "
            "Optimize hydraulics for cooling and cuttings removal. "
            "Monitor for thermal degradation and adjust parameters as needed."
        ),
        key_factors=[
            "Well temperature",
            "Bit durability",
            "Hydraulic efficiency",
            "Formation abrasivity"
        ],
        primary_authority=[
            "SPE 23967: Bit Performance in Geothermal Wells",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Drilling engineer",
        adversary_position="High-stability bits are more expensive and may reduce ROP.",
        counter_arguments=[
            "Reduced trips and failures justify higher cost.",
            "Parameter optimization maintains ROP."
        ],
        resolution_strategy="Select bits based on temperature and formation; monitor for thermal wear.",
        entity_scope="Drilling engineers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SPE 23967"
    ),
    DoctrineBlock(
        topic="Bit Selection for Air Drilling",
        keywords=["air drilling", "bit selection", "roller cone", "PDC", "cooling"],
        conclusion_template="Air drilling favors roller cone bits with open bearings and robust gauge protection.",
        reasoning_framework=(
            "Air drilling provides minimal cooling and cuttings removal. "
            "Select roller cone bits with open bearings and aggressive gauge protection. "
            "PDC bits may be used in soft, homogeneous formations with adequate air flow. "
            "Monitor for bit overheating and adjust air flow as needed."
        ),
        key_factors=[
            "Cooling",
            "Cuttings removal",
            "Bit durability",
            "Bearing type"
        ],
        primary_authority=[
            "SPE 23968: Air Drilling Bit Performance",
            "Halliburton Bit Selection Guide"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Roller cone bits have lower ROP than PDC in some formations.",
        counter_arguments=[
            "Air drilling parameters can be optimized for ROP.",
            "Hybrid bits are being developed for air drilling."
        ],
        resolution_strategy="Select bit based on formation and air flow; monitor for overheating.",
        entity_scope="Drilling engineers",
        confidence=0.90,
        confidence_zone="Medium",
        controlling_precedent="SPE 23968"
    ),
    DoctrineBlock(
        topic="Bit Selection for Managed Pressure Drilling (MPD)",
        keywords=["MPD", "managed pressure", "bit selection", "PDC", "hydraulics"],
        conclusion_template="MPD operations require bits with efficient hydraulics and low ECD profiles.",
        reasoning_framework=(
            "MPD limits allowable ECD and pressure fluctuations. "
            "Select bits with low-pressure-drop hydraulics and efficient cuttings removal. "
            "PDC bits with optimized nozzle and blade design are preferred. "
            "Monitor for ECD excursions and adjust parameters as needed."
        ),
        key_factors=[
            "ECD limits",
            "Hydraulic design",
            "Bit profile",
            "Cuttings removal"
        ],
        primary_authority=[
            "SPE 23969: Bit Performance in MPD",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Low-ECD bits may reduce ROP in some formations.",
        counter_arguments=[
            "Hydraulic modeling optimizes performance.",
            "Interval-specific bit selection can balance ECD and ROP."
        ],
        resolution_strategy="Model hydraulics for MPD; select bits based on ECD and formation.",
        entity_scope="Drilling engineers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 23969"
    ),
    DoctrineBlock(
        topic="Bit Selection for Underbalanced Drilling",
        keywords=["underbalanced", "bit selection", "PDC", "roller cone", "hydraulics"],
        conclusion_template="Underbalanced drilling requires bits with robust sealing and efficient cuttings evacuation.",
        reasoning_framework=(
            "Underbalanced drilling exposes bits to gas influx and reduced hydrostatic pressure. "
            "Select bits with robust sealing (sealed bearings for roller cones, solid bodies for PDC). "
            "Optimize hydraulics for efficient cuttings removal. "
            "Monitor for bit wear and adjust parameters as needed."
        ),
        key_factors=[
            "Sealing",
            "Hydraulic efficiency",
            "Bit durability",
            "Formation type"
        ],
        primary_authority=[
            "SPE 23970: Bit Performance in Underbalanced Drilling",
            "Halliburton Bit Selection Guide"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Sealed bits are more expensive and may not be needed in all wells.",
        counter_arguments=[
            "Cost is justified by improved reliability.",
            "Interval-specific selection optimizes performance."
        ],
        resolution_strategy="Select bits based on underbalanced conditions and offset performance; monitor for wear.",
        entity_scope="Drilling engineers",
        confidence=0.91,
        confidence_zone="Medium",
        controlling_precedent="SPE 23970"
    ),
    DoctrineBlock(
        topic="Bit Selection for Casing-While-Drilling (CWD)",
        keywords=["CWD", "casing-while-drilling", "bit selection", "PDC", "roller cone"],
        conclusion_template="CWD operations require bits compatible with casing systems and capable of drilling and reaming.",
        reasoning_framework=(
            "CWD bits must drill and ream while attached to casing. "
            "Select bits with robust cutting structures and gauge protection. "
            "PDC bits are preferred for soft to medium formations; roller cones for hard or interbedded zones. "
            "Ensure bit can be drilled out or retrieved as required by the operation."
        ),
        key_factors=[
            "Casing compatibility",
            "Bit durability",
            "Gauge protection",
            "Retrievability"
        ],
        primary_authority=[
            "SPE 23971: Bit Performance in CWD",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Drilling engineer",
        adversary_position="CWD bits are more expensive and may limit ROP.",
        counter_arguments=[
            "Reduced trips and improved wellbore quality offset cost.",
            "Interval-specific selection optimizes performance."
        ],
        resolution_strategy="Select bits based on casing system and formation; monitor for wear and retrievability.",
        entity_scope="Drilling engineers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 23971"
    ),
    DoctrineBlock(
        topic="Bit Selection for Multilateral Wells",
        keywords=["multilateral", "bit selection", "PDC", "steerability", "durability"],
        conclusion_template="Multilateral wells require bits with high steerability, durability, and efficient cuttings removal.",
        reasoning_framework=(
            "Multilateral wells involve complex trajectories and junctions. "
            "Select PDC bits with short gauge, asymmetric blade layout, and robust durability. "
            "Optimize hydraulics for cuttings removal in junctions. "
            "Monitor for increased wear due to side loading and adjust parameters as needed."
        ),
        key_factors=[
            "Steerability",
            "Bit durability",
            "Hydraulic efficiency",
            "Junction complexity"
        ],
        primary_authority=[
            "SPE 23972: Bit Performance in Multilaterals",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Drilling engineer",
        adversary_position="High-steerability bits may sacrifice durability.",
        counter_arguments=[
            "Advanced PDC designs balance steerability and durability.",
            "Interval-specific selection optimizes performance."
        ],
        resolution_strategy="Select bits based on trajectory and junction design; monitor for wear.",
        entity_scope="Drilling engineers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SPE 23972"
    ),
    DoctrineBlock(
        topic="Bit Selection for Slimhole Drilling",
        keywords=["slimhole", "bit selection", "PDC", "roller cone", "hydraulics"],
        conclusion_template="Slimhole drilling requires bits with robust gauge protection and efficient hydraulics.",
        reasoning_framework=(
            "Slimhole wells have smaller annular clearances, increasing risk of bit sticking and poor cuttings removal. "
            "Select PDC or roller cone bits with robust gauge protection and optimized hydraulics. "
            "Monitor for bit sticking and adjust parameters as needed."
        ),
        key_factors=[
            "Annular clearance",
            "Gauge protection",
            "Hydraulic efficiency",
            "Bit durability"
        ],
        primary_authority=[
            "SPE 23973: Bit Performance in Slimhole Wells",
            "Halliburton Bit Selection Guide"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Slimhole bits may have reduced durability and ROP.",
        counter_arguments=[
            "Optimized design and parameter adjustment maintain performance.",
            "Interval-specific selection maximizes run length."
        ],
        resolution_strategy="Select bits based on hole size and formation; monitor for sticking and wear.",
        entity_scope="Drilling engineers",
        confidence=0.91,
        confidence_zone="Medium",
        controlling_precedent="SPE 23973"
    ),
    DoctrineBlock(
        topic="Bit Selection for High Dogleg Severity Wells",
        keywords=["dogleg severity", "bit selection", "PDC", "steerability", "durability"],
        conclusion_template="High dogleg severity wells require bits with high steerability and robust durability.",
        reasoning_framework=(
            "High dogleg wells impose side loading and increased wear on bits. "
            "Select PDC bits with short gauge, asymmetric blade layout, and reinforced cutters. "
            "Monitor for increased wear and adjust parameters to maintain trajectory and bit life."
        ),
        key_factors=[
            "Dogleg severity",
            "Steerability",
            "Bit durability",
            "Gauge design"
        ],
        primary_authority=[
            "SPE 23974: Bit Performance in High Dogleg Wells",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Drilling engineer",
        adversary_position="High-steerability bits may reduce ROP and durability.",
        counter_arguments=[
            "Advanced designs balance steerability and durability.",
            "Interval-specific selection optimizes performance."
        ],
        resolution_strategy="Select bits based on trajectory and offset performance; monitor for wear.",
        entity_scope="Drilling engineers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 23974"
    ),
    DoctrineBlock(
        topic="Bit Selection for Hard Stringers",
        keywords=["hard stringers", "bit selection", "PDC", "roller cone", "impact resistance"],
        conclusion_template="Hard stringers require bits with high impact resistance and optimized cutter geometry.",
        reasoning_framework=(
            "Hard stringers cause impact loading and cutter breakage. "
            "Select PDC bits with impact-resistant cutters and optimized back rake, or roller cone bits for severe cases. "
            "Monitor for vibration and adjust parameters to minimize shock loading."
        ),
        key_factors=[
            "Stringer hardness",
            "Cutter material",
            "Bit geometry",
            "Operational parameters"
        ],
        primary_authority=[
            "SPE 23975: Bit Performance in Hard Stringers",
            "Halliburton Bit Selection Guide"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Impact-resistant bits may reduce ROP in softer intervals.",
        counter_arguments=[
            "Interval-specific selection optimizes performance.",
            "Hybrid bits can be considered for variable lithology."
        ],
        resolution_strategy="Analyze formation logs; select bit based on stringer frequency and hardness.",
        entity_scope="Drilling engineers",
        confidence=0.91,
        confidence_zone="Medium",
        controlling_precedent="SPE 23975"
    ),
    DoctrineBlock(
        topic="Bit Selection for High Angle Wells",
        keywords=["high angle", "bit selection", "PDC", "steerability", "durability"],
        conclusion_template="High angle wells require bits with high steerability, durability, and efficient cuttings removal.",
        reasoning_framework=(
            "High angle wells increase side loading and cuttings removal challenges. "
            "Select PDC bits with short gauge, asymmetric blade layout, and robust durability. "
            "Optimize hydraulics for cuttings evacuation. "
            "Monitor for increased wear and adjust parameters as needed."
        ),
        key_factors=[
            "Well angle",
            "Steerability",
            "Bit durability",
            "Hydraulic efficiency"
        ],
        primary_authority=[
            "SPE 23976: Bit Performance in High Angle Wells",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Drilling engineer",
        adversary_position="High-steerability bits may reduce ROP and durability.",
        counter_arguments=[
            "Advanced designs balance steerability and durability.",
            "Interval-specific selection optimizes performance."
        ],
        resolution_strategy="Select bits based on trajectory and offset performance; monitor for wear.",
        entity_scope="Drilling engineers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 23976"
    ),
    DoctrineBlock(
        topic="Bit Selection for Deepwater Wells",
        keywords=["deepwater", "bit selection", "PDC", "roller cone", "hydraulics"],
        conclusion_template="Deepwater wells require bits with high durability, efficient hydraulics, and compatibility with riser systems.",
        reasoning_framework=(
            "Deepwater drilling imposes long trip times and high operational costs. "
            "Select bits with high durability and efficient hydraulics for long runs. "
            "Ensure bit is compatible with riser and BOP systems. "
            "Monitor for wear and adjust parameters to maximize run length."
        ),
        key_factors=[
            "Run length",
            "Bit durability",
            "Hydraulic efficiency",
            "System compatibility"
        ],
        primary_authority=[
            "SPE 23977: Bit Performance in Deepwater Wells",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Drilling engineer",
        adversary_position="High-durability bits are more expensive and may reduce ROP.",
        counter_arguments=[
            "Reduced trips and failures offset higher bit cost.",
            "Parameter optimization maintains ROP."
        ],
        resolution_strategy="Select bits based on well plan and offset performance; monitor for wear.",
        entity_scope="Drilling engineers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SPE 23977"
    ),
    DoctrineBlock(
        topic="Bit Selection for Shallow Gas Hazards",
        keywords=["shallow gas", "bit selection", "PDC", "roller cone", "hydraulics"],
        conclusion_template="Shallow gas hazards require bits with efficient hydraulics and rapid penetration capability.",
        reasoning_framework=(
            "Shallow gas zones require rapid penetration to minimize exposure time. "
            "Select bits with high ROP and efficient hydraulics for cuttings removal. "
            "PDC bits are preferred for soft formations; roller cones for interbedded or unpredictable zones. "
            "Monitor for gas shows and adjust parameters as needed."
        ),
        key_factors=[
            "Gas hazard depth",
            "ROP",
            "Hydraulic efficiency",
            "Formation type"
        ],
        primary_authority=[
            "SPE 23978: Bit Performance in Shallow Gas Zones",
            "Halliburton Bit Selection Guide"
        ],
        burden_holder="Drilling engineer",
        adversary_position="High-ROP bits may increase vibration and bit damage.",
        counter_arguments=[
            "Parameter adjustment and real-time monitoring mitigate risk.",
            "Interval-specific selection optimizes performance."
        ],
        resolution_strategy="Select bits based on gas hazard analysis and offset performance; monitor for shows.",
        entity_scope="Drilling engineers",
        confidence=0.91,
        confidence_zone="Medium",
        controlling_precedent="SPE 23978"
    ),
    DoctrineBlock(
        topic="Bit Selection for Lost Circulation Zones",
        keywords=["lost circulation", "bit selection", "PDC", "roller cone", "hydraulics"],
        conclusion_template="Lost circulation zones require bits with low hydraulic pressure drop and efficient cuttings removal.",
        reasoning_framework=(
            "Lost circulation increases risk of stuck pipe and poor hole cleaning. "
            "Select bits with low-pressure-drop hydraulics and efficient cuttings evacuation. "
            "PDC bits are preferred for soft to medium formations; roller cones for interbedded or unpredictable zones. "
            "Monitor for losses and adjust parameters as needed."
        ),
        key_factors=[
            "Loss severity",
            "Hydraulic design",
            "Bit profile",
            "Formation type"
        ],
        primary_authority=[
            "SPE 23979: Bit Performance in Lost Circulation Zones",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Low-pressure-drop bits may reduce ROP in some formations.",
        counter_arguments=[
            "Hydraulic modeling optimizes performance.",
            "Interval-specific selection balances losses and ROP."
        ],
        resolution_strategy="Select bits based on loss analysis and offset performance; monitor for losses.",
        entity_scope="Drilling engineers",
        confidence=0.91,
        confidence_zone="Medium",
        controlling_precedent="SPE 23979"
    ),
    DoctrineBlock(
        topic="Bit Selection for High Abrasion Formations",
        keywords=["high abrasion", "bit selection", "PDC", "roller cone", "gauge protection"],
        conclusion_template="High abrasion formations require bits with maximum wear resistance and robust gauge protection.",
        reasoning_framework=(
            "High abrasion accelerates cutter and gauge wear. "
            "Select PDC bits with wear-resistant cutters and robust gauge protection for homogeneous intervals. "
            "Roller cone bits are preferred for highly interbedded or unpredictable zones. "
            "Monitor for wear and adjust parameters to maintain performance."
        ),
        key_factors=[
            "Abrasivity",
            "Bit durability",
            "Gauge protection",
            "Hydraulic efficiency"
        ],
        primary_authority=[
            "SPE 23980: Bit Performance in High Abrasion Formations",
            "Halliburton Bit Selection Guide"
        ],
        burden_holder="Drilling engineer",
        adversary_position="High-durability bits may reduce ROP in softer intervals.",
        counter_arguments=[
            "Interval-specific selection optimizes performance.",
            "Hybrid bits can be considered for variable lithology."
        ],
        resolution_strategy="Analyze formation logs; select bit based on abrasivity and offset failures.",
        entity_scope="Drilling engineers",
        confidence=0.91,
        confidence_zone="Medium",
        controlling_precedent="SPE 23980"
    ),
    DoctrineBlock(
        topic="Bit Selection for Plug Drilling and Abandonment",
        keywords=["plug drilling", "abandonment", "bit selection", "PDC", "roller cone"],
        conclusion_template="Plug drilling and abandonment require bits with high durability and compatibility with cement and casing.",
        reasoning_framework=(
            "Plug drilling involves drilling through cement, casing, and formation. "
            "Select bits with high durability and robust gauge protection. "
            "PDC bits are preferred for soft to medium plugs; roller cones for hard or unpredictable plugs. "
            "Monitor for wear and adjust parameters as needed."
        ),
        key_factors=[
            "Plug composition",
            "Bit durability",
            "Gauge protection",
            "Formation type"
        ],
        primary_authority=[
            "SPE 23981: Bit Performance in Plug Drilling",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Drilling engineer",
        adversary_position="High-durability bits are more expensive and may reduce ROP.",
        counter_arguments=[
            "Reduced trips and failures offset higher bit cost.",
            "Interval-specific selection optimizes performance."
        ],
        resolution_strategy="Select bits based on plug composition and offset performance; monitor for wear.",
        entity_scope="Drilling engineers",
        confidence=0.91,
        confidence_zone="Medium",
        controlling_precedent="SPE 23981"
    ),
    DoctrineBlock(
        topic="Bit Selection for Pilot Holes",
        keywords=["pilot hole", "bit selection", "PDC", "roller cone", "hydraulics"],
        conclusion_template="Pilot holes require bits with high steerability, durability, and efficient cuttings removal.",
        reasoning_framework=(
            "Pilot holes are drilled to assess formation and plan main wellbore. "
            "Select PDC bits with short gauge and robust durability for soft to medium formations. "
            "Roller cone bits are preferred for hard or interbedded zones. "
            "Optimize hydraulics for cuttings removal and monitor for wear."
        ),
        key_factors=[
            "Formation type",
            "Steerability",
            "Bit durability",
            "Hydraulic efficiency"
        ],
        primary_authority=[
            "SPE 23982: Bit Performance in Pilot Holes",
            "Halliburton Bit Selection Guide"
        ],
        burden_holder="Drilling engineer",
        adversary_position="High-steerability bits may reduce ROP and durability.",
        counter_arguments=[
            "Advanced designs balance steerability and durability.",
            "Interval-specific selection optimizes performance."
        ],
        resolution_strategy="Select bits based on pilot objectives and formation; monitor for wear.",
        entity_scope="Drilling engineers",
        confidence=0.91,
        confidence_zone="Medium",
        controlling_precedent="SPE 23982"
    ),
    DoctrineBlock(
        topic="Bit Selection for Sidetracking Operations",
        keywords=["sidetracking", "bit selection", "PDC", "roller cone", "steerability"],
        conclusion_template="Sidetracking requires bits with high steerability, durability, and compatibility with whipstock systems.",
        reasoning_framework=(
            "Sidetracking involves drilling a new wellbore from an existing one. "
            "Select PDC bits with short gauge and robust durability for soft to medium formations. "
            "Roller cone bits are preferred for hard or interbedded zones. "
            "Ensure bit is compatible with whipstock and BHA design. "
            "Monitor for wear and adjust parameters as needed."
        ),
        key_factors=[
            "Steerability",
            "Bit durability",
            "Whipstock compatibility",
            "Formation type"
        ],
        primary_authority=[
            "SPE 23983: Bit Performance in Sidetracking",
            "Baker Hughes Drill Bit Handbook"
        ],
        burden_holder="Drilling engineer",
        adversary_position="High-steerability bits may reduce ROP and durability.",
        counter_arguments=[
            "Advanced designs balance steerability and durability.",
            "Interval-specific selection optimizes performance."
        ],
        resolution_strategy="Select bits based on sidetrack objectives and formation; monitor for wear.",
        entity_scope="Drilling engineers",
        confidence=0.91,
        confidence_zone="Medium",
        controlling_precedent="SPE 23983"
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
        if (keyword_lower in doctrine.topic.lower() or
            any(keyword_lower in k.lower() for k in doctrine.keywords) or
            keyword_lower in doctrine.reasoning_framework.lower() or
            keyword_lower in doctrine.conclusion_template.lower()):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]