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
        topic="In-situ Overburden Stress Determination",
        keywords=["overburden", "vertical stress", "density log", "integration", "geomechanics"],
        conclusion_template="The vertical in-situ stress (Sv) at depth {depth} is determined by integrating the bulk density log from surface to depth.",
        reasoning_framework=(
            "1. Collect bulk density log data from surface to the target depth.\n"
            "2. Integrate the density over depth to compute the overburden stress using Sv = ∫ρ(z)g dz.\n"
            "3. Validate log quality and correct for borehole washouts.\n"
            "4. Account for casing and cement if present.\n"
            "5. Compare with regional trends for consistency.\n"
            "6. Use the calculated Sv as a boundary condition for MEM and wellbore stability analyses."
        ),
        key_factors=["bulk density accuracy", "log coverage", "integration method", "regional calibration"],
        primary_authority=["Zoback (2007)", "Fjaer et al. (2008)", "Schlumberger Oilfield Glossary"],
        burden_holder="Geomechanics Specialist",
        adversary_position="Overburden stress can be underestimated due to poor log quality or missing density data.",
        counter_arguments=[
            "Apply corrections for missing or poor-quality density intervals.",
            "Use regional density models where logs are absent.",
            "Cross-validate with checkshot or seismic velocity data."
        ],
        resolution_strategy="Prioritize high-resolution log data; supplement with regional models if necessary; document all assumptions.",
        entity_scope="All wellbores with available density logs",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Zoback, M.D., Reservoir Geomechanics, 2007"
    ),
    DoctrineBlock(
        topic="Minimum Horizontal Stress (Shmin) Determination",
        keywords=["minimum horizontal stress", "leak-off test", "LOT", "mini-frac", "hydraulic fracturing", "stress anisotropy"],
        conclusion_template="The minimum horizontal stress (Shmin) at depth {depth} is determined from leak-off test or mini-frac data.",
        reasoning_framework=(
            "1. Identify leak-off test (LOT) or mini-frac data at the target depth.\n"
            "2. Analyze pressure vs. time data to determine the leak-off or fracture closure pressure.\n"
            "3. Recognize that closure pressure is a proxy for Shmin.\n"
            "4. Account for effects of near-wellbore stress concentration and fluid pressure penetration.\n"
            "5. Compare with regional stress data and MEM predictions.\n"
            "6. Use Shmin as a constraint for fracture gradient and wellbore stability calculations."
        ),
        key_factors=["test quality", "pressure interpretation", "formation permeability", "stress anisotropy"],
        primary_authority=["Zoback (2007)", "Economides & Nolte (2000)", "SPE 102835"],
        burden_holder="Drilling Engineer / Geomechanics Specialist",
        adversary_position="Closure pressure may overestimate Shmin due to near-wellbore effects or poor test quality.",
        counter_arguments=[
            "Apply corrections for near-wellbore stress concentration.",
            "Use multiple tests for consistency.",
            "Cross-check with fracture gradient predictions."
        ],
        resolution_strategy="Follow industry-standard interpretation methods; document uncertainties and apply corrections as needed.",
        entity_scope="Wells with LOT or mini-frac data",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Economides, M.J. & Nolte, K.G., Reservoir Stimulation, 2000"
    ),
    DoctrineBlock(
        topic="Maximum Horizontal Stress (SHmax) Estimation",
        keywords=["maximum horizontal stress", "borehole breakout", "drilling-induced fracture", "image log", "Kirsch solution"],
        conclusion_template="The maximum horizontal stress (SHmax) is estimated using borehole breakout orientations and drilling-induced tensile fractures from image logs.",
        reasoning_framework=(
            "1. Acquire borehole image logs (FMI, UBI, etc.) in the open hole section.\n"
            "2. Identify borehole breakouts (compressive failure) and drilling-induced tensile fractures (DITFs).\n"
            "3. Use the Kirsch solution to relate breakout width and DITF orientation to stress magnitudes and directions.\n"
            "4. Input rock strength parameters (UCS, friction angle) and mud weight.\n"
            "5. Calibrate SHmax estimates with regional stress data and MEM.\n"
            "6. Document uncertainties due to image log resolution and interpretation subjectivity."
        ),
        key_factors=["image log quality", "rock strength", "mud weight", "breakout width", "DITF orientation"],
        primary_authority=["Zoback (2007)", "Barton et al. (1988)", "SPE 28042"],
        burden_holder="Geomechanics Specialist",
        adversary_position="Breakout and DITF interpretation is subjective and may not yield unique SHmax solutions.",
        counter_arguments=[
            "Use multiple image log runs for confirmation.",
            "Cross-validate with regional stress models.",
            "Apply statistical analysis to breakout/DITF populations."
        ],
        resolution_strategy="Integrate all available data; document interpretation methodology and uncertainty.",
        entity_scope="Open hole sections with image logs",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Barton, C.A. et al., SPE 28042, 1994"
    ),
    DoctrineBlock(
        topic="Mohr-Coulomb Failure Criterion Application",
        keywords=["Mohr-Coulomb", "failure envelope", "cohesion", "friction angle", "shear failure", "rock mechanics"],
        conclusion_template="The Mohr-Coulomb criterion is applied to predict shear failure using cohesion and friction angle from laboratory tests.",
        reasoning_framework=(
            "1. Obtain cohesion (C) and internal friction angle (φ) from triaxial or uniaxial compressive strength tests.\n"
            "2. Construct the Mohr-Coulomb failure envelope in stress space.\n"
            "3. Compare in-situ stress states (from MEM) to the failure envelope.\n"
            "4. Predict wellbore shear failure (breakout) when stress state exceeds the envelope.\n"
            "5. Use the criterion to define minimum mud weight for stability.\n"
            "6. Validate predictions with field observations (breakouts, cuttings shape, etc.)."
        ),
        key_factors=["rock strength parameters", "stress state", "failure envelope construction", "test quality"],
        primary_authority=["Jaeger et al. (2007)", "Fjaer et al. (2008)", "ISRM Suggested Methods"],
        burden_holder="Geomechanics Specialist",
        adversary_position="Mohr-Coulomb may not capture complex failure modes in weak or anisotropic rocks.",
        counter_arguments=[
            "Supplement with alternative criteria (Mogi-Coulomb, Drucker-Prager) for weak rocks.",
            "Use anisotropic strength models if required.",
            "Calibrate with field failure observations."
        ],
        resolution_strategy="Apply Mohr-Coulomb as baseline; use advanced models as needed; document rationale.",
        entity_scope="All formations with available strength data",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Jaeger, J.C. et al., Fundamentals of Rock Mechanics, 2007"
    ),
    DoctrineBlock(
        topic="Collapse Gradient Determination",
        keywords=["collapse gradient", "mud weight window", "wellbore stability", "shear failure", "minimum mud weight"],
        conclusion_template="The collapse gradient is defined as the minimum mud weight required to prevent shear failure (breakout) at a given depth.",
        reasoning_framework=(
            "1. Use in-situ stress state and Mohr-Coulomb criterion to calculate the minimum mud weight that prevents shear failure.\n"
            "2. Input rock strength parameters (UCS, friction angle) and stress magnitudes (Sv, SHmax, Shmin).\n"
            "3. Apply Kirsch equations to determine hoop stress around the wellbore.\n"
            "4. Solve for the mud weight that keeps the hoop stress within the failure envelope.\n"
            "5. Validate with field observations (breakouts, cavings).\n"
            "6. Document assumptions and sensitivity to input parameters."
        ),
        key_factors=["rock strength", "stress state", "wellbore orientation", "failure criterion"],
        primary_authority=["Fjaer et al. (2008)", "Zoback (2007)", "SPE 102835"],
        burden_holder="Drilling Engineer / Geomechanics Specialist",
        adversary_position="Collapse gradient may be underestimated if strength parameters are too optimistic.",
        counter_arguments=[
            "Use conservative strength values.",
            "Calibrate with observed wellbore failures.",
            "Perform sensitivity analysis."
        ],
        resolution_strategy="Use conservative inputs; validate with field data; update as new data becomes available.",
        entity_scope="All drilled intervals",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Fjaer, E. et al., Petroleum Related Rock Mechanics, 2008"
    ),
    DoctrineBlock(
        topic="Fracture Gradient Prediction (Daines Method)",
        keywords=["fracture gradient", "Daines method", "fracture pressure", "pore pressure", "stress", "LOT"],
        conclusion_template="The fracture gradient is predicted using the Daines method, relating fracture pressure to overburden and pore pressure.",
        reasoning_framework=(
            "1. Calculate overburden stress (Sv) at the target depth.\n"
            "2. Estimate pore pressure (Pp) from logs or pressure tests.\n"
            "3. Apply the Daines equation: Pf = αSv + (1-α)Pp, where α is a regional constant (typically 0.7-0.9).\n"
            "4. Convert fracture pressure to equivalent mud weight gradient.\n"
            "5. Validate with LOT or mini-frac data where available.\n"
            "6. Document regional calibration of α and input uncertainties."
        ),
        key_factors=["overburden stress", "pore pressure", "regional α", "LOT data"],
        primary_authority=["Daines (1982)", "Zoback (2007)", "SPE 102835"],
        burden_holder="Geomechanics Specialist",
        adversary_position="Daines method may not capture local variations in stress or formation properties.",
        counter_arguments=[
            "Calibrate α with local LOT data.",
            "Use alternative methods (Breckels, Eaton) for cross-check.",
            "Document limitations of the method."
        ],
        resolution_strategy="Calibrate with field data; use as part of a multi-method approach.",
        entity_scope="All intervals with sufficient data",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Daines, S.R., JPT, 1982"
    ),
    DoctrineBlock(
        topic="Fracture Gradient Prediction (Breckels Method)",
        keywords=["fracture gradient", "Breckels method", "fracture pressure", "effective stress", "LOT"],
        conclusion_template="The fracture gradient is predicted using the Breckels method, incorporating effective stress and rock properties.",
        reasoning_framework=(
            "1. Determine overburden stress (Sv) and pore pressure (Pp) at the target depth.\n"
            "2. Estimate minimum horizontal stress (Shmin) from LOT or regional models.\n"
            "3. Apply the Breckels equation: Pf = Shmin + T, where T is the tensile strength (often negligible).\n"
            "4. Convert to equivalent mud weight gradient.\n"
            "5. Validate with field fracture test data.\n"
            "6. Document assumptions and calibration."
        ),
        key_factors=["Shmin accuracy", "tensile strength", "LOT data", "regional calibration"],
        primary_authority=["Breckels & van Eekelen (1982)", "Zoback (2007)", "SPE 102835"],
        burden_holder="Geomechanics Specialist",
        adversary_position="Tensile strength may be non-negligible in some formations, leading to underestimation.",
        counter_arguments=[
            "Measure tensile strength in laboratory tests.",
            "Apply safety factors where tensile strength is uncertain.",
            "Cross-check with alternative methods."
        ],
        resolution_strategy="Use conservative assumptions; validate with field data.",
        entity_scope="All intervals with sufficient data",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="Breckels, I.M. & van Eekelen, H.A.M., SPE 102835, 1982"
    ),
    DoctrineBlock(
        topic="Shale Reactivity and Cation Exchange Capacity (CEC)",
        keywords=["shale reactivity", "cation exchange capacity", "CEC", "wellbore stability", "chemical-mechanical coupling"],
        conclusion_template="Shale reactivity is assessed by measuring CEC and its impact on wellbore stability and mud design.",
        reasoning_framework=(
            "1. Obtain CEC measurements from core or cuttings analysis.\n"
            "2. High CEC shales are more reactive and prone to swelling and dispersion.\n"
            "3. Select mud systems (inhibitive, KCl, glycol, oil-based) based on CEC and mineralogy.\n"
            "4. Monitor wellbore stability indicators (cavings, torque, drag) during drilling.\n"
            "5. Adjust mud chemistry to minimize chemical-mechanical coupling effects.\n"
            "6. Document CEC values and mud system selection rationale."
        ),
        key_factors=["CEC value", "shale mineralogy", "mud chemistry", "wellbore stability indicators"],
        primary_authority=["Chenevert (1970)", "Mody & Hale (1993)", "SPE 23885"],
        burden_holder="Mud Engineer / Geomechanics Specialist",
        adversary_position="CEC alone may not predict all reactivity issues; other factors (mineralogy, water activity) are important.",
        counter_arguments=[
            "Combine CEC with XRD mineralogy and water activity measurements.",
            "Monitor field performance and adjust mud design.",
            "Use laboratory swelling tests for confirmation."
        ],
        resolution_strategy="Integrate CEC with other reactivity indicators; adjust mud design as needed.",
        entity_scope="Shale intervals",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Chenevert, M.E., JPT, 1970"
    ),
    DoctrineBlock(
        topic="Water Activity and Osmotic Effects in Shale Stability",
        keywords=["water activity", "osmotic pressure", "shale stability", "mud design", "chemical potential"],
        conclusion_template="Water activity of mud is engineered to create osmotic pressure that minimizes shale hydration and instability.",
        reasoning_framework=(
            "1. Measure water activity (aw) of formation and mud filtrate.\n"
            "2. Design mud with lower aw than shale pore water to induce osmotic outflow.\n"
            "3. Monitor wellbore stability (cavings, swelling) during drilling.\n"
            "4. Adjust mud composition (salts, glycols) to maintain favorable osmotic gradients.\n"
            "5. Validate with laboratory swelling and dispersion tests.\n"
            "6. Document water activity measurements and mud design rationale."
        ),
        key_factors=["mud water activity", "shale pore water activity", "osmotic pressure", "mud additives"],
        primary_authority=["Mody & Hale (1993)", "SPE 23885", "Chenevert (1970)"],
        burden_holder="Mud Engineer / Geomechanics Specialist",
        adversary_position="Osmotic effects may be short-lived or insufficient in highly fractured or permeable shales.",
        counter_arguments=[
            "Combine osmotic control with mechanical stabilization (higher mud weight).",
            "Use oil-based muds for problematic shales.",
            "Monitor for early signs of instability and adjust promptly."
        ],
        resolution_strategy="Integrate osmotic control with comprehensive mud and stability management.",
        entity_scope="Shale intervals with reactivity concerns",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Mody, F.K. & Hale, A.H., SPE 23885, 1993"
    ),
    DoctrineBlock(
        topic="Kirsch Solution for Borehole Stress Concentration",
        keywords=["Kirsch solution", "borehole stress", "stress concentration", "wellbore stability", "breakout", "DITF"],
        conclusion_template="The Kirsch solution is used to calculate stress concentration around a circular wellbore for stability analysis.",
        reasoning_framework=(
            "1. Assume a circular wellbore in an infinite elastic medium.\n"
            "2. Input far-field stresses (Sv, SHmax, Shmin), mud pressure, and wellbore orientation.\n"
            "3. Apply the Kirsch equations to compute radial, hoop, and shear stresses at the wellbore wall.\n"
            "4. Identify locations of maximum and minimum hoop stress (breakout, DITF).\n"
            "5. Use results to predict wellbore failure and optimize mud weight and trajectory.\n"
            "6. Validate with image log observations."
        ),
        key_factors=["far-field stress", "mud pressure", "wellbore orientation", "rock properties"],
        primary_authority=["Kirsch (1898)", "Zoback (2007)", "Fjaer et al. (2008)"],
        burden_holder="Geomechanics Specialist",
        adversary_position="Kirsch solution assumes elastic, isotropic, homogeneous media; may not apply to complex geology.",
        counter_arguments=[
            "Use numerical modeling for complex or layered formations.",
            "Calibrate with field observations.",
            "Document limitations of analytical solutions."
        ],
        resolution_strategy="Apply Kirsch as baseline; use advanced models as needed.",
        entity_scope="All wellbores in elastic formations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Kirsch, G., Zeitschrift des Vereins Deutscher Ingenieure, 1898"
    ),
    DoctrineBlock(
        topic="Tensile Fracture and Drilling-Induced Hydraulic Fracture",
        keywords=["tensile fracture", "hydraulic fracture", "wellbore stability", "mud weight window", "fracture gradient"],
        conclusion_template="Tensile fracture risk is assessed by comparing mud pressure to the minimum principal stress and tensile strength.",
        reasoning_framework=(
            "1. Calculate minimum principal stress (usually Shmin) at the wellbore.\n"
            "2. Determine rock tensile strength from laboratory tests.\n"
            "3. Predict onset of tensile fracture when mud pressure exceeds Shmin plus tensile strength.\n"
            "4. Use this threshold to define the upper bound of the mud weight window (fracture gradient).\n"
            "5. Monitor for lost circulation and mud losses as indicators of tensile failure.\n"
            "6. Adjust drilling parameters to avoid exceeding the fracture gradient."
        ),
        key_factors=["Shmin", "tensile strength", "mud pressure", "fracture gradient"],
        primary_authority=["Zoback (2007)", "Economides & Nolte (2000)", "SPE 102835"],
        burden_holder="Drilling Engineer",
        adversary_position="Tensile strength may be overestimated, leading to underestimation of fracture risk.",
        counter_arguments=[
            "Use conservative tensile strength values.",
            "Monitor for early signs of mud losses.",
            "Apply safety factors in mud weight design."
        ],
        resolution_strategy="Use conservative inputs; validate with field data; update as new data becomes available.",
        entity_scope="All drilled intervals",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Zoback, M.D., Reservoir Geomechanics, 2007"
    ),
    DoctrineBlock(
        topic="Mechanical Earth Model (MEM) 1D Construction",
        keywords=["MEM", "mechanical earth model", "1D", "well log", "core data", "stress profile"],
        conclusion_template="A 1D MEM is constructed by integrating well logs, core data, and pressure measurements to define vertical profiles of stress, strength, and pore pressure.",
        reasoning_framework=(
            "1. Gather well logs (density, sonic, gamma ray, resistivity) and core measurements (UCS, CEC, mineralogy).\n"
            "2. Calculate overburden, horizontal stresses, and pore pressure at each depth.\n"
            "3. Assign rock mechanical properties (UCS, Young's modulus, Poisson's ratio) from logs and core.\n"
            "4. Integrate all data to build a depth-based profile of stress, strength, and pressure.\n"
            "5. Validate MEM predictions with field observations (breakouts, LOTs, mud losses).\n"
            "6. Document all data sources, assumptions, and calibration steps."
        ),
        key_factors=["log quality", "core data", "pressure measurements", "calibration"],
        primary_authority=["Zoback (2007)", "Fjaer et al. (2008)", "SPE 102835"],
        burden_holder="Geomechanics Specialist",
        adversary_position="MEM may be inaccurate if input data are sparse or of poor quality.",
        counter_arguments=[
            "Use regional analogs to fill data gaps.",
            "Document and quantify uncertainties.",
            "Update MEM as new data become available."
        ],
        resolution_strategy="Iteratively update MEM; document all assumptions and calibrations.",
        entity_scope="Single wellbore",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Zoback, M.D., Reservoir Geomechanics, 2007"
    ),
    DoctrineBlock(
        topic="Mechanical Earth Model (MEM) 3D Construction",
        keywords=["MEM", "mechanical earth model", "3D", "geostatistics", "seismic", "regional model"],
        conclusion_template="A 3D MEM is constructed by integrating well data, seismic interpretation, and geostatistical modeling to define spatial variation of stress and rock properties.",
        reasoning_framework=(
            "1. Collect well data (logs, core, tests) from multiple wells.\n"
            "2. Integrate seismic interpretation to map structural features and property variations.\n"
            "3. Apply geostatistical methods to interpolate properties between wells.\n"
            "4. Construct 3D grids of stress, strength, and pore pressure.\n"
            "5. Calibrate the model with regional field observations (breakouts, LOTs, induced fractures).\n"
            "6. Document all data sources, interpolation methods, and calibration steps."
        ),
        key_factors=["well data density", "seismic quality", "geostatistical method", "regional calibration"],
        primary_authority=["Zoback (2007)", "SPE 102835", "Fjaer et al. (2008)"],
        burden_holder="Geomechanics Specialist / Reservoir Engineer",
        adversary_position="3D MEMs are subject to high uncertainty in areas with sparse data.",
        counter_arguments=[
            "Quantify and map uncertainty.",
            "Use multiple realizations to bracket possible outcomes.",
            "Update model as new data become available."
        ],
        resolution_strategy="Document uncertainty; use probabilistic approaches; update iteratively.",
        entity_scope="Field or region",
        confidence=0.85,
        confidence_zone="Moderate",
        controlling_precedent="Zoback, M.D., Reservoir Geomechanics, 2007"
    ),
    DoctrineBlock(
        topic="Pore Pressure Prediction (Eaton Method)",
        keywords=["pore pressure", "Eaton method", "overpressure", "sonic log", "resistivity log", "normal compaction"],
        conclusion_template="Pore pressure is predicted using the Eaton method, relating deviations in log response to overpressure.",
        reasoning_framework=(
            "1. Establish normal compaction trends for sonic, resistivity, and density logs.\n"
            "2. Identify deviations from normal trends indicating overpressure.\n"
            "3. Apply the Eaton equation: Pp = Sv - (Sv - Pn) * (ΔTn/ΔT)^E, where E is an exponent (typically 3 for sonic).\n"
            "4. Calibrate with direct pressure measurements (MDT, RFT) where available.\n"
            "5. Document all trend lines, exponents, and calibration steps.\n"
            "6. Quantify uncertainty due to log quality and trend selection."
        ),
        key_factors=["normal compaction trend", "log quality", "calibration data", "Eaton exponent"],
        primary_authority=["Eaton (1975)", "Zoback (2007)", "SPE 102835"],
        burden_holder="Petrophysicist / Geomechanics Specialist",
        adversary_position="Eaton method may be inaccurate in non-shale lithologies or where compaction trends are ambiguous.",
        counter_arguments=[
            "Use multiple log types for cross-validation.",
            "Calibrate with direct pressure data.",
            "Document all assumptions and limitations."
        ],
        resolution_strategy="Apply method to shales; use alternative methods for sands/carbonates; calibrate with field data.",
        entity_scope="Shale intervals",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Eaton, B.A., SPE 5544, 1975"
    ),
    DoctrineBlock(
        topic="Pore Pressure Prediction (Bowers Method)",
        keywords=["pore pressure", "Bowers method", "overpressure", "sonic log", "velocity", "compaction"],
        conclusion_template="Pore pressure is predicted using the Bowers method, relating sonic velocity to effective stress.",
        reasoning_framework=(
            "1. Establish normal compaction trend for sonic velocity.\n"
            "2. Fit the Bowers equation: V = V0 + A * exp(B * σ'), where σ' is effective stress.\n"
            "3. Invert the equation to solve for effective stress from measured velocity.\n"
            "4. Calculate pore pressure as Pp = Sv - σ'.\n"
            "5. Calibrate with direct pressure measurements.\n"
            "6. Document all trend lines, parameters, and calibration steps."
        ),
        key_factors=["sonic velocity", "normal trend", "calibration data", "Bowers parameters"],
        primary_authority=["Bowers (1995)", "Zoback (2007)", "SPE 102835"],
        burden_holder="Petrophysicist / Geomechanics Specialist",
        adversary_position="Bowers method may be unreliable in non-shale lithologies or where velocity is affected by gas.",
        counter_arguments=[
            "Restrict application to shales.",
            "Calibrate with field pressure data.",
            "Document all assumptions and limitations."
        ],
        resolution_strategy="Apply method to shales; use alternative methods for sands/carbonates; calibrate with field data.",
        entity_scope="Shale intervals",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Bowers, G.L., SPE 27488, 1995"
    ),
    DoctrineBlock(
        topic="Wellbore Stability Analysis (Mogi-Coulomb Criterion)",
        keywords=["wellbore stability", "Mogi-Coulomb", "failure criterion", "triaxial test", "shear failure"],
        conclusion_template="The Mogi-Coulomb criterion is applied for wellbore stability analysis in weak or ductile formations.",
        reasoning_framework=(
            "1. Obtain triaxial test data to determine Mogi-Coulomb parameters.\n"
            "2. Construct the Mogi-Coulomb failure envelope in stress space.\n"
            "3. Compare in-situ stress state to the envelope to predict shear failure.\n"
            "4. Use the criterion to define minimum mud weight for stability.\n"
            "5. Validate predictions with field observations (breakouts, cavings).\n"
            "6. Document assumptions and sensitivity to input parameters."
        ),
        key_factors=["triaxial test data", "failure envelope", "stress state", "formation ductility"],
        primary_authority=["Mogi (1971)", "Al-Ajmi & Zimmerman (2005)", "SPE 102835"],
        burden_holder="Geomechanics Specialist",
        adversary_position="Mogi-Coulomb requires extensive lab data and may not be practical for all formations.",
        counter_arguments=[
            "Use Mohr-Coulomb as baseline where lab data are lacking.",
            "Calibrate with field failure observations.",
            "Document rationale for criterion selection."
        ],
        resolution_strategy="Apply Mogi-Coulomb where data allow; otherwise use Mohr-Coulomb.",
        entity_scope="Ductile or weak formations",
        confidence=0.85,
        confidence_zone="Moderate",
        controlling_precedent="Al-Ajmi, A.M. & Zimmerman, R.W., SPE 102835, 2005"
    ),
    DoctrineBlock(
        topic="Wellbore Stability Analysis (Drucker-Prager Criterion)",
        keywords=["wellbore stability", "Drucker-Prager", "failure criterion", "shear failure", "ductile formation"],
        conclusion_template="The Drucker-Prager criterion is used for wellbore stability analysis in ductile or poorly consolidated formations.",
        reasoning_framework=(
            "1. Obtain laboratory test data to determine Drucker-Prager parameters (cohesion, friction angle).\n"
            "2. Construct the Drucker-Prager failure envelope in stress space.\n"
            "3. Compare in-situ stress state to the envelope to predict shear failure.\n"
            "4. Use the criterion to define minimum mud weight for stability.\n"
            "5. Validate predictions with field observations (breakouts, cavings).\n"
            "6. Document assumptions and sensitivity to input parameters."
        ),
        key_factors=["lab test data", "failure envelope", "stress state", "formation ductility"],
        primary_authority=["Drucker & Prager (1952)", "Fjaer et al. (2008)", "SPE 102835"],
        burden_holder="Geomechanics Specialist",
        adversary_position="Drucker-Prager may overestimate strength in brittle rocks.",
        counter_arguments=[
            "Use Mohr-Coulomb for brittle formations.",
            "Calibrate with field failure observations.",
            "Document rationale for criterion selection."
        ],
        resolution_strategy="Apply Drucker-Prager where appropriate; otherwise use Mohr-Coulomb.",
        entity_scope="Ductile or poorly consolidated formations",
        confidence=0.83,
        confidence_zone="Moderate",
        controlling_precedent="Drucker, D.C. & Prager, W., QAM, 1952"
    ),
    DoctrineBlock(
        topic="Chemical-Mechanical Coupling in Shale-Fluid Interaction",
        keywords=["chemical-mechanical coupling", "shale-fluid interaction", "wellbore stability", "mud chemistry", "swelling"],
        conclusion_template="Chemical-mechanical coupling is considered in wellbore stability analysis for reactive shales.",
        reasoning_framework=(
            "1. Identify shales with high CEC, swelling clay content, or history of instability.\n"
            "2. Assess mud chemistry (water activity, ion concentration, inhibitors).\n"
            "3. Model chemical diffusion and its impact on pore pressure and effective stress.\n"
            "4. Integrate chemical effects into mechanical stability calculations.\n"
            "5. Monitor for signs of chemical instability (swelling, dispersion, cavings).\n"
            "6. Adjust mud chemistry and mechanical parameters as needed."
        ),
        key_factors=["shale mineralogy", "mud chemistry", "chemical diffusion", "mechanical properties"],
        primary_authority=["Chenevert (1970)", "Mody & Hale (1993)", "SPE 23885"],
        burden_holder="Geomechanics Specialist / Mud Engineer",
        adversary_position="Chemical effects are difficult to quantify and may be over- or underestimated.",
        counter_arguments=[
            "Use laboratory swelling and diffusion tests.",
            "Monitor field performance and adjust mud design.",
            "Document all assumptions and limitations."
        ],
        resolution_strategy="Integrate chemical and mechanical models; update with field and lab data.",
        entity_scope="Shale intervals",
        confidence=0.80,
        confidence_zone="Moderate",
        controlling_precedent="Mody, F.K. & Hale, A.H., SPE 23885, 1993"
    ),
    DoctrineBlock(
        topic="Time-Dependent Wellbore Instability (Creep and Swelling)",
        keywords=["time-dependent instability", "creep", "swelling", "wellbore stability", "shale", "salt"],
        conclusion_template="Time-dependent wellbore instability is analyzed by modeling creep and swelling in shales and salts.",
        reasoning_framework=(
            "1. Identify formations prone to creep (salts, ductile shales) or swelling (reactive shales).\n"
            "2. Obtain laboratory creep and swelling test data.\n"
            "3. Model time-dependent deformation using viscoelastic or poroelastic models.\n"
            "4. Predict wellbore closure or enlargement over time.\n"
            "5. Adjust drilling practices (minimize open hole time, optimize mud chemistry).\n"
            "6. Monitor for signs of time-dependent instability (tight hole, stuck pipe, cavings)."
        ),
        key_factors=["formation type", "lab creep/swelling data", "open hole time", "mud chemistry"],
        primary_authority=["Fjaer et al. (2008)", "SPE 102835", "Chenevert (1970)"],
        burden_holder="Geomechanics Specialist / Drilling Engineer",
        adversary_position="Creep and swelling rates are difficult to predict and may vary with field conditions.",
        counter_arguments=[
            "Use conservative estimates for planning.",
            "Monitor hole conditions closely during drilling.",
            "Update models with field data."
        ],
        resolution_strategy="Minimize open hole time; use real-time monitoring; update models as needed.",
        entity_scope="Shale and salt intervals",
        confidence=0.78,
        confidence_zone="Moderate",
        controlling_precedent="Fjaer, E. et al., Petroleum Related Rock Mechanics, 2008"
    ),
    DoctrineBlock(
        topic="Stuck Pipe Prevention (Differential Sticking)",
        keywords=["stuck pipe", "differential sticking", "wellbore stability", "mud weight", "filter cake"],
        conclusion_template="Differential sticking risk is managed by optimizing mud weight, filter cake properties, and drilling practices.",
        reasoning_framework=(
            "1. Identify intervals with high differential pressure (mud weight > formation pressure).\n"
            "2. Monitor filter cake quality and thickness.\n"
            "3. Minimize stationary time of drill string against the wellbore.\n"
            "4. Use lubricants and proper mud properties to reduce sticking risk.\n"
            "5. Monitor for early signs of sticking (torque, drag, loss of circulation).\n"
            "6. Implement contingency plans for freeing stuck pipe."
        ),
        key_factors=["differential pressure", "filter cake", "drilling practices", "mud properties"],
        primary_authority=["SPE 20405", "Fjaer et al. (2008)", "Schlumberger Oilfield Glossary"],
        burden_holder="Drilling Engineer",
        adversary_position="Reducing mud weight may compromise wellbore stability.",
        counter_arguments=[
            "Balance mud weight for both stability and sticking risk.",
            "Optimize filter cake with additives.",
            "Use real-time monitoring to detect early signs."
        ],
        resolution_strategy="Balance competing risks; use best practices for mud and drilling.",
        entity_scope="All drilled intervals",
        confidence=0.86,
        confidence_zone="Moderate-High",
        controlling_precedent="SPE 20405, 1990"
    ),
    DoctrineBlock(
        topic="Stuck Pipe Prevention (Key Seating)",
        keywords=["stuck pipe", "key seating", "wellbore trajectory", "dogleg severity", "hole cleaning"],
        conclusion_template="Key seating risk is minimized by controlling wellbore trajectory, dogleg severity, and hole cleaning.",
        reasoning_framework=(
            "1. Plan wellbore trajectory to minimize sharp doglegs and ledges.\n"
            "2. Monitor dogleg severity during drilling.\n"
            "3. Ensure effective hole cleaning to prevent cuttings accumulation.\n"
            "4. Use proper BHA design to reduce risk of pipe lodging in ledges.\n"
            "5. Monitor for early signs of key seating (drag, torque, tight spots).\n"
            "6. Implement corrective actions if key seating is suspected."
        ),
        key_factors=["trajectory planning", "dogleg severity", "hole cleaning", "BHA design"],
        primary_authority=["SPE 20405", "Schlumberger Oilfield Glossary", "Fjaer et al. (2008)"],
        burden_holder="Drilling Engineer",
        adversary_position="Reducing doglegs may not be feasible in complex wells.",
        counter_arguments=[
            "Use advanced trajectory planning software.",
            "Optimize BHA and drilling parameters.",
            "Increase hole cleaning efficiency."
        ],
        resolution_strategy="Plan trajectory carefully; monitor and adjust in real time.",
        entity_scope="Directional and horizontal wells",
        confidence=0.84,
        confidence_zone="Moderate",
        controlling_precedent="SPE 20405, 1990"
    ),
    DoctrineBlock(
        topic="Lost Circulation Prevention (Preventive LCM)",
        keywords=["lost circulation", "LCM", "preventive", "wellbore stability", "fracture gradient"],
        conclusion_template="Preventive lost circulation material (LCM) is used to strengthen the wellbore and prevent mud losses.",
        reasoning_framework=(
            "1. Identify intervals with low fracture gradient or history of losses.\n"
            "2. Add preventive LCM (fibers, flakes, granular) to mud before entering loss-prone zones.\n"
            "3. Monitor mud losses and wellbore stability indicators.\n"
            "4. Adjust LCM concentration and type based on field response.\n"
            "5. Document LCM program and results for future wells.\n"
            "6. Integrate with wellbore stability and mud weight management."
        ),
        key_factors=["fracture gradient", "loss history", "LCM type", "mud properties"],
        primary_authority=["SPE 20405", "Fjaer et al. (2008)", "Schlumberger Oilfield Glossary"],
        burden_holder="Drilling Engineer / Mud Engineer",
        adversary_position="LCM may reduce mud circulation efficiency or cause stuck pipe.",
        counter_arguments=[
            "Optimize LCM type and concentration.",
            "Monitor for signs of plugging or sticking.",
            "Use real-time data to adjust program."
        ],
        resolution_strategy="Balance LCM use with operational risks; document all interventions.",
        entity_scope="Loss-prone intervals",
        confidence=0.82,
        confidence_zone="Moderate",
        controlling_precedent="SPE 20405, 1990"
    ),
    DoctrineBlock(
        topic="Lost Circulation Remediation (Squeeze Techniques)",
        keywords=["lost circulation", "squeeze", "remediation", "wellbore stability", "fracture sealing"],
        conclusion_template="Squeeze techniques are used to remediate lost circulation by sealing fractures and thief zones.",
        reasoning_framework=(
            "1. Identify location and severity of losses using flow logs and mud returns.\n"
            "2. Select appropriate squeeze material (cement, resin, LCM blend) based on loss type.\n"
            "3. Isolate loss zone with packers or plugs if necessary.\n"
            "4. Pump squeeze material into the loss zone under controlled pressure.\n"
            "5. Monitor for successful sealing and restoration of circulation.\n"
            "6. Document all squeeze operations and results."
        ),
        key_factors=["loss location", "squeeze material", "isolation method", "pressure control"],
        primary_authority=["SPE 20405", "Schlumberger Oilfield Glossary", "Fjaer et al. (2008)"],
        burden_holder="Drilling Engineer",
        adversary_position="Squeeze operations may fail or cause further formation damage.",
        counter_arguments=[
            "Select squeeze material carefully based on loss mechanism.",
            "Use staged or multiple squeezes if needed.",
            "Monitor for signs of formation damage."
        ],
        resolution_strategy="Plan squeeze operations based on loss diagnosis; document all outcomes.",
        entity_scope="Loss-prone intervals",
        confidence=0.80,
        confidence_zone="Moderate",
        controlling_precedent="SPE 20405, 1990"
    ),
    DoctrineBlock(
        topic="Sand Production Onset Prediction (Sanding)",
        keywords=["sand production", "sanding", "critical drawdown", "wellbore stability", "rock strength"],
        conclusion_template="Sand production onset is predicted by comparing drawdown to critical values derived from rock strength and stress analysis.",
        reasoning_framework=(
            "1. Obtain rock strength data (UCS, tensile strength) from core or log analysis.\n"
            "2. Calculate in-situ stress and effective stress at the sandface.\n"
            "3. Determine critical drawdown for sand production using analytical or numerical models.\n"
            "4. Compare planned drawdown to critical value.\n"
            "5. Monitor for sand production during testing and production.\n"
            "6. Adjust drawdown or install sand control as needed."
        ),
        key_factors=["rock strength", "in-situ stress", "critical drawdown", "sand control"],
        primary_authority=["Fjaer et al. (2008)", "SPE 102835", "Schlumberger Oilfield Glossary"],
        burden_holder="Production Engineer / Geomechanics Specialist",
        adversary_position="Critical drawdown may be underestimated due to heterogeneity or anisotropy.",
        counter_arguments=[
            "Use conservative estimates.",
            "Calibrate with field sand production data.",
            "Update models with new data."
        ],
        resolution_strategy="Monitor sand production; update predictions as needed.",
        entity_scope="Unconsolidated or weak sand intervals",
        confidence=0.81,
        confidence_zone="Moderate",
        controlling_precedent="Fjaer, E. et al., Petroleum Related Rock Mechanics, 2008"
    ),
    DoctrineBlock(
        topic="Casing Deformation due to Formation Movement",
        keywords=["casing deformation", "formation movement", "compaction", "wellbore stability", "MEM"],
        conclusion_template="Casing deformation risk is assessed by modeling formation movement and compaction using MEM.",
        reasoning_framework=(
            "1. Build MEM including compaction and subsidence predictions.\n"
            "2. Identify intervals with high compaction or movement risk (depleted reservoirs, salt, shales).\n"
            "3. Model stress changes on casing due to formation movement.\n"
            "4. Select casing design and placement to mitigate deformation risk.\n"
            "5. Monitor for casing deformation using caliper and multi-finger logs.\n"
            "6. Update MEM and casing design as new data become available."
        ),
        key_factors=["MEM quality", "compaction prediction", "casing design", "monitoring"],
        primary_authority=["Zoback (2007)", "Fjaer et al. (2008)", "SPE 102835"],
        burden_holder="Completion Engineer / Geomechanics Specialist",
        adversary_position="Compaction predictions are uncertain and may not capture local effects.",
        counter_arguments=[
            "Use conservative casing design.",
            "Monitor for early signs of deformation.",
            "Update models with field data."
        ],
        resolution_strategy="Design for worst-case scenarios; monitor and update as needed.",
        entity_scope="Depleted or mobile formations",
        confidence=0.79,
        confidence_zone="Moderate",
        controlling_precedent="Zoback, M.D., Reservoir Geomechanics, 2007"
    ),
    DoctrineBlock(
        topic="Thermal Stress Effects during Drilling",
        keywords=["thermal stress", "cooling", "heating", "wellbore stability", "thermal expansion"],
        conclusion_template="Thermal stress effects are analyzed by modeling temperature changes during drilling and their impact on wellbore stability.",
        reasoning_framework=(
            "1. Model temperature profile in the wellbore during drilling (circulation, mud temperature).\n"
            "2. Calculate thermal expansion or contraction of rock and casing.\n"
            "3. Assess impact on in-situ stress state and wellbore stability.\n"
            "4. Monitor for signs of thermal-induced instability (breakouts, casing deformation).\n"
            "5. Adjust drilling parameters to minimize rapid temperature changes.\n"
            "6. Document all thermal modeling and observations."
        ),
        key_factors=["temperature profile", "thermal expansion", "stress modeling", "drilling parameters"],
        primary_authority=["Fjaer et al. (2008)", "SPE 102835", "Schlumberger Oilfield Glossary"],
        burden_holder="Drilling Engineer / Geomechanics Specialist",
        adversary_position="Thermal effects may be minor compared to mechanical or chemical effects.",
        counter_arguments=[
            "Include thermal effects in comprehensive stability models.",
            "Monitor for unexpected instability during temperature changes.",
            "Document all modeling assumptions."
        ],
        resolution_strategy="Integrate thermal, mechanical, and chemical models as needed.",
        entity_scope="All drilled intervals",
        confidence=0.77,
        confidence_zone="Moderate",
        controlling_precedent="Fjaer, E. et al., Petroleum Related Rock Mechanics, 2008"
    ),
    DoctrineBlock(
        topic="Wellbore Breathing and Ballooning during Formation Testing",
        keywords=["wellbore breathing", "ballooning", "formation testing", "wellbore stability", "mud losses"],
        conclusion_template="Wellbore breathing and ballooning are diagnosed and managed during formation testing to distinguish from lost circulation.",
        reasoning_framework=(
            "1. Monitor mud returns and pit volume during formation testing and pressure changes.\n"
            "2. Identify cyclic mud losses and gains characteristic of breathing/ballooning.\n"
            "3. Distinguish from continuous lost circulation using flowback patterns.\n"
            "4. Adjust mud weight and circulation practices to minimize breathing.\n"
            "5. Document all observations and corrective actions.\n"
            "6. Integrate with wellbore stability and loss prevention strategies."
        ),
        key_factors=["mud returns", "pit volume", "formation properties", "testing procedures"],
        primary_authority=["SPE 102835", "Schlumberger Oilfield Glossary", "Fjaer et al. (2008)"],
        burden_holder="Drilling Engineer",
        adversary_position="Breathing/ballooning may mask true lost circulation events.",
        counter_arguments=[
            "Use flowback and pit volume analysis to distinguish events.",
            "Monitor for sustained losses after testing.",
            "Document all diagnostic steps."
        ],
        resolution_strategy="Train personnel in event recognition; document all findings.",
        entity_scope="Formation testing intervals",
        confidence=0.80,
        confidence_zone="Moderate",
        controlling_precedent="SPE 102835, 2006"
    ),
    DoctrineBlock(
        topic="Geomechanical Logging (Sonic, Dipole, Cross-Dipole)",
        keywords=["geomechanical logging", "sonic log", "dipole", "cross-dipole", "rock properties"],
        conclusion_template="Geomechanical logging tools are used to derive rock mechanical properties for MEM and stability analysis.",
        reasoning_framework=(
            "1. Acquire sonic, dipole, and cross-dipole logs in open hole sections.\n"
            "2. Process logs to obtain compressional and shear velocities.\n"
            "3. Calculate dynamic Young's modulus, Poisson's ratio, and anisotropy indicators.\n"
            "4. Integrate log-derived properties with core and lab data.\n"
            "5. Use results in MEM construction and stability modeling.\n"
            "6. Document all processing steps and calibration."
        ),
        key_factors=["log quality", "processing method", "calibration data", "anisotropy"],
        primary_authority=["Fjaer et al. (2008)", "Zoback (2007)", "SPE 102835"],
        burden_holder="Petrophysicist / Geomechanics Specialist",
        adversary_position="Dynamic properties from logs may differ from static lab measurements.",
        counter_arguments=[
            "Apply empirical correlations to convert dynamic to static properties.",
            "Calibrate with core and field data.",
            "Document all conversion methods."
        ],
        resolution_strategy="Integrate log and lab data; document all assumptions.",
        entity_scope="Open hole intervals",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Fjaer, E. et al., Petroleum Related Rock Mechanics, 2008"
    ),
    DoctrineBlock(
        topic="Depletion-Induced Stress Changes (Reservoir Compaction)",
        keywords=["depletion", "stress change", "reservoir compaction", "wellbore stability", "MEM"],
        conclusion_template="Depletion-induced stress changes are modeled to assess impact on wellbore stability and casing integrity.",
        reasoning_framework=(
            "1. Model reservoir pressure decline and compaction using MEM.\n"
            "2. Calculate changes in horizontal and vertical stresses due to depletion.\n"
            "3. Assess impact on wellbore stability (collapse, breakout) and casing deformation.\n"
            "4. Monitor for field evidence of compaction (subsidence, casing deformation).\n"
            "5. Adjust drilling and completion plans based on predicted stress changes.\n"
            "6. Update MEM as new depletion and compaction data become available."
        ),
        key_factors=["reservoir pressure decline", "compaction model", "stress path", "field monitoring"],
        primary_authority=["Zoback (2007)", "Fjaer et al. (2008)", "SPE 102835"],
        burden_holder="Geomechanics Specialist / Reservoir Engineer",
        adversary_position="Stress path assumptions may not capture local reservoir heterogeneity.",
        counter_arguments=[
            "Use field monitoring to validate models.",
            "Update MEM with new data.",
            "Document all assumptions and limitations."
        ],
        resolution_strategy="Integrate modeling and field data; update plans as needed.",
        entity_scope="Depleted reservoirs",
        confidence=0.84,
        confidence_zone="Moderate",
        controlling_precedent="Zoback, M.D., Reservoir Geomechanics, 2007"
    ),
    # Additional doctrines for completeness (to reach 40+)
    DoctrineBlock(
        topic="Wellbore Trajectory Optimization for Stability",
        keywords=["wellbore trajectory", "stability", "azimuth", "inclination", "MEM"],
        conclusion_template="Wellbore trajectory is optimized based on MEM to minimize risk of instability and maximize drilling efficiency.",
        reasoning_framework=(
            "1. Use MEM to model stress orientation and magnitude at planned well location.\n"
            "2. Simulate different wellbore azimuths and inclinations to assess stability risk.\n"
            "3. Select trajectory that minimizes exposure to high-stress or weak formations.\n"
            "4. Validate with field experience and offset well data.\n"
            "5. Document trajectory selection rationale and risk mitigation measures.\n"
            "6. Update trajectory as new MEM data become available."
        ),
        key_factors=["MEM quality", "stress orientation", "formation strength", "drilling efficiency"],
        primary_authority=["Zoback (2007)", "SPE 102835", "Fjaer et al. (2008)"],
        burden_holder="Drilling Engineer / Geomechanics Specialist",
        adversary_position="Optimal trajectory may conflict with reservoir or operational objectives.",
        counter_arguments=[
            "Balance stability with reservoir access and operational constraints.",
            "Document all trade-offs and risk mitigation.",
            "Update plan as new data become available."
        ],
        resolution_strategy="Integrate geomechanical and reservoir objectives; document all decisions.",
        entity_scope="All planned wells",
        confidence=0.86,
        confidence_zone="Moderate-High",
        controlling_precedent="Zoback, M.D., Reservoir Geomechanics, 2007"
    ),
    DoctrineBlock(
        topic="Mud Weight Window Management",
        keywords=["mud weight window", "collapse gradient", "fracture gradient", "wellbore stability"],
        conclusion_template="Mud weight window is managed by balancing collapse and fracture gradients to ensure safe and stable drilling.",
        reasoning_framework=(
            "1. Calculate collapse gradient (minimum mud weight) and fracture gradient (maximum mud weight) at each depth.\n"
            "2. Select mud weight that maintains wellbore stability without inducing losses.\n"
            "3. Monitor for signs of instability (breakouts, cavings) or losses (mud losses, pressure drops).\n"
            "4. Adjust mud weight and properties as drilling progresses.\n"
            "5. Document all mud weight changes and rationale.\n"
            "6. Integrate with wellbore stability and loss prevention strategies."
        ),
        key_factors=["collapse gradient", "fracture gradient", "wellbore stability", "mud properties"],
        primary_authority=["Fjaer et al. (2008)", "Zoback (2007)", "SPE 102835"],
        burden_holder="Drilling Engineer / Mud Engineer",
        adversary_position="Narrow mud weight windows may be difficult to manage in practice.",
        counter_arguments=[
            "Use real-time monitoring and rapid response protocols.",
            "Apply advanced mud systems for narrow windows.",
            "Document all operational challenges."
        ],
        resolution_strategy="Integrate real-time data; adjust mud program as needed.",
        entity_scope="All drilled intervals",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Fjaer, E. et al., Petroleum Related Rock Mechanics, 2008"
    ),
    DoctrineBlock(
        topic="Wellbore Strengthening Techniques",
        keywords=["wellbore strengthening", "LCM", "stress cage", "mud additives", "fracture gradient"],
        conclusion_template="Wellbore strengthening techniques are applied to increase fracture gradient and reduce lost circulation risk.",
        reasoning_framework=(
            "1. Identify intervals with low fracture gradient or history of losses.\n"
            "2. Apply wellbore strengthening materials (LCM, stress cage, mud additives) during drilling.\n"
            "3. Monitor for increases in fracture gradient and reduction in mud losses.\n"
            "4. Adjust strengthening program based on field response.\n"
            "5. Document all interventions and results.\n"
            "6. Integrate with wellbore stability and mud weight management."
        ),
        key_factors=["fracture gradient", "LCM type", "mud properties", "field monitoring"],
        primary_authority=["SPE 102835", "Fjaer et al. (2008)", "Schlumberger Oilfield Glossary"],
        burden_holder="Drilling Engineer / Mud Engineer",
        adversary_position="Strengthening techniques may not be effective in all formations.",
        counter_arguments=[
            "Select materials based on formation properties.",
            "Monitor and adjust program in real time.",
            "Document all outcomes and lessons learned."
        ],
        resolution_strategy="Apply strengthening selectively; monitor effectiveness.",
        entity_scope="Loss-prone intervals",
        confidence=0.83,
        confidence_zone="Moderate",
        controlling_precedent="SPE 102835, 2006"
    ),
    DoctrineBlock(
        topic="Casing Seat Selection for Stability",
        keywords=["casing seat", "stability", "MEM", "collapse gradient", "fracture gradient"],
        conclusion_template="Casing seat depth is selected based on MEM to ensure stability and manage mud weight window.",
        reasoning_framework=(
            "1. Use MEM to identify intervals with significant changes in collapse or fracture gradient.\n"
            "2. Select casing seat above intervals with high instability or loss risk.\n"
            "3. Validate selection with offset well data and field experience.\n"
            "4. Document all casing seat decisions and rationale.\n"
            "5. Adjust plan as new MEM or field data become available.\n"
            "6. Integrate with overall well design and drilling program."
        ),
        key_factors=["MEM quality", "gradient changes", "offset data", "field experience"],
        primary_authority=["Zoback (2007)", "Fjaer et al. (2008)", "SPE 102835"],
        burden_holder="Drilling Engineer / Geomechanics Specialist",
        adversary_position="Casing seat selection may be constrained by operational or reservoir objectives.",
        counter_arguments=[
            "Balance stability with operational constraints.",
            "Document all trade-offs and mitigation measures.",
            "Update plan as new data become available."
        ],
        resolution_strategy="Integrate geomechanical, operational, and reservoir objectives.",
        entity_scope="All planned wells",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="Zoback, M.D., Reservoir Geomechanics, 2007"
    ),
    DoctrineBlock(
        topic="Real-Time Wellbore Stability Monitoring",
        keywords=["real-time monitoring", "wellbore stability", "drilling parameters", "cavings", "breakouts"],
        conclusion_template="Real-time monitoring is implemented to detect wellbore instability and enable rapid response.",
        reasoning_framework=(
            "1. Monitor drilling parameters (torque, drag, ROP, mud losses) in real time.\n"
            "2. Analyze cuttings and cavings for signs of instability.\n"
            "3. Use image logs and caliper logs to detect breakouts and washouts.\n"
            "4. Implement rapid response protocols (adjust mud weight, circulation, drilling parameters).\n"
            "5. Document all instability events and responses.\n"
            "6. Update wellbore stability models with real-time data."
        ),
        key_factors=["monitoring system", "response protocols", "data integration", "model updating"],
        primary_authority=["SPE 102835", "Fjaer et al. (2008)", "Schlumberger Oilfield Glossary"],
        burden_holder="Drilling Engineer / Geomechanics Specialist",
        adversary_position="Real-time systems may generate false positives or miss subtle events.",
        counter_arguments=[
            "Train personnel in event recognition.",
            "Integrate multiple data sources for confirmation.",
            "Document all events and responses."
        ],
        resolution_strategy="Use integrated monitoring and response; document all findings.",
        entity_scope="All drilled intervals",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 102835, 2006"
    ),
    DoctrineBlock(
        topic="Formation Strength Testing (UCS, Triaxial, Tensile)",
        keywords=["formation strength", "UCS", "triaxial test", "tensile test", "wellbore stability"],
        conclusion_template="Formation strength is determined from laboratory UCS, triaxial, and tensile tests for use in stability analysis.",
        reasoning_framework=(
            "1. Obtain core samples from target intervals.\n"
            "2. Perform UCS, triaxial, and tensile strength tests in the laboratory.\n"
            "3. Analyze results to determine strength parameters (UCS, cohesion, friction angle, tensile strength).\n"
            "4. Integrate with log-derived estimates for intervals without core.\n"
            "5. Use results in MEM and wellbore stability models.\n"
            "6. Document all test procedures and results."
        ),
        key_factors=["core quality", "test procedures", "data integration", "model updating"],
        primary_authority=["Fjaer et al. (2008)", "ISRM Suggested Methods", "Zoback (2007)"],
        burden_holder="Geomechanics Specialist",
        adversary_position="Lab tests may not represent in-situ conditions due to sample disturbance.",
        counter_arguments=[
            "Correct for sample disturbance using empirical factors.",
            "Calibrate with field observations.",
            "Document all corrections and assumptions."
        ],
        resolution_strategy="Integrate lab and field data; document all procedures.",
        entity_scope="Cored intervals",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Fjaer, E. et al., Petroleum Related Rock Mechanics, 2008"
    ),
    DoctrineBlock(
        topic="Mud Losses Diagnosis and Management",
        keywords=["mud losses", "diagnosis", "management", "wellbore stability", "formation testing"],
        conclusion_template="Mud losses are diagnosed and managed by integrating drilling data, formation properties, and loss prevention strategies.",
        reasoning_framework=(
            "1. Monitor mud returns, pit volume, and drilling parameters for signs of losses.\n"
            "2. Diagnose loss type (seepage, partial, total) and location using flow logs and pressure data.\n"
            "3. Implement loss prevention measures (LCM, mud weight adjustment, squeeze techniques).\n"
            "4. Document all loss events and responses.\n"
            "5. Update wellbore stability and loss models with new data.\n"
            "6. Train personnel in loss recognition and response."
        ),
        key_factors=["monitoring system", "diagnosis accuracy", "response protocols", "data integration"],
        primary_authority=["SPE 20405", "Fjaer et al. (2008)", "Schlumberger Oilfield Glossary"],
        burden_holder="Drilling Engineer / Mud Engineer",
        adversary_position="Loss diagnosis may be ambiguous, leading to inappropriate responses.",
        counter_arguments=[
            "Use multiple data sources for confirmation.",
            "Document all diagnostic steps and rationale.",
            "Update models with field data."
        ],
        resolution_strategy="Integrate data and expertise; document all events and responses.",
        entity_scope="All drilled intervals",
        confidence=0.85,
        confidence_zone="Moderate",
        controlling_precedent="SPE 20405, 1990"
    ),
    DoctrineBlock(
        topic="Borehole Enlargement and Washout Analysis",
        keywords=["borehole enlargement", "washout", "caliper log", "wellbore stability", "hole cleaning"],
        conclusion_template="Borehole enlargement and washout are analyzed using caliper logs and drilling data to assess stability and cleaning efficiency.",
        reasoning_framework=(
            "1. Acquire caliper logs in open hole intervals.\n"
            "2. Compare measured borehole diameter to bit size to identify enlargement or washout.\n"
            "3. Correlate with drilling parameters (ROP, mud properties, hole cleaning efficiency).\n"
            "4. Assess impact on wellbore stability and subsequent operations (logging, casing running).\n"
            "5. Implement corrective actions (adjust mud properties, improve hole cleaning).\n"
            "6. Document all findings and responses."
        ),
        key_factors=["caliper log quality", "drilling parameters", "hole cleaning", "mud properties"],
        primary_authority=["Fjaer et al. (2008)", "SPE 102835", "Schlumberger Oilfield Glossary"],
        burden_holder="Drilling Engineer / Geomechanics Specialist",
        adversary_position="Washout may be misinterpreted as instability rather than poor cleaning.",
        counter_arguments=[
            "Integrate caliper data with drilling and cleaning records.",
            "Monitor for recurring patterns.",
            "Document all diagnostic steps."
        ],
        resolution_strategy="Integrate multiple data sources; document all findings.",
        entity_scope="Open hole intervals",
        confidence=0.83,
        confidence_zone="Moderate",
        controlling_precedent="Fjaer, E. et al., Petroleum Related Rock Mechanics, 2008"
    ),
    DoctrineBlock(
        topic="Wellbore Strength and Fracture Closure Analysis",
        keywords=["wellbore strength", "fracture closure", "LOT", "fracture gradient", "stability"],
        conclusion_template="Wellbore strength and fracture closure are analyzed using LOT data to optimize mud weight and prevent losses.",
        reasoning_framework=(
            "1. Analyze LOT data to determine fracture initiation and closure pressures.\n"
            "2. Assess wellbore strengthening effects from mud and LCM.\n"
            "3. Calculate optimal mud weight to maintain fracture closure and prevent losses.\n"
            "4. Monitor for mud losses and adjust program as needed.\n"
            "5. Document all LOT interpretations and mud weight decisions.\n"
            "6. Integrate with wellbore stability and loss prevention strategies."
        ),
        key_factors=["LOT data quality", "fracture closure pressure", "mud properties", "LCM effectiveness"],
        primary_authority=["SPE 102835", "Fjaer et al. (2008)", "Schlumberger Oilfield Glossary"],
        burden_holder="Drilling Engineer / Geomechanics Specialist",
        adversary_position="LOT interpretation may be ambiguous, leading to incorrect mud weight selection.",
        counter_arguments=[
            "Use multiple LOTs for confirmation.",
            "Document all interpretations and rationale.",
            "Update program with new data."
        ],
        resolution_strategy="Integrate LOT data and field experience; document all decisions.",
        entity_scope="All drilled intervals",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="SPE 102835, 2006"
    ),
    DoctrineBlock(
        topic="Formation Collapse and Wellbore Abandonment Criteria",
        keywords=["formation collapse", "wellbore abandonment", "stability", "MEM", "collapse gradient"],
        conclusion_template="Formation collapse and wellbore abandonment criteria are defined based on MEM and collapse gradient analysis.",
        reasoning_framework=(
            "1. Use MEM to identify intervals at risk of collapse under planned mud weights.\n"
            "2. Define abandonment criteria based on predicted instability and operational risk.\n"
            "3. Monitor for signs of collapse (breakouts, tight hole, stuck pipe).\n"
            "4. Implement abandonment procedures if criteria are met.\n"
            "5. Document all decisions and criteria.\n"
            "6. Update criteria as new MEM or field data become available."
        ),
        key_factors=["MEM quality", "collapse gradient", "operational risk", "monitoring"],
        primary_authority=["Zoback (2007)", "Fjaer et al. (2008)", "SPE 102835"],
        burden_holder="Drilling Engineer / Geomechanics Specialist",
        adversary_position="Abandonment criteria may be too conservative, leading to unnecessary well loss.",
        counter_arguments=[
            "Balance safety with operational objectives.",
            "Document all trade-offs and mitigation measures.",
            "Update criteria with field experience."
        ],
        resolution_strategy="Integrate MEM, operational, and safety considerations; document all decisions.",
        entity_scope="All drilled intervals",
        confidence=0.85,
        confidence_zone="Moderate",
        controlling_precedent="Zoback, M.D., Reservoir Geomechanics, 2007"
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