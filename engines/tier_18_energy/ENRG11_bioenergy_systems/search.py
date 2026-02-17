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
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[Tuple[int, str], float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.term_freqs[doc.id] = Counter(tokens)
            for token in set(tokens):
                self.term_doc_freq[token] += 1
            self.total_docs += 1
            self.avg_doc_length = (
                sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            )
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            tf = self.term_freqs[doc_id][term]
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            numerator = tf * (self._bm25_k1 + 1)
            denominator = tf + self._bm25_k1 * (
                1 - self._bm25_b + self._bm25_b * doc_len / self.avg_doc_length
            )
            score += idf * (numerator / denominator)
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            tf = self.term_freqs[doc_id][term]
            if tf == 0:
                continue
            norm_tf = tf / doc_len
            idf = self._compute_idf(term)
            score += norm_tf * idf
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scored_docs = []
        for doc_id in self.documents:
            if use_tfidf:
                score = self._score_tfidf(doc_id, query_terms)
            else:
                score = self._score_bm25(doc_id, query_terms)
            if score > 0:
                snippet = self._make_snippet(doc_id, query_terms)
                scored_docs.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scored_docs.sort(key=lambda x: x.score, reverse=True)
        return scored_docs[:limit]

    def _make_snippet(self, doc_id: int, query_terms: List[str]) -> str:
        doc = self.documents[doc_id]
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:160] + ('...' if len(content) > 160 else '')
        start = max(positions[0] - 10, 0)
        end = min(positions[0] + 30, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in query_terms:
            snippet = re.sub(r'\b(%s)\b' % re.escape(term), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet[:160] + ('...' if len(snippet) > 160 else '')

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
        }

# Singleton factory for search index
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Biomass Feedstock Energy Density Analysis",
            "Energy density of biomass feedstocks determines their suitability for conversion processes. Wood pellets, agricultural residues, and energy crops are compared for calorific value, moisture content, and ash yield. Higher energy density improves logistics and conversion efficiency.",
            ["biomass", "energy density", "feedstock", "calorific value"],
            1.0
        ),
        SearchDocument(
            2,
            "Anaerobic Digestion Kinetics and Reactor Design",
            "Anaerobic digestion involves microbial breakdown of organic matter in absence of oxygen. Kinetic models such as first-order, Monod, and ADM1 are used to predict biogas yield. Reactor types include CSTR, UASB, and plug-flow, each with unique hydraulic and mixing characteristics.",
            ["anaerobic digestion", "kinetics", "reactor design", "biogas"],
            1.0
        ),
        SearchDocument(
            3,
            "Biogas Upgrading and Purification Technologies",
            "Biogas contains methane, CO2, H2S, and trace contaminants. Upgrading technologies include water scrubbing, PSA, membrane separation, and chemical absorption. Purified biomethane can be injected into the gas grid or used as vehicle fuel.",
            ["biogas", "upgrading", "purification", "methane", "PSA"],
            1.0
        ),
        SearchDocument(
            4,
            "Biodiesel Transesterification Chemistry and Process Control",
            "Transesterification converts triglycerides in vegetable oils or animal fats to biodiesel and glycerol using methanol and a catalyst. Process control involves temperature, molar ratio, and catalyst concentration. Alkali, acid, and enzymatic catalysts are compared.",
            ["biodiesel", "transesterification", "chemistry", "process control"],
            1.0
        ),
        SearchDocument(
            5,
            "Cellulosic Ethanol Production via Enzymatic Hydrolysis",
            "Cellulosic biomass is hydrolyzed by cellulase enzymes to release fermentable sugars. Pretreatment methods (steam explosion, acid, alkaline) enhance enzyme accessibility. Fermentation converts sugars to ethanol. Process integration improves yield and economics.",
            ["cellulosic ethanol", "enzymatic hydrolysis", "pretreatment", "fermentation"],
            1.0
        ),
        SearchDocument(
            6,
            "Feedstock Logistics and Supply Chain Optimization",
            "Efficient logistics for biomass feedstocks involve harvesting, storage, transport, and preprocessing. Optimization models minimize costs and emissions. GIS and simulation tools help design supply chains for bioenergy plants.",
            ["feedstock logistics", "supply chain", "optimization", "GIS"],
            1.0
        ),
        SearchDocument(
            7,
            "Thermochemical Biomass Conversion: Gasification vs Pyrolysis",
            "Gasification produces syngas by partial oxidation at high temperatures, while pyrolysis yields bio-oil, char, and gases under limited oxygen. Reactor design, temperature, and feedstock properties affect product distribution and quality.",
            ["thermochemical", "gasification", "pyrolysis", "syngas", "bio-oil"],
            1.0
        ),
        SearchDocument(
            8,
            "Bioenergy Environmental Life Cycle and Carbon Accounting",
            "Life cycle assessment (LCA) quantifies environmental impacts of bioenergy systems. Carbon accounting tracks GHG emissions from feedstock production, conversion, and use. Sustainable bioenergy reduces net carbon emissions compared to fossil fuels.",
            ["life cycle", "carbon accounting", "LCA", "GHG", "sustainability"],
            1.0
        ),
        SearchDocument(
            9,
            "Algae Cultivation for Biofuel Production",
            "Microalgae are cultivated in open ponds or photobioreactors for biofuel. Nutrient supply, light, CO2, and temperature affect growth. Harvesting and lipid extraction methods determine biofuel yield and quality.",
            ["algae", "cultivation", "biofuel", "photobioreactor", "lipid extraction"],
            1.0
        ),
        SearchDocument(
            10,
            "Biomass Co-firing in Coal Power Plants",
            "Co-firing biomass with coal reduces carbon emissions and utilizes renewable feedstocks. Boiler modifications, fuel blending, and ash management are required. Energy output and emission profiles depend on feedstock and co-firing ratio.",
            ["biomass", "co-firing", "coal", "power plant", "emissions"],
            1.0
        ),
        SearchDocument(
            11,
            "Renewable Diesel via Hydrotreating (HVO/HEFA)",
            "Hydrotreating converts fats and oils to renewable diesel using hydrogen and catalysts. HVO and HEFA processes remove oxygen and saturate hydrocarbons. Product properties match conventional diesel and can be blended or used directly.",
            ["renewable diesel", "hydrotreating", "HVO", "HEFA", "catalyst"],
            1.0
        ),
        SearchDocument(
            12,
            "Biogas CHP Sizing and Economics",
            "Combined heat and power (CHP) systems utilize biogas for electricity and heat generation. Sizing involves matching biogas production to energy demand. Economic analysis considers capital, O&M, and incentives for optimal system design.",
            ["biogas", "CHP", "sizing", "economics", "energy demand"],
            1.0
        ),
        SearchDocument(
            13,
            "Enzyme Production for Cellulosic Hydrolysis",
            "Enzyme production uses genetically engineered microbes or fungi to produce cellulases. Fermentation conditions, substrate, and purification affect enzyme yield and activity. Cost-effective enzyme supply is critical for cellulosic ethanol.",
            ["enzyme production", "cellulosic hydrolysis", "cellulase", "fermentation"],
            1.0
        ),
        SearchDocument(
            14,
            "Pretreatment Technologies for Lignocellulosic Biomass",
            "Pretreatment disrupts lignin and hemicellulose to improve enzyme access. Methods include steam explosion, dilute acid, ammonia fiber expansion, and ionic liquids. Selection depends on feedstock and downstream process requirements.",
            ["pretreatment", "lignocellulosic", "steam explosion", "acid", "ionic liquids"],
            1.0
        ),
        SearchDocument(
            15,
            "Microbial Consortia in Anaerobic Digestion",
            "Anaerobic digestion relies on synergistic microbial communities. Hydrolytic, acidogenic, acetogenic, and methanogenic microbes convert complex organics to biogas. Community structure affects stability and yield.",
            ["microbial consortia", "anaerobic digestion", "methanogenesis", "biogas"],
            1.0
        ),
        SearchDocument(
            16,
            "Membrane Separation for Biogas Upgrading",
            "Membrane technologies selectively separate CO2 and H2S from methane in biogas. Polymer and inorganic membranes offer high selectivity and scalability. Integration with other upgrading methods enhances biomethane purity.",
            ["membrane separation", "biogas", "upgrading", "CO2", "methane"],
            1.0
        ),
        SearchDocument(
            17,
            "Feedstock Quality and Contaminant Management",
            "Feedstock quality affects conversion efficiency and product quality. Contaminants such as heavy metals, plastics, and stones must be removed. Quality control protocols ensure consistent feedstock for bioenergy processes.",
            ["feedstock quality", "contaminants", "conversion", "quality control"],
            1.0
        ),
        SearchDocument(
            18,
            "Process Simulation in Bioenergy Systems",
            "Simulation tools model bioenergy processes for optimization and design. Aspen Plus, SuperPro Designer, and custom models evaluate mass and energy balances, economics, and environmental impacts.",
            ["process simulation", "bioenergy", "optimization", "Aspen Plus"],
            1.0
        ),
        SearchDocument(
            19,
            "Biogas Desulfurization Techniques",
            "Desulfurization removes H2S from biogas to protect equipment and improve biomethane quality. Techniques include iron sponge, activated carbon, biological scrubbers, and chemical absorption.",
            ["biogas", "desulfurization", "H2S", "iron sponge", "activated carbon"],
            1.0
        ),
        SearchDocument(
            20,
            "Advanced Catalysts for Biodiesel Production",
            "Catalyst development improves transesterification efficiency and product purity. Heterogeneous, enzymatic, and nano-catalysts are explored for higher activity and easier separation.",
            ["catalysts", "biodiesel", "transesterification", "nano-catalyst"],
            1.0
        ),
        SearchDocument(
            21,
            "Supply Chain Risk Management in Biomass Logistics",
            "Risk management addresses supply variability, weather impacts, and market fluctuations. Strategies include diversification, inventory buffers, and contract structures to ensure reliable feedstock supply.",
            ["supply chain", "risk management", "biomass logistics", "inventory"],
            1.0
        ),
        SearchDocument(
            22,
            "Gasification Reactor Types and Performance",
            "Gasification reactors include fixed bed, fluidized bed, and entrained flow designs. Performance depends on temperature, pressure, feedstock, and gasifying agent. Syngas composition and tar formation are key metrics.",
            ["gasification", "reactor", "syngas", "tar", "fluidized bed"],
            1.0
        ),
        SearchDocument(
            23,
            "Bioenergy Policy and Incentives",
            "Government policies and incentives drive bioenergy adoption. Feed-in tariffs, tax credits, and renewable portfolio standards support project development and commercialization.",
            ["policy", "incentives", "bioenergy", "feed-in tariff"],
            1.0
        ),
        SearchDocument(
            24,
            "Algae Harvesting and Dewatering Methods",
            "Efficient harvesting and dewatering are critical for algae biofuel production. Methods include centrifugation, filtration, flocculation, and membrane separation. Process selection affects energy use and yield.",
            ["algae", "harvesting", "dewatering", "biofuel", "centrifugation"],
            1.0
        ),
        SearchDocument(
            25,
            "Carbon Capture Integration in Biomass Power",
            "Integrating carbon capture with biomass power plants enables negative emissions. Technologies include amine scrubbing, oxyfuel combustion, and bioenergy with carbon capture and storage (BECCS).",
            ["carbon capture", "biomass power", "BECCS", "negative emissions"],
            1.0
        ),
        SearchDocument(
            26,
            "Enzymatic Pretreatment for Enhanced Hydrolysis",
            "Enzymatic pretreatment uses lignin-degrading enzymes to improve cellulose accessibility. Combined with mechanical or chemical methods, it increases hydrolysis rates and yields.",
            ["enzymatic pretreatment", "hydrolysis", "lignin", "cellulose"],
            1.0
        ),
        SearchDocument(
            27,
            "Thermochemical Pathways for Renewable Fuels",
            "Thermochemical conversion includes gasification, pyrolysis, and hydrothermal liquefaction. Pathways produce syngas, bio-oil, and renewable fuels from diverse biomass feedstocks.",
            ["thermochemical", "renewable fuels", "gasification", "pyrolysis"],
            1.0
        ),
        SearchDocument(
            28,
            "Life Cycle GHG Emissions of Bioenergy Systems",
            "Life cycle greenhouse gas (GHG) emissions assessment compares bioenergy systems to fossil fuels. Factors include feedstock production, conversion, transport, and end-use.",
            ["life cycle", "GHG", "bioenergy", "emissions"],
            1.0
        ),
        SearchDocument(
            29,
            "Algae Strain Selection for Biofuel Yield",
            "Strain selection impacts algae growth rate, lipid content, and biofuel yield. Screening and genetic engineering optimize strains for commercial production.",
            ["algae", "strain selection", "biofuel", "lipid"],
            1.0
        ),
        SearchDocument(
            30,
            "Biomass Ash Management in Co-firing",
            "Ash from biomass co-firing affects boiler performance and emissions. Management strategies include ash blending, disposal, and recycling for construction materials.",
            ["biomass", "ash management", "co-firing", "boiler", "emissions"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)