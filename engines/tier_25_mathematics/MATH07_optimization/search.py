import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Any, Optional

class SearchDocument:
    def __init__(self, doc_id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = doc_id
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
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self.k1 = 1.5
        self.b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            token_counts = Counter(tokens)
            for token, freq in token_counts.items():
                self.term_freqs[token][doc.id] = freq
                self.term_doc_freqs[token] += 1
            self._update_avg_doc_length()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        candidate_docs = set()
        for token in query_tokens:
            candidate_docs.update(self.term_freqs[token].keys())
        scores = {}
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            doc_weight = self.documents[doc_id].weight
            combined_score = bm25_score * 0.7 + tfidf_score * 0.3
            combined_score *= doc_weight
            scores[doc_id] = combined_score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, Any]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freqs),
            'documents': list(self.documents.keys())
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: str, query_tokens: List[str]) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        for term in query_tokens:
            idf = self._compute_idf(term)
            freq = self.term_freqs[term].get(doc_id, 0)
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * doc_length / avg_dl)
            if denominator == 0:
                continue
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id: str, query_tokens: List[str]) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        for term in query_tokens:
            tf = self.term_freqs[term].get(doc_id, 0)
            if doc_length > 0:
                tf_norm = tf / doc_length
            else:
                tf_norm = 0.0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, content: str, query_tokens: List[str], max_length: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            snippet = ' '.join(tokens[:max_length])
        else:
            start = max(positions[0] - 10, 0)
            end = min(positions[0] + 20, len(tokens))
            snippet = ' '.join(tokens[start:end])
        snippet = snippet.strip()
        if len(snippet) > max_length:
            snippet = snippet[:max_length] + '...'
        return snippet

    def _update_avg_doc_length(self):
        if self.total_docs == 0:
            self.avg_doc_length = 0.0
        else:
            total_length = sum(self.doc_lengths.values())
            self.avg_doc_length = total_length / self.total_docs

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
            doc_id="1",
            title="Optimization Principles in Mathematics",
            content="Optimization is a branch of mathematics concerned with finding the best solution from all feasible solutions. Topics include convex optimization, linear programming, and nonlinear optimization.",
            tags=["optimization", "mathematics", "convex", "linear", "nonlinear"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="2",
            title="Convex Sets and Functions",
            content="Convex sets and convex functions are foundational in optimization theory. A set is convex if the line segment between any two points in the set lies entirely within the set.",
            tags=["convex", "sets", "functions", "optimization"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="3",
            title="Linear Programming Methods",
            content="Linear programming involves optimizing a linear objective function subject to linear equality and inequality constraints. The simplex method and interior-point methods are commonly used.",
            tags=["linear programming", "simplex", "interior-point", "optimization"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="4",
            title="Nonlinear Optimization Techniques",
            content="Nonlinear optimization deals with objective functions that are not linear. Techniques include gradient descent, Newton's method, and Lagrange multipliers.",
            tags=["nonlinear", "gradient descent", "Newton", "Lagrange"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="5",
            title="Duality in Optimization",
            content="Duality provides a framework for analyzing optimization problems by relating them to dual problems. Strong duality holds for convex problems under certain conditions.",
            tags=["duality", "convex", "optimization", "strong duality"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="6",
            title="KKT Conditions",
            content="The Karush-Kuhn-Tucker (KKT) conditions are necessary for a solution in nonlinear programming to be optimal, given certain regularity conditions.",
            tags=["KKT", "nonlinear", "optimality", "regularity"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="7",
            title="Gradient Methods",
            content="Gradient methods are iterative techniques for finding local minima of differentiable functions. Examples include steepest descent and conjugate gradient.",
            tags=["gradient", "steepest descent", "conjugate gradient"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="8",
            title="Interior-Point Algorithms",
            content="Interior-point algorithms are efficient for large-scale linear and nonlinear programming. They traverse the interior of the feasible region.",
            tags=["interior-point", "linear", "nonlinear", "feasible region"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="9",
            title="Simplex Algorithm",
            content="The simplex algorithm is a popular method for solving linear programming problems. It moves along the edges of the feasible region to find the optimal vertex.",
            tags=["simplex", "linear programming", "feasible region"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="10",
            title="Lagrange Multipliers",
            content="Lagrange multipliers are used to find extrema of functions subject to equality constraints. They are fundamental in constrained optimization.",
            tags=["Lagrange", "multipliers", "constraints", "optimization"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="11",
            title="Multi-objective Optimization",
            content="Multi-objective optimization involves optimizing several conflicting objectives simultaneously. Pareto optimality is a key concept.",
            tags=["multi-objective", "Pareto", "optimization", "conflicting objectives"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="12",
            title="Stochastic Optimization",
            content="Stochastic optimization deals with uncertainty in optimization problems. Methods include simulated annealing, genetic algorithms, and stochastic gradient descent.",
            tags=["stochastic", "simulated annealing", "genetic algorithms", "gradient descent"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="13",
            title="Constraint Programming",
            content="Constraint programming is a paradigm for solving combinatorial problems by stating constraints that must be satisfied. Applications include scheduling and resource allocation.",
            tags=["constraint programming", "combinatorial", "scheduling", "resource allocation"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="14",
            title="Global Optimization",
            content="Global optimization seeks the best solution over the entire feasible region, not just local optima. Techniques include branch and bound, and evolutionary algorithms.",
            tags=["global optimization", "branch and bound", "evolutionary algorithms"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="15",
            title="Mathematical Programming",
            content="Mathematical programming encompasses optimization problems where the objective and constraints are expressed mathematically. Includes linear, nonlinear, and integer programming.",
            tags=["mathematical programming", "linear", "nonlinear", "integer"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="16",
            title="Integer Programming",
            content="Integer programming restricts some or all variables to integer values. It is used in combinatorial optimization and has applications in logistics and scheduling.",
            tags=["integer programming", "combinatorial", "logistics", "scheduling"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="17",
            title="Dynamic Programming",
            content="Dynamic programming solves complex problems by breaking them down into simpler subproblems. It is widely used in optimization and computer science.",
            tags=["dynamic programming", "optimization", "subproblems"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="18",
            title="Heuristic Methods",
            content="Heuristic methods provide approximate solutions to optimization problems. Examples include greedy algorithms and local search.",
            tags=["heuristic", "greedy algorithms", "local search"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="19",
            title="Metaheuristics",
            content="Metaheuristics are higher-level procedures for guiding heuristics. Examples include genetic algorithms, simulated annealing, and tabu search.",
            tags=["metaheuristics", "genetic algorithms", "simulated annealing", "tabu search"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="20",
            title="Robust Optimization",
            content="Robust optimization deals with uncertainty in optimization models, ensuring solutions remain feasible under varying conditions.",
            tags=["robust optimization", "uncertainty", "feasibility"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="21",
            title="Sensitivity Analysis",
            content="Sensitivity analysis studies how changes in input parameters affect the optimal solution. It is important in decision-making.",
            tags=["sensitivity analysis", "parameters", "optimal solution"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="22",
            title="Machine Learning and Optimization",
            content="Optimization is integral to machine learning, from training models to tuning hyperparameters. Gradient-based methods are prevalent.",
            tags=["machine learning", "optimization", "gradient-based", "hyperparameters"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="23",
            title="Applications of Optimization",
            content="Optimization is applied in engineering, economics, logistics, and data science. It improves efficiency and resource allocation.",
            tags=["applications", "engineering", "economics", "logistics", "data science"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="24",
            title="Optimal Control Theory",
            content="Optimal control theory deals with finding control policies that optimize dynamic systems. Applications include robotics and economics.",
            tags=["optimal control", "dynamic systems", "robotics", "economics"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="25",
            title="Numerical Optimization",
            content="Numerical optimization uses computational methods to solve optimization problems. Techniques include line search, trust region, and quasi-Newton methods.",
            tags=["numerical optimization", "line search", "trust region", "quasi-Newton"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="26",
            title="Multi-level Optimization",
            content="Multi-level optimization involves hierarchical decision-making, where solutions at one level affect constraints at another.",
            tags=["multi-level optimization", "hierarchical", "constraints"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="27",
            title="Optimization in Data Science",
            content="Data science relies on optimization for model fitting, feature selection, and clustering. Algorithms include k-means and support vector machines.",
            tags=["data science", "model fitting", "feature selection", "clustering"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="28",
            title="Optimization in Engineering Design",
            content="Engineering design uses optimization to improve performance, reduce costs, and ensure safety. Methods include structural optimization and reliability analysis.",
            tags=["engineering design", "structural optimization", "reliability analysis"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="29",
            title="Optimization in Economics",
            content="Economics uses optimization to model consumer behavior, market equilibrium, and resource allocation. Utility maximization is a central concept.",
            tags=["economics", "consumer behavior", "market equilibrium", "resource allocation"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="30",
            title="Optimization in Logistics",
            content="Logistics optimization improves supply chain efficiency, routing, and inventory management. Algorithms include vehicle routing and warehouse optimization.",
            tags=["logistics", "supply chain", "routing", "inventory management"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)