import math
import threading
import re
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
    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.term_doc_freqs: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.term_freqs: Dict[str, int] = defaultdict(int)
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.total_terms: int = 0
        self.avg_doc_length: float = 0.0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self.k1 = 1.5
        self.b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_terms += len(tokens)
            term_counts = Counter(tokens)
            for term, freq in term_counts.items():
                self.term_doc_freqs[term][doc.id] = freq
                self.term_freqs[term] += freq
            for term in term_counts:
                self.doc_freqs[term] += 1
            self.avg_doc_length = self.total_terms / max(len(self.documents), 1)
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[str, float] = defaultdict(float)
        for term in query_terms:
            idf = self._compute_idf(term)
            for doc_id, freq in self.term_doc_freqs.get(term, {}).items():
                doc = self.documents[doc_id]
                score_bm25 = self._score_bm25(term, freq, doc_id, idf, doc.weight)
                score_tfidf = self._score_tfidf(term, freq, doc_id, idf, doc.weight)
                doc_scores[doc_id] += score_bm25 + 0.5 * score_tfidf
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            stats = {
                'num_documents': len(self.documents),
                'avg_doc_length': self.avg_doc_length,
                'total_terms': self.total_terms,
                'unique_terms': len(self.term_freqs),
            }
            return stats

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        tokens = text.split()
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = len(self.documents)
        df = self.doc_freqs.get(term, 0)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, term: str, freq: int, doc_id: str, idf: float, weight: float) -> float:
        doc_len = self.doc_lengths[doc_id]
        avg_len = self.avg_doc_length if self.avg_doc_length > 0 else 1
        numerator = freq * (self.k1 + 1)
        denominator = freq + self.k1 * (1 - self.b + self.b * doc_len / avg_len)
        score = idf * (numerator / denominator) * weight
        return score

    def _score_tfidf(self, term: str, freq: int, doc_id: str, idf: float, weight: float) -> float:
        doc_len = self.doc_lengths[doc_id]
        tf = freq / doc_len if doc_len > 0 else 0
        score = tf * idf * weight
        return score

    def _make_snippet(self, content: str, query_terms: List[str]) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:30]) + ('...' if len(tokens) > 30 else '')
        start = max(positions[0] - 10, 0)
        end = min(positions[0] + 20, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return snippet + ('...' if end < len(tokens) else '')

# Singleton factory
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            doc_id="1",
            title="Doctrine of Unity",
            content="Unity is the foundation of the BLD05 philosophy. It emphasizes collective action, shared purpose, and the harmonization of individual goals with the greater good.",
            tags=["unity", "philosophy", "collective"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="2",
            title="Principle of Adaptability",
            content="Adaptability ensures resilience in the face of change. BLD05 doctrine encourages flexible thinking and rapid response to evolving circumstances.",
            tags=["adaptability", "resilience", "change"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="3",
            title="Legacy Preservation",
            content="Preserving legacy is central to BLD05. The doctrine advocates for archiving knowledge, maintaining traditions, and honoring historical achievements.",
            tags=["legacy", "archive", "tradition"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="4",
            title="Ethics of Collaboration",
            content="Collaboration is a core ethical value in BLD05. Working together, sharing resources, and mutual support are encouraged to achieve optimal outcomes.",
            tags=["collaboration", "ethics", "support"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="5",
            title="Doctrine of Innovation",
            content="Innovation drives progress. BLD05 doctrine supports creative problem solving, experimentation, and the pursuit of novel solutions.",
            tags=["innovation", "progress", "creativity"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="6",
            title="Principle of Transparency",
            content="Transparency fosters trust and accountability. BLD05 doctrine mandates open communication, clear documentation, and accessible decision-making.",
            tags=["transparency", "trust", "accountability"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="7",
            title="Doctrine of Sustainability",
            content="Sustainability is vital for long-term success. BLD05 doctrine promotes resource conservation, environmental stewardship, and sustainable practices.",
            tags=["sustainability", "environment", "conservation"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="8",
            title="Principle of Inclusivity",
            content="Inclusivity ensures that all voices are heard. BLD05 doctrine values diversity, equal opportunity, and the integration of multiple perspectives.",
            tags=["inclusivity", "diversity", "opportunity"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="9",
            title="Doctrine of Efficiency",
            content="Efficiency maximizes impact. BLD05 doctrine encourages streamlined processes, resource optimization, and elimination of waste.",
            tags=["efficiency", "optimization", "impact"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="10",
            title="Principle of Accountability",
            content="Accountability is essential for integrity. BLD05 doctrine requires responsibility, transparency, and ethical conduct in all actions.",
            tags=["accountability", "integrity", "responsibility"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="11",
            title="Doctrine of Knowledge Sharing",
            content="Knowledge sharing accelerates growth. BLD05 doctrine advocates for open exchange of information, mentorship, and collaborative learning.",
            tags=["knowledge", "sharing", "learning"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="12",
            title="Principle of Strategic Planning",
            content="Strategic planning guides action. BLD05 doctrine emphasizes foresight, goal setting, and systematic evaluation.",
            tags=["strategy", "planning", "evaluation"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="13",
            title="Doctrine of Empathy",
            content="Empathy strengthens community. BLD05 doctrine encourages understanding, compassion, and support for others.",
            tags=["empathy", "community", "compassion"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="14",
            title="Principle of Continuous Improvement",
            content="Continuous improvement is a pillar of BLD05. The doctrine promotes regular assessment, feedback, and iterative enhancement.",
            tags=["improvement", "feedback", "assessment"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="15",
            title="Doctrine of Open Access",
            content="Open access democratizes information. BLD05 doctrine supports unrestricted entry to resources, data, and knowledge.",
            tags=["open access", "democracy", "information"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="16",
            title="Principle of Leadership",
            content="Leadership guides direction. BLD05 doctrine values vision, initiative, and the ability to inspire others.",
            tags=["leadership", "vision", "initiative"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="17",
            title="Doctrine of Systemic Thinking",
            content="Systemic thinking enables holistic solutions. BLD05 doctrine encourages seeing connections, understanding complexity, and designing integrated systems.",
            tags=["systemic", "holistic", "complexity"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="18",
            title="Principle of Data Integrity",
            content="Data integrity ensures reliability. BLD05 doctrine mandates accurate recording, validation, and protection of information.",
            tags=["data", "integrity", "reliability"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="19",
            title="Doctrine of Community Engagement",
            content="Community engagement fosters belonging. BLD05 doctrine supports participation, outreach, and shared responsibility.",
            tags=["community", "engagement", "participation"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="20",
            title="Principle of Resource Allocation",
            content="Resource allocation optimizes outcomes. BLD05 doctrine emphasizes fair distribution, prioritization, and effective utilization.",
            tags=["resource", "allocation", "distribution"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="21",
            title="Doctrine of Conflict Resolution",
            content="Conflict resolution maintains harmony. BLD05 doctrine advocates for mediation, negotiation, and constructive dialogue.",
            tags=["conflict", "resolution", "dialogue"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="22",
            title="Principle of Ethical Conduct",
            content="Ethical conduct is non-negotiable. BLD05 doctrine requires honesty, fairness, and adherence to moral standards.",
            tags=["ethics", "conduct", "morality"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="23",
            title="Doctrine of Digital Transformation",
            content="Digital transformation accelerates progress. BLD05 doctrine supports adoption of technology, automation, and digital literacy.",
            tags=["digital", "transformation", "technology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="24",
            title="Principle of Risk Management",
            content="Risk management safeguards assets. BLD05 doctrine emphasizes identification, mitigation, and proactive planning.",
            tags=["risk", "management", "mitigation"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="25",
            title="Doctrine of Purpose",
            content="Purpose drives motivation. BLD05 doctrine encourages clarity of mission, alignment of values, and pursuit of meaningful goals.",
            tags=["purpose", "motivation", "mission"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="26",
            title="Principle of Accessibility",
            content="Accessibility removes barriers. BLD05 doctrine advocates for inclusive design, universal access, and equitable participation.",
            tags=["accessibility", "inclusion", "design"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="27",
            title="Doctrine of Communication",
            content="Communication connects people. BLD05 doctrine values clarity, listening, and effective information exchange.",
            tags=["communication", "clarity", "exchange"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="28",
            title="Principle of Personal Development",
            content="Personal development enriches capability. BLD05 doctrine encourages self-improvement, learning, and growth.",
            tags=["personal", "development", "growth"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="29",
            title="Doctrine of Decentralization",
            content="Decentralization empowers autonomy. BLD05 doctrine supports distributed decision-making, local initiative, and reduced hierarchy.",
            tags=["decentralization", "autonomy", "initiative"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="30",
            title="Principle of Fairness",
            content="Fairness ensures justice. BLD05 doctrine mandates impartiality, equal treatment, and unbiased evaluation.",
            tags=["fairness", "justice", "impartiality"],
            weight=1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)