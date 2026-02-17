"""
LG07 Employment Law Engine - Search Module
=============================================
TF-IDF based vector search over employment law doctrine blocks,
statutory provisions, case law references, and regulatory guidance.

Components:
    - DoctrineSearchIndex: TF-IDF inverted index for doctrine search
    - SearchResult: Ranked search result with scoring breakdown
    - StatuteSearchEngine: Statute-specific search with section matching
    - CaseSearchEngine: Case law search with citation parsing
    - HybridSearchEngine: Combined keyword + semantic + statute search
    - EmploymentClaimClassifier: Classify query into claim type
    - JurisdictionRouter: Route queries to federal vs state analysis
    - SearchResultAggregator: Merge and deduplicate results across engines

Version: 1.0.0
Engine: LG07 Employment Law
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
    employment_category: str
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
            "employment_category": self.employment_category,
            "matched_tokens": self.matched_tokens,
            "source": self.source,
            "metadata": self.metadata,
        }


# ============================================================================
# CLAIM CLASSIFICATION
# ============================================================================

class ClaimType(Enum):
    """Employment law claim classification."""
    DISCRIMINATION = "discrimination"
    HARASSMENT = "harassment"
    RETALIATION = "retaliation"
    WAGE_HOUR = "wage_hour"
    LEAVE = "leave"
    SAFETY = "safety"
    BENEFITS = "benefits"
    LABOR_RELATIONS = "labor_relations"
    TERMINATION = "termination"
    NON_COMPETE = "non_compete"
    WORKERS_COMP = "workers_comp"
    WHISTLEBLOWER = "whistleblower"
    GENERAL = "general"


CLAIM_KEYWORDS: Dict[ClaimType, List[str]] = {
    ClaimType.DISCRIMINATION: [
        "discrimination", "bias", "disparate", "title vii", "race", "sex", "gender",
        "religion", "national origin", "color", "protected class", "bfoq",
        "pregnancy", "pda", "equal opportunity",
    ],
    ClaimType.HARASSMENT: [
        "harassment", "hostile", "sexual harassment", "quid pro quo", "unwelcome",
        "severe or pervasive", "toxic", "abusive", "inappropriate",
    ],
    ClaimType.RETALIATION: [
        "retaliation", "retaliated", "reprisal", "adverse action", "punished",
        "fired for complaining", "filed complaint",
    ],
    ClaimType.WAGE_HOUR: [
        "overtime", "minimum wage", "flsa", "wage", "hour", "exempt", "nonexempt",
        "misclassification", "off the clock", "tip", "comp time", "salary",
        "independent contractor", "1099",
    ],
    ClaimType.LEAVE: [
        "fmla", "leave", "medical leave", "family leave", "intermittent",
        "serious health condition", "maternity", "paternity",
    ],
    ClaimType.SAFETY: [
        "osha", "safety", "hazard", "unsafe", "injury", "citation",
        "general duty", "workplace safety", "violation",
    ],
    ClaimType.BENEFITS: [
        "erisa", "benefits", "pension", "401k", "retirement", "health plan",
        "fiduciary", "vesting", "cobra",
    ],
    ClaimType.LABOR_RELATIONS: [
        "union", "nlra", "nlrb", "collective bargaining", "concerted activity",
        "unfair labor practice", "organizing", "strike",
    ],
    ClaimType.TERMINATION: [
        "fired", "terminated", "wrongful termination", "at will", "constructive discharge",
        "wrongful discharge", "public policy", "implied contract",
    ],
    ClaimType.NON_COMPETE: [
        "non-compete", "noncompete", "non-solicitation", "restrictive covenant",
        "trade secret", "confidentiality", "garden leave",
    ],
    ClaimType.WORKERS_COMP: [
        "workers comp", "workers compensation", "work injury", "occupational",
        "on the job injury", "comp claim",
    ],
    ClaimType.WHISTLEBLOWER: [
        "whistleblower", "whistle blower", "sox", "dodd frank", "qui tam",
        "false claims", "reported fraud", "reported violation",
    ],
}


# ============================================================================
# TOKENIZER
# ============================================================================

class EmploymentLawTokenizer:
    """Tokenizer optimized for employment law text with legal term preservation."""

    LEGAL_COMPOUNDS: ClassVar[Dict[str, str]] = {
        "title vii": "title_vii",
        "title seven": "title_vii",
        "hostile work environment": "hostile_work_environment",
        "quid pro quo": "quid_pro_quo",
        "at will": "at_will",
        "at-will": "at_will",
        "disparate impact": "disparate_impact",
        "disparate treatment": "disparate_treatment",
        "minimum wage": "minimum_wage",
        "overtime pay": "overtime_pay",
        "off the clock": "off_the_clock",
        "tip credit": "tip_credit",
        "comp time": "comp_time",
        "serious health condition": "serious_health_condition",
        "intermittent leave": "intermittent_leave",
        "essential functions": "essential_functions",
        "reasonable accommodation": "reasonable_accommodation",
        "interactive process": "interactive_process",
        "undue hardship": "undue_hardship",
        "public policy": "public_policy",
        "wrongful termination": "wrongful_termination",
        "wrongful discharge": "wrongful_discharge",
        "constructive discharge": "constructive_discharge",
        "non compete": "non_compete",
        "non solicitation": "non_solicitation",
        "trade secret": "trade_secret",
        "unfair labor practice": "unfair_labor_practice",
        "concerted activity": "concerted_activity",
        "collective bargaining": "collective_bargaining",
        "general duty clause": "general_duty_clause",
        "workers compensation": "workers_compensation",
        "workers comp": "workers_comp",
        "mass layoff": "mass_layoff",
        "plant closing": "plant_closing",
        "warn act": "warn_act",
        "protected class": "protected_class",
        "protected activity": "protected_activity",
        "adverse action": "adverse_action",
        "back pay": "back_pay",
        "front pay": "front_pay",
        "punitive damages": "punitive_damages",
        "compensatory damages": "compensatory_damages",
        "liquidated damages": "liquidated_damages",
    }

    STOP_WORDS: ClassVar[Set[str]] = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "can", "shall", "to", "of", "in", "for",
        "on", "with", "at", "by", "from", "as", "into", "through", "during",
        "before", "after", "above", "below", "between", "under", "over",
        "and", "but", "or", "nor", "not", "so", "yet", "both", "either",
        "neither", "each", "every", "all", "any", "few", "more", "most",
        "other", "some", "such", "no", "only", "same", "than", "too", "very",
        "just", "because", "if", "when", "while", "where", "how", "what",
        "which", "who", "whom", "this", "that", "these", "those", "my",
        "your", "his", "her", "its", "our", "their", "i", "me", "we", "us",
        "you", "he", "she", "it", "they", "them",
    }

    def tokenize(self, text: str) -> List[str]:
        """Tokenize text preserving legal compound terms."""
        text_lower = text.lower().strip()

        # Phase 1: Replace compound terms with tokens
        for compound, token in sorted(self.LEGAL_COMPOUNDS.items(), key=lambda x: -len(x[0])):
            text_lower = text_lower.replace(compound, token)

        # Phase 2: Split on non-alphanumeric (preserve underscores)
        raw_tokens = re.findall(r"[a-z0-9_]+", text_lower)

        # Phase 3: Remove stop words, keep legal terms
        tokens = [t for t in raw_tokens if t not in self.STOP_WORDS or t in self.LEGAL_COMPOUNDS.values()]

        return tokens

    def tokenize_with_bigrams(self, text: str) -> List[str]:
        """Tokenize and include bigrams for phrase detection."""
        tokens = self.tokenize(text)
        bigrams = [f"{tokens[i]}_{tokens[i+1]}" for i in range(len(tokens) - 1)]
        return tokens + bigrams


# ============================================================================
# EMPLOYMENT CLAIM CLASSIFIER
# ============================================================================

class EmploymentClaimClassifier:
    """Classify queries into employment law claim types."""

    def __init__(self) -> None:
        """Initialize with keyword index."""
        self._keyword_index: Dict[str, List[ClaimType]] = {}
        for claim_type, keywords in CLAIM_KEYWORDS.items():
            for keyword in keywords:
                if keyword not in self._keyword_index:
                    self._keyword_index[keyword] = []
                self._keyword_index[keyword].append(claim_type)

    def classify(self, query: str) -> List[Tuple[ClaimType, float]]:
        """Classify a query into one or more claim types with confidence scores."""
        query_lower = query.lower()
        scores: Counter = Counter()

        for keyword, claim_types in self._keyword_index.items():
            if keyword in query_lower:
                for ct in claim_types:
                    scores[ct] += 1.0

        if not scores:
            return [(ClaimType.GENERAL, 0.3)]

        max_score = max(scores.values())
        results: List[Tuple[ClaimType, float]] = []
        for claim_type, score in scores.most_common():
            normalized_score = min(0.99, score / max(max_score, 1.0))
            results.append((claim_type, round(normalized_score, 4)))

        return results

    def get_primary_claim(self, query: str) -> Tuple[ClaimType, float]:
        """Get the most likely claim type for a query."""
        results = self.classify(query)
        return results[0] if results else (ClaimType.GENERAL, 0.3)


# ============================================================================
# TF-IDF INDEX
# ============================================================================

class DoctrineSearchIndex:
    """TF-IDF inverted index for employment law doctrine search."""

    def __init__(self) -> None:
        """Initialize empty index."""
        self._tokenizer = EmploymentLawTokenizer()
        self._classifier = EmploymentClaimClassifier()
        self._documents: Dict[str, Dict[str, Any]] = {}
        self._term_doc_freq: Counter = Counter()
        self._doc_term_freq: Dict[str, Counter] = {}
        self._doc_lengths: Dict[str, int] = {}
        self._avg_doc_length: float = 0.0
        self._total_docs: int = 0
        self._index_hash: str = ""
        self._built: bool = False
        self._build_time_ms: float = 0.0
        logger.info("DoctrineSearchIndex initialized for LG07 Employment Law")

    def add_document(self, doc_id: str, topic: str, content: str,
                     category: str = "", authority: str = "",
                     confidence: float = 0.5, tags: Optional[List[str]] = None,
                     last_updated: str = "", metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a document to the index."""
        self._documents[doc_id] = {
            "topic": topic,
            "content": content,
            "category": category,
            "authority": authority,
            "confidence": confidence,
            "tags": tags or [],
            "last_updated": last_updated,
            "metadata": metadata or {},
        }
        tokens = self._tokenizer.tokenize_with_bigrams(f"{topic} {content} {' '.join(tags or [])}")
        term_freq = Counter(tokens)
        self._doc_term_freq[doc_id] = term_freq
        self._doc_lengths[doc_id] = len(tokens)

        for term in term_freq:
            self._term_doc_freq[term] += 1

        self._total_docs = len(self._documents)
        self._built = False

    def build(self) -> None:
        """Finalize the index for searching."""
        start = time.monotonic()
        if self._total_docs > 0:
            self._avg_doc_length = sum(self._doc_lengths.values()) / self._total_docs
        else:
            self._avg_doc_length = 0.0

        # Compute index hash
        index_data = json.dumps(sorted(self._documents.keys()))
        self._index_hash = hashlib.sha256(index_data.encode()).hexdigest()[:16]
        self._built = True
        self._build_time_ms = (time.monotonic() - start) * 1000.0
        logger.info("Search index built: {} docs, avg_len={:.1f}, hash={}",
                     self._total_docs, self._avg_doc_length, self._index_hash)

    def _bm25_score(self, query_tokens: List[str], doc_id: str,
                     k1: float = 1.5, b: float = 0.75) -> float:
        """Compute BM25 score for a document against query tokens."""
        if doc_id not in self._doc_term_freq:
            return 0.0

        doc_tf = self._doc_term_freq[doc_id]
        doc_len = self._doc_lengths.get(doc_id, 0)
        score = 0.0

        for term in query_tokens:
            if term not in doc_tf:
                continue
            tf = doc_tf[term]
            df = self._term_doc_freq.get(term, 0)
            if df == 0:
                continue

            idf = math.log((self._total_docs - df + 0.5) / (df + 0.5) + 1.0)
            tf_norm = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len / max(self._avg_doc_length, 1.0)))
            score += idf * tf_norm

        return score

    def _authority_boost(self, doc: Dict[str, Any]) -> float:
        """Compute authority boost based on source hierarchy."""
        authority = doc.get("authority", "").lower()
        if "supreme court" in authority or "u.s." in authority:
            return 1.5
        if "circuit" in authority or "court of appeals" in authority:
            return 1.3
        if "usc" in authority or "u.s.c." in authority:
            return 1.4
        if "cfr" in authority or "c.f.r." in authority:
            return 1.2
        if "eeoc" in authority or "dol" in authority or "nlrb" in authority:
            return 1.1
        return 1.0

    def _recency_boost(self, doc: Dict[str, Any]) -> float:
        """Compute recency boost based on last update date."""
        last_updated = doc.get("last_updated", "")
        if not last_updated:
            return 0.8
        try:
            update_date = datetime.fromisoformat(last_updated.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            age_days = (now - update_date).days
            if age_days < 90:
                return 1.2
            if age_days < 365:
                return 1.0
            if age_days < 730:
                return 0.9
            return 0.8
        except (ValueError, TypeError):
            return 0.8

    def _category_boost(self, doc_category: str, query_categories: List[str]) -> float:
        """Boost score if document category matches query category."""
        if not query_categories:
            return 1.0
        if doc_category in query_categories:
            return 1.5
        return 1.0

    def search(self, query: str, max_results: int = 20,
               min_score: float = 0.01, category_filter: Optional[str] = None,
               boost_categories: Optional[List[str]] = None) -> List[SearchResult]:
        """Search the index with BM25 + authority + recency scoring."""
        if not self._built:
            self.build()

        start = time.monotonic()
        tokens = self._tokenizer.tokenize_with_bigrams(query)

        if not tokens:
            return []

        results: List[SearchResult] = []
        claim_type, claim_conf = self._classifier.get_primary_claim(query)

        for doc_id, doc in self._documents.items():
            if category_filter and doc.get("category", "") != category_filter:
                continue

            bm25 = self._bm25_score(tokens, doc_id)
            if bm25 < min_score:
                continue

            auth_boost = self._authority_boost(doc)
            recency_boost = self._recency_boost(doc)
            cat_boost = self._category_boost(doc.get("category", ""), boost_categories or [])

            final_score = bm25 * auth_boost * recency_boost * cat_boost

            matched = [t for t in tokens if t in self._doc_term_freq.get(doc_id, {})]

            results.append(SearchResult(
                doc_id=doc_id,
                topic=doc["topic"],
                content=doc["content"],
                score=final_score,
                tf_idf_score=bm25,
                authority_score=auth_boost,
                recency_score=recency_boost,
                employment_category=doc.get("category", "general"),
                matched_tokens=matched,
                source="doctrine_cache",
                metadata={
                    "confidence": doc.get("confidence", 0.5),
                    "tags": doc.get("tags", []),
                    "claim_type": claim_type.value,
                    "claim_confidence": claim_conf,
                    "category_boost": cat_boost,
                },
            ))

        results.sort(key=lambda r: r.score, reverse=True)
        elapsed = (time.monotonic() - start) * 1000.0
        logger.debug("Search '{}': {} results in {:.1f}ms", query[:80], len(results[:max_results]), elapsed)
        return results[:max_results]

    def keyword_search(self, keywords: List[str], max_results: int = 20) -> List[SearchResult]:
        """Simple keyword-based search without BM25 weighting."""
        if not self._built:
            self.build()

        results: List[SearchResult] = []
        keywords_lower = [k.lower() for k in keywords]

        for doc_id, doc in self._documents.items():
            content_lower = doc["content"].lower()
            topic_lower = doc["topic"].lower()
            tags_lower = " ".join(doc.get("tags", [])).lower()
            combined = f"{topic_lower} {content_lower} {tags_lower}"

            matched: List[str] = []
            for kw in keywords_lower:
                if kw in combined:
                    matched.append(kw)

            if not matched:
                continue

            score = len(matched) / len(keywords_lower)

            results.append(SearchResult(
                doc_id=doc_id,
                topic=doc["topic"],
                content=doc["content"],
                score=score,
                tf_idf_score=score,
                authority_score=self._authority_boost(doc),
                recency_score=self._recency_boost(doc),
                employment_category=doc.get("category", "general"),
                matched_tokens=matched,
                source="keyword_search",
            ))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:max_results]

    def get_index_stats(self) -> Dict[str, Any]:
        """Get index statistics."""
        return {
            "total_documents": self._total_docs,
            "total_unique_terms": len(self._term_doc_freq),
            "avg_doc_length": round(self._avg_doc_length, 2),
            "index_hash": self._index_hash,
            "built": self._built,
            "build_time_ms": round(self._build_time_ms, 3),
            "top_terms": dict(self._term_doc_freq.most_common(30)),
        }

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific document by ID."""
        return self._documents.get(doc_id)

    def get_documents_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all documents in a category."""
        return [
            {"doc_id": did, **doc}
            for did, doc in self._documents.items()
            if doc.get("category", "") == category
        ]


# ============================================================================
# STATUTE SEARCH ENGINE
# ============================================================================

class StatuteSearchEngine:
    """Search engine specialized for employment statute lookups."""

    STATUTE_INDEX: ClassVar[Dict[str, Dict[str, Any]]] = {
        "29_usc_201": {"title": "FLSA", "full": "Fair Labor Standards Act", "sections": "201-219", "topic": "wage_hour"},
        "42_usc_2000e": {"title": "Title VII", "full": "Civil Rights Act of 1964", "sections": "2000e-2000e-17", "topic": "discrimination"},
        "42_usc_12101": {"title": "ADA", "full": "Americans with Disabilities Act", "sections": "12101-12213", "topic": "disability"},
        "29_usc_621": {"title": "ADEA", "full": "Age Discrimination in Employment Act", "sections": "621-634", "topic": "age_discrimination"},
        "29_usc_2601": {"title": "FMLA", "full": "Family and Medical Leave Act", "sections": "2601-2654", "topic": "leave"},
        "29_usc_2101": {"title": "WARN", "full": "Worker Adjustment and Retraining Notification Act", "sections": "2101-2109", "topic": "mass_layoff"},
        "29_usc_1001": {"title": "ERISA", "full": "Employee Retirement Income Security Act", "sections": "1001-1461", "topic": "benefits"},
        "29_usc_151": {"title": "NLRA", "full": "National Labor Relations Act", "sections": "151-169", "topic": "labor_relations"},
        "29_usc_651": {"title": "OSH Act", "full": "Occupational Safety and Health Act", "sections": "651-678", "topic": "safety"},
        "42_usc_1981": {"title": "Section 1981", "full": "Civil Rights Act of 1866", "sections": "1981", "topic": "race_discrimination"},
        "18_usc_1514a": {"title": "SOX", "full": "Sarbanes-Oxley Whistleblower Protection", "sections": "1514A", "topic": "whistleblower"},
        "29_usc_206d": {"title": "EPA", "full": "Equal Pay Act", "sections": "206(d)", "topic": "equal_pay"},
        "42_usc_2000ff": {"title": "GINA", "full": "Genetic Information Nondiscrimination Act", "sections": "2000ff", "topic": "genetic_discrimination"},
        "38_usc_4301": {"title": "USERRA", "full": "Uniformed Services Employment and Reemployment Rights Act", "sections": "4301-4335", "topic": "military_service"},
    }

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search for statutes matching a query."""
        query_lower = query.lower()
        results: List[Dict[str, Any]] = []

        for statute_key, info in self.STATUTE_INDEX.items():
            score = 0.0
            title_lower = info["title"].lower()
            full_lower = info["full"].lower()

            if title_lower in query_lower:
                score += 2.0
            if full_lower in query_lower:
                score += 1.5
            if info["topic"] in query_lower:
                score += 1.0

            words = query_lower.split()
            for word in words:
                if word in full_lower:
                    score += 0.3

            if score > 0:
                results.append({
                    "statute_key": statute_key,
                    "score": round(score, 4),
                    **info,
                })

        results.sort(key=lambda r: r["score"], reverse=True)
        return results


# ============================================================================
# CASE SEARCH ENGINE
# ============================================================================

class CaseSearchEngine:
    """Search engine for employment law case references."""

    LANDMARK_CASES: ClassVar[Dict[str, Dict[str, Any]]] = {
        "griggs_v_duke_power": {
            "citation": "401 U.S. 424 (1971)",
            "topic": "disparate_impact",
            "holding": "Facially neutral employment practices that have disparate impact on protected groups violate Title VII unless justified by business necessity.",
            "category": "title_vii",
        },
        "mcdonnell_douglas_v_green": {
            "citation": "411 U.S. 792 (1973)",
            "topic": "burden_shifting",
            "holding": "Established the burden-shifting framework for individual disparate treatment claims under Title VII.",
            "category": "title_vii",
        },
        "meritor_savings_v_vinson": {
            "citation": "477 U.S. 57 (1986)",
            "topic": "hostile_work_environment",
            "holding": "Hostile work environment sexual harassment is actionable under Title VII even without economic harm.",
            "category": "title_vii",
        },
        "burlington_industries_v_ellerth": {
            "citation": "524 U.S. 742 (1998)",
            "topic": "supervisor_harassment",
            "holding": "Employer vicarious liability for supervisor harassment with affirmative defense (Ellerth/Faragher).",
            "category": "title_vii",
        },
        "faragher_v_boca_raton": {
            "citation": "524 U.S. 775 (1998)",
            "topic": "supervisor_harassment",
            "holding": "Companion to Ellerth establishing employer affirmative defense to supervisor harassment claims.",
            "category": "title_vii",
        },
        "bostock_v_clayton_county": {
            "citation": "590 U.S. ___ (2020)",
            "topic": "lgbtq_discrimination",
            "holding": "Title VII protects employees against discrimination based on sexual orientation and gender identity.",
            "category": "title_vii",
        },
        "toyota_v_williams": {
            "citation": "534 U.S. 184 (2002)",
            "topic": "ada_disability_definition",
            "holding": "Defined 'substantially limits' for ADA disability determination (later superseded by ADAAA).",
            "category": "ada",
        },
        "us_airways_v_barnett": {
            "citation": "535 U.S. 391 (2002)",
            "topic": "reasonable_accommodation",
            "holding": "Reasonable accommodation under ADA ordinarily does not require superseding a seniority system.",
            "category": "ada",
        },
        "gross_v_fbl_financial": {
            "citation": "557 U.S. 167 (2009)",
            "topic": "adea_but_for_causation",
            "holding": "ADEA requires but-for causation (no mixed-motive framework).",
            "category": "adea",
        },
        "ibp_v_alvarez": {
            "citation": "546 U.S. 21 (2005)",
            "topic": "donning_doffing",
            "holding": "Time spent donning and doffing protective gear may be compensable under FLSA.",
            "category": "flsa",
        },
        "encino_motorcars_v_navarro": {
            "citation": "584 U.S. ___ (2018)",
            "topic": "flsa_exemption",
            "holding": "FLSA exemptions should not be construed narrowly; fair interpretation standard applies.",
            "category": "flsa",
        },
        "ragsdale_v_wolverine": {
            "citation": "535 U.S. 81 (2002)",
            "topic": "fmla_notice",
            "holding": "DOL regulation requiring employer notice of FMLA designation exceeds statutory authority.",
            "category": "fmla",
        },
        "nlrb_v_weingarten": {
            "citation": "420 U.S. 251 (1975)",
            "topic": "weingarten_rights",
            "holding": "Employees have right to union representation during investigatory interviews.",
            "category": "nlra",
        },
        "epic_systems_v_lewis": {
            "citation": "584 U.S. ___ (2018)",
            "topic": "class_action_waiver",
            "holding": "Arbitration agreements with class/collective action waivers are enforceable under FLSA/NLRA.",
            "category": "flsa",
        },
    }

    def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search landmark cases matching a query."""
        query_lower = query.lower()
        results: List[Dict[str, Any]] = []

        for case_key, info in self.LANDMARK_CASES.items():
            score = 0.0
            case_name = case_key.replace("_", " ")
            holding_lower = info["holding"].lower()
            topic_lower = info["topic"].replace("_", " ")

            if case_name in query_lower:
                score += 3.0
            if info["citation"].lower() in query_lower:
                score += 3.0
            if topic_lower in query_lower:
                score += 1.5
            if info["category"] in query_lower:
                score += 0.5

            words = set(query_lower.split())
            holding_words = set(holding_lower.split())
            overlap = words & holding_words
            score += len(overlap) * 0.1

            if score > 0:
                results.append({
                    "case_key": case_key,
                    "case_name": case_name.title().replace("V ", "v. "),
                    "score": round(score, 4),
                    **info,
                })

        results.sort(key=lambda r: r["score"], reverse=True)
        return results[:max_results]


# ============================================================================
# HYBRID SEARCH ENGINE
# ============================================================================

class HybridSearchEngine:
    """Combines doctrine, statute, and case search for comprehensive results."""

    def __init__(self, doctrine_index: DoctrineSearchIndex) -> None:
        """Initialize with doctrine index."""
        self._doctrine_index = doctrine_index
        self._statute_engine = StatuteSearchEngine()
        self._case_engine = CaseSearchEngine()
        self._classifier = EmploymentClaimClassifier()

    def search(self, query: str, max_results: int = 20,
               include_statutes: bool = True, include_cases: bool = True,
               category_filter: Optional[str] = None) -> Dict[str, Any]:
        """Perform hybrid search across all engines."""
        start = time.monotonic()
        claim_type, claim_conf = self._classifier.get_primary_claim(query)

        # Doctrine search
        doctrine_results = self._doctrine_index.search(
            query, max_results=max_results, category_filter=category_filter
        )

        # Statute search
        statute_results: List[Dict[str, Any]] = []
        if include_statutes:
            statute_results = self._statute_engine.search(query)

        # Case search
        case_results: List[Dict[str, Any]] = []
        if include_cases:
            case_results = self._case_engine.search(query, max_results=10)

        elapsed = (time.monotonic() - start) * 1000.0

        return {
            "query": query,
            "claim_type": claim_type.value,
            "claim_confidence": round(claim_conf, 4),
            "doctrine_results": [r.to_dict() for r in doctrine_results],
            "doctrine_count": len(doctrine_results),
            "statute_results": statute_results,
            "statute_count": len(statute_results),
            "case_results": case_results,
            "case_count": len(case_results),
            "total_results": len(doctrine_results) + len(statute_results) + len(case_results),
            "search_time_ms": round(elapsed, 3),
            "category_filter": category_filter,
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get hybrid search statistics."""
        return {
            "doctrine_index": self._doctrine_index.get_index_stats(),
            "statutes_indexed": len(StatuteSearchEngine.STATUTE_INDEX),
            "cases_indexed": len(CaseSearchEngine.LANDMARK_CASES),
        }


# ============================================================================
# SEARCH RESULT AGGREGATOR
# ============================================================================

class SearchResultAggregator:
    """Merge and deduplicate results from multiple search engines."""

    def aggregate(self, results_sets: List[List[SearchResult]],
                  max_results: int = 20) -> List[SearchResult]:
        """Merge multiple result sets, deduplicate, and re-rank."""
        seen_topics: Set[str] = set()
        all_results: List[SearchResult] = []

        for result_set in results_sets:
            for result in result_set:
                if result.topic not in seen_topics:
                    seen_topics.add(result.topic)
                    all_results.append(result)
                else:
                    # Boost score if found in multiple engines
                    for existing in all_results:
                        if existing.topic == result.topic:
                            existing.score = max(existing.score, result.score) * 1.1
                            break

        all_results.sort(key=lambda r: r.score, reverse=True)
        return all_results[:max_results]

    def merge_hybrid_results(self, hybrid: Dict[str, Any],
                             max_results: int = 20) -> List[Dict[str, Any]]:
        """Merge hybrid search results into a unified ranked list."""
        unified: List[Dict[str, Any]] = []

        for dr in hybrid.get("doctrine_results", []):
            dr["result_type"] = "doctrine"
            unified.append(dr)

        for sr in hybrid.get("statute_results", []):
            sr["result_type"] = "statute"
            sr["content"] = sr.get("full", "")
            unified.append(sr)

        for cr in hybrid.get("case_results", []):
            cr["result_type"] = "case"
            cr["content"] = cr.get("holding", "")
            unified.append(cr)

        unified.sort(key=lambda r: r.get("score", 0), reverse=True)
        return unified[:max_results]


# ============================================================================
# MODULE-LEVEL CONVENIENCE FUNCTIONS
# ============================================================================

_search_index: Optional[DoctrineSearchIndex] = None
_hybrid_engine: Optional[HybridSearchEngine] = None


def get_search_index() -> DoctrineSearchIndex:
    """Get or create the global search index."""
    global _search_index
    if _search_index is None:
        _search_index = DoctrineSearchIndex()
    return _search_index


def get_hybrid_engine() -> HybridSearchEngine:
    """Get or create the global hybrid search engine."""
    global _hybrid_engine
    if _hybrid_engine is None:
        _hybrid_engine = HybridSearchEngine(get_search_index())
    return _hybrid_engine


def search_doctrines(query: str, max_results: int = 20,
                     category_filter: Optional[str] = None) -> List[SearchResult]:
    """Search doctrines using the global index."""
    return get_search_index().search(query, max_results=max_results, category_filter=category_filter)


def hybrid_search(query: str, max_results: int = 20) -> Dict[str, Any]:
    """Perform hybrid search using the global engine."""
    return get_hybrid_engine().search(query, max_results=max_results)
