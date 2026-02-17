"""
LG18 Legislative Analysis Engine - Search Module
===================================================
TF-IDF based vector search over legislative doctrine blocks,
statutory construction canons, regulatory rulemaking references,
and preemption analysis.

Components:
    - DoctrineSearchIndex: TF-IDF inverted index for doctrine search
    - SearchResult: Ranked search result with scoring breakdown
    - LegislativeHistorySearcher: Legislative history analysis
    - CanonOfConstructionMatcher: Canon applicability matching
    - RulemakingTracker: Rulemaking stage and compliance tracking
    - BillComparisonEngine: Compare bill versions and amendments

Version: 2.0.0
Engine: LG18 Legislative Analysis
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
    leg_category: str
    matched_tokens: List[str]
    source: str = "doctrine_cache"
    jurisdiction: Optional[str] = None
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
            "leg_category": self.leg_category,
            "jurisdiction": self.jurisdiction,
            "matched_tokens": self.matched_tokens,
            "source": self.source,
            "metadata": self.metadata,
        }


# ============================================================================
# LEGISLATIVE HISTORY ENTRY
# ============================================================================

@dataclass
class LegislativeHistoryEntry:
    """A single entry from legislative history analysis."""
    source_type: str
    chamber: str
    date: str
    speaker: str
    content_excerpt: str
    relevance_score: float
    reliability_weight: float
    citation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "source_type": self.source_type,
            "chamber": self.chamber,
            "date": self.date,
            "speaker": self.speaker,
            "content_excerpt": self.content_excerpt[:500],
            "relevance_score": round(self.relevance_score, 4),
            "reliability_weight": round(self.reliability_weight, 4),
            "citation": self.citation,
        }


# ============================================================================
# BILL COMPARISON RESULT
# ============================================================================

@dataclass
class BillComparisonResult:
    """Result of comparing two bill versions or amendments."""
    bill_a_id: str
    bill_b_id: str
    sections_added: List[str]
    sections_removed: List[str]
    sections_modified: List[str]
    key_differences: List[str]
    compatibility_score: float
    preemption_changes: List[str]
    funding_changes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "bill_a_id": self.bill_a_id,
            "bill_b_id": self.bill_b_id,
            "sections_added": self.sections_added,
            "sections_removed": self.sections_removed,
            "sections_modified": self.sections_modified,
            "key_differences": self.key_differences,
            "compatibility_score": round(self.compatibility_score, 4),
            "preemption_changes": self.preemption_changes,
            "funding_changes": self.funding_changes,
        }


# ============================================================================
# CANON MATCH RESULT
# ============================================================================

@dataclass
class CanonMatchResult:
    """Result of matching a statutory question to applicable canons."""
    canon_name: str
    relevance_score: float
    description: str
    application_steps: List[str]
    supporting_cases: List[str]
    counter_arguments: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "canon_name": self.canon_name,
            "relevance_score": round(self.relevance_score, 4),
            "description": self.description,
            "application_steps": self.application_steps,
            "supporting_cases": self.supporting_cases,
            "counter_arguments": self.counter_arguments,
        }


# ============================================================================
# TF-IDF DOCTRINE SEARCH INDEX
# ============================================================================

class DoctrineSearchIndex:
    """TF-IDF inverted index for searching legislative doctrine blocks."""

    def __init__(self, top_k: int = 5, score_threshold: float = 0.3) -> None:
        self._documents: Dict[str, str] = {}
        self._doc_metadata: Dict[str, Dict[str, Any]] = {}
        self._tf: Dict[str, Dict[str, float]] = {}
        self._idf: Dict[str, float] = {}
        self._doc_count: int = 0
        self._token_doc_freq: Counter = Counter()
        self._top_k: int = top_k
        self._score_threshold: float = score_threshold
        self._built: bool = False
        self._index_hash: str = ""

    def add_document(
        self,
        doc_id: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a document to the index."""
        self._documents[doc_id] = content
        self._doc_metadata[doc_id] = metadata or {}
        self._built = False

    def build(self) -> None:
        """Build the TF-IDF index from all added documents."""
        start = time.perf_counter()
        self._doc_count = len(self._documents)
        if self._doc_count == 0:
            logger.warning("No documents to index")
            return

        self._token_doc_freq = Counter()
        self._tf = {}

        for doc_id, content in self._documents.items():
            tokens = self._tokenize(content)
            token_counts = Counter(tokens)
            total_tokens = len(tokens)
            self._tf[doc_id] = {}
            unique_tokens = set(tokens)
            for token in unique_tokens:
                self._token_doc_freq[token] += 1
            for token, count in token_counts.items():
                self._tf[doc_id][token] = count / max(total_tokens, 1)

        self._idf = {}
        for token, doc_freq in self._token_doc_freq.items():
            self._idf[token] = math.log((self._doc_count + 1) / (doc_freq + 1)) + 1

        content_for_hash = json.dumps(sorted(self._documents.keys()))
        self._index_hash = hashlib.sha256(content_for_hash.encode("utf-8")).hexdigest()
        self._built = True

        elapsed = (time.perf_counter() - start) * 1000
        logger.info(
            "Search index built in {:.1f}ms: {} docs, {} unique tokens",
            elapsed,
            self._doc_count,
            len(self._idf),
        )

    def search(
        self,
        query: str,
        top_k: Optional[int] = None,
        category_filter: Optional[str] = None,
    ) -> List[SearchResult]:
        """Search the index for documents matching the query."""
        if not self._built:
            self.build()

        k = top_k or self._top_k
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        scores: Dict[str, float] = {}
        matched_tokens_map: Dict[str, List[str]] = defaultdict(list)

        for token in query_tokens:
            if token not in self._idf:
                continue
            idf_val = self._idf[token]
            for doc_id in self._documents:
                tf_val = self._tf.get(doc_id, {}).get(token, 0.0)
                if tf_val > 0:
                    tfidf = tf_val * idf_val
                    scores[doc_id] = scores.get(doc_id, 0.0) + tfidf
                    matched_tokens_map[doc_id].append(token)

        results: List[SearchResult] = []
        for doc_id, tf_idf_score in scores.items():
            if tf_idf_score < self._score_threshold:
                continue

            meta = self._doc_metadata.get(doc_id, {})
            category = meta.get("category", "unknown")

            if category_filter and category != category_filter:
                continue

            authority = meta.get("authority_score", 0.75)
            recency = 1.0
            staleness = meta.get("staleness_days", 0)
            if staleness > 0:
                recency = max(0.5, 1.0 - (staleness / 365.0))

            combined_score = tf_idf_score * authority * recency

            results.append(SearchResult(
                doc_id=doc_id,
                topic=meta.get("topic", doc_id),
                content=self._documents[doc_id][:500],
                score=combined_score,
                tf_idf_score=tf_idf_score,
                authority_score=authority,
                recency_score=recency,
                leg_category=category,
                matched_tokens=matched_tokens_map.get(doc_id, []),
                source="doctrine_cache",
                jurisdiction=meta.get("jurisdiction"),
                metadata=meta,
            ))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:k]

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into lowercase terms, removing stopwords and short tokens."""
        stopwords = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "shall",
            "should", "may", "might", "can", "could", "of", "in", "to", "for",
            "with", "on", "at", "by", "from", "as", "into", "through", "during",
            "before", "after", "above", "below", "between", "under", "over",
            "and", "but", "or", "nor", "not", "so", "yet", "both", "either",
            "neither", "each", "every", "all", "any", "few", "more", "most",
            "other", "some", "such", "no", "only", "own", "same", "than", "too",
            "very", "just", "because", "if", "when", "while", "where", "how",
            "what", "which", "who", "whom", "this", "that", "these", "those",
            "it", "its", "they", "them", "their", "we", "us", "our", "he", "him",
            "his", "she", "her", "i", "me", "my",
        }
        raw = re.sub(r"[^a-zA-Z0-9_]", " ", text.lower())
        tokens = raw.split()
        return [t for t in tokens if len(t) >= 2 and t not in stopwords]

    def get_index_stats(self) -> Dict[str, Any]:
        """Return index statistics."""
        return {
            "document_count": self._doc_count,
            "unique_tokens": len(self._idf),
            "built": self._built,
            "index_hash": self._index_hash[:16] if self._index_hash else "",
            "top_k": self._top_k,
            "score_threshold": self._score_threshold,
        }

    def get_index_hash(self) -> str:
        """Return the SHA-256 hash of the index."""
        return self._index_hash


def compute_query_hash(query: str, mode: str) -> str:
    """Compute a deterministic SHA-256 hash for a query + mode."""
    content = f"{query.strip().lower()}|{mode.strip().lower()}"
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


# ============================================================================
# MODULE-LEVEL INDEX SINGLETON
# ============================================================================

_SEARCH_INDEX: Optional[DoctrineSearchIndex] = None


def get_search_index() -> DoctrineSearchIndex:
    """Return the singleton search index, building if necessary."""
    global _SEARCH_INDEX
    if _SEARCH_INDEX is None:
        _SEARCH_INDEX = DoctrineSearchIndex()
    return _SEARCH_INDEX


# ============================================================================
# LEGISLATIVE HISTORY SEARCHER
# ============================================================================

class LegislativeHistorySearcher:
    """Searches and ranks legislative history sources by reliability."""

    RELIABILITY_WEIGHTS: ClassVar[Dict[str, float]] = {
        "conference_report": 0.95,
        "committee_report": 0.85,
        "committee_hearing": 0.70,
        "floor_manager_statement": 0.75,
        "sponsor_statement": 0.65,
        "floor_colloquy": 0.50,
        "individual_member_statement": 0.40,
        "presidential_signing_statement": 0.35,
        "rejected_amendment": 0.55,
        "subsequent_legislative_history": 0.25,
        "crs_report": 0.60,
    }

    def rank_sources(self, sources: List[Dict[str, Any]]) -> List[LegislativeHistoryEntry]:
        """Rank legislative history sources by reliability."""
        entries: List[LegislativeHistoryEntry] = []
        for source in sources:
            source_type = source.get("type", "individual_member_statement")
            reliability = self.RELIABILITY_WEIGHTS.get(source_type, 0.30)
            relevance = source.get("relevance", 0.5)
            entry = LegislativeHistoryEntry(
                source_type=source_type,
                chamber=source.get("chamber", "unknown"),
                date=source.get("date", ""),
                speaker=source.get("speaker", "unknown"),
                content_excerpt=source.get("content", ""),
                relevance_score=relevance,
                reliability_weight=reliability,
                citation=source.get("citation", ""),
            )
            entries.append(entry)
        entries.sort(key=lambda e: e.reliability_weight * e.relevance_score, reverse=True)
        return entries

    def assess_legislative_history_value(
        self, question: str, available_sources: List[str]
    ) -> Dict[str, Any]:
        """Assess whether legislative history is valuable for interpreting a provision."""
        has_high_reliability = any(
            self.RELIABILITY_WEIGHTS.get(s, 0) >= 0.80 for s in available_sources
        )
        has_conference_report = "conference_report" in available_sources
        has_committee_report = "committee_report" in available_sources

        textualist_concern = (
            "Under textualism (Bostock v. Clayton County, 2020), legislative history is not an "
            "authoritative source of statutory meaning. The current Supreme Court majority is "
            "generally skeptical of reliance on legislative history."
        )
        purposivist_value = (
            "Under purposivism, legislative history illuminates the evil Congress targeted "
            "and the remedy it chose. Conference and committee reports are the most reliable sources."
        )

        recommendation: str
        if has_conference_report:
            recommendation = "Conference report available; strongest legislative history source. Consider using as supporting evidence even before textualist courts."
        elif has_committee_report:
            recommendation = "Committee report available; reliable source of legislative purpose. Some textualist judges will consider committee reports to confirm textual meaning."
        elif has_high_reliability:
            recommendation = "High-reliability sources available. Use to support textual arguments; do not rely on legislative history as the primary basis."
        else:
            recommendation = "Only low-reliability sources available. Legislative history may be of limited value; focus on textual and structural arguments."

        return {
            "question_excerpt": question[:300],
            "available_sources": available_sources,
            "high_reliability_available": has_high_reliability,
            "textualist_concern": textualist_concern,
            "purposivist_value": purposivist_value,
            "recommendation": recommendation,
            "assessed_at": datetime.now(timezone.utc).isoformat(),
        }


# ============================================================================
# CANON OF CONSTRUCTION MATCHER
# ============================================================================

class CanonOfConstructionMatcher:
    """Matches statutory interpretation questions to applicable canons."""

    CANONS: ClassVar[Dict[str, Dict[str, Any]]] = {
        "plain_meaning": {
            "triggers": ["plain", "text", "literal", "ordinary meaning", "unambiguous", "clear"],
            "description": "Apply the statute according to its plain text when unambiguous",
            "cases": ["Caminetti v. United States, 242 U.S. 470 (1917)", "Bostock v. Clayton County, 590 U.S. 644 (2020)"],
            "counter": ["Absurdity doctrine may override plain meaning", "Text may be less clear than it appears"],
        },
        "ejusdem_generis": {
            "triggers": ["general term", "catch-all", "other", "list", "enumeration", "same kind"],
            "description": "Limit general terms following specific lists to the same class",
            "cases": ["Circuit City v. Adams, 532 U.S. 105 (2001)", "Yates v. United States, 574 U.S. 528 (2015)"],
            "counter": ["Specific items may not share a common genus", "Ali v. FBI: canon not automatic"],
        },
        "noscitur_a_sociis": {
            "triggers": ["associated", "neighbor", "context", "surrounding words", "grouped"],
            "description": "Interpret ambiguous words by reference to their statutory neighbors",
            "cases": ["Jarecki v. G.D. Searle, 367 U.S. 303 (1961)", "Gustafson v. Alloyd, 513 U.S. 561 (1995)"],
            "counter": ["Word may have independent force regardless of neighbors"],
        },
        "expressio_unius": {
            "triggers": ["omitted", "excluded", "not mentioned", "not listed", "absent", "silent"],
            "description": "The expression of one thing implies the exclusion of others",
            "cases": ["Russello v. United States, 464 U.S. 16 (1983)", "NLRB v. SW General, 580 U.S. 288 (2017)"],
            "counter": ["List may be illustrative, not exhaustive", "Silence may be inadvertent"],
        },
        "rule_of_lenity": {
            "triggers": ["criminal", "penal", "penalty", "imprisonment", "ambiguous criminal"],
            "description": "Resolve ambiguity in criminal statutes in favor of the defendant",
            "cases": ["Yates v. United States, 574 U.S. 528 (2015)", "Dubin v. United States, 599 U.S. 110 (2023)"],
            "counter": ["Requires 'grievous' ambiguity (Muscarello)", "Lenity is a tiebreaker of last resort"],
        },
        "avoidance": {
            "triggers": ["constitutional", "unconstitutional", "constitutional doubt", "avoid", "serious question"],
            "description": "Choose the interpretation that avoids serious constitutional questions",
            "cases": ["NLRB v. Catholic Bishop, 440 U.S. 490 (1979)", "Bond v. United States, 572 U.S. 844 (2014)"],
            "counter": ["Cannot torture text to avoid constitutional issues", "Textualists skeptical of avoidance"],
        },
        "whole_act": {
            "triggers": ["context", "whole statute", "structure", "harmonize", "other sections", "read together"],
            "description": "Read each provision in the context of the entire statute",
            "cases": ["King v. Burwell, 576 U.S. 473 (2015)", "FDA v. Brown & Williamson, 529 U.S. 120 (2000)"],
            "counter": ["Poor drafting may prevent harmonization", "Different sections may use terms differently"],
        },
        "surplusage": {
            "triggers": ["superfluous", "redundant", "meaningless", "surplusage", "every word"],
            "description": "Presume every word in the statute has independent meaning",
            "cases": ["Hibbs v. Winn, 542 U.S. 88 (2004)", "Marx v. General Revenue Corp., 568 U.S. 371 (2013)"],
            "counter": ["Congress sometimes uses redundant language for emphasis"],
        },
    }

    def match_canons(self, query: str, top_k: int = 3) -> List[CanonMatchResult]:
        """Match a query to applicable canons of construction."""
        query_lower = query.lower()
        scored: List[Tuple[float, str]] = []

        for canon_name, canon_info in self.CANONS.items():
            triggers = canon_info["triggers"]
            score = 0.0
            for trigger in triggers:
                if trigger in query_lower:
                    score += 0.3
            if canon_name.replace("_", " ") in query_lower:
                score += 0.5
            if score > 0:
                scored.append((score, canon_name))

        scored.sort(key=lambda x: x[0], reverse=True)
        results: List[CanonMatchResult] = []
        for score, name in scored[:top_k]:
            info = self.CANONS[name]
            results.append(CanonMatchResult(
                canon_name=name,
                relevance_score=min(score, 1.0),
                description=info["description"],
                application_steps=[
                    f"Step 1: Identify the relevant statutory text",
                    f"Step 2: Apply {name.replace('_', ' ')} canon",
                    f"Step 3: Assess result against statutory structure",
                    f"Step 4: Consider counter-arguments",
                    f"Step 5: Reach conclusion with confidence level",
                ],
                supporting_cases=info["cases"],
                counter_arguments=info["counter"],
            ))

        if not results:
            results.append(CanonMatchResult(
                canon_name="plain_meaning",
                relevance_score=0.5,
                description="Default: Apply the statute according to its plain text",
                application_steps=[
                    "Step 1: Examine the statutory text",
                    "Step 2: Determine ordinary public meaning",
                    "Step 3: If unambiguous, apply as written",
                    "Step 4: If ambiguous, proceed to other canons",
                    "Step 5: Consider context and structure",
                ],
                supporting_cases=self.CANONS["plain_meaning"]["cases"],
                counter_arguments=self.CANONS["plain_meaning"]["counter"],
            ))

        return results


# ============================================================================
# RULEMAKING TRACKER
# ============================================================================

class RulemakingSearchTracker:
    """Search and track regulatory rulemaking activities."""

    RULEMAKING_TYPES: ClassVar[Dict[str, Dict[str, Any]]] = {
        "notice_and_comment": {
            "apa_section": "5 USC 553",
            "steps": ["NPRM", "Public Comment", "Final Rule", "Effective Date"],
            "filibuster_proof": True,
            "typical_duration_months": "6-18",
        },
        "formal_rulemaking": {
            "apa_section": "5 USC 556-557",
            "steps": ["Notice", "Trial-type Hearing", "Initial Decision", "Final Decision"],
            "filibuster_proof": True,
            "typical_duration_months": "12-36",
        },
        "direct_final_rule": {
            "apa_section": "5 USC 553 (variation)",
            "steps": ["Publication", "Comment Period", "Effective if No Adverse Comments"],
            "filibuster_proof": True,
            "typical_duration_months": "2-4",
        },
        "interim_final_rule": {
            "apa_section": "5 USC 553(b)(B) good cause",
            "steps": ["Publication as Final", "Post-Promulgation Comments", "Possible Revision"],
            "filibuster_proof": True,
            "typical_duration_months": "1-6",
        },
        "negotiated_rulemaking": {
            "apa_section": "Negotiated Rulemaking Act, 5 USC 561-570a",
            "steps": ["Committee Formation", "Negotiation", "Consensus", "NPRM", "Final Rule"],
            "filibuster_proof": True,
            "typical_duration_months": "12-24",
        },
    }

    def get_rulemaking_info(self, rulemaking_type: str) -> Dict[str, Any]:
        """Get information about a specific rulemaking type."""
        info = self.RULEMAKING_TYPES.get(rulemaking_type)
        if info:
            return {
                "type": rulemaking_type,
                **info,
                "deference_standard": "Independent judgment (post-Loper Bright)",
                "challenge_standard": "Arbitrary and capricious (Motor Vehicle Mfrs. v. State Farm, 463 U.S. 29 (1983))",
            }
        return {
            "type": rulemaking_type,
            "error": f"Unknown rulemaking type: {rulemaking_type}",
            "available_types": list(self.RULEMAKING_TYPES.keys()),
        }

    def assess_cra_vulnerability(self, rule_info: Dict[str, Any]) -> Dict[str, Any]:
        """Assess whether a rule is vulnerable to Congressional Review Act disapproval."""
        is_major_rule = rule_info.get("is_major_rule", False)
        annual_economic_impact = rule_info.get("annual_economic_impact", 0)
        political_controversy = rule_info.get("political_controversy", "low")
        presidential_transition = rule_info.get("presidential_transition", False)

        vulnerability_score = 0.0
        factors: List[str] = []

        if is_major_rule or annual_economic_impact >= 100_000_000:
            vulnerability_score += 0.3
            factors.append("Major rule with significant economic impact (>=100M annually)")
        if political_controversy in ("high", "very_high"):
            vulnerability_score += 0.25
            factors.append("High political controversy increases CRA disapproval likelihood")
        if presidential_transition:
            vulnerability_score += 0.35
            factors.append("Presidential transition period: CRA lookback window applies to late-term rules")

        vulnerability_score = min(vulnerability_score, 1.0)

        return {
            "rule_info": rule_info,
            "cra_vulnerability_score": round(vulnerability_score, 4),
            "factors": factors,
            "cra_statute": "5 USC 801-808",
            "consequence_of_disapproval": "Rule treated as if never took effect; agency barred from reissuing in substantially the same form",
            "assessed_at": datetime.now(timezone.utc).isoformat(),
        }


# ============================================================================
# BILL COMPARISON ENGINE
# ============================================================================

class BillComparisonEngine:
    """Compares bill versions and amendments."""

    def compare_bills(
        self,
        bill_a: Dict[str, Any],
        bill_b: Dict[str, Any],
    ) -> BillComparisonResult:
        """Compare two bill versions or related bills."""
        sections_a = set(bill_a.get("sections", []))
        sections_b = set(bill_b.get("sections", []))

        added = sorted(sections_b - sections_a)
        removed = sorted(sections_a - sections_b)
        common = sections_a & sections_b
        modified: List[str] = []
        for section in common:
            text_a = bill_a.get("section_text", {}).get(section, "")
            text_b = bill_b.get("section_text", {}).get(section, "")
            if text_a != text_b:
                modified.append(section)

        differences: List[str] = []
        if added:
            differences.append(f"{len(added)} sections added in version B")
        if removed:
            differences.append(f"{len(removed)} sections removed in version B")
        if modified:
            differences.append(f"{len(modified)} sections modified between versions")

        preemption_a = set(bill_a.get("preemption_provisions", []))
        preemption_b = set(bill_b.get("preemption_provisions", []))
        preemption_changes: List[str] = []
        new_preemption = preemption_b - preemption_a
        removed_preemption = preemption_a - preemption_b
        if new_preemption:
            preemption_changes.append(f"New preemption provisions: {', '.join(sorted(new_preemption))}")
        if removed_preemption:
            preemption_changes.append(f"Removed preemption provisions: {', '.join(sorted(removed_preemption))}")

        funding_a = bill_a.get("funding_level", 0)
        funding_b = bill_b.get("funding_level", 0)
        funding_changes: List[str] = []
        if funding_a != funding_b:
            change = funding_b - funding_a
            direction = "increased" if change > 0 else "decreased"
            funding_changes.append(f"Funding {direction} by {abs(change)}")

        total_changes = len(added) + len(removed) + len(modified)
        total_sections = max(len(sections_a | sections_b), 1)
        compatibility = 1.0 - (total_changes / total_sections)

        return BillComparisonResult(
            bill_a_id=bill_a.get("bill_id", "A"),
            bill_b_id=bill_b.get("bill_id", "B"),
            sections_added=added,
            sections_removed=removed,
            sections_modified=modified,
            key_differences=differences,
            compatibility_score=max(0.0, compatibility),
            preemption_changes=preemption_changes,
            funding_changes=funding_changes,
        )


# ============================================================================
# SINGLETON ACCESSORS
# ============================================================================

_LEG_HISTORY_SEARCHER: Optional[LegislativeHistorySearcher] = None
_CANON_MATCHER: Optional[CanonOfConstructionMatcher] = None
_RULEMAKING_TRACKER: Optional[RulemakingSearchTracker] = None
_BILL_COMPARISON: Optional[BillComparisonEngine] = None


def get_leg_history_searcher() -> LegislativeHistorySearcher:
    """Return the singleton legislative history searcher."""
    global _LEG_HISTORY_SEARCHER
    if _LEG_HISTORY_SEARCHER is None:
        _LEG_HISTORY_SEARCHER = LegislativeHistorySearcher()
    return _LEG_HISTORY_SEARCHER


def get_canon_matcher() -> CanonOfConstructionMatcher:
    """Return the singleton canon matcher."""
    global _CANON_MATCHER
    if _CANON_MATCHER is None:
        _CANON_MATCHER = CanonOfConstructionMatcher()
    return _CANON_MATCHER


def get_rulemaking_tracker() -> RulemakingSearchTracker:
    """Return the singleton rulemaking tracker."""
    global _RULEMAKING_TRACKER
    if _RULEMAKING_TRACKER is None:
        _RULEMAKING_TRACKER = RulemakingSearchTracker()
    return _RULEMAKING_TRACKER


def get_bill_comparison() -> BillComparisonEngine:
    """Return the singleton bill comparison engine."""
    global _BILL_COMPARISON
    if _BILL_COMPARISON is None:
        _BILL_COMPARISON = BillComparisonEngine()
    return _BILL_COMPARISON
