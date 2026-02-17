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
        topic="Euclidean Parallel Postulate",
        keywords=["parallel lines", "Euclidean geometry", "postulate", "axiom"],
        conclusion_template="Given a line and a point not on it, exactly one parallel line can be drawn through the point.",
        reasoning_framework=(
            "The Euclidean Parallel Postulate asserts that for any given line and a point not on that line, "
            "there exists exactly one line through the point that does not intersect the original line, "
            "i.e., is parallel to it. This postulate is independent of the other Euclidean axioms and forms "
            "the basis for classical plane geometry. Its acceptance leads to the unique properties of Euclidean "
            "space, such as the sum of angles in a triangle being 180 degrees. Attempts to prove the postulate "
            "from other axioms led to the discovery of non-Euclidean geometries."
        ),
        key_factors=[
            "Uniqueness of parallel line",
            "Independence from other axioms",
            "Implications for triangle angle sum",
            "Foundation for Euclidean geometry"
        ],
        primary_authority=[
            "Euclid's Elements, Book I, Postulate 5",
            "David Hilbert, Foundations of Geometry"
        ],
        burden_holder="Proponent of Euclidean geometry",
        adversary_position="Non-Euclidean geometry allows multiple or no parallels",
        counter_arguments=[
            "Hyperbolic geometry: infinite parallels",
            "Elliptic geometry: no parallels"
        ],
        resolution_strategy="Rely on axiomatic independence and logical consistency within Euclidean framework.",
        entity_scope="Lines and points in Euclidean plane",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book I, Postulate 5"
    ),
    DoctrineBlock(
        topic="Triangle Angle Sum Theorem",
        keywords=["triangle", "angle sum", "Euclidean geometry", "theorem"],
        conclusion_template="The sum of the interior angles of a triangle in Euclidean geometry is 180 degrees.",
        reasoning_framework=(
            "The Triangle Angle Sum Theorem is proven using parallel lines and alternate interior angles. "
            "Given a triangle, a line parallel to one side is drawn through the opposite vertex. The alternate "
            "interior angles formed are congruent to the triangle's angles, and their sum is a straight angle, "
            "i.e., 180 degrees. This property is unique to Euclidean geometry and does not hold in non-Euclidean spaces."
        ),
        key_factors=[
            "Use of parallel lines",
            "Properties of alternate interior angles",
            "Dependence on Euclidean postulates"
        ],
        primary_authority=[
            "Euclid's Elements, Book I, Proposition 32",
            "Hilbert, Foundations of Geometry"
        ],
        burden_holder="Proponent asserting Euclidean triangle properties",
        adversary_position="In non-Euclidean geometries, the sum differs from 180 degrees",
        counter_arguments=[
            "Hyperbolic geometry: sum < 180 degrees",
            "Spherical geometry: sum > 180 degrees"
        ],
        resolution_strategy="Apply only within Euclidean framework; specify geometry type.",
        entity_scope="Triangles in Euclidean plane",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book I, Proposition 32"
    ),
    DoctrineBlock(
        topic="Congruence Criteria for Triangles",
        keywords=["congruence", "triangles", "SSS", "SAS", "ASA", "AAS"],
        conclusion_template="Two triangles are congruent if they satisfy SSS, SAS, ASA, or AAS criteria.",
        reasoning_framework=(
            "Triangle congruence is established by comparing sides and angles. The Side-Side-Side (SSS), "
            "Side-Angle-Side (SAS), Angle-Side-Angle (ASA), and Angle-Angle-Side (AAS) criteria are sufficient "
            "to guarantee congruence. Each criterion is proven using rigid motions or superposition, ensuring "
            "that all corresponding sides and angles are equal. These criteria are foundational for geometric proofs."
        ),
        key_factors=[
            "Equality of sides and angles",
            "Rigid motions (isometries)",
            "Superposition principle"
        ],
        primary_authority=[
            "Euclid's Elements, Book I, Propositions 4, 8, 26",
            "Hilbert, Foundations of Geometry"
        ],
        burden_holder="Party asserting triangle congruence",
        adversary_position="SSA and AAA do not guarantee congruence",
        counter_arguments=[
            "SSA may yield two distinct triangles",
            "AAA only guarantees similarity"
        ],
        resolution_strategy="Restrict to proven congruence criteria; analyze given data.",
        entity_scope="Triangles in Euclidean geometry",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book I, Propositions 4, 8, 26"
    ),
    DoctrineBlock(
        topic="Similarity Criteria for Triangles",
        keywords=["similarity", "triangles", "AA", "SSS", "SAS"],
        conclusion_template="Two triangles are similar if they satisfy AA, SSS, or SAS similarity criteria.",
        reasoning_framework=(
            "Triangle similarity is established when corresponding angles are equal and sides are proportional. "
            "The Angle-Angle (AA), Side-Side-Side (SSS), and Side-Angle-Side (SAS) criteria are sufficient for "
            "proving similarity. The AA criterion is based on the fact that two equal angles guarantee the third, "
            "and proportionality follows. SSS and SAS criteria rely on proportional sides and included angles."
        ),
        key_factors=[
            "Equality of corresponding angles",
            "Proportionality of sides",
            "Transitivity of similarity"
        ],
        primary_authority=[
            "Euclid's Elements, Book VI, Propositions 4, 6",
            "Hilbert, Foundations of Geometry"
        ],
        burden_holder="Party asserting triangle similarity",
        adversary_position="SSA and AAA (without proportionality) do not guarantee similarity",
        counter_arguments=[
            "SSA may not guarantee similarity",
            "AAA without proportionality is insufficient"
        ],
        resolution_strategy="Apply only established similarity criteria; check proportionality.",
        entity_scope="Triangles in Euclidean geometry",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book VI, Propositions 4, 6"
    ),
    DoctrineBlock(
        topic="Pythagorean Theorem",
        keywords=["right triangle", "pythagoras", "theorem", "hypotenuse"],
        conclusion_template="In a right triangle, the square of the hypotenuse equals the sum of the squares of the other two sides.",
        reasoning_framework=(
            "The Pythagorean Theorem is a fundamental result in Euclidean geometry. It states that for any right triangle, "
            "with legs of lengths a and b, and hypotenuse c, the equation a^2 + b^2 = c^2 holds. The theorem is proven "
            "using geometric rearrangement, similarity, or algebraic methods. It is foundational for distance calculations "
            "and analytic geometry."
        ),
        key_factors=[
            "Right angle in triangle",
            "Relationship between sides",
            "Geometric and algebraic proofs"
        ],
        primary_authority=[
            "Euclid's Elements, Book I, Proposition 47",
            "Proofs from Bhaskara, Garfield, and others"
        ],
        burden_holder="Party asserting the relationship in right triangles",
        adversary_position="Does not apply to non-right triangles",
        counter_arguments=[
            "Law of cosines generalizes to all triangles",
            "Requires right angle for equality"
        ],
        resolution_strategy="Verify presence of right angle; apply theorem accordingly.",
        entity_scope="Right triangles in Euclidean geometry",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book I, Proposition 47"
    ),
    DoctrineBlock(
        topic="Circle Theorems: Central and Inscribed Angles",
        keywords=["circle", "central angle", "inscribed angle", "arc"],
        conclusion_template="The measure of a central angle is equal to the arc it subtends; an inscribed angle is half the arc.",
        reasoning_framework=(
            "In a circle, the central angle theorem states that the angle at the center is equal to the measure of the arc it "
            "intercepts. The inscribed angle theorem asserts that an angle formed on the circumference by two chords is half "
            "the measure of the arc it subtends. These theorems are proven using isosceles triangles and properties of arcs."
        ),
        key_factors=[
            "Position of angle vertex (center or circumference)",
            "Relationship between angles and arcs",
            "Use of isosceles triangles"
        ],
        primary_authority=[
            "Euclid's Elements, Book III, Propositions 20, 21",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting angle-arc relationships",
        adversary_position="Theorems do not apply outside circles",
        counter_arguments=[
            "Elliptic or non-circular curves do not satisfy these properties"
        ],
        resolution_strategy="Restrict application to circles; verify definitions.",
        entity_scope="Angles and arcs in circles",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book III, Propositions 20, 21"
    ),
    DoctrineBlock(
        topic="Properties of Parallelograms",
        keywords=["parallelogram", "opposite sides", "opposite angles", "diagonals"],
        conclusion_template="In a parallelogram, opposite sides are equal and parallel, opposite angles are equal, and diagonals bisect each other.",
        reasoning_framework=(
            "A parallelogram is a quadrilateral with both pairs of opposite sides parallel. From this definition, several properties follow: "
            "opposite sides are congruent, opposite angles are equal, and the diagonals bisect each other. These are proven using congruent triangles "
            "and parallel line properties."
        ),
        key_factors=[
            "Definition of parallelogram",
            "Parallel sides",
            "Congruent triangles formed by diagonals"
        ],
        primary_authority=[
            "Euclid's Elements, Book I, Propositions 34, 35",
            "Hilbert, Foundations of Geometry"
        ],
        burden_holder="Party asserting parallelogram properties",
        adversary_position="Non-parallelogram quadrilaterals lack these properties",
        counter_arguments=[
            "Trapezoids and general quadrilaterals do not have all these properties"
        ],
        resolution_strategy="Verify both pairs of sides are parallel before applying properties.",
        entity_scope="Parallelograms in Euclidean plane",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book I, Propositions 34, 35"
    ),
    DoctrineBlock(
        topic="Area of a Triangle",
        keywords=["area", "triangle", "base", "height"],
        conclusion_template="The area of a triangle is one half the product of its base and height.",
        reasoning_framework=(
            "The area formula for a triangle, Area = (1/2) * base * height, is derived by considering a triangle as half of a parallelogram with the same base and height. "
            "This relationship is established by geometric construction and decomposition."
        ),
        key_factors=[
            "Identification of base and corresponding height",
            "Decomposition into parallelogram",
            "Units of measurement"
        ],
        primary_authority=[
            "Euclid's Elements, Book I, Proposition 41",
            "Modern geometry textbooks"
        ],
        burden_holder="Party asserting area calculation",
        adversary_position="Incorrect base or height selection leads to error",
        counter_arguments=[
            "Base and height must be perpendicular",
            "Slant heights are not valid"
        ],
        resolution_strategy="Ensure correct identification of base and perpendicular height.",
        entity_scope="Triangles in Euclidean plane",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book I, Proposition 41"
    ),
    DoctrineBlock(
        topic="Area of a Circle",
        keywords=["area", "circle", "radius", "pi"],
        conclusion_template="The area of a circle is π times the square of its radius.",
        reasoning_framework=(
            "The area formula for a circle, Area = πr^2, is derived using the method of exhaustion, which approximates the circle with inscribed polygons. "
            "As the number of sides increases, the area approaches πr^2. This is foundational for calculus and analysis."
        ),
        key_factors=[
            "Radius measurement",
            "Value of π (pi)",
            "Limit process with polygons"
        ],
        primary_authority=[
            "Archimedes, Measurement of a Circle",
            "Euclid's Elements, Book XII"
        ],
        burden_holder="Party asserting area calculation",
        adversary_position="Formula does not apply to non-circular regions",
        counter_arguments=[
            "Ellipses and other curves require different formulas"
        ],
        resolution_strategy="Verify region is a true circle; apply correct formula.",
        entity_scope="Circles in Euclidean plane",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Archimedes, Measurement of a Circle"
    ),
    DoctrineBlock(
        topic="Law of Sines",
        keywords=["law of sines", "triangle", "sine", "angle", "side"],
        conclusion_template="In any triangle, the ratio of the length of a side to the sine of its opposite angle is constant.",
        reasoning_framework=(
            "The Law of Sines states that for any triangle with sides a, b, c and opposite angles A, B, C, "
            "a/sin(A) = b/sin(B) = c/sin(C). This is proven using the area formula for triangles and properties of the sine function. "
            "It is useful for solving triangles when two angles and a side or two sides and a non-included angle are known."
        ),
        key_factors=[
            "Knowledge of sides and angles",
            "Use of sine function",
            "Area formula for triangles"
        ],
        primary_authority=[
            "Euclid's Elements, Book IV",
            "Modern trigonometry texts"
        ],
        burden_holder="Party applying the law to solve triangles",
        adversary_position="Ambiguous case (SSA) may yield two solutions",
        counter_arguments=[
            "Check for ambiguous case",
            "Law does not apply to degenerate triangles"
        ],
        resolution_strategy="Analyze given data for ambiguity; apply law accordingly.",
        entity_scope="All triangles in Euclidean plane",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Modern trigonometry"
    ),
    DoctrineBlock(
        topic="Law of Cosines",
        keywords=["law of cosines", "triangle", "cosine", "side", "angle"],
        conclusion_template="In any triangle, c^2 = a^2 + b^2 - 2ab cos(C), relating sides and included angle.",
        reasoning_framework=(
            "The Law of Cosines generalizes the Pythagorean Theorem to all triangles. It relates the lengths of sides a, b, c and the cosine of the included angle C: "
            "c^2 = a^2 + b^2 - 2ab cos(C). This law is proven using coordinate geometry or geometric construction, and is essential for solving triangles with two sides and the included angle."
        ),
        key_factors=[
            "Knowledge of two sides and included angle",
            "Use of cosine function",
            "Generalization of Pythagorean Theorem"
        ],
        primary_authority=[
            "Euclid's Elements, Book II, Proposition 12",
            "Modern trigonometry texts"
        ],
        burden_holder="Party applying the law to solve triangles",
        adversary_position="Law reduces to Pythagorean Theorem for right triangles",
        counter_arguments=[
            "For right triangles, cos(90°) = 0, recovering Pythagoras",
            "Law does not apply to non-triangular figures"
        ],
        resolution_strategy="Verify triangle and angle; apply law as appropriate.",
        entity_scope="All triangles in Euclidean plane",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Modern trigonometry"
    ),
    DoctrineBlock(
        topic="Properties of Regular Polygons",
        keywords=["regular polygon", "sides", "angles", "symmetry"],
        conclusion_template="A regular polygon has all sides and angles equal, and is cyclic and equiangular.",
        reasoning_framework=(
            "A regular polygon is defined as a convex polygon with all sides and all angles congruent. "
            "Such polygons are cyclic (can be inscribed in a circle), and have rotational and reflectional symmetry. "
            "The measure of each interior angle is ((n-2)*180)/n degrees, where n is the number of sides."
        ),
        key_factors=[
            "Equality of sides and angles",
            "Cyclic nature",
            "Symmetry properties"
        ],
        primary_authority=[
            "Euclid's Elements, Book IV",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting regularity",
        adversary_position="Irregular polygons lack these properties",
        counter_arguments=[
            "Non-convex or irregular polygons do not have equal sides/angles"
        ],
        resolution_strategy="Verify all sides and angles are congruent.",
        entity_scope="Convex polygons in Euclidean plane",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book IV"
    ),
    DoctrineBlock(
        topic="Inscribed Angle Theorem",
        keywords=["circle", "inscribed angle", "arc", "theorem"],
        conclusion_template="An inscribed angle in a circle is half the measure of its intercepted arc.",
        reasoning_framework=(
            "The Inscribed Angle Theorem states that an angle formed by two chords in a circle with the vertex on the circle "
            "is equal to half the measure of the intercepted arc. The proof uses properties of central angles and isosceles triangles."
        ),
        key_factors=[
            "Location of angle vertex on circle",
            "Relationship to central angle",
            "Arc measurement"
        ],
        primary_authority=[
            "Euclid's Elements, Book III, Proposition 21",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting angle-arc relationship",
        adversary_position="Theorem does not apply to ellipses or other curves",
        counter_arguments=[
            "Inscribed angle properties are unique to circles"
        ],
        resolution_strategy="Restrict application to circles; verify definitions.",
        entity_scope="Angles in circles",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book III, Proposition 21"
    ),
    DoctrineBlock(
        topic="Tangent to a Circle",
        keywords=["circle", "tangent", "perpendicular", "radius"],
        conclusion_template="A tangent to a circle is perpendicular to the radius at the point of contact.",
        reasoning_framework=(
            "A tangent is a line that touches a circle at exactly one point. The radius drawn to the point of tangency is perpendicular to the tangent. "
            "This is proven by contradiction: if not perpendicular, a second intersection would occur, violating the definition of a tangent."
        ),
        key_factors=[
            "Definition of tangent",
            "Uniqueness of intersection point",
            "Perpendicularity to radius"
        ],
        primary_authority=[
            "Euclid's Elements, Book III, Proposition 16",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting tangent property",
        adversary_position="Secant lines intersect at two points",
        counter_arguments=[
            "Secants and chords do not satisfy this property"
        ],
        resolution_strategy="Verify line meets circle at one point; check perpendicularity.",
        entity_scope="Lines and circles in Euclidean plane",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book III, Proposition 16"
    ),
    DoctrineBlock(
        topic="Power of a Point Theorem",
        keywords=["power of a point", "circle", "chord", "secant", "tangent"],
        conclusion_template="For a point and a circle, the products of segment lengths from the point to the circle are equal for intersecting chords, secants, or tangents.",
        reasoning_framework=(
            "The Power of a Point Theorem relates the lengths of line segments from a point to a circle. For chords AB and CD intersecting at P inside the circle, "
            "PA*PB = PC*PD. For a point outside the circle, the product of the lengths of a secant and its external segment equals the square of the tangent from the point."
        ),
        key_factors=[
            "Relative position of point to circle",
            "Intersection types (chord, secant, tangent)",
            "Product of segment lengths"
        ],
        primary_authority=[
            "Euclid's Elements, Book III, Propositions 35, 36",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting segment product equality",
        adversary_position="Theorem does not apply to non-circular curves",
        counter_arguments=[
            "Ellipses and parabolas do not satisfy this property"
        ],
        resolution_strategy="Verify circle and intersection types; apply theorem.",
        entity_scope="Points and circles in Euclidean plane",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book III, Propositions 35, 36"
    ),
    DoctrineBlock(
        topic="Properties of Medians in a Triangle",
        keywords=["triangle", "median", "centroid", "concurrency"],
        conclusion_template="The medians of a triangle are concurrent at the centroid, which divides each median in a 2:1 ratio.",
        reasoning_framework=(
            "A median of a triangle connects a vertex to the midpoint of the opposite side. The three medians are always concurrent at the centroid, "
            "which is the triangle's center of mass. The centroid divides each median into segments with a 2:1 ratio, with the longer segment adjacent to the vertex."
        ),
        key_factors=[
            "Construction of medians",
            "Concurrency at centroid",
            "2:1 ratio division"
        ],
        primary_authority=[
            "Euclid's Elements, Book I, Proposition 37",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting median properties",
        adversary_position="Other lines (altitudes, angle bisectors) have different concurrency points",
        counter_arguments=[
            "Orthocenter, incenter, circumcenter are distinct",
            "Not all lines are medians"
        ],
        resolution_strategy="Verify lines are medians; apply centroid properties.",
        entity_scope="Triangles in Euclidean plane",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book I, Proposition 37"
    ),
    DoctrineBlock(
        topic="Properties of Altitudes in a Triangle",
        keywords=["triangle", "altitude", "orthocenter", "concurrency"],
        conclusion_template="The altitudes of a triangle are concurrent at the orthocenter.",
        reasoning_framework=(
            "An altitude is a perpendicular segment from a vertex to the opposite side (or its extension). The three altitudes of a triangle are always concurrent at the orthocenter. "
            "The orthocenter's position relative to the triangle depends on the triangle's type (acute, right, obtuse)."
        ),
        key_factors=[
            "Construction of altitudes",
            "Concurrency at orthocenter",
            "Triangle type affects orthocenter location"
        ],
        primary_authority=[
            "Modern geometry texts",
            "Hilbert, Foundations of Geometry"
        ],
        burden_holder="Party asserting altitude properties",
        adversary_position="Other lines (medians, angle bisectors) have different concurrency points",
        counter_arguments=[
            "Centroid, incenter, circumcenter are distinct",
            "Not all lines are altitudes"
        ],
        resolution_strategy="Verify lines are altitudes; apply orthocenter properties.",
        entity_scope="Triangles in Euclidean plane",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Modern geometry"
    ),
    DoctrineBlock(
        topic="Properties of Angle Bisectors in a Triangle",
        keywords=["triangle", "angle bisector", "incenter", "concurrency"],
        conclusion_template="The angle bisectors of a triangle are concurrent at the incenter, which is equidistant from all sides.",
        reasoning_framework=(
            "An angle bisector divides a triangle's angle into two equal parts. The three angle bisectors are always concurrent at the incenter, "
            "which is the center of the inscribed circle (incircle). The incenter is equidistant from all sides of the triangle."
        ),
        key_factors=[
            "Construction of angle bisectors",
            "Concurrency at incenter",
            "Equidistance from sides"
        ],
        primary_authority=[
            "Euclid's Elements, Book IV, Proposition 4",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting angle bisector properties",
        adversary_position="Other lines (medians, altitudes) have different concurrency points",
        counter_arguments=[
            "Centroid, orthocenter, circumcenter are distinct",
            "Not all lines are angle bisectors"
        ],
        resolution_strategy="Verify lines are angle bisectors; apply incenter properties.",
        entity_scope="Triangles in Euclidean plane",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book IV, Proposition 4"
    ),
    DoctrineBlock(
        topic="Properties of Perpendicular Bisectors in a Triangle",
        keywords=["triangle", "perpendicular bisector", "circumcenter", "concurrency"],
        conclusion_template="The perpendicular bisectors of a triangle's sides are concurrent at the circumcenter, equidistant from the vertices.",
        reasoning_framework=(
            "A perpendicular bisector divides a side into two equal parts at a right angle. The three perpendicular bisectors of a triangle are concurrent at the circumcenter, "
            "which is the center of the circumscribed circle (circumcircle). The circumcenter is equidistant from all vertices."
        ),
        key_factors=[
            "Construction of perpendicular bisectors",
            "Concurrency at circumcenter",
            "Equidistance from vertices"
        ],
        primary_authority=[
            "Euclid's Elements, Book IV, Proposition 5",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting perpendicular bisector properties",
        adversary_position="Other lines (medians, altitudes) have different concurrency points",
        counter_arguments=[
            "Centroid, orthocenter, incenter are distinct",
            "Not all lines are perpendicular bisectors"
        ],
        resolution_strategy="Verify lines are perpendicular bisectors; apply circumcenter properties.",
        entity_scope="Triangles in Euclidean plane",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book IV, Proposition 5"
    ),
    DoctrineBlock(
        topic="Properties of Cyclic Quadrilaterals",
        keywords=["cyclic quadrilateral", "circle", "opposite angles", "supplementary"],
        conclusion_template="A quadrilateral is cyclic if and only if its opposite angles are supplementary.",
        reasoning_framework=(
            "A cyclic quadrilateral is one whose vertices all lie on a circle. The defining property is that the sum of each pair of opposite angles is 180 degrees. "
            "This is proven using the inscribed angle theorem and properties of circles."
        ),
        key_factors=[
            "Vertices on a circle",
            "Opposite angles",
            "Supplementary relationship"
        ],
        primary_authority=[
            "Euclid's Elements, Book III, Proposition 22",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting cyclicity",
        adversary_position="Non-cyclic quadrilaterals lack this property",
        counter_arguments=[
            "General quadrilaterals do not have supplementary opposite angles"
        ],
        resolution_strategy="Verify all vertices on a circle; check angle sums.",
        entity_scope="Quadrilaterals in Euclidean plane",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book III, Proposition 22"
    ),
    DoctrineBlock(
        topic="Midline Theorem (Triangle Midsegment)",
        keywords=["triangle", "midline", "midsegment", "parallel", "half length"],
        conclusion_template="The segment joining the midpoints of two sides of a triangle is parallel to the third side and half its length.",
        reasoning_framework=(
            "The midline (or midsegment) theorem states that in a triangle, the segment connecting the midpoints of two sides is parallel to the third side and has half its length. "
            "This is proven using properties of similar triangles and congruence."
        ),
        key_factors=[
            "Identification of midpoints",
            "Parallelism to third side",
            "Half-length property"
        ],
        primary_authority=[
            "Euclid's Elements, Book VI, Proposition 2",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting midline properties",
        adversary_position="Other segments do not have these properties",
        counter_arguments=[
            "Segments not joining midpoints do not guarantee parallelism or half-length"
        ],
        resolution_strategy="Verify segment joins midpoints; apply theorem.",
        entity_scope="Triangles in Euclidean plane",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book VI, Proposition 2"
    ),
    DoctrineBlock(
        topic="Exterior Angle Theorem",
        keywords=["triangle", "exterior angle", "theorem", "greater than interior"],
        conclusion_template="An exterior angle of a triangle is equal to the sum of the two non-adjacent interior angles and greater than either.",
        reasoning_framework=(
            "The Exterior Angle Theorem states that the measure of an exterior angle of a triangle is equal to the sum of the two remote interior angles. "
            "Additionally, the exterior angle is greater than either remote interior angle. This is proven using properties of supplementary angles and triangle angle sums."
        ),
        key_factors=[
            "Construction of exterior angle",
            "Triangle angle sum",
            "Supplementary angles"
        ],
        primary_authority=[
            "Euclid's Elements, Book I, Proposition 32",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting exterior angle properties",
        adversary_position="Theorem does not apply to non-triangular figures",
        counter_arguments=[
            "Quadrilaterals and other polygons have different properties"
        ],
        resolution_strategy="Verify triangle structure; apply theorem.",
        entity_scope="Triangles in Euclidean plane",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book I, Proposition 32"
    ),
    DoctrineBlock(
        topic="Angle Bisector Theorem",
        keywords=["triangle", "angle bisector", "proportional", "side"],
        conclusion_template="An angle bisector in a triangle divides the opposite side into segments proportional to the adjacent sides.",
        reasoning_framework=(
            "The Angle Bisector Theorem states that an angle bisector in a triangle divides the opposite side into two segments that are proportional to the adjacent sides. "
            "If the angle bisector from vertex A meets side BC at D, then BD/DC = AB/AC. The proof uses properties of similar triangles."
        ),
        key_factors=[
            "Construction of angle bisector",
            "Proportionality of side segments",
            "Similarity of triangles"
        ],
        primary_authority=[
            "Euclid's Elements, Book VI, Proposition 3",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting proportionality",
        adversary_position="Other lines do not guarantee this proportionality",
        counter_arguments=[
            "Medians and altitudes do not generally divide sides proportionally"
        ],
        resolution_strategy="Verify line is angle bisector; apply theorem.",
        entity_scope="Triangles in Euclidean plane",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book VI, Proposition 3"
    ),
    DoctrineBlock(
        topic="Properties of Trapezoids",
        keywords=["trapezoid", "parallel sides", "median", "area"],
        conclusion_template="A trapezoid has one pair of parallel sides; the median is parallel to the bases and its length is the average of the bases.",
        reasoning_framework=(
            "A trapezoid is a quadrilateral with exactly one pair of parallel sides (the bases). The segment joining the midpoints of the non-parallel sides (the median) "
            "is parallel to the bases and its length is the arithmetic mean of the bases. The area is given by (1/2) * (sum of bases) * height."
        ),
        key_factors=[
            "Identification of parallel sides",
            "Median construction",
            "Area formula"
        ],
        primary_authority=[
            "Euclid's Elements, Book I",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting trapezoid properties",
        adversary_position="Parallelograms have both pairs of sides parallel",
        counter_arguments=[
            "Parallelograms are not trapezoids under strict definitions"
        ],
        resolution_strategy="Verify only one pair of sides is parallel.",
        entity_scope="Quadrilaterals in Euclidean plane",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Modern geometry"
    ),
    DoctrineBlock(
        topic="Heron's Formula",
        keywords=["triangle", "area", "heron's formula", "sides"],
        conclusion_template="The area of a triangle with sides a, b, c is √[s(s-a)(s-b)(s-c)], where s = (a+b+c)/2.",
        reasoning_framework=(
            "Heron's Formula allows calculation of a triangle's area when all three sides are known. The semi-perimeter s = (a+b+c)/2 is computed, "
            "and the area is the square root of s(s-a)(s-b)(s-c). The proof uses algebraic manipulation and the Law of Cosines."
        ),
        key_factors=[
            "Knowledge of all three sides",
            "Calculation of semi-perimeter",
            "Algebraic manipulation"
        ],
        primary_authority=[
            "Heron of Alexandria, Metrica",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting area calculation",
        adversary_position="Formula does not apply to degenerate triangles",
        counter_arguments=[
            "Sides must satisfy triangle inequality"
        ],
        resolution_strategy="Verify triangle inequality; apply formula.",
        entity_scope="Triangles in Euclidean plane",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Heron of Alexandria, Metrica"
    ),
    DoctrineBlock(
        topic="Properties of Rhombuses",
        keywords=["rhombus", "parallelogram", "equal sides", "diagonals"],
        conclusion_template="A rhombus is a parallelogram with all sides equal; diagonals bisect at right angles.",
        reasoning_framework=(
            "A rhombus is a special parallelogram with all sides congruent. Its diagonals are perpendicular bisectors of each other and bisect the angles. "
            "These properties are proven using congruent triangles and symmetry."
        ),
        key_factors=[
            "Equality of sides",
            "Diagonals perpendicular and bisecting",
            "Angle bisectors"
        ],
        primary_authority=[
            "Euclid's Elements, Book I, Proposition 34",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting rhombus properties",
        adversary_position="General parallelograms lack perpendicular diagonals",
        counter_arguments=[
            "Rectangle and general parallelogram have different diagonal properties"
        ],
        resolution_strategy="Verify all sides equal; check diagonal properties.",
        entity_scope="Quadrilaterals in Euclidean plane",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book I, Proposition 34"
    ),
    DoctrineBlock(
        topic="Properties of Rectangles",
        keywords=["rectangle", "parallelogram", "right angle", "diagonals"],
        conclusion_template="A rectangle is a parallelogram with all angles right; diagonals are equal and bisect each other.",
        reasoning_framework=(
            "A rectangle is a parallelogram with four right angles. Its diagonals are congruent and bisect each other. "
            "These properties are proven using congruent triangles and properties of parallelograms."
        ),
        key_factors=[
            "Right angles",
            "Congruent diagonals",
            "Bisecting diagonals"
        ],
        primary_authority=[
            "Euclid's Elements, Book I, Proposition 34",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting rectangle properties",
        adversary_position="General parallelograms lack right angles",
        counter_arguments=[
            "Rhombus and general parallelogram have different angle properties"
        ],
        resolution_strategy="Verify all angles are right; check diagonal properties.",
        entity_scope="Quadrilaterals in Euclidean plane",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book I, Proposition 34"
    ),
    DoctrineBlock(
        topic="Properties of Squares",
        keywords=["square", "parallelogram", "equal sides", "right angles", "diagonals"],
        conclusion_template="A square is a parallelogram with all sides equal and all angles right; diagonals are equal, bisect at right angles, and bisect angles.",
        reasoning_framework=(
            "A square is a regular quadrilateral: all sides are congruent and all angles are right. Its diagonals are congruent, bisect each other at right angles, and bisect the angles. "
            "These properties are proven using congruent triangles and symmetry."
        ),
        key_factors=[
            "Equality of sides",
            "Right angles",
            "Diagonal properties"
        ],
        primary_authority=[
            "Euclid's Elements, Book I, Proposition 46",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting square properties",
        adversary_position="Rectangles and rhombuses lack all properties simultaneously",
        counter_arguments=[
            "Rectangles lack equal sides; rhombuses lack right angles"
        ],
        resolution_strategy="Verify all sides and angles; check diagonal properties.",
        entity_scope="Quadrilaterals in Euclidean plane",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book I, Proposition 46"
    ),
    DoctrineBlock(
        topic="Properties of Kites",
        keywords=["kite", "quadrilateral", "equal adjacent sides", "diagonals"],
        conclusion_template="A kite has two pairs of adjacent sides equal; one diagonal is the axis of symmetry and bisects the other at right angles.",
        reasoning_framework=(
            "A kite is a quadrilateral with two distinct pairs of adjacent sides equal. One diagonal is the axis of symmetry, bisecting the other at a right angle. "
            "These properties are proven using congruent triangles and symmetry."
        ),
        key_factors=[
            "Equality of adjacent sides",
            "Diagonal properties",
            "Axis of symmetry"
        ],
        primary_authority=[
            "Modern geometry texts"
        ],
        burden_holder="Party asserting kite properties",
        adversary_position="General quadrilaterals lack these properties",
        counter_arguments=[
            "Parallelograms and trapezoids have different side and diagonal properties"
        ],
        resolution_strategy="Verify side lengths and diagonal properties.",
        entity_scope="Quadrilaterals in Euclidean plane",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Modern geometry"
    ),
    DoctrineBlock(
        topic="Properties of Chords in a Circle",
        keywords=["circle", "chord", "equidistant", "center"],
        conclusion_template="Chords equidistant from the center of a circle are equal in length.",
        reasoning_framework=(
            "In a circle, chords that are equidistant from the center are congruent. Conversely, congruent chords are equidistant from the center. "
            "This is proven using perpendicular bisectors and properties of isosceles triangles."
        ),
        key_factors=[
            "Distance from center",
            "Chord length",
            "Perpendicular bisector"
        ],
        primary_authority=[
            "Euclid's Elements, Book III, Proposition 9",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting chord properties",
        adversary_position="Non-equidistant chords may differ in length",
        counter_arguments=[
            "Distance from center determines chord length"
        ],
        resolution_strategy="Measure distance from center; compare chord lengths.",
        entity_scope="Chords in circles",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book III, Proposition 9"
    ),
    DoctrineBlock(
        topic="Arc Length of a Circle",
        keywords=["circle", "arc length", "radius", "central angle"],
        conclusion_template="The length of an arc is (θ/360) × 2πr, where θ is the central angle in degrees.",
        reasoning_framework=(
            "The arc length formula is derived from the proportion of the circle's circumference corresponding to the central angle. "
            "For angle θ (in degrees), arc length = (θ/360) × 2πr. For radians, arc length = rθ. This is foundational for circular motion and trigonometry."
        ),
        key_factors=[
            "Central angle measurement",
            "Radius",
            "Proportionality to circumference"
        ],
        primary_authority=[
            "Euclid's Elements, Book III",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting arc length calculation",
        adversary_position="Formula does not apply to non-circular arcs",
        counter_arguments=[
            "Elliptical arcs require different formulas"
        ],
        resolution_strategy="Verify arc is part of a circle; apply correct formula.",
        entity_scope="Arcs in circles",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Modern geometry"
    ),
    DoctrineBlock(
        topic="Sector Area of a Circle",
        keywords=["circle", "sector", "area", "central angle"],
        conclusion_template="The area of a sector is (θ/360) × πr^2, where θ is the central angle in degrees.",
        reasoning_framework=(
            "The area of a sector is proportional to the area of the whole circle, based on the central angle. "
            "For angle θ (in degrees), sector area = (θ/360) × πr^2. For radians, sector area = (1/2)r^2θ."
        ),
        key_factors=[
            "Central angle measurement",
            "Radius",
            "Proportionality to total area"
        ],
        primary_authority=[
            "Euclid's Elements, Book III",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting sector area calculation",
        adversary_position="Formula does not apply to non-circular sectors",
        counter_arguments=[
            "Elliptical sectors require different formulas"
        ],
        resolution_strategy="Verify sector is part of a circle; apply correct formula.",
        entity_scope="Sectors in circles",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Modern geometry"
    ),
    DoctrineBlock(
        topic="Coordinate Geometry: Distance Formula",
        keywords=["coordinate geometry", "distance", "formula", "cartesian plane"],
        conclusion_template="The distance between points (x1, y1) and (x2, y2) is √[(x2-x1)^2 + (y2-y1)^2].",
        reasoning_framework=(
            "The distance formula is derived from the Pythagorean Theorem. In the Cartesian plane, the horizontal and vertical differences form the legs of a right triangle, "
            "and the distance is the hypotenuse. This formula is foundational for analytic geometry."
        ),
        key_factors=[
            "Coordinates of points",
            "Application of Pythagorean Theorem",
            "Cartesian plane"
        ],
        primary_authority=[
            "René Descartes, La Géométrie",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting distance calculation",
        adversary_position="Formula does not apply in non-Euclidean spaces",
        counter_arguments=[
            "Curved spaces require different metrics"
        ],
        resolution_strategy="Verify Euclidean plane; apply formula.",
        entity_scope="Points in Cartesian plane",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="René Descartes, La Géométrie"
    ),
    DoctrineBlock(
        topic="Coordinate Geometry: Slope Formula",
        keywords=["coordinate geometry", "slope", "formula", "cartesian plane"],
        conclusion_template="The slope of the line through points (x1, y1) and (x2, y2) is (y2-y1)/(x2-x1), x1 ≠ x2.",
        reasoning_framework=(
            "The slope formula measures the steepness of a line in the Cartesian plane. It is the ratio of the vertical change to the horizontal change between two points. "
            "This formula is essential for equations of lines and analytic geometry."
        ),
        key_factors=[
            "Coordinates of points",
            "Vertical and horizontal differences",
            "Non-vertical lines"
        ],
        primary_authority=[
            "René Descartes, La Géométrie",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting slope calculation",
        adversary_position="Vertical lines have undefined slope",
        counter_arguments=[
            "Division by zero for vertical lines"
        ],
        resolution_strategy="Check x1 ≠ x2; handle vertical lines separately.",
        entity_scope="Lines in Cartesian plane",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="René Descartes, La Géométrie"
    ),
    DoctrineBlock(
        topic="Equation of a Circle (Cartesian Plane)",
        keywords=["coordinate geometry", "circle", "equation", "cartesian plane"],
        conclusion_template="The equation of a circle with center (h, k) and radius r is (x-h)^2 + (y-k)^2 = r^2.",
        reasoning_framework=(
            "The equation is derived from the definition of a circle as the locus of points equidistant from a center. "
            "The distance formula is applied to all points (x, y) at distance r from (h, k), yielding (x-h)^2 + (y-k)^2 = r^2."
        ),
        key_factors=[
            "Center coordinates",
            "Radius",
            "Distance formula"
        ],
        primary_authority=[
            "René Descartes, La Géométrie",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting equation",
        adversary_position="Equation does not describe non-circular loci",
        counter_arguments=[
            "Ellipses, parabolas, hyperbolas have different equations"
        ],
        resolution_strategy="Verify locus is a circle; apply equation.",
        entity_scope="Circles in Cartesian plane",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="René Descartes, La Géométrie"
    ),
    DoctrineBlock(
        topic="Equation of a Line (Slope-Intercept Form)",
        keywords=["coordinate geometry", "line", "equation", "slope-intercept"],
        conclusion_template="The equation of a line with slope m and y-intercept b is y = mx + b.",
        reasoning_framework=(
            "The slope-intercept form expresses a line in terms of its slope and y-intercept. It is derived from the definition of slope and the point-slope form. "
            "This form is widely used for graphing and analyzing linear relationships."
        ),
        key_factors=[
            "Slope",
            "Y-intercept",
            "Linear relationship"
        ],
        primary_authority=[
            "René Descartes, La Géométrie",
            "Modern algebra texts"
        ],
        burden_holder="Party asserting equation",
        adversary_position="Vertical lines cannot be written in this form",
        counter_arguments=[
            "Vertical lines require x = constant form"
        ],
        resolution_strategy="Check for vertical lines; use appropriate form.",
        entity_scope="Lines in Cartesian plane",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="René Descartes, La Géométrie"
    ),
    DoctrineBlock(
        topic="Equation of a Line (Point-Slope Form)",
        keywords=["coordinate geometry", "line", "equation", "point-slope"],
        conclusion_template="The equation of a line through (x1, y1) with slope m is y - y1 = m(x - x1).",
        reasoning_framework=(
            "The point-slope form is derived from the definition of slope. It is useful for writing the equation of a line given a point and the slope, "
            "and can be rearranged into other forms as needed."
        ),
        key_factors=[
            "Known point",
            "Slope",
            "Linear relationship"
        ],
        primary_authority=[
            "René Descartes, La Géométrie",
            "Modern algebra texts"
        ],
        burden_holder="Party asserting equation",
        adversary_position="Vertical lines require different form",
        counter_arguments=[
            "Slope undefined for vertical lines"
        ],
        resolution_strategy="Check for vertical lines; use x = constant if needed.",
        entity_scope="Lines in Cartesian plane",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="René Descartes, La Géométrie"
    ),
    DoctrineBlock(
        topic="Equation of a Parabola (Standard Form)",
        keywords=["coordinate geometry", "parabola", "equation", "standard form"],
        conclusion_template="The equation of a parabola with vertex at (h, k) and axis parallel to y-axis is y = a(x-h)^2 + k.",
        reasoning_framework=(
            "The standard form is derived from the geometric definition of a parabola as the locus of points equidistant from a focus and directrix. "
            "Completing the square transforms the general quadratic equation into standard form."
        ),
        key_factors=[
            "Vertex coordinates",
            "Parameter a (determines opening and width)",
            "Axis orientation"
        ],
        primary_authority=[
            "René Descartes, La Géométrie",
            "Modern algebra texts"
        ],
        burden_holder="Party asserting equation",
        adversary_position="Equation does not describe non-parabolic loci",
        counter_arguments=[
            "Circles, ellipses, hyperbolas have different equations"
        ],
        resolution_strategy="Verify locus is a parabola; apply equation.",
        entity_scope="Parabolas in Cartesian plane",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="René Descartes, La Géométrie"
    ),
    DoctrineBlock(
        topic="Equation of an Ellipse (Standard Form)",
        keywords=["coordinate geometry", "ellipse", "equation", "standard form"],
        conclusion_template="The equation of an ellipse with center (h, k), axes a, b is ((x-h)^2)/a^2 + ((y-k)^2)/b^2 = 1.",
        reasoning_framework=(
            "The standard form is derived from the geometric definition of an ellipse as the locus of points whose sum of distances to two foci is constant. "
            "The axes a and b determine the shape and orientation. Completing the square transforms the general quadratic equation into standard form."
        ),
        key_factors=[
            "Center coordinates",
            "Axes lengths",
            "Orientation"
        ],
        primary_authority=[
            "René Descartes, La Géométrie",
            "Modern algebra texts"
        ],
        burden_holder="Party asserting equation",
        adversary_position="Equation does not describe non-elliptical loci",
        counter_arguments=[
            "Circles, parabolas, hyperbolas have different equations"
        ],
        resolution_strategy="Verify locus is an ellipse; apply equation.",
        entity_scope="Ellipses in Cartesian plane",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="René Descartes, La Géométrie"
    ),
    DoctrineBlock(
        topic="Equation of a Hyperbola (Standard Form)",
        keywords=["coordinate geometry", "hyperbola", "equation", "standard form"],
        conclusion_template="The equation of a hyperbola with center (h, k), axes a, b is ((x-h)^2)/a^2 - ((y-k)^2)/b^2 = 1.",
        reasoning_framework=(
            "The standard form is derived from the geometric definition of a hyperbola as the locus of points whose absolute difference of distances to two foci is constant. "
            "The axes a and b determine the shape and orientation. Completing the square transforms the general quadratic equation into standard form."
        ),
        key_factors=[
            "Center coordinates",
            "Axes lengths",
            "Orientation"
        ],
        primary_authority=[
            "René Descartes, La Géométrie",
            "Modern algebra texts"
        ],
        burden_holder="Party asserting equation",
        adversary_position="Equation does not describe non-hyperbolic loci",
        counter_arguments=[
            "Circles, ellipses, parabolas have different equations"
        ],
        resolution_strategy="Verify locus is a hyperbola; apply equation.",
        entity_scope="Hyperbolas in Cartesian plane",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="René Descartes, La Géométrie"
    ),
    DoctrineBlock(
        topic="Converse of the Pythagorean Theorem",
        keywords=["right triangle", "pythagoras", "converse", "theorem"],
        conclusion_template="If a^2 + b^2 = c^2 for triangle sides, the triangle is right-angled with hypotenuse c.",
        reasoning_framework=(
            "The converse states that if the squares of two sides of a triangle sum to the square of the third, the triangle is right-angled. "
            "This is proven by constructing a triangle with the given sides and showing the angle opposite the largest side is a right angle."
        ),
        key_factors=[
            "Side lengths",
            "Triangle construction",
            "Uniqueness of right angle"
        ],
        primary_authority=[
            "Euclid's Elements, Book I, Proposition 48",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting right angle",
        adversary_position="Triangle may not exist if sides violate triangle inequality",
        counter_arguments=[
            "Sides must satisfy triangle inequality"
        ],
        resolution_strategy="Verify triangle can be constructed; apply converse.",
        entity_scope="Triangles in Euclidean plane",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book I, Proposition 48"
    ),
    DoctrineBlock(
        topic="Similarity of Circles",
        keywords=["circle", "similarity", "scaling", "proportional"],
        conclusion_template="All circles are similar; their radii and corresponding chords, arcs, and areas are proportional.",
        reasoning_framework=(
            "Circles are similar because they can be mapped onto each other by scaling (dilation). All corresponding linear measurements are proportional to the radii, "
            "and areas are proportional to the squares of the radii. This property is foundational for similarity in geometry."
        ),
        key_factors=[
            "Scaling transformations",
            "Proportionality of measurements",
            "Dilation"
        ],
        primary_authority=[
            "Euclid's Elements, Book III",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting similarity",
        adversary_position="Non-circular curves are not similar to circles",
        counter_arguments=[
            "Ellipses and other curves lack this property"
        ],
        resolution_strategy="Restrict to circles; apply scaling.",
        entity_scope="Circles in Euclidean plane",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book III"
    ),
    DoctrineBlock(
        topic="Properties of Regular Polyhedra (Platonic Solids)",
        keywords=["polyhedron", "regular", "platonic solid", "faces", "symmetry"],
        conclusion_template="There are exactly five regular convex polyhedra, each with congruent regular polygonal faces and identical vertices.",
        reasoning_framework=(
            "A regular polyhedron (Platonic solid) is a convex solid with congruent regular polygonal faces and identical vertices. "
            "There are exactly five such solids: tetrahedron, cube, octahedron, dodecahedron, and icosahedron. This is proven by analyzing the angle sums at vertices."
        ),
        key_factors=[
            "Face regularity",
            "Vertex configuration",
            "Convexity"
        ],
        primary_authority=[
            "Euclid's Elements, Book XIII",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting regularity",
        adversary_position="Non-regular or non-convex polyhedra do not satisfy these properties",
        counter_arguments=[
            "Archimedean solids and others are not regular"
        ],
        resolution_strategy="Verify all faces and vertices; check convexity.",
        entity_scope="Convex polyhedra in 3D Euclidean space",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book XIII"
    ),
    DoctrineBlock(
        topic="Euler's Formula for Polyhedra",
        keywords=["polyhedron", "euler's formula", "vertices", "edges", "faces"],
        conclusion_template="For any convex polyhedron, V - E + F = 2, where V, E, F are the numbers of vertices, edges, and faces.",
        reasoning_framework=(
            "Euler's Formula is a topological invariant for convex polyhedra. It relates the number of vertices (V), edges (E), and faces (F) by V - E + F = 2. "
            "The formula is proven using induction and planar graphs, and is foundational for polyhedral geometry."
        ),
        key_factors=[
            "Convexity",
            "Counting of vertices, edges, faces",
            "Planar graph representation"
        ],
        primary_authority=[
            "Leonhard Euler, 1758",
            "Modern topology texts"
        ],
        burden_holder="Party asserting formula",
        adversary_position="Non-convex or complex polyhedra may not satisfy the formula",
        counter_arguments=[
            "Polyhedra with holes (genus > 0) have different Euler characteristics"
        ],
        resolution_strategy="Verify convexity; apply formula.",
        entity_scope="Convex polyhedra in 3D Euclidean space",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Leonhard Euler, 1758"
    ),
    DoctrineBlock(
        topic="Volume of a Prism",
        keywords=["prism", "volume", "base area", "height"],
        conclusion_template="The volume of a prism is the area of the base times the height.",
        reasoning_framework=(
            "A prism is a solid with two congruent polygonal bases and parallelogram faces. The volume is found by multiplying the area of the base by the height (perpendicular distance between bases). "
            "This is proven by decomposing the prism into unit cubes or by Cavalieri's Principle."
        ),
        key_factors=[
            "Base area",
            "Height",
            "Congruence of bases"
        ],
        primary_authority=[
            "Euclid's Elements, Book XI",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting volume calculation",
        adversary_position="Formula does not apply to non-prismatic solids",
        counter_arguments=[
            "Pyramids and spheres require different formulas"
        ],
        resolution_strategy="Verify solid is a prism; apply formula.",
        entity_scope="Prisms in 3D Euclidean space",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book XI"
    ),
    DoctrineBlock(
        topic="Volume of a Pyramid",
        keywords=["pyramid", "volume", "base area", "height"],
        conclusion_template="The volume of a pyramid is one third the area of the base times the height.",
        reasoning_framework=(
            "A pyramid is a solid with a polygonal base and triangular faces meeting at a vertex. The volume is (1/3) × base area × height. "
            "This is proven using Cavalieri's Principle and by comparing the pyramid to a prism with the same base and height."
        ),
        key_factors=[
            "Base area",
            "Height",
            "Comparison to prism"
        ],
        primary_authority=[
            "Euclid's Elements, Book XII",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting volume calculation",
        adversary_position="Formula does not apply to non-pyramidal solids",
        counter_arguments=[
            "Prisms and spheres require different formulas"
        ],
        resolution_strategy="Verify solid is a pyramid; apply formula.",
        entity_scope="Pyramids in 3D Euclidean space",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book XII"
    ),
    DoctrineBlock(
        topic="Volume of a Cylinder",
        keywords=["cylinder", "volume", "base area", "height", "pi"],
        conclusion_template="The volume of a cylinder is πr^2h, where r is the radius and h is the height.",
        reasoning_framework=(
            "A cylinder is a solid with congruent circular bases and a curved surface. The volume is found by multiplying the area of the base (πr^2) by the height. "
            "This is proven using Cavalieri's Principle and integration."
        ),
        key_factors=[
            "Base radius",
            "Height",
            "Congruence of bases"
        ],
        primary_authority=[
            "Archimedes, On the Sphere and Cylinder",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting volume calculation",
        adversary_position="Formula does not apply to non-cylindrical solids",
        counter_arguments=[
            "Cones and spheres require different formulas"
        ],
        resolution_strategy="Verify solid is a cylinder; apply formula.",
        entity_scope="Cylinders in 3D Euclidean space",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Archimedes, On the Sphere and Cylinder"
    ),
    DoctrineBlock(
        topic="Volume of a Cone",
        keywords=["cone", "volume", "base area", "height", "pi"],
        conclusion_template="The volume of a cone is one third the area of the base times the height: (1/3)πr^2h.",
        reasoning_framework=(
            "A cone is a solid with a circular base and a vertex. The volume is (1/3) × base area × height, or (1/3)πr^2h. "
            "This is proven using Cavalieri's Principle and by comparing the cone to a cylinder with the same base and height."
        ),
        key_factors=[
            "Base radius",
            "Height",
            "Comparison to cylinder"
        ],
        primary_authority=[
            "Archimedes, On the Sphere and Cylinder",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting volume calculation",
        adversary_position="Formula does not apply to non-conical solids",
        counter_arguments=[
            "Cylinders and spheres require different formulas"
        ],
        resolution_strategy="Verify solid is a cone; apply formula.",
        entity_scope="Cones in 3D Euclidean space",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Archimedes, On the Sphere and Cylinder"
    ),
    DoctrineBlock(
        topic="Volume of a Sphere",
        keywords=["sphere", "volume", "radius", "pi"],
        conclusion_template="The volume of a sphere is (4/3)πr^3, where r is the radius.",
        reasoning_framework=(
            "A sphere is a set of points equidistant from a center in 3D space. The volume is (4/3)πr^3, derived using the method of exhaustion and calculus. "
            "This formula is foundational for solid geometry."
        ),
        key_factors=[
            "Radius",
            "Pi (π)",
            "Integration or exhaustion method"
        ],
        primary_authority=[
            "Archimedes, On the Sphere and Cylinder",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting volume calculation",
        adversary_position="Formula does not apply to non-spherical solids",
        counter_arguments=[
            "Cylinders and cones require different formulas"
        ],
        resolution_strategy="Verify solid is a sphere; apply formula.",
        entity_scope="Spheres in 3D Euclidean space",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Archimedes, On the Sphere and Cylinder"
    ),
    DoctrineBlock(
        topic="Surface Area of a Sphere",
        keywords=["sphere", "surface area", "radius", "pi"],
        conclusion_template="The surface area of a sphere is 4πr^2, where r is the radius.",
        reasoning_framework=(
            "The surface area of a sphere is 4πr^2, derived using calculus or by comparing the sphere to a circumscribed cylinder. "
            "This formula is foundational for solid geometry and physics."
        ),
        key_factors=[
            "Radius",
            "Pi (π)",
            "Integration or geometric comparison"
        ],
        primary_authority=[
            "Archimedes, On the Sphere and Cylinder",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting surface area calculation",
        adversary_position="Formula does not apply to non-spherical surfaces",
        counter_arguments=[
            "Cylinders and cones require different formulas"
        ],
        resolution_strategy="Verify surface is a sphere; apply formula.",
        entity_scope="Spheres in 3D Euclidean space",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Archimedes, On the Sphere and Cylinder"
    ),
    DoctrineBlock(
        topic="Surface Area of a Cylinder",
        keywords=["cylinder", "surface area", "radius", "height", "pi"],
        conclusion_template="The surface area of a cylinder is 2πrh + 2πr^2, where r is the radius and h is the height.",
        reasoning_framework=(
            "The surface area of a cylinder is the sum of the lateral area (2πrh) and the areas of the two bases (2πr^2). "
            "This is derived by 'unwrapping' the lateral surface into a rectangle and adding the base areas."
        ),
        key_factors=[
            "Radius",
            "Height",
            "Pi (π)"
        ],
        primary_authority=[
            "Archimedes, On the Sphere and Cylinder",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting surface area calculation",
        adversary_position="Formula does not apply to non-cylindrical surfaces",
        counter_arguments=[
            "Spheres and cones require different formulas"
        ],
        resolution_strategy="Verify surface is a cylinder; apply formula.",
        entity_scope="Cylinders in 3D Euclidean space",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Archimedes, On the Sphere and Cylinder"
    ),
    DoctrineBlock(
        topic="Surface Area of a Cone",
        keywords=["cone", "surface area", "radius", "slant height", "pi"],
        conclusion_template="The surface area of a right circular cone is πrℓ + πr^2, where r is the radius and ℓ is the slant height.",
        reasoning_framework=(
            "The surface area of a cone is the sum of the lateral area (πrℓ) and the base area (πr^2). "
            "The lateral area is found by 'unwrapping' the cone into a sector of a circle."
        ),
        key_factors=[
            "Radius",
            "Slant height",
            "Pi (π)"
        ],
        primary_authority=[
            "Archimedes, On the Sphere and Cylinder",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting surface area calculation",
        adversary_position="Formula does not apply to non-conical surfaces",
        counter_arguments=[
            "Spheres and cylinders require different formulas"
        ],
        resolution_strategy="Verify surface is a cone; apply formula.",
        entity_scope="Cones in 3D Euclidean space",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Archimedes, On the Sphere and Cylinder"
    ),
    DoctrineBlock(
        topic="Properties of Similar Solids",
        keywords=["solid", "similarity", "scaling", "volume", "surface area"],
        conclusion_template="Similar solids have corresponding lengths in the same ratio, areas in the square of the ratio, and volumes in the cube of the ratio.",
        reasoning_framework=(
            "If two solids are similar, corresponding linear dimensions are in the same ratio k. Surface areas are in the ratio k^2, and volumes are in the ratio k^3. "
            "This is proven using scaling arguments and is foundational for geometric modeling."
        ),
        key_factors=[
            "Similarity ratio",
            "Proportionality of measurements",
            "Scaling laws"
        ],
        primary_authority=[
            "Euclid's Elements, Book XII",
            "Modern geometry texts"
        ],
        burden_holder="Party asserting similarity",
        adversary_position="Non-similar solids do not have these proportional relationships",
        counter_arguments=[
            "Irregular or non-similar solids violate these ratios"
        ],
        resolution_strategy="Verify similarity; apply scaling laws.",
        entity_scope="Solids in 3D Euclidean space",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Euclid's Elements, Book XII"
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