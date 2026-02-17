import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

# --- Data Classes ---

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

# --- Search Index ---

class SearchIndex:
    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_tokens: Dict[str, List[str]] = {}
        self.inverted_index: Dict[str, Set[str]] = defaultdict(set)
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_doc_freqs: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._recompute_stats()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            self.documents[doc.id] = doc
            self.doc_tokens[doc.id] = tokens
            self.doc_lengths[doc.id] = len(tokens)
            for token in tokens:
                self.inverted_index[token].add(doc.id)
                self.term_doc_freqs[token][doc.id] = self.term_doc_freqs[token].get(doc.id, 0) + 1
            self.N += 1
            self._recompute_stats()

    def search(self, query: str, limit: int = 10, method: str = "bm25") -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        candidate_docs = set()
        for token in query_tokens:
            candidate_docs |= self.inverted_index.get(token, set())
        scores = {}
        for doc_id in candidate_docs:
            if method == "bm25":
                score = self._score_bm25(doc_id, query_tokens)
            elif method == "tfidf":
                score = self._score_tfidf(doc_id, query_tokens)
            else:
                score = self._score_bm25(doc_id, query_tokens)
            scores[doc_id] = score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avg_doc_length,
                "vocab_size": len(self.inverted_index)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

    def _recompute_stats(self):
        total_length = 0
        for doc_id, tokens in self.doc_tokens.items():
            total_length += len(tokens)
        self.avg_doc_length = (total_length / self.N) if self.N > 0 else 0.0
        self.doc_freqs = {token: len(docset) for token, docset in self.inverted_index.items()}
        self.idf_cache = {}
        for token in self.doc_freqs:
            self.idf_cache[token] = self._compute_idf(token)

    def _compute_idf(self, term: str) -> float:
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            return 0.0
        return math.log(1 + (self.N - df + 0.5) / (df + 0.5))

    def _score_bm25(self, doc_id: str, query_tokens: List[str], k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in set(query_tokens):
            tf = self.term_doc_freqs.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            idf = self.idf_cache.get(term, self._compute_idf(term))
            denom = tf + k1 * (1 - b + b * doc_len / (self.avg_doc_length + 1e-9))
            score += idf * tf * (k1 + 1) / (denom + 1e-9)
        return score * doc.weight

    def _score_tfidf(self, doc_id: str, query_tokens: List[str]) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tf_counter = Counter(self.doc_tokens[doc_id])
        for term in set(query_tokens):
            tf = tf_counter.get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / (doc_len + 1e-9)
            idf = self.idf_cache.get(term, self._compute_idf(term))
            score += tf_norm * idf
        return score * doc.weight

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], snippet_len: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            return content[:200] + "..." if len(content) > 200 else content
        start = max(positions[0] - snippet_len // 2, 0)
        end = min(start + snippet_len, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        return snippet + "..."

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

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id="1",
            title="Knowledge Gap Identification Algorithms",
            content="Techniques for identifying knowledge gaps include coverage analysis, knowledge graph traversal, and blind spot detection. These methods help in systematically uncovering missing or weakly understood concepts.",
            tags=["knowledge gap", "coverage analysis", "blind spot", "knowledge graph"],
            weight=1.0
        ),
        SearchDocument(
            id="2",
            title="Socratic Method for Question Formulation",
            content="The Socratic Method involves asking probing questions to stimulate critical thinking and illuminate ideas. It is effective for uncovering assumptions and deepening understanding.",
            tags=["socratic method", "question formulation", "critical thinking"],
            weight=1.0
        ),
        SearchDocument(
            id="3",
            title="Bloom's Taxonomy in Question Design",
            content="Bloom's Taxonomy categorizes cognitive skills from remembering to creating. It guides the formulation of questions that target various depths of understanding.",
            tags=["bloom taxonomy", "question design", "cognitive skills"],
            weight=1.0
        ),
        SearchDocument(
            id="4",
            title="Learning Prioritization: Impact and Urgency",
            content="Prioritizing learning objectives based on their impact and urgency ensures efficient allocation of study time and resources, maximizing learning outcomes.",
            tags=["learning prioritization", "impact", "urgency"],
            weight=1.0
        ),
        SearchDocument(
            id="5",
            title="Curiosity-Driven Exploration Bonuses",
            content="Rewarding curiosity through exploration bonuses encourages the pursuit of novel information and the discovery of unknown-unknowns in learning environments.",
            tags=["curiosity", "exploration", "bonus"],
            weight=1.0
        ),
        SearchDocument(
            id="6",
            title="Active Learning Query Selection",
            content="Active learning strategies select the most informative queries to maximize learning efficiency, often using uncertainty or expected information gain as criteria.",
            tags=["active learning", "query selection", "information gain"],
            weight=1.0
        ),
        SearchDocument(
            id="7",
            title="Uncertainty Quantification: Epistemic vs Aleatoric",
            content="Epistemic uncertainty arises from lack of knowledge, while aleatoric uncertainty is due to inherent randomness. Distinguishing between them is crucial for robust decision-making.",
            tags=["uncertainty", "epistemic", "aleatoric"],
            weight=1.0
        ),
        SearchDocument(
            id="8",
            title="Information Gain Metrics: Mutual Information & Entropy Reduction",
            content="Mutual information and entropy reduction are metrics used to quantify the value of information, guiding question selection and exploration.",
            tags=["information gain", "mutual information", "entropy"],
            weight=1.0
        ),
        SearchDocument(
            id="9",
            title="Question Taxonomy: Factual, Conceptual, Procedural, Metacognitive",
            content="Questions can be classified as factual, conceptual, procedural, or metacognitive, each serving distinct roles in the learning process.",
            tags=["question taxonomy", "factual", "conceptual", "procedural", "metacognitive"],
            weight=1.0
        ),
        SearchDocument(
            id="10",
            title="Knowledge Graph Traversal for Gap Detection",
            content="Traversing knowledge graphs helps identify disconnected nodes and missing prerequisite links, revealing knowledge gaps.",
            tags=["knowledge graph", "traversal", "gap detection"],
            weight=1.0
        ),
        SearchDocument(
            id="11",
            title="Blind Spot Detection via Coverage Analysis",
            content="Coverage analysis quantifies which areas of a domain have been explored, highlighting blind spots and guiding further study.",
            tags=["blind spot", "coverage analysis", "exploration"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="Unknown-Unknown Estimation & Calibration",
            content="Estimating unknown-unknowns involves modeling what is not yet discovered, often using calibration techniques and meta-learning.",
            tags=["unknown-unknown", "calibration", "meta-learning"],
            weight=1.0
        ),
        SearchDocument(
            id="13",
            title="Systematic Review & Meta-Analysis in Research",
            content="Systematic reviews and meta-analyses synthesize evidence across studies, providing comprehensive insights and identifying research gaps.",
            tags=["systematic review", "meta-analysis", "research"],
            weight=1.0
        ),
        SearchDocument(
            id="14",
            title="Hypothesis Generation: Abductive Reasoning",
            content="Abductive reasoning generates plausible hypotheses by inferring the best explanations from observed data.",
            tags=["hypothesis generation", "abductive reasoning"],
            weight=1.0
        ),
        SearchDocument(
            id="15",
            title="Experimental Design: A/B Testing & Multivariate",
            content="A/B testing and multivariate experiments are used to evaluate the effects of different interventions in a controlled manner.",
            tags=["experimental design", "a/b testing", "multivariate"],
            weight=1.0
        ),
        SearchDocument(
            id="16",
            title="Metacognition: Monitoring & Self-Assessment",
            content="Metacognitive strategies involve monitoring one's own understanding and assessing learning progress to adjust study tactics.",
            tags=["metacognition", "monitoring", "self-assessment"],
            weight=1.0
        ),
        SearchDocument(
            id="17",
            title="Learning Transfer: Near, Far, Analogical",
            content="Learning transfer refers to applying knowledge in new contexts. Near transfer involves similar contexts, far transfer involves different ones, and analogical transfer uses structural similarities.",
            tags=["learning transfer", "near transfer", "far transfer", "analogical"],
            weight=1.0
        ),
        SearchDocument(
            id="18",
            title="Spaced Repetition Scheduling: Leitner, SuperMemo",
            content="Spaced repetition algorithms like Leitner and SuperMemo optimize review intervals to enhance long-term retention.",
            tags=["spaced repetition", "leitner", "supermemo"],
            weight=1.0
        ),
        SearchDocument(
            id="19",
            title="Ebbinghaus Retention Modeling: The Forgetting Curve",
            content="The Ebbinghaus forgetting curve models memory decay over time, informing the scheduling of reviews for effective learning.",
            tags=["ebbinghaus", "forgetting curve", "retention"],
            weight=1.0
        ),
        SearchDocument(
            id="20",
            title="Knowledge Dependency Mapping: Prerequisite Chains",
            content="Mapping prerequisite chains clarifies dependencies among concepts, supporting personalized learning paths and gap analysis.",
            tags=["dependency mapping", "prerequisite", "knowledge mapping"],
            weight=1.0
        ),
        SearchDocument(
            id="21",
            title="Exploration vs Exploitation: Multi-Armed Bandit",
            content="The multi-armed bandit framework balances exploration of new options with exploitation of known rewards, optimizing learning strategies.",
            tags=["exploration", "exploitation", "multi-armed bandit"],
            weight=1.0
        ),
        SearchDocument(
            id="22",
            title="Thompson Sampling in Exploration-Exploitation",
            content="Thompson Sampling is a Bayesian method for balancing exploration and exploitation in sequential decision-making.",
            tags=["thompson sampling", "exploration", "exploitation"],
            weight=1.0
        ),
        SearchDocument(
            id="23",
            title="Upper Confidence Bound (UCB) Algorithms",
            content="UCB algorithms select actions based on upper confidence bounds, ensuring sufficient exploration while maximizing reward.",
            tags=["ucb", "upper confidence bound", "exploration"],
            weight=1.0
        ),
        SearchDocument(
            id="24",
            title="Meta-Learning for Adaptive Knowledge Gap Detection",
            content="Meta-learning enables adaptive strategies for identifying and addressing knowledge gaps across diverse domains.",
            tags=["meta-learning", "adaptive", "knowledge gap"],
            weight=1.0
        ),
        SearchDocument(
            id="25",
            title="Coverage Analysis for Blind Spot Detection",
            content="Analyzing domain coverage helps in detecting blind spots and prioritizing areas for further investigation.",
            tags=["coverage analysis", "blind spot", "domain coverage"],
            weight=1.0
        ),
        SearchDocument(
            id="26",
            title="Analogical Reasoning in Learning Transfer",
            content="Analogical reasoning supports far transfer by mapping structural similarities between different domains.",
            tags=["analogical reasoning", "learning transfer", "far transfer"],
            weight=1.0
        ),
        SearchDocument(
            id="27",
            title="Procedural Knowledge Assessment",
            content="Assessing procedural knowledge focuses on evaluating the ability to perform tasks and apply methods.",
            tags=["procedural knowledge", "assessment", "skills"],
            weight=1.0
        ),
        SearchDocument(
            id="28",
            title="Factual vs Conceptual Questioning",
            content="Factual questions test recall of information, while conceptual questions assess understanding of relationships and principles.",
            tags=["factual", "conceptual", "questioning"],
            weight=1.0
        ),
        SearchDocument(
            id="29",
            title="Self-Assessment Techniques in Metacognition",
            content="Effective self-assessment methods enhance metacognitive awareness and guide learning adjustments.",
            tags=["self-assessment", "metacognition", "learning"],
            weight=1.0
        ),
        SearchDocument(
            id="30",
            title="Entropy Reduction in Active Learning",
            content="Selecting queries that maximize entropy reduction accelerates the acquisition of new knowledge.",
            tags=["entropy reduction", "active learning", "query selection"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)