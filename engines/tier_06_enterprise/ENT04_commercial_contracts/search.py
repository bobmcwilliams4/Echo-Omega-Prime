import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --- SearchDocument Class ---
class SearchDocument:
    def __init__(self, doc_id: int, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = doc_id
        self.title = title
        self.content = content
        self.tags = tags
        self.weight = weight

# --- SearchResult Class ---
class SearchResult:
    def __init__(self, doc_id: int, score: float, title: str, snippet: str):
        self.doc_id = doc_id
        self.score = score
        self.title = title
        self.snippet = snippet

# --- SearchIndex Class ---
class SearchIndex:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_len: Dict[int, int] = {}
        self.avg_doc_len: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_doc_tf: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.term_idf: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._doc_id_counter = 1
        self._re_token = re.compile(r'\w+')
        self._dirty = True

    def _tokenize(self, text: str) -> List[str]:
        tokens = self._re_token.findall(text.lower())
        return tokens

    def add_document(self, title: str, content: str, tags: List[str], weight: float = 1.0) -> int:
        with self.lock:
            doc_id = self._doc_id_counter
            self._doc_id_counter += 1
            doc = SearchDocument(doc_id, title, content, tags, weight)
            self.documents[doc_id] = doc
            tokens = self._tokenize(content)
            self.doc_len[doc_id] = len(tokens)
            tf_counter = Counter(tokens)
            self.term_doc_tf[doc_id] = dict(tf_counter)
            for term in tf_counter:
                self.term_doc_freq[term] += 1
            self._dirty = True
            return doc_id

    def _compute_idf(self):
        N = len(self.documents)
        self.term_idf.clear()
        for term, df in self.term_doc_freq.items():
            # BM25 idf formula
            idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
            self.term_idf[term] = idf
        self.avg_doc_len = sum(self.doc_len.values()) / (N if N else 1)
        self._dirty = False

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        tf_dict = self.term_doc_tf[doc_id]
        score = 0.0
        doc_length = self.doc_len[doc_id]
        for term in query_terms:
            if term not in tf_dict:
                continue
            tf = tf_dict[term]
            idf = self.term_idf.get(term, 0.0)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_length / (self.avg_doc_len if self.avg_doc_len else 1))
            score += idf * numerator / (denominator if denominator else 1)
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        tf_dict = self.term_doc_tf[doc_id]
        doc_length = self.doc_len[doc_id]
        score = 0.0
        for term in query_terms:
            tf = tf_dict.get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_length
            idf = self.term_idf.get(term, 0.0)
            score += tf_norm * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        tokens = self._tokenize(query)
        if not tokens:
            return []
        with self.lock:
            if self._dirty:
                self._compute_idf()
        scores = []
        for doc_id in self.documents:
            if use_tfidf:
                score = self._score_tfidf(tokens, doc_id)
            else:
                score = self._score_bm25(tokens, doc_id)
            if score > 0.0:
                snippet = self._make_snippet(doc_id, tokens)
                scores.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scores.sort(key=lambda r: r.score, reverse=True)
        return scores[:limit]

    def _make_snippet(self, doc_id: int, query_terms: List[str], length: int = 160) -> str:
        content = self.documents[doc_id].content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:length] + ('...' if len(content) > length else '')
        start = max(positions[0] - 10, 0)
        end = min(start + 40, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(r'\b(%s)\b' % re.escape(term), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet[:length] + ('...' if len(snippet) > length else '')

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            stats = {
                'num_documents': len(self.documents),
                'avg_doc_len': self.avg_doc_len,
                'num_terms': len(self.term_doc_freq),
            }
        return stats

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

# --- Preseed Documents ---
def _preseed_documents(idx: SearchIndex):
    docs = [
        {
            'title': "UCC 2-201 Statute of Frauds",
            'content': "UCC 2-201 requires contracts for the sale of goods priced at $500 or more to be in writing and signed by the party against whom enforcement is sought. Exceptions include specially manufactured goods, admissions in court, and partial performance.",
            'tags': ["UCC", "Statute of Frauds", "Sale of Goods"],
        },
        {
            'title': "UCC 2-207 Battle of Forms",
            'content': "UCC 2-207 governs conflicting terms in offer and acceptance forms. It allows contract formation even when acceptance contains additional or different terms, subject to certain limitations and exceptions.",
            'tags': ["UCC", "Battle of Forms", "Offer", "Acceptance"],
        },
        {
            'title': "UCC 2-302 Unconscionability",
            'content': "UCC 2-302 permits courts to refuse enforcement of unconscionable contracts or clauses. Unconscionability can be procedural or substantive, and courts may strike or modify offending terms.",
            'tags': ["UCC", "Unconscionability", "Contract Law"],
        },
        {
            'title': "UCC 2-615 Commercial Impracticability",
            'content': "UCC 2-615 excuses performance when unforeseen events make it commercially impracticable. The event must be outside the control of the parties and not anticipated at contract formation.",
            'tags': ["UCC", "Commercial Impracticability", "Force Majeure"],
        },
        {
            'title': "SaaS License vs Sale Distinction",
            'content': "SaaS agreements typically grant a license to use software rather than a sale of goods. This distinction affects contract terms, warranties, and the applicability of the UCC.",
            'tags': ["SaaS", "License", "Sale", "UCC"],
        },
        {
            'title': "Force Majeure Clauses",
            'content': "Force majeure clauses allocate risk for events beyond the parties' control, such as natural disasters, war, or pandemics. They may excuse performance or extend deadlines.",
            'tags': ["Force Majeure", "Risk Allocation", "Commercial Contracts"],
        },
        {
            'title': "Limitation of Liability Clauses",
            'content': "Limitation of liability clauses cap the damages one party may recover. They are subject to judicial scrutiny for unconscionability and may not cover intentional misconduct.",
            'tags': ["Limitation of Liability", "Damages", "Contract Law"],
        },
        {
            'title': "Indemnification Clauses",
            'content': "Indemnification clauses require one party to compensate the other for losses arising from specified events or actions. Scope and exclusions must be clearly defined.",
            'tags': ["Indemnification", "Risk Allocation", "Commercial Contracts"],
        },
        {
            'title': "Warranty Disclaimers",
            'content': "Warranty disclaimers limit or exclude implied warranties, such as merchantability or fitness for a particular purpose. They must be conspicuous and clear to be enforceable.",
            'tags': ["Warranty", "Disclaimer", "UCC"],
        },
        {
            'title': "Choice of Law and Forum Selection",
            'content': "Choice of law clauses specify which jurisdiction's law governs the contract. Forum selection clauses determine where disputes will be litigated or arbitrated.",
            'tags': ["Choice of Law", "Forum Selection", "Jurisdiction"],
        },
        {
            'title': "Non-Disclosure Agreements (NDAs)",
            'content': "NDAs protect confidential information from unauthorized disclosure. They define what information is confidential, obligations, exceptions, and remedies for breach.",
            'tags': ["NDA", "Confidentiality", "Commercial Contracts"],
        },
        {
            'title': "Material Breach vs Minor Breach",
            'content': "A material breach justifies contract termination, while a minor breach entitles the non-breaching party to damages but not termination. Courts assess the impact on contract purpose.",
            'tags': ["Material Breach", "Minor Breach", "Remedies"],
        },
        {
            'title': "Anti-Assignment Clauses",
            'content': "Anti-assignment clauses prohibit or restrict the transfer of contractual rights or obligations. They protect parties from unwanted changes in counterparties.",
            'tags': ["Anti-Assignment", "Contract Rights", "Commercial Contracts"],
        },
        {
            'title': "Most Favored Nation (MFN) Clauses",
            'content': "MFN clauses require a party to offer terms no less favorable than those offered to other parties. They are common in supply and distribution agreements.",
            'tags': ["MFN", "Supply Agreements", "Distribution"],
        },
        {
            'title': "CISG Application to International Sales",
            'content': "The CISG governs international sales of goods between parties in contracting states. Parties may opt out or modify its application by contract.",
            'tags': ["CISG", "International Sales", "UCC"],
        },
        {
            'title': "Master Service Agreement (MSA) Structure",
            'content': "An MSA sets forth general terms for ongoing services, with specific work orders or statements of work detailing deliverables, timelines, and pricing.",
            'tags': ["MSA", "Services", "Work Orders"],
        },
        {
            'title': "Liquidated Damages vs Penalties",
            'content': "Liquidated damages clauses set predetermined damages for breach. Courts enforce them if they are reasonable estimates, not punitive penalties.",
            'tags': ["Liquidated Damages", "Penalties", "Remedies"],
        },
        {
            'title': "Duty of Good Faith and Fair Dealing",
            'content': "Every commercial contract imposes a duty of good faith and fair dealing. Parties must act honestly and not undermine the contract's purpose.",
            'tags': ["Good Faith", "Fair Dealing", "UCC"],
        },
        {
            'title': "Integration and Merger Clauses",
            'content': "Integration clauses declare the written contract as the complete and exclusive statement of the parties' agreement, excluding prior negotiations.",
            'tags': ["Integration", "Merger", "Parol Evidence"],
        },
        {
            'title': "Best Efforts vs Reasonable Efforts Obligations",
            'content': "Best efforts clauses require a party to pursue objectives with maximum effort, while reasonable efforts require diligence consistent with industry standards.",
            'tags': ["Best Efforts", "Reasonable Efforts", "Obligations"],
        },
        {
            'title': "Modification and No Oral Modification Clauses",
            'content': "Modification clauses specify how contracts may be changed. No oral modification clauses require changes to be in writing to be enforceable.",
            'tags': ["Modification", "No Oral Modification", "Contract Law"],
        },
        {
            'title': "Arbitration Clauses in Commercial Contracts",
            'content': "Arbitration clauses require disputes to be resolved by arbitration rather than litigation. They may specify procedures, rules, and arbitrator selection.",
            'tags': ["Arbitration", "Dispute Resolution", "Commercial Contracts"],
        },
        {
            'title': "Intellectual Property Ownership in Services Contracts",
            'content': "Services contracts must address ownership of intellectual property created during the engagement. Clauses may assign IP to the client or retain it with the provider.",
            'tags': ["Intellectual Property", "Ownership", "Services Contracts"],
        },
        {
            'title': "Termination for Convenience Clauses",
            'content': "Termination for convenience clauses allow a party to end the contract without cause. They may require notice and specify compensation for work performed.",
            'tags': ["Termination", "Convenience", "Commercial Contracts"],
        },
        {
            'title': "Joint Venture Agreements",
            'content': "Joint venture agreements establish collaborative business arrangements. Key terms include contributions, governance, profit sharing, and exit strategies.",
            'tags': ["Joint Venture", "Collaboration", "Commercial Contracts"],
        },
        {
            'title': "Supply Chain and Distribution Agreements",
            'content': "Supply chain and distribution agreements govern the flow of goods from manufacturer to customer. Terms address pricing, delivery, risk of loss, and exclusivity.",
            'tags': ["Supply Chain", "Distribution", "Commercial Contracts"],
        },
        {
            'title': "Parol Evidence Rule in Commercial Contracts",
            'content': "The parol evidence rule limits the use of extrinsic evidence to interpret written contracts, except in cases of ambiguity, fraud, or mistake.",
            'tags': ["Parol Evidence", "Interpretation", "Contract Law"],
        },
        {
            'title': "Assignment and Delegation under UCC",
            'content': "UCC allows assignment of rights and delegation of duties unless the contract prohibits it or the assignment materially alters the obligor's risk.",
            'tags': ["Assignment", "Delegation", "UCC"],
        },
        {
            'title': "Notice Requirements in Commercial Contracts",
            'content': "Notice clauses specify how and when parties must communicate important information, such as breach, termination, or modification.",
            'tags': ["Notice", "Communication", "Commercial Contracts"],
        },
        {
            'title': "Remedies for Breach of Commercial Contract",
            'content': "Remedies include damages, specific performance, rescission, and restitution. The UCC and common law provide guidance for calculating damages.",
            'tags': ["Remedies", "Breach", "Damages"],
        },
        {
            'title': "Exclusivity Clauses in Distribution Agreements",
            'content': "Exclusivity clauses grant one party exclusive rights to distribute goods or services in a defined territory or market segment.",
            'tags': ["Exclusivity", "Distribution", "Supply Chain"],
        },
        {
            'title': "Confidentiality Obligations in Services Agreements",
            'content': "Services agreements often include confidentiality obligations to protect proprietary information, trade secrets, and client data.",
            'tags': ["Confidentiality", "Services", "Obligations"],
        },
        {
            'title': "Change Control Procedures in MSAs",
            'content': "MSAs may include change control procedures to manage modifications to scope, deliverables, or pricing. Changes typically require written approval.",
            'tags': ["Change Control", "MSA", "Modification"],
        },
        {
            'title': "Payment Terms in Commercial Contracts",
            'content': "Payment terms specify invoicing, due dates, late fees, and dispute resolution for amounts owed under commercial contracts.",
            'tags': ["Payment", "Terms", "Commercial Contracts"],
        },
        {
            'title': "Governing Law Clauses",
            'content': "Governing law clauses identify the legal system that will interpret and enforce the contract. They are critical for cross-border transactions.",
            'tags': ["Governing Law", "Jurisdiction", "Commercial Contracts"],
        },
        {
            'title': "Dispute Resolution Procedures",
            'content': "Dispute resolution procedures may include negotiation, mediation, arbitration, or litigation. Contracts often specify the preferred method and process.",
            'tags': ["Dispute Resolution", "Procedures", "Commercial Contracts"],
        },
        {
            'title': "Retention of Title Clauses",
            'content': "Retention of title clauses allow sellers to retain ownership of goods until payment is made. They protect sellers in insolvency situations.",
            'tags': ["Retention of Title", "Ownership", "Sale of Goods"],
        },
        {
            'title': "Audit Rights in Commercial Agreements",
            'content': "Audit rights clauses permit one party to inspect records or operations to verify compliance with contract terms, such as payment or confidentiality.",
            'tags': ["Audit Rights", "Compliance", "Commercial Agreements"],
        },
        {
            'title': "Subcontracting in Services Contracts",
            'content': "Subcontracting clauses address whether and how a party may delegate performance to third parties. They may require consent and impose liability.",
            'tags': ["Subcontracting", "Services", "Delegation"],
        },
        {
            'title': "Escrow Arrangements for Software",
            'content': "Escrow arrangements protect licensees by requiring software source code to be deposited with a neutral third party, released upon specified events.",
            'tags': ["Escrow", "Software", "License"],
        },
        {
            'title': "Insurance Requirements in Commercial Contracts",
            'content': "Insurance clauses require parties to maintain specified types and amounts of insurance, such as liability, property, or cyber coverage.",
            'tags': ["Insurance", "Requirements", "Commercial Contracts"],
        },
        {
            'title': "Performance Bonds in Supply Agreements",
            'content': "Performance bonds guarantee fulfillment of contractual obligations. They provide financial security to the obligee if the obligor defaults.",
            'tags': ["Performance Bond", "Supply Agreements", "Security"],
        },
        {
            'title': "Data Protection Clauses in SaaS Agreements",
            'content': "Data protection clauses address privacy, security, and compliance with laws such as GDPR. They specify responsibilities and remedies for data breaches.",
            'tags': ["Data Protection", "SaaS", "Privacy"],
        },
        {
            'title': "Termination for Cause Clauses",
            'content': "Termination for cause clauses allow a party to end the contract for specified breaches or events, such as insolvency or failure to perform.",
            'tags': ["Termination", "Cause", "Commercial Contracts"],
        },
        {
            'title': "Non-Compete Clauses in Commercial Agreements",
            'content': "Non-compete clauses restrict parties from engaging in competing activities for a defined period and territory. Enforceability varies by jurisdiction.",
            'tags': ["Non-Compete", "Restriction", "Commercial Agreements"],
        },
        {
            'title': "Assignment of Intellectual Property Rights",
            'content': "Assignment clauses transfer ownership of intellectual property from one party to another. They must be clear and comply with statutory requirements.",
            'tags': ["Assignment", "Intellectual Property", "Ownership"],
        },
        {
            'title': "Service Level Agreements (SLAs)",
            'content': "SLAs define performance standards, metrics, and remedies for failure to meet service levels in SaaS and outsourcing contracts.",
            'tags': ["SLA", "Performance", "Services"],
        },
    ]
    for doc in docs:
        idx.add_document(doc['title'], doc['content'], doc['tags'])