import threading
import math
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

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
        self.doc_tokens: Dict[int, List[str]] = {}
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._recompute_stats()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_tokens[doc.id] = tokens
            self.doc_lengths[doc.id] = len(tokens)
            term_counts = Counter(tokens)
            for term, count in term_counts.items():
                self.inverted_index[term][doc.id] = count
            self._recompute_stats()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        candidate_docs = set()
        for token in query_tokens:
            candidate_docs.update(self.inverted_index.get(token, {}).keys())
        scored_results = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            final_score = 0.7 * bm25_score + 0.3 * tfidf_score
            snippet = self._make_snippet(self.documents[doc_id], query_tokens)
            scored_results.append(SearchResult(doc_id, final_score, self.documents[doc_id].title, snippet))
        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                'num_documents': self.N,
                'avg_doc_length': self.avg_doc_length,
                'vocab_size': len(self.inverted_index)
            }

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-z0-9]{2,}\b', text.lower())
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = len(self.inverted_index.get(term, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_tokens: List[str], k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in set(query_tokens):
            tf = self.inverted_index.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            denom = tf + k1 * (1 - b + b * doc_len / self.avg_doc_length)
            score += idf * ((tf * (k1 + 1)) / denom)
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_tokens: List[str]) -> float:
        tfidf = 0.0
        doc_len = self.doc_lengths[doc_id]
        term_counts = self.inverted_index
        for term in set(query_tokens):
            tf = term_counts.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len
            idf = self._compute_idf(term)
            tfidf += tf_norm * idf
        return tfidf * self.documents[doc_id].weight

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            return content[:160] + ('...' if len(content) > 160 else '')
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for qt in set(query_tokens):
            snippet = re.sub(r'\b(%s)\b' % re.escape(qt), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet

    def _recompute_stats(self):
        self.N = len(self.documents)
        if self.N == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N
        self.idf_cache.clear()

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "CDL Requirements Overview",
            "Commercial Driver's License (CDL) requirements are governed by 49 CFR 383. Drivers operating commercial motor vehicles must meet age, medical, and knowledge requirements, and pass skills tests. Endorsements are required for hazardous materials, passenger, and tank vehicles.",
            ["CDL", "49 CFR 383", "Licensing"],
            1.0
        ),
        SearchDocument(
            2,
            "Hours of Service Rules",
            "49 CFR 395 outlines Hours of Service (HOS) regulations for property-carrying and passenger-carrying drivers. Key provisions include maximum driving limits, mandatory rest breaks, and recordkeeping requirements. Violations can result in penalties and out-of-service orders.",
            ["HOS", "49 CFR 395", "Fatigue"],
            1.0
        ),
        SearchDocument(
            3,
            "ELD Mandate Compliance",
            "The Electronic Logging Device (ELD) Mandate, under 49 CFR 395.8, requires most commercial drivers to use ELDs to record hours of service. ELDs must meet technical specifications and be registered with the FMCSA.",
            ["ELD", "49 CFR 395.8", "Technology"],
            1.0
        ),
        SearchDocument(
            4,
            "Drug and Alcohol Testing",
            "49 CFR 382 requires employers to implement drug and alcohol testing programs for safety-sensitive transportation employees. Testing includes pre-employment, random, post-accident, reasonable suspicion, and return-to-duty testing.",
            ["Drug Testing", "Alcohol", "49 CFR 382"],
            1.0
        ),
        SearchDocument(
            5,
            "Vehicle Inspection and Maintenance",
            "Vehicle inspection and maintenance standards are set by 49 CFR 396. Carriers must systematically inspect, repair, and maintain all vehicles. Drivers must complete daily vehicle inspection reports (DVIR).",
            ["Inspection", "Maintenance", "49 CFR 396"],
            1.0
        ),
        SearchDocument(
            6,
            "Weight Limits and Bridge Formula",
            "23 USC 127 establishes federal weight limits for commercial vehicles and the Bridge Formula for axle weight distribution. Violations can result in fines and restricted route access.",
            ["Weight Limits", "Bridge Formula", "23 USC 127"],
            1.0
        ),
        SearchDocument(
            7,
            "Oversize Permits and Routing",
            "Oversize and overweight vehicles require special permits and routing. State DOTs issue permits with specific conditions, including escort vehicles, travel time restrictions, and route surveys.",
            ["Oversize", "Permits", "Routing"],
            1.0
        ),
        SearchDocument(
            8,
            "Hazmat Transportation Regulations",
            "Hazardous materials transportation is regulated by PHMSA under 49 CFR 171-180. Requirements include proper packaging, labeling, placarding, shipping papers, and emergency response information.",
            ["Hazmat", "PHMSA", "49 CFR 171-180"],
            1.0
        ),
        SearchDocument(
            9,
            "Railroad Track Safety Standards",
            "FRA regulations 49 CFR 213-243 cover railroad track safety, inspection, maintenance, and employee qualifications. Railroads must comply with standards for track geometry, structure, and operations.",
            ["Railroad", "FRA", "49 CFR 213-243"],
            1.0
        ),
        SearchDocument(
            10,
            "FAA General Operating Rules",
            "14 CFR Part 91 sets general operating and flight rules for civil aviation. Topics include pilot certification, flight operations, equipment requirements, and airspace use.",
            ["FAA", "14 CFR Part 91", "Aviation"],
            1.0
        ),
        SearchDocument(
            11,
            "FAA Part 121 Air Carrier Operations",
            "FAA Part 121 governs scheduled air carrier operations, including crew qualifications, flight time limitations, maintenance, and operational control. Compliance is mandatory for airlines.",
            ["FAA", "Part 121", "Air Carrier"],
            1.0
        ),
        SearchDocument(
            12,
            "USDOT Number and Operating Authority",
            "Motor carriers must obtain a USDOT Number and, if applicable, operating authority from FMCSA. Registration is required for interstate commerce and certain intrastate carriers.",
            ["USDOT", "Operating Authority", "FMCSA"],
            1.0
        ),
        SearchDocument(
            13,
            "State DOT Compliance and UCR",
            "State Departments of Transportation (DOTs) enforce federal and state regulations. The Unified Carrier Registration (UCR) program requires carriers to register and pay fees annually.",
            ["State DOT", "UCR", "Registration"],
            1.0
        ),
        SearchDocument(
            14,
            "CSA Safety Measurement System",
            "FMCSA's Compliance, Safety, Accountability (CSA) program uses the Safety Measurement System (SMS) to assess carrier safety performance. SMS scores are based on roadside inspections, violations, and crash data.",
            ["CSA", "SMS", "FMCSA"],
            1.0
        ),
        SearchDocument(
            15,
            "Medical Certification Standards",
            "49 CFR 391.41-391.49 set medical qualification standards for commercial drivers. Drivers must be examined by a certified medical examiner and carry a valid medical certificate.",
            ["Medical", "49 CFR 391.41", "Certification"],
            1.0
        ),
        SearchDocument(
            16,
            "Cargo Securement Requirements",
            "Cargo securement regulations in 49 CFR 393.100-393.142 require carriers to prevent shifting or falling cargo. Specific rules apply to different commodities and securement devices.",
            ["Cargo Securement", "49 CFR 393", "Safety"],
            1.0
        ),
        SearchDocument(
            17,
            "Insurance and Financial Responsibility",
            "49 CFR 387 mandates minimum insurance requirements for motor carriers. Proof of financial responsibility must be maintained and provided upon request.",
            ["Insurance", "49 CFR 387", "Financial Responsibility"],
            1.0
        ),
        SearchDocument(
            18,
            "Roadside Inspection Levels",
            "The Commercial Vehicle Safety Alliance (CVSA) defines six levels of roadside inspections, ranging from full vehicle and driver inspections to walk-arounds and paperwork checks.",
            ["CVSA", "Roadside Inspection", "Safety"],
            1.0
        ),
        SearchDocument(
            19,
            "Wireless Communication Prohibition",
            "49 CFR 392.82 prohibits commercial drivers from using hand-held mobile phones while driving. Violations can result in fines and disqualification.",
            ["Wireless", "49 CFR 392.82", "Cell Phone"],
            1.0
        ),
        SearchDocument(
            20,
            "Broker Authority and Bond",
            "49 CFR 371 requires freight brokers to obtain operating authority and maintain a surety bond or trust fund. Brokers must keep transaction records for three years.",
            ["Broker", "49 CFR 371", "Bond"],
            1.0
        ),
        SearchDocument(
            21,
            "Passenger Carrier Safety",
            "49 CFR 390-399 contain safety regulations for passenger carriers, including vehicle standards, driver qualifications, and operational rules.",
            ["Passenger Carrier", "49 CFR 390-399", "Safety"],
            1.0
        ),
        SearchDocument(
            22,
            "Transportation Worker Identification Credential (TWIC)",
            "TWIC is a TSA-issued credential required for workers needing unescorted access to secure areas of maritime facilities and vessels. Enrollment includes a security threat assessment and fingerprinting.",
            ["TWIC", "Credential", "Maritime"],
            1.0
        ),
        SearchDocument(
            23,
            "Fatality Analysis Reporting System (FARS)",
            "FARS is a nationwide database maintained by NHTSA that collects data on fatal motor vehicle crashes. It is used for research, policy, and safety analysis.",
            ["FARS", "NHTSA", "Crash Data"],
            1.0
        ),
        SearchDocument(
            24,
            "Driver Qualification File (DQF) Requirements",
            "Carriers must maintain a Driver Qualification File for each driver, including application, MVR, medical certificate, and safety performance history, per 49 CFR 391.",
            ["DQF", "49 CFR 391", "Driver File"],
            1.0
        ),
        SearchDocument(
            25,
            "Random Drug Testing Rates",
            "FMCSA sets annual minimum random drug and alcohol testing rates for CDL drivers. Employers must ensure compliance and maintain records of testing.",
            ["Drug Testing", "FMCSA", "Random Testing"],
            1.0
        ),
        SearchDocument(
            26,
            "Hazmat Security Plan Requirements",
            "Carriers transporting certain hazardous materials must develop and implement a security plan per 49 CFR 172.800. Plans address personnel security, unauthorized access, and en route security.",
            ["Hazmat", "Security Plan", "49 CFR 172.800"],
            1.0
        ),
        SearchDocument(
            27,
            "Out-of-Service Criteria",
            "CVSA publishes out-of-service criteria for vehicles and drivers found in violation of critical safety regulations during inspections. Out-of-service orders require immediate correction.",
            ["CVSA", "Out-of-Service", "Inspection"],
            1.0
        ),
        SearchDocument(
            28,
            "Driver's Record of Duty Status",
            "Drivers must maintain a record of duty status (RODS) to document hours worked and rest periods, as required by 49 CFR 395. ELDs are the preferred method for RODS.",
            ["RODS", "49 CFR 395", "ELD"],
            1.0
        ),
        SearchDocument(
            29,
            "Annual Vehicle Inspection",
            "49 CFR 396.17 requires commercial vehicles to undergo an annual inspection by a qualified inspector. Inspection reports must be retained for at least 14 months.",
            ["Inspection", "49 CFR 396.17", "Annual"],
            1.0
        ),
        SearchDocument(
            30,
            "CSA BASICs Categories",
            "CSA's BASICs (Behavior Analysis and Safety Improvement Categories) include Unsafe Driving, Hours-of-Service Compliance, Driver Fitness, Controlled Substances/Alcohol, Vehicle Maintenance, Hazardous Materials Compliance, and Crash Indicator.",
            ["CSA", "BASICs", "FMCSA"],
            1.0
        ),
        SearchDocument(
            31,
            "Hazmat Placarding Requirements",
            "Proper placarding is required for vehicles transporting hazardous materials per 49 CFR 172.500. Placards must be visible and correspond to the hazard class.",
            ["Hazmat", "Placarding", "49 CFR 172.500"],
            1.0
        ),
        SearchDocument(
            32,
            "Railroad Employee Training",
            "49 CFR 243 requires railroads to develop and submit employee training programs for FRA approval. Training must cover safety, operations, and regulatory compliance.",
            ["Railroad", "Employee Training", "49 CFR 243"],
            1.0
        ),
        SearchDocument(
            33,
            "Aviation Drug and Alcohol Testing",
            "FAA requires drug and alcohol testing for safety-sensitive aviation employees under 14 CFR Part 120. Testing includes pre-employment, random, and post-accident.",
            ["FAA", "Drug Testing", "14 CFR Part 120"],
            1.0
        ),
        SearchDocument(
            34,
            "Unified Carrier Registration (UCR) Fees",
            "UCR fees are based on the size of a carrier's fleet and must be paid annually. Failure to pay can result in enforcement action by state agencies.",
            ["UCR", "Fees", "State DOT"],
            1.0
        ),
        SearchDocument(
            35,
            "Intermodal Equipment Provider Requirements",
            "49 CFR 390.21 requires intermodal equipment providers to register with FMCSA and mark equipment with a USDOT number. Providers are responsible for maintenance and repairs.",
            ["Intermodal", "Equipment", "49 CFR 390.21"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)