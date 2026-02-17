import math
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
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_term_freqs: Dict[int, Counter] = {}
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.avg_doc_len: float = 0.0
        self.total_doc_len: int = 0
        self.N: int = 0  # total number of documents
        self.idf_cache: Dict[str, float] = {}

    def add_document(self, doc: SearchDocument):
        if doc.id in self.documents:
            # Remove old document stats
            old_doc_len = sum(self.doc_term_freqs[doc.id].values())
            self.total_doc_len -= old_doc_len
            old_terms = self.doc_term_freqs[doc.id].keys()
            for term in old_terms:
                self.term_doc_freqs[term] -= 1
                if self.term_doc_freqs[term] <= 0:
                    del self.term_doc_freqs[term]
            del self.doc_term_freqs[doc.id]
            del self.documents[doc.id]
            self.N -= 1

        tokens = self._tokenize(doc.title + " " + doc.content)
        term_freqs = Counter(tokens)
        self.documents[doc.id] = doc
        self.doc_term_freqs[doc.id] = term_freqs

        for term in term_freqs.keys():
            self.term_doc_freqs[term] += 1

        doc_len = sum(term_freqs.values())
        self.total_doc_len += doc_len
        self.N += 1
        self.avg_doc_len = self.total_doc_len / self.N if self.N > 0 else 0.0
        self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms or self.N == 0:
            return []

        scores: Dict[int, float] = defaultdict(float)
        for term in set(query_terms):
            idf = self._compute_idf(term)
            for doc_id, doc in self.documents.items():
                tf = self.doc_term_freqs[doc_id].get(term, 0)
                if tf == 0:
                    continue
                score = self._score_bm25(tf, idf, doc_id)
                scores[doc_id] += score * doc.weight

        if not scores:
            return []

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            "total_documents": self.N,
            "average_document_length": self.avg_doc_len,
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

    def _score_bm25(self, tf: int, idf: float, doc_id: int) -> float:
        doc_len = sum(self.doc_term_freqs[doc_id].values())
        norm_tf = tf
        denom = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_len)
        score = idf * (norm_tf * (self.k1 + 1)) / denom if denom > 0 else 0.0
        return score

    def _make_snippet(self, content: str, query_terms: List[str], snippet_len: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            pos = content_lower.find(term)
            if pos >= 0:
                positions.append(pos)
        if not positions:
            snippet = content[:snippet_len].strip()
            if len(content) > snippet_len:
                snippet += "..."
            return snippet

        start = max(min(positions) - snippet_len // 4, 0)
        end = start + snippet_len
        snippet = content[start:end].strip()
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet += "..."
        return snippet


_search_index_instance: Optional[SearchIndex] = None


def get_search_index() -> SearchIndex:
    global _search_index_instance
    if _search_index_instance is None:
        _search_index_instance = SearchIndex()
        _preseed_documents(_search_index_instance)
    return _search_index_instance


def _preseed_documents(index: SearchIndex):
    # 25+ domain documents for AUTO04 electrical systems domain
    docs = [
        SearchDocument(
            1,
            "Basic Electrical Circuit Theory",
            "Electrical circuits consist of voltage sources, resistors, capacitors, and inductors connected in series or parallel to perform specific functions.",
            ["circuit", "theory", "basics"]
        ),
        SearchDocument(
            2,
            "Ohm's Law and Applications",
            "Ohm's Law states that the current through a conductor between two points is directly proportional to the voltage across the two points.",
            ["ohm", "law", "current", "voltage"]
        ),
        SearchDocument(
            3,
            "Series and Parallel Circuits",
            "In series circuits, components are connected end-to-end, while in parallel circuits, components are connected across the same voltage source.",
            ["series", "parallel", "circuits"]
        ),
        SearchDocument(
            4,
            "Alternating Current (AC) Fundamentals",
            "AC is an electric current which periodically reverses direction, unlike direct current (DC) which flows only in one direction.",
            ["ac", "alternating current", "fundamentals"]
        ),
        SearchDocument(
            5,
            "Direct Current (DC) Fundamentals",
            "DC is the unidirectional flow of electric charge, commonly used in batteries and electronic devices.",
            ["dc", "direct current", "fundamentals"]
        ),
        SearchDocument(
            6,
            "Transformers and Their Operation",
            "Transformers transfer electrical energy between circuits through electromagnetic induction, changing voltage and current levels.",
            ["transformer", "electromagnetic", "induction"]
        ),
        SearchDocument(
            7,
            "Electrical Power and Energy",
            "Power in electrical circuits is the rate at which energy is transferred or converted, measured in watts.",
            ["power", "energy", "watts"]
        ),
        SearchDocument(
            8,
            "Capacitors and Capacitance",
            "Capacitors store electrical energy in an electric field, characterized by their capacitance measured in farads.",
            ["capacitor", "capacitance", "energy storage"]
        ),
        SearchDocument(
            9,
            "Inductors and Inductance",
            "Inductors store energy in a magnetic field when electrical current flows through them, measured in henrys.",
            ["inductor", "inductance", "magnetic field"]
        ),
        SearchDocument(
            10,
            "Electrical Safety Standards",
            "Safety standards ensure proper handling and operation of electrical systems to prevent accidents and damage.",
            ["safety", "standards", "electrical"]
        ),
        SearchDocument(
            11,
            "Circuit Protection Devices",
            "Devices such as fuses and circuit breakers protect electrical circuits from overcurrent and short circuits.",
            ["protection", "fuse", "circuit breaker"]
        ),
        SearchDocument(
            12,
            "Electrical Wiring and Installation",
            "Proper wiring techniques and installation practices are essential for safe and efficient electrical systems.",
            ["wiring", "installation", "practices"]
        ),
        SearchDocument(
            13,
            "Motors and Generators",
            "Electric motors convert electrical energy into mechanical energy, while generators do the reverse.",
            ["motor", "generator", "energy conversion"]
        ),
        SearchDocument(
            14,
            "Battery Technologies and Maintenance",
            "Batteries store chemical energy and require maintenance to ensure longevity and performance.",
            ["battery", "maintenance", "technology"]
        ),
        SearchDocument(
            15,
            "Power Electronics and Converters",
            "Power electronics involve devices that control and convert electrical power efficiently.",
            ["power electronics", "converters", "control"]
        ),
        SearchDocument(
            16,
            "Signal Processing in Electrical Systems",
            "Signal processing involves analyzing and modifying electrical signals for communication and control.",
            ["signal", "processing", "communication"]
        ),
        SearchDocument(
            17,
            "Electrical Measurement Instruments",
            "Instruments like multimeters and oscilloscopes measure voltage, current, resistance, and waveforms.",
            ["measurement", "instruments", "multimeter", "oscilloscope"]
        ),
        SearchDocument(
            18,
            "Grounding and Earthing Principles",
            "Grounding provides a reference point for electrical circuits and helps protect against electrical shock.",
            ["grounding", "earthing", "safety"]
        ),
        SearchDocument(
            19,
            "Power Distribution Systems",
            "Power distribution involves delivering electrical power from generation sources to end users safely and efficiently.",
            ["power distribution", "systems", "delivery"]
        ),
        SearchDocument(
            20,
            "Electrical Load Analysis",
            "Load analysis determines the power requirements and characteristics of electrical systems.",
            ["load", "analysis", "power requirements"]
        ),
        SearchDocument(
            21,
            "Renewable Energy Electrical Systems",
            "Electrical systems designed to integrate renewable energy sources like solar and wind power.",
            ["renewable", "solar", "wind", "energy"]
        ),
        SearchDocument(
            22,
            "Electrical System Troubleshooting",
            "Techniques and tools used to diagnose and fix electrical system faults and failures.",
            ["troubleshooting", "diagnosis", "faults"]
        ),
        SearchDocument(
            23,
            "Control Systems and Automation",
            "Electrical control systems automate processes using sensors, controllers, and actuators.",
            ["control", "automation", "sensors"]
        ),
        SearchDocument(
            24,
            "Electrical Codes and Regulations",
            "Codes and regulations govern the design, installation, and maintenance of electrical systems.",
            ["codes", "regulations", "standards"]
        ),
        SearchDocument(
            25,
            "Electrical System Design Principles",
            "Design principles ensure electrical systems are safe, efficient, and meet user requirements.",
            ["design", "principles", "efficiency"]
        ),
        SearchDocument(
            26,
            "Power Factor and Its Correction",
            "Power factor measures the efficiency of power usage and can be corrected to improve system performance.",
            ["power factor", "correction", "efficiency"]
        ),
        SearchDocument(
            27,
            "Electrical Noise and Interference",
            "Noise and interference affect signal quality and can be mitigated through shielding and filtering.",
            ["noise", "interference", "shielding"]
        ),
        SearchDocument(
            28,
            "Lighting Systems and Controls",
            "Electrical lighting systems include lamps, ballasts, and controls for energy-efficient illumination.",
            ["lighting", "controls", "illumination"]
        ),
        SearchDocument(
            29,
            "Electrical System Maintenance Procedures",
            "Regular maintenance ensures reliability and safety of electrical systems through inspections and testing.",
            ["maintenance", "inspection", "testing"]
        ),
        SearchDocument(
            30,
            "High Voltage Electrical Systems",
            "High voltage systems require specialized equipment and safety measures for operation and maintenance.",
            ["high voltage", "equipment", "safety"]
        ),
    ]
    for doc in docs:
        index.add_document(doc)