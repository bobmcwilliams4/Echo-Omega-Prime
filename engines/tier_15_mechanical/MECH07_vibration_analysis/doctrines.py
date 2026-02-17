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
        topic="Unbalance Diagnosis",
        keywords=["unbalance", "mass eccentricity", "rotor", "vibration amplitude", "phase angle"],
        conclusion_template="If vibration amplitude at running speed is dominant and phase is consistent, unbalance is confirmed.",
        reasoning_framework="""
        1. Measure vibration amplitude and phase at bearings.
        2. Identify dominant frequency at 1x running speed.
        3. Check for phase consistency across measurement points.
        4. Confirm that amplitude increases with speed squared.
        5. Rule out other faults (e.g., misalignment, looseness) via secondary indicators.
        6. If all criteria met, attribute vibration to unbalance.
        """,
        key_factors=["Amplitude at 1x", "Phase consistency", "Speed-amplitude relationship", "Absence of harmonics"],
        primary_authority=["ISO 1940-1", "Vibration Analysis Handbook", "Bently Nevada Field Guide"],
        burden_holder="Analyst",
        adversary_position="Unbalance is not the root cause; other faults may be present.",
        counter_arguments=[
            "Misalignment can also show high 1x amplitude.",
            "Resonance may amplify unbalance symptoms.",
            "Mechanical looseness can mask true unbalance."
        ],
        resolution_strategy="Use phase analysis and confirm via trial weights or balancing runs.",
        entity_scope="Rotating machinery (MECH07)",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ISO 1940-1"
    ),
    DoctrineBlock(
        topic="Misalignment Diagnosis",
        keywords=["misalignment", "coupling", "parallel", "angular", "vibration harmonics"],
        conclusion_template="If significant 1x and 2x vibration components are present with axial movement, misalignment is indicated.",
        reasoning_framework="""
        1. Collect vibration data in all three axes.
        2. Identify presence of 1x and 2x running speed components.
        3. Evaluate axial vibration amplitude.
        4. Inspect coupling for wear or heat.
        5. Confirm via phase analysis and shaft alignment tools.
        6. Rule out unbalance and looseness by cross-checking symptoms.
        """,
        key_factors=["1x and 2x amplitude", "Axial vibration", "Coupling condition", "Phase difference"],
        primary_authority=["ISO 10816", "Practical Machinery Vibration Analysis and Predictive Maintenance"],
        burden_holder="Vibration Analyst",
        adversary_position="Observed symptoms are due to unbalance or looseness, not misalignment.",
        counter_arguments=[
            "Unbalance can also show high 1x amplitude.",
            "Mechanical looseness can create harmonics.",
            "Resonance can exaggerate vibration."
        ],
        resolution_strategy="Confirm with laser alignment tools and repeat measurements post-correction.",
        entity_scope="Coupled rotating equipment",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ISO 10816"
    ),
    DoctrineBlock(
        topic="Bearing Defect Frequencies",
        keywords=["bearing", "defect frequency", "BPFO", "BPFI", "BSF", "FTF"],
        conclusion_template="If vibration spectrum shows peaks at calculated bearing defect frequencies, a bearing fault is likely.",
        reasoning_framework="""
        1. Identify bearing type and geometry.
        2. Calculate BPFO, BPFI, BSF, and FTF using bearing dimensions and shaft speed.
        3. Analyze FFT spectrum for peaks at these frequencies.
        4. Cross-check with time waveform for impact signatures.
        5. Use envelope analysis for early detection.
        6. Eliminate other sources of similar frequencies (e.g., gear mesh).
        """,
        key_factors=["Calculated defect frequencies", "FFT spectrum peaks", "Envelope analysis results"],
        primary_authority=["SKF Bearing Analysis Guide", "ISO 15243"],
        burden_holder="Condition Monitoring Engineer",
        adversary_position="Peaks are due to gear mesh or electrical noise, not bearing defects.",
        counter_arguments=[
            "Gear mesh frequencies can overlap with bearing defect frequencies.",
            "Electrical noise can create false positives.",
            "Misalignment can increase bearing loads and mimic defects."
        ],
        resolution_strategy="Confirm with demodulation, trending, and physical inspection if possible.",
        entity_scope="Rolling element bearings",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ISO 15243"
    ),
    DoctrineBlock(
        topic="Vibration Severity Standards",
        keywords=["severity", "ISO 10816", "acceptance criteria", "alarm limits"],
        conclusion_template="If measured vibration exceeds ISO 10816 limits, corrective action is required.",
        reasoning_framework="""
        1. Identify machine group and operating condition as per ISO 10816.
        2. Measure RMS vibration velocity at bearing housings.
        3. Compare readings to severity zones (A, B, C, D).
        4. Set alarm and trip limits based on standard.
        5. Document and trend vibration levels for maintenance planning.
        """,
        key_factors=["ISO 10816 group", "RMS velocity", "Severity zone"],
        primary_authority=["ISO 10816", "API 670"],
        burden_holder="Maintenance Engineer",
        adversary_position="ISO limits are too conservative/aggressive for this application.",
        counter_arguments=[
            "Some machines tolerate higher vibration due to design.",
            "Special applications may require custom limits.",
            "Transient conditions may temporarily exceed limits."
        ],
        resolution_strategy="Adjust limits with OEM input and historical data if justified.",
        entity_scope="General industrial machinery",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ISO 10816"
    ),
    DoctrineBlock(
        topic="Resonance Identification",
        keywords=["resonance", "natural frequency", "critical speed", "amplitude spike"],
        conclusion_template="If vibration amplitude peaks sharply at a specific speed, resonance is present.",
        reasoning_framework="""
        1. Perform run-up and coast-down tests.
        2. Plot amplitude versus speed (Bode plot).
        3. Identify sharp amplitude peaks at specific speeds.
        4. Compare with calculated/FEA natural frequencies.
        5. Use impact testing to confirm mode shapes.
        6. Differentiate from unbalance by phase shift (90 degrees at resonance).
        """,
        key_factors=["Amplitude peak", "Speed correlation", "Phase shift", "Natural frequency"],
        primary_authority=["Bently Nevada Machinery Diagnostics", "API 684"],
        burden_holder="Vibration Specialist",
        adversary_position="Amplitude peak is due to unbalance or process upsets.",
        counter_arguments=[
            "Unbalance can cause high amplitude at running speed.",
            "Process changes can create transient peaks.",
            "Measurement errors can mimic resonance."
        ],
        resolution_strategy="Correlate with phase data and repeat tests under controlled conditions.",
        entity_scope="Rotating machinery",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 684"
    ),
    DoctrineBlock(
        topic="Gear Mesh Frequency Analysis",
        keywords=["gear mesh", "GMF", "sidebands", "tooth defect", "modulation"],
        conclusion_template="If vibration spectrum shows GMF and sidebands, gear defect is probable.",
        reasoning_framework="""
        1. Calculate gear mesh frequency (GMF = number of teeth x shaft speed).
        2. Analyze FFT for GMF and sidebands at shaft running speed.
        3. Look for harmonics and modulation patterns.
        4. Inspect gears for wear, pitting, or cracks.
        5. Confirm with time waveform and demodulation analysis.
        """,
        key_factors=["GMF amplitude", "Sideband presence", "Harmonics", "Physical inspection"],
        primary_authority=["AGMA 6000", "Practical Gear Design Handbook"],
        burden_holder="Reliability Engineer",
        adversary_position="Sidebands are due to load variation, not gear defects.",
        counter_arguments=[
            "Load variation can create sidebands.",
            "Misalignment can modulate GMF.",
            "Bearing defects can produce similar frequencies."
        ],
        resolution_strategy="Correlate vibration data with gear inspection and operational history.",
        entity_scope="Gearboxes and gear-driven equipment",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AGMA 6000"
    ),
    DoctrineBlock(
        topic="Mechanical Looseness Diagnosis",
        keywords=["looseness", "structural", "harmonics", "broadband vibration"],
        conclusion_template="If multiple harmonics and broadband vibration are present, mechanical looseness is likely.",
        reasoning_framework="""
        1. Analyze FFT for presence of 1x, 2x, 3x, and higher harmonics.
        2. Look for non-synchronous broadband vibration.
        3. Inspect machine for loose bolts, foundation cracks, or worn fits.
        4. Check for phase instability across measurement points.
        5. Confirm by tightening suspected components and retesting.
        """,
        key_factors=["Multiple harmonics", "Broadband noise", "Physical looseness", "Phase instability"],
        primary_authority=["Vibration Analysis Handbook", "ISO 10816"],
        burden_holder="Maintenance Technician",
        adversary_position="Harmonics are due to process or electrical issues.",
        counter_arguments=[
            "Process upsets can create broadband vibration.",
            "Electrical noise can mimic looseness.",
            "Resonance can amplify harmonics."
        ],
        resolution_strategy="Physical inspection and retest after corrective action.",
        entity_scope="All rotating machinery",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="ISO 10816"
    ),
    DoctrineBlock(
        topic="Rotor Dynamics Critical Speeds",
        keywords=["critical speed", "rotor dynamics", "Campbell diagram", "mode shape"],
        conclusion_template="If operational speed coincides with a calculated critical speed, design modification or operational changes are required.",
        reasoning_framework="""
        1. Model rotor using finite element analysis (FEA).
        2. Construct Campbell diagram to identify critical speeds.
        3. Compare operational speed range with critical speeds.
        4. Analyze mode shapes for potential resonance.
        5. Recommend design or operational changes to avoid critical speeds.
        """,
        key_factors=["Critical speed calculation", "Campbell diagram", "Mode shapes", "Operational speed"],
        primary_authority=["API 617", "Bently Nevada Rotor Dynamics Manual"],
        burden_holder="Design Engineer",
        adversary_position="Critical speed is not within operational range or is damped sufficiently.",
        counter_arguments=[
            "System damping may reduce resonance risk.",
            "Operational speed may not coincide with critical speed.",
            "Design modifications may be cost-prohibitive."
        ],
        resolution_strategy="Validate with field tests and adjust design or operation as needed.",
        entity_scope="High-speed rotating machinery",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API 617"
    ),
    DoctrineBlock(
        topic="Balancing Methodology",
        keywords=["balancing", "trial weight", "single-plane", "multi-plane", "correction"],
        conclusion_template="If unbalance is confirmed, perform balancing using appropriate methodology to reduce vibration below acceptance limits.",
        reasoning_framework="""
        1. Identify rotor type and balance quality grade.
        2. Select single-plane or multi-plane balancing as appropriate.
        3. Install trial weights and measure vibration response.
        4. Calculate correction weights and locations.
        5. Apply corrections and verify vibration reduction.
        6. Document balance results and residual unbalance.
        """,
        key_factors=["Balance quality grade", "Trial weight response", "Correction calculation", "Residual unbalance"],
        primary_authority=["ISO 1940-1", "API 684"],
        burden_holder="Field Balancing Technician",
        adversary_position="Balancing is not effective due to other faults or structural issues.",
        counter_arguments=[
            "Mechanical looseness can prevent effective balancing.",
            "Resonance can mask unbalance correction.",
            "Improper measurement can lead to incorrect corrections."
        ],
        resolution_strategy="Address underlying faults before balancing and use proper instrumentation.",
        entity_scope="Rotors and shafts",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ISO 1940-1"
    ),
    DoctrineBlock(
        topic="Proximity Probe Installation",
        keywords=["proximity probe", "shaft displacement", "installation", "alignment", "runout"],
        conclusion_template="If proximity probes are installed as per API 670, accurate shaft displacement measurement is ensured.",
        reasoning_framework="""
        1. Select probe type and range suitable for shaft diameter.
        2. Install probes at recommended locations (typically 90 degrees apart).
        3. Align probes to minimize runout and ensure perpendicularity.
        4. Calibrate probes using appropriate standards.
        5. Document installation and verify signal quality.
        """,
        key_factors=["Probe type", "Installation location", "Alignment", "Calibration"],
        primary_authority=["API 670", "Bently Nevada Proximity Probe Manual"],
        burden_holder="Instrumentation Technician",
        adversary_position="Improper installation leads to inaccurate measurements.",
        counter_arguments=[
            "Shaft runout can affect readings.",
            "Improper alignment can cause signal loss.",
            "Environmental factors can degrade probe performance."
        ],
        resolution_strategy="Follow manufacturer and API 670 guidelines; verify with calibration tools.",
        entity_scope="Critical rotating equipment",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API 670"
    ),
    DoctrineBlock(
        topic="Accelerometer Selection and Mounting",
        keywords=["accelerometer", "mounting", "frequency response", "sensitivity", "installation"],
        conclusion_template="If accelerometers are correctly selected and mounted, vibration measurements are reliable.",
        reasoning_framework="""
        1. Determine frequency range and amplitude of interest.
        2. Select accelerometer with appropriate sensitivity and range.
        3. Mount accelerometer rigidly using stud or adhesive.
        4. Avoid mounting on thin or flexible surfaces.
        5. Route cables to minimize electrical noise.
        6. Calibrate and document installation.
        """,
        key_factors=["Frequency range", "Mounting method", "Surface condition", "Cable routing"],
        primary_authority=["ISO 10816", "Wilcoxon Accelerometer Application Guide"],
        burden_holder="Instrumentation Engineer",
        adversary_position="Improper selection or mounting leads to unreliable data.",
        counter_arguments=[
            "Magnet mounting can reduce high-frequency response.",
            "Loose mounting can introduce noise.",
            "Incorrect cable routing can pick up EMI."
        ],
        resolution_strategy="Follow best practices for mounting and selection; verify with calibration.",
        entity_scope="All vibration-monitored equipment",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ISO 10816"
    ),
    DoctrineBlock(
        topic="Oil Whirl and Whip Instability",
        keywords=["oil whirl", "oil whip", "fluid film instability", "sub-synchronous vibration"],
        conclusion_template="If sub-synchronous vibration at 0.42-0.48x running speed is present, oil whirl/whip is likely.",
        reasoning_framework="""
        1. Monitor vibration spectrum for sub-synchronous peaks (0.42-0.48x).
        2. Confirm with time waveform and orbit analysis.
        3. Check for journal bearing design and operating conditions.
        4. Inspect for low oil pressure or high clearance.
        5. Differentiate from other faults by absence of harmonics.
        """,
        key_factors=["Sub-synchronous frequency", "Journal bearing type", "Operating conditions", "Orbit shape"],
        primary_authority=["API 684", "Bently Nevada Machinery Diagnostics"],
        burden_holder="Machinery Diagnostics Engineer",
        adversary_position="Sub-synchronous vibration is due to process or electrical issues.",
        counter_arguments=[
            "Process upsets can cause similar vibration.",
            "Electrical noise can create sub-synchronous peaks.",
            "Resonance may amplify sub-synchronous frequencies."
        ],
        resolution_strategy="Correlate with bearing design and operating data; confirm with orbit analysis.",
        entity_scope="Journal bearing machines",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 684"
    ),
    DoctrineBlock(
        topic="FFT Spectrum Analysis",
        keywords=["FFT", "spectrum", "frequency analysis", "harmonics", "sidebands"],
        conclusion_template="If FFT analysis reveals characteristic fault frequencies, targeted diagnosis is possible.",
        reasoning_framework="""
        1. Collect time-domain vibration data.
        2. Perform FFT to convert to frequency domain.
        3. Identify peaks at running speed, harmonics, and fault frequencies.
        4. Use sidebands and modulation to differentiate faults.
        5. Trend frequency components for condition monitoring.
        """,
        key_factors=["Peak identification", "Harmonics", "Sidebands", "Frequency trending"],
        primary_authority=["ISO 13373-2", "Vibration Analysis Handbook"],
        burden_holder="Vibration Analyst",
        adversary_position="FFT analysis is insufficient without time waveform and phase data.",
        counter_arguments=[
            "Some faults are better detected in time domain.",
            "Phase analysis is required for confirmation.",
            "FFT can miss transient events."
        ],
        resolution_strategy="Use FFT in conjunction with other analysis methods.",
        entity_scope="All vibration-monitored equipment",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ISO 13373-2"
    ),
    DoctrineBlock(
        topic="Time Waveform Analysis",
        keywords=["time waveform", "transient", "impact", "modulation", "fault detection"],
        conclusion_template="If time waveform shows impacts or modulation, mechanical fault is indicated.",
        reasoning_framework="""
        1. Record time waveform data at appropriate sampling rate.
        2. Analyze for impacts, modulation, or periodicity.
        3. Compare with baseline waveforms.
        4. Use waveform shape to differentiate between faults (e.g., impacts for bearing, modulation for gear).
        5. Correlate with FFT and envelope analysis.
        """,
        key_factors=["Impact events", "Modulation", "Waveform shape", "Baseline comparison"],
        primary_authority=["ISO 13373-2", "Vibration Analysis Handbook"],
        burden_holder="Condition Monitoring Analyst",
        adversary_position="Waveform anomalies are due to process or electrical noise.",
        counter_arguments=[
            "Process upsets can create transient events.",
            "Electrical interference can distort waveform.",
            "Baseline may not represent all operating conditions."
        ],
        resolution_strategy="Repeat measurements and correlate with process data.",
        entity_scope="All monitored machinery",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ISO 13373-2"
    ),
    DoctrineBlock(
        topic="Orbit Analysis and Shaft Centerline Monitoring",
        keywords=["orbit analysis", "shaft centerline", "journal bearing", "instability", "preload"],
        conclusion_template="If orbit shape and centerline position deviate from baseline, bearing or shaft fault is likely.",
        reasoning_framework="""
        1. Use proximity probes to record X-Y shaft displacement.
        2. Plot orbit and centerline position.
        3. Compare with baseline for shape and position changes.
        4. Identify instability (e.g., oil whirl) or preload conditions.
        5. Correlate with vibration and process data.
        """,
        key_factors=["Orbit shape", "Centerline position", "Baseline comparison", "Instability indicators"],
        primary_authority=["API 684", "Bently Nevada Orbit Analysis Guide"],
        burden_holder="Machinery Diagnostics Engineer",
        adversary_position="Orbit changes are due to process or load variation.",
        counter_arguments=[
            "Process changes can affect centerline position.",
            "Load variation can distort orbit.",
            "Measurement error can affect orbit shape."
        ],
        resolution_strategy="Repeat tests and correlate with process and vibration data.",
        entity_scope="Journal bearing machines",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API 684"
    ),
    DoctrineBlock(
        topic="Electrical Motor Vibration",
        keywords=["electrical motor", "vibration", "electromagnetic forces", "bar defect", "eccentricity"],
        conclusion_template="If vibration at line frequency or its harmonics is present, electrical fault is probable.",
        reasoning_framework="""
        1. Measure vibration spectrum for line frequency (50/60 Hz) and harmonics.
        2. Identify sidebands at slip frequency.
        3. Inspect for rotor bar defects or eccentricity.
        4. Correlate with motor current signature analysis (MCSA).
        5. Rule out mechanical faults via phase and time waveform analysis.
        """,
        key_factors=["Line frequency vibration", "Slip frequency sidebands", "MCSA results", "Physical inspection"],
        primary_authority=["IEEE 112", "Practical Machinery Vibration Analysis and Predictive Maintenance"],
        burden_holder="Motor Diagnostics Engineer",
        adversary_position="Vibration is due to mechanical faults, not electrical.",
        counter_arguments=[
            "Unbalance or misalignment can cause similar symptoms.",
            "Mechanical looseness can create harmonics.",
            "Process upsets can affect vibration."
        ],
        resolution_strategy="Correlate electrical and mechanical data; confirm with MCSA.",
        entity_scope="AC induction motors",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="IEEE 112"
    ),
    # --- 25+ additional DoctrineBlocks for comprehensive coverage ---
    DoctrineBlock(
        topic="Soft Foot Detection",
        keywords=["soft foot", "baseplate", "machine frame", "distortion", "foot lift"],
        conclusion_template="If foot lift or distortion is detected during tightening, soft foot is present.",
        reasoning_framework="""
        1. Loosen and retighten machine feet sequentially.
        2. Measure lift or distortion at each foot.
        3. Identify significant movement (>0.05 mm).
        4. Inspect baseplate and shims for corrosion or debris.
        5. Correct with proper shimming and retest.
        """,
        key_factors=["Foot lift", "Distortion", "Shim condition", "Baseplate flatness"],
        primary_authority=["ISO 1925", "Practical Machinery Alignment"],
        burden_holder="Maintenance Technician",
        adversary_position="Movement is due to foundation settling or thermal growth.",
        counter_arguments=[
            "Thermal expansion can cause apparent soft foot.",
            "Foundation movement may mimic soft foot.",
            "Measurement error can affect results."
        ],
        resolution_strategy="Repeat tests at ambient and operating temperature; verify with dial indicators.",
        entity_scope="All base-mounted machinery",
        confidence=0.90,
        confidence_zone="Moderate",
        controlling_precedent="ISO 1925"
    ),
    DoctrineBlock(
        topic="Thermal Growth Compensation",
        keywords=["thermal growth", "alignment", "hot alignment", "expansion"],
        conclusion_template="If thermal growth is significant, hot alignment should be performed.",
        reasoning_framework="""
        1. Measure machine temperature at cold and hot conditions.
        2. Calculate thermal expansion of shafts and frames.
        3. Adjust alignment targets for expected growth.
        4. Perform hot alignment check after reaching operating temperature.
        5. Document alignment results and adjust as necessary.
        """,
        key_factors=["Temperature change", "Expansion calculation", "Hot alignment", "Alignment targets"],
        primary_authority=["API 686", "Practical Machinery Alignment"],
        burden_holder="Alignment Technician",
        adversary_position="Thermal growth is negligible for this machine.",
        counter_arguments=[
            "Some machines have minimal thermal growth.",
            "OEM may specify cold alignment targets.",
            "Measurement error can affect results."
        ],
        resolution_strategy="Consult OEM and validate with field measurements.",
        entity_scope="Large rotating equipment",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="API 686"
    ),
    DoctrineBlock(
        topic="Baseplate Grouting Standards",
        keywords=["grouting", "baseplate", "foundation", "voids", "resonance"],
        conclusion_template="If baseplate grouting is incomplete, vibration and resonance risk increases.",
        reasoning_framework="""
        1. Inspect baseplate for voids and incomplete grouting.
        2. Tap test for hollow sounds indicating voids.
        3. Review grouting material and installation method.
        4. Correlate with vibration data for resonance or looseness.
        5. Repair grouting and retest vibration.
        """,
        key_factors=["Grouting completeness", "Void detection", "Material quality", "Vibration correlation"],
        primary_authority=["API 686", "ISO 1925"],
        burden_holder="Construction Supervisor",
        adversary_position="Baseplate is sufficiently supported despite minor voids.",
        counter_arguments=[
            "Small voids may not affect performance.",
            "Repair may be disruptive or costly.",
            "Other factors may contribute to vibration."
        ],
        resolution_strategy="Prioritize repair for critical equipment; monitor vibration trends.",
        entity_scope="All base-mounted machinery",
        confidence=0.87,
        confidence_zone="Moderate",
        controlling_precedent="API 686"
    ),
    DoctrineBlock(
        topic="Shaft Crack Detection",
        keywords=["shaft crack", "subharmonic", "vibration", "stiffness change", "phase modulation"],
        conclusion_template="If subharmonic vibration and phase modulation are present, shaft crack is suspected.",
        reasoning_framework="""
        1. Monitor for subharmonic peaks (0.5x, 1.5x) in FFT.
        2. Analyze phase data for modulation or instability.
        3. Inspect shaft for visible cracks or discoloration.
        4. Use advanced NDT (ultrasound, eddy current) for confirmation.
        5. Trend vibration and phase data for progression.
        """,
        key_factors=["Subharmonic peaks", "Phase modulation", "NDT results", "Physical inspection"],
        primary_authority=["API 684", "Vibration Analysis Handbook"],
        burden_holder="Reliability Engineer",
        adversary_position="Subharmonics are due to process or electrical issues.",
        counter_arguments=[
            "Process upsets can create subharmonics.",
            "Electrical noise can affect phase data.",
            "Measurement error can mimic crack symptoms."
        ],
        resolution_strategy="Confirm with NDT and repeat measurements.",
        entity_scope="Critical rotors and shafts",
        confidence=0.85,
        confidence_zone="Moderate",
        controlling_precedent="API 684"
    ),
    DoctrineBlock(
        topic="Shaft Coupling Inspection",
        keywords=["coupling", "inspection", "wear", "backlash", "misalignment"],
        conclusion_template="If coupling shows wear or excessive backlash, replacement or realignment is required.",
        reasoning_framework="""
        1. Inspect coupling for wear, cracks, or corrosion.
        2. Measure backlash and compare to OEM limits.
        3. Check for evidence of misalignment (heat, debris).
        4. Replace worn components and realign shafts.
        5. Retest vibration and document results.
        """,
        key_factors=["Wear", "Backlash", "Misalignment evidence", "OEM limits"],
        primary_authority=["AGMA 9000", "Practical Machinery Alignment"],
        burden_holder="Maintenance Technician",
        adversary_position="Wear is within acceptable limits; replacement is unnecessary.",
        counter_arguments=[
            "OEM limits may allow some wear.",
            "Replacement may be deferred if vibration is acceptable.",
            "Other faults may cause similar symptoms."
        ],
        resolution_strategy="Follow OEM recommendations and monitor vibration.",
        entity_scope="All coupled machinery",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="AGMA 9000"
    ),
    DoctrineBlock(
        topic="Resonance Avoidance in Design",
        keywords=["resonance", "design", "natural frequency", "critical speed", "stiffness"],
        conclusion_template="If resonance is within operational range, design modifications are necessary.",
        reasoning_framework="""
        1. Calculate natural frequencies and critical speeds during design.
        2. Ensure operational speed range avoids resonance.
        3. Modify design (stiffness, mass, damping) if necessary.
        4. Validate with FEA and prototype testing.
        5. Document design changes and test results.
        """,
        key_factors=["Natural frequency", "Operational speed", "Design modifications", "Test results"],
        primary_authority=["API 617", "ISO 14839"],
        burden_holder="Design Engineer",
        adversary_position="Resonance can be managed operationally without design changes.",
        counter_arguments=[
            "Operational controls may avoid resonance.",
            "Design changes may be costly.",
            "Damping may be sufficient."
        ],
        resolution_strategy="Validate with testing and consult with OEM.",
        entity_scope="New machinery design",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 617"
    ),
    DoctrineBlock(
        topic="High-Frequency Vibration Analysis",
        keywords=["high-frequency", "envelope analysis", "bearing fault", "impact", "demodulation"],
        conclusion_template="If envelope analysis shows high-frequency impacts, early bearing fault is indicated.",
        reasoning_framework="""
        1. Collect high-frequency vibration data (>5 kHz).
        2. Perform envelope analysis to extract impact events.
        3. Identify peaks at bearing defect frequencies.
        4. Trend impact energy for early fault detection.
        5. Confirm with physical inspection if possible.
        """,
        key_factors=["Envelope analysis", "Impact frequency", "Trend data", "Physical inspection"],
        primary_authority=["ISO 15243", "SKF Bearing Analysis Guide"],
        burden_holder="Condition Monitoring Analyst",
        adversary_position="Impacts are due to process or electrical noise.",
        counter_arguments=[
            "Electrical noise can create false impacts.",
            "Process upsets may cause high-frequency events.",
            "Mounting issues can affect high-frequency response."
        ],
        resolution_strategy="Repeat analysis and confirm with inspection.",
        entity_scope="Rolling element bearings",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ISO 15243"
    ),
    DoctrineBlock(
        topic="Vibration Trending and Alarm Management",
        keywords=["trending", "alarm", "trip", "condition monitoring", "threshold"],
        conclusion_template="If vibration trends exceed alarm or trip thresholds, maintenance action is required.",
        reasoning_framework="""
        1. Set alarm and trip thresholds based on standards and historical data.
        2. Continuously trend vibration data.
        3. Investigate causes of alarm or trip events.
        4. Schedule maintenance or shutdown as needed.
        5. Document actions and review thresholds periodically.
        """,
        key_factors=["Alarm threshold", "Trend data", "Trip events", "Maintenance action"],
        primary_authority=["ISO 10816", "API 670"],
        burden_holder="Condition Monitoring Engineer",
        adversary_position="Alarm limits are too conservative or not justified.",
        counter_arguments=[
            "Historical data may justify higher limits.",
            "Transient events may not require action.",
            "False alarms can occur."
        ],
        resolution_strategy="Review and adjust thresholds with OEM and historical data.",
        entity_scope="All monitored equipment",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ISO 10816"
    ),
    DoctrineBlock(
        topic="Modal Analysis for Structural Resonance",
        keywords=["modal analysis", "structural resonance", "mode shape", "impact testing"],
        conclusion_template="If modal analysis identifies resonance near operating speed, structural modification is recommended.",
        reasoning_framework="""
        1. Perform impact testing to identify mode shapes and frequencies.
        2. Compare modal frequencies with operational speed.
        3. Identify resonance risk and recommend modifications (stiffening, mass change, damping).
        4. Validate changes with retesting.
        5. Document findings and corrective actions.
        """,
        key_factors=["Modal frequency", "Mode shape", "Operational speed", "Modification results"],
        primary_authority=["ISO 7626", "API 684"],
        burden_holder="Structural Engineer",
        adversary_position="Resonance is not significant or can be managed operationally.",
        counter_arguments=[
            "Operational controls may avoid resonance.",
            "Modification may be costly.",
            "Resonance may not affect reliability."
        ],
        resolution_strategy="Validate with testing and consult with OEM.",
        entity_scope="Machine structures and foundations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ISO 7626"
    ),
    DoctrineBlock(
        topic="Phase Analysis for Fault Differentiation",
        keywords=["phase analysis", "fault differentiation", "unbalance", "misalignment", "looseness"],
        conclusion_template="If phase analysis is consistent with fault signature, diagnosis is confirmed.",
        reasoning_framework="""
        1. Measure phase across multiple points and axes.
        2. Compare phase relationships to fault signatures (e.g., 0° for unbalance, 180° for misalignment).
        3. Use phase change with speed to identify resonance.
        4. Correlate with amplitude and frequency data.
        5. Confirm diagnosis with corrective action and retest.
        """,
        key_factors=["Phase relationship", "Fault signature", "Amplitude correlation", "Retest results"],
        primary_authority=["ISO 13373-2", "Vibration Analysis Handbook"],
        burden_holder="Vibration Analyst",
        adversary_position="Phase data is inconclusive or affected by other factors.",
        counter_arguments=[
            "Multiple faults can affect phase.",
            "Measurement error can distort results.",
            "Phase lag may be affected by system dynamics."
        ],
        resolution_strategy="Repeat measurements and correlate with other data.",
        entity_scope="All rotating machinery",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ISO 13373-2"
    ),
    DoctrineBlock(
        topic="Precision Shaft Alignment",
        keywords=["shaft alignment", "laser alignment", "dial indicator", "coupling"],
        conclusion_template="If shaft alignment is within tolerance, coupling and bearing life are maximized.",
        reasoning_framework="""
        1. Use laser or dial indicator tools for precise measurement.
        2. Adjust machine position to achieve parallel and angular alignment within tolerance.
        3. Tighten bolts and recheck alignment.
        4. Document results and monitor vibration post-alignment.
        5. Repeat alignment after major maintenance or movement.
        """,
        key_factors=["Alignment tolerance", "Measurement method", "Vibration reduction", "Documentation"],
        primary_authority=["API 686", "Practical Machinery Alignment"],
        burden_holder="Maintenance Technician",
        adversary_position="Alignment is not critical for flexible couplings.",
        counter_arguments=[
            "Flexible couplings can tolerate some misalignment.",
            "Thermal growth may affect alignment.",
            "Measurement error can affect results."
        ],
        resolution_strategy="Follow best practices and monitor vibration.",
        entity_scope="All coupled machinery",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API 686"
    ),
    DoctrineBlock(
        topic="Machine Train Alignment",
        keywords=["machine train", "multi-coupling", "alignment", "thermal growth"],
        conclusion_template="If all machines in train are aligned within tolerance, vibration is minimized.",
        reasoning_framework="""
        1. Plan alignment sequence for multi-coupling trains.
        2. Compensate for thermal growth and baseplate movement.
        3. Use laser alignment tools for accuracy.
        4. Tighten and retest each coupling.
        5. Document alignment and monitor vibration.
        """,
        key_factors=["Alignment sequence", "Thermal growth compensation", "Measurement accuracy", "Vibration monitoring"],
        primary_authority=["API 686", "Practical Machinery Alignment"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Minor misalignment is acceptable in long trains.",
        counter_arguments=[
            "Thermal movement may affect alignment.",
            "Measurement error can accumulate.",
            "OEM may specify relaxed tolerances."
        ],
        resolution_strategy="Follow best practices and consult OEM.",
        entity_scope="Multi-coupling machine trains",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 686"
    ),
    DoctrineBlock(
        topic="Rolling Element Bearing Lubrication",
        keywords=["bearing lubrication", "grease", "oil", "relubrication interval", "contamination"],
        conclusion_template="If lubrication is adequate and clean, bearing life is maximized.",
        reasoning_framework="""
        1. Select lubricant type and grade per OEM.
        2. Set relubrication intervals based on operating conditions.
        3. Monitor for contamination (water, particles).
        4. Inspect used lubricant for wear debris.
        5. Adjust intervals and type as needed.
        """,
        key_factors=["Lubricant type", "Interval", "Contamination", "Wear debris"],
        primary_authority=["ISO 15243", "SKF Lubrication Handbook"],
        burden_holder="Maintenance Technician",
        adversary_position="Lubrication is excessive or insufficient for actual conditions.",
        counter_arguments=[
            "Over-lubrication can cause overheating.",
            "Under-lubrication leads to early failure.",
            "Contamination may occur between intervals."
        ],
        resolution_strategy="Monitor lubricant condition and adjust practices.",
        entity_scope="All rolling element bearings",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ISO 15243"
    ),
    DoctrineBlock(
        topic="Journal Bearing Clearance Measurement",
        keywords=["journal bearing", "clearance", "measurement", "oil film", "instability"],
        conclusion_template="If bearing clearance is within specification, oil film stability is ensured.",
        reasoning_framework="""
        1. Measure bearing clearance with feeler gauge or plastigage.
        2. Compare to OEM or API 670 limits.
        3. Inspect for wear or scoring.
        4. Monitor for signs of instability (oil whirl, whip).
        5. Replace or repair if out of tolerance.
        """,
        key_factors=["Clearance measurement", "OEM limits", "Wear", "Instability indicators"],
        primary_authority=["API 670", "ISO 4386"],
        burden_holder="Maintenance Technician",
        adversary_position="Clearance is excessive but machine is stable.",
        counter_arguments=[
            "Some wear is acceptable.",
            "Replacement may be deferred if stable.",
            "Measurement error can occur."
        ],
        resolution_strategy="Monitor vibration and oil analysis; replace if instability occurs.",
        entity_scope="Journal bearing machines",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 670"
    ),
    DoctrineBlock(
        topic="Vibration Data Acquisition Best Practices",
        keywords=["data acquisition", "sampling rate", "transducer placement", "signal quality"],
        conclusion_template="If data is acquired per best practices, analysis accuracy is maximized.",
        reasoning_framework="""
        1. Select appropriate sampling rate (at least 2.5x highest frequency of interest).
        2. Place transducers at recommended locations.
        3. Minimize cable length and avoid EMI sources.
        4. Calibrate equipment before use.
        5. Document acquisition settings and conditions.
        """,
        key_factors=["Sampling rate", "Transducer placement", "Calibration", "Signal quality"],
        primary_authority=["ISO 13373-2", "Vibration Analysis Handbook"],
        burden_holder="Data Acquisition Technician",
        adversary_position="Field conditions may prevent ideal data acquisition.",
        counter_arguments=[
            "Space constraints may affect placement.",
            "Environmental noise can affect data.",
            "Calibration drift may occur."
        ],
        resolution_strategy="Document deviations and compensate in analysis.",
        entity_scope="All vibration-monitored equipment",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ISO 13373-2"
    ),
    DoctrineBlock(
        topic="Vibration Analysis Training and Certification",
        keywords=["training", "certification", "analyst", "ISO 18436", "competency"],
        conclusion_template="If analysts are ISO 18436 certified, analysis reliability is maximized.",
        reasoning_framework="""
        1. Require ISO 18436 certification for all vibration analysts.
        2. Provide ongoing training and competency assessments.
        3. Maintain certification records.
        4. Encourage participation in industry forums and workshops.
        5. Review analysis quality and provide feedback.
        """,
        key_factors=["Certification", "Training", "Competency", "Quality review"],
        primary_authority=["ISO 18436", "Mobius Institute"],
        burden_holder="Maintenance Manager",
        adversary_position="On-the-job training is sufficient for most analysis.",
        counter_arguments=[
            "Certification may not reflect practical skill.",
            "Training costs may be high.",
            "On-the-job experience is valuable."
        ],
        resolution_strategy="Combine certification with practical experience and mentoring.",
        entity_scope="All vibration analysts",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ISO 18436"
    ),
    DoctrineBlock(
        topic="Wireless Vibration Monitoring",
        keywords=["wireless", "vibration monitoring", "data transmission", "battery life", "signal integrity"],
        conclusion_template="If wireless sensors are properly installed and maintained, monitoring reliability is comparable to wired systems.",
        reasoning_framework="""
        1. Select wireless sensors with adequate range and battery life.
        2. Install in locations with minimal interference.
        3. Monitor signal integrity and data loss.
        4. Replace batteries or recharge as per schedule.
        5. Validate data against wired reference sensors.
        """,
        key_factors=["Sensor range", "Battery life", "Signal integrity", "Data validation"],
        primary_authority=["ISO 13373-2", "Vibration Analysis Handbook"],
        burden_holder="Condition Monitoring Engineer",
        adversary_position="Wireless systems are less reliable than wired.",
        counter_arguments=[
            "Signal loss may occur in harsh environments.",
            "Battery failure can cause data gaps.",
            "Wireless protocols may be less secure."
        ],
        resolution_strategy="Use hybrid systems and monitor for data integrity.",
        entity_scope="All monitored equipment",
        confidence=0.90,
        confidence_zone="Moderate",
        controlling_precedent="ISO 13373-2"
    ),
    DoctrineBlock(
        topic="Root Cause Failure Analysis (RCFA)",
        keywords=["RCFA", "failure analysis", "vibration", "fault tree", "corrective action"],
        conclusion_template="If RCFA is performed after failure, recurrence risk is minimized.",
        reasoning_framework="""
        1. Collect all relevant data (vibration, process, maintenance).
        2. Construct fault tree or cause map.
        3. Identify root cause and contributing factors.
        4. Implement corrective and preventive actions.
        5. Document findings and monitor for recurrence.
        """,
        key_factors=["Data collection", "Fault tree", "Corrective action", "Documentation"],
        primary_authority=["ISO 14224", "Practical Machinery RCFA"],
        burden_holder="Reliability Engineer",
        adversary_position="RCFA is time-consuming and may not prevent recurrence.",
        counter_arguments=[
            "Some failures are random or unavoidable.",
            "RCFA may not identify all causes.",
            "Implementation of actions may be delayed."
        ],
        resolution_strategy="Prioritize RCFA for critical failures and track action completion.",
        entity_scope="All critical machinery",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ISO 14224"
    ),
    DoctrineBlock(
        topic="Process-Induced Vibration",
        keywords=["process vibration", "fluid flow", "cavitation", "pulsation", "pressure fluctuation"],
        conclusion_template="If vibration correlates with process changes, process-induced vibration is likely.",
        reasoning_framework="""
        1. Trend vibration data with process parameters (flow, pressure).
        2. Identify correlation between vibration and process changes.
        3. Inspect for cavitation, pulsation, or pressure surges.
        4. Consult process and instrumentation diagrams.
        5. Implement process modifications as needed.
        """,
        key_factors=["Process correlation", "Cavitation", "Pulsation", "Process diagrams"],
        primary_authority=["API 674", "Vibration Analysis Handbook"],
        burden_holder="Process Engineer",
        adversary_position="Vibration is due to mechanical faults, not process.",
        counter_arguments=[
            "Mechanical faults can be masked by process vibration.",
            "Process changes may be transient.",
            "Instrumentation error can affect correlation."
        ],
        resolution_strategy="Correlate with process data and confirm with mechanical inspection.",
        entity_scope="Pumps, compressors, process equipment",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 674"
    ),
    DoctrineBlock(
        topic="Vibration Acceptance Testing",
        keywords=["acceptance testing", "commissioning", "baseline", "OEM limits", "ISO 10816"],
        conclusion_template="If vibration is within acceptance limits at commissioning, machine is fit for service.",
        reasoning_framework="""
        1. Perform vibration measurements at commissioning.
        2. Compare results to OEM and ISO 10816 limits.
        3. Establish baseline for future trending.
        4. Document test results and acceptance status.
        5. Address any deviations before startup.
        """,
        key_factors=["Acceptance limits", "Baseline data", "Documentation", "Deviation correction"],
        primary_authority=["ISO 10816", "API 670"],
        burden_holder="Commissioning Engineer",
        adversary_position="Acceptance limits are too strict or not representative.",
        counter_arguments=[
            "OEM limits may be conservative.",
            "Transient conditions may affect results.",
            "Baseline may change after initial operation."
        ],
        resolution_strategy="Review limits with OEM and retest after adjustments.",
        entity_scope="All new or overhauled machinery",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ISO 10816"
    ),
    DoctrineBlock(
        topic="Vibration Monitoring Program Effectiveness",
        keywords=["monitoring program", "effectiveness", "KPI", "failure reduction", "cost savings"],
        conclusion_template="If KPIs show reduced failures and costs, monitoring program is effective.",
        reasoning_framework="""
        1. Define KPIs (failure rate, downtime, cost savings).
        2. Track and trend KPIs over time.
        3. Correlate improvements with monitoring activities.
        4. Adjust program scope and methods as needed.
        5. Report results to management.
        """,
        key_factors=["KPI definition", "Trend analysis", "Program adjustment", "Reporting"],
        primary_authority=["ISO 55000", "Practical Condition Monitoring"],
        burden_holder="Reliability Manager",
        adversary_position="Improvements are due to other factors, not monitoring.",
        counter_arguments=[
            "Process changes may reduce failures.",
            "Other maintenance activities may affect results.",
            "Data may be insufficient for trend analysis."
        ],
        resolution_strategy="Use statistical analysis and control for confounding factors.",
        entity_scope="All monitored facilities",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ISO 55000"
    ),
    DoctrineBlock(
        topic="Data Integration with CMMS",
        keywords=["CMMS", "data integration", "work order", "vibration alert", "maintenance planning"],
        conclusion_template="If vibration data is integrated with CMMS, maintenance planning is optimized.",
        reasoning_framework="""
        1. Configure vibration monitoring system to trigger CMMS work orders.
        2. Link vibration alerts to maintenance history.
        3. Use data for predictive maintenance scheduling.
        4. Review and close work orders based on vibration trends.
        5. Analyze effectiveness of maintenance actions.
        """,
        key_factors=["System integration", "Work order linkage", "Predictive scheduling", "Effectiveness analysis"],
        primary_authority=["ISO 55000", "Practical Condition Monitoring"],
        burden_holder="Maintenance Planner",
        adversary_position="Integration is costly and may not yield benefits.",
        counter_arguments=[
            "Manual planning may be sufficient.",
            "Integration may require IT resources.",
            "Data may not be actionable."
        ],
        resolution_strategy="Pilot integration and assess ROI.",
        entity_scope="Facilities with CMMS",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ISO 55000"
    ),
    DoctrineBlock(
        topic="Remote Vibration Diagnostics",
        keywords=["remote diagnostics", "cloud", "IIoT", "data security", "real-time monitoring"],
        conclusion_template="If remote diagnostics are implemented securely, real-time fault detection is enhanced.",
        reasoning_framework="""
        1. Transmit vibration data to secure cloud platform.
        2. Analyze data remotely with advanced algorithms.
        3. Alert local personnel to faults in real time.
        4. Ensure data security and privacy compliance.
        5. Validate remote findings with on-site checks.
        """,
        key_factors=["Data transmission", "Security", "Algorithm accuracy", "On-site validation"],
        primary_authority=["ISO 27001", "Practical Condition Monitoring"],
        burden_holder="IT and Reliability Engineer",
        adversary_position="Remote systems are vulnerable to cyber threats.",
        counter_arguments=[
            "Cybersecurity risk may outweigh benefits.",
            "Data loss or delay may occur.",
            "On-site validation is still required."
        ],
        resolution_strategy="Implement robust cybersecurity and hybrid diagnostic approach.",
        entity_scope="Facilities with IIoT infrastructure",
        confidence=0.90,
        confidence_zone="Moderate",
        controlling_precedent="ISO 27001"
    ),
    DoctrineBlock(
        topic="Vibration Analysis for Regulatory Compliance",
        keywords=["regulatory compliance", "environmental", "OSHA", "noise", "vibration exposure"],
        conclusion_template="If vibration levels meet regulatory limits, compliance is achieved.",
        reasoning_framework="""
        1. Identify applicable regulations (OSHA, local, ISO).
        2. Measure and document vibration and noise exposure.
        3. Compare results to regulatory limits.
        4. Implement mitigation if limits are exceeded.
        5. Maintain records for audits.
        """,
        key_factors=["Regulatory limits", "Measurement", "Documentation", "Mitigation"],
        primary_authority=["OSHA", "ISO 2631"],
        burden_holder="EHS Manager",
        adversary_position="Regulations are not applicable to this facility.",
        counter_arguments=[
            "Some facilities may be exempt.",
            "Measurement error can affect compliance.",
            "Mitigation may be costly."
        ],
        resolution_strategy="Consult legal and regulatory experts; document compliance.",
        entity_scope="All regulated facilities",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OSHA"
    ),
    DoctrineBlock(
        topic="Vibration Analysis for Asset Life Extension",
        keywords=["asset life", "life extension", "condition monitoring", "failure prevention"],
        conclusion_template="If vibration analysis is used proactively, asset life is extended.",
        reasoning_framework="""
        1. Implement regular vibration monitoring.
        2. Detect and correct faults early.
        3. Schedule maintenance based on condition, not time.
        4. Track asset life and failure rates.
        5. Report life extension and cost savings.
        """,
        key_factors=["Monitoring frequency", "Early detection", "Condition-based maintenance", "Life tracking"],
        primary_authority=["ISO 55000", "Practical Condition Monitoring"],
        burden_holder="Asset Manager",
        adversary_position="Life extension is due to other factors.",
        counter_arguments=[
            "Process improvements may affect life.",
            "Other maintenance activities contribute.",
            "Data may be insufficient."
        ],
        resolution_strategy="Use statistical analysis and compare with historical data.",
        entity_scope="All monitored assets",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ISO 55000"
    ),
    DoctrineBlock(
        topic="Vibration Analysis for Energy Efficiency",
        keywords=["energy efficiency", "vibration", "misalignment", "unbalance", "power consumption"],
        conclusion_template="If vibration faults are corrected, energy efficiency improves.",
        reasoning_framework="""
        1. Measure power consumption before and after fault correction.
        2. Correlate vibration reduction with energy savings.
        3. Quantify cost savings for management.
        4. Repeat analysis periodically.
        5. Document results and adjust maintenance strategy.
        """,
        key_factors=["Power measurement", "Vibration reduction", "Cost savings", "Documentation"],
        primary_authority=["ISO 50001", "Practical Condition Monitoring"],
        burden_holder="Energy Manager",
        adversary_position="Energy savings are negligible.",
        counter_arguments=[
            "Savings may be small for some faults.",
            "Other factors may affect energy use.",
            "Measurement error can occur."
        ],
        resolution_strategy="Aggregate savings across assets and report trends.",
        entity_scope="All monitored equipment",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ISO 50001"
    ),
    DoctrineBlock(
        topic="Vibration Analysis for Predictive Maintenance",
        keywords=["predictive maintenance", "PdM", "condition monitoring", "failure prevention"],
        conclusion_template="If predictive maintenance is based on vibration analysis, unplanned failures are reduced.",
        reasoning_framework="""
        1. Monitor vibration continuously or at regular intervals.
        2. Set thresholds for alarm and maintenance action.
        3. Schedule maintenance based on condition, not calendar.
        4. Track failure rates and downtime.
        5. Adjust program based on results.
        """,
        key_factors=["Monitoring interval", "Thresholds", "Failure rate", "Program adjustment"],
        primary_authority=["ISO 17359", "Practical Condition Monitoring"],
        burden_holder="Maintenance Manager",
        adversary_position="Predictive maintenance is costly and may not reduce failures.",
        counter_arguments=[
            "Initial costs may be high.",
            "Savings may not justify investment.",
            "Other factors may affect failure rates."
        ],
        resolution_strategy="Track ROI and adjust program scope.",
        entity_scope="All monitored equipment",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ISO 17359"
    ),
    DoctrineBlock(
        topic="Vibration Analysis for Safety Improvement",
        keywords=["safety", "vibration", "failure prevention", "risk reduction"],
        conclusion_template="If vibration analysis identifies faults early, safety risk is reduced.",
        reasoning_framework="""
        1. Monitor critical equipment for vibration faults.
        2. Investigate and correct faults promptly.
        3. Track safety incidents and correlate with vibration findings.
        4. Report safety improvements to management.
        5. Adjust monitoring scope as needed.
        """,
        key_factors=["Fault detection", "Incident tracking", "Risk reduction", "Reporting"],
        primary_authority=["ISO 45001", "Practical Condition Monitoring"],
        burden_holder="Safety Manager",
        adversary_position="Safety improvements are due to other programs.",
        counter_arguments=[
            "Other safety initiatives may reduce risk.",
            "Correlation does not imply causation.",
            "Data may be insufficient."
        ],
        resolution_strategy="Integrate vibration analysis with safety management system.",
        entity_scope="All critical equipment",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ISO 45001"
    ),
    DoctrineBlock(
        topic="Vibration Analysis for Warranty Claims",
        keywords=["warranty", "claim", "OEM", "vibration data", "failure documentation"],
        conclusion_template="If vibration data documents fault progression, warranty claim is supported.",
        reasoning_framework="""
        1. Collect and archive vibration data from commissioning.
        2. Document fault progression and corrective actions.
        3. Present data to OEM for warranty claim.
        4. Support claim with trend analysis and failure reports.
        5. Negotiate resolution with OEM.
        """,
        key_factors=["Data archiving", "Fault documentation", "Trend analysis", "OEM negotiation"],
        primary_authority=["OEM Warranty Policy", "ISO 9001"],
        burden_holder="Asset Owner",
        adversary_position="Data is insufficient or inconclusive.",
        counter_arguments=[
            "Data gaps may weaken claim.",
            "OEM may dispute analysis.",
            "Other factors may contribute to failure."
        ],
        resolution_strategy="Maintain comprehensive records and consult legal if needed.",
        entity_scope="All warranted equipment",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OEM Warranty Policy"
    ),
    DoctrineBlock(
        topic="Vibration Analysis for Continuous Improvement",
        keywords=["continuous improvement", "Kaizen", "vibration", "maintenance optimization"],
        conclusion_template="If vibration analysis is used for continuous improvement, maintenance effectiveness increases.",
        reasoning_framework="""
        1. Review vibration analysis findings regularly.
        2. Identify recurring faults and root causes.
        3. Implement corrective and preventive actions.
        4. Track improvement metrics (MTBF, downtime).
        5. Adjust maintenance strategy as needed.
        """,
        key_factors=["Review frequency", "Root cause analysis", "Improvement metrics", "Strategy adjustment"],
        primary_authority=["ISO 9001", "Practical Condition Monitoring"],
        burden_holder="Maintenance Manager",
        adversary_position="Improvements are due to other initiatives.",
        counter_arguments=[
            "Other programs may affect results.",
            "Data may be insufficient.",
            "Improvements may not be sustained."
        ],
        resolution_strategy="Integrate vibration analysis with continuous improvement process.",
        entity_scope="All maintenance programs",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ISO 9001"
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