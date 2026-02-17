import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Any

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
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self._re_tokenize = re.compile(r'\b\w+\b', re.UNICODE)

    def _tokenize(self, text: str) -> List[str]:
        tokens = self._re_tokenize.findall(text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            tf_counter = Counter(tokens)
            for term, freq in tf_counter.items():
                self.term_freqs[term][doc.id] = freq
                self.term_doc_freq[term] += 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self.idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: str, k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            tf = self.term_freqs.get(term, {}).get(doc_id, 0)
            idf = self._compute_idf(term)
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * doc_len / self.avg_doc_length) if self.avg_doc_length > 0 else 1
            score += idf * (numerator / denominator)
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tf_counter = self.term_freqs
        for term in query_terms:
            tf = tf_counter.get(term, {}).get(doc_id, 0)
            if doc_len > 0:
                tf_norm = tf / doc_len
            else:
                tf_norm = 0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            docs_with_term = self.term_freqs.get(term, {})
            candidate_docs.update(docs_with_term.keys())
        scored_results = []
        for doc_id in candidate_docs:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                snippet = self._generate_snippet(doc_id, query_terms)
                scored_results.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:limit]

    def _generate_snippet(self, doc_id: str, query_terms: List[str], snippet_length: int = 160) -> str:
        doc = self.documents[doc_id]
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, token in enumerate(tokens) if token in query_terms]
        if positions:
            start = max(positions[0] - 10, 0)
            end = min(start + 30, len(tokens))
            snippet_tokens = tokens[start:end]
            snippet = ' '.join(snippet_tokens)
            for term in query_terms:
                snippet = re.sub(r'\b(' + re.escape(term) + r')\b', r'**\1**', snippet, flags=re.IGNORECASE)
            return snippet[:snippet_length] + ('...' if len(snippet) > snippet_length else '')
        else:
            return content[:snippet_length] + ('...' if len(content) > snippet_length else '')

    def get_stats(self) -> Dict[str, Any]:
        return {
            'total_documents': self.total_docs,
            'average_document_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
            'documents': list(self.documents.keys()),
        }

_search_index_instance = None
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
            title="Acid Rain Formation and Effects",
            content="Acid rain forms when sulfur dioxide and nitrogen oxides react with water vapor in the atmosphere. This leads to the production of sulfuric and nitric acids, which fall as precipitation. Acid rain causes soil acidification, damages aquatic ecosystems, and erodes buildings.",
            tags=["acid rain", "sulfur dioxide", "nitrogen oxides", "environmental impact"],
            weight=1.0
        ),
        SearchDocument(
            id="2",
            title="Greenhouse Gases and Climate Change",
            content="Greenhouse gases such as carbon dioxide, methane, and nitrous oxide trap heat in the Earth's atmosphere, leading to global warming. Human activities like fossil fuel combustion and agriculture increase greenhouse gas concentrations, contributing to climate change.",
            tags=["greenhouse gases", "climate change", "carbon dioxide", "methane"],
            weight=1.0
        ),
        SearchDocument(
            id="3",
            title="Ozone Layer Depletion",
            content="The ozone layer protects life on Earth from harmful ultraviolet radiation. Chlorofluorocarbons (CFCs) and other ozone-depleting substances break down ozone molecules, resulting in increased UV exposure and health risks such as skin cancer.",
            tags=["ozone layer", "CFCs", "UV radiation", "depletion"],
            weight=1.0
        ),
        SearchDocument(
            id="4",
            title="Water Pollution and Treatment",
            content="Water pollution arises from contaminants like heavy metals, pesticides, and pathogens entering water bodies. Treatment methods include filtration, sedimentation, and chemical disinfection to ensure safe drinking water.",
            tags=["water pollution", "treatment", "heavy metals", "pesticides"],
            weight=1.0
        ),
        SearchDocument(
            id="5",
            title="Air Quality Monitoring Techniques",
            content="Air quality is monitored using sensors that detect pollutants such as particulate matter, sulfur dioxide, and ozone. Techniques include spectrophotometry, gas chromatography, and gravimetric analysis.",
            tags=["air quality", "monitoring", "particulate matter", "sensors"],
            weight=1.0
        ),
        SearchDocument(
            id="6",
            title="Solid Waste Management Strategies",
            content="Solid waste management involves collection, transportation, recycling, and disposal of waste materials. Strategies include composting, incineration, and landfill management to minimize environmental impact.",
            tags=["solid waste", "management", "recycling", "composting"],
            weight=1.0
        ),
        SearchDocument(
            id="7",
            title="Heavy Metal Contamination in Soil",
            content="Heavy metals like lead, mercury, and cadmium contaminate soil through industrial activities and improper waste disposal. These metals pose risks to plant growth and human health.",
            tags=["heavy metals", "soil contamination", "lead", "mercury"],
            weight=1.0
        ),
        SearchDocument(
            id="8",
            title="Bioremediation of Polluted Sites",
            content="Bioremediation uses microorganisms to degrade environmental pollutants such as hydrocarbons and pesticides. This process is effective for cleaning contaminated soil and water.",
            tags=["bioremediation", "microorganisms", "pollutants", "hydrocarbons"],
            weight=1.0
        ),
        SearchDocument(
            id="9",
            title="Environmental Impact of Mining",
            content="Mining activities release pollutants including heavy metals and acid mine drainage. Environmental impacts include habitat destruction, water contamination, and air pollution.",
            tags=["mining", "environmental impact", "acid mine drainage", "pollution"],
            weight=1.0
        ),
        SearchDocument(
            id="10",
            title="Photochemical Smog Formation",
            content="Photochemical smog forms when sunlight reacts with nitrogen oxides and volatile organic compounds in the atmosphere. This produces ozone and other irritants, affecting respiratory health.",
            tags=["photochemical smog", "ozone", "nitrogen oxides", "VOC"],
            weight=1.0
        ),
        SearchDocument(
            id="11",
            title="Eutrophication in Aquatic Ecosystems",
            content="Eutrophication occurs when excess nutrients, mainly nitrogen and phosphorus, enter water bodies. This leads to algal blooms, oxygen depletion, and loss of aquatic life.",
            tags=["eutrophication", "nutrients", "algal blooms", "phosphorus"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="Persistent Organic Pollutants (POPs)",
            content="Persistent organic pollutants are toxic chemicals such as DDT and PCBs that resist degradation. POPs accumulate in the environment and pose risks to human and animal health.",
            tags=["POPs", "persistent organic pollutants", "DDT", "PCBs"],
            weight=1.0
        ),
        SearchDocument(
            id="13",
            title="Carbon Footprint Reduction Methods",
            content="Reducing carbon footprint involves energy conservation, renewable energy adoption, and efficient transportation. These methods help mitigate climate change by lowering greenhouse gas emissions.",
            tags=["carbon footprint", "energy conservation", "renewable energy", "emissions"],
            weight=1.0
        ),
        SearchDocument(
            id="14",
            title="Environmental Chemistry of Pesticides",
            content="Pesticides impact environmental chemistry through persistence, bioaccumulation, and toxicity. Their degradation products can contaminate soil and water, affecting ecosystems.",
            tags=["pesticides", "environmental chemistry", "bioaccumulation", "toxicity"],
            weight=1.0
        ),
        SearchDocument(
            id="15",
            title="Microplastics in the Environment",
            content="Microplastics are small plastic particles resulting from the breakdown of larger plastics. They are found in oceans, rivers, and soil, posing risks to wildlife and human health.",
            tags=["microplastics", "plastic pollution", "environment", "wildlife"],
            weight=1.0
        ),
        SearchDocument(
            id="16",
            title="Atmospheric Chemistry of Sulfur Compounds",
            content="Sulfur compounds such as sulfur dioxide and hydrogen sulfide undergo atmospheric reactions, contributing to acid rain and particulate formation.",
            tags=["sulfur compounds", "atmospheric chemistry", "acid rain", "particulates"],
            weight=1.0
        ),
        SearchDocument(
            id="17",
            title="Environmental Toxicology of Mercury",
            content="Mercury is a toxic heavy metal released from coal combustion and mining. It bioaccumulates in fish and can cause neurological disorders in humans.",
            tags=["mercury", "toxicology", "bioaccumulation", "coal combustion"],
            weight=1.0
        ),
        SearchDocument(
            id="18",
            title="Wastewater Treatment Processes",
            content="Wastewater treatment involves primary, secondary, and tertiary processes to remove contaminants. Methods include biological treatment, filtration, and chemical precipitation.",
            tags=["wastewater", "treatment", "biological", "filtration"],
            weight=1.0
        ),
        SearchDocument(
            id="19",
            title="Environmental Chemistry of Nitrogen Cycle",
            content="The nitrogen cycle involves processes such as nitrogen fixation, nitrification, and denitrification. Human activities disrupt the cycle, leading to pollution and eutrophication.",
            tags=["nitrogen cycle", "fixation", "nitrification", "denitrification"],
            weight=1.0
        ),
        SearchDocument(
            id="20",
            title="Hazardous Waste Disposal Methods",
            content="Hazardous waste is disposed of using methods like incineration, landfilling, and chemical stabilization. Proper disposal prevents environmental contamination and health risks.",
            tags=["hazardous waste", "disposal", "incineration", "stabilization"],
            weight=1.0
        ),
        SearchDocument(
            id="21",
            title="Role of Catalysts in Pollution Control",
            content="Catalysts are used in pollution control devices such as catalytic converters to reduce emissions of nitrogen oxides and carbon monoxide from vehicles.",
            tags=["catalysts", "pollution control", "emissions", "converters"],
            weight=1.0
        ),
        SearchDocument(
            id="22",
            title="Environmental Chemistry of Fertilizers",
            content="Fertilizers supply essential nutrients to plants but can cause environmental issues like runoff and eutrophication. Proper management reduces negative impacts.",
            tags=["fertilizers", "nutrients", "runoff", "eutrophication"],
            weight=1.0
        ),
        SearchDocument(
            id="23",
            title="Radioactive Pollution and Its Effects",
            content="Radioactive pollution results from nuclear accidents and improper disposal of radioactive materials. It poses risks such as cancer and genetic mutations.",
            tags=["radioactive pollution", "nuclear", "disposal", "health risks"],
            weight=1.0
        ),
        SearchDocument(
            id="24",
            title="Environmental Chemistry of Organic Solvents",
            content="Organic solvents are used in industry and laboratories. Improper disposal leads to soil and water contamination, affecting environmental and human health.",
            tags=["organic solvents", "contamination", "industry", "health"],
            weight=1.0
        ),
        SearchDocument(
            id="25",
            title="Global Environmental Policies",
            content="Global environmental policies such as the Kyoto Protocol and Paris Agreement aim to reduce greenhouse gas emissions and protect ecosystems worldwide.",
            tags=["environmental policies", "Kyoto Protocol", "Paris Agreement", "emissions"],
            weight=1.0
        ),
        SearchDocument(
            id="26",
            title="Environmental Chemistry of Water Hardness",
            content="Water hardness is caused by dissolved calcium and magnesium ions. Hard water affects industrial processes and household appliances, requiring treatment.",
            tags=["water hardness", "calcium", "magnesium", "treatment"],
            weight=1.0
        ),
        SearchDocument(
            id="27",
            title="Environmental Chemistry of Soil pH",
            content="Soil pH affects nutrient availability and plant growth. Acidic soils may require lime treatment, while alkaline soils can limit micronutrient uptake.",
            tags=["soil pH", "nutrients", "acidic", "alkaline"],
            weight=1.0
        ),
        SearchDocument(
            id="28",
            title="Environmental Chemistry of Detergents",
            content="Detergents contain surfactants that can cause water pollution. Biodegradable detergents reduce environmental impact compared to conventional types.",
            tags=["detergents", "surfactants", "biodegradable", "pollution"],
            weight=1.0
        ),
        SearchDocument(
            id="29",
            title="Environmental Chemistry of Plastics",
            content="Plastics are synthetic polymers that persist in the environment. Their degradation produces microplastics, affecting wildlife and ecosystems.",
            tags=["plastics", "polymers", "microplastics", "degradation"],
            weight=1.0
        ),
        SearchDocument(
            id="30",
            title="Environmental Chemistry of Atmospheric Particulates",
            content="Atmospheric particulates originate from combustion, industrial processes, and natural sources. They impact air quality and human health.",
            tags=["atmospheric particulates", "combustion", "air quality", "health"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)