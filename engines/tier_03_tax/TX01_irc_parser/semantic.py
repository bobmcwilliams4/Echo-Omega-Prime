"""
TX01 IRC Parser Engine - Semantic Normalization
Domain-specific term normalization for IRC statutory language
"""

from typing import Dict, List, Set, Optional
import re
from dataclasses import dataclass


@dataclass
class NormalizationRule:
    """Represents a semantic normalization transformation"""
    canonical_form: str
    variants: List[str]
    context_required: Optional[str] = None


class SemanticNormalizer:
    """Normalize IRC statutory language to canonical forms"""

    def __init__(self):
        self.normalization_rules = self._build_normalization_rules()
        self.statutory_terms = self._build_statutory_terms()
        self.citation_patterns = self._build_citation_patterns()

    def _build_normalization_rules(self) -> Dict[str, NormalizationRule]:
        """Build comprehensive normalization ruleset"""
        rules = {
            "section": NormalizationRule(
                canonical_form="section",
                variants=["sec.", "sec", "§", "sect.", "sect"]
            ),
            "subsection": NormalizationRule(
                canonical_form="subsection",
                variants=["subsec.", "subsec", "sub.", "subdivision"]
            ),
            "paragraph": NormalizationRule(
                canonical_form="paragraph",
                variants=["para.", "para", "¶", "par."]
            ),
            "subparagraph": NormalizationRule(
                canonical_form="subparagraph",
                variants=["subpara.", "subpar.", "sub-paragraph"]
            ),
            "internal_revenue_code": NormalizationRule(
                canonical_form="Internal Revenue Code",
                variants=["IRC", "I.R.C.", "Code", "Title 26"]
            ),
            "treasury_regulation": NormalizationRule(
                canonical_form="Treasury Regulation",
                variants=["Treas. Reg.", "Reg.", "T.D.", "26 CFR"]
            ),
            "revenue_ruling": NormalizationRule(
                canonical_form="Revenue Ruling",
                variants=["Rev. Rul.", "Rev.Rul.", "Revenue Rul.", "RR"]
            ),
            "revenue_procedure": NormalizationRule(
                canonical_form="Revenue Procedure",
                variants=["Rev. Proc.", "Rev.Proc.", "Revenue Proc.", "RP"]
            ),
            "private_letter_ruling": NormalizationRule(
                canonical_form="Private Letter Ruling",
                variants=["PLR", "P.L.R.", "Priv. Ltr. Rul.", "Letter Ruling"]
            ),
            "taxable_year": NormalizationRule(
                canonical_form="taxable year",
                variants=["tax year", "fiscal year", "tax period", "taxable period"]
            ),
            "gross_income": NormalizationRule(
                canonical_form="gross income",
                variants=["GI", "total income", "aggregate income"]
            ),
            "adjusted_gross_income": NormalizationRule(
                canonical_form="adjusted gross income",
                variants=["AGI", "A.G.I."]
            ),
            "taxable_income": NormalizationRule(
                canonical_form="taxable income",
                variants=["TI", "net income subject to tax"]
            ),
            "ordinary_income": NormalizationRule(
                canonical_form="ordinary income",
                variants=["OI", "non-capital income"]
            ),
            "capital_gain": NormalizationRule(
                canonical_form="capital gain",
                variants=["CG", "cap gain", "long-term capital gain", "LTCG", "short-term capital gain", "STCG"]
            ),
            "capital_asset": NormalizationRule(
                canonical_form="capital asset",
                variants=["cap asset", "investment property"]
            ),
            "adjusted_basis": NormalizationRule(
                canonical_form="adjusted basis",
                variants=["basis", "tax basis", "cost basis", "AB"]
            ),
            "amount_realized": NormalizationRule(
                canonical_form="amount realized",
                variants=["AR", "proceeds", "sales proceeds"]
            ),
            "fair_market_value": NormalizationRule(
                canonical_form="fair market value",
                variants=["FMV", "market value", "fair value"]
            ),
            "business_purpose": NormalizationRule(
                canonical_form="business purpose",
                variants=["biz purpose", "commercial purpose", "non-tax purpose"]
            ),
            "economic_substance": NormalizationRule(
                canonical_form="economic substance",
                variants=["econ substance", "substantive effect", "meaningful change"]
            ),
        }
        return rules

    def _build_statutory_terms(self) -> Set[str]:
        """Terms that should never be normalized (preserve as statutory language)"""
        return {
            "shall", "may", "must", "will", "includes", "means", "other than",
            "except", "unless", "provided", "determined", "prescribed", "engaged in",
            "carrying on", "derived from", "attributable to", "with respect to",
            "in connection with", "for purposes of", "subject to", "pursuant to"
        }

    def _build_citation_patterns(self) -> Dict[str, re.Pattern]:
        """Regex patterns for IRC citations and cross-references"""
        return {
            "irc_section": re.compile(r'§\s*(\d+[A-Z]?)(?:\(([a-z])\))?(?:\((\d+)\))?(?:\(([A-Z])\))?(?:\(([ivxlcdm]+)\))?(?:\(([IVXLCDM]+)\))?'),
            "irc_section_alt": re.compile(r'[Ss]ection\s+(\d+[A-Z]?)(?:\(([a-z])\))?(?:\((\d+)\))?(?:\(([A-Z])\))?(?:\(([ivxlcdm]+)\))?(?:\(([IVXLCDM]+)\))?'),
            "reg_citation": re.compile(r'(?:Treas\.\s*Reg\.|§)\s*(\d+)\.(\d+[A-Z]?)-(\d+[A-Z]?)(?:\(([a-z])\))?(?:\((\d+)\))?'),
            "rev_rul": re.compile(r'Rev\.\s*Rul\.\s*(\d{2,4})-(\d+)'),
            "rev_proc": re.compile(r'Rev\.\s*Proc\.\s*(\d{2,4})-(\d+)'),
            "plr": re.compile(r'(?:PLR|Priv\.\s*Ltr\.\s*Rul\.)\s*(\d{9})'),
            "pub_law": re.compile(r'Pub\.\s*L\.\s*(\d+)-(\d+)'),
            "usc_title": re.compile(r'(\d+)\s+U\.?S\.?C\.?\s*§?\s*(\d+)'),
        }

    def normalize_query(self, query: str) -> str:
        """Normalize user query to canonical form"""
        normalized = query

        # Apply normalization rules
        for canonical, rule in self.normalization_rules.items():
            for variant in rule.variants:
                # Case-insensitive replacement but preserve statutory terms
                pattern = re.compile(r'\b' + re.escape(variant) + r'\b', re.IGNORECASE)
                if variant.lower() not in self.statutory_terms:
                    normalized = pattern.sub(rule.canonical_form, normalized)

        # Normalize whitespace
        normalized = re.sub(r'\s+', ' ', normalized).strip()

        return normalized

    def extract_citations(self, text: str) -> Dict[str, List[str]]:
        """Extract all citation types from text"""
        citations = {
            "irc_sections": [],
            "regulations": [],
            "revenue_rulings": [],
            "revenue_procedures": [],
            "plrs": [],
            "public_laws": [],
            "usc_citations": []
        }

        # IRC sections
        for match in self.citation_patterns["irc_section"].finditer(text):
            citations["irc_sections"].append(match.group(0))
        for match in self.citation_patterns["irc_section_alt"].finditer(text):
            citations["irc_sections"].append(match.group(0))

        # Treasury Regulations
        for match in self.citation_patterns["reg_citation"].finditer(text):
            citations["regulations"].append(match.group(0))

        # Revenue Rulings
        for match in self.citation_patterns["rev_rul"].finditer(text):
            citations["revenue_rulings"].append(match.group(0))

        # Revenue Procedures
        for match in self.citation_patterns["rev_proc"].finditer(text):
            citations["revenue_procedures"].append(match.group(0))

        # PLRs
        for match in self.citation_patterns["plr"].finditer(text):
            citations["plrs"].append(match.group(0))

        # Public Laws
        for match in self.citation_patterns["pub_law"].finditer(text):
            citations["public_laws"].append(match.group(0))

        # USC Citations
        for match in self.citation_patterns["usc_title"].finditer(text):
            citations["usc_citations"].append(match.group(0))

        return citations

    def parse_irc_citation(self, citation: str) -> Optional[Dict[str, str]]:
        """Parse IRC citation into hierarchical components"""
        # Try both patterns
        match = self.citation_patterns["irc_section"].search(citation)
        if not match:
            match = self.citation_patterns["irc_section_alt"].search(citation)

        if not match:
            return None

        groups = match.groups()
        result = {
            "section": groups[0] if groups[0] else None,
            "subsection": groups[1] if len(groups) > 1 and groups[1] else None,
            "paragraph": groups[2] if len(groups) > 2 and groups[2] else None,
            "subparagraph": groups[3] if len(groups) > 3 and groups[3] else None,
            "clause": groups[4] if len(groups) > 4 and groups[4] else None,
            "subclause": groups[5] if len(groups) > 5 and groups[5] else None,
        }

        # Build canonical citation
        canonical_parts = [f"§ {result['section']}"]
        if result['subsection']:
            canonical_parts.append(f"({result['subsection']})")
        if result['paragraph']:
            canonical_parts.append(f"({result['paragraph']})")
        if result['subparagraph']:
            canonical_parts.append(f"({result['subparagraph']})")
        if result['clause']:
            canonical_parts.append(f"({result['clause']})")
        if result['subclause']:
            canonical_parts.append(f"({result['subclause']})")

        result["canonical_citation"] = "".join(canonical_parts)
        result["hierarchical_level"] = self._determine_hierarchical_level(result)

        return result

    def _determine_hierarchical_level(self, parsed: Dict[str, str]) -> str:
        """Determine deepest hierarchical level of citation"""
        if parsed.get("subclause"):
            return "subclause"
        elif parsed.get("clause"):
            return "clause"
        elif parsed.get("subparagraph"):
            return "subparagraph"
        elif parsed.get("paragraph"):
            return "paragraph"
        elif parsed.get("subsection"):
            return "subsection"
        else:
            return "section"

    def parse_reg_citation(self, citation: str) -> Optional[Dict[str, str]]:
        """Parse Treasury Regulation citation"""
        match = self.citation_patterns["reg_citation"].search(citation)
        if not match:
            return None

        groups = match.groups()
        return {
            "title": groups[0],  # Usually "1" for income tax
            "section": groups[1],
            "regulation_number": groups[2],
            "subsection": groups[3] if len(groups) > 3 and groups[3] else None,
            "paragraph": groups[4] if len(groups) > 4 and groups[4] else None,
            "canonical_citation": f"Treas. Reg. § {groups[0]}.{groups[1]}-{groups[2]}"
        }

    def normalize_statutory_language(self, text: str) -> str:
        """Normalize statutory text while preserving legal meaning"""
        # Preserve exact statutory phrases
        normalized = text

        # Standardize section references
        normalized = re.sub(r'\bsec\.\s*', 'section ', normalized, flags=re.IGNORECASE)
        normalized = re.sub(r'\bsubsec\.\s*', 'subsection ', normalized, flags=re.IGNORECASE)

        # Standardize conjunctions in tests
        normalized = re.sub(r'\s+and\s+', ' and ', normalized)
        normalized = re.sub(r'\s+or\s+', ' or ', normalized)

        # Standardize parenthetical exceptions
        normalized = re.sub(r'\s*\(\s*other than\s+', ' (other than ', normalized, flags=re.IGNORECASE)
        normalized = re.sub(r'\s*\(\s*except\s+', ' (except ', normalized, flags=re.IGNORECASE)

        # Remove excessive whitespace but preserve paragraph structure
        normalized = re.sub(r' +', ' ', normalized)
        normalized = re.sub(r'\n\n+', '\n\n', normalized)

        return normalized.strip()

    def identify_cross_references(self, text: str) -> List[Dict[str, str]]:
        """Identify all cross-references in statutory text"""
        cross_refs = []

        # Pattern: "as defined in § X"
        for match in re.finditer(r'as defined in\s+(§\s*\d+[A-Z]?(?:\([a-z]\))?(?:\(\d+\))?)', text):
            parsed = self.parse_irc_citation(match.group(1))
            if parsed:
                cross_refs.append({
                    "type": "definition",
                    "reference": parsed["canonical_citation"],
                    "context": match.group(0)
                })

        # Pattern: "under § X"
        for match in re.finditer(r'under\s+(§\s*\d+[A-Z]?(?:\([a-z]\))?(?:\(\d+\))?)', text):
            parsed = self.parse_irc_citation(match.group(1))
            if parsed:
                cross_refs.append({
                    "type": "reference",
                    "reference": parsed["canonical_citation"],
                    "context": match.group(0)
                })

        # Pattern: "pursuant to § X"
        for match in re.finditer(r'pursuant to\s+(§\s*\d+[A-Z]?(?:\([a-z]\))?(?:\(\d+\))?)', text):
            parsed = self.parse_irc_citation(match.group(1))
            if parsed:
                cross_refs.append({
                    "type": "procedural",
                    "reference": parsed["canonical_citation"],
                    "context": match.group(0)
                })

        # Pattern: "except as provided in § X"
        for match in re.finditer(r'except as provided in\s+(§\s*\d+[A-Z]?(?:\([a-z]\))?(?:\(\d+\))?)', text):
            parsed = self.parse_irc_citation(match.group(1))
            if parsed:
                cross_refs.append({
                    "type": "exception",
                    "reference": parsed["canonical_citation"],
                    "context": match.group(0)
                })

        return cross_refs
