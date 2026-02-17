import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --- Data Structures ---

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
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_lengths: Dict[int, int] = {}
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
            for token in tokens:
                self.inverted_index[token][doc.id] = self.inverted_index[token].get(doc.id, 0) + 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        candidate_doc_ids = set()
        for token in query_tokens:
            candidate_doc_ids.update(self.inverted_index.get(token, {}).keys())
        scored_results = []
        for doc_id in candidate_doc_ids:
            bm25_score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            combined_score = 0.7 * bm25_score + 0.3 * tfidf_score
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_tokens)
            scored_results.append(SearchResult(doc_id, combined_score, doc.title, snippet))
        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "total_documents": self.total_docs,
                "avg_doc_length": self.avg_doc_length,
                "unique_terms": len(self.inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9\-]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = len(self.inverted_index.get(term, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_tokens: List[str]) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        tokens = self.doc_tokens[doc_id]
        doc_len = self.doc_lengths[doc_id]
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        term_freqs = Counter(tokens)
        for term in query_tokens:
            if term not in term_freqs:
                continue
            tf = term_freqs[term]
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / avg_dl)
            score += idf * (numerator / denominator)
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_tokens: List[str]) -> float:
        score = 0.0
        tokens = self.doc_tokens[doc_id]
        doc_len = self.doc_lengths[doc_id]
        term_freqs = Counter(tokens)
        for term in query_tokens:
            cache_key = (doc_id, term)
            if cache_key in self._tfidf_cache:
                tfidf = self._tfidf_cache[cache_key]
            else:
                tf = term_freqs[term] / doc_len if doc_len > 0 else 0.0
                idf = self._compute_idf(term)
                tfidf = tf * idf
                self._tfidf_cache[cache_key] = tfidf
            score += tfidf
        return score

    def _make_snippet(self, content: str, query_tokens: List[str], max_len: int = 160) -> str:
        content_lower = content.lower()
        for token in query_tokens:
            idx = content_lower.find(token)
            if idx != -1:
                start = max(0, idx - 40)
                end = min(len(content), idx + 80)
                snippet = content[start:end]
                if start > 0:
                    snippet = "..." + snippet
                if end < len(content):
                    snippet = snippet + "..."
                return snippet
        return content[:max_len] + ("..." if len(content) > max_len else "")

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

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1, "Carbohydrates: Structure and Function",
            "Carbohydrates are organic molecules composed of carbon, hydrogen, and oxygen. They serve as energy sources and structural components in food. Monosaccharides, disaccharides, and polysaccharides are key types.",
            ["carbohydrates", "macronutrients", "structure"], 1.0
        ),
        SearchDocument(
            2, "Proteins: Amino Acids and Denaturation",
            "Proteins are polymers of amino acids. Denaturation involves the disruption of secondary, tertiary, or quaternary structures, affecting solubility and functionality in food systems.",
            ["proteins", "denaturation", "macronutrients"], 1.0
        ),
        SearchDocument(
            3, "Lipids: Classification and Rancidity",
            "Lipids include fats, oils, and phospholipids. Rancidity, caused by lipid oxidation or hydrolysis, leads to off-flavors and reduced shelf life. Antioxidants inhibit oxidation.",
            ["lipids", "rancidity", "antioxidants"], 1.0
        ),
        SearchDocument(
            4, "Maillard Reaction and Flavor Development",
            "The Maillard reaction occurs between reducing sugars and amino acids upon heating, forming complex flavors and brown pigments in cooked foods.",
            ["maillard", "flavor", "browning"], 1.0
        ),
        SearchDocument(
            5, "Food Preservation: Pasteurization, Sterilization, UHT",
            "Pasteurization, sterilization, and ultra-high temperature (UHT) processing reduce or eliminate microbial load, extending shelf life while preserving nutritional quality.",
            ["preservation", "pasteurization", "sterilization", "UHT"], 1.0
        ),
        SearchDocument(
            6, "Water Activity (Aw) and Microbial Growth",
            "Water activity (Aw) measures free water in food. Most bacteria require Aw > 0.91; molds can grow at Aw as low as 0.80. Controlling Aw limits microbial spoilage.",
            ["water activity", "microbial growth", "preservation"], 1.0
        ),
        SearchDocument(
            7, "Food Additives: GRAS, E-numbers, FDA Regulation",
            "Food additives are substances added to foods for preservation, flavor, or texture. GRAS status, E-numbers, and FDA regulations govern their safe use.",
            ["additives", "GRAS", "E-numbers", "FDA"], 1.0
        ),
        SearchDocument(
            8, "Emulsification: HLB and Surfactant Stability",
            "Emulsifiers stabilize oil-in-water or water-in-oil systems. The hydrophilic-lipophilic balance (HLB) value predicts emulsifier suitability and stability.",
            ["emulsification", "HLB", "surfactants"], 1.0
        ),
        SearchDocument(
            9, "Starch: Gelatinization, Retrogradation, Modification",
            "Starch gelatinization involves water uptake and granule swelling upon heating. Retrogradation is the re-association of starch chains, affecting texture. Modification improves functionality.",
            ["starch", "gelatinization", "retrogradation", "modification"], 1.0
        ),
        SearchDocument(
            10, "Protein Gelation and Foaming",
            "Proteins can form gels or foams by unfolding and creating networks. Gelation is important in products like tofu; foaming is key in meringues.",
            ["protein", "gelation", "foaming"], 1.0
        ),
        SearchDocument(
            11, "Lipid Oxidation and Antioxidants",
            "Lipid oxidation leads to rancidity and off-flavors. Antioxidants such as tocopherols and BHA/BHT inhibit oxidation and prolong shelf life.",
            ["lipid oxidation", "antioxidants", "rancidity"], 1.0
        ),
        SearchDocument(
            12, "Food Safety: HACCP Critical Control Points",
            "Hazard Analysis and Critical Control Points (HACCP) is a systematic approach to food safety. Identifying and monitoring critical control points prevents hazards.",
            ["HACCP", "food safety", "critical control"], 1.0
        ),
        SearchDocument(
            13, "Microbial Contamination: Salmonella, Listeria, E. coli",
            "Pathogens like Salmonella, Listeria monocytogenes, and E. coli O157:H7 can contaminate food, causing illness. Control involves sanitation and temperature management.",
            ["microbial contamination", "Salmonella", "Listeria", "E. coli"], 1.0
        ),
        SearchDocument(
            14, "Mycotoxin Detection: Aflatoxin, Ochratoxin",
            "Mycotoxins such as aflatoxin and ochratoxin are toxic metabolites from molds. Detection methods include ELISA and chromatography.",
            ["mycotoxins", "aflatoxin", "ochratoxin", "detection"], 1.0
        ),
        SearchDocument(
            15, "Pesticide Residue: MRL Analysis, GC-MS, LC-MS",
            "Maximum Residue Limits (MRLs) define safe pesticide levels in food. Analytical methods like GC-MS and LC-MS are used for detection.",
            ["pesticide residue", "MRL", "GC-MS", "LC-MS"], 1.0
        ),
        SearchDocument(
            16, "Food Allergen Labeling: Big 9, FALCPA",
            "The Big 9 allergens include milk, eggs, fish, shellfish, tree nuts, peanuts, wheat, soy, and sesame. FALCPA mandates clear labeling for consumer safety.",
            ["allergens", "labeling", "FALCPA", "Big 9"], 1.0
        ),
        SearchDocument(
            17, "Fermentation: Lactic, Alcoholic, Acetic",
            "Fermentation processes include lactic acid (yogurt), alcoholic (beer, wine), and acetic acid (vinegar) fermentations, each with unique microbial pathways.",
            ["fermentation", "lactic", "alcoholic", "acetic"], 1.0
        ),
        SearchDocument(
            18, "Enzyme Catalysis: Amylase, Protease, Lipase",
            "Enzymes like amylase, protease, and lipase catalyze biochemical reactions in food processing, such as starch breakdown, protein hydrolysis, and fat modification.",
            ["enzymes", "amylase", "protease", "lipase"], 1.0
        ),
        SearchDocument(
            19, "Food Rheology: Viscosity and Texture Analysis",
            "Food rheology studies flow and deformation. Viscosity measures resistance to flow; texture analysis quantifies properties like firmness and elasticity.",
            ["rheology", "viscosity", "texture"], 1.0
        ),
        SearchDocument(
            20, "Nutritional Analysis: Proximate, Kjeldahl, Soxhlet",
            "Nutritional analysis includes proximate composition (moisture, fat, protein, ash), Kjeldahl method for protein, and Soxhlet extraction for fat content.",
            ["nutritional analysis", "proximate", "Kjeldahl", "Soxhlet"], 1.0
        ),
        SearchDocument(
            21, "Food Packaging: MAP, Barrier Properties, Migration",
            "Modified Atmosphere Packaging (MAP) extends shelf life. Barrier properties prevent gas and moisture transfer; migration refers to movement of substances from packaging to food.",
            ["packaging", "MAP", "barrier", "migration"], 1.0
        ),
        SearchDocument(
            22, "Shelf Life Prediction: Arrhenius, Q10",
            "Shelf life can be predicted using the Arrhenius equation and Q10 temperature coefficient, modeling the rate of quality loss over time.",
            ["shelf life", "Arrhenius", "Q10", "prediction"], 1.0
        ),
        SearchDocument(
            23, "Starch Retrogradation in Bread Staling",
            "Retrogradation of amylopectin in bread leads to staling. Storage conditions affect the rate of retrogradation and bread texture.",
            ["starch", "retrogradation", "bread"], 1.0
        ),
        SearchDocument(
            24, "Protein Functionality in Meat Processing",
            "Proteins influence water holding, emulsification, and gelation in processed meats. Denaturation and cross-linking impact texture and yield.",
            ["protein", "meat", "functionality"], 1.0
        ),
        SearchDocument(
            25, "Lipid Hydrolysis and Free Fatty Acids",
            "Lipid hydrolysis releases free fatty acids, which can cause off-flavors and reduce quality. Lipase enzymes accelerate hydrolysis in dairy and oil products.",
            ["lipid", "hydrolysis", "free fatty acids"], 1.0
        ),
        SearchDocument(
            26, "Food Additive Regulations: International Harmonization",
            "Codex Alimentarius harmonizes international food additive standards, including E-numbers and MRLs, to facilitate global trade and safety.",
            ["additives", "Codex", "E-numbers", "MRL"], 1.0
        ),
        SearchDocument(
            27, "Thermal Processing: D-value and Z-value",
            "D-value is the time to reduce microbial population by 90% at a given temperature. Z-value is the temperature change needed to change the D-value tenfold.",
            ["thermal processing", "D-value", "Z-value"], 1.0
        ),
        SearchDocument(
            28, "Surfactant Stability in Emulsions",
            "Surfactant stability affects emulsion shelf life. Factors include HLB value, concentration, and environmental conditions such as pH and temperature.",
            ["surfactant", "stability", "emulsion"], 1.0
        ),
        SearchDocument(
            29, "Foodborne Pathogen Detection: PCR and Immunoassays",
            "PCR and immunoassays are rapid methods for detecting foodborne pathogens, offering sensitivity and specificity for safety monitoring.",
            ["pathogen", "detection", "PCR", "immunoassay"], 1.0
        ),
        SearchDocument(
            30, "Enzyme Modification of Food Texture",
            "Enzymes modify food texture by hydrolyzing or cross-linking macromolecules. Transglutaminase, for example, improves texture in dairy and meat products.",
            ["enzyme", "modification", "texture"], 1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)