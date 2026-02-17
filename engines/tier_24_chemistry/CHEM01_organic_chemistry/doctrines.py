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
        topic="SN2_Nucleophilic_Substitution",
        keywords=["bimolecular", "nucleophile", "backside attack", "inversion", "primary alkyl halide", "polar aprotic"],
        conclusion_template="The SN2 mechanism proceeds with a strong nucleophile and a primary substrate, resulting in inversion of configuration.",
        reasoning_framework="""
The SN2 reaction is a concerted, single-step process where the nucleophile attacks the electrophilic carbon from the side opposite to the leaving group (backside attack). The transition state involves simultaneous bond formation and bond breaking. The rate depends on both the nucleophile and substrate concentrations (second order). Steric hindrance is a key factor; thus, methyl and primary substrates react fastest. Polar aprotic solvents enhance nucleophilicity, favoring SN2. The reaction results in inversion of stereochemistry at the reactive center (Walden inversion).
        """,
        key_factors=[
            "Substrate structure (primary > secondary >> tertiary)",
            "Strength and concentration of nucleophile",
            "Leaving group ability",
            "Solvent effects (polar aprotic preferred)",
            "Steric hindrance"
        ],
        primary_authority=[
            "March's Advanced Organic Chemistry",
            "Clayden, Greeves, Warren & Wothers: Organic Chemistry"
        ],
        burden_holder="Proponent of SN2 pathway",
        adversary_position="SN1 or E2 mechanism predominates under the given conditions",
        counter_arguments=[
            "Tertiary substrates hinder backside attack, favoring SN1/E2",
            "Weak nucleophiles or polar protic solvents disfavor SN2"
        ],
        resolution_strategy="Analyze substrate, nucleophile, solvent, and leaving group; confirm by stereochemical outcome and kinetic studies.",
        entity_scope="Alkyl halides and related electrophiles",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Walden Inversion (1896); Hughes-Ingold rules"
    ),
    DoctrineBlock(
        topic="SN1_Nucleophilic_Substitution",
        keywords=["unimolecular", "carbocation", "racemization", "tertiary alkyl halide", "polar protic"],
        conclusion_template="The SN1 mechanism is favored with tertiary substrates and polar protic solvents, leading to racemization.",
        reasoning_framework="""
The SN1 mechanism involves a two-step process: first, the leaving group departs to form a carbocation intermediate; second, the nucleophile attacks the planar carbocation. The rate-determining step is unimolecular, depending only on substrate concentration. Carbocation stability is critical (tertiary > secondary >> primary). Polar protic solvents stabilize carbocations and anions, favoring SN1. The reaction often leads to racemization due to planar intermediate. Rearrangements may occur if more stable carbocations can form.
        """,
        key_factors=[
            "Substrate structure (carbocation stability)",
            "Leaving group ability",
            "Solvent polarity (protic)",
            "Nucleophile strength (less important)",
            "Potential for rearrangement"
        ],
        primary_authority=[
            "March's Advanced Organic Chemistry",
            "Solomons & Fryhle: Organic Chemistry"
        ],
        burden_holder="Proponent of SN1 pathway",
        adversary_position="SN2 or E1/E2 mechanisms predominate",
        counter_arguments=[
            "Primary and methyl substrates do not form stable carbocations",
            "Strong nucleophiles and polar aprotic solvents disfavor SN1"
        ],
        resolution_strategy="Assess substrate, solvent, and product stereochemistry; monitor for rearrangement products.",
        entity_scope="Alkyl halides and related electrophiles",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Hughes-Ingold rules; Walden racemization"
    ),
    DoctrineBlock(
        topic="E2_Elimination",
        keywords=["bimolecular", "strong base", "antiperiplanar", "alkene formation", "Zaitsev", "Hofmann"],
        conclusion_template="E2 elimination is favored by strong bases and antiperiplanar geometry, leading to alkene formation.",
        reasoning_framework="""
The E2 mechanism is a concerted, single-step elimination where a strong base abstracts a proton antiperiplanar to the leaving group, resulting in alkene formation. The reaction is second order, depending on both substrate and base. Stereochemistry is dictated by the requirement for antiperiplanar geometry. Zaitsev's rule predicts the more substituted alkene as the major product unless bulky bases (Hofmann elimination) or steric hindrance favor less substituted alkenes.
        """,
        key_factors=[
            "Base strength and steric bulk",
            "Substrate structure (primary, secondary, tertiary)",
            "Leaving group ability",
            "Antiperiplanar geometry",
            "Solvent effects"
        ],
        primary_authority=[
            "March's Advanced Organic Chemistry",
            "Carey & Sundberg: Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of E2 pathway",
        adversary_position="SN2 or E1/SN1 mechanisms predominate",
        counter_arguments=[
            "Poor leaving group or lack of antiperiplanar hydrogens inhibits E2",
            "Weak bases or polar protic solvents favor E1"
        ],
        resolution_strategy="Analyze base, substrate, and product distribution; use deuterium labeling to confirm mechanism.",
        entity_scope="Alkyl halides, alcohols (after activation)",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Zaitsev's Rule (1875); Hofmann elimination"
    ),
    DoctrineBlock(
        topic="Grignard_Reagent_Chemistry",
        keywords=["organomagnesium", "nucleophile", "carbonyl addition", "ether solvent", "protonation"],
        conclusion_template="Grignard reagents act as strong nucleophiles and bases, adding to electrophilic centers such as carbonyls.",
        reasoning_framework="""
Grignard reagents (RMgX) are prepared by reacting alkyl or aryl halides with magnesium in dry ether. They are highly reactive nucleophiles and bases, attacking electrophilic centers such as carbonyl groups to form alcohols after acidic workup. The reaction is sensitive to moisture and protic solvents, which destroy the reagent. The choice of substrate, solvent, and temperature affects yield and selectivity. Grignard reagents can also act as bases, deprotonating acidic hydrogens.
        """,
        key_factors=[
            "Preparation conditions (anhydrous, ether solvent)",
            "Substrate electrophilicity",
            "Functional group compatibility",
            "Workup procedure",
            "Reagent stability"
        ],
        primary_authority=[
            "Grignard, V.: Nobel Lecture (1912)",
            "March's Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of Grignard methodology",
        adversary_position="Alternative nucleophilic addition or organolithium chemistry",
        counter_arguments=[
            "Functional groups incompatible with Grignard (e.g., -OH, -NH2, -COOH)",
            "Moisture or air sensitivity reduces yield"
        ],
        resolution_strategy="Ensure anhydrous conditions and compatible substrates; confirm product by spectroscopy.",
        entity_scope="Organomagnesium reagents and carbonyl compounds",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Grignard's Nobel Prize work (1900-1912)"
    ),
    DoctrineBlock(
        topic="Wittig_Reaction",
        keywords=["ylide", "phosphonium", "alkene synthesis", "carbonyl", "stereoselectivity"],
        conclusion_template="The Wittig reaction converts aldehydes or ketones to alkenes via phosphonium ylides.",
        reasoning_framework="""
The Wittig reaction involves the reaction of a phosphonium ylide with an aldehyde or ketone to form an alkene and triphenylphosphine oxide. The reaction proceeds via a [2+2] cycloaddition to form an oxaphosphetane intermediate, which decomposes to the alkene. The stereochemistry (E/Z) of the product depends on the nature of the ylide (stabilized or unstabilized) and the carbonyl substrate. The reaction is widely used for carbon-carbon double bond formation.
        """,
        key_factors=[
            "Ylide stability (stabilized vs unstabilized)",
            "Carbonyl substrate (aldehyde vs ketone)",
            "Reaction conditions (solvent, temperature)",
            "Stereoselectivity (E/Z ratio)",
            "Functional group compatibility"
        ],
        primary_authority=[
            "Wittig, G.: Nobel Lecture (1979)",
            "Carey & Sundberg: Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of Wittig methodology",
        adversary_position="Alternative olefination (e.g., Horner–Wadsworth–Emmons)",
        counter_arguments=[
            "Sterically hindered substrates may give poor yields",
            "Competing side reactions with certain functional groups"
        ],
        resolution_strategy="Optimize ylide and substrate; analyze product stereochemistry by NMR.",
        entity_scope="Aldehydes, ketones, phosphonium ylides",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Wittig's Nobel Prize work (1954-1979)"
    ),
    DoctrineBlock(
        topic="Diels_Alder_Reaction",
        keywords=["[4+2] cycloaddition", "diene", "dienophile", "pericyclic", "endo rule", "stereochemistry"],
        conclusion_template="The Diels-Alder reaction forms six-membered rings via a concerted [4+2] cycloaddition between a diene and a dienophile.",
        reasoning_framework="""
The Diels-Alder reaction is a pericyclic, concerted [4+2] cycloaddition between a conjugated diene and a dienophile, forming a six-membered ring. The reaction is stereospecific, with the endo product typically favored due to secondary orbital interactions (endo rule). Electron-rich dienes and electron-poor dienophiles accelerate the reaction. The reaction proceeds under thermal conditions and is widely used in synthetic organic chemistry for constructing cyclic systems.
        """,
        key_factors=[
            "Diene conformation (s-cis required)",
            "Dienophile electron deficiency",
            "Substituent effects",
            "Temperature and solvent",
            "Endo/exo selectivity"
        ],
        primary_authority=[
            "Diels, O. & Alder, K.: Nobel Lecture (1950)",
            "March's Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of Diels-Alder pathway",
        adversary_position="Competing reactions or stepwise mechanisms",
        counter_arguments=[
            "Steric hindrance or improper diene conformation inhibits reaction",
            "Electron-rich dienophiles react sluggishly"
        ],
        resolution_strategy="Ensure s-cis diene and activated dienophile; confirm product by NMR and IR.",
        entity_scope="Conjugated dienes and electron-deficient alkenes/alkynes",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Diels-Alder Nobel Prize (1950); Endo rule"
    ),
    DoctrineBlock(
        topic="Aldol_Condensation",
        keywords=["enolate", "aldol addition", "dehydration", "base-catalyzed", "crossed aldol", "enone"],
        conclusion_template="Aldol condensation forms β-hydroxy carbonyls or α,β-unsaturated carbonyls via enolate addition and dehydration.",
        reasoning_framework="""
Aldol condensation involves the formation of an enolate ion (under base or acid catalysis) that attacks a carbonyl carbon, forming a β-hydroxy carbonyl (aldol addition). Subsequent dehydration yields an α,β-unsaturated carbonyl compound (aldol condensation). The reaction can be intramolecular or intermolecular (crossed aldol). Selectivity depends on enolate formation and substrate reactivity. Control of conditions can suppress or promote dehydration.
        """,
        key_factors=[
            "Enolate formation (base or acid catalysis)",
            "Substrate reactivity (aldehydes > ketones)",
            "Reaction conditions (temperature, solvent)",
            "Possibility of self-condensation or crossed reactions",
            "Dehydration step"
        ],
        primary_authority=[
            "March's Advanced Organic Chemistry",
            "Carey & Sundberg: Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of aldol pathway",
        adversary_position="Competing condensation or polymerization",
        counter_arguments=[
            "Steric hindrance or lack of α-hydrogens prevents enolate formation",
            "Uncontrolled conditions lead to mixtures"
        ],
        resolution_strategy="Control enolate generation; use selective substrates; monitor by TLC and NMR.",
        entity_scope="Aldehydes, ketones, enolizable carbonyls",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Wurtz, 1872; Zimmerman-Traxler model"
    ),
    DoctrineBlock(
        topic="Protecting_Groups_Strategy",
        keywords=["functional group protection", "selectivity", "orthogonality", "deprotection", "synthetic planning"],
        conclusion_template="Protecting groups are used to temporarily mask reactive functional groups during multi-step syntheses.",
        reasoning_framework="""
Protecting groups are introduced to temporarily mask functional groups that would otherwise interfere with a desired transformation. The choice of protecting group depends on its stability under the planned reaction conditions and its ease of removal (orthogonality). The strategy is essential for complex molecule synthesis, enabling selective reactions. Common protecting groups include silyl ethers for alcohols, Boc for amines, and acetal/ketal for carbonyls. Deprotection should occur under mild, selective conditions.
        """,
        key_factors=[
            "Functional group compatibility",
            "Stability under reaction conditions",
            "Ease and selectivity of deprotection",
            "Orthogonality (non-interference with other groups)",
            "Impact on overall synthetic efficiency"
        ],
        primary_authority=[
            "Greene & Wuts: Protective Groups in Organic Synthesis",
            "March's Advanced Organic Chemistry"
        ],
        burden_holder="Synthetic chemist proposing protection",
        adversary_position="Direct transformation without protection",
        counter_arguments=[
            "Additional steps reduce overall yield",
            "Deprotection may cause side reactions"
        ],
        resolution_strategy="Select protecting groups based on planned transformations; confirm by NMR and IR.",
        entity_scope="All functional groups in organic synthesis",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Greene & Wuts, 1981-present"
    ),
    DoctrineBlock(
        topic="Oxidation_Reactions_Alcohols",
        keywords=["primary alcohol", "secondary alcohol", "aldehyde", "ketone", "carboxylic acid", "PCC", "Jones", "Swern"],
        conclusion_template="Alcohols are oxidized to aldehydes, ketones, or carboxylic acids depending on substrate and oxidant.",
        reasoning_framework="""
Primary alcohols can be oxidized to aldehydes or further to carboxylic acids, while secondary alcohols yield ketones. The choice of oxidant and conditions determines selectivity. PCC and Swern oxidation allow for aldehyde formation without overoxidation, while Jones oxidation and KMnO4 lead to carboxylic acids. Tertiary alcohols do not undergo oxidation under normal conditions. The reaction is monitored by TLC, NMR, or IR.
        """,
        key_factors=[
            "Alcohol class (primary, secondary, tertiary)",
            "Choice of oxidant (PCC, Swern, Jones, KMnO4)",
            "Reaction conditions (solvent, temperature)",
            "Functional group compatibility",
            "Overoxidation risk"
        ],
        primary_authority=[
            "March's Advanced Organic Chemistry",
            "Carey & Sundberg: Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of oxidation method",
        adversary_position="Alternative oxidation or reduction",
        counter_arguments=[
            "Sensitive substrates may decompose",
            "Toxicity or environmental impact of oxidants"
        ],
        resolution_strategy="Select oxidant based on substrate and desired product; monitor for overoxidation.",
        entity_scope="Alcohols and oxidizing agents",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Collins, Swern, Jones oxidations"
    ),
    DoctrineBlock(
        topic="Reduction_Reactions_Carbonyls",
        keywords=["aldehyde", "ketone", "NaBH4", "LiAlH4", "selectivity", "hydride reduction"],
        conclusion_template="Carbonyl compounds are reduced to alcohols by hydride donors such as NaBH4 or LiAlH4.",
        reasoning_framework="""
Aldehydes and ketones are reduced to primary and secondary alcohols, respectively, by hydride transfer from reagents like sodium borohydride (NaBH4) or lithium aluminum hydride (LiAlH4). NaBH4 is milder and compatible with protic solvents, while LiAlH4 is more reactive and reduces esters, acids, and amides. Selectivity is determined by reagent choice and reaction conditions. Functional group compatibility must be considered.
        """,
        key_factors=[
            "Carbonyl class (aldehyde, ketone, ester, acid)",
            "Reagent choice (NaBH4 vs LiAlH4)",
            "Solvent compatibility",
            "Functional group tolerance",
            "Workup procedure"
        ],
        primary_authority=[
            "March's Advanced Organic Chemistry",
            "Carey & Sundberg: Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of reduction method",
        adversary_position="Alternative reduction or oxidation",
        counter_arguments=[
            "LiAlH4 is highly reactive and moisture sensitive",
            "Functional groups may be reduced unintentionally"
        ],
        resolution_strategy="Select appropriate hydride; confirm reduction by NMR and IR.",
        entity_scope="Carbonyl compounds and hydride reagents",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Meerwein-Ponndorf-Verley, Wolff-Kishner, Clemmensen reductions"
    ),
    DoctrineBlock(
        topic="Electrophilic_Aromatic_Substitution",
        keywords=["aromatic ring", "electrophile", "substitution", "activating group", "deactivating group", "regioselectivity"],
        conclusion_template="Electrophilic aromatic substitution introduces substituents onto aromatic rings, with regioselectivity governed by existing groups.",
        reasoning_framework="""
Electrophilic aromatic substitution (EAS) involves the attack of an aromatic π system on an electrophile, forming a resonance-stabilized carbocation intermediate (arenium ion), followed by deprotonation to restore aromaticity. The nature of substituents already on the ring determines the rate and regioselectivity: activating groups (e.g., -OH, -OCH3) direct ortho/para, while deactivating groups (e.g., -NO2, -CF3) direct meta. Common EAS reactions include nitration, sulfonation, halogenation, Friedel-Crafts alkylation/acylation.
        """,
        key_factors=[
            "Nature and position of existing substituents",
            "Electrophile strength",
            "Reaction conditions (temperature, solvent, catalyst)",
            "Aromatic ring structure",
            "Steric effects"
        ],
        primary_authority=[
            "March's Advanced Organic Chemistry",
            "Carey & Sundberg: Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of EAS pathway",
        adversary_position="Nucleophilic or radical aromatic substitution",
        counter_arguments=[
            "Strong deactivators may prevent reaction",
            "Polyalkylation or rearrangement in Friedel-Crafts"
        ],
        resolution_strategy="Analyze substituent effects and reaction conditions; confirm regioisomer by NMR.",
        entity_scope="Aromatic compounds and electrophiles",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Hückel's rule; directing effects"
    ),
    DoctrineBlock(
        topic="Nucleophilic_Aromatic_Substitution",
        keywords=["aromatic ring", "nucleophile", "leaving group", "electron-withdrawing group", "Meisenheimer complex"],
        conclusion_template="Nucleophilic aromatic substitution occurs on activated rings with good leaving groups and strong electron-withdrawing substituents.",
        reasoning_framework="""
Nucleophilic aromatic substitution (NAS) proceeds via addition-elimination (Meisenheimer complex) or elimination-addition (benzyne) mechanisms. The presence of strong electron-withdrawing groups (e.g., -NO2) ortho/para to the leaving group activates the ring. Good leaving groups (e.g., halides) are required. The nucleophile attacks the activated carbon, forming a resonance-stabilized intermediate, which then eliminates the leaving group. The reaction is favored by harsh conditions (heat, strong nucleophile).
        """,
        key_factors=[
            "Presence and position of electron-withdrawing groups",
            "Leaving group ability",
            "Nucleophile strength",
            "Reaction conditions (temperature, solvent)",
            "Aromatic ring activation"
        ],
        primary_authority=[
            "March's Advanced Organic Chemistry",
            "Carey & Sundberg: Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of NAS pathway",
        adversary_position="Electrophilic or radical aromatic substitution",
        counter_arguments=[
            "Lack of activating groups or poor leaving group inhibits reaction",
            "Competing side reactions at high temperature"
        ],
        resolution_strategy="Ensure proper activation and leaving group; confirm product by NMR and MS.",
        entity_scope="Activated aromatic compounds and nucleophiles",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Meisenheimer complex (1902); Benzyne mechanism"
    ),
    DoctrineBlock(
        topic="Stereochemistry_Chirality",
        keywords=["chiral center", "enantiomer", "diastereomer", "optical activity", "configuration", "R/S", "E/Z"],
        conclusion_template="Stereochemistry governs the spatial arrangement of atoms, leading to chiral and achiral molecules with distinct properties.",
        reasoning_framework="""
Stereochemistry deals with the 3D arrangement of atoms in molecules. Chirality arises when a molecule is non-superimposable on its mirror image, typically due to a tetrahedral carbon with four different substituents (chiral center). Enantiomers have identical physical properties except for optical rotation and interactions with other chiral entities. Diastereomers differ at one or more stereocenters and have different physical properties. Configuration is assigned using the Cahn-Ingold-Prelog (R/S, E/Z) system. Stereochemistry affects reactivity, biological activity, and physical properties.
        """,
        key_factors=[
            "Number and type of stereocenters",
            "Molecular symmetry",
            "Configuration assignment (R/S, E/Z)",
            "Optical activity",
            "Physical and biological properties"
        ],
        primary_authority=[
            "Eliel & Wilen: Stereochemistry of Organic Compounds",
            "March's Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of stereochemical assignment",
        adversary_position="Alternative configuration or achirality",
        counter_arguments=[
            "Meso compounds are achiral despite stereocenters",
            "Incorrect assignment of priorities"
        ],
        resolution_strategy="Apply CIP rules; use polarimetry, NMR, and X-ray crystallography.",
        entity_scope="All organic molecules with stereocenters",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Cahn-Ingold-Prelog rules (1956); Pasteur's resolution (1848)"
    ),
    DoctrineBlock(
        topic="Retrosynthetic_Analysis",
        keywords=["disconnection", "synthons", "target molecule", "strategic bond", "functional group interconversion"],
        conclusion_template="Retrosynthetic analysis breaks down complex molecules into simpler precursors, guiding synthetic planning.",
        reasoning_framework="""
Retrosynthetic analysis involves mentally breaking down a target molecule into simpler starting materials by identifying strategic bonds for disconnection. Each disconnection corresponds to a known synthetic transformation. Synthons are idealized fragments, which are then mapped to real reagents (synthetic equivalents). The process is iterative, considering functional group interconversions, reactivity, and selectivity. The goal is to design an efficient, practical synthetic route.
        """,
        key_factors=[
            "Identification of strategic bonds",
            "Availability of starting materials",
            "Functional group compatibility",
            "Selectivity and protecting group needs",
            "Step economy"
        ],
        primary_authority=[
            "Corey, E.J.: Nobel Lecture (1990)",
            "Warren: Organic Synthesis – The Disconnection Approach"
        ],
        burden_holder="Synthetic planner",
        adversary_position="Alternative synthetic routes",
        counter_arguments=[
            "Proposed disconnections may be impractical",
            "Functional group incompatibility"
        ],
        resolution_strategy="Iterative analysis; consult precedent and literature; confirm feasibility experimentally.",
        entity_scope="All organic molecules",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="Corey's retrosynthetic analysis (1967-1990)"
    ),
    DoctrineBlock(
        topic="NMR_Spectroscopy",
        keywords=["nuclear magnetic resonance", "chemical shift", "coupling constant", "integration", "spin-spin splitting"],
        conclusion_template="NMR spectroscopy elucidates molecular structure by analyzing chemical shifts, coupling, and integration.",
        reasoning_framework="""
NMR spectroscopy exploits the magnetic properties of certain nuclei (e.g., 1H, 13C) in a magnetic field. The chemical shift reflects the electronic environment. Spin-spin coupling reveals connectivity and spatial relationships. Integration provides relative proton counts. Multiplicity and coupling constants (J) inform about neighboring nuclei. Advanced techniques (COSY, HSQC, HMBC) enable 2D correlation. NMR is essential for structure elucidation, purity assessment, and stereochemical assignment.
        """,
        key_factors=[
            "Chemical shift values",
            "Integration and multiplicity",
            "Coupling constants",
            "Solvent and temperature effects",
            "Advanced 2D techniques"
        ],
        primary_authority=[
            "Claridge: High-Resolution NMR Techniques in Organic Chemistry",
            "Silverstein & Webster: Spectrometric Identification of Organic Compounds"
        ],
        burden_holder="Analyst interpreting spectra",
        adversary_position="Alternative structural assignment",
        counter_arguments=[
            "Signal overlap or exchange broadening complicates analysis",
            "Impurities or solvent peaks may obscure signals"
        ],
        resolution_strategy="Use 2D NMR and reference spectra; confirm with complementary techniques.",
        entity_scope="NMR-active organic compounds",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Bloch, Purcell Nobel (1952); C-13 NMR"
    ),
    DoctrineBlock(
        topic="IR_Spectroscopy",
        keywords=["infrared", "functional group identification", "stretching", "bending", "wavenumber", "fingerprint region"],
        conclusion_template="IR spectroscopy identifies functional groups by characteristic absorption frequencies.",
        reasoning_framework="""
IR spectroscopy measures molecular vibrations (stretching, bending) that absorb infrared light at characteristic wavenumbers. Functional groups have distinct absorption bands (e.g., C=O ~1700 cm-1, O-H ~3300 cm-1). The fingerprint region (600-1500 cm-1) is unique for each molecule. IR is used for functional group identification, monitoring reactions, and confirming purity. Sample preparation (neat, solution, KBr pellet) affects spectra.
        """,
        key_factors=[
            "Characteristic absorption frequencies",
            "Sample preparation",
            "Intensity and shape of peaks",
            "Fingerprint region analysis",
            "Interference from impurities"
        ],
        primary_authority=[
            "Silverstein & Webster: Spectrometric Identification of Organic Compounds",
            "Pavia, Lampman, Kriz: Introduction to Spectroscopy"
        ],
        burden_holder="Analyst interpreting spectra",
        adversary_position="Alternative functional group assignment",
        counter_arguments=[
            "Overlapping bands or weak absorptions",
            "Hydrogen bonding shifts frequencies"
        ],
        resolution_strategy="Compare to reference spectra; use complementary techniques (NMR, MS).",
        entity_scope="IR-active organic compounds",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Coblentz, 1905; Modern FT-IR"
    ),
    DoctrineBlock(
        topic="Mass_Spectrometry",
        keywords=["ionization", "fragmentation", "molecular ion", "base peak", "isotopic pattern", "mass-to-charge"],
        conclusion_template="Mass spectrometry determines molecular weight and structure via ionization and fragmentation patterns.",
        reasoning_framework="""
Mass spectrometry (MS) ionizes molecules and separates ions by mass-to-charge ratio (m/z). The molecular ion peak gives molecular weight; fragmentation patterns reveal structural features. Isotopic patterns (e.g., Br, Cl) assist in elemental analysis. Techniques include electron impact (EI), chemical ionization (CI), electrospray (ESI), and MALDI. MS is used for molecular formula determination, structure elucidation, and purity assessment. Tandem MS (MS/MS) enables sequencing and complex analysis.
        """,
        key_factors=[
            "Ionization technique",
            "Molecular ion and base peak identification",
            "Fragmentation pathways",
            "Isotopic distribution",
            "Instrument resolution"
        ],
        primary_authority=[
            "Gross: Mass Spectrometry – A Textbook",
            "Silverstein & Webster: Spectrometric Identification of Organic Compounds"
        ],
        burden_holder="Analyst interpreting spectra",
        adversary_position="Alternative structural assignment",
        counter_arguments=[
            "Absence of molecular ion in EI",
            "Complex fragmentation in large molecules"
        ],
        resolution_strategy="Combine MS with NMR and IR; use high-resolution MS for exact mass.",
        entity_scope="Ionizable organic compounds",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Dempster, 1918; Modern MS techniques"
    ),
    DoctrineBlock(
        topic="Radical_Reactions",
        keywords=["homolytic cleavage", "initiation", "propagation", "termination", "halogenation", "peroxides"],
        conclusion_template="Radical reactions proceed via chain mechanisms with initiation, propagation, and termination steps.",
        reasoning_framework="""
Radical reactions involve species with unpaired electrons, generated by homolytic bond cleavage (e.g., heat, light, peroxides). The mechanism includes initiation (radical generation), propagation (chain reaction), and termination (radical recombination). Common examples include halogenation of alkanes and polymerization. Selectivity is influenced by bond dissociation energies and radical stability (tertiary > secondary > primary). Inhibitors (e.g., BHT) quench radicals.
        """,
        key_factors=[
            "Radical generation method",
            "Substrate structure and radical stability",
            "Reaction conditions (light, heat, initiators)",
            "Presence of inhibitors",
            "Selectivity (regio- and chemoselectivity)"
        ],
        primary_authority=[
            "March's Advanced Organic Chemistry",
            "Carey & Sundberg: Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of radical pathway",
        adversary_position="Ionic or concerted mechanisms",
        counter_arguments=[
            "Competing side reactions or overhalogenation",
            "Inhibitors suppress radical chain"
        ],
        resolution_strategy="Control initiation and monitor intermediates; confirm by product analysis.",
        entity_scope="Organic molecules susceptible to homolytic cleavage",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Gomberg, 1900; Modern radical chemistry"
    ),
    DoctrineBlock(
        topic="Pericyclic_Reactions",
        keywords=["concerted", "cyclic transition state", "Woodward-Hoffmann", "sigmatropic", "electrocyclic", "cycloaddition"],
        conclusion_template="Pericyclic reactions proceed via concerted, cyclic transition states governed by orbital symmetry rules.",
        reasoning_framework="""
Pericyclic reactions are concerted processes involving cyclic redistribution of bonding electrons through a transition state with continuous orbital overlap. Types include cycloadditions (e.g., Diels-Alder), electrocyclic reactions, and sigmatropic rearrangements. The Woodward-Hoffmann rules predict allowedness based on orbital symmetry (conservation of orbital symmetry). Stereochemistry is controlled by the reaction mode (thermal vs photochemical). These reactions are generally stereospecific and regioselective.
        """,
        key_factors=[
            "Type of pericyclic reaction",
            "Orbital symmetry (Woodward-Hoffmann rules)",
            "Reaction conditions (thermal, photochemical)",
            "Substrate structure",
            "Stereochemical outcome"
        ],
        primary_authority=[
            "Woodward & Hoffmann: The Conservation of Orbital Symmetry (1965)",
            "March's Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of pericyclic mechanism",
        adversary_position="Stepwise or radical mechanisms",
        counter_arguments=[
            "Steric or electronic effects may inhibit pericyclic pathway",
            "Photochemical conditions may alter outcome"
        ],
        resolution_strategy="Apply symmetry rules; confirm by stereochemical analysis and kinetic studies.",
        entity_scope="Organic molecules with conjugated systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Woodward-Hoffmann rules (1965)"
    ),
    DoctrineBlock(
        topic="Green_Chemistry_Principles",
        keywords=["atom economy", "waste minimization", "renewable feedstocks", "safer solvents", "energy efficiency"],
        conclusion_template="Green chemistry aims to design chemical processes that reduce or eliminate hazardous substances and waste.",
        reasoning_framework="""
Green chemistry is guided by 12 principles, including prevention of waste, atom economy, use of safer solvents and reagents, renewable feedstocks, energy efficiency, and design for degradation. The goal is to minimize environmental impact and improve sustainability. Metrics such as E-factor and atom economy are used to assess process greenness. Regulatory and societal pressures drive adoption in academia and industry.
        """,
        key_factors=[
            "Atom economy and E-factor",
            "Hazard and toxicity of reagents and products",
            "Energy and resource consumption",
            "Renewable vs non-renewable feedstocks",
            "Process safety and scalability"
        ],
        primary_authority=[
            "Anastas & Warner: Green Chemistry: Theory and Practice (1998)",
            "ACS Green Chemistry Institute"
        ],
        burden_holder="Process designer",
        adversary_position="Traditional, less sustainable methods",
        counter_arguments=[
            "Green alternatives may be less efficient or more costly",
            "Limited availability of renewable feedstocks"
        ],
        resolution_strategy="Evaluate process using green metrics; prioritize safety and sustainability.",
        entity_scope="All chemical processes and products",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Anastas & Warner, 1998; 12 Principles of Green Chemistry"
    ),
    DoctrineBlock(
        topic="Polymer_Chemistry_Fundamentals",
        keywords=["monomer", "polymerization", "addition", "condensation", "degree of polymerization", "copolymer"],
        conclusion_template="Polymers are formed by linking monomers via addition or condensation polymerization, with properties governed by structure.",
        reasoning_framework="""
Polymer chemistry studies the synthesis and properties of macromolecules formed by repeating monomer units. Addition (chain-growth) polymerization involves unsaturated monomers (e.g., ethylene), while condensation (step-growth) polymerization produces polymers with elimination of small molecules (e.g., nylon). Degree of polymerization, molecular weight, and tacticity affect physical properties. Copolymers combine different monomers for tailored properties. Characterization uses GPC, NMR, and DSC.
        """,
        key_factors=[
            "Monomer structure and reactivity",
            "Polymerization mechanism (addition, condensation)",
            "Degree of polymerization and molecular weight",
            "Tacticity and branching",
            "Thermal and mechanical properties"
        ],
        primary_authority=[
            "Odian: Principles of Polymerization",
            "Allcock, Lampe & Mark: Contemporary Polymer Chemistry"
        ],
        burden_holder="Polymer chemist",
        adversary_position="Alternative polymerization or material selection",
        counter_arguments=[
            "Chain transfer or termination limits molecular weight",
            "Impurities affect polymer properties"
        ],
        resolution_strategy="Optimize monomer purity and reaction conditions; characterize by GPC and NMR.",
        entity_scope="Monomers, polymers, and copolymers",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Staudinger, 1920s; Flory, 1953 Nobel"
    ),
    DoctrineBlock(
        topic="Carbohydrate_Chemistry",
        keywords=["monosaccharide", "glycosidic bond", "anomer", "mutarotation", "stereochemistry", "polysaccharide"],
        conclusion_template="Carbohydrate chemistry focuses on the structure, reactivity, and synthesis of sugars and their derivatives.",
        reasoning_framework="""
Carbohydrates are polyhydroxy aldehydes or ketones, classified as monosaccharides, oligosaccharides, and polysaccharides. Stereochemistry is crucial (D/L, α/β anomers). Glycosidic bond formation links monosaccharides. Mutarotation describes interconversion between anomers in solution. Protecting groups and selective activation are key in oligosaccharide synthesis. Analytical techniques include NMR, MS, and optical rotation.
        """,
        key_factors=[
            "Monosaccharide configuration and ring form",
            "Anomeric effect and mutarotation",
            "Glycosidic bond formation and cleavage",
            "Protecting group strategy",
            "Analytical methods"
        ],
        primary_authority=[
            "Fraser-Reid, Tatsuta, Thiem: Glycoscience",
            "Wolfrom & Shafizadeh: Advances in Carbohydrate Chemistry"
        ],
        burden_holder="Carbohydrate chemist",
        adversary_position="Alternative synthetic or analytical methods",
        counter_arguments=[
            "Complexity of stereochemistry and protecting group manipulations",
            "Low yields in oligosaccharide synthesis"
        ],
        resolution_strategy="Careful planning of protecting group sequence; use modern glycosylation methods.",
        entity_scope="Monosaccharides, oligosaccharides, polysaccharides",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Fischer, 1891; Haworth, 1929"
    ),
    DoctrineBlock(
        topic="Amino_Acid_Peptide_Chemistry",
        keywords=["amino acid", "peptide bond", "solid-phase synthesis", "chirality", "protection", "sequence"],
        conclusion_template="Amino acid and peptide chemistry involves synthesis, protection, and sequencing of peptides and proteins.",
        reasoning_framework="""
Amino acids are chiral molecules with amino and carboxyl groups. Peptide bonds link amino acids to form peptides and proteins. Solid-phase peptide synthesis (SPPS) enables automated, stepwise assembly using protecting groups (e.g., Fmoc, Boc). Sequence and stereochemistry are critical for biological activity. Analytical techniques include HPLC, MS, and Edman degradation. Racemization and side reactions must be minimized.
        """,
        key_factors=[
            "Amino acid configuration (L/D)",
            "Protecting group strategy",
            "Coupling reagents and conditions",
            "Sequence and length",
            "Purification and analysis"
        ],
        primary_authority=[
            "Merrifield: Nobel Lecture (1984)",
            "Bodanszky: Principles of Peptide Synthesis"
        ],
        burden_holder="Peptide chemist",
        adversary_position="Alternative synthetic or sequencing methods",
        counter_arguments=[
            "Racemization during coupling",
            "Incomplete deprotection or coupling"
        ],
        resolution_strategy="Optimize coupling and deprotection; analyze by HPLC and MS.",
        entity_scope="Amino acids, peptides, proteins",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Merrifield SPPS (1963); Edman degradation"
    ),
    DoctrineBlock(
        topic="Lipid_Chemistry",
        keywords=["fatty acid", "triglyceride", "phospholipid", "saponification", "unsaturation", "membrane"],
        conclusion_template="Lipid chemistry studies the structure, synthesis, and function of fats, oils, and related molecules.",
        reasoning_framework="""
Lipids are hydrophobic biomolecules including fatty acids, triglycerides, phospholipids, and sterols. Fatty acids vary in chain length and degree of unsaturation. Triglycerides are formed by esterification of glycerol with fatty acids. Saponification yields soaps and glycerol. Phospholipids are key membrane components. Analytical techniques include GC, MS, and NMR. Lipid oxidation and hydrogenation affect stability and nutrition.
        """,
        key_factors=[
            "Fatty acid structure (chain length, saturation)",
            "Esterification and hydrolysis",
            "Functional group modifications",
            "Analytical techniques",
            "Biological function"
        ],
        primary_authority=[
            "Lehninger: Principles of Biochemistry",
            "Christie: Lipid Analysis"
        ],
        burden_holder="Lipid chemist",
        adversary_position="Alternative analytical or synthetic approaches",
        counter_arguments=[
            "Complex mixtures complicate analysis",
            "Unsaturation leads to oxidation"
        ],
        resolution_strategy="Use advanced analytical methods; control storage and handling.",
        entity_scope="Fatty acids, triglycerides, phospholipids, sterols",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Chevreul, 1813; Modern lipidomics"
    ),
    DoctrineBlock(
        topic="Organometallic_Cross_Coupling",
        keywords=["palladium", "Suzuki", "Heck", "Negishi", "C-C bond formation", "ligand"],
        conclusion_template="Organometallic cross-coupling forms C–C bonds via transition metal catalysis, enabling complex molecule construction.",
        reasoning_framework="""
Cross-coupling reactions use transition metal catalysts (often Pd) to join organometallic reagents (e.g., boronic acids, stannanes) with organic halides. Key types include Suzuki, Heck, Negishi, Stille, and Sonogashira couplings. Ligands control catalyst activity and selectivity. The reactions tolerate many functional groups and are widely used in pharmaceuticals and materials science. Air and moisture sensitivity of catalysts and reagents must be managed.
        """,
        key_factors=[
            "Choice of catalyst and ligand",
            "Reactivity of coupling partners",
            "Functional group compatibility",
            "Reaction conditions (solvent, temperature, base)",
            "Purification and analysis"
        ],
        primary_authority=[
            "Suzuki, Heck, Negishi: Nobel Lectures (2010)",
            "Miyaura & Suzuki: Chem. Rev. 1995"
        ],
        burden_holder="Synthetic chemist",
        adversary_position="Alternative C–C bond-forming methods",
        counter_arguments=[
            "Catalyst deactivation by air/moisture",
            "Side reactions (homocoupling, β-hydride elimination)"
        ],
        resolution_strategy="Use inert atmosphere; optimize catalyst and conditions; confirm product by NMR and MS.",
        entity_scope="Organohalides, organometallic reagents, transition metal catalysts",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Suzuki, Heck, Negishi Nobel (2010)"
    ),
    DoctrineBlock(
        topic="Safety_Handling_Organic_Reagents",
        keywords=["hazard", "toxicity", "flammability", "PPE", "waste disposal", "MSDS"],
        conclusion_template="Safe handling of organic reagents requires knowledge of hazards, use of PPE, and proper waste management.",
        reasoning_framework="""
Organic reagents may be toxic, flammable, corrosive, or reactive. Safety requires understanding hazards (consult MSDS), using appropriate personal protective equipment (PPE), working in fume hoods, and proper storage. Waste must be segregated and disposed of according to regulations. Emergency procedures (spills, exposure) must be established. Training and risk assessment are mandatory in academic and industrial settings.
        """,
        key_factors=[
            "Hazard identification (MSDS, GHS labels)",
            "PPE selection and use",
            "Engineering controls (fume hoods, ventilation)",
            "Waste segregation and disposal",
            "Training and emergency preparedness"
        ],
        primary_authority=[
            "Prudent Practices in the Laboratory (NRC)",
            "OSHA Laboratory Standard"
        ],
        burden_holder="Lab personnel and supervisors",
        adversary_position="Negligence or non-compliance",
        counter_arguments=[
            "Lack of awareness or training",
            "Improper storage or disposal"
        ],
        resolution_strategy="Mandatory training; regular audits; enforce safety protocols.",
        entity_scope="All users of organic reagents",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="OSHA, EPA, NRC guidelines"
    ),
    # Additional doctrines for coverage and depth
    DoctrineBlock(
        topic="E1_Elimination",
        keywords=["unimolecular", "carbocation", "alkene", "rearrangement", "secondary", "tertiary"],
        conclusion_template="E1 elimination forms alkenes via carbocation intermediates, often with rearrangement.",
        reasoning_framework="""
E1 elimination proceeds via a two-step mechanism: first, the leaving group departs to form a carbocation; second, a base abstracts a proton to form the alkene. The rate depends only on substrate concentration. Carbocation rearrangement is possible, leading to more substituted alkenes (Zaitsev's rule). E1 competes with SN1 under similar conditions (secondary/tertiary substrates, polar protic solvents).
        """,
        key_factors=[
            "Substrate structure (carbocation stability)",
            "Leaving group ability",
            "Base strength (not critical)",
            "Solvent polarity",
            "Potential for rearrangement"
        ],
        primary_authority=[
            "March's Advanced Organic Chemistry",
            "Solomons & Fryhle: Organic Chemistry"
        ],
        burden_holder="Proponent of E1 pathway",
        adversary_position="E2 or SN1/SN2 mechanisms",
        counter_arguments=[
            "Primary substrates rarely undergo E1",
            "Competing substitution reactions"
        ],
        resolution_strategy="Analyze product distribution and rearrangement; confirm by kinetic studies.",
        entity_scope="Secondary/tertiary alkyl halides, alcohols (after activation)",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Hughes-Ingold rules"
    ),
    DoctrineBlock(
        topic="Friedel_Crafts_Alkylation",
        keywords=["alkylation", "aromatic ring", "carbocation", "Lewis acid", "polyalkylation", "rearrangement"],
        conclusion_template="Friedel-Crafts alkylation introduces alkyl groups onto aromatic rings using alkyl halides and Lewis acids.",
        reasoning_framework="""
Friedel-Crafts alkylation uses alkyl halides and Lewis acids (e.g., AlCl3) to generate carbocations, which alkylate aromatic rings. The reaction is limited by carbocation rearrangement, polyalkylation, and deactivation by electron-withdrawing groups. Isopropylation and tert-butylation are common. Deactivated rings (e.g., nitrobenzene) do not react. The reaction is exothermic and may require temperature control.
        """,
        key_factors=[
            "Aromatic ring activation",
            "Alkyl halide reactivity",
            "Lewis acid strength",
            "Carbocation rearrangement",
            "Polyalkylation risk"
        ],
        primary_authority=[
            "March's Advanced Organic Chemistry",
            "Carey & Sundberg: Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of Friedel-Crafts alkylation",
        adversary_position="Alternative alkylation or acylation",
        counter_arguments=[
            "Polyalkylation reduces selectivity",
            "Rearrangement leads to unexpected products"
        ],
        resolution_strategy="Control stoichiometry and temperature; use acylation-reduction for better selectivity.",
        entity_scope="Activated aromatic compounds and alkyl halides",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Friedel & Crafts, 1877"
    ),
    DoctrineBlock(
        topic="Friedel_Crafts_Acylation",
        keywords=["acylation", "aromatic ring", "Lewis acid", "ketone", "monoacylation", "deactivation"],
        conclusion_template="Friedel-Crafts acylation introduces acyl groups onto aromatic rings, forming ketones with high selectivity.",
        reasoning_framework="""
Friedel-Crafts acylation uses acyl chlorides and Lewis acids (e.g., AlCl3) to acylate aromatic rings, forming aryl ketones. The reaction is less prone to polyacylation and rearrangement than alkylation. Electron-withdrawing groups deactivate the ring. The acyl group deactivates the product, preventing further reaction. The process is widely used for synthesizing aromatic ketones.
        """,
        key_factors=[
            "Aromatic ring activation",
            "Acyl chloride reactivity",
            "Lewis acid strength",
            "Product deactivation",
            "Monoacylation selectivity"
        ],
        primary_authority=[
            "March's Advanced Organic Chemistry",
            "Carey & Sundberg: Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of Friedel-Crafts acylation",
        adversary_position="Alternative acylation or alkylation",
        counter_arguments=[
            "Deactivated rings do not react",
            "Lewis acid may complex with product"
        ],
        resolution_strategy="Use excess aromatic substrate; control temperature and stoichiometry.",
        entity_scope="Activated aromatic compounds and acyl chlorides",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Friedel & Crafts, 1877"
    ),
    DoctrineBlock(
        topic="Hofmann_Elimination",
        keywords=["quaternary ammonium", "alkene", "least substituted", "exhaustive methylation", "E2", "Hofmann product"],
        conclusion_template="Hofmann elimination yields the least substituted alkene via E2 elimination of quaternary ammonium salts.",
        reasoning_framework="""
Hofmann elimination converts quaternary ammonium salts to alkenes using silver oxide and heat. The reaction proceeds via E2 mechanism, favoring formation of the least substituted alkene (Hofmann product) due to steric effects. The process requires exhaustive methylation of amines. Competing elimination and substitution must be considered.
        """,
        key_factors=[
            "Quaternary ammonium salt formation",
            "Base strength (silver oxide)",
            "Steric effects",
            "E2 mechanism",
            "Product distribution (Hofmann vs Zaitsev)"
        ],
        primary_authority=[
            "March's Advanced Organic Chemistry",
            "Carey & Sundberg: Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of Hofmann elimination",
        adversary_position="Zaitsev elimination predominates",
        counter_arguments=[
            "Bulky groups favor Hofmann product",
            "Competing substitution may occur"
        ],
        resolution_strategy="Ensure complete methylation; analyze product distribution by GC or NMR.",
        entity_scope="Quaternary ammonium salts",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Hofmann, 1851"
    ),
    DoctrineBlock(
        topic="Baeyer_Villiger_Oxidation",
        keywords=["ketone", "peracid", "ester", "migration", "Baeyer-Villiger", "rearrangement"],
        conclusion_template="Baeyer-Villiger oxidation converts ketones to esters or cyclic ketones to lactones via peracid oxidation.",
        reasoning_framework="""
Baeyer-Villiger oxidation uses peracids (e.g., mCPBA) to oxidize ketones to esters or lactones. The reaction involves nucleophilic attack by the peracid, formation of a Criegee intermediate, and migration of an adjacent group to oxygen. The migratory aptitude follows the order: tertiary > secondary > aryl > primary > methyl. The reaction is regioselective and useful for ring expansion.
        """,
        key_factors=[
            "Ketone structure",
            "Peracid reactivity",
            "Migratory aptitude",
            "Reaction conditions",
            "Functional group compatibility"
        ],
        primary_authority=[
            "March's Advanced Organic Chemistry",
            "Baeyer & Villiger, 1899"
        ],
        burden_holder="Proponent of Baeyer-Villiger oxidation",
        adversary_position="Alternative oxidation or rearrangement",
        counter_arguments=[
            "Competing overoxidation or hydrolysis",
            "Low migratory aptitude reduces yield"
        ],
        resolution_strategy="Select appropriate peracid; control temperature; confirm product by NMR and IR.",
        entity_scope="Ketones and peracids",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Baeyer & Villiger, 1899"
    ),
    DoctrineBlock(
        topic="Michael_Addition",
        keywords=["conjugate addition", "enolate", "α,β-unsaturated carbonyl", "soft nucleophile", "1,4-addition"],
        conclusion_template="Michael addition involves 1,4-conjugate addition of nucleophiles to α,β-unsaturated carbonyls.",
        reasoning_framework="""
Michael addition is a conjugate (1,4) addition of a nucleophile (often an enolate) to an α,β-unsaturated carbonyl compound. The reaction is catalyzed by base and is highly regioselective. Soft nucleophiles (e.g., thiols, amines) are particularly effective. The reaction is widely used in C–C bond formation and in the synthesis of complex molecules.
        """,
        key_factors=[
            "Nucleophile softness and reactivity",
            "Electrophile activation (α,β-unsaturated carbonyl)",
            "Base catalysis",
            "Regioselectivity (1,4 vs 1,2 addition)",
            "Functional group compatibility"
        ],
        primary_authority=[
            "Michael, A.: J. Prakt. Chem. 1887",
            "March's Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of Michael addition",
        adversary_position="Direct (1,2) addition predominates",
        counter_arguments=[
            "Hard nucleophiles favor 1,2 addition",
            "Steric hindrance reduces yield"
        ],
        resolution_strategy="Select soft nucleophile and base; confirm product by NMR and MS.",
        entity_scope="Enolates, α,β-unsaturated carbonyls",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Michael, 1887"
    ),
    DoctrineBlock(
        topic="Claisen_Condensation",
        keywords=["enolate", "ester", "β-ketoester", "base", "self-condensation", "crossed Claisen"],
        conclusion_template="Claisen condensation forms β-ketoesters or β-diketones via enolate addition to esters.",
        reasoning_framework="""
Claisen condensation involves the base-catalyzed reaction of an ester with an enolate to form a β-ketoester or β-diketone. The reaction requires at least one α-hydrogen and is typically carried out with alkoxide bases. Crossed Claisen condensations use two different esters, at least one lacking α-hydrogens to prevent self-condensation. The reaction is quenched with acid to neutralize the enolate.
        """,
        key_factors=[
            "Ester structure and α-hydrogen presence",
            "Base choice (alkoxide matching ester)",
            "Self vs crossed condensation",
            "Reaction conditions",
            "Product workup"
        ],
        primary_authority=[
            "Claisen, L.: Ber. Dtsch. Chem. Ges. 1887",
            "March's Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of Claisen condensation",
        adversary_position="Competing self-condensation or hydrolysis",
        counter_arguments=[
            "Lack of α-hydrogen prevents enolate formation",
            "Side reactions with incompatible bases"
        ],
        resolution_strategy="Use esters with appropriate α-hydrogens; match base to ester; confirm product by NMR.",
        entity_scope="Esters and enolates",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Claisen, 1887"
    ),
    DoctrineBlock(
        topic="Cannizzaro_Reaction",
        keywords=["aldehyde", "no α-hydrogen", "disproportionation", "base", "alcohol", "carboxylate"],
        conclusion_template="Cannizzaro reaction disproportionates non-enolizable aldehydes to alcohol and carboxylate under basic conditions.",
        reasoning_framework="""
The Cannizzaro reaction involves the base-induced disproportionation of aldehydes lacking α-hydrogens. One molecule is reduced to an alcohol, the other oxidized to a carboxylate. The reaction proceeds via hydride transfer between two aldehyde molecules. It is limited to non-enolizable aldehydes (e.g., benzaldehyde).
        """,
        key_factors=[
            "Aldehyde structure (no α-hydrogen)",
            "Base strength (concentrated alkali)",
            "Reaction stoichiometry",
            "Product separation",
            "Functional group compatibility"
        ],
        primary_authority=[
            "Cannizzaro, S.: Gazz. Chim. Ital. 1853",
            "March's Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of Cannizzaro reaction",
        adversary_position="Aldol condensation predominates",
        counter_arguments=[
            "Aldehydes with α-hydrogens undergo aldol condensation",
            "Side reactions with sensitive substrates"
        ],
        resolution_strategy="Select appropriate aldehyde; control base and temperature; confirm by NMR and IR.",
        entity_scope="Non-enolizable aldehydes",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Cannizzaro, 1853"
    ),
    DoctrineBlock(
        topic="Sandmeyer_Reaction",
        keywords=["diazonium salt", "aromatic substitution", "copper(I) catalyst", "halogenation", "cyanation", "Sandmeyer"],
        conclusion_template="Sandmeyer reaction replaces aromatic amines with halides or cyano groups via diazonium salts and copper(I) salts.",
        reasoning_framework="""
The Sandmeyer reaction uses aromatic diazonium salts, generated from primary aromatic amines, and copper(I) salts to introduce halides or cyano groups onto aromatic rings. The reaction is highly versatile for aromatic substitution. The diazonium salt is unstable and must be generated in situ. Side reactions include reduction or hydrolysis of diazonium intermediates.
        """,
        key_factors=[
            "Diazonium salt formation",
            "Copper(I) catalyst choice",
            "Substituent effects on aromatic ring",
            "Temperature and reaction control",
            "Product isolation"
        ],
        primary_authority=[
            "Sandmeyer, T.: Ber. Dtsch. Chem. Ges. 1884",
            "March's Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of Sandmeyer reaction",
        adversary_position="Alternative aromatic substitution",
        counter_arguments=[
            "Unstable diazonium salts may decompose",
            "Side reactions reduce yield"
        ],
        resolution_strategy="Generate diazonium salt in situ; control temperature; confirm product by NMR and MS.",
        entity_scope="Aromatic amines and diazonium salts",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Sandmeyer, 1884"
    ),
    DoctrineBlock(
        topic="Wolff_Kishner_Reduction",
        keywords=["hydrazone", "alkaline", "reduction", "alkane", "high temperature", "Wolff-Kishner"],
        conclusion_template="Wolff-Kishner reduction converts carbonyls to alkanes via hydrazone intermediates under basic conditions.",
        reasoning_framework="""
Wolff-Kishner reduction involves conversion of aldehydes or ketones to hydrazones, followed by heating with strong base to yield alkanes. The reaction requires high temperature and is compatible with base-stable substrates. Acid-sensitive groups are tolerated, but base-sensitive groups may be affected. The reaction is complementary to Clemmensen reduction (acidic conditions).
        """,
        key_factors=[
            "Hydrazone formation",
            "Base strength and temperature",
            "Substrate stability under basic conditions",
            "Functional group compatibility",
            "Product isolation"
        ],
        primary_authority=[
            "Wolff, L.; Kishner, N.: Ber. Dtsch. Chem. Ges. 1911",
            "March's Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of Wolff-Kishner reduction",
        adversary_position="Clemmensen reduction preferred",
        counter_arguments=[
            "High temperature may cause decomposition",
            "Base-sensitive groups are incompatible"
        ],
        resolution_strategy="Assess substrate compatibility; confirm by NMR and IR.",
        entity_scope="Aldehydes, ketones, hydrazones",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Wolff, 1911; Kishner, 1911"
    ),
    DoctrineBlock(
        topic="Clemmensen_Reduction",
        keywords=["zinc amalgam", "acidic", "reduction", "alkane", "Clemmensen", "carbonyl"],
        conclusion_template="Clemmensen reduction converts carbonyls to alkanes using zinc amalgam and hydrochloric acid.",
        reasoning_framework="""
Clemmensen reduction uses zinc amalgam and concentrated HCl to reduce aldehydes and ketones to alkanes. The reaction is performed under strongly acidic conditions and is suitable for acid-stable substrates. Base-sensitive groups are tolerated. The reaction is complementary to Wolff-Kishner reduction (basic conditions).
        """,
        key_factors=[
            "Substrate stability under acidic conditions",
            "Zinc amalgam preparation",
            "Reaction temperature",
            "Functional group compatibility",
            "Product isolation"
        ],
        primary_authority=[
            "Clemmensen, E.: Ber. Dtsch. Chem. Ges. 1913",
            "March's Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of Clemmensen reduction",
        adversary_position="Wolff-Kishner reduction preferred",
        counter_arguments=[
            "Acid-sensitive groups may decompose",
            "Preparation of zinc amalgam is hazardous"
        ],
        resolution_strategy="Assess substrate compatibility; confirm by NMR and IR.",
        entity_scope="Aldehydes, ketones",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Clemmensen, 1913"
    ),
    DoctrineBlock(
        topic="Hydroboration_Oxidation",
        keywords=["alkene", "anti-Markovnikov", "borane", "oxidation", "alcohol", "syn addition"],
        conclusion_template="Hydroboration-oxidation converts alkenes to alcohols with anti-Markovnikov regioselectivity and syn stereochemistry.",
        reasoning_framework="""
Hydroboration-oxidation involves addition of borane to an alkene (syn addition), followed by oxidation with hydrogen peroxide to yield an alcohol. The reaction proceeds with anti-Markovnikov regioselectivity due to boron addition to the less substituted carbon. The process is stereospecific and avoids carbocation rearrangement.
        """,
        key_factors=[
            "Alkene structure",
            "Borane reagent choice",
            "Reaction conditions",
            "Regio- and stereoselectivity",
            "Functional group compatibility"
        ],
        primary_authority=[
            "Brown, H.C.: Nobel Lecture (1979)",
            "March's Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of hydroboration-oxidation",
        adversary_position="Acid-catalyzed hydration preferred",
        counter_arguments=[
            "Sterically hindered alkenes react slowly",
            "Borane reagents require careful handling"
        ],
        resolution_strategy="Select appropriate borane; confirm product by NMR and IR.",
        entity_scope="Alkenes and borane reagents",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Brown, 1956; Nobel Prize 1979"
    ),
    DoctrineBlock(
        topic="Ozonolysis",
        keywords=["alkene", "ozone", "oxidative cleavage", "carbonyl", "reductive workup", "ozonide"],
        conclusion_template="Ozonolysis cleaves alkenes to carbonyl compounds via ozonide intermediates and reductive or oxidative workup.",
        reasoning_framework="""
Ozonolysis involves the reaction of ozone with alkenes to form ozonides, which are then cleaved by reductive (e.g., Zn/AcOH, DMS) or oxidative (e.g., H2O2) workup to yield aldehydes, ketones, or carboxylic acids. The reaction is highly regioselective and used for structure determination and synthesis. Ozone is hazardous and must be handled with care.
        """,
        key_factors=[
            "Alkene structure",
            "Ozone generation and handling",
            "Workup conditions (reductive vs oxidative)",
            "Product analysis",
            "Safety precautions"
        ],
        primary_authority=[
            "Harries, C.: Ber. Dtsch. Chem. Ges. 1905",
            "March's Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of ozonolysis",
        adversary_position="Alternative oxidative cleavage methods",
        counter_arguments=[
            "Ozone is hazardous and requires special equipment",
            "Overoxidation may occur with sensitive substrates"
        ],
        resolution_strategy="Use proper safety protocols; confirm product by NMR and IR.",
        entity_scope="Alkenes and ozone",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Harries, 1905"
    ),
    DoctrineBlock(
        topic="Markovnikov_vs_AntiMarkovnikov_Addition",
        keywords=["alkene", "regioselectivity", "Markovnikov", "anti-Markovnikov", "carbocation", "peroxide effect"],
        conclusion_template="Markovnikov addition places the electrophile on the more substituted carbon, while anti-Markovnikov reverses this under radical conditions.",
        reasoning_framework="""
Markovnikov's rule states that in the addition of HX to an alkene, the hydrogen attaches to the carbon with more hydrogens (less substituted), and the halide to the more substituted carbon. This is due to carbocation stability. In the presence of peroxides, radical mechanisms (anti-Markovnikov) predominate, with the halide adding to the less substituted carbon. The outcome depends on reagent, solvent, and presence of initiators.
        """,
        key_factors=[
            "Alkene substitution pattern",
            "Nature of reagent (HX, peroxides)",
            "Reaction conditions",
            "Radical vs ionic mechanism",
            "Product analysis"
        ],
        primary_authority=[
            "Markovnikov, V.: J. Prakt. Chem. 1870",
            "March's Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of regioselectivity assignment",
        adversary_position="Opposite regioisomer predominates",
        counter_arguments=[
            "Peroxide effect only applies to HBr",
            "Steric and electronic effects may alter outcome"
        ],
        resolution_strategy="Control reaction conditions; confirm product by NMR and GC.",
        entity_scope="Alkenes and addition reagents",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Markovnikov, 1870; Kharasch peroxide effect"
    ),
    DoctrineBlock(
        topic="Tautomerism_Keto_Enol",
        keywords=["keto-enol", "tautomerism", "proton transfer", "enolate", "acid/base catalysis", "equilibrium"],
        conclusion_template="Keto-enol tautomerism is a dynamic equilibrium between carbonyl and enol forms, catalyzed by acid or base.",
        reasoning_framework="""
Keto-enol tautomerism involves proton transfer between the α-carbon and carbonyl oxygen, interconverting keto and enol forms. The equilibrium is typically toward the keto form, but enol content increases with conjugation or hydrogen bonding. Acid or base catalysis accelerates tautomerization. Tautomerism affects reactivity (e.g., enolization in aldol reactions) and NMR spectra.
        """,
        key_factors=[
            "Substrate structure and conjugation",
            "Catalysis (acid or base)",
            "Solvent effects",
            "Temperature",
            "Analytical methods (NMR, IR)"
        ],
        primary_authority=[
            "March's Advanced Organic Chemistry",
            "Carey & Sundberg: Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of tautomeric equilibrium",
        adversary_position="Single dominant tautomer",
        counter_arguments=[
            "Steric or electronic effects may suppress enolization",
            "Solvent and temperature alter equilibrium"
        ],
        resolution_strategy="Analyze by NMR and IR; control conditions to favor desired tautomer.",
        entity_scope="Carbonyl compounds with α-hydrogens",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Liebig, 1835; Modern NMR studies"
    ),
    DoctrineBlock(
        topic="Reformatsky_Reaction",
        keywords=["α-haloester", "zinc", "organometallic", "carbonyl addition", "β-hydroxyester", "Reformatsky"],
        conclusion_template="Reformatsky reaction forms β-hydroxyesters by zinc-mediated addition of α-haloesters to carbonyls.",
        reasoning_framework="""
The Reformatsky reaction uses zinc to generate organozinc reagents from α-haloesters, which add to aldehydes or ketones to form β-hydroxyesters. The reaction is milder than Grignard addition and compatible with many functional groups. Side reactions include reduction or self-condensation. The reaction is quenched with acid to release the product.
        """,
        key_factors=[
            "α-Haloester and carbonyl structure",
            "Zinc activation",
            "Reaction conditions (solvent, temperature)",
            "Functional group compatibility",
            "Product workup"
        ],
        primary_authority=[
            "Reformatsky, S.: Z. Chem. 1887",
            "March's Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of Reformatsky reaction",
        adversary_position="Grignard or other organometallic addition",
        counter_arguments=[
            "Inert zinc or poor activation reduces yield",
            "Competing side reactions"
        ],
        resolution_strategy="Use activated zinc; control conditions; confirm product by NMR and IR.",
        entity_scope="α-Haloesters, aldehydes, ketones",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Reformatsky, 1887"
    ),
    DoctrineBlock(
        topic="Gabriel_Synthesis",
        keywords=["phthalimide", "alkylation", "primary amine", "hydrazinolysis", "Gabriel", "nucleophilic substitution"],
        conclusion_template="Gabriel synthesis prepares primary amines by alkylation of phthalimide followed by hydrolysis or hydrazinolysis.",
        reasoning_framework="""
Gabriel synthesis involves nucleophilic substitution of phthalimide anion with alkyl halides, followed by hydrolysis or hydrazinolysis to release the primary amine. The method avoids overalkylation and is selective for primary amines. Secondary and tertiary amines are not accessible. The reaction is limited by the reactivity of the alkyl halide and conditions for phthalimide cleavage.
        """,
        key_factors=[
            "Alkyl halide reactivity",
            "Phthalimide activation",
            "Hydrolysis or hydrazinolysis conditions",
            "Selectivity for primary amines",
            "Functional group compatibility"
        ],
        primary_authority=[
            "Gabriel, S.: Ber. Dtsch. Chem. Ges. 1887",
            "March's Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of Gabriel synthesis",
        adversary_position="Alternative amine synthesis (e.g., reductive amination)",
        counter_arguments=[
            "Unreactive alkyl halides give low yield",
            "Side reactions during hydrolysis"
        ],
        resolution_strategy="Select reactive alkyl halide; optimize cleavage conditions; confirm product by NMR.",
        entity_scope="Phthalimide, alkyl halides",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Gabriel, 1887"
    ),
    DoctrineBlock(
        topic="Mannich_Reaction",
        keywords=["aminoalkylation", "enolizable carbonyl", "formaldehyde", "amine", "Mannich base", "β-amino carbonyl"],
        conclusion_template="Mannich reaction forms β-amino carbonyl compounds by condensation of an enolizable carbonyl, formaldehyde, and amine.",
        reasoning_framework="""
The Mannich reaction condenses an enolizable carbonyl compound, formaldehyde, and a primary or secondary amine to yield a β-amino carbonyl (Mannich base). The reaction is catalyzed by acid or base and is widely used in alkaloid and pharmaceutical synthesis. The process is regioselective and compatible with various functional groups.
        """,
        key_factors=[
            "Enolizable carbonyl structure",
            "Amine and formaldehyde reactivity",
            "Reaction conditions (acid/base catalysis)",
            "Regioselectivity",
            "Product isolation"
        ],
        primary_authority=[
            "Mannich, C.: Ber. Dtsch. Chem. Ges. 1912",
            "March's Advanced Organic Chemistry"
        ],
        burden_holder="Proponent of Mannich reaction",
        adversary_position="Alternative C–N bond-forming methods",
        counter_arguments=[
            "Non-enolizable carbonyls do not react",
            "Side reactions with excess formaldehyde"
        ],
        resolution_strategy="Select appropriate substrates; control stoichiometry; confirm product by NMR and IR.",
        entity_scope="Enolizable carbonyls, amines, formaldehyde",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Mannich, 1912"
    ),
    DoctrineBlock(
        topic="Bromination_of_