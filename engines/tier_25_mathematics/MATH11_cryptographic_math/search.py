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
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_lengths: Dict[int, int] = {}
        self.doc_tag_index: Dict[str, List[int]] = defaultdict(list)
        self.total_docs: int = 0
        self.avg_doc_length: float = 0.0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._preseeded = False

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            token_counts = Counter(tokens)
            for token, count in token_counts.items():
                self.inverted_index[token][doc.id] = count
            for tag in doc.tags:
                self.doc_tag_index[tag.lower()].append(doc.id)
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs else 0.0
            self.idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = len(self.inverted_index.get(term, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int, k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        avgdl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        doc = self.documents[doc_id]
        for term in query_terms:
            tf = self.inverted_index.get(term, {}).get(doc_id, 0)
            idf = self._compute_idf(term)
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * doc_length / avgdl)
            if denominator == 0:
                continue
            score += idf * (numerator / denominator)
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        doc = self.documents[doc_id]
        for term in query_terms:
            tf = self.inverted_index.get(term, {}).get(doc_id, 0)
            if doc_length == 0:
                continue
            norm_tf = tf / doc_length
            idf = self._compute_idf(term)
            score += norm_tf * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, {}).keys())
        scored_results: List[Tuple[int, float]] = []
        for doc_id in candidate_docs:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                scored_results.append((doc_id, score))
        scored_results.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored_results[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], max_length: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = ' '.join(tokens[:max_length])
        else:
            start = max(positions[0] - 10, 0)
            end = min(start + max_length, len(tokens))
            snippet = ' '.join(tokens[start:end])
        return snippet[:max_length] + ('...' if len(snippet) > max_length else '')

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_documents': self.total_docs,
            'average_document_length': self.avg_doc_length,
            'unique_terms': len(self.inverted_index),
        }

    def _preseed_documents(self):
        if self._preseeded:
            return
        docs = [
            SearchDocument(
                1,
                "Elliptic Curve Cryptography Fundamentals",
                "Elliptic curve cryptography (ECC) uses algebraic structures of elliptic curves over finite fields for secure key exchange and digital signatures.",
                ["ECC", "finite fields", "key exchange", "digital signatures"],
                1.0
            ),
            SearchDocument(
                2,
                "RSA Algorithm and Number Theory",
                "RSA relies on the difficulty of factoring large integers. It uses Euler's totient function and modular exponentiation for encryption and decryption.",
                ["RSA", "number theory", "modular exponentiation", "totient"],
                1.0
            ),
            SearchDocument(
                3,
                "Discrete Logarithm Problem in Cryptography",
                "The discrete logarithm problem forms the basis for the security of Diffie-Hellman and ElGamal cryptosystems. It is hard to compute log_g(h) in finite groups.",
                ["discrete logarithm", "Diffie-Hellman", "ElGamal", "finite groups"],
                1.0
            ),
            SearchDocument(
                4,
                "Prime Number Generation for Cryptosystems",
                "Cryptographic algorithms require large prime numbers. Probabilistic primality tests like Miller-Rabin are used for efficient generation.",
                ["prime generation", "primality test", "Miller-Rabin", "cryptosystems"],
                1.0
            ),
            SearchDocument(
                5,
                "Hash Functions and Collision Resistance",
                "Hash functions map data to fixed-size values. Collision resistance ensures no two inputs produce the same hash, crucial for digital signatures.",
                ["hash functions", "collision resistance", "digital signatures"],
                1.0
            ),
            SearchDocument(
                6,
                "Modular Arithmetic in Cryptography",
                "Modular arithmetic underpins many cryptographic operations, including modular addition, multiplication, and exponentiation.",
                ["modular arithmetic", "modular exponentiation", "cryptography"],
                1.0
            ),
            SearchDocument(
                7,
                "Symmetric vs Asymmetric Encryption",
                "Symmetric encryption uses the same key for encryption and decryption, while asymmetric encryption uses public and private key pairs.",
                ["symmetric encryption", "asymmetric encryption", "public key", "private key"],
                1.0
            ),
            SearchDocument(
                8,
                "Diffie-Hellman Key Exchange",
                "Diffie-Hellman enables secure key exchange over insecure channels using modular exponentiation and the discrete logarithm problem.",
                ["Diffie-Hellman", "key exchange", "modular exponentiation"],
                1.0
            ),
            SearchDocument(
                9,
                "Cryptographic Protocols and Zero-Knowledge Proofs",
                "Zero-knowledge proofs allow one party to prove knowledge of a secret without revealing it. Used in authentication and privacy-preserving protocols.",
                ["zero-knowledge proofs", "authentication", "privacy"],
                1.0
            ),
            SearchDocument(
                10,
                "Block Ciphers and Modes of Operation",
                "Block ciphers encrypt fixed-size blocks of data. Modes of operation like CBC, ECB, and CTR define how blocks are processed.",
                ["block cipher", "CBC", "ECB", "CTR", "modes of operation"],
                1.0
            ),
            SearchDocument(
                11,
                "Public Key Infrastructure (PKI)",
                "PKI manages digital certificates and public keys. It enables secure communication and authentication in networks.",
                ["PKI", "digital certificates", "public keys", "authentication"],
                1.0
            ),
            SearchDocument(
                12,
                "Digital Signatures and Verification",
                "Digital signatures use asymmetric cryptography to verify authenticity and integrity of messages. Algorithms include RSA and ECDSA.",
                ["digital signatures", "verification", "RSA", "ECDSA"],
                1.0
            ),
            SearchDocument(
                13,
                "Cryptanalysis and Attack Models",
                "Cryptanalysis studies methods to break cryptographic systems. Attack models include brute-force, side-channel, and chosen-ciphertext attacks.",
                ["cryptanalysis", "attack models", "side-channel", "brute-force"],
                1.0
            ),
            SearchDocument(
                14,
                "Random Number Generation in Cryptography",
                "Secure random number generators are essential for key generation, initialization vectors, and nonces in cryptographic protocols.",
                ["random number generation", "key generation", "nonces"],
                1.0
            ),
            SearchDocument(
                15,
                "Mathematical Foundations of Hashing",
                "Hashing relies on mathematical properties like avalanche effect and uniform distribution to ensure unpredictability.",
                ["hashing", "avalanche effect", "uniform distribution"],
                1.0
            ),
            SearchDocument(
                16,
                "Lattice-Based Cryptography",
                "Lattice-based cryptography offers post-quantum security. It relies on hard problems like shortest vector and learning with errors.",
                ["lattice", "post-quantum", "learning with errors", "shortest vector"],
                1.0
            ),
            SearchDocument(
                17,
                "Homomorphic Encryption",
                "Homomorphic encryption allows computations on encrypted data without decryption. Useful for privacy-preserving cloud computing.",
                ["homomorphic encryption", "privacy", "cloud computing"],
                1.0
            ),
            SearchDocument(
                18,
                "Mathematical Proofs in Cryptographic Security",
                "Security proofs use reductionist arguments, showing breaking a scheme implies solving a hard mathematical problem.",
                ["security proofs", "reduction", "hard problems"],
                1.0
            ),
            SearchDocument(
                19,
                "Finite Fields and Galois Theory",
                "Finite fields, also known as Galois fields, are used in ECC and error-correcting codes. They have prime power order.",
                ["finite fields", "Galois theory", "ECC", "error-correcting codes"],
                1.0
            ),
            SearchDocument(
                20,
                "Cryptographic Hash Algorithms: SHA Family",
                "SHA algorithms (SHA-1, SHA-2, SHA-3) are widely used for hashing. They differ in structure, security, and performance.",
                ["SHA", "hash algorithms", "SHA-1", "SHA-2", "SHA-3"],
                1.0
            ),
            SearchDocument(
                21,
                "Mathematics of Key Exchange Protocols",
                "Key exchange protocols rely on mathematical operations in groups, rings, and fields to securely establish shared secrets.",
                ["key exchange", "groups", "rings", "fields"],
                1.0
            ),
            SearchDocument(
                22,
                "Quantum Computing and Cryptography",
                "Quantum algorithms like Shor's threaten classical cryptography. Post-quantum schemes use lattices, codes, and multivariate polynomials.",
                ["quantum computing", "Shor's algorithm", "post-quantum", "lattices"],
                1.0
            ),
            SearchDocument(
                23,
                "Mathematical Analysis of Stream Ciphers",
                "Stream ciphers generate keystreams using mathematical functions. Security depends on unpredictability and resistance to correlation attacks.",
                ["stream cipher", "keystream", "correlation attacks"],
                1.0
            ),
            SearchDocument(
                24,
                "Algebraic Attacks on Cryptosystems",
                "Algebraic attacks exploit mathematical structure in cryptosystems, solving equations to recover keys.",
                ["algebraic attacks", "cryptosystems", "equations"],
                1.0
            ),
            SearchDocument(
                25,
                "Mathematical Structure of One-Way Functions",
                "One-way functions are easy to compute but hard to invert. They are foundational for hash functions and public-key cryptography.",
                ["one-way functions", "hash functions", "public-key"],
                1.0
            ),
            SearchDocument(
                26,
                "Mathematics of Authentication Protocols",
                "Authentication protocols use challenge-response and mathematical proofs to verify identity securely.",
                ["authentication", "challenge-response", "mathematical proofs"],
                1.0
            ),
            SearchDocument(
                27,
                "Error-Correcting Codes in Cryptography",
                "Error-correcting codes use algebraic structures to detect and correct errors in data transmission, often used in cryptographic channels.",
                ["error-correcting codes", "algebraic structures", "data transmission"],
                1.0
            ),
            SearchDocument(
                28,
                "Mathematical Complexity in Cryptographic Algorithms",
                "Complexity theory analyzes the computational hardness of cryptographic algorithms, ensuring practical security.",
                ["complexity theory", "computational hardness", "cryptographic algorithms"],
                1.0
            ),
            SearchDocument(
                29,
                "Group Theory Applications in Cryptography",
                "Group theory provides the mathematical foundation for many cryptographic schemes, including ECC and Diffie-Hellman.",
                ["group theory", "ECC", "Diffie-Hellman"],
                1.0
            ),
            SearchDocument(
                30,
                "Mathematical Analysis of Hash Collisions",
                "Hash collision analysis uses probability and combinatorics to estimate likelihood and impact in cryptographic systems.",
                ["hash collisions", "probability", "combinatorics"],
                1.0
            ),
        ]
        for doc in docs:
            self.add_document(doc)
        self._preseeded = True

def get_search_index() -> SearchIndex:
    if not hasattr(get_search_index, "_instance"):
        get_search_index._instance = SearchIndex()
        get_search_index._instance._preseed_documents()
    return get_search_index._instance