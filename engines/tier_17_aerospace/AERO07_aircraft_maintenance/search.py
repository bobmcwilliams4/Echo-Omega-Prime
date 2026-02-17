import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

class SearchDocument:
    def __init__(self, doc_id: int, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = doc_id
        self.title = title
        self.content = content
        self.tags = tags
        self.weight = weight

class SearchResult:
    def __init__(self, doc_id: int, score: float, title: str, snippet: str):
        self.doc_id = doc_id
        self.score = score
        self.title = title
        self.snippet = snippet

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = defaultdict(dict)
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def _tokenize(self, text: str) -> List[str]:
        # Lowercase, remove punctuation, split by whitespace
        tokens = re.findall(r'\b[a-zA-Z0-9\-]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return  # Prevent duplicate
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.term_freqs[doc.id] = Counter(tokens)
            for term in set(tokens):
                self.term_doc_freq[term] += 1
            self.total_docs += 1
            self.avg_doc_length = (
                sum(self.doc_lengths.values()) / self.total_docs
                if self.total_docs > 0 else 0.0
            )
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        term_freqs = self.term_freqs[doc_id]
        for term in query_terms:
            tf = term_freqs.get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            numerator = tf * (self._bm25_k1 + 1)
            denominator = tf + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / self.avg_doc_length)
            score += idf * numerator / denominator
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        # Term frequency normalization: tf = freq / max_freq_in_doc
        term_freqs = self.term_freqs[doc_id]
        max_freq = max(term_freqs.values()) if term_freqs else 1
        score = 0.0
        for term in query_terms:
            tf = term_freqs.get(term, 0) / max_freq
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            score += tf * idf
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: List[Tuple[float, int]] = []
        for doc_id in self.documents:
            bm25_score = self._score_bm25(query_terms, doc_id)
            tfidf_score = self._score_tfidf(query_terms, doc_id)
            combined_score = bm25_score + 0.5 * tfidf_score
            if combined_score > 0:
                doc_scores.append((combined_score, doc_id))
        top_docs = heapq.nlargest(limit, doc_scores)
        results = []
        for score, doc_id in top_docs:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], max_length: int = 180) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = ' '.join(tokens[:max_length])
        else:
            start = max(positions[0] - 10, 0)
            end = min(start + max_length, len(tokens))
            snippet = ' '.join(tokens[start:end])
        # Highlight query terms
        for term in set(query_terms):
            snippet = re.sub(r'\b{}\b'.format(re.escape(term)), f'*{term}*', snippet, flags=re.IGNORECASE)
        return snippet

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
        }

# Singleton factory for search index
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_domain_documents(_search_index_instance)
        return _search_index_instance

def _seed_domain_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "MSG-3 Fundamentals for AERO07 Engine",
            "MSG-3 (Maintenance Steering Group-3) analysis is the foundation for developing maintenance programs for the AERO07 engine. It identifies failure modes, tasks, and intervals based on reliability and safety. The process involves functional failure analysis, task selection, and optimization for airworthiness.",
            ["MSG-3", "Maintenance", "AERO07", "Reliability"],
            1.0
        ),
        SearchDocument(
            2,
            "Airworthiness Directive (AD) Compliance for AERO07",
            "Airworthiness Directives (ADs) are mandatory requirements issued by aviation authorities. For AERO07, compliance involves tracking ADs, evaluating applicability, and documenting actions. Non-compliance can result in grounding and regulatory penalties.",
            ["AD", "Compliance", "AERO07", "Regulatory"],
            1.0
        ),
        SearchDocument(
            3,
            "Reliability-Centered Maintenance (RCM) for AERO07",
            "RCM methodology for AERO07 focuses on maximizing reliability and minimizing downtime. It uses data-driven analysis to select maintenance tasks, balancing preventive and corrective actions. Key steps include failure mode identification, risk assessment, and task optimization.",
            ["RCM", "Reliability", "AERO07", "Maintenance"],
            1.0
        ),
        SearchDocument(
            4,
            "Non-Destructive Testing (NDT) Methods for AERO07",
            "NDT methods such as ultrasonic, eddy current, magnetic particle, and dye penetrant are used for AERO07 engine inspection. Selection depends on material, geometry, and defect type. Qualification of NDT personnel is required under aviation standards.",
            ["NDT", "Inspection", "AERO07", "Qualification"],
            1.0
        ),
        SearchDocument(
            5,
            "Supplemental Structural Inspection Program (SSIP) for AERO07",
            "SSIP requirements for AERO07 address fatigue and structural integrity. The program defines inspection intervals, critical areas, and reporting procedures. Compliance ensures continued airworthiness and prevents catastrophic failures.",
            ["SSIP", "Structural", "AERO07", "Fatigue"],
            1.0
        ),
        SearchDocument(
            6,
            "Corrosion Prevention and Control Program (CPCP) Implementation",
            "CPCP for AERO07 involves regular inspections, corrosion removal, protective coatings, and environmental controls. Implementation reduces maintenance costs and extends engine life. Documentation and training are essential for effective CPCP.",
            ["CPCP", "Corrosion", "AERO07", "Prevention"],
            1.0
        ),
        SearchDocument(
            7,
            "Engine Health Monitoring (EHM) for AERO07",
            "EHM uses sensors and data analytics to monitor AERO07 engine parameters such as temperature, vibration, and oil quality. Condition trend analysis enables early detection of anomalies, predictive maintenance, and reduced unscheduled removals.",
            ["EHM", "Monitoring", "AERO07", "Analytics"],
            1.0
        ),
        SearchDocument(
            8,
            "FAR Part 145 Repair Station Certification",
            "FAR Part 145 outlines requirements for repair station certification, including facilities, personnel, quality systems, and recordkeeping. AERO07 maintenance must be performed by certified stations to ensure compliance and safety.",
            ["FAR 145", "Certification", "AERO07", "Repair"],
            1.0
        ),
        SearchDocument(
            9,
            "A-Check, B-Check, C-Check, D-Check Intervals for AERO07",
            "AERO07 maintenance checks are categorized as A, B, C, and D. A-Check is light, performed frequently; B-Check is intermediate; C-Check is comprehensive; D-Check is heavy and involves complete overhaul. Intervals are based on flight hours and cycles.",
            ["Checks", "Intervals", "AERO07", "Overhaul"],
            1.0
        ),
        SearchDocument(
            10,
            "Service Bulletin (SB) Compliance for AERO07",
            "Service Bulletins (SBs) provide technical updates and modifications. For AERO07, SBs may be mandatory or optional. Compliance ensures safety, reliability, and regulatory conformity. Documentation of SB status is required for audits.",
            ["SB", "Compliance", "AERO07", "Technical"],
            1.0
        ),
        SearchDocument(
            11,
            "Component Time-Between-Overhaul (TBO) and Life-Limited Parts",
            "AERO07 components have defined TBO and life limits. TBO is the maximum interval between overhauls; life-limited parts must be replaced at specified times. Tracking ensures safety and prevents failures.",
            ["TBO", "Life-Limited", "AERO07", "Components"],
            1.0
        ),
        SearchDocument(
            12,
            "ETOPS Maintenance Requirements for AERO07",
            "ETOPS (Extended-range Twin-engine Operational Performance Standards) requires enhanced maintenance for AERO07. Significant systems include engines, electrical, and fire protection. Procedures address reliability, redundancy, and rapid response.",
            ["ETOPS", "Maintenance", "AERO07", "Reliability"],
            1.0
        ),
        SearchDocument(
            13,
            "FAR Part 43 Maintenance Records and Return to Service",
            "FAR Part 43 mandates accurate maintenance records for AERO07. Requirements include description of work, date, technician signature, and return-to-service authorization. Proper recordkeeping supports compliance and traceability.",
            ["FAR 43", "Records", "AERO07", "Service"],
            1.0
        ),
        SearchDocument(
            14,
            "Minimum Equipment List (MEL) Dispatch Deviations",
            "MEL defines equipment required for safe dispatch of AERO07. Deviations and restrictions are documented, with procedures for repair and continued operation. MEL compliance is critical for regulatory approval.",
            ["MEL", "Dispatch", "AERO07", "Deviations"],
            1.0
        ),
        SearchDocument(
            15,
            "Progressive Maintenance Program for AERO07",
            "Progressive maintenance divides tasks into segments performed at shorter intervals. For AERO07, this reduces downtime and improves reliability. Program requirements include task scheduling, documentation, and quality assurance.",
            ["Progressive", "Maintenance", "AERO07", "Segmentation"],
            1.0
        ),
        SearchDocument(
            16,
            "Human Factors in AERO07 Maintenance",
            "Human factors address error prevention, training, and ergonomics in AERO07 maintenance. Strategies include fatigue management, communication, and safety culture. Reducing human error improves reliability and safety.",
            ["Human Factors", "AERO07", "Error Prevention", "Safety"],
            1.0
        ),
        SearchDocument(
            17,
            "AERO07 Engine Failure Modes and Effects Analysis (FMEA)",
            "FMEA identifies potential failure modes in AERO07 engine, assesses effects, and prioritizes corrective actions. The process supports MSG-3 and RCM methodologies, improving safety and reliability.",
            ["FMEA", "Failure Modes", "AERO07", "Safety"],
            1.0
        ),
        SearchDocument(
            18,
            "AERO07 Engine Oil System Maintenance",
            "Routine inspection and maintenance of the oil system in AERO07 includes checking oil levels, quality, and filter replacement. Oil analysis supports EHM and early detection of wear or contamination.",
            ["Oil System", "Maintenance", "AERO07", "EHM"],
            1.0
        ),
        SearchDocument(
            19,
            "AERO07 Engine Vibration Monitoring",
            "Vibration monitoring for AERO07 uses sensors and trend analysis to detect imbalance, bearing wear, and blade defects. Early intervention prevents catastrophic failures and supports predictive maintenance.",
            ["Vibration", "Monitoring", "AERO07", "Predictive"],
            1.0
        ),
        SearchDocument(
            20,
            "AERO07 Engine Fire Protection System",
            "Fire protection in AERO07 includes detection, suppression, and maintenance of fire extinguishing equipment. Compliance with ETOPS and regulatory standards is mandatory.",
            ["Fire Protection", "AERO07", "ETOPS", "Safety"],
            1.0
        ),
        SearchDocument(
            21,
            "AERO07 Engine Compressor Section Inspection",
            "Inspection of the compressor section in AERO07 uses NDT methods to detect cracks, corrosion, and wear. Scheduled inspections are part of C-Check and D-Check intervals.",
            ["Compressor", "Inspection", "AERO07", "NDT"],
            1.0
        ),
        SearchDocument(
            22,
            "AERO07 Engine Life-Limited Parts Management",
            "Tracking and managing life-limited parts for AERO07 is essential for airworthiness. Systems include electronic records, scheduled replacements, and compliance with ADs and SBs.",
            ["Life-Limited", "Parts", "AERO07", "Management"],
            1.0
        ),
        SearchDocument(
            23,
            "AERO07 Engine Overhaul Procedures",
            "Overhaul of AERO07 involves disassembly, inspection, repair, and reassembly. Procedures follow MSG-3, AD, and SB requirements. Quality assurance ensures reliability and compliance.",
            ["Overhaul", "Procedures", "AERO07", "Quality"],
            1.0
        ),
        SearchDocument(
            24,
            "AERO07 Engine Corrosion Inspection Techniques",
            "Corrosion inspection for AERO07 uses visual, NDT, and advanced imaging methods. CPCP implementation reduces risk and extends engine life. Documentation of findings is required.",
            ["Corrosion", "Inspection", "AERO07", "CPCP"],
            1.0
        ),
        SearchDocument(
            25,
            "AERO07 Engine Maintenance Error Reporting",
            "Reporting maintenance errors for AERO07 supports continuous improvement. Systems include root cause analysis, corrective actions, and training. Human factors are considered to prevent recurrence.",
            ["Error Reporting", "AERO07", "Human Factors", "Improvement"],
            1.0
        ),
        SearchDocument(
            26,
            "AERO07 Engine SB Status Tracking",
            "Tracking SB status for AERO07 involves electronic databases, compliance checks, and audit preparation. Mandatory SBs must be completed before return to service.",
            ["SB", "Tracking", "AERO07", "Compliance"],
            1.0
        ),
        SearchDocument(
            27,
            "AERO07 Engine MEL Restrictions",
            "MEL restrictions for AERO07 define allowable deviations and repair timelines. Dispatch is permitted only when safety and regulatory requirements are met.",
            ["MEL", "Restrictions", "AERO07", "Dispatch"],
            1.0
        ),
        SearchDocument(
            28,
            "AERO07 Engine Progressive Maintenance Segmentation",
            "Segmentation of progressive maintenance for AERO07 enables flexible scheduling and reduced downtime. Tasks are grouped based on criticality and resource availability.",
            ["Progressive", "Segmentation", "AERO07", "Scheduling"],
            1.0
        ),
        SearchDocument(
            29,
            "AERO07 Engine Quality Assurance in Repair Stations",
            "Quality assurance for AERO07 repair stations under FAR Part 145 includes audits, training, and process validation. Compliance ensures reliability and regulatory approval.",
            ["Quality Assurance", "Repair", "AERO07", "FAR 145"],
            1.0
        ),
        SearchDocument(
            30,
            "AERO07 Engine Maintenance Recordkeeping Best Practices",
            "Best practices for maintenance recordkeeping of AERO07 include electronic logs, signature verification, and secure storage. Compliance with FAR Part 43 is mandatory.",
            ["Recordkeeping", "AERO07", "FAR 43", "Best Practices"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)