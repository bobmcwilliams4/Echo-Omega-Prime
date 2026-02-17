"""
MATH10 — Geometry Intelligence Engine
TIE-20 Compliant | Tier 13 Mathematics | PORT 8572
Euclidean geometry, coordinate geometry, trigonometry, transformations,
computational geometry, 3D geometry — all pure Python.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import math
import sys
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
ENGINE_DIR = Path(__file__).parent
ENGINES_ROOT = ENGINE_DIR.parent
sys.path.insert(0, str(ENGINES_ROOT))

ENGINE_ID = "MATH10"
ENGINE_NAME = "Geometry Intelligence Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8572
ENGINE_TIER = 13
ENGINE_MODE = "DET"
ENGINE_AUTH = 5.0

# ---------------------------------------------------------------------------
# Loguru configuration
# ---------------------------------------------------------------------------
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="DEBUG",
)
LOG_PATH = ENGINE_DIR / "logs"
LOG_PATH.mkdir(exist_ok=True)
logger.add(LOG_PATH / "math10.log", rotation="10 MB", retention="30 days", level="DEBUG")
AUDIT_PATH = ENGINE_DIR / "audit_trail.jsonl"

# ---------------------------------------------------------------------------
# TIE-1: Three-Layer Response
# ---------------------------------------------------------------------------
class ResponseLayer(str, Enum):
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"

# ---------------------------------------------------------------------------
# TIE-2: Response Modes
# ---------------------------------------------------------------------------
class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

# ---------------------------------------------------------------------------
# TIE-5: Confidence Stratification
# ---------------------------------------------------------------------------
class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

# ---------------------------------------------------------------------------
# TIE-13: Zoned Analysis
# ---------------------------------------------------------------------------
class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------
class GeometryQuery(BaseModel):
    query: str = Field(..., description="Natural language or structured geometry query")
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    zone: AnalysisZone = Field(default=AnalysisZone.REPORTING)
    show_steps: bool = Field(default=True)
    session_id: Optional[str] = None

class ShapeAreaRequest(BaseModel):
    shape: str
    params: dict[str, float]

class CoordinateRequest(BaseModel):
    operation: str
    points: list[list[float]]
    params: Optional[dict[str, float]] = None

class TrigRequest(BaseModel):
    operation: str
    params: dict[str, float]

class TransformRequest(BaseModel):
    operation: str
    points: list[list[float]]
    params: dict[str, float]

class CompGeoRequest(BaseModel):
    operation: str
    points: list[list[float]]
    params: Optional[dict[str, Any]] = None

class Solid3DRequest(BaseModel):
    shape: str
    params: dict[str, float]

class TriangleSolveRequest(BaseModel):
    case: str  # SSS, SAS, ASA, AAS, SSA
    known: dict[str, float]

class EngineResponse(BaseModel):
    engine_id: str = ENGINE_ID
    version: str = ENGINE_VERSION
    query_id: str
    layer: str
    mode: str
    zone: str
    result: Any
    steps: list[str] = []
    confidence: str = ConfidenceLevel.DEFENSIBLE.value
    confidence_score: float = 1.0
    authorities: list[str] = []
    determinism_hash: str = ""
    latency_ms: float = 0.0
    timestamp: str = ""

# ---------------------------------------------------------------------------
# TIE-3: Doctrine Cache (loaded from JSON)
# ---------------------------------------------------------------------------
DOCTRINE_CACHE: list[dict[str, Any]] = []

def _load_doctrine_cache() -> list[dict[str, Any]]:
    cache_path = ENGINE_DIR / "doctrine_cache.json"
    if cache_path.exists():
        with open(cache_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            logger.info("Loaded {} doctrine entries from cache", len(data))
            return data
    logger.warning("No doctrine_cache.json found at {}", cache_path)
    return []

def doctrine_lookup(topic: str) -> Optional[dict[str, Any]]:
    topic_lower = topic.lower()
    for entry in DOCTRINE_CACHE:
        keywords = [k.lower() for k in entry.get("keywords", [])]
        if any(kw in topic_lower for kw in keywords):
            return entry
    return None

# ---------------------------------------------------------------------------
# TIE-6: Semantic Normalization
# ---------------------------------------------------------------------------
SEMANTIC_DICT: dict[str, str] = {}

def _load_semantic_dict() -> dict[str, str]:
    path = ENGINE_DIR / "semantic_dict.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            logger.info("Loaded {} semantic mappings", len(data))
            return data
    return {}

def normalize_term(term: str) -> str:
    return SEMANTIC_DICT.get(term.lower().strip(), term.lower().strip())

# ---------------------------------------------------------------------------
# TIE-10: Coverage Map
# ---------------------------------------------------------------------------
COVERAGE_MAP: dict[str, Any] = {}

def _load_coverage_map() -> dict[str, Any]:
    path = ENGINE_DIR / "coverage_map.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return {}

COVERAGE_HITS: dict[str, int] = {}

def record_coverage_hit(domain: str) -> None:
    COVERAGE_HITS[domain] = COVERAGE_HITS.get(domain, 0) + 1

# ---------------------------------------------------------------------------
# TIE-11: Metrics Collector
# ---------------------------------------------------------------------------
class MetricsCollector:
    def __init__(self) -> None:
        self.total_queries: int = 0
        self.cache_hits: int = 0
        self.cache_misses: int = 0
        self.errors: int = 0
        self.latencies: list[float] = []
        self.start_time: float = time.time()

    def record_query(self, latency_ms: float, cache_hit: bool) -> None:
        self.total_queries += 1
        self.latencies.append(latency_ms)
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

    def record_error(self) -> None:
        self.errors += 1

    def summary(self) -> dict[str, Any]:
        uptime = time.time() - self.start_time
        avg_lat = sum(self.latencies) / len(self.latencies) if self.latencies else 0.0
        return {
            "total_queries": self.total_queries,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "hit_rate": self.cache_hits / max(self.total_queries, 1),
            "errors": self.errors,
            "error_rate": self.errors / max(self.total_queries, 1),
            "avg_latency_ms": round(avg_lat, 2),
            "p95_latency_ms": round(sorted(self.latencies)[int(len(self.latencies) * 0.95)] if self.latencies else 0, 2),
            "uptime_seconds": round(uptime, 1),
            "queries_per_minute": round(self.total_queries / max(uptime / 60, 0.0167), 2),
        }

METRICS = MetricsCollector()

# ---------------------------------------------------------------------------
# TIE-9: Drift Watcher
# ---------------------------------------------------------------------------
class DriftWatcher:
    def __init__(self) -> None:
        self.baseline_hashes: dict[str, str] = {}
        self.drift_events: list[dict[str, Any]] = []

    def set_baseline(self, key: str, value: str) -> None:
        self.baseline_hashes[key] = hashlib.sha256(value.encode()).hexdigest()

    def check_drift(self, key: str, value: str) -> bool:
        current = hashlib.sha256(value.encode()).hexdigest()
        if key in self.baseline_hashes and self.baseline_hashes[key] != current:
            self.drift_events.append({
                "key": key,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "old_hash": self.baseline_hashes[key],
                "new_hash": current,
            })
            self.baseline_hashes[key] = current
            return True
        if key not in self.baseline_hashes:
            self.baseline_hashes[key] = current
        return False

    def report(self) -> list[dict[str, Any]]:
        return self.drift_events

DRIFT = DriftWatcher()

# ---------------------------------------------------------------------------
# TIE-8: Telemetry
# ---------------------------------------------------------------------------
class TelemetryRecord(BaseModel):
    query_id: str
    timestamp: str
    engine_id: str = ENGINE_ID
    layer: str
    latency_ms: float
    cache_hit: bool
    error: Optional[str] = None

TELEMETRY_LOG: list[dict[str, Any]] = []

def record_telemetry(rec: TelemetryRecord) -> None:
    TELEMETRY_LOG.append(rec.model_dump())
    if len(TELEMETRY_LOG) > 5000:
        TELEMETRY_LOG.pop(0)

# ---------------------------------------------------------------------------
# TIE-15: Audit Trail JSONL
# ---------------------------------------------------------------------------
def write_audit(entry: dict[str, Any]) -> None:
    entry["audit_ts"] = datetime.now(timezone.utc).isoformat()
    try:
        with open(AUDIT_PATH, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")
    except Exception as exc:
        logger.error("Audit write failed: {}", exc)

# ---------------------------------------------------------------------------
# TIE-16: Determinism Hash
# ---------------------------------------------------------------------------
def determinism_hash(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode()).hexdigest()

# ---------------------------------------------------------------------------
# TIE-14: Fact Fragility Scoring
# ---------------------------------------------------------------------------
def fact_fragility_score(result: Any) -> dict[str, Any]:
    return {
        "verifiability": "HIGH",
        "recharacterization_risk": "LOW",
        "testimony_dependence": "NONE",
        "fragility_index": 0.05,
        "note": "Mathematical results are deterministic and fully verifiable.",
    }

# ---------------------------------------------------------------------------
# TIE-4: Authority Hardening
# ---------------------------------------------------------------------------
AUTHORITY_HIERARCHY: list[dict[str, Any]] = [
    {"level": 1, "name": "Euclid_Elements", "weight": 1.0, "source": "Euclid, Elements (c. 300 BC)"},
    {"level": 2, "name": "Hilbert_Axioms", "weight": 0.95, "source": "Hilbert, Foundations of Geometry (1899)"},
    {"level": 3, "name": "Standard_Textbooks", "weight": 0.85, "source": "Coxeter, Geometry Revisited; Stewart Calculus"},
    {"level": 4, "name": "Computational_References", "weight": 0.80, "source": "de Berg et al., Computational Geometry (2008)"},
    {"level": 5, "name": "Derived_Formulas", "weight": 0.70, "source": "Engine-derived via axioms"},
]

def resolve_authority(topic: str) -> list[str]:
    doctrine = doctrine_lookup(topic)
    if doctrine:
        return doctrine.get("primary_authority", ["Euclid, Elements"])
    return ["Euclid, Elements", "Standard mathematical axioms"]

# ---------------------------------------------------------------------------
# TIE-19: Multi-Doctrine Decomposition
# ---------------------------------------------------------------------------
class IssueCategory(str, Enum):
    EUCLIDEAN_2D = "EUCLIDEAN_2D"
    EUCLIDEAN_3D = "EUCLIDEAN_3D"
    COORDINATE = "COORDINATE"
    TRIGONOMETRY = "TRIGONOMETRY"
    TRANSFORMATIONS = "TRANSFORMATIONS"
    COMPUTATIONAL = "COMPUTATIONAL"
    ANALYTIC = "ANALYTIC"
    PROOF = "PROOF"

def classify_issue(query: str) -> list[IssueCategory]:
    q = query.lower()
    cats: list[IssueCategory] = []
    if any(w in q for w in ["area", "perimeter", "triangle", "circle", "rectangle", "polygon", "ellipse", "trapezoid", "parallelogram"]):
        cats.append(IssueCategory.EUCLIDEAN_2D)
    if any(w in q for w in ["sphere", "cylinder", "cone", "prism", "pyramid", "torus", "volume", "surface area", "3d", "solid"]):
        cats.append(IssueCategory.EUCLIDEAN_3D)
    if any(w in q for w in ["distance", "midpoint", "slope", "line equation", "coordinate", "intercept", "perpendicular", "parallel"]):
        cats.append(IssueCategory.COORDINATE)
    if any(w in q for w in ["sin", "cos", "tan", "trig", "angle", "law of sines", "law of cosines", "identity", "radian"]):
        cats.append(IssueCategory.TRIGONOMETRY)
    if any(w in q for w in ["rotation", "reflection", "translation", "scaling", "transform", "matrix"]):
        cats.append(IssueCategory.TRANSFORMATIONS)
    if any(w in q for w in ["convex hull", "point-in-polygon", "intersection", "shoelace", "graham", "ray casting", "computational"]):
        cats.append(IssueCategory.COMPUTATIONAL)
    if any(w in q for w in ["tangent line", "arc length", "sector", "circle equation", "analytic"]):
        cats.append(IssueCategory.ANALYTIC)
    if any(w in q for w in ["prove", "proof", "axiom", "theorem", "postulate"]):
        cats.append(IssueCategory.PROOF)
    if not cats:
        cats.append(IssueCategory.EUCLIDEAN_2D)
    return cats

# ═══════════════════════════════════════════════════════════════════════════
# GEOMETRY COMPUTATION CORE — REAL IMPLEMENTATIONS
# ═══════════════════════════════════════════════════════════════════════════

# ---------------------------------------------------------------------------
# 2D Shape Computations
# ---------------------------------------------------------------------------

def triangle_area_heron(a: float, b: float, c: float) -> tuple[float, list[str]]:
    """Area of triangle via Heron's formula given three side lengths."""
    steps: list[str] = []
    if a + b <= c or a + c <= b or b + c <= a:
        raise ValueError(f"Invalid triangle sides: {a}, {b}, {c} — triangle inequality violated.")
    s = (a + b + c) / 2.0
    steps.append(f"Semi-perimeter s = (a+b+c)/2 = ({a}+{b}+{c})/2 = {s}")
    area_sq = s * (s - a) * (s - b) * (s - c)
    steps.append(f"s(s-a)(s-b)(s-c) = {s}*{s - a}*{s - b}*{s - c} = {area_sq}")
    area = math.sqrt(area_sq)
    steps.append(f"Area = sqrt({area_sq}) = {area}")
    return area, steps

def triangle_area_cross(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float) -> tuple[float, list[str]]:
    """Area of triangle via cross product given vertices."""
    steps: list[str] = []
    steps.append(f"Vertices: ({x1},{y1}), ({x2},{y2}), ({x3},{y3})")
    area = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2.0
    steps.append(f"Area = |({x2}-{x1})*({y3}-{y1}) - ({x3}-{x1})*({y2}-{y1})| / 2 = {area}")
    return area, steps

def triangle_centroid(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float) -> tuple[tuple[float, float], list[str]]:
    """Centroid of triangle."""
    cx = (x1 + x2 + x3) / 3.0
    cy = (y1 + y2 + y3) / 3.0
    steps = [f"Centroid = (({x1}+{x2}+{x3})/3, ({y1}+{y2}+{y3})/3) = ({cx}, {cy})"]
    return (cx, cy), steps

def triangle_incircle(a: float, b: float, c: float) -> tuple[dict[str, float], list[str]]:
    """Incircle radius given side lengths."""
    steps: list[str] = []
    s = (a + b + c) / 2.0
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    r = area / s
    steps.append(f"s = {s}, Area = {area}")
    steps.append(f"Inradius r = Area/s = {area}/{s} = {r}")
    return {"inradius": r, "area": area, "semi_perimeter": s}, steps

def triangle_circumcircle(a: float, b: float, c: float) -> tuple[dict[str, float], list[str]]:
    """Circumcircle radius given side lengths."""
    steps: list[str] = []
    s = (a + b + c) / 2.0
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    R = (a * b * c) / (4.0 * area)
    steps.append(f"Area (Heron) = {area}")
    steps.append(f"Circumradius R = abc/(4*Area) = {a}*{b}*{c}/(4*{area}) = {R}")
    return {"circumradius": R, "area": area}, steps

def rectangle_props(length: float, width: float) -> tuple[dict[str, float], list[str]]:
    """Area, perimeter, diagonal of rectangle."""
    area = length * width
    perimeter = 2 * (length + width)
    diagonal = math.sqrt(length**2 + width**2)
    steps = [
        f"Area = {length} * {width} = {area}",
        f"Perimeter = 2*({length}+{width}) = {perimeter}",
        f"Diagonal = sqrt({length}^2+{width}^2) = {diagonal}",
    ]
    return {"area": area, "perimeter": perimeter, "diagonal": diagonal}, steps

def circle_props(radius: float) -> tuple[dict[str, float], list[str]]:
    """Area, circumference, diameter of circle."""
    area = math.pi * radius**2
    circ = 2 * math.pi * radius
    steps = [
        f"Area = pi*r^2 = pi*{radius}^2 = {area}",
        f"Circumference = 2*pi*r = 2*pi*{radius} = {circ}",
        f"Diameter = 2r = {2 * radius}",
    ]
    return {"area": area, "circumference": circ, "diameter": 2 * radius}, steps

def ellipse_props(a: float, b: float) -> tuple[dict[str, float], list[str]]:
    """Area and approximate perimeter of ellipse with semi-axes a, b."""
    area = math.pi * a * b
    # Ramanujan approximation
    h = ((a - b) / (a + b))**2
    perimeter = math.pi * (a + b) * (1 + 3 * h / (10 + math.sqrt(4 - 3 * h)))
    steps = [
        f"Area = pi*a*b = pi*{a}*{b} = {area}",
        f"h = ((a-b)/(a+b))^2 = {h}",
        f"Perimeter (Ramanujan) ~ pi*(a+b)*(1+3h/(10+sqrt(4-3h))) = {perimeter}",
    ]
    return {"area": area, "perimeter_approx": perimeter, "semi_major": max(a, b), "semi_minor": min(a, b)}, steps

def regular_polygon_props(n: int, side: float) -> tuple[dict[str, float], list[str]]:
    """Area, perimeter, apothem of regular n-gon with given side length."""
    if n < 3:
        raise ValueError("Polygon must have at least 3 sides.")
    perimeter = n * side
    apothem = side / (2 * math.tan(math.pi / n))
    area = 0.5 * perimeter * apothem
    interior_angle = (n - 2) * 180.0 / n
    steps = [
        f"n = {n}, side = {side}",
        f"Perimeter = n*s = {perimeter}",
        f"Apothem = s/(2*tan(pi/n)) = {apothem}",
        f"Area = 0.5*P*a = 0.5*{perimeter}*{apothem} = {area}",
        f"Interior angle = (n-2)*180/n = {interior_angle} degrees",
    ]
    return {"area": area, "perimeter": perimeter, "apothem": apothem, "interior_angle": interior_angle}, steps

def trapezoid_props(a: float, b: float, h: float) -> tuple[dict[str, float], list[str]]:
    """Area of trapezoid with parallel sides a, b and height h."""
    area = 0.5 * (a + b) * h
    steps = [
        f"Parallel sides: a={a}, b={b}, height={h}",
        f"Area = 0.5*(a+b)*h = 0.5*({a}+{b})*{h} = {area}",
    ]
    return {"area": area}, steps

def parallelogram_props(base: float, height: float, side: float, angle_deg: float) -> tuple[dict[str, float], list[str]]:
    """Area, perimeter, diagonals of parallelogram."""
    area = base * height
    perimeter = 2 * (base + side)
    angle_rad = math.radians(angle_deg)
    d1 = math.sqrt(base**2 + side**2 + 2 * base * side * math.cos(angle_rad))
    d2 = math.sqrt(base**2 + side**2 - 2 * base * side * math.cos(angle_rad))
    steps = [
        f"Area = base*height = {base}*{height} = {area}",
        f"Perimeter = 2*(base+side) = 2*({base}+{side}) = {perimeter}",
        f"Diagonal d1 = sqrt(a^2+b^2+2ab*cos(theta)) = {d1}",
        f"Diagonal d2 = sqrt(a^2+b^2-2ab*cos(theta)) = {d2}",
    ]
    return {"area": area, "perimeter": perimeter, "diagonal_1": d1, "diagonal_2": d2}, steps

# ---------------------------------------------------------------------------
# 3D Solid Computations
# ---------------------------------------------------------------------------

def sphere_props(radius: float) -> tuple[dict[str, float], list[str]]:
    """Volume and surface area of sphere."""
    vol = (4.0 / 3.0) * math.pi * radius**3
    sa = 4.0 * math.pi * radius**2
    steps = [
        f"Volume = (4/3)*pi*r^3 = (4/3)*pi*{radius}^3 = {vol}",
        f"Surface area = 4*pi*r^2 = 4*pi*{radius}^2 = {sa}",
    ]
    return {"volume": vol, "surface_area": sa}, steps

def cylinder_props(radius: float, height: float) -> tuple[dict[str, float], list[str]]:
    """Volume and surface area of cylinder."""
    vol = math.pi * radius**2 * height
    lateral = 2 * math.pi * radius * height
    sa = lateral + 2 * math.pi * radius**2
    steps = [
        f"Volume = pi*r^2*h = pi*{radius}^2*{height} = {vol}",
        f"Lateral SA = 2*pi*r*h = {lateral}",
        f"Total SA = lateral + 2*pi*r^2 = {sa}",
    ]
    return {"volume": vol, "surface_area": sa, "lateral_area": lateral}, steps

def cone_props(radius: float, height: float) -> tuple[dict[str, float], list[str]]:
    """Volume and surface area of cone."""
    slant = math.sqrt(radius**2 + height**2)
    vol = (1.0 / 3.0) * math.pi * radius**2 * height
    lateral = math.pi * radius * slant
    sa = lateral + math.pi * radius**2
    steps = [
        f"Slant height = sqrt(r^2+h^2) = sqrt({radius}^2+{height}^2) = {slant}",
        f"Volume = (1/3)*pi*r^2*h = {vol}",
        f"Lateral SA = pi*r*l = pi*{radius}*{slant} = {lateral}",
        f"Total SA = lateral + pi*r^2 = {sa}",
    ]
    return {"volume": vol, "surface_area": sa, "slant_height": slant, "lateral_area": lateral}, steps

def prism_props(base_area: float, base_perimeter: float, height: float) -> tuple[dict[str, float], list[str]]:
    """Volume and surface area of a prism given base area, perimeter, height."""
    vol = base_area * height
    lateral = base_perimeter * height
    sa = lateral + 2 * base_area
    steps = [
        f"Volume = base_area*h = {base_area}*{height} = {vol}",
        f"Lateral SA = perimeter*h = {base_perimeter}*{height} = {lateral}",
        f"Total SA = lateral + 2*base_area = {sa}",
    ]
    return {"volume": vol, "surface_area": sa, "lateral_area": lateral}, steps

def pyramid_props(base_area: float, base_perimeter: float, height: float, slant_height: float) -> tuple[dict[str, float], list[str]]:
    """Volume and surface area of pyramid."""
    vol = (1.0 / 3.0) * base_area * height
    lateral = 0.5 * base_perimeter * slant_height
    sa = lateral + base_area
    steps = [
        f"Volume = (1/3)*base_area*h = (1/3)*{base_area}*{height} = {vol}",
        f"Lateral SA = 0.5*perimeter*slant = 0.5*{base_perimeter}*{slant_height} = {lateral}",
        f"Total SA = lateral + base_area = {sa}",
    ]
    return {"volume": vol, "surface_area": sa, "lateral_area": lateral}, steps

def torus_props(major_r: float, minor_r: float) -> tuple[dict[str, float], list[str]]:
    """Volume and surface area of torus (R = major, r = minor)."""
    vol = 2 * math.pi**2 * major_r * minor_r**2
    sa = 4 * math.pi**2 * major_r * minor_r
    steps = [
        f"Volume = 2*pi^2*R*r^2 = 2*pi^2*{major_r}*{minor_r}^2 = {vol}",
        f"Surface area = 4*pi^2*R*r = 4*pi^2*{major_r}*{minor_r} = {sa}",
    ]
    return {"volume": vol, "surface_area": sa}, steps

# ---------------------------------------------------------------------------
# Coordinate Geometry
# ---------------------------------------------------------------------------

def distance_2d(x1: float, y1: float, x2: float, y2: float) -> tuple[float, list[str]]:
    """Euclidean distance between two points."""
    d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    steps = [f"d = sqrt(({x2}-{x1})^2 + ({y2}-{y1})^2) = sqrt({(x2-x1)**2}+{(y2-y1)**2}) = {d}"]
    return d, steps

def midpoint_2d(x1: float, y1: float, x2: float, y2: float) -> tuple[tuple[float, float], list[str]]:
    """Midpoint of segment."""
    mx = (x1 + x2) / 2.0
    my = (y1 + y2) / 2.0
    steps = [f"Midpoint = (({x1}+{x2})/2, ({y1}+{y2})/2) = ({mx}, {my})"]
    return (mx, my), steps

def slope_2d(x1: float, y1: float, x2: float, y2: float) -> tuple[Optional[float], list[str]]:
    """Slope of line through two points."""
    if abs(x2 - x1) < 1e-15:
        return None, [f"Vertical line: x = {x1}, slope is undefined."]
    m = (y2 - y1) / (x2 - x1)
    steps = [f"Slope m = ({y2}-{y1})/({x2}-{x1}) = {y2 - y1}/{x2 - x1} = {m}"]
    return m, steps

def line_equation_point_slope(x1: float, y1: float, m: float) -> tuple[dict[str, Any], list[str]]:
    """Line equation from point and slope."""
    b = y1 - m * x1
    steps = [
        f"Point-slope: y - {y1} = {m}(x - {x1})",
        f"Slope-intercept: y = {m}x + {b}",
        f"General form: {m}x - y + {b} = 0",
    ]
    return {"slope": m, "y_intercept": b, "slope_intercept": f"y = {m}x + {b}", "general": f"{m}x - y + {b} = 0"}, steps

def line_equation_two_points(x1: float, y1: float, x2: float, y2: float) -> tuple[dict[str, Any], list[str]]:
    """Line equation from two points."""
    m_val, m_steps = slope_2d(x1, y1, x2, y2)
    if m_val is None:
        return {"type": "vertical", "equation": f"x = {x1}"}, [f"Vertical line x = {x1}"]
    result, steps = line_equation_point_slope(x1, y1, m_val)
    return result, m_steps + steps

def perpendicular_slope(m: float) -> tuple[float, list[str]]:
    """Perpendicular slope."""
    if abs(m) < 1e-15:
        return float("inf"), ["Slope is 0, perpendicular is vertical (undefined slope)."]
    mp = -1.0 / m
    steps = [f"Perpendicular slope = -1/m = -1/{m} = {mp}"]
    return mp, steps

def angle_between_lines(m1: float, m2: float) -> tuple[float, list[str]]:
    """Acute angle between two lines in degrees."""
    denom = 1.0 + m1 * m2
    if abs(denom) < 1e-15:
        return 90.0, ["Lines are perpendicular: angle = 90 degrees"]
    tan_theta = abs((m1 - m2) / denom)
    theta = math.degrees(math.atan(tan_theta))
    steps = [
        f"tan(theta) = |({m1}-{m2})/(1+{m1}*{m2})| = |{m1 - m2}/{denom}| = {tan_theta}",
        f"theta = arctan({tan_theta}) = {theta} degrees",
    ]
    return theta, steps

def point_to_line_distance(px: float, py: float, a: float, b: float, c: float) -> tuple[float, list[str]]:
    """Distance from point (px, py) to line ax+by+c=0."""
    d = abs(a * px + b * py + c) / math.sqrt(a**2 + b**2)
    steps = [f"d = |{a}*{px}+{b}*{py}+{c}| / sqrt({a}^2+{b}^2) = {d}"]
    return d, steps

# ---------------------------------------------------------------------------
# Circle (Analytic Geometry)
# ---------------------------------------------------------------------------

def circle_equation(h: float, k: float, r: float) -> tuple[dict[str, str], list[str]]:
    """Standard and general form of circle equation."""
    standard = f"(x-{h})^2 + (y-{k})^2 = {r**2}"
    D = -2 * h
    E = -2 * k
    F = h**2 + k**2 - r**2
    general = f"x^2 + y^2 + {D}x + {E}y + {F} = 0"
    steps = [
        f"Center ({h}, {k}), radius {r}",
        f"Standard form: {standard}",
        f"General form: {general}",
    ]
    return {"standard": standard, "general": general, "center": [h, k], "radius": r}, steps

def circle_tangent_at_point(h: float, k: float, r: float, px: float, py: float) -> tuple[dict[str, Any], list[str]]:
    """Tangent line to circle at point (px, py) on the circle."""
    steps: list[str] = []
    dist = math.sqrt((px - h)**2 + (py - k)**2)
    if abs(dist - r) > 1e-6:
        steps.append(f"Point ({px},{py}) not on circle (distance to center = {dist}, r = {r}).")
        raise ValueError(f"Point ({px},{py}) is not on the circle.")
    dx = px - h
    dy = py - k
    if abs(dy) < 1e-15:
        steps.append(f"Radius is horizontal, tangent is vertical: x = {px}")
        return {"equation": f"x = {px}", "type": "vertical"}, steps
    slope_radius = dy / dx if abs(dx) > 1e-15 else None
    if slope_radius is None:
        steps.append(f"Radius is vertical, tangent is horizontal: y = {py}")
        return {"equation": f"y = {py}", "slope": 0}, steps
    m_tangent = -dx / dy
    b_tangent = py - m_tangent * px
    steps.append(f"Slope of radius = {slope_radius}")
    steps.append(f"Tangent slope = -1/slope_radius = {m_tangent}")
    steps.append(f"Tangent: y = {m_tangent}x + {b_tangent}")
    return {"slope": m_tangent, "y_intercept": b_tangent, "equation": f"y = {m_tangent}x + {b_tangent}"}, steps

def circle_line_intersection(h: float, k: float, r: float, m: float, b: float) -> tuple[dict[str, Any], list[str]]:
    """Intersection of circle (h,k,r) with line y = mx + b."""
    steps: list[str] = []
    A = 1 + m**2
    B = 2 * (m * (b - k) - h)
    C = h**2 + (b - k)**2 - r**2
    disc = B**2 - 4 * A * C
    steps.append(f"Substitute y=mx+b into circle: {A}x^2 + {B}x + {C} = 0")
    steps.append(f"Discriminant = {disc}")
    if disc < -1e-12:
        steps.append("No intersection (discriminant < 0)")
        return {"count": 0, "points": []}, steps
    if abs(disc) < 1e-12:
        x1 = -B / (2 * A)
        y1 = m * x1 + b
        steps.append(f"Tangent point: ({x1}, {y1})")
        return {"count": 1, "points": [[x1, y1]]}, steps
    sqrt_disc = math.sqrt(disc)
    x1 = (-B + sqrt_disc) / (2 * A)
    x2 = (-B - sqrt_disc) / (2 * A)
    y1 = m * x1 + b
    y2 = m * x2 + b
    steps.append(f"Intersection points: ({x1},{y1}) and ({x2},{y2})")
    return {"count": 2, "points": [[x1, y1], [x2, y2]]}, steps

def arc_length(radius: float, angle_deg: float) -> tuple[float, list[str]]:
    """Arc length given radius and central angle in degrees."""
    angle_rad = math.radians(angle_deg)
    length = radius * angle_rad
    steps = [
        f"Angle in radians = {angle_deg} * pi/180 = {angle_rad}",
        f"Arc length = r * theta = {radius} * {angle_rad} = {length}",
    ]
    return length, steps

def sector_area(radius: float, angle_deg: float) -> tuple[float, list[str]]:
    """Sector area given radius and central angle in degrees."""
    angle_rad = math.radians(angle_deg)
    area = 0.5 * radius**2 * angle_rad
    steps = [
        f"Angle in radians = {angle_rad}",
        f"Sector area = 0.5*r^2*theta = 0.5*{radius}^2*{angle_rad} = {area}",
    ]
    return area, steps

# ---------------------------------------------------------------------------
# Trigonometry
# ---------------------------------------------------------------------------

def trig_functions(angle_deg: float) -> tuple[dict[str, float], list[str]]:
    """All 6 trig functions for a given angle in degrees."""
    rad = math.radians(angle_deg)
    s = math.sin(rad)
    c = math.cos(rad)
    results: dict[str, float] = {"sin": s, "cos": c}
    steps = [f"Angle = {angle_deg} deg = {rad} rad", f"sin = {s}", f"cos = {c}"]
    if abs(c) > 1e-15:
        t = math.tan(rad)
        results["tan"] = t
        steps.append(f"tan = {t}")
    else:
        results["tan"] = float("inf")
        steps.append("tan = undefined (cos=0)")
    if abs(s) > 1e-15:
        results["csc"] = 1.0 / s
        steps.append(f"csc = {1.0 / s}")
    else:
        results["csc"] = float("inf")
        steps.append("csc = undefined (sin=0)")
    if abs(c) > 1e-15:
        results["sec"] = 1.0 / c
        steps.append(f"sec = {1.0 / c}")
    else:
        results["sec"] = float("inf")
        steps.append("sec = undefined (cos=0)")
    if abs(s) > 1e-15 and abs(c) > 1e-15:
        results["cot"] = c / s
        steps.append(f"cot = {c / s}")
    else:
        results["cot"] = float("inf") if abs(s) < 1e-15 else 0.0
        steps.append(f"cot = {results['cot']}")
    return results, steps

def inverse_trig(func: str, value: float) -> tuple[dict[str, float], list[str]]:
    """Inverse trig function: arcsin, arccos, arctan."""
    steps: list[str] = []
    func_lower = func.lower().replace("arc", "a")
    if func_lower in ("asin", "arcsin", "sin"):
        if abs(value) > 1.0:
            raise ValueError(f"arcsin domain error: |{value}| > 1")
        rad = math.asin(value)
    elif func_lower in ("acos", "arccos", "cos"):
        if abs(value) > 1.0:
            raise ValueError(f"arccos domain error: |{value}| > 1")
        rad = math.acos(value)
    elif func_lower in ("atan", "arctan", "tan"):
        rad = math.atan(value)
    else:
        raise ValueError(f"Unknown inverse trig function: {func}")
    deg = math.degrees(rad)
    steps.append(f"{func}({value}) = {rad} rad = {deg} deg")
    return {"radians": rad, "degrees": deg}, steps

def verify_identity(identity_name: str) -> tuple[dict[str, Any], list[str]]:
    """Verify a standard trig identity numerically at multiple angles."""
    identities: dict[str, Any] = {
        "pythagorean": {
            "formula": "sin^2(x) + cos^2(x) = 1",
            "check": lambda x: math.sin(x)**2 + math.cos(x)**2,
            "expected": 1.0,
        },
        "double_angle_sin": {
            "formula": "sin(2x) = 2*sin(x)*cos(x)",
            "check": lambda x: math.sin(2 * x) - 2 * math.sin(x) * math.cos(x),
            "expected": 0.0,
        },
        "double_angle_cos": {
            "formula": "cos(2x) = cos^2(x) - sin^2(x)",
            "check": lambda x: math.cos(2 * x) - (math.cos(x)**2 - math.sin(x)**2),
            "expected": 0.0,
        },
        "tan_identity": {
            "formula": "1 + tan^2(x) = sec^2(x)",
            "check": lambda x: (1 + math.tan(x)**2) - (1 / math.cos(x))**2 if abs(math.cos(x)) > 1e-10 else 0.0,
            "expected": 0.0,
        },
        "sum_sin": {
            "formula": "sin(a+b) = sin(a)cos(b) + cos(a)sin(b)",
            "check": lambda x: math.sin(x + 0.5) - (math.sin(x) * math.cos(0.5) + math.cos(x) * math.sin(0.5)),
            "expected": 0.0,
        },
        "cofunction": {
            "formula": "sin(x) = cos(pi/2 - x)",
            "check": lambda x: math.sin(x) - math.cos(math.pi / 2 - x),
            "expected": 0.0,
        },
    }
    name_lower = identity_name.lower().replace(" ", "_").replace("-", "_")
    if name_lower not in identities:
        available = list(identities.keys())
        raise ValueError(f"Unknown identity '{identity_name}'. Available: {available}")
    ident = identities[name_lower]
    test_angles = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    results_list: list[dict[str, float]] = []
    max_error = 0.0
    steps = [f"Identity: {ident['formula']}", f"Testing at {len(test_angles)} angles..."]
    for angle in test_angles:
        val = ident["check"](angle)
        error = abs(val - ident["expected"])
        max_error = max(max_error, error)
        results_list.append({"angle_rad": angle, "result": val, "error": error})
    verified = max_error < 1e-10
    steps.append(f"Max error = {max_error}")
    steps.append(f"Verified: {verified}")
    return {
        "identity": ident["formula"],
        "verified": verified,
        "max_error": max_error,
        "test_results": results_list,
    }, steps

def law_of_sines(a: Optional[float], A_deg: Optional[float], b: Optional[float], B_deg: Optional[float]) -> tuple[dict[str, Any], list[str]]:
    """Apply law of sines: a/sin(A) = b/sin(B)."""
    steps: list[str] = []
    steps.append("Law of Sines: a/sin(A) = b/sin(B)")
    if a is not None and A_deg is not None:
        ratio = a / math.sin(math.radians(A_deg))
        steps.append(f"Ratio = a/sin(A) = {a}/sin({A_deg}) = {ratio}")
        if b is not None and B_deg is None:
            sin_B = b / ratio
            if abs(sin_B) > 1.0:
                raise ValueError("No solution: sin(B) > 1")
            B_rad = math.asin(sin_B)
            B_deg_calc = math.degrees(B_rad)
            steps.append(f"sin(B) = b/ratio = {b}/{ratio} = {sin_B}")
            steps.append(f"B = arcsin({sin_B}) = {B_deg_calc} deg")
            return {"B_degrees": B_deg_calc, "ratio": ratio, "sin_B": sin_B}, steps
        if B_deg is not None and b is None:
            b_calc = ratio * math.sin(math.radians(B_deg))
            steps.append(f"b = ratio*sin(B) = {ratio}*sin({B_deg}) = {b_calc}")
            return {"b": b_calc, "ratio": ratio}, steps
        return {"ratio": ratio}, steps
    raise ValueError("Insufficient data for law of sines.")

def law_of_cosines(a: float, b: float, C_deg: Optional[float] = None, c: Optional[float] = None) -> tuple[dict[str, Any], list[str]]:
    """Law of cosines: c^2 = a^2 + b^2 - 2ab*cos(C), or find angle C given all sides."""
    steps: list[str] = []
    if C_deg is not None and c is None:
        C_rad = math.radians(C_deg)
        c_sq = a**2 + b**2 - 2 * a * b * math.cos(C_rad)
        c_val = math.sqrt(c_sq)
        steps.append(f"c^2 = {a}^2 + {b}^2 - 2*{a}*{b}*cos({C_deg}) = {c_sq}")
        steps.append(f"c = {c_val}")
        return {"c": c_val}, steps
    if c is not None and C_deg is None:
        cos_C = (a**2 + b**2 - c**2) / (2 * a * b)
        if abs(cos_C) > 1.0:
            raise ValueError("Invalid triangle: cos(C) out of range.")
        C_rad = math.acos(cos_C)
        C_deg_calc = math.degrees(C_rad)
        steps.append(f"cos(C) = ({a}^2+{b}^2-{c}^2)/(2*{a}*{b}) = {cos_C}")
        steps.append(f"C = arccos({cos_C}) = {C_deg_calc} deg")
        return {"C_degrees": C_deg_calc, "cos_C": cos_C}, steps
    raise ValueError("Provide either C_deg or c, not both/neither.")

def solve_triangle(case: str, known: dict[str, float]) -> tuple[dict[str, Any], list[str]]:
    """
    Solve a triangle given a case type:
    SSS: sides a, b, c → angles A, B, C
    SAS: sides a, b and included angle C → side c, angles A, B
    ASA: angles A, B and included side c → side a, b, angle C
    AAS: angles A, B and non-included side a → side b, c, angle C
    SSA: sides a, b and angle A → angle B, side c, angle C (ambiguous case)
    """
    steps: list[str] = []
    case_upper = case.upper()
    steps.append(f"Solving triangle: case={case_upper}, known={known}")

    if case_upper == "SSS":
        a, b, c = known["a"], known["b"], known["c"]
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("Triangle inequality violated.")
        cos_A = (b**2 + c**2 - a**2) / (2 * b * c)
        cos_B = (a**2 + c**2 - b**2) / (2 * a * c)
        A_deg = math.degrees(math.acos(max(-1.0, min(1.0, cos_A))))
        B_deg = math.degrees(math.acos(max(-1.0, min(1.0, cos_B))))
        C_deg = 180.0 - A_deg - B_deg
        steps.append(f"A = arccos(({b}^2+{c}^2-{a}^2)/(2*{b}*{c})) = {A_deg} deg")
        steps.append(f"B = arccos(({a}^2+{c}^2-{b}^2)/(2*{a}*{c})) = {B_deg} deg")
        steps.append(f"C = 180 - A - B = {C_deg} deg")
        area, _ = triangle_area_heron(a, b, c)
        return {"A": A_deg, "B": B_deg, "C": C_deg, "a": a, "b": b, "c": c, "area": area}, steps

    if case_upper == "SAS":
        a, b, C_deg_val = known["a"], known["b"], known["C"]
        C_rad = math.radians(C_deg_val)
        c = math.sqrt(a**2 + b**2 - 2 * a * b * math.cos(C_rad))
        cos_A = (b**2 + c**2 - a**2) / (2 * b * c)
        A_deg = math.degrees(math.acos(max(-1.0, min(1.0, cos_A))))
        B_deg = 180.0 - A_deg - C_deg_val
        steps.append(f"c = sqrt({a}^2+{b}^2-2*{a}*{b}*cos({C_deg_val})) = {c}")
        steps.append(f"A = {A_deg} deg, B = {B_deg} deg")
        area = 0.5 * a * b * math.sin(C_rad)
        return {"A": A_deg, "B": B_deg, "C": C_deg_val, "a": a, "b": b, "c": c, "area": area}, steps

    if case_upper == "ASA":
        A_deg_val, B_deg_val, c = known["A"], known["B"], known["c"]
        C_deg_val = 180.0 - A_deg_val - B_deg_val
        if C_deg_val <= 0:
            raise ValueError("Angles sum > 180.")
        sin_ratio = c / math.sin(math.radians(C_deg_val))
        a = sin_ratio * math.sin(math.radians(A_deg_val))
        b = sin_ratio * math.sin(math.radians(B_deg_val))
        steps.append(f"C = 180 - {A_deg_val} - {B_deg_val} = {C_deg_val} deg")
        steps.append(f"a = c*sin(A)/sin(C) = {a}, b = c*sin(B)/sin(C) = {b}")
        area, _ = triangle_area_heron(a, b, c)
        return {"A": A_deg_val, "B": B_deg_val, "C": C_deg_val, "a": a, "b": b, "c": c, "area": area}, steps

    if case_upper == "AAS":
        A_deg_val, B_deg_val, a = known["A"], known["B"], known["a"]
        C_deg_val = 180.0 - A_deg_val - B_deg_val
        if C_deg_val <= 0:
            raise ValueError("Angles sum > 180.")
        sin_ratio = a / math.sin(math.radians(A_deg_val))
        b = sin_ratio * math.sin(math.radians(B_deg_val))
        c = sin_ratio * math.sin(math.radians(C_deg_val))
        steps.append(f"C = {C_deg_val} deg")
        steps.append(f"b = {b}, c = {c}")
        area, _ = triangle_area_heron(a, b, c)
        return {"A": A_deg_val, "B": B_deg_val, "C": C_deg_val, "a": a, "b": b, "c": c, "area": area}, steps

    if case_upper == "SSA":
        a, b, A_deg_val = known["a"], known["b"], known["A"]
        A_rad = math.radians(A_deg_val)
        sin_B = b * math.sin(A_rad) / a
        if abs(sin_B) > 1.0:
            raise ValueError("No solution: sin(B) > 1.")
        B_rad = math.asin(sin_B)
        B_deg_val = math.degrees(B_rad)
        solutions = []
        for B_candidate in [B_deg_val, 180.0 - B_deg_val]:
            C_candidate = 180.0 - A_deg_val - B_candidate
            if C_candidate <= 0:
                continue
            c = a * math.sin(math.radians(C_candidate)) / math.sin(A_rad)
            solutions.append({"A": A_deg_val, "B": B_candidate, "C": C_candidate, "a": a, "b": b, "c": c})
        steps.append(f"sin(B) = {sin_B}")
        steps.append(f"Possible solutions: {len(solutions)}")
        for i, sol in enumerate(solutions):
            steps.append(f"  Solution {i + 1}: B={sol['B']:.4f}, C={sol['C']:.4f}, c={sol['c']:.4f}")
        return {"solutions": solutions, "ambiguous": len(solutions) > 1}, steps

    raise ValueError(f"Unknown case: {case}. Use SSS, SAS, ASA, AAS, or SSA.")

# ---------------------------------------------------------------------------
# Transformations (2D)
# ---------------------------------------------------------------------------

def rotation_2d(points: list[list[float]], angle_deg: float, center: tuple[float, float] = (0.0, 0.0)) -> tuple[list[list[float]], list[str]]:
    """Rotate points around center by angle_deg degrees CCW."""
    steps: list[str] = []
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    steps.append(f"Rotation by {angle_deg} deg about ({center[0]}, {center[1]})")
    steps.append(f"Matrix: [[{cos_a:.6f}, {-sin_a:.6f}], [{sin_a:.6f}, {cos_a:.6f}]]")
    result: list[list[float]] = []
    for p in points:
        dx = p[0] - center[0]
        dy = p[1] - center[1]
        nx = cos_a * dx - sin_a * dy + center[0]
        ny = sin_a * dx + cos_a * dy + center[1]
        result.append([nx, ny])
        steps.append(f"  ({p[0]},{p[1]}) -> ({nx:.6f},{ny:.6f})")
    return result, steps

def reflection_2d(points: list[list[float]], axis: str = "x") -> tuple[list[list[float]], list[str]]:
    """Reflect points across x-axis, y-axis, or y=x."""
    steps: list[str] = []
    result: list[list[float]] = []
    steps.append(f"Reflection across {axis}-axis")
    for p in points:
        if axis.lower() == "x":
            result.append([p[0], -p[1]])
        elif axis.lower() == "y":
            result.append([-p[0], p[1]])
        elif axis.lower() == "y=x":
            result.append([p[1], p[0]])
        elif axis.lower() == "origin":
            result.append([-p[0], -p[1]])
        else:
            raise ValueError(f"Unknown axis: {axis}. Use x, y, y=x, or origin.")
        steps.append(f"  ({p[0]},{p[1]}) -> ({result[-1][0]},{result[-1][1]})")
    return result, steps

def translation_2d(points: list[list[float]], dx: float, dy: float) -> tuple[list[list[float]], list[str]]:
    """Translate points by (dx, dy)."""
    steps = [f"Translation by ({dx}, {dy})"]
    result: list[list[float]] = []
    for p in points:
        result.append([p[0] + dx, p[1] + dy])
        steps.append(f"  ({p[0]},{p[1]}) -> ({result[-1][0]},{result[-1][1]})")
    return result, steps

def scaling_2d(points: list[list[float]], sx: float, sy: float, center: tuple[float, float] = (0.0, 0.0)) -> tuple[list[list[float]], list[str]]:
    """Scale points by (sx, sy) about center."""
    steps = [f"Scaling by ({sx}, {sy}) about ({center[0]}, {center[1]})"]
    result: list[list[float]] = []
    for p in points:
        nx = center[0] + sx * (p[0] - center[0])
        ny = center[1] + sy * (p[1] - center[1])
        result.append([nx, ny])
        steps.append(f"  ({p[0]},{p[1]}) -> ({nx},{ny})")
    return result, steps

def compose_transforms_2d(points: list[list[float]], transforms: list[dict[str, Any]]) -> tuple[list[list[float]], list[str]]:
    """Apply a sequence of 2D transforms in order."""
    steps: list[str] = []
    current = [list(p) for p in points]
    for i, t in enumerate(transforms):
        op = t.get("type", "").lower()
        steps.append(f"--- Transform {i + 1}: {op} ---")
        if op == "rotation":
            current, s = rotation_2d(current, t.get("angle", 0), tuple(t.get("center", [0, 0])))
        elif op == "reflection":
            current, s = reflection_2d(current, t.get("axis", "x"))
        elif op == "translation":
            current, s = translation_2d(current, t.get("dx", 0), t.get("dy", 0))
        elif op == "scaling":
            current, s = scaling_2d(current, t.get("sx", 1), t.get("sy", 1), tuple(t.get("center", [0, 0])))
        else:
            s = [f"Unknown transform type: {op}"]
        steps.extend(s)
    return current, steps

# ---------------------------------------------------------------------------
# Computational Geometry
# ---------------------------------------------------------------------------

def _cross(o: list[float], a: list[float], b: list[float]) -> float:
    """Cross product of vectors OA and OB."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def convex_hull_graham(points: list[list[float]]) -> tuple[list[list[float]], list[str]]:
    """Convex hull via Graham scan (Andrew's monotone chain variant)."""
    steps: list[str] = []
    pts = sorted(points, key=lambda p: (p[0], p[1]))
    if len(pts) <= 1:
        return pts, ["Trivial hull (0 or 1 points)."]
    steps.append(f"Sorted {len(pts)} points by x, then y")
    lower: list[list[float]] = []
    for p in pts:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list[list[float]] = []
    for p in reversed(pts):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    hull = lower[:-1] + upper[:-1]
    steps.append(f"Lower hull: {len(lower) - 1} points")
    steps.append(f"Upper hull: {len(upper) - 1} points")
    steps.append(f"Total hull vertices: {len(hull)}")
    return hull, steps

def point_in_polygon_raycast(point: list[float], polygon: list[list[float]]) -> tuple[bool, list[str]]:
    """Ray casting algorithm for point-in-polygon test."""
    steps: list[str] = []
    x, y = point[0], point[1]
    n = len(polygon)
    inside = False
    j = n - 1
    crossings = 0
    for i in range(n):
        xi, yi = polygon[i][0], polygon[i][1]
        xj, yj = polygon[j][0], polygon[j][1]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
            crossings += 1
        j = i
    steps.append(f"Point ({x},{y}), polygon with {n} vertices")
    steps.append(f"Ray crossings: {crossings}")
    steps.append(f"Inside: {inside}")
    return inside, steps

def line_segment_intersection(p1: list[float], p2: list[float], p3: list[float], p4: list[float]) -> tuple[Optional[list[float]], list[str]]:
    """Find intersection point of segments p1-p2 and p3-p4, if it exists."""
    steps: list[str] = []
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    x3, y3 = p3[0], p3[1]
    x4, y4 = p4[0], p4[1]
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    steps.append(f"Segment 1: ({x1},{y1})-({x2},{y2})")
    steps.append(f"Segment 2: ({x3},{y3})-({x4},{y4})")
    if abs(denom) < 1e-15:
        steps.append("Segments are parallel or coincident (denom ~ 0)")
        return None, steps
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
    steps.append(f"t = {t}, u = {u}")
    if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
        ix = x1 + t * (x2 - x1)
        iy = y1 + t * (y2 - y1)
        steps.append(f"Intersection at ({ix}, {iy})")
        return [ix, iy], steps
    steps.append("No intersection within segment bounds")
    return None, steps

def polygon_area_shoelace(vertices: list[list[float]]) -> tuple[float, list[str]]:
    """Polygon area via shoelace formula."""
    steps: list[str] = []
    n = len(vertices)
    if n < 3:
        raise ValueError("Need at least 3 vertices for a polygon.")
    total = 0.0
    for i in range(n):
        j = (i + 1) % n
        total += vertices[i][0] * vertices[j][1]
        total -= vertices[j][0] * vertices[i][1]
    area = abs(total) / 2.0
    steps.append(f"Shoelace on {n} vertices")
    steps.append(f"Sum of cross terms = {total}")
    steps.append(f"Area = |{total}|/2 = {area}")
    return area, steps

def polygon_perimeter(vertices: list[list[float]]) -> tuple[float, list[str]]:
    """Perimeter of polygon."""
    n = len(vertices)
    total = 0.0
    steps: list[str] = []
    for i in range(n):
        j = (i + 1) % n
        d = math.sqrt((vertices[j][0] - vertices[i][0])**2 + (vertices[j][1] - vertices[i][1])**2)
        total += d
    steps.append(f"Perimeter of {n}-gon = {total}")
    return total, steps

# ---------------------------------------------------------------------------
# Dispatch maps for structured API
# ---------------------------------------------------------------------------

SHAPE_2D_DISPATCH: dict[str, Any] = {
    "triangle_heron": lambda p: triangle_area_heron(p["a"], p["b"], p["c"]),
    "triangle_cross": lambda p: triangle_area_cross(p["x1"], p["y1"], p["x2"], p["y2"], p["x3"], p["y3"]),
    "triangle_centroid": lambda p: triangle_centroid(p["x1"], p["y1"], p["x2"], p["y2"], p["x3"], p["y3"]),
    "triangle_incircle": lambda p: triangle_incircle(p["a"], p["b"], p["c"]),
    "triangle_circumcircle": lambda p: triangle_circumcircle(p["a"], p["b"], p["c"]),
    "rectangle": lambda p: rectangle_props(p["length"], p["width"]),
    "circle": lambda p: circle_props(p["radius"]),
    "ellipse": lambda p: ellipse_props(p["a"], p["b"]),
    "regular_polygon": lambda p: regular_polygon_props(int(p["n"]), p["side"]),
    "trapezoid": lambda p: trapezoid_props(p["a"], p["b"], p["h"]),
    "parallelogram": lambda p: parallelogram_props(p["base"], p["height"], p["side"], p["angle"]),
}

SHAPE_3D_DISPATCH: dict[str, Any] = {
    "sphere": lambda p: sphere_props(p["radius"]),
    "cylinder": lambda p: cylinder_props(p["radius"], p["height"]),
    "cone": lambda p: cone_props(p["radius"], p["height"]),
    "prism": lambda p: prism_props(p["base_area"], p["base_perimeter"], p["height"]),
    "pyramid": lambda p: pyramid_props(p["base_area"], p["base_perimeter"], p["height"], p["slant_height"]),
    "torus": lambda p: torus_props(p["major_r"], p["minor_r"]),
}

COORD_DISPATCH: dict[str, Any] = {
    "distance": lambda pts, _: distance_2d(pts[0][0], pts[0][1], pts[1][0], pts[1][1]),
    "midpoint": lambda pts, _: midpoint_2d(pts[0][0], pts[0][1], pts[1][0], pts[1][1]),
    "slope": lambda pts, _: slope_2d(pts[0][0], pts[0][1], pts[1][0], pts[1][1]),
    "line_equation": lambda pts, _: line_equation_two_points(pts[0][0], pts[0][1], pts[1][0], pts[1][1]),
    "line_from_point_slope": lambda pts, par: line_equation_point_slope(pts[0][0], pts[0][1], par["m"]),
    "perpendicular_slope": lambda pts, par: perpendicular_slope(par["m"]),
    "angle_between_lines": lambda pts, par: angle_between_lines(par["m1"], par["m2"]),
    "point_to_line": lambda pts, par: point_to_line_distance(pts[0][0], pts[0][1], par["a"], par["b"], par["c"]),
}

TRIG_DISPATCH: dict[str, Any] = {
    "trig_functions": lambda p: trig_functions(p["angle"]),
    "inverse_trig": lambda p: inverse_trig(p["func"], p["value"]),
    "verify_identity": lambda p: verify_identity(p["identity"]),
    "law_of_sines": lambda p: law_of_sines(p.get("a"), p.get("A"), p.get("b"), p.get("B")),
    "law_of_cosines": lambda p: law_of_cosines(p["a"], p["b"], p.get("C"), p.get("c")),
}

TRANSFORM_DISPATCH: dict[str, Any] = {
    "rotation": lambda pts, par: rotation_2d(pts, par.get("angle", 0), tuple(par.get("center", [0, 0]))),
    "reflection": lambda pts, par: reflection_2d(pts, par.get("axis", "x")),
    "translation": lambda pts, par: translation_2d(pts, par.get("dx", 0), par.get("dy", 0)),
    "scaling": lambda pts, par: scaling_2d(pts, par.get("sx", 1), par.get("sy", 1), tuple(par.get("center", [0, 0]))),
}

COMPGEO_DISPATCH: dict[str, Any] = {
    "convex_hull": lambda pts, _: convex_hull_graham(pts),
    "point_in_polygon": lambda pts, par: point_in_polygon_raycast(par["point"], pts),
    "line_intersection": lambda pts, _: line_segment_intersection(pts[0], pts[1], pts[2], pts[3]),
    "polygon_area": lambda pts, _: polygon_area_shoelace(pts),
    "polygon_perimeter": lambda pts, _: polygon_perimeter(pts),
}

# ---------------------------------------------------------------------------
# TIE-20: Deep Analysis Mode
# ---------------------------------------------------------------------------

def deep_analysis(query: str) -> tuple[dict[str, Any], list[str]]:
    """Multi-source synthesis for complex geometry queries."""
    steps: list[str] = []
    categories = classify_issue(query)
    steps.append(f"Issue categories: {[c.value for c in categories]}")
    doctrine = doctrine_lookup(query)
    if doctrine:
        steps.append(f"Doctrine match: {doctrine.get('topic', 'unknown')}")
    authorities = resolve_authority(query)
    steps.append(f"Authorities: {authorities}")
    fragility = fact_fragility_score(query)
    steps.append(f"Fragility: {fragility}")
    return {
        "categories": [c.value for c in categories],
        "doctrine_match": doctrine.get("topic") if doctrine else None,
        "doctrine_content": doctrine.get("conclusion_template") if doctrine else None,
        "authorities": authorities,
        "fragility": fragility,
        "reasoning": "Deep analysis synthesizes doctrine cache, authority hierarchy, and domain-specific computation.",
    }, steps

# ---------------------------------------------------------------------------
# TIE-1: Three-Layer Response Orchestrator
# ---------------------------------------------------------------------------

def three_layer_response(query: str, mode: ResponseMode, zone: AnalysisZone, show_steps: bool) -> EngineResponse:
    """Route query through doctrine cache -> semantic -> deep analysis."""
    t0 = time.time()
    query_id = str(uuid.uuid4())
    all_steps: list[str] = []
    layer_used = ResponseLayer.DOCTRINE_CACHE
    normalized = normalize_term(query)
    all_steps.append(f"Normalized query: {normalized}")
    categories = classify_issue(query)
    for cat in categories:
        record_coverage_hit(cat.value)

    # Layer 1: Doctrine cache
    doctrine = doctrine_lookup(query)
    if doctrine:
        layer_used = ResponseLayer.DOCTRINE_CACHE
        result = {
            "topic": doctrine["topic"],
            "conclusion": doctrine["conclusion_template"],
            "reasoning": doctrine.get("reasoning_framework", ""),
            "key_factors": doctrine.get("key_factors", []),
            "authorities": doctrine.get("primary_authority", []),
        }
        all_steps.append("Doctrine cache HIT")
        latency = (time.time() - t0) * 1000
        METRICS.record_query(latency, True)
    else:
        all_steps.append("Doctrine cache MISS — falling through to deep analysis")
        layer_used = ResponseLayer.DEEP_ANALYSIS
        result, deep_steps = deep_analysis(query)
        all_steps.extend(deep_steps)
        latency = (time.time() - t0) * 1000
        METRICS.record_query(latency, False)

    # Mode formatting
    if mode == ResponseMode.FAST:
        if isinstance(result, dict) and "conclusion" in result:
            result = {"answer": result["conclusion"]}
    elif mode == ResponseMode.DEFENSE:
        result["zone"] = zone.value
        result["fragility"] = fact_fragility_score(result)
    elif mode == ResponseMode.MEMO:
        result["full_memo"] = True
        result["authorities"] = resolve_authority(query)

    d_hash = determinism_hash(result)
    authorities = resolve_authority(query)

    response = EngineResponse(
        query_id=query_id,
        layer=layer_used.value,
        mode=mode.value,
        zone=zone.value,
        result=result,
        steps=all_steps if show_steps else [],
        confidence=ConfidenceLevel.DEFENSIBLE.value,
        confidence_score=0.98,
        authorities=authorities,
        determinism_hash=d_hash,
        latency_ms=round(latency, 2),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    # Telemetry
    record_telemetry(TelemetryRecord(
        query_id=query_id,
        timestamp=response.timestamp,
        layer=layer_used.value,
        latency_ms=response.latency_ms,
        cache_hit=(layer_used == ResponseLayer.DOCTRINE_CACHE),
    ))
    # Audit
    write_audit({"query_id": query_id, "query": query, "layer": layer_used.value, "mode": mode.value})

    return response

# ═══════════════════════════════════════════════════════════════════════════
# FastAPI Application — TIE-17
# ═══════════════════════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI):
    global DOCTRINE_CACHE, SEMANTIC_DICT, COVERAGE_MAP
    logger.info("MATH10 Geometry Engine starting on port {}", ENGINE_PORT)
    DOCTRINE_CACHE = _load_doctrine_cache()
    SEMANTIC_DICT = _load_semantic_dict()
    COVERAGE_MAP = _load_coverage_map()
    for entry in DOCTRINE_CACHE:
        DRIFT.set_baseline(entry.get("topic", ""), json.dumps(entry, sort_keys=True))
    logger.info("MATH10 ready — {} doctrines, {} semantic terms", len(DOCTRINE_CACHE), len(SEMANTIC_DICT))
    yield
    logger.info("MATH10 shutting down")

app = FastAPI(
    title=ENGINE_NAME,
    version=ENGINE_VERSION,
    description="TIE-20 compliant geometry intelligence engine",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TIE-12: Health Endpoint
@app.get("/health")
async def health() -> dict[str, Any]:
    return {
        "engine_id": ENGINE_ID,
        "name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "status": "healthy",
        "port": ENGINE_PORT,
        "tier": ENGINE_TIER,
        "mode": ENGINE_MODE,
        "auth_level": ENGINE_AUTH,
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "semantic_terms": len(SEMANTIC_DICT),
        "coverage_domains": len(COVERAGE_MAP.get("domains", [])),
        "uptime_seconds": round(time.time() - METRICS.start_time, 1),
        "metrics": METRICS.summary(),
        "drift_events": len(DRIFT.report()),
        "telemetry_records": len(TELEMETRY_LOG),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

# TIE-1: Natural language query
@app.post("/query", response_model=EngineResponse)
async def query_endpoint(req: GeometryQuery) -> EngineResponse:
    try:
        return three_layer_response(req.query, req.mode, req.zone, req.show_steps)
    except Exception as exc:
        METRICS.record_error()
        logger.error("Query error: {}", exc)
        raise HTTPException(status_code=400, detail=str(exc))

# 2D Shapes
@app.post("/shapes/2d")
async def shapes_2d(req: ShapeAreaRequest) -> dict[str, Any]:
    t0 = time.time()
    shape = req.shape.lower().replace(" ", "_")
    if shape not in SHAPE_2D_DISPATCH:
        raise HTTPException(status_code=400, detail=f"Unknown 2D shape: {shape}. Available: {list(SHAPE_2D_DISPATCH.keys())}")
    try:
        result, steps = SHAPE_2D_DISPATCH[shape](req.params)
        record_coverage_hit("EUCLIDEAN_2D")
        latency = (time.time() - t0) * 1000
        METRICS.record_query(latency, False)
        return {"shape": shape, "result": result, "steps": steps, "determinism_hash": determinism_hash(result), "latency_ms": round(latency, 2)}
    except Exception as exc:
        METRICS.record_error()
        raise HTTPException(status_code=400, detail=str(exc))

# 3D Solids
@app.post("/shapes/3d")
async def shapes_3d(req: Solid3DRequest) -> dict[str, Any]:
    t0 = time.time()
    shape = req.shape.lower().replace(" ", "_")
    if shape not in SHAPE_3D_DISPATCH:
        raise HTTPException(status_code=400, detail=f"Unknown 3D shape: {shape}. Available: {list(SHAPE_3D_DISPATCH.keys())}")
    try:
        result, steps = SHAPE_3D_DISPATCH[shape](req.params)
        record_coverage_hit("EUCLIDEAN_3D")
        latency = (time.time() - t0) * 1000
        METRICS.record_query(latency, False)
        return {"shape": shape, "result": result, "steps": steps, "determinism_hash": determinism_hash(result), "latency_ms": round(latency, 2)}
    except Exception as exc:
        METRICS.record_error()
        raise HTTPException(status_code=400, detail=str(exc))

# Coordinate Geometry
@app.post("/coordinate")
async def coordinate_endpoint(req: CoordinateRequest) -> dict[str, Any]:
    t0 = time.time()
    op = req.operation.lower().replace(" ", "_")
    if op not in COORD_DISPATCH:
        raise HTTPException(status_code=400, detail=f"Unknown coordinate operation: {op}. Available: {list(COORD_DISPATCH.keys())}")
    try:
        result, steps = COORD_DISPATCH[op](req.points, req.params or {})
        record_coverage_hit("COORDINATE")
        latency = (time.time() - t0) * 1000
        METRICS.record_query(latency, False)
        return {"operation": op, "result": result, "steps": steps, "determinism_hash": determinism_hash(result), "latency_ms": round(latency, 2)}
    except Exception as exc:
        METRICS.record_error()
        raise HTTPException(status_code=400, detail=str(exc))

# Trigonometry
@app.post("/trig")
async def trig_endpoint(req: TrigRequest) -> dict[str, Any]:
    t0 = time.time()
    op = req.operation.lower().replace(" ", "_")
    if op not in TRIG_DISPATCH:
        raise HTTPException(status_code=400, detail=f"Unknown trig operation: {op}. Available: {list(TRIG_DISPATCH.keys())}")
    try:
        result, steps = TRIG_DISPATCH[op](req.params)
        record_coverage_hit("TRIGONOMETRY")
        latency = (time.time() - t0) * 1000
        METRICS.record_query(latency, False)
        return {"operation": op, "result": result, "steps": steps, "determinism_hash": determinism_hash(result), "latency_ms": round(latency, 2)}
    except Exception as exc:
        METRICS.record_error()
        raise HTTPException(status_code=400, detail=str(exc))

# Triangle Solver
@app.post("/triangle/solve")
async def triangle_solve(req: TriangleSolveRequest) -> dict[str, Any]:
    t0 = time.time()
    try:
        result, steps = solve_triangle(req.case, req.known)
        record_coverage_hit("TRIGONOMETRY")
        latency = (time.time() - t0) * 1000
        METRICS.record_query(latency, False)
        return {"case": req.case, "result": result, "steps": steps, "determinism_hash": determinism_hash(result), "latency_ms": round(latency, 2)}
    except Exception as exc:
        METRICS.record_error()
        raise HTTPException(status_code=400, detail=str(exc))

# Transformations
@app.post("/transform")
async def transform_endpoint(req: TransformRequest) -> dict[str, Any]:
    t0 = time.time()
    op = req.operation.lower().replace(" ", "_")
    if op not in TRANSFORM_DISPATCH:
        raise HTTPException(status_code=400, detail=f"Unknown transform: {op}. Available: {list(TRANSFORM_DISPATCH.keys())}")
    try:
        result, steps = TRANSFORM_DISPATCH[op](req.points, req.params)
        record_coverage_hit("TRANSFORMATIONS")
        latency = (time.time() - t0) * 1000
        METRICS.record_query(latency, False)
        return {"operation": op, "result": result, "steps": steps, "determinism_hash": determinism_hash(result), "latency_ms": round(latency, 2)}
    except Exception as exc:
        METRICS.record_error()
        raise HTTPException(status_code=400, detail=str(exc))

# Computational Geometry
@app.post("/compgeo")
async def compgeo_endpoint(req: CompGeoRequest) -> dict[str, Any]:
    t0 = time.time()
    op = req.operation.lower().replace(" ", "_")
    if op not in COMPGEO_DISPATCH:
        raise HTTPException(status_code=400, detail=f"Unknown compgeo operation: {op}. Available: {list(COMPGEO_DISPATCH.keys())}")
    try:
        result, steps = COMPGEO_DISPATCH[op](req.points, req.params or {})
        record_coverage_hit("COMPUTATIONAL")
        latency = (time.time() - t0) * 1000
        METRICS.record_query(latency, False)
        return {"operation": op, "result": result, "steps": steps, "determinism_hash": determinism_hash(result), "latency_ms": round(latency, 2)}
    except Exception as exc:
        METRICS.record_error()
        raise HTTPException(status_code=400, detail=str(exc))

# Circle analytics
@app.post("/circle/equation")
async def circle_eq_endpoint(h: float = Query(...), k: float = Query(...), r: float = Query(...)) -> dict[str, Any]:
    result, steps = circle_equation(h, k, r)
    return {"result": result, "steps": steps}

@app.post("/circle/tangent")
async def circle_tangent_endpoint(h: float = Query(...), k: float = Query(...), r: float = Query(...), px: float = Query(...), py: float = Query(...)) -> dict[str, Any]:
    try:
        result, steps = circle_tangent_at_point(h, k, r, px, py)
        return {"result": result, "steps": steps}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.post("/circle/line_intersection")
async def circle_line_int_endpoint(h: float = Query(...), k: float = Query(...), r: float = Query(...), m: float = Query(...), b: float = Query(...)) -> dict[str, Any]:
    result, steps = circle_line_intersection(h, k, r, m, b)
    return {"result": result, "steps": steps}

@app.post("/circle/arc_length")
async def arc_length_endpoint(radius: float = Query(...), angle_deg: float = Query(...)) -> dict[str, Any]:
    result, steps = arc_length(radius, angle_deg)
    return {"result": result, "steps": steps}

@app.post("/circle/sector_area")
async def sector_area_endpoint(radius: float = Query(...), angle_deg: float = Query(...)) -> dict[str, Any]:
    result, steps = sector_area(radius, angle_deg)
    return {"result": result, "steps": steps}

# Metrics
@app.get("/metrics")
async def metrics_endpoint() -> dict[str, Any]:
    return {
        "engine_id": ENGINE_ID,
        "metrics": METRICS.summary(),
        "coverage_hits": COVERAGE_HITS,
        "drift_events": DRIFT.report(),
        "telemetry_count": len(TELEMETRY_LOG),
    }

# Telemetry
@app.get("/telemetry")
async def telemetry_endpoint(limit: int = Query(default=100)) -> dict[str, Any]:
    return {"records": TELEMETRY_LOG[-limit:], "total": len(TELEMETRY_LOG)}

# Drift
@app.get("/drift")
async def drift_endpoint() -> dict[str, Any]:
    return {"drift_events": DRIFT.report(), "baseline_count": len(DRIFT.baseline_hashes)}

# Coverage
@app.get("/coverage")
async def coverage_endpoint() -> dict[str, Any]:
    return {
        "map": COVERAGE_MAP,
        "hits": COVERAGE_HITS,
        "uncovered": [d for d in COVERAGE_MAP.get("domains", []) if d not in COVERAGE_HITS],
    }

# Doctrines
@app.get("/doctrines")
async def doctrines_endpoint() -> dict[str, Any]:
    return {"count": len(DOCTRINE_CACHE), "topics": [d.get("topic", "") for d in DOCTRINE_CACHE]}

# Compose transforms
@app.post("/transform/compose")
async def compose_transforms(points: list[list[float]], transforms: list[dict[str, Any]]) -> dict[str, Any]:
    t0 = time.time()
    try:
        result, steps = compose_transforms_2d(points, transforms)
        latency = (time.time() - t0) * 1000
        return {"result": result, "steps": steps, "latency_ms": round(latency, 2)}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

# ═══════════════════════════════════════════════════════════════════════════
# Entrypoint
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info("Launching MATH10 Geometry Engine on port {}", ENGINE_PORT)
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT, log_level="info")
