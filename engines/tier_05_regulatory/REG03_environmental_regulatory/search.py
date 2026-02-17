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

# --- Search Index Implementation ---

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_tokens: Dict[int, List[str]] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.inverted_index: Dict[str, List[int]] = defaultdict(list)
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[Tuple[int, str], float] = {}
        self.k1 = 1.5
        self.b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_tokens[doc.id] = tokens
            self.doc_lengths[doc.id] = len(tokens)
            for token in set(tokens):
                self.inverted_index[token].append(doc.id)
                self.term_doc_freq[token] += 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        candidate_docs = set()
        for token in query_tokens:
            candidate_docs.update(self.inverted_index.get(token, []))
        scored_results = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            doc = self.documents[doc_id]
            final_score = bm25_score * 0.7 + tfidf_score * 0.3
            snippet = self._make_snippet(doc.content, query_tokens)
            scored_results.append(SearchResult(doc_id, final_score * doc.weight, doc.title, snippet))
        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:limit]

    def get_stats(self) -> Dict[str, float]:
        return {
            "total_docs": self.total_docs,
            "avg_doc_length": self.avg_doc_length,
            "unique_terms": len(self.inverted_index),
        }

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return [t for t in tokens if t not in _STOPWORDS]

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_tokens: List[str]) -> float:
        doc_tokens = self.doc_tokens[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        freq = Counter(doc_tokens)
        for term in query_tokens:
            if term not in freq:
                continue
            idf = self._compute_idf(term)
            tf = freq[term]
            denom = tf + self.k1 * (1 - self.b + self.b * doc_len / (self.avg_doc_length + 1e-9))
            score += idf * ((tf * (self.k1 + 1)) / (denom + 1e-9))
        return score

    def _score_tfidf(self, doc_id: int, query_tokens: List[str]) -> float:
        doc_tokens = self.doc_tokens[doc_id]
        doc_len = self.doc_lengths[doc_id]
        freq = Counter(doc_tokens)
        score = 0.0
        for term in query_tokens:
            cache_key = (doc_id, term)
            if cache_key in self._tfidf_cache:
                tfidf = self._tfidf_cache[cache_key]
            else:
                tf = freq[term] / doc_len if doc_len > 0 else 0.0
                idf = self._compute_idf(term)
                tfidf = tf * idf
                self._tfidf_cache[cache_key] = tfidf
            score += tfidf
        return score

    def _make_snippet(self, content: str, query_tokens: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            return content[:160] + "..." if len(content) > 160 else content
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for qt in set(query_tokens):
            snippet = re.sub(r'\b({})\b'.format(re.escape(qt)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + "..."

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

# --- Stopwords ---

_STOPWORDS = set("""
the and of a to in for on with by at from as is are be this that which or an under section part title
""".split())

# --- Pre-seeded Domain Documents ---

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "CAA Title V Operating Permit Overview",
            "Title V of the Clean Air Act (CAA) requires major sources of air pollutants to obtain operating permits. The Title V permit program consolidates all applicable requirements into a single document and ensures compliance with emission standards.",
            ["CAA", "Title V", "Air Permits"],
            1.0
        ),
        SearchDocument(
            2,
            "CWA Section 402 NPDES Permitting Process",
            "Section 402 of the Clean Water Act establishes the National Pollutant Discharge Elimination System (NPDES) permitting program, regulating point source discharges to waters of the United States. Facilities must apply for NPDES permits to discharge pollutants.",
            ["CWA", "NPDES", "Water Permits"],
            1.0
        ),
        SearchDocument(
            3,
            "RCRA Subtitle C: Hazardous Waste Management",
            "Subtitle C of the Resource Conservation and Recovery Act (RCRA) governs the generation, transportation, treatment, storage, and disposal of hazardous waste. Facilities must comply with cradle-to-grave tracking and obtain EPA identification numbers.",
            ["RCRA", "Hazardous Waste"],
            1.0
        ),
        SearchDocument(
            4,
            "CERCLA Section 107: Liability Provisions",
            "Section 107 of CERCLA (Superfund) imposes liability on potentially responsible parties (PRPs) for releases of hazardous substances. Liability is strict, joint and several, and retroactive. PRPs may include current and former owners and operators.",
            ["CERCLA", "Superfund", "Liability"],
            1.0
        ),
        SearchDocument(
            5,
            "NEPA Environmental Impact Statement (EIS) Requirements",
            "The National Environmental Policy Act (NEPA) requires federal agencies to prepare Environmental Impact Statements (EIS) for major federal actions significantly affecting the quality of the human environment. The EIS process includes public participation and alternatives analysis.",
            ["NEPA", "EIS", "Environmental Review"],
            1.0
        ),
        SearchDocument(
            6,
            "ESA Section 7 Consultation Procedures",
            "Section 7 of the Endangered Species Act (ESA) requires federal agencies to consult with the U.S. Fish and Wildlife Service or NOAA Fisheries to ensure that actions do not jeopardize listed species or destroy critical habitat.",
            ["ESA", "Consultation", "Wildlife"],
            1.0
        ),
        SearchDocument(
            7,
            "TSCA Chemical Regulation and PMN Requirements",
            "The Toxic Substances Control Act (TSCA) regulates the manufacture, import, processing, and distribution of chemical substances. Pre-Manufacture Notice (PMN) is required for new chemicals not listed on the TSCA Inventory.",
            ["TSCA", "Chemicals", "PMN"],
            1.0
        ),
        SearchDocument(
            8,
            "EPCRA Tier II Chemical Inventory Reporting",
            "The Emergency Planning and Community Right-to-Know Act (EPCRA) requires facilities to submit Tier II reports on hazardous chemical inventories to state and local authorities, enhancing emergency preparedness and public awareness.",
            ["EPCRA", "Tier II", "Reporting"],
            1.0
        ),
        SearchDocument(
            9,
            "TCEQ Air Permitting in Texas",
            "The Texas Commission on Environmental Quality (TCEQ) issues air permits for construction and operation of facilities emitting air contaminants. Permitting ensures compliance with state and federal air quality standards.",
            ["TCEQ", "Air Permits", "Texas"],
            1.0
        ),
        SearchDocument(
            10,
            "Railroad Commission Rule 8: Oil and Gas Waste Disposal",
            "Texas Railroad Commission Rule 8 regulates the disposal of oil and gas wastes, including requirements for pit design, liner installation, and waste tracking. Operators must obtain permits for waste disposal activities.",
            ["Railroad Commission", "Rule 8", "Waste Disposal"],
            1.0
        ),
        SearchDocument(
            11,
            "NRC Radioactive Materials Licensing",
            "The Nuclear Regulatory Commission (NRC) licenses the possession and use of radioactive materials. Applicants must demonstrate radiation safety, security, and compliance with NRC regulations.",
            ["NRC", "Radioactive Materials", "Licensing"],
            1.0
        ),
        SearchDocument(
            12,
            "Spill Reporting under the National Contingency Plan (NCP)",
            "The National Oil and Hazardous Substances Pollution Contingency Plan (NCP) outlines procedures for reporting and responding to oil and hazardous substance spills. Facilities must notify the National Response Center (NRC) immediately upon a release.",
            ["NCP", "Spill Reporting", "CERCLA"],
            1.0
        ),
        SearchDocument(
            13,
            "CERCLA Remedial Investigation/Feasibility Study (RI/FS)",
            "The RI/FS process under CERCLA evaluates the nature and extent of contamination and develops and compares remedial alternatives for Superfund sites.",
            ["CERCLA", "RI/FS", "Superfund"],
            1.0
        ),
        SearchDocument(
            14,
            "CAA Title V Permit Renewal and Modification",
            "Title V operating permits must be renewed every five years. Modifications may be required for changes in facility operations, emissions, or applicable requirements.",
            ["CAA", "Title V", "Renewal"],
            1.0
        ),
        SearchDocument(
            15,
            "CWA NPDES Stormwater Permitting",
            "NPDES permits are required for stormwater discharges from industrial activities, construction sites, and municipal separate storm sewer systems (MS4s). Best management practices (BMPs) are often required.",
            ["CWA", "NPDES", "Stormwater"],
            1.0
        ),
        SearchDocument(
            16,
            "RCRA Generator Categories and Requirements",
            "RCRA classifies hazardous waste generators as very small, small, or large quantity generators, each with specific accumulation, storage, and reporting requirements.",
            ["RCRA", "Generators", "Hazardous Waste"],
            1.0
        ),
        SearchDocument(
            17,
            "NEPA Categorical Exclusions (CEs)",
            "Certain federal actions may be categorically excluded from NEPA analysis if they do not individually or cumulatively have a significant effect on the environment.",
            ["NEPA", "Categorical Exclusion"],
            1.0
        ),
        SearchDocument(
            18,
            "ESA Section 9: Prohibited Acts",
            "Section 9 of the ESA prohibits the take of endangered species, including harassing, harming, pursuing, hunting, shooting, wounding, killing, trapping, capturing, or collecting.",
            ["ESA", "Section 9", "Prohibited Acts"],
            1.0
        ),
        SearchDocument(
            19,
            "TSCA Risk Evaluation Process",
            "TSCA requires EPA to prioritize, evaluate, and regulate risks from existing chemicals. The risk evaluation process includes hazard assessment, exposure assessment, and risk characterization.",
            ["TSCA", "Risk Evaluation"],
            1.0
        ),
        SearchDocument(
            20,
            "EPCRA Section 313 Toxic Release Inventory (TRI)",
            "Facilities meeting certain thresholds must report releases of listed toxic chemicals under EPCRA Section 313, supporting the Toxic Release Inventory (TRI) database.",
            ["EPCRA", "TRI", "Section 313"],
            1.0
        ),
        SearchDocument(
            21,
            "TCEQ New Source Review (NSR) Permitting",
            "NSR permits are required for new or modified sources of air emissions in Texas. The review ensures that new sources will not cause or contribute to a violation of air quality standards.",
            ["TCEQ", "NSR", "Air Permits"],
            1.0
        ),
        SearchDocument(
            22,
            "Railroad Commission Oil Spill Response",
            "The Railroad Commission of Texas oversees oil spill response and cleanup for oil and gas exploration and production activities.",
            ["Railroad Commission", "Oil Spill", "Texas"],
            1.0
        ),
        SearchDocument(
            23,
            "NRC Decommissioning of Nuclear Facilities",
            "Decommissioning is the safe removal of a nuclear facility from service and reduction of residual radioactivity to a level that permits release of the property for unrestricted use.",
            ["NRC", "Decommissioning", "Nuclear"],
            1.0
        ),
        SearchDocument(
            24,
            "CERCLA Removal Actions",
            "Removal actions under CERCLA are short-term responses to releases or threatened releases of hazardous substances that require prompt action.",
            ["CERCLA", "Removal", "Superfund"],
            1.0
        ),
        SearchDocument(
            25,
            "Spill Reporting under CERCLA Section 103",
            "Section 103 of CERCLA requires immediate reporting of releases of hazardous substances above reportable quantities to the National Response Center.",
            ["CERCLA", "Spill Reporting", "Section 103"],
            1.0
        ),
        SearchDocument(
            26,
            "CAA Title V Compliance Certification",
            "Facilities with Title V permits must submit annual compliance certifications, documenting compliance with all permit terms and conditions.",
            ["CAA", "Title V", "Compliance"],
            1.0
        ),
        SearchDocument(
            27,
            "CWA Section 401 Water Quality Certification",
            "Section 401 of the Clean Water Act requires applicants for federal permits or licenses to obtain state water quality certification, ensuring compliance with state water quality standards.",
            ["CWA", "Section 401", "Water Quality"],
            1.0
        ),
        SearchDocument(
            28,
            "TSCA Significant New Use Rule (SNUR)",
            "EPA may require notification before chemicals are used in new ways that might create concerns, under the Significant New Use Rule (SNUR) provisions of TSCA.",
            ["TSCA", "SNUR", "Chemicals"],
            1.0
        ),
        SearchDocument(
            29,
            "EPCRA Emergency Planning Notification",
            "EPCRA requires facilities to notify state and local authorities of the presence of extremely hazardous substances above threshold planning quantities.",
            ["EPCRA", "Emergency Planning"],
            1.0
        ),
        SearchDocument(
            30,
            "TCEQ Air Emissions Inventory Reporting",
            "Facilities in Texas must submit annual emissions inventories to TCEQ, detailing the types and amounts of air contaminants emitted.",
            ["TCEQ", "Emissions Inventory", "Air"],
            1.0
        ),
        SearchDocument(
            31,
            "Railroad Commission Rule 8 Pit Closure",
            "Operators must properly close and remediate waste pits used for oil and gas operations under Rule 8.",
            ["Railroad Commission", "Rule 8", "Pit Closure"],
            1.0
        ),
        SearchDocument(
            32,
            "NRC Radioactive Waste Disposal",
            "Disposal of radioactive waste is regulated by NRC to protect public health and safety. Requirements include waste classification, packaging, and disposal site licensing.",
            ["NRC", "Radioactive Waste", "Disposal"],
            1.0
        ),
        SearchDocument(
            33,
            "NEPA Environmental Assessment (EA)",
            "An Environmental Assessment (EA) is prepared under NEPA to determine whether a federal action has the potential to cause significant environmental effects.",
            ["NEPA", "EA", "Environmental Review"],
            1.0
        ),
        SearchDocument(
            34,
            "CERCLA Potentially Responsible Parties (PRPs)",
            "PRPs under CERCLA may include current and former owners, operators, arrangers, and transporters associated with hazardous substance releases.",
            ["CERCLA", "PRP", "Superfund"],
            1.0
        ),
        SearchDocument(
            35,
            "CWA NPDES Permit Monitoring and Reporting",
            "NPDES permit holders must monitor discharges and submit regular reports to regulatory agencies, demonstrating compliance with permit limits.",
            ["CWA", "NPDES", "Monitoring"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)