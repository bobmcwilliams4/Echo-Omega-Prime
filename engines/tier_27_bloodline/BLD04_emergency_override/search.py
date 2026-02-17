import math
import re
import threading
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional


class SearchDocument:
    def __init__(self, doc_id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = doc_id
        self.title = title
        self.content = content
        self.tags = tags
        self.weight = weight


class SearchResult:
    def __init__(self, doc_id: str, score: float, title: str, snippet: str):
        self.doc_id = doc_id
        self.score = score
        self.title = title
        self.snippet = snippet


class SearchIndex:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_term_freqs: Dict[str, Counter] = {}
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.N = 0  # total number of documents
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                # Remove old document stats
                old_tf = self.doc_term_freqs[doc.id]
                for term in old_tf:
                    self.term_doc_freqs[term] -= 1
                    if self.term_doc_freqs[term] <= 0:
                        del self.term_doc_freqs[term]
                del self.doc_term_freqs[doc.id]
                del self.doc_lengths[doc.id]
                self.N -= 1

            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            tf = Counter(tokens)
            self.doc_term_freqs[doc.id] = tf
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = sum(tf.values())
            for term in tf:
                self.term_doc_freqs[term] += 1
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []

        # Compute IDF for query terms
        idf = {term: self._compute_idf(term) for term in query_terms}

        scores: Dict[str, float] = defaultdict(float)

        for term in query_terms:
            if term not in self.term_doc_freqs:
                continue
            for doc_id, tf in self.doc_term_freqs.items():
                if term not in tf:
                    continue
                score = self._score_bm25(tf[term], idf[term], self.doc_lengths[doc_id])
                scores[doc_id] += score

        # Adjust scores by document weight
        for doc_id in scores:
            scores[doc_id] *= self.documents[doc_id].weight

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]

        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "total_documents": self.N,
                "average_document_length": self.avg_doc_length,
                "unique_terms": len(self.term_doc_freqs),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, tf: int, idf: float, doc_len: int) -> float:
        norm_tf = tf
        denom = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length) if self.avg_doc_length > 0 else tf + self.k1
        score = idf * (norm_tf * (self.k1 + 1)) / denom if denom > 0 else 0.0
        return score

    def _make_snippet(self, content: str, query_terms: List[str], snippet_length: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            pos = content_lower.find(term)
            if pos >= 0:
                positions.append(pos)
        if not positions:
            snippet = content[:snippet_length]
            if len(content) > snippet_length:
                snippet += "..."
            return snippet

        start = max(min(positions) - snippet_length // 4, 0)
        end = start + snippet_length
        snippet = content[start:end]
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet += "..."
        return snippet


_singleton_instance: Optional[SearchIndex] = None
_singleton_lock = threading.Lock()


def get_search_index() -> SearchIndex:
    global _singleton_instance
    with _singleton_lock:
        if _singleton_instance is None:
            _singleton_instance = SearchIndex()
            _seed_documents(_singleton_instance)
        return _singleton_instance


def _seed_documents(index: SearchIndex):
    # Pre-seed with 25+ domain documents matching BLD04_emergency_override doctrine topics
    docs = [
        SearchDocument(
            "doc001",
            "Sovereign Override Authority Overview",
            "The sovereign override authority grants the highest level of control to authorized personnel during emergency situations, enabling immediate suspension of standard protocols.",
            ["sovereign_override_authority", "emergency", "authority"],
            1.2,
        ),
        SearchDocument(
            "doc002",
            "Emergency Override Triggers",
            "Emergency override triggers include system failures, security breaches, and critical infrastructure threats that necessitate immediate intervention.",
            ["emergency_override_triggers", "triggers", "security"],
            1.1,
        ),
        SearchDocument(
            "doc003",
            "Break Glass Procedures",
            "Break glass procedures define the steps to be taken when conventional access is denied, allowing emergency access under strict audit and control.",
            ["break_glass_procedures", "access", "emergency"],
            1.3,
        ),
        SearchDocument(
            "doc004",
            "Insufficient Data for Drift Analysis",
            "When data is insufficient for drift analysis, emergency override protocols must be carefully evaluated to avoid false positives or negatives.",
            ["insufficient_data", "drift_analysis", "emergency_override"],
            1.0,
        ),
        SearchDocument(
            "doc005",
            "Authorization Levels for Sovereign Override",
            "Authorization levels define who can initiate sovereign override, including chain of command and verification processes.",
            ["sovereign_override_authority", "authorization", "levels"],
            1.15,
        ),
        SearchDocument(
            "doc006",
            "System Failure Emergency Override",
            "In the event of system failure, emergency override mechanisms allow manual control to restore critical operations.",
            ["emergency_override_triggers", "system_failure", "manual_control"],
            1.1,
        ),
        SearchDocument(
            "doc007",
            "Security Breach Response Procedures",
            "Security breach response includes immediate activation of emergency override to isolate affected systems and prevent spread.",
            ["emergency_override_triggers", "security_breach", "response"],
            1.25,
        ),
        SearchDocument(
            "doc008",
            "Audit Trails for Break Glass Access",
            "All break glass access events must be logged with detailed audit trails to ensure accountability and traceability.",
            ["break_glass_procedures", "audit", "accountability"],
            1.2,
        ),
        SearchDocument(
            "doc009",
            "Emergency Override Activation Criteria",
            "Clear criteria must be established for when emergency override can be activated to prevent misuse or accidental triggers.",
            ["emergency_override_triggers", "activation", "criteria"],
            1.1,
        ),
        SearchDocument(
            "doc010",
            "Data Requirements for Drift Analysis",
            "Adequate data collection is essential for reliable drift analysis; insufficient data may trigger emergency override protocols.",
            ["insufficient_data", "drift_analysis", "data_requirements"],
            1.0,
        ),
        SearchDocument(
            "doc011",
            "Sovereign Override Policy Compliance",
            "All actions under sovereign override must comply with established policies and legal frameworks to maintain legitimacy.",
            ["sovereign_override_authority", "policy", "compliance"],
            1.2,
        ),
        SearchDocument(
            "doc012",
            "Emergency Override Communication Protocols",
            "Communication protocols ensure that all relevant parties are informed promptly when emergency override is enacted.",
            ["emergency_override_triggers", "communication", "protocols"],
            1.1,
        ),
        SearchDocument(
            "doc013",
            "Break Glass Access Request Workflow",
            "The workflow for requesting break glass access involves multi-factor authentication and supervisory approval.",
            ["break_glass_procedures", "workflow", "access_request"],
            1.3,
        ),
        SearchDocument(
            "doc014",
            "Handling Insufficient Data in Emergency Scenarios",
            "Procedures for handling insufficient data during emergencies include fallback mechanisms and manual overrides.",
            ["insufficient_data", "emergency", "fallback"],
            1.05,
        ),
        SearchDocument(
            "doc015",
            "Sovereign Override Revocation Process",
            "The revocation process outlines how and when sovereign override authority is rescinded after emergency resolution.",
            ["sovereign_override_authority", "revocation", "process"],
            1.1,
        ),
        SearchDocument(
            "doc016",
            "Emergency Override System Architecture",
            "The system architecture supports rapid activation and secure management of emergency override functions.",
            ["emergency_override_triggers", "system_architecture", "security"],
            1.15,
        ),
        SearchDocument(
            "doc017",
            "Break Glass Access Security Controls",
            "Security controls for break glass access include encryption, monitoring, and real-time alerts.",
            ["break_glass_procedures", "security_controls", "monitoring"],
            1.25,
        ),
        SearchDocument(
            "doc018",
            "Data Drift Detection Limitations",
            "Limitations in data drift detection can lead to false alarms, necessitating emergency override safeguards.",
            ["insufficient_data", "drift_analysis", "limitations"],
            1.0,
        ),
        SearchDocument(
            "doc019",
            "Sovereign Override Training Requirements",
            "Personnel authorized for sovereign override must undergo specialized training and certification.",
            ["sovereign_override_authority", "training", "certification"],
            1.2,
        ),
        SearchDocument(
            "doc020",
            "Emergency Override Logging and Reporting",
            "All emergency override activities must be logged and reported for post-event analysis and compliance.",
            ["emergency_override_triggers", "logging", "reporting"],
            1.15,
        ),
        SearchDocument(
            "doc021",
            "Break Glass Access Incident Response",
            "Incident response plans must include procedures for break glass access misuse or abuse.",
            ["break_glass_procedures", "incident_response", "misuse"],
            1.3,
        ),
        SearchDocument(
            "doc022",
            "Mitigating Insufficient Data Risks",
            "Strategies to mitigate risks from insufficient data include enhanced monitoring and conservative override thresholds.",
            ["insufficient_data", "risk_mitigation", "monitoring"],
            1.05,
        ),
        SearchDocument(
            "doc023",
            "Sovereign Override Legal Considerations",
            "Legal considerations include jurisdiction, liability, and compliance with international regulations.",
            ["sovereign_override_authority", "legal", "compliance"],
            1.2,
        ),
        SearchDocument(
            "doc024",
            "Emergency Override Testing and Drills",
            "Regular testing and drills ensure readiness and effectiveness of emergency override procedures.",
            ["emergency_override_triggers", "testing", "drills"],
            1.1,
        ),
        SearchDocument(
            "doc025",
            "Break Glass Access User Accountability",
            "User accountability is enforced through identity verification and activity monitoring during break glass access.",
            ["break_glass_procedures", "accountability", "identity_verification"],
            1.3,
        ),
        SearchDocument(
            "doc026",
            "Data Quality Impact on Drift Analysis",
            "Poor data quality can severely impact drift analysis accuracy, increasing reliance on emergency override.",
            ["insufficient_data", "data_quality", "drift_analysis"],
            1.0,
        ),
        SearchDocument(
            "doc027",
            "Sovereign Override Escalation Procedures",
            "Escalation procedures define the chain of command and communication during sovereign override activation.",
            ["sovereign_override_authority", "escalation", "procedures"],
            1.15,
        ),
        SearchDocument(
            "doc028",
            "Emergency Override Fail-Safe Mechanisms",
            "Fail-safe mechanisms prevent catastrophic failures during emergency override activation.",
            ["emergency_override_triggers", "fail_safe", "mechanisms"],
            1.2,
        ),
        SearchDocument(
            "doc029",
            "Break Glass Access Policy Review",
            "Periodic policy reviews ensure break glass procedures remain effective and compliant with evolving standards.",
            ["break_glass_procedures", "policy", "review"],
            1.25,
        ),
        SearchDocument(
            "doc030",
            "Handling Ambiguous Data in Emergency Overrides",
            "Ambiguous data requires cautious interpretation and may delay emergency override activation pending further analysis.",
            ["insufficient_data", "ambiguous_data", "emergency_override"],
            1.05,
        ),
    ]

    for doc in docs:
        index.add_document(doc)