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
        topic="First Law of Thermodynamics",
        keywords=["energy conservation", "internal energy", "work", "heat", "thermodynamics"],
        conclusion_template="The total energy of an isolated system is conserved; ΔU = q + w.",
        reasoning_framework="""
        The First Law of Thermodynamics states that energy can neither be created nor destroyed, only transformed. 
        For any process in a closed system, the change in internal energy (ΔU) is equal to the heat (q) added to the system 
        plus the work (w) done on the system. This framework requires careful accounting of all energy exchanges, 
        including heat transfer and work performed by or on the system. The sign conventions (q positive if heat is absorbed, 
        w positive if work is done on the system) must be consistently applied. The law underpins all energy balance calculations 
        in physical chemistry, from calorimetry to reaction energetics, and forms the basis for defining state functions 
        and path functions. The law is universally applicable to all physical and chemical processes, provided the system 
        boundaries are clearly defined and all forms of energy transfer are considered.
        """,
        key_factors=["system boundary definition", "energy transfer modes", "state functions", "path functions", "sign convention"],
        primary_authority=["R. Atkins, Physical Chemistry", "IUPAC Gold Book"],
        burden_holder="Proponent of energy change claim",
        adversary_position="Energy can be created or destroyed under certain conditions",
        counter_arguments=[
            "No experimental evidence supports creation or destruction of energy.",
            "All observed processes conform to energy conservation.",
            "Apparent violations are due to incomplete system definition."
        ],
        resolution_strategy="Clarify system boundaries and account for all energy exchanges.",
        entity_scope="All physical and chemical systems",
        confidence=0.99,
        confidence_zone="Established Law",
        controlling_precedent="Joule's experiments on mechanical equivalent of heat"
    ),
    DoctrineBlock(
        topic="Second Law and Entropy",
        keywords=["entropy", "spontaneity", "irreversibility", "thermodynamics", "disorder"],
        conclusion_template="The entropy of the universe increases for any spontaneous process; ΔS_univ > 0.",
        reasoning_framework="""
        The Second Law of Thermodynamics introduces the concept of entropy (S) as a measure of disorder or the number 
        of microstates available to a system. For any spontaneous process, the total entropy change of the universe 
        (system plus surroundings) is positive. This law explains the directionality of natural processes and the 
        impossibility of perpetual motion machines of the second kind. The statistical interpretation (Boltzmann's formula, 
        S = k_B ln Ω) connects macroscopic thermodynamics with microscopic states. Entropy changes are calculated for 
        both system and surroundings, especially in reversible and irreversible processes. The law is foundational for 
        predicting spontaneity and equilibrium in chemical reactions and phase changes.
        """,
        key_factors=["entropy change of system", "entropy change of surroundings", "reversibility", "statistical interpretation"],
        primary_authority=["L. Boltzmann", "R. Atkins, Physical Chemistry"],
        burden_holder="Proponent of spontaneous process",
        adversary_position="Processes can be spontaneous with ΔS_univ ≤ 0",
        counter_arguments=[
            "All observed spontaneous processes increase total entropy.",
            "Statistical mechanics supports entropy increase.",
            "Exceptions are due to incomplete entropy accounting."
        ],
        resolution_strategy="Calculate ΔS for both system and surroundings; apply statistical mechanics if needed.",
        entity_scope="All thermodynamic processes",
        confidence=0.98,
        confidence_zone="Established Law",
        controlling_precedent="Clausius' formulation of the Second Law"
    ),
    DoctrineBlock(
        topic="Gibbs Free Energy and Spontaneity",
        keywords=["Gibbs free energy", "spontaneity", "thermodynamics", "ΔG", "equilibrium"],
        conclusion_template="A process at constant temperature and pressure is spontaneous if ΔG < 0.",
        reasoning_framework="""
        Gibbs free energy (G) is defined as G = H - TS, where H is enthalpy, T is temperature, and S is entropy. 
        The change in Gibbs free energy (ΔG) determines the spontaneity of processes at constant temperature and pressure. 
        If ΔG is negative, the process is spontaneous; if positive, non-spontaneous; if zero, the system is at equilibrium. 
        The relationship ΔG = ΔH - TΔS links enthalpy and entropy changes to spontaneity. This doctrine is widely used 
        in predicting chemical reaction feasibility, phase transitions, and biochemical processes. The sign and magnitude 
        of ΔG are calculated using standard state values and corrected for reaction conditions.
        """,
        key_factors=["enthalpy change", "entropy change", "temperature", "standard states", "reaction conditions"],
        primary_authority=["J. Willard Gibbs", "IUPAC Gold Book"],
        burden_holder="Proponent of process spontaneity",
        adversary_position="Processes can be spontaneous with ΔG ≥ 0",
        counter_arguments=[
            "Thermodynamic spontaneity requires ΔG < 0 under specified conditions.",
            "Kinetic factors do not override thermodynamic criteria.",
            "Non-standard conditions must be properly accounted for."
        ],
        resolution_strategy="Calculate ΔG using accurate thermodynamic data and correct for actual conditions.",
        entity_scope="Processes at constant T and P",
        confidence=0.97,
        confidence_zone="Established Law",
        controlling_precedent="Gibbs' original derivations"
    ),
    DoctrineBlock(
        topic="Chemical Potential",
        keywords=["chemical potential", "μ", "partial molar free energy", "equilibrium", "phase transitions"],
        conclusion_template="At equilibrium, the chemical potential of each component is uniform throughout all phases.",
        reasoning_framework="""
        The chemical potential (μ) is the partial molar Gibbs free energy of a component in a mixture. It quantifies 
        the tendency of particles to move between phases or react. At equilibrium, the chemical potential of each 
        component must be equal in all phases and locations. Differences in μ drive diffusion, phase changes, and 
        chemical reactions. The chemical potential is fundamental in deriving criteria for equilibrium in multicomponent 
        systems, phase diagrams, and colligative property calculations. It is calculated from standard chemical potentials 
        and corrected for concentration, pressure, and temperature.
        """,
        key_factors=["partial molar quantities", "phase equilibrium", "concentration", "pressure", "temperature"],
        primary_authority=["J. Willard Gibbs", "R. Atkins, Physical Chemistry"],
        burden_holder="Proponent of equilibrium condition",
        adversary_position="Equilibrium can exist with unequal chemical potentials",
        counter_arguments=[
            "Unequal chemical potentials result in net transfer or reaction.",
            "Equilibrium requires no net change, which only occurs when μ is equal.",
            "Experimental evidence supports uniform μ at equilibrium."
        ],
        resolution_strategy="Measure or calculate μ for all components and phases.",
        entity_scope="Multiphase and multicomponent systems",
        confidence=0.96,
        confidence_zone="Established Law",
        controlling_precedent="Gibbs' phase rule and equilibrium criteria"
    ),
    DoctrineBlock(
        topic="Rate Laws and Reaction Order",
        keywords=["rate law", "reaction order", "kinetics", "rate constant", "concentration dependence"],
        conclusion_template="The rate of a reaction is proportional to the product of reactant concentrations raised to their respective orders.",
        reasoning_framework="""
        Rate laws express the relationship between the rate of a chemical reaction and the concentrations of reactants. 
        The general form is rate = k [A]^m [B]^n, where k is the rate constant and m, n are the reaction orders with 
        respect to each reactant. Reaction order is determined experimentally and may not correspond to stoichiometry. 
        The rate law is foundational for understanding reaction mechanisms, predicting concentration-time profiles, 
        and designing reactors. Integrated rate laws allow calculation of concentrations as a function of time for 
        various reaction orders. Deviations from simple rate laws indicate complex mechanisms or non-ideal behavior.
        """,
        key_factors=["experimental determination", "rate constant", "order of reaction", "mechanistic implications"],
        primary_authority=["IUPAC Gold Book", "P. Atkins, Physical Chemistry"],
        burden_holder="Proponent of specific rate law",
        adversary_position="Stoichiometry determines rate law directly",
        counter_arguments=[
            "Experimental data often show non-integer or unexpected reaction orders.",
            "Mechanism, not stoichiometry, dictates rate law form.",
            "Complex reactions may have composite or fractional orders."
        ],
        resolution_strategy="Determine rate law experimentally and analyze for mechanistic insight.",
        entity_scope="Homogeneous and heterogeneous reactions",
        confidence=0.95,
        confidence_zone="Established Law",
        controlling_precedent="Ostwald's studies on reaction order"
    ),
    DoctrineBlock(
        topic="Arrhenius Equation",
        keywords=["Arrhenius equation", "activation energy", "temperature dependence", "rate constant", "kinetics"],
        conclusion_template="The rate constant k increases exponentially with temperature according to k = A exp(-Ea/RT).",
        reasoning_framework="""
        The Arrhenius equation relates the rate constant (k) of a reaction to temperature (T) and activation energy (Ea): 
        k = A exp(-Ea/RT), where A is the pre-exponential factor and R is the gas constant. This relationship explains 
        the observed increase in reaction rates with temperature. The equation allows extraction of Ea and A from 
        experimental data via linearization (ln k vs 1/T). Deviations from Arrhenius behavior may indicate complex 
        mechanisms or temperature-dependent pre-exponential factors. The equation is widely used in predicting 
        reaction rates, optimizing industrial processes, and understanding temperature effects on kinetics.
        """,
        key_factors=["activation energy", "pre-exponential factor", "temperature", "experimental data"],
        primary_authority=["Svante Arrhenius", "IUPAC Gold Book"],
        burden_holder="Proponent of temperature dependence claim",
        adversary_position="Rate constants are independent of temperature",
        counter_arguments=[
            "Empirical data universally show temperature dependence.",
            "Arrhenius equation accurately models most reactions.",
            "Exceptions are rare and typically involve complex mechanisms."
        ],
        resolution_strategy="Fit rate data to Arrhenius equation and analyze deviations.",
        entity_scope="Elementary and complex reactions",
        confidence=0.94,
        confidence_zone="Established Law",
        controlling_precedent="Arrhenius' original kinetic studies"
    ),
    DoctrineBlock(
        topic="Transition State Theory",
        keywords=["transition state", "activated complex", "kinetics", "reaction coordinate", "rate constant"],
        conclusion_template="Reaction rates are determined by the concentration of the activated complex at the transition state.",
        reasoning_framework="""
        Transition State Theory (TST) models chemical reactions as proceeding via a high-energy activated complex 
        (transition state) along the reaction coordinate. The rate of reaction is proportional to the concentration 
        of this activated complex and the frequency with which it converts to products. TST provides a theoretical 
        basis for the Arrhenius equation and allows calculation of rate constants from molecular properties. 
        The theory assumes equilibrium between reactants and the transition state and neglects quantum tunneling 
        except at very low temperatures. TST is essential for interpreting potential energy surfaces and for 
        computational modeling of reaction mechanisms.
        """,
        key_factors=["activated complex", "potential energy surface", "reaction coordinate", "frequency factor"],
        primary_authority=["Eyring, Evans, Polanyi", "IUPAC Gold Book"],
        burden_holder="Proponent of TST applicability",
        adversary_position="Reaction rates are not determined by transition state properties",
        counter_arguments=[
            "TST predictions match experimental rates for many reactions.",
            "Quantum corrections can be applied for tunneling effects.",
            "Deviations are understood in terms of dynamic recrossing or non-equilibrium effects."
        ],
        resolution_strategy="Compare experimental rates with TST predictions and apply corrections as needed.",
        entity_scope="Elementary reactions, especially in gas phase",
        confidence=0.92,
        confidence_zone="Well Established",
        controlling_precedent="Eyring's formulation of TST"
    ),
    DoctrineBlock(
        topic="Catalysis Mechanisms",
        keywords=["catalysis", "mechanism", "activation energy", "enzyme", "heterogeneous catalysis"],
        conclusion_template="Catalysts increase reaction rates by providing alternative pathways with lower activation energy.",
        reasoning_framework="""
        Catalysts function by offering alternative reaction mechanisms with reduced activation energy barriers, 
        thereby increasing the rate of reaction without being consumed. Mechanistic analysis distinguishes between 
        homogeneous, heterogeneous, and enzymatic catalysis, each with unique features. Catalysts may stabilize 
        transition states, orient reactants, or facilitate electron transfer. The effectiveness of a catalyst 
        depends on its interaction with reactants, surface properties (for heterogeneous systems), and environmental 
        conditions. Catalysis is central to industrial chemistry, biochemistry, and environmental processes.
        """,
        key_factors=["activation energy reduction", "alternative pathways", "catalyst specificity", "surface effects"],
        primary_authority=["IUPAC Gold Book", "P. Atkins, Physical Chemistry"],
        burden_holder="Proponent of catalytic effect",
        adversary_position="Catalysts do not alter reaction rates or mechanisms",
        counter_arguments=[
            "Experimental data show increased rates with catalysts.",
            "Catalysts are not consumed, distinguishing them from reactants.",
            "Mechanistic studies confirm alternative pathways."
        ],
        resolution_strategy="Demonstrate rate enhancement and unchanged catalyst post-reaction.",
        entity_scope="All catalyzed chemical reactions",
        confidence=0.93,
        confidence_zone="Well Established",
        controlling_precedent="Sabatier's principle of catalysis"
    ),
    DoctrineBlock(
        topic="Schrödinger Equation and Wavefunctions",
        keywords=["Schrödinger equation", "wavefunction", "quantum mechanics", "energy levels", "operators"],
        conclusion_template="The behavior of quantum systems is governed by the time-dependent or time-independent Schrödinger equation.",
        reasoning_framework="""
        The Schrödinger equation is the foundational equation of non-relativistic quantum mechanics. The time-independent 
        form, Hψ = Eψ, allows calculation of allowed energy levels and wavefunctions (ψ) for systems such as atoms and 
        molecules. The wavefunction encodes all measurable properties of the system, and its square modulus gives 
        probability densities. Operators corresponding to observables act on ψ to yield measurable quantities. Solutions 
        are subject to boundary conditions and normalization. The equation is central to understanding electronic structure, 
        spectroscopy, and chemical bonding.
        """,
        key_factors=["Hamiltonian operator", "boundary conditions", "normalization", "energy quantization"],
        primary_authority=["E. Schrödinger", "IUPAC Gold Book"],
        burden_holder="Proponent of quantum mechanical description",
        adversary_position="Classical mechanics suffices for atomic-scale systems",
        counter_arguments=[
            "Classical models fail to explain quantization and spectra.",
            "Quantum predictions match experimental results.",
            "Wavefunction formalism is essential for modern chemistry."
        ],
        resolution_strategy="Apply Schrödinger equation to relevant systems and compare predictions to experiment.",
        entity_scope="Atomic and molecular systems",
        confidence=0.99,
        confidence_zone="Established Law",
        controlling_precedent="Hydrogen atom solution"
    ),
    DoctrineBlock(
        topic="Molecular Orbital Theory",
        keywords=["molecular orbital", "bonding", "antibonding", "delocalization", "electronic structure"],
        conclusion_template="Molecular orbital theory explains bonding by the combination of atomic orbitals to form delocalized molecular orbitals.",
        reasoning_framework="""
        Molecular Orbital (MO) Theory describes the electronic structure of molecules by combining atomic orbitals 
        to form molecular orbitals that are delocalized over the entire molecule. Bonding and antibonding MOs arise 
        from constructive and destructive interference, respectively. The filling of MOs according to the Pauli 
        principle and Hund's rule determines bond order, magnetism, and electronic spectra. MO theory accounts for 
        phenomena such as resonance, aromaticity, and the electronic properties of conjugated systems, which are 
        inadequately explained by valence bond theory alone.
        """,
        key_factors=["orbital overlap", "bond order", "delocalization", "electron configuration"],
        primary_authority=["F. Hund", "R. S. Mulliken", "IUPAC Gold Book"],
        burden_holder="Proponent of MO-based bonding explanation",
        adversary_position="Valence bond theory fully explains molecular bonding",
        counter_arguments=[
            "MO theory explains delocalization and properties not captured by VB theory.",
            "Spectroscopic data support MO predictions.",
            "Resonance and aromaticity require MO framework."
        ],
        resolution_strategy="Analyze molecular properties using both VB and MO theory; compare with experiment.",
        entity_scope="Molecules with delocalized electrons",
        confidence=0.95,
        confidence_zone="Well Established",
        controlling_precedent="MO treatment of benzene"
    ),
    DoctrineBlock(
        topic="Hartree-Fock Method",
        keywords=["Hartree-Fock", "self-consistent field", "quantum chemistry", "approximation", "electronic structure"],
        conclusion_template="The Hartree-Fock method approximates the electronic structure by treating electron interactions in a mean-field approach.",
        reasoning_framework="""
        The Hartree-Fock (HF) method is a quantum chemical approach that approximates the many-electron wavefunction 
        as a single Slater determinant, treating electron-electron repulsion in an average way (mean field). The method 
        iteratively solves for self-consistent molecular orbitals, yielding energies and properties for atoms and molecules. 
        While HF neglects electron correlation beyond the mean field, it forms the basis for more accurate post-HF methods 
        (e.g., MP2, CCSD). HF is widely used for qualitative electronic structure analysis and as a starting point for 
        computational chemistry calculations.
        """,
        key_factors=["mean-field approximation", "Slater determinant", "self-consistency", "electron correlation"],
        primary_authority=["D. R. Hartree", "V. Fock", "IUPAC Gold Book"],
        burden_holder="Proponent of HF-based electronic structure",
        adversary_position="HF method is insufficient due to lack of correlation",
        counter_arguments=[
            "HF provides a good qualitative description for many systems.",
            "Post-HF methods can correct for correlation.",
            "HF is computationally efficient and widely validated."
        ],
        resolution_strategy="Use HF for qualitative insight; apply post-HF methods for quantitative accuracy.",
        entity_scope="Atoms and molecules in computational chemistry",
        confidence=0.90,
        confidence_zone="Well Established",
        controlling_precedent="HF calculations of small molecules"
    ),
    DoctrineBlock(
        topic="Statistical Mechanics Foundations",
        keywords=["statistical mechanics", "partition function", "ensemble", "thermodynamics", "microscopic states"],
        conclusion_template="Macroscopic thermodynamic properties can be derived from statistical averages over microscopic states.",
        reasoning_framework="""
        Statistical mechanics bridges the gap between microscopic particle behavior and macroscopic thermodynamic 
        properties. The partition function (Z) encodes the statistical weights of all accessible microstates and 
        is central to calculating thermodynamic quantities (e.g., energy, entropy, free energy). Ensembles (microcanonical, 
        canonical, grand canonical) provide frameworks for different physical situations. The approach allows prediction 
        of equilibrium properties, fluctuations, and response functions from first principles. Statistical mechanics 
        underpins the molecular interpretation of entropy, temperature, and chemical potential.
        """,
        key_factors=["partition function", "ensemble choice", "microstate probabilities", "thermodynamic averages"],
        primary_authority=["J. Willard Gibbs", "L. Boltzmann", "IUPAC Gold Book"],
        burden_holder="Proponent of statistical mechanical derivation",
        adversary_position="Thermodynamics is independent of microscopic details",
        counter_arguments=[
            "Statistical mechanics explains thermodynamic laws from molecular principles.",
            "Predictions match experimental data.",
            "Provides insight into fluctuations and non-equilibrium phenomena."
        ],
        resolution_strategy="Derive macroscopic properties from partition function and compare with experiment.",
        entity_scope="All systems with large numbers of particles",
        confidence=0.97,
        confidence_zone="Established Law",
        controlling_precedent="Boltzmann's entropy formula"
    ),
    DoctrineBlock(
        topic="Adsorption Isotherms",
        keywords=["adsorption", "isotherm", "Langmuir", "BET", "surface chemistry"],
        conclusion_template="Adsorption isotherms describe the relationship between adsorbate concentration and surface coverage at constant temperature.",
        reasoning_framework="""
        Adsorption isotherms quantify how molecules adhere to surfaces as a function of concentration or pressure at 
        constant temperature. The Langmuir isotherm assumes monolayer adsorption on homogeneous sites, while the BET 
        isotherm extends to multilayer adsorption. Deviations from ideal behavior indicate surface heterogeneity or 
        interactions between adsorbed species. Isotherms are essential for characterizing catalysts, porous materials, 
        and environmental surfaces. Parameters extracted from isotherm models provide insight into surface area, 
        adsorption energy, and capacity.
        """,
        key_factors=["adsorption model", "surface homogeneity", "monolayer/multilayer", "experimental data"],
        primary_authority=["IUPAC Gold Book", "I. Langmuir", "S. Brunauer"],
        burden_holder="Proponent of specific isotherm model",
        adversary_position="Isotherm models are not universally applicable",
        counter_arguments=[
            "Different models apply to different systems.",
            "Experimental fitting distinguishes appropriate model.",
            "Surface characterization guides model selection."
        ],
        resolution_strategy="Fit experimental data to multiple isotherm models and assess goodness of fit.",
        entity_scope="Surface and interface chemistry",
        confidence=0.89,
        confidence_zone="Well Established",
        controlling_precedent="Langmuir's adsorption studies"
    ),
    DoctrineBlock(
        topic="Electrochemistry and Nernst Equation",
        keywords=["electrochemistry", "Nernst equation", "cell potential", "redox", "concentration dependence"],
        conclusion_template="The Nernst equation relates cell potential to standard potential and activities of reactants and products.",
        reasoning_framework="""
        The Nernst equation provides a quantitative relationship between the electrode potential of a half-cell or 
        full cell and the concentrations (activities) of the involved species: E = E° - (RT/nF) ln Q, where E° is 
        the standard potential, n is the number of electrons, F is Faraday's constant, and Q is the reaction quotient. 
        The equation is fundamental for predicting cell voltages, understanding redox equilibria, and designing 
        electrochemical sensors and batteries. Deviations from ideality arise from non-ideal solution behavior, 
        requiring activity corrections.
        """,
        key_factors=["standard potential", "reaction quotient", "temperature", "activity coefficients"],
        primary_authority=["W. Nernst", "IUPAC Gold Book"],
        burden_holder="Proponent of predicted cell potential",
        adversary_position="Cell potential is independent of concentration",
        counter_arguments=[
            "Experimental measurements confirm Nernst equation predictions.",
            "Non-idealities can be corrected using activity coefficients.",
            "Standard potentials are well tabulated."
        ],
        resolution_strategy="Calculate cell potential using Nernst equation and correct for non-idealities.",
        entity_scope="Electrochemical cells and sensors",
        confidence=0.96,
        confidence_zone="Established Law",
        controlling_precedent="Nernst's original electrochemical studies"
    ),
    DoctrineBlock(
        topic="Spectroscopy Fundamentals",
        keywords=["spectroscopy", "absorption", "emission", "selection rules", "quantization"],
        conclusion_template="Spectroscopic transitions occur between quantized energy levels, governed by selection rules.",
        reasoning_framework="""
        Spectroscopy involves the interaction of electromagnetic radiation with matter, resulting in absorption or 
        emission corresponding to transitions between quantized energy levels. The allowed transitions are determined 
        by selection rules derived from quantum mechanics, such as changes in angular momentum or parity. Spectroscopic 
        methods (UV-Vis, IR, NMR, etc.) provide information about electronic, vibrational, and rotational states. 
        The intensity and position of spectral lines yield structural and dynamic information about molecules.
        """,
        key_factors=["energy quantization", "selection rules", "transition dipole moment", "spectral resolution"],
        primary_authority=["IUPAC Gold Book", "P. Atkins, Physical Chemistry"],
        burden_holder="Proponent of spectroscopic assignment",
        adversary_position="All transitions are equally probable",
        counter_arguments=[
            "Selection rules explain observed spectral patterns.",
            "Forbidden transitions are weak or absent.",
            "Quantum mechanical calculations match experimental spectra."
        ],
        resolution_strategy="Apply selection rules and compare predicted spectra with experiment.",
        entity_scope="Molecular and atomic spectroscopy",
        confidence=0.94,
        confidence_zone="Well Established",
        controlling_precedent="Quantum mechanical derivation of selection rules"
    ),
    DoctrineBlock(
        topic="Phase Diagrams and Phase Rule",
        keywords=["phase diagram", "Gibbs phase rule", "components", "phases", "equilibrium"],
        conclusion_template="The number of degrees of freedom in a system is given by F = C - P + 2.",
        reasoning_framework="""
        The Gibbs phase rule relates the number of components (C), phases (P), and degrees of freedom (F) in a 
        system at equilibrium: F = C - P + 2. Phase diagrams graphically represent the stability regions of different 
        phases as a function of temperature, pressure, and composition. The rule is essential for interpreting 
        phase equilibria in pure substances and mixtures, predicting invariant points (eutectic, triple point), 
        and designing separation processes. Deviations from the rule may indicate non-equilibrium or metastable states.
        """,
        key_factors=["number of components", "number of phases", "external variables", "equilibrium conditions"],
        primary_authority=["J. Willard Gibbs", "IUPAC Gold Book"],
        burden_holder="Proponent of phase rule application",
        adversary_position="Phase rule does not apply to real systems",
        counter_arguments=[
            "Phase rule applies to systems at equilibrium.",
            "Non-equilibrium states require separate analysis.",
            "Experimental phase diagrams confirm predictions."
        ],
        resolution_strategy="Verify equilibrium and apply phase rule to interpret diagram.",
        entity_scope="Pure substances and mixtures",
        confidence=0.95,
        confidence_zone="Well Established",
        controlling_precedent="Gibbs' original phase rule derivation"
    ),
    DoctrineBlock(
        topic="Diffusion and Transport Phenomena",
        keywords=["diffusion", "Fick's laws", "transport", "flux", "gradient"],
        conclusion_template="The rate of diffusion is proportional to the concentration gradient, as described by Fick's laws.",
        reasoning_framework="""
        Diffusion is the net movement of particles from regions of high concentration to low concentration, driven 
        by the concentration gradient. Fick's first law states that the diffusive flux is proportional to the gradient, 
        while Fick's second law describes the time evolution of concentration profiles. Transport phenomena encompass 
        diffusion, thermal conduction, and viscosity, all governed by similar mathematical frameworks. The diffusion 
        coefficient depends on temperature, medium, and particle size. Deviations from Fickian behavior occur in 
        complex or heterogeneous systems.
        """,
        key_factors=["concentration gradient", "diffusion coefficient", "medium properties", "boundary conditions"],
        primary_authority=["A. Fick", "IUPAC Gold Book"],
        burden_holder="Proponent of diffusion model",
        adversary_position="Diffusion rate is independent of concentration gradient",
        counter_arguments=[
            "Experimental data confirm Fick's laws in most systems.",
            "Non-Fickian diffusion is a special case requiring alternative models.",
            "Transport coefficients are measurable and predictive."
        ],
        resolution_strategy="Apply Fick's laws and measure diffusion coefficients experimentally.",
        entity_scope="Gases, liquids, and solids",
        confidence=0.93,
        confidence_zone="Well Established",
        controlling_precedent="Fick's original diffusion experiments"
    ),
    DoctrineBlock(
        topic="Colligative Properties",
        keywords=["colligative properties", "vapor pressure lowering", "boiling point elevation", "freezing point depression", "osmotic pressure"],
        conclusion_template="Colligative properties depend only on the number of solute particles, not their identity.",
        reasoning_framework="""
        Colligative properties arise from the presence of solute particles in a solvent and include vapor pressure 
        lowering, boiling point elevation, freezing point depression, and osmotic pressure. These properties depend 
        solely on the number of dissolved particles, not their chemical nature. The van't Hoff factor accounts for 
        dissociation or association in solution. Colligative properties are used to determine molar masses and 
        study solution behavior. Deviations from ideality occur at high concentrations or with strong solute-solvent 
        interactions.
        """,
        key_factors=["solute particle number", "van't Hoff factor", "ideal solution behavior", "concentration"],
        primary_authority=["J. H. van't Hoff", "IUPAC Gold Book"],
        burden_holder="Proponent of colligative property explanation",
        adversary_position="Colligative properties depend on solute identity",
        counter_arguments=[
            "Experimental measurements support dependence on particle number.",
            "Corrections for non-ideality are well established.",
            "Identity effects are secondary to particle count."
        ],
        resolution_strategy="Apply colligative property equations and account for van't Hoff factor.",
        entity_scope="Dilute solutions",
        confidence=0.92,
        confidence_zone="Well Established",
        controlling_precedent="van't Hoff's osmotic pressure studies"
    ),
    DoctrineBlock(
        topic="Computational Chemistry Methods",
        keywords=["computational chemistry", "ab initio", "DFT", "molecular mechanics", "simulation"],
        conclusion_template="Computational chemistry employs a range of methods to model molecular systems at various levels of theory.",
        reasoning_framework="""
        Computational chemistry encompasses a spectrum of methods, from ab initio quantum mechanical calculations 
        (e.g., Hartree-Fock, post-HF, DFT) to molecular mechanics and dynamics simulations. The choice of method 
        depends on system size, required accuracy, and computational resources. Ab initio methods provide high 
        accuracy for small systems, while molecular mechanics enables large-scale simulations. Hybrid approaches 
        (QM/MM) combine quantum and classical methods. Validation against experimental data is essential for 
        reliable predictions.
        """,
        key_factors=["level of theory", "system size", "accuracy requirements", "validation"],
        primary_authority=["IUPAC Gold Book", "C. J. Cramer, Essentials of Computational Chemistry"],
        burden_holder="Proponent of computational result",
        adversary_position="Computational methods are unreliable or inaccurate",
        counter_arguments=[
            "Method selection is based on system and property of interest.",
            "Benchmarking and validation ensure reliability.",
            "Computational predictions increasingly match experiment."
        ],
        resolution_strategy="Select appropriate method and validate against experimental or high-level data.",
        entity_scope="Molecular systems in silico",
        confidence=0.91,
        confidence_zone="Well Established",
        controlling_precedent="Benchmark studies of computational methods"
    ),
    DoctrineBlock(
        topic="Photochemistry Principles",
        keywords=["photochemistry", "excited state", "quantum yield", "Jablonski diagram", "photoinduced reaction"],
        conclusion_template="Photochemical reactions are initiated by absorption of photons, leading to excited electronic states.",
        reasoning_framework="""
        Photochemistry studies chemical changes induced by absorption of light. Molecules absorb photons and are 
        promoted to excited electronic states, which may undergo various processes: fluorescence, phosphorescence, 
        non-radiative decay, or chemical reaction. The Jablonski diagram summarizes possible pathways. Quantum yield 
        quantifies the efficiency of photochemical processes. The nature and fate of excited states are governed by 
        selection rules, energy gaps, and environmental factors. Photochemistry is central to vision, photosynthesis, 
        and photolithography.
        """,
        key_factors=["excited state dynamics", "quantum yield", "energy transfer", "environmental effects"],
        primary_authority=["N. J. Turro, Modern Molecular Photochemistry", "IUPAC Gold Book"],
        burden_holder="Proponent of photochemical mechanism",
        adversary_position="Light does not induce chemical change",
        counter_arguments=[
            "Experimental evidence for photoinduced reactions is overwhelming.",
            "Quantum yields quantify photochemical efficiency.",
            "Spectroscopic techniques confirm excited state involvement."
        ],
        resolution_strategy="Demonstrate light-induced reaction and measure quantum yield.",
        entity_scope="Molecular systems under irradiation",
        confidence=0.93,
        confidence_zone="Well Established",
        controlling_precedent="Grotthuss-Draper law"
    ),
    DoctrineBlock(
        topic="Polymer Physical Chemistry",
        keywords=["polymer", "molecular weight", "glass transition", "crystallinity", "chain conformation"],
        conclusion_template="Polymer properties depend on molecular weight, chain structure, and thermal transitions.",
        reasoning_framework="""
        The physical chemistry of polymers addresses how molecular weight, chain architecture (linear, branched, 
        crosslinked), and thermal transitions (glass transition, melting) determine material properties. The distribution 
        of molecular weights (polydispersity) affects viscosity, mechanical strength, and solubility. Chain conformation 
        and crystallinity influence optical and barrier properties. Techniques such as GPC, DSC, and X-ray diffraction 
        are used for characterization. Understanding these factors is essential for designing polymers with desired 
        properties.
        """,
        key_factors=["molecular weight distribution", "thermal transitions", "chain architecture", "crystallinity"],
        primary_authority=["P. J. Flory", "IUPAC Gold Book"],
        burden_holder="Proponent of structure-property relationship",
        adversary_position="Polymer properties are independent of structure",
        counter_arguments=[
            "Experimental data show strong dependence on molecular weight and structure.",
            "Thermal transitions define material applications.",
            "Chain conformation affects mechanical and optical behavior."
        ],
        resolution_strategy="Characterize polymer structure and correlate with measured properties.",
        entity_scope="Synthetic and natural polymers",
        confidence=0.90,
        confidence_zone="Well Established",
        controlling_precedent="Flory's theory of polymer solutions"
    ),
    DoctrineBlock(
        topic="Chemical Equilibrium Thermodynamics",
        keywords=["chemical equilibrium", "thermodynamics", "equilibrium constant", "Le Chatelier's principle", "reaction quotient"],
        conclusion_template="At equilibrium, the reaction quotient equals the equilibrium constant, and ΔG = 0.",
        reasoning_framework="""
        Chemical equilibrium is achieved when the rates of forward and reverse reactions are equal, resulting in 
        constant concentrations of reactants and products. The equilibrium constant (K) relates to the standard 
        Gibbs free energy change: ΔG° = -RT ln K. Le Chatelier's principle predicts the response of equilibrium 
        to changes in concentration, pressure, or temperature. The reaction quotient (Q) indicates the direction 
        of shift needed to reach equilibrium. Thermodynamic criteria ensure that ΔG = 0 at equilibrium.
        """,
        key_factors=["equilibrium constant", "reaction quotient", "Gibbs free energy", "external perturbations"],
        primary_authority=["IUPAC Gold Book", "P. Atkins, Physical Chemistry"],
        burden_holder="Proponent of equilibrium position",
        adversary_position="Equilibrium can exist with ΔG ≠ 0",
        counter_arguments=[
            "Thermodynamic equilibrium requires ΔG = 0.",
            "Kinetics determines rate, not position, of equilibrium.",
            "Le Chatelier's principle is predictive and experimentally validated."
        ],
        resolution_strategy="Calculate Q, K, and ΔG; predict shifts using Le Chatelier's principle.",
        entity_scope="Reversible chemical reactions",
        confidence=0.97,
        confidence_zone="Established Law",
        controlling_precedent="Law of mass action"
    ),
    DoctrineBlock(
        topic="Real Gas Behavior",
        keywords=["real gas", "van der Waals equation", "non-ideality", "compressibility factor", "intermolecular forces"],
        conclusion_template="Real gases deviate from ideal behavior due to intermolecular forces and finite molecular volume.",
        reasoning_framework="""
        The ideal gas law assumes point particles with no interactions, but real gases exhibit deviations at high 
        pressures and low temperatures. The van der Waals equation introduces corrections for molecular volume (b) 
        and attractive forces (a): (P + a/V^2)(V - b) = RT. The compressibility factor (Z) quantifies deviation 
        from ideality. Understanding real gas behavior is essential for accurate predictions in industrial and 
        laboratory settings. Other equations of state (Redlich-Kwong, Peng-Robinson) provide improved accuracy 
        for specific systems.
        """,
        key_factors=["pressure", "temperature", "van der Waals parameters", "compressibility factor"],
        primary_authority=["J. D. van der Waals", "IUPAC Gold Book"],
        burden_holder="Proponent of real gas model",
        adversary_position="Ideal gas law suffices for all conditions",
        counter_arguments=[
            "Experimental P-V-T data show deviations from ideality.",
            "van der Waals and other models fit real gas behavior.",
            "Ideal gas law is a limiting case."
        ],
        resolution_strategy="Apply real gas equations and compare with experimental data.",
        entity_scope="Gases under non-ideal conditions",
        confidence=0.93,
        confidence_zone="Well Established",
        controlling_precedent="van der Waals' original studies"
    ),
    DoctrineBlock(
        topic="Boltzmann Distribution",
        keywords=["Boltzmann distribution", "statistical mechanics", "population", "energy levels", "temperature"],
        conclusion_template="At thermal equilibrium, the population of states follows the Boltzmann distribution.",
        reasoning_framework="""
        The Boltzmann distribution describes the probability of a system occupying a state of energy E at temperature T: 
        P(E) ∝ exp(-E/k_BT). This distribution governs the population of molecular energy levels, reaction rates, 
        and equilibrium constants. It is foundational for understanding temperature dependence of physical and chemical 
        processes, including spectroscopy and kinetics. The distribution emerges naturally from statistical mechanics 
        and is validated by experimental observations.
        """,
        key_factors=["energy level spacing", "temperature", "partition function", "statistical weights"],
        primary_authority=["L. Boltzmann", "IUPAC Gold Book"],
        burden_holder="Proponent of equilibrium population distribution",
        adversary_position="Populations are independent of energy and temperature",
        counter_arguments=[
            "Spectroscopic intensities confirm Boltzmann statistics.",
            "Temperature dependence matches theoretical predictions.",
            "Non-equilibrium populations relax to Boltzmann distribution over time."
        ],
        resolution_strategy="Measure populations experimentally and compare with Boltzmann prediction.",
        entity_scope="Thermal equilibrium systems",
        confidence=0.97,
        confidence_zone="Established Law",
        controlling_precedent="Boltzmann's statistical mechanics"
    ),
    DoctrineBlock(
        topic="Partition Function Centrality",
        keywords=["partition function", "statistical mechanics", "thermodynamics", "energy states", "ensemble"],
        conclusion_template="The partition function encodes all thermodynamic information of a system at equilibrium.",
        reasoning_framework="""
        The partition function (Z) is the sum over all possible states, weighted by their Boltzmann factors: 
        Z = Σ exp(-E_i/k_BT). All macroscopic thermodynamic properties (energy, entropy, free energy, heat capacity) 
        can be derived from Z and its derivatives. The choice of ensemble (canonical, grand canonical, etc.) determines 
        the form of Z. Accurate calculation of Z is crucial for connecting microscopic models to experimental observables.
        """,
        key_factors=["energy spectrum", "ensemble choice", "temperature", "state degeneracy"],
        primary_authority=["J. Willard Gibbs", "L. Boltzmann"],
        burden_holder="Proponent of partition function approach",
        adversary_position="Thermodynamic properties are independent of partition function",
        counter_arguments=[
            "Statistical mechanics derives all properties from Z.",
            "Experimental data confirm predictions from partition function.",
            "Partition function is central in all ensemble formulations."
        ],
        resolution_strategy="Calculate Z for the system and derive properties; compare with experiment.",
        entity_scope="Systems at thermal equilibrium",
        confidence=0.96,
        confidence_zone="Established Law",
        controlling_precedent="Gibbs' ensemble theory"
    ),
    DoctrineBlock(
        topic="Le Chatelier's Principle",
        keywords=["Le Chatelier", "equilibrium shift", "perturbation", "concentration", "pressure", "temperature"],
        conclusion_template="A system at equilibrium responds to a disturbance by shifting to counteract the change.",
        reasoning_framework="""
        Le Chatelier's Principle predicts the qualitative response of a system at equilibrium to changes in 
        concentration, pressure, or temperature. The system shifts in the direction that minimizes the effect 
        of the disturbance, re-establishing equilibrium. This principle is widely used to predict the outcome 
        of experimental manipulations and to optimize industrial chemical processes. Quantitative predictions 
        require calculation of the new equilibrium position using thermodynamic data.
        """,
        key_factors=["type of disturbance", "direction of shift", "thermodynamic data", "reaction stoichiometry"],
        primary_authority=["H. Le Chatelier", "IUPAC Gold Book"],
        burden_holder="Proponent of predicted shift",
        adversary_position="Equilibrium position is unaffected by external changes",
        counter_arguments=[
            "Experimental results confirm predicted shifts.",
            "Thermodynamic calculations support principle.",
            "Principle is consistent with reaction quotient analysis."
        ],
        resolution_strategy="Identify disturbance and predict shift using Le Chatelier's principle.",
        entity_scope="Reversible chemical reactions",
        confidence=0.95,
        confidence_zone="Well Established",
        controlling_precedent="Le Chatelier's original studies"
    ),
    DoctrineBlock(
        topic="Quantum Tunneling in Chemistry",
        keywords=["quantum tunneling", "barrier penetration", "kinetics", "isotope effect", "reaction rate"],
        conclusion_template="Quantum tunneling allows particles to surmount energy barriers lower than their classical energy.",
        reasoning_framework="""
        Quantum tunneling is a phenomenon where particles pass through energy barriers that would be insurmountable 
        classically. In chemistry, tunneling can significantly enhance reaction rates, especially for light atoms 
        (e.g., hydrogen transfer) and at low temperatures. The effect is observed in kinetic isotope effects and 
        deviations from Arrhenius behavior. Tunneling is incorporated into rate theories via corrections to 
        transition state theory or semiclassical models. Its significance depends on barrier width, height, and 
        particle mass.
        """,
        key_factors=["barrier width and height", "particle mass", "temperature", "isotope effects"],
        primary_authority=["IUPAC Gold Book", "P. Atkins, Physical Chemistry"],
        burden_holder="Proponent of tunneling contribution",
        adversary_position="Classical over-the-barrier passage suffices",
        counter_arguments=[
            "Observed rates exceed classical predictions in many cases.",
            "Isotope effects confirm tunneling.",
            "Quantum mechanical models match experimental data."
        ],
        resolution_strategy="Analyze kinetic data and apply tunneling corrections as appropriate.",
        entity_scope="Reactions involving light atoms or low temperatures",
        confidence=0.90,
        confidence_zone="Well Established",
        controlling_precedent="Bell's tunneling model"
    ),
    DoctrineBlock(
        topic="Thermodynamic Cycles",
        keywords=["thermodynamic cycle", "Hess's law", "enthalpy", "state function", "energy conservation"],
        conclusion_template="The total enthalpy change for a process is independent of the path taken, depending only on initial and final states.",
        reasoning_framework="""
        Thermodynamic cycles, such as those used in Hess's law, demonstrate that enthalpy is a state function. 
        The enthalpy change for a reaction is the same whether it occurs in one step or multiple steps. This 
        principle allows calculation of enthalpy changes for reactions that are difficult to measure directly, 
        by combining known enthalpy changes for related reactions. The approach is grounded in the First Law 
        of Thermodynamics and is widely used in calorimetry and reaction energetics.
        """,
        key_factors=["state function property", "enthalpy data", "reaction pathway", "energy conservation"],
        primary_authority=["G. H. Hess", "IUPAC Gold Book"],
        burden_holder="Proponent of enthalpy calculation",
        adversary_position="Enthalpy change depends on reaction path",
        counter_arguments=[
            "Experimental data confirm path independence.",
            "State function property is fundamental to thermodynamics.",
            "Hess's law is universally validated."
        ],
        resolution_strategy="Construct thermodynamic cycles and sum enthalpy changes.",
        entity_scope="Chemical reactions and processes",
        confidence=0.97,
        confidence_zone="Established Law",
        controlling_precedent="Hess's law"
    ),
    DoctrineBlock(
        topic="Enzyme Kinetics (Michaelis-Menten)",
        keywords=["enzyme kinetics", "Michaelis-Menten", "Vmax", "Km", "catalysis"],
        conclusion_template="The Michaelis-Menten equation describes the rate of enzyme-catalyzed reactions as a function of substrate concentration.",
        reasoning_framework="""
        The Michaelis-Menten model provides a quantitative framework for enzyme kinetics: 
        v = (Vmax [S]) / (Km + [S]), where Vmax is the maximum rate, Km is the Michaelis constant, and [S] is 
        substrate concentration. The model assumes formation of an enzyme-substrate complex and steady-state 
        conditions. Deviations from Michaelis-Menten behavior indicate allosteric effects, cooperativity, or 
        multi-substrate mechanisms. The parameters Vmax and Km are determined experimentally and provide insight 
        into enzyme efficiency and affinity.
        """,
        key_factors=["enzyme-substrate complex", "steady-state assumption", "Vmax", "Km"],
        primary_authority=["L. Michaelis", "M. L. Menten", "IUPAC Gold Book"],
        burden_holder="Proponent of Michaelis-Menten kinetics",
        adversary_position="Enzyme kinetics do not follow Michaelis-Menten equation",
        counter_arguments=[
            "Most enzymes follow Michaelis-Menten kinetics under standard conditions.",
            "Non-Michaelis-Menten behavior is well characterized.",
            "Model parameters are experimentally accessible."
        ],
        resolution_strategy="Fit kinetic data to Michaelis-Menten equation and analyze deviations.",
        entity_scope="Enzyme-catalyzed reactions",
        confidence=0.93,
        confidence_zone="Well Established",
        controlling_precedent="Michaelis-Menten original studies"
    ),
    DoctrineBlock(
        topic="Debye-Hückel Theory",
        keywords=["Debye-Hückel", "ionic strength", "activity coefficient", "electrolyte solution", "non-ideality"],
        conclusion_template="The Debye-Hückel theory quantifies the effect of ionic strength on activity coefficients in dilute solutions.",
        reasoning_framework="""
        The Debye-Hückel theory models the non-ideal behavior of electrolyte solutions by accounting for electrostatic 
        interactions between ions. The theory provides an expression for the activity coefficient as a function of 
        ionic strength, valid for dilute solutions. Deviations at higher concentrations are addressed by extended 
        models. The theory is essential for accurate calculation of equilibrium constants, solubility, and electrochemical 
        potentials in ionic solutions.
        """,
        key_factors=["ionic strength", "activity coefficient", "solution concentration", "electrostatic interactions"],
        primary_authority=["P. Debye", "E. Hückel", "IUPAC Gold Book"],
        burden_holder="Proponent of activity correction",
        adversary_position="Electrolyte solutions behave ideally",
        counter_arguments=[
            "Experimental data show significant non-ideality.",
            "Debye-Hückel theory matches dilute solution behavior.",
            "Extensions address higher concentrations."
        ],
        resolution_strategy="Apply Debye-Hückel equation and compare with experimental activity coefficients.",
        entity_scope="Dilute electrolyte solutions",
        confidence=0.91,
        confidence_zone="Well Established",
        controlling_precedent="Debye-Hückel original papers"
    ),
    DoctrineBlock(
        topic="Beer-Lambert Law",
        keywords=["Beer-Lambert law", "absorbance", "concentration", "path length", "spectroscopy"],
        conclusion_template="Absorbance is directly proportional to concentration and path length: A = εcl.",
        reasoning_framework="""
        The Beer-Lambert law relates the absorbance (A) of a solution to the concentration (c) of the absorbing 
        species, the path length (l), and the molar absorptivity (ε): A = εcl. The law is foundational for 
        quantitative spectroscopic analysis. Deviations occur at high concentrations, with chemical interactions, 
        or instrument limitations. Calibration and careful experimental design ensure accurate application.
        """,
        key_factors=["molar absorptivity", "concentration range", "instrument calibration", "solvent effects"],
        primary_authority=["A. Beer", "J. H. Lambert", "IUPAC Gold Book"],
        burden_holder="Proponent of quantitative analysis",
        adversary_position="Absorbance is not proportional to concentration",
        counter_arguments=[
            "Law holds for dilute solutions and well-behaved systems.",
            "Deviations are predictable and correctable.",
            "Widely validated in analytical chemistry."
        ],
        resolution_strategy="Validate linearity with calibration standards and apply corrections as needed.",
        entity_scope="Spectroscopic analysis of solutions",
        confidence=0.95,
        confidence_zone="Well Established",
        controlling_precedent="Beer-Lambert original experiments"
    ),
    DoctrineBlock(
        topic="Thermodynamic vs Kinetic Control",
        keywords=["thermodynamic control", "kinetic control", "product distribution", "activation energy", "reaction conditions"],
        conclusion_template="Product distribution is determined by thermodynamic stability or kinetic accessibility, depending on reaction conditions.",
        reasoning_framework="""
        In reactions with multiple possible products, the major product may be determined by either thermodynamic 
        control (most stable product) or kinetic control (product formed fastest). Low temperatures and short 
        reaction times favor kinetic products, while high temperatures and longer times favor thermodynamic products. 
        The distinction is critical in organic synthesis, catalysis, and materials chemistry. Product ratios can 
        be shifted by altering reaction conditions.
        """,
        key_factors=["activation energy", "product stability", "reaction time", "temperature"],
        primary_authority=["IUPAC Gold Book", "P. Atkins, Physical Chemistry"],
        burden_holder="Proponent of product distribution explanation",
        adversary_position="Product ratios are fixed by stoichiometry",
        counter_arguments=[
            "Experimental data show condition-dependent product ratios.",
            "Energy diagrams illustrate kinetic and thermodynamic pathways.",
            "Control can be switched by changing conditions."
        ],
        resolution_strategy="Analyze energy profiles and vary conditions to determine control regime.",
        entity_scope="Reactions with multiple products",
        confidence=0.92,
        confidence_zone="Well Established",
        controlling_precedent="Curtin-Hammett principle"
    ),
    DoctrineBlock(
        topic="Osmotic Pressure",
        keywords=["osmotic pressure", "semipermeable membrane", "colligative property", "van't Hoff equation", "solution"],
        conclusion_template="Osmotic pressure is proportional to solute concentration and temperature: Π = cRT.",
        reasoning_framework="""
        Osmotic pressure (Π) is the pressure required to prevent solvent flow through a semipermeable membrane 
        separating solutions of different concentrations. The van't Hoff equation, Π = cRT, applies to dilute 
        solutions and treats osmotic pressure as a colligative property. Deviations occur at higher concentrations 
        or with non-ideal solutes. Osmotic pressure is fundamental in biology, medicine, and industrial processes.
        """,
        key_factors=["solute concentration", "temperature", "membrane properties", "solution ideality"],
        primary_authority=["J. H. van't Hoff", "IUPAC Gold Book"],
        burden_holder="Proponent of osmotic pressure calculation",
        adversary_position="Osmotic pressure is unrelated to solute concentration",
        counter_arguments=[
            "Experimental measurements confirm van't Hoff equation.",
            "Non-idealities are well characterized.",
            "Osmotic pressure is widely used for molar mass determination."
        ],
        resolution_strategy="Apply van't Hoff equation and correct for non-ideality as needed.",
        entity_scope="Dilute solutions and biological systems",
        confidence=0.94,
        confidence_zone="Well Established",
        controlling_precedent="van't Hoff's osmotic pressure studies"
    ),
    DoctrineBlock(
        topic="Raoult's Law",
        keywords=["Raoult's law", "vapor pressure", "ideal solution", "mole fraction", "phase equilibrium"],
        conclusion_template="The vapor pressure of an ideal solution is proportional to the mole fraction of each component.",
        reasoning_framework="""
        Raoult's law states that the partial vapor pressure of each component in an ideal solution is equal to 
        its mole fraction multiplied by its pure component vapor pressure: P_i = x_i P_i*. The total vapor pressure 
        is the sum of partial pressures. Deviations from Raoult's law indicate non-ideal interactions, leading 
        to positive or negative deviations. The law is fundamental for understanding distillation, azeotropes, 
        and phase diagrams.
        """,
        key_factors=["mole fraction", "pure component vapor pressure", "solution ideality", "intermolecular interactions"],
        primary_authority=["F. M. Raoult", "IUPAC Gold Book"],
        burden_holder="Proponent of Raoult's law application",
        adversary_position="Vapor pressure is independent of composition",
        counter_arguments=[
            "Ideal solutions follow Raoult's law closely.",
            "Deviations are predictable and quantifiable.",
            "Law is foundational in phase equilibrium studies."
        ],
        resolution_strategy="Determine solution ideality and apply Raoult's law or corrections.",
        entity_scope="Ideal and non-ideal solutions",
        confidence=0.93,
        confidence_zone="Well Established",
        controlling_precedent="Raoult's original experiments"
    ),
    DoctrineBlock(
        topic="Henry's Law",
        keywords=["Henry's law", "gas solubility", "partial pressure", "solution", "proportionality constant"],
        conclusion_template="The solubility of a gas in a liquid is proportional to its partial pressure: c = k_H P.",
        reasoning_framework="""
        Henry's law states that at constant temperature, the concentration of a dissolved gas is proportional 
        to its partial pressure above the solution: c = k_H P, where k_H is the Henry's law constant. The law 
        applies to dilute solutions and non-reactive gases. Deviations occur with strong solute-solvent interactions 
        or at high pressures. Henry's law is critical for environmental chemistry, beverage carbonation, and 
        gas-liquid equilibria.
        """,
        key_factors=["partial pressure", "Henry's law constant", "solution ideality", "temperature"],
        primary_authority=["W. Henry", "IUPAC Gold Book"],
        burden_holder="Proponent of gas solubility prediction",
        adversary_position="Gas solubility is independent of pressure",
        counter_arguments=[
            "Experimental data confirm Henry's law for dilute solutions.",
            "Deviations are well understood and quantifiable.",
            "Law is widely applied in industry and research."
        ],
        resolution_strategy="Apply Henry's law and correct for non-ideality as needed.",
        entity_scope="Dilute gas-liquid systems",
        confidence=0.92,
        confidence_zone="Well Established",
        controlling_precedent="Henry's original studies"
    ),
    DoctrineBlock(
        topic="Van't Hoff Equation for Equilibrium",
        keywords=["van't Hoff equation", "temperature dependence", "equilibrium constant", "enthalpy change", "thermodynamics"],
        conclusion_template="The temperature dependence of the equilibrium constant is given by the van't Hoff equation.",
        reasoning_framework="""
        The van't Hoff equation relates the change in the equilibrium constant (K) with temperature to the standard 
        enthalpy change (ΔH°): d(ln K)/dT = ΔH°/(RT^2). Integration allows prediction of K at different temperatures. 
        The equation is derived from the Gibbs-Helmholtz equation and is widely used in chemical thermodynamics 
        to predict the effect of temperature on reaction equilibria.
        """,
        key_factors=["standard enthalpy change", "temperature", "equilibrium constant", "integration limits"],
        primary_authority=["J. H. van't Hoff", "IUPAC Gold Book"],
        burden_holder="Proponent of temperature effect on equilibrium",
        adversary_position="Equilibrium constant is independent of temperature",
        counter_arguments=[
            "Experimental data confirm van't Hoff predictions.",
            "Thermodynamic derivation is rigorous.",
            "Equation is widely used in chemical engineering."
        ],
        resolution_strategy="Apply van't Hoff equation and compare with experimental K values.",
        entity_scope="Temperature-dependent equilibria",
        confidence=0.94,
        confidence_zone="Well Established",
        controlling_precedent="van't Hoff's original derivation"
    ),
    DoctrineBlock(
        topic="Clapeyron and Clausius-Clapeyron Equations",
        keywords=["Clapeyron equation", "Clausius-Clapeyron", "phase transition", "vapor pressure", "enthalpy of vaporization"],
        conclusion_template="The Clausius-Clapeyron equation describes the temperature dependence of vapor pressure for phase transitions.",
        reasoning_framework="""
        The Clapeyron equation provides a general relationship between pressure, temperature, and enthalpy of 
        phase transitions. The Clausius-Clapeyron equation is a simplified form applicable to vaporization and 
        sublimation: d(ln P)/dT = ΔH_vap/(RT^2). Integration yields the vapor pressure as a function of temperature. 
        The equations are fundamental for determining enthalpy changes and constructing phase diagrams.
        """,
        key_factors=["enthalpy of transition", "temperature", "pressure", "phase boundaries"],
        primary_authority=["B. P. E. Clapeyron", "R. Clausius", "IUPAC Gold Book"],
        burden_holder="Proponent of phase transition analysis",
        adversary_position="Vapor pressure is independent of temperature",
        counter_arguments=[
            "Experimental vapor pressure data fit Clausius-Clapeyron equation.",
            "Thermodynamic derivation is rigorous.",
            "Equation is essential for phase diagram construction."
        ],
        resolution_strategy="Apply Clausius-Clapeyron equation to experimental data.",
        entity_scope="Phase transitions in pure substances",
        confidence=0.95,
        confidence_zone="Well Established",
        controlling_precedent="Clapeyron and Clausius original works"
    ),
    DoctrineBlock(
        topic="Nernst Heat Theorem (Third Law of Thermodynamics)",
        keywords=["Third Law", "Nernst heat theorem", "entropy", "absolute zero", "thermodynamics"],
        conclusion_template="As temperature approaches absolute zero, the entropy of a perfect crystal approaches zero.",
        reasoning_framework="""
        The Third Law of Thermodynamics, or Nernst heat theorem, states that the entropy of a perfect crystal 
        at absolute zero is exactly zero. This provides an absolute reference for entropy and explains the 
        unattainability of absolute zero. The law underpins the calculation of absolute entropies and the 
        behavior of materials at low temperatures. Deviations occur in systems with residual disorder or 
        non-crystalline phases.
        """,
        key_factors=["crystal perfection", "temperature", "entropy measurement", "residual entropy"],
        primary_authority=["W. Nernst", "IUPAC Gold Book"],
        burden_holder="Proponent of absolute entropy calculation",
        adversary_position="Entropy remains finite at absolute zero",
        counter_arguments=[
            "Experimental data support vanishing entropy for perfect crystals.",
            "Residual entropy is due to disorder, not a violation of the law.",
            "Third Law is foundational for low-temperature thermodynamics."
        ],
        resolution_strategy="Ensure crystal perfection and measure entropy at low temperatures.",
        entity_scope="Perfect crystals at low temperature",
        confidence=0.96,
        confidence_zone="Established Law",
        controlling_precedent="Nernst's original heat theorem"
    ),
    DoctrineBlock(
        topic="Surface Tension and Capillarity",
        keywords=["surface tension", "capillarity", "interfacial energy", "liquid", "contact angle"],
        conclusion_template="Surface tension arises from unbalanced molecular forces at interfaces and governs capillary phenomena.",
        reasoning_framework="""
        Surface tension is the energy required to increase the surface area of a liquid due to unbalanced 
        intermolecular forces at the interface. Capillarity describes the rise or depression of liquids in 
        narrow tubes, governed by surface tension and contact angle. The phenomena are quantified by the 
        Young-Laplace and Jurin equations. Surface tension is critical in biological, environmental, and 
        technological contexts.
        """,
        key_factors=["intermolecular forces", "contact angle", "tube radius", "liquid properties"],
        primary_authority=["IUPAC Gold Book", "P. Atkins, Physical Chemistry"],
        burden_holder="Proponent of surface tension explanation",
        adversary_position="Surface tension is unrelated to molecular forces",
        counter_arguments=[
            "Molecular models explain surface phenomena.",
            "Experimental measurements confirm theoretical predictions.",
            "Capillarity is quantitatively described by surface tension."
        ],
        resolution_strategy="Measure surface tension and analyze capillary rise.",
        entity_scope="Liquids and interfaces",
        confidence=0.93,
        confidence_zone="Well Established",
        controlling_precedent="Young-Laplace equation"
    ),
    DoctrineBlock(
        topic="Heat Capacity and Degrees of Freedom",
        keywords=["heat capacity", "degrees of freedom", "equipartition theorem", "molecular motion", "thermodynamics"],
        conclusion_template="Heat capacity is determined by the number and type of degrees of freedom accessible at a given temperature.",
        reasoning_framework="""
        The equipartition theorem of statistical mechanics states that each quadratic degree of freedom contributes 
        (1/2)k_BT to the average energy and thus to the heat capacity. Translational, rotational, and vibrational 
        modes contribute depending on temperature and quantum effects. Deviations from classical predictions occur 
        at low temperatures due to quantization. Heat capacity measurements provide insight into molecular structure 
        and bonding.
        """,
        key_factors=["degrees of freedom", "temperature", "quantum effects", "molecular structure"],
        primary_authority=["IUPAC Gold Book", "P. Atkins, Physical Chemistry"],
        burden_holder="Proponent of heat capacity prediction",
        adversary_position="Heat capacity is independent of molecular structure",
        counter_arguments=[
            "Experimental data confirm dependence on degrees of freedom.",
            "Quantum effects explain low-temperature deviations.",
            "Theory matches measured heat capacities."
        ],
        resolution_strategy="Apply equipartition theorem and correct for quantum effects.",
        entity_scope="Gases, liquids, and solids",
        confidence=0.94,
        confidence_zone="Well Established",
        controlling_precedent="Mayer's relation for gases"
    ),
    DoctrineBlock(
        topic="Kinetic Molecular Theory of Gases",
        keywords=["kinetic molecular theory", "gas laws", "molecular motion", "pressure", "temperature"],
        conclusion_template="Gas pressure and temperature arise from the collective motion of molecules, as described by kinetic theory.",
        reasoning_framework="""
        Kinetic molecular theory explains macroscopic gas properties in terms of molecular motion. Gas pressure 
        results from collisions of molecules with container walls, and temperature is proportional to average 
        kinetic energy. The theory derives the ideal gas law and predicts molecular speed distributions. Deviations 
        from ideality are explained by intermolecular forces and finite molecular volume. The theory is foundational 
        for understanding diffusion, effusion, and thermal conductivity.
        """,
        key_factors=["molecular velocity", "collision frequency", "mean free path", "temperature"],
        primary_authority=["IUPAC Gold Book", "J. C. Maxwell"],
        burden_holder="Proponent of kinetic theory explanation",
        adversary_position="Gas laws are unrelated to molecular motion",
        counter_arguments=[
            "Theory quantitatively predicts gas behavior.",
            "Experimental data confirm molecular speed distributions.",
            "Deviations are explained by real gas effects."
        ],
        resolution_strategy="Apply kinetic theory equations and compare with experiment.",
        entity_scope="Ideal and real gases",
        confidence=0.95,
        confidence_zone="Well Established",
        controlling_precedent="Maxwell-Boltzmann distribution"
    ),
    DoctrineBlock(
        topic="Zeroth Law of Thermodynamics",
        keywords=["zeroth law", "thermal equilibrium", "temperature", "transitivity", "thermodynamics"],
        conclusion_template="If two systems are each in thermal equilibrium with a third, they are in equilibrium with each other.",
        reasoning_framework="""
        The Zeroth Law of Thermodynamics establishes the concept of temperature and thermal equilibrium. If 
        system A is in equilibrium with system B, and B with C, then A and C are also in equilibrium. This 
        transitive property allows the definition of temperature as a measurable property and underpins the 
        construction of thermometers and temperature scales.
        """,
        key_factors=["thermal contact", "equilibrium", "temperature measurement", "transitivity"],
        primary_authority=["IUPAC Gold Book", "P. Atkins, Physical Chemistry"],
        burden_holder="Proponent of temperature comparison",
        adversary_position="Thermal equilibrium is not transitive",
        counter_arguments=[
            "Experimental evidence supports transitivity.",
            "Temperature scales are based on the zeroth law.",
            "Law is foundational for thermometry."
        ],
        resolution_strategy="Establish equilibrium via thermal contact and compare temperatures.",
        entity_scope="All thermodynamic systems",
        confidence=0.98,
        confidence_zone="Established Law",
        controlling_precedent="Development of temperature scales"
    ),
    DoctrineBlock(
        topic="Gibbs-Helmholtz Equation",
        keywords=["Gibbs-Helmholtz equation", "free energy", "enthalpy", "temperature dependence", "thermodynamics"],
        conclusion_template="The Gibbs-Helmholtz equation relates the temperature dependence of free energy to enthalpy.",
        reasoning_framework="""
        The Gibbs-Helmholtz equation expresses the relationship between the change in Gibbs free energy (ΔG) with 
        temperature and enthalpy (ΔH): (∂(ΔG/T)/∂T)_P = -ΔH/T^2. The equation is used to analyze the temperature 
        dependence of equilibrium constants and to extract enthalpy changes from free energy data. It is derived 
        from fundamental thermodynamic relationships and is widely applied in chemical thermodynamics.
        """,
        key_factors=["free energy", "enthalpy", "temperature", "partial derivatives"],
        primary_authority=["J. Willard Gibbs", "H. von Helmholtz", "IUPAC Gold Book"],
        burden_holder="Proponent of temperature dependence analysis",
        adversary_position="Free energy is independent of temperature",
        counter_arguments=[
            "Thermodynamic derivation is rigorous.",
            "Experimental data confirm predictions.",
            "Equation is essential for equilibrium analysis."
        ],
        resolution_strategy="Apply Gibbs-Helmholtz equation to experimental data.",
        entity_scope="Thermodynamic systems",
        confidence=0.95,
        confidence_zone="Well Established",
        controlling_precedent="Gibbs and Helmholtz original works"
    ),
    DoctrineBlock(
        topic="Fluorescence and Phosphorescence",
        keywords=["fluorescence", "phosphorescence", "excited state", "spin multiplicity", "radiative decay"],
        conclusion_template="Fluorescence and phosphorescence are radiative processes from excited states with different spin multiplicities.",
        reasoning_framework="""
        Fluorescence is the rapid emission of light as a molecule relaxes from an excited singlet state to the 
        ground state, typically within nanoseconds. Phosphorescence involves relaxation from an excited triplet 
        state to the singlet ground state, a spin-forbidden process that occurs on much longer timescales. The 
        distinction is rooted in quantum mechanical selection rules and spin multiplicity. Both processes are 
        central to spectroscopy, imaging, and materials science.
        """,
        key_factors=["excited state type", "spin selection rules", "lifetime", "quantum yield"],
        primary_authority=["IUPAC Gold Book", "N. J. Turro, Modern Molecular Photochemistry"],
        burden_holder="Proponent of emission mechanism",
        adversary_position="All radiative decay processes are identical",
        counter_arguments=[
            "Lifetimes and spectra differ between fluorescence and phosphorescence.",
            "Spin rules explain observed differences.",
            "Experimental techniques distinguish the processes."
        ],
        resolution_strategy="Measure emission lifetimes and analyze spectra.",
        entity_scope="Molecular photophysics",
        confidence=0.93,
        confidence_zone="Well Established",
        controlling_precedent="Jablonski diagram"
    ),
    DoctrineBlock(
        topic="Marcus Theory of Electron Transfer",
        keywords=["Marcus theory", "electron transfer", "reorganization energy", "kinetics", "redox"],
        conclusion_template="The rate of electron transfer depends on reorganization energy and driving force, as described by Marcus theory.",
        reasoning_framework="""
        Marcus theory provides a quantitative model for the rates of electron transfer reactions in solution. 
        The rate depends on the reorganization energy (λ), which reflects the structural changes needed for 
        electron transfer, and the thermodynamic driving force (ΔG°). The theory predicts an inverted region 
        where increasing driving force slows the reaction. Marcus theory is validated by extensive experimental 
        data and is central to understanding redox processes, photosynthesis, and molecular electronics.
        """,
        key_factors=["reorganization energy", "driving force", "solvent effects", "activation barrier"],
        primary_authority=["R. A. Marcus", "IUPAC Gold Book"],
        burden_holder="Proponent of electron transfer rate explanation",
        adversary_position="Electron transfer rates are independent of reorganization energy",
        counter_arguments=[
            "Experimental data confirm Marcus predictions.",
            "Theory explains inverted region and solvent effects.",
            "Widely applied in chemistry and biology."
        ],
        resolution_strategy="Measure rate constants and analyze with Marcus equation.",
        entity_scope="Redox reactions in solution",
        confidence=0.92,
        confidence_zone="Well Established",
        controlling_precedent="Marcus' original theory and Nobel Prize"
    ),
    DoctrineBlock(
        topic="Hückel Theory for Conjugated Systems",
        keywords=["Hückel theory", "conjugated systems", "π electrons", "molecular orbitals", "aromaticity"],
        conclusion_template="Hückel theory predicts the electronic structure and aromaticity of planar conjugated systems.",
        reasoning_framework="""
        Hückel molecular orbital theory is a simple quantum mechanical model for π electron systems in planar 
        conjugated hydrocarbons. The theory predicts energy levels, delocalization, and aromatic stabilization. 
        It explains the 4n+2 rule for aromaticity and provides qualitative predictions for UV-Vis spectra and 
        reactivity. Despite its simplicity, Hückel theory captures essential features of conjugated systems.
        """,
        key_factors=["planarity", "π electron count", "molecular symmetry", "delocalization"],
        primary_authority=["E. Hückel", "IUPAC Gold Book"],
        burden_holder="Proponent of Hückel theory application",
        adversary_position="Conjugated systems require more complex models",
        counter_arguments=[
            "Hückel theory provides accurate qualitative predictions.",
            "Aromaticity and spectra are explained by the model.",
            "Extensions improve quantitative accuracy."
        ],
        resolution_strategy="Apply Hückel theory to relevant systems and compare with experiment.",
        entity_scope="Planar conjugated hydrocarbons",
        confidence=0.90,
        confidence_zone="Well Established",
        controlling_precedent="Hückel's original aromaticity studies"
    ),
    DoctrineBlock(
        topic="Langmuir Adsorption Model",
        keywords=["Langmuir model", "adsorption", "monolayer", "surface coverage", "isotherm"],
        conclusion_template="The Langmuir model describes monolayer adsorption on a homogeneous surface with finite sites.",
        reasoning_framework="""
        The Langmuir adsorption model assumes a fixed number of identical sites on a surface, each capable of 
        binding one adsorbate molecule. The model yields an isotherm relating surface coverage (θ) to adsorbate 
        concentration (C): θ = (KC)/(1 + KC), where K is the adsorption equilibrium constant. The model is 
        foundational for surface chemistry and catalysis, though deviations indicate heterogeneity or multilayer 
        adsorption.
        """,
        key_factors=["site homogeneity", "monolayer coverage", "adsorption equilibrium constant", "surface area"],
        primary_authority=["I. Langmuir", "IUPAC Gold Book"],
        burden_holder="Proponent of Langmuir model application",
        adversary_position="Adsorption is always multilayer or heterogeneous",
        counter_arguments=[
            "Many systems fit Langmuir model at low coverage.",
            "Deviations are well characterized.",
            "Model is essential for surface area determination."
        ],
        resolution_strategy="Fit adsorption data to Langmuir isotherm and assess fit quality.",
        entity_scope="Surface adsorption processes",
        confidence=0.91,
        confidence_zone="Well Established",
        controlling_precedent="Langmuir's original adsorption studies"
    ),
    DoctrineBlock(
        topic="Pseudofirst-Order Kinetics",
        keywords=["pseudofirst-order", "kinetics", "excess reactant", "rate law", "simplification"],
        conclusion_template="When one reactant is in large excess, the reaction follows pseudofirst-order kinetics.",
        reasoning_framework="""
        In reactions where one reactant is present in large excess, its concentration remains effectively constant, 
        simplifying the rate law to first-order in the limiting reactant. This allows easier determination of rate 
        constants and mechanistic analysis. The approach is widely used in kinetics experiments and in biological 
        systems where substrates are buffered.
        """,
        key_factors=["excess reactant", "rate law simplification", "experimental design", "data analysis"],
        primary_authority=["IUPAC Gold Book", "P. Atkins, Physical Chemistry"],
        burden_holder="Proponent of pseudofirst-order analysis",
        adversary_position="All reactants must be treated explicitly",
        counter_arguments=[
            "Mathematical simplification is valid under excess conditions.",
            "Experimental results confirm pseudofirst-order behavior.",
            "Approach is standard in kinetics studies."
        ],
        resolution_strategy="Ensure excess of one reactant and analyze data accordingly.",
        entity_scope="Kinetic experiments with excess reactant",
        confidence=0