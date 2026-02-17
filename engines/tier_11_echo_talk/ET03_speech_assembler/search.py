import math
import threading
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
        self.term_doc_freqs: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.doc_tags: Dict[int, List[str]] = {}
        self.N = 0
        self.avg_doc_len = 0.0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.term_freqs[doc.id] = Counter(tokens)
            for token in set(tokens):
                self.term_doc_freqs[token][doc.id] = self.term_freqs[doc.id][token]
            self.doc_tags[doc.id] = doc.tags
            self.N = len(self.documents)
            self.avg_doc_len = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        scores = defaultdict(float)
        snippets = {}
        for doc_id, doc in self.documents.items():
            score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            combined_score = score * 0.7 + tfidf_score * 0.3
            if combined_score > 0:
                scores[doc_id] = combined_score * doc.weight
                snippets[doc_id] = self._make_snippet(doc.content, query_tokens)
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = snippets[doc_id]
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            "num_documents": self.N,
            "avg_doc_length": self.avg_doc_len,
            "unique_terms": len(self.term_doc_freqs),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = len(self.term_doc_freqs.get(term, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_tokens: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        for term in query_tokens:
            idf = self._compute_idf(term)
            freq = self.term_freqs[doc_id].get(term, 0)
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * doc_len / (self.avg_doc_len if self.avg_doc_len > 0 else 1))
            term_score = idf * numerator / (denominator + 1e-10)
            score += term_score
        return score

    def _score_tfidf(self, doc_id: int, query_tokens: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        for term in query_tokens:
            tf = self.term_freqs[doc_id].get(term, 0) / (doc_len if doc_len > 0 else 1)
            idf = self._compute_idf(term)
            score += tf * idf
        return score

    def _make_snippet(self, content: str, query_tokens: List[str], window: int = 40) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            return ' '.join(tokens[:window])
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = ' '.join(tokens[start:end])
        for term in query_tokens:
            snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet

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

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Conversational State Machine Fundamentals",
            "A conversational state machine manages dialogue by tracking states, transitions, and context. It enables structured conversation flow and supports turn-taking, interruption handling, and context-aware responses.",
            ["state-machine", "dialogue", "context", "turn-taking"],
            1.0
        ),
        SearchDocument(
            2,
            "Turn-Taking Management",
            "Turn-taking in dialogue systems involves detecting speaker changes, managing conversational cues, and ensuring smooth transitions between participants. Effective turn-taking prevents overlap and supports barge-in.",
            ["turn-taking", "dialogue", "speaker-change", "barge-in"],
            1.0
        ),
        SearchDocument(
            3,
            "Context Window Management",
            "Sliding context windows maintain a relevant subset of conversation history, typically the last 40 messages. This approach balances memory constraints and contextual relevance for response generation.",
            ["context-window", "history", "sliding-window", "memory"],
            1.0
        ),
        SearchDocument(
            4,
            "Response Chunking for TTS",
            "Response chunking divides long outputs into manageable segments for text-to-speech (TTS). Chunking improves intelligibility, allows for pauses, and supports prosody control in synthesized speech.",
            ["chunking", "tts", "speech", "prosody"],
            1.0
        ),
        SearchDocument(
            5,
            "SSML Markup Generation",
            "SSML (Speech Synthesis Markup Language) enables fine-grained control over speech output, including pauses, emphasis, prosody, and pronunciation. Automated SSML markup generation tailors responses for TTS engines.",
            ["ssml", "markup", "tts", "prosody"],
            1.0
        ),
        SearchDocument(
            6,
            "Pause Insertion Rules",
            "Pause insertion rules determine where and how to add pauses in speech output. Typical rules include pauses after sentences, before emphasis, and at conversational boundaries to enhance clarity.",
            ["pause", "speech", "rules", "clarity"],
            1.0
        ),
        SearchDocument(
            7,
            "Emphasis Marking in Speech Output",
            "Emphasis marking highlights key words or phrases in speech output, using SSML tags or prosody hints. Emphasis improves listener comprehension and guides attention during dialogue.",
            ["emphasis", "speech", "ssml", "prosody"],
            1.0
        ),
        SearchDocument(
            8,
            "Prosody Hints for Voice Output",
            "Prosody hints adjust pitch, rate, and volume in voice output. These hints, often encoded in SSML, make responses more natural and expressive, supporting nuanced conversational flow.",
            ["prosody", "voice", "ssml", "expressiveness"],
            1.0
        ),
        SearchDocument(
            9,
            "Response Length Optimization for Voice",
            "Optimizing response length for voice output ensures messages are concise, clear, and easy to follow. Techniques include chunking, summarization, and adaptive truncation based on context.",
            ["response-length", "voice", "optimization", "summarization"],
            1.0
        ),
        SearchDocument(
            10,
            "Multi-Part Response Assembly",
            "Multi-part response assembly combines several message segments into a coherent dialogue turn. This supports complex answers, clarifications, and follow-ups, improving conversational depth.",
            ["multi-part", "assembly", "clarification", "follow-up"],
            1.0
        ),
        SearchDocument(
            11,
            "Follow-up Question Generation",
            "Follow-up question generation creates relevant queries based on prior conversation. This technique maintains engagement, clarifies intent, and supports topic continuity in dialogue.",
            ["follow-up", "question", "generation", "engagement"],
            1.0
        ),
        SearchDocument(
            12,
            "Clarification Request Handling",
            "Clarification request handling detects ambiguous inputs and prompts for further information. This improves accuracy and user satisfaction by resolving uncertainty in conversation.",
            ["clarification", "request", "ambiguity", "accuracy"],
            1.0
        ),
        SearchDocument(
            13,
            "Conversation Summary Generation",
            "Conversation summary generation produces concise overviews of dialogue history. Summaries help users recall context, track topics, and support context window management.",
            ["summary", "generation", "history", "context"],
            1.0
        ),
        SearchDocument(
            14,
            "Topic Tracking in Dialogue",
            "Topic tracking monitors conversational subjects, identifies shifts, and maintains continuity. This enables context-aware responses and supports anaphora resolution.",
            ["topic-tracking", "dialogue", "context", "anaphora"],
            1.0
        ),
        SearchDocument(
            15,
            "Anaphora Resolution in Dialogue",
            "Anaphora resolution identifies references to prior entities or topics in conversation. This process ensures accurate interpretation of pronouns and context-dependent expressions.",
            ["anaphora", "resolution", "reference", "context"],
            1.0
        ),
        SearchDocument(
            16,
            "Conversation Flow Templates",
            "Conversation flow templates define structured dialogue patterns for common scenarios. Templates guide state transitions, turn-taking, and response generation, improving system consistency.",
            ["flow", "templates", "dialogue", "structure"],
            1.0
        ),
        SearchDocument(
            17,
            "Interruption Handling in Dialogue",
            "Interruption handling detects and manages conversational breaks, overlaps, and barge-ins. Robust interruption management preserves context and supports smooth recovery.",
            ["interruption", "handling", "barge-in", "recovery"],
            1.0
        ),
        SearchDocument(
            18,
            "Barge-In Support for Voice Output",
            "Barge-in support allows users to interrupt ongoing speech output. The system detects interruptions, halts TTS, and adapts responses to maintain conversational flow.",
            ["barge-in", "voice", "output", "interruption"],
            1.0
        ),
        SearchDocument(
            19,
            "Conversation Timeout Handling",
            "Conversation timeout handling manages periods of inactivity. The system prompts users, ends sessions gracefully, or summarizes context to maintain engagement.",
            ["timeout", "handling", "inactivity", "engagement"],
            1.0
        ),
        SearchDocument(
            20,
            "Graceful Conversation Ending",
            "Graceful conversation ending ensures polite, context-aware closure of dialogue sessions. Techniques include summarization, farewell messages, and follow-up suggestions.",
            ["ending", "graceful", "closure", "farewell"],
            1.0
        ),
        SearchDocument(
            21,
            "Sliding 40-Message Context Window",
            "A sliding window of 40 messages maintains relevant conversational context. This approach balances memory usage and ensures responses remain contextually appropriate.",
            ["sliding-window", "context", "40-message", "memory"],
            1.0
        ),
        SearchDocument(
            22,
            "Dialogue State Tracking",
            "Dialogue state tracking records the current conversational state, previous turns, and relevant entities. This enables context-aware response generation and supports state machine logic.",
            ["state-tracking", "dialogue", "entities", "context"],
            1.0
        ),
        SearchDocument(
            23,
            "Adaptive Response Chunking",
            "Adaptive response chunking tailors segment sizes based on user preferences, device capabilities, and conversational context. This improves TTS output and user experience.",
            ["adaptive", "chunking", "tts", "preferences"],
            1.0
        ),
        SearchDocument(
            24,
            "SSML Prosody Control",
            "SSML prosody control adjusts speech parameters such as pitch, rate, and volume. Fine-tuned prosody enhances expressiveness and naturalness in voice responses.",
            ["ssml", "prosody", "pitch", "rate", "volume"],
            1.0
        ),
        SearchDocument(
            25,
            "Clarification Strategies in Dialogue",
            "Clarification strategies include explicit prompts, rephrasing, and context reminders. These approaches resolve ambiguity and support effective conversational flow.",
            ["clarification", "strategies", "ambiguity", "flow"],
            1.0
        ),
        SearchDocument(
            26,
            "Conversation Recovery after Interruption",
            "Conversation recovery techniques restore context after interruptions or barge-ins. Methods include context summarization, state rollback, and user prompts.",
            ["recovery", "interruption", "context", "rollback"],
            1.0
        ),
        SearchDocument(
            27,
            "Voice Output Optimization",
            "Voice output optimization balances clarity, expressiveness, and response length. Techniques include prosody control, chunking, and adaptive SSML markup.",
            ["voice", "output", "optimization", "ssml"],
            1.0
        ),
        SearchDocument(
            28,
            "Entity Tracking in Dialogue",
            "Entity tracking monitors references to people, places, and objects in conversation. This supports anaphora resolution, context management, and response generation.",
            ["entity", "tracking", "anaphora", "context"],
            1.0
        ),
        SearchDocument(
            29,
            "Conversational Flow Management",
            "Conversational flow management orchestrates state transitions, turn-taking, and interruption handling. Flow management ensures coherent, context-aware dialogue.",
            ["flow", "management", "state", "turn-taking"],
            1.0
        ),
        SearchDocument(
            30,
            "Dialogue Template Customization",
            "Dialogue template customization adapts flow templates to specific domains, user preferences, and scenarios. Customization improves relevance and user satisfaction.",
            ["template", "customization", "dialogue", "preferences"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)