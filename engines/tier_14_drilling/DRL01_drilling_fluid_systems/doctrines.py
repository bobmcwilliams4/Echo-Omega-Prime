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
        topic="Water-Based Mud (WBM) Formulation Design",
        keywords=["WBM", "formulation", "water-based mud", "additives", "bentonite", "viscosifier", "fluid loss", "drilling"],
        conclusion_template="A properly designed WBM system should balance rheology, fluid loss, and inhibition according to formation requirements.",
        reasoning_framework="""
1. Identify formation type and drilling objectives.
2. Select base fluid (freshwater, seawater, or brine) based on availability and compatibility.
3. Choose bentonite or polymer viscosifiers for desired rheology.
4. Add fluid loss control agents (e.g., PAC, CMC) to minimize filtrate invasion.
5. Incorporate shale inhibitors (e.g., KCl, glycol) if drilling reactive shales.
6. Adjust pH and alkalinity with lime or caustic soda.
7. Evaluate mud properties (PV, YP, gel strength) and optimize with appropriate additives.
8. Ensure environmental compliance with local regulations.
9. Conduct pilot tests and adjust formulation as drilling progresses.
10. Maintain documentation and QA/QC records.
""",
        key_factors=["Formation mineralogy", "Shale reactivity", "Fluid loss requirements", "Environmental regulations", "Additive compatibility"],
        primary_authority=["API RP 13B-1", "API Spec 13A", "Drilling Fluids Processing Handbook (ASME Shale Shaker Committee)"],
        burden_holder="Mud Engineer",
        adversary_position="Cost-driven reduction of additive concentrations may compromise wellbore stability.",
        counter_arguments=[
            "Insufficient inhibitor or fluid loss control can result in stuck pipe and wellbore collapse.",
            "Optimized additive selection reduces overall cost by preventing non-productive time."
        ],
        resolution_strategy="Justify additive selection with formation data and pilot test results; document cost-benefit analysis.",
        entity_scope="Drilling Fluid Service Companies, Operators",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 4"
    ),
    DoctrineBlock(
        topic="Oil-Based Mud (OBM) and Synthetic-Based Mud (SBM) Systems",
        keywords=["OBM", "SBM", "oil-based mud", "synthetic-based mud", "emulsion", "invert", "diesel", "ester", "base oil"],
        conclusion_template="OBM and SBM systems are preferred for challenging formations, offering superior inhibition, lubricity, and thermal stability.",
        reasoning_framework="""
1. Assess formation sensitivity to water and need for inhibition.
2. Select base oil (diesel, mineral oil, synthetic ester) based on environmental and performance criteria.
3. Formulate invert emulsion with appropriate water-to-oil ratio (typically 70:30 to 90:10).
4. Add primary emulsifiers and secondary emulsifiers to stabilize the system.
5. Incorporate lime for alkalinity and to react with acidic gases.
6. Adjust rheology with organoclays and polymers.
7. Monitor electrical stability, emulsion stability, and HTHP filtration.
8. Ensure compliance with discharge regulations (e.g., North Sea OSPAR, Gulf of Mexico NPDES).
9. Document system performance and adjust as needed.
""",
        key_factors=["Formation reactivity", "Environmental discharge limits", "Lubricity requirements", "Thermal stability", "Cost"],
        primary_authority=["API RP 13B-2", "OSPAR Decision 2000/2", "NPDES General Permit"],
        burden_holder="Drilling Fluid Engineer",
        adversary_position="Water-based muds are less expensive and environmentally preferable.",
        counter_arguments=[
            "OBM/SBM systems reduce stuck pipe and torque in deviated wells.",
            "SBMs offer improved environmental profile over traditional OBMs."
        ],
        resolution_strategy="Select system based on formation risk, environmental compliance, and total cost of ownership.",
        entity_scope="Operators, Environmental Regulators",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 13B-2 Section 5"
    ),
    DoctrineBlock(
        topic="Mud Weight Control and Barite Addition Calculations",
        keywords=["mud weight", "barite", "density", "calculation", "solids", "sag", "well control"],
        conclusion_template="Mud weight is adjusted by calculated barite addition to maintain well control and prevent formation influx.",
        reasoning_framework="""
1. Determine required mud weight (ppg or SG) based on pore pressure and fracture gradient.
2. Calculate current mud density and volume.
3. Use the barite addition formula:
   Pounds of barite per barrel = (42 × (desired MW - current MW)) / (35 - desired MW)
4. Add barite incrementally while circulating and monitoring for sag.
5. Mix thoroughly to prevent localized high-density slugs.
6. Monitor ECD and adjust pump rates as needed.
7. Ensure barite quality meets API Spec 13A.
8. Record additions and update mud inventory.
""",
        key_factors=["Pore pressure", "Fracture gradient", "Barite quality", "Mixing efficiency", "Sag risk"],
        primary_authority=["API Spec 13A", "API RP 13B-1", "Well Control Guidelines (IADC)"],
        burden_holder="Drilling Supervisor",
        adversary_position="Excessive barite addition increases solids content and may cause sag or lost circulation.",
        counter_arguments=[
            "Accurate calculation and gradual addition minimize risks.",
            "Alternative weighting agents (hematite, ilmenite) may be considered for high-density requirements."
        ],
        resolution_strategy="Validate calculations, monitor mud properties, and use sag testing protocols.",
        entity_scope="Drilling Contractors, Mud Engineers",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="API Spec 13A Section 7"
    ),
    DoctrineBlock(
        topic="Mud Rheology: Plastic Viscosity, Yield Point, and Gel Strength",
        keywords=["rheology", "plastic viscosity", "yield point", "gel strength", "flow", "viscometer"],
        conclusion_template="Control of PV, YP, and gel strength is essential for effective hole cleaning and wellbore stability.",
        reasoning_framework="""
1. Measure mud rheology using Fann viscometer at 600/300/6/3 rpm.
2. Calculate Plastic Viscosity (PV = 600 rpm - 300 rpm).
3. Calculate Yield Point (YP = 300 rpm - PV).
4. Assess gel strengths at 10 seconds and 10 minutes.
5. Adjust with viscosifiers (bentonite, polymers) or thinners (lignite, tannins) as needed.
6. Optimize for hole cleaning (higher YP), barite suspension (adequate gel strength), and pumpability (moderate PV).
7. Monitor for excessive gelation, which may cause surge/swab or stuck pipe.
8. Document and trend rheological properties.
""",
        key_factors=["Solids content", "Additive selection", "Temperature", "Hydraulics", "Well profile"],
        primary_authority=["API RP 13B-1", "Drilling Engineering (Neal Adams)"],
        burden_holder="Mud Engineer",
        adversary_position="High YP or gel strength increases ECD and surge pressures.",
        counter_arguments=[
            "Optimized rheology balances cleaning and ECD.",
            "Periodic checks and adjustments prevent operational issues."
        ],
        resolution_strategy="Trend rheology data and adjust formulation proactively.",
        entity_scope="Drilling Operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 6"
    ),
    DoctrineBlock(
        topic="Fluid Loss Control: API Filtrate and HPHT Filtration",
        keywords=["fluid loss", "API filtrate", "HPHT", "filtration", "control", "additives", "loss circulation"],
        conclusion_template="Fluid loss additives are selected and dosed to minimize filtrate invasion as measured by API and HPHT tests.",
        reasoning_framework="""
1. Conduct API fluid loss test (100 psi, 30 min) and HPHT test (500 psi, 250°F).
2. Compare results to program requirements (typically <15 mL for API, <10 mL for HPHT).
3. Select appropriate additives (starch, PAC, CMC, synthetic polymers).
4. Adjust concentrations based on test outcomes.
5. Monitor for formation damage or filter cake buildup.
6. Re-test after each significant mud treatment.
7. Document all test results and adjustments.
""",
        key_factors=["Formation permeability", "Temperature", "Additive compatibility", "Filtrate volume", "Filter cake quality"],
        primary_authority=["API RP 13B-1", "API RP 13B-2", "Drilling Fluids Processing Handbook"],
        burden_holder="Fluid Engineer",
        adversary_position="Excessive fluid loss control may increase solids and impact rheology.",
        counter_arguments=[
            "Proper selection and dosage minimize negative impacts.",
            "Pilot testing ensures optimal performance."
        ],
        resolution_strategy="Balance fluid loss control with rheological requirements and formation compatibility.",
        entity_scope="Mud Laboratories, Field Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 8"
    ),
    DoctrineBlock(
        topic="Shale Inhibition via Potassium Chloride (KCl) Muds",
        keywords=["shale inhibition", "KCl", "potassium chloride", "reactive shale", "dispersion", "swelling"],
        conclusion_template="KCl muds inhibit shale swelling and dispersion by cation exchange and osmotic effects.",
        reasoning_framework="""
1. Identify reactive shale intervals via cuttings analysis and well logs.
2. Prepare KCl solution (2-8% by weight) as base or additive to WBM.
3. Monitor mud salinity and K+ ion concentration.
4. Evaluate shale stability via dispersion and accretion tests.
5. Adjust KCl concentration as drilling progresses.
6. Combine with polymers (e.g., PHPA) for enhanced inhibition.
7. Monitor for salt contamination and adjust treatment accordingly.
8. Ensure environmental discharge compliance.
""",
        key_factors=["Shale mineralogy", "Cation exchange capacity", "K+ concentration", "Environmental discharge limits"],
        primary_authority=["API RP 13B-1", "Drilling Fluids Processing Handbook", "OSPAR"],
        burden_holder="Mud Engineer",
        adversary_position="High KCl concentrations may increase corrosion and environmental risk.",
        counter_arguments=[
            "Optimized KCl dosage minimizes risk while providing inhibition.",
            "Alternative inhibitors (glycol, amines) may be considered."
        ],
        resolution_strategy="Base KCl concentration on shale reactivity and environmental limits.",
        entity_scope="Drilling Operations, Environmental Compliance",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 9"
    ),
    DoctrineBlock(
        topic="Lost Circulation Materials: Bridging and Sealing Formulations",
        keywords=["lost circulation", "LCM", "bridging", "sealing", "formation loss", "pill", "plugging"],
        conclusion_template="LCM selection and application are tailored to loss severity and formation characteristics.",
        reasoning_framework="""
1. Diagnose loss type: seepage, partial, or total.
2. Select bridging material (e.g., sized calcium carbonate, walnut shells, mica) based on loss zone aperture.
3. Formulate LCM pill with appropriate blend and carrier fluid.
4. Pump pill and monitor loss rates.
5. For severe losses, consider cement or high-strength plugs.
6. Document LCM type, concentration, and effectiveness.
7. Adjust future LCM strategy based on results.
""",
        key_factors=["Loss zone aperture", "Formation type", "LCM compatibility", "Severity of loss", "Operational constraints"],
        primary_authority=["API RP 13B-1", "Lost Circulation: Mechanisms and Solutions (Mese, 2017)"],
        burden_holder="Drilling Supervisor",
        adversary_position="Excessive LCM use may damage productive zones.",
        counter_arguments=[
            "Proper sizing and placement minimize formation damage.",
            "Pilot testing and monitoring optimize LCM effectiveness."
        ],
        resolution_strategy="Select LCM based on loss diagnostics and formation compatibility.",
        entity_scope="Drilling Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 10"
    ),
    DoctrineBlock(
        topic="Solids Control Equipment: Shale Shakers, Centrifuges, and Degassers",
        keywords=["solids control", "shale shaker", "centrifuge", "degasser", "desander", "desilter"],
        conclusion_template="Efficient solids control maximizes mud life and minimizes dilution and disposal costs.",
        reasoning_framework="""
1. Select shaker screen size and type for expected cuttings size.
2. Operate shakers at optimal G-force and deck angle.
3. Use desanders and desilters for intermediate particle removal.
4. Deploy centrifuges for ultra-fine solids control.
5. Install degassers to remove entrained gas.
6. Monitor mud properties and solids content.
7. Maintain and inspect equipment regularly.
8. Document performance and adjust as needed.
""",
        key_factors=["Cuttings size distribution", "Mud properties", "Equipment capacity", "Maintenance", "Solids loading"],
        primary_authority=["API RP 13C", "ASME Shale Shaker Handbook"],
        burden_holder="Mud Engineer",
        adversary_position="High capital and operating costs for advanced solids control.",
        counter_arguments=[
            "Reduced dilution and disposal costs offset equipment investment.",
            "Improved wellbore stability and mud performance."
        ],
        resolution_strategy="Optimize equipment selection based on well profile and solids loading.",
        entity_scope="Drilling Contractors, Operators",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 13C Section 3"
    ),
    DoctrineBlock(
        topic="Cement Contamination: Diagnosis and Treatment",
        keywords=["cement contamination", "diagnosis", "treatment", "lime", "calcium", "deflocculation"],
        conclusion_template="Cement contamination is diagnosed by elevated calcium and treated by dilution, deflocculants, and pH adjustment.",
        reasoning_framework="""
1. Identify cement contamination via high calcium, increased viscosity, and pH changes.
2. Confirm with titration and chemical analysis.
3. Dilute contaminated mud with fresh base fluid.
4. Add deflocculants (lignosulfonate, lignite) to reduce viscosity.
5. Adjust pH with caustic soda or lime as needed.
6. Remove excess solids via solids control equipment.
7. Monitor mud properties and repeat treatment if necessary.
8. Document contamination events and treatments.
""",
        key_factors=["Calcium concentration", "Mud pH", "Viscosity", "Solids content", "Additive compatibility"],
        primary_authority=["API RP 13B-1", "Drilling Fluids Processing Handbook"],
        burden_holder="Mud Engineer",
        adversary_position="Excessive dilution increases mud costs and disposal volumes.",
        counter_arguments=[
            "Early diagnosis and targeted treatment minimize dilution needs.",
            "Proper solids control reduces long-term costs."
        ],
        resolution_strategy="Implement rapid diagnosis and staged treatment protocols.",
        entity_scope="Drilling Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 11"
    ),
    DoctrineBlock(
        topic="High-Pressure High-Temperature (HPHT) Drilling Fluid Systems",
        keywords=["HPHT", "high pressure", "high temperature", "thermal stability", "fluid system", "additives"],
        conclusion_template="HPHT fluid systems require thermally stable base fluids, additives, and rigorous QA/QC.",
        reasoning_framework="""
1. Define HPHT conditions (>10,000 psi, >300°F).
2. Select base fluid (synthetic, invert, or high-performance WBM) with proven HPHT stability.
3. Use thermally stable viscosifiers (e.g., xanthan, synthetic polymers).
4. Add fluid loss and shale inhibitors rated for HPHT service.
5. Conduct HPHT filtration and rheology tests at expected downhole conditions.
6. Monitor for barite sag and emulsion stability.
7. Implement strict QA/QC and pilot testing.
8. Document all formulations and test results.
""",
        key_factors=["Temperature rating", "Pressure rating", "Additive stability", "Sag risk", "Emulsion stability"],
        primary_authority=["API RP 13B-1", "API RP 13B-2", "HPHT Drilling Fluids (SPE 92354)"],
        burden_holder="Drilling Fluid Engineer",
        adversary_position="Standard mud systems are less expensive and easier to maintain.",
        counter_arguments=[
            "HPHT conditions require specialized systems to prevent well control incidents.",
            "Failure to use HPHT-rated fluids can result in catastrophic failure."
        ],
        resolution_strategy="Base system selection on downhole conditions and test data.",
        entity_scope="HPHT Drilling Operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 12"
    ),
    DoctrineBlock(
        topic="Completion and Workover Fluids: Clear Brines and Low-Solids Systems",
        keywords=["completion fluid", "workover fluid", "clear brine", "low-solids", "density", "formation damage"],
        conclusion_template="Clear brines and low-solids fluids minimize formation damage during completion and workover operations.",
        reasoning_framework="""
1. Select brine type (NaCl, KCl, CaCl2, ZnBr2, formate) based on required density and compatibility.
2. Ensure fluid is filtered to <2 micron solids.
3. Test for formation compatibility (swelling, precipitation).
4. Monitor fluid density and adjust with base brine or solids as needed.
5. Maintain corrosion inhibitors and oxygen scavengers.
6. Document fluid properties and QA/QC results.
7. Recover and recycle brine where possible.
""",
        key_factors=["Density requirement", "Formation compatibility", "Solids content", "Corrosion risk", "Cost"],
        primary_authority=["API RP 13J", "Completion and Workover Fluids (SPE 16903)"],
        burden_holder="Completion Engineer",
        adversary_position="High-density brines are costly and may cause corrosion.",
        counter_arguments=[
            "Low-solids brines reduce formation damage and enhance productivity.",
            "Corrosion inhibitors mitigate risk."
        ],
        resolution_strategy="Select brine based on formation tests and cost-benefit analysis.",
        entity_scope="Completion Operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 13J Section 4"
    ),
    DoctrineBlock(
        topic="Environmental Regulations for Drilling Fluid Disposal and Discharge",
        keywords=["environmental", "regulation", "disposal", "discharge", "NPDES", "OSPAR", "cuttings", "waste"],
        conclusion_template="Drilling fluid disposal and discharge must comply with local, national, and international regulations.",
        reasoning_framework="""
1. Identify applicable regulations (NPDES, OSPAR, EPA, local agencies).
2. Test mud and cuttings for contaminants (oil, metals, TPH, toxicity).
3. Select disposal method: onshore landfill, injection, thermal desorption, or offshore discharge.
4. Treat fluids to meet discharge limits (e.g., oil on cuttings <1% by weight).
5. Maintain records of waste volumes, test results, and disposal routes.
6. Audit contractors and disposal facilities.
7. Prepare for regulatory inspections and reporting.
""",
        key_factors=["Regulatory jurisdiction", "Contaminant levels", "Disposal method", "Recordkeeping", "Contractor compliance"],
        primary_authority=["NPDES General Permit", "OSPAR Decision 2000/2", "EPA 40 CFR 435"],
        burden_holder="Operator",
        adversary_position="Strict regulations increase operational cost and complexity.",
        counter_arguments=[
            "Non-compliance risks fines and license revocation.",
            "Best practices reduce long-term liability."
        ],
        resolution_strategy="Implement robust waste tracking and contractor management systems.",
        entity_scope="Operators, Waste Contractors",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="EPA 40 CFR 435"
    ),
    DoctrineBlock(
        topic="pH and Alkalinity Management in Water-Based Muds",
        keywords=["pH", "alkalinity", "water-based mud", "buffer", "lime", "caustic soda", "corrosion"],
        conclusion_template="pH and alkalinity are controlled to optimize mud performance and minimize corrosion.",
        reasoning_framework="""
1. Measure pH and alkalinity using standard titration methods.
2. Maintain pH in the range 9.0-10.5 for most WBM systems.
3. Adjust with caustic soda (NaOH) or lime (Ca(OH)2) as needed.
4. Monitor for acid gas influx (CO2, H2S) and adjust alkalinity accordingly.
5. Prevent excessive pH, which may destabilize polymers or increase scaling.
6. Document all treatments and test results.
""",
        key_factors=["Mud composition", "Gas influx", "Additive stability", "Corrosion risk", "Formation compatibility"],
        primary_authority=["API RP 13B-1", "Drilling Fluids Processing Handbook"],
        burden_holder="Mud Engineer",
        adversary_position="High pH may cause polymer degradation or scaling.",
        counter_arguments=[
            "Controlled pH ensures additive performance and corrosion control.",
            "Routine monitoring prevents excursions."
        ],
        resolution_strategy="Base pH adjustments on regular measurements and system requirements.",
        entity_scope="Drilling Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 13"
    ),
    DoctrineBlock(
        topic="Wellbore Stability Analysis and Mud Weight Windows",
        keywords=["wellbore stability", "mud weight window", "collapse", "fracture", "geomechanics", "pore pressure"],
        conclusion_template="Mud weight is maintained within the safe window to prevent wellbore collapse and fracturing.",
        reasoning_framework="""
1. Analyze offset well data for pore pressure and fracture gradient.
2. Model wellbore stability using geomechanical software.
3. Define minimum (collapse) and maximum (fracture) mud weights.
4. Monitor ECD and adjust mud weight as drilling progresses.
5. Document all calculations and update with real-time data.
6. Prepare contingency plans for abnormal pressure or losses.
""",
        key_factors=["Pore pressure", "Fracture gradient", "Formation strength", "ECD", "Well trajectory"],
        primary_authority=["Wellbore Stability (SPE 54309)", "API RP 13B-1"],
        burden_holder="Drilling Engineer",
        adversary_position="Narrow mud weight windows increase operational risk.",
        counter_arguments=[
            "Real-time monitoring and modeling mitigate risk.",
            "Contingency planning ensures rapid response."
        ],
        resolution_strategy="Integrate geomechanical modeling with real-time drilling data.",
        entity_scope="Drilling Operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="SPE 54309"
    ),
    DoctrineBlock(
        topic="Glycol and Amine Shale Inhibitors for Extreme Reactive Formations",
        keywords=["glycol", "amine", "shale inhibitor", "reactive formation", "dispersion", "swelling"],
        conclusion_template="Glycol and amine inhibitors are used to enhance shale stability in highly reactive formations.",
        reasoning_framework="""
1. Identify intervals with extreme shale reactivity.
2. Select glycol (polyethylene glycol) or amine-based inhibitors.
3. Dose according to laboratory compatibility and field performance data.
4. Monitor shale cuttings for dispersion and accretion.
5. Adjust inhibitor concentration as needed.
6. Ensure compatibility with other mud additives.
7. Document inhibitor usage and performance.
""",
        key_factors=["Shale reactivity", "Inhibitor compatibility", "Environmental limits", "Cost", "Performance data"],
        primary_authority=["API RP 13B-1", "Drilling Fluids Processing Handbook"],
        burden_holder="Mud Engineer",
        adversary_position="Inhibitor cost and environmental impact may be prohibitive.",
        counter_arguments=[
            "Enhanced inhibition reduces NPT and stuck pipe risk.",
            "Field trials demonstrate cost-effectiveness."
        ],
        resolution_strategy="Base inhibitor selection on formation reactivity and environmental compliance.",
        entity_scope="Drilling Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 14"
    ),
    DoctrineBlock(
        topic="Barite Sag Prevention in Deviated Wells",
        keywords=["barite sag", "deviated well", "sag test", "rheology", "suspension", "density"],
        conclusion_template="Barite sag is prevented by optimizing rheology and circulation practices, especially in deviated wells.",
        reasoning_framework="""
1. Identify sag-prone intervals (high angle, low annular velocity).
2. Conduct static and dynamic sag tests (e.g., Viscometer Sag Test, Sag Shoe Test).
3. Optimize low-shear rheology with polymers or organoclays.
4. Maintain adequate circulation rates during connections.
5. Monitor density profiles and adjust mud properties as needed.
6. Document sag events and mitigation measures.
""",
        key_factors=["Well deviation", "Annular velocity", "Low-shear rheology", "Barite quality", "Circulation practices"],
        primary_authority=["API RP 13B-1", "Barite Sag in Deviated Wells (SPE 56636)"],
        burden_holder="Mud Engineer",
        adversary_position="Rheology optimization increases additive cost and complexity.",
        counter_arguments=[
            "Sag prevention avoids costly well control events.",
            "Routine sag testing ensures early detection."
        ],
        resolution_strategy="Implement regular sag testing and adjust formulation proactively.",
        entity_scope="Directional Drilling Operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="SPE 56636"
    ),
    DoctrineBlock(
        topic="Emulsion Stability in Oil-Based Muds",
        keywords=["emulsion stability", "oil-based mud", "OBM", "electrical stability", "emulsifier", "invert"],
        conclusion_template="Emulsion stability is maintained by proper emulsifier selection, water/oil ratio, and electrical stability monitoring.",
        reasoning_framework="""
1. Select primary and secondary emulsifiers based on base oil and water phase.
2. Maintain water/oil ratio within recommended limits (typically 70:30 to 90:10).
3. Monitor electrical stability (ES) using standard tests (>400 V for stable OBM).
4. Adjust emulsifier concentration as needed.
5. Monitor for water-wetting, phase separation, or high HTHP filtration.
6. Document all ES readings and treatments.
""",
        key_factors=["Emulsifier type", "Water/oil ratio", "Temperature", "Contaminants", "ES value"],
        primary_authority=["API RP 13B-2", "Drilling Fluids Processing Handbook"],
        burden_holder="Mud Engineer",
        adversary_position="High emulsifier concentrations increase cost and may impact environmental profile.",
        counter_arguments=[
            "Stable emulsion prevents wellbore instability and fluid loss.",
            "Routine ES monitoring optimizes additive usage."
        ],
        resolution_strategy="Optimize emulsifier dosage based on ES trends and mud performance.",
        entity_scope="Drilling Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 13B-2 Section 7"
    ),
    DoctrineBlock(
        topic="Salt Contamination Diagnosis and Treatment",
        keywords=["salt contamination", "NaCl", "diagnosis", "treatment", "deflocculation", "solids"],
        conclusion_template="Salt contamination is diagnosed by increased chloride and treated by dilution and deflocculants.",
        reasoning_framework="""
1. Identify salt contamination via chloride titration and increased mud viscosity.
2. Confirm with mud property trends and solids analysis.
3. Dilute with fresh water or low-salinity base fluid.
4. Add deflocculants (lignosulfonate, lignite) to restore rheology.
5. Monitor for recurring contamination and adjust mud program.
6. Document all treatments and outcomes.
""",
        key_factors=["Chloride concentration", "Mud rheology", "Solids content", "Source of contamination"],
        primary_authority=["API RP 13B-1", "Drilling Fluids Processing Handbook"],
        burden_holder="Mud Engineer",
        adversary_position="Dilution increases mud cost and waste volume.",
        counter_arguments=[
            "Early diagnosis and targeted treatment minimize dilution needs.",
            "Deflocculants restore mud properties efficiently."
        ],
        resolution_strategy="Implement routine chloride monitoring and staged treatment.",
        entity_scope="Drilling Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 15"
    ),
    DoctrineBlock(
        topic="Anhydrite (CaSO4) Contamination Treatment",
        keywords=["anhydrite", "CaSO4", "contamination", "treatment", "calcium", "deflocculant"],
        conclusion_template="Anhydrite contamination is treated by dilution, deflocculants, and pH control.",
        reasoning_framework="""
1. Identify anhydrite contamination via increased calcium and sulfate titration.
2. Dilute with fresh base fluid to reduce calcium concentration.
3. Add deflocculants (lignosulfonate, lignite) to restore rheology.
4. Adjust pH to maintain additive performance.
5. Monitor mud properties and repeat treatment as needed.
6. Document all contamination events and treatments.
""",
        key_factors=["Calcium concentration", "Sulfate concentration", "Mud rheology", "pH", "Source of contamination"],
        primary_authority=["API RP 13B-1", "Drilling Fluids Processing Handbook"],
        burden_holder="Mud Engineer",
        adversary_position="Dilution increases cost and waste volume.",
        counter_arguments=[
            "Targeted treatment minimizes dilution.",
            "Routine monitoring prevents severe contamination."
        ],
        resolution_strategy="Implement staged treatment and routine monitoring.",
        entity_scope="Drilling Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 16"
    ),
    DoctrineBlock(
        topic="Drilling Fluid Hydraulics and Equivalent Circulating Density (ECD)",
        keywords=["hydraulics", "ECD", "equivalent circulating density", "pressure", "annular", "cuttings transport"],
        conclusion_template="Hydraulics and ECD are modeled and monitored to optimize hole cleaning and prevent well control issues.",
        reasoning_framework="""
1. Model annular pressure losses using hydraulics software.
2. Calculate ECD at casing shoe and TD.
3. Adjust pump rates and mud rheology to optimize cuttings transport.
4. Monitor for ECD excursions that may induce losses or fracturing.
5. Document all calculations and real-time data.
6. Update models with actual drilling parameters.
""",
        key_factors=["Annular geometry", "Mud rheology", "Pump rate", "Well depth", "Formation pressure"],
        primary_authority=["Drilling Engineering (Neal Adams)", "API RP 13B-1"],
        burden_holder="Drilling Engineer",
        adversary_position="Hydraulics modeling increases planning time and complexity.",
        counter_arguments=[
            "Optimized hydraulics reduce NPT and well control risk.",
            "Real-time monitoring enables rapid response."
        ],
        resolution_strategy="Integrate hydraulics modeling with real-time data acquisition.",
        entity_scope="Drilling Operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Drilling Engineering (Neal Adams)"
    ),
    DoctrineBlock(
        topic="Synthetic-Based Mud (SBM) Systems and Environmental Advantages",
        keywords=["SBM", "synthetic-based mud", "environment", "ester", "olefin", "discharge", "toxicity"],
        conclusion_template="SBM systems offer improved environmental profile over OBM, with lower toxicity and enhanced biodegradability.",
        reasoning_framework="""
1. Select synthetic base fluid (ester, olefin, paraffin) based on environmental and performance criteria.
2. Formulate invert emulsion with low aromatic content.
3. Test for toxicity, biodegradation, and bioaccumulation.
4. Monitor oil on cuttings and discharge parameters.
5. Compare SBM performance with OBM and WBM alternatives.
6. Document environmental compliance and system performance.
""",
        key_factors=["Base fluid type", "Toxicity", "Biodegradability", "Discharge limits", "Performance"],
        primary_authority=["OSPAR Decision 2000/2", "API RP 13B-2"],
        burden_holder="Operator",
        adversary_position="SBM cost and logistics may outweigh environmental benefits.",
        counter_arguments=[
            "SBM use enables compliance in sensitive areas.",
            "Improved performance reduces NPT and total cost."
        ],
        resolution_strategy="Conduct cost-benefit and environmental impact analysis.",
        entity_scope="Operators, Environmental Regulators",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OSPAR Decision 2000/2"
    ),
    DoctrineBlock(
        topic="Managed Pressure Drilling (MPD) Fluid Systems",
        keywords=["MPD", "managed pressure drilling", "fluid system", "ECD", "well control", "narrow window"],
        conclusion_template="MPD fluid systems are engineered to maintain bottomhole pressure within a narrow window using surface backpressure and fluid properties.",
        reasoning_framework="""
1. Analyze formation pressure and fracture gradient.
2. Select fluid system compatible with MPD equipment (rotating control device, choke manifold).
3. Model ECD and bottomhole pressure under dynamic conditions.
4. Adjust mud weight and rheology to optimize pressure control.
5. Monitor real-time pressure and flow data.
6. Document all system changes and pressure events.
""",
        key_factors=["Pressure window", "MPD equipment", "Fluid compatibility", "Real-time monitoring", "Well control procedures"],
        primary_authority=["API RP 92M", "Managed Pressure Drilling (SPE 11208)"],
        burden_holder="Drilling Engineer",
        adversary_position="MPD increases operational complexity and cost.",
        counter_arguments=[
            "MPD enables safe drilling in challenging pressure environments.",
            "Reduces risk of kicks and losses."
        ],
        resolution_strategy="Base MPD fluid system selection on well risk and cost-benefit analysis.",
        entity_scope="MPD Operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 92M"
    ),
    DoctrineBlock(
        topic="Underbalanced Drilling (UBD) Fluids: Gas, Foam, and Aerated Muds",
        keywords=["UBD", "underbalanced drilling", "gas", "foam", "aerated mud", "well control", "formation damage"],
        conclusion_template="UBD fluids are engineered to maintain bottomhole pressure below formation pressure, minimizing formation damage.",
        reasoning_framework="""
1. Select UBD fluid type (gas, foam, aerated mud) based on formation and well design.
2. Model bottomhole pressure to ensure underbalanced conditions.
3. Monitor for influx and maintain well control equipment (rotating BOP, separator).
4. Optimize fluid rheology and gas/liquid ratio for cuttings transport.
5. Document all UBD events and fluid system changes.
""",
        key_factors=["Formation pressure", "Well control", "Fluid type", "Cuttings transport", "Equipment compatibility"],
        primary_authority=["API RP 92U", "Underbalanced Drilling (SPE 47884)"],
        burden_holder="Drilling Engineer",
        adversary_position="UBD increases well control risk and operational complexity.",
        counter_arguments=[
            "Proper planning and equipment mitigate risk.",
            "UBD minimizes formation damage and enhances productivity."
        ],
        resolution_strategy="Implement robust well control procedures and real-time monitoring.",
        entity_scope="UBD Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 92U"
    ),
    DoctrineBlock(
        topic="API RP 13B-1 Testing Procedures: Standardization and QA/QC",
        keywords=["API RP 13B-1", "testing", "procedure", "QA/QC", "standardization", "mud testing"],
        conclusion_template="Standardized API RP 13B-1 procedures ensure reliable mud property measurement and QA/QC.",
        reasoning_framework="""
1. Follow API RP 13B-1 for all mud property tests (rheology, fluid loss, density, etc.).
2. Calibrate equipment regularly and document calibration records.
3. Train personnel in standardized procedures.
4. Maintain QA/QC logs for all tests and treatments.
5. Audit laboratory and field testing practices.
6. Report deviations and corrective actions.
""",
        key_factors=["Test procedure", "Equipment calibration", "Personnel training", "QA/QC documentation"],
        primary_authority=["API RP 13B-1"],
        burden_holder="Mud Laboratory Supervisor",
        adversary_position="Standardization increases time and resource requirements.",
        counter_arguments=[
            "Standardization ensures data reliability and regulatory compliance.",
            "QA/QC reduces operational risk."
        ],
        resolution_strategy="Implement training and regular audits.",
        entity_scope="Mud Laboratories, Field Operations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1"
    ),
    DoctrineBlock(
        topic="Formate Brines: Potassium and Cesium Formate for Ultra-HPHT",
        keywords=["formate brine", "potassium formate", "cesium formate", "ultra-HPHT", "completion fluid", "density"],
        conclusion_template="Formate brines provide high-density, low-solids fluids for ultra-HPHT drilling and completion.",
        reasoning_framework="""
1. Select potassium or cesium formate based on required density and compatibility.
2. Filter brine to <2 micron solids.
3. Test for formation compatibility and corrosion risk.
4. Monitor fluid density and adjust as needed.
5. Maintain inhibitor levels and document all treatments.
6. Recover and recycle formate brine where possible.
""",
        key_factors=["Density", "Formation compatibility", "Solids content", "Corrosion", "Cost"],
        primary_authority=["API RP 13J", "Formate Brines (SPE 50766)"],
        burden_holder="Completion Engineer",
        adversary_position="Formate brines are expensive and may increase corrosion risk.",
        counter_arguments=[
            "Low-solids formate brines minimize formation damage.",
            "Corrosion inhibitors mitigate risk."
        ],
        resolution_strategy="Base selection on formation tests and cost-benefit analysis.",
        entity_scope="Ultra-HPHT Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SPE 50766"
    ),
    # Additional doctrines for completeness and to reach 40+ entries
    DoctrineBlock(
        topic="Polymer-Based Drilling Fluids: Selection and Application",
        keywords=["polymer", "drilling fluid", "selection", "application", "viscosifier", "inhibitor"],
        conclusion_template="Polymer-based fluids are selected for their inhibitive and rheological properties in challenging formations.",
        reasoning_framework="""
1. Identify formation challenges (shale reactivity, high temperature).
2. Select polymer type (PHPA, PAC, xanthan) based on required properties.
3. Dose according to laboratory and field performance data.
4. Monitor mud rheology and inhibition performance.
5. Adjust polymer concentration as drilling progresses.
6. Document all treatments and performance data.
""",
        key_factors=["Formation type", "Polymer compatibility", "Cost", "Performance data"],
        primary_authority=["API RP 13B-1", "Drilling Fluids Processing Handbook"],
        burden_holder="Mud Engineer",
        adversary_position="Polymer cost and disposal may be prohibitive.",
        counter_arguments=[
            "Enhanced inhibition reduces NPT and stuck pipe risk.",
            "Field trials demonstrate cost-effectiveness."
        ],
        resolution_strategy="Base selection on formation challenges and cost-benefit analysis.",
        entity_scope="Drilling Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 17"
    ),
    DoctrineBlock(
        topic="Calcium-Treated Muds for Anhydrite and Gypsum Formations",
        keywords=["calcium-treated mud", "anhydrite", "gypsum", "formation", "inhibition", "solubility"],
        conclusion_template="Calcium-treated muds are used to inhibit anhydrite and gypsum dissolution and maintain wellbore stability.",
        reasoning_framework="""
1. Identify anhydrite or gypsum intervals via logs and cuttings.
2. Treat mud with calcium chloride or gypsum to saturate with Ca2+.
3. Monitor calcium concentration and adjust as needed.
4. Test for formation compatibility and inhibition performance.
5. Document all treatments and performance data.
""",
        key_factors=["Formation mineralogy", "Calcium concentration", "Solubility", "Inhibition performance"],
        primary_authority=["API RP 13B-1", "Drilling Fluids Processing Handbook"],
        burden_holder="Mud Engineer",
        adversary_position="High calcium may impact additive performance.",
        counter_arguments=[
            "Saturation prevents further dissolution and wellbore enlargement.",
            "Routine monitoring ensures additive compatibility."
        ],
        resolution_strategy="Base treatment on formation mineralogy and compatibility tests.",
        entity_scope="Drilling Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 18"
    ),
    DoctrineBlock(
        topic="Thermally Activated Lost Circulation Materials",
        keywords=["thermally activated", "LCM", "lost circulation", "high temperature", "plugging"],
        conclusion_template="Thermally activated LCMs are deployed in high-temperature zones to seal fractures and prevent losses.",
        reasoning_framework="""
1. Identify high-temperature loss zones.
2. Select thermally activated LCM (e.g., crosslinking polymer, resin).
3. Formulate and pump LCM pill at recommended temperature and concentration.
4. Monitor loss rates and adjust treatment as needed.
5. Document all LCM treatments and outcomes.
""",
        key_factors=["Temperature", "Loss zone size", "LCM type", "Compatibility"],
        primary_authority=["API RP 13B-1", "Lost Circulation: Mechanisms and Solutions (Mese, 2017)"],
        burden_holder="Drilling Supervisor",
        adversary_position="Thermally activated LCMs are expensive and may be difficult to remove.",
        counter_arguments=[
            "Effective in sealing high-temperature fractures.",
            "Pilot testing ensures success."
        ],
        resolution_strategy="Base selection on temperature profile and pilot test results.",
        entity_scope="HPHT Drilling Operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 19"
    ),
    DoctrineBlock(
        topic="Biodegradable Drilling Fluid Additives",
        keywords=["biodegradable", "additive", "drilling fluid", "environment", "discharge"],
        conclusion_template="Biodegradable additives are preferred for environmentally sensitive areas and offshore discharge.",
        reasoning_framework="""
1. Identify environmental sensitivity and discharge requirements.
2. Select biodegradable additives (e.g., starch, polyglycol, esters).
3. Test for performance and compatibility.
4. Monitor discharge parameters and document compliance.
5. Adjust additive selection as regulations evolve.
""",
        key_factors=["Environmental sensitivity", "Additive performance", "Discharge limits", "Cost"],
        primary_authority=["OSPAR Decision 2000/2", "EPA 40 CFR 435"],
        burden_holder="Operator",
        adversary_position="Biodegradable additives may have lower performance or higher cost.",
        counter_arguments=[
            "Improved compliance and reduced liability.",
            "Advances in additive technology close performance gap."
        ],
        resolution_strategy="Balance performance and compliance in additive selection.",
        entity_scope="Offshore Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OSPAR Decision 2000/2"
    ),
    DoctrineBlock(
        topic="Dual-Gradient Drilling Fluid Systems",
        keywords=["dual-gradient", "drilling fluid", "deepwater", "pressure management", "MPD"],
        conclusion_template="Dual-gradient systems enable safe drilling in deepwater by managing riser and downhole pressures independently.",
        reasoning_framework="""
1. Analyze deepwater well profile and pressure regime.
2. Select dual-gradient system (e.g., seawater riser, mud below BOP).
3. Model pressure gradients and ECD.
4. Monitor real-time pressure and adjust fluid system as needed.
5. Document all system changes and pressure events.
""",
        key_factors=["Water depth", "Pressure regime", "System compatibility", "Real-time monitoring"],
        primary_authority=["API RP 92M", "Deepwater Well Control (SPE 87187)"],
        burden_holder="Drilling Engineer",
        adversary_position="Dual-gradient systems increase complexity and cost.",
        counter_arguments=[
            "Enable drilling of wells otherwise not feasible.",
            "Reduce risk of riser unloading and well control events."
        ],
        resolution_strategy="Base system selection on well risk and operational feasibility.",
        entity_scope="Deepwater Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE 87187"
    ),
    DoctrineBlock(
        topic="Micronized Weighting Agents for High-Density Muds",
        keywords=["micronized", "weighting agent", "high-density", "mud", "barite", "sag"],
        conclusion_template="Micronized weighting agents improve suspension and reduce sag in high-density muds.",
        reasoning_framework="""
1. Select micronized barite or hematite for high-density applications.
2. Formulate mud to maintain suspension and minimize sag.
3. Monitor rheology and density profiles.
4. Adjust weighting agent concentration as needed.
5. Document all treatments and performance data.
""",
        key_factors=["Density requirement", "Sag risk", "Rheology", "Cost"],
        primary_authority=["API Spec 13A", "Barite Sag in Deviated Wells (SPE 56636)"],
        burden_holder="Mud Engineer",
        adversary_position="Micronized agents are more expensive than standard barite.",
        counter_arguments=[
            "Improved suspension reduces well control risk.",
            "Lower dilution and maintenance costs."
        ],
        resolution_strategy="Base selection on sag risk and cost-benefit analysis.",
        entity_scope="HPHT and Deviated Wells",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 56636"
    ),
    DoctrineBlock(
        topic="Nano-Enhanced Drilling Fluids",
        keywords=["nano", "nanoparticle", "drilling fluid", "rheology", "fluid loss", "wellbore strengthening"],
        conclusion_template="Nano-enhanced fluids offer improved rheology, fluid loss, and wellbore strengthening.",
        reasoning_framework="""
1. Select nanoparticle type (silica, clay, graphene) based on desired property enhancement.
2. Dose according to laboratory and field performance data.
3. Monitor mud properties and wellbore stability.
4. Adjust nanoparticle concentration as drilling progresses.
5. Document all treatments and performance data.
""",
        key_factors=["Nanoparticle type", "Performance enhancement", "Cost", "Compatibility"],
        primary_authority=["Nano-Enhanced Drilling Fluids (SPE 169003)"],
        burden_holder="Mud Engineer",
        adversary_position="Nano-additives are expensive and may pose environmental risks.",
        counter_arguments=[
            "Enhanced performance reduces NPT and wellbore instability.",
            "Ongoing research addresses environmental concerns."
        ],
        resolution_strategy="Base selection on performance data and regulatory guidance.",
        entity_scope="Challenging Formations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 169003"
    ),
    DoctrineBlock(
        topic="Drilling Fluid Lubricants for Extended Reach Wells",
        keywords=["lubricant", "drilling fluid", "extended reach", "torque", "drag", "OBM", "WBM"],
        conclusion_template="Lubricants are added to reduce torque and drag in extended reach and horizontal wells.",
        reasoning_framework="""
1. Identify torque and drag challenges via modeling and field data.
2. Select lubricant type (synthetic, ester, polyglycol) compatible with mud system.
3. Dose according to performance data and environmental limits.
4. Monitor torque, drag, and mud properties.
5. Document all treatments and performance data.
""",
        key_factors=["Well profile", "Lubricant compatibility", "Environmental limits", "Cost"],
        primary_authority=["Drilling Fluids Processing Handbook", "Extended Reach Drilling (SPE 87188)"],
        burden_holder="Drilling Engineer",
        adversary_position="Lubricants may impact mud properties or environmental compliance.",
        counter_arguments=[
            "Proper selection and dosing minimize negative impacts.",
            "Improved performance reduces NPT."
        ],
        resolution_strategy="Base selection on torque/drag modeling and compliance requirements.",
        entity_scope="Extended Reach Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SPE 87188"
    ),
    DoctrineBlock(
        topic="Filtration Control in Depleted and Fractured Formations",
        keywords=["filtration control", "depleted formation", "fractured formation", "fluid loss", "bridging"],
        conclusion_template="Filtration control is critical in depleted and fractured formations to prevent losses and maintain wellbore stability.",
        reasoning_framework="""
1. Identify depleted or fractured intervals via logs and drilling data.
2. Select bridging and fluid loss additives (calcium carbonate, polymers).
3. Formulate and dose based on loss severity and formation size.
4. Monitor fluid loss and adjust treatment as needed.
5. Document all treatments and outcomes.
""",
        key_factors=["Formation type", "Loss severity", "Additive compatibility", "Cost"],
        primary_authority=["API RP 13B-1", "Lost Circulation: Mechanisms and Solutions (Mese, 2017)"],
        burden_holder="Mud Engineer",
        adversary_position="Excessive bridging may damage productive zones.",
        counter_arguments=[
            "Proper sizing and placement minimize formation damage.",
            "Pilot testing ensures effectiveness."
        ],
        resolution_strategy="Base selection on formation diagnostics and pilot tests.",
        entity_scope="Depleted and Fractured Formations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 20"
    ),
    DoctrineBlock(
        topic="Dispersants and Thinners in Water-Based Muds",
        keywords=["dispersant", "thinner", "water-based mud", "rheology", "solids control"],
        conclusion_template="Dispersants and thinners are used to control rheology and prevent flocculation in WBM.",
        reasoning_framework="""
1. Monitor mud rheology and solids content.
2. Select dispersant or thinner (lignosulfonate, tannin, polyphosphate) based on system compatibility.
3. Dose according to laboratory and field performance data.
4. Monitor for over-treatment and adjust as needed.
5. Document all treatments and outcomes.
""",
        key_factors=["Mud composition", "Solids content", "Additive compatibility", "Cost"],
        primary_authority=["API RP 13B-1", "Drilling Fluids Processing Handbook"],
        burden_holder="Mud Engineer",
        adversary_position="Over-treatment may destabilize mud and increase fluid loss.",
        counter_arguments=[
            "Routine monitoring prevents over-treatment.",
            "Optimized dosing maintains mud performance."
        ],
        resolution_strategy="Base dosing on regular rheology checks and compatibility tests.",
        entity_scope="Drilling Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 21"
    ),
    DoctrineBlock(
        topic="Drilling Fluid QA/QC and Traceability",
        keywords=["QA/QC", "traceability", "drilling fluid", "additive", "inventory", "compliance"],
        conclusion_template="QA/QC and traceability systems ensure additive quality, regulatory compliance, and operational efficiency.",
        reasoning_framework="""
1. Implement additive tracking from supplier to wellsite.
2. Maintain batch records and certificates of analysis.
3. Conduct QA/QC tests on all additives and base fluids.
4. Document all mud treatments and inventory movements.
5. Audit traceability system regularly.
""",
        key_factors=["Additive quality", "Recordkeeping", "Regulatory compliance", "Supplier management"],
        primary_authority=["API RP 13B-1", "ISO 9001"],
        burden_holder="Mud Laboratory Supervisor",
        adversary_position="Traceability systems increase administrative burden.",
        counter_arguments=[
            "Improved quality reduces operational risk.",
            "Regulatory compliance avoids penalties."
        ],
        resolution_strategy="Automate traceability and integrate with QA/QC systems.",
        entity_scope="Mud Laboratories, Field Operations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ISO 9001"
    ),
    DoctrineBlock(
        topic="Drilling Fluid Temperature Management",
        keywords=["temperature management", "drilling fluid", "thermal stability", "cooling", "HPHT"],
        conclusion_template="Temperature management ensures additive stability and mud performance in HPHT wells.",
        reasoning_framework="""
1. Monitor downhole and surface mud temperatures.
2. Select additives rated for expected temperature range.
3. Implement cooling systems as needed (mud coolers, heat exchangers).
4. Monitor mud properties for thermal degradation.
5. Document all temperature management measures.
""",
        key_factors=["Downhole temperature", "Additive stability", "Cooling system", "Cost"],
        primary_authority=["API RP 13B-1", "HPHT Drilling Fluids (SPE 92354)"],
        burden_holder="Mud Engineer",
        adversary_position="Cooling systems increase cost and complexity.",
        counter_arguments=[
            "Additive stability is critical for well control.",
            "Proper management prevents mud degradation."
        ],
        resolution_strategy="Base temperature management on well profile and additive requirements.",
        entity_scope="HPHT Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="SPE 92354"
    ),
    DoctrineBlock(
        topic="Drilling Fluid Corrosion Control",
        keywords=["corrosion control", "drilling fluid", "pH", "oxygen scavenger", "inhibitor"],
        conclusion_template="Corrosion control is achieved by pH management, oxygen scavengers, and corrosion inhibitors.",
        reasoning_framework="""
1. Monitor pH and alkalinity regularly.
2. Add oxygen scavengers (sodium sulfite, hydrazine) as needed.
3. Select corrosion inhibitors compatible with mud system.
4. Monitor for signs of corrosion (iron content, visual inspection).
5. Document all treatments and outcomes.
""",
        key_factors=["Mud pH", "Oxygen content", "Additive compatibility", "Cost"],
        primary_authority=["API RP 13B-1", "Drilling Fluids Processing Handbook"],
        burden_holder="Mud Engineer",
        adversary_position="Inhibitor cost and compatibility issues.",
        counter_arguments=[
            "Corrosion control prevents equipment failure.",
            "Routine monitoring optimizes dosing."
        ],
        resolution_strategy="Base inhibitor selection on mud composition and corrosion risk.",
        entity_scope="Drilling Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 22"
    ),
    DoctrineBlock(
        topic="Drilling Fluid Defoamer Selection and Application",
        keywords=["defoamer", "drilling fluid", "foam", "gas", "application"],
        conclusion_template="Defoamers are selected and dosed to control foam in mud systems containing gas or air.",
        reasoning_framework="""
1. Monitor mud for foam generation, especially in gas-cut or aerated systems.
2. Select defoamer type (silicone, glycol, alcohol) compatible with mud system.
3. Dose according to laboratory and field performance data.
4. Monitor for over-treatment and adjust as needed.
5. Document all treatments and outcomes.
""",
        key_factors=["Foam severity", "Defoamer compatibility", "Cost", "Performance data"],
        primary_authority=["API RP 13B-1", "Drilling Fluids Processing Handbook"],
        burden_holder="Mud Engineer",
        adversary_position="Over-treatment may impact mud properties.",
        counter_arguments=[
            "Routine monitoring prevents over-treatment.",
            "Optimized dosing maintains mud performance."
        ],
        resolution_strategy="Base dosing on foam severity and compatibility tests.",
        entity_scope="Drilling Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 23"
    ),
    DoctrineBlock(
        topic="Drilling Fluid Microbial Control",
        keywords=["microbial control", "drilling fluid", "biocide", "bacteria", "souring"],
        conclusion_template="Biocides are used to control microbial growth and prevent mud souring and corrosion.",
        reasoning_framework="""
1. Monitor mud for microbial activity (sulfate-reducing bacteria, acid-producing bacteria).
2. Select biocide type (glutaraldehyde, THPS) compatible with mud system.
3. Dose according to laboratory and field performance data.
4. Monitor for re-growth and adjust treatment as needed.
5. Document all treatments and outcomes.
""",
        key_factors=["Microbial activity", "Biocide compatibility", "Cost", "Performance data"],
        primary_authority=["API RP 13B-1", "Drilling Fluids Processing Handbook"],
        burden_holder="Mud Engineer",
        adversary_position="Biocide use may impact environmental compliance.",
        counter_arguments=[
            "Proper selection and dosing minimize environmental risk.",
            "Routine monitoring ensures effectiveness."
        ],
        resolution_strategy="Base biocide selection on microbial activity and compliance requirements.",
        entity_scope="Drilling Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 24"
    ),
    DoctrineBlock(
        topic="Drilling Fluid Inventory Management",
        keywords=["inventory management", "drilling fluid", "additive", "logistics", "cost"],
        conclusion_template="Effective inventory management ensures timely supply and cost control of drilling fluid additives.",
        reasoning_framework="""
1. Forecast additive requirements based on well plan and offset data.
2. Maintain inventory records and reorder points.
3. Audit inventory regularly and reconcile with usage.
4. Document all receipts, transfers, and usage.
5. Integrate inventory management with QA/QC and traceability systems.
""",
        key_factors=["Forecast accuracy", "Recordkeeping", "Supplier reliability", "Cost"],
        primary_authority=["API RP 13B-1", "ISO 9001"],
        burden_holder="Mud Engineer",
        adversary_position="Inventory management increases administrative burden.",
        counter_arguments=[
            "Prevents stockouts and operational delays.",
            "Improves cost control and regulatory compliance."
        ],
        resolution_strategy="Automate inventory management and integrate with QA/QC systems.",
        entity_scope="Mud Laboratories, Field Operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ISO 9001"
    ),
    DoctrineBlock(
        topic="Drilling Fluid Waste Minimization and Recycling",
        keywords=["waste minimization", "recycling", "drilling fluid", "environment", "cost"],
        conclusion_template="Waste minimization and recycling reduce environmental impact and disposal costs.",
        reasoning_framework="""
1. Identify waste streams and recycling opportunities.
2. Implement solids control and fluid recovery systems.
3. Monitor waste volumes and recycling rates.
4. Document all waste minimization and recycling activities.
5. Audit performance and adjust practices as needed.
""",
        key_factors=["Waste volume", "Recycling technology", "Cost", "Regulatory compliance"],
        primary_authority=["EPA 40 CFR 435", "OSPAR Decision 2000/2"],
        burden_holder="Operator",
        adversary_position="Recycling systems increase capital and operating costs.",
        counter_arguments=[
            "Reduced disposal costs and environmental liability.",
            "Improved regulatory compliance."
        ],
        resolution_strategy="Base recycling investment on waste volume and cost-benefit analysis.",
        entity_scope="Operators, Waste Contractors",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EPA 40 CFR 435"
    ),
    DoctrineBlock(
        topic="Drilling Fluid Data Management and Reporting",
        keywords=["data management", "reporting", "drilling fluid", "compliance", "QA/QC"],
        conclusion_template="Robust data management and reporting ensure regulatory compliance and operational efficiency.",
        reasoning_framework="""
1. Implement electronic data capture for all mud properties and treatments.
2. Maintain secure and auditable records.
3. Generate reports for regulatory agencies and internal review.
4. Audit data management system regularly.
5. Integrate with QA/QC and traceability systems.
""",
        key_factors=["Data integrity", "Recordkeeping", "Regulatory compliance", "System integration"],
        primary_authority=["API RP 13B-1", "ISO 9001"],
        burden_holder="Mud Laboratory Supervisor",
        adversary_position="Data management systems increase administrative burden.",
        counter_arguments=[
            "Improved compliance and operational efficiency.",
            "Automated reporting reduces manual workload."
        ],
        resolution_strategy="Automate data management and integrate with QA/QC systems.",
        entity_scope="Mud Laboratories, Field Operations",
        confidence=0.97,
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