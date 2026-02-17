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
        topic="protein_primary_structure",
        keywords=["amino acid sequence", "peptide bond", "N-terminus", "C-terminus", "primary structure"],
        conclusion_template="The primary structure of a protein is determined by its unique sequence of amino acids linked by peptide bonds.",
        reasoning_framework=(
            "The primary structure of a protein refers to the linear sequence of amino acids as encoded by the corresponding gene. "
            "Each amino acid is joined to the next via a peptide bond, forming a polypeptide chain. "
            "The order of amino acids determines all higher levels of protein structure and ultimately its function. "
            "The N-terminus is the start of the chain (with a free amino group), and the C-terminus is the end (with a free carboxyl group). "
            "Mutations that alter the amino acid sequence can have profound effects on protein folding and function. "
            "Primary structure is established during translation and is invariant unless altered by mutation or post-translational modification. "
            "Analytical techniques such as Edman degradation and mass spectrometry can be used to determine primary structure. "
            "The central dogma of molecular biology (DNA -> RNA -> Protein) underpins the determination of primary structure. "
            "The sequence is read from the N-terminus to the C-terminus. "
            "Errors in primary structure can lead to diseases such as sickle cell anemia, where a single amino acid substitution causes pathology."
        ),
        key_factors=[
            "Amino acid sequence",
            "Peptide bond formation",
            "Genetic code",
            "N-terminus and C-terminus orientation",
            "Mutation impact"
        ],
        primary_authority=["Lehninger Principles of Biochemistry", "Alberts Molecular Biology of the Cell"],
        burden_holder="Proponent of sequence-function relationship",
        adversary_position="Primary structure is not always determinative of function",
        counter_arguments=[
            "Post-translational modifications can alter function",
            "Chaperones may assist folding beyond sequence information"
        ],
        resolution_strategy="Emphasize that while primary structure is necessary, higher-order structures and modifications also contribute to function.",
        entity_scope="All proteins",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Sanger sequencing of insulin (1952)"
    ),
    DoctrineBlock(
        topic="protein_secondary_structure",
        keywords=["alpha helix", "beta sheet", "hydrogen bond", "secondary structure", "Ramachandran plot"],
        conclusion_template="Secondary structure in proteins arises from regular hydrogen bonding patterns, forming alpha helices and beta sheets.",
        reasoning_framework=(
            "Secondary structure refers to local regions of regular folding within a polypeptide, stabilized by hydrogen bonds between backbone amide and carbonyl groups. "
            "The most common secondary structures are the alpha helix and the beta sheet. "
            "Alpha helices are right-handed coils stabilized by hydrogen bonds every fourth residue. "
            "Beta sheets consist of beta strands connected laterally by at least two or three backbone hydrogen bonds, forming a sheet-like array. "
            "The Ramachandran plot describes the allowable phi and psi angles for amino acid residues, predicting possible secondary structures. "
            "Proline and glycine residues often disrupt secondary structures due to their unique conformational properties. "
            "Secondary structure elements are detected by X-ray crystallography, NMR, and circular dichroism spectroscopy. "
            "Secondary structure formation is an early step in protein folding and is critical for proper tertiary structure."
        ),
        key_factors=[
            "Hydrogen bonding",
            "Amino acid sequence",
            "Steric constraints",
            "Ramachandran plot",
            "Disruptive residues"
        ],
        primary_authority=["Pauling & Corey (1951)", "Branden & Tooze: Introduction to Protein Structure"],
        burden_holder="Proponent of secondary structure's role in folding",
        adversary_position="Secondary structure is not always present or regular",
        counter_arguments=[
            "Intrinsically disordered proteins lack regular secondary structure",
            "Loops and turns are also important structural elements"
        ],
        resolution_strategy="Acknowledge exceptions but emphasize the prevalence and importance of alpha helices and beta sheets.",
        entity_scope="Globular and fibrous proteins",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Pauling and Corey's discovery of alpha helix and beta sheet"
    ),
    DoctrineBlock(
        topic="protein_tertiary_structure",
        keywords=["3D folding", "hydrophobic effect", "disulfide bond", "tertiary structure", "protein domains"],
        conclusion_template="Tertiary structure is the overall three-dimensional shape of a protein, stabilized by various interactions among side chains.",
        reasoning_framework=(
            "Tertiary structure describes the complete three-dimensional conformation of a single polypeptide chain, including all its secondary structure elements and loops. "
            "It is stabilized by hydrophobic interactions, hydrogen bonds, ionic interactions, van der Waals forces, and covalent disulfide bonds. "
            "The hydrophobic effect drives nonpolar side chains to the protein's interior, while polar and charged residues are generally exposed to the solvent. "
            "Disulfide bonds between cysteine residues can further stabilize the folded structure, especially in extracellular proteins. "
            "Protein domains are distinct structural and functional units within a tertiary structure. "
            "Proper folding is essential for biological activity; misfolding can lead to aggregation and diseases such as Alzheimer's. "
            "Chaperone proteins assist in correct folding in vivo. "
            "Tertiary structure is determined by X-ray crystallography, NMR, and cryo-electron microscopy."
        ),
        key_factors=[
            "Hydrophobic effect",
            "Disulfide bonds",
            "Ionic and hydrogen bonding",
            "Protein domains",
            "Chaperone involvement"
        ],
        primary_authority=["Lehninger Principles of Biochemistry", "Branden & Tooze"],
        burden_holder="Proponent of sequence-determined folding",
        adversary_position="Folding is not always spontaneous or sequence-determined",
        counter_arguments=[
            "Chaperones are sometimes required",
            "Environmental factors can influence folding"
        ],
        resolution_strategy="Clarify that while sequence encodes structure, cellular context and chaperones can be essential.",
        entity_scope="All polypeptides",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Anfinsen's dogma (1973)"
    ),
    DoctrineBlock(
        topic="protein_quaternary_structure",
        keywords=["subunit", "oligomer", "multimer", "quaternary structure", "allosteric regulation"],
        conclusion_template="Quaternary structure refers to the arrangement and interaction of multiple polypeptide subunits in a protein complex.",
        reasoning_framework=(
            "Quaternary structure arises when two or more polypeptide chains (subunits) associate to form a functional protein complex. "
            "Subunits can be identical (homooligomers) or different (heterooligomers). "
            "Interactions stabilizing quaternary structure include hydrophobic interactions, hydrogen bonds, ionic bonds, and sometimes disulfide bridges. "
            "Allosteric regulation often depends on quaternary structure, as seen in hemoglobin. "
            "Quaternary structure enables cooperative binding, regulation, and complex functionality not possible in monomeric proteins. "
            "Dissociation of subunits can lead to loss of function. "
            "Analytical techniques include gel filtration, ultracentrifugation, and X-ray crystallography."
        ),
        key_factors=[
            "Subunit composition",
            "Inter-subunit interactions",
            "Allosteric effects",
            "Cooperativity",
            "Analytical detection"
        ],
        primary_authority=["Alberts Molecular Biology of the Cell", "Lehninger Principles of Biochemistry"],
        burden_holder="Proponent of functional importance of quaternary structure",
        adversary_position="Some proteins function as monomers",
        counter_arguments=[
            "Monomeric proteins do not require quaternary structure",
            "Not all complexes are stable in vivo"
        ],
        resolution_strategy="Acknowledge monomeric proteins but emphasize the regulatory and functional advantages of quaternary structure.",
        entity_scope="Multimeric proteins",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Perutz and Kendrew's work on hemoglobin (1960)"
    ),
    DoctrineBlock(
        topic="enzyme_kinetics_michaelis_menten",
        keywords=["enzyme kinetics", "Michaelis-Menten", "Km", "Vmax", "substrate saturation"],
        conclusion_template="The Michaelis-Menten model describes the rate of enzymatic reactions as a function of substrate concentration.",
        reasoning_framework=(
            "The Michaelis-Menten equation models the initial velocity (v) of an enzyme-catalyzed reaction as v = (Vmax [S]) / (Km + [S]), "
            "where [S] is substrate concentration, Vmax is the maximum velocity, and Km is the substrate concentration at half-maximal velocity. "
            "The model assumes rapid formation and breakdown of the enzyme-substrate complex and that product formation is the rate-limiting step. "
            "Km reflects the affinity of the enzyme for its substrate; a lower Km indicates higher affinity. "
            "Vmax is proportional to the total enzyme concentration. "
            "The Lineweaver-Burk plot (double reciprocal) is used to linearize the data for parameter estimation. "
            "Michaelis-Menten kinetics are valid under steady-state conditions and for simple (non-allosteric) enzymes."
        ),
        key_factors=[
            "Substrate concentration",
            "Enzyme concentration",
            "Km and Vmax values",
            "Steady-state assumption",
            "Experimental design"
        ],
        primary_authority=["Michaelis & Menten (1913)", "Lehninger Principles of Biochemistry"],
        burden_holder="Proponent of Michaelis-Menten applicability",
        adversary_position="Many enzymes do not follow Michaelis-Menten kinetics",
        counter_arguments=[
            "Allosteric enzymes show sigmoidal kinetics",
            "Enzyme inhibition and cooperativity complicate the model"
        ],
        resolution_strategy="Apply Michaelis-Menten only to appropriate systems; use alternative models for allosteric enzymes.",
        entity_scope="Simple, non-allosteric enzymes",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Michaelis-Menten original paper (1913)"
    ),
    DoctrineBlock(
        topic="enzyme_inhibition",
        keywords=["competitive inhibition", "noncompetitive inhibition", "uncompetitive inhibition", "enzyme inhibitor", "reversible inhibition"],
        conclusion_template="Enzyme inhibition can be classified as competitive, noncompetitive, or uncompetitive, each affecting kinetic parameters differently.",
        reasoning_framework=(
            "Enzyme inhibitors decrease the rate of enzymatic reactions. "
            "Competitive inhibitors bind to the active site, preventing substrate binding; they increase Km but do not affect Vmax. "
            "Noncompetitive inhibitors bind to an allosteric site, reducing Vmax without affecting Km. "
            "Uncompetitive inhibitors bind only to the enzyme-substrate complex, decreasing both Km and Vmax. "
            "Inhibition can be reversible or irreversible. "
            "Kinetic analysis (e.g., Lineweaver-Burk plots) distinguishes between types of inhibition. "
            "Understanding inhibition is critical for drug design and metabolic regulation."
        ),
        key_factors=[
            "Type of inhibitor",
            "Binding site",
            "Effect on Km and Vmax",
            "Reversibility",
            "Experimental evidence"
        ],
        primary_authority=["Lehninger Principles of Biochemistry", "Berg, Tymoczko & Stryer: Biochemistry"],
        burden_holder="Proponent of inhibition classification",
        adversary_position="Some inhibitors do not fit classic categories",
        counter_arguments=[
            "Mixed inhibition displays characteristics of multiple types",
            "Allosteric regulation can complicate analysis"
        ],
        resolution_strategy="Use kinetic data to classify inhibition and acknowledge mixed mechanisms.",
        entity_scope="All enzymes",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Lineweaver and Burk (1934)"
    ),
    DoctrineBlock(
        topic="allosteric_regulation",
        keywords=["allosteric enzyme", "cooperativity", "sigmoidal kinetics", "allosteric site", "modulator"],
        conclusion_template="Allosteric regulation involves effector molecules binding at sites other than the active site, altering enzyme activity.",
        reasoning_framework=(
            "Allosteric enzymes have multiple binding sites, including the active site and one or more allosteric sites. "
            "Binding of effectors (activators or inhibitors) to allosteric sites induces conformational changes that alter enzyme activity. "
            "Allosteric regulation enables fine-tuned control of metabolic pathways. "
            "Cooperativity, where substrate binding at one site affects binding at others, leads to sigmoidal (S-shaped) kinetics. "
            "The Monod-Wyman-Changeux (MWC) and Koshland-Némethy-Filmer (KNF) models describe allosteric transitions. "
            "Allosteric regulation is common in key metabolic enzymes (e.g., phosphofructokinase-1 in glycolysis)."
        ),
        key_factors=[
            "Presence of allosteric sites",
            "Effector molecules",
            "Cooperativity",
            "Kinetic behavior",
            "Structural evidence"
        ],
        primary_authority=["Monod, Wyman & Changeux (1965)", "Lehninger Principles of Biochemistry"],
        burden_holder="Proponent of allosteric regulation",
        adversary_position="Not all enzymes are allosteric",
        counter_arguments=[
            "Some enzymes are regulated only by substrate concentration",
            "Allosteric effects can be subtle or context-dependent"
        ],
        resolution_strategy="Identify allosteric enzymes by sigmoidal kinetics and effector response.",
        entity_scope="Multisubunit enzymes",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Monod-Wyman-Changeux model (1965)"
    ),
    DoctrineBlock(
        topic="glycolysis",
        keywords=["glycolysis", "glucose metabolism", "Embden-Meyerhof pathway", "ATP production", "pyruvate"],
        conclusion_template="Glycolysis is a ten-step pathway converting glucose to pyruvate, generating ATP and NADH.",
        reasoning_framework=(
            "Glycolysis occurs in the cytoplasm and is the central pathway for glucose catabolism. "
            "It consists of ten enzyme-catalyzed steps, divided into an investment phase (uses 2 ATP) and a payoff phase (produces 4 ATP and 2 NADH). "
            "The net yield per glucose is 2 ATP and 2 NADH. "
            "Key regulatory steps include hexokinase/glucokinase, phosphofructokinase-1 (PFK-1), and pyruvate kinase. "
            "Glycolysis functions under both aerobic and anaerobic conditions. "
            "Under anaerobic conditions, pyruvate is converted to lactate (in animals) or ethanol (in yeast). "
            "Glycolysis provides intermediates for biosynthetic pathways."
        ),
        key_factors=[
            "Enzyme regulation",
            "ATP and NADH yield",
            "Aerobic vs anaerobic fate",
            "Pathway intermediates",
            "Tissue specificity"
        ],
        primary_authority=["Lehninger Principles of Biochemistry", "Berg, Tymoczko & Stryer"],
        burden_holder="Proponent of glycolysis as universal pathway",
        adversary_position="Some cells preferentially use other pathways",
        counter_arguments=[
            "Neurons rely heavily on glycolysis",
            "Some tissues (e.g., liver) favor gluconeogenesis under certain conditions"
        ],
        resolution_strategy="Emphasize glycolysis as a central, but not exclusive, pathway.",
        entity_scope="All cells",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Embden-Meyerhof pathway elucidation (1930s)"
    ),
    DoctrineBlock(
        topic="tca_cycle",
        keywords=["TCA cycle", "Krebs cycle", "citric acid cycle", "acetyl-CoA", "NADH", "FADH2"],
        conclusion_template="The TCA cycle oxidizes acetyl-CoA to CO2, generating NADH, FADH2, and GTP for energy production.",
        reasoning_framework=(
            "The tricarboxylic acid (TCA) cycle, also known as the Krebs or citric acid cycle, occurs in the mitochondrial matrix. "
            "It begins with the condensation of acetyl-CoA and oxaloacetate to form citrate. "
            "Through a series of eight steps, acetyl groups are fully oxidized to CO2. "
            "The cycle produces 3 NADH, 1 FADH2, and 1 GTP (or ATP) per acetyl-CoA. "
            "NADH and FADH2 donate electrons to the electron transport chain, driving oxidative phosphorylation. "
            "The TCA cycle is amphibolic, providing intermediates for biosynthesis as well as energy production. "
            "Key regulatory enzymes include citrate synthase, isocitrate dehydrogenase, and alpha-ketoglutarate dehydrogenase."
        ),
        key_factors=[
            "Acetyl-CoA input",
            "NADH and FADH2 output",
            "CO2 production",
            "Regulatory enzymes",
            "Mitochondrial localization"
        ],
        primary_authority=["Hans Krebs (1937)", "Lehninger Principles of Biochemistry"],
        burden_holder="Proponent of TCA as central metabolic hub",
        adversary_position="Some cells lack a complete TCA cycle",
        counter_arguments=[
            "Red blood cells lack mitochondria and TCA cycle",
            "Some anaerobic organisms use alternative pathways"
        ],
        resolution_strategy="Acknowledge exceptions but affirm TCA cycle's centrality in aerobic metabolism.",
        entity_scope="Aerobic cells",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Krebs' elucidation of the cycle (1937)"
    ),
    DoctrineBlock(
        topic="oxidative_phosphorylation",
        keywords=["electron transport chain", "ATP synthase", "proton gradient", "mitochondria", "chemiosmosis"],
        conclusion_template="Oxidative phosphorylation couples electron transport to ATP synthesis via a proton gradient across the mitochondrial membrane.",
        reasoning_framework=(
            "Oxidative phosphorylation occurs in the inner mitochondrial membrane. "
            "Electrons from NADH and FADH2 are transferred through complexes I-IV of the electron transport chain, ultimately reducing oxygen to water. "
            "Electron transfer is coupled to the pumping of protons from the matrix to the intermembrane space, creating an electrochemical gradient (proton motive force). "
            "ATP synthase (Complex V) uses the energy stored in this gradient to synthesize ATP from ADP and Pi. "
            "The process is described by the chemiosmotic hypothesis (Peter Mitchell, 1961). "
            "Inhibitors (e.g., cyanide, oligomycin) and uncouplers (e.g., DNP) disrupt oxidative phosphorylation. "
            "The majority of cellular ATP is generated by this process under aerobic conditions."
        ),
        key_factors=[
            "Electron donors (NADH, FADH2)",
            "Proton gradient",
            "ATP synthase activity",
            "Oxygen availability",
            "Inhibitors and uncouplers"
        ],
        primary_authority=["Peter Mitchell (1961)", "Lehninger Principles of Biochemistry"],
        burden_holder="Proponent of chemiosmotic coupling",
        adversary_position="Alternative mechanisms proposed historically",
        counter_arguments=[
            "Substrate-level phosphorylation occurs independently",
            "Some bacteria use different electron acceptors"
        ],
        resolution_strategy="Highlight experimental support for chemiosmotic hypothesis in eukaryotes.",
        entity_scope="Aerobic eukaryotes",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Mitchell's chemiosmotic hypothesis (1961)"
    ),
    DoctrineBlock(
        topic="gluconeogenesis",
        keywords=["gluconeogenesis", "glucose synthesis", "liver", "non-carbohydrate precursors", "regulation"],
        conclusion_template="Gluconeogenesis synthesizes glucose from non-carbohydrate precursors, primarily in the liver.",
        reasoning_framework=(
            "Gluconeogenesis is the metabolic pathway that generates glucose from non-carbohydrate sources such as lactate, glycerol, and glucogenic amino acids. "
            "It occurs mainly in the liver and, to a lesser extent, in the kidney cortex. "
            "Gluconeogenesis shares several enzymes with glycolysis but bypasses the irreversible steps via unique enzymes: pyruvate carboxylase, PEP carboxykinase, fructose-1,6-bisphosphatase, and glucose-6-phosphatase. "
            "The pathway is energetically expensive, requiring 6 high-energy phosphate bonds per glucose molecule. "
            "Regulation is reciprocal with glycolysis, ensuring that both pathways are not highly active simultaneously. "
            "Hormonal control (insulin, glucagon, cortisol) modulates gluconeogenic activity."
        ),
        key_factors=[
            "Substrate availability",
            "Enzyme regulation",
            "Hormonal control",
            "Energy requirements",
            "Tissue specificity"
        ],
        primary_authority=["Lehninger Principles of Biochemistry", "Berg, Tymoczko & Stryer"],
        burden_holder="Proponent of gluconeogenesis as essential for glucose homeostasis",
        adversary_position="Some animals lack complete gluconeogenesis",
        counter_arguments=[
            "Obligate carnivores have limited gluconeogenic capacity",
            "Fasting and diabetes alter pathway flux"
        ],
        resolution_strategy="Emphasize the physiological importance in humans and most mammals.",
        entity_scope="Liver and kidney cortex",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Cori cycle elucidation (1930s)"
    ),
    DoctrineBlock(
        topic="fatty_acid_oxidation",
        keywords=["beta-oxidation", "fatty acid catabolism", "mitochondria", "acetyl-CoA", "energy production"],
        conclusion_template="Fatty acid oxidation (beta-oxidation) breaks down fatty acids to acetyl-CoA, generating NADH and FADH2.",
        reasoning_framework=(
            "Fatty acid oxidation occurs primarily in the mitochondrial matrix. "
            "Fatty acids are activated to acyl-CoA and transported into mitochondria via the carnitine shuttle. "
            "Beta-oxidation involves sequential removal of two-carbon units as acetyl-CoA, with each cycle generating one NADH and one FADH2. "
            "Acetyl-CoA enters the TCA cycle, and NADH/FADH2 feed into oxidative phosphorylation. "
            "Regulation occurs at the level of fatty acid entry into mitochondria and by hormonal signals (e.g., glucagon, epinephrine). "
            "Peroxisomal beta-oxidation handles very-long-chain fatty acids."
        ),
        key_factors=[
            "Carnitine shuttle",
            "Enzyme activity",
            "Hormonal regulation",
            "Energy yield",
            "Tissue specificity"
        ],
        primary_authority=["Lehninger Principles of Biochemistry", "Nelson & Cox"],
        burden_holder="Proponent of beta-oxidation as major energy source",
        adversary_position="Carbohydrates are primary energy source in some tissues",
        counter_arguments=[
            "Brain relies on glucose except during starvation",
            "Red blood cells cannot oxidize fatty acids"
        ],
        resolution_strategy="Highlight tissue-specific roles and metabolic flexibility.",
        entity_scope="Mitochondria of most tissues",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Knoop's beta-oxidation hypothesis (1904)"
    ),
    DoctrineBlock(
        topic="fatty_acid_synthesis",
        keywords=["fatty acid synthesis", "acetyl-CoA carboxylase", "malonyl-CoA", "cytosol", "NADPH"],
        conclusion_template="Fatty acid synthesis builds long-chain fatty acids from acetyl-CoA and malonyl-CoA in the cytosol, using NADPH.",
        reasoning_framework=(
            "Fatty acid synthesis occurs in the cytosol, primarily in liver and adipose tissue. "
            "Acetyl-CoA is carboxylated to malonyl-CoA by acetyl-CoA carboxylase (rate-limiting step). "
            "Fatty acid synthase catalyzes the sequential addition of two-carbon units from malonyl-CoA to a growing acyl chain. "
            "NADPH provides reducing power. "
            "The process stops at palmitate (16:0), which can be further elongated or desaturated. "
            "Regulation is reciprocal with beta-oxidation and is controlled by insulin, citrate, and palmitoyl-CoA."
        ),
        key_factors=[
            "Acetyl-CoA and malonyl-CoA availability",
            "NADPH supply",
            "Enzyme regulation",
            "Hormonal control",
            "Subcellular localization"
        ],
        primary_authority=["Lehninger Principles of Biochemistry", "Berg, Tymoczko & Stryer"],
        burden_holder="Proponent of cytosolic fatty acid synthesis",
        adversary_position="Some fatty acid synthesis occurs in mitochondria",
        counter_arguments=[
            "Mitochondrial fatty acid synthesis is minor in mammals",
            "Plants and bacteria have different pathways"
        ],
        resolution_strategy="Clarify that cytosolic pathway is predominant in animals.",
        entity_scope="Liver and adipose cytosol",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Wakil's elucidation of fatty acid synthase (1960s)"
    ),
    DoctrineBlock(
        topic="amino_acid_metabolism",
        keywords=["amino acid catabolism", "transamination", "urea cycle", "essential amino acids", "nitrogen balance"],
        conclusion_template="Amino acid metabolism involves transamination, deamination, and disposal of nitrogen via the urea cycle.",
        reasoning_framework=(
            "Amino acids are metabolized for energy, biosynthesis, or excretion. "
            "Transamination transfers amino groups to alpha-ketoglutarate, forming glutamate. "
            "Deamination of glutamate releases ammonia, which is toxic and must be converted to urea in the liver. "
            "The urea cycle disposes of excess nitrogen. "
            "Essential amino acids cannot be synthesized de novo and must be obtained from the diet. "
            "Amino acid catabolism provides intermediates for gluconeogenesis or ketogenesis. "
            "Nitrogen balance reflects the equilibrium between intake and excretion."
        ),
        key_factors=[
            "Transamination and deamination",
            "Urea cycle function",
            "Dietary requirements",
            "Metabolic fates",
            "Nitrogen toxicity"
        ],
        primary_authority=["Lehninger Principles of Biochemistry", "Murray, Bender & Botham: Harper's Illustrated Biochemistry"],
        burden_holder="Proponent of urea cycle as main nitrogen disposal route",
        adversary_position="Alternative pathways exist in some organisms",
        counter_arguments=[
            "Ammonotelic and uricotelic animals use different strategies",
            "Liver failure impairs urea cycle"
        ],
        resolution_strategy="Emphasize urea cycle's role in mammals.",
        entity_scope="Mammalian liver",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Krebs-Henseleit urea cycle (1932)"
    ),
    DoctrineBlock(
        topic="purine_metabolism",
        keywords=["purine synthesis", "purine salvage", "gout", "PRPP", "uric acid"],
        conclusion_template="Purine metabolism encompasses de novo synthesis, salvage pathways, and degradation to uric acid.",
        reasoning_framework=(
            "Purines (adenine, guanine) are synthesized de novo from ribose-5-phosphate via the PRPP pathway. "
            "Salvage pathways recycle free purine bases, catalyzed by enzymes such as HGPRT. "
            "Defects in salvage (e.g., Lesch-Nyhan syndrome) lead to excess uric acid and neurological symptoms. "
            "Purine degradation produces uric acid, which is excreted in urine. "
            "Hyperuricemia can cause gout due to uric acid crystal deposition in joints. "
            "Regulation occurs at the PRPP amidotransferase step."
        ),
        key_factors=[
            "PRPP availability",
            "Salvage enzyme activity",
            "Uric acid excretion",
            "Genetic defects",
            "Clinical manifestations"
        ],
        primary_authority=["Lehninger Principles of Biochemistry", "Harper's Illustrated Biochemistry"],
        burden_holder="Proponent of salvage pathway importance",
        adversary_position="De novo synthesis predominates in some tissues",
        counter_arguments=[
            "Brain relies heavily on salvage pathways",
            "Overproduction or underexcretion of uric acid can have multiple causes"
        ],
        resolution_strategy="Balance discussion of synthesis and salvage; highlight clinical relevance.",
        entity_scope="All tissues",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Elion's work on purine analogs (1950s)"
    ),
    DoctrineBlock(
        topic="pyrimidine_metabolism",
        keywords=["pyrimidine synthesis", "orotic aciduria", "UMP synthase", "pyrimidine salvage", "thymidylate synthase"],
        conclusion_template="Pyrimidine metabolism includes de novo synthesis, salvage, and degradation, with distinct clinical implications.",
        reasoning_framework=(
            "Pyrimidines (cytosine, thymine, uracil) are synthesized de novo from carbamoyl phosphate and aspartate. "
            "The pathway proceeds through orotic acid, which is converted to UMP by UMP synthase. "
            "Deficiency of UMP synthase leads to orotic aciduria. "
            "Salvage pathways recycle pyrimidine bases. "
            "Thymidylate synthase is essential for dTMP synthesis, targeted by anticancer drugs (e.g., 5-fluorouracil). "
            "Pyrimidine degradation yields beta-alanine and beta-aminoisobutyrate, which are water-soluble and excreted."
        ),
        key_factors=[
            "Carbamoyl phosphate availability",
            "UMP synthase activity",
            "Salvage pathway function",
            "Thymidylate synthase",
            "Clinical disorders"
        ],
        primary_authority=["Lehninger Principles of Biochemistry", "Harper's Illustrated Biochemistry"],
        burden_holder="Proponent of de novo and salvage pathway balance",
        adversary_position="Some cells rely almost exclusively on salvage",
        counter_arguments=[
            "Rapidly dividing cells require robust de novo synthesis",
            "Defects in enzymes cause clinical syndromes"
        ],
        resolution_strategy="Discuss both pathways and their clinical importance.",
        entity_scope="All nucleated cells",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Elion and Hitchings' work on antimetabolites (1950s)"
    ),
    DoctrineBlock(
        topic="dna_replication",
        keywords=["DNA replication", "semiconservative", "DNA polymerase", "origin of replication", "Okazaki fragment"],
        conclusion_template="DNA replication is semiconservative, requiring DNA polymerases, primers, and coordinated synthesis of leading and lagging strands.",
        reasoning_framework=(
            "DNA replication ensures accurate transmission of genetic information. "
            "It is semiconservative: each daughter DNA contains one parental and one newly synthesized strand. "
            "Replication begins at origins and proceeds bidirectionally. "
            "DNA polymerases synthesize new DNA in the 5' to 3' direction, requiring an RNA primer. "
            "The leading strand is synthesized continuously; the lagging strand is synthesized discontinuously as Okazaki fragments. "
            "Helicase unwinds the double helix; primase lays down RNA primers; ligase joins Okazaki fragments. "
            "Proofreading and repair mechanisms ensure fidelity."
        ),
        key_factors=[
            "Origin recognition",
            "Polymerase activity",
            "Primer synthesis",
            "Strand coordination",
            "Proofreading"
        ],
        primary_authority=["Watson & Crick", "Alberts Molecular Biology of the Cell"],
        burden_holder="Proponent of semiconservative mechanism",
        adversary_position="Alternative mechanisms proposed historically",
        counter_arguments=[
            "Rolling circle and conservative replication in some viruses",
            "Replication errors and mutations"
        ],
        resolution_strategy="Emphasize experimental evidence for semiconservative replication in cells.",
        entity_scope="All dividing cells",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Meselson-Stahl experiment (1958)"
    ),
    DoctrineBlock(
        topic="dna_repair",
        keywords=["DNA repair", "nucleotide excision repair", "base excision repair", "mismatch repair", "mutagenesis"],
        conclusion_template="Multiple DNA repair pathways correct damage and maintain genomic integrity.",
        reasoning_framework=(
            "DNA is subject to damage from endogenous and exogenous sources. "
            "Base excision repair corrects small, non-helix-distorting lesions. "
            "Nucleotide excision repair removes bulky adducts and thymine dimers. "
            "Mismatch repair fixes replication errors. "
            "Double-strand breaks are repaired by homologous recombination or non-homologous end joining. "
            "Defects in repair pathways lead to diseases such as xeroderma pigmentosum and Lynch syndrome."
        ),
        key_factors=[
            "Type of DNA damage",
            "Repair pathway",
            "Enzyme activity",
            "Genetic defects",
            "Disease associations"
        ],
        primary_authority=["Alberts Molecular Biology of the Cell", "Lehninger Principles of Biochemistry"],
        burden_holder="Proponent of repair pathway specificity",
        adversary_position="Some damage escapes repair",
        counter_arguments=[
            "Error-prone repair can introduce mutations",
            "Cell cycle checkpoints and apoptosis mitigate damage"
        ],
        resolution_strategy="Discuss repair efficiency and consequences of failure.",
        entity_scope="All cells",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Lindahl, Modrich, Sancar Nobel Prize (2015)"
    ),
    DoctrineBlock(
        topic="transcription",
        keywords=["transcription", "RNA polymerase", "promoter", "mRNA synthesis", "regulation"],
        conclusion_template="Transcription synthesizes RNA from a DNA template, initiated at promoters and regulated by transcription factors.",
        reasoning_framework=(
            "Transcription is the process of copying genetic information from DNA to RNA. "
            "RNA polymerase binds to promoter regions and synthesizes RNA in the 5' to 3' direction. "
            "Initiation, elongation, and termination are distinct phases. "
            "Transcription factors and enhancers modulate gene expression. "
            "In eukaryotes, multiple RNA polymerases transcribe different classes of RNA. "
            "Regulation is complex, involving chromatin structure, epigenetic marks, and non-coding RNAs."
        ),
        key_factors=[
            "Promoter recognition",
            "Polymerase specificity",
            "Transcription factors",
            "Regulatory elements",
            "Epigenetic control"
        ],
        primary_authority=["Alberts Molecular Biology of the Cell", "Lewin's Genes"],
        burden_holder="Proponent of transcriptional regulation",
        adversary_position="Some genes are constitutively expressed",
        counter_arguments=[
            "Housekeeping genes have minimal regulation",
            "Post-transcriptional regulation also important"
        ],
        resolution_strategy="Highlight diversity of regulatory mechanisms.",
        entity_scope="All cells",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Jacob and Monod operon model (1961)"
    ),
    DoctrineBlock(
        topic="rna_processing",
        keywords=["RNA processing", "splicing", "5' cap", "polyadenylation", "alternative splicing"],
        conclusion_template="Eukaryotic pre-mRNA undergoes capping, splicing, and polyadenylation to become mature mRNA.",
        reasoning_framework=(
            "Primary RNA transcripts (pre-mRNA) in eukaryotes are processed before translation. "
            "A 5' methylguanosine cap is added for stability and ribosome recognition. "
            "Introns are removed and exons joined by the spliceosome. "
            "A poly(A) tail is added at the 3' end, enhancing stability and export. "
            "Alternative splicing allows one gene to produce multiple protein isoforms. "
            "Defects in processing can cause disease (e.g., beta-thalassemia)."
        ),
        key_factors=[
            "Splice site recognition",
            "Capping and polyadenylation enzymes",
            "Alternative splicing",
            "mRNA stability",
            "Disease associations"
        ],
        primary_authority=["Alberts Molecular Biology of the Cell", "Lewin's Genes"],
        burden_holder="Proponent of processing for functional mRNA",
        adversary_position="Prokaryotes lack extensive RNA processing",
        counter_arguments=[
            "Some non-coding RNAs are processed differently",
            "Processing errors can have severe consequences"
        ],
        resolution_strategy="Emphasize eukaryotic context and clinical relevance.",
        entity_scope="Eukaryotic cells",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Sharp and Roberts discovery of introns (1977)"
    ),
    DoctrineBlock(
        topic="translation",
        keywords=["translation", "ribosome", "tRNA", "codon", "initiation", "elongation", "termination"],
        conclusion_template="Translation decodes mRNA into protein using ribosomes, tRNAs, and accessory factors.",
        reasoning_framework=(
            "Translation is the process of synthesizing proteins from mRNA templates. "
            "Ribosomes read mRNA codons and recruit tRNAs carrying specific amino acids. "
            "Initiation involves assembly of the ribosome at the start codon (AUG). "
            "Elongation adds amino acids to the growing polypeptide chain. "
            "Termination occurs at stop codons, releasing the completed protein. "
            "Accuracy is ensured by codon-anticodon pairing and proofreading. "
            "Translation is regulated by initiation factors, mRNA structure, and microRNAs."
        ),
        key_factors=[
            "Ribosome structure",
            "tRNA charging",
            "Initiation and elongation factors",
            "Codon recognition",
            "Regulatory mechanisms"
        ],
        primary_authority=["Lehninger Principles of Biochemistry", "Alberts Molecular Biology of the Cell"],
        burden_holder="Proponent of translation fidelity",
        adversary_position="Some translation errors occur",
        counter_arguments=[
            "Frameshifting and readthrough can happen",
            "Quality control mechanisms exist"
        ],
        resolution_strategy="Discuss error rates and cellular quality control.",
        entity_scope="All cells",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Nirenberg and Matthaei genetic code experiments (1961)"
    ),
    DoctrineBlock(
        topic="signal_transduction_gpcr",
        keywords=["GPCR", "G protein-coupled receptor", "second messenger", "cAMP", "signal amplification"],
        conclusion_template="GPCRs transduce extracellular signals via G proteins, activating second messenger pathways.",
        reasoning_framework=(
            "G protein-coupled receptors (GPCRs) are a large family of membrane proteins that respond to diverse signals. "
            "Ligand binding induces conformational changes, activating heterotrimeric G proteins. "
            "G proteins modulate effectors such as adenylyl cyclase (cAMP production) or phospholipase C (IP3/DAG). "
            "Second messengers amplify the signal and activate downstream kinases. "
            "GPCR signaling is terminated by receptor desensitization and GTP hydrolysis. "
            "GPCRs are major drug targets due to their physiological importance."
        ),
        key_factors=[
            "Ligand specificity",
            "G protein activation",
            "Second messenger generation",
            "Signal amplification",
            "Termination mechanisms"
        ],
        primary_authority=["Gilman Nobel Prize (1994)", "Alberts Molecular Biology of the Cell"],
        burden_holder="Proponent of GPCR as primary signaling mechanism",
        adversary_position="Other receptor types mediate signaling",
        counter_arguments=[
            "Receptor tyrosine kinases and ion channels also transmit signals",
            "GPCR cross-talk with other pathways"
        ],
        resolution_strategy="Discuss GPCRs as one of several major signaling mechanisms.",
        entity_scope="Eukaryotic cells",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Gilman's discovery of G proteins (1980s)"
    ),
    DoctrineBlock(
        topic="signal_transduction_rtk",
        keywords=["receptor tyrosine kinase", "autophosphorylation", "MAP kinase", "growth factor", "signal cascade"],
        conclusion_template="RTKs transmit signals by ligand-induced dimerization and autophosphorylation, activating downstream cascades.",
        reasoning_framework=(
            "Receptor tyrosine kinases (RTKs) are transmembrane proteins activated by growth factors and hormones. "
            "Ligand binding induces dimerization and autophosphorylation of tyrosine residues. "
            "Phosphotyrosines serve as docking sites for adaptor proteins, initiating signaling cascades such as the MAP kinase pathway. "
            "RTK signaling regulates cell growth, differentiation, and metabolism. "
            "Dysregulation leads to cancer and other diseases. "
            "Termination involves receptor internalization and phosphatase activity."
        ),
        key_factors=[
            "Ligand binding",
            "Dimerization",
            "Autophosphorylation",
            "Adaptor proteins",
            "Signal termination"
        ],
        primary_authority=["Lehninger Principles of Biochemistry", "Alberts Molecular Biology of the Cell"],
        burden_holder="Proponent of RTK as key growth factor receptor",
        adversary_position="Not all growth factors use RTKs",
        counter_arguments=[
            "Cytokine receptors use JAK-STAT pathway",
            "GPCRs also mediate some growth signals"
        ],
        resolution_strategy="Clarify RTK specificity and cross-talk with other pathways.",
        entity_scope="Eukaryotic cells",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Ullrich and Schlessinger RTK studies (1980s)"
    ),
    DoctrineBlock(
        topic="membrane_transport",
        keywords=["membrane transport", "facilitated diffusion", "active transport", "ion channel", "ATPase"],
        conclusion_template="Membrane transport includes passive and active mechanisms, mediated by channels, carriers, and pumps.",
        reasoning_framework=(
            "Biological membranes are selectively permeable. "
            "Passive transport (diffusion, facilitated diffusion) moves substances down their concentration gradients without energy input. "
            "Facilitated diffusion uses carrier proteins or channels (e.g., glucose transporter, ion channels). "
            "Active transport requires energy (usually ATP) to move substances against gradients (e.g., Na+/K+ ATPase). "
            "Secondary active transport couples movement of one solute to another's gradient. "
            "Transport defects cause diseases such as cystic fibrosis (CFTR channel mutation)."
        ),
        key_factors=[
            "Concentration gradients",
            "Transport protein specificity",
            "Energy requirement",
            "Directionality",
            "Pathophysiology"
        ],
        primary_authority=["Alberts Molecular Biology of the Cell", "Lehninger Principles of Biochemistry"],
        burden_holder="Proponent of transport classification",
        adversary_position="Some transporters have mixed mechanisms",
        counter_arguments=[
            "Symporters and antiporters blur categories",
            "Vesicular transport is distinct"
        ],
        resolution_strategy="Use mechanistic criteria for classification; acknowledge exceptions.",
        entity_scope="All cells",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Hodgkin and Huxley ion channel studies (1952)"
    ),
    DoctrineBlock(
        topic="vitamins_coenzymes",
        keywords=["vitamin", "coenzyme", "deficiency", "enzyme cofactor", "metabolism"],
        conclusion_template="Vitamins often serve as coenzymes or precursors, essential for enzyme function and metabolic health.",
        reasoning_framework=(
            "Vitamins are organic compounds required in small amounts for normal metabolism. "
            "Many act as coenzymes or precursors (e.g., B vitamins: NAD+, FAD, CoA, TPP, PLP, biotin). "
            "Deficiency impairs enzyme activity, leading to characteristic diseases (e.g., pellagra, scurvy, beriberi). "
            "Fat-soluble vitamins (A, D, E, K) have additional roles in vision, calcium metabolism, antioxidant defense, and coagulation. "
            "Excess or deficiency can both be harmful. "
            "Coenzyme recycling and dietary intake are critical for homeostasis."
        ),
        key_factors=[
            "Dietary intake",
            "Coenzyme function",
            "Deficiency symptoms",
            "Enzyme specificity",
            "Toxicity"
        ],
        primary_authority=["Lehninger Principles of Biochemistry", "Harper's Illustrated Biochemistry"],
        burden_holder="Proponent of vitamin necessity",
        adversary_position="Some organisms synthesize all required coenzymes",
        counter_arguments=[
            "Gut microbiota may provide some vitamins",
            "Synthetic analogs can substitute in some cases"
        ],
        resolution_strategy="Emphasize human dietary requirements and clinical relevance.",
        entity_scope="Humans and higher animals",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Discovery of vitamins (early 20th century)"
    ),
    DoctrineBlock(
        topic="clinical_biochemistry",
        keywords=["clinical biochemistry", "biomarker", "diagnosis", "enzyme assay", "reference range"],
        conclusion_template="Clinical biochemistry uses quantitative analysis of biomolecules to diagnose and monitor disease.",
        reasoning_framework=(
            "Clinical biochemistry applies biochemical principles to medical diagnosis and management. "
            "Measurement of enzymes, metabolites, and electrolytes in blood and urine provides diagnostic information. "
            "Common tests include glucose, creatinine, liver enzymes (ALT, AST), cardiac markers (troponin), and lipid profiles. "
            "Reference ranges are established for healthy populations; deviations indicate pathology. "
            "Pre-analytical, analytical, and post-analytical factors affect test interpretation. "
            "Point-of-care testing and automation have improved accessibility and turnaround time."
        ),
        key_factors=[
            "Biomarker selection",
            "Assay accuracy",
            "Reference ranges",
            "Clinical context",
            "Quality control"
        ],
        primary_authority=["Tietz Textbook of Clinical Chemistry", "Burtis & Bruns"],
        burden_holder="Proponent of biochemical testing utility",
        adversary_position="Clinical context may override biochemical findings",
        counter_arguments=[
            "False positives/negatives occur",
            "Clinical judgment is essential"
        ],
        resolution_strategy="Integrate biochemical data with clinical assessment.",
        entity_scope="Clinical laboratories",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Development of clinical enzyme assays (1950s-1970s)"
    ),
    # Additional doctrines for comprehensive coverage
    DoctrineBlock(
        topic="protein_posttranslational_modification",
        keywords=["posttranslational modification", "phosphorylation", "glycosylation", "ubiquitination", "protein function"],
        conclusion_template="Posttranslational modifications diversify protein function, localization, and stability.",
        reasoning_framework=(
            "Proteins often undergo covalent modifications after translation, altering their function, localization, or degradation. "
            "Common modifications include phosphorylation (regulation), glycosylation (stability, recognition), ubiquitination (degradation), methylation, acetylation, and lipidation. "
            "These modifications are reversible and tightly regulated. "
            "Defects in modification pathways can cause disease (e.g., cancer, congenital disorders of glycosylation)."
        ),
        key_factors=[
            "Modification type",
            "Enzyme specificity",
            "Reversibility",
            "Functional impact",
            "Disease relevance"
        ],
        primary_authority=["Alberts Molecular Biology of the Cell", "Lehninger Principles of Biochemistry"],
        burden_holder="Proponent of modification importance",
        adversary_position="Some proteins function without modification",
        counter_arguments=[
            "Not all proteins are modified",
            "Some modifications are non-essential"
        ],
        resolution_strategy="Emphasize regulatory and functional diversity conferred by modifications.",
        entity_scope="Eukaryotic proteins",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Discovery of protein phosphorylation (1950s)"
    ),
    DoctrineBlock(
        topic="enzyme_cofactors",
        keywords=["enzyme cofactor", "metal ion", "prosthetic group", "apoenzyme", "holoenzyme"],
        conclusion_template="Enzyme cofactors, including metal ions and organic molecules, are essential for catalytic activity.",
        reasoning_framework=(
            "Many enzymes require non-protein cofactors for activity. "
            "Cofactors can be metal ions (e.g., Mg2+, Zn2+, Fe2+/3+) or organic molecules (coenzymes, prosthetic groups). "
            "The protein portion alone (apoenzyme) is inactive; the complete enzyme (holoenzyme) is catalytically competent. "
            "Cofactor binding can be transient or permanent. "
            "Deficiency of cofactors impairs enzyme function and metabolism."
        ),
        key_factors=[
            "Cofactor type",
            "Binding affinity",
            "Enzyme specificity",
            "Catalytic mechanism",
            "Nutritional status"
        ],
        primary_authority=["Lehninger Principles of Biochemistry", "Harper's Illustrated Biochemistry"],
        burden_holder="Proponent of cofactor necessity",
        adversary_position="Some enzymes are purely proteinaceous",
        counter_arguments=[
            "Ribozymes function without cofactors",
            "Some enzymes use only amino acid side chains"
        ],
        resolution_strategy="Clarify prevalence and exceptions.",
        entity_scope="All enzymes",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Fischer's lock-and-key model (1894)"
    ),
    DoctrineBlock(
        topic="enzyme_specificity",
        keywords=["enzyme specificity", "active site", "substrate recognition", "induced fit", "catalysis"],
        conclusion_template="Enzyme specificity arises from precise active site-substrate complementarity and induced fit.",
        reasoning_framework=(
            "Enzymes exhibit high specificity for their substrates, determined by the three-dimensional structure of the active site. "
            "The lock-and-key model describes static complementarity, while the induced fit model accounts for conformational changes upon substrate binding. "
            "Specificity ensures proper metabolic flux and prevents unwanted side reactions. "
            "Mutations in active site residues can alter specificity and lead to disease."
        ),
        key_factors=[
            "Active site structure",
            "Substrate complementarity",
            "Induced fit",
            "Mutational effects",
            "Kinetic parameters"
        ],
        primary_authority=["Koshland induced fit model (1958)", "Lehninger Principles of Biochemistry"],
        burden_holder="Proponent of specificity as enzyme hallmark",
        adversary_position="Some enzymes are promiscuous",
        counter_arguments=[
            "Promiscuous enzymes catalyze multiple reactions",
            "Evolution can repurpose enzyme specificity"
        ],
        resolution_strategy="Discuss spectrum of specificity and evolutionary implications.",
        entity_scope="All enzymes",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Koshland's induced fit model (1958)"
    ),
    DoctrineBlock(
        topic="enzyme_regulation_covalent",
        keywords=["covalent modification", "enzyme regulation", "phosphorylation", "kinase", "phosphatase"],
        conclusion_template="Covalent modification, especially phosphorylation, is a major mechanism of enzyme regulation.",
        reasoning_framework=(
            "Many enzymes are regulated by reversible covalent modifications, most commonly phosphorylation and dephosphorylation. "
            "Protein kinases add phosphate groups (often activating or inhibiting enzymes), while phosphatases remove them. "
            "Other modifications include acetylation, methylation, and ADP-ribosylation. "
            "Covalent regulation allows rapid, reversible, and signal-dependent control of enzyme activity."
        ),
        key_factors=[
            "Modification type",
            "Enzyme targets",
            "Regulatory signals",
            "Reversibility",
            "Physiological context"
        ],
        primary_authority=["Lehninger Principles of Biochemistry", "Alberts Molecular Biology of the Cell"],
        burden_holder="Proponent of covalent regulation",
        adversary_position="Allosteric regulation is also important",
        counter_arguments=[
            "Some enzymes are regulated only allosterically",
            "Covalent modification can be slow or irreversible"
        ],
        resolution_strategy="Discuss interplay of covalent and allosteric mechanisms.",
        entity_scope="Eukaryotic enzymes",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Fischer and Krebs discovery of phosphorylation (1950s)"
    ),
    DoctrineBlock(
        topic="enzyme_regulation_allosteric",
        keywords=["allosteric regulation", "feedback inhibition", "cooperativity", "metabolic pathway", "enzyme activity"],
        conclusion_template="Allosteric regulation enables feedback control and fine-tuning of metabolic pathways.",
        reasoning_framework=(
            "Allosteric enzymes are regulated by effectors binding at sites distinct from the active site. "
            "Feedback inhibition is a common mechanism, where pathway end-products inhibit upstream enzymes. "
            "Cooperativity among subunits allows sensitive response to metabolite concentrations. "
            "Allosteric regulation is rapid, reversible, and essential for metabolic homeostasis."
        ),
        key_factors=[
            "Effector molecules",
            "Feedback loops",
            "Cooperativity",
            "Pathway integration",
            "Physiological relevance"
        ],
        primary_authority=["Monod, Wyman & Changeux (1965)", "Lehninger Principles of Biochemistry"],
        burden_holder="Proponent of allosteric regulation",
        adversary_position="Covalent modification also regulates enzymes",
        counter_arguments=[
            "Many enzymes are regulated by both mechanisms",
            "Some metabolic steps are not regulated"
        ],
        resolution_strategy="Emphasize complementary roles of regulation mechanisms.",
        entity_scope="Key metabolic enzymes",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Monod-Wyman-Changeux model (1965)"
    ),
    DoctrineBlock(
        topic="glycogen_metabolism",
        keywords=["glycogen synthesis", "glycogenolysis", "glycogen phosphorylase", "glycogen synthase", "regulation"],
        conclusion_template="Glycogen metabolism is tightly regulated by hormonal and allosteric mechanisms to balance energy storage and release.",
        reasoning_framework=(
            "Glycogen is a branched glucose polymer stored in liver and muscle. "
            "Glycogen synthase catalyzes synthesis; glycogen phosphorylase catalyzes breakdown. "
            "Regulation involves covalent modification (phosphorylation/dephosphorylation) and allosteric effectors (AMP, glucose-6-phosphate). "
            "Hormones (insulin, glucagon, epinephrine) coordinate glycogen metabolism in response to blood glucose levels."
        ),
        key_factors=[
            "Enzyme activity",
            "Hormonal signals",
            "Allosteric effectors",
            "Tissue specificity",
            "Pathophysiology"
        ],
        primary_authority=["Lehninger Principles of Biochemistry", "Berg, Tymoczko & Stryer"],
        burden_holder="Proponent of regulatory complexity",
        adversary_position="Some regulation is tissue-specific",
        counter_arguments=[
            "Muscle and liver differ in regulation",
            "Genetic diseases affect glycogen metabolism"
        ],
        resolution_strategy="Discuss tissue-specific differences and clinical implications.",
        entity_scope="Liver and muscle",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Cori's discovery of glycogen phosphorylase (1940s)"
    ),
    DoctrineBlock(
        topic="pentose_phosphate_pathway",
        keywords=["pentose phosphate pathway", "NADPH", "ribose-5-phosphate", "oxidative branch", "non-oxidative branch"],
        conclusion_template="The pentose phosphate pathway generates NADPH and ribose-5-phosphate for biosynthesis and antioxidant defense.",
        reasoning_framework=(
            "The pentose phosphate pathway (PPP) operates in the cytosol and has two phases: oxidative (produces NADPH and ribulose-5-phosphate) and non-oxidative (interconverts sugars). "
            "NADPH is essential for reductive biosynthesis and maintaining glutathione in its reduced form. "
            "Ribose-5-phosphate is required for nucleotide synthesis. "
            "The PPP is highly active in tissues with biosynthetic or antioxidant demands (liver, adipose, red blood cells). "
            "Glucose-6-phosphate dehydrogenase (G6PD) is the rate-limiting enzyme; deficiency leads to hemolytic anemia."
        ),
        key_factors=[
            "NADPH production",
            "Ribose-5-phosphate supply",
            "Enzyme regulation",
            "Tissue specificity",
            "Clinical relevance"
        ],
        primary_authority=["Lehninger Principles of Biochemistry", "Harper's Illustrated Biochemistry"],
        burden_holder="Proponent of PPP importance",
        adversary_position="Glycolysis predominates in some tissues",
        counter_arguments=[
            "PPP flux varies by tissue and demand",
            "G6PD deficiency is common"
        ],
        resolution_strategy="Highlight tissue-specific roles and clinical implications.",
        entity_scope="Cytosol of all cells",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Warburg's elucidation of PPP (1930s)"
    ),
    DoctrineBlock(
        topic="cholesterol_metabolism",
        keywords=["cholesterol synthesis", "HMG-CoA reductase", "LDL", "statin", "atherosclerosis"],
        conclusion_template="Cholesterol metabolism is regulated at HMG-CoA reductase and is central to cardiovascular health.",
        reasoning_framework=(
            "Cholesterol is synthesized from acetyl-CoA via the mevalonate pathway, with HMG-CoA reductase as the rate-limiting enzyme. "
            "Dietary intake and endogenous synthesis are balanced to maintain homeostasis. "
            "Cholesterol is transported in blood as LDL and HDL particles. "
            "Statins inhibit HMG-CoA reductase, lowering LDL and reducing cardiovascular risk. "
            "Excess cholesterol contributes to atherosclerosis."
        ),
        key_factors=[
            "HMG-CoA reductase activity",
            "Dietary intake",
            "Lipoprotein transport",
            "Pharmacological intervention",
            "Disease risk"
        ],
        primary_authority=["Lehninger Principles of Biochemistry", "Goldstein & Brown (Nobel 1985)"],
        burden_holder="Proponent of cholesterol regulation",
        adversary_position="Some cholesterol is essential for cell membranes",
        counter_arguments=[
            "Complete inhibition is not desirable",
            "Genetic disorders affect cholesterol metabolism"
        ],
        resolution_strategy="Balance discussion of physiological and pathological roles.",
        entity_scope="Liver and plasma",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Goldstein and Brown's LDL receptor studies (1980s)"
    ),
    DoctrineBlock(
        topic="heme_metabolism",
        keywords=["heme synthesis", "porphyrin", "heme oxygenase", "bilirubin", "jaundice"],
        conclusion_template="Heme metabolism involves synthesis from glycine and succinyl-CoA and degradation to bilirubin.",
        reasoning_framework=(
            "Heme is synthesized in mitochondria and cytosol from glycine and succinyl-CoA via the porphyrin pathway. "
            "The rate-limiting enzyme is ALA synthase. "
            "Heme is degraded by heme oxygenase to biliverdin, then to bilirubin, which is conjugated in the liver and excreted in bile. "
            "Disorders of heme metabolism cause porphyrias and jaundice."
        ),
        key_factors=[
            "Enzyme activity",
            "Substrate availability",
            "Genetic defects",
            "Clinical manifestations",
            "Excretion pathways"
        ],
        primary_authority=["Lehninger Principles of Biochemistry", "Harper's Illustrated Biochemistry"],
        burden_holder="Proponent of pathway importance",
        adversary_position="Alternative pathways in some organisms",
        counter_arguments=[
            "Bacteria synthesize heme differently",
            "Neonatal jaundice is common"
        ],
        resolution_strategy="Emphasize mammalian pathway and clinical relevance.",
        entity_scope="Liver, bone marrow",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Shemin and Rittenberg's studies (1940s)"
    ),
    DoctrineBlock(
        topic="amino_acid_biosynthesis",
        keywords=["amino acid synthesis", "essential amino acids", "transamination", "carbon skeleton", "anaplerosis"],
        conclusion_template="Non-essential amino acids are synthesized from metabolic intermediates; essential amino acids must be obtained from the diet.",
        reasoning_framework=(
            "Amino acids are synthesized from intermediates of glycolysis, TCA cycle, and PPP. "
            "Transamination reactions transfer amino groups to carbon skeletons. "
            "Essential amino acids cannot be synthesized by humans and must be supplied in the diet. "
            "Anaplerotic reactions replenish TCA cycle intermediates used for biosynthesis."
        ),
        key_factors=[
            "Metabolic intermediates",
            "Transamination enzymes",
            "Dietary requirements",
            "Genetic defects",
            "Nutritional status"
        ],
        primary_authority=["Lehninger Principles of Biochemistry", "Harper's Illustrated Biochemistry"],
        burden_holder="Proponent of biosynthetic capacity",
        adversary_position="Some organisms synthesize all amino acids",
        counter_arguments=[
            "Plants and bacteria have complete pathways",
            "Genetic disorders impair synthesis"
        ],
        resolution_strategy="Emphasize human dietary requirements.",
        entity_scope="Liver and other tissues",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Elucidation of essential amino acids (early 20th century)"
    ),
    DoctrineBlock(
        topic="nucleotide_synthesis_regulation",
        keywords=["nucleotide synthesis", "feedback inhibition", "PRPP", "ribonucleotide reductase", "balanced supply"],
        conclusion_template="Nucleotide synthesis is tightly regulated by feedback inhibition and allosteric control to maintain balanced pools.",
        reasoning_framework=(
            "De novo synthesis of nucleotides is regulated at key steps by feedback inhibition from end-products. "
            "PRPP amidotransferase is inhibited by purine nucleotides; carbamoyl phosphate synthetase II is regulated by pyrimidines. "
            "Ribonucleotide reductase controls deoxyribonucleotide production and is allosterically regulated to balance dNTP pools. "
            "Imbalances cause mutagenesis and disease."
        ),
        key_factors=[
            "Feedback inhibition",
            "Allosteric regulation",
            "Enzyme specificity",
            "Balanced supply",
            "Disease associations"
        ],
        primary_authority=["Lehninger Principles of Biochemistry", "Harper's Illustrated Biochemistry"],
        burden_holder="Proponent of regulatory importance",
        adversary_position="Salvage pathways also contribute",
        counter_arguments=[
            "Salvage can compensate for some defects",
            "Cancer cells often upregulate synthesis"
        ],
        resolution_strategy="Discuss interplay of de novo and salvage pathways.",
        entity_scope="All dividing cells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Elion and Hitchings' studies (1950s)"
    ),
    DoctrineBlock(
        topic="dna_topology",
        keywords=["DNA topology", "supercoiling", "topoisomerase", "replication", "transcription"],
        conclusion_template="DNA topology, including supercoiling, is regulated by topoisomerases during replication and transcription.",
        reasoning_framework=(
            "DNA supercoiling affects replication, transcription, and chromosome compaction. "
            "Topoisomerases introduce or remove supercoils to relieve torsional stress. "
            "Type I topoisomerases make single-strand breaks; type II make double-strand breaks. "
            "Inhibitors of topoisomerases are used as antibiotics and anticancer drugs."
        ),
        key_factors=[
            "Supercoiling state",
            "Topoisomerase activity",
            "Replication and transcription",
            "Drug targets",
            "Mutational effects"
        ],
        primary_authority=["Wang's discovery of topoisomerase (1971)", "Alberts Molecular Biology of the Cell"],
        burden_holder="Proponent of topological regulation",
        adversary_position="Some viruses use alternative mechanisms",
        counter_arguments=[
            "Circular DNA in prokaryotes",
            "Topoisomerase mutations cause disease"
        ],
        resolution_strategy="Emphasize eukaryotic and prokaryotic differences.",
        entity_scope="All cells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Wang's topoisomerase studies (1970s)"
    ),
    DoctrineBlock(
        topic="epigenetic_regulation",
        keywords=["epigenetics", "DNA methylation", "histone modification", "chromatin", "gene expression"],
        conclusion_template="Epigenetic regulation modulates gene expression without altering DNA sequence, via methylation and histone modifications.",
        reasoning_framework=(
            "Epigenetic mechanisms include DNA methylation, histone acetylation/methylation, and chromatin remodeling. "
            "These modifications alter chromatin structure and gene accessibility. "
            "Epigenetic marks are heritable through cell division but reversible. "
            "Epigenetic dysregulation contributes to cancer and developmental disorders."
        ),
        key_factors=[
            "DNA methylation",
            "Histone modification",
            "Chromatin structure",
            "Gene accessibility",
            "Heritability"
        ],
        primary_authority=["Bird (1978)", "Alberts Molecular Biology of the Cell"],
        burden_holder="Proponent of epigenetic importance",
        adversary_position="Genetic mutations also regulate expression",
        counter_arguments=[
            "Epigenetic changes are reversible",
            "Environmental factors influence epigenetics"
        ],
        resolution_strategy="Discuss interplay of genetic and epigenetic regulation.",
        entity_scope="Eukaryotic cells",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Bird's DNA methylation studies (1970s)"
    ),
    DoctrineBlock(
        topic="protein_degradation",
        keywords=["protein degradation", "ubiquitin-proteasome", "lysosome", "autophagy", "protein turnover"],
        conclusion_template="Protein degradation occurs via the ubiquitin-proteasome system and lysosomal pathways, maintaining protein quality.",
        reasoning_framework=(
            "Proteins are degraded to regulate cellular function and remove damaged or misfolded proteins. "
            "The ubiquitin-proteasome system tags proteins with ubiquitin for degradation. "
            "Lysosomal degradation handles extracellular and long-lived proteins via autophagy. "
            "Protein turnover is essential for cellular homeostasis; defects lead to disease."
        ),
        key_factors=[
            "Ubiquitination",
            "Proteasome activity",
            "Lysosomal function",
            "Autophagy",
            "Disease associations"
        ],
        primary_authority=["Ciechanover, Hershko & Rose (Nobel 2004)", "Lehninger Principles of Biochemistry"],
        burden_holder="Proponent of degradation pathways",
        adversary_position="Some proteins are long-lived",
        counter_arguments=[
            "Structural proteins have slow turnover",
            "Proteostasis networks are complex"
        ],
        resolution_strategy="Discuss balance between synthesis and degradation.",
        entity_scope="All cells",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Discovery of ubiquitin-mediated degradation (1980s)"
    ),
    DoctrineBlock(
        topic="cell_cycle_control",
        keywords=["cell cycle", "cyclin", "CDK", "checkpoint", "cell division"],
        conclusion_template="Cell cycle progression is regulated by cyclins, CDKs, and checkpoints ensuring genomic integrity.",
        reasoning_framework=(
            "The cell cycle consists of G1, S, G2, and M phases. "
            "Cyclin-dependent kinases (CDKs) are activated by cyclins to drive cell cycle transitions. "
            "Checkpoints monitor DNA integrity and spindle assembly, halting the cycle if errors are detected. "
            "Dysregulation leads to uncontrolled proliferation and cancer."
        ),
        key_factors=[
            "Cyclin-CDK complexes",
            "Checkpoint proteins",
            "DNA integrity",
            "Mitotic spindle",
            "Disease associations"
        ],
        primary_authority=["Nurse, Hunt & Hartwell (Nobel 2001)", "Alberts Molecular Biology of the Cell"],
        burden_holder="Proponent of checkpoint importance",
        adversary_position="Some cells bypass checkpoints",
        counter_arguments=[
            "Cancer cells often have defective checkpoints",
            "Stem cells have unique regulation"
        ],
        resolution_strategy="Discuss normal and pathological regulation.",
        entity_scope="Dividing cells",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Nurse and Hartwell's cell cycle studies (1970s-80s)"
    ),
    DoctrineBlock(
        topic="apoptosis",
        keywords=["apoptosis", "programmed cell death", "caspase", "Bcl-2", "cellular homeostasis"],
        conclusion_template="Apoptosis is a regulated process of programmed cell death mediated by caspases and Bcl-2 family proteins.",
        reasoning_framework=(
            "Apoptosis eliminates damaged or unnecessary cells in a controlled manner. "
            "Caspases are proteases that execute the death program. "
            "Bcl-2 family proteins regulate mitochondrial outer membrane permeabilization. "
            "Phagocytes clear apoptotic bodies, preventing inflammation. "
            "Defects in apoptosis contribute to cancer, autoimmune disease, and neurodegeneration."
        ),
        key_factors=[
            "Caspase activation",
            "Bcl-2 regulation",
            "Mitochondrial involvement",
            "Phagocytosis",
            "Disease relevance"
        ],
        primary_authority=["Kerr, Wyllie & Currie (1972)", "Alberts Molecular Biology of the Cell"],
        burden_holder="Proponent of apoptosis as essential",
        adversary_position="Necrosis is also a form of cell death",
        counter_arguments=[
            "Necroptosis and autophagy are alternative death pathways",
            "Apoptosis can be dysregulated"
        ],
        resolution_strategy="Discuss distinctions and overlap between death pathways.",
        entity_scope="Multicellular organisms",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Kerr's discovery of apoptosis (1972)"
    ),
    DoctrineBlock(
        topic="oncogene_tumor_suppressor",
        keywords=["oncogene", "tumor suppressor", "p53", "Rb", "cancer"],
        conclusion_template="Oncogenes promote, and tumor suppressors inhibit, cell proliferation; mutations drive cancer development.",
        reasoning_framework=(
            "Oncogenes are mutated or overexpressed genes that drive cell proliferation (e.g., Ras, Myc). "
            "Tumor suppressors (e.g., p53, Rb) inhibit proliferation and promote genome stability. "
            "Loss of tumor suppressor function or gain of oncogene function leads to cancer. "
            "Multiple mutations are typically required for tumorigenesis."
        ),
        key_factors=[
            "Gene mutation",
            "Protein function",
            "Cell cycle regulation",
            "Genome stability",
            "Cancer risk"
        ],
        primary_authority=["Vogelstein & Kinzler", "Alberts Molecular Biology of the Cell"],
        burden_holder="Proponent of multi-hit hypothesis",
        adversary_position="Epigenetic changes also contribute",
        counter_arguments=[
            "Epigenetic silencing of tumor suppressors",
            "Microenvironment influences tumorigenesis"
        ],
        resolution_strategy="Discuss genetic and epigenetic contributions.",
        entity_scope="Multicellular organisms",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Knudson's two-hit hypothesis (1971)"
    ),
    DoctrineBlock(
        topic="cell_signaling_cross_talk",
        keywords=["cell signaling", "cross-talk", "integration", "signal transduction", "network"],
        conclusion_template="Signaling pathways interact via cross-talk, integrating multiple inputs for coordinated cellular responses.",
        reasoning_framework=(
            "Cell signaling pathways rarely act in isolation; cross-talk enables integration of diverse signals. "
            "Shared components (e.g., kinases, second messengers) allow convergence and divergence of pathways. "
            "Cross-talk modulates sensitivity, specificity, and adaptation. "
            "Dysregulation can lead to disease."
        ),
        key_factors=[
            "Shared signaling components",
            "Pathway integration",
            "Cellular context",
            "Feedback loops",
            "Disease associations"
        ],
        primary_authority=["Alberts Molecular Biology of the Cell", "Lehninger Principles of Biochemistry"],
        burden_holder="Proponent of network integration",
        adversary_position="Some pathways are insulated",
        counter_arguments=[
            "Scaffold proteins restrict cross-talk",
            "Spatial compartmentalization limits integration"
        ],
        resolution_strategy="Discuss balance between integration and insulation.",
        entity_scope="Eukaryotic cells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Studies of MAPK and PI3K/Akt cross-talk (2000s)"
    ),
    DoctrineBlock(
        topic="cellular_respiration_overview",
        keywords=["cellular respiration", "glycolysis", "TCA cycle", "oxidative phosphorylation", "ATP"],
        conclusion_template="Cellular respiration comprises glycolysis, TCA cycle, and oxidative phosphorylation, maximizing ATP yield from glucose.",
        reasoning_framework=(
            "Cellular respiration is the process by which cells extract energy