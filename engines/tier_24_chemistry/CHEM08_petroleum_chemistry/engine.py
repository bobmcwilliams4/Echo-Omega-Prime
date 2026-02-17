import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from loguru import logger
import hashlib
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple, Set, Callable
from enum import Enum, auto
from datetime import datetime, timedelta
import json
import threading

# ================= ENUMS ===================

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class PositionZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class ConfidenceZone(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class IssueCategory(str, Enum):
    CRUDE_OIL_CHARACTERIZATION = "Crude Oil Characterization"
    DISTILLATION = "Distillation"
    PETROLEUM_FRACTIONS = "Petroleum Fractions"
    HYDROCARBON_CLASSES = "Hydrocarbon Classes"
    REFINING_PROCESSES = "Refining Processes"
    PETROCHEMICAL_FEEDSTOCKS = "Petrochemical Feedstocks"
    PRODUCT_SPECIFICATIONS = "Product Specifications"
    FUEL_PROPERTIES = "Fuel Properties"
    LUBRICANT_BASE_OILS = "Lubricant Base Oils"
    NATURAL_GAS_PROCESSING = "Natural Gas Processing"
    ASPHALTENE_BEHAVIOR = "Asphaltene Behavior"
    CATALYTIC_PROCESSES = "Catalytic Processes"
    HYDROPROCESSING = "Hydroprocessing"
    COKING = "Coking"
    ISOMERIZATION = "Isomerization"
    ALKYLATION = "Alkylation"
    OTHERS = "Others"

# ================= METRICS COLLECTOR ===================

class MetricsCollector:
    def __init__(self):
        self.queries: List[Dict[str, Any]] = []
        self.errors: List[Dict[str, Any]] = []
        self.lock = threading.Lock()
        self.doctrine_hits: Dict[str, int] = {}
        self.query_times: List[float] = []

    def record_query(self, doctrine_ids: List[str], latency: float):
        with self.lock:
            self.queries.append({"time": datetime.utcnow(), "doctrines": doctrine_ids, "latency": latency})
            for d in doctrine_ids:
                self.doctrine_hits[d] = self.doctrine_hits.get(d, 0) + 1
            self.query_times.append(latency)

    def record_error(self, error: str):
        with self.lock:
            self.errors.append({"time": datetime.utcnow(), "error": error})

    def get_latency_stats(self) -> Dict[str, float]:
        with self.lock:
            if not self.query_times:
                return {"avg": 0.0, "max": 0.0, "min": 0.0}
            return {
                "avg": sum(self.query_times) / len(self.query_times),
                "max": max(self.query_times),
                "min": min(self.query_times)
            }

    def get_doctrine_hit_rate(self) -> Dict[str, int]:
        with self.lock:
            return dict(self.doctrine_hits)

    def queries_last_hour(self) -> int:
        cutoff = datetime.utcnow() - timedelta(hours=1)
        with self.lock:
            return sum(1 for q in self.queries if q["time"] > cutoff)

metrics_collector = MetricsCollector()

# ================= PYDANTIC MODELS ===================

class QueryRequest(BaseModel):
    scenario: str = Field(..., description="Petroleum chemistry scenario or question")
    mode: ResponseMode = Field(..., description="Response mode")
    entity_type: str = Field(..., description="Entity type (e.g., refinery, lab, product)")
    complexity: int = Field(..., ge=1, le=5, description="Complexity level (1-5)")

class QueryResponse(BaseModel):
    engine_id: str
    query_id: str
    mode: ResponseMode
    confidence: float
    confidence_zone: ConfidenceZone
    position_zone: PositionZone
    primary_conclusion: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    counter_arguments: List[str]
    resolution_strategy: str
    determinism_hash: str

# ================= DOCTRINE CACHE ===================

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: Callable[[Dict[str, Any]], str]
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: float
    confidence_zone: ConfidenceZone
    controlling_precedent: List[str]
    issue_category: IssueCategory

# ================= SEMANTIC NORMALIZATION ===================

SEMANTIC_NORMALIZATION = {
    "SARA": "Saturates, Aromatics, Resins, Asphaltenes",
    "API": "American Petroleum Institute Gravity",
    "TBP": "True Boiling Point",
    "FCC": "Fluid Catalytic Cracking",
    "HDS": "Hydrodesulfurization",
    "HDN": "Hydrodenitrogenation",
    "HDM": "Hydrodemetallization",
    "BTX": "Benzene, Toluene, Xylene",
    "NGL": "Natural Gas Liquids",
    "RVP": "Reid Vapor Pressure",
    "RON": "Research Octane Number",
    "MON": "Motor Octane Number",
    "AKI": "Anti-Knock Index",
    "TAN": "Total Acid Number",
    "VGO": "Vacuum Gas Oil",
    "ASTM D86": "Standard Test Method for Distillation of Petroleum Products at Atmospheric Pressure",
    "ASTM D1160": "Standard Test Method for Distillation of Petroleum Products at Reduced Pressure",
    "ASTM D2892": "Standard Test Method for Distillation of Crude Oil",
    "Pour Point": "Lowest temperature at which oil will flow",
    "Flash Point": "Lowest temperature at which vapors ignite",
    "Cetane Number": "Ignition quality of diesel fuel",
    "Group I": "Solvent-refined base oils",
    "Group II": "Hydroprocessed base oils",
    "Group III": "Severely hydrocracked base oils",
    "Group IV": "Polyalphaolefin base oils",
    "Group V": "All other base oils",
    "Conradson Carbon Residue": "Carbon residue left after evaporation and pyrolysis",
    "Platforming": "Catalytic reforming process",
    "Isomerization": "Conversion of n-paraffins to iso-paraffins",
    "Delayed Coking": "Thermal cracking process for residuum",
    "Hydrocracking": "Catalytic cracking in presence of hydrogen",
    "Alkylation": "Combining isobutane and olefins to produce alkylate",
    "Naphtha": "Light petroleum fraction boiling up to ~200°C",
    "Kerosene": "Petroleum fraction boiling ~150-275°C",
    "Diesel": "Petroleum fraction boiling ~250-350°C",
    "Residuum": "Bottom product of distillation",
    "Paraffin": "Alkane hydrocarbons",
    "Naphthene": "Cycloalkane hydrocarbons",
    "Aromatic": "Aromatic ring hydrocarbons",
    "Olefin": "Alkene hydrocarbons",
    "Asphaltene": "High molecular weight, polar fraction of crude",
    "Hydrotreating": "Catalytic removal of impurities",
    "Fractionation": "Separation of components by boiling point",
    "Colloidal Stability": "Ability of asphaltenes to remain dispersed",
    "Onset Precipitation": "Point at which asphaltenes begin to precipitate",
    "Flocculation": "Aggregation of asphaltene particles",
    "Petrochemical Feedstock": "Raw material for petrochemical production",
    "Vacuum Distillation": "Distillation under reduced pressure",
    "Atmospheric Distillation": "Distillation at atmospheric pressure"
}

def semantic_normalize(term: str) -> str:
    return SEMANTIC_NORMALIZATION.get(term, term)

# ================= EPISTEMIC GUARDRAILS ===================

BANNED_PHRASES = [
    "always", "never", "cannot be wrong", "guaranteed", "no exceptions", "perfectly", "absolutely certain",
    "proven beyond doubt", "undisputed", "infallible", "irrefutable", "without risk", "flawless", "impossible to fail"
]

def apply_epistemic_guardrails(text: str) -> str:
    for phrase in BANNED_PHRASES:
        text = text.replace(phrase, "[epistemic caution]")
    return text

# ================= FACT FRAGILITY SCORING ===================

def score_fact_fragility(fact: str) -> Dict[str, float]:
    # Heuristic: longer, more technical, more references = less fragile
    verifiability = min(1.0, 0.5 + 0.05 * fact.count("ASTM") + 0.05 * fact.count("API"))
    recharacterization_risk = max(0.0, 0.5 - 0.05 * fact.count("measured") - 0.03 * fact.count("analyzed"))
    testimony_dependence = 0.3 if "reported" in fact or "claimed" in fact else 0.1
    return {
        "verifiability": round(verifiability, 2),
        "recharacterization_risk": round(recharacterization_risk, 2),
        "testimony_dependence": round(testimony_dependence, 2)
    }

# ================= AUTHORITY HARDENING ===================

AUTHORITY_WEIGHTS = {
    "ASTM": 1.0,
    "API": 0.95,
    "UOP": 0.9,
    "IP": 0.85,
    "ISO": 0.8,
    "Energy Institute": 0.75,
    "SPE": 0.7,
    "Peer-reviewed": 0.6,
    "Industry Practice": 0.5
}

def authority_hardening(authorities: List[str]) -> List[Tuple[str, float]]:
    weighted = []
    for auth in authorities:
        for key, weight in AUTHORITY_WEIGHTS.items():
            if key in auth:
                weighted.append((auth, weight))
                break
        else:
            weighted.append((auth, 0.4))
    weighted.sort(key=lambda x: -x[1])
    return weighted

def resolve_authority_conflict(auths1: List[str], auths2: List[str]) -> List[str]:
    w1 = authority_hardening(auths1)
    w2 = authority_hardening(auths2)
    all_auths = {a for a, _ in w1 + w2}
    ranked = sorted(all_auths, key=lambda a: -max([w for auth, w in w1 + w2 if auth == a]))
    return ranked

# ================= DOCTRINE BLOCKS ===================

def rf_crude_oil_sara(context: Dict[str, Any]) -> str:
    """
    SARA analysis divides crude oil into saturates, aromatics, resins, and asphaltenes.
    The SARA fractions are determined by chromatographic separation, typically using ASTM D2007 or D6560.
    Saturates are nonpolar alkanes and cycloalkanes, aromatics contain one or more aromatic rings, resins are polar molecules with heteroatoms, and asphaltenes are high molecular weight, polar, insoluble in n-heptane.
    SARA composition affects crude stability, fouling tendency, and asphaltene precipitation risk.
    High asphaltene and resin content increases fouling and sludge formation in refining.
    SARA is foundational for predicting crude compatibility and blending behavior.
    The method's accuracy depends on solvent selection and sample handling.
    SARA is referenced in ASTM D2007, D6560, and IP 143.
    """
    return (
        "SARA analysis (Saturates, Aromatics, Resins, Asphaltenes) is a chromatographic method "
        "for characterizing crude oil composition. It informs on fouling, stability, and asphaltene precipitation. "
        "Results guide blending and refining strategies, with method accuracy depending on solvent and protocol. "
        "See ASTM D2007, D6560, and IP 143 for standardized procedures."
    )

def rf_crude_oil_api_gravity(context: Dict[str, Any]) -> str:
    """
    API gravity is a measure of crude oil density relative to water, calculated as API = (141.5/SG) - 131.5.
    It is determined using ASTM D287 or D1298.
    Higher API indicates lighter crude, which is generally more valuable due to higher yields of light products.
    API gravity influences refinery configuration, product slate, and process selection.
    Blending crudes with different APIs can optimize feedstock properties.
    API gravity is a key parameter in refinery economics and product pricing.
    """
    return (
        "API gravity quantifies crude oil density and is central to valuation and processing decisions. "
        "Measured by ASTM D287/D1298, it guides blending, refinery configuration, and product yield forecasts. "
        "Higher API crudes are lighter and more valuable. "
        "See API MPMS Ch. 9.1 and ASTM D287 for methods."
    )

def rf_crude_oil_sulfur_content(context: Dict[str, Any]) -> str:
    """
    Sulfur content in crude oil is measured by ASTM D4294, D2622, or D5453.
    High sulfur crudes require more intensive hydrotreating and produce more SOx emissions.
    Sulfur affects catalyst life, product quality, and environmental compliance.
    Refineries may pay less for high-sulfur ('sour') crudes.
    Sulfur speciation (H2S, mercaptans, thiophenes) impacts processing strategies.
    """
    return (
        "Sulfur content, measured by ASTM D4294/D2622/D5453, is a critical crude property impacting processing, "
        "catalyst life, and environmental compliance. High sulfur ('sour') crudes are less valuable and require "
        "more hydrotreating. Sulfur speciation further influences refinery strategies."
    )

def rf_crude_oil_tan(context: Dict[str, Any]) -> str:
    """
    TAN (Total Acid Number) quantifies acidic compounds in crude, measured by ASTM D664.
    High TAN crudes are corrosive, especially at high temperatures, affecting refinery materials selection.
    TAN influences blending, corrosion inhibitor use, and process economics.
    Monitoring TAN is essential for asset integrity and maintenance planning.
    """
    return (
        "Total Acid Number (TAN), determined by ASTM D664, measures crude acidity and predicts corrosion risk. "
        "High TAN crudes require careful materials selection and inhibitor strategies. "
        "TAN is a key blending and maintenance planning parameter."
    )

def rf_distillation_tbp(context: Dict[str, Any]) -> str:
    """
    True Boiling Point (TBP) distillation, per ASTM D2892, provides a detailed boiling range distribution.
    TBP is used to model refinery yields, design distillation columns, and characterize crude fractions.
    TBP data is more precise than simple atmospheric distillation (ASTM D86).
    TBP curves are essential for process simulation and product slate optimization.
    """
    return (
        "TBP distillation (ASTM D2892) yields detailed boiling range data for crude oil, "
        "enabling accurate refinery yield modeling and process design. "
        "TBP curves are foundational for simulation and optimization."
    )

def rf_distillation_astm_d86(context: Dict[str, Any]) -> str:
    """
    ASTM D86 is a standard distillation method for petroleum products at atmospheric pressure.
    It provides initial, 10%, 50%, 90%, and final boiling points.
    D86 is widely used for gasoline, jet, and diesel fuel specification.
    D86 data is less detailed than TBP but faster and suitable for quality control.
    """
    return (
        "ASTM D86 distillation provides rapid boiling point data for fuels, supporting product specification "
        "and quality control. While less detailed than TBP, D86 is industry standard for gasoline, jet, and diesel."
    )

def rf_petroleum_fractions(context: Dict[str, Any]) -> str:
    """
    Petroleum fractions are defined by boiling range: naphtha (<200°C), kerosene (150-275°C), diesel (250-350°C), VGO (350-550°C), residuum (>550°C).
    Fractionation is performed by atmospheric and vacuum distillation.
    Each fraction serves as feedstock for further processing (e.g., naphtha for reforming, VGO for FCC).
    Fraction properties determine downstream process selection and product quality.
    """
    return (
        "Petroleum fractions—naphtha, kerosene, diesel, VGO, residuum—are separated by distillation. "
        "Their boiling ranges and properties dictate downstream processing and product applications."
    )

def rf_hydrocarbon_classes(context: Dict[str, Any]) -> str:
    """
    Hydrocarbons in petroleum are classified as paraffins (alkanes), naphthenes (cycloalkanes), aromatics, and olefins.
    Paraffins and naphthenes dominate in crude; aromatics increase after reforming.
    Olefins are rare in crude but abundant in FCC products.
    Hydrocarbon class distribution affects octane, cetane, and product stability.
    """
    return (
        "Petroleum hydrocarbons are categorized as paraffins, naphthenes, aromatics, and olefins. "
        "Their distribution influences fuel properties such as octane, cetane, and stability."
    )

def rf_atmospheric_distillation(context: Dict[str, Any]) -> str:
    """
    Atmospheric distillation is the primary separation step in refining, operating at 1 atm.
    It separates crude into naphtha, kerosene, diesel, AGO, and atmospheric resid.
    Overhead and side draws are sent to further processing.
    Column design considers feed preheat, reflux, and draw tray configuration.
    """
    return (
        "Atmospheric distillation separates crude into major fractions at 1 atm. "
        "Column design and operation impact yield and energy efficiency. "
        "Products are routed to downstream units for further upgrading."
    )

def rf_vacuum_distillation(context: Dict[str, Any]) -> str:
    """
    Vacuum distillation processes atmospheric residuum at reduced pressure (<50 mmHg).
    It recovers VGO and vacuum resid, minimizing thermal cracking.
    Vacuum operation lowers boiling points, reducing coke formation.
    VGO is a key FCC and hydrocracking feedstock.
    """
    return (
        "Vacuum distillation recovers VGO and vacuum resid from atmospheric bottoms under reduced pressure. "
        "This minimizes cracking and coke, providing feed for FCC and hydrocracking."
    )

def rf_catalytic_reforming(context: Dict[str, Any]) -> str:
    """
    Catalytic reforming converts low-octane naphtha into high-octane reformate using Pt-based catalysts.
    Key reactions: dehydrogenation, isomerization, cyclization, hydrocracking.
    Reformate is rich in aromatics (BTX) and boosts gasoline octane.
    Hydrogen is coproduced, supporting hydrotreating.
    Catalyst life is affected by feed sulfur and chloride balance.
    """
    return (
        "Catalytic reforming upgrades naphtha to high-octane reformate and aromatics (BTX). "
        "It also generates hydrogen for refinery use. Catalyst management is critical for performance."
    )

def rf_fcc(context: Dict[str, Any]) -> str:
    """
    Fluid Catalytic Cracking (FCC) converts VGO and heavy feeds into gasoline, LPG, and olefins.
    Operates at 500°C+, using zeolite catalysts in a circulating fluid bed.
    FCC maximizes gasoline yield and produces propylene for petrochemicals.
    Catalyst activity, feed metals, and coke yield are key control parameters.
    """
    return (
        "FCC is the primary gasoline and propylene producer, converting VGO with zeolite catalysts. "
        "Process control focuses on catalyst activity, coke, and metals management."
    )

def rf_hydrocracking(context: Dict[str, Any]) -> str:
    """
    Hydrocracking uses bifunctional catalysts (acid + metal) and high H2 pressure to convert VGO/resid to diesel, jet, and naphtha.
    Operates at 350-450°C, 100-200 bar.
    Hydrocracking produces high-quality, low-sulfur products.
    Catalyst selection and process severity are tailored to feed and product targets.
    """
    return (
        "Hydrocracking produces premium diesel, jet, and naphtha from heavy feeds under high H2 pressure. "
        "It achieves deep conversion and desulfurization. Catalyst and severity optimization are essential."
    )

def rf_alkylation(context: Dict[str, Any]) -> str:
    """
    Alkylation combines isobutane with olefins (C3-C4) using HF or H2SO4 catalyst to produce alkylate.
    Alkylate is a high-octane, low-RVP gasoline blendstock.
    Process safety is critical due to acid handling.
    Feed olefin purity and isobutane-to-olefin ratio affect yield and quality.
    """
    return (
        "Alkylation produces high-octane alkylate for gasoline by reacting isobutane with olefins. "
        "HF or H2SO4 catalysts are used, requiring stringent safety protocols."
    )

def rf_isomerization(context: Dict[str, Any]) -> str:
    """
    Isomerization converts n-paraffins (C5-C6) to iso-paraffins, raising gasoline octane.
    Catalysts: Pt/Al2O3, zeolites; process is sensitive to feed sulfur.
    Isomerate is blended into gasoline to meet octane specs.
    Process operates at 100-200°C, moderate H2 pressure.
    """
    return (
        "Isomerization upgrades light naphtha by converting n-paraffins to iso-paraffins, enhancing octane. "
        "Process requires clean feeds and specialized catalysts."
    )

def rf_coking(context: Dict[str, Any]) -> str:
    """
    Coking thermally cracks residuum to produce lighter products and petroleum coke.
    Delayed coking is most common; fluid and flexicoking are alternatives.
    Coke quality depends on feed properties and operating conditions.
    Coking enables deep conversion but increases complexity and emissions.
    """
    return (
        "Coking cracks residuum to lighter products and coke, enabling deep conversion of heavy oils. "
        "Delayed coking is widely used; coke quality and yield depend on feed and operation."
    )

def rf_hydrotreating(context: Dict[str, Any]) -> str:
    """
    Hydrotreating removes sulfur, nitrogen, and metals using NiMo or CoMo catalysts under H2.
    Typical conditions: 300-400°C, 30-130 bar.
    Hydrotreating protects downstream catalysts and meets product sulfur specs.
    Severity is adjusted to balance conversion and catalyst life.
    """
    return (
        "Hydrotreating purifies feeds by removing sulfur, nitrogen, and metals with NiMo/CoMo catalysts. "
        "It is essential for meeting sulfur specs and protecting downstream units."
    )

def rf_petroleum_product_specifications(context: Dict[str, Any]) -> str:
    """
    Product specs (gasoline, diesel, jet) are defined by ASTM standards (e.g., D4814, D975, D1655).
    Key parameters: octane/cetane, sulfur, RVP, distillation, flash point.
    Compliance ensures performance, safety, and regulatory acceptance.
    Specs evolve with environmental and engine technology changes.
    """
    return (
        "Petroleum product specifications are governed by ASTM standards, covering octane/cetane, sulfur, RVP, "
        "distillation, and safety properties. Compliance ensures marketability and regulatory approval."
    )

def rf_octane_rating(context: Dict[str, Any]) -> str:
    """
    Octane rating (RON, MON, AKI) measures gasoline's resistance to knock.
    RON (ASTM D2699) and MON (ASTM D2700) use standardized engines.
    AKI = (RON + MON)/2.
    Higher octane fuels prevent engine knock, enabling higher compression ratios.
    """
    return (
        "Octane rating, determined by RON (D2699), MON (D2700), and AKI, quantifies gasoline's knock resistance. "
        "Higher octane supports advanced engine designs and performance."
    )

def rf_cetane_number(context: Dict[str, Any]) -> str:
    """
    Cetane number (ASTM D613) measures diesel ignition quality.
    Higher cetane reduces ignition delay, improving cold start and combustion.
    Additives and hydroprocessing can raise cetane.
    """
    return (
        "Cetane number (ASTM D613) indicates diesel ignition quality. "
        "Higher cetane improves cold start and combustion. Refiners may use additives or hydroprocessing to boost cetane."
    )

def rf_rvp(context: Dict[str, Any]) -> str:
    """
    Reid Vapor Pressure (RVP, ASTM D323) measures gasoline volatility.
    RVP affects evaporative emissions, driveability, and seasonal blending.
    Regulatory limits vary by region and season.
    """
    return (
        "RVP (ASTM D323) quantifies gasoline volatility, impacting emissions and driveability. "
        "Seasonal and regional regulations dictate RVP limits for compliance."
    )

def rf_flash_point(context: Dict[str, Any]) -> str:
    """
    Flash point (ASTM D93/D56) is the lowest temperature at which vapors ignite.
    It is a key safety parameter for transport and storage.
    Specified for diesel, jet, and lubricants.
    """
    return (
        "Flash point, determined by ASTM D93/D56, is a critical safety property for fuels and lubricants. "
        "It governs handling, storage, and regulatory classification."
    )

def rf_pour_point(context: Dict[str, Any]) -> str:
    """
    Pour point (ASTM D97) is the lowest temperature at which oil flows.
    It affects cold weather operability of fuels and lubricants.
    Additives can depress pour point.
    """
    return (
        "Pour point (ASTM D97) indicates the lowest temperature for oil flow, affecting cold weather performance. "
        "Pour point depressants are used to improve operability."
    )

def rf_lubricant_base_oils(context: Dict[str, Any]) -> str:
    """
    Lubricant base oils are classified as Group I-V (API 1509).
    Group I: solvent-refined; II/III: hydroprocessed; IV: PAO; V: others.
    Properties: viscosity index, volatility, oxidation stability.
    Selection depends on application, cost, and performance.
    """
    return (
        "Lubricant base oils are grouped I-V by refining method and properties. "
        "Selection impacts lubricant performance, cost, and application suitability."
    )

def rf_petrochemical_feedstocks(context: Dict[str, Any]) -> str:
    """
    Petrochemical feedstocks include ethylene, propylene, butadiene, BTX, derived from naphtha, LPG, or FCC offgas.
    Feedstock selection depends on process (steam cracking, FCC, reforming).
    Purity and composition affect yields and downstream product quality.
    """
    return (
        "Petrochemical feedstocks (ethylene, propylene, BTX) are sourced from naphtha, LPG, and FCC units. "
        "Feedstock quality and selection drive petrochemical yields and economics."
    )

def rf_ngl_processing(context: Dict[str, Any]) -> str:
    """
    Natural Gas Liquids (NGLs) are separated by cryogenic or absorption processes.
    Fractionation yields ethane, propane, butane, natural gasoline.
    NGLs are key petrochemical and fuel feedstocks.
    Processing is governed by GPA and API standards.
    """
    return (
        "NGL processing separates ethane, propane, butane, and natural gasoline from raw gas. "
        "Fractionation and cryogenic methods are used per GPA/API standards."
    )

def rf_asphaltene_precipitation(context: Dict[str, Any]) -> str:
    """
    Asphaltene precipitation occurs when solubility is reduced (e.g., by n-alkane addition, pressure drop).
    Onset is detected by titration (ASTM D6560) or microscopy.
    Precipitation causes fouling, plugging, and instability in blending.
    Colloidal stability is managed by controlling resin/asphaltene ratio.
    """
    return (
        "Asphaltene precipitation is triggered by changes in solubility, monitored by ASTM D6560. "
        "Managing resin/asphaltene ratio and blending conditions maintains colloidal stability."
    )

def rf_conradson_carbon_residue(context: Dict[str, Any]) -> str:
    """
    Conradson Carbon Residue (CCR, ASTM D189) measures coke-forming tendency.
    High CCR indicates fouling risk in FCC, coking, and furnaces.
    Used for feedstock selection and process optimization.
    """
    return (
        "CCR (ASTM D189) quantifies coke-forming tendency, guiding feedstock selection for FCC and coking. "
        "High CCR feeds pose fouling and operational risks."
    )

def rf_fractionation(context: Dict[str, Any]) -> str:
    """
    Fractionation separates petroleum streams by boiling point using distillation columns.
    Tray and packing design, reflux ratio, and cut points are optimized for yield and purity.
    Fractionation is applied in crude, FCC, hydrocracking, and NGL units.
    """
    return (
        "Fractionation by distillation is fundamental to refining, optimizing yield and purity of products. "
        "Column design and operation are tailored to feed and product requirements."
    )

def rf_hdn(context: Dict[str, Any]) -> str:
    """
    Hydrodenitrogenation (HDN) removes organic nitrogen from feeds using NiMo/CoMo catalysts.
    Nitrogen poisons FCC and reforming catalysts.
    HDN is integrated with hydrotreating for deep purification.
    """
    return (
        "HDN removes nitrogen from feeds, protecting FCC and reforming catalysts. "
        "It is achieved with NiMo/CoMo catalysts, typically in hydrotreating units."
    )

def rf_hdm(context: Dict[str, Any]) -> str:
    """
    Hydrodemetallization (HDM) removes metals (Ni, V) from heavy feeds.
    Metals poison FCC/hydrocracking catalysts and increase coke.
    HDM is performed in guard beds before main hydrotreating.
    """
    return (
        "HDM eliminates metals from heavy feeds, preventing catalyst poisoning and coke. "
        "Guard beds are used upstream of hydrotreating/hydrocracking."
    )

def rf_btx_production(context: Dict[str, Any]) -> str:
    """
    BTX (benzene, toluene, xylene) are produced by catalytic reforming and extracted from reformate or pyrolysis gasoline.
    Extraction uses solvent or distillation (UOP Tatoray, Sulfolane).
    BTX are key aromatics for petrochemicals.
    """
    return (
        "BTX aromatics are produced by reforming and extracted for petrochemical use. "
        "Solvent extraction and distillation (UOP, Sulfolane) are standard methods."
    )

def rf_delayed_coking(context: Dict[str, Any]) -> str:
    """
    Delayed coking thermally cracks residuum in large drums, producing gas, naphtha, diesel, and petroleum coke.
    Drum cycle and quench control coke quality.
    Coking enables deep conversion but increases complexity and emissions.
    """
    return (
        "Delayed coking cracks residuum in drums, yielding lighter products and coke. "
        "Drum operation and quenching control product quality and yield."
    )

def rf_colloidal_stability(context: Dict[str, Any]) -> str:
    """
    Colloidal stability of asphaltenes is maintained by resin/asphaltene ratio.
    Instability leads to precipitation, fouling, and blending incompatibility.
    Stability is assessed by spot tests, microscopy, and solvent titration.
    """
    return (
        "Colloidal stability of asphaltenes is governed by resin/asphaltene balance. "
        "Instability causes fouling and blending issues. Spot tests and titration assess stability."
    )

def rf_onset_precipitation(context: Dict[str, Any]) -> str:
    """
    Onset of asphaltene precipitation is detected by titration (ASTM D6560) or optical methods.
    Early detection allows blending and additive strategies to prevent fouling.
    """
    return (
        "Onset of asphaltene precipitation is identified by ASTM D6560 or optical methods. "
        "Early intervention prevents fouling via blending and additives."
    )

def rf_flocculation(context: Dict[str, Any]) -> str:
    """
    Flocculation is aggregation of asphaltene particles, leading to sludge and fouling.
    Controlled by solvent quality, temperature, and resin content.
    Monitored by microscopy and filtration tests.
    """
    return (
        "Flocculation of asphaltenes forms sludge and fouling. "
        "Solvent quality, temperature, and resin content are key controls."
    )

DOCTRINE_BLOCKS: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Crude Oil SARA Analysis",
        keywords=["SARA", "saturates", "aromatics", "resins", "asphaltenes", "chromatography", "ASTM D2007"],
        conclusion_template="SARA analysis provides a detailed compositional breakdown of crude oil, "
                           "informing on fouling, stability, and blending behavior. Standardized methods ensure comparability.",
        reasoning_framework=rf_crude_oil_sara,
        key_factors=[
            "Chromatographic method selection",
            "Solvent system and protocol",
            "Sample handling and representativity",
            "Impact on fouling and stability",
            "ASTM/IP standardization"
        ],
        primary_authority=[
            "ASTM D2007: Standard Test Method for Characteristic Groups in Asphalts",
            "ASTM D6560: Determination of Asphaltenes in Crude Petroleum",
            "IP 143: Determination of Asphaltenes (Heptane Insolubles)"
        ],
        burden_holder="Refinery/Lab",
        adversary_position="SARA is not predictive for all fouling scenarios",
        counter_arguments=[
            "SARA fractions depend on method and solvent",
            "Asphaltene content may not correlate with fouling in all crudes",
            "Sample aging affects results",
            "Alternative methods (NMR, FTIR) exist",
            "SARA does not capture all polar species"
        ],
        resolution_strategy="Use standardized protocols and cross-validate with alternative methods for critical decisions.",
        entity_scope="Crude Oil",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ASTM D2007", "ASTM D6560", "IP 143"
        ],
        issue_category=IssueCategory.CRUDE_OIL_CHARACTERIZATION
    ),
    DoctrineBlock(
        topic="Crude Oil API Gravity",
        keywords=["API gravity", "density", "ASTM D287", "ASTM D1298", "valuation"],
        conclusion_template="API gravity is a primary indicator of crude oil quality and value, "
                           "guiding blending and refinery configuration decisions.",
        reasoning_framework=rf_crude_oil_api_gravity,
        key_factors=[
            "Measurement method (D287/D1298)",
            "Crude valuation and pricing",
            "Blending strategies",
            "Impact on product yields",
            "Refinery configuration"
        ],
        primary_authority=[
            "ASTM D287: API Gravity of Crude Petroleum",
            "ASTM D1298: Density, Relative Density, or API Gravity of Crude Petroleum",
            "API Manual of Petroleum Measurement Standards (MPMS) Ch. 9.1"
        ],
        burden_holder="Crude Supplier",
        adversary_position="API gravity does not capture all quality aspects",
        counter_arguments=[
            "API gravity ignores sulfur, metals, and TAN",
            "Blending can mask underlying issues",
            "Measurement errors affect valuation",
            "API is temperature dependent",
            "Other indices (UOP K factor) may be preferred"
        ],
        resolution_strategy="Combine API with sulfur, TAN, and metals for comprehensive assessment.",
        entity_scope="Crude Oil",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ASTM D287", "ASTM D1298", "API MPMS Ch. 9.1"
        ],
        issue_category=IssueCategory.CRUDE_OIL_CHARACTERIZATION
    ),
    DoctrineBlock(
        topic="Crude Oil Sulfur Content",
        keywords=["sulfur", "ASTM D4294", "ASTM D2622", "ASTM D5453", "sour crude"],
        conclusion_template="Sulfur content critically impacts crude value, processing requirements, and environmental compliance.",
        reasoning_framework=rf_crude_oil_sulfur_content,
        key_factors=[
            "Measurement method (D4294/D2622/D5453)",
            "Sulfur speciation",
            "Hydrotreating requirements",
            "Impact on catalyst life",
            "Environmental regulations"
        ],
        primary_authority=[
            "ASTM D4294: Sulfur in Petroleum Products by XRF",
            "ASTM D2622: Sulfur in Petroleum Products by WDXRF",
            "ASTM D5453: Sulfur in Light Hydrocarbons by UVF"
        ],
        burden_holder="Crude Supplier",
        adversary_position="Sulfur speciation is more important than total sulfur",
        counter_arguments=[
            "Total sulfur does not indicate H2S/mercaptan content",
            "Measurement interference possible",
            "Sulfur distribution affects processing",
            "Low sulfur may still require hydrotreating",
            "Regulations may change"
        ],
        resolution_strategy="Combine total and speciated sulfur analysis for process planning.",
        entity_scope="Crude Oil",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ASTM D4294", "ASTM D2622", "ASTM D5453"
        ],
        issue_category=IssueCategory.CRUDE_OIL_CHARACTERIZATION
    ),
    DoctrineBlock(
        topic="Crude Oil Total Acid Number (TAN)",
        keywords=["TAN", "ASTM D664", "acidity", "corrosion", "blending"],
        conclusion_template="TAN is a key indicator of crude corrosivity, influencing materials selection and blending.",
        reasoning_framework=rf_crude_oil_tan,
        key_factors=[
            "Measurement method (D664)",
            "Corrosion risk assessment",
            "Blending strategies",
            "Materials selection",
            "Impact on maintenance"
        ],
        primary_authority=[
            "ASTM D664: Acid Number of Petroleum Products",
            "API TR 938-C: Corrosion in High TAN Crudes",
            "NACE SP0775: Mitigation of Sulfidic Acid Corrosion"
        ],
        burden_holder="Crude Supplier",
        adversary_position="TAN does not capture all corrosive species",
        counter_arguments=[
            "Naphthenic acids vary in aggressiveness",
            "TAN can be reduced by blending",
            "Other acids (organic/inorganic) present",
            "Measurement drift possible",
            "Corrosion inhibitors may mask risk"
        ],
        resolution_strategy="Combine TAN with corrosion monitoring and inhibitor programs.",
        entity_scope="Crude Oil",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ASTM D664", "API TR 938-C", "NACE SP0775"
        ],
        issue_category=IssueCategory.CRUDE_OIL_CHARACTERIZATION
    ),
    DoctrineBlock(
        topic="Distillation: True Boiling Point (TBP)",
        keywords=["TBP", "ASTM D2892", "boiling range", "yield", "simulation"],
        conclusion_template="TBP distillation provides detailed boiling range data, essential for refinery modeling and product optimization.",
        reasoning_framework=rf_distillation_tbp,
        key_factors=[
            "Measurement method (D2892)",
            "Boiling range distribution",
            "Refinery yield modeling",
            "Process simulation",
            "Product slate optimization"
        ],
        primary_authority=[
            "ASTM D2892: Distillation of Crude Oil",
            "API Technical Data Book, Section 2",
            "UOP 916: TBP Distillation"
        ],
        burden_holder="Refinery",
        adversary_position="TBP is time-consuming and costly",
        counter_arguments=[
            "TBP requires large sample size",
            "Not suitable for all crudes",
            "ASTM D86 is faster",
            "Simulation can substitute",
            "Operator skill affects accuracy"
        ],
        resolution_strategy="Use TBP for critical modeling; supplement with D86 for routine control.",
        entity_scope="Crude Oil/Refinery",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ASTM D2892", "API TDB", "UOP 916"
        ],
        issue_category=IssueCategory.DISTILLATION
    ),
    DoctrineBlock(
        topic="Distillation: ASTM D86",
        keywords=["ASTM D86", "distillation", "boiling point", "quality control", "fuel"],
        conclusion_template="ASTM D86 distillation provides rapid boiling range data for fuels, supporting specification and quality control.",
        reasoning_framework=rf_distillation_astm_d86,
        key_factors=[
            "Measurement method (D86)",
            "Boiling point distribution",
            "Product specification",
            "Quality control",
            "Comparison to TBP"
        ],
        primary_authority=[
            "ASTM D86: Distillation of Petroleum Products",
            "ASTM D4814: Gasoline Specification",
            "ASTM D975: Diesel Specification"
        ],
        burden_holder="Lab",
        adversary_position="D86 lacks TBP resolution",
        counter_arguments=[
            "D86 is less precise for complex feeds",
            "Sample loss possible",
            "Operator bias",
            "Not suitable for heavy fractions",
            "TBP preferred for modeling"
        ],
        resolution_strategy="Use D86 for routine QC; TBP for detailed analysis.",
        entity_scope="Fuels",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ASTM D86", "ASTM D4814", "ASTM D975"
        ],
        issue_category=IssueCategory.DISTILLATION
    ),
    DoctrineBlock(
        topic="Petroleum Fractions",
        keywords=["naphtha", "kerosene", "diesel", "VGO", "residuum", "boiling range"],
        conclusion_template="Petroleum fractions are defined by boiling range and serve as feedstocks for downstream processes.",
        reasoning_framework=rf_petroleum_fractions,
        key_factors=[
            "Boiling range definitions",
            "Fractionation method",
            "Feedstock allocation",
            "Product quality",
            "Downstream processing"
        ],
        primary_authority=[
            "API Technical Data Book, Section 2",
            "ASTM D86/D2892",
            "UOP 916"
        ],
        burden_holder="Refinery",
        adversary_position="Boiling ranges overlap; definitions vary",
        counter_arguments=[
            "Cut points are refinery-specific",
            "Product specs may differ",
            "Feedstock quality affects allocation",
            "Fraction blending is common",
            "International standards may differ"
        ],
        resolution_strategy="Adopt site-specific cut points and validate with product specs.",
        entity_scope="Refinery",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "API TDB", "ASTM D86", "ASTM D2892"
        ],
        issue_category=IssueCategory.PETROLEUM_FRACTIONS
    ),
    DoctrineBlock(
        topic="Hydrocarbon Classes",
        keywords=["paraffin", "naphthene", "aromatic", "olefin", "hydrocarbon class"],
        conclusion_template="Hydrocarbon class distribution affects fuel properties and process selection.",
        reasoning_framework=rf_hydrocarbon_classes,
        key_factors=[
            "Class definitions",
            "Distribution in crude and products",
            "Impact on octane/cetane",
            "Process influence",
            "Analytical methods"
        ],
        primary_authority=[
            "ASTM D3239: Aromatics in Petroleum",
            "API Technical Data Book, Section 2",
            "UOP 915"
        ],
        burden_holder="Lab",
        adversary_position="Class overlap and measurement uncertainty",
        counter_arguments=[
            "Aromatics and naphthenes overlap",
            "Olefin quantification is challenging",
            "NMR/FTIR may be required",
            "Process changes shift distribution",
            "Class definitions vary"
        ],
        resolution_strategy="Use multiple analytical methods for robust class quantification.",
        entity_scope="Crude/Products",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ASTM D3239", "API TDB", "UOP 915"
        ],
        issue_category=IssueCategory.HYDROCARBON_CLASSES
    ),
    DoctrineBlock(
        topic="Atmospheric Distillation",
        keywords=["atmospheric distillation", "column", "fractionation", "naphtha", "diesel"],
        conclusion_template="Atmospheric distillation is the primary separation step, producing major refinery fractions.",
        reasoning_framework=rf_atmospheric_distillation,
        key_factors=[
            "Column design",
            "Feed preheat",
            "Draw tray configuration",
            "Product routing",
            "Energy efficiency"
        ],
        primary_authority=[
            "API Technical Data Book, Section 2",
            "Perry's Chemical Engineers' Handbook, Ch. 13",
            "ASTM D2892"
        ],
        burden_holder="Refinery",
        adversary_position="Atmospheric distillation has limited cut point flexibility",
        counter_arguments=[
            "Thermal cracking risk at high temp",
            "Limited separation for heavy ends",
            "Energy intensive",
            "Product overlap",
            "Requires vacuum distillation for deeper cuts"
        ],
        resolution_strategy="Optimize column operation and integrate with vacuum distillation.",
        entity_scope="Refinery",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "API TDB", "Perry's Handbook", "ASTM D2892"
        ],
        issue_category=IssueCategory.REFINING_PROCESSES
    ),
    DoctrineBlock(
        topic="Vacuum Distillation",
        keywords=["vacuum distillation", "VGO", "vacuum resid", "pressure", "coke"],
        conclusion_template="Vacuum distillation recovers VGO and resid under reduced pressure, minimizing cracking.",
        reasoning_framework=rf_vacuum_distillation,
        key_factors=[
            "Operating pressure",
            "Feed preheat",
            "Coke minimization",
            "Product quality",
            "Integration with FCC/hydrocracking"
        ],
        primary_authority=[
            "API Technical Data Book, Section 2",
            "Perry's Chemical Engineers' Handbook, Ch. 13",
            "ASTM D1160"
        ],
        burden_holder="Refinery",
        adversary_position="Vacuum distillation is capital intensive",
        counter_arguments=[
            "Requires large columns and ejectors",
            "Limited by feed metals and asphaltenes",
            "Coke formation still possible",
            "Product yields depend on cut points",
            "Integration complexity"
        ],
        resolution_strategy="Balance cut points and integrate with downstream units for maximum value.",
        entity_scope="Refinery",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "API TDB", "Perry's Handbook", "ASTM D1160"
        ],
        issue_category=IssueCategory.REFINING_PROCESSES
    ),
    DoctrineBlock(
        topic="Catalytic Reforming",
        keywords=["catalytic reforming", "naphtha", "platforming", "aromatics", "octane"],
        conclusion_template="Catalytic reforming upgrades naphtha to high-octane reformate and aromatics, producing hydrogen.",
        reasoning_framework=rf_catalytic_reforming,
        key_factors=[
            "Catalyst selection",
            "Feed sulfur content",
            "Aromatics yield",
            "Hydrogen production",
            "Catalyst regeneration"
        ],
        primary_authority=[
            "UOP Platforming Process Manual",
            "API Technical Data Book, Section 3",
            "ASTM D2699/D2700"
        ],
        burden_holder="Refinery",
        adversary_position="Catalyst deactivation limits run length",
        counter_arguments=[
            "Chloride balance critical",
            "Sulfur poisons catalyst",
            "Regeneration downtime",
            "Aromatics regulations",
            "Hydrogen management"
        ],
        resolution_strategy="Implement feed pretreatment and optimize regeneration cycles.",
        entity_scope="Refinery",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "UOP Platforming", "API TDB", "ASTM D2699"
        ],
        issue_category=IssueCategory.CATALYTIC_PROCESSES
    ),
    DoctrineBlock(
        topic="Fluid Catalytic Cracking (FCC)",
        keywords=["FCC", "fluid catalytic cracking", "VGO", "gasoline", "olefins"],
        conclusion_template="FCC is the main gasoline and propylene producer, converting VGO with zeolite catalysts.",
        reasoning_framework=rf_fcc,
        key_factors=[
            "Catalyst activity",
            "Feed quality",
            "Coke yield",
            "Metals management",
            "Gasoline/propylene yield"
        ],
        primary_authority=[
            "API Technical Data Book, Section 3",
            "UOP FCC Process Manual",
            "ASTM D323"
        ],
        burden_holder="Refinery",
        adversary_position="Metals and coke limit FCC performance",
        counter_arguments=[
            "Feed metals poison catalyst",
            "Coke reduces yield",
            "Emissions control required",
            "Product quality varies",
            "Catalyst attrition"
        ],
        resolution_strategy="Use feed pretreatment and catalyst additives to manage metals and coke.",
        entity_scope="Refinery",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "API TDB", "UOP FCC", "ASTM D323"
        ],
        issue_category=IssueCategory.CATALYTIC_PROCESSES
    ),
    DoctrineBlock(
        topic="Hydrocracking",
        keywords=["hydrocracking", "diesel", "kerosene", "VGO", "high pressure"],
        conclusion_template="Hydrocracking produces premium diesel, jet, and naphtha from heavy feeds under high H2 pressure.",
        reasoning_framework=rf_hydrocracking,
        key_factors=[
            "Catalyst selection",
            "Process severity",
            "Hydrogen partial pressure",
            "Product selectivity",
            "Feed quality"
        ],
        primary_authority=[
            "API Technical Data Book, Section 3",
            "UOP Hydrocracking Process Manual",
            "ASTM D975"
        ],
        burden_holder="Refinery",
        adversary_position="Hydrocracking is capital and energy intensive",
        counter_arguments=[
            "High H2 consumption",
            "Catalyst cost",
            "Feed metals impact",
            "Product selectivity trade-offs",
            "Integration with hydrotreating"
        ],
        resolution_strategy="Optimize severity and integrate with hydrogen management.",
        entity_scope="Refinery",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "API TDB", "UOP Hydrocracking", "ASTM D975"
        ],
        issue_category=IssueCategory.CATALYTIC_PROCESSES
    ),
    DoctrineBlock(
        topic="Alkylation",
        keywords=["alkylation", "isobutane", "olefin", "HF", "sulfuric acid"],
        conclusion_template="Alkylation produces high-octane alkylate for gasoline using HF or H2SO4 catalysts.",
        reasoning_framework=rf_alkylation,
        key_factors=[
            "Catalyst selection",
            "Feed purity",
            "Isobutane/olefin ratio",
            "Process safety",
            "Product octane"
        ],
        primary_authority=[
            "API Technical Data Book, Section 3",
            "UOP Alkylation Process Manual",
            "ASTM D4814"
        ],
        burden_holder="Refinery",
        adversary_position="Acid handling poses safety risks",
        counter_arguments=[
            "HF is highly toxic",
            "Acid consumption and disposal",
            "Feed impurities reduce yield",
            "Regulatory scrutiny",
            "Alternative processes (solid acid)"
        ],
        resolution_strategy="Implement rigorous safety and acid management protocols.",
        entity_scope="Refinery",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "API TDB", "UOP Alkylation", "ASTM D4814"
        ],
        issue_category=IssueCategory.CATALYTIC_PROCESSES
    ),
    DoctrineBlock(
        topic="Isomerization",
        keywords=["isomerization", "light naphtha", "pentane", "hexane", "octane"],
        conclusion_template="Isomerization upgrades light naphtha by converting n-paraffins to iso-paraffins, enhancing octane.",
        reasoning_framework=rf_isomerization,
        key_factors=[
            "Catalyst selection",
            "Feed sulfur content",
            "Octane improvement",
            "Hydrogen management",
            "Process temperature"
        ],
        primary_authority=[
            "API Technical Data Book, Section 3",
            "UOP Isomerization Process Manual",
            "ASTM D4814"
        ],
        burden_holder="Refinery",
        adversary_position="Feed impurities poison catalyst",
        counter_arguments=[
            "Sulfur/olefins deactivate catalyst",
            "Limited octane gain for some feeds",
            "Hydrogen supply needed",
            "Process complexity",
            "Alternative blending options"
        ],
        resolution_strategy="Ensure feed pretreatment and optimize catalyst selection.",
        entity_scope="Refinery",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "API TDB", "UOP Isomerization", "ASTM D4814"
        ],
        issue_category=IssueCategory.CATALYTIC_PROCESSES
    ),
    DoctrineBlock(
        topic="Coking",
        keywords=["coking", "delayed coking", "fluid coking", "Conradson carbon residue", "coke"],
        conclusion_template="Coking cracks residuum to lighter products and coke, enabling deep conversion of heavy oils.",
        reasoning_framework=rf_coking,
        key_factors=[
            "Feed properties",
            "Operating temperature",
            "Coke quality",
            "Product yield",
            "Emissions management"
        ],
        primary_authority=[
            "API Technical Data Book, Section 3",
            "ASTM D189: Conradson Carbon Residue",
            "UOP Delayed Coking Process Manual"
        ],
        burden_holder="Refinery",
        adversary_position="Coking increases emissions and complexity",
        counter_arguments=[
            "Coke disposal challenges",
            "Emissions control required",
            "Feed metals impact coke quality",
            "Cycle time affects yield",
            "Alternative deep conversion options"
        ],
        resolution_strategy="Optimize feed selection and emissions controls.",
        entity_scope="Refinery",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "API TDB", "ASTM D189", "UOP Delayed Coking"
        ],
        issue_category=IssueCategory.COKING
    ),
    DoctrineBlock(
        topic="Hydrotreating",
        keywords=["hydrotreating", "HDS", "HDN", "HDM", "NiMo", "CoMo"],
        conclusion_template="Hydrotreating purifies feeds by removing sulfur, nitrogen, and metals with NiMo/CoMo catalysts.",
        reasoning_framework=rf_hydrotreating,
        key_factors=[
            "Catalyst selection",
            "Operating conditions",
            "Sulfur/nitrogen/metals removal",
            "Feed pretreatment",
            "Catalyst life"
        ],
        primary_authority=[
            "API Technical Data Book, Section 3",
            "UOP Hydrotreating Process Manual",
            "ASTM D5453"
        ],
        burden_holder="Refinery",
        adversary_position="Hydrotreating increases hydrogen demand",
        counter_arguments=[
            "Hydrogen supply constraints",
            "Catalyst deactivation",
            "Operating cost",
            "Feed contaminants",
            "Integration with FCC/hydrocracking"
        ],
        resolution_strategy="Optimize hydrogen management and integrate with upstream units.",
        entity_scope="Refinery",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "API TDB", "UOP Hydrotreating", "ASTM D5453"
        ],
        issue_category=IssueCategory.HYDROPROCESSING
    ),
    DoctrineBlock(
        topic="Petroleum Product Specifications",
        keywords=["ASTM", "specification", "gasoline", "diesel", "jet fuel"],
        conclusion_template="Product specifications are governed by ASTM standards, ensuring performance, safety, and regulatory compliance.",
        reasoning_framework=rf_petroleum_product_specifications,
        key_factors=[
            "ASTM standard selection",
            "Key property limits",
            "Regulatory requirements",
            "Performance criteria",
            "Spec evolution"
        ],
        primary_authority=[
            "ASTM D4814: Gasoline Specification",
            "ASTM D975: Diesel Specification",
            "ASTM D1655: Jet Fuel Specification"
        ],
        burden_holder="Refinery",
        adversary_position="Specs may lag engine technology",
        counter_arguments=[
            "Specs evolve slowly",
            "Regional differences",
            "Performance in new engines",
            "Additive effects",
            "Alternative fuels"
        ],
        resolution_strategy="Monitor spec updates and validate with engine testing.",
        entity_scope="Products",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ASTM D4814", "ASTM D975", "ASTM D1655"
        ],
        issue_category=IssueCategory.PRODUCT_SPECIFICATIONS
    ),
    DoctrineBlock(
        topic="Octane Rating",
        keywords=["octane", "RON", "MON", "AKI", "ASTM D2699", "ASTM D2700"],
        conclusion_template="Octane rating quantifies gasoline's knock resistance, supporting engine performance and design.",
        reasoning_framework=rf_octane_rating,
        key_factors=[
            "Measurement method (D2699/D2700)",
            "RON/MON/AKI definitions",
            "Impact on engine knock",
            "Fuel formulation",
            "Regulatory limits"
        ],
        primary_authority=[
            "ASTM D2699: Research Octane Number",
            "ASTM D2700: Motor Octane Number",
            "API Technical Data Book, Section 4"
        ],
        burden_holder="Refinery",
        adversary_position="Octane does not capture all performance aspects",
        counter_arguments=[
            "Octane sensitivity varies",
            "Additives affect knock",
            "Engine design differences",
            "RVP interaction",
            "Alternative metrics (driveability index)"
        ],
        resolution_strategy="Combine octane with driveability and emissions metrics.",
        entity_scope="Gasoline",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ASTM D2699", "ASTM D2700", "API TDB"
        ],
        issue_category=IssueCategory.FUEL_PROPERTIES
    ),
    DoctrineBlock(
        topic="Cetane Number",
        keywords=["cetane number", "ASTM D613", "diesel", "ignition quality"],
        conclusion_template="Cetane number indicates diesel ignition quality, affecting cold start and combustion.",
        reasoning_framework=rf_cetane_number,
        key_factors=[
            "Measurement method (D613)",
            "Ignition delay",
            "Cold start performance",
            "Additive use",
            "Hydroprocessing impact"
        ],
        primary_authority=[
            "ASTM D613: Cetane Number",
            "API Technical Data Book, Section 4",
            "ASTM D975"
        ],
        burden_holder="Refinery",
        adversary_position="Cetane does not capture all combustion phenomena",
        counter_arguments=[
            "Additives may mask base quality",
            "Engine design differences",
            "Cold flow properties also matter",
            "Measurement repeatability",
            "Alternative metrics (CNMI)"
        ],
        resolution_strategy="Combine cetane with cold flow and emissions metrics.",
        entity_scope="Diesel",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ASTM D613", "API TDB", "ASTM D975"
        ],
        issue_category=IssueCategory.FUEL_PROPERTIES
    ),
    DoctrineBlock(
        topic="Reid Vapor Pressure (RVP)",
        keywords=["RVP", "ASTM D323", "gasoline", "volatility", "emissions"],
        conclusion_template="RVP quantifies gasoline volatility, impacting emissions and driveability.",
        reasoning_framework=rf_rvp,
        key_factors=[
            "Measurement method (D323)",
            "Seasonal/regional limits",
            "Evaporative emissions",
            "Driveability",
            "Blendstock selection"
        ],
        primary_authority=[
            "ASTM D323: RVP",
            "ASTM D4814: Gasoline Specification",
            "EPA RVP Regulations"
        ],
        burden_holder="Refinery",
        adversary_position="RVP does not capture all volatility effects",
        counter_arguments=[
            "Driveability index may be better",
            "Blendstock interaction",
            "Measurement variability",
            "Regional spec differences",
            "Alternative volatility metrics"
        ],
        resolution_strategy="Combine RVP with driveability and emissions testing.",
        entity_scope="Gasoline",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ASTM D323", "ASTM D4814", "EPA"
        ],
        issue_category=IssueCategory.FUEL_PROPERTIES
    ),
    DoctrineBlock(
        topic="Flash Point",
        keywords=["flash point", "ASTM D93", "ASTM D56", "safety", "transport"],
        conclusion_template="Flash point is a critical safety property for fuels and lubricants, governing handling and transport.",
        reasoning_framework=rf_flash_point,
        key_factors=[
            "Measurement method (D93/D56)",
            "Product classification",
            "Transport regulations",
            "Storage safety",
            "Additive effects"
        ],
        primary_authority=[
            "ASTM D93: Flash Point by Pensky-Martens",
            "ASTM D56: Flash Point by Tag Closed Cup",
            "API Technical Data Book, Section 4"
        ],
        burden_holder="Refinery",
        adversary_position="Flash point does not predict all hazards",
        counter_arguments=[
            "Additives may lower flash point",
            "Measurement variability",
            "Vapor pressure interaction",
            "Regulatory changes",
            "Alternative safety metrics"
        ],
        resolution_strategy="Combine flash point with RVP and safety audits.",
        entity_scope="Fuels/Lubricants",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ASTM D93", "ASTM D56", "API TDB"
        ],
        issue_category=IssueCategory.FUEL_PROPERTIES
    ),
    DoctrineBlock(
        topic="Pour Point",
        keywords=["pour point", "ASTM D97", "cold flow", "additives", "lubricants"],
        conclusion_template="Pour point indicates lowest temperature for oil flow, affecting cold weather performance.",
        reasoning_framework=rf_pour_point,
        key_factors=[
            "Measurement method (D97)",
            "Cold flow properties",
            "Additive use",
            "Product application",
            "Blending strategies"
        ],
        primary_authority=[
            "ASTM D97: Pour Point",
            "API Technical Data Book, Section 4",
            "ASTM D2500: Cloud Point"
        ],
        burden_holder="Refinery",
        adversary_position="Pour point does not capture all cold flow issues",
        counter_arguments=[
            "Cloud point may be more relevant",
            "Additives may mask base oil",
            "Measurement repeatability",
            "Blending effects",
            "Application-specific requirements"
        ],
        resolution_strategy="Combine pour and cloud point testing for cold flow assessment.",
        entity_scope="Fuels/Lubricants",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ASTM D97", "API TDB", "ASTM D2500"
        ],
        issue_category=IssueCategory.FUEL_PROPERTIES
    ),
    DoctrineBlock(
        topic="Lubricant Base Oils",
        keywords=["base oil", "Group I", "Group II", "Group III", "Group IV", "Group V"],
        conclusion_template="Lubricant base oils are grouped I-V by refining method and properties, impacting performance and cost.",
        reasoning_framework=rf_lubricant_base_oils,
        key_factors=[
            "API 1509 classification",
            "Viscosity index",
            "Oxidation stability",
            "Volatility",
            "Application suitability"
        ],
        primary_authority=[
            "API 1509: Engine Oil Licensing",
            "ASTM D6074: Base Oil Properties",
            "ASTM D4485: Engine Oil Performance"
        ],
        burden_holder="Refinery",
        adversary_position="Group definitions may overlap",
        counter_arguments=[
            "Hydroprocessing blurs boundaries",
            "Additives affect performance",
            "Cost/performance trade-offs",
            "Application-specific needs",
            "Emerging base oils (esters, GTL)"
        ],
        resolution_strategy="Select base oil group based on application and performance requirements.",
        entity_scope="Lubricants",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "API 1509", "ASTM D6074", "ASTM D4485"
        ],
        issue_category=IssueCategory.LUBRICANT_BASE_OILS
    ),
    DoctrineBlock(
        topic="Petrochemical Feedstocks",
        keywords=["petrochemical feedstock", "ethylene", "propylene", "butadiene", "BTX"],
        conclusion_template="Petrochemical feedstocks (ethylene, propylene, BTX) are sourced from naphtha, LPG, and FCC units.",
        reasoning_framework=rf_petrochemical_feedstocks,
        key_factors=[
            "Feedstock source",
            "Purity and composition",
            "Process selection",
            "Yield optimization",
            "Downstream integration"
        ],
        primary_authority=[
            "API Technical Data Book, Section 5",
            "UOP Olefin Process Manual",
            "ASTM D1157: Hydrocarbon Gases"
        ],
        burden_holder="Refinery",
        adversary_position="Feedstock impurities affect yields",
        counter_arguments=[
            "Contaminants reduce selectivity",
            "Process integration complexity",
            "Market volatility",
            "Alternative feedstocks (bio, GTL)",
            "Spec changes"
        ],
        resolution_strategy="Optimize feedstock selection and integrate impurity removal.",
        entity_scope="Petrochemicals",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "API TDB", "UOP Olefin", "ASTM D1157"
        ],
        issue_category=IssueCategory.PETROCHEMICAL_FEEDSTOCKS
    ),
    DoctrineBlock(
        topic="Natural Gas Liquids (NGL) Processing",
        keywords=["NGL", "ethane", "propane", "butane", "fractionation"],
        conclusion_template="NGL processing separates ethane, propane, butane, and natural gasoline from raw gas.",
        reasoning_framework=rf_ngl_processing,
        key_factors=[
            "Separation method",
            "Fractionation train design",
            "Product purity",
            "GPA/API standards",
            "Integration with gas processing"
        ],
        primary_authority=[
            "GPA 2145: NGL Specifications",
            "API Technical Data Book, Section 6",
            "ASTM D1157"
        ],
        burden_holder="Gas Processor",
        adversary_position="Cryogenic processing is energy intensive",
        counter_arguments=[
            "Absorption/adsorption alternatives",
            "Product recovery trade-offs",
            "Integration with LNG",
            "Market volatility",
            "Spec changes"
        ],
        resolution_strategy="Balance energy use and recovery with market demand.",
        entity_scope="Gas Processing",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "GPA 2145", "API TDB", "ASTM D1157"
        ],
        issue_category=IssueCategory.NATURAL_GAS_PROCESSING
    ),
    DoctrineBlock(
        topic="Asphaltene Precipitation",
        keywords=["asphaltene", "precipitation", "onset", "ASTM D6560", "colloidal stability"],
        conclusion_template="Asphaltene precipitation is triggered by solubility changes, monitored by ASTM D6560.",
        reasoning_framework=rf_asphaltene_precipitation,
        key_factors=[
            "Solubility parameter",
            "Onset detection",
            "Fouling risk",
            "Resin/asphaltene ratio",
            "Blending strategies"
        ],
        primary_authority=[
            "ASTM D6560: Asphaltenes in Crude",
            "SPE 16978: Asphaltene Precipitation",
            "IP 143"
        ],
        burden_holder="Refinery",
        adversary_position="Onset detection methods vary",
        counter_arguments=[
            "Titration vs. microscopy",
            "Sample handling effects",
            "Blending can mask risk",
            "Alternative stability indices",
            "Measurement repeatability"
        ],
        resolution_strategy="Use multiple detection methods and validate with fouling monitoring.",
        entity_scope="Crude Oil",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ASTM D6560", "SPE 16978", "IP 143"
        ],
        issue_category=IssueCategory.ASPHALTENE_BEHAVIOR
    ),
    DoctrineBlock(
        topic="Conradson Carbon Residue (CCR)",
        keywords=["Conradson carbon residue", "ASTM D189", "coke", "fouling", "feedstock selection"],
        conclusion_template="CCR quantifies coke-forming tendency, guiding feedstock selection for FCC and coking.",
        reasoning_framework=rf_conradson_carbon_residue,
        key_factors=[
            "Measurement method (D189)",
            "Coke yield prediction",
            "Feedstock allocation",
            "Fouling risk",
            "Process optimization"
        ],
        primary_authority=[
            "ASTM D189: Conradson Carbon Residue",
            "API Technical Data Book, Section 3",
            "UOP 915"
        ],
        burden_holder="Refinery",
        adversary_position="CCR does not capture all fouling precursors",
        counter_arguments=[
            "Metals and asphaltenes also matter",
            "Measurement variability",
            "Process conditions affect coke",
            "Alternative indices (Ramsbottom)",
            "Feed blending"
        ],
        resolution_strategy="Combine CCR with metals and asphaltene analysis for feed selection.",
        entity_scope="Refinery",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ASTM D189", "API TDB", "UOP 915"
        ],
        issue_category=IssueCategory.COKING
    ),
    DoctrineBlock(
        topic="Fractionation",
        keywords=["fractionation", "distillation", "boiling point", "tray", "packing"],
        conclusion_template="Fractionation by distillation is fundamental to refining, optimizing yield and purity.",
        reasoning_framework=rf_fractionation,
        key_factors=[
            "Column design",
            "Reflux ratio",
            "Cut point selection",
            "Yield/purity optimization",
            "Process integration"
        ],
        primary_authority=[
            "Perry's Chemical Engineers' Handbook, Ch. 13",
            "API Technical Data Book, Section 2",
            "ASTM D2892"
        ],
        burden_holder="Refinery",
        adversary_position="Fractionation is energy intensive and has limited flexibility",
        counter_arguments=[
            "Energy costs are significant",
            "Column fouling affects performance",
            "Cut point flexibility limited by design",
            "Product overlap between cuts",
            "Requires continuous optimization"
        ],
        resolution_strategy="Optimize column operation and integrate with downstream processing.",
        entity_scope="Refinery",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Perry's Handbook", "API TDB", "ASTM D2892"
        ],
        issue_category=IssueCategory.REFINING_PROCESSES
    ),
]

# ================= THREE LAYER RESPONSE ===================

def doctrine_cache_search(scenario: str) -> List[DoctrineBlock]:
    hits = []
    scenario_lower = scenario.lower()
    for block in DOCTRINE_BLOCKS:
        for kw in block.keywords:
            if kw.lower() in scenario_lower:
                hits.append(block)
                break
    return hits

def semantic_search(scenario: str) -> List[DoctrineBlock]:
    scenario_norm = scenario.lower()
    for k, v in SEMANTIC_NORMALIZATION.items():
        scenario_norm = scenario_norm.replace(k.lower(), v.lower())
    hits = []
    for block in DOCTRINE_BLOCKS:
        for kw in block.keywords:
            if kw.lower() in scenario_norm:
                hits.append(block)
                break
    return hits

def deep_analysis(scenario: str, mode: ResponseMode) -> Tuple[Optional[DoctrineBlock], str, List[str], List[str], str, float, ConfidenceZone, PositionZone]:
    relevant = doctrine_cache_search(scenario)
    if not relevant:
        relevant = semantic_search(scenario)
    if not relevant:
        max_overlap = 0
        best = None
        words = set(scenario.lower().split())
        for block in DOCTRINE_BLOCKS:
            overlap = len(set(kw.lower() for kw in block.keywords).intersection(words))
            if overlap > max_overlap:
                max_overlap = overlap
                best = block
        if best:
            relevant = [best]
    if not relevant:
        relevant = [DOCTRINE_BLOCKS[0]]
    doctrine = relevant[0]
    reasoning = doctrine.reasoning_framework({})
    key_factors = doctrine.key_factors
    authorities = [a for a, _ in authority_hardening(doctrine.primary_authority)]
    resolution_strategy = doctrine.resolution_strategy
    confidence = doctrine.confidence
    confidence_zone = doctrine.confidence_zone
    position_zone = PositionZone.REPORTING
    return doctrine, reasoning, key_factors, authorities, resolution_strategy, confidence, confidence_zone, position_zone

# ================= COVERAGE MAP ===================

COVERAGE_MAP: Dict[str, Set[str]] = {"triggered": set(), "missed": set(), "epistemic_gap": set()}

def update_coverage(doctrine: DoctrineBlock, triggered: bool):
    if triggered:
        COVERAGE_MAP["triggered"].add(doctrine.topic)
    else:
        COVERAGE_MAP["missed"].add(doctrine.topic)

def detect_epistemic_gap(scenario: str):
    found = doctrine_cache_search(scenario)
    if not found:
        COVERAGE_MAP["epistemic_gap"].add(scenario)

# ================= DRIFT WATCHER ===================

DRIFT_BASELINE = {d.topic: d.confidence for d in DOCTRINE_BLOCKS}

def detect_drift() -> Dict[str, float]:
    drift = {}
    for d in DOCTRINE_BLOCKS:
        baseline = DRIFT_BASELINE.get(d.topic, 0)
        if abs(d.confidence - baseline) > 0.05:
            drift[d.topic] = d.confidence - baseline
    return drift

# ================= AUDIT TRAIL ===================

AUDIT_FILE = Path(__file__).parent / "chem08_audit_trail.jsonl"
AUDIT_LOCK = threading.Lock()

def log_audit_trail(entry: Dict[str, Any]):
    with AUDIT_LOCK:
        with open(AUDIT_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")

# ================= DETERMINISM HASH ===================

def compute_determinism_hash(response: Dict[str, Any]) -> str:
    resp_copy = dict(response)
    resp_copy.pop("determinism_hash", None)
    canonical = json.dumps(resp_copy, sort_keys=True, default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

# ================= FASTAPI APP ===================

app = FastAPI(title="Petroleum Chemistry Engine (CHEM08)", version="1.0.0", docs_url="/docs", redoc_url="/redoc")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def on_startup():
    logger.info("CHEM08 Petroleum Chemistry Engine starting up.")

@app.on_event("shutdown")
def on_shutdown():
    logger.info("CHEM08 Petroleum Chemistry Engine shutting down.")

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    query_id = str(uuid.uuid4())
    t0 = datetime.utcnow()
    try:
        doctrine, reasoning, key_factors, authorities, resolution_strategy, confidence, confidence_zone, position_zone = deep_analysis(
            request.scenario, request.mode)
        primary_conclusion = apply_epistemic_guardrails(doctrine.conclusion_template)
        reasoning_framework = apply_epistemic_guardrails(reasoning)
        fragility = score_fact_fragility(primary_conclusion)
        update_coverage(doctrine, True)
        response_dict = {
            "engine_id": "CHEM08",
            "query_id": query_id,
            "mode": request.mode,
            "confidence": confidence,
            "confidence_zone": confidence_zone,
            "position_zone": position_zone,
            "primary_conclusion": primary_conclusion,
            "reasoning_framework": reasoning_framework,
            "key_factors": key_factors,
            "primary_authority": authorities,
            "counter_arguments": doctrine.counter_arguments,
            "resolution_strategy": resolution_strategy,
            "determinism_hash": ""
        }
        determinism_hash = compute_determinism_hash(response_dict)
        response_dict["determinism_hash"] = determinism_hash
        t1 = datetime.utcnow()
        latency = (t1 - t0).total_seconds()
        metrics_collector.record_query([doctrine.topic], latency)
        log_audit_trail({
            "timestamp": t1.isoformat(),
            "query_id": query_id,
            "scenario": request.scenario,
            "mode": request.mode.value,
            "doctrine_topic": doctrine.topic,
            "confidence": confidence,
            "determinism_hash": determinism_hash
        })
        return QueryResponse(**response_dict)
    except Exception as e:
        metrics_collector.record_error(str(e))
        logger.error(f"Query error: {e}")
        raise

@app.get("/health")
async def health_endpoint():
    return {
        "status": "ok",
        "engine_id": "CHEM08",
        "version": "1.0.0",
        "doctrines_loaded": len(DOCTRINE_BLOCKS),
        "time": datetime.utcnow().isoformat()
    }

@app.get("/metrics")
async def metrics_endpoint():
    return {
        "latency_stats": metrics_collector.get_latency_stats(),
        "doctrine_hit_rate": metrics_collector.get_doctrine_hit_rate(),
        "queries_last_hour": metrics_collector.queries_last_hour(),
        "total_queries": len(metrics_collector.queries),
        "total_errors": len(metrics_collector.errors)
    }

@app.get("/coverage")
async def coverage_endpoint():
    return {
        "triggered": list(COVERAGE_MAP["triggered"]),
        "missed": list(COVERAGE_MAP["missed"]),
        "epistemic_gap": list(COVERAGE_MAP["epistemic_gap"])
    }

@app.get("/drift")
async def drift_endpoint():
    return detect_drift()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8499)
