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
        topic="Vector Spaces",
        keywords=["vector space", "linear algebra", "field", "axioms"],
        conclusion_template="A set V with operations of addition and scalar multiplication forms a vector space over field F if all vector space axioms are satisfied.",
        reasoning_framework="""
        To determine if a set V with operations forms a vector space over a field F, verify the following axioms:
        1. Closure under addition: For all u, v in V, u + v is in V.
        2. Closure under scalar multiplication: For all a in F, v in V, a*v is in V.
        3. Associativity of addition: For all u, v, w in V, (u + v) + w = u + (v + w).
        4. Commutativity of addition: For all u, v in V, u + v = v + u.
        5. Existence of additive identity: There exists 0 in V such that v + 0 = v for all v in V.
        6. Existence of additive inverses: For all v in V, there exists -v in V such that v + (-v) = 0.
        7. Compatibility of scalar multiplication: For all a, b in F, v in V, (ab)*v = a*(b*v).
        8. Identity element of scalar multiplication: For all v in V, 1*v = v, where 1 is the multiplicative identity in F.
        9. Distributivity of scalar multiplication with respect to vector addition: For all a in F, u, v in V, a*(u + v) = a*u + a*v.
        10. Distributivity of scalar multiplication with respect to field addition: For all a, b in F, v in V, (a + b)*v = a*v + b*v.
        If all axioms are satisfied, V is a vector space over F.
        """,
        key_factors=["Closure", "Associativity", "Commutativity", "Identity", "Inverses", "Distributivity", "Field properties"],
        primary_authority=["Linear Algebra textbooks", "Axler: Linear Algebra Done Right", "Lang: Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Demonstrate violation of any vector space axiom",
        counter_arguments=["Set fails closure under addition or scalar multiplication", "Missing additive identity", "No additive inverses"],
        resolution_strategy="Systematic verification of each axiom with explicit examples or counterexamples",
        entity_scope="Sets with operations defined over fields",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 1"
    ),
    DoctrineBlock(
        topic="Subspaces",
        keywords=["subspace", "vector space", "subset", "linear algebra"],
        conclusion_template="A subset W of a vector space V is a subspace if W is non-empty and closed under addition and scalar multiplication.",
        reasoning_framework="""
        To establish that W is a subspace of V:
        1. Non-empty: W contains at least one element (often the zero vector).
        2. Closed under addition: For all u, v in W, u + v is in W.
        3. Closed under scalar multiplication: For all a in F, v in W, a*v is in W.
        If these conditions are met, W is a subspace of V.
        Commonly, the zero vector's presence is checked first, then closure properties.
        """,
        key_factors=["Non-emptiness", "Closure under addition", "Closure under scalar multiplication"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show W fails closure or lacks zero vector",
        counter_arguments=["W does not contain zero vector", "Addition or scalar multiplication not closed"],
        resolution_strategy="Direct verification of closure and zero vector presence",
        entity_scope="Subsets of vector spaces",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 1"
    ),
    DoctrineBlock(
        topic="Linear Independence",
        keywords=["linear independence", "vectors", "span", "linear combination"],
        conclusion_template="A set of vectors {v1, ..., vn} is linearly independent if the only solution to a1*v1 + ... + an*vn = 0 is a1=...=an=0.",
        reasoning_framework="""
        To determine linear independence:
        1. Form the equation a1*v1 + ... + an*vn = 0.
        2. Solve for coefficients a1, ..., an.
        3. If the only solution is all ai = 0, the set is linearly independent.
        4. If there exists a nontrivial solution (some ai ≠ 0), the set is dependent.
        Use matrix methods (row reduction) or theoretical arguments to analyze the solution space.
        """,
        key_factors=["Existence of nontrivial solutions", "Span", "Linear combinations"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Provide a nontrivial linear combination yielding zero",
        counter_arguments=["Existence of nontrivial solution", "Vectors are scalar multiples"],
        resolution_strategy="Matrix row reduction or theoretical proof",
        entity_scope="Sets of vectors in vector spaces",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 2"
    ),
    DoctrineBlock(
        topic="Basis",
        keywords=["basis", "vector space", "linear independence", "span"],
        conclusion_template="A set B is a basis for vector space V if B is linearly independent and spans V.",
        reasoning_framework="""
        To establish B as a basis for V:
        1. Show B is linearly independent.
        2. Show every vector in V can be written as a linear combination of vectors in B.
        If both conditions are satisfied, B is a basis.
        The number of vectors in B is the dimension of V.
        """,
        key_factors=["Linear independence", "Spanning", "Dimension"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show B fails independence or spanning",
        counter_arguments=["B does not span V", "B is not independent"],
        resolution_strategy="Direct proof or matrix methods",
        entity_scope="Sets of vectors in vector spaces",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 2"
    ),
    DoctrineBlock(
        topic="Dimension",
        keywords=["dimension", "basis", "vector space", "cardinality"],
        conclusion_template="The dimension of a vector space V is the number of vectors in any basis for V.",
        reasoning_framework="""
        Dimension is defined as the cardinality of any basis for V.
        All bases for V have the same number of vectors.
        To find dimension:
        1. Find a basis for V.
        2. Count the number of vectors in the basis.
        For finite-dimensional spaces, this is straightforward; for infinite-dimensional, cardinality is used.
        """,
        key_factors=["Basis", "Cardinality", "Finite vs infinite dimension"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show existence of bases with different cardinalities",
        counter_arguments=["Different bases have different sizes", "No basis found"],
        resolution_strategy="Proof of basis equivalence, constructive basis finding",
        entity_scope="Vector spaces",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 2"
    ),
    DoctrineBlock(
        topic="Row Space",
        keywords=["row space", "matrix", "span", "linear algebra"],
        conclusion_template="The row space of matrix A is the span of its row vectors in F^n.",
        reasoning_framework="""
        The row space of an m x n matrix A is the set of all linear combinations of its row vectors.
        To analyze row space:
        1. Take all rows of A as vectors in F^n.
        2. The span of these vectors forms the row space.
        Row reduction can be used to find a basis for the row space.
        """,
        key_factors=["Row vectors", "Span", "Linear combinations"],
        primary_authority=["Strang: Introduction to Linear Algebra", "Axler: Linear Algebra Done Right"],
        burden_holder="Proponent",
        adversary_position="Show row vectors do not span claimed space",
        counter_arguments=["Rows are not independent", "Span is incorrect"],
        resolution_strategy="Row reduction, direct computation",
        entity_scope="Matrices over fields",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Strang: Introduction to Linear Algebra, Ch. 3"
    ),
    DoctrineBlock(
        topic="Column Space",
        keywords=["column space", "matrix", "span", "linear algebra"],
        conclusion_template="The column space of matrix A is the span of its column vectors in F^m.",
        reasoning_framework="""
        The column space of an m x n matrix A is the set of all linear combinations of its column vectors.
        To analyze column space:
        1. Take all columns of A as vectors in F^m.
        2. The span of these vectors forms the column space.
        Column reduction or pivot analysis can be used to find a basis.
        """,
        key_factors=["Column vectors", "Span", "Linear combinations"],
        primary_authority=["Strang: Introduction to Linear Algebra", "Axler: Linear Algebra Done Right"],
        burden_holder="Proponent",
        adversary_position="Show columns do not span claimed space",
        counter_arguments=["Columns are not independent", "Span is incorrect"],
        resolution_strategy="Column reduction, pivot analysis",
        entity_scope="Matrices over fields",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Strang: Introduction to Linear Algebra, Ch. 3"
    ),
    DoctrineBlock(
        topic="Null Space",
        keywords=["null space", "kernel", "matrix", "linear algebra"],
        conclusion_template="The null space of matrix A is the set of all vectors x such that Ax = 0.",
        reasoning_framework="""
        The null space (kernel) of matrix A is the solution set to Ax = 0.
        To find null space:
        1. Set up the equation Ax = 0.
        2. Solve for x using row reduction.
        3. The set of all solutions forms the null space.
        The null space is a subspace of F^n.
        """,
        key_factors=["Kernel", "Homogeneous solutions", "Row reduction"],
        primary_authority=["Strang: Introduction to Linear Algebra", "Axler: Linear Algebra Done Right"],
        burden_holder="Proponent",
        adversary_position="Show claimed null space does not satisfy Ax = 0",
        counter_arguments=["Incorrect solution set", "Nonzero vectors not mapped to zero"],
        resolution_strategy="Row reduction, direct computation",
        entity_scope="Matrices over fields",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Strang: Introduction to Linear Algebra, Ch. 3"
    ),
    DoctrineBlock(
        topic="Rank",
        keywords=["rank", "matrix", "dimension", "linear algebra"],
        conclusion_template="The rank of matrix A is the dimension of its row space (or column space).",
        reasoning_framework="""
        Rank is defined as the maximal number of linearly independent rows or columns in A.
        To find rank:
        1. Reduce A to row echelon form.
        2. Count the number of nonzero rows.
        This equals the dimension of the row space and column space.
        Rank is used to determine solvability of linear systems.
        """,
        key_factors=["Row reduction", "Linear independence", "Dimension"],
        primary_authority=["Strang: Introduction to Linear Algebra", "Axler: Linear Algebra Done Right"],
        burden_holder="Proponent",
        adversary_position="Show more independent rows/columns exist",
        counter_arguments=["Incorrect count", "Dependent rows/columns"],
        resolution_strategy="Row reduction, direct computation",
        entity_scope="Matrices over fields",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Strang: Introduction to Linear Algebra, Ch. 3"
    ),
    DoctrineBlock(
        topic="Rank-Nullity Theorem",
        keywords=["rank-nullity theorem", "dimension", "matrix", "linear algebra"],
        conclusion_template="For matrix A (m x n), dim(null space) + rank(A) = n.",
        reasoning_framework="""
        The rank-nullity theorem states that for a linear transformation T: V -> W, dim(ker T) + rank(T) = dim(V).
        For matrices, dim(null space) + rank(A) = number of columns.
        To apply:
        1. Find rank(A) via row reduction.
        2. Find nullity (dimension of null space).
        3. Verify sum equals number of columns.
        Used to analyze solution spaces and structure of linear systems.
        """,
        key_factors=["Rank", "Nullity", "Dimension", "Linear transformation"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show sum does not equal number of columns",
        counter_arguments=["Incorrect rank or nullity", "Sum mismatch"],
        resolution_strategy="Direct computation, theoretical proof",
        entity_scope="Matrices and linear transformations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 3"
    ),
    DoctrineBlock(
        topic="Linear Transformations",
        keywords=["linear transformation", "matrix", "function", "linear algebra"],
        conclusion_template="A function T: V -> W is linear if T(av + bw) = aT(v) + bT(w) for all v, w in V and a, b in F.",
        reasoning_framework="""
        To verify linearity:
        1. Check additivity: T(v + w) = T(v) + T(w).
        2. Check homogeneity: T(a*v) = a*T(v).
        If both hold for all v, w in V and a in F, T is linear.
        Linear transformations preserve vector space structure.
        """,
        key_factors=["Additivity", "Homogeneity", "Preservation of structure"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show T fails additivity or homogeneity",
        counter_arguments=["T does not preserve addition or scalar multiplication"],
        resolution_strategy="Direct verification, counterexample",
        entity_scope="Functions between vector spaces",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 3"
    ),
    DoctrineBlock(
        topic="Matrix Representation of Linear Transformations",
        keywords=["matrix representation", "linear transformation", "basis", "linear algebra"],
        conclusion_template="A linear transformation T: V -> W is represented by a matrix relative to chosen bases of V and W.",
        reasoning_framework="""
        To represent T as a matrix:
        1. Choose bases for V and W.
        2. Express T(basis vector) as linear combination of W's basis.
        3. Columns of matrix are coefficients of these combinations.
        The matrix captures T's action relative to bases.
        Changing bases changes representation via similarity transformations.
        """,
        key_factors=["Choice of basis", "Coefficients", "Similarity"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show representation fails to capture T's action",
        counter_arguments=["Incorrect coefficients", "Basis mismatch"],
        resolution_strategy="Direct computation, basis change analysis",
        entity_scope="Linear transformations between finite-dimensional vector spaces",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 3"
    ),
    DoctrineBlock(
        topic="Invertibility of Matrices",
        keywords=["invertible matrix", "nonsingular", "inverse", "linear algebra"],
        conclusion_template="A square matrix A is invertible if there exists B such that AB = BA = I.",
        reasoning_framework="""
        To determine invertibility:
        1. Check if A is square.
        2. Find B such that AB = BA = I.
        3. Alternatively, check if det(A) ≠ 0.
        4. Row reduction: If A reduces to identity, it is invertible.
        Invertibility implies unique solutions to Ax = b for all b.
        """,
        key_factors=["Square matrix", "Existence of inverse", "Determinant", "Row reduction"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show no matrix B exists or det(A) = 0",
        counter_arguments=["Determinant zero", "No inverse found"],
        resolution_strategy="Row reduction, determinant computation",
        entity_scope="Square matrices over fields",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 4"
    ),
    DoctrineBlock(
        topic="Determinant",
        keywords=["determinant", "matrix", "linear algebra", "invertibility"],
        conclusion_template="The determinant of a square matrix A is a scalar measuring volume scaling and invertibility.",
        reasoning_framework="""
        The determinant is computed via cofactor expansion, row reduction, or recursive definitions.
        Properties:
        1. det(A) = 0 iff A is singular.
        2. det(AB) = det(A)det(B).
        3. det(A^T) = det(A).
        4. Row operations affect determinant predictably.
        Used to analyze invertibility, volume scaling, and orientation.
        """,
        key_factors=["Cofactor expansion", "Row operations", "Invertibility"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show determinant calculation is incorrect",
        counter_arguments=["Incorrect expansion", "Row operation error"],
        resolution_strategy="Direct computation, property analysis",
        entity_scope="Square matrices over fields",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 4"
    ),
    DoctrineBlock(
        topic="Eigenvalues and Eigenvectors",
        keywords=["eigenvalue", "eigenvector", "matrix", "linear algebra"],
        conclusion_template="λ is an eigenvalue of A if there exists nonzero v such that Av = λv; v is the corresponding eigenvector.",
        reasoning_framework="""
        To find eigenvalues:
        1. Solve det(A - λI) = 0.
        2. For each λ, solve (A - λI)v = 0 for nonzero v.
        Eigenvectors are solutions to this equation.
        Used in diagonalization, stability analysis, and more.
        """,
        key_factors=["Characteristic polynomial", "Determinant", "Nontrivial solutions"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show no nonzero v exists for claimed λ",
        counter_arguments=["Incorrect λ", "No eigenvector found"],
        resolution_strategy="Direct computation, characteristic polynomial analysis",
        entity_scope="Square matrices over fields",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 5"
    ),
    DoctrineBlock(
        topic="Diagonalization",
        keywords=["diagonalization", "matrix", "eigenvalue", "linear algebra"],
        conclusion_template="A matrix A is diagonalizable if there exists invertible P and diagonal D such that A = PDP^{-1}.",
        reasoning_framework="""
        To diagonalize A:
        1. Find eigenvalues and eigenvectors.
        2. If n linearly independent eigenvectors exist, form P from them.
        3. D is diagonal with eigenvalues.
        If not enough independent eigenvectors, A is not diagonalizable.
        Used for simplifying powers of matrices and systems.
        """,
        key_factors=["Eigenvalues", "Eigenvectors", "Invertibility", "Independence"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show insufficient independent eigenvectors",
        counter_arguments=["Defective matrix", "Repeated eigenvalues without enough eigenvectors"],
        resolution_strategy="Direct computation, independence analysis",
        entity_scope="Square matrices over fields",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 5"
    ),
    DoctrineBlock(
        topic="Orthogonality",
        keywords=["orthogonality", "inner product", "vector", "linear algebra"],
        conclusion_template="Vectors u and v are orthogonal if their inner product is zero.",
        reasoning_framework="""
        To check orthogonality:
        1. Compute inner product <u, v>.
        2. If <u, v> = 0, vectors are orthogonal.
        Orthogonality is used in projections, decompositions, and basis construction.
        """,
        key_factors=["Inner product", "Zero value", "Projection"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show inner product is nonzero",
        counter_arguments=["Incorrect inner product", "Vectors not perpendicular"],
        resolution_strategy="Direct computation, geometric analysis",
        entity_scope="Vectors in inner product spaces",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 6"
    ),
    DoctrineBlock(
        topic="Orthogonal Projection",
        keywords=["orthogonal projection", "vector", "subspace", "linear algebra"],
        conclusion_template="The orthogonal projection of v onto subspace W is the unique vector in W closest to v.",
        reasoning_framework="""
        To compute orthogonal projection:
        1. Find basis for W.
        2. Use formula: proj_W(v) = sum(<v, w_i>/<w_i, w_i>)*w_i for orthogonal basis {w_i}.
        Projection minimizes distance between v and W.
        Used in least squares, decompositions.
        """,
        key_factors=["Inner product", "Distance minimization", "Basis"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show projection is not closest vector",
        counter_arguments=["Incorrect computation", "Non-orthogonal basis"],
        resolution_strategy="Direct computation, geometric analysis",
        entity_scope="Vectors and subspaces in inner product spaces",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 6"
    ),
    DoctrineBlock(
        topic="Gram-Schmidt Process",
        keywords=["Gram-Schmidt", "orthogonalization", "basis", "linear algebra"],
        conclusion_template="The Gram-Schmidt process converts a basis into an orthogonal (or orthonormal) basis.",
        reasoning_framework="""
        To apply Gram-Schmidt:
        1. Start with basis {v1, ..., vn}.
        2. Set u1 = v1.
        3. For k > 1, set uk = vk - sum(<vk, uj>/<uj, uj>)*uj for j=1 to k-1.
        4. Normalize for orthonormal basis.
        Used for constructing orthogonal bases and simplifying computations.
        """,
        key_factors=["Orthogonalization", "Inner product", "Normalization"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show process fails to produce orthogonal basis",
        counter_arguments=["Incorrect subtraction", "Normalization error"],
        resolution_strategy="Step-by-step computation, verification",
        entity_scope="Bases in inner product spaces",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 6"
    ),
    DoctrineBlock(
        topic="Least Squares Solution",
        keywords=["least squares", "linear system", "projection", "linear algebra"],
        conclusion_template="The least squares solution to Ax = b minimizes ||Ax - b||; x = (A^T A)^{-1}A^T b if A^T A is invertible.",
        reasoning_framework="""
        To find least squares solution:
        1. Set up normal equations: A^T A x = A^T b.
        2. Solve for x.
        3. If A^T A is invertible, x = (A^T A)^{-1}A^T b.
        Used when system Ax = b is inconsistent.
        Solution is projection of b onto column space of A.
        """,
        key_factors=["Normal equations", "Invertibility", "Projection"],
        primary_authority=["Strang: Introduction to Linear Algebra", "Axler: Linear Algebra Done Right"],
        burden_holder="Proponent",
        adversary_position="Show solution does not minimize norm",
        counter_arguments=["Incorrect computation", "A^T A not invertible"],
        resolution_strategy="Direct computation, invertibility check",
        entity_scope="Linear systems with more equations than unknowns",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Strang: Introduction to Linear Algebra, Ch. 7"
    ),
    DoctrineBlock(
        topic="Inner Product Spaces",
        keywords=["inner product space", "vector", "linear algebra", "norm"],
        conclusion_template="A vector space V with an inner product is an inner product space.",
        reasoning_framework="""
        To verify inner product space:
        1. Check vector space axioms.
        2. Check inner product properties: linearity, symmetry, positive-definiteness.
        Inner product induces norm and geometric concepts.
        Used in orthogonality, projections, and more.
        """,
        key_factors=["Vector space", "Inner product properties", "Norm"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show inner product fails properties",
        counter_arguments=["Non-positive definite", "Non-symmetric"],
        resolution_strategy="Direct verification, counterexample",
        entity_scope="Vector spaces with inner product defined",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 6"
    ),
    DoctrineBlock(
        topic="Norm",
        keywords=["norm", "vector", "length", "linear algebra"],
        conclusion_template="The norm of vector v is ||v|| = sqrt(<v, v>) in inner product spaces.",
        reasoning_framework="""
        Norm measures length of vector.
        In inner product spaces, ||v|| = sqrt(<v, v>).
        Properties: positive-definite, homogeneous, triangle inequality.
        Used in distance, convergence, and geometric analysis.
        """,
        key_factors=["Inner product", "Positive-definite", "Triangle inequality"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show norm fails properties",
        counter_arguments=["Negative norm", "Triangle inequality violation"],
        resolution_strategy="Direct computation, property verification",
        entity_scope="Vectors in normed spaces",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 6"
    ),
    DoctrineBlock(
        topic="Spectral Theorem",
        keywords=["spectral theorem", "self-adjoint", "eigenvalue", "linear algebra"],
        conclusion_template="A self-adjoint operator on finite-dimensional inner product space has orthonormal basis of eigenvectors.",
        reasoning_framework="""
        For self-adjoint (Hermitian) operators:
        1. All eigenvalues are real.
        2. Eigenvectors corresponding to distinct eigenvalues are orthogonal.
        3. There exists orthonormal basis of eigenvectors.
        Used in diagonalization, quantum mechanics, and more.
        """,
        key_factors=["Self-adjointness", "Orthonormal basis", "Real eigenvalues"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show operator is not self-adjoint or lacks basis",
        counter_arguments=["Non-Hermitian", "No orthonormal basis"],
        resolution_strategy="Direct computation, theoretical proof",
        entity_scope="Operators on finite-dimensional inner product spaces",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 7"
    ),
    DoctrineBlock(
        topic="Jordan Canonical Form",
        keywords=["Jordan form", "canonical form", "matrix", "linear algebra"],
        conclusion_template="Every square matrix over algebraically closed field is similar to a Jordan canonical form.",
        reasoning_framework="""
        To find Jordan form:
        1. Compute eigenvalues and generalized eigenvectors.
        2. Construct Jordan blocks for each eigenvalue.
        3. Matrix is similar to block diagonal Jordan form.
        Used for analyzing non-diagonalizable matrices.
        """,
        key_factors=["Eigenvalues", "Generalized eigenvectors", "Similarity"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show matrix not similar to Jordan form",
        counter_arguments=["Insufficient generalized eigenvectors", "Field not algebraically closed"],
        resolution_strategy="Direct computation, theoretical proof",
        entity_scope="Square matrices over algebraically closed fields",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 8"
    ),
    DoctrineBlock(
        topic="Singular Value Decomposition",
        keywords=["SVD", "singular value decomposition", "matrix", "linear algebra"],
        conclusion_template="Any m x n matrix A can be written as UΣV^T with U, V orthogonal and Σ diagonal.",
        reasoning_framework="""
        SVD decomposes A as UΣV^T:
        1. U: orthogonal m x m matrix.
        2. Σ: diagonal m x n matrix with nonnegative entries (singular values).
        3. V: orthogonal n x n matrix.
        Used in data compression, pseudoinverse, and more.
        """,
        key_factors=["Orthogonal matrices", "Singular values", "Decomposition"],
        primary_authority=["Strang: Introduction to Linear Algebra", "Axler: Linear Algebra Done Right"],
        burden_holder="Proponent",
        adversary_position="Show decomposition fails or matrices not orthogonal",
        counter_arguments=["Incorrect singular values", "Non-orthogonal U or V"],
        resolution_strategy="Direct computation, theoretical proof",
        entity_scope="Matrices over real or complex fields",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Strang: Introduction to Linear Algebra, Ch. 8"
    ),
    DoctrineBlock(
        topic="Change of Basis",
        keywords=["change of basis", "matrix", "linear transformation", "linear algebra"],
        conclusion_template="Changing basis in V transforms matrix representation via similarity: A' = P^{-1}AP.",
        reasoning_framework="""
        To change basis:
        1. Find transition matrix P from old to new basis.
        2. Compute A' = P^{-1}AP.
        Used to simplify computations and reveal structure.
        Similarity preserves eigenvalues and determinant.
        """,
        key_factors=["Transition matrix", "Similarity", "Preservation"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show transformation does not preserve structure",
        counter_arguments=["Incorrect transition matrix", "Similarity error"],
        resolution_strategy="Direct computation, theoretical proof",
        entity_scope="Matrix representations of linear transformations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 3"
    ),
    DoctrineBlock(
        topic="Direct Sum",
        keywords=["direct sum", "vector space", "subspace", "linear algebra"],
        conclusion_template="V is direct sum of subspaces W1, ..., Wn if every v in V is unique sum of w1 in W1, ..., wn in Wn.",
        reasoning_framework="""
        To verify direct sum:
        1. Check V = W1 + ... + Wn (every vector is sum).
        2. Check uniqueness: intersection of subspaces is {0}.
        Used in decomposing spaces and analyzing structure.
        """,
        key_factors=["Uniqueness", "Intersection", "Decomposition"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show sum not unique or intersection nonzero",
        counter_arguments=["Non-unique representation", "Intersection not trivial"],
        resolution_strategy="Direct computation, intersection analysis",
        entity_scope="Vector spaces and subspaces",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 2"
    ),
    DoctrineBlock(
        topic="Quotient Spaces",
        keywords=["quotient space", "vector space", "subspace", "linear algebra"],
        conclusion_template="V/W is the set of cosets v + W for v in V; forms vector space if W is subspace.",
        reasoning_framework="""
        To construct quotient space:
        1. Define cosets: v + W = {v + w | w in W}.
        2. Operations: (v + W) + (u + W) = (v + u) + W; a*(v + W) = (a*v) + W.
        3. If W is subspace, quotient inherits vector space structure.
        Used in factorization and structure analysis.
        """,
        key_factors=["Cosets", "Subspace", "Operations"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show quotient fails vector space axioms",
        counter_arguments=["W not subspace", "Coset operations fail"],
        resolution_strategy="Direct computation, axiom verification",
        entity_scope="Vector spaces and subspaces",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 2"
    ),
    DoctrineBlock(
        topic="Isomorphism of Vector Spaces",
        keywords=["isomorphism", "vector space", "linear transformation", "linear algebra"],
        conclusion_template="V and W are isomorphic if there exists invertible linear transformation T: V -> W.",
        reasoning_framework="""
        To establish isomorphism:
        1. Find linear transformation T: V -> W.
        2. Show T is invertible (bijective).
        3. Isomorphic spaces have same dimension.
        Used to classify spaces up to structure.
        """,
        key_factors=["Invertibility", "Dimension", "Linear transformation"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show no invertible transformation exists",
        counter_arguments=["Different dimensions", "Transformation not bijective"],
        resolution_strategy="Direct computation, dimension analysis",
        entity_scope="Vector spaces",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 3"
    ),
    DoctrineBlock(
        topic="Symmetric Matrices",
        keywords=["symmetric matrix", "matrix", "linear algebra", "transpose"],
        conclusion_template="A matrix A is symmetric if A = A^T.",
        reasoning_framework="""
        To check symmetry:
        1. Compute transpose A^T.
        2. Compare entries: A[i][j] = A[j][i].
        Symmetric matrices have real eigenvalues and orthogonal eigenvectors.
        Used in quadratic forms, spectral theorem.
        """,
        key_factors=["Transpose", "Entry comparison", "Eigenvalues"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show A ≠ A^T",
        counter_arguments=["Entry mismatch", "Non-symmetric structure"],
        resolution_strategy="Direct computation, entry analysis",
        entity_scope="Square matrices",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 6"
    ),
    DoctrineBlock(
        topic="Positive Definite Matrices",
        keywords=["positive definite", "matrix", "quadratic form", "linear algebra"],
        conclusion_template="A symmetric matrix A is positive definite if x^T A x > 0 for all nonzero x.",
        reasoning_framework="""
        To check positive definiteness:
        1. Verify symmetry: A = A^T.
        2. For all nonzero x, compute x^T A x.
        3. If always positive, A is positive definite.
        Used in optimization, stability, and quadratic forms.
        """,
        key_factors=["Symmetry", "Quadratic form", "Positivity"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show x^T A x ≤ 0 for some x",
        counter_arguments=["Negative or zero quadratic form", "Non-symmetric"],
        resolution_strategy="Direct computation, eigenvalue analysis",
        entity_scope="Symmetric matrices",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 6"
    ),
    DoctrineBlock(
        topic="Quadratic Forms",
        keywords=["quadratic form", "matrix", "vector", "linear algebra"],
        conclusion_template="A quadratic form is Q(x) = x^T A x for symmetric matrix A.",
        reasoning_framework="""
        Quadratic forms are functions Q(x) = x^T A x.
        A must be symmetric for real-valued Q.
        Used in optimization, classification, and geometry.
        Analyze definiteness via eigenvalues of A.
        """,
        key_factors=["Symmetry", "Eigenvalues", "Definiteness"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show A not symmetric or Q not quadratic",
        counter_arguments=["Non-symmetric matrix", "Incorrect form"],
        resolution_strategy="Direct computation, eigenvalue analysis",
        entity_scope="Symmetric matrices and vectors",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 6"
    ),
    DoctrineBlock(
        topic="Affine Spaces",
        keywords=["affine space", "vector space", "linear algebra", "translation"],
        conclusion_template="An affine space is a set of points closed under affine combinations but not vector addition.",
        reasoning_framework="""
        Affine spaces generalize vector spaces:
        1. Points are related via translations.
        2. Closed under affine combinations: sum a_i p_i with sum a_i = 1.
        3. Not closed under vector addition.
        Used in geometry and computer graphics.
        """,
        key_factors=["Affine combinations", "Translation", "Closure"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show closure under vector addition",
        counter_arguments=["Incorrect closure", "Not affine"],
        resolution_strategy="Direct computation, combination analysis",
        entity_scope="Sets of points in vector spaces",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 2"
    ),
    DoctrineBlock(
        topic="Linear Systems Solvability",
        keywords=["linear system", "solvability", "matrix", "rank"],
        conclusion_template="A linear system Ax = b is solvable iff rank(A) = rank([A|b]).",
        reasoning_framework="""
        To check solvability:
        1. Compute rank(A).
        2. Compute rank([A|b]), augmented matrix.
        3. If ranks equal, system is consistent.
        Used in analyzing existence of solutions.
        """,
        key_factors=["Rank", "Augmented matrix", "Consistency"],
        primary_authority=["Strang: Introduction to Linear Algebra", "Axler: Linear Algebra Done Right"],
        burden_holder="Proponent",
        adversary_position="Show ranks differ",
        counter_arguments=["Rank mismatch", "Inconsistent system"],
        resolution_strategy="Direct computation, rank analysis",
        entity_scope="Linear systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Strang: Introduction to Linear Algebra, Ch. 3"
    ),
    DoctrineBlock(
        topic="Homogeneous Linear Systems",
        keywords=["homogeneous system", "linear system", "null space", "linear algebra"],
        conclusion_template="A homogeneous system Ax = 0 has nontrivial solutions iff nullity(A) > 0.",
        reasoning_framework="""
        To analyze homogeneous system:
        1. Solve Ax = 0.
        2. If nullity(A) > 0 (dimension of null space), nontrivial solutions exist.
        Used in analyzing dependence and structure.
        """,
        key_factors=["Nullity", "Dimension", "Dependence"],
        primary_authority=["Strang: Introduction to Linear Algebra", "Axler: Linear Algebra Done Right"],
        burden_holder="Proponent",
        adversary_position="Show nullity is zero",
        counter_arguments=["Full rank", "No nontrivial solution"],
        resolution_strategy="Direct computation, null space analysis",
        entity_scope="Linear systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Strang: Introduction to Linear Algebra, Ch. 3"
    ),
    DoctrineBlock(
        topic="Cramer's Rule",
        keywords=["Cramer's rule", "linear system", "determinant", "matrix"],
        conclusion_template="If A is invertible, x_i = det(A_i)/det(A) solves Ax = b, where A_i is A with column i replaced by b.",
        reasoning_framework="""
        To apply Cramer's Rule:
        1. Check A is square and det(A) ≠ 0.
        2. For each variable x_i, replace column i with b, compute determinant.
        3. x_i = det(A_i)/det(A).
        Used for explicit solutions to small systems.
        """,
        key_factors=["Invertibility", "Determinant", "Column replacement"],
        primary_authority=["Strang: Introduction to Linear Algebra", "Axler: Linear Algebra Done Right"],
        burden_holder="Proponent",
        adversary_position="Show det(A) = 0 or incorrect computation",
        counter_arguments=["Singular matrix", "Incorrect determinant"],
        resolution_strategy="Direct computation, determinant analysis",
        entity_scope="Square systems of equations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Strang: Introduction to Linear Algebra, Ch. 3"
    ),
    DoctrineBlock(
        topic="Permutation Matrices",
        keywords=["permutation matrix", "matrix", "linear algebra", "row operations"],
        conclusion_template="A permutation matrix is obtained by permuting rows of identity matrix.",
        reasoning_framework="""
        To construct permutation matrix:
        1. Start with identity matrix.
        2. Permute rows according to desired order.
        Permutation matrices are orthogonal and used in row operations.
        """,
        key_factors=["Row permutation", "Orthogonality", "Identity matrix"],
        primary_authority=["Strang: Introduction to Linear Algebra", "Axler: Linear Algebra Done Right"],
        burden_holder="Proponent",
        adversary_position="Show matrix not permutation",
        counter_arguments=["Incorrect permutation", "Non-orthogonal"],
        resolution_strategy="Direct computation, row analysis",
        entity_scope="Square matrices",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Strang: Introduction to Linear Algebra, Ch. 3"
    ),
    DoctrineBlock(
        topic="Projection Matrices",
        keywords=["projection matrix", "matrix", "linear algebra", "projection"],
        conclusion_template="A projection matrix P satisfies P^2 = P; projects onto subspace.",
        reasoning_framework="""
        To verify projection matrix:
        1. Compute P^2.
        2. If P^2 = P, matrix is projection.
        Projection matrices are used in decompositions and least squares.
        """,
        key_factors=["Idempotence", "Subspace", "Decomposition"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show P^2 ≠ P",
        counter_arguments=["Non-idempotent", "Incorrect projection"],
        resolution_strategy="Direct computation, idempotence analysis",
        entity_scope="Square matrices",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 6"
    ),
    DoctrineBlock(
        topic="LU Decomposition",
        keywords=["LU decomposition", "matrix", "linear algebra", "factorization"],
        conclusion_template="Any square matrix A can be written as A = LU, with L lower and U upper triangular.",
        reasoning_framework="""
        To find LU decomposition:
        1. Use Gaussian elimination to reduce A to upper triangular U.
        2. Record multipliers to construct L.
        Used in solving systems and matrix inversion.
        Not all matrices admit LU without row exchanges.
        """,
        key_factors=["Triangular matrices", "Gaussian elimination", "Multipliers"],
        primary_authority=["Strang: Introduction to Linear Algebra", "Axler: Linear Algebra Done Right"],
        burden_holder="Proponent",
        adversary_position="Show decomposition fails or requires row exchanges",
        counter_arguments=["Pivoting required", "Non-unique decomposition"],
        resolution_strategy="Direct computation, elimination analysis",
        entity_scope="Square matrices",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Strang: Introduction to Linear Algebra, Ch. 7"
    ),
    DoctrineBlock(
        topic="Vector Norms",
        keywords=["vector norm", "p-norm", "norm", "linear algebra"],
        conclusion_template="The p-norm of vector v is ||v||_p = (sum |v_i|^p)^{1/p} for p ≥ 1.",
        reasoning_framework="""
        Vector norms generalize length:
        1. p-norm: ||v||_p = (sum |v_i|^p)^{1/p}.
        2. Common cases: p=1 (Manhattan), p=2 (Euclidean), p=∞ (max norm).
        Norms must satisfy positivity, homogeneity, triangle inequality.
        Used in analysis, optimization, and geometry.
        """,
        key_factors=["Positivity", "Homogeneity", "Triangle inequality"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show norm fails properties",
        counter_arguments=["Triangle inequality violation", "Negative norm"],
        resolution_strategy="Direct computation, property verification",
        entity_scope="Vectors in normed spaces",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 6"
    ),
    DoctrineBlock(
        topic="Trace of a Matrix",
        keywords=["trace", "matrix", "linear algebra", "sum"],
        conclusion_template="The trace of matrix A is the sum of its diagonal entries.",
        reasoning_framework="""
        To compute trace:
        1. Sum diagonal entries: trace(A) = sum A[i][i].
        Trace is invariant under similarity transformations.
        Used in eigenvalue analysis and matrix functions.
        """,
        key_factors=["Diagonal entries", "Similarity", "Invariance"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show incorrect sum or non-invariance",
        counter_arguments=["Incorrect computation", "Similarity error"],
        resolution_strategy="Direct computation, theoretical proof",
        entity_scope="Square matrices",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 5"
    ),
    DoctrineBlock(
        topic="Block Matrices",
        keywords=["block matrix", "matrix", "partition", "linear algebra"],
        conclusion_template="A block matrix is partitioned into submatrices, enabling structured operations.",
        reasoning_framework="""
        Block matrices are partitioned into rectangular submatrices.
        Operations (addition, multiplication) follow block structure.
        Used in simplifying computations and representing systems.
        Block diagonal, block triangular forms are common.
        """,
        key_factors=["Partition", "Submatrix", "Structured operations"],
        primary_authority=["Strang: Introduction to Linear Algebra", "Axler: Linear Algebra Done Right"],
        burden_holder="Proponent",
        adversary_position="Show operations fail block structure",
        counter_arguments=["Incorrect partition", "Operation error"],
        resolution_strategy="Direct computation, block analysis",
        entity_scope="Matrices",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Strang: Introduction to Linear Algebra, Ch. 3"
    ),
    DoctrineBlock(
        topic="Tensor Product of Vector Spaces",
        keywords=["tensor product", "vector space", "linear algebra", "multilinear"],
        conclusion_template="The tensor product V ⊗ W is a vector space capturing multilinear structure.",
        reasoning_framework="""
        Tensor product constructs V ⊗ W:
        1. Elements are formal sums of v ⊗ w.
        2. Operations are bilinear.
        Used in multilinear algebra, quantum mechanics, and geometry.
        """,
        key_factors=["Bilinearity", "Formal sums", "Multilinear structure"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show product fails bilinearity",
        counter_arguments=["Incorrect operation", "Non-bilinear"],
        resolution_strategy="Direct computation, property verification",
        entity_scope="Vector spaces",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 8"
    ),
    DoctrineBlock(
        topic="Minimal Polynomial",
        keywords=["minimal polynomial", "matrix", "linear algebra", "eigenvalue"],
        conclusion_template="The minimal polynomial of matrix A is the monic polynomial of least degree annihilating A.",
        reasoning_framework="""
        To find minimal polynomial:
        1. Find all polynomials p such that p(A) = 0.
        2. Choose monic polynomial of least degree.
        Used in structure analysis and Jordan form.
        """,
        key_factors=["Annihilation", "Degree", "Monic polynomial"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show polynomial does not annihilate A",
        counter_arguments=["Incorrect degree", "Non-monic"],
        resolution_strategy="Direct computation, polynomial analysis",
        entity_scope="Square matrices",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 8"
    ),
    DoctrineBlock(
        topic="Characteristic Polynomial",
        keywords=["characteristic polynomial", "matrix", "eigenvalue", "linear algebra"],
        conclusion_template="The characteristic polynomial of A is det(A - λI); roots are eigenvalues.",
        reasoning_framework="""
        To compute characteristic polynomial:
        1. Form matrix A - λI.
        2. Compute determinant: det(A - λI).
        3. Roots are eigenvalues.
        Used in spectral analysis and diagonalization.
        """,
        key_factors=["Determinant", "Eigenvalues", "Roots"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show roots not eigenvalues",
        counter_arguments=["Incorrect determinant", "Root mismatch"],
        resolution_strategy="Direct computation, root analysis",
        entity_scope="Square matrices",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 5"
    ),
    DoctrineBlock(
        topic="Matrix Exponential",
        keywords=["matrix exponential", "matrix", "linear algebra", "exponential"],
        conclusion_template="The matrix exponential exp(A) is sum_{k=0}^∞ (1/k!)A^k.",
        reasoning_framework="""
        Matrix exponential is defined via power series:
        1. exp(A) = sum_{k=0}^∞ (1/k!)A^k.
        2. Used in solving systems of differential equations.
        Computation may use diagonalization or Jordan form.
        """,
        key_factors=["Power series", "Convergence", "Diagonalization"],
        primary_authority=["Strang: Introduction to Linear Algebra", "Axler: Linear Algebra Done Right"],
        burden_holder="Proponent",
        adversary_position="Show series does not converge or incorrect computation",
        counter_arguments=["Non-convergent series", "Incorrect powers"],
        resolution_strategy="Direct computation, convergence analysis",
        entity_scope="Square matrices",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Strang: Introduction to Linear Algebra, Ch. 8"
    ),
    DoctrineBlock(
        topic="Matrix Similarity",
        keywords=["matrix similarity", "matrix", "linear algebra", "transformation"],
        conclusion_template="Matrices A and B are similar if there exists invertible P such that B = P^{-1}AP.",
        reasoning_framework="""
        To check similarity:
        1. Find invertible matrix P.
        2. Compute B = P^{-1}AP.
        Similar matrices have same characteristic polynomial, trace, and determinant.
        Used in classification and structure analysis.
        """,
        key_factors=["Invertibility", "Characteristic polynomial", "Preservation"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show no such P exists",
        counter_arguments=["Different invariants", "No invertible P"],
        resolution_strategy="Direct computation, invariant analysis",
        entity_scope="Square matrices",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 5"
    ),
    DoctrineBlock(
        topic="Idempotent Matrices",
        keywords=["idempotent matrix", "matrix", "linear algebra", "projection"],
        conclusion_template="A matrix A is idempotent if A^2 = A.",
        reasoning_framework="""
        To check idempotence:
        1. Compute A^2.
        2. If A^2 = A, matrix is idempotent.
        Used in projection and decomposition.
        """,
        key_factors=["Idempotence", "Projection", "Decomposition"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show A^2 ≠ A",
        counter_arguments=["Non-idempotent", "Incorrect computation"],
        resolution_strategy="Direct computation, property verification",
        entity_scope="Square matrices",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 6"
    ),
    DoctrineBlock(
        topic="Nilpotent Matrices",
        keywords=["nilpotent matrix", "matrix", "linear algebra", "power"],
        conclusion_template="A matrix A is nilpotent if A^k = 0 for some k ≥ 1.",
        reasoning_framework="""
        To check nilpotence:
        1. Compute powers A^k for increasing k.
        2. If A^k = 0 for some k, matrix is nilpotent.
        Used in Jordan form and structure analysis.
        """,
        key_factors=["Power", "Zero matrix", "Degree"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show no k exists with A^k = 0",
        counter_arguments=["Non-nilpotent", "Incorrect computation"],
        resolution_strategy="Direct computation, power analysis",
        entity_scope="Square matrices",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 8"
    ),
    DoctrineBlock(
        topic="Orthogonal Matrices",
        keywords=["orthogonal matrix", "matrix", "linear algebra", "transpose"],
        conclusion_template="A matrix Q is orthogonal if Q^T Q = I.",
        reasoning_framework="""
        To check orthogonality:
        1. Compute Q^T Q.
        2. If Q^T Q = I, Q is orthogonal.
        Orthogonal matrices preserve length and angles.
        Used in rotations and SVD.
        """,
        key_factors=["Transpose", "Identity matrix", "Preservation"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show Q^T Q ≠ I",
        counter_arguments=["Non-orthogonal", "Incorrect computation"],
        resolution_strategy="Direct computation, property verification",
        entity_scope="Square matrices",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 6"
    ),
    DoctrineBlock(
        topic="Hermitian Matrices",
        keywords=["Hermitian matrix", "matrix", "complex", "linear algebra"],
        conclusion_template="A matrix A is Hermitian if A = A^* (conjugate transpose).",
        reasoning_framework="""
        To check Hermitian property:
        1. Compute conjugate transpose A^*.
        2. Compare entries: A[i][j] = conjugate(A[j][i]).
        Hermitian matrices have real eigenvalues and orthogonal eigenvectors.
        Used in quantum mechanics and spectral analysis.
        """,
        key_factors=["Conjugate transpose", "Entry comparison", "Eigenvalues"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show A ≠ A^*",
        counter_arguments=["Non-Hermitian", "Incorrect computation"],
        resolution_strategy="Direct computation, entry analysis",
        entity_scope="Square matrices over complex fields",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 7"
    ),
    DoctrineBlock(
        topic="Unitary Matrices",
        keywords=["unitary matrix", "matrix", "complex", "linear algebra"],
        conclusion_template="A matrix U is unitary if U^* U = I.",
        reasoning_framework="""
        To check unitarity:
        1. Compute conjugate transpose U^*.
        2. Compute U^* U.
        3. If U^* U = I, U is unitary.
        Unitary matrices preserve length and angles in complex spaces.
        Used in quantum mechanics and SVD.
        """,
        key_factors=["Conjugate transpose", "Identity matrix", "Preservation"],
        primary_authority=["Axler: Linear Algebra Done Right", "Strang: Introduction to Linear Algebra"],
        burden_holder="Proponent",
        adversary_position="Show U^* U ≠ I",
        counter_arguments=["Non-unitary", "Incorrect computation"],
        resolution_strategy="Direct computation, property verification",
        entity_scope="Square matrices over complex fields",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Axler: Linear Algebra Done Right, Ch. 7"
    ),
    DoctrineBlock(
        topic="Matrix Rank Deficiency",
        keywords=["rank deficiency", "matrix", "rank", "linear algebra"],
        conclusion_template="A matrix is rank deficient if rank(A) < min(m, n) for m x n matrix.",
        reasoning_framework="""
        To check rank deficiency:
        1. Compute rank(A).
        2. Compare to min(m, n).
        3. If rank(A) < min(m, n), matrix is rank deficient.
        Used in analyzing solution spaces and redundancy.
        """,
        key_factors=["Rank", "Dimension", "Redundancy"],
        primary_authority=["Strang: Introduction to Linear Algebra", "Axler: Linear Algebra Done Right"],
        burden_holder="Proponent",
        adversary_position="Show rank equals min(m, n)",
        counter_arguments=["Full rank", "Incorrect computation"],
        resolution_strategy="Direct computation, rank analysis",
        entity_scope="Matrices",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Strang: Introduction to Linear Algebra, Ch. 3"
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
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in k.lower() for k in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]