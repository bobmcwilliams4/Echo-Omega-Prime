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
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.inverted_index: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            token_counts = Counter(tokens)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            for token, count in token_counts.items():
                self.inverted_index[token][doc.id] = count
                self.term_doc_freqs[token] += 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        candidate_docs = set()
        for token in query_tokens:
            candidate_docs.update(self.inverted_index.get(token, {}).keys())
        scored_results: List[Tuple[str, float]] = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(query_tokens, doc_id)
            tfidf_score = self._score_tfidf(query_tokens, doc_id)
            doc = self.documents[doc_id]
            score = bm25_score * 0.7 + tfidf_score * 0.3
            score *= doc.weight
            scored_results.append((doc_id, score))
        scored_results.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored_results[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, any]:
        return {
            "total_documents": self.total_docs,
            "avg_doc_length": self.avg_doc_length,
            "unique_terms": len(self.term_doc_freqs),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_tokens: List[str], doc_id: str) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        for term in set(query_tokens):
            if doc_id not in self.inverted_index.get(term, {}):
                continue
            f = self.inverted_index[term][doc_id]
            idf = self._compute_idf(term)
            denom = f + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_length / (self.avg_doc_length or 1))
            term_score = idf * (f * (self._bm25_k1 + 1)) / (denom + 1e-10)
            score += term_score
        return score

    def _score_tfidf(self, query_tokens: List[str], doc_id: str) -> float:
        tfidf = 0.0
        doc_length = self.doc_lengths.get(doc_id, 1)
        for term in set(query_tokens):
            tf = self.inverted_index.get(term, {}).get(doc_id, 0) / doc_length
            idf = self._compute_idf(term)
            tfidf += tf * idf
        return tfidf

    def _make_snippet(self, content: str, query_tokens: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            snippet_tokens = tokens[:window]
        else:
            start = max(positions[0] - window // 2, 0)
            end = min(start + window, len(tokens))
            snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for qt in set(query_tokens):
            snippet = re.sub(r'\b(' + re.escape(qt) + r')\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    if _search_index_instance is None:
        with _search_index_lock:
            if _search_index_instance is None:
                idx = SearchIndex()
                _seed_documents(idx)
                _search_index_instance = idx
    return _search_index_instance

def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            id="1",
            title="Texas Administrative Procedure Act: Rulemaking Overview",
            content="The Texas Administrative Procedure Act (APA) governs the process by which state agencies propose and adopt rules. Agencies must provide public notice, allow for comment, and file rules with the Secretary of State. The APA ensures transparency and public participation in agency rulemaking.",
            tags=["APA", "Rulemaking", "Transparency"],
            weight=1.0
        ),
        SearchDocument(
            id="2",
            title="Railroad Commission: Oil and Gas Regulation",
            content="The Railroad Commission of Texas regulates oil and gas exploration, production, and transportation. Operators must obtain permits, comply with environmental standards, and report production data. The Commission enforces rules to protect public safety and natural resources.",
            tags=["Railroad Commission", "Oil and Gas", "Permitting"],
            weight=1.0
        ),
        SearchDocument(
            id="3",
            title="TCEQ: Environmental Permitting Procedures",
            content="The Texas Commission on Environmental Quality (TCEQ) issues permits for air, water, and waste activities. Applicants must submit detailed plans, undergo technical review, and may be subject to contested case hearings. TCEQ enforces compliance through inspections and penalties.",
            tags=["TCEQ", "Permitting", "Enforcement"],
            weight=1.0
        ),
        SearchDocument(
            id="4",
            title="Texas Department of Insurance: Regulatory Authority",
            content="The Texas Department of Insurance (TDI) oversees the insurance industry, including licensing, rate approval, and consumer protection. TDI promulgates rules, investigates violations, and may impose administrative penalties or revoke licenses.",
            tags=["Insurance", "TDI", "Licensing"],
            weight=1.0
        ),
        SearchDocument(
            id="5",
            title="State Occupational Licensing Requirements",
            content="Many professions in Texas require state-issued licenses. Licensing boards establish qualifications, administer exams, and enforce standards. Applicants may appeal denials through administrative hearings.",
            tags=["Licensing", "Occupational", "Hearings"],
            weight=1.0
        ),
        SearchDocument(
            id="6",
            title="SOAH: Contested Case Hearing Procedures",
            content="The State Office of Administrative Hearings (SOAH) conducts contested case hearings for various agencies. Parties have the right to present evidence, cross-examine witnesses, and receive a written decision. SOAH ensures due process in administrative disputes.",
            tags=["SOAH", "Hearings", "Due Process"],
            weight=1.0
        ),
        SearchDocument(
            id="7",
            title="State Preemption of Local Regulation",
            content="Texas law may preempt local ordinances when state statutes occupy the field. Courts examine legislative intent and conflicts between state and local rules. Preemption ensures statewide uniformity but may limit local autonomy.",
            tags=["Preemption", "Local Regulation", "Uniformity"],
            weight=1.0
        ),
        SearchDocument(
            id="8",
            title="Public Utility Commission: Electric and Telecom Regulation",
            content="The Public Utility Commission of Texas (PUC) regulates electric and telecommunications utilities. The PUC sets rates, resolves consumer complaints, and enforces service quality standards. Utilities must comply with PUC rules and orders.",
            tags=["PUC", "Utilities", "Telecom"],
            weight=1.0
        ),
        SearchDocument(
            id="9",
            title="TABC: Alcoholic Beverage Regulation",
            content="The Texas Alcoholic Beverage Commission (TABC) licenses and regulates the manufacture, distribution, and sale of alcoholic beverages. TABC enforces age restrictions, investigates violations, and may suspend or revoke permits.",
            tags=["TABC", "Alcohol", "Licensing"],
            weight=1.0
        ),
        SearchDocument(
            id="10",
            title="Agency Enabling Statute Interpretation",
            content="Agencies derive their authority from enabling statutes. Courts interpret ambiguous statutory language using legislative history and agency expertise. Limits on agency power are strictly construed.",
            tags=["Statutes", "Interpretation", "Agency Authority"],
            weight=1.0
        ),
        SearchDocument(
            id="11",
            title="Texas Open Records Act: Agency Transparency",
            content="The Texas Public Information Act (Open Records Act) requires agencies to disclose public records upon request, subject to exceptions for confidential information. Agencies must respond promptly and may seek Attorney General opinions on disclosure.",
            tags=["Open Records", "Transparency", "Disclosure"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="Due Process in Administrative Proceedings",
            content="Administrative proceedings must afford due process, including notice, an opportunity to be heard, and an impartial decision-maker. Agencies must follow procedural rules and provide written findings.",
            tags=["Due Process", "Hearings", "Procedures"],
            weight=1.0
        ),
        SearchDocument(
            id="13",
            title="Judicial Review of Agency Actions",
            content="Parties aggrieved by agency decisions may seek judicial review in district court. Courts review the administrative record for substantial evidence and may reverse decisions that are arbitrary or exceed statutory authority.",
            tags=["Judicial Review", "Agency Actions", "Appeals"],
            weight=1.0
        ),
        SearchDocument(
            id="14",
            title="Texas Ethics Commission: Campaign and Lobbying Regulation",
            content="The Texas Ethics Commission enforces campaign finance and lobbying laws. Candidates and lobbyists must file periodic reports. The Commission investigates complaints and may assess civil penalties.",
            tags=["Ethics", "Campaign Finance", "Lobbying"],
            weight=1.0
        ),
        SearchDocument(
            id="15",
            title="Workers Compensation Commission: Oversight and Enforcement",
            content="The Texas Department of Insurance, Division of Workers’ Compensation, oversees the workers’ compensation system. The Commission resolves benefit disputes, enforces employer compliance, and investigates fraud.",
            tags=["Workers Compensation", "Oversight", "Enforcement"],
            weight=1.0
        ),
        SearchDocument(
            id="16",
            title="State Procurement and Competitive Bidding",
            content="State agencies must follow competitive bidding procedures for procurement of goods and services. The Texas Comptroller oversees procurement policy, and agencies must document the selection process and award contracts to the lowest responsible bidder.",
            tags=["Procurement", "Bidding", "Contracts"],
            weight=1.0
        ),
        SearchDocument(
            id="17",
            title="Cooperative Federalism: State Program Delegation",
            content="Texas agencies may administer federal programs under cooperative federalism. State implementation must comply with federal standards, and agencies may receive federal funding contingent on program performance.",
            tags=["Federalism", "Delegation", "Federal Programs"],
            weight=1.0
        ),
        SearchDocument(
            id="18",
            title="Dormant Commerce Clause and State Regulation",
            content="The Dormant Commerce Clause limits state regulation that discriminates against or unduly burdens interstate commerce. Texas laws challenged under this doctrine are subject to judicial scrutiny.",
            tags=["Commerce Clause", "Interstate", "State Regulation"],
            weight=1.0
        ),
        SearchDocument(
            id="19",
            title="Attorney General: Enforcement and Legal Opinions",
            content="The Texas Attorney General enforces state laws and issues legal opinions to agencies and officials. Opinions are advisory but often guide agency action. The Attorney General may represent agencies in litigation.",
            tags=["Attorney General", "Enforcement", "Opinions"],
            weight=1.0
        ),
        SearchDocument(
            id="20",
            title="APA Notice and Comment Requirements",
            content="The APA requires agencies to publish proposed rules in the Texas Register and allow public comment. Agencies must consider comments and may revise rules before adoption.",
            tags=["APA", "Notice", "Comment"],
            weight=1.0
        ),
        SearchDocument(
            id="21",
            title="Emergency Rulemaking under the APA",
            content="Agencies may adopt emergency rules without prior notice or comment if necessary to protect public health, safety, or welfare. Emergency rules are temporary and must be justified in writing.",
            tags=["APA", "Emergency", "Rulemaking"],
            weight=1.0
        ),
        SearchDocument(
            id="22",
            title="Rule Challenge Procedures",
            content="Interested persons may challenge the validity of agency rules in court. Courts may invalidate rules that exceed statutory authority or fail to comply with procedural requirements.",
            tags=["Rule Challenge", "Judicial Review", "Procedures"],
            weight=1.0
        ),
        SearchDocument(
            id="23",
            title="Open Meetings Act: Agency Decision-Making",
            content="The Texas Open Meetings Act requires that agency meetings be open to the public, with advance notice of topics. Certain matters may be discussed in closed session, but final actions must be taken in public.",
            tags=["Open Meetings", "Transparency", "Agency"],
            weight=1.0
        ),
        SearchDocument(
            id="24",
            title="Administrative Subpoenas and Investigations",
            content="Agencies may issue subpoenas to compel testimony or documents during investigations. Recipients may challenge subpoenas as overbroad or burdensome.",
            tags=["Subpoena", "Investigation", "Agency"],
            weight=1.0
        ),
        SearchDocument(
            id="25",
            title="Contested Case Hearings: Evidence and Burden of Proof",
            content="In contested case hearings, the agency or applicant bears the burden of proof. Parties may present evidence, call witnesses, and cross-examine. The administrative law judge issues findings of fact and conclusions of law.",
            tags=["Contested Case", "Evidence", "Hearings"],
            weight=1.0
        ),
        SearchDocument(
            id="26",
            title="Judicial Deference to Agency Interpretation",
            content="Texas courts may defer to reasonable agency interpretations of ambiguous statutes, especially when the agency has special expertise. However, courts retain the final authority to interpret the law.",
            tags=["Deference", "Interpretation", "Agency"],
            weight=1.0
        ),
        SearchDocument(
            id="27",
            title="Rulemaking Petitions and Public Participation",
            content="Any interested person may petition a state agency to adopt, amend, or repeal a rule. Agencies must consider petitions and respond in writing, promoting public participation in rulemaking.",
            tags=["Petition", "Rulemaking", "Participation"],
            weight=1.0
        ),
        SearchDocument(
            id="28",
            title="Administrative Record: Contents and Preservation",
            content="The administrative record includes all materials considered by the agency in making a decision. The record must be preserved for judicial review and may include transcripts, exhibits, and staff reports.",
            tags=["Administrative Record", "Preservation", "Review"],
            weight=1.0
        ),
        SearchDocument(
            id="29",
            title="Sanctions and Penalties in Agency Proceedings",
            content="Agencies may impose sanctions or penalties for violations of statutes or rules. Penalties may include fines, license suspension, or revocation. Due process protections apply.",
            tags=["Sanctions", "Penalties", "Agency"],
            weight=1.0
        ),
        SearchDocument(
            id="30",
            title="Alternative Dispute Resolution in Administrative Law",
            content="Agencies may use mediation or other alternative dispute resolution (ADR) methods to resolve disputes. ADR can reduce costs and expedite resolution compared to formal hearings.",
            tags=["ADR", "Mediation", "Dispute Resolution"],
            weight=1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)