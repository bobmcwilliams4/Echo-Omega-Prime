"""
LG06 IP Analysis Engine - Search Module
==========================================
TF-IDF based vector search over IP doctrine blocks,
patent claims, trademark records, and prior art references.

Components:
    - DoctrineSearchIndex: TF-IDF inverted index for doctrine search
    - SearchResult: Ranked search result with scoring breakdown
    - PatentClaimParser: Structured claim parsing and mapping
    - PriorArtSearchEngine: Prior art search with relevance scoring
    - InfringementMapper: Claim-to-product element mapping
    - TrademarkSearchEngine: Trademark clearance search simulation
    - IPCitationParser: Patent/trademark/copyright citation extraction
    - FTOAnalyzer: Freedom-to-operate claim matrix

Version: 2.0.0
Engine: LG06 IP Analysis
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Optional, Set, Tuple

from loguru import logger


# ============================================================================
# SEARCH RESULT
# ============================================================================

@dataclass
class SearchResult:
    """A single search result with scoring breakdown."""
    doc_id: str
    topic: str
    content: str
    score: float
    tf_idf_score: float
    authority_score: float
    recency_score: float
    ip_category: str
    matched_tokens: List[str]
    source: str = "doctrine_cache"
    metadata: Dict[str, Any] = dc_field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "doc_id": self.doc_id,
            "topic": self.topic,
            "content": self.content[:500],
            "score": round(self.score, 6),
            "tf_idf_score": round(self.tf_idf_score, 6),
            "authority_score": round(self.authority_score, 6),
            "recency_score": round(self.recency_score, 6),
            "ip_category": self.ip_category,
            "matched_tokens": self.matched_tokens,
            "source": self.source,
            "metadata": self.metadata,
        }


# ============================================================================
# PARSED CLAIM
# ============================================================================

@dataclass
class ParsedClaim:
    """A parsed patent claim with structured elements."""
    claim_number: int
    claim_type: str  # independent, dependent
    preamble: str
    body: str
    elements: List[str]
    depends_on: Optional[int] = None
    means_plus_function: bool = False
    method_claim: bool = False
    apparatus_claim: bool = False
    system_claim: bool = False
    composition_claim: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "claim_number": self.claim_number,
            "claim_type": self.claim_type,
            "preamble": self.preamble,
            "body": self.body,
            "elements": self.elements,
            "depends_on": self.depends_on,
            "means_plus_function": self.means_plus_function,
            "method_claim": self.method_claim,
            "apparatus_claim": self.apparatus_claim,
            "system_claim": self.system_claim,
            "composition_claim": self.composition_claim,
        }


# ============================================================================
# PRIOR ART RESULT
# ============================================================================

@dataclass
class PriorArtResult:
    """A prior art search result."""
    reference_id: str
    title: str
    reference_type: str  # patent, publication, product, standard
    date: str
    relevance_score: float
    matching_claims: List[int]
    key_disclosures: List[str]
    anticipation_risk: float
    obviousness_risk: float
    source: str
    metadata: Dict[str, Any] = dc_field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "reference_id": self.reference_id,
            "title": self.title,
            "reference_type": self.reference_type,
            "date": self.date,
            "relevance_score": round(self.relevance_score, 4),
            "matching_claims": self.matching_claims,
            "key_disclosures": self.key_disclosures,
            "anticipation_risk": round(self.anticipation_risk, 4),
            "obviousness_risk": round(self.obviousness_risk, 4),
            "source": self.source,
            "metadata": self.metadata,
        }


# ============================================================================
# FTO ELEMENT MAPPING
# ============================================================================

@dataclass
class FTOElementMapping:
    """Mapping of a claim element to a product feature for FTO analysis."""
    claim_number: int
    element_index: int
    element_text: str
    product_feature: str
    mapping_strength: float  # 0.0 to 1.0
    analysis_notes: str
    risk_level: str  # low, medium, high, critical

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "claim_number": self.claim_number,
            "element_index": self.element_index,
            "element_text": self.element_text,
            "product_feature": self.product_feature,
            "mapping_strength": round(self.mapping_strength, 4),
            "analysis_notes": self.analysis_notes,
            "risk_level": self.risk_level,
        }


# ============================================================================
# INFRINGEMENT ANALYSIS RESULT
# ============================================================================

@dataclass
class InfringementAnalysisResult:
    """Result of an infringement analysis."""
    patent_id: str
    claim_number: int
    infringement_type: str
    literal_match: bool
    equivalents_match: bool
    all_elements_met: bool
    element_mappings: List[FTOElementMapping]
    overall_risk: float
    risk_level: str
    defenses_available: List[str]
    notes: str

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "patent_id": self.patent_id,
            "claim_number": self.claim_number,
            "infringement_type": self.infringement_type,
            "literal_match": self.literal_match,
            "equivalents_match": self.equivalents_match,
            "all_elements_met": self.all_elements_met,
            "element_mappings": [m.to_dict() for m in self.element_mappings],
            "overall_risk": round(self.overall_risk, 4),
            "risk_level": self.risk_level,
            "defenses_available": self.defenses_available,
            "notes": self.notes,
        }


# ============================================================================
# DOCTRINE SEARCH INDEX (TF-IDF)
# ============================================================================

class DoctrineSearchIndex:
    """TF-IDF inverted index for searching over IP doctrine blocks.

    Supports boosted search with authority weighting, IP category
    filtering, and recency scoring.
    """

    def __init__(self, min_token_length: int = 2, max_token_length: int = 50) -> None:
        self._documents: Dict[str, Dict[str, Any]] = {}
        self._inverted_index: Dict[str, Set[str]] = defaultdict(set)
        self._term_freq: Dict[str, Counter] = {}
        self._doc_freq: Counter = Counter()
        self._doc_count: int = 0
        self._min_token_length: int = min_token_length
        self._max_token_length: int = max_token_length
        self._idf_cache: Dict[str, float] = {}
        self._dirty: bool = False
        logger.info("DoctrineSearchIndex initialized")

    def add_document(
        self,
        doc_id: str,
        topic: str,
        content: str,
        ip_category: str = "general",
        authority_score: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a document to the search index."""
        tokens = self._tokenize(content)
        tf = Counter(tokens)
        unique_tokens = set(tokens)

        self._documents[doc_id] = {
            "topic": topic,
            "content": content,
            "ip_category": ip_category,
            "authority_score": authority_score,
            "tokens": tokens,
            "unique_tokens": unique_tokens,
            "metadata": metadata or {},
            "indexed_at": datetime.now(timezone.utc).isoformat(),
        }
        self._term_freq[doc_id] = tf
        for token in unique_tokens:
            self._inverted_index[token].add(doc_id)
            self._doc_freq[token] += 1
        self._doc_count += 1
        self._dirty = True

    def search(
        self,
        query_tokens: List[str],
        top_k: int = 5,
        score_threshold: float = 0.1,
        ip_category_filter: Optional[str] = None,
        authority_weight: float = 0.3,
        recency_weight: float = 0.1,
    ) -> List[SearchResult]:
        """Search the index with TF-IDF scoring."""
        if self._dirty:
            self._rebuild_idf_cache()

        candidate_docs: Set[str] = set()
        for token in query_tokens:
            normalized = token.lower()
            if normalized in self._inverted_index:
                candidate_docs.update(self._inverted_index[normalized])

        if not candidate_docs:
            return []

        results: List[SearchResult] = []
        for doc_id in candidate_docs:
            doc = self._documents[doc_id]

            if ip_category_filter and doc["ip_category"] != ip_category_filter:
                continue

            tf_idf = self._compute_tf_idf(doc_id, query_tokens)
            auth_score = doc["authority_score"]
            recency = self._compute_recency_score(doc.get("indexed_at", ""))

            combined = (
                tf_idf * (1.0 - authority_weight - recency_weight) +
                auth_score * authority_weight +
                recency * recency_weight
            )

            if combined < score_threshold:
                continue

            matched = [t for t in query_tokens if t.lower() in doc["unique_tokens"]]

            results.append(SearchResult(
                doc_id=doc_id,
                topic=doc["topic"],
                content=doc["content"],
                score=combined,
                tf_idf_score=tf_idf,
                authority_score=auth_score,
                recency_score=recency,
                ip_category=doc["ip_category"],
                matched_tokens=matched,
                source="doctrine_cache",
                metadata=doc.get("metadata", {}),
            ))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text for indexing."""
        tokens = re.findall(r"[\w]+(?:[-_][\w]+)*", text.lower())
        return [
            t for t in tokens
            if self._min_token_length <= len(t) <= self._max_token_length
        ]

    def _compute_tf_idf(self, doc_id: str, query_tokens: List[str]) -> float:
        """Compute TF-IDF score for a document against query tokens."""
        if doc_id not in self._term_freq:
            return 0.0
        tf = self._term_freq[doc_id]
        doc_length = sum(tf.values())
        if doc_length == 0:
            return 0.0

        score = 0.0
        for token in query_tokens:
            normalized = token.lower()
            term_count = tf.get(normalized, 0)
            if term_count == 0:
                continue
            tf_val = term_count / doc_length
            idf_val = self._idf_cache.get(normalized, 0.0)
            score += tf_val * idf_val
        return score

    def _rebuild_idf_cache(self) -> None:
        """Rebuild the IDF cache."""
        self._idf_cache.clear()
        for term, df in self._doc_freq.items():
            self._idf_cache[term] = math.log((self._doc_count + 1) / (df + 1)) + 1.0
        self._dirty = False

    def _compute_recency_score(self, indexed_at: str) -> float:
        """Compute recency score based on indexing time."""
        if not indexed_at:
            return 0.5
        try:
            dt = datetime.fromisoformat(indexed_at.replace("Z", "+00:00"))
            age_days = (datetime.now(timezone.utc) - dt).total_seconds() / 86400.0
            return max(0.0, 1.0 - (age_days / 365.0))
        except (ValueError, TypeError):
            return 0.5

    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics."""
        return {
            "document_count": self._doc_count,
            "unique_terms": len(self._inverted_index),
            "avg_doc_length": (
                sum(len(d["tokens"]) for d in self._documents.values()) / max(self._doc_count, 1)
            ),
            "categories": list(set(d["ip_category"] for d in self._documents.values())),
        }


# ============================================================================
# PATENT CLAIM PARSER
# ============================================================================

class PatentClaimParser:
    """Parses structured patent claims into elements."""

    _CLAIM_PATTERN: ClassVar[re.Pattern] = re.compile(
        r"(?:(\d+)\.\s*)(.*?)(?=\d+\.\s|\Z)", re.DOTALL
    )
    _DEPENDENCY_PATTERN: ClassVar[re.Pattern] = re.compile(
        r"(?:The\s+\w+\s+of\s+claim|according\s+to\s+claim)\s+(\d+)", re.IGNORECASE
    )
    _MEANS_PATTERN: ClassVar[re.Pattern] = re.compile(
        r"means\s+for\s+\w+", re.IGNORECASE
    )
    _METHOD_INDICATORS: ClassVar[List[str]] = [
        "method", "process", "step of", "comprising the steps",
        "a step of", "the step of",
    ]
    _APPARATUS_INDICATORS: ClassVar[List[str]] = [
        "apparatus", "device", "system comprising", "machine",
    ]
    _COMPOSITION_INDICATORS: ClassVar[List[str]] = [
        "composition", "compound", "formulation", "mixture",
    ]

    def parse_claims(self, claim_text: str) -> List[ParsedClaim]:
        """Parse a full claim set into structured claims."""
        claims: List[ParsedClaim] = []
        matches = self._CLAIM_PATTERN.findall(claim_text)

        for num_str, body in matches:
            try:
                claim_num = int(num_str)
            except ValueError:
                continue

            body = body.strip()
            depends_on = self._detect_dependency(body)
            claim_type = "dependent" if depends_on else "independent"
            preamble, claim_body = self._split_preamble(body)
            elements = self._extract_elements(claim_body)
            is_means = bool(self._MEANS_PATTERN.search(body))
            is_method = any(ind in body.lower() for ind in self._METHOD_INDICATORS)
            is_apparatus = any(ind in body.lower() for ind in self._APPARATUS_INDICATORS)
            is_composition = any(ind in body.lower() for ind in self._COMPOSITION_INDICATORS)

            claims.append(ParsedClaim(
                claim_number=claim_num,
                claim_type=claim_type,
                preamble=preamble,
                body=claim_body,
                elements=elements,
                depends_on=depends_on,
                means_plus_function=is_means,
                method_claim=is_method,
                apparatus_claim=is_apparatus,
                system_claim="system" in body.lower(),
                composition_claim=is_composition,
            ))

        return claims

    def _detect_dependency(self, body: str) -> Optional[int]:
        """Detect if claim depends on another claim."""
        match = self._DEPENDENCY_PATTERN.search(body)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                return None
        return None

    def _split_preamble(self, body: str) -> Tuple[str, str]:
        """Split claim into preamble and body at 'comprising' or 'consisting'."""
        split_words = ["comprising:", "consisting of:", "consisting essentially of:",
                       "comprising", "consisting of", "wherein", "including:"]
        body_lower = body.lower()
        best_pos = len(body)
        best_word = ""
        for word in split_words:
            pos = body_lower.find(word)
            if 0 < pos < best_pos:
                best_pos = pos
                best_word = word
        if best_word:
            return body[:best_pos].strip(), body[best_pos:].strip()
        return "", body

    def _extract_elements(self, body: str) -> List[str]:
        """Extract claim elements (limitations) from the body."""
        elements: List[str] = []
        parts = re.split(r";\s*(?=[a-z])", body)
        if len(parts) <= 1:
            parts = re.split(r",\s*(?=(?:a|an|the|said|wherein|and|at least)\s)", body)
        for part in parts:
            cleaned = part.strip().rstrip(";,.")
            if len(cleaned) > 10:
                elements.append(cleaned)
        if not elements and len(body) > 10:
            elements.append(body.strip())
        return elements

    def get_independent_claims(self, claims: List[ParsedClaim]) -> List[ParsedClaim]:
        """Filter to only independent claims."""
        return [c for c in claims if c.claim_type == "independent"]

    def get_claim_tree(self, claims: List[ParsedClaim]) -> Dict[int, List[int]]:
        """Build a dependency tree of claims."""
        tree: Dict[int, List[int]] = defaultdict(list)
        for claim in claims:
            if claim.depends_on is not None:
                tree[claim.depends_on].append(claim.claim_number)
        return dict(tree)


# ============================================================================
# PRIOR ART SEARCH ENGINE
# ============================================================================

class PriorArtSearchEngine:
    """Simulates prior art search with structured result scoring."""

    # Pre-loaded prior art database (representative references)
    PRIOR_ART_DB: ClassVar[List[Dict[str, Any]]] = [
        {
            "id": "PA_001",
            "title": "Method for Data Processing Using Neural Networks",
            "type": "patent",
            "date": "2018-03-15",
            "keywords": ["neural network", "data processing", "machine learning",
                         "deep learning", "inference", "training"],
            "abstract": "A method for processing data using multi-layer neural networks with optimized backpropagation and adaptive learning rates for real-time inference.",
        },
        {
            "id": "PA_002",
            "title": "System for Secure Blockchain Transactions",
            "type": "patent",
            "date": "2019-07-22",
            "keywords": ["blockchain", "cryptocurrency", "smart contract",
                         "distributed ledger", "consensus", "hash"],
            "abstract": "A system for executing secure transactions on a blockchain network using zero-knowledge proofs and sharded consensus mechanisms.",
        },
        {
            "id": "PA_003",
            "title": "Apparatus for Wireless Power Transfer",
            "type": "patent",
            "date": "2020-01-10",
            "keywords": ["wireless power", "inductive charging", "resonant coupling",
                         "power transfer", "coil", "electromagnetic"],
            "abstract": "An apparatus for wirelessly transferring power using resonant inductive coupling with automatic impedance matching and foreign object detection.",
        },
        {
            "id": "PA_004",
            "title": "Pharmaceutical Composition for Cancer Treatment",
            "type": "patent",
            "date": "2017-11-30",
            "keywords": ["pharmaceutical", "cancer", "antibody", "immunotherapy",
                         "checkpoint inhibitor", "oncology", "pd-1"],
            "abstract": "A pharmaceutical composition comprising a novel PD-1 checkpoint inhibitor antibody conjugated with a cytotoxic payload for targeted cancer therapy.",
        },
        {
            "id": "PA_005",
            "title": "Survey of Natural Language Processing Techniques",
            "type": "publication",
            "date": "2021-06-15",
            "keywords": ["nlp", "natural language processing", "transformer",
                         "bert", "gpt", "attention mechanism", "language model"],
            "abstract": "A comprehensive survey of state-of-the-art natural language processing techniques including transformer architectures, pre-training strategies, and fine-tuning approaches.",
        },
        {
            "id": "PA_006",
            "title": "IoT Device Authentication Framework",
            "type": "patent",
            "date": "2021-03-08",
            "keywords": ["iot", "internet of things", "authentication",
                         "device identity", "certificate", "tls", "mutual auth"],
            "abstract": "A framework for authenticating IoT devices in a mesh network using certificate-based mutual TLS with hardware-bound device identities.",
        },
        {
            "id": "PA_007",
            "title": "Autonomous Vehicle Navigation System",
            "type": "patent",
            "date": "2022-09-01",
            "keywords": ["autonomous", "vehicle", "self-driving", "lidar",
                         "sensor fusion", "path planning", "obstacle detection"],
            "abstract": "A navigation system for autonomous vehicles using multi-sensor fusion of LiDAR, camera, and radar data with real-time path planning and obstacle avoidance.",
        },
        {
            "id": "PA_008",
            "title": "CRISPR Gene Editing Method",
            "type": "patent",
            "date": "2019-12-20",
            "keywords": ["crispr", "gene editing", "cas9", "guide rna",
                         "genome", "biotechnology", "genetic modification"],
            "abstract": "A method for precise gene editing using an optimized CRISPR-Cas9 system with enhanced guide RNA design for improved on-target efficiency and reduced off-target effects.",
        },
        {
            "id": "PA_009",
            "title": "5G Beamforming Antenna Array",
            "type": "patent",
            "date": "2020-05-15",
            "keywords": ["5g", "beamforming", "antenna", "massive mimo",
                         "millimeter wave", "phased array"],
            "abstract": "A beamforming antenna array for 5G millimeter wave communications using massive MIMO with digital precoding and analog phase shifting.",
        },
        {
            "id": "PA_010",
            "title": "Cloud Computing Resource Allocation Method",
            "type": "patent",
            "date": "2021-08-12",
            "keywords": ["cloud", "resource allocation", "containerization",
                         "kubernetes", "serverless", "microservice", "scaling"],
            "abstract": "A method for dynamically allocating cloud computing resources using predictive scaling algorithms with container orchestration and serverless function management.",
        },
    ]

    def search(self, query_tokens: List[str], top_k: int = 5) -> List[PriorArtResult]:
        """Search the prior art database."""
        results: List[PriorArtResult] = []
        query_set = set(t.lower() for t in query_tokens)

        for ref in self.PRIOR_ART_DB:
            ref_keywords = set(k.lower() for k in ref["keywords"])
            overlap = query_set.intersection(ref_keywords)
            if not overlap:
                # Check abstract for partial matches
                abstract_lower = ref["abstract"].lower()
                for token in query_set:
                    if token in abstract_lower:
                        overlap.add(token)

            if not overlap:
                continue

            relevance = len(overlap) / max(len(query_set), 1)
            anticipation = relevance * 0.7 if relevance > 0.5 else relevance * 0.3
            obviousness = relevance * 0.8 if relevance > 0.3 else relevance * 0.4

            results.append(PriorArtResult(
                reference_id=ref["id"],
                title=ref["title"],
                reference_type=ref["type"],
                date=ref["date"],
                relevance_score=relevance,
                matching_claims=[],
                key_disclosures=list(overlap),
                anticipation_risk=anticipation,
                obviousness_risk=obviousness,
                source="internal_db",
                metadata={"abstract": ref["abstract"][:300]},
            ))

        results.sort(key=lambda r: r.relevance_score, reverse=True)
        return results[:top_k]


# ============================================================================
# INFRINGEMENT MAPPER
# ============================================================================

class InfringementMapper:
    """Maps claim elements to product features for infringement analysis."""

    DEFENSE_CATALOG: ClassVar[Dict[str, str]] = {
        "invalidity": "Challenge patent validity based on prior art, 101 eligibility, or 112 deficiencies",
        "non_infringement": "Argue product does not meet all claim limitations",
        "prosecution_history_estoppel": "Use narrowing amendments during prosecution to limit scope",
        "patent_exhaustion": "First sale doctrine - authorized sale exhausts patent rights",
        "experimental_use": "Research/experimental use exception (very narrow in US)",
        "laches": "Unreasonable delay in bringing suit (6+ years typical)",
        "equitable_estoppel": "Patentee's conduct led to reasonable reliance",
        "repair_vs_reconstruction": "Permissible repair of patented article",
        "reverse_doc_equivalents": "Product so far changed in principle it cannot infringe",
        "license_defense": "Authorized license covers the accused activity",
        "prior_user_rights": "Prior commercial use before effective filing date (AIA 35 USC 273)",
    }

    def analyze_infringement(
        self,
        patent_id: str,
        claims: List[ParsedClaim],
        product_features: List[str],
        claim_numbers: Optional[List[int]] = None,
    ) -> List[InfringementAnalysisResult]:
        """Analyze potential infringement of claims by product features."""
        results: List[InfringementAnalysisResult] = []
        target_claims = claims
        if claim_numbers:
            target_claims = [c for c in claims if c.claim_number in claim_numbers]

        for claim in target_claims:
            mappings = self._map_elements(claim, product_features)
            elements_met = sum(1 for m in mappings if m.mapping_strength > 0.5)
            total_elements = len(claim.elements)
            all_met = elements_met == total_elements and total_elements > 0

            literal = all_met and all(m.mapping_strength > 0.8 for m in mappings)
            equivalents = all_met and not literal

            if total_elements > 0:
                risk = elements_met / total_elements
            else:
                risk = 0.0

            if literal:
                risk = min(risk * 1.2, 1.0)

            risk_level = self._classify_risk(risk)
            defenses = self._identify_defenses(risk, literal, equivalents, claim)

            results.append(InfringementAnalysisResult(
                patent_id=patent_id,
                claim_number=claim.claim_number,
                infringement_type="literal" if literal else ("equivalents" if equivalents else "none"),
                literal_match=literal,
                equivalents_match=equivalents,
                all_elements_met=all_met,
                element_mappings=mappings,
                overall_risk=risk,
                risk_level=risk_level,
                defenses_available=defenses,
                notes=self._generate_notes(claim, mappings, risk_level),
            ))

        return results

    def _map_elements(self, claim: ParsedClaim, product_features: List[str]) -> List[FTOElementMapping]:
        """Map claim elements to product features using keyword overlap."""
        mappings: List[FTOElementMapping] = []
        for idx, element in enumerate(claim.elements):
            best_feature = ""
            best_strength = 0.0
            element_tokens = set(re.findall(r"\w+", element.lower()))

            for feature in product_features:
                feature_tokens = set(re.findall(r"\w+", feature.lower()))
                if not element_tokens or not feature_tokens:
                    continue
                overlap = len(element_tokens.intersection(feature_tokens))
                strength = overlap / max(len(element_tokens), 1)
                if strength > best_strength:
                    best_strength = strength
                    best_feature = feature

            risk_level = self._classify_risk(best_strength)
            notes = f"Element maps to '{best_feature}' with {best_strength:.0%} overlap" if best_feature else "No matching product feature found"

            mappings.append(FTOElementMapping(
                claim_number=claim.claim_number,
                element_index=idx,
                element_text=element[:200],
                product_feature=best_feature,
                mapping_strength=best_strength,
                analysis_notes=notes,
                risk_level=risk_level,
            ))

        return mappings

    def _classify_risk(self, score: float) -> str:
        """Classify risk level from score."""
        if score >= 0.85:
            return "critical"
        if score >= 0.65:
            return "high"
        if score >= 0.4:
            return "medium"
        return "low"

    def _identify_defenses(
        self,
        risk: float,
        literal: bool,
        equivalents: bool,
        claim: ParsedClaim,
    ) -> List[str]:
        """Identify available defenses based on infringement type and risk."""
        defenses: List[str] = []
        defenses.append("invalidity")
        if not literal:
            defenses.append("non_infringement")
        if equivalents:
            defenses.append("prosecution_history_estoppel")
            defenses.append("reverse_doc_equivalents")
        if claim.means_plus_function:
            defenses.append("non_infringement")
        defenses.append("prior_user_rights")
        if risk < 0.5:
            defenses.append("experimental_use")
        return defenses

    def _generate_notes(
        self,
        claim: ParsedClaim,
        mappings: List[FTOElementMapping],
        risk_level: str,
    ) -> str:
        """Generate analysis notes for infringement result."""
        total = len(mappings)
        high_risk = sum(1 for m in mappings if m.risk_level in ("high", "critical"))
        low_risk = sum(1 for m in mappings if m.risk_level == "low")

        parts = [
            f"Claim {claim.claim_number} ({claim.claim_type}) has {total} elements.",
            f"{high_risk} elements show high/critical mapping strength.",
            f"{low_risk} elements show low mapping strength.",
        ]
        if claim.means_plus_function:
            parts.append("Contains means-plus-function limitations (112(f)) - narrow construction applies.")
        if claim.method_claim:
            parts.append("Method claim - must show each step is performed.")
        parts.append(f"Overall risk assessment: {risk_level}.")
        return " ".join(parts)


# ============================================================================
# TRADEMARK SEARCH ENGINE
# ============================================================================

class TrademarkSearchEngine:
    """Simulates trademark clearance search with confusion analysis."""

    EXISTING_MARKS_DB: ClassVar[List[Dict[str, Any]]] = [
        {"mark": "APPLE", "classes": [9, 42], "status": "live", "owner": "Apple Inc.", "distinctiveness": "arbitrary"},
        {"mark": "GOOGLE", "classes": [9, 35, 42], "status": "live", "owner": "Google LLC", "distinctiveness": "fanciful"},
        {"mark": "AMAZON", "classes": [9, 35, 39], "status": "live", "owner": "Amazon.com", "distinctiveness": "arbitrary"},
        {"mark": "MICROSOFT", "classes": [9, 42], "status": "live", "owner": "Microsoft Corp.", "distinctiveness": "suggestive"},
        {"mark": "TESLA", "classes": [9, 12], "status": "live", "owner": "Tesla Inc.", "distinctiveness": "arbitrary"},
        {"mark": "NIKE", "classes": [25, 28], "status": "live", "owner": "Nike Inc.", "distinctiveness": "arbitrary"},
        {"mark": "COCA-COLA", "classes": [32, 30], "status": "live", "owner": "Coca-Cola Co.", "distinctiveness": "fanciful"},
        {"mark": "INTEL", "classes": [9], "status": "live", "owner": "Intel Corp.", "distinctiveness": "suggestive"},
        {"mark": "ORACLE", "classes": [9, 42], "status": "live", "owner": "Oracle Corp.", "distinctiveness": "arbitrary"},
        {"mark": "SAMSUNG", "classes": [9, 11, 7], "status": "live", "owner": "Samsung Electronics", "distinctiveness": "arbitrary"},
    ]

    def search(self, proposed_mark: str, nice_classes: Optional[List[int]] = None) -> List[Dict[str, Any]]:
        """Search for potentially conflicting marks."""
        results: List[Dict[str, Any]] = []
        proposed_lower = proposed_mark.lower()

        for entry in self.EXISTING_MARKS_DB:
            mark_lower = entry["mark"].lower()
            similarity = self._compute_similarity(proposed_lower, mark_lower)
            class_overlap = False
            if nice_classes:
                class_overlap = bool(set(nice_classes).intersection(set(entry["classes"])))

            if similarity > 0.3 or (similarity > 0.15 and class_overlap):
                confusion_factors = self._assess_confusion(
                    proposed_mark, entry["mark"], similarity, class_overlap, entry
                )
                results.append({
                    "conflicting_mark": entry["mark"],
                    "owner": entry["owner"],
                    "classes": entry["classes"],
                    "status": entry["status"],
                    "distinctiveness": entry["distinctiveness"],
                    "similarity_score": round(similarity, 4),
                    "class_overlap": class_overlap,
                    "confusion_risk": confusion_factors["overall_risk"],
                    "confusion_factors": confusion_factors,
                })

        results.sort(key=lambda r: r["confusion_risk"], reverse=True)
        return results

    def _compute_similarity(self, a: str, b: str) -> float:
        """Compute string similarity using character n-gram overlap."""
        if a == b:
            return 1.0
        if not a or not b:
            return 0.0

        # Character bigrams
        bigrams_a = set(a[i:i+2] for i in range(len(a) - 1))
        bigrams_b = set(b[i:i+2] for i in range(len(b) - 1))
        if not bigrams_a or not bigrams_b:
            return 0.0

        overlap = len(bigrams_a.intersection(bigrams_b))
        total = len(bigrams_a.union(bigrams_b))
        jaccard = overlap / total if total > 0 else 0.0

        # Levenshtein-based score (simplified)
        max_len = max(len(a), len(b))
        common_prefix = 0
        for ca, cb in zip(a, b):
            if ca == cb:
                common_prefix += 1
            else:
                break
        prefix_score = common_prefix / max_len

        return (jaccard * 0.6) + (prefix_score * 0.4)

    def _assess_confusion(
        self,
        proposed: str,
        existing: str,
        similarity: float,
        class_overlap: bool,
        entry: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Assess likelihood of confusion using du Pont factors."""
        sight_score = similarity
        sound_score = self._phonetic_similarity(proposed.lower(), existing.lower())
        meaning_score = 0.1  # Default low for different words

        goods_overlap = 0.8 if class_overlap else 0.1
        strength = {"fanciful": 1.0, "arbitrary": 0.9, "suggestive": 0.7, "descriptive": 0.4, "generic": 0.0}
        mark_strength = strength.get(entry.get("distinctiveness", "suggestive"), 0.5)

        overall = (
            sight_score * 0.25 +
            sound_score * 0.2 +
            meaning_score * 0.1 +
            goods_overlap * 0.25 +
            mark_strength * 0.2
        )

        return {
            "sight_similarity": round(sight_score, 4),
            "sound_similarity": round(sound_score, 4),
            "meaning_similarity": round(meaning_score, 4),
            "goods_services_overlap": round(goods_overlap, 4),
            "senior_mark_strength": round(mark_strength, 4),
            "overall_risk": round(overall, 4),
            "risk_level": "high" if overall > 0.6 else ("medium" if overall > 0.35 else "low"),
        }

    def _phonetic_similarity(self, a: str, b: str) -> float:
        """Simple phonetic similarity based on consonant skeleton."""
        vowels = set("aeiou")
        skel_a = "".join(c for c in a if c not in vowels)
        skel_b = "".join(c for c in b if c not in vowels)
        if not skel_a or not skel_b:
            return 0.0
        max_len = max(len(skel_a), len(skel_b))
        matches = sum(1 for ca, cb in zip(skel_a, skel_b) if ca == cb)
        return matches / max_len


# ============================================================================
# MODULE-LEVEL SINGLETONS AND CONVENIENCE FUNCTIONS
# ============================================================================

_search_index: Optional[DoctrineSearchIndex] = None
_claim_parser: Optional[PatentClaimParser] = None
_prior_art_engine: Optional[PriorArtSearchEngine] = None
_infringement_mapper: Optional[InfringementMapper] = None
_trademark_engine: Optional[TrademarkSearchEngine] = None


def get_search_index() -> DoctrineSearchIndex:
    """Get or create the search index singleton."""
    global _search_index
    if _search_index is None:
        _search_index = DoctrineSearchIndex()
    return _search_index


def get_claim_parser() -> PatentClaimParser:
    """Get or create the claim parser singleton."""
    global _claim_parser
    if _claim_parser is None:
        _claim_parser = PatentClaimParser()
    return _claim_parser


def get_prior_art_engine() -> PriorArtSearchEngine:
    """Get or create the prior art search engine singleton."""
    global _prior_art_engine
    if _prior_art_engine is None:
        _prior_art_engine = PriorArtSearchEngine()
    return _prior_art_engine


def get_infringement_mapper() -> InfringementMapper:
    """Get or create the infringement mapper singleton."""
    global _infringement_mapper
    if _infringement_mapper is None:
        _infringement_mapper = InfringementMapper()
    return _infringement_mapper


def get_trademark_engine() -> TrademarkSearchEngine:
    """Get or create the trademark search engine singleton."""
    global _trademark_engine
    if _trademark_engine is None:
        _trademark_engine = TrademarkSearchEngine()
    return _trademark_engine


def compute_query_hash(query: str) -> str:
    """Compute a deterministic hash for a query string."""
    return hashlib.sha256(query.strip().lower().encode("utf-8")).hexdigest()
