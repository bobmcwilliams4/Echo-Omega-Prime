"""
R02 Permit Analyzer - Semantic Normalization
Deterministic term normalization for permit-related queries.

GOVERNANCE NOTICE:
This layer is preprocessing only. Fully deterministic.
No probabilistic models. No vector inference. No auto-learning.

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import re
from loguru import logger


# ==============================================================================
# SEMANTIC NORMALIZATION RESULT
# ==============================================================================

@dataclass
class NormalizationResult:
    """Result of semantic normalization with tracking."""
    original_query: str
    normalized_query: str
    permit_types_detected: List[str]
    regulatory_bodies: List[str]
    operation_types: List[str]
    depth_indicators: Dict[str, Optional[int]]
    location_indicators: Dict[str, str]
    substitutions_made: List[Dict[str, str]]
    normalization_confidence: float


# ==============================================================================
# PERMIT TYPE DETECTION
# ==============================================================================

class PermitType(Enum):
    """Standardized permit type classifications."""
    DRILLING_W1 = "drilling_w1"
    DRILLING_W1A = "drilling_w1a"
    RULE_37_EXCEPTION = "rule_37_exception"
    RULE_38_DENSITY = "rule_38_density"
    INJECTION_UIC = "injection_uic"
    DISPOSAL_SWD = "disposal_swd"
    ENHANCED_RECOVERY = "enhanced_recovery"
    PIPELINE_T4 = "pipeline_t4"
    SURFACE_CASING = "surface_casing"
    AIR_QUALITY = "air_quality"
    STORMWATER = "stormwater"
    FLARING = "flaring"
    VENTING = "venting"
    EMERGENCY = "emergency"
    TEMPORARY = "temporary"
    AMENDMENT = "amendment"
    RENEWAL = "renewal"
    TRANSFER = "transfer"
    ROW = "right_of_way"
    COUNTY_ROAD = "county_road_crossing"
    H2S_CONTINGENCY = "h2s_contingency"


# ==============================================================================
# SEMANTIC DICTIONARY
# ==============================================================================

PERMIT_TERM_DICTIONARY = {
    # Drilling permits
    r'\b(w-?1a?)\b': 'drilling_permit_w1',
    r'\bdrilling\s+permit\b': 'drilling_permit_w1',
    r'\bpermit\s+to\s+drill\b': 'drilling_permit_w1',
    r'\bapplication\s+to\s+drill\b': 'drilling_permit_w1',

    # Spacing and density
    r'\brule\s*37\b': 'rule_37_spacing_exception',
    r'\bspacing\s+exception\b': 'rule_37_spacing_exception',
    r'\bdensity\s+exception\b': 'rule_38_density',
    r'\brule\s*38\b': 'rule_38_density',

    # Injection and disposal
    r'\b(swds?|salt\s*water\s+disposal)\b': 'disposal_well_swd',
    r'\bdisposal\s+well\b': 'disposal_well_swd',
    r'\binjection\s+well\b': 'injection_well_uic',
    r'\buic\s+permit\b': 'injection_well_uic',
    r'\bclass\s*ii\s+well\b': 'injection_well_uic',
    r'\benhanced\s+recovery\b': 'enhanced_recovery',
    r'\bwater\s?flood\b': 'enhanced_recovery',

    # Pipeline
    r'\bt-?4\s+permit\b': 'pipeline_t4',
    r'\bpipeline\s+permit\b': 'pipeline_t4',
    r'\bgathering\s+line\b': 'pipeline_t4',

    # Environmental
    r'\bair\s+quality\b': 'air_quality_permit',
    r'\btceq\b': 'tceq_permit',
    r'\bstorm\s*water\b': 'stormwater_permit',
    r'\bflaring\b': 'flaring_permit',
    r'\bventing\b': 'venting_permit',

    # Casing and safety
    r'\bsurface\s+casing\b': 'surface_casing_requirement',
    r'\bh2s\b': 'h2s_contingency',
    r'\bsour\s+gas\b': 'h2s_contingency',

    # Permit actions
    r'\bamendment\b': 'permit_amendment',
    r'\brenewal\b': 'permit_renewal',
    r'\btransfer\b': 'permit_transfer',
    r'\bemergency\s+permit\b': 'emergency_permit',
    r'\btemporary\s+permit\b': 'temporary_permit',

    # Right of way
    r'\bright\s+of\s+way\b': 'right_of_way',
    r'\br\.?o\.?w\.?\b': 'right_of_way',
    r'\bcounty\s+road\s+crossing\b': 'county_road_crossing',

    # Regulatory bodies
    r'\b(rrc|railroad\s+commission)\b': 'texas_railroad_commission',
    r'\btceq\b': 'texas_commission_environmental_quality',
    r'\bepa\b': 'environmental_protection_agency',
    r'\busace\b': 'us_army_corps_engineers',
    r'\bglo\b': 'general_land_office',

    # Operation types
    r'\bhorizontal\s+well\b': 'horizontal_drilling',
    r'\bvertical\s+well\b': 'vertical_drilling',
    r'\bdeviated\s+well\b': 'deviated_drilling',
    r'\bworkover\b': 'workover_operation',
    r'\brecompletion\b': 'recompletion',
    r'\bplugback\b': 'plugback',

    # Depth indicators
    r'\bdeep\s+well\b': 'deep_well_indicator',
    r'\bshallow\s+well\b': 'shallow_well_indicator',
    r'\bfreshwater\s+zone\b': 'freshwater_protection_zone',

    # Location
    r'\boffshore\b': 'offshore_location',
    r'\bonshore\b': 'onshore_location',
    r'\burban\s+area\b': 'urban_location',
}


# ==============================================================================
# NORMALIZATION ENGINE
# ==============================================================================

class SemanticNormalizer:
    """
    Deterministic semantic normalization for permit queries.
    Standardizes terminology, detects permit types, extracts key indicators.
    """

    def __init__(self):
        self.dictionary = PERMIT_TERM_DICTIONARY
        logger.info(f"Semantic normalizer initialized with {len(self.dictionary)} patterns")

    def normalize(self, query: str) -> NormalizationResult:
        """
        Apply semantic normalization to query text.
        Returns normalized text with metadata.
        """
        original_query = query
        normalized = query.lower().strip()
        substitutions = []
        permit_types = set()
        regulatory_bodies = set()
        operation_types = set()

        # Apply dictionary substitutions
        for pattern, replacement in self.dictionary.items():
            matches = list(re.finditer(pattern, normalized, re.IGNORECASE))
            if matches:
                for match in matches:
                    substitutions.append({
                        "original": match.group(0),
                        "replacement": replacement,
                        "position": match.start()
                    })

                    # Categorize by type
                    if "permit" in replacement or "rule_" in replacement or "swd" in replacement:
                        permit_types.add(replacement)
                    elif "texas_" in replacement or "environmental" in replacement or "army" in replacement:
                        regulatory_bodies.add(replacement)
                    elif "drilling" in replacement or "workover" in replacement or "recompletion" in replacement:
                        operation_types.add(replacement)

                # Perform substitution
                normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)

        # Extract depth indicators
        depth_indicators = self._extract_depth_indicators(normalized)

        # Extract location indicators
        location_indicators = self._extract_location_indicators(normalized)

        # Calculate normalization confidence
        confidence = self._calculate_confidence(
            len(substitutions),
            len(permit_types),
            len(regulatory_bodies)
        )

        return NormalizationResult(
            original_query=original_query,
            normalized_query=normalized,
            permit_types_detected=sorted(list(permit_types)),
            regulatory_bodies=sorted(list(regulatory_bodies)),
            operation_types=sorted(list(operation_types)),
            depth_indicators=depth_indicators,
            location_indicators=location_indicators,
            substitutions_made=substitutions,
            normalization_confidence=confidence
        )

    def _extract_depth_indicators(self, normalized: str) -> Dict[str, Optional[int]]:
        """Extract depth references from query."""
        depth_info = {
            "total_depth": None,
            "casing_depth": None,
            "freshwater_depth": None
        }

        # Total depth pattern
        td_match = re.search(r'(\d{3,5})\s*(?:ft|feet|\')\s+(?:td|total\s+depth)', normalized)
        if td_match:
            depth_info["total_depth"] = int(td_match.group(1))

        # Casing depth
        casing_match = re.search(r'casing\s+(?:at\s+)?(\d{3,5})\s*(?:ft|feet|\')', normalized)
        if casing_match:
            depth_info["casing_depth"] = int(casing_match.group(1))

        # Freshwater protection depth
        fw_match = re.search(r'(?:freshwater|usable\s+water).*?(\d{3,5})\s*(?:ft|feet|\')', normalized)
        if fw_match:
            depth_info["freshwater_depth"] = int(fw_match.group(1))

        return depth_info

    def _extract_location_indicators(self, normalized: str) -> Dict[str, str]:
        """Extract location context from query."""
        location_info = {}

        # County detection
        county_match = re.search(r'(\w+)\s+county', normalized, re.IGNORECASE)
        if county_match:
            location_info["county"] = county_match.group(1).title()

        # Field detection
        field_match = re.search(r'(\w+)\s+field', normalized, re.IGNORECASE)
        if field_match:
            location_info["field"] = field_match.group(1).title()

        # District
        district_match = re.search(r'district\s+(\d+[a-z]?)', normalized, re.IGNORECASE)
        if district_match:
            location_info["rrc_district"] = district_match.group(1).upper()

        return location_info

    def _calculate_confidence(
        self,
        substitution_count: int,
        permit_type_count: int,
        regulatory_body_count: int
    ) -> float:
        """
        Calculate normalization confidence score.
        Higher score indicates more semantic clarity.
        """
        # Base score from substitutions
        base_score = min(0.6, substitution_count * 0.1)

        # Bonus for detected permit types
        permit_bonus = min(0.3, permit_type_count * 0.15)

        # Bonus for regulatory body mentions
        regulatory_bonus = min(0.1, regulatory_body_count * 0.05)

        confidence = base_score + permit_bonus + regulatory_bonus

        return min(1.0, confidence)


# ==============================================================================
# PUBLIC API
# ==============================================================================

_normalizer_instance: Optional[SemanticNormalizer] = None


def get_normalizer() -> SemanticNormalizer:
    """Get global semantic normalizer instance."""
    global _normalizer_instance
    if _normalizer_instance is None:
        _normalizer_instance = SemanticNormalizer()
    return _normalizer_instance


def normalize_semantics(query: str) -> NormalizationResult:
    """Normalize query semantics (convenience function)."""
    return get_normalizer().normalize(query)
