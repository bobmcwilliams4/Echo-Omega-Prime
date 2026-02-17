import math
import re
import threading
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional


class SearchDocument:
    def __init__(self, id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = id
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
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freqs: Dict[str, Dict[str, int]] = defaultdict(dict)  # term -> {doc_id: freq}
        self.idf_cache: Dict[str, float] = {}
        self.total_docs: int = 0
        self.lock = threading.Lock()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                # Remove old document data
                self._remove_document(doc.id)
            tokens = self._tokenize(doc.title + " " + doc.content)
            term_freqs = Counter(tokens)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            for term, freq in term_freqs.items():
                self.term_doc_freqs[term][doc.id] = freq
            self.total_docs = len(self.documents)
            self.avg_doc_length = (
                sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            )
            self.idf_cache.clear()

    def _remove_document(self, doc_id: str):
        if doc_id not in self.documents:
            return
        # Remove term frequencies for this doc
        for term in list(self.term_doc_freqs.keys()):
            if doc_id in self.term_doc_freqs[term]:
                del self.term_doc_freqs[term][doc_id]
            if not self.term_doc_freqs[term]:
                del self.term_doc_freqs[term]
        del self.documents[doc_id]
        del self.doc_lengths[doc_id]
        self.total_docs = len(self.documents)
        self.avg_doc_length = (
            sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
        )
        self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms or self.total_docs == 0:
            return []

        scores: Dict[str, float] = defaultdict(float)
        idf_values = {term: self._compute_idf(term) for term in query_terms}

        for term in query_terms:
            postings = self.term_doc_freqs.get(term, {})
            idf = idf_values.get(term, 0.0)
            for doc_id, freq in postings.items():
                score = self._score_bm25(freq, idf, self.doc_lengths[doc_id])
                scores[doc_id] += score

        # Adjust scores by document weight
        for doc_id in scores.keys():
            scores[doc_id] *= self.documents[doc_id].weight

        ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]

        results = []
        for doc_id, score in ranked_docs:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id=doc_id, score=score, title=doc.title, snippet=snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "total_documents": self.total_docs,
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
        df = len(self.term_doc_freqs.get(term, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, freq: int, idf: float, doc_len: int) -> float:
        numerator = freq * (self.k1 + 1)
        denominator = freq + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
        return idf * numerator / denominator if denominator != 0 else 0.0

    def _make_snippet(self, content: str, query_terms: List[str], snippet_len: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            start = 0
            while True:
                idx = content_lower.find(term, start)
                if idx == -1:
                    break
                positions.append(idx)
                start = idx + 1
        if not positions:
            snippet = content[:snippet_len].strip()
            if len(content) > snippet_len:
                snippet += "..."
            return snippet

        positions.sort()
        start_pos = max(positions[0] - snippet_len // 4, 0)
        end_pos = start_pos + snippet_len
        snippet = content[start_pos:end_pos].strip()
        if start_pos > 0:
            snippet = "..." + snippet
        if end_pos < len(content):
            snippet += "..."
        return snippet


_singleton_instance: Optional[SearchIndex] = None
_singleton_lock = threading.Lock()


def get_search_index() -> SearchIndex:
    global _singleton_instance
    if _singleton_instance is None:
        with _singleton_lock:
            if _singleton_instance is None:
                _singleton_instance = SearchIndex()
                _preseed_documents(_singleton_instance)
    return _singleton_instance


def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id="doc001",
            title="API Cement Class Selection Guidelines",
            content=(
                "This document outlines the API cement classes used in oil well cementing operations. "
                "It explains the properties and applications of each class to ensure proper selection "
                "based on well conditions."
            ),
            tags=["API Cement", "Cement Class", "Selection", "Guidelines"],
            weight=1.2,
        ),
        SearchDocument(
            id="doc002",
            title="Designing Cement Slurry Density for Well Integrity",
            content=(
                "Cement slurry density design is critical for well integrity. This document covers methods "
                "to calculate and adjust slurry density to balance formation pressure and prevent fluid migration."
            ),
            tags=["Cement Slurry", "Density Design", "Well Integrity"],
            weight=1.1,
        ),
        SearchDocument(
            id="doc003",
            title="Cement Additives: Retarders and Their Applications",
            content=(
                "Retarders are additives used to delay the setting time of cement slurry. This document "
                "details types of retarders, their chemical mechanisms, and field applications."
            ),
            tags=["Cement Additives", "Retarders", "Setting Time"],
            weight=1.0,
        ),
        SearchDocument(
            id="doc004",
            title="Fluid Loss Control Additives in Cement Slurries",
            content=(
                "Fluid loss control additives prevent the loss of water from cement slurry into the formation. "
                "This document discusses common fluid loss additives and their impact on slurry properties."
            ),
            tags=["Cement Additives", "Fluid Loss Control", "Slurry Properties"],
            weight=1.0,
        ),
        SearchDocument(
            id="doc005",
            title="Primary Cementing and Displacement Efficiency",
            content=(
                "Primary cementing operations require efficient displacement of drilling fluids by cement slurry. "
                "This document explains displacement efficiency factors and best practices."
            ),
            tags=["Primary Cementing", "Displacement Efficiency", "Operations"],
            weight=1.3,
        ),
        SearchDocument(
            id="doc006",
            title="Interpreting Cement Bond Logs (CBL)",
            content=(
                "Cement Bond Logs provide information about the quality of cement bonding. This document "
                "explains interpretation techniques and common indicators of cement integrity."
            ),
            tags=["Cement Bond Log", "CBL", "Interpretation"],
            weight=1.1,
        ),
        SearchDocument(
            id="doc007",
            title="Remedial Cementing: Squeeze Operations Procedures",
            content=(
                "Squeeze cementing is a remedial operation to seal unwanted fluid channels. This document "
                "details procedures, equipment, and materials used in squeeze operations."
            ),
            tags=["Remedial Cementing", "Squeeze Operations", "Procedures"],
            weight=1.2,
        ),
        SearchDocument(
            id="doc008",
            title="Gas Migration Mechanisms and Prevention in Cementing",
            content=(
                "Gas migration during cementing can compromise well integrity. This document reviews mechanisms "
                "of gas migration and methods to prevent it."
            ),
            tags=["Gas Migration", "Prevention", "Cementing"],
            weight=1.3,
        ),
        SearchDocument(
            id="doc009",
            title="Foamed Cement: Design and Application Techniques",
            content=(
                "Foamed cement is used to reduce slurry density and improve placement. This document covers "
                "design principles and field applications of foamed cement."
            ),
            tags=["Foamed Cement", "Design", "Application"],
            weight=1.1,
        ),
        SearchDocument(
            id="doc010",
            title="Challenges and Solutions in HPHT Cementing",
            content=(
                "High Pressure High Temperature (HPHT) cementing poses unique challenges. This document discusses "
                "common issues and engineering solutions for HPHT environments."
            ),
            tags=["HPHT Cementing", "Challenges", "Solutions"],
            weight=1.4,
        ),
        SearchDocument(
            id="doc011",
            title="Managing Lost Circulation During Cementing Operations",
            content=(
                "Lost circulation can cause cementing failures. This document explains causes, detection, and "
                "mitigation techniques for lost circulation."
            ),
            tags=["Lost Circulation", "Cementing", "Mitigation"],
            weight=1.2,
        ),
        SearchDocument(
            id="doc012",
            title="Two-Plug Cementing Method Overview",
            content=(
                "The two-plug method is a common technique for primary cementing. This document outlines the "
                "steps, equipment, and advantages of the two-plug method."
            ),
            tags=["Two-Plug Cementing", "Method", "Primary Cementing"],
            weight=1.1,
        ),
        SearchDocument(
            id="doc013",
            title="Liner Cementing Using the DV Tool",
            content=(
                "The DV tool enhances liner cementing operations by improving displacement efficiency. This "
                "document describes the tool's design and operational guidelines."
            ),
            tags=["Liner Cementing", "DV Tool", "Displacement Efficiency"],
            weight=1.3,
        ),
        SearchDocument(
            id="doc014",
            title="Cement Contamination: Mud and Cement Mixing Effects",
            content=(
                "Contamination of cement slurry by drilling mud affects cement properties. This document "
                "explores contamination sources and prevention methods."
            ),
            tags=["Cement Contamination", "Mud Mixing", "Cement Properties"],
            weight=1.2,
        ),
        SearchDocument(
            id="doc015",
            title="Free Water and Cement Settling Phenomena",
            content=(
                "Free water and settling in cement slurry can cause channeling and weak zones. This document "
                "examines causes and control measures."
            ),
            tags=["Free Water", "Cement Settling", "Slurry Stability"],
            weight=1.1,
        ),
        SearchDocument(
            id="doc016",
            title="Thickening Time and API Cementing Schedules",
            content=(
                "Thickening time defines the workable period of cement slurry. This document reviews API "
                "schedules and factors affecting thickening time."
            ),
            tags=["Thickening Time", "API Schedules", "Cementing"],
            weight=1.0,
        ),
        SearchDocument(
            id="doc017",
            title="Optimizing Cement Slurry Rheology for Pumping",
            content=(
                "Proper slurry rheology ensures efficient pumping and placement. This document discusses "
                "rheological properties and optimization techniques."
            ),
            tags=["Cement Slurry", "Rheology", "Pumping"],
            weight=1.0,
        ),
        SearchDocument(
            id="doc018",
            title="Additives for Enhancing Cement Slurry Performance",
            content=(
                "Various additives improve cement slurry performance under different conditions. This document "
                "provides an overview of common additives and their functions."
            ),
            tags=["Cement Additives", "Performance", "Slurry"],
            weight=1.1,
        ),
        SearchDocument(
            id="doc019",
            title="Cement Hydration and Strength Development",
            content=(
                "Understanding cement hydration is key to predicting strength development. This document "
                "explains hydration chemistry and testing methods."
            ),
            tags=["Cement Hydration", "Strength Development", "Chemistry"],
            weight=1.0,
        ),
        SearchDocument(
            id="doc020",
            title="Techniques for Evaluating Cement Integrity",
            content=(
                "Evaluating cement integrity ensures zonal isolation. This document covers logging tools "
                "and evaluation techniques."
            ),
            tags=["Cement Integrity", "Evaluation", "Logging"],
            weight=1.2,
        ),
        SearchDocument(
            id="doc021",
            title="Preventing Gas Channeling in Primary Cementing",
            content=(
                "Gas channeling compromises cement jobs. This document discusses prevention strategies and "
                "monitoring during primary cementing."
            ),
            tags=["Gas Migration", "Channeling", "Primary Cementing"],
            weight=1.3,
        ),
        SearchDocument(
            id="doc022",
            title="Foamed Cement Additive Selection Criteria",
            content=(
                "Selecting appropriate additives is crucial for foamed cement stability. This document "
                "reviews criteria and additive types."
            ),
            tags=["Foamed Cement", "Additives", "Selection"],
            weight=1.0,
        ),
        SearchDocument(
            id="doc023",
            title="High Temperature Cementing Additive Technologies",
            content=(
                "Special additives are required for high temperature cementing. This document details "
                "technologies and formulations."
            ),
            tags=["HPHT Cementing", "Additives", "High Temperature"],
            weight=1.2,
        ),
        SearchDocument(
            id="doc024",
            title="Lost Circulation Materials for Cementing Applications",
            content=(
                "Lost circulation materials (LCMs) help mitigate fluid loss during cementing. This document "
                "describes types and application methods."
            ),
            tags=["Lost Circulation", "Materials", "Cementing"],
            weight=1.1,
        ),
        SearchDocument(
            id="doc025",
            title="Two-Plug Cementing: Troubleshooting Common Issues",
            content=(
                "This document addresses common problems encountered during two-plug cementing and "
                "provides troubleshooting tips."
            ),
            tags=["Two-Plug Cementing", "Troubleshooting", "Operations"],
            weight=1.0,
        ),
        SearchDocument(
            id="doc026",
            title="Liner Cementing Best Practices with DV Tool",
            content=(
                "Best practices for liner cementing using the DV tool to maximize displacement and zonal isolation."
            ),
            tags=["Liner Cementing", "DV Tool", "Best Practices"],
            weight=1.3,
        ),
        SearchDocument(
            id="doc027",
            title="Cement Contamination Effects on Slurry Properties",
            content=(
                "Analyzes how contamination impacts slurry rheology, thickening time, and final set properties."
            ),
            tags=["Cement Contamination", "Slurry Properties", "Effects"],
            weight=1.1,
        ),
        SearchDocument(
            id="doc028",
            title="Free Water Control Techniques in Cementing",
            content=(
                "Methods to detect and control free water in cement slurry to prevent channeling and weak zones."
            ),
            tags=["Free Water", "Control", "Cementing"],
            weight=1.0,
        ),
        SearchDocument(
            id="doc029",
            title="API Thickening Time Schedules and Field Adjustments",
            content=(
                "Review of API thickening time schedules with guidance on adjusting for temperature and additives."
            ),
            tags=["Thickening Time", "API Schedules", "Adjustments"],
            weight=1.0,
        ),
        SearchDocument(
            id="doc030",
            title="Advanced Cement Bond Log Interpretation Techniques",
            content=(
                "Advanced methods for interpreting CBL data to assess cement sheath quality and detect microannuli."
            ),
            tags=["Cement Bond Log", "CBL", "Advanced Interpretation"],
            weight=1.2,
        ),
    ]

    for doc in docs:
        index.add_document(doc)