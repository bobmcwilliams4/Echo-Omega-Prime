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
        self.doc_tokens: Dict[str, List[str]] = {}
        self.inverted_index: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.idf: Dict[str, float] = {}
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._update_needed = True

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.title + " " + doc.content)
            self.doc_tokens[doc.id] = tokens
            self.doc_lengths[doc.id] = len(tokens)
            token_counts = Counter(tokens)
            for token, count in token_counts.items():
                self.inverted_index[token][doc.id] = count
            self.total_docs += 1
            self._update_needed = True

    def _compute_idf(self):
        if not self._update_needed:
            return
        N = self.total_docs
        self.avg_doc_length = sum(self.doc_lengths.values()) / max(1, N)
        self.idf.clear()
        for term, docs in self.inverted_index.items():
            df = len(docs)
            # BM25 idf formula
            idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
            self.idf[term] = idf
        self._update_needed = False

    def _score_bm25(self, query_tokens: List[str], doc_id: str) -> float:
        doc = self.documents[doc_id]
        tokens = self.doc_tokens[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        tf_counts = Counter(tokens)
        self._compute_idf()
        for term in query_tokens:
            if term not in tf_counts:
                continue
            tf = tf_counts[term]
            idf = self.idf.get(term, 0.0)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * (numerator / denominator)
        return score * doc.weight

    def _score_tfidf(self, query_tokens: List[str], doc_id: str) -> float:
        doc = self.documents[doc_id]
        tokens = self.doc_tokens[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tf_counts = Counter(tokens)
        self._compute_idf()
        score = 0.0
        for term in query_tokens:
            tf = tf_counts.get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len
            idf = self.idf.get(term, 0.0)
            score += tf_norm * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        candidate_docs = set()
        for term in query_tokens:
            candidate_docs.update(self.inverted_index.get(term, {}).keys())
        scored_docs: List[Tuple[str, float]] = []
        for doc_id in candidate_docs:
            if use_tfidf:
                score = self._score_tfidf(query_tokens, doc_id)
            else:
                score = self._score_bm25(query_tokens, doc_id)
            if score > 0:
                scored_docs.append((doc_id, score))
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored_docs[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], max_len: int = 160) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if positions:
            start = max(positions[0] - 10, 0)
            end = min(positions[0] + 30, len(tokens))
            snippet_tokens = tokens[start:end]
            snippet = ' '.join(snippet_tokens)
        else:
            snippet = content[:max_len]
        return snippet

    def get_stats(self) -> Dict[str, any]:
        self._compute_idf()
        stats = {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.inverted_index),
        }
        return stats

# Singleton factory
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id="1",
            title="Crude Oil Composition and Classification",
            content="Crude oil is a complex mixture of hydrocarbons, classified based on its sulfur content and API gravity. Major components include paraffins, naphthenes, aromatics, and asphaltenes.",
            tags=["crude oil", "composition", "classification"],
            weight=1.0
        ),
        SearchDocument(
            id="2",
            title="Fractional Distillation in Petroleum Refining",
            content="Fractional distillation separates crude oil into fractions such as gasoline, kerosene, diesel, and lubricating oils based on boiling point differences.",
            tags=["distillation", "refining", "fractions"],
            weight=1.0
        ),
        SearchDocument(
            id="3",
            title="Catalytic Cracking Process",
            content="Catalytic cracking converts heavy fractions into lighter products like gasoline and LPG using zeolite catalysts at high temperatures.",
            tags=["catalytic cracking", "refining", "zeolite"],
            weight=1.0
        ),
        SearchDocument(
            id="4",
            title="Hydrotreating and Hydrocracking",
            content="Hydrotreating removes sulfur, nitrogen, and metals from petroleum fractions. Hydrocracking breaks large molecules into smaller ones using hydrogen and catalysts.",
            tags=["hydrotreating", "hydrocracking", "catalysts"],
            weight=1.0
        ),
        SearchDocument(
            id="5",
            title="Petroleum Chemistry: Alkanes and Cycloalkanes",
            content="Alkanes and cycloalkanes are saturated hydrocarbons found in crude oil. Their chemical stability makes them valuable as fuels.",
            tags=["alkanes", "cycloalkanes", "hydrocarbons"],
            weight=1.0
        ),
        SearchDocument(
            id="6",
            title="Aromatic Hydrocarbons in Petroleum",
            content="Aromatic hydrocarbons such as benzene, toluene, and xylene are present in petroleum and are important feedstocks for the chemical industry.",
            tags=["aromatics", "benzene", "petroleum"],
            weight=1.0
        ),
        SearchDocument(
            id="7",
            title="Sulfur Compounds and Desulfurization",
            content="Sulfur compounds in petroleum cause environmental pollution. Desulfurization processes reduce sulfur content to meet regulatory standards.",
            tags=["sulfur", "desulfurization", "environment"],
            weight=1.0
        ),
        SearchDocument(
            id="8",
            title="Petroleum Refinery Flow Diagram",
            content="A typical petroleum refinery includes units for distillation, cracking, reforming, hydrotreating, and blending to produce finished products.",
            tags=["refinery", "flow diagram", "units"],
            weight=1.0
        ),
        SearchDocument(
            id="9",
            title="Gasoline Production and Octane Rating",
            content="Gasoline is produced by blending various refinery streams. Octane rating measures resistance to knocking and is improved by reforming and blending.",
            tags=["gasoline", "octane", "blending"],
            weight=1.0
        ),
        SearchDocument(
            id="10",
            title="Petrochemical Feedstocks from Petroleum",
            content="Petrochemical feedstocks such as ethylene, propylene, and butadiene are derived from petroleum refining and are used to manufacture plastics and synthetic fibers.",
            tags=["petrochemicals", "feedstocks", "ethylene"],
            weight=1.0
        ),
        SearchDocument(
            id="11",
            title="Environmental Impact of Petroleum Chemistry",
            content="Petroleum chemistry affects the environment through emissions, spills, and waste. Technologies like carbon capture and cleaner fuels mitigate these impacts.",
            tags=["environment", "emissions", "carbon capture"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="Visbreaking and Thermal Cracking",
            content="Visbreaking is a mild thermal cracking process to reduce viscosity of heavy residues. Thermal cracking produces lighter hydrocarbons from heavy fractions.",
            tags=["visbreaking", "thermal cracking", "residues"],
            weight=1.0
        ),
        SearchDocument(
            id="13",
            title="Petroleum Chemistry: Isomerization",
            content="Isomerization rearranges straight-chain hydrocarbons into branched isomers, increasing octane rating of gasoline.",
            tags=["isomerization", "octane", "gasoline"],
            weight=1.0
        ),
        SearchDocument(
            id="14",
            title="Reforming in Petroleum Refining",
            content="Reforming converts low-octane naphtha into high-octane gasoline components and aromatics using platinum catalysts.",
            tags=["reforming", "naphtha", "platinum"],
            weight=1.0
        ),
        SearchDocument(
            id="15",
            title="Petroleum Chemistry: Asphaltenes",
            content="Asphaltenes are high molecular weight components of crude oil, affecting viscosity and stability. Their removal is important in refining.",
            tags=["asphaltenes", "viscosity", "stability"],
            weight=1.0
        ),
        SearchDocument(
            id="16",
            title="Petroleum Chemistry: Gas Processing",
            content="Gas processing removes impurities from natural gas and separates valuable hydrocarbons like methane, ethane, and propane.",
            tags=["gas processing", "natural gas", "methane"],
            weight=1.0
        ),
        SearchDocument(
            id="17",
            title="Petroleum Chemistry: Lubricants",
            content="Lubricants are produced from base oils and additives. Their properties depend on viscosity, oxidation stability, and pour point.",
            tags=["lubricants", "base oils", "additives"],
            weight=1.0
        ),
        SearchDocument(
            id="18",
            title="Petroleum Chemistry: Additives",
            content="Additives improve fuel and lubricant performance. Examples include detergents, anti-knock agents, and corrosion inhibitors.",
            tags=["additives", "detergents", "corrosion"],
            weight=1.0
        ),
        SearchDocument(
            id="19",
            title="Petroleum Chemistry: Polymerization",
            content="Polymerization transforms small hydrocarbons into polymers used in plastics, rubber, and synthetic fibers.",
            tags=["polymerization", "plastics", "rubber"],
            weight=1.0
        ),
        SearchDocument(
            id="20",
            title="Petroleum Chemistry: Alkylation",
            content="Alkylation combines isobutane and olefins to produce high-octane gasoline components using acid catalysts.",
            tags=["alkylation", "isobutane", "olefins"],
            weight=1.0
        ),
        SearchDocument(
            id="21",
            title="Petroleum Chemistry: Extraction Processes",
            content="Extraction processes separate valuable components from petroleum using solvents. Examples include solvent dewaxing and aromatics extraction.",
            tags=["extraction", "solvents", "dewaxing"],
            weight=1.0
        ),
        SearchDocument(
            id="22",
            title="Petroleum Chemistry: Gasoline Blending",
            content="Gasoline blending involves mixing refinery streams to meet specifications for volatility, octane, and emissions.",
            tags=["blending", "gasoline", "specifications"],
            weight=1.0
        ),
        SearchDocument(
            id="23",
            title="Petroleum Chemistry: Residue Upgrading",
            content="Residue upgrading converts heavy residues into lighter products using processes like coking, hydrocracking, and visbreaking.",
            tags=["residue", "upgrading", "coking"],
            weight=1.0
        ),
        SearchDocument(
            id="24",
            title="Petroleum Chemistry: Bitumen",
            content="Bitumen is a viscous, black material used in road construction and roofing. It is produced from heavy residues in petroleum refining.",
            tags=["bitumen", "road construction", "residues"],
            weight=1.0
        ),
        SearchDocument(
            id="25",
            title="Petroleum Chemistry: Fuel Quality Standards",
            content="Fuel quality standards regulate properties such as sulfur content, volatility, and octane rating to ensure environmental compliance and engine performance.",
            tags=["fuel quality", "standards", "compliance"],
            weight=1.0
        ),
        SearchDocument(
            id="26",
            title="Petroleum Chemistry: Gas Sweetening",
            content="Gas sweetening removes hydrogen sulfide and carbon dioxide from natural gas using amine solutions, improving safety and reducing corrosion.",
            tags=["gas sweetening", "hydrogen sulfide", "amine"],
            weight=1.0
        ),
        SearchDocument(
            id="27",
            title="Petroleum Chemistry: Oil Sands Processing",
            content="Oil sands processing extracts bitumen from sand using hot water, solvents, and froth flotation, followed by upgrading to synthetic crude.",
            tags=["oil sands", "bitumen", "extraction"],
            weight=1.0
        ),
        SearchDocument(
            id="28",
            title="Petroleum Chemistry: Water Treatment",
            content="Water treatment in refineries removes contaminants from process water using filtration, chemical treatment, and biological methods.",
            tags=["water treatment", "filtration", "refineries"],
            weight=1.0
        ),
        SearchDocument(
            id="29",
            title="Petroleum Chemistry: Corrosion Control",
            content="Corrosion control in petroleum facilities uses inhibitors, coatings, and cathodic protection to prevent equipment degradation.",
            tags=["corrosion", "inhibitors", "protection"],
            weight=1.0
        ),
        SearchDocument(
            id="30",
            title="Petroleum Chemistry: Gas Flaring",
            content="Gas flaring disposes of excess hydrocarbons in refineries and oil fields. Technologies aim to reduce emissions and recover valuable gases.",
            tags=["gas flaring", "emissions", "recovery"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)