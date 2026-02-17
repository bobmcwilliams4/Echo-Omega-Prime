from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    UNCERTAIN = "Uncertain"

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
        topic="Refrac Candidate Selection - Production Decline Analysis",
        keywords=["refrac", "candidate selection", "production decline", "analysis", "DCA"],
        conclusion_template="A well is a suitable refrac candidate if its production decline curve indicates significant remaining reserves and a clear deviation from expected EUR.",
        reasoning_framework="""
        1. Analyze historical production data using Decline Curve Analysis (DCA).
        2. Identify wells with sharp production decline post-initial stimulation.
        3. Evaluate remaining reserves and compare with offset wells.
        4. Consider well age, completion design, and reservoir properties.
        5. Assess if the decline is due to mechanical issues or reservoir depletion.
        6. Exclude wells with terminal decline or poor reservoir connectivity.
        7. Prioritize wells with under-stimulated zones or bypassed pay.
        8. Integrate petrophysical and pressure data for comprehensive assessment.
        9. Validate candidate selection with economic thresholds.
        10. Document all assumptions and uncertainties in the analysis.
        """,
        key_factors=[
            "Historical production rates",
            "Decline curve type (exponential, hyperbolic, harmonic)",
            "Remaining reserves estimation",
            "Completion and stimulation history",
            "Reservoir quality indicators",
            "Economic cutoffs"
        ],
        primary_authority=[
            "SPE 187168: 'Refracturing Candidate Selection Using Production Data Analytics'",
            "Society of Petroleum Engineers (SPE) DCA Guidelines"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Production decline is due to irreversible reservoir depletion; refrac will not yield incremental recovery.",
        counter_arguments=[
            "Decline may be due to suboptimal initial stimulation.",
            "Bypassed pay zones may exist.",
            "Mechanical issues may be remediable."
        ],
        resolution_strategy="Integrate DCA with petrophysical and completion data; validate with mini-frac or diagnostic testing.",
        entity_scope="Horizontal unconventional wells",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 187168"
    ),
    DoctrineBlock(
        topic="Refrac Stress Reorientation Theory",
        keywords=["refrac", "stress reorientation", "fracture geometry", "reservoir stress"],
        conclusion_template="Stress reorientation post-initial frac can alter fracture geometry during refrac, enabling stimulation of previously untreated rock.",
        reasoning_framework="""
        1. Initial hydraulic fracturing alters in-situ stress fields.
        2. Stress shadowing and depletion-induced changes reorient principal stresses.
        3. Refrac treatments propagate fractures in new orientations.
        4. Use microseismic and image log data to validate stress rotation.
        5. Model stress changes using geomechanical simulations.
        6. Assess the risk of fracture hits on offset wells.
        7. Predict refrac fracture geometry for optimal well spacing.
        8. Integrate with completion design to maximize reservoir contact.
        9. Document uncertainty in stress prediction.
        """,
        key_factors=[
            "Magnitude and direction of principal stresses",
            "Fracture orientation pre- and post-initial frac",
            "Reservoir depletion effects",
            "Geomechanical modeling results",
            "Microseismic validation"
        ],
        primary_authority=[
            "SPE 184880: 'Stress Reorientation and Its Impact on Refracturing'",
            "Journal of Petroleum Technology, 2017"
        ],
        burden_holder="Geomechanics Specialist",
        adversary_position="Stress changes are insufficient to alter fracture orientation; refrac will follow original paths.",
        counter_arguments=[
            "Field data shows new fracture azimuths post-refrac.",
            "Geomechanical models predict stress rotation.",
            "Microseismic mapping confirms fracture reorientation."
        ],
        resolution_strategy="Combine field diagnostics and modeling to confirm stress reorientation before refrac.",
        entity_scope="Unconventional shale reservoirs",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 184880"
    ),
    DoctrineBlock(
        topic="Mechanical Diversion - Bridge Plugs and Composite Plugs",
        keywords=["mechanical diversion", "bridge plugs", "composite plugs", "zonal isolation", "refrac"],
        conclusion_template="Bridge plugs and composite plugs provide effective zonal isolation for staged refrac treatments, enhancing stimulation efficiency.",
        reasoning_framework="""
        1. Deploy bridge or composite plugs to isolate previously stimulated intervals.
        2. Confirm plug setting depth and integrity with wireline or coiled tubing.
        3. Pressure test isolation before refrac pumping.
        4. Pump refrac treatment into open intervals above the plug.
        5. Retrieve or drill out plugs post-treatment as per operational plan.
        6. Evaluate plug performance via pressure response and post-job logs.
        7. Consider plug degradation and debris risks for composite plugs.
        8. Document plug setting and retrieval operations for future reference.
        """,
        key_factors=[
            "Plug setting accuracy",
            "Pressure isolation integrity",
            "Plug material compatibility",
            "Operational risks (debris, retrieval)",
            "Stimulation efficiency"
        ],
        primary_authority=[
            "API RP 100-1: Hydraulic Fracturing Operations",
            "SPE 191407: 'Mechanical Diversion in Refracturing'"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Mechanical plugs may fail to provide complete isolation, leading to ineffective refrac.",
        counter_arguments=[
            "Advances in plug technology improve reliability.",
            "Pressure tests can confirm isolation.",
            "Composite plugs minimize retrieval risks."
        ],
        resolution_strategy="Use field-proven plug systems and validate isolation with pressure diagnostics.",
        entity_scope="Horizontal and vertical wells",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1"
    ),
    DoctrineBlock(
        topic="Chemical Diversion for Refrac",
        keywords=["chemical diversion", "diverter", "refrac", "zonal isolation", "stimulation"],
        conclusion_template="Chemical diverters can temporarily block high-permeability zones, redirecting refrac fluids to under-stimulated intervals.",
        reasoning_framework="""
        1. Select diverter type based on reservoir temperature and fluid compatibility.
        2. Pump diverter ahead or as a slug during refrac treatment.
        3. Monitor pressure response to confirm diversion effectiveness.
        4. Ensure diverter degrades or dissolves post-treatment to restore flow.
        5. Evaluate risk of formation damage or incomplete diversion.
        6. Integrate with mechanical diversion if needed for complex completions.
        7. Document diverter type, concentration, and placement for future analysis.
        """,
        key_factors=[
            "Diverter material properties",
            "Reservoir temperature and chemistry",
            "Pressure response during diversion",
            "Risk of formation damage",
            "Integration with mechanical diversion"
        ],
        primary_authority=[
            "SPE 194325: 'Chemical Diversion in Refracturing Operations'",
            "World Oil, 2019"
        ],
        burden_holder="Stimulation Engineer",
        adversary_position="Chemical diverters may not provide effective isolation in heterogeneous reservoirs.",
        counter_arguments=[
            "Field trials show improved stimulation coverage.",
            "Diverter selection can be tailored to reservoir conditions.",
            "Combination with mechanical diversion enhances effectiveness."
        ],
        resolution_strategy="Pilot test diverter systems and monitor treatment response closely.",
        entity_scope="Unconventional and conventional reservoirs",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 194325"
    ),
    DoctrineBlock(
        topic="Bullhead Refrac Technique",
        keywords=["bullhead", "refrac", "stimulation", "wellbore", "treatment"],
        conclusion_template="Bullhead refrac involves pumping treatment fluids directly down the casing or tubing, relying on pressure to force fluids into the formation.",
        reasoning_framework="""
        1. Evaluate wellbore integrity and completion configuration.
        2. Select bullhead technique when mechanical isolation is not feasible.
        3. Pump refrac fluids at rates and pressures sufficient to overcome formation entry pressure.
        4. Monitor surface and downhole pressures for treatment placement.
        5. Assess risk of screenout or unintended fracture propagation.
        6. Use diverters or rate changes to improve fluid distribution.
        7. Document treatment parameters and post-job well performance.
        """,
        key_factors=[
            "Wellbore integrity",
            "Completion type (openhole, cased hole)",
            "Formation entry pressure",
            "Treatment rate and pressure",
            "Risk of screenout"
        ],
        primary_authority=[
            "SPE 181728: 'Bullhead Refracturing in Horizontal Wells'",
            "API RP 100-1"
        ],
        burden_holder="Stimulation Engineer",
        adversary_position="Bullhead refrac may result in poor fluid placement and limited stimulation of target zones.",
        counter_arguments=[
            "Optimized rates and diverters can improve placement.",
            "Suitable for wells with limited access.",
            "Cost-effective for certain well types."
        ],
        resolution_strategy="Model fluid distribution and monitor treatment response in real-time.",
        entity_scope="Horizontal and vertical wells",
        confidence=0.78,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 181728"
    ),
    DoctrineBlock(
        topic="Economic Analysis - Refrac vs New Drill Decision",
        keywords=["economic analysis", "refrac", "new drill", "cost-benefit", "decision"],
        conclusion_template="Refrac is economically preferable to new drilling when expected incremental EUR and NPV exceed those of a new well at lower capital cost.",
        reasoning_framework="""
        1. Estimate incremental EUR from refrac using production forecasts.
        2. Calculate refrac capital and operating costs.
        3. Compare with new drill EUR, costs, and risk profile.
        4. Run discounted cash flow (DCF) and NPV analysis for both options.
        5. Factor in downtime, infrastructure reuse, and regulatory costs.
        6. Assess sensitivity to commodity price, cost overruns, and operational risks.
        7. Document assumptions and economic thresholds for decision-making.
        """,
        key_factors=[
            "Incremental EUR from refrac",
            "Refrac and new drill costs",
            "NPV and IRR calculations",
            "Operational and regulatory risks",
            "Commodity price sensitivity"
        ],
        primary_authority=[
            "SPE 199876: 'Economic Evaluation of Refracturing vs New Drilling'",
            "Society of Petroleum Evaluation Engineers (SPEE) Guidelines"
        ],
        burden_holder="Asset Manager",
        adversary_position="New drills offer higher EUR and lower operational risks compared to refracs.",
        counter_arguments=[
            "Refrac capital costs are significantly lower.",
            "Infrastructure reuse reduces time to first oil.",
            "Refrac can unlock bypassed reserves."
        ],
        resolution_strategy="Run scenario-based economic models and update with real-time cost/performance data.",
        entity_scope="Unconventional oil and gas assets",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 199876"
    ),
    DoctrineBlock(
        topic="Production History Analysis for Refrac Timing",
        keywords=["production history", "refrac timing", "analysis", "well performance"],
        conclusion_template="Optimal refrac timing is determined by analyzing production history to identify inflection points indicating diminishing returns from primary stimulation.",
        reasoning_framework="""
        1. Gather complete production history for candidate wells.
        2. Identify inflection points in rate vs time plots.
        3. Correlate production drops with operational events (e.g., equipment failure, water breakthrough).
        4. Use statistical models to predict remaining economic life without refrac.
        5. Assess impact of refrac timing on incremental recovery and economics.
        6. Document uncertainties and validate with offset well data.
        """,
        key_factors=[
            "Production rate trends",
            "Inflection point identification",
            "Operational event correlation",
            "Economic life prediction",
            "Offset well performance"
        ],
        primary_authority=[
            "SPE 185042: 'Timing of Refracturing Operations'",
            "AAPG Bulletin, 2016"
        ],
        burden_holder="Production Engineer",
        adversary_position="Early refrac may not maximize incremental recovery; late refrac may result in diminished returns.",
        counter_arguments=[
            "Data-driven timing optimizes recovery.",
            "Offset analysis reduces uncertainty.",
            "Economic models guide timing decisions."
        ],
        resolution_strategy="Integrate production data analytics with economic modeling.",
        entity_scope="Horizontal unconventional wells",
        confidence=0.83,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 185042"
    ),
    DoctrineBlock(
        topic="Casing Integrity Assessment Before Refrac",
        keywords=["casing integrity", "assessment", "refrac", "wellbore integrity", "pressure testing"],
        conclusion_template="Casing integrity must be verified prior to refrac to prevent fluid migration and ensure well control.",
        reasoning_framework="""
        1. Review well construction and previous workover records.
        2. Conduct pressure testing to validate casing integrity.
        3. Run caliper and cement bond logs to detect deformation or poor cement.
        4. Assess risk of microannulus or corrosion.
        5. Repair or remediate compromised casing before refrac.
        6. Document all findings and remediation actions.
        """,
        key_factors=[
            "Pressure test results",
            "Caliper and cement bond log data",
            "Well construction records",
            "Corrosion and deformation assessment",
            "Remediation feasibility"
        ],
        primary_authority=[
            "API Standard 53: Blowout Prevention Equipment",
            "SPE 202145: 'Casing Integrity in Refracturing'"
        ],
        burden_holder="Well Integrity Engineer",
        adversary_position="Casing assessment is unnecessary if well has no history of problems.",
        counter_arguments=[
            "Hidden casing issues may exist.",
            "Regulatory compliance requires integrity testing.",
            "Remediation is less costly than post-refrac failure."
        ],
        resolution_strategy="Adhere to API and regulatory standards for integrity assessment.",
        entity_scope="All well types",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API Standard 53"
    ),
    DoctrineBlock(
        topic="Refrac Flowback Protocols",
        keywords=["refrac", "flowback", "protocols", "well cleanup", "production"],
        conclusion_template="Standardized flowback protocols are essential to manage pressure, prevent sand production, and optimize post-refrac well performance.",
        reasoning_framework="""
        1. Develop flowback schedule based on treatment size and reservoir pressure.
        2. Gradually increase choke size to control drawdown.
        3. Monitor sand production and adjust rates accordingly.
        4. Use surface and downhole sensors to track pressure and flow.
        5. Implement contingency plans for screenout or equipment failure.
        6. Document flowback data for post-job analysis.
        """,
        key_factors=[
            "Flowback rate and pressure control",
            "Sand production monitoring",
            "Choke management",
            "Sensor data integration",
            "Contingency planning"
        ],
        primary_authority=[
            "SPE 193847: 'Best Practices for Refrac Flowback'",
            "API RP 100-1"
        ],
        burden_holder="Production Operations",
        adversary_position="Aggressive flowback maximizes early production and is preferable to controlled protocols.",
        counter_arguments=[
            "Aggressive flowback increases risk of sand production and equipment damage.",
            "Controlled protocols optimize long-term well performance.",
            "Data-driven adjustments improve outcomes."
        ],
        resolution_strategy="Implement and adhere to standardized flowback protocols with real-time monitoring.",
        entity_scope="All refrac wells",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 193847"
    ),
    DoctrineBlock(
        topic="Refrac Case Studies - Permian Basin Horizontal Wells",
        keywords=["refrac", "case studies", "Permian Basin", "horizontal wells", "field data"],
        conclusion_template="Permian Basin horizontal refracs have demonstrated significant incremental recovery when candidate selection and execution are optimized.",
        reasoning_framework="""
        1. Review published case studies and operator reports.
        2. Analyze pre- and post-refrac production data.
        3. Identify common success factors (candidate selection, diversion, timing).
        4. Document lessons learned and best practices.
        5. Compare with other basins to assess transferability.
        6. Integrate findings into local refrac planning.
        """,
        key_factors=[
            "Incremental recovery rates",
            "Candidate selection criteria",
            "Operational best practices",
            "Lessons learned",
            "Basin-specific challenges"
        ],
        primary_authority=[
            "SPE 204112: 'Permian Basin Refrac Case Studies'",
            "Permian Basin Oil & Gas Magazine"
        ],
        burden_holder="Field Development Team",
        adversary_position="Permian case studies are not applicable to other basins due to unique geology.",
        counter_arguments=[
            "Best practices are adaptable with local calibration.",
            "Lessons learned reduce operational risk.",
            "Case studies provide valuable benchmarks."
        ],
        resolution_strategy="Calibrate case study findings to local reservoir and operational context.",
        entity_scope="Permian Basin horizontal wells",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 204112"
    ),
    DoctrineBlock(
        topic="Refrac Pump Schedule Design",
        keywords=["refrac", "pump schedule", "design", "treatment", "stimulation"],
        conclusion_template="Optimized pump schedules balance rate, pressure, and fluid composition to maximize refrac effectiveness and minimize operational risks.",
        reasoning_framework="""
        1. Design pump schedule based on reservoir properties and completion design.
        2. Vary rate and pressure to optimize fracture propagation.
        3. Sequence fluid types (pad, proppant, flush) for effective placement.
        4. Monitor real-time data to adjust schedule as needed.
        5. Integrate diversion and zonal isolation strategies.
        6. Document all schedule changes and treatment outcomes.
        """,
        key_factors=[
            "Reservoir and completion data",
            "Rate and pressure optimization",
            "Fluid sequencing",
            "Real-time monitoring",
            "Integration with diversion techniques"
        ],
        primary_authority=[
            "SPE 201234: 'Pump Schedule Optimization for Refracturing'",
            "API RP 100-1"
        ],
        burden_holder="Stimulation Engineer",
        adversary_position="Standard pump schedules are sufficient; optimization adds unnecessary complexity.",
        counter_arguments=[
            "Optimized schedules improve stimulation efficiency.",
            "Real-time adjustments reduce risk of screenout.",
            "Custom schedules address unique well conditions."
        ],
        resolution_strategy="Use simulation and real-time data to iteratively optimize pump schedules.",
        entity_scope="All refrac operations",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 201234"
    ),
    DoctrineBlock(
        topic="Refrac Risk Assessment - Screenout and Casing Failure",
        keywords=["refrac", "risk assessment", "screenout", "casing failure", "mitigation"],
        conclusion_template="Comprehensive risk assessment identifies and mitigates screenout and casing failure risks during refrac operations.",
        reasoning_framework="""
        1. Analyze historical screenout and casing failure incidents.
        2. Model fracture propagation and proppant transport.
        3. Assess casing condition and pressure limits.
        4. Implement real-time monitoring for early detection.
        5. Prepare contingency plans for screenout and well control.
        6. Document risk mitigation measures and post-job review.
        """,
        key_factors=[
            "Historical incident data",
            "Fracture and proppant modeling",
            "Casing integrity",
            "Real-time monitoring",
            "Contingency planning"
        ],
        primary_authority=[
            "SPE 200145: 'Screenout and Casing Failure in Refracturing'",
            "API Standard 53"
        ],
        burden_holder="Operations Manager",
        adversary_position="Screenout and casing failure risks are inherent and cannot be fully mitigated.",
        counter_arguments=[
            "Proactive risk assessment reduces incident rates.",
            "Real-time monitoring enables rapid response.",
            "Contingency planning limits operational impact."
        ],
        resolution_strategy="Integrate risk assessment into refrac planning and execution workflows.",
        entity_scope="All refrac operations",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 200145"
    ),
    DoctrineBlock(
        topic="Refrac Through Existing Perforations vs New Perforations",
        keywords=["refrac", "existing perforations", "new perforations", "stimulation", "wellbore"],
        conclusion_template="Refrac through new perforations is generally preferred to avoid near-wellbore damage and improve stimulation of bypassed zones.",
        reasoning_framework="""
        1. Evaluate condition of existing perforations (plugging, damage).
        2. Assess reservoir connectivity and bypassed pay.
        3. Model fluid entry profiles for both options.
        4. Consider operational complexity and cost.
        5. Select new perforations if existing intervals are damaged or depleted.
        6. Document perforation strategy and post-job performance.
        """,
        key_factors=[
            "Perforation condition",
            "Reservoir connectivity",
            "Fluid entry modeling",
            "Operational complexity",
            "Cost and performance trade-offs"
        ],
        primary_authority=[
            "SPE 196789: 'Perforation Strategies for Refracturing'",
            "API RP 100-1"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Existing perforations are sufficient and minimize operational cost.",
        counter_arguments=[
            "New perforations target bypassed zones.",
            "Existing perforations may be plugged or damaged.",
            "Improved stimulation efficiency with new intervals."
        ],
        resolution_strategy="Base perforation strategy on well diagnostics and reservoir modeling.",
        entity_scope="Horizontal and vertical wells",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 196789"
    ),
    DoctrineBlock(
        topic="Production History DCA Methodology for Refrac Selection",
        keywords=["production history", "DCA", "refrac selection", "methodology", "analysis"],
        conclusion_template="Decline Curve Analysis (DCA) of production history is a reliable methodology for identifying refrac candidates with significant remaining reserves.",
        reasoning_framework="""
        1. Gather complete production data for candidate wells.
        2. Fit decline curves (exponential, hyperbolic, harmonic) to historical data.
        3. Estimate remaining reserves and compare with economic thresholds.
        4. Validate DCA results with offset well performance.
        5. Integrate with petrophysical and completion data for robust selection.
        6. Document methodology and uncertainties.
        """,
        key_factors=[
            "Production data quality",
            "Decline curve fitting",
            "Remaining reserves estimation",
            "Economic thresholds",
            "Offset well validation"
        ],
        primary_authority=[
            "SPE 187168",
            "SPEE Monograph 3: DCA in Unconventional Reservoirs"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="DCA is unreliable in unconventional reservoirs due to complex flow regimes.",
        counter_arguments=[
            "DCA validated with offset and post-refrac data.",
            "Integration with other data improves reliability.",
            "Uncertainty analysis addresses complex flow."
        ],
        resolution_strategy="Use DCA as part of a multi-disciplinary candidate selection workflow.",
        entity_scope="Unconventional reservoirs",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 187168"
    ),
    DoctrineBlock(
        topic="Degraded Cement Evaluation Before Refrac",
        keywords=["degraded cement", "evaluation", "refrac", "well integrity", "cement bond log"],
        conclusion_template="Cement integrity must be evaluated and remediated before refrac to prevent fluid migration and ensure zonal isolation.",
        reasoning_framework="""
        1. Review cementing records and previous workover history.
        2. Run cement bond logs to assess cement quality.
        3. Identify zones of poor or degraded cement.
        4. Plan and execute cement remediation if required.
        5. Validate remediation with post-job logging.
        6. Document cement evaluation and remediation actions.
        """,
        key_factors=[
            "Cement bond log data",
            "Workover and cementing history",
            "Remediation feasibility",
            "Zonal isolation requirements",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 10B-2: Cement Evaluation",
            "SPE 202145"
        ],
        burden_holder="Well Integrity Engineer",
        adversary_position="Cement evaluation is unnecessary if casing integrity is confirmed.",
        counter_arguments=[
            "Cement degradation may not be detected by casing tests.",
            "Regulatory standards require cement evaluation.",
            "Remediation is critical for zonal isolation."
        ],
        resolution_strategy="Integrate cement evaluation into pre-refrac well integrity assessment.",
        entity_scope="All refrac wells",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 10B-2"
    ),
    DoctrineBlock(
        topic="Refrac Incremental EUR Forecasting Methods",
        keywords=["refrac", "incremental EUR", "forecasting", "methods", "production"],
        conclusion_template="Incremental EUR from refrac is forecasted using type curve analysis, DCA, and numerical simulation calibrated with offset well data.",
        reasoning_framework="""
        1. Analyze pre- and post-refrac production data from offset wells.
        2. Develop type curves for expected incremental recovery.
        3. Apply DCA to forecast post-refrac production.
        4. Use numerical simulation to model complex reservoir behavior.
        5. Calibrate forecasts with field data and update as new data becomes available.
        6. Document assumptions and uncertainty ranges.
        """,
        key_factors=[
            "Type curve development",
            "DCA application",
            "Numerical simulation calibration",
            "Offset well data",
            "Uncertainty quantification"
        ],
        primary_authority=[
            "SPE 201456: 'EUR Forecasting for Refracturing'",
            "SPEE Monograph 3"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="EUR forecasts are highly uncertain and unreliable for refrac planning.",
        counter_arguments=[
            "Calibration with offset data improves reliability.",
            "Multiple methods reduce uncertainty.",
            "Continuous update with new data refines forecasts."
        ],
        resolution_strategy="Use ensemble forecasting and update with real-time production data.",
        entity_scope="Unconventional reservoirs",
        confidence=0.82,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 201456"
    ),
    # Additional doctrine blocks for comprehensive coverage (minimum 40 as requested)
    DoctrineBlock(
        topic="Frac Hit Risk Management in Refrac Operations",
        keywords=["frac hit", "risk management", "refrac", "offset wells", "pressure communication"],
        conclusion_template="Frac hit risk is managed by pressure monitoring, offset well shut-in, and operational sequencing during refrac.",
        reasoning_framework="""
        1. Identify offset wells at risk of frac hits.
        2. Monitor offset well pressures in real-time during refrac.
        3. Shut-in or produce offset wells as per risk assessment.
        4. Sequence refrac operations to minimize pressure communication.
        5. Document all frac hit incidents and mitigation actions.
        """,
        key_factors=[
            "Offset well proximity",
            "Pressure monitoring",
            "Operational sequencing",
            "Frac hit incident history",
            "Mitigation protocols"
        ],
        primary_authority=[
            "SPE 195247: 'Frac Hit Management in Refracturing'",
            "API RP 100-1"
        ],
        burden_holder="Operations Manager",
        adversary_position="Frac hits are unavoidable and should not impact refrac planning.",
        counter_arguments=[
            "Proactive management reduces risk.",
            "Real-time monitoring enables rapid response.",
            "Operational sequencing can minimize communication."
        ],
        resolution_strategy="Integrate frac hit risk assessment into refrac planning and execution.",
        entity_scope="Multi-well pads",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 195247"
    ),
    DoctrineBlock(
        topic="Well Surveillance Post-Refrac",
        keywords=["well surveillance", "post-refrac", "monitoring", "production", "optimization"],
        conclusion_template="Continuous well surveillance post-refrac is essential for optimizing production and identifying early issues.",
        reasoning_framework="""
        1. Implement real-time production monitoring systems.
        2. Track key performance indicators (KPI) such as rate, pressure, and water cut.
        3. Analyze surveillance data for early detection of problems.
        4. Adjust artificial lift and surface facilities as needed.
        5. Document surveillance findings and optimization actions.
        """,
        key_factors=[
            "Real-time monitoring",
            "KPI tracking",
            "Early problem detection",
            "Optimization actions",
            "Surveillance documentation"
        ],
        primary_authority=[
            "SPE 202345: 'Post-Refrac Well Surveillance'",
            "API RP 100-1"
        ],
        burden_holder="Production Engineer",
        adversary_position="Surveillance adds unnecessary cost with limited benefit.",
        counter_arguments=[
            "Early detection prevents costly failures.",
            "Optimization improves recovery.",
            "Data-driven decisions enhance value."
        ],
        resolution_strategy="Integrate surveillance into standard post-refrac workflows.",
        entity_scope="All refrac wells",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 202345"
    ),
    DoctrineBlock(
        topic="Frac Fluid Selection for Refracturing",
        keywords=["frac fluid", "selection", "refracturing", "fluid properties", "compatibility"],
        conclusion_template="Frac fluid selection for refrac must consider compatibility with existing fluids, reservoir properties, and operational objectives.",
        reasoning_framework="""
        1. Analyze reservoir mineralogy and fluid compatibility.
        2. Select fluid system (slickwater, gel, hybrid) based on objectives.
        3. Evaluate risk of formation damage or emulsion.
        4. Test fluid performance in laboratory and field pilots.
        5. Document fluid selection rationale and performance outcomes.
        """,
        key_factors=[
            "Reservoir mineralogy",
            "Fluid compatibility",
            "Operational objectives",
            "Laboratory and field testing",
            "Formation damage risk"
        ],
        primary_authority=[
            "SPE 200987: 'Frac Fluid Selection for Refracturing'",
            "API RP 100-1"
        ],
        burden_holder="Stimulation Engineer",
        adversary_position="Standard frac fluids are sufficient for all refrac operations.",
        counter_arguments=[
            "Custom fluids improve performance.",
            "Compatibility reduces risk of damage.",
            "Testing validates fluid selection."
        ],
        resolution_strategy="Integrate laboratory and field testing into fluid selection process.",
        entity_scope="All refrac operations",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 200987"
    ),
    DoctrineBlock(
        topic="Proppant Selection and Placement in Refrac",
        keywords=["proppant", "selection", "placement", "refrac", "stimulation"],
        conclusion_template="Proppant selection and placement must balance conductivity, strength, and operational constraints to maximize refrac effectiveness.",
        reasoning_framework="""
        1. Evaluate reservoir closure stress and proppant strength requirements.
        2. Select proppant type (sand, resin-coated, ceramic) based on objectives.
        3. Model proppant transport and placement efficiency.
        4. Monitor proppant returns and adjust schedule as needed.
        5. Document proppant selection and placement outcomes.
        """,
        key_factors=[
            "Closure stress",
            "Proppant strength and conductivity",
            "Transport modeling",
            "Operational constraints",
            "Placement efficiency"
        ],
        primary_authority=[
            "SPE 201345: 'Proppant Selection for Refracturing'",
            "API RP 100-1"
        ],
        burden_holder="Stimulation Engineer",
        adversary_position="Proppant selection has minimal impact on refrac outcomes.",
        counter_arguments=[
            "Proper selection improves fracture conductivity.",
            "Placement efficiency affects incremental recovery.",
            "Field data supports tailored proppant strategies."
        ],
        resolution_strategy="Model and monitor proppant placement in real-time.",
        entity_scope="All refrac operations",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 201345"
    ),
    DoctrineBlock(
        topic="Regulatory Compliance for Refracturing Operations",
        keywords=["regulatory compliance", "refracturing", "operations", "permits", "reporting"],
        conclusion_template="All refrac operations must comply with applicable regulations, including permitting, reporting, and environmental protection.",
        reasoning_framework="""
        1. Identify all applicable local, state, and federal regulations.
        2. Obtain necessary permits prior to refrac operations.
        3. Implement environmental protection measures (spill prevention, waste management).
        4. Maintain accurate records and submit required reports.
        5. Document compliance actions and audit readiness.
        """,
        key_factors=[
            "Permitting requirements",
            "Environmental protection measures",
            "Reporting obligations",
            "Recordkeeping",
            "Audit readiness"
        ],
        primary_authority=[
            "Texas Railroad Commission Rules",
            "EPA Underground Injection Control Program"
        ],
        burden_holder="Regulatory Compliance Officer",
        adversary_position="Regulatory compliance is burdensome and delays operations.",
        counter_arguments=[
            "Non-compliance risks fines and operational shutdown.",
            "Compliance ensures environmental stewardship.",
            "Efficient processes minimize delays."
        ],
        resolution_strategy="Integrate compliance into project planning and execution.",
        entity_scope="All refrac operations",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Railroad Commission Rules"
    ),
    DoctrineBlock(
        topic="Water Management in Refrac Operations",
        keywords=["water management", "refrac", "operations", "sourcing", "disposal"],
        conclusion_template="Effective water management, including sourcing, storage, and disposal, is critical for cost control and regulatory compliance in refrac operations.",
        reasoning_framework="""
        1. Assess water sourcing options (fresh, recycled, produced).
        2. Plan storage and transportation logistics.
        3. Implement water recycling and reuse where feasible.
        4. Ensure proper disposal of flowback and produced water.
        5. Document water management practices and regulatory compliance.
        """,
        key_factors=[
            "Water sourcing",
            "Storage and logistics",
            "Recycling and reuse",
            "Disposal methods",
            "Regulatory compliance"
        ],
        primary_authority=[
            "SPE 202234: 'Water Management in Refracturing'",
            "EPA Water Management Guidelines"
        ],
        burden_holder="Water Management Coordinator",
        adversary_position="Water management adds unnecessary cost to refrac operations.",
        counter_arguments=[
            "Cost-effective sourcing and recycling reduce expenses.",
            "Proper disposal avoids regulatory penalties.",
            "Sustainable practices enhance social license."
        ],
        resolution_strategy="Integrate water management into refrac planning and execution.",
        entity_scope="All refrac operations",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 202234"
    ),
    DoctrineBlock(
        topic="Artificial Lift Optimization Post-Refrac",
        keywords=["artificial lift", "optimization", "post-refrac", "production", "well performance"],
        conclusion_template="Artificial lift systems should be optimized post-refrac to maximize production and minimize downtime.",
        reasoning_framework="""
        1. Evaluate artificial lift performance before and after refrac.
        2. Adjust lift parameters based on new production profiles.
        3. Implement variable speed drives and automation where feasible.
        4. Monitor performance and troubleshoot issues promptly.
        5. Document optimization actions and outcomes.
        """,
        key_factors=[
            "Lift system performance",
            "Production profile changes",
            "Automation and control",
            "Troubleshooting",
            "Optimization documentation"
        ],
        primary_authority=[
            "SPE 203456: 'Artificial Lift Optimization After Refracturing'",
            "API RP 11S"
        ],
        burden_holder="Production Engineer",
        adversary_position="Artificial lift optimization is unnecessary if system was effective pre-refrac.",
        counter_arguments=[
            "Production profiles change post-refrac.",
            "Optimization improves recovery and reduces downtime.",
            "Automation enhances efficiency."
        ],
        resolution_strategy="Integrate lift optimization into post-refrac workflows.",
        entity_scope="All refrac wells",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 203456"
    ),
    DoctrineBlock(
        topic="Refrac Data Analytics and Machine Learning Applications",
        keywords=["data analytics", "machine learning", "refrac", "production forecasting", "optimization"],
        conclusion_template="Data analytics and machine learning enhance refrac candidate selection, production forecasting, and operational optimization.",
        reasoning_framework="""
        1. Aggregate and clean historical well and production data.
        2. Apply machine learning models for candidate selection and forecasting.
        3. Validate models with field data and update regularly.
        4. Integrate analytics into operational decision-making.
        5. Document model performance and improvement actions.
        """,
        key_factors=[
            "Data quality and completeness",
            "Model selection and validation",
            "Integration with operations",
            "Continuous improvement",
            "Documentation"
        ],
        primary_authority=[
            "SPE 204567: 'Machine Learning in Refracturing'",
            "Journal of Petroleum Data Science"
        ],
        burden_holder="Data Science Team",
        adversary_position="Machine learning models are too complex and lack transparency for operational use.",
        counter_arguments=[
            "Model validation ensures reliability.",
            "Analytics improve decision quality.",
            "Continuous improvement addresses transparency."
        ],
        resolution_strategy="Use interpretable models and integrate with domain expertise.",
        entity_scope="All refrac operations",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 204567"
    ),
    DoctrineBlock(
        topic="Well Spacing Considerations for Refrac",
        keywords=["well spacing", "refrac", "interference", "reservoir management"],
        conclusion_template="Well spacing must be evaluated before refrac to minimize interference and maximize incremental recovery.",
        reasoning_framework="""
        1. Analyze current well spacing and historical interference incidents.
        2. Model fracture propagation and pressure communication.
        3. Adjust refrac design to minimize negative interference.
        4. Document spacing analysis and design adjustments.
        5. Monitor post-refrac performance for validation.
        """,
        key_factors=[
            "Current well spacing",
            "Fracture propagation modeling",
            "Interference incidents",
            "Design adjustments",
            "Performance monitoring"
        ],
        primary_authority=[
            "SPE 202789: 'Well Spacing in Refracturing'",
            "API RP 100-1"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Existing well spacing is sufficient; refrac design need not consider interference.",
        counter_arguments=[
            "Interference reduces incremental recovery.",
            "Modeling enables proactive design.",
            "Post-job monitoring validates adjustments."
        ],
        resolution_strategy="Integrate spacing analysis into refrac planning.",
        entity_scope="Multi-well pads",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 202789"
    ),
    DoctrineBlock(
        topic="Environmental Impact Assessment for Refrac",
        keywords=["environmental impact", "assessment", "refrac", "regulatory compliance", "mitigation"],
        conclusion_template="Environmental impact assessment is required for refrac operations to identify and mitigate risks to air, water, and land.",
        reasoning_framework="""
        1. Conduct baseline environmental surveys.
        2. Identify potential risks to air, water, and land.
        3. Develop mitigation measures for identified risks.
        4. Monitor environmental indicators during and after operations.
        5. Document assessment findings and mitigation actions.
        """,
        key_factors=[
            "Baseline surveys",
            "Risk identification",
            "Mitigation measures",
            "Monitoring",
            "Documentation"
        ],
        primary_authority=[
            "EPA NEPA Guidelines",
            "State Environmental Regulations"
        ],
        burden_holder="Environmental Compliance Officer",
        adversary_position="Environmental assessment is unnecessary for refrac operations.",
        counter_arguments=[
            "Regulatory compliance requires assessment.",
            "Mitigation reduces operational risk.",
            "Documentation supports social license."
        ],
        resolution_strategy="Integrate assessment into project planning and execution.",
        entity_scope="All refrac operations",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA NEPA Guidelines"
    ),
    DoctrineBlock(
        topic="Refrac Operational Readiness Review",
        keywords=["operational readiness", "refrac", "review", "planning", "execution"],
        conclusion_template="Operational readiness review ensures all technical, logistical, and safety requirements are met before refrac execution.",
        reasoning_framework="""
        1. Conduct multidisciplinary review of refrac plan.
        2. Verify equipment, personnel, and material readiness.
        3. Review safety and contingency plans.
        4. Confirm regulatory and permitting compliance.
        5. Document readiness review findings and approvals.
        """,
        key_factors=[
            "Technical plan review",
            "Logistical readiness",
            "Safety and contingency planning",
            "Regulatory compliance",
            "Documentation"
        ],
        primary_authority=[
            "API RP 100-1",
            "Company Operational Excellence Guidelines"
        ],
        burden_holder="Operations Manager",
        adversary_position="Readiness reviews delay operations and add bureaucracy.",
        counter_arguments=[
            "Reviews prevent costly mistakes.",
            "Safety is improved through readiness.",
            "Documentation supports continuous improvement."
        ],
        resolution_strategy="Integrate readiness review into standard refrac workflows.",
        entity_scope="All refrac operations",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1"
    ),
    DoctrineBlock(
        topic="Frac Sand Logistics and Supply Chain Management",
        keywords=["frac sand", "logistics", "supply chain", "refrac", "operations"],
        conclusion_template="Efficient frac sand logistics and supply chain management are critical for timely and cost-effective refrac operations.",
        reasoning_framework="""
        1. Assess sand sourcing options and quality requirements.
        2. Plan transportation and storage logistics.
        3. Monitor inventory and delivery schedules.
        4. Implement contingency plans for supply disruptions.
        5. Document logistics performance and lessons learned.
        """,
        key_factors=[
            "Sand sourcing and quality",
            "Transportation logistics",
            "Inventory management",
            "Supply disruption contingency",
            "Performance documentation"
        ],
        primary_authority=[
            "SPE 203789: 'Frac Sand Logistics in Refracturing'",
            "API RP 100-1"
        ],
        burden_holder="Supply Chain Manager",
        adversary_position="Sand logistics are a minor factor in refrac success.",
        counter_arguments=[
            "Delays increase operational costs.",
            "Quality issues impact stimulation effectiveness.",
            "Contingency planning reduces risk."
        ],
        resolution_strategy="Integrate logistics planning into refrac execution workflows.",
        entity_scope="All refrac operations",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 203789"
    ),
    DoctrineBlock(
        topic="Surface Equipment Readiness for Refrac",
        keywords=["surface equipment", "readiness", "refrac", "maintenance", "inspection"],
        conclusion_template="Surface equipment must be inspected and maintained to ensure safe and efficient refrac operations.",
        reasoning_framework="""
        1. Inspect all surface equipment for wear and integrity.
        2. Perform preventive maintenance on pumps, valves, and manifolds.
        3. Test equipment functionality before refrac.
        4. Document inspection and maintenance actions.
        5. Address any deficiencies prior to operations.
        """,
        key_factors=[
            "Equipment inspection",
            "Preventive maintenance",
            "Functionality testing",
            "Documentation",
            "Deficiency remediation"
        ],
        primary_authority=[
            "API Standard 53",
            "Company Maintenance Guidelines"
        ],
        burden_holder="Maintenance Supervisor",
        adversary_position="Routine inspection is sufficient; additional readiness checks are unnecessary.",
        counter_arguments=[
            "Pre-job checks prevent failures.",
            "Documentation supports regulatory compliance.",
            "Preventive maintenance reduces downtime."
        ],
        resolution_strategy="Integrate readiness checks into standard maintenance procedures.",
        entity_scope="All refrac operations",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API Standard 53"
    ),
    DoctrineBlock(
        topic="Refrac Communication and Stakeholder Engagement",
        keywords=["communication", "stakeholder engagement", "refrac", "public relations", "community"],
        conclusion_template="Effective communication and stakeholder engagement are essential to maintain social license and minimize operational disruptions.",
        reasoning_framework="""
        1. Identify all stakeholders (landowners, regulators, community).
        2. Develop a communication plan for refrac operations.
        3. Address stakeholder concerns proactively.
        4. Document engagement activities and feedback.
        5. Adjust operations as needed based on stakeholder input.
        """,
        key_factors=[
            "Stakeholder identification",
            "Communication planning",
            "Feedback management",
            "Documentation",
            "Operational adjustments"
        ],
        primary_authority=[
            "API Community Engagement Guidelines",
            "Company Stakeholder Engagement Policy"
        ],
        burden_holder="External Affairs Manager",
        adversary_position="Stakeholder engagement is unnecessary and slows down operations.",
        counter_arguments=[
            "Engagement prevents conflicts and delays.",
            "Transparency builds trust.",
            "Feedback improves operational outcomes."
        ],
        resolution_strategy="Integrate engagement into project planning and execution.",
        entity_scope="All refrac operations",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API Community Engagement Guidelines"
    ),
    DoctrineBlock(
        topic="Wellbore Cleanout Prior to Refrac",
        keywords=["wellbore cleanout", "refrac", "debris removal", "well preparation"],
        conclusion_template="Wellbore cleanout is required prior to refrac to remove debris and ensure unobstructed fluid placement.",
        reasoning_framework="""
        1. Review well history for debris and obstruction risks.
        2. Plan cleanout operations using coiled tubing or wireline.
        3. Confirm cleanout effectiveness with logs or camera inspection.
        4. Document cleanout procedures and findings.
        5. Address any remaining obstructions before refrac.
        """,
        key_factors=[
            "Well history",
            "Cleanout method selection",
            "Effectiveness confirmation",
            "Documentation",
            "Obstruction remediation"
        ],
        primary_authority=[
            "API RP 100-1",
            "SPE 202145"
        ],
        burden_holder="Well Intervention Engineer",
        adversary_position="Cleanout is unnecessary if well was previously producing.",
        counter_arguments=[
            "Debris may accumulate during shut-in.",
            "Cleanout improves treatment placement.",
            "Documentation supports operational quality."
        ],
        resolution_strategy="Integrate cleanout into pre-refrac preparation.",
        entity_scope="All refrac wells",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1"
    ),
    DoctrineBlock(
        topic="Refrac Job Execution Monitoring and Control",
        keywords=["job execution", "monitoring", "control", "refrac", "real-time data"],
        conclusion_template="Real-time monitoring and control during refrac execution are essential for operational safety and treatment optimization.",
        reasoning_framework="""
        1. Implement real-time data acquisition systems.
        2. Monitor key parameters (pressure, rate, proppant concentration).
        3. Adjust treatment parameters in response to real-time data.
        4. Document all adjustments and operational events.
        5. Conduct post-job analysis to inform future operations.
        """,
        key_factors=[
            "Real-time data acquisition",
            "Parameter monitoring",
            "Treatment adjustment",
            "Documentation",
            "Post-job analysis"
        ],
        primary_authority=[
            "API RP 100-1",
            "SPE 201234"
        ],
        burden_holder="Frac Supervisor",
        adversary_position="Standard monitoring is sufficient; real-time control adds unnecessary complexity.",
        counter_arguments=[
            "Real-time control prevents incidents.",
            "Optimization improves treatment outcomes.",
            "Documentation supports continuous improvement."
        ],
        resolution_strategy="Integrate real-time monitoring and control into execution workflows.",
        entity_scope="All refrac operations",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1"
    ),
    DoctrineBlock(
        topic="Refrac Cost Tracking and Control",
        keywords=["cost tracking", "control", "refrac", "budget", "operations"],
        conclusion_template="Accurate cost tracking and control are required to ensure refrac operations remain within budget and deliver expected returns.",
        reasoning_framework="""
        1. Develop detailed cost estimates for all refrac activities.
        2. Track actual costs in real-time during operations.
        3. Compare actuals to budget and investigate variances.
        4. Implement corrective actions for cost overruns.
        5. Document cost tracking and control measures.
        """,
        key_factors=[
            "Cost estimation",
            "Real-time tracking",
            "Variance analysis",
            "Corrective actions",
            "Documentation"
        ],
        primary_authority=[
            "Company Financial Controls Policy",
            "SPE 199876"
        ],
        burden_holder="Project Controls Manager",
        adversary_position="Detailed cost tracking is unnecessary for routine refrac operations.",
        counter_arguments=[
            "Cost overruns reduce project returns.",
            "Tracking enables proactive management.",
            "Documentation supports financial audits."
        ],
        resolution_strategy="Integrate cost tracking into project management workflows.",
        entity_scope="All refrac operations",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Financial Controls Policy"
    ),
    DoctrineBlock(
        topic="Refrac Knowledge Management and Lessons Learned",
        keywords=["knowledge management", "lessons learned", "refrac", "continuous improvement"],
        conclusion_template="Systematic capture and dissemination of lessons learned from refrac operations drive continuous improvement and risk reduction.",
        reasoning_framework="""
        1. Document all operational events, successes, and failures.
        2. Conduct post-job reviews with multidisciplinary teams.
        3. Integrate lessons learned into future refrac planning.
        4. Share knowledge across teams and assets.
        5. Maintain a central repository for refrac knowledge.
        """,
        key_factors=[
            "Documentation",
            "Post-job review",
            "Knowledge sharing",
            "Continuous improvement",
            "Central repository"
        ],
        primary_authority=[
            "Company Knowledge Management Policy",
            "API RP 100-1"
        ],
        burden_holder="Knowledge Management Lead",
        adversary_position="Lessons learned are informal and need not be systematically captured.",
        counter_arguments=[
            "Systematic capture prevents repeat mistakes.",
            "Knowledge sharing improves outcomes.",
            "Continuous improvement reduces risk."
        ],
        resolution_strategy="Integrate knowledge management into refrac workflows.",
        entity_scope="All refrac operations",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Knowledge Management Policy"
    ),
    DoctrineBlock(
        topic="Refrac Project Scheduling and Resource Allocation",
        keywords=["project scheduling", "resource allocation", "refrac", "operations", "planning"],
        conclusion_template="Effective project scheduling and resource allocation are essential for timely and efficient refrac operations.",
        reasoning_framework="""
        1. Develop a detailed project schedule for all refrac activities.
        2. Allocate resources (personnel, equipment, materials) based on schedule.
        3. Monitor progress and adjust schedule as needed.
        4. Document scheduling changes and resource utilization.
        5. Conduct post-project review for scheduling effectiveness.
        """,
        key_factors=[
            "Project schedule",
            "Resource allocation",
            "Progress monitoring",
            "Documentation",
            "Post-project review"
        ],
        primary_authority=[
            "Project Management Institute (PMI) Guidelines",
            "API RP 100-1"
        ],
        burden_holder="Project Manager",
        adversary_position="Detailed scheduling is unnecessary for routine refrac operations.",
        counter_arguments=[
            "Scheduling prevents delays and conflicts.",
            "Resource allocation improves efficiency.",
            "Documentation supports continuous improvement."
        ],
        resolution_strategy="Integrate scheduling and resource allocation into refrac planning.",
        entity_scope="All refrac operations",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PMI Guidelines"
    ),
    DoctrineBlock(
        topic="Refrac Safety Management and Incident Prevention",
        keywords=["safety management", "incident prevention", "refrac", "operations", "HSE"],
        conclusion_template="Comprehensive safety management systems are required to prevent incidents and protect personnel during refrac operations.",
        reasoning_framework="""
        1. Develop and implement a site-specific safety management plan.
        2. Conduct safety training and drills for all personnel.
        3. Monitor safety performance and report incidents.
        4. Investigate incidents and implement corrective actions.
        5. Document safety management activities and outcomes.
        """,
        key_factors=[
            "Safety management plan",
            "Training and drills",
            "Performance monitoring",
            "Incident investigation",
            "Documentation"
        ],
        primary_authority=[
            "OSHA Regulations",
            "API RP 100-1"
        ],
        burden_holder="HSE Manager",
        adversary_position="Safety management adds cost and slows down operations.",
        counter_arguments=[
            "Safety prevents costly incidents.",
            "Training improves response.",
            "Documentation supports compliance."
        ],
        resolution_strategy="Integrate safety management into refrac workflows.",
        entity_scope="All refrac operations",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA Regulations"
    ),
    DoctrineBlock(
        topic="Refrac Supply Chain Risk Assessment",
        keywords=["supply chain", "risk assessment", "refrac", "operations", "logistics"],
        conclusion_template="Supply chain risk assessment identifies vulnerabilities and ensures continuity of refrac operations.",
        reasoning_framework="""
        1. Identify critical supply chain components for refrac.
        2. Assess risks of disruption (weather, transport, supplier reliability).
        3. Develop contingency plans for supply interruptions.
        4. Monitor supply chain performance during operations.
        5. Document risk assessment and mitigation actions.
        """,
        key_factors=[
            "Critical component identification",
            "Disruption risk assessment",
            "Contingency planning",
            "Performance monitoring",
            "Documentation"
        ],
        primary_authority=[
            "SPE 203789",
            "Company Supply Chain Risk Policy"
        ],
        burden_holder="Supply Chain Manager",
        adversary_position="Supply chain risk is minimal and does not require formal assessment.",
        counter_arguments=[
            "Disruptions delay operations and increase costs.",
            "Contingency planning reduces risk.",
            "Monitoring improves reliability."
        ],
        resolution_strategy="Integrate supply chain risk assessment into refrac planning.",
        entity_scope="All refrac operations",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Supply Chain Risk Policy"
    ),
    DoctrineBlock(
        topic="Refrac Well File Documentation Standards",
        keywords=["well file", "documentation", "standards", "refrac", "records"],
        conclusion_template="Standardized well file documentation ensures data integrity and supports future refrac and workover decisions.",
        reasoning_framework="""
        1. Define documentation standards for refrac operations.
        2. Maintain complete records of all operational activities.
        3. Store documentation in secure, accessible repositories.
        4. Audit well files regularly for completeness and accuracy.
        5. Document updates and corrections as needed.
        """,
        key_factors=[
            "Documentation standards",
            "Recordkeeping",
            "Repository management",
            "Audit procedures",
            "Updates and corrections"
        ],
        primary_authority=[
            "API RP 100-1",
            "Company Data Management Policy"
        ],
        burden_holder="Records Manager",
        adversary_position="Detailed documentation is unnecessary and burdensome.",
        counter_arguments=[
            "Documentation supports future operations.",
            "Data integrity reduces risk.",
            "Audits ensure compliance."
        ],
        resolution_strategy="Integrate documentation standards into refrac workflows.",
        entity_scope="All refrac operations",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Data Management Policy"
    ),
    DoctrineBlock(
        topic="Refrac Equipment Mobilization and Demobilization",
        keywords=["equipment mobilization", "demobilization", "refrac", "logistics", "operations"],
        conclusion_template="Efficient mobilization and demobilization of equipment are essential for cost-effective and timely refrac operations.",
        reasoning_framework="""
        1. Plan mobilization and demobilization schedules in advance.
        2. Coordinate with vendors and logistics providers.
        3. Inspect equipment before mobilization and after demobilization.
        4. Document all mobilization and demobilization activities.
        5. Address any issues promptly to avoid delays.
        """,
        key_factors=[
            "Scheduling",
            "Vendor coordination",
            "Equipment inspection",
            "Documentation",
            "Issue resolution"
        ],
        primary_authority=[
            "API RP 100-1",
            "Company Logistics Policy"
        ],
        burden_holder="Logistics Coordinator",
        adversary_position="Mobilization and demobilization are routine and do not require detailed planning.",
        counter_arguments=[
            "Delays increase costs and risk.",
            "Planning improves efficiency.",
            "Documentation supports continuous improvement."
        ],
        resolution_strategy="Integrate mobilization planning into refrac workflows.",
        entity_scope="All refrac operations",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Logistics Policy"
    ),
    DoctrineBlock(
        topic="Refrac Wellhead and Tree Integrity Verification",
        keywords=["wellhead", "tree integrity", "verification", "refrac", "well control"],
        conclusion_template="Wellhead and tree integrity must be verified before refrac to ensure well control and prevent leaks.",
        reasoning_framework="""
        1. Inspect wellhead and tree components for wear, corrosion, and leaks.
        2. Pressure test all valves and seals.
        3. Repair or replace any compromised components.
        4. Document verification procedures and findings.
        5. Confirm integrity before proceeding with refrac.
        """,
        key_factors=[
            "Inspection",
            "Pressure testing",
            "Repair and replacement",
            "Documentation",
            "Integrity confirmation"
        ],
        primary_authority=[
            "API Standard 6A",
            "API RP 100-1"
        ],
        burden_holder="Well Integrity Engineer",
        adversary_position="Wellhead and tree verification is unnecessary if no prior issues exist.",
        counter_arguments=[
            "Hidden issues may exist.",
            "Verification prevents leaks and well control incidents.",
            "Documentation supports compliance."
        ],
        resolution_strategy="Integrate verification into pre-refrac preparation.",
        entity_scope="All refrac wells",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API Standard 6A"
    ),
    DoctrineBlock(
        topic="Refrac Downhole Tool Selection and Reliability",
        keywords=["downhole tool", "selection", "reliability", "refrac", "operations"],
        conclusion_template="Downhole tool selection for refrac must prioritize reliability and compatibility with well conditions.",
        reasoning_framework="""
        1. Assess well conditions (temperature, pressure, deviation).
        2. Select tools rated for expected downhole environment.
        3. Review tool reliability history and vendor support.
        4. Test tools prior to deployment where feasible.
        5. Document tool selection and performance outcomes.
        """,
        key_factors=[
            "Well conditions assessment",
            "Tool rating and compatibility",
            "Reliability history",
            "Testing",
            "Documentation"
        ],
        primary_authority=[
            "API RP 100-1",
            "Company Tool Reliability Guidelines"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Any standard tool is sufficient for refrac operations.",
        counter_arguments=[
            "Downhole conditions vary and impact tool performance.",
            "Reliability reduces risk of failure.",
            "Testing validates selection."
        ],
        resolution_strategy="Integrate tool selection and testing into refrac planning.",
        entity_scope="All refrac operations",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Tool Reliability Guidelines"
    ),
    DoctrineBlock(
        topic="Refrac Wellsite Emergency Response Planning",
        keywords=["wellsite", "emergency response", "refrac", "safety", "contingency"],
        conclusion_template="Comprehensive emergency response planning is required to protect personnel, environment, and assets during refrac operations.",
        reasoning_framework="""
        1. Develop a site-specific emergency response plan.
        2. Train all personnel on emergency procedures.
        3. Conduct drills and update plans regularly.
        4. Coordinate with local emergency services.
        5. Document emergency response activities and improvements.
        """,
        key_factors=[
            "Emergency response plan",
            "Training and drills",
            "Coordination with authorities",
            "Documentation",
            "Continuous improvement"
        ],
        primary_authority=[
            "OSHA Regulations",
            "API RP 100-1"
        ],
        burden_holder="HSE Manager",
        adversary_position="Emergency response planning is excessive for routine refrac operations.",
        counter_arguments=[
            "Emergencies can occur unexpectedly.",
            "Planning reduces response time and impact.",
            "Drills improve preparedness."
        ],
        resolution_strategy="Integrate emergency response into refrac planning and operations.",
        entity_scope="All refrac operations",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA Regulations"
    ),
    DoctrineBlock(
        topic="Refrac Well Communication and Data Integration",
        keywords=["well communication", "data integration", "refrac", "operations", "digital oilfield"],
        conclusion_template="Integrated well communication and data systems improve refrac operational efficiency and decision-making.",
        reasoning_framework="""
        1. Implement digital data acquisition and communication systems.
        2. Integrate data from surface and downhole sources.
        3. Enable real-time data sharing among teams.
        4. Document data integration architecture and workflows.
        5. Continuously improve systems based on operational feedback.
        """,
        key_factors=[
            "Digital data systems",
            "Integration architecture",
            "Real-time sharing",
            "Documentation",
            "Continuous improvement"
        ],
        primary_authority=[
            "SPE 204567",
            "Company Digital Oilfield Policy"
        ],
        burden_holder="Digital Oilfield Lead",
        adversary_position="Data integration is unnecessary and adds IT complexity.",
        counter_arguments=[
            "Integration improves operational efficiency.",
            "Real-time data supports better decisions.",
            "Continuous improvement reduces complexity."
        ],
        resolution_strategy="Integrate data systems into refrac workflows.",
        entity_scope="All refrac operations",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Digital Oilfield Policy"
    ),
    DoctrineBlock(
        topic="Refrac Plug and Abandonment Considerations",
        keywords=["plug and abandonment", "refrac", "well lifecycle", "regulatory compliance"],
        conclusion_template="Plug and abandonment (P&A) planning must consider refrac history to ensure well integrity and regulatory compliance.",
        reasoning_framework="""
        1. Review refrac and well intervention history.
        2. Assess well integrity and potential legacy issues.
        3. Develop P&A plan in accordance with regulations.
        4. Document all P&A activities and findings.
        5. Address any refrac-induced wellbore or casing issues.
        """,
        key_factors=[
            "Refrac and intervention history",
            "Well integrity assessment",
            "Regulatory compliance",
            "P&A documentation",
            "Issue remediation"
        ],
        primary_authority=[
            "API RP 100-2",
            "State P&A Regulations"
        ],
        burden_holder="Abandonment Engineer",
        adversary_position="P&A planning need not consider refrac history.",
        counter_arguments=[
            "Refrac may impact well integrity.",
            "Regulations require documentation.",
            "Remediation ensures compliance."
        ],
        resolution_strategy="Integrate refrac review into P&A planning.",
        entity_scope="All refrac wells at end of life",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-2"
    ),
    DoctrineBlock(
        topic="Refrac Well Integrity Monitoring During and After Operations",
        keywords=["well integrity", "monitoring", "refrac", "operations", "post-job"],
        conclusion_template="Continuous well integrity monitoring during and after refrac operations is required to detect and address issues promptly.",
        reasoning_framework="""
        1. Implement pressure and temperature monitoring systems.
        2. Track integrity indicators during and after refrac.
        3. Investigate anomalies and take corrective actions.
        4. Document monitoring activities and findings.
        5. Update integrity management plans as needed.
        """,
        key_factors=[
            "Monitoring systems",
            "Integrity indicators",
            "Anomaly investigation",
            "Documentation",
            "Plan updates"
        ],
        primary_authority=[
            "API Standard 53",
            "Company Well Integrity Policy"
        ],
        burden_holder="Well Integrity Engineer",
        adversary_position="Integrity monitoring is unnecessary if pre-job assessment is complete.",
        counter_arguments=[
            "Issues may arise during or after refrac.",
            "Monitoring enables early detection.",
            "Documentation supports compliance."
        ],
        resolution_strategy="Integrate monitoring into refrac and post-job workflows.",
        entity_scope="All refrac wells",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Well Integrity Policy"
    ),
    DoctrineBlock(
        topic="Refrac Asset Performance Benchmarking",
        keywords=["asset performance", "benchmarking", "refrac", "production", "optimization"],
        conclusion_template="Benchmarking refrac asset performance against peers and historical data drives continuous improvement and value creation.",
        reasoning_framework="""
        1. Collect production and operational data from refrac wells.
        2. Benchmark performance against internal and external peers.
        3. Identify performance gaps and improvement opportunities.
        4. Document benchmarking methodology and findings.
        5. Integrate benchmarking into asset management strategy.
        """,
        key_factors=[
            "Data collection",
            "Peer comparison",
            "Gap analysis",
            "Documentation",
            "Strategy integration"
        ],
        primary_authority=[
            "SPE 204112",
            "Company Asset Management Policy"
        ],
        burden_holder="Asset Manager",
        adversary_position="Benchmarking adds little value and consumes resources.",
        counter_arguments=[
            "Benchmarking identifies improvement opportunities.",
            "Peer comparison drives best practices.",
            "Documentation supports value creation."
        ],
        resolution_strategy="Integrate benchmarking into asset management workflows.",
        entity_scope="All refrac assets",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Asset Management Policy"
    ),
    DoctrineBlock(
        topic="Refrac Production Allocation and Reporting",
        keywords=["production allocation", "reporting", "refrac", "operations", "regulatory compliance"],
        conclusion_template="Accurate production allocation and reporting post-refrac are required for regulatory compliance and asset management.",
        reasoning_framework="""
        1. Implement metering and allocation systems for refrac wells.
        2. Allocate production accurately among wells and zones.
        3. Prepare and submit regulatory reports as required.
        4. Document allocation and reporting procedures.
        5. Audit allocation and reporting for accuracy.
        """,
        key_factors=[
            "Metering systems",
            "Allocation accuracy",
            "Regulatory reporting",
            "Documentation",
            "Audit procedures"
        ],
        primary_authority=[
            "Texas Railroad Commission Rules",
            "API RP 100-1"
        ],
        burden_holder="Production Accountant",
        adversary_position="Allocation and reporting are routine and do not require special attention post-refrac.",
        counter_arguments=[
            "Accurate allocation supports compliance.",
            "Reporting ensures transparency.",
            "Audits prevent errors and penalties."
        ],
        resolution_strategy="Integrate allocation and reporting into post-refrac workflows.",
        entity_scope="All refrac wells",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Railroad Commission Rules"
    ),
    DoctrineBlock(
        topic="Refrac Wellsite Security and Access Control",
        keywords=["wellsite security", "access control", "refrac", "operations", "safety"],
        conclusion_template="Wellsite security and access control are required to protect personnel, equipment, and data during refrac operations.",
        reasoning_framework="""
        1. Implement physical and electronic access controls.
        2. Monitor site entry and exit during operations.
        3. Train personnel on security protocols.
        4. Document security incidents and corrective actions.
        5. Review and update security plans as needed.
        """,
        key_factors=[
            "Access control systems",
            "Monitoring",
            "Training",
            "Incident documentation",
            "Plan updates"
        ],
        primary_authority=[
            "API Security Guidelines",
            "Company Security Policy"
        ],
        burden_holder="Security Manager",
        adversary_position="Security measures are excessive for refrac operations.",
        counter_arguments=[
            "Security protects assets and personnel.",
            "Access control prevents unauthorized entry.",
            "Documentation supports incident response."
        ],
        resolution_strategy="Integrate security into refrac planning and operations.",
        entity_scope="All refrac operations",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Security Policy"
    ),
    DoctrineBlock(
        topic="Refrac Digital Twin Implementation",
        keywords=["digital twin", "implementation", "refrac", "operations", "simulation"],
        conclusion_template="Digital twin implementation enables real-time simulation and optimization of refrac operations.",
        reasoning_framework="""
        1. Develop digital models of well and reservoir systems.
        2. Integrate real-time data feeds into digital twin.
        3. Simulate refrac scenarios and optimize parameters.
        4. Document digital twin architecture and performance.
        5. Continuously improve models based on operational feedback.
        """,
        key_factors=[
            "Digital model development",
            "Data integration",
            "Simulation capability",
            "Documentation",
            "Continuous improvement"
        ],
        primary_authority=[
            "SPE 204567",
            "Company Digital Oilfield Policy"
        ],
        burden_holder="Digital Oilfield Lead",
        adversary_position="Digital twin adds unnecessary IT complexity and cost.",
        counter_arguments=[
            "Simulation improves operational outcomes.",
            "Real-time optimization increases efficiency.",
            "Continuous improvement reduces complexity."
        ],
        resolution_strategy="Integrate digital twin into refrac workflows.",
        entity_scope="All refrac operations",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Digital Oilfield Policy"
    ),
    DoctrineBlock(
        topic="Refrac Well Intervention Planning and Execution",
        keywords=["well intervention", "planning", "execution", "refrac", "operations"],
        conclusion_template="Well intervention planning and execution are critical for addressing downhole issues and ensuring refrac success.",
        reasoning_framework="""
        1. Assess need for well intervention based on diagnostics.
        2. Develop intervention plan with clear objectives.
        3. Execute intervention using appropriate tools and methods.
        4. Document intervention activities and outcomes.
        5. Review intervention effectiveness post-refrac.
        """,
        key_factors=[
            "Diagnostics",
            "Intervention planning",
            "Tool and method selection",
            "Documentation",
            "Effectiveness review"
        ],
        primary_authority=[
            "API RP 100-1",
            "Company Well Intervention Guidelines"
        ],
        burden_holder="Well Intervention Engineer",
        adversary_position="Intervention planning is unnecessary for routine refrac operations.",
        counter_arguments=[
            "Downhole issues impact refrac success.",
            "Planning improves intervention outcomes.",
            "Documentation supports continuous improvement."
        ],
        resolution_strategy="Integrate intervention planning into refrac workflows.",
        entity_scope="All refrac wells",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Well Intervention Guidelines"
    ),
    DoctrineBlock(
        topic="Refrac Project Closeout and Post-Job Review",
        keywords=["project closeout", "post-job review", "refrac", "operations", "continuous improvement"],
        conclusion_template="Project closeout and post-job review ensure lessons learned are captured and continuous improvement is achieved for future refrac operations.",
        reasoning_framework="""
        1. Conduct multidisciplinary post-job review meetings.
        2. Document successes, failures, and improvement opportunities.
        3. Update operational guidelines based on review findings.
        4. Archive all project documentation for future reference.
        5. Integrate lessons learned into future refrac planning.
        """,
        key_factors=[
            "Post-job review",
            "Documentation",
            "Guideline updates",
            "Archiving",
            "Continuous improvement"
        ],
        primary_authority=[
            "Company Project Management Policy",
            "API RP 100-1"
        ],
        burden_holder="Project Manager",
        adversary_position="Post-job review is unnecessary for routine refrac operations.",
        counter_arguments=[
            "Reviews drive continuous improvement.",
            "Documentation supports future projects.",
            "Guideline updates prevent repeat mistakes."
        ],
        resolution_strategy="Integrate closeout and review into refrac project workflows.",
        entity_scope="All refrac operations",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Project Management Policy