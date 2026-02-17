"""
TX10 State Nexus Engine - Semantic Normalization
Domain-specific term normalization and synonym mapping
"""

from typing import Dict, List, Set
import re


class SemanticNormalizer:
    """Normalize state tax nexus terminology for consistent doctrine matching"""

    def __init__(self):
        self.synonym_map = self._build_synonym_map()
        self.abbreviation_map = self._build_abbreviation_map()
        self.state_abbreviations = self._build_state_abbreviations()

    def _build_synonym_map(self) -> Dict[str, List[str]]:
        """Map equivalent terms in state tax nexus domain"""
        return {
            "substantial_nexus": [
                "substantial nexus", "nexus standard", "minimum connection",
                "sufficient connection", "jurisdictional nexus", "tax nexus"
            ],
            "economic_nexus": [
                "economic nexus", "wayfair nexus", "sales threshold nexus",
                "remote seller nexus", "marketplace nexus", "economic presence"
            ],
            "physical_presence": [
                "physical presence", "in-state presence", "brick and mortar",
                "physical location", "office presence", "employee presence",
                "property presence", "tangible presence"
            ],
            "pl_86_272": [
                "p.l. 86-272", "pl 86-272", "public law 86-272",
                "15 usc 381", "solicitation protection", "solicitation safe harbor"
            ],
            "apportionment": [
                "apportionment", "allocation", "division of income",
                "income attribution", "factor apportionment", "formula apportionment"
            ],
            "sales_factor": [
                "sales factor", "receipts factor", "revenue factor",
                "gross receipts factor", "sales apportionment"
            ],
            "property_factor": [
                "property factor", "asset factor", "capital factor",
                "real property factor", "tangible property factor"
            ],
            "payroll_factor": [
                "payroll factor", "compensation factor", "wage factor",
                "employee factor", "salary factor"
            ],
            "fair_apportionment": [
                "fair apportionment", "fairly apportioned", "constitutional apportionment",
                "internal consistency", "external consistency"
            ],
            "discrimination": [
                "discrimination", "discriminatory", "preferential treatment",
                "unequal treatment", "disparate treatment", "facial discrimination"
            ],
            "due_process": [
                "due process", "minimum contacts", "fair warning",
                "purposeful availment", "jurisdictional contacts"
            ],
            "commerce_clause": [
                "commerce clause", "dormant commerce clause", "negative commerce clause",
                "interstate commerce", "complete auto test"
            ],
            "unitary_business": [
                "unitary business", "unitary group", "integrated enterprise",
                "three unities", "contribution and dependency", "functional integration"
            ],
            "combined_reporting": [
                "combined reporting", "combined return", "consolidated return",
                "unitary combined reporting", "water's edge", "worldwide combined"
            ],
            "throwback_rule": [
                "throwback rule", "throwback", "sales throwback",
                "throwback provision", "destination throwback"
            ],
            "throwout_rule": [
                "throwout rule", "throwout", "sales throwout",
                "throwout provision", "nowhere income exclusion"
            ],
            "market_based_sourcing": [
                "market-based sourcing", "market sourcing", "market assignment",
                "customer location sourcing", "destination-based sourcing"
            ],
            "cost_of_performance": [
                "cost of performance", "income-producing activity",
                "performance sourcing", "service performance location"
            ],
            "factor_presence": [
                "factor presence nexus", "factor nexus", "bright-line nexus",
                "threshold nexus", "quantitative nexus"
            ],
            "affiliate_nexus": [
                "affiliate nexus", "attribution nexus", "agency nexus",
                "subsidiary nexus", "related party nexus", "interbrand nexus"
            ],
            "marketplace_facilitator": [
                "marketplace facilitator", "platform", "marketplace provider",
                "third-party marketplace", "online marketplace", "facilitator"
            ],
            "click_through_nexus": [
                "click-through nexus", "affiliate referral nexus",
                "commission nexus", "referral nexus"
            ],
            "franchise_tax": [
                "franchise tax", "privilege tax", "capital tax",
                "net worth tax", "doing business tax"
            ],
            "margin_tax": [
                "margin tax", "texas margin tax", "taxable margin",
                "gross receipts margin", "franchise tax margin"
            ],
            "salt_cap": [
                "salt cap", "salt deduction cap", "10000 limit",
                "164(b)(6)", "state and local tax deduction limit"
            ],
            "ptet": [
                "ptet", "pass-through entity tax", "entity-level tax",
                "elective entity tax", "tet", "pet"
            ],
            "solicitation": [
                "solicitation", "solicitation of orders", "order solicitation",
                "sales solicitation", "mere solicitation"
            ],
            "tangible_personal_property": [
                "tangible personal property", "tpp", "tangible goods",
                "physical goods", "inventory", "merchandise"
            ],
            "services": [
                "services", "professional services", "consulting services",
                "service income", "service revenue"
            ],
            "intangibles": [
                "intangibles", "intangible property", "intellectual property",
                "ip", "licenses", "royalties", "patents", "trademarks"
            ],
            "uditpa": [
                "uditpa", "uniform division of income",
                "uniform division of income for tax purposes act"
            ],
            "mtc": [
                "mtc", "multistate tax commission", "multistate tax compact"
            ],
            "sst": [
                "sst", "streamlined sales tax", "streamlined sales and use tax",
                "streamlined sales tax agreement", "sstgb"
            ]
        }

    def _build_abbreviation_map(self) -> Dict[str, str]:
        """Map abbreviations to full terms"""
        return {
            "tpp": "tangible personal property",
            "pl": "public law",
            "usc": "united states code",
            "irc": "internal revenue code",
            "cogs": "cost of goods sold",
            "cop": "cost of performance",
            "mbs": "market-based sourcing",
            "agi": "adjusted gross income",
            "appt": "apportionment",
            "bo": "business and occupation",
            "cat": "commercial activity tax",
            "fba": "fulfillment by amazon",
            "saas": "software as a service",
            "ip": "intellectual property",
            "llc": "limited liability company",
            "lp": "limited partnership",
            "gp": "general partnership"
        }

    def _build_state_abbreviations(self) -> Dict[str, str]:
        """Map state abbreviations to full names"""
        return {
            "al": "alabama", "ak": "alaska", "az": "arizona", "ar": "arkansas",
            "ca": "california", "co": "colorado", "ct": "connecticut", "de": "delaware",
            "fl": "florida", "ga": "georgia", "hi": "hawaii", "id": "idaho",
            "il": "illinois", "in": "indiana", "ia": "iowa", "ks": "kansas",
            "ky": "kentucky", "la": "louisiana", "me": "maine", "md": "maryland",
            "ma": "massachusetts", "mi": "michigan", "mn": "minnesota", "ms": "mississippi",
            "mo": "missouri", "mt": "montana", "ne": "nebraska", "nv": "nevada",
            "nh": "new hampshire", "nj": "new jersey", "nm": "new mexico", "ny": "new york",
            "nc": "north carolina", "nd": "north dakota", "oh": "ohio", "ok": "oklahoma",
            "or": "oregon", "pa": "pennsylvania", "ri": "rhode island", "sc": "south carolina",
            "sd": "south dakota", "tn": "tennessee", "tx": "texas", "ut": "utah",
            "vt": "vermont", "va": "virginia", "wa": "washington", "wv": "west virginia",
            "wi": "wisconsin", "wy": "wyoming"
        }

    def normalize(self, text: str) -> str:
        """Normalize text for semantic matching"""
        if not text:
            return ""

        # Lowercase
        text = text.lower()

        # Remove punctuation (except hyphens in specific contexts)
        text = re.sub(r'[^\w\s\-]', ' ', text)

        # Expand abbreviations
        for abbrev, full in self.abbreviation_map.items():
            text = re.sub(rf'\b{abbrev}\b', full, text)

        # Expand state abbreviations
        for abbrev, full in self.state_abbreviations.items():
            text = re.sub(rf'\b{abbrev}\b', full, text)

        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def extract_keywords(self, text: str) -> Set[str]:
        """Extract domain-specific keywords from text"""
        normalized = self.normalize(text)
        keywords = set()

        # Check for each canonical term
        for canonical, synonyms in self.synonym_map.items():
            for synonym in synonyms:
                if synonym in normalized:
                    keywords.add(canonical)
                    break

        return keywords

    def get_canonical_term(self, term: str) -> str:
        """Get canonical form of a term"""
        normalized = self.normalize(term)

        for canonical, synonyms in self.synonym_map.items():
            for synonym in synonyms:
                if synonym in normalized or normalized in synonym:
                    return canonical

        return normalized

    def expand_query(self, query: str) -> List[str]:
        """Expand query with synonyms for broader matching"""
        normalized = self.normalize(query)
        expanded = [normalized]

        # Add all synonyms for any matched canonical term
        for canonical, synonyms in self.synonym_map.items():
            for synonym in synonyms:
                if synonym in normalized or normalized in synonym:
                    expanded.extend(synonyms)
                    break

        return list(set(expanded))

    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity based on shared canonical terms"""
        keywords1 = self.extract_keywords(text1)
        keywords2 = self.extract_keywords(text2)

        if not keywords1 or not keywords2:
            return 0.0

        intersection = keywords1 & keywords2
        union = keywords1 | keywords2

        return len(intersection) / len(union) if union else 0.0

    def identify_state_references(self, text: str) -> List[str]:
        """Extract state references from text"""
        normalized = self.normalize(text)
        states = []

        # Check for full state names
        for abbrev, full_name in self.state_abbreviations.items():
            if full_name in normalized:
                states.append(full_name)

        # Check for specific state mentions in case formats
        state_pattern = r'\b(' + '|'.join(self.state_abbreviations.values()) + r')\b'
        matches = re.findall(state_pattern, normalized)
        states.extend(matches)

        return list(set(states))

    def identify_case_citations(self, text: str) -> List[str]:
        """Extract case citations from text"""
        # Pattern: Name v. Name, Volume Reporter Page (Court Year)
        citation_pattern = r'[\w\s]+\s+v\.?\s+[\w\s]+,?\s+\d+\s+[A-Z][\.A-Za-z0-9]+\s+\d+'
        citations = re.findall(citation_pattern, text)
        return citations

    def identify_statutory_references(self, text: str) -> List[str]:
        """Extract statutory references from text"""
        references = []

        # IRC sections
        irc_pattern = r'(?:IRC|I\.R\.C\.)\s*§?\s*\d+[\(\)a-z0-9]*'
        references.extend(re.findall(irc_pattern, text, re.IGNORECASE))

        # USC sections
        usc_pattern = r'\d+\s+U\.?S\.?C\.?\s*§?\s*\d+[\(\)a-z0-9]*'
        references.extend(re.findall(usc_pattern, text, re.IGNORECASE))

        # State code sections
        state_code_pattern = r'(?:Cal\.|Tex\.|N\.Y\.|Ill\.|Fla\.)\s+(?:Rev\.\s*&\s*Tax\.|Tax)\s+Code\s*§?\s*\d+'
        references.extend(re.findall(state_code_pattern, text, re.IGNORECASE))

        # P.L. references
        pl_pattern = r'P\.?L\.?\s*\d+-\d+'
        references.extend(re.findall(pl_pattern, text, re.IGNORECASE))

        return references
