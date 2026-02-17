import hashlib
import re

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_AUTHOR = "MATH01_engine_team"
SEMANTIC_MAP_ENGINE = "MATH01_arithmetic"

SEMANTIC_MAP = {
    # Arithmetic operations
    "addition": "add",
    "add": "add",
    "plus": "add",
    "sum": "add",
    "summation": "add",
    "total": "add",
    "aggregate": "add",
    "increase": "add",
    "augend": "add",
    "increment": "add",
    "combine": "add",
    "joining": "add",
    "put together": "add",
    "added": "add",
    "adding": "add",
    "adition": "add",  # misspelling
    "ad": "add",  # abbreviation
    "addition operation": "add",
    "addn": "add",  # abbreviation
    "sum up": "add",
    "summing": "add",
    "summed": "add",
    "plus sign": "add",
    "positive": "add",
    "increase by": "add",
    "accumulate": "add",
    "accumulation": "add",
    "more": "add",
    "extra": "add",
    "combine together": "add",
    "combin": "add",  # misspelling
    "totalize": "add",
    "totalling": "add",
    "totals": "add",
    "join": "add",
    "put together": "add",
    "together": "add",
    "sumation": "add",  # misspelling

    # Subtraction
    "subtraction": "subtract",
    "subtract": "subtract",
    "minus": "subtract",
    "difference": "subtract",
    "deduct": "subtract",
    "decrease": "subtract",
    "reduce": "subtract",
    "take away": "subtract",
    "substract": "subtract",  # misspelling
    "subtrahend": "subtract",
    "less": "subtract",
    "remove": "subtract",
    "decrement": "subtract",
    "take off": "subtract",
    "sub": "subtract",  # abbreviation
    "subtraction operation": "subtract",
    "subtr": "subtract",  # abbreviation
    "minus sign": "subtract",
    "negative": "subtract",
    "decrease by": "subtract",
    "deduction": "subtract",
    "deducting": "subtract",
    "deducted": "subtract",
    "reduction": "subtract",
    "reducing": "subtract",
    "removed": "subtract",
    "removing": "subtract",
    "take": "subtract",
    "takeout": "subtract",
    "takeaway": "subtract",
    "substracting": "subtract",  # misspelling
    "substracted": "subtract",  # misspelling
    "subtrahend": "subtract",
    "difference between": "subtract",
    "less than": "subtract",
    "lesser": "subtract",
    "minus operation": "subtract",

    # Multiplication
    "multiplication": "multiply",
    "multiply": "multiply",
    "times": "multiply",
    "product": "multiply",
    "mult": "multiply",  # abbreviation
    "multiplicand": "multiply",
    "multiplying": "multiply",
    "multiplied": "multiply",
    "multiplication operation": "multiply",
    "multiplicative": "multiply",
    "multiple": "multiply",
    "multiplicator": "multiply",
    "multip": "multiply",  # abbreviation
    "times sign": "multiply",
    "cross": "multiply",
    "cross product": "multiply",
    "x": "multiply",
    "×": "multiply",
    "factor": "multiply",
    "factors": "multiply",
    "multipl": "multiply",  # misspelling
    "multiplcation": "multiply",  # misspelling
    "multiplied by": "multiply",
    "multiplies": "multiply",
    "multiplying by": "multiply",
    "multiplication table": "multiply",
    "multiplication facts": "multiply",
    "multiplication sign": "multiply",
    "multiplication symbol": "multiply",
    "multiplicative identity": "multiply",
    "multiplicative inverse": "multiply",
    "multiplicative property": "multiply",
    "times table": "multiply",
    "times tables": "multiply",
    "times operation": "multiply",
    "timesing": "multiply",  # misspelling

    # Division
    "division": "divide",
    "divide": "divide",
    "quotient": "divide",
    "div": "divide",  # abbreviation
    "dividing": "divide",
    "divided": "divide",
    "division operation": "divide",
    "divisor": "divide",
    "dividend": "divide",
    "divided by": "divide",
    "division sign": "divide",
    "division symbol": "divide",
    "division facts": "divide",
    "division table": "divide",
    "division tables": "divide",
    "division property": "divide",
    "division identity": "divide",
    "division inverse": "divide",
    "divison": "divide",  # misspelling
    "dividing by": "divide",
    "divides": "divide",
    "divisible": "divide",
    "divisibility": "divide",
    "dividing operation": "divide",
    "split": "divide",
    "splitting": "divide",
    "split up": "divide",
    "split into": "divide",
    "partition": "divide",
    "partitioning": "divide",
    "partitioned": "divide",
    "separate": "divide",
    "separating": "divide",
    "separated": "divide",
    "ratio": "divide",
    "divid": "divide",  # misspelling
    "divded": "divide",  # misspelling
    "divison operation": "divide",  # misspelling
    "divsion": "divide",  # misspelling
    "dividng": "divide",  # misspelling

    # Arithmetic properties
    "commutative": "commutative_property",
    "commutative property": "commutative_property",
    "commutativity": "commutative_property",
    "commutative law": "commutative_property",
    "commutative rule": "commutative_property",
    "commutative operation": "commutative_property",
    "associative": "associative_property",
    "associative property": "associative_property",
    "associativity": "associative_property",
    "associative law": "associative_property",
    "associative rule": "associative_property",
    "associative operation": "associative_property",
    "distributive": "distributive_property",
    "distributive property": "distributive_property",
    "distributivity": "distributive_property",
    "distributive law": "distributive_property",
    "distributive rule": "distributive_property",
    "distributive operation": "distributive_property",
    "identity": "identity_property",
    "identity property": "identity_property",
    "identity element": "identity_property",
    "identity law": "identity_property",
    "identity rule": "identity_property",
    "identity operation": "identity_property",
    "inverse": "inverse_property",
    "inverse property": "inverse_property",
    "inverse element": "inverse_property",
    "inverse law": "inverse_property",
    "inverse rule": "inverse_property",
    "inverse operation": "inverse_property",
    "zero property": "zero_property",
    "zero": "zero_property",
    "zero element": "zero_property",
    "zero law": "zero_property",
    "zero rule": "zero_property",
    "zero operation": "zero_property",

    # Numbers
    "number": "number",
    "numbers": "number",
    "numeral": "number",
    "numerals": "number",
    "integer": "integer",
    "integers": "integer",
    "whole number": "integer",
    "whole numbers": "integer",
    "natural number": "integer",
    "natural numbers": "integer",
    "counting number": "integer",
    "counting numbers": "integer",
    "positive integer": "integer",
    "negative integer": "integer",
    "signed integer": "integer",
    "unsigned integer": "integer",
    "int": "integer",
    "intg": "integer",  # abbreviation
    "intiger": "integer",  # misspelling
    "intgers": "integer",  # misspelling
    "rational number": "rational",
    "rational numbers": "rational",
    "fraction": "rational",
    "fractions": "rational",
    "decimal": "decimal",
    "decimals": "decimal",
    "real number": "real",
    "real numbers": "real",
    "irrational number": "irrational",
    "irrational numbers": "irrational",
    "complex number": "complex",
    "complex numbers": "complex",
    "imaginary number": "complex",
    "imaginary numbers": "complex",
    "prime number": "prime",
    "prime numbers": "prime",
    "composite number": "composite",
    "composite numbers": "composite",
    "even number": "even",
    "even numbers": "even",
    "odd number": "odd",
    "odd numbers": "odd",
    "digit": "digit",
    "digits": "digit",
    "place value": "place_value",
    "place values": "place_value",
    "base": "base",
    "bases": "base",
    "radix": "base",
    "numeration": "numeration",
    "numeration system": "numeration",
    "numeration systems": "numeration",
    "number system": "numeration",
    "number systems": "numeration",
    "notation": "notation",
    "notational": "notation",
    "notation system": "notation",
    "notation systems": "notation",
    "arabic numeral": "number",
    "roman numeral": "number",
    "binary": "binary",
    "binary number": "binary",
    "binary numbers": "binary",
    "octal": "octal",
    "octal number": "octal",
    "octal numbers": "octal",
    "hexadecimal": "hexadecimal",
    "hexadecimal number": "hexadecimal",
    "hexadecimal numbers": "hexadecimal",

    # Place value and notation
    "ones": "ones_place",
    "units": "ones_place",
    "unit": "ones_place",
    "tens": "tens_place",
    "hundreds": "hundreds_place",
    "thousands": "thousands_place",
    "millions": "millions_place",
    "billions": "billions_place",
    "trillions": "trillions_place",
    "ones place": "ones_place",
    "tens place": "tens_place",
    "hundreds place": "hundreds_place",
    "thousands place": "thousands_place",
    "millions place": "millions_place",
    "billions place": "billions_place",
    "trillions place": "trillions_place",
    "place": "place_value",
    "place value": "place_value",
    "place values": "place_value",
    "digit place": "place_value",
    "digit places": "place_value",
    "decimal place": "decimal_place",
    "decimal places": "decimal_place",
    "fractional place": "decimal_place",
    "fractional places": "decimal_place",
    "rightmost digit": "ones_place",
    "leftmost digit": "highest_place",
    "most significant digit": "highest_place",
    "least significant digit": "ones_place",

    # Arithmetic expressions
    "expression": "expression",
    "expressions": "expression",
    "arithmetic expression": "expression",
    "arithmetic expressions": "expression",
    "math expression": "expression",
    "math expressions": "expression",
    "formula": "expression",
    "formulas": "expression",
    "equation": "equation",
    "equations": "equation",
    "arithmetic equation": "equation",
    "arithmetic equations": "equation",
    "math equation": "equation",
    "math equations": "equation",
    "statement": "expression",
    "statements": "expression",
    "problem": "expression",
    "problems": "expression",
    "task": "expression",
    "tasks": "expression",
    "question": "expression",
    "questions": "expression",
    "operation": "operation",
    "operations": "operation",
    "arithmetic operation": "operation",
    "arithmetic operations": "operation",
    "math operation": "operation",
    "math operations": "operation",
    "calculate": "calculate",
    "calculation": "calculate",
    "calculations": "calculate",
    "computing": "calculate",
    "compute": "calculate",
    "computations": "calculate",
    "computation": "calculate",
    "solving": "solve",
    "solve": "solve",
    "solution": "solve",
    "solutions": "solve",
    "find": "solve",
    "finding": "solve",
    "answer": "solve",
    "answers": "solve",
    "result": "solve",
    "results": "solve",
    "evaluate": "evaluate",
    "evaluation": "evaluate",
    "evaluating": "evaluate",
    "simplify": "simplify",
    "simplification": "simplify",
    "simplifying": "simplify",
    "reduce": "simplify",
    "reducing": "simplify",
    "reduction": "simplify",

    # Symbols
    "+": "add",
    "-": "subtract",
    "*": "multiply",
    "×": "multiply",
    "x": "multiply",
    "/": "divide",
    "÷": "divide",
    "=": "equals",
    "equals": "equals",
    "equal": "equals",
    "is equal to": "equals",
    "is": "equals",
    "equal sign": "equals",
    "equal symbol": "equals",
    "equal to": "equals",
    "equivalent": "equals",
    "equivalence": "equals",
    "equivalent to": "equals",
    "equate": "equals",
    "equating": "equals",
    "equated": "equals",

    # Miscellaneous
    "arithmetic": "arithmetic",
    "math": "arithmetic",
    "mathematics": "arithmetic",
    "mathematic": "arithmetic",
    "mathematician": "arithmetic",
    "mathematicians": "arithmetic",
    "maths": "arithmetic",
    "arithmetics": "arithmetic",
    "mathematical": "arithmetic",
    "mathematical operation": "operation",
    "mathematical operations": "operation",
    "mathematical expression": "expression",
    "mathematical expressions": "expression",
    "mathematical equation": "equation",
    "mathematical equations": "equation",
    "mathematical problem": "expression",
    "mathematical problems": "expression",
    "mathematical task": "expression",
    "mathematical tasks": "expression",

    # Order of operations
    "order of operations": "order_of_operations",
    "pemdas": "order_of_operations",
    "bedmas": "order_of_operations",
    "bodmas": "order_of_operations",
    "bidmas": "order_of_operations",
    "precedence": "order_of_operations",
    "priority": "order_of_operations",
    "parentheses": "parentheses",
    "brackets": "parentheses",
    "parenthesis": "parentheses",
    "bracket": "parentheses",
    "grouping": "parentheses",
    "group": "parentheses",
    "grouped": "parentheses",
    "grouping symbol": "parentheses",
    "grouping symbols": "parentheses",

    # Estimation and rounding
    "estimate": "estimate",
    "estimation": "estimate",
    "estimating": "estimate",
    "round": "round",
    "rounding": "round",
    "rounded": "round",
    "approximate": "round",
    "approximation": "round",
    "approximating": "round",
    "nearest": "round",
    "nearest integer": "round",
    "nearest ten": "round",
    "nearest hundred": "round",
    "nearest thousand": "round",
    "nearest value": "round",
    "nearest place": "round",

    # Comparison
    "compare": "compare",
    "comparison": "compare",
    "comparing": "compare",
    "greater": "greater",
    "greater than": "greater",
    "more than": "greater",
    "larger": "greater",
    "larger than": "greater",
    "biggest": "greater",
    "biggest value": "greater",
    "maximum": "greater",
    "max": "greater",
    "largest": "greater",
    "largest value": "greater",
    "less": "less",
    "less than": "less",
    "smaller": "less",
    "smaller than": "less",
    "minimum": "less",
    "min": "less",
    "smallest": "less",
    "smallest value": "less",
    "lowest": "less",
    "lowest value": "less",

    # Misc arithmetic terms
    "operation": "operation",
    "operations": "operation",
    "operand": "operand",
    "operands": "operand",
    "operator": "operator",
    "operators": "operator",
    "symbol": "symbol",
    "symbols": "symbol",
    "notation": "notation",
    "notational": "notation",
    "notation system": "notation",
    "notation systems": "notation",

    # Arithmetic sequence and series
    "sequence": "sequence",
    "sequences": "sequence",
    "arithmetic sequence": "sequence",
    "arithmetic sequences": "sequence",
    "series": "series",
    "arithmetic series": "series",
    "arithmetic progression": "sequence",
    "progression": "sequence",
    "progressions": "sequence",

    # Misc
    "calculate": "calculate",
    "calculation": "calculate",
    "calculations": "calculate",
    "computing": "calculate",
    "compute": "calculate",
    "computations": "calculate",
    "computation": "calculate",
    "solving": "solve",
    "solve": "solve",
    "solution": "solve",
    "solutions": "solve",
    "find": "solve",
    "finding": "solve",
    "answer": "solve",
    "answers": "solve",
    "result": "solve",
    "results": "solve",
    "evaluate": "evaluate",
    "evaluation": "evaluate",
    "evaluating": "evaluate",
    "simplify": "simplify",
    "simplification": "simplify",
    "simplifying": "simplify",
    "reduce": "simplify",
    "reducing": "simplify",
    "reduction": "simplify",

    # Misspellings and variants
    "arithmatic": "arithmetic",  # misspelling
    "arithmetics": "arithmetic",
    "mathematic": "arithmetic",
    "mathematician": "arithmetic",
    "mathematicians": "arithmetic",
    "maths": "arithmetic",
    "mathematical": "arithmetic",
    "mathematical operation": "operation",
    "mathematical operations": "operation",
    "mathematical expression": "expression",
    "mathematical expressions": "expression",
    "mathematical equation": "equation",
    "mathematical equations": "equation",
    "mathematical problem": "expression",
    "mathematical problems": "expression",
    "mathematical task": "expression",
    "mathematical tasks": "expression",

    # Additional synonyms, abbreviations, misspellings
    "addtion": "add",  # misspelling
    "subtrction": "subtract",  # misspelling
    "multipication": "multiply",  # misspelling
    "divison": "divide",  # misspelling
    "eqation": "equation",  # misspelling
    "exprssion": "expression",  # misspelling
    "calclate": "calculate",  # misspelling
    "soluton": "solve",  # misspelling
    "evluate": "evaluate",  # misspelling
    "simplfy": "simplify",  # misspelling
    "redction": "simplify",  # misspelling
    "estimte": "estimate",  # misspelling
    "rouding": "round",  # misspelling
    "comparson": "compare",  # misspelling
    "sequnce": "sequence",  # misspelling
    "seres": "series",  # misspelling
    "progession": "sequence",  # misspelling
    "progresion": "sequence",  # misspelling
    "progessions": "sequence",  # misspelling
    "arithmatic sequence": "sequence",  # misspelling
    "arithmatic series": "series",  # misspelling
    "arithmatic progression": "sequence",  # misspelling
    "arithmatic progressions": "sequence",  # misspelling
    "mathematic operation": "operation",  # misspelling
    "mathematic operations": "operation",  # misspelling
    "mathematic expression": "expression",  # misspelling
    "mathematic expressions": "expression",  # misspelling
    "mathematic equation": "equation",  # misspelling
    "mathematic equations": "equation",  # misspelling
    "mathematic problem": "expression",  # misspelling
    "mathematic problems": "expression",  # misspelling
    "mathematic task": "expression",  # misspelling
    "mathematic tasks": "expression",  # misspelling
}

_EXPECTED_ENTRY_COUNT = len(SEMANTIC_MAP)

def _compute_map_hash():
    items = sorted(SEMANTIC_MAP.items())
    map_str = "".join(f"{k}:{v};" for k, v in items)
    meta = f"{SEMANTIC_MAP_VERSION}|{SEMANTIC_MAP_AUTHOR}|{SEMANTIC_MAP_ENGINE}|{_EXPECTED_ENTRY_COUNT}"
    full_str = map_str + meta
    return hashlib.sha256(full_str.encode("utf-8")).hexdigest()

_MAP_INTEGRITY_HASH = _compute_map_hash()

def verify_integrity():
    actual_count = len(SEMANTIC_MAP)
    hash_check = _compute_map_hash()
    is_valid = (actual_count == _EXPECTED_ENTRY_COUNT) and (hash_check == _MAP_INTEGRITY_HASH)
    return {
        "status": "ok" if is_valid else "error",
        "entries": actual_count,
        "hash": hash_check,
        "is_valid": is_valid,
    }

def normalize_term(term: str) -> str:
    t = term.strip().lower()
    t = re.sub(r"\s+", " ", t)
    return SEMANTIC_MAP.get(t, t)

def get_related_terms(term: str) -> list:
    normalized = normalize_term(term)
    related = [k for k, v in SEMANTIC_MAP.items() if v == normalized]
    return sorted(set(related))

def get_all_mappings() -> dict:
    return dict(SEMANTIC_MAP)