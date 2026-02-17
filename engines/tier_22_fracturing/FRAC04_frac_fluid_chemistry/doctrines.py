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
        topic="Anionic Friction Reducers in Slickwater Fracs",
        keywords=["anionic", "friction reducer", "slickwater", "polyacrylamide", "viscosity", "drag reduction", "polymer", "frac fluid"],
        conclusion_template="Anionic polyacrylamide friction reducers are the preferred choice for slickwater fracturing fluids in low to moderate TDS water due to their high drag reduction efficiency and cost-effectiveness.",
        reasoning_framework=(
            "Anionic friction reducers, primarily polyacrylamide-based, are widely used in slickwater hydraulic fracturing due to their ability to reduce pipe friction and allow higher pump rates. Their performance depends on water quality, especially total dissolved solids (TDS), hardness, and presence of multivalent cations. In low to moderate TDS (<10,000 mg/L), anionic FRs provide optimal viscosity and drag reduction. However, in high TDS or high hardness brines, their efficiency decreases due to charge neutralization and precipitation. Selection should also consider compatibility with other additives and proppant transport requirements. Regulatory acceptance and field-proven performance further support their use."
        ),
        key_factors=[
            "Water TDS and hardness",
            "Polymer molecular weight and charge density",
            "Compatibility with other additives",
            "Field performance data",
            "Cost per treated barrel"
        ],
        primary_authority=[
            "SPE 115866 - Friction Reducer Chemistry and Application",
            "API RP 19C - Measurement of Properties of Proppants Used in Hydraulic Fracturing"
        ],
        burden_holder="Frac fluid designer",
        adversary_position="Cationic or nonionic friction reducers are superior in all water types.",
        counter_arguments=[
            "Anionic FRs outperform in low to moderate TDS water.",
            "Cationic FRs are more expensive and may have environmental concerns.",
            "Nonionic FRs are less effective in drag reduction at low doses."
        ],
        resolution_strategy="Select anionic FRs for TDS <10,000 mg/L, validate with lab drag reduction tests, and confirm field performance.",
        entity_scope="Frac fluid chemistry teams, completions engineers",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Field data from major US shale basins (Permian, Marcellus)"
    ),
    DoctrineBlock(
        topic="Cationic Friction Reducers for High-Hardness Brines",
        keywords=["cationic", "friction reducer", "high hardness", "brine", "polyDADMAC", "drag reduction", "compatibility"],
        conclusion_template="Cationic friction reducers are recommended for use in high-hardness brines where anionic FRs lose effectiveness due to precipitation with divalent cations.",
        reasoning_framework=(
            "Cationic friction reducers, such as polyDADMAC and quaternary ammonium polymers, maintain drag reduction performance in high-hardness brines (Ca2+, Mg2+ > 1,000 mg/L) where anionic FRs precipitate. Their positive charge prevents neutralization by divalent cations, ensuring solubility and efficacy. However, cationic FRs may be less compatible with anionic additives (e.g., scale inhibitors) and can pose higher environmental risks due to aquatic toxicity. Selection should balance performance, regulatory constraints, and cost. Lab jar testing and field trials are essential for validation."
        ),
        key_factors=[
            "Brine hardness (Ca2+, Mg2+ concentration)",
            "Compatibility with other additives",
            "Environmental regulations",
            "Cost and supply chain",
            "Field trial data"
        ],
        primary_authority=[
            "SPE 169123 - High-Hardness Brine Friction Reducer Evaluation",
            "API RP 13B-1 - Standard Procedures for Testing Drilling Fluids"
        ],
        burden_holder="Frac fluid chemist",
        adversary_position="Anionic FRs can be used in any brine with sufficient overdosing.",
        counter_arguments=[
            "Overdosing anionic FRs leads to excessive cost and potential formation damage.",
            "Cationic FRs are specifically engineered for high-hardness environments.",
            "Compatibility and environmental impact must be managed."
        ],
        resolution_strategy="Use cationic FRs in high-hardness brines, confirm with lab and field performance tests, and ensure regulatory compliance.",
        entity_scope="Frac fluid chemistry, regulatory compliance",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Permian Basin field trials, Texas Railroad Commission guidelines"
    ),
    DoctrineBlock(
        topic="Borate-Crosslinked Guar Gel Systems",
        keywords=["borate", "crosslinked", "guar", "gel", "viscosity", "high temperature", "proppant transport"],
        conclusion_template="Borate-crosslinked guar gels are the industry standard for high-viscosity fracturing fluids in moderate-temperature reservoirs (120-250°F), providing excellent proppant transport and clean-up.",
        reasoning_framework=(
            "Borate-crosslinked guar gels are formed by adding borate ions to hydrated guar polymer, creating a reversible crosslinked network that imparts high viscosity and elasticity. This system is optimal for proppant transport, leakoff control, and fracture width maintenance in moderate-temperature reservoirs. The crosslinking is pH-dependent (optimal at pH 9-10.5) and reversible, aiding in fluid clean-up with breakers. Limitations include sensitivity to low pH, boron precipitation at high TDS, and residue formation if not properly broken. Field experience and lab rheology data support their widespread use."
        ),
        key_factors=[
            "Reservoir temperature",
            "pH control",
            "Water quality (TDS, boron content)",
            "Breaker selection",
            "Proppant loading"
        ],
        primary_authority=[
            "SPE 56538 - Guar and Guar Derivatives in Hydraulic Fracturing",
            "API RP 39 - Recommended Practice for Fracturing Fluids"
        ],
        burden_holder="Frac fluid designer",
        adversary_position="Linear gels or VES fluids can replace borate-crosslinked systems in all cases.",
        counter_arguments=[
            "Borate-crosslinked gels provide superior viscosity and proppant transport.",
            "Linear gels are inadequate for high proppant loads.",
            "VES fluids are costlier and less robust at high temperatures."
        ],
        resolution_strategy="Select borate-crosslinked guar for 120-250°F, ensure pH and water quality control, and optimize breaker dosage.",
        entity_scope="Frac fluid chemistry, completions engineering",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 39, major US shale field data"
    ),
    DoctrineBlock(
        topic="Zirconate and Titanate Crosslinkers for High-Temp Gels",
        keywords=["zirconate", "titanate", "crosslinker", "high temperature", "guar", "CMHPG", "viscosity"],
        conclusion_template="Zirconate and titanate crosslinkers are preferred for crosslinking guar and CMHPG fluids in high-temperature (>250°F) fracturing applications due to their thermal stability.",
        reasoning_framework=(
            "Zirconate and titanate crosslinkers form stable, covalent bonds with guar and carboxymethyl hydroxypropyl guar (CMHPG) polymers, resulting in high-viscosity gels that withstand elevated temperatures (>250°F). These crosslinkers are less sensitive to pH and water quality than borate systems and provide extended viscosity retention under shear. However, they require precise dosage control to avoid over-crosslinking and potential formation damage. Compatibility with breakers and other additives must be verified. Field and lab data confirm their effectiveness in deep, hot reservoirs."
        ),
        key_factors=[
            "Reservoir temperature",
            "Polymer type and concentration",
            "Crosslinker dosage",
            "Shear stability",
            "Breaker compatibility"
        ],
        primary_authority=[
            "SPE 121686 - High-Temperature Crosslinker Chemistry",
            "API RP 39"
        ],
        burden_holder="Frac fluid chemist",
        adversary_position="Borate crosslinkers are sufficient for all temperatures.",
        counter_arguments=[
            "Borate systems degrade above 250°F.",
            "Zirconate/titanate crosslinkers provide superior thermal stability.",
            "Field failures with borate at high temperature are documented."
        ],
        resolution_strategy="Use zirconate/titanate crosslinkers for >250°F, validate with lab rheology and field pilot tests.",
        entity_scope="Frac fluid chemistry, completions engineering",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Deep gas and geothermal field applications"
    ),
    DoctrineBlock(
        topic="Hybrid Frac Design - Slickwater and Gel Stages",
        keywords=["hybrid", "frac design", "slickwater", "gel", "stages", "proppant", "transition", "efficiency"],
        conclusion_template="Hybrid frac designs combining slickwater and gel stages optimize proppant placement and minimize fluid costs in unconventional reservoirs.",
        reasoning_framework=(
            "Hybrid fracturing designs alternate between slickwater (low-viscosity, high-rate) and gel (high-viscosity, lower-rate) stages. Slickwater stages enhance fracture complexity and reduce fluid costs, while gel stages improve proppant transport and placement in wider fractures. The transition timing and stage sequencing are critical for maximizing conductivity and minimizing screen-outs. Design must consider reservoir characteristics, proppant type, and operational constraints. Field studies show improved production and operational efficiency with hybrid approaches."
        ),
        key_factors=[
            "Reservoir permeability and closure stress",
            "Stage sequencing and timing",
            "Proppant type and concentration",
            "Fluid cost and logistics",
            "Operational constraints"
        ],
        primary_authority=[
            "SPE 140185 - Hybrid Fracturing in Shale Reservoirs",
            "API RP 19C"
        ],
        burden_holder="Completions engineer",
        adversary_position="Pure slickwater or pure gel is always superior.",
        counter_arguments=[
            "Hybrid designs balance cost and proppant placement.",
            "Pure slickwater may result in poor proppant transport.",
            "Pure gel increases fluid cost and may reduce fracture complexity."
        ],
        resolution_strategy="Design hybrid stages based on reservoir and operational data, validate with post-frac production analysis.",
        entity_scope="Completions engineering, frac design teams",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Marcellus and Permian hybrid frac case studies"
    ),
    DoctrineBlock(
        topic="Viscoelastic Surfactant (VES) Fluids",
        keywords=["viscoelastic", "surfactant", "VES", "polymer-free", "clean fluid", "frac", "gel"],
        conclusion_template="Viscoelastic surfactant (VES) fluids are recommended for polymer-free fracturing in sensitive formations where residue-free flowback is critical.",
        reasoning_framework=(
            "VES fluids form micellar structures that impart viscosity and elasticity without using polymers. They are ideal for water-sensitive or low-permeability formations where polymer residue could cause damage. VES fluids are easily broken with hydrocarbons or brines, ensuring clean flowback. However, they are more expensive than guar-based systems and may have limited viscosity at high temperature or high shear. Compatibility with other additives and formation fluids must be verified. Field applications confirm their value in high-value, damage-sensitive wells."
        ),
        key_factors=[
            "Formation sensitivity to residue",
            "Temperature and shear conditions",
            "Cost constraints",
            "Additive compatibility",
            "Flowback requirements"
        ],
        primary_authority=[
            "SPE 71696 - VES Fluids in Hydraulic Fracturing",
            "API RP 39"
        ],
        burden_holder="Frac fluid designer",
        adversary_position="Polymer-based fluids are always preferable due to cost.",
        counter_arguments=[
            "VES fluids eliminate polymer residue and associated damage.",
            "Cost is justified in high-value or damage-sensitive wells.",
            "Polymer-based fluids may impair permeability."
        ],
        resolution_strategy="Select VES fluids for sensitive formations, confirm with lab compatibility and cost-benefit analysis.",
        entity_scope="Frac fluid chemistry, completions engineering",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="Gulf of Mexico and Middle East VES frac projects"
    ),
    DoctrineBlock(
        topic="Enzyme Breakers for Guar-Based Fluids",
        keywords=["enzyme breaker", "guar", "polymer", "fluid clean-up", "breakdown", "residue"],
        conclusion_template="Enzyme breakers are preferred for breaking guar-based fracturing fluids in moderate-temperature wells, minimizing residue and formation damage.",
        reasoning_framework=(
            "Enzyme breakers specifically target the glycosidic bonds in guar polymers, enabling efficient viscosity reduction and minimizing insoluble residue. They are most effective in moderate-temperature wells (100-180°F) and are less aggressive than oxidizer breakers, reducing risk of over-breaking and premature viscosity loss. Enzyme activity is pH and temperature dependent; thus, formulation must ensure optimal conditions for enzyme function. Field and lab data show improved clean-up and production compared to oxidizer-only systems."
        ),
        key_factors=[
            "Well temperature",
            "pH control",
            "Enzyme stability",
            "Polymer concentration",
            "Desired break profile"
        ],
        primary_authority=[
            "SPE 56798 - Enzyme Breakers for Fracturing Fluids",
            "API RP 39"
        ],
        burden_holder="Frac fluid chemist",
        adversary_position="Oxidizer breakers are always more effective.",
        counter_arguments=[
            "Enzymes minimize residue and are less aggressive.",
            "Oxidizers may cause over-breaking and formation damage.",
            "Enzymes are more selective and environmentally friendly."
        ],
        resolution_strategy="Use enzyme breakers for moderate temperatures, ensure pH and temperature control, and validate with residue analysis.",
        entity_scope="Frac fluid chemistry, completions engineering",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="US shale field data, API RP 39"
    ),
    DoctrineBlock(
        topic="Oxidizer Breakers - Persulfate and Peroxide Systems",
        keywords=["oxidizer breaker", "persulfate", "peroxide", "guar", "polymer", "breakdown", "high temperature"],
        conclusion_template="Oxidizer breakers such as persulfate and peroxide are recommended for rapid and complete breaking of guar-based fluids in high-temperature wells.",
        reasoning_framework=(
            "Oxidizer breakers generate free radicals that cleave guar polymer chains, rapidly reducing viscosity. Persulfate is commonly used for high-temperature wells (>150°F), while peroxide is effective at lower temperatures or when rapid break is needed. Dosage must be carefully controlled to avoid premature break and potential formation damage. Compatibility with crosslinkers and other additives is essential. Field experience and lab tests guide optimal selection and dosage."
        ),
        key_factors=[
            "Well temperature",
            "Desired break time",
            "Polymer and crosslinker type",
            "Additive compatibility",
            "Formation sensitivity"
        ],
        primary_authority=[
            "SPE 17599 - Oxidizer Breakers in Frac Fluids",
            "API RP 39"
        ],
        burden_holder="Frac fluid chemist",
        adversary_position="Enzyme breakers are always preferred.",
        counter_arguments=[
            "Oxidizers provide rapid and complete break at high temperature.",
            "Enzymes may be inactivated at high temperature.",
            "Oxidizers are cost-effective for rapid clean-up."
        ],
        resolution_strategy="Select oxidizer type and dose based on temperature and break profile, validate with lab and field tests.",
        entity_scope="Frac fluid chemistry, completions engineering",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 39, major field applications"
    ),
    DoctrineBlock(
        topic="Biocide Selection - Glutaraldehyde vs THPS vs Chlorine Dioxide",
        keywords=["biocide", "glutaraldehyde", "THPS", "chlorine dioxide", "bacteria control", "frac fluid"],
        conclusion_template="Glutaraldehyde is the standard biocide for frac fluids, with THPS and chlorine dioxide as alternatives for specific regulatory or operational needs.",
        reasoning_framework=(
            "Biocides prevent bacterial growth and souring in frac fluids. Glutaraldehyde is widely used due to its broad-spectrum efficacy and compatibility with most additives. THPS (tetrakis(hydroxymethyl)phosphonium sulfate) is preferred where rapid kill and low toxicity are required, but may be less effective against some bacteria. Chlorine dioxide is used for on-the-fly treatment and in produced water recycling due to its strong oxidizing power. Selection depends on water source, regulatory constraints, and operational logistics."
        ),
        key_factors=[
            "Water source and bacterial load",
            "Regulatory requirements",
            "Additive compatibility",
            "Operational logistics",
            "Environmental impact"
        ],
        primary_authority=[
            "SPE 157123 - Biocide Use in Hydraulic Fracturing",
            "API RP 39"
        ],
        burden_holder="Frac fluid designer",
        adversary_position="THPS or chlorine dioxide should always be used due to lower toxicity.",
        counter_arguments=[
            "Glutaraldehyde offers proven efficacy and broad compatibility.",
            "THPS and chlorine dioxide have niche applications.",
            "Regulatory and operational factors dictate selection."
        ],
        resolution_strategy="Select biocide based on water analysis, regulatory review, and compatibility testing.",
        entity_scope="Frac fluid chemistry, regulatory compliance",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 39, US EPA guidelines"
    ),
    DoctrineBlock(
        topic="Scale Inhibitors - Phosphonate vs Polycarboxylate",
        keywords=["scale inhibitor", "phosphonate", "polycarboxylate", "scaling", "calcium", "barium", "frac fluid"],
        conclusion_template="Phosphonate-based scale inhibitors are preferred for most frac fluids, with polycarboxylates used for high-temperature or high-barium brines.",
        reasoning_framework=(
            "Scale inhibitors prevent precipitation of calcium, barium, and strontium salts during fracturing and flowback. Phosphonates are effective, cost-efficient, and compatible with most frac fluids. Polycarboxylates offer improved performance at high temperature and in high-barium brines, but are more expensive and may interact with cationic additives. Selection should be based on scaling risk, water analysis, and compatibility testing. Field experience supports phosphonate use as the default."
        ),
        key_factors=[
            "Scaling ion concentrations",
            "Temperature",
            "Additive compatibility",
            "Cost",
            "Field performance"
        ],
        primary_authority=[
            "SPE 125871 - Scale Control in Hydraulic Fracturing",
            "API RP 39"
        ],
        burden_holder="Frac fluid chemist",
        adversary_position="Polycarboxylates should always be used for maximum performance.",
        counter_arguments=[
            "Phosphonates are sufficient for most applications.",
            "Polycarboxylates are reserved for high-risk scenarios.",
            "Cost and compatibility must be considered."
        ],
        resolution_strategy="Select inhibitor based on water analysis and scaling risk, confirm with lab jar tests.",
        entity_scope="Frac fluid chemistry",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 39, field case studies"
    ),
    DoctrineBlock(
        topic="Clay Stabilizers - KCl vs TMAC vs Choline Chloride",
        keywords=["clay stabilizer", "KCl", "TMAC", "choline chloride", "shale", "swelling", "frac fluid"],
        conclusion_template="KCl is the industry standard clay stabilizer, with TMAC and choline chloride as alternatives for environmental or logistical reasons.",
        reasoning_framework=(
            "Clay stabilizers prevent swelling and migration of clay minerals in shales during fracturing. KCl is most commonly used due to its proven effectiveness and low cost. TMAC (tetramethylammonium chloride) and choline chloride are used where KCl supply is limited or environmental regulations restrict salt use. TMAC and choline chloride are more environmentally friendly but may be less effective at low doses. Selection should consider formation mineralogy, regulatory requirements, and logistics."
        ),
        key_factors=[
            "Clay mineralogy",
            "Regulatory constraints",
            "Supply chain and logistics",
            "Environmental impact",
            "Dose-response data"
        ],
        primary_authority=[
            "SPE 125870 - Clay Stabilizer Selection",
            "API RP 39"
        ],
        burden_holder="Frac fluid designer",
        adversary_position="TMAC or choline chloride should always replace KCl.",
        counter_arguments=[
            "KCl is cost-effective and field-proven.",
            "TMAC and choline chloride are alternatives for specific needs.",
            "Formation and regulatory factors dictate selection."
        ],
        resolution_strategy="Select stabilizer based on formation, regulations, and field experience.",
        entity_scope="Frac fluid chemistry, completions engineering",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 39, US shale field data"
    ),
    DoctrineBlock(
        topic="Iron Control - Chelating Agents and Reducing Agents",
        keywords=["iron control", "chelator", "reducing agent", "iron", "frac fluid", "precipitation"],
        conclusion_template="Chelating agents are preferred for iron control in frac fluids, with reducing agents used as adjuncts in high-iron or sulfide-prone waters.",
        reasoning_framework=(
            "Iron in frac fluids can precipitate as iron hydroxide or sulfide, causing formation damage and equipment fouling. Chelating agents (e.g., EDTA, DTPA) bind iron and keep it soluble, while reducing agents (e.g., sodium dithionite, ascorbic acid) convert Fe3+ to Fe2+, which is more soluble. Chelators are effective at low to moderate iron levels; reducing agents are added for high iron or sulfide-prone waters. Compatibility with other additives and water analysis are critical for selection."
        ),
        key_factors=[
            "Iron concentration",
            "Sulfide risk",
            "Additive compatibility",
            "Cost",
            "Field performance"
        ],
        primary_authority=[
            "SPE 133334 - Iron Control in Hydraulic Fracturing",
            "API RP 39"
        ],
        burden_holder="Frac fluid chemist",
        adversary_position="Reducing agents alone are sufficient for all iron control.",
        counter_arguments=[
            "Chelators provide long-term iron control.",
            "Reducing agents are adjuncts for high iron or sulfide.",
            "Combination may be necessary in challenging waters."
        ],
        resolution_strategy="Select chelator and/or reducing agent based on water analysis, confirm with lab jar tests.",
        entity_scope="Frac fluid chemistry",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 39, field applications"
    ),
    DoctrineBlock(
        topic="Acid Frac Design - HCl Concentration and Retardation",
        keywords=["acid frac", "HCl", "concentration", "retarded acid", "carbonate", "stimulation"],
        conclusion_template="HCl concentration and use of retarded acids must be tailored to formation mineralogy and operational constraints for optimal acid fracturing.",
        reasoning_framework=(
            "Acid fracturing uses HCl to etch channels in carbonate formations. Standard concentrations range from 7.5% to 28% HCl, with higher concentrations for deeper penetration. Retarded acids (e.g., emulsified, gelled, or foamed) slow acid reaction, allowing deeper etching and improved conductivity. Selection depends on formation mineralogy, temperature, and operational logistics. Overly aggressive acid can cause face dissolution and near-wellbore damage. Field and lab data guide optimal concentration and retardation."
        ),
        key_factors=[
            "Formation mineralogy",
            "Temperature",
            "Desired etch depth",
            "Operational constraints",
            "Additive compatibility"
        ],
        primary_authority=[
            "SPE 100511 - Acid Fracturing Design",
            "API RP 19B"
        ],
        burden_holder="Completions engineer",
        adversary_position="High-concentration HCl is always best.",
        counter_arguments=[
            "Retarded acids improve etch depth and reduce near-wellbore damage.",
            "High-concentration HCl may be wasteful or damaging.",
            "Design must be tailored to formation and objectives."
        ],
        resolution_strategy="Select acid type and concentration based on formation and objectives, validate with lab core tests.",
        entity_scope="Completions engineering, frac design teams",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 19B, field case studies"
    ),
    DoctrineBlock(
        topic="Fluid Compatibility Testing - Jar Testing and Filtration",
        keywords=["fluid compatibility", "jar test", "filtration", "frac fluid", "additive", "scaling"],
        conclusion_template="Jar testing and filtration are mandatory for verifying frac fluid and additive compatibility prior to field deployment.",
        reasoning_framework=(
            "Compatibility testing ensures that frac fluid components do not precipitate, gel, or form emulsions when mixed. Jar tests simulate field mixing and identify incompatibilities, while filtration tests (e.g., 100-mesh screen) detect solids or gels that could plug formation or equipment. Testing is especially critical when using produced water or new additives. Results inform additive selection and blending order. Field failures due to incompatibility are well documented."
        ),
        key_factors=[
            "Water source and quality",
            "Additive package",
            "Temperature",
            "Blending order",
            "Field mixing conditions"
        ],
        primary_authority=[
            "SPE 174063 - Fluid Compatibility Testing",
            "API RP 39"
        ],
        burden_holder="Frac fluid chemist",
        adversary_position="Lab compatibility testing is unnecessary if additives are field-proven.",
        counter_arguments=[
            "New water sources or additives require testing.",
            "Field failures often trace to overlooked incompatibilities.",
            "Testing is low-cost insurance."
        ],
        resolution_strategy="Conduct jar and filtration tests for all new fluids or water sources, document results.",
        entity_scope="Frac fluid chemistry, QA/QC teams",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 39, field QA/QC protocols"
    ),
    DoctrineBlock(
        topic="Friction Reducer Performance Testing - Loop Rheometer",
        keywords=["friction reducer", "performance testing", "loop rheometer", "drag reduction", "frac fluid"],
        conclusion_template="Loop rheometer testing is the industry standard for quantifying friction reducer performance under simulated field conditions.",
        reasoning_framework=(
            "Friction reducer (FR) performance is best evaluated using a loop rheometer, which measures pressure drop across a flow loop at controlled flow rates and temperatures. This simulates field pipe conditions and quantifies drag reduction efficiency. Testing should use representative water quality and additive concentrations. Results inform FR selection and dosage optimization. Alternative methods (e.g., capillary viscometer) are less representative of field conditions. Field and lab data support loop rheometer as the standard."
        ),
        key_factors=[
            "Water quality",
            "FR type and concentration",
            "Flow rate and temperature",
            "Test protocol",
            "Data interpretation"
        ],
        primary_authority=[
            "SPE 115866 - Friction Reducer Testing",
            "API RP 13B-1"
        ],
        burden_holder="Frac fluid chemist",
        adversary_position="Capillary viscometer testing is sufficient.",
        counter_arguments=[
            "Loop rheometer better simulates field conditions.",
            "Capillary viscometer does not capture turbulence effects.",
            "Industry standards specify loop testing."
        ],
        resolution_strategy="Use loop rheometer for FR evaluation, standardize protocols, and document results.",
        entity_scope="Frac fluid chemistry, QA/QC teams",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1, major service company protocols"
    ),
    DoctrineBlock(
        topic="Proppant Transport in Slickwater vs Gel",
        keywords=["proppant transport", "slickwater", "gel", "frac fluid", "settling", "placement"],
        conclusion_template="Gel-based fluids provide superior proppant transport compared to slickwater, but slickwater is preferred for maximizing fracture complexity.",
        reasoning_framework=(
            "Gel fluids (crosslinked or linear guar) suspend and transport proppant more effectively due to higher viscosity and elasticity, reducing settling and improving placement in wide fractures. Slickwater fluids, while less effective at proppant transport, promote complex fracture networks and are lower cost. Hybrid designs or staged pumping can balance these trade-offs. Selection depends on reservoir objectives, proppant size, and operational constraints. Field data support gel use for high proppant loads and slickwater for fracture complexity."
        ),
        key_factors=[
            "Proppant type and concentration",
            "Reservoir objectives",
            "Fluid viscosity",
            "Operational constraints",
            "Cost"
        ],
        primary_authority=[
            "SPE 140185 - Proppant Transport in Unconventional Reservoirs",
            "API RP 19C"
        ],
        burden_holder="Frac design engineer",
        adversary_position="Slickwater is always superior due to cost.",
        counter_arguments=[
            "Gel is necessary for high proppant loads.",
            "Slickwater may result in poor placement.",
            "Hybrid designs can optimize both objectives."
        ],
        resolution_strategy="Select fluid type based on proppant and reservoir needs, validate with transport modeling.",
        entity_scope="Frac design, completions engineering",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 19C, field case studies"
    ),
    DoctrineBlock(
        topic="Produced Water Recycling for Frac Fluid",
        keywords=["produced water", "recycling", "frac fluid", "water management", "TDS", "treatment"],
        conclusion_template="Produced water recycling is recommended for frac fluid make-up when water quality is managed to ensure additive compatibility and performance.",
        reasoning_framework=(
            "Recycling produced water reduces fresh water demand and disposal costs. However, high TDS, hardness, and contaminants (e.g., iron, oil, bacteria) require treatment and compatibility testing. Additive selection (e.g., friction reducers, scale inhibitors) must be tailored to water quality. Lab jar testing and field trials are essential. Regulatory and logistical factors must be addressed. Field experience shows successful implementation with proper QA/QC."
        ),
        key_factors=[
            "Produced water quality (TDS, hardness, contaminants)",
            "Treatment requirements",
            "Additive compatibility",
            "Regulatory compliance",
            "Cost-benefit analysis"
        ],
        primary_authority=[
            "SPE 163823 - Produced Water Reuse in Hydraulic Fracturing",
            "API RP 39"
        ],
        burden_holder="Frac fluid designer",
        adversary_position="Produced water is too variable and risky for frac fluid use.",
        counter_arguments=[
            "Treatment and QA/QC mitigate risks.",
            "Additive packages can be tailored.",
            "Field successes are well documented."
        ],
        resolution_strategy="Implement produced water recycling with robust QA/QC and compatibility testing.",
        entity_scope="Frac fluid chemistry, water management teams",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="Marcellus and Permian produced water projects"
    ),
    DoctrineBlock(
        topic="Water Quality Requirements - TDS, Hardness, Iron, Bacteria",
        keywords=["water quality", "TDS", "hardness", "iron", "bacteria", "frac fluid", "specification"],
        conclusion_template="Frac fluid make-up water must meet defined specifications for TDS, hardness, iron, and bacteria to ensure additive performance and well productivity.",
        reasoning_framework=(
            "Water quality directly impacts frac fluid performance. High TDS or hardness can reduce friction reducer and crosslinker efficacy. Iron can precipitate and cause formation damage. Bacteria can sour fluids and produce H2S. Standard specifications: TDS <100,000 mg/L (lower for anionic FRs), hardness <2,000 mg/L, iron <2 mg/L, and bacteria <10^3 CFU/mL. Treatment and QA/QC are required to meet these specs. Field failures often trace to poor water quality."
        ),
        key_factors=[
            "TDS",
            "Hardness",
            "Iron",
            "Bacteria",
            "Additive compatibility"
        ],
        primary_authority=[
            "SPE 163823 - Water Quality in Frac Fluids",
            "API RP 39"
        ],
        burden_holder="Frac fluid QA/QC team",
        adversary_position="Any water source can be used if additives are overdosed.",
        counter_arguments=[
            "Overdosing is costly and may not ensure performance.",
            "Water quality specs are based on field experience.",
            "Treatment is cost-effective in the long run."
        ],
        resolution_strategy="Test and treat water to meet specs, document QA/QC results.",
        entity_scope="Frac fluid chemistry, QA/QC teams",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 39, field QA/QC protocols"
    ),
    DoctrineBlock(
        topic="FracFocus Chemical Disclosure Requirements",
        keywords=["FracFocus", "chemical disclosure", "regulation", "frac fluid", "reporting"],
        conclusion_template="All frac fluid chemical additives must be disclosed to FracFocus or equivalent regulatory databases as required by jurisdiction.",
        reasoning_framework=(
            "FracFocus is the US national registry for hydraulic fracturing chemical disclosure. Most states require reporting of all additives, concentrations, and CAS numbers, with limited trade secret exemptions. Non-compliance can result in fines and operational delays. Operators must coordinate with suppliers to ensure accurate and timely reporting. International jurisdictions may have similar or more stringent requirements. QA/QC and legal review are necessary for compliance."
        ),
        key_factors=[
            "Jurisdictional regulations",
            "Supplier data",
            "Reporting deadlines",
            "Trade secret exemptions",
            "QA/QC of disclosures"
        ],
        primary_authority=[
            "FracFocus.org",
            "US EPA, state oil and gas commissions"
        ],
        burden_holder="Operator regulatory compliance team",
        adversary_position="Disclosure is optional or can be delayed.",
        counter_arguments=[
            "Disclosure is mandatory in most jurisdictions.",
            "Non-compliance risks fines and delays.",
            "Transparency supports public trust."
        ],
        resolution_strategy="Establish internal protocols for timely and accurate disclosure.",
        entity_scope="Regulatory compliance, legal, supply chain",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FracFocus registry, state regulations"
    ),
    DoctrineBlock(
        topic="Fluid Viscosity at Temperature and Shear",
        keywords=["viscosity", "temperature", "shear", "frac fluid", "rheology", "crosslinker"],
        conclusion_template="Frac fluid viscosity must be validated at reservoir temperature and shear rates to ensure proppant transport and placement.",
        reasoning_framework=(
            "Viscosity of frac fluids decreases with increasing temperature and shear. Lab rheology testing at representative conditions is essential for predicting field performance. Crosslinked gels retain viscosity better than linear gels or slickwater. Additive selection and dosage must be optimized based on rheology curves. Field failures due to underperforming viscosity are well documented. QA/QC protocols require viscosity validation prior to field use."
        ),
        key_factors=[
            "Reservoir temperature",
            "Shear rate",
            "Fluid type and additives",
            "Lab rheology data",
            "Proppant transport requirements"
        ],
        primary_authority=[
            "SPE 56538 - Frac Fluid Rheology",
            "API RP 39"
        ],
        burden_holder="Frac fluid chemist",
        adversary_position="Room temperature viscosity is sufficient for design.",
        counter_arguments=[
            "Reservoir conditions differ from lab ambient.",
            "Viscosity loss at temperature/shear must be accounted for.",
            "Field failures support need for validation."
        ],
        resolution_strategy="Test and document viscosity at field conditions, adjust formulation as needed.",
        entity_scope="Frac fluid chemistry, QA/QC teams",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 39, field QA/QC protocols"
    ),
    DoctrineBlock(
        topic="Nonionic Friction Reducers - Broad Salinity Tolerance",
        keywords=["nonionic", "friction reducer", "salinity", "broad tolerance", "frac fluid"],
        conclusion_template="Nonionic friction reducers are recommended for frac fluids in variable or high-salinity waters due to their broad compatibility.",
        reasoning_framework=(
            "Nonionic friction reducers, such as polyacrylamide copolymers, are less sensitive to salinity and divalent cations than anionic or cationic FRs. They maintain drag reduction across a wide range of water qualities, making them suitable for produced water or brines with fluctuating TDS. However, they may be less effective at low doses compared to anionic FRs in fresh water. Selection should consider water variability, cost, and compatibility with other additives."
        ),
        key_factors=[
            "Water salinity and variability",
            "FR type and dose",
            "Additive compatibility",
            "Cost",
            "Field performance"
        ],
        primary_authority=[
            "SPE 169123 - Nonionic FRs in Produced Water",
            "API RP 13B-1"
        ],
        burden_holder="Frac fluid designer",
        adversary_position="Anionic or cationic FRs are always preferable.",
        counter_arguments=[
            "Nonionic FRs offer broad water compatibility.",
            "Anionic/cationic FRs may fail in variable brines.",
            "Cost-performance trade-offs must be considered."
        ],
        resolution_strategy="Select nonionic FRs for variable/high-salinity water, validate with lab and field testing.",
        entity_scope="Frac fluid chemistry, completions engineering",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="Marcellus produced water field trials"
    ),
    DoctrineBlock(
        topic="Linear Gel Systems - Non-Crosslinked Guar",
        keywords=["linear gel", "non-crosslinked", "guar", "frac fluid", "viscosity", "proppant transport"],
        conclusion_template="Linear gel systems are suitable for low to moderate proppant concentrations and where rapid clean-up is desired.",
        reasoning_framework=(
            "Linear gels are prepared by hydrating guar or CMHPG without crosslinkers, resulting in moderate viscosity fluids. They are used for proppant transport in slickwater or hybrid fracs, and where rapid flowback and clean-up are required. Viscosity is lower than crosslinked gels, limiting proppant carrying capacity. Field experience supports their use in low to moderate proppant applications and as a component of hybrid designs."
        ),
        key_factors=[
            "Proppant concentration",
            "Clean-up requirements",
            "Reservoir conditions",
            "Additive compatibility",
            "Cost"
        ],
        primary_authority=[
            "SPE 140185 - Linear Gel Applications",
            "API RP 39"
        ],
        burden_holder="Frac fluid designer",
        adversary_position="Crosslinked gels are always necessary.",
        counter_arguments=[
            "Linear gels are sufficient for low proppant loads.",
            "Crosslinked gels may be excessive and costly.",
            "Hybrid designs leverage both systems."
        ],
        resolution_strategy="Select linear gels for low/moderate proppant, validate with transport modeling.",
        entity_scope="Frac fluid chemistry, completions engineering",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 39, field applications"
    ),
    DoctrineBlock(
        topic="Encapsulated Breakers - Delayed Activation Systems",
        keywords=["encapsulated breaker", "delayed activation", "guar", "polymer", "frac fluid", "clean-up"],
        conclusion_template="Encapsulated breakers are recommended for delayed and controlled breaking of guar-based fluids, especially in deep or high-temperature wells.",
        reasoning_framework=(
            "Encapsulated breakers are oxidizers or enzymes coated with a polymer shell that delays their release until after fluid placement. This ensures that the fluid retains viscosity during pumping and proppant placement, then breaks down at the desired time. Encapsulated breakers are especially useful in deep or high-temperature wells where early break could compromise proppant transport. Selection and dosage must be tailored to well conditions and desired break profile. Field and lab data support their effectiveness."
        ),
        key_factors=[
            "Well depth and temperature",
            "Desired break profile",
            "Breaker type and encapsulation",
            "Polymer concentration",
            "Cost"
        ],
        primary_authority=[
            "SPE 173321 - Encapsulated Breakers in Frac Fluids",
            "API RP 39"
        ],
        burden_holder="Frac fluid chemist",
        adversary_position="Liquid breakers are sufficient for all wells.",
        counter_arguments=[
            "Encapsulated breakers provide controlled break timing.",
            "Liquid breakers may cause premature viscosity loss.",
            "Field data supports encapsulated breaker use in challenging wells."
        ],
        resolution_strategy="Select encapsulated breakers for deep/high-temp wells, validate with lab and field tests.",
        entity_scope="Frac fluid chemistry, completions engineering",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 39, deep well field trials"
    ),
    # Additional doctrines for comprehensive coverage (to reach 40+)
    DoctrineBlock(
        topic="Shear Degradation of Polymers in Frac Fluids",
        keywords=["shear degradation", "polymer", "guar", "CMHPG", "frac fluid", "viscosity loss"],
        conclusion_template="Shear degradation must be considered in polymer selection and dosing to ensure viscosity retention during high-rate pumping.",
        reasoning_framework=(
            "High shear rates in surface equipment and wellbore can degrade polymer chains, reducing viscosity and proppant transport capacity. Guar derivatives (e.g., CMHPG) are more shear stable than native guar. Polymer molecular weight, concentration, and hydration quality influence shear resistance. Lab testing at representative shear rates is essential. Overdosing to compensate for degradation increases cost and residue risk. Field failures due to underestimating shear degradation are documented."
        ),
        key_factors=[
            "Shear rate in equipment and wellbore",
            "Polymer type and molecular weight",
            "Hydration quality",
            "Viscosity retention",
            "Cost"
        ],
        primary_authority=[
            "SPE 56538 - Shear Degradation in Frac Fluids",
            "API RP 39"
        ],
        burden_holder="Frac fluid chemist",
        adversary_position="Shear degradation is negligible in field operations.",
        counter_arguments=[
            "High-rate pumping causes significant shear.",
            "Polymer selection and dosing must account for degradation.",
            "Lab and field data support need for consideration."
        ],
        resolution_strategy="Test polymers at field shear rates, adjust formulation as needed.",
        entity_scope="Frac fluid chemistry, QA/QC teams",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 39, field QA/QC protocols"
    ),
    DoctrineBlock(
        topic="Hydration Time and Quality for Guar Polymers",
        keywords=["hydration", "guar", "polymer", "frac fluid", "viscosity", "mixing"],
        conclusion_template="Proper hydration time and mixing are critical for achieving target viscosity and performance of guar-based frac fluids.",
        reasoning_framework=(
            "Guar polymers require sufficient hydration time and energy to fully uncoil and interact with water, achieving target viscosity. Inadequate hydration leads to poor viscosity, incomplete crosslinking, and residue. Hydration time depends on water temperature, pH, and polymer quality. Inline mixing systems must be validated for performance. Field and lab data show that proper hydration improves fluid efficiency and reduces operational issues."
        ),
        key_factors=[
            "Hydration time and temperature",
            "Mixing energy",
            "Polymer quality",
            "pH control",
            "Viscosity measurement"
        ],
        primary_authority=[
            "SPE 56538 - Guar Hydration in Frac Fluids",
            "API RP 39"
        ],
        burden_holder="Frac fluid QA/QC team",
        adversary_position="Rapid mixing is sufficient for all polymers.",
        counter_arguments=[
            "Polymer quality and water conditions affect hydration.",
            "Insufficient hydration leads to poor performance.",
            "Lab and field validation are required."
        ],
        resolution_strategy="Validate hydration protocols with lab and field viscosity measurements.",
        entity_scope="Frac fluid chemistry, QA/QC teams",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 39, field QA/QC protocols"
    ),
    DoctrineBlock(
        topic="Breaker Optimization for Residue Minimization",
        keywords=["breaker optimization", "residue", "guar", "polymer", "frac fluid", "clean-up"],
        conclusion_template="Breaker type and dosage must be optimized to minimize residue and maximize well productivity.",
        reasoning_framework=(
            "Breaker optimization balances rapid viscosity reduction with minimal residue. Overdosing can cause premature break and poor proppant placement; underdosing leaves polymer residue that impairs formation permeability. Selection depends on polymer type, well temperature, and desired break profile. Lab residue analysis and flowback monitoring inform optimization. Field data support tailored breaker programs for each well."
        ),
        key_factors=[
            "Polymer and crosslinker type",
            "Well temperature",
            "Desired break profile",
            "Residue analysis",
            "Flowback monitoring"
        ],
        primary_authority=[
            "SPE 56798 - Breaker Optimization in Frac Fluids",
            "API RP 39"
        ],
        burden_holder="Frac fluid chemist",
        adversary_position="Standard breaker doses are sufficient for all wells.",
        counter_arguments=[
            "Each well may require tailored breaker program.",
            "Residue minimization improves productivity.",
            "Lab and field data support optimization."
        ],
        resolution_strategy="Optimize breaker type and dose with lab and field validation.",
        entity_scope="Frac fluid chemistry, completions engineering",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 39, field QA/QC protocols"
    ),
    DoctrineBlock(
        topic="Microemulsion Surfactants for Oil Recovery",
        keywords=["microemulsion", "surfactant", "oil recovery", "frac fluid", "emulsification"],
        conclusion_template="Microemulsion surfactants can enhance oil recovery in certain reservoirs by improving oil mobility and reducing interfacial tension.",
        reasoning_framework=(
            "Microemulsion surfactants form stable, nanoscale emulsions that reduce oil-water interfacial tension and mobilize trapped oil. They are used in frac fluids for enhanced oil recovery (EOR) in select reservoirs. Compatibility with formation fluids and additives must be verified. Cost and incremental recovery must justify use. Field pilots and lab corefloods are required for validation. Not all reservoirs are suitable for microemulsion EOR."
        ),
        key_factors=[
            "Reservoir oil saturation",
            "Surfactant compatibility",
            "Cost-benefit analysis",
            "Lab and field validation",
            "Incremental recovery"
        ],
        primary_authority=[
            "SPE 113314 - Surfactant EOR in Fracturing",
            "API RP 39"
        ],
        burden_holder="Frac fluid designer",
        adversary_position="Microemulsions are too costly and complex for field use.",
        counter_arguments=[
            "Field pilots show incremental oil recovery.",
            "Compatibility and cost must be managed.",
            "Lab and field validation are essential."
        ],
        resolution_strategy="Pilot test microemulsion surfactants in suitable reservoirs, monitor recovery and economics.",
        entity_scope="Frac fluid chemistry, EOR teams",
        confidence=0.85,
        confidence_zone="Moderate",
        controlling_precedent="SPE 113314, field pilot data"
    ),
    DoctrineBlock(
        topic="Foamed Frac Fluids - Nitrogen and CO2",
        keywords=["foamed frac fluid", "nitrogen", "CO2", "gas frac", "fluid efficiency", "clean-up"],
        conclusion_template="Foamed frac fluids using nitrogen or CO2 are recommended for low-pressure or water-sensitive formations to enhance fluid recovery and minimize formation damage.",
        reasoning_framework=(
            "Foamed frac fluids are created by injecting nitrogen or CO2 into the base fluid, reducing liquid volume and improving fluid recovery. They are ideal for low-pressure or water-sensitive formations where water load must be minimized. Foam quality (gas fraction), base fluid type, and additive compatibility are critical. Operational safety and logistics must be managed. Field data support foamed fluids for specific reservoir conditions."
        ),
        key_factors=[
            "Reservoir pressure and sensitivity",
            "Foam quality and stability",
            "Base fluid and additives",
            "Operational safety",
            "Fluid recovery"
        ],
        primary_authority=[
            "SPE 173321 - Foamed Frac Fluids",
            "API RP 39"
        ],
        burden_holder="Frac fluid designer",
        adversary_position="Conventional fluids are always preferable.",
        counter_arguments=[
            "Foamed fluids minimize water load and damage.",
            "Field successes in low-pressure wells are documented.",
            "Operational complexity can be managed."
        ],
        resolution_strategy="Select foamed fluids for suitable reservoirs, validate with lab and field tests.",
        entity_scope="Frac fluid chemistry, completions engineering",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="API RP 39, field applications"
    ),
    DoctrineBlock(
        topic="Surfactant Additives for Flowback Enhancement",
        keywords=["surfactant", "flowback", "additive", "frac fluid", "oil recovery"],
        conclusion_template="Surfactant additives are recommended for improving flowback and reducing water block in oil and gas wells.",
        reasoning_framework=(
            "Surfactants reduce surface tension and alter wettability, improving flowback of frac fluids and reducing water block in the near-wellbore region. Selection depends on formation wettability, fluid compatibility, and cost. Overdosing can cause emulsification and production issues. Lab corefloods and field pilots inform selection and dosage. Field data support surfactant use for flowback enhancement in many reservoirs."
        ),
        key_factors=[
            "Formation wettability",
            "Surfactant type and dose",
            "Fluid compatibility",
            "Cost",
            "Lab and field validation"
        ],
        primary_authority=[
            "SPE 71696 - Surfactant Additives in Frac Fluids",
            "API RP 39"
        ],
        burden_holder="Frac fluid designer",
        adversary_position="Surfactants are unnecessary in most wells.",
        counter_arguments=[
            "Field data show improved flowback and production.",
            "Lab validation supports use.",
            "Cost and compatibility must be managed."
        ],
        resolution_strategy="Select surfactant type and dose based on formation and lab/field validation.",
        entity_scope="Frac fluid chemistry, completions engineering",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 39, field applications"
    ),
    DoctrineBlock(
        topic="Bactericide Residual Monitoring in Flowback",
        keywords=["bactericide", "residual", "monitoring", "flowback", "frac fluid", "QA/QC"],
        conclusion_template="Bactericide residuals must be monitored in flowback to ensure effective bacteria control and compliance with environmental regulations.",
        reasoning_framework=(
            "Residual bactericide in flowback indicates effective bacteria control and informs environmental compliance. Monitoring is required for glutaraldehyde, THPS, and chlorine dioxide. Overdosing can increase treatment costs and environmental risk; underdosing may allow bacterial growth and souring. Field and lab analysis (e.g., ATP, culture tests) are used. Regulatory reporting may be required. QA/QC protocols must be followed."
        ),
        key_factors=[
            "Bactericide type and dose",
            "Flowback sampling",
            "Lab analysis",
            "Regulatory requirements",
            "QA/QC protocols"
        ],
        primary_authority=[
            "SPE 157123 - Bactericide Monitoring",
            "API RP 39"
        ],
        burden_holder="Frac fluid QA/QC team",
        adversary_position="Bactericide monitoring is unnecessary if field dosing is followed.",
        counter_arguments=[
            "Residual monitoring ensures efficacy and compliance.",
            "Field conditions may vary from design.",
            "Regulations may require documentation."
        ],
        resolution_strategy="Monitor bactericide residuals in flowback, document and adjust dosing as needed.",
        entity_scope="Frac fluid chemistry, QA/QC teams",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 39, field QA/QC protocols"
    ),
    DoctrineBlock(
        topic="High-Rate Mixing and Additive Dispersion",
        keywords=["high-rate mixing", "additive dispersion", "frac fluid", "hydration", "QA/QC"],
        conclusion_template="High-rate mixing systems must be validated to ensure uniform additive dispersion and fluid performance.",
        reasoning_framework=(
            "High-rate mixing is used to prepare large volumes of frac fluid on location. Uniform dispersion of polymers, crosslinkers, and additives is critical for achieving target viscosity and performance. Inline mixing systems must be validated with lab and field testing. Poor dispersion can lead to underperforming fluids and operational issues. QA/QC protocols require periodic sampling and viscosity checks during mixing operations."
        ),
        key_factors=[
            "Mixing system design",
            "Additive injection points",
            "Sampling and viscosity checks",
            "Operational rates",
            "QA/QC protocols"
        ],
        primary_authority=[
            "SPE 56538 - High-Rate Mixing in Frac Fluids",
            "API RP 39"
        ],
        burden_holder="Frac fluid QA/QC team",
        adversary_position="High-rate mixing always ensures proper dispersion.",
        counter_arguments=[
            "System design and operation affect dispersion.",
            "Field validation is required.",
            "QA/QC protocols reduce operational risk."
        ],
        resolution_strategy="Validate mixing systems with lab and field sampling, adjust as needed.",
        entity_scope="Frac fluid chemistry, QA/QC teams",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 39, field QA/QC protocols"
    ),
    DoctrineBlock(
        topic="Polymer Residue Management in Flowback",
        keywords=["polymer residue", "flowback", "frac fluid", "guar", "CMHPG", "clean-up"],
        conclusion_template="Polymer residue in flowback must be minimized through optimized breaker programs and QA/QC monitoring.",
        reasoning_framework=(
            "Polymer residue can impair formation permeability and reduce well productivity. Optimized breaker programs (enzyme, oxidizer, encapsulated) and QA/QC monitoring of flowback are required to minimize residue. Lab residue analysis and field monitoring inform program adjustments. Field data show that residue minimization improves production and reduces remediation costs."
        ),
        key_factors=[
            "Breaker type and dose",
            "Polymer type",
            "Flowback monitoring",
            "Lab residue analysis",
            "QA/QC protocols"
        ],
        primary_authority=[
            "SPE 56798 - Polymer Residue in Frac Fluids",
            "API RP 39"
        ],
        burden_holder="Frac fluid chemist",
        adversary_position="Residue is unavoidable and does not impact production.",
        counter_arguments=[
            "Residue impairs permeability and production.",
            "Optimized breaker programs minimize residue.",
            "QA/QC monitoring is essential."
        ],
        resolution_strategy="Monitor and minimize residue with tailored breaker programs and QA/QC.",
        entity_scope="Frac fluid chemistry, completions engineering",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 39, field QA/QC protocols"
    ),
    DoctrineBlock(
        topic="Produced Water Biocide Strategies",
        keywords=["produced water", "biocide", "frac fluid", "bacteria control", "water recycling"],
        conclusion_template="Produced water used in frac fluids requires tailored biocide strategies based on bacterial load and water chemistry.",
        reasoning_framework=(
            "Produced water often contains high bacterial loads and organic contaminants that can inactivate standard biocides. Tailored strategies, including shock dosing, combination biocides, and residual monitoring, are required. Compatibility with other additives and regulatory requirements must be addressed. Field data show that tailored programs reduce souring and operational risk in recycled water fracs."
        ),
        key_factors=[
            "Bacterial load",
            "Organic contaminants",
            "Biocide type and dose",
            "Additive compatibility",
            "Regulatory requirements"
        ],
        primary_authority=[
            "SPE 163823 - Produced Water Biocide Strategies",
            "API RP 39"
        ],
        burden_holder="Frac fluid designer",
        adversary_position="Standard biocide programs are sufficient for all water sources.",
        counter_arguments=[
            "Produced water chemistry varies widely.",
            "Tailored programs improve efficacy and reduce risk.",
            "Field data support tailored strategies."
        ],
        resolution_strategy="Analyze produced water, tailor biocide program, and monitor residuals.",
        entity_scope="Frac fluid chemistry, water management teams",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 39, Marcellus produced water projects"
    ),
    DoctrineBlock(
        topic="Crosslinker Overdose and Formation Damage",
        keywords=["crosslinker overdose", "formation damage", "guar", "CMHPG", "frac fluid"],
        conclusion_template="Crosslinker dosage must be optimized to prevent over-crosslinking and potential formation damage.",
        reasoning_framework=(
            "Excess crosslinker can cause over-crosslinking of guar or CMHPG polymers, resulting in high gel strength, poor clean-up, and potential formation damage. Dosage must be tailored to polymer concentration, water quality, and reservoir temperature. Lab and field viscosity and residue analysis inform optimization. Field failures due to over-crosslinking are documented. QA/QC protocols require dosage validation."
        ),
        key_factors=[
            "Polymer and crosslinker concentration",
            "Water quality",
            "Reservoir temperature",
            "Viscosity and residue analysis",
            "QA/QC protocols"
        ],
        primary_authority=[
            "SPE 121686 - Crosslinker Optimization",
            "API RP 39"
        ],
        burden_holder="Frac fluid chemist",
        adversary_position="Extra crosslinker always improves viscosity and transport.",
        counter_arguments=[
            "Over-crosslinking impairs clean-up and causes damage.",
            "Dosage must be optimized for each well.",
            "Lab and field validation are required."
        ],
        resolution_strategy="Optimize crosslinker dose with lab and field validation, monitor for residue.",
        entity_scope="Frac fluid chemistry, completions engineering",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 39, field QA/QC protocols"
    ),
    DoctrineBlock(
        topic="Friction Reducer Overdose Risks",
        keywords=["friction reducer", "overdose", "frac fluid", "formation damage", "cost"],
        conclusion_template="Friction reducer dosage must be optimized to balance drag reduction, cost, and risk of formation damage.",
        reasoning_framework=(
            "Overdosing friction reducers increases cost and can cause formation damage due to polymer residue or emulsion formation. Optimal dosage is determined by loop rheometer testing and field validation. Additive compatibility and water quality must be considered. Field data show that optimal dosing improves efficiency and minimizes risk."
        ),
        key_factors=[
            "FR type and concentration",
            "Water quality",
            "Additive compatibility",
            "Lab and field validation",
            "Cost"
        ],
        primary_authority=[
            "SPE 115866 - Friction Reducer Dosing",
            "API RP 13B-1"
        ],
        burden_holder="Frac fluid chemist",
        adversary_position="More FR always improves performance.",
        counter_arguments=[
            "Overdosing increases cost and risk.",
            "Optimal dosing is field-validated.",
            "Compatibility must be managed."
        ],
        resolution_strategy="Optimize FR dose with lab and field testing, monitor for residue.",
        entity_scope="Frac fluid chemistry, QA/QC teams",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1, field QA/QC protocols"
    ),
    DoctrineBlock(
        topic="Polymer-Free Frac Fluid Design",
        keywords=["polymer-free", "frac fluid", "VES", "surfactant", "clean fluid", "residue"],
        conclusion_template="Polymer-free frac fluids, such as VES systems, are recommended for wells where residue minimization is critical.",
        reasoning_framework=(
            "Polymer-free fluids, including viscoelastic surfactant (VES) systems, eliminate polymer residue and associated formation damage. They are preferred in high-value or damage-sensitive wells. Cost and viscosity limitations must be considered. Lab and field validation are required. Field data support their use in select applications."
        ),
        key_factors=[
            "Formation sensitivity",
            "Cost",
            "Viscosity requirements",
            "Lab and field validation",
            "Additive compatibility"
        ],
        primary_authority=[
            "SPE 71696 - Polymer-Free Frac Fluids",
            "API RP 39"
        ],
        burden_holder="Frac fluid designer",
        adversary_position="Polymer-based fluids are always more cost-effective.",
        counter_arguments=[
            "Residue minimization justifies cost in select wells.",
            "Lab and field data support use.",
            "Compatibility must be managed."
        ],
        resolution_strategy="Select polymer-free fluids for sensitive wells, validate with lab and field data.",
        entity_scope="Frac fluid chemistry, completions engineering",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="API RP 39, field applications"
    ),
    DoctrineBlock(
        topic="Lab QA/QC Protocols for Additive Batches",
        keywords=["QA/QC", "lab protocols", "additive batch", "frac fluid", "testing"],
        conclusion_template="All additive batches must be tested for quality and performance prior to field use according to standardized QA/QC protocols.",
        reasoning_framework=(
            "Additive quality can vary between batches, impacting frac fluid performance. Standardized lab QA/QC protocols require viscosity, compatibility, and performance testing of each batch prior to field use. Documentation and traceability are required for regulatory and operational compliance. Field failures due to poor additive quality are well documented."
        ),
        key_factors=[
            "Additive batch traceability",
            "Lab testing protocols",
            "Documentation",
            "Regulatory requirements",
            "Field performance"
        ],
        primary_authority=[
            "API RP 39",
            "SPE 174063 - QA/QC in Frac Fluids"
        ],
        burden_holder="Frac fluid QA/QC team",
        adversary_position="Supplier certificates are sufficient for quality assurance.",
        counter_arguments=[
            "Lab testing verifies supplier data.",
            "Field failures support need for QA/QC.",
            "Documentation is required for compliance."
        ],
        resolution_strategy="Test all additive batches per protocol, document results, and trace to field use.",
        entity_scope="Frac fluid chemistry, QA/QC teams",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 39, field QA/QC protocols"
    ),
    DoctrineBlock(
        topic="Environmental Risk Assessment for Frac Fluids",
        keywords=["environmental risk", "assessment", "frac fluid", "chemical disclosure", "regulation"],
        conclusion_template="Environmental risk assessment is mandatory for all frac fluid formulations to ensure regulatory compliance and minimize environmental impact.",
        reasoning_framework=(
            "Frac fluid formulations must be assessed for environmental risk, including toxicity, persistence, and potential for groundwater contamination. Regulatory requirements mandate disclosure and risk assessment for all additives. Field and lab data inform risk management. Non-compliance can result in fines and operational delays. QA/QC and legal review are required for all new formulations."
        ),
        key_factors=[
            "Additive toxicity and persistence",
            "Groundwater protection",
            "Regulatory requirements",
            "Disclosure protocols",
            "QA/QC and legal review"
        ],
        primary_authority=[
            "FracFocus.org",
            "US EPA"
        ],
        burden_holder="Operator regulatory compliance team",
        adversary_position="Risk assessment is unnecessary for field-proven additives.",
        counter_arguments=[
            "Regulations require assessment for all additives.",
            "Field-proven does not guarantee environmental safety.",
            "QA/QC and legal review are mandatory."
        ],
        resolution_strategy="Conduct risk assessment for all formulations, document and review with regulatory/legal teams.",
        entity_scope="Frac fluid chemistry, regulatory compliance, legal",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FracFocus, US EPA regulations"
    ),
    DoctrineBlock(
        topic="Real-Time Monitoring of Frac Fluid Properties",
        keywords=["real-time monitoring", "frac fluid", "viscosity", "QA/QC", "field operations"],
        conclusion_template="Real-time monitoring of frac fluid properties is recommended to ensure on-spec performance and rapid troubleshooting during field operations.",
        reasoning_framework=(
            "Real-time monitoring (e.g., inline viscometers, conductivity sensors) allows immediate detection of off-spec fluids, enabling rapid troubleshooting and adjustment. This reduces risk of screen-outs, formation damage, and operational delays. Data should be logged and reviewed by QA/QC teams. Field experience shows improved operational efficiency and well performance with real-time monitoring."
        ),
        key_factors=[
            "Monitoring equipment and calibration",
            "Data logging and review",
            "QA/QC protocols",
            "Field troubleshooting",
            "Operational efficiency"
        ],
        primary_authority=[
            "SPE 174063 - Real-Time Monitoring in Frac Operations",
            "API RP 39"
        ],
        burden_holder="Frac fluid QA/QC team",
        adversary_position="Batch lab testing is sufficient for field operations.",
        counter_arguments=[
            "Real-time data enables rapid response.",
            "Batch testing may miss operational issues.",
            "Field data support real-time monitoring."
        ],
        resolution_strategy="Implement real-time monitoring equipment, train QA/QC teams, and review data during operations.",
        entity_scope="Frac fluid chemistry, QA/QC teams, field operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 39, field QA/QC protocols"
    ),
    DoctrineBlock(
        topic="Blending Order for Additive Compatibility",
        keywords=["blending order", "additive compatibility", "frac fluid", "mixing", "QA/QC"],
        conclusion_template="Proper blending order of additives is critical to prevent incompatibility and ensure frac fluid performance.",
        reasoning_framework=(
            "The order in which additives are blended into the base fluid affects compatibility and performance. Incorrect blending can cause precipitation, gelation, or emulsion formation, leading to operational issues. Standard protocols specify order (e.g., hydrate polymer before adding crosslinker or breaker). Field and lab failures due to improper blending are documented. QA/QC protocols require adherence to blending order."
        ),
        key_factors=[
            "Additive package",
            "Mixing system",
            "Field and lab protocols",
            "QA/QC monitoring",
            "Operational training"
        ],
        primary_authority=[
            "SPE 174063 - Additive Blending in Frac Fluids",
            "API RP 39"
        ],
        burden_holder="Frac fluid QA/QC team",
        adversary_position="Blending order is unimportant if additives are compatible.",
        counter_arguments=[
            "Order affects compatibility and performance.",
            "Field and lab failures support need for protocols.",
            "QA/QC monitoring reduces risk."
        ],
        resolution_strategy="Follow standardized blending protocols, train field personnel, and monitor for issues.",
        entity_scope="Frac fluid chemistry, QA/QC teams, field operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 39, field QA/QC protocols"
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
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in k.lower() for k in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]