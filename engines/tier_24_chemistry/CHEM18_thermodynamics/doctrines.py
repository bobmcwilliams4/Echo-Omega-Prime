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
        topic="Peng-Robinson Equation of State Application",
        keywords=["Peng-Robinson", "Equation of State", "PR EOS", "phase equilibria", "thermodynamics", "cubic EOS"],
        conclusion_template="The Peng-Robinson equation of state is appropriate for predicting vapor-liquid equilibria and thermodynamic properties of non-polar and mildly polar fluids at moderate to high pressures.",
        reasoning_framework=(
            "The Peng-Robinson equation of state (PR EOS) is a cubic equation of state widely used in chemical engineering for the prediction of phase equilibria. "
            "It improves upon the van der Waals and Redlich-Kwong equations by introducing temperature-dependent attractive parameters and an acentric factor, "
            "allowing for better accuracy with non-polar and slightly polar compounds. The PR EOS is formulated as:\n"
            "P = RT/(V-b) - a(T)/(V^2 + 2bV - b^2)\n"
            "where a(T) and b are substance-specific parameters. The equation is solved for the compressibility factor Z, "
            "from which fugacity coefficients and phase equilibria can be determined. Its main limitations are for highly polar or associating compounds, "
            "where deviations from experimental data can be significant. Application requires critical properties and acentric factor data, "
            "and mixing rules (e.g., van der Waals) for mixtures. The PR EOS is a standard in process simulation packages."
        ),
        key_factors=[
            "Critical temperature and pressure",
            "Acentric factor",
            "Temperature and pressure conditions",
            "Nature of components (non-polar, mildly polar)",
            "Mixing rules for mixtures"
        ],
        primary_authority=[
            "Peng, D.-Y. and Robinson, D. B., Ind. Eng. Chem. Fundam., 15, 59–64 (1976)",
            "Smith, J.M., Van Ness, H.C., Abbott, M.M., Introduction to Chemical Engineering Thermodynamics"
        ],
        burden_holder="Proponent of PR EOS application",
        adversary_position="PR EOS is inadequate for highly polar or associating systems",
        counter_arguments=[
            "For highly polar or associating systems, activity coefficient models or more advanced equations of state (e.g., CPA, SAFT) may be preferable.",
            "Experimental validation is necessary for novel or complex mixtures."
        ],
        resolution_strategy="Use PR EOS for non-polar and mildly polar systems; validate with experimental data for complex systems.",
        entity_scope="Process simulation, phase equilibrium calculations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Peng and Robinson (1976); Smith, Van Ness & Abbott"
    ),
    DoctrineBlock(
        topic="NRTL Activity Coefficient Model for Non-Ideal Liquids",
        keywords=["NRTL", "activity coefficient", "liquid phase", "non-ideal", "thermodynamics"],
        conclusion_template="The NRTL model is recommended for calculating activity coefficients in highly non-ideal liquid mixtures, especially where hydrogen bonding or strong polarity exists.",
        reasoning_framework=(
            "The Non-Random Two-Liquid (NRTL) model is an activity coefficient model used to describe the non-ideal behavior of liquid mixtures. "
            "It is particularly effective for systems exhibiting strong deviations from Raoult's Law, such as those with hydrogen bonding or high polarity. "
            "The NRTL model introduces binary interaction parameters (τ and α) to account for molecular interactions and local composition effects. "
            "Parameters are typically regressed from experimental VLE or LLE data. The model can handle both miscible and partially miscible systems, "
            "and is widely used in distillation, extraction, and azeotrope prediction. Limitations include the need for reliable parameter data and "
            "potential numerical instability for highly non-ideal systems."
        ),
        key_factors=[
            "Binary interaction parameters (τ, α)",
            "Experimental VLE/LLE data availability",
            "Degree of non-ideality",
            "Presence of hydrogen bonding or strong polarity"
        ],
        primary_authority=[
            "Renon, H. and Prausnitz, J.M., AIChE J., 14, 135–144 (1968)",
            "Perry's Chemical Engineers' Handbook, 9th Edition"
        ],
        burden_holder="User proposing NRTL model",
        adversary_position="NRTL parameters are unavailable or unreliable for the system",
        counter_arguments=[
            "Alternative models (e.g., UNIQUAC, Wilson) may be used if NRTL parameters are not available.",
            "Group contribution methods (e.g., UNIFAC) can provide estimated parameters."
        ],
        resolution_strategy="Use NRTL where parameters are available and system is highly non-ideal; otherwise, consider alternative models.",
        entity_scope="Liquid phase non-ideal mixtures",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Renon and Prausnitz (1968); Perry's Handbook"
    ),
    DoctrineBlock(
        topic="Gibbs Free Energy Minimization for Chemical Equilibrium",
        keywords=["Gibbs free energy", "chemical equilibrium", "minimization", "thermodynamics", "reaction"],
        conclusion_template="Chemical equilibrium is achieved when the total Gibbs free energy of the system is minimized at constant temperature and pressure.",
        reasoning_framework=(
            "The principle of Gibbs free energy minimization states that, for a closed system at constant temperature and pressure, "
            "the equilibrium composition corresponds to the minimum total Gibbs free energy. This is a fundamental thermodynamic criterion for equilibrium. "
            "The method involves expressing the total Gibbs free energy as a function of the number of moles of each species, subject to atomic balance constraints. "
            "Lagrange multipliers are often used to enforce these constraints. The minimization can be performed analytically for simple systems or numerically for complex mixtures. "
            "This approach is general and applies to both homogeneous and heterogeneous equilibria, including multiphase and multiphase-multireaction systems."
        ),
        key_factors=[
            "System temperature and pressure",
            "Species standard Gibbs energies of formation",
            "Atomic/mass balance constraints",
            "Phase equilibria considerations"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M., Introduction to Chemical Engineering Thermodynamics",
            "Prausnitz, J.M., Lichtenthaler, R.N., de Azevedo, E.G., Molecular Thermodynamics of Fluid-Phase Equilibria"
        ],
        burden_holder="Analyst performing equilibrium calculation",
        adversary_position="Alternative criteria (e.g., equilibrium constants) are more practical for simple systems",
        counter_arguments=[
            "For simple reactions, equilibrium constants may be more convenient, but Gibbs minimization is more general and robust for complex systems.",
            "Numerical methods are required for large systems."
        ],
        resolution_strategy="Use Gibbs free energy minimization for complex or multiphase systems; equilibrium constants for simple cases.",
        entity_scope="Chemical equilibrium calculations",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Smith, Van Ness & Abbott; Prausnitz et al."
    ),
    DoctrineBlock(
        topic="Rachford-Rice Flash Calculation for Two-Phase Equilibrium",
        keywords=["Rachford-Rice", "flash calculation", "two-phase", "vapor-liquid equilibrium", "thermodynamics"],
        conclusion_template="The Rachford-Rice equation is the standard method for isothermal flash calculations to determine vapor and liquid phase compositions and amounts.",
        reasoning_framework=(
            "The Rachford-Rice equation is a mass balance relationship used to solve isothermal flash problems, where a feed stream is partially vaporized or condensed. "
            "Given overall composition, temperature, and pressure, the equation is used to determine the fraction of vapor and the compositions of each phase. "
            "The equation is:\n"
            "Σ [zi (Ki - 1) / (1 + V(Ki - 1))] = 0\n"
            "where zi is the feed mole fraction, Ki is the equilibrium ratio, and V is the vapor fraction. "
            "The equation is solved iteratively (e.g., by Newton-Raphson) for V, then phase compositions are calculated. "
            "The Rachford-Rice method is robust and widely implemented in process simulators."
        ),
        key_factors=[
            "Feed composition",
            "Temperature and pressure",
            "Equilibrium ratios (Ki)",
            "Phase rule applicability"
        ],
        primary_authority=[
            "Rachford, H.H. and Rice, J.D., J. Petrol. Technol., 4, 19–23 (1952)",
            "Smith, J.M., Van Ness, H.C., Abbott, M.M."
        ],
        burden_holder="Process engineer performing flash calculation",
        adversary_position="Non-idealities or three-phase systems may require more advanced methods",
        counter_arguments=[
            "For highly non-ideal or multicomponent systems, activity coefficient models or rigorous EOS may be needed.",
            "Three-phase flashes require extension of the method."
        ],
        resolution_strategy="Use Rachford-Rice for two-phase flashes; apply advanced models for non-ideal or multiphase systems.",
        entity_scope="Vapor-liquid equilibrium, process simulation",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Rachford and Rice (1952); Smith, Van Ness & Abbott"
    ),
    DoctrineBlock(
        topic="UNIFAC Group Contribution Method for Predictive VLE",
        keywords=["UNIFAC", "group contribution", "VLE", "activity coefficient", "prediction", "thermodynamics"],
        conclusion_template="The UNIFAC method is suitable for predicting activity coefficients and VLE for mixtures lacking experimental data, using group contribution parameters.",
        reasoning_framework=(
            "The UNIFAC (UNIQUAC Functional-group Activity Coefficients) method is a predictive model for estimating activity coefficients in non-ideal liquid mixtures. "
            "It decomposes molecules into functional groups, and uses group interaction parameters to calculate activity coefficients. "
            "This allows for the prediction of VLE behavior in systems where experimental data is unavailable. "
            "UNIFAC is particularly valuable in process design and simulation for screening solvent systems and predicting azeotrope formation. "
            "Limitations include the accuracy of group parameters and inability to capture specific interactions (e.g., strong hydrogen bonding) not well represented by group contributions."
        ),
        key_factors=[
            "Availability of group parameters",
            "Molecular structure (group identification)",
            "Degree of non-ideality",
            "Presence of specific interactions"
        ],
        primary_authority=[
            "Fredenslund, A., Gmehling, J., Rasmussen, P., Ind. Eng. Chem. Process Des. Dev., 21, 118–127 (1977)",
            "Perry's Chemical Engineers' Handbook"
        ],
        burden_holder="User applying UNIFAC method",
        adversary_position="Group parameters may be missing or inaccurate for novel compounds",
        counter_arguments=[
            "Experimental VLE data or regression of parameters may be necessary for novel systems.",
            "Alternative models (e.g., NRTL, UNIQUAC) may be more accurate for specific systems."
        ],
        resolution_strategy="Use UNIFAC for initial screening and when experimental data is lacking; validate with experiments for critical applications.",
        entity_scope="Non-ideal liquid mixtures, VLE prediction",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Fredenslund et al. (1977); Perry's Handbook"
    ),
    DoctrineBlock(
        topic="Fugacity and Fugacity Coefficient in Phase Equilibria",
        keywords=["fugacity", "fugacity coefficient", "phase equilibria", "thermodynamics", "EOS"],
        conclusion_template="Fugacity and fugacity coefficients are essential for quantifying chemical potential and phase equilibria in real fluids.",
        reasoning_framework=(
            "Fugacity is a corrected pressure that accounts for non-ideality in real gases and liquids, serving as a bridge between the chemical potential and measurable properties. "
            "The fugacity coefficient (φ) is defined as the ratio of fugacity to pressure (φ = f/P). In phase equilibrium, the fugacity of each component must be equal in all coexisting phases. "
            "Fugacity coefficients are calculated using equations of state (e.g., Peng-Robinson, SRK) or activity coefficient models. "
            "They are crucial for accurate phase equilibrium calculations, especially at high pressures or for non-ideal mixtures."
        ),
        key_factors=[
            "Equation of state or activity coefficient model",
            "System pressure and temperature",
            "Component non-ideality",
            "Phase equilibrium conditions"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Prausnitz, J.M., Lichtenthaler, R.N., de Azevedo, E.G."
        ],
        burden_holder="Thermodynamics analyst",
        adversary_position="Ideal gas or Raoult's Law is sufficient for dilute or low-pressure systems",
        counter_arguments=[
            "For ideal gases or dilute solutions, fugacity approaches pressure or mole fraction; corrections are negligible.",
            "At high pressures or for non-ideal systems, fugacity corrections are essential."
        ],
        resolution_strategy="Use fugacity/fugacity coefficients for non-ideal and high-pressure systems; ideal approximations for dilute/low-pressure cases.",
        entity_scope="Phase equilibrium, chemical potential calculations",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="Smith, Van Ness & Abbott; Prausnitz et al."
    ),
    DoctrineBlock(
        topic="Hess's Law and Standard Enthalpy of Reaction",
        keywords=["Hess's Law", "enthalpy of reaction", "thermodynamics", "energy balance"],
        conclusion_template="Hess's Law allows calculation of reaction enthalpy from standard enthalpies of formation, enabling energy balance in chemical processes.",
        reasoning_framework=(
            "Hess's Law states that the enthalpy change of a chemical reaction is independent of the pathway, depending only on the initial and final states. "
            "This allows the calculation of reaction enthalpy (ΔH_rxn) by summing the standard enthalpies of formation (ΔH_f) of products and reactants:\n"
            "ΔH_rxn = Σ ν_products ΔH_f,products - Σ ν_reactants ΔH_f,reactants\n"
            "This principle is fundamental for process energy balances, reactor design, and thermodynamic analysis. "
            "Standard enthalpy values are tabulated for many compounds. For reactions at non-standard conditions, heat capacity corrections may be applied."
        ),
        key_factors=[
            "Standard enthalpies of formation",
            "Stoichiometry of reaction",
            "Temperature corrections (if not at 298 K)",
            "Tabulated thermodynamic data"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Perry's Chemical Engineers' Handbook"
        ],
        burden_holder="Process designer or analyst",
        adversary_position="Direct calorimetric measurement may be required for novel or complex reactions",
        counter_arguments=[
            "For reactions involving unknown compounds, experimental determination may be necessary.",
            "Heat capacity corrections must be included for non-standard conditions."
        ],
        resolution_strategy="Use Hess's Law for standard reactions; supplement with experiments or corrections as needed.",
        entity_scope="Reaction thermodynamics, energy balances",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="Smith, Van Ness & Abbott; Perry's Handbook"
    ),
    DoctrineBlock(
        topic="Second Law Analysis and Entropy Generation",
        keywords=["Second Law", "entropy generation", "irreversibility", "thermodynamics", "process analysis"],
        conclusion_template="Second Law analysis quantifies irreversibility and entropy generation, guiding process optimization for efficiency.",
        reasoning_framework=(
            "The Second Law of Thermodynamics states that entropy of an isolated system increases in any spontaneous process. "
            "Entropy generation quantifies irreversibility in real processes (e.g., heat transfer across finite temperature differences, mixing, friction). "
            "Second Law analysis involves calculating entropy balances for systems and surroundings, identifying sources of inefficiency. "
            "Minimizing entropy generation leads to more efficient processes and reduced exergy destruction. "
            "This analysis is essential in power generation, refrigeration, and chemical process optimization."
        ),
        key_factors=[
            "Process irreversibility",
            "Heat and mass transfer mechanisms",
            "System and surroundings entropy balances",
            "Exergy analysis"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Bejan, A., Advanced Engineering Thermodynamics"
        ],
        burden_holder="Process analyst",
        adversary_position="First Law (energy balance) is sufficient for some analyses",
        counter_arguments=[
            "First Law analysis does not quantify inefficiency or lost work.",
            "Second Law analysis provides deeper insight into process optimization."
        ],
        resolution_strategy="Apply Second Law analysis for process optimization and efficiency improvement.",
        entity_scope="Process design, optimization, energy systems",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Smith, Van Ness & Abbott; Bejan"
    ),
    DoctrineBlock(
        topic="Azeotrope Formation and Breaking Strategies",
        keywords=["azeotrope", "azeotropic distillation", "breaking azeotrope", "VLE", "thermodynamics"],
        conclusion_template="Azeotropes limit separation by distillation; breaking strategies include pressure-swing, entrainer addition, and hybrid processes.",
        reasoning_framework=(
            "An azeotrope is a mixture that boils at a constant composition, making separation by simple distillation impossible. "
            "Azeotropes arise from non-ideal interactions, typically identified by VLE data or activity coefficient models. "
            "Breaking azeotropes can be achieved by:\n"
            "1. Pressure-swing distillation: exploiting pressure dependence of azeotropic composition.\n"
            "2. Adding an entrainer: introducing a third component to alter relative volatilities (azeotropic or extractive distillation).\n"
            "3. Hybrid processes: combining distillation with membrane separation or adsorption.\n"
            "Selection depends on system properties, economics, and safety."
        ),
        key_factors=[
            "Azeotropic composition and pressure dependence",
            "Entrainer selection and compatibility",
            "Process economics and safety",
            "VLE and activity coefficient data"
        ],
        primary_authority=[
            "Perry's Chemical Engineers' Handbook",
            "Seader, J.D., Henley, E.J., Separation Process Principles"
        ],
        burden_holder="Process designer",
        adversary_position="Azeotrope cannot be broken economically or safely",
        counter_arguments=[
            "Alternative separation methods (e.g., pervaporation, adsorption) may be feasible.",
            "Process intensification can improve economics."
        ],
        resolution_strategy="Evaluate all breaking strategies; select based on technical and economic feasibility.",
        entity_scope="Distillation, separation processes",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Perry's Handbook; Seader & Henley"
    ),
    DoctrineBlock(
        topic="Soave-Redlich-Kwong (SRK) Equation of State",
        keywords=["SRK", "Soave-Redlich-Kwong", "equation of state", "thermodynamics", "phase equilibria"],
        conclusion_template="The SRK equation of state is suitable for vapor-liquid equilibrium calculations of hydrocarbons and light gases at moderate pressures.",
        reasoning_framework=(
            "The Soave-Redlich-Kwong (SRK) equation of state is a cubic EOS developed to improve the prediction of vapor-liquid equilibria for hydrocarbons and light gases. "
            "It modifies the attractive term of the Redlich-Kwong EOS with a temperature-dependent function, enhancing accuracy for non-polar and slightly polar compounds. "
            "The SRK EOS is expressed as:\n"
            "P = RT/(V-b) - a(T)/(V(V+b))\n"
            "where a(T) incorporates the acentric factor. The SRK EOS is widely used in natural gas and petroleum industries. "
            "Limitations include reduced accuracy for highly polar or associating compounds."
        ),
        key_factors=[
            "Critical properties and acentric factor",
            "Component polarity",
            "Pressure and temperature range",
            "Mixing rules for mixtures"
        ],
        primary_authority=[
            "Soave, G., Chem. Eng. Sci., 27, 1197–1203 (1972)",
            "Smith, J.M., Van Ness, H.C., Abbott, M.M."
        ],
        burden_holder="User applying SRK EOS",
        adversary_position="SRK EOS is inadequate for polar or associating systems",
        counter_arguments=[
            "Activity coefficient models or advanced EOS may be required for polar systems.",
            "Experimental validation is necessary for complex mixtures."
        ],
        resolution_strategy="Use SRK for hydrocarbons and light gases; validate for other systems.",
        entity_scope="Phase equilibrium, process simulation",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Soave (1972); Smith, Van Ness & Abbott"
    ),
    DoctrineBlock(
        topic="UNIQUAC Activity Coefficient Model",
        keywords=["UNIQUAC", "activity coefficient", "liquid phase", "non-ideal", "thermodynamics"],
        conclusion_template="The UNIQUAC model is recommended for correlating and predicting activity coefficients in non-ideal liquid mixtures, especially for systems with significant size and shape differences.",
        reasoning_framework=(
            "The UNIQUAC (Universal Quasi-Chemical) model is an activity coefficient model that accounts for both entropic (size/shape) and enthalpic (energy) contributions to non-ideality. "
            "It is suitable for a wide range of liquid mixtures, including those with significant molecular size and shape differences. "
            "The model requires binary interaction parameters, typically regressed from experimental VLE data. "
            "UNIQUAC is widely used in process simulation and design, and forms the basis for the UNIFAC group contribution method."
        ),
        key_factors=[
            "Binary interaction parameters",
            "Molecular size and shape differences",
            "Availability of experimental VLE data",
            "Degree of non-ideality"
        ],
        primary_authority=[
            "Abrams, D.S. and Prausnitz, J.M., AIChE J., 21, 116–128 (1975)",
            "Perry's Chemical Engineers' Handbook"
        ],
        burden_holder="User proposing UNIQUAC model",
        adversary_position="UNIQUAC parameters are unavailable or system is highly associating",
        counter_arguments=[
            "NRTL or Wilson models may be preferable for highly associating systems.",
            "Group contribution methods can estimate parameters."
        ],
        resolution_strategy="Use UNIQUAC for systems with significant size/shape differences; validate with experiments.",
        entity_scope="Liquid phase non-ideal mixtures",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Abrams and Prausnitz (1975); Perry's Handbook"
    ),
    DoctrineBlock(
        topic="Wilson Activity Coefficient Model",
        keywords=["Wilson model", "activity coefficient", "liquid phase", "thermodynamics", "non-ideal"],
        conclusion_template="The Wilson model is effective for highly miscible, non-ideal liquid mixtures with complete miscibility and moderate non-ideality.",
        reasoning_framework=(
            "The Wilson model is an activity coefficient model based on local composition theory, suitable for highly miscible liquid mixtures. "
            "It uses binary interaction parameters derived from experimental VLE data. The model assumes complete miscibility and is not applicable to systems with partial miscibility or phase splitting. "
            "It is widely used for hydrocarbon-alcohol and other non-ideal mixtures with moderate deviations from Raoult's Law."
        ),
        key_factors=[
            "Binary interaction parameters",
            "Complete miscibility",
            "Degree of non-ideality",
            "Experimental VLE data"
        ],
        primary_authority=[
            "Wilson, G.M., J. Am. Chem. Soc., 86, 127–130 (1964)",
            "Smith, J.M., Van Ness, H.C., Abbott, M.M."
        ],
        burden_holder="User applying Wilson model",
        adversary_position="Wilson model is not suitable for partially miscible or highly non-ideal systems",
        counter_arguments=[
            "NRTL or UNIQUAC models may be preferable for partially miscible or strongly non-ideal systems.",
            "Wilson model cannot predict phase splitting."
        ],
        resolution_strategy="Use Wilson model for highly miscible, moderately non-ideal mixtures.",
        entity_scope="Liquid phase non-ideal mixtures",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Wilson (1964); Smith, Van Ness & Abbott"
    ),
    DoctrineBlock(
        topic="Virial Equation of State for Moderate Pressures",
        keywords=["Virial equation", "equation of state", "moderate pressure", "thermodynamics", "compressibility"],
        conclusion_template="The Virial equation of state is suitable for describing real gas behavior at moderate pressures, using virial coefficients from experimental or theoretical sources.",
        reasoning_framework=(
            "The Virial equation of state expands the compressibility factor Z as a power series in pressure or inverse molar volume:\n"
            "Z = 1 + B(T)P/RT + C(T)P^2/RT^2 + ...\n"
            "where B(T), C(T), etc. are virial coefficients dependent on temperature and molecular interactions. "
            "The Virial EOS is accurate for gases at low to moderate pressures, where higher-order terms are negligible. "
            "Virial coefficients can be obtained from experimental PVT data or theoretical calculations. "
            "The model is not suitable for high-pressure or liquid-phase systems."
        ),
        key_factors=[
            "Virial coefficients (B, C, ...)",
            "Pressure and temperature range",
            "Nature of gas (non-polar, polar)",
            "Availability of experimental data"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Perry's Chemical Engineers' Handbook"
        ],
        burden_holder="User applying Virial EOS",
        adversary_position="Virial EOS is inadequate for high-pressure or liquid systems",
        counter_arguments=[
            "Cubic equations of state are preferable for high-pressure or liquid-phase calculations.",
            "Virial EOS is limited to moderate pressures."
        ],
        resolution_strategy="Use Virial EOS for real gases at moderate pressures; apply cubic EOS for other conditions.",
        entity_scope="Gas phase, moderate pressure systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Smith, Van Ness & Abbott; Perry's Handbook"
    ),
    DoctrineBlock(
        topic="Bubble Point and Dew Point Calculations",
        keywords=["bubble point", "dew point", "VLE", "thermodynamics", "phase equilibrium"],
        conclusion_template="Bubble point and dew point calculations determine the temperature or pressure at which a mixture begins to boil or condense, essential for distillation and separation processes.",
        reasoning_framework=(
            "Bubble point is the temperature (or pressure) at which the first bubble of vapor forms from a liquid mixture at a given pressure (or temperature). "
            "Dew point is the temperature (or pressure) at which the first drop of liquid condenses from a vapor mixture. "
            "These calculations use Raoult's Law for ideal systems or activity coefficient models/EOS for non-ideal systems. "
            "They are fundamental in distillation design, flash calculations, and phase envelope construction."
        ),
        key_factors=[
            "Mixture composition",
            "Pressure or temperature",
            "Vapor-liquid equilibrium model",
            "Non-ideality corrections"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Perry's Chemical Engineers' Handbook"
        ],
        burden_holder="Process designer or analyst",
        adversary_position="Non-idealities require advanced models for accurate results",
        counter_arguments=[
            "Activity coefficient models or EOS should be used for non-ideal or high-pressure systems.",
            "Raoult's Law is sufficient for ideal mixtures."
        ],
        resolution_strategy="Select appropriate VLE model based on system non-ideality; validate with experimental data.",
        entity_scope="Distillation, separation processes",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Smith, Van Ness & Abbott; Perry's Handbook"
    ),
    DoctrineBlock(
        topic="Excess Gibbs Energy and Excess Properties",
        keywords=["excess Gibbs energy", "excess properties", "non-ideal", "thermodynamics", "activity coefficient"],
        conclusion_template="Excess Gibbs energy quantifies deviation from ideality in mixtures and forms the basis for activity coefficient models.",
        reasoning_framework=(
            "Excess Gibbs energy (G^E) is defined as the difference between the actual Gibbs energy of a mixture and that predicted by an ideal solution at the same conditions. "
            "It quantifies non-ideal interactions and is used to derive activity coefficient models (e.g., NRTL, UNIQUAC, Wilson). "
            "Other excess properties (e.g., excess enthalpy, excess volume) provide additional insight into mixture behavior. "
            "Excess property models are essential for accurate phase equilibrium and property prediction in non-ideal systems."
        ),
        key_factors=[
            "Mixture composition",
            "Temperature and pressure",
            "Non-ideality of components",
            "Model selection for excess properties"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Prausnitz, J.M., Lichtenthaler, R.N., de Azevedo, E.G."
        ],
        burden_holder="Thermodynamics analyst",
        adversary_position="Ideal solution models are sufficient for dilute or regular mixtures",
        counter_arguments=[
            "Excess property models are essential for strongly non-ideal mixtures.",
            "Ideal models are limited to dilute or regular solutions."
        ],
        resolution_strategy="Use excess property models for non-ideal mixtures; validate with experiments.",
        entity_scope="Non-ideal mixtures, phase equilibrium",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Smith, Van Ness & Abbott; Prausnitz et al."
    ),
    DoctrineBlock(
        topic="Supercritical Fluid Thermodynamics and CO2 Applications",
        keywords=["supercritical fluid", "CO2", "thermodynamics", "phase behavior", "extraction"],
        conclusion_template="Supercritical CO2 exhibits unique solvent properties, enabling applications in extraction, reaction, and materials processing.",
        reasoning_framework=(
            "Supercritical fluids (SCFs) are substances above their critical temperature and pressure, exhibiting properties intermediate between liquids and gases. "
            "Supercritical CO2 is widely used due to its moderate critical conditions, non-toxicity, and tunable solvent power. "
            "Applications include extraction (e.g., caffeine, essential oils), reaction media, and materials processing. "
            "Thermodynamic modeling of SCFs requires equations of state (e.g., Peng-Robinson, SAFT) and accurate phase behavior data. "
            "Solubility and density can be manipulated by pressure and temperature, enabling selective separations."
        ),
        key_factors=[
            "Critical properties of CO2",
            "Pressure and temperature control",
            "Solubility and phase behavior",
            "Process safety and economics"
        ],
        primary_authority=[
            "Brunner, G., Supercritical Fluids as Solvents and Reaction Media",
            "Perry's Chemical Engineers' Handbook"
        ],
        burden_holder="Process designer",
        adversary_position="SCF processes may be uneconomical or require specialized equipment",
        counter_arguments=[
            "Process intensification and equipment advances have improved SCF economics.",
            "Alternative solvents may be considered for specific applications."
        ],
        resolution_strategy="Evaluate SCF processes based on technical and economic feasibility.",
        entity_scope="Extraction, reaction, materials processing",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="Brunner; Perry's Handbook"
    ),
    DoctrineBlock(
        topic="Thermodynamic Package Selection in Process Simulation",
        keywords=["thermodynamic package", "process simulation", "model selection", "EOS", "activity coefficient"],
        conclusion_template="Selection of thermodynamic packages should be based on system composition, pressure, temperature, and required accuracy, referencing authoritative guidelines.",
        reasoning_framework=(
            "Thermodynamic package selection is critical for accurate process simulation. "
            "The choice depends on system composition (e.g., hydrocarbons, polar compounds), pressure and temperature range, and the property of interest (e.g., VLE, LLE, SLE). "
            "Guidelines from process simulator vendors (e.g., AspenTech, Honeywell) and literature should be consulted. "
            "Cubic EOS (e.g., Peng-Robinson, SRK) are standard for hydrocarbons; activity coefficient models (e.g., NRTL, UNIQUAC) are preferred for polar or non-ideal systems. "
            "Hybrid models or user-defined packages may be necessary for complex systems."
        ),
        key_factors=[
            "System composition",
            "Pressure and temperature range",
            "Phase behavior and property of interest",
            "Model availability and validation"
        ],
        primary_authority=[
            "AspenTech Documentation",
            "Perry's Chemical Engineers' Handbook"
        ],
        burden_holder="Process simulation engineer",
        adversary_position="Default package selection may be inadequate for complex systems",
        counter_arguments=[
            "Custom or hybrid models may be required for unique systems.",
            "Experimental validation is essential for critical applications."
        ],
        resolution_strategy="Follow authoritative guidelines; validate package selection with experimental data.",
        entity_scope="Process simulation, design, optimization",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AspenTech; Perry's Handbook"
    ),
    DoctrineBlock(
        topic="GERG-2008 Equation of State for Natural Gas",
        keywords=["GERG-2008", "equation of state", "natural gas", "thermodynamics", "mixtures"],
        conclusion_template="The GERG-2008 EOS is the reference standard for accurate thermodynamic property prediction of natural gas mixtures.",
        reasoning_framework=(
            "The GERG-2008 equation of state is a multi-parameter, reference-quality EOS for natural gas and related mixtures. "
            "It provides highly accurate predictions of density, speed of sound, calorific value, and other properties over a wide range of conditions. "
            "GERG-2008 is used by industry and metrology institutes for custody transfer, process design, and quality control. "
            "Implementation requires detailed compositional analysis and specialized software."
        ),
        key_factors=[
            "Detailed gas composition",
            "Pressure and temperature range",
            "Required property accuracy",
            "Software implementation"
        ],
        primary_authority=[
            "Kunz, O. and Wagner, W., GERG-2008 EOS for Natural Gases",
            "International Organization for Standardization (ISO 20765-2:2015)"
        ],
        burden_holder="Natural gas analyst or operator",
        adversary_position="Simpler EOS may be sufficient for preliminary calculations",
        counter_arguments=[
            "Cubic EOS may be used for screening or non-critical applications.",
            "GERG-2008 is necessary for custody transfer and metrology."
        ],
        resolution_strategy="Use GERG-2008 for high-accuracy applications; cubic EOS for preliminary work.",
        entity_scope="Natural gas industry, custody transfer",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="Kunz & Wagner; ISO 20765-2"
    ),
    DoctrineBlock(
        topic="Le Chatelier's Principle and Reaction Equilibrium Shifts",
        keywords=["Le Chatelier", "reaction equilibrium", "thermodynamics", "shifts", "process control"],
        conclusion_template="Le Chatelier's Principle predicts the direction of equilibrium shift in response to changes in temperature, pressure, or composition.",
        reasoning_framework=(
            "Le Chatelier's Principle states that a system at equilibrium will adjust to counteract imposed changes in temperature, pressure, or composition. "
            "For exothermic reactions, increasing temperature shifts equilibrium to reactants; for endothermic, to products. "
            "Increasing pressure favors the side with fewer moles of gas. "
            "This principle guides process control and optimization in reactors and separation units."
        ),
        key_factors=[
            "Reaction enthalpy (exothermic/endothermic)",
            "Change in moles of gas",
            "Temperature and pressure changes",
            "System constraints"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Le Chatelier, H., Annales des Mines, 13, 157–165 (1884)"
        ],
        burden_holder="Process operator or designer",
        adversary_position="Kinetic limitations may prevent equilibrium shift",
        counter_arguments=[
            "Reaction kinetics may limit the extent of equilibrium shift.",
            "Catalysts or alternative process conditions may be required."
        ],
        resolution_strategy="Consider both thermodynamics and kinetics in process design.",
        entity_scope="Reaction engineering, process control",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Smith, Van Ness & Abbott; Le Chatelier"
    ),
    DoctrineBlock(
        topic="Activity and Activity Coefficient in Non-Ideal Solutions",
        keywords=["activity", "activity coefficient", "non-ideal solution", "thermodynamics", "phase equilibrium"],
        conclusion_template="Activity and activity coefficients quantify deviations from ideality in solutions, essential for accurate phase and reaction equilibrium calculations.",
        reasoning_framework=(
            "Activity (a) is the effective concentration of a species in a non-ideal solution, defined as a = γx, where γ is the activity coefficient and x is the mole fraction. "
            "Activity coefficients account for non-ideal interactions and are determined from experimental data or predictive models (e.g., NRTL, UNIQUAC, UNIFAC). "
            "Accurate calculation of activities is essential for phase equilibrium, reaction equilibrium, and electrochemical systems."
        ),
        key_factors=[
            "Non-ideality of solution",
            "Model selection for activity coefficients",
            "Experimental data availability",
            "Application (phase or reaction equilibrium)"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Prausnitz, J.M., Lichtenthaler, R.N., de Azevedo, E.G."
        ],
        burden_holder="Thermodynamics analyst",
        adversary_position="Ideal solution models are sufficient for dilute or regular mixtures",
        counter_arguments=[
            "Non-ideal models are necessary for strongly interacting systems.",
            "Ideal models are limited in scope."
        ],
        resolution_strategy="Use activity coefficient models for non-ideal solutions; validate with experiments.",
        entity_scope="Non-ideal solutions, phase and reaction equilibrium",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Smith, Van Ness & Abbott; Prausnitz et al."
    ),
    DoctrineBlock(
        topic="van der Waals Mixing Rules in Equation of State",
        keywords=["van der Waals", "mixing rules", "equation of state", "thermodynamics", "mixtures"],
        conclusion_template="van der Waals mixing rules are standard for combining pure component parameters in cubic equations of state for mixtures.",
        reasoning_framework=(
            "van der Waals mixing rules are used to extend cubic equations of state (e.g., Peng-Robinson, SRK) to mixtures. "
            "The rules combine pure component parameters (a, b) using mole fractions and binary interaction parameters (kij):\n"
            "a_mix = ΣΣ xi xj (aij), where aij = sqrt(ai aj)(1 - kij)\n"
            "b_mix = Σ xi bi\n"
            "Binary interaction parameters are regressed from experimental data. "
            "These rules are widely used in process simulation and phase equilibrium calculations."
        ),
        key_factors=[
            "Pure component parameters (a, b)",
            "Binary interaction parameters (kij)",
            "Mixture composition",
            "Availability of experimental data"
        ],
        primary_authority=[
            "van der Waals, J.D., Nobel Lecture (1910)",
            "Smith, J.M., Van Ness, H.C., Abbott, M.M."
        ],
        burden_holder="User applying cubic EOS to mixtures",
        adversary_position="Advanced mixing rules may improve accuracy for complex mixtures",
        counter_arguments=[
            "Advanced mixing rules (e.g., Wong-Sandler) may be needed for highly non-ideal mixtures.",
            "van der Waals rules are standard for most applications."
        ],
        resolution_strategy="Use van der Waals mixing rules for standard mixtures; consider advanced rules for complex systems.",
        entity_scope="Mixture phase equilibrium, process simulation",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="van der Waals; Smith, Van Ness & Abbott"
    ),
    DoctrineBlock(
        topic="Joule-Thomson Effect and Coefficient",
        keywords=["Joule-Thomson effect", "Joule-Thomson coefficient", "thermodynamics", "gas expansion", "cooling"],
        conclusion_template="The Joule-Thomson effect describes temperature change during isenthalpic expansion of a real gas; the coefficient determines cooling or heating direction.",
        reasoning_framework=(
            "The Joule-Thomson effect is the temperature change observed when a real gas expands isenthalpically (constant enthalpy) through a valve or porous plug. "
            "The Joule-Thomson coefficient (μJT) is defined as (∂T/∂P)_H. "
            "For most gases at room temperature, μJT is positive (cooling upon expansion), but can be negative for some gases or at high temperatures. "
            "The inversion temperature separates cooling and heating behavior. "
            "The effect is exploited in gas liquefaction and refrigeration processes."
        ),
        key_factors=[
            "Gas type and initial conditions",
            "Joule-Thomson coefficient",
            "Inversion temperature",
            "Process constraints"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Perry's Chemical Engineers' Handbook"
        ],
        burden_holder="Process designer",
        adversary_position="Ideal gases do not exhibit the Joule-Thomson effect",
        counter_arguments=[
            "The effect is negligible for ideal gases; significant only for real gases.",
            "Process design must consider real gas behavior."
        ],
        resolution_strategy="Apply Joule-Thomson analysis for real gases in expansion/cooling processes.",
        entity_scope="Gas processing, refrigeration",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Smith, Van Ness & Abbott; Perry's Handbook"
    ),
    DoctrineBlock(
        topic="Critical Point and Critical Phenomena",
        keywords=["critical point", "critical phenomena", "thermodynamics", "phase behavior", "supercritical"],
        conclusion_template="The critical point defines the temperature and pressure above which distinct liquid and vapor phases do not exist; critical phenomena influence phase behavior and process design.",
        reasoning_framework=(
            "The critical point is the unique combination of temperature and pressure at which the properties of liquid and vapor phases become identical. "
            "Above the critical point, the substance exists as a supercritical fluid with unique properties. "
            "Critical phenomena include large density fluctuations and opalescence near the critical point. "
            "Knowledge of critical properties is essential for phase equilibrium modeling, equipment design, and supercritical fluid applications."
        ),
        key_factors=[
            "Critical temperature and pressure",
            "Phase behavior near critical point",
            "Supercritical fluid properties",
            "Process safety and design"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Prausnitz, J.M., Lichtenthaler, R.N., de Azevedo, E.G."
        ],
        burden_holder="Process designer or analyst",
        adversary_position="Critical phenomena complicate process control near critical conditions",
        counter_arguments=[
            "Process design should avoid operation near critical point unless necessary.",
            "Advanced models are required for accurate prediction near critical conditions."
        ],
        resolution_strategy="Use accurate models and safety margins near critical point.",
        entity_scope="Phase equilibrium, process design",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Smith, Van Ness & Abbott; Prausnitz et al."
    ),
    # Additional doctrines for a total of 40+
    DoctrineBlock(
        topic="Electrolyte Thermodynamics and Pitzer Model",
        keywords=["electrolyte", "Pitzer model", "thermodynamics", "activity coefficient", "salts"],
        conclusion_template="The Pitzer model is recommended for calculating activity coefficients in concentrated electrolyte solutions.",
        reasoning_framework=(
            "The Pitzer model extends Debye-Hückel theory to concentrated electrolyte solutions, accounting for ion-ion and ion-solvent interactions. "
            "It uses virial expansions and empirical parameters regressed from experimental data. "
            "The model is widely used for brines, seawater, and industrial salt solutions where dilute approximations fail. "
            "Limitations include parameter availability and complexity for multicomponent systems."
        ),
        key_factors=[
            "Electrolyte concentration",
            "Availability of Pitzer parameters",
            "Temperature and ionic strength",
            "Experimental data"
        ],
        primary_authority=[
            "Pitzer, K.S., Activity Coefficients in Electrolyte Solutions",
            "Perry's Chemical Engineers' Handbook"
        ],
        burden_holder="Analyst modeling electrolyte systems",
        adversary_position="Pitzer parameters may be unavailable for novel salts",
        counter_arguments=[
            "Alternative models (e.g., Bromley, eNRTL) may be used.",
            "Experimental parameter regression may be required."
        ],
        resolution_strategy="Use Pitzer model for concentrated electrolytes; validate or regress parameters as needed.",
        entity_scope="Electrolyte solutions, brines",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="Pitzer; Perry's Handbook"
    ),
    DoctrineBlock(
        topic="Henry's Law in Dilute Solutions",
        keywords=["Henry's Law", "dilute solution", "thermodynamics", "gas solubility", "phase equilibrium"],
        conclusion_template="Henry's Law is valid for dilute solutions, relating the solubility of a gas to its partial pressure above the solution.",
        reasoning_framework=(
            "Henry's Law states that the solubility of a gas in a liquid at low concentration is proportional to its partial pressure above the solution: "
            "C = kH * P, where kH is the Henry's Law constant. "
            "The law is valid for dilute solutions and low pressures. "
            "Deviations occur at higher concentrations or for strongly interacting solutes."
        ),
        key_factors=[
            "Dilute solution assumption",
            "Henry's Law constant",
            "Temperature dependence",
            "Gas-liquid interactions"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Perry's Chemical Engineers' Handbook"
        ],
        burden_holder="Analyst applying Henry's Law",
        adversary_position="Non-ideality or high concentration invalidates Henry's Law",
        counter_arguments=[
            "Activity coefficient corrections may be required for non-ideal systems.",
            "Raoult's Law or other models may apply at higher concentrations."
        ],
        resolution_strategy="Apply Henry's Law for dilute solutions; use corrections for non-ideal or concentrated systems.",
        entity_scope="Dilute solutions, gas solubility",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Smith, Van Ness & Abbott; Perry's Handbook"
    ),
    DoctrineBlock(
        topic="Clapeyron Equation and Phase Transitions",
        keywords=["Clapeyron equation", "phase transition", "thermodynamics", "vapor pressure", "latent heat"],
        conclusion_template="The Clapeyron equation relates the slope of the phase boundary to enthalpy and volume changes during phase transitions.",
        reasoning_framework=(
            "The Clapeyron equation is a fundamental thermodynamic relationship describing the slope of the coexistence curve between two phases:\n"
            "dP/dT = ΔH/ (TΔV)\n"
            "where ΔH is the latent heat and ΔV is the volume change. "
            "It is used to estimate vapor pressure curves, melting points, and other phase transition properties. "
            "The equation assumes equilibrium and reversible transitions."
        ),
        key_factors=[
            "Latent heat of transition",
            "Volume change between phases",
            "Temperature and pressure",
            "Equilibrium conditions"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Perry's Chemical Engineers' Handbook"
        ],
        burden_holder="Thermodynamics analyst",
        adversary_position="Non-equilibrium or rapid transitions may not follow Clapeyron equation",
        counter_arguments=[
            "The equation is valid only for equilibrium, reversible transitions.",
            "Kinetic effects must be considered for rapid processes."
        ],
        resolution_strategy="Apply Clapeyron equation for equilibrium phase transitions.",
        entity_scope="Phase transitions, vapor pressure estimation",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Smith, Van Ness & Abbott; Perry's Handbook"
    ),
    DoctrineBlock(
        topic="Raoult's Law for Ideal Solutions",
        keywords=["Raoult's Law", "ideal solution", "thermodynamics", "vapor-liquid equilibrium", "phase equilibrium"],
        conclusion_template="Raoult's Law applies to ideal solutions, relating partial vapor pressures to mole fractions and pure component vapor pressures.",
        reasoning_framework=(
            "Raoult's Law states that the partial pressure of each component in an ideal solution is equal to the product of its mole fraction and its pure component vapor pressure: "
            "Pi = xi * Pi^sat. "
            "The law is valid for ideal or nearly ideal mixtures, typically of chemically similar components. "
            "Deviations from Raoult's Law are addressed using activity coefficients."
        ),
        key_factors=[
            "Ideal solution assumption",
            "Mole fractions",
            "Pure component vapor pressures",
            "Temperature"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Perry's Chemical Engineers' Handbook"
        ],
        burden_holder="Analyst applying Raoult's Law",
        adversary_position="Non-ideal mixtures require activity coefficient corrections",
        counter_arguments=[
            "Activity coefficient models should be used for non-ideal mixtures.",
            "Raoult's Law is a limiting case."
        ],
        resolution_strategy="Apply Raoult's Law for ideal mixtures; use corrections for non-ideal systems.",
        entity_scope="Ideal solutions, VLE calculations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Smith, Van Ness & Abbott; Perry's Handbook"
    ),
    DoctrineBlock(
        topic="Antoine Equation for Vapor Pressure Correlation",
        keywords=["Antoine equation", "vapor pressure", "correlation", "thermodynamics", "phase equilibrium"],
        conclusion_template="The Antoine equation is a widely used empirical correlation for vapor pressure as a function of temperature.",
        reasoning_framework=(
            "The Antoine equation is an empirical relationship used to correlate vapor pressure data for pure substances:\n"
            "log10(P) = A - B/(C + T)\n"
            "where P is vapor pressure, T is temperature, and A, B, C are substance-specific constants. "
            "The equation provides accurate vapor pressure predictions over moderate temperature ranges. "
            "Constants are tabulated for many compounds."
        ),
        key_factors=[
            "Antoine constants (A, B, C)",
            "Temperature range",
            "Substance identity",
            "Data source"
        ],
        primary_authority=[
            "Perry's Chemical Engineers' Handbook",
            "Smith, J.M., Van Ness, H.C., Abbott, M.M."
        ],
        burden_holder="Analyst correlating vapor pressure data",
        adversary_position="Extrapolation outside data range leads to errors",
        counter_arguments=[
            "Use alternative correlations (e.g., Wagner equation) for wide temperature ranges.",
            "Experimental data should be used for critical applications."
        ],
        resolution_strategy="Use Antoine equation within validated temperature range.",
        entity_scope="Vapor pressure estimation, phase equilibrium",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Perry's Handbook; Smith, Van Ness & Abbott"
    ),
    DoctrineBlock(
        topic="Heat of Mixing and Enthalpy Models",
        keywords=["heat of mixing", "enthalpy", "thermodynamics", "non-ideal mixtures", "excess enthalpy"],
        conclusion_template="Heat of mixing quantifies enthalpy change upon mixing; excess enthalpy models are used for non-ideal mixtures.",
        reasoning_framework=(
            "Heat of mixing is the enthalpy change when pure components are mixed at constant temperature and pressure. "
            "For ideal solutions, heat of mixing is zero; for non-ideal mixtures, it is quantified by excess enthalpy (H^E). "
            "Excess enthalpy models (e.g., NRTL, UNIQUAC) are used to predict or correlate data. "
            "Knowledge of heat of mixing is important for reactor design, safety, and process optimization."
        ),
        key_factors=[
            "Mixture composition",
            "Temperature and pressure",
            "Non-ideality",
            "Model selection"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Prausnitz, J.M., Lichtenthaler, R.N., de Azevedo, E.G."
        ],
        burden_holder="Process designer",
        adversary_position="Experimental data may be required for complex systems",
        counter_arguments=[
            "Model predictions should be validated with experiments.",
            "Advanced models may be needed for highly non-ideal mixtures."
        ],
        resolution_strategy="Use enthalpy models for non-ideal mixtures; validate with data.",
        entity_scope="Mixing, reactor design, process safety",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Smith, Van Ness & Abbott; Prausnitz et al."
    ),
    DoctrineBlock(
        topic="Partial Molar Properties and Their Determination",
        keywords=["partial molar property", "thermodynamics", "solution", "Gibbs-Duhem", "excess property"],
        conclusion_template="Partial molar properties describe the change in an extensive property upon addition of an infinitesimal amount of a component to a mixture.",
        reasoning_framework=(
            "Partial molar properties (e.g., partial molar volume, enthalpy, Gibbs energy) are defined as the change in a system's extensive property when an infinitesimal amount of a component is added, at constant T, P, and composition of other components. "
            "They are determined experimentally (e.g., by measuring solution properties as a function of composition) or calculated from models. "
            "The Gibbs-Duhem equation relates partial molar properties of all components in a mixture."
        ),
        key_factors=[
            "Mixture composition",
            "Measurement or model",
            "Gibbs-Duhem relation",
            "Thermodynamic consistency"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Prausnitz, J.M., Lichtenthaler, R.N., de Azevedo, E.G."
        ],
        burden_holder="Thermodynamics analyst",
        adversary_position="Direct measurement may be challenging for some properties",
        counter_arguments=[
            "Model-based estimation can supplement experimental data.",
            "Thermodynamic consistency checks are essential."
        ],
        resolution_strategy="Combine experimental and model-based approaches for partial molar properties.",
        entity_scope="Solution thermodynamics, property estimation",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Smith, Van Ness & Abbott; Prausnitz et al."
    ),
    DoctrineBlock(
        topic="Retrograde Condensation in Multicomponent Systems",
        keywords=["retrograde condensation", "multicomponent", "phase behavior", "thermodynamics", "natural gas"],
        conclusion_template="Retrograde condensation occurs in multicomponent systems when cooling or depressurizing leads to vaporization rather than condensation.",
        reasoning_framework=(
            "Retrograde condensation is a phenomenon observed in multicomponent mixtures (e.g., natural gas) where, upon cooling or depressurizing, "
            "the system transitions from a two-phase region to a single vapor phase, contrary to typical condensation behavior. "
            "This occurs due to the complex interplay of component volatilities and is predicted by phase envelopes calculated from equations of state."
        ),
        key_factors=[
            "Mixture composition",
            "Pressure and temperature path",
            "Phase envelope calculation",
            "EOS selection"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Perry's Chemical Engineers' Handbook"
        ],
        burden_holder="Process engineer",
        adversary_position="Conventional condensation models may not predict retrograde behavior",
        counter_arguments=[
            "Accurate phase envelope calculation is essential.",
            "Experimental validation may be required for critical applications."
        ],
        resolution_strategy="Use EOS-based phase envelope calculations for multicomponent systems.",
        entity_scope="Natural gas processing, phase behavior",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Smith, Van Ness & Abbott; Perry's Handbook"
    ),
    DoctrineBlock(
        topic="Flash Point and Flammability Limits",
        keywords=["flash point", "flammability", "thermodynamics", "safety", "process design"],
        conclusion_template="Flash point and flammability limits are critical safety parameters, determined experimentally or by correlation, for process design and hazard analysis.",
        reasoning_framework=(
            "Flash point is the lowest temperature at which a liquid produces enough vapor to form an ignitable mixture with air. "
            "Flammability limits define the concentration range over which vapors are flammable. "
            "These properties are determined experimentally or estimated using correlations. "
            "They are essential for process safety, storage, and transportation of chemicals."
        ),
        key_factors=[
            "Chemical identity",
            "Experimental data",
            "Temperature and pressure",
            "Process safety requirements"
        ],
        primary_authority=[
            "Perry's Chemical Engineers' Handbook",
            "NFPA (National Fire Protection Association) Standards"
        ],
        burden_holder="Process safety engineer",
        adversary_position="Correlations may be inaccurate for complex mixtures",
        counter_arguments=[
            "Experimental determination is preferred for critical applications.",
            "Conservative design margins should be used."
        ],
        resolution_strategy="Use experimental data or validated correlations for safety-critical parameters.",
        entity_scope="Process safety, hazard analysis",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Perry's Handbook; NFPA Standards"
    ),
    DoctrineBlock(
        topic="Colligative Properties and Solution Behavior",
        keywords=["colligative properties", "solution", "thermodynamics", "boiling point elevation", "freezing point depression"],
        conclusion_template="Colligative properties depend on solute concentration, not identity, and are used to estimate boiling point elevation, freezing point depression, and osmotic pressure.",
        reasoning_framework=(
            "Colligative properties are solution properties that depend only on the number of solute particles, not their identity. "
            "Examples include boiling point elevation, freezing point depression, and osmotic pressure. "
            "These properties are predicted using ideal solution theory and are used in process design, food, and pharmaceutical industries."
        ),
        key_factors=[
            "Solute concentration",
            "Ideal solution assumption",
            "Temperature",
            "Application (e.g., food, pharma)"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Perry's Chemical Engineers' Handbook"
        ],
        burden_holder="Process designer",
        adversary_position="Non-idealities may affect colligative property predictions",
        counter_arguments=[
            "Activity coefficient corrections may be required for non-ideal solutions.",
            "Experimental validation is important for critical processes."
        ],
        resolution_strategy="Apply ideal theory for dilute solutions; use corrections as needed.",
        entity_scope="Solution thermodynamics, process design",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Smith, Van Ness & Abbott; Perry's Handbook"
    ),
    DoctrineBlock(
        topic="Thermodynamic Consistency Tests for VLE Data",
        keywords=["thermodynamic consistency", "VLE data", "Gibbs-Duhem", "phase equilibrium", "data validation"],
        conclusion_template="Thermodynamic consistency tests (e.g., Gibbs-Duhem integration) are essential for validating experimental VLE data.",
        reasoning_framework=(
            "Thermodynamic consistency tests, such as the Gibbs-Duhem integration, are used to assess the reliability of experimental VLE data. "
            "Consistent data sets satisfy the Gibbs-Duhem equation within experimental error. "
            "Inconsistent data may indicate experimental errors or non-equilibrium conditions. "
            "Consistency testing is a prerequisite for parameter regression and model development."
        ),
        key_factors=[
            "Experimental VLE data quality",
            "Gibbs-Duhem equation",
            "Data analysis techniques",
            "Model regression"
        ],
        primary_authority=[
            "Prausnitz, J.M., Lichtenthaler, R.N., de Azevedo, E.G.",
            "Smith, J.M., Van Ness, H.C., Abbott, M.M."
        ],
        burden_holder="Data analyst",
        adversary_position="Experimental uncertainty may mask inconsistency",
        counter_arguments=[
            "Statistical analysis should accompany consistency tests.",
            "Experimental replication may be necessary."
        ],
        resolution_strategy="Apply consistency tests and statistical analysis to VLE data.",
        entity_scope="Phase equilibrium, data validation",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Prausnitz et al.; Smith, Van Ness & Abbott"
    ),
    DoctrineBlock(
        topic="Thermodynamic Cycles and Process Efficiency",
        keywords=["thermodynamic cycle", "process efficiency", "Carnot cycle", "Rankine cycle", "thermodynamics"],
        conclusion_template="Thermodynamic cycles (e.g., Carnot, Rankine) provide benchmarks for process efficiency and guide power and refrigeration system design.",
        reasoning_framework=(
            "Thermodynamic cycles are sequences of processes that return a system to its initial state, used to model engines, power plants, and refrigeration systems. "
            "The Carnot cycle defines the theoretical maximum efficiency between two temperature reservoirs. "
            "The Rankine cycle is the standard for steam power plants. "
            "Real cycles are less efficient due to irreversibility and losses. "
            "Cycle analysis guides process optimization and equipment selection."
        ),
        key_factors=[
            "Cycle type (Carnot, Rankine, etc.)",
            "Temperature limits",
            "Irreversibility and losses",
            "Process application"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Bejan, A., Advanced Engineering Thermodynamics"
        ],
        burden_holder="Process designer",
        adversary_position="Real cycles deviate from ideal due to irreversibility",
        counter_arguments=[
            "Second Law analysis quantifies deviations.",
            "Process improvements can reduce losses."
        ],
        resolution_strategy="Use ideal cycles as benchmarks; optimize real processes for efficiency.",
        entity_scope="Power generation, refrigeration, process design",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Smith, Van Ness & Abbott; Bejan"
    ),
    DoctrineBlock(
        topic="Phase Rule and Degrees of Freedom",
        keywords=["phase rule", "degrees of freedom", "Gibbs phase rule", "thermodynamics", "phase equilibrium"],
        conclusion_template="The Gibbs phase rule determines the number of independent variables (degrees of freedom) in a multiphase, multicomponent system.",
        reasoning_framework=(
            "The Gibbs phase rule is given by F = C - P + 2, where F is the degrees of freedom, C is the number of components, and P is the number of phases. "
            "It specifies how many intensive variables (e.g., temperature, pressure, composition) can be independently varied without changing the number of phases. "
            "The rule is fundamental for phase diagram construction and process design."
        ),
        key_factors=[
            "Number of components",
            "Number of phases",
            "System constraints",
            "Phase equilibrium conditions"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Perry's Chemical Engineers' Handbook"
        ],
        burden_holder="Process designer or analyst",
        adversary_position="Non-equilibrium or reactive systems may not follow the phase rule",
        counter_arguments=[
            "The rule applies only to equilibrium, non-reactive systems.",
            "Additional constraints may reduce degrees of freedom."
        ],
        resolution_strategy="Apply phase rule for equilibrium systems; adjust for constraints.",
        entity_scope="Phase equilibrium, process design",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Smith, Van Ness & Abbott; Perry's Handbook"
    ),
    DoctrineBlock(
        topic="Latent Heat and Enthalpy of Phase Change",
        keywords=["latent heat", "enthalpy", "phase change", "thermodynamics", "vaporization"],
        conclusion_template="Latent heat is the enthalpy change associated with phase transitions, essential for energy balances and process design.",
        reasoning_framework=(
            "Latent heat is the energy required for a substance to change phase at constant temperature and pressure (e.g., vaporization, fusion, sublimation). "
            "It is a key parameter in energy balances, distillation, evaporation, and refrigeration processes. "
            "Latent heats are determined experimentally or estimated by correlations (e.g., Watson correlation)."
        ),
        key_factors=[
            "Phase transition type",
            "Temperature and pressure",
            "Experimental data or correlations",
            "Process application"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Perry's Chemical Engineers' Handbook"
        ],
        burden_holder="Process designer",
        adversary_position="Correlations may be inaccurate for complex substances",
        counter_arguments=[
            "Experimental data is preferred for critical applications.",
            "Validated correlations should be used within their range."
        ],
        resolution_strategy="Use experimental or validated correlation data for latent heat.",
        entity_scope="Phase change processes, energy balances",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Smith, Van Ness & Abbott; Perry's Handbook"
    ),
    DoctrineBlock(
        topic="Thermodynamic Property Estimation Methods",
        keywords=["property estimation", "thermodynamics", "correlations", "group contribution", "process simulation"],
        conclusion_template="Thermodynamic properties are estimated using empirical correlations, group contribution methods, or equations of state when experimental data is unavailable.",
        reasoning_framework=(
            "Thermodynamic property estimation is essential when experimental data is lacking. "
            "Empirical correlations (e.g., DIPPR, API), group contribution methods (e.g., UNIFAC, Joback), and equations of state are commonly used. "
            "Selection depends on property, compound type, and required accuracy. "
            "Estimates should be validated with experimental data when possible."
        ),
        key_factors=[
            "Property of interest",
            "Compound type",
            "Model or correlation availability",
            "Validation with data"
        ],
        primary_authority=[
            "Perry's Chemical Engineers' Handbook",
            "DIPPR Project 801 Database"
        ],
        burden_holder="Process designer or analyst",
        adversary_position="Estimates may be inaccurate for novel or complex compounds",
        counter_arguments=[
            "Experimental measurement is preferred for critical applications.",
            "Multiple estimation methods can improve reliability."
        ],
        resolution_strategy="Use validated estimation methods; confirm with data.",
        entity_scope="Process simulation, property estimation",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Perry's Handbook; DIPPR"
    ),
    DoctrineBlock(
        topic="Enthalpy-Entropy Diagrams and Process Analysis",
        keywords=["enthalpy-entropy diagram", "Mollier diagram", "process analysis", "thermodynamics", "energy balance"],
        conclusion_template="Enthalpy-entropy (h-s) diagrams are valuable tools for visualizing thermodynamic processes and performing energy and exergy analyses.",
        reasoning_framework=(
            "Enthalpy-entropy (h-s) diagrams, also known as Mollier diagrams, plot enthalpy versus entropy for a substance. "
            "They are widely used in power and refrigeration cycles to visualize process paths, identify state points, and calculate work and heat transfer. "
            "Diagrams are available for water/steam, refrigerants, and other common fluids."
        ),
        key_factors=[
            "Substance identity",
            "Process path",
            "Diagram accuracy",
            "Application (power, refrigeration)"
        ],
        primary_authority=[
            "Perry's Chemical Engineers' Handbook",
            "Smith, J.M., Van Ness, H.C., Abbott, M.M."
        ],
        burden_holder="Process analyst",
        adversary_position="Diagrams may be unavailable for novel substances",
        counter_arguments=[
            "Property tables or equations of state can supplement diagrams.",
            "Custom diagrams can be generated from models."
        ],
        resolution_strategy="Use h-s diagrams or property tables for process analysis.",
        entity_scope="Power and refrigeration cycles, process analysis",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Perry's Handbook; Smith, Van Ness & Abbott"
    ),
    DoctrineBlock(
        topic="Equilibrium Constant and Temperature Dependence",
        keywords=["equilibrium constant", "temperature dependence", "thermodynamics", "van't Hoff equation", "reaction equilibrium"],
        conclusion_template="The equilibrium constant varies with temperature according to the van't Hoff equation, reflecting the enthalpy change of reaction.",
        reasoning_framework=(
            "The equilibrium constant (K) for a chemical reaction depends on temperature, as described by the van't Hoff equation:\n"
            "d(ln K)/dT = ΔH°/RT^2\n"
            "where ΔH° is the standard enthalpy change. "
            "This relationship allows prediction of equilibrium shifts with temperature changes, essential for reactor design and optimization."
        ),
        key_factors=[
            "Standard enthalpy change",
            "Temperature",
            "van't Hoff equation",
            "Reaction type"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Perry's Chemical Engineers' Handbook"
        ],
        burden_holder="Reaction engineer",
        adversary_position="Non-idealities or complex reactions may require advanced models",
        counter_arguments=[
            "van't Hoff equation assumes constant enthalpy; corrections may be needed for temperature-dependent enthalpy.",
            "Non-idealities should be considered for real systems."
        ],
        resolution_strategy="Use van't Hoff equation for temperature dependence; apply corrections as needed.",
        entity_scope="Reaction equilibrium, reactor design",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Smith, Van Ness & Abbott; Perry's Handbook"
    ),
    DoctrineBlock(
        topic="Thermodynamic Integration and Path Functions",
        keywords=["thermodynamic integration", "path function", "state function", "thermodynamics", "energy calculation"],
        conclusion_template="Thermodynamic integration is used to calculate changes in state functions along a specified path, essential for energy and entropy calculations.",
        reasoning_framework=(
            "Thermodynamic integration involves calculating the change in a state function (e.g., enthalpy, entropy) by integrating a path-dependent differential (e.g., dQ/T, PdV) along a process path. "
            "This is essential for processes where direct measurement is impractical. "
            "Path functions (work, heat) depend on the process path, while state functions depend only on initial and final states."
        ),
        key_factors=[
            "Process path",
            "State and path functions",
            "Integration limits",
            "Measurement or model"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M.",
            "Perry's Chemical Engineers' Handbook"
        ],
        burden_holder="Process analyst",
        adversary_position="Integration may be complex for real processes",
        counter_arguments=[
            "Numerical integration and simulation tools can be used.",
            "Simplified models may be applied for approximate calculations."
        ],
        resolution_strategy="Apply thermodynamic integration for accurate energy and entropy calculations.",
        entity_scope="Process analysis, energy and entropy calculations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Smith, Van Ness & Abbott; Perry's Handbook"
    ),
    DoctrineBlock(
        topic="Vapor-Liquid-Liquid Equilibrium (VLLE) Modeling",
        keywords=["VLLE", "vapor-liquid-liquid equilibrium", "thermodynamics", "phase behavior", "multiphase"],
        conclusion_template="VLLE modeling requires simultaneous solution of phase equilibrium equations for all coexisting phases, using activity coefficient and EOS models.",
        reasoning_framework=(
            "Vapor-liquid-liquid equilibrium (VLLE) occurs when a system separates into two immiscible liquid phases and a vapor phase. "
            "Modeling requires the equality of chemical potentials (or fugacities) for each component in all phases. "
            "Activity coefficient models (e.g., NRTL, UNIQUAC) are used for liquid phases, and equations of state for the vapor phase. "
            "Simultaneous solution is performed using iterative numerical methods."
        ),
        key_factors=[
            "Mixture composition",
            "Phase equilibrium models",
            "Numerical solution methods",
            "Experimental validation"
        ],
        primary_authority=[
            "Prausnitz, J.M., Lichtenthaler, R.N., de Azevedo, E.G.",
            "Perry's Chemical Engineers' Handbook"
        ],
        burden_holder="Process designer or analyst",
        adversary_position="VLLE modeling is complex and may lack reliable parameters",
        counter_arguments=[
            "Experimental data is essential for model validation.",
            "Simplified models may be used for screening."
        ],
        resolution_strategy="Use validated models and data for VLLE calculations.",
        entity_scope="Multiphase equilibrium, process design",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Prausnitz et al.; Perry's Handbook"
    ),
    DoctrineBlock(
        topic="Thermodynamic Stability and Spinodal Decomposition",
        keywords=["thermodynamic stability", "spinodal decomposition", "phase separation", "thermodynamics