from dataclasses import dataclass
from typing import List, Optional
import enum
import pathlib

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
        topic="Nernst Equation and Electrode Potential",
        keywords=["Nernst equation", "electrode potential", "redox", "equilibrium", "electrochemical cell"],
        conclusion_template="The electrode potential at non-standard conditions can be accurately calculated using the Nernst equation, allowing prediction of cell voltage under varying concentrations and temperatures.",
        reasoning_framework=(
            "The Nernst equation derives from the fundamental thermodynamic relationship between Gibbs free energy and electromotive force. "
            "It relates the electrode potential to the standard electrode potential, temperature, number of electrons transferred, and activities or concentrations of the redox species. "
            "By applying the equation, one can predict how changes in ion concentration and temperature shift the equilibrium potential of an electrode reaction. "
            "This framework assumes ideal behavior or uses activity coefficients to correct for non-idealities. "
            "It is foundational in understanding electrochemical cells, corrosion potentials, and sensor responses. "
            "The equation is expressed as E = E0 - (RT/nF) * ln(Q), where Q is the reaction quotient. "
            "This allows dynamic modeling of electrode potentials in real systems, guiding design and interpretation of experiments."
        ),
        key_factors=["Standard electrode potential (E0)", "Temperature (T)", "Number of electrons transferred (n)", "Reaction quotient (Q)", "Gas constant (R)", "Faraday constant (F)"],
        primary_authority=["Bard & Faulkner, Electrochemical Methods, 2nd Ed.", "Atkins & de Paula, Physical Chemistry, 10th Ed."],
        burden_holder="Proponent of predicted electrode potential under non-standard conditions",
        adversary_position="Claims that standard potentials suffice without correction for concentration or temperature",
        counter_arguments=[
            "Experimental data shows significant deviation from standard potentials at varying concentrations.",
            "Thermodynamic principles mandate correction via reaction quotient.",
            "Ignoring temperature effects leads to inaccurate potential predictions."
        ],
        resolution_strategy="Apply Nernst equation with measured or estimated activities; validate predictions experimentally.",
        entity_scope="Electrochemical cells, sensors, corrosion systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Nernst, W. (1889). Z. Phys. Chem."
    ),
    DoctrineBlock(
        topic="Butler-Volmer Kinetics and Exchange Current Density",
        keywords=["Butler-Volmer equation", "exchange current density", "electrode kinetics", "activation overpotential", "charge transfer"],
        conclusion_template="The rate of an electrochemical reaction at an electrode interface is governed by the Butler-Volmer equation, with the exchange current density serving as a key kinetic parameter.",
        reasoning_framework=(
            "The Butler-Volmer equation models the current-overpotential relationship for electrode reactions by combining anodic and cathodic processes. "
            "It incorporates the exchange current density, which quantifies the intrinsic rate of electron transfer at equilibrium, and the charge transfer coefficient, which reflects symmetry of the energy barrier. "
            "The equation is derived from transition state theory and electrochemical kinetics, linking microscopic reaction rates to measurable current densities. "
            "It captures the exponential increase of current with overpotential in both anodic and cathodic directions, enabling prediction of reaction rates under various driving forces. "
            "This framework is essential for interpreting polarization curves, designing electrodes, and optimizing energy conversion devices."
        ),
        key_factors=["Exchange current density (i0)", "Overpotential (η)", "Charge transfer coefficient (α)", "Temperature (T)", "Number of electrons transferred (n)", "Gas constant (R)", "Faraday constant (F)"],
        primary_authority=["Bard & Faulkner, Electrochemical Methods, 2nd Ed.", "Damjanovic & Bockris, Electrochemical Kinetics"],
        burden_holder="Researcher modeling electrode reaction rates",
        adversary_position="Simplifies kinetics to linear or Tafel approximations ignoring full Butler-Volmer behavior",
        counter_arguments=[
            "Tafel approximations fail at low overpotentials where kinetics are nonlinear.",
            "Exchange current density must be experimentally determined for accuracy.",
            "Charge transfer coefficients vary with reaction mechanism and electrode surface."
        ],
        resolution_strategy="Use full Butler-Volmer equation for comprehensive modeling; validate parameters experimentally.",
        entity_scope="Electrode interfaces, fuel cells, batteries, corrosion",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Butler, S. (1924); Volmer, M. (1925)"
    ),
    DoctrineBlock(
        topic="Cyclic Voltammetry Interpretation",
        keywords=["cyclic voltammetry", "redox peaks", "scan rate", "peak current", "diffusion control", "reversibility"],
        conclusion_template="Cyclic voltammetry provides qualitative and quantitative insights into redox processes, electrode kinetics, and diffusion characteristics by analyzing peak shapes, positions, and currents.",
        reasoning_framework=(
            "Cyclic voltammetry (CV) involves sweeping the electrode potential cyclically and measuring resulting current to probe electrochemical reactions. "
            "The shape and position of anodic and cathodic peaks reveal reversibility, electron transfer kinetics, and coupled chemical reactions. "
            "Peak current dependence on scan rate distinguishes diffusion-controlled from adsorption-controlled processes. "
            "The Randles-Sevcik equation relates peak current to diffusion coefficient, concentration, and scan rate, enabling quantitative analysis. "
            "Interpretation requires consideration of uncompensated resistance, double-layer charging, and electrode surface conditions. "
            "CV is widely used for mechanistic studies, sensor development, and material characterization."
        ),
        key_factors=["Peak potential separation (ΔEp)", "Peak current (Ip)", "Scan rate (ν)", "Diffusion coefficient (D)", "Concentration (C)", "Electrode surface area (A)"],
        primary_authority=["Bard & Faulkner, Electrochemical Methods, 2nd Ed.", "Compton & Banks, Understanding Voltammetry"],
        burden_holder="Analyst interpreting CV data",
        adversary_position="Assumes peak currents are solely capacitive or ignores kinetic effects",
        counter_arguments=[
            "Capacitive currents distort baseline but do not produce redox peaks.",
            "Kinetic limitations shift peak potentials and affect peak shapes.",
            "Diffusion coefficients can be extracted from scan rate dependence."
        ],
        resolution_strategy="Use established electrochemical theory and control experiments to separate faradaic and non-faradaic currents.",
        entity_scope="Electrochemical analysis, sensor development, catalysis",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Randles, J.E.B. (1948); Nicholson & Shain (1964)"
    ),
    DoctrineBlock(
        topic="Electrochemical Impedance Spectroscopy (EIS)",
        keywords=["EIS", "impedance", "Nyquist plot", "Bode plot", "equivalent circuit", "charge transfer resistance", "double layer capacitance"],
        conclusion_template="Electrochemical impedance spectroscopy enables deconvolution of complex electrode processes by modeling frequency-dependent impedance with equivalent circuits.",
        reasoning_framework=(
            "EIS measures the response of an electrochemical system to a small AC perturbation over a range of frequencies, capturing resistive and capacitive behaviors. "
            "Analysis of Nyquist and Bode plots allows identification of charge transfer resistance, double layer capacitance, diffusion impedance (Warburg element), and other phenomena. "
            "Equivalent circuit models represent physical processes with electrical components, facilitating parameter extraction and mechanistic understanding. "
            "This approach is critical for battery diagnostics, corrosion monitoring, sensor characterization, and catalyst evaluation. "
            "Proper experimental design and data fitting are essential to avoid misinterpretation due to non-idealities and noise."
        ),
        key_factors=["Frequency range", "Amplitude of perturbation", "Equivalent circuit elements", "Charge transfer resistance (Rct)", "Double layer capacitance (Cdl)", "Warburg impedance (Zw)"],
        primary_authority=["Bard & Faulkner, Electrochemical Methods, 2nd Ed.", "Lasia, Electrochemical Impedance Spectroscopy and its Applications"],
        burden_holder="Researcher interpreting EIS data",
        adversary_position="Assumes single time constant or ignores diffusion effects",
        counter_arguments=[
            "Many systems exhibit multiple overlapping processes requiring complex circuits.",
            "Diffusion impedance manifests as characteristic low-frequency behavior.",
            "Simplistic models can misrepresent system behavior."
        ],
        resolution_strategy="Use multi-element equivalent circuits and validate with complementary techniques.",
        entity_scope="Electrochemical cells, corrosion, sensors, catalysis",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Orazem & Tribollet, Electrochemical Impedance Spectroscopy, 2008"
    ),
    DoctrineBlock(
        topic="Lithium-Ion Battery Electrochemistry",
        keywords=["lithium-ion battery", "intercalation", "solid electrolyte interphase", "anode", "cathode", "capacity fade", "SEI"],
        conclusion_template="Lithium-ion battery performance and degradation are governed by intercalation mechanisms, solid electrolyte interphase formation, and electrode material stability.",
        reasoning_framework=(
            "Lithium-ion batteries operate via reversible intercalation of lithium ions into electrode host materials, typically graphite anodes and layered oxide cathodes. "
            "The formation of a solid electrolyte interphase (SEI) on the anode surface is critical for stabilizing the interface but contributes to capacity fade through continuous growth and electrolyte consumption. "
            "Electrode structural changes, electrolyte decomposition, and lithium plating also affect cycle life and safety. "
            "Understanding these processes requires integrating electrochemical kinetics, materials science, and thermodynamics. "
            "Advanced characterization techniques and modeling guide the development of improved materials and electrolytes."
        ),
        key_factors=["Intercalation potential", "SEI composition and stability", "Electrolyte formulation", "Charge/discharge rates", "Temperature", "Electrode morphology"],
        primary_authority=["Tarascon & Armand, Nature, 2001", "Goodenough & Kim, Chem. Mater., 2010"],
        burden_holder="Battery developer optimizing performance and lifetime",
        adversary_position="Attributes capacity fade solely to mechanical degradation ignoring chemical effects",
        counter_arguments=[
            "SEI growth consumes lithium and electrolyte, causing irreversible capacity loss.",
            "Electrolyte decomposition products impact electrode surface chemistry.",
            "Mechanical stresses are significant but not the sole degradation mechanism."
        ],
        resolution_strategy="Combine electrochemical testing with surface analysis to identify dominant degradation pathways.",
        entity_scope="Lithium-ion battery cells and packs",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Peled, E. (1979). J. Electrochem. Soc."
    ),
    DoctrineBlock(
        topic="Proton Exchange Membrane Fuel Cells (PEMFC)",
        keywords=["PEM fuel cell", "proton exchange membrane", "catalyst layer", "oxygen reduction reaction", "hydrogen oxidation reaction", "water management"],
        conclusion_template="PEM fuel cell performance depends on efficient proton conduction, catalyst activity for hydrogen oxidation and oxygen reduction, and effective water management within the membrane electrode assembly.",
        reasoning_framework=(
            "PEM fuel cells convert chemical energy of hydrogen and oxygen into electricity via electrochemical reactions at the anode and cathode, separated by a proton-conducting membrane. "
            "The hydrogen oxidation reaction (HOR) at the anode and oxygen reduction reaction (ORR) at the cathode are catalyzed by platinum-based catalysts. "
            "Water produced at the cathode must be managed to maintain membrane hydration for proton conductivity without flooding electrodes. "
            "Mass transport limitations, catalyst degradation, and membrane durability are critical factors influencing cell performance and lifetime. "
            "Modeling and experimental studies focus on optimizing catalyst layers, membrane properties, and operating conditions."
        ),
        key_factors=["Proton conductivity", "Catalyst loading and dispersion", "Water content and management", "Gas diffusion layers", "Operating temperature and pressure"],
        primary_authority=["Larminie & Dicks, Fuel Cell Systems Explained", "Barbir, PEM Fuel Cells"],
        burden_holder="Fuel cell engineer optimizing performance",
        adversary_position="Neglects water management or catalyst degradation effects",
        counter_arguments=[
            "Dry membranes reduce proton conductivity leading to voltage losses.",
            "Flooding blocks reactant access to catalyst sites.",
            "Catalyst sintering reduces active surface area over time."
        ],
        resolution_strategy="Balance hydration and gas transport; use durable catalysts and membranes; monitor operating conditions.",
        entity_scope="PEM fuel cell stacks and systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Zawodzinski et al., J. Electrochem. Soc., 1993"
    ),
    DoctrineBlock(
        topic="Water Electrolysis (Alkaline, PEM, SOEC)",
        keywords=["water electrolysis", "alkaline electrolysis", "PEM electrolysis", "solid oxide electrolysis cell", "hydrogen production", "overpotential"],
        conclusion_template="Water electrolysis technologies enable hydrogen production by splitting water molecules, with performance governed by electrode kinetics, electrolyte conductivity, and cell design.",
        reasoning_framework=(
            "Water electrolysis involves the anodic oxygen evolution reaction (OER) and cathodic hydrogen evolution reaction (HER). "
            "Alkaline electrolysis uses a liquid alkaline electrolyte and non-precious metal catalysts, while PEM electrolysis employs a solid polymer electrolyte and noble metal catalysts for higher current densities and purity. "
            "Solid oxide electrolysis cells (SOEC) operate at high temperatures enabling efficient steam electrolysis. "
            "Overpotentials arise from kinetic barriers, ohmic losses, and mass transport limitations. "
            "Optimizing catalyst activity, membrane conductivity, and cell architecture is essential for energy-efficient hydrogen production."
        ),
        key_factors=["Electrode catalyst activity", "Electrolyte conductivity", "Operating temperature", "Cell voltage and current density", "Mass transport"],
        primary_authority=["Barbir, PEM Electrolysis", "Zeng & Zhang, Prog. Energy Combust. Sci., 2010"],
        burden_holder="Electrolyzer designer improving efficiency",
        adversary_position="Overlooks kinetic overpotentials or assumes ideal catalysts",
        counter_arguments=[
            "Real catalysts exhibit significant overpotentials affecting energy consumption.",
            "Membrane resistance contributes to voltage losses.",
            "Mass transport limitations reduce achievable current densities."
        ],
        resolution_strategy="Employ advanced catalysts, optimize cell design, and operate under conditions minimizing losses.",
        entity_scope="Water electrolyzers for hydrogen production",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Bockris & Srinivasan, Electrochemical Hydrogen Technology, 1972"
    ),
    DoctrineBlock(
        topic="Corrosion Electrochemistry and Polarization Curves",
        keywords=["corrosion", "polarization curve", "anodic reaction", "cathodic reaction", "corrosion potential", "corrosion rate"],
        conclusion_template="Corrosion rates and mechanisms can be elucidated by analyzing polarization curves that depict the relationship between electrode potential and current density.",
        reasoning_framework=(
            "Corrosion involves simultaneous anodic metal dissolution and cathodic reduction reactions. "
            "Polarization curves plot current density versus electrode potential, revealing corrosion potential (Ecorr) and corrosion current density (Icorr). "
            "Tafel extrapolation of anodic and cathodic branches allows quantification of corrosion rates. "
            "The mixed potential theory explains that corrosion potential is where anodic and cathodic currents balance. "
            "Environmental factors, alloy composition, and surface conditions influence the shape of polarization curves and corrosion behavior."
        ),
        key_factors=["Corrosion potential (Ecorr)", "Corrosion current density (Icorr)", "Tafel slopes", "Electrolyte composition", "Temperature", "Surface condition"],
        primary_authority=["Jones, Principles and Prevention of Corrosion", "Bard & Faulkner, Electrochemical Methods"],
        burden_holder="Corrosion engineer assessing material durability",
        adversary_position="Assumes corrosion rate from open circuit potential alone",
        counter_arguments=[
            "Open circuit potential does not quantify corrosion rate.",
            "Polarization curves provide kinetic parameters essential for rate calculation.",
            "Environmental changes alter anodic and cathodic kinetics."
        ],
        resolution_strategy="Perform potentiodynamic polarization and Tafel analysis to determine corrosion parameters.",
        entity_scope="Metallic materials in corrosive environments",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Evans, U.R. (1960). Corrosion and Electrochemistry"
    ),
    DoctrineBlock(
        topic="Electroplating and Electrodeposition",
        keywords=["electroplating", "electrodeposition", "metal coating", "current efficiency", "throwing power", "bath composition"],
        conclusion_template="Electroplating quality and uniformity depend on controlling current density, bath composition, and mass transport to achieve desired metal deposition characteristics.",
        reasoning_framework=(
            "Electroplating deposits a metal layer onto a substrate via electrodeposition from an electrolyte solution containing metal ions. "
            "Current efficiency, defined as the fraction of current used for metal deposition, affects thickness and quality. "
            "Throwing power describes the ability to plate uniformly on complex geometries. "
            "Bath composition, temperature, agitation, and additives influence deposit morphology, grain size, and internal stress. "
            "Understanding electrochemical kinetics and mass transport phenomena is essential for optimizing plating processes and preventing defects."
        ),
        key_factors=["Current density", "Bath metal ion concentration", "Temperature", "Agitation", "Additives", "Substrate preparation"],
        primary_authority=["Schlesinger & Paunovic, Modern Electroplating", "Lowenheim, Electroplating Engineering Handbook"],
        burden_holder="Process engineer controlling plating quality",
        adversary_position="Neglects mass transport limitations or additive effects",
        counter_arguments=[
            "Mass transport limits maximum current density without concentration polarization.",
            "Additives modify deposit properties and must be carefully controlled.",
            "Substrate cleanliness affects adhesion and deposit uniformity."
        ],
        resolution_strategy="Monitor and control plating parameters; use agitation and additives to optimize deposition.",
        entity_scope="Electroplating baths and processes",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Lowenheim, F.A. (1978). Electroplating Engineering Handbook"
    ),
    DoctrineBlock(
        topic="Supercapacitors and Double-Layer Capacitance",
        keywords=["supercapacitors", "double-layer capacitance", "electrochemical capacitor", "energy storage", "pseudocapacitance"],
        conclusion_template="Supercapacitors store energy primarily via electrostatic double-layer capacitance and pseudocapacitance, enabling high power density and long cycle life.",
        reasoning_framework=(
            "Supercapacitors utilize high surface area electrodes and electrolytes to form electric double layers at interfaces, storing charge electrostatically. "
            "Pseudocapacitance arises from fast, reversible redox reactions at or near the electrode surface, enhancing capacitance beyond pure double-layer effects. "
            "The combination results in devices with higher capacitance and power density than conventional capacitors but lower energy density than batteries. "
            "Understanding charge storage mechanisms, electrode materials, and electrolyte properties is key to optimizing performance. "
            "Equivalent circuit modeling and electrochemical characterization techniques elucidate behavior and guide design."
        ),
        key_factors=["Electrode surface area", "Electrolyte ionic conductivity", "Pseudocapacitive materials", "Charge-discharge rates", "Cycle stability"],
        primary_authority=["Conway, Electrochemical Supercapacitors", "Simon & Gogotsi, Nat. Mater., 2008"],
        burden_holder="Materials scientist developing supercapacitor electrodes",
        adversary_position="Attributes capacitance solely to double-layer effects ignoring pseudocapacitance",
        counter_arguments=[
            "Pseudocapacitive materials contribute significantly to total capacitance.",
            "Electrochemical signatures distinguish double-layer and faradaic processes.",
            "Incorporating pseudocapacitive materials improves energy density."
        ],
        resolution_strategy="Combine electrochemical techniques and materials characterization to identify and enhance capacitance mechanisms.",
        entity_scope="Supercapacitor devices and materials",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Conway, B.E. (1999). Electrochemical Supercapacitors"
    ),
    DoctrineBlock(
        topic="Potentiostats and Electrochemical Instrumentation",
        keywords=["potentiostat", "galvanostat", "electrochemical cell", "control modes", "signal measurement", "noise reduction"],
        conclusion_template="Potentiostats enable precise control and measurement of electrode potentials and currents, facilitating diverse electrochemical experiments with high accuracy.",
        reasoning_framework=(
            "Potentiostats maintain a set electrode potential relative to a reference electrode by adjusting current flow through a counter electrode. "
            "Galvanostats control current and measure resulting potentials. "
            "Advanced instrumentation incorporates feedback loops, low-noise amplifiers, and digital signal processing to enhance measurement fidelity. "
            "Proper cell setup, electrode configuration, and shielding minimize artifacts and noise. "
            "Understanding instrument capabilities and limitations is essential for designing experiments and interpreting data."
        ),
        key_factors=["Control mode (potentiostatic/galvanostatic)", "Electrode configuration", "Measurement bandwidth", "Noise filtering", "Calibration"],
        primary_authority=["Bard & Faulkner, Electrochemical Methods", "Gamry Instruments Application Notes"],
        burden_holder="Electrochemist setting up experiments",
        adversary_position="Underestimates impact of instrumentation artifacts",
        counter_arguments=[
            "Uncompensated resistance and capacitance distort measurements.",
            "Noise can mask small signals without proper filtering.",
            "Calibration ensures accuracy and reproducibility."
        ],
        resolution_strategy="Use appropriate instrumentation settings, cell design, and calibration protocols.",
        entity_scope="Electrochemical laboratories and instrumentation",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Bard & Faulkner, Electrochemical Methods, 2nd Ed."
    ),
    DoctrineBlock(
        topic="Electrochemical Sensors and Biosensors",
        keywords=["electrochemical sensor", "biosensor", "selectivity", "sensitivity", "transducer", "enzyme electrode"],
        conclusion_template="Electrochemical sensors transduce chemical or biological interactions into measurable electrical signals, with performance dictated by selectivity, sensitivity, and stability.",
        reasoning_framework=(
            "Electrochemical sensors utilize electrodes modified with recognition elements (e.g., enzymes, antibodies) to detect analytes via redox reactions or binding events. "
            "Signal transduction mechanisms include amperometry, potentiometry, and impedance changes. "
            "Selectivity arises from the specificity of recognition elements and electrode surface chemistry. "
            "Sensitivity depends on electrode surface area, catalytic activity, and signal amplification strategies. "
            "Stability and reproducibility are influenced by immobilization methods and environmental conditions. "
            "Integration with electronics enables real-time monitoring and miniaturization."
        ),
        key_factors=["Recognition element specificity", "Electrode material", "Signal transduction method", "Interference rejection", "Operating conditions"],
        primary_authority=["Wang, Analytical Electrochemistry", "Turner et al., Biosensors & Bioelectronics"],
        burden_holder="Sensor developer ensuring reliable detection",
        adversary_position="Overlooks interference effects or sensor drift",
        counter_arguments=[
            "Interferents can produce false signals without proper selectivity.",
            "Sensor drift reduces accuracy over time.",
            "Calibration and signal processing mitigate these issues."
        ],
        resolution_strategy="Design selective recognition layers; implement calibration and compensation algorithms.",
        entity_scope="Chemical and biological sensing devices",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Wang, J. (2006). Analytical Electrochemistry"
    ),
    DoctrineBlock(
        topic="Electrochemical Capacitors vs Batteries",
        keywords=["electrochemical capacitor", "battery", "energy density", "power density", "charge storage mechanism", "cycle life"],
        conclusion_template="Electrochemical capacitors and batteries differ fundamentally in charge storage mechanisms, resulting in trade-offs between energy density, power density, and cycle life.",
        reasoning_framework=(
            "Electrochemical capacitors store charge via electrostatic double-layer formation and pseudocapacitance, enabling rapid charge-discharge cycles and high power density. "
            "Batteries store energy through bulk redox reactions involving phase changes, providing higher energy density but lower power density and shorter cycle life. "
            "The choice between technologies depends on application requirements for energy, power, longevity, and cost. "
            "Hybrid devices attempt to combine advantages of both. "
            "Understanding electrochemical mechanisms and material properties guides device selection and development."
        ),
        key_factors=["Charge storage mechanism", "Energy density", "Power density", "Cycle life", "Self-discharge rate"],
        primary_authority=["Conway, Electrochemical Supercapacitors", "Tarascon & Armand, Nature, 2001"],
        burden_holder="Energy storage system designer",
        adversary_position="Assumes capacitors can replace batteries without trade-offs",
        counter_arguments=[
            "Capacitors have lower energy density limiting runtime.",
            "Batteries have slower charge-discharge rates.",
            "Material and cost considerations influence technology choice."
        ],
        resolution_strategy="Match device characteristics to application needs; consider hybrid solutions.",
        entity_scope="Energy storage devices",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Conway, B.E. (1999). Electrochemical Supercapacitors"
    ),
    DoctrineBlock(
        topic="Electrowinning and Electrorefining of Metals",
        keywords=["electrowinning", "electrorefining", "metal recovery", "purification", "current efficiency", "impurities"],
        conclusion_template="Electrowinning and electrorefining processes enable metal recovery and purification by controlled electrodeposition, with efficiency influenced by electrolyte composition and operating conditions.",
        reasoning_framework=(
            "Electrowinning extracts metals from solutions by cathodic deposition, while electrorefining purifies metals by selective dissolution and redeposition. "
            "Current efficiency depends on minimizing side reactions such as hydrogen evolution. "
            "Electrolyte composition, temperature, and current density affect deposit morphology and purity. "
            "Impurities can co-deposit or remain in solution, requiring process control and additives. "
            "Understanding electrochemical kinetics and mass transport is essential for optimizing yield and quality."
        ),
        key_factors=["Current density", "Electrolyte composition", "Temperature", "Impurity concentration", "Additives"],
        primary_authority=["Lowenheim, Electroplating Engineering Handbook", "Schlesinger & Paunovic, Modern Electroplating"],
        burden_holder="Metallurgical engineer optimizing recovery processes",
        adversary_position="Ignores side reactions or impurity effects",
        counter_arguments=[
            "Side reactions reduce current efficiency and increase costs.",
            "Impurities affect deposit quality and downstream processing.",
            "Additives can suppress unwanted reactions."
        ],
        resolution_strategy="Control operating parameters and electrolyte chemistry; monitor deposit quality.",
        entity_scope="Metal recovery and refining operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Lowenheim, F.A. (1978). Electroplating Engineering Handbook"
    ),
    DoctrineBlock(
        topic="Electron Transfer Kinetics and Marcus Theory",
        keywords=["electron transfer", "Marcus theory", "activation energy", "reorganization energy", "rate constant", "outer sphere reaction"],
        conclusion_template="Electron transfer rates are governed by the interplay of driving force, reorganization energy, and electronic coupling as described by Marcus theory.",
        reasoning_framework=(
            "Marcus theory provides a quantitative framework for outer-sphere electron transfer reactions, relating the rate constant to the free energy change and reorganization energy of the system. "
            "The theory models the activation barrier as a function of nuclear reorganization of reactants and solvent. "
            "It predicts a parabolic dependence of rate on driving force, including the inverted region where excessive driving force reduces rate. "
            "This framework bridges quantum mechanics and classical thermodynamics, informing design of redox-active materials and catalysts."
        ),
        key_factors=["Free energy change (ΔG0)", "Reorganization energy (λ)", "Electronic coupling", "Temperature", "Solvent dynamics"],
        primary_authority=["Marcus, R.A., J. Chem. Phys., 1956", "Bard & Faulkner, Electrochemical Methods"],
        burden_holder="Chemist modeling electron transfer rates",
        adversary_position="Uses classical Arrhenius kinetics ignoring reorganization effects",
        counter_arguments=[
            "Marcus theory explains rate anomalies not captured by Arrhenius models.",
            "Reorganization energy is critical for accurate rate predictions.",
            "Experimental data supports Marcus parabolic dependence."
        ],
        resolution_strategy="Apply Marcus theory parameters from spectroscopy and electrochemistry for modeling.",
        entity_scope="Electron transfer reactions in solution and at interfaces",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Marcus, R.A. (1956). J. Chem. Phys."
    ),
    DoctrineBlock(
        topic="Electrochemical CO2 Reduction",
        keywords=["CO2 reduction", "electrocatalysis", "product selectivity", "overpotential", "reaction pathways", "catalyst design"],
        conclusion_template="Electrochemical CO2 reduction efficiency and product distribution depend on catalyst surface properties, applied potential, and electrolyte environment.",
        reasoning_framework=(
            "CO2 reduction involves multiple proton-coupled electron transfer steps leading to diverse products such as CO, formate, hydrocarbons, and alcohols. "
            "Catalyst surface structure, composition, and binding energies influence reaction pathways and selectivity. "
            "Applied overpotential affects reaction kinetics and competing hydrogen evolution reaction. "
            "Electrolyte pH and cation effects modulate intermediate stabilization. "
            "Comprehensive mechanistic understanding guides rational catalyst design to improve efficiency and selectivity."
        ),
        key_factors=["Catalyst material and morphology", "Applied potential", "Electrolyte composition", "pH", "Mass transport"],
        primary_authority=["Jaramillo et al., Science, 2016", "Koper, Chem. Sci., 2013"],
        burden_holder="Researcher developing CO2 reduction catalysts",
        adversary_position="Attributes product distribution solely to applied potential ignoring catalyst effects",
        counter_arguments=[
            "Catalyst surface properties strongly influence intermediate binding and pathways.",
            "Electrolyte environment modulates reaction energetics.",
            "Applied potential alone cannot explain selectivity trends."
        ],
        resolution_strategy="Integrate experimental and computational studies to tailor catalyst properties.",
        entity_scope="Electrocatalytic CO2 reduction systems",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="Hori, Y. (2008). Modern Aspects of Electrochemistry"
    ),
    DoctrineBlock(
        topic="Ionic Conductivity in Solid Electrolytes",
        keywords=["ionic conductivity", "solid electrolyte", "ion transport", "activation energy", "grain boundaries", "defects"],
        conclusion_template="Ionic conductivity in solid electrolytes arises from ion migration facilitated by crystal defects and is influenced by temperature, microstructure, and material composition.",
        reasoning_framework=(
            "Solid electrolytes conduct ions through vacancies, interstitials, or interstitialcy mechanisms within crystalline or amorphous matrices. "
            "Activation energy barriers govern ion mobility, with temperature dependence described by Arrhenius behavior. "
            "Grain boundaries and defects can either enhance or impede conduction depending on structure and chemistry. "
            "Material doping and microstructural engineering optimize pathways for fast ion transport. "
            "Understanding these factors is critical for solid-state batteries and fuel cells."
        ),
        key_factors=["Defect concentration", "Grain boundary characteristics", "Temperature", "Material composition", "Crystal structure"],
        primary_authority=["Goodenough, J.B., Solid State Ionics", "Bruce et al., Chem. Soc. Rev., 2012"],
        burden_holder="Materials scientist developing solid electrolytes",
        adversary_position="Assumes bulk conductivity dominates ignoring grain boundary effects",
        counter_arguments=[
            "Grain boundaries often present higher resistance.",
            "Defect engineering can enhance overall conductivity.",
            "Microstructure critically affects ion transport."
        ],
        resolution_strategy="Combine impedance spectroscopy and microscopy to characterize conduction pathways.",
        entity_scope="Solid electrolyte materials for energy devices",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Goodenough, J.B. (1976). Solid State Ionics"
    ),
    DoctrineBlock(
        topic="Redox Flow Batteries",
        keywords=["redox flow battery", "electrolyte flow", "energy storage", "membrane", "electrode kinetics", "capacity fade"],
        conclusion_template="Redox flow battery performance depends on electrolyte composition, membrane selectivity, and electrode kinetics, enabling scalable energy storage with decoupled power and capacity.",
        reasoning_framework=(
            "Redox flow batteries store energy in liquid electrolytes containing redox-active species circulated through electrochemical cells. "
            "Membrane selectivity prevents cross-mixing of electrolytes while allowing ion transport. "
            "Electrode kinetics and mass transport influence power density and efficiency. "
            "Capacity fade arises from electrolyte degradation, crossover, and side reactions. "
            "System design balances flow rates, cell architecture, and electrolyte chemistry to optimize performance and longevity."
        ),
        key_factors=["Electrolyte redox species", "Membrane permeability", "Flow rate", "Electrode surface area", "Operating temperature"],
        primary_authority=["Skyllas-Kazacos et al., J. Electrochem. Soc., 1996", "Weber et al., J. Appl. Electrochem., 2011"],
        burden_holder="System designer optimizing flow battery operation",
        adversary_position="Neglects electrolyte crossover or assumes ideal membranes",
        counter_arguments=[
            "Crossover reduces capacity and efficiency.",
            "Membrane degradation affects long-term performance.",
            "Electrode kinetics limit achievable power."
        ],
        resolution_strategy="Select membranes with high selectivity; monitor electrolyte composition; optimize flow and electrode design.",
        entity_scope="Redox flow battery systems",
        confidence=0.91,
        confidence_zone="Moderate-High",
        controlling_precedent="Skyllas-Kazacos, M. et al. (1996). J. Electrochem. Soc."
    ),
    DoctrineBlock(
        topic="pH Measurement and Glass Electrode",
        keywords=["pH measurement", "glass electrode", "reference electrode", "Nernst response", "junction potential", "calibration"],
        conclusion_template="Accurate pH measurement relies on the Nernstian response of glass electrodes combined with stable reference electrodes and proper calibration.",
        reasoning_framework=(
            "Glass electrodes measure hydrogen ion activity via a potential developed across a hydrated glass membrane sensitive to H+ ions. "
            "The electrode potential follows the Nernst equation with a slope of approximately 59 mV per pH unit at 25°C. "
            "Reference electrodes provide a stable potential against which the glass electrode is measured. "
            "Liquid junction potentials and temperature variations can introduce errors. "
            "Regular calibration with standard buffers ensures accuracy and compensates for electrode drift."
        ),
        key_factors=["Glass membrane composition", "Reference electrode stability", "Temperature", "Junction potential", "Calibration procedure"],
        primary_authority=["Bates, R.G., Determination of pH", "Bard & Faulkner, Electrochemical Methods"],
        burden_holder="Analyst performing pH measurements",
        adversary_position="Assumes electrode potential is independent of temperature or junction effects",
        counter_arguments=[
            "Temperature affects Nernst slope and electrode response.",
            "Junction potentials cause systematic errors.",
            "Calibration corrects for these influences."
        ],
        resolution_strategy="Use temperature compensation and frequent calibration with standard buffers.",
        entity_scope="Analytical chemistry and process control",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Bates, R.G. (1973). Determination of pH"
    ),
    DoctrineBlock(
        topic="Electrochemical Machining (ECM)",
        keywords=["electrochemical machining", "material removal", "tool electrode", "electrolyte flow", "surface finish", "current density"],
        conclusion_template="Electrochemical machining removes material by anodic dissolution controlled by current density and electrolyte flow, enabling precision shaping without mechanical stress.",
        reasoning_framework=(
            "ECM uses controlled anodic dissolution of a workpiece in an electrolyte under an applied current, with a shaped tool electrode defining the geometry. "
            "Material removal rate is proportional to current density and Faraday's laws. "
            "Electrolyte flow removes reaction products and heat, maintaining process stability. "
            "Surface finish and dimensional accuracy depend on current distribution and gap control. "
            "ECM is suitable for hard or complex materials where mechanical machining is challenging."
        ),
        key_factors=["Current density", "Electrolyte composition and flow rate", "Tool-workpiece gap", "Voltage", "Temperature"],
        primary_authority=["Davis, J.R., Surface Engineering for Corrosion and Wear Resistance", "Bard & Faulkner, Electrochemical Methods"],
        burden_holder="Process engineer optimizing ECM parameters",
        adversary_position="Assumes mechanical removal mechanisms dominate",
        counter_arguments=[
            "Material removal occurs via electrochemical dissolution, not mechanical forces.",
            "Proper electrolyte flow is essential to prevent localized heating and pitting.",
            "Current distribution governs machining precision."
        ],
        resolution_strategy="Control electrical and fluid parameters; monitor machining gap and surface quality.",
        entity_scope="Manufacturing and precision machining",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Davis, J.R. (2001). Surface Engineering"
    ),
    DoctrineBlock(
        topic="Electrode Surface Roughness Effects on Electrochemical Reactions",
        keywords=["electrode surface roughness", "electrochemical kinetics", "active surface area", "double layer", "mass transport"],
        conclusion_template="Electrode surface roughness increases effective active area, influencing reaction rates, double layer capacitance, and mass transport phenomena.",
        reasoning_framework=(
            "Surface roughness enhances the real surface area compared to geometric area, increasing sites available for electron transfer. "
            "This affects measured current densities, double layer capacitance, and local mass transport conditions. "
            "Roughness can induce microconvection and alter diffusion layer thickness. "
            "Quantifying roughness factors is essential for accurate kinetic parameter extraction and electrode design. "
            "Techniques such as cyclic voltammetry and impedance spectroscopy help characterize roughness effects."
        ),
        key_factors=["Roughness factor", "Electrode material", "Measurement technique", "Mass transport regime", "Double layer structure"],
        primary_authority=["Bard & Faulkner, Electrochemical Methods", "Compton & Banks, Understanding Voltammetry"],
        burden_holder="Electrochemist interpreting kinetic data",
        adversary_position="Assumes geometric area equals active area",
        counter_arguments=[
            "Ignoring roughness leads to underestimation of intrinsic kinetics.",
            "Surface morphology influences capacitance and current response.",
            "Correcting for roughness improves data interpretation."
        ],
        resolution_strategy="Measure and apply roughness factors; use complementary characterization methods.",
        entity_scope="Electrode surface characterization",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Bard & Faulkner, Electrochemical Methods, 2nd Ed."
    ),
    DoctrineBlock(
        topic="Mass Transport Limitations in Electrochemical Systems",
        keywords=["mass transport", "diffusion", "convection", "migration", "limiting current", "Nernst diffusion layer"],
        conclusion_template="Mass transport processes including diffusion, convection, and migration govern reactant supply and product removal, limiting electrochemical reaction rates under certain conditions.",
        reasoning_framework=(
            "Electrochemical reactions consume or produce species at electrode surfaces, requiring transport from or to the bulk solution. "
            "Diffusion arises from concentration gradients, convection from fluid motion, and migration from electric fields. "
            "Under steady-state, the Nernst diffusion layer defines the region of concentration gradient. "
            "Limiting current occurs when mass transport cannot sustain reaction rate, leading to concentration polarization. "
            "Understanding and controlling mass transport is essential for optimizing electrode performance and interpreting kinetic data."
        ),
        key_factors=["Diffusion coefficient", "Convection velocity", "Electric field strength", "Concentration gradients", "Electrode geometry"],
        primary_authority=["Bard & Faulkner, Electrochemical Methods", "Newman & Thomas-Alyea, Electrochemical Systems"],
        burden_holder="Electrochemical engineer designing cells",
        adversary_position="Neglects mass transport effects in kinetic analysis",
        counter_arguments=[
            "Mass transport limitations cause deviations from intrinsic kinetics.",
            "Ignoring convection and migration leads to inaccurate models.",
            "Experimental control of hydrodynamics is necessary."
        ],
        resolution_strategy="Incorporate mass transport terms in models; use rotating disk electrodes or flow cells for control.",
        entity_scope="Electrochemical reactors and sensors",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Bard & Faulkner, Electrochemical Methods, 2nd Ed."
    ),
    DoctrineBlock(
        topic="Electrochemical Double Layer Structure and Capacitance",
        keywords=["double layer", "Helmholtz layer", "diffuse layer", "capacitance", "potential distribution", "electrode interface"],
        conclusion_template="The electrochemical double layer at electrode interfaces consists of compact and diffuse regions, determining capacitance and potential distribution critical for interfacial processes.",
        reasoning_framework=(
            "Upon immersion of an electrode in electrolyte, charge separation forms the double layer comprising the compact Helmholtz layer and the diffuse Gouy-Chapman layer. "
            "The Helmholtz layer consists of specifically adsorbed ions and oriented solvent molecules, while the diffuse layer contains mobile ions distributed by electrostatic forces. "
            "The total capacitance is a series combination of these layers, influencing charge storage and reaction kinetics. "
            "Models such as Gouy-Chapman-Stern describe potential and charge distribution. "
            "Double layer properties affect adsorption, electron transfer rates, and impedance."
        ),
        key_factors=["Ion concentration", "Electrode potential", "Solvent dielectric constant", "Temperature", "Specific adsorption"],
        primary_authority=["Bard & Faulkner, Electrochemical Methods", "Stern, Z. Phys. Chem., 1924"],
        burden_holder="Electrochemist modeling interface phenomena",
        adversary_position="Assumes simple capacitor model ignoring diffuse layer",
        counter_arguments=[
            "Diffuse layer contributes significantly at low ionic strength.",
            "Specific adsorption alters capacitance and potential profiles.",
            "Advanced models better fit experimental data."
        ],
        resolution_strategy="Use Gouy-Chapman-Stern model and impedance spectroscopy for characterization.",
        entity_scope="Electrode-electrolyte interfaces",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Stern, O. (1924). Z. Phys. Chem."
    ),
    DoctrineBlock(
        topic="Electrode Passivation and Breakdown",
        keywords=["passivation", "oxide layer", "breakdown potential", "corrosion resistance", "electrochemical stability"],
        conclusion_template="Electrode passivation forms protective oxide layers that inhibit corrosion, with breakdown occurring at critical potentials leading to localized attack.",
        reasoning_framework=(
            "Certain metals form stable oxide films on their surfaces under anodic polarization, reducing corrosion rates by acting as barriers to ion and electron transport. "
            "Passivation depends on potential, pH, and electrolyte composition. "
            "Breakdown potential marks the onset of film rupture or localized corrosion such as pitting. "
            "Electrochemical techniques including potentiodynamic scans identify passivation and breakdown behavior. "
            "Understanding these phenomena informs material selection and corrosion prevention strategies."
        ),
        key_factors=["Oxide film composition", "Potential", "pH", "Chloride ion concentration", "Temperature"],
        primary_authority=["Jones, Principles and Prevention of Corrosion", "Bard & Faulkner, Electrochemical Methods"],
        burden_holder="Corrosion engineer assessing material performance",
        adversary_position="Assumes uniform corrosion without passivation effects",
        counter_arguments=[
            "Passivation significantly reduces corrosion rates.",
            "Localized breakdown leads to accelerated attack.",
            "Environmental factors influence passivation stability."
        ],
        resolution_strategy="Use electrochemical testing to determine passivation range; apply protective coatings or inhibitors.",
        entity_scope="Metallic materials in corrosive environments",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Evans, U.R. (1960). Corrosion and Electrochemistry"
    ),
    DoctrineBlock(
        topic="Electrochemical Noise Analysis for Corrosion Monitoring",
        keywords=["electrochemical noise", "corrosion monitoring", "fluctuation analysis", "localized corrosion", "signal processing"],
        conclusion_template="Electrochemical noise analysis detects and characterizes corrosion processes by monitoring spontaneous fluctuations in current and potential.",
        reasoning_framework=(
            "Electrochemical noise arises from stochastic fluctuations in corrosion current and potential due to localized events such as pitting or film rupture. "
            "Analyzing noise amplitude, frequency content, and statistical properties provides insights into corrosion mechanisms and severity. "
            "Signal processing techniques including spectral analysis and wavelet transforms enhance detection sensitivity. "
            "Noise analysis complements traditional electrochemical methods and enables early warning of corrosion damage."
        ),
        key_factors=["Noise amplitude", "Frequency spectrum", "Statistical parameters", "Electrode surface condition", "Environmental factors"],
        primary_authority=["Bard & Faulkner, Electrochemical Methods", "Uhlig, Corrosion Handbook"],
        burden_holder="Corrosion engineer implementing monitoring systems",
        adversary_position="Considers noise as measurement artifact only",
        counter_arguments=[
            "Noise contains valuable mechanistic information.",
            "Proper instrumentation and analysis distinguish signal from noise.",
            "Noise trends correlate with corrosion progression."
        ],
        resolution_strategy="Deploy sensitive instrumentation and advanced analysis algorithms for monitoring.",
        entity_scope="Corrosion monitoring in industrial systems",
        confidence=0.90,
        confidence_zone="Moderate-High",
        controlling_precedent="Bard & Faulkner, Electrochemical Methods, 2nd Ed."
    ),
    DoctrineBlock(
        topic="Electrochemical Hydrogen Evolution Reaction (HER)",
        keywords=["hydrogen evolution reaction", "catalysis", "overpotential", "Tafel slope", "exchange current density"],
        conclusion_template="The hydrogen evolution reaction kinetics depend on catalyst surface properties, with overpotential and Tafel slope characterizing reaction efficiency.",
        reasoning_framework=(
            "HER involves proton reduction to hydrogen gas at the cathode, proceeding via Volmer, Heyrovsky, and Tafel steps depending on conditions and catalyst. "
            "Exchange current density quantifies intrinsic catalytic activity. "
            "Tafel slope analysis reveals rate-determining steps and reaction mechanism. "
            "Catalyst materials such as platinum exhibit low overpotentials and high exchange currents. "
            "Understanding HER kinetics guides development of efficient electrocatalysts for water splitting and fuel cells."
        ),
        key_factors=["Exchange current density", "Tafel slope", "Catalyst material", "Electrolyte pH", "Temperature"],
        primary_authority=["Bard & Faulkner, Electrochemical Methods", "Trasatti, J. Electroanal. Chem."],
        burden_holder="Catalyst developer optimizing HER activity",
        adversary_position="Assumes HER kinetics independent of catalyst surface structure",
        counter_arguments=[
            "Surface structure strongly affects adsorption energies and kinetics.",
            "Different rate-determining steps manifest in Tafel slopes.",
            "Catalyst composition and morphology influence exchange current."
        ],
        resolution_strategy="Combine electrochemical measurements and surface characterization to optimize catalysts.",
        entity_scope="Electrocatalysis and energy conversion",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Bard & Faulkner, Electrochemical Methods, 2nd Ed."
    ),
    DoctrineBlock(
        topic="Oxygen Reduction Reaction (ORR) Mechanisms",
        keywords=["oxygen reduction reaction", "catalysis", "four-electron pathway", "two-electron pathway", "overpotential", "selectivity"],
        conclusion_template="ORR proceeds via multiple pathways with catalyst-dependent selectivity, influencing efficiency and product distribution in fuel cells and sensors.",
        reasoning_framework=(
            "ORR involves reduction of O2 to water or hydrogen peroxide via four-electron or two-electron pathways. "
            "Catalyst surface properties determine pathway preference and kinetics. "
            "Platinum catalysts favor the four-electron pathway with low overpotential. "
            "Reaction intermediates and adsorbates influence rate and selectivity. "
            "Understanding ORR mechanisms enables design of catalysts with improved activity and durability."
        ),
        key_factors=["Catalyst composition", "Surface structure", "Electrolyte pH", "Overpotential", "Reaction intermediates"],
        primary_authority=["Bard & Faulkner, Electrochemical Methods", "Shao et al., Chem. Rev., 2016"],
        burden_holder="Fuel cell catalyst researcher",
        adversary_position="Assumes single ORR pathway dominates regardless of catalyst",
        counter_arguments=[
            "Different catalysts exhibit distinct selectivity and kinetics.",
            "Two-electron pathway produces undesirable peroxide species.",
            "Catalyst design targets four-electron pathway for efficiency."
        ],
        resolution_strategy="Use electrochemical and spectroscopic methods to elucidate mechanisms and guide catalyst development.",
        entity_scope="Fuel cells and electrochemical sensors",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Bard & Faulkner, Electrochemical Methods, 2nd Ed."
    ),
    DoctrineBlock(
        topic="Electrochemical Stability Window of Electrolytes",
        keywords=["electrochemical stability", "electrolyte decomposition", "potential window", "oxidation", "reduction", "solvent stability"],
        conclusion_template="The electrochemical stability window defines the potential range within which an electrolyte remains stable without decomposition, critical for device performance.",
        reasoning_framework=(
            "Electrolyte solvents and salts decompose outside specific anodic and cathodic potentials, limiting usable voltage range. "
            "Stability window depends on molecular structure, impurities, and electrode materials. "
            "Decomposition products can degrade device components and performance. "
            "Measuring stability window involves cyclic voltammetry and controlled potential experiments. "
            "Selecting electrolytes with wide stability windows enables higher energy density and safer operation."
        ),
        key_factors=["Oxidation potential", "Reduction potential", "Electrode material", "Electrolyte purity", "Temperature"],
        primary_authority=["Xu, K., Chem. Rev., 2014", "Bard & Faulkner, Electrochemical Methods"],
        burden_holder="Electrolyte chemist selecting formulations",
        adversary_position="Assumes electrolyte stability beyond measured limits",
        counter_arguments=[
            "Electrolyte decomposition leads to capacity fade and safety risks.",
            "Impurities lower stability window.",
            "Electrode catalysis can promote decomposition."
        ],
        resolution_strategy="Perform rigorous electrochemical testing; use additives to enhance stability.",
        entity_scope="Battery and capacitor electrolytes",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Xu, K. (2014). Chem. Rev."
    ),
    DoctrineBlock(
        topic="Electrochemical Surface Area (ECSA) Determination",
        keywords=["electrochemical surface area", "catalyst characterization", "charge integration", "hydrogen adsorption", "double layer capacitance"],
        conclusion_template="ECSA quantifies the active surface area of electrocatalysts, determined via electrochemical methods such as charge integration of adsorption/desorption peaks or capacitance measurements.",
        reasoning_framework=(
            "ECSA reflects the real surface area accessible for electrochemical reactions, differing from geometric area due to roughness and porosity. "
            "Methods include integrating charge under hydrogen adsorption/desorption peaks in cyclic voltammetry or measuring double layer capacitance. "
            "Accurate ECSA measurement is essential for normalizing catalytic activity and comparing materials. "
            "Factors such as electrolyte composition and scan rate influence measurements. "
            "Combining multiple techniques improves reliability."
        ),
        key_factors=["Hydrogen adsorption charge", "Capacitance values", "Scan rate", "Electrolyte composition", "Baseline correction"],
        primary_authority=["Bard & Faulkner, Electrochemical Methods", "Trasatti, J. Electroanal. Chem."],
        burden_holder="Catalyst researcher quantifying active area",
        adversary_position="Uses geometric area for activity normalization",
        counter_arguments=[
            "Geometric area underestimates true active sites.",
            "ECSA provides meaningful comparison of intrinsic activity.",
            "Measurement conditions affect ECSA values."
        ],
        resolution_strategy="Standardize measurement protocols; report ECSA alongside geometric area.",
        entity_scope="Electrocatalyst characterization",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Trasatti, S. (1991). J. Electroanal. Chem."
    ),
    DoctrineBlock(
        topic="Electrochemical Quartz Crystal Microbalance (EQCM)",
        keywords=["EQCM", "mass change", "electrodeposition", "frequency shift", "viscoelastic effects"],
        conclusion_template="EQCM measures mass changes at electrode surfaces during electrochemical reactions by monitoring frequency shifts of a quartz crystal resonator.",
        reasoning_framework=(
            "The quartz crystal microbalance detects nanogram-level mass changes via shifts in resonance frequency proportional to deposited or dissolved mass. "
            "Coupling with electrochemical control enables correlation of mass changes with charge passed, revealing reaction mechanisms and efficiencies. "
            "Viscoelastic properties of films can affect frequency and dissipation signals, requiring careful interpretation. "
            "EQCM is valuable for studying electrodeposition, corrosion, and adsorption phenomena."
        ),
        key_factors=["Frequency shift", "Sauerbrey equation", "Electrode surface", "Viscoelasticity", "Electrochemical parameters"],
        primary_authority=["Buttry & Ward, Chem. Rev., 1992", "Bard & Faulkner, Electrochemical Methods"],
        burden_holder="Researcher studying interfacial mass changes",
        adversary_position="Ignores viscoelastic effects in data interpretation",
        counter_arguments=[
            "Non-rigid films cause deviations from Sauerbrey relation.",
            "Dissipation monitoring aids in distinguishing effects.",
            "Proper modeling improves data accuracy."
        ],
        resolution_strategy="Combine frequency and dissipation measurements; validate with complementary techniques.",
        entity_scope="Electrochemical surface analysis",
        confidence=0.91,
        confidence_zone="Moderate-High",
        controlling_precedent="Buttry, D.A. & Ward, M.D. (1992). Chem. Rev."
    ),
    DoctrineBlock(
        topic="Electrochemical Reduction of Nitrogen to Ammonia",
        keywords=["nitrogen reduction reaction", "ammonia synthesis", "electrocatalysis", "selectivity", "overpotential"],
        conclusion_template="Electrochemical nitrogen reduction to ammonia requires catalysts that lower activation barriers and suppress competing hydrogen evolution for efficient ammonia production.",
        reasoning_framework=(
            "The nitrogen reduction reaction (NRR) involves multi-electron and proton transfers to convert N2 to NH3 under ambient conditions. "
            "Catalyst design focuses on activating the strong N≡N bond while minimizing hydrogen evolution reaction (HER) competing for protons and electrons. "
            "Overpotential and selectivity are critical metrics. "
            "Mechanistic understanding from experimental and computational studies guides development of effective catalysts. "
            "Challenges include low current densities and product quantification."
        ),
        key_factors=["Catalyst active sites", "Overpotential", "Proton availability", "Electrolyte composition", "Reaction intermediates"],
        primary_authority=["Chen et al., Chem. Rev., 2020", "Bard & Faulkner, Electrochemical Methods"],
        burden_holder="Researcher developing NRR catalysts",
        adversary_position="Assumes high selectivity achievable without suppressing HER",
        counter_arguments=[
            "HER competes strongly at relevant potentials.",
            "Catalyst surface engineering is necessary to favor NRR.",
            "Electrolyte and operating conditions influence selectivity."
        ],
        resolution_strategy="Design catalysts with tailored binding energies; optimize reaction environment.",
        entity_scope="Electrocatalytic ammonia synthesis",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="Chen, J.G. et al. (2020). Chem. Rev."
    ),
    DoctrineBlock(
        topic="Electrochemical Energy Storage Mechanisms",
        keywords=["energy storage", "faradaic", "non-faradaic", "capacitive", "battery", "supercapacitor"],
        conclusion_template="Electrochemical energy storage involves faradaic processes with charge transfer reactions and non-faradaic processes involving charge separation at interfaces, defining device performance characteristics.",
        reasoning_framework=(
            "Faradaic storage involves redox reactions transferring electrons across interfaces, characteristic of batteries and pseudocapacitors. "
            "Non-faradaic storage arises from electrostatic charge accumulation in electric double layers, typical of supercapacitors. "
            "Device performance metrics such as energy density, power density, and cycle life depend on the dominant storage mechanism. "
            "Understanding these mechanisms aids in material selection and device design for specific applications."
        ),
        key_factors=["Charge transfer reactions", "Double layer capacitance", "Material properties", "Electrode architecture", "Operating conditions"],
        primary_authority=["Conway, Electrochemical Supercapacitors", "Tarascon & Armand, Nature, 2001"],
        burden_holder="Energy storage developer",
        adversary_position="Confuses capacitive and battery storage mechanisms",
        counter_arguments=[
            "Distinct electrochemical signatures differentiate mechanisms.",
            "Performance trade-offs arise from underlying storage processes.",
            "Hybrid devices combine mechanisms for optimized performance."
        ],
        resolution_strategy="Characterize devices electrochemically to identify dominant mechanisms.",
        entity_scope="Energy storage technologies",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Conway, B.E. (1999). Electrochemical Supercapacitors"
    ),
    DoctrineBlock(
        topic="Electrochemical Reaction Mechanisms and Pathways",
        keywords=["reaction mechanism", "intermediates", "electron transfer", "chemical steps", "rate determining step"],
        conclusion_template="Electrochemical reaction mechanisms involve sequential electron transfer and chemical steps, with identification of intermediates and rate-determining steps critical for understanding kinetics.",
        reasoning_framework=(
            "Electrochemical reactions proceed via elementary steps including electron transfer and chemical transformations. "
            "Intermediates formed during the reaction influence overall kinetics and product distribution. "
            "Identifying the rate-determining step enables targeted catalyst and process improvements. "
            "Techniques such as cyclic voltammetry, spectroscopy, and computational modeling elucidate mechanisms. "
            "Mechanistic insights guide rational design of electrocatalysts and reaction conditions."
        ),
        key_factors=["Intermediates identification", "Electron transfer rates", "Chemical reaction rates", "Potential dependence", "Catalyst surface"],
        primary_authority=["Bard & Faulkner, Electrochemical Methods", "Koper, Chem. Sci., 2013"],
        burden_holder="Researcher elucidating reaction pathways",
        adversary_position="Assumes single-step electron transfer without intermediates",
        counter_arguments=[
            "Many reactions involve multiple steps and intermediates.",
            "Mechanistic complexity affects kinetics and selectivity.",
            "Experimental and theoretical methods reveal detailed pathways."
        ],
        resolution_strategy="Combine electrochemical and spectroscopic data with modeling.",
        entity_scope="Electrochemical reaction studies",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Bard & Faulkner, Electrochemical Methods, 2nd Ed."
    ),
    DoctrineBlock(
        topic="Electrochemical Gas Sensors",
        keywords=["gas sensor", "electrochemical detection", "selectivity", "sensitivity", "electrode design", "interference"],
        conclusion_template="Electrochemical gas sensors detect target gases via selective redox reactions at electrodes, with performance influenced by electrode materials and operating conditions.",
        reasoning_framework=(
            "Electrochemical gas sensors operate by oxidizing or reducing target gases at working electrodes, producing measurable currents proportional to gas concentration. "
            "Selectivity is achieved through electrode material choice, potential control, and electrolyte composition. "
            "Sensitivity depends on electrode surface area and catalytic activity. "
            "Interferences from other gases and environmental factors can affect accuracy. "
            "Sensor design balances response time, stability, and power consumption."
        ),
        key_factors=["Electrode material", "Operating potential", "Electrolyte", "Gas diffusion", "Interfering species"],
        primary_authority=["Wang, Analytical Electrochemistry", "Turner et al., Biosensors & Bioelectronics"],
        burden_holder="Sensor developer ensuring reliable gas detection",
        adversary_position="Neglects interference effects or cross-sensitivity",
        counter_arguments=[
            "Interfering gases produce false signals without selectivity.",
            "Electrode modification improves specificity.",
            "Calibration compensates for environmental variations."
        ],
        resolution_strategy="Design selective electrodes; implement signal processing and calibration.",
        entity_scope="Gas sensing applications",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Wang, J. (2006). Analytical Electrochemistry"
    ),
    DoctrineBlock(
        topic="Electrochemical Methods for Corrosion Inhibition Evaluation",
        keywords=["corrosion inhibition", "electrochemical testing", "polarization resistance", "impedance spectroscopy", "inhibitor efficiency"],
        conclusion_template="Electrochemical techniques such as polarization resistance and impedance spectroscopy quantitatively evaluate corrosion inhibitor performance.",
        reasoning_framework=(
            "Corrosion inhibitors reduce metal dissolution rates by adsorbing on surfaces or altering reaction kinetics. "
            "Polarization resistance measurements provide rapid assessment of corrosion rate changes due to inhibitors. "
            "Electrochemical impedance spectroscopy reveals changes in charge transfer resistance and double layer capacitance. "
            "Comparing parameters with and without inhibitors quantifies efficiency. "
            "Testing under relevant environmental conditions ensures practical applicability."
        ),
        key_factors=["Polarization resistance", "Charge transfer resistance", "Double layer capacitance", "Inhibitor concentration", "Environmental conditions"],
        primary_authority=["Jones, Principles and Prevention of Corrosion", "Bard & Faulkner, Electrochemical Methods"],
        burden_holder="Corrosion engineer assessing inhibitor efficacy",
        adversary_position="Relies solely on weight loss measurements ignoring electrochemical data",
        counter_arguments=[
            "Electrochemical methods provide faster and mechanistic insights.",
            "Weight loss lacks sensitivity and temporal resolution.",
            "Combined approaches yield comprehensive evaluation."
        ],
        resolution_strategy="Use electrochemical testing complemented by gravimetric methods.",
        entity_scope="Corrosion inhibition studies",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Jones, D.A. (1996). Principles and Prevention of Corrosion"
    ),
    DoctrineBlock(
        topic="Electrochemical Hydrogen Storage Materials",
        keywords=["hydrogen storage", "electrochemical absorption", "metal hydrides", "capacity", "kinetics"],
        conclusion_template="Electrochemical hydrogen storage utilizes metal hydrides and other materials capable of reversible hydrogen absorption and release, with performance governed by thermodynamics and kinetics.",
        reasoning_framework=(
            "Certain metals and alloys absorb hydrogen electrochemically forming hydrides, enabling compact and safe hydrogen storage. "
            "Storage capacity depends on material composition and microstructure. "
            "Kinetics of absorption and desorption affect charge/discharge rates. "
            "Thermodynamic parameters such as enthalpy and entropy changes determine operating conditions. "
            "Material cycling stability and degradation are critical for practical applications."
        ),
        key_factors=["Material composition", "Hydrogen absorption capacity", "Kinetics", "Thermodynamics", "Cycling stability"],
        primary_authority=["Schlapbach & Züttel, Nature, 2001", "Bard & Faulkner, Electrochemical Methods"],
        burden_holder="Materials scientist developing hydrogen storage systems",
        adversary_position="Assumes high capacity without considering kinetics or stability",
        counter_arguments=[
            "Fast kinetics and stability are essential for practical use.",
            "Material degradation reduces capacity over cycles.",
            "Thermodynamic constraints limit operating conditions."
        ],
        resolution_strategy="Optimize materials for balanced capacity, kinetics, and durability.",
        entity_scope="Hydrogen storage technologies",
        confidence=0.90,
        confidence_zone="Moderate-High",
        controlling_precedent="Schlapbach, L. & Züttel, A. (2001). Nature"
    ),
    DoctrineBlock(
        topic="Electrochemical Surface Modification Techniques",
        keywords=["surface modification", "electrochemical treatment", "anodization", "electropolishing", "coating"],
        conclusion_template="Electrochemical surface modification techniques such as anodization and electropolishing alter surface properties to enhance corrosion resistance, adhesion, and functionality.",
        reasoning_framework=(
            "Anodization forms oxide layers on metals by controlled anodic oxidation, improving corrosion resistance and appearance. "
            "Electropolishing smooths surfaces by preferential anodic dissolution, reducing roughness and defects. "
            "Electrochemical deposition applies coatings or functional layers with controlled thickness and composition. "
            "Process parameters including voltage, current density, electrolyte composition, and time govern outcomes. "
            "These techniques enable tailored surface properties for diverse applications."
        ),
        key_factors=["Current density", "Electrolyte composition", "Voltage", "Time", "Temperature"],
        primary_authority=["Davis, J.R., Surface Engineering for Corrosion and Wear Resistance", "Bard & Faulkner, Electrochemical Methods"],
        burden_holder="Surface engineer optimizing treatment processes",
        adversary_position="Assumes mechanical methods suffice for surface modification",
        counter_arguments=[
            "Electrochemical methods provide precise control and uniformity.",
            "They enable formation of functional oxide layers not achievable mechanically.",
            "Process parameters critically affect surface characteristics."
        ],
        resolution_strategy="Optimize electrochemical parameters and monitor surface properties post-treatment.",
        entity_scope="Surface engineering and materials processing",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Davis, J.R. (2001). Surface Engineering"
    ),
    DoctrineBlock(
        topic="Electrochemical Reaction Rate Constants Determination",
        keywords=["rate constant", "electrochemical kinetics", "Tafel analysis", "exchange current density", "overpotential"],
        conclusion_template="Electrochemical reaction rate constants can be extracted from Tafel plots and exchange current density measurements, providing insights into reaction kinetics.",
        reasoning_framework=(
            "Tafel analysis involves plotting overpotential versus logarithm of current density to determine kinetic parameters including rate constants and transfer coefficients. "
            "Exchange current density represents the intrinsic reaction rate at equilibrium potential. "
            "Accurate determination requires correction for ohmic losses and mass transport effects. "
            "These parameters enable modeling and comparison of catalytic activities. "
            "Combining electrochemical data with theoretical models refines kinetic understanding."
        ),
        key_factors=["Tafel slope", "Exchange current density", "Overpotential", "Temperature", "Electrode surface area"],
        primary_authority=["Bard & Faulkner, Electrochemical Methods", "Damjanovic & Bockris, Electrochemical Kinetics"],
        burden_holder="Electrochemist analyzing reaction kinetics",
        adversary_position="Uses raw current-overpotential data without corrections",
        counter_arguments=[
            "Ohmic and mass transport effects distort kinetic parameters.",
            "Proper data treatment yields reliable rate constants.",
            "Surface area normalization is essential."
        ],
        resolution_strategy="Apply iR compensation and mass transport corrections; use standardized protocols.",
        entity_scope="Electrochemical kinetics studies",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Bard & Faulkner, Electrochemical Methods, 2nd Ed."
    ),
    DoctrineBlock(
        topic="Electrochemical Reduction of Oxygen in Alkaline Media",
        keywords=["oxygen reduction", "alkaline media", "catalysis", "reaction mechanism", "overpotential"],
        conclusion_template="Oxygen reduction in alkaline media proceeds via distinct mechanisms influenced by catalyst type and operating conditions, affecting efficiency and selectivity.",
        reasoning_framework=(
            "In alkaline electrolytes, ORR can proceed via direct four-electron reduction to hydroxide or via two-electron pathways producing peroxide intermediates. "
            "Catalyst materials such as silver, platinum, and transition metal oxides exhibit different activities and selectivities. "
            "Overpotential and pH influence reaction kinetics. "
            "Understanding mechanisms aids in designing catalysts for alkaline fuel cells and metal-air batteries."
        ),
        key_factors=["Catalyst composition", "Electrolyte pH", "Overpotential", "Reaction intermediates", "Temperature"],
        primary_authority=["Bard & Faulkner, Electrochemical Methods", "Shao et al., Chem. Rev., 2016"],
        burden_holder="Fuel cell catalyst developer",
        adversary_position="Assumes acidic ORR mechanisms apply directly to alkaline media",
        counter_arguments=[
            "Mechanistic differences exist between acidic and alkaline ORR.",
            "Catalyst performance varies with electrolyte pH.",
            "Tailored catalysts improve alkaline ORR efficiency."
        ],
        resolution_strategy="Conduct electrochemical and spectroscopic studies specific to alkaline conditions.",
        entity_scope="Alkaline fuel cells and batteries",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Bard & Faulkner, Electrochemical Methods, 2nd Ed."
    ),
    DoctrineBlock(
        topic="Electrochemical Impedance of Porous Electrodes",
        keywords=["porous electrode", "impedance", "diffusion", "charge transfer resistance", "constant phase element"],
        conclusion_template="Porous electrodes exhibit complex impedance behavior characterized by distributed charge transfer resistance and diffusion elements, modeled using equivalent circuits with constant phase elements.",
        reasoning_framework=(
            "Porous electrodes have heterogeneous surfaces and tortuous pathways affecting ion and electron transport. "
            "Impedance spectra show depressed semicircles and Warburg diffusion tails. "
            "Constant phase elements model non-ideal capacitive behavior due to surface roughness and porosity. "
            "Equivalent circuit fitting extracts parameters related to kinetics and mass transport. "
            "Understanding impedance aids in optimizing electrode design for batteries, fuel cells, and sensors."
        ),
        key_factors=["Charge transfer resistance", "Double layer capacitance", "Warburg impedance", "Constant phase element parameters", "Porosity"],
        primary_authority=["Lasia, Electrochemical Impedance Spectroscopy", "Bard & Faulkner, Electrochemical Methods"],
        burden_holder="Electrochemical engineer analyzing porous electrodes",
        adversary_position="Uses simple RC circuits ignoring porosity effects",
        counter_arguments=[
            "Porosity induces distributed time constants.",
            "Constant phase elements better represent real behavior.",
            "Ignoring these leads to inaccurate parameter extraction."
        ],
        resolution_strategy="Employ advanced equivalent circuit models and validate with physical characterization.",
        entity_scope="Porous electrode systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Lasia, A. (2014). Electrochemical Impedance Spectroscopy"
    ),
    DoctrineBlock(
        topic="Electrochemical Reduction of Metal Ions",
        keywords=["metal ion reduction", "electrodeposition", "nucleation", "growth", "overpotential"],
        conclusion_template="Electrochemical reduction of metal ions involves nucleation and growth processes influenced by overpotential, electrolyte composition, and electrode surface.",
        reasoning_framework=(
            "Metal ions in solution are reduced at the cathode forming nuclei that grow into deposits. "
            "Nucleation can be instantaneous or progressive, affecting deposit morphology. "
            "Overpotential drives reduction rate and influences nucleation density. "
            "Electrolyte additives and impurities modify growth patterns and deposit quality. "
            "Understanding these processes enables control over electrodeposited metal properties."
        ),
        key_factors=["Overpotential", "Nucleation rate", "Electrolyte composition", "Additives", "Temperature"],
        primary_authority=["Lowenheim, Electroplating Engineering Handbook", "Bard & Faulkner, Electrochemical Methods"],
        burden_holder="Electroplating engineer controlling deposit characteristics",
        adversary_position="Assumes uniform nucleation without considering kinetics",
        counter_arguments=[
            "Nucleation kinetics determine deposit microstructure.",
            "Additives influence nucleation and growth mechanisms.",
            "Controlling overpotential optimizes deposit quality."
        ],
        resolution_strategy="Use chronoamperometry and microscopy to study nucleation; adjust parameters accordingly.",
        entity_scope="Electrodeposition processes",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Lowenheim, F.A. (1978). Electroplating Engineering Handbook"
    ),
    DoctrineBlock(
        topic="Electrochemical Oxidation of Organic Compounds",
        keywords=["organic oxidation", "electrocatalysis", "reaction pathways", "overpotential", "selectivity"],
        conclusion_template="Electrochemical oxidation of organic compounds proceeds via complex pathways influenced by catalyst properties and applied potential, affecting product distribution and efficiency.",
        reasoning_framework=(
            "Organic molecules undergo electron transfer and chemical transformations at electrode surfaces during oxidation. "
            "Catalyst materials and surface structure influence reaction intermediates and selectivity. "
            "Overpotential affects reaction rates and competing side reactions. "
            "Understanding mechanisms aids in designing selective and efficient electrochemical oxidation processes for synthesis and pollution control."
        ),
        key_factors=["Catalyst material", "Applied potential", "Electrolyte composition", "Reaction intermediates", "Temperature"],
        primary_authority=["Bard & Faulkner, Electrochemical Methods", "Compton & Banks, Understanding Voltammetry"],
        burden_holder="Researcher developing electrochemical oxidation processes",
        adversary_position="Assumes simple direct electron transfer without intermediates",
        counter_arguments=[
            "Multiple intermediates and pathways often exist.",
            "Catalyst properties strongly influence outcomes.",
            "Mechanistic studies guide process optimization."
        ],
        resolution_strategy="Combine electrochemical and spectroscopic methods to elucidate pathways.",
        entity_scope="Electrochemical organic synthesis and remediation",
        confidence=0.90,
        confidence_zone="Moderate-High",
        controlling_precedent="Bard & Faulkner, Electrochemical Methods, 2nd Ed."
    ),
    DoctrineBlock(
        topic="Electrochemical Formation and Reduction of Metal Oxides",
        keywords=["metal oxide", "electrochemical formation", "reduction", "passivation", "catalysis"],
        conclusion_template="Metal oxides form and reduce electrochemically, influencing passivation behavior and catalytic activity depending on potential and environment.",
        reasoning_framework=(
            "Metal surfaces oxidize anodically forming oxide films that can be reduced cathodically under certain potentials. "
            "Oxide formation contributes to passivation and corrosion resistance. "
            "Some metal oxides serve as electrocatalysts for reactions such as oxygen evolution and reduction. "
            "Electrochemical techniques characterize oxide growth, composition, and reduction kinetics. "
            "Understanding these processes informs corrosion control and catalyst design."
        ),
        key_factors=["Potential", "pH", "Electrolyte composition", "Oxide thickness", "Temperature"],
        primary_authority=["Bard & Faulkner, Electrochemical Methods", "Jones, Principles and Prevention of Corrosion"],
        burden_holder="Materials scientist studying oxide behavior",
        adversary_position="Ignores dynamic nature of oxide films",
        counter_arguments=[
            "Oxide films form and dissolve dynamically under electrochemical conditions.",
            "Film properties affect corrosion and catalytic performance.",
            "Electrochemical methods reveal oxide characteristics."
        ],
        resolution_strategy="Use cyclic voltammetry and impedance spectroscopy to study oxides.",
        entity_scope="Metal surfaces and catalysts",
        confidence=0.93,
        confidence_zone="