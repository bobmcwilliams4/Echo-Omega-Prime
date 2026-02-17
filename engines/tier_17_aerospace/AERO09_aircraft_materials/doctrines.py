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
        topic="CFRP Quasi-Isotropic Layup Design",
        keywords=["CFRP", "quasi-isotropic", "layup", "composite", "fiber orientation", "aerospace"],
        conclusion_template="A quasi-isotropic layup for CFRP should utilize a symmetric and balanced stacking sequence, typically [0/+45/-45/90]s, to approximate isotropic in-plane properties and meet AERO09 structural requirements.",
        reasoning_framework="""
        1. Review the required in-plane mechanical properties for the component.
        2. Select a stacking sequence that balances 0°, ±45°, and 90° plies to achieve quasi-isotropy.
        3. Ensure symmetry and balance to minimize warping and residual stresses.
        4. Validate the layup via classical laminate theory and finite element analysis.
        5. Reference CMH-17 and SAE AIR1371 for aerospace best practices.
        6. Confirm compliance with AERO09-specific load cases and environmental conditions.
        7. Document layup schedule and rationale for traceability.
        """,
        key_factors=[
            "Ply orientation and sequence",
            "Symmetry and balance",
            "Mechanical property targets",
            "Manufacturability",
            "Damage tolerance",
            "Regulatory compliance"
        ],
        primary_authority=[
            "CMH-17 Composite Materials Handbook",
            "SAE AIR1371",
            "AERO09 Structural Design Manual"
        ],
        burden_holder="Design Engineer",
        adversary_position="Alternative layups may offer improved out-of-plane properties or reduced cost.",
        counter_arguments=[
            "Non-quasi-isotropic layups can lead to anisotropic behavior and unpredictable failure modes.",
            "AERO09 requires quasi-isotropic properties for primary structure."
        ],
        resolution_strategy="Demonstrate equivalency through test data and analysis if deviating from quasi-isotropic layup.",
        entity_scope="Primary and secondary CFRP structures in AERO09",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="CMH-17, Section 2.2.3"
    ),
    DoctrineBlock(
        topic="Aluminum 7075-T6 vs 2024-T3 Alloy Selection",
        keywords=["Aluminum", "7075-T6", "2024-T3", "alloy", "selection", "aircraft", "structural"],
        conclusion_template="Select 7075-T6 for high-strength, fatigue-critical AERO09 components; use 2024-T3 where superior fracture toughness and formability are required.",
        reasoning_framework="""
        1. Compare mechanical properties: 7075-T6 offers higher ultimate tensile strength but lower fracture toughness than 2024-T3.
        2. Assess corrosion resistance: 2024-T3 is more susceptible to intergranular corrosion; both require protection.
        3. Evaluate fatigue performance for the intended application.
        4. Consider manufacturability: 2024-T3 is more formable and weldable.
        5. Reference MMPDS and AERO09 material allowables.
        6. Factor in cost and availability.
        7. Document selection rationale and ensure traceability.
        """,
        key_factors=[
            "Tensile and yield strength",
            "Fracture toughness",
            "Fatigue resistance",
            "Corrosion behavior",
            "Formability",
            "Cost"
        ],
        primary_authority=[
            "MMPDS-15",
            "AERO09 Materials Specification",
            "SAE AMS-QQ-A-250"
        ],
        burden_holder="Materials Engineer",
        adversary_position="7075-T6's lower toughness may be unacceptable for damage-tolerant design.",
        counter_arguments=[
            "7075-T6's superior strength justifies its use in highly loaded parts with adequate inspection intervals.",
            "2024-T3's toughness is preferred for fuselage skins and areas prone to impact."
        ],
        resolution_strategy="Perform trade study and document selection in the AERO09 material review board (MRB) minutes.",
        entity_scope="Metallic structural components in AERO09",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="MMPDS-15, Table 2.3.1"
    ),
    DoctrineBlock(
        topic="Titanium Ti-6Al-4V Applications and Heat Treatment",
        keywords=["Titanium", "Ti-6Al-4V", "heat treatment", "applications", "beta anneal", "solution treat", "aging"],
        conclusion_template="Apply Ti-6Al-4V in high-temperature, high-strength AERO09 applications; utilize solution treatment and aging (STA) for optimal properties.",
        reasoning_framework="""
        1. Identify components subjected to temperatures up to 350°C and requiring high specific strength.
        2. Select Ti-6Al-4V due to its favorable strength-to-weight ratio and corrosion resistance.
        3. Choose heat treatment: STA for maximum strength, or annealing for improved ductility.
        4. Reference AMS 2801 and AERO09 heat treat procedures.
        5. Validate microstructure and mechanical properties via metallography and tensile testing.
        6. Ensure traceability of heat treat records.
        7. Document application and treatment in the AERO09 process database.
        """,
        key_factors=[
            "Operating temperature",
            "Strength and ductility requirements",
            "Corrosion environment",
            "Heat treat process control",
            "Traceability"
        ],
        primary_authority=[
            "AMS 2801",
            "AERO09 Process Specification",
            "MMPDS-15"
        ],
        burden_holder="Process Engineer",
        adversary_position="Annealed Ti-6Al-4V offers better toughness but lower strength.",
        counter_arguments=[
            "STA provides the best combination of strength and fatigue resistance for most AERO09 applications.",
            "Annealed condition may be justified for parts requiring extensive forming."
        ],
        resolution_strategy="Select heat treatment based on component criticality and document in process planning.",
        entity_scope="AERO09 titanium alloy parts",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="AMS 2801"
    ),
    DoctrineBlock(
        topic="Nickel Superalloys for Turbine Hot Section",
        keywords=["Nickel superalloy", "turbine", "hot section", "Inconel", "creep", "oxidation", "thermal fatigue"],
        conclusion_template="Utilize precipitation-strengthened nickel superalloys (e.g., Inconel 718, Rene 41) for AERO09 turbine hot section components operating above 650°C.",
        reasoning_framework="""
        1. Analyze thermal environment and mechanical loads in the hot section.
        2. Select nickel superalloys for their superior creep, oxidation, and thermal fatigue resistance.
        3. Reference MMPDS and OEM specifications for allowables.
        4. Consider cast vs. wrought vs. powder metallurgy forms.
        5. Validate microstructure and properties via high-temperature testing.
        6. Ensure proper coating selection for oxidation/corrosion protection.
        7. Document alloy selection and justification in AERO09 materials database.
        """,
        key_factors=[
            "Operating temperature",
            "Creep and fatigue resistance",
            "Oxidation/corrosion resistance",
            "Manufacturing process",
            "Cost and availability"
        ],
        primary_authority=[
            "MMPDS-15",
            "AERO09 Turbine Materials Specification",
            "SAE AMS 5662"
        ],
        burden_holder="Hot Section Materials Engineer",
        adversary_position="Ceramic matrix composites may offer higher temperature capability.",
        counter_arguments=[
            "Nickel superalloys have proven reliability and established supply chains.",
            "CMCs are not yet fully qualified for AERO09 turbine applications."
        ],
        resolution_strategy="Monitor CMC developments; use nickel superalloys per current AERO09 design.",
        entity_scope="AERO09 turbine hot section",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AERO09 Turbine Materials Specification"
    ),
    DoctrineBlock(
        topic="S-N Curve Fatigue Analysis and Endurance Limit",
        keywords=["S-N curve", "fatigue", "endurance limit", "fatigue life", "cyclic loading", "test data"],
        conclusion_template="Determine fatigue life using S-N curves derived from statistically significant test data; apply endurance limit for ferrous alloys, or fatigue strength at 10^7 cycles for non-ferrous alloys.",
        reasoning_framework="""
        1. Obtain S-N curve data for the specific material, geometry, and surface condition.
        2. Apply mean stress correction (e.g., Goodman, Gerber) as required.
        3. For ferrous alloys, use the endurance limit as the fatigue threshold.
        4. For non-ferrous alloys, define fatigue strength at 10^7 cycles.
        5. Incorporate knockdown factors for surface finish, size, and environment.
        6. Validate with coupon and component-level testing.
        7. Document analysis and assumptions in the AERO09 fatigue substantiation report.
        """,
        key_factors=[
            "Material S-N data",
            "Mean stress effects",
            "Surface condition",
            "Environmental factors",
            "Statistical basis"
        ],
        primary_authority=[
            "MMPDS-15",
            "AERO09 Fatigue Analysis Manual",
            "ASTM E466"
        ],
        burden_holder="Fatigue Analyst",
        adversary_position="S-N data may not capture all real-world loading spectra.",
        counter_arguments=[
            "S-N curves are industry standard for fatigue substantiation.",
            "Supplement with spectrum fatigue testing as required."
        ],
        resolution_strategy="Use S-N approach for initial design; validate with full-scale testing.",
        entity_scope="All fatigue-critical AERO09 components",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="MMPDS-15, Section 7"
    ),
    DoctrineBlock(
        topic="Paris Law Crack Growth and Damage Tolerance",
        keywords=["Paris Law", "crack growth", "damage tolerance", "fracture mechanics", "aerospace", "inspection interval"],
        conclusion_template="Apply Paris Law (da/dN = C*(ΔK)^m) to predict crack growth rates and establish inspection intervals for AERO09 damage-tolerant structure.",
        reasoning_framework="""
        1. Identify critical crack locations and initial flaw sizes.
        2. Obtain Paris Law constants (C, m) for the relevant material and environment.
        3. Calculate stress intensity range (ΔK) for expected loading.
        4. Integrate Paris Law to predict crack growth to critical size.
        5. Establish inspection intervals ensuring crack detectability before failure.
        6. Reference FAA AC 25.571 and AERO09 damage tolerance manual.
        7. Document analysis and inspection plan.
        """,
        key_factors=[
            "Material Paris Law constants",
            "Initial flaw size",
            "Stress intensity factor",
            "Inspection method capability",
            "Environmental effects"
        ],
        primary_authority=[
            "FAA AC 25.571",
            "AERO09 Damage Tolerance Manual",
            "ASTM E647"
        ],
        burden_holder="Damage Tolerance Analyst",
        adversary_position="Paris Law does not account for short crack or closure effects.",
        counter_arguments=[
            "Paris Law is validated for long cracks; use alternative models for short cracks.",
            "Conservative assumptions mitigate uncertainty."
        ],
        resolution_strategy="Supplement Paris Law with experimental data for short crack growth.",
        entity_scope="AERO09 primary structure",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.571"
    ),
    DoctrineBlock(
        topic="CMH-17 Statistical Allowables Development",
        keywords=["CMH-17", "statistical allowables", "A-basis", "B-basis", "composite", "test plan"],
        conclusion_template="Develop A- and B-basis allowables per CMH-17, using minimum 6-batch, 18-panel test programs for AERO09 composite materials.",
        reasoning_framework="""
        1. Design test program per CMH-17, ensuring statistical validity.
        2. Test at least 6 batches, 3 panels per batch, for each property and condition.
        3. Analyze data using appropriate statistical methods (e.g., tolerance intervals).
        4. Establish A-basis (99/95) and B-basis (90/95) allowables.
        5. Document all test procedures, data, and analysis.
        6. Reference allowables in AERO09 material and structural substantiation.
        7. Maintain traceability to test coupons and panels.
        """,
        key_factors=[
            "Number of batches and panels",
            "Statistical method",
            "Test conditions",
            "Data traceability",
            "Regulatory compliance"
        ],
        primary_authority=[
            "CMH-17, Volume 1",
            "AERO09 Composite Materials Specification",
            "FAA AC 20-107B"
        ],
        burden_holder="Composite Materials Engineer",
        adversary_position="Reduced-basis allowables may be justified for non-critical structure.",
        counter_arguments=[
            "A- and B-basis are required for primary structure per AERO09 and FAA policy.",
            "Reduced-basis only for non-critical, with proper justification."
        ],
        resolution_strategy="Follow CMH-17 unless deviation is approved by AERO09 MRB.",
        entity_scope="AERO09 composite materials",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="CMH-17, Section 8.2"
    ),
    DoctrineBlock(
        topic="BVID and Compression After Impact (CAI) Testing",
        keywords=["BVID", "CAI", "compression after impact", "composite", "damage tolerance", "test"],
        conclusion_template="Perform CAI testing per ASTM D7137 on BVID panels to establish post-impact strength for AERO09 composite structures.",
        reasoning_framework="""
        1. Generate barely visible impact damage (BVID) per ASTM D7136.
        2. Test impacted panels in compression per ASTM D7137.
        3. Record residual strength and failure mode.
        4. Use results to set design allowables and damage limits.
        5. Reference CAI data in AERO09 structural substantiation.
        6. Document test setup, results, and traceability.
        7. Maintain compliance with regulatory and OEM requirements.
        """,
        key_factors=[
            "Impact energy and location",
            "Panel geometry and layup",
            "Test method",
            "Residual strength",
            "Failure mode"
        ],
        primary_authority=[
            "ASTM D7136",
            "ASTM D7137",
            "AERO09 Composite Test Plan"
        ],
        burden_holder="Test Engineer",
        adversary_position="CAI tests may not represent all in-service damage scenarios.",
        counter_arguments=[
            "BVID/CAI is industry standard for composite damage tolerance.",
            "Supplement with additional tests as needed for unique threats."
        ],
        resolution_strategy="Use BVID/CAI as baseline; expand test matrix for special cases.",
        entity_scope="AERO09 composite structure",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASTM D7137"
    ),
    DoctrineBlock(
        topic="Corrosion Protection Schemes for Aluminum Alloys",
        keywords=["corrosion", "protection", "aluminum", "alloy", "anodize", "primer", "sealant"],
        conclusion_template="Apply Type II anodize, chromate primer, and polysulfide sealant for corrosion protection of AERO09 aluminum alloys in aggressive environments.",
        reasoning_framework="""
        1. Assess environmental exposure (humidity, salt spray, temperature).
        2. Specify Type II sulfuric acid anodize per MIL-A-8625.
        3. Apply chromate or non-chromate primer per MIL-PRF-23377.
        4. Seal faying surfaces with polysulfide sealant per AMS 3276.
        5. Validate protection via salt spray and cyclic corrosion testing.
        6. Document process and inspection results.
        7. Maintain traceability to lot and batch.
        """,
        key_factors=[
            "Environmental severity",
            "Coating compatibility",
            "Process control",
            "Inspection and testing",
            "Regulatory requirements"
        ],
        primary_authority=[
            "MIL-A-8625",
            "MIL-PRF-23377",
            "AERO09 Corrosion Control Manual"
        ],
        burden_holder="Surface Finishing Engineer",
        adversary_position="Non-chromate alternatives may be required for environmental compliance.",
        counter_arguments=[
            "Non-chromate primers are approved for AERO09 if validated by testing.",
            "Chromate systems remain baseline for maximum protection."
        ],
        resolution_strategy="Use non-chromate systems where required by law; otherwise, default to chromate.",
        entity_scope="AERO09 aluminum structure",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="AERO09 Corrosion Control Manual"
    ),
    DoctrineBlock(
        topic="Additive Manufacturing Qualification for Aerospace",
        keywords=["additive manufacturing", "AM", "qualification", "aerospace", "process control", "test"],
        conclusion_template="Qualify AM processes for AERO09 per MMPDS and AMS 7003, including process parameter control, coupon testing, and full-scale validation.",
        reasoning_framework="""
        1. Select AM process (e.g., LPBF, EBM) and material.
        2. Establish process parameter windows and monitor via in-situ sensing.
        3. Produce and test coupons for mechanical property validation.
        4. Perform NDE and metallography to assess defects and microstructure.
        5. Conduct full-scale part testing for critical applications.
        6. Document all process and test data for traceability.
        7. Reference MMPDS and AMS 7003 for qualification requirements.
        """,
        key_factors=[
            "Process parameter control",
            "Material traceability",
            "Mechanical property validation",
            "NDE and inspection",
            "Statistical process control"
        ],
        primary_authority=[
            "MMPDS-15",
            "AMS 7003",
            "AERO09 Additive Manufacturing Specification"
        ],
        burden_holder="AM Process Engineer",
        adversary_position="AM variability may preclude use in critical structure.",
        counter_arguments=[
            "Qualification per AMS 7003 ensures repeatability.",
            "Restrict AM to non-critical parts if necessary."
        ],
        resolution_strategy="Limit AM to Class III/IV structure until full qualification is achieved.",
        entity_scope="AERO09 AM parts",
        confidence=0.92,
        confidence_zone="Medium",
        controlling_precedent="AMS 7003"
    ),
    DoctrineBlock(
        topic="Fiber Volume Fraction and Void Content",
        keywords=["fiber volume fraction", "void content", "composite", "quality control", "resin", "laminate"],
        conclusion_template="Maintain fiber volume fraction between 55-60% and void content below 1.5% for AERO09 structural laminates per CMH-17.",
        reasoning_framework="""
        1. Select prepreg or resin infusion process to achieve target fiber volume.
        2. Monitor and control process parameters (e.g., pressure, temperature, resin flow).
        3. Measure fiber volume and void content via burn-off or microscopy.
        4. Reference CMH-17 for acceptance criteria.
        5. Document all measurements and corrective actions.
        6. Reject or rework laminates outside specification.
        7. Maintain traceability to batch and panel.
        """,
        key_factors=[
            "Process control",
            "Measurement accuracy",
            "Material batch variability",
            "Acceptance criteria",
            "Traceability"
        ],
        primary_authority=[
            "CMH-17, Volume 2",
            "AERO09 Composite Quality Manual",
            "ASTM D3171"
        ],
        burden_holder="Quality Engineer",
        adversary_position="Higher fiber volume may increase brittleness.",
        counter_arguments=[
            "CMH-17 limits are based on optimal balance of properties.",
            "Adjust for specific applications as justified by test data."
        ],
        resolution_strategy="Document deviations and obtain MRB approval for out-of-spec laminates.",
        entity_scope="AERO09 composite laminates",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="CMH-17, Section 2.5"
    ),
    DoctrineBlock(
        topic="Resin Transfer Molding (RTM) Process",
        keywords=["RTM", "resin transfer molding", "composite", "process", "aerospace", "quality"],
        conclusion_template="Implement RTM for AERO09 secondary composite structures, ensuring process control and void content <1.5% per CMH-17.",
        reasoning_framework="""
        1. Design mold and preform for uniform resin flow.
        2. Control resin viscosity, injection pressure, and temperature.
        3. Monitor fill and cure via sensors and data logging.
        4. Inspect finished parts for voids, dry spots, and fiber wash.
        5. Validate mechanical properties with coupon testing.
        6. Reference CMH-17 and AERO09 process specs.
        7. Document all process parameters and inspection results.
        """,
        key_factors=[
            "Mold design",
            "Resin and fiber selection",
            "Process parameter control",
            "Inspection and testing",
            "Documentation"
        ],
        primary_authority=[
            "CMH-17, Volume 3",
            "AERO09 Composite Process Specification",
            "ASTM D2734"
        ],
        burden_holder="Process Engineer",
        adversary_position="RTM may not achieve properties of autoclave-cured prepreg.",
        counter_arguments=[
            "RTM is suitable for secondary structure with proper process control.",
            "Use prepreg/autoclave for primary structure."
        ],
        resolution_strategy="Limit RTM to non-critical applications unless qualified by test.",
        entity_scope="AERO09 composite secondary structure",
        confidence=0.91,
        confidence_zone="Medium",
        controlling_precedent="CMH-17, Section 3.4"
    ),
    DoctrineBlock(
        topic="Honeycomb Core Selection and Properties",
        keywords=["honeycomb core", "selection", "properties", "Nomex", "aluminum", "compression", "shear"],
        conclusion_template="Select Nomex or aluminum honeycomb core for AERO09 sandwich panels based on temperature, strength, and fire resistance requirements.",
        reasoning_framework="""
        1. Determine panel application and required properties (compression, shear, fire resistance).
        2. Select Nomex for fire resistance and low weight; aluminum for higher strength and temperature.
        3. Reference MMPDS and OEM specs for core properties.
        4. Validate core-cell size, density, and orientation.
        5. Document selection rationale and traceability.
        6. Test panels for flatwise compression and shear per ASTM standards.
        7. Maintain compliance with AERO09 sandwich panel specification.
        """,
        key_factors=[
            "Core material",
            "Cell size and density",
            "Mechanical properties",
            "Fire resistance",
            "Cost"
        ],
        primary_authority=[
            "MMPDS-15",
            "AERO09 Sandwich Panel Specification",
            "ASTM C365"
        ],
        burden_holder="Design Engineer",
        adversary_position="Foam cores may offer lower cost and easier processing.",
        counter_arguments=[
            "Honeycomb cores provide superior strength-to-weight ratio.",
            "Foam cores are limited to non-structural applications."
        ],
        resolution_strategy="Use honeycomb for all load-bearing AERO09 sandwich panels.",
        entity_scope="AERO09 sandwich structures",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AERO09 Sandwich Panel Specification"
    ),
    # --- Additional 28+ DoctrineBlocks follow ---
    DoctrineBlock(
        topic="Prepreg Material Shelf Life and Storage",
        keywords=["prepreg", "shelf life", "storage", "composite", "freezer", "expiration"],
        conclusion_template="Store prepreg at -18°C or below; use within manufacturer’s shelf life or requalify per AERO09 procedures.",
        reasoning_framework="""
        1. Verify prepreg batch expiration date upon receipt.
        2. Store at -18°C or colder in monitored freezers.
        3. Record all freezer entry/exit events and cumulative out-time.
        4. Do not use expired prepreg without requalification testing.
        5. Reference manufacturer’s technical data sheet and AERO09 material control procedures.
        6. Discard or requalify expired material per CMH-17 guidelines.
        7. Maintain full traceability to batch and panel.
        """,
        key_factors=[
            "Storage temperature",
            "Shelf life",
            "Out-time control",
            "Traceability",
            "Requalification procedures"
        ],
        primary_authority=[
            "CMH-17, Section 2.7",
            "AERO09 Material Control Manual",
            "Manufacturer TDS"
        ],
        burden_holder="Material Handler",
        adversary_position="Short shelf life increases material waste and cost.",
        counter_arguments=[
            "Strict control ensures laminate quality and performance.",
            "Requalification can extend shelf life if justified by test."
        ],
        resolution_strategy="Monitor inventory and rotate stock to minimize waste.",
        entity_scope="AERO09 composite manufacturing",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="CMH-17, Section 2.7"
    ),
    DoctrineBlock(
        topic="Composite Bonded Joint Design",
        keywords=["composite", "bonded joint", "design", "adhesive", "peel", "shear"],
        conclusion_template="Design bonded joints with stepped or scarfed geometry to maximize shear and minimize peel stresses per CMH-17.",
        reasoning_framework="""
        1. Analyze load paths and joint geometry.
        2. Favor scarf or stepped joints over simple lap joints to reduce peel stress.
        3. Select adhesive system compatible with adherends and service environment.
        4. Validate joint strength with coupon and subcomponent testing.
        5. Reference CMH-17 and AERO09 bonding specification.
        6. Document joint design and test data.
        7. Maintain process control and inspection records.
        """,
        key_factors=[
            "Joint geometry",
            "Adhesive selection",
            "Surface preparation",
            "Load path",
            "Environmental durability"
        ],
        primary_authority=[
            "CMH-17, Section 6",
            "AERO09 Bonding Specification",
            "ASTM D1002"
        ],
        burden_holder="Design Engineer",
        adversary_position="Mechanical fasteners may provide more reliable load path.",
        counter_arguments=[
            "Bonded joints reduce weight and stress concentrations.",
            "Hybrid joints can combine benefits of both methods."
        ],
        resolution_strategy="Use bonded joints where qualified by test; supplement with fasteners as needed.",
        entity_scope="AERO09 composite structure",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="CMH-17, Section 6"
    ),
    DoctrineBlock(
        topic="Composite Fastener Hole Quality",
        keywords=["composite", "fastener hole", "quality", "drilling", "delamination", "inspection"],
        conclusion_template="Drill composite fastener holes with diamond or carbide tools at low feed rates; inspect for delamination per AERO09 standards.",
        reasoning_framework="""
        1. Select appropriate drill bit geometry and material (diamond or carbide).
        2. Use low feed and speed to minimize heat and delamination.
        3. Back up laminate with sacrificial material during drilling.
        4. Inspect holes visually and with NDE for delamination or fiber pull-out.
        5. Reference AERO09 hole quality acceptance criteria.
        6. Document all drilling parameters and inspection results.
        7. Repair or reject out-of-spec holes per MRB procedures.
        """,
        key_factors=[
            "Tool selection",
            "Drilling parameters",
            "Inspection method",
            "Repair criteria",
            "Traceability"
        ],
        primary_authority=[
            "AERO09 Composite Assembly Manual",
            "CMH-17, Section 7",
            "ASTM D6262"
        ],
        burden_holder="Assembly Technician",
        adversary_position="Automated drilling may increase throughput but reduce quality.",
        counter_arguments=[
            "Automated systems must be qualified for hole quality.",
            "Manual drilling preferred for critical locations."
        ],
        resolution_strategy="Qualify automated systems before use on primary structure.",
        entity_scope="AERO09 composite assembly",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AERO09 Composite Assembly Manual"
    ),
    DoctrineBlock(
        topic="Composite Surface Preparation for Bonding",
        keywords=["composite", "surface preparation", "bonding", "abrade", "solvent wipe"],
        conclusion_template="Abrade and solvent-wipe composite surfaces prior to bonding per AERO09 specification to ensure adhesive performance.",
        reasoning_framework="""
        1. Abrade bonding surfaces with fine grit (e.g., 180-220) sandpaper.
        2. Remove dust and debris with clean, dry air.
        3. Wipe with approved solvent (e.g., isopropyl alcohol).
        4. Avoid contamination between preparation and bonding.
        5. Reference AERO09 bonding procedure and CMH-17.
        6. Document preparation steps and inspection results.
        7. Reject or rework surfaces not meeting criteria.
        """,
        key_factors=[
            "Abrasive selection",
            "Solvent compatibility",
            "Contamination control",
            "Process documentation",
            "Inspection"
        ],
        primary_authority=[
            "AERO09 Bonding Specification",
            "CMH-17, Section 6.2",
            "ASTM D2093"
        ],
        burden_holder="Bonding Technician",
        adversary_position="Plasma or laser surface treatment may improve bond strength.",
        counter_arguments=[
            "Advanced methods require qualification and process control.",
            "Abrade/solvent-wipe is proven and repeatable."
        ],
        resolution_strategy="Use advanced methods only after qualification and MRB approval.",
        entity_scope="AERO09 composite bonding",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AERO09 Bonding Specification"
    ),
    DoctrineBlock(
        topic="Composite Repair Patch Design",
        keywords=["composite", "repair", "patch", "scarf", "step", "structural"],
        conclusion_template="Design scarf or stepped repair patches with minimum 20:1 taper for AERO09 primary composite structure.",
        reasoning_framework="""
        1. Assess damage size and location.
        2. Select scarf (preferred) or stepped patch geometry.
        3. Use minimum 20:1 taper ratio to ensure load transfer.
        4. Match parent laminate layup and fiber orientation.
        5. Validate repair with coupon and subcomponent testing.
        6. Reference AERO09 repair manual and CMH-17.
        7. Document repair design and execution.
        """,
        key_factors=[
            "Patch geometry",
            "Taper ratio",
            "Layup matching",
            "Bond quality",
            "Testing"
        ],
        primary_authority=[
            "AERO09 Composite Repair Manual",
            "CMH-17, Section 9",
            "ASTM D3039"
        ],
        burden_holder="Repair Engineer",
        adversary_position="Bolted repairs may be faster for field applications.",
        counter_arguments=[
            "Bonded repairs restore original properties and aerodynamics.",
            "Bolted repairs introduce stress concentrations."
        ],
        resolution_strategy="Use bonded repairs for primary structure; bolted only for temporary fixes.",
        entity_scope="AERO09 composite repair",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="AERO09 Composite Repair Manual"
    ),
    DoctrineBlock(
        topic="Composite Cure Cycle Control",
        keywords=["composite", "cure cycle", "autoclave", "oven", "temperature", "pressure"],
        conclusion_template="Control cure cycle per prepreg manufacturer’s specification; monitor temperature and pressure throughout cycle for AERO09 laminates.",
        reasoning_framework="""
        1. Program autoclave/oven with manufacturer’s recommended cure profile.
        2. Place thermocouples at critical laminate locations.
        3. Monitor and record temperature and pressure throughout cure.
        4. Validate cure with resin flow and degree of cure tests.
        5. Reference AERO09 process specification and CMH-17.
        6. Document cure cycle and any deviations.
        7. Reject or rework out-of-spec laminates per MRB.
        """,
        key_factors=[
            "Cure profile",
            "Temperature uniformity",
            "Pressure control",
            "Process monitoring",
            "Documentation"
        ],
        primary_authority=[
            "AERO09 Composite Process Specification",
            "CMH-17, Section 3.2",
            "Manufacturer TDS"
        ],
        burden_holder="Process Engineer",
        adversary_position="Out-of-autoclave processes may reduce cost.",
        counter_arguments=[
            "Autoclave cure ensures highest laminate quality.",
            "OOA processes require separate qualification."
        ],
        resolution_strategy="Use OOA only for non-critical structure unless qualified by test.",
        entity_scope="AERO09 composite manufacturing",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AERO09 Composite Process Specification"
    ),
    DoctrineBlock(
        topic="Composite Environmental Conditioning",
        keywords=["composite", "environmental conditioning", "hot/wet", "cold/dry", "test", "aging"],
        conclusion_template="Condition composite coupons at 70°C/85% RH for 14 days for hot/wet property testing per CMH-17 and AERO09 requirements.",
        reasoning_framework="""
        1. Prepare test coupons per CMH-17 geometry.
        2. Expose coupons to 70°C/85% RH for 14 days (hot/wet) or -55°C for 24h (cold/dry).
        3. Test mechanical properties immediately after conditioning.
        4. Reference AERO09 test plan and CMH-17.
        5. Document conditioning parameters and test results.
        6. Use data for allowables and design substantiation.
        7. Maintain traceability to batch and panel.
        """,
        key_factors=[
            "Conditioning environment",
            "Exposure time",
            "Test timing",
            "Documentation",
            "Traceability"
        ],
        primary_authority=[
            "CMH-17, Section 8.3",
            "AERO09 Test Plan",
            "ASTM D5229"
        ],
        burden_holder="Test Engineer",
        adversary_position="In-service conditions may differ from test environments.",
        counter_arguments=[
            "Standard environments ensure comparability of data.",
            "Supplement with additional conditioning if required."
        ],
        resolution_strategy="Expand test matrix for unique AERO09 environments as needed.",
        entity_scope="AERO09 composite materials testing",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="CMH-17, Section 8.3"
    ),
    DoctrineBlock(
        topic="Composite Out-Time Tracking",
        keywords=["composite", "out-time", "tracking", "prepreg", "resin", "shelf life"],
        conclusion_template="Track cumulative out-time for all prepreg and resin batches; do not exceed manufacturer’s maximum out-time for AERO09 laminates.",
        reasoning_framework="""
        1. Record all out-of-freezer events for each batch.
        2. Sum cumulative out-time and compare to manufacturer’s limit.
        3. Mark and segregate material approaching out-time expiration.
        4. Discard or requalify material exceeding out-time.
        5. Reference AERO09 material control procedures.
        6. Document all out-time events and corrective actions.
        7. Maintain traceability to batch and panel.
        """,
        key_factors=[
            "Out-time limit",
            "Tracking system",
            "Material segregation",
            "Documentation",
            "Traceability"
        ],
        primary_authority=[
            "AERO09 Material Control Manual",
            "CMH-17, Section 2.7",
            "Manufacturer TDS"
        ],
        burden_holder="Material Handler",
        adversary_position="Manual tracking is error-prone.",
        counter_arguments=[
            "Electronic tracking systems are recommended for accuracy.",
            "Manual logs acceptable with proper oversight."
        ],
        resolution_strategy="Implement electronic tracking where possible.",
        entity_scope="AERO09 composite manufacturing",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="AERO09 Material Control Manual"
    ),
    DoctrineBlock(
        topic="Composite Ply Drop-Off Design",
        keywords=["composite", "ply drop-off", "taper", "stress concentration", "design"],
        conclusion_template="Taper ply drop-offs at a maximum slope of 1:30 to minimize stress concentrations in AERO09 composite laminates.",
        reasoning_framework="""
        1. Analyze load path and laminate thickness transitions.
        2. Taper ply drop-offs at no steeper than 1:30 slope.
        3. Stagger drop-off locations to avoid local thickness changes.
        4. Validate design with FEA and coupon testing.
        5. Reference AERO09 design manual and CMH-17.
        6. Document ply drop-off locations and rationale.
        7. Inspect finished laminates for compliance.
        """,
        key_factors=[
            "Taper ratio",
            "Drop-off location",
            "Stress analysis",
            "Testing",
            "Inspection"
        ],
        primary_authority=[
            "AERO09 Composite Design Manual",
            "CMH-17, Section 2.4",
            "ASTM D3039"
        ],
        burden_holder="Design Engineer",
        adversary_position="Steeper tapers may be justified for non-critical structure.",
        counter_arguments=[
            "1:30 is standard for primary structure.",
            "Deviations require test data and MRB approval."
        ],
        resolution_strategy="Document and justify any deviations from standard taper.",
        entity_scope="AERO09 composite structure",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AERO09 Composite Design Manual"
    ),
    DoctrineBlock(
        topic="Composite Tooling Material Selection",
        keywords=["composite", "tooling", "material selection", "invar", "aluminum", "epoxy"],
        conclusion_template="Use Invar tooling for tight-tolerance AERO09 composite parts; aluminum or epoxy tools for prototypes or low-rate production.",
        reasoning_framework="""
        1. Assess dimensional tolerance and production rate requirements.
        2. Select Invar for minimal thermal expansion and high repeatability.
        3. Use aluminum or epoxy for lower cost and faster turnaround in prototypes.
        4. Validate tool surface finish and dimensional stability.
        5. Reference AERO09 tooling specification.
        6. Document tooling material and maintenance plan.
        7. Inspect tools regularly for wear and damage.
        """,
        key_factors=[
            "Thermal expansion",
            "Dimensional stability",
            "Cost",
            "Production rate",
            "Tool life"
        ],
        primary_authority=[
            "AERO09 Tooling Specification",
            "CMH-17, Section 3.5",
            "SAE AIR1418"
        ],
        burden_holder="Tooling Engineer",
        adversary_position="Epoxy tools may distort under autoclave conditions.",
        counter_arguments=[
            "Epoxy tools are suitable only for low-temperature cures.",
            "Invar is preferred for autoclave and high-rate production."
        ],
        resolution_strategy="Match tooling material to process and production needs.",
        entity_scope="AERO09 composite manufacturing",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AERO09 Tooling Specification"
    ),
    DoctrineBlock(
        topic="Composite Nondestructive Evaluation (NDE)",
        keywords=["composite", "NDE", "ultrasonic", "thermography", "inspection"],
        conclusion_template="Use ultrasonic C-scan as primary NDE method for AERO09 composite laminates; supplement with thermography or shearography as needed.",
        reasoning_framework="""
        1. Select NDE method based on defect type and laminate geometry.
        2. Use ultrasonic C-scan for delamination and void detection.
        3. Apply thermography or shearography for large-area or complex shapes.
        4. Reference AERO09 NDE specification and ASTM standards.
        5. Document inspection results and defect disposition.
        6. Maintain inspector qualification and calibration records.
        7. Re-inspect after repair or rework.
        """,
        key_factors=[
            "Defect type",
            "Laminate geometry",
            "NDE method capability",
            "Inspector qualification",
            "Documentation"
        ],
        primary_authority=[
            "AERO09 NDE Specification",
            "ASTM E2580",
            "CMH-17, Section 10"
        ],
        burden_holder="NDE Inspector",
        adversary_position="Visual inspection may suffice for non-critical structure.",
        counter_arguments=[
            "Ultrasonic NDE is required for primary structure.",
            "Visual is only for non-critical or secondary parts."
        ],
        resolution_strategy="Follow NDE specification for part classification.",
        entity_scope="AERO09 composite inspection",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AERO09 NDE Specification"
    ),
    DoctrineBlock(
        topic="Composite Laminate Traceability",
        keywords=["composite", "laminate", "traceability", "batch", "panel", "documentation"],
        conclusion_template="Maintain full traceability from raw material batch to finished laminate for all AERO09 composite parts.",
        reasoning_framework="""
        1. Assign unique batch and panel IDs to all materials and parts.
        2. Record all process steps, inspections, and test results.
        3. Link laminate records to raw material certificates.
        4. Store traceability data in AERO09 quality management system.
        5. Reference CMH-17 and AERO09 quality manual.
        6. Audit traceability records regularly.
        7. Reject or quarantine parts with incomplete traceability.
        """,
        key_factors=[
            "Batch and panel ID",
            "Process documentation",
            "Inspection records",
            "Data management",
            "Audit"
        ],
        primary_authority=[
            "AERO09 Quality Manual",
            "CMH-17, Section 2.6",
            "AS9100"
        ],
        burden_holder="Quality Engineer",
        adversary_position="Traceability adds cost and administrative burden.",
        counter_arguments=[
            "Traceability is required for regulatory compliance.",
            "Reduces risk of undetected material or process issues."
        ],
        resolution_strategy="Automate traceability where possible to reduce burden.",
        entity_scope="AERO09 composite manufacturing",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="AERO09 Quality Manual"
    ),
    DoctrineBlock(
        topic="Composite Panel Flatness and Thickness Tolerance",
        keywords=["composite", "panel", "flatness", "thickness", "tolerance", "inspection"],
        conclusion_template="Inspect composite panels for flatness within ±0.5 mm/m and thickness within ±0.25 mm per AERO09 specification.",
        reasoning_framework="""
        1. Measure panel flatness and thickness at specified locations.
        2. Compare measurements to AERO09 tolerance requirements.
        3. Document all inspection results.
        4. Reject or rework panels outside tolerance.
        5. Reference AERO09 inspection procedure.
        6. Maintain traceability to batch and panel.
        7. Audit inspection records regularly.
        """,
        key_factors=[
            "Measurement method",
            "Tolerance limits",
            "Documentation",
            "Rework criteria",
            "Traceability"
        ],
        primary_authority=[
            "AERO09 Inspection Specification",
            "CMH-17, Section 2.8",
            "ASTM D2583"
        ],
        burden_holder="Quality Inspector",
        adversary_position="Relaxed tolerances may be acceptable for non-critical panels.",
        counter_arguments=[
            "Tight tolerances are required for aerodynamic and structural performance.",
            "Relaxation only with MRB approval."
        ],
        resolution_strategy="Document and justify any deviations from standard tolerances.",
        entity_scope="AERO09 composite panels",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AERO09 Inspection Specification"
    ),
    DoctrineBlock(
        topic="Composite Panel Edge Treatment",
        keywords=["composite", "panel", "edge treatment", "sealing", "delamination"],
        conclusion_template="Seal all exposed composite panel edges with compatible resin or edge sealant to prevent moisture ingress and delamination.",
        reasoning_framework="""
        1. Inspect all panel edges for exposed fibers or porosity.
        2. Apply compatible resin or edge sealant per AERO09 specification.
        3. Cure and inspect sealant for coverage and adhesion.
        4. Document edge treatment process and inspection.
        5. Reference CMH-17 and AERO09 panel specification.
        6. Rework or reject panels with incomplete edge sealing.
        7. Maintain traceability to batch and panel.
        """,
        key_factors=[
            "Sealant compatibility",
            "Coverage",
            "Cure quality",
            "Inspection",
            "Documentation"
        ],
        primary_authority=[
            "AERO09 Panel Specification",
            "CMH-17, Section 2.9",
            "ASTM D2093"
        ],
        burden_holder="Assembly Technician",
        adversary_position="Unsealed edges may be acceptable for interior panels.",
        counter_arguments=[
            "Edge sealing is required for all exposed edges.",
            "Interior panels may be exempt with MRB approval."
        ],
        resolution_strategy="Document and justify any exemptions from edge sealing.",
        entity_scope="AERO09 composite panels",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AERO09 Panel Specification"
    ),
    DoctrineBlock(
        topic="Composite Panel Lightning Strike Protection",
        keywords=["composite", "panel", "lightning strike protection", "LSP", "expanded foil"],
        conclusion_template="Integrate expanded copper or aluminum foil mesh for lightning strike protection in AERO09 exterior composite panels.",
        reasoning_framework="""
        1. Identify panels exposed to lightning strike risk.
        2. Integrate expanded foil mesh into outer ply during layup.
        3. Ensure electrical continuity and grounding per AERO09 LSP specification.
        4. Validate protection with simulated strike testing.
        5. Document LSP integration and inspection.
        6. Reference SAE ARP5412 and AERO09 LSP procedure.
        7. Repair or rework panels with LSP defects.
        """,
        key_factors=[
            "Foil mesh type",
            "Integration method",
            "Electrical continuity",
            "Testing",
            "Documentation"
        ],
        primary_authority=[
            "AERO09 LSP Specification",
            "SAE ARP5412",
            "CMH-17, Section 2.10"
        ],
        burden_holder="Design Engineer",
        adversary_position="LSP adds weight and complexity.",
        counter_arguments=[
            "LSP is required for exterior panels per regulatory requirements.",
            "Weight penalty is minimal compared to risk."
        ],
        resolution_strategy="Optimize foil mesh design to minimize weight.",
        entity_scope="AERO09 exterior composite panels",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AERO09 LSP Specification"
    ),
    DoctrineBlock(
        topic="Composite Panel Fire, Smoke, and Toxicity (FST) Compliance",
        keywords=["composite", "panel", "fire", "smoke", "toxicity", "FST", "test"],
        conclusion_template="Test all interior composite panels for FST compliance per FAR 25.853 and AERO09 requirements.",
        reasoning_framework="""
        1. Prepare test panels per AERO09 and regulatory geometry.
        2. Test for flame propagation, smoke density, and toxicity.
        3. Reference FAR 25.853 and AERO09 FST specification.
        4. Document test results and compliance status.
        5. Maintain traceability to batch and panel.
        6. Rework or reject panels failing FST tests.
        7. Audit FST compliance records regularly.
        """,
        key_factors=[
            "Test method",
            "Panel geometry",
            "Documentation",
            "Traceability",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FAR 25.853",
            "AERO09 FST Specification",
            "ASTM E662"
        ],
        burden_holder="Test Engineer",
        adversary_position="FST testing adds cost and schedule risk.",
        counter_arguments=[
            "FST compliance is mandatory for certification.",
            "Testing ensures passenger safety."
        ],
        resolution_strategy="Schedule FST testing early to avoid delays.",
        entity_scope="AERO09 interior composite panels",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FAR 25.853"
    ),
    DoctrineBlock(
        topic="Composite Panel Paint and Finish Requirements",
        keywords=["composite", "panel", "paint", "finish", "primer", "topcoat"],
        conclusion_template="Apply compatible primer and topcoat per AERO09 paint specification to all exterior composite panels.",
        reasoning_framework="""
        1. Prepare panel surface per paint manufacturer’s instructions.
        2. Apply primer and topcoat using approved methods.
        3. Inspect finish for coverage, adhesion, and defects.
        4. Reference AERO09 paint specification.
        5. Document paint lot, application method, and inspection results.
        6. Rework or reject panels with finish defects.
        7. Maintain traceability to batch and panel.
        """,
        key_factors=[
            "Paint compatibility",
            "Application method",
            "Inspection",
            "Documentation",
            "Traceability"
        ],
        primary_authority=[
            "AERO09 Paint Specification",
            "CMH-17, Section 2.11",
            "ASTM D3359"
        ],
        burden_holder="Paint Technician",
        adversary_position="Paint adds weight and may affect surface properties.",
        counter_arguments=[
            "Paint is required for UV and environmental protection.",
            "Weight can be minimized by controlling film thickness."
        ],
        resolution_strategy="Optimize paint system for minimum weight and maximum durability.",
        entity_scope="AERO09 exterior composite panels",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AERO09 Paint Specification"
    ),
    DoctrineBlock(
        topic="Composite Panel Impact Resistance Testing",
        keywords=["composite", "panel", "impact resistance", "test", "drop weight"],
        conclusion_template="Test composite panels for impact resistance per ASTM D7136; use results to set design allowables for AERO09 structures.",
        reasoning_framework="""
        1. Prepare test panels per AERO09 geometry.
        2. Conduct drop-weight impact tests per ASTM D7136.
        3. Record damage size, depth, and failure mode.
        4. Reference AERO09 test plan and CMH-17.
        5. Document test results and use for allowables development.
        6. Maintain traceability to batch and panel.
        7. Rework or reject panels failing impact resistance criteria.
        """,
        key_factors=[
            "Test method",
            "Panel geometry",
            "Damage assessment",
            "Documentation",
            "Traceability"
        ],
        primary_authority=[
            "ASTM D7136",
            "AERO09 Test Plan",
            "CMH-17, Section 8.4"
        ],
        burden_holder="Test Engineer",
        adversary_position="Lab tests may not represent all in-service impact scenarios.",
        counter_arguments=[
            "Standard tests provide baseline for design.",
            "Supplement with additional tests as needed."
        ],
        resolution_strategy="Expand test matrix for unique AERO09 threats.",
        entity_scope="AERO09 composite panels",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASTM D7136"
    ),
    DoctrineBlock(
        topic="Composite Panel Moisture Absorption and Conditioning",
        keywords=["composite", "panel", "moisture absorption", "conditioning", "test"],
        conclusion_template="Condition composite panels to moisture equilibrium at 70°C/85% RH prior to property testing per CMH-17.",
        reasoning_framework="""
        1. Expose panels to 70°C/85% RH until mass change is <0.01%/day.
        2. Test mechanical properties immediately after conditioning.
        3. Reference CMH-17 and AERO09 test plan.
        4. Document conditioning parameters and test results.
        5. Maintain traceability to batch and panel.
        6. Use data for allowables and design substantiation.
        7. Audit conditioning records regularly.
        """,
        key_factors=[
            "Conditioning environment",
            "Equilibrium criteria",
            "Documentation",
            "Traceability",
            "Testing"
        ],
        primary_authority=[
            "CMH-17, Section 8.3",
            "AERO09 Test Plan",
            "ASTM D5229"
        ],
        burden_holder="Test Engineer",
        adversary_position="In-service moisture uptake may differ from lab conditioning.",
        counter_arguments=[
            "Standard conditioning ensures comparability of data.",
            "Supplement with additional conditioning if required."
        ],
        resolution_strategy="Expand test matrix for unique AERO09 environments as needed.",
        entity_scope="AERO09 composite panels",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="CMH-17, Section 8.3"
    ),
    DoctrineBlock(
        topic="Composite Panel Core-to-Face Adhesion",
        keywords=["composite", "panel", "core-to-face adhesion", "peel test", "honeycomb"],
        conclusion_template="Test core-to-face adhesion per ASTM C297; reject AERO09 sandwich panels failing minimum peel strength.",
        reasoning_framework="""
        1. Prepare sandwich panel specimens per ASTM C297.
        2. Conduct flatwise tensile (peel) tests.
        3. Record failure load and mode.
        4. Reference AERO09 sandwich panel specification.
        5. Document test results and panel traceability.
        6. Rework or reject panels failing minimum adhesion.
        7. Audit test records regularly.
        """,
        key_factors=[
            "Test method",
            "Panel geometry",
            "Failure mode",
            "Documentation",
            "Traceability"
        ],
        primary_authority=[
            "ASTM C297",
            "AERO09 Sandwich Panel Specification",
            "CMH-17, Section 8.5"
        ],
        burden_holder="Test Engineer",
        adversary_position="Peel test may not represent all in-service loads.",
        counter_arguments=[
            "Peel test is standard for core-to-face adhesion.",
            "Supplement with additional tests as needed."
        ],
        resolution_strategy="Expand test matrix for unique AERO09 applications.",
        entity_scope="AERO09 sandwich panels",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASTM C297"
    ),
    DoctrineBlock(
        topic="Composite Panel Core Crush Strength",
        keywords=["composite", "panel", "core crush strength", "honeycomb", "test"],
        conclusion_template="Test honeycomb core crush strength per ASTM C365; use results for AERO09 sandwich panel design allowables.",
        reasoning_framework="""
        1. Prepare core specimens per ASTM C365.
        2. Conduct flatwise compression tests.
        3. Record failure load and mode.
        4. Reference AERO09 sandwich panel specification.
        5. Document test results and core traceability.
        6. Use data for allowables and design substantiation.
        7. Audit test records regularly.
        """,
        key_factors=[
            "Test method",
            "Core geometry",
            "Failure mode",
            "Documentation",
            "Traceability"
        ],
        primary_authority=[
            "ASTM C365",
            "AERO09 Sandwich Panel Specification",
            "CMH-17, Section 8.6"
        ],
        burden_holder="Test Engineer",
        adversary_position="Lab tests may not represent all in-service loads.",
        counter_arguments=[
            "Standard tests provide baseline for design.",
            "Supplement with additional tests as needed."
        ],
        resolution_strategy="Expand test matrix for unique AERO09 applications.",
        entity_scope="AERO09 sandwich panels",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASTM C365"
    ),
    DoctrineBlock(
        topic="Composite Panel Flatwise Tensile Strength",
        keywords=["composite", "panel", "flatwise tensile strength", "honeycomb", "test"],
        conclusion_template="Test flatwise tensile strength of sandwich panels per ASTM C297 for AERO09 allowables development.",
        reasoning_framework="""
        1. Prepare sandwich panel specimens per ASTM C297.
        2. Conduct flatwise tensile tests.
        3. Record failure load and mode.
        4. Reference AERO09 sandwich panel specification.
        5. Document test results and panel traceability.
        6. Use data for allowables and design substantiation.
        7. Audit test records regularly.
        """,
        key_factors=[
            "Test method",
            "Panel geometry",
            "Failure mode",
            "Documentation",
            "Traceability"
        ],
        primary_authority=[
            "ASTM C297",
            "AERO09 Sandwich Panel Specification",
            "CMH-17, Section 8.7"
        ],
        burden_holder="Test Engineer",
        adversary_position="Flatwise tensile test may not represent all in-service loads.",
        counter_arguments=[
            "Standard tests provide baseline for design.",
            "Supplement with additional tests as needed."
        ],
        resolution_strategy="Expand test matrix for unique AERO09 applications.",
        entity_scope="AERO09 sandwich panels",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASTM C297"
    ),
    DoctrineBlock(
        topic="Composite Panel Shear Strength",
        keywords=["composite", "panel", "shear strength", "honeycomb", "test"],
        conclusion_template="Test honeycomb panel shear strength per ASTM C273; use results for AERO09 sandwich panel design allowables.",
        reasoning_framework="""
        1. Prepare panel specimens per ASTM C273.
        2. Conduct shear tests and record failure load and mode.
        3. Reference AERO09 sandwich panel specification.
        4. Document test results and panel traceability.
        5. Use data for allowables and design substantiation.
        6. Audit test records regularly.
        7. Rework or reject panels failing shear strength criteria.
        """,
        key_factors=[
            "Test method",
            "Panel geometry",
            "Failure mode",
            "Documentation",
            "Traceability"
        ],
        primary_authority=[
            "ASTM C273",
            "AERO09 Sandwich Panel Specification",
            "CMH-17, Section 8.8"
        ],
        burden_holder="Test Engineer",
        adversary_position="Shear test may not represent all in-service loads.",
        counter_arguments=[
            "Standard tests provide baseline for design.",
            "Supplement with additional tests as needed."
        ],
        resolution_strategy="Expand test matrix for unique AERO09 applications.",
        entity_scope="AERO09 sandwich panels",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASTM C273"
    ),
    DoctrineBlock(
        topic="Composite Panel Facing Buckling",
        keywords=["composite", "panel", "facing buckling", "honeycomb", "design"],
        conclusion_template="Analyze facing buckling of sandwich panels per CMH-17 and validate with panel-level testing for AERO09 structures.",
        reasoning_framework="""
        1. Calculate critical buckling load using classical sandwich theory.
        2. Validate analysis with panel-level buckling tests.
        3. Reference AERO09 sandwich panel specification and CMH-17.
        4. Document analysis, test results, and panel traceability.
        5. Use data for allowables and design substantiation.
        6. Audit analysis and test records regularly.
        7. Rework or redesign panels failing buckling criteria.
        """,
        key_factors=[
            "Analysis method",
            "Panel geometry",
            "Test validation",
            "Documentation",
            "Traceability"
        ],
        primary_authority=[
            "CMH-17, Section 8.9",
            "AERO09 Sandwich Panel Specification",
            "ASTM D7249"
        ],
        burden_holder="Design Engineer",
        adversary_position="Analysis may not capture all real-world failure modes.",
        counter_arguments=[
            "Panel-level testing validates analysis.",
            "Supplement with additional tests as needed."
        ],
        resolution_strategy="Expand test matrix for unique AERO09 applications.",
        entity_scope="AERO09 sandwich panels",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="CMH-17, Section 8.9"
    ),
    DoctrineBlock(
        topic="Composite Panel Insert Design and Testing",
        keywords=["composite", "panel", "insert", "design", "testing", "honeycomb"],
        conclusion_template="Design and test panel inserts per AERO09 specification; validate pull-out and shear strength with coupon and panel tests.",
        reasoning_framework="""
        1. Select insert type and geometry based on load requirements.
        2. Bond or pot inserts per AERO09 process specification.
        3. Test insert pull-out and shear strength with coupons and panels.
        4. Reference CMH-17 and AERO09 insert specification.
        5. Document design, test results, and panel traceability.
        6. Rework or redesign inserts failing strength criteria.
        7. Audit insert test records regularly.
        """,
        key_factors=[
            "Insert type",
            "Bonding method",
            "Test method",
            "Documentation",
            "Traceability"
        ],
        primary_authority=[
            "AERO09 Insert Specification",
            "CMH-17, Section 8.10",
            "ASTM D7332"
        ],
        burden_holder="Design Engineer",
        adversary_position="Inserts may introduce local stress concentrations.",
        counter_arguments=[
            "Proper design and testing mitigate risk.",
            "Use load-spreading inserts for high-load applications."
        ],
        resolution_strategy="Optimize insert design for load and durability.",
        entity_scope="AERO09 sandwich panels",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AERO09 Insert Specification"
    ),
    DoctrineBlock(
        topic="Composite Panel Potting Material Selection",
        keywords=["composite", "panel", "potting material", "insert", "honeycomb"],
        conclusion_template="Select potting material compatible with core and facing; validate with mechanical and environmental tests per AERO09 specification.",
        reasoning_framework="""
        1. Assess compatibility of potting material with core and facing.
        2. Reference AERO09 potting material specification.
        3. Test potting for mechanical strength and environmental durability.
        4. Document material selection, test results, and panel traceability.
        5. Maintain records of potting material batches and application.
        6. Rework or reject panels with potting defects.
        7. Audit potting records regularly.
        """,
        key_factors=[
            "Material compatibility",
            "Mechanical strength",
            "Environmental durability",
            "Documentation",
            "Traceability"
        ],
        primary_authority=[
            "AERO09 Potting Material Specification",
            "CMH-17, Section 8.11",
            "ASTM D7332"
        ],
        burden_holder="Materials Engineer",
        adversary_position="Potting adds weight and may degrade over time.",
        counter_arguments=[
            "Proper selection and testing ensure durability.",
            "Minimize potting volume to reduce weight."
        ],
        resolution_strategy="Optimize potting design for weight and performance.",
        entity_scope="AERO09 sandwich panels",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AERO09 Potting Material Specification"
    ),
    DoctrineBlock(
        topic="Composite Panel Core Splice Design",
        keywords=["composite", "panel", "core splice", "honeycomb", "design"],
        conclusion_template="Design core splices with staggered joints and compatible adhesive per AERO09 specification; validate with panel tests.",
        reasoning_framework="""
        1. Stagger core splice joints to avoid continuous weak lines.
        2. Use compatible adhesive per AERO09 specification.
        3. Validate splice strength with panel-level tests.
        4. Document design, test results, and panel traceability.
        5. Rework or redesign splices failing strength criteria.
        6. Audit splice records regularly.
        7. Reference CMH-17 and AERO09 sandwich panel specification.
        """,
        key_factors=[
            "Joint location",
            "Adhesive compatibility",
            "Test method",
            "Documentation",
            "Traceability"
        ],
        primary_authority=[
            "AERO09 Sandwich Panel Specification",
            "CMH-17, Section 8.12",
            "ASTM D7332"
        ],
        burden_holder="Design Engineer",
        adversary_position="Core splices may be weak points in the panel.",
        counter_arguments=[
            "Proper design and testing mitigate risk.",
            "Staggered joints and compatible adhesive ensure strength."
        ],
        resolution_strategy="Optimize core splice design for strength and durability.",
        entity_scope="AERO09 sandwich panels",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AERO09 Sandwich Panel Specification"
    ),
    DoctrineBlock(
        topic="Composite Panel Core Venting",
        keywords=["composite", "panel", "core venting", "honeycomb", "altitude"],
        conclusion_template="Provide core venting holes in honeycomb panels to prevent pressure buildup at altitude per AERO09 specification.",
        reasoning_framework="""
        1. Drill or mold vent holes in honeycomb core at specified intervals.
        2. Reference AERO09 core venting specification.
        3. Validate venting effectiveness with altitude chamber tests.
        4. Document venting design, test results, and panel traceability.
        5. Rework or redesign panels with inadequate venting.
        6. Audit venting records regularly.
        7. Maintain compliance with regulatory requirements.
        """,
        key_factors=[
            "Venting hole size and spacing",
            "Altitude test results",
            "Documentation",
            "Traceability",
            "Regulatory compliance"
        ],
        primary_authority=[
            "AERO09 Core Venting Specification",
            "CMH-17, Section 8.13",
            "FAA AC 43.13-1B"
        ],
        burden_holder="Design Engineer",
        adversary_position="Venting holes may reduce panel strength.",
        counter_arguments=[
            "Properly sized and located holes have minimal effect.",
            "Testing validates venting and strength."
        ],
        resolution_strategy="Optimize venting design for strength and pressure relief.",
        entity_scope="AERO09 sandwich panels",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AERO09 Core Venting Specification"
    ),
    DoctrineBlock(
        topic="Composite Panel Core Filler Selection",
        keywords=["composite", "panel", "core filler", "honeycomb", "edge closeout"],
        conclusion_template="Select compatible core filler for edge closeouts and cutouts per AERO09 specification; validate with mechanical and environmental tests.",
        reasoning_framework="""
        1. Select core filler compatible with honeycomb and facing.
        2. Reference AERO09 core filler specification.
        3. Apply and cure filler per manufacturer’s instructions.
        4. Test filled areas for mechanical strength and environmental durability.
        5. Document filler selection, application, and test results.
        6. Rework or reject panels with filler defects.
        7. Audit filler records regularly.
        """,
        key_factors=[
            "Material compatibility",
            "Application method",
            "Mechanical strength",
            "Environmental durability",
            "Documentation"
        ],
        primary_authority=[
            "AERO09 Core Filler Specification",
            "CMH-17, Section 8.14",
            "ASTM D7332"
        ],
        burden_holder="Materials Engineer",
        adversary_position="Core filler adds weight and may degrade over time.",
        counter_arguments=[
            "Proper selection and testing ensure durability.",
            "Minimize filler volume to reduce weight."
        ],
        resolution_strategy="Optimize filler design for weight and performance.",
        entity_scope="AERO09 sandwich panels",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AERO09 Core Filler Specification"
    ),
    DoctrineBlock(
        topic="Composite Panel Core Edge Closeout Design",
        keywords=["composite", "panel", "core edge closeout", "honeycomb", "design"],
        conclusion_template="Design edge closeouts with compatible filler and facing wrap per AERO09 specification; validate with mechanical and environmental tests.",
        reasoning_framework="""
        1. Select compatible filler and wrap facing over core edge.
        2. Reference AERO09 edge closeout specification.
        3. Test closeout for mechanical strength and environmental durability.
        4. Document design, application, and test results.
        5. Rework or redesign closeouts failing tests.
        6. Audit closeout records regularly.
        7. Maintain compliance with regulatory requirements.
        """,
        key_factors=[
            "Filler compatibility",
            "Facing wrap method",
            "Mechanical strength",
            "Environmental durability",
            "Documentation"
        ],
        primary_authority=[
            "AERO09 Edge Closeout Specification",
            "CMH-17, Section 8.15",
            "ASTM D7332"
        ],
        burden_holder="Design Engineer",
        adversary_position="Edge closeouts add weight and complexity.",
        counter_arguments=[
            "Edge closeouts are required for durability and moisture protection.",
            "Optimize design to minimize weight."
        ],
        resolution_strategy="Optimize closeout design for weight and performance.",
        entity_scope="AERO09 sandwich panels",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AERO09 Edge Closeout Specification"
    ),
    DoctrineBlock(
        topic="Composite Panel Core Material Traceability",
        keywords=["composite", "panel", "core material", "traceability", "honeycomb"],
        conclusion_template="Maintain full traceability of core material batch and panel for all AERO09 sandwich structures.",
        reasoning_framework="""
        1. Assign unique batch IDs to all core material.
        2. Record all process steps, inspections, and test results.
        3. Link core material records to panel and finished part.
        4. Store traceability data in AERO09 quality management system.
        5. Reference CMH-17 and AERO09 quality manual.
        6. Audit traceability records regularly.
        7. Reject or quarantine panels with incomplete traceability.
        """,
        key_factors=[
            "Batch ID",
            "Process documentation",
            "Inspection records",
            "Data management",
            "Audit"
        ],
        primary_authority=[
            "AERO09 Quality Manual",
            "CMH-17, Section 2.6",
            "AS9100"
        ],
        burden_holder="Quality Engineer",
        adversary_position="Traceability adds cost and administrative burden.",
        counter_arguments=[
            "Traceability is required for regulatory compliance.",
            "Reduces risk of undetected material or process issues."
        ],
        resolution_strategy="Automate traceability where possible to reduce burden.",
        entity_scope="AERO09 sandwich panels",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="AERO09 Quality Manual"
    ),
    DoctrineBlock(
        topic="Composite Panel Core Material Storage",
        keywords=["composite", "panel", "core material", "storage", "honeycomb"],
        conclusion_template="Store honeycomb core material in clean, dry environment at 18-25°C; inspect for contamination or damage before use.",
        reasoning_framework="""
        1. Store core material in original packaging at 18-25°C and <60% RH.
        2. Inspect for contamination, moisture, or damage prior to use.
        3. Reference AERO09 core material storage specification.
        4. Document storage conditions and inspection results.
        5. Rework or reject core material with defects.
        6. Maintain traceability to batch and panel.
        7. Audit storage records regularly.
        """,
        key_factors=[
            "Storage temperature and humidity",
            "Contamination control",
            "Inspection",
            "Documentation",
            "Traceability"
        ],
        primary_authority=[
            "AERO09 Core Material Storage Specification",
            "CMH-17, Section 2.7",
            "Manufacturer TDS"
        ],
        burden_holder="Material Handler",
        adversary_position="Improper storage may degrade core properties.",
        counter_arguments=[
            "Proper storage ensures material quality.",
            "Inspect all core material prior to use."
        ],
        resolution_strategy="Audit storage conditions regularly.",
        entity_scope="AERO09 sandwich panels",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AERO09 Core Material Storage Specification"
    ),
    DoctrineBlock(
        topic="Composite Panel Core Material Shelf Life",
        keywords=["composite", "panel", "core material", "shelf life", "honeycomb"],
        conclusion_template="Use honeycomb core material within manufacturer’s shelf life; requalify or discard expired material per AERO09 procedures.",
        reasoning_framework="""
        1. Verify core material batch expiration date upon receipt.
        2. Store at recommended temperature and humidity.
        3. Do not use expired core material without requalification testing.
        4. Reference manufacturer’s TDS and AERO09 material control procedures.
        5. Discard or requalify expired material per CMH-17 guidelines.
        6. Maintain traceability to batch and panel.
        7. Audit shelf life records regularly.
        """,
        key_factors=[
            "Shelf life",
            "Storage conditions",
            "Requalification procedures",
            "Documentation",
            "Traceability"
        ],
        primary_authority=[
            "AERO09 Material Control Manual",
            "CMH-17, Section 2.7",
            "Manufacturer TDS"
        ],
        burden_holder="Material Handler",
        adversary_position="Short shelf life increases material waste and cost.",
        counter_arguments=[
            "Strict control ensures panel