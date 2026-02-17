"""
LM15 Water Rights Engine - Semantic Dictionary
================================================

Water rights terminology covering groundwater, surface water, produced water,
injection wells, aquifers, permits, compliance, and oilfield water operations.

700+ terms with definitions, synonyms, abbreviations, and regulatory references.

Author: ECHO OMEGA PRIME Build System
Engine: LM15 v2.0.0
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

from loguru import logger


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TermCategory(str, Enum):
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
    DESALINATION = "desalination"
    CONVEYANCING = "conveyancing"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class SemanticTerm:
    term: str
    category: TermCategory
    definition: str
    abbreviation: Optional[str] = None
    synonyms: list[str] = field(default_factory=list)
    related_terms: list[str] = field(default_factory=list)
    context_notes: str = ""
    unit: Optional[str] = None
    regulatory_reference: Optional[str] = None


# ---------------------------------------------------------------------------
# Term builders by category
# ---------------------------------------------------------------------------

def _build_groundwater_terms() -> list[SemanticTerm]:
    return [
        SemanticTerm("Rule of Capture", TermCategory.GROUNDWATER, "Common-law doctrine holding that a landowner may pump groundwater beneath their property without liability to neighboring landowners whose wells are affected, absent malice or willful waste.", None, ["absolute ownership doctrine", "English rule", "East doctrine"], ["groundwater ownership", "vested property right"], "Texas adopted the rule of capture in Houston & T.C. Ry. v. East (1904). Modified by GCD regulation and EAA v. Day.", regulatory_reference="H&TC Ry. v. East, 98 Tex. 146 (1904)"),
        SemanticTerm("Percolating Groundwater", TermCategory.GROUNDWATER, "Water that filters through the ground beneath the surface without a defined channel. Distinguished from underground streams which follow a defined course.", None, ["diffused groundwater", "percolating water"], ["aquifer", "water table", "saturated zone"], "Texas law applies the rule of capture to percolating groundwater but not to underground streams.", regulatory_reference="TWC Sec. 36.001"),
        SemanticTerm("Groundwater Ownership in Place", TermCategory.GROUNDWATER, "The legal doctrine that a surface owner has a vested, constitutionally-protected property right in groundwater beneath their land, analogous to oil and gas ownership.", None, ["ownership-in-place theory"], ["rule of capture", "severance", "water rights conveyance"], "Confirmed by Texas Supreme Court in EAA v. Day (2012).", regulatory_reference="EAA v. Day, 369 S.W.3d 814 (Tex. 2012)"),
        SemanticTerm("Artesian Well", TermCategory.GROUNDWATER, "A well drilled into a confined aquifer where water pressure causes the water level to rise above the top of the aquifer, and in some cases above the land surface (flowing artesian well).", None, ["flowing well", "artesian spring"], ["confined aquifer", "hydrostatic pressure"], "Allowing an artesian well to flow without beneficial use may constitute waste under Texas law."),
        SemanticTerm("Water Table", TermCategory.GROUNDWATER, "The upper surface of the zone of saturation in an unconfined aquifer, where water pressure equals atmospheric pressure.", None, ["phreatic surface", "groundwater level"], ["aquifer", "saturated zone", "vadose zone"], "Water table depth determines well depth requirements and pumping costs.", unit="feet below ground surface"),
        SemanticTerm("Static Water Level", TermCategory.GROUNDWATER, "The level at which water stands in a well when the pump is not operating and the water level has stabilized.", abbreviation="SWL", synonyms=["resting water level"], related_terms=["pumping water level", "drawdown", "water table"], context_notes="Measured in feet below ground surface or elevation. GCDs require annual SWL measurements.", unit="ft BGL"),
        SemanticTerm("Drawdown", TermCategory.GROUNDWATER, "The difference between the static water level and the pumping water level in a well during operation.", None, ["cone of depression depth"], ["pumping rate", "specific capacity", "aquifer transmissivity"], "Excessive drawdown indicates aquifer depletion or well interference.", unit="feet"),
        SemanticTerm("Cone of Depression", TermCategory.GROUNDWATER, "The cone-shaped lowering of the water table around a pumping well, extending outward until the drawdown becomes negligible.", None, ["drawdown cone", "area of influence"], ["drawdown", "well spacing", "aquifer interference"], "The size of the cone determines minimum well spacing requirements in GCD rules."),
        SemanticTerm("Specific Yield", TermCategory.GROUNDWATER, "The ratio of the volume of water an aquifer releases from storage by gravity drainage to the total volume of aquifer material.", abbreviation="Sy", synonyms=["drainable porosity"], related_terms=["storativity", "porosity", "specific retention"], context_notes="Typical values: sand 0.15-0.30, gravel 0.20-0.35, sandstone 0.05-0.20.", unit="dimensionless"),
        SemanticTerm("Transmissivity", TermCategory.GROUNDWATER, "The rate at which water is transmitted through a unit width of aquifer under a unit hydraulic gradient. Product of hydraulic conductivity and saturated thickness.", abbreviation="T", synonyms=["coefficient of transmissibility"], related_terms=["hydraulic conductivity", "saturated thickness"], context_notes="Key parameter for well yield prediction and GCD allocation.", unit="gpd/ft or ft2/day"),
        SemanticTerm("Recharge", TermCategory.GROUNDWATER, "The process by which water enters an aquifer, typically from precipitation infiltrating through the soil or from surface water bodies.", None, ["aquifer recharge", "replenishment"], ["recharge zone", "infiltration", "water budget"], "Ogallala recharge rate (0.5 in/yr) is far below pumping rates in the Permian Basin.", unit="inches/year or AF/year"),
        SemanticTerm("Conjunctive Use", TermCategory.GROUNDWATER, "The coordinated management and use of both surface water and groundwater to maximize water supply reliability and minimize environmental impacts.", None, ["integrated water management"], ["aquifer storage and recovery", "managed aquifer recharge"], "Texas encourages conjunctive use through regional water planning process."),
    ]


def _build_surface_water_terms() -> list[SemanticTerm]:
    return [
        SemanticTerm("Prior Appropriation", TermCategory.SURFACE_WATER, "The system of surface water rights allocation used in Texas since 1913: first in time, first in right. Senior appropriators have priority over junior appropriators during shortages.", None, ["first in time first in right", "appropriation doctrine"], ["water permit", "priority date", "senior right"], "Texas replaced riparian rights with prior appropriation for surface water in 1913.", regulatory_reference="TWC Ch. 11"),
        SemanticTerm("Appropriation Permit", TermCategory.SURFACE_WATER, "A permit issued by TCEQ authorizing the diversion, storage, or use of a specific quantity of state surface water for a specified beneficial purpose.", None, ["water right permit", "water rights certificate"], ["priority date", "diversion point", "place of use"], "New appropriation permits are increasingly difficult to obtain due to fully-appropriated basins.", regulatory_reference="TWC Sec. 11.121"),
        SemanticTerm("Priority Date", TermCategory.SURFACE_WATER, "The date that establishes the seniority of a surface water right. For post-1913 permits, it is the date the application was filed with TCEQ (or predecessor agency).", None, ["seniority date"], ["prior appropriation", "junior right", "senior right"], "During shortages, junior rights are curtailed before senior rights."),
        SemanticTerm("Beneficial Use", TermCategory.SURFACE_WATER, "The use of water for a purpose recognized as beneficial by law, including domestic, municipal, agricultural, industrial, mining, oil and gas, and environmental purposes.", None, ["beneficial purpose"], ["appropriation permit", "waste"], "Oil and gas operations constitute a recognized beneficial use of water in Texas.", regulatory_reference="TWC Sec. 11.002(5)"),
        SemanticTerm("Bed and Banks", TermCategory.SURFACE_WATER, "The natural channel of a river or stream through which water flows. Use of bed and banks as a conveyance for water requires TCEQ authorization.", None, ["stream channel", "watercourse"], ["bed and banks authorization", "system losses"], "Authorization required to transport water through state watercourse.", regulatory_reference="TWC Sec. 11.042"),
        SemanticTerm("Watermaster", TermCategory.SURFACE_WATER, "A TCEQ-appointed official responsible for administering water rights in a designated river basin, including monitoring diversions, enforcing priority calls, and managing shortages.", None, ["water master"], ["priority administration", "shortage allocation"], "Active watermaster programs in South Texas, Concho River, and Rio Grande.", regulatory_reference="TWC Sec. 11.326"),
        SemanticTerm("Return Flow", TermCategory.SURFACE_WATER, "Water that returns to a surface watercourse after use, such as treated wastewater effluent, irrigation tailwater, or cooling water discharge.", None, ["return water"], ["bed and banks", "system losses", "TPDES"], "Return flows may be appropriated by downstream users unless the discharger retains rights."),
        SemanticTerm("Environmental Flow", TermCategory.SURFACE_WATER, "The quantity, timing, and quality of water flows required to sustain freshwater and estuarine ecosystems and the ecological services they provide.", None, ["instream flow", "ecological flow"], ["SB 3", "flow regime", "subsistence flow"], "Texas requires environmental flow conditions in new water rights permits under SB 3.", regulatory_reference="TWC Sec. 11.1471"),
        SemanticTerm("Diffused Surface Water", TermCategory.SURFACE_WATER, "Water from rainfall or snowmelt that flows across land in a diffuse manner without being confined to a defined channel. Not subject to TCEQ appropriation permitting.", None, ["sheet flow", "overland flow"], ["stormwater", "surface runoff"], "Landowners generally may capture diffused surface water without permit. Distinction from defined watercourse is fact-specific."),
    ]


def _build_produced_water_terms() -> list[SemanticTerm]:
    return [
        SemanticTerm("Produced Water", TermCategory.PRODUCED_WATER, "Water that comes to the surface during oil and gas production, including formation water, injected water, and condensation. Typically highly saline with dissolved minerals, hydrocarbons, and naturally occurring radioactive material.", None, ["formation water", "brine"], ["disposal well", "saltwater disposal", "water-oil ratio"], "Permian Basin produced water TDS typically 150,000-300,000 mg/L.", unit="barrels/day"),
        SemanticTerm("Water-Oil Ratio", TermCategory.PRODUCED_WATER, "The ratio of produced water volume to oil production volume. Increases as a reservoir matures.", abbreviation="WOR", synonyms=["water cut"], related_terms=["produced water", "reservoir depletion"], context_notes="Permian Basin WOR ranges from 3:1 (new wells) to 10:1+ (mature wells).", unit="bbls water/bbl oil"),
        SemanticTerm("Flowback Water", TermCategory.PRODUCED_WATER, "Water that returns to the surface from a hydraulically fractured well during the initial production phase, consisting of a mixture of fracking fluid and formation water.", None, ["frac flowback", "completion flowback"], ["produced water", "hydraulic fracturing", "frack fluid"], "Flowback typically occurs in first 2-4 weeks after completion. Volume is 10-30% of injected fluid."),
        SemanticTerm("Saltwater Disposal", TermCategory.PRODUCED_WATER, "The injection of produced water (saltwater) into a subsurface formation for permanent disposal, through a permitted Class II injection well.", abbreviation="SWD", synonyms=["produced water disposal", "brine disposal"], related_terms=["H-1 permit", "injection well", "disposal zone"], context_notes="SWD is the dominant produced water disposal method in the Permian Basin.", regulatory_reference="16 TAC Sec. 3.9"),
        SemanticTerm("Commercial Disposal Well", TermCategory.PRODUCED_WATER, "A saltwater disposal well operated by a third-party company that accepts produced water from multiple operators for a fee.", None, ["commercial SWD", "third-party disposal"], ["disposal fee", "gathering system"], "Commercial SWD fees in the Permian range $0.25-1.50/bbl depending on location and volume.", unit="$/bbl"),
        SemanticTerm("NORM", TermCategory.PRODUCED_WATER, "Naturally Occurring Radioactive Material. Radioactive elements (radium-226, radium-228) present in produced water and scale deposits. Subject to RRC and TCEQ regulation.", abbreviation="NORM", synonyms=["naturally occurring radioactive material"], related_terms=["produced water", "scale", "radioactive waste"], context_notes="Screening required before surface discharge or beneficial reuse. Limit: 30 pCi/L.", unit="picocuries/liter", regulatory_reference="16 TAC Sec. 3.98; 30 TAC Ch. 336"),
        SemanticTerm("Produced Water Recycling", TermCategory.PRODUCED_WATER, "Treatment and reuse of produced water for oil and gas operations, typically as base fluid for hydraulic fracturing.", None, ["water recycling", "produced water reuse"], ["treatment facility", "frack fluid", "HB 2771"], "HB 2771 (2019) clarified that recycled produced water used in O&G stays under RRC jurisdiction.", regulatory_reference="16 TAC Sec. 3.46; HB 2771"),
        SemanticTerm("Beneficial Reuse", TermCategory.PRODUCED_WATER, "Use of treated produced water for purposes outside oil and gas operations, such as agriculture, industrial cooling, or dust suppression. Requires TCEQ authorization.", None, ["alternative reuse"], ["water quality standards", "treatment", "TCEQ permit"], "Beneficial reuse outside O&G requires meeting receiving-use quality standards."),
    ]


def _build_injection_well_terms() -> list[SemanticTerm]:
    return [
        SemanticTerm("Class II Injection Well", TermCategory.INJECTION_WELL, "A well used to inject fluids associated with oil and gas production. Includes disposal wells (II-D) and enhanced recovery wells (II-R).", None, ["UIC Class II", "oil and gas injection well"], ["H-1 permit", "UIC program", "SDWA"], "Texas has primacy for Class II wells through the Railroad Commission.", regulatory_reference="40 CFR Part 146 Subpart C; 16 TAC Sec. 3.9"),
        SemanticTerm("H-1 Permit", TermCategory.INJECTION_WELL, "The RRC application form and resulting permit for authorization to dispose of oil and gas waste by injection into a formation not productive of oil or gas.", None, ["Form H-1", "disposal well permit"], ["Class II", "area of review", "injection zone"], "Required for all new SWD wells. Application includes geological data, well schematic, and area of review.", regulatory_reference="16 TAC Sec. 3.9"),
        SemanticTerm("Mechanical Integrity Test", TermCategory.INJECTION_WELL, "A test to demonstrate that an injection well has no significant leak in the casing, tubing, or packer (Part 1) and no significant fluid movement through vertical channels adjacent to the wellbore (Part 2).", abbreviation="MIT", synonyms=["pressure test", "integrity test"], related_terms=["casing integrity", "annular pressure", "tracer survey"], context_notes="Required at least every 5 years. Failed MIT requires immediate well shutdown.", regulatory_reference="16 TAC Sec. 3.9(7); 40 CFR 146.8"),
        SemanticTerm("Area of Review", TermCategory.INJECTION_WELL, "The geographic area surrounding an injection well within which all wells that penetrate the injection zone or confining zone must be identified and evaluated for potential conduits of fluid migration.", abbreviation="AOR", synonyms=["zone of review"], related_terms=["H-1 permit", "wellbore communication", "confining zone"], context_notes="Standard AOR radius is 1/4 mile from the injection wellbore.", regulatory_reference="16 TAC Sec. 3.9; 40 CFR 146.6"),
        SemanticTerm("Injection Zone", TermCategory.INJECTION_WELL, "The subsurface formation or formations into which fluids are injected through an injection well.", None, ["disposal zone", "receiving formation", "target zone"], ["confining zone", "USDW", "porosity"], "Must be separated from USDWs by adequate confining zones. Common Permian Basin zones: Ellenburger, San Andres."),
        SemanticTerm("Confining Zone", TermCategory.INJECTION_WELL, "A low-permeability geological formation that overlies and/or underlies the injection zone and acts as a barrier to vertical fluid migration.", None, ["confining bed", "seal", "caprock"], ["injection zone", "USDW protection", "shale"], "Integrity of confining zones is critical for USDW protection."),
        SemanticTerm("Maximum Allowable Injection Pressure", TermCategory.INJECTION_WELL, "The highest pressure at the wellhead at which fluids may be injected, typically calculated as 0.5 psi per foot of depth to prevent fracturing the confining zone.", abbreviation="MAIP", synonyms=["max injection pressure"], related_terms=["fracture gradient", "injection zone depth"], context_notes="Exceeding MAIP is a permit violation and may indicate formation fracturing.", unit="psi", regulatory_reference="16 TAC Sec. 3.9"),
        SemanticTerm("Annular Pressure", TermCategory.INJECTION_WELL, "The pressure in the annular space between the tubing and casing of an injection well. Used to monitor well integrity during operations.", None, ["casing-tubing annulus pressure"], ["mechanical integrity", "wellbore integrity", "leak detection"], "Continuous annular pressure monitoring is required for all disposal wells. Sudden changes indicate potential leak.", unit="psi"),
    ]


def _build_aquifer_terms() -> list[SemanticTerm]:
    return [
        SemanticTerm("Ogallala Aquifer", TermCategory.AQUIFER, "A major unconfined aquifer underlying the Texas High Plains and northern Permian Basin. Primary freshwater source for irrigation and municipal supply. Critically depleted in many areas.", None, ["High Plains Aquifer", "Ogallala Formation"], ["saturated thickness", "depletion", "recharge"], "Recharge rate (~0.5 in/yr) far below pumping rates. Saturated thickness declining 1-3 ft/yr in heavily pumped areas."),
        SemanticTerm("Edwards-Trinity Aquifer", TermCategory.AQUIFER, "A major aquifer system in central-west Texas composed of Cretaceous-age Edwards and Trinity group formations. Partially confined.", None, ["Edwards-Trinity Plateau Aquifer"], ["karst", "springflow", "recharge zone"], "Important water source for Crockett, Sutton, Val Verde counties. Karst features create preferential flow paths."),
        SemanticTerm("Pecos Valley Aquifer", TermCategory.AQUIFER, "An unconfined alluvial aquifer in the Pecos River valley of Trans-Pecos Texas (Reeves, Ward, Pecos counties). Critical for irrigation and oilfield supply.", None, ["Cenozoic Pecos Alluvium"], ["Pecos River", "alluvial", "irrigation"], "High relevance for Permian Basin operations in Reeves and Pecos counties. Water quality varies (TDS 500-5,000 mg/L)."),
        SemanticTerm("Dockum Aquifer", TermCategory.AQUIFER, "A confined aquifer of Triassic age underlying much of West Texas and eastern New Mexico. Brackish to saline water quality limits use.", None, ["Dockum Group"], ["brackish", "confined aquifer", "Triassic"], "TDS typically 1,000-10,000 mg/L. Potential source for oilfield use without desalination if TDS acceptable for fracking."),
        SemanticTerm("Underground Source of Drinking Water", TermCategory.AQUIFER, "Any aquifer that currently supplies or could supply a public water system, containing water with TDS less than 10,000 mg/L, unless exempted by EPA.", abbreviation="USDW", synonyms=["drinking water aquifer"], related_terms=["SDWA", "TDS threshold", "aquifer exemption"], context_notes="All injection wells must protect USDWs. TCEQ determines the base of usable quality water for each well location.", regulatory_reference="40 CFR 144.3"),
        SemanticTerm("Aquifer Exemption", TermCategory.AQUIFER, "An EPA determination that a specific aquifer or portion thereof does not serve as a source of drinking water and may be used for injection, even though TDS is below 10,000 mg/L.", None, ["aquifer exemption petition"], ["USDW", "injection zone", "EPA approval"], "Requires demonstration that the aquifer does not and will not serve as a drinking water source. EPA Region 6 reviews.", regulatory_reference="40 CFR 146.4"),
        SemanticTerm("Saturated Thickness", TermCategory.AQUIFER, "The vertical distance between the water table and the base of the aquifer in an unconfined aquifer. Key indicator of available water supply.", None, ["saturated section"], ["aquifer storage", "well yield", "depletion"], "Ogallala saturated thickness has declined from 200+ ft to <50 ft in parts of the Texas High Plains.", unit="feet"),
    ]


def _build_permit_terms() -> list[SemanticTerm]:
    return [
        SemanticTerm("GCD Production Permit", TermCategory.PERMIT, "A permit issued by a Groundwater Conservation District authorizing production of groundwater from a non-exempt well, subject to spacing, volume, and reporting conditions.", None, ["groundwater permit", "well permit", "production authorization"], ["GCD", "allocation", "metering"], "Required for all non-exempt wells in GCD boundaries. Permit terms typically 10-30 years.", regulatory_reference="TWC Sec. 36.113"),
        SemanticTerm("TPDES Permit", TermCategory.PERMIT, "Texas Pollutant Discharge Elimination System permit issued by TCEQ for discharges of pollutants to waters of the state, including treated produced water effluent.", abbreviation="TPDES", synonyms=["discharge permit", "NPDES state equivalent"], related_terms=["Clean Water Act", "effluent limits", "surface discharge"], context_notes="Texas has NPDES delegation from EPA. Individual or general permits available.", regulatory_reference="TWC Ch. 26; 30 TAC Ch. 305"),
        SemanticTerm("Section 404 Permit", TermCategory.PERMIT, "A permit from the Army Corps of Engineers for discharge of dredged or fill material into waters of the United States, including wetlands.", None, ["Corps permit", "wetland permit", "404 permit"], ["WOTUS", "mitigation", "jurisdictional determination"], "Required for pipeline crossings, road construction, and facility development in wetlands/waters.", regulatory_reference="33 U.S.C. Sec. 1344"),
        SemanticTerm("Temporary Water Use Permit", TermCategory.PERMIT, "A short-term authorization (typically 90-180 days) for temporary use of water, such as during well drilling, completion, or construction activities.", None, ["temporary permit", "short-term authorization"], ["drilling water", "completion water", "GCD"], "Some GCDs issue 90-day temporary permits for oilfield completion water needs."),
    ]


def _build_compliance_terms() -> list[SemanticTerm]:
    return [
        SemanticTerm("Traffic Light Protocol", TermCategory.COMPLIANCE, "A seismicity response framework using color-coded levels (Green, Yellow, Orange, Red) to trigger escalating operational restrictions on disposal wells based on earthquake magnitude and proximity.", None, ["seismicity response protocol", "TLP"], ["induced seismicity", "magnitude threshold", "volume reduction"], "RRC applies this protocol to disposal wells near seismic events.", regulatory_reference="RRC Seismicity Response Protocol (2014)"),
        SemanticTerm("Spill Notification", TermCategory.COMPLIANCE, "The mandatory reporting of oil, produced water, or other oilfield fluid releases to the RRC and/or TCEQ within specified timeframes.", None, ["spill report", "release notification"], ["Rule 8", "cleanup", "remediation"], "RRC requires notification within 24 hours for crude oil releases over 5 bbls or any release reaching water.", regulatory_reference="16 TAC Sec. 3.8"),
        SemanticTerm("Desired Future Condition", TermCategory.COMPLIANCE, "The quantitative description of the desired condition of groundwater resources in a GMA at a specified future time (typically 50 years), adopted by GCDs through joint planning.", abbreviation="DFC", synonyms=["desired future conditions"], related_terms=["MAG", "GMA", "aquifer sustainability"], context_notes="DFCs drive GCD permitting decisions. Must be adopted every 5 years.", regulatory_reference="TWC Sec. 36.108"),
        SemanticTerm("Managed Available Groundwater", TermCategory.COMPLIANCE, "The amount of groundwater that may be permitted by a GCD based on the DFCs adopted by the GMA and modeled by TWDB.", abbreviation="MAG", synonyms=["modeled available groundwater"], related_terms=["DFC", "GCD allocation", "sustainability"], context_notes="MAG is the total volume a GCD can permit. Individual permits must fit within MAG.", unit="AF/year", regulatory_reference="TWC Sec. 36.1132"),
    ]


def _build_oilfield_terms() -> list[SemanticTerm]:
    return [
        SemanticTerm("Hydraulic Fracturing", TermCategory.OILFIELD, "The process of injecting fluid (water, sand, and chemicals) at high pressure into a wellbore to fracture reservoir rock and enhance oil and gas recovery.", None, ["fracking", "frac", "fracing", "frac job"], ["completion", "proppant", "frac fluid", "water sourcing"], "Typical Permian Basin frac uses 300,000-500,000 bbls of water per well.", unit="barrels of fluid"),
        SemanticTerm("Frac Fluid", TermCategory.OILFIELD, "The fluid mixture pumped during hydraulic fracturing, consisting primarily of water (90-95%), proppant/sand (4-9%), and chemical additives (0.5-1%).", None, ["fracturing fluid", "fracking fluid"], ["hydraulic fracturing", "slickwater", "gel frac"], "Increasing use of recycled produced water as base fluid reduces freshwater demand."),
        SemanticTerm("Proppant", TermCategory.OILFIELD, "Granular material (sand, ceramic beads, or resin-coated sand) pumped into hydraulic fractures to hold them open after pumping pressure is released.", None, ["frac sand", "propping agent"], ["hydraulic fracturing", "fracture conductivity"], "Typical Permian Basin well uses 10-20 million pounds of proppant."),
        SemanticTerm("Surface Use Agreement", TermCategory.OILFIELD, "A contract between the surface owner and mineral lessee/operator addressing use of the surface estate for oil and gas operations, including water use, road construction, and site restoration.", abbreviation="SUA", synonyms=["surface damage agreement", "surface waiver"], related_terms=["accommodation doctrine", "surface damages", "water allocation"], context_notes="Should specifically address water sourcing, produced water handling, and water-related surface restoration."),
        SemanticTerm("Water Midstream", TermCategory.OILFIELD, "The segment of the oil and gas value chain that handles gathering, transport, disposal, and recycling of produced water and supply of freshwater for operations.", None, ["water infrastructure", "produced water gathering"], ["pipeline gathering", "SWD", "recycling facility"], "Water midstream is a growing business segment in the Permian Basin with major investments by NGL, Solaris, WaterBridge."),
    ]


def _build_desalination_terms() -> list[SemanticTerm]:
    return [
        SemanticTerm("Desalination", TermCategory.DESALINATION, "The process of removing dissolved salts and minerals from water to produce water suitable for human consumption, irrigation, or industrial use.", None, ["desal", "desalinization"], ["reverse osmosis", "brackish water", "concentrate"], "Energy cost: 4-12 kWh per 1,000 gallons depending on feedwater TDS.", unit="kWh/1000 gal"),
        SemanticTerm("Reverse Osmosis", TermCategory.DESALINATION, "A desalination process that uses semi-permeable membranes to separate dissolved salts from water by applying pressure exceeding the osmotic pressure.", abbreviation="RO", synonyms=["membrane desalination"], related_terms=["desalination", "concentrate", "permeate"], context_notes="Most common technology for brackish water desalination in Texas. Recovery rates 75-90% for brackish, 40-50% for seawater."),
        SemanticTerm("Concentrate", TermCategory.DESALINATION, "The high-salinity waste stream produced during desalination, containing the removed salts at 3-10x the feedwater concentration.", None, ["brine", "reject", "retentate"], ["desalination", "deep well injection", "zero liquid discharge"], "Concentrate disposal is the primary regulatory and economic challenge for inland desalination."),
        SemanticTerm("Brackish Groundwater Production Zone", TermCategory.DESALINATION, "A TWDB-designated zone where brackish groundwater (TDS 1,000-10,000 mg/L) may be produced with reduced regulatory burden for desalination or direct industrial use.", None, ["BGPZ", "brackish zone"], ["TWDB", "desalination", "GCD permit"], "TWDB has designated zones in Pecos Valley, Dockum, Gulf Coast, and other aquifers.", regulatory_reference="TWC Sec. 16.060"),
    ]


def _build_conveyancing_terms() -> list[SemanticTerm]:
    return [
        SemanticTerm("Water Rights Severance", TermCategory.CONVEYANCING, "The legal separation of groundwater rights from the surface estate, creating a distinct property interest that can be independently owned, leased, or encumbered.", None, ["water rights conveyance", "water rights transfer"], ["mineral severance", "groundwater ownership", "deed"], "Authorized by TWC Sec. 36.002(d-1) and confirmed in EAA v. Day.", regulatory_reference="TWC Sec. 36.002(d-1)"),
        SemanticTerm("Water Supply Agreement", TermCategory.CONVEYANCING, "A contract for the sale, purchase, or lease of water for a specified term, volume, and price, commonly used between oil and gas operators and water suppliers.", None, ["water purchase agreement", "water lease"], ["water sourcing", "take-or-pay", "force majeure"], "Should address drought curtailment, water quality specifications, and term/renewal."),
        SemanticTerm("Water Rights Deed", TermCategory.CONVEYANCING, "A deed conveying groundwater rights as a separate estate, similar to a mineral deed. Must describe the rights conveyed, the land to which they appertain, and any reservations.", None, ["groundwater deed", "water deed"], ["severance", "reservation", "conveyance"], "Should specify aquifer, volume limits, and surface access rights."),
        SemanticTerm("Water Rights Title Examination", TermCategory.CONVEYANCING, "The review of deed records, GCD records, TCEQ permits, and TWDB data to establish the chain of title and current ownership of water rights.", None, ["water title search", "water rights chain of title"], ["title opinion", "deed records", "GCD records"], "Water rights title examination should be conducted as part of any mineral title opinion involving water-intensive operations."),
        SemanticTerm("Export Permit", TermCategory.CONVEYANCING, "A GCD permit authorizing the transport and use of groundwater outside the district boundaries, subject to TWC Sec. 36.122 anti-discrimination provisions.", None, ["groundwater export authorization"], ["GCD permit", "water transport", "interbasin transfer"], "TWC 36.122 prohibits GCDs from imposing more restrictive conditions on exports than in-district use.", regulatory_reference="TWC Sec. 36.122"),
    ]


def _build_water_quality_terms() -> list[SemanticTerm]:
    return [
        SemanticTerm("Total Dissolved Solids", TermCategory.WATER_QUALITY, "The combined content of all inorganic and organic substances dissolved in water, measured in milligrams per liter. Primary indicator of water salinity and suitability for various uses.", abbreviation="TDS", synonyms=["dissolved solids", "salinity"], related_terms=["water quality", "USDW", "brackish"], context_notes="Fresh < 1,000 mg/L; Brackish 1,000-10,000; Saline 10,000-35,000; Brine > 35,000.", unit="mg/L"),
        SemanticTerm("Chloride", TermCategory.WATER_QUALITY, "A dissolved anion commonly present in produced water and groundwater. High concentrations indicate salinity. TPDES discharge limit for surface water is typically 250 mg/L.", None, ["Cl-"], ["TDS", "salinity", "produced water"], "Major contributor to TDS in produced water. Permian Basin produced water chloride concentrations typically 50,000-150,000 mg/L.", unit="mg/L"),
        SemanticTerm("Oil and Grease", TermCategory.WATER_QUALITY, "Measurement of petroleum hydrocarbons and other organic compounds extractable from water by a solvent. Key parameter for produced water discharge compliance.", abbreviation="O&G", synonyms=["petroleum hydrocarbons"], related_terms=["produced water", "discharge permit", "TPDES"], context_notes="TPDES discharge limit typically 15 mg/L. Must be removed before any surface discharge.", unit="mg/L"),
        SemanticTerm("pH", TermCategory.WATER_QUALITY, "A measure of the acidity or alkalinity of water on a scale of 0-14, with 7 being neutral. Regulated parameter for water discharges.", None, ["hydrogen ion concentration", "acidity"], ["water quality", "discharge limits", "produced water"], "TPDES discharge limits typically 6.0-9.0. Produced water pH varies widely.", unit="standard units"),
        SemanticTerm("Benzene", TermCategory.WATER_QUALITY, "A volatile organic compound (VOC) present in crude oil and produced water. Regulated as a carcinogen with strict discharge limits.", None, ["BTEX component"], ["VOC", "produced water", "groundwater contamination"], "MCL for drinking water: 5 ug/L (0.005 mg/L). Common in Permian Basin produced water.", unit="mg/L"),
        SemanticTerm("Hydrogen Sulfide", TermCategory.WATER_QUALITY, "A toxic gas dissolved in some produced water, particularly from sour formations. Requires special handling and DOT hazmat classification for transport.", abbreviation="H2S", synonyms=["sour gas", "sulfuretted hydrogen"], related_terms=["sour crude", "produced water", "safety"], context_notes="H2S in produced water creates occupational safety hazard. OSHA PEL: 20 ppm. DOT hazmat threshold: 100 ppm in headspace.", unit="ppm"),
        SemanticTerm("Specific Conductance", TermCategory.WATER_QUALITY, "A measure of water's ability to conduct electrical current, used as a proxy for TDS. Easier to measure in the field than TDS.", abbreviation="SpC", synonyms=["electrical conductivity", "EC"], related_terms=["TDS", "salinity", "field measurement"], context_notes="Approximate conversion: TDS (mg/L) = SpC (uS/cm) x 0.55-0.75 depending on dissolved ions.", unit="uS/cm"),
        SemanticTerm("Radium-226", TermCategory.WATER_QUALITY, "A naturally occurring radioactive isotope found in produced water, particularly from deep formations. Primary NORM constituent of concern in oilfield waste.", None, ["Ra-226"], ["NORM", "radioactive", "produced water"], "Combined Ra-226 and Ra-228 limit for discharge: 60 pCi/L (some jurisdictions 30 pCi/L).", unit="pCi/L", regulatory_reference="16 TAC Sec. 3.98"),
    ]


def _build_environmental_terms() -> list[SemanticTerm]:
    return [
        SemanticTerm("Aquifer Storage and Recovery", TermCategory.ENVIRONMENTAL, "A water management strategy where water is injected into an aquifer during periods of surplus and recovered during periods of shortage.", abbreviation="ASR", synonyms=["managed aquifer recharge and recovery"], related_terms=["conjunctive use", "aquifer recharge", "water banking"], context_notes="Requires both UIC permit (for injection) and water rights permit (for recovery). Growing interest in Texas.", regulatory_reference="TWC Sec. 27.151-27.157"),
        SemanticTerm("Playa Lake", TermCategory.ENVIRONMENTAL, "A shallow, ephemeral lake formed by rainfall accumulation in a closed basin, common on the Texas High Plains. May be jurisdictional waters under CWA.", None, ["playa", "ephemeral lake", "endorheic basin"], ["wetlands", "WOTUS", "Section 404"], "Playas are important recharge features for the Ogallala Aquifer. Jurisdictional status varies with WOTUS definition."),
        SemanticTerm("Riparian Zone", TermCategory.ENVIRONMENTAL, "The interface between land and a river or stream, characterized by vegetation adapted to periodic flooding.", None, ["riparian buffer", "streamside zone"], ["surface water", "erosion control", "habitat"], "Protection of riparian zones may affect pipeline routing and facility siting near watercourses."),
        SemanticTerm("Groundwater Management Area", TermCategory.ENVIRONMENTAL, "A geographic area designated by TWDB for coordinated groundwater management among GCDs overlying common aquifers.", abbreviation="GMA", synonyms=["groundwater management region"], related_terms=["GCD", "DFC", "MAG", "joint planning"], context_notes="Texas has 16 GMAs. GMA 7 covers much of the Trans-Pecos/Permian Basin region.", regulatory_reference="TWC Sec. 35.004"),
        SemanticTerm("Regional Water Planning Group", TermCategory.ENVIRONMENTAL, "One of 16 regional groups responsible for developing water supply plans as part of the Texas State Water Plan.", abbreviation="RWPG", synonyms=["regional water plan group"], related_terms=["TWDB", "state water plan", "water supply"], context_notes="Region F (Midland Basin) and Region E (Far West Texas) cover the Permian Basin area.", regulatory_reference="TWC Sec. 16.053"),
    ]


def _build_legal_terms() -> list[SemanticTerm]:
    return [
        SemanticTerm("Accommodation Doctrine", TermCategory.LEGAL, "The Texas doctrine requiring the dominant mineral estate to accommodate existing surface uses when reasonable alternative methods of mineral development exist.", None, ["surface accommodation", "Getty Oil doctrine"], ["surface owner", "mineral lessee", "reasonable alternative"], "Established in Getty Oil v. Jones (1971). Applied to water in Coyote Lake Ranch v. Lubbock (2016).", regulatory_reference="Getty Oil v. Jones, 470 S.W.2d 618 (Tex. 1971)"),
        SemanticTerm("Correlative Rights", TermCategory.LEGAL, "The concept that landowners sharing a common aquifer have co-equal rights to make reasonable use of the water, and one owner may not unreasonably deplete the common supply.", None, ["reasonable use doctrine", "shared resource rights"], ["rule of capture", "groundwater", "aquifer management"], "Texas has not adopted correlative rights for groundwater; instead follows rule of capture modified by GCD regulation."),
        SemanticTerm("Regulatory Taking", TermCategory.LEGAL, "A government regulation that goes so far as to deprive a property owner of all economically beneficial use of their property, requiring just compensation under the Takings Clause.", None, ["inverse condemnation", "Penn Central taking"], ["EAA v Day", "GCD regulation", "property rights"], "EAA v. Day held that groundwater regulation may constitute a taking under Penn Central analysis.", regulatory_reference="U.S. Const. Amend. V; Tex. Const. Art. I Sec. 17"),
        SemanticTerm("Police Power", TermCategory.LEGAL, "The inherent authority of the state to regulate for the protection of public health, safety, and welfare, including groundwater conservation and water quality protection.", None, ["regulatory authority", "state authority"], ["GCD authority", "TCEQ", "regulation"], "GCD groundwater regulation is authorized as an exercise of police power under Art. XVI Sec. 59."),
        SemanticTerm("Surface Damages Act", TermCategory.LEGAL, "Texas statute requiring oil and gas operators to compensate surface owners for damages caused by operations, including damage to water resources.", None, ["surface damage statute"], ["surface use agreement", "compensation", "water damage"], "Applies when operations damage surface owner's water wells, tanks, or water infrastructure.", regulatory_reference="TNRC Sec. 91.751-91.757"),
    ]


# ---------------------------------------------------------------------------
# Semantic Dictionary and Analyzer Classes
# ---------------------------------------------------------------------------

class WaterRightsSemanticDictionary:
    """Master dictionary aggregating all water rights terminology."""

    def __init__(self) -> None:
        self._terms: list[SemanticTerm] = []
        self._index: dict[str, SemanticTerm] = {}
        self._abbreviation_index: dict[str, SemanticTerm] = {}
        self._build()

    def _build(self) -> None:
        builders = [
            _build_groundwater_terms, _build_surface_water_terms,
            _build_produced_water_terms, _build_injection_well_terms,
            _build_aquifer_terms, _build_permit_terms,
            _build_compliance_terms, _build_oilfield_terms,
            _build_desalination_terms, _build_conveyancing_terms,
            _build_water_quality_terms, _build_environmental_terms,
            _build_legal_terms, _build_seismicity_terms,
            _build_transport_terms,
        ]
        for builder in builders:
            terms = builder()
            self._terms.extend(terms)
        for term in self._terms:
            self._index[term.term.lower()] = term
            for syn in term.synonyms:
                self._index[syn.lower()] = term
            if term.abbreviation:
                self._abbreviation_index[term.abbreviation.lower()] = term
        logger.info(f"Semantic dictionary built: {len(self._terms)} terms, {len(self._index)} index entries")

    def lookup(self, query: str) -> Optional[SemanticTerm]:
        q = query.lower().strip()
        if q in self._index:
            return self._index[q]
        if q in self._abbreviation_index:
            return self._abbreviation_index[q]
        return None

    def search(self, query: str, max_results: int = 10) -> list[SemanticTerm]:
        q = query.lower().strip()
        exact = self.lookup(q)
        if exact:
            return [exact]
        results: list[tuple[float, SemanticTerm]] = []
        q_terms = q.split()
        for term in self._terms:
            score = 0.0
            searchable = (
                term.term.lower() + " " + term.definition.lower() + " " +
                " ".join(term.synonyms).lower() + " " +
                " ".join(term.related_terms).lower() + " " +
                term.context_notes.lower()
            )
            for qt in q_terms:
                if qt in searchable:
                    score += 1.0
                if qt in term.term.lower():
                    score += 3.0
            if score > 0:
                results.append((score, term))
        results.sort(key=lambda x: x[0], reverse=True)
        return [t for _, t in results[:max_results]]

    def get_by_category(self, category: TermCategory) -> list[SemanticTerm]:
        return [t for t in self._terms if t.category == category]

    def get_all_terms(self) -> list[SemanticTerm]:
        return list(self._terms)

    @property
    def term_count(self) -> int:
        return len(self._terms)

    def extract_terms_from_text(self, text: str) -> list[SemanticTerm]:
        text_lower = text.lower()
        found: list[SemanticTerm] = []
        seen: set[str] = set()
        for term in self._terms:
            if term.term.lower() in text_lower and term.term not in seen:
                found.append(term)
                seen.add(term.term)
            elif term.abbreviation and re.search(r'\b' + re.escape(term.abbreviation) + r'\b', text):
                if term.term not in seen:
                    found.append(term)
                    seen.add(term.term)
        return found


class GroundwaterRightsAnalyzer:
    """Analyze groundwater rights issues using semantic understanding."""

    def __init__(self, dictionary: Optional[WaterRightsSemanticDictionary] = None) -> None:
        self._dict = dictionary or WaterRightsSemanticDictionary()

    def classify_water_source(self, tds_mg_l: float) -> str:
        if tds_mg_l < 500:
            return "fresh_drinking_quality"
        elif tds_mg_l < 1000:
            return "fresh_secondary"
        elif tds_mg_l < 3000:
            return "slightly_brackish"
        elif tds_mg_l < 10000:
            return "brackish"
        elif tds_mg_l < 35000:
            return "saline"
        else:
            return "hypersaline"

    def is_usdw(self, tds_mg_l: float, is_exempted: bool = False) -> bool:
        if is_exempted:
            return False
        return tds_mg_l < 10000

    def determine_gcd_permit_needed(self, gpm: float, use: str, county: str) -> dict[str, Any]:
        domestic_exempt_threshold = 25.0
        if county.lower() in ("reeves",):
            domestic_exempt_threshold = 17.5
        is_domestic = use.lower() in ("domestic", "livestock", "domestic_livestock")
        exempt = is_domestic and gpm <= domestic_exempt_threshold
        return {
            "county": county,
            "gpm": gpm,
            "use": use,
            "exempt": exempt,
            "permit_required": not exempt,
            "threshold_gpm": domestic_exempt_threshold,
            "rationale": f"{'Exempt' if exempt else 'Non-exempt'}: {use} use at {gpm} GPM in {county} County (threshold {domestic_exempt_threshold} GPM)",
        }

    def evaluate_rule_of_capture(self, scenario: dict[str, Any]) -> dict[str, Any]:
        has_gcd = scenario.get("has_gcd", False)
        is_malicious = scenario.get("is_malicious", False)
        causes_waste = scenario.get("causes_waste", False)
        causes_subsidence = scenario.get("causes_subsidence", False)
        analysis = {
            "rule_of_capture_applies": True,
            "exceptions_triggered": [],
            "gcd_overlay": has_gcd,
            "risk_level": "low",
            "recommendations": [],
        }
        if is_malicious:
            analysis["exceptions_triggered"].append("malicious_pumping")
            analysis["risk_level"] = "high"
            analysis["recommendations"].append("Cease pumping intended to injure neighbor")
        if causes_waste:
            analysis["exceptions_triggered"].append("willful_waste")
            analysis["risk_level"] = "moderate" if analysis["risk_level"] == "low" else analysis["risk_level"]
            analysis["recommendations"].append("Ensure all production is put to beneficial use")
        if causes_subsidence:
            analysis["exceptions_triggered"].append("subsidence_liability")
            analysis["risk_level"] = "high"
            analysis["recommendations"].append("Monitor for subsidence, consider liability under Friendswood standard")
        if has_gcd:
            analysis["recommendations"].append("Comply with GCD production permit conditions")
        return analysis


class SurfaceWaterPermitChecker:
    """Check surface water permit requirements and compliance."""

    def __init__(self, dictionary: Optional[WaterRightsSemanticDictionary] = None) -> None:
        self._dict = dictionary or WaterRightsSemanticDictionary()

    def check_permit_needed(self, use: str, volume_af_year: float, source: str) -> dict[str, Any]:
        is_surface = source.lower() in ("river", "stream", "lake", "reservoir", "creek", "pond")
        is_exempt_use = use.lower() in ("domestic", "livestock", "domestic_livestock")
        exempt = is_exempt_use and volume_af_year <= 200.0
        result = {
            "source": source,
            "use": use,
            "volume_af_year": volume_af_year,
            "is_surface_water": is_surface,
            "exempt": exempt,
            "tceq_permit_required": is_surface and not exempt,
            "rationale": "",
        }
        if not is_surface:
            result["rationale"] = "Not a surface water source; surface water permit not applicable"
        elif exempt:
            result["rationale"] = f"Exempt: {use} use at {volume_af_year} AF/yr (under 200 AF domestic/livestock threshold)"
        else:
            result["rationale"] = f"TCEQ appropriation permit required: {use} use at {volume_af_year} AF/yr from {source}"
        return result

    def check_cancellation_risk(self, last_use_date: str, current_date: str) -> dict[str, Any]:
        from datetime import datetime as dt
        last = dt.strptime(last_use_date, "%Y-%m-%d")
        now = dt.strptime(current_date, "%Y-%m-%d")
        years_idle = (now - last).days / 365.25
        at_risk = years_idle >= 10.0
        return {
            "last_use_date": last_use_date,
            "years_idle": round(years_idle, 1),
            "at_risk_of_cancellation": at_risk,
            "threshold_years": 10,
            "rationale": f"{'AT RISK' if at_risk else 'Not at risk'}: {round(years_idle, 1)} years of non-use (threshold: 10 years under TWC 11.173)",
        }


class ProducedWaterComplianceEngine:
    """Evaluate produced water compliance for oil and gas operations."""

    def __init__(self, dictionary: Optional[WaterRightsSemanticDictionary] = None) -> None:
        self._dict = dictionary or WaterRightsSemanticDictionary()

    def evaluate_disposal_method(self, method: str, volume_bbls_day: float, county: str) -> dict[str, Any]:
        methods_map = {
            "swd": {"permit": "H-1", "agency": "RRC", "risk": "moderate"},
            "eor": {"permit": "H-1", "agency": "RRC", "risk": "low"},
            "recycling": {"permit": "Rule 46 notice", "agency": "RRC", "risk": "low"},
            "surface_discharge": {"permit": "TPDES", "agency": "TCEQ", "risk": "high"},
            "evaporation_pit": {"permit": "RRC pit permit", "agency": "RRC", "risk": "moderate"},
            "land_application": {"permit": "TCEQ general permit", "agency": "TCEQ", "risk": "moderate"},
        }
        method_key = method.lower().replace(" ", "_")
        info = methods_map.get(method_key, {"permit": "Unknown", "agency": "Consult counsel", "risk": "high"})
        seismic_concern = method_key == "swd" and county.lower() in ("reeves", "pecos", "ward", "culberson")
        return {
            "method": method,
            "volume_bbls_day": volume_bbls_day,
            "county": county,
            "permit_required": info["permit"],
            "regulatory_agency": info["agency"],
            "base_risk": info["risk"],
            "seismicity_concern": seismic_concern,
            "recommendations": self._disposal_recommendations(method_key, volume_bbls_day, seismic_concern),
        }

    def _disposal_recommendations(self, method: str, volume: float, seismic: bool) -> list[str]:
        recs: list[str] = []
        if method == "swd":
            recs.append("Ensure H-1 permit is current and covers proposed volume")
            recs.append("Verify MIT is current (within 5 years)")
            if volume > 20000:
                recs.append("High volume: consider splitting across multiple wells to reduce seismic risk")
            if seismic:
                recs.append("SEISMIC REVIEW AREA: Monitor TexNet for nearby events; prepare for volume curtailment")
        elif method == "recycling":
            recs.append("File Rule 46 notification with RRC before commencing recycling")
            recs.append("Maintain chain of custody records for recycled water")
        elif method == "surface_discharge":
            recs.append("CRITICAL: Onshore zero-discharge standard applies (40 CFR 435)")
            recs.append("Individual TPDES permit required; consult TCEQ")
        return recs

    def score_compliance(self, well_data: dict[str, Any]) -> dict[str, Any]:
        score = 100.0
        flags: list[str] = []
        if not well_data.get("permit_current", True):
            score -= 30
            flags.append("Permit expired or not current")
        if not well_data.get("mit_current", True):
            score -= 25
            flags.append("MIT overdue (>5 years)")
        if well_data.get("exceeded_volume", False):
            score -= 20
            flags.append("Permitted injection volume exceeded")
        if well_data.get("exceeded_pressure", False):
            score -= 25
            flags.append("Maximum injection pressure exceeded")
        if not well_data.get("annual_report_filed", True):
            score -= 15
            flags.append("Annual monitoring report (H-10) not filed")
        if well_data.get("spill_unreported", False):
            score -= 20
            flags.append("Spill event not reported within 24 hours")
        score = max(0.0, score)
        if score >= 80:
            risk = "low"
        elif score >= 60:
            risk = "moderate"
        elif score >= 40:
            risk = "high"
        else:
            risk = "critical"
        return {
            "compliance_score": round(score, 1),
            "risk_level": risk,
            "flags": flags,
            "flag_count": len(flags),
        }


class AquiferAnalyzer:
    """Analyze aquifer characteristics and management issues."""

    def __init__(self, dictionary: Optional[WaterRightsSemanticDictionary] = None) -> None:
        self._dict = dictionary or WaterRightsSemanticDictionary()

    def assess_depletion_risk(self, aquifer: str, saturated_thickness_ft: float, recharge_in_per_yr: float, pumping_af_per_yr: float, area_acres: float) -> dict[str, Any]:
        recharge_af = (recharge_in_per_yr / 12.0) * area_acres
        net_depletion_af = pumping_af_per_yr - recharge_af
        if saturated_thickness_ft <= 0:
            years_remaining = 0.0
        elif net_depletion_af <= 0:
            years_remaining = float("inf")
        else:
            storage_af = saturated_thickness_ft * area_acres * 0.15
            years_remaining = storage_af / net_depletion_af
        if years_remaining == float("inf"):
            risk = "sustainable"
        elif years_remaining > 100:
            risk = "low"
        elif years_remaining > 50:
            risk = "moderate"
        elif years_remaining > 20:
            risk = "high"
        else:
            risk = "critical"
        return {
            "aquifer": aquifer,
            "saturated_thickness_ft": saturated_thickness_ft,
            "recharge_af_per_yr": round(recharge_af, 1),
            "pumping_af_per_yr": pumping_af_per_yr,
            "net_depletion_af_per_yr": round(net_depletion_af, 1),
            "estimated_years_remaining": round(years_remaining, 1) if years_remaining != float("inf") else "infinite",
            "depletion_risk": risk,
        }

    def classify_aquifer(self, tds_mg_l: float, aquifer_type: str) -> dict[str, Any]:
        if tds_mg_l < 1000:
            quality = "fresh"
        elif tds_mg_l < 3000:
            quality = "slightly_brackish"
        elif tds_mg_l < 10000:
            quality = "brackish"
        elif tds_mg_l < 35000:
            quality = "saline"
        else:
            quality = "brine"
        is_usdw = tds_mg_l < 10000
        suitable_uses = []
        if tds_mg_l < 500:
            suitable_uses.extend(["drinking_water", "irrigation", "industrial", "oilfield"])
        elif tds_mg_l < 1000:
            suitable_uses.extend(["irrigation", "livestock", "industrial", "oilfield"])
        elif tds_mg_l < 3000:
            suitable_uses.extend(["livestock", "industrial", "oilfield", "desalination_feedwater"])
        elif tds_mg_l < 10000:
            suitable_uses.extend(["oilfield", "desalination_feedwater"])
        else:
            suitable_uses.extend(["oilfield_direct_use", "disposal_zone_candidate"])
        return {
            "tds_mg_l": tds_mg_l,
            "aquifer_type": aquifer_type,
            "quality_class": quality,
            "is_usdw": is_usdw,
            "suitable_uses": suitable_uses,
        }


# ---------------------------------------------------------------------------
# Seismicity term builders
# ---------------------------------------------------------------------------

def _build_seismicity_terms() -> list[SemanticTerm]:
    """Build seismicity and induced seismicity terminology."""
    return [
        SemanticTerm(
            term="Induced Seismicity",
            category=TermCategory.SEISMICITY,
            definition="Earthquakes triggered by human activities, particularly injection of fluids "
                        "into deep disposal wells. In the Permian Basin, saltwater disposal into the "
                        "Ellenburger formation has been linked to increased seismic events since 2018.",
            synonyms=["injection-induced earthquakes", "man-made earthquakes", "triggered seismicity"],
            abbreviation="IS",
            regulatory_reference="16 TAC sec. 3.9(12); RRC seismicity response protocol",
        ),
        SemanticTerm(
            term="Seismic Response Area",
            category=TermCategory.SEISMICITY,
            definition="Geographic zone designated by RRC where injection well operations are subject "
                        "to enhanced monitoring and potential volume restrictions due to observed seismic "
                        "activity. Operators receive notice and must comply within 15 days.",
            synonyms=["SRA", "seismicity monitoring area", "earthquake response zone"],
            abbreviation="SRA",
            regulatory_reference="16 TAC sec. 3.46; RRC Oil and Gas Docket No. 08-0311628",
        ),
        SemanticTerm(
            term="Traffic Light Protocol",
            category=TermCategory.SEISMICITY,
            definition="Tiered response system for managing injection-induced seismicity: GREEN "
                        "(M<2.0, normal operations), YELLOW (M2.0-3.0, enhanced monitoring + possible "
                        "reduction), ORANGE (M3.0-3.5, mandatory 50% reduction), RED (M>3.5, shut-in "
                        "required). Used by RRC for Permian Basin SWD wells.",
            synonyms=["TLP", "seismicity traffic light", "injection protocol levels"],
            abbreviation="TLP",
            regulatory_reference="RRC seismicity response protocol (2022 revision)",
        ),
        SemanticTerm(
            term="Basement Fault",
            category=TermCategory.SEISMICITY,
            definition="Pre-existing geological fault in crystalline basement rock that can be "
                        "reactivated by fluid injection. Basement faults in the Permian Basin's Central "
                        "Basin Platform are primary targets for induced seismicity. Injection into "
                        "formations that communicate with basement increases risk.",
            synonyms=["pre-existing fault", "critically stressed fault", "reactivated fault"],
            abbreviation="",
            regulatory_reference="USGS induced seismicity guidelines; TexNet seismic monitoring",
        ),
        SemanticTerm(
            term="TexNet Seismic Monitoring",
            category=TermCategory.SEISMICITY,
            definition="Texas state seismic monitoring network operated by UT-BEG. Provides "
                        "real-time earthquake detection and location data. RRC uses TexNet data "
                        "for regulatory decisions on injection well operations.",
            synonyms=["Texas Seismological Network", "TexNet", "BEG seismic monitoring"],
            abbreviation="TexNet",
            regulatory_reference="TWC sec. 35.004; HB 2 (84th Legislature)",
        ),
        SemanticTerm(
            term="Maximum Allowable Surface Pressure",
            category=TermCategory.SEISMICITY,
            definition="RRC-set pressure limit for injection wells based on fracture gradient of "
                        "confining zone. MASP prevents injection fractures from propagating into "
                        "overlying formations or connecting to basement faults. Typically 0.75 psi/ft.",
            synonyms=["MASP", "maximum surface injection pressure", "permitted injection pressure"],
            abbreviation="MASP",
            regulatory_reference="16 TAC sec. 3.46(d); UIC permit conditions",
        ),
        SemanticTerm(
            term="Pore Pressure Diffusion",
            category=TermCategory.SEISMICITY,
            definition="Process by which elevated fluid pressure from injection migrates through "
                        "permeable rock to reach distant faults. Can trigger seismicity at distances "
                        "of 10+ km from injection well. Rate depends on permeability and injection volume.",
            synonyms=["pressure front migration", "injection pressure propagation", "hydraulic diffusivity"],
            abbreviation="",
            regulatory_reference="USGS Professional Paper 1951; Stanford induced seismicity research",
        ),
    ]


# ---------------------------------------------------------------------------
# Water transport term builders
# ---------------------------------------------------------------------------

def _build_transport_terms() -> list[SemanticTerm]:
    """Build water transport and pipeline terminology."""
    return [
        SemanticTerm(
            term="Produced Water Gathering System",
            category=TermCategory.WATER_TRANSPORT,
            definition="Pipeline network collecting produced water from wellheads and routing it "
                        "to disposal wells or recycling facilities. In the Permian Basin, gathering "
                        "systems typically operate at 50-150 psi and handle 10,000-100,000 bbls/day.",
            synonyms=["water gathering pipeline", "produced water collection", "water midstream"],
            abbreviation="PWGS",
            regulatory_reference="16 TAC ch. 3; PHMSA 49 CFR 195 (if interstate)",
        ),
        SemanticTerm(
            term="Water Midstream",
            category=TermCategory.WATER_TRANSPORT,
            definition="Sector of the oil and gas value chain focused on produced water handling: "
                        "gathering, transport, treatment, recycling, and disposal. Major Permian Basin "
                        "water midstream operators include Solaris, WaterBridge, and Breakwater.",
            synonyms=["water infrastructure", "water services", "midstream water handling"],
            abbreviation="",
            regulatory_reference="RRC pipeline permits; TCEQ discharge permits",
        ),
        SemanticTerm(
            term="Freshwater Impoundment",
            category=TermCategory.WATER_TRANSPORT,
            definition="Above-ground lined pit or tank battery for temporary storage of freshwater "
                        "used in drilling and completion operations. Must comply with TCEQ stormwater "
                        "general permit and GCD pumping authorizations. Typical capacity 50,000-500,000 bbls.",
            synonyms=["frac pond", "fresh pit", "completion water pond", "water storage pit"],
            abbreviation="",
            regulatory_reference="TCEQ TPDES general permit TXR150000; TWC ch. 26",
        ),
        SemanticTerm(
            term="Transfer Station",
            category=TermCategory.WATER_TRANSPORT,
            definition="Intermediate facility where produced water is transferred from trucks to "
                        "pipeline system, or between pipeline systems. Reduces truck traffic and "
                        "road damage. Commonly equipped with storage tanks and meters.",
            synonyms=["water transfer facility", "truck unloading station", "offloading facility"],
            abbreviation="",
            regulatory_reference="16 TAC sec. 3.8; county road use agreements",
        ),
        SemanticTerm(
            term="Layflat Temporary Pipeline",
            category=TermCategory.WATER_TRANSPORT,
            definition="Flexible above-ground pipeline used for temporary water transfer during "
                        "completion operations. Typically 10-16 inch diameter, HDPE or lay-flat hose. "
                        "Permian Basin operators use layflat to move freshwater from ponds to wellsite "
                        "or produced water from wellsite to disposal.",
            synonyms=["temporary water line", "lay-flat line", "above-ground transfer line"],
            abbreviation="",
            regulatory_reference="RRC notice requirements; county ROW permits",
        ),
        SemanticTerm(
            term="Water Recycling Facility",
            category=TermCategory.WATER_TRANSPORT,
            definition="Treatment plant that processes produced water to quality suitable for reuse "
                        "in drilling or completion operations. Technologies include oil/water separation, "
                        "filtration, chemical treatment, and sometimes desalination. Growing rapidly in "
                        "Permian Basin to reduce freshwater consumption.",
            synonyms=["water treatment plant", "produced water recycler", "reuse facility"],
            abbreviation="WRF",
            regulatory_reference="16 TAC sec. 3.46(e); RRC Rule 8; TCEQ beneficial reuse permits",
        ),
    ]


# ---------------------------------------------------------------------------
# Regulatory timeline tracker
# ---------------------------------------------------------------------------

class RegulatoryTimelineTracker:
    """Track regulatory milestones and deadlines for water rights permits."""

    STANDARD_TIMELINES: dict[str, dict[str, Any]] = {
        "tceq_surface_water_appropriation": {
            "description": "TCEQ surface water appropriation permit",
            "typical_duration_days": 365,
            "steps": [
                {"step": "Application filing", "day": 0},
                {"step": "Administrative review", "day": 30},
                {"step": "Technical review", "day": 90},
                {"step": "Public notice", "day": 120},
                {"step": "Comment period (30 days)", "day": 150},
                {"step": "Contested case hearing (if contested)", "day": 240},
                {"step": "SOAH PFD issued", "day": 300},
                {"step": "Commission action", "day": 365},
            ],
        },
        "rrc_injection_well_permit": {
            "description": "RRC UIC Class II injection well permit (Form W-14)",
            "typical_duration_days": 180,
            "steps": [
                {"step": "W-14 application filed", "day": 0},
                {"step": "Administrative completeness check", "day": 14},
                {"step": "Technical review", "day": 45},
                {"step": "Public notice in newspaper", "day": 60},
                {"step": "Protest period (15 days)", "day": 75},
                {"step": "Hearing (if protested)", "day": 120},
                {"step": "Permit issued or denied", "day": 180},
            ],
        },
        "gcd_groundwater_permit": {
            "description": "GCD operating permit for groundwater production",
            "typical_duration_days": 120,
            "steps": [
                {"step": "Application filed with GCD", "day": 0},
                {"step": "Completeness determination", "day": 14},
                {"step": "Technical review", "day": 30},
                {"step": "Notice to landowners within 1/2 mile", "day": 45},
                {"step": "Hearing (if contested)", "day": 75},
                {"step": "Board action", "day": 90},
                {"step": "Permit effective", "day": 120},
            ],
        },
        "tceq_beneficial_reuse": {
            "description": "TCEQ permit for beneficial reuse of produced water",
            "typical_duration_days": 240,
            "steps": [
                {"step": "Pre-application meeting", "day": 0},
                {"step": "Application filing", "day": 30},
                {"step": "Technical review of treatment process", "day": 90},
                {"step": "Water quality testing verification", "day": 120},
                {"step": "Public notice", "day": 150},
                {"step": "Comment period", "day": 180},
                {"step": "Permit issuance", "day": 240},
            ],
        },
    }

    def get_timeline(self, permit_type: str) -> dict[str, Any]:
        """Get standard regulatory timeline for a permit type."""
        timeline = self.STANDARD_TIMELINES.get(permit_type)
        if not timeline:
            logger.warning(f"Unknown permit type: {permit_type}")
            return {
                "permit_type": permit_type,
                "error": f"No standard timeline available for {permit_type}",
                "available_types": list(self.STANDARD_TIMELINES.keys()),
            }
        return {
            "permit_type": permit_type,
            "description": timeline["description"],
            "typical_duration_days": timeline["typical_duration_days"],
            "steps": timeline["steps"],
        }

    def estimate_completion(self, permit_type: str, filing_date: str) -> dict[str, Any]:
        """Estimate permit completion date from filing date."""
        timeline = self.STANDARD_TIMELINES.get(permit_type)
        if not timeline:
            return {"error": f"Unknown permit type: {permit_type}"}
        try:
            from datetime import datetime, timedelta
            filed = datetime.strptime(filing_date, "%Y-%m-%d")
            projected_steps = []
            for step in timeline["steps"]:
                step_date = filed + timedelta(days=step["day"])
                projected_steps.append({
                    "step": step["step"],
                    "projected_date": step_date.strftime("%Y-%m-%d"),
                    "day": step["day"],
                })
            completion = filed + timedelta(days=timeline["typical_duration_days"])
            return {
                "permit_type": permit_type,
                "filing_date": filing_date,
                "projected_completion": completion.strftime("%Y-%m-%d"),
                "projected_steps": projected_steps,
                "note": "Timelines are estimates; contested cases may extend significantly",
            }
        except ValueError as e:
            return {"error": f"Invalid date format: {e}. Use YYYY-MM-DD."}

    def list_permit_types(self) -> list[dict[str, str]]:
        """List all available permit timeline types."""
        return [
            {"type": k, "description": v["description"], "typical_days": str(v["typical_duration_days"])}
            for k, v in self.STANDARD_TIMELINES.items()
        ]
