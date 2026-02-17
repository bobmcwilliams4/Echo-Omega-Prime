import hashlib

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_AUTHOR = "CHEM05 Team"
SEMANTIC_MAP_ENGINE = "CHEM05_biochemistry"

SEMANTIC_MAP = {
    # protein_primary_structure
    "primary structure": "protein_primary_structure",
    "protein primary structure": "protein_primary_structure",
    "1° structure": "protein_primary_structure",
    "1 degree structure": "protein_primary_structure",
    "amino acid sequence": "protein_primary_structure",
    "aa sequence": "protein_primary_structure",
    "polypeptide chain": "protein_primary_structure",
    "protein sequence": "protein_primary_structure",
    "priamry structure": "protein_primary_structure",  # misspelling

    # protein_secondary_structure
    "secondary structure": "protein_secondary_structure",
    "protein secondary structure": "protein_secondary_structure",
    "2° structure": "protein_secondary_structure",
    "2 degree structure": "protein_secondary_structure",
    "alpha helix": "protein_secondary_structure",
    "alpha-helix": "protein_secondary_structure",
    "α helix": "protein_secondary_structure",
    "alpha helix structure": "protein_secondary_structure",
    "beta sheet": "protein_secondary_structure",
    "beta-sheet": "protein_secondary_structure",
    "β sheet": "protein_secondary_structure",
    "beta strand": "protein_secondary_structure",
    "beta-strand": "protein_secondary_structure",
    "β strand": "protein_secondary_structure",
    "random coil": "protein_secondary_structure",
    "coil structure": "protein_secondary_structure",
    "secondary strcture": "protein_secondary_structure",  # misspelling

    # protein_tertiary_structure
    "tertiary structure": "protein_tertiary_structure",
    "protein tertiary structure": "protein_tertiary_structure",
    "3° structure": "protein_tertiary_structure",
    "3 degree structure": "protein_tertiary_structure",
    "folded protein": "protein_tertiary_structure",
    "protein fold": "protein_tertiary_structure",
    "tertiary strcture": "protein_tertiary_structure",  # misspelling

    # protein_quaternary_structure
    "quaternary structure": "protein_quaternary_structure",
    "protein quaternary structure": "protein_quaternary_structure",
    "4° structure": "protein_quaternary_structure",
    "4 degree structure": "protein_quaternary_structure",
    "multimeric protein": "protein_quaternary_structure",
    "protein complex": "protein_quaternary_structure",
    "oligomeric protein": "protein_quaternary_structure",
    "quaternary strcture": "protein_quaternary_structure",  # misspelling

    # enzyme_kinetics_michaelis_menten
    "michaelis menten": "enzyme_kinetics_michaelis_menten",
    "michaelis-menten": "enzyme_kinetics_michaelis_menten",
    "enzyme kinetics": "enzyme_kinetics_michaelis_menten",
    "michaelis constant": "enzyme_kinetics_michaelis_menten",
    "km": "enzyme_kinetics_michaelis_menten",
    "vmax": "enzyme_kinetics_michaelis_menten",
    "max velocity": "enzyme_kinetics_michaelis_menten",
    "enzyme velocity": "enzyme_kinetics_michaelis_menten",
    "michalis menten": "enzyme_kinetics_michaelis_menten",  # misspelling
    "michalis-menten": "enzyme_kinetics_michaelis_menten",

    # enzyme_inhibition
    "enzyme inhibition": "enzyme_inhibition",
    "competitive inhibition": "enzyme_inhibition",
    "noncompetitive inhibition": "enzyme_inhibition",
    "uncompetitive inhibition": "enzyme_inhibition",
    "mixed inhibition": "enzyme_inhibition",
    "inhibitor": "enzyme_inhibition",
    "inhibitors": "enzyme_inhibition",
    "enzyme inhibitor": "enzyme_inhibition",
    "enzyme inhibitors": "enzyme_inhibition",
    "inhibit": "enzyme_inhibition",
    "inhibiting": "enzyme_inhibition",

    # allosteric_regulation
    "allosteric regulation": "allosteric_regulation",
    "allosteric control": "allosteric_regulation",
    "allosteric modulator": "allosteric_regulation",
    "allosteric effector": "allosteric_regulation",
    "allosteric activator": "allosteric_regulation",
    "allosteric inhibitor": "allosteric_regulation",
    "allostery": "allosteric_regulation",

    # glycolysis
    "glycolysis": "glycolysis",
    "embden-meyerhof pathway": "glycolysis",
    "embden meyerhof pathway": "glycolysis",
    "glycolytic pathway": "glycolysis",
    "glycolitic pathway": "glycolysis",  # misspelling
    "glycolitic": "glycolysis",  # misspelling
    "glucose metabolism": "glycolysis",
    "glucose catabolism": "glycolysis",

    # tca_cycle
    "tca cycle": "tca_cycle",
    "tricarboxylic acid cycle": "tca_cycle",
    "citric acid cycle": "tca_cycle",
    "krebs cycle": "tca_cycle",
    "krebs' cycle": "tca_cycle",
    "krebs's cycle": "tca_cycle",
    "citric acid cylce": "tca_cycle",  # misspelling
    "tca cylce": "tca_cycle",  # misspelling

    # oxidative_phosphorylation
    "oxidative phosphorylation": "oxidative_phosphorylation",
    "oxidative phosphorilation": "oxidative_phosphorylation",  # misspelling
    "electron transport chain": "oxidative_phosphorylation",
    "etc": "oxidative_phosphorylation",
    "atp synthesis": "oxidative_phosphorylation",
    "atp synthase": "oxidative_phosphorylation",
    "oxidative phosphorylation system": "oxidative_phosphorylation",

    # gluconeogenesis
    "gluconeogenesis": "gluconeogenesis",
    "glucose synthesis": "gluconeogenesis",
    "new glucose formation": "gluconeogenesis",
    "glucogenesis": "gluconeogenesis",  # common misspelling
    "glucogenogenesis": "gluconeogenesis",  # misspelling
    "glucogenisis": "gluconeogenesis",  # misspelling

    # fatty_acid_oxidation
    "fatty acid oxidation": "fatty_acid_oxidation",
    "beta oxidation": "fatty_acid_oxidation",
    "β oxidation": "fatty_acid_oxidation",
    "fatty acid catabolism": "fatty_acid_oxidation",
    "lipid oxidation": "fatty_acid_oxidation",
    "fatty acid breakdown": "fatty_acid_oxidation",
    "fatty acid oxydation": "fatty_acid_oxidation",  # misspelling

    # fatty_acid_synthesis
    "fatty acid synthesis": "fatty_acid_synthesis",
    "lipid biosynthesis": "fatty_acid_synthesis",
    "lipid synthesis": "fatty_acid_synthesis",
    "fatty acid anabolism": "fatty_acid_synthesis",
    "fatty acid synthetase": "fatty_acid_synthesis",
    "fatty acid synthase": "fatty_acid_synthesis",
    "fatty acid syntesis": "fatty_acid_synthesis",  # misspelling

    # amino_acid_metabolism
    "amino acid metabolism": "amino_acid_metabolism",
    "aa metabolism": "amino_acid_metabolism",
    "amino acid catabolism": "amino_acid_metabolism",
    "amino acid anabolism": "amino_acid_metabolism",
    "amino acid biosynthesis": "amino_acid_metabolism",
    "amino acid degradation": "amino_acid_metabolism",

    # purine_metabolism
    "purine metabolism": "purine_metabolism",
    "purine biosynthesis": "purine_metabolism",
    "purine catabolism": "purine_metabolism",
    "purine degradation": "purine_metabolism",
    "purine salvage pathway": "purine_metabolism",
    "purine nucleotide metabolism": "purine_metabolism",

    # pyrimidine_metabolism
    "pyrimidine metabolism": "pyrimidine_metabolism",
    "pyrimidine biosynthesis": "pyrimidine_metabolism",
    "pyrimidine catabolism": "pyrimidine_metabolism",
    "pyrimidine degradation": "pyrimidine_metabolism",
    "pyrimidine salvage pathway": "pyrimidine_metabolism",
    "pyrimidine nucleotide metabolism": "pyrimidine_metabolism",

    # dna_replication
    "dna replication": "dna_replication",
    "deoxyribonucleic acid replication": "dna_replication",
    "dna synthesis": "dna_replication",
    "dna polymerization": "dna_replication",
    "dna pol": "dna_replication",
    "dna polymerase": "dna_replication",
    "dna replcation": "dna_replication",  # misspelling

    # dna_repair
    "dna repair": "dna_repair",
    "deoxyribonucleic acid repair": "dna_repair",
    "dna damage repair": "dna_repair",
    "dna mismatch repair": "dna_repair",
    "dna excision repair": "dna_repair",
    "dna repair mechanisms": "dna_repair",

    # transcription
    "transcription": "transcription",
    "rna synthesis": "transcription",
    "mrna synthesis": "transcription",
    "messenger rna synthesis": "transcription",
    "rna pol": "transcription",
    "rna polymerase": "transcription",
    "gene transcription": "transcription",
    "transciption": "transcription",  # misspelling

    # rna_processing
    "rna processing": "rna_processing",
    "mrna processing": "rna_processing",
    "rna splicing": "rna_processing",
    "mrna splicing": "rna_processing",
    "rna editing": "rna_processing",
    "mrna editing": "rna_processing",
    "rna capping": "rna_processing",
    "mrna capping": "rna_processing",
    "rna polyadenylation": "rna_processing",
    "mrna polyadenylation": "rna_processing",

    # translation
    "translation": "translation",
    "protein synthesis": "translation",
    "mrna translation": "translation",
    "polypeptide synthesis": "translation",
    "ribosome": "translation",
    "ribosomal translation": "translation",
    "translational process": "translation",

    # signal_transduction_gpcr
    "gpcr signaling": "signal_transduction_gpcr",
    "gpcr signal transduction": "signal_transduction_gpcr",
    "g protein coupled receptor": "signal_transduction_gpcr",
    "g-protein coupled receptor": "signal_transduction_gpcr",
    "g protein coupled receptor signaling": "signal_transduction_gpcr",
    "g-protein coupled receptor signaling": "signal_transduction_gpcr",
    "gpcr": "signal_transduction_gpcr",
    "g protein receptor": "signal_transduction_gpcr",

    # signal_transduction_rtk
    "rtk signaling": "signal_transduction_rtk",
    "rtk signal transduction": "signal_transduction_rtk",
    "receptor tyrosine kinase": "signal_transduction_rtk",
    "receptor tyrosine kinase signaling": "signal_transduction_rtk",
    "rtk": "signal_transduction_rtk",
    "tyrosine kinase receptor": "signal_transduction_rtk",

    # membrane_transport
    "membrane transport": "membrane_transport",
    "active transport": "membrane_transport",
    "passive transport": "membrane_transport",
    "facilitated diffusion": "membrane_transport",
    "simple diffusion": "membrane_transport",
    "endocytosis": "membrane_transport",
    "exocytosis": "membrane_transport",
    "membrane permeability": "membrane_transport",

    # vitamins_coenzymes
    "vitamins": "vitamins_coenzymes",
    "coenzymes": "vitamins_coenzymes",
    "vitamin b1": "vitamins_coenzymes",
    "thiamine": "vitamins_coenzymes",
    "vitamin b2": "vitamins_coenzymes",
    "riboflavin": "vitamins_coenzymes",
    "vitamin b3": "vitamins_coenzymes",
    "niacin": "vitamins_coenzymes",
    "vitamin b5": "vitamins_coenzymes",
    "pantothenic acid": "vitamins_coenzymes",
    "vitamin b6": "vitamins_coenzymes",
    "pyridoxine": "vitamins_coenzymes",
    "vitamin b7": "vitamins_coenzymes",
    "biotin": "vitamins_coenzymes",
    "vitamin b9": "vitamins_coenzymes",
    "folic acid": "vitamins_coenzymes",
    "vitamin b12": "vitamins_coenzymes",
    "cobalamin": "vitamins_coenzymes",
    "vitamin c": "vitamins_coenzymes",
    "ascorbic acid": "vitamins_coenzymes",
    "vitamin d": "vitamins_coenzymes",
    "calciferol": "vitamins_coenzymes",
    "vitamin e": "vitamins_coenzymes",
    "tocopherol": "vitamins_coenzymes",
    "vitamin k": "vitamins_coenzymes",
    "phylloquinone": "vitamins_coenzymes",

    # clinical_biochemistry
    "clinical biochemistry": "clinical_biochemistry",
    "clinical chemistry": "clinical_biochemistry",
    "medical biochemistry": "clinical_biochemistry",
    "laboratory medicine": "clinical_biochemistry",
    "clinical lab tests": "clinical_biochemistry",
    "biochemical tests": "clinical_biochemistry",
    "blood biochemistry": "clinical_biochemistry",
    "serum biochemistry": "clinical_biochemistry",
    "clinical biochmistry": "clinical_biochemistry",  # misspelling
}

_EXPECTED_ENTRY_COUNT = len(SEMANTIC_MAP)


def _compute_map_hash() -> str:
    hasher = hashlib.sha256()
    # Sort items by key to ensure consistent ordering
    for key in sorted(SEMANTIC_MAP.keys()):
        value = SEMANTIC_MAP[key]
        entry = f"{key}=>{value}"
        hasher.update(entry.encode("utf-8"))
    return hasher.hexdigest()


_MAP_INTEGRITY_HASH = _compute_map_hash()


def verify_integrity() -> dict:
    current_count = len(SEMANTIC_MAP)
    current_hash = _compute_map_hash()
    is_valid = (current_count == _EXPECTED_ENTRY_COUNT) and (current_hash == _MAP_INTEGRITY_HASH)
    return {
        "status": "ok" if is_valid else "corrupted",
        "entries": current_count,
        "expected_entries": _EXPECTED_ENTRY_COUNT,
        "hash": current_hash,
        "expected_hash": _MAP_INTEGRITY_HASH,
        "is_valid": is_valid,
    }


def normalize_term(term: str) -> str:
    """
    Normalize a domain term to its canonical form.
    Returns the normalized form if found, else returns the term lowercased.
    """
    term_lower = term.strip().lower()
    return SEMANTIC_MAP.get(term_lower, term_lower)


def get_related_terms(term: str) -> list[str]:
    """
    Return a list of terms that map to the same normalized form as the input term.
    If term not found, returns empty list.
    """
    normalized = normalize_term(term)
    related = [k for k, v in SEMANTIC_MAP.items() if v == normalized]
    return related


def get_all_mappings() -> dict:
    """
    Return a copy of the entire semantic map dictionary.
    """
    return SEMANTIC_MAP.copy()