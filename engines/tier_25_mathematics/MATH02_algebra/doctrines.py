from dataclasses import dataclass, field
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
        topic="Solving Linear Equations",
        keywords=["linear equations", "solving", "algebra", "variables", "isolation"],
        conclusion_template="To solve a linear equation, isolate the variable on one side using inverse operations.",
        reasoning_framework=(
            "1. Identify the variable and constants in the equation.\n"
            "2. Apply inverse operations to both sides to isolate the variable.\n"
            "3. Simplify both sides after each operation.\n"
            "4. Check for like terms and combine if possible.\n"
            "5. Ensure the variable is alone on one side, with all constants on the other.\n"
            "6. Substitute the solution back into the original equation to verify correctness.\n"
            "7. If the equation has no solution (contradiction), state so.\n"
            "8. If the equation is always true (identity), indicate infinite solutions.\n"
            "9. Maintain equivalence at each step by performing the same operation on both sides.\n"
            "10. Document each transformation for clarity and rigor."
        ),
        key_factors=[
            "Correct identification of variable and constants",
            "Appropriate application of inverse operations",
            "Maintaining equation balance",
            "Verification of solution"
        ],
        primary_authority=[
            "Principles of Algebra, Section 2.1",
            "Common Core State Standards: HSA-REI.A.1"
        ],
        burden_holder="Solver",
        adversary_position="Variable cannot be isolated or equation is unsolvable",
        counter_arguments=[
            "Equation is inconsistent (no solution)",
            "Equation is an identity (infinite solutions)",
            "Variable terms cancel out"
        ],
        resolution_strategy="Systematic application of inverse operations and verification.",
        entity_scope="Single-variable linear equations",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Ax=b, where a≠0"
    ),
    DoctrineBlock(
        topic="Factoring Quadratic Equations",
        keywords=["quadratic", "factoring", "trinomial", "roots", "zero product property"],
        conclusion_template="A quadratic equation can be factored into two binomials if it is factorable over the integers.",
        reasoning_framework=(
            "1. Express the quadratic in standard form: ax^2 + bx + c = 0.\n"
            "2. Identify a, b, and c.\n"
            "3. Search for two integers m and n such that m*n = a*c and m + n = b.\n"
            "4. Rewrite the middle term using m and n.\n"
            "5. Factor by grouping.\n"
            "6. Apply the zero product property to solve for x.\n"
            "7. If factoring is not possible, consider alternative methods (completing the square, quadratic formula).\n"
            "8. Verify solutions by substitution."
        ),
        key_factors=[
            "Recognizing standard form",
            "Finding integer factors",
            "Correct grouping",
            "Application of zero product property"
        ],
        primary_authority=[
            "Principles of Algebra, Section 4.2",
            "Common Core State Standards: HSA-REI.B.4"
        ],
        burden_holder="Solver",
        adversary_position="Quadratic is not factorable over integers",
        counter_arguments=[
            "Discriminant is negative (no real roots)",
            "Prime quadratic (cannot be factored over integers)",
            "Incorrect factorization"
        ],
        resolution_strategy="Attempt factoring, then use quadratic formula if necessary.",
        entity_scope="Quadratic equations with real coefficients",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ax^2+bx+c=0, a≠0"
    ),
    DoctrineBlock(
        topic="Quadratic Formula",
        keywords=["quadratic formula", "roots", "discriminant", "solutions", "algebra"],
        conclusion_template="The solutions to ax^2 + bx + c = 0 are given by x = [-b ± sqrt(b^2-4ac)]/(2a).",
        reasoning_framework=(
            "1. Confirm the equation is in the form ax^2 + bx + c = 0.\n"
            "2. Identify coefficients a, b, and c.\n"
            "3. Compute the discriminant D = b^2 - 4ac.\n"
            "4. If D > 0, there are two distinct real roots.\n"
            "5. If D = 0, there is one real root (double root).\n"
            "6. If D < 0, there are two complex roots.\n"
            "7. Substitute a, b, and c into the quadratic formula.\n"
            "8. Simplify the expression to obtain the roots.\n"
            "9. Check solutions by substitution."
        ),
        key_factors=[
            "Correct identification of coefficients",
            "Accurate computation of discriminant",
            "Proper substitution into formula",
            "Recognition of root types"
        ],
        primary_authority=[
            "Principles of Algebra, Section 4.3",
            "Common Core State Standards: HSA-REI.B.4b"
        ],
        burden_holder="Solver",
        adversary_position="Quadratic formula misapplied or coefficients incorrect",
        counter_arguments=[
            "Incorrect discriminant calculation",
            "Misidentification of coefficients",
            "Arithmetic errors"
        ],
        resolution_strategy="Careful substitution and verification of roots.",
        entity_scope="All quadratic equations",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Quadratic Formula"
    ),
    DoctrineBlock(
        topic="Completing the Square",
        keywords=["completing the square", "quadratic", "vertex form", "algebra"],
        conclusion_template="Completing the square rewrites ax^2 + bx + c as a(x-h)^2 + k.",
        reasoning_framework=(
            "1. Ensure the quadratic is in standard form.\n"
            "2. If a ≠ 1, factor a from the x^2 and x terms.\n"
            "3. Take half of the coefficient of x, square it, and add and subtract inside the parenthesis.\n"
            "4. Rewrite as a perfect square trinomial.\n"
            "5. Express in vertex form a(x-h)^2 + k.\n"
            "6. Use this form to identify the vertex and solve equations as needed.\n"
            "7. Check by expanding to confirm equivalence."
        ),
        key_factors=[
            "Factoring out leading coefficient",
            "Correct calculation of (b/2)^2",
            "Maintaining equation balance",
            "Accurate rewriting"
        ],
        primary_authority=[
            "Principles of Algebra, Section 4.4",
            "Common Core State Standards: HSA-REI.B.4a"
        ],
        burden_holder="Solver",
        adversary_position="Incorrect completion or misapplication",
        counter_arguments=[
            "Arithmetic errors in squaring",
            "Forgetting to balance equation",
            "Incorrect factorization"
        ],
        resolution_strategy="Stepwise transformation and verification by expansion.",
        entity_scope="Quadratic equations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Completing the Square"
    ),
    DoctrineBlock(
        topic="Systems of Linear Equations (Substitution)",
        keywords=["systems", "linear equations", "substitution", "simultaneous equations"],
        conclusion_template="Solve one equation for a variable, substitute into the other, and solve for remaining variables.",
        reasoning_framework=(
            "1. Choose one equation and solve for one variable in terms of the other.\n"
            "2. Substitute this expression into the other equation.\n"
            "3. Solve the resulting single-variable equation.\n"
            "4. Back-substitute to find the other variable.\n"
            "5. Check the solution in both original equations.\n"
            "6. If equations are dependent, infinite solutions exist.\n"
            "7. If inconsistent, no solution exists."
        ),
        key_factors=[
            "Correct isolation of variable",
            "Accurate substitution",
            "Verification in both equations"
        ],
        primary_authority=[
            "Principles of Algebra, Section 5.1",
            "Common Core State Standards: HSA-REI.C.6"
        ],
        burden_holder="Solver",
        adversary_position="No solution or infinite solutions",
        counter_arguments=[
            "Equations are inconsistent",
            "Equations are dependent",
            "Arithmetic or substitution errors"
        ],
        resolution_strategy="Systematic substitution and checking for consistency.",
        entity_scope="Systems of two linear equations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Substitution Method"
    ),
    DoctrineBlock(
        topic="Systems of Linear Equations (Elimination)",
        keywords=["systems", "elimination", "linear equations", "addition", "subtraction"],
        conclusion_template="Add or subtract equations to eliminate a variable, then solve for the remaining variable.",
        reasoning_framework=(
            "1. Align equations in standard form.\n"
            "2. Multiply one or both equations to align coefficients of one variable.\n"
            "3. Add or subtract equations to eliminate that variable.\n"
            "4. Solve for the remaining variable.\n"
            "5. Substitute back to find the other variable.\n"
            "6. Check the solution in both equations.\n"
            "7. Analyze for special cases: dependent or inconsistent systems."
        ),
        key_factors=[
            "Alignment of coefficients",
            "Correct addition/subtraction",
            "Verification in both equations"
        ],
        primary_authority=[
            "Principles of Algebra, Section 5.2",
            "Common Core State Standards: HSA-REI.C.5"
        ],
        burden_holder="Solver",
        adversary_position="No unique solution",
        counter_arguments=[
            "Equations are multiples (dependent)",
            "No intersection (inconsistent)",
            "Arithmetic errors"
        ],
        resolution_strategy="Careful elimination and back-substitution.",
        entity_scope="Systems of two linear equations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Elimination Method"
    ),
    DoctrineBlock(
        topic="Inequalities (Linear)",
        keywords=["inequalities", "linear", "algebra", "solution set", "interval notation"],
        conclusion_template="Solve linear inequalities as equations, but reverse the inequality when multiplying/dividing by a negative.",
        reasoning_framework=(
            "1. Treat the inequality like an equation for solving.\n"
            "2. Apply inverse operations to isolate the variable.\n"
            "3. If multiplying/dividing by a negative, reverse the inequality sign.\n"
            "4. Express the solution in interval notation or on a number line.\n"
            "5. Check boundary points and test values.\n"
            "6. Consider compound inequalities if present."
        ),
        key_factors=[
            "Reversal of inequality when required",
            "Accurate solution set representation",
            "Verification of solution"
        ],
        primary_authority=[
            "Principles of Algebra, Section 6.1",
            "Common Core State Standards: HSA-REI.B.3"
        ],
        burden_holder="Solver",
        adversary_position="Incorrect handling of inequality sign",
        counter_arguments=[
            "Forgetting to reverse the sign",
            "Incorrect interval notation",
            "Boundary value errors"
        ],
        resolution_strategy="Careful attention to sign changes and solution representation.",
        entity_scope="Linear inequalities in one variable",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Linear Inequality Solution"
    ),
    DoctrineBlock(
        topic="Absolute Value Equations",
        keywords=["absolute value", "equations", "piecewise", "algebra"],
        conclusion_template="An absolute value equation |A| = B has solutions A = B or A = -B, provided B ≥ 0.",
        reasoning_framework=(
            "1. Isolate the absolute value expression.\n"
            "2. Set up two equations: one with the expression equal to B, one equal to -B.\n"
            "3. Solve each equation separately.\n"
            "4. Check for extraneous solutions, especially if B < 0 (no solution).\n"
            "5. Substitute solutions into the original equation to verify."
        ),
        key_factors=[
            "Isolating the absolute value",
            "Setting up correct cases",
            "Checking for extraneous solutions"
        ],
        primary_authority=[
            "Principles of Algebra, Section 6.2",
            "Common Core State Standards: HSA-REI.B.3"
        ],
        burden_holder="Solver",
        adversary_position="No real solution if B < 0",
        counter_arguments=[
            "B negative (no solution)",
            "Extraneous solutions from squaring",
            "Arithmetic errors"
        ],
        resolution_strategy="Systematic case analysis and verification.",
        entity_scope="Absolute value equations in one variable",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Absolute Value Solution"
    ),
    DoctrineBlock(
        topic="Absolute Value Inequalities",
        keywords=["absolute value", "inequalities", "piecewise", "intervals"],
        conclusion_template="|A| < B becomes -B < A < B; |A| > B becomes A < -B or A > B.",
        reasoning_framework=(
            "1. Isolate the absolute value expression.\n"
            "2. For |A| < B (B > 0), rewrite as -B < A < B.\n"
            "3. For |A| > B (B > 0), rewrite as A < -B or A > B.\n"
            "4. Solve the resulting compound inequalities.\n"
            "5. Express the solution set in interval notation.\n"
            "6. Check for extraneous solutions and boundary cases."
        ),
        key_factors=[
            "Correct case analysis",
            "Accurate interval notation",
            "Boundary value consideration"
        ],
        primary_authority=[
            "Principles of Algebra, Section 6.3",
            "Common Core State Standards: HSA-REI.B.3"
        ],
        burden_holder="Solver",
        adversary_position="Incorrect interval or case analysis",
        counter_arguments=[
            "B negative (no solution)",
            "Incorrect compound inequality",
            "Boundary errors"
        ],
        resolution_strategy="Careful case separation and interval representation.",
        entity_scope="Absolute value inequalities in one variable",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Absolute Value Inequality Solution"
    ),
    DoctrineBlock(
        topic="Exponents (Product Rule)",
        keywords=["exponents", "product rule", "algebra", "powers"],
        conclusion_template="When multiplying like bases, add the exponents: a^m * a^n = a^{m+n}.",
        reasoning_framework=(
            "1. Identify terms with the same base.\n"
            "2. Apply the product rule: a^m * a^n = a^{m+n}.\n"
            "3. Combine exponents by addition.\n"
            "4. Simplify the expression.\n"
            "5. Check for special cases (zero or negative exponents)."
        ),
        key_factors=[
            "Same base identification",
            "Correct exponent addition",
            "Simplification"
        ],
        primary_authority=[
            "Principles of Algebra, Section 7.1",
            "Common Core State Standards: HSA-SSE.A.1"
        ],
        burden_holder="Solver",
        adversary_position="Bases are not the same",
        counter_arguments=[
            "Different bases",
            "Arithmetic errors in addition",
            "Misapplication of rule"
        ],
        resolution_strategy="Verify bases and add exponents only when appropriate.",
        entity_scope="Expressions with exponents",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Exponent Product Rule"
    ),
    DoctrineBlock(
        topic="Exponents (Quotient Rule)",
        keywords=["exponents", "quotient rule", "algebra", "powers"],
        conclusion_template="When dividing like bases, subtract the exponents: a^m / a^n = a^{m-n}.",
        reasoning_framework=(
            "1. Identify terms with the same base.\n"
            "2. Apply the quotient rule: a^m / a^n = a^{m-n}.\n"
            "3. Subtract exponents (numerator minus denominator).\n"
            "4. Simplify the expression.\n"
            "5. Address negative exponents as reciprocals."
        ),
        key_factors=[
            "Same base identification",
            "Correct exponent subtraction",
            "Handling negative exponents"
        ],
        primary_authority=[
            "Principles of Algebra, Section 7.2",
            "Common Core State Standards: HSA-SSE.A.1"
        ],
        burden_holder="Solver",
        adversary_position="Bases are not the same or negative exponents mishandled",
        counter_arguments=[
            "Different bases",
            "Arithmetic errors in subtraction",
            "Negative exponent confusion"
        ],
        resolution_strategy="Careful base comparison and exponent arithmetic.",
        entity_scope="Expressions with exponents",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Exponent Quotient Rule"
    ),
    DoctrineBlock(
        topic="Exponents (Power of a Power)",
        keywords=["exponents", "power of a power", "algebra", "powers"],
        conclusion_template="When raising a power to a power, multiply the exponents: (a^m)^n = a^{mn}.",
        reasoning_framework=(
            "1. Identify the base and exponents.\n"
            "2. Apply the rule: (a^m)^n = a^{m*n}.\n"
            "3. Multiply the exponents.\n"
            "4. Simplify the expression.\n"
            "5. Check for special cases (zero or negative exponents)."
        ),
        key_factors=[
            "Correct identification of exponents",
            "Accurate multiplication",
            "Simplification"
        ],
        primary_authority=[
            "Principles of Algebra, Section 7.3",
            "Common Core State Standards: HSA-SSE.A.1"
        ],
        burden_holder="Solver",
        adversary_position="Exponents added instead of multiplied",
        counter_arguments=[
            "Arithmetic errors in multiplication",
            "Misapplication of rule",
            "Negative exponent confusion"
        ],
        resolution_strategy="Multiply exponents only when raising a power to a power.",
        entity_scope="Expressions with exponents",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Exponent Power Rule"
    ),
    DoctrineBlock(
        topic="Exponents (Zero and Negative Exponents)",
        keywords=["exponents", "zero exponent", "negative exponent", "algebra"],
        conclusion_template="a^0 = 1 for a ≠ 0; a^{-n} = 1/a^n.",
        reasoning_framework=(
            "1. Recognize that any nonzero base raised to the zero power is 1.\n"
            "2. For negative exponents, rewrite as the reciprocal of the positive exponent.\n"
            "3. Simplify expressions using these rules.\n"
            "4. Avoid zero in the denominator.\n"
            "5. Check for special cases (a=0)."
        ),
        key_factors=[
            "Correct application of zero and negative exponent rules",
            "Avoiding division by zero",
            "Simplification"
        ],
        primary_authority=[
            "Principles of Algebra, Section 7.4",
            "Common Core State Standards: HSA-SSE.A.1"
        ],
        burden_holder="Solver",
        adversary_position="Base is zero or negative exponents mishandled",
        counter_arguments=[
            "Division by zero",
            "Negative exponent confusion",
            "Misapplication of zero exponent rule"
        ],
        resolution_strategy="Careful application of rules and avoidance of undefined expressions.",
        entity_scope="Expressions with exponents",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Zero and Negative Exponent Rules"
    ),
    DoctrineBlock(
        topic="Polynomials (Addition and Subtraction)",
        keywords=["polynomials", "addition", "subtraction", "like terms", "algebra"],
        conclusion_template="Add or subtract polynomials by combining like terms.",
        reasoning_framework=(
            "1. Align polynomials in standard form.\n"
            "2. Identify and combine like terms (same variable and exponent).\n"
            "3. Add or subtract coefficients as appropriate.\n"
            "4. Write the result in standard form, ordered by descending degree.\n"
            "5. Check for missing terms and verify arithmetic."
        ),
        key_factors=[
            "Identification of like terms",
            "Correct coefficient arithmetic",
            "Standard form representation"
        ],
        primary_authority=[
            "Principles of Algebra, Section 8.1",
            "Common Core State Standards: HSA-APR.A.1"
        ],
        burden_holder="Solver",
        adversary_position="Like terms not properly combined",
        counter_arguments=[
            "Terms not aligned",
            "Arithmetic errors",
            "Incorrect standard form"
        ],
        resolution_strategy="Careful alignment and combination of like terms.",
        entity_scope="Polynomial expressions",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Polynomial Addition/Subtraction"
    ),
    DoctrineBlock(
        topic="Polynomials (Multiplication)",
        keywords=["polynomials", "multiplication", "distributive property", "FOIL", "algebra"],
        conclusion_template="Multiply polynomials using distributive property, combining like terms.",
        reasoning_framework=(
            "1. Apply the distributive property (a(b + c) = ab + ac).\n"
            "2. For binomials, use FOIL (First, Outer, Inner, Last).\n"
            "3. Multiply each term in one polynomial by each term in the other.\n"
            "4. Combine like terms.\n"
            "5. Write the result in standard form.\n"
            "6. Check for arithmetic errors."
        ),
        key_factors=[
            "Correct application of distributive property",
            "Comprehensive term multiplication",
            "Combination of like terms"
        ],
        primary_authority=[
            "Principles of Algebra, Section 8.2",
            "Common Core State Standards: HSA-APR.A.1"
        ],
        burden_holder="Solver",
        adversary_position="Terms omitted or not combined",
        counter_arguments=[
            "Incomplete multiplication",
            "Arithmetic errors",
            "Incorrect standard form"
        ],
        resolution_strategy="Systematic multiplication and careful combination of terms.",
        entity_scope="Polynomial expressions",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Polynomial Multiplication"
    ),
    DoctrineBlock(
        topic="Polynomials (Division and Synthetic Division)",
        keywords=["polynomials", "division", "synthetic division", "long division", "algebra"],
        conclusion_template="Divide polynomials using long or synthetic division, expressing the result as quotient plus remainder.",
        reasoning_framework=(
            "1. Arrange the dividend and divisor in descending order of degree.\n"
            "2. For long division, divide the leading term of the dividend by the leading term of the divisor.\n"
            "3. Multiply the divisor by the result and subtract from the dividend.\n"
            "4. Repeat until the degree of the remainder is less than the divisor.\n"
            "5. For synthetic division, use when the divisor is linear (x - c).\n"
            "6. Express the result as quotient plus remainder over divisor.\n"
            "7. Check by multiplying divisor and quotient and adding remainder."
        ),
        key_factors=[
            "Correct arrangement of terms",
            "Accurate division and subtraction",
            "Appropriate use of synthetic division"
        ],
        primary_authority=[
            "Principles of Algebra, Section 8.3",
            "Common Core State Standards: HSA-APR.B.2"
        ],
        burden_holder="Solver",
        adversary_position="Division steps omitted or remainder mishandled",
        counter_arguments=[
            "Incorrect arrangement",
            "Arithmetic errors",
            "Remainder not properly expressed"
        ],
        resolution_strategy="Stepwise division and verification by multiplication.",
        entity_scope="Polynomial division",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Polynomial Division"
    ),
    DoctrineBlock(
        topic="Factoring by Grouping",
        keywords=["factoring", "grouping", "polynomials", "algebra"],
        conclusion_template="Group terms to factor common factors, then factor the resulting expression.",
        reasoning_framework=(
            "1. Divide the polynomial into two groups.\n"
            "2. Factor out the greatest common factor (GCF) from each group.\n"
            "3. If the remaining binomials are identical, factor them out.\n"
            "4. Write the expression as a product of two factors.\n"
            "5. Check by expanding to verify equivalence."
        ),
        key_factors=[
            "Correct grouping",
            "Identification of GCF",
            "Verification by expansion"
        ],
        primary_authority=[
            "Principles of Algebra, Section 9.2",
            "Common Core State Standards: HSA-APR.A.1"
        ],
        burden_holder="Solver",
        adversary_position="Grouping does not yield common factor",
        counter_arguments=[
            "Incorrect grouping",
            "GCF not factored",
            "Expansion does not match original"
        ],
        resolution_strategy="Systematic grouping and verification.",
        entity_scope="Polynomials with four or more terms",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Factoring by Grouping"
    ),
    DoctrineBlock(
        topic="Greatest Common Factor (GCF)",
        keywords=["GCF", "greatest common factor", "factoring", "algebra"],
        conclusion_template="The GCF of terms is the largest expression that divides all terms without remainder.",
        reasoning_framework=(
            "1. List all factors of each term.\n"
            "2. Identify the largest factor common to all terms.\n"
            "3. For variables, use the lowest power present in all terms.\n"
            "4. Factor out the GCF from the expression.\n"
            "5. Check by distributing to ensure equivalence."
        ),
        key_factors=[
            "Accurate factor listing",
            "Correct identification of GCF",
            "Verification by distribution"
        ],
        primary_authority=[
            "Principles of Algebra, Section 9.1",
            "Common Core State Standards: HSA-SSE.A.2"
        ],
        burden_holder="Solver",
        adversary_position="GCF not properly identified",
        counter_arguments=[
            "Overlooking common factors",
            "Incorrect variable powers",
            "Distribution error"
        ],
        resolution_strategy="Careful analysis and distribution check.",
        entity_scope="Polynomial expressions",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="GCF Factoring"
    ),
    DoctrineBlock(
        topic="Difference of Squares",
        keywords=["factoring", "difference of squares", "algebra"],
        conclusion_template="a^2 - b^2 = (a + b)(a - b).",
        reasoning_framework=(
            "1. Recognize the expression as a difference of two squares.\n"
            "2. Identify a and b such that the terms are perfect squares.\n"
            "3. Apply the formula: a^2 - b^2 = (a + b)(a - b).\n"
            "4. Expand to verify correctness.\n"
            "5. Check for further factorization if possible."
        ),
        key_factors=[
            "Identification of perfect squares",
            "Correct application of formula",
            "Verification by expansion"
        ],
        primary_authority=[
            "Principles of Algebra, Section 9.3",
            "Common Core State Standards: HSA-SSE.A.2"
        ],
        burden_holder="Solver",
        adversary_position="Expression is not a difference of squares",
        counter_arguments=[
            "Terms not perfect squares",
            "Sum of squares (not factorable over reals)",
            "Arithmetic errors"
        ],
        resolution_strategy="Careful identification and formula application.",
        entity_scope="Binomial expressions",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Difference of Squares"
    ),
    DoctrineBlock(
        topic="Sum and Difference of Cubes",
        keywords=["factoring", "sum of cubes", "difference of cubes", "algebra"],
        conclusion_template="a^3 + b^3 = (a + b)(a^2 - ab + b^2); a^3 - b^3 = (a - b)(a^2 + ab + b^2).",
        reasoning_framework=(
            "1. Recognize the expression as a sum or difference of cubes.\n"
            "2. Identify a and b such that the terms are perfect cubes.\n"
            "3. Apply the appropriate formula:\n"
            "   a^3 + b^3 = (a + b)(a^2 - ab + b^2)\n"
            "   a^3 - b^3 = (a - b)(a^2 + ab + b^2)\n"
            "4. Expand to verify correctness.\n"
            "5. Check for further factorization if possible."
        ),
        key_factors=[
            "Identification of perfect cubes",
            "Correct formula application",
            "Verification by expansion"
        ],
        primary_authority=[
            "Principles of Algebra, Section 9.4",
            "Common Core State Standards: HSA-SSE.A.2"
        ],
        burden_holder="Solver",
        adversary_position="Expression is not a sum/difference of cubes",
        counter_arguments=[
            "Terms not perfect cubes",
            "Arithmetic errors",
            "Incorrect formula"
        ],
        resolution_strategy="Careful identification and formula application.",
        entity_scope="Binomial expressions",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Sum/Difference of Cubes"
    ),
    DoctrineBlock(
        topic="Rational Expressions (Simplification)",
        keywords=["rational expressions", "simplification", "algebra", "fractions"],
        conclusion_template="Simplify rational expressions by factoring numerator and denominator, then canceling common factors.",
        reasoning_framework=(
            "1. Factor numerator and denominator completely.\n"
            "2. Identify and cancel common factors.\n"
            "3. State restrictions on variable values (denominator ≠ 0).\n"
            "4. Express the simplified form.\n"
            "5. Check by multiplying back to original."
        ),
        key_factors=[
            "Complete factoring",
            "Identification of common factors",
            "Domain restrictions"
        ],
        primary_authority=[
            "Principles of Algebra, Section 10.1",
            "Common Core State Standards: HSA-APR.D.6"
        ],
        burden_holder="Solver",
        adversary_position="Factors not fully canceled or domain not stated",
        counter_arguments=[
            "Omitted restrictions",
            "Incomplete factoring",
            "Arithmetic errors"
        ],
        resolution_strategy="Thorough factoring and explicit domain statement.",
        entity_scope="Rational expressions",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Rational Expression Simplification"
    ),
    DoctrineBlock(
        topic="Rational Expressions (Addition and Subtraction)",
        keywords=["rational expressions", "addition", "subtraction", "common denominator"],
        conclusion_template="Add or subtract rational expressions by finding a common denominator.",
        reasoning_framework=(
            "1. Factor denominators to find the least common denominator (LCD).\n"
            "2. Rewrite each expression with the LCD.\n"
            "3. Add or subtract numerators, keeping the denominator.\n"
            "4. Simplify the numerator if possible.\n"
            "5. State restrictions on variable values (denominator ≠ 0).\n"
            "6. Simplify the final expression."
        ),
        key_factors=[
            "Correct identification of LCD",
            "Accurate rewriting of expressions",
            "Domain restrictions"
        ],
        primary_authority=[
            "Principles of Algebra, Section 10.2",
            "Common Core State Standards: HSA-APR.D.7"
        ],
        burden_holder="Solver",
        adversary_position="LCD not properly found or restrictions omitted",
        counter_arguments=[
            "Incorrect LCD",
            "Omitted restrictions",
            "Arithmetic errors"
        ],
        resolution_strategy="Systematic LCD identification and explicit domain statement.",
        entity_scope="Rational expressions",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Rational Expression Addition/Subtraction"
    ),
    DoctrineBlock(
        topic="Rational Expressions (Multiplication and Division)",
        keywords=["rational expressions", "multiplication", "division", "factoring"],
        conclusion_template="Multiply numerators and denominators, cancel common factors; for division, multiply by the reciprocal.",
        reasoning_framework=(
            "1. Factor all numerators and denominators.\n"
            "2. For multiplication, multiply numerators and denominators.\n"
            "3. For division, multiply by the reciprocal of the divisor.\n"
            "4. Cancel common factors.\n"
            "5. State restrictions on variable values (denominator ≠ 0).\n"
            "6. Simplify the final expression."
        ),
        key_factors=[
            "Factoring before multiplication/division",
            "Correct reciprocal application",
            "Domain restrictions"
        ],
        primary_authority=[
            "Principles of Algebra, Section 10.3",
            "Common Core State Standards: HSA-APR.D.7"
        ],
        burden_holder="Solver",
        adversary_position="Reciprocal not applied or restrictions omitted",
        counter_arguments=[
            "Incorrect reciprocal",
            "Omitted restrictions",
            "Arithmetic errors"
        ],
        resolution_strategy="Careful factoring and explicit domain statement.",
        entity_scope="Rational expressions",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Rational Expression Multiplication/Division"
    ),
    DoctrineBlock(
        topic="Radicals (Simplification)",
        keywords=["radicals", "simplification", "square roots", "algebra"],
        conclusion_template="Simplify radicals by factoring out perfect squares and expressing in simplest form.",
        reasoning_framework=(
            "1. Factor the radicand to identify perfect square factors.\n"
            "2. Rewrite the radical as the product of the square root of the perfect square and the remaining factor.\n"
            "3. Simplify the square root of the perfect square.\n"
            "4. Express the radical in simplest form.\n"
            "5. Check by squaring the result."
        ),
        key_factors=[
            "Identification of perfect squares",
            "Accurate factoring",
            "Simplification"
        ],
        primary_authority=[
            "Principles of Algebra, Section 11.1",
            "Common Core State Standards: HSN-RN.A.2"
        ],
        burden_holder="Solver",
        adversary_position="Radical not fully simplified",
        counter_arguments=[
            "Overlooking perfect squares",
            "Arithmetic errors",
            "Incorrect simplification"
        ],
        resolution_strategy="Thorough factoring and verification by squaring.",
        entity_scope="Radical expressions",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Radical Simplification"
    ),
    DoctrineBlock(
        topic="Radicals (Addition and Subtraction)",
        keywords=["radicals", "addition", "subtraction", "like radicals", "algebra"],
        conclusion_template="Add or subtract radicals only if they are like radicals (same index and radicand).",
        reasoning_framework=(
            "1. Simplify each radical to its simplest form.\n"
            "2. Identify like radicals (same index and radicand).\n"
            "3. Add or subtract coefficients of like radicals.\n"
            "4. Write the result in simplest form.\n"
            "5. Check for further simplification."
        ),
        key_factors=[
            "Identification of like radicals",
            "Simplification before combining",
            "Correct coefficient arithmetic"
        ],
        primary_authority=[
            "Principles of Algebra, Section 11.2",
            "Common Core State Standards: HSN-RN.A.2"
        ],
        burden_holder="Solver",
        adversary_position="Radicals not simplified or not like",
        counter_arguments=[
            "Radicals not like",
            "Arithmetic errors",
            "Incomplete simplification"
        ],
        resolution_strategy="Simplify first, then combine like radicals.",
        entity_scope="Radical expressions",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Radical Addition/Subtraction"
    ),
    DoctrineBlock(
        topic="Radicals (Multiplication and Division)",
        keywords=["radicals", "multiplication", "division", "algebra"],
        conclusion_template="Multiply/divide radicals with the same index by multiplying/dividing radicands.",
        reasoning_framework=(
            "1. Ensure radicals have the same index.\n"
            "2. For multiplication: sqrt(a) * sqrt(b) = sqrt(ab).\n"
            "3. For division: sqrt(a) / sqrt(b) = sqrt(a/b), b ≠ 0.\n"
            "4. Simplify the resulting radical.\n"
            "5. Rationalize denominators if required."
        ),
        key_factors=[
            "Same index verification",
            "Accurate multiplication/division",
            "Simplification"
        ],
        primary_authority=[
            "Principles of Algebra, Section 11.3",
            "Common Core State Standards: HSN-RN.A.2"
        ],
        burden_holder="Solver",
        adversary_position="Indices not the same or denominator not rationalized",
        counter_arguments=[
            "Different indices",
            "Arithmetic errors",
            "Denominator not rationalized"
        ],
        resolution_strategy="Ensure same index and rationalize denominators.",
        entity_scope="Radical expressions",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Radical Multiplication/Division"
    ),
    DoctrineBlock(
        topic="Rationalizing Denominators",
        keywords=["radicals", "rationalizing denominators", "algebra"],
        conclusion_template="Multiply numerator and denominator by a suitable radical to eliminate radicals from the denominator.",
        reasoning_framework=(
            "1. Identify the radical in the denominator.\n"
            "2. Multiply numerator and denominator by the radical needed to create a rational denominator.\n"
            "3. For binomials with radicals, use the conjugate.\n"
            "4. Simplify the resulting expression.\n"
            "5. Check by multiplying out denominator to ensure rationality."
        ),
        key_factors=[
            "Correct identification of conjugate",
            "Accurate multiplication",
            "Simplification"
        ],
        primary_authority=[
            "Principles of Algebra, Section 11.4",
            "Common Core State Standards: HSN-RN.A.2"
        ],
        burden_holder="Solver",
        adversary_position="Denominator not fully rationalized",
        counter_arguments=[
            "Incorrect conjugate",
            "Arithmetic errors",
            "Radical remains in denominator"
        ],
        resolution_strategy="Multiply by appropriate radical or conjugate.",
        entity_scope="Rational expressions with radicals",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Rationalizing Denominators"
    ),
    DoctrineBlock(
        topic="Complex Numbers (Addition and Subtraction)",
        keywords=["complex numbers", "addition", "subtraction", "real part", "imaginary part"],
        conclusion_template="Add or subtract complex numbers by combining real and imaginary parts separately.",
        reasoning_framework=(
            "1. Write complex numbers in standard form a + bi.\n"
            "2. Add or subtract real parts.\n"
            "3. Add or subtract imaginary parts.\n"
            "4. Write the result in standard form.\n"
            "5. Check for simplification."
        ),
        key_factors=[
            "Correct identification of real and imaginary parts",
            "Accurate arithmetic",
            "Standard form representation"
        ],
        primary_authority=[
            "Principles of Algebra, Section 12.1",
            "Common Core State Standards: HSN-CN.A.1"
        ],
        burden_holder="Solver",
        adversary_position="Parts not properly combined",
        counter_arguments=[
            "Arithmetic errors",
            "Incorrect standard form",
            "Parts not separated"
        ],
        resolution_strategy="Separate real and imaginary parts before combining.",
        entity_scope="Complex numbers",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Complex Number Addition/Subtraction"
    ),
    DoctrineBlock(
        topic="Complex Numbers (Multiplication)",
        keywords=["complex numbers", "multiplication", "i squared", "algebra"],
        conclusion_template="Multiply complex numbers using distributive property and substitute i^2 = -1.",
        reasoning_framework=(
            "1. Write complex numbers in standard form.\n"
            "2. Apply distributive property (FOIL for binomials).\n"
            "3. Substitute i^2 = -1 where applicable.\n"
            "4. Combine real and imaginary parts.\n"
            "5. Write the result in standard form."
        ),
        key_factors=[
            "Correct application of distributive property",
            "Substitution of i^2 = -1",
            "Standard form representation"
        ],
        primary_authority=[
            "Principles of Algebra, Section 12.2",
            "Common Core State Standards: HSN-CN.A.2"
        ],
        burden_holder="Solver",
        adversary_position="i^2 not properly substituted",
        counter_arguments=[
            "Arithmetic errors",
            "i^2 not replaced",
            "Incorrect standard form"
        ],
        resolution_strategy="Apply FOIL and substitute i^2 = -1.",
        entity_scope="Complex numbers",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Complex Number Multiplication"
    ),
    DoctrineBlock(
        topic="Complex Numbers (Division)",
        keywords=["complex numbers", "division", "conjugate", "algebra"],
        conclusion_template="Multiply numerator and denominator by the conjugate of the denominator to divide complex numbers.",
        reasoning_framework=(
            "1. Write numerator and denominator in standard form.\n"
            "2. Multiply both by the conjugate of the denominator.\n"
            "3. Simplify denominator to a real number.\n"
            "4. Simplify numerator and write in standard form.\n"
            "5. Divide real and imaginary parts by the real denominator."
        ),
        key_factors=[
            "Correct identification of conjugate",
            "Accurate multiplication",
            "Standard form representation"
        ],
        primary_authority=[
            "Principles of Algebra, Section 12.3",
            "Common Core State Standards: HSN-CN.A.3"
        ],
        burden_holder="Solver",
        adversary_position="Conjugate not applied or denominator not real",
        counter_arguments=[
            "Incorrect conjugate",
            "Arithmetic errors",
            "Denominator not real"
        ],
        resolution_strategy="Multiply by conjugate and simplify.",
        entity_scope="Complex numbers",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Complex Number Division"
    ),
    DoctrineBlock(
        topic="Linear Functions (Slope-Intercept Form)",
        keywords=["linear functions", "slope-intercept", "y=mx+b", "algebra"],
        conclusion_template="The slope-intercept form of a line is y = mx + b, where m is the slope and b is the y-intercept.",
        reasoning_framework=(
            "1. Identify the slope (m) and y-intercept (b).\n"
            "2. Substitute values into y = mx + b.\n"
            "3. Use the equation to graph the line or solve for y.\n"
            "4. Check by substituting points to verify they lie on the line."
        ),
        key_factors=[
            "Correct identification of m and b",
            "Accurate substitution",
            "Verification with points"
        ],
        primary_authority=[
            "Principles of Algebra, Section 13.1",
            "Common Core State Standards: HSF-LE.A.2"
        ],
        burden_holder="Solver",
        adversary_position="Incorrect identification of slope or intercept",
        counter_arguments=[
            "Arithmetic errors",
            "Misidentification of slope/intercept",
            "Points do not satisfy equation"
        ],
        resolution_strategy="Careful identification and verification.",
        entity_scope="Linear functions",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Slope-Intercept Form"
    ),
    DoctrineBlock(
        topic="Linear Functions (Point-Slope Form)",
        keywords=["linear functions", "point-slope", "algebra"],
        conclusion_template="The point-slope form is y - y1 = m(x - x1), for a line with slope m through (x1, y1).",
        reasoning_framework=(
            "1. Identify a point (x1, y1) on the line and the slope m.\n"
            "2. Substitute values into y - y1 = m(x - x1).\n"
            "3. Rearrange to slope-intercept or standard form as needed.\n"
            "4. Check by substituting other points."
        ),
        key_factors=[
            "Correct identification of point and slope",
            "Accurate substitution",
            "Verification with points"
        ],
        primary_authority=[
            "Principles of Algebra, Section 13.2",
            "Common Core State Standards: HSF-LE.A.2"
        ],
        burden_holder="Solver",
        adversary_position="Point or slope misidentified",
        counter_arguments=[
            "Arithmetic errors",
            "Incorrect substitution",
            "Points do not satisfy equation"
        ],
        resolution_strategy="Careful substitution and verification.",
        entity_scope="Linear functions",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Point-Slope Form"
    ),
    DoctrineBlock(
        topic="Linear Functions (Standard Form)",
        keywords=["linear functions", "standard form", "Ax+By=C", "algebra"],
        conclusion_template="The standard form of a line is Ax + By = C, with A, B, C integers and A ≥ 0.",
        reasoning_framework=(
            "1. Rearrange the equation to Ax + By = C.\n"
            "2. Ensure A, B, and C are integers and A ≥ 0.\n"
            "3. Eliminate fractions by multiplying both sides as needed.\n"
            "4. Check by substituting points."
        ),
        key_factors=[
            "Correct rearrangement",
            "Integer coefficients",
            "Verification with points"
        ],
        primary_authority=[
            "Principles of Algebra, Section 13.3",
            "Common Core State Standards: HSF-LE.A.2"
        ],
        burden_holder="Solver",
        adversary_position="Coefficients not integers or A < 0",
        counter_arguments=[
            "Arithmetic errors",
            "Incorrect rearrangement",
            "Points do not satisfy equation"
        ],
        resolution_strategy="Rearrange and verify integer coefficients.",
        entity_scope="Linear functions",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Standard Form of Line"
    ),
    DoctrineBlock(
        topic="Slope of a Line",
        keywords=["slope", "linear functions", "rise over run", "algebra"],
        conclusion_template="The slope m between (x1, y1) and (x2, y2) is m = (y2 - y1)/(x2 - x1), x2 ≠ x1.",
        reasoning_framework=(
            "1. Identify two points (x1, y1) and (x2, y2).\n"
            "2. Compute the difference in y-values (rise).\n"
            "3. Compute the difference in x-values (run).\n"
            "4. Divide rise by run to find the slope.\n"
            "5. Check for undefined slope (vertical line, x2 = x1)."
        ),
        key_factors=[
            "Correct identification of points",
            "Accurate subtraction",
            "Division by nonzero run"
        ],
        primary_authority=[
            "Principles of Algebra, Section 13.4",
            "Common Core State Standards: HSF-LE.A.2"
        ],
        burden_holder="Solver",
        adversary_position="Vertical line (undefined slope)",
        counter_arguments=[
            "x2 = x1 (division by zero)",
            "Arithmetic errors",
            "Incorrect point order"
        ],
        resolution_strategy="Check for vertical lines and verify arithmetic.",
        entity_scope="Linear functions",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Slope Formula"
    ),
    DoctrineBlock(
        topic="Parallel and Perpendicular Lines",
        keywords=["parallel lines", "perpendicular lines", "slope", "algebra"],
        conclusion_template="Parallel lines have equal slopes; perpendicular lines have slopes that are negative reciprocals.",
        reasoning_framework=(
            "1. Write equations in slope-intercept form to identify slopes.\n"
            "2. For parallel lines, compare slopes for equality.\n"
            "3. For perpendicular lines, check if m1 * m2 = -1.\n"
            "4. Verify with sample points.\n"
            "5. Check for vertical and horizontal lines as special cases."
        ),
        key_factors=[
            "Correct identification of slopes",
            "Verification of negative reciprocal",
            "Special cases handling"
        ],
        primary_authority=[
            "Principles of Algebra, Section 13.5",
            "Common Core State Standards: HSF-LE.A.2"
        ],
        burden_holder="Solver",
        adversary_position="Slopes not properly compared",
        counter_arguments=[
            "Arithmetic errors",
            "Special cases overlooked",
            "Incorrect reciprocal"
        ],
        resolution_strategy="Careful slope comparison and verification.",
        entity_scope="Linear functions",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Parallel/Perpendicular Slopes"
    ),
    DoctrineBlock(
        topic="Domain and Range",
        keywords=["domain", "range", "functions", "algebra"],
        conclusion_template="The domain is the set of all input values; the range is the set of all output values.",
        reasoning_framework=(
            "1. Analyze the function for restrictions (e.g., denominator ≠ 0, radicand ≥ 0).\n"
            "2. State the set of permissible input values (domain).\n"
            "3. Determine possible output values (range) based on the function's form.\n"
            "4. Express domain and range in interval or set notation.\n"
            "5. Check by substituting values."
        ),
        key_factors=[
            "Identification of restrictions",
            "Accurate notation",
            "Verification by substitution"
        ],
        primary_authority=[
            "Principles of Algebra, Section 14.1",
            "Common Core State Standards: HSF-IF.B.5"
        ],
        burden_holder="Solver",
        adversary_position="Restrictions overlooked or notation incorrect",
        counter_arguments=[
            "Domain/range not properly stated",
            "Notation errors",
            "Arithmetic errors"
        ],
        resolution_strategy="Careful analysis and explicit notation.",
        entity_scope="Functions",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Domain and Range"
    ),
    DoctrineBlock(
        topic="Function Notation",
        keywords=["function notation", "f(x)", "algebra"],
        conclusion_template="f(x) denotes the output of function f for input x.",
        reasoning_framework=(
            "1. Recognize f(x) as the value of function f at input x.\n"
            "2. Substitute the given value for x into the function expression.\n"
            "3. Evaluate to find the output.\n"
            "4. Use function notation consistently in equations and graphs.\n"
            "5. Check by substituting multiple values."
        ),
        key_factors=[
            "Correct substitution",
            "Consistent notation",
            "Verification"
        ],
        primary_authority=[
            "Principles of Algebra, Section 14.2",
            "Common Core State Standards: HSF-IF.A.2"
        ],
        burden_holder="Solver",
        adversary_position="Notation misused or substitution incorrect",
        counter_arguments=[
            "Arithmetic errors",
            "Notation errors",
            "Incorrect substitution"
        ],
        resolution_strategy="Careful substitution and consistent use of notation.",
        entity_scope="Functions",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Function Notation"
    ),
    DoctrineBlock(
        topic="Piecewise Functions",
        keywords=["piecewise functions", "algebra", "domain", "range"],
        conclusion_template="A piecewise function is defined by different expressions over different intervals of the domain.",
        reasoning_framework=(
            "1. Identify the intervals and corresponding expressions.\n"
            "2. For a given input, determine which interval it belongs to.\n"
            "3. Evaluate the corresponding expression.\n"
            "4. State the domain and range explicitly.\n"
            "5. Check for continuity at interval boundaries."
        ),
        key_factors=[
            "Correct interval identification",
            "Accurate evaluation",
            "Domain and range analysis"
        ],
        primary_authority=[
            "Principles of Algebra, Section 14.3",
            "Common Core State Standards: HSF-IF.A.2"
        ],
        burden_holder="Solver",
        adversary_position="Intervals or expressions misapplied",
        counter_arguments=[
            "Incorrect interval assignment",
            "Arithmetic errors",
            "Continuity overlooked"
        ],
        resolution_strategy="Careful interval analysis and evaluation.",
        entity_scope="Piecewise functions",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Piecewise Function Evaluation"
    ),
    DoctrineBlock(
        topic="Inverse Functions",
        keywords=["inverse functions", "algebra", "one-to-one"],
        conclusion_template="The inverse function f^{-1}(x) undoes the action of f(x), such that f(f^{-1}(x)) = x.",
        reasoning_framework=(
            "1. Replace f(x) with y.\n"
            "2. Swap x and y in the equation.\n"
            "3. Solve for y to find f^{-1}(x).\n"
            "4. State the domain and range of the inverse.\n"
            "5. Check by composing f and f^{-1}."
        ),
        key_factors=[
            "Correct swapping of variables",
            "Accurate solving for y",
            "Domain and range analysis"
        ],
        primary_authority=[
            "Principles of Algebra, Section 14.4",
            "Common Core State Standards: HSF-IF.B.4"
        ],
        burden_holder="Solver",
        adversary_position="Function not one-to-one or inverse not found",
        counter_arguments=[
            "Function not invertible",
            "Arithmetic errors",
            "Incorrect composition"
        ],
        resolution_strategy="Verify invertibility and check composition.",
        entity_scope="Invertible functions",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Inverse Function"
    ),
    DoctrineBlock(
        topic="Direct and Inverse Variation",
        keywords=["direct variation", "inverse variation", "algebra", "proportionality"],
        conclusion_template="Direct variation: y = kx; inverse variation: y = k/x, k ≠ 0.",
        reasoning_framework=(
            "1. Identify whether the relationship is direct or inverse.\n"
            "2. For direct, y increases as x increases (y = kx).\n"
            "3. For inverse, y decreases as x increases (y = k/x).\n"
            "4. Solve for the constant k using given values.\n"
            "5. Use the model to predict other values."
        ),
        key_factors=[
            "Correct identification of variation type",
            "Accurate calculation of k",
            "Model application"
        ],
        primary_authority=[
            "Principles of Algebra, Section 15.1",
            "Common Core State Standards: HSF-LE.A.1"
        ],
        burden_holder="Solver",
        adversary_position="Variation type misidentified",
        counter_arguments=[
            "Arithmetic errors",
            "Incorrect model",
            "k = 0 (degenerate case)"
        ],
        resolution_strategy="Careful analysis and model selection.",
        entity_scope="Direct and inverse variation relationships",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Direct/Inverse Variation"
    ),
    DoctrineBlock(
        topic="DRIFT detected for topic",
        keywords=["drift", "doctrine update", "topic", "algebra"],
        conclusion_template="A DRIFT has been detected for topic '{topic}'. Review and update doctrine as needed.",
        reasoning_framework=(
            "1. Monitor for changes in authoritative sources or standards.\n"
            "2. If a DRIFT is detected, compare existing doctrine with new guidance.\n"
            "3. Identify specific areas of change or ambiguity.\n"
            "4. Document the DRIFT and notify relevant stakeholders.\n"
            "5. Update doctrine blocks to reflect current best practices.\n"
            "6. Maintain a record of changes for traceability."
        ),
        key_factors=[
            "Detection of authoritative changes",
            "Comparison with existing doctrine",
            "Timely notification and update"
        ],
        primary_authority=[
            "Engine Policy",
            "Common Core State Standards"
        ],
        burden_holder="Doctrine maintainer",
        adversary_position="Doctrine is outdated or inconsistent",
        counter_arguments=[
            "No actual change in authority",
            "Misinterpretation of new guidance",
            "Delay in update"
        ],
        resolution_strategy="Prompt review and revision of doctrine.",
        entity_scope="All algebra topics",
        confidence=0.90,
        confidence_zone="Medium",
        controlling_precedent="DRIFT Policy"
    ),
    # Add more DoctrineBlock instances as needed to reach 40+
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(query: str) -> List[DoctrineBlock]:
    query_lower = query.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if (query_lower in doctrine.topic.lower() or
            any(query_lower in kw.lower() for kw in doctrine.keywords) or
            query_lower in doctrine.conclusion_template.lower() or
            query_lower in doctrine.reasoning_framework.lower()):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]