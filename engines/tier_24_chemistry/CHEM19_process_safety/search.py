import math
import re
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
        self.doc_term_freqs: Dict[str, Counter] = {}
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.token_pattern = re.compile(r'\b\w+\b', re.UNICODE)
    
    def add_document(self, doc: SearchDocument):
        if doc.id in self.documents:
            # Remove old doc data
            old_terms = self.doc_term_freqs.get(doc.id, Counter())
            for term in old_terms:
                self.term_doc_freqs[term] -= 1
                if self.term_doc_freqs[term] <= 0:
                    del self.term_doc_freqs[term]
            del self.doc_term_freqs[doc.id]
            del self.doc_lengths[doc.id]
            del self.documents[doc.id]
        
        tokens = self._tokenize(doc.title + ' ' + doc.content + ' ' + ' '.join(doc.tags))
        term_freqs = Counter(tokens)
        self.documents[doc.id] = doc
        self.doc_term_freqs[doc.id] = term_freqs
        self.doc_lengths[doc.id] = sum(term_freqs.values())
        for term in term_freqs:
            self.term_doc_freqs[term] += 1
        self.N = len(self.documents)
        self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
        self.idf_cache.clear()
    
    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        scores: Dict[str, float] = defaultdict(float)
        idf_values = {term: self._compute_idf(term) for term in query_terms}
        for doc_id, term_freqs in self.doc_term_freqs.items():
            score = self._score_bm25(term_freqs, idf_values, query_terms, doc_id)
            if score > 0:
                scores[doc_id] = score * self.documents[doc_id].weight
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id=doc_id, score=score, title=doc.title, snippet=snippet))
        return results
    
    def get_stats(self) -> Dict[str, float]:
        return {
            'total_documents': self.N,
            'average_document_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freqs),
        }
    
    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = self.token_pattern.findall(text)
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
    
    def _score_bm25(self, term_freqs: Counter, idf_values: Dict[str, float], query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        for term in query_terms:
            tf = term_freqs.get(term, 0)
            if tf == 0:
                continue
            idf = idf_values.get(term, 0.0)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length) if self.avg_doc_length > 0 else 1
            score += idf * numerator / denominator
        return score
    
    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], snippet_length: int = 160) -> str:
        content = doc.title + '. ' + doc.content
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            start = 0
            while True:
                idx = content_lower.find(term, start)
                if idx == -1:
                    break
                positions.append(idx)
                start = idx + len(term)
        if not positions:
            snippet = content[:snippet_length].strip()
            if len(content) > snippet_length:
                snippet += '...'
            return snippet
        positions.sort()
        start_pos = max(positions[0] - snippet_length // 4, 0)
        end_pos = min(start_pos + snippet_length, len(content))
        snippet = content[start_pos:end_pos].strip()
        if start_pos > 0:
            snippet = '...' + snippet
        if end_pos < len(content):
            snippet += '...'
        return snippet

_search_index_instance: Optional[SearchIndex] = None

def get_search_index() -> SearchIndex:
    global _search_index_instance
    if _search_index_instance is None:
        _search_index_instance = SearchIndex()
        _preseed_documents(_search_index_instance)
    return _search_index_instance

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id="doc001",
            title="HAZOP Node Selection and Deviation Analysis",
            content=(
                "Hazard and Operability Study (HAZOP) methodology for selecting process nodes and "
                "analyzing deviations to identify potential hazards and operability problems in chemical processes."
            ),
            tags=["HAZOP", "Node Selection", "Deviation Analysis", "Process Safety"],
            weight=1.2
        ),
        SearchDocument(
            id="doc002",
            title="LOPA Independent Protection Layer Criteria",
            content=(
                "Layer of Protection Analysis (LOPA) criteria for identifying and evaluating independent protection layers "
                "to mitigate process risks effectively."
            ),
            tags=["LOPA", "Independent Protection Layer", "Risk Mitigation"],
            weight=1.3
        ),
        SearchDocument(
            id="doc003",
            title="Consequence Modeling: Toxic Gas Dispersion",
            content=(
                "Modeling the dispersion of toxic gases in the atmosphere to predict concentration profiles and impact zones "
                "for safety assessments."
            ),
            tags=["Consequence Modeling", "Toxic Gas", "Dispersion", "Atmospheric Modeling"],
            weight=1.1
        ),
        SearchDocument(
            id="doc004",
            title="Consequence Modeling: Fire and Thermal Radiation",
            content=(
                "Assessment of fire hazards including thermal radiation effects to evaluate potential damage and safety distances."
            ),
            tags=["Consequence Modeling", "Fire", "Thermal Radiation", "Safety Distances"],
            weight=1.1
        ),
        SearchDocument(
            id="doc005",
            title="Consequence Modeling: Vapor Cloud Explosion (VCE)",
            content=(
                "Modeling vapor cloud explosions to estimate overpressure, impulse, and damage potential in chemical plants."
            ),
            tags=["Consequence Modeling", "VCE", "Explosion", "Overpressure"],
            weight=1.2
        ),
        SearchDocument(
            id="doc006",
            title="Relief Valve Sizing: Fire Case (API 520/521)",
            content=(
                "Guidelines for sizing relief valves under fire case scenarios following API 520 and API 521 standards."
            ),
            tags=["Relief Valve", "Sizing", "Fire Case", "API 520", "API 521"],
            weight=1.3
        ),
        SearchDocument(
            id="doc007",
            title="Relief Valve Sizing: Blocked Outlet Case",
            content=(
                "Methodology for sizing relief valves considering blocked outlet conditions to ensure safe pressure relief."
            ),
            tags=["Relief Valve", "Sizing", "Blocked Outlet", "Pressure Relief"],
            weight=1.3
        ),
        SearchDocument(
            id="doc008",
            title="Dust Explosion Prevention: Kst Classification",
            content=(
                "Classification of dust explosibility using Kst values to implement appropriate explosion prevention measures."
            ),
            tags=["Dust Explosion", "Kst Classification", "Explosion Prevention"],
            weight=1.2
        ),
        SearchDocument(
            id="doc009",
            title="Chemical Reactivity Hazards: DIERS Methodology",
            content=(
                "Applying the DIERS (Design Institute for Emergency Relief Systems) methodology for evaluating chemical reactivity hazards."
            ),
            tags=["Chemical Reactivity", "DIERS", "Emergency Relief", "Hazards"],
            weight=1.3
        ),
        SearchDocument(
            id="doc010",
            title="OSHA PSM 14 Elements Compliance",
            content=(
                "Overview of OSHA Process Safety Management (PSM) standard's 14 elements for regulatory compliance and safety."
            ),
            tags=["OSHA", "PSM", "Compliance", "Process Safety"],
            weight=1.4
        ),
        SearchDocument(
            id="doc011",
            title="Management of Change (MOC) Process",
            content=(
                "Procedures and best practices for managing changes in process operations to maintain safety and compliance."
            ),
            tags=["Management of Change", "MOC", "Process Safety", "Change Control"],
            weight=1.3
        ),
        SearchDocument(
            id="doc012",
            title="Inherently Safer Design (ISD) Principles",
            content=(
                "Principles of inherently safer design aimed at eliminating or reducing hazards in chemical process design."
            ),
            tags=["Inherently Safer Design", "ISD", "Process Safety", "Hazard Reduction"],
            weight=1.4
        ),
        SearchDocument(
            id="doc013",
            title="Static Electricity Hazards in Process Operations",
            content=(
                "Identification and mitigation of static electricity hazards to prevent ignition sources in chemical plants."
            ),
            tags=["Static Electricity", "Hazards", "Ignition Prevention", "Process Safety"],
            weight=1.2
        ),
        SearchDocument(
            id="doc014",
            title="Boiling Liquid Expanding Vapor Explosion (BLEVE) Prevention",
            content=(
                "Strategies and safety measures to prevent BLEVE incidents in pressure vessels containing boiling liquids."
            ),
            tags=["BLEVE", "Explosion Prevention", "Pressure Vessels", "Safety Measures"],
            weight=1.3
        ),
        SearchDocument(
            id="doc015",
            title="HAZOP Guide: Node Selection Techniques",
            content=(
                "Detailed guide on selecting nodes for HAZOP studies to ensure comprehensive hazard identification."
            ),
            tags=["HAZOP", "Node Selection", "Guide", "Hazard Identification"],
            weight=1.1
        ),
        SearchDocument(
            id="doc016",
            title="LOPA Risk Assessment and IPL Effectiveness",
            content=(
                "Evaluating risk reduction and effectiveness of Independent Protection Layers in LOPA studies."
            ),
            tags=["LOPA", "Risk Assessment", "IPL", "Effectiveness"],
            weight=1.2
        ),
        SearchDocument(
            id="doc017",
            title="Toxic Gas Dispersion Modeling Techniques",
            content=(
                "Advanced techniques for modeling toxic gas dispersion including Gaussian and CFD approaches."
            ),
            tags=["Toxic Gas", "Dispersion", "Modeling", "CFD"],
            weight=1.1
        ),
        SearchDocument(
            id="doc018",
            title="Fire and Thermal Radiation Hazard Analysis",
            content=(
                "Methods for analyzing fire hazards and thermal radiation impacts on personnel and equipment."
            ),
            tags=["Fire", "Thermal Radiation", "Hazard Analysis"],
            weight=1.2
        ),
        SearchDocument(
            id="doc019",
            title="Vapor Cloud Explosion Overpressure Estimation",
            content=(
                "Techniques for estimating overpressure and blast effects from vapor cloud explosions."
            ),
            tags=["VCE", "Overpressure", "Explosion", "Blast Effects"],
            weight=1.2
        ),
        SearchDocument(
            id="doc020",
            title="API 520/521 Relief Valve Sizing Procedures",
            content=(
                "Step-by-step procedures for sizing relief valves according to API 520 and 521 standards."
            ),
            tags=["Relief Valve", "API 520", "API 521", "Sizing Procedures"],
            weight=1.3
        ),
        SearchDocument(
            id="doc021",
            title="Blocked Outlet Relief Valve Sizing Challenges",
            content=(
                "Challenges and solutions for sizing relief valves under blocked outlet conditions."
            ),
            tags=["Relief Valve", "Blocked Outlet", "Sizing Challenges"],
            weight=1.2
        ),
        SearchDocument(
            id="doc022",
            title="Dust Explosion Kst Values and Safety Measures",
            content=(
                "Understanding Kst values for dust explosions and implementing appropriate safety measures."
            ),
            tags=["Dust Explosion", "Kst", "Safety Measures"],
            weight=1.2
        ),
        SearchDocument(
            id="doc023",
            title="DIERS Approach to Chemical Reactivity Hazard Analysis",
            content=(
                "Applying DIERS approach for emergency relief system design considering chemical reactivity hazards."
            ),
            tags=["DIERS", "Chemical Reactivity", "Emergency Relief"],
            weight=1.3
        ),
        SearchDocument(
            id="doc024",
            title="OSHA PSM 14 Elements Detailed Overview",
            content=(
                "In-depth overview of each of the 14 elements required for OSHA Process Safety Management compliance."
            ),
            tags=["OSHA", "PSM", "Compliance", "Process Safety"],
            weight=1.4
        ),
        SearchDocument(
            id="doc025",
            title="Management of Change Best Practices",
            content=(
                "Best practices and procedures for effective Management of Change in chemical process industries."
            ),
            tags=["MOC", "Best Practices", "Change Management"],
            weight=1.3
        ),
        SearchDocument(
            id="doc026",
            title="Inherently Safer Design Implementation Strategies",
            content=(
                "Strategies to implement inherently safer design principles in chemical process design and operation."
            ),
            tags=["ISD", "Implementation", "Process Safety"],
            weight=1.4
        ),
        SearchDocument(
            id="doc027",
            title="Static Electricity Hazard Controls in Process Plants",
            content=(
                "Control measures and grounding techniques to mitigate static electricity hazards in process plants."
            ),
            tags=["Static Electricity", "Hazard Control", "Grounding"],
            weight=1.2
        ),
        SearchDocument(
            id="doc028",
            title="BLEVE Incident Case Studies and Prevention",
            content=(
                "Case studies of BLEVE incidents and recommended prevention methods in chemical facilities."
            ),
            tags=["BLEVE", "Case Studies", "Prevention"],
            weight=1.3
        ),
    ]
    for doc in docs:
        index.add_document(doc)