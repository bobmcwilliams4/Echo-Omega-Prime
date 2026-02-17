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
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_tokens: Dict[str, List[str]] = {}
        self.inverted_index: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.total_docs: int = 0
        self.tf_cache: Dict[str, Dict[str, float]] = defaultdict(dict)
        self._preseed_documents()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_tokens[doc.id] = tokens
            self.doc_lengths[doc.id] = len(tokens)
            for token in tokens:
                self.inverted_index[token][doc.id] = self.inverted_index[token].get(doc.id, 0) + 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0
            self.idf_cache.clear()
            self.tf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        scores = defaultdict(float)
        doc_snippets = {}
        for token in query_tokens:
            idf = self._compute_idf(token)
            for doc_id, freq in self.inverted_index.get(token, {}).items():
                doc = self.documents[doc_id]
                score = self._score_bm25(token, doc_id, freq, idf, doc.weight)
                scores[doc_id] += score
                if doc_id not in doc_snippets:
                    doc_snippets[doc_id] = self._make_snippet(doc.content, token)
        # TF-IDF scoring
        tfidf_scores = self._score_tfidf(query_tokens)
        for doc_id, tfidf_score in tfidf_scores.items():
            scores[doc_id] += tfidf_score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = doc_snippets.get(doc_id, self._make_snippet(doc.content, query_tokens[0] if query_tokens else ''))
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_documents': self.total_docs,
            'average_document_length': self.avg_doc_length,
            'unique_terms': len(self.inverted_index),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        N = self.total_docs
        n_q = len(self.inverted_index.get(term, {}))
        idf = math.log(1 + (N - n_q + 0.5) / (n_q + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, term: str, doc_id: str, freq: int, idf: float, weight: float) -> float:
        k1 = 1.5
        b = 0.75
        doc_length = self.doc_lengths[doc_id]
        avg_doc_length = self.avg_doc_length if self.avg_doc_length > 0 else 1
        numerator = freq * (k1 + 1)
        denominator = freq + k1 * (1 - b + b * doc_length / avg_doc_length)
        score = idf * (numerator / denominator) * weight
        return score

    def _score_tfidf(self, query_tokens: List[str]) -> Dict[str, float]:
        tfidf_scores = defaultdict(float)
        for term in query_tokens:
            idf = self._compute_idf(term)
            for doc_id in self.inverted_index.get(term, {}):
                tf = self._compute_tf(term, doc_id)
                tfidf_scores[doc_id] += tf * idf
        return tfidf_scores

    def _compute_tf(self, term: str, doc_id: str) -> float:
        if term in self.tf_cache and doc_id in self.tf_cache[term]:
            return self.tf_cache[term][doc_id]
        freq = self.inverted_index.get(term, {}).get(doc_id, 0)
        doc_length = self.doc_lengths.get(doc_id, 1)
        tf = freq / doc_length
        self.tf_cache[term][doc_id] = tf
        return tf

    def _make_snippet(self, content: str, term: str, window: int = 40) -> str:
        content_lower = content.lower()
        term_lower = term.lower()
        idx = content_lower.find(term_lower)
        if idx == -1:
            return content[:window] + '...' if len(content) > window else content
        start = max(0, idx - window // 2)
        end = min(len(content), idx + window // 2)
        snippet = content[start:end]
        return '...' + snippet + '...' if start > 0 else snippet + '...'

    def _preseed_documents(self):
        docs = [
            SearchDocument(
                id="doc1",
                title="Descriptive Statistics Overview",
                content="Descriptive statistics summarize and describe the features of a dataset. Measures include mean, median, mode, variance, and standard deviation.",
                tags=["descriptive", "summary", "central tendency"],
                weight=1.0
            ),
            SearchDocument(
                id="doc2",
                title="Inferential Statistics Introduction",
                content="Inferential statistics allow us to make predictions or inferences about a population based on a sample. Common methods include hypothesis testing and confidence intervals.",
                tags=["inferential", "hypothesis", "confidence interval"],
                weight=1.0
            ),
            SearchDocument(
                id="doc3",
                title="Mean, Median, and Mode",
                content="Mean is the average value, median is the middle value, and mode is the most frequent value in a dataset. These are measures of central tendency.",
                tags=["mean", "median", "mode", "central tendency"],
                weight=1.0
            ),
            SearchDocument(
                id="doc4",
                title="Variance and Standard Deviation",
                content="Variance measures the spread of data points. Standard deviation is the square root of variance and indicates how much values deviate from the mean.",
                tags=["variance", "standard deviation", "spread"],
                weight=1.0
            ),
            SearchDocument(
                id="doc5",
                title="Probability Distributions",
                content="Probability distributions describe how probabilities are distributed over values. Examples include normal, binomial, and Poisson distributions.",
                tags=["probability", "distribution", "normal", "binomial", "poisson"],
                weight=1.0
            ),
            SearchDocument(
                id="doc6",
                title="Normal Distribution",
                content="The normal distribution is a symmetric, bell-shaped curve characterized by its mean and standard deviation. It is widely used in statistics.",
                tags=["normal distribution", "bell curve", "mean", "standard deviation"],
                weight=1.0
            ),
            SearchDocument(
                id="doc7",
                title="Binomial Distribution",
                content="The binomial distribution models the number of successes in a fixed number of independent Bernoulli trials. Parameters are n and p.",
                tags=["binomial", "bernoulli", "success", "trial"],
                weight=1.0
            ),
            SearchDocument(
                id="doc8",
                title="Poisson Distribution",
                content="Poisson distribution models the number of events occurring in a fixed interval of time or space. It is used for rare events.",
                tags=["poisson", "rare event", "interval"],
                weight=1.0
            ),
            SearchDocument(
                id="doc9",
                title="Hypothesis Testing",
                content="Hypothesis testing evaluates whether a statement about a population parameter is true. Steps include stating hypotheses, choosing significance level, and making a decision.",
                tags=["hypothesis", "testing", "significance", "decision"],
                weight=1.0
            ),
            SearchDocument(
                id="doc10",
                title="Confidence Intervals",
                content="A confidence interval gives a range of values for a population parameter. It is calculated from sample data and associated with a confidence level.",
                tags=["confidence interval", "range", "parameter"],
                weight=1.0
            ),
            SearchDocument(
                id="doc11",
                title="Correlation and Covariance",
                content="Correlation measures the relationship between two variables. Covariance indicates the direction of the linear relationship.",
                tags=["correlation", "covariance", "relationship"],
                weight=1.0
            ),
            SearchDocument(
                id="doc12",
                title="Regression Analysis",
                content="Regression analysis estimates relationships among variables. Linear regression predicts a dependent variable based on independent variables.",
                tags=["regression", "linear", "dependent", "independent"],
                weight=1.0
            ),
            SearchDocument(
                id="doc13",
                title="Sampling Methods",
                content="Sampling methods include random, stratified, and cluster sampling. Proper sampling is crucial for valid statistical inference.",
                tags=["sampling", "random", "stratified", "cluster"],
                weight=1.0
            ),
            SearchDocument(
                id="doc14",
                title="Central Limit Theorem",
                content="The central limit theorem states that the sampling distribution of the sample mean approaches a normal distribution as sample size increases.",
                tags=["central limit theorem", "sampling", "normal distribution"],
                weight=1.0
            ),
            SearchDocument(
                id="doc15",
                title="Law of Large Numbers",
                content="The law of large numbers states that as the sample size increases, the sample mean approaches the population mean.",
                tags=["law of large numbers", "sample", "population"],
                weight=1.0
            ),
            SearchDocument(
                id="doc16",
                title="Outliers and Robust Statistics",
                content="Outliers are extreme values that can affect statistical analyses. Robust statistics are resistant to outliers.",
                tags=["outlier", "robust", "extreme", "resistant"],
                weight=1.0
            ),
            SearchDocument(
                id="doc17",
                title="Nonparametric Methods",
                content="Nonparametric methods do not assume a specific distribution. Examples include the Wilcoxon test and Kruskal-Wallis test.",
                tags=["nonparametric", "wilcoxon", "kruskal-wallis"],
                weight=1.0
            ),
            SearchDocument(
                id="doc18",
                title="Bayesian Statistics",
                content="Bayesian statistics use probability to represent uncertainty in parameters. Prior and posterior distributions are central concepts.",
                tags=["bayesian", "prior", "posterior", "uncertainty"],
                weight=1.0
            ),
            SearchDocument(
                id="doc19",
                title="Maximum Likelihood Estimation",
                content="Maximum likelihood estimation finds parameter values that maximize the likelihood of observed data.",
                tags=["maximum likelihood", "estimation", "parameter"],
                weight=1.0
            ),
            SearchDocument(
                id="doc20",
                title="ANOVA (Analysis of Variance)",
                content="ANOVA tests whether means of several groups are equal. It is used to analyze differences among group means.",
                tags=["anova", "variance", "group", "mean"],
                weight=1.0
            ),
            SearchDocument(
                id="doc21",
                title="Chi-Square Test",
                content="The chi-square test assesses whether observed frequencies differ from expected frequencies. It is used for categorical data.",
                tags=["chi-square", "frequency", "categorical"],
                weight=1.0
            ),
            SearchDocument(
                id="doc22",
                title="Statistical Power",
                content="Statistical power is the probability of detecting an effect if it exists. It depends on sample size, effect size, and significance level.",
                tags=["power", "effect", "sample size", "significance"],
                weight=1.0
            ),
            SearchDocument(
                id="doc23",
                title="P-Value Interpretation",
                content="The p-value is the probability of observing data as extreme as the sample, assuming the null hypothesis is true.",
                tags=["p-value", "null hypothesis", "probability"],
                weight=1.0
            ),
            SearchDocument(
                id="doc24",
                title="Type I and Type II Errors",
                content="Type I error is rejecting a true null hypothesis. Type II error is failing to reject a false null hypothesis.",
                tags=["type I error", "type II error", "null hypothesis"],
                weight=1.0
            ),
            SearchDocument(
                id="doc25",
                title="Statistical Significance",
                content="Statistical significance indicates whether an observed effect is likely due to chance. It is determined by the p-value and significance level.",
                tags=["statistical significance", "effect", "chance", "p-value"],
                weight=1.0
            ),
            SearchDocument(
                id="doc26",
                title="Data Visualization in Statistics",
                content="Data visualization helps to understand and communicate statistical results. Common plots include histograms, boxplots, and scatterplots.",
                tags=["visualization", "histogram", "boxplot", "scatterplot"],
                weight=1.0
            ),
            SearchDocument(
                id="doc27",
                title="Parametric vs. Nonparametric Tests",
                content="Parametric tests assume underlying distributions. Nonparametric tests do not. Choice depends on data characteristics.",
                tags=["parametric", "nonparametric", "test", "distribution"],
                weight=1.0
            ),
            SearchDocument(
                id="doc28",
                title="Resampling Methods",
                content="Resampling methods such as bootstrap and permutation tests are used to assess variability and significance.",
                tags=["resampling", "bootstrap", "permutation"],
                weight=1.0
            ),
            SearchDocument(
                id="doc29",
                title="Statistical Modeling",
                content="Statistical modeling uses mathematical models to represent data and relationships. Examples include linear and logistic regression.",
                tags=["modeling", "linear regression", "logistic regression"],
                weight=1.0
            ),
            SearchDocument(
                id="doc30",
                title="Multivariate Statistics",
                content="Multivariate statistics analyze data with more than one variable. Techniques include principal component analysis and factor analysis.",
                tags=["multivariate", "principal component", "factor analysis"],
                weight=1.0
            ),
        ]
        for doc in docs:
            self.add_document(doc)

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    if _search_index_instance is None:
        with _search_index_lock:
            if _search_index_instance is None:
                _search_index_instance = SearchIndex()
    return _search_index_instance