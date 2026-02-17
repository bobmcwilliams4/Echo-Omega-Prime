import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import hashlib
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple, Set
from enum import Enum, auto
from datetime import datetime, timedelta

# =========================
# ENUMS
# =========================

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
    HETEROGENEOUS_CATALYSIS = "HETEROGENEOUS_CATALYSIS"
    HOMOGENEOUS_CATALYSIS = "HOMOGENEOUS_CATALYSIS"
    ENZYME_KINETICS = "ENZYME_KINETICS"
    CATALYST_CHARACTERIZATION = "CATALYST_CHARACTERIZATION"
    REACTION_KINETICS = "REACTION_KINETICS"
    REACTOR_DESIGN = "REACTOR_DESIGN"
    CATALYST_DEACTIVATION = "CATALYST_DEACTIVATION"
    ZEOLITE_CATALYSIS = "ZEOLITE_CATALYSIS"
    FISCHER_TROPSCH = "FISCHER_TROPSCH"
    HYDROPROCESSING = "HYDROPROCESSING"
    FCC = "FCC"
    AMMONIA_SYNTHESIS = "AMMONIA_SYNTHESIS"
    CATALYTIC_CONVERTER = "CATALYTIC_CONVERTER"
    PHOTOCATALYSIS = "PHOTOCATALYSIS"
    ELECTROCATALYSIS = "ELECTROCATALYSIS"
    BIOCATALYSIS = "BIOCATALYSIS"
    CATALYST_SELECTIVITY = "CATALYST_SELECTIVITY"
    MASS_TRANSFER = "MASS_TRANSFER"
    CATALYST_REGENERATION = "CATALYST_REGENERATION"
    GREEN_CHEMISTRY = "GREEN_CHEMISTRY"

# =========================
# METRICS COLLECTOR
# =========================

class MetricsCollector:
    def __init__(self):
        self.queries: List[Dict[str, Any]] = []
        self.errors: List[Dict[str, Any]] = []
        self.doctrine_hits: Dict[str, int] = {}
        self.latencies: List[float] = []

    def record_query(self, query_id: str, doctrine_keys: List[str], latency: float):
        self.queries.append({
            "query_id": query_id,
            "doctrines": doctrine_keys,
            "timestamp": datetime.utcnow(),
            "latency": latency
        })
        for k in doctrine_keys:
            self.doctrine_hits[k] = self.doctrine_hits.get(k, 0) + 1
        self.latencies.append(latency)

    def record_error(self, query_id: str, error: str):
        self.errors.append({
            "query_id": query_id,
            "error": error,
            "timestamp": datetime.utcnow()
        })

    def get_latency_stats(self) -> Dict[str, float]:
        if not self.latencies:
            return {"min": 0, "max": 0, "avg": 0}
        return {
            "min": min(self.latencies),
            "max": max(self.latencies),
            "avg": sum(self.latencies) / len(self.latencies)
        }

    def get_doctrine_hit_rate(self) -> Dict[str, int]:
        return dict(self.doctrine_hits)

    def queries_last_hour(self) -> int:
        cutoff = datetime.utcnow() - timedelta(hours=1)
        return sum(1 for q in self.queries if q["timestamp"] > cutoff)

metrics_collector = MetricsCollector()

# =========================
# PYDANTIC MODELS
# =========================

class QueryRequest(BaseModel):
    scenario: str = Field(..., description="Catalytic process scenario or question")
    mode: ResponseMode = Field(..., description="Response mode")
    entity_type: str = Field(..., description="Type of catalyst or process entity")
    complexity: int = Field(..., ge=1, le=5, description="Scenario complexity (1-5)")

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

# =========================
# DOCTRINE CACHE
# =========================

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
    confidence_zone: ConfidenceZone
    controlling_precedent: str

# -- Doctrine Blocks (30+) --
DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Heterogeneous Catalysis: Surface Adsorption and Langmuir Isotherm",
        keywords=["heterogeneous", "adsorption", "Langmuir", "surface", "BET"],
        conclusion_template=(
            "The rate and selectivity of heterogeneous catalytic reactions are fundamentally governed by the adsorption equilibrium between reactant molecules and catalyst surface sites. "
            "The Langmuir adsorption isotherm provides a robust model for monolayer adsorption, while the BET method extends to multilayer systems. "
            "Accurate characterization of adsorption phenomena is critical for catalyst design and process optimization."
        ),
        reasoning_framework=(
            "1. Surface adsorption is the initial step in heterogeneous catalysis, dictating the availability of active sites for reaction (Somorjai & Li, 2010).\n"
            "2. The Langmuir isotherm assumes uniform surface sites and no interaction between adsorbed molecules, yielding θ = (Kp)/(1+Kp), where θ is surface coverage (Atkins & de Paula, 2017).\n"
            "3. For real catalysts, surface heterogeneity and multilayer adsorption are addressed by the BET equation, which extends Langmuir's model (Brunauer et al., 1938).\n"
            "4. Experimental determination of adsorption isotherms (e.g., N2 physisorption) enables calculation of surface area and pore size distribution, critical for catalyst performance.\n"
            "5. Deviations from ideal behavior (e.g., strong adsorbate-adsorbate interactions) require advanced models or in situ spectroscopic validation.\n"
            "6. The rate-determining step may shift from adsorption to surface reaction or desorption depending on reactant partial pressures and temperature.\n"
            "7. Accurate kinetic modeling must incorporate competitive adsorption in multicomponent systems.\n"
            "8. The presence of strongly adsorbed poisons can block active sites, reducing catalytic activity (Bartholomew, 2001).\n"
            "9. Surface reconstruction or sintering can alter adsorption characteristics over time, impacting catalyst lifetime.\n"
            "10. Integration of adsorption data with microkinetic models enhances predictive power for reactor-scale simulations."
        ),
        key_factors=[
            "Surface area and pore structure",
            "Adsorption equilibrium constants",
            "Competitive adsorption effects",
            "Presence of poisons or inhibitors",
            "Temperature and pressure dependence"
        ],
        primary_authority=[
            "Somorjai, G.A. & Li, Y. (2010). Introduction to Surface Chemistry and Catalysis.",
            "Brunauer, S., Emmett, P.H., & Teller, E. (1938). J. Am. Chem. Soc. 60, 309.",
            "Atkins, P. & de Paula, J. (2017). Physical Chemistry, 11th Ed."
        ],
        burden_holder="Process Engineer",
        adversary_position="Assumes ideal surface and neglects real catalyst heterogeneity.",
        counter_arguments=[
            "Langmuir model fails for strong adsorbate-adsorbate interactions.",
            "BET method is invalid for microporous materials.",
            "Surface reconstruction alters site availability.",
            "Competitive adsorption distorts single-component isotherms.",
            "Poisoning by trace contaminants not accounted for."
        ],
        resolution_strategy="Cross-validate isotherm models with experimental spectroscopy and apply microkinetic simulations for non-ideal systems.",
        entity_scope="Solid catalysts in fixed-bed reactors",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Brunauer et al., 1938; Somorjai & Li, 2010"
    ),
    DoctrineBlock(
        topic="Homogeneous Catalysis: Organometallic Mechanisms (Wilkinson, Grubbs)",
        keywords=["homogeneous", "organometallic", "Wilkinson", "Grubbs", "mechanism"],
        conclusion_template=(
            "Homogeneous catalysis via organometallic complexes enables highly selective transformations under mild conditions. "
            "Wilkinson's catalyst (RhCl(PPh3)3) is a benchmark for hydrogenation, while Grubbs' catalysts revolutionized olefin metathesis. "
            "Mechanistic understanding is essential for tuning activity and selectivity."
        ),
        reasoning_framework=(
            "1. Homogeneous catalysts are soluble in the reaction medium, allowing for molecular-level control of the catalytic cycle (Hartwig, 2010).\n"
            "2. Wilkinson's catalyst operates via oxidative addition, migratory insertion, and reductive elimination steps (Wilkinson, 1966).\n"
            "3. Ligand effects (electronic and steric) modulate the rate and selectivity of hydrogenation (Tolman, 1977).\n"
            "4. Grubbs' catalysts (Ru-based) mediate olefin metathesis through a [2+2] cycloaddition and metallacyclobutane intermediates (Grubbs & Trnka, 2001).\n"
            "5. Catalyst deactivation via ligand dissociation or bimolecular decomposition is a key limitation.\n"
            "6. Solvent polarity and coordinating ability affect catalyst stability and turnover number (TON).\n"
            "7. Additives (e.g., phosphines, NHCs) can enhance catalyst lifetime or suppress side reactions.\n"
            "8. Kinetic studies (e.g., stopped-flow, NMR) elucidate rate-limiting steps and resting states.\n"
            "9. Computational chemistry (DFT) provides insights into transition states and energy barriers.\n"
            "10. Industrial implementation requires balancing catalyst cost, recovery, and product purity."
        ),
        key_factors=[
            "Ligand structure and electronics",
            "Solvent effects",
            "Catalyst stability and deactivation",
            "Turnover number (TON) and frequency (TOF)",
            "Substrate scope and functional group tolerance"
        ],
        primary_authority=[
            "Hartwig, J.F. (2010). Organotransition Metal Chemistry.",
            "Wilkinson, G. (1966). Nobel Lecture: Organometallic Compounds.",
            "Grubbs, R.H. & Trnka, T.M. (2001). Acc. Chem. Res. 34, 18."
        ],
        burden_holder="Catalyst Developer",
        adversary_position="Questions catalyst robustness and scalability in industrial settings.",
        counter_arguments=[
            "Homogeneous catalysts are difficult to separate from products.",
            "Ligand dissociation leads to rapid deactivation.",
            "Air/moisture sensitivity complicates handling.",
            "High catalyst cost limits large-scale use.",
            "Side reactions reduce selectivity in complex mixtures."
        ],
        resolution_strategy="Optimize ligand design, employ biphasic systems for catalyst recovery, and validate with pilot-scale studies.",
        entity_scope="Solution-phase catalytic processes",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Wilkinson, 1966; Grubbs & Trnka, 2001"
    ),
    DoctrineBlock(
        topic="Enzyme Kinetics: Michaelis-Menten and Inhibition",
        keywords=["enzyme", "kinetics", "Michaelis-Menten", "inhibition", "Lineweaver-Burk"],
        conclusion_template=(
            "Enzyme-catalyzed reactions are characterized by the Michaelis-Menten model, which describes the relationship between substrate concentration and reaction velocity. "
            "Inhibition (competitive, noncompetitive, uncompetitive) alters kinetic parameters and must be considered in biocatalytic process design."
        ),
        reasoning_framework=(
            "1. The Michaelis-Menten equation v = (Vmax[S])/(Km + [S]) models the hyperbolic dependence of rate on substrate concentration (Michaelis & Menten, 1913).\n"
            "2. Km reflects the substrate concentration at half-maximal velocity and is a measure of enzyme-substrate affinity.\n"
            "3. Lineweaver-Burk plots (double reciprocal) linearize the kinetic data, facilitating parameter extraction (Lineweaver & Burk, 1934).\n"
            "4. Competitive inhibitors increase apparent Km without affecting Vmax, as they bind to the active site.\n"
            "5. Noncompetitive inhibitors decrease Vmax but do not alter Km, binding to allosteric sites.\n"
            "6. Uncompetitive inhibitors bind only to the enzyme-substrate complex, reducing both Km and Vmax.\n"
            "7. Product inhibition and substrate inhibition must be accounted for in high-conversion systems.\n"
            "8. Enzyme immobilization can alter apparent kinetic parameters due to mass transfer limitations.\n"
            "9. Temperature and pH affect enzyme activity and stability, requiring optimization for industrial applications.\n"
            "10. Kinetic modeling guides reactor design and process control in biocatalysis."
        ),
        key_factors=[
            "Km and Vmax values",
            "Type of inhibition",
            "Enzyme stability",
            "Substrate and product concentrations",
            "Mass transfer effects"
        ],
        primary_authority=[
            "Michaelis, L. & Menten, M.L. (1913). Biochem. Z. 49, 333.",
            "Lineweaver, H. & Burk, D. (1934). J. Am. Chem. Soc. 56, 658.",
            "Cornish-Bowden, A. (2012). Fundamentals of Enzyme Kinetics."
        ],
        burden_holder="Bioprocess Engineer",
        adversary_position="Assumes ideal enzyme behavior and neglects real-world mass transfer or stability issues.",
        counter_arguments=[
            "Inhibitor effects are more complex in vivo.",
            "Enzyme denaturation at process conditions.",
            "Immobilization alters kinetic parameters.",
            "Product inhibition limits achievable yield.",
            "Diffusion limitations in immobilized systems."
        ],
        resolution_strategy="Empirically determine kinetic parameters under process conditions and validate with pilot-scale data.",
        entity_scope="Enzyme-catalyzed industrial processes",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Michaelis & Menten, 1913; Cornish-Bowden, 2012"
    ),
    DoctrineBlock(
        topic="Catalyst Characterization: XRD, BET, TPR, TPD, XPS",
        keywords=["characterization", "XRD", "BET", "TPR", "XPS"],
        conclusion_template=(
            "Comprehensive catalyst characterization is essential for correlating structure with catalytic performance. "
            "Techniques such as XRD, BET, TPR, TPD, and XPS provide complementary information on crystallinity, surface area, reducibility, acidity, and surface composition."
        ),
        reasoning_framework=(
            "1. X-ray diffraction (XRD) identifies crystalline phases and crystallite size via Scherrer analysis (Cullity & Stock, 2014).\n"
            "2. BET N2 physisorption quantifies surface area and pore volume, critical for dispersion and accessibility (Brunauer et al., 1938).\n"
            "3. Temperature-programmed reduction (TPR) reveals reducibility and metal-support interactions.\n"
            "4. Temperature-programmed desorption (TPD) assesses acid/base site strength and distribution.\n"
            "5. X-ray photoelectron spectroscopy (XPS) determines surface oxidation states and elemental composition (Briggs & Grant, 2003).\n"
            "6. Combining techniques enables identification of structure-activity relationships.\n"
            "7. In situ/operando methods capture dynamic changes under reaction conditions.\n"
            "8. Sample preparation and data interpretation require rigorous protocols to avoid artifacts.\n"
            "9. Correlation of characterization data with catalytic performance guides rational catalyst design.\n"
            "10. Advanced methods (e.g., STEM, EXAFS) provide atomic-scale insight for next-generation catalysts."
        ),
        key_factors=[
            "Crystalline phase identification",
            "Surface area and porosity",
            "Redox properties",
            "Acid/base site distribution",
            "Surface composition and oxidation state"
        ],
        primary_authority=[
            "Cullity, B.D. & Stock, S.R. (2014). Elements of X-ray Diffraction.",
            "Brunauer, S. et al. (1938). J. Am. Chem. Soc. 60, 309.",
            "Briggs, D. & Grant, J.T. (2003). Surface Analysis by XPS and AES."
        ],
        burden_holder="Catalyst Analyst",
        adversary_position="Questions reliability of characterization due to sample preparation artifacts.",
        counter_arguments=[
            "XRD cannot detect amorphous phases.",
            "BET method is sensitive to degassing conditions.",
            "TPR/TPD results depend on ramp rate and carrier gas.",
            "XPS probes only the top few nanometers.",
            "Sample handling may induce surface changes."
        ],
        resolution_strategy="Cross-validate with multiple techniques and apply in situ/operando characterization where possible.",
        entity_scope="All catalyst types (heterogeneous, supported, bulk)",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Cullity & Stock, 2014; Briggs & Grant, 2003"
    ),
    DoctrineBlock(
        topic="Reaction Kinetics: Rate Laws and Arrhenius Equation",
        keywords=["kinetics", "rate law", "Arrhenius", "activation energy", "temperature"],
        conclusion_template=(
            "Reaction kinetics are governed by rate laws that relate reactant concentrations to reaction rate. "
            "The Arrhenius equation quantifies the temperature dependence of rate constants, with activation energy as a key parameter."
        ),
        reasoning_framework=(
            "1. Rate laws are determined experimentally and can be zero, first, or second order with respect to reactants (Levenspiel, 1999).\n"
            "2. The Arrhenius equation k = A exp(-Ea/RT) describes the exponential increase of rate constant with temperature (Arrhenius, 1889).\n"
            "3. Activation energy (Ea) is extracted from the slope of ln(k) vs. 1/T plots.\n"
            "4. Catalysts lower Ea by providing alternative reaction pathways, increasing rate without affecting equilibrium.\n"
            "5. Reaction order may change with mechanism or at different conversions.\n"
            "6. In complex systems, apparent kinetics may reflect mass transfer or adsorption limitations.\n"
            "7. Microkinetic modeling integrates elementary steps for mechanistic insight.\n"
            "8. Temperature-programmed experiments (e.g., TPR) can reveal kinetic parameters.\n"
            "9. Kinetic isotope effects (KIE) provide evidence for rate-determining steps.\n"
            "10. Accurate kinetic models are essential for reactor design and scale-up."
        ),
        key_factors=[
            "Reaction order",
            "Activation energy (Ea)",
            "Pre-exponential factor (A)",
            "Temperature dependence",
            "Mass transfer limitations"
        ],
        primary_authority=[
            "Levenspiel, O. (1999). Chemical Reaction Engineering, 3rd Ed.",
            "Arrhenius, S. (1889). Z. Phys. Chem. 4, 226.",
            "Fogler, H.S. (2016). Elements of Chemical Reaction Engineering."
        ],
        burden_holder="Process Kineticist",
        adversary_position="Assumes intrinsic kinetics, neglecting transport effects.",
        counter_arguments=[
            "Observed rate may be limited by diffusion.",
            "Catalyst deactivation alters apparent kinetics.",
            "Temperature gradients in reactors affect rate.",
            "Side reactions complicate kinetic analysis.",
            "Experimental error in rate measurements."
        ],
        resolution_strategy="Validate intrinsic kinetics via differential reactors and rule out transport limitations.",
        entity_scope="All catalytic reactions",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Levenspiel, 1999; Arrhenius, 1889"
    ),
    DoctrineBlock(
        topic="Reactor Design: CSTR, PFR, Batch, Semi-batch",
        keywords=["reactor", "CSTR", "PFR", "batch", "semi-batch"],
        conclusion_template=(
            "Selection of reactor type (CSTR, PFR, batch, semi-batch) depends on reaction kinetics, heat/mass transfer, and process integration. "
            "Each reactor type offers distinct advantages and limitations for catalytic processes."
        ),
        reasoning_framework=(
            "1. Continuous stirred-tank reactors (CSTR) provide uniform composition but may suffer from back-mixing and lower conversion per pass (Levenspiel, 1999).\n"
            "2. Plug flow reactors (PFR) offer high conversion and are suitable for fast, exothermic reactions with minimal back-mixing.\n"
            "3. Batch reactors are flexible for small-scale or multi-product operations but less efficient for large volumes.\n"
            "4. Semi-batch reactors allow for controlled addition/removal of reactants or products, useful for managing heat release or selectivity.\n"
            "5. Reactor selection impacts catalyst lifetime, as fouling or deactivation may be more severe in certain configurations.\n"
            "6. Heat and mass transfer limitations must be addressed via design (e.g., baffles, internals).\n"
            "7. Scale-up requires maintaining similar hydrodynamics and residence time distributions.\n"
            "8. Computational fluid dynamics (CFD) aids in optimizing reactor geometry and operation.\n"
            "9. Integration with separation units (e.g., membrane reactors) can enhance process efficiency.\n"
            "10. Safety and operability considerations are paramount in high-pressure or exothermic systems."
        ),
        key_factors=[
            "Residence time distribution",
            "Heat/mass transfer",
            "Catalyst deactivation profile",
            "Process flexibility",
            "Safety and scale-up"
        ],
        primary_authority=[
            "Levenspiel, O. (1999). Chemical Reaction Engineering, 3rd Ed.",
            "Fogler, H.S. (2016). Elements of Chemical Reaction Engineering.",
            "Nauman, E.B. (2008). Chemical Reactor Design, Optimization, and Scaleup."
        ],
        burden_holder="Process Designer",
        adversary_position="Questions scalability and control of side reactions.",
        counter_arguments=[
            "CSTRs require large volumes for high conversion.",
            "PFRs may develop hot spots in exothermic reactions.",
            "Batch operation is labor-intensive.",
            "Semi-batch control is complex.",
            "Scale-up may alter hydrodynamics."
        ],
        resolution_strategy="Pilot-scale testing and CFD modeling to validate design before scale-up.",
        entity_scope="All catalytic reactor systems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Levenspiel, 1999; Fogler, 2016"
    ),
    DoctrineBlock(
        topic="Catalyst Deactivation: Sintering, Poisoning, Coking",
        keywords=["deactivation", "sintering", "poisoning", "coking", "lifetime"],
        conclusion_template=(
            "Catalyst deactivation is a major challenge in industrial catalysis, arising from sintering, poisoning, and coking. "
            "Understanding and mitigating these mechanisms is essential for process reliability and economics."
        ),
        reasoning_framework=(
            "1. Sintering involves the growth of catalyst particles at elevated temperatures, reducing active surface area (Bartholomew, 2001).\n"
            "2. Poisoning occurs when impurities (e.g., S, Pb, Cl) bind irreversibly to active sites, blocking catalytic function.\n"
            "3. Coking results from the deposition of carbonaceous species, especially in hydrocarbon processing (Bartholomew, 2001).\n"
            "4. Deactivation kinetics can be modeled to predict catalyst lifetime and regeneration intervals.\n"
            "5. Support selection and promoter addition can enhance resistance to sintering or poisoning.\n"
            "6. Feed purification and process control minimize exposure to poisons.\n"
            "7. Regeneration strategies (oxidative, reductive) restore activity but may induce structural changes.\n"
            "8. In situ monitoring (e.g., TGA, DRIFTS) enables early detection of deactivation.\n"
            "9. Catalyst design (e.g., core-shell, encapsulation) can mitigate deactivation pathways.\n"
            "10. Economic analysis must weigh catalyst cost, replacement frequency, and downtime."
        ),
        key_factors=[
            "Operating temperature",
            "Feed impurities",
            "Coke formation propensity",
            "Regeneration protocols",
            "Support and promoter effects"
        ],
        primary_authority=[
            "Bartholomew, C.H. (2001). Appl. Catal. A 212, 17.",
            "Ertl, G. et al. (2008). Handbook of Heterogeneous Catalysis.",
            "van Santen, R.A. (2017). Catalysis: An Integrated Approach."
        ],
        burden_holder="Operations Manager",
        adversary_position="Questions long-term stability and regeneration efficacy.",
        counter_arguments=[
            "Regeneration may not fully restore activity.",
            "Sintering is irreversible at high temperature.",
            "Trace poisons accumulate over time.",
            "Coke removal may damage catalyst structure.",
            "Deactivation kinetics are system-specific."
        ],
        resolution_strategy="Implement real-time monitoring and optimize regeneration cycles based on deactivation modeling.",
        entity_scope="All industrial catalytic processes",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Bartholomew, 2001; Ertl et al., 2008"
    ),
    DoctrineBlock(
        topic="Zeolite Catalysis: Shape Selectivity and Acidity",
        keywords=["zeolite", "shape selectivity", "acidity", "framework", "microporous"],
        conclusion_template=(
            "Zeolites are microporous aluminosilicates exhibiting unique shape selectivity and tunable acidity. "
            "Their framework topology and acid site distribution enable tailored catalytic transformations."
        ),
        reasoning_framework=(
            "1. Zeolite frameworks (e.g., MFI, FAU) define pore size and connectivity, controlling molecular access (Corma, 1997).\n"
            "2. Shape selectivity arises from size exclusion, transition state stabilization, and product diffusion limitations.\n"
            "3. Brønsted and Lewis acid sites are generated by framework Al and extra-framework cations, respectively.\n"
            "4. Acidity is quantified by NH3-TPD, pyridine-IR, or MAS NMR spectroscopy.\n"
            "5. Si/Al ratio tunes acid strength and hydrothermal stability.\n"
            "6. Post-synthetic modifications (e.g., dealumination, ion exchange) tailor catalytic properties.\n"
            "7. Zeolites excel in hydrocarbon cracking, isomerization, and alkylation due to their selectivity.\n"
            "8. Deactivation via coking or dealumination is a key challenge in high-temperature processes.\n"
            "9. Hierarchical zeolites with mesoporosity enhance diffusion and accessibility.\n"
            "10. Structure-activity relationships guide rational design for target reactions."
        ),
        key_factors=[
            "Framework topology",
            "Acid site density and strength",
            "Si/Al ratio",
            "Pore size and connectivity",
            "Coke resistance"
        ],
        primary_authority=[
            "Corma, A. (1997). Chem. Rev. 97, 2373.",
            "van Santen, R.A. (2017). Catalysis: An Integrated Approach.",
            "Weitkamp, J. (2000). Solid State Ionics 131, 175."
        ],
        burden_holder="Zeolite Chemist",
        adversary_position="Questions diffusion limitations and deactivation by coking.",
        counter_arguments=[
            "Micropores limit access for bulky molecules.",
            "Dealumination reduces acid site density.",
            "Coke formation blocks pores.",
            "Framework collapse under steam.",
            "Acidity characterization may be ambiguous."
        ],
        resolution_strategy="Employ hierarchical zeolites and advanced characterization to optimize performance.",
        entity_scope="Zeolite-catalyzed hydrocarbon processes",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Corma, 1997; Weitkamp, 2000"
    ),
    DoctrineBlock(
        topic="Fischer-Tropsch Synthesis: Cobalt and Iron Catalysts",
        keywords=["Fischer-Tropsch", "cobalt", "iron", "syngas", "hydrocarbon synthesis"],
        conclusion_template=(
            "Fischer-Tropsch synthesis converts syngas (CO+H2) to hydrocarbons using cobalt or iron catalysts. "
            "Catalyst selection and process conditions determine product distribution and catalyst lifetime."
        ),
        reasoning_framework=(
            "1. Cobalt catalysts are preferred for low-temperature FT (200-240°C) due to higher activity and selectivity to long-chain paraffins (Dry, 2002).\n"
            "2. Iron catalysts are suitable for high-temperature FT and tolerate higher CO2 and water concentrations.\n"
            "3. Catalyst support (e.g., Al2O3, SiO2, TiO2) affects dispersion, reducibility, and stability.\n"
            "4. Promoters (e.g., Ru, Re, K) enhance activity, selectivity, or resistance to deactivation.\n"
            "5. Water-gas shift activity is significant for iron but minimal for cobalt catalysts.\n"
            "6. Deactivation occurs via sintering, oxidation, or carbon deposition.\n"
            "7. Product distribution follows the Anderson-Schulz-Flory model, tunable by process conditions.\n"
            "8. Reactor design (fixed-bed, slurry, fluidized-bed) impacts heat removal and scale-up.\n"
            "9. Syngas purity and H2/CO ratio are critical for optimal performance.\n"
            "10. Life-cycle analysis must consider catalyst cost, regeneration, and environmental impact."
        ),
        key_factors=[
            "Catalyst metal (Co vs. Fe)",
            "Support and promoter effects",
            "Syngas composition",
            "Reactor configuration",
            "Deactivation mechanisms"
        ],
        primary_authority=[
            "Dry, M.E. (2002). Catal. Today 71, 227.",
            "Bartholomew, C.H. (2001). Appl. Catal. A 212, 17.",
            "Ertl, G. et al. (2008). Handbook of Heterogeneous Catalysis."
        ],
        burden_holder="Process Developer",
        adversary_position="Questions catalyst cost and deactivation under real syngas feeds.",
        counter_arguments=[
            "Cobalt is expensive and sensitive to sulfur.",
            "Iron catalysts deactivate rapidly at low temperature.",
            "Heat removal is challenging at scale.",
            "Product selectivity is limited by ASF distribution.",
            "Syngas impurities poison active sites."
        ],
        resolution_strategy="Optimize support/promoter formulation and implement rigorous feed purification.",
        entity_scope="Fischer-Tropsch reactors (all scales)",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Dry, 2002; Bartholomew, 2001"
    ),
    DoctrineBlock(
        topic="Hydrocracking, Hydrodesulfurization, and Hydrotreating",
        keywords=["hydrocracking", "hydrodesulfurization", "hydrotreating", "sulfur removal", "NiMo"],
        conclusion_template=(
            "Hydrocracking, hydrodesulfurization (HDS), and hydrotreating are key processes for upgrading petroleum fractions. "
            "Bifunctional catalysts (e.g., NiMo/Al2O3) enable simultaneous cracking, hydrogenation, and sulfur removal."
        ),
        reasoning_framework=(
            "1. Hydrotreating removes heteroatoms (S, N, O) via hydrogenation and cleavage, improving fuel quality (Speight, 2014).\n"
            "2. Hydrodesulfurization employs sulfided NiMo or CoMo catalysts supported on γ-Al2O3.\n"
            "3. Hydrocracking uses bifunctional catalysts with acid and metal sites for C-C bond cleavage and isomerization.\n"
            "4. Reaction conditions (T, P, H2/feed ratio) dictate activity, selectivity, and catalyst life.\n"
            "5. Catalyst deactivation by coking or metal sintering is mitigated by periodic regeneration.\n"
            "6. Feedstock impurities (e.g., metals, asphaltenes) accelerate deactivation.\n"
            "7. Reactor configuration (fixed-bed, ebullated-bed) impacts heat management and scale-up.\n"
            "8. Product slate is tunable via catalyst formulation and process parameters.\n"
            "9. Environmental regulations drive ultra-low sulfur fuel production.\n"
            "10. Advanced characterization (e.g., STEM, XPS) guides catalyst optimization."
        ),
        key_factors=[
            "Catalyst composition (NiMo, CoMo)",
            "Support acidity and surface area",
            "Operating temperature and pressure",
            "Feedstock impurities",
            "Regeneration protocols"
        ],
        primary_authority=[
            "Speight, J.G. (2014). The Chemistry and Technology of Petroleum.",
            "Ertl, G. et al. (2008). Handbook of Heterogeneous Catalysis.",
            "Song, C. (2003). Catal. Today 86, 211."
        ],
        burden_holder="Refinery Process Engineer",
        adversary_position="Questions catalyst stability and sulfur removal at high throughput.",
        counter_arguments=[
            "Coking rapidly deactivates acid sites.",
            "Feed metals poison active sites.",
            "Hydrogen consumption increases operating cost.",
            "Regeneration may not restore full activity.",
            "Scale-up complicates heat management."
        ],
        resolution_strategy="Optimize catalyst formulation and implement staged reactors with on-line regeneration.",
        entity_scope="Hydroprocessing units",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Speight, 2014; Song, 2003"
    ),
    DoctrineBlock(
        topic="Fluid Catalytic Cracking (FCC): Riser and Regenerator",
        keywords=["FCC", "riser", "regenerator", "cracking", "coke"],
        conclusion_template=(
            "Fluid catalytic cracking (FCC) is a cornerstone of modern refining, converting heavy feedstocks to lighter products. "
            "The riser reactor and regenerator are critical for maintaining catalyst activity and process efficiency."
        ),
        reasoning_framework=(
            "1. FCC employs a circulating catalyst (zeolite-based) between the riser (reaction) and regenerator (coke burn-off) (Gary & Handwerk, 2007).\n"
            "2. In the riser, feed vapor contacts hot catalyst, initiating rapid cracking and isomerization.\n"
            "3. Coke deposition deactivates catalyst, necessitating continuous regeneration in an air-blown vessel.\n"
            "4. Heat balance between riser and regenerator is crucial for stable operation.\n"
            "5. Catalyst formulation (zeolite type, matrix, metals traps) tunes selectivity and coke yield.\n"
            "6. Cyclones and stripper sections minimize catalyst loss and maximize product recovery.\n"
            "7. Emissions control (NOx, SOx, particulates) is a regulatory requirement.\n"
            "8. Advanced diagnostics (e.g., gamma scanning) monitor catalyst circulation and bed inventory.\n"
            "9. Process optimization targets maximum gasoline yield and minimum coke/make-up catalyst.\n"
            "10. Scale-up and revamp projects require detailed hydrodynamic and kinetic modeling."
        ),
        key_factors=[
            "Catalyst formulation and activity",
            "Riser temperature and residence time",
            "Regenerator air rate and temperature",
            "Coke yield and burn-off efficiency",
            "Emissions control"
        ],
        primary_authority=[
            "Gary, J.H. & Handwerk, G.E. (2007). Petroleum Refining: Technology and Economics.",
            "Weitkamp, J. (2000). Solid State Ionics 131, 175.",
            "Song, C. (2003). Catal. Today 86, 211."
        ],
        burden_holder="FCC Unit Engineer",
        adversary_position="Questions catalyst attrition and emissions compliance.",
        counter_arguments=[
            "Catalyst loss increases operating cost.",
            "Incomplete regeneration leads to declining activity.",
            "Emissions limits require costly controls.",
            "Feedstock variability affects product slate.",
            "Hydrodynamic instability risks upsets."
        ],
        resolution_strategy="Implement advanced monitoring and optimize regenerator operation for emissions and catalyst life.",
        entity_scope="FCC units in petroleum refineries",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Gary & Handwerk, 2007; Weitkamp, 2000"
    ),
    DoctrineBlock(
        topic="Haber-Bosch Ammonia Synthesis: Iron Catalyst",
        keywords=["Haber-Bosch", "ammonia", "iron catalyst", "N2 activation", "syngas"],
        conclusion_template=(
            "The Haber-Bosch process synthesizes ammonia from N2 and H2 using promoted iron catalysts under high temperature and pressure. "
            "Catalyst design and process integration are critical for efficiency and longevity."
        ),
        reasoning_framework=(
            "1. Ammonia synthesis is limited by N2 activation, requiring high temperature (400-500°C) and pressure (100-300 bar) (Ertl, 2008).\n"
            "2. Iron catalysts promoted with K, Al2O3, and CaO enhance activity and stability.\n"
            "3. Catalyst operates via dissociative adsorption of N2 and stepwise hydrogenation to NH3.\n"
            "4. Equilibrium conversion is favored by low temperature but rate increases with temperature, necessitating a compromise.\n"
            "5. Reactor design (multi-bed with interstage cooling) manages exothermicity and maximizes yield.\n"
            "6. Feed gas purity (removal of O2, CO, S) is essential to prevent poisoning.\n"
            "7. Catalyst deactivation occurs via sintering and poisoning by trace impurities.\n"
            "8. Process integration with hydrogen production and ammonia separation improves efficiency.\n"
            "9. Advanced kinetic modeling and in situ characterization guide catalyst improvement.\n"
            "10. Life-cycle analysis considers energy input, CO2 emissions, and catalyst recycling."
        ),
        key_factors=[
            "Promoter selection (K, Al2O3, CaO)",
            "Operating temperature and pressure",
            "Feed gas purity",
            "Reactor configuration",
            "Deactivation mechanisms"
        ],
        primary_authority=[
            "Ertl, G. (2008). Handbook of Heterogeneous Catalysis.",
            "Appl, M. (1999). Ammonia: Principles and Industrial Practice.",
            "Schlögl, R. (2003). Angew. Chem. Int. Ed. 42, 2004."
        ],
        burden_holder="Ammonia Plant Engineer",
        adversary_position="Questions energy efficiency and catalyst lifetime.",
        counter_arguments=[
            "High pressure increases capital and operating cost.",
            "Iron catalyst deactivates via sintering.",
            "Trace impurities poison active sites.",
            "Equilibrium limits conversion per pass.",
            "Process is energy intensive."
        ],
        resolution_strategy="Optimize promoter formulation, implement rigorous feed purification, and recycle unreacted gases.",
        entity_scope="Ammonia synthesis plants",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Ertl, 2008; Appl, 1999"
    ),
    DoctrineBlock(
        topic="Catalytic Converter: TWC (Platinum, Palladium, Rhodium)",
        keywords=["catalytic converter", "TWC", "platinum", "palladium", "rhodium"],
        conclusion_template=(
            "Three-way catalytic converters (TWC) employ platinum, palladium, and rhodium to simultaneously oxidize CO and hydrocarbons and reduce NOx. "
            "Precise control of air-fuel ratio and catalyst formulation is essential for emissions compliance."
        ),
        reasoning_framework=(
            "1. TWC function requires stoichiometric air-fuel ratio (λ=1) for simultaneous oxidation and reduction (Shelef & McCabe, 2000).\n"
            "2. Platinum and palladium catalyze CO and hydrocarbon oxidation; rhodium is selective for NOx reduction.\n"
            "3. Oxygen storage components (e.g., CeO2) buffer transient fluctuations in exhaust composition.\n"
            "4. Catalyst washcoat formulation (support, dispersion, promoter) tunes activity and durability.\n"
            "5. Thermal aging and poisoning (e.g., Pb, S, P) degrade catalyst performance over time.\n"
            "6. On-board diagnostics (OBD) monitor catalyst efficiency via lambda sensors.\n"
            "7. Emissions standards (Euro 6, EPA Tier 3) drive continuous improvement in TWC design.\n"
            "8. Advanced characterization (e.g., XPS, TEM) guides material optimization.\n"
            "9. Recycling of spent catalysts recovers precious metals and reduces environmental impact.\n"
            "10. Integration with engine control strategies maximizes conversion efficiency."
        ),
        key_factors=[
            "Precious metal loading and dispersion",
            "Oxygen storage capacity",
            "Thermal stability",
            "Poison resistance",
            "Air-fuel ratio control"
        ],
        primary_authority=[
            "Shelef, M. & McCabe, R.W. (2000). Catal. Today 62, 35.",
            "Ertl, G. et al. (2008). Handbook of Heterogeneous Catalysis.",
            "Twigg, M.V. (2011). Catalytic Control of Emissions."
        ],
        burden_holder="Automotive Emissions Engineer",
        adversary_position="Questions catalyst durability and cost under real-world driving.",
        counter_arguments=[
            "Thermal aging reduces activity.",
            "Poisoning by S, P, Pb is cumulative.",
            "Precious metal cost is high.",
            "Transient operation challenges λ control.",
            "Washcoat adhesion loss at high temperature."
        ],
        resolution_strategy="Optimize washcoat and oxygen storage, and implement advanced engine control for emissions compliance.",
        entity_scope="Automotive exhaust aftertreatment",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Shelef & McCabe, 2000; Twigg, 2011"
    ),
    DoctrineBlock(
        topic="Photocatalysis: TiO2, Band Gap, UV/Visible Activation",
        keywords=["photocatalysis", "TiO2", "band gap", "UV", "visible light"],
        conclusion_template=(
            "Photocatalysis employs semiconductors such as TiO2 to drive chemical transformations using light. "
            "Band gap engineering and surface modification extend activity from UV to visible light."
        ),
        reasoning_framework=(
            "1. TiO2 (anatase, rutile) is a benchmark photocatalyst due to its stability and suitable band gap (3.2 eV for anatase) (Fujishima & Honda, 1972).\n"
            "2. UV irradiation excites electrons from the valence to conduction band, generating electron-hole pairs.\n"
            "3. Surface modification (e.g., doping with N, C, metals) narrows the band gap, enabling visible light activation.\n"
            "4. Charge carrier recombination limits quantum efficiency; strategies include heterojunctions and co-catalysts.\n"
            "5. Photocatalytic activity is assessed via pollutant degradation or H2 evolution under controlled illumination.\n"
            "6. Surface area, crystallinity, and defect density affect performance.\n"
            "7. In situ spectroscopies (e.g., EPR, PL) probe charge carrier dynamics.\n"
            "8. Reactor design (slurry, immobilized) impacts light penetration and mass transfer.\n"
            "9. Stability under irradiation and in real matrices (e.g., wastewater) is critical for application.\n"
            "10. Life-cycle analysis considers energy input and material sustainability."
        ),
        key_factors=[
            "Band gap energy",
            "Surface modification",
            "Charge carrier dynamics",
            "Light intensity and wavelength",
            "Reactor configuration"
        ],
        primary_authority=[
            "Fujishima, A. & Honda, K. (1972). Nature 238, 37.",
            "Henderson, M.A. (2011). Surf. Sci. Rep. 66, 185.",
            "Kudo, A. & Miseki, Y. (2009). Chem. Soc. Rev. 38, 253."
        ],
        burden_holder="Photocatalysis Researcher",
        adversary_position="Questions quantum efficiency and stability under real conditions.",
        counter_arguments=[
            "Charge recombination limits efficiency.",
            "Visible light activity is often low.",
            "Surface modification may reduce stability.",
            "Scaling up is challenging.",
            "Real water matrices contain inhibitors."
        ],
        resolution_strategy="Employ heterojunctions, co-catalysts, and validate in real-world matrices.",
        entity_scope="Photocatalytic reactors (lab to pilot scale)",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Fujishima & Honda, 1972; Kudo & Miseki, 2009"
    ),
    DoctrineBlock(
        topic="Electrocatalysis: HER, OER, ORR, Overpotential",
        keywords=["electrocatalysis", "HER", "OER", "ORR", "overpotential"],
        conclusion_template=(
            "Electrocatalysis underpins energy conversion technologies such as water splitting and fuel cells. "
            "Key reactions include the hydrogen evolution reaction (HER), oxygen evolution reaction (OER), and oxygen reduction reaction (ORR), with overpotential as a critical performance metric."
        ),
        reasoning_framework=(
            "1. HER and OER are central to electrolytic water splitting; ORR is key in fuel cells (Trasatti, 1972).\n"
            "2. Overpotential (η) is the extra potential required above the thermodynamic value to drive the reaction at a given rate.\n"
            "3. Catalyst materials (Pt, IrO2, RuO2, non-precious metals) are selected for activity, stability, and cost.\n"
            "4. Tafel analysis quantifies kinetic parameters and mechanistic insight.\n"
            "5. Electrode structure (surface area, porosity) affects mass transport and catalyst utilization.\n"
            "6. Electrolyte composition (pH, ions) influences reaction pathways and stability.\n"
            "7. Durability testing (chronoamperometry, cycling) assesses long-term performance.\n"
            "8. In situ/operando spectroscopies (e.g., XAS, Raman) probe active sites and intermediates.\n"
            "9. Computational screening accelerates discovery of new electrocatalysts.\n"
            "10. Integration into devices requires scalable synthesis and robust electrode architectures."
        ),
        key_factors=[
            "Overpotential (η)",
            "Catalyst material and loading",
            "Electrode structure",
            "Electrolyte composition",
            "Durability and stability"
        ],
        primary_authority=[
            "Trasatti, S. (1972). J. Electroanal. Chem. 39, 163.",
            "Seh, Z.W. et al. (2017). Science 355, eaad4998.",
            "Nørskov, J.K. et al. (2004). J. Phys. Chem. B 108, 17886."
        ],
        burden_holder="Electrochemical Engineer",
        adversary_position="Questions catalyst stability and cost for large-scale deployment.",
        counter_arguments=[
            "Precious metals are expensive.",
            "Non-precious catalysts may lack durability.",
            "Mass transport limitations at high current.",
            "Electrolyte degradation affects stability.",
            "Scale-up of nanostructured catalysts is challenging."
        ],
        resolution_strategy="Develop non-precious, robust catalysts and validate with long-term durability testing.",
        entity_scope="Electrolyzers and fuel cells",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Trasatti, 1972; Seh et al., 2017"
    ),
    DoctrineBlock(
        topic="Biocatalysis: Immobilized Enzymes and Whole Cells",
        keywords=["biocatalysis", "immobilization", "whole cell", "enzyme", "carrier"],
        conclusion_template=(
            "Biocatalysis leverages immobilized enzymes or whole cells for selective transformations. "
            "Immobilization enhances stability and reusability, while whole-cell systems enable cofactor regeneration."
        ),
        reasoning_framework=(
            "1. Enzyme immobilization on carriers (e.g., resins, silica, polymers) enhances operational stability (Sheldon & van Pelt, 2013).\n"
            "2. Immobilization methods include adsorption, covalent binding, entrapment, and encapsulation.\n"
            "3. Whole-cell biocatalysis provides native cofactor regeneration and metabolic pathways.\n"
            "4. Mass transfer limitations may arise due to carrier porosity or cell wall permeability.\n"
            "5. Reactor design (packed-bed, fluidized-bed) impacts productivity and scale-up.\n"
            "6. Immobilized systems facilitate enzyme recovery and continuous operation.\n"
            "7. Enzyme leaching and carrier degradation are potential drawbacks.\n"
            "8. Cofactor recycling (e.g., NADH/NAD+) is critical for redox reactions.\n"
            "9. Genetic engineering can enhance cell robustness or expand substrate scope.\n"
            "10. Regulatory and safety considerations apply for whole-cell processes."
        ),
        key_factors=[
            "Immobilization method",
            "Carrier properties",
            "Mass transfer limitations",
            "Cofactor regeneration",
            "Reactor configuration"
        ],
        primary_authority=[
            "Sheldon, R.A. & van Pelt, S. (2013). Chem. Soc. Rev. 42, 6223.",
            "Bornscheuer, U.T. (2012). Enzyme Catalysis in Organic Synthesis.",
            "Liese, A. et al. (2006). Industrial Biotransformations."
        ],
        burden_holder="Bioprocess Engineer",
        adversary_position="Questions mass transfer and enzyme leaching in immobilized systems.",
        counter_arguments=[
            "Carrier porosity limits substrate diffusion.",
            "Enzyme leaching reduces operational stability.",
            "Whole-cell systems may have side reactions.",
            "Cofactor cost is high without recycling.",
            "Carrier degradation over time."
        ],
        resolution_strategy="Optimize carrier selection, implement cofactor recycling, and validate with pilot-scale operation.",
        entity_scope="Biocatalytic reactors (immobilized and whole-cell)",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Sheldon & van Pelt, 2013; Liese et al., 2006"
    ),
    DoctrineBlock(
        topic="Catalyst Selectivity, Conversion, Yield, TON, TOF",
        keywords=["selectivity", "conversion", "yield", "TON", "TOF"],
        conclusion_template=(
            "Catalyst performance is quantified by selectivity, conversion, yield, turnover number (TON), and turnover frequency (TOF). "
            "Optimizing these metrics is essential for economic and sustainable catalysis."
        ),
        reasoning_framework=(
            "1. Conversion is the fraction of reactant transformed; selectivity is the fraction converted to desired product (Fogler, 2016).\n"
            "2. Yield combines conversion and selectivity, reflecting process efficiency.\n"
            "3. TON is the number of moles of product per mole of active site; TOF is TON per unit time.\n"
            "4. High selectivity reduces separation cost and waste generation.\n"
            "5. Reaction conditions (T, P, feed ratio) influence all metrics.\n"
            "6. Catalyst deactivation lowers conversion and selectivity over time.\n"
            "7. Side reactions and product inhibition may reduce yield.\n"
            "8. Accurate quantification requires rigorous material balances and analytical methods.\n"
            "9. Process optimization balances activity, selectivity, and stability.\n"
            "10. Life-cycle and sustainability metrics (E-factor, atom economy) complement traditional performance indicators."
        ),
        key_factors=[
            "Reaction conditions",
            "Catalyst stability",
            "Product analysis accuracy",
            "Side reactions",
            "Material balance closure"
        ],
        primary_authority=[
            "Fogler, H.S. (2016). Elements of Chemical Reaction Engineering.",
            "Sheldon, R.A. (2012). Green Chem. 14, 1480.",
            "Levenspiel, O. (1999). Chemical Reaction Engineering."
        ],
        burden_holder="Process Analyst",
        adversary_position="Questions accuracy of selectivity and yield measurements.",
        counter_arguments=[
            "Incomplete material balance skews metrics.",
            "Product losses in separation not accounted.",
            "Catalyst deactivation alters performance.",
            "Side products complicate analysis.",
            "Analytical error in product quantification."
        ],
        resolution_strategy="Implement rigorous analytical protocols and periodic catalyst re-evaluation.",
        entity_scope="All catalytic processes",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Fogler, 2016; Sheldon, 2012"
    ),
    DoctrineBlock(
        topic="Mass Transfer Limitations: Thiele Modulus and Effectiveness Factor",
        keywords=["mass transfer", "Thiele modulus", "effectiveness factor", "diffusion", "external transport"],
        conclusion_template=(
            "Mass transfer limitations (internal and external) can mask intrinsic catalytic activity. "
            "The Thiele modulus and effectiveness factor quantify the impact of diffusion on observed rates."
        ),
        reasoning_framework=(
            "1. External mass transfer refers to transport from bulk fluid to catalyst surface; internal refers to diffusion within catalyst pores (Levenspiel, 1999).\n"
            "2. The Thiele modulus (ϕ) compares reaction rate to diffusion rate inside catalyst particles.\n"
            "3. Effectiveness factor (η) is the ratio of observed to intrinsic rate; η < 1 indicates diffusion limitation.\n"
            "4. Large catalyst particles or high reaction rates increase diffusion limitations.\n"
            "5. Experimental tests (e.g., varying particle size, stirring rate) diagnose transport limitations.\n"
            "6. Mathematical models (Weisz-Prater criterion) provide quantitative assessment.\n"
            "7. Reactor design (e.g., slurry, fixed-bed) affects the prevalence of mass transfer effects.\n"
            "8. Catalyst design (hierarchical porosity) can mitigate internal diffusion resistance.\n"
            "9. Accurate kinetic modeling requires ruling out mass transfer limitations.\n"
            "10. Scale-up must preserve hydrodynamics to avoid unexpected transport effects."
        ),
        key_factors=[
            "Particle size and porosity",
            "Stirring/agitation rate",
            "Reaction rate vs. diffusion rate",
            "Reactor configuration",
            "Diagnostic experiments"
        ],
        primary_authority=[
            "Levenspiel, O. (1999). Chemical Reaction Engineering.",
            "Fogler, H.S. (2016). Elements of Chemical Reaction Engineering.",
            "Weisz, P.B. & Prater, C.D. (1954). Adv. Catal. 6, 143."
        ],
        burden_holder="Process Kineticist",
        adversary_position="Questions whether observed kinetics are truly intrinsic.",
        counter_arguments=[
            "Diffusion limitations mask catalyst performance.",
            "Particle size effects not accounted for.",
            "Hydrodynamics differ at scale.",
            "Diagnostic tests may be inconclusive.",
            "Porosity characterization may be incomplete."
        ],
        resolution_strategy="Apply Weisz-Prater and Thiele modulus analysis, and validate with particle size variation.",
        entity_scope="All catalytic reactors",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Levenspiel, 1999; Weisz & Prater, 1954"
    ),
    DoctrineBlock(
        topic="Catalyst Regeneration: Oxidative and Reductive Methods",
        keywords=["regeneration", "oxidative", "reductive", "coke removal", "activity recovery"],
        conclusion_template=(
            "Catalyst regeneration restores activity lost to coking, poisoning, or sintering. "
            "Oxidative and reductive methods are tailored to catalyst type and deactivation mechanism."
        ),
        reasoning_framework=(
            "1. Oxidative regeneration (air, O2) removes coke via combustion, restoring active sites (Bartholomew, 2001).\n"
            "2. Reductive regeneration (H2, CO) reactivates metal sites poisoned by sulfur or oxygenates.\n"
            "3. Regeneration conditions (T, P, gas composition) must avoid catalyst sintering or structural collapse.\n"
            "4. In situ regeneration minimizes downtime but may require process integration.\n"
            "5. Off-line regeneration allows for more aggressive conditions but increases operational complexity.\n"
            "6. Monitoring (TGA, off-gas analysis) ensures complete coke removal and prevents hot spots.\n"
            "7. Multiple regeneration cycles may degrade catalyst structure or dispersion.\n"
            "8. Additives (e.g., steam, promoters) can enhance regeneration efficacy.\n"
            "9. Economic analysis weighs catalyst replacement vs. regeneration cost.\n"
            "10. Environmental controls are required for emissions during regeneration."
        ),
        key_factors=[
            "Type of deactivation (coke, poison, sintering)",
            "Regeneration protocol (oxidative/reductive)",
            "Temperature and atmosphere control",
            "Cycle frequency and duration",
            "Monitoring and safety"
        ],
        primary_authority=[
            "Bartholomew, C.H. (2001). Appl. Catal. A 212, 17.",
            "Ertl, G. et al. (2008). Handbook of Heterogeneous Catalysis.",
            "Song, C. (2003). Catal. Today 86, 211."
        ],
        burden_holder="Operations Manager",
        adversary_position="Questions long-term catalyst stability after repeated regeneration.",
        counter_arguments=[
            "Regeneration may induce sintering.",
            "Incomplete coke removal reduces activity.",
            "Poison removal may be irreversible.",
            "Structural collapse after multiple cycles.",
            "Emissions during regeneration require controls."
        ],
        resolution_strategy="Optimize regeneration conditions and monitor catalyst structure after each cycle.",
        entity_scope="All industrial catalytic processes",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Bartholomew, 2001; Song, 2003"
    ),
    DoctrineBlock(
        topic="Green Chemistry: Atom Economy and E-Factor",
        keywords=["green chemistry", "atom economy", "E-factor", "sustainability", "waste"],
        conclusion_template=(
            "Green chemistry principles prioritize atom economy and minimize E-factor to reduce waste and improve sustainability. "
            "Catalytic processes are central to achieving these goals in industrial chemistry."
        ),
        reasoning_framework=(
            "1. Atom economy measures the fraction of reactant atoms incorporated into the desired product (Trost, 1991).\n"
            "2. E-factor quantifies the mass of waste per mass of product, guiding process optimization (Sheldon, 1997).\n"
            "3. Catalysis enhances atom economy by enabling selective transformations with minimal byproducts.\n"
            "4. Process intensification (e.g., tandem catalysis, flow chemistry) further reduces waste.\n"
            "5. Life-cycle analysis considers energy, water, and raw material inputs.\n"
            "6. Regulatory and market pressures drive adoption of green metrics.\n"
            "7. Catalyst recovery and recycling reduce environmental impact.\n"
            "8. Renewable feedstocks (biomass, CO2) improve sustainability.\n"
            "9. Metrics must be balanced with economic and technical feasibility.\n"
            "10. Continuous improvement is required to meet evolving sustainability targets."
        ),
        key_factors=[
            "Atom economy",
            "E-factor",
            "Catalyst recovery",
            "Renewable feedstocks",
            "Life-cycle analysis"
        ],
        primary_authority=[
            "Trost, B.M. (1991). Science 254, 1471.",
            "Sheldon, R.A. (1997). Chem. Ind. 1, 12.",
            "Anastas, P.T. & Warner, J.C. (1998). Green Chemistry: Theory and Practice."
        ],
        burden_holder="Sustainability Officer",
        adversary_position="Questions trade-offs between green metrics and process economics.",
        counter_arguments=[
            "High atom economy may require costly catalysts.",
            "E-factor does not account for toxicity.",
            "Catalyst recovery may be energy intensive.",
            "Renewable feedstocks may be less efficient.",
            "Life-cycle data may be incomplete."
        ],
        resolution_strategy="Integrate green metrics with techno-economic analysis and prioritize continuous improvement.",
        entity_scope="All catalytic processes",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Trost, 1991; Sheldon, 1997"
    ),
    # ... (Add at least 10 more DoctrineBlocks for full 30+ coverage)
]

# =========================
# AUTHORITY HARDENING
# =========================

AUTHORITY_WEIGHTS = {
    "Handbook of Heterogeneous Catalysis": 1.0,
    "Levenspiel, 1999": 0.95,
    "Fogler, 2016": 0.95,
    "Bartholomew, 2001": 0.93,
    "Ertl, 2008": 0.97,
    "Brunauer et al., 1938": 0.92,
    "Corma, 1997": 0.91,
    "Sheldon, 2012": 0.90,
    "Trost, 1991": 0.90,
    "Sheldon & van Pelt, 2013": 0.89,
    "Michaelis & Menten, 1913": 0.94,
    "Wilkinson, 1966": 0.92,
    "Grubbs & Trnka, 2001": 0.92,
    "Dry, 2002": 0.91,
    "Appl, 1999": 0.91,
    "Song, 2003": 0.90,
    "Shelef & McCabe, 2000": 0.90,
    "Weisz & Prater, 1954": 0.90,
    "Anastas & Warner, 1998": 0.89,
    "Twice-cited": 0.88
}

def resolve_authority_conflict(authorities: List[str]) -> Tuple[str, float]:
    max_weight = -1
    best_auth = ""
    for auth in authorities:
        for k, w in AUTHORITY_WEIGHTS.items():
            if k in auth and w > max_weight:
                max_weight = w
                best_auth = auth
    return best_auth, max_weight if max_weight > 0 else 0.85

# =========================
# SEMANTIC NORMALIZATION
# =========================

SEMANTIC_MAP = {
    "BET": "Brunauer–Emmett–Teller method",
    "XRD": "X-ray diffraction",
    "TPR": "Temperature-programmed reduction",
    "TPD": "Temperature-programmed desorption",
    "XPS": "X-ray photoelectron spectroscopy",
    "FCC": "Fluid catalytic cracking",
    "HDS": "Hydrodesulfurization",
    "TON": "Turnover number",
    "TOF": "Turnover frequency",
    "HER": "Hydrogen evolution reaction",
    "OER": "Oxygen evolution reaction",
    "ORR": "Oxygen reduction reaction",
    "ASF": "Anderson-Schulz-Flory distribution",
    "CSTR": "Continuous stirred-tank reactor",
    "PFR": "Plug flow reactor",
    "NH3-TPD": "Ammonia temperature-programmed desorption",
    "CeO2": "Cerium dioxide",
    "NHC": "N-heterocyclic carbene",
    "DFT": "Density functional theory",
    "KIE": "Kinetic isotope effect",
    "DRIFTS": "Diffuse reflectance infrared Fourier transform spectroscopy",
    "STEM": "Scanning transmission electron microscopy",
    "EXAFS": "Extended X-ray absorption fine structure",
    "MAS NMR": "Magic angle spinning nuclear magnetic resonance",
    "EPR": "Electron paramagnetic resonance",
    "PL": "Photoluminescence",
    "CFD": "Computational fluid dynamics",
    "OBD": "On-board diagnostics",
    "λ": "Air-fuel equivalence ratio",
    "E-factor": "Environmental factor",
    "Si/Al": "Silicon-to-aluminum ratio",
    "pH": "Potential of hydrogen"
}

def semantic_normalize(text: str) -> str:
    for k, v in SEMANTIC_MAP.items():
        text = text.replace(k, v)
    return text

# =========================
# EPISTEMIC GUARDRAILS
# =========================

BANNED_PHRASES = [
    "always", "never", "guaranteed", "impossible", "no risk", "foolproof", "perfect", "certainly", "all cases", "without exception"
]

def apply_epistemic_guardrails(text: str) -> str:
    for phrase in BANNED_PHRASES:
        text = text.replace(phrase, "[epistemic-guardrail-redacted]")
    return text

# =========================
# FACT FRAGILITY SCORING
# =========================

def score_fact_fragility(block: DoctrineBlock) -> Dict[str, float]:
    verifiability = 0.8 + 0.2 * (len(block.primary_authority) / 5)
    recharacterization_risk = 1.0 - block.confidence
    testimony_dependence = 0.2 + 0.1 * (block.reasoning_framework.count("in situ") + block.reasoning_framework.count("pilot-scale"))
    return {
        "verifiability": min(verifiability, 1.0),
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": min(testimony_dependence, 1.0)
    }

# =========================
# THREE-LAYER RESPONSE
# =========================

def doctrine_layer(query: QueryRequest) -> Optional[DoctrineBlock]:
    q = query.scenario.lower()
    for block in DOCTRINE_CACHE:
        if any(k.lower() in q for k in block.keywords):
            return block
    return None

def semantic_search_layer(query: QueryRequest) -> Optional[DoctrineBlock]:
    q = query.scenario.lower()
    best_score = 0
    best_block = None
    for block in DOCTRINE_CACHE:
        score = sum(1 for k in block.keywords if k.lower() in q)
        if score > best_score:
            best_score = score
            best_block = block
    return best_block

def deep_analysis_layer(query: QueryRequest) -> Optional[DoctrineBlock]:
    # Multi-doctrine decomposition and issue category mapping
    q = query.scenario.lower()
    hits = []
    for block in DOCTRINE_CACHE:
        if any(k.lower() in q for k in block.keywords):
            hits.append(block)
    if not hits:
        return None
    # Select the block with highest confidence
    hits.sort(key=lambda b: b.confidence, reverse=True)
    return hits[0]

def multi_doctrine_decomposition(query: QueryRequest) -> List[DoctrineBlock]:
    q = query.scenario.lower()
    return [block for block in DOCTRINE_CACHE if any(k.lower() in q for k in block.keywords)]

def interaction_dag(blocks: List[DoctrineBlock]) -> Dict[str, List[str]]:
    dag = {}
    for block in blocks:
        dag[block.topic] = [b.topic for b in blocks if b != block and set(block.keywords) & set(b.keywords)]
    return dag

def eight_step_resolution(blocks: List[DoctrineBlock]) -> str:
    steps = [
        "1. Identify relevant doctrines.",
        "2. Map scenario to doctrine keywords.",
        "3. Assess authority hierarchy and conflicts.",
        "4. Score fact fragility for each doctrine.",
        "5. Analyze interaction DAG for dependencies.",
        "6. Synthesize primary conclusion with epistemic guardrails.",
        "7. Resolve counter-arguments and adversary positions.",
        "8. Propose actionable resolution strategy."
    ]
    return "\n".join(steps)

# =========================
# COVERAGE MAP
# =========================

def coverage_map(query: QueryRequest, doctrine_hits: List[DoctrineBlock]) -> Dict[str, Any]:
    triggered = [b.topic for b in doctrine_hits]
    missed = [b.topic for b in DOCTRINE_CACHE if b not in doctrine_hits]
    epistemic_gap = len(triggered) == 0
    return {
        "triggered": triggered,
        "missed": missed,
        "epistemic_gap": epistemic_gap
    }

# =========================
# DRIFT WATCHER
# =========================

DRIFT_BASELINE = {block.topic: block.confidence for block in DOCTRINE_CACHE}

def detect_drift() -> Dict[str, Any]:
    drifted = []
    for block in DOCTRINE_CACHE:
        baseline = DRIFT_BASELINE.get(block.topic, block.confidence)
        if abs(block.confidence - baseline) > 0.05:
            drifted.append(block.topic)
    return {
        "drifted": drifted,
        "baseline": DRIFT_BASELINE
    }

# =========================
# AUDIT TRAIL
# =========================

AUDIT_LOG_PATH = Path(__file__).parent / "audit_log.jsonl"

def log_audit(query_id: str, request: QueryRequest, response: QueryResponse):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "query_id": query_id,
        "request": request.dict(),
        "response": response.dict()
    }
    try:
        with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(str(entry) + "\n")
    except Exception as e:
        logger.error(f"Audit log write failed: {e}")

# =========================
# DETERMINISM HASH
# =========================

def determinism_hash(response: QueryResponse) -> str:
    m = hashlib.sha256()
    m.update(response.primary_conclusion.encode("utf-8"))
    m.update(response.reasoning_framework.encode("utf-8"))
    m.update("".join(response.key_factors).encode("utf-8"))
    m.update("".join(response.primary_authority).encode("utf-8"))
    m.update("".join(response.counter_arguments).encode("utf-8"))
    m.update(response.resolution_strategy.encode("utf-8"))
    m.update(str(response.confidence).encode("utf-8"))
    m.update(response.confidence_zone.value.encode("utf-8"))
    m.update(response.position_zone.value.encode("utf-8"))
    return m.hexdigest()

# =========================
# FASTAPI APP
# =========================

app = FastAPI(title="Catalysis & Reaction Engineering Engine (CHEM16)", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def startup_event():
    logger.info("CHEM16 Engine started.")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("CHEM16 Engine stopped.")

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    query_id = str(uuid.uuid4())
    start_time = datetime.utcnow()
    try:
        # Three-layer response
        block = doctrine_layer(request)
        if not block:
            block = semantic_search_layer(request)
        if not block:
            block = deep_analysis_layer(request)
        if not block:
            # Fallback: select highest-confidence doctrine
            block = max(DOCTRINE_CACHE, key=lambda b: b.confidence)
        # Multi-doctrine for coverage
        doctrine_hits = multi_doctrine_decomposition(request)
        # Authority hardening
        primary_authority, _ = resolve_authority_conflict(block.primary_authority)
        # Semantic normalization and epistemic guardrails
        conclusion = semantic_normalize(block.conclusion_template)
        conclusion = apply_epistemic_guardrails(conclusion)
        reasoning = semantic_normalize(block.reasoning_framework)
        reasoning = apply_epistemic_guardrails(reasoning)
        # Fact fragility scoring
        fragility = score_fact_fragility(block)
        # Position zone tagging
        if request.complexity >= 4:
            position_zone = PositionZone.AUDIT
        elif request.complexity == 3:
            position_zone = PositionZone.REPORTING
        else:
            position_zone = PositionZone.PLANNING
        # Determinism hash
        response = QueryResponse(
            engine_id="CHEM16",
            query_id=query_id,
            mode=request.mode,
            confidence=block.confidence,
            confidence_zone=block.confidence_zone,
            position_zone=position_zone,
            primary_conclusion=conclusion,
            reasoning_framework=reasoning,
            key_factors=block.key_factors,
            primary_authority=block.primary_authority,
            counter_arguments=block.counter_arguments,
            resolution_strategy=block.resolution_strategy,
            determinism_hash=""
        )
        response.determinism_hash = determinism_hash(response)
        # Metrics and audit
        latency = (datetime.utcnow() - start_time).total_seconds()
        metrics_collector.record_query(query_id, [b.topic for b in doctrine_hits], latency)
        log_audit(query_id, request, response)
        return response
    except Exception as e:
        logger.error(f"Query error: {e}")
        metrics_collector.record_error(query_id, str(e))
        raise

@app.get("/health")
async def health():
    return {"status": "ok", "engine_id": "CHEM16"}

@app.get("/metrics")
async def metrics():
    return {
        "latency_stats": metrics_collector.get_latency_stats(),
        "doctrine_hit_rate": metrics_collector.get_doctrine_hit_rate(),
        "queries_last_hour": metrics_collector.queries_last_hour()
    }

@app.get("/coverage")
async def coverage(request: Request):
    # Simulate coverage for a sample query
    sample_query = QueryRequest(
        scenario="Effect of mass transfer limitations in fixed-bed reactors",
        mode=ResponseMode.FAST,
        entity_type="heterogeneous catalyst",
        complexity=3
    )
    doctrine_hits = multi_doctrine_decomposition(sample_query)
    return coverage_map(sample_query, doctrine_hits)

@app.get("/drift")
async def drift():
    return detect_drift()

@app.get("/doctrines")
async def doctrines():
    return [block.topic for block in DOCTRINE_CACHE]
