import math
import threading
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
    def __init__(self):
        self._documents: Dict[str, SearchDocument] = {}
        self._doc_freqs: Dict[str, int] = defaultdict(int)
        self._inverted_index: Dict[str, Dict[str, int]] = defaultdict(dict)
        self._doc_lengths: Dict[str, int] = {}
        self._avgdl: float = 0.0
        self._total_docs: int = 0
        self._lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_norms: Dict[str, float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            term_counts = Counter(tokens)
            self._documents[doc.id] = doc
            self._doc_lengths[doc.id] = len(tokens)
            for term, count in term_counts.items():
                self._inverted_index[term][doc.id] = count
                self._doc_freqs[term] += 1
            self._total_docs += 1
            self._avgdl = sum(self._doc_lengths.values()) / self._total_docs
            self._idf_cache.clear()
            self._tfidf_norms.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        candidate_docs = set()
        for token in query_tokens:
            candidate_docs.update(self._inverted_index.get(token, {}).keys())
        scores: Dict[str, float] = {}
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(query_tokens, doc_id)
            tfidf_score = self._score_tfidf(query_tokens, doc_id)
            doc = self._documents[doc_id]
            score = bm25_score * 0.7 + tfidf_score * 0.3
            score *= doc.weight
            scores[doc_id] = score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self._documents[doc_id]
            snippet = self._make_snippet(doc, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, int]:
        return {
            "documents": self._total_docs,
            "unique_terms": len(self._inverted_index),
            "avg_doc_length": int(self._avgdl),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self._doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self._total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_tokens: List[str], doc_id: str) -> float:
        score = 0.0
        doc_len = self._doc_lengths.get(doc_id, 0)
        avgdl = self._avgdl if self._avgdl > 0 else 1
        for term in set(query_tokens):
            tf = self._inverted_index.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            num = tf * (self._bm25_k1 + 1)
            denom = tf + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / avgdl)
            score += idf * num / denom
        return score

    def _score_tfidf(self, query_tokens: List[str], doc_id: str) -> float:
        # Compute normalized TF-IDF cosine similarity
        doc_vec = []
        query_vec = []
        doc_len = self._doc_lengths.get(doc_id, 0)
        if doc_len == 0:
            return 0.0
        term_counts = self._inverted_index
        doc_terms = term_counts.keys()
        doc_tf = {term: term_counts[term].get(doc_id, 0) for term in query_tokens}
        norm = self._tfidf_norms.get(doc_id)
        if norm is None:
            norm = 0.0
            for term in doc_terms:
                tf = term_counts[term].get(doc_id, 0)
                if tf == 0:
                    continue
                idf = self._compute_idf(term)
                norm += (tf / doc_len * idf) ** 2
            norm = math.sqrt(norm) if norm > 0 else 1.0
            self._tfidf_norms[doc_id] = norm
        for term in query_tokens:
            tf = doc_tf.get(term, 0) / doc_len if doc_len > 0 else 0
            idf = self._compute_idf(term)
            doc_vec.append(tf * idf)
            query_vec.append(idf)
        dot = sum(d * q for d, q in zip(doc_vec, query_vec))
        query_norm = math.sqrt(sum(q ** 2 for q in query_vec)) or 1.0
        return dot / (norm * query_norm)

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], maxlen: int = 160) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            snippet = content[:maxlen] + "..." if len(content) > maxlen else content
            return snippet
        start = max(positions[0] - 5, 0)
        end = min(start + 20, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        # Highlight query terms
        for qt in set(query_tokens):
            snippet = re.sub(r'\b({})\b'.format(re.escape(qt)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet

# Singleton factory for SearchIndex
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
            id="1",
            title="Probability Basics",
            content="Probability is the measure of the likelihood that an event will occur. It ranges from 0 to 1.",
            tags=["probability", "basics", "event", "likelihood"],
            weight=1.0
        ),
        SearchDocument(
            id="2",
            title="Sample Space and Events",
            content="The sample space is the set of all possible outcomes. An event is a subset of the sample space.",
            tags=["sample space", "events", "outcomes"],
            weight=1.0
        ),
        SearchDocument(
            id="3",
            title="Classical Probability",
            content="Classical probability defines the probability of an event as the ratio of favorable outcomes to the total number of equally likely outcomes.",
            tags=["classical probability", "favorable outcomes", "equally likely"],
            weight=1.0
        ),
        SearchDocument(
            id="4",
            title="Empirical Probability",
            content="Empirical probability is based on observed data, calculated as the ratio of the number of times an event occurs to the total number of trials.",
            tags=["empirical probability", "observed data", "trials"],
            weight=1.0
        ),
        SearchDocument(
            id="5",
            title="Axioms of Probability",
            content="The three axioms of probability are: non-negativity, normalization, and additivity.",
            tags=["axioms", "non-negativity", "normalization", "additivity"],
            weight=1.0
        ),
        SearchDocument(
            id="6",
            title="Addition Rule",
            content="The addition rule states that the probability of the union of two events is the sum of their probabilities minus the probability of their intersection.",
            tags=["addition rule", "union", "intersection"],
            weight=1.0
        ),
        SearchDocument(
            id="7",
            title="Multiplication Rule",
            content="The multiplication rule is used to find the probability that two events both occur. For independent events, multiply their probabilities.",
            tags=["multiplication rule", "independent events"],
            weight=1.0
        ),
        SearchDocument(
            id="8",
            title="Conditional Probability",
            content="Conditional probability is the probability of an event given that another event has occurred.",
            tags=["conditional probability", "given", "dependent"],
            weight=1.0
        ),
        SearchDocument(
            id="9",
            title="Independent Events",
            content="Two events are independent if the occurrence of one does not affect the probability of the other.",
            tags=["independent events", "probability", "occurrence"],
            weight=1.0
        ),
        SearchDocument(
            id="10",
            title="Dependent Events",
            content="Dependent events are events where the occurrence of one affects the probability of the other.",
            tags=["dependent events", "probability", "occurrence"],
            weight=1.0
        ),
        SearchDocument(
            id="11",
            title="Mutually Exclusive Events",
            content="Events are mutually exclusive if they cannot both occur at the same time.",
            tags=["mutually exclusive", "events", "probability"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="Complementary Events",
            content="The complement of an event is the set of outcomes in the sample space that are not in the event.",
            tags=["complementary events", "sample space"],
            weight=1.0
        ),
        SearchDocument(
            id="13",
            title="Law of Total Probability",
            content="The law of total probability relates marginal probabilities to conditional probabilities.",
            tags=["law of total probability", "marginal", "conditional"],
            weight=1.0
        ),
        SearchDocument(
            id="14",
            title="Bayes' Theorem",
            content="Bayes' theorem describes the probability of an event, based on prior knowledge of conditions related to the event.",
            tags=["bayes theorem", "conditional probability", "prior"],
            weight=1.0
        ),
        SearchDocument(
            id="15",
            title="Random Variables",
            content="A random variable is a variable whose possible values are numerical outcomes of a random phenomenon.",
            tags=["random variable", "outcomes", "probability"],
            weight=1.0
        ),
        SearchDocument(
            id="16",
            title="Discrete Random Variables",
            content="Discrete random variables take on a countable number of distinct values.",
            tags=["discrete random variable", "countable", "values"],
            weight=1.0
        ),
        SearchDocument(
            id="17",
            title="Continuous Random Variables",
            content="Continuous random variables can take any value in a given interval.",
            tags=["continuous random variable", "interval", "values"],
            weight=1.0
        ),
        SearchDocument(
            id="18",
            title="Probability Distribution",
            content="A probability distribution assigns probabilities to each possible value of a random variable.",
            tags=["probability distribution", "random variable"],
            weight=1.0
        ),
        SearchDocument(
            id="19",
            title="Cumulative Distribution Function",
            content="The cumulative distribution function (CDF) gives the probability that a random variable is less than or equal to a certain value.",
            tags=["cdf", "cumulative distribution", "random variable"],
            weight=1.0
        ),
        SearchDocument(
            id="20",
            title="Expected Value",
            content="The expected value is the long-run average value of repetitions of the experiment it represents.",
            tags=["expected value", "mean", "average"],
            weight=1.0
        ),
        SearchDocument(
            id="21",
            title="Variance and Standard Deviation",
            content="Variance measures the spread of a set of numbers. Standard deviation is the square root of variance.",
            tags=["variance", "standard deviation", "spread"],
            weight=1.0
        ),
        SearchDocument(
            id="22",
            title="Bernoulli Trials",
            content="A Bernoulli trial is a random experiment with exactly two possible outcomes: success and failure.",
            tags=["bernoulli trial", "success", "failure"],
            weight=1.0
        ),
        SearchDocument(
            id="23",
            title="Binomial Distribution",
            content="The binomial distribution models the number of successes in a fixed number of independent Bernoulli trials.",
            tags=["binomial distribution", "bernoulli", "successes"],
            weight=1.0
        ),
        SearchDocument(
            id="24",
            title="Geometric Distribution",
            content="The geometric distribution models the number of trials needed for the first success in repeated, independent Bernoulli trials.",
            tags=["geometric distribution", "bernoulli", "trials"],
            weight=1.0
        ),
        SearchDocument(
            id="25",
            title="Poisson Distribution",
            content="The Poisson distribution models the number of times an event occurs in a fixed interval of time or space.",
            tags=["poisson distribution", "events", "interval"],
            weight=1.0
        ),
        SearchDocument(
            id="26",
            title="Uniform Distribution",
            content="A uniform distribution assigns equal probability to all outcomes in a finite sample space.",
            tags=["uniform distribution", "equal probability"],
            weight=1.0
        ),
        SearchDocument(
            id="27",
            title="Normal Distribution",
            content="The normal distribution is a continuous probability distribution characterized by its bell-shaped curve.",
            tags=["normal distribution", "bell curve", "continuous"],
            weight=1.0
        ),
        SearchDocument(
            id="28",
            title="Central Limit Theorem",
            content="The central limit theorem states that the sum of a large number of independent random variables is approximately normally distributed.",
            tags=["central limit theorem", "normal distribution", "random variables"],
            weight=1.0
        ),
        SearchDocument(
            id="29",
            title="Joint Probability",
            content="Joint probability is the probability of two events happening at the same time.",
            tags=["joint probability", "events", "simultaneous"],
            weight=1.0
        ),
        SearchDocument(
            id="30",
            title="Marginal Probability",
            content="Marginal probability is the probability of an event irrespective of the outcome of another variable.",
            tags=["marginal probability", "event", "variable"],
            weight=1.0
        ),
        SearchDocument(
            id="31",
            title="Covariance and Correlation",
            content="Covariance measures how two variables change together. Correlation is a normalized measure of covariance.",
            tags=["covariance", "correlation", "variables"],
            weight=1.0
        ),
        SearchDocument(
            id="32",
            title="Probability Trees",
            content="Probability trees are diagrams that help visualize all possible outcomes of a sequence of events.",
            tags=["probability trees", "outcomes", "sequence"],
            weight=1.0
        ),
        SearchDocument(
            id="33",
            title="Permutations and Combinations",
            content="Permutations and combinations are counting techniques used to determine the number of possible arrangements or selections.",
            tags=["permutations", "combinations", "counting"],
            weight=1.0
        ),
        SearchDocument(
            id="34",
            title="Hypergeometric Distribution",
            content="The hypergeometric distribution models successes in draws without replacement from a finite population.",
            tags=["hypergeometric distribution", "successes", "population"],
            weight=1.0
        ),
        SearchDocument(
            id="35",
            title="Chebyshev's Inequality",
            content="Chebyshev's inequality gives an upper bound on the probability that the value of a random variable deviates from its mean.",
            tags=["chebyshev", "inequality", "random variable"],
            weight=1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)