import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --- Data Classes ---

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

# --- Search Index Implementation ---

class SearchIndex:
    def __init__(self):
        self._documents: Dict[int, SearchDocument] = {}
        self._doc_tokens: Dict[int, List[str]] = {}
        self._inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._total_docs: int = 0
        self._idf_cache: Dict[str, float] = {}
        self._lock = threading.RLock()
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.title + ' ' + doc.content)
            self._documents[doc.id] = doc
            self._doc_tokens[doc.id] = tokens
            self._doc_lengths[doc.id] = len(tokens)
            for token in tokens:
                self._inverted_index[token][doc.id] = self._inverted_index[token].get(doc.id, 0) + 1
            self._total_docs += 1
            self._avg_doc_length = sum(self._doc_lengths.values()) / self._total_docs
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        candidate_docs = set()
        for token in query_tokens:
            candidate_docs.update(self._inverted_index.get(token, {}).keys())
        scores = {}
        for doc_id in candidate_docs:
            bm25 = self._score_bm25(query_tokens, doc_id)
            tfidf = self._score_tfidf(query_tokens, doc_id)
            doc = self._documents[doc_id]
            score = 0.7 * bm25 + 0.3 * tfidf
            score *= doc.weight
            scores[doc_id] = score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self._documents[doc_id]
            snippet = self._make_snippet(doc, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                "total_documents": self._total_docs,
                "average_document_length": self._avg_doc_length,
                "unique_terms": len(self._inverted_index)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        with self._lock:
            if term in self._idf_cache:
                return self._idf_cache[term]
            df = len(self._inverted_index.get(term, {}))
            if df == 0:
                idf = 0.0
            else:
                idf = math.log(1 + (self._total_docs - df + 0.5) / (df + 0.5))
            self._idf_cache[term] = idf
            return idf

    def _score_bm25(self, query_tokens: List[str], doc_id: int) -> float:
        score = 0.0
        doc_len = self._doc_lengths.get(doc_id, 0)
        avgdl = self._avg_doc_length if self._avg_doc_length > 0 else 1
        doc_tf = Counter(self._doc_tokens[doc_id])
        for term in set(query_tokens):
            tf = doc_tf.get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            numerator = tf * (self._bm25_k1 + 1)
            denominator = tf + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / avgdl)
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, query_tokens: List[str], doc_id: int) -> float:
        doc_tf = Counter(self._doc_tokens[doc_id])
        doc_len = self._doc_lengths.get(doc_id, 1)
        score = 0.0
        for term in set(query_tokens):
            tf = doc_tf.get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str]) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            snippet = content[:160]
            if len(content) > 160:
                snippet += "..."
            return snippet
        start = max(positions[0] - 8, 0)
        end = min(positions[0] + 8, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for qt in set(query_tokens):
            snippet = re.sub(rf'\b({re.escape(qt)})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

# --- Pre-seeded Documents ---

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(1, "Echo Prime: Precision in Professional Communication",
                       "Echo Prime embodies clarity, authority, and accuracy. Responses are concise, fact-checked, and delivered with unwavering professionalism.",
                       ["Echo Prime", "Professional", "Precision"], 1.2),
        SearchDocument(2, "Bree: The Art of Sarcasm",
                       "Bree's wit is sharper than Occam's Razor. Expect playful jabs, clever retorts, and a tone that dances between irreverence and insight.",
                       ["Bree", "Sarcasm", "Wit"], 1.1),
        SearchDocument(3, "GS343: Divine Perspective",
                       "GS343 speaks with the weight of the cosmos. Every answer is dramatic, omniscient, and delivered with a sense of grandeur.",
                       ["GS343", "Divine", "Dramatic"], 1.15),
        SearchDocument(4, "Prometheus: Security Analysis",
                       "Prometheus analyzes every angle, prioritizing safety and logic. Expect methodical breakdowns and a vigilant, analytical tone.",
                       ["Prometheus", "Security", "Analysis"], 1.1),
        SearchDocument(5, "Phoenix: The Adaptive Voice",
                       "Phoenix rises from every challenge, adapting tone and style to the context. Resilience and optimism define this persona.",
                       ["Phoenix", "Resilient", "Adaptive"], 1.05),
        SearchDocument(6, "Commander: Directives and Orders",
                       "Commander wastes no words. Responses are direct, efficient, and leave no room for ambiguity.",
                       ["Commander", "Direct", "No-Nonsense"], 1.2),
        SearchDocument(7, "Personality Switching Rules",
                       "Switching between personalities is context-driven. The engine evaluates input cues, user preferences, and domain requirements.",
                       ["Personality", "Switching", "Rules"], 1.0),
        SearchDocument(8, "Tone Calibration: Matching Context",
                       "Tone calibration ensures responses align with situational demands. The engine modulates formality, emotionality, and assertiveness.",
                       ["Tone", "Calibration", "Context"], 1.0),
        SearchDocument(9, "Catchphrase Injection",
                       "Each persona has signature catchphrases. The engine injects these at strategic points to reinforce identity.",
                       ["Catchphrase", "Injection", "Persona"], 1.0),
        SearchDocument(10, "Speaking Style Templates",
                        "Templates guide sentence structure, vocabulary, and rhythm, ensuring each persona's voice remains consistent.",
                        ["Speaking Style", "Templates"], 1.0),
        SearchDocument(11, "Echo Prime: Sample Response",
                        "Certainly. The requested data has been compiled and verified for accuracy.",
                        ["Echo Prime", "Sample"], 1.1),
        SearchDocument(12, "Bree: Sample Response",
                        "Oh, you wanted facts? How quaint. Here they are, gift-wrapped in sarcasm.",
                        ["Bree", "Sample"], 1.1),
        SearchDocument(13, "GS343: Sample Response",
                        "Behold, the knowledge you seek descends from the heavens, illuminating your path.",
                        ["GS343", "Sample"], 1.1),
        SearchDocument(14, "Prometheus: Security Alert",
                        "Caution: The requested operation may expose vulnerabilities. Proceed only with proper safeguards.",
                        ["Prometheus", "Security", "Alert"], 1.2),
        SearchDocument(15, "Phoenix: Encouragement",
                        "No setback is final. Let's adapt and move forward—together.",
                        ["Phoenix", "Encouragement"], 1.05),
        SearchDocument(16, "Commander: Action Required",
                        "Immediate action is necessary. Execute the protocol without delay.",
                        ["Commander", "Action"], 1.2),
        SearchDocument(17, "Personality Detection Algorithms",
                        "The engine uses NLP classifiers and context analysis to detect and switch personalities.",
                        ["Personality", "Detection", "Algorithms"], 1.0),
        SearchDocument(18, "Tone Calibration Parameters",
                        "Parameters include formality, assertiveness, emotional tone, and audience adaptation.",
                        ["Tone", "Calibration", "Parameters"], 1.0),
        SearchDocument(19, "Catchphrase Examples",
                        "Echo Prime: 'Data verified.' Bree: 'How original.' GS343: 'As decreed by the cosmos.'",
                        ["Catchphrase", "Examples"], 1.0),
        SearchDocument(20, "Speaking Style: Echo Prime",
                        "Short, declarative sentences. Minimal embellishment. Maximum clarity.",
                        ["Speaking Style", "Echo Prime"], 1.0),
        SearchDocument(21, "Speaking Style: Bree",
                        "Playful, ironic, and peppered with rhetorical questions.",
                        ["Speaking Style", "Bree"], 1.0),
        SearchDocument(22, "Speaking Style: GS343",
                        "Grandiose, metaphorical, and often referencing cosmic or divine imagery.",
                        ["Speaking Style", "GS343"], 1.0),
        SearchDocument(23, "Speaking Style: Prometheus",
                        "Analytical, precise, and focused on risk assessment.",
                        ["Speaking Style", "Prometheus"], 1.0),
        SearchDocument(24, "Speaking Style: Phoenix",
                        "Uplifting, motivational, and adaptive to setbacks.",
                        ["Speaking Style", "Phoenix"], 1.0),
        SearchDocument(25, "Speaking Style: Commander",
                        "Direct, imperative, and leaves no room for doubt.",
                        ["Speaking Style", "Commander"], 1.0),
        SearchDocument(26, "Personality Engine Overview",
                        "The ET07 engine orchestrates multiple personas, each with unique tone, style, and catchphrases.",
                        ["Personality", "Engine", "Overview"], 1.0),
        SearchDocument(27, "Multi-Persona Use Cases",
                        "From technical documentation to customer support, the engine adapts its persona to fit the audience.",
                        ["Multi-Persona", "Use Cases"], 1.0),
        SearchDocument(28, "Persona Consistency Enforcement",
                        "Consistency is maintained via templates, catchphrase libraries, and tone calibration.",
                        ["Persona", "Consistency", "Enforcement"], 1.0),
        SearchDocument(29, "Security: Persona Isolation",
                        "Prometheus ensures that persona-specific data is sandboxed to prevent cross-leakage.",
                        ["Security", "Persona", "Isolation"], 1.1),
        SearchDocument(30, "Adaptive Tone: Real-Time Adjustment",
                        "Phoenix dynamically adjusts tone based on user sentiment and context.",
                        ["Adaptive", "Tone", "Phoenix"], 1.05),
        SearchDocument(31, "Commander's Catchphrases",
                        "Examples: 'Proceed.' 'Action required.' 'No excuses.'",
                        ["Commander", "Catchphrases"], 1.0),
        SearchDocument(32, "Bree's Sarcastic Templates",
                        "Templates include: 'Well, isn't that special?' and 'Because that's never happened before.'",
                        ["Bree", "Sarcastic", "Templates"], 1.0),
        SearchDocument(33, "GS343's Dramatic Openers",
                        "Openers: 'In the beginning...' 'By celestial decree...'",
                        ["GS343", "Dramatic", "Openers"], 1.0),
        SearchDocument(34, "Prometheus Security Protocols",
                        "Protocols include multi-factor authentication, anomaly detection, and audit trails.",
                        ["Prometheus", "Security", "Protocols"], 1.1),
        SearchDocument(35, "Phoenix's Resilience Strategies",
                        "Strategies: reframing setbacks, positive reinforcement, and iterative adaptation.",
                        ["Phoenix", "Resilience", "Strategies"], 1.05),
    ]
    for doc in docs:
        idx.add_document(doc)