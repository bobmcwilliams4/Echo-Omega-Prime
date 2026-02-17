import threading
import math
import re
import heapq
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

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
        self._inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self._doc_freqs: Dict[str, int] = defaultdict(int)
        self._doc_term_freqs: Dict[int, Counter] = {}
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
                return  # No duplicates
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            term_freq = Counter(tokens)
            self._documents[doc.id] = doc
            self._doc_term_freqs[doc.id] = term_freq
            self._doc_lengths[doc.id] = len(tokens)
            for token in term_freq:
                self._inverted_index[token].add(doc.id)
                self._doc_freqs[token] += 1
            self._total_docs += 1
            self._avg_doc_length = sum(self._doc_lengths.values()) / self._total_docs if self._total_docs > 0 else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        tokens = self._tokenize(query)
        if not tokens:
            return []
        candidate_doc_ids = set()
        for token in tokens:
            candidate_doc_ids.update(self._inverted_index.get(token, set()))
        scored_results = []
        for doc_id in candidate_doc_ids:
            bm25_score = self._score_bm25(doc_id, tokens)
            tfidf_score = self._score_tfidf(doc_id, tokens)
            final_score = 0.7 * bm25_score + 0.3 * tfidf_score
            doc = self._documents[doc_id]
            snippet = self._make_snippet(doc, tokens)
            scored_results.append(SearchResult(doc_id, final_score, doc.title, snippet))
        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                "total_documents": self._total_docs,
                "avg_doc_length": self._avg_doc_length,
                "unique_terms": len(self._inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        tokens = text.split()
        return [t for t in tokens if len(t) > 1]

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self._doc_freqs.get(term, 0)
        N = self._total_docs
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_tokens: List[str]) -> float:
        doc = self._documents[doc_id]
        term_freq = self._doc_term_freqs[doc_id]
        doc_len = self._doc_lengths[doc_id]
        avg_dl = self._avg_doc_length if self._avg_doc_length > 0 else 1.0
        score = 0.0
        for term in set(query_tokens):
            tf = term_freq.get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            denom = tf + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / avg_dl)
            score += idf * (tf * (self._bm25_k1 + 1)) / denom
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_tokens: List[str]) -> float:
        term_freq = self._doc_term_freqs[doc_id]
        doc_len = self._doc_lengths[doc_id]
        score = 0.0
        for term in set(query_tokens):
            tf = term_freq.get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len if doc_len > 0 else 0.0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], max_len: int = 160) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            snippet = content[:max_len]
        else:
            start = max(positions[0] - 5, 0)
            end = min(start + 30, len(tokens))
            snippet = " ".join(tokens[start:end])
        if len(snippet) > max_len:
            snippet = snippet[:max_len] + "..."
        return snippet

# --- Singleton Factory ---

_search_index_instance = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

# --- Pre-seed Documents ---

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1, "Voice Input Classification Rules",
            "Defines the rules for classifying voice input into commands, queries, and intents. Supports multi-modal input and context-aware classification.",
            ["classification", "voice", "input", "rules"], 1.0),
        SearchDocument(
            2, "STT Output Normalization",
            "Standardizes speech-to-text (STT) output by removing artifacts, correcting common errors, and applying text normalization for downstream processing.",
            ["stt", "normalization", "output"], 1.0),
        SearchDocument(
            3, "Conversation Mode Selection",
            "Automatically selects between deterministic, hybrid, and LLM conversation modes based on input context and user preferences.",
            ["conversation", "mode", "selection"], 1.0),
        SearchDocument(
            4, "Deterministic Mode Triggers",
            "Specifies triggers and rules for activating deterministic mode, including keyword detection and input pattern matching.",
            ["deterministic", "mode", "triggers"], 1.0),
        SearchDocument(
            5, "Hybrid Mode Triggers",
            "Describes how hybrid mode is triggered by ambiguous input or when both rule-based and LLM responses are beneficial.",
            ["hybrid", "mode", "triggers"], 1.0),
        SearchDocument(
            6, "LLM Mode Triggers",
            "Details the triggers for switching to large language model (LLM) mode, such as open-ended queries and complex requests.",
            ["llm", "mode", "triggers"], 1.0),
        SearchDocument(
            7, "Input Intent Classification",
            "Implements intent classification using both statistical and neural models, supporting extensible intent taxonomies.",
            ["input", "intent", "classification"], 1.0),
        SearchDocument(
            8, "Command vs Query Detection",
            "Differentiates between commands and queries in voice input using syntactic and semantic analysis.",
            ["command", "query", "detection"], 1.0),
        SearchDocument(
            9, "Voice Activity Detection (VAD)",
            "Employs robust VAD algorithms to segment speech from silence and background noise, improving input reliability.",
            ["vad", "voice", "activity", "detection"], 1.0),
        SearchDocument(
            10, "Wakeword Handling",
            "Handles wakeword detection, suppression, and false positive mitigation for seamless user experience.",
            ["wakeword", "detection", "handling"], 1.0),
        SearchDocument(
            11, "Multi-Turn Context Tracking",
            "Tracks conversational context across multiple turns, maintaining state and resolving references.",
            ["multi-turn", "context", "tracking"], 1.0),
        SearchDocument(
            12, "Language Detection",
            "Detects spoken language in real time to route input to appropriate models and normalization pipelines.",
            ["language", "detection"], 1.0),
        SearchDocument(
            13, "Profanity Filtering",
            "Filters profane and inappropriate content from STT output using customizable blacklists and context-aware rules.",
            ["profanity", "filtering"], 1.0),
        SearchDocument(
            14, "Input Length Validation",
            "Validates input length to prevent buffer overflows and ensure manageable utterance sizes for processing.",
            ["input", "length", "validation"], 1.0),
        SearchDocument(
            15, "Urgency Detection",
            "Detects urgency in voice input to prioritize critical commands and escalate emergency scenarios.",
            ["urgency", "detection"], 1.0),
        SearchDocument(
            16, "PII Detection in Voice",
            "Identifies personally identifiable information (PII) in voice input for compliance and privacy protection.",
            ["pii", "detection", "privacy"], 1.0),
        SearchDocument(
            17, "Whisper STT Integration",
            "Integrates OpenAI Whisper for high-accuracy speech-to-text, supporting multiple languages and accents.",
            ["whisper", "stt", "integration"], 1.0),
        SearchDocument(
            18, "Noise Handling",
            "Implements noise reduction and robust input handling to improve recognition in challenging environments.",
            ["noise", "handling"], 1.0),
        SearchDocument(
            19, "Multi-Speaker Diarization",
            "Segments and labels speech by speaker, enabling multi-user conversations and speaker-specific actions.",
            ["multi-speaker", "diarization"], 1.0),
        SearchDocument(
            20, "Input Confidence Scoring",
            "Assigns confidence scores to input segments, allowing downstream modules to handle uncertainty.",
            ["input", "confidence", "scoring"], 1.0),
        SearchDocument(
            21, "No Doctrine Match",
            "Handles cases where input does not match any known doctrine, triggering fallback and clarification mechanisms.",
            ["no", "doctrine", "match"], 1.0),
        SearchDocument(
            22, "Context-Aware Classification",
            "Enhances input classification by incorporating conversational and environmental context.",
            ["context-aware", "classification"], 1.0),
        SearchDocument(
            23, "Real-Time Processing Pipeline",
            "Describes the real-time pipeline for voice input, including VAD, normalization, and intent detection.",
            ["real-time", "processing", "pipeline"], 1.0),
        SearchDocument(
            24, "Ambiguity Resolution",
            "Resolves ambiguous input using hybrid mode and clarification prompts.",
            ["ambiguity", "resolution"], 1.0),
        SearchDocument(
            25, "Fallback Strategies",
            "Defines strategies for fallback when input cannot be classified or understood.",
            ["fallback", "strategies"], 1.0),
        SearchDocument(
            26, "Customizable Taxonomies",
            "Supports customizable intent and command taxonomies for domain adaptation.",
            ["customizable", "taxonomies"], 1.0),
        SearchDocument(
            27, "User Preference Adaptation",
            "Adapts classification and mode selection based on user preferences and interaction history.",
            ["user", "preference", "adaptation"], 1.0),
        SearchDocument(
            28, "Latency Optimization",
            "Optimizes for low-latency voice input processing in real-time applications.",
            ["latency", "optimization"], 1.0),
        SearchDocument(
            29, "Security and Privacy",
            "Implements security and privacy safeguards for all voice input processing stages.",
            ["security", "privacy"], 1.0),
        SearchDocument(
            30, "Extensible Plugin Architecture",
            "Supports plugins for extending classification, normalization, and detection capabilities.",
            ["extensible", "plugin", "architecture"], 1.0),
    ]
    for doc in docs:
        index.add_document(doc)