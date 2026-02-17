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

# --- Search Index ---

class SearchIndex:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_doc_tf: Dict[str, Dict[int, int]] = defaultdict(lambda: defaultdict(int))
        self.idf_cache: Dict[str, float] = {}
        self.tf_idf_cache: Dict[int, Dict[str, float]] = defaultdict(dict)
        self.lock = threading.Lock()
        self._doc_id_counter = 1

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())
        return tokens

    def add_document(self, title: str, content: str, tags: List[str], weight: float = 1.0) -> int:
        with self.lock:
            doc_id = self._doc_id_counter
            self._doc_id_counter += 1
            document = SearchDocument(doc_id, title, content, tags, weight)
            self.documents[doc_id] = document

            tokens = self._tokenize(content)
            self.doc_lengths[doc_id] = len(tokens)
            token_counts = Counter(tokens)
            for token, count in token_counts.items():
                self.term_doc_freq[token] += 1
                self.term_doc_tf[token][doc_id] = count

            self._update_avg_doc_length()
            self.idf_cache.clear()
            self.tf_idf_cache.clear()
            return doc_id

    def _update_avg_doc_length(self):
        if self.doc_lengths:
            self.avg_doc_length = sum(self.doc_lengths.values()) / len(self.doc_lengths)
        else:
            self.avg_doc_length = 0.0

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        N = len(self.documents)
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        document = self.documents[doc_id]
        for term in query_terms:
            tf = self.term_doc_tf.get(term, {}).get(doc_id, 0)
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_length / (self.avg_doc_length or 1))
            bm25_score = idf * (numerator / (denominator or 1))
            score += bm25_score
        return score * document.weight

    def _score_tf_idf(self, query_terms: List[str], doc_id: int) -> float:
        if doc_id in self.tf_idf_cache:
            tf_idf_vec = self.tf_idf_cache[doc_id]
        else:
            tf_idf_vec = {}
            tokens = self._tokenize(self.documents[doc_id].content)
            token_counts = Counter(tokens)
            doc_length = len(tokens)
            for term in token_counts:
                tf = token_counts[term] / (doc_length or 1)
                idf = self._compute_idf(term)
                tf_idf_vec[term] = tf * idf
            self.tf_idf_cache[doc_id] = tf_idf_vec

        score = 0.0
        for term in query_terms:
            score += tf_idf_vec.get(term, 0.0)
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10, use_bm25: bool = True, use_tf_idf: bool = True) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[int, float] = {}
        for doc_id in self.documents:
            bm25_score = self._score_bm25(query_terms, doc_id) if use_bm25 else 0.0
            tf_idf_score = self._score_tf_idf(query_terms, doc_id) if use_tf_idf else 0.0
            score = bm25_score + tf_idf_score
            if score > 0:
                doc_scores[doc_id] = score

        top_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in top_docs:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            result = SearchResult(doc_id, score, doc.title, snippet)
            results.append(result)
        return results

    def _make_snippet(self, content: str, query_terms: List[str], snippet_len: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, token in enumerate(tokens) if token in query_terms]
        if not positions:
            snippet = ' '.join(tokens[:snippet_len])
        else:
            start = max(positions[0] - 10, 0)
            end = min(start + snippet_len, len(tokens))
            snippet = ' '.join(tokens[start:end])
        return snippet + ('...' if len(tokens) > snippet_len else '')

    def get_stats(self) -> Dict[str, int]:
        return {
            'documents': len(self.documents),
            'unique_terms': len(self.term_doc_freq),
            'avg_doc_length': int(self.avg_doc_length),
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
        # Goal Decomposition via Hierarchical Task Networks
        ("Hierarchical Task Networks in Goal Decomposition",
         "Hierarchical Task Networks (HTNs) are used to break complex goals into manageable sub-tasks. HTNs enable AGI03 to recursively decompose objectives, ensuring clarity and actionable steps.",
         ["HTN", "Goal Decomposition", "Planning"], 1.0),
        ("HTN: Recursive Subgoal Generation",
         "AGI03 leverages recursive subgoal generation to structure tasks. Each parent goal is decomposed until atomic actions are identified, facilitating efficient execution.",
         ["HTN", "Subgoal", "Recursion"], 1.0),
        ("HTN: Temporal and Resource Constraints",
         "HTNs incorporate temporal and resource constraints, allowing AGI03 to optimize task sequences and allocate resources effectively.",
         ["HTN", "Resource Allocation", "Temporal"], 1.0),
        # Objectives and Key Results (OKR) Framework
        ("OKR Framework: Setting Objectives",
         "Objectives in OKR are ambitious, qualitative goals. AGI03 sets objectives aligned with organizational vision, driving focus and motivation.",
         ["OKR", "Objectives", "Vision"], 1.0),
        ("OKR Framework: Key Results",
         "Key Results are measurable outcomes that track progress toward objectives. AGI03 defines clear, quantifiable KRs to ensure accountability.",
         ["OKR", "Key Results", "Measurement"], 1.0),
        ("OKR: Quarterly Review and Calibration",
         "AGI03 conducts quarterly OKR reviews, calibrating goals based on performance and changing priorities.",
         ["OKR", "Review", "Calibration"], 1.0),
        # SMART Goal Enforcement
        ("SMART Goals: Specificity and Measurability",
         "AGI03 enforces SMART criteria: Specific, Measurable, Achievable, Relevant, and Time-bound. Each goal is validated for clarity and feasibility.",
         ["SMART", "Goal Setting", "Validation"], 1.0),
        ("SMART: Achievability and Stretch",
         "Goals are calibrated for achievability, targeting a 70% success rate to promote stretch and innovation.",
         ["SMART", "Stretch Goals", "Achievability"], 1.0),
        ("SMART: Time-bound Execution",
         "AGI03 ensures all goals have explicit deadlines, driving timely execution and progress tracking.",
         ["SMART", "Time-bound", "Execution"], 1.0),
        # Eisenhower Priority Matrix
        ("Eisenhower Matrix: Urgent vs Important",
         "The Eisenhower Matrix categorizes tasks into four quadrants: Urgent-Important, Not Urgent-Important, Urgent-Not Important, Not Urgent-Not Important. AGI03 prioritizes accordingly.",
         ["Eisenhower", "Priority", "Urgency"], 1.0),
        ("Eisenhower: Quadrant Analysis",
         "AGI03 analyzes task quadrants to focus on high-impact, non-urgent tasks, reducing reactive work.",
         ["Eisenhower", "Quadrant", "Analysis"], 1.0),
        ("Eisenhower: Delegation and Scheduling",
         "Tasks in the Urgent-Not Important quadrant are delegated, while Not Urgent-Important tasks are scheduled for strategic focus.",
         ["Eisenhower", "Delegation", "Scheduling"], 1.0),
        # MoSCoW Prioritization
        ("MoSCoW: Must, Should, Could, Won't",
         "MoSCoW prioritization assigns tasks to Must, Should, Could, and Won't categories. AGI03 uses this method to clarify deliverables.",
         ["MoSCoW", "Prioritization", "Deliverables"], 1.0),
        ("MoSCoW: Dynamic Reprioritization",
         "AGI03 dynamically reprioritizes tasks based on changing requirements and resource availability.",
         ["MoSCoW", "Dynamic", "Reprioritization"], 1.0),
        ("MoSCoW: Stakeholder Alignment",
         "Stakeholder input is integrated into MoSCoW prioritization, ensuring alignment and transparency.",
         ["MoSCoW", "Stakeholder", "Alignment"], 1.0),
        # RICE Scoring for Prioritization
        ("RICE Scoring: Reach, Impact, Confidence, Effort",
         "AGI03 uses RICE scoring to prioritize initiatives. Reach, Impact, Confidence, and Effort are quantified for objective decision-making.",
         ["RICE", "Scoring", "Prioritization"], 1.0),
        ("RICE: Quantitative Prioritization",
         "RICE scores are calculated to rank tasks, maximizing value delivery and minimizing wasted effort.",
         ["RICE", "Quantitative", "Ranking"], 1.0),
        ("RICE: Confidence Calibration",
         "AGI03 calibrates confidence scores using historical data and expert input to improve prioritization accuracy.",
         ["RICE", "Confidence", "Calibration"], 1.0),
        # Resource Allocation via Linear Programming
        ("Linear Programming: Optimal Resource Allocation",
         "AGI03 applies linear programming to allocate resources optimally across competing tasks, maximizing efficiency.",
         ["Linear Programming", "Resource Allocation", "Optimization"], 1.0),
        ("LP: Constraints and Objective Functions",
         "Constraints and objective functions are defined for each allocation problem, enabling AGI03 to solve for optimal solutions.",
         ["LP", "Constraints", "Objective Function"], 1.0),
        ("LP: Real-time Adjustment",
         "AGI03 adjusts resource allocations in real-time based on task progress and changing constraints.",
         ["LP", "Real-time", "Adjustment"], 1.0),
        # Opportunity Cost Analysis
        ("Opportunity Cost: Decision Analysis",
         "AGI03 evaluates opportunity costs for each decision, ensuring resources are allocated to the highest-value tasks.",
         ["Opportunity Cost", "Decision", "Analysis"], 1.0),
        ("Opportunity Cost: Comparative Evaluation",
         "Comparative evaluation of alternatives is performed to quantify opportunity costs and inform prioritization.",
         ["Opportunity Cost", "Comparative", "Evaluation"], 1.0),
        ("Opportunity Cost: Risk Assessment",
         "AGI03 integrates risk assessment into opportunity cost analysis, balancing potential rewards and losses.",
         ["Opportunity Cost", "Risk", "Assessment"], 1.0),
        # Risk-Reward Balancing and Expected Value Analysis
        ("Risk-Reward: Expected Value Analysis",
         "AGI03 calculates expected value for each initiative, balancing risk and reward to optimize outcomes.",
         ["Risk-Reward", "Expected Value", "Analysis"], 1.0),
        ("Risk-Reward: Probability Modeling",
         "Probability modeling is used to estimate risks and rewards, supporting rational decision-making.",
         ["Risk-Reward", "Probability", "Modeling"], 1.0),
        ("Risk-Reward: Portfolio Optimization",
         "AGI03 optimizes task portfolios by balancing risk and reward across multiple initiatives.",
         ["Risk-Reward", "Portfolio", "Optimization"], 1.0),
        # Stretch Goal Calibration (70% Achievability Target)
        ("Stretch Goals: Calibration for Innovation",
         "Stretch goals are set to achieve a 70% success rate, encouraging innovation while maintaining achievability.",
         ["Stretch Goals", "Calibration", "Innovation"], 1.0),
        ("Stretch Goals: Feedback Loops",
         "AGI03 uses feedback loops to calibrate stretch goals, adjusting targets based on performance data.",
         ["Stretch Goals", "Feedback", "Calibration"], 1.0),
        ("Stretch Goals: Motivation and Engagement",
         "Well-calibrated stretch goals enhance motivation and engagement, driving superior performance.",
         ["Stretch Goals", "Motivation", "Engagement"], 1.0),
        # Moonshot Thinking (10x vs 10%)
        ("Moonshot Thinking: 10x Innovation",
         "AGI03 applies moonshot thinking to pursue 10x improvements, challenging conventional limits.",
         ["Moonshot", "10x", "Innovation"], 1.0),
        ("Moonshot: Risk Tolerance",
         "Moonshot initiatives require higher risk tolerance and visionary leadership. AGI03 balances risk with potential rewards.",
         ["Moonshot", "Risk", "Vision"], 1.0),
        ("Moonshot: Incremental vs Exponential",
         "AGI03 distinguishes between incremental (10%) and exponential (10x) improvements, prioritizing transformative opportunities.",
         ["Moonshot", "Incremental", "Exponential"], 1.0),
        # AGI03 Doctrine Integration
        ("AGI03: Integrated Goal Management",
         "AGI03 integrates HTN, OKR, SMART, Eisenhower, MoSCoW, RICE, LP, Opportunity Cost, Risk-Reward, Stretch Goals, and Moonshot frameworks for holistic goal management.",
         ["AGI03", "Integration", "Goal Management"], 1.5),
        ("AGI03: Adaptive Prioritization Engine",
         "The AGI03 engine adapts prioritization dynamically using multiple frameworks, ensuring optimal resource allocation and goal achievement.",
         ["AGI03", "Adaptive", "Prioritization"], 1.5),
        ("AGI03: Autonomous Goal Calibration",
         "AGI03 autonomously calibrates goals, leveraging feedback, analytics, and strategic frameworks for continuous improvement.",
         ["AGI03", "Autonomous", "Calibration"], 1.5),
    ]
    for title, content, tags, weight in docs:
        index.add_document(title, content, tags, weight)