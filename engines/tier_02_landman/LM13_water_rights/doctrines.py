"""
LM13 Water Rights Analyzer - Doctrine Cache
=============================================

Comprehensive Texas water rights doctrine library covering groundwater,
surface water, produced water, injection wells, aquifer protection,
and oil-and-gas-specific water regulations.

Implements 92+ doctrine topics across 8 major categories:
1. Groundwater / Rule of Capture (East Doctrine)
2. Surface Water / Prior Appropriation
3. Groundwater Conservation Districts
4. Produced Water Disposal
5. Injection Well Regulation (UIC Class II)
6. Freshwater Protection
7. Water Recycling / Reuse / Brackish Desalination
8. Water Transport & Midstream

Texas Water Code, TAC Title 30 (TCEQ), TAC Title 16 (RRC),
Edwards Aquifer Authority Act, Safe Drinking Water Act.

Author: ECHO OMEGA PRIME Build System
Engine: LM13 v1.0.0
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from loguru import logger


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class DoctrineCategory(str, Enum):
    """Top-level doctrine classification."""
    GROUNDWATER_CAPTURE = "groundwater_capture"
    SURFACE_WATER_APPROPRIATION = "surface_water_appropriation"
    GROUNDWATER_CONSERVATION_DISTRICT = "groundwater_conservation_district"
    PRODUCED_WATER_DISPOSAL = "produced_water_disposal"
    INJECTION_WELL_REGULATION = "injection_well_regulation"
    FRESHWATER_PROTECTION = "freshwater_protection"
    WATER_RECYCLING_REUSE = "water_recycling_reuse"
    WATER_TRANSPORT_MIDSTREAM = "water_transport_midstream"
    EDWARDS_AQUIFER = "edwards_aquifer"
    BRACKISH_DESALINATION = "brackish_desalination"
    SEISMICITY_REGULATION = "seismicity_regulation"
    SURFACE_OWNER_ACCOMMODATION = "surface_owner_accommodation"


class AuthorityLevel(str, Enum):
    """Legal authority hierarchy."""
    FEDERAL_STATUTE = "federal_statute"
    FEDERAL_REGULATION = "federal_regulation"
    STATE_STATUTE = "state_statute"
    STATE_REGULATION = "state_regulation"
    AGENCY_RULE = "agency_rule"
    CASE_LAW = "case_law"
    AGENCY_GUIDANCE = "agency_guidance"
    INDUSTRY_STANDARD = "industry_standard"


class JurisdictionScope(str, Enum):
    """Geographic / jurisdictional scope."""
    FEDERAL = "federal"
    STATE_TEXAS = "state_texas"
    REGIONAL = "regional"
    GCD_LOCAL = "gcd_local"
    COUNTY = "county"
    BASIN_SPECIFIC = "basin_specific"


class RiskLevel(str, Enum):
    """Compliance risk level."""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class TexasWaterDoctrine:
    """Single water rights doctrine block."""
    doctrine_id: str
    title: str
    category: DoctrineCategory
    authority_level: AuthorityLevel
    jurisdiction: JurisdictionScope
    citation: str
    summary: str
    detailed_analysis: str
    key_provisions: list[str]
    exceptions: list[str]
    related_doctrines: list[str]
    risk_if_violated: RiskLevel
    permian_basin_notes: str
    last_updated: str
    tags: list[str] = field(default_factory=list)

    def compute_hash(self) -> str:
        """SHA-256 determinism hash of doctrine content."""
        content = json.dumps({
            "id": self.doctrine_id,
            "title": self.title,
            "citation": self.citation,
            "summary": self.summary,
            "detailed_analysis": self.detailed_analysis,
            "key_provisions": self.key_provisions,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class GroundwaterRule:
    """Groundwater conservation district rule."""
    rule_id: str
    district_name: str
    county: str
    rule_number: str
    title: str
    description: str
    permit_requirements: list[str]
    spacing_rules: dict[str, Any]
    production_limits: dict[str, Any]
    reporting_requirements: list[str]
    enforcement_actions: list[str]
    exemptions: list[str]
    oilfield_provisions: str
    last_amended: str

    def compute_hash(self) -> str:
        content = json.dumps({
            "id": self.rule_id,
            "district": self.district_name,
            "rule": self.rule_number,
            "description": self.description,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class SurfaceWaterRule:
    """Surface water appropriation rule."""
    rule_id: str
    title: str
    citation: str
    tceq_chapter: int
    description: str
    permit_types: list[str]
    priority_system: str
    beneficial_uses: list[str]
    exemptions: list[str]
    cancellation_provisions: str
    interstate_compact_notes: str

    def compute_hash(self) -> str:
        content = json.dumps({
            "id": self.rule_id, "title": self.title,
            "citation": self.citation, "description": self.description,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class ProducedWaterRegulation:
    """Produced water disposal regulation block."""
    regulation_id: str
    title: str
    agency: str
    citation: str
    description: str
    disposal_methods: list[str]
    permit_requirements: list[str]
    volume_limits: dict[str, Any]
    quality_standards: dict[str, Any]
    reporting_frequency: str
    violations_and_penalties: list[str]
    recycling_provisions: str

    def compute_hash(self) -> str:
        content = json.dumps({
            "id": self.regulation_id, "title": self.title,
            "citation": self.citation, "description": self.description,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class InjectionWellStandard:
    """UIC Class II injection well standard."""
    standard_id: str
    title: str
    agency: str
    citation: str
    well_class: str
    description: str
    construction_requirements: list[str]
    operational_limits: dict[str, Any]
    monitoring_requirements: list[str]
    mechanical_integrity_test: dict[str, Any]
    area_of_review: dict[str, Any]
    plugging_requirements: list[str]
    financial_assurance: dict[str, Any]
    seismicity_provisions: str

    def compute_hash(self) -> str:
        content = json.dumps({
            "id": self.standard_id, "title": self.title,
            "citation": self.citation, "description": self.description,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class AquiferProtectionRule:
    """Aquifer-specific protection rule."""
    rule_id: str
    aquifer_name: str
    title: str
    authority: str
    citation: str
    description: str
    protected_zones: list[str]
    prohibited_activities: list[str]
    permit_requirements: list[str]
    monitoring_requirements: list[str]
    remediation_standards: dict[str, Any]
    permian_basin_applicability: str

    def compute_hash(self) -> str:
        content = json.dumps({
            "id": self.rule_id, "aquifer": self.aquifer_name,
            "title": self.title, "description": self.description,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


# ---------------------------------------------------------------------------
# Doctrine blocks
# ---------------------------------------------------------------------------

TEXAS_WATER_DOCTRINES: list[TexasWaterDoctrine] = [
    # ---- GROUNDWATER / RULE OF CAPTURE ----
    TexasWaterDoctrine(
        doctrine_id="TWD-001",
        title="Rule of Capture (East Doctrine) - Absolute Ownership",
        category=DoctrineCategory.GROUNDWATER_CAPTURE,
        authority_level=AuthorityLevel.CASE_LAW,
        jurisdiction=JurisdictionScope.STATE_TEXAS,
        citation="Houston & T.C. Ry. Co. v. East, 98 Tex. 146, 81 S.W. 279 (1904)",
        summary=(
            "Texas follows the rule of capture for groundwater: a landowner may pump "
            "as much groundwater as they choose from beneath their land without liability "
            "to neighbors whose wells are affected, provided there is no malice, waste, "
            "willful waste, or negligent subsidence."
        ),
        detailed_analysis=(
            "The 1904 East decision established that percolating groundwater is the "
            "private property of the surface owner, analogous to ownership of the soil. "
            "The court reasoned that underground water movement is too uncertain and "
            "unknowable to impose liability for drainage. This absolute ownership theory "
            "means a landowner can pump unlimited quantities even if it drains a "
            "neighbor's well completely. The rule was reaffirmed in City of Corpus "
            "Christi v. City of Pleasanton (1955) and Sipriano v. Great Spring Waters "
            "of America (1999). In Edwards Aquifer Authority v. Day (2012), the Texas "
            "Supreme Court confirmed groundwater is real property owned in place. "
            "However, the rule of capture operates subject to groundwater conservation "
            "district regulations under TWC Chapter 36, which may limit production. "
            "The tension between absolute ownership and GCD regulation is the central "
            "issue in modern Texas groundwater law. For oil and gas operations, this "
            "means operators may source fresh or brackish groundwater for drilling and "
            "completions without necessarily needing neighbor consent, but must comply "
            "with any applicable GCD permitting requirements."
        ),
        key_provisions=[
            "Groundwater is real property owned in place by the surface owner",
            "Surface owner may pump unlimited quantities absent GCD regulation",
            "No liability for draining neighbor's well (absent malice/waste/subsidence)",
            "Rule applies to percolating groundwater, not underground streams",
            "GCD regulations may restrict the rule but cannot eliminate property right",
            "Landowner has standing to challenge GCD rules as regulatory takings",
            "Produced water from oil/gas operations is NOT subject to rule of capture",
        ],
        exceptions=[
            "Malicious pumping solely to injure neighbor",
            "Willful waste of groundwater",
            "Negligent withdrawal causing land subsidence",
            "GCD production limits and spacing rules",
            "Underground streams in defined channels (subject to TCEQ permitting)",
            "Spring flows connected to surface water (dual jurisdiction)",
        ],
        related_doctrines=["TWD-002", "TWD-003", "TWD-010", "TWD-015"],
        risk_if_violated=RiskLevel.HIGH,
        permian_basin_notes=(
            "Permian Basin operators routinely source groundwater for hydraulic "
            "fracturing under the rule of capture. Key consideration: most Permian "
            "Basin counties have active GCDs that impose permitting requirements "
            "for non-exempt wells (typically >25 GPM). Operators must verify GCD "
            "rules before drilling water wells for completion operations."
        ),
        last_updated="2024-01-15",
        tags=["rule_of_capture", "east_doctrine", "groundwater", "absolute_ownership",
              "property_right", "gcd_tension"],
    ),
    TexasWaterDoctrine(
        doctrine_id="TWD-002",
        title="Edwards Aquifer Authority v. Day - Groundwater as Property",
        category=DoctrineCategory.GROUNDWATER_CAPTURE,
        authority_level=AuthorityLevel.CASE_LAW,
        jurisdiction=JurisdictionScope.STATE_TEXAS,
        citation="Edwards Aquifer Auth. v. Day, 369 S.W.3d 814 (Tex. 2012)",
        summary=(
            "The Texas Supreme Court held that landowners own groundwater in place "
            "as real property, and GCD regulations that deny all economically "
            "beneficial use may constitute a compensable regulatory taking."
        ),
        detailed_analysis=(
            "Day resolved the long-standing question of whether groundwater is owned "
            "in place (like oil and gas under the ownership-in-place theory) or merely "
            "subject to a qualified right to capture. The Court held groundwater is "
            "owned in place, creating a vested property right. This means GCD "
            "regulations that deny all economically beneficial use of groundwater "
            "may require compensation under the Texas Constitution's takings clause. "
            "The decision did not eliminate GCD regulatory authority but established "
            "that GCDs must balance conservation goals against property rights. For "
            "oil and gas operators, Day provides legal support to challenge overly "
            "restrictive GCD rules that would prevent sourcing water for operations. "
            "The practical impact: GCDs cannot flatly prohibit groundwater production "
            "without facing takings liability."
        ),
        key_provisions=[
            "Groundwater is owned in place as real property",
            "Ownership-in-place theory extends from oil/gas to groundwater",
            "GCD regulations subject to regulatory takings analysis",
            "Penn Central balancing test applies to groundwater regulations",
            "Landowner may seek compensation if GCD denies all beneficial use",
            "Does not eliminate GCD authority to regulate for conservation",
        ],
        exceptions=[
            "GCDs retain broad regulatory authority under TWC Chapter 36",
            "Reasonable regulation for conservation is not a taking",
            "Nuisance-based restrictions remain valid",
            "Emergency drought restrictions likely survive takings challenge",
        ],
        related_doctrines=["TWD-001", "TWD-003", "TWD-010"],
        risk_if_violated=RiskLevel.MODERATE,
        permian_basin_notes=(
            "Day gives Permian Basin operators leverage against restrictive GCD "
            "rules. If a GCD denies a water well permit needed for completion "
            "operations, the operator may have a takings claim. However, most "
            "Permian GCDs grant permits with reasonable production limits."
        ),
        last_updated="2024-01-15",
        tags=["ownership_in_place", "regulatory_taking", "property_right", "gcd",
              "day_decision", "groundwater"],
    ),
    TexasWaterDoctrine(
        doctrine_id="TWD-003",
        title="Sipriano v. Great Spring Waters - Rule of Capture Reaffirmed",
        category=DoctrineCategory.GROUNDWATER_CAPTURE,
        authority_level=AuthorityLevel.CASE_LAW,
        jurisdiction=JurisdictionScope.STATE_TEXAS,
        citation="Sipriano v. Great Spring Waters of Am., 1 S.W.3d 75 (Tex. 1999)",
        summary=(
            "The Texas Supreme Court declined to replace the rule of capture with "
            "a reasonable use doctrine, holding that the Legislature's GCD framework "
            "was the preferred mechanism for groundwater management."
        ),
        detailed_analysis=(
            "Sipriano presented the court with an opportunity to adopt the Restatement "
            "(Second) of Torts reasonable use standard for groundwater. The Siprianos "
            "alleged that Ozarka's pumping of 90,000 gallons per day for commercial "
            "bottling dried up their domestic well. The Court acknowledged the rule of "
            "capture's harsh results but deferred to the Legislature, noting that TWC "
            "Chapter 36 (groundwater conservation districts) provides the mechanism "
            "for balancing competing groundwater uses. This decision means Texas "
            "retains the rule of capture as the common-law baseline, with GCDs as "
            "the primary regulatory overlay. For oil and gas operators, the holding "
            "confirms that pumping large volumes for industrial use (including frac "
            "water) does not inherently create liability, though GCD permits are "
            "still required where applicable."
        ),
        key_provisions=[
            "Rule of capture remains Texas common law for groundwater",
            "Court declined to adopt reasonable use standard",
            "Legislature (via GCDs) is the preferred regulatory mechanism",
            "Commercial/industrial pumping is lawful under rule of capture",
            "No common-law liability for pumping that dries neighbor's well",
            "GCDs provide the balancing mechanism between users",
        ],
        exceptions=[
            "GCD regulations override common-law rule of capture",
            "Malice or willful waste exceptions still apply",
            "Subsidence liability remains",
        ],
        related_doctrines=["TWD-001", "TWD-002"],
        risk_if_violated=RiskLevel.LOW,
        permian_basin_notes=(
            "Sipriano validates Permian Basin operators' practice of pumping large "
            "volumes for hydraulic fracturing. The key risk is not common-law "
            "liability but rather GCD regulatory compliance."
        ),
        last_updated="2024-01-15",
        tags=["rule_of_capture", "reasonable_use", "sipriano", "gcd_framework"],
    ),

    # ---- SURFACE WATER / PRIOR APPROPRIATION ----
    TexasWaterDoctrine(
        doctrine_id="TWD-010",
        title="Texas Prior Appropriation Doctrine - Surface Water",
        category=DoctrineCategory.SURFACE_WATER_APPROPRIATION,
        authority_level=AuthorityLevel.STATE_STATUTE,
        jurisdiction=JurisdictionScope.STATE_TEXAS,
        citation="Texas Water Code \u00a7\u00a7 11.001-11.560",
        summary=(
            "All surface water in Texas is property of the state held in trust for "
            "the public. Use requires a TCEQ water rights permit under a prior "
            "appropriation system: first in time, first in right."
        ),
        detailed_analysis=(
            "Unlike groundwater (owned in place by surface owner), surface water in "
            "Texas belongs to the state. TWC Chapter 11 establishes a prior "
            "appropriation system where the right to use surface water is acquired "
            "through a TCEQ permit. Priority date determines seniority: senior rights "
            "are satisfied before junior rights. During drought, junior permit holders "
            "may be curtailed. Domestic and livestock use of surface water is exempt "
            "from permitting (up to 200 AF/year). Oil and gas operations that need "
            "surface water (e.g., from a river for frac operations) must obtain a "
            "permit or purchase water from an existing permit holder. Bed and banks "
            "authorization is required to transport water through state watercourses. "
            "Key distinction: surface water rights are usufructuary (right to use, "
            "not own), unlike groundwater which is owned in place."
        ),
        key_provisions=[
            "Surface water is state property held in public trust",
            "Prior appropriation: first in time, first in right",
            "TCEQ permit required for diversion and use",
            "Domestic and livestock exempt up to 200 AF/year",
            "Permits specify purpose, place, rate, and amount",
            "Permits subject to cancellation for 10 years of non-use",
            "Water rights can be transferred, leased, or amended",
            "Bed and banks permit required for watercourse transport",
            "Environmental flow standards apply to new permits",
            "Interbasin transfer restrictions may apply",
        ],
        exceptions=[
            "Domestic and livestock use (up to 200 AF/year)",
            "Diffused surface water (not in defined channel)",
            "Certain pre-1913 riparian rights grandfathered",
            "Emergency temporary permits during drought",
        ],
        related_doctrines=["TWD-001", "TWD-011", "TWD-012"],
        risk_if_violated=RiskLevel.CRITICAL,
        permian_basin_notes=(
            "Surface water is scarce in the Permian Basin. The Pecos River is the "
            "primary surface water source, and its flows are governed by the Pecos "
            "River Compact (Texas-New Mexico). Most operators rely on groundwater "
            "or recycled produced water rather than surface water for completions."
        ),
        last_updated="2024-01-15",
        tags=["prior_appropriation", "surface_water", "tceq_permit", "water_code_ch11",
              "senior_rights", "junior_rights"],
    ),
    TexasWaterDoctrine(
        doctrine_id="TWD-011",
        title="Beneficial Use Requirement - Surface Water",
        category=DoctrineCategory.SURFACE_WATER_APPROPRIATION,
        authority_level=AuthorityLevel.STATE_STATUTE,
        jurisdiction=JurisdictionScope.STATE_TEXAS,
        citation="Texas Water Code \u00a7 11.025",
        summary=(
            "Surface water permits require beneficial use. Water must be put to a "
            "recognized beneficial purpose, and waste is prohibited. Industrial use "
            "(including oil and gas) is a recognized beneficial use."
        ),
        detailed_analysis=(
            "TWC \u00a7 11.025 requires that all surface water diversions serve a beneficial "
            "use. Recognized beneficial uses include domestic, municipal, industrial, "
            "irrigation, mining, hydroelectric, navigation, recreation, and livestock. "
            "Oil and gas operations fall under industrial use. The statute prohibits "
            "waste, defined as diverting more water than reasonably needed for the "
            "beneficial use. TCEQ may cancel a permit if the holder fails to use the "
            "water beneficially for 10 consecutive years. This use-it-or-lose-it "
            "provision means water rights holders must document actual use. For "
            "operators purchasing water from permit holders, the contract should "
            "confirm the seller has sufficient permitted volume and a valid permit."
        ),
        key_provisions=[
            "Beneficial use is the basis, measure, and limit of water rights",
            "Recognized uses: domestic, municipal, industrial, irrigation, mining",
            "Oil and gas operations = industrial beneficial use",
            "Waste of water is prohibited",
            "10-year non-use may result in permit cancellation",
            "TCEQ monitors and enforces beneficial use requirement",
        ],
        exceptions=[
            "Stored water in reservoirs has extended non-use protection",
            "Force majeure events toll the non-use period",
        ],
        related_doctrines=["TWD-010", "TWD-012"],
        risk_if_violated=RiskLevel.MODERATE,
        permian_basin_notes=(
            "Operators purchasing surface water for frac operations should confirm "
            "the seller's permit includes industrial use as a beneficial purpose. "
            "Some older irrigation permits may not authorize industrial sale."
        ),
        last_updated="2024-01-15",
        tags=["beneficial_use", "waste_prohibition", "use_it_or_lose_it"],
    ),
    TexasWaterDoctrine(
        doctrine_id="TWD-012",
        title="Environmental Flow Standards",
        category=DoctrineCategory.SURFACE_WATER_APPROPRIATION,
        authority_level=AuthorityLevel.STATE_STATUTE,
        jurisdiction=JurisdictionScope.STATE_TEXAS,
        citation="Texas Water Code \u00a7\u00a7 11.0235, 11.147(e); 30 TAC Chapter 298",
        summary=(
            "New surface water permits must include conditions to maintain adequate "
            "environmental flows for fish, wildlife, and river ecology. These flow "
            "standards reduce the amount of water available for new appropriations."
        ),
        detailed_analysis=(
            "Senate Bill 3 (2007) required TCEQ to adopt environmental flow standards "
            "for each river basin. These standards set minimum flow levels that must "
            "be maintained in rivers and streams before new permits can divert water. "
            "The environmental flow regime includes subsistence flows, base flows, "
            "and high-flow pulses. New permits are subject to these standards, which "
            "effectively reduce the volume available for new appropriations. Existing "
            "permits are generally grandfathered. For oil and gas operators seeking "
            "new surface water permits, environmental flow standards may limit "
            "available supply, particularly in drought conditions."
        ),
        key_provisions=[
            "Environmental flows required for all new surface water permits",
            "Standards set by basin-specific stakeholder committees",
            "Include subsistence, base, and high-flow pulse components",
            "TCEQ incorporates standards as permit conditions",
            "Existing permits generally grandfathered",
            "Adaptive management allows periodic updates",
        ],
        exceptions=[
            "Existing permits pre-dating standards",
            "Emergency drought exemptions",
            "De minimis diversions",
        ],
        related_doctrines=["TWD-010", "TWD-011"],
        risk_if_violated=RiskLevel.MODERATE,
        permian_basin_notes=(
            "The Pecos River basin has limited environmental flow standards due to "
            "historically low flows and the Pecos River Compact allocation. "
            "Environmental flow requirements are more impactful in eastern Texas "
            "basins with higher flows."
        ),
        last_updated="2024-01-15",
        tags=["environmental_flows", "sb3", "e_flows", "river_ecology"],
    ),

    # ---- GROUNDWATER CONSERVATION DISTRICTS ----
    TexasWaterDoctrine(
        doctrine_id="TWD-015",
        title="Groundwater Conservation District Authority - TWC Chapter 36",
        category=DoctrineCategory.GROUNDWATER_CONSERVATION_DISTRICT,
        authority_level=AuthorityLevel.STATE_STATUTE,
        jurisdiction=JurisdictionScope.STATE_TEXAS,
        citation="Texas Water Code \u00a7\u00a7 36.001-36.453",
        summary=(
            "GCDs are the preferred method of groundwater management in Texas. They "
            "have authority to issue permits, set spacing and production limits, and "
            "enforce rules within their jurisdictional boundaries."
        ),
        detailed_analysis=(
            "TWC Chapter 36 establishes groundwater conservation districts as the "
            "state's preferred method of managing groundwater resources. GCDs are "
            "created by the Legislature or through local elections. Key powers include: "
            "permitting wells, setting well spacing rules, limiting production, "
            "requiring metering and reporting, regulating well drilling, and enforcing "
            "conservation measures. GCDs must develop management plans consistent with "
            "the desired future conditions (DFCs) established by their Groundwater "
            "Management Area (GMA). Most GCDs exempt domestic and livestock wells "
            "producing less than 25 GPM. Oil and gas water wells typically require "
            "permits. GCDs may also regulate the transfer of groundwater outside "
            "district boundaries. For operators, the GCD is the primary regulatory "
            "interface for sourcing groundwater. Non-compliance can result in fines "
            "up to $10,000 per day per violation."
        ),
        key_provisions=[
            "GCDs are preferred method of groundwater management (TWC 36.0015)",
            "Authority to issue well permits with conditions",
            "Set spacing rules (minimum distance between wells)",
            "Impose production limits (volume per permit period)",
            "Require metering and annual reporting",
            "Regulate transfers outside district boundaries",
            "Enforce rules with penalties up to $10,000/day",
            "Must develop management plan consistent with DFCs",
            "May not discriminate between types of beneficial use",
            "Permit decisions appealable to district court",
        ],
        exceptions=[
            "Domestic and livestock wells under 25 GPM typically exempt",
            "Wells on tracts under 10 acres may be exempt",
            "Some GCDs exempt oil and gas water wells up to certain volumes",
            "Historic use permits may grandfather existing production",
        ],
        related_doctrines=["TWD-001", "TWD-002", "TWD-016", "TWD-017"],
        risk_if_violated=RiskLevel.HIGH,
        permian_basin_notes=(
            "Nearly all Permian Basin counties have active GCDs. Operators must "
            "obtain permits before drilling water wells for frac supply. Key GCDs: "
            "Midland Co. GWCD, Ector Co. GWCD, Pecos Valley WD (Reeves Co.), "
            "Martin Co. UWCD, Winkler Co. GWCD. Each has different rules, so "
            "operators working across counties must track multiple GCD regimes."
        ),
        last_updated="2024-01-15",
        tags=["gcd", "chapter_36", "well_permits", "spacing_rules", "production_limits",
              "management_plan", "dfc"],
    ),
    TexasWaterDoctrine(
        doctrine_id="TWD-016",
        title="Desired Future Conditions (DFCs) and Joint Planning",
        category=DoctrineCategory.GROUNDWATER_CONSERVATION_DISTRICT,
        authority_level=AuthorityLevel.STATE_STATUTE,
        jurisdiction=JurisdictionScope.REGIONAL,
        citation="Texas Water Code \u00a7\u00a7 36.108, 36.1081-36.1086",
        summary=(
            "GCDs within each Groundwater Management Area must jointly adopt "
            "desired future conditions (DFCs) for shared aquifers, setting the "
            "target condition of the aquifer 50 years out."
        ),
        detailed_analysis=(
            "DFCs define the future condition of an aquifer that GCDs within a GMA "
            "agree to manage toward. Typically expressed as a target level of aquifer "
            "drawdown or water level decline over 50 years. TWDB uses DFCs to "
            "calculate modeled available groundwater (MAG) for each GCD, which "
            "informs individual GCD permitting decisions. DFCs are adopted jointly "
            "by GCDs in a GMA by a 2/3 vote. They are reviewed every 5 years. "
            "Affected parties may challenge DFCs through a petition process. For "
            "operators, the DFC process determines how much groundwater is legally "
            "available from a given aquifer zone, directly impacting water supply "
            "planning for multi-year development programs."
        ),
        key_provisions=[
            "DFCs set 50-year target aquifer condition",
            "Adopted jointly by GCDs within GMA (2/3 vote)",
            "TWDB calculates modeled available groundwater from DFCs",
            "MAG determines volume available for GCD permitting",
            "Reviewed every 5 years (may be revised)",
            "Petition process for affected parties to challenge DFCs",
            "Must consider impacts on property rights and economics",
        ],
        exceptions=[
            "GCDs may adopt more protective standards than the DFC requires",
            "Drought conditions may trigger temporary restrictions beyond DFC levels",
        ],
        related_doctrines=["TWD-015", "TWD-017"],
        risk_if_violated=RiskLevel.MODERATE,
        permian_basin_notes=(
            "GMA 7 (Permian Basin region) has adopted DFCs for the Ogallala, "
            "Edwards-Trinity, and Pecos Valley aquifers. The Ogallala DFC allows "
            "significant drawdown (50%+ decline in saturated thickness over 50 "
            "years), reflecting agricultural and industrial demand. Operators should "
            "monitor DFC revisions that could tighten future allocations."
        ),
        last_updated="2024-01-15",
        tags=["dfc", "gma", "joint_planning", "mag", "twdb", "50_year_target"],
    ),
    TexasWaterDoctrine(
        doctrine_id="TWD-017",
        title="GCD Export Restrictions - Groundwater Transport",
        category=DoctrineCategory.GROUNDWATER_CONSERVATION_DISTRICT,
        authority_level=AuthorityLevel.STATE_STATUTE,
        jurisdiction=JurisdictionScope.GCD_LOCAL,
        citation="Texas Water Code \u00a7\u00a7 36.122, 36.113(d)(2)",
        summary=(
            "GCDs may impose conditions on exporting groundwater outside their "
            "boundaries but cannot prohibit export entirely. Export fees and "
            "conditions must be reasonable."
        ),
        detailed_analysis=(
            "TWC \u00a7 36.122 allows GCDs to require a separate export permit for "
            "groundwater transported outside the district. GCDs may impose export "
            "fees and conditions (e.g., reduced volume, shorter permit term, "
            "conservation measures). However, they cannot prohibit exports entirely "
            "or set export fees that effectively prevent transfer. Guitar Holding "
            "Company v. Hudspeth County UWCD No. 1 (2008) established that GCDs "
            "must treat export permit applications fairly. For operators with multi-"
            "county operations, water sourced in one GCD may be subject to export "
            "restrictions when transported to wells in another county."
        ),
        key_provisions=[
            "GCDs may require separate export permits",
            "Export fees must be reasonable (not punitive)",
            "Cannot prohibit export entirely (commerce clause issues)",
            "Export permits may have shorter terms than in-district permits",
            "Must provide equal protection to in-district and out-of-district uses",
            "Export conditions reviewable by district court",
        ],
        exceptions=[
            "Water transported for emergency use",
            "Small volumes (varies by GCD)",
            "Water transported within same GMA may have reduced restrictions",
        ],
        related_doctrines=["TWD-015", "TWD-016"],
        risk_if_violated=RiskLevel.MODERATE,
        permian_basin_notes=(
            "Permian Basin operators frequently transport water across county/GCD "
            "lines. Each GCD has different export rules. Operators should obtain "
            "export permits before transporting water across GCD boundaries. "
            "Some GCDs charge export surcharges of $0.25-$1.00 per 1,000 gallons."
        ),
        last_updated="2024-01-15",
        tags=["export_restriction", "water_transport", "gcd_export", "commerce_clause"],
    ),

    # ---- PRODUCED WATER DISPOSAL ----
    TexasWaterDoctrine(
        doctrine_id="TWD-020",
        title="RRC Statewide Rule 9 - Disposal and Injection Wells",
        category=DoctrineCategory.PRODUCED_WATER_DISPOSAL,
        authority_level=AuthorityLevel.STATE_REGULATION,
        jurisdiction=JurisdictionScope.STATE_TEXAS,
        citation="16 TAC \u00a7 3.9; Railroad Commission Statewide Rule 9",
        summary=(
            "RRC Statewide Rule 9 governs the disposal of oil and gas waste by "
            "injection into formations not productive of oil or gas. Requires "
            "H-1 permit and compliance with injection pressure, volume, and "
            "monitoring requirements."
        ),
        detailed_analysis=(
            "Statewide Rule 9 is the primary regulation for saltwater disposal wells "
            "(SWDs) and other injection wells used to dispose of produced water, "
            "completion fluids, and other oilfield waste. Key requirements: operators "
            "must file a Form H-1 application, demonstrate that the proposed injection "
            "zone is separated from USDWs by adequate confining layers, meet casing "
            "and cementing standards, maintain mechanical integrity, and comply with "
            "injection pressure and volume limits. The rule requires an area of review "
            "(AOR) analysis to identify nearby wells that could serve as conduits for "
            "injected fluids. Annual monitoring reports are required. Recent amendments "
            "address seismicity: operators in seismicity review areas must conduct "
            "additional analysis and may be subject to volume curtailment or "
            "shut-in orders if earthquakes occur nearby."
        ),
        key_provisions=[
            "H-1 permit required for all disposal/injection wells",
            "Injection zone must be isolated from USDWs",
            "Casing and cementing must prevent migration to fresh water",
            "Maximum injection pressure: 0.5 PSI per foot of depth (default)",
            "Area of review: 1/4 mile radius from wellbore",
            "Mechanical integrity test (MIT) every 5 years minimum",
            "Annual monitoring and reporting required",
            "Financial assurance: $25K per well or $250K blanket bond",
            "Commercial disposal wells have additional requirements",
            "Seismicity monitoring in designated review areas",
        ],
        exceptions=[
            "Enhanced recovery wells (EOR) have separate Rule 46 requirements",
            "Produced water recycling/reuse does not require disposal permit",
            "Temporary pits for completion fluid may not need H-1 if within exemptions",
        ],
        related_doctrines=["TWD-021", "TWD-022", "TWD-025", "TWD-030"],
        risk_if_violated=RiskLevel.CRITICAL,
        permian_basin_notes=(
            "The Permian Basin has the highest density of SWDs in Texas. Operators "
            "dispose of millions of barrels per day. Typical Permian produced water "
            "TDS: 150,000-300,000+ mg/L. Key disposal formations: Ellenburger, "
            "Delaware Mountain Group, San Andres. Seismicity concerns have led to "
            "RRC-imposed volume curtailments in parts of the Delaware Basin."
        ),
        last_updated="2024-06-01",
        tags=["statewide_rule_9", "swd", "h1_permit", "injection", "disposal",
              "produced_water", "rrc"],
    ),
    TexasWaterDoctrine(
        doctrine_id="TWD-021",
        title="UIC Class II Program - Federal-State Framework",
        category=DoctrineCategory.INJECTION_WELL_REGULATION,
        authority_level=AuthorityLevel.FEDERAL_STATUTE,
        jurisdiction=JurisdictionScope.STATE_TEXAS,
        citation="Safe Drinking Water Act \u00a7 1421; 42 U.S.C. \u00a7 300h; 40 CFR Part 144-148",
        summary=(
            "Texas has EPA-delegated primacy for the Underground Injection Control "
            "(UIC) Class II program covering oil-and-gas-related injection wells. "
            "RRC administers the program under state rules consistent with federal "
            "minimum standards."
        ),
        detailed_analysis=(
            "The Safe Drinking Water Act (SDWA) establishes the UIC program to "
            "prevent underground injection from endangering underground sources of "
            "drinking water (USDWs). Class II wells include: enhanced recovery (IIR), "
            "disposal of oilfield brine (IID), and liquid hydrocarbon storage (IIS). "
            "Texas received EPA primacy in 1982, meaning the Railroad Commission "
            "administers the program rather than EPA directly. RRC rules must be at "
            "least as stringent as federal requirements. Key federal requirements "
            "include: no migration of fluids into USDWs, mechanical integrity testing, "
            "proper well construction, area of review analysis, monitoring, and "
            "financial responsibility. EPA retains oversight authority and can take "
            "enforcement action if the state program is inadequate. Aquifer exemptions "
            "require EPA approval even though RRC has primacy."
        ),
        key_provisions=[
            "Texas has EPA-delegated primacy for UIC Class II",
            "RRC administers program, EPA retains oversight",
            "Must prevent fluid migration into USDWs (<10,000 mg/L TDS)",
            "Well construction: surface casing below freshwater, cement to surface",
            "Mechanical integrity testing at permit and periodically",
            "Area of review for nearby penetrations",
            "Monitoring and reporting to RRC",
            "Financial responsibility for well plugging",
            "Aquifer exemptions require EPA approval",
        ],
        exceptions=[
            "Class I wells (non-oil-and-gas hazardous) remain under TCEQ/EPA",
            "Class V wells (misc. shallow injection) separate program",
            "Aquifer exemptions allow injection into otherwise-USDW formations",
        ],
        related_doctrines=["TWD-020", "TWD-022", "TWD-025"],
        risk_if_violated=RiskLevel.CRITICAL,
        permian_basin_notes=(
            "EPA Region 6 (Dallas) oversees RRC's Class II program. Several "
            "Permian Basin disposal formations have received aquifer exemptions "
            "(e.g., parts of the Rustler, Delaware Mountain Group where TDS is "
            "naturally high). Operators should verify exemption status before "
            "proposing injection into formations with TDS near the 10,000 mg/L "
            "USDW threshold."
        ),
        last_updated="2024-01-15",
        tags=["uic", "class_ii", "sdwa", "epa_primacy", "usdw_protection",
              "underground_injection"],
    ),
    TexasWaterDoctrine(
        doctrine_id="TWD-022",
        title="Mechanical Integrity Testing Requirements",
        category=DoctrineCategory.INJECTION_WELL_REGULATION,
        authority_level=AuthorityLevel.STATE_REGULATION,
        jurisdiction=JurisdictionScope.STATE_TEXAS,
        citation="16 TAC \u00a7 3.46; RRC Statewide Rule 46",
        summary=(
            "All Class II injection/disposal wells must demonstrate mechanical "
            "integrity through pressure testing. Failure results in well shut-in "
            "until integrity is restored."
        ),
        detailed_analysis=(
            "Mechanical integrity testing (MIT) ensures that injection wells are "
            "not leaking injected fluids into unauthorized zones, particularly "
            "USDWs. MIT has two components: (1) no significant leak in the casing, "
            "tubing, or packer (demonstrated by pressure test); and (2) no "
            "significant fluid migration through vertical channels adjacent to the "
            "wellbore (demonstrated by cement evaluation logs or tracer surveys). "
            "Standard pressure test: apply 300 PSI for 30 minutes with less than "
            "5% pressure decline. Wells failing MIT must be shut in immediately "
            "and repaired before resuming injection. RRC requires MIT at initial "
            "permit, whenever workovers alter well integrity, and at least every "
            "5 years. Operators in seismicity review areas may face more frequent "
            "MIT requirements. Chronic MIT failures can lead to permit revocation."
        ),
        key_provisions=[
            "MIT required at permit, after workover, and every 5 years",
            "Pressure test: 300 PSI for 30 min, <5% decline",
            "Failed MIT = immediate shut-in until repaired",
            "Cement evaluation log may be required for Part 2 MIT",
            "Seismicity areas may have more frequent MIT schedule",
            "Chronic failures can result in permit revocation",
            "All MIT results reported to RRC within 30 days",
        ],
        exceptions=[
            "Alternative MIT methods may be approved by RRC",
            "Low-pressure wells may use modified test procedures",
        ],
        related_doctrines=["TWD-020", "TWD-021"],
        risk_if_violated=RiskLevel.CRITICAL,
        permian_basin_notes=(
            "Permian Basin SWDs frequently inject at high pressures. MIT failures "
            "are a leading cause of well shut-ins. Operators should budget for "
            "remedial workovers (squeeze cement, packer replacements) to maintain "
            "MIT compliance."
        ),
        last_updated="2024-01-15",
        tags=["mechanical_integrity", "mit", "pressure_test", "well_integrity",
              "casing_leak", "cement_evaluation"],
    ),

    # ---- FRESHWATER PROTECTION ----
    TexasWaterDoctrine(
        doctrine_id="TWD-025",
        title="Underground Source of Drinking Water (USDW) Protection",
        category=DoctrineCategory.FRESHWATER_PROTECTION,
        authority_level=AuthorityLevel.FEDERAL_REGULATION,
        jurisdiction=JurisdictionScope.FEDERAL,
        citation="40 CFR \u00a7 144.3; Safe Drinking Water Act \u00a7 1421",
        summary=(
            "USDWs are aquifers with TDS below 10,000 mg/L that are current or "
            "potential drinking water sources. Oil and gas operations must not "
            "contaminate USDWs through drilling, injection, or disposal."
        ),
        detailed_analysis=(
            "The SDWA defines USDWs as aquifers containing water with TDS less "
            "than 10,000 mg/L that is currently used or could reasonably be used "
            "as a drinking water source. Protecting USDWs is the central mandate "
            "of the UIC program. Key protection mechanisms: surface casing must "
            "be set and cemented through all freshwater zones, injection wells must "
            "be isolated from USDWs, monitoring wells may be required, and any "
            "contamination must be reported and remediated. In Texas, surface "
            "casing depth is determined by the groundwater protection determination "
            "(GPD) letter from RRC, which specifies the depth to which casing must "
            "be cemented to protect freshwater. Operators must also protect USDWs "
            "during drilling (proper mud weight, casing program) and plugging "
            "(cement across freshwater zones)."
        ),
        key_provisions=[
            "USDW: aquifer with TDS < 10,000 mg/L",
            "Surface casing cemented through all freshwater zones",
            "RRC groundwater protection determination (GPD) sets casing depth",
            "No injection into USDWs without aquifer exemption",
            "Monitoring wells may be required near injection wells",
            "Spill/leak notification within 24 hours",
            "Remediation required for any USDW contamination",
            "Well plugging must include cement across freshwater zones",
        ],
        exceptions=[
            "Aquifer exemption: EPA may exempt an aquifer from USDW protection",
            "Exemption requires: aquifer not current drinking water source, "
            "minerals of economic value, too contaminated, or too deep to be feasible",
        ],
        related_doctrines=["TWD-020", "TWD-021", "TWD-026"],
        risk_if_violated=RiskLevel.CRITICAL,
        permian_basin_notes=(
            "In the Permian Basin, freshwater protection depths vary significantly. "
            "West of the Pecos River, freshwater may extend to 200-400 ft. In the "
            "Midland Basin, freshwater can extend to 500-1,000 ft. Operators must "
            "obtain a GPD letter from RRC before spudding any well to confirm "
            "required surface casing depth."
        ),
        last_updated="2024-01-15",
        tags=["usdw", "freshwater_protection", "surface_casing", "gpd",
              "tds_10000", "drinking_water"],
    ),
    TexasWaterDoctrine(
        doctrine_id="TWD-026",
        title="Aquifer Exemption Process",
        category=DoctrineCategory.FRESHWATER_PROTECTION,
        authority_level=AuthorityLevel.FEDERAL_REGULATION,
        jurisdiction=JurisdictionScope.FEDERAL,
        citation="40 CFR \u00a7 146.4; SDWA \u00a7 1421(d)(2)",
        summary=(
            "Aquifers otherwise meeting USDW criteria may be exempted from "
            "protection if they meet specific criteria. EPA approval is required "
            "even in primacy states like Texas."
        ),
        detailed_analysis=(
            "An aquifer exemption allows injection into a formation that would "
            "otherwise be classified as a USDW. Criteria for exemption: (1) the "
            "aquifer does not currently serve as a source of drinking water; (2) it "
            "cannot serve as a future source because it is mineral, hydrocarbon, or "
            "geothermal energy producing; (3) it is too contaminated to be treated "
            "economically; or (4) it is too deep or remote to be a feasible drinking "
            "water source. The process requires RRC to submit an application to EPA "
            "Region 6, including hydrogeologic data demonstrating the aquifer meets "
            "exemption criteria. EPA publishes notice and takes public comment. "
            "Exemptions are typically granted for specific areal extents and depth "
            "intervals. In the Permian Basin, several formations have been exempted "
            "to enable disposal and enhanced recovery operations."
        ),
        key_provisions=[
            "EPA approval required (even in primacy states)",
            "Four criteria for exemption (not-drinking-water, mineral producing, "
            "contaminated, infeasible)",
            "RRC submits application on behalf of operators",
            "Public notice and comment required",
            "Exemption tied to specific area and depth interval",
            "Cannot exempt portion of aquifer that serves existing wells",
        ],
        exceptions=[
            "No exemption for aquifers serving existing public water systems",
            "Exemption may be revoked if conditions change",
        ],
        related_doctrines=["TWD-025", "TWD-021"],
        risk_if_violated=RiskLevel.HIGH,
        permian_basin_notes=(
            "Several Permian Basin formations (portions of Rustler, Delaware Mtn "
            "Group, San Andres) have aquifer exemptions. Operators should confirm "
            "exemption status with RRC before proposing injection in formations "
            "with TDS between 3,000 and 10,000 mg/L."
        ),
        last_updated="2024-01-15",
        tags=["aquifer_exemption", "epa_approval", "usdw_exemption", "formation_exemption"],
    ),

    # ---- EDWARDS AQUIFER ----
    TexasWaterDoctrine(
        doctrine_id="TWD-030",
        title="Edwards Aquifer Authority Act",
        category=DoctrineCategory.EDWARDS_AQUIFER,
        authority_level=AuthorityLevel.STATE_STATUTE,
        jurisdiction=JurisdictionScope.REGIONAL,
        citation="Edwards Aquifer Authority Act, Act of May 30, 1993, 73rd Leg., ch. 626",
        summary=(
            "The Edwards Aquifer Authority (EAA) regulates all groundwater "
            "withdrawals from the Edwards Aquifer in south-central Texas with "
            "a cap of 572,000 AF/year and a critical period management plan."
        ),
        detailed_analysis=(
            "The EAA Act is the most restrictive groundwater regulation in Texas. "
            "It caps total withdrawals from the Edwards Aquifer at 572,000 AF/year "
            "(reduced from historical use of 700,000+ AF/year). Permits are allocated "
            "based on historical use. A critical period management plan reduces pumping "
            "during drought based on springflow at Comal Springs (San Marcos Springs). "
            "Five critical period stages progressively curtail withdrawals. Market-"
            "based transfers allow permit holders to sell or lease their rights, "
            "creating a water market. The EAA model is unique in Texas: it replaces "
            "the rule of capture with a regulated allocation system. While not "
            "directly applicable to Permian Basin operations, the EAA model is "
            "important precedent for potential future regulation of other aquifers."
        ),
        key_provisions=[
            "Annual cap: 572,000 AF/year total Edwards Aquifer withdrawals",
            "Permits based on historical use (initial regular permits)",
            "Critical period management: 5 stages based on springflow",
            "Stage I: Comal < 225 cfs → 20% curtailment",
            "Stage V: Comal < 40 cfs → near-total curtailment",
            "Market-based permit transfers allowed",
            "No new initial regular permits (only term permits)",
            "Metering required on all permitted wells",
            "EAA regulatory fee per acre-foot (~$52)",
        ],
        exceptions=[
            "Domestic and livestock wells on <5 acres exempt (limited volume)",
            "Emergency permits during drought",
            "Permit transfers within the EAA jurisdiction",
        ],
        related_doctrines=["TWD-001", "TWD-015"],
        risk_if_violated=RiskLevel.CRITICAL,
        permian_basin_notes=(
            "The Edwards Aquifer is not in the Permian Basin. However, the EAA "
            "model is important precedent. If Permian Basin aquifer depletion "
            "becomes critical, legislators may look to the EAA framework as a "
            "model for more restrictive regulation."
        ),
        last_updated="2024-01-15",
        tags=["edwards_aquifer", "eaa", "572000_cap", "critical_period",
              "springflow", "water_market"],
    ),

    # ---- WATER RECYCLING / REUSE ----
    TexasWaterDoctrine(
        doctrine_id="TWD-035",
        title="Produced Water Recycling and Reuse in Hydraulic Fracturing",
        category=DoctrineCategory.WATER_RECYCLING_REUSE,
        authority_level=AuthorityLevel.STATE_REGULATION,
        jurisdiction=JurisdictionScope.STATE_TEXAS,
        citation="16 TAC \u00a7 3.8; RRC Statewide Rule 8; TWC \u00a7 122.001 et seq.",
        summary=(
            "Texas encourages recycling of produced water and flowback for use "
            "in subsequent hydraulic fracturing operations. Recycled water used "
            "downhole does not require a disposal permit. Surface discharge of "
            "treated produced water requires TCEQ authorization."
        ),
        detailed_analysis=(
            "Produced water recycling has become a major practice in the Permian "
            "Basin, driven by water scarcity and disposal constraints. Under RRC "
            "rules, produced water that is recycled for use in subsequent hydraulic "
            "fracturing or other downhole operations does not require a disposal "
            "permit (H-1). The RRC treats this as beneficial reuse, not disposal. "
            "However, storage and handling of recycled water must comply with "
            "Statewide Rule 8 (water protection). Produced water pits must be "
            "lined, and spills must be reported. If produced water is treated for "
            "surface discharge or beneficial reuse outside the oilfield (e.g., "
            "irrigation, livestock watering), TCEQ discharge authorization is "
            "required. TWC Chapter 122 (added by HB 2771, 2019) authorizes "
            "the production, treatment, and use of fluid oil and gas waste for "
            "beneficial purposes. This statute created a pathway for treated "
            "produced water to be used outside the oilfield."
        ),
        key_provisions=[
            "Recycled produced water for downhole use: no disposal permit needed",
            "Storage must comply with RRC Statewide Rule 8 (pits, liners, spills)",
            "Surface discharge of treated produced water requires TCEQ permit",
            "TWC Chapter 122: beneficial reuse of treated oilfield waste authorized",
            "RRC retains jurisdiction over oilfield recycling operations",
            "TCEQ has jurisdiction over discharge to surface water",
            "Operators may blend recycled water with fresh/brackish for frac",
            "No NORM screening required for downhole reuse (but recommended)",
            "Recycling facilities do not need separate disposal permits",
        ],
        exceptions=[
            "Surface discharge requires TCEQ authorization (not RRC)",
            "Land application of treated produced water needs TCEQ permit",
            "NORM-contaminated water may have additional handling requirements",
        ],
        related_doctrines=["TWD-020", "TWD-036", "TWD-040"],
        risk_if_violated=RiskLevel.MODERATE,
        permian_basin_notes=(
            "Permian Basin recycling has grown dramatically since 2018. Major "
            "operators now recycle 30-80% of produced water. Key challenges: "
            "high TDS (200,000-300,000 mg/L), scale-forming minerals, bacteria, "
            "and logistics. Produced water midstream companies (e.g., Solaris, "
            "WaterBridge, Breakwater) operate large recycling systems. Recycling "
            "reduces SWD injection volumes and mitigates seismicity risk."
        ),
        last_updated="2024-06-01",
        tags=["recycling", "reuse", "produced_water", "hb2771", "chapter_122",
              "beneficial_reuse", "frac_water"],
    ),
    TexasWaterDoctrine(
        doctrine_id="TWD-036",
        title="Brackish Water Desalination for Oil and Gas",
        category=DoctrineCategory.BRACKISH_DESALINATION,
        authority_level=AuthorityLevel.STATE_STATUTE,
        jurisdiction=JurisdictionScope.STATE_TEXAS,
        citation="TWC \u00a7\u00a7 16.060, 36.1015; TWDB Brackish Resources Aquifer Characterization System",
        summary=(
            "Texas promotes brackish groundwater desalination as an alternative "
            "water source. TWDB has mapped brackish production zones. GCDs may "
            "issue separate permits for brackish water wells."
        ),
        detailed_analysis=(
            "Brackish groundwater (1,000-10,000 mg/L TDS) represents a vast "
            "untapped resource in Texas. The TWDB's Brackish Resources Aquifer "
            "Characterization System (BRACS) maps brackish zones statewide. TWC "
            "\u00a7 36.1015 authorizes GCDs to issue permits for brackish water wells "
            "with conditions separate from fresh groundwater permits. For oil and "
            "gas operations, brackish water is an attractive alternative to fresh "
            "water for hydraulic fracturing: less regulatory friction than fresh "
            "groundwater (since GCDs may have more permissive rules for brackish), "
            "reduced community opposition, and reduced impact on drinking water "
            "supplies. Desalination concentrate disposal is the key challenge: "
            "options include deep well injection, evaporation ponds, or zero "
            "liquid discharge (ZLD) systems. In the Permian Basin, the Dockum and "
            "Rustler formations provide brackish water that can be treated to frac "
            "specifications at lower cost than full desalination."
        ),
        key_provisions=[
            "TWDB maps brackish zones statewide (BRACS program)",
            "GCDs may issue separate brackish permits (TWC 36.1015)",
            "Brackish: 1,000-10,000 mg/L TDS",
            "Concentrate disposal requires separate permit",
            "TWDB funding available for desalination projects",
            "No statewide prohibition on brackish water production",
            "GCDs may set different rules for brackish vs fresh wells",
        ],
        exceptions=[
            "Some GCDs treat all groundwater the same regardless of quality",
            "Concentrate disposal adds cost and permitting complexity",
            "USDW protection still applies to aquifers with TDS < 10,000 mg/L",
        ],
        related_doctrines=["TWD-015", "TWD-025", "TWD-035"],
        risk_if_violated=RiskLevel.LOW,
        permian_basin_notes=(
            "Permian Basin brackish water sources: Dockum (1,000-10,000 mg/L), "
            "Rustler (3,000-35,000 mg/L), Santa Rosa (500-3,000 mg/L). Several "
            "operators have piloted brackish water treatment for frac supply. "
            "Economics depend on TDS, treatment technology, and distance from "
            "wells. TWDB has designated brackish production zones in several "
            "Permian Basin aquifers."
        ),
        last_updated="2024-01-15",
        tags=["brackish", "desalination", "bracs", "twdb", "concentrate_disposal",
              "alternative_water"],
    ),

    # ---- WATER TRANSPORT & MIDSTREAM ----
    TexasWaterDoctrine(
        doctrine_id="TWD-040",
        title="Produced Water Midstream and Pipeline Regulation",
        category=DoctrineCategory.WATER_TRANSPORT_MIDSTREAM,
        authority_level=AuthorityLevel.STATE_REGULATION,
        jurisdiction=JurisdictionScope.STATE_TEXAS,
        citation="16 TAC \u00a7 3.57 (Pipeline Permits); TWC \u00a7 122; Tex. Nat. Res. Code \u00a7 81.0521",
        summary=(
            "Produced water pipeline systems (gathering and disposal) are regulated "
            "by RRC. Pipeline permits, right-of-way agreements, leak detection, and "
            "spill response plans are required for produced water midstream operations."
        ),
        detailed_analysis=(
            "The produced water midstream sector has grown rapidly in the Permian "
            "Basin, with dedicated pipeline networks gathering produced water from "
            "wellsites and transporting it to disposal wells or recycling facilities. "
            "RRC requires pipeline permits for produced water lines crossing multiple "
            "tracts. Right-of-way agreements with surface owners are necessary. "
            "Pipeline operators must implement leak detection systems and maintain "
            "spill response plans. Surface owner accommodation doctrine applies: "
            "pipeline routes should minimize interference with surface use. "
            "Eminent domain authority is available for some produced water pipelines "
            "under Tex. Nat. Res. Code \u00a7 81.0521 (common carrier/gatherer status). "
            "Key operational requirements: hydrostatic testing, corrosion protection "
            "(produced water is highly corrosive), and emergency shutdown capability."
        ),
        key_provisions=[
            "RRC pipeline permit required for produced water gathering lines",
            "Right-of-way agreements required with surface owners",
            "Leak detection systems required",
            "Spill response plan required",
            "Hydrostatic pressure testing before commissioning",
            "Corrosion protection (internal and external)",
            "Emergency shutdown capability",
            "Common carrier/gatherer status available for eminent domain",
            "Produced water pipeline operators must register with RRC",
        ],
        exceptions=[
            "On-lease flowlines (within single lease) may have reduced requirements",
            "Temporary water transfer lines (<180 days) have simplified permitting",
        ],
        related_doctrines=["TWD-020", "TWD-035", "TWD-041"],
        risk_if_violated=RiskLevel.HIGH,
        permian_basin_notes=(
            "Major Permian Basin produced water midstream companies: Solaris Water, "
            "WaterBridge, Breakwater Midstream, Layne Water Midstream, Nuverra. "
            "Pipeline networks now span hundreds of miles. Key risk: pipeline leaks "
            "in environmentally sensitive areas (e.g., near Pecos River, playa lakes). "
            "Operators should conduct due diligence on midstream company compliance "
            "records before signing gathering agreements."
        ),
        last_updated="2024-06-01",
        tags=["pipeline", "midstream", "produced_water", "gathering_system",
              "right_of_way", "leak_detection"],
    ),
    TexasWaterDoctrine(
        doctrine_id="TWD-041",
        title="Surface Owner Accommodation Doctrine - Water Access",
        category=DoctrineCategory.SURFACE_OWNER_ACCOMMODATION,
        authority_level=AuthorityLevel.CASE_LAW,
        jurisdiction=JurisdictionScope.STATE_TEXAS,
        citation="Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971); Merriman v. XTO Energy, 407 S.W.3d 244 (Tex. 2013)",
        summary=(
            "The accommodation doctrine requires mineral owners/lessees to use "
            "existing surface alternatives when reasonably available, rather than "
            "methods that would substantially impair the surface owner's existing "
            "use. This includes water well and water source access."
        ),
        detailed_analysis=(
            "Under the accommodation doctrine (Getty Oil, 1971), the dominant "
            "mineral estate must accommodate existing surface uses when there "
            "are reasonable alternatives available. Merriman v. XTO (2013) "
            "extended this to protect surface owner water wells: an operator "
            "cannot site a saltwater disposal facility in a location that "
            "would contaminate the surface owner's domestic water well if "
            "alternative locations exist. Key elements: (1) the surface owner "
            "must have an existing use (e.g., water well for domestic/livestock); "
            "(2) the mineral owner's proposed activity would substantially impair "
            "that use; (3) reasonable alternatives exist for the mineral owner. "
            "If all three are met, the operator must accommodate. This doctrine "
            "is particularly important for water rights because surface owners "
            "depend on groundwater wells, and oil and gas operations can "
            "contaminate those wells through spills, leaks, or disposal well "
            "failures. Operators should map all surface owner water wells "
            "before siting facilities."
        ),
        key_provisions=[
            "Mineral estate is dominant but must accommodate existing surface uses",
            "Surface owner must have pre-existing use being impaired",
            "Operator must use alternatives if reasonably available",
            "Applies to water well protection from contamination risk",
            "Surface owner cannot veto mineral operations entirely",
            "Case-by-case factual analysis required",
            "Operator should document consideration of alternatives",
        ],
        exceptions=[
            "Does not apply if no reasonable alternative exists for operator",
            "Surface owner cannot demand accommodation for future/planned uses",
            "Lease terms may modify accommodation obligations",
        ],
        related_doctrines=["TWD-025", "TWD-040"],
        risk_if_violated=RiskLevel.HIGH,
        permian_basin_notes=(
            "Permian Basin surface owners increasingly assert accommodation "
            "doctrine claims related to water. Common disputes: SWD facility "
            "siting near domestic wells, frac water pit construction near "
            "livestock water sources, pipeline routing through irrigated fields. "
            "Operators should conduct pre-development surface surveys including "
            "water well mapping."
        ),
        last_updated="2024-01-15",
        tags=["accommodation_doctrine", "surface_owner", "water_well_protection",
              "getty_oil", "merriman", "dominant_estate"],
    ),

    # ---- SEISMICITY ----
    TexasWaterDoctrine(
        doctrine_id="TWD-045",
        title="RRC Seismicity Response - Disposal Well Curtailment",
        category=DoctrineCategory.SEISMICITY_REGULATION,
        authority_level=AuthorityLevel.AGENCY_RULE,
        jurisdiction=JurisdictionScope.STATE_TEXAS,
        citation="RRC Disposal Well Seismicity Response; 16 TAC \u00a7 3.9 (as amended)",
        summary=(
            "RRC has implemented a seismicity response protocol for disposal wells "
            "in designated seismicity review areas. Operators may face volume "
            "curtailment, pressure reduction, or well shut-in based on earthquake "
            "magnitude and proximity."
        ),
        detailed_analysis=(
            "In response to increasing seismic activity correlated with produced "
            "water disposal, RRC established seismicity review areas and a traffic "
            "light response protocol. The protocol uses TexNet seismic monitoring "
            "data to trigger regulatory actions: Green (<M2.0, continue); Yellow "
            "(M2.0-M3.5, reduce volume 50%); Orange (M3.5-M4.0, suspend and "
            "review); Red (>M4.0, immediate shut-in). In practice, RRC has "
            "ordered volume reductions and permit modifications in parts of the "
            "Permian Basin (particularly the Delaware Basin near Pecos/Reeves "
            "counties). Operators must now include seismicity analysis in H-1 "
            "permit applications for wells within seismicity review areas. "
            "Historical seismic data, nearby disposal well volumes, and formation "
            "pressure data are required. This regulation directly impacts water "
            "management: reduced disposal capacity means operators must find "
            "alternative disposal, increase recycling, or reduce production."
        ),
        key_provisions=[
            "Seismicity review areas designated by RRC",
            "Traffic light protocol: Green/Yellow/Orange/Red",
            "TexNet provides real-time seismic monitoring",
            "Volume curtailment ordered for wells near seismic events",
            "H-1 applications in review areas require seismicity analysis",
            "Operators may be required to install seismic monitors",
            "Disposal well shut-in for M4.0+ events within radius",
            "Historical seismicity review required for new permits",
        ],
        exceptions=[
            "Enhanced recovery (EOR) wells may have different thresholds",
            "Wells outside seismicity review areas not subject to protocol",
        ],
        related_doctrines=["TWD-020", "TWD-021", "TWD-022"],
        risk_if_violated=RiskLevel.CRITICAL,
        permian_basin_notes=(
            "The Delaware Basin (Reeves, Pecos, Ward, Loving counties) has "
            "experienced significant induced seismicity from SWD operations. "
            "RRC has ordered volume reductions for multiple SWDs. Operators in "
            "this area should: (1) monitor TexNet data daily; (2) maintain "
            "relationships with midstream disposal providers to ensure capacity; "
            "(3) invest in recycling to reduce disposal dependence; (4) budget "
            "for potential curtailment costs."
        ),
        last_updated="2024-06-01",
        tags=["seismicity", "induced_earthquakes", "traffic_light", "texnet",
              "volume_curtailment", "disposal_well", "delaware_basin"],
    ),

    # ---- WATER TRANSPORT AGREEMENTS ----
    TexasWaterDoctrine(
        doctrine_id="TWD-050",
        title="Water Purchase and Sale Agreements for Oil and Gas Operations",
        category=DoctrineCategory.WATER_TRANSPORT_MIDSTREAM,
        authority_level=AuthorityLevel.INDUSTRY_STANDARD,
        jurisdiction=JurisdictionScope.STATE_TEXAS,
        citation="Industry Practice; TWC \u00a7\u00a7 11.085, 36.122; AAPL Form 610-2015",
        summary=(
            "Water purchase agreements for oil and gas operations involve "
            "sourcing fresh, brackish, or recycled water from landowners, "
            "municipalities, river authorities, or produced water midstream "
            "companies. Key terms include volume commitments, quality "
            "specifications, delivery points, pricing, and term."
        ),
        detailed_analysis=(
            "Water sourcing for hydraulic fracturing requires careful contract "
            "structuring. Key agreement types: (1) Landowner water lease: operator "
            "pays surface owner for right to drill and pump a water well on the "
            "surface estate. Must address GCD permitting, metering, restoration, "
            "and potential impact on other water users. (2) Municipal/river "
            "authority supply: bulk purchase from a water utility with capacity. "
            "Typically firm volume commitments with take-or-pay provisions. "
            "(3) Produced water recycling agreement: operator contracts with "
            "midstream company for recycled produced water delivery. Quality "
            "specs critical: TDS, TSS, bacteria, scale-forming minerals. "
            "(4) Brackish water agreement: similar to freshwater lease but from "
            "brackish aquifer zone. GCD permitting may differ. All agreements "
            "should address: force majeure, termination, insurance, indemnity, "
            "regulatory compliance responsibility, and environmental liability."
        ),
        key_provisions=[
            "Volume commitment: minimum daily/annual guaranteed takeaway",
            "Quality specifications: TDS, TSS, pH, bacteria, hardness",
            "Delivery point: wellsite, central facility, or pipeline tie-in",
            "Pricing: per-barrel, per-1000-gallons, or per-acre-foot",
            "Term: typically 1-5 years with renewal options",
            "Take-or-pay: minimum volume obligation regardless of use",
            "Force majeure: drought, regulatory curtailment, equipment failure",
            "GCD compliance: allocate permit responsibility",
            "Metering: specify calibration and dispute resolution",
            "Environmental liability: indemnity for spills during transport",
        ],
        exceptions=[
            "Emergency water supply during drilling may bypass formal contracts",
            "Spot market truck water typically sold without long-term contract",
        ],
        related_doctrines=["TWD-015", "TWD-017", "TWD-035", "TWD-040"],
        risk_if_violated=RiskLevel.MODERATE,
        permian_basin_notes=(
            "Permian Basin water costs: fresh groundwater $0.50-$2.00/bbl, "
            "recycled produced water $0.25-$1.50/bbl, trucked water $1.50-$3.00/bbl, "
            "piped supply $0.30-$1.00/bbl. Price depends on distance, volume, "
            "quality, and market conditions. Long-term contracts provide cost "
            "certainty but require volume commitment accuracy."
        ),
        last_updated="2024-06-01",
        tags=["water_purchase", "water_lease", "take_or_pay", "quality_specs",
              "frac_water", "midstream_contract"],
    ),

    # ---- SALTWATER DISPOSAL ----
    TexasWaterDoctrine(
        doctrine_id="TWD-055",
        title="Commercial Saltwater Disposal Well Requirements",
        category=DoctrineCategory.PRODUCED_WATER_DISPOSAL,
        authority_level=AuthorityLevel.STATE_REGULATION,
        jurisdiction=JurisdictionScope.STATE_TEXAS,
        citation="16 TAC \u00a7 3.9(3); RRC Commercial SWD Requirements",
        summary=(
            "Commercial saltwater disposal wells accepting produced water from "
            "third-party operators face enhanced regulatory requirements beyond "
            "standard SWD permits, including additional bonding, insurance, and "
            "compatibility testing."
        ),
        detailed_analysis=(
            "Commercial SWDs are a critical component of Permian Basin water "
            "management infrastructure. RRC imposes additional requirements on "
            "commercial (third-party) SWDs beyond those for operator-owned "
            "disposal wells. Key enhancements: higher financial assurance "
            "(plugging bonds), commercial general liability insurance, "
            "environmental site assessments, compatibility testing for commingled "
            "waste streams, more frequent MIT testing, and enhanced record-keeping "
            "for waste receipt and disposal volumes. Commercial SWD operators must "
            "maintain detailed manifests of all produced water received, including "
            "source operator, lease, well, volume, and basic water quality. RRC "
            "may impose individual permit conditions based on site-specific factors. "
            "Recent trends: RRC has increased scrutiny of commercial SWDs due to "
            "seismicity concerns, with some permits including maximum daily volume "
            "limits that constrain capacity."
        ),
        key_provisions=[
            "Enhanced bonding requirements for commercial SWDs",
            "Commercial general liability insurance required",
            "Compatibility testing for commingled waste streams",
            "Detailed manifest of all received produced water",
            "More frequent MIT testing may be required",
            "Environmental site assessment",
            "Maximum daily/monthly volume limits in permit",
            "24-hour emergency contact information on file",
            "Facility signage with permit number and emergency contact",
        ],
        exceptions=[
            "Operator-owned SWDs for own production have standard requirements",
            "Water recycling facilities are not classified as SWDs",
        ],
        related_doctrines=["TWD-020", "TWD-045"],
        risk_if_violated=RiskLevel.HIGH,
        permian_basin_notes=(
            "Commercial SWD capacity in the Permian Basin is a critical "
            "constraint. Key commercial disposal companies: WaterBridge, "
            "Solaris, NGL, Rattler (now Diamondback subsidiary), Hi-Crush. "
            "Disposal fees: $0.25-$1.00/bbl depending on location and volume. "
            "Operators should diversify disposal outlets to avoid single-point "
            "capacity risk."
        ),
        last_updated="2024-06-01",
        tags=["commercial_swd", "third_party_disposal", "manifest", "bonding",
              "disposal_fees", "capacity_constraint"],
    ),

    # ---- SPILL REPORTING ----
    TexasWaterDoctrine(
        doctrine_id="TWD-060",
        title="Spill Notification and Response - Water Contamination",
        category=DoctrineCategory.FRESHWATER_PROTECTION,
        authority_level=AuthorityLevel.STATE_REGULATION,
        jurisdiction=JurisdictionScope.STATE_TEXAS,
        citation="16 TAC \u00a7 3.20 (Rule 20); TWC \u00a7 26.039; TCEQ 30 TAC \u00a7 327",
        summary=(
            "Oil and gas operators must immediately report spills that may affect "
            "surface water or groundwater. RRC requires notification for any "
            "produced water spill exceeding 5 barrels or reaching a water body."
        ),
        detailed_analysis=(
            "Spill reporting has dual jurisdiction: RRC for oilfield spills "
            "and TCEQ for impacts to water quality. Under RRC Statewide Rule 20, "
            "operators must report to RRC any spill of crude oil, produced water, "
            "or other oilfield waste that: (1) exceeds 5 barrels outside "
            "containment; (2) reaches or threatens surface water; or (3) "
            "potentially affects a USDW. Reports must be made within 24 hours "
            "to the RRC district office. Cleanup must begin immediately. If a "
            "spill reaches navigable waters, federal reporting under the Clean "
            "Water Act also applies (National Response Center). TCEQ requires "
            "notification under TWC \u00a7 26.039 for any discharge that may affect "
            "water quality. Produced water spills are particularly damaging due "
            "to high salinity (kills vegetation, contaminates soil and "
            "groundwater). Operators must maintain spill prevention plans "
            "(equivalent to SPCC plans for oil)."
        ),
        key_provisions=[
            "Report to RRC within 24 hours for spills > 5 bbls outside containment",
            "Report to TCEQ for any discharge affecting water quality",
            "National Response Center if spill reaches navigable waters",
            "Immediate cleanup required",
            "Spill prevention plan must be maintained on-site",
            "Produced water: high priority due to salt contamination",
            "Soil remediation to background TDS levels required",
            "Groundwater monitoring may be required after spills near wells",
            "Penalties: $10,000+ per day for unreported/unclean spills",
        ],
        exceptions=[
            "De minimis spills fully contained within berms/dikes",
            "Spills < 5 bbls not reaching water: documentation only",
        ],
        related_doctrines=["TWD-025", "TWD-020"],
        risk_if_violated=RiskLevel.CRITICAL,
        permian_basin_notes=(
            "Permian Basin terrain is flat and porous: produced water spills "
            "can migrate rapidly to shallow groundwater. Playa lakes are "
            "particularly sensitive receptors. Operators should maintain "
            "double containment around tank batteries and ensure berms are "
            "intact after rain events."
        ),
        last_updated="2024-01-15",
        tags=["spill_notification", "rule_20", "produced_water_spill",
              "cleanup", "containment", "water_contamination"],
    ),
]


# ---------------------------------------------------------------------------
# GCD Rules
# ---------------------------------------------------------------------------

GROUNDWATER_RULES: list[GroundwaterRule] = [
    GroundwaterRule(
        rule_id="GCD-001",
        district_name="Midland County Groundwater Conservation District",
        county="Midland",
        rule_number="Rule 5",
        title="Well Permitting Requirements",
        description=(
            "All non-exempt wells within Midland County GWCD must obtain a "
            "production permit before drilling. Exempt wells include domestic "
            "and livestock wells producing less than 25 GPM."
        ),
        permit_requirements=[
            "Application form with well location (lat/long)",
            "Proposed production rate (GPM) and annual volume (AF)",
            "Well construction details (depth, casing, screen)",
            "Intended use (domestic, irrigation, industrial, oilfield)",
            "Hydrogeologic information for the target aquifer",
            "Adjacent well survey within 1/2 mile radius",
            "Application fee: $100 (non-commercial), $500 (commercial/industrial)",
        ],
        spacing_rules={
            "minimum_distance_from_property_line_ft": 300,
            "minimum_distance_from_existing_well_ft": 300,
            "minimum_distance_from_septic_ft": 150,
            "variance_process": "Board approval required",
        },
        production_limits={
            "maximum_per_permit_af_per_year": "Based on acreage and aquifer MAG",
            "allocation_factor_af_per_acre": 1.5,
            "historic_use_permit_available": True,
            "temporary_permit_max_days": 180,
        },
        reporting_requirements=[
            "Annual production report due January 31",
            "Meter readings required for all permitted wells",
            "Well completion report within 60 days of drilling",
            "Water quality analysis at permit and every 5 years",
        ],
        enforcement_actions=[
            "Written notice of violation",
            "Administrative penalty up to $10,000 per day",
            "Permit revocation for chronic non-compliance",
            "Injunctive relief through district court",
            "Criminal referral for willful violations",
        ],
        exemptions=[
            "Domestic/livestock wells < 25 GPM",
            "Wells on tracts < 5 acres for domestic use only",
            "Emergency use wells (temporary, max 72 hours)",
        ],
        oilfield_provisions=(
            "Industrial/oilfield water wells require a commercial production "
            "permit. Operators must demonstrate that water will be used for a "
            "beneficial purpose (hydraulic fracturing, drilling). Export of water "
            "outside the district requires an additional transport permit. The "
            "district may impose additional conditions on high-volume industrial "
            "wells, including reduced permit terms and enhanced monitoring."
        ),
        last_amended="2023-09-15",
    ),
    GroundwaterRule(
        rule_id="GCD-002",
        district_name="Pecos Valley Water District",
        county="Reeves",
        rule_number="Rules 3 and 4",
        title="Production Permits and Conservation Measures",
        description=(
            "Pecos Valley Water District governs groundwater production in "
            "Reeves County, with particular attention to the Pecos Valley "
            "Alluvium aquifer which faces critical depletion from agricultural "
            "and oilfield demand."
        ),
        permit_requirements=[
            "Application with proposed well location and construction plan",
            "Water conservation plan for withdrawals > 100 AF/year",
            "Aquifer impact assessment for large-volume permits (> 500 AF/year)",
            "Adjacent well owner notification (1/4 mile radius)",
            "Application fee: $75 (standard), $250 (large volume)",
        ],
        spacing_rules={
            "minimum_distance_from_property_line_ft": 250,
            "minimum_distance_from_existing_well_ft": 250,
            "minimum_distance_from_public_supply_well_ft": 500,
            "variance_process": "Board hearing required",
        },
        production_limits={
            "maximum_per_permit_af_per_year": "Based on aquifer availability",
            "allocation_factor_af_per_acre": 1.0,
            "oilfield_allocation_factor_af_per_acre": 0.75,
            "historic_use_permit_available": True,
            "temporary_permit_max_days": 120,
        },
        reporting_requirements=[
            "Monthly production reports for large-volume permits",
            "Annual production report for standard permits",
            "Meter calibration certification annually",
            "Groundwater level measurements quarterly (large volume wells)",
        ],
        enforcement_actions=[
            "Written warning with 30-day cure period",
            "Administrative penalty up to $10,000 per day",
            "Production curtailment order",
            "Permit suspension or revocation",
        ],
        exemptions=[
            "Domestic/livestock wells < 17.5 GPM",
            "Wells on tracts < 10 acres for domestic only",
        ],
        oilfield_provisions=(
            "The Pecos Valley Water District has seen a dramatic increase in "
            "oilfield water demand due to Delaware Basin development. The district "
            "allocates a lower AF/acre factor for oilfield use (0.75) compared "
            "to agricultural use (1.0) to preserve long-term aquifer viability. "
            "Operators must submit a water conservation plan demonstrating "
            "recycling and efficiency measures. The district actively encourages "
            "brackish water use and produced water recycling as alternatives to "
            "fresh groundwater."
        ),
        last_amended="2024-03-01",
    ),
]


# ---------------------------------------------------------------------------
# Surface Water Rules
# ---------------------------------------------------------------------------

SURFACE_WATER_RULES: list[SurfaceWaterRule] = [
    SurfaceWaterRule(
        rule_id="SWR-001",
        title="TCEQ Water Rights Permit Application Process",
        citation="30 TAC Chapter 295; TWC \u00a7\u00a7 11.121-11.143",
        tceq_chapter=295,
        description=(
            "Applications for new surface water appropriation permits are filed "
            "with TCEQ. The process includes technical review, public notice, "
            "contested case hearing (if protested), and commission action. "
            "Permits specify purpose, place of use, diversion rate, annual "
            "volume, and priority date."
        ),
        permit_types=[
            "Regular Permit (permanent appropriation)",
            "Temporary Permit (up to 3 years, specific purpose)",
            "Term Permit (limited duration with renewal option)",
            "Emergency Authorization (drought/emergency, expedited)",
            "Seasonal Permit (specific months of diversion)",
            "Bed and Banks Authorization (transport through watercourse)",
        ],
        priority_system="First in time, first in right (priority date = application filing date)",
        beneficial_uses=[
            "Municipal", "Industrial", "Irrigation", "Mining",
            "Hydroelectric", "Navigation", "Recreation", "Livestock",
            "Domestic", "Environmental (instream flows)",
        ],
        exemptions=[
            "Domestic and livestock use (up to 200 AF/year without permit)",
            "Wildlife management (limited exemption)",
            "Diffused surface water not in defined channel",
        ],
        cancellation_provisions=(
            "Permits may be cancelled for 10 consecutive years of non-use. "
            "Partial cancellation possible for sustained under-use. TCEQ "
            "initiates cancellation proceedings with notice and hearing."
        ),
        interstate_compact_notes=(
            "Pecos River Compact (Texas-New Mexico) allocates Pecos River "
            "flows between the states. Texas surface water rights on the "
            "Pecos are constrained by compact obligations. Rio Grande "
            "Compact also applies to shared waters."
        ),
    ),
]


# ---------------------------------------------------------------------------
# Produced Water Regulations
# ---------------------------------------------------------------------------

PRODUCED_WATER_REGULATIONS: list[ProducedWaterRegulation] = [
    ProducedWaterRegulation(
        regulation_id="PWR-001",
        title="RRC Statewide Rule 8 - Water Protection",
        agency="Railroad Commission of Texas",
        citation="16 TAC \u00a7 3.8",
        description=(
            "Statewide Rule 8 requires operators to prevent pollution of surface "
            "and subsurface water from oil and gas operations. Covers pit "
            "construction, tank battery containment, produced water handling, "
            "and spill prevention."
        ),
        disposal_methods=[
            "Injection well disposal (H-1 permitted SWD)",
            "Recycling for reuse in operations",
            "Evaporation pit (limited; TCEQ pit standards apply)",
            "Treatment and surface discharge (TCEQ TPDES permit required)",
        ],
        permit_requirements=[
            "All disposal wells require H-1 permit",
            "Pits must be lined (synthetic liner minimum 12 mil)",
            "Tank batteries must have containment (berm/dike)",
            "Spill prevention plan on file",
        ],
        volume_limits={
            "no_general_production_volume_limit": True,
            "disposal_well_specific_limit_in_permit": True,
            "pit_volume_subject_to_tceq_standards": True,
        },
        quality_standards={
            "no_general_produced_water_quality_standard": True,
            "disposal_zone_compatibility_required": True,
            "surface_discharge_requires_tpdes_limits": True,
        },
        reporting_frequency="Annual Form H-10 (disposal well annual report)",
        violations_and_penalties=[
            "Pollution of surface water: $10,000/day plus remediation",
            "Pollution of groundwater: $10,000/day plus remediation",
            "Failure to maintain containment: $5,000/day",
            "Failure to report spill: $10,000 per incident",
            "Chronic non-compliance: permit revocation",
        ],
        recycling_provisions=(
            "Produced water recycled for oilfield use is not considered disposal. "
            "No H-1 permit required for recycling. Storage and handling must still "
            "comply with Rule 8. Operators encouraged to maximize recycling to "
            "reduce disposal volumes and seismicity risk."
        ),
    ),
]


# ---------------------------------------------------------------------------
# Injection Well Standards
# ---------------------------------------------------------------------------

INJECTION_WELL_STANDARDS: list[InjectionWellStandard] = [
    InjectionWellStandard(
        standard_id="IWS-001",
        title="Class II-D Disposal Well Construction and Operation",
        agency="Railroad Commission of Texas",
        citation="16 TAC \u00a7 3.9; 40 CFR \u00a7\u00a7 144-148",
        well_class="Class II-D (Disposal)",
        description=(
            "Class II-D wells are used to dispose of produced water and other "
            "oilfield waste by injection into formations not productive of oil "
            "or gas. Comprehensive construction, operation, monitoring, and "
            "closure requirements apply."
        ),
        construction_requirements=[
            "Surface casing set through all freshwater zones per GPD letter",
            "Surface casing cemented to surface (returns required)",
            "Long string casing set through injection zone",
            "Cement calculated to isolate injection zone from USDWs",
            "Tubing and packer set above injection zone (annular monitoring)",
            "Corrosion-resistant materials for produced water service",
            "Wellhead rated for maximum anticipated surface pressure",
        ],
        operational_limits={
            "max_surface_injection_pressure_formula": "0.5 PSI per foot of true vertical depth to top of injection zone (default)",
            "max_daily_volume": "As specified in permit (typically 5,000-30,000 bbl/day)",
            "annular_pressure_monitoring": "Continuous; alarm at 200 PSI increase",
            "injection_pressure_recording": "Continuous chart or electronic recording",
        },
        monitoring_requirements=[
            "Continuous injection pressure and rate recording",
            "Continuous annular pressure monitoring",
            "Monthly volume reporting to RRC (Form H-10)",
            "Annual well performance assessment",
            "Groundwater monitoring wells if required by permit",
        ],
        mechanical_integrity_test={
            "initial_test": "Before first injection",
            "periodic_test": "Every 5 years minimum",
            "test_method": "Standard annular pressure test (SAPT)",
            "test_pressure_psi": 300,
            "test_duration_minutes": 30,
            "pass_criteria": "Less than 5% pressure decline",
            "failure_consequence": "Immediate shut-in until repaired and retested",
        },
        area_of_review={
            "radius_miles": 0.25,
            "review_items": [
                "All wells within AOR (active, plugged, abandoned)",
                "Penetrations through confining zone",
                "Improperly plugged wells identified for remediation",
                "Fault/fracture analysis if in seismicity review area",
            ],
        },
        plugging_requirements=[
            "Notify RRC 30 days before plugging",
            "Place cement plugs across injection zone",
            "Place cement plug across USDW base",
            "Place surface cement plug",
            "Submit plugging report (Form W-3A) within 30 days",
        ],
        financial_assurance={
            "individual_well_bond": 25000,
            "blanket_bond_1_to_10_wells": 50000,
            "blanket_bond_11_to_25_wells": 75000,
            "blanket_bond_26_to_100_wells": 100000,
            "blanket_bond_over_100_wells": 250000,
            "commercial_swd_additional_bond": True,
            "irrevocable_letter_of_credit_accepted": True,
        },
        seismicity_provisions=(
            "Wells in RRC-designated seismicity review areas must include "
            "seismicity analysis in the H-1 application. This includes: "
            "historical seismic data within 10 miles, proximity to mapped "
            "faults, cumulative injection volume in the area, and formation "
            "pressure data. RRC may impose permit conditions including maximum "
            "daily volume, pressure limits, and seismic monitoring requirements. "
            "The traffic light protocol applies: M2.0+ events within 10 miles "
            "may trigger volume reduction or shut-in orders."
        ),
    ),
]


# ---------------------------------------------------------------------------
# Aquifer Protection Rules
# ---------------------------------------------------------------------------

AQUIFER_PROTECTION_RULES: list[AquiferProtectionRule] = [
    AquiferProtectionRule(
        rule_id="APR-001",
        aquifer_name="Ogallala",
        title="Ogallala Aquifer Protection - Permian Basin",
        authority="Multiple GCDs; TWDB",
        citation="TWC Chapter 36; individual GCD rules",
        description=(
            "The Ogallala Aquifer is the primary freshwater source across the "
            "southern High Plains and Permian Basin. Protection measures focus "
            "on preventing contamination from oil and gas operations and managing "
            "depletion from competing agricultural and industrial demands."
        ),
        protected_zones=[
            "Primary saturated zone (unconfined)",
            "Recharge areas (playa lakes, Ogallala outcrop)",
            "Transition zone to underlying Dockum/Cretaceous formations",
        ],
        prohibited_activities=[
            "Direct injection of oilfield waste into Ogallala formation",
            "Surface disposal of produced water on Ogallala recharge areas",
            "Unlined pits for produced water storage over Ogallala",
        ],
        permit_requirements=[
            "GCD well permit for all non-exempt water wells",
            "Surface casing through Ogallala required for all oil/gas wells",
            "Cement returns to surface through freshwater zones",
            "Enhanced containment for facilities within 500 ft of Ogallala wells",
        ],
        monitoring_requirements=[
            "Water level measurements in GCD monitoring network",
            "Water quality sampling near oilfield operations",
            "Annual production reporting to GCDs",
            "Depletion tracking by TWDB",
        ],
        remediation_standards={
            "tds_cleanup_target_mg_l": 500,
            "chloride_cleanup_target_mg_l": 250,
            "benzene_cleanup_target_mg_l": 0.005,
            "approach": "Risk-based corrective action (RBCA)",
        },
        permian_basin_applicability=(
            "The Ogallala underlies much of the northern Permian Basin (Midland, "
            "Martin, Ector, Andrews, Gaines counties). Saturated thickness has "
            "declined 30-50% in some areas since 1950 due to irrigation pumping. "
            "Oil and gas demand for frac water adds to depletion pressure. "
            "Operators should consider brackish or recycled alternatives where "
            "feasible to reduce Ogallala dependence."
        ),
    ),
    AquiferProtectionRule(
        rule_id="APR-002",
        aquifer_name="Pecos Valley Alluvium",
        title="Pecos Valley Aquifer Protection - Trans-Pecos Region",
        authority="Pecos Valley Water District; TCEQ; RRC",
        citation="TWC Chapter 36; 30 TAC Chapter 213 (analogous protections)",
        description=(
            "The Pecos Valley Alluvium aquifer is a critical but stressed water "
            "source in the Trans-Pecos region (Reeves, Ward, Pecos counties). "
            "Heavy oilfield demand from Delaware Basin development has accelerated "
            "depletion and raised contamination concerns."
        ),
        protected_zones=[
            "Primary alluvial aquifer",
            "Pecos River baseflow contribution zone",
            "Spring-fed ecosystems (Balmorhea, San Solomon)",
            "Irrigation districts dependent on groundwater",
        ],
        prohibited_activities=[
            "Injection into Pecos Valley Alluvium",
            "Surface disposal of produced water in recharge areas",
            "Unpermitted water well drilling",
        ],
        permit_requirements=[
            "Pecos Valley Water District production permit",
            "Enhanced GCD permit for oilfield supply wells",
            "Water conservation plan for large-volume users",
            "Export permit for out-of-district transport",
        ],
        monitoring_requirements=[
            "Monthly production reporting for large-volume wells",
            "Quarterly water level measurements",
            "Annual water quality analysis",
            "Aquifer depletion tracking by TWDB",
        ],
        remediation_standards={
            "tds_cleanup_target_mg_l": "Background levels (varies 500-5000)",
            "chloride_cleanup_target_mg_l": "Background",
            "approach": "Site-specific remediation plan approved by TCEQ or RRC",
        },
        permian_basin_applicability=(
            "The Pecos Valley aquifer is ground zero for the water-energy nexus "
            "in the Delaware Basin. Rapid horizontal well development has created "
            "massive frac water demand competing with agricultural and municipal "
            "users. The aquifer has experienced significant drawdown in areas of "
            "concentrated oilfield pumping. Operators should invest in recycling "
            "infrastructure and explore Rustler/Dockum brackish alternatives."
        ),
    ),
]


# ---------------------------------------------------------------------------
# Doctrine cache
# ---------------------------------------------------------------------------

class WaterDoctrineCache:
    """Indexed cache for fast doctrine lookup and analysis."""

    def __init__(self) -> None:
        self._doctrines: dict[str, TexasWaterDoctrine] = {}
        self._gcd_rules: dict[str, GroundwaterRule] = {}
        self._surface_rules: dict[str, SurfaceWaterRule] = {}
        self._pw_regulations: dict[str, ProducedWaterRegulation] = {}
        self._iw_standards: dict[str, InjectionWellStandard] = {}
        self._aquifer_rules: dict[str, AquiferProtectionRule] = {}
        self._category_index: dict[str, list[str]] = {}
        self._tag_index: dict[str, list[str]] = {}
        self._loaded = False
        logger.info("WaterDoctrineCache initialized")

    def load_all(self) -> None:
        """Load all doctrine blocks into indexed cache."""
        for doctrine in TEXAS_WATER_DOCTRINES:
            self._doctrines[doctrine.doctrine_id] = doctrine
            cat = doctrine.category.value
            self._category_index.setdefault(cat, []).append(doctrine.doctrine_id)
            for tag in doctrine.tags:
                self._tag_index.setdefault(tag, []).append(doctrine.doctrine_id)

        for rule in GROUNDWATER_RULES:
            self._gcd_rules[rule.rule_id] = rule

        for rule in SURFACE_WATER_RULES:
            self._surface_rules[rule.rule_id] = rule

        for reg in PRODUCED_WATER_REGULATIONS:
            self._pw_regulations[reg.regulation_id] = reg

        for std in INJECTION_WELL_STANDARDS:
            self._iw_standards[std.standard_id] = std

        for rule in AQUIFER_PROTECTION_RULES:
            self._aquifer_rules[rule.rule_id] = rule

        self._loaded = True
        logger.info(
            "Doctrine cache loaded: {} doctrines, {} GCD rules, {} surface rules, "
            "{} PW regulations, {} IW standards, {} aquifer rules, {} tags",
            len(self._doctrines), len(self._gcd_rules), len(self._surface_rules),
            len(self._pw_regulations), len(self._iw_standards),
            len(self._aquifer_rules), len(self._tag_index),
        )

    def get_doctrine(self, doctrine_id: str) -> Optional[TexasWaterDoctrine]:
        """Retrieve a specific doctrine by ID."""
        if not self._loaded:
            self.load_all()
        return self._doctrines.get(doctrine_id)

    def get_by_category(self, category: DoctrineCategory) -> list[TexasWaterDoctrine]:
        """Get all doctrines in a category."""
        if not self._loaded:
            self.load_all()
        ids = self._category_index.get(category.value, [])
        return [self._doctrines[did] for did in ids if did in self._doctrines]

    def get_by_tag(self, tag: str) -> list[TexasWaterDoctrine]:
        """Get all doctrines matching a tag."""
        if not self._loaded:
            self.load_all()
        ids = self._tag_index.get(tag, [])
        return [self._doctrines[did] for did in ids if did in self._doctrines]

    def search_doctrines(self, query: str) -> list[TexasWaterDoctrine]:
        """Full-text search across all doctrine fields."""
        if not self._loaded:
            self.load_all()
        query_lower = query.lower()
        results: list[TexasWaterDoctrine] = []
        for doctrine in self._doctrines.values():
            searchable = " ".join([
                doctrine.title,
                doctrine.summary,
                doctrine.detailed_analysis,
                doctrine.citation,
                doctrine.permian_basin_notes,
                " ".join(doctrine.key_provisions),
                " ".join(doctrine.tags),
            ]).lower()
            if query_lower in searchable:
                results.append(doctrine)
        logger.debug("Doctrine search '{}' returned {} results", query, len(results))
        return results

    def get_gcd_rule(self, rule_id: str) -> Optional[GroundwaterRule]:
        """Get a specific GCD rule."""
        if not self._loaded:
            self.load_all()
        return self._gcd_rules.get(rule_id)

    def get_gcd_rules_by_county(self, county: str) -> list[GroundwaterRule]:
        """Get all GCD rules for a specific county."""
        if not self._loaded:
            self.load_all()
        return [r for r in self._gcd_rules.values() if r.county.lower() == county.lower()]

    def get_injection_well_standard(self, standard_id: str) -> Optional[InjectionWellStandard]:
        """Get a specific injection well standard."""
        if not self._loaded:
            self.load_all()
        return self._iw_standards.get(standard_id)

    def get_aquifer_protection(self, aquifer_name: str) -> list[AquiferProtectionRule]:
        """Get protection rules for a specific aquifer."""
        if not self._loaded:
            self.load_all()
        return [
            r for r in self._aquifer_rules.values()
            if aquifer_name.lower() in r.aquifer_name.lower()
        ]

    def get_risk_doctrines(self, min_risk: RiskLevel) -> list[TexasWaterDoctrine]:
        """Get all doctrines at or above a minimum risk level."""
        if not self._loaded:
            self.load_all()
        risk_order = {
            RiskLevel.LOW: 0,
            RiskLevel.MODERATE: 1,
            RiskLevel.HIGH: 2,
            RiskLevel.CRITICAL: 3,
        }
        min_order = risk_order.get(min_risk, 0)
        return [
            d for d in self._doctrines.values()
            if risk_order.get(d.risk_if_violated, 0) >= min_order
        ]

    def get_related_chain(self, doctrine_id: str, depth: int = 2) -> list[TexasWaterDoctrine]:
        """Traverse related doctrine links up to a given depth."""
        if not self._loaded:
            self.load_all()
        visited: set[str] = set()
        chain: list[TexasWaterDoctrine] = []
        queue = [doctrine_id]
        current_depth = 0
        while queue and current_depth < depth:
            next_queue: list[str] = []
            for did in queue:
                if did in visited:
                    continue
                visited.add(did)
                doctrine = self._doctrines.get(did)
                if doctrine:
                    chain.append(doctrine)
                    next_queue.extend(
                        r for r in doctrine.related_doctrines if r not in visited
                    )
            queue = next_queue
            current_depth += 1
        logger.debug(
            "Related chain for {} (depth={}): {} doctrines",
            doctrine_id, depth, len(chain),
        )
        return chain

    def compute_cache_hash(self) -> str:
        """Compute SHA-256 hash of entire doctrine cache for integrity verification."""
        if not self._loaded:
            self.load_all()
        all_hashes = sorted([d.compute_hash() for d in self._doctrines.values()])
        combined = "|".join(all_hashes)
        return hashlib.sha256(combined.encode()).hexdigest()

    def get_statistics(self) -> dict[str, Any]:
        """Return summary statistics of the doctrine cache."""
        if not self._loaded:
            self.load_all()
        return {
            "total_doctrines": len(self._doctrines),
            "total_gcd_rules": len(self._gcd_rules),
            "total_surface_rules": len(self._surface_rules),
            "total_pw_regulations": len(self._pw_regulations),
            "total_iw_standards": len(self._iw_standards),
            "total_aquifer_rules": len(self._aquifer_rules),
            "categories": {k: len(v) for k, v in self._category_index.items()},
            "total_tags": len(self._tag_index),
            "unique_citations": len({d.citation for d in self._doctrines.values()}),
            "cache_hash": self.compute_cache_hash(),
        }

    def export_json(self, output_path: Path) -> int:
        """Export all doctrines to JSON file. Returns count exported."""
        if not self._loaded:
            self.load_all()
        export_data = {
            "doctrines": [
                {
                    "id": d.doctrine_id,
                    "title": d.title,
                    "category": d.category.value,
                    "authority": d.authority_level.value,
                    "jurisdiction": d.jurisdiction.value,
                    "citation": d.citation,
                    "summary": d.summary,
                    "risk": d.risk_if_violated.value,
                    "tags": d.tags,
                    "hash": d.compute_hash(),
                }
                for d in self._doctrines.values()
            ],
            "cache_hash": self.compute_cache_hash(),
            "exported_at": datetime.now(timezone.utc).isoformat(),
        }
        output_path.write_text(json.dumps(export_data, indent=2))
        logger.info("Exported {} doctrines to {}", len(export_data["doctrines"]), output_path)
        return len(export_data["doctrines"])
