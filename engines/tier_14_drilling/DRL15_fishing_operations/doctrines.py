from dataclasses import dataclass, field
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
        topic="Differential Sticking Mechanism",
        keywords=["differential sticking", "stuck pipe", "borehole", "mud weight", "formation pressure"],
        conclusion_template="Differential sticking occurs when the drill string is forced against the permeable formation due to overbalanced mud pressure.",
        reasoning_framework="""
1. Evaluate the pressure differential between the wellbore and the formation.
2. Assess the contact area and duration between the drill string and the permeable zone.
3. Consider the mud properties, especially filter cake quality and thickness.
4. Analyze the well trajectory for inclination and doglegs that may increase sticking risk.
5. Review operational parameters such as overpull, torque, and circulation loss.
6. Cross-reference with offset well data for similar sticking events.
7. Conclude if the observed symptoms match the differential sticking profile.
""",
        key_factors=[
            "Mud overbalance",
            "Filter cake integrity",
            "Pipe contact duration",
            "Formation permeability",
            "Wellbore geometry"
        ],
        primary_authority=[
            "API RP 10B-2",
            "SPE 20432",
            "Bourgoyne et al., Applied Drilling Engineering"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Mechanical sticking is the primary cause, not differential.",
        counter_arguments=[
            "No significant overbalance observed.",
            "Pipe was not stationary for extended periods.",
            "Filter cake was properly conditioned."
        ],
        resolution_strategy="Validate with pressure logs, pipe movement history, and mud reports.",
        entity_scope="Drilling Operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="SPE 20432"
    ),
    DoctrineBlock(
        topic="Mechanical Pipe Sticking Diagnosis",
        keywords=["mechanical sticking", "bridging", "wellbore collapse", "drill string"],
        conclusion_template="Mechanical sticking is diagnosed when physical obstructions or borehole instability prevent pipe movement.",
        reasoning_framework="""
1. Review drilling logs for signs of wellbore collapse, sloughing, or bridging.
2. Analyze torque and drag trends for sudden increases.
3. Inspect cuttings for cavings or large fragments.
4. Compare stuck depth with known unstable formations.
5. Evaluate hole cleaning efficiency and annular velocities.
6. Consider tripping speed and swab/surge effects.
7. Rule out differential sticking through pressure analysis.
8. Confirm diagnosis with caliper logs and downhole imaging if available.
""",
        key_factors=[
            "Wellbore stability",
            "Hole cleaning",
            "Formation type",
            "Tripping speed",
            "Cuttings analysis"
        ],
        primary_authority=[
            "API RP 13B-1",
            "SPE 20432",
            "Mitchell, Practical Wellbore Hydraulics and Hole Cleaning"
        ],
        burden_holder="Wellsite Geologist",
        adversary_position="Sticking is due to differential pressure, not mechanical causes.",
        counter_arguments=[
            "No evidence of borehole collapse.",
            "Cuttings are normal.",
            "No tripping events prior to sticking."
        ],
        resolution_strategy="Correlate stuck depth with formation logs and cuttings analysis.",
        entity_scope="Drilling Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1"
    ),
    DoctrineBlock(
        topic="Free Point Determination Methods",
        keywords=["free point", "stuck pipe", "wireline", "free point indicator", "pipe stretch"],
        conclusion_template="The free point is determined by measuring pipe stretch response to applied surface force using wireline tools.",
        reasoning_framework="""
1. Deploy a wireline free point indicator tool to the suspected stuck interval.
2. Apply incremental overpull and record pipe stretch at various depths.
3. Identify the depth where pipe stretch ceases, indicating the stuck point.
4. Cross-verify with surface hookload readings and torque data.
5. Consider tool calibration and environmental corrections.
6. Document findings for fishing tool selection and backoff planning.
""",
        key_factors=[
            "Accurate depth correlation",
            "Tool calibration",
            "Surface overpull measurement",
            "Pipe stretch response",
            "Environmental corrections"
        ],
        primary_authority=[
            "API RP 7G",
            "SPE 20432",
            "Schlumberger Oilfield Glossary"
        ],
        burden_holder="Wireline Engineer",
        adversary_position="Surface measurements are sufficient without wireline intervention.",
        counter_arguments=[
            "Surface readings can be ambiguous.",
            "Wireline tools may not reach the stuck interval.",
            "Environmental factors may affect readings."
        ],
        resolution_strategy="Combine wireline and surface data for highest accuracy.",
        entity_scope="Fishing Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 7G"
    ),
    DoctrineBlock(
        topic="Hydraulic vs Mechanical Jar Selection",
        keywords=["fishing jars", "hydraulic jar", "mechanical jar", "impact force", "stuck pipe"],
        conclusion_template="Hydraulic jars are preferred for deeper, deviated wells requiring controlled impact; mechanical jars suit shallow, straight holes.",
        reasoning_framework="""
1. Assess well depth and deviation to determine jar type suitability.
2. Evaluate the need for controlled impact timing (hydraulic) versus immediate action (mechanical).
3. Consider downhole temperature and pressure effects on jar performance.
4. Review past jar performance in similar wells.
5. Factor in BHA length and jar placement constraints.
6. Select jar type based on operational objectives and risk profile.
""",
        key_factors=[
            "Well depth",
            "Hole deviation",
            "Impact control",
            "Temperature/pressure",
            "BHA configuration"
        ],
        primary_authority=[
            "API RP 7G",
            "Weatherford Jar Selection Guide",
            "SPE 20432"
        ],
        burden_holder="Fishing Tool Specialist",
        adversary_position="Mechanical jars are always sufficient regardless of well conditions.",
        counter_arguments=[
            "Hydraulic jars may fail at high temperatures.",
            "Mechanical jars are simpler and more reliable.",
            "Hydraulic jars add cost and complexity."
        ],
        resolution_strategy="Match jar type to well profile and operational requirements.",
        entity_scope="Fishing Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Weatherford Jar Selection Guide"
    ),
    DoctrineBlock(
        topic="Jar Placement Engineering",
        keywords=["jar placement", "BHA design", "fishing assembly", "impact force", "stuck pipe"],
        conclusion_template="Jars should be placed above the stuck point with sufficient free pipe above to maximize impact efficiency.",
        reasoning_framework="""
1. Determine the free point using wireline or surface methods.
2. Calculate the required free pipe length above the jar for optimal acceleration.
3. Avoid placing jars in compression zones or near heavy BHA components.
4. Consider well deviation and dogleg severity for jar effectiveness.
5. Review manufacturer's guidelines for jar placement.
6. Simulate jar impact using BHA modeling software.
7. Adjust placement based on fishing tool configuration and operational constraints.
""",
        key_factors=[
            "Free pipe length",
            "BHA configuration",
            "Well deviation",
            "Compression/tension zones",
            "Manufacturer guidelines"
        ],
        primary_authority=[
            "Weatherford Jar Placement Manual",
            "API RP 7G",
            "SPE 20432"
        ],
        burden_holder="Fishing Engineer",
        adversary_position="Jars can be placed anywhere in the string.",
        counter_arguments=[
            "Limited space in BHA restricts placement.",
            "Well deviation reduces jar effectiveness.",
            "Compression zones may damage jars."
        ],
        resolution_strategy="Model jar placement and validate with field experience.",
        entity_scope="Fishing Operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Weatherford Jar Placement Manual"
    ),
    DoctrineBlock(
        topic="Overshot vs Spear Selection Criteria",
        keywords=["overshot", "spear", "fishing tool", "fish engagement", "stuck pipe"],
        conclusion_template="Overshots are preferred for external engagement of tubulars; spears are used for internal engagement when the fish ID is accessible.",
        reasoning_framework="""
1. Identify the fish type, size, and condition (tubular, drill pipe, casing, etc.).
2. Assess accessibility of the fish's internal and external profiles.
3. Evaluate the presence of obstructions, deformation, or upsets.
4. Consider the risk of further damaging the fish.
5. Review prior fishing attempts and tool compatibility.
6. Select overshot for external engagement or spear for internal, based on fish accessibility.
""",
        key_factors=[
            "Fish profile and condition",
            "Internal/external accessibility",
            "Obstructions or deformation",
            "Tool compatibility",
            "Risk of further damage"
        ],
        primary_authority=[
            "NOV Fishing Tools Handbook",
            "API RP 7G",
            "SPE 20432"
        ],
        burden_holder="Fishing Supervisor",
        adversary_position="Spears are always preferable due to positive engagement.",
        counter_arguments=[
            "Fish ID may be damaged or inaccessible.",
            "Overshot provides better control for external engagement.",
            "Spear may split thin-walled fish."
        ],
        resolution_strategy="Inspect fish with calipers or imaging tools before selection.",
        entity_scope="Fishing Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NOV Fishing Tools Handbook"
    ),
    DoctrineBlock(
        topic="Washover Pipe Operations",
        keywords=["washover pipe", "fishing", "stuck pipe", "cutting", "circulation"],
        conclusion_template="Washover pipe is used to cut around and free stuck tubulars by circulating fluid and removing debris.",
        reasoning_framework="""
1. Select washover pipe size to match the fish OD with clearance for circulation.
2. Assemble washover string with appropriate shoes and stabilizers.
3. Run washover pipe to the stuck interval, maintaining circulation to remove cuttings.
4. Monitor torque, drag, and fluid returns for signs of progress.
5. Avoid excessive weight or rotation to prevent pipe damage.
6. Retrieve washover pipe and assess fish condition for further operations.
""",
        key_factors=[
            "Fish OD and length",
            "Circulation rate",
            "Shoe design",
            "Debris removal efficiency",
            "Torque and drag monitoring"
        ],
        primary_authority=[
            "Baker Hughes Fishing Handbook",
            "API RP 7G",
            "SPE 20432"
        ],
        burden_holder="Fishing Supervisor",
        adversary_position="Washover is unnecessary; direct pulling is sufficient.",
        counter_arguments=[
            "Debris may prevent direct pulling.",
            "Washover reduces risk of damaging fish.",
            "Direct pulling may part the string."
        ],
        resolution_strategy="Attempt washover before aggressive pulling.",
        entity_scope="Fishing Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Baker Hughes Fishing Handbook"
    ),
    DoctrineBlock(
        topic="Junk Mill vs Section Mill Selection",
        keywords=["junk mill", "section mill", "milling", "fish removal", "casing cutting"],
        conclusion_template="Junk mills are used for milling small obstructions; section mills are for cutting and removing casing sections.",
        reasoning_framework="""
1. Identify the type and size of the obstruction or casing to be removed.
2. Assess wellbore access and BHA limitations.
3. Evaluate the need for fullbore access after milling.
4. Consider the risk of damaging the wellbore or adjacent strings.
5. Select junk mill for small, hard obstructions or section mill for casing removal.
6. Review manufacturer's guidelines for mill selection.
""",
        key_factors=[
            "Obstruction type and size",
            "Wellbore access",
            "BHA limitations",
            "Fullbore access requirement",
            "Risk of collateral damage"
        ],
        primary_authority=[
            "Smith Bits Milling Guide",
            "API RP 7G",
            "SPE 20432"
        ],
        burden_holder="Fishing Engineer",
        adversary_position="Junk mills can remove all obstructions, including casing.",
        counter_arguments=[
            "Section mills are designed for casing removal.",
            "Junk mills may not cut full casing wall.",
            "Improper mill selection can damage wellbore."
        ],
        resolution_strategy="Match mill type to obstruction and operational objective.",
        entity_scope="Fishing Operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Smith Bits Milling Guide"
    ),
    DoctrineBlock(
        topic="Milling Parameters Optimization",
        keywords=["milling parameters", "RPM", "WOB", "fluid circulation", "BHA vibration"],
        conclusion_template="Optimal milling parameters balance rate of penetration, tool life, and wellbore integrity.",
        reasoning_framework="""
1. Review manufacturer's recommended RPM and WOB for the selected mill.
2. Adjust parameters based on real-time torque, vibration, and temperature data.
3. Monitor cuttings size and returns for milling efficiency.
4. Avoid excessive WOB or RPM to prevent BHA failure.
5. Optimize fluid circulation for cooling and debris removal.
6. Continuously adjust based on downhole feedback and surface measurements.
""",
        key_factors=[
            "Manufacturer recommendations",
            "Real-time drilling data",
            "Cuttings analysis",
            "Fluid circulation rate",
            "BHA vibration monitoring"
        ],
        primary_authority=[
            "Smith Bits Milling Guide",
            "API RP 7G",
            "SPE 20432"
        ],
        burden_holder="Drilling Supervisor",
        adversary_position="Maximum RPM and WOB always yield best results.",
        counter_arguments=[
            "Excessive parameters reduce tool life.",
            "High RPM increases vibration risk.",
            "Optimal parameters depend on downhole conditions."
        ],
        resolution_strategy="Monitor and adjust parameters in real time.",
        entity_scope="Drilling/Fishing Operations",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="Smith Bits Milling Guide"
    ),
    DoctrineBlock(
        topic="Wireline Fishing Tools and Techniques",
        keywords=["wireline", "fishing", "retrieval", "overshot", "fishing spear", "impression block"],
        conclusion_template="Wireline fishing tools are used for retrieving small, non-tubular objects and diagnosing fish orientation.",
        reasoning_framework="""
1. Assess the size, shape, and material of the fish.
2. Select appropriate wireline tools (overshot, spear, magnet, impression block).
3. Run impression block to determine fish orientation and top profile.
4. Attempt retrieval with overshot or spear, adjusting tool size as needed.
5. Use magnets for ferrous objects and baskets for debris.
6. Document each run and adjust technique based on results.
""",
        key_factors=[
            "Fish size and material",
            "Fish orientation",
            "Tool selection",
            "Wellbore access",
            "Impression block results"
        ],
        primary_authority=[
            "Schlumberger Wireline Catalog",
            "API RP 7G",
            "SPE 20432"
        ],
        burden_holder="Wireline Engineer",
        adversary_position="Wireline fishing is ineffective for most downhole objects.",
        counter_arguments=[
            "Wireline is limited by fish size.",
            "Some objects require mechanical fishing.",
            "Wireline provides valuable diagnostic data."
        ],
        resolution_strategy="Use wireline for diagnostics and small object retrieval.",
        entity_scope="Fishing Operations",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="Schlumberger Wireline Catalog"
    ),
    DoctrineBlock(
        topic="String Shot Backoff Procedures",
        keywords=["string shot", "backoff", "stuck pipe", "explosive severance", "fishing"],
        conclusion_template="String shot backoff is performed at a free point to sever the pipe and enable fish retrieval.",
        reasoning_framework="""
1. Determine the free point using wireline or mechanical methods.
2. Select the appropriate string shot charge for pipe size and grade.
3. Run the string shot to the backoff depth and set up surface safety protocols.
4. Detonate the charge and confirm severance with wireline or surface indicators.
5. Retrieve the upper string and prepare for fishing operations.
6. Document the operation and review for lessons learned.
""",
        key_factors=[
            "Accurate free point determination",
            "Charge selection",
            "Safety protocols",
            "Severance confirmation",
            "Post-backoff fishing plan"
        ],
        primary_authority=[
            "API RP 7G",
            "Schlumberger Wireline Catalog",
            "SPE 20432"
        ],
        burden_holder="Wireline Engineer",
        adversary_position="Mechanical backoff is safer and more reliable.",
        counter_arguments=[
            "String shot is faster and more precise.",
            "Mechanical backoff may not work if threads are damaged.",
            "Explosives require strict safety protocols."
        ],
        resolution_strategy="Use string shot when mechanical backoff is not feasible.",
        entity_scope="Fishing Operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 7G"
    ),
    DoctrineBlock(
        topic="Fish vs Sidetrack Economics",
        keywords=["fishing", "sidetrack", "cost analysis", "risk assessment", "well economics"],
        conclusion_template="Sidetracking is justified when fishing costs and risks exceed the value of the original wellbore.",
        reasoning_framework="""
1. Estimate the cost and probability of fishing success based on historical data.
2. Calculate the cost and time required for sidetracking.
3. Assess the value of the remaining reserves in the original wellbore.
4. Factor in operational risks, NPT, and lost production.
5. Compare total costs, risks, and time for both options.
6. Select the option with the highest expected value and lowest risk.
""",
        key_factors=[
            "Fishing success probability",
            "Sidetrack cost and time",
            "Remaining reserves value",
            "Operational risk",
            "NPT and lost production"
        ],
        primary_authority=[
            "API Bulletin D20",
            "SPE 20432",
            "Bourgoyne et al., Applied Drilling Engineering"
        ],
        burden_holder="Drilling Superintendent",
        adversary_position="Fishing should always be attempted regardless of cost.",
        counter_arguments=[
            "Sidetracking may access better reserves.",
            "Fishing success rates are low in similar wells.",
            "Extended NPT increases overall cost."
        ],
        resolution_strategy="Conduct a detailed economic and risk analysis.",
        entity_scope="Project Management",
        confidence=0.87,
        confidence_zone="Moderate",
        controlling_precedent="API Bulletin D20"
    ),
    DoctrineBlock(
        topic="Whipstock Sidetrack Operations",
        keywords=["whipstock", "sidetrack", "window milling", "deviation", "wellbore"],
        conclusion_template="Whipstock sidetracking is used to create a new wellbore path when the original is inaccessible.",
        reasoning_framework="""
1. Select whipstock type (mechanical or hydraulic) based on well conditions.
2. Set whipstock at the planned kickoff point and anchor securely.
3. Mill a window in the casing using a window mill and follow with a watermelon mill.
4. Monitor deviation and dogleg severity during sidetrack.
5. Maintain wellbore stability with proper mud properties.
6. Survey the new wellbore path and adjust as needed.
7. Document the operation for future reference.
""",
        key_factors=[
            "Whipstock selection",
            "Kickoff point",
            "Window milling technique",
            "Wellbore stability",
            "Survey accuracy"
        ],
        primary_authority=[
            "Baker Hughes Whipstock Manual",
            "API RP 7G",
            "SPE 20432"
        ],
        burden_holder="Directional Driller",
        adversary_position="Sidetracking can be done without whipstock.",
        counter_arguments=[
            "Whipstock provides controlled deviation.",
            "Window milling without whipstock is less precise.",
            "Mechanical whipstock is more reliable in cased hole."
        ],
        resolution_strategy="Use whipstock for controlled, precise sidetracking.",
        entity_scope="Drilling Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Baker Hughes Whipstock Manual"
    ),
    DoctrineBlock(
        topic="Differential Sticking Prevention",
        keywords=["differential sticking", "prevention", "mud weight", "pipe movement", "filter cake"],
        conclusion_template="Prevent differential sticking by minimizing overbalance, maintaining pipe movement, and conditioning mud.",
        reasoning_framework="""
1. Monitor and control mud weight to minimize overbalance.
2. Maintain continuous pipe movement during connections and trips.
3. Condition mud to build a thin, impermeable filter cake.
4. Avoid prolonged static periods, especially across permeable zones.
5. Use lubricants and spotting fluids as preventive measures.
6. Train crews to recognize early signs of sticking.
""",
        key_factors=[
            "Mud weight control",
            "Pipe movement",
            "Filter cake quality",
            "Lubricant use",
            "Crew training"
        ],
        primary_authority=[
            "API RP 13B-1",
            "SPE 20432",
            "Bourgoyne et al., Applied Drilling Engineering"
        ],
        burden_holder="Drilling Supervisor",
        adversary_position="Differential sticking is unavoidable in some formations.",
        counter_arguments=[
            "Proper mud conditioning reduces risk.",
            "Continuous pipe movement is effective.",
            "Spotting fluids can free stuck pipe."
        ],
        resolution_strategy="Implement best practices and monitor for early warning signs.",
        entity_scope="Drilling Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1"
    ),
    DoctrineBlock(
        topic="Key Seat Prevention Strategies",
        keywords=["key seat", "dogleg", "hole cleaning", "drill string", "stuck pipe"],
        conclusion_template="Prevent key seats by minimizing doglegs, using proper stabilizers, and effective hole cleaning.",
        reasoning_framework="""
1. Plan well trajectory to minimize dogleg severity.
2. Use string and near-bit stabilizers to centralize the BHA.
3. Maintain adequate annular velocity for effective hole cleaning.
4. Monitor for early signs of torque increase or drag.
5. Ream tight spots and backream as necessary.
6. Train crews on key seat recognition and prevention.
""",
        key_factors=[
            "Dogleg severity",
            "Stabilizer placement",
            "Hole cleaning efficiency",
            "Torque and drag monitoring",
            "Crew training"
        ],
        primary_authority=[
            "API RP 7G",
            "SPE 20432",
            "Mitchell, Practical Wellbore Hydraulics and Hole Cleaning"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Key seats are inevitable in directional wells.",
        counter_arguments=[
            "Proper BHA design reduces risk.",
            "Effective hole cleaning prevents cuttings accumulation.",
            "Backreaming eliminates tight spots."
        ],
        resolution_strategy="Design well path and BHA for minimal key seat risk.",
        entity_scope="Drilling Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 7G"
    ),
    DoctrineBlock(
        topic="Fishing Job Risk Assessment and Planning",
        keywords=["fishing job", "risk assessment", "contingency planning", "NPT", "HSE"],
        conclusion_template="Comprehensive risk assessment and contingency planning are essential for successful fishing operations.",
        reasoning_framework="""
1. Identify all potential hazards and failure points in the fishing operation.
2. Assess the likelihood and consequence of each risk.
3. Develop contingency plans for high-risk scenarios.
4. Allocate resources and personnel for critical tasks.
5. Review historical fishing job data for lessons learned.
6. Communicate the risk plan to all stakeholders.
7. Update risk assessment as the operation progresses.
""",
        key_factors=[
            "Hazard identification",
            "Risk likelihood and consequence",
            "Contingency planning",
            "Resource allocation",
            "Stakeholder communication"
        ],
        primary_authority=[
            "API RP 75",
            "SPE 20432",
            "Company HSE Manual"
        ],
        burden_holder="Fishing Supervisor",
        adversary_position="Risk assessment is unnecessary for routine fishing jobs.",
        counter_arguments=[
            "Unexpected events can escalate rapidly.",
            "Contingency planning reduces NPT.",
            "HSE compliance requires risk assessment."
        ],
        resolution_strategy="Conduct formal risk assessment before all fishing jobs.",
        entity_scope="Fishing Operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 75"
    ),
    DoctrineBlock(
        topic="Fishing Tool Safety Joint Application",
        keywords=["safety joint", "fishing tool", "BHA", "emergency release", "stuck pipe"],
        conclusion_template="Safety joints provide an emergency release point in the fishing BHA and should be included above the primary tool.",
        reasoning_framework="""
1. Select a safety joint compatible with the fishing tool and BHA configuration.
2. Place the safety joint above the primary fishing tool for easy release.
3. Ensure the joint is properly torqued and tested before running in hole.
4. Train crews on activation and retrieval procedures.
5. Inspect and maintain safety joints regularly.
6. Document all safety joint activations and outcomes.
""",
        key_factors=[
            "BHA configuration",
            "Tool compatibility",
            "Proper placement",
            "Crew training",
            "Maintenance and inspection"
        ],
        primary_authority=[
            "Weatherford Fishing Tools Manual",
            "API RP 7G",
            "SPE 20432"
        ],
        burden_holder="Fishing Engineer",
        adversary_position="Safety joints add unnecessary complexity and cost.",
        counter_arguments=[
            "Safety joints prevent loss of entire BHA.",
            "Emergency release reduces NPT.",
            "Proper training mitigates complexity."
        ],
        resolution_strategy="Standardize safety joint use in all fishing BHAs.",
        entity_scope="Fishing Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Weatherford Fishing Tools Manual"
    ),
    DoctrineBlock(
        topic="Stuck Pipe Spotting Fluids",
        keywords=["stuck pipe", "spotting fluid", "lubricant", "differential sticking", "pipe freeing"],
        conclusion_template="Spotting fluids are deployed to reduce friction and differential pressure, aiding in freeing stuck pipe.",
        reasoning_framework="""
1. Select spotting fluid based on mud system, formation, and sticking mechanism.
2. Pump spotting fluid to the stuck interval and allow soak time.
3. Monitor for changes in overpull, torque, and pipe movement.
4. Use circulation and reciprocation to enhance fluid effectiveness.
5. Evaluate results and repeat or escalate as necessary.
6. Document fluid type, volume, and outcomes for future reference.
""",
        key_factors=[
            "Fluid compatibility",
            "Soak time",
            "Circulation effectiveness",
            "Pipe movement monitoring",
            "Documentation"
        ],
        primary_authority=[
            "API RP 13B-1",
            "SPE 20432",
            "Bourgoyne et al., Applied Drilling Engineering"
        ],
        burden_holder="Drilling Supervisor",
        adversary_position="Spotting fluids are ineffective for severe sticking.",
        counter_arguments=[
            "Proper fluid selection improves success rate.",
            "Spotting fluids are cost-effective.",
            "Severe sticking may require mechanical intervention."
        ],
        resolution_strategy="Use spotting fluids as first response to stuck pipe.",
        entity_scope="Drilling Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1"
    ),
    DoctrineBlock(
        topic="Fishing Assembly Design and Makeup",
        keywords=["fishing assembly", "BHA design", "tool selection", "makeup torque", "operational efficiency"],
        conclusion_template="Fishing assemblies must be designed for strength, compatibility, and operational objectives, with proper makeup torque applied.",
        reasoning_framework="""
1. Select tools based on fish type, well geometry, and operational goals.
2. Design BHA for optimal strength, flexibility, and jar placement.
3. Ensure all connections are properly torqued and tested.
4. Review manufacturer's specifications for tool compatibility.
5. Simulate assembly performance using modeling software.
6. Document assembly configuration and torque values.
""",
        key_factors=[
            "Tool selection",
            "BHA strength and flexibility",
            "Makeup torque",
            "Compatibility",
            "Documentation"
        ],
        primary_authority=[
            "Weatherford Fishing Tools Manual",
            "API RP 7G",
            "SPE 20432"
        ],
        burden_holder="Fishing Engineer",
        adversary_position="Standard assemblies are sufficient for all fishing jobs.",
        counter_arguments=[
            "Custom design improves success rates.",
            "Proper torque prevents downhole failures.",
            "Modeling optimizes assembly performance."
        ],
        resolution_strategy="Design and document fishing assemblies for each job.",
        entity_scope="Fishing Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Weatherford Fishing Tools Manual"
    ),
    # Additional doctrines for 40+ total, covering subtopics and advanced cases:
    DoctrineBlock(
        topic="Hydraulic Jar Timing Adjustment",
        keywords=["hydraulic jar", "timing", "delay", "impact force", "fishing"],
        conclusion_template="Hydraulic jar timing must be adjusted to match the free pipe length and maximize impact at the stuck point.",
        reasoning_framework="""
1. Calculate free pipe length above the jar.
2. Adjust jar delay mechanism according to manufacturer's recommendations.
3. Test jar timing at surface before running in hole.
4. Monitor downhole response and adjust as necessary.
5. Document timing settings and results for future reference.
""",
        key_factors=[
            "Free pipe length",
            "Jar delay setting",
            "Surface testing",
            "Downhole monitoring",
            "Documentation"
        ],
        primary_authority=[
            "Weatherford Jar Placement Manual",
            "API RP 7G"
        ],
        burden_holder="Fishing Tool Specialist",
        adversary_position="Default jar timing is always sufficient.",
        counter_arguments=[
            "Improper timing reduces impact.",
            "Well conditions may change timing requirements.",
            "Surface testing ensures correct settings."
        ],
        resolution_strategy="Adjust and test jar timing for each operation.",
        entity_scope="Fishing Operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Weatherford Jar Placement Manual"
    ),
    DoctrineBlock(
        topic="Overshot Grapple Selection",
        keywords=["overshot", "grapple", "fishing tool", "engagement", "fish retrieval"],
        conclusion_template="Select grapple type (basket, spiral, or slip) based on fish OD, condition, and engagement length.",
        reasoning_framework="""
1. Measure fish OD and assess surface condition.
2. Choose basket grapple for smooth, uniform fish.
3. Use spiral grapple for irregular or damaged fish surfaces.
4. Select slip grapple for maximum holding force in short engagement.
5. Confirm grapple compatibility with overshot body.
6. Test engagement at surface if possible.
""",
        key_factors=[
            "Fish OD",
            "Surface condition",
            "Engagement length",
            "Grapple type",
            "Compatibility"
        ],
        primary_authority=[
            "NOV Fishing Tools Handbook",
            "API RP 7G"
        ],
        burden_holder="Fishing Supervisor",
        adversary_position="Any grapple type will suffice.",
        counter_arguments=[
            "Improper grapple selection reduces retrieval success.",
            "Fish condition dictates grapple type.",
            "Testing improves confidence."
        ],
        resolution_strategy="Match grapple type to fish condition and test engagement.",
        entity_scope="Fishing Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NOV Fishing Tools Handbook"
    ),
    DoctrineBlock(
        topic="Impression Block Interpretation",
        keywords=["impression block", "wireline", "fish orientation", "diagnostics", "fishing"],
        conclusion_template="Impression blocks provide a mold of the fish top, aiding in tool selection and engagement planning.",
        reasoning_framework="""
1. Run impression block to the fish top and retrieve for analysis.
2. Examine the impression for shape, size, and orientation.
3. Identify any irregularities, upsets, or obstructions.
4. Use impression data to select appropriate fishing tool and engagement method.
5. Document impression results for future reference.
""",
        key_factors=[
            "Impression clarity",
            "Fish top shape",
            "Obstructions",
            "Tool selection",
            "Documentation"
        ],
        primary_authority=[
            "Schlumberger Wireline Catalog",
            "API RP 7G"
        ],
        burden_holder="Wireline Engineer",
        adversary_position="Impression blocks are unnecessary with modern imaging.",
        counter_arguments=[
            "Impression blocks are simple and reliable.",
            "Imaging tools may not be available.",
            "Physical mold aids tool selection."
        ],
        resolution_strategy="Use impression blocks for diagnostic and planning purposes.",
        entity_scope="Fishing Operations",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="Schlumberger Wireline Catalog"
    ),
    DoctrineBlock(
        topic="Backoff Torque Calculation",
        keywords=["backoff", "torque", "pipe severance", "stuck pipe", "fishing"],
        conclusion_template="Calculate required backoff torque based on pipe size, grade, and connection type to ensure clean severance.",
        reasoning_framework="""
1. Identify pipe size, grade, and connection type.
2. Refer to manufacturer's torque tables for backoff values.
3. Apply calculated torque at the free point.
4. Monitor for pipe rotation and surface indicators of backoff.
5. Confirm severance before proceeding with fishing.
""",
        key_factors=[
            "Pipe size and grade",
            "Connection type",
            "Torque table reference",
            "Surface monitoring",
            "Severance confirmation"
        ],
        primary_authority=[
            "API RP 7G",
            "SPE 20432"
        ],
        burden_holder="Drilling Supervisor",
        adversary_position="Standard torque is always sufficient.",
        counter_arguments=[
            "Incorrect torque may damage pipe.",
            "Manufacturer tables ensure accuracy.",
            "Surface monitoring confirms success."
        ],
        resolution_strategy="Calculate and apply correct torque for each backoff.",
        entity_scope="Fishing Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 7G"
    ),
    DoctrineBlock(
        topic="Magnet Fishing Tool Application",
        keywords=["magnet", "fishing tool", "retrieval", "ferrous debris", "wireline"],
        conclusion_template="Magnet tools are used to retrieve small ferrous debris from the wellbore during fishing operations.",
        reasoning_framework="""
1. Assess the type and size of ferrous debris present.
2. Select appropriate magnet tool based on debris size and wellbore diameter.
3. Run magnet tool on wireline or slickline to debris depth.
4. Retrieve and inspect magnet for debris capture.
5. Repeat as necessary until debris is cleared.
""",
        key_factors=[
            "Debris type and size",
            "Magnet tool selection",
            "Wellbore diameter",
            "Retrieval effectiveness",
            "Repeat runs"
        ],
        primary_authority=[
            "Schlumberger Wireline Catalog",
            "API RP 7G"
        ],
        burden_holder="Wireline Engineer",
        adversary_position="Magnets are ineffective for most debris.",
        counter_arguments=[
            "Magnets are effective for small ferrous objects.",
            "Multiple runs may be required.",
            "Alternative tools exist for non-ferrous debris."
        ],
        resolution_strategy="Use magnets as first response for ferrous debris.",
        entity_scope="Fishing Operations",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="Schlumberger Wireline Catalog"
    ),
    DoctrineBlock(
        topic="Washover Shoe Selection",
        keywords=["washover shoe", "fishing", "cutting", "debris removal", "stuck pipe"],
        conclusion_template="Select washover shoe type (toothed, smooth, or carbide) based on fish material and debris type.",
        reasoning_framework="""
1. Identify fish material and hardness.
2. Select toothed shoe for hard or irregular fish.
3. Use smooth shoe for soft or uniform fish.
4. Choose carbide shoe for abrasive or hard debris.
5. Confirm shoe compatibility with washover pipe.
6. Test shoe at surface if possible.
""",
        key_factors=[
            "Fish material",
            "Debris type",
            "Shoe type",
            "Compatibility",
            "Surface testing"
        ],
        primary_authority=[
            "Baker Hughes Fishing Handbook",
            "API RP 7G"
        ],
        burden_holder="Fishing Supervisor",
        adversary_position="Any shoe type will suffice.",
        counter_arguments=[
            "Improper shoe selection reduces efficiency.",
            "Fish material dictates shoe type.",
            "Testing improves confidence."
        ],
        resolution_strategy="Match shoe type to fish and debris characteristics.",
        entity_scope="Fishing Operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Baker Hughes Fishing Handbook"
    ),
    DoctrineBlock(
        topic="Section Mill Blade Wear Monitoring",
        keywords=["section mill", "blade wear", "milling", "casing removal", "tool life"],
        conclusion_template="Monitor section mill blade wear to prevent tool failure and ensure efficient casing removal.",
        reasoning_framework="""
1. Inspect mill blades before and after each run.
2. Monitor torque and vibration for signs of blade wear.
3. Replace blades according to manufacturer's guidelines.
4. Record blade wear data for future reference.
5. Adjust milling parameters to optimize blade life.
""",
        key_factors=[
            "Blade inspection",
            "Torque and vibration monitoring",
            "Replacement schedule",
            "Data recording",
            "Parameter adjustment"
        ],
        primary_authority=[
            "Smith Bits Milling Guide",
            "API RP 7G"
        ],
        burden_holder="Drilling Supervisor",
        adversary_position="Blade wear is not a significant concern.",
        counter_arguments=[
            "Worn blades reduce milling efficiency.",
            "Tool failure increases NPT.",
            "Monitoring extends tool life."
        ],
        resolution_strategy="Implement regular blade inspection and replacement.",
        entity_scope="Fishing Operations",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="Smith Bits Milling Guide"
    ),
    DoctrineBlock(
        topic="Wireline Fishing Safety Protocols",
        keywords=["wireline", "fishing", "safety", "explosives", "HSE"],
        conclusion_template="Strict safety protocols must be followed during wireline fishing, especially when using explosives.",
        reasoning_framework="""
1. Review and adhere to company and regulatory safety guidelines.
2. Conduct pre-job safety meetings and hazard assessments.
3. Use proper PPE and barricade the work area.
4. Handle explosives with certified personnel only.
5. Document all safety incidents and lessons learned.
""",
        key_factors=[
            "Safety guidelines",
            "Pre-job meetings",
            "PPE use",
            "Explosives handling",
            "Incident documentation"
        ],
        primary_authority=[
            "API RP 75",
            "Company HSE Manual"
        ],
        burden_holder="Wireline Supervisor",
        adversary_position="Routine fishing does not require strict safety protocols.",
        counter_arguments=[
            "Explosives increase risk.",
            "HSE compliance is mandatory.",
            "Incidents can have severe consequences."
        ],
        resolution_strategy="Enforce safety protocols for all wireline fishing jobs.",
        entity_scope="Fishing Operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 75"
    ),
    DoctrineBlock(
        topic="Junk Mill Stabilizer Placement",
        keywords=["junk mill", "stabilizer", "BHA", "milling", "vibration control"],
        conclusion_template="Place stabilizers above and below the junk mill to minimize vibration and improve milling efficiency.",
        reasoning_framework="""
1. Design BHA with stabilizers positioned close to the junk mill.
2. Adjust stabilizer spacing based on well deviation and BHA length.
3. Monitor vibration and torque during milling.
4. Modify stabilizer placement if excessive vibration occurs.
5. Document BHA configuration and performance.
""",
        key_factors=[
            "Stabilizer placement",
            "BHA design",
            "Vibration monitoring",
            "Well deviation",
            "Documentation"
        ],
        primary_authority=[
            "Smith Bits Milling Guide",
            "API RP 7G"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Stabilizers are not needed for junk milling.",
        counter_arguments=[
            "Stabilizers reduce vibration.",
            "Improved milling efficiency.",
            "Well deviation increases vibration risk."
        ],
        resolution_strategy="Optimize stabilizer placement for each milling job.",
        entity_scope="Fishing Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Smith Bits Milling Guide"
    ),
    DoctrineBlock(
        topic="Wireline Tool Weakpoint Application",
        keywords=["wireline", "weakpoint", "tool release", "fishing", "safety"],
        conclusion_template="Wireline weakpoints are used to ensure tool release in case of sticking, minimizing risk of wireline loss.",
        reasoning_framework="""
1. Select weakpoint rating based on tool weight and expected overpull.
2. Install weakpoint between tool and wireline head.
3. Monitor tension during operations to avoid premature release.
4. Document weakpoint rating and activation events.
5. Replace weakpoints after each activation.
""",
        key_factors=[
            "Weakpoint rating",
            "Tool weight",
            "Tension monitoring",
            "Documentation",
            "Replacement schedule"
        ],
        primary_authority=[
            "Schlumberger Wireline Catalog",
            "API RP 7G"
        ],
        burden_holder="Wireline Engineer",
        adversary_position="Weakpoints are unnecessary and increase tool loss risk.",
        counter_arguments=[
            "Weakpoints prevent wireline loss.",
            "Proper rating avoids premature release.",
            "Documentation improves future planning."
        ],
        resolution_strategy="Standardize weakpoint use in wireline fishing.",
        entity_scope="Fishing Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Schlumberger Wireline Catalog"
    ),
    DoctrineBlock(
        topic="Fishing Job Communication Protocols",
        keywords=["fishing job", "communication", "stakeholders", "HSE", "NPT"],
        conclusion_template="Effective communication protocols ensure all stakeholders are informed and reduce NPT during fishing jobs.",
        reasoning_framework="""
1. Identify all internal and external stakeholders.
2. Establish communication channels and reporting frequency.
3. Document and distribute daily operation summaries.
4. Hold regular briefings and update plans as needed.
5. Review communication effectiveness after job completion.
""",
        key_factors=[
            "Stakeholder identification",
            "Communication channels",
            "Reporting frequency",
            "Briefings",
            "Post-job review"
        ],
        primary_authority=[
            "API RP 75",
            "Company HSE Manual"
        ],
        burden_holder="Fishing Supervisor",
        adversary_position="Routine fishing jobs do not require formal communication.",
        counter_arguments=[
            "Unexpected events require rapid response.",
            "NPT is reduced with clear communication.",
            "HSE compliance mandates documentation."
        ],
        resolution_strategy="Implement formal communication protocols for all fishing jobs.",
        entity_scope="Fishing Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 75"
    ),
    DoctrineBlock(
        topic="Sidetrack Kickoff Point Selection",
        keywords=["sidetrack", "kickoff point", "wellbore deviation", "casing exit", "drilling"],
        conclusion_template="Select kickoff point based on wellbore stability, casing condition, and sidetrack objectives.",
        reasoning_framework="""
1. Evaluate wellbore and casing condition at potential kickoff points.
2. Assess offset data for stability and dogleg severity.
3. Select a point that minimizes risk of wellbore collapse.
4. Plan window milling and deviation tools accordingly.
5. Document selection criteria and expected outcomes.
""",
        key_factors=[
            "Wellbore stability",
            "Casing condition",
            "Offset data",
            "Dogleg severity",
            "Documentation"
        ],
        primary_authority=[
            "Baker Hughes Whipstock Manual",
            "API RP 7G"
        ],
        burden_holder="Directional Driller",
        adversary_position="Kickoff point can be selected arbitrarily.",
        counter_arguments=[
            "Improper selection increases risk.",
            "Offset data improves decision-making.",
            "Documentation aids future planning."
        ],
        resolution_strategy="Select kickoff point based on stability and objectives.",
        entity_scope="Drilling Operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Baker Hughes Whipstock Manual"
    ),
    DoctrineBlock(
        topic="Fishing Tool Crossover Sub Application",
        keywords=["crossover sub", "fishing tool", "BHA", "thread compatibility", "makeup"],
        conclusion_template="Crossover subs are used to connect fishing tools with different thread types, ensuring BHA compatibility.",
        reasoning_framework="""
1. Identify thread types on fishing tool and BHA.
2. Select crossover sub with matching threads.
3. Verify makeup torque and pressure rating.
4. Inspect crossover sub for wear or damage.
5. Document crossover use and configuration.
""",
        key_factors=[
            "Thread compatibility",
            "Makeup torque",
            "Pressure rating",
            "Inspection",
            "Documentation"
        ],
        primary_authority=[
            "Weatherford Fishing Tools Manual",
            "API RP 7G"
        ],
        burden_holder="Fishing Engineer",
        adversary_position="Crossover subs are unnecessary with standard tools.",
        counter_arguments=[
            "Thread types often differ.",
            "Proper subs prevent leaks.",
            "Documentation aids troubleshooting."
        ],
        resolution_strategy="Standardize crossover sub use for thread compatibility.",
        entity_scope="Fishing Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Weatherford Fishing Tools Manual"
    ),
    DoctrineBlock(
        topic="Fishing Assembly Modeling Software Application",
        keywords=["fishing assembly", "modeling software", "BHA simulation", "performance prediction", "design"],
        conclusion_template="Modeling software should be used to simulate fishing assembly performance and optimize design.",
        reasoning_framework="""
1. Input fish and well parameters into modeling software.
2. Simulate BHA performance under expected downhole conditions.
3. Adjust tool selection and placement based on simulation results.
4. Validate model predictions with field data.
5. Document simulation parameters and outcomes.
""",
        key_factors=[
            "Input accuracy",
            "Simulation results",
            "Tool selection",
            "Field validation",
            "Documentation"
        ],
        primary_authority=[
            "Weatherford Fishing Tools Manual",
            "SPE 20432"
        ],
        burden_holder="Fishing Engineer",
        adversary_position="Modeling is unnecessary for routine assemblies.",
        counter_arguments=[
            "Simulation reduces risk.",
            "Modeling optimizes performance.",
            "Documentation aids future planning."
        ],
        resolution_strategy="Use modeling software for all complex fishing assemblies.",
        entity_scope="Fishing Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Weatherford Fishing Tools Manual"
    ),
    DoctrineBlock(
        topic="Fishing Job Post-Operation Review",
        keywords=["fishing job", "post-operation review", "lessons learned", "NPT reduction", "continuous improvement"],
        conclusion_template="Conduct post-operation reviews to capture lessons learned and improve future fishing job performance.",
        reasoning_framework="""
1. Gather all operation data and reports.
2. Review successes, failures, and unexpected events.
3. Identify root causes of NPT or incidents.
4. Document lessons learned and recommended changes.
5. Share findings with relevant teams and update procedures.
""",
        key_factors=[
            "Data collection",
            "Root cause analysis",
            "Documentation",
            "Knowledge sharing",
            "Procedure updates"
        ],
        primary_authority=[
            "API RP 75",
            "Company HSE Manual"
        ],
        burden_holder="Fishing Supervisor",
        adversary_position="Post-job reviews are unnecessary for routine jobs.",
        counter_arguments=[
            "Continuous improvement reduces NPT.",
            "Lessons learned improve future performance.",
            "Documentation aids compliance."
        ],
        resolution_strategy="Standardize post-operation reviews for all fishing jobs.",
        entity_scope="Fishing Operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 75"
    ),
    DoctrineBlock(
        topic="Fishing Tool Redress and Maintenance",
        keywords=["fishing tool", "redress", "maintenance", "tool life", "BHA reliability"],
        conclusion_template="Regular redress and maintenance of fishing tools are essential for reliability and safety.",
        reasoning_framework="""
1. Inspect tools for wear, damage, and fatigue after each job.
2. Redress or replace worn components according to manufacturer's guidelines.
3. Maintain detailed maintenance records.
4. Test tools before each run.
5. Train personnel on proper maintenance procedures.
""",
        key_factors=[
            "Inspection",
            "Redress schedule",
            "Maintenance records",
            "Testing",
            "Personnel training"
        ],
        primary_authority=[
            "Weatherford Fishing Tools Manual",
            "API RP 7G"
        ],
        burden_holder="Fishing Engineer",
        adversary_position="Maintenance is only needed after tool failure.",
        counter_arguments=[
            "Preventive maintenance reduces failures.",
            "Redress extends tool life.",
            "Records improve traceability."
        ],
        resolution_strategy="Implement regular maintenance and redress schedule.",
        entity_scope="Fishing Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Weatherford Fishing Tools Manual"
    ),
    DoctrineBlock(
        topic="Fishing Job HSE Compliance",
        keywords=["fishing job", "HSE", "compliance", "regulations", "safety"],
        conclusion_template="All fishing operations must comply with HSE regulations and company policies.",
        reasoning_framework="""
1. Review applicable HSE regulations and company policies.
2. Conduct pre-job safety meetings and hazard assessments.
3. Ensure all personnel are trained and certified.
4. Monitor compliance during operations.
5. Document incidents and corrective actions.
""",
        key_factors=[
            "Regulatory review",
            "Pre-job meetings",
            "Personnel training",
            "Compliance monitoring",
            "Incident documentation"
        ],
        primary_authority=[
            "API RP 75",
            "Company HSE Manual"
        ],
        burden_holder="Fishing Supervisor",
        adversary_position="HSE compliance slows operations.",
        counter_arguments=[
            "Non-compliance risks severe penalties.",
            "Safety is paramount.",
            "Documentation aids future planning."
        ],
        resolution_strategy="Enforce HSE compliance for all fishing jobs.",
        entity_scope="Fishing Operations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 75"
    ),
    DoctrineBlock(
        topic="Fishing Tool Inventory Management",
        keywords=["fishing tool", "inventory", "management", "availability", "logistics"],
        conclusion_template="Maintain accurate fishing tool inventory to ensure availability and reduce NPT.",
        reasoning_framework="""
1. Track tool usage and location in real time.
2. Maintain minimum stock levels for critical tools.
3. Schedule regular inventory audits.
4. Coordinate with logistics for timely resupply.
5. Document tool movements and usage.
""",
        key_factors=[
            "Real-time tracking",
            "Stock levels",
            "Inventory audits",
            "Logistics coordination",
            "Documentation"
        ],
        primary_authority=[
            "Company Logistics Manual",
            "API RP 7G"
        ],
        burden_holder="Fishing Supervisor",
        adversary_position="Inventory management is unnecessary for routine jobs.",
        counter_arguments=[
            "Tool shortages increase NPT.",
            "Audits prevent loss.",
            "Documentation improves accountability."
        ],
        resolution_strategy="Standardize inventory management for all fishing tools.",
        entity_scope="Fishing Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Company Logistics Manual"
    ),
    DoctrineBlock(
        topic="Fishing Tool Compatibility Verification",
        keywords=["fishing tool", "compatibility", "BHA", "thread type", "pressure rating"],
        conclusion_template="Verify tool compatibility for thread type, pressure rating, and operational objectives before assembly.",
        reasoning_framework="""
1. Check thread type and size for all BHA components.
2. Confirm pressure and temperature ratings.
3. Review operational objectives and tool limitations.
4. Test assembly at surface before running in hole.
5. Document compatibility verification.
""",
        key_factors=[
            "Thread type and size",
            "Pressure rating",
            "Temperature rating",
            "Operational objectives",
            "Documentation"
        ],
        primary_authority=[
            "Weatherford Fishing Tools Manual",
            "API RP 7G"
        ],
        burden_holder="Fishing Engineer",
        adversary_position="Compatibility checks are unnecessary with standard tools.",
        counter_arguments=[
            "Mismatched threads cause failures.",
            "Pressure ratings must match well conditions.",
            "Documentation aids troubleshooting."
        ],
        resolution_strategy="Verify and document compatibility for all assemblies.",
        entity_scope="Fishing Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Weatherford Fishing Tools Manual"
    ),
    DoctrineBlock(
        topic="Fishing Tool Make-Up Torque Verification",
        keywords=["fishing tool", "make-up torque", "BHA", "connection integrity", "fishing"],
        conclusion_template="Verify make-up torque for all fishing tool connections to ensure integrity and prevent downhole failures.",
        reasoning_framework="""
1. Refer to manufacturer's torque specifications for each connection.
2. Use calibrated torque wrenches during assembly.
3. Record applied torque values.
4. Inspect connections for signs of over- or under-torque.
5. Document torque verification for each job.
""",
        key_factors=[
            "Torque specification",
            "Calibrated tools",
            "Inspection",
            "Documentation",
            "Connection integrity"
        ],
        primary_authority=[
            "Weatherford Fishing Tools Manual",
            "API RP 7G"
        ],
        burden_holder="Fishing Engineer",
        adversary_position="Torque verification is unnecessary for experienced crews.",
        counter_arguments=[
            "Incorrect torque causes failures.",
            "Calibration ensures accuracy.",
            "Documentation aids compliance."
        ],
        resolution_strategy="Standardize torque verification for all fishing jobs.",
        entity_scope="Fishing Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Weatherford Fishing Tools Manual"
    ),
    DoctrineBlock(
        topic="Fishing Job Pre-Operation Checklist",
        keywords=["fishing job", "pre-operation", "checklist", "planning", "readiness"],
        conclusion_template="Use a pre-operation checklist to ensure all equipment, personnel, and plans are ready before fishing jobs.",
        reasoning_framework="""
1. Review job objectives and operational plan.
2. Verify tool selection and readiness.
3. Confirm personnel assignments and training.
4. Check inventory and logistics for required equipment.
5. Conduct pre-job safety meeting and hazard assessment.
6. Document checklist completion.
""",
        key_factors=[
            "Operational plan",
            "Tool readiness",
            "Personnel training",
            "Inventory check",
            "Documentation"
        ],
        primary_authority=[
            "API RP 75",
            "Company HSE Manual"
        ],
        burden_holder="Fishing Supervisor",
        adversary_position="Checklists are unnecessary for routine jobs.",
        counter_arguments=[
            "Checklists prevent oversights.",
            "Readiness reduces NPT.",
            "Documentation aids compliance."
        ],
        resolution_strategy="Implement pre-operation checklists for all fishing jobs.",
        entity_scope="Fishing Operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 75"
    ),
    DoctrineBlock(
        topic="Fishing Assembly Overpull Limit Calculation",
        keywords=["fishing assembly", "overpull", "limit", "BHA strength", "stuck pipe"],
        conclusion_template="Calculate overpull limits based on weakest BHA component to prevent downhole failures.",
        reasoning_framework="""
1. Identify the weakest component in the fishing assembly.
2. Refer to manufacturer's tensile strength data.
3. Calculate safe overpull limit with safety factor.
4. Communicate limit to rig crew and monitor during operations.
5. Document calculation and any overpull events.
""",
        key_factors=[
            "Weakest component",
            "Tensile strength",
            "Safety factor",
            "Communication",
            "Documentation"
        ],
        primary_authority=[
            "Weatherford Fishing Tools Manual",
            "API RP 7G"
        ],
        burden_holder="Fishing Engineer",
        adversary_position="Maximum rig pull can always be applied.",
        counter_arguments=[
            "Overpull above limit causes failures.",
            "Safety factor prevents accidents.",
            "Documentation aids future planning."
        ],
        resolution_strategy="Calculate and communicate overpull limits for each job.",
        entity_scope="Fishing Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Weatherford Fishing Tools Manual"
    ),
    DoctrineBlock(
        topic="Fishing Job Contingency Tool Planning",
        keywords=["fishing job", "contingency", "tool planning", "NPT reduction", "readiness"],
        conclusion_template="Plan and stage contingency tools for likely fishing job complications to reduce NPT.",
        reasoning_framework="""
1. Review potential complications based on well and fish data.
2. Identify and stage contingency tools at the rig site.
3. Train personnel on contingency tool use.
4. Document contingency plan and tool staging.
5. Review and update plan as operation progresses.
""",
        key_factors=[
            "Complication review",
            "Tool staging",
            "Personnel training",
            "Documentation",
            "Plan updates"
        ],
        primary_authority=[
            "API RP 75",
            "Company HSE Manual"
        ],
        burden_holder="Fishing Supervisor",
        adversary_position="Contingency planning is unnecessary for routine jobs.",
        counter_arguments=[
            "Unexpected events require readiness.",
            "Staged tools reduce NPT.",
            "Documentation aids compliance."
        ],
        resolution_strategy="Implement contingency tool planning for all fishing jobs.",
        entity_scope="Fishing Operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 75"
    ),
    DoctrineBlock(
        topic="Fishing Job Real-Time Data Monitoring",
        keywords=["fishing job", "real-time data", "monitoring", "decision making", "NPT reduction"],
        conclusion_template="Monitor real-time data (torque, drag, overpull, circulation) to inform decisions and reduce NPT during fishing jobs.",
        reasoning_framework="""
1. Set up real-time data acquisition for key parameters.
2. Monitor data trends for early warning signs.
3. Adjust operations based on data analysis.
4. Communicate findings to all stakeholders.
5. Document data and decisions for post-job review.
""",
        key_factors=[
            "Data acquisition",
            "Trend monitoring",
            "Operational adjustment",
            "Communication",
            "Documentation"
        ],
        primary_authority=[
            "API RP 7G",
            "Company HSE Manual"
        ],
        burden_holder="Fishing Supervisor",
        adversary_position="Real-time monitoring is unnecessary for routine jobs.",
        counter_arguments=[
            "Early warning reduces NPT.",
            "Data-driven decisions improve outcomes.",
            "Documentation aids future planning."
        ],
        resolution_strategy="Implement real-time monitoring for all fishing jobs.",
        entity_scope="Fishing Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 7G"
    ),
    DoctrineBlock(
        topic="Fishing Job Environmental Impact Minimization",
        keywords=["fishing job", "environmental impact", "minimization", "waste management", "regulations"],
        conclusion_template="Minimize environmental impact by managing waste, spills, and emissions during fishing operations.",
        reasoning_framework="""
1. Review environmental regulations and company policies.
2. Implement waste management and spill prevention measures.
3. Monitor for spills and emissions during operations.
4. Train personnel on environmental best practices.
5. Document incidents and corrective actions.
""",
        key_factors=[
            "Regulatory review",
            "Waste management",
            "Spill prevention",
            "Personnel training",
            "Documentation"
        ],
        primary_authority=[
            "API RP 75",
            "Company Environmental Manual"
        ],
        burden_holder="Fishing Supervisor",
        adversary_position="Environmental measures slow operations.",
        counter_arguments=[
            "Non-compliance risks penalties.",
            "Best practices reduce impact.",
            "Documentation aids compliance."
        ],
        resolution_strategy="Implement environmental best practices for all fishing jobs.",
        entity_scope="Fishing Operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 75"
    ),
    DoctrineBlock(
        topic="Fishing Job Digital Reporting",
        keywords=["fishing job", "digital reporting", "data management", "compliance", "NPT reduction"],
        conclusion_template="Use digital reporting tools to document fishing job data, improve compliance, and reduce NPT.",
        reasoning_framework="""
1. Set up digital reporting system for fishing job data.
2. Train personnel on data entry and management.
3. Review and validate data for accuracy.
4. Share reports with relevant stakeholders.
5. Archive data for future reference and compliance.
""",
        key_factors=[
            "Digital system setup",
            "Personnel training",
            "Data validation",
            "Stakeholder sharing",
            "Archiving"
        ],
        primary_authority=[
            "Company IT Manual",
            "API RP 75"
        ],
        burden_holder="Fishing Supervisor",
        adversary_position="Paper reporting is sufficient.",
        counter_arguments=[
            "Digital reporting improves accuracy.",
            "Data is easily shared and archived.",
            "Compliance is easier to demonstrate."
        ],
        resolution_strategy="Standardize digital reporting for all fishing jobs.",
        entity_scope="Fishing Operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Company IT Manual"
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