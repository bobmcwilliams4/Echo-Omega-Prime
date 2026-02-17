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
    BM25_K1 = 1.5
    BM25_B = 0.75

    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.doc_tags: Dict[str, List[str]] = {}
        self.lock = threading.Lock()
        self.total_docs: int = 0
        self.idf_cache: Dict[str, float] = {}
        self._preseeded = False

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.doc_tags[doc.id] = doc.tags
            self.total_docs += 1
            for token in tokens:
                self.term_freqs[token][doc.id] += 1
            for token in set(tokens):
                self.term_doc_freq[token] += 1
            self._recompute_avg_doc_length()
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        doc_scores: Dict[str, float] = defaultdict(float)
        doc_snippets: Dict[str, str] = {}
        for token in query_tokens:
            idf = self._compute_idf(token)
            for doc_id in self.term_freqs[token]:
                tf = self.term_freqs[token][doc_id]
                score = self._score_bm25(token, doc_id, tf, idf)
                doc_scores[doc_id] += score
        # TF-IDF normalization
        for token in query_tokens:
            idf = self._compute_idf(token)
            for doc_id in self.term_freqs[token]:
                tf = self.term_freqs[token][doc_id]
                norm_tf = tf / self.doc_lengths[doc_id]
                doc_scores[doc_id] += norm_tf * idf * 0.2  # TF-IDF bonus
        # Weight adjustment
        for doc_id in doc_scores:
            doc_scores[doc_id] *= self.documents[doc_id].weight
        # Snippet extraction
        for doc_id in doc_scores:
            doc = self.documents[doc_id]
            snippet = self._extract_snippet(doc.content, query_tokens)
            doc_snippets[doc_id] = snippet
        results = [
            SearchResult(doc_id, doc_scores[doc_id], self.documents[doc_id].title, doc_snippets[doc_id])
            for doc_id in sorted(doc_scores, key=doc_scores.get, reverse=True)
        ]
        return results[:limit]

    def get_stats(self) -> Dict[str, float]:
        return {
            "total_docs": self.total_docs,
            "avg_doc_length": self.avg_doc_length,
            "unique_terms": len(self.term_doc_freq),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

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

    def _score_bm25(self, term: str, doc_id: str, tf: int, idf: float) -> float:
        doc_length = self.doc_lengths[doc_id]
        avg_length = self.avg_doc_length if self.avg_doc_length > 0 else 1
        numerator = tf * (self.BM25_K1 + 1)
        denominator = tf + self.BM25_K1 * (1 - self.BM25_B + self.BM25_B * doc_length / avg_length)
        return idf * numerator / denominator

    def _recompute_avg_doc_length(self):
        if self.total_docs == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs

    def _extract_snippet(self, content: str, query_tokens: List[str]) -> str:
        sentences = re.split(r'(?<=[.!?])\s+', content)
        for sentence in sentences:
            if any(token in sentence.lower() for token in query_tokens):
                return sentence.strip()
        return sentences[0].strip() if sentences else content[:160]

    def _preseed(self):
        if self._preseeded:
            return
        docs = [
            SearchDocument(
                id="graph_def",
                title="Definition of a Graph",
                content="A graph is a mathematical structure consisting of a set of vertices and a set of edges connecting pairs of vertices.",
                tags=["definition", "graph", "vertices", "edges"]
            ),
            SearchDocument(
                id="simple_graph",
                title="Simple Graphs",
                content="A simple graph is an unweighted, undirected graph containing no loops or multiple edges.",
                tags=["simple", "graph", "undirected", "loops", "multiple edges"]
            ),
            SearchDocument(
                id="directed_graph",
                title="Directed Graphs",
                content="A directed graph, or digraph, is a graph in which edges have a direction, going from one vertex to another.",
                tags=["directed", "digraph", "edges", "direction"]
            ),
            SearchDocument(
                id="weighted_graph",
                title="Weighted Graphs",
                content="A weighted graph assigns a numerical value, called weight, to each edge.",
                tags=["weighted", "edges", "weights"]
            ),
            SearchDocument(
                id="adjacency_matrix",
                title="Adjacency Matrix",
                content="The adjacency matrix of a graph is a square matrix used to represent the connections between vertices.",
                tags=["adjacency", "matrix", "representation"]
            ),
            SearchDocument(
                id="adjacency_list",
                title="Adjacency List",
                content="An adjacency list is a collection of lists or arrays used to represent which vertices are adjacent to which.",
                tags=["adjacency", "list", "representation"]
            ),
            SearchDocument(
                id="degree_vertex",
                title="Degree of a Vertex",
                content="The degree of a vertex in a graph is the number of edges incident to it.",
                tags=["degree", "vertex", "edges"]
            ),
            SearchDocument(
                id="path_graph",
                title="Paths in Graphs",
                content="A path in a graph is a sequence of vertices where each adjacent pair is connected by an edge.",
                tags=["path", "sequence", "vertices", "edges"]
            ),
            SearchDocument(
                id="cycle_graph",
                title="Cycles in Graphs",
                content="A cycle is a path that starts and ends at the same vertex without repeating any edges.",
                tags=["cycle", "path", "vertex", "edges"]
            ),
            SearchDocument(
                id="connected_graph",
                title="Connected Graphs",
                content="A graph is connected if there is a path between every pair of vertices.",
                tags=["connected", "path", "vertices"]
            ),
            SearchDocument(
                id="component_graph",
                title="Components of a Graph",
                content="A component is a maximal connected subgraph.",
                tags=["component", "connected", "subgraph"]
            ),
            SearchDocument(
                id="tree_graph",
                title="Trees",
                content="A tree is a connected acyclic graph.",
                tags=["tree", "acyclic", "connected"]
            ),
            SearchDocument(
                id="spanning_tree",
                title="Spanning Trees",
                content="A spanning tree of a graph is a subgraph that is a tree and includes all the vertices.",
                tags=["spanning", "tree", "subgraph", "vertices"]
            ),
            SearchDocument(
                id="bipartite_graph",
                title="Bipartite Graphs",
                content="A bipartite graph is a graph whose vertices can be divided into two disjoint sets such that every edge connects a vertex in one set to a vertex in the other.",
                tags=["bipartite", "sets", "edges"]
            ),
            SearchDocument(
                id="complete_graph",
                title="Complete Graphs",
                content="A complete graph is a graph in which every pair of distinct vertices is connected by a unique edge.",
                tags=["complete", "vertices", "edges"]
            ),
            SearchDocument(
                id="planar_graph",
                title="Planar Graphs",
                content="A planar graph can be drawn on a plane without any edges crossing.",
                tags=["planar", "drawing", "edges"]
            ),
            SearchDocument(
                id="graph_isomorphism",
                title="Graph Isomorphism",
                content="Two graphs are isomorphic if there is a bijection between their vertex sets that preserves adjacency.",
                tags=["isomorphism", "bijection", "adjacency"]
            ),
            SearchDocument(
                id="eulerian_path",
                title="Eulerian Paths and Circuits",
                content="An Eulerian path is a path that uses every edge exactly once. An Eulerian circuit is an Eulerian path that starts and ends at the same vertex.",
                tags=["eulerian", "path", "circuit", "edges"]
            ),
            SearchDocument(
                id="hamiltonian_path",
                title="Hamiltonian Paths and Cycles",
                content="A Hamiltonian path visits every vertex exactly once. A Hamiltonian cycle is a Hamiltonian path that forms a cycle.",
                tags=["hamiltonian", "path", "cycle", "vertex"]
            ),
            SearchDocument(
                id="graph_coloring",
                title="Graph Coloring",
                content="Graph coloring is the assignment of colors to vertices so that no two adjacent vertices share the same color.",
                tags=["coloring", "vertices", "adjacent"]
            ),
            SearchDocument(
                id="chromatic_number",
                title="Chromatic Number",
                content="The chromatic number of a graph is the minimum number of colors needed to color the vertices.",
                tags=["chromatic", "number", "coloring"]
            ),
            SearchDocument(
                id="clique_graph",
                title="Cliques in Graphs",
                content="A clique is a subset of vertices such that every two distinct vertices are adjacent.",
                tags=["clique", "vertices", "adjacent"]
            ),
            SearchDocument(
                id="independent_set",
                title="Independent Sets",
                content="An independent set is a set of vertices no two of which are adjacent.",
                tags=["independent", "vertices", "adjacent"]
            ),
            SearchDocument(
                id="matching_graph",
                title="Matching in Graphs",
                content="A matching is a set of edges without common vertices.",
                tags=["matching", "edges", "vertices"]
            ),
            SearchDocument(
                id="vertex_cover",
                title="Vertex Cover",
                content="A vertex cover is a set of vertices such that every edge has at least one endpoint in the set.",
                tags=["vertex", "cover", "edges"]
            ),
            SearchDocument(
                id="edge_cover",
                title="Edge Cover",
                content="An edge cover is a set of edges such that every vertex is incident to at least one edge in the set.",
                tags=["edge", "cover", "vertex"]
            ),
            SearchDocument(
                id="network_flow",
                title="Network Flow",
                content="Network flow is the study of flows through a network, often represented as a directed graph with capacities.",
                tags=["network", "flow", "directed", "capacities"]
            ),
            SearchDocument(
                id="graph_algorithms",
                title="Graph Algorithms",
                content="Graph algorithms include breadth-first search, depth-first search, Dijkstra's algorithm, and Kruskal's algorithm.",
                tags=["algorithm", "breadth-first", "depth-first", "dijkstra", "kruskal"]
            ),
            SearchDocument(
                id="subgraph",
                title="Subgraphs",
                content="A subgraph is a graph formed from a subset of the vertices and edges of a larger graph.",
                tags=["subgraph", "vertices", "edges"]
            ),
            SearchDocument(
                id="graph_representation",
                title="Graph Representation",
                content="Graphs can be represented using adjacency matrices, adjacency lists, or incidence matrices.",
                tags=["representation", "adjacency", "incidence", "matrix", "list"]
            ),
            SearchDocument(
                id="incidence_matrix",
                title="Incidence Matrix",
                content="The incidence matrix of a graph is a matrix that shows the relationship between vertices and edges.",
                tags=["incidence", "matrix", "vertices", "edges"]
            ),
            SearchDocument(
                id="graph_traversal",
                title="Graph Traversal",
                content="Graph traversal refers to visiting all the vertices in a graph, commonly using BFS or DFS.",
                tags=["traversal", "bfs", "dfs", "vertices"]
            ),
            SearchDocument(
                id="cut_vertex",
                title="Cut Vertices and Bridges",
                content="A cut vertex is a vertex whose removal increases the number of connected components. A bridge is an edge whose removal increases the number of components.",
                tags=["cut", "vertex", "bridge", "components"]
            ),
            SearchDocument(
                id="graph_theory_applications",
                title="Applications of Graph Theory",
                content="Graph theory is used in computer science, biology, social networks, transportation, and many other fields.",
                tags=["applications", "computer science", "biology", "social networks", "transportation"]
            ),
        ]
        for doc in docs:
            self.add_document(doc)
        self._preseeded = True

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _search_index_instance._preseed()
    return _search_index_instance