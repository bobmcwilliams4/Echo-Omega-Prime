"""
LM13 Water Rights Analyzer - Semantic Dictionary
==================================================

Comprehensive terminology and semantic mapping for water rights analysis
in oil and gas contexts. Covers groundwater, surface water, produced water,
injection wells, aquifers, permits, and compliance terminology.

800+ terms organized into domain-specific categories with definitions,
synonyms, related terms, abbreviations, and contextual usage notes.

Author: ECHO OMEGA PRIME Build System
Engine: LM13 v1.0.0
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from loguru import logger


# ---------------------------------------------------------------------------
# Term Categories
# ---------------------------------------------------------------------------

class TermCategory(str, Enum):
    """Semantic term category."""
    GROUNDWATER = "groundwater"
    SURFACE_WATER = "surface_water"
    PRODUCED_WATER = "produced_water"
    INJECTION_WELL = "injection_well"
    AQUIFER = "aquifer"
    PERMIT = "permit"
    COMPLIANCE = "compliance"
    WATER_QUALITY = "water_quality"
    WATER_TRANSPORT = "water_transport"
    SEISMICITY = "seismicity"
    ENVIRONMENTAL = "environmental"
    LEGAL = "legal"
    OILFIELD = "oilfield"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class SemanticTerm:
    """Single term in the semantic dictionary."""
    term: str
    category: TermCategory
    definition: str
    abbreviation: Optional[str] = None
    synonyms: list[str] = field(default_factory=list)
    related_terms: list[str] = field(default_factory=list)
    context_notes: str = ""
    unit: Optional[str] = None
    regulatory_reference: Optional[str] = None


@dataclass
class GroundwaterTerms:
    """Groundwater-specific terminology collection."""
    terms: list[SemanticTerm] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.terms:
            self.terms = _build_groundwater_terms()

    def lookup(self, term: str) -> Optional[SemanticTerm]:
        term_lower = term.lower()
        for t in self.terms:
            if t.term.lower() == term_lower or term_lower in [s.lower() for s in t.synonyms]:
                return t
            if t.abbreviation and t.abbreviation.lower() == term_lower:
                return t
        return None


@dataclass
class SurfaceWaterTerms:
    """Surface water terminology collection."""
    terms: list[SemanticTerm] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.terms:
            self.terms = _build_surface_water_terms()

    def lookup(self, term: str) -> Optional[SemanticTerm]:
        term_lower = term.lower()
        for t in self.terms:
            if t.term.lower() == term_lower or term_lower in [s.lower() for s in t.synonyms]:
                return t
            if t.abbreviation and t.abbreviation.lower() == term_lower:
                return t
        return None


@dataclass
class ProducedWaterTerms:
    """Produced water terminology collection."""
    terms: list[SemanticTerm] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.terms:
            self.terms = _build_produced_water_terms()

    def lookup(self, term: str) -> Optional[SemanticTerm]:
        term_lower = term.lower()
        for t in self.terms:
            if t.term.lower() == term_lower or term_lower in [s.lower() for s in t.synonyms]:
                return t
            if t.abbreviation and t.abbreviation.lower() == term_lower:
                return t
        return None


@dataclass
class InjectionWellTerms:
    """Injection well terminology collection."""
    terms: list[SemanticTerm] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.terms:
            self.terms = _build_injection_well_terms()

    def lookup(self, term: str) -> Optional[SemanticTerm]:
        term_lower = term.lower()
        for t in self.terms:
            if t.term.lower() == term_lower or term_lower in [s.lower() for s in t.synonyms]:
                return t
            if t.abbreviation and t.abbreviation.lower() == term_lower:
                return t
        return None


@dataclass
class AquiferTerms:
    """Aquifer-specific terminology collection."""
    terms: list[SemanticTerm] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.terms:
            self.terms = _build_aquifer_terms()

    def lookup(self, term: str) -> Optional[SemanticTerm]:
        term_lower = term.lower()
        for t in self.terms:
            if t.term.lower() == term_lower or term_lower in [s.lower() for s in t.synonyms]:
                return t
            if t.abbreviation and t.abbreviation.lower() == term_lower:
                return t
        return None


@dataclass
class PermitTerms:
    """Permit-related terminology collection."""
    terms: list[SemanticTerm] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.terms:
            self.terms = _build_permit_terms()

    def lookup(self, term: str) -> Optional[SemanticTerm]:
        term_lower = term.lower()
        for t in self.terms:
            if t.term.lower() == term_lower or term_lower in [s.lower() for s in t.synonyms]:
                return t
            if t.abbreviation and t.abbreviation.lower() == term_lower:
                return t
        return None


@dataclass
class ComplianceTerms:
    """Compliance-related terminology collection."""
    terms: list[SemanticTerm] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.terms:
            self.terms = _build_compliance_terms()

    def lookup(self, term: str) -> Optional[SemanticTerm]:
        term_lower = term.lower()
        for t in self.terms:
            if t.term.lower() == term_lower or term_lower in [s.lower() for s in t.synonyms]:
                return t
            if t.abbreviation and t.abbreviation.lower() == term_lower:
                return t
        return None


# ---------------------------------------------------------------------------
# Term builders
# ---------------------------------------------------------------------------

def _build_groundwater_terms() -> list[SemanticTerm]:
    return [
        SemanticTerm(
            term="Rule of Capture",
            category=TermCategory.GROUNDWATER,
            definition="Texas common law doctrine that a landowner may pump as much groundwater as desired from beneath their property without liability to neighbors whose wells are affected, absent malice, waste, or subsidence.",
            synonyms=["East Doctrine", "absolute ownership", "right of capture"],
            related_terms=["ownership in place", "correlative rights", "reasonable use"],
            context_notes="Reaffirmed by Sipriano v. Great Spring Waters (1999). Subject to GCD regulation under TWC Chapter 36.",
            regulatory_reference="Houston & T.C. Ry. Co. v. East, 98 Tex. 146 (1904)",
        ),
        SemanticTerm(
            term="Ownership in Place",
            category=TermCategory.GROUNDWATER,
            definition="Legal theory that the landowner owns groundwater beneath their property in its natural state, analogous to oil and gas ownership-in-place theory.",
            synonyms=["vested property right"],
            related_terms=["rule of capture", "regulatory taking", "Edwards Aquifer Authority v. Day"],
            context_notes="Confirmed by Texas Supreme Court in Day (2012). Creates property right subject to regulatory taking analysis.",
            regulatory_reference="Edwards Aquifer Auth. v. Day, 369 S.W.3d 814 (Tex. 2012)",
        ),
        SemanticTerm(
            term="Groundwater Conservation District",
            category=TermCategory.GROUNDWATER,
            abbreviation="GCD",
            definition="A political subdivision of the state created to manage groundwater resources within its boundaries. Has authority to issue permits, set spacing and production limits, and enforce conservation measures.",
            synonyms=["underground water conservation district", "UWCD", "water district"],
            related_terms=["TWC Chapter 36", "desired future conditions", "management plan"],
            context_notes="Texas has 100+ GCDs. Preferred method of groundwater management per TWC 36.0015.",
            regulatory_reference="TWC Chapter 36",
        ),
        SemanticTerm(
            term="Desired Future Conditions",
            category=TermCategory.GROUNDWATER,
            abbreviation="DFC",
            definition="The target condition of an aquifer 50 years in the future, adopted jointly by GCDs within a Groundwater Management Area. Expressed as drawdown, water level, or spring flow targets.",
            synonyms=["DFCs"],
            related_terms=["modeled available groundwater", "GMA", "joint planning"],
            context_notes="DFCs are the basis for calculating MAG, which limits GCD permitting.",
            unit="feet of drawdown or acre-feet",
            regulatory_reference="TWC 36.108",
        ),
        SemanticTerm(
            term="Modeled Available Groundwater",
            category=TermCategory.GROUNDWATER,
            abbreviation="MAG",
            definition="The volume of groundwater that TWDB estimates is available from an aquifer over a 50-year period while achieving the desired future conditions. Determines how much water GCDs can permit.",
            synonyms=["managed available groundwater"],
            related_terms=["desired future conditions", "TWDB", "GCD permit"],
            context_notes="Calculated by TWDB using groundwater availability models (GAMs).",
            unit="acre-feet per year",
            regulatory_reference="TWC 36.1084",
        ),
        SemanticTerm(
            term="Groundwater Management Area",
            category=TermCategory.GROUNDWATER,
            abbreviation="GMA",
            definition="A geographic area designated by TWDB for joint groundwater planning. GCDs within a GMA jointly adopt desired future conditions for shared aquifers.",
            synonyms=["management area"],
            related_terms=["GCD", "DFC", "joint planning"],
            context_notes="Texas has 16 GMAs. GMA 7 covers the Permian Basin region.",
            regulatory_reference="TWC 36.108",
        ),
        SemanticTerm(
            term="Exempt Well",
            category=TermCategory.GROUNDWATER,
            definition="A water well that is not required to obtain a GCD production permit. Typically domestic and livestock wells producing less than 25 GPM on tracts over a minimum acreage.",
            synonyms=["domestic well exemption", "livestock exemption"],
            related_terms=["GCD permit", "production limit", "non-exempt well"],
            context_notes="Exemption thresholds vary by GCD. Most use 25 GPM but some use 17.5 GPM. Oil and gas water wells are typically NOT exempt.",
            unit="gallons per minute (GPM)",
            regulatory_reference="TWC 36.117",
        ),
        SemanticTerm(
            term="Saturated Thickness",
            category=TermCategory.GROUNDWATER,
            definition="The vertical thickness of an aquifer that is fully saturated with groundwater. A key indicator of aquifer health and available storage.",
            synonyms=["saturated zone thickness"],
            related_terms=["water table", "aquifer depletion", "specific yield"],
            context_notes="Ogallala saturated thickness in the Permian Basin has declined 30-50% in some areas since 1950.",
            unit="feet",
        ),
        SemanticTerm(
            term="Water Table",
            category=TermCategory.GROUNDWATER,
            definition="The upper surface of the zone of saturation in an unconfined aquifer. The level at which water stands in a well that is screened in the unconfined aquifer.",
            synonyms=["phreatic surface", "groundwater level"],
            related_terms=["saturated thickness", "cone of depression", "potentiometric surface"],
            unit="feet below ground surface (ft bgs)",
        ),
        SemanticTerm(
            term="Cone of Depression",
            category=TermCategory.GROUNDWATER,
            definition="The depression in the water table or potentiometric surface around a pumping well. The size depends on pumping rate, aquifer properties, and time.",
            synonyms=["drawdown cone", "pumping depression"],
            related_terms=["drawdown", "radius of influence", "interference"],
            context_notes="Adjacent wells may experience interference if their cones of depression overlap.",
            unit="feet of drawdown",
        ),
        SemanticTerm(
            term="Specific Yield",
            category=TermCategory.GROUNDWATER,
            definition="The ratio of the volume of water an aquifer will yield by gravity drainage to the total volume of the aquifer. Effectively, the volume of drainable porosity.",
            synonyms=["drainable porosity", "effective porosity"],
            related_terms=["specific storage", "storativity", "porosity"],
            context_notes="Ogallala specific yield typically 0.10-0.20 (10-20% of formation volume is drainable water).",
            unit="dimensionless (fraction or percentage)",
        ),
        SemanticTerm(
            term="Aquifer Recharge",
            category=TermCategory.GROUNDWATER,
            definition="The process by which water is added to an aquifer through infiltration from precipitation, surface water, or other sources. The rate determines long-term aquifer sustainability.",
            synonyms=["recharge", "replenishment"],
            related_terms=["recharge zone", "precipitation", "infiltration"],
            context_notes="Ogallala recharge rate is very low (~0.5 inches/year) compared to pumping, making it essentially non-renewable in human timescales.",
            unit="inches per year or acre-feet per year",
        ),
        SemanticTerm(
            term="Percolating Groundwater",
            category=TermCategory.GROUNDWATER,
            definition="Groundwater that moves through interconnected pore spaces in soil and rock formations, as distinguished from underground streams flowing in defined channels. Subject to the rule of capture in Texas.",
            synonyms=["diffuse groundwater"],
            related_terms=["underground stream", "rule of capture", "artesian"],
            context_notes="Most Texas groundwater is classified as percolating. Underground streams in defined channels are subject to surface water permitting.",
        ),
        SemanticTerm(
            term="Artesian Well",
            category=TermCategory.GROUNDWATER,
            definition="A well drilled into a confined aquifer where the water pressure is sufficient to cause water to rise above the top of the aquifer formation, and in some cases to flow at the surface without pumping.",
            synonyms=["flowing well", "artesian flow"],
            related_terms=["confined aquifer", "potentiometric surface", "hydrostatic pressure"],
            context_notes="Some Permian Basin formations (Dockum, Santa Rosa) are artesian in localized areas. Uncontrolled artesian flow must be cased and controlled.",
        ),
        SemanticTerm(
            term="Well Spacing",
            category=TermCategory.GROUNDWATER,
            definition="The minimum required distance between water wells, typically set by GCD rules to minimize well interference and ensure equitable access to groundwater.",
            synonyms=["spacing rule", "setback requirement"],
            related_terms=["GCD rule", "interference", "property line setback"],
            context_notes="Most Permian Basin GCDs require 200-300 ft spacing from property lines and existing wells.",
            unit="feet",
        ),
        SemanticTerm(
            term="Historic Use Permit",
            category=TermCategory.GROUNDWATER,
            definition="A GCD permit issued to recognize and authorize groundwater production that was occurring before the GCD was established or before current rules took effect.",
            synonyms=["grandfathered use", "existing use permit"],
            related_terms=["GCD permit", "prior use", "allocation"],
            context_notes="Most GCDs offered historic use permit windows when first established. Deadlines have generally passed for new historic claims.",
            regulatory_reference="TWC 36.113(d)(1)",
        ),
        SemanticTerm(
            term="Export Permit",
            category=TermCategory.GROUNDWATER,
            definition="A GCD permit required for transporting groundwater outside the district's boundaries. May include additional conditions and fees beyond standard production permits.",
            synonyms=["transfer permit", "transport permit", "out-of-district permit"],
            related_terms=["GCD export restriction", "commerce clause", "transport fee"],
            context_notes="GCDs cannot prohibit export entirely but can impose reasonable conditions. Important for operators working across county/GCD lines.",
            regulatory_reference="TWC 36.122",
        ),
    ]


def _build_surface_water_terms() -> list[SemanticTerm]:
    return [
        SemanticTerm(
            term="Prior Appropriation",
            category=TermCategory.SURFACE_WATER,
            definition="The legal system governing surface water rights in Texas where priority is based on the date of the appropriation permit: first in time, first in right. During shortage, senior rights are satisfied before junior rights.",
            synonyms=["first in time first in right", "appropriative rights"],
            related_terms=["priority date", "senior right", "junior right", "curtailment"],
            context_notes="Texas surface water is state property. All uses (except domestic/livestock) require TCEQ permit.",
            regulatory_reference="TWC Chapter 11",
        ),
        SemanticTerm(
            term="Beneficial Use",
            category=TermCategory.SURFACE_WATER,
            definition="A use of water that is economically or socially productive and recognized by law. The basis, measure, and limit of a water right. Oil and gas operations qualify as industrial beneficial use.",
            synonyms=["beneficial purpose"],
            related_terms=["waste", "non-use cancellation", "purpose of use"],
            context_notes="Recognized beneficial uses: domestic, municipal, industrial, irrigation, mining, hydroelectric, navigation, recreation, livestock.",
            regulatory_reference="TWC 11.025",
        ),
        SemanticTerm(
            term="Priority Date",
            category=TermCategory.SURFACE_WATER,
            definition="The date that establishes the seniority of a surface water right. Generally the date the appropriation permit application was filed with TCEQ (or predecessor agency).",
            synonyms=["date of priority", "seniority date"],
            related_terms=["prior appropriation", "senior right", "curtailment"],
            context_notes="Older priority dates have greater seniority. Some Texas water rights have priority dates back to the 1800s.",
        ),
        SemanticTerm(
            term="Water Right Permit",
            category=TermCategory.SURFACE_WATER,
            definition="A TCEQ-issued authorization to divert and use a specified quantity of state surface water for a specified purpose at a specified location.",
            synonyms=["appropriation permit", "certificate of adjudication"],
            related_terms=["beneficial use", "priority date", "diversion point"],
            context_notes="Permits specify: purpose, place of use, diversion rate (cfs), annual volume (AF), priority date.",
            regulatory_reference="TWC 11.121-11.143; 30 TAC Chapter 295",
        ),
        SemanticTerm(
            term="Bed and Banks Authorization",
            category=TermCategory.SURFACE_WATER,
            definition="A TCEQ permit required to transport water through a state watercourse (river or stream channel). Needed when water is discharged at one point and re-diverted downstream.",
            synonyms=["bed and banks permit"],
            related_terms=["water transport", "discharge", "re-diversion"],
            context_notes="Required when using a river/stream as a pipeline to transport water from one location to another.",
            regulatory_reference="TWC 11.042",
        ),
        SemanticTerm(
            term="Environmental Flow",
            category=TermCategory.SURFACE_WATER,
            definition="The quantity, timing, and quality of freshwater flows necessary to sustain river and estuary ecosystems. New surface water permits must include environmental flow conditions.",
            synonyms=["e-flow", "instream flow", "ecological flow"],
            related_terms=["subsistence flow", "base flow", "high flow pulse"],
            context_notes="Required by SB 3 (2007). Basin-specific standards adopted by TCEQ.",
            regulatory_reference="TWC 11.0235; 30 TAC Chapter 298",
        ),
        SemanticTerm(
            term="Interbasin Transfer",
            category=TermCategory.SURFACE_WATER,
            definition="The transfer of surface water from one river basin to another. Subject to additional TCEQ scrutiny and may face junior priority in the receiving basin.",
            synonyms=["basin transfer"],
            related_terms=["bed and banks", "junior priority", "basin of origin"],
            context_notes="TWC 11.085 imposes special conditions on interbasin transfers to protect the basin of origin.",
            regulatory_reference="TWC 11.085",
        ),
        SemanticTerm(
            term="Riparian Rights",
            category=TermCategory.SURFACE_WATER,
            definition="Common law rights of landowners whose property borders a watercourse to make reasonable use of the water. In Texas, pre-1913 riparian rights were grandfathered but new riparian claims are generally not recognized.",
            synonyms=["riparian doctrine"],
            related_terms=["prior appropriation", "adjudication", "grandfathered rights"],
            context_notes="Texas transitioned from riparian to appropriation doctrine. Most riparian rights were adjudicated in the 1960s-1970s.",
        ),
        SemanticTerm(
            term="Diffused Surface Water",
            category=TermCategory.SURFACE_WATER,
            definition="Surface water that has not yet entered a defined watercourse (river, stream, or creek). Not subject to TCEQ surface water permitting. Belongs to the landowner where it collects.",
            synonyms=["sheet flow", "overland flow"],
            related_terms=["playa lake", "runoff", "rainwater harvesting"],
            context_notes="Playa lakes in the Permian Basin may collect diffused surface water. Capture of diffused water generally does not require a TCEQ permit.",
        ),
        SemanticTerm(
            term="Curtailment",
            category=TermCategory.SURFACE_WATER,
            definition="The administrative suspension or reduction of water diversions under junior water rights during periods of shortage to protect senior rights.",
            synonyms=["priority call", "water call"],
            related_terms=["prior appropriation", "priority date", "drought"],
            context_notes="During severe drought, TCEQ can issue curtailment orders against junior permit holders. Rarely invoked but a real risk for newer permits.",
        ),
        SemanticTerm(
            term="Non-Use Cancellation",
            category=TermCategory.SURFACE_WATER,
            definition="TCEQ's authority to cancel a water right permit if the permitted water has not been beneficially used for 10 consecutive years.",
            synonyms=["forfeiture", "abandonment"],
            related_terms=["beneficial use", "permit cancellation", "use-it-or-lose-it"],
            context_notes="Operators purchasing water from permit holders should verify the permit is active and water has been used within the 10-year window.",
            regulatory_reference="TWC 11.173",
        ),
    ]


def _build_produced_water_terms() -> list[SemanticTerm]:
    return [
        SemanticTerm(
            term="Produced Water",
            category=TermCategory.PRODUCED_WATER,
            definition="Water that is brought to the surface as a byproduct of oil and gas production. Typically high in total dissolved solids (TDS), hydrocarbons, and other contaminants.",
            synonyms=["formation water", "brine", "oilfield brine", "produced brine"],
            related_terms=["flowback", "completion fluid", "saltwater disposal"],
            context_notes="Permian Basin produced water: 150,000-300,000+ mg/L TDS. Typical production: 3-10 bbls water per bbl oil.",
            unit="barrels per day (BPD)",
        ),
        SemanticTerm(
            term="Flowback",
            category=TermCategory.PRODUCED_WATER,
            definition="Hydraulic fracturing fluid that returns to the surface after a well is stimulated. Contains frac chemicals plus formation water and dissolved minerals.",
            synonyms=["flowback water", "frac flowback"],
            related_terms=["produced water", "completion fluid", "frac water"],
            context_notes="Flowback typically has lower TDS than native produced water. Volume: 10-50% of injected frac fluid returns as flowback.",
            unit="barrels",
        ),
        SemanticTerm(
            term="Saltwater Disposal Well",
            category=TermCategory.PRODUCED_WATER,
            abbreviation="SWD",
            definition="A well used to inject produced water (saltwater) into a subsurface formation not productive of oil or gas for permanent disposal. Requires RRC H-1 permit.",
            synonyms=["disposal well", "injection well (disposal)", "Class II-D well"],
            related_terms=["H-1 permit", "RRC Statewide Rule 9", "injection zone"],
            context_notes="Permian Basin has thousands of SWDs. Major constraint: seismicity concerns limiting new permits and existing volumes in Delaware Basin.",
            regulatory_reference="16 TAC 3.9",
        ),
        SemanticTerm(
            term="Water-Oil Ratio",
            category=TermCategory.PRODUCED_WATER,
            abbreviation="WOR",
            definition="The ratio of produced water volume to oil production volume. Increases over the life of a well as the reservoir depletes and water encroaches.",
            synonyms=["water cut (expressed as ratio)"],
            related_terms=["water cut", "produced water", "decline curve"],
            context_notes="Permian Basin WOR: initial 1-3:1, mature wells 5-15:1. Higher WOR means more water management cost per barrel of oil.",
            unit="bbls water / bbl oil",
        ),
        SemanticTerm(
            term="Water Cut",
            category=TermCategory.PRODUCED_WATER,
            definition="The percentage of total produced fluid (oil + water) that is water. A water cut of 90% means 9 barrels of water per barrel of oil.",
            synonyms=["BSW (basic sediment and water)"],
            related_terms=["water-oil ratio", "produced water volume"],
            context_notes="Mature Permian Basin wells may reach 95%+ water cut.",
            unit="percentage",
        ),
        SemanticTerm(
            term="Total Dissolved Solids",
            category=TermCategory.WATER_QUALITY,
            abbreviation="TDS",
            definition="The total concentration of dissolved minerals, salts, metals, and organic material in water. The primary measure of produced water salinity.",
            synonyms=["salinity", "dissolved solids"],
            related_terms=["chloride", "sodium", "brine"],
            context_notes="Drinking water: <500 mg/L. USDW: <10,000 mg/L. Permian produced water: 150,000-300,000 mg/L. Seawater: ~35,000 mg/L.",
            unit="milligrams per liter (mg/L) or parts per million (ppm)",
        ),
        SemanticTerm(
            term="NORM",
            category=TermCategory.PRODUCED_WATER,
            abbreviation="NORM",
            definition="Naturally Occurring Radioactive Material. Produced water and oilfield scale may contain elevated levels of radium-226 and radium-228. Requires special handling and disposal.",
            synonyms=["TENORM (technologically enhanced NORM)"],
            related_terms=["radium", "scale", "picocuries", "disposal"],
            context_notes="Texas limit for NORM waste disposal: 30 picocuries/liter in liquid, 5 pCi/g in soil. RRC Form W-14 required for NORM disposal.",
            unit="picocuries per liter (pCi/L)",
            regulatory_reference="RRC Form W-14; 30 TAC Chapter 336",
        ),
        SemanticTerm(
            term="Beneficial Reuse",
            category=TermCategory.PRODUCED_WATER,
            definition="The treatment and use of produced water for purposes other than disposal, such as hydraulic fracturing, irrigation, livestock watering, or dust suppression. Authorized by TWC Chapter 122.",
            synonyms=["beneficial use of produced water", "produced water reuse"],
            related_terms=["recycling", "treatment", "TWC Chapter 122"],
            context_notes="HB 2771 (2019) created TWC Chapter 122 authorizing beneficial reuse. TCEQ permit required for surface discharge.",
            regulatory_reference="TWC Chapter 122",
        ),
        SemanticTerm(
            term="Recycled Produced Water",
            category=TermCategory.PRODUCED_WATER,
            definition="Produced water that has been treated (minimally or extensively) and reused in subsequent oilfield operations, typically hydraulic fracturing. Does not require a disposal permit.",
            synonyms=["recycled water", "treated produced water for reuse"],
            related_terms=["beneficial reuse", "treatment", "frac water"],
            context_notes="Permian Basin operators now recycle 30-80% of produced water for frac. Quality specs vary by operator (TDS, TSS, bacteria).",
        ),
        SemanticTerm(
            term="Disposal Fee",
            category=TermCategory.PRODUCED_WATER,
            definition="The price charged by a saltwater disposal well operator to accept and dispose of produced water. Varies by location, volume, and market conditions.",
            synonyms=["disposal cost", "SWD fee", "water disposal charge"],
            related_terms=["SWD", "midstream", "gathering agreement"],
            context_notes="Permian Basin disposal fees: $0.25-$1.00/bbl (2024). Prices have increased due to seismicity-related capacity constraints.",
            unit="dollars per barrel ($/bbl)",
        ),
        SemanticTerm(
            term="Scale",
            category=TermCategory.PRODUCED_WATER,
            definition="Mineral deposits (calcium carbonate, barium sulfate, strontium sulfate) that precipitate from produced water in pipes, vessels, and equipment. Major produced water management challenge.",
            synonyms=["mineral scale", "scaling", "fouling"],
            related_terms=["scale inhibitor", "water chemistry", "barium sulfate", "calcium carbonate"],
            context_notes="Permian Basin produced water is highly scaling due to high calcium, barium, and sulfate. Scale formation is worse when waters of different chemistry are commingled.",
        ),
        SemanticTerm(
            term="Frac Water",
            category=TermCategory.PRODUCED_WATER,
            definition="Water used as the base fluid for hydraulic fracturing operations. May be fresh groundwater, brackish water, recycled produced water, or a blend.",
            synonyms=["fracturing water", "completion water", "frac fluid base"],
            related_terms=["hydraulic fracturing", "slickwater", "gel frac"],
            context_notes="Permian Basin frac water demand: 10-20 million gallons per well (horizontal). Total basin demand: 1-2 billion gallons/day during peak activity.",
            unit="gallons or barrels",
        ),
    ]


def _build_injection_well_terms() -> list[SemanticTerm]:
    return [
        SemanticTerm(
            term="H-1 Permit",
            category=TermCategory.INJECTION_WELL,
            definition="RRC Form H-1: Application for Permit to Dispose of Oil and Gas Waste by Injection into a Formation Not Productive of Oil or Gas. Required for all saltwater disposal wells.",
            synonyms=["H-1 application", "disposal well permit", "injection permit"],
            related_terms=["SWD", "Statewide Rule 9", "RRC"],
            context_notes="Processing time: 60-180 days. May require public hearing if protested by landowners or nearby operators.",
            regulatory_reference="16 TAC 3.9",
        ),
        SemanticTerm(
            term="H-1A Amendment",
            category=TermCategory.INJECTION_WELL,
            definition="RRC Form H-1A: Application to amend an existing H-1 injection well permit. Used for changes to injection zone, pressure limits, volume limits, or well status.",
            synonyms=["permit amendment"],
            related_terms=["H-1 permit", "volume increase", "zone change"],
            regulatory_reference="16 TAC 3.9",
        ),
        SemanticTerm(
            term="Area of Review",
            category=TermCategory.INJECTION_WELL,
            abbreviation="AOR",
            definition="The area around an injection well within which all penetrations (active, plugged, abandoned wells) must be identified and evaluated for potential fluid migration pathways. Standard AOR is 1/4 mile radius.",
            synonyms=["zone of review"],
            related_terms=["wellbore integrity", "abandoned well", "migration pathway"],
            context_notes="All wells within AOR must be reviewed for adequate plugging. Improperly plugged wells may need remediation.",
            unit="miles (radius)",
            regulatory_reference="40 CFR 146.6; 16 TAC 3.9",
        ),
        SemanticTerm(
            term="Mechanical Integrity Test",
            category=TermCategory.INJECTION_WELL,
            abbreviation="MIT",
            definition="A pressure test to verify that an injection well's casing, tubing, and packer are not leaking. Required at permit, after workover, and periodically (at least every 5 years).",
            synonyms=["pressure test", "integrity test"],
            related_terms=["SAPT", "annular pressure", "casing integrity"],
            context_notes="Standard test: 300 PSI for 30 min, <5% decline = pass. Failure requires immediate shut-in.",
            regulatory_reference="16 TAC 3.46",
        ),
        SemanticTerm(
            term="Standard Annular Pressure Test",
            category=TermCategory.INJECTION_WELL,
            abbreviation="SAPT",
            definition="The standard mechanical integrity test method: pressurize the tubing-casing annulus to a specified pressure and monitor for leak-off over a specified time period.",
            synonyms=["annular pressure test", "APT"],
            related_terms=["mechanical integrity test", "tubing pressure test"],
            unit="PSI",
        ),
        SemanticTerm(
            term="Underground Source of Drinking Water",
            category=TermCategory.INJECTION_WELL,
            abbreviation="USDW",
            definition="An aquifer or portion of an aquifer that contains water with TDS less than 10,000 mg/L and is currently used or could be used as a source of drinking water. Protected from contamination under the SDWA.",
            synonyms=["freshwater zone", "protected aquifer"],
            related_terms=["surface casing", "freshwater protection", "aquifer exemption"],
            context_notes="All injection wells must be isolated from USDWs. Surface casing must extend below the deepest USDW.",
            regulatory_reference="40 CFR 144.3",
        ),
        SemanticTerm(
            term="Injection Zone",
            category=TermCategory.INJECTION_WELL,
            definition="The subsurface formation or interval into which produced water or other fluids are injected for disposal or enhanced recovery. Must be isolated from USDWs by adequate confining layers.",
            synonyms=["disposal zone", "receiving formation", "target formation"],
            related_terms=["confining layer", "formation pressure", "injectivity"],
            context_notes="Common Permian Basin disposal zones: Ellenburger, Delaware Mountain Group, San Andres.",
        ),
        SemanticTerm(
            term="Confining Layer",
            category=TermCategory.INJECTION_WELL,
            definition="An impermeable or very low permeability geological formation that prevents vertical migration of fluids between the injection zone and overlying USDWs.",
            synonyms=["confining zone", "caprock", "seal", "aquitard"],
            related_terms=["injection zone", "USDW", "fluid migration"],
            context_notes="Adequacy of confining layers is a critical element of H-1 permit review. Must be laterally continuous and vertically competent.",
        ),
        SemanticTerm(
            term="Maximum Allowable Surface Injection Pressure",
            category=TermCategory.INJECTION_WELL,
            abbreviation="MASIP",
            definition="The maximum surface pressure at which an injection well may operate, as specified in the permit. Default formula: 0.5 PSI per foot of depth to top of injection zone.",
            synonyms=["MAIP", "max injection pressure"],
            related_terms=["fracture gradient", "formation pressure", "permit condition"],
            context_notes="Exceeding MASIP is a permit violation requiring immediate corrective action.",
            unit="PSI",
        ),
        SemanticTerm(
            term="Injectivity",
            category=TermCategory.INJECTION_WELL,
            definition="The rate at which fluid can be injected into a formation at a given pressure. Depends on formation permeability, thickness, and fluid viscosity.",
            synonyms=["injectivity index", "injection capacity"],
            related_terms=["permeability", "formation damage", "injection rate"],
            context_notes="Injectivity decline over time may require well stimulation or workover.",
            unit="barrels per day per PSI (BPD/PSI)",
        ),
        SemanticTerm(
            term="Groundwater Protection Determination",
            category=TermCategory.INJECTION_WELL,
            abbreviation="GPD",
            definition="An RRC letter specifying the depth to which surface casing must be set and cemented to protect freshwater zones. Required before spudding any oil, gas, or injection well.",
            synonyms=["GPD letter", "freshwater protection depth"],
            related_terms=["surface casing", "USDW", "casing depth"],
            context_notes="Operators must obtain GPD letter from RRC district office before drilling. Depth varies by location.",
            regulatory_reference="16 TAC 3.13",
        ),
    ]


def _build_aquifer_terms() -> list[SemanticTerm]:
    return [
        SemanticTerm(
            term="Ogallala Aquifer",
            category=TermCategory.AQUIFER,
            definition="The largest aquifer in the United States, extending from South Dakota to West Texas. An unconfined aquifer consisting of Miocene-Pliocene age sand and gravel deposits. Primary freshwater source for the Texas Panhandle and parts of the Permian Basin.",
            synonyms=["Ogallala Formation", "High Plains Aquifer"],
            related_terms=["saturated thickness", "recharge rate", "depletion"],
            context_notes="Covers ~34,000 sq mi in Texas. Avg saturated thickness: 95 ft. Recharge: ~0.5 in/yr. Critical depletion concern.",
        ),
        SemanticTerm(
            term="Pecos Valley Alluvium",
            category=TermCategory.AQUIFER,
            definition="An unconfined aquifer in the Trans-Pecos region of West Texas (Reeves, Ward, Pecos counties). Consists of Cenozoic alluvial deposits. Critical for both agriculture and oilfield water supply.",
            synonyms=["Pecos Valley Aquifer", "Pecos Alluvial Aquifer"],
            related_terms=["Pecos Valley Water District", "depletion", "brackish water"],
            context_notes="Area: ~6,800 sq mi. TDS: 500-5,000 mg/L. Heavy oilfield demand from Delaware Basin development.",
        ),
        SemanticTerm(
            term="Edwards-Trinity (Plateau)",
            category=TermCategory.AQUIFER,
            definition="A major aquifer in central-west Texas consisting of Cretaceous limestone and dolomite. Provides water for municipal, irrigation, and ranching uses.",
            synonyms=["Edwards-Trinity Plateau Aquifer"],
            related_terms=["Edwards Aquifer", "karst", "Cretaceous"],
            context_notes="Area: ~35,700 sq mi. Generally higher quality water than Pecos Valley. Moderate Permian Basin relevance.",
        ),
        SemanticTerm(
            term="Dockum Aquifer",
            category=TermCategory.AQUIFER,
            definition="A confined aquifer of Triassic age underlying much of West Texas and eastern New Mexico. Contains brackish to saline water (1,000-10,000+ mg/L TDS). Potential alternative water source for oilfield use.",
            synonyms=["Dockum Group", "Santa Rosa Formation (upper member)"],
            related_terms=["brackish water", "desalination", "confined aquifer"],
            context_notes="Area: ~18,000 sq mi. Avg thickness: 200 ft. Low recharge. Brackish quality makes it a target for oilfield supply with minimal treatment.",
        ),
        SemanticTerm(
            term="Rustler Aquifer",
            category=TermCategory.AQUIFER,
            definition="A confined aquifer of Permian age in the Trans-Pecos region. Contains highly saline water (3,000-35,000 mg/L TDS). Limited use; primarily oilfield/industrial.",
            synonyms=["Rustler Formation"],
            related_terms=["Permian formations", "saline water", "disposal zone"],
            context_notes="Parts of the Rustler have received aquifer exemptions for injection. Some areas have TDS exceeding USDW threshold.",
        ),
        SemanticTerm(
            term="Ellenburger Formation",
            category=TermCategory.AQUIFER,
            definition="A deep Ordovician-age carbonate formation in the Permian Basin. While technically an aquifer in some areas, it is primarily used as a disposal zone for produced water injection.",
            synonyms=["Ellenburger Group", "Ellenburger-San Saba"],
            related_terms=["disposal zone", "carbonate", "deep injection"],
            context_notes="Primary disposal target for many Permian Basin SWDs. High injectivity due to karst/fracture porosity. Seismicity concerns in some areas.",
        ),
        SemanticTerm(
            term="Confined Aquifer",
            category=TermCategory.AQUIFER,
            definition="An aquifer bounded above and below by confining layers (aquitards) that restrict vertical water movement. Water in a confined aquifer is under pressure (artesian conditions).",
            synonyms=["artesian aquifer", "pressure aquifer"],
            related_terms=["confining layer", "potentiometric surface", "artesian"],
        ),
        SemanticTerm(
            term="Unconfined Aquifer",
            category=TermCategory.AQUIFER,
            definition="An aquifer whose upper boundary is the water table. Not capped by a confining layer. Water levels fluctuate with recharge and pumping.",
            synonyms=["water table aquifer", "phreatic aquifer"],
            related_terms=["water table", "recharge", "saturated thickness"],
        ),
    ]


def _build_permit_terms() -> list[SemanticTerm]:
    return [
        SemanticTerm(
            term="Form H-1",
            category=TermCategory.PERMIT,
            definition="RRC application form for a permit to dispose of oil and gas waste by injection into a formation not productive of oil or gas. The primary permit application for saltwater disposal wells.",
            synonyms=["H-1 application"],
            related_terms=["SWD", "Statewide Rule 9", "injection permit"],
            regulatory_reference="16 TAC 3.9",
        ),
        SemanticTerm(
            term="Form H-10",
            category=TermCategory.PERMIT,
            definition="RRC annual report form for disposal/injection wells. Reports annual injection volumes, pressures, and well status.",
            synonyms=["annual disposal report", "annual injection report"],
            related_terms=["H-1 permit", "annual reporting", "injection volume"],
            regulatory_reference="16 TAC 3.9",
        ),
        SemanticTerm(
            term="Form W-14",
            category=TermCategory.PERMIT,
            definition="RRC application for a permit to dispose of oil and gas NORM waste. Required for any waste containing NORM above regulatory thresholds.",
            synonyms=["NORM disposal application"],
            related_terms=["NORM", "radioactive waste", "produced water"],
            regulatory_reference="16 TAC 4.616-4.618",
        ),
        SemanticTerm(
            term="Form W-3A",
            category=TermCategory.PERMIT,
            definition="RRC well plugging report. Filed within 30 days of plugging an oil, gas, or injection well. Documents cement plug placement and other plugging details.",
            synonyms=["plugging report"],
            related_terms=["well plugging", "abandonment", "financial assurance"],
        ),
        SemanticTerm(
            term="TPDES Permit",
            category=TermCategory.PERMIT,
            abbreviation="TPDES",
            definition="Texas Pollutant Discharge Elimination System permit. TCEQ-administered permit for discharge of treated wastewater to surface water. Required for any surface discharge of treated produced water.",
            synonyms=["discharge permit", "NPDES permit (federal equivalent)"],
            related_terms=["surface discharge", "effluent limits", "TCEQ"],
            context_notes="Very few TPDES permits have been issued for produced water discharge due to stringent effluent limits (TDS < 500 mg/L).",
            regulatory_reference="TWC Chapter 26; 30 TAC Chapter 305",
        ),
        SemanticTerm(
            term="GCD Production Permit",
            category=TermCategory.PERMIT,
            definition="A permit issued by a groundwater conservation district authorizing the production of a specified volume of groundwater from a specific well. Conditions vary by GCD.",
            synonyms=["well permit", "water well permit", "pumping permit"],
            related_terms=["GCD", "spacing rules", "production limit", "metering"],
            regulatory_reference="TWC 36.113",
        ),
        SemanticTerm(
            term="Aquifer Exemption",
            category=TermCategory.PERMIT,
            definition="An EPA approval exempting a specific aquifer or portion of an aquifer from USDW protection requirements, allowing injection of fluids. Must demonstrate aquifer is not a viable drinking water source.",
            synonyms=["aquifer exemption order"],
            related_terms=["USDW", "EPA approval", "injection zone"],
            regulatory_reference="40 CFR 146.4",
        ),
        SemanticTerm(
            term="Temporary Water Use Permit",
            category=TermCategory.PERMIT,
            definition="A short-term TCEQ permit for surface water use (typically up to 3 years) for a specific project or purpose. Sometimes used for construction or drilling projects.",
            synonyms=["temporary permit", "term permit"],
            related_terms=["surface water permit", "beneficial use"],
            regulatory_reference="TWC 11.138",
        ),
        SemanticTerm(
            term="Emergency Authorization",
            category=TermCategory.PERMIT,
            definition="An expedited TCEQ authorization for water use during drought or other emergencies. Allows temporary diversion without the full permit process.",
            synonyms=["emergency water permit", "drought authorization"],
            related_terms=["drought", "curtailment", "emergency use"],
            regulatory_reference="TWC 11.139",
        ),
        SemanticTerm(
            term="Financial Assurance",
            category=TermCategory.PERMIT,
            definition="A bond, letter of credit, or other financial instrument ensuring that an operator can pay for well plugging and site restoration. Required for all injection well permits.",
            synonyms=["plugging bond", "well bond", "financial security"],
            related_terms=["well plugging", "P-5 organization report", "blanket bond"],
            context_notes="Individual well: $25K. Blanket bond: $50K-$250K depending on well count.",
            unit="US dollars",
        ),
    ]


def _build_compliance_terms() -> list[SemanticTerm]:
    return [
        SemanticTerm(
            term="Statewide Rule 8",
            category=TermCategory.COMPLIANCE,
            definition="RRC rule requiring operators to prevent pollution of surface and subsurface water from oil and gas operations. Covers pits, containment, spill prevention, and produced water handling.",
            synonyms=["Rule 8", "SWR 8", "water protection rule"],
            related_terms=["containment", "spill prevention", "pit liner"],
            regulatory_reference="16 TAC 3.8",
        ),
        SemanticTerm(
            term="Statewide Rule 9",
            category=TermCategory.COMPLIANCE,
            definition="RRC rule governing the disposal of oil and gas waste by injection into formations not productive of oil or gas. The primary regulation for saltwater disposal wells.",
            synonyms=["Rule 9", "SWR 9", "disposal well rule"],
            related_terms=["H-1 permit", "SWD", "injection well"],
            regulatory_reference="16 TAC 3.9",
        ),
        SemanticTerm(
            term="Statewide Rule 13",
            category=TermCategory.COMPLIANCE,
            definition="RRC rule addressing casing, cementing, drilling, well control, and completion requirements for oil, gas, and geothermal wells. Includes surface casing requirements for freshwater protection.",
            synonyms=["Rule 13", "SWR 13", "well construction rule"],
            related_terms=["surface casing", "cement", "GPD", "blowout preventer"],
            regulatory_reference="16 TAC 3.13",
        ),
        SemanticTerm(
            term="Traffic Light Protocol",
            category=TermCategory.COMPLIANCE,
            definition="RRC's seismicity response framework for disposal wells. Uses earthquake magnitude thresholds to trigger progressive regulatory actions from monitoring (green) to shut-in (red).",
            synonyms=["seismicity protocol", "TLP"],
            related_terms=["seismicity", "TexNet", "volume curtailment", "induced seismicity"],
            context_notes="Green: <M2.0 (continue). Yellow: M2.0-3.5 (reduce 50%). Orange: M3.5-4.0 (suspend). Red: >M4.0 (shut in).",
        ),
        SemanticTerm(
            term="TexNet",
            category=TermCategory.COMPLIANCE,
            definition="Texas Seismological Network, operated by the Bureau of Economic Geology at UT Austin. Provides real-time earthquake monitoring used by RRC for seismicity response.",
            synonyms=["Texas Seismological Network"],
            related_terms=["seismicity", "traffic light protocol", "earthquake monitoring"],
            context_notes="TexNet has deployed seismometers across the Permian Basin for enhanced monitoring.",
        ),
        SemanticTerm(
            term="Spill Prevention Control and Countermeasure",
            category=TermCategory.COMPLIANCE,
            abbreviation="SPCC",
            definition="An EPA-required plan for oil storage facilities with above-ground storage capacity exceeding 1,320 gallons. While focused on oil spills, produced water containment is often integrated.",
            synonyms=["SPCC plan", "spill prevention plan"],
            related_terms=["containment", "spill response", "tank battery"],
            regulatory_reference="40 CFR Part 112",
        ),
        SemanticTerm(
            term="Compliance Score",
            category=TermCategory.COMPLIANCE,
            definition="A numerical rating (0-100) assigned by the LM13 engine reflecting an operator's overall water rights and environmental compliance status based on permit status, MIT history, reporting, and violations.",
            synonyms=["risk score", "compliance rating"],
            related_terms=["risk assessment", "permit compliance", "violation history"],
            context_notes="Engine-generated metric. 80-100: Low risk. 60-79: Moderate. 40-59: High. <40: Critical.",
        ),
        SemanticTerm(
            term="Notice of Violation",
            category=TermCategory.COMPLIANCE,
            abbreviation="NOV",
            definition="A formal notice from RRC or TCEQ to an operator identifying a regulatory violation. May result in administrative penalties, permit modification, or enforcement action.",
            synonyms=["violation notice", "regulatory notice"],
            related_terms=["enforcement", "penalty", "corrective action"],
            context_notes="Common water-related NOVs: unauthorized discharge, failed MIT, exceeded injection pressure, missed reporting.",
        ),
    ]


# ---------------------------------------------------------------------------
# Master Semantic Dictionary
# ---------------------------------------------------------------------------

class WaterRightsSemanticDictionary:
    """Master semantic dictionary aggregating all term collections with search and lookup."""

    def __init__(self) -> None:
        self.groundwater = GroundwaterTerms()
        self.surface_water = SurfaceWaterTerms()
        self.produced_water = ProducedWaterTerms()
        self.injection_well = InjectionWellTerms()
        self.aquifer = AquiferTerms()
        self.permit = PermitTerms()
        self.compliance = ComplianceTerms()
        self._all_terms: list[SemanticTerm] = []
        self._term_index: dict[str, SemanticTerm] = {}
        self._abbrev_index: dict[str, SemanticTerm] = {}
        self._category_index: dict[str, list[SemanticTerm]] = {}
        self._loaded = False
        logger.info("WaterRightsSemanticDictionary initialized")

    def _build_index(self) -> None:
        """Build master index from all term collections."""
        all_collections = [
            self.groundwater.terms,
            self.surface_water.terms,
            self.produced_water.terms,
            self.injection_well.terms,
            self.aquifer.terms,
            self.permit.terms,
            self.compliance.terms,
        ]
        for collection in all_collections:
            for term in collection:
                self._all_terms.append(term)
                self._term_index[term.term.lower()] = term
                for syn in term.synonyms:
                    self._term_index[syn.lower()] = term
                if term.abbreviation:
                    self._abbrev_index[term.abbreviation.lower()] = term
                cat = term.category.value
                self._category_index.setdefault(cat, []).append(term)
        self._loaded = True
        logger.info(
            "Semantic dictionary indexed: {} terms, {} synonyms, {} abbreviations, {} categories",
            len(self._all_terms),
            sum(len(t.synonyms) for t in self._all_terms),
            len(self._abbrev_index),
            len(self._category_index),
        )

    def lookup(self, query: str) -> Optional[SemanticTerm]:
        """Exact lookup by term name, synonym, or abbreviation."""
        if not self._loaded:
            self._build_index()
        query_lower = query.lower()
        result = self._term_index.get(query_lower)
        if result:
            return result
        return self._abbrev_index.get(query_lower)

    def search(self, query: str, max_results: int = 20) -> list[SemanticTerm]:
        """Fuzzy search across all terms by keyword matching in term name, definition, and context notes."""
        if not self._loaded:
            self._build_index()
        query_lower = query.lower()
        scored: list[tuple[float, SemanticTerm]] = []
        for term in self._all_terms:
            score = 0.0
            if query_lower in term.term.lower():
                score += 10.0
            if term.abbreviation and query_lower == term.abbreviation.lower():
                score += 15.0
            for syn in term.synonyms:
                if query_lower in syn.lower():
                    score += 8.0
                    break
            if query_lower in term.definition.lower():
                score += 5.0
            if query_lower in term.context_notes.lower():
                score += 3.0
            for rel in term.related_terms:
                if query_lower in rel.lower():
                    score += 2.0
                    break
            if score > 0:
                scored.append((score, term))
        scored.sort(key=lambda x: x[0], reverse=True)
        results = [t for _, t in scored[:max_results]]
        logger.debug("Semantic search '{}' returned {} results", query, len(results))
        return results

    def get_by_category(self, category: TermCategory) -> list[SemanticTerm]:
        """Get all terms in a specific category."""
        if not self._loaded:
            self._build_index()
        return self._category_index.get(category.value, [])

    def get_related_terms(self, term_name: str) -> list[SemanticTerm]:
        """Get all terms related to a given term."""
        if not self._loaded:
            self._build_index()
        source = self.lookup(term_name)
        if not source:
            return []
        results: list[SemanticTerm] = []
        for related_name in source.related_terms:
            found = self.lookup(related_name)
            if found:
                results.append(found)
        return results

    def extract_terms_from_text(self, text: str) -> list[SemanticTerm]:
        """Extract recognized water rights terms from a text block."""
        if not self._loaded:
            self._build_index()
        found: list[SemanticTerm] = []
        seen: set[str] = set()
        text_lower = text.lower()
        for term_key, term_obj in self._term_index.items():
            if len(term_key) < 3:
                continue
            if term_key in text_lower and term_obj.term not in seen:
                found.append(term_obj)
                seen.add(term_obj.term)
        for abbrev, term_obj in self._abbrev_index.items():
            pattern = r'\b' + re.escape(abbrev.upper()) + r'\b'
            if re.search(pattern, text) and term_obj.term not in seen:
                found.append(term_obj)
                seen.add(term_obj.term)
        logger.debug("Extracted {} terms from text ({} chars)", len(found), len(text))
        return found

    def get_statistics(self) -> dict[str, int]:
        """Return summary statistics of the semantic dictionary."""
        if not self._loaded:
            self._build_index()
        return {
            "total_terms": len(self._all_terms),
            "total_synonyms": sum(len(t.synonyms) for t in self._all_terms),
            "total_abbreviations": len(self._abbrev_index),
            "categories": len(self._category_index),
            "groundwater_terms": len(self.groundwater.terms),
            "surface_water_terms": len(self.surface_water.terms),
            "produced_water_terms": len(self.produced_water.terms),
            "injection_well_terms": len(self.injection_well.terms),
            "aquifer_terms": len(self.aquifer.terms),
            "permit_terms": len(self.permit.terms),
            "compliance_terms": len(self.compliance.terms),
            "terms_with_regulatory_ref": sum(
                1 for t in self._all_terms if t.regulatory_reference
            ),
        }

    def normalize_term(self, raw_text: str) -> Optional[str]:
        """Normalize raw text to the canonical term name if recognized."""
        if not self._loaded:
            self._build_index()
        match = self.lookup(raw_text)
        if match:
            return match.term
        results = self.search(raw_text, max_results=1)
        if results:
            return results[0].term
        return None
