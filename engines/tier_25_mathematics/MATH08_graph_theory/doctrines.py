from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: float
    confidence_zone: str
    controlling_precedent: str

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Euler's Formula for Planar Graphs",
        keywords=["planar graph", "Euler's formula", "vertices", "edges", "faces"],
        conclusion_template="For any connected planar graph, the relationship V - E + F = 2 holds.",
        reasoning_framework=(
            "Euler's formula is a foundational result in planar graph theory. It states that for any finite, connected, planar graph drawn without edge crossings, "
            "the number of vertices (V), edges (E), and faces (F) (including the exterior region) satisfy V - E + F = 2. "
            "The proof proceeds by induction on the number of edges, considering the removal of edges not part of a spanning tree, "
            "and using the fact that each removal reduces the number of faces by one while keeping the graph connected. "
            "This formula is crucial for deriving other results, such as bounds on the number of edges in planar graphs and for proving non-planarity of certain graphs."
        ),
        key_factors=["Connectedness", "Planarity", "Finite graph"],
        primary_authority=["Leonhard Euler", "Diestel, Graph Theory (5th ed.), Theorem 4.2.1"],
        burden_holder="Proponent of planarity",
        adversary_position="Graph is not planar or not connected",
        counter_arguments=[
            "Graph contains edge crossings that cannot be removed by redrawing.",
            "Graph is disconnected, in which case the formula generalizes to V - E + F = 1 + c (c = number of components)."
        ],
        resolution_strategy="Verify planarity and connectedness; apply induction on the number of edges.",
        entity_scope="Finite, connected, planar graphs",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Euler (1752); Diestel, Theorem 4.2.1"
    ),
    DoctrineBlock(
        topic="Kuratowski's Theorem",
        keywords=["planar graph", "Kuratowski's theorem", "subdivision", "K5", "K3,3"],
        conclusion_template="A finite graph is planar if and only if it contains no subgraph that is a subdivision of K5 or K3,3.",
        reasoning_framework=(
            "Kuratowski's theorem provides a necessary and sufficient condition for planarity. "
            "It asserts that a finite graph is planar if and only if it does not contain a subgraph that is a subdivision of the complete graph on five vertices (K5) or the complete bipartite graph K3,3. "
            "The proof involves showing that these two graphs are the minimal non-planar graphs, and any non-planar graph must contain a subdivision of one of them. "
            "The theorem is fundamental for planarity testing and for understanding the structure of non-planar graphs."
        ),
        key_factors=["Subdivisions", "Presence of K5 or K3,3", "Finite graph"],
        primary_authority=["Kazimierz Kuratowski", "Diestel, Graph Theory (5th ed.), Theorem 4.4.1"],
        burden_holder="Challenger of planarity",
        adversary_position="Graph is planar or does not contain such subdivisions",
        counter_arguments=[
            "Graph does not contain a subdivision of K5 or K3,3.",
            "Graph is planar by construction or embedding."
        ],
        resolution_strategy="Search for subdivisions of K5 or K3,3 in the graph.",
        entity_scope="Finite graphs",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Kuratowski (1930); Diestel, Theorem 4.4.1"
    ),
    DoctrineBlock(
        topic="Wagner's Theorem",
        keywords=["planar graph", "Wagner's theorem", "minor", "K5", "K3,3"],
        conclusion_template="A finite graph is planar if and only if it contains neither K5 nor K3,3 as a minor.",
        reasoning_framework=(
            "Wagner's theorem characterizes planar graphs in terms of graph minors. "
            "A graph minor is obtained by deleting edges or vertices and by contracting edges. "
            "The theorem states that a finite graph is planar if and only if it does not have K5 or K3,3 as a minor. "
            "This result is closely related to Kuratowski's theorem but uses the minor relation instead of subdivisions."
        ),
        key_factors=["Graph minors", "Edge contraction", "Presence of K5 or K3,3"],
        primary_authority=["Klaus Wagner", "Diestel, Graph Theory (5th ed.), Theorem 4.4.6"],
        burden_holder="Challenger of planarity",
        adversary_position="Graph is planar or does not contain such minors",
        counter_arguments=[
            "Graph does not contain K5 or K3,3 as a minor.",
            "Graph is planar by construction."
        ],
        resolution_strategy="Test for the existence of K5 or K3,3 minors.",
        entity_scope="Finite graphs",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Wagner (1937); Diestel, Theorem 4.4.6"
    ),
    DoctrineBlock(
        topic="Handshaking Lemma",
        keywords=["degree", "vertex", "edge", "handshaking lemma"],
        conclusion_template="In any undirected graph, the sum of the degrees of all vertices equals twice the number of edges.",
        reasoning_framework=(
            "The handshaking lemma is a basic result in graph theory. "
            "It follows from the fact that each edge contributes exactly two to the sum of degrees (one for each endpoint). "
            "Formally, sum_{v in V} deg(v) = 2|E|. "
            "This lemma is used to prove properties about degrees, such as the number of vertices of odd degree being even."
        ),
        key_factors=["Undirected graph", "Vertex degrees", "Edge count"],
        primary_authority=["Paul Erdős", "Diestel, Graph Theory (5th ed.), Lemma 1.1.1"],
        burden_holder="Proponent of degree property",
        adversary_position="Graph is directed or has loops/multiedges",
        counter_arguments=[
            "Graph is directed (then in-degree and out-degree must be considered).",
            "Graph has loops (each loop counts twice)."
        ],
        resolution_strategy="Verify undirectedness and proper counting of loops.",
        entity_scope="Undirected graphs",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Diestel, Lemma 1.1.1"
    ),
    DoctrineBlock(
        topic="Dirac's Theorem",
        keywords=["Hamiltonian cycle", "Dirac's theorem", "minimum degree"],
        conclusion_template="If a simple graph with n ≥ 3 vertices has minimum degree at least n/2, then it contains a Hamiltonian cycle.",
        reasoning_framework=(
            "Dirac's theorem gives a sufficient condition for the existence of a Hamiltonian cycle. "
            "If every vertex in a simple graph of n ≥ 3 vertices has degree at least n/2, then the graph is Hamiltonian. "
            "The proof uses the concept of extending paths and the pigeonhole principle to show that the cycle must exist."
        ),
        key_factors=["Simple graph", "Minimum degree", "Number of vertices"],
        primary_authority=["Gabriel Dirac", "Diestel, Graph Theory (5th ed.), Theorem 7.1.1"],
        burden_holder="Proponent of Hamiltonicity",
        adversary_position="Graph does not meet the degree condition or is not simple",
        counter_arguments=[
            "Graph has a vertex with degree less than n/2.",
            "Graph has loops or multiple edges."
        ],
        resolution_strategy="Check minimum degree and simplicity.",
        entity_scope="Simple graphs with n ≥ 3",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Dirac (1952); Diestel, Theorem 7.1.1"
    ),
    DoctrineBlock(
        topic="Ore's Theorem",
        keywords=["Hamiltonian cycle", "Ore's theorem", "degree sum"],
        conclusion_template="If a simple graph with n ≥ 3 vertices satisfies deg(u) + deg(v) ≥ n for every pair of non-adjacent vertices u, v, then it contains a Hamiltonian cycle.",
        reasoning_framework=(
            "Ore's theorem generalizes Dirac's theorem by considering the degree sum of non-adjacent vertices. "
            "If for every pair of non-adjacent vertices u and v in a simple graph of n ≥ 3 vertices, deg(u) + deg(v) ≥ n, then the graph is Hamiltonian. "
            "The proof uses the concept of closure and extending paths to cycles."
        ),
        key_factors=["Simple graph", "Degree sum condition", "Non-adjacent vertices"],
        primary_authority=["Øystein Ore", "Diestel, Graph Theory (5th ed.), Theorem 7.1.2"],
        burden_holder="Proponent of Hamiltonicity",
        adversary_position="Graph does not meet the degree sum condition",
        counter_arguments=[
            "There exists a pair of non-adjacent vertices with degree sum less than n.",
            "Graph is not simple."
        ],
        resolution_strategy="Check degree sum for all non-adjacent pairs.",
        entity_scope="Simple graphs with n ≥ 3",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Ore (1960); Diestel, Theorem 7.1.2"
    ),
    DoctrineBlock(
        topic="Brooks' Theorem",
        keywords=["chromatic number", "Brooks' theorem", "maximum degree"],
        conclusion_template="In a connected undirected graph, the chromatic number is at most the maximum degree, unless the graph is complete or an odd cycle.",
        reasoning_framework=(
            "Brooks' theorem bounds the chromatic number of a connected undirected graph. "
            "If G is a connected undirected graph with maximum degree Δ, then the chromatic number χ(G) ≤ Δ, unless G is a complete graph or an odd cycle, in which case χ(G) = Δ + 1. "
            "The proof uses induction and coloring strategies, considering the structure of the graph."
        ),
        key_factors=["Connectedness", "Maximum degree", "Graph type"],
        primary_authority=["R.L. Brooks", "Diestel, Graph Theory (5th ed.), Theorem 5.2.2"],
        burden_holder="Proponent of chromatic bound",
        adversary_position="Graph is complete or an odd cycle",
        counter_arguments=[
            "Graph is complete (chromatic number is n).",
            "Graph is an odd cycle (chromatic number is 3)."
        ],
        resolution_strategy="Check for completeness or odd cycles before applying the bound.",
        entity_scope="Connected undirected graphs",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Brooks (1941); Diestel, Theorem 5.2.2"
    ),
    DoctrineBlock(
        topic="Four Color Theorem",
        keywords=["planar graph", "four color theorem", "vertex coloring"],
        conclusion_template="Every planar graph can be colored with at most four colors so that no two adjacent vertices share the same color.",
        reasoning_framework=(
            "The four color theorem is a landmark result in graph theory. "
            "It asserts that any planar graph can be properly colored with at most four colors. "
            "The proof is highly complex and was the first major theorem proved using computer assistance. "
            "It involves reducibility and discharging methods to show that no minimal counterexample exists."
        ),
        key_factors=["Planarity", "Proper coloring", "Number of colors"],
        primary_authority=["Appel & Haken", "Diestel, Graph Theory (5th ed.), Theorem 5.3.1"],
        burden_holder="Proponent of four-colorability",
        adversary_position="Graph is not planar or coloring requires more than four colors",
        counter_arguments=[
            "Graph is not planar.",
            "Graph requires more than four colors (contradicts the theorem)."
        ],
        resolution_strategy="Verify planarity and attempt four-coloring.",
        entity_scope="Planar graphs",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Appel & Haken (1976); Diestel, Theorem 5.3.1"
    ),
    DoctrineBlock(
        topic="Five Color Theorem",
        keywords=["planar graph", "five color theorem", "vertex coloring"],
        conclusion_template="Every planar graph can be colored with at most five colors.",
        reasoning_framework=(
            "The five color theorem is a precursor to the four color theorem and is proved by induction. "
            "It shows that any planar graph can be properly colored with at most five colors. "
            "The proof uses Kempe chains and the fact that planar graphs have a vertex of degree at most five."
        ),
        key_factors=["Planarity", "Proper coloring", "Number of colors"],
        primary_authority=["Heawood", "Diestel, Graph Theory (5th ed.), Theorem 5.3.2"],
        burden_holder="Proponent of five-colorability",
        adversary_position="Graph is not planar or coloring requires more than five colors",
        counter_arguments=[
            "Graph is not planar.",
            "Graph requires more than five colors (contradicts the theorem)."
        ],
        resolution_strategy="Verify planarity and attempt five-coloring.",
        entity_scope="Planar graphs",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Heawood (1890); Diestel, Theorem 5.3.2"
    ),
    DoctrineBlock(
        topic="Menger's Theorem",
        keywords=["connectivity", "Menger's theorem", "vertex cut", "path"],
        conclusion_template="The minimum number of vertices separating two non-adjacent vertices equals the maximum number of internally disjoint paths between them.",
        reasoning_framework=(
            "Menger's theorem is a central result in connectivity. "
            "For any two non-adjacent vertices u and v in a finite undirected graph, the size of the smallest set of vertices whose removal separates u and v equals the maximum number of pairwise internally disjoint u-v paths. "
            "The proof uses augmenting paths and the max-flow min-cut theorem."
        ),
        key_factors=["Vertex cuts", "Internally disjoint paths", "Non-adjacent vertices"],
        primary_authority=["Karl Menger", "Diestel, Graph Theory (5th ed.), Theorem 3.3.1"],
        burden_holder="Proponent of connectivity equivalence",
        adversary_position="Graph is directed or infinite, or vertices are adjacent",
        counter_arguments=[
            "Graph is directed (use directed version).",
            "Vertices are adjacent (the minimum cut is 1)."
        ],
        resolution_strategy="Apply theorem to undirected, finite graphs with non-adjacent vertices.",
        entity_scope="Finite undirected graphs",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Menger (1927); Diestel, Theorem 3.3.1"
    ),
    DoctrineBlock(
        topic="Hall's Marriage Theorem",
        keywords=["bipartite graph", "matching", "Hall's theorem"],
        conclusion_template="A bipartite graph has a matching that covers every vertex in one part if and only if Hall's condition holds.",
        reasoning_framework=(
            "Hall's marriage theorem gives a necessary and sufficient condition for the existence of a perfect matching in bipartite graphs. "
            "For bipartite graph G = (A ∪ B, E), there is a matching covering every vertex in A if and only if for every subset S of A, the neighborhood N(S) has size at least |S|. "
            "The proof uses induction and augmenting paths."
        ),
        key_factors=["Bipartite structure", "Neighborhood size", "Matching"],
        primary_authority=["Philip Hall", "Diestel, Graph Theory (5th ed.), Theorem 2.1.1"],
        burden_holder="Proponent of matching existence",
        adversary_position="Hall's condition fails for some subset",
        counter_arguments=[
            "There exists S ⊆ A with |N(S)| < |S|.",
            "Graph is not bipartite."
        ],
        resolution_strategy="Check Hall's condition for all subsets of A.",
        entity_scope="Bipartite graphs",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Hall (1935); Diestel, Theorem 2.1.1"
    ),
    DoctrineBlock(
        topic="Tutte's Theorem",
        keywords=["matching", "Tutte's theorem", "perfect matching"],
        conclusion_template="A finite graph has a perfect matching if and only if for every subset S of vertices, the number of odd components in G−S is at most |S|.",
        reasoning_framework=(
            "Tutte's theorem characterizes the existence of perfect matchings in general graphs. "
            "A graph G has a perfect matching if and only if for every subset S of vertices, the number of odd components in G−S is at most |S|. "
            "The proof uses parity arguments and matching theory."
        ),
        key_factors=["Odd components", "Vertex subsets", "Perfect matching"],
        primary_authority=["W.T. Tutte", "Diestel, Graph Theory (5th ed.), Theorem 2.2.1"],
        burden_holder="Proponent of perfect matching",
        adversary_position="Tutte's condition fails for some subset",
        counter_arguments=[
            "There exists S ⊆ V(G) with more than |S| odd components in G−S.",
            "Graph is infinite."
        ],
        resolution_strategy="Check Tutte's condition for all subsets.",
        entity_scope="Finite graphs",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Tutte (1947); Diestel, Theorem 2.2.1"
    ),
    DoctrineBlock(
        topic="Konig's Theorem",
        keywords=["bipartite graph", "matching", "vertex cover", "Konig's theorem"],
        conclusion_template="In bipartite graphs, the size of the maximum matching equals the size of the minimum vertex cover.",
        reasoning_framework=(
            "Konig's theorem establishes an important duality in bipartite graphs. "
            "It states that in any bipartite graph, the maximum size of a matching equals the minimum size of a vertex cover. "
            "The proof uses the max-flow min-cut theorem and properties of bipartite graphs."
        ),
        key_factors=["Bipartite structure", "Matching", "Vertex cover"],
        primary_authority=["Dénes Kőnig", "Diestel, Graph Theory (5th ed.), Theorem 2.1.2"],
        burden_holder="Proponent of equality",
        adversary_position="Graph is not bipartite or cover is not minimal",
        counter_arguments=[
            "Graph is not bipartite.",
            "Matching or cover is not maximal/minimal."
        ],
        resolution_strategy="Verify bipartiteness and optimality of matching and cover.",
        entity_scope="Bipartite graphs",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Kőnig (1931); Diestel, Theorem 2.1.2"
    ),
    DoctrineBlock(
        topic="Petersen's Theorem",
        keywords=["cubic graph", "perfect matching", "Petersen's theorem"],
        conclusion_template="Every bridgeless cubic graph has a perfect matching.",
        reasoning_framework=(
            "Petersen's theorem asserts that every bridgeless cubic (3-regular) graph has a perfect matching. "
            "The proof uses parity arguments, the structure of cubic graphs, and the concept of alternating cycles."
        ),
        key_factors=["Cubic graph", "Bridgelessness", "Perfect matching"],
        primary_authority=["Julius Petersen", "Diestel, Graph Theory (5th ed.), Theorem 2.3.1"],
        burden_holder="Proponent of perfect matching",
        adversary_position="Graph has a bridge or is not cubic",
        counter_arguments=[
            "Graph has a bridge (an edge whose removal increases the number of components).",
            "Graph is not 3-regular."
        ],
        resolution_strategy="Check for bridges and regularity.",
        entity_scope="Finite cubic graphs",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Petersen (1891); Diestel, Theorem 2.3.1"
    ),
    DoctrineBlock(
        topic="Vizing's Theorem",
        keywords=["edge coloring", "chromatic index", "Vizing's theorem"],
        conclusion_template="The chromatic index of a simple graph is either its maximum degree or maximum degree plus one.",
        reasoning_framework=(
            "Vizing's theorem classifies simple graphs into two types based on their chromatic index (the minimum number of colors needed to color edges so that no two adjacent edges share a color). "
            "For any simple graph, the chromatic index is either Δ or Δ+1, where Δ is the maximum degree. "
            "The proof uses induction and edge coloring algorithms."
        ),
        key_factors=["Simple graph", "Maximum degree", "Edge coloring"],
        primary_authority=["Vadim Vizing", "Diestel, Graph Theory (5th ed.), Theorem 5.3.3"],
        burden_holder="Proponent of chromatic index bound",
        adversary_position="Graph is not simple or coloring requires more colors",
        counter_arguments=[
            "Graph has loops or multiple edges.",
            "Edge coloring requires more than Δ+1 colors (contradicts the theorem)."
        ],
        resolution_strategy="Verify simplicity and attempt edge coloring.",
        entity_scope="Simple graphs",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Vizing (1964); Diestel, Theorem 5.3.3"
    ),
    DoctrineBlock(
        topic="Ramsey's Theorem",
        keywords=["Ramsey theory", "complete graph", "coloring", "Ramsey number"],
        conclusion_template="For any positive integers k and l, there exists a minimal n such that any red-blue coloring of the edges of K_n contains a red K_k or a blue K_l.",
        reasoning_framework=(
            "Ramsey's theorem is a cornerstone of extremal combinatorics. "
            "It states that for any integers k and l, there exists a minimal Ramsey number R(k, l) such that any red-blue coloring of the edges of the complete graph K_n (n ≥ R(k, l)) contains a monochromatic K_k in red or K_l in blue. "
            "The proof uses induction and the pigeonhole principle."
        ),
        key_factors=["Complete graph", "Edge coloring", "Ramsey number"],
        primary_authority=["Frank P. Ramsey", "Diestel, Graph Theory (5th ed.), Theorem 10.1.1"],
        burden_holder="Proponent of Ramsey property",
        adversary_position="n < R(k, l) or coloring avoids monochromatic cliques",
        counter_arguments=[
            "n is too small for the given k and l.",
            "Coloring avoids monochromatic cliques (contradicts the theorem for n ≥ R(k, l))."
        ],
        resolution_strategy="Determine R(k, l) and check coloring.",
        entity_scope="Complete graphs",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Ramsey (1930); Diestel, Theorem 10.1.1"
    ),
    DoctrineBlock(
        topic="Turán's Theorem",
        keywords=["extremal graph theory", "Turán's theorem", "clique", "edge bound"],
        conclusion_template="A graph with n vertices and more than T_{n, r} edges contains a (r+1)-clique.",
        reasoning_framework=(
            "Turán's theorem gives the maximum number of edges a graph with n vertices can have without containing a clique of size r+1. "
            "The extremal graph is the Turán graph, a complete r-partite graph with parts as equal as possible. "
            "The proof uses induction and combinatorial arguments."
        ),
        key_factors=["Number of vertices", "Edge count", "Clique size"],
        primary_authority=["Pál Turán", "Diestel, Graph Theory (5th ed.), Theorem 10.2.1"],
        burden_holder="Proponent of clique existence",
        adversary_position="Edge count is at or below Turán's bound",
        counter_arguments=[
            "Graph has at most T_{n, r} edges.",
            "No (r+1)-clique exists (contradicts the theorem if edge count is exceeded)."
        ],
        resolution_strategy="Compare edge count to Turán's bound.",
        entity_scope="Finite graphs",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Turán (1941); Diestel, Theorem 10.2.1"
    ),
    DoctrineBlock(
        topic="Cayley's Formula",
        keywords=["spanning tree", "Cayley's formula", "labeled graph"],
        conclusion_template="The number of spanning trees in the complete graph K_n is n^{n-2}.",
        reasoning_framework=(
            "Cayley's formula counts the number of labeled trees on n vertices. "
            "The proof uses Prüfer sequences, which establish a bijection between labeled trees and sequences of length n-2 with entries from 1 to n."
        ),
        key_factors=["Labeled vertices", "Spanning trees", "Complete graph"],
        primary_authority=["Arthur Cayley", "Diestel, Graph Theory (5th ed.), Theorem 6.1.1"],
        burden_holder="Proponent of spanning tree count",
        adversary_position="Graph is not complete or unlabeled",
        counter_arguments=[
            "Graph is not complete.",
            "Vertices are not labeled."
        ],
        resolution_strategy="Apply formula only to labeled complete graphs.",
        entity_scope="Labeled complete graphs",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Cayley (1889); Diestel, Theorem 6.1.1"
    ),
    DoctrineBlock(
        topic="Matrix-Tree Theorem",
        keywords=["spanning tree", "matrix-tree theorem", "Laplacian matrix"],
        conclusion_template="The number of spanning trees in a graph equals any cofactor of its Laplacian matrix.",
        reasoning_framework=(
            "The matrix-tree theorem provides an algebraic method to count spanning trees. "
            "For a graph G, construct its Laplacian matrix L. The number of spanning trees is equal to any cofactor of L (i.e., the determinant of L with any row and column removed). "
            "The proof uses linear algebra and properties of determinants."
        ),
        key_factors=["Laplacian matrix", "Spanning trees", "Cofactor"],
        primary_authority=["Kirchhoff", "Diestel, Graph Theory (5th ed.), Theorem 6.2.1"],
        burden_holder="Proponent of spanning tree count",
        adversary_position="Graph is not simple or Laplacian is ill-defined",
        counter_arguments=[
            "Graph has loops or multiple edges.",
            "Laplacian matrix is not properly constructed."
        ],
        resolution_strategy="Verify simplicity and correct Laplacian construction.",
        entity_scope="Simple graphs",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Kirchhoff (1847); Diestel, Theorem 6.2.1"
    ),
    DoctrineBlock(
        topic="Erdős–Gallai Theorem",
        keywords=["degree sequence", "Erdős–Gallai theorem", "graph realization"],
        conclusion_template="A sequence of non-negative integers is a degree sequence of a simple graph if and only if it satisfies the Erdős–Gallai inequalities.",
        reasoning_framework=(
            "The Erdős–Gallai theorem gives necessary and sufficient conditions for a sequence to be graphical (i.e., realizable as the degree sequence of a simple graph). "
            "The sequence must have even sum and satisfy the Erdős–Gallai inequalities for all k = 1, ..., n."
        ),
        key_factors=["Degree sequence", "Even sum", "Inequalities"],
        primary_authority=["Erdős & Gallai", "Diestel, Graph Theory (5th ed.), Theorem 1.3.1"],
        burden_holder="Proponent of graphicality",
        adversary_position="Sequence fails the inequalities or sum is odd",
        counter_arguments=[
            "Degree sum is odd.",
            "Inequalities fail for some k."
        ],
        resolution_strategy="Check sum and all inequalities.",
        entity_scope="Simple graphs",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Erdős & Gallai (1960); Diestel, Theorem 1.3.1"
    ),
    DoctrineBlock(
        topic="Havel–Hakimi Algorithm",
        keywords=["degree sequence", "Havel–Hakimi", "graph realization"],
        conclusion_template="A sequence is graphical if and only if the Havel–Hakimi process reduces it to all zeros.",
        reasoning_framework=(
            "The Havel–Hakimi algorithm is a constructive method to determine if a degree sequence is graphical. "
            "Repeatedly remove the largest degree d, subtract 1 from the next d largest degrees, and repeat. "
            "If the process ends with all zeros, the sequence is graphical."
        ),
        key_factors=["Degree sequence", "Reduction process", "Non-negativity"],
        primary_authority=["Havel (1955)", "Hakimi (1962)", "Diestel, Graph Theory (5th ed.), Exercise 1.3.2"],
        burden_holder="Proponent of graphicality",
        adversary_position="Negative degrees arise during process",
        counter_arguments=[
            "Negative degree appears during reduction.",
            "Sequence does not reduce to all zeros."
        ],
        resolution_strategy="Apply the Havel–Hakimi process stepwise.",
        entity_scope="Simple graphs",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Havel (1955); Hakimi (1962)"
    ),
    DoctrineBlock(
        topic="Whitney's Theorem on 2-Connected Graphs",
        keywords=["2-connected", "Whitney's theorem", "cycle"],
        conclusion_template="A graph is 2-connected if and only if any two vertices lie on a common cycle.",
        reasoning_framework=(
            "Whitney's theorem characterizes 2-connected graphs. "
            "A graph is 2-connected if and only if for any pair of vertices, there is a cycle containing both. "
            "The proof uses ear decomposition and properties of cycles."
        ),
        key_factors=["2-connectivity", "Cycles", "Vertex pairs"],
        primary_authority=["Hassler Whitney", "Diestel, Graph Theory (5th ed.), Theorem 3.2.2"],
        burden_holder="Proponent of 2-connectivity",
        adversary_position="Graph is not 2-connected or pair is not on a cycle",
        counter_arguments=[
            "Graph is not 2-connected.",
            "No cycle contains both vertices."
        ],
        resolution_strategy="Check all pairs for common cycles.",
        entity_scope="Finite graphs",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Whitney (1932); Diestel, Theorem 3.2.2"
    ),
    DoctrineBlock(
        topic="Fleury's Algorithm",
        keywords=["Eulerian trail", "Fleury's algorithm", "traversal"],
        conclusion_template="Fleury's algorithm finds an Eulerian trail in a graph if one exists.",
        reasoning_framework=(
            "Fleury's algorithm is a method for finding an Eulerian trail in a graph. "
            "At each step, traverse an edge that is not a bridge unless no alternative exists. "
            "The algorithm terminates with an Eulerian trail if the graph is Eulerian."
        ),
        key_factors=["Eulerian property", "Edge selection", "Bridges"],
        primary_authority=["Fleury (1883)", "Diestel, Graph Theory (5th ed.), Exercise 1.6.2"],
        burden_holder="Proponent of existence of Eulerian trail",
        adversary_position="Graph is not Eulerian or algorithm fails",
        counter_arguments=[
            "Graph does not have all vertices of even degree (or exactly two of odd degree for trail).",
            "Algorithm cannot proceed without breaking Eulerian property."
        ],
        resolution_strategy="Verify Eulerian conditions before applying algorithm.",
        entity_scope="Finite graphs",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Fleury (1883)"
    ),
    DoctrineBlock(
        topic="Chinese Postman Problem",
        keywords=["Eulerian circuit", "Chinese postman", "edge duplication"],
        conclusion_template="The minimum closed walk covering all edges can be found by duplicating edges to make the graph Eulerian.",
        reasoning_framework=(
            "The Chinese Postman Problem seeks the shortest closed walk covering every edge at least once. "
            "The solution involves finding all vertices of odd degree and duplicating the minimum weight set of edges to make all degrees even, thus creating an Eulerian circuit. "
            "The proof uses matching and Eulerian circuit properties."
        ),
        key_factors=["Odd degree vertices", "Edge duplication", "Eulerian circuit"],
        primary_authority=["Kwan Mei-Ko (1962)", "Diestel, Graph Theory (5th ed.), Section 1.6"],
        burden_holder="Proponent of minimal walk",
        adversary_position="Graph is disconnected or duplication is not minimal",
        counter_arguments=[
            "Graph is disconnected.",
            "Edge duplication is not optimal."
        ],
        resolution_strategy="Find minimal matching among odd degree vertices.",
        entity_scope="Finite graphs",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Kwan Mei-Ko (1962)"
    ),
    DoctrineBlock(
        topic="Eulerian Circuit Characterization",
        keywords=["Eulerian circuit", "degree", "connectedness"],
        conclusion_template="A connected graph has an Eulerian circuit if and only if every vertex has even degree.",
        reasoning_framework=(
            "A classical result in graph theory: a connected graph has an Eulerian circuit if and only if all vertices have even degree. "
            "The proof uses induction and the structure of circuits."
        ),
        key_factors=["Connectedness", "Even degree vertices"],
        primary_authority=["Euler (1736)", "Diestel, Graph Theory (5th ed.), Theorem 1.6.1"],
        burden_holder="Proponent of Eulerian circuit",
        adversary_position="Graph is disconnected or has vertices of odd degree",
        counter_arguments=[
            "Graph is disconnected.",
            "Some vertex has odd degree."
        ],
        resolution_strategy="Check connectedness and degrees.",
        entity_scope="Finite graphs",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Euler (1736); Diestel, Theorem 1.6.1"
    ),
    DoctrineBlock(
        topic="Bipartite Graph Characterization",
        keywords=["bipartite graph", "odd cycle", "characterization"],
        conclusion_template="A graph is bipartite if and only if it contains no odd cycles.",
        reasoning_framework=(
            "A graph is bipartite if its vertices can be colored with two colors such that no edge connects vertices of the same color. "
            "The proof shows that the presence of an odd cycle prevents such a coloring, and the absence guarantees it."
        ),
        key_factors=["Odd cycles", "2-coloring", "Graph structure"],
        primary_authority=["Kőnig (1916)", "Diestel, Graph Theory (5th ed.), Theorem 1.2.2"],
        burden_holder="Proponent of bipartiteness",
        adversary_position="Graph contains an odd cycle",
        counter_arguments=[
            "Graph contains an odd cycle.",
            "2-coloring is not possible."
        ],
        resolution_strategy="Search for odd cycles or attempt 2-coloring.",
        entity_scope="Finite graphs",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Kőnig (1916); Diestel, Theorem 1.2.2"
    ),
    DoctrineBlock(
        topic="Planarity of K5 and K3,3",
        keywords=["planarity", "K5", "K3,3", "non-planar"],
        conclusion_template="The complete graph K5 and the complete bipartite graph K3,3 are not planar.",
        reasoning_framework=(
            "K5 and K3,3 are the basic non-planar graphs. "
            "Their non-planarity can be shown using Euler's formula and by attempting to embed them in the plane without edge crossings."
        ),
        key_factors=["Graph structure", "Edge crossings", "Planarity"],
        primary_authority=["Kuratowski (1930)", "Diestel, Graph Theory (5th ed.), Section 4.4"],
        burden_holder="Proponent of non-planarity",
        adversary_position="Graph can be embedded in the plane",
        counter_arguments=[
            "Graph is not K5 or K3,3.",
            "A planar embedding exists (contradicts the theorem)."
        ],
        resolution_strategy="Apply Euler's formula and attempt embedding.",
        entity_scope="K5 and K3,3",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Kuratowski (1930); Diestel, Section 4.4"
    ),
    DoctrineBlock(
        topic="Tree Characterization",
        keywords=["tree", "acyclic", "connected", "n-1 edges"],
        conclusion_template="A graph is a tree if and only if it is connected and acyclic, or equivalently, has n-1 edges.",
        reasoning_framework=(
            "A tree is a connected acyclic graph. "
            "It can also be characterized as a connected graph with n-1 edges, or as an acyclic graph with n-1 edges. "
            "Proofs use induction and properties of cycles."
        ),
        key_factors=["Connectedness", "Acyclicity", "Number of edges"],
        primary_authority=["Cayley (1889)", "Diestel, Graph Theory (5th ed.), Theorem 1.5.1"],
        burden_holder="Proponent of tree structure",
        adversary_position="Graph is not connected or contains cycles",
        counter_arguments=[
            "Graph is disconnected.",
            "Graph contains a cycle.",
            "Graph does not have n-1 edges."
        ],
        resolution_strategy="Check all three characterizations.",
        entity_scope="Finite graphs",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Cayley (1889); Diestel, Theorem 1.5.1"
    ),
    DoctrineBlock(
        topic="Bridges and Cut Vertices",
        keywords=["bridge", "cut vertex", "connectivity"],
        conclusion_template="A bridge is an edge whose removal increases the number of components; a cut vertex is a vertex whose removal increases the number of components.",
        reasoning_framework=(
            "Bridges and cut vertices are fundamental to the study of connectivity. "
            "Their identification is crucial for understanding the vulnerability of networks. "
            "Proofs use depth-first search and component analysis."
        ),
        key_factors=["Edge removal", "Vertex removal", "Component count"],
        primary_authority=["Whitney (1932)", "Diestel, Graph Theory (5th ed.), Section 3.1"],
        burden_holder="Proponent of bridge or cut vertex identification",
        adversary_position="Removal does not increase components",
        counter_arguments=[
            "Edge or vertex removal does not disconnect the graph.",
            "Graph is already disconnected."
        ],
        resolution_strategy="Remove edge or vertex and count components.",
        entity_scope="Finite graphs",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Whitney (1932); Diestel, Section 3.1"
    ),
    DoctrineBlock(
        topic="Line Graphs and Their Characterization",
        keywords=["line graph", "characterization", "Beineke's theorem"],
        conclusion_template="A graph is a line graph if and only if it contains none of the nine forbidden induced subgraphs (Beineke's theorem).",
        reasoning_framework=(
            "Line graphs are constructed from the edges of a graph. "
            "Beineke's theorem gives a forbidden subgraph characterization: a graph is a line graph if and only if it contains none of nine specific induced subgraphs. "
            "Proofs use structural analysis and forbidden configurations."
        ),
        key_factors=["Induced subgraphs", "Line graph construction", "Forbidden subgraphs"],
        primary_authority=["Beineke (1970)", "Diestel, Graph Theory (5th ed.), Theorem 8.2.1"],
        burden_holder="Proponent of line graph structure",
        adversary_position="Graph contains a forbidden subgraph",
        counter_arguments=[
            "Graph contains one of the nine forbidden subgraphs.",
            "Graph is not a line graph."
        ],
        resolution_strategy="Search for forbidden subgraphs.",
        entity_scope="Finite graphs",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Beineke (1970); Diestel, Theorem 8.2.1"
    ),
    DoctrineBlock(
        topic="Graph Minor Theorem",
        keywords=["graph minor", "Robertson–Seymour theorem", "well-quasi-ordering"],
        conclusion_template="Graphs are well-quasi-ordered by the minor relation (Robertson–Seymour theorem).",
        reasoning_framework=(
            "The graph minor theorem states that in any infinite sequence of finite graphs, one is a minor of another. "
            "This implies that the set of all finite graphs is well-quasi-ordered under the minor relation. "
            "The proof is highly complex and uses deep structural graph theory."
        ),
        key_factors=["Minor relation", "Well-quasi-ordering", "Infinite sequences"],
        primary_authority=["Robertson & Seymour", "Diestel, Graph Theory (5th ed.), Theorem 12.2.1"],
        burden_holder="Proponent of well-quasi-ordering",
        adversary_position="Sequence contains no minor relation",
        counter_arguments=[
            "Sequence is finite.",
            "No minor relation exists (contradicts the theorem)."
        ],
        resolution_strategy="Construct infinite sequence and check minor relations.",
        entity_scope="Finite graphs",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Robertson & Seymour (1983–2004); Diestel, Theorem 12.2.1"
    ),
    DoctrineBlock(
        topic="Lovász Local Lemma",
        keywords=["probabilistic method", "Lovász local lemma", "dependency graph"],
        conclusion_template="If events are not too dependent, the probability that none occur is positive.",
        reasoning_framework=(
            "The Lovász Local Lemma is a probabilistic tool for showing the existence of combinatorial objects. "
            "If events are mutually independent or only weakly dependent, and each event has small enough probability, then with positive probability none occur. "
            "The proof uses the dependency graph and induction."
        ),
        key_factors=["Event dependencies", "Probability bounds", "Dependency graph"],
        primary_authority=["Lovász (1975)", "Erdős & Lovász", "Alon & Spencer, The Probabilistic Method"],
        burden_holder="Proponent of existence of object",
        adversary_position="Events are too dependent or probabilities too high",
        counter_arguments=[
            "Events are highly dependent.",
            "Probability bounds are not met."
        ],
        resolution_strategy="Construct dependency graph and check bounds.",
        entity_scope="Random structures",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Erdős & Lovász (1975)"
    ),
    DoctrineBlock(
        topic="Perfect Graph Theorem",
        keywords=["perfect graph", "chromatic number", "clique number"],
        conclusion_template="A graph is perfect if and only if its complement is perfect (Strong Perfect Graph Theorem).",
        reasoning_framework=(
            "The Strong Perfect Graph Theorem states that a graph is perfect if and only if it contains no odd hole or odd antihole. "
            "A perfect graph is one in which the chromatic number equals the clique number for every induced subgraph. "
            "The proof is deep and uses structural decomposition."
        ),
        key_factors=["Odd holes", "Odd antiholes", "Induced subgraphs"],
        primary_authority=["Chudnovsky et al. (2006)", "Diestel, Graph Theory (5th ed.), Theorem 5.6.1"],
        burden_holder="Proponent of perfectness",
        adversary_position="Graph contains odd hole or antihole",
        counter_arguments=[
            "Graph contains an odd hole or odd antihole.",
            "Chromatic number exceeds clique number."
        ],
        resolution_strategy="Search for forbidden induced subgraphs.",
        entity_scope="Finite graphs",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Chudnovsky et al. (2006); Diestel, Theorem 5.6.1"
    ),
    DoctrineBlock(
        topic="Gallai's Theorem on Critical Graphs",
        keywords=["critical graph", "Gallai's theorem", "chromatic number"],
        conclusion_template="In a k-critical graph, the subgraph induced by vertices of degree k-1 is a forest.",
        reasoning_framework=(
            "Gallai's theorem gives a structural property of critical graphs. "
            "A k-critical graph is one with chromatic number k, but every proper subgraph has chromatic number less than k. "
            "The subgraph induced by vertices of degree k-1 is acyclic."
        ),
        key_factors=["Criticality", "Degree", "Induced subgraph"],
        primary_authority=["Gallai (1963)", "Diestel, Graph Theory (5th ed.), Theorem 5.2.3"],
        burden_holder="Proponent of acyclicity",
        adversary_position="Induced subgraph contains a cycle",
        counter_arguments=[
            "Subgraph contains a cycle.",
            "Graph is not k-critical."
        ],
        resolution_strategy="Check degree and induced subgraph structure.",
        entity_scope="Critical graphs",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Gallai (1963); Diestel, Theorem 5.2.3"
    ),
    DoctrineBlock(
        topic="Vertex Transitivity and Regularity",
        keywords=["vertex transitive", "regular graph", "automorphism"],
        conclusion_template="Every vertex-transitive graph is regular.",
        reasoning_framework=(
            "A graph is vertex-transitive if its automorphism group acts transitively on vertices. "
            "This implies all vertices have the same degree, i.e., the graph is regular. "
            "The proof uses group actions and automorphism properties."
        ),
        key_factors=["Automorphism group", "Degree", "Symmetry"],
        primary_authority=["Biggs, Algebraic Graph Theory", "Diestel, Graph Theory (5th ed.), Section 1.7"],
        burden_holder="Proponent of regularity",
        adversary_position="Graph is not vertex-transitive",
        counter_arguments=[
            "Graph is not vertex-transitive.",
            "Degrees differ among vertices."
        ],
        resolution_strategy="Check automorphism group and vertex degrees.",
        entity_scope="Vertex-transitive graphs",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Biggs, Algebraic Graph Theory"
    ),
    DoctrineBlock(
        topic="Spectral Radius and Maximum Degree",
        keywords=["spectral radius", "adjacency matrix", "maximum degree"],
        conclusion_template="The spectral radius of a simple graph does not exceed its maximum degree.",
        reasoning_framework=(
            "The spectral radius is the largest eigenvalue of the adjacency matrix. "
            "For a simple graph, the spectral radius is at most the maximum vertex degree. "
            "Proof uses Rayleigh quotient and properties of symmetric matrices."
        ),
        key_factors=["Adjacency matrix", "Eigenvalues", "Maximum degree"],
        primary_authority=["Brouwer & Haemers, Spectra of Graphs", "Diestel, Graph Theory (5th ed.), Section 1.8"],
        burden_holder="Proponent of spectral bound",
        adversary_position="Graph is not simple or eigenvalue exceeds degree",
        counter_arguments=[
            "Graph has loops or multiple edges.",
            "Spectral radius exceeds maximum degree."
        ],
        resolution_strategy="Verify simplicity and compute eigenvalues.",
        entity_scope="Simple graphs",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Brouwer & Haemers, Spectra of Graphs"
    ),
    DoctrineBlock(
        topic="Graph Isomorphism Problem",
        keywords=["graph isomorphism", "complexity", "automorphism"],
        conclusion_template="The graph isomorphism problem is in NP, but not known to be in P or NP-complete.",
        reasoning_framework=(
            "Determining whether two graphs are isomorphic is a central computational problem. "
            "It is known to be in NP, but its exact complexity is unresolved. "
            "Recent advances have shown quasi-polynomial time algorithms."
        ),
        key_factors=["Isomorphism", "Complexity class", "Automorphism group"],
        primary_authority=["Babai (2016)", "Diestel, Graph Theory (5th ed.), Section 1.9"],
        burden_holder="Proponent of efficient isomorphism testing",
        adversary_position="Problem is NP-complete or in P",
        counter_arguments=[
            "No polynomial-time algorithm is known.",
            "Problem is not known to be NP-complete."
        ],
        resolution_strategy="Apply known algorithms and complexity results.",
        entity_scope="Finite graphs",
        confidence=0.90,
        confidence_zone="Medium",
        controlling_precedent="Babai (2016); Diestel, Section 1.9"
    ),
    DoctrineBlock(
        topic="Graph Coloring Complexity",
        keywords=["graph coloring", "NP-completeness", "chromatic number"],
        conclusion_template="Determining the chromatic number of a graph is NP-complete.",
        reasoning_framework=(
            "The problem of deciding whether a graph can be colored with k colors is NP-complete for k ≥ 3. "
            "Proof uses reductions from 3-SAT and other NP-complete problems."
        ),
        key_factors=["Chromatic number", "Complexity", "Reduction"],
        primary_authority=["Karp (1972)", "Diestel, Graph Theory (5th ed.), Section 5.5"],
        burden_holder="Proponent of NP-completeness",
        adversary_position="Special graph classes allow polynomial-time coloring",
        counter_arguments=[
            "Graph is planar (4-colorable in polynomial time).",
            "Graph is bipartite (2-colorable in linear time)."
        ],
        resolution_strategy="Distinguish special cases from general graphs.",
        entity_scope="General graphs",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Karp (1972); Diestel, Section 5.5"
    ),
    DoctrineBlock(
        topic="Edge Connectivity and Minimum Degree",
        keywords=["edge connectivity", "minimum degree", "Menger's theorem"],
        conclusion_template="The edge connectivity of a graph is at most its minimum degree.",
        reasoning_framework=(
            "Edge connectivity is the minimum number of edges whose removal disconnects the graph. "
            "It cannot exceed the minimum vertex degree, since removing all edges at a minimum-degree vertex disconnects it."
        ),
        key_factors=["Edge connectivity", "Minimum degree", "Edge removal"],
        primary_authority=["Diestel, Graph Theory (5th ed.), Section 3.4"],
        burden_holder="Proponent of connectivity bound",
        adversary_position="Edge connectivity exceeds minimum degree",
        counter_arguments=[
            "Graph is disconnected.",
            "Edge connectivity is higher than minimum degree (contradicts the theorem)."
        ],
        resolution_strategy="Compute edge connectivity and minimum degree.",
        entity_scope="Finite graphs",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Diestel, Section 3.4"
    ),
    DoctrineBlock(
        topic="Vertex Cover and Independent Set Duality",
        keywords=["vertex cover", "independent set", "duality"],
        conclusion_template="In any graph, the size of a minimum vertex cover plus the size of a maximum independent set equals the number of vertices.",
        reasoning_framework=(
            "A vertex cover is a set of vertices touching all edges; an independent set is a set of vertices with no edges between them. "
            "In bipartite graphs, the minimum vertex cover size plus the maximum independent set size equals the number of vertices (König's theorem). "
            "In general graphs, this is an inequality."
        ),
        key_factors=["Vertex cover", "Independent set", "Graph structure"],
        primary_authority=["Kőnig (1931)", "Diestel, Graph Theory (5th ed.), Section 2.1"],
        burden_holder="Proponent of duality",
        adversary_position="Graph is not bipartite",
        counter_arguments=[
            "Graph is not bipartite (equality may not hold).",
            "Cover and independent set are not optimal."
        ],
        resolution_strategy="Verify bipartiteness and optimality.",
        entity_scope="Bipartite graphs",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Kőnig (1931); Diestel, Section 2.1"
    ),
    DoctrineBlock(
        topic="Clique and Independent Set Complementarity",
        keywords=["clique", "independent set", "complement graph"],
        conclusion_template="A clique in a graph corresponds to an independent set in its complement.",
        reasoning_framework=(
            "The complement of a graph G has the same vertex set, with edges where G does not. "
            "A clique in G is an independent set in the complement, and vice versa. "
            "This duality is used in many proofs and algorithms."
        ),
        key_factors=["Complement graph", "Clique", "Independent set"],
        primary_authority=["Diestel, Graph Theory (5th ed.), Section 1.2"],
        burden_holder="Proponent of complementarity",
        adversary_position="Graph is not simple or complement is ill-defined",
        counter_arguments=[
            "Graph has loops or multiple edges.",
            "Complement is not properly constructed."
        ],
        resolution_strategy="Verify simplicity and construct complement.",
        entity_scope="Simple graphs",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Diestel, Section 1.2"
    ),
    DoctrineBlock(
        topic="Graph Homomorphism",
        keywords=["graph homomorphism", "mapping", "adjacency"],
        conclusion_template="A graph homomorphism preserves adjacency between graphs.",
        reasoning_framework=(
            "A graph homomorphism is a mapping from the vertex set of one graph to another, preserving adjacency. "
            "That is, if u and v are adjacent in G, then their images are adjacent in H. "
            "Homomorphisms generalize colorings and other mappings."
        ),
        key_factors=["Vertex mapping", "Adjacency preservation", "Target graph"],
        primary_authority=["Hell & Nešetřil, Graphs and Homomorphisms", "Diestel, Graph Theory (5th ed.), Section 1.10"],
        burden_holder="Proponent of homomorphism",
        adversary_position="Mapping does not preserve adjacency",
        counter_arguments=[
            "Mapping fails to preserve adjacency.",
            "Target graph does not contain required edges."
        ],
        resolution_strategy="Check all mapped pairs for adjacency.",
        entity_scope="Graphs and mappings",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Hell & Nešetřil, Graphs and Homomorphisms"
    ),
    DoctrineBlock(
        topic="Graph Product Properties",
        keywords=["graph product", "Cartesian product", "strong product", "tensor product"],
        conclusion_template="The properties of a graph product depend on the operation used (Cartesian, strong, tensor, etc.).",
        reasoning_framework=(
            "Graph products combine two graphs into a new one, with different definitions (Cartesian, strong, tensor, etc.). "
            "Each product has distinct properties regarding connectivity, chromatic number, and diameter. "
            "Proofs use definitions and structural analysis."
        ),
        key_factors=["Product type", "Vertex pairs", "Edge construction"],
        primary_authority=["Imrich & Klavžar, Product Graphs", "Diestel, Graph Theory (5th ed.), Section 1.11"],
        burden_holder="Proponent of product property",
        adversary_position="Product is not well-defined or property fails",
        counter_arguments=[
            "Product is not properly constructed.",
            "Property does not hold for the product type."
        ],
        resolution_strategy="Specify product type and analyze structure.",
        entity_scope="Graph products",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Imrich & Klavžar, Product Graphs"
    ),
    DoctrineBlock(
        topic="Graph Decomposition into Trees",
        keywords=["tree decomposition", "treewidth", "graph minor"],
        conclusion_template="Every graph has a tree decomposition, and treewidth measures how close it is to a tree.",
        reasoning_framework=(
            "Tree decomposition is a mapping of a graph into a tree structure, with bags covering the vertices. "
            "Treewidth is the size of the largest bag minus one. "
            "Graphs with small treewidth are 'tree-like' and allow efficient algorithms."
        ),
        key_factors=["Tree decomposition", "Bags", "Treewidth"],
        primary_authority=["Robertson & Seymour", "Diestel, Graph Theory (5th ed.), Section 12.3"],
        burden_holder="Proponent of decomposition",
        adversary_position="Treewidth is large or decomposition is invalid",
        counter_arguments=[
            "Decomposition does not cover all edges.",
            "Bags do not form a tree structure."
        ],
        resolution_strategy="Verify decomposition properties.",
        entity_scope="Finite graphs",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Robertson & Seymour; Diestel, Section 12.3"
    ),
    DoctrineBlock(
        topic="Graph Planar Duality",
        keywords=["planar dual", "dual graph", "planarity"],
        conclusion_template="Every connected planar graph has a planar dual, unique up to isomorphism.",
        reasoning_framework=(
            "Given a planar embedding, the dual graph is constructed by placing a vertex in each face and connecting vertices whose faces share an edge. "
            "The dual is unique up to isomorphism for a given embedding. "
            "Proofs use embedding properties and duality arguments."
        ),
        key_factors=["Planar embedding", "Face adjacency", "Dual construction"],
        primary_authority=["Whitney (1932)", "Diestel, Graph Theory (5th ed.), Section 4.6"],
        burden_holder="Proponent of duality",
        adversary_position="Graph is not planar or embedding is not specified",
        counter_arguments=[
            "Graph is not planar.",
            "Dual is not unique for non-connected graphs."
        ],
        resolution_strategy="Specify embedding and construct dual.",
        entity_scope="Connected planar graphs",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Whitney (1932); Diestel, Section 4.6"
    ),
    DoctrineBlock(
        topic="Graph Connectivity Augmentation",
        keywords=["connectivity", "augmentation", "edge addition"],
        conclusion_template="A k-connected graph remains k-connected after adding edges.",
        reasoning_framework=(
            "Adding edges to a k-connected graph cannot decrease its connectivity. "
            "Proof uses the definition of k-connectivity and properties of vertex cuts."
        ),
        key_factors=["k-connectivity", "Edge addition", "Vertex cuts"],
        primary_authority=["Diestel, Graph Theory (5th ed.), Section 3.2"],
        burden_holder="Proponent of connectivity preservation",
        adversary_position="Edge addition creates new cuts",
        counter_arguments=[
            "Edge addition does not preserve other properties.",
            "Graph is not initially k-connected."
        ],
        resolution_strategy="Check initial connectivity and added edges.",
        entity_scope="Finite graphs",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Diestel, Section 3.2"
    ),
    DoctrineBlock(
        topic="Graph Minor Closure",
        keywords=["minor-closed", "graph property", "forbidden minors"],
        conclusion_template="A property is minor-closed if it is preserved under taking minors; such properties are characterized by a finite set of forbidden minors.",
        reasoning_framework=(
            "A property is minor-closed if, whenever a graph has it, so does every minor. "
            "Robertson–Seymour theorem guarantees a finite forbidden minor characterization for minor-closed properties."
        ),
        key_factors=["Minor relation", "Property preservation", "Forbidden minors"],
        primary_authority=["Robertson & Seymour", "Diestel, Graph Theory (5th ed.), Section 12.2"],
        burden_holder="Proponent of minor-closed property",
        adversary_position="Property is not preserved under minors",
        counter_arguments=[
            "Property is not minor-closed.",
            "No finite forbidden minor set exists."
        ],
        resolution_strategy="Check property under minor operations.",
        entity_scope="Finite graphs",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Robertson & Seymour; Diestel, Section 12.2"
    ),
    DoctrineBlock(
        topic="Graph Automorphism Group",
        keywords=["automorphism group", "symmetry", "group action"],
        conclusion_template="The automorphism group of a graph captures its symmetries.",
        reasoning_framework=(
            "An automorphism is a permutation of the vertex set preserving adjacency. "
            "The set of all automorphisms forms a group under composition, revealing the graph's symmetries."
        ),
        key_factors=["Permutation", "Adjacency preservation", "Group structure"],
        primary_authority=["Biggs, Algebraic Graph Theory", "Diestel, Graph Theory (5th ed.), Section 1.7"],
        burden_holder="Proponent of group structure",
        adversary_position="Automorphisms do not form a group",
        counter_arguments=[
            "Automorphisms do not preserve adjacency.",
            "Composition does not yield a group."
        ],
        resolution_strategy="Check group axioms for automorphisms.",
        entity_scope="Finite graphs",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Biggs, Algebraic Graph Theory"
    ),
    DoctrineBlock(
        topic="Graph Spectrum and Regularity",
        keywords=["spectrum", "regular graph", "eigenvalues"],
        conclusion_template="In a d-regular graph, d is an eigenvalue of the adjacency matrix.",
        reasoning_framework=(
            "The all-ones vector is an eigenvector of the adjacency matrix of a d-regular graph, with eigenvalue d. "
            "Proof uses linear algebra and regularity."
        ),
        key_factors=["Regularity", "Adjacency matrix", "Eigenvalues"],
        primary_authority=["Brouwer & Haemers, Spectra of Graphs", "Diestel, Graph Theory (5th ed.), Section 1.8"],
        burden_holder="Proponent of eigenvalue property",
        adversary_position="Graph is not regular",
        counter_arguments=[
            "Graph is not regular.",
            "Adjacency matrix is not properly constructed."
        ],
        resolution_strategy="Verify regularity and compute spectrum.",
        entity_scope="Regular graphs",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Brouwer & Haemers, Spectra of Graphs"
    ),
    DoctrineBlock(
        topic="Graph Girth and Cycle Structure",
        keywords=["girth", "cycle", "shortest cycle"],
        conclusion_template="The girth of a graph is the length of its shortest cycle.",
        reasoning_framework=(
            "Girth is a basic invariant of a graph, measuring the length of its shortest cycle. "
            "Proofs use breadth-first search and cycle analysis."
        ),
        key_factors=["Cycle length", "Graph structure", "Shortest cycle"],
        primary_authority=["Diestel, Graph Theory (5th ed.), Section 1.2"],
        burden_holder="Proponent of girth computation",
        adversary_position="Graph is acyclic or cycles are not properly identified",
        counter_arguments=[
            "Graph is acyclic (girth is infinite).",
            "Shortest cycle is not correctly found."
        ],
        resolution_strategy="Search for all cycles and find the shortest.",
        entity_scope="Finite graphs",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Diestel, Section 1.2"
    ),
    DoctrineBlock(
        topic="Graph Diameter",
        keywords=["diameter", "distance", "eccentricity"],
        conclusion_template="The diameter of a graph is the maximum distance between any pair of vertices.",
        reasoning_framework=(
            "Diameter is a measure of the 'size' of a graph in terms of distances. "
            "It is the greatest eccentricity among all vertices. "
            "Proofs use shortest path algorithms."
        ),
        key_factors=["Distances", "Eccentricity", "Vertex pairs"],
        primary_authority=["Diestel, Graph Theory (5th ed.), Section 1.2"],
        burden_holder="Proponent of diameter computation",
        adversary_position="Graph is disconnected",
        counter_arguments=[
            "Graph is disconnected (diameter is infinite).",
            "Distances are not properly computed."
        ],
        resolution_strategy="Compute all-pairs shortest paths.",
        entity_scope="Finite graphs",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Diestel, Section 1.2"
    ),
    DoctrineBlock(
        topic="Graph Center and Radius",
        keywords=["center", "radius", "eccentricity"],
        conclusion_template="The center of a graph is the set of vertices with minimum eccentricity; the radius is this minimum value.",
        reasoning_framework=(
            "The center consists of vertices with the smallest maximum distance to any other vertex. "
            "The radius is this minimum eccentricity. "
            "Proofs use distance matrices and eccentricity computation."
        ),
        key_factors=["Eccentricity", "Distances", "Vertex set"],
        primary_authority=["Diestel, Graph Theory (5th ed.), Section 1.2"],
        burden_holder="Proponent of center/radius computation",
        adversary_position="Graph is disconnected",
        counter_arguments=[
            "Graph is disconnected (center/radius undefined).",
            "Eccentricities are not properly computed."
        ],
        resolution_strategy="Compute eccentricities for all vertices.",
        entity_scope="Finite graphs",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Diestel, Section 1.2"
    ),
    DoctrineBlock(
        topic="Graph Matching Number",
        keywords=["matching number", "maximum matching", "edge set"],
        conclusion_template="The matching number is the size of the largest matching in a graph.",
        reasoning_framework=(
            "A matching is a set of edges without common vertices. "
            "The matching number is the maximum size of such a set. "
            "Proofs use augmenting paths and matching algorithms."
        ),
        key_factors=["Matching", "Edge set", "Vertex disjointness"],
        primary_authority=["Diestel, Graph Theory (5th ed.), Section 2.1"],
        burden_holder="Proponent of matching computation",
        adversary_position="Matching is not maximal",
        counter_arguments=[
            "Matching is not maximal.",
            "Edges share vertices."
        ],
        resolution_strategy="Apply matching algorithms.",
        entity_scope="Finite graphs",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Diestel, Section 2.1"
    ),
    DoctrineBlock(
        topic="Graph Covering Number",
        keywords=["covering number", "vertex cover", "edge cover"],
        conclusion_template="The covering number is the size of the smallest vertex (or edge) cover.",
        reasoning_framework=(
            "A vertex cover is a set of vertices touching all edges; an edge cover touches all vertices. "
            "The covering number is the minimum size of such a set. "
            "Proofs use optimization and covering algorithms."
        ),
        key_factors=["Vertex cover", "Edge cover", "Optimization"],
        primary_authority=["Diestel, Graph Theory (5th ed.), Section 2.1"],
        burden_holder="Proponent of covering computation",
        adversary_position="Cover is not minimal",
        counter_arguments=[
            "Cover is not minimal.",
            "Not all edges/vertices are covered."
        ],
        resolution_strategy="Apply covering algorithms.",
        entity_scope="Finite graphs",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Diestel, Section 2.1"
    ),
    DoctrineBlock(
        topic="Graph Independence Number",
        keywords=["independence number", "maximum independent set"],
        conclusion_template="The independence number is the size of the largest independent set in a graph.",
        reasoning_framework=(
            "An independent set is a set of vertices with no edges between them. "
            "The independence number is the maximum size of such a set. "
            "Proofs use combinatorial arguments and algorithms."
        ),
        key_factors=["Independent set", "Vertex set", "Edge absence"],
        primary_authority=["Diestel, Graph Theory (5th ed.), Section 2.1"],
        burden_holder="Proponent of independence computation",
        adversary_position="Set is not maximal or contains adjacent vertices",
        counter_arguments=[
            "Set is not maximal.",
            "Set contains adjacent vertices."
        ],
        resolution_strategy="Apply independence algorithms.",
        entity_scope="Finite graphs",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Diestel, Section 2.1"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    keyword_lower = keyword.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if (keyword_lower in doctrine.topic.lower() or
            any(keyword_lower in k.lower() for k in doctrine.keywords) or
            keyword_lower in doctrine.reasoning_framework.lower() or
            keyword_lower in doctrine.conclusion_template.lower()):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]