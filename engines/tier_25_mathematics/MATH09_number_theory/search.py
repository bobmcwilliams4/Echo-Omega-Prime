import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --------------------------
# Data Classes
# --------------------------

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

# --------------------------
# Search Index
# --------------------------

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)  # term -> {doc_id: freq}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.doc_freq: Dict[str, int] = defaultdict(int)
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._recompute_stats = True

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            counts = Counter(tokens)
            for term, freq in counts.items():
                self.inverted_index[term][doc.id] = freq
                self.doc_freq[term] += 1
            self.N += 1
            self._recompute_stats = True

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def _compute_avg_doc_length(self):
        if not self.doc_lengths:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / len(self.doc_lengths)

    def _compute_idf(self, term: str) -> float:
        # BM25 idf
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freq.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int, k1=1.5, b=0.75) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        if doc_len == 0:
            return 0.0
        doc = self.documents[doc_id]
        tf_doc = {}
        for term in query_terms:
            tf_doc[term] = self.inverted_index.get(term, {}).get(doc_id, 0)
        for term in set(query_terms):
            tf = tf_doc[term]
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            denom = tf + k1 * (1 - b + b * doc_len / (self.avg_doc_length if self.avg_doc_length > 0 else 1))
            score += idf * (tf * (k1 + 1)) / denom
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        if doc_len == 0:
            return 0.0
        doc = self.documents[doc_id]
        tf_doc = {}
        for term in query_terms:
            tf_doc[term] = self.inverted_index.get(term, {}).get(doc_id, 0)
        for term in set(query_terms):
            tf = tf_doc[term]
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            tf_norm = tf / doc_len
            score += tf_norm * idf
        return score * doc.weight

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avg_doc_length,
                "vocab_size": len(self.inverted_index)
            }

    def search(self, query: str, limit: int = 5) -> List[SearchResult]:
        with self.lock:
            if self._recompute_stats:
                self._compute_avg_doc_length()
                self.idf_cache.clear()
                self._recompute_stats = False

            query_terms = self._tokenize(query)
            candidate_docs = set()
            for term in query_terms:
                candidate_docs.update(self.inverted_index.get(term, {}).keys())

            scored = []
            for doc_id in candidate_docs:
                bm25_score = self._score_bm25(query_terms, doc_id)
                tfidf_score = self._score_tfidf(query_terms, doc_id)
                total_score = bm25_score + 0.5 * tfidf_score
                if total_score > 0:
                    doc = self.documents[doc_id]
                    snippet = self._make_snippet(doc, query_terms)
                    scored.append(SearchResult(doc_id, total_score, doc.title, snippet))

            scored.sort(key=lambda r: r.score, reverse=True)
            return scored[:limit]

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], maxlen: int = 180) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:maxlen]
            if len(content) > maxlen:
                snippet += "..."
            return snippet
        first = positions[0]
        start = max(0, first - 8)
        end = min(len(tokens), first + 12)
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(rf'\b({re.escape(term)})\b', r'**\1**', snippet, flags=re.I)
        if start > 0:
            snippet = "..." + snippet
        if end < len(tokens):
            snippet = snippet + "..."
        return snippet

# --------------------------
# Singleton Factory
# --------------------------

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

# --------------------------
# Domain Documents
# --------------------------

def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Fundamental Theorem of Arithmetic",
            "Every integer greater than 1 can be written uniquely as a product of prime numbers, up to the order of the factors. This is known as the Fundamental Theorem of Arithmetic.",
            ["fta", "uniqueness", "prime factorization"],
            1.2
        ),
        SearchDocument(
            2,
            "Definition of Prime Number",
            "A prime number is an integer greater than 1 that has no positive divisors other than 1 and itself.",
            ["prime", "definition"],
            1.0
        ),
        SearchDocument(
            3,
            "Primality Test: Trial Division",
            "Trial division is the simplest primality test. To check if n is prime, try dividing n by all primes less than or equal to sqrt(n). If none divide n, then n is prime.",
            ["primality test", "trial division"],
            1.0
        ),
        SearchDocument(
            4,
            "Sieve of Eratosthenes",
            "The Sieve of Eratosthenes is an efficient algorithm for finding all primes up to a given limit n. It works by iteratively marking the multiples of each prime starting from 2.",
            ["prime", "sieve", "algorithm"],
            1.0
        ),
        SearchDocument(
            5,
            "Prime Factorization Algorithm",
            "Prime factorization is the process of determining the prime numbers that multiply together to yield a given integer. Algorithms include trial division and Pollard's rho.",
            ["prime factorization", "algorithm"],
            1.1
        ),
        SearchDocument(
            6,
            "Uniqueness of Prime Factorization",
            "The uniqueness of prime factorization states that each integer greater than 1 has a unique prime decomposition, disregarding the order of the factors.",
            ["fta", "uniqueness"],
            1.2
        ),
        SearchDocument(
            7,
            "Euler's Totient Function Definition",
            "Euler's totient function φ(n) counts the number of positive integers up to n that are coprime to n.",
            ["euler", "totient", "definition"],
            1.0
        ),
        SearchDocument(
            8,
            "Formula for Euler's Totient Function",
            "If n = p1^k1 * p2^k2 * ... * pr^kr is the prime factorization of n, then φ(n) = n × Π(1 - 1/pi) over all distinct primes pi dividing n.",
            ["euler", "totient", "formula"],
            1.1
        ),
        SearchDocument(
            9,
            "Chinese Remainder Theorem Statement",
            "The Chinese Remainder Theorem states that if n1, n2, ..., nk are pairwise coprime, then the system x ≡ a1 mod n1, ..., x ≡ ak mod nk has a unique solution modulo N = n1*n2*...*nk.",
            ["crt", "congruence", "theorem"],
            1.2
        ),
        SearchDocument(
            10,
            "Chinese Remainder Theorem Example",
            "To solve x ≡ 2 mod 3, x ≡ 3 mod 5, x ≡ 2 mod 7, use the Chinese Remainder Theorem to find x modulo 105.",
            ["crt", "example"],
            1.0
        ),
        SearchDocument(
            11,
            "Greatest Common Divisor (GCD)",
            "The greatest common divisor of two integers a and b is the largest integer that divides both a and b. Euclid's algorithm efficiently computes the GCD.",
            ["gcd", "euclid", "algorithm"],
            1.0
        ),
        SearchDocument(
            12,
            "Euclid's Algorithm for GCD",
            "Euclid's algorithm computes the GCD of a and b by repeatedly replacing (a, b) with (b, a mod b) until b is zero. The last nonzero value of a is the GCD.",
            ["gcd", "euclid", "algorithm"],
            1.0
        ),
        SearchDocument(
            13,
            "Coprimality and Relatively Prime",
            "Two integers are coprime if their greatest common divisor is 1. For example, 8 and 15 are coprime.",
            ["coprime", "gcd"],
            1.0
        ),
        SearchDocument(
            14,
            "Prime Number Theorem",
            "The prime number theorem describes the asymptotic distribution of prime numbers. It states that the number of primes less than n is approximately n / log n.",
            ["prime", "distribution", "theorem"],
            1.0
        ),
        SearchDocument(
            15,
            "Fermat's Little Theorem",
            "If p is a prime and a is an integer not divisible by p, then a^(p-1) ≡ 1 mod p. This is Fermat's Little Theorem.",
            ["fermat", "theorem", "modular arithmetic"],
            1.0
        ),
        SearchDocument(
            16,
            "Miller-Rabin Primality Test",
            "The Miller-Rabin test is a probabilistic algorithm to determine if a number is likely prime. It is more efficient than trial division for large numbers.",
            ["primality test", "miller-rabin", "algorithm"],
            1.1
        ),
        SearchDocument(
            17,
            "Pollard's Rho Algorithm",
            "Pollard's rho is an efficient probabilistic algorithm for integer factorization, especially useful for numbers with small factors.",
            ["factorization", "pollard", "algorithm"],
            1.1
        ),
        SearchDocument(
            18,
            "Wilson's Theorem",
            "Wilson's theorem states that a natural number n > 1 is prime if and only if (n-1)! ≡ -1 mod n.",
            ["wilson", "theorem", "primality test"],
            1.0
        ),
        SearchDocument(
            19,
            "Applications of Euler's Totient Function",
            "Euler's totient function is used in RSA cryptography, modular inverses, and counting reduced fractions.",
            ["euler", "totient", "applications"],
            1.0
        ),
        SearchDocument(
            20,
            "Prime Gaps",
            "A prime gap is the difference between two successive prime numbers. The study of prime gaps is an active area of research in number theory.",
            ["prime", "gap", "number theory"],
            1.0
        ),
        SearchDocument(
            21,
            "General Number Theory Query",
            "Number theory is the branch of mathematics devoted to the study of the integers and their properties, including divisibility, primes, and congruences.",
            ["number theory", "integers", "divisibility"],
            1.0
        ),
        SearchDocument(
            22,
            "Prime Counting Function π(n)",
            "The prime counting function π(n) gives the number of primes less than or equal to n.",
            ["prime", "counting", "function"],
            1.0
        ),
        SearchDocument(
            23,
            "Modular Inverse",
            "The modular inverse of a modulo n is an integer x such that a*x ≡ 1 mod n. It exists if and only if a and n are coprime.",
            ["modular inverse", "congruence"],
            1.0
        ),
        SearchDocument(
            24,
            "Divisibility Rules",
            "Divisibility rules help determine if one integer divides another without performing division. For example, an integer is divisible by 3 if the sum of its digits is divisible by 3.",
            ["divisibility", "rules"],
            1.0
        ),
        SearchDocument(
            25,
            "Prime Factorization Example",
            "The prime factorization of 60 is 2 × 2 × 3 × 5. Each factor is a prime number.",
            ["prime factorization", "example"],
            1.0
        ),
        SearchDocument(
            26,
            "Solving Linear Congruences",
            "A linear congruence ax ≡ b mod n has a solution if and only if gcd(a, n) divides b. The solution can be found using the extended Euclidean algorithm.",
            ["congruence", "linear", "gcd"],
            1.0
        ),
        SearchDocument(
            27,
            "Extended Euclidean Algorithm",
            "The extended Euclidean algorithm computes the GCD of a and b and also finds integers x and y such that ax + by = gcd(a, b).",
            ["euclid", "gcd", "algorithm"],
            1.0
        ),
        SearchDocument(
            28,
            "Prime Power Factorization",
            "A prime power is a number of the form p^k, where p is prime and k is a positive integer. Prime power factorization expresses a number as a product of prime powers.",
            ["prime power", "factorization"],
            1.0
        ),
        SearchDocument(
            29,
            "RSA Cryptography and Totient Function",
            "RSA encryption relies on the difficulty of factoring large numbers and uses Euler's totient function to compute private keys.",
            ["rsa", "cryptography", "totient"],
            1.0
        ),
        SearchDocument(
            30,
            "Primitive Roots",
            "A primitive root modulo n is an integer g such that its powers generate all numbers coprime to n modulo n.",
            ["primitive root", "modular arithmetic"],
            1.0
        ),
        SearchDocument(
            31,
            "Order of an Integer Modulo n",
            "The order of an integer a modulo n is the smallest positive integer k such that a^k ≡ 1 mod n.",
            ["order", "modular arithmetic"],
            1.0
        ),
        SearchDocument(
            32,
            "Legendre Symbol",
            "The Legendre symbol (a/p) is defined for an integer a and an odd prime p and indicates whether a is a quadratic residue modulo p.",
            ["legendre", "symbol", "quadratic residue"],
            1.0
        ),
        SearchDocument(
            33,
            "Quadratic Residues",
            "A quadratic residue modulo n is an integer q such that there exists an integer x with x^2 ≡ q mod n.",
            ["quadratic residue", "modular arithmetic"],
            1.0
        ),
        SearchDocument(
            34,
            "Generalized Chinese Remainder Theorem",
            "The Chinese Remainder Theorem can be generalized to moduli that are not pairwise coprime, but the solution may not be unique.",
            ["crt", "generalized", "congruence"],
            1.0
        ),
        SearchDocument(
            35,
            "Prime Number Generation Algorithms",
            "Algorithms for generating large prime numbers include probabilistic tests like Miller-Rabin and deterministic sieves for small numbers.",
            ["prime", "generation", "algorithm"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)