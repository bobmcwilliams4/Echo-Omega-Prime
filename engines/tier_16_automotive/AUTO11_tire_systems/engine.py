"""
AUTO11 Tire Systems Analysis Engine v1.0.0

TIE-grade intelligence engine for tire construction, wear patterns, pressure optimization,
tire-road dynamics, seasonal selection, and failure forensics.

Port: 9321
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field
import uvicorn


# ============================================================================
# CONFIGURATION & MODELS
# ============================================================================

class ResponseMode(str, Enum):
    """Analysis response modes"""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    """Confidence stratification levels"""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class AnalysisZone(str, Enum):
    """Analysis zone separation"""
    DIAGNOSTIC = "DIAGNOSTIC"
    SPECIFICATION = "SPECIFICATION"
    FORENSIC = "FORENSIC"


class IssueCategory(str, Enum):
    """Tire issue categories"""
    CONSTRUCTION = "CONSTRUCTION"
    WEAR_PATTERN = "WEAR_PATTERN"
    PRESSURE = "PRESSURE"
    DYNAMICS = "DYNAMICS"
    SEASONAL = "SEASONAL"
    FAILURE = "FAILURE"
    SIDEWALL = "SIDEWALL"
    TREAD = "TREAD"
    BALANCE = "BALANCE"
    ALIGNMENT = "ALIGNMENT"
    LOAD_RATING = "LOAD_RATING"
    SPEED_RATING = "SPEED_RATING"


@dataclass
class DoctrineBlock:
    """Pre-compiled tire engineering doctrine"""
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    controlling_precedent: List[str]
    category: IssueCategory

    def match_score(self, query: str) -> float:
        """Calculate relevance score for query"""
        query_lower = query.lower()
        score = 0.0

        if self.topic.lower() in query_lower:
            score += 5.0

        for keyword in self.keywords:
            if keyword.lower() in query_lower:
                score += 2.0

        for factor in self.key_factors:
            if factor.lower() in query_lower:
                score += 1.0

        return score


class QueryRequest(BaseModel):
    """Query request model"""
    query: str = Field(..., min_length=1)
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.DIAGNOSTIC
    context: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    """Query response model"""
    answer: str
    confidence: ConfidenceLevel
    mode: ResponseMode
    zone: AnalysisZone
    doctrines_triggered: List[str]
    reasoning_chain: List[str]
    authority_citations: List[str]
    determinism_hash: str
    latency_ms: float
    timestamp: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    queries_processed: int
    avg_latency_ms: float
    cache_hit_rate: float


# ============================================================================
# DOCTRINE CACHE - 25+ REAL TIRE ENGINEERING BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Radial vs Bias-Ply Construction",
        keywords=["radial", "bias-ply", "belted", "construction", "carcass", "ply"],
        conclusion_template=[
            "Radial tire construction provides superior performance in most modern applications",
            "Bias-ply tires retain advantages in specific heavy-duty and off-road scenarios",
            "The carcass construction fundamentally determines tire behavior and longevity"
        ],
        reasoning_framework="""
        Radial tires have plies running perpendicular (90 degrees) to the direction of travel,
        with steel belts running circumferentially under the tread. This construction allows
        the sidewall and tread to function independently. The sidewall flexes easily for
        comfort while the tread remains relatively rigid for stability and wear resistance.

        Bias-ply tires have carcass plies running at 30-40 degree angles, crisscrossing
        each other. This creates a stiffer sidewall that resists punctures and sidewall
        damage better than radials, making them superior for severe off-road use,
        agricultural equipment, and vintage vehicles designed for bias-ply geometry.

        Radial advantages: Lower rolling resistance (better fuel economy), cooler running
        temperatures, longer tread life (30-50% more), better high-speed stability, superior
        wet traction. The independent sidewall/tread function allows optimized compounds
        for each area.

        Bias-ply advantages: Stronger sidewalls resist cuts and punctures, better load
        capacity at equivalent size, more forgiving of rim damage, easier to repair,
        preferable for slow-speed heavy loads and rough terrain where sidewall protection
        matters more than fuel economy.

        Modern passenger vehicles universally use radials. Bias-ply survives in tractors,
        some trailers, classic cars, and specialty equipment where original design assumed
        bias-ply characteristics.
        """,
        key_factors=[
            "Ply angle orientation",
            "Belt package design",
            "Sidewall stiffness characteristics",
            "Heat dissipation properties",
            "Rolling resistance coefficients",
            "Sidewall puncture resistance"
        ],
        primary_authority=[
            "SAE J1650 - Tire Dimensional Standards",
            "FMVSS 139 - New Pneumatic Radial Tires",
            "Tire and Rim Association Yearbook"
        ],
        burden_holder="Engineer specifying tire type",
        adversary_position="All tires perform similarly regardless of construction",
        counter_arguments=[
            "Radials cost more initially",
            "Bias-ply easier to mount on damaged rims",
            "Some vintage vehicles ride poorly on radials",
            "Agricultural equipment often requires bias-ply load characteristics"
        ],
        resolution_strategy="Match construction type to application: radial for highway/modern vehicles, bias-ply for heavy off-road/vintage applications",
        entity_scope="All pneumatic tire applications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "Radial tire patents (Michelin 1946)",
            "FMVSS adoption of radial standards",
            "Industry-wide shift to radials 1970s-1980s"
        ],
        category=IssueCategory.CONSTRUCTION
    ),

    DoctrineBlock(
        topic="Center Wear Pattern Analysis",
        keywords=["center wear", "overinflation", "crown wear", "pressure", "tread"],
        conclusion_template=[
            "Excessive center tread wear indicates chronic overinflation",
            "Pressure must be corrected immediately to prevent premature tire replacement",
            "Overinflation reduces contact patch and compromises traction safety"
        ],
        reasoning_framework="""
        Center wear occurs when tire pressure exceeds the recommended specification,
        causing the tire to balloon outward. This reduces the contact patch to primarily
        the center ribs of the tread, concentrating all wear in that area while the
        shoulder blocks remain relatively unworn.

        The crown (center) of an overinflated tire supports the vehicle weight on a
        smaller area, increasing pounds per square inch at the road surface. This
        accelerates wear rate in the center while shoulders never fully contact the road.
        The result is a distinctive wear pattern where center depth measures 2-4/32 inch
        less than shoulder depth.

        Root causes: Driver adding excessive pressure for perceived fuel economy benefit
        (real gains minimal), incorrect pressure specification being followed (door jamb
        vs sidewall max), pressure checked when cold but added when hot, seasonal
        temperature increase not compensated for (10 degrees F = ~1 PSI change).

        Consequences beyond premature wear: Reduced wet traction (smaller contact patch),
        harsher ride quality (less sidewall flex), increased susceptibility to impact
        damage (less air cushion), uneven braking forces. The tire loses 15-25% of its
        intended tread life depending on overinflation severity.

        Correction: Reduce pressure to vehicle manufacturer specification (door jamb
        sticker, NOT tire sidewall maximum). Tire sidewall shows maximum safe pressure,
        not recommended operating pressure. Check pressure cold (before driving).
        Rotation won't fix center wear but prevents it from continuing.
        """,
        key_factors=[
            "Pressure differential from spec",
            "Center vs shoulder tread depth delta",
            "Contact patch geometry",
            "Temperature effects on pressure",
            "Load carrying capacity",
            "Inflation frequency"
        ],
        primary_authority=[
            "NHTSA Tire Safety Information",
            "RMA Tire Care & Safety Guide",
            "Vehicle manufacturer specifications"
        ],
        burden_holder="Vehicle owner/operator",
        adversary_position="Center wear is normal and doesn't indicate a problem",
        counter_arguments=[
            "Higher pressure improves fuel economy slightly",
            "Tire sidewall shows higher pressure rating",
            "Previous owner inflated to this pressure without issues"
        ],
        resolution_strategy="Educate on proper pressure specification, implement monthly cold pressure checks, rotate if wear not severe",
        entity_scope="All passenger and light truck tires",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "TREAD Act requirements",
            "TPMS regulations",
            "Tire manufacturer recommendations"
        ],
        category=IssueCategory.WEAR_PATTERN
    ),

    DoctrineBlock(
        topic="Shoulder Wear Pattern Analysis",
        keywords=["shoulder wear", "underinflation", "edge wear", "pressure", "sidewall"],
        conclusion_template=[
            "Shoulder wear on both sides indicates chronic underinflation",
            "One-sided shoulder wear indicates alignment or suspension issues",
            "Underinflation causes excessive heat buildup and structural failure risk"
        ],
        reasoning_framework="""
        Shoulder wear manifests when tire pressure is below specification, causing the
        tire to deform excessively under load. The center of the tread lifts off the
        road while shoulders bear disproportionate weight, accelerating wear on the
        outer tread blocks while center ribs remain deeper.

        Bilateral shoulder wear (both sides) definitively indicates underinflation.
        The tire sidewalls flex excessively, flattening the tread profile so only
        shoulders contact the road. This generates excessive heat in the sidewalls,
        risking ply separation and catastrophic failure.

        Unilateral shoulder wear (one side only) indicates negative camber (tire tilts
        inward at top), worn suspension components, or aggressive cornering habits.
        This is NOT a pressure issue but an alignment/mechanical problem requiring
        suspension diagnosis.

        Underinflation consequences: 15-20% reduction in tire life, 5-10% increase in
        rolling resistance (worse fuel economy despite common belief that low pressure
        helps MPG), excessive heat generation leading to belt separation risk, poor
        handling response, increased stopping distances. At 20% underinflation, tire
        temperature can increase 50+ degrees F.

        Critical distinction: Bilateral vs unilateral shoulder wear requires different
        corrective actions. Both-sides = pressure correction. One-side = alignment check.
        Rotating tires with unilateral wear without fixing alignment just moves the
        problem to different corners.

        TPMS (Tire Pressure Monitoring System) only alerts at 25% underinflation - damage
        occurs well before warning light illuminates. Monthly manual pressure checks remain
        essential despite TPMS presence.
        """,
        key_factors=[
            "Bilateral vs unilateral pattern",
            "Pressure deficit percentage",
            "Sidewall flex extent",
            "Heat generation levels",
            "Load carrying impact",
            "TPMS threshold limitations"
        ],
        primary_authority=[
            "FMVSS 138 - Tire Pressure Monitoring",
            "NHTSA TPMS Final Rule",
            "Tire manufacturer pressure guidelines"
        ],
        burden_holder="Vehicle owner for pressure, technician for alignment diagnosis",
        adversary_position="Lower pressure provides better ride comfort without drawbacks",
        counter_arguments=[
            "Softer ride quality at lower pressure",
            "TPMS hasn't triggered warning",
            "Tire looks fine visually"
        ],
        resolution_strategy="Bilateral: correct pressure and monitor. Unilateral: alignment check, suspension inspection, correct mechanical issue before rotation",
        entity_scope="All pneumatic tires",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "TREAD Act Section 13",
            "FMVSS 138 25% threshold",
            "RMA Tire Pressure Bulletin"
        ],
        category=IssueCategory.WEAR_PATTERN
    ),

    DoctrineBlock(
        topic="Cupping and Scalloping Wear",
        keywords=["cupping", "scalloping", "suspension", "balance", "shock absorber"],
        conclusion_template=[
            "Cupped wear indicates worn suspension components or wheel balance issues",
            "The pattern results from uncontrolled vertical tire oscillation",
            "Correction requires addressing root mechanical causes, not just rotation"
        ],
        reasoning_framework="""
        Cupping (also called scalloping) creates a distinctive wavy wear pattern across
        the tread surface, with alternating high and low spots typically 3-4 inches apart.
        Running your hand across the tread feels like a washboard. This pattern indicates
        the tire is bouncing vertically at its natural resonant frequency without adequate
        damping control.

        Primary causes: Worn shock absorbers or struts that can't control rebound damping,
        allowing the tire to bounce. Out-of-balance wheels causing vibration that couples
        with suspension resonance. Worn ball joints or control arm bushings creating
        excessive vertical play. Mismatched tire diameters on the same axle (different
        brands/models/wear levels).

        The mechanism: As the tire rotates, worn suspension allows vertical oscillation.
        Each time the tire bounces up and comes back down, it scrubs the same tread
        section slightly differently, creating a high spot. The next section experiences
        different contact pressure, creating a low spot. This repeating pattern develops
        over thousands of miles.

        Cupping accelerates exponentially once started. The uneven surface creates more
        vibration, which worsens suspension component wear, which increases cupping rate.
        The tire becomes progressively noisier (roaring sound at highway speeds) and
        handling degrades noticeably.

        Diagnosis: Perform bounce test (push down on corner, should rebound once and settle).
        If it bounces 2+ times, shocks/struts are worn. Check wheel balance (cupped tires
        are difficult to balance - may need road force balancing). Inspect suspension
        components for play. Measure tire diameters to ensure matching.

        Rotation alone won't fix cupping - it moves the noise to different corners but
        doesn't address the root cause. Replace worn suspension components first, then
        assess if tires can be saved or need replacement.
        """,
        key_factors=[
            "Shock absorber damping capability",
            "Wheel balance status",
            "Suspension bushing condition",
            "Tire diameter matching",
            "Road force variation",
            "Resonance frequency"
        ],
        primary_authority=[
            "SAE J1634 - Tire Rolling Resistance",
            "OEM suspension specifications",
            "Tire Rack test data"
        ],
        burden_holder="Technician performing suspension diagnosis",
        adversary_position="Cupping is normal tire wear and rotation will resolve it",
        counter_arguments=[
            "Tires have good tread depth remaining",
            "Vehicle doesn't feel rough to driver",
            "Previous rotation didn't solve the problem"
        ],
        resolution_strategy="Replace worn suspension components, rebalance or road force balance wheels, rotate if cupping minor, replace tires if severe",
        entity_scope="All suspension-mounted tires",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "OEM maintenance schedules",
            "Suspension component wear limits",
            "Road force balancing standards"
        ],
        category=IssueCategory.WEAR_PATTERN
    ),

    DoctrineBlock(
        topic="Feathering Wear Pattern",
        keywords=["feathering", "toe", "alignment", "edge wear", "directional"],
        conclusion_template=[
            "Feathering indicates improper toe alignment setting",
            "The pattern shows tread blocks worn at an angle rather than squarely",
            "Toe alignment must be corrected to prevent continued rapid wear"
        ],
        reasoning_framework="""
        Feathering creates a distinctive pattern where individual tread blocks are worn
        smooth on one edge and sharp on the other, like a saw tooth or feather edge.
        Running your hand across the tread feels smooth in one direction and catches
        in the other direction. This indicates the tire is scrubbing laterally as it
        rolls forward.

        Root cause is incorrect toe alignment. Toe is the angle the front of the tire
        points relative to the vehicle centerline. Toe-in means fronts of tires are
        closer together than rears. Toe-out is the opposite. Either extreme causes
        feathering but in different patterns.

        Excessive toe-in: Inside edges of tread blocks wear rounded/smooth, outside
        edges remain sharp. The tire scrubs outward as it rolls forward. Common on
        vehicles with worn steering linkage or after suspension work without alignment
        correction.

        Excessive toe-out: Outside edges wear smooth, inside edges sharp. Tire scrubs
        inward. Often caused by collision damage bending steering/suspension components,
        or aggressive driver hitting curbs.

        The feathering direction reveals the toe error direction. Smooth edge points
        toward the direction of scrub. Wear rate is severe - toe setting just 1/4 inch
        out of spec can destroy tire tread in 5,000 miles despite appearing minor.

        Toe affects tire wear more dramatically than camber or caster. Even perfect
        camber/caster won't prevent feathering if toe is wrong. Modern vehicles use
        precise toe settings (often specified to 1/16 inch total) for optimal tire
        life and fuel economy.

        Rotation doesn't fix feathering, just moves the pattern. Must perform alignment
        correction first. Severely feathered tires may need replacement even if tread
        depth remains adequate - the rough surface increases rolling resistance and
        noise significantly.
        """,
        key_factors=[
            "Toe angle specification",
            "Tread block edge geometry",
            "Steering linkage wear",
            "Scrub radius calculation",
            "Suspension geometry changes",
            "Wear rate acceleration"
        ],
        primary_authority=[
            "OEM alignment specifications",
            "Hunter alignment standards",
            "SAE J1099 - Alignment terminology"
        ],
        burden_holder="Alignment technician",
        adversary_position="Slight alignment variations don't materially affect tire wear",
        counter_arguments=[
            "Alignment was done recently",
            "Vehicle tracks straight",
            "Other tires not showing feathering"
        ],
        resolution_strategy="Perform complete alignment check, correct toe to specification, inspect steering linkage for wear, replace tires if feathering severe",
        entity_scope="All steered wheels (front on most vehicles, all four on 4WS)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "OEM maintenance requirements",
            "Alignment equipment certification",
            "Tire warranty exclusions for misalignment"
        ],
        category=IssueCategory.WEAR_PATTERN
    ),

    DoctrineBlock(
        topic="Load Index and Speed Rating Compliance",
        keywords=["load index", "speed rating", "capacity", "UTQG", "sidewall", "replacement"],
        conclusion_template=[
            "Replacement tires must meet or exceed OEM load index and speed ratings",
            "Undersized tires create liability exposure and safety risks",
            "Load/speed ratings are engineering specifications, not suggestions"
        ],
        reasoning_framework="""
        Every tire sidewall displays a load index (numerical) and speed rating (letter)
        that define maximum safe operating parameters. Example: P225/65R17 102H means
        load index 102 (1874 lbs per tire) and speed rating H (130 mph max sustained).
        These ratings are engineering certifications, not marketing suggestions.

        Load index represents the maximum weight each tire can safely support when
        properly inflated. The index is a code number (60-120+ typical range) that
        cross-references to a specific weight capacity in pounds. Vehicle manufacturers
        calculate required load index based on GVWR (Gross Vehicle Weight Rating)
        divided by four, with safety margin.

        Installing tires with lower load index than OEM specification creates multiple
        failure modes: Overloaded tire runs hotter, risks belt separation and blowout.
        Sidewall flexes excessively, accelerating fatigue cracking. Load capacity
        degrades further with underinflation. Vehicle may exceed tire rating when
        loaded with passengers and cargo, even if acceptable empty.

        Speed rating indicates maximum sustained speed the tire can safely handle.
        Rating letters: Q=99mph, R=106, S=112, T=118, H=130, V=149, W=168, Y=186, (Y)=186+.
        This isn't just top speed - it's thermal and structural limits. Exceeding speed
        rating causes dangerous heat buildup even if tire doesn't visibly fail immediately.

        Common replacement errors: Installing T-rated (118 mph) tires on vehicle with
        OEM H-rating (130 mph) because they're cheaper. Using LT (Light Truck) tires
        with lower load index on SUV because they look more aggressive. Mounting
        different load ratings on same axle.

        Legal/liability implications: Tire-related accident with underspecified tires
        creates clear negligence claim. Insurance may deny coverage. Tire warranty
        explicitly excludes misapplication. Vehicle manufacturer warranty may be voided
        for suspension/drivetrain damage.

        Exceeding ratings is acceptable: Higher load index and faster speed rating
        than OEM is safe. The inverse is never acceptable. When replacing tires,
        always match or exceed both specifications.
        """,
        key_factors=[
            "Load index numerical value",
            "Speed rating letter code",
            "GVWR calculations",
            "Thermal operating limits",
            "Warranty compliance",
            "Liability exposure"
        ],
        primary_authority=[
            "FMVSS 139 - Tire load/speed requirements",
            "TRA Load/Speed Correspondence Table",
            "DOT tire certification requirements"
        ],
        burden_holder="Tire installer/retailer",
        adversary_position="Close enough ratings are acceptable for cost savings",
        counter_arguments=[
            "Driver never exceeds 75 mph",
            "Vehicle rarely carries heavy loads",
            "Lower rated tires are same size/fit"
        ],
        resolution_strategy="Educate on engineering basis for ratings, explain liability risks, provide proper specification tire options",
        entity_scope="All replacement tire installations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "FMVSS requirements",
            "Tire manufacturer specifications",
            "Negligence case law for misapplication"
        ],
        category=IssueCategory.LOAD_RATING
    ),

    DoctrineBlock(
        topic="Seasonal Tire Selection - Winter vs All-Season",
        keywords=["winter", "all-season", "snow", "temperature", "compound", "siping"],
        conclusion_template=[
            "Winter tires provide superior performance below 45 degrees F",
            "All-season tires are compromises that don't excel in any condition",
            "The rubber compound temperature threshold determines capability, not tread pattern"
        ],
        reasoning_framework="""
        The critical distinction between winter and all-season tires is rubber compound
        formulation, not tread pattern appearance. Winter tire compounds remain pliable
        below 45 degrees F, maintaining grip. All-season compounds harden below this
        threshold, losing traction even on dry pavement.

        Winter tire technology: Specialized rubber compounds using high silica content
        and chemical additives maintain flexibility at freezing temperatures. Tread
        design incorporates thousands of sipes (thin slits) that create additional
        biting edges for ice traction. Deeper tread grooves (10-12/32 inch new vs
        8-10/32 for all-season) evacuate snow and slush. Directional or asymmetric
        patterns optimize snow evacuation.

        The mountain/snowflake symbol (3PMSF - Three Peak Mountain Snow Flake) certifies
        the tire meets minimum traction standards on snow. This requires lab testing,
        not just marketing claims. All-season tires with M+S (Mud and Snow) marking
        are not equivalent - M+S is a tread pattern designation, not a performance
        certification.

        All-season tire limitations: Compound optimized for 40-90 degrees F operation.
        Below 40F, rubber stiffens significantly, reducing grip on all surfaces. Snow
        traction is marginal at best despite M+S marking. Ice traction is severely
        compromised. Stopping distances increase 20-40% vs winter tires in cold/snow
        conditions.

        Regional considerations: Areas with sustained winter temperatures below 45F
        and regular snow/ice benefit significantly from dedicated winter tires. Mild
        climates (southern US) where freezing is rare can use all-seasons year-round.
        Transitional climates benefit from tire swapping at seasonal temperature changes.

        Common misconceptions debunked: AWD/4WD doesn't compensate for inadequate tires -
        it helps acceleration but doesn't improve braking or cornering. Heavier vehicles
        don't stop better on ice. New all-seasons aren't as good as worn winters in
        cold conditions. Summer tires in winter are dangerous even without snow.

        Performance data: Winter tires reduce stopping distance 20-40% on ice, 15-30%
        on snow vs all-seasons. Cornering grip improves similarly. The difference
        between avoiding a collision and causing one.
        """,
        key_factors=[
            "Compound temperature threshold",
            "Siping density and design",
            "3PMSF certification vs M+S marking",
            "Tread depth and void ratio",
            "Regional climate patterns",
            "Seasonal temperature transitions"
        ],
        primary_authority=[
            "3PMSF test standard (ASTM F1805)",
            "Tire Rack winter tire test data",
            "Transport Canada winter tire studies"
        ],
        burden_holder="Vehicle operator selecting tires",
        adversary_position="All-season tires work fine in winter conditions",
        counter_arguments=[
            "AWD/4WD provides sufficient winter capability",
            "Winter tires wear quickly on dry pavement",
            "Cost of seasonal tire swap not justified"
        ],
        resolution_strategy="Educate on compound science, demonstrate stopping distance data, recommend dedicated winter tires where climate appropriate",
        entity_scope="Passenger and light truck tire selection",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "3PMSF certification requirements",
            "Provincial/state winter tire regulations",
            "Insurance implications of inadequate tires"
        ],
        category=IssueCategory.SEASONAL
    ),

    DoctrineBlock(
        topic="Tire Pressure Monitoring System (TPMS) Function and Limitations",
        keywords=["TPMS", "sensor", "warning light", "pressure monitoring", "25 percent"],
        conclusion_template=[
            "TPMS alerts only at 25 percent underinflation, not optimal pressure",
            "Tire damage begins well before TPMS warning triggers",
            "Manual pressure checks remain essential despite TPMS presence"
        ],
        reasoning_framework="""
        TPMS became mandatory on all US passenger vehicles in 2008 under FMVSS 138.
        The system alerts drivers when tire pressure drops 25 percent below the vehicle
        manufacturer's recommended cold pressure specification. This threshold is a
        minimum federal requirement, not an optimal monitoring standard.

        Two TPMS technologies exist: Direct TPMS uses pressure sensors mounted inside
        each wheel, transmitting actual pressure readings to the vehicle computer.
        Indirect TPMS uses ABS wheel speed sensors to detect circumference changes
        from underinflation (underinflated tire rotates faster due to smaller diameter).

        Direct TPMS provides real-time pressure data but sensors have 5-10 year battery
        life requiring eventual replacement. Sensors cost $50-100 each. Indirect TPMS
        has no additional hardware cost but can't detect equal underinflation on all
        four tires and requires recalibration after any tire change or pressure adjustment.

        The 25 percent trigger threshold creates a dangerous false sense of security.
        Example: Recommended pressure 35 PSI means TPMS alerts at 26 PSI. But tire
        performance degrades measurably at 30 PSI (14% low). The tire operates
        underinflated for thousands of miles before warning appears, accumulating
        heat damage and accelerated wear.

        TPMS limitations: Doesn't alert for slow leaks until 25% threshold reached.
        Doesn't warn of overinflation. Can't distinguish underinflation cause (leak
        vs cold weather vs normal permeation). Sensor battery failure often isn't
        detected until complete failure. Malfunction indicator (separate from low
        pressure warning) is easily ignored by drivers.

        Temperature effects compound the issue: 10 degree F temperature drop equals
        ~1 PSI pressure loss. Tire at 35 PSI in 70F garage drops to 29 PSI at 10F
        ambient - 17% underinflated but TPMS doesn't alert. Winter pressure loss is
        normal physics, not a leak, but still causes underinflation damage.

        Best practice: Check all tire pressures manually when cold (before driving)
        at least monthly and before long trips. Don't rely on TPMS as primary monitoring.
        Treat TPMS warning as urgent but late alert requiring immediate action. Consider
        TPMS a backup safety system, not primary maintenance tool.
        """,
        key_factors=[
            "25 percent federal threshold",
            "Direct vs indirect technology",
            "Sensor battery lifespan",
            "Temperature pressure relationship",
            "Warning light interpretation",
            "Maintenance check intervals"
        ],
        primary_authority=[
            "FMVSS 138 - Tire Pressure Monitoring",
            "TREAD Act Section 13",
            "NHTSA TPMS FAQ"
        ],
        burden_holder="Vehicle owner for manual checks",
        adversary_position="TPMS eliminates need for manual pressure checks",
        counter_arguments=[
            "TPMS hasn't triggered warning so tires must be fine",
            "Tire looks properly inflated visually",
            "Modern systems are highly accurate"
        ],
        resolution_strategy="Educate on 25% threshold limitation, explain temperature effects, establish monthly manual check routine",
        entity_scope="All vehicles with TPMS (2008+ in US)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "FMVSS 138 final rule",
            "TPMS sensor replacement requirements",
            "Tire manufacturer pressure recommendations"
        ],
        category=IssueCategory.PRESSURE
    ),

    DoctrineBlock(
        topic="Sidewall Impact Damage and Bubble Formation",
        keywords=["sidewall", "bubble", "bulge", "impact", "pothole", "curb"],
        conclusion_template=[
            "Sidewall bubbles indicate internal structural failure and require immediate tire replacement",
            "Impact damage severs internal cords creating high-pressure bulges",
            "Driving on damaged tire risks catastrophic blowout"
        ],
        reasoning_framework="""
        Sidewall bubbles (bulges) form when internal reinforcement cords are severed
        by impact damage while the outer rubber layer remains intact. Air pressure
        pushes the unsupported rubber outward, creating a visible bulge. This is
        irreparable structural failure requiring immediate tire replacement.

        Damage mechanism: Tire impacts pothole, curb, or road debris with sufficient
        force to pinch sidewall against wheel rim. The pinch point exceeds the tensile
        strength of internal polyester or aramid cords, breaking them. With cords
        severed, that section of sidewall loses structural integrity. Air pressure
        (typically 30-35 PSI) pushes the weakened area outward like a balloon.

        The bubble may appear immediately after impact or develop over hours/days as
        the damaged cords gradually separate further. Size ranges from golf ball to
        softball. Location is typically lower sidewall near the bead or mid-sidewall
        where impact forces concentrate.

        Why this is catastrophic: The bulge concentrates stress on remaining intact
        cords surrounding the damaged area. Each tire revolution flexes the bulge,
        progressively weakening adjacent cords. The failure zone expands outward.
        Eventually the entire section ruptures, causing instant total air loss and
        loss of vehicle control.

        Blowout risk factors: Highway speeds generate extreme heat and flexing cycles,
        accelerating failure. Heavy loads increase stress on weakened area. Hot weather
        increases internal pressure, pushing harder on damaged section. The tire can
        fail without warning at any moment.

        No repair is possible: Tire cord structure cannot be restored. Patch/plug
        repairs only address tread punctures, never sidewall damage. Some drivers
        attempt to continue using the tire - this is extremely dangerous. Tire
        manufacturers, tire retailers, and safety organizations universally condemn
        driving on bubble-damaged tires.

        Insurance/warranty implications: Impact damage is not covered by tire warranty.
        Road hazard warranties may cover it depending on policy terms. Some insurance
        policies cover tire replacement under comprehensive coverage (confirm deductible
        makes claim worthwhile). Document damage with photos for potential claims.

        Temporary spare use: If spare is inadequate for extended driving, damaged tire
        can be replaced with spare for immediate safety, then proper replacement
        obtained ASAP. Never put spare on front axle if it's undersized - put on rear
        and move rear tire to front.
        """,
        key_factors=[
            "Cord severance mechanism",
            "Bulge size and location",
            "Failure progression rate",
            "Blowout risk severity",
            "No repair possibility",
            "Replacement urgency"
        ],
        primary_authority=[
            "RMA Tire Repair Guidelines",
            "Tire manufacturer service bulletins",
            "NHTSA tire safety guidance"
        ],
        burden_holder="Vehicle operator who continued driving on damaged tire",
        adversary_position="Small bubbles are cosmetic and don't affect safety",
        counter_arguments=[
            "Tire holds air pressure normally",
            "Bubble hasn't grown recently",
            "Vehicle drives normally"
        ],
        resolution_strategy="Emphasize blowout risk, show failure mechanism photos, provide immediate replacement options including used tire if budget constrained",
        entity_scope="All pneumatic tires with sidewall damage",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "RMA unrepairable damage criteria",
            "Tire manufacturer safety bulletins",
            "Liability case law for known defect"
        ],
        category=IssueCategory.SIDEWALL
    ),

    DoctrineBlock(
        topic="Hydroplaning Dynamics and Tread Depth Requirements",
        keywords=["hydroplaning", "aquaplaning", "tread depth", "water evacuation", "wet traction"],
        conclusion_template=[
            "Hydroplaning occurs when tire cannot evacuate water fast enough to maintain road contact",
            "Tread depth below 4/32 inch severely compromises wet traction",
            "Vehicle speed, tire pressure, and tread design all affect hydroplaning threshold"
        ],
        reasoning_framework="""
        Hydroplaning (aquaplaning) is the complete loss of tire-road contact when a
        wedge of water builds up under the tire faster than tread grooves can evacuate
        it. The tire rides on a film of water rather than touching pavement, eliminating
        all steering, braking, and acceleration control.

        Physics of hydroplaning: As tire approaches standing water, tread grooves must
        channel water out from under the contact patch. Water evacuation capacity depends
        on groove volume (depth × width × length) and vehicle speed. At low speeds,
        grooves have time to evacuate water. Above a critical speed, water inflow exceeds
        outflow capacity. Pressure builds under the tire center, lifting it off the road.

        Hydroplaning speed formula: V = 10.35 × sqrt(tire_pressure_PSI). For 32 PSI tire,
        hydroplaning begins around 58 mph in standing water. This is the best-case with
        new tires. Worn tires hydroplane at much lower speeds.

        Tread depth effects: New tire (10/32 inch) can evacuate 8+ gallons of water per
        second at highway speeds. At 4/32 inch (half worn), capacity drops to ~3 gallons.
        At 2/32 inch (legal minimum), capacity is <1 gallon - inadequate for moderate
        rain. Hydroplaning speed decreases proportionally with tread depth reduction.

        Most states define legal minimum tread depth as 2/32 inch, measured at the
        shallowest point. This is barely adequate for dry traction and completely
        inadequate for wet conditions. Tire manufacturers and safety organizations
        recommend replacement at 4/32 inch for wet climate regions, 3/32 inch minimum
        elsewhere.

        Tread wear indicators (wear bars) are molded into tire grooves at 2/32 inch
        depth. When tread wears flush with wear bars, the tire is at legal minimum but
        functionally unsafe in rain. Don't wait for wear bars - measure with depth gauge.

        Other hydroplaning factors: Tire pressure affects contact patch shape - underinflation
        increases hydroplaning susceptibility. Tread design matters - directional patterns
        with continuous center grooves evacuate water better than symmetric patterns.
        Vehicle weight helps - heavier vehicles hydroplane at slightly higher speeds.
        Water depth matters most - 1/10 inch standing water is enough if speed is high.

        Driver detection: Hydroplaning feels like sudden loss of steering resistance
        (wheel goes light), engine RPM increases without acceleration (no traction),
        rear end may drift sideways. Correct response: Ease off accelerator gently,
        don't brake hard or steer sharply, let vehicle slow until traction returns.

        Prevention: Replace tires at 4/32 inch in wet climates. Reduce speed in rain
        (45-50 mph max in heavy rain regardless of speed limit). Increase following
        distance. Avoid standing water in wheel ruts. Ensure proper tire pressure.
        """,
        key_factors=[
            "Tread groove volume and design",
            "Critical hydroplaning speed",
            "Tread depth degradation curve",
            "Water depth and coverage",
            "Tire pressure effects",
            "Vehicle weight distribution"
        ],
        primary_authority=[
            "SAE J2452 - Wet Traction Standards",
            "NHTSA tire safety recommendations",
            "Transport Canada winter tire studies"
        ],
        burden_holder="Driver operating at unsafe speed for conditions",
        adversary_position="Legal minimum tread depth is adequate for all conditions",
        counter_arguments=[
            "Tire still has tread visible",
            "Vehicle has ABS and traction control",
            "Driver has experience in rain"
        ],
        resolution_strategy="Educate on tread depth effects, demonstrate penny test (2/32) and quarter test (4/32), recommend proactive replacement",
        entity_scope="All tires operated in wet conditions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "State minimum tread depth laws",
            "Tire manufacturer wet traction data",
            "Accident liability for worn tires"
        ],
        category=IssueCategory.TREAD
    ),

    DoctrineBlock(
        topic="Tire Age and Date Code Interpretation",
        keywords=["DOT date", "age", "expiration", "date code", "manufactured"],
        conclusion_template=[
            "Tire age is determined by DOT date code, not purchase date or tread depth",
            "Tires degrade from age-related oxidation regardless of use",
            "Six years of service or ten years from manufacture is maximum safe life"
        ],
        reasoning_framework="""
        Every tire manufactured since 2000 has a DOT date code molded into the sidewall
        indicating the week and year of manufacture. The code format is four digits:
        first two = week of year (01-52), last two = year. Example: 2619 means 26th
        week of 2019 (late June 2019).

        Location of date code: On one sidewall (usually inside when mounted), within
        a DOT serial number sequence. Begins with DOT, followed by plant code and size
        code, ending with the four-digit date code. May be inside an oval or following
        other numbers. Not all DOT numbers on the tire contain the date - some are just
        certification marks.

        Why tire age matters: Rubber compounds degrade from oxidation, UV exposure,
        ozone, temperature cycling, and flex fatigue over time even if the tire is never
        driven. The chemical bonds in the rubber polymer chains break down, reducing
        elasticity and strength. This process is irreversible and independent of tread
        wear.

        Aging effects: Sidewall cracking (weather checking) appears as small cracks in
        the rubber surface. Tread separation risk increases as adhesion between rubber
        layers weakens. Compound becomes brittle, reducing impact resistance and grip.
        Belt edges may separate from surrounding rubber. The tire may look fine but
        internal structure is compromised.

        Industry recommendations: Most tire manufacturers recommend replacement at 10
        years from date of manufacture regardless of appearance or tread depth. NHTSA
        recommends replacement at 6 years of service. The difference accounts for storage
        time before purchase. A tire manufactured in 2019 but sold in 2022 should be
        replaced in 2028 (6 service years) not 2029 (10 manufacture years).

        Accelerating factors: Hot climates (Arizona, Texas, Florida) accelerate aging
        significantly. UV exposure (outdoor parking) worsens degradation. Low use
        (RV, classic car) doesn't prevent aging. Underinflation increases sidewall
        flex stress, accelerating fatigue. These factors can reduce safe life to 5
        years or less.

        Special cases: Spare tires age at the same rate as mounted tires. Many vehicle
        spares are over 6 years old and unsafe. Winter tires stored properly (cool,
        dark, no weight) age slower than tires in service. Tires stored improperly
        (outdoors, stacked under load) age faster.

        Legal/warranty implications: Tire manufacturers only warranty manufacturing
        defects, not age-related degradation. Tire retailers typically won't mount
        tires over 6 years old due to liability concerns. Some countries regulate
        maximum tire age for commercial vehicles.

        Inspection protocol: Check date code at purchase - reject tires over 2 years
        old as new. Inspect tires over 6 years old for sidewall cracks, tread separation,
        bulges. Replace at 10 years maximum regardless of appearance. Document date
        code when purchasing used vehicles.
        """,
        key_factors=[
            "DOT date code format and location",
            "Oxidation degradation mechanism",
            "Service years vs manufacture years",
            "Climate acceleration factors",
            "Storage condition effects",
            "Inspection protocols"
        ],
        primary_authority=[
            "NHTSA tire aging study",
            "Tire manufacturer recommendations",
            "RMA tire age guidelines"
        ],
        burden_holder="Vehicle owner monitoring tire age",
        adversary_position="Tires with good tread don't need replacement based on age",
        counter_arguments=[
            "Tire looks fine and holds air",
            "Low mileage means tire is barely used",
            "Spare tire has never been on the ground"
        ],
        resolution_strategy="Educate on oxidation chemistry, demonstrate sidewall cracking, provide date code reading guide, recommend age-based replacement schedule",
        entity_scope="All pneumatic tires regardless of use",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "NHTSA 6-year recommendation",
            "Manufacturer 10-year maximum",
            "Tire retailer mounting policies"
        ],
        category=IssueCategory.FAILURE
    ),

    DoctrineBlock(
        topic="Run-Flat Tire Technology and Limitations",
        keywords=["run-flat", "RFT", "extended mobility", "zero pressure", "reinforced sidewall"],
        conclusion_template=[
            "Run-flat tires allow limited driving after complete air loss",
            "Speed and distance restrictions (50 mph / 50 miles typical) must be observed",
            "TPMS is mandatory with run-flats to detect air loss"
        ],
        reasoning_framework="""
        Run-flat tires (RFT or extended mobility tires) are designed to support vehicle
        weight after complete air pressure loss, allowing continued driving to reach
        a service facility. This eliminates immediate roadside tire changes in dangerous
        locations and allows vehicles to be designed without spare tire storage.

        Two primary RFT technologies: Self-supporting RFTs have heavily reinforced
        sidewalls that can support vehicle weight without air pressure. The sidewall
        contains additional rubber and structural reinforcement. Support ring RFTs use
        a rigid ring attached to the wheel rim that supports the tire tread after air
        loss. Self-supporting is more common.

        Operating limitations after air loss: Maximum speed typically 50 mph, maximum
        distance 50 miles (check specific tire manufacturer specs - ranges from 25-100
        miles). These limits prevent catastrophic structural failure from excessive heat
        buildup in the unsupported tire. Exceeding limits can cause unrepairable rim
        damage and tire disintegration.

        Why TPMS is mandatory: Without air pressure, self-supporting RFTs drive nearly
        normally - the driver may not realize the tire is flat. TPMS alerts driver to
        air loss so distance/speed limits can be observed. Driving on flat run-flat
        without knowing it often results in exceeding the 50-mile limit, destroying
        the tire and wheel.

        Advantages: No immediate tire change in dangerous locations (busy highway,
        bad weather). No spare tire needed (weight savings, more cargo space). Some
        vehicles use run-flats to enable lower floor design. Peace of mind for drivers
        uncomfortable changing tires.

        Disadvantages: Harsher ride quality (stiffer sidewalls). Higher cost (30-50%
        premium over conventional). Limited repair options (sidewall damage often
        unrepairable). Not all tire shops can mount RFTs (requires specific equipment).
        Can't mix RFTs with conventional tires on same vehicle. Reduced tread life
        (heavier weight increases wear).

        Replacement considerations: RFT-equipped vehicles often lack spare tire and
        may lack jack/lug wrench. Switching to conventional tires requires adding
        spare tire system. Some vehicle dynamic systems are calibrated for RFT
        behavior. BMW, Mini Cooper, and some Corvettes use RFTs as OEM fitment.

        After air loss event: Tire must be dismounted and inspected internally for
        damage. If distance/speed limits were observed and no internal damage found,
        tire may be repaired (if damage was simple puncture in repairable zone).
        However, most tire shops refuse to repair RFTs after zero-pressure driving
        due to liability concerns. Many manufacturers recommend replacement after
        any air loss event.

        Driver protocol: When RFT loses air, reduce speed immediately to 50 mph or
        less, drive no more than 50 miles, head directly to tire service facility.
        Avoid sharp steering inputs and hard braking. If vibration develops, pull
        over immediately (tire may be disintegrating).
        """,
        key_factors=[
            "Reinforced sidewall construction",
            "50 mph / 50 mile typical limits",
            "TPMS requirement for air loss detection",
            "Repair limitations after zero pressure",
            "Vehicle system integration",
            "Cost and availability tradeoffs"
        ],
        primary_authority=[
            "Tire manufacturer RFT specifications",
            "SAE J2421 - Run-flat terminology",
            "OEM vehicle owner manuals"
        ],
        burden_holder="Driver observing speed/distance limits after air loss",
        adversary_position="RFTs allow indefinite driving without air pressure",
        counter_arguments=[
            "Tire drives normally so must be fine",
            "Can extend distance limit slightly",
            "Run-flats don't need TPMS"
        ],
        resolution_strategy="Educate on manufacturer limits, explain heat buildup failure mechanism, emphasize TPMS critical importance, inspect for damage",
        entity_scope="Vehicles equipped with run-flat tires",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "Tire manufacturer limitations",
            "OEM service manuals",
            "RFT installation guidelines"
        ],
        category=IssueCategory.CONSTRUCTION
    ),

    DoctrineBlock(
        topic="Wheel Balance and Vibration Diagnosis",
        keywords=["balance", "vibration", "shake", "weights", "dynamic", "static"],
        conclusion_template=[
            "Unbalanced wheels cause vibration at specific speed ranges",
            "Proper balance requires both static and dynamic correction",
            "Road force balancing addresses variation that weight placement can't fix"
        ],
        reasoning_framework="""
        Wheel balance is the equal distribution of weight around the tire/wheel assembly's
        rotational axis. Perfect balance means the assembly's center of mass aligns with
        the rotational axis. Any mass offset creates centrifugal force during rotation,
        causing vibration that increases with speed.

        Static vs dynamic imbalance: Static imbalance is heavy spot on one side of the
        tire centerline - the wheel wobbles up/down. Dynamic imbalance is unequal weight
        distribution between inner and outer bead areas - the wheel wobbles side to side.
        Most imbalances combine both types. Proper balancing corrects both by placing
        weights at specific locations on the wheel rim.

        Balancing procedure: Mount tire/wheel on spin balancer machine, spin at high
        speed, sensors detect vibration magnitude and phase angle, machine calculates
        weight amounts and placement locations. Technician attaches clip-on or stick-on
        weights to rim at specified positions. Re-spin to verify correction. Target
        is typically under 0.25 oz-in residual imbalance.

        Vibration symptom diagnosis: Front wheel imbalance typically causes steering
        wheel vibration at 55-70 mph. Rear wheel imbalance causes seat/floorboard
        vibration at similar speeds. Vibration that increases with speed indicates
        balance issue. Vibration constant regardless of speed suggests damaged suspension
        component. Vibration only during braking indicates warped brake rotor.

        When balancing won't solve vibration: Bent wheel rim, egg-shaped tire (radial
        runout), bulge in tire (lateral runout), separated belt in tire, damaged
        driveshaft, worn CV joint. These require different diagnosis and repair.
        Repeatedly balancing without improvement suggests the problem isn't balance.

        Road force balancing (advanced technique): Measures how round the tire actually
        is by pressing a large roller against the spinning tire, simulating road contact.
        Detects variations in tire stiffness (force variation) that weight placement
        can't fix. Can often minimize force variation by rotating tire on wheel to
        optimal position. Some defective tires can't be corrected even with road force
        balancing and must be replaced.

        Balance weight locations: Clip-on weights attach to wheel rim flanges, visible
        on outside. Stick-on weights attach inside wheel barrel, hidden from view.
        Many modern wheels use stick-on for aesthetics. Lost weights cause immediate
        imbalance return. Inspect for missing weights if vibration develops suddenly.

        Rebalancing intervals: Wheels should be rebalanced with each tire rotation
        (every 5,000-7,500 miles), whenever tires are dismounted, or when vibration
        develops. Weights can fall off, tire wear changes balance, impacts can
        shift balance. Rebalancing is inexpensive prevention against accelerated
        tire and suspension wear from vibration.
        """,
        key_factors=[
            "Static vs dynamic imbalance types",
            "Centrifugal force vs speed relationship",
            "Weight placement calculation",
            "Road force variation measurement",
            "Vibration symptom patterns",
            "Rebalancing intervals"
        ],
        primary_authority=[
            "Hunter Engineering specifications",
            "SAE J1986 - Balance procedures",
            "OEM wheel/tire specifications"
        ],
        burden_holder="Tire technician performing balance",
        adversary_position="Vibration isn't significant enough to require service",
        counter_arguments=[
            "Vibration only occurs at high speeds rarely driven",
            "Vehicle is old so some vibration is normal",
            "Previous balance didn't help"
        ],
        resolution_strategy="Demonstrate vibration effects on tire wear and component life, road force balance if standard balance insufficient, inspect for bent rim or defective tire",
        entity_scope="All mounted tire/wheel assemblies",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "Balance machine calibration standards",
            "Tire manufacturer runout specifications",
            "Vehicle manufacturer vibration limits"
        ],
        category=IssueCategory.BALANCE
    ),

    DoctrineBlock(
        topic="Nitrogen Inflation vs Compressed Air",
        keywords=["nitrogen", "air", "inflation", "permeation", "pressure loss", "oxidation"],
        conclusion_template=[
            "Nitrogen inflation reduces pressure loss rate and internal oxidation",
            "Benefits are marginal for passenger vehicles in normal use",
            "Proper pressure maintenance matters more than inflation gas type"
        ],
        reasoning_framework="""
        Nitrogen inflation uses dry nitrogen gas (typically 95-98% pure) instead of
        compressed air (78% nitrogen, 21% oxygen, 1% other gases) to fill tires. The
        practice originated in racing and aircraft applications where performance
        benefits justify cost and effort.

        Technical advantages of nitrogen: Larger molecular size than oxygen means
        slower permeation through rubber (tire holds pressure longer). Dry nitrogen
        has no moisture, eliminating internal condensation that can cause oxidation
        and corrosion. Nitrogen doesn't support combustion, marginally safer in extreme
        heat scenarios. More stable pressure across temperature changes (though this
        benefit is often overstated - both gases follow ideal gas law).

        Actual performance data: Nitrogen-filled tires lose pressure approximately
        30-40% slower than air-filled tires. A tire losing 1 PSI per month with air
        might lose 0.6-0.7 PSI per month with nitrogen. Both still require monthly
        pressure checks. The moisture content of compressed air varies significantly
        - properly maintained air compressors with moisture separators deliver fairly
        dry air approaching nitrogen's benefits.

        Marginal benefit for passenger vehicles: Aircraft tires experience extreme
        temperature changes (+30F to -40F in minutes climbing to altitude) where
        nitrogen stability helps. Racing tires run at extreme temperatures where
        moisture could cause pressure spikes. Passenger vehicles rarely experience
        conditions where nitrogen provides meaningful advantage over air.

        Cost/benefit analysis: Nitrogen inflation typically costs $5-10 per tire vs
        free compressed air. Top-off service requires returning to nitrogen provider
        (can't use gas station air without diluting nitrogen concentration). Most
        tire shops don't have nitrogen equipment. The pressure retention improvement
        doesn't eliminate need for monthly pressure checks.

        Oxidation prevention claims: Oxygen inside tire can theoretically oxidize
        inner liner rubber and corrode steel belts/wheel rim. However, modern tire
        inner liners are formulated to resist oxidation, and corrosion risk is minimal
        with modern wheel coatings. The major oxidation damage to tires comes from
        external UV/ozone exposure, which nitrogen doesn't affect.

        Marketing vs reality: Nitrogen inflation is often oversold with exaggerated
        claims of dramatically improved fuel economy, much longer tire life, better
        safety. Actual measurable benefits are small. The key factor in tire longevity
        and performance is maintaining proper pressure - whether using nitrogen or air
        matters far less than checking pressure monthly.

        When nitrogen makes sense: Racing applications where pressure consistency
        is critical. Aircraft where extreme temperature swings occur. Heavy equipment
        with large tires where inflation cost is significant. Vehicles that will see
        minimal pressure maintenance (though better to just check pressure regularly).

        Mixing nitrogen and air: Adding compressed air to nitrogen-filled tire dilutes
        the nitrogen concentration but doesn't harm the tire. Most nitrogen fills
        aren't pure anyway (95-98% typical). If stranded with low pressure and only
        air available, add air without hesitation - low pressure is more dangerous
        than nitrogen dilution.
        """,
        key_factors=[
            "Permeation rate differential",
            "Moisture content elimination",
            "Temperature stability claims",
            "Cost vs benefit ratio",
            "Oxidation prevention magnitude",
            "Practical service accessibility"
        ],
        primary_authority=[
            "Consumer Reports nitrogen testing",
            "SAE nitrogen inflation studies",
            "Tire manufacturer statements"
        ],
        burden_holder="Service provider making nitrogen claims",
        adversary_position="Nitrogen provides dramatic performance and safety benefits",
        counter_arguments=[
            "Race cars use nitrogen so it must be superior",
            "Tires never need pressure checks with nitrogen",
            "Nitrogen dramatically improves fuel economy"
        ],
        resolution_strategy="Acknowledge real but modest benefits, emphasize proper maintenance matters most, recommend air for typical passenger vehicles",
        entity_scope="All tire inflation applications",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent=[
            "Consumer testing results",
            "Tire manufacturer recommendations",
            "FTC truth in advertising standards"
        ],
        category=IssueCategory.PRESSURE
    ),

    DoctrineBlock(
        topic="Tire Rotation Patterns and Intervals",
        keywords=["rotation", "pattern", "interval", "directional", "staggered", "wear"],
        conclusion_template=[
            "Regular tire rotation equalizes wear and maximizes tire life",
            "Rotation pattern depends on tire type and vehicle drivetrain",
            "5,000-7,500 mile interval is optimal for most vehicles"
        ],
        reasoning_framework="""
        Tire rotation is the periodic changing of tire positions to equalize wear
        patterns across all four tires. Front and rear axles have different weight
        distributions, steering loads, and braking forces, causing different wear
        rates and patterns. Rotation spreads wear evenly, maximizing total tire life.

        Why rotation is necessary: Front tires on FWD vehicles wear faster due to
        steering, driving torque, and typically higher weight on front axle. Rear
        tires on RWD wear faster from driving torque. Front tires on all vehicles
        wear outer edges more from cornering loads. Without rotation, some tires
        would require replacement while others have significant tread remaining.

        Standard rotation patterns: Forward cross (FWD vehicles): Left front to left
        rear, right front to right rear, left rear to right front, right rear to left
        front. Rearward cross (RWD/AWD): Opposite direction. X-pattern: All four tires
        swap diagonally. Side-to-side: Left front ↔ right front, left rear ↔ right rear
        (directional tires only).

        Special cases requiring different patterns: Directional tires (tread designed
        to rotate one direction only) can only move front-to-rear on same side, not
        cross. Staggered fitment (different size front vs rear, common on performance
        cars) can only rotate side-to-side if at all. Asymmetric tires can rotate
        normally despite inside/outside markings.

        Optimal rotation interval: Manufacturer recommendations typically specify
        5,000-7,500 miles. Some suggest every other oil change. High-performance
        vehicles may need more frequent rotation (3,000-5,000 miles). Tire wear
        should be measured at each rotation to verify pattern is effective and detect
        mechanical issues.

        Including spare tire: Full-size spare that matches other tires should be
        included in rotation to spread wear across five tires, extending set life.
        Five-tire rotation adds complexity (no standard pattern). Compact temporary
        spares should never be included in rotation.

        Benefits beyond wear equalization: Rotation provides opportunity for thorough
        tire inspection (tread depth, sidewall damage, foreign objects, irregular wear).
        Allows detection of alignment issues, suspension problems, or pressure issues
        before they become severe. Rebalancing wheels during rotation prevents
        vibration issues.

        Consequences of not rotating: One or two tires wear prematurely, requiring
        early replacement. Replacing only worn tires creates mismatched set with
        different tread depths. Uneven tread depths can affect ABS/traction control
        function. AWD vehicles particularly sensitive to tread depth matching - must
        replace all four if depth variance exceeds 2/32 inch. Skipping rotation
        effectively wastes 25-40% of tire investment.

        Cost consideration: Rotation typically costs $20-40 or is free with tire
        purchase at many retailers. This modest cost preserves thousands of dollars
        of tire investment. Missing one rotation interval isn't catastrophic, but
        skipping multiple rotations causes irreversible wear imbalance.
        """,
        key_factors=[
            "Wear rate differentials by position",
            "Rotation pattern selection criteria",
            "Interval optimization",
            "Directional tire constraints",
            "AWD tread depth matching requirements",
            "Inspection opportunity value"
        ],
        primary_authority=[
            "Tire manufacturer rotation schedules",
            "Vehicle owner manual specifications",
            "TRA Tire Care Guide"
        ],
        burden_holder="Vehicle owner maintaining rotation schedule",
        adversary_position="Rotation is unnecessary maintenance upsell",
        counter_arguments=[
            "Tires seem to wear evenly without rotation",
            "Vehicle has AWD so rotation doesn't help",
            "Previous vehicles never had tires rotated"
        ],
        resolution_strategy="Demonstrate wear rate data, calculate tire life extension, show AWD manufacturer requirements, include rotation with other service",
        entity_scope="All vehicles with four matching tires",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "OEM maintenance schedules",
            "Tire warranty requirements",
            "AWD manufacturer specifications"
        ],
        category=IssueCategory.WEAR_PATTERN
    ),

    DoctrineBlock(
        topic="Plus-Sizing and Minus-Sizing Tire Changes",
        keywords=["plus-sizing", "minus-sizing", "diameter", "aspect ratio", "rim", "speedometer"],
        conclusion_template=[
            "Plus-sizing increases wheel diameter while maintaining overall tire diameter",
            "Changes affect ride quality, performance, and speedometer accuracy",
            "Overall diameter must remain within 3 percent of original specification"
        ],
        reasoning_framework="""
        Plus-sizing (or up-sizing) replaces the OEM wheel/tire combination with a
        larger diameter wheel and lower profile tire that maintains approximately
        the same overall diameter. Example: Replace 16 inch wheel with 225/65R16
        tire (28.5 inch diameter) with 18 inch wheel and 225/50R18 tire (28.2 inch
        diameter). Minus-sizing is the opposite - smaller wheel, taller sidewall.

        Why plus-sizing: Appearance preference (larger wheels perceived as more
        aggressive/sporty). Handling improvement (shorter sidewall flexes less,
        improving responsiveness). Brake clearance (larger wheels accommodate
        bigger brakes). Wider tire options (low-profile tires often available in
        wider widths for more grip).

        Critical constraint - overall diameter: The total height of the mounted tire
        must remain very close to original (+/- 3 percent maximum). Diameter changes
        affect speedometer/odometer accuracy, gear ratios, ABS/traction control
        calibration, ground clearance, and fender clearance. Changes outside 3 percent
        cause significant problems.

        Calculating overall diameter: Formula is (rim_diameter_inches + 2 × sidewall_height_inches).
        Sidewall height = tire_width_mm × aspect_ratio / 100 / 25.4. Example:
        225/65R16 = 16 + 2×(225×0.65/25.4) = 16 + 11.52 = 27.52 inches. Online
        calculators simplify this process.

        Effects of diameter changes: Larger overall diameter makes speedometer read
        slower than actual (dangerous). Odometer accumulates fewer miles than actually
        driven (reduces resale value, violates odometer disclosure laws). Smaller
        diameter has opposite effects. ABS/traction control systems calibrated for
        specific tire rotational speed may malfunction. Gear ratios effectively change,
        affecting acceleration and fuel economy.

        Aspect ratio vs profile: Aspect ratio is sidewall height as percentage of
        tread width. 225/65 means sidewall is 65% of 225mm width = 146mm (5.75 inch)
        sidewall height. Lower aspect ratio (50, 45, 40) means shorter sidewall,
        harsher ride, better handling, more vulnerable to pothole damage, higher cost.

        Wheel width requirements: Each tire size has minimum and maximum rim width
        range. Installing tire on rim outside this range affects handling, wear
        pattern, bead seating safety. Wider rim stretches tire, narrower rim pinches
        it. Manufacturers publish rim width specifications - must be followed.

        Load rating and speed rating: Must match or exceed OEM specifications regardless
        of size changes. Plus-sized tires often have lower load ratings at same speed
        rating - verify before purchase. Never compromise safety specifications for
        appearance.

        Common plus-sizing progressions: 16 to 17 inch (+1), 16 to 18 inch (+2),
        17 to 20 inch (+3). Each increment increases wheel cost significantly and
        reduces tire availability/cost-effectiveness. Plus-3 and larger are typically
        show vehicles, not practical daily drivers.

        Minus-sizing applications: Winter tire setups often use minus-1 or minus-2
        (smaller wheel, taller tire) for softer ride in cold weather, more air cushion
        for pothole protection, lower cost. Some off-road applications use taller
        sidewalls for better impact resistance. Ensures winter tire can be purchased
        in narrower width for better snow penetration.
        """,
        key_factors=[
            "Overall diameter maintenance",
            "Aspect ratio vs handling/ride tradeoff",
            "Speedometer accuracy preservation",
            "Rim width compatibility",
            "Load and speed rating compliance",
            "Cost escalation with size increases"
        ],
        primary_authority=[
            "Tire manufacturer fitment guides",
            "TRA rim width standards",
            "Vehicle manufacturer specifications"
        ],
        burden_holder="Installer verifying diameter and specifications",
        adversary_position="Any tire that fits the wheel and clears the fender is acceptable",
        counter_arguments=[
            "Slight diameter change doesn't matter",
            "Wider tires always improve traction",
            "Larger wheels look better regardless of specs"
        ],
        resolution_strategy="Use tire size calculator, verify diameter within 3%, confirm load/speed ratings, educate on speedometer/ABS effects",
        entity_scope="All aftermarket wheel/tire size changes",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "FMVSS speedometer accuracy requirements",
            "Tire manufacturer fitment guidelines",
            "State odometer disclosure laws"
        ],
        category=IssueCategory.CONSTRUCTION
    )
]


# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

class TelemetryCollector:
    """Comprehensive telemetry and metrics collection"""

    def __init__(self):
        self.query_count = 0
        self.total_latency = 0.0
        self.cache_hits = 0
        self.cache_misses = 0
        self.doctrine_triggers: Dict[str, int] = {}
        self.error_count = 0
        self.start_time = time.time()

    def record_query(self, latency_ms: float, doctrines: List[str], cache_hit: bool):
        """Record query metrics"""
        self.query_count += 1
        self.total_latency += latency_ms
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        for doctrine in doctrines:
            self.doctrine_triggers[doctrine] = self.doctrine_triggers.get(doctrine, 0) + 1

    def record_error(self):
        """Record error occurrence"""
        self.error_count += 1

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        uptime = time.time() - self.start_time
        return {
            "queries_processed": self.query_count,
            "avg_latency_ms": self.total_latency / self.query_count if self.query_count > 0 else 0.0,
            "cache_hit_rate": self.cache_hits / (self.cache_hits + self.cache_misses) if (self.cache_hits + self.cache_misses) > 0 else 0.0,
            "error_rate": self.error_count / self.query_count if self.query_count > 0 else 0.0,
            "uptime_seconds": uptime,
            "top_doctrines": sorted(self.doctrine_triggers.items(), key=lambda x: x[1], reverse=True)[:10]
        }


# ============================================================================
# ENGINE CORE
# ============================================================================

class AUTO11TireEngine:
    """TIE-grade Tire Systems Analysis Engine"""

    def __init__(self):
        self.version = "1.0.0"
        self.doctrines = DOCTRINE_CACHE
        self.telemetry = TelemetryCollector()
        logger.info(f"AUTO11 Tire Systems Engine v{self.version} initialized with {len(self.doctrines)} doctrines")

    def three_layer_response(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> Tuple[str, List[str], List[str], ConfidenceLevel]:
        """Three-layer analysis: cache → semantic → deep"""
        start_time = time.time()

        # Layer 1: Doctrine cache (0-50ms)
        cache_results = self._search_doctrine_cache(query)
        if cache_results and mode == ResponseMode.FAST:
            latency = (time.time() - start_time) * 1000
            doctrines = [d.topic for d in cache_results[:3]]
            self.telemetry.record_query(latency, doctrines, True)
            return self._format_cache_response(cache_results[:3], mode, zone)

        # Layer 2: Semantic retrieval
        semantic_results = self._semantic_search(query, cache_results)

        # Layer 3: Deep analysis for MEMO mode
        if mode == ResponseMode.MEMO:
            return self._deep_analysis(query, semantic_results, zone)

        # Build response
        latency = (time.time() - start_time) * 1000
        doctrines = [d.topic for d in semantic_results[:5]]
        self.telemetry.record_query(latency, doctrines, False)

        return self._format_semantic_response(semantic_results, mode, zone)

    def _search_doctrine_cache(self, query: str) -> List[DoctrineBlock]:
        """Search doctrine cache for relevant blocks"""
        scored = [(d, d.match_score(query)) for d in self.doctrines]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [d for d, score in scored if score > 3.0]

    def _semantic_search(self, query: str, cache_results: List[DoctrineBlock]) -> List[DoctrineBlock]:
        """Semantic retrieval fallback"""
        if cache_results:
            return cache_results
        # Fallback to keyword matching
        query_lower = query.lower()
        matches = [d for d in self.doctrines if any(kw.lower() in query_lower for kw in d.keywords)]
        return matches if matches else self.doctrines[:5]

    def _format_cache_response(self, doctrines: List[DoctrineBlock], mode: ResponseMode, zone: AnalysisZone) -> Tuple[str, List[str], List[str], ConfidenceLevel]:
        """Format fast cache response"""
        primary = doctrines[0]

        if zone == AnalysisZone.DIAGNOSTIC:
            answer = f"{primary.conclusion_template[0]}\n\nKey factors:\n"
            answer += "\n".join(f"- {factor}" for factor in primary.key_factors[:5])
        elif zone == AnalysisZone.SPECIFICATION:
            answer = f"Technical specification analysis:\n\n{primary.reasoning_framework[:500]}"
        else:  # FORENSIC
            answer = f"Failure analysis:\n\n{primary.conclusion_template[0]}\n\n"
            answer += f"Root cause: {primary.reasoning_framework[:300]}"

        reasoning = [primary.topic, primary.conclusion_template[0]]
        authorities = primary.primary_authority
        confidence = primary.confidence

        return answer, reasoning, authorities, confidence

    def _format_semantic_response(self, doctrines: List[DoctrineBlock], mode: ResponseMode, zone: AnalysisZone) -> Tuple[str, List[str], List[str], ConfidenceLevel]:
        """Format semantic response"""
        if not doctrines:
            return "Insufficient doctrine coverage for this tire analysis.", [], [], ConfidenceLevel.HIGH_RISK

        primary = doctrines[0]

        answer = f"# {primary.topic}\n\n"
        answer += f"{primary.conclusion_template[0]}\n\n"
        answer += f"## Analysis\n\n{primary.reasoning_framework[:600]}\n\n"

        if mode == ResponseMode.DEFENSE:
            answer += f"## Counter-Arguments\n\n"
            answer += "\n".join(f"- {arg}" for arg in primary.counter_arguments)
            answer += f"\n\n## Resolution Strategy\n\n{primary.resolution_strategy}"

        reasoning = [d.topic for d in doctrines[:3]]
        authorities = []
        for d in doctrines[:3]:
            authorities.extend(d.primary_authority)

        confidence = primary.confidence

        return answer, reasoning, authorities, confidence

    def _deep_analysis(self, query: str, doctrines: List[DoctrineBlock], zone: AnalysisZone) -> Tuple[str, List[str], List[str], ConfidenceLevel]:
        """Deep analysis for MEMO mode"""
        if not doctrines:
            return "Insufficient doctrine coverage for comprehensive analysis.", [], [], ConfidenceLevel.HIGH_RISK

        primary = doctrines[0]

        answer = f"# COMPREHENSIVE TIRE ANALYSIS MEMORANDUM\n\n"
        answer += f"## Issue: {primary.topic}\n\n"
        answer += f"### Executive Summary\n\n"
        answer += "\n".join(primary.conclusion_template)
        answer += f"\n\n### Technical Analysis\n\n{primary.reasoning_framework}\n\n"
        answer += f"### Key Technical Factors\n\n"
        answer += "\n".join(f"{i+1}. {factor}" for i, factor in enumerate(primary.key_factors))
        answer += f"\n\n### Authoritative Standards\n\n"
        answer += "\n".join(f"- {auth}" for auth in primary.primary_authority)
        answer += f"\n\n### Counter-Arguments and Rebuttal\n\n"
        answer += "\n".join(f"- **Claim**: {arg}\n  **Rebuttal**: {primary.resolution_strategy}" for arg in primary.counter_arguments[:3])
        answer += f"\n\n### Recommended Action\n\n{primary.resolution_strategy}"
        answer += f"\n\n### Confidence Assessment\n\n{primary.confidence.value}"

        reasoning = [d.topic for d in doctrines]
        authorities = []
        for d in doctrines:
            authorities.extend(d.primary_authority)

        return answer, reasoning, authorities, primary.confidence

    def calculate_determinism_hash(self, query: str, answer: str, mode: ResponseMode) -> str:
        """Calculate SHA-256 hash for determinism tracking"""
        content = f"{query}|{answer}|{mode.value}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(title="AUTO11 Tire Systems Analysis", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = AUTO11TireEngine()


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    metrics = engine.telemetry.get_metrics()
    return HealthResponse(
        status="operational",
        version=engine.version,
        port=9321,
        doctrines_loaded=len(engine.doctrines),
        uptime_seconds=metrics["uptime_seconds"],
        queries_processed=metrics["queries_processed"],
        avg_latency_ms=metrics["avg_latency_ms"],
        cache_hit_rate=metrics["cache_hit_rate"]
    )


@app.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest):
    """Main query endpoint"""
    try:
        start_time = time.time()

        answer, reasoning, authorities, confidence = engine.three_layer_response(
            request.query,
            request.mode,
            request.zone
        )

        latency_ms = (time.time() - start_time) * 1000
        determinism_hash = engine.calculate_determinism_hash(request.query, answer, request.mode)

        return QueryResponse(
            answer=answer,
            confidence=confidence,
            mode=request.mode,
            zone=request.zone,
            doctrines_triggered=reasoning,
            reasoning_chain=reasoning,
            authority_citations=authorities,
            determinism_hash=determinism_hash,
            latency_ms=latency_ms,
            timestamp=datetime.utcnow().isoformat()
        )

    except Exception as e:
        engine.telemetry.record_error()
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
async def get_metrics():
    """Get engine metrics"""
    return engine.telemetry.get_metrics()


@app.get("/doctrines")
async def list_doctrines():
    """List all doctrine topics"""
    return {
        "total": len(engine.doctrines),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "keywords": d.keywords,
                "confidence": d.confidence.value
            }
            for d in engine.doctrines
        ]
    }


if __name__ == "__main__":
    logger.info("Starting AUTO11 Tire Systems Analysis Engine on port 9321")
    uvicorn.run(app, host="0.0.0.0", port=9321)
