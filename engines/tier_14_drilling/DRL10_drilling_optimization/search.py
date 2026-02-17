import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

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
        self._documents: Dict[int, SearchDocument] = {}
        self._inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self._term_freqs: Dict[int, Counter] = {}
        self._doc_lengths: Dict[int, int] = {}
        self._doc_tags: Dict[int, Set[str]] = {}
        self._N = 0
        self._avgdl = 0.0
        self._lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            term_freq = Counter(tokens)
            self._documents[doc.id] = doc
            self._term_freqs[doc.id] = term_freq
            self._doc_lengths[doc.id] = len(tokens)
            self._doc_tags[doc.id] = set(doc.tags)
            for term in term_freq:
                self._inverted_index[term].add(doc.id)
            self._N += 1
            self._avgdl = sum(self._doc_lengths.values()) / self._N if self._N > 0 else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs |= self._inverted_index.get(term, set())
        scored_results = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc = self._documents[doc_id]
            final_score = bm25_score * 0.7 + tfidf_score * 0.3
            snippet = self._make_snippet(doc, query_terms)
            scored_results.append(SearchResult(doc_id, final_score, doc.title, snippet))
        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                "document_count": self._N,
                "average_doc_length": self._avgdl,
                "unique_terms": len(self._inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = len(self._inverted_index.get(term, []))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self._N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc = self._documents[doc_id]
        freq = self._term_freqs[doc_id]
        dl = self._doc_lengths[doc_id]
        for term in query_terms:
            idf = self._compute_idf(term)
            tf = freq.get(term, 0)
            numerator = tf * (self._bm25_k1 + 1)
            denominator = tf + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * dl / (self._avgdl + 1e-9))
            if denominator == 0:
                continue
            score += idf * (numerator / denominator)
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        freq = self._term_freqs[doc_id]
        dl = self._doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf = freq.get(term, 0) / (dl + 1e-9)
            idf = self._compute_idf(term)
            score += tf * idf
        return score * self._documents[doc_id].weight

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:160] + "..." if len(content) > 160 else content
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(r'\b(%s)\b' % re.escape(term), r'*\1*', snippet, flags=re.IGNORECASE)
        return snippet

# Singleton factory
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "ROP Optimization: WOB and RPM Relationship",
            "Understanding the relationship between Weight on Bit (WOB) and Rotary Speed (RPM) is crucial for optimizing Rate of Penetration (ROP). This document explores best practices and field data analysis for maximizing drilling efficiency.",
            ["ROP_Optimization", "WOB", "RPM", "Drilling_Efficiency"],
            1.0
        ),
        SearchDocument(
            2,
            "Real-Time MSE Monitoring for Drilling Operations",
            "Mechanical Specific Energy (MSE) is a key indicator for drilling performance. Real-time monitoring enables early detection of inefficiencies and drilling dysfunctions, allowing for immediate corrective actions.",
            ["MSE", "Real_Time", "Drilling_Performance", "Monitoring"],
            1.0
        ),
        SearchDocument(
            3,
            "Stick-Slip Detection in Drilling: Methods and Tools",
            "Stick-slip is a common drilling dysfunction that can cause severe bit and BHA damage. This document reviews detection algorithms and mitigation strategies using surface and downhole data.",
            ["Stick_Slip", "Dysfunction_Detection", "BHA", "Bit_Damage"],
            1.0
        ),
        SearchDocument(
            4,
            "Invisible Lost Time (ILT) Analysis in Drilling",
            "Invisible Lost Time (ILT) refers to non-productive time that is not explicitly recorded. Advanced analytics can identify ILT events and help optimize operational efficiency.",
            ["ILT", "Invisible_Lost_Time", "Analytics", "Operational_Efficiency"],
            1.0
        ),
        SearchDocument(
            5,
            "Cost Per Foot Analysis and AFE Tracking",
            "Tracking cost per foot drilled and comparing against the Authorization For Expenditure (AFE) is essential for project economics. This guide provides methodologies for accurate cost analysis.",
            ["Cost_Per_Foot", "AFE", "Economics", "Tracking"],
            1.0
        ),
        SearchDocument(
            6,
            "Offset Well Benchmarking for Performance Improvement",
            "Benchmarking against offset wells provides valuable insights for drilling optimization. This document discusses key metrics and comparative analysis techniques.",
            ["Offset_Well", "Benchmarking", "Performance", "Optimization"],
            1.0
        ),
        SearchDocument(
            7,
            "Bit Selection Optimization: Criteria and Case Studies",
            "Optimal bit selection is fundamental for maximizing ROP and minimizing drilling dysfunctions. This document covers selection criteria, bit types, and field case studies.",
            ["Bit_Selection", "Optimization", "ROP", "Case_Studies"],
            1.0
        ),
        SearchDocument(
            8,
            "BHA Optimization for ROP Enhancement",
            "Bottom Hole Assembly (BHA) design impacts ROP and wellbore quality. Learn about BHA optimization strategies for various drilling environments.",
            ["BHA_Optimization", "ROP", "Wellbore_Quality", "Design"],
            1.0
        ),
        SearchDocument(
            9,
            "Drilling Fluid Optimization for ROP",
            "Drilling fluid properties such as rheology, density, and lubricity affect ROP and bit life. This document reviews fluid selection and real-time monitoring techniques.",
            ["Drilling_Fluid", "ROP_Optimization", "Fluid_Selection", "Monitoring"],
            1.0
        ),
        SearchDocument(
            10,
            "Connection Time Optimization in Drilling",
            "Reducing connection time can significantly improve overall drilling efficiency. Explore best practices and automation technologies for connection time optimization.",
            ["Connection_Time", "Optimization", "Drilling_Efficiency", "Automation"],
            1.0
        ),
        SearchDocument(
            11,
            "Learning Curve Analysis in Pad Development",
            "Learning curve analysis helps identify operational improvements over time in pad drilling. This document presents statistical models and field examples.",
            ["Learning_Curve", "Pad_Development", "Analysis", "Operational_Improvement"],
            1.0
        ),
        SearchDocument(
            12,
            "Trip Time Optimization: Methods and Metrics",
            "Trip time optimization reduces non-productive time during pipe tripping operations. Learn about key metrics and process improvements.",
            ["Trip_Time", "Optimization", "NPT", "Metrics"],
            1.0
        ),
        SearchDocument(
            13,
            "D-Exponent: A Tool for Drilling Efficiency",
            "The D-Exponent is a normalized drilling parameter used to evaluate formation drillability and bit performance. This document explains calculation methods and interpretation.",
            ["D_Exponent", "Drilling_Efficiency", "Bit_Performance", "Formation_Evaluation"],
            1.0
        ),
        SearchDocument(
            14,
            "Advanced ROP Optimization: WOB and RPM Synergy",
            "This study investigates the synergistic effects of WOB and RPM on ROP, including optimization algorithms and field implementation results.",
            ["ROP_Optimization", "WOB", "RPM", "Synergy"],
            1.0
        ),
        SearchDocument(
            15,
            "Real-Time Stick-Slip Monitoring and Mitigation",
            "Real-time detection and mitigation of stick-slip events can extend bit life and reduce NPT. This document reviews sensor technologies and control strategies.",
            ["Stick_Slip", "Real_Time", "Mitigation", "Sensors"],
            1.0
        ),
        SearchDocument(
            16,
            "MSE-Based Drilling Dysfunction Detection",
            "Mechanical Specific Energy analysis is used to detect drilling dysfunctions such as bit balling, whirl, and stick-slip. This document presents case studies and diagnostic workflows.",
            ["MSE", "Dysfunction_Detection", "Bit_Balling", "Whirl"],
            1.0
        ),
        SearchDocument(
            17,
            "Invisible Lost Time: Detection and Reduction",
            "Techniques for detecting and reducing Invisible Lost Time (ILT) using data analytics and operational reviews.",
            ["ILT", "Detection", "Reduction", "Data_Analytics"],
            1.0
        ),
        SearchDocument(
            18,
            "AFE Tracking: Best Practices",
            "Best practices for tracking Authorization For Expenditure (AFE) and integrating with drilling performance metrics.",
            ["AFE", "Tracking", "Best_Practices", "Performance"],
            1.0
        ),
        SearchDocument(
            19,
            "Offset Well Data Integration for Benchmarking",
            "Integrating offset well data enables more accurate benchmarking and performance improvement initiatives.",
            ["Offset_Well", "Data_Integration", "Benchmarking", "Performance"],
            1.0
        ),
        SearchDocument(
            20,
            "Bit Selection: Impact on Drilling Cost",
            "Bit selection directly impacts drilling cost and efficiency. This document provides a cost-benefit analysis of bit types.",
            ["Bit_Selection", "Cost", "Efficiency", "Analysis"],
            1.0
        ),
        SearchDocument(
            21,
            "BHA Design Considerations for ROP",
            "Key design considerations for BHA to maximize ROP and minimize vibration-related dysfunctions.",
            ["BHA_Design", "ROP", "Vibration", "Dysfunction"],
            1.0
        ),
        SearchDocument(
            22,
            "Drilling Fluid Rheology and ROP",
            "The rheological properties of drilling fluids affect cuttings transport and ROP. This document reviews laboratory and field data.",
            ["Drilling_Fluid", "Rheology", "ROP", "Cuttings_Transport"],
            1.0
        ),
        SearchDocument(
            23,
            "Connection Time Reduction: Field Results",
            "Field results showing the impact of connection time reduction initiatives on overall drilling performance.",
            ["Connection_Time", "Reduction", "Field_Results", "Performance"],
            1.0
        ),
        SearchDocument(
            24,
            "Pad Development Learning Curves: Case Study",
            "A case study on learning curve analysis in multi-well pad development, highlighting operational gains.",
            ["Pad_Development", "Learning_Curve", "Case_Study", "Operational_Gains"],
            1.0
        ),
        SearchDocument(
            25,
            "Trip Time Analysis for Drilling Operations",
            "Comprehensive analysis of trip time data to identify bottlenecks and optimize tripping procedures.",
            ["Trip_Time", "Analysis", "Drilling_Operations", "Optimization"],
            1.0
        ),
        SearchDocument(
            26,
            "D-Exponent Trends in Unconventional Wells",
            "Analysis of D-Exponent trends in unconventional wells for improved drilling efficiency and formation evaluation.",
            ["D_Exponent", "Unconventional", "Trends", "Efficiency"],
            1.0
        ),
        SearchDocument(
            27,
            "Integrated ROP Optimization: WOB, RPM, and Bit Selection",
            "An integrated approach to ROP optimization considering WOB, RPM, and bit selection parameters.",
            ["ROP_Optimization", "WOB", "RPM", "Bit_Selection"],
            1.0
        ),
        SearchDocument(
            28,
            "Real-Time Drilling Fluid Monitoring for ROP",
            "Real-time monitoring of drilling fluid properties to optimize ROP and prevent drilling problems.",
            ["Drilling_Fluid", "Real_Time", "Monitoring", "ROP"],
            1.0
        ),
        SearchDocument(
            29,
            "Automated Stick-Slip Detection Algorithms",
            "Overview of automated algorithms for detecting stick-slip events in drilling operations.",
            ["Stick_Slip", "Detection", "Algorithms", "Automation"],
            1.0
        ),
        SearchDocument(
            30,
            "Invisible Lost Time: Root Cause Analysis",
            "Root cause analysis of Invisible Lost Time (ILT) events and recommendations for mitigation.",
            ["ILT", "Root_Cause", "Analysis", "Mitigation"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)