from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

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
        topic="Crystal Structure: Body-Centered Cubic (BCC)",
        keywords=["BCC", "crystal structure", "iron", "metals", "lattice"],
        conclusion_template="BCC metals exhibit lower ductility and higher hardness compared to FCC metals.",
        reasoning_framework="""
        The BCC crystal structure is characterized by atoms at each corner of the cube and a single atom at the center. This arrangement leads to a lower packing density (68%) compared to FCC (74%), resulting in fewer slip systems. The limited slip systems restrict dislocation movement, making BCC metals generally harder and less ductile. Temperature also affects BCC metals significantly; at low temperatures, the ductility decreases further due to the absence of close-packed planes. Examples include α-iron, chromium, and tungsten.
        """,
        key_factors=["Packing density", "Slip systems", "Temperature sensitivity", "Dislocation movement"],
        primary_authority=["Callister, Materials Science and Engineering", "ASM Handbook"],
        burden_holder="Proponent of BCC mechanical property claims",
        adversary_position="BCC metals can be made ductile through alloying or processing",
        counter_arguments=[
            "BCC metals can exhibit improved ductility at higher temperatures",
            "Alloying elements may increase slip systems"
        ],
        resolution_strategy="Evaluate mechanical properties under standardized conditions and compare with FCC metals.",
        entity_scope="Metals with BCC structure",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Callister, 10th Edition, Ch. 3"
    ),
    DoctrineBlock(
        topic="Crystal Structure: Face-Centered Cubic (FCC)",
        keywords=["FCC", "crystal structure", "aluminum", "copper", "ductility", "lattice"],
        conclusion_template="FCC metals are highly ductile and exhibit excellent formability due to multiple slip systems.",
        reasoning_framework="""
        The FCC structure features atoms at each corner and at the centers of all cube faces. With 12 slip systems, FCC metals allow for easy dislocation movement, resulting in high ductility and toughness. The close-packed nature (74% packing density) promotes efficient atomic bonding and deformation. FCC metals include aluminum, copper, gold, and nickel. Their mechanical properties are less sensitive to temperature changes compared to BCC metals, making them ideal for applications requiring extensive forming.
        """,
        key_factors=["Slip systems", "Packing density", "Dislocation movement", "Temperature insensitivity"],
        primary_authority=["Callister, Materials Science and Engineering", "ASM Handbook"],
        burden_holder="Proponent of FCC ductility claims",
        adversary_position="FCC metals can lose ductility under certain alloying or processing conditions",
        counter_arguments=[
            "Work hardening can reduce ductility",
            "Certain alloying elements may embrittle FCC metals"
        ],
        resolution_strategy="Assess mechanical properties after processing and alloying.",
        entity_scope="Metals with FCC structure",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Callister, 10th Edition, Ch. 3"
    ),
    DoctrineBlock(
        topic="Crystal Structure: Hexagonal Close-Packed (HCP)",
        keywords=["HCP", "crystal structure", "magnesium", "titanium", "lattice", "ductility"],
        conclusion_template="HCP metals generally exhibit lower ductility due to limited slip systems.",
        reasoning_framework="""
        The HCP structure consists of atoms arranged in hexagonal layers, with a packing density similar to FCC (74%). However, the slip systems are limited (typically 3-6), restricting dislocation movement and resulting in lower ductility compared to FCC metals. HCP metals like magnesium and titanium are prone to brittle fracture, especially at low temperatures. Alloying and processing can enhance ductility by activating additional slip systems.
        """,
        key_factors=["Slip systems", "Packing density", "Dislocation movement", "Temperature effects"],
        primary_authority=["Callister, Materials Science and Engineering", "ASM Handbook"],
        burden_holder="Proponent of HCP ductility claims",
        adversary_position="HCP metals can be made ductile through alloying or texture control",
        counter_arguments=[
            "Texture control during processing can improve ductility",
            "Certain alloying elements activate more slip systems"
        ],
        resolution_strategy="Analyze mechanical properties post-processing and alloying.",
        entity_scope="Metals with HCP structure",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Callister, 10th Edition, Ch. 3"
    ),
    DoctrineBlock(
        topic="Phase Diagrams: Binary Eutectic Systems",
        keywords=["phase diagram", "binary", "eutectic", "solidification", "microstructure"],
        conclusion_template="Binary eutectic systems exhibit a distinct eutectic point where two phases solidify simultaneously.",
        reasoning_framework="""
        In binary eutectic systems, the phase diagram displays a eutectic point at which the liquid transforms into two solid phases at a specific composition and temperature. The eutectic reaction (L → α + β) is characterized by a unique microstructure of alternating lamellae or rods. The eutectic composition and temperature are determined experimentally and are critical for alloy design. Eutectic alloys often have improved mechanical properties due to fine microstructures.
        """,
        key_factors=["Eutectic point", "Phase boundaries", "Microstructure", "Solidification behavior"],
        primary_authority=["ASM Handbook", "Phase Diagrams: Understanding the Basics"],
        burden_holder="Proponent of eutectic behavior claims",
        adversary_position="Eutectic microstructures can be altered by cooling rate or impurities",
        counter_arguments=[
            "Rapid cooling can suppress eutectic formation",
            "Impurities may shift eutectic composition"
        ],
        resolution_strategy="Experimental validation of phase diagram and microstructure.",
        entity_scope="Binary alloy systems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook, Vol. 3"
    ),
    DoctrineBlock(
        topic="Phase Diagrams: Ternary Systems",
        keywords=["phase diagram", "ternary", "three-component", "solidification", "microstructure"],
        conclusion_template="Ternary phase diagrams provide a comprehensive view of phase equilibria in three-component systems.",
        reasoning_framework="""
        Ternary phase diagrams represent the equilibrium between three components, typically displayed as triangular diagrams. These diagrams are essential for understanding complex alloy systems, predicting phase formation, and guiding alloy design. The interpretation requires knowledge of tie-lines, tie-triangles, and invariant reactions. Experimental determination is challenging due to the increased number of variables, but computational thermodynamics aids in accurate modeling.
        """,
        key_factors=["Tie-lines", "Tie-triangles", "Invariant reactions", "Phase equilibria"],
        primary_authority=["ASM Handbook", "Phase Diagrams: Understanding the Basics"],
        burden_holder="Proponent of ternary phase diagram claims",
        adversary_position="Ternary diagrams may not accurately reflect real alloy behavior",
        counter_arguments=[
            "Experimental errors can distort ternary diagrams",
            "Non-equilibrium solidification may alter predicted phases"
        ],
        resolution_strategy="Combine experimental and computational approaches for validation.",
        entity_scope="Ternary alloy systems",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook, Vol. 3"
    ),
    DoctrineBlock(
        topic="Diffusion: Fick's First Law",
        keywords=["diffusion", "Fick's First Law", "concentration gradient", "flux"],
        conclusion_template="Fick's First Law quantifies steady-state diffusion as proportional to the concentration gradient.",
        reasoning_framework="""
        Fick's First Law states that the diffusion flux is proportional to the negative concentration gradient: J = -D(dC/dx), where J is the flux, D is the diffusion coefficient, and dC/dx is the concentration gradient. This law applies to steady-state conditions and is fundamental in modeling mass transport in solids, liquids, and gases. The diffusion coefficient depends on temperature, material, and atomic structure.
        """,
        key_factors=["Diffusion coefficient", "Concentration gradient", "Steady-state conditions"],
        primary_authority=["Callister, Materials Science and Engineering", "Crank, The Mathematics of Diffusion"],
        burden_holder="Proponent of steady-state diffusion claims",
        adversary_position="Non-steady-state conditions invalidate Fick's First Law",
        counter_arguments=[
            "Fick's First Law does not apply to transient diffusion",
            "Diffusion coefficient may vary with concentration"
        ],
        resolution_strategy="Ensure steady-state conditions before application.",
        entity_scope="Solid, liquid, and gaseous materials",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Crank, The Mathematics of Diffusion"
    ),
    DoctrineBlock(
        topic="Diffusion: Fick's Second Law",
        keywords=["diffusion", "Fick's Second Law", "transient", "concentration profile"],
        conclusion_template="Fick's Second Law models non-steady-state diffusion and predicts concentration profiles over time.",
        reasoning_framework="""
        Fick's Second Law describes how concentration changes with time: dC/dt = D(d²C/dx²). This law is used to model transient diffusion processes, such as carburizing or decarburizing of steels. Solutions to Fick's Second Law require initial and boundary conditions and may involve error functions for simple cases. The diffusion coefficient may depend on concentration and temperature, affecting the solution.
        """,
        key_factors=["Diffusion coefficient", "Initial conditions", "Boundary conditions", "Transient diffusion"],
        primary_authority=["Callister, Materials Science and Engineering", "Crank, The Mathematics of Diffusion"],
        burden_holder="Proponent of transient diffusion claims",
        adversary_position="Complex geometries or variable diffusion coefficients complicate solutions",
        counter_arguments=[
            "Analytical solutions may not exist for complex cases",
            "Numerical methods may be required"
        ],
        resolution_strategy="Apply numerical methods for complex geometries and variable coefficients.",
        entity_scope="Solid, liquid, and gaseous materials",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Crank, The Mathematics of Diffusion"
    ),
    DoctrineBlock(
        topic="Mechanical Properties: Yield Strength",
        keywords=["mechanical properties", "yield strength", "stress", "plastic deformation"],
        conclusion_template="Yield strength defines the stress at which a material begins to plastically deform.",
        reasoning_framework="""
        Yield strength is a critical mechanical property indicating the onset of plastic deformation. It is determined from stress-strain curves, typically at a 0.2% offset for metals. Factors influencing yield strength include grain size, alloying, work hardening, and heat treatment. Yield strength is essential for engineering design, ensuring safety and performance under load.
        """,
        key_factors=["Stress-strain curve", "Grain size", "Alloying", "Heat treatment"],
        primary_authority=["Callister, Materials Science and Engineering", "ASM Handbook"],
        burden_holder="Proponent of yield strength claims",
        adversary_position="Yield strength may vary with processing and environmental conditions",
        counter_arguments=[
            "Environmental factors (temperature, corrosion) can reduce yield strength",
            "Processing history alters yield strength"
        ],
        resolution_strategy="Standardize testing conditions and report yield strength accordingly.",
        entity_scope="Metals, polymers, ceramics",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook, Vol. 2"
    ),
    DoctrineBlock(
        topic="Mechanical Properties: Tensile Strength",
        keywords=["mechanical properties", "tensile strength", "ultimate strength", "stress", "fracture"],
        conclusion_template="Tensile strength is the maximum stress a material can withstand before fracture.",
        reasoning_framework="""
        Tensile strength, also known as ultimate strength, is measured during tensile testing and represents the peak stress before necking and fracture. Influenced by composition, microstructure, and processing, tensile strength is a key parameter for material selection. It is distinct from yield strength, as it reflects the material's resistance to catastrophic failure.
        """,
        key_factors=["Stress-strain curve", "Composition", "Microstructure", "Processing"],
        primary_authority=["Callister, Materials Science and Engineering", "ASM Handbook"],
        burden_holder="Proponent of tensile strength claims",
        adversary_position="Tensile strength may be reduced by defects or environmental factors",
        counter_arguments=[
            "Defects (voids, inclusions) lower tensile strength",
            "High temperatures reduce tensile strength"
        ],
        resolution_strategy="Perform testing under controlled conditions and inspect for defects.",
        entity_scope="Metals, polymers, ceramics",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook, Vol. 2"
    ),
    DoctrineBlock(
        topic="Heat Treatment: Annealing",
        keywords=["heat treatment", "annealing", "recrystallization", "grain growth", "softening"],
        conclusion_template="Annealing restores ductility and reduces hardness through recrystallization and grain growth.",
        reasoning_framework="""
        Annealing involves heating a material to a specific temperature, holding, and cooling slowly. The process eliminates defects, relieves internal stresses, and promotes recrystallization, resulting in new, strain-free grains. Grain growth may occur if held at high temperatures, affecting mechanical properties. Annealing is used to improve ductility, reduce hardness, and prepare metals for further processing.
        """,
        key_factors=["Temperature", "Holding time", "Cooling rate", "Recrystallization"],
        primary_authority=["ASM Handbook", "Callister, Materials Science and Engineering"],
        burden_holder="Proponent of annealing benefits",
        adversary_position="Excessive grain growth can reduce mechanical properties",
        counter_arguments=[
            "Over-annealing leads to coarse grains and reduced strength",
            "Improper cooling may cause unwanted phases"
        ],
        resolution_strategy="Optimize annealing parameters for desired properties.",
        entity_scope="Metals and alloys",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook, Vol. 4"
    ),
    DoctrineBlock(
        topic="Heat Treatment: Quenching",
        keywords=["heat treatment", "quenching", "rapid cooling", "martensite", "hardness"],
        conclusion_template="Quenching increases hardness by transforming austenite to martensite through rapid cooling.",
        reasoning_framework="""
        Quenching involves heating a metal to a high temperature and rapidly cooling in water, oil, or air. The process traps carbon in solution, forming martensite—a hard, brittle phase. Quenching is essential in steel hardening, but may induce residual stresses and cracking. The choice of quenching medium affects cooling rate and final properties.
        """,
        key_factors=["Quenching medium", "Cooling rate", "Martensite formation", "Residual stresses"],
        primary_authority=["ASM Handbook", "Callister, Materials Science and Engineering"],
        burden_holder="Proponent of quenching effectiveness",
        adversary_position="Quenching can cause cracking and distortion",
        counter_arguments=[
            "Rapid cooling induces thermal stresses",
            "Quenching may lead to brittleness"
        ],
        resolution_strategy="Control cooling rate and follow with tempering to reduce brittleness.",
        entity_scope="Steels and alloys",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook, Vol. 4"
    ),
    DoctrineBlock(
        topic="Heat Treatment: Tempering",
        keywords=["heat treatment", "tempering", "martensite", "toughness", "ductility"],
        conclusion_template="Tempering reduces brittleness and increases toughness by decomposing martensite.",
        reasoning_framework="""
        Tempering follows quenching and involves heating to a moderate temperature to allow martensite decomposition. The process increases toughness and ductility while reducing hardness. Tempering parameters (temperature, time) are selected based on desired properties. Excessive tempering may reduce hardness below acceptable levels.
        """,
        key_factors=["Tempering temperature", "Time", "Martensite decomposition", "Toughness"],
        primary_authority=["ASM Handbook", "Callister, Materials Science and Engineering"],
        burden_holder="Proponent of tempering benefits",
        adversary_position="Over-tempering can reduce hardness excessively",
        counter_arguments=[
            "High tempering temperatures may soften steel too much",
            "Improper tempering may not relieve all stresses"
        ],
        resolution_strategy="Optimize tempering conditions for balanced properties.",
        entity_scope="Steels and alloys",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook, Vol. 4"
    ),
    DoctrineBlock(
        topic="Corrosion: Galvanic",
        keywords=["corrosion", "galvanic", "electrochemical", "anode", "cathode"],
        conclusion_template="Galvanic corrosion occurs when two dissimilar metals are electrically connected in an electrolyte.",
        reasoning_framework="""
        Galvanic corrosion is driven by differences in electrochemical potential between metals. The less noble metal acts as the anode and corrodes preferentially, while the more noble metal acts as the cathode. Factors affecting galvanic corrosion include electrolyte composition, area ratio, and electrical connectivity. Prevention strategies include material selection, insulation, and protective coatings.
        """,
        key_factors=["Electrochemical potential", "Electrolyte", "Area ratio", "Electrical connectivity"],
        primary_authority=["ASM Handbook", "Fontana, Corrosion Engineering"],
        burden_holder="Proponent of galvanic corrosion risk",
        adversary_position="Galvanic corrosion can be mitigated by design",
        counter_arguments=[
            "Insulating materials prevents electrical connection",
            "Area ratio optimization reduces corrosion rate"
        ],
        resolution_strategy="Design to minimize galvanic couples and apply protective measures.",
        entity_scope="Metallic structures",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Fontana, Corrosion Engineering"
    ),
    DoctrineBlock(
        topic="Corrosion: Pitting",
        keywords=["corrosion", "pitting", "localized", "chloride", "passivity"],
        conclusion_template="Pitting corrosion is a localized attack resulting in small holes or pits, often initiated by chloride ions.",
        reasoning_framework="""
        Pitting corrosion breaks down passive films on metals, leading to highly localized attack. Chloride ions are particularly aggressive in initiating pits. Once a pit forms, the local environment becomes acidic and accelerates corrosion. Pitting is dangerous due to its unpredictability and potential for catastrophic failure. Prevention includes alloying for passivity and controlling environmental exposure.
        """,
        key_factors=["Passive film", "Chloride ions", "Local acidity", "Pit initiation"],
        primary_authority=["ASM Handbook", "Fontana, Corrosion Engineering"],
        burden_holder="Proponent of pitting corrosion risk",
        adversary_position="Pitting can be prevented by proper alloy selection",
        counter_arguments=[
            "High chromium alloys resist pitting",
            "Environmental control reduces risk"
        ],
        resolution_strategy="Select alloys with high resistance and monitor environments.",
        entity_scope="Metallic structures",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Fontana, Corrosion Engineering"
    ),
    DoctrineBlock(
        topic="Corrosion: Crevice",
        keywords=["corrosion", "crevice", "localized", "oxygen depletion", "passivity"],
        conclusion_template="Crevice corrosion occurs in confined spaces where oxygen depletion breaks down passivity.",
        reasoning_framework="""
        Crevice corrosion is initiated in gaps or crevices where stagnant conditions cause oxygen depletion. The lack of oxygen prevents the formation of protective passive films, resulting in localized attack. The process is self-accelerating as corrosion products further restrict oxygen access. Prevention includes design to eliminate crevices and use of resistant alloys.
        """,
        key_factors=["Oxygen depletion", "Crevice geometry", "Passive film", "Stagnant conditions"],
        primary_authority=["ASM Handbook", "Fontana, Corrosion Engineering"],
        burden_holder="Proponent of crevice corrosion risk",
        adversary_position="Crevice corrosion can be minimized by design",
        counter_arguments=[
            "Eliminating crevices prevents corrosion",
            "Resistant alloys reduce susceptibility"
        ],
        resolution_strategy="Design to avoid crevices and select appropriate materials.",
        entity_scope="Metallic structures",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Fontana, Corrosion Engineering"
    ),
    DoctrineBlock(
        topic="Corrosion: Stress",
        keywords=["corrosion", "stress corrosion cracking", "SCC", "tensile stress", "environment"],
        conclusion_template="Stress corrosion cracking (SCC) occurs when tensile stress and a corrosive environment act together.",
        reasoning_framework="""
        SCC is a synergistic effect where tensile stress and a specific corrosive environment cause brittle fracture. Common in high-strength alloys exposed to chloride or caustic environments. Crack initiation and propagation are accelerated by stress concentration and environmental factors. Prevention includes stress relief, environmental control, and alloy selection.
        """,
        key_factors=["Tensile stress", "Corrosive environment", "Crack initiation", "Alloy susceptibility"],
        primary_authority=["ASM Handbook", "Fontana, Corrosion Engineering"],
        burden_holder="Proponent of SCC risk",
        adversary_position="SCC can be prevented by proper stress management",
        counter_arguments=[
            "Stress relief reduces SCC risk",
            "Environmental control prevents SCC"
        ],
        resolution_strategy="Combine stress management and environmental control.",
        entity_scope="Metallic structures",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Fontana, Corrosion Engineering"
    ),
    DoctrineBlock(
        topic="Polymers: Chain Architecture",
        keywords=["polymers", "chain architecture", "linear", "branched", "crosslinked"],
        conclusion_template="Polymer chain architecture determines mechanical properties and processing behavior.",
        reasoning_framework="""
        Polymers can be linear, branched, or crosslinked. Linear polymers are flexible and easy to process, branched polymers have altered packing and properties, and crosslinked polymers are rigid and thermoset. Architecture affects crystallinity, melting point, and mechanical strength. Selection depends on application requirements.
        """,
        key_factors=["Chain structure", "Crystallinity", "Mechanical properties", "Processing"],
        primary_authority=["Callister, Materials Science and Engineering", "ASM Handbook"],
        burden_holder="Proponent of architecture-property relationship",
        adversary_position="Other factors (additives, fillers) affect properties",
        counter_arguments=[
            "Additives may dominate mechanical behavior",
            "Processing conditions alter properties"
        ],
        resolution_strategy="Isolate architecture effects through controlled experiments.",
        entity_scope="Polymers and plastics",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Callister, 10th Edition, Ch. 14"
    ),
    DoctrineBlock(
        topic="Polymers: Crystallinity",
        keywords=["polymers", "crystallinity", "amorphous", "mechanical properties", "thermal properties"],
        conclusion_template="Degree of crystallinity in polymers affects mechanical and thermal properties.",
        reasoning_framework="""
        Crystallinity refers to the ordered arrangement of polymer chains. High crystallinity increases strength, stiffness, and melting point, while amorphous regions provide flexibility and impact resistance. Processing conditions, chain architecture, and cooling rate influence crystallinity. Applications require tailored crystallinity for desired performance.
        """,
        key_factors=["Crystallinity", "Chain architecture", "Processing", "Mechanical properties"],
        primary_authority=["Callister, Materials Science and Engineering", "ASM Handbook"],
        burden_holder="Proponent of crystallinity-property relationship",
        adversary_position="Additives and fillers may override crystallinity effects",
        counter_arguments=[
            "Fillers can dominate mechanical properties",
            "Rapid cooling may prevent crystallinity"
        ],
        resolution_strategy="Control processing and isolate crystallinity effects.",
        entity_scope="Polymers and plastics",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Callister, 10th Edition, Ch. 14"
    ),
    DoctrineBlock(
        topic="Crystal Structure: Grain Boundaries",
        keywords=["grain boundary", "crystal structure", "defects", "diffusion", "mechanical properties"],
        conclusion_template="Grain boundaries act as barriers to dislocation movement and sites for diffusion.",
        reasoning_framework="""
        Grain boundaries are interfaces between crystals of different orientations. They impede dislocation movement, increasing strength (Hall-Petch effect), but also serve as fast diffusion paths and sites for corrosion or precipitation. Grain boundary engineering enhances properties by controlling grain size and boundary character.
        """,
        key_factors=["Grain size", "Boundary character", "Dislocation movement", "Diffusion"],
        primary_authority=["Callister, Materials Science and Engineering", "ASM Handbook"],
        burden_holder="Proponent of grain boundary effects",
        adversary_position="Excessive grain boundaries may reduce toughness",
        counter_arguments=[
            "Small grains increase strength but reduce toughness",
            "Grain boundaries may be sites for crack initiation"
        ],
        resolution_strategy="Optimize grain size for balanced properties.",
        entity_scope="Polycrystalline materials",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Callister, 10th Edition, Ch. 4"
    ),
    DoctrineBlock(
        topic="Phase Diagrams: Peritectic Reaction",
        keywords=["phase diagram", "peritectic", "solidification", "microstructure"],
        conclusion_template="Peritectic reactions involve the transformation of a liquid and one solid phase into a second solid phase.",
        reasoning_framework="""
        Peritectic reactions occur at a specific composition and temperature, where a liquid and a solid phase react to form a new solid phase (L + α → β). The resulting microstructure depends on cooling rate and composition. Peritectic alloys may exhibit complex solidification behavior and require careful control during processing.
        """,
        key_factors=["Peritectic point", "Phase boundaries", "Microstructure", "Solidification behavior"],
        primary_authority=["ASM Handbook", "Phase Diagrams: Understanding the Basics"],
        burden_holder="Proponent of peritectic behavior claims",
        adversary_position="Peritectic microstructures can be altered by cooling rate or impurities",
        counter_arguments=[
            "Rapid cooling can suppress peritectic formation",
            "Impurities may shift peritectic composition"
        ],
        resolution_strategy="Experimental validation of phase diagram and microstructure.",
        entity_scope="Binary and ternary alloy systems",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook, Vol. 3"
    ),
    DoctrineBlock(
        topic="Diffusion: Interstitial Diffusion",
        keywords=["diffusion", "interstitial", "carbon in iron", "atomic movement"],
        conclusion_template="Interstitial diffusion involves small atoms moving through spaces between host atoms.",
        reasoning_framework="""
        Interstitial diffusion is faster than substitutional diffusion due to smaller atom size and lower activation energy. Carbon diffusing in iron is a classic example, critical for steel processing. The rate depends on temperature, host lattice structure, and concentration gradient. Interstitial diffusion is modeled using Fick's laws.
        """,
        key_factors=["Atom size", "Activation energy", "Lattice structure", "Temperature"],
        primary_authority=["Callister, Materials Science and Engineering", "Crank, The Mathematics of Diffusion"],
        burden_holder="Proponent of interstitial diffusion claims",
        adversary_position="Interstitial diffusion may be limited by lattice distortions",
        counter_arguments=[
            "Lattice distortions can impede diffusion",
            "High concentrations may block diffusion paths"
        ],
        resolution_strategy="Control concentration and temperature for optimal diffusion.",
        entity_scope="Metals and alloys",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Callister, 10th Edition, Ch. 5"
    ),
    DoctrineBlock(
        topic="Diffusion: Substitutional Diffusion",
        keywords=["diffusion", "substitutional", "atomic movement", "alloying"],
        conclusion_template="Substitutional diffusion involves atoms exchanging positions with host atoms, typically slower than interstitial diffusion.",
        reasoning_framework="""
        Substitutional diffusion requires atoms to exchange places with host atoms, involving higher activation energy. The rate is influenced by atom size, lattice structure, and temperature. Alloying elements diffuse by substitutional mechanisms, affecting microstructure and properties. Fick's laws apply, but diffusion coefficients are lower than for interstitial diffusion.
        """,
        key_factors=["Atom size", "Activation energy", "Lattice structure", "Temperature"],
        primary_authority=["Callister, Materials Science and Engineering", "Crank, The Mathematics of Diffusion"],
        burden_holder="Proponent of substitutional diffusion claims",
        adversary_position="Substitutional diffusion may be enhanced by defects",
        counter_arguments=[
            "Vacancies and defects increase diffusion rate",
            "High temperatures accelerate diffusion"
        ],
        resolution_strategy="Control defect concentration and temperature for desired diffusion.",
        entity_scope="Metals and alloys",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Callister, 10th Edition, Ch. 5"
    ),
    DoctrineBlock(
        topic="Mechanical Properties: Hardness",
        keywords=["mechanical properties", "hardness", "indentation", "resistance"],
        conclusion_template="Hardness measures a material's resistance to indentation and scratching.",
        reasoning_framework="""
        Hardness is assessed using tests such as Rockwell, Brinell, and Vickers. It correlates with strength and wear resistance but does not directly indicate toughness. Factors influencing hardness include microstructure, composition, and heat treatment. Hardness is used for quality control and material selection.
        """,
        key_factors=["Testing method", "Microstructure", "Composition", "Heat treatment"],
        primary_authority=["ASM Handbook", "Callister, Materials Science and Engineering"],
        burden_holder="Proponent of hardness claims",
        adversary_position="Hardness may not correlate with other properties",
        counter_arguments=[
            "High hardness may reduce toughness",
            "Surface treatments can alter hardness"
        ],
        resolution_strategy="Use multiple tests and correlate with other properties.",
        entity_scope="Metals, polymers, ceramics",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook, Vol. 2"
    ),
    DoctrineBlock(
        topic="Mechanical Properties: Toughness",
        keywords=["mechanical properties", "toughness", "fracture", "energy absorption"],
        conclusion_template="Toughness is the ability of a material to absorb energy before fracture.",
        reasoning_framework="""
        Toughness is measured by impact tests (Charpy, Izod) and reflects resistance to crack propagation. Influenced by microstructure, temperature, and processing. High toughness is essential for safety-critical applications. Trade-offs exist between toughness, strength, and hardness.
        """,
        key_factors=["Impact test", "Microstructure", "Temperature", "Processing"],
        primary_authority=["ASM Handbook", "Callister, Materials Science and Engineering"],
        burden_holder="Proponent of toughness claims",
        adversary_position="Toughness may decrease with increased strength or hardness",
        counter_arguments=[
            "High strength alloys may be brittle",
            "Low temperatures reduce toughness"
        ],
        resolution_strategy="Balance properties through alloy design and processing.",
        entity_scope="Metals, polymers, ceramics",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook, Vol. 2"
    ),
    DoctrineBlock(
        topic="Heat Treatment: Normalizing",
        keywords=["heat treatment", "normalizing", "grain refinement", "mechanical properties"],
        conclusion_template="Normalizing produces fine, uniform grains and improves mechanical properties.",
        reasoning_framework="""
        Normalizing involves heating above the critical temperature and air cooling. The process refines grain size, improves toughness, and homogenizes microstructure. Used for steels to enhance mechanical properties and prepare for further processing.
        """,
        key_factors=["Temperature", "Cooling rate", "Grain size", "Microstructure"],
        primary_authority=["ASM Handbook", "Callister, Materials Science and Engineering"],
        burden_holder="Proponent of normalizing benefits",
        adversary_position="Normalizing may not eliminate all defects",
        counter_arguments=[
            "Some defects persist after normalizing",
            "Air cooling may induce residual stresses"
        ],
        resolution_strategy="Combine normalizing with other treatments for optimal results.",
        entity_scope="Steels and alloys",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook, Vol. 4"
    ),
    DoctrineBlock(
        topic="Corrosion: Uniform",
        keywords=["corrosion", "uniform", "general", "electrochemical", "metal loss"],
        conclusion_template="Uniform corrosion results in even metal loss across the surface.",
        reasoning_framework="""
        Uniform corrosion is the most common form, occurring evenly over exposed surfaces. Driven by electrochemical reactions, it is predictable and manageable. Rate depends on environment, material, and protective measures. Prevention includes coatings and material selection.
        """,
        key_factors=["Electrochemical reaction", "Environment", "Material", "Coatings"],
        primary_authority=["ASM Handbook", "Fontana, Corrosion Engineering"],
        burden_holder="Proponent of uniform corrosion risk",
        adversary_position="Uniform corrosion can be controlled by protective measures",
        counter_arguments=[
            "Coatings prevent uniform corrosion",
            "Material selection reduces rate"
        ],
        resolution_strategy="Apply protective coatings and select resistant materials.",
        entity_scope="Metallic structures",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Fontana, Corrosion Engineering"
    ),
    DoctrineBlock(
        topic="Polymers: Glass Transition Temperature",
        keywords=["polymers", "glass transition", "Tg", "thermal properties", "mechanical properties"],
        conclusion_template="Glass transition temperature (Tg) marks the transition from rigid to rubbery behavior in polymers.",
        reasoning_framework="""
        Tg is the temperature at which amorphous polymers change from a glassy to a rubbery state. Below Tg, polymers are brittle; above Tg, they are flexible. Tg depends on chain architecture, additives, and processing. Applications require polymers with appropriate Tg for service conditions.
        """,
        key_factors=["Chain architecture", "Additives", "Processing", "Service temperature"],
        primary_authority=["Callister, Materials Science and Engineering", "ASM Handbook"],
        burden_holder="Proponent of Tg-property relationship",
        adversary_position="Additives may alter Tg significantly",
        counter_arguments=[
            "Plasticizers lower Tg",
            "Crosslinking raises Tg"
        ],
        resolution_strategy="Control additives and processing to tailor Tg.",
        entity_scope="Polymers and plastics",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Callister, 10th Edition, Ch. 14"
    ),
    DoctrineBlock(
        topic="Crystal Structure: Point Defects",
        keywords=["point defect", "vacancy", "interstitial", "substitutional", "crystal structure"],
        conclusion_template="Point defects alter material properties by disrupting atomic arrangement.",
        reasoning_framework="""
        Point defects include vacancies, interstitials, and substitutional atoms. They affect diffusion, electrical conductivity, and mechanical properties. Defect concentration depends on temperature and processing. Engineering defects can tailor material properties for specific applications.
        """,
        key_factors=["Defect type", "Concentration", "Temperature", "Processing"],
        primary_authority=["Callister, Materials Science and Engineering", "ASM Handbook"],
        burden_holder="Proponent of defect-property relationship",
        adversary_position="Other factors may dominate property changes",
        counter_arguments=[
            "Microstructure may override defect effects",
            "Defects may be annealed out"
        ],
        resolution_strategy="Control defect concentration and analyze property changes.",
        entity_scope="Crystalline materials",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Callister, 10th Edition, Ch. 4"
    ),
    DoctrineBlock(
        topic="Phase Diagrams: Solid Solution",
        keywords=["phase diagram", "solid solution", "alloying", "solubility", "microstructure"],
        conclusion_template="Solid solutions form when one element dissolves in another, creating a single-phase microstructure.",
        reasoning_framework="""
        Solid solutions are classified as substitutional or interstitial. The extent of solubility depends on atomic size, electronegativity, and crystal structure (Hume-Rothery rules). Solid solutions affect mechanical properties, corrosion resistance, and processing behavior. Phase diagrams indicate solubility limits and guide alloy design.
        """,
        key_factors=["Solubility", "Atomic size", "Electronegativity", "Crystal structure"],
        primary_authority=["ASM Handbook", "Phase Diagrams: Understanding the Basics"],
        burden_holder="Proponent of solid solution claims",
        adversary_position="Solubility may be limited by structure or impurities",
        counter_arguments=[
            "Impurities restrict solubility",
            "Non-equilibrium processing may prevent solid solution formation"
        ],
        resolution_strategy="Validate solubility experimentally and consult phase diagrams.",
        entity_scope="Alloy systems",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook, Vol. 3"
    ),
    DoctrineBlock(
        topic="Mechanical Properties: Fatigue",
        keywords=["mechanical properties", "fatigue", "cyclic loading", "crack initiation", "failure"],
        conclusion_template="Fatigue failure occurs under repeated cyclic loading, often below yield strength.",
        reasoning_framework="""
        Fatigue is characterized by crack initiation and propagation due to cyclic stress. The fatigue limit is the maximum stress a material can withstand for infinite cycles. Influenced by surface finish, microstructure, and environment. Prevention includes design for reduced stress concentration and surface treatments.
        """,
        key_factors=["Cyclic loading", "Surface finish", "Microstructure", "Environment"],
        primary_authority=["ASM Handbook", "Callister, Materials Science and Engineering"],
        burden_holder="Proponent of fatigue risk",
        adversary_position="Fatigue life can be extended by design and processing",
        counter_arguments=[
            "Surface treatments improve fatigue life",
            "Design reduces stress concentration"
        ],
        resolution_strategy="Optimize design and processing for fatigue resistance.",
        entity_scope="Metals, polymers, ceramics",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook, Vol. 2"
    ),
    DoctrineBlock(
        topic="Polymers: Degree of Polymerization",
        keywords=["polymers", "degree of polymerization", "molecular weight", "properties"],
        conclusion_template="Degree of polymerization determines molecular weight and influences mechanical properties.",
        reasoning_framework="""
        Degree of polymerization is the number of repeating units in a polymer chain. Higher degree increases molecular weight, strength, and viscosity. Processing and additives affect polymerization. Applications require polymers with tailored molecular weight for performance.
        """,
        key_factors=["Molecular weight", "Chain length", "Processing", "Additives"],
        primary_authority=["Callister, Materials Science and Engineering", "ASM Handbook"],
        burden_holder="Proponent of polymerization-property relationship",
        adversary_position="Other factors may dominate mechanical properties",
        counter_arguments=[
            "Additives may override polymerization effects",
            "Processing alters properties"
        ],
        resolution_strategy="Control polymerization and isolate effects experimentally.",
        entity_scope="Polymers and plastics",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Callister, 10th Edition, Ch. 14"
    ),
    DoctrineBlock(
        topic="Crystal Structure: Dislocations",
        keywords=["dislocation", "crystal structure", "defects", "mechanical properties"],
        conclusion_template="Dislocations enable plastic deformation and influence mechanical properties.",
        reasoning_framework="""
        Dislocations are line defects in crystals, allowing atoms to slip past each other. Their movement is responsible for plastic deformation. Dislocation density, type (edge, screw), and interactions affect strength, ductility, and work hardening. Controlling dislocations through processing tailors material properties.
        """,
        key_factors=["Dislocation type", "Density", "Movement", "Interactions"],
        primary_authority=["Callister, Materials Science and Engineering", "ASM Handbook"],
        burden_holder="Proponent of dislocation-property relationship",
        adversary_position="Other defects may dominate mechanical behavior",
        counter_arguments=[
            "Grain boundaries may override dislocation effects",
            "Dislocation movement may be impeded by impurities"
        ],
        resolution_strategy="Analyze defect interactions and optimize processing.",
        entity_scope="Crystalline materials",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Callister, 10th Edition, Ch. 4"
    ),
    DoctrineBlock(
        topic="Phase Diagrams: Eutectoid Reaction",
        keywords=["phase diagram", "eutectoid", "solid-state transformation", "microstructure"],
        conclusion_template="Eutectoid reactions involve the transformation of one solid phase into two new solid phases.",
        reasoning_framework="""
        Eutectoid reactions occur at a specific composition and temperature, where a solid phase transforms into two new solid phases (α → β + γ). In steels, the eutectoid reaction forms pearlite from austenite. Microstructure and properties depend on cooling rate and composition. Phase diagrams guide heat treatment and alloy design.
        """,
        key_factors=["Eutectoid point", "Phase boundaries", "Microstructure", "Solid-state transformation"],
        primary_authority=["ASM Handbook", "Phase Diagrams: Understanding the Basics"],
        burden_holder="Proponent of eutectoid behavior claims",
        adversary_position="Microstructure can be altered by cooling rate or impurities",
        counter_arguments=[
            "Rapid cooling may suppress eutectoid formation",
            "Impurities shift eutectoid composition"
        ],
        resolution_strategy="Validate microstructure experimentally and consult phase diagrams.",
        entity_scope="Steels and alloys",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook, Vol. 3"
    ),
    DoctrineBlock(
        topic="Mechanical Properties: Creep",
        keywords=["mechanical properties", "creep", "high temperature", "deformation", "time-dependent"],
        conclusion_template="Creep is time-dependent deformation under constant stress at elevated temperatures.",
        reasoning_framework="""
        Creep occurs in metals, polymers, and ceramics subjected to stress at high temperature. Characterized by primary, secondary, and tertiary stages. Influenced by temperature, stress, microstructure, and environment. Prevention includes alloy selection and design for reduced stress.
        """,
        key_factors=["Temperature", "Stress", "Microstructure", "Environment"],
        primary_authority=["ASM Handbook", "Callister, Materials Science and Engineering"],
        burden_holder="Proponent of creep risk",
        adversary_position="Creep can be minimized by alloy design and processing",
        counter_arguments=[
            "Alloying improves creep resistance",
            "Processing refines microstructure"
        ],
        resolution_strategy="Select alloys and optimize processing for creep resistance.",
        entity_scope="Metals, polymers, ceramics",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook, Vol. 2"
    ),
    DoctrineBlock(
        topic="Polymers: Thermoplastic vs Thermoset",
        keywords=["polymers", "thermoplastic", "thermoset", "processing", "properties"],
        conclusion_template="Thermoplastics can be remelted and reshaped, while thermosets are permanently crosslinked.",
        reasoning_framework="""
        Thermoplastics are linear or branched polymers that soften on heating and can be reshaped. Thermosets are crosslinked and do not melt; they decompose on heating. Properties and applications differ: thermoplastics are used for flexible, recyclable products, while thermosets are used for rigid, high-temperature applications.
        """,
        key_factors=["Chain architecture", "Crosslinking", "Processing", "Application"],
        primary_authority=["Callister, Materials Science and Engineering", "ASM Handbook"],
        burden_holder="Proponent of processing-property relationship",
        adversary_position="Additives may alter behavior",
        counter_arguments=[
            "Plasticizers may make thermosets flexible",
            "Fillers change processing characteristics"
        ],
        resolution_strategy="Control additives and processing for desired behavior.",
        entity_scope="Polymers and plastics",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Callister, 10th Edition, Ch. 14"
    ),
    DoctrineBlock(
        topic="Crystal Structure: Twin Boundaries",
        keywords=["twin boundary", "crystal structure", "defects", "mechanical properties"],
        conclusion_template="Twin boundaries are mirror planes in crystals that affect mechanical properties.",
        reasoning_framework="""
        Twin boundaries are special grain boundaries where the crystal orientation is mirrored. They can strengthen materials by impeding dislocation movement and are formed during deformation or annealing. Twin boundaries are important in metals like brass and stainless steel.
        """,
        key_factors=["Twin formation", "Dislocation movement", "Mechanical properties", "Processing"],
        primary_authority=["Callister, Materials Science and Engineering", "ASM Handbook"],
        burden_holder="Proponent of twin boundary effects",
        adversary_position="Twin boundaries may reduce ductility",
        counter_arguments=[
            "Excessive twins can embrittle materials",
            "Twin boundaries may be sites for crack initiation"
        ],
        resolution_strategy="Control twin formation through processing.",
        entity_scope="Crystalline materials",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Callister, 10th Edition, Ch. 4"
    ),
    DoctrineBlock(
        topic="Phase Diagrams: Lever Rule",
        keywords=["phase diagram", "lever rule", "composition", "microstructure"],
        conclusion_template="The lever rule calculates phase fractions in two-phase regions of phase diagrams.",
        reasoning_framework="""
        The lever rule is a graphical method for determining the proportion of phases in a two-phase region. It uses the tie-line and the overall composition to calculate fractions. Essential for alloy design and predicting microstructure after solidification.
        """,
        key_factors=["Tie-line", "Composition", "Phase fraction", "Microstructure"],
        primary_authority=["ASM Handbook", "Phase Diagrams: Understanding the Basics"],
        burden_holder="Proponent of lever rule application",
        adversary_position="Non-equilibrium conditions may invalidate lever rule",
        counter_arguments=[
            "Rapid cooling prevents equilibrium",
            "Impurities shift phase boundaries"
        ],
        resolution_strategy="Validate microstructure experimentally and consult phase diagrams.",
        entity_scope="Alloy systems",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook, Vol. 3"
    ),
    DoctrineBlock(
        topic="Mechanical Properties: Impact Toughness",
        keywords=["mechanical properties", "impact toughness", "Charpy test", "energy absorption"],
        conclusion_template="Impact toughness measures energy absorbed during fracture under high strain rate.",
        reasoning_framework="""
        Impact toughness is assessed by Charpy or Izod tests, indicating resistance to sudden fracture. Influenced by microstructure, temperature, and notch sensitivity. High impact toughness is essential for safety-critical applications. Alloying and heat treatment can improve toughness.
        """,
        key_factors=["Impact test", "Microstructure", "Temperature", "Notch sensitivity"],
        primary_authority=["ASM Handbook", "Callister, Materials Science and Engineering"],
        burden_holder="Proponent of impact toughness claims",
        adversary_position="Impact toughness may decrease with increased strength",
        counter_arguments=[
            "High strength alloys may be brittle",
            "Low temperatures reduce impact toughness"
        ],
        resolution_strategy="Balance properties through alloy design and processing.",
        entity_scope="Metals, polymers, ceramics",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook, Vol. 2"
    ),
    DoctrineBlock(
        topic="Corrosion: Intergranular",
        keywords=["corrosion", "intergranular", "grain boundary", "sensitization", "stainless steel"],
        conclusion_template="Intergranular corrosion occurs along grain boundaries, often due to sensitization.",
        reasoning_framework="""
        Intergranular corrosion is caused by precipitation of chromium carbides at grain boundaries, depleting chromium and breaking down passivity. Common in stainless steels exposed to high temperatures. Prevention includes alloying with stabilizers and controlling heat treatment.
        """,
        key_factors=["Grain boundary", "Chromium depletion", "Sensitization", "Heat treatment"],
        primary_authority=["ASM Handbook", "Fontana, Corrosion Engineering"],
        burden_holder="Proponent of intergranular corrosion risk",
        adversary_position="Proper heat treatment prevents intergranular corrosion",
        counter_arguments=[
            "Stabilizers prevent carbide formation",
            "Controlled cooling avoids sensitization"
        ],
        resolution_strategy="Apply appropriate heat treatment and alloying.",
        entity_scope="Stainless steels",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Fontana, Corrosion Engineering"
    ),
    DoctrineBlock(
        topic="Polymers: Copolymerization",
        keywords=["polymers", "copolymerization", "properties", "processing"],
        conclusion_template="Copolymerization combines different monomers to tailor polymer properties.",
        reasoning_framework="""
        Copolymerization produces polymers with blocks, random, or alternating arrangements of monomers. Properties such as strength, flexibility, and chemical resistance are tailored by monomer selection and arrangement. Used in engineering plastics and specialty applications.
        """,
        key_factors=["Monomer selection", "Arrangement", "Properties", "Processing"],
        primary_authority=["Callister, Materials Science and Engineering", "ASM Handbook"],
        burden_holder="Proponent of copolymerization-property relationship",
        adversary_position="Additives may override copolymerization effects",
        counter_arguments=[
            "Fillers dominate mechanical properties",
            "Processing alters copolymer behavior"
        ],
        resolution_strategy="Control monomer selection and processing for desired properties.",
        entity_scope="Polymers and plastics",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Callister, 10th Edition, Ch. 14"
    ),
    DoctrineBlock(
        topic="Crystal Structure: Stacking Faults",
        keywords=["stacking fault", "crystal structure", "defects", "mechanical properties"],
        conclusion_template="Stacking faults disrupt the regular stacking sequence of crystal planes and affect mechanical properties.",
        reasoning_framework="""
        Stacking faults are planar defects in crystals, common in FCC and HCP structures. They influence dislocation movement, work hardening, and mechanical properties. Stacking fault energy determines ease of dislocation movement and twinning. Engineering stacking faults can tailor properties for specific applications.
        """,
        key_factors=["Stacking fault energy", "Dislocation movement", "Mechanical properties", "Processing"],
        primary_authority=["Callister, Materials Science and Engineering", "ASM Handbook"],
        burden_holder="Proponent of stacking fault effects",
        adversary_position="Other defects may dominate mechanical behavior",
        counter_arguments=[
            "Grain boundaries may override stacking fault effects",
            "Stacking faults may be annealed out"
        ],
        resolution_strategy="Control stacking fault formation through processing.",
        entity_scope="Crystalline materials",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Callister, 10th Edition, Ch. 4"
    ),
    DoctrineBlock(
        topic="Phase Diagrams: Solvus Line",
        keywords=["phase diagram", "solvus line", "solubility", "precipitation", "microstructure"],
        conclusion_template="The solvus line indicates the limit of solubility and onset of precipitation in alloys.",
        reasoning_framework="""
        The solvus line separates single-phase and two-phase regions in phase diagrams. Crossing the solvus line during cooling triggers precipitation of a second phase, affecting microstructure and properties. Control of cooling rate and composition is essential for desired alloy performance.
        """,
        key_factors=["Solubility", "Precipitation", "Microstructure", "Composition"],
        primary_authority=["ASM Handbook", "Phase Diagrams: Understanding the Basics"],
        burden_holder="Proponent of solvus line application",
        adversary_position="Non-equilibrium conditions may alter precipitation behavior",
        counter_arguments=[
            "Rapid cooling prevents equilibrium precipitation",
            "Impurities shift solvus line"
        ],
        resolution_strategy="Validate microstructure experimentally and consult phase diagrams.",
        entity_scope="Alloy systems",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook, Vol. 3"
    ),
    DoctrineBlock(
        topic="Mechanical Properties: Elastic Modulus",
        keywords=["mechanical properties", "elastic modulus", "Young's modulus", "stiffness"],
        conclusion_template="Elastic modulus measures material stiffness and resistance to elastic deformation.",
        reasoning_framework="""
        Elastic modulus is determined from the slope of the stress-strain curve in the elastic region. Influenced by bonding, structure, and composition. High modulus materials are stiff and resist deformation. Used in engineering design for load-bearing applications.
        """,
        key_factors=["Stress-strain curve", "Bonding", "Structure", "Composition"],
        primary_authority=["ASM Handbook", "Callister, Materials Science and Engineering"],
        burden_holder="Proponent of elastic modulus claims",
        adversary_position="Elastic modulus may vary with temperature and processing",
        counter_arguments=[
            "High temperatures reduce modulus",
            "Processing alters microstructure and modulus"
        ],
        resolution_strategy="Standardize testing and report modulus accordingly.",
        entity_scope="Metals, polymers, ceramics",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook, Vol. 2"
    ),
    DoctrineBlock(
        topic="Polymers: Crystallization Kinetics",
        keywords=["polymers", "crystallization kinetics", "processing", "microstructure"],
        conclusion_template="Crystallization kinetics determine the rate and extent of polymer crystallinity during processing.",
        reasoning_framework="""
        Crystallization kinetics depend on cooling rate, chain architecture, and additives. Rapid cooling produces amorphous polymers, while slow cooling allows crystallization. Kinetics affect mechanical and thermal properties. Control during processing is essential for desired performance.
        """,
        key_factors=["Cooling rate", "Chain architecture", "Additives", "Processing"],
        primary_authority=["Callister, Materials Science and Engineering", "ASM Handbook"],
        burden_holder="Proponent of crystallization-property relationship",
        adversary_position="Additives may override kinetic effects",
        counter_arguments=[
            "Fillers dominate crystallization behavior",
            "Processing alters kinetics"
        ],
        resolution_strategy="Control processing and additives for desired crystallinity.",
        entity_scope="Polymers and plastics",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Callister, 10th Edition, Ch. 14"
    ),
    DoctrineBlock(
        topic="Corrosion: Microbial",
        keywords=["corrosion", "microbial", "bacteria", "biofilm", "electrochemical"],
        conclusion_template="Microbial corrosion is caused by bacteria forming biofilms and altering electrochemical conditions.",
        reasoning_framework="""
        Microbial corrosion occurs when bacteria colonize metal surfaces, forming biofilms that change local chemistry. Sulfate-reducing bacteria are common culprits, producing hydrogen sulfide and accelerating corrosion. Prevention includes biocide treatment and material selection.
        """,
        key_factors=["Bacteria", "Biofilm", "Local chemistry", "Electrochemical reaction"],
        primary_authority=["ASM Handbook", "Fontana, Corrosion Engineering"],
        burden_holder="Proponent of microbial corrosion risk",
        adversary_position="Microbial corrosion can be controlled by biocide treatment",
        counter_arguments=[
            "Biocides eliminate bacteria",
            "Material selection reduces susceptibility"
        ],
        resolution_strategy="Apply biocides and select resistant materials.",
        entity_scope="Metallic structures",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Fontana, Corrosion Engineering"
    ),
    DoctrineBlock(
        topic="Mechanical Properties: Ductility",
        keywords=["mechanical properties", "ductility", "plastic deformation", "elongation"],
        conclusion_template="Ductility measures a material's ability to undergo plastic deformation before fracture.",
        reasoning_framework="""
        Ductility is quantified by percent elongation or reduction in area during tensile testing. Influenced by microstructure, composition, and processing. High ductility is required for forming operations and safety-critical applications. Trade-offs exist with strength and hardness.
        """,
        key_factors=["Elongation", "Microstructure", "Composition", "Processing"],
        primary_authority=["ASM Handbook", "Callister, Materials Science and Engineering"],
        burden_holder="Proponent of ductility claims",
        adversary_position="Ductility may decrease with increased strength or hardness",
        counter_arguments=[
            "High strength alloys may be brittle",
            "Processing alters ductility"
        ],
        resolution_strategy="Balance properties through alloy design and processing.",
        entity_scope="Metals, polymers, ceramics",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook, Vol. 2"
    ),
    DoctrineBlock(
        topic="Phase Diagrams: Miscibility Gap",
        keywords=["phase diagram", "miscibility gap", "solubility", "phase separation"],
        conclusion_template="A miscibility gap indicates a region where two phases are immiscible and separate.",
        reasoning_framework="""
        Miscibility gaps occur in phase diagrams when two components are not fully soluble in each other. The gap is bounded by solvus lines and results in phase separation. Understanding miscibility gaps is essential for alloy design and predicting microstructure.
        """,
        key_factors=["Solubility", "Phase separation", "Composition", "Microstructure"],
        primary_authority=["ASM Handbook", "Phase Diagrams: Understanding the Basics"],
        burden_holder="Proponent of miscibility gap claims",
        adversary_position="Non-equilibrium processing may suppress phase separation",
        counter_arguments=[
            "Rapid cooling prevents separation",
            "Impurities shift miscibility gap"
        ],
        resolution_strategy="Validate microstructure experimentally and consult phase diagrams.",
        entity_scope="Alloy systems",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook, Vol. 3"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    results = []
    keyword_lower = keyword.lower()
    for doctrine in DOCTRINE_CACHE:
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in k.lower() for k in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]