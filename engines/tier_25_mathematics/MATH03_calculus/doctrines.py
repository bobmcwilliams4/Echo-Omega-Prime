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
        topic="Limits: Definition",
        keywords=["limit", "epsilon-delta", "approach", "convergence"],
        conclusion_template="The limit of f(x) as x approaches a is L.",
        reasoning_framework=(
            "The limit of a function f(x) as x approaches a is L if for every epsilon > 0, "
            "there exists a delta > 0 such that whenever 0 < |x - a| < delta, "
            "it follows that |f(x) - L| < epsilon. This formalizes the intuitive notion of a function "
            "approaching a value as the input approaches a point. The process involves identifying the "
            "appropriate delta for a given epsilon, often by manipulating inequalities and analyzing the "
            "behavior of f(x) near x = a. The existence of the limit is established if such a delta can be "
            "found for every epsilon. If not, the limit does not exist."
        ),
        key_factors=[
            "Behavior of f(x) near x = a",
            "Ability to find delta for every epsilon",
            "Continuity or discontinuity at x = a"
        ],
        primary_authority=[
            "Walter Rudin, Principles of Mathematical Analysis",
            "James Stewart, Calculus"
        ],
        burden_holder="Proponent of the limit's existence",
        adversary_position="No such delta exists for some epsilon; limit does not exist",
        counter_arguments=[
            "Function oscillates or diverges near x = a",
            "Different left and right limits"
        ],
        resolution_strategy="Construct epsilon-delta proof or provide counterexample",
        entity_scope="Real-valued functions of a real variable",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Rudin, Theorem 4.1"
    ),
    DoctrineBlock(
        topic="Limits: One-Sided Limits",
        keywords=["left-hand limit", "right-hand limit", "approach from left", "approach from right"],
        conclusion_template="The left-hand/right-hand limit of f(x) as x approaches a is L.",
        reasoning_framework=(
            "One-sided limits consider the behavior of f(x) as x approaches a from only one direction: "
            "from the left (x → a-) or from the right (x → a+). The left-hand limit exists if for every "
            "epsilon > 0, there exists delta > 0 such that for all x in (a-delta, a), |f(x) - L| < epsilon. "
            "Similarly, the right-hand limit uses (a, a+delta). The overall limit exists at x = a if and only if "
            "both one-sided limits exist and are equal. One-sided limits are crucial for analyzing piecewise "
            "functions and discontinuities."
        ),
        key_factors=[
            "Function definition on one side of a",
            "Behavior as x approaches a from one side",
            "Equality of one-sided limits"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the one-sided limit",
        adversary_position="Limit does not exist from the specified side",
        counter_arguments=[
            "Function is undefined or diverges on one side",
            "Oscillatory behavior on the approach"
        ],
        resolution_strategy="Apply one-sided epsilon-delta definition; check for existence",
        entity_scope="Functions with domain including intervals on one side of a",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 2.2"
    ),
    DoctrineBlock(
        topic="Continuity: Definition",
        keywords=["continuity", "continuous", "limit equals value", "no jump"],
        conclusion_template="The function f(x) is continuous at x = a.",
        reasoning_framework=(
            "A function f(x) is continuous at x = a if three conditions are met: "
            "(1) f(a) is defined, (2) the limit of f(x) as x approaches a exists, and "
            "(3) the limit equals f(a). This ensures there is no 'jump' or 'hole' at x = a. "
            "The epsilon-delta definition of continuity states that for every epsilon > 0, "
            "there exists delta > 0 such that whenever |x - a| < delta, |f(x) - f(a)| < epsilon. "
            "Continuity on an interval requires continuity at every point in the interval."
        ),
        key_factors=[
            "Existence of f(a)",
            "Existence of limit as x → a",
            "Equality of limit and function value"
        ],
        primary_authority=[
            "Walter Rudin, Principles of Mathematical Analysis",
            "James Stewart, Calculus"
        ],
        burden_holder="Proponent of continuity",
        adversary_position="At least one continuity condition fails",
        counter_arguments=[
            "Removable, jump, or infinite discontinuity at x = a",
            "Function undefined at x = a"
        ],
        resolution_strategy="Check all three continuity conditions",
        entity_scope="Functions defined on subsets of the real numbers",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Rudin, Theorem 4.8"
    ),
    DoctrineBlock(
        topic="Continuity: Types of Discontinuity",
        keywords=["removable", "jump", "infinite", "discontinuity"],
        conclusion_template="f(x) has a removable/jump/infinite discontinuity at x = a.",
        reasoning_framework=(
            "Discontinuities are classified as removable, jump, or infinite. "
            "A removable discontinuity occurs when the limit exists at x = a but f(a) is either undefined or not equal to the limit. "
            "A jump discontinuity occurs when the left and right limits exist but are not equal. "
            "An infinite discontinuity occurs when at least one one-sided limit diverges to infinity. "
            "Identifying the type of discontinuity informs possible remedies (e.g., redefining f(a) for removable discontinuities)."
        ),
        key_factors=[
            "Existence and equality of one-sided limits",
            "Definition of f(a)",
            "Behavior near x = a"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the discontinuity classification",
        adversary_position="Discontinuity is of a different type or does not exist",
        counter_arguments=[
            "Misclassification of discontinuity",
            "Function is actually continuous"
        ],
        resolution_strategy="Analyze limits and function value at x = a",
        entity_scope="Functions with isolated discontinuities",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 2.4"
    ),
    DoctrineBlock(
        topic="Intermediate Value Theorem",
        keywords=["IVT", "intermediate value", "continuous", "existence"],
        conclusion_template="There exists c in (a, b) such that f(c) = N.",
        reasoning_framework=(
            "The Intermediate Value Theorem states that if f is continuous on [a, b] and N is any number between f(a) and f(b), "
            "then there exists at least one c in (a, b) such that f(c) = N. The proof relies on the completeness property of real numbers. "
            "The theorem guarantees the existence of a solution but does not specify its value. It is foundational for root-finding methods."
        ),
        key_factors=[
            "Continuity of f on [a, b]",
            "N between f(a) and f(b)"
        ],
        primary_authority=[
            "Walter Rudin, Principles of Mathematical Analysis",
            "James Stewart, Calculus"
        ],
        burden_holder="Proponent of the existence claim",
        adversary_position="Function is not continuous or N is not between f(a) and f(b)",
        counter_arguments=[
            "Discontinuity in [a, b]",
            "N outside the range [f(a), f(b)]"
        ],
        resolution_strategy="Verify continuity and apply IVT",
        entity_scope="Continuous real-valued functions on closed intervals",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Rudin, Theorem 4.23"
    ),
    DoctrineBlock(
        topic="Extreme Value Theorem",
        keywords=["EVT", "maximum", "minimum", "continuous", "attain"],
        conclusion_template="f attains a maximum and minimum on [a, b].",
        reasoning_framework=(
            "The Extreme Value Theorem asserts that if f is continuous on a closed interval [a, b], "
            "then f attains both an absolute maximum and minimum value on [a, b]. "
            "The proof uses the compactness of [a, b] and the continuity of f, ensuring the existence of points "
            "where these extrema occur. The theorem does not guarantee uniqueness."
        ),
        key_factors=[
            "Continuity of f on [a, b]",
            "Closed and bounded interval"
        ],
        primary_authority=[
            "Walter Rudin, Principles of Mathematical Analysis",
            "James Stewart, Calculus"
        ],
        burden_holder="Proponent of the existence of extrema",
        adversary_position="Function is not continuous or interval is not closed",
        counter_arguments=[
            "Discontinuity or open interval",
            "Unbounded function values"
        ],
        resolution_strategy="Check continuity and interval endpoints",
        entity_scope="Continuous real-valued functions on closed intervals",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Rudin, Theorem 4.16"
    ),
    DoctrineBlock(
        topic="Differentiability: Definition",
        keywords=["derivative", "differentiable", "limit", "tangent"],
        conclusion_template="f is differentiable at x = a.",
        reasoning_framework=(
            "A function f is differentiable at x = a if the limit "
            "lim_{h→0} [f(a+h) - f(a)]/h exists. This limit, if it exists, is the derivative f'(a). "
            "Differentiability implies local linearity and the existence of a unique tangent line at x = a. "
            "If the limit does not exist (e.g., due to a corner, cusp, or vertical tangent), f is not differentiable at a."
        ),
        key_factors=[
            "Existence of the limit defining the derivative",
            "Continuity at x = a (necessary but not sufficient)"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of differentiability",
        adversary_position="Limit does not exist or is not finite",
        counter_arguments=[
            "Corner, cusp, or vertical tangent at x = a",
            "Function not continuous at x = a"
        ],
        resolution_strategy="Compute the derivative limit from both sides",
        entity_scope="Functions defined in a neighborhood of a",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 2.7"
    ),
    DoctrineBlock(
        topic="Differentiability Implies Continuity",
        keywords=["differentiability", "continuity", "implication"],
        conclusion_template="If f is differentiable at a, then f is continuous at a.",
        reasoning_framework=(
            "Differentiability at a point implies continuity at that point. "
            "If the derivative exists at x = a, then the limit of f(x) as x approaches a equals f(a). "
            "This follows from the definition of the derivative and the properties of limits. "
            "However, continuity does not imply differentiability."
        ),
        key_factors=[
            "Existence of derivative at x = a",
            "Relationship between limits and function value"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Walter Rudin, Principles of Mathematical Analysis"
        ],
        burden_holder="Proponent of the implication",
        adversary_position="Function is differentiable but not continuous (contradicts definition)",
        counter_arguments=[
            "Misinterpretation of differentiability",
            "Pathological counterexample"
        ],
        resolution_strategy="Apply definition of derivative and continuity",
        entity_scope="Functions differentiable at a point",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 2.8"
    ),
    DoctrineBlock(
        topic="Chain Rule",
        keywords=["chain rule", "composition", "derivative", "function of a function"],
        conclusion_template="The derivative of f(g(x)) is f'(g(x)) * g'(x).",
        reasoning_framework=(
            "The chain rule provides a method for differentiating composite functions. "
            "If y = f(g(x)), then dy/dx = f'(g(x)) * g'(x). The proof uses the limit definition of the derivative "
            "and the substitution of variables. The chain rule is essential for differentiating nested functions, "
            "such as trigonometric, exponential, and logarithmic compositions."
        ),
        key_factors=[
            "Differentiability of inner and outer functions",
            "Correct identification of composition"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the differentiation result",
        adversary_position="Incorrect application or non-differentiability",
        counter_arguments=[
            "One or both functions not differentiable",
            "Misidentification of inner/outer functions"
        ],
        resolution_strategy="Apply chain rule formula and check differentiability",
        entity_scope="Compositions of differentiable functions",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 3.5"
    ),
    DoctrineBlock(
        topic="Product Rule",
        keywords=["product rule", "derivative", "multiplication"],
        conclusion_template="The derivative of f(x)g(x) is f'(x)g(x) + f(x)g'(x).",
        reasoning_framework=(
            "The product rule states that the derivative of the product of two functions is "
            "the derivative of the first times the second plus the first times the derivative of the second. "
            "Formally, (fg)' = f'g + fg'. The proof uses the limit definition of the derivative and algebraic manipulation."
        ),
        key_factors=[
            "Differentiability of both functions",
            "Correct application of the rule"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the derivative formula",
        adversary_position="Incorrect differentiation or non-differentiability",
        counter_arguments=[
            "One or both functions not differentiable",
            "Misapplication of the rule"
        ],
        resolution_strategy="Apply product rule formula",
        entity_scope="Products of differentiable functions",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 3.3"
    ),
    DoctrineBlock(
        topic="Quotient Rule",
        keywords=["quotient rule", "derivative", "division"],
        conclusion_template="The derivative of f(x)/g(x) is [f'(x)g(x) - f(x)g'(x)] / [g(x)]^2.",
        reasoning_framework=(
            "The quotient rule provides a method for differentiating the ratio of two functions. "
            "If y = f(x)/g(x), then y' = [f'(x)g(x) - f(x)g'(x)] / [g(x)]^2, provided g(x) ≠ 0. "
            "The proof uses the product rule and the chain rule applied to the reciprocal of g(x)."
        ),
        key_factors=[
            "Differentiability of numerator and denominator",
            "Denominator nonzero",
            "Correct application of the rule"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the derivative formula",
        adversary_position="g(x) = 0 or incorrect differentiation",
        counter_arguments=[
            "Denominator zero at x",
            "One or both functions not differentiable"
        ],
        resolution_strategy="Apply quotient rule formula and check domain",
        entity_scope="Quotients of differentiable functions with nonzero denominator",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 3.4"
    ),
    DoctrineBlock(
        topic="Mean Value Theorem",
        keywords=["MVT", "mean value", "derivative", "average rate of change"],
        conclusion_template="There exists c in (a, b) such that f'(c) = [f(b) - f(a)] / (b - a).",
        reasoning_framework=(
            "The Mean Value Theorem states that if f is continuous on [a, b] and differentiable on (a, b), "
            "then there exists at least one c in (a, b) such that f'(c) equals the average rate of change "
            "over [a, b]. The proof uses Rolle's Theorem and properties of continuous and differentiable functions. "
            "The MVT is foundational for error estimation and analysis of function behavior."
        ),
        key_factors=[
            "Continuity on [a, b]",
            "Differentiability on (a, b)"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Walter Rudin, Principles of Mathematical Analysis"
        ],
        burden_holder="Proponent of the existence of c",
        adversary_position="Function not continuous or differentiable as required",
        counter_arguments=[
            "Discontinuity or non-differentiability",
            "Open or unbounded interval"
        ],
        resolution_strategy="Verify hypotheses and apply MVT",
        entity_scope="Functions continuous on [a, b] and differentiable on (a, b)",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 4.2"
    ),
    DoctrineBlock(
        topic="Rolle's Theorem",
        keywords=["Rolle's Theorem", "derivative zero", "equal endpoints"],
        conclusion_template="There exists c in (a, b) such that f'(c) = 0.",
        reasoning_framework=(
            "Rolle's Theorem is a special case of the Mean Value Theorem. "
            "If f is continuous on [a, b], differentiable on (a, b), and f(a) = f(b), "
            "then there exists at least one c in (a, b) such that f'(c) = 0. "
            "The proof relies on the Extreme Value Theorem and analysis of the function's maximum or minimum."
        ),
        key_factors=[
            "Continuity on [a, b]",
            "Differentiability on (a, b)",
            "Equal function values at endpoints"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Walter Rudin, Principles of Mathematical Analysis"
        ],
        burden_holder="Proponent of the existence of c",
        adversary_position="Hypotheses not satisfied",
        counter_arguments=[
            "Discontinuity, non-differentiability, or unequal endpoints"
        ],
        resolution_strategy="Verify hypotheses and apply Rolle's Theorem",
        entity_scope="Functions continuous on [a, b] and differentiable on (a, b)",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 4.1"
    ),
    DoctrineBlock(
        topic="Fundamental Theorem of Calculus, Part 1",
        keywords=["FTC", "antiderivative", "integral", "differentiation", "accumulation"],
        conclusion_template="If F(x) = ∫_a^x f(t) dt, then F'(x) = f(x).",
        reasoning_framework=(
            "The Fundamental Theorem of Calculus, Part 1, states that if f is continuous on [a, b], "
            "then the function F defined by F(x) = ∫_a^x f(t) dt is differentiable on (a, b) and F'(x) = f(x). "
            "This establishes the connection between integration and differentiation, showing that integration "
            "can be 'undone' by differentiation. The proof uses the Mean Value Theorem and properties of definite integrals."
        ),
        key_factors=[
            "Continuity of f on [a, b]",
            "Definition of F as an integral"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the differentiability and derivative formula",
        adversary_position="f not continuous or F not properly defined",
        counter_arguments=[
            "Discontinuity of f",
            "Improper definition of F"
        ],
        resolution_strategy="Check continuity and apply FTC Part 1",
        entity_scope="Continuous functions on closed intervals",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 5.3"
    ),
    DoctrineBlock(
        topic="Fundamental Theorem of Calculus, Part 2",
        keywords=["FTC", "evaluation", "antiderivative", "definite integral"],
        conclusion_template="∫_a^b f(x) dx = F(b) - F(a), where F is any antiderivative of f.",
        reasoning_framework=(
            "The Fundamental Theorem of Calculus, Part 2, states that if f is continuous on [a, b] "
            "and F is any antiderivative of f, then the definite integral of f from a to b equals F(b) - F(a). "
            "This theorem provides a practical method for evaluating definite integrals using antiderivatives. "
            "The proof uses properties of Riemann sums and the relationship between differentiation and integration."
        ),
        key_factors=[
            "Continuity of f on [a, b]",
            "Existence of an antiderivative F"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the evaluation formula",
        adversary_position="f not continuous or F not an antiderivative",
        counter_arguments=[
            "Discontinuity of f",
            "Incorrect antiderivative"
        ],
        resolution_strategy="Check continuity and apply FTC Part 2",
        entity_scope="Continuous functions on closed intervals",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 5.4"
    ),
    DoctrineBlock(
        topic="L'Hospital's Rule",
        keywords=["L'Hospital", "indeterminate", "0/0", "∞/∞", "limit", "derivative"],
        conclusion_template="lim_{x→a} f(x)/g(x) = lim_{x→a} f'(x)/g'(x), if the latter limit exists.",
        reasoning_framework=(
            "L'Hospital's Rule provides a method for evaluating limits of the form 0/0 or ∞/∞. "
            "If f and g are differentiable near a, g'(x) ≠ 0 near a, and lim_{x→a} f(x)/g(x) yields an indeterminate form, "
            "then lim_{x→a} f(x)/g(x) = lim_{x→a} f'(x)/g'(x), provided the latter limit exists. "
            "The proof uses Cauchy's Mean Value Theorem. The rule does not apply to other indeterminate forms without manipulation."
        ),
        key_factors=[
            "Indeterminate form 0/0 or ∞/∞",
            "Differentiability of f and g near a",
            "g'(x) ≠ 0 near a"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the limit evaluation",
        adversary_position="Limit not indeterminate or differentiability fails",
        counter_arguments=[
            "Limit not of the correct form",
            "g'(x) = 0 near a"
        ],
        resolution_strategy="Check hypotheses and apply L'Hospital's Rule",
        entity_scope="Limits of quotients with indeterminate forms",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 4.7"
    ),
    DoctrineBlock(
        topic="Taylor's Theorem",
        keywords=["Taylor", "polynomial", "approximation", "remainder", "expansion"],
        conclusion_template="f(x) = P_n(x) + R_n(x), where P_n is the Taylor polynomial of degree n.",
        reasoning_framework=(
            "Taylor's Theorem provides an approximation of a function f(x) near a point a by a polynomial of degree n, "
            "called the Taylor polynomial. The remainder term R_n(x) quantifies the error of the approximation. "
            "If f has n+1 continuous derivatives on an interval containing a, then "
            "f(x) = P_n(x) + R_n(x), where R_n(x) = f^{(n+1)}(c)/(n+1)! * (x-a)^{n+1} for some c between a and x. "
            "The theorem is foundational for series expansions and numerical analysis."
        ),
        key_factors=[
            "Existence of n+1 derivatives",
            "Interval containing a and x"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the approximation and error bound",
        adversary_position="Insufficient differentiability or incorrect remainder",
        counter_arguments=[
            "Function not sufficiently differentiable",
            "Misapplication of the theorem"
        ],
        resolution_strategy="Verify differentiability and compute remainder",
        entity_scope="Functions with n+1 derivatives on interval",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 11.11"
    ),
    DoctrineBlock(
        topic="Uniform Continuity",
        keywords=["uniform continuity", "epsilon-delta", "interval", "Heine–Cantor"],
        conclusion_template="f is uniformly continuous on interval I.",
        reasoning_framework=(
            "A function f is uniformly continuous on an interval I if for every epsilon > 0, "
            "there exists delta > 0 such that for all x, y in I, |x - y| < delta implies |f(x) - f(y)| < epsilon. "
            "Uniform continuity strengthens ordinary continuity by making delta independent of the point. "
            "The Heine–Cantor theorem states that every continuous function on a closed, bounded interval is uniformly continuous."
        ),
        key_factors=[
            "Continuity on interval",
            "Dependence of delta on epsilon only"
        ],
        primary_authority=[
            "Walter Rudin, Principles of Mathematical Analysis",
            "James Stewart, Calculus"
        ],
        burden_holder="Proponent of uniform continuity",
        adversary_position="Delta depends on point or function not continuous",
        counter_arguments=[
            "Function not continuous or interval not closed and bounded",
            "Counterexample showing non-uniformity"
        ],
        resolution_strategy="Apply epsilon-delta definition or Heine–Cantor theorem",
        entity_scope="Functions on intervals",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Rudin, Theorem 4.19"
    ),
    DoctrineBlock(
        topic="Inverse Function Theorem (Single Variable)",
        keywords=["inverse function", "differentiable", "monotonic", "bijective"],
        conclusion_template="If f is differentiable and f'(a) ≠ 0, then f has a differentiable inverse near a.",
        reasoning_framework=(
            "The Inverse Function Theorem for single-variable functions states that if f is differentiable at a, "
            "f'(a) ≠ 0, and f is one-to-one in a neighborhood of a, then f has a differentiable inverse near f(a). "
            "The derivative of the inverse is given by (f^{-1})'(f(a)) = 1 / f'(a). The proof uses the Mean Value Theorem "
            "and properties of monotonic functions."
        ),
        key_factors=[
            "Differentiability at a",
            "Nonzero derivative",
            "Local injectivity"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the existence of inverse and differentiability",
        adversary_position="Derivative zero or function not one-to-one",
        counter_arguments=[
            "f'(a) = 0",
            "Function not locally invertible"
        ],
        resolution_strategy="Check hypotheses and apply theorem",
        entity_scope="Differentiable functions with nonzero derivative",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 4.9"
    ),
    DoctrineBlock(
        topic="Integration by Substitution",
        keywords=["integration", "substitution", "u-substitution", "change of variable"],
        conclusion_template="∫ f(g(x))g'(x) dx = ∫ f(u) du, where u = g(x).",
        reasoning_framework=(
            "Integration by substitution is the reverse of the chain rule. "
            "If u = g(x) is a differentiable function and f is continuous, then "
            "∫ f(g(x))g'(x) dx = ∫ f(u) du. The method simplifies integrals by changing variables, "
            "making them easier to evaluate. The limits of integration must also be adjusted for definite integrals."
        ),
        key_factors=[
            "Differentiability of g(x)",
            "Continuity of f",
            "Correct substitution and limits"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the substitution method",
        adversary_position="Incorrect substitution or function not differentiable",
        counter_arguments=[
            "Improper substitution",
            "Function not differentiable"
        ],
        resolution_strategy="Apply substitution and verify limits",
        entity_scope="Integrals of composite functions",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 5.5"
    ),
    DoctrineBlock(
        topic="Integration by Parts",
        keywords=["integration", "by parts", "product", "antiderivative"],
        conclusion_template="∫ u dv = uv - ∫ v du.",
        reasoning_framework=(
            "Integration by parts is derived from the product rule for differentiation. "
            "If u and v are differentiable functions, then ∫ u dv = uv - ∫ v du. "
            "The method is useful for integrating products of functions, especially when one function is easily differentiable "
            "and the other is easily integrable."
        ),
        key_factors=[
            "Differentiability of u and v",
            "Correct identification of u and dv"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the integration result",
        adversary_position="Improper choice of u or dv",
        counter_arguments=[
            "Functions not differentiable",
            "Misapplication of the formula"
        ],
        resolution_strategy="Apply integration by parts formula",
        entity_scope="Integrals of products of functions",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 7.1"
    ),
    DoctrineBlock(
        topic="Improper Integrals: Convergence",
        keywords=["improper integral", "convergence", "infinite interval", "unbounded integrand"],
        conclusion_template="The improper integral ∫_a^∞ f(x) dx converges/diverges.",
        reasoning_framework=(
            "Improper integrals are defined as limits of definite integrals as the interval becomes infinite "
            "or the integrand becomes unbounded. The integral ∫_a^∞ f(x) dx converges if the limit as b → ∞ of ∫_a^b f(x) dx exists and is finite. "
            "Comparison tests and p-test are commonly used to determine convergence or divergence."
        ),
        key_factors=[
            "Behavior of f(x) as x → ∞ or near singularity",
            "Existence of the limit",
            "Comparison with known convergent/divergent integrals"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of convergence or divergence",
        adversary_position="Limit does not exist or diverges",
        counter_arguments=[
            "Function diverges or comparison test fails",
            "Improper handling of singularity"
        ],
        resolution_strategy="Apply limit definition and comparison tests",
        entity_scope="Integrals over unbounded intervals or with unbounded integrands",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 7.8"
    ),
    DoctrineBlock(
        topic="Convergence of Sequences",
        keywords=["sequence", "convergence", "limit", "bounded", "monotonic"],
        conclusion_template="The sequence {a_n} converges to L.",
        reasoning_framework=(
            "A sequence {a_n} converges to L if for every epsilon > 0, there exists N such that for all n ≥ N, "
            "|a_n - L| < epsilon. The Monotone Convergence Theorem states that every bounded, monotonic sequence converges. "
            "The proof uses the completeness of the real numbers."
        ),
        key_factors=[
            "Boundedness and monotonicity (for MCT)",
            "Epsilon-N definition",
            "Behavior of sequence terms"
        ],
        primary_authority=[
            "Walter Rudin, Principles of Mathematical Analysis",
            "James Stewart, Calculus"
        ],
        burden_holder="Proponent of convergence",
        adversary_position="Sequence diverges or oscillates",
        counter_arguments=[
            "Unbounded or non-monotonic sequence",
            "Counterexample sequence"
        ],
        resolution_strategy="Apply epsilon-N definition or MCT",
        entity_scope="Sequences of real numbers",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Rudin, Theorem 3.14"
    ),
    DoctrineBlock(
        topic="Convergence of Series",
        keywords=["series", "convergence", "sum", "infinite", "test"],
        conclusion_template="The series ∑ a_n converges/diverges.",
        reasoning_framework=(
            "A series ∑ a_n converges if the sequence of partial sums S_n = ∑_{k=1}^n a_k converges. "
            "Tests for convergence include the comparison test, ratio test, root test, and alternating series test. "
            "Absolute convergence implies convergence, but not vice versa. Divergence is established if the terms do not approach zero."
        ),
        key_factors=[
            "Behavior of partial sums",
            "Application of convergence tests",
            "Absolute vs conditional convergence"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Walter Rudin, Principles of Mathematical Analysis"
        ],
        burden_holder="Proponent of convergence or divergence",
        adversary_position="Series diverges or test misapplied",
        counter_arguments=[
            "Terms do not approach zero",
            "Failure of convergence tests"
        ],
        resolution_strategy="Apply appropriate convergence test",
        entity_scope="Infinite series of real numbers",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 11.2"
    ),
    DoctrineBlock(
        topic="Alternating Series Test (Leibniz's Test)",
        keywords=["alternating series", "Leibniz", "convergence", "decreasing", "limit zero"],
        conclusion_template="The alternating series ∑ (-1)^{n} a_n converges.",
        reasoning_framework=(
            "The Alternating Series Test (Leibniz's Test) states that if {a_n} is a sequence of positive, decreasing terms "
            "with lim_{n→∞} a_n = 0, then the alternating series ∑ (-1)^{n} a_n converges. "
            "The proof uses the properties of partial sums and bounded monotonic sequences."
        ),
        key_factors=[
            "Terms positive and decreasing",
            "Limit of terms is zero"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of convergence",
        adversary_position="Terms not decreasing or limit not zero",
        counter_arguments=[
            "Terms not positive or not decreasing",
            "Limit of a_n not zero"
        ],
        resolution_strategy="Check hypotheses and apply test",
        entity_scope="Alternating series with positive terms",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 11.5"
    ),
    DoctrineBlock(
        topic="Absolute and Conditional Convergence",
        keywords=["absolute convergence", "conditional convergence", "series", "sum"],
        conclusion_template="The series ∑ a_n converges absolutely/conditionally.",
        reasoning_framework=(
            "A series ∑ a_n converges absolutely if ∑ |a_n| converges. "
            "Absolute convergence implies convergence. If ∑ a_n converges but ∑ |a_n| diverges, "
            "the series is conditionally convergent. The distinction is important for rearrangement of terms and analysis."
        ),
        key_factors=[
            "Convergence of ∑ |a_n|",
            "Convergence of ∑ a_n"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Walter Rudin, Principles of Mathematical Analysis"
        ],
        burden_holder="Proponent of convergence type",
        adversary_position="Misclassification of convergence",
        counter_arguments=[
            "Series diverges absolutely",
            "Misapplication of tests"
        ],
        resolution_strategy="Test absolute convergence first",
        entity_scope="Infinite series of real numbers",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 11.6"
    ),
    DoctrineBlock(
        topic="Radius and Interval of Convergence (Power Series)",
        keywords=["power series", "radius of convergence", "interval", "convergence", "ratio test"],
        conclusion_template="The power series ∑ a_n (x - c)^n converges for |x - c| < R.",
        reasoning_framework=(
            "The radius of convergence R of a power series ∑ a_n (x - c)^n is found using the ratio or root test. "
            "The series converges absolutely for |x - c| < R and diverges for |x - c| > R. "
            "Convergence at endpoints must be checked separately. The interval of convergence is the set of x for which the series converges."
        ),
        key_factors=[
            "Computation of radius via ratio/root test",
            "Behavior at endpoints",
            "Absolute convergence"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of convergence interval",
        adversary_position="Incorrect computation or endpoint analysis",
        counter_arguments=[
            "Misapplication of tests",
            "Failure to check endpoints"
        ],
        resolution_strategy="Apply ratio/root test and check endpoints",
        entity_scope="Power series in real variable",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 11.8"
    ),
    DoctrineBlock(
        topic="Differentiation and Integration of Power Series",
        keywords=["power series", "differentiation", "integration", "termwise", "radius of convergence"],
        conclusion_template="A power series can be differentiated/integrated termwise within its radius of convergence.",
        reasoning_framework=(
            "Within the radius of convergence, a power series can be differentiated or integrated term by term, "
            "and the resulting series has the same radius of convergence. The proof uses uniform convergence and properties of series."
        ),
        key_factors=[
            "Termwise operations",
            "Radius of convergence",
            "Uniform convergence"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of termwise operation",
        adversary_position="Operation outside radius or non-uniform convergence",
        counter_arguments=[
            "Operation outside radius",
            "Non-uniform convergence"
        ],
        resolution_strategy="Check radius and apply termwise operation",
        entity_scope="Power series within radius of convergence",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 11.9"
    ),
    DoctrineBlock(
        topic="Cauchy-Schwarz Inequality (Calculus Context)",
        keywords=["Cauchy-Schwarz", "inequality", "integral", "inner product"],
        conclusion_template="|∫ f(x)g(x) dx| ≤ (∫ f(x)^2 dx)^{1/2} (∫ g(x)^2 dx)^{1/2}.",
        reasoning_framework=(
            "The Cauchy-Schwarz inequality for integrals states that for square-integrable functions f and g on [a, b], "
            "|∫_a^b f(x)g(x) dx| ≤ (∫_a^b f(x)^2 dx)^{1/2} (∫_a^b g(x)^2 dx)^{1/2}. "
            "The proof uses properties of inner products and the non-negativity of the L^2 norm."
        ),
        key_factors=[
            "Square-integrability of f and g",
            "Properties of inner products"
        ],
        primary_authority=[
            "Walter Rudin, Principles of Mathematical Analysis",
            "James Stewart, Calculus"
        ],
        burden_holder="Proponent of the inequality",
        adversary_position="Functions not square-integrable",
        counter_arguments=[
            "Improper integrability",
            "Violation of hypotheses"
        ],
        resolution_strategy="Verify square-integrability and apply inequality",
        entity_scope="Square-integrable functions on [a, b]",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Rudin, Theorem 3.12"
    ),
    DoctrineBlock(
        topic="Change of Variables in Definite Integrals",
        keywords=["change of variable", "definite integral", "substitution", "limits"],
        conclusion_template="∫_a^b f(g(x))g'(x) dx = ∫_{g(a)}^{g(b)} f(u) du.",
        reasoning_framework=(
            "The change of variables formula for definite integrals allows substitution of u = g(x), "
            "adjusting the limits accordingly. If g is differentiable and f is continuous, then "
            "∫_a^b f(g(x))g'(x) dx = ∫_{g(a)}^{g(b)} f(u) du. The proof uses the Fundamental Theorem of Calculus and chain rule."
        ),
        key_factors=[
            "Differentiability of g(x)",
            "Continuity of f",
            "Correct adjustment of limits"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the substitution",
        adversary_position="Incorrect limits or non-differentiability",
        counter_arguments=[
            "Improper substitution",
            "Function not differentiable"
        ],
        resolution_strategy="Apply substitution and adjust limits",
        entity_scope="Definite integrals with differentiable substitution",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 5.5"
    ),
    DoctrineBlock(
        topic="Integration of Rational Functions by Partial Fractions",
        keywords=["partial fractions", "rational function", "integration", "decomposition"],
        conclusion_template="∫ P(x)/Q(x) dx can be expressed as a sum of simpler integrals via partial fractions.",
        reasoning_framework=(
            "Integration of rational functions involves decomposing P(x)/Q(x) into a sum of simpler fractions, "
            "each of which can be integrated individually. The process requires factoring Q(x), expressing the integrand "
            "as a sum of partial fractions, and integrating each term. The method is effective for proper rational functions."
        ),
        key_factors=[
            "Degree of numerator less than denominator",
            "Factorization of denominator",
            "Correct decomposition"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the decomposition and integration",
        adversary_position="Improper decomposition or irreducible denominator",
        counter_arguments=[
            "Improper rational function",
            "Failure to factor denominator"
        ],
        resolution_strategy="Decompose and integrate each term",
        entity_scope="Proper rational functions",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 7.4"
    ),
    DoctrineBlock(
        topic="Arc Length of a Curve",
        keywords=["arc length", "curve", "integral", "distance"],
        conclusion_template="The arc length of y = f(x) from x = a to x = b is ∫_a^b sqrt(1 + [f'(x)]^2) dx.",
        reasoning_framework=(
            "The arc length of a smooth curve y = f(x) from x = a to x = b is given by "
            "∫_a^b sqrt(1 + [f'(x)]^2) dx. The formula is derived by approximating the curve with line segments, "
            "computing their lengths, and taking the limit as the partition becomes finer."
        ),
        key_factors=[
            "Differentiability of f",
            "Correct application of formula"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the arc length formula",
        adversary_position="Function not differentiable or incorrect formula",
        counter_arguments=[
            "Function not smooth",
            "Misapplication of the formula"
        ],
        resolution_strategy="Verify differentiability and apply formula",
        entity_scope="Smooth curves in the plane",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 8.1"
    ),
    DoctrineBlock(
        topic="Surface Area of Revolution",
        keywords=["surface area", "revolution", "integral", "solid of revolution"],
        conclusion_template="The surface area generated by revolving y = f(x) about the x-axis is ∫_a^b 2π f(x) sqrt(1 + [f'(x)]^2) dx.",
        reasoning_framework=(
            "The surface area of a solid generated by revolving y = f(x), a ≤ x ≤ b, about the x-axis is "
            "∫_a^b 2π f(x) sqrt(1 + [f'(x)]^2) dx. The formula is derived by approximating the surface with frustums "
            "and summing their lateral areas, then taking the limit."
        ),
        key_factors=[
            "Differentiability of f",
            "Non-negativity of f(x)",
            "Correct application of formula"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the surface area formula",
        adversary_position="Function not differentiable or negative values",
        counter_arguments=[
            "Function not smooth",
            "Negative values for f(x)"
        ],
        resolution_strategy="Verify differentiability and non-negativity",
        entity_scope="Smooth, non-negative functions",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 8.2"
    ),
    DoctrineBlock(
        topic="Volume of Revolution (Disk/Washer Method)",
        keywords=["volume", "revolution", "disk method", "washer method", "integral"],
        conclusion_template="The volume is ∫_a^b π [R(x)]^2 dx (disk) or ∫_a^b π ([R(x)]^2 - [r(x)]^2) dx (washer).",
        reasoning_framework=(
            "The volume of a solid generated by revolving a region about the x-axis can be computed using the disk or washer method. "
            "For the disk method, volume = ∫_a^b π [R(x)]^2 dx, where R(x) is the outer radius. "
            "For the washer method, volume = ∫_a^b π ([R(x)]^2 - [r(x)]^2) dx, where r(x) is the inner radius. "
            "The method is based on summing the volumes of infinitesimal disks or washers."
        ),
        key_factors=[
            "Correct identification of radii",
            "Limits of integration",
            "Continuity of bounding functions"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the volume formula",
        adversary_position="Incorrect radii or limits",
        counter_arguments=[
            "Misidentification of radii",
            "Improper limits"
        ],
        resolution_strategy="Apply disk/washer formula with correct bounds",
        entity_scope="Regions bounded by continuous functions",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 6.2"
    ),
    DoctrineBlock(
        topic="Integration of Even and Odd Functions",
        keywords=["even function", "odd function", "integration", "symmetric interval"],
        conclusion_template="∫_{-a}^a f(x) dx = 0 if f is odd; = 2∫_0^a f(x) dx if f is even.",
        reasoning_framework=(
            "If f is an odd function (f(-x) = -f(x)), then the integral over a symmetric interval [-a, a] is zero. "
            "If f is even (f(-x) = f(x)), then the integral is twice the integral from 0 to a. "
            "This follows from the properties of even and odd functions and the symmetry of the interval."
        ),
        key_factors=[
            "Parity of the function",
            "Symmetry of the interval"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the parity and result",
        adversary_position="Function not even/odd or interval not symmetric",
        counter_arguments=[
            "Function lacks required symmetry",
            "Interval not symmetric"
        ],
        resolution_strategy="Verify parity and interval symmetry",
        entity_scope="Integrable functions on symmetric intervals",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 5.3"
    ),
    DoctrineBlock(
        topic="Critical Points and Extrema",
        keywords=["critical point", "extremum", "maximum", "minimum", "derivative zero"],
        conclusion_template="f has a local maximum/minimum at x = c.",
        reasoning_framework=(
            "A critical point occurs where f'(c) = 0 or f'(c) is undefined. "
            "To determine if a critical point is a local maximum or minimum, use the First or Second Derivative Test. "
            "The First Derivative Test examines sign changes of f' around c. "
            "The Second Derivative Test uses the value of f''(c): if f''(c) > 0, local minimum; if f''(c) < 0, local maximum."
        ),
        key_factors=[
            "Existence of critical points",
            "Sign of first and second derivatives",
            "Continuity and differentiability"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of extremum classification",
        adversary_position="Incorrect identification or test misapplied",
        counter_arguments=[
            "Inflection point or saddle point",
            "Test inconclusive"
        ],
        resolution_strategy="Apply derivative tests and analyze sign changes",
        entity_scope="Differentiable functions",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 4.3"
    ),
    DoctrineBlock(
        topic="Inflection Points",
        keywords=["inflection point", "concavity", "second derivative", "change in concavity"],
        conclusion_template="f has an inflection point at x = c.",
        reasoning_framework=(
            "An inflection point occurs at x = c if the concavity of f changes at c. "
            "This is usually detected by f''(c) = 0 and a sign change in f'' around c. "
            "The existence of f''(c) = 0 alone is not sufficient; the sign change must be verified."
        ),
        key_factors=[
            "Second derivative zero at c",
            "Sign change of f'' around c",
            "Continuity of f"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of inflection point",
        adversary_position="No sign change or discontinuity",
        counter_arguments=[
            "No change in concavity",
            "Discontinuity at c"
        ],
        resolution_strategy="Check sign of f'' on both sides of c",
        entity_scope="Twice differentiable functions",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 4.4"
    ),
    DoctrineBlock(
        topic="Optimization Problems",
        keywords=["optimization", "maximum", "minimum", "critical point", "applied"],
        conclusion_template="The maximum/minimum value of f occurs at x = c.",
        reasoning_framework=(
            "Optimization involves finding the maximum or minimum values of a function, often subject to constraints. "
            "The process includes identifying the domain, finding critical points, evaluating endpoints, and comparing values. "
            "The Extreme Value Theorem ensures existence of extrema for continuous functions on closed intervals."
        ),
        key_factors=[
            "Domain and constraints",
            "Critical points and endpoints",
            "Continuity of function"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of optimal value",
        adversary_position="Improper handling of constraints or domain",
        counter_arguments=[
            "Missed critical points",
            "Improper domain analysis"
        ],
        resolution_strategy="Analyze all candidates and compare values",
        entity_scope="Continuous functions on closed intervals",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 4.7"
    ),
    DoctrineBlock(
        topic="Related Rates",
        keywords=["related rates", "implicit differentiation", "rate of change", "application"],
        conclusion_template="The rate of change of y with respect to t is dy/dt = ...",
        reasoning_framework=(
            "Related rates problems involve finding the rate of change of one quantity in terms of another, "
            "often using implicit differentiation with respect to time. The process includes expressing all variables "
            "in terms of time, differentiating both sides, and solving for the desired rate."
        ),
        key_factors=[
            "Relationship between variables",
            "Differentiability",
            "Chain rule application"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the computed rate",
        adversary_position="Incorrect differentiation or relationship",
        counter_arguments=[
            "Misapplication of chain rule",
            "Incorrect relationships"
        ],
        resolution_strategy="Express all variables in terms of time and differentiate",
        entity_scope="Differentiable relationships between variables",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 3.9"
    ),
    DoctrineBlock(
        topic="Implicit Differentiation",
        keywords=["implicit differentiation", "derivative", "implicit function", "chain rule"],
        conclusion_template="dy/dx is computed by differentiating both sides and solving for dy/dx.",
        reasoning_framework=(
            "Implicit differentiation is used when y is defined implicitly as a function of x. "
            "Differentiate both sides of the equation with respect to x, treating y as a function of x, "
            "and solve for dy/dx. The chain rule is essential for differentiating terms involving y."
        ),
        key_factors=[
            "Implicit relationship between x and y",
            "Differentiability",
            "Correct application of chain rule"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the computed derivative",
        adversary_position="Incorrect differentiation",
        counter_arguments=[
            "Failure to apply chain rule",
            "Misidentification of variables"
        ],
        resolution_strategy="Differentiate both sides and solve for dy/dx",
        entity_scope="Implicitly defined differentiable functions",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 3.7"
    ),
    DoctrineBlock(
        topic="Differentials and Linear Approximation",
        keywords=["differential", "linear approximation", "tangent line", "approximate change"],
        conclusion_template="The approximate change in f is df = f'(x) dx.",
        reasoning_framework=(
            "Differentials provide a linear approximation to the change in a function. "
            "If y = f(x), then the differential dy = f'(x) dx approximates the change in y for small dx. "
            "The tangent line at x = a gives the best linear approximation to f near a."
        ),
        key_factors=[
            "Differentiability of f",
            "Small change in x",
            "Tangent line equation"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the approximation",
        adversary_position="Function not differentiable or large dx",
        counter_arguments=[
            "Large dx invalidates approximation",
            "Function not differentiable"
        ],
        resolution_strategy="Apply linear approximation for small dx",
        entity_scope="Differentiable functions",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 3.10"
    ),
    DoctrineBlock(
        topic="Newton's Method",
        keywords=["Newton's method", "root-finding", "iteration", "tangent line"],
        conclusion_template="The next approximation is x_{n+1} = x_n - f(x_n)/f'(x_n).",
        reasoning_framework=(
            "Newton's Method is an iterative algorithm for approximating roots of differentiable functions. "
            "Starting from an initial guess x_0, the sequence x_{n+1} = x_n - f(x_n)/f'(x_n) converges to a root under suitable conditions. "
            "The method uses the tangent line at each iteration to improve the approximation. Convergence is quadratic if the initial guess is close."
        ),
        key_factors=[
            "Differentiability of f",
            "Nonzero derivative at iterates",
            "Good initial guess"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the method and convergence",
        adversary_position="Derivative zero or poor initial guess",
        counter_arguments=[
            "Derivative vanishes",
            "Divergence due to poor guess"
        ],
        resolution_strategy="Check derivative and monitor convergence",
        entity_scope="Root-finding for differentiable functions",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 4.8"
    ),
    DoctrineBlock(
        topic="Indeterminate Forms and Limits",
        keywords=["indeterminate form", "limit", "0/0", "∞/∞", "L'Hospital"],
        conclusion_template="The limit is evaluated by transforming the indeterminate form.",
        reasoning_framework=(
            "Indeterminate forms such as 0/0, ∞/∞, 0×∞, ∞-∞, 0^0, 1^∞, and ∞^0 require special techniques for evaluation. "
            "Methods include algebraic manipulation, L'Hospital's Rule, and logarithmic transformation. "
            "The correct approach depends on the form and the functions involved."
        ),
        key_factors=[
            "Type of indeterminate form",
            "Applicability of L'Hospital's Rule",
            "Algebraic manipulation"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the limit evaluation",
        adversary_position="Incorrect form or method",
        counter_arguments=[
            "Form not indeterminate",
            "Misapplication of rules"
        ],
        resolution_strategy="Identify form and apply appropriate technique",
        entity_scope="Limits involving indeterminate forms",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 4.7"
    ),
    DoctrineBlock(
        topic="Squeeze Theorem",
        keywords=["squeeze theorem", "limit", "bound", "sandwich"],
        conclusion_template="If f(x) ≤ g(x) ≤ h(x) and lim_{x→a} f(x) = lim_{x→a} h(x) = L, then lim_{x→a} g(x) = L.",
        reasoning_framework=(
            "The Squeeze Theorem states that if f(x) ≤ g(x) ≤ h(x) for all x near a (except possibly at a), "
            "and if lim_{x→a} f(x) = lim_{x→a} h(x) = L, then lim_{x→a} g(x) = L. "
            "The proof uses the properties of inequalities and limits."
        ),
        key_factors=[
            "Bounding functions",
            "Equality of bounding limits",
            "Inequality holds near a"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Walter Rudin, Principles of Mathematical Analysis"
        ],
        burden_holder="Proponent of the bounding and limit equality",
        adversary_position="Inequality fails or limits not equal",
        counter_arguments=[
            "Bounding functions not properly defined",
            "Limits of bounds not equal"
        ],
        resolution_strategy="Verify inequalities and compute bounding limits",
        entity_scope="Functions with bounding relationships",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 2.3"
    ),
    DoctrineBlock(
        topic="Parametric Curves: Derivatives and Integrals",
        keywords=["parametric curve", "derivative", "integral", "arc length"],
        conclusion_template="dy/dx = (dy/dt)/(dx/dt); arc length = ∫ sqrt([dx/dt]^2 + [dy/dt]^2) dt.",
        reasoning_framework=(
            "For a curve defined parametrically by x = x(t), y = y(t), the derivative dy/dx is given by (dy/dt)/(dx/dt), "
            "provided dx/dt ≠ 0. The arc length from t = a to t = b is ∫_a^b sqrt([dx/dt]^2 + [dy/dt]^2) dt. "
            "These formulas generalize the concepts of slope and length to parametric representations."
        ),
        key_factors=[
            "Differentiability of x(t) and y(t)",
            "dx/dt ≠ 0 for derivative",
            "Correct limits for arc length"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the parametric formulas",
        adversary_position="dx/dt = 0 or incorrect limits",
        counter_arguments=[
            "dx/dt vanishes",
            "Improper parameterization"
        ],
        resolution_strategy="Verify differentiability and apply formulas",
        entity_scope="Parametric curves with differentiable components",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 10.2"
    ),
    DoctrineBlock(
        topic="Polar Coordinates: Area and Derivatives",
        keywords=["polar coordinates", "area", "derivative", "r(θ)"],
        conclusion_template="Area = (1/2) ∫_α^β [r(θ)]^2 dθ; dy/dx = [dr/dθ sinθ + r cosθ] / [dr/dθ cosθ - r sinθ].",
        reasoning_framework=(
            "For a curve given in polar coordinates r = r(θ), the area enclosed from θ = α to θ = β is "
            "(1/2) ∫_α^β [r(θ)]^2 dθ. The derivative dy/dx is computed using the chain rule and the relationships "
            "x = r cosθ, y = r sinθ. These formulas extend calculus to polar representations."
        ),
        key_factors=[
            "Differentiability of r(θ)",
            "Correct limits of integration",
            "Chain rule application"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 1"
        ],
        burden_holder="Proponent of the polar formulas",
        adversary_position="Incorrect differentiation or limits",
        counter_arguments=[
            "Improper limits",
            "Non-differentiable r(θ)"
        ],
        resolution_strategy="Apply formulas and verify differentiability",
        entity_scope="Curves in polar coordinates",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 10.4"
    ),
    DoctrineBlock(
        topic="Directional Derivative and Gradient (Multivariable)",
        keywords=["directional derivative", "gradient", "multivariable", "partial derivative"],
        conclusion_template="The directional derivative of f at a in direction u is D_u f(a) = ∇f(a) · u.",
        reasoning_framework=(
            "The directional derivative of f at point a in the direction of unit vector u is "
            "D_u f(a) = ∇f(a) · u, where ∇f(a) is the gradient vector. The gradient points in the direction of "
            "maximum increase, and its magnitude gives the rate of increase. The proof uses the definition of the derivative in multiple variables."
        ),
        key_factors=[
            "Differentiability of f",
            "Unit vector direction",
            "Computation of gradient"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 2"
        ],
        burden_holder="Proponent of the derivative computation",
        adversary_position="Function not differentiable or incorrect direction",
        counter_arguments=[
            "Non-differentiable function",
            "Direction not a unit vector"
        ],
        resolution_strategy="Compute gradient and dot with unit vector",
        entity_scope="Differentiable functions of several variables",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 14.6"
    ),
    DoctrineBlock(
        topic="Multiple Integrals: Fubini's Theorem",
        keywords=["multiple integral", "Fubini's Theorem", "double integral", "order of integration"],
        conclusion_template="∬_R f(x, y) dA = ∫_a^b ∫_c^d f(x, y) dy dx (or dx dy).",
        reasoning_framework=(
            "Fubini's Theorem allows the computation of double integrals as iterated integrals. "
            "If f is continuous on a rectangle R = [a, b] × [c, d], then ∬_R f(x, y) dA = ∫_a^b ∫_c^d f(x, y) dy dx = ∫_c^d ∫_a^b f(x, y) dx dy. "
            "The theorem extends to more general regions under certain conditions."
        ),
        key_factors=[
            "Continuity of f on R",
            "Rectangular or simple region",
            "Order of integration"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 2"
        ],
        burden_holder="Proponent of the iterated integral",
        adversary_position="Function not continuous or improper region",
        counter_arguments=[
            "Discontinuity",
            "Region not suitable for Fubini's Theorem"
        ],
        resolution_strategy="Verify continuity and region type",
        entity_scope="Continuous functions on rectangles",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 15.2"
    ),
    DoctrineBlock(
        topic="Change of Variables in Multiple Integrals (Jacobian)",
        keywords=["change of variables", "multiple integral", "Jacobian", "transformation"],
        conclusion_template="∬_R f(x, y) dA = ∬_S f(x(u, v), y(u, v)) |J| du dv.",
        reasoning_framework=(
            "The change of variables formula for double integrals uses the Jacobian determinant. "
            "If (x, y) = T(u, v) is a differentiable, one-to-one transformation with nonzero Jacobian, then "
            "∬_R f(x, y) dA = ∬_S f(x(u, v), y(u, v)) |J| du dv, where |J| is the absolute value of the Jacobian determinant. "
            "The proof uses properties of differentiable mappings and area scaling."
        ),
        key_factors=[
            "Differentiability and invertibility of transformation",
            "Nonzero Jacobian",
            "Proper region mapping"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 2"
        ],
        burden_holder="Proponent of the transformation and Jacobian",
        adversary_position="Transformation not invertible or Jacobian zero",
        counter_arguments=[
            "Singular transformation",
            "Improper region mapping"
        ],
        resolution_strategy="Verify transformation and compute Jacobian",
        entity_scope="Double integrals under differentiable transformations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 15.9"
    ),
    DoctrineBlock(
        topic="Green's Theorem",
        keywords=["Green's Theorem", "line integral", "double integral", "vector field"],
        conclusion_template="∮_C M dx + N dy = ∬_R (N_x - M_y) dA.",
        reasoning_framework=(
            "Green's Theorem relates a line integral around a simple, positively oriented, closed curve C "
            "to a double integral over the region R it encloses. If M and N have continuous partial derivatives on an open region "
            "containing R, then ∮_C M dx + N dy = ∬_R (N_x - M_y) dA. The proof uses properties of vector fields and the Fundamental Theorem of Calculus."
        ),
        key_factors=[
            "Simple, closed, positively oriented curve",
            "Continuity of partial derivatives",
            "Region R in the plane"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 2"
        ],
        burden_holder="Proponent of the theorem's hypotheses",
        adversary_position="Curve not simple/closed or discontinuity",
        counter_arguments=[
            "Curve not simple or not positively oriented",
            "Discontinuity of partial derivatives"
        ],
        resolution_strategy="Verify curve and continuity conditions",
        entity_scope="Vector fields in the plane",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 16.4"
    ),
    DoctrineBlock(
        topic="Divergence Theorem (Gauss's Theorem)",
        keywords=["Divergence Theorem", "Gauss", "flux", "triple integral", "vector field"],
        conclusion_template="∬_S F · n dS = ∭_E div F dV.",
        reasoning_framework=(
            "The Divergence Theorem relates the flux of a vector field F across the closed surface S bounding a region E "
            "to the triple integral of the divergence of F over E. If F has continuous partial derivatives, then "
            "∬_S F · n dS = ∭_E div F dV. The proof uses properties of vector fields and the Fundamental Theorem of Calculus in higher dimensions."
        ),
        key_factors=[
            "Closed surface S bounding region E",
            "Continuity of partial derivatives",
            "Orientation of surface"
        ],
        primary_authority=[
            "James Stewart, Calculus",
            "Tom Apostol, Calculus Vol. 2"
        ],
        burden_holder="Proponent of the theorem's hypotheses",
        adversary_position="Surface not closed or discontinuity",
        counter_arguments=[
            "Surface not closed",
            "Discontinuity of partial derivatives"
        ],
        resolution_strategy="Verify surface and continuity conditions",
        entity_scope="Vector fields in three dimensions",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Stewart, Section 16.9"
    ),
    DoctrineBlock(
        topic="Stokes' Theorem",
        keywords=["Stokes' Theorem", "curl", "surface integral", "line integral", "vector field"],
        conclusion_template="∮_C F · dr = ∬_S curl F · n dS.",
        reasoning_framework=