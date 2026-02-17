import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

class SearchDocument:
    def __init__(self, doc_id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = doc_id
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
        self.doc_lengths: Dict[str, int] = {}
        self.term_doc_freqs: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.term_freqs: Dict[str, int] = defaultdict(int)
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.idf_cache: Dict[str, float] = {}
        self.avg_doc_length: float = 0.0
        self.lock = threading.RLock()
        self.k1 = 1.5
        self.b = 0.75
        self._preseeded = False

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            term_counts = Counter(tokens)
            for term, freq in term_counts.items():
                self.term_doc_freqs[term][doc.id] = freq
                self.term_freqs[term] += freq
            for term in term_counts:
                self.doc_freqs[term] += 1
            self._update_avg_doc_length()
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        with self.lock:
            query_terms = self._tokenize(query)
            scores = defaultdict(float)
            for term in query_terms:
                idf = self._compute_idf(term)
                for doc_id, freq in self.term_doc_freqs.get(term, {}).items():
                    doc = self.documents[doc_id]
                    score = self._score_bm25(term, freq, doc_id, idf, doc.weight)
                    scores[doc_id] += score
            # TF-IDF normalization
            tfidf_scores = self._tfidf_score(query_terms)
            for doc_id, tfidf_score in tfidf_scores.items():
                scores[doc_id] += tfidf_score
            ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            results = []
            for doc_id, score in ranked[:limit]:
                doc = self.documents[doc_id]
                snippet = self._make_snippet(doc.content, query_terms)
                results.append(SearchResult(doc_id, score, doc.title, snippet))
            return results

    def get_stats(self) -> Dict[str, int]:
        with self.lock:
            return {
                "document_count": len(self.documents),
                "unique_terms": len(self.term_freqs),
                "avg_doc_length": self.avg_doc_length
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        with self.lock:
            if term in self.idf_cache:
                return self.idf_cache[term]
            N = len(self.documents)
            df = self.doc_freqs.get(term, 0)
            idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
            self.idf_cache[term] = idf
            return idf

    def _score_bm25(self, term: str, freq: int, doc_id: str, idf: float, weight: float) -> float:
        dl = self.doc_lengths[doc_id]
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1
        numerator = freq * (self.k1 + 1)
        denominator = freq + self.k1 * (1 - self.b + self.b * dl / avg_dl)
        score = idf * (numerator / denominator) * weight
        return score

    def _tfidf_score(self, query_terms: List[str]) -> Dict[str, float]:
        tfidf_scores = defaultdict(float)
        N = len(self.documents)
        for term in query_terms:
            idf = self._compute_idf(term)
            for doc_id, freq in self.term_doc_freqs.get(term, {}).items():
                tf = freq / self.doc_lengths[doc_id]
                tfidf_scores[doc_id] += tf * idf
        return tfidf_scores

    def _update_avg_doc_length(self):
        total_length = sum(self.doc_lengths.values())
        count = len(self.doc_lengths)
        self.avg_doc_length = total_length / count if count > 0 else 0

    def _make_snippet(self, content: str, query_terms: List[str]) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:30]) + '...'
        start = max(positions[0] - 10, 0)
        end = min(positions[0] + 20, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return snippet + '...'

    def preseed_documents(self):
        if self._preseeded:
            return
        docs = [
            SearchDocument(
                "doc1",
                "Principle of Least Privilege",
                "The principle of least privilege requires that users and systems are granted only the minimum access necessary to perform their tasks. This reduces the attack surface and limits potential damage from compromised accounts.",
                ["least_privilege", "access_control", "security"],
                1.0
            ),
            SearchDocument(
                "doc2",
                "Defense in Depth Strategy",
                "Defense in depth is a layered approach to security, employing multiple controls at different levels to protect resources. If one layer fails, others remain to mitigate threats.",
                ["defense_in_depth", "layered_security", "strategy"],
                1.0
            ),
            SearchDocument(
                "doc3",
                "Sovereign Override Mechanisms",
                "Sovereign override allows authorized entities to bypass standard controls in exceptional circumstances, ensuring continuity and resilience in critical operations.",
                ["sovereign_override", "resilience", "emergency"],
                1.0
            ),
            SearchDocument(
                "doc4",
                "Token Integrity Verification",
                "Token integrity ensures that authentication tokens are valid, unaltered, and issued by trusted authorities. Verification mechanisms include cryptographic signatures and expiration checks.",
                ["token_integrity", "authentication", "verification"],
                1.0
            ),
            SearchDocument(
                "doc5",
                "Brute Force Prevention Techniques",
                "Brute force prevention involves rate limiting, account lockouts, and CAPTCHA challenges to deter automated attacks on authentication endpoints.",
                ["brute_force_prevention", "rate_limiting", "authentication"],
                1.0
            ),
            SearchDocument(
                "doc6",
                "Privileged Access Management",
                "Privileged access management restricts and monitors elevated permissions to critical systems, enforcing least privilege and auditing activities.",
                ["least_privilege", "privileged_access", "monitoring"],
                1.0
            ),
            SearchDocument(
                "doc7",
                "Multi-factor Authentication",
                "Multi-factor authentication strengthens token integrity by requiring multiple forms of verification, such as passwords and biometrics.",
                ["token_integrity", "authentication", "multi_factor"],
                1.0
            ),
            SearchDocument(
                "doc8",
                "Layered Network Security",
                "Layered network security implements defense in depth by segmenting networks, deploying firewalls, and using intrusion detection systems.",
                ["defense_in_depth", "network_security", "segmentation"],
                1.0
            ),
            SearchDocument(
                "doc9",
                "Emergency Access Protocols",
                "Emergency access protocols define sovereign override procedures for rapid response during incidents, balancing security and operational needs.",
                ["sovereign_override", "emergency", "incident_response"],
                1.0
            ),
            SearchDocument(
                "doc10",
                "Token Expiry and Revocation",
                "Token expiry and revocation mechanisms maintain token integrity by ensuring expired or compromised tokens cannot be used for authentication.",
                ["token_integrity", "revocation", "expiry"],
                1.0
            ),
            SearchDocument(
                "doc11",
                "Account Lockout Policies",
                "Account lockout policies are a brute force prevention measure, temporarily disabling accounts after repeated failed login attempts.",
                ["brute_force_prevention", "account_lockout", "policy"],
                1.0
            ),
            SearchDocument(
                "doc12",
                "Segregation of Duties",
                "Segregation of duties enforces least privilege by dividing responsibilities among multiple users, reducing risk of fraud or error.",
                ["least_privilege", "segregation", "duties"],
                1.0
            ),
            SearchDocument(
                "doc13",
                "Security Monitoring and Alerting",
                "Continuous monitoring and alerting support defense in depth by detecting anomalous activity and responding to threats in real time.",
                ["defense_in_depth", "monitoring", "alerting"],
                1.0
            ),
            SearchDocument(
                "doc14",
                "Override Logging and Audit Trails",
                "Sovereign override actions must be logged and audited to ensure accountability and traceability during exceptional access events.",
                ["sovereign_override", "logging", "audit"],
                1.0
            ),
            SearchDocument(
                "doc15",
                "Cryptographic Token Validation",
                "Cryptographic validation of tokens is essential for token integrity, using digital signatures to confirm authenticity.",
                ["token_integrity", "cryptography", "validation"],
                1.0
            ),
            SearchDocument(
                "doc16",
                "Adaptive Rate Limiting",
                "Adaptive rate limiting dynamically adjusts thresholds to prevent brute force attacks while minimizing impact on legitimate users.",
                ["brute_force_prevention", "rate_limiting", "adaptive"],
                1.0
            ),
            SearchDocument(
                "doc17",
                "Role-Based Access Control",
                "Role-based access control implements least privilege by assigning permissions based on roles, limiting access to only what is necessary.",
                ["least_privilege", "rbac", "access_control"],
                1.0
            ),
            SearchDocument(
                "doc18",
                "Redundancy in Security Controls",
                "Redundancy in security controls is a defense in depth principle, ensuring multiple safeguards are in place for critical assets.",
                ["defense_in_depth", "redundancy", "controls"],
                1.0
            ),
            SearchDocument(
                "doc19",
                "Override Authorization Workflow",
                "Override authorization workflows govern sovereign override requests, requiring multi-party approval and documented justification.",
                ["sovereign_override", "authorization", "workflow"],
                1.0
            ),
            SearchDocument(
                "doc20",
                "Token Replay Attack Mitigation",
                "Mitigating token replay attacks is crucial for token integrity, using nonce values and timestamp validation.",
                ["token_integrity", "replay_attack", "mitigation"],
                1.0
            ),
            SearchDocument(
                "doc21",
                "CAPTCHA Implementation",
                "CAPTCHA is a brute force prevention tool, distinguishing human users from automated scripts during authentication.",
                ["brute_force_prevention", "captcha", "authentication"],
                1.0
            ),
            SearchDocument(
                "doc22",
                "Just-in-Time Privilege Elevation",
                "Just-in-time privilege elevation grants temporary access, enforcing least privilege and reducing exposure to threats.",
                ["least_privilege", "privilege_elevation", "temporary_access"],
                1.0
            ),
            SearchDocument(
                "doc23",
                "Defense in Depth for Cloud Environments",
                "Applying defense in depth in cloud environments involves layered controls such as encryption, access management, and monitoring.",
                ["defense_in_depth", "cloud_security", "encryption"],
                1.0
            ),
            SearchDocument(
                "doc24",
                "Override Risk Assessment",
                "Risk assessment is required before sovereign override actions, evaluating potential impact and necessity.",
                ["sovereign_override", "risk_assessment", "impact"],
                1.0
            ),
            SearchDocument(
                "doc25",
                "Token Blacklisting",
                "Token blacklisting prevents use of compromised tokens, supporting token integrity and secure authentication.",
                ["token_integrity", "blacklisting", "authentication"],
                1.0
            ),
            SearchDocument(
                "doc26",
                "Brute Force Detection Analytics",
                "Analytics tools detect brute force attempts by analyzing login patterns and flagging suspicious activity.",
                ["brute_force_prevention", "analytics", "detection"],
                1.0
            ),
            SearchDocument(
                "doc27",
                "Privilege Review and Recertification",
                "Regular privilege review ensures least privilege is maintained, recertifying user access as business needs change.",
                ["least_privilege", "review", "recertification"],
                1.0
            ),
            SearchDocument(
                "doc28",
                "Defense in Depth for Physical Security",
                "Physical security layers, such as access badges and surveillance, complement digital defense in depth strategies.",
                ["defense_in_depth", "physical_security", "surveillance"],
                1.0
            ),
            SearchDocument(
                "doc29",
                "Override Escalation Procedures",
                "Override escalation procedures define steps for sovereign override, including notification and approval requirements.",
                ["sovereign_override", "escalation", "procedures"],
                1.0
            ),
            SearchDocument(
                "doc30",
                "Token Rotation Policies",
                "Token rotation policies enhance token integrity by periodically replacing tokens to reduce risk of compromise.",
                ["token_integrity", "rotation", "policy"],
                1.0
            ),
            SearchDocument(
                "doc31",
                "Brute Force Attack Response Plan",
                "A response plan for brute force attacks includes detection, mitigation, and recovery steps to protect authentication systems.",
                ["brute_force_prevention", "response", "attack"],
                1.0
            ),
            SearchDocument(
                "doc32",
                "Enforcing Least Privilege in DevOps",
                "DevOps environments require strict least privilege enforcement, limiting access to deployment and infrastructure tools.",
                ["least_privilege", "devops", "enforcement"],
                1.0
            ),
            SearchDocument(
                "doc33",
                "Defense in Depth for Application Security",
                "Application security employs defense in depth through input validation, error handling, and secure coding practices.",
                ["defense_in_depth", "application_security", "secure_coding"],
                1.0
            ),
            SearchDocument(
                "doc34",
                "Override Notification Systems",
                "Notification systems alert stakeholders when sovereign override is exercised, ensuring transparency and accountability.",
                ["sovereign_override", "notification", "transparency"],
                1.0
            ),
            SearchDocument(
                "doc35",
                "Token Binding Techniques",
                "Token binding links tokens to specific sessions or devices, improving token integrity and reducing misuse.",
                ["token_integrity", "binding", "session"],
                1.0
            ),
            SearchDocument(
                "doc36",
                "Brute Force Prevention for APIs",
                "API endpoints require brute force prevention measures such as throttling and IP blacklisting.",
                ["brute_force_prevention", "api", "throttling"],
                1.0
            ),
            SearchDocument(
                "doc37",
                "Least Privilege for Third-Party Integrations",
                "Third-party integrations must adhere to least privilege, granting only necessary permissions and monitoring activity.",
                ["least_privilege", "third_party", "integration"],
                1.0
            ),
            SearchDocument(
                "doc38",
                "Defense in Depth for IoT Devices",
                "IoT devices benefit from defense in depth, including firmware updates, network segmentation, and device authentication.",
                ["defense_in_depth", "iot", "firmware"],
                1.0
            ),
            SearchDocument(
                "doc39",
                "Override Policy Documentation",
                "Comprehensive documentation of override policies ensures clarity and compliance with sovereign override requirements.",
                ["sovereign_override", "documentation", "policy"],
                1.0
            ),
            SearchDocument(
                "doc40",
                "Token Revocation List Management",
                "Managing token revocation lists is essential for maintaining token integrity and preventing unauthorized access.",
                ["token_integrity", "revocation", "management"],
                1.0
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
            _search_index_instance.preseed_documents()
        return _search_index_instance