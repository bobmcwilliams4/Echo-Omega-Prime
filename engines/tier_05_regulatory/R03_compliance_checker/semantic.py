"""
Semantic Normalization Module
R03 Compliance Checker Engine

Domain-specific term normalization for regulatory compliance queries
"""

from typing import Dict, List, Set
import re


# Regulatory Authority Synonyms
AUTHORITY_SYNONYMS = {
    "railroad commission": "RRC",
    "texas railroad commission": "RRC",
    "commission": "RRC",
    "tceq": "TCEQ",
    "texas commission on environmental quality": "TCEQ",
    "environmental quality": "TCEQ",
    "epa": "EPA",
    "environmental protection agency": "EPA",
    "osha": "OSHA",
    "occupational safety": "OSHA",
    "dot": "DOT",
    "department of transportation": "DOT",
    "phmsa": "DOT_PHMSA",
}

# Compliance Topic Synonyms
TOPIC_SYNONYMS = {
    "production report": "P-4",
    "monthly report": "P-4",
    "p4": "P-4",
    "organization report": "P-5",
    "p5": "P-5",
    "plugging notice": "W-3A",
    "w3a": "W-3A",
    "plugging certificate": "W-3",
    "completion report": "W-2",
    "hydrogen sulfide": "H2S",
    "sour gas": "H2S",
    "spill prevention": "SPCC",
    "spcc plan": "SPCC",
    "permit by rule": "PBR",
    "pbr": "PBR",
    "new source performance": "NSPS",
    "nsps": "NSPS",
    "leak detection": "LDAR",
    "ldar": "LDAR",
    "surface casing": "SURFACE_CASING",
    "pit liner": "PIT_LINER",
    "earthen pit": "PIT_LINER",
}

# Equipment and Facility Terms
EQUIPMENT_SYNONYMS = {
    "storage tank": "TANK",
    "oil tank": "TANK",
    "production tank": "TANK",
    "tank battery": "TANK_BATTERY",
    "pneumatic controller": "PNEUMATIC_CONTROLLER",
    "gas-actuated controller": "PNEUMATIC_CONTROLLER",
    "dehydrator": "DEHYDRATOR",
    "glycol dehydrator": "DEHYDRATOR",
    "flare": "FLARE",
    "combustor": "FLARE",
    "engine": "ENGINE",
    "compressor": "ENGINE",
}

# Pollutant Synonyms
POLLUTANT_SYNONYMS = {
    "volatile organic compounds": "VOC",
    "voc": "VOC",
    "nitrogen oxides": "NOX",
    "nox": "NOX",
    "carbon monoxide": "CO",
    "methane": "CH4",
    "hazardous air pollutants": "HAP",
    "haps": "HAP",
}

# Regulatory Action Synonyms
ACTION_SYNONYMS = {
    "violation": "VIOLATION",
    "non-compliance": "VIOLATION",
    "penalty": "PENALTY",
    "fine": "PENALTY",
    "enforcement": "ENFORCEMENT",
    "inspection": "INSPECTION",
    "audit": "AUDIT",
}

# Time-related Synonyms
TIME_SYNONYMS = {
    "deadline": "DEADLINE",
    "due date": "DEADLINE",
    "reporting period": "REPORTING_PERIOD",
    "annual": "ANNUAL",
    "monthly": "MONTHLY",
    "quarterly": "QUARTERLY",
    "immediate": "IMMEDIATE",
}


class SemanticNormalizer:
    """Normalize regulatory compliance queries to canonical forms."""

    def __init__(self):
        self.all_synonyms = {
            **AUTHORITY_SYNONYMS,
            **TOPIC_SYNONYMS,
            **EQUIPMENT_SYNONYMS,
            **POLLUTANT_SYNONYMS,
            **ACTION_SYNONYMS,
            **TIME_SYNONYMS,
        }

        # Compile regex patterns for common regulatory references
        self.rule_pattern = re.compile(r'\b(rule|statewide rule|district rule)\s*(\d+)', re.IGNORECASE)
        self.form_pattern = re.compile(r'\b(form|rrc form)\s*([a-z]-?\d+[a-z]?)', re.IGNORECASE)
        self.cfr_pattern = re.compile(r'\b(\d+)\s*cfr\s*(\d+(?:\.\d+)?)', re.IGNORECASE)
        self.tac_pattern = re.compile(r'\b(\d+)\s*tac\s*(?:§|section)?\s*(\d+(?:\.\d+)?)', re.IGNORECASE)

    def normalize(self, query: str) -> str:
        """
        Normalize a compliance query to canonical terminology.

        Args:
            query: Raw user query

        Returns:
            Normalized query with canonical terms
        """
        normalized = query.lower()

        # Normalize regulatory references
        normalized = self._normalize_rules(normalized)
        normalized = self._normalize_forms(normalized)
        normalized = self._normalize_citations(normalized)

        # Apply synonym replacements
        for synonym, canonical in self.all_synonyms.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(synonym) + r'\b'
            normalized = re.sub(pattern, canonical, normalized, flags=re.IGNORECASE)

        return normalized

    def _normalize_rules(self, text: str) -> str:
        """Normalize RRC rule references to standard format."""
        def replace_rule(match):
            rule_num = match.group(2)
            return f"RULE_{rule_num}"

        return self.rule_pattern.sub(replace_rule, text)

    def _normalize_forms(self, text: str) -> str:
        """Normalize RRC form references to standard format."""
        def replace_form(match):
            form_id = match.group(2).upper().replace('-', '')
            return f"FORM_{form_id}"

        return self.form_pattern.sub(replace_form, text)

    def _normalize_citations(self, text: str) -> str:
        """Normalize CFR and TAC citations to standard format."""
        # CFR citations
        def replace_cfr(match):
            title = match.group(1)
            part = match.group(2)
            return f"{title}_CFR_{part}"

        text = self.cfr_pattern.sub(replace_cfr, text)

        # TAC citations
        def replace_tac(match):
            title = match.group(1)
            section = match.group(2)
            return f"{title}_TAC_{section}"

        text = self.tac_pattern.sub(replace_tac, text)

        return text

    def extract_entities(self, query: str) -> Dict[str, List[str]]:
        """
        Extract regulatory entities from query.

        Returns:
            Dictionary with entity types as keys and lists of entities as values
        """
        entities = {
            "authorities": [],
            "forms": [],
            "rules": [],
            "citations": [],
            "pollutants": [],
            "equipment": [],
        }

        query_lower = query.lower()

        # Extract authorities
        for synonym, canonical in AUTHORITY_SYNONYMS.items():
            if synonym in query_lower and canonical not in entities["authorities"]:
                entities["authorities"].append(canonical)

        # Extract forms
        for match in self.form_pattern.finditer(query):
            form_id = match.group(2).upper().replace('-', '')
            entities["forms"].append(f"FORM_{form_id}")

        # Extract rules
        for match in self.rule_pattern.finditer(query):
            rule_num = match.group(2)
            entities["rules"].append(f"RULE_{rule_num}")

        # Extract CFR citations
        for match in self.cfr_pattern.finditer(query):
            title = match.group(1)
            part = match.group(2)
            entities["citations"].append(f"{title}_CFR_{part}")

        # Extract TAC citations
        for match in self.tac_pattern.finditer(query):
            title = match.group(1)
            section = match.group(2)
            entities["citations"].append(f"{title}_TAC_{section}")

        # Extract pollutants
        for synonym, canonical in POLLUTANT_SYNONYMS.items():
            if synonym in query_lower and canonical not in entities["pollutants"]:
                entities["pollutants"].append(canonical)

        # Extract equipment
        for synonym, canonical in EQUIPMENT_SYNONYMS.items():
            if synonym in query_lower and canonical not in entities["equipment"]:
                entities["equipment"].append(canonical)

        return entities

    def identify_compliance_zone(self, query: str) -> str:
        """
        Identify the compliance zone for the query.

        Returns:
            One of: PREVENTIVE, OPERATIONAL, REMEDIAL, AUDIT
        """
        query_lower = query.lower()

        # Preventive zone indicators
        preventive_terms = ['planning', 'before', 'prepare', 'permit application', 'new well', 'upcoming']
        if any(term in query_lower for term in preventive_terms):
            return "PREVENTIVE"

        # Remedial zone indicators
        remedial_terms = ['violation', 'penalty', 'non-compliance', 'correct', 'fix', 'remediate', 'late']
        if any(term in query_lower for term in remedial_terms):
            return "REMEDIAL"

        # Audit zone indicators
        audit_terms = ['audit', 'review', 'verify', 'check compliance', 'inspection', 'assess']
        if any(term in query_lower for term in audit_terms):
            return "AUDIT"

        # Default to operational zone
        return "OPERATIONAL"

    def expand_abbreviations(self, text: str) -> str:
        """
        Expand common regulatory abbreviations to full terms.

        Args:
            text: Text with abbreviations

        Returns:
            Text with expanded abbreviations
        """
        abbreviations = {
            "RRC": "Railroad Commission of Texas",
            "TCEQ": "Texas Commission on Environmental Quality",
            "EPA": "Environmental Protection Agency",
            "OSHA": "Occupational Safety and Health Administration",
            "DOT": "Department of Transportation",
            "PHMSA": "Pipeline and Hazardous Materials Safety Administration",
            "SPCC": "Spill Prevention Control and Countermeasure",
            "PBR": "Permit by Rule",
            "NSPS": "New Source Performance Standards",
            "LDAR": "Leak Detection and Repair",
            "VOC": "Volatile Organic Compounds",
            "NOX": "Nitrogen Oxides",
            "HAP": "Hazardous Air Pollutants",
            "TPY": "Tons Per Year",
            "CFR": "Code of Federal Regulations",
            "TAC": "Texas Administrative Code",
        }

        result = text
        for abbr, expansion in abbreviations.items():
            # Only expand if abbreviation appears as standalone word
            pattern = r'\b' + re.escape(abbr) + r'\b'
            result = re.sub(pattern, f"{abbr} ({expansion})", result)

        return result

    def classify_query_intent(self, query: str) -> str:
        """
        Classify the intent of a compliance query.

        Returns:
            One of: REQUIREMENT_LOOKUP, DEADLINE_CHECK, PENALTY_ASSESSMENT,
                   COMPLIANCE_STATUS, REPORTING_GUIDANCE, PERMIT_QUESTION
        """
        query_lower = query.lower()

        # Deadline checking
        if any(term in query_lower for term in ['when', 'deadline', 'due', 'by when', 'timing']):
            return "DEADLINE_CHECK"

        # Penalty assessment
        if any(term in query_lower for term in ['penalty', 'fine', 'enforcement', 'violation cost']):
            return "PENALTY_ASSESSMENT"

        # Compliance status
        if any(term in query_lower for term in ['compliant', 'comply', 'meet requirement', 'in compliance']):
            return "COMPLIANCE_STATUS"

        # Reporting guidance
        if any(term in query_lower for term in ['how to report', 'filing', 'submit', 'report requirement']):
            return "REPORTING_GUIDANCE"

        # Permit questions
        if any(term in query_lower for term in ['permit', 'authorization', 'approval', 'registration']):
            return "PERMIT_QUESTION"

        # Default to requirement lookup
        return "REQUIREMENT_LOOKUP"


def get_normalizer() -> SemanticNormalizer:
    """Factory function to create normalizer instance."""
    return SemanticNormalizer()
