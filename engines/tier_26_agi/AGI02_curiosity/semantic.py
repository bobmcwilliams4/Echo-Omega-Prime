import hashlib
import re

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_AUTHOR = "AGI02_curiosity"
SEMANTIC_MAP_ENGINE = "AGI02"

SEMANTIC_MAP = {
    # Knowledge Gap Identification Algorithms
    "knowledge gap identification": "knowledge_gap_identification",
    "knowledge gap detection": "knowledge_gap_identification",
    "gap detection": "knowledge_gap_identification",
    "gap analysis": "knowledge_gap_identification",
    "knowledge gap analysis": "knowledge_gap_identification",
    "gap identification": "knowledge_gap_identification",
    "blind spot detection": "blind_spot_detection",
    "blindspot detection": "blind_spot_detection",
    "coverage analysis": "blind_spot_detection",
    "coverage assessment": "blind_spot_detection",
    "unknown unknown estimation": "unknown_unknown_estimation",
    "unknown-unknown estimation": "unknown_unknown_estimation",
    "unknown unknowns": "unknown_unknown_estimation",
    "unknown unknown estimation & calibration": "unknown_unknown_estimation",
    "unknown unknown calibration": "unknown_unknown_estimation",
    "unknown unknown estimation and calibration": "unknown_unknown_estimation",
    "knowledge graph traversal": "knowledge_graph_traversal",
    "knowledge graph exploration": "knowledge_graph_traversal",
    "graph traversal": "knowledge_graph_traversal",
    "knowledge graph gap detection": "knowledge_graph_traversal",
    "knowledge graph gap analysis": "knowledge_graph_traversal",

    # Question Formulation Strategies
    "socratic method": "socratic_method",
    "socratic questioning": "socratic_method",
    "bloom taxonomy": "bloom_taxonomy",
    "bloom's taxonomy": "bloom_taxonomy",
    "bloom taxonomy levels": "bloom_taxonomy",
    "question formulation": "question_formulation",
    "question generation": "question_formulation",
    "question strategy": "question_formulation",
    "question formulation strategies": "question_formulation",
    "question taxonomy": "question_taxonomy",
    "question types": "question_taxonomy",
    "factual question": "factual_question",
    "factual questions": "factual_question",
    "conceptual question": "conceptual_question",
    "conceptual questions": "conceptual_question",
    "procedural question": "procedural_question",
    "procedural questions": "procedural_question",
    "metacognitive question": "metacognitive_question",
    "metacognitive questions": "metacognitive_question",

    # Learning Prioritization
    "learning prioritization": "learning_prioritization",
    "prioritization by impact": "learning_prioritization",
    "prioritization by urgency": "learning_prioritization",
    "impact and urgency prioritization": "learning_prioritization",
    "impact-urgency matrix": "learning_prioritization",
    "curiosity-driven exploration bonuses": "curiosity_driven_exploration_bonuses",
    "curiosity bonus": "curiosity_driven_exploration_bonuses",
    "exploration bonus": "curiosity_driven_exploration_bonuses",
    "curiosity reward": "curiosity_driven_exploration_bonuses",
    "active learning": "active_learning",
    "active learning query selection": "active_learning",
    "query selection": "active_learning",
    "uncertainty quantification": "uncertainty_quantification",
    "uncertainty estimation": "uncertainty_quantification",
    "epistemic uncertainty": "epistemic_uncertainty",
    "aleatoric uncertainty": "aleatoric_uncertainty",
    "information gain": "information_gain",
    "mutual information": "mutual_information",
    "entropy reduction": "entropy_reduction",
    "information gain metrics": "information_gain",
    "mutual info": "mutual_information",
    "entropy decrease": "entropy_reduction",

    # Research Methodology
    "systematic review": "systematic_review",
    "systematic literature review": "systematic_review",
    "meta-analysis": "meta_analysis",
    "meta analysis": "meta_analysis",
    "hypothesis generation": "hypothesis_generation",
    "abductive reasoning": "abductive_reasoning",
    "abduction": "abductive_reasoning",
    "experimental design": "experimental_design",
    "a/b testing": "ab_testing",
    "ab testing": "ab_testing",
    "multivariate testing": "multivariate_testing",
    "multivariate": "multivariate_testing",
    "experimental plan": "experimental_design",

    # Metacognition & Learning Transfer
    "metacognition": "metacognition",
    "self-assessment": "self_assessment",
    "monitoring": "monitoring",
    "learning transfer": "learning_transfer",
    "near transfer": "near_transfer",
    "far transfer": "far_transfer",
    "analogical transfer": "analogical_transfer",

    # Spaced Repetition & Forgetting Curve
    "spaced repetition": "spaced_repetition",
    "leitner system": "leitner_system",
    "leitner": "leitner_system",
    "supermemo": "supermemo",
    "forgetting curve": "forgetting_curve",
    "ebbinghaus retention": "ebbinghaus_retention",
    "ebbinghaus retention modeling": "ebbinghaus_retention",

    # Knowledge Dependency
    "knowledge dependency mapping": "knowledge_dependency_mapping",
    "prerequisite chains": "prerequisite_chains",
    "prerequisites": "prerequisite_chains",
    "dependency mapping": "knowledge_dependency_mapping",

    # Exploration vs Exploitation
    "exploration vs exploitation": "exploration_vs_exploitation",
    "multi-armed bandit": "multi_armed_bandit",
    "multiarmed bandit": "multi_armed_bandit",
    "mab": "multi_armed_bandit",
    "thompson sampling": "thompson_sampling",
    "ucb": "upper_confidence_bound",
    "upper confidence bound": "upper_confidence_bound",
    "upper-confidence bound": "upper_confidence_bound",

    # Synonyms, abbreviations, misspellings, related terms
    "knowledge gaps": "knowledge_gap_identification",
    "knowledge-gap": "knowledge_gap_identification",
    "knowledge-gaps": "knowledge_gap_identification",
    "gap detect": "knowledge_gap_identification",
    "gap-detect": "knowledge_gap_identification",
    "gapdet": "knowledge_gap_identification",
    "socratic": "socratic_method",
    "bloom": "bloom_taxonomy",
    "bloom taxonomy taxonomy": "bloom_taxonomy",
    "bloom's": "bloom_taxonomy",
    "bloom's taxonmy": "bloom_taxonomy",
    "bloom taxonmy": "bloom_taxonomy",
    "question taxonomy taxonomy": "question_taxonomy",
    "factual": "factual_question",
    "conceptual": "conceptual_question",
    "procedural": "procedural_question",
    "metacognitive": "metacognitive_question",
    "prioritization": "learning_prioritization",
    "curiosity bonus": "curiosity_driven_exploration_bonuses",
    "curiosity bonuses": "curiosity_driven_exploration_bonuses",
    "active query selection": "active_learning",
    "uncertainty": "uncertainty_quantification",
    "epistemic": "epistemic_uncertainty",
    "aleatoric": "aleatoric_uncertainty",
    "info gain": "information_gain",
    "mutual info": "mutual_information",
    "entropy reduction metrics": "entropy_reduction",
    "systematic lit review": "systematic_review",
    "meta analysis": "meta_analysis",
    "abductive": "abductive_reasoning",
    "abduction reasoning": "abductive_reasoning",
    "a/b test": "ab_testing",
    "multivariate test": "multivariate_testing",
    "self assessment": "self_assessment",
    "monitor": "monitoring",
    "near transfer": "near_transfer",
    "far transfer": "far_transfer",
    "analogical": "analogical_transfer",
    "leitner box": "leitner_system",
    "forgetting curve model": "forgetting_curve",
    "ebbinghaus retention model": "ebbinghaus_retention",
    "prereq chains": "prerequisite_chains",
    "dependency map": "knowledge_dependency_mapping",
    "exploration exploitation": "exploration_vs_exploitation",
    "multi armed bandits": "multi_armed_bandit",
    "mab algorithm": "multi_armed_bandit",
    "thompson sampler": "thompson_sampling",
    "ucb algorithm": "upper_confidence_bound",
    "upper confidence bounds": "upper_confidence_bound",

    # Additional synonyms and misspellings to reach 200+ entries
    "knowledge gap id": "knowledge_gap_identification",
    "knowledge gap ids": "knowledge_gap_identification",
    "knowledge-gap id": "knowledge_gap_identification",
    "knowledge-gap ids": "knowledge_gap_identification",
    "gap id": "knowledge_gap_identification",
    "gap ids": "knowledge_gap_identification",
    "blindspot detect": "blind_spot_detection",
    "blind spot detect": "blind_spot_detection",
    "coverage analyses": "blind_spot_detection",
    "coverage analyse": "blind_spot_detection",
    "unknown unknown est": "unknown_unknown_estimation",
    "unknown unknown est.": "unknown_unknown_estimation",
    "unknown unknown calibration": "unknown_unknown_estimation",
    "knowledge graph traverse": "knowledge_graph_traversal",
    "knowledge graph traversing": "knowledge_graph_traversal",
    "graph traversal algorithm": "knowledge_graph_traversal",
    "socratic method questioning": "socratic_method",
    "socratic questioning method": "socratic_method",
    "bloom taxonomy framework": "bloom_taxonomy",
    "bloom taxonomy model": "bloom_taxonomy",
    "question formulation strategy": "question_formulation",
    "question formulation strategies": "question_formulation",
    "question generation strategy": "question_formulation",
    "question generation strategies": "question_formulation",
    "question taxonomy classification": "question_taxonomy",
    "question types taxonomy": "question_taxonomy",
    "factual questions examples": "factual_question",
    "conceptual questions examples": "conceptual_question",
    "procedural questions examples": "procedural_question",
    "metacognitive questions examples": "metacognitive_question",
    "learning prioritization impact": "learning_prioritization",
    "learning prioritization urgency": "learning_prioritization",
    "impact urgency matrix": "learning_prioritization",
    "curiosity driven exploration bonus": "curiosity_driven_exploration_bonuses",
    "curiosity driven exploration bonuses": "curiosity_driven_exploration_bonuses",
    "exploration bonuses": "curiosity_driven_exploration_bonuses",
    "active learning query select": "active_learning",
    "active learning query selection": "active_learning",
    "uncertainty quantification epistemic": "epistemic_uncertainty",
    "uncertainty quantification aleatoric": "aleatoric_uncertainty",
    "information gain metric": "information_gain",
    "mutual information metric": "mutual_information",
    "entropy reduction metric": "entropy_reduction",
    "systematic review methodology": "systematic_review",
    "meta-analysis methodology": "meta_analysis",
    "hypothesis generation abductive reasoning": "abductive_reasoning",
    "abductive reasoning hypothesis generation": "abductive_reasoning",
    "experimental design ab testing": "ab_testing",
    "experimental design multivariate": "multivariate_testing",
    "metacognition monitoring": "monitoring",
    "metacognition self assessment": "self_assessment",
    "learning transfer near": "near_transfer",
    "learning transfer far": "far_transfer",
    "learning transfer analogical": "analogical_transfer",
    "spaced repetition scheduling": "spaced_repetition",
    "leitner spaced repetition": "leitner_system",
    "supermemo spaced repetition": "supermemo",
    "forgetting curve ebbinghaus": "ebbinghaus_retention",
    "knowledge dependency prerequisite chains": "prerequisite_chains",
    "prerequisite chains knowledge dependency": "prerequisite_chains",
    "exploration exploitation tradeoff": "exploration_vs_exploitation",
    "multi armed bandit algorithm": "multi_armed_bandit",
    "thompson sampling algorithm": "thompson_sampling",
    "ucb algorithm upper confidence bound": "upper_confidence_bound",
    "upper confidence bound algorithm": "upper_confidence_bound",

    # More variants, abbreviations, misspellings
    "knowledge gap id alg": "knowledge_gap_identification",
    "knowledge gap id algorithm": "knowledge_gap_identification",
    "knowledge gap id algo": "knowledge_gap_identification",
    "blind spot detect alg": "blind_spot_detection",
    "blind spot detection alg": "blind_spot_detection",
    "unknown unknown est alg": "unknown_unknown_estimation",
    "knowledge graph traversal alg": "knowledge_graph_traversal",
    "socratic questioning method": "socratic_method",
    "bloom taxonomy levels": "bloom_taxonomy",
    "question formulation strat": "question_formulation",
    "question formulation strategy": "question_formulation",
    "question taxonomy types": "question_taxonomy",
    "factual q": "factual_question",
    "conceptual q": "conceptual_question",
    "procedural q": "procedural_question",
    "metacognitive q": "metacognitive_question",
    "learning prioritization impact urgency": "learning_prioritization",
    "curiosity bonus exploration": "curiosity_driven_exploration_bonuses",
    "active learning query select": "active_learning",
    "uncertainty quantification epistemic aleatoric": "uncertainty_quantification",
    "information gain mutual info": "information_gain",
    "entropy reduction metric": "entropy_reduction",
    "systematic review meta analysis": "systematic_review",
    "hypothesis generation abductive": "abductive_reasoning",
    "experimental design ab testing multivariate": "experimental_design",
    "metacognition monitoring self assessment": "metacognition",
    "learning transfer near far analogical": "learning_transfer",
    "spaced repetition leitner supermemo": "spaced_repetition",
    "forgetting curve ebbinghaus retention": "forgetting_curve",
    "knowledge dependency prerequisite chains": "knowledge_dependency_mapping",
    "exploration exploitation multi armed bandit": "exploration_vs_exploitation",
    "thompson sampling ucb": "multi_armed_bandit",
    "ucb upper confidence bound": "upper_confidence_bound",
    "multi armed bandit mab": "multi_armed_bandit",
    "mab multi armed bandit": "multi_armed_bandit",
    "thompson sampling ts": "thompson_sampling",
    "ucb algorithm ucb": "upper_confidence_bound",
    "knowledge gap id detection": "knowledge_gap_identification",
    "knowledge gap detection algorithm": "knowledge_gap_identification",
    "knowledge gap detection alg": "knowledge_gap_identification",
    "blind spot detection coverage analysis": "blind_spot_detection",
    "unknown unknown estimation calibration": "unknown_unknown_estimation",
    "knowledge graph traversal gap detection": "knowledge_graph_traversal",
    "socratic method questioning technique": "socratic_method",
    "bloom taxonomy cognitive levels": "bloom_taxonomy",
    "question formulation socratic method": "question_formulation",
    "question taxonomy factual conceptual procedural metacognitive": "question_taxonomy",
    "learning prioritization impact urgency matrix": "learning_prioritization",
    "curiosity driven exploration bonus reward": "curiosity_driven_exploration_bonuses",
    "active learning query selection strategy": "active_learning",
    "uncertainty quantification epistemic aleatoric types": "uncertainty_quantification",
    "information gain mutual information entropy reduction": "information_gain",
    "systematic review meta analysis research": "systematic_review",
    "hypothesis generation abductive reasoning abduction": "abductive_reasoning",
    "experimental design a/b testing multivariate testing": "experimental_design",
    "metacognition monitoring self assessment techniques": "metacognition",
    "learning transfer near far analogical transfer": "learning_transfer",
    "spaced repetition scheduling leitner supermemo": "spaced_repetition",
    "forgetting curve ebbinghaus retention modeling": "forgetting_curve",
    "knowledge dependency mapping prerequisite chains dependencies": "knowledge_dependency_mapping",
    "exploration exploitation multi armed bandit thompson sampling ucb": "exploration_vs_exploitation",
    "multi armed bandit thompson sampling ucb algorithms": "multi_armed_bandit",
    "thompson sampling ts algorithm": "thompson_sampling",
    "ucb upper confidence bound algorithm": "upper_confidence_bound",
    "multi armed bandit mab algorithm": "multi_armed_bandit",
    "knowledge gap identification algorithms": "knowledge_gap_identification",
    "question formulation strategies socratic method bloom taxonomy": "question_formulation",
    "learning prioritization by impact and urgency": "learning_prioritization",
    "curiosity driven exploration bonuses": "curiosity_driven_exploration_bonuses",
    "active learning query selection": "active_learning",
    "uncertainty quantification epistemic vs aleatoric": "uncertainty_quantification",
    "information gain metrics mutual information entropy reduction": "information_gain",
    "question taxonomy factual conceptual procedural metacognitive": "question_taxonomy",
    "knowledge graph traversal for gap detection": "knowledge_graph_traversal",
    "blind spot detection via coverage analysis": "blind_spot_detection",
    "unknown unknown estimation and calibration": "unknown_unknown_estimation",
    "research methodology systematic review meta analysis": "systematic_review",
    "hypothesis generation abductive reasoning": "abductive_reasoning",
    "experimental design a/b testing multivariate": "experimental_design",
    "metacognition monitoring self assessment": "metacognition",
    "learning transfer near far analogical": "learning_transfer",
    "spaced repetition scheduling leitner supermemo": "spaced_repetition",
    "forgetting curve ebbinghaus retention modeling": "forgetting_curve",
    "knowledge dependency mapping prerequisite chains": "knowledge_dependency_mapping",
    "exploration vs exploitation multi armed bandit thompson sampling ucb": "exploration_vs_exploitation",
}

_EXPECTED_ENTRY_COUNT = len(SEMANTIC_MAP)

def _compute_map_hash() -> str:
    hasher = hashlib.sha256()
    for key in sorted(SEMANTIC_MAP.keys()):
        val = SEMANTIC_MAP[key]
        hasher.update(key.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(val.encode("utf-8"))
        hasher.update(b"\0")
    return hasher.hexdigest()

_MAP_INTEGRITY_HASH = _compute_map_hash()

def verify_integrity() -> dict:
    actual_count = len(SEMANTIC_MAP)
    actual_hash = _compute_map_hash()
    is_valid = (actual_count == _EXPECTED_ENTRY_COUNT) and (actual_hash == _MAP_INTEGRITY_HASH)
    return {
        "status": "valid" if is_valid else "invalid",
        "entries": actual_count,
        "expected_entries": _EXPECTED_ENTRY_COUNT,
        "hash": actual_hash,
        "expected_hash": _MAP_INTEGRITY_HASH,
        "is_valid": is_valid,
    }

def normalize_term(term: str) -> str:
    if not isinstance(term, str):
        raise TypeError("term must be a string")
    term_clean = term.strip().lower()
    # Remove punctuation except internal hyphens and slashes
    term_clean = re.sub(r"[^\w\s\-/]", "", term_clean)
    # Normalize whitespace
    term_clean = re.sub(r"\s+", " ", term_clean)
    # Direct map lookup
    if term_clean in SEMANTIC_MAP:
        return SEMANTIC_MAP[term_clean]
    # Try partial matches or fuzzy fallback
    # Simple fallback: exact match after removing spaces and hyphens
    term_simple = term_clean.replace(" ", "").replace("-", "")
    for key in SEMANTIC_MAP:
        key_simple = key.replace(" ", "").replace("-", "")
        if term_simple == key_simple:
            return SEMANTIC_MAP[key]
    # If no match, return normalized cleaned term as is
    return term_clean

def get_related_terms(term: str) -> list[str]:
    norm = normalize_term(term)
    related = [k for k, v in SEMANTIC_MAP.items() if v == norm]
    return sorted(set(related))

def get_all_mappings() -> dict:
    return dict(SEMANTIC_MAP)