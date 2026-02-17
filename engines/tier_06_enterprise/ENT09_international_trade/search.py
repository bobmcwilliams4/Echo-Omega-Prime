import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Any, Optional

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
        self.doc_lengths: Dict[int, int] = {}
        self.term_doc_freqs: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.doc_tags: Dict[int, List[str]] = {}
        self.doc_weights: Dict[int, float] = {}
        self.total_docs: int = 0
        self.avg_doc_length: float = 0.0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.term_freqs[doc.id] = Counter(tokens)
            self.doc_tags[doc.id] = doc.tags
            self.doc_weights[doc.id] = doc.weight
            for term in self.term_freqs[doc.id]:
                self.term_doc_freqs[term][doc.id] = self.term_freqs[doc.id][term]
            self.total_docs += 1
            self.avg_doc_length = (
                sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            )
            self.idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = len(self.term_doc_freqs.get(term, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        weight = self.doc_weights.get(doc_id, 1.0)
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            idf = self._compute_idf(term)
            numerator = tf * (self._bm25_k1 + 1)
            denominator = tf + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_length / self.avg_doc_length)
            if denominator == 0:
                continue
            score += idf * numerator / denominator
        return score * weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        weight = self.doc_weights.get(doc_id, 1.0)
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            if doc_length == 0:
                continue
            norm_tf = tf / doc_length
            idf = self._compute_idf(term)
            score += norm_tf * idf
        return score * weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_doc_ids = set()
        for term in query_terms:
            candidate_doc_ids.update(self.term_doc_freqs.get(term, {}).keys())
        scores = {}
        for doc_id in candidate_doc_ids:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                scores[doc_id] = score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._generate_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _generate_snippet(self, content: str, query_terms: List[str], max_length: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = ' '.join(tokens[:max_length])
        else:
            start = max(positions[0] - 10, 0)
            end = min(start + max_length, len(tokens))
            snippet = ' '.join(tokens[start:end])
        return snippet[:max_length] + ('...' if len(snippet) > max_length else '')

    def get_stats(self) -> Dict[str, Any]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freqs),
        }

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "EAR Export License Requirements",
            "The Export Administration Regulations (EAR) require exporters to determine if a license is needed for their product based on the Commerce Control List (CCL), destination country, end-user, and end-use. License exceptions may apply, but exporters must screen for embargoed countries and denied parties.",
            ["EAR", "Export License", "CCL", "Compliance"],
            1.0
        ),
        SearchDocument(
            2,
            "ITAR Defense Articles Control",
            "International Traffic in Arms Regulations (ITAR) governs the export and import of defense articles and services listed on the United States Munitions List (USML). Registration with DDTC is mandatory for manufacturers, exporters, and brokers. Violations may result in severe penalties.",
            ["ITAR", "USML", "Defense Articles", "DDTC"],
            1.0
        ),
        SearchDocument(
            3,
            "OFAC Sanctions Compliance",
            "The Office of Foreign Assets Control (OFAC) administers and enforces economic and trade sanctions against targeted foreign countries, terrorists, and narcotics traffickers. Companies must screen transactions and customers against OFAC lists to avoid prohibited dealings.",
            ["OFAC", "Sanctions", "Compliance", "Screening"],
            1.0
        ),
        SearchDocument(
            4,
            "HTS Classification and Tariffs",
            "The Harmonized Tariff Schedule (HTS) provides codes for classifying imported goods. Accurate classification determines tariff rates and eligibility for trade programs. Customs brokers assist in proper HTS assignment and tariff calculation.",
            ["HTS", "Tariffs", "Classification", "Customs"],
            1.0
        ),
        SearchDocument(
            5,
            "FCPA Anti-Bribery Provisions",
            "The Foreign Corrupt Practices Act (FCPA) prohibits bribery of foreign officials and mandates accurate recordkeeping. Companies must implement compliance programs to prevent and detect violations, which can result in criminal and civil penalties.",
            ["FCPA", "Anti-Bribery", "Compliance", "Recordkeeping"],
            1.0
        ),
        SearchDocument(
            6,
            "USMCA Rules of Origin",
            "The United States-Mexico-Canada Agreement (USMCA) establishes rules of origin for goods to qualify for preferential tariff treatment. Documentation and certification are required to prove eligibility, and audits may verify compliance.",
            ["USMCA", "Rules of Origin", "Tariffs", "Certification"],
            1.0
        ),
        SearchDocument(
            7,
            "Antidumping and Countervailing Duties",
            "Antidumping duties are imposed on imports sold below fair market value, while countervailing duties address subsidized goods. Importers must be aware of applicable orders and deposit requirements to avoid penalties.",
            ["Antidumping", "Countervailing", "Duties", "Trade Remedies"],
            1.0
        ),
        SearchDocument(
            8,
            "Section 301 Tariffs on China",
            "Section 301 of the Trade Act authorizes tariffs on Chinese imports in response to unfair trade practices. The USTR maintains lists of affected products, and importers must check HTS codes for applicability.",
            ["Section 301", "China", "Tariffs", "USTR"],
            1.0
        ),
        SearchDocument(
            9,
            "Section 232 Steel and Aluminum Tariffs",
            "Section 232 tariffs are imposed on steel and aluminum imports to protect national security. Exclusions may be requested, and importers must comply with quota and licensing requirements.",
            ["Section 232", "Steel", "Aluminum", "Tariffs"],
            1.0
        ),
        SearchDocument(
            10,
            "Foreign Trade Zones (FTZ)",
            "Foreign Trade Zones allow companies to defer, reduce, or eliminate customs duties on imported goods. FTZs provide operational flexibility and cost savings, but compliance with zone regulations is essential.",
            ["FTZ", "Customs", "Duty Deferral", "Compliance"],
            1.0
        ),
        SearchDocument(
            11,
            "Customs Valuation Transaction Value",
            "Customs valuation determines the dutiable value of imported goods, typically based on transaction value. Proper documentation and disclosure of assists, royalties, and related party transactions are required.",
            ["Customs Valuation", "Transaction Value", "Import", "Compliance"],
            1.0
        ),
        SearchDocument(
            12,
            "Deemed Export of Technology and Source Code",
            "A deemed export occurs when controlled technology or source code is released to a foreign national in the U.S. Exporters must assess license requirements under EAR and ITAR for such transfers.",
            ["Deemed Export", "Technology", "Source Code", "EAR", "ITAR"],
            1.0
        ),
        SearchDocument(
            13,
            "Incoterms and Risk of Loss",
            "Incoterms define the responsibilities of buyers and sellers regarding delivery, risk of loss, and costs. Selecting the appropriate Incoterm is critical for contract clarity and risk management.",
            ["Incoterms", "Risk of Loss", "Contracts", "Delivery"],
            1.0
        ),
        SearchDocument(
            14,
            "Voluntary Self-Disclosure of Export Violations",
            "Voluntary self-disclosure to BIS, DDTC, or OFAC can mitigate penalties for export violations. Companies should promptly investigate, document, and report noncompliance to relevant authorities.",
            ["Self-Disclosure", "Export Violations", "BIS", "DDTC", "OFAC"],
            1.0
        ),
        SearchDocument(
            15,
            "Import Licensing and Quota Administration",
            "Certain imports require licenses or are subject to quotas. Agencies such as USDA, FDA, and CBP administer licensing and quota programs. Importers must comply with application and reporting requirements.",
            ["Import Licensing", "Quota", "USDA", "FDA", "CBP"],
            1.0
        ),
        SearchDocument(
            16,
            "Country of Origin Marking Requirements",
            "Imported goods must be marked with their country of origin in accordance with CBP regulations. Failure to comply may result in penalties and denial of entry.",
            ["Country of Origin", "Marking", "CBP", "Compliance"],
            1.0
        ),
        SearchDocument(
            17,
            "Letters of Credit in International Trade",
            "Letters of credit are financial instruments used to secure payment in international trade. They provide assurance to sellers and buyers, but parties must understand terms, conditions, and documentation requirements.",
            ["Letters of Credit", "International Trade", "Payment", "Banking"],
            1.0
        ),
        SearchDocument(
            18,
            "Trade Compliance Audits and Recordkeeping",
            "Trade compliance audits review adherence to export and import regulations. Proper recordkeeping is essential for demonstrating compliance and responding to government inquiries.",
            ["Trade Compliance", "Audits", "Recordkeeping", "Regulations"],
            1.0
        ),
        SearchDocument(
            19,
            "Denied Party Screening",
            "Denied party screening is a critical step in export compliance to ensure transactions do not involve prohibited individuals or entities. Automated tools can help maintain compliance with government lists.",
            ["Denied Party", "Screening", "Export Compliance", "Lists"],
            1.0
        ),
        SearchDocument(
            20,
            "Export Control Classification Number (ECCN)",
            "ECCN identifies items subject to export controls under the EAR. Accurate classification is necessary to determine license requirements and eligibility for exceptions.",
            ["ECCN", "Export Controls", "EAR", "Classification"],
            1.0
        ),
        SearchDocument(
            21,
            "BIS Entity List and Export Restrictions",
            "The Bureau of Industry and Security (BIS) maintains the Entity List, which restricts exports to certain parties. Exporters must check the Entity List and assess license requirements before shipping.",
            ["BIS", "Entity List", "Export Restrictions", "Compliance"],
            1.0
        ),
        SearchDocument(
            22,
            "Export Documentation Requirements",
            "Exporters must prepare and submit required documents such as commercial invoices, packing lists, and export declarations. Proper documentation ensures compliance and facilitates customs clearance.",
            ["Export Documentation", "Compliance", "Customs", "Clearance"],
            1.0
        ),
        SearchDocument(
            23,
            "ITAR Registration and Licensing",
            "ITAR mandates registration with DDTC for manufacturers, exporters, and brokers of defense articles. Licensing is required for exports, and compliance programs must address recordkeeping and reporting.",
            ["ITAR", "DDTC", "Registration", "Licensing"],
            1.0
        ),
        SearchDocument(
            24,
            "OFAC Specially Designated Nationals (SDN) List",
            "OFAC's SDN List identifies individuals and entities subject to sanctions. U.S. persons are prohibited from conducting transactions with SDNs, and screening is mandatory.",
            ["OFAC", "SDN List", "Sanctions", "Screening"],
            1.0
        ),
        SearchDocument(
            25,
            "Customs Broker Responsibilities",
            "Customs brokers facilitate import and export transactions, ensuring compliance with regulations. They assist with classification, valuation, and documentation, and must maintain proper records.",
            ["Customs Broker", "Compliance", "Classification", "Valuation"],
            1.0
        ),
        SearchDocument(
            26,
            "Export Administration Regulations (EAR) Overview",
            "EAR controls dual-use items and technology. Exporters must determine jurisdiction, classify products, and assess license requirements. Violations can result in administrative and criminal penalties.",
            ["EAR", "Dual-Use", "Export Controls", "Compliance"],
            1.0
        ),
        SearchDocument(
            27,
            "ITAR Technical Data Controls",
            "Technical data related to defense articles is controlled under ITAR. Exporters must restrict access to foreign persons and obtain licenses for transfers.",
            ["ITAR", "Technical Data", "Defense Articles", "Licensing"],
            1.0
        ),
        SearchDocument(
            28,
            "OFAC General Licenses",
            "OFAC issues general licenses authorizing certain transactions otherwise prohibited by sanctions. Exporters must review license terms and maintain records of authorized activities.",
            ["OFAC", "General License", "Sanctions", "Recordkeeping"],
            1.0
        ),
        SearchDocument(
            29,
            "Section 301 Exclusion Requests",
            "Importers affected by Section 301 tariffs may submit exclusion requests to USTR. Approved exclusions provide relief from additional duties, but documentation and eligibility criteria apply.",
            ["Section 301", "Exclusion", "USTR", "Tariffs"],
            1.0
        ),
        SearchDocument(
            30,
            "Foreign Trade Zone Activation Process",
            "Companies seeking FTZ status must apply to the Foreign-Trade Zones Board and comply with activation procedures. FTZs offer duty savings, but require strict compliance and reporting.",
            ["FTZ", "Activation", "Duty Savings", "Compliance"],
            1.0
        ),
        SearchDocument(
            31,
            "Customs Entry Procedures",
            "Importers must file entry documents with CBP to clear goods through customs. Accurate classification, valuation, and payment of duties are required for compliance.",
            ["Customs Entry", "CBP", "Classification", "Valuation"],
            1.0
        ),
        SearchDocument(
            32,
            "Incoterms 2020 Updates",
            "Incoterms 2020 introduced changes to delivery terms, insurance requirements, and risk allocation. Parties should update contracts to reflect new Incoterms for clarity and compliance.",
            ["Incoterms", "2020", "Delivery Terms", "Contracts"],
            1.0
        ),
        SearchDocument(
            33,
            "FCPA Books and Records Requirements",
            "FCPA requires companies to maintain accurate books and records and implement internal controls to prevent bribery. Violations may result in enforcement actions and fines.",
            ["FCPA", "Books and Records", "Internal Controls", "Compliance"],
            1.0
        ),
        SearchDocument(
            34,
            "USMCA Certification of Origin",
            "USMCA requires certification of origin for goods seeking preferential treatment. Exporters and importers must retain records and provide certification upon request.",
            ["USMCA", "Certification", "Origin", "Records"],
            1.0
        ),
        SearchDocument(
            35,
            "Antidumping Investigation Process",
            "Antidumping investigations determine whether imports are sold below fair value. The process involves petitions, preliminary determinations, and final orders.",
            ["Antidumping", "Investigation", "Fair Value", "Orders"],
            1.0
        ),
        SearchDocument(
            36,
            "Section 232 Quota Administration",
            "Section 232 quotas limit imports of steel and aluminum. Importers must monitor quota status and comply with CBP reporting requirements.",
            ["Section 232", "Quota", "Steel", "Aluminum"],
            1.0
        ),
        SearchDocument(
            37,
            "Deemed Export License Determination",
            "Exporters must evaluate whether a deemed export requires a license based on technology classification and recipient nationality. EAR and ITAR provide guidance for license determination.",
            ["Deemed Export", "License", "EAR", "ITAR"],
            1.0
        ),
        SearchDocument(
            38,
            "Trade Compliance Risk Assessment",
            "Risk assessments identify vulnerabilities in trade compliance programs. Companies should review procedures, training, and screening to mitigate risks.",
            ["Trade Compliance", "Risk Assessment", "Procedures", "Training"],
            1.0
        ),
        SearchDocument(
            39,
            "Voluntary Self-Disclosure Process",
            "The voluntary self-disclosure process involves internal investigation, preparation of disclosure documents, and submission to regulatory agencies. Timely disclosure can reduce penalties.",
            ["Self-Disclosure", "Process", "Export Violations", "Penalties"],
            1.0
        ),
        SearchDocument(
            40,
            "Import Quota Management",
            "Importers must manage quotas by monitoring allocations, submitting applications, and complying with reporting requirements. Failure to comply may result in penalties.",
            ["Import Quota", "Management", "Applications", "Reporting"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)