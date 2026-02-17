from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

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
        topic="Fundamental Theorem of Arithmetic",
        keywords=["prime factorization", "unique factorization", "number theory", "integers", "primes"],
        conclusion_template="Every integer greater than 1 can be uniquely represented as a product of prime numbers, up to the order of the factors.",
        reasoning_framework=(
            "The Fundamental Theorem of Arithmetic asserts that the set of prime numbers forms the building blocks of all positive integers. "
            "The proof proceeds by induction: for the base case, 2 is prime. For n > 2, if n is prime, it is its own factorization. "
            "If n is composite, it can be written as a product of smaller integers, each of which can be factored into primes by the inductive hypothesis. "
            "Uniqueness is shown by contradiction: suppose two distinct prime factorizations exist, then a prime in one factorization must divide the product of primes in the other, "
            "which is only possible if it equals one of those primes, contradicting distinctness. "
            "This theorem is foundational for all further results in number theory, including divisibility, greatest common divisors, and arithmetic functions."
        ),
        key_factors=["Existence of prime factorization", "Uniqueness up to order", "Inductive proof", "Contradiction argument"],
        primary_authority=["Euclid's Elements", "Gauss's Disquisitiones Arithmeticae", "Modern algebraic texts"],
        burden_holder="Proponent of unique factorization",
        adversary_position="Existence of non-unique factorization in integers",
        counter_arguments=[
            "Non-unique factorization occurs only in certain algebraic structures, not in the integers.",
            "Counterexamples exist in some rings, but not in Z."
        ],
        resolution_strategy="Apply proof by induction and contradiction to establish uniqueness in Z.",
        entity_scope="Positive integers greater than 1",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Euclid's Elements, Book VII, Proposition 30"
    ),
    DoctrineBlock(
        topic="Primality Test",
        keywords=["prime test", "primality", "algorithm", "number theory", "composite", "probabilistic", "deterministic"],
        conclusion_template="Given a positive integer n, determine whether n is prime or composite using an appropriate primality test.",
        reasoning_framework=(
            "Primality testing is the process of determining whether a given integer n > 1 is prime. "
            "Classical methods include trial division up to sqrt(n), which is inefficient for large n. "
            "Modern algorithms include the Miller-Rabin probabilistic test, which relies on properties of modular exponentiation, "
            "and the deterministic AKS primality test, which runs in polynomial time. "
            "The choice of test depends on the size of n and the required certainty. Probabilistic tests are faster but may yield false positives, "
            "while deterministic tests guarantee correctness. "
            "For cryptographic applications, probabilistic tests are often used with multiple rounds to reduce error probability."
        ),
        key_factors=["Algorithm efficiency", "Error probability", "Size of n", "Certainty requirement"],
        primary_authority=["Miller-Rabin (1976)", "AKS (2002)", "Gauss's primality criteria"],
        burden_holder="Tester asserting primality",
        adversary_position="Claim that n is composite",
        counter_arguments=[
            "Probabilistic tests can yield pseudoprimes.",
            "Composite numbers can pass some rounds of Miller-Rabin."
        ],
        resolution_strategy="Use multiple rounds of probabilistic tests or deterministic algorithms for certainty.",
        entity_scope="Positive integers greater than 1",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Miller-Rabin, AKS Primality Test"
    ),
    DoctrineBlock(
        topic="Prime Factorization (FTA)",
        keywords=["prime factorization", "unique factorization", "decomposition", "number theory", "integers"],
        conclusion_template="Given a positive integer n, find its unique prime factorization.",
        reasoning_framework=(
            "Prime factorization is the process of decomposing an integer n > 1 into a product of prime numbers. "
            "By the Fundamental Theorem of Arithmetic, this factorization is unique up to the order of the factors. "
            "Algorithms for factorization include trial division, Fermat's method, Pollard's rho algorithm, and the quadratic sieve. "
            "Trial division is practical for small n; advanced algorithms are required for large n, especially in cryptographic contexts. "
            "The uniqueness of factorization underpins many results in number theory, including the computation of arithmetic functions and the study of divisibility."
        ),
        key_factors=["Existence and uniqueness", "Algorithmic efficiency", "Size of n", "Factorization method"],
        primary_authority=["Euclid's Elements", "Modern computational methods"],
        burden_holder="Factorizer asserting uniqueness",
        adversary_position="Existence of multiple distinct factorizations",
        counter_arguments=[
            "Non-unique factorization occurs only in non-UFDs, not in Z.",
            "Advanced algorithms may fail for very large n."
        ],
        resolution_strategy="Apply efficient algorithms and verify uniqueness.",
        entity_scope="Positive integers greater than 1",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Fundamental Theorem of Arithmetic"
    ),
    DoctrineBlock(
        topic="Euler's Totient Function",
        keywords=["totient", "phi function", "coprime", "number theory", "arithmetic function"],
        conclusion_template="For a positive integer n, Euler's totient function φ(n) counts the number of positive integers less than n that are coprime to n.",
        reasoning_framework=(
            "Euler's totient function φ(n) is defined as the number of integers k with 1 ≤ k < n such that gcd(k, n) = 1. "
            "The function is multiplicative: if m and n are coprime, then φ(mn) = φ(m)φ(n). "
            "For a prime p, φ(p) = p - 1. For n = p1^a1 * ... * pk^ak, φ(n) = n * Π(1 - 1/pi) over all distinct primes pi dividing n. "
            "The totient function is central to Euler's theorem: for any integer a coprime to n, a^φ(n) ≡ 1 mod n. "
            "Applications include RSA cryptography, modular arithmetic, and group theory."
        ),
        key_factors=["Definition", "Multiplicativity", "Prime power formula", "Coprimality"],
        primary_authority=["Euler's theorem", "Gauss's Disquisitiones Arithmeticae"],
        burden_holder="Proponent of totient properties",
        adversary_position="Claim that φ(n) is not multiplicative",
        counter_arguments=[
            "Multiplicativity fails if m and n are not coprime.",
            "Incorrect application of prime power formula."
        ],
        resolution_strategy="Verify coprimality and apply prime power formula.",
        entity_scope="Positive integers",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Euler's theorem"
    ),
    DoctrineBlock(
        topic="Chinese Remainder Theorem",
        keywords=["CRT", "modular arithmetic", "congruence", "number theory", "coprime moduli"],
        conclusion_template="Given a system of congruences with pairwise coprime moduli, there exists a unique solution modulo the product of the moduli.",
        reasoning_framework=(
            "The Chinese Remainder Theorem states that for integers n1, ..., nk that are pairwise coprime, and integers a1, ..., ak, "
            "the system x ≡ ai mod ni has a unique solution modulo N = n1 * ... * nk. "
            "The proof constructs the solution explicitly using the method of successive substitutions or via the construction x = Σ ai * Ni * yi, "
            "where Ni = N/ni and yi is the modular inverse of Ni modulo ni. "
            "CRT is fundamental in modular arithmetic, cryptography, and computational number theory. "
            "The theorem generalizes to non-coprime moduli with appropriate conditions, but uniqueness may fail."
        ),
        key_factors=["Pairwise coprimality", "Existence and uniqueness", "Explicit construction", "Modular inverses"],
        primary_authority=["Sun Zi Suan Jing", "Gauss's Disquisitiones Arithmeticae"],
        burden_holder="Proponent of CRT solution",
        adversary_position="Claim that no unique solution exists",
        counter_arguments=[
            "Moduli are not coprime; uniqueness fails.",
            "Incorrect computation of modular inverses."
        ],
        resolution_strategy="Verify coprimality and construct solution explicitly.",
        entity_scope="Integers modulo N",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gauss's Disquisitiones Arithmeticae"
    ),
    DoctrineBlock(
        topic="General Number Theory Query",
        keywords=["number theory", "query", "integers", "primes", "arithmetic"],
        conclusion_template="Apply relevant number theory doctrines to answer the query based on established principles.",
        reasoning_framework=(
            "General number theory queries require identification of the relevant doctrine, such as divisibility, primality, factorization, or modular arithmetic. "
            "The approach is to analyze the query, determine which theorem or principle applies, and apply it rigorously. "
            "If no direct doctrine applies, attempt to reduce the query to known results or construct a proof using established methods. "
            "Consult authoritative sources and precedents for guidance."
        ),
        key_factors=["Doctrine identification", "Reduction to known results", "Proof construction", "Authoritative sources"],
        primary_authority=["Euclid's Elements", "Gauss's Disquisitiones Arithmeticae", "Modern texts"],
        burden_holder="Query responder",
        adversary_position="Claim that doctrine does not apply",
        counter_arguments=[
            "Doctrine misapplied.",
            "Query falls outside established principles."
        ],
        resolution_strategy="Clarify scope and apply relevant doctrine.",
        entity_scope="Integers and arithmetic structures",
        confidence=0.90,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Standard number theory texts"
    ),
    DoctrineBlock(
        topic="Divisibility in Integers",
        keywords=["divisibility", "integer", "number theory", "gcd", "prime"],
        conclusion_template="An integer a divides b if and only if there exists an integer k such that b = ak.",
        reasoning_framework=(
            "Divisibility is a fundamental relation in number theory. For integers a and b, a divides b if b = ak for some integer k. "
            "Properties include: if a divides b and b divides c, then a divides c; if a divides b and a divides c, then a divides b + c. "
            "Divisibility is used to define prime numbers, greatest common divisors, and is central to many proofs."
        ),
        key_factors=["Definition", "Transitivity", "Additivity", "Relation to primes"],
        primary_authority=["Euclid's Elements", "Modern algebraic texts"],
        burden_holder="Proponent of divisibility",
        adversary_position="Claim that a does not divide b",
        counter_arguments=[
            "No integer k exists.",
            "Misapplication of divisibility properties."
        ],
        resolution_strategy="Construct explicit k or apply divisibility properties.",
        entity_scope="Integers",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Euclid's Elements"
    ),
    DoctrineBlock(
        topic="Greatest Common Divisor (GCD)",
        keywords=["gcd", "greatest common divisor", "number theory", "euclidean algorithm"],
        conclusion_template="The greatest common divisor of integers a and b is the largest integer d such that d divides both a and b.",
        reasoning_framework=(
            "The GCD of a and b, denoted gcd(a, b), is the largest integer dividing both. "
            "The Euclidean algorithm computes gcd efficiently: repeatedly replace (a, b) with (b, a mod b) until b = 0; the last nonzero a is the gcd. "
            "GCD is used in simplifying fractions, solving Diophantine equations, and in modular arithmetic."
        ),
        key_factors=["Definition", "Euclidean algorithm", "Divisibility", "Applications"],
        primary_authority=["Euclid's Elements", "Modern computational texts"],
        burden_holder="Proponent of GCD value",
        adversary_position="Claim that another integer is greater and divides both",
        counter_arguments=[
            "Incorrect computation of GCD.",
            "Existence of larger common divisor."
        ],
        resolution_strategy="Apply Euclidean algorithm and verify divisibility.",
        entity_scope="Integers",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Euclid's Elements"
    ),
    DoctrineBlock(
        topic="Least Common Multiple (LCM)",
        keywords=["lcm", "least common multiple", "number theory", "multiples", "gcd"],
        conclusion_template="The least common multiple of integers a and b is the smallest positive integer m such that both a and b divide m.",
        reasoning_framework=(
            "LCM is defined as the smallest positive integer divisible by both a and b. "
            "It can be computed using the formula lcm(a, b) = |ab| / gcd(a, b). "
            "LCM is used in solving equations involving multiples, synchronizing periodic events, and in number theoretic functions."
        ),
        key_factors=["Definition", "Relation to GCD", "Computation formula", "Applications"],
        primary_authority=["Euclid's Elements", "Modern algebraic texts"],
        burden_holder="Proponent of LCM value",
        adversary_position="Claim that another integer is smaller and divisible by both",
        counter_arguments=[
            "Incorrect computation of LCM.",
            "Existence of smaller common multiple."
        ],
        resolution_strategy="Apply formula and verify divisibility.",
        entity_scope="Positive integers",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Euclid's Elements"
    ),
    DoctrineBlock(
        topic="Euclidean Algorithm",
        keywords=["euclidean algorithm", "gcd", "number theory", "algorithm", "integers"],
        conclusion_template="The Euclidean algorithm computes the greatest common divisor of two integers efficiently.",
        reasoning_framework=(
            "The Euclidean algorithm is an iterative process for finding the GCD of two integers a and b. "
            "At each step, replace (a, b) with (b, a mod b) until b = 0. The last nonzero a is the GCD. "
            "The algorithm is efficient, running in logarithmic time relative to the size of the inputs. "
            "It forms the basis for many number theoretic algorithms, including solving linear Diophantine equations."
        ),
        key_factors=["Iterative process", "Efficiency", "Termination", "Basis for other algorithms"],
        primary_authority=["Euclid's Elements", "Modern computational texts"],
        burden_holder="Proponent of algorithm correctness",
        adversary_position="Claim that algorithm does not terminate or gives incorrect result",
        counter_arguments=[
            "Incorrect implementation.",
            "Inputs not integers."
        ],
        resolution_strategy="Verify implementation and input types.",
        entity_scope="Integers",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Euclid's Elements"
    ),
    DoctrineBlock(
        topic="Modular Arithmetic",
        keywords=["modular arithmetic", "congruence", "number theory", "modulo", "integers"],
        conclusion_template="For integers a, b, and n, a ≡ b mod n if n divides (a - b).",
        reasoning_framework=(
            "Modular arithmetic studies arithmetic operations under equivalence classes modulo n. "
            "a ≡ b mod n means n divides (a - b). Addition, subtraction, and multiplication are well-defined modulo n. "
            "Applications include cryptography, coding theory, and solving congruences."
        ),
        key_factors=["Definition", "Well-defined operations", "Applications", "Equivalence classes"],
        primary_authority=["Gauss's Disquisitiones Arithmeticae", "Modern texts"],
        burden_holder="Proponent of congruence",
        adversary_position="Claim that a and b are not congruent modulo n",
        counter_arguments=[
            "Incorrect computation of (a - b).",
            "Misapplication of modulo operation."
        ],
        resolution_strategy="Compute (a - b) and verify divisibility by n.",
        entity_scope="Integers modulo n",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gauss's Disquisitiones Arithmeticae"
    ),
    DoctrineBlock(
        topic="Fermat's Little Theorem",
        keywords=["fermat's little theorem", "primes", "modular arithmetic", "number theory"],
        conclusion_template="If p is prime and a is not divisible by p, then a^(p-1) ≡ 1 mod p.",
        reasoning_framework=(
            "Fermat's Little Theorem states that for any integer a not divisible by prime p, a^(p-1) ≡ 1 mod p. "
            "The proof uses properties of modular arithmetic and the fact that the set {a, 2a, ..., (p-1)a} modulo p is a permutation of {1, ..., p-1}. "
            "This theorem is used in primality testing and cryptography."
        ),
        key_factors=["Prime modulus", "Non-divisibility", "Permutation argument", "Applications"],
        primary_authority=["Fermat's correspondence", "Gauss's Disquisitiones Arithmeticae"],
        burden_holder="Proponent of theorem",
        adversary_position="Claim that congruence does not hold",
        counter_arguments=[
            "a is divisible by p.",
            "p is not prime."
        ],
        resolution_strategy="Verify conditions and apply theorem.",
        entity_scope="Integers modulo p",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Fermat's correspondence"
    ),
    DoctrineBlock(
        topic="Fermat's Factorization Method",
        keywords=["fermat's factorization", "factorization", "number theory", "algorithm"],
        conclusion_template="Fermat's factorization expresses n as a difference of squares: n = a^2 - b^2.",
        reasoning_framework=(
            "Fermat's factorization method is based on expressing n as a^2 - b^2 = (a + b)(a - b). "
            "For odd n, search for integers a ≥ sqrt(n) such that a^2 - n is a perfect square. "
            "This method is efficient for numbers with factors close together."
        ),
        key_factors=["Difference of squares", "Perfect squares", "Efficiency", "Applicability"],
        primary_authority=["Fermat's correspondence", "Modern texts"],
        burden_holder="Factorizer",
        adversary_position="Claim that n cannot be expressed as difference of squares",
        counter_arguments=[
            "Factors not close together.",
            "No suitable a found."
        ],
        resolution_strategy="Apply method and verify result.",
        entity_scope="Odd integers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Fermat's correspondence"
    ),
    DoctrineBlock(
        topic="Pollard's Rho Algorithm",
        keywords=["pollard's rho", "factorization", "number theory", "algorithm", "primes"],
        conclusion_template="Pollard's rho algorithm finds a nontrivial factor of composite n using pseudorandom sequences.",
        reasoning_framework=(
            "Pollard's rho algorithm uses pseudorandom sequences and cycle detection to find a nontrivial factor of n. "
            "The method iterates x_{i+1} = f(x_i) mod n, typically f(x) = x^2 + 1. "
            "When gcd(|x_i - x_j|, n) > 1 for some i, j, a factor is found. "
            "The algorithm is efficient for numbers with small factors."
        ),
        key_factors=["Pseudorandom sequence", "Cycle detection", "GCD computation", "Efficiency"],
        primary_authority=["Pollard (1975)", "Modern computational texts"],
        burden_holder="Factorizer",
        adversary_position="Claim that algorithm fails to find factor",
        counter_arguments=[
            "Factors are large.",
            "Sequence does not cycle."
        ],
        resolution_strategy="Adjust parameters or use alternative methods.",
        entity_scope="Composite integers",
        confidence=0.93,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Pollard (1975)"
    ),
    DoctrineBlock(
        topic="Quadratic Sieve",
        keywords=["quadratic sieve", "factorization", "number theory", "algorithm"],
        conclusion_template="The quadratic sieve is an efficient algorithm for factoring large integers.",
        reasoning_framework=(
            "The quadratic sieve is based on finding numbers x such that x^2 mod n is smooth (has only small prime factors). "
            "Collecting enough such relations allows construction of a congruence of squares, leading to factorization. "
            "The algorithm is efficient for integers up to 100 digits."
        ),
        key_factors=["Smooth numbers", "Congruence of squares", "Relation collection", "Efficiency"],
        primary_authority=["Pomerance (1981)", "Modern computational texts"],
        burden_holder="Factorizer",
        adversary_position="Claim that algorithm is inefficient or fails",
        counter_arguments=[
            "n is too large.",
            "Insufficient smooth relations."
        ],
        resolution_strategy="Increase factor base or use alternative methods.",
        entity_scope="Large composite integers",
        confidence=0.91,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Pomerance (1981)"
    ),
    DoctrineBlock(
        topic="Miller-Rabin Primality Test",
        keywords=["miller-rabin", "primality test", "probabilistic", "number theory", "algorithm"],
        conclusion_template="The Miller-Rabin test probabilistically determines whether n is composite or likely prime.",
        reasoning_framework=(
            "The Miller-Rabin test decomposes n-1 as 2^s * d and tests whether a^d ≡ 1 mod n or a^{2^r d} ≡ -1 mod n for some r. "
            "If neither holds for a randomly chosen base a, n is composite. "
            "Multiple rounds reduce error probability. "
            "The test is efficient and widely used in practice."
        ),
        key_factors=["Decomposition", "Witness selection", "Error probability", "Efficiency"],
        primary_authority=["Miller (1976)", "Rabin (1980)", "Modern texts"],
        burden_holder="Tester",
        adversary_position="Claim that n is composite despite passing test",
        counter_arguments=[
            "Existence of pseudoprimes.",
            "Insufficient rounds."
        ],
        resolution_strategy="Increase rounds or use deterministic test.",
        entity_scope="Positive integers",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Miller (1976), Rabin (1980)"
    ),
    DoctrineBlock(
        topic="AKS Primality Test",
        keywords=["aks", "primality test", "deterministic", "number theory", "algorithm"],
        conclusion_template="The AKS algorithm determines primality in polynomial time for any integer n.",
        reasoning_framework=(
            "The AKS primality test checks whether (x + a)^n ≡ x^n + a mod n for all a and x. "
            "If n passes all checks, it is prime. "
            "The algorithm runs in polynomial time and is deterministic, guaranteeing correctness."
        ),
        key_factors=["Polynomial time", "Deterministic", "Congruence checks", "Correctness"],
        primary_authority=["Agrawal, Kayal, Saxena (2002)", "Modern texts"],
        burden_holder="Tester",
        adversary_position="Claim that n is composite despite passing test",
        counter_arguments=[
            "Incorrect implementation.",
            "Algorithm not applied fully."
        ],
        resolution_strategy="Verify implementation and completeness.",
        entity_scope="Positive integers",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Agrawal, Kayal, Saxena (2002)"
    ),
    DoctrineBlock(
        topic="Prime Number Theorem",
        keywords=["prime number theorem", "distribution", "primes", "number theory"],
        conclusion_template="The number of primes less than n is approximately n / log n.",
        reasoning_framework=(
            "The Prime Number Theorem describes the asymptotic distribution of primes: π(n) ~ n / log n as n → ∞. "
            "Proofs use complex analysis, particularly properties of the Riemann zeta function. "
            "The theorem provides estimates for the density of primes and is fundamental in analytic number theory."
        ),
        key_factors=["Asymptotic behavior", "Density", "Complex analysis", "Riemann zeta function"],
        primary_authority=["Hadamard (1896)", "de la Vallée Poussin (1896)", "Modern analytic texts"],
        burden_holder="Proponent of theorem",
        adversary_position="Claim that primes are more/less dense",
        counter_arguments=[
            "Finite n deviates from asymptotic estimate.",
            "Non-analytic proofs."
        ],
        resolution_strategy="Apply theorem for large n.",
        entity_scope="Positive integers",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Hadamard (1896), de la Vallée Poussin (1896)"
    ),
    DoctrineBlock(
        topic="Goldbach's Conjecture",
        keywords=["goldbach's conjecture", "even numbers", "primes", "number theory"],
        conclusion_template="Every even integer greater than 2 can be expressed as the sum of two primes.",
        reasoning_framework=(
            "Goldbach's Conjecture asserts that every even integer > 2 is the sum of two primes. "
            "Extensive computational evidence supports the conjecture, but no general proof exists. "
            "Partial results include the weak Goldbach conjecture and results for large n."
        ),
        key_factors=["Even integers", "Sum of primes", "Computational evidence", "Partial results"],
        primary_authority=["Goldbach (1742)", "Modern computational studies"],
        burden_holder="Proponent of conjecture",
        adversary_position="Claim that counterexample exists",
        counter_arguments=[
            "No proof for all n.",
            "Conjecture unproven."
        ],
        resolution_strategy="Provide computational evidence and partial results.",
        entity_scope="Even integers > 2",
        confidence=0.80,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Goldbach (1742)"
    ),
    DoctrineBlock(
        topic="Twin Prime Conjecture",
        keywords=["twin primes", "conjecture", "primes", "number theory"],
        conclusion_template="There are infinitely many pairs of primes p and p+2.",
        reasoning_framework=(
            "The Twin Prime Conjecture posits the existence of infinitely many pairs of primes differing by 2. "
            "Partial results include bounded gaps between primes (Zhang, 2013) and extensive computational evidence. "
            "No general proof exists."
        ),
        key_factors=["Prime pairs", "Bounded gaps", "Computational evidence", "Partial results"],
        primary_authority=["Zhang (2013)", "Goldbach (1742)", "Modern texts"],
        burden_holder="Proponent of conjecture",
        adversary_position="Claim that only finitely many twin primes exist",
        counter_arguments=[
            "Conjecture unproven.",
            "No proof for infinitude."
        ],
        resolution_strategy="Provide partial results and computational evidence.",
        entity_scope="Positive integers",
        confidence=0.75,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Zhang (2013)"
    ),
    DoctrineBlock(
        topic="Dirichlet's Theorem on Primes in Arithmetic Progression",
        keywords=["dirichlet's theorem", "arithmetic progression", "primes", "number theory"],
        conclusion_template="Every arithmetic progression a, a+d, a+2d, ... with gcd(a, d) = 1 contains infinitely many primes.",
        reasoning_framework=(
            "Dirichlet's theorem states that any arithmetic progression with first term a and difference d, where gcd(a, d) = 1, "
            "contains infinitely many primes. "
            "The proof uses Dirichlet L-functions and analytic methods."
        ),
        key_factors=["Arithmetic progression", "Coprimality", "Analytic methods", "Infinitude"],
        primary_authority=["Dirichlet (1837)", "Modern analytic texts"],
        burden_holder="Proponent of theorem",
        adversary_position="Claim that only finitely many primes exist in progression",
        counter_arguments=[
            "Progression does not satisfy coprimality.",
            "Conjecture unproven for specific cases."
        ],
        resolution_strategy="Verify coprimality and apply analytic methods.",
        entity_scope="Positive integers",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Dirichlet (1837)"
    ),
    DoctrineBlock(
        topic="Legendre Symbol",
        keywords=["legendre symbol", "quadratic residue", "modular arithmetic", "number theory"],
        conclusion_template="The Legendre symbol (a/p) indicates whether a is a quadratic residue modulo prime p.",
        reasoning_framework=(
            "The Legendre symbol (a/p) is defined as 1 if a is a quadratic residue modulo p, -1 if not, and 0 if p divides a. "
            "Properties include multiplicativity and relation to quadratic reciprocity."
        ),
        key_factors=["Quadratic residues", "Prime modulus", "Multiplicativity", "Reciprocity"],
        primary_authority=["Legendre (1798)", "Gauss's Disquisitiones Arithmeticae"],
        burden_holder="Proponent of symbol value",
        adversary_position="Claim that a is not a quadratic residue",
        counter_arguments=[
            "Incorrect computation.",
            "a divisible by p."
        ],
        resolution_strategy="Apply definition and reciprocity laws.",
        entity_scope="Integers modulo p",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Legendre (1798)"
    ),
    DoctrineBlock(
        topic="Quadratic Reciprocity",
        keywords=["quadratic reciprocity", "legendre symbol", "number theory", "primes"],
        conclusion_template="Quadratic reciprocity relates the solvability of x^2 ≡ p mod q and x^2 ≡ q mod p for distinct odd primes p and q.",
        reasoning_framework=(
            "Quadratic reciprocity states that for distinct odd primes p and q, "
            "(p/q)(q/p) = (-1)^{((p-1)/2)((q-1)/2)}. "
            "The law enables computation of quadratic residues and is central to number theory."
        ),
        key_factors=["Odd primes", "Legendre symbol", "Residue computation", "Reciprocity law"],
        primary_authority=["Gauss's Disquisitiones Arithmeticae", "Modern texts"],
        burden_holder="Proponent of reciprocity law",
        adversary_position="Claim that law does not hold",
        counter_arguments=[
            "Primes not odd.",
            "Incorrect computation."
        ],
        resolution_strategy="Verify conditions and apply law.",
        entity_scope="Odd primes",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gauss's Disquisitiones Arithmeticae"
    ),
    DoctrineBlock(
        topic="Möbius Function",
        keywords=["möbius function", "arithmetic function", "number theory", "multiplicativity"],
        conclusion_template="The Möbius function μ(n) is defined as 0 if n has a squared prime factor, 1 if n=1, and (-1)^k if n is a product of k distinct primes.",
        reasoning_framework=(
            "The Möbius function μ(n) is used in inversion formulas and analytic number theory. "
            "It is multiplicative and central to the Möbius inversion formula, which relates arithmetic functions."
        ),
        key_factors=["Definition", "Multiplicativity", "Inversion formula", "Prime factorization"],
        primary_authority=["Möbius (1832)", "Modern analytic texts"],
        burden_holder="Proponent of function value",
        adversary_position="Claim that μ(n) is incorrectly computed",
        counter_arguments=[
            "n has squared prime factor.",
            "Incorrect factorization."
        ],
        resolution_strategy="Factor n and apply definition.",
        entity_scope="Positive integers",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Möbius (1832)"
    ),
    DoctrineBlock(
        topic="Perfect Numbers",
        keywords=["perfect numbers", "divisors", "number theory", "sum of divisors"],
        conclusion_template="A perfect number is an integer equal to the sum of its proper divisors.",
        reasoning_framework=(
            "Perfect numbers are integers n such that σ(n) = 2n, where σ(n) is the sum of divisors function. "
            "Even perfect numbers are characterized by Euclid's formula: n = 2^{p-1}(2^p - 1) for prime p where 2^p - 1 is prime (Mersenne prime). "
            "Odd perfect numbers are unproven to exist."
        ),
        key_factors=["Sum of divisors", "Euclid's formula", "Mersenne primes", "Existence"],
        primary_authority=["Euclid's Elements", "Modern texts"],
        burden_holder="Proponent of perfect number",
        adversary_position="Claim that n is not perfect",
        counter_arguments=[
            "Incorrect divisor sum.",
            "n not of Euclid's form."
        ],
        resolution_strategy="Compute sum of divisors and verify form.",
        entity_scope="Positive integers",
        confidence=0.93,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Euclid's Elements"
    ),
    DoctrineBlock(
        topic="Amicable Numbers",
        keywords=["amicable numbers", "divisors", "number theory", "sum of divisors"],
        conclusion_template="A pair of numbers (a, b) is amicable if the sum of proper divisors of a equals b and vice versa.",
        reasoning_framework=(
            "Amicable numbers are pairs (a, b) such that σ(a) - a = b and σ(b) - b = a. "
            "The concept dates to Pythagoras and has been studied for centuries. "
            "Algorithms exist for finding amicable pairs."
        ),
        key_factors=["Sum of divisors", "Pair relation", "Algorithms", "Historical context"],
        primary_authority=["Pythagoras", "Modern texts"],
        burden_holder="Proponent of amicable pair",
        adversary_position="Claim that pair is not amicable",
        counter_arguments=[
            "Incorrect divisor sums.",
            "Pair does not satisfy relation."
        ],
        resolution_strategy="Compute divisor sums and verify relation.",
        entity_scope="Positive integers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Pythagoras"
    ),
    DoctrineBlock(
        topic="Diophantine Equations",
        keywords=["diophantine equations", "integer solutions", "number theory", "equations"],
        conclusion_template="A Diophantine equation is an equation seeking integer solutions.",
        reasoning_framework=(
            "Diophantine equations are equations where integer solutions are sought. "
            "Methods include modular arithmetic, factorization, and the use of GCD. "
            "Some equations are solvable, others are not; Hilbert's tenth problem shows no general algorithm exists."
        ),
        key_factors=["Integer solutions", "Methods", "Solvability", "Hilbert's tenth problem"],
        primary_authority=["Diophantus", "Hilbert", "Modern texts"],
        burden_holder="Proponent of solution existence",
        adversary_position="Claim that no integer solution exists",
        counter_arguments=[
            "Equation unsolvable.",
            "Incorrect application of methods."
        ],
        resolution_strategy="Apply methods and check solvability.",
        entity_scope="Integers",
        confidence=0.90,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Hilbert's tenth problem"
    ),
    DoctrineBlock(
        topic="Pythagorean Triples",
        keywords=["pythagorean triples", "diophantine equations", "number theory", "right triangles"],
        conclusion_template="A Pythagorean triple (a, b, c) satisfies a^2 + b^2 = c^2 with integer values.",
        reasoning_framework=(
            "Pythagorean triples are integer solutions to a^2 + b^2 = c^2. "
            "Primitive triples are generated by a = m^2 - n^2, b = 2mn, c = m^2 + n^2 for integers m > n > 0. "
            "All triples are multiples of primitive ones."
        ),
        key_factors=["Equation", "Primitive generation", "Multiples", "Integer values"],
        primary_authority=["Euclid's Elements", "Modern texts"],
        burden_holder="Proponent of triple",
        adversary_position="Claim that triple is not integer solution",
        counter_arguments=[
            "Incorrect values.",
            "Not primitive."
        ],
        resolution_strategy="Verify values and primitive status.",
        entity_scope="Positive integers",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Euclid's Elements"
    ),
    DoctrineBlock(
        topic="RSA Cryptosystem",
        keywords=["rsa", "cryptography", "number theory", "primes", "modular arithmetic"],
        conclusion_template="RSA relies on the difficulty of factoring large integers and properties of Euler's totient function.",
        reasoning_framework=(
            "RSA cryptosystem uses two large primes p and q to form modulus n = pq. "
            "Public and private keys are generated using Euler's totient function φ(n). "
            "Security relies on the difficulty of factoring n."
        ),
        key_factors=["Prime generation", "Totient function", "Factorization difficulty", "Key generation"],
        primary_authority=["Rivest, Shamir, Adleman (1977)", "Modern cryptographic texts"],
        burden_holder="Cryptographer",
        adversary_position="Claim that system is insecure",
        counter_arguments=[
            "Small primes used.",
            "Factorization algorithms improve."
        ],
        resolution_strategy="Use large primes and monitor algorithmic advances.",
        entity_scope="Integers modulo n",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Rivest, Shamir, Adleman (1977)"
    ),
    DoctrineBlock(
        topic="Primitive Roots",
        keywords=["primitive roots", "modular arithmetic", "number theory", "multiplicative order"],
        conclusion_template="A primitive root modulo n is an integer g such that its powers generate all units modulo n.",
        reasoning_framework=(
            "Primitive roots exist for prime moduli and certain composite moduli. "
            "g is a primitive root modulo n if its multiplicative order is φ(n). "
            "Applications include cryptography and discrete logarithms."
        ),
        key_factors=["Existence", "Order", "Generation", "Applications"],
        primary_authority=["Gauss's Disquisitiones Arithmeticae", "Modern texts"],
        burden_holder="Proponent of primitive root",
        adversary_position="Claim that g is not primitive root",
        counter_arguments=[
            "Order less than φ(n).",
            "n does not admit primitive roots."
        ],
        resolution_strategy="Compute order and verify existence.",
        entity_scope="Integers modulo n",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gauss's Disquisitiones Arithmeticae"
    ),
    DoctrineBlock(
        topic="Order of an Element Modulo n",
        keywords=["order", "modular arithmetic", "number theory", "multiplicative order"],
        conclusion_template="The order of a modulo n is the smallest positive integer k such that a^k ≡ 1 mod n.",
        reasoning_framework=(
            "Order is fundamental in group theory and modular arithmetic. "
            "It determines cyclicity and is used in cryptographic algorithms."
        ),
        key_factors=["Definition", "Cyclicity", "Applications", "Computation"],
        primary_authority=["Modern algebraic texts"],
        burden_holder="Proponent of order value",
        adversary_position="Claim that k is not minimal",
        counter_arguments=[
            "Incorrect computation.",
            "a not coprime to n."
        ],
        resolution_strategy="Verify coprimality and compute powers.",
        entity_scope="Integers modulo n",
        confidence=0.93,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Modern algebraic texts"
    ),
    DoctrineBlock(
        topic="Multiplicative Group Modulo n",
        keywords=["multiplicative group", "modular arithmetic", "number theory", "group theory"],
        conclusion_template="The set of integers coprime to n forms a multiplicative group modulo n.",
        reasoning_framework=(
            "The multiplicative group modulo n consists of integers 1 ≤ a < n with gcd(a, n) = 1. "
            "The group has order φ(n) and is cyclic for certain n."
        ),
        key_factors=["Coprimality", "Group structure", "Order", "Cyclicity"],
        primary_authority=["Modern algebraic texts"],
        burden_holder="Proponent of group structure",
        adversary_position="Claim that set is not a group",
        counter_arguments=[
            "Set not closed under multiplication.",
            "Non-coprime elements included."
        ],
        resolution_strategy="Verify coprimality and closure.",
        entity_scope="Integers modulo n",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Modern algebraic texts"
    ),
    DoctrineBlock(
        topic="Wilson's Theorem",
        keywords=["wilson's theorem", "primes", "factorial", "modular arithmetic"],
        conclusion_template="An integer p > 1 is prime if and only if (p-1)! ≡ -1 mod p.",
        reasoning_framework=(
            "Wilson's theorem states that (p-1)! ≡ -1 mod p if and only if p is prime. "
            "The proof uses properties of modular arithmetic and permutation of residues."
        ),
        key_factors=["Factorial", "Prime modulus", "Congruence", "Proof"],
        primary_authority=["Wilson (1771)", "Gauss's Disquisitiones Arithmeticae"],
        burden_holder="Proponent of theorem",
        adversary_position="Claim that congruence does not hold",
        counter_arguments=[
            "p not prime.",
            "Incorrect computation."
        ],
        resolution_strategy="Verify primality and compute factorial.",
        entity_scope="Positive integers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Wilson (1771)"
    ),
    DoctrineBlock(
        topic="Sum of Divisors Function",
        keywords=["sum of divisors", "sigma function", "number theory", "arithmetic function"],
        conclusion_template="The sum of divisors function σ(n) gives the sum of all positive divisors of n.",
        reasoning_framework=(
            "σ(n) is used in the study of perfect, amicable, and abundant numbers. "
            "It is multiplicative and can be computed using prime factorization."
        ),
        key_factors=["Definition", "Multiplicativity", "Computation", "Applications"],
        primary_authority=["Euclid's Elements", "Modern texts"],
        burden_holder="Proponent of function value",
        adversary_position="Claim that sum is incorrect",
        counter_arguments=[
            "Incorrect factorization.",
            "Misapplication of multiplicativity."
        ],
        resolution_strategy="Factor n and apply formula.",
        entity_scope="Positive integers",
        confidence=0.93,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Euclid's Elements"
    ),
    DoctrineBlock(
        topic="Abundant Numbers",
        keywords=["abundant numbers", "sum of divisors", "number theory", "sigma function"],
        conclusion_template="An abundant number is an integer n for which σ(n) > 2n.",
        reasoning_framework=(
            "Abundant numbers have sum of divisors greater than twice the number. "
            "They are studied in relation to perfect and deficient numbers."
        ),
        key_factors=["Sum of divisors", "Comparison", "Classification", "Applications"],
        primary_authority=["Euclid's Elements", "Modern texts"],
        burden_holder="Proponent of abundance",
        adversary_position="Claim that n is not abundant",
        counter_arguments=[
            "Incorrect computation.",
            "n not greater than 2n."
        ],
        resolution_strategy="Compute σ(n) and compare.",
        entity_scope="Positive integers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Euclid's Elements"
    ),
    DoctrineBlock(
        topic="Deficient Numbers",
        keywords=["deficient numbers", "sum of divisors", "number theory", "sigma function"],
        conclusion_template="A deficient number is an integer n for which σ(n) < 2n.",
        reasoning_framework=(
            "Deficient numbers have sum of divisors less than twice the number. "
            "They are studied in relation to perfect and abundant numbers."
        ),
        key_factors=["Sum of divisors", "Comparison", "Classification", "Applications"],
        primary_authority=["Euclid's Elements", "Modern texts"],
        burden_holder="Proponent of deficiency",
        adversary_position="Claim that n is not deficient",
        counter_arguments=[
            "Incorrect computation.",
            "n not less than 2n."
        ],
        resolution_strategy="Compute σ(n) and compare.",
        entity_scope="Positive integers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Euclid's Elements"
    ),
    DoctrineBlock(
        topic="Sieve of Eratosthenes",
        keywords=["sieve of eratosthenes", "primes", "algorithm", "number theory"],
        conclusion_template="The Sieve of Eratosthenes efficiently finds all primes up to n.",
        reasoning_framework=(
            "The Sieve of Eratosthenes iteratively marks multiples of each prime starting from 2. "
            "Unmarked numbers are primes. "
            "The algorithm is efficient for moderate n and forms the basis for prime generation."
        ),
        key_factors=["Iteration", "Marking multiples", "Efficiency", "Prime generation"],
        primary_authority=["Eratosthenes", "Modern texts"],
        burden_holder="Proponent of algorithm",
        adversary_position="Claim that sieve misses primes",
        counter_arguments=[
            "Incorrect implementation.",
            "n too large for practical computation."
        ],
        resolution_strategy="Verify implementation and adjust n.",
        entity_scope="Positive integers up to n",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Eratosthenes"
    ),
    DoctrineBlock(
        topic="Bertrand's Postulate",
        keywords=["bertrand's postulate", "primes", "number theory", "distribution"],
        conclusion_template="For any integer n > 1, there exists a prime p with n < p < 2n.",
        reasoning_framework=(
            "Bertrand's postulate guarantees at least one prime between n and 2n for n > 1. "
            "The proof uses combinatorial and analytic methods."
        ),
        key_factors=["Interval", "Existence", "Proof methods", "Distribution"],
        primary_authority=["Bertrand (1845)", "Chebyshev (1850)", "Modern texts"],
        burden_holder="Proponent of postulate",
        adversary_position="Claim that no prime exists in interval",
        counter_arguments=[
            "n too small.",
            "Incorrect interval."
        ],
        resolution_strategy="Verify n and apply postulate.",
        entity_scope="Positive integers",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Bertrand (1845), Chebyshev (1850)"
    ),
    DoctrineBlock(
        topic="Carmichael Numbers",
        keywords=["carmichael numbers", "composite", "primality test", "number theory"],
        conclusion_template="Carmichael numbers are composite numbers that pass Fermat's Little Theorem for all bases coprime to n.",
        reasoning_framework=(
            "Carmichael numbers are composite n such that a^{n-1} ≡ 1 mod n for all a coprime to n. "
            "They are pseudoprimes and can fool Fermat primality tests."
        ),
        key_factors=["Composite", "Fermat's theorem", "Pseudoprimes", "Primality testing"],
        primary_authority=["Carmichael (1910)", "Modern texts"],
        burden_holder="Proponent of Carmichael property",
        adversary_position="Claim that n is not Carmichael",
        counter_arguments=[
            "n not composite.",
            "Fails for some base."
        ],
        resolution_strategy="Test all coprime bases.",
        entity_scope="Positive integers",
        confidence=0.90,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Carmichael (1910)"
    ),
    DoctrineBlock(
        topic="Pseudoprimes",
        keywords=["pseudoprimes", "primality test", "number theory", "composite"],
        conclusion_template="A pseudoprime is a composite number that passes a primality test for some base.",
        reasoning_framework=(
            "Pseudoprimes are composite numbers that pass tests like Fermat's Little Theorem for specific bases. "
            "They are rare and can be detected with stronger tests."
        ),
        key_factors=["Composite", "Primality test", "Base selection", "Detection"],
        primary_authority=["Modern texts"],
        burden_holder="Proponent of pseudoprimality",
        adversary_position="Claim that n is not pseudoprime",
        counter_arguments=[
            "Fails for some base.",
            "n is actually prime."
        ],
        resolution_strategy="Test multiple bases and confirm compositeness.",
        entity_scope="Positive integers",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Modern texts"
    ),
    DoctrineBlock(
        topic="Euler's Theorem",
        keywords=["euler's theorem", "modular arithmetic", "totient", "number theory"],
        conclusion_template="If a and n are coprime, then a^{φ(n)} ≡ 1 mod n.",
        reasoning_framework=(
            "Euler's theorem generalizes Fermat's Little Theorem to composite moduli. "
            "If gcd(a, n) = 1, then a^{φ(n)} ≡ 1 mod n. "
            "The proof uses properties of the multiplicative group modulo n."
        ),
        key_factors=["Coprimality", "Totient function", "Group properties", "Proof"],
        primary_authority=["Euler (1763)", "Modern texts"],
        burden_holder="Proponent of theorem",
        adversary_position="Claim that congruence does not hold",
        counter_arguments=[
            "a not coprime to n.",
            "Incorrect computation."
        ],
        resolution_strategy="Verify coprimality and compute totient.",
        entity_scope="Integers modulo n",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Euler (1763)"
    ),
    DoctrineBlock(
        topic="Chinese Remainder Theorem for Non-Coprime Moduli",
        keywords=["crt", "non-coprime", "modular arithmetic", "number theory"],
        conclusion_template="CRT can be generalized to non-coprime moduli under certain conditions.",
        reasoning_framework=(
            "CRT for non-coprime moduli requires compatibility of congruences. "
            "A solution exists if the congruences are consistent modulo the GCD of moduli."
        ),
        key_factors=["Compatibility", "GCD", "Consistency", "Generalization"],
        primary_authority=["Modern texts"],
        burden_holder="Proponent of solution existence",
        adversary_position="Claim that no solution exists",
        counter_arguments=[
            "Congruences incompatible.",
            "Incorrect GCD computation."
        ],
        resolution_strategy="Check compatibility and compute GCD.",
        entity_scope="Integers modulo lcm of moduli",
        confidence=0.90,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Modern texts"
    ),
    DoctrineBlock(
        topic="Linear Congruence",
        keywords=["linear congruence", "modular arithmetic", "number theory", "equations"],
        conclusion_template="The linear congruence ax ≡ b mod n has a solution if and only if gcd(a, n) divides b.",
        reasoning_framework=(
            "A linear congruence ax ≡ b mod n is solvable if gcd(a, n) divides b. "
            "Solutions are constructed using modular inverses and the Euclidean algorithm."
        ),
        key_factors=["GCD", "Solvability", "Modular inverse", "Construction"],
        primary_authority=["Euclid's Elements", "Modern texts"],
        burden_holder="Proponent of solution existence",
        adversary_position="Claim that no solution exists",
        counter_arguments=[
            "GCD does not divide b.",
            "Incorrect construction."
        ],
        resolution_strategy="Compute GCD and construct solution.",
        entity_scope="Integers modulo n",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Euclid's Elements"
    ),
    DoctrineBlock(
        topic="Quadratic Congruence",
        keywords=["quadratic congruence", "modular arithmetic", "number theory", "equations"],
        conclusion_template="The congruence x^2 ≡ a mod n is solvable depending on the value of the Legendre/Jacobi symbol.",
        reasoning_framework=(
            "Quadratic congruences are solved using the Legendre and Jacobi symbols. "
            "For prime modulus, x^2 ≡ a mod p is solvable if (a/p) = 1. "
            "Algorithms exist for finding solutions."
        ),
        key_factors=["Legendre symbol", "Solvability", "Prime modulus", "Algorithms"],
        primary_authority=["Gauss's Disquisitiones Arithmeticae", "Modern texts"],
        burden_holder="Proponent of solution existence",
        adversary_position="Claim that no solution exists",
        counter_arguments=[
            "Incorrect symbol computation.",
            "a not quadratic residue."
        ],
        resolution_strategy="Compute symbol and apply algorithms.",
        entity_scope="Integers modulo n",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gauss's Disquisitiones Arithmeticae"
    ),
    DoctrineBlock(
        topic="Jacobi Symbol",
        keywords=["jacobi symbol", "quadratic residue", "modular arithmetic", "number theory"],
        conclusion_template="The Jacobi symbol (a/n) generalizes the Legendre symbol to composite n.",
        reasoning_framework=(
            "The Jacobi symbol is defined for any odd positive integer n and is multiplicative. "
            "It is used in primality testing and solving quadratic congruences."
        ),
        key_factors=["Definition", "Multiplicativity", "Composite modulus", "Applications"],
        primary_authority=["Jacobi (1837)", "Modern texts"],
        burden_holder="Proponent of symbol value",
        adversary_position="Claim that symbol is incorrectly computed",
        counter_arguments=[
            "Incorrect computation.",
            "n not odd."
        ],
        resolution_strategy="Verify n and apply definition.",
        entity_scope="Odd positive integers",
        confidence=0.93,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Jacobi (1837)"
    ),
    DoctrineBlock(
        topic="Sum of Two Squares Theorem",
        keywords=["sum of two squares", "number theory", "primes", "representation"],
        conclusion_template="A prime p ≡ 1 mod 4 can be expressed as the sum of two squares.",
        reasoning_framework=(
            "The theorem states that primes congruent to 1 mod 4 can be written as p = a^2 + b^2. "
            "Proof uses properties of quadratic residues and Gaussian integers."
        ),
        key_factors=["Congruence", "Representation", "Quadratic residues", "Gaussian integers"],
        primary_authority=["Fermat", "Modern texts"],
        burden_holder="Proponent of representation",
        adversary_position="Claim that p cannot be written as sum of squares",
        counter_arguments=[
            "p not congruent to 1 mod 4.",
            "Incorrect values."
        ],
        resolution_strategy="Verify congruence and construct representation.",
        entity_scope="Primes",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Fermat"
    ),
    DoctrineBlock(
        topic="Mersenne Primes",
        keywords=["mersenne primes", "primes", "number theory", "special primes"],
        conclusion_template="A Mersenne prime is of the form 2^p - 1 where p is prime.",
        reasoning_framework=(
            "Mersenne primes are primes of the form 2^p - 1. "
            "They are rare and used in the search for large primes. "
            "Primality of Mersenne numbers is tested using the Lucas-Lehmer test."
        ),
        key_factors=["Form", "Primality", "Testing", "Applications"],
        primary_authority=["Mersenne (1644)", "Modern texts"],
        burden_holder="Proponent of primality",
        adversary_position="Claim that number is not prime",
        counter_arguments=[
            "p not prime.",
            "Fails Lucas-Lehmer test."
        ],
        resolution_strategy="Apply Lucas-Lehmer test.",
        entity_scope="Positive integers",
        confidence=0.93,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Mersenne (1644)"
    ),
    DoctrineBlock(
        topic="Lucas-Lehmer Test",
        keywords=["lucas-lehmer test", "mersenne primes", "primality test", "number theory"],
        conclusion_template="The Lucas-Lehmer test determines primality of Mersenne numbers.",
        reasoning_framework=(
            "The Lucas-Lehmer test iteratively computes a sequence and checks divisibility by Mersenne number. "
            "If final value is zero modulo Mersenne number, it is prime."
        ),
        key_factors=["Iteration", "Sequence", "Divisibility", "Primality"],
        primary_authority=["Lucas (1876)", "Lehmer (1930)", "Modern texts"],
        burden_holder="Tester",
        adversary_position="Claim that number is not prime",
        counter_arguments=[
            "Incorrect sequence computation.",
            "Fails test."
        ],
        resolution_strategy="Verify computation and apply test.",
        entity_scope="Mersenne numbers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Lucas (1876), Lehmer (1930)"
    ),
    DoctrineBlock(
        topic="Perfect Squares",
        keywords=["perfect squares", "number theory", "representation", "integers"],
        conclusion_template="A perfect square is an integer that is the square of another integer.",
        reasoning_framework=(
            "Perfect squares are integers n such that n = k^2 for some integer k. "
            "They have special properties in factorization and representation."
        ),
        key_factors=["Definition", "Representation", "Properties", "Applications"],
        primary_authority=["Euclid's Elements", "Modern texts"],
        burden_holder="Proponent of perfect square",
        adversary_position="Claim that n is not perfect square",
        counter_arguments=[
            "n not integer square.",
            "Incorrect computation."
        ],
        resolution_strategy="Compute square root and verify integer.",
        entity_scope="Positive integers",
        confidence=0.93,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Euclid's Elements"
    ),
    DoctrineBlock(
        topic="Square-Free Numbers",
        keywords=["square-free numbers", "number theory", "factorization", "integers"],
        conclusion_template="A square-free number is an integer not divisible by any perfect square greater than 1.",
        reasoning_framework=(
            "Square-free numbers have no repeated prime factors. "
            "They are important in the study of arithmetic functions and factorization."
        ),
        key_factors=["Definition", "Prime factorization", "Properties", "Applications"],
        primary_authority=["Modern texts"],
        burden_holder="Proponent of square-freeness",
        adversary_position="Claim that n is not square-free",
        counter_arguments=[
            "n has repeated prime factor.",
            "Incorrect factorization."
        ],
        resolution_strategy="Factor n and check for repeated primes.",
        entity_scope="Positive integers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Modern texts"
    ),
    DoctrineBlock(
        topic="Arithmetic Functions",
        keywords=["arithmetic functions", "number theory", "functions", "integers"],
        conclusion_template="Arithmetic functions assign values to integers based on their arithmetic properties.",
        reasoning_framework=(
            "Arithmetic functions include σ(n), φ(n), μ(n), and others. "
            "They are used in analytic and algebraic number theory."
        ),
        key_factors=["Definition", "Examples", "Applications", "Properties"],
        primary_authority=["Modern texts"],
        burden_holder="Proponent of function definition",
        adversary_position="Claim that function is not arithmetic",
        counter_arguments=[
            "Incorrect definition.",
            "Misapplication."
        ],
        resolution_strategy="Clarify definition and provide examples.",
        entity_scope="Positive integers",
        confidence=0.91,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Modern texts"
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