import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

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
        self._documents: Dict[int, SearchDocument] = {}
        self._inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)  # term -> {doc_id: tf}
        self._doc_lengths: Dict[int, int] = {}  # doc_id -> length
        self._avg_doc_length: float = 0.0
        self._total_docs: int = 0
        self._idf_cache: Dict[str, float] = {}
        self._lock = threading.Lock()
        self._doc_titles: Dict[int, str] = {}
        self._doc_contents: Dict[int, str] = {}
        self._doc_tags: Dict[int, Set[str]] = {}

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return  # No duplicate IDs
            self._documents[doc.id] = doc
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            tf = Counter(tokens)
            for term, freq in tf.items():
                self._inverted_index[term][doc.id] = freq
            length = len(tokens)
            self._doc_lengths[doc.id] = length
            self._doc_titles[doc.id] = doc.title
            self._doc_contents[doc.id] = doc.content
            self._doc_tags[doc.id] = set(doc.tags)
            self._total_docs += 1
            self._avg_doc_length = sum(self._doc_lengths.values()) / self._total_docs if self._total_docs > 0 else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        doc_snippets: Dict[int, str] = {}
        doc_matched_terms: Dict[int, Set[str]] = defaultdict(set)
        for term in set(query_terms):
            postings = self._inverted_index.get(term, {})
            idf = self._compute_idf(term)
            for doc_id, tf in postings.items():
                doc = self._documents[doc_id]
                score = self._score_bm25(term, tf, doc_id, idf, doc.weight)
                doc_scores[doc_id] += score
                doc_matched_terms[doc_id].add(term)
        # TF-IDF fallback for non-BM25 terms
        for term in set(query_terms):
            if term not in self._inverted_index:
                continue
            postings = self._inverted_index[term]
            for doc_id, tf in postings.items():
                tfidf = self._score_tfidf(term, tf, doc_id)
                doc_scores[doc_id] += 0.1 * tfidf  # Less weight than BM25

        top_docs = heapq.nlargest(limit, doc_scores.items(), key=lambda x: x[1])
        results = []
        for doc_id, score in top_docs:
            snippet = self._make_snippet(self._doc_contents[doc_id], doc_matched_terms[doc_id])
            results.append(SearchResult(doc_id, score, self._doc_titles[doc_id], snippet))
        return results

    def get_stats(self):
        with self._lock:
            return {
                "documents": self._total_docs,
                "avg_doc_length": self._avg_doc_length,
                "vocabulary_size": len(self._inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        # Lowercase, remove punctuation, split on whitespace
        text = text.lower()
        text = re.sub(r'[^a-z0-9_+\-/]', ' ', text)
        tokens = text.split()
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = self._total_docs
        df = len(self._inverted_index.get(term, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, term: str, tf: int, doc_id: int, idf: float, weight: float) -> float:
        k1 = 1.5
        b = 0.75
        doc_len = self._doc_lengths[doc_id]
        avg_dl = self._avg_doc_length if self._avg_doc_length > 0 else 1
        norm_tf = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len / avg_dl))
        return idf * norm_tf * weight

    def _score_tfidf(self, term: str, tf: int, doc_id: int) -> float:
        # Term frequency normalization (logarithmic)
        tf_norm = 1 + math.log(tf) if tf > 0 else 0
        idf = self._compute_idf(term)
        return tf_norm * idf

    def _make_snippet(self, content: str, terms: Set[str]) -> str:
        # Return a snippet with matched terms highlighted (simple)
        tokens = self._tokenize(content)
        snippet_tokens = []
        for t in tokens:
            if t in terms:
                snippet_tokens.append(f"[{t}]")
            else:
                snippet_tokens.append(t)
            if len(snippet_tokens) >= 35:
                break
        return " ".join(snippet_tokens) + ("..." if len(tokens) > 35 else "")

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

# --- Pre-seed Documents ---

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Cyclic Timetabling in Passenger Railways",
            "Cyclic timetabling ensures that trains run at regular intervals, optimizing passenger convenience and rolling stock utilization. The Periodic Event Scheduling Problem (PESP) model is commonly used for generating robust cyclic timetables.",
            ["cyclic_timetabling", "PESP", "scheduling"],
            1.0
        ),
        SearchDocument(
            2,
            "Rolling Stock Assignment Optimization",
            "Assigning rolling stock efficiently minimizes operational costs and maximizes fleet utilization. Optimization models consider train types, maintenance cycles, and passenger demand to allocate vehicles.",
            ["rolling_stock", "fleet_optimization", "assignment"],
            1.0
        ),
        SearchDocument(
            3,
            "Crew Scheduling and Labor Compliance",
            "Crew scheduling must adhere to labor laws and union agreements. Advanced algorithms optimize crew assignments while ensuring compliance with rest periods and shift length regulations.",
            ["crew_scheduling", "labor_compliance", "operations"],
            1.0
        ),
        SearchDocument(
            4,
            "Station Dwell Time Analysis",
            "Analyzing station dwell times is critical for accurate timetabling and minimizing delays. Factors include passenger boarding/alighting rates, door operations, and platform design.",
            ["dwell_time", "station_analysis", "passenger_flow"],
            1.0
        ),
        SearchDocument(
            5,
            "Fare Structure and Revenue Optimization",
            "Designing fare structures impacts ridership and revenue. Models consider elasticity, ticket types, and peak/off-peak pricing to optimize revenue while maintaining accessibility.",
            ["fare_structure", "revenue_optimization", "pricing"],
            1.0
        ),
        SearchDocument(
            6,
            "On-Time Performance Metrics",
            "On-Time Performance (OTP) is measured by the percentage of trains arriving within a defined threshold. Reliability analysis identifies root causes of delays and informs improvement strategies.",
            ["otp", "reliability", "performance_metrics"],
            1.0
        ),
        SearchDocument(
            7,
            "Platform Screen Doors: Safety and Operations",
            "Platform Screen Doors (PSD) enhance passenger safety and enable automated train operations. Integration with signaling and precise train stopping is essential for effective PSD deployment.",
            ["psd", "safety", "operations"],
            1.0
        ),
        SearchDocument(
            8,
            "ADA Accessibility and Universal Design",
            "ADA compliance ensures stations and vehicles are accessible to all passengers. Universal design principles improve navigation, boarding, and amenities for people with disabilities.",
            ["ada", "accessibility", "universal_design"],
            1.0
        ),
        SearchDocument(
            9,
            "Positive Train Control for Passenger Rail",
            "Positive Train Control (PTC) systems prevent collisions and overspeed derailments. PTC integrates GPS, wireless communications, and onboard computers to enhance safety.",
            ["ptc", "safety", "train_control"],
            1.0
        ),
        SearchDocument(
            10,
            "Passenger Demand Forecasting",
            "Accurate demand forecasting uses historical ridership, demographic trends, and special event data. Models inform service planning and capacity allocation.",
            ["demand_forecasting", "ridership", "modeling"],
            1.0
        ),
        SearchDocument(
            11,
            "Load Factor and Crowding Management",
            "Managing load factors ensures passenger comfort and safety. Real-time monitoring and dynamic train dispatching help mitigate crowding during peak periods.",
            ["load_factor", "crowding", "capacity_management"],
            1.0
        ),
        SearchDocument(
            12,
            "FRA Passenger Equipment Safety Standards",
            "FRA regulations set safety standards for passenger rail equipment, including crashworthiness, fire safety, and emergency egress requirements.",
            ["fra", "safety_standards", "equipment"],
            1.0
        ),
        SearchDocument(
            13,
            "Station Parking and Park-and-Ride Facilities",
            "Park-and-ride facilities extend the catchment area of stations. Effective design considers access, capacity, pricing, and integration with local transit.",
            ["parking", "station_facilities", "park_and_ride"],
            1.0
        ),
        SearchDocument(
            14,
            "Passenger Information Systems (PIS)",
            "Modern PIS provide real-time updates on train arrivals, delays, and platform assignments. Integration with mobile apps enhances the passenger experience.",
            ["pis", "information_systems", "real_time"],
            1.0
        ),
        SearchDocument(
            15,
            "Cross-Border and Inter-City Operations",
            "Cross-border passenger rail requires harmonization of signaling, safety, and customs procedures. Inter-city services balance speed, frequency, and network integration.",
            ["cross_border", "inter_city", "operations"],
            1.0
        ),
        SearchDocument(
            16,
            "Energy Consumption and Regenerative Braking",
            "Energy-efficient operations leverage regenerative braking, eco-driving, and energy management systems. Monitoring consumption supports sustainability goals.",
            ["energy", "regenerative_braking", "sustainability"],
            1.0
        ),
        SearchDocument(
            17,
            "Station Design and Passenger Flow Optimization",
            "Optimized station layouts reduce congestion and improve safety. Simulation tools model passenger movement to inform design decisions.",
            ["station_design", "passenger_flow", "optimization"],
            1.0
        ),
        SearchDocument(
            18,
            "Service Reliability and MDBF",
            "Mean Distance Between Failures (MDBF) is a key reliability metric. Maintenance strategies and asset monitoring improve service continuity.",
            ["reliability", "mdbf", "service"],
            1.0
        ),
        SearchDocument(
            19,
            "Transit-Oriented Development (TOD)",
            "TOD integrates land use and transit planning to encourage sustainable urban growth. High-density, mixed-use development near stations increases ridership.",
            ["tod", "land_use", "development"],
            1.0
        ),
        SearchDocument(
            20,
            "Passenger Flow Simulation Techniques",
            "Simulation of passenger flows supports station design, evacuation planning, and crowd management. Agent-based and cellular automata models are commonly used.",
            ["passenger_flow", "simulation", "station_design"],
            1.0
        ),
        SearchDocument(
            21,
            "Railway Signaling for Passenger Operations",
            "Advanced signaling systems, such as ETCS and CBTC, increase line capacity and safety. Integration with PTC and PSD is crucial for modern networks.",
            ["signaling", "ptc", "psd"],
            1.0
        ),
        SearchDocument(
            22,
            "Fare Capping and Contactless Payments",
            "Fare capping ensures passengers never pay more than a daily or weekly maximum. Contactless payment systems improve convenience and reduce dwell times.",
            ["fare_capping", "contactless", "payments"],
            1.0
        ),
        SearchDocument(
            23,
            "Resilience to Extreme Weather",
            "Railway networks must withstand extreme weather events. Infrastructure hardening and real-time monitoring reduce service disruptions.",
            ["resilience", "weather", "infrastructure"],
            1.0
        ),
        SearchDocument(
            24,
            "Passenger Counting Technologies",
            "Automated passenger counting systems provide accurate load data for planning and real-time crowding management.",
            ["passenger_counting", "technology", "crowding"],
            1.0
        ),
        SearchDocument(
            25,
            "International Rail Standards and Interoperability",
            "Harmonizing technical standards enables cross-border rail services. Interoperability covers signaling, rolling stock, and safety requirements.",
            ["international", "standards", "interoperability"],
            1.0
        ),
        SearchDocument(
            26,
            "Real-Time Data Integration for Operations",
            "Integrating real-time data from trains, stations, and infrastructure enables predictive maintenance and dynamic scheduling.",
            ["real_time", "data_integration", "operations"],
            1.0
        ),
        SearchDocument(
            27,
            "Passenger Rail Security and Emergency Preparedness",
            "Security planning includes surveillance, emergency communications, and staff training to ensure passenger safety.",
            ["security", "emergency", "preparedness"],
            1.0
        ),
        SearchDocument(
            28,
            "Accessibility Innovations in Passenger Rail",
            "Innovations such as tactile guidance, audible announcements, and mobile wayfinding apps improve accessibility for all passengers.",
            ["accessibility", "innovation", "universal_design"],
            1.0
        ),
        SearchDocument(
            29,
            "Sustainability in Rail Operations",
            "Sustainable practices include energy-efficient vehicles, green station design, and renewable energy sourcing.",
            ["sustainability", "energy", "station_design"],
            1.0
        ),
        SearchDocument(
            30,
            "Labor Relations and Workforce Management",
            "Effective labor relations support service reliability. Workforce management systems optimize scheduling, training, and compliance.",
            ["labor", "workforce", "management"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)