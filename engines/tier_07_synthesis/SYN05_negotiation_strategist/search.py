import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --- Document and Result Classes ---

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

# --- Search Index Class ---

class SearchIndex:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = defaultdict(dict)

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            term_counts = Counter(tokens)
            for term, freq in term_counts.items():
                self.term_freqs[doc.id][term] = freq
                self.term_doc_freqs[term] += 1
            self._idf_cache.clear()
            self._tfidf_cache.clear()
            self._recompute_avg_doc_length()

    def _recompute_avg_doc_length(self):
        if self.total_docs == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        tokens = text.split()
        return [t for t in tokens if len(t) > 1]

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

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * (numerator / denominator)
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        if doc_id in self._tfidf_cache and self._tfidf_cache[doc_id]:
            tfidf_vec = self._tfidf_cache[doc_id]
        else:
            tfidf_vec = {}
            doc_len = self.doc_lengths[doc_id]
            for term, tf in self.term_freqs[doc_id].items():
                idf = self._compute_idf(term)
                tf_norm = tf / doc_len
                tfidf_vec[term] = tf_norm * idf
            self._tfidf_cache[doc_id] = tfidf_vec
        score = 0.0
        for term in query_terms:
            score += tfidf_vec.get(term, 0.0)
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10, method: str = 'bm25') -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        scores: List[Tuple[int, float]] = []
        for doc_id in self.documents:
            if method == 'bm25':
                score = self._score_bm25(query_terms, doc_id)
            elif method == 'tfidf':
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                scores.append((doc_id, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scores[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id=doc.id, score=score, title=doc.title, snippet=snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], max_len: int = 200) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = ' '.join(tokens[:max_len])
        else:
            start = max(positions[0] - 10, 0)
            end = min(start + max_len, len(tokens))
            snippet = ' '.join(tokens[start:end])
        return snippet[:max_len] + ('...' if len(snippet) > max_len else '')

    def get_stats(self) -> Dict[str, int]:
        return {
            'total_documents': self.total_docs,
            'unique_terms': len(self.term_doc_freqs),
            'avg_doc_length': int(self.avg_doc_length)
        }

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

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Principled Negotiation: Getting to Yes",
            "Principled negotiation focuses on interests, not positions. It emphasizes mutual gains, objective criteria, and separating people from the problem. The four pillars are: people, interests, options, and criteria.",
            ["principled negotiation", "getting to yes", "mutual gains"],
            1.0
        ),
        SearchDocument(
            2,
            "BATNA Analysis and Reservation Price",
            "BATNA stands for Best Alternative to a Negotiated Agreement. Knowing your BATNA and reservation price is critical to negotiation preparation and leverage. Always improve your BATNA and estimate the other party's BATNA.",
            ["BATNA", "reservation price", "leverage"],
            1.0
        ),
        SearchDocument(
            3,
            "ZOPA: Zone of Possible Agreement",
            "ZOPA is the overlap between parties' reservation prices. Identifying ZOPA enables negotiators to focus on feasible deals and avoid impasse.",
            ["ZOPA", "zone of possible agreement", "reservation price"],
            1.0
        ),
        SearchDocument(
            4,
            "Anchoring and Adjustment Heuristic",
            "Anchoring is the cognitive bias where the first number offered in negotiation sets the tone. Adjustment refers to the incremental changes from the anchor. Effective negotiators use anchors strategically.",
            ["anchoring", "adjustment", "cognitive bias"],
            1.0
        ),
        SearchDocument(
            5,
            "Concession Strategy and Pattern",
            "Concessions are the currency of negotiation. Plan your concession pattern, avoid large early concessions, and reciprocate strategically. Track concessions to maintain leverage.",
            ["concession", "strategy", "pattern"],
            1.0
        ),
        SearchDocument(
            6,
            "Integrative (Win-Win) Negotiation",
            "Integrative negotiation seeks to expand the pie and create value for all parties. It involves sharing information, exploring interests, and inventing options for mutual gain.",
            ["integrative negotiation", "win-win", "mutual gain"],
            1.0
        ),
        SearchDocument(
            7,
            "Distributive (Win-Lose) Negotiation",
            "Distributive negotiation is about claiming value and dividing a fixed pie. It is competitive, often involves positional bargaining, and focuses on maximizing individual outcomes.",
            ["distributive negotiation", "win-lose", "competitive"],
            1.0
        ),
        SearchDocument(
            8,
            "Multiparty Negotiation Dynamics",
            "Multiparty negotiations involve coalitions, voting, and complex communication. Managing group dynamics, aligning interests, and preventing fragmentation are key challenges.",
            ["multiparty negotiation", "coalitions", "group dynamics"],
            1.0
        ),
        SearchDocument(
            9,
            "Impasse Breaking and Dispute Resolution Ladder",
            "Impasse can be broken by reframing issues, introducing mediators, or escalating to arbitration. The dispute resolution ladder includes negotiation, mediation, arbitration, and litigation.",
            ["impasse", "dispute resolution", "mediation"],
            1.0
        ),
        SearchDocument(
            10,
            "Deal Structure and Term Prioritization",
            "Structuring deals involves prioritizing terms, sequencing issues, and packaging concessions. Identify must-haves versus tradeables and use deal structuring to facilitate agreement.",
            ["deal structure", "term prioritization", "sequencing"],
            1.0
        ),
        SearchDocument(
            11,
            "Information Asymmetry and Signaling",
            "Negotiators often face information asymmetry. Use signaling to communicate intentions, and beware of misdirection. Ask questions to reduce information gaps.",
            ["information asymmetry", "signaling", "misdirection"],
            1.0
        ),
        SearchDocument(
            12,
            "Mnookin Beyond Winning Framework",
            "Mnookin's Beyond Winning framework emphasizes negotiation as a process for relationship building, creative problem solving, and ethical advocacy. It balances client interests and broader values.",
            ["mnookin", "beyond winning", "ethical advocacy"],
            1.0
        ),
        SearchDocument(
            13,
            "Game Theory Applications in Negotiation",
            "Game theory provides tools for analyzing negotiation strategies, including Nash equilibrium, zero-sum games, and cooperative games. Use game theory to anticipate moves and optimize outcomes.",
            ["game theory", "nash equilibrium", "zero-sum"],
            1.0
        ),
        SearchDocument(
            14,
            "Deadline Pressure and Time Tactics",
            "Deadlines create pressure and can be used as negotiation tactics. Time management, pacing, and strategic delays influence outcomes. Beware of artificial deadlines.",
            ["deadline", "time tactics", "pressure"],
            1.0
        ),
        SearchDocument(
            15,
            "Cross-Cultural Negotiation Dynamics",
            "Negotiation across cultures requires sensitivity to values, communication styles, and norms. Adapt strategies to cultural context and avoid ethnocentrism.",
            ["cross-cultural", "values", "communication"],
            1.0
        ),
        SearchDocument(
            16,
            "Email and Virtual Negotiation Challenges",
            "Virtual negotiations lack nonverbal cues, increasing risk of misunderstanding. Use clear language, confirm assumptions, and build rapport online.",
            ["email negotiation", "virtual", "rapport"],
            1.0
        ),
        SearchDocument(
            17,
            "Power Dynamics and Leverage Sources",
            "Power in negotiation comes from information, alternatives, relationships, and legitimacy. Identify sources of leverage and use them ethically.",
            ["power dynamics", "leverage", "alternatives"],
            1.0
        ),
        SearchDocument(
            18,
            "Reactive Devaluation and Psychological Biases",
            "Reactive devaluation is the tendency to dismiss proposals from the opposing party. Recognize psychological biases to improve negotiation outcomes.",
            ["reactive devaluation", "psychological bias", "negotiation"],
            1.0
        ),
        SearchDocument(
            19,
            "Negotiating with Agents and Principals",
            "Negotiations often involve agents representing principals. Clarify authority, align interests, and manage communication between parties.",
            ["agents", "principals", "authority"],
            1.0
        ),
        SearchDocument(
            20,
            "Contingent Contracts and Risk Management",
            "Contingent contracts address uncertainty by linking outcomes to future events. Use them to manage risk and bridge gaps in expectations.",
            ["contingent contract", "risk management", "uncertainty"],
            1.0
        ),
        SearchDocument(
            21,
            "Post-Settlement Settlement and Continuous Improvement",
            "Post-settlement settlement involves revisiting agreements to create additional value. Continuous improvement in negotiation processes leads to better outcomes.",
            ["post-settlement", "continuous improvement", "value"],
            1.0
        ),
        SearchDocument(
            22,
            "Negotiation Ethics and Deception",
            "Ethical negotiation requires honesty, transparency, and respect. Deception undermines trust and can damage relationships.",
            ["ethics", "deception", "trust"],
            1.0
        ),
        SearchDocument(
            23,
            "Internal Alignment and Stakeholder Management",
            "Aligning internal stakeholders is crucial for negotiation success. Manage expectations, communicate priorities, and build consensus.",
            ["internal alignment", "stakeholder management", "consensus"],
            1.0
        ),
        SearchDocument(
            24,
            "Gender and Diversity in Negotiation",
            "Gender and diversity influence negotiation styles, outcomes, and perceptions. Promote inclusivity and recognize unconscious bias.",
            ["gender", "diversity", "inclusivity"],
            1.0
        ),
        SearchDocument(
            25,
            "Relationship vs Transaction Focus",
            "Negotiators must balance relationship-building with transactional goals. Long-term relationships often yield greater value than short-term wins.",
            ["relationship", "transaction", "long-term"],
            1.0
        ),
        SearchDocument(
            26,
            "Interest-Based Bargaining Techniques",
            "Interest-based bargaining uncovers underlying motivations and needs. Use open-ended questions and active listening to reveal interests.",
            ["interest-based", "bargaining", "active listening"],
            1.0
        ),
        SearchDocument(
            27,
            "Negotiation Preparation Checklist",
            "Effective preparation includes defining objectives, researching parties, setting BATNA, and planning strategy. Preparation is the foundation of negotiation success.",
            ["preparation", "checklist", "objectives"],
            1.0
        ),
        SearchDocument(
            28,
            "Negotiation Styles and Adaptation",
            "Negotiators may be competitive, collaborative, accommodating, or avoiding. Adapt your style to the context and counterpart.",
            ["negotiation style", "adaptation", "collaborative"],
            1.0
        ),
        SearchDocument(
            29,
            "Negotiation Communication Skills",
            "Communication skills include listening, questioning, framing, and persuasion. Mastering communication improves negotiation outcomes.",
            ["communication", "listening", "persuasion"],
            1.0
        ),
        SearchDocument(
            30,
            "Negotiation in Complex Projects",
            "Complex projects require multi-issue negotiation, stakeholder mapping, and iterative agreement. Use project management tools to support negotiation.",
            ["complex projects", "stakeholder mapping", "multi-issue"],
            1.0
        ),
        SearchDocument(
            31,
            "Negotiation Outcome Evaluation",
            "Evaluate negotiation outcomes using objective criteria, satisfaction, and relationship impact. Learn from each negotiation to improve future performance.",
            ["outcome evaluation", "objective criteria", "satisfaction"],
            1.0
        ),
        SearchDocument(
            32,
            "Negotiation Tactics: Hardball vs Softball",
            "Hardball tactics include threats, bluffing, and ultimatums. Softball tactics focus on collaboration and rapport. Choose tactics based on context and desired outcomes.",
            ["tactics", "hardball", "softball"],
            1.0
        ),
        SearchDocument(
            33,
            "Negotiation and Emotional Intelligence",
            "Emotional intelligence helps negotiators manage emotions, build rapport, and resolve conflict. Self-awareness and empathy are key skills.",
            ["emotional intelligence", "rapport", "conflict resolution"],
            1.0
        ),
        SearchDocument(
            34,
            "Negotiation and Technology",
            "Technology enables virtual negotiation, document sharing, and analytics. Use technology to enhance negotiation efficiency and effectiveness.",
            ["technology", "virtual negotiation", "analytics"],
            1.0
        ),
        SearchDocument(
            35,
            "Negotiation and Trust Building",
            "Trust is foundational to successful negotiation. Build trust through reliability, transparency, and consistent behavior.",
            ["trust", "transparency", "reliability"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)