import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

class SearchDocument:
    def __init__(self, id: int, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = id
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
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + ' ' + doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
            self.documents[doc.id] = doc
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * freq * (self.k1 + 1) / denom
        return score * self.documents[doc_id].weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            tf_norm = tf[term] / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        bm25_scores = {}
        tfidf_scores = {}
        for doc_id in self.documents:
            bm25 = self._score_bm25(query_terms, doc_id)
            tfidf = self._score_tfidf(query_terms, doc_id)
            # Combine BM25 and TF-IDF (weighted sum)
            score = 0.7 * bm25 + 0.3 * tfidf
            if score > 0:
                bm25_scores[doc_id] = score
                tfidf_scores[doc_id] = tfidf
        ranked = sorted(bm25_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], maxlen: int = 180) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:maxlen]
            return snippet + ('...' if len(content) > maxlen else '')
        start = max(positions[0] - 8, 0)
        end = min(start + 32, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        if len(snippet) > maxlen:
            snippet = snippet[:maxlen]
        return snippet + '...'

    def get_stats(self) -> Dict[str, float]:
        return {
            'num_documents': self.N,
            'avg_doc_length': self.avg_doc_length,
            'num_terms': len(self.doc_freqs)
        }

# Singleton factory for SearchIndex
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
            id=1,
            title="Stribeck Curve: Lubrication Regime Identification",
            content="The Stribeck curve illustrates the relationship between friction coefficient and the Hersey number, enabling identification of boundary, mixed, and hydrodynamic lubrication regimes.",
            tags=["stribeck", "lubrication", "regime", "friction"],
            weight=1.0
        ),
        SearchDocument(
            id=2,
            title="Archard Wear Equation: Predicting Adhesive Wear",
            content="The Archard equation predicts wear volume based on applied load, sliding distance, and material hardness. It is crucial for estimating adhesive wear in tribological contacts.",
            tags=["archard", "wear", "adhesive", "prediction"],
            weight=1.0
        ),
        SearchDocument(
            id=3,
            title="Reynolds Equation: Film Pressure in Hydrodynamic Bearings",
            content="The Reynolds equation models pressure distribution in thin lubricant films, essential for hydrodynamic bearing design and performance analysis.",
            tags=["reynolds", "hydrodynamic", "bearing", "pressure"],
            weight=1.0
        ),
        SearchDocument(
            id=4,
            title="Elastohydrodynamic Lubrication (EHL): Rolling Contact Film Thickness",
            content="EHL theory accounts for elastic deformation and lubricant viscosity increase under pressure, predicting minimum film thickness in rolling contacts.",
            tags=["ehl", "elastohydrodynamic", "film", "thickness"],
            weight=1.0
        ),
        SearchDocument(
            id=5,
            title="Oil Analysis: Wear Metals and Contamination Limits",
            content="Oil analysis detects wear metals like Fe, Cu, and contaminants such as Si, setting limits for effective machinery condition monitoring.",
            tags=["oil analysis", "wear metals", "contamination", "limits"],
            weight=1.0
        ),
        SearchDocument(
            id=6,
            title="Lubricant Base Oil Groups (API): Performance Characteristics",
            content="API classifies base oils into Groups I-V based on refining method, sulfur content, and viscosity index, affecting lubricant performance.",
            tags=["base oil", "api", "lubricant", "groups"],
            weight=1.0
        ),
        SearchDocument(
            id=7,
            title="EP and AW Additives: Extreme Pressure and Anti-Wear Mechanisms",
            content="EP additives react under high loads to form protective films, while AW additives reduce wear under moderate conditions.",
            tags=["ep additives", "aw additives", "extreme pressure", "anti-wear"],
            weight=1.0
        ),
        SearchDocument(
            id=8,
            title="Grease Selection: NLGI Grade, Thickener Type, and Dropping Point",
            content="Grease selection involves NLGI grade for consistency, thickener type for compatibility, and dropping point for temperature resistance.",
            tags=["grease", "nlgi", "thickener", "dropping point"],
            weight=1.0
        ),
        SearchDocument(
            id=9,
            title="Surface Engineering: Nitriding, PVD, and DLC Coatings",
            content="Surface treatments like nitriding, physical vapor deposition (PVD), and diamond-like carbon (DLC) coatings enhance wear resistance.",
            tags=["surface engineering", "nitriding", "pvd", "dlc"],
            weight=1.0
        ),
        SearchDocument(
            id=10,
            title="Bearing Lubrication: Minimum Film Thickness Calculation",
            content="Calculating minimum film thickness ensures separation of surfaces in bearings, preventing wear and failure.",
            tags=["bearing", "lubrication", "film thickness"],
            weight=1.0
        ),
        SearchDocument(
            id=11,
            title="Viscosity Index Improvers: Shear Stability",
            content="Viscosity index improvers enhance lubricant viscosity-temperature behavior. Shear stability distinguishes temporary from permanent viscosity loss.",
            tags=["viscosity index", "improvers", "shear stability"],
            weight=1.0
        ),
        SearchDocument(
            id=12,
            title="Boundary Lubrication: Additive Chemistry",
            content="Boundary lubrication relies on chemical additives such as ZDDP to form protective films where full fluid separation is not possible.",
            tags=["boundary lubrication", "additives", "zddp"],
            weight=1.0
        ),
        SearchDocument(
            id=13,
            title="Mixed Lubrication: Transition Regime",
            content="Mixed lubrication occurs when both asperity contact and fluid film support the load, typically in the Stribeck curve's transition region.",
            tags=["mixed lubrication", "transition", "stribeck"],
            weight=1.0
        ),
        SearchDocument(
            id=14,
            title="Hydrodynamic Lubrication: Full Film Separation",
            content="Hydrodynamic lubrication provides full separation of surfaces by a continuous fluid film, minimizing wear and friction.",
            tags=["hydrodynamic", "lubrication", "film"],
            weight=1.0
        ),
        SearchDocument(
            id=15,
            title="Wear Particle Analysis: Ferrography",
            content="Ferrography separates and analyzes wear particles in lubricants, offering insights into wear mechanisms and severity.",
            tags=["wear particle", "ferrography", "analysis"],
            weight=1.0
        ),
        SearchDocument(
            id=16,
            title="Adhesive vs. Abrasive Wear: Mechanisms",
            content="Adhesive wear results from material transfer between surfaces, while abrasive wear involves hard particles or asperities cutting softer material.",
            tags=["adhesive wear", "abrasive wear", "mechanisms"],
            weight=1.0
        ),
        SearchDocument(
            id=17,
            title="Elastomer Compatibility: Lubricant Selection",
            content="Selecting lubricants compatible with elastomers prevents seal degradation and leakage in tribological systems.",
            tags=["elastomer", "lubricant", "compatibility"],
            weight=1.0
        ),
        SearchDocument(
            id=18,
            title="Synthetic Lubricants: Polyalphaolefin (PAO) and Esters",
            content="Synthetic lubricants like PAO and esters offer superior thermal stability, oxidation resistance, and low-temperature performance.",
            tags=["synthetic", "lubricants", "pao", "esters"],
            weight=1.0
        ),
        SearchDocument(
            id=19,
            title="Grease Thickener Types: Lithium, Calcium, Polyurea",
            content="Lithium, calcium, and polyurea are common grease thickeners, each with unique water resistance and temperature properties.",
            tags=["grease", "thickener", "lithium", "calcium", "polyurea"],
            weight=1.0
        ),
        SearchDocument(
            id=20,
            title="Dropping Point: Grease High-Temperature Limit",
            content="The dropping point indicates the maximum temperature at which grease retains its structure before liquefying.",
            tags=["dropping point", "grease", "temperature"],
            weight=1.0
        ),
        SearchDocument(
            id=21,
            title="NLGI Grades: Grease Consistency",
            content="NLGI grades classify grease consistency from 000 (fluid) to 6 (block), guiding selection for specific applications.",
            tags=["nlgi", "grease", "consistency"],
            weight=1.0
        ),
        SearchDocument(
            id=22,
            title="API Group IV and V: Synthetic Base Oils",
            content="API Groups IV (PAO) and V (esters, PAGs) define synthetic base oils with high performance for demanding applications.",
            tags=["api", "group iv", "group v", "synthetic", "base oil"],
            weight=1.0
        ),
        SearchDocument(
            id=23,
            title="ZDDP: Anti-Wear Additive Chemistry",
            content="Zinc dialkyldithiophosphate (ZDDP) is a widely used anti-wear additive, forming protective phosphate films on metal surfaces.",
            tags=["zddp", "anti-wear", "additive"],
            weight=1.0
        ),
        SearchDocument(
            id=24,
            title="DLC Coatings: Ultra-Low Friction and Wear",
            content="Diamond-like carbon (DLC) coatings provide ultra-low friction and high wear resistance for tribological components.",
            tags=["dlc", "coating", "friction", "wear"],
            weight=1.0
        ),
        SearchDocument(
            id=25,
            title="Reynolds Equation: Assumptions and Limitations",
            content="The Reynolds equation assumes isoviscous, incompressible flow and neglects inertia, limiting its application to thin films.",
            tags=["reynolds", "assumptions", "limitations"],
            weight=1.0
        ),
        SearchDocument(
            id=26,
            title="Film Thickness Ratio: Lambda (λ) Parameter",
            content="The lambda ratio (λ) compares lubricant film thickness to composite surface roughness, indicating lubrication regime.",
            tags=["film thickness", "lambda", "lubrication regime"],
            weight=1.0
        ),
        SearchDocument(
            id=27,
            title="Viscosity Index: Lubricant Temperature Sensitivity",
            content="A high viscosity index indicates less viscosity change with temperature, desirable for stable lubrication.",
            tags=["viscosity index", "temperature", "lubricant"],
            weight=1.0
        ),
        SearchDocument(
            id=28,
            title="Contaminant Limits: ISO 4406 Cleanliness Codes",
            content="ISO 4406 codes set limits for particle contamination in lubricants, critical for hydraulic and precision systems.",
            tags=["contaminant", "iso 4406", "cleanliness"],
            weight=1.0
        ),
        SearchDocument(
            id=29,
            title="PVD Coatings: Physical Vapor Deposition for Wear Resistance",
            content="PVD coatings deposit hard, wear-resistant films such as TiN and CrN, enhancing component life in tribological applications.",
            tags=["pvd", "coating", "wear resistance"],
            weight=1.0
        ),
        SearchDocument(
            id=30,
            title="Elastohydrodynamic Film Thickness: Hamrock-Dowson Equation",
            content="The Hamrock-Dowson equation estimates minimum film thickness in EHL contacts, considering speed, load, viscosity, and material properties.",
            tags=["ehl", "hamrock-dowson", "film thickness"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)