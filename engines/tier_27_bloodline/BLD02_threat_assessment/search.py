import math
import threading
import heapq
import re
from collections import defaultdict, Counter

class SearchDocument:
    def __init__(self, doc_id, title, content, tags=None, weight=1.0):
        self.id = doc_id
        self.title = title
        self.content = content
        self.tags = tags or []
        self.weight = weight

class SearchResult:
    def __init__(self, doc_id, score, title, snippet):
        self.doc_id = doc_id
        self.score = score
        self.title = title
        self.snippet = snippet

class SearchIndex:
    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.documents = {}
        self.doc_lengths = {}
        self.avg_doc_length = 0.0
        self.term_doc_freq = defaultdict(set)
        self.term_freq = defaultdict(lambda: defaultdict(int))
        self.total_docs = 0
        self.lock = threading.Lock()
        self.idf_cache = {}
        self.tags_index = defaultdict(set)

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            for token in tokens:
                self.term_doc_freq[token].add(doc.id)
                self.term_freq[token][doc.id] += 1
            for tag in doc.tags:
                self.tags_index[tag.lower()].add(doc.id)
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self.idf_cache.clear()

    def search(self, query, limit=10):
        query_tokens = self._tokenize(query)
        doc_scores = defaultdict(float)
        doc_snippets = {}
        docs_to_score = set()
        for token in query_tokens:
            docs_to_score.update(self.term_doc_freq.get(token, set()))
        if not docs_to_score:
            return []
        for doc_id in docs_to_score:
            bm25_score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            doc = self.documents[doc_id]
            combined_score = bm25_score * 0.7 + tfidf_score * 0.3
            combined_score *= doc.weight
            doc_scores[doc_id] = combined_score
            doc_snippets[doc_id] = self._generate_snippet(doc, query_tokens)
        top_docs = heapq.nlargest(limit, doc_scores.items(), key=lambda x: x[1])
        results = []
        for doc_id, score in top_docs:
            doc = self.documents[doc_id]
            snippet = doc_snippets[doc_id]
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self):
        return {
            "total_documents": self.total_docs,
            "average_document_length": self.avg_doc_length,
            "unique_terms": len(self.term_doc_freq),
            "tags": list(self.tags_index.keys())
        }

    def _tokenize(self, text):
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def _compute_idf(self, term):
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = len(self.term_doc_freq.get(term, set()))
        if df == 0:
            return 0.0
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id, query_tokens):
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        for term in query_tokens:
            idf = self._compute_idf(term)
            f = self.term_freq[term].get(doc_id, 0)
            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1 - self.b + self.b * doc_length / avg_dl)
            if denominator == 0:
                continue
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id, query_tokens):
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        for term in query_tokens:
            tf = self.term_freq[term].get(doc_id, 0)
            if doc_length == 0:
                continue
            tf_norm = tf / doc_length
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _generate_snippet(self, doc: SearchDocument, query_tokens):
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            snippet = content[:160]
        else:
            start = max(positions[0] - 10, 0)
            end = min(positions[0] + 20, len(tokens))
            snippet_tokens = tokens[start:end]
            snippet = ' '.join(snippet_tokens)
        return snippet.strip()

_search_index_instance = None
_search_index_lock = threading.Lock()

def get_search_index():
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            doc_id="1",
            title="Physical Security Threats in Corporate Environments",
            content="Physical security threats include unauthorized access, theft, vandalism, and sabotage. Mitigating these risks requires surveillance, access control, and employee training.",
            tags=["physical_security_threat", "corporate"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="2",
            title="Cybersecurity Threat Frameworks: NIST and MITRE",
            content="Cybersecurity threat frameworks such as NIST and MITRE ATT&CK provide structured approaches to identifying and mitigating cyber risks. They emphasize threat intelligence, vulnerability management, and incident response.",
            tags=["cybersecurity_threat_framework", "nist", "mitre"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="3",
            title="Financial Threat Detection: Fraud and Money Laundering",
            content="Financial threats include fraud, money laundering, and embezzlement. Detection strategies involve transaction monitoring, anomaly detection, and regulatory compliance.",
            tags=["financial_threat_detection", "fraud"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="4",
            title="Legal Threat Assessment: Regulatory Risks",
            content="Legal threats arise from regulatory changes, compliance failures, and litigation. Proactive assessment involves legal audits, risk mapping, and policy updates.",
            tags=["legal_threat_assessment", "regulatory"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="5",
            title="Reputation Threat Monitoring: Social Media and PR",
            content="Reputation threats stem from negative publicity, social media crises, and misinformation. Monitoring tools and crisis management plans are essential for mitigation.",
            tags=["reputation_threat_monitoring", "social_media"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="6",
            title="Insider Threat Detection: Behavioral Analytics",
            content="Insider threats involve employees or contractors misusing access. Behavioral analytics, access reviews, and whistleblower programs help detect and prevent such risks.",
            tags=["insider_threat_detection", "behavioral"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="7",
            title="Supply Chain Threat Analysis: Vendor Risk",
            content="Supply chain threats include vendor risk, counterfeit products, and logistics disruptions. Risk analysis requires supplier audits, contract reviews, and contingency planning.",
            tags=["supply_chain_threat_analysis", "vendor"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="8",
            title="Geopolitical Risk in the Permian Basin",
            content="Geopolitical risks in the Permian Basin affect oil and gas operations. Factors include regulatory changes, international sanctions, and local unrest.",
            tags=["geopolitical_permian_basin_risk", "oil_gas"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="9",
            title="Credential Compromise Threats: Password Security",
            content="Credential compromise occurs through phishing, brute force, and credential stuffing. Strong password policies and multi-factor authentication mitigate these threats.",
            tags=["credential_compromise_threat", "password"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="10",
            title="Ransomware Threats: Prevention and Response",
            content="Ransomware attacks encrypt data and demand payment. Prevention includes regular backups, patching, and employee awareness. Incident response plans are critical.",
            tags=["ransomware_threat", "prevention"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="11",
            title="Social Engineering Threats: Phishing and Impersonation",
            content="Social engineering exploits human vulnerabilities through phishing, pretexting, and impersonation. Security awareness training reduces risk.",
            tags=["social_engineering_threats", "phishing"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="12",
            title="Environmental Compliance Threats: Regulatory Enforcement",
            content="Environmental compliance threats include regulatory enforcement, fines, and operational shutdowns. Risk mitigation involves monitoring emissions and maintaining permits.",
            tags=["environmental_compliance_threat", "regulatory"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="13",
            title="DDoS Service Disruption: Mitigation Strategies",
            content="Distributed Denial of Service (DDoS) attacks disrupt online services. Mitigation includes traffic filtering, rate limiting, and cloud-based protection.",
            tags=["ddos_service_disruption", "mitigation"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="14",
            title="Intellectual Property Theft: Data Protection",
            content="Intellectual property theft involves unauthorized copying or use of proprietary data. Protection strategies include encryption, access control, and legal action.",
            tags=["intellectual_property_theft", "data_protection"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="15",
            title="Economic Downturn Market Risk: Impact on Operations",
            content="Economic downturns increase market risk, affecting revenue and operations. Scenario planning and financial reserves help mitigate impact.",
            tags=["economic_downturn_market_risk", "operations"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="16",
            title="Physical Security: Access Control Systems",
            content="Access control systems restrict entry to sensitive areas. Technologies include card readers, biometrics, and security personnel.",
            tags=["physical_security_threat", "access_control"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="17",
            title="Cybersecurity: Vulnerability Management",
            content="Vulnerability management identifies and remediates software flaws. Patch management and vulnerability scanning are key components.",
            tags=["cybersecurity_threat_framework", "vulnerability"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="18",
            title="Financial Threats: Transaction Monitoring",
            content="Transaction monitoring detects suspicious financial activity. Automated systems flag anomalies for investigation.",
            tags=["financial_threat_detection", "transaction"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="19",
            title="Legal Compliance: Litigation Risk",
            content="Litigation risk arises from contractual disputes and regulatory violations. Legal teams must monitor changes in law and maintain compliance.",
            tags=["legal_threat_assessment", "litigation"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="20",
            title="Reputation Management: Crisis Response",
            content="Crisis response plans address reputation threats from negative events. Rapid communication and transparency are vital.",
            tags=["reputation_threat_monitoring", "crisis"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="21",
            title="Insider Threats: Data Leakage Prevention",
            content="Data leakage prevention tools monitor and block unauthorized data transfers. Employee monitoring and policy enforcement are critical.",
            tags=["insider_threat_detection", "data_leakage"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="22",
            title="Supply Chain: Counterfeit Detection",
            content="Counterfeit detection in supply chains uses product authentication and supplier verification. Technology solutions include RFID and blockchain.",
            tags=["supply_chain_threat_analysis", "counterfeit"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="23",
            title="Permian Basin: Regulatory Changes",
            content="Regulatory changes in the Permian Basin impact oil production and compliance requirements. Monitoring legal developments is essential.",
            tags=["geopolitical_permian_basin_risk", "regulatory"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="24",
            title="Credential Security: Multi-Factor Authentication",
            content="Multi-factor authentication adds layers of security to credential protection. Implementation reduces risk of compromise.",
            tags=["credential_compromise_threat", "mfa"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="25",
            title="Ransomware: Backup Strategies",
            content="Effective backup strategies are critical for ransomware resilience. Regular, offsite backups enable rapid recovery.",
            tags=["ransomware_threat", "backup"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="26",
            title="Social Engineering: Pretexting Techniques",
            content="Pretexting is a social engineering technique where attackers fabricate scenarios to obtain sensitive information.",
            tags=["social_engineering_threats", "pretexting"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="27",
            title="Environmental Compliance: Permit Management",
            content="Permit management ensures ongoing compliance with environmental regulations. Automated tracking and renewal systems reduce risk.",
            tags=["environmental_compliance_threat", "permit"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="28",
            title="DDoS: Cloud-Based Protection",
            content="Cloud-based DDoS protection scales to absorb large attacks. Providers offer real-time mitigation and analytics.",
            tags=["ddos_service_disruption", "cloud"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="29",
            title="Intellectual Property: Legal Remedies",
            content="Legal remedies for intellectual property theft include cease-and-desist orders, litigation, and damages recovery.",
            tags=["intellectual_property_theft", "legal"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="30",
            title="Economic Downturn: Scenario Planning",
            content="Scenario planning prepares organizations for economic downturns by modeling potential impacts and developing response strategies.",
            tags=["economic_downturn_market_risk", "scenario"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="31",
            title="Physical Security: Surveillance Systems",
            content="Surveillance systems monitor premises for physical threats. Technologies include CCTV, motion sensors, and remote monitoring.",
            tags=["physical_security_threat", "surveillance"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="32",
            title="Cybersecurity: Incident Response",
            content="Incident response teams handle cybersecurity breaches. Procedures include containment, eradication, and recovery.",
            tags=["cybersecurity_threat_framework", "incident_response"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="33",
            title="Financial Threats: Regulatory Compliance",
            content="Regulatory compliance is essential for financial threat mitigation. Organizations must adhere to anti-money laundering and fraud prevention laws.",
            tags=["financial_threat_detection", "regulatory"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="34",
            title="Legal Threats: Policy Updates",
            content="Policy updates address evolving legal threats. Regular review ensures compliance with new regulations and reduces litigation risk.",
            tags=["legal_threat_assessment", "policy"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="35",
            title="Reputation Threats: Misinformation Management",
            content="Misinformation management counters false narratives that threaten reputation. Strategies include fact-checking and proactive communication.",
            tags=["reputation_threat_monitoring", "misinformation"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="36",
            title="Insider Threats: Whistleblower Programs",
            content="Whistleblower programs encourage reporting of insider threats. Confidential channels and protection policies are vital.",
            tags=["insider_threat_detection", "whistleblower"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="37",
            title="Supply Chain: Logistics Disruption",
            content="Logistics disruptions in supply chains can halt production. Risk mitigation includes redundancy and diversified suppliers.",
            tags=["supply_chain_threat_analysis", "logistics"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="38",
            title="Permian Basin: International Sanctions",
            content="International sanctions impact Permian Basin operations. Companies must monitor geopolitical developments and adjust strategies.",
            tags=["geopolitical_permian_basin_risk", "sanctions"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="39",
            title="Credential Compromise: Credential Stuffing",
            content="Credential stuffing attacks use stolen credentials to access accounts. Detection includes monitoring login anomalies and enforcing password resets.",
            tags=["credential_compromise_threat", "stuffing"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="40",
            title="Ransomware: Incident Response",
            content="Incident response for ransomware includes isolating affected systems, communicating with stakeholders, and restoring from backups.",
            tags=["ransomware_threat", "incident_response"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)