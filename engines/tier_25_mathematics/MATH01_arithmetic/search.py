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
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_doc_map: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self.tf_cache: Dict[str, Dict[str, float]] = defaultdict(dict)
        self._preseeded = False

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            token_counts = Counter(tokens)
            for token, count in token_counts.items():
                self.term_doc_freq[token] += 1
                self.term_doc_map[token][doc.id] = count
            self._update_avg_doc_length()
            self.idf_cache.clear()
            self.tf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        doc_scores: Dict[str, float] = defaultdict(float)
        doc_tf_scores: Dict[str, float] = defaultdict(float)
        for token in query_tokens:
            idf = self._compute_idf(token)
            docs_with_token = self.term_doc_map.get(token, {})
            for doc_id, freq in docs_with_token.items():
                score = self._score_bm25(token, doc_id, idf)
                doc_scores[doc_id] += score
                tfidf_score = self._score_tfidf(token, doc_id)
                doc_tf_scores[doc_id] += tfidf_score
        # Combine BM25 and TF-IDF scores, weighted
        results = []
        for doc_id in doc_scores:
            bm25_score = doc_scores[doc_id]
            tfidf_score = doc_tf_scores[doc_id]
            doc = self.documents[doc_id]
            combined_score = bm25_score * 0.7 + tfidf_score * 0.3
            snippet = self._make_snippet(doc.content, query_tokens)
            results.append(SearchResult(doc_id, combined_score * doc.weight, doc.title, snippet))
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:limit]

    def get_stats(self) -> Dict[str, float]:
        return {
            "total_docs": self.total_docs,
            "avg_doc_length": self.avg_doc_length,
            "unique_terms": len(self.term_doc_freq),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r'[^a-z0-9\+\-\*/\^\(\)\[\]\{\}\.,]', ' ', text)
        tokens = re.findall(r'\b[a-z0-9\+\-\*/\^\(\)\[\]\{\}\.,]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, term: str, doc_id: str, idf: Optional[float] = None) -> float:
        if idf is None:
            idf = self._compute_idf(term)
        freq = self.term_doc_map.get(term, {}).get(doc_id, 0)
        doc_length = self.doc_lengths.get(doc_id, 1)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1
        numerator = freq * (self.k1 + 1)
        denominator = freq + self.k1 * (1 - self.b + self.b * doc_length / avg_dl)
        return idf * numerator / denominator if denominator != 0 else 0.0

    def _score_tfidf(self, term: str, doc_id: str) -> float:
        if term in self.tf_cache and doc_id in self.tf_cache[term]:
            return self.tf_cache[term][doc_id]
        freq = self.term_doc_map.get(term, {}).get(doc_id, 0)
        doc_length = self.doc_lengths.get(doc_id, 1)
        tf = freq / doc_length if doc_length > 0 else 0.0
        idf = self._compute_idf(term)
        score = tf * idf
        self.tf_cache[term][doc_id] = score
        return score

    def _update_avg_doc_length(self):
        if self.total_docs == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs

    def _make_snippet(self, content: str, query_tokens: List[str], length: int = 120) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            snippet = ' '.join(tokens[:length])
        else:
            start = max(positions[0] - 10, 0)
            end = min(start + length, len(tokens))
            snippet = ' '.join(tokens[start:end])
        snippet = snippet.strip()
        return snippet[:length] + ('...' if len(snippet) > length else '')

    def _preseed_documents(self):
        if self._preseeded:
            return
        docs = [
            SearchDocument(
                id="1",
                title="Addition and Subtraction Basics",
                content="Addition is combining two or more numbers to get a sum. Subtraction is removing one number from another to get the difference.",
                tags=["addition", "subtraction", "arithmetic", "basics"],
                weight=1.0
            ),
            SearchDocument(
                id="2",
                title="Multiplication Fundamentals",
                content="Multiplication is repeated addition. The product of two numbers is calculated by multiplying them together.",
                tags=["multiplication", "arithmetic", "product"],
                weight=1.0
            ),
            SearchDocument(
                id="3",
                title="Division Concepts",
                content="Division splits a number into equal parts. The quotient is the result of dividing one number by another.",
                tags=["division", "arithmetic", "quotient"],
                weight=1.0
            ),
            SearchDocument(
                id="4",
                title="Order of Operations",
                content="The order of operations is PEMDAS: Parentheses, Exponents, Multiplication, Division, Addition, Subtraction. Always follow this order when solving arithmetic expressions.",
                tags=["order", "operations", "PEMDAS", "arithmetic"],
                weight=1.0
            ),
            SearchDocument(
                id="5",
                title="Properties of Addition",
                content="Addition has properties: commutative (a+b=b+a), associative ((a+b)+c=a+(b+c)), and identity (a+0=a).",
                tags=["addition", "properties", "commutative", "associative", "identity"],
                weight=1.0
            ),
            SearchDocument(
                id="6",
                title="Properties of Multiplication",
                content="Multiplication is commutative (a*b=b*a), associative ((a*b)*c=a*(b*c)), distributive (a*(b+c)=a*b+a*c), and has identity (a*1=a).",
                tags=["multiplication", "properties", "commutative", "associative", "distributive", "identity"],
                weight=1.0
            ),
            SearchDocument(
                id="7",
                title="Negative Numbers in Arithmetic",
                content="Negative numbers are less than zero. Adding, subtracting, multiplying, and dividing negative numbers follows specific rules.",
                tags=["negative", "numbers", "arithmetic"],
                weight=1.0
            ),
            SearchDocument(
                id="8",
                title="Fractions and Decimals",
                content="Fractions represent parts of a whole. Decimals are another way to express fractions. Arithmetic operations can be performed on both.",
                tags=["fractions", "decimals", "arithmetic"],
                weight=1.0
            ),
            SearchDocument(
                id="9",
                title="Exponents and Powers",
                content="Exponents indicate repeated multiplication. Powers are the result of raising a base to an exponent.",
                tags=["exponents", "powers", "arithmetic"],
                weight=1.0
            ),
            SearchDocument(
                id="10",
                title="Roots and Radicals",
                content="Roots are the inverse of exponents. The square root of a number is a value that, when multiplied by itself, gives the original number.",
                tags=["roots", "radicals", "arithmetic"],
                weight=1.0
            ),
            SearchDocument(
                id="11",
                title="Estimating Arithmetic Results",
                content="Estimation helps quickly approximate arithmetic results using rounding and mental math.",
                tags=["estimation", "arithmetic", "rounding"],
                weight=1.0
            ),
            SearchDocument(
                id="12",
                title="Word Problems in Arithmetic",
                content="Word problems require translating real-world situations into arithmetic expressions to solve.",
                tags=["word problems", "arithmetic", "applications"],
                weight=1.0
            ),
            SearchDocument(
                id="13",
                title="Arithmetic Sequences",
                content="An arithmetic sequence is a list of numbers with a constant difference between consecutive terms.",
                tags=["arithmetic", "sequences", "difference"],
                weight=1.0
            ),
            SearchDocument(
                id="14",
                title="Prime Numbers and Arithmetic",
                content="Prime numbers are only divisible by 1 and themselves. They play a key role in arithmetic and number theory.",
                tags=["prime", "numbers", "arithmetic"],
                weight=1.0
            ),
            SearchDocument(
                id="15",
                title="Greatest Common Divisor (GCD)",
                content="The GCD of two numbers is the largest number that divides both. It is useful in simplifying fractions.",
                tags=["GCD", "arithmetic", "fractions"],
                weight=1.0
            ),
            SearchDocument(
                id="16",
                title="Least Common Multiple (LCM)",
                content="The LCM of two numbers is the smallest number that both can divide. It is used in addition and subtraction of fractions.",
                tags=["LCM", "arithmetic", "fractions"],
                weight=1.0
            ),
            SearchDocument(
                id="17",
                title="Estimating with Rounding",
                content="Rounding numbers makes arithmetic easier by simplifying numbers to the nearest ten, hundred, etc.",
                tags=["rounding", "arithmetic", "estimation"],
                weight=1.0
            ),
            SearchDocument(
                id="18",
                title="Mental Math Strategies",
                content="Mental math uses techniques like breaking numbers apart, using patterns, and estimation to solve arithmetic quickly.",
                tags=["mental math", "arithmetic", "strategies"],
                weight=1.0
            ),
            SearchDocument(
                id="19",
                title="Arithmetic with Percentages",
                content="Percentages are fractions out of 100. Arithmetic operations can be performed with percentages for real-world calculations.",
                tags=["percentages", "arithmetic", "fractions"],
                weight=1.0
            ),
            SearchDocument(
                id="20",
                title="Arithmetic with Money",
                content="Money arithmetic involves addition, subtraction, multiplication, and division with decimals and currency units.",
                tags=["money", "arithmetic", "decimals"],
                weight=1.0
            ),
            SearchDocument(
                id="21",
                title="Estimating Sums and Differences",
                content="Estimate sums and differences by rounding numbers before performing arithmetic operations.",
                tags=["estimation", "sums", "differences", "arithmetic"],
                weight=1.0
            ),
            SearchDocument(
                id="22",
                title="Arithmetic with Measurements",
                content="Measurements involve arithmetic with units like length, mass, and time. Conversion between units is often required.",
                tags=["measurements", "arithmetic", "units"],
                weight=1.0
            ),
            SearchDocument(
                id="23",
                title="Arithmetic Patterns",
                content="Patterns in arithmetic help predict future values and solve problems efficiently.",
                tags=["patterns", "arithmetic", "prediction"],
                weight=1.0
            ),
            SearchDocument(
                id="24",
                title="Arithmetic in Everyday Life",
                content="Arithmetic is used daily for budgeting, shopping, cooking, and planning.",
                tags=["everyday", "life", "arithmetic", "applications"],
                weight=1.0
            ),
            SearchDocument(
                id="25",
                title="Arithmetic with Large Numbers",
                content="Handling large numbers in arithmetic requires careful calculation and estimation.",
                tags=["large numbers", "arithmetic", "estimation"],
                weight=1.0
            ),
            SearchDocument(
                id="26",
                title="Arithmetic with Small Numbers",
                content="Small numbers are important in precision arithmetic, such as scientific measurements.",
                tags=["small numbers", "arithmetic", "precision"],
                weight=1.0
            ),
            SearchDocument(
                id="27",
                title="Arithmetic with Zero",
                content="Zero is the additive identity. Multiplying any number by zero gives zero. Division by zero is undefined.",
                tags=["zero", "arithmetic", "identity"],
                weight=1.0
            ),
            SearchDocument(
                id="28",
                title="Arithmetic with Powers of Ten",
                content="Powers of ten simplify arithmetic with decimals and scientific notation.",
                tags=["powers of ten", "arithmetic", "decimals"],
                weight=1.0
            ),
            SearchDocument(
                id="29",
                title="Arithmetic with Ratios",
                content="Ratios compare two quantities. Arithmetic operations can be performed on ratios to solve problems.",
                tags=["ratios", "arithmetic", "comparison"],
                weight=1.0
            ),
            SearchDocument(
                id="30",
                title="Arithmetic with Proportions",
                content="Proportions are equations that state two ratios are equal. Solving proportions involves arithmetic operations.",
                tags=["proportions", "arithmetic", "ratios"],
                weight=1.0
            ),
        ]
        for doc in docs:
            self.add_document(doc)
        self._preseeded = True

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _search_index_instance._preseed_documents()
        return _search_index_instance