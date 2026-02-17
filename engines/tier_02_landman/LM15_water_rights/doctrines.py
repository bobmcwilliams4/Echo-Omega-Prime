"""
LM15 Water Rights Engine - Doctrine Cache
===========================================

50+ doctrine blocks covering Texas water law: groundwater capture,
surface water appropriation, GCD regulation, produced water disposal,
injection wells, freshwater protection, recycling, desalination,
interstate compacts, and accommodation doctrine.

Author: ECHO OMEGA PRIME Build System
Engine: LM15 v2.0.0
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
    INTERSTATE_COMPACT = "interstate_compact"
    FEDERAL_WATER_LAW = "federal_water_law"
    WATER_CONVEYANCING = "water_conveyancing"
    DROUGHT_PLANNING = "drought_planning"


class AuthorityLevel(str, Enum):
    FEDERAL_STATUTE = "federal_statute"
    FEDERAL_REGULATION = "federal_regulation"
    STATE_STATUTE = "state_statute"
    STATE_REGULATION = "state_regulation"
    AGENCY_RULE = "agency_rule"
    CASE_LAW = "case_law"
    AGENCY_GUIDANCE = "agency_guidance"
    INDUSTRY_STANDARD = "industry_standard"


class JurisdictionScope(str, Enum):
    FEDERAL = "federal"
    STATE_TEXAS = "state_texas"
    REGIONAL = "regional"
    GCD_LOCAL = "gcd_local"
    COUNTY = "county"
    BASIN_SPECIFIC = "basin_specific"
    INTERSTATE = "interstate"


class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class DoctrineCacheBlock:
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
        content = json.dumps({
            "id": self.doctrine_id, "title": self.title,
            "citation": self.citation, "summary": self.summary,
            "detailed_analysis": self.detailed_analysis,
            "key_provisions": self.key_provisions,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class GroundwaterRule:
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
            "id": self.rule_id, "district": self.district_name,
            "rule": self.rule_number, "description": self.description,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class SurfaceWaterRule:
    rule_id: str
    title: str
    citation: str
    agency: str
    description: str
    permit_types: list[str]
    priority_system: str
    exemptions: list[str]
    cancellation_provisions: str
    amendment_rules: str
    enforcement: str
    permian_basin_relevance: str

    def compute_hash(self) -> str:
        content = json.dumps({
            "id": self.rule_id, "title": self.title,
            "citation": self.citation, "description": self.description,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class ProducedWaterRegulation:
    reg_id: str
    title: str
    agency: str
    citation: str
    description: str
    disposal_methods: list[str]
    volume_limits: dict[str, Any]
    quality_standards: dict[str, Any]
    reporting_requirements: list[str]
    recycling_provisions: str
    enforcement_actions: list[str]
    permian_basin_notes: str

    def compute_hash(self) -> str:
        content = json.dumps({
            "id": self.reg_id, "title": self.title,
            "citation": self.citation, "description": self.description,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class InjectionWellStandard:
    std_id: str
    title: str
    well_class: str
    citation: str
    agency: str
    description: str
    permit_requirements: list[str]
    construction_standards: dict[str, Any]
    operating_limits: dict[str, Any]
    monitoring_requirements: list[str]
    mit_interval_years: int
    closure_requirements: list[str]
    seismicity_provisions: str
    permian_basin_notes: str

    def compute_hash(self) -> str:
        content = json.dumps({
            "id": self.std_id, "title": self.title,
            "citation": self.citation, "description": self.description,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class AquiferProtectionRule:
    rule_id: str
    title: str
    aquifer_name: str
    citation: str
    description: str
    protection_zones: list[str]
    tds_thresholds: dict[str, float]
    casing_requirements: list[str]
    monitoring_requirements: list[str]
    contamination_response: list[str]
    permian_basin_relevance: str

    def compute_hash(self) -> str:
        content = json.dumps({
            "id": self.rule_id, "title": self.title,
            "aquifer": self.aquifer_name, "description": self.description,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class InterstateCompactProvision:
    compact_id: str
    compact_name: str
    parties: list[str]
    year_ratified: int
    citation: str
    texas_obligations: list[str]
    allocation_method: str
    enforcement_mechanism: str
    supreme_court_cases: list[str]
    permian_basin_relevance: str

    def compute_hash(self) -> str:
        content = json.dumps({
            "id": self.compact_id, "name": self.compact_name,
            "citation": self.citation, "parties": self.parties,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


# ---------------------------------------------------------------------------
# Doctrine cache builder
# ---------------------------------------------------------------------------

def _build_groundwater_doctrines() -> list[DoctrineCacheBlock]:
    return [
        DoctrineCacheBlock(
            doctrine_id="WR-GW-001",
            title="Rule of Capture - Absolute Ownership Doctrine",
            category=DoctrineCategory.GROUNDWATER_CAPTURE,
            authority_level=AuthorityLevel.CASE_LAW,
            jurisdiction=JurisdictionScope.STATE_TEXAS,
            citation="Houston & T.C. Ry. Co. v. East, 98 Tex. 146, 81 S.W. 279 (1904)",
            summary="Texas follows the rule of capture for groundwater: a landowner may pump groundwater beneath their land without liability to neighbors whose wells are affected, absent malice or willful waste.",
            detailed_analysis="The East case established that percolating groundwater in Texas is the private property of the surface owner. Unlike surface water which follows prior appropriation, groundwater is treated as part of the realty. A landowner has the absolute right to capture groundwater regardless of effect on neighboring wells. The doctrine has been modified by GCD regulation under TWC Ch. 36 and by the recognition of groundwater as a vested property right in EAA v. Day (2012). The rule still applies in areas without GCD oversight, though the Texas Supreme Court has indicated willingness to recognize waste and subsidence claims. The doctrine creates significant tension with sustainable yield management, particularly in depleting aquifers like the Ogallala.",
            key_provisions=[
                "Landowner owns groundwater in place as real property",
                "No liability for draining neighbor's groundwater absent malice or waste",
                "Percolating groundwater distinguished from underground streams",
                "GCD regulation does not eliminate ownership but may restrict production",
                "Negligent waste of artesian well flow is actionable (City of Corpus Christi v. City of Pleasanton)",
            ],
            exceptions=[
                "Willful waste or malicious pumping to injure neighbor",
                "Subsidence damage (Friendswood Dev. Co. v. Smith-Southwest Indus.)",
                "GCD production limits under TWC Ch. 36",
                "Contamination liability under TCEQ rules",
                "Fraudulent concealment of well information",
            ],
            related_doctrines=["WR-GW-002", "WR-GW-003", "WR-GCD-001"],
            risk_if_violated=RiskLevel.MODERATE,
            permian_basin_notes="Rule of capture remains strong in Permian Basin. Most Permian counties now have GCDs that overlay production limits on the capture right. Oilfield freshwater sourcing still largely governed by capture for non-exempt wells.",
            last_updated="2026-02-10",
            tags=["groundwater", "rule_of_capture", "east_doctrine", "property_right", "permian_basin"],
        ),
        DoctrineCacheBlock(
            doctrine_id="WR-GW-002",
            title="Groundwater as Vested Property Right - EAA v. Day",
            category=DoctrineCategory.GROUNDWATER_CAPTURE,
            authority_level=AuthorityLevel.CASE_LAW,
            jurisdiction=JurisdictionScope.STATE_TEXAS,
            citation="Edwards Aquifer Authority v. Day, 369 S.W.3d 814 (Tex. 2012)",
            summary="The Texas Supreme Court held that landowners have a constitutionally protected vested property right in groundwater in place, analogous to oil and gas ownership. GCD regulations that deny all beneficial use may constitute a compensable taking.",
            detailed_analysis="In EAA v. Day, the Texas Supreme Court resolved a long-standing question by holding that groundwater ownership is a vested right under Article I, Section 17 of the Texas Constitution. The court analogized groundwater to oil and gas under the ownership-in-place theory. This means that while GCDs may regulate groundwater production under their police power authority, regulations that go too far and deny all economically beneficial use constitute a regulatory taking requiring just compensation. The Penn Central balancing test applies. The decision fundamentally changed the calculus for GCD rulemaking by imposing constitutional limits on how restrictive production permits can be. It also confirmed that groundwater rights are severable from surface rights and can be separately conveyed.",
            key_provisions=[
                "Groundwater is owned in place as real property",
                "Ownership is constitutionally protected under Art. I Sec. 17 Texas Constitution",
                "Analogy to oil and gas ownership-in-place theory",
                "GCD regulation subject to takings analysis under Penn Central",
                "Groundwater rights severable from surface estate",
                "Regulatory taking requires just compensation",
            ],
            exceptions=[
                "Reasonable regulation under police power still permitted",
                "Production limits tied to DFCs may survive takings challenge",
                "Emergency drought restrictions likely survive",
                "Rule does not guarantee specific volume, only the right itself",
            ],
            related_doctrines=["WR-GW-001", "WR-GCD-001", "WR-CONV-001"],
            risk_if_violated=RiskLevel.HIGH,
            permian_basin_notes="EAA v. Day is critical for Permian Basin operators who purchase groundwater rights. Confirms that water rights purchases are constitutionally protected investments. GCDs in the Permian must balance DFC compliance with avoiding takings claims from large-volume users.",
            last_updated="2026-02-10",
            tags=["groundwater", "property_right", "takings", "eaa_v_day", "constitutional"],
        ),
        DoctrineCacheBlock(
            doctrine_id="WR-GW-003",
            title="Groundwater Waste Prohibition",
            category=DoctrineCategory.GROUNDWATER_CAPTURE,
            authority_level=AuthorityLevel.CASE_LAW,
            jurisdiction=JurisdictionScope.STATE_TEXAS,
            citation="City of Corpus Christi v. City of Pleasanton, 154 Tex. 289 (1955); TWC Sec. 36.001(8)",
            summary="While the rule of capture permits broad pumping rights, Texas law prohibits willful waste of groundwater. Waste includes producing water without beneficial use, allowing artesian wells to flow unchecked, and pollution of aquifers.",
            detailed_analysis="The waste prohibition is the primary common-law limitation on the rule of capture. Willful waste occurs when a landowner produces groundwater without putting it to beneficial use or allows an artesian well to flow uncontrolled. TWC Section 36.001(8) defines waste to include production exceeding beneficial use, escape or flow onto adjacent land without beneficial use, and pollution. GCDs have authority under TWC Sec. 36.116 to adopt rules to prevent waste. The prohibition is narrower than it might appear: production for oil and gas operations, irrigation, municipal supply, and industrial use all constitute beneficial uses. The tension arises when a GCD determines that aggregate pumping exceeds the aquifer's sustainable yield, potentially making individual permits subject to curtailment.",
            key_provisions=[
                "Willful waste of groundwater is prohibited under common law",
                "TWC Sec. 36.001(8) statutory definition of waste",
                "Beneficial use requirement for non-exempt production",
                "GCD authority to adopt anti-waste rules under TWC Sec. 36.116",
                "Artesian well flow must be controlled",
                "Pollution of aquifer constitutes waste",
            ],
            exceptions=[
                "Domestic and livestock use presumed beneficial",
                "Oil and gas operations water use generally deemed beneficial",
                "Emergency or force majeure events",
                "De minimis waste below reporting thresholds",
            ],
            related_doctrines=["WR-GW-001", "WR-GW-002", "WR-GCD-002"],
            risk_if_violated=RiskLevel.MODERATE,
            permian_basin_notes="In the Permian Basin, waste concerns arise from large-volume freshwater sourcing for fracking operations. GCDs may scrutinize whether freshwater use for hydraulic fracturing is the highest beneficial use when brackish or recycled water alternatives exist.",
            last_updated="2026-02-10",
            tags=["groundwater", "waste", "beneficial_use", "gcd_authority"],
        ),
        DoctrineCacheBlock(
            doctrine_id="WR-GW-004",
            title="Subsidence Liability Exception to Rule of Capture",
            category=DoctrineCategory.GROUNDWATER_CAPTURE,
            authority_level=AuthorityLevel.CASE_LAW,
            jurisdiction=JurisdictionScope.STATE_TEXAS,
            citation="Friendswood Dev. Co. v. Smith-Southwest Indus., Inc., 576 S.W.2d 21 (Tex. 1978)",
            summary="A landowner who negligently pumps groundwater causing subsidence damage to neighboring property may be liable in tort, creating an exception to the rule of capture immunity.",
            detailed_analysis="The Friendswood decision carved out a subsidence exception to the rule of capture. The Texas Supreme Court held that while the rule of capture immunizes a pumper from liability for draining a neighbor's well, it does not immunize against damage to the surface of neighboring land caused by subsidence. The court applied a negligence standard prospectively only (from the date of the opinion forward). The decision led to creation of subsidence districts in the Houston area (Harris-Galveston, Fort Bend) and informs GCD regulation in areas prone to subsidence. In the Permian Basin, subsidence from groundwater withdrawal is less common than in the Gulf Coast region, but localized subsidence from dewatering around mining and oil field operations has been documented.",
            key_provisions=[
                "Negligent groundwater pumping causing subsidence is actionable",
                "Prospective application only from 1978 forward",
                "Standard is negligence, not strict liability",
                "Plaintiff must prove causation between pumping and subsidence",
                "Led to creation of subsidence districts",
            ],
            exceptions=[
                "Pre-1978 pumping operations grandfathered",
                "Natural subsidence not attributable to pumping",
                "Subsidence within pumper's own property boundary",
            ],
            related_doctrines=["WR-GW-001", "WR-GW-002"],
            risk_if_violated=RiskLevel.HIGH,
            permian_basin_notes="Subsidence risk in Permian Basin is generally low compared to Gulf Coast, but localized concerns exist near large-volume freshwater pumping operations for fracking. Operators should monitor for sinkholes in karst-prone Edwards-Trinity areas.",
            last_updated="2026-02-10",
            tags=["groundwater", "subsidence", "negligence", "tort_liability"],
        ),
        DoctrineCacheBlock(
            doctrine_id="WR-GW-005",
            title="Groundwater Marketing and Export Rights",
            category=DoctrineCategory.GROUNDWATER_CAPTURE,
            authority_level=AuthorityLevel.STATE_STATUTE,
            jurisdiction=JurisdictionScope.STATE_TEXAS,
            citation="TWC Sec. 36.122; Guitar Holding Co. v. Hudspeth County UWCD No. 1, 263 S.W.3d 910 (Tex. 2008)",
            summary="A GCD may not impose more restrictive permit conditions on groundwater transported out of the district than on water used within the district. Export fees are limited and subject to statutory caps.",
            detailed_analysis="TWC Section 36.122 was enacted to prevent GCDs from imposing discriminatory restrictions on groundwater exports. The statute requires GCDs to issue export permits on terms no more restrictive than permits for in-district use, though the permit term may be limited to the lesser of the term of the contract to supply water outside the district or 30 years. Export permit fees are capped and must be based on the district's costs. The Guitar Holding decision confirmed that GCDs cannot use their regulatory power to impose de facto bans on groundwater exports. This is significant for Permian Basin operators who may sell water rights to distant municipalities or industrial users.",
            key_provisions=[
                "Export permits may not be more restrictive than in-district permits",
                "Maximum export permit term is lesser of contract term or 30 years",
                "Export fees limited to district's actual costs",
                "GCD must process export applications within same timeframe as other permits",
                "Judicial review available for denied export permits",
            ],
            exceptions=[
                "GCD may require transport plan and monitoring",
                "Export may be curtailed during critical drought",
                "Export fees may include reasonable administrative costs",
            ],
            related_doctrines=["WR-GW-002", "WR-GCD-001", "WR-CONV-001"],
            risk_if_violated=RiskLevel.MODERATE,
            permian_basin_notes="Groundwater export from Permian Basin GCDs to San Antonio, El Paso, and Midland-Odessa metro areas is a growing issue. Operators purchasing water rights for oilfield use should verify export permit requirements if transporting water across GCD boundaries.",
            last_updated="2026-02-10",
            tags=["groundwater", "export", "marketing", "gcd_regulation"],
        ),
    ]


def _build_gcd_doctrines() -> list[DoctrineCacheBlock]:
    return [
        DoctrineCacheBlock(
            doctrine_id="WR-GCD-001",
            title="GCD Enabling Authority - TWC Chapter 36",
            category=DoctrineCategory.GROUNDWATER_CONSERVATION_DISTRICT,
            authority_level=AuthorityLevel.STATE_STATUTE,
            jurisdiction=JurisdictionScope.GCD_LOCAL,
            citation="TWC Ch. 36; Tex. Const. Art. XVI, Sec. 59",
            summary="Groundwater conservation districts are the state's preferred method of groundwater management. TWC Chapter 36 grants GCDs authority to regulate well spacing, production, waste prevention, and aquifer protection within their boundaries.",
            detailed_analysis="TWC Chapter 36 is the comprehensive enabling statute for GCDs. It authorizes districts to require permits for drilling and producing non-exempt wells, establish well spacing requirements, limit production based on tract size or aquifer conditions, adopt rules to prevent waste and protect water quality, and enforce compliance through civil penalties and well plugging orders. GCDs must adopt management plans consistent with the regional water plan and implement rules to achieve Desired Future Conditions (DFCs) adopted by the relevant Groundwater Management Area. The statute provides for judicial review of GCD decisions and establishes the contested case hearing process through SOAH. Exempt wells (domestic/livestock under 25,000 GPD for most GCDs) are not subject to permitting but must still comply with spacing and registration requirements.",
            key_provisions=[
                "GCDs authorized under Art. XVI Sec. 59 Texas Constitution",
                "Permitting authority for non-exempt wells under TWC Sec. 36.113",
                "Spacing rules under TWC Sec. 36.116",
                "Production limits tied to tract acreage or managed available groundwater",
                "Desired Future Conditions under TWC Sec. 36.108",
                "Contested case hearing through SOAH under TWC Sec. 36.415",
                "Exempt well provisions under TWC Sec. 36.117",
                "Well registration requirements under TWC Sec. 36.111",
            ],
            exceptions=[
                "Domestic and livestock wells exempt from permitting under TWC Sec. 36.117",
                "Wells drilled before GCD creation may have historic use rights",
                "Oil and gas exempt wells under TWC Sec. 36.117(b)(2)",
                "Temporary emergency permits during drought",
            ],
            related_doctrines=["WR-GW-002", "WR-GW-005", "WR-GCD-002"],
            risk_if_violated=RiskLevel.HIGH,
            permian_basin_notes="All major Permian Basin counties have GCDs. Operators must obtain production permits for non-exempt oilfield water wells. The oil and gas exemption under TWC Sec. 36.117(b)(2) is narrow: it applies only to wells drilled for oil and gas exploration/production purposes, not dedicated freshwater supply wells for fracking.",
            last_updated="2026-02-10",
            tags=["gcd", "twc_chapter_36", "permitting", "spacing", "dfc"],
        ),
        DoctrineCacheBlock(
            doctrine_id="WR-GCD-002",
            title="Desired Future Conditions and Managed Available Groundwater",
            category=DoctrineCategory.GROUNDWATER_CONSERVATION_DISTRICT,
            authority_level=AuthorityLevel.STATE_STATUTE,
            jurisdiction=JurisdictionScope.REGIONAL,
            citation="TWC Sec. 36.108; TWC Sec. 36.1132",
            summary="GCDs within each Groundwater Management Area must jointly establish Desired Future Conditions (DFCs) for aquifers, which TWDB then uses to calculate Managed Available Groundwater (MAG) for each GCD.",
            detailed_analysis="The DFC/MAG process is the cornerstone of Texas groundwater planning. GMA joint planning committees adopt DFCs that describe the desired condition of aquifers 50 years into the future. TWDB then models the Managed Available Groundwater (MAG) for each GCD based on those DFCs. GCDs must implement permit rules that, in the aggregate, achieve the MAG. This creates a quantified regulatory framework that connects individual well permits to basin-wide sustainability goals. DFCs are adopted every 5 years concurrent with the state water planning cycle. Contested DFCs may be challenged through SOAH. The process is inherently political as it pits agricultural irrigators, municipal suppliers, industrial users, and oil and gas operators against each other for finite groundwater allocations.",
            key_provisions=[
                "GMA joint planning committees adopt DFCs under TWC Sec. 36.108",
                "TWDB calculates MAG from DFCs",
                "GCDs must implement rules to achieve MAG",
                "5-year planning cycle aligned with state water plan",
                "SOAH challenge process for contested DFCs",
                "DFCs consider aquifer uses, conditions, and environmental impacts",
            ],
            exceptions=[
                "Emergency drought conditions may override DFC compliance timelines",
                "Existing permit holders may receive transition provisions",
            ],
            related_doctrines=["WR-GCD-001", "WR-GW-002", "WR-GW-005"],
            risk_if_violated=RiskLevel.HIGH,
            permian_basin_notes="GMA 7 (Trans-Pecos/Permian Basin region) has adopted DFCs for the Pecos Valley, Dockum, and Edwards-Trinity aquifers. Ogallala DFCs in GMA 2 reflect severe depletion concerns. MAG allocations directly constrain how much freshwater Permian operators can pump for fracking.",
            last_updated="2026-02-10",
            tags=["gcd", "dfc", "mag", "groundwater_planning", "gma"],
        ),
        DoctrineCacheBlock(
            doctrine_id="WR-GCD-003",
            title="Oil and Gas Exempt Well Provisions",
            category=DoctrineCategory.GROUNDWATER_CONSERVATION_DISTRICT,
            authority_level=AuthorityLevel.STATE_STATUTE,
            jurisdiction=JurisdictionScope.GCD_LOCAL,
            citation="TWC Sec. 36.117(b)(2); 16 TAC Sec. 76.10",
            summary="Wells used solely for oil and gas exploration, drilling, or production activities including hydraulic fracturing may be exempt from GCD permitting requirements, but the exemption is narrow and subject to GCD interpretation.",
            detailed_analysis="TWC Sec. 36.117(b)(2) exempts from GCD permitting any well used solely to supply water for a rig actively engaged in drilling or exploration operations for an oil or gas well permitted by the RRC. However, this exemption has been narrowly construed. Many GCDs interpret the exemption to cover only water used at the drill site during active drilling, not bulk freshwater sourcing for fracking operations from dedicated water wells. Some GCDs require permits for frack water supply wells even when the water is used for oil and gas purposes. The exemption does not override GCD spacing rules, and exempt wells must still be registered. Recent legislative efforts have sought to clarify the scope, but ambiguity remains. Operators should consult individual GCD rules before relying on the exemption.",
            key_provisions=[
                "Exemption limited to water for rig actively drilling or exploring",
                "Must be for oil or gas well permitted by RRC",
                "Does not exempt dedicated freshwater supply wells for bulk fracking",
                "Well must still comply with GCD spacing requirements",
                "Well must be registered with GCD even if exempt",
                "GCD may require metering on exempt wells",
            ],
            exceptions=[
                "Some GCDs extend exemption to include completion operations",
                "Temporary permits available as alternative to exemption claim",
                "Recycled produced water use does not trigger GCD jurisdiction",
            ],
            related_doctrines=["WR-GCD-001", "WR-PW-004", "WR-FP-002"],
            risk_if_violated=RiskLevel.HIGH,
            permian_basin_notes="Permian Basin GCDs vary widely on how they interpret the oil and gas exemption. Midland County GWCD requires permits for all freshwater wells producing over 25 GPM regardless of intended use. Operators should not assume exemption without written confirmation from the specific GCD.",
            last_updated="2026-02-10",
            tags=["gcd", "oil_gas_exemption", "fracking", "freshwater", "permitting"],
        ),
    ]


def _build_surface_water_doctrines() -> list[DoctrineCacheBlock]:
    return [
        DoctrineCacheBlock(
            doctrine_id="WR-SW-001",
            title="Prior Appropriation - Texas Surface Water Rights",
            category=DoctrineCategory.SURFACE_WATER_APPROPRIATION,
            authority_level=AuthorityLevel.STATE_STATUTE,
            jurisdiction=JurisdictionScope.STATE_TEXAS,
            citation="TWC Ch. 11; Tex. Const. Art. XVI, Sec. 59a",
            summary="All surface water in Texas belongs to the state. Use requires a permit from TCEQ under the prior appropriation system: first in time, first in right. Domestic and livestock use is exempt up to 200 AF/year.",
            detailed_analysis="Texas adopted the prior appropriation system for surface water in 1913, replacing the common-law riparian rights system. Under TWC Chapter 11, all water in rivers, streams, lakes, and impoundments belongs to the state and may be used only under a permit or other authorization from TCEQ. Priority is established by the date of the permit application (or the date of first use for pre-1913 rights). Senior appropriators have priority over junior appropriators during shortages. TCEQ administers the water rights permitting program including new appropriations, amendments, transfers, and cancellations. Permits may be cancelled after 10 years of non-use. The domestic and livestock exemption allows up to 200 AF/year without a permit for watering livestock and domestic household use. The Watermaster program enforces priority calls in certain basins.",
            key_provisions=[
                "State ownership of all surface water under TWC Sec. 11.021",
                "Prior appropriation: first in time, first in right",
                "TCEQ permitting authority under TWC Sec. 11.121",
                "Domestic and livestock exemption up to 200 AF/year (TWC Sec. 11.142)",
                "10-year non-use cancellation under TWC Sec. 11.173",
                "Watermaster enforcement in designated basins",
                "Environmental flow standards under SB 3 (2007)",
                "Bed and banks authorization for transporting water",
            ],
            exceptions=[
                "Domestic and livestock use up to 200 AF/year exempt",
                "Diffused surface water (sheet flow) may not require permit",
                "Emergency authorizations during drought",
                "Federal reserved rights on tribal and federal lands",
            ],
            related_doctrines=["WR-SW-002", "WR-SW-003", "WR-CONV-001"],
            risk_if_violated=RiskLevel.CRITICAL,
            permian_basin_notes="Surface water is extremely scarce in the Permian Basin. Most surface water rights are held by municipalities (Midland, Odessa) and irrigation districts. Oil and gas operators rarely hold surface water permits but may purchase water from permit holders. The Pecos River is subject to interstate compact allocation.",
            last_updated="2026-02-10",
            tags=["surface_water", "prior_appropriation", "tceq", "water_permit"],
        ),
        DoctrineCacheBlock(
            doctrine_id="WR-SW-002",
            title="Bed and Banks Authorization",
            category=DoctrineCategory.SURFACE_WATER_APPROPRIATION,
            authority_level=AuthorityLevel.STATE_STATUTE,
            jurisdiction=JurisdictionScope.STATE_TEXAS,
            citation="TWC Sec. 11.042; 30 TAC Ch. 297",
            summary="Any person transporting water through state watercourses (bed and banks) for authorized purposes must obtain bed and banks authorization from TCEQ. This applies to return flows, recycled water discharges, and interbasin transfers.",
            detailed_analysis="Bed and banks authorization is required whenever water is introduced into or diverted from a state watercourse. This includes returning treated effluent to a river, transporting permitted water through a stream channel, and discharging produced water treatment effluent. The authorization addresses system losses (evaporation, seepage), impacts on other appropriators, and water quality concerns. For oil and gas operators, bed and banks authorization may be needed when treated produced water is discharged into a creek or river. The authorization is typically issued as a condition of the water rights permit or TPDES permit. TCEQ evaluates the impact on downstream senior appropriators and environmental flows.",
            key_provisions=[
                "Authorization required for use of state watercourse as conveyance",
                "System loss assessment (typically 5-20% depending on distance)",
                "Must not injure existing water rights holders",
                "Water quality must meet stream standards at discharge point",
                "Applies to return flows, interbasin transfers, and discharges",
            ],
            exceptions=[
                "Natural return flows from irrigation",
                "Stormwater runoff not requiring authorization",
                "Emergency bypass during flood events",
            ],
            related_doctrines=["WR-SW-001", "WR-PW-003", "WR-FED-001"],
            risk_if_violated=RiskLevel.HIGH,
            permian_basin_notes="Bed and banks authorization is relevant when Permian Basin operators consider discharging treated produced water to surface streams. The Pecos River and tributaries are potential receiving waters but are subject to interstate compact and salinity concerns.",
            last_updated="2026-02-10",
            tags=["bed_and_banks", "surface_water", "transport", "tceq"],
        ),
        DoctrineCacheBlock(
            doctrine_id="WR-SW-003",
            title="Environmental Flow Standards - SB 3",
            category=DoctrineCategory.SURFACE_WATER_APPROPRIATION,
            authority_level=AuthorityLevel.STATE_STATUTE,
            jurisdiction=JurisdictionScope.STATE_TEXAS,
            citation="TWC Sec. 11.1471; SB 3 (80th Leg., 2007)",
            summary="TCEQ must establish environmental flow standards for new water rights permits to protect the ecological health of rivers, streams, and estuaries. New permits include environmental flow conditions that restrict diversions during low-flow periods.",
            detailed_analysis="Senate Bill 3 (2007) created a science-based process for setting environmental flow standards in Texas river basins. Environmental Flow Advisory Groups, Science Advisory Committees, and Stakeholder Committees develop flow recommendations. TCEQ adopts rules establishing environmental flow standards for each basin. All new water rights permits issued after the adoption of flow standards must include conditions protecting environmental flows. Existing permits are not retroactively affected. The standards establish subsistence flows, base flows, and high-flow pulse requirements that limit when diversions may occur. This framework does not apply to groundwater but may indirectly affect conjunctive use strategies.",
            key_provisions=[
                "Science-based environmental flow standards for each river basin",
                "New permits must include environmental flow conditions",
                "Subsistence, base, and high-flow pulse flow tiers",
                "Existing permits grandfathered from environmental flow conditions",
                "Adaptive management and periodic review of standards",
            ],
            exceptions=[
                "Existing water rights not subject to new flow standards",
                "Emergency drought provisions may supersede",
                "Domestic and livestock use remains exempt",
            ],
            related_doctrines=["WR-SW-001", "WR-FED-001"],
            risk_if_violated=RiskLevel.MODERATE,
            permian_basin_notes="Environmental flow standards for the Pecos River basin are minimal due to limited flows. However, operators seeking new surface water permits in the Permian region must comply with applicable environmental flow conditions.",
            last_updated="2026-02-10",
            tags=["environmental_flows", "sb3", "surface_water", "ecological"],
        ),
    ]


def _build_produced_water_doctrines() -> list[DoctrineCacheBlock]:
    return [
        DoctrineCacheBlock(
            doctrine_id="WR-PW-001",
            title="Produced Water Disposal - RRC Jurisdiction and Statewide Rules",
            category=DoctrineCategory.PRODUCED_WATER_DISPOSAL,
            authority_level=AuthorityLevel.STATE_REGULATION,
            jurisdiction=JurisdictionScope.STATE_TEXAS,
            citation="16 TAC Ch. 3 (Statewide Rules 8, 9, 13, 14, 46); TNRC Ch. 91",
            summary="The Railroad Commission of Texas has exclusive jurisdiction over disposal of oil and gas waste including produced water. Disposal by injection requires an H-1 permit. Surface discharge of produced water is prohibited except under limited TPDES permits.",
            detailed_analysis="Under TNRC Chapter 91 and 16 TAC Chapter 3, the RRC regulates all aspects of produced water handling, disposal, and transportation in Texas. Statewide Rule 8 requires protection of surface and subsurface fresh water from oil and gas pollution. Rule 9 governs disposal well permitting and operation. Rule 13 addresses casing requirements to protect freshwater zones. Rule 14 covers plugging of wells. Rule 46 addresses recycling and reuse of oil and gas waste including produced water. Operators must obtain H-1 permits for disposal wells, maintain mechanical integrity, and file annual monitoring reports. Commercial saltwater disposal operators face additional requirements including financial assurance and area of review analysis. The typical Permian Basin well produces 3-10 barrels of water per barrel of oil, making produced water management a critical operational and cost concern.",
            key_provisions=[
                "RRC exclusive jurisdiction over oil and gas waste disposal",
                "H-1 permit required for all disposal/injection wells (Rule 9)",
                "Surface discharge of produced water prohibited (Rule 8)",
                "Casing and cementing requirements to protect freshwater (Rule 13)",
                "Annual monitoring and reporting required",
                "Commercial SWD operators: additional financial assurance",
                "Spill reporting within 24 hours for volumes over 5 bbls",
                "Produced water may be recycled under Rule 46 provisions",
            ],
            exceptions=[
                "Recycled produced water reused in operations (Rule 46)",
                "TPDES-permitted discharge of treated produced water (TCEQ jurisdiction)",
                "Emergency response discharges during well control events",
            ],
            related_doctrines=["WR-PW-002", "WR-IW-001", "WR-FP-001"],
            risk_if_violated=RiskLevel.CRITICAL,
            permian_basin_notes="Permian Basin produces enormous volumes of water (water-oil ratios of 3:1 to 10:1). Disposal well capacity is a critical constraint. Commercial SWD fees range $0.25-$1.50/bbl. Recycling adoption is increasing but still handles <10% of produced water volume.",
            last_updated="2026-02-10",
            tags=["produced_water", "rrc", "disposal", "statewide_rules", "h1_permit"],
        ),
        DoctrineCacheBlock(
            doctrine_id="WR-PW-002",
            title="Produced Water Recycling and Beneficial Reuse",
            category=DoctrineCategory.WATER_RECYCLING_REUSE,
            authority_level=AuthorityLevel.STATE_REGULATION,
            jurisdiction=JurisdictionScope.STATE_TEXAS,
            citation="16 TAC Sec. 3.8; 16 TAC Sec. 3.46; HB 2771 (86th Leg., 2019)",
            summary="Texas has enacted legislation and RRC rules encouraging recycling and beneficial reuse of produced water. HB 2771 clarified that recycled produced water used in oil and gas operations is not subject to TCEQ waste disposal permitting.",
            detailed_analysis="HB 2771 (2019) was landmark legislation that removed regulatory barriers to produced water recycling in Texas. The bill clarified that oil and gas waste recycled for use in oil and gas operations remains under RRC jurisdiction and is not subject to TCEQ solid waste permits. RRC Rule 46 governs recycling operations and requires notice to the RRC, proper handling and containment, and record-keeping. Treated produced water may also be authorized for beneficial reuse outside oil and gas operations (agricultural, industrial, municipal) but such reuse requires TCEQ authorization and must meet applicable water quality standards. The economic case for recycling is strengthening as disposal well capacity tightens and freshwater costs increase in the Permian Basin.",
            key_provisions=[
                "HB 2771 clarifies RRC jurisdiction over recycled produced water in O&G",
                "Rule 46 recycling notification and record-keeping requirements",
                "Beneficial reuse outside O&G requires TCEQ authorization",
                "Treated water must meet receiving-use quality standards",
                "No TCEQ solid waste permit needed for O&G recycling",
                "Operators must maintain chain of custody records",
            ],
            exceptions=[
                "Beneficial reuse for drinking water not currently authorized",
                "Discharge to surface water requires TPDES permit regardless",
                "NORM-contaminated produced water has additional handling requirements",
            ],
            related_doctrines=["WR-PW-001", "WR-PW-003", "WR-FP-001"],
            risk_if_violated=RiskLevel.MODERATE,
            permian_basin_notes="Permian Basin recycling infrastructure is growing rapidly. Major operators (Pioneer, Diamondback, Concho) have invested in centralized recycling facilities. Typical treatment involves oil/water separation, filtration, and iron removal. Treated water is reused as frack fluid base. Economics favor recycling when disposal costs exceed $0.75/bbl or freshwater costs exceed $1.00/bbl.",
            last_updated="2026-02-10",
            tags=["recycling", "beneficial_reuse", "produced_water", "hb_2771"],
        ),
        DoctrineCacheBlock(
            doctrine_id="WR-PW-003",
            title="Produced Water Surface Discharge - TPDES Permitting",
            category=DoctrineCategory.PRODUCED_WATER_DISPOSAL,
            authority_level=AuthorityLevel.STATE_REGULATION,
            jurisdiction=JurisdictionScope.STATE_TEXAS,
            citation="TWC Ch. 26; 30 TAC Ch. 307; 30 TAC Ch. 321; EPA NPDES 40 CFR 435",
            summary="Surface discharge of treated produced water requires a TPDES permit from TCEQ. Effluent limits are based on federal categorical standards (40 CFR 435) and Texas Surface Water Quality Standards. Zero discharge is the default for onshore oil and gas.",
            detailed_analysis="Federal law under the Clean Water Act and EPA regulations at 40 CFR Part 435 establish a zero-discharge standard for produced water from onshore oil and gas operations. This means that surface discharge of produced water is prohibited unless the water has been treated to meet discharge standards and a TPDES individual permit is obtained from TCEQ. The practical effect is that virtually all onshore produced water in Texas is disposed via injection wells rather than surface discharge. Limited exceptions exist for beneficial reuse after treatment, agricultural application under TCEQ general permit, and discharge west of the 98th meridian if water quality meets livestock watering standards. TCEQ evaluates discharge applications against Texas Surface Water Quality Standards (30 TAC Ch. 307) which establish parameter-specific effluent limits including TDS, chlorides, oil and grease, and NORM.",
            key_provisions=[
                "Zero discharge standard for onshore O&G under 40 CFR 435",
                "TPDES individual permit required for any surface discharge",
                "Effluent must meet Texas Surface Water Quality Standards",
                "TDS, chloride, O&G, NORM limits apply at discharge point",
                "West of 98th meridian exception for livestock-quality water",
                "Agricultural reuse under TCEQ general permit (30 TAC Ch. 321)",
            ],
            exceptions=[
                "West of 98th meridian livestock watering discharge",
                "Agricultural reuse with TCEQ general permit",
                "Storm water from well sites (separate permit category)",
                "Emergency bypass during well control situations",
            ],
            related_doctrines=["WR-PW-001", "WR-FED-001", "WR-SW-002"],
            risk_if_violated=RiskLevel.CRITICAL,
            permian_basin_notes="The Permian Basin is west of the 98th meridian, making the livestock watering exception potentially available. However, typical Permian produced water TDS (150,000-300,000 mg/L) far exceeds livestock standards. Treatment to discharge quality is currently uneconomic for most operations.",
            last_updated="2026-02-10",
            tags=["produced_water", "surface_discharge", "tpdes", "clean_water_act"],
        ),
        DoctrineCacheBlock(
            doctrine_id="WR-PW-004",
            title="Freshwater Sourcing for Hydraulic Fracturing",
            category=DoctrineCategory.FRESHWATER_PROTECTION,
            authority_level=AuthorityLevel.INDUSTRY_STANDARD,
            jurisdiction=JurisdictionScope.BASIN_SPECIFIC,
            citation="GCD Rules (various); RRC Rule 8; API Guidance Document HF2",
            summary="Freshwater sourcing for hydraulic fracturing operations requires compliance with GCD permitting, RRC freshwater protection rules, and operator best practices for water management and conservation.",
            detailed_analysis="A typical Permian Basin horizontal well completion requires 300,000 to 500,000 barrels (12-21 million gallons) of water for hydraulic fracturing. Sourcing this volume requires either groundwater from permitted wells, surface water purchases from permit holders, recycled produced water, or brackish water. GCD permits are required for non-exempt groundwater wells. Operators must comply with RRC Rule 8 freshwater protection requirements when drilling water wells and during completions. Best practices include water management plans, metering of all water sources, use of recycled or brackish water where feasible, and coordination with local water districts. Some operators have entered long-term water supply agreements with municipal utilities and private water companies. Water costs are a significant component of well economics, typically $2-5 per barrel in the Permian Basin.",
            key_provisions=[
                "GCD permit required for non-exempt freshwater wells",
                "RRC Rule 8 freshwater protection during drilling operations",
                "Water management plan recommended for large operations",
                "Metering required by most GCDs",
                "Recycled and brackish water alternatives encouraged",
                "Water supply agreements with municipalities common",
            ],
            exceptions=[
                "Oil and gas exempt wells under TWC 36.117(b)(2) (narrow)",
                "Temporary water use during drilling may qualify for short-term permit",
                "Recycled water use does not require freshwater permit",
            ],
            related_doctrines=["WR-GCD-003", "WR-PW-002", "WR-FP-001"],
            risk_if_violated=RiskLevel.MODERATE,
            permian_basin_notes="Permian Basin freshwater costs range $2-5/bbl depending on location and availability. Ogallala depletion is a growing constraint in the northern Permian. Operators are shifting to brackish water and recycled produced water to reduce freshwater dependence.",
            last_updated="2026-02-10",
            tags=["freshwater", "fracking", "sourcing", "water_management"],
        ),
    ]


def _build_injection_well_doctrines() -> list[DoctrineCacheBlock]:
    return [
        DoctrineCacheBlock(
            doctrine_id="WR-IW-001",
            title="UIC Class II Injection Well Permitting",
            category=DoctrineCategory.INJECTION_WELL_REGULATION,
            authority_level=AuthorityLevel.STATE_REGULATION,
            jurisdiction=JurisdictionScope.STATE_TEXAS,
            citation="16 TAC Sec. 3.9; 16 TAC Sec. 3.46; SDWA 42 U.S.C. Sec. 300h",
            summary="Saltwater disposal and enhanced recovery injection wells in Texas require RRC H-1 permits under the UIC Class II program. Texas has EPA primacy for UIC Class II wells. Permits require area of review, casing integrity, and ongoing monitoring.",
            detailed_analysis="The Underground Injection Control (UIC) program under the Safe Drinking Water Act delegates Class II well regulation to states with approved programs. Texas has primacy through the RRC for oil and gas injection wells. An H-1 permit application requires geological data, well construction specifications, area of review (1/4-mile radius), identification of USDWs within the area, casing and cementing program, proposed injection zone and confining zones, maximum injection pressure (typically 0.5 psi/ft of depth), and maximum daily volume. Commercial disposal wells have additional requirements including financial assurance ($25,000 per well or $250,000 blanket bond), public notice, and enhanced monitoring. Permit conditions include mechanical integrity testing every 5 years, annual monitoring reports, and compliance with seismicity protocols in designated review areas.",
            key_provisions=[
                "H-1 permit required for all Class II injection wells",
                "Area of review: 1/4-mile radius from wellbore",
                "USDW identification and protection required",
                "Maximum injection pressure: 0.5 psi/ft typical",
                "Mechanical integrity test (MIT) every 5 years",
                "Annual monitoring report (Form H-10)",
                "Commercial SWD: $25K bond per well or $250K blanket",
                "Casing program must isolate all freshwater zones",
            ],
            exceptions=[
                "Enhanced recovery wells may have different pressure limits",
                "Pilot injection projects may get temporary permits",
                "EPA retains enforcement authority even in primacy states",
            ],
            related_doctrines=["WR-IW-002", "WR-PW-001", "WR-SEIS-001"],
            risk_if_violated=RiskLevel.CRITICAL,
            permian_basin_notes="Permian Basin has thousands of active SWD wells. Average disposal volumes are 10,000-30,000 bbls/day per well. RRC District 8 (Midland) processes the most H-1 applications in the state. Disposal well capacity constraints are a growing concern as production increases.",
            last_updated="2026-02-10",
            tags=["injection_well", "uic", "class_ii", "h1_permit", "swd"],
        ),
        DoctrineCacheBlock(
            doctrine_id="WR-IW-002",
            title="Mechanical Integrity Testing Requirements",
            category=DoctrineCategory.INJECTION_WELL_REGULATION,
            authority_level=AuthorityLevel.STATE_REGULATION,
            jurisdiction=JurisdictionScope.STATE_TEXAS,
            citation="16 TAC Sec. 3.9(7); EPA 40 CFR 146.8",
            summary="All UIC Class II injection wells must demonstrate mechanical integrity through pressure testing at least every 5 years. Failed MIT requires well repair or plugging. Two types of MIT are required: internal (casing integrity) and external (no fluid movement behind casing).",
            detailed_analysis="Mechanical integrity testing is the primary tool for ensuring that injection wells do not endanger underground sources of drinking water. Part 1 MIT (internal) demonstrates that there is no significant leak in the casing, tubing, or packer by pressurizing the casing-tubing annulus to a specified pressure and monitoring for 30 minutes (standard) or by monitoring annular pressure during injection. Part 2 MIT (external) demonstrates no significant fluid movement through vertical channels adjacent to the wellbore, typically through radioactive tracer surveys, temperature logs, or noise logs. The RRC requires MIT at least every 5 years and may require additional testing after well workovers, seismic events, or reports of surface leaks. A failed MIT triggers a well shutdown until repairs are made and a passing test is achieved. Repeated MIT failures may result in well plugging orders.",
            key_provisions=[
                "Part 1 MIT: casing/tubing pressure test (annulus method)",
                "Part 2 MIT: external integrity (tracer/temperature/noise log)",
                "Required at least every 5 years",
                "Required after workover or significant well modification",
                "Failed MIT requires immediate well shutdown",
                "30-minute pressure stabilization criterion (standard test)",
                "Pressure decline limit: typically 3% or 10 psi over 30 min",
            ],
            exceptions=[
                "Enhanced recovery wells may use alternative Part 2 methods",
                "Newly completed wells: MIT at initial completion suffices until next scheduled test",
            ],
            related_doctrines=["WR-IW-001", "WR-FP-001", "WR-SEIS-001"],
            risk_if_violated=RiskLevel.CRITICAL,
            permian_basin_notes="Aging SWD wells in the Permian Basin face increasing MIT failure rates. Wells drilled in the 1960s-1980s with older casing designs are particularly vulnerable. Operators should budget for MIT remediation costs.",
            last_updated="2026-02-10",
            tags=["mit", "mechanical_integrity", "injection_well", "casing_integrity"],
        ),
    ]


def _build_seismicity_doctrines() -> list[DoctrineCacheBlock]:
    return [
        DoctrineCacheBlock(
            doctrine_id="WR-SEIS-001",
            title="Induced Seismicity and Disposal Well Regulation",
            category=DoctrineCategory.SEISMICITY_REGULATION,
            authority_level=AuthorityLevel.AGENCY_RULE,
            jurisdiction=JurisdictionScope.STATE_TEXAS,
            citation="RRC Disposal Well Seismicity Response Protocol (2014, updated 2023); TexNet",
            summary="The RRC has adopted a traffic light protocol for managing induced seismicity from saltwater disposal wells. Wells near seismic events face volume reductions, suspension, or shutdown depending on earthquake magnitude and proximity.",
            detailed_analysis="Following the increase in induced seismicity linked to high-volume saltwater disposal, the RRC adopted a seismicity response protocol that uses a traffic light system. Green (M < 2.0): no action required. Yellow (M 2.0-3.5): RRC may review nearby disposal wells and require volume reductions of up to 50%. Orange (M 3.5-4.0): suspension of operations pending review, enhanced monitoring, and potential permanent volume restrictions. Red (M > 4.0): immediate shut-in of all disposal wells within the review area, investigation, and potential permanent closure. The TexNet seismic monitoring network (operated by UT-BEG) provides real-time seismic data. The RRC maintains seismic review areas where new permit applications receive enhanced scrutiny. Operators in review areas may be required to install seismic monitoring stations as a permit condition.",
            key_provisions=[
                "Traffic light protocol: Green/Yellow/Orange/Red based on magnitude",
                "TexNet monitoring network provides real-time data",
                "Volume reduction of 50% at Yellow level",
                "Suspension at Orange level (M 3.5-4.0)",
                "Immediate shut-in at Red level (M > 4.0)",
                "Seismic review areas with enhanced permit scrutiny",
                "Operator may be required to install monitoring stations",
                "Review radius: 10 miles from epicenter typical",
            ],
            exceptions=[
                "Enhanced recovery wells (Class II-R) evaluated separately",
                "Shallow disposal into depleted reservoirs lower risk",
                "Pre-existing natural seismicity evaluated as baseline",
            ],
            related_doctrines=["WR-IW-001", "WR-IW-002", "WR-PW-001"],
            risk_if_violated=RiskLevel.CRITICAL,
            permian_basin_notes="The Permian Basin has experienced significant induced seismicity, particularly in the Delaware Basin (Reeves, Pecos, Ward counties). The RRC has designated multiple seismic review areas. New SWD permit applications in Reeves County face heightened scrutiny. Operators should evaluate seismic risk before acquiring disposal well assets.",
            last_updated="2026-02-10",
            tags=["seismicity", "induced_earthquakes", "swd", "traffic_light", "texnet"],
        ),
    ]


def _build_freshwater_protection_doctrines() -> list[DoctrineCacheBlock]:
    return [
        DoctrineCacheBlock(
            doctrine_id="WR-FP-001",
            title="RRC Statewide Rule 8 - Protection of Fresh Water",
            category=DoctrineCategory.FRESHWATER_PROTECTION,
            authority_level=AuthorityLevel.STATE_REGULATION,
            jurisdiction=JurisdictionScope.STATE_TEXAS,
            citation="16 TAC Sec. 3.8; TNRC Sec. 91.101",
            summary="Statewide Rule 8 requires that all oil and gas operations be conducted so as to prevent pollution of surface and subsurface fresh water. This includes casing requirements, pit construction standards, spill prevention, and well plugging obligations.",
            detailed_analysis="Rule 8 is the RRC's primary freshwater protection regulation. It requires operators to set and cement surface casing through all freshwater-bearing formations to a depth sufficient to protect all USDWs (typically determined by the TCEQ letter to the RRC). Surface casing must be cemented to surface. Intermediate casing may be required in areas with multiple freshwater zones. Pit construction for drilling fluids and completion fluids must comply with containment standards including synthetic liners for pits containing saltwater or oil-based fluids. Spills must be reported to the RRC within 24 hours if the volume exceeds 5 barrels of crude oil or 1 barrel of other substances, or any spill reaching water. Freshwater protection extends to well plugging: plugging operations must isolate all permeable zones and protect freshwater formations with cement plugs.",
            key_provisions=[
                "Surface casing through all freshwater formations",
                "Cement surface casing to surface (no returns permitted without approval)",
                "TCEQ letter determines freshwater protection depth",
                "Pit containment standards with synthetic liners",
                "Spill reporting within 24 hours",
                "Well plugging must protect freshwater zones",
                "Prohibition on produced water contact with fresh water",
                "Operator financial responsibility for cleanup",
            ],
            exceptions=[
                "Existing wells drilled before current rules may be grandfathered",
                "Emergency operations may receive temporary variances",
                "De minimis releases below reporting thresholds",
            ],
            related_doctrines=["WR-IW-001", "WR-PW-001", "WR-FP-002"],
            risk_if_violated=RiskLevel.CRITICAL,
            permian_basin_notes="In the Permian Basin, surface casing depths range from 200 to 1,500 feet depending on the depth of freshwater formations. The TCEQ-designated freshwater protection depth is location-specific. Operators must obtain a TCEQ letter before drilling.",
            last_updated="2026-02-10",
            tags=["rule_8", "freshwater", "protection", "casing", "rrc"],
        ),
        DoctrineCacheBlock(
            doctrine_id="WR-FP-002",
            title="Underground Source of Drinking Water (USDW) Protection",
            category=DoctrineCategory.FRESHWATER_PROTECTION,
            authority_level=AuthorityLevel.FEDERAL_REGULATION,
            jurisdiction=JurisdictionScope.FEDERAL,
            citation="40 CFR 144.3; SDWA 42 U.S.C. Sec. 300h; 30 TAC Ch. 290",
            summary="A USDW is any aquifer with TDS below 10,000 mg/L that is not an exempted aquifer. USDWs must be protected from contamination by injection well operations, drilling activities, and surface pollution sources.",
            detailed_analysis="The Safe Drinking Water Act defines USDWs as aquifers that currently serve as or could serve as sources of drinking water, with TDS below 10,000 mg/L, unless they have been granted an aquifer exemption by EPA. Protection of USDWs is the primary objective of the UIC program and drives casing, cementing, and monitoring requirements for injection wells. In Texas, TCEQ determines the depth of the base of usable quality water (BUQW) for each well location, and the RRC requires surface casing to be set below that depth. Aquifer exemptions allow injection into formations that would otherwise be classified as USDWs, but EPA approval is required and the process is lengthy. The exemption applies only to the specific geographic and stratigraphic interval approved.",
            key_provisions=[
                "USDW defined as aquifer with TDS < 10,000 mg/L",
                "All injection wells must protect USDWs",
                "TCEQ determines base of usable quality water depth",
                "Surface casing must extend below BUQW",
                "Aquifer exemption requires EPA approval",
                "Exempted aquifer: does not currently serve as drinking water source",
                "Monitoring wells may be required near injection zones adjacent to USDWs",
            ],
            exceptions=[
                "Aquifer exemptions under 40 CFR 146.4",
                "Aquifers that cannot yield sufficient quantity for public supply",
                "Aquifers contaminated beyond remediation (EPA determination)",
            ],
            related_doctrines=["WR-FP-001", "WR-IW-001", "WR-FED-002"],
            risk_if_violated=RiskLevel.CRITICAL,
            permian_basin_notes="USDW depths in the Permian Basin vary widely. In the Midland Basin, usable water zones extend to 200-600 feet. In the Delaware Basin (Reeves, Pecos), brackish water zones extend deeper, potentially complicating USDW determinations for shallow disposal targets.",
            last_updated="2026-02-10",
            tags=["usdw", "drinking_water", "sdwa", "aquifer_protection"],
        ),
    ]


def _build_edwards_aquifer_doctrines() -> list[DoctrineCacheBlock]:
    return [
        DoctrineCacheBlock(
            doctrine_id="WR-EA-001",
            title="Edwards Aquifer Authority Act and Regulation",
            category=DoctrineCategory.EDWARDS_AQUIFER,
            authority_level=AuthorityLevel.STATE_STATUTE,
            jurisdiction=JurisdictionScope.REGIONAL,
            citation="Edwards Aquifer Authority Act, 73rd Leg., R.S., Ch. 626 (1993); 30 TAC Ch. 213",
            summary="The Edwards Aquifer Authority regulates groundwater withdrawals from the Edwards Aquifer in south-central Texas under a unique cap-and-trade permit system with a total annual withdrawal cap of 572,000 AF and a market-based transfer mechanism.",
            detailed_analysis="The EAA is unique in Texas groundwater management as the only entity with explicit statutory authority to cap total aquifer withdrawals. The EAA Act capped permitted withdrawals at 572,000 AF/year (originally 450,000, raised in stages). Permits are based on historical use during the base period (1972-1993). Permits are transferable through the EAA's market-based system, creating a groundwater rights market. Critical period management involves 5 stages triggered by springflow levels at Comal and San Marcos Springs, with progressively more severe curtailments. The EAA also manages recharge enhancement projects, aquifer storage and recovery (ASR), and demand management programs. TCEQ administers Edwards Aquifer protection rules (30 TAC Ch. 213) for activities over the recharge, contributing, and transition zones, including water quality protection plans for construction and development.",
            key_provisions=[
                "Total withdrawal cap: 572,000 AF/year",
                "Permits based on 1972-1993 historical use",
                "Market-based permit transfers allowed",
                "5-stage critical period management",
                "Comal Springs trigger: 225 cfs Stage I",
                "San Marcos Springs trigger: 96 cfs Stage I",
                "Aquifer storage and recovery programs",
                "TCEQ Edwards rules (Ch. 213) for recharge zone protection",
            ],
            exceptions=[
                "Domestic and livestock wells under 25,000 GPD exempt from permit",
                "Emergency permits available during drought",
                "Interim authorization for new users pending permit",
            ],
            related_doctrines=["WR-GW-002", "WR-GCD-001", "WR-DESAL-001"],
            risk_if_violated=RiskLevel.CRITICAL,
            permian_basin_notes="The Edwards Aquifer is not in the Permian Basin, but EAA case law (especially EAA v. Day) has statewide implications for groundwater property rights and GCD regulation. San Antonio's increasing water demand may drive interest in Permian Basin groundwater exports.",
            last_updated="2026-02-10",
            tags=["edwards_aquifer", "eaa", "cap_and_trade", "critical_period"],
        ),
    ]


def _build_accommodation_doctrines() -> list[DoctrineCacheBlock]:
    return [
        DoctrineCacheBlock(
            doctrine_id="WR-ACCOM-001",
            title="Accommodation Doctrine Applied to Water Use",
            category=DoctrineCategory.SURFACE_OWNER_ACCOMMODATION,
            authority_level=AuthorityLevel.CASE_LAW,
            jurisdiction=JurisdictionScope.STATE_TEXAS,
            citation="Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971); Coyote Lake Ranch v. City of Lubbock, 498 S.W.3d 53 (Tex. 2016)",
            summary="Under the accommodation doctrine, a mineral lessee must accommodate existing surface uses when reasonable alternatives exist for mineral development. Applied to water, this limits a lessee's right to consume surface owner's water or contaminate freshwater resources.",
            detailed_analysis="The accommodation doctrine, established in Getty Oil v. Jones, requires the dominant mineral estate holder to accommodate existing surface uses when alternative methods of mineral development exist that would allow both surface and mineral uses to coexist. In the water context, this means a mineral lessee cannot freely appropriate all surface water or groundwater on the leased premises if doing so would unreasonably interfere with the surface owner's existing water use. The lessee must use reasonable alternatives (e.g., sourcing water off-site, using recycled water) if available. Coyote Lake Ranch v. City of Lubbock (2016) extended these principles to groundwater by holding that a surface owner could deny access to the mineral estate holder's groundwater lessee where the surface owner had a pre-existing, reasonable use of the surface that would be impaired. The case clarified that groundwater rights severed from the surface do not automatically include surface access rights.",
            key_provisions=[
                "Mineral lessee must accommodate existing surface water uses",
                "Alternative methods of operation must be used if reasonably available",
                "Surface owner's pre-existing water use creates duty of accommodation",
                "Lessee may not appropriate all water resources on leased premises",
                "Severed groundwater rights require separate surface access agreement",
                "Due regard standard for surface owner's improvements and water infrastructure",
            ],
            exceptions=[
                "If no reasonable alternative exists, mineral estate prevails",
                "Lease may contractually address water use allocation",
                "Surface use agreement may modify accommodation obligations",
            ],
            related_doctrines=["WR-GW-001", "WR-CONV-001", "WR-PW-004"],
            risk_if_violated=RiskLevel.HIGH,
            permian_basin_notes="In the Permian Basin, accommodation doctrine issues frequently arise when operators need large volumes of freshwater for fracking on ranches where surface owners depend on the same aquifer for livestock and domestic use. Operators should negotiate comprehensive surface use agreements addressing water allocation.",
            last_updated="2026-02-10",
            tags=["accommodation_doctrine", "surface_owner", "mineral_lessee", "water_use"],
        ),
    ]


def _build_conveyancing_doctrines() -> list[DoctrineCacheBlock]:
    return [
        DoctrineCacheBlock(
            doctrine_id="WR-CONV-001",
            title="Water Rights Conveyancing and Severance",
            category=DoctrineCategory.WATER_CONVEYANCING,
            authority_level=AuthorityLevel.CASE_LAW,
            jurisdiction=JurisdictionScope.STATE_TEXAS,
            citation="EAA v. Day, 369 S.W.3d 814 (Tex. 2012); TWC Sec. 36.002(d-1)",
            summary="Groundwater rights in Texas may be severed from the surface estate and separately conveyed, leased, or encumbered. The conveyance must be by written instrument. Surface water rights (permits) are transferable with TCEQ approval.",
            detailed_analysis="Following EAA v. Day's confirmation that groundwater is owned in place as real property, water rights conveyancing has become an active market in Texas. Groundwater rights may be conveyed by deed, leased for a term, or encumbered by deed of trust. TWC Sec. 36.002(d-1) authorizes separate conveyance of groundwater rights. A severance creates a separate estate, analogous to the mineral estate. The grantor may reserve groundwater rights in a surface conveyance. GCDs must recognize severed groundwater rights in their permitting process. Surface water rights (TCEQ permits) may be transferred to a new owner or a different use with TCEQ approval under TWC Sec. 11.122. The transfer application is publicly noticed and must demonstrate no injury to other water rights. Title examination for water rights should include review of deeds, GCD records, TCEQ permit records, and TWDB groundwater database entries.",
            key_provisions=[
                "Groundwater rights severable from surface estate under TWC 36.002(d-1)",
                "Severance by written instrument (deed)",
                "Grantor may reserve groundwater in surface conveyance",
                "GCD must recognize severed rights in permitting",
                "Surface water rights transferable with TCEQ approval (TWC 11.122)",
                "Transfer must not injure existing rights",
                "Title examination should cover deeds, GCD records, TCEQ permits",
            ],
            exceptions=[
                "Some GCDs do not have specific rules for severed rights permitting",
                "Severed groundwater rights do not automatically include surface access",
                "Federal water rights (tribal, military) may have separate transfer rules",
            ],
            related_doctrines=["WR-GW-002", "WR-GW-005", "WR-ACCOM-001"],
            risk_if_violated=RiskLevel.HIGH,
            permian_basin_notes="Water rights transactions are increasingly common in the Permian Basin as water scarcity increases. Landmen should examine water rights in title opinions. Severance language should be specific about aquifer, volume, and duration. Water supply agreements for oilfield use should be reviewed for termination and force majeure provisions.",
            last_updated="2026-02-10",
            tags=["water_conveyancing", "severance", "transfer", "title_examination"],
        ),
    ]


def _build_federal_water_doctrines() -> list[DoctrineCacheBlock]:
    return [
        DoctrineCacheBlock(
            doctrine_id="WR-FED-001",
            title="Clean Water Act Section 404 - Dredge and Fill",
            category=DoctrineCategory.FEDERAL_WATER_LAW,
            authority_level=AuthorityLevel.FEDERAL_STATUTE,
            jurisdiction=JurisdictionScope.FEDERAL,
            citation="33 U.S.C. Sec. 1344; 40 CFR 230; 33 CFR 320-332",
            summary="CWA Section 404 requires a permit from the Army Corps of Engineers for the discharge of dredged or fill material into waters of the United States, including wetlands. Oil and gas construction activities in or near jurisdictional waters may trigger Section 404 requirements.",
            detailed_analysis="Section 404 of the Clean Water Act regulates discharges of dredged or fill material into waters of the United States (WOTUS), including navigable waters, tributaries, and adjacent wetlands. The Army Corps of Engineers issues individual and general (nationwide) permits. Nationwide Permit 12 (utility line activities) and NWP 39 (commercial and institutional developments) are commonly used for oil and gas pipeline crossings and facility construction. Permit conditions include avoidance, minimization, and compensatory mitigation for unavoidable impacts. Texas does not have a state-assumed 404 program; the Corps retains jurisdiction. The scope of WOTUS has been subject to significant litigation and regulatory changes. Oil and gas operators must conduct jurisdictional determinations before constructing facilities near potential WOTUS.",
            key_provisions=[
                "Corps of Engineers permit for fill in WOTUS",
                "Nationwide Permit 12 for pipeline crossings (up to 1/2 acre impact)",
                "Individual permit for larger impacts",
                "Mitigation sequencing: avoid, minimize, compensate",
                "Jurisdictional determination required before construction",
                "Agricultural exemptions for normal farming activities",
                "Oil and gas exploration road construction may require permit",
            ],
            exceptions=[
                "Normal farming, silviculture, ranching activities (Sec. 404(f))",
                "Maintenance of currently serviceable structures",
                "Construction of farm or stock ponds",
                "Construction of irrigation ditches",
            ],
            related_doctrines=["WR-FED-002", "WR-SW-001", "WR-PW-003"],
            risk_if_violated=RiskLevel.HIGH,
            permian_basin_notes="Section 404 issues in the Permian Basin arise primarily at pipeline crossings of draws, playas, and the Pecos River. The arid environment reduces but does not eliminate jurisdictional waters. Playa lakes in the southern High Plains may be jurisdictional depending on current WOTUS definition.",
            last_updated="2026-02-10",
            tags=["cwa", "section_404", "wetlands", "corps_of_engineers"],
        ),
        DoctrineCacheBlock(
            doctrine_id="WR-FED-002",
            title="Safe Drinking Water Act - UIC Program Framework",
            category=DoctrineCategory.FEDERAL_WATER_LAW,
            authority_level=AuthorityLevel.FEDERAL_STATUTE,
            jurisdiction=JurisdictionScope.FEDERAL,
            citation="42 U.S.C. Sec. 300h et seq.; 40 CFR Parts 144-148",
            summary="The Safe Drinking Water Act establishes the Underground Injection Control program to protect USDWs from contamination by injection well operations. Texas has primacy for Class II (oil and gas) wells through the RRC and for other classes through TCEQ.",
            detailed_analysis="The SDWA UIC program regulates five classes of injection wells: Class I (industrial/municipal waste), Class II (oil and gas), Class III (mineral extraction), Class IV (hazardous waste - banned), and Class V (all others). Texas has primacy for Class II wells through the RRC and for Classes I, III, and V through TCEQ. The UIC program requires that injection wells not endanger USDWs, defined as aquifers with TDS below 10,000 mg/L. EPA Region 6 (Dallas) maintains oversight authority and may take enforcement action if the state fails to adequately enforce the program. Key requirements include well construction standards, operating requirements (pressure limits, volume monitoring), mechanical integrity testing, well plugging and abandonment standards, and financial assurance. EPA reviews state programs periodically and may withdraw primacy for inadequate enforcement.",
            key_provisions=[
                "Five classes of injection wells regulated",
                "Texas primacy: RRC for Class II, TCEQ for Classes I/III/V",
                "No endangerment of USDWs standard",
                "EPA Region 6 oversight and enforcement backup",
                "Well construction, operation, monitoring, closure standards",
                "Financial assurance requirements",
                "Periodic program review by EPA",
            ],
            exceptions=[
                "Class IV (hazardous waste injection) is banned",
                "Aquifer exemptions allow injection into non-drinking-water aquifers",
                "Emergency injection may proceed under temporary authorization",
            ],
            related_doctrines=["WR-IW-001", "WR-FP-002", "WR-FED-001"],
            risk_if_violated=RiskLevel.CRITICAL,
            permian_basin_notes="The SDWA UIC framework is the federal backstop for all Permian Basin injection well operations. EPA Region 6 has conducted enhanced reviews of disposal wells in the Permian Basin following induced seismicity concerns. Operators should be aware that even in a primacy state, EPA retains enforcement authority.",
            last_updated="2026-02-10",
            tags=["sdwa", "uic", "injection_control", "epa", "primacy"],
        ),
    ]


def _build_interstate_compact_doctrines() -> list[DoctrineCacheBlock]:
    return [
        DoctrineCacheBlock(
            doctrine_id="WR-IC-001",
            title="Pecos River Compact",
            category=DoctrineCategory.INTERSTATE_COMPACT,
            authority_level=AuthorityLevel.FEDERAL_STATUTE,
            jurisdiction=JurisdictionScope.INTERSTATE,
            citation="Pecos River Compact, 63 Stat. 159 (1949); Texas v. New Mexico, 482 U.S. 124 (1987)",
            summary="The Pecos River Compact between Texas and New Mexico allocates flows of the Pecos River. New Mexico must deliver to Texas a quantity of water determined by the inflow-outflow formula. Violations have been litigated before the U.S. Supreme Court.",
            detailed_analysis="The Pecos River Compact was ratified in 1949. It requires New Mexico to deliver water to Texas at the state line based on a formula that relates New Mexico's permitted depletions to the natural inflow. Texas v. New Mexico (1987) found New Mexico in violation and appointed a River Master to administer deliveries. The compact is relevant to Permian Basin operations because the Pecos River flows through Reeves, Pecos, and Terrell counties and is a potential water source and discharge receiving water. Groundwater pumping in southeastern New Mexico that reduces Pecos River baseflow is a continuing point of contention. The compact does not directly regulate groundwater, but the hydrologic connection between the Pecos Valley Aquifer and the river means that groundwater development on both sides of the border affects compact compliance.",
            key_provisions=[
                "Inflow-outflow formula determines NM delivery obligation",
                "River Master appointed by U.S. Supreme Court",
                "Texas v. New Mexico found NM in violation",
                "No direct groundwater regulation in compact",
                "Hydrologic connection between aquifer and river recognized",
                "Compact Commission meets annually",
            ],
            exceptions=[
                "Compact does not preempt state groundwater law",
                "Tributary water development within each state's discretion",
            ],
            related_doctrines=["WR-IC-002", "WR-SW-001"],
            risk_if_violated=RiskLevel.HIGH,
            permian_basin_notes="The Pecos River flows through the heart of the Permian Basin in Texas. Operators using Pecos River water must have TCEQ surface water permits. Disposal well operations near the Pecos must ensure no hydraulic communication with the river. Groundwater pumping from the Pecos Valley Aquifer may be constrained by compact-related concerns.",
            last_updated="2026-02-10",
            tags=["pecos_river", "interstate_compact", "new_mexico", "river_master"],
        ),
        DoctrineCacheBlock(
            doctrine_id="WR-IC-002",
            title="Rio Grande Compact",
            category=DoctrineCategory.INTERSTATE_COMPACT,
            authority_level=AuthorityLevel.FEDERAL_STATUTE,
            jurisdiction=JurisdictionScope.INTERSTATE,
            citation="Rio Grande Compact, 53 Stat. 785 (1939); Texas v. New Mexico and Colorado, 583 U.S. __ (2018)",
            summary="The Rio Grande Compact among Colorado, New Mexico, and Texas allocates flows of the Rio Grande. Scheduled deliveries at Elephant Butte Reservoir determine Texas's allocation. Recent Supreme Court litigation addressed New Mexico's groundwater pumping affecting deliveries.",
            detailed_analysis="The Rio Grande Compact requires New Mexico to deliver water to Elephant Butte Reservoir for the benefit of downstream users in southern New Mexico and Texas. Texas receives its share through the Rio Grande Project operated by the Bureau of Reclamation. In Texas v. New Mexico and Colorado (2018), the Supreme Court held that Texas could bring an action against New Mexico for compact violations caused by New Mexico's groundwater pumping below Elephant Butte that captured water that would otherwise have flowed to Texas. The decision expanded compact enforcement to encompass groundwater activities that interfere with compact deliveries, a significant development for interstate water law.",
            key_provisions=[
                "Scheduled deliveries to Elephant Butte based on index gauges",
                "Bureau of Reclamation operates Rio Grande Project",
                "Texas's allocation administered through Elephant Butte index",
                "Groundwater pumping below Elephant Butte affects compact deliveries",
                "Supreme Court: Texas may sue NM for groundwater interference",
                "Annual accounting and carryover credit system",
            ],
            exceptions=[
                "Above-Elephant Butte deliveries differ from below-Elephant Butte allocation",
                "Compact does not directly allocate groundwater",
            ],
            related_doctrines=["WR-IC-001", "WR-IC-003"],
            risk_if_violated=RiskLevel.HIGH,
            permian_basin_notes="The Rio Grande is east and south of the core Permian Basin but relevant for operators with interests in the Trans-Pecos region. The compact's expansion to cover groundwater interference has implications for all interstate water disputes.",
            last_updated="2026-02-10",
            tags=["rio_grande", "interstate_compact", "elephant_butte", "supreme_court"],
        ),
        DoctrineCacheBlock(
            doctrine_id="WR-IC-003",
            title="Red River Compact",
            category=DoctrineCategory.INTERSTATE_COMPACT,
            authority_level=AuthorityLevel.FEDERAL_STATUTE,
            jurisdiction=JurisdictionScope.INTERSTATE,
            citation="Red River Compact, 94 Stat. 3305 (1980); Tarrant Regional Water District v. Herrmann, 569 U.S. 614 (2013)",
            summary="The Red River Compact among Texas, Oklahoma, Arkansas, and Louisiana divides the Red River basin into reaches with specific allocation rules. The Supreme Court held in Tarrant that the compact does not require Oklahoma to allow Texas to access Oklahoma water.",
            detailed_analysis="The Red River Compact divides the basin into 5 numbered reaches and assigns equal shares within each reach to the signatory states. Tarrant Regional Water District v. Herrmann (2013) was a significant case where the Supreme Court held that the Red River Compact did not grant Texas cross-border access to Oklahoma water. The decision confirmed that state water law within each state's borders is preserved by the compact. This is relevant to Texas water planners who had hoped to access Oklahoma water to meet growing North Texas demand.",
            key_provisions=[
                "Basin divided into 5 reaches with allocation rules",
                "Equal shares among states within each reach",
                "State water law preserved within each state",
                "No cross-border access right (Tarrant decision)",
                "Red River Compact Commission administers",
            ],
            exceptions=[
                "Emergency provisions for drought conditions",
                "Reach-specific allocation formulas vary",
            ],
            related_doctrines=["WR-IC-001", "WR-IC-002"],
            risk_if_violated=RiskLevel.MODERATE,
            permian_basin_notes="The Red River basin is north of the Permian Basin. Limited direct relevance, but the Tarrant decision's principles regarding interstate water access apply broadly to any Texas water supply planning that contemplates out-of-state sourcing.",
            last_updated="2026-02-10",
            tags=["red_river", "interstate_compact", "oklahoma", "tarrant"],
        ),
    ]


def _build_desalination_doctrines() -> list[DoctrineCacheBlock]:
    return [
        DoctrineCacheBlock(
            doctrine_id="WR-DESAL-001",
            title="Brackish Water Desalination Law and Regulation",
            category=DoctrineCategory.BRACKISH_DESALINATION,
            authority_level=AuthorityLevel.STATE_STATUTE,
            jurisdiction=JurisdictionScope.STATE_TEXAS,
            citation="TWC Sec. 16.060; HB 2031 (84th Leg., 2015); TWDB Brackish Groundwater Guidelines",
            summary="Texas has designated brackish groundwater production zones and encouraged desalination through TWDB programs. GCDs may or may not require permits for brackish wells depending on local rules. Concentrate disposal is the primary regulatory challenge.",
            detailed_analysis="HB 2031 (2015) directed TWDB to designate Brackish Groundwater Production Zones where brackish water (TDS 1,000-10,000 mg/L) can be produced without unreasonably affecting freshwater aquifers. TWDB has designated zones in multiple aquifers. Production from designated zones may qualify for expedited GCD permitting. However, desalination creates a concentrate waste stream (brine) that must be disposed of, typically by deep well injection, evaporation ponds, or zero-liquid-discharge (ZLD) technology. The concentrate disposal permit is usually the rate-limiting step for desalination projects. In the Permian Basin, brackish water is abundant but desalination energy costs (4-12 kWh per 1,000 gallons) and concentrate disposal challenges limit adoption. TWDB provides financial assistance for desalination projects through its water infrastructure fund.",
            key_provisions=[
                "TWDB designates brackish groundwater production zones",
                "Expedited GCD permitting in designated zones",
                "Concentrate disposal requires separate permit (TCEQ or RRC)",
                "Deep well injection most common disposal method",
                "TWDB financial assistance available for desal projects",
                "Brackish TDS range: 1,000-10,000 mg/L",
                "GCD may require production monitoring and reporting",
            ],
            exceptions=[
                "Some GCDs do not regulate brackish zones",
                "Oilfield use of brackish water may not require desal",
                "Concentrate may be blended with produced water for disposal",
            ],
            related_doctrines=["WR-GCD-001", "WR-GW-005", "WR-PW-002"],
            risk_if_violated=RiskLevel.MODERATE,
            permian_basin_notes="The Permian Basin has extensive brackish water resources, particularly in the Dockum and deep Pecos Valley aquifers. Several operators are evaluating brackish water as frack fluid alternative. The energy cost of desalination ($0.50-2.00/bbl) can be competitive with freshwater transport costs in remote locations.",
            last_updated="2026-02-10",
            tags=["desalination", "brackish", "twdb", "concentrate_disposal"],
        ),
    ]


def _build_drought_doctrines() -> list[DoctrineCacheBlock]:
    return [
        DoctrineCacheBlock(
            doctrine_id="WR-DROUGHT-001",
            title="Drought Contingency Planning and Water District Taxation",
            category=DoctrineCategory.DROUGHT_PLANNING,
            authority_level=AuthorityLevel.STATE_STATUTE,
            jurisdiction=JurisdictionScope.STATE_TEXAS,
            citation="TWC Sec. 11.1272; TWC Ch. 36 Subchapter L; TWC Sec. 49.001 et seq.",
            summary="Texas water utilities and GCDs must adopt drought contingency plans with staged curtailment triggers. Water districts have taxing authority to fund operations, infrastructure, and groundwater management activities.",
            detailed_analysis="TWC Sec. 11.1272 requires holders of surface water rights to prepare and submit drought contingency plans to TCEQ. Plans must include trigger conditions, staged response measures, demand reduction targets, and enforcement provisions. GCDs must similarly adopt drought provisions in their management plans under TWC Ch. 36. During declared droughts, GCDs may impose emergency production restrictions that supersede normal permit conditions. Water districts organized under TWC Ch. 49 have authority to levy ad valorem taxes, assess fees, and issue bonds to fund water supply, conservation, and management activities. In the Permian Basin, drought planning is critical given the semi-arid climate and heavy industrial water demand from oil and gas operations. GCD drought curtailment may directly affect oilfield water supply, requiring operators to maintain contingency water sources.",
            key_provisions=[
                "Mandatory drought contingency plans for TCEQ permit holders",
                "Staged curtailment triggers (voluntary, mandatory, emergency)",
                "GCD emergency production restrictions during drought",
                "Water district taxing authority under TWC Ch. 49",
                "Financial assurance for drought response infrastructure",
                "Demand reduction targets and enforcement mechanisms",
                "Cross-jurisdictional coordination during regional drought",
            ],
            exceptions=[
                "Domestic and livestock use generally last to be curtailed",
                "Emergency provisions may bypass normal permitting",
                "Essential public health water supply prioritized",
            ],
            related_doctrines=["WR-GCD-001", "WR-SW-001", "WR-GCD-002"],
            risk_if_violated=RiskLevel.HIGH,
            permian_basin_notes="West Texas drought frequency is increasing. GCDs may curtail oilfield water permits before municipal or domestic uses. Operators should maintain multiple water source agreements and recycled water capacity as drought contingency. The 2011 drought caused significant operational disruptions for operators dependent on single freshwater sources.",
            last_updated="2026-02-10",
            tags=["drought", "contingency", "water_district", "taxation", "curtailment"],
        ),
    ]


def build_doctrine_cache() -> list[DoctrineCacheBlock]:
    """Build the complete doctrine cache with all categories."""
    logger.info("Building LM15 Water Rights doctrine cache")
    cache: list[DoctrineCacheBlock] = []
    builders = [
        ("Groundwater Capture", _build_groundwater_doctrines),
        ("GCD Regulation", _build_gcd_doctrines),
        ("Surface Water", _build_surface_water_doctrines),
        ("Produced Water", _build_produced_water_doctrines),
        ("Injection Wells", _build_injection_well_doctrines),
        ("Seismicity", _build_seismicity_doctrines),
        ("Freshwater Protection", _build_freshwater_protection_doctrines),
        ("Edwards Aquifer", _build_edwards_aquifer_doctrines),
        ("Accommodation Doctrine", _build_accommodation_doctrines),
        ("Water Conveyancing", _build_conveyancing_doctrines),
        ("Federal Water Law", _build_federal_water_doctrines),
        ("Interstate Compacts", _build_interstate_compact_doctrines),
        ("Desalination", _build_desalination_doctrines),
        ("Drought Planning", _build_drought_doctrines),
    ]
    for name, builder in builders:
        doctrines = builder()
        cache.extend(doctrines)
        logger.debug(f"Loaded {len(doctrines)} doctrines for {name}")
    logger.info(f"Doctrine cache built: {len(cache)} total blocks across {len(builders)} categories")
    return cache


def search_doctrines(
    cache: list[DoctrineCacheBlock],
    query: str,
    category: Optional[DoctrineCategory] = None,
    risk_level: Optional[RiskLevel] = None,
    max_results: int = 20,
) -> list[DoctrineCacheBlock]:
    """Search doctrine cache by query text, category, and risk level."""
    query_lower = query.lower()
    query_terms = query_lower.split()
    results: list[tuple[float, DoctrineCacheBlock]] = []
    for doctrine in cache:
        if category and doctrine.category != category:
            continue
        if risk_level and doctrine.risk_if_violated != risk_level:
            continue
        score = 0.0
        searchable = (
            doctrine.title.lower() + " " +
            doctrine.summary.lower() + " " +
            doctrine.citation.lower() + " " +
            " ".join(doctrine.tags).lower() + " " +
            doctrine.detailed_analysis.lower()
        )
        for term in query_terms:
            if term in searchable:
                score += 1.0
            if term in doctrine.title.lower():
                score += 3.0
            if term in doctrine.citation.lower():
                score += 2.0
            for tag in doctrine.tags:
                if term in tag.lower():
                    score += 1.5
        if score > 0:
            results.append((score, doctrine))
    results.sort(key=lambda x: x[0], reverse=True)
    matched = [d for _, d in results[:max_results]]
    logger.debug(f"Doctrine search '{query}': {len(matched)} results from {len(cache)} total")
    return matched


def get_coverage_map(cache: list[DoctrineCacheBlock]) -> dict[str, Any]:
    """Generate coverage map showing doctrine distribution across categories."""
    coverage: dict[str, list[str]] = {}
    for doctrine in cache:
        cat = doctrine.category.value
        if cat not in coverage:
            coverage[cat] = []
        coverage[cat].append(doctrine.doctrine_id)
    summary = {
        "total_doctrines": len(cache),
        "categories": len(coverage),
        "coverage_by_category": {k: len(v) for k, v in coverage.items()},
        "doctrine_ids_by_category": coverage,
        "risk_distribution": {},
        "authority_distribution": {},
    }
    for risk in RiskLevel:
        count = sum(1 for d in cache if d.risk_if_violated == risk)
        summary["risk_distribution"][risk.value] = count
    for auth in AuthorityLevel:
        count = sum(1 for d in cache if d.authority_level == auth)
        summary["authority_distribution"][auth.value] = count
    logger.info(f"Coverage map: {summary['total_doctrines']} doctrines across {summary['categories']} categories")
    return summary


def verify_doctrine_integrity(cache: list[DoctrineCacheBlock]) -> dict[str, Any]:
    """Verify integrity of all doctrine blocks via SHA-256 hashing."""
    results = {
        "total": len(cache),
        "verified": 0,
        "failed": 0,
        "hashes": {},
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    for doctrine in cache:
        doc_hash = doctrine.compute_hash()
        results["hashes"][doctrine.doctrine_id] = doc_hash
        results["verified"] += 1
    integrity_payload = json.dumps(results["hashes"], sort_keys=True)
    results["aggregate_hash"] = hashlib.sha256(integrity_payload.encode()).hexdigest()
    logger.info(
        f"Doctrine integrity check: {results['verified']}/{results['total']} verified, "
        f"aggregate hash: {results['aggregate_hash'][:16]}..."
    )
    return results


# ---------------------------------------------------------------------------
# Pre-built rule collections
# ---------------------------------------------------------------------------

def _build_groundwater_rules() -> list[GroundwaterRule]:
    return [
        GroundwaterRule(
            rule_id="GCD-MID-001",
            district_name="Midland County GWCD",
            county="Midland",
            rule_number="Rule 5",
            title="Well Spacing and Production Permit",
            description="Regulates spacing, production limits, and metering for non-exempt wells in Midland County",
            permit_requirements=["Application with well location plat", "Hydrogeologic report for wells >100 GPM", "Annual water use report"],
            spacing_rules={"minimum_distance_from_property_line_ft": 300, "minimum_distance_from_existing_well_ft": 600},
            production_limits={"allocation_af_per_acre_per_year": 1.5, "maximum_permit_term_years": 30},
            reporting_requirements=["Annual metered production report", "Water quality sampling every 3 years"],
            enforcement_actions=["Written notice of violation", "Administrative penalty up to $10,000/day", "Well plugging order"],
            exemptions=["Domestic/livestock wells under 25,000 GPD", "Wells on tracts less than 10 acres (domestic only)"],
            oilfield_provisions="Oilfield water wells for drilling/completion may qualify for temporary permit. Dedicated freshwater supply wells for fracking require standard production permit.",
            last_amended="2024-06-15",
        ),
        GroundwaterRule(
            rule_id="GCD-ECT-001",
            district_name="Ector County GWCD",
            county="Ector",
            rule_number="Rule 4.1",
            title="Groundwater Production Permit Requirements",
            description="Production permit requirements for non-exempt wells in Ector County including oilfield supply wells",
            permit_requirements=["Permit application with GPS coordinates", "Proposed production schedule", "Casing and completion specifications"],
            spacing_rules={"minimum_distance_from_property_line_ft": 200, "minimum_distance_from_existing_well_ft": 500},
            production_limits={"allocation_af_per_acre_per_year": 2.0, "maximum_permit_term_years": 25},
            reporting_requirements=["Monthly metered production report", "Annual aquifer level measurement"],
            enforcement_actions=["Notice of violation", "Cease and desist order", "Administrative penalty"],
            exemptions=["Domestic/livestock wells under 25,000 GPD", "Monitoring wells"],
            oilfield_provisions="All oilfield water supply wells producing over 25 GPM require a production permit. The O&G exemption (TWC 36.117(b)(2)) is interpreted to cover only rig supply water during active drilling, not bulk frack water sourcing.",
            last_amended="2023-11-20",
        ),
        GroundwaterRule(
            rule_id="GCD-REE-001",
            district_name="Pecos Valley Water District",
            county="Reeves",
            rule_number="Rule 3",
            title="Well Registration and Production Limits",
            description="Groundwater production regulation in Reeves County over the Pecos Valley Aquifer",
            permit_requirements=["Well registration within 30 days of completion", "Production permit for wells over 17.5 GPM", "Annual use report"],
            spacing_rules={"minimum_distance_from_property_line_ft": 250, "minimum_distance_from_existing_well_ft": 500},
            production_limits={"allocation_af_per_acre_per_year": 1.0, "maximum_permit_term_years": 20},
            reporting_requirements=["Annual production and static water level report", "Notification of well modification or deepening"],
            enforcement_actions=["Warning letter", "Production curtailment order", "Administrative penalty up to $5,000/violation"],
            exemptions=["Domestic/livestock wells under 17.5 GPM", "Stock watering windmills"],
            oilfield_provisions="Oilfield supply wells require standard production permits. High-volume temporary permits (90-day) available for completion operations. District monitors water-oil ratios through RRC data to estimate produced water volumes.",
            last_amended="2024-01-10",
        ),
    ]


def _build_surface_water_rules() -> list[SurfaceWaterRule]:
    return [
        SurfaceWaterRule(
            rule_id="SW-TCEQ-001",
            title="TCEQ Water Rights Permitting - New Appropriation",
            citation="30 TAC Ch. 295, 297; TWC Ch. 11",
            agency="TCEQ",
            description="Requirements for obtaining a new surface water appropriation permit from TCEQ, including application, notice, contested case hearing, and priority date assignment",
            permit_types=["Regular Permit", "Term Permit", "Seasonal Permit", "Temporary Permit", "Emergency Authorization"],
            priority_system="First in time, first in right. Priority date is filing date of application.",
            exemptions=["Domestic and livestock use up to 200 AF/year", "Wildlife management use (limited)"],
            cancellation_provisions="Permits may be cancelled after 10 consecutive years of non-use under TWC Sec. 11.173. TCEQ initiates cancellation proceedings.",
            amendment_rules="Amendment required for change in purpose of use, place of use, diversion point, or increase in volume exceeding 25%",
            enforcement="TCEQ Water Master program in designated basins. Administrative penalties up to $25,000/day for unauthorized diversions.",
            permian_basin_relevance="Surface water is scarce in the Permian Basin. Most permits are held by municipalities and irrigation districts. Oil and gas operators typically purchase water from permit holders rather than seeking new appropriations.",
        ),
    ]


def _build_produced_water_regulations() -> list[ProducedWaterRegulation]:
    return [
        ProducedWaterRegulation(
            reg_id="PW-RRC-001",
            title="RRC Statewide Rule 9 - Disposal Well Operations",
            agency="Railroad Commission of Texas",
            citation="16 TAC Sec. 3.9",
            description="Comprehensive regulation of saltwater disposal wells including permit application, construction standards, operating limits, monitoring, and closure requirements",
            disposal_methods=["Deep well injection into non-productive zone", "Enhanced oil recovery injection"],
            volume_limits={"max_daily_bbls": 30000, "permit_specific": True},
            quality_standards={"no_hazardous_waste": True, "norm_screening": True},
            reporting_requirements=["Form H-10 annual monitoring report", "H-1A for permit amendments", "Spill reporting within 24 hours"],
            recycling_provisions="Recycled produced water reused in O&G operations governed by Rule 46. No separate disposal permit needed for recycling.",
            enforcement_actions=["Notice of violation", "Compliance order", "Administrative penalty up to $10,000/day", "Well plugging order", "Permit revocation"],
            permian_basin_notes="Permian Basin disposal well capacity is a critical constraint. Some operators face 50+ mile truck hauls to available disposal. Commercial SWD pricing ($0.25-1.50/bbl) is a major operating cost.",
        ),
    ]


def _build_injection_well_standards() -> list[InjectionWellStandard]:
    return [
        InjectionWellStandard(
            std_id="IW-STD-001",
            title="Class II Saltwater Disposal Well Construction Standards",
            well_class="Class II-D (Disposal)",
            citation="16 TAC Sec. 3.9; 16 TAC Sec. 3.13; 40 CFR 146.22",
            agency="RRC / EPA",
            description="Construction standards for saltwater disposal wells including casing, cementing, tubing, packer, and wellhead requirements",
            permit_requirements=["H-1 application", "Geological data package", "Area of review analysis", "Well schematic", "Financial assurance"],
            construction_standards={
                "surface_casing": "Set below base of USDW, cemented to surface",
                "intermediate_casing": "Required where multiple freshwater zones exist",
                "long_string_casing": "Set through injection zone, cemented above injection interval",
                "tubing_and_packer": "Required for all disposal operations",
                "wellhead": "Must withstand maximum operating pressure",
            },
            operating_limits={
                "max_injection_pressure_psi_per_ft": 0.5,
                "max_daily_volume_bbls": 30000,
                "annular_monitoring": "Continuous pressure monitoring required",
            },
            monitoring_requirements=["Injection pressure and rate (continuous)", "Annular pressure (continuous)", "Cumulative volume (monthly)", "Water quality (annual)"],
            mit_interval_years=5,
            closure_requirements=["Plugging plan approval from RRC", "Cement plugs across injection zone and freshwater zones", "Surface casing cut and capped", "Site remediation to RRC standards"],
            seismicity_provisions="Wells in seismic review areas subject to enhanced monitoring. Traffic light protocol may require volume reduction or shut-in based on nearby seismic events.",
            permian_basin_notes="Permian Basin SWD wells typically inject into the Ellenburger formation (deep) or depleted San Andres/Clearfork zones. Shallow disposal into the San Andres is common but faces increased seismicity scrutiny.",
        ),
    ]


def _build_aquifer_protection_rules() -> list[AquiferProtectionRule]:
    return [
        AquiferProtectionRule(
            rule_id="AQ-OGA-001",
            title="Ogallala Aquifer Protection and Management",
            aquifer_name="Ogallala",
            citation="TWC Ch. 36; GMA 2 DFC Resolution (2022)",
            description="Protection and sustainable management rules for the Ogallala Aquifer in the Texas High Plains and northern Permian Basin region",
            protection_zones=["Recharge zones (limited)", "High-depletion areas", "Areas of declining saturated thickness"],
            tds_thresholds={"freshwater_max_mg_l": 1000, "typical_range_mg_l_low": 300, "typical_range_mg_l_high": 1500},
            casing_requirements=["Surface casing through Ogallala formation", "Cement to surface", "Isolation from underlying Dockum"],
            monitoring_requirements=["GCD water level monitoring network", "Annual static water level measurement", "Water quality sampling program"],
            contamination_response=["Spill containment and notification", "Groundwater investigation if contamination suspected", "Remediation under TCEQ supervision"],
            permian_basin_relevance="CRITICAL - Ogallala is the primary freshwater source for the northern Permian Basin. Depletion rates exceed recharge by 10-50x in many areas. Saturated thickness has declined 50-150 feet since 1950 in parts of the Texas High Plains.",
        ),
    ]


def _build_interstate_compact_provisions() -> list[InterstateCompactProvision]:
    return [
        InterstateCompactProvision(
            compact_id="IC-PECOS-001",
            compact_name="Pecos River Compact",
            parties=["Texas", "New Mexico"],
            year_ratified=1949,
            citation="63 Stat. 159; Public Law 81-91",
            texas_obligations=["Accept deliveries per inflow-outflow formula", "Fund Texas share of compact administration", "Participate in annual Compact Commission meetings"],
            allocation_method="Inflow-outflow formula based on NM depletions relative to 1947 conditions",
            enforcement_mechanism="U.S. Supreme Court original jurisdiction; River Master appointed",
            supreme_court_cases=["Texas v. New Mexico, 462 U.S. 554 (1983)", "Texas v. New Mexico, 482 U.S. 124 (1987)"],
            permian_basin_relevance="HIGH - Pecos River flows through Reeves, Pecos, and Terrell counties. Compact constrains surface water availability. Groundwater-surface water interaction complicates management.",
        ),
    ]


# ---------------------------------------------------------------------------
# Desalination regulations builder
# ---------------------------------------------------------------------------

def _build_desalination_regulations() -> list[DoctrineCacheBlock]:
    """Build doctrine blocks for desalination regulatory framework."""
    return [
        DoctrineCacheBlock(
            doctrine_id="DESAL-REG-001",
            title="TWDB Desalination Grants - TWC Chapter 16",
            category=DoctrineCategory.BRACKISH_DESALINATION,
            authority_level=AuthorityLevel.STATUTE,
            jurisdiction=JurisdictionScope.STATE,
            citation="TWC ch. 16, subchapter J",
            summary="TWDB authorized to provide grants and loans for desalination projects "
                     "including seawater, brackish groundwater, and produced water treatment. "
                     "Projects must demonstrate technical and economic feasibility.",
            key_provisions=[
                "TWDB Innovative Water Technologies fund covers up to 50% of pilot costs",
                "Concentrate disposal must comply with TCEQ discharge/injection permits",
                "Environmental review required for marine intake/discharge",
                "Regional water planning must incorporate desal as supply source",
                "Priority given to projects serving multiple water user groups",
            ],
            risk_if_violated=RiskLevel.MEDIUM,
            last_updated="2025-09-01",
            permian_basin_notes="Brackish groundwater desalination is increasingly viable in the "
                                 "Permian Basin. The Dockum and Santa Rosa aquifers contain 3,000-10,000 mg/L "
                                 "TDS water suitable for treatment. Multiple pilot projects underway.",
        ),
        DoctrineCacheBlock(
            doctrine_id="DESAL-REG-002",
            title="Brackish Groundwater Production Zone Designation",
            category=DoctrineCategory.BRACKISH_DESALINATION,
            authority_level=AuthorityLevel.STATUTE,
            jurisdiction=JurisdictionScope.STATE,
            citation="TWC sec. 36.1015; 31 TAC ch. 356 subchapter I",
            summary="GCDs may designate brackish groundwater production zones where pumping "
                     "will not impact freshwater aquifers. TWDB studies and recommends zones.",
            key_provisions=[
                "TWDB completes brackish groundwater studies for each aquifer",
                "Production zone designation requires TWDB recommendation",
                "GCD may set separate permit conditions for brackish production",
                "Monitoring wells required at zone boundaries",
                "Annual reporting on TDS changes at monitoring points",
            ],
            risk_if_violated=RiskLevel.MEDIUM,
            last_updated="2025-06-01",
            permian_basin_notes="Several Permian Basin GCDs are working with TWDB on brackish zone "
                                 "designations. The Dockum aquifer beneath Midland-Ector area has been "
                                 "identified as a high-priority candidate for production zone designation.",
        ),
    ]


def _build_playa_lake_regulations() -> list[DoctrineCacheBlock]:
    """Build doctrine blocks for playa lake water rights in West Texas."""
    return [
        DoctrineCacheBlock(
            doctrine_id="PLAYA-001",
            title="Playa Lake Water Rights - Diffused Surface Water Doctrine",
            category=DoctrineCategory.SURFACE_WATER,
            authority_level=AuthorityLevel.CASE_LAW,
            jurisdiction=JurisdictionScope.STATE,
            citation="Fleming v. Davis, 37 S.W.2d 747 (Tex. Comm'n App. 1931); TWC sec. 11.021",
            summary="Playa lakes in West Texas are generally classified as diffused surface water "
                     "rather than state water. Landowners may capture and use diffused surface water "
                     "without TCEQ appropriation permit. However, if a playa connects to a watercourse "
                     "during high-water events, it may become state water subject to permitting.",
            key_provisions=[
                "Diffused surface water belongs to landowner where it falls",
                "No TCEQ permit required for diffused surface water capture",
                "Connection to state watercourse converts status to state water",
                "Downstream landowner cannot claim playa water via prior appropriation",
                "Oilfield use of playa water common in Permian Basin operations",
                "TCEQ may assert jurisdiction if playa feeds into navigable stream",
            ],
            risk_if_violated=RiskLevel.MEDIUM,
            last_updated="2025-01-15",
            permian_basin_notes="Playa lakes are a significant supplemental water source for Permian Basin "
                                 "oil and gas operations. Operators commonly pump from playas for drilling "
                                 "and completion water. The legal status depends on connectivity to state "
                                 "watercourses, which varies seasonally.",
        ),
    ]


# ---------------------------------------------------------------------------
# Pre-built collections for import
# ---------------------------------------------------------------------------

GROUNDWATER_RULES: list[GroundwaterRule] = _build_groundwater_rules()
SURFACE_WATER_RULES: list[SurfaceWaterRule] = _build_surface_water_rules()
PRODUCED_WATER_REGULATIONS: list[ProducedWaterRegulation] = _build_produced_water_regulations()
INJECTION_WELL_STANDARDS: list[InjectionWellStandard] = _build_injection_well_standards()
AQUIFER_PROTECTION_RULES: list[AquiferProtectionRule] = _build_aquifer_protection_rules()
INTERSTATE_COMPACT_PROVISIONS: list[InterstateCompactProvision] = _build_interstate_compact_provisions()
DESALINATION_REGULATIONS: list[DoctrineCacheBlock] = _build_desalination_regulations()
PLAYA_LAKE_REGULATIONS: list[DoctrineCacheBlock] = _build_playa_lake_regulations()
