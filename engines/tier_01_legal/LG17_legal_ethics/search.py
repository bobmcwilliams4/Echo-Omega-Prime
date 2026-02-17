"""
LG17 Legal Ethics Engine - Search Module
==========================================
TF-IDF inverted index search over legal ethics doctrine blocks,
plus domain-specific analyzers for conflict screening, malpractice risk,
disciplinary action assessment, and privilege analysis workflows.

Components:
    - DoctrineSearchIndex: TF-IDF inverted index with BM25 scoring
    - SearchResult: Ranked result with score, snippet, provenance
    - EthicsRuleSearcher: Model Rule lookup and cross-reference
    - ConflictScreener: Multi-party conflict screening workflow
    - MalpracticeRiskAssessor: Malpractice exposure analysis
    - DisciplinaryActionSearcher: Sanction precedent lookup

Port: 8407
Engine: LG17 Legal Ethics
Version: 2.0.0
"""

from __future__ import annotations

import hashlib
import math
import re
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, ClassVar, Dict, FrozenSet, List, Optional, Set, Tuple

from loguru import logger


# ============================================================================
# SEARCH RESULT
# ============================================================================

@dataclass
class SearchResult:
    """A single search result from the doctrine index."""
    topic: str
    category: str
    score: float
    snippet: str
    authority: str = ""
    rule_reference: str = ""
    restatement_reference: str = ""
    jurisdiction: str = ""
    relevance_explanation: str = ""
    block_hash: str = ""
    result_hash: str = ""

    def __post_init__(self) -> None:
        if not self.result_hash:
            content = f"{self.topic}|{self.score}|{self.snippet[:100]}"
            self.result_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


# ============================================================================
# INVERTED INDEX (TF-IDF + BM25)
# ============================================================================

class DoctrineSearchIndex:
    """TF-IDF inverted index with BM25 scoring over doctrine blocks."""

    BM25_K1: ClassVar[float] = 1.5
    BM25_B: ClassVar[float] = 0.75

    def __init__(self) -> None:
        self._index: Dict[str, Dict[str, float]] = defaultdict(dict)
        self._doc_lengths: Dict[str, int] = {}
        self._doc_metadata: Dict[str, Dict[str, Any]] = {}
        self._doc_content: Dict[str, str] = {}
        self._total_docs: int = 0
        self._avg_doc_length: float = 0.0
        self._df: Counter = Counter()
        self._built: bool = False

    def add_document(
        self,
        doc_id: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a document to the index."""
        tokens = self._tokenize(content)
        self._doc_lengths[doc_id] = len(tokens)
        self._doc_content[doc_id] = content
        self._doc_metadata[doc_id] = metadata or {}
        tf: Counter = Counter(tokens)
        unique_terms: Set[str] = set()
        for term, count in tf.items():
            self._index[term][doc_id] = count / max(len(tokens), 1)
            unique_terms.add(term)
        for term in unique_terms:
            self._df[term] += 1
        self._total_docs += 1
        self._built = False

    def build(self) -> None:
        """Finalize index by computing average doc length."""
        if self._total_docs > 0:
            self._avg_doc_length = sum(self._doc_lengths.values()) / self._total_docs
        else:
            self._avg_doc_length = 1.0
        self._built = True
        logger.info(
            f"DoctrineSearchIndex built: {self._total_docs} docs, "
            f"{len(self._index)} unique terms"
        )

    def search(
        self,
        query: str,
        top_k: int = 20,
        min_score: float = 0.01,
    ) -> List[SearchResult]:
        """Search the index using BM25."""
        if not self._built:
            self.build()
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        scores: Dict[str, float] = defaultdict(float)
        for token in query_tokens:
            if token not in self._index:
                continue
            df = self._df.get(token, 0)
            idf = math.log((self._total_docs - df + 0.5) / (df + 0.5) + 1.0)
            for doc_id, tf in self._index[token].items():
                doc_len = self._doc_lengths.get(doc_id, 1)
                raw_tf = tf * doc_len
                numerator = raw_tf * (self.BM25_K1 + 1)
                denominator = raw_tf + self.BM25_K1 * (
                    1 - self.BM25_B + self.BM25_B * doc_len / max(self._avg_doc_length, 1)
                )
                scores[doc_id] += idf * (numerator / max(denominator, 0.001))
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results: List[SearchResult] = []
        for doc_id, score in ranked[:top_k]:
            if score < min_score:
                break
            meta = self._doc_metadata.get(doc_id, {})
            content = self._doc_content.get(doc_id, "")
            snippet = self._extract_snippet(content, query_tokens)
            results.append(
                SearchResult(
                    topic=meta.get("topic", doc_id),
                    category=meta.get("category", ""),
                    score=round(score, 4),
                    snippet=snippet,
                    authority=meta.get("authority", ""),
                    rule_reference=meta.get("rule_reference", ""),
                    restatement_reference=meta.get("restatement_reference", ""),
                    jurisdiction=meta.get("jurisdiction", ""),
                    relevance_explanation=meta.get("relevance_explanation", ""),
                    block_hash=meta.get("block_hash", ""),
                )
            )
        return results

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text for indexing."""
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s\.\-]", " ", text)
        tokens = text.split()
        stopwords = frozenset([
            "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "shall", "can", "to", "of", "in", "for",
            "on", "with", "at", "by", "from", "as", "into", "through", "during",
            "before", "after", "above", "below", "between", "under", "again",
            "further", "then", "once", "here", "there", "when", "where", "why",
            "how", "all", "each", "every", "both", "few", "more", "most", "other",
            "some", "such", "no", "nor", "not", "only", "own", "same", "so",
            "than", "too", "very", "just", "about", "it", "its", "this", "that",
            "these", "those", "and", "but", "or", "if", "while", "because",
        ])
        return [t for t in tokens if t not in stopwords and len(t) > 1]

    def _extract_snippet(self, content: str, query_tokens: List[str], max_len: int = 300) -> str:
        """Extract a relevant snippet from content."""
        lower_content = content.lower()
        best_pos = 0
        best_score = 0
        window = 200
        for i in range(0, len(lower_content) - window + 1, 50):
            chunk = lower_content[i : i + window]
            score = sum(1 for t in query_tokens if t in chunk)
            if score > best_score:
                best_score = score
                best_pos = i
        start = max(0, best_pos - 50)
        end = min(len(content), best_pos + max_len)
        snippet = content[start:end].strip()
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."
        return snippet

    @property
    def total_documents(self) -> int:
        """Return total indexed documents."""
        return self._total_docs

    @property
    def total_terms(self) -> int:
        """Return total unique terms."""
        return len(self._index)


# ============================================================================
# ETHICS RULE SEARCHER
# ============================================================================

class EthicsRuleSearcher:
    """Search and cross-reference ABA Model Rules and related ethics sources."""

    RULE_HIERARCHY: Dict[str, List[str]] = {
        "client_lawyer_relationship": [
            "1.0", "1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7",
            "1.8", "1.9", "1.10", "1.11", "1.12", "1.13", "1.14",
            "1.15", "1.16", "1.17", "1.18",
        ],
        "counselor": ["2.1", "2.2", "2.3", "2.4"],
        "advocate": ["3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8", "3.9"],
        "transactions_with_others": ["4.1", "4.2", "4.3", "4.4"],
        "law_firms_and_associations": ["5.1", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7"],
        "public_service": ["6.1", "6.2", "6.3", "6.4", "6.5"],
        "information_about_services": ["7.1", "7.2", "7.3", "7.4", "7.5", "7.6"],
        "maintaining_integrity": ["8.1", "8.2", "8.3", "8.4", "8.5"],
    }

    RULE_TITLES: Dict[str, str] = {
        "1.0": "Terminology",
        "1.1": "Competence",
        "1.2": "Scope of Representation & Authority",
        "1.3": "Diligence",
        "1.4": "Communication",
        "1.5": "Fees",
        "1.6": "Confidentiality of Information",
        "1.7": "Conflict of Interest: Current Clients",
        "1.8": "Conflict of Interest: Current Clients - Specific Rules",
        "1.9": "Duties to Former Clients",
        "1.10": "Imputation of Conflicts of Interest",
        "1.11": "Special Conflicts: Government Officers & Employees",
        "1.12": "Former Judge, Arbitrator, Mediator, or Other Third-Party Neutral",
        "1.13": "Organization as Client",
        "1.14": "Client with Diminished Capacity",
        "1.15": "Safekeeping Property",
        "1.16": "Declining or Terminating Representation",
        "1.17": "Sale of Law Practice",
        "1.18": "Duties to Prospective Client",
        "2.1": "Advisor",
        "2.3": "Evaluation for Use by Third Persons",
        "2.4": "Lawyer Serving as Third-Party Neutral",
        "3.1": "Meritorious Claims and Contentions",
        "3.3": "Candor Toward the Tribunal",
        "3.4": "Fairness to Opposing Party and Counsel",
        "3.5": "Impartiality and Decorum of the Tribunal",
        "3.6": "Trial Publicity",
        "3.7": "Lawyer as Witness",
        "3.8": "Special Responsibilities of a Prosecutor",
        "4.1": "Truthfulness in Statements to Others",
        "4.2": "Communication with Person Represented by Counsel",
        "4.3": "Dealing with Unrepresented Person",
        "4.4": "Respect for Rights of Third Persons",
        "5.1": "Responsibilities of Partners, Managers, and Supervisory Lawyers",
        "5.3": "Responsibilities Regarding Nonlawyer Assistance",
        "5.4": "Professional Independence of a Lawyer",
        "5.5": "Unauthorized Practice of Law; Multijurisdictional Practice",
        "7.1": "Communications Concerning a Lawyer's Services",
        "7.2": "Advertising",
        "7.3": "Solicitation of Clients",
        "8.1": "Bar Admission and Disciplinary Matters",
        "8.3": "Reporting Professional Misconduct",
        "8.4": "Misconduct",
        "8.5": "Disciplinary Authority; Choice of Law",
    }

    def get_rule_title(self, rule_number: str) -> str:
        """Get the title of a Model Rule."""
        return self.RULE_TITLES.get(rule_number, f"Model Rule {rule_number}")

    def get_category_for_rule(self, rule_number: str) -> str:
        """Get the category a rule belongs to."""
        for category, rules in self.RULE_HIERARCHY.items():
            if rule_number in rules:
                return category
        return "unknown"

    def get_related_rules(self, rule_number: str) -> List[str]:
        """Get related rules in the same category."""
        category = self.get_category_for_rule(rule_number)
        if category == "unknown":
            return []
        return [
            r for r in self.RULE_HIERARCHY.get(category, []) if r != rule_number
        ]

    def search_by_keyword(self, keyword: str) -> List[Dict[str, str]]:
        """Search rules by keyword in title."""
        keyword_lower = keyword.lower()
        results: List[Dict[str, str]] = []
        for rule_num, title in self.RULE_TITLES.items():
            if keyword_lower in title.lower():
                results.append({
                    "rule": rule_num,
                    "title": title,
                    "category": self.get_category_for_rule(rule_num),
                })
        return results


# ============================================================================
# CONFLICT SCREENER
# ============================================================================

@dataclass
class ConflictScreenResult:
    """Result of a multi-party conflict screening."""
    conflicts_found: int
    total_pairs_checked: int
    conflicts: List[Dict[str, Any]] = dc_field(default_factory=list)
    clear_pairs: List[Dict[str, str]] = dc_field(default_factory=list)
    screening_hash: str = ""
    duration_ms: float = 0.0

    def __post_init__(self) -> None:
        if not self.screening_hash:
            content = f"{self.conflicts_found}|{self.total_pairs_checked}"
            self.screening_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


class ConflictScreener:
    """Multi-party conflict screening workflow."""

    def screen_parties(
        self,
        client_name: str,
        adverse_parties: List[str],
        related_entities: Optional[List[str]] = None,
        matter_description: str = "",
        prior_clients: Optional[List[str]] = None,
    ) -> ConflictScreenResult:
        """Screen multiple parties for conflicts against a client."""
        start = time.time()
        all_parties = adverse_parties + (related_entities or [])
        prior = [p.lower() for p in (prior_clients or [])]
        client_lower = client_name.lower()
        conflicts: List[Dict[str, Any]] = []
        clear: List[Dict[str, str]] = []
        pairs_checked = 0

        for party in all_parties:
            pairs_checked += 1
            party_lower = party.lower()

            # Check if party is a current client
            if party_lower == client_lower:
                conflicts.append({
                    "party": party,
                    "conflict_type": "identity",
                    "rule": "N/A",
                    "description": "Party is the same as the client",
                })
                continue

            # Check if party is a prior client
            if party_lower in prior:
                conflicts.append({
                    "party": party,
                    "conflict_type": "successive",
                    "rule": "Model Rule 1.9",
                    "description": f"'{party}' is a former client. Apply substantially related test.",
                })
                continue

            # Check matter description for adversity indicators
            if party_lower in matter_description.lower():
                conflicts.append({
                    "party": party,
                    "conflict_type": "concurrent",
                    "rule": "Model Rule 1.7",
                    "description": f"'{party}' appears in the matter description. Potential concurrent conflict.",
                })
                continue

            clear.append({"party": party, "status": "no_conflict_detected"})

        duration = (time.time() - start) * 1000
        return ConflictScreenResult(
            conflicts_found=len(conflicts),
            total_pairs_checked=pairs_checked,
            conflicts=conflicts,
            clear_pairs=clear,
            duration_ms=round(duration, 3),
        )


# ============================================================================
# MALPRACTICE RISK ASSESSOR
# ============================================================================

class MalpracticeRiskLevel(str, Enum):
    """Malpractice risk levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    MINIMAL = "minimal"


@dataclass
class MalpracticeRiskResult:
    """Result of a malpractice risk assessment."""
    risk_level: MalpracticeRiskLevel
    risk_score: float
    risk_factors: List[Dict[str, Any]] = dc_field(default_factory=list)
    mitigation_steps: List[str] = dc_field(default_factory=list)
    insurance_considerations: str = ""
    analysis: str = ""


class MalpracticeRiskAssessor:
    """Assess malpractice exposure for a representation."""

    RISK_INDICATORS: Dict[str, float] = {
        "statute of limitations": 0.9,
        "deadline": 0.8,
        "filing deadline": 0.9,
        "discovery deadline": 0.7,
        "no engagement letter": 0.8,
        "no fee agreement": 0.7,
        "unfamiliar area of law": 0.7,
        "complex transaction": 0.6,
        "high stakes": 0.6,
        "multiple parties": 0.5,
        "conflict of interest": 0.8,
        "inadequate communication": 0.6,
        "no malpractice insurance": 0.9,
        "missed deadline": 1.0,
        "trust account": 0.8,
        "client funds": 0.7,
    }

    def assess(
        self,
        matter_description: str,
        risk_factors: Optional[List[str]] = None,
        has_engagement_letter: bool = True,
        has_malpractice_insurance: bool = True,
        lawyer_experience_years: int = 10,
    ) -> MalpracticeRiskResult:
        """Assess malpractice risk for a matter."""
        lower_desc = matter_description.lower()
        detected_factors: List[Dict[str, Any]] = []
        total_risk = 0.0

        # Check known indicators against description
        for indicator, weight in self.RISK_INDICATORS.items():
            if indicator in lower_desc:
                detected_factors.append({
                    "factor": indicator,
                    "weight": weight,
                    "source": "matter_description",
                })
                total_risk += weight

        # Add explicit risk factors
        for factor in (risk_factors or []):
            factor_lower = factor.lower()
            weight = self.RISK_INDICATORS.get(factor_lower, 0.5)
            detected_factors.append({
                "factor": factor,
                "weight": weight,
                "source": "explicit",
            })
            total_risk += weight

        # Engagement letter check
        if not has_engagement_letter:
            detected_factors.append({
                "factor": "no_engagement_letter",
                "weight": 0.8,
                "source": "assessment_input",
            })
            total_risk += 0.8

        # Insurance check
        if not has_malpractice_insurance:
            detected_factors.append({
                "factor": "no_malpractice_insurance",
                "weight": 0.9,
                "source": "assessment_input",
            })
            total_risk += 0.9

        # Experience adjustment
        if lawyer_experience_years < 3:
            total_risk += 0.3
            detected_factors.append({
                "factor": "limited_experience",
                "weight": 0.3,
                "source": "experience_level",
            })

        # Normalize score
        risk_score = min(1.0, total_risk / max(len(detected_factors), 1))

        # Determine risk level
        if risk_score >= 0.8:
            level = MalpracticeRiskLevel.CRITICAL
        elif risk_score >= 0.6:
            level = MalpracticeRiskLevel.HIGH
        elif risk_score >= 0.4:
            level = MalpracticeRiskLevel.MODERATE
        elif risk_score >= 0.2:
            level = MalpracticeRiskLevel.LOW
        else:
            level = MalpracticeRiskLevel.MINIMAL

        mitigation = self._build_mitigation(detected_factors, has_engagement_letter, has_malpractice_insurance)

        return MalpracticeRiskResult(
            risk_level=level,
            risk_score=round(risk_score, 3),
            risk_factors=detected_factors,
            mitigation_steps=mitigation,
            insurance_considerations=(
                "Ensure malpractice insurance coverage is adequate for the matter type and amounts at stake."
                if has_malpractice_insurance
                else "CRITICAL: Obtain malpractice insurance immediately. Many jurisdictions require disclosure of uninsured status."
            ),
            analysis=(
                f"Malpractice risk level: {level.value}. Score: {risk_score:.3f}. "
                f"{len(detected_factors)} risk factors identified."
            ),
        )

    def _build_mitigation(
        self,
        factors: List[Dict[str, Any]],
        has_letter: bool,
        has_insurance: bool,
    ) -> List[str]:
        """Build mitigation recommendations."""
        steps: List[str] = []
        if not has_letter:
            steps.append("Execute an engagement letter defining the scope, fees, and limitations of the representation")
        if not has_insurance:
            steps.append("Obtain professional liability insurance before commencing the representation")
        factor_names = {f["factor"] for f in factors}
        if "deadline" in factor_names or "statute of limitations" in factor_names or "filing deadline" in factor_names:
            steps.append("Implement calendaring and docketing systems with backup reminders")
        if "conflict of interest" in factor_names:
            steps.append("Run a comprehensive conflicts check and document the analysis")
        if "trust account" in factor_names or "client funds" in factor_names:
            steps.append("Ensure IOLTA/trust account procedures are properly documented and reconciled monthly")
        if "unfamiliar area of law" in factor_names:
            steps.append("Associate with experienced counsel in the practice area or obtain specialized CLE")
        steps.append("Maintain detailed file notes documenting all client communications and key decisions")
        steps.append("Send periodic status updates to the client and document all communications")
        return steps


# ============================================================================
# DISCIPLINARY ACTION SEARCHER
# ============================================================================

class DisciplinaryActionSearcher:
    """Search disciplinary action precedents by violation type."""

    SANCTION_PRECEDENTS: Dict[str, Dict[str, Any]] = {
        "conversion_of_client_funds": {
            "typical_sanction": "disbarment",
            "aba_standard": "4.11",
            "description": "Intentional or knowing conversion of client property. Disbarment is the presumptive sanction.",
            "leading_case": "In re Crandall, 832 A.2d 756 (D.C. 2003)",
            "aggravating_factors": ["pattern of misconduct", "amount converted", "vulnerability of victim"],
        },
        "commingling": {
            "typical_sanction": "suspension",
            "aba_standard": "4.12",
            "description": "Commingling personal and client funds without conversion. Suspension is typical; inadvertent commingling may result in reprimand.",
            "leading_case": "In re Wilson, 409 A.2d 1153 (N.J. 1979)",
            "aggravating_factors": ["pattern", "duration", "amount involved"],
        },
        "neglect": {
            "typical_sanction": "suspension",
            "aba_standard": "4.42",
            "description": "Pattern of neglect causing injury to clients. Single incidents may warrant reprimand; chronic neglect warrants suspension or disbarment.",
            "leading_case": "In re Hawkins, 109 A.3d 1142 (D.C. 2015)",
            "aggravating_factors": ["multiple clients affected", "duration of neglect", "harm caused"],
        },
        "conflict_of_interest": {
            "typical_sanction": "suspension",
            "aba_standard": "4.32",
            "description": "Engaging in dual representation without informed consent or when not consentable. Severity depends on harm caused.",
            "leading_case": "Fiandaca v. Cunningham, 827 F.2d 825 (1st Cir. 1987)",
            "aggravating_factors": ["knowing violation", "harm to client", "personal benefit"],
        },
        "dishonesty_fraud": {
            "typical_sanction": "disbarment",
            "aba_standard": "5.11",
            "description": "Intentional dishonesty, fraud, deceit, or misrepresentation. Often results in disbarment if intentional.",
            "leading_case": "In re Bonet, 29 P.3d 1242 (Wash. 2001)",
            "aggravating_factors": ["intentional", "client harm", "multiple instances"],
        },
        "failure_to_communicate": {
            "typical_sanction": "reprimand",
            "aba_standard": "4.42",
            "description": "Failure to keep client informed or respond to requests. Typically results in reprimand for isolated instances; suspension for patterns.",
            "leading_case": "State disciplinary proceedings (varies by jurisdiction)",
            "aggravating_factors": ["multiple clients", "critical communications missed"],
        },
        "unauthorized_practice": {
            "typical_sanction": "suspension",
            "aba_standard": "7.0",
            "description": "Practicing law without a license or in an unauthorized jurisdiction. May also result in fee forfeiture and criminal prosecution.",
            "leading_case": "Birbrower v. Superior Court, 17 Cal.4th 119 (1998)",
            "aggravating_factors": ["knowing violation", "harm to client", "fees collected"],
        },
        "incompetence": {
            "typical_sanction": "suspension",
            "aba_standard": "4.52",
            "description": "Repeated failure to provide competent representation. Pattern incompetence warrants suspension; single isolated instance may result in reprimand with CLE requirement.",
            "leading_case": "In re Inglimo, 740 N.W.2d 125 (Wis. 2007)",
            "aggravating_factors": ["repeated failures", "areas outside expertise", "client harm"],
        },
    }

    def search_precedents(self, violation_type: str) -> Optional[Dict[str, Any]]:
        """Search for disciplinary precedents by violation type."""
        key = violation_type.lower().replace(" ", "_").replace("-", "_")
        return self.SANCTION_PRECEDENTS.get(key)

    def get_all_violation_types(self) -> List[str]:
        """Get all known violation types."""
        return list(self.SANCTION_PRECEDENTS.keys())

    def get_sanction_for_violation(self, violation_type: str) -> str:
        """Get the typical sanction for a violation type."""
        precedent = self.search_precedents(violation_type)
        if precedent:
            return precedent["typical_sanction"]
        return "varies_by_jurisdiction"

    def analyze_sanction_factors(
        self,
        violation_type: str,
        mental_state: str = "knowing",
        injury_level: str = "moderate",
        prior_discipline: bool = False,
        cooperative: bool = True,
    ) -> Dict[str, Any]:
        """Analyze sanction factors under ABA Standards."""
        precedent = self.search_precedents(violation_type) or {
            "typical_sanction": "unknown",
            "description": "Violation type not in precedent database",
        }

        # Apply ABA Standards four-factor analysis
        aggravating: List[str] = []
        mitigating: List[str] = []

        if prior_discipline:
            aggravating.append("prior disciplinary offenses")
        if mental_state == "intentional":
            aggravating.append("dishonest or selfish motive")
        if injury_level in ("severe", "substantial"):
            aggravating.append("substantial experience in the practice of law")

        if not prior_discipline:
            mitigating.append("absence of prior disciplinary record")
        if cooperative:
            mitigating.append("cooperative attitude toward proceedings")
        if mental_state == "negligent":
            mitigating.append("negligent mental state (less culpable)")

        # Determine recommended sanction
        base = precedent.get("typical_sanction", "reprimand")
        if len(aggravating) > len(mitigating) and mental_state == "intentional":
            recommended = "disbarment" if base in ("disbarment", "suspension") else "suspension"
        elif len(mitigating) > len(aggravating) and mental_state == "negligent":
            recommended = "reprimand" if base in ("suspension", "reprimand") else base
        else:
            recommended = base

        return {
            "violation_type": violation_type,
            "base_sanction": base,
            "recommended_sanction": recommended,
            "mental_state": mental_state,
            "injury_level": injury_level,
            "aggravating_factors": aggravating,
            "mitigating_factors": mitigating,
            "precedent": precedent,
            "analysis": (
                f"Based on ABA Standards four-factor analysis, recommended sanction for "
                f"'{violation_type}' with {mental_state} mental state and {injury_level} "
                f"injury is: {recommended}. "
                f"Aggravating factors: {len(aggravating)}. Mitigating factors: {len(mitigating)}."
            ),
        }


# ============================================================================
# MODULE-LEVEL FUNCTIONS
# ============================================================================

def compute_query_hash(query: str) -> str:
    """Compute SHA-256 hash of a query string."""
    return hashlib.sha256(query.encode("utf-8")).hexdigest()[:16]


def build_search_index(doctrine_blocks: List[Any]) -> DoctrineSearchIndex:
    """Build a search index from doctrine blocks."""
    idx = DoctrineSearchIndex()
    for block in doctrine_blocks:
        content_parts = [
            block.topic,
            block.category,
            block.summary,
            block.analysis,
            block.authority,
            " ".join(block.keywords),
        ]
        if hasattr(block, "rule_reference") and block.rule_reference:
            content_parts.append(block.rule_reference)
        if hasattr(block, "sanctions") and block.sanctions:
            content_parts.append(block.sanctions)
        if hasattr(block, "texas_notes") and block.texas_notes:
            content_parts.append(block.texas_notes)
        content = " ".join(content_parts)
        metadata = block.to_dict()
        idx.add_document(doc_id=block.topic, content=content, metadata=metadata)
    idx.build()
    return idx
