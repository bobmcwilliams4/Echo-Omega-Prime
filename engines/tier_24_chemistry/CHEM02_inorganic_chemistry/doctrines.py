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
        topic="Crystal Field Stabilization Energy in Octahedral Complexes",
        keywords=["crystal field theory", "octahedral", "CFSE", "ligand field", "transition metals"],
        conclusion_template="The crystal field stabilization energy (CFSE) for an octahedral complex is determined by the electronic configuration of the metal ion and the nature of the ligands.",
        reasoning_framework=(
            "1. Identify the metal ion and its oxidation state.\n"
            "2. Determine the d-electron count for the metal center.\n"
            "3. Assign electrons to the t2g and eg orbitals according to Hund's rule and the crystal field splitting pattern.\n"
            "4. Calculate the CFSE using the formula: CFSE = (-0.4 × number of t2g electrons + 0.6 × number of eg electrons)Δo.\n"
            "5. Account for pairing energy if relevant.\n"
            "6. Consider the spectrochemical series to estimate Δo for the specific ligand field.\n"
            "7. Conclude the relative stability and magnetic properties based on CFSE value."
        ),
        key_factors=["d-electron count", "ligand field strength", "pairing energy", "geometry"],
        primary_authority=["Cotton & Wilkinson, Advanced Inorganic Chemistry", "Miessler, Fischer & Tarr, Inorganic Chemistry"],
        burden_holder="Proponent of specific electronic configuration",
        adversary_position="Alternative electron arrangements or geometries",
        counter_arguments=[
            "Jahn-Teller distortions may alter orbital energies.",
            "High-spin vs low-spin configurations can change CFSE.",
            "π-bonding effects may not be fully captured by simple crystal field theory."
        ],
        resolution_strategy="Apply ligand field theory corrections and consider experimental spectroscopic data.",
        entity_scope="Transition metal octahedral complexes",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Crystal Field Theory (Bethe, 1929); Spectrochemical Series"
    ),
    DoctrineBlock(
        topic="Chelate Effect in Coordination Chemistry",
        keywords=["chelation", "stability", "entropy", "ligand", "thermodynamics"],
        conclusion_template="Chelating ligands form more stable complexes than analogous monodentate ligands due to the chelate effect.",
        reasoning_framework=(
            "1. Compare the formation constants (Kf) for chelating vs monodentate ligand complexes.\n"
            "2. Analyze the entropy change upon complex formation: chelation releases more solvent molecules, increasing entropy.\n"
            "3. Consider the enthalpic contribution: ring formation may provide additional stabilization.\n"
            "4. Evaluate the number of possible chelate rings and their sizes.\n"
            "5. Reference empirical data from stability series and formation constants.\n"
            "6. Conclude that the chelate effect is primarily entropic in origin, but also benefits from enthalpic contributions."
        ),
        key_factors=["ligand denticity", "ring size", "entropy change", "formation constant"],
        primary_authority=["Huheey, Inorganic Chemistry: Principles of Structure and Reactivity", "Martell & Hancock, Metal Complexes in Aqueous Solutions"],
        burden_holder="Advocate for chelating ligand superiority",
        adversary_position="Monodentate ligands can achieve similar stability under certain conditions",
        counter_arguments=[
            "Steric hindrance may reduce chelate stability.",
            "Macrocyclic ligands may not always outperform polydentate open-chain ligands.",
            "Solvent effects can modulate the chelate effect."
        ],
        resolution_strategy="Quantitative comparison of stability constants and thermodynamic parameters.",
        entity_scope="Coordination complexes with chelating ligands",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Werner’s Coordination Theory; Irving-Williams Series"
    ),
    DoctrineBlock(
        topic="Jahn-Teller Distortion in d9 Octahedral Complexes",
        keywords=["Jahn-Teller effect", "octahedral", "d9", "Cu(II)", "distortion"],
        conclusion_template="Octahedral d9 complexes exhibit Jahn-Teller distortion, typically elongating along one axis.",
        reasoning_framework=(
            "1. Recognize that d9 configuration (e.g., Cu(II)) in octahedral field leads to electronic degeneracy in eg orbitals.\n"
            "2. Apply the Jahn-Teller theorem: any non-linear molecule with degenerate electronic states will distort to remove degeneracy.\n"
            "3. Predict the distortion: elongation (z-axis) or compression, with elongation being more common for d9.\n"
            "4. Relate distortion to spectroscopic and magnetic properties.\n"
            "5. Cite structural data from X-ray crystallography and EPR spectra."
        ),
        key_factors=["electronic degeneracy", "orbital occupancy", "structural data"],
        primary_authority=["Jahn & Teller, Proceedings of the Royal Society A (1937)", "Cotton & Wilkinson, Advanced Inorganic Chemistry"],
        burden_holder="Proponent of distortion mechanism",
        adversary_position="Complexes with minimal or no distortion",
        counter_arguments=[
            "Strong ligand fields may suppress distortion.",
            "Solid-state packing can influence observed geometry.",
            "Dynamic (rather than static) distortion may occur."
        ],
        resolution_strategy="Combine theoretical predictions with experimental evidence (XRD, EPR).",
        entity_scope="Octahedral d9 transition metal complexes",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Jahn-Teller Theorem (1937)"
    ),
    DoctrineBlock(
        topic="Spectrochemical Series and Ligand Field Strength",
        keywords=["spectrochemical series", "ligand field", "Δo", "crystal field splitting", "transition metals"],
        conclusion_template="Ligands are ordered in the spectrochemical series according to their ability to split d-orbital energies in transition metal complexes.",
        reasoning_framework=(
            "1. Define the spectrochemical series as an empirical ordering of ligands by their field strength.\n"
            "2. Strong field ligands (e.g., CN-, CO) produce large Δo, favoring low-spin complexes.\n"
            "3. Weak field ligands (e.g., I-, Br-) produce small Δo, favoring high-spin complexes.\n"
            "4. Use UV-Vis spectroscopy to determine Δo for specific complexes.\n"
            "5. Relate ligand field strength to electronic transitions and magnetic properties."
        ),
        key_factors=["ligand identity", "Δo value", "spin state", "spectroscopic data"],
        primary_authority=["Cotton & Wilkinson, Advanced Inorganic Chemistry", "Miessler, Fischer & Tarr, Inorganic Chemistry"],
        burden_holder="Proponent of ligand ordering",
        adversary_position="Exceptions to the series in specific cases",
        counter_arguments=[
            "π-backbonding can alter ligand field strength.",
            "Steric effects may override electronic trends.",
            "Series is empirical and may not apply to all metals."
        ],
        resolution_strategy="Refer to experimental Δo values and electronic spectra.",
        entity_scope="Transition metal complexes",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Spectrochemical Series (Werner, 1893; empirical data)"
    ),
    DoctrineBlock(
        topic="High-Spin vs Low-Spin Configurations in Octahedral Complexes",
        keywords=["high-spin", "low-spin", "octahedral", "crystal field", "spin pairing"],
        conclusion_template="The spin state of an octahedral complex depends on the relative magnitudes of crystal field splitting energy (Δo) and pairing energy.",
        reasoning_framework=(
            "1. Calculate Δo for the metal-ligand combination using the spectrochemical series.\n"
            "2. Compare Δo to the electron pairing energy (P).\n"
            "3. If Δo < P, electrons occupy higher energy eg orbitals (high-spin); if Δo > P, electrons pair in t2g orbitals (low-spin).\n"
            "4. Consider the effect on magnetic properties: high-spin complexes are more paramagnetic.\n"
            "5. Analyze experimental data (magnetic susceptibility, electronic spectra) for confirmation."
        ),
        key_factors=["Δo", "pairing energy", "ligand identity", "metal ion"],
        primary_authority=["Miessler, Fischer & Tarr, Inorganic Chemistry", "Cotton & Wilkinson, Advanced Inorganic Chemistry"],
        burden_holder="Proponent of predicted spin state",
        adversary_position="Alternative spin state assignment",
        counter_arguments=[
            "Intermediate spin states may occur in some cases.",
            "Spin crossover phenomena can complicate predictions.",
            "Solvent and temperature effects may alter spin state."
        ],
        resolution_strategy="Corroborate with experimental magnetic and spectroscopic data.",
        entity_scope="Octahedral transition metal complexes",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Crystal Field Theory; Spectrochemical Series"
    ),
    DoctrineBlock(
        topic="Hard and Soft Acids and Bases (HSAB) Principle",
        keywords=["HSAB", "Pearson", "acid", "base", "stability", "reactivity"],
        conclusion_template="Hard acids prefer to bind to hard bases, and soft acids to soft bases, maximizing complex stability.",
        reasoning_framework=(
            "1. Define hard acids/bases as small, non-polarizable species; soft acids/bases as large, polarizable species.\n"
            "2. Use Pearson's HSAB theory to predict preferred interactions.\n"
            "3. Rationalize stability trends in metal-ligand complexes and inorganic reactions.\n"
            "4. Apply to predict product distribution in competitive binding scenarios.\n"
            "5. Reference empirical data and exceptions (e.g., borderline cases)."
        ),
        key_factors=["acid/base hardness", "polarizability", "ionic/covalent character"],
        primary_authority=["Pearson, J. Chem. Educ. 1963, 40, 12, 640", "Huheey, Inorganic Chemistry"],
        burden_holder="Proponent of predicted binding preference",
        adversary_position="Observed exceptions to HSAB predictions",
        counter_arguments=[
            "Steric effects may override HSAB predictions.",
            "Solvent and temperature can modulate acid/base character.",
            "HSAB is a qualitative, not quantitative, principle."
        ],
        resolution_strategy="Combine HSAB with thermodynamic and kinetic data.",
        entity_scope="All inorganic acid-base interactions",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Pearson’s HSAB Principle (1963)"
    ),
    DoctrineBlock(
        topic="Trans Effect in Square Planar Complexes",
        keywords=["trans effect", "square planar", "ligand substitution", "Pt(II)", "kinetics"],
        conclusion_template="Ligands with strong trans effects accelerate substitution of ligands trans to themselves in square planar complexes.",
        reasoning_framework=(
            "1. Identify the square planar complex and the ligands involved.\n"
            "2. Rank ligands by their trans effect: strong σ-donors and π-acceptors have higher trans effects.\n"
            "3. Predict the site of ligand substitution based on the trans effect.\n"
            "4. Rationalize with kinetic data and observed product distributions.\n"
            "5. Reference classic examples (e.g., Pt(II) ammine complexes)."
        ),
        key_factors=["ligand identity", "σ-donor/π-acceptor ability", "kinetic data"],
        primary_authority=["Basolo & Pearson, Mechanisms of Inorganic Reactions", "Miessler, Fischer & Tarr, Inorganic Chemistry"],
        burden_holder="Proponent of predicted substitution pathway",
        adversary_position="Alternative substitution mechanisms",
        counter_arguments=[
            "Steric effects may influence substitution site.",
            "Solvent and temperature can alter kinetic preferences.",
            "Trans influence (thermodynamic) may differ from trans effect (kinetic)."
        ],
        resolution_strategy="Analyze kinetic data and product distributions.",
        entity_scope="Square planar transition metal complexes",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Trans Effect (I. J. K. Basolo, R. G. Pearson, 1958)"
    ),
    DoctrineBlock(
        topic="Lanthanide Contraction and Its Consequences",
        keywords=["lanthanide contraction", "atomic radius", "periodic trends", "f-block", "chemistry"],
        conclusion_template="The lanthanide contraction results in smaller than expected atomic and ionic radii for post-lanthanide elements, affecting their chemistry.",
        reasoning_framework=(
            "1. Recognize that poor shielding by 4f electrons leads to increased effective nuclear charge across the lanthanide series.\n"
            "2. Observe the steady decrease in atomic and ionic radii from La to Lu.\n"
            "3. Note the impact on the chemistry of subsequent elements (e.g., Zr/Hf, Nb/Ta pairs).\n"
            "4. Relate to separation difficulties and similarities in chemical behavior.\n"
            "5. Reference empirical measurements of ionic radii and periodic trends."
        ),
        key_factors=["4f electron shielding", "atomic/ionic radius", "periodic trends"],
        primary_authority=["Cotton, Advanced Inorganic Chemistry", "Greenwood & Earnshaw, Chemistry of the Elements"],
        burden_holder="Proponent of contraction effects",
        adversary_position="Alternative explanations for observed trends",
        counter_arguments=[
            "Relativistic effects also contribute to contraction.",
            "d-block contraction can confound observed trends.",
            "Experimental uncertainties in radii measurements."
        ],
        resolution_strategy="Compare empirical data across the periodic table.",
        entity_scope="Lanthanides and post-lanthanide elements",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Lanthanide Contraction (Goldschmidt, 1925)"
    ),
    DoctrineBlock(
        topic="Oxidation States of Transition Metals",
        keywords=["oxidation state", "transition metals", "variable valency", "redox", "chemistry"],
        conclusion_template="Transition metals exhibit multiple oxidation states due to the similar energies of their (n-1)d and ns electrons.",
        reasoning_framework=(
            "1. Identify the electron configuration of the transition metal.\n"
            "2. Note the small energy difference between (n-1)d and ns orbitals.\n"
            "3. Rationalize the accessibility of multiple oxidation states.\n"
            "4. Relate to the variety of compounds and redox chemistry observed.\n"
            "5. Reference standard reduction potentials and common oxidation states."
        ),
        key_factors=["electron configuration", "orbital energies", "redox chemistry"],
        primary_authority=["Cotton & Wilkinson, Advanced Inorganic Chemistry", "Miessler, Fischer & Tarr, Inorganic Chemistry"],
        burden_holder="Proponent of oxidation state assignment",
        adversary_position="Alternative oxidation state assignments",
        counter_arguments=[
            "Ligand field can stabilize unusual oxidation states.",
            "Solid-state effects may alter accessible states.",
            "Experimental ambiguities in assigning oxidation numbers."
        ],
        resolution_strategy="Combine spectroscopic, magnetic, and electrochemical data.",
        entity_scope="Transition metal compounds",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Transition Metal Chemistry (General)"
    ),
    DoctrineBlock(
        topic="18-Electron Rule in Organometallic Chemistry",
        keywords=["18-electron rule", "organometallic", "valence electron count", "stability", "transition metals"],
        conclusion_template="Stable organometallic complexes of transition metals often obey the 18-electron rule, analogous to the noble gas configuration.",
        reasoning_framework=(
            "1. Count the total valence electrons on the metal center, including those donated by ligands.\n"
            "2. Compare the total to 18 electrons, which fills the s, p, and d orbitals.\n"
            "3. Rationalize stability for complexes that obey the rule (e.g., [Fe(CO)5], [Cr(CO)6]).\n"
            "4. Note exceptions: electron-deficient or electron-rich complexes may be stabilized by other factors.\n"
            "5. Reference empirical data and molecular orbital diagrams."
        ),
        key_factors=["valence electron count", "ligand type", "molecular orbital filling"],
        primary_authority=["Elschenbroich, Organometallics", "Miessler, Fischer & Tarr, Inorganic Chemistry"],
        burden_holder="Proponent of electron count rationale",
        adversary_position="Stable complexes with non-18 electron counts",
        counter_arguments=[
            "Steric bulk can stabilize 16-electron species.",
            "π-acidic ligands may allow for exceptions.",
            "Cluster compounds may not follow the rule."
        ],
        resolution_strategy="Analyze molecular orbital diagrams and reactivity.",
        entity_scope="Transition metal organometallic complexes",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="18-Electron Rule (General)"
    ),
    DoctrineBlock(
        topic="Ligand Substitution Mechanisms in Octahedral Complexes",
        keywords=["ligand substitution", "octahedral", "associative", "dissociative", "interchange"],
        conclusion_template="Ligand substitution in octahedral complexes can proceed via associative, dissociative, or interchange mechanisms, depending on the complex and conditions.",
        reasoning_framework=(
            "1. Classify the complex as labile or inert based on the metal and ligands.\n"
            "2. Analyze kinetic data: first-order (dissociative) or second-order (associative/interchange).\n"
            "3. Consider the effect of entering and leaving group properties.\n"
            "4. Use activation parameters (ΔH‡, ΔS‡) to distinguish mechanisms.\n"
            "5. Reference classic studies on Cr(III), Co(III), and Pt(II) complexes."
        ),
        key_factors=["kinetic data", "activation parameters", "metal/ligand identity"],
        primary_authority=["Basolo & Pearson, Mechanisms of Inorganic Reactions", "Taube, Inorganic Reaction Mechanisms"],
        burden_holder="Proponent of mechanism assignment",
        adversary_position="Alternative substitution pathway",
        counter_arguments=[
            "Solvent and ionic strength can alter mechanism.",
            "Intermediate formation may complicate analysis.",
            "Multiple pathways may operate simultaneously."
        ],
        resolution_strategy="Integrate kinetic, thermodynamic, and spectroscopic data.",
        entity_scope="Octahedral transition metal complexes",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Mechanisms of Inorganic Reactions (Basolo & Pearson)"
    ),
    DoctrineBlock(
        topic="π-Acceptor Ligands and Backbonding",
        keywords=["π-acceptor", "backbonding", "CO", "phosphines", "metal-ligand bonding"],
        conclusion_template="π-Acceptor ligands stabilize low oxidation state metals via synergic bonding: σ-donation from ligand and π-backdonation from metal.",
        reasoning_framework=(
            "1. Identify ligands capable of π-acceptance (e.g., CO, NO+, phosphines).\n"
            "2. Describe synergic bonding: ligand donates electron density via σ-bond, metal donates back via π-bond.\n"
            "3. Rationalize stabilization of low oxidation states and observed spectroscopic shifts (e.g., IR CO stretching frequency).\n"
            "4. Reference molecular orbital diagrams and empirical data."
        ),
        key_factors=["ligand π-acceptor ability", "metal electron density", "spectroscopic evidence"],
        primary_authority=["Elschenbroich, Organometallics", "Cotton & Wilkinson, Advanced Inorganic Chemistry"],
        burden_holder="Proponent of backbonding mechanism",
        adversary_position="Purely σ-bonding or alternative explanations",
        counter_arguments=[
            "Steric effects may limit backbonding.",
            "Not all low-valent metals engage in strong backbonding.",
            "Spectroscopic shifts may have multiple causes."
        ],
        resolution_strategy="Correlate IR, NMR, and X-ray data with bonding models.",
        entity_scope="Transition metal π-acceptor complexes",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Synergic Bonding Model (Dewar-Chatt-Duncanson, 1951)"
    ),
    DoctrineBlock(
        topic="Symmetry Elements and Point Groups in Inorganic Molecules",
        keywords=["symmetry", "point group", "molecular structure", "group theory", "character table"],
        conclusion_template="Molecules are classified into point groups based on their symmetry elements, which dictate their spectroscopic and physical properties.",
        reasoning_framework=(
            "1. Identify all symmetry elements present: rotation axes, mirror planes, inversion centers, improper axes.\n"
            "2. Assign the molecule to a point group using systematic flowcharts.\n"
            "3. Use character tables to predict IR/Raman activity and orbital degeneracies.\n"
            "4. Reference standard group theory texts and spectroscopic data."
        ),
        key_factors=["symmetry elements", "molecular geometry", "spectroscopic properties"],
        primary_authority=["Cotton, Chemical Applications of Group Theory", "Atkins & Overton, Shriver & Atkins' Inorganic Chemistry"],
        burden_holder="Proponent of point group assignment",
        adversary_position="Alternative symmetry assignments",
        counter_arguments=[
            "Dynamic disorder may obscure symmetry.",
            "Substituent effects can lower symmetry.",
            "Experimental data may be ambiguous."
        ],
        resolution_strategy="Combine structural and spectroscopic analysis.",
        entity_scope="All inorganic molecules",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Group Theory (Cotton, 1963)"
    ),
    DoctrineBlock(
        topic="Thermodynamic vs Kinetic Control in Inorganic Reactions",
        keywords=["thermodynamics", "kinetics", "reaction control", "inorganic", "product distribution"],
        conclusion_template="The product distribution in inorganic reactions depends on whether conditions favor thermodynamic or kinetic control.",
        reasoning_framework=(
            "1. Define thermodynamic product as the most stable, and kinetic product as the one formed fastest.\n"
            "2. Analyze reaction conditions: temperature, solvent, catalyst.\n"
            "3. Use activation energy and reaction coordinate diagrams.\n"
            "4. Reference experimental data on product ratios under varying conditions.\n"
            "5. Apply to classic cases (e.g., isomerization, ligand substitution)."
        ),
        key_factors=["activation energy", "reaction conditions", "product stability"],
        primary_authority=["Atkins & Overton, Shriver & Atkins' Inorganic Chemistry", "Basolo & Pearson, Mechanisms of Inorganic Reactions"],
        burden_holder="Proponent of control regime",
        adversary_position="Alternative product distribution explanations",
        counter_arguments=[
            "Reversible reactions may reach equilibrium regardless of initial control.",
            "Competing side reactions can obscure analysis.",
            "Experimental determination of control may be challenging."
        ],
        resolution_strategy="Vary reaction conditions and analyze resulting product ratios.",
        entity_scope="Inorganic reaction systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Thermodynamic/Kinetic Control Paradigm"
    ),
    DoctrineBlock(
        topic="Redox Potentials and the Nernst Equation",
        keywords=["redox", "Nernst equation", "electrochemistry", "potential", "inorganic"],
        conclusion_template="The Nernst equation relates the redox potential of a half-cell to the concentrations of reactants and products.",
        reasoning_framework=(
            "1. Write the half-cell reaction and identify standard reduction potential (E°).\n"
            "2. Apply the Nernst equation: E = E° - (RT/nF)ln(Q), where Q is the reaction quotient.\n"
            "3. Calculate cell potential under non-standard conditions.\n"
            "4. Use to predict spontaneity and direction of redox reactions.\n"
            "5. Reference standard tables and experimental measurements."
        ),
        key_factors=["concentration", "temperature", "number of electrons transferred"],
        primary_authority=["Bard & Faulkner, Electrochemical Methods", "Atkins & Overton, Shriver & Atkins' Inorganic Chemistry"],
        burden_holder="Proponent of calculated potential",
        adversary_position="Observed potentials deviate from predictions",
        counter_arguments=[
            "Junction potentials and activity coefficients can affect measurements.",
            "Non-ideal behavior in concentrated solutions.",
            "Electrode surface effects."
        ],
        resolution_strategy="Correct for non-idealities and compare with experimental data.",
        entity_scope="Inorganic redox systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Nernst Equation (Walther Nernst, 1889)"
    ),
    DoctrineBlock(
        topic="Band Theory of Solids",
        keywords=["band theory", "solid state", "conductors", "semiconductors", "insulators"],
        conclusion_template="The electronic properties of solids are explained by band theory, distinguishing conductors, semiconductors, and insulators.",
        reasoning_framework=(
            "1. Model the solid as a periodic array of atoms; atomic orbitals combine to form bands.\n"
            "2. Define the valence and conduction bands; band gap separates them.\n"
            "3. Conductors have overlapping bands; semiconductors have small gaps; insulators have large gaps.\n"
            "4. Relate to electrical conductivity and optical properties.\n"
            "5. Reference experimental data (e.g., resistivity, absorption spectra)."
        ),
        key_factors=["band gap", "electron mobility", "crystal structure"],
        primary_authority=["Ashcroft & Mermin, Solid State Physics", "Atkins & Overton, Shriver & Atkins' Inorganic Chemistry"],
        burden_holder="Proponent of band assignment",
        adversary_position="Localized electron models (e.g., valence bond theory)",
        counter_arguments=[
            "Defects and impurities can dominate properties.",
            "Strong electron correlations may invalidate simple band theory.",
            "Low-dimensional systems may require alternative models."
        ],
        resolution_strategy="Combine band theory with experimental characterization.",
        entity_scope="Solid state inorganic materials",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Band Theory (Bloch, 1928)"
    ),
    DoctrineBlock(
        topic="Schottky and Frenkel Defects in Ionic Solids",
        keywords=["Schottky defect", "Frenkel defect", "ionic solids", "crystal defects", "solid state"],
        conclusion_template="Ionic solids can exhibit Schottky (vacancy) and Frenkel (displacement) defects, affecting their properties.",
        reasoning_framework=(
            "1. Define Schottky defect: paired cation and anion vacancies.\n"
            "2. Define Frenkel defect: cation displaced to interstitial site, leaving a vacancy.\n"
            "3. Relate defect concentration to temperature and crystal structure.\n"
            "4. Analyze impact on ionic conductivity and density.\n"
            "5. Reference classic examples (e.g., NaCl, AgCl)."
        ),
        key_factors=["crystal structure", "ionic size", "temperature"],
        primary_authority=["West, Solid State Chemistry", "Atkins & Overton, Shriver & Atkins' Inorganic Chemistry"],
        burden_holder="Proponent of defect mechanism",
        adversary_position="Alternative defect types or mechanisms",
        counter_arguments=[
            "Non-stoichiometry can complicate defect analysis.",
            "Defect clustering may occur at high concentrations.",
            "Experimental detection of defects can be challenging."
        ],
        resolution_strategy="Combine crystallographic and conductivity measurements.",
        entity_scope="Ionic inorganic solids",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Defect Chemistry (Schottky, 1930; Frenkel, 1926)"
    ),
    DoctrineBlock(
        topic="Catalysis: Homogeneous vs Heterogeneous",
        keywords=["catalysis", "homogeneous", "heterogeneous", "mechanism", "inorganic"],
        conclusion_template="Homogeneous catalysts operate in the same phase as reactants, while heterogeneous catalysts are in a different phase; both have distinct mechanistic features.",
        reasoning_framework=(
            "1. Define homogeneous catalysis: catalyst and reactants in same phase (usually solution).\n"
            "2. Define heterogeneous catalysis: catalyst is a solid, reactants are gases or liquids.\n"
            "3. Compare mechanisms: homogeneous often involves well-defined intermediates; heterogeneous involves adsorption, surface reaction, desorption.\n"
            "4. Evaluate advantages and limitations of each type.\n"
            "5. Reference industrial examples (e.g., Wilkinson's catalyst, Haber process)."
        ),
        key_factors=["phase", "mechanistic pathway", "catalyst recovery", "selectivity"],
        primary_authority=["Atkins & Overton, Shriver & Atkins' Inorganic Chemistry", "Somorjai, Introduction to Surface Chemistry and Catalysis"],
        burden_holder="Proponent of catalytic classification",
        adversary_position="Ambiguous cases (e.g., supported homogeneous catalysts)",
        counter_arguments=[
            "Phase transfer catalysts blur the distinction.",
            "Nanoparticle catalysts may exhibit both behaviors.",
            "Catalyst leaching can complicate classification."
        ],
        resolution_strategy="Analyze reaction conditions and catalyst structure.",
        entity_scope="Inorganic catalytic systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Catalysis Classification (General)"
    ),
    DoctrineBlock(
        topic="Bioinorganic Chemistry of Hemoglobin",
        keywords=["bioinorganic", "hemoglobin", "iron", "oxygen transport", "heme"],
        conclusion_template="Hemoglobin utilizes an iron(II) heme center to reversibly bind oxygen, enabling biological oxygen transport.",
        reasoning_framework=(
            "1. Describe the structure of heme: porphyrin ring with central Fe(II).\n"
            "2. Explain reversible O2 binding: Fe(II) binds O2, forming an Fe(II)-O2 adduct.\n"
            "3. Discuss cooperative binding and allosteric effects in hemoglobin tetramer.\n"
            "4. Relate to physiological function and spectroscopic properties.\n"
            "5. Reference X-ray and spectroscopic studies."
        ),
        key_factors=["iron oxidation state", "porphyrin structure", "O2 binding affinity"],
        primary_authority=["Bertini, Gray, Stiefel & Valentine, Biological Inorganic Chemistry", "Lippard & Berg, Principles of Bioinorganic Chemistry"],
        burden_holder="Proponent of Fe(II)-O2 binding mechanism",
        adversary_position="Alternative oxygen transport mechanisms",
        counter_arguments=[
            "Methemoglobin (Fe(III)) cannot bind O2.",
            "Other metalloproteins (e.g., hemocyanin) use different metals.",
            "Cooperative binding is not universal."
        ],
        resolution_strategy="Combine structural, kinetic, and physiological data.",
        entity_scope="Oxygen transport proteins",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Hemoglobin Structure (Perutz, 1960)"
    ),
    DoctrineBlock(
        topic="Acid-Base Concepts: Arrhenius, Brønsted-Lowry, Lewis",
        keywords=["acid-base", "Arrhenius", "Brønsted-Lowry", "Lewis", "proton", "electron pair"],
        conclusion_template="Acid-base behavior can be described by Arrhenius (H+/OH-), Brønsted-Lowry (proton donor/acceptor), or Lewis (electron pair acceptor/donor) definitions.",
        reasoning_framework=(
            "1. Define Arrhenius acids/bases: produce H+ or OH- in water.\n"
            "2. Define Brønsted-Lowry acids/bases: donate or accept protons.\n"
            "3. Define Lewis acids/bases: accept or donate electron pairs.\n"
            "4. Apply each concept to a range of inorganic reactions.\n"
            "5. Reference classic examples and limitations of each model."
        ),
        key_factors=["proton transfer", "electron pair transfer", "solvent effects"],
        primary_authority=["Atkins & Overton, Shriver & Atkins' Inorganic Chemistry", "Huheey, Inorganic Chemistry"],
        burden_holder="Proponent of acid-base classification",
        adversary_position="Alternative or overlapping definitions",
        counter_arguments=[
            "Some reactions fit multiple definitions.",
            "Solvent and context can change acid/base character.",
            "Lewis concept is the most general but least specific."
        ],
        resolution_strategy="Select the most applicable model for the reaction in question.",
        entity_scope="All inorganic acid-base reactions",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Acid-Base Theories (Arrhenius, 1887; Brønsted, 1923; Lewis, 1923)"
    ),
    DoctrineBlock(
        topic="Nuclear Stability and Magic Numbers",
        keywords=["nuclear chemistry", "magic numbers", "stability", "nucleons", "isotopes"],
        conclusion_template="Nuclei with magic numbers of protons or neutrons exhibit enhanced stability due to closed shells.",
        reasoning_framework=(
            "1. Define magic numbers: 2, 8, 20, 28, 50, 82, 126.\n"
            "2. Relate to nuclear shell model: closed shells confer extra stability.\n"
            "3. Observe abundance of isotopes with magic numbers.\n"
            "4. Reference nuclear binding energy and decay data.\n"
            "5. Note limitations and exceptions (e.g., deformation in heavy nuclei)."
        ),
        key_factors=["proton/neutron number", "shell closure", "binding energy"],
        primary_authority=["Krane, Introductory Nuclear Physics", "Atkins & Overton, Shriver & Atkins' Inorganic Chemistry"],
        burden_holder="Proponent of magic number stability",
        adversary_position="Alternative explanations for nuclear stability",
        counter_arguments=[
            "Pairing effects also contribute to stability.",
            "Deformed nuclei may be more stable than spherical ones.",
            "Shell model is not universally applicable."
        ],
        resolution_strategy="Combine shell model predictions with empirical data.",
        entity_scope="Atomic nuclei",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Nuclear Shell Model (Mayer & Jensen, 1949)"
    ),
    DoctrineBlock(
        topic="Ziegler-Natta Polymerization Catalysis",
        keywords=["Ziegler-Natta", "polymerization", "catalysis", "olefins", "TiCl4", "AlEt3"],
        conclusion_template="Ziegler-Natta catalysts enable stereospecific polymerization of olefins via coordination-insertion mechanisms.",
        reasoning_framework=(
            "1. Describe the catalyst system: transition metal halide (e.g., TiCl4) and organoaluminum co-catalyst (e.g., AlEt3).\n"
            "2. Outline the coordination-insertion mechanism: olefin coordinates to metal, inserts into metal-carbon bond.\n"
            "3. Rationalize stereospecificity and control of polymer microstructure.\n"
            "4. Reference industrial applications and empirical data.\n"
            "5. Note limitations and advances (e.g., metallocene catalysts)."
        ),
        key_factors=["catalyst composition", "mechanism", "polymer microstructure"],
        primary_authority=["Chadwick & Jones, Olefin Polymerization", "Atkins & Overton, Shriver & Atkins' Inorganic Chemistry"],
        burden_holder="Proponent of mechanism and catalyst classification",
        adversary_position="Alternative polymerization mechanisms",
        counter_arguments=[
            "Chain transfer and termination can complicate mechanism.",
            "Heterogeneous catalyst surfaces are complex.",
            "Metallocene catalysts follow similar but distinct pathways."
        ],
        resolution_strategy="Combine kinetic, spectroscopic, and polymer analysis.",
        entity_scope="Olefin polymerization catalysis",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Ziegler-Natta Catalysis (1953)"
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Heavy Metals",
        keywords=["environmental", "heavy metals", "toxicity", "speciation", "remediation"],
        conclusion_template="The environmental impact of heavy metals depends on their chemical speciation, mobility, and bioavailability.",
        reasoning_framework=(
            "1. Identify the chemical forms (species) of heavy metals in the environment.\n"
            "2. Assess mobility: solubility, adsorption, and complexation with ligands.\n"
            "3. Evaluate bioavailability and toxicity based on speciation.\n"
            "4. Reference remediation strategies: precipitation, adsorption, ion exchange.\n"
            "5. Cite regulatory standards and case studies."
        ),
        key_factors=["speciation", "mobility", "bioavailability", "remediation method"],
        primary_authority=["Alloway, Heavy Metals in Soils", "Stumm & Morgan, Aquatic Chemistry"],
        burden_holder="Proponent of risk assessment or remediation strategy",
        adversary_position="Alternative risk or remediation assessments",
        counter_arguments=[
            "Speciation can change with environmental conditions.",
            "Remediation may produce secondary pollution.",
            "Risk assessment is context-dependent."
        ],
        resolution_strategy="Combine chemical analysis with ecological and toxicological data.",
        entity_scope="Environmental inorganic chemistry",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Environmental Chemistry Guidelines (EPA, WHO)"
    ),
    DoctrineBlock(
        topic="Corrosion Mechanisms of Iron",
        keywords=["corrosion", "iron", "redox", "passivation", "electrochemistry"],
        conclusion_template="Iron corrodes via electrochemical redox reactions, forming rust; passivation layers can inhibit further corrosion.",
        reasoning_framework=(
            "1. Outline the anodic (Fe → Fe2+ + 2e-) and cathodic (O2 + 4H+ + 4e- → 2H2O) reactions.\n"
            "2. Describe the formation of rust (hydrated iron oxides).\n"
            "3. Discuss the role of passivation layers (e.g., Fe3O4) in inhibiting corrosion.\n"
            "4. Analyze environmental factors: pH, chloride ions, oxygen availability.\n"
            "5. Reference corrosion prevention methods (coatings, cathodic protection)."
        ),
        key_factors=["electrochemical potential", "environmental conditions", "passivation"],
        primary_authority=["Fontana, Corrosion Engineering", "Atkins & Overton, Shriver & Atkins' Inorganic Chemistry"],
        burden_holder="Proponent of corrosion mechanism or prevention method",
        adversary_position="Alternative mechanisms or failure of passivation",
        counter_arguments=[
            "Localized corrosion (pitting) can bypass passivation.",
            "Microbial activity may accelerate corrosion.",
            "Alloying elements can alter corrosion behavior."
        ],
        resolution_strategy="Combine electrochemical analysis with materials testing.",
        entity_scope="Iron and steel corrosion",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Electrochemical Corrosion Theory"
    ),
    DoctrineBlock(
        topic="Water Treatment by Precipitation and Ion Exchange",
        keywords=["water treatment", "precipitation", "ion exchange", "hardness", "removal"],
        conclusion_template="Water treatment commonly employs precipitation and ion exchange to remove inorganic contaminants.",
        reasoning_framework=(
            "1. Precipitation: add reagents to convert dissolved ions into insoluble solids (e.g., Ca2+ + CO32- → CaCO3).\n"
            "2. Ion exchange: pass water through resin to swap undesirable ions for benign ones (e.g., Na+ for Ca2+).\n"
            "3. Evaluate efficiency, selectivity, and regeneration of treatment systems.\n"
            "4. Reference regulatory standards for water quality.\n"
            "5. Cite case studies and operational considerations."
        ),
        key_factors=["ion selectivity", "precipitation conditions", "resin capacity"],
        primary_authority=["Stumm & Morgan, Aquatic Chemistry", "Sawyer, McCarty & Parkin, Chemistry for Environmental Engineering"],
        burden_holder="Proponent of treatment method",
        adversary_position="Alternative or combined treatment methods",
        counter_arguments=[
            "Precipitation may not remove all contaminants.",
            "Ion exchange resins can foul or exhaust.",
            "Combined methods may be more effective."
        ],
        resolution_strategy="Combine chemical analysis with pilot-scale testing.",
        entity_scope="Water treatment chemistry",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Water Treatment Standards (EPA, WHO)"
    ),
    DoctrineBlock(
        topic="Geochemical Cycling of Elements",
        keywords=["geochemistry", "element cycling", "reservoirs", "flux", "earth system"],
        conclusion_template="Elements cycle through Earth's reservoirs (atmosphere, hydrosphere, lithosphere, biosphere) via geochemical processes.",
        reasoning_framework=(
            "1. Identify major reservoirs and fluxes for the element of interest.\n"
            "2. Analyze processes: weathering, precipitation, biological uptake, volcanic activity.\n"
            "3. Quantify residence times and steady-state concentrations.\n"
            "4. Reference isotopic tracers and geochemical models.\n"
            "5. Cite case studies (e.g., carbon, nitrogen, sulfur cycles)."
        ),
        key_factors=["reservoir size", "flux rate", "biogeochemical process"],
        primary_authority=["Berner, The Global Water Cycle", "Stumm & Morgan, Aquatic Chemistry"],
        burden_holder="Proponent of cycling model",
        adversary_position="Alternative models or flux estimates",
        counter_arguments=[
            "Anthropogenic activity can alter natural cycles.",
            "Uncertainties in flux measurements.",
            "Complex feedbacks may not be captured."
        ],
        resolution_strategy="Integrate observational data with modeling.",
        entity_scope="Earth system geochemistry",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Geochemical Cycle Models"
    ),
    DoctrineBlock(
        topic="Mössbauer Spectroscopy in Inorganic Chemistry",
        keywords=["Mössbauer spectroscopy", "iron", "isomer shift", "quadrupole splitting", "hyperfine"],
        conclusion_template="Mössbauer spectroscopy provides information on oxidation state, spin state, and local environment of Mössbauer-active nuclei (e.g., 57Fe).",
        reasoning_framework=(
            "1. Explain the Mössbauer effect: recoil-free γ-ray absorption/emission.\n"
            "2. Interpret isomer shift as a measure of s-electron density at the nucleus.\n"
            "3. Analyze quadrupole splitting for information on electric field gradients.\n"
            "4. Use hyperfine splitting to probe magnetic ordering.\n"
            "5. Reference applications in iron-containing compounds and minerals."
        ),
        key_factors=["isomer shift", "quadrupole splitting", "hyperfine field"],
        primary_authority=["Gütlich, Mössbauer Spectroscopy and Transition Metal Chemistry", "Atkins & Overton, Shriver & Atkins' Inorganic Chemistry"],
        burden_holder="Proponent of spectroscopic interpretation",
        adversary_position="Alternative assignments of spectral features",
        counter_arguments=[
            "Overlapping signals can complicate analysis.",
            "Dynamic effects may broaden or shift features.",
            "Other nuclei may contribute to spectra."
        ],
        resolution_strategy="Combine Mössbauer with complementary spectroscopies.",
        entity_scope="Inorganic compounds with Mössbauer-active nuclei",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Mössbauer Effect (Rudolf Mössbauer, 1958)"
    ),
    DoctrineBlock(
        topic="Superconductivity in Inorganic Materials",
        keywords=["superconductivity", "critical temperature", "Meissner effect", "Cooper pairs", "solid state"],
        conclusion_template="Certain inorganic materials exhibit superconductivity below a critical temperature, characterized by zero resistance and the Meissner effect.",
        reasoning_framework=(
            "1. Define superconductivity: zero electrical resistance and expulsion of magnetic field (Meissner effect).\n"
            "2. Identify critical temperature (Tc) for material.\n"
            "3. Explain BCS theory: formation of Cooper pairs.\n"
            "4. Reference high-Tc ceramic superconductors (e.g., YBa2Cu3O7-x).\n"
            "5. Discuss technological applications and limitations."
        ),
        key_factors=["critical temperature", "material structure", "magnetic properties"],
        primary_authority=["Poole, Superconductivity", "Ashcroft & Mermin, Solid State Physics"],
        burden_holder="Proponent of superconducting classification",
        adversary_position="Alternative explanations for observed properties",
        counter_arguments=[
            "Granularity and impurities can affect superconductivity.",
            "Not all zero-resistance states are superconducting.",
            "High-Tc mechanisms may differ from BCS theory."
        ],
        resolution_strategy="Combine electrical, magnetic, and structural measurements.",
        entity_scope="Inorganic superconductors",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="BCS Theory (Bardeen, Cooper, Schrieffer, 1957)"
    ),
    DoctrineBlock(
        topic="Ceramic Materials: Structure and Properties",
        keywords=["ceramics", "structure", "ionic solids", "mechanical properties", "processing"],
        conclusion_template="Ceramic materials are typically crystalline or amorphous inorganic solids with high hardness, brittleness, and chemical stability.",
        reasoning_framework=(
            "1. Classify ceramics by structure: crystalline (e.g., alumina) or amorphous (e.g., glass).\n"
            "2. Relate properties to bonding: ionic/covalent bonds confer hardness and brittleness.\n"
            "3. Discuss processing methods: sintering, vitrification.\n"
            "4. Reference applications (e.g., insulators, refractories).\n"
            "5. Analyze mechanical and thermal properties."
        ),
        key_factors=["crystal structure", "bonding", "processing method"],
        primary_authority=["Kingery, Bowen & Uhlmann, Introduction to Ceramics", "West, Solid State Chemistry"],
        burden_holder="Proponent of structure-property relationship",
        adversary_position="Polymer/metal-ceramic composites with altered properties",
        counter_arguments=[
            "Defects and porosity can weaken ceramics.",
            "Composites may overcome brittleness.",
            "Processing conditions greatly affect properties."
        ],
        resolution_strategy="Correlate microstructure with bulk properties.",
        entity_scope="Inorganic ceramic materials",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Ceramic Science (Kingery, 1976)"
    ),
    DoctrineBlock(
        topic="Semiconductor Doping and Conductivity",
        keywords=["semiconductor", "doping", "n-type", "p-type", "conductivity"],
        conclusion_template="Doping semiconductors with donor or acceptor impurities increases their electrical conductivity by introducing charge carriers.",
        reasoning_framework=(
            "1. Define intrinsic semiconductor: pure material with limited conductivity.\n"
            "2. n-type doping: add donor atoms (e.g., P in Si) to provide extra electrons.\n"
            "3. p-type doping: add acceptor atoms (e.g., B in Si) to create holes.\n"
            "4. Relate carrier concentration to conductivity.\n"
            "5. Reference device applications (e.g., diodes, transistors)."
        ),
        key_factors=["dopant type", "carrier concentration", "band structure"],
        primary_authority=["Sze, Physics of Semiconductor Devices", "Ashcroft & Mermin, Solid State Physics"],
        burden_holder="Proponent of doping mechanism",
        adversary_position="Alternative explanations for conductivity changes",
        counter_arguments=[
            "Compensation by native defects can reduce effectiveness.",
            "High dopant concentrations may lead to clustering.",
            "Temperature dependence of carrier mobility."
        ],
        resolution_strategy="Combine electrical measurements with structural analysis.",
        entity_scope="Inorganic semiconductors",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Semiconductor Physics (Shockley, 1949)"
    ),
    DoctrineBlock(
        topic="Photochemical Water Splitting",
        keywords=["photochemistry", "water splitting", "catalysis", "solar energy", "hydrogen"],
        conclusion_template="Photochemical water splitting uses light energy and catalysts to generate hydrogen and oxygen from water.",
        reasoning_framework=(
            "1. Outline the overall reaction: 2H2O → 2H2 + O2.\n"
            "2. Identify the need for suitable photocatalysts (e.g., TiO2).\n"
            "3. Discuss the energetics: band gap must straddle water redox potentials.\n"
            "4. Reference quantum efficiency and practical challenges.\n"
            "5. Cite advances in catalyst design and solar fuels research."
        ),
        key_factors=["catalyst band gap", "light absorption", "charge separation"],
        primary_authority=["Fujishima & Honda, Nature 1972", "Kudo & Miseki, Chem. Soc. Rev. 2009"],
        burden_holder="Proponent of photochemical mechanism",
        adversary_position="Alternative water splitting methods",
        counter_arguments=[
            "Recombination of charge carriers reduces efficiency.",
            "Catalyst degradation limits lifetime.",
            "Sacrificial reagents may be required."
        ],
        resolution_strategy="Optimize catalyst design and reaction conditions.",
        entity_scope="Inorganic photochemical systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Photocatalytic Water Splitting (Fujishima & Honda, 1972)"
    ),
    DoctrineBlock(
        topic="Main Group Hydrides: Structure and Reactivity",
        keywords=["main group", "hydrides", "structure", "reactivity", "inorganic"],
        conclusion_template="Main group element hydrides exhibit diverse structures and reactivities, from simple diatomics to complex polymers.",
        reasoning_framework=(
            "1. Classify hydrides: ionic (e.g., NaH), covalent (e.g., PH3), metallic (e.g., MgH2).\n"
            "2. Relate structure to position in the periodic table.\n"
            "3. Discuss thermal stability, reactivity with water/air, and applications.\n"
            "4. Reference bonding models and empirical data.\n"
            "5. Cite industrial and synthetic uses."
        ),
        key_factors=["element group", "bonding", "thermal stability"],
        primary_authority=["Greenwood & Earnshaw, Chemistry of the Elements", "Atkins & Overton, Shriver & Atkins' Inorganic Chemistry"],
        burden_holder="Proponent of structure/reactivity assignment",
        adversary_position="Alternative bonding models",
        counter_arguments=[
            "Polymorphism can complicate structural analysis.",
            "Hydride reactivity is sensitive to impurities.",
            "Thermodynamic data may be limited."
        ],
        resolution_strategy="Combine structural, thermodynamic, and reactivity studies.",
        entity_scope="Main group hydrides",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Main Group Chemistry (General)"
    ),
    DoctrineBlock(
        topic="Electron Counting in Cluster Compounds",
        keywords=["cluster compounds", "electron counting", "Wade's rules", "boranes", "carboranes"],
        conclusion_template="Electron counting in cluster compounds follows Wade's rules, relating structure to skeletal electron pairs.",
        reasoning_framework=(
            "1. Identify the number of skeletal atoms in the cluster.\n"
            "2. Count total valence electrons and convert to skeletal electron pairs.\n"
            "3. Apply Wade's rules: closo, n+1; nido, n+2; arachno, n+3 pairs.\n"
            "4. Assign structure type based on electron count.\n"
            "5. Reference classic examples (e.g., B6H6^2-, B5H9)."
        ),
        key_factors=["number of atoms", "valence electron count", "structure type"],
        primary_authority=["Wade, J. Chem. Soc., Dalton Trans., 1971", "Greenwood & Earnshaw, Chemistry of the Elements"],
        burden_holder="Proponent of electron counting assignment",
        adversary_position="Alternative structural assignments",
        counter_arguments=[
            "Exceptions to Wade's rules exist.",
            "Heteroatoms can complicate electron counting.",
            "Dynamic fluxionality may obscure structure."
        ],
        resolution_strategy="Combine electron counting with structural analysis.",
        entity_scope="Inorganic cluster compounds",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Wade's Rules (1971)"
    ),
    DoctrineBlock(
        topic="Spin Crossover in Transition Metal Complexes",
        keywords=["spin crossover", "transition metals", "high-spin", "low-spin", "thermodynamics"],
        conclusion_template="Some transition metal complexes exhibit spin crossover, changing between high-spin and low-spin states in response to temperature, pressure, or light.",
        reasoning_framework=(
            "1. Identify complexes with intermediate ligand field strengths (e.g., Fe(II), d6).\n"
            "2. Analyze thermodynamic parameters (ΔH, ΔS) for spin state interconversion.\n"
            "3. Observe spin crossover via magnetic, spectroscopic, or structural changes.\n"
            "4. Reference applications in molecular switches and sensors.\n"
            "5. Cite classic studies and recent advances."
        ),
        key_factors=["ligand field strength", "thermodynamic parameters", "external stimuli"],
        primary_authority=["Gütlich, Spin Crossover in Transition Metal Compounds", "Atkins & Overton, Shriver & Atkins' Inorganic Chemistry"],
        burden_holder="Proponent of spin crossover assignment",
        adversary_position="Static spin state assignment",
        counter_arguments=[
            "Kinetic barriers may prevent crossover.",
            "Cooperative effects can lead to abrupt transitions.",
            "Not all complexes exhibit observable crossover."
        ],
        resolution_strategy="Combine variable-temperature measurements with theoretical modeling.",
        entity_scope="Spin-crossover transition metal complexes",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Spin Crossover Chemistry (Gütlich, 1994)"
    ),
    DoctrineBlock(
        topic="Oxo Transfer in Inorganic Catalysis",
        keywords=["oxo transfer", "catalysis", "transition metals", "oxygen atom", "mechanism"],
        conclusion_template="Oxo transfer reactions involve the transfer of an oxygen atom from a metal-oxo species to a substrate, central to many catalytic cycles.",
        reasoning_framework=(
            "1. Identify the metal-oxo species and substrate.\n"
            "2. Outline the mechanism: oxygen atom transfer to substrate, often with change in metal oxidation state.\n"
            "3. Reference classic examples (e.g., OsO4 dihydroxylation, Mo(VI) oxo transfer).\n"
            "4. Analyze kinetic and spectroscopic evidence for intermediates.\n"
            "5. Discuss synthetic and biological relevance."
        ),
        key_factors=["metal-oxo species", "substrate identity", "mechanistic evidence"],
        primary_authority=["Meyer, Acc. Chem. Res. 1989", "Atkins & Overton, Shriver & Atkins' Inorganic Chemistry"],
        burden_holder="Proponent of oxo transfer mechanism",
        adversary_position="Alternative oxidation mechanisms",
        counter_arguments=[
            "Radical pathways may compete with oxo transfer.",
            "Ligand exchange can complicate mechanism.",
            "Spectroscopic assignment of intermediates may be ambiguous."
        ],
        resolution_strategy="Combine mechanistic studies with isotopic labeling.",
        entity_scope="Oxo transfer catalytic cycles",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Oxo Transfer Mechanisms (General)"
    ),
    DoctrineBlock(
        topic="Thermodynamics of Inorganic Precipitation Reactions",
        keywords=["thermodynamics", "precipitation", "solubility product", "Ksp", "inorganic"],
        conclusion_template="The extent of precipitation in inorganic reactions is governed by the solubility product (Ksp) and the ionic product of the solution.",
        reasoning_framework=(
            "1. Write the dissolution/precipitation equilibrium and corresponding Ksp expression.\n"
            "2. Calculate the ionic product (Q) for the solution.\n"
            "3. If Q > Ksp, precipitation occurs; if Q < Ksp, dissolution occurs.\n"
            "4. Reference temperature dependence and common ion effect.\n"
            "5. Cite experimental solubility data."
        ),
        key_factors=["Ksp value", "ionic product", "temperature", "common ion effect"],
        primary_authority=["Atkins & Overton, Shriver & Atkins' Inorganic Chemistry", "Stumm & Morgan, Aquatic Chemistry"],
        burden_holder="Proponent of precipitation prediction",
        adversary_position="Observed deviations from predicted precipitation",
        counter_arguments=[
            "Supersaturation and nucleation kinetics can delay precipitation.",
            "Complex formation may increase solubility.",
            "Colloidal stability can prevent precipitation."
        ],
        resolution_strategy="Combine thermodynamic calculations with experimental observation.",
        entity_scope="Inorganic precipitation reactions",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Solubility Product Principle"
    ),
    DoctrineBlock(
        topic="Kinetics of Ligand Exchange in Inert Complexes",
        keywords=["kinetics", "ligand exchange", "inert complexes", "activation energy", "octahedral"],
        conclusion_template="Ligand exchange in inert complexes proceeds slowly due to high activation energy barriers, often requiring associative or dissociative mechanisms.",
        reasoning_framework=(
            "1. Define inert complexes (e.g., Cr(III), Co(III) with low-spin d6 configurations).\n"
            "2. Analyze kinetic data: rate constants, activation parameters.\n"
            "3. Propose associative (A), dissociative (D), or interchange (I) mechanisms.\n"
            "4. Reference classic studies and compare with labile complexes.\n"
            "5. Discuss implications for reactivity and synthesis."
        ),
        key_factors=["activation energy", "electronic configuration", "mechanistic pathway"],
        primary_authority=["Taube, Inorganic Reaction Mechanisms", "Basolo & Pearson, Mechanisms of Inorganic Reactions"],
        burden_holder="Proponent of kinetic/mechanistic assignment",
        adversary_position="Alternative interpretations of rate data",
        counter_arguments=[
            "Solvent and ionic strength can affect rates.",
            "Multiple pathways may operate.",
            "Experimental errors in rate measurement."
        ],
        resolution_strategy="Combine kinetic, thermodynamic, and spectroscopic data.",
        entity_scope="Inert octahedral complexes",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Inorganic Reaction Mechanisms (Taube, 1952)"
    ),
    DoctrineBlock(
        topic="Electrochemical Series and Redox Reactivity",
        keywords=["electrochemical series", "redox", "standard potential", "reactivity", "inorganic"],
        conclusion_template="The electrochemical series ranks elements by standard reduction potential, predicting redox reactivity and direction of electron flow.",
        reasoning_framework=(
            "1. Reference standard reduction potentials (E°) for half-reactions.\n"
            "2. More positive E° indicates greater tendency to be reduced.\n"
            "3. Use the series to predict feasibility and direction of redox reactions.\n"
            "4. Apply to displacement reactions and corrosion.\n"
            "5. Note limitations (non-standard conditions, complex formation)."
        ),
        key_factors=["standard potential", "reaction conditions", "complex formation"],
        primary_authority=["Bard & Faulkner, Electrochemical Methods", "Atkins & Overton, Shriver & Atkins' Inorganic Chemistry"],
        burden_holder="Proponent of redox prediction",
        adversary_position="Observed deviations from series predictions",
        counter_arguments=[
            "Concentration and pH can alter potentials.",
            "Kinetic barriers may prevent reaction.",
            "Complex formation can shift potentials."
        ],
        resolution_strategy="Adjust for non-standard conditions and compare with experimental data.",
        entity_scope="Inorganic redox systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Electrochemical Series (General)"
    ),
    DoctrineBlock(
        topic="Symmetry-Allowed and Forbidden Transitions in Spectroscopy",
        keywords=["symmetry", "spectroscopy", "Laporte rule", "selection rules", "electronic transitions"],
        conclusion_template="Electronic transitions in inorganic complexes are governed by symmetry-based selection rules, such as the Laporte rule.",
        reasoning_framework=(
            "1. Assign the point group and symmetry labels to molecular orbitals.\n"
            "2. Apply selection rules: transitions are allowed if the direct product of initial and final states contains the same irreducible representation as the transition operator.\n"
            "3. Laporte rule: in centrosymmetric complexes, only g→u or u→g transitions are allowed.\n"
            "4. Forbidden transitions may gain intensity via vibronic coupling.\n"
            "5. Reference UV-Vis spectra and transition intensities."
        ),
        key_factors=["molecular symmetry", "transition operator", "spectral intensity"],
        primary_authority=["Cotton, Chemical Applications of Group Theory", "Atkins & Overton, Shriver & Atkins' Inorganic Chemistry"],
        burden_holder="Proponent of transition assignment",
        adversary_position="Alternative explanations for observed intensities",
        counter_arguments=[
            "Spin-orbit coupling can relax selection rules.",
            "Distortions can lower symmetry.",
            "Experimental spectra may be complex."
        ],
        resolution_strategy="Combine group theory analysis with spectroscopic data.",
        entity_scope="Inorganic spectroscopic transitions",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Laporte Rule (1925)"
    ),
    DoctrineBlock(
        topic="Industrial Inorganic Processes: Haber-Bosch Synthesis",
        keywords=["industrial", "Haber-Bosch", "ammonia", "catalysis", "process"],
        conclusion_template="The Haber-Bosch process synthesizes ammonia from N2 and H2 using an iron catalyst under high temperature and pressure.",
        reasoning_framework=(
            "1. Outline the reaction: N2 + 3H2 ⇌ 2NH3.\n"
            "2. Describe process conditions: 400–500°C, 150–300 atm, iron catalyst with promoters.\n"
            "3. Discuss equilibrium and kinetic considerations.\n"
            "4. Reference industrial scale and global importance.\n"
            "5. Cite advances in catalyst design and process optimization."
        ),
        key_factors=["catalyst", "temperature", "pressure", "equilibrium"],
        primary_authority=["Smil, Enriching the Earth", "Atkins & Overton, Shriver & Atkins' Inorganic Chemistry"],
        burden_holder="Proponent of process design",
        adversary_position="Alternative ammonia synthesis methods",
        counter_arguments=[
            "High energy input and CO2 emissions.",
            "Alternative catalysts and processes are under development.",
            "Process optimization can improve efficiency."
        ],
        resolution_strategy="Compare process metrics and environmental impact.",
        entity_scope="Industrial ammonia synthesis",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Haber-Bosch Process (1909)"
    ),
    DoctrineBlock(
        topic="Actinide Chemistry: Oxidation States and Complexation",
        keywords=["actinides", "oxidation state", "complexation", "f-block", "inorganic"],
        conclusion_template="Actinides exhibit a wide range of oxidation states and complexation behavior due to the availability of 5f, 6d, and 7s orbitals.",
        reasoning_framework=(
            "1. Identify common oxidation states for actinides (e.g., U(III) to U(VI)).\n"
            "2. Relate to electron configuration and relativistic effects.\n"
            "3. Discuss complexation with inorganic and organic ligands.\n"
            "4. Reference environmental and nuclear applications.\n"
            "5. Cite spectroscopic and structural data."
        ),
        key_factors=["oxidation state", "ligand field", "relativistic effects"],
        primary_authority=["Choppin, Liljenzin & Rydberg, Radiochemistry and Nuclear Chemistry", "Greenwood & Earnshaw, Chemistry of the Elements"],
        burden_holder="Proponent of oxidation state/complex assignment",
        adversary_position="Alternative assignments or interpretations",
        counter_arguments=[
            "Redox instability can complicate assignments.",
            "Spectroscopic data may be ambiguous.",
            "Complexation can stabilize unusual states."
        ],
        resolution_strategy="Combine multiple lines of evidence (spectroscopy, electrochemistry, crystallography).",
        entity_scope="Actinide chemistry",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Actinide Chemistry (General)"
    ),
    DoctrineBlock(
        topic="Thermodynamic Stability of Metal Complexes",
        keywords=["thermodynamics", "stability constant", "formation constant", "metal complex"],
        conclusion_template="The thermodynamic stability of a metal complex is quantified by its formation (stability) constant, reflecting the equilibrium position.",
        reasoning_framework=(
            "1. Write the equilibrium for complex formation and the corresponding stability constant (Kf).\n"
            "2. Higher Kf indicates greater thermodynamic stability.\n"
            "3. Analyze factors affecting Kf: ligand denticity, chelate effect, metal ion properties.\n"
            "4. Reference empirical data and compare related complexes.\n"
            "5. Discuss implications for synthesis and reactivity."
        ),
        key_factors=["Kf value", "ligand properties", "metal ion properties"],
        primary_authority=["Huheey, Inorganic Chemistry", "Martell & Hancock, Metal Complexes in Aqueous Solutions"],
        burden_holder="Proponent of stability assignment",
        adversary_position="Alternative stability assignments",
        counter_arguments=[
            "Kinetic inertness may not reflect thermodynamic stability.",
            "Solvent and ionic strength can alter Kf.",
            "Competing equilibria may complicate analysis."
        ],
        resolution_strategy="Combine thermodynamic measurements with kinetic and spectroscopic data.",
        entity_scope="Metal-ligand complexes",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Stability Constant Theory"
    ),
    DoctrineBlock(
        topic="Solid Solutions and Non-Stoichiometry in Inorganic Solids",
        keywords=["solid solution", "non-stoichiometry", "defects", "crystal structure", "inorganic"],
        conclusion_template="Solid solutions and non-stoichiometry in inorganic solids arise from substitutional or interstitial defects, affecting material properties.",
        reasoning_framework=(
            "1. Define solid solution: continuous variation in composition via substitution or interstitial occupancy.\n"
            "2. Non-stoichiometry results from defects (vacancies, interstitials, substitutions).\n"
            "3. Analyze impact on electrical, magnetic, and catalytic properties.\n"
            "4. Reference classic examples (e.g., FeO, TiO2-x).\n"
            "5. Cite structural and analytical techniques."
        ),
        key_factors=["defect type", "composition", "property change"],
        primary_authority=["West, Solid State Chemistry", "Atkins & Overton, Shriver & Atkins' Inorganic Chemistry"],
        burden_holder="Proponent of defect model",
        adversary_position="Alternative structural models",
        counter_arguments=[
            "Phase separation can mimic solid solution behavior.",
            "Defect clustering may occur.",
            "Analytical limitations in detecting non-stoichiometry."
        ],
        resolution_strategy="Combine structural, compositional, and property measurements.",
        entity_scope="Inorganic solid solutions",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Solid Solution Theory"
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