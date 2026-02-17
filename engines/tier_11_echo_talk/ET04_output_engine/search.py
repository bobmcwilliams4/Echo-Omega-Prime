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

# --- Search Index ---

class SearchIndex:
    def __init__(self):
        self._documents: Dict[int, SearchDocument] = {}
        self._doc_tokens: Dict[int, List[str]] = {}
        self._inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._total_docs: int = 0
        self._corpus_size: int = 0

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            self._documents[doc.id] = doc
            self._doc_tokens[doc.id] = tokens
            self._doc_lengths[doc.id] = len(tokens)
            self._corpus_size += len(tokens)
            for token in tokens:
                self._inverted_index[token][doc.id] = self._inverted_index[token].get(doc.id, 0) + 1
            self._total_docs += 1
            self._avg_doc_length = self._corpus_size / self._total_docs if self._total_docs > 0 else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        scores: Dict[int, float] = defaultdict(float)
        snippets: Dict[int, str] = {}
        for token in set(query_tokens):
            postings = self._inverted_index.get(token, {})
            idf = self._compute_idf(token)
            for doc_id, tf in postings.items():
                doc = self._documents[doc_id]
                doc_len = self._doc_lengths[doc_id]
                bm25_score = self._score_bm25(tf, len(query_tokens), doc_len, idf, doc.weight)
                tfidf_score = self._score_tfidf(tf, doc_len, idf, doc.weight)
                scores[doc_id] += bm25_score + tfidf_score
                if doc_id not in snippets:
                    snippets[doc_id] = self._make_snippet(doc, query_tokens)
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self._documents[doc_id]
            snippet = snippets[doc_id]
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                "total_documents": self._total_docs,
                "average_doc_length": self._avg_doc_length,
                "corpus_size": self._corpus_size,
                "unique_terms": len(self._inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = self._total_docs
        df = len(self._inverted_index.get(term, {}))
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5)) if df > 0 else 0.0
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, tf: int, qf: int, doc_len: int, idf: float, weight: float) -> float:
        k1 = 1.5
        b = 0.75
        avgdl = self._avg_doc_length if self._avg_doc_length > 0 else 1
        denom = tf + k1 * (1 - b + b * (doc_len / avgdl))
        score = idf * ((tf * (k1 + 1)) / (denom + 1e-10)) * weight
        return score

    def _score_tfidf(self, tf: int, doc_len: int, idf: float, weight: float) -> float:
        tf_norm = tf / (doc_len + 1e-10)
        return tf_norm * idf * weight

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str]) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            return content[:120] + "..." if len(content) > 120 else content
        start = max(positions[0] - 5, 0)
        end = min(positions[0] + 15, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        return snippet + "..." if len(snippet) < len(tokens) else snippet

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

# --- Pre-seed Documents ---

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1, "ElevenLabs v3 API Integration",
            "Integrate ElevenLabs v3 API for advanced TTS capabilities, supporting voice selection, streaming, and emotion tags.",
            ["elevenlabs", "api", "tts", "integration"], 1.2
        ),
        SearchDocument(
            2, "Voice ID Mapping",
            "Map internal voice IDs to ElevenLabs: Echo, Bree, GS343, Prometheus, Phoenix, Commander.",
            ["voice", "id", "mapping", "elevenlabs"], 1.1
        ),
        SearchDocument(
            3, "Emotion Tag Processing",
            "Process emotion tags such as Laughs, Whispers, Sighs, Sarcastic, and Excited for expressive TTS.",
            ["emotion", "tags", "tts", "processing"], 1.0
        ),
        SearchDocument(
            4, "Cartesia API for GS343",
            "Integrate Cartesia API to enhance GS343 voice personality, enabling dynamic voice characteristics.",
            ["cartesia", "gs343", "api", "personality"], 1.15
        ),
        SearchDocument(
            5, "Whisper STT Integration",
            "Leverage Whisper for speech-to-text, enabling accurate transcription and real-time feedback.",
            ["whisper", "stt", "integration", "transcription"], 1.0
        ),
        SearchDocument(
            6, "Voice Streaming: Chunked Transfer",
            "Implement chunked transfer encoding for low-latency voice streaming and buffer management.",
            ["voice", "streaming", "chunked", "buffer"], 1.2
        ),
        SearchDocument(
            7, "Audio Format Handling",
            "Support PCM, MP3, and OGG formats with sample rate management for compatibility.",
            ["audio", "format", "pcm", "mp3", "ogg"], 1.1
        ),
        SearchDocument(
            8, "Voice Cloning Parameters",
            "Configure voice cloning parameters for personalized TTS output and speaker adaptation.",
            ["voice", "cloning", "parameters", "tts"], 1.05
        ),
        SearchDocument(
            9, "Pronunciation Dictionary Integration",
            "Integrate custom pronunciation dictionaries to improve TTS accuracy and user experience.",
            ["pronunciation", "dictionary", "tts"], 1.0
        ),
        SearchDocument(
            10, "SSML to Emotion Tag Conversion",
            "Convert SSML markup to internal emotion tags for expressive speech synthesis.",
            ["ssml", "emotion", "conversion"], 1.1
        ),
        SearchDocument(
            11, "TTS Latency Optimization",
            "Optimize TTS pipeline to minimize latency, including buffer prefetch and parallel processing.",
            ["tts", "latency", "optimization"], 1.2
        ),
        SearchDocument(
            12, "Audio Buffer Management",
            "Efficiently manage audio buffers for seamless streaming and playback.",
            ["audio", "buffer", "management"], 1.0
        ),
        SearchDocument(
            13, "Fallback Voice Selection",
            "Implement fallback strategies for unavailable voices, ensuring continuity.",
            ["voice", "fallback", "selection"], 1.0
        ),
        SearchDocument(
            14, "Voice Personality Matching",
            "Match user requests to the closest available voice personality using metadata and scoring.",
            ["voice", "personality", "matching"], 1.15
        ),
        SearchDocument(
            15, "Audio Quality Scoring",
            "Score audio output quality using perceptual metrics and noise analysis.",
            ["audio", "quality", "scoring"], 1.1
        ),
        SearchDocument(
            16, "Noise Gate Application",
            "Apply noise gate filters to reduce background noise in TTS output.",
            ["noise", "gate", "audio"], 1.0
        ),
        SearchDocument(
            17, "Volume Normalization",
            "Normalize audio volume to ensure consistent playback levels across outputs.",
            ["volume", "normalization", "audio"], 1.0
        ),
        SearchDocument(
            18, "Audio Caching",
            "Cache generated audio to reduce redundant TTS synthesis and improve response time.",
            ["audio", "caching", "performance"], 1.1
        ),
        SearchDocument(
            19, "Concurrent TTS Handling",
            "Support concurrent TTS requests with thread-safe buffer and resource management.",
            ["tts", "concurrent", "handling"], 1.2
        ),
        SearchDocument(
            20, "Echo Voice Profile",
            "Details and tuning for the Echo voice, including emotion and pronunciation settings.",
            ["voice", "echo", "profile"], 1.0
        ),
        SearchDocument(
            21, "Bree Voice Profile",
            "Bree voice configuration, emotion support, and best use cases.",
            ["voice", "bree", "profile"], 1.0
        ),
        SearchDocument(
            22, "GS343 Voice Profile",
            "GS343 voice integration, Cartesia API personality, and advanced features.",
            ["voice", "gs343", "profile"], 1.1
        ),
        SearchDocument(
            23, "Prometheus Voice Profile",
            "Prometheus voice details, emotion tags, and fallback strategies.",
            ["voice", "prometheus", "profile"], 1.0
        ),
        SearchDocument(
            24, "Phoenix Voice Profile",
            "Phoenix voice setup, supported audio formats, and emotion mapping.",
            ["voice", "phoenix", "profile"], 1.0
        ),
        SearchDocument(
            25, "Commander Voice Profile",
            "Commander voice, emotion tag compatibility, and pronunciation dictionary integration.",
            ["voice", "commander", "profile"], 1.0
        ),
        SearchDocument(
            26, "Emotion Tag: Laughs",
            "How to process and synthesize 'laughs' emotion tag for natural TTS.",
            ["emotion", "laughs", "tts"], 1.0
        ),
        SearchDocument(
            27, "Emotion Tag: Whispers",
            "Implementing whisper emotion for subtle and soft speech synthesis.",
            ["emotion", "whispers", "tts"], 1.0
        ),
        SearchDocument(
            28, "Emotion Tag: Sighs",
            "Sighs emotion synthesis for expressive and realistic TTS output.",
            ["emotion", "sighs", "tts"], 1.0
        ),
        SearchDocument(
            29, "Emotion Tag: Sarcastic",
            "Sarcastic emotion processing for nuanced speech delivery.",
            ["emotion", "sarcastic", "tts"], 1.0
        ),
        SearchDocument(
            30, "Emotion Tag: Excited",
            "Excited emotion synthesis for energetic and lively TTS.",
            ["emotion", "excited", "tts"], 1.0
        ),
        SearchDocument(
            31, "Sample Rate Management",
            "Manage sample rates for PCM, MP3, and OGG to ensure compatibility and quality.",
            ["sample", "rate", "pcm", "mp3", "ogg"], 1.0
        ),
        SearchDocument(
            32, "Streaming Buffer Optimization",
            "Optimize streaming buffers for low-latency, high-quality audio playback.",
            ["streaming", "buffer", "optimization"], 1.1
        ),
        SearchDocument(
            33, "SSML Markup Examples",
            "Examples of SSML markup for emotion, pronunciation, and voice selection.",
            ["ssml", "markup", "examples"], 1.0
        ),
        SearchDocument(
            34, "Voice Cloning Security",
            "Security considerations for voice cloning and user privacy.",
            ["voice", "cloning", "security"], 1.0
        ),
        SearchDocument(
            35, "TTS Pipeline Overview",
            "Overview of the ET04 TTS pipeline, including API integration, streaming, and caching.",
            ["tts", "pipeline", "overview"], 1.0
        ),
        SearchDocument(
            36, "Pronunciation Dictionary Format",
            "Supported formats and integration for custom pronunciation dictionaries.",
            ["pronunciation", "dictionary", "format"], 1.0
        ),
        SearchDocument(
            37, "Audio Output Formats",
            "Supported output formats: PCM, MP3, OGG, and their configuration.",
            ["audio", "output", "formats"], 1.0
        ),
        SearchDocument(
            38, "Voice Selection Algorithm",
            "Algorithm for selecting the best matching voice based on user request and metadata.",
            ["voice", "selection", "algorithm"], 1.1
        ),
        SearchDocument(
            39, "Emotion Tag Normalization",
            "Normalize emotion tags from SSML and user input for consistent processing.",
            ["emotion", "tag", "normalization"], 1.0
        ),
        SearchDocument(
            40, "Audio Quality Metrics",
            "Metrics used to assess and score audio output quality.",
            ["audio", "quality", "metrics"], 1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)