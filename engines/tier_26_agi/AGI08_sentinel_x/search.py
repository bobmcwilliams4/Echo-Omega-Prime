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
        self.documents: Dict[int, SearchDocument] = {}
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.RLock()
        self._recompute_stats = True

    def add_document(self, doc: SearchDocument):
        with self.lock:
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            token_counts = Counter(tokens)
            self.doc_lengths[doc.id] = len(tokens)
            for token, count in token_counts.items():
                self.inverted_index[token][doc.id] = count
            self.N = len(self.documents)
            self._recompute_stats = True

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        with self.lock:
            query_tokens = self._tokenize(query)
            doc_scores = defaultdict(float)
            doc_snippets = {}
            # Precompute stats if needed
            if self._recompute_stats:
                self._update_stats()
            # BM25 scoring
            for token in set(query_tokens):
                idf = self._compute_idf(token)
                postings = self.inverted_index.get(token, {})
                for doc_id, freq in postings.items():
                    doc = self.documents[doc_id]
                    score = self._score_bm25(token, doc_id, freq, idf, doc.weight)
                    doc_scores[doc_id] += score
            # TF-IDF scoring (normalized)
            tfidf_scores = self._score_tfidf(query_tokens)
            # Combine BM25 and TF-IDF (weighted sum)
            for doc_id in doc_scores:
                doc_scores[doc_id] = 0.7 * doc_scores[doc_id] + 0.3 * tfidf_scores.get(doc_id, 0.0)
            # Prepare results
            results = []
            for doc_id, score in sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]:
                doc = self.documents[doc_id]
                snippet = self._make_snippet(doc.content, query_tokens)
                results.append(SearchResult(doc_id, score, doc.title, snippet))
            return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            if self._recompute_stats:
                self._update_stats()
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avg_doc_length,
                "vocab_size": len(self.inverted_index)
            }

    def _tokenize(self, text: str) -> List[str]:
        # Simple word tokenizer, case-insensitive
        return re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())

    def _compute_idf(self, token: str) -> float:
        if token in self.idf_cache:
            return self.idf_cache[token]
        df = len(self.inverted_index.get(token, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[token] = idf
        return idf

    def _score_bm25(self, token: str, doc_id: int, freq: int, idf: float, weight: float) -> float:
        k1 = 1.5
        b = 0.75
        doc_len = self.doc_lengths[doc_id]
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        tf = freq
        denom = tf + k1 * (1 - b + b * doc_len / avg_dl)
        score = idf * ((tf * (k1 + 1)) / denom)
        return score * weight

    def _score_tfidf(self, query_tokens: List[str]) -> Dict[int, float]:
        # Compute normalized TF-IDF for each document
        tfidf_scores = defaultdict(float)
        query_terms = set(query_tokens)
        for token in query_terms:
            idf = self._compute_idf(token)
            postings = self.inverted_index.get(token, {})
            for doc_id, freq in postings.items():
                tf = freq / self.doc_lengths[doc_id]
                tfidf_scores[doc_id] += tf * idf * self.documents[doc_id].weight
        return tfidf_scores

    def _make_snippet(self, content: str, query_tokens: List[str], size: int = 160) -> str:
        # Find first occurrence of any query token, extract snippet
        content_lower = content.lower()
        positions = []
        for qt in query_tokens:
            idx = content_lower.find(qt)
            if idx != -1:
                positions.append(idx)
        if positions:
            start = max(0, min(positions) - 30)
        else:
            start = 0
        snippet = content[start:start+size]
        if len(snippet) < len(content):
            snippet += "..."
        return snippet

    def _update_stats(self):
        self.N = len(self.documents)
        if self.N == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N
        self.idf_cache.clear()
        self._recompute_stats = False

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

# --- Pre-seed Domain Documents ---

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "STRIDE Threat Modeling Overview",
            "STRIDE is a threat modeling framework that categorizes threats into Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege. It helps identify and mitigate security risks in software systems.",
            ["STRIDE", "Threat Modeling", "Security"],
            1.0
        ),
        SearchDocument(
            2,
            "PASTA: Process for Attack Simulation and Threat Analysis",
            "PASTA is a risk-centric threat modeling methodology with seven stages: definition of objectives, technical scope, decomposition, threat analysis, vulnerability analysis, attack modeling, and risk analysis.",
            ["PASTA", "Threat Modeling", "Risk"],
            1.0
        ),
        SearchDocument(
            3,
            "DREAD Risk Assessment Model",
            "DREAD is a risk assessment model that scores threats based on Damage, Reproducibility, Exploitability, Affected Users, and Discoverability. It helps prioritize vulnerabilities for remediation.",
            ["DREAD", "Risk Assessment", "Threat"],
            1.0
        ),
        SearchDocument(
            4,
            "Attack Trees in Threat Analysis",
            "Attack trees are diagrams that model how attacks can be carried out against a system. Each node represents a possible attack step, helping analysts visualize and evaluate security threats.",
            ["Attack Trees", "Threat Analysis", "Modeling"],
            1.0
        ),
        SearchDocument(
            5,
            "OWASP Top 10: Injection",
            "Injection flaws, such as SQL, NoSQL, OS, and LDAP injection, occur when untrusted data is sent to an interpreter as part of a command or query. Attackers can execute malicious commands or access data without authorization.",
            ["OWASP", "Injection", "Vulnerabilities"],
            1.0
        ),
        SearchDocument(
            6,
            "OWASP Top 10: Cross-Site Scripting (XSS)",
            "Cross-Site Scripting (XSS) enables attackers to inject client-side scripts into web pages viewed by other users. XSS can be used to hijack sessions, deface websites, or redirect users to malicious sites.",
            ["OWASP", "XSS", "Web Security"],
            1.0
        ),
        SearchDocument(
            7,
            "OWASP Top 10: Cross-Site Request Forgery (CSRF)",
            "CSRF attacks trick authenticated users into submitting requests to a web application without their consent. Proper use of anti-CSRF tokens and same-site cookies can mitigate these attacks.",
            ["OWASP", "CSRF", "Web Security"],
            1.0
        ),
        SearchDocument(
            8,
            "OWASP Top 10: Server-Side Request Forgery (SSRF)",
            "SSRF flaws allow attackers to induce the server-side application to make HTTP requests to an unintended location. SSRF can be used to access internal resources or escalate attacks.",
            ["OWASP", "SSRF", "Web Security"],
            1.0
        ),
        SearchDocument(
            9,
            "CVSS Scoring: Base Metrics",
            "The Common Vulnerability Scoring System (CVSS) base metrics represent the intrinsic characteristics of a vulnerability, such as attack vector, complexity, privileges required, user interaction, scope, and impact.",
            ["CVSS", "Scoring", "Base"],
            1.0
        ),
        SearchDocument(
            10,
            "CVSS Scoring: Temporal Metrics",
            "CVSS temporal metrics reflect the characteristics of a vulnerability that may change over time, including exploit code maturity, remediation level, and report confidence.",
            ["CVSS", "Scoring", "Temporal"],
            1.0
        ),
        SearchDocument(
            11,
            "CVSS Scoring: Environmental Metrics",
            "CVSS environmental metrics allow organizations to customize CVSS scores based on their environment, considering security requirements and modified base metrics.",
            ["CVSS", "Scoring", "Environmental"],
            1.0
        ),
        SearchDocument(
            12,
            "Intrusion Detection: Signature-Based",
            "Signature-based intrusion detection systems (IDS) identify attacks by matching patterns of known threats. They are effective against known attacks but may miss new or obfuscated threats.",
            ["Intrusion Detection", "Signature-Based", "IDS"],
            1.0
        ),
        SearchDocument(
            13,
            "Intrusion Detection: Anomaly-Based",
            "Anomaly-based IDS detect deviations from normal behavior to identify potential threats. They can detect novel attacks but may produce more false positives.",
            ["Intrusion Detection", "Anomaly-Based", "IDS"],
            1.0
        ),
        SearchDocument(
            14,
            "Intrusion Detection: Hybrid Systems",
            "Hybrid intrusion detection systems combine signature-based and anomaly-based techniques to improve detection accuracy and reduce false positives.",
            ["Intrusion Detection", "Hybrid", "IDS"],
            1.0
        ),
        SearchDocument(
            15,
            "SIEM Integration and Log Correlation",
            "Security Information and Event Management (SIEM) systems aggregate and analyze log data from multiple sources. Log correlation helps detect complex attack patterns and supports incident response.",
            ["SIEM", "Log Correlation", "Security"],
            1.0
        ),
        SearchDocument(
            16,
            "Threat Modeling: Data Flow Diagrams",
            "Data Flow Diagrams (DFDs) are used in threat modeling to visualize data movement and trust boundaries. DFDs help identify potential threats and security controls.",
            ["Threat Modeling", "DFD", "Data Flow"],
            1.0
        ),
        SearchDocument(
            17,
            "STRIDE: Spoofing Threats",
            "Spoofing involves impersonating users or systems to gain unauthorized access. Authentication mechanisms can mitigate spoofing threats.",
            ["STRIDE", "Spoofing", "Authentication"],
            1.0
        ),
        SearchDocument(
            18,
            "STRIDE: Tampering Threats",
            "Tampering refers to unauthorized modification of data or code. Integrity checks and cryptographic signatures help prevent tampering.",
            ["STRIDE", "Tampering", "Integrity"],
            1.0
        ),
        SearchDocument(
            19,
            "STRIDE: Repudiation Threats",
            "Repudiation threats occur when users deny performing actions. Audit logs and non-repudiation controls are essential to address these threats.",
            ["STRIDE", "Repudiation", "Audit"],
            1.0
        ),
        SearchDocument(
            20,
            "STRIDE: Information Disclosure",
            "Information Disclosure exposes confidential data to unauthorized parties. Encryption and access controls are key mitigations.",
            ["STRIDE", "Information Disclosure", "Confidentiality"],
            1.0
        ),
        SearchDocument(
            21,
            "STRIDE: Denial of Service",
            "Denial of Service (DoS) attacks aim to disrupt service availability. Rate limiting and resource management can help mitigate DoS threats.",
            ["STRIDE", "Denial of Service", "Availability"],
            1.0
        ),
        SearchDocument(
            22,
            "STRIDE: Elevation of Privilege",
            "Elevation of Privilege allows attackers to gain higher access rights. Principle of least privilege and privilege separation are important defenses.",
            ["STRIDE", "Elevation of Privilege", "Authorization"],
            1.0
        ),
        SearchDocument(
            23,
            "Threat Modeling: Identifying Assets",
            "Asset identification is a foundational step in threat modeling. Understanding what needs protection helps prioritize security efforts.",
            ["Threat Modeling", "Assets", "Security"],
            1.0
        ),
        SearchDocument(
            24,
            "OWASP Top 10: Security Misconfiguration",
            "Security misconfiguration is a common vulnerability that exposes systems to attacks. Regular reviews and automated configuration management are recommended.",
            ["OWASP", "Security Misconfiguration", "Vulnerabilities"],
            1.0
        ),
        SearchDocument(
            25,
            "OWASP Top 10: Sensitive Data Exposure",
            "Sensitive data exposure occurs when applications do not adequately protect confidential information. Encryption in transit and at rest is essential.",
            ["OWASP", "Sensitive Data Exposure", "Confidentiality"],
            1.0
        ),
        SearchDocument(
            26,
            "Threat Modeling: Mitigation Strategies",
            "Mitigation strategies in threat modeling include applying security controls, reducing attack surface, and validating inputs. Effective mitigations reduce risk.",
            ["Threat Modeling", "Mitigation", "Security Controls"],
            1.0
        ),
        SearchDocument(
            27,
            "PASTA: Attack Simulation",
            "Attack simulation in PASTA involves modeling how adversaries might exploit vulnerabilities. This step supports risk assessment and prioritization.",
            ["PASTA", "Attack Simulation", "Threat Modeling"],
            1.0
        ),
        SearchDocument(
            28,
            "OWASP Top 10: Broken Authentication",
            "Broken authentication allows attackers to compromise passwords, keys, or session tokens. Multi-factor authentication and secure session management are recommended.",
            ["OWASP", "Broken Authentication", "Vulnerabilities"],
            1.0
        ),
        SearchDocument(
            29,
            "SIEM: Real-Time Alerting",
            "SIEM systems provide real-time alerting for security incidents by correlating events across the infrastructure. Timely alerts enable rapid response.",
            ["SIEM", "Alerting", "Incident Response"],
            1.0
        ),
        SearchDocument(
            30,
            "Attack Trees: AND/OR Nodes",
            "Attack trees use AND and OR nodes to represent complex attack paths. AND nodes require all child conditions, while OR nodes require any child condition.",
            ["Attack Trees", "Modeling", "Security"],
            1.0
        ),
        SearchDocument(
            31,
            "DREAD: Scoring Example",
            "A DREAD scoring example: SQL injection vulnerability. Damage: high, Reproducibility: high, Exploitability: high, Affected users: many, Discoverability: high. Total risk is critical.",
            ["DREAD", "Scoring", "Example"],
            1.0
        ),
        SearchDocument(
            32,
            "Anomaly Detection: Machine Learning",
            "Machine learning techniques can enhance anomaly-based intrusion detection by learning normal patterns and flagging deviations.",
            ["Anomaly Detection", "Machine Learning", "IDS"],
            1.0
        ),
        SearchDocument(
            33,
            "SIEM: Log Normalization",
            "Log normalization in SIEM systems standardizes log formats, enabling effective correlation and analysis across diverse sources.",
            ["SIEM", "Log Normalization", "Security"],
            1.0
        ),
        SearchDocument(
            34,
            "Threat Modeling: Trust Boundaries",
            "Trust boundaries define points where data or control passes between different trust levels. Identifying boundaries is key to threat modeling.",
            ["Threat Modeling", "Trust Boundaries", "Security"],
            1.0
        ),
        SearchDocument(
            35,
            "OWASP Top 10: Using Components with Known Vulnerabilities",
            "Using vulnerable components can compromise application security. Regular updates and dependency management are essential.",
            ["OWASP", "Vulnerabilities", "Components"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)