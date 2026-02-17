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
        topic="Free Radical Addition Polymerization",
        keywords=[
            "free radical", "initiation", "propagation", "termination",
            "chain transfer", "monomer", "polymerization kinetics",
            "radical stability", "chain growth", "polymer molecular weight"
        ],
        conclusion_template=(
            "In free radical addition polymerization, the polymer chain grows "
            "via successive addition of monomer units to an active radical site, "
            "with the overall rate controlled by initiation, propagation, and termination steps."
        ),
        reasoning_framework=(
            "Free radical addition polymerization proceeds through three fundamental steps: initiation, "
            "propagation, and termination. Initiation involves the generation of radical species, often "
            "via thermal or photochemical decomposition of initiators such as benzoyl peroxide or AIBN. "
            "Propagation consists of the addition of monomer molecules to the radical chain end, "
            "forming a growing polymer radical. Termination occurs when two radical chains combine or "
            "disproportionate, ceasing chain growth. Chain transfer reactions may also occur, transferring "
            "the radical site to another molecule, affecting molecular weight distribution. The kinetics "
            "are governed by rate constants for each step and the concentration of monomer and initiator. "
            "Radical stability influences the rate and control of polymer growth. Molecular weight and polymer "
            "architecture depend on the balance of these steps and reaction conditions such as temperature and solvent."
        ),
        key_factors=[
            "Initiator type and concentration",
            "Monomer reactivity",
            "Temperature",
            "Solvent effects",
            "Chain transfer agents",
            "Radical stability",
            "Termination mechanisms"
        ],
        primary_authority=[
            "Odian, G. Principles of Polymerization, 4th Edition, Wiley, 2004",
            "Brandrup, J., Immergut, E. H., Polymer Handbook, Wiley, 1999"
        ],
        burden_holder="Polymer chemist or process engineer",
        adversary_position=(
            "Claims that free radical polymerization cannot achieve controlled molecular weights "
            "or architectures due to inherent termination and chain transfer reactions."
        ),
        counter_arguments=[
            "Use of controlled radical polymerization techniques (e.g., ATRP, RAFT) mitigates termination.",
            "Optimization of reaction conditions reduces undesired side reactions.",
            "Kinetic modeling allows prediction and control of polymer properties."
        ],
        resolution_strategy=(
            "Employ kinetic studies and controlled radical polymerization methods to demonstrate "
            "control over molecular weight and architecture, validating the applicability of free radical polymerization."
        ),
        entity_scope="Synthetic polymerization processes involving vinyl monomers",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Odian (2004), Chapter 5: Free Radical Polymerization Mechanisms"
    ),
    DoctrineBlock(
        topic="Living/Controlled Radical Polymerization (ATRP, RAFT, NMP)",
        keywords=[
            "ATRP", "RAFT", "NMP", "living polymerization", "controlled radical polymerization",
            "chain transfer", "reversible deactivation", "molecular weight control",
            "polymer architecture", "kinetic control"
        ],
        conclusion_template=(
            "Living/controlled radical polymerization techniques enable precise control over polymer molecular weight, "
            "distribution, and architecture by reversible deactivation of growing radicals."
        ),
        reasoning_framework=(
            "Living or controlled radical polymerization (CRP) methods such as Atom Transfer Radical Polymerization (ATRP), "
            "Reversible Addition-Fragmentation chain Transfer (RAFT), and Nitroxide Mediated Polymerization (NMP) rely on "
            "reversible deactivation of the propagating radical species. This equilibrium between active and dormant states "
            "minimizes irreversible termination and chain transfer, allowing polymer chains to grow uniformly. ATRP uses "
            "transition metal complexes to reversibly activate and deactivate radicals. RAFT employs chain transfer agents "
            "with thiocarbonylthio groups to mediate chain growth. NMP utilizes stable nitroxide radicals to cap growing chains. "
            "These mechanisms enable synthesis of polymers with narrow molecular weight distributions, predetermined molecular weights, "
            "and complex architectures such as block copolymers. Kinetic control is achieved by balancing activation/deactivation rates "
            "and monomer concentration."
        ),
        key_factors=[
            "Choice of CRP method (ATRP, RAFT, NMP)",
            "Catalyst or chain transfer agent design",
            "Monomer compatibility",
            "Reaction temperature",
            "Solvent effects",
            "Initiator efficiency",
            "Equilibrium constants for activation/deactivation"
        ],
        primary_authority=[
            "Matyjaszewski, K., Controlled Radical Polymerization, ACS Symposium Series, 2003",
            "Chiefari, J. et al., Macromolecules, 1998, 31, 5559",
            "Georges, M. K., Nitroxide Mediated Polymerization, Prog. Polym. Sci., 2000"
        ],
        burden_holder="Polymer synthesis researcher or industrial chemist",
        adversary_position=(
            "Argues that living radical polymerization cannot fully suppress termination or achieve truly 'living' characteristics."
        ),
        counter_arguments=[
            "Empirical data shows narrow dispersity and predictable molecular weights.",
            "Advanced catalyst and agent designs improve control and reduce termination.",
            "Kinetic models confirm reversible deactivation equilibria."
        ],
        resolution_strategy=(
            "Demonstrate living characteristics via kinetic experiments, molecular weight analysis, and chain extension studies."
        ),
        entity_scope="Controlled radical polymerization of vinyl monomers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Matyjaszewski (2003), RAFT seminal papers (Chiefari et al., 1998)"
    ),
    DoctrineBlock(
        topic="Condensation Step-Growth Polymerization",
        keywords=[
            "step-growth", "condensation polymerization", "polycondensation",
            "functional groups", "degree of polymerization", "carboxylic acid",
            "alcohol", "amine", "esterification", "amide formation"
        ],
        conclusion_template=(
            "Condensation step-growth polymerization proceeds through repeated reaction of bifunctional or multifunctional monomers, "
            "forming polymers with molecular weight increasing gradually as conversion approaches completion."
        ),
        reasoning_framework=(
            "Step-growth polymerization involves the reaction of monomers with two or more reactive end groups, such as carboxylic acids, "
            "alcohols, or amines. Unlike chain-growth polymerization, polymer chains grow by stepwise reaction between any two molecular species, "
            "including monomers, oligomers, and polymers. The molecular weight distribution broadens as the reaction proceeds, and high molecular "
            "weights are only achieved at very high monomer conversion. Typical reactions include esterification, amidation, and urethane formation. "
            "Stoichiometric balance of functional groups is critical to achieving high molecular weight. Side reactions such as cyclization or incomplete "
            "conversion reduce polymer chain length. Kinetic models based on Carothers equation describe the relationship between conversion and degree of polymerization."
        ),
        key_factors=[
            "Monomer functionality and stoichiometry",
            "Reaction conversion",
            "Reaction temperature and catalysts",
            "Removal of condensation byproducts",
            "Side reactions and cyclization",
            "Molecular weight distribution"
        ],
        primary_authority=[
            "Carothers, W. H., J. Am. Chem. Soc., 1936, 58, 1625",
            "Odian, G., Principles of Polymerization, Wiley, 2004",
            "Flory, P. J., Principles of Polymer Chemistry, Cornell University Press, 1953"
        ],
        burden_holder="Polymer chemist or process engineer",
        adversary_position=(
            "Claims that step-growth polymerization cannot achieve high molecular weights without perfect stoichiometry."
        ),
        counter_arguments=[
            "Careful control of monomer purity and stoichiometry enables high molecular weight polymers.",
            "Use of catalysts and removal of byproducts drives reaction to high conversion.",
            "Kinetic and statistical models predict achievable molecular weights."
        ],
        resolution_strategy=(
            "Implement rigorous stoichiometric control and reaction monitoring to optimize polymer molecular weight."
        ),
        entity_scope="Step-growth polymerization of bifunctional and multifunctional monomers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Carothers (1936), Flory (1953)"
    ),
    DoctrineBlock(
        topic="Molecular Weight Distribution and GPC/SEC",
        keywords=[
            "molecular weight distribution", "GPC", "SEC", "gel permeation chromatography",
            "polydispersity index", "number average molecular weight", "weight average molecular weight",
            "calibration", "detectors", "polymer characterization"
        ],
        conclusion_template=(
            "Gel Permeation Chromatography (GPC) or Size Exclusion Chromatography (SEC) provides critical data on polymer molecular weight distribution, "
            "enabling calculation of average molecular weights and polydispersity indices essential for polymer characterization."
        ),
        reasoning_framework=(
            "GPC/SEC separates polymer molecules based on their hydrodynamic volume as they pass through porous columns. Larger molecules elute earlier "
            "because they are excluded from pores, while smaller molecules penetrate pores and elute later. The elution volume is correlated to molecular "
            "weight via calibration with standards of known molecular weight. Detectors such as refractive index, light scattering, or viscometry provide "
            "quantitative data. From the elution profile, number average molecular weight (Mn), weight average molecular weight (Mw), and polydispersity index "
            "(PDI = Mw/Mn) are calculated, reflecting polymer chain length distribution. Accurate calibration and sample preparation are crucial for reliable results."
        ),
        key_factors=[
            "Column selection and calibration standards",
            "Detector type and sensitivity",
            "Sample preparation and solvent choice",
            "Polymer-solvent interactions",
            "Data analysis methods",
            "Polydispersity and molecular weight averages"
        ],
        primary_authority=[
            "Williams, D. F., Polymer Characterization: Physical Techniques, Wiley, 1999",
            "Hawker, C. J., Wooley, K. L., Science, 2005, 309, 1200",
            "ASTM D5296-16 Standard Guide for Molecular Weight Characterization of Polymers by GPC"
        ],
        burden_holder="Polymer analyst or quality control chemist",
        adversary_position=(
            "Asserts that GPC data is unreliable due to calibration errors and solvent effects."
        ),
        counter_arguments=[
            "Use of universal calibration and multi-detector systems improves accuracy.",
            "Proper sample preparation minimizes aggregation and interaction artifacts.",
            "Cross-validation with other techniques (e.g., light scattering) confirms results."
        ],
        resolution_strategy=(
            "Adopt standardized protocols and calibration methods to ensure reproducible and accurate molecular weight data."
        ),
        entity_scope="Polymer molecular weight characterization",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASTM D5296-16, Williams (1999)"
    ),
    DoctrineBlock(
        topic="Thermal Analysis: DSC (Differential Scanning Calorimetry)",
        keywords=[
            "DSC", "differential scanning calorimetry", "glass transition temperature",
            "melting point", "crystallization", "thermal transitions", "enthalpy",
            "heat flow", "polymer thermal properties", "thermal stability"
        ],
        conclusion_template=(
            "Differential Scanning Calorimetry (DSC) is a fundamental technique for determining polymer thermal transitions such as glass transition, melting, and crystallization temperatures."
        ),
        reasoning_framework=(
            "DSC measures the heat flow into or out of a polymer sample as it is heated or cooled at a controlled rate. Endothermic and exothermic events correspond "
            "to thermal transitions including glass transition (Tg), melting (Tm), and crystallization (Tc). The glass transition is observed as a step change in heat capacity, "
            "while melting and crystallization appear as peaks due to latent heat. The magnitude and temperature of these transitions provide insight into polymer composition, "
            "molecular weight, crystallinity, and thermal stability. DSC data is essential for processing and application design, informing temperature limits and behavior."
        ),
        key_factors=[
            "Heating/cooling rate",
            "Sample preparation and mass",
            "Baseline correction",
            "Polymer crystallinity",
            "Molecular weight effects",
            "Additives and plasticizers"
        ],
        primary_authority=[
            "Hutchinson, J. M., Polymer Science: A Comprehensive Reference, Elsevier, 2012",
            "Skoog, D. A., Holler, F. J., Crouch, S. R., Principles of Instrumental Analysis, Cengage, 2017"
        ],
        burden_holder="Polymer scientist or materials engineer",
        adversary_position=(
            "Claims DSC cannot accurately determine Tg in semi-crystalline polymers due to overlapping transitions."
        ),
        counter_arguments=[
            "Modulated DSC and advanced data analysis separate overlapping transitions.",
            "Complementary techniques (DMA, TMA) corroborate DSC findings.",
            "Careful sample preparation and baseline subtraction improve accuracy."
        ],
        resolution_strategy=(
            "Use advanced DSC methods and corroborate with other thermal analysis techniques to accurately characterize polymer transitions."
        ),
        entity_scope="Thermal characterization of polymers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Hutchinson (2012), Skoog et al. (2017)"
    ),
    DoctrineBlock(
        topic="Polymer Rheology and Viscoelasticity",
        keywords=[
            "rheology", "viscoelasticity", "storage modulus", "loss modulus",
            "complex viscosity", "shear thinning", "creep", "stress relaxation",
            "dynamic mechanical analysis", "polymer melt behavior"
        ],
        conclusion_template=(
            "Polymer rheology and viscoelasticity describe the deformation and flow behavior of polymers under applied stress, critical for processing and performance."
        ),
        reasoning_framework=(
            "Polymers exhibit both viscous and elastic responses to deformation, characterized as viscoelastic behavior. Rheological measurements quantify storage modulus (elastic response), "
            "loss modulus (viscous response), and complex viscosity under oscillatory or steady shear conditions. Shear thinning behavior is common in polymer melts and solutions, facilitating processing. "
            "Time-temperature superposition principles enable prediction of long-term behavior from short-term tests. Creep and stress relaxation experiments reveal polymer response under constant stress or strain. "
            "Dynamic Mechanical Analysis (DMA) provides temperature and frequency-dependent viscoelastic properties, informing material selection and design."
        ),
        key_factors=[
            "Molecular weight and distribution",
            "Temperature",
            "Frequency and strain amplitude",
            "Polymer architecture (linear, branched, crosslinked)",
            "Additives and fillers",
            "Measurement geometry"
        ],
        primary_authority=[
            "Macosko, C. W., Rheology: Principles, Measurements, and Applications, Wiley-VCH, 1994",
            "Ferry, J. D., Viscoelastic Properties of Polymers, 3rd Ed., Wiley, 1980"
        ],
        burden_holder="Polymer rheologist or process engineer",
        adversary_position=(
            "Suggests that polymer rheology is too complex for predictive modeling due to nonlinearities and molecular diversity."
        ),
        counter_arguments=[
            "Empirical models and molecular theories provide accurate predictions within defined regimes.",
            "Advanced rheometers and DMA enable detailed characterization.",
            "Time-temperature superposition and master curves simplify complex behavior."
        ],
        resolution_strategy=(
            "Combine experimental rheology with modeling to predict polymer behavior under processing and service conditions."
        ),
        entity_scope="Polymer melt and solution rheology",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Macosko (1994), Ferry (1980)"
    ),
    DoctrineBlock(
        topic="Polymer Processing: Injection Molding",
        keywords=[
            "injection molding", "polymer processing", "melt flow", "cooling rate",
            "mold design", "shrinkage", "warpage", "cycle time", "thermal degradation",
            "processing parameters"
        ],
        conclusion_template=(
            "Injection molding of polymers requires precise control of melt flow, temperature, and cooling to produce defect-free parts with desired properties."
        ),
        reasoning_framework=(
            "Injection molding involves melting polymer pellets and injecting the melt into a mold cavity where it cools and solidifies. Melt flow behavior, influenced by polymer rheology, "
            "determines fill patterns and potential defects such as weld lines or voids. Cooling rate affects crystallinity and residual stresses, impacting shrinkage and warpage. Mold design "
            "must accommodate flow paths, venting, and thermal management. Processing parameters including injection pressure, screw speed, and mold temperature are optimized to balance cycle time "
            "and part quality. Thermal degradation risks increase with excessive temperature or residence time. Monitoring and control of these factors ensure consistent production of high-quality parts."
        ),
        key_factors=[
            "Polymer melt viscosity",
            "Mold temperature and cooling channels",
            "Injection pressure and speed",
            "Screw design and back pressure",
            "Cycle time optimization",
            "Material thermal stability",
            "Part geometry and wall thickness"
        ],
        primary_authority=[
            "Rosato, D. V., Rosato, D. V., Injection Molding Handbook, 3rd Ed., Springer, 2000",
            "Strong, A. B., Plastics: Materials and Processing, Pearson, 2006"
        ],
        burden_holder="Process engineer or manufacturing specialist",
        adversary_position=(
            "Claims that injection molding cannot produce complex geometries without defects or excessive cycle times."
        ),
        counter_arguments=[
            "Advanced mold design and simulation tools mitigate defects.",
            "Optimized processing parameters reduce cycle times.",
            "Material selection and additives improve flow and stability."
        ],
        resolution_strategy=(
            "Use process simulation, mold design optimization, and material characterization to achieve defect-free injection molded parts efficiently."
        ),
        entity_scope="Thermoplastic polymer injection molding",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Rosato (2000), Strong (2006)"
    ),
    DoctrineBlock(
        topic="Polymer Degradation: Thermal",
        keywords=[
            "thermal degradation", "polymer stability", "chain scission",
            "crosslinking", "oxidation", "activation energy", "decomposition",
            "thermal aging", "stabilizers", "kinetics"
        ],
        conclusion_template=(
            "Thermal degradation of polymers involves chain scission and crosslinking reactions initiated by heat, leading to changes in molecular weight and material properties."
        ),
        reasoning_framework=(
            "When polymers are exposed to elevated temperatures, chemical bonds may break (chain scission) or form new crosslinks, altering polymer structure. Thermal degradation kinetics depend on "
            "activation energy and temperature, often following Arrhenius behavior. Oxidative degradation occurs in the presence of oxygen, generating free radicals that propagate degradation. "
            "Thermal aging results in embrittlement, discoloration, and loss of mechanical properties. Stabilizers such as antioxidants and UV absorbers are incorporated to retard degradation. "
            "Analytical techniques like TGA and DSC monitor degradation onset and progression. Understanding degradation mechanisms guides material selection and processing conditions to enhance durability."
        ),
        key_factors=[
            "Polymer chemical structure",
            "Temperature and exposure time",
            "Presence of oxygen and moisture",
            "Additives and stabilizers",
            "Molecular weight",
            "Processing history"
        ],
        primary_authority=[
            "Billmeyer, F. W., Textbook of Polymer Science, Wiley, 1984",
            "Krevelen, D. W., Properties of Polymers, 4th Ed., Elsevier, 2009"
        ],
        burden_holder="Materials scientist or polymer engineer",
        adversary_position=(
            "Argues that thermal degradation cannot be effectively controlled in high-temperature applications."
        ),
        counter_arguments=[
            "Use of stabilizers and optimized processing extends polymer lifetime.",
            "Thermal analysis and kinetic modeling predict degradation behavior.",
            "Material selection tailored to application temperature mitigates degradation."
        ],
        resolution_strategy=(
            "Implement stabilizer packages and monitor thermal exposure to manage degradation and ensure performance."
        ),
        entity_scope="Thermal stability of polymers under processing and service conditions",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Billmeyer (1984), Krevelen (2009)"
    ),
    DoctrineBlock(
        topic="Polymer Degradation: UV",
        keywords=[
            "UV degradation", "photodegradation", "photooxidation", "free radicals",
            "chromophores", "stabilizers", "UV absorbers", "polymer chain scission",
            "discoloration", "surface degradation"
        ],
        conclusion_template=(
            "UV degradation of polymers results from absorption of ultraviolet radiation, generating free radicals that cause chain scission and photooxidation, leading to material embrittlement and discoloration."
        ),
        reasoning_framework=(
            "Exposure to UV radiation excites chromophoric groups within polymers or additives, generating free radicals that initiate chain scission and oxidation reactions. This photodegradation "
            "primarily affects polymer surfaces, causing discoloration, loss of mechanical integrity, and surface cracking. The rate and extent depend on polymer chemistry, presence of UV stabilizers, "
            "and environmental conditions such as oxygen and moisture. UV absorbers and hindered amine light stabilizers (HALS) are incorporated to mitigate damage by absorbing harmful radiation "
            "or scavenging radicals. Accelerated weathering tests simulate long-term exposure to evaluate polymer durability."
        ),
        key_factors=[
            "Polymer chemical structure and chromophores",
            "UV radiation intensity and wavelength",
            "Oxygen availability",
            "Presence and type of UV stabilizers",
            "Environmental moisture",
            "Exposure duration"
        ],
        primary_authority=[
            "Allen, N. S., Edge, M., Fundamentals of Polymer Degradation and Stabilization, Springer, 1992",
            "Wypych, G., Handbook of UV Degradation and Stabilization, ChemTec Publishing, 2012"
        ],
        burden_holder="Materials scientist or polymer formulator",
        adversary_position=(
            "Claims that UV stabilization is ineffective for long-term outdoor polymer applications."
        ),
        counter_arguments=[
            "Combination of UV absorbers and HALS significantly extends service life.",
            "Surface coatings and additives reduce UV penetration and damage.",
            "Accelerated testing validates stabilization strategies."
        ],
        resolution_strategy=(
            "Design polymer formulations with appropriate UV stabilizers and validate performance under simulated environmental conditions."
        ),
        entity_scope="Photodegradation of polymers exposed to sunlight",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Allen & Edge (1992), Wypych (2012)"
    ),
    DoctrineBlock(
        topic="Polymer Degradation: Oxidative",
        keywords=[
            "oxidative degradation", "autoxidation", "free radicals", "peroxides",
            "chain scission", "crosslinking", "antioxidants", "thermal oxidation",
            "polymer aging", "stabilization"
        ],
        conclusion_template=(
            "Oxidative degradation involves free radical chain reactions initiated by heat or mechanical stress, leading to polymer chain scission and crosslinking, which degrade material properties."
        ),
        reasoning_framework=(
            "Polymers exposed to oxygen at elevated temperatures or under mechanical stress undergo autoxidation, a free radical chain reaction involving initiation, propagation, and termination steps. "
            "Hydroperoxides formed during propagation decompose to generate new radicals, accelerating degradation. Chain scission reduces molecular weight, while crosslinking increases brittleness. "
            "Antioxidants such as hindered phenols and phosphites interrupt radical propagation, enhancing polymer stability. The balance between degradation and stabilization determines polymer lifetime. "
            "Analytical methods including FTIR and chemiluminescence detect oxidative changes. Understanding these mechanisms informs material design and processing to minimize oxidative damage."
        ),
        key_factors=[
            "Temperature and oxygen concentration",
            "Polymer chemical structure",
            "Mechanical stress and processing conditions",
            "Presence and type of antioxidants",
            "Molecular weight and morphology",
            "Exposure duration"
        ],
        primary_authority=[
            "Billmeyer, F. W., Textbook of Polymer Science, Wiley, 1984",
            "Krevelen, D. W., Properties of Polymers, 4th Ed., Elsevier, 2009"
        ],
        burden_holder="Materials scientist or polymer engineer",
        adversary_position=(
            "Suggests that antioxidants are insufficient to prevent oxidative degradation in demanding applications."
        ),
        counter_arguments=[
            "Optimized antioxidant packages significantly retard oxidation.",
            "Processing conditions minimizing thermal and mechanical stress reduce degradation.",
            "Material selection and design improve oxidative stability."
        ],
        resolution_strategy=(
            "Employ comprehensive stabilization strategies and monitor oxidative markers to ensure polymer durability."
        ),
        entity_scope="Oxidative stability of polymers under thermal and mechanical stress",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Billmeyer (1984), Krevelen (2009)"
    ),
    DoctrineBlock(
        topic="Polymer Degradation: Hydrolytic",
        keywords=[
            "hydrolytic degradation", "ester hydrolysis", "amide hydrolysis",
            "polyester", "polyamide", "water absorption", "acid/base catalysis",
            "molecular weight reduction", "environmental stress cracking",
            "biodegradation"
        ],
        conclusion_template=(
            "Hydrolytic degradation involves cleavage of susceptible bonds such as esters and amides in polymers upon exposure to moisture, leading to molecular weight reduction and property loss."
        ),
        reasoning_framework=(
            "Polymers containing hydrolyzable groups (e.g., esters in polyesters, amides in polyamides) undergo bond cleavage when exposed to water, especially under acidic or basic conditions. "
            "Water molecules attack the polymer backbone, breaking covalent bonds and reducing molecular weight. This process is accelerated by elevated temperature, pH extremes, and mechanical stress. "
            "Water absorption and diffusion into the polymer matrix influence degradation rate. Hydrolytic degradation compromises mechanical properties and can lead to environmental stress cracking. "
            "In biodegradable polymers, hydrolysis is a key mechanism for controlled degradation. Analytical techniques such as GPC and FTIR monitor molecular weight changes and chemical structure alterations."
        ),
        key_factors=[
            "Polymer chemical structure and bond susceptibility",
            "Water availability and diffusion",
            "pH and catalytic species",
            "Temperature",
            "Mechanical stress",
            "Additives and stabilizers"
        ],
        primary_authority=[
            "Vert, M., et al., Biodegradable Polymers and Plastics, Springer, 2012",
            "Krevelen, D. W., Properties of Polymers, 4th Ed., Elsevier, 2009"
        ],
        burden_holder="Materials scientist or polymer engineer",
        adversary_position=(
            "Claims hydrolytic degradation is negligible in most polymer applications."
        ),
        counter_arguments=[
            "Hydrolysis is significant in polyesters and polyamides exposed to moisture.",
            "Accelerated aging tests demonstrate measurable degradation.",
            "Material design and coatings mitigate hydrolytic effects."
        ],
        resolution_strategy=(
            "Evaluate hydrolytic stability through accelerated testing and tailor polymer chemistry for intended environment."
        ),
        entity_scope="Hydrolytic stability of susceptible polymers",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Vert et al. (2012), Krevelen (2009)"
    ),
    DoctrineBlock(
        topic="Polymer Blends and Compatibilization",
        keywords=[
            "polymer blends", "compatibilization", "phase separation",
            "interfacial adhesion", "block copolymers", "reactive compatibilizers",
            "morphology control", "mechanical properties", "miscibility",
            "processing"
        ],
        conclusion_template=(
            "Compatibilization of polymer blends improves interfacial adhesion and morphology, enhancing mechanical properties and stability of immiscible polymer mixtures."
        ),
        reasoning_framework=(
            "Polymer blends combine two or more polymers to achieve tailored properties. Most polymers are immiscible, leading to phase separation and poor interfacial adhesion, which degrade mechanical performance. "
            "Compatibilizers, such as block or graft copolymers with segments miscible in each phase, localize at interfaces, reducing interfacial tension and stabilizing morphology. Reactive compatibilizers form covalent bonds "
            "during processing, improving adhesion. Morphology control via processing conditions and compatibilizer concentration influences toughness, strength, and thermal properties. Analytical techniques like TEM and AFM characterize blend morphology."
        ),
        key_factors=[
            "Polymer pair miscibility",
            "Compatibilizer type and concentration",
            "Processing temperature and shear",
            "Molecular weight and architecture",
            "Interfacial tension",
            "Blend ratio"
        ],
        primary_authority=[
            "Paul, D. R., Bucknall, C. B., Polymer Blends, Wiley, 2000",
            "Utracki, L. A., Polymer Blends Handbook, Springer, 2002"
        ],
        burden_holder="Polymer formulator or materials scientist",
        adversary_position=(
            "Asserts that compatibilization cannot fully overcome immiscibility in polymer blends."
        ),
        counter_arguments=[
            "Effective compatibilizers significantly improve blend properties.",
            "Processing optimization enhances morphology control.",
            "Reactive compatibilization forms stable interfaces."
        ],
        resolution_strategy=(
            "Develop and apply compatibilizers tailored to polymer pairs and processing conditions to achieve desired blend performance."
        ),
        entity_scope="Polymer blend formulation and processing",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Paul & Bucknall (2000), Utracki (2002)"
    ),
    DoctrineBlock(
        topic="Biopolymers and Biodegradable Polymers",
        keywords=[
            "biopolymers", "biodegradable polymers", "polylactic acid",
            "polyhydroxyalkanoates", "degradation mechanisms", "compostability",
            "renewable resources", "environmental impact", "polymer synthesis",
            "sustainability"
        ],
        conclusion_template=(
            "Biopolymers and biodegradable polymers derived from renewable resources offer environmentally friendly alternatives with controlled degradation pathways."
        ),
        reasoning_framework=(
            "Biopolymers such as polylactic acid (PLA) and polyhydroxyalkanoates (PHA) are synthesized from renewable feedstocks and designed to degrade via hydrolytic or enzymatic mechanisms. "
            "Biodegradation involves microbial assimilation of polymer fragments, leading to mineralization under composting or environmental conditions. Polymer synthesis routes include ring-opening polymerization and fermentation. "
            "Material properties such as crystallinity, molecular weight, and additives influence degradation rate and mechanical performance. Life cycle assessment evaluates environmental benefits. Challenges include balancing durability and degradability."
        ),
        key_factors=[
            "Polymer chemical structure",
            "Molecular weight and crystallinity",
            "Environmental conditions (temperature, moisture, microbes)",
            "Additives and plasticizers",
            "Processing methods",
            "End-of-life scenarios"
        ],
        primary_authority=[
            "Auras, R., et al., Polylactic Acid: Synthesis, Properties, Processing, and Applications, Wiley, 2010",
            "Chen, G.-Q., Biodegradable Plastics, Springer, 2010"
        ],
        burden_holder="Polymer scientist or sustainability analyst",
        adversary_position=(
            "Claims biopolymers lack sufficient performance and biodegradability under real-world conditions."
        ),
        counter_arguments=[
            "Material design optimizes mechanical properties and degradation rates.",
            "Standardized testing protocols validate biodegradability.",
            "Ongoing research improves biopolymer formulations."
        ],
        resolution_strategy=(
            "Integrate material development with environmental testing to ensure performance and sustainability."
        ),
        entity_scope="Biopolymer synthesis and environmental degradation",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Auras et al. (2010), Chen (2010)"
    ),
    DoctrineBlock(
        topic="Oilfield Polymer Applications: EOR and Drilling Fluids",
        keywords=[
            "enhanced oil recovery", "EOR", "drilling fluids", "polymer flooding",
            "viscosity modification", "shear stability", "thermal stability",
            "polyacrylamide", "biopolymers", "reservoir conditions"
        ],
        conclusion_template=(
            "Polymers used in oilfield applications enhance recovery and drilling performance by modifying fluid rheology and stability under harsh reservoir conditions."
        ),
        reasoning_framework=(
            "In enhanced oil recovery (EOR), polymers such as partially hydrolyzed polyacrylamide (HPAM) increase water viscosity, improving sweep efficiency and oil displacement. "
            "Polymers must withstand high salinity, temperature, and shear conditions without significant degradation. In drilling fluids, polymers control viscosity, filtration, and suspension of cuttings. "
            "Biopolymers like xanthan gum offer biodegradability and shear tolerance. Polymer selection balances performance, cost, and environmental impact. Rheological properties and degradation behavior are critical for application success."
        ),
        key_factors=[
            "Polymer type and molecular weight",
            "Reservoir temperature and salinity",
            "Shear and mechanical degradation",
            "Polymer concentration",
            "Compatibility with reservoir fluids",
            "Environmental regulations"
        ],
        primary_authority=[
            "Lake, L. W., Enhanced Oil Recovery, Prentice Hall, 1989",
            "Sheng, J. J., Modern Chemical Enhanced Oil Recovery, Gulf Professional Publishing, 2011"
        ],
        burden_holder="Petroleum engineer or polymer chemist",
        adversary_position=(
            "Argues polymers degrade rapidly under reservoir conditions, limiting effectiveness."
        ),
        counter_arguments=[
            "Advanced polymer chemistries improve thermal and shear stability.",
            "Field trials demonstrate successful polymer flooding.",
            "Additives and formulations mitigate degradation."
        ],
        resolution_strategy=(
            "Conduct laboratory and field testing to optimize polymer formulations for reservoir conditions."
        ),
        entity_scope="Polymer applications in oilfield EOR and drilling fluids",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Lake (1989), Sheng (2011)"
    ),
    DoctrineBlock(
        topic="Polymer Composites: Fiber Reinforcement",
        keywords=[
            "polymer composites", "fiber reinforcement", "mechanical properties",
            "interface adhesion", "fiber-matrix interaction", "load transfer",
            "composite processing", "fiber orientation", "matrix selection",
            "damage mechanisms"
        ],
        conclusion_template=(
            "Fiber reinforcement in polymer composites enhances mechanical properties through effective load transfer and interface adhesion between fibers and matrix."
        ),
        reasoning_framework=(
            "Polymer composites combine a polymer matrix with reinforcing fibers such as glass, carbon, or aramid to improve strength, stiffness, and toughness. The fiber-matrix interface is critical for load transfer; "
            "poor adhesion leads to debonding and reduced performance. Fiber orientation and volume fraction influence anisotropy and mechanical behavior. Processing methods (e.g., lay-up, pultrusion, injection molding) affect fiber dispersion and alignment. "
            "Damage mechanisms include fiber breakage, matrix cracking, and delamination. Composite design balances mechanical requirements, weight, cost, and manufacturability."
        ),
        key_factors=[
            "Fiber type and properties",
            "Matrix chemistry and properties",
            "Fiber volume fraction and orientation",
            "Interface adhesion and coupling agents",
            "Processing method",
            "Environmental exposure"
        ],
        primary_authority=[
            "Mallick, P. K., Fiber-Reinforced Composites, 3rd Ed., CRC Press, 2007",
            "Hull, D., Clyne, T. W., An Introduction to Composite Materials, 2nd Ed., Cambridge University Press, 1996"
        ],
        burden_holder="Composite materials engineer or polymer scientist",
        adversary_position=(
            "Claims fiber reinforcement does not significantly improve polymer properties due to interface weaknesses."
        ),
        counter_arguments=[
            "Use of coupling agents and surface treatments enhances adhesion.",
            "Optimized fiber orientation maximizes mechanical benefits.",
            "Processing controls fiber dispersion and interface quality."
        ],
        resolution_strategy=(
            "Employ surface modification and processing optimization to achieve desired composite performance."
        ),
        entity_scope="Fiber-reinforced polymer composites",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Mallick (2007), Hull & Clyne (1996)"
    ),
    DoctrineBlock(
        topic="Free Radical Addition Polymerization: Initiation Mechanisms",
        keywords=[
            "free radical initiation", "thermal initiators", "photoinitiators",
            "redox initiation", "radical generation", "benzoyl peroxide",
            "AIBN", "radical stability", "initiation rate"
        ],
        conclusion_template=(
            "Initiation in free radical polymerization involves generation of radicals via thermal, photochemical, or redox processes that start chain growth."
        ),
        reasoning_framework=(
            "Radical initiation is the first step in free radical polymerization, generating reactive species that add to monomers. Thermal initiators such as benzoyl peroxide decompose upon heating to form radicals. "
            "Photoinitiators generate radicals upon UV or visible light exposure, enabling spatial and temporal control. Redox initiators combine oxidizing and reducing agents to produce radicals at lower temperatures. "
            "Initiation rate affects polymerization kinetics and molecular weight distribution. Radical stability influences initiation efficiency and side reactions. Understanding initiation mechanisms guides initiator selection and process design."
        ),
        key_factors=[
            "Initiator type and concentration",
            "Temperature and light intensity",
            "Solvent and monomer environment",
            "Radical half-life and reactivity",
            "Decomposition kinetics"
        ],
        primary_authority=[
            "Odian, G., Principles of Polymerization, Wiley, 2004",
            "Brandrup, J., Immergut, E. H., Polymer Handbook, Wiley, 1999"
        ],
        burden_holder="Polymer chemist or process engineer",
        adversary_position=(
            "Suggests initiation methods lack control leading to broad molecular weight distributions."
        ),
        counter_arguments=[
            "Controlled initiation techniques and optimized conditions improve polymer uniformity.",
            "Use of photoinitiators enables precise initiation control.",
            "Kinetic studies allow prediction and tuning of initiation rates."
        ],
        resolution_strategy=(
            "Select appropriate initiators and conditions based on polymerization requirements and monomer characteristics."
        ),
        entity_scope="Initiation step in free radical polymerization",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Odian (2004), Brandrup (1999)"
    ),
    DoctrineBlock(
        topic="Living Radical Polymerization: ATRP Mechanism",
        keywords=[
            "ATRP", "atom transfer radical polymerization", "transition metal catalyst",
            "reversible activation", "dormant species", "radical equilibrium",
            "copper catalyst", "ligands", "polymerization control"
        ],
        conclusion_template=(
            "ATRP controls radical polymerization through reversible activation/deactivation mediated by transition metal catalysts, enabling living polymer growth."
        ),
        reasoning_framework=(
            "ATRP employs a transition metal complex, typically copper with ligands, to reversibly activate dormant alkyl halide species to radicals that propagate polymer chains. "
            "The equilibrium between active radicals and dormant species limits termination and allows chain growth control. Ligand choice affects catalyst activity and polymerization kinetics. "
            "The process enables synthesis of polymers with predetermined molecular weights and narrow dispersity. Control depends on maintaining catalyst redox balance and minimizing side reactions."
        ),
        key_factors=[
            "Catalyst and ligand selection",
            "Monomer and initiator compatibility",
            "Reaction temperature",
            "Solvent effects",
            "Equilibrium constant for activation/deactivation",
            "Oxygen sensitivity"
        ],
        primary_authority=[
            "Matyjaszewski, K., Macromolecules, 2012",
            "Matyjaszewski, K., Controlled Radical Polymerization, ACS Symposium Series, 2003"
        ],
        burden_holder="Polymer chemist or synthetic scientist",
        adversary_position=(
            "Claims ATRP catalysts are too sensitive and limit practical applications."
        ),
        counter_arguments=[
            "Advances in catalyst design improve robustness and oxygen tolerance.",
            "Ligand engineering enhances catalyst stability.",
            "Process optimization enables scalable ATRP."
        ],
        resolution_strategy=(
            "Develop and apply improved catalysts and protocols to expand ATRP applicability."
        ),
        entity_scope="ATRP controlled radical polymerization",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Matyjaszewski (2012)"
    ),
    DoctrineBlock(
        topic="Living Radical Polymerization: RAFT Mechanism",
        keywords=[
            "RAFT", "reversible addition-fragmentation chain transfer",
            "chain transfer agent", "thiocarbonylthio", "radical equilibrium",
            "polymerization control", "living polymerization", "molecular weight",
            "dispersity"
        ],
        conclusion_template=(
            "RAFT polymerization uses chain transfer agents to mediate radical polymerization, enabling control over molecular weight and polymer architecture."
        ),
        reasoning_framework=(
            "RAFT polymerization involves addition of propagating radicals to a thiocarbonylthio chain transfer agent, forming intermediate radicals that fragment to release dormant chains and new radicals. "
            "This reversible addition-fragmentation process establishes an equilibrium between active and dormant species, minimizing termination and allowing controlled chain growth. "
            "RAFT agents are tailored for specific monomers and reaction conditions. The method enables synthesis of block copolymers and complex architectures with narrow molecular weight distributions."
        ),
        key_factors=[
            "RAFT agent structure and concentration",
            "Monomer compatibility",
            "Reaction temperature",
            "Solvent effects",
            "Initiator efficiency",
            "Equilibrium constants"
        ],
        primary_authority=[
            "Chiefari, J., Macromolecules, 1998",
            "Moad, G., Rizzardo, E., Thang, S. H., Polymer, 2008"
        ],
        burden_holder="Polymer chemist or synthetic scientist",
        adversary_position=(
            "Asserts RAFT agents introduce impurities and side reactions limiting polymer quality."
        ),
        counter_arguments=[
            "Purification and optimized RAFT agents reduce impurities.",
            "Side reactions are minimized under controlled conditions.",
            "Extensive studies validate RAFT polymer quality."
        ],
        resolution_strategy=(
            "Select appropriate RAFT agents and optimize reaction conditions to achieve high-quality polymers."
        ),
        entity_scope="RAFT controlled radical polymerization",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Chiefari (1998), Moad et al. (2008)"
    ),
    DoctrineBlock(
        topic="Living Radical Polymerization: NMP Mechanism",
        keywords=[
            "NMP", "nitroxide mediated polymerization", "stable nitroxide",
            "reversible capping", "radical equilibrium", "polymerization control",
            "living polymerization", "molecular weight", "dispersity"
        ],
        conclusion_template=(
            "NMP controls radical polymerization via reversible capping of growing radicals by stable nitroxide species, enabling living polymer growth."
        ),
        reasoning_framework=(
            "NMP employs stable nitroxide radicals that reversibly bind to propagating polymer radicals, forming dormant species and establishing an equilibrium that limits termination. "
            "This reversible capping allows controlled chain growth with predictable molecular weights and narrow dispersity. The choice of nitroxide and reaction conditions affects control efficiency. "
            "NMP is compatible with styrenic and acrylate monomers and enables synthesis of block copolymers and complex architectures."
        ),
        key_factors=[
            "Nitroxide structure and concentration",
            "Monomer compatibility",
            "Reaction temperature",
            "Solvent effects",
            "Initiator efficiency",
            "Equilibrium constants"
        ],
        primary_authority=[
            "Georges, M. K., Prog. Polym. Sci., 2000",
            "Matyjaszewski, K., Controlled Radical Polymerization, ACS Symposium Series, 2003"
        ],
        burden_holder="Polymer chemist or synthetic scientist",
        adversary_position=(
            "Claims NMP is limited by slow kinetics and narrow monomer scope."
        ),
        counter_arguments=[
            "Nitroxide design improvements expand monomer compatibility.",
            "Process optimization enhances polymerization rates.",
            "NMP complements other CRP methods for specific applications."
        ],
        resolution_strategy=(
            "Develop advanced nitroxides and optimize conditions to broaden NMP applicability."
        ),
        entity_scope="NMP controlled radical polymerization",
        confidence=0.90,
        confidence_zone="Moderate-High",
        controlling_precedent="Georges (2000), Matyjaszewski (2003)"
    ),
    DoctrineBlock(
        topic="Polymer Processing: Extrusion",
        keywords=[
            "extrusion", "polymer melt", "screw design", "die swell",
            "shear heating", "pressure profile", "thermal degradation",
            "processing parameters", "material homogeneity", "additive dispersion"
        ],
        conclusion_template=(
            "Extrusion processing requires control of melt flow, temperature, and pressure to produce homogeneous polymer products with desired properties."
        ),
        reasoning_framework=(
            "Extrusion involves forcing molten polymer through a shaped die using a rotating screw. Screw design influences shear rate, mixing, and residence time. Die swell occurs due to polymer elasticity upon exiting the die. "
            "Shear heating raises melt temperature, which must be controlled to prevent thermal degradation. Pressure profiles along the extruder affect flow stability. Additive dispersion and material homogeneity depend on mixing efficiency. "
            "Processing parameters including screw speed, barrel temperature, and back pressure are optimized for product quality and throughput."
        ),
        key_factors=[
            "Screw geometry and speed",
            "Barrel temperature profile",
            "Die design",
            "Polymer rheology",
            "Additive compatibility",
            "Residence time"
        ],
        primary_authority=[
            "Rosato, D. V., Rosato, D. V., Injection Molding Handbook, Springer, 2000",
            "Strong, A. B., Plastics: Materials and Processing, Pearson, 2006"
        ],
        burden_holder="Process engineer or polymer technologist",
        adversary_position=(
            "Suggests extrusion cannot achieve uniform additive dispersion or prevent degradation."
        ),
        counter_arguments=[
            "Optimized screw and die design improve mixing and reduce degradation.",
            "Process monitoring and control maintain product consistency.",
            "Material selection and additives enhance stability."
        ],
        resolution_strategy=(
            "Apply process simulation and experimental optimization to achieve desired extrusion outcomes."
        ),
        entity_scope="Polymer extrusion processing",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Rosato (2000), Strong (2006)"
    ),
    DoctrineBlock(
        topic="Polymer Processing: Blow Molding",
        keywords=[
            "blow molding", "polymer processing", "parison formation",
            "stretch blow molding", "cooling rate", "wall thickness",
            "molecular orientation", "processing parameters", "defects",
            "material selection"
        ],
        conclusion_template=(
            "Blow molding processes shape hollow polymer parts by inflating a molten parison, with control of cooling and orientation critical for part quality."
        ),
        reasoning_framework=(
            "Blow molding involves extruding or injection molding a molten polymer parison, which is inflated inside a mold to form hollow parts such as bottles. Stretch blow molding adds biaxial orientation, improving mechanical properties. "
            "Cooling rate affects crystallinity and residual stresses, influencing dimensional stability and clarity. Wall thickness distribution depends on parison control and blowing parameters. Defects such as uneven thickness, weld lines, or air entrapment arise from processing inconsistencies. "
            "Material selection balances melt strength, clarity, and barrier properties."
        ),
        key_factors=[
            "Parison temperature and thickness",
            "Blowing pressure and speed",
            "Mold temperature and cooling",
            "Polymer melt strength",
            "Stretch ratio",
            "Material crystallinity"
        ],
        primary_authority=[
            "Strong, A. B., Plastics: Materials and Processing, Pearson, 2006",
            "Rosato, D. V., Rosato, D. V., Injection Molding Handbook, Springer, 2000"
        ],
        burden_holder="Process engineer or polymer technologist",
        adversary_position=(
            "Claims blow molding cannot produce uniform parts with consistent properties."
        ),
        counter_arguments=[
            "Advanced parison control and mold design improve uniformity.",
            "Process monitoring reduces defects.",
            "Material selection tailored to process enhances performance."
        ],
        resolution_strategy=(
            "Optimize processing parameters and material formulations to achieve high-quality blow molded parts."
        ),
        entity_scope="Polymer blow molding processing",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Strong (2006), Rosato (2000)"
    ),
    DoctrineBlock(
        topic="Polymer Processing: Compression Molding",
        keywords=[
            "compression molding", "polymer processing", "thermosets",
            "pressure application", "curing", "mold design", "cycle time",
            "thermal conductivity", "part thickness", "material flow"
        ],
        conclusion_template=(
            "Compression molding shapes polymers by applying heat and pressure in a mold, curing thermosets or shaping thermoplastics with controlled flow."
        ),
        reasoning_framework=(
            "In compression molding, polymer material is placed in an open mold cavity and compressed by closing the mold under heat and pressure. For thermosets, curing reactions occur during molding, solidifying the part. "
            "For thermoplastics, the process shapes the material with minimal flow compared to injection molding. Mold design influences heat transfer and pressure distribution, affecting part quality and cycle time. "
            "Material flow and thickness uniformity are critical to avoid defects such as voids or incomplete filling. Thermal conductivity of mold and polymer affects curing and cooling rates."
        ),
        key_factors=[
            "Material type (thermoset or thermoplastic)",
            "Mold temperature and pressure",
            "Cycle time",
            "Material flow characteristics",
            "Part geometry and thickness",
            "Curing kinetics"
        ],
        primary_authority=[
            "Strong, A. B., Plastics: Materials and Processing, Pearson, 2006",
            "Rosato, D. V., Rosato, D. V., Injection Molding Handbook, Springer, 2000"
        ],
        burden_holder="Process engineer or polymer technologist",
        adversary_position=(
            "Suggests compression molding is inefficient and produces inconsistent parts."
        ),
        counter_arguments=[
            "Proper mold design and process control yield consistent parts.",
            "Compression molding is cost-effective for large, simple parts.",
            "Material selection and curing optimization improve quality."
        ],
        resolution_strategy=(
            "Employ process optimization and material characterization to maximize compression molding efficiency."
        ),
        entity_scope="Polymer compression molding processing",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Strong (2006), Rosato (2000)"
    ),
    DoctrineBlock(
        topic="Polymer Degradation: Mechanical",
        keywords=[
            "mechanical degradation", "chain scission", "stress cracking",
            "fatigue", "abrasion", "impact resistance", "molecular weight",
            "processing damage", "environmental stress cracking", "fracture"
        ],
        conclusion_template=(
            "Mechanical degradation results from physical stresses causing chain scission, microcracking, and loss of mechanical properties in polymers."
        ),
        reasoning_framework=(
            "Polymers subjected to mechanical stresses such as tension, compression, abrasion, or impact may experience chain scission and microstructural damage. "
            "Repeated cyclic loading leads to fatigue and environmental stress cracking, especially in presence of chemicals or moisture. Molecular weight reduction from chain scission decreases toughness and elongation at break. "
            "Processing steps like extrusion or molding can induce mechanical degradation if parameters are not optimized. Understanding mechanical degradation mechanisms informs material selection and design for durability."
        ),
        key_factors=[
            "Type and magnitude of mechanical stress",
            "Environmental conditions",
            "Polymer molecular weight and structure",
            "Additives and fillers",
            "Processing history",
            "Exposure duration"
        ],
        primary_authority=[
            "Billmeyer, F. W., Textbook of Polymer Science, Wiley, 1984",
            "Krevelen, D. W., Properties of Polymers, 4th Ed., Elsevier, 2009"
        ],
        burden_holder="Materials scientist or polymer engineer",
        adversary_position=(
            "Claims mechanical degradation is negligible in well-processed polymers."
        ),
        counter_arguments=[
            "Mechanical degradation is evident in fatigue and environmental stress cracking tests.",
            "Processing optimization minimizes induced damage.",
            "Material design enhances mechanical durability."
        ],
        resolution_strategy=(
            "Evaluate mechanical degradation through testing and optimize processing and formulation accordingly."
        ),
        entity_scope="Mechanical durability of polymers",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Billmeyer (1984), Krevelen (2009)"
    ),
    DoctrineBlock(
        topic="Polymer Composites: Matrix Selection",
        keywords=[
            "polymer matrix", "thermoplastic", "thermoset", "matrix properties",
            "compatibility", "processing", "mechanical properties", "thermal stability",
            "chemical resistance", "composite performance"
        ],
        conclusion_template=(
            "Selection of polymer matrix in composites critically influences processing, mechanical properties, and environmental resistance."
        ),
        reasoning_framework=(
            "The polymer matrix binds reinforcing fibers and transfers load in composites. Thermoplastics offer recyclability and toughness, while thermosets provide superior thermal and chemical resistance. "
            "Matrix compatibility with fibers affects interface adhesion and composite performance. Processing methods vary depending on matrix type, influencing fiber wetting and dispersion. "
            "Matrix properties such as glass transition temperature, modulus, and elongation determine composite behavior under service conditions. Chemical resistance and thermal stability are vital for application environments."
        ),
        key_factors=[
            "Matrix polymer type and properties",
            "Fiber compatibility",
            "Processing method",
            "Thermal and chemical resistance",
            "Mechanical properties",
            "Environmental exposure"
        ],
        primary_authority=[
            "Mallick, P. K., Fiber-Reinforced Composites, CRC Press, 2007",
            "Hull, D., Clyne, T. W., An Introduction to Composite Materials, Cambridge University Press, 1996"
        ],
        burden_holder="Composite materials engineer or polymer scientist",
        adversary_position=(
            "Suggests matrix selection has limited impact on composite performance."
        ),
        counter_arguments=[
            "Matrix properties strongly influence composite mechanical and environmental behavior.",
            "Optimized matrix-fiber compatibility enhances load transfer.",
            "Processing considerations depend on matrix choice."
        ],
        resolution_strategy=(
            "Select matrix polymers based on application requirements and fiber compatibility to optimize composite performance."
        ),
        entity_scope="Polymer matrix selection for composites",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Mallick (2007), Hull & Clyne (1996)"
    ),
    DoctrineBlock(
        topic="Polymer Blends: Thermodynamics of Mixing",
        keywords=[
            "polymer blends", "miscibility", "Flory-Huggins theory",
            "interaction parameter", "phase separation", "entropy",
            "enthalpy", "temperature dependence", "morphology"
        ],
        conclusion_template=(
            "Polymer blend miscibility is governed by thermodynamics of mixing, with phase behavior predicted by Flory-Huggins theory and interaction parameters."
        ),
        reasoning_framework=(
            "The miscibility of polymer blends depends on the balance of entropic and enthalpic contributions to the Gibbs free energy of mixing. Flory-Huggins theory models this using segmental volume fractions and an interaction parameter (χ). "
            "Positive χ values indicate unfavorable interactions leading to phase separation, while negative or low χ values favor miscibility. Temperature influences miscibility via the temperature dependence of χ. "
            "Phase diagrams predict single-phase or multiphase regions. Miscibility affects morphology, mechanical properties, and processing behavior. Compatibilizers can modify χ and improve blend stability."
        ),
        key_factors=[
            "Polymer chemical structure",
            "Interaction parameter (χ)",
            "Temperature",
            "Molecular weight",
            "Blend composition",
            "Compatibilizer presence"
        ],
        primary_authority=[
            "Paul, D. R., Barlow, J. W., Polymer Blends, Academic Press, 1978",
            "Utracki, L. A., Polymer Blends Handbook, Springer, 2002"
        ],
        burden_holder="Polymer scientist or formulator",
        adversary_position=(
            "Claims thermodynamics cannot predict blend miscibility accurately."
        ),
        counter_arguments=[
            "Flory-Huggins theory provides qualitative and quantitative predictions.",
            "Experimental phase diagrams validate theoretical models.",
            "Compatibilization strategies adjust miscibility."
        ],
        resolution_strategy=(
            "Combine theoretical modeling with experimental validation to guide blend formulation."
        ),
        entity_scope="Thermodynamics of polymer blends",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Paul & Barlow (1978), Utracki (2002)"
    ),
    DoctrineBlock(
        topic="Polymer Rheology: Time-Temperature Superposition",
        keywords=[
            "time-temperature superposition", "viscoelasticity", "master curve",
            "shift factor", "Williams-Landel-Ferry equation", "relaxation time",
            "temperature dependence", "polymer melts", "dynamic mechanical analysis"
        ],
        conclusion_template=(
            "Time-temperature superposition principle enables construction of master curves describing polymer viscoelastic behavior over wide time and temperature ranges."
        ),
        reasoning_framework=(
            "Viscoelastic properties of polymers depend on time (or frequency) and temperature. Time-temperature superposition (TTS) shifts viscoelastic data measured at various temperatures horizontally along the log time/frequency axis to form a master curve at a reference temperature. "
            "The shift factor (aT) quantifies this horizontal shift and is often modeled by the Williams-Landel-Ferry (WLF) equation near Tg or Arrhenius behavior at higher temperatures. Master curves provide comprehensive insight into polymer relaxation and flow behavior beyond experimental timescales. "
            "TTS assumes thermorheological simplicity, which holds for many amorphous polymers but may fail for complex systems."
        ),
        key_factors=[
            "Temperature range",
            "Reference temperature",
            "Polymer type and morphology",
            "Measurement frequency/time",
            "Thermorheological simplicity",
            "Shift factor modeling"
        ],
        primary_authority=[
            "Ferry, J. D., Viscoelastic Properties of Polymers, Wiley, 1980",
            "Williams, M. L., Landel, R. F., Ferry, J. D., J. Am. Chem. Soc., 1955"
        ],
        burden_holder="Polymer rheologist or materials scientist",
        adversary_position=(
            "Argues TTS is invalid for polymers with complex morphologies or phase behavior."
        ),
        counter_arguments=[
            "TTS is valid for many amorphous polymers and provides useful approximations.",
            "Deviations can be identified and accounted for in analysis.",
            "Complementary techniques validate viscoelastic predictions."
        ],
        resolution_strategy=(
            "Apply TTS judiciously with awareness of its limitations and validate with experimental data."
        ),
        entity_scope="Polymer viscoelastic behavior characterization",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Ferry (1980), Williams et al. (1955)"
    ),
    DoctrineBlock(
        topic="Polymer Processing: Thermoforming",
        keywords=[
            "thermoforming", "sheet heating", "mold forming", "cooling",
            "material thinning", "orientation", "processing parameters",
            "defects", "polymer sheets", "cycle time"
        ],
        conclusion_template=(
            "Thermoforming shapes heated polymer sheets over molds, with control of heating and cooling critical to part quality and dimensional accuracy."
        ),
        reasoning_framework=(
            "In thermoforming, polymer sheets are heated to a pliable temperature and formed over molds by vacuum, pressure, or mechanical means. Heating must be uniform to avoid thinning or tearing. "
            "Cooling solidifies the part, with cooling rate affecting crystallinity and residual stresses. Material orientation induced during forming influences mechanical properties and shrinkage. "
            "Processing parameters such as sheet temperature, mold temperature, and forming speed are optimized to minimize defects like warpage, sink marks, or uneven thickness. Material selection balances formability and performance."
        ),
        key_factors=[
            "Sheet heating uniformity",
            "Mold temperature and design",
            "Forming pressure and speed",
            "Material melt strength",
            "Cooling rate",
            "Material thickness"
        ],
        primary_authority=[
            "Strong, A. B., Plastics: Materials and Processing, Pearson, 2006",
            "Rosato, D. V., Rosato, D. V., Injection Molding Handbook, Springer, 2000"
        ],
        burden_holder="Process engineer or polymer technologist",
        adversary_position=(
            "Claims thermoforming produces inconsistent parts with poor mechanical properties."
        ),
        counter_arguments=[
            "Optimized heating and forming parameters improve uniformity.",
            "Material selection enhances formability and strength.",
            "Process monitoring reduces defects."
        ],
        resolution_strategy=(
            "Implement precise temperature control and mold design to achieve high-quality thermoformed parts."
        ),
        entity_scope="Thermoforming polymer sheet processing",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Strong (2006), Rosato (2000)"
    ),
    DoctrineBlock(
        topic="Polymer Composites: Damage and Failure Mechanisms",
        keywords=[
            "composite damage", "matrix cracking", "fiber breakage",
            "delamination", "fatigue", "impact resistance", "fracture toughness",
            "environmental effects", "non-destructive evaluation", "failure analysis"
        ],
        conclusion_template=(
            "Damage and failure in polymer composites arise from matrix cracking, fiber breakage, delamination, and environmental degradation, affecting structural integrity."
        ),
        reasoning_framework=(
            "Polymer composites fail through multiple mechanisms including matrix cracking due to stress concentration, fiber breakage under load, and delamination at interfaces. "
            "Fatigue loading induces progressive damage accumulation. Impact events cause localized damage reducing residual strength. Environmental factors such as moisture and temperature accelerate degradation. "
            "Non-destructive evaluation techniques (ultrasound, X-ray tomography) detect internal damage. Failure analysis guides design improvements and maintenance strategies."
        ),
        key_factors=[
            "Load type and magnitude",
            "Fiber and matrix properties",
            "Interface strength",
            "Environmental exposure",
            "Manufacturing defects",
            "Inspection methods"
        ],
        primary_authority=[
            "Mallick, P. K., Fiber-Reinforced Composites, CRC Press, 2007",
            "Hull, D., Clyne, T. W., An Introduction to Composite Materials, Cambridge University Press, 1996"
        ],
        burden_holder="Composite materials engineer or failure analyst",
        adversary_position=(
            "Suggests composites are prone to unpredictable failure limiting their use."
        ),
        counter_arguments=[
            "Understanding damage mechanisms enables design for durability.",
            "Quality control and inspection reduce defects.",
            "Material and interface optimization improve failure resistance."
        ],
        resolution_strategy=(
            "Integrate damage modeling, material selection, and inspection to enhance composite reliability."
        ),
        entity_scope="Polymer composite damage and failure",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Mallick (2007), Hull & Clyne (1996)"
    ),
    DoctrineBlock(
        topic="Polymer Blends: Reactive Compatibilization",
        keywords=[
            "reactive compatibilization", "polymer blends", "in situ grafting",
            "interface modification", "functional groups", "copolymer formation",
            "morphology stabilization", "mechanical properties", "processing"
        ],
        conclusion_template=(
            "Reactive compatibilization modifies polymer blend interfaces in situ via chemical reactions, improving morphology and mechanical properties."
        ),
        reasoning_framework=(
            "Reactive compatibilization involves chemical reactions between functional groups on different polymers during melt processing, forming graft or block copolymers at interfaces. "
            "This in situ formation of compatibilizers reduces interfacial tension and stabilizes morphology. Functional groups such as anhydrides, epoxides, or isocyanates react with complementary groups on blend components. "
            "Processing conditions influence reaction extent and compatibilizer distribution. Enhanced interfacial adhesion improves mechanical properties such as impact strength and elongation."
        ),
        key_factors=[
            "Functional group availability and reactivity",
            "Processing temperature and time",
            "Polymer blend composition",
            "Compatibilizer concentration",
            "Morphology control",
            "Mechanical testing"
        ],
        primary_authority=[
            "Paul, D. R., Polymer Blends, Wiley, 2000",
            "Utracki, L. A., Polymer Blends Handbook, Springer, 2002"
        ],
        burden_holder="Polymer formulator or process engineer",
        adversary_position=(
            "Claims reactive compatibilization leads to uncontrolled reactions and property variability."
        ),
        counter_arguments=[
            "Controlled functionalization and processing yield reproducible results.",
            "Characterization confirms compatibilizer formation and morphology.",
            "Mechanical testing validates property improvements."
        ],
        resolution_strategy=(
            "Optimize functional group chemistry and processing to achieve consistent compatibilization."
        ),
        entity_scope="Reactive compatibilization in polymer blends",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Paul (2000), Utracki (2002)"
    ),
    DoctrineBlock(
        topic="Biopolymers: Polylactic Acid (PLA) Properties and Applications",
        keywords=[
            "polylactic acid", "PLA", "biopolymer", "biodegradable",
            "mechanical properties", "thermal properties", "processing",
            "applications", "compostability", "environmental impact"
        ],
        conclusion_template=(
            "Polylactic acid (PLA) is a biodegradable biopolymer with favorable mechanical and thermal properties suitable for packaging and biomedical applications."
        ),
        reasoning_framework=(
            "PLA is synthesized via ring-opening polymerization of lactide derived from renewable resources. It exhibits good tensile strength and modulus but relatively low thermal stability and impact resistance. "
            "Processing methods include extrusion, injection molding, and 3D printing. PLA biodegrades under industrial composting conditions via hydrolysis and microbial assimilation. Applications span packaging, disposable items, and medical devices. "
            "Material modifications such as copolymerization and blending improve properties and degradation rates. Environmental benefits include reduced fossil fuel dependence and lower carbon footprint."
        ),
        key_factors=[
            "Molecular weight and crystallinity",
            "Processing conditions",
            "Additives and plasticizers",
            "Degradation environment",
            "Mechanical and thermal requirements",
            "End-of-life management"
        ],
        primary_authority=[
            "Auras, R., et al., Polylactic Acid: Synthesis, Properties, Processing, and Applications, Wiley, 2010",
            "Drumright, R. E., Gruber, P. R., Henton, D. E., Adv. Mater., 2000"
        ],
        burden_holder="Polymer scientist or product developer",
        adversary_position=(
            "Claims PLA lacks sufficient performance for broad applications."
        ),
        counter_arguments=[
            "Material modifications enhance PLA properties.",
            "Processing optimization improves performance.",
            "Environmental benefits outweigh limitations."
        ],
        resolution_strategy=(
            "Tailor PLA formulations and processing for targeted applications and validate performance."
        ),
        entity_scope="PLA biopolymer properties and applications",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Auras et al. (2010), Drumright et al. (2000)"
    ),
    DoctrineBlock(
        topic="Oilfield Polymers: Shear Stability",
        keywords=[
            "shear stability", "polymer degradation", "mechanical shear",
            "molecular weight reduction", "viscosity loss", "reservoir conditions",
            "polyacrylamide", "biopolymers", "stabilizers"
        ],
        conclusion_template=(
            "Shear stability of oilfield polymers is critical to maintaining viscosity and performance under high shear conditions in reservoirs and surface equipment."
        ),
        reasoning_framework=(
            "Polymers used in enhanced oil recovery and drilling fluids experience high shear rates that can cause mechanical degradation and molecular weight reduction. "
            "Shear-induced chain scission reduces solution viscosity, impairing performance. Polymer structure, molecular weight, and additives influence shear resistance. "
            "Biopolymers often exhibit better shear stability due to branched structures. Stabilizers and process optimization mitigate shear degradation. Laboratory tests simulate field shear conditions to evaluate polymer stability."
        ),
        key_factors=[
            "Polymer molecular weight and architecture",
            "Shear rate and duration",
            "Reservoir temperature and salinity",
            "Additives and stabilizers",
            "Polymer concentration",
            "Testing protocols"
        ],
        primary_authority=[
            "Lake, L. W., Enhanced Oil Recovery, Prentice Hall, 1989",
            "Sheng, J. J., Modern Chemical Enhanced Oil Recovery, Gulf Professional Publishing, 2011"
        ],
        burden_holder="Petroleum engineer or polymer chemist",
        adversary_position=(
            "Claims polymers degrade too rapidly under shear to be effective."
        ),
        counter_arguments=[
            "Shear stable polymers and additives improve longevity.",
            "Field data supports polymer efficacy.",
            "Testing protocols guide formulation improvements."
        ],
        resolution_strategy=(
            "Develop shear stable polymers and validate under simulated and field conditions."
        ),
        entity_scope="Shear stability of oilfield polymers",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Lake (1989), Sheng (2011)"
    ),
    DoctrineBlock(
        topic="Polymer Composites: Fiber Surface Treatment",
        keywords=[
            "fiber surface treatment", "coupling agents", "silane",
            "interface adhesion", "composite performance", "fiber modification",
            "surface energy", "chemical bonding", "mechanical interlocking"
        ],
        conclusion_template=(
            "Fiber surface treatments enhance interfacial adhesion in polymer composites by improving chemical bonding and mechanical interlocking."
        ),
        reasoning_framework=(
            "Surface treatments such as silane coupling agents modify fiber surfaces to increase compatibility with polymer matrices. Treatments reduce surface energy mismatch and introduce reactive groups that form covalent bonds with the matrix. "
            "Improved adhesion enhances load transfer, mechanical properties, and durability. Treatment methods include chemical grafting, plasma treatment, and sizing application. Optimizing treatment chemistry and process conditions is essential for performance."
        ),
        key_factors=[
            "Fiber type and surface chemistry",
            "Coupling agent chemistry",
            "Treatment method and conditions",
            "Matrix compatibility",
            "Processing parameters",
            "Environmental exposure"
        ],
        primary_authority=[
            "Mallick, P. K., Fiber-Reinforced Composites, CRC Press, 2007",
            "Hull, D., Clyne, T. W., An Introduction to Composite Materials, Cambridge University Press, 1996"
        ],
        burden_holder="Composite materials engineer or polymer scientist",
        adversary_position=(
            "Claims surface treatments add cost without significant performance gains."
        ),
        counter_arguments=[
            "Surface treatments demonstrably improve mechanical properties and durability.",
            "Cost-benefit analyses support treatment application in high-performance composites.",
            "Processing optimization integrates treatments efficiently."
        ],
        resolution_strategy=(
            "Apply appropriate surface treatments tailored to fiber and matrix systems to maximize composite performance."
        ),
        entity_scope="Fiber surface treatment in polymer composites",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Mallick (2007), Hull & Clyne (1996)"
    ),
    DoctrineBlock(
        topic="Polymer Rheology: Shear Thinning Behavior",
        keywords=[
            "shear thinning", "non-Newtonian flow", "polymer melts",
            "viscosity", "shear rate", "molecular alignment", "processing",
            "flow behavior", "rheological models"
        ],
        conclusion_template=(
            "Polymer melts exhibit shear thinning, where viscosity decreases with increasing shear rate due to molecular alignment and disentanglement."
        ),
        reasoning_framework=(
            "Shear thinning behavior arises from the alignment of polymer chains in the direction of flow, reducing entanglements and resistance to deformation. "
            "This non-Newtonian flow characteristic facilitates processing methods such as extrusion and injection molding by lowering viscosity at high shear rates. "
            "Rheological models like the Carreau or Cross models describe shear thinning quantitatively. Molecular weight and branching influence the degree of shear thinning."
        ),
        key_factors=[
            "Molecular weight and distribution",
            "Shear rate and temperature",
            "Polymer architecture",
            "Branching and entanglements",
            "Rheological model parameters"
        ],
        primary_authority=[
            "Macosko, C. W., Rheology: Principles, Measurements, and Applications, Wiley-VCH, 1994",
            "Bird, R. B., Armstrong, R. C., Hassager, O., Dynamics of Polymeric Liquids, Wiley, 1987"
        ],
        burden_holder="Polymer rheologist or process engineer",
        adversary_position=(
            "Claims shear thinning complicates processing control and modeling."
        ),
        counter_arguments=[
            "Rheological models accurately predict shear thinning behavior.",
            "Process control accounts for viscosity changes.",
            "Material design tailors shear thinning characteristics."
        ],
        resolution_strategy=(
            "Use rheological characterization and modeling to optimize processing parameters."
        ),
        entity_scope="Shear thinning in polymer melts",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Macosko (1994), Bird et al. (1987)"
    ),
    DoctrineBlock(
        topic="Polymer Processing: Injection Molding Defects",
        keywords=[
            "injection molding", "defects", "sink marks", "warpage",
            "voids", "weld lines", "flash", "processing parameters",
            "mold design", "material properties"
        ],