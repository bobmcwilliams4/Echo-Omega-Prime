from dataclasses import dataclass, field
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
        topic="Addition of Natural Numbers",
        keywords=["addition", "natural numbers", "sum", "commutativity", "associativity"],
        conclusion_template="The sum of {a} and {b} is {result}.",
        reasoning_framework="""
Addition of natural numbers is a binary operation defined on the set of natural numbers (N). 
The operation is both commutative and associative, meaning that the order of addition does not affect the result, 
and grouping of operands does not change the outcome. The identity element is 0, such that for any natural number n, n + 0 = n. 
Addition is closed in N, i.e., the sum of any two natural numbers is also a natural number. 
The operation can be defined recursively: for any n in N, n + 0 = n and n + S(m) = S(n + m), where S denotes the successor function. 
Addition is the foundation for more complex operations like multiplication and exponentiation. 
Proofs of properties often use induction.
""",
        key_factors=["Commutativity", "Associativity", "Closure", "Identity element"],
        primary_authority=["Peano's Axioms", "Principia Mathematica", "NCTM Standards"],
        burden_holder="Proponent of the operation",
        adversary_position="Addition is not always closed or commutative in all number systems.",
        counter_arguments=[
            "In natural numbers, closure and commutativity are proven by Peano's axioms.",
            "Counterexamples in other systems (e.g., matrices) do not apply to N."
        ],
        resolution_strategy="Reference foundational axioms and standard proofs.",
        entity_scope="Natural Numbers",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Peano's Axioms"
    ),
    DoctrineBlock(
        topic="Subtraction of Integers",
        keywords=["subtraction", "integers", "difference", "inverse operation"],
        conclusion_template="The difference between {a} and {b} is {result}.",
        reasoning_framework="""
Subtraction is defined as the inverse operation of addition. For integers, subtraction is always possible, 
as the set of integers (Z) is closed under subtraction. The operation is not commutative nor associative. 
For any integers a and b, a - b is defined as the unique integer c such that a = b + c. 
Subtraction can be visualized as movement along the number line. 
The operation is essential for defining negative numbers and for solving equations of the form x + b = a.
""",
        key_factors=["Inverse of addition", "Closure in Z", "Non-commutativity", "Non-associativity"],
        primary_authority=["Peano's Axioms", "NCTM Standards", "Mathematical Analysis texts"],
        burden_holder="Proponent of subtraction",
        adversary_position="Subtraction is not always defined in N; negative results are not natural numbers.",
        counter_arguments=[
            "Extension to integers resolves closure issues.",
            "Subtraction in N is only partially defined."
        ],
        resolution_strategy="Clarify the domain and extend to integers for full closure.",
        entity_scope="Integers",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Extension of Peano's Axioms to Z"
    ),
    DoctrineBlock(
        topic="Multiplication of Real Numbers",
        keywords=["multiplication", "real numbers", "product", "commutativity", "distributivity"],
        conclusion_template="The product of {a} and {b} is {result}.",
        reasoning_framework="""
Multiplication in the real numbers (R) is a binary operation that is commutative, associative, and distributive over addition. 
The identity element is 1, and the operation is closed in R. Multiplication can be defined via repeated addition for natural numbers, 
and extended to rationals and reals via limits and completeness. Negative numbers and zero have specific rules: 
any number times zero is zero, and the product of two negatives is positive. 
Multiplication is fundamental for defining powers, roots, and for the structure of fields.
""",
        key_factors=["Commutativity", "Associativity", "Distributivity", "Closure", "Identity element"],
        primary_authority=["Field Axioms", "Real Analysis texts", "NCTM Standards"],
        burden_holder="Proponent of the operation",
        adversary_position="Multiplication is not always commutative in non-commutative structures (e.g., matrices).",
        counter_arguments=[
            "In R, commutativity and other properties are established by field axioms.",
            "Non-commutative examples are outside the scope of R."
        ],
        resolution_strategy="Restrict discussion to real numbers and cite field axioms.",
        entity_scope="Real Numbers",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Field Axioms"
    ),
    DoctrineBlock(
        topic="Division by Zero",
        keywords=["division", "zero", "undefined", "real numbers", "rationals"],
        conclusion_template="Division by zero is undefined.",
        reasoning_framework="""
Division by zero is not defined in the real numbers, rationals, or integers. 
For any number a, the expression a/0 does not yield a unique, meaningful result. 
Attempting to define division by zero leads to contradictions and loss of structure (e.g., field properties). 
In calculus, limits involving division by zero may tend to infinity, but the operation itself remains undefined. 
This doctrine is foundational for the consistency of arithmetic and algebra.
""",
        key_factors=["Undefined operation", "Loss of algebraic structure", "Contradictions"],
        primary_authority=["Field Axioms", "Standard Algebra Texts", "NCTM Standards"],
        burden_holder="Proponent of defining division by zero",
        adversary_position="Division by zero could be defined as infinity or a special symbol.",
        counter_arguments=[
            "Defining division by zero breaks field properties.",
            "No consistent extension exists in standard arithmetic."
        ],
        resolution_strategy="Reject definitions that violate field axioms.",
        entity_scope="Real Numbers, Rationals, Integers",
        confidence=1.0,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Field Axioms"
    ),
    DoctrineBlock(
        topic="Order of Operations (PEMDAS/BODMAS)",
        keywords=["order of operations", "PEMDAS", "BODMAS", "parentheses", "exponents"],
        conclusion_template="The expression {expression} evaluates to {result} following the order of operations.",
        reasoning_framework="""
The order of operations is a convention that dictates the sequence in which arithmetic operations are performed. 
The standard order is Parentheses/Brackets, Exponents/Orders, Multiplication and Division (left to right), Addition and Subtraction (left to right). 
This convention ensures that expressions are interpreted consistently. 
Ambiguities are resolved by explicit parentheses. 
Order of operations is universally taught and is essential for correct computation in mathematics and programming.
""",
        key_factors=["Conventional precedence", "Parentheses override", "Left-to-right evaluation"],
        primary_authority=["NCTM Standards", "Mathematical Practice Guides", "School Curricula"],
        burden_holder="Evaluator of the expression",
        adversary_position="Alternative conventions may exist in historical or regional contexts.",
        counter_arguments=[
            "PEMDAS/BODMAS is globally accepted in modern mathematics.",
            "Ambiguities are resolved by explicit notation."
        ],
        resolution_strategy="Apply standard conventions and clarify with parentheses as needed.",
        entity_scope="All arithmetic expressions",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NCTM Standards"
    ),
    DoctrineBlock(
        topic="Commutativity of Addition",
        keywords=["addition", "commutativity", "real numbers", "natural numbers"],
        conclusion_template="Addition is commutative: {a} + {b} = {b} + {a}.",
        reasoning_framework="""
Commutativity of addition states that the order of addends does not affect the sum. 
This property holds in natural numbers, integers, rationals, and real numbers. 
Proofs rely on Peano's axioms and induction for natural numbers, and field axioms for reals. 
Commutativity is essential for algebraic manipulation and simplification.
""",
        key_factors=["Order independence", "Proof by induction", "Field properties"],
        primary_authority=["Peano's Axioms", "Field Axioms", "NCTM Standards"],
        burden_holder="Proponent of commutativity",
        adversary_position="Addition is not commutative in all algebraic structures (e.g., matrices).",
        counter_arguments=[
            "Restriction to standard number systems preserves commutativity.",
            "Non-commutative examples are outside the scope."
        ],
        resolution_strategy="Specify the domain and cite foundational axioms.",
        entity_scope="Natural Numbers, Integers, Rationals, Reals",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Peano's Axioms, Field Axioms"
    ),
    DoctrineBlock(
        topic="Associativity of Multiplication",
        keywords=["multiplication", "associativity", "real numbers", "integers"],
        conclusion_template="Multiplication is associative: ({a} × {b}) × {c} = {a} × ({b} × {c}).",
        reasoning_framework="""
Associativity of multiplication means that the grouping of factors does not affect the product. 
This property holds in integers, rationals, and real numbers, and is established by the field axioms. 
Associativity allows for reordering and regrouping in computations and algebraic proofs. 
Exceptions exist in some non-standard algebraic structures (e.g., octonions).
""",
        key_factors=["Grouping independence", "Field properties", "Algebraic manipulation"],
        primary_authority=["Field Axioms", "Algebra Texts", "NCTM Standards"],
        burden_holder="Proponent of associativity",
        adversary_position="Associativity fails in some non-standard structures.",
        counter_arguments=[
            "Standard number systems are associative under multiplication.",
            "Exceptions are not relevant to basic arithmetic."
        ],
        resolution_strategy="Restrict to standard number systems and cite axioms.",
        entity_scope="Integers, Rationals, Reals",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Field Axioms"
    ),
    DoctrineBlock(
        topic="Distributive Law",
        keywords=["distributive", "multiplication", "addition", "law", "real numbers"],
        conclusion_template="Multiplication distributes over addition: {a} × ({b} + {c}) = {a} × {b} + {a} × {c}.",
        reasoning_framework="""
The distributive law connects multiplication and addition, stating that multiplying a number by a sum 
is equivalent to multiplying each addend and then adding the results. 
This property is a cornerstone of algebra and is used in expansion, factoring, and simplification. 
The distributive law is proven from field axioms and is valid in all standard number systems.
""",
        key_factors=["Interaction of operations", "Proof from field axioms", "Algebraic manipulation"],
        primary_authority=["Field Axioms", "Algebra Texts", "NCTM Standards"],
        burden_holder="Proponent of distributivity",
        adversary_position="Distributivity may fail in some non-standard structures.",
        counter_arguments=[
            "Distributive law holds in all standard number systems.",
            "Non-standard exceptions are outside the scope."
        ],
        resolution_strategy="Cite field axioms and restrict to standard domains.",
        entity_scope="Integers, Rationals, Reals",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Field Axioms"
    ),
    DoctrineBlock(
        topic="Identity Element for Addition",
        keywords=["identity element", "addition", "zero", "real numbers"],
        conclusion_template="Zero is the additive identity: {a} + 0 = {a}.",
        reasoning_framework="""
The identity element for addition is zero, meaning that adding zero to any number leaves it unchanged. 
This property is fundamental to the structure of number systems and is included in the axioms of groups and fields. 
It enables the definition of additive inverses and is essential for solving equations.
""",
        key_factors=["Zero as identity", "Axiomatic foundation", "Equation solving"],
        primary_authority=["Group Axioms", "Field Axioms", "NCTM Standards"],
        burden_holder="Proponent of the identity property",
        adversary_position="Alternative structures may have different identities.",
        counter_arguments=[
            "In standard arithmetic, zero is universally the additive identity.",
            "Other identities are not relevant to standard systems."
        ],
        resolution_strategy="Restrict to standard number systems and cite axioms.",
        entity_scope="Integers, Rationals, Reals",
        confidence=1.0,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Group and Field Axioms"
    ),
    DoctrineBlock(
        topic="Multiplicative Inverse",
        keywords=["multiplicative inverse", "reciprocal", "real numbers", "division"],
        conclusion_template="The multiplicative inverse of {a} is {result}, since {a} × {result} = 1.",
        reasoning_framework="""
Every nonzero real number has a unique multiplicative inverse (reciprocal), such that their product is 1. 
This property is essential for division and for the structure of fields. 
Zero does not have a multiplicative inverse, as division by zero is undefined. 
The existence and uniqueness of inverses is a field axiom.
""",
        key_factors=["Nonzero requirement", "Reciprocal", "Field axiom"],
        primary_authority=["Field Axioms", "Algebra Texts", "NCTM Standards"],
        burden_holder="Proponent of the inverse property",
        adversary_position="Zero lacks a multiplicative inverse.",
        counter_arguments=[
            "Zero is excluded by definition.",
            "Division by zero is undefined."
        ],
        resolution_strategy="Cite field axioms and clarify the domain.",
        entity_scope="Nonzero Real Numbers",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Field Axioms"
    ),
    DoctrineBlock(
        topic="Closure Property",
        keywords=["closure", "property", "operation", "real numbers", "integers"],
        conclusion_template="The set {S} is closed under {operation}.",
        reasoning_framework="""
A set is closed under an operation if applying the operation to elements of the set always yields an element of the same set. 
For example, integers are closed under addition, subtraction, and multiplication, but not under division. 
Closure is a basic property used to define algebraic structures like groups, rings, and fields.
""",
        key_factors=["Set definition", "Operation", "Result within set"],
        primary_authority=["Algebra Texts", "NCTM Standards", "Group Theory"],
        burden_holder="Proponent of closure",
        adversary_position="Some sets are not closed under certain operations.",
        counter_arguments=[
            "Specify the operation and set clearly.",
            "Provide counterexamples where closure fails."
        ],
        resolution_strategy="Define the set and operation explicitly.",
        entity_scope="Any algebraic set",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Algebraic Structure Definitions"
    ),
    DoctrineBlock(
        topic="Even and Odd Numbers",
        keywords=["even", "odd", "parity", "integers", "divisibility"],
        conclusion_template="{n} is {parity} because it is {reason}.",
        reasoning_framework="""
An even number is an integer divisible by 2; an odd number is not divisible by 2. 
Parity is preserved under addition and multiplication: even ± even = even, odd ± odd = even, even × any = even, odd × odd = odd. 
Parity is used in divisibility, modular arithmetic, and number theory proofs.
""",
        key_factors=["Divisibility by 2", "Parity rules", "Integer domain"],
        primary_authority=["Number Theory Texts", "NCTM Standards", "Elementary Mathematics"],
        burden_holder="Proponent of parity classification",
        adversary_position="Non-integers do not have parity.",
        counter_arguments=[
            "Parity is defined only for integers.",
            "Extend definition with caution."
        ],
        resolution_strategy="Restrict to integers and clarify definitions.",
        entity_scope="Integers",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Number Theory"
    ),
    DoctrineBlock(
        topic="Prime Numbers",
        keywords=["prime", "composite", "divisibility", "number theory"],
        conclusion_template="{n} is prime if its only positive divisors are 1 and itself.",
        reasoning_framework="""
A prime number is an integer greater than 1 with no positive divisors other than 1 and itself. 
Primes are the building blocks of the integers, as every integer greater than 1 can be uniquely factored into primes (Fundamental Theorem of Arithmetic). 
Tests for primality include trial division, Sieve of Eratosthenes, and probabilistic algorithms.
""",
        key_factors=["Divisibility", "Uniqueness", "Greater than 1"],
        primary_authority=["Number Theory Texts", "Euclid's Elements", "NCTM Standards"],
        burden_holder="Proponent of primality",
        adversary_position="1 is sometimes considered prime in historical texts.",
        counter_arguments=[
            "Modern definition excludes 1 for uniqueness of factorization.",
            "Historical definitions are outdated."
        ],
        resolution_strategy="Adopt modern definitions and cite theorems.",
        entity_scope="Positive Integers > 1",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Fundamental Theorem of Arithmetic"
    ),
    DoctrineBlock(
        topic="Greatest Common Divisor (GCD)",
        keywords=["gcd", "greatest common divisor", "euclidean algorithm", "divisibility"],
        conclusion_template="The GCD of {a} and {b} is {result}.",
        reasoning_framework="""
The greatest common divisor of two integers is the largest integer that divides both without remainder. 
The Euclidean algorithm efficiently computes the GCD. 
GCD is used in simplifying fractions, solving Diophantine equations, and number theory.
""",
        key_factors=["Divisibility", "Euclidean algorithm", "Integer domain"],
        primary_authority=["Number Theory Texts", "Euclid's Elements", "NCTM Standards"],
        burden_holder="Proponent of GCD calculation",
        adversary_position="GCD is undefined for zero and negative numbers.",
        counter_arguments=[
            "GCD(0, n) is defined as |n| for n ≠ 0.",
            "Negative numbers are handled by absolute value."
        ],
        resolution_strategy="Clarify definitions and handle edge cases.",
        entity_scope="Integers",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Euclidean Algorithm"
    ),
    DoctrineBlock(
        topic="Least Common Multiple (LCM)",
        keywords=["lcm", "least common multiple", "multiples", "divisibility"],
        conclusion_template="The LCM of {a} and {b} is {result}.",
        reasoning_framework="""
The least common multiple of two integers is the smallest positive integer divisible by both. 
LCM is computed using the formula LCM(a, b) = |a × b| / GCD(a, b). 
LCM is used in adding fractions, scheduling, and number theory.
""",
        key_factors=["Multiples", "Divisibility", "GCD relation"],
        primary_authority=["Number Theory Texts", "NCTM Standards", "Elementary Mathematics"],
        burden_holder="Proponent of LCM calculation",
        adversary_position="LCM is undefined for zero.",
        counter_arguments=[
            "By convention, LCM(0, n) = 0.",
            "Clarify definitions for edge cases."
        ],
        resolution_strategy="Define LCM for all integer pairs, including zero.",
        entity_scope="Integers",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Number Theory"
    ),
    DoctrineBlock(
        topic="Properties of Zero",
        keywords=["zero", "additive identity", "multiplication", "absorption"],
        conclusion_template="Zero has unique properties in arithmetic operations.",
        reasoning_framework="""
Zero is the additive identity: a + 0 = a for any a. 
Multiplying any number by zero yields zero: a × 0 = 0. 
Zero is the only number that is neither positive nor negative. 
Division by zero is undefined. 
Zero plays a critical role in algebraic structures and calculus.
""",
        key_factors=["Additive identity", "Multiplicative absorption", "Undefined division"],
        primary_authority=["Algebra Texts", "NCTM Standards", "Field Axioms"],
        burden_holder="Proponent of zero's properties",
        adversary_position="Zero may behave differently in extended systems (e.g., projective geometry).",
        counter_arguments=[
            "Standard arithmetic defines zero's properties clearly.",
            "Extensions are outside the basic arithmetic scope."
        ],
        resolution_strategy="Restrict to standard arithmetic and cite axioms.",
        entity_scope="All number systems",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Field Axioms"
    ),
    DoctrineBlock(
        topic="Negative Numbers",
        keywords=["negative numbers", "integers", "additive inverse", "subtraction"],
        conclusion_template="The additive inverse of {a} is {-a}.",
        reasoning_framework="""
Negative numbers are defined as the additive inverses of positive numbers. 
For any integer a, there exists -a such that a + (-a) = 0. 
Negative numbers extend the natural numbers to the integers, allowing for full closure under subtraction. 
They obey the same arithmetic laws as positive numbers.
""",
        key_factors=["Additive inverse", "Closure under subtraction", "Integer extension"],
        primary_authority=["Algebra Texts", "NCTM Standards", "Number Theory"],
        burden_holder="Proponent of negative numbers",
        adversary_position="Negative numbers are not natural numbers.",
        counter_arguments=[
            "Extension to integers is standard.",
            "Natural numbers are a subset of integers."
        ],
        resolution_strategy="Clarify the domain and cite standard extensions.",
        entity_scope="Integers",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Algebraic Structures"
    ),
    DoctrineBlock(
        topic="Absolute Value",
        keywords=["absolute value", "modulus", "distance", "real numbers"],
        conclusion_template="The absolute value of {a} is {result}.",
        reasoning_framework="""
The absolute value of a real number is its distance from zero on the number line, always non-negative. 
It is defined as |a| = a if a ≥ 0, and |a| = -a if a < 0. 
Absolute value is used in distance calculations, inequalities, and analysis.
""",
        key_factors=["Non-negativity", "Distance interpretation", "Piecewise definition"],
        primary_authority=["Analysis Texts", "NCTM Standards", "Algebra Texts"],
        burden_holder="Proponent of absolute value",
        adversary_position="Absolute value is not differentiable at zero.",
        counter_arguments=[
            "Non-differentiability is a calculus issue, not arithmetic.",
            "Piecewise definition is standard."
        ],
        resolution_strategy="Clarify the context and restrict to arithmetic properties.",
        entity_scope="Real Numbers",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Analysis Texts"
    ),
    DoctrineBlock(
        topic="Properties of Exponents",
        keywords=["exponents", "powers", "laws", "multiplication", "real numbers"],
        conclusion_template="The value of {a}^{b} is {result} using exponent rules.",
        reasoning_framework="""
Exponents represent repeated multiplication. 
The laws of exponents include: a^m × a^n = a^{m+n}, (a^m)^n = a^{mn}, a^0 = 1 (for a ≠ 0), and a^{-n} = 1/a^n. 
These rules are derived from the definition of exponentiation and are valid for real numbers, with restrictions for zero and negative bases.
""",
        key_factors=["Repeated multiplication", "Exponent laws", "Domain restrictions"],
        primary_authority=["Algebra Texts", "NCTM Standards", "Analysis Texts"],
        burden_holder="Proponent of exponent rules",
        adversary_position="Exponent rules may fail for zero or negative bases.",
        counter_arguments=[
            "Clarify domain and restrict as needed.",
            "Zero and negative bases require special handling."
        ],
        resolution_strategy="State domain restrictions explicitly.",
        entity_scope="Real Numbers (with restrictions)",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Algebra Texts"
    ),
    DoctrineBlock(
        topic="Roots and Radicals",
        keywords=["roots", "radicals", "square root", "nth root", "real numbers"],
        conclusion_template="The {n}th root of {a} is {result}.",
        reasoning_framework="""
Roots are the inverse operation of exponentiation. 
The principal nth root of a real number a is the unique non-negative real number x such that x^n = a. 
Square roots of negative numbers are not real. 
Radicals are used in solving equations and simplifying expressions.
""",
        key_factors=["Inverse of exponentiation", "Principal root", "Domain restrictions"],
        primary_authority=["Algebra Texts", "NCTM Standards", "Analysis Texts"],
        burden_holder="Proponent of root calculation",
        adversary_position="Roots of negative numbers are undefined in reals.",
        counter_arguments=[
            "Complex numbers extend the definition.",
            "Restrict to real numbers for arithmetic."
        ],
        resolution_strategy="Clarify the domain and restrict to reals as needed.",
        entity_scope="Real Numbers (with restrictions)",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Algebra Texts"
    ),
    DoctrineBlock(
        topic="Decimal Representation",
        keywords=["decimal", "representation", "real numbers", "place value"],
        conclusion_template="{n} is represented as {decimal} in decimal notation.",
        reasoning_framework="""
Decimal representation expresses real numbers as sums of powers of ten, using digits 0-9. 
Place value determines the magnitude of each digit. 
Terminating and repeating decimals correspond to rationals; non-repeating, non-terminating decimals are irrational.
""",
        key_factors=["Place value", "Rational/irrational distinction", "Base 10"],
        primary_authority=["Elementary Mathematics", "NCTM Standards", "Number Theory"],
        burden_holder="Proponent of decimal representation",
        adversary_position="Some numbers cannot be exactly represented in decimal.",
        counter_arguments=[
            "Irrational numbers have infinite, non-repeating decimals.",
            "Decimal expansion is a standard representation."
        ],
        resolution_strategy="Clarify the type of number and representation limits.",
        entity_scope="Real Numbers",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Elementary Mathematics"
    ),
    DoctrineBlock(
        topic="Rational and Irrational Numbers",
        keywords=["rational", "irrational", "real numbers", "fraction", "decimal"],
        conclusion_template="{n} is {type} because {reason}.",
        reasoning_framework="""
A rational number can be expressed as a fraction a/b with integers a, b (b ≠ 0). 
Irrational numbers cannot be written as such fractions and have non-repeating, non-terminating decimal expansions. 
Examples: 1/2 is rational, √2 and π are irrational. 
The set of real numbers is the union of rationals and irrationals.
""",
        key_factors=["Fraction representation", "Decimal expansion", "Set inclusion"],
        primary_authority=["Number Theory Texts", "NCTM Standards", "Analysis Texts"],
        burden_holder="Proponent of classification",
        adversary_position="Some decimals may appear rational but are not.",
        counter_arguments=[
            "Decimal expansion criteria are well-defined.",
            "Clarify representation and definitions."
        ],
        resolution_strategy="Use precise definitions and examples.",
        entity_scope="Real Numbers",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Number Theory"
    ),
    DoctrineBlock(
        topic="Fraction Simplification",
        keywords=["fractions", "simplification", "gcd", "lowest terms"],
        conclusion_template="{a}/{b} simplifies to {result}.",
        reasoning_framework="""
A fraction is simplified when the numerator and denominator share no common factors other than 1. 
Simplification is achieved by dividing both by their GCD. 
This process does not change the value of the fraction and is essential for comparison and computation.
""",
        key_factors=["GCD", "Equivalent fractions", "Lowest terms"],
        primary_authority=["Elementary Mathematics", "NCTM Standards", "Number Theory"],
        burden_holder="Proponent of simplification",
        adversary_position="Simplification may not be unique for improper fractions.",
        counter_arguments=[
            "Lowest terms are unique for each rational number.",
            "Improper fractions can be converted to mixed numbers."
        ],
        resolution_strategy="Clarify definitions and provide examples.",
        entity_scope="Rational Numbers",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Elementary Mathematics"
    ),
    DoctrineBlock(
        topic="Proportions and Ratios",
        keywords=["proportion", "ratio", "fractions", "equivalence"],
        conclusion_template="The ratio of {a} to {b} is {result}.",
        reasoning_framework="""
A ratio compares two quantities by division. 
A proportion states that two ratios are equal. 
Proportional reasoning is used in scaling, similarity, and solving equations. 
Cross-multiplication is a standard method for verifying proportions.
""",
        key_factors=["Division", "Equivalence", "Cross-multiplication"],
        primary_authority=["Elementary Mathematics", "NCTM Standards", "Algebra Texts"],
        burden_holder="Proponent of proportionality",
        adversary_position="Ratios may be undefined for zero denominators.",
        counter_arguments=[
            "Division by zero is excluded by definition.",
            "Clarify domain restrictions."
        ],
        resolution_strategy="State restrictions and use cross-multiplication.",
        entity_scope="Rational Numbers (with restrictions)",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Elementary Mathematics"
    ),
    DoctrineBlock(
        topic="Percentages",
        keywords=["percent", "percentage", "proportion", "hundredths"],
        conclusion_template="{n}% is equivalent to {fraction} or {decimal}.",
        reasoning_framework="""
A percentage expresses a number as a fraction of 100. 
Conversion between percentages, decimals, and fractions is standard practice. 
Percentages are widely used in statistics, finance, and everyday calculations.
""",
        key_factors=["Fraction of 100", "Conversion", "Practical applications"],
        primary_authority=["Elementary Mathematics", "NCTM Standards", "Statistics Texts"],
        burden_holder="Proponent of conversion",
        adversary_position="Percentages can be misleading without context.",
        counter_arguments=[
            "Clarify the base quantity and context.",
            "Use precise conversions."
        ],
        resolution_strategy="Provide context and standard conversion methods.",
        entity_scope="Rational Numbers",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Elementary Mathematics"
    ),
    DoctrineBlock(
        topic="Order Relations",
        keywords=["order", "inequality", "greater than", "less than", "real numbers"],
        conclusion_template="{a} {relation} {b} is {truth}.",
        reasoning_framework="""
Order relations in real numbers are defined by the properties of inequalities. 
For any real numbers a and b, exactly one of a < b, a = b, or a > b holds (trichotomy law). 
Inequalities are preserved under addition and multiplication by positive numbers.
""",
        key_factors=["Trichotomy", "Transitivity", "Preservation under operations"],
        primary_authority=["Analysis Texts", "NCTM Standards", "Algebra Texts"],
        burden_holder="Proponent of the relation",
        adversary_position="Order may not be preserved under multiplication by negatives.",
        counter_arguments=[
            "Multiplying by a negative reverses the inequality.",
            "Clarify the operation involved."
        ],
        resolution_strategy="Specify the operation and domain.",
        entity_scope="Real Numbers",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Analysis Texts"
    ),
    DoctrineBlock(
        topic="Properties of Inequalities",
        keywords=["inequality", "transitivity", "addition", "multiplication"],
        conclusion_template="If {a} < {b} and {b} < {c}, then {a} < {c}.",
        reasoning_framework="""
Inequalities are transitive, additive, and multiplicative (with restrictions). 
Adding the same number to both sides preserves the inequality. 
Multiplying both sides by a positive number preserves the relation; by a negative number, it reverses the inequality.
""",
        key_factors=["Transitivity", "Addition", "Multiplication rules"],
        primary_authority=["Analysis Texts", "Algebra Texts", "NCTM Standards"],
        burden_holder="Proponent of the inequality property",
        adversary_position="Multiplication by zero or negatives complicates inequalities.",
        counter_arguments=[
            "Multiplication by zero collapses the inequality.",
            "Negative multiplication reverses the relation."
        ],
        resolution_strategy="State all cases explicitly.",
        entity_scope="Real Numbers",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Analysis Texts"
    ),
    DoctrineBlock(
        topic="Mathematical Induction",
        keywords=["induction", "proof", "natural numbers", "recursion"],
        conclusion_template="By induction, the statement holds for all natural numbers.",
        reasoning_framework="""
Mathematical induction is a proof technique for statements about natural numbers. 
It consists of a base case (prove for n=1) and an inductive step (assume true for n=k, prove for n=k+1). 
If both are established, the statement holds for all natural numbers.
""",
        key_factors=["Base case", "Inductive step", "Well-ordering principle"],
        primary_authority=["Mathematical Logic Texts", "Peano's Axioms", "NCTM Standards"],
        burden_holder="Proponent of the induction proof",
        adversary_position="Induction only applies to well-ordered sets.",
        counter_arguments=[
            "Natural numbers are well-ordered.",
            "Other domains require different techniques."
        ],
        resolution_strategy="Restrict to natural numbers and cite axioms.",
        entity_scope="Natural Numbers",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Peano's Axioms"
    ),
    DoctrineBlock(
        topic="Distributivity of Division over Addition",
        keywords=["division", "addition", "distributivity", "arithmetic"],
        conclusion_template="Division distributes over addition only in the numerator: ({a} + {b}) / {c} = {a}/{c} + {b}/{c}.",
        reasoning_framework="""
Division distributes over addition in the numerator but not in the denominator. 
For example, (a + b)/c = a/c + b/c, but a/(b + c) ≠ a/b + a/c in general. 
This property is used in fraction decomposition and algebraic manipulation.
""",
        key_factors=["Numerator distributivity", "Denominator restriction", "Fraction decomposition"],
        primary_authority=["Algebra Texts", "NCTM Standards", "Elementary Mathematics"],
        burden_holder="Proponent of distributivity",
        adversary_position="Division does not distribute over addition in the denominator.",
        counter_arguments=[
            "Provide counterexamples for denominator.",
            "Clarify the direction of distributivity."
        ],
        resolution_strategy="State the property precisely and provide examples.",
        entity_scope="Rational Numbers (with restrictions)",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Algebra Texts"
    ),
    DoctrineBlock(
        topic="Zero Product Property",
        keywords=["zero product", "property", "multiplication", "roots"],
        conclusion_template="If {a} × {b} = 0, then {a} = 0 or {b} = 0.",
        reasoning_framework="""
The zero product property states that if the product of two real numbers is zero, then at least one factor must be zero. 
This property is fundamental for solving equations and factoring polynomials.
""",
        key_factors=["Multiplication", "Roots", "Equation solving"],
        primary_authority=["Algebra Texts", "NCTM Standards", "Field Axioms"],
        burden_holder="Proponent of the property",
        adversary_position="Zero product property may fail in non-integral domains.",
        counter_arguments=[
            "Standard number systems are integral domains.",
            "Counterexamples are outside the scope."
        ],
        resolution_strategy="Restrict to standard number systems.",
        entity_scope="Integers, Rationals, Reals",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Field Axioms"
    ),
    DoctrineBlock(
        topic="Properties of Negative Numbers in Multiplication",
        keywords=["negative numbers", "multiplication", "sign rules"],
        conclusion_template="The product of two negative numbers is positive.",
        reasoning_framework="""
Multiplying two negative numbers yields a positive result. 
This follows from the distributive law and the definition of negative numbers as additive inverses. 
The rule is essential for consistency in arithmetic and algebra.
""",
        key_factors=["Distributive law", "Additive inverse", "Consistency"],
        primary_authority=["Algebra Texts", "NCTM Standards", "Number Theory"],
        burden_holder="Proponent of the sign rule",
        adversary_position="The rule may seem counterintuitive.",
        counter_arguments=[
            "Proofs use distributivity and consistency.",
            "Counterintuitive results are explained by algebraic structure."
        ],
        resolution_strategy="Provide algebraic proofs and examples.",
        entity_scope="Integers, Rationals, Reals",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Algebra Texts"
    ),
    DoctrineBlock(
        topic="Commutativity of Multiplication",
        keywords=["multiplication", "commutativity", "real numbers", "integers"],
        conclusion_template="Multiplication is commutative: {a} × {b} = {b} × {a}.",
        reasoning_framework="""
Commutativity of multiplication holds in integers, rationals, and real numbers. 
The order of factors does not affect the product. 
This property is established by field axioms and is essential for algebraic manipulation.
""",
        key_factors=["Order independence", "Field properties", "Algebraic manipulation"],
        primary_authority=["Field Axioms", "Algebra Texts", "NCTM Standards"],
        burden_holder="Proponent of commutativity",
        adversary_position="Multiplication is not commutative in all structures (e.g., matrices).",
        counter_arguments=[
            "Restrict to standard number systems.",
            "Non-commutative examples are outside the scope."
        ],
        resolution_strategy="Specify the domain and cite axioms.",
        entity_scope="Integers, Rationals, Reals",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Field Axioms"
    ),
    DoctrineBlock(
        topic="Associativity of Addition",
        keywords=["addition", "associativity", "real numbers", "integers"],
        conclusion_template="Addition is associative: ({a} + {b}) + {c} = {a} + ({b} + {c}).",
        reasoning_framework="""
Associativity of addition means that the grouping of addends does not affect the sum. 
This property holds in natural numbers, integers, rationals, and real numbers. 
It is proven by induction and is foundational for algebraic manipulation.
""",
        key_factors=["Grouping independence", "Proof by induction", "Field properties"],
        primary_authority=["Peano's Axioms", "Field Axioms", "NCTM Standards"],
        burden_holder="Proponent of associativity",
        adversary_position="Associativity may fail in non-standard structures.",
        counter_arguments=[
            "Standard number systems are associative.",
            "Non-standard exceptions are outside the scope."
        ],
        resolution_strategy="Restrict to standard number systems.",
        entity_scope="Natural Numbers, Integers, Rationals, Reals",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Peano's Axioms, Field Axioms"
    ),
    DoctrineBlock(
        topic="Multiplicative Identity",
        keywords=["multiplicative identity", "one", "multiplication", "real numbers"],
        conclusion_template="One is the multiplicative identity: {a} × 1 = {a}.",
        reasoning_framework="""
The multiplicative identity is 1, meaning that multiplying any number by 1 leaves it unchanged. 
This property is fundamental to the structure of number systems and is included in the axioms of groups and fields.
""",
        key_factors=["One as identity", "Axiomatic foundation", "Equation solving"],
        primary_authority=["Group Axioms", "Field Axioms", "NCTM Standards"],
        burden_holder="Proponent of the identity property",
        adversary_position="Alternative structures may have different identities.",
        counter_arguments=[
            "In standard arithmetic, one is universally the multiplicative identity.",
            "Other identities are not relevant to standard systems."
        ],
        resolution_strategy="Restrict to standard number systems and cite axioms.",
        entity_scope="Integers, Rationals, Reals",
        confidence=1.0,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Group and Field Axioms"
    ),
    DoctrineBlock(
        topic="Properties of Zero in Multiplication",
        keywords=["zero", "multiplication", "absorption", "real numbers"],
        conclusion_template="Any number multiplied by zero is zero.",
        reasoning_framework="""
Multiplying any number by zero yields zero: a × 0 = 0. 
This is called the absorption property and is fundamental in algebra and arithmetic.
""",
        key_factors=["Absorption", "Multiplication", "Zero"],
        primary_authority=["Algebra Texts", "NCTM Standards", "Field Axioms"],
        burden_holder="Proponent of the property",
        adversary_position="Zero may behave differently in extended systems.",
        counter_arguments=[
            "Standard arithmetic defines the property clearly.",
            "Extensions are outside the basic arithmetic scope."
        ],
        resolution_strategy="Restrict to standard arithmetic and cite axioms.",
        entity_scope="All number systems",
        confidence=1.0,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Field Axioms"
    ),
    DoctrineBlock(
        topic="Properties of One in Exponents",
        keywords=["one", "exponents", "powers", "multiplicative identity"],
        conclusion_template="Any number to the power zero is one (except zero): {a}^0 = 1.",
        reasoning_framework="""
For any nonzero real number a, a^0 = 1. 
This follows from the laws of exponents and the definition of the multiplicative identity. 
Zero to the zero power is undefined or indeterminate.
""",
        key_factors=["Exponent laws", "Multiplicative identity", "Domain restrictions"],
        primary_authority=["Algebra Texts", "NCTM Standards", "Analysis Texts"],
        burden_holder="Proponent of the exponent rule",
        adversary_position="Zero to the zero power is indeterminate.",
        counter_arguments=[
            "Restrict the base to nonzero numbers.",
            "Clarify the definition and exceptions."
        ],
        resolution_strategy="State domain restrictions explicitly.",
        entity_scope="Nonzero Real Numbers",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Algebra Texts"
    ),
    DoctrineBlock(
        topic="Division of Fractions",
        keywords=["division", "fractions", "reciprocal", "multiplication"],
        conclusion_template="{a}/{b} ÷ {c}/{d} = {a} × {d} / ({b} × {c}).",
        reasoning_framework="""
To divide by a fraction, multiply by its reciprocal. 
This is justified by the definition of division as the inverse of multiplication. 
The operation is undefined if the divisor is zero.
""",
        key_factors=["Reciprocal", "Inverse operation", "Domain restrictions"],
        primary_authority=["Elementary Mathematics", "NCTM Standards", "Algebra Texts"],
        burden_holder="Proponent of the division rule",
        adversary_position="Division by zero is undefined.",
        counter_arguments=[
            "Restrict the divisor to nonzero fractions.",
            "Clarify the operation and exceptions."
        ],
        resolution_strategy="State domain restrictions and provide examples.",
        entity_scope="Rational Numbers (with restrictions)",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Elementary Mathematics"
    ),
    DoctrineBlock(
        topic="Addition and Subtraction of Fractions",
        keywords=["addition", "subtraction", "fractions", "common denominator"],
        conclusion_template="{a}/{b} ± {c}/{d} = ({a} × {d} ± {c} × {b}) / ({b} × {d}).",
        reasoning_framework="""
To add or subtract fractions, first find a common denominator. 
Rewrite each fraction with the common denominator, then add or subtract the numerators. 
Simplify the result if possible.
""",
        key_factors=["Common denominator", "Numerator operation", "Simplification"],
        primary_authority=["Elementary Mathematics", "NCTM Standards", "Algebra Texts"],
        burden_holder="Proponent of the operation",
        adversary_position="Complex denominators may complicate computation.",
        counter_arguments=[
            "Use least common denominator for efficiency.",
            "Provide step-by-step procedures."
        ],
        resolution_strategy="Demonstrate with examples and clarify steps.",
        entity_scope="Rational Numbers",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Elementary Mathematics"
    ),
    DoctrineBlock(
        topic="Estimation and Rounding",
        keywords=["estimation", "rounding", "approximation", "place value"],
        conclusion_template="{n} rounded to the nearest {place} is {result}.",
        reasoning_framework="""
Estimation and rounding are techniques for approximating numbers to a specified degree of accuracy. 
Rounding rules depend on place value: if the digit to the right is 5 or more, round up; otherwise, round down. 
Estimation is used for mental math, error analysis, and practical decision-making.
""",
        key_factors=["Place value", "Rounding rules", "Accuracy"],
        primary_authority=["Elementary Mathematics", "NCTM Standards", "Statistics Texts"],
        burden_holder="Proponent of the rounding method",
        adversary_position="Rounding can introduce bias or error.",
        counter_arguments=[
            "Specify the rounding rule used.",
            "Quantify the potential error."
        ],
        resolution_strategy="Clarify the method and context.",
        entity_scope="Real Numbers",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Elementary Mathematics"
    ),
    DoctrineBlock(
        topic="Scientific Notation",
        keywords=["scientific notation", "powers of ten", "standard form", "large numbers"],
        conclusion_template="{n} in scientific notation is {result}.",
        reasoning_framework="""
Scientific notation expresses numbers as a × 10^k, where 1 ≤ |a| < 10 and k is an integer. 
This form is used for very large or very small numbers to simplify computation and comparison. 
Conversion between standard and scientific notation is systematic.
""",
        key_factors=["Powers of ten", "Coefficient", "Exponent"],
        primary_authority=["Elementary Mathematics", "NCTM Standards", "Science Texts"],
        burden_holder="Proponent of the notation",
        adversary_position="Scientific notation may be confusing for beginners.",
        counter_arguments=[
            "Provide clear conversion steps.",
            "Use examples to illustrate."
        ],
        resolution_strategy="Demonstrate with examples and clarify rules.",
        entity_scope="Real Numbers",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Elementary Mathematics"
    ),
    DoctrineBlock(
        topic="Properties of Operations in Modular Arithmetic",
        keywords=["modular arithmetic", "congruence", "operations", "remainder"],
        conclusion_template="{a} ≡ {b} (mod {n}) if {n} divides {a} - {b}.",
        reasoning_framework="""
In modular arithmetic, numbers are considered equivalent if their difference is divisible by the modulus. 
Addition, subtraction, and multiplication are well-defined and inherit properties from integer arithmetic. 
Division is only defined when the divisor is coprime to the modulus.
""",
        key_factors=["Congruence relation", "Well-defined operations", "Coprimality for division"],
        primary_authority=["Number Theory Texts", "NCTM Standards", "Algebra Texts"],
        burden_holder="Proponent of modular operation",
        adversary_position="Division is not always defined in modular arithmetic.",
        counter_arguments=[
            "Division requires coprimality.",
            "Clarify the conditions for each operation."
        ],
        resolution_strategy="State all restrictions and provide examples.",
        entity_scope="Integers modulo n",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Number Theory"
    ),
    DoctrineBlock(
        topic="Properties of Arithmetic Sequences",
        keywords=["arithmetic sequence", "common difference", "progression", "formula"],
        conclusion_template="The nth term of the sequence is {result}.",
        reasoning_framework="""
An arithmetic sequence has a constant difference between consecutive terms. 
The nth term is given by a_n = a_1 + (n-1)d, where a_1 is the first term and d is the common difference. 
The sum of the first n terms is S_n = n/2 × (a_1 + a_n).
""",
        key_factors=["Common difference", "Term formula", "Sum formula"],
        primary_authority=["Algebra Texts", "Elementary Mathematics", "NCTM Standards"],
        burden_holder="Proponent of the sequence formula",
        adversary_position="Non-arithmetic sequences do not follow these formulas.",
        counter_arguments=[
            "Clarify the definition of arithmetic sequence.",
            "Provide counterexamples for other types."
        ],
        resolution_strategy="Restrict to arithmetic sequences and cite formulas.",
        entity_scope="Sequences of real numbers",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Algebra Texts"
    ),
    DoctrineBlock(
        topic="Properties of Geometric Sequences",
        keywords=["geometric sequence", "common ratio", "progression", "formula"],
        conclusion_template="The nth term of the geometric sequence is {result}.",
        reasoning_framework="""
A geometric sequence has a constant ratio between consecutive terms. 
The nth term is a_n = a_1 × r^{n-1}, where a_1 is the first term and r is the common ratio. 
The sum of the first n terms (for r ≠ 1) is S_n = a_1 × (1 - r^n) / (1 - r).
""",
        key_factors=["Common ratio", "Term formula", "Sum formula"],
        primary_authority=["Algebra Texts", "Elementary Mathematics", "NCTM Standards"],
        burden_holder="Proponent of the sequence formula",
        adversary_position="Non-geometric sequences do not follow these formulas.",
        counter_arguments=[
            "Clarify the definition of geometric sequence.",
            "Provide counterexamples for other types."
        ],
        resolution_strategy="Restrict to geometric sequences and cite formulas.",
        entity_scope="Sequences of real numbers",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Algebra Texts"
    ),
    DoctrineBlock(
        topic="Properties of Arithmetic Mean",
        keywords=["arithmetic mean", "average", "sum", "number of terms"],
        conclusion_template="The arithmetic mean of the set is {result}.",
        reasoning_framework="""
The arithmetic mean (average) of a set of numbers is the sum of the numbers divided by the number of terms. 
It is a measure of central tendency and is used in statistics and data analysis.
""",
        key_factors=["Sum", "Number of terms", "Central tendency"],
        primary_authority=["Statistics Texts", "Elementary Mathematics", "NCTM Standards"],
        burden_holder="Proponent of the mean calculation",
        adversary_position="Mean may not represent skewed data accurately.",
        counter_arguments=[
            "Use median or mode for skewed data.",
            "Clarify the context and purpose."
        ],
        resolution_strategy="State the limitations and provide alternatives.",
        entity_scope="Finite sets of real numbers",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Statistics Texts"
    ),
    DoctrineBlock(
        topic="Properties of Median and Mode",
        keywords=["median", "mode", "statistics", "central tendency"],
        conclusion_template="The median is {median}, and the mode is {mode}.",
        reasoning_framework="""
The median is the middle value in an ordered data set; the mode is the value that occurs most frequently. 
Both are measures of central tendency and are less sensitive to outliers than the mean.
""",
        key_factors=["Order", "Frequency", "Outlier resistance"],
        primary_authority=["Statistics Texts", "Elementary Mathematics", "NCTM Standards"],
        burden_holder="Proponent of the calculation",
        adversary_position="Data sets may have multiple modes or no mode.",
        counter_arguments=[
            "Clarify definitions for multimodal or mode-less sets.",
            "Provide examples."
        ],
        resolution_strategy="State all cases and provide examples.",
        entity_scope="Finite sets of real numbers",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Statistics Texts"
    ),
    DoctrineBlock(
        topic="Properties of Commutative, Associative, and Distributive Laws",
        keywords=["commutative", "associative", "distributive", "laws", "arithmetic"],
        conclusion_template="The laws hold for addition and multiplication in standard number systems.",
        reasoning_framework="""
The commutative, associative, and distributive laws are foundational properties of addition and multiplication in arithmetic. 
They enable flexible computation and algebraic manipulation. 
These laws are proven from the axioms of groups and fields and are valid in natural numbers, integers, rationals, and reals.
""",
        key_factors=["Axiomatic foundation", "Algebraic manipulation", "Standard number systems"],
        primary_authority=["Group and Field Axioms", "Algebra Texts", "NCTM Standards"],
        burden_holder="Proponent of the laws",
        adversary_position="Laws may fail in non-standard structures.",
        counter_arguments=[
            "Restrict to standard number systems.",
            "Non-standard exceptions are outside the scope."
        ],
        resolution_strategy="Specify the domain and cite axioms.",
        entity_scope="Natural Numbers, Integers, Rationals, Reals",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Group and Field Axioms"
    ),
    DoctrineBlock(
        topic="Properties of Operations with Zero and One",
        keywords=["zero", "one", "operations", "identity", "absorption"],
        conclusion_template="Zero and one have unique roles as identity and absorption elements.",
        reasoning_framework="""
Zero is the additive identity and absorption element for multiplication. 
One is the multiplicative identity. 
These properties are essential for the structure of number systems and for solving equations.
""",
        key_factors=["Identity", "Absorption", "Equation solving"],
        primary_authority=["Group and Field Axioms", "Algebra Texts", "NCTM Standards"],
        burden_holder="Proponent of the properties",
        adversary_position="Alternative structures may alter these roles.",
        counter_arguments=[
            "Standard arithmetic defines these roles clearly.",
            "Extensions are outside the basic arithmetic scope."
        ],
        resolution_strategy="Restrict to standard arithmetic and cite axioms.",
        entity_scope="All number systems",
        confidence=1.0,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Group and Field Axioms"
    ),
    DoctrineBlock(
        topic="Properties of Negative Exponents",
        keywords=["negative exponents", "powers", "reciprocal", "real numbers"],
        conclusion_template="{a}^{-n} = 1 / {a}^n for a ≠ 0.",
        reasoning_framework="""
Negative exponents represent reciprocals: a^{-n} = 1 / a^n for a ≠ 0. 
This extends the laws of exponents and is justified by the definition of inverse operations.
""",
        key_factors=["Reciprocal", "Exponent laws", "Domain restrictions"],
        primary_authority=["Algebra Texts", "NCTM Standards", "Analysis Texts"],
        burden_holder="Proponent of the exponent rule",
        adversary_position="Zero to a negative exponent is undefined.",
        counter_arguments=[
            "Restrict the base to nonzero numbers.",
            "Clarify the definition and exceptions."
        ],
        resolution_strategy="State domain restrictions explicitly.",
        entity_scope="Nonzero Real Numbers",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Algebra Texts"
    ),
    DoctrineBlock(
        topic="Properties of Zero Exponent",
        keywords=["zero exponent", "powers", "one", "real numbers"],
        conclusion_template="Any nonzero number to the zero power is one: {a}^0 = 1.",
        reasoning_framework="""
For any nonzero real number a, a^0 = 1. 
This follows from the laws of exponents and the definition of the multiplicative identity. 
Zero to the zero power is undefined or indeterminate.
""",
        key_factors=["Exponent laws", "Multiplicative identity", "Domain restrictions"],
        primary_authority=["Algebra Texts", "NCTM Standards", "Analysis Texts"],
        burden_holder="Proponent of the exponent rule",
        adversary_position="Zero to the zero power is indeterminate.",
        counter_arguments=[
            "Restrict the base to nonzero numbers.",
            "Clarify the definition and exceptions."
        ],
        resolution_strategy="State domain restrictions explicitly.",
        entity_scope="Nonzero Real Numbers",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Algebra Texts"
    ),
    DoctrineBlock(
        topic="Properties of Operations with Negative Numbers",
        keywords=["negative numbers", "addition", "subtraction", "multiplication"],
        conclusion_template="Operations with negative numbers follow standard sign rules.",
        reasoning_framework="""
Addition and subtraction of negative numbers follow the rules of additive inverses. 
Multiplication and division follow sign rules: negative × negative = positive, negative × positive = negative, etc. 
These rules are essential for consistency in arithmetic.
""",
        key_factors=["Additive inverse", "Sign rules", "Consistency"],
        primary_authority=["Algebra Texts", "NCTM Standards", "Number Theory"],
        burden_holder="Proponent of the sign rules",
        adversary_position="Sign rules may seem counterintuitive.",
        counter_arguments=[
            "Provide algebraic proofs and examples.",
            "Clarify the rules step by step."
        ],
        resolution_strategy="Demonstrate with examples and clarify rules.",
        entity_scope="Integers, Rationals, Reals",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Algebra Texts"
    ),
    DoctrineBlock(
        topic="Properties of Absolute Value in Equations",
        keywords=["absolute value", "equations", "solutions", "real numbers"],
        conclusion_template="The solutions to |{a}| = {b} are {solutions}.",
        reasoning_framework="""
Equations involving absolute value have two cases: a = b or a = -b. 
Absolute value equations are solved by considering both possibilities and checking for extraneous solutions.
""",
        key_factors=["Two cases", "Extraneous solutions", "Piecewise definition"],
        primary_authority=["Algebra Texts", "NCTM Standards", "Analysis Texts"],
        burden_holder="Proponent of the solution method",
        adversary_position="Extraneous solutions may arise.",
        counter_arguments=[
            "Check all solutions in the original equation.",
            "Clarify the method and provide examples."
        ],
        resolution_strategy="State all cases and verify solutions.",
        entity_scope="Real Numbers",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Algebra Texts"
    ),
    DoctrineBlock(
        topic="Properties of Division by Negative Numbers",
        keywords=["division", "negative numbers", "sign rules", "real numbers"],
        conclusion_template="Dividing by a negative number reverses the sign of the result.",
        reasoning_framework="""
Dividing by a negative number is equivalent to multiplying by its reciprocal, which is also negative. 
This operation reverses the sign of the result and is consistent with the rules of multiplication and division.
""",
        key_factors=["Reciprocal", "Sign reversal", "Consistency"],
        primary_authority=["Algebra Texts", "NCTM Standards", "Number Theory"],
        burden_holder="Proponent of the sign rule",
        adversary_position="Sign rules may seem counterintuitive.",
        counter_arguments=[
            "Provide algebraic proofs and examples.",
            "Clarify the rules step by step."
        ],
        resolution_strategy="Demonstrate with examples and clarify rules.",
        entity_scope="Integers, Rationals, Reals",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Algebra Texts"
    ),
    DoctrineBlock(
        topic="Properties of Zero in Division",
        keywords=["zero", "division", "undefined", "real numbers"],
        conclusion_template="Division by zero is undefined; zero divided by any nonzero number is zero.",
        reasoning_framework="""
Division by zero is undefined in all standard number systems. 
Zero divided by any nonzero number is zero. 
These properties are essential for consistency in arithmetic and algebra.
""",
        key_factors=["Undefined operation", "Zero numerator", "Consistency"],
        primary_authority=["Algebra Texts", "NCTM Standards", "Field Axioms"],
        burden_holder="Proponent of the division rules",
        adversary_position="Division by zero may be defined in extended systems.",
        counter_arguments=[
            "Standard arithmetic does not define division by zero.",
            "Extensions are outside the basic arithmetic scope."
        ],
        resolution_strategy="Restrict to standard arithmetic and cite axioms.",
        entity_scope="All number systems",
        confidence=1.0,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Field Axioms"
    ),
    DoctrineBlock(
        topic="Properties of Operations with Fractions and Decimals",
        keywords=["fractions", "decimals", "operations", "conversion"],
        conclusion_template="Operations with fractions and decimals follow standard rules after conversion.",
        reasoning_framework="""
Fractions and decimals are two representations of rational numbers. 
Operations can be performed directly or by converting between forms. 
Conversion is systematic: fraction to decimal by division, decimal to fraction by place value.
""",
        key_factors=["Conversion", "Standard rules", "Representation"],
        primary_authority=["Elementary Mathematics", "NCTM Standards", "Algebra Texts"],
        burden_holder="Proponent of the operation",
        adversary_position="Conversion may introduce rounding errors.",
        counter_arguments=[
            "Use exact representations where possible.",
            "Quantify and minimize rounding errors."
        ],
        resolution_strategy="Clarify the method and context.",
        entity_scope="Rational Numbers",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Elementary Mathematics"
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
            keyword_lower in doctrine.reasoning_framework.lower()):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]